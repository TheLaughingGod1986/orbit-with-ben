import {
  ConnectionValidationResult,
  ExternalPublishStatus,
  PlatformCapabilities,
  PlatformConnectionRecord,
  PlatformPostRecord,
  PublishingAdapter,
  PublishingContext,
  PublishResult,
} from "@/lib/publishing/types";
import { classifyHttpError, redactSummary } from "@/lib/publishing/errors";
import { probeVideo, validateForPlatform } from "@/lib/publishing/media/ffprobe";
import fs from "fs";

function scopesOf(connection?: PlatformConnectionRecord | null): string[] {
  if (!connection?.grantedScopes) return [];
  try {
    return JSON.parse(connection.grantedScopes);
  } catch {
    return [];
  }
}

export class TikTokPublishingAdapter implements PublishingAdapter {
  platform = "tiktok" as const;
  id = "tiktok";
  label = "TikTok";

  getCapabilities(connection?: PlatformConnectionRecord | null): PlatformCapabilities {
    const scopes = scopesOf(connection);
    const connected = connection?.connectionStatus === "connected";
    const canDraft = connected && scopes.some((s) => s.includes("video.upload"));
    const canDirect = connected && scopes.some((s) => s.includes("video.publish"));
    return {
      canConnect: true,
      canUploadVideo: canDraft || canDirect,
      canPublishDirectly: canDirect,
      canUploadDraft: canDraft,
      canScheduleNatively: false,
      canSetThumbnail: false,
      canSetPrivacy: canDirect,
      canReadPublishStatus: canDirect,
      canRetrievePostUrl: false,
      canDeletePost: false,
      requiresAppReview: true,
      requiresManualCompletion: !canDirect,
      limitations: [
        canDraft && !canDirect
          ? "Direct Post unavailable. TikTok draft upload is available."
          : !canDraft
            ? "TikTok Content Posting scopes not granted / not approved"
            : "Unaudited Direct Post clients are restricted to SELF_ONLY",
      ],
    };
  }

  async validateConnection(connection: PlatformConnectionRecord): Promise<ConnectionValidationResult> {
    const caps = this.getCapabilities(connection);
    if (!connection.accessTokenEncrypted) {
      return { ok: false, status: "expired", capabilities: caps, errors: ["Missing TikTok token"], warnings: [] };
    }
    if (!caps.canUploadDraft && !caps.canPublishDirectly) {
      return {
        ok: false,
        status: "requires_attention",
        capabilities: caps,
        errors: ["TikTok draft upload and Direct Post are both unavailable for this app/user."],
        warnings: [],
      };
    }
    return {
      ok: true,
      status: "connected",
      accountName: connection.accountName || undefined,
      accountUsername: connection.accountUsername || undefined,
      capabilities: caps,
      errors: [],
      warnings: caps.limitations,
    };
  }

  async validatePost(post: PlatformPostRecord) {
    const errors: string[] = [];
    const warnings: string[] = [];
    const file = post.mediaFilePath || post.exportPath;
    if (!file) errors.push("Video file missing");
    else {
      const probe = await probeVideo(file);
      const check = validateForPlatform("tiktok", probe);
      errors.push(...check.errors);
      warnings.push(...check.warnings);
    }
    return { ok: errors.length === 0, errors, warnings };
  }

  async publish(
    post: PlatformPostRecord,
    connection: PlatformConnectionRecord,
    context: PublishingContext,
  ): Promise<PublishResult> {
    const caps = this.getCapabilities(connection);
    const validation = await this.validatePost(post);
    if (!validation.ok) {
      return {
        success: false,
        published: false,
        message: validation.errors.join("; "),
        method: "api",
        errorCategory: "validation",
        retryable: false,
      };
    }
    if (process.env.TIKTOK_UPLOADS_PAUSED === "1" || process.env.TIKTOK_UPLOADS_PAUSED === "true") {
      return {
        success: false,
        published: false,
        message: "TikTok uploads paused (account ban). Ben must lift before any post.",
        method: "api",
        errorCategory: "validation",
        retryable: false,
      };
    }
    try {
      const blockPath = "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok/TIKTOK_UPLOAD_BLOCK.json";
      if (fs.existsSync(blockPath)) {
        const block = JSON.parse(fs.readFileSync(blockPath, "utf8")) as { paused?: boolean };
        if (block.paused) {
          return {
            success: false,
            published: false,
            message: "TikTok uploads paused (account ban). Ben must lift TIKTOK_UPLOAD_BLOCK.json.",
            method: "api",
            errorCategory: "validation",
            retryable: false,
          };
        }
      }
    } catch {
      /* ignore unreadable lock — env flag still applies */
    }

    if (context.dryRun) {
      return {
        success: true,
        published: false,
        message: caps.canPublishDirectly
          ? "Dry-run: TikTok Direct Post not sent"
          : "Dry-run: TikTok draft upload not sent",
        method: "dry_run",
      };
    }

    const filePath = post.mediaFilePath || post.exportPath!;
    const size = fs.statSync(filePath).size;

    if (caps.canPublishDirectly) {
      return this.directPost(post, context, filePath, size);
    }
    if (caps.canUploadDraft) {
      return this.draftUpload(context, filePath, size);
    }
    return {
      success: false,
      published: false,
      message: "TikTok publishing unavailable for this connection",
      method: "manual",
      errorCategory: "permission",
      retryable: false,
      requiresManualCompletion: true,
    };
  }

  private async draftUpload(
    context: PublishingContext,
    filePath: string,
    size: number,
  ): Promise<PublishResult> {
    const initRes = await fetch("https://open.tiktokapis.com/v2/post/publish/inbox/video/init/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${context.accessToken}`,
        "Content-Type": "application/json; charset=UTF-8",
      },
      body: JSON.stringify({
        source_info: {
          source: "FILE_UPLOAD",
          video_size: size,
          chunk_size: size,
          total_chunk_count: 1,
        },
      }),
    });
    const initBody = await initRes.json();
    if (!initRes.ok || !initBody?.data?.upload_url) {
      const c = classifyHttpError(initRes.status, JSON.stringify(initBody));
      return {
        success: false,
        published: false,
        message: "TikTok draft init failed",
        method: "draft_upload",
        errorCategory: c.category,
        retryable: c.retryable,
        httpStatus: initRes.status,
        responseSummary: redactSummary(initBody),
      };
    }
    const uploadUrl = initBody.data.upload_url as string;
    const publishId = initBody.data.publish_id as string | undefined;
    const buf = fs.readFileSync(filePath);
    const put = await fetch(uploadUrl, {
      method: "PUT",
      headers: {
        "Content-Type": "video/mp4",
        "Content-Range": `bytes 0-${buf.length - 1}/${buf.length}`,
      },
      body: buf,
    });
    if (!put.ok) {
      return {
        success: false,
        published: false,
        message: "TikTok draft media transfer failed",
        method: "draft_upload",
        errorCategory: "network",
        retryable: true,
        httpStatus: put.status,
      };
    }
    return {
      success: true,
      published: false,
      externalUploadId: publishId,
      message:
        "TikTok draft uploaded. Open TikTok and complete publication from inbox. Do not mark published until you record the live URL.",
      method: "draft_upload",
      requiresManualCompletion: true,
      responseSummary: redactSummary({ publishId }),
    };
  }

  private async directPost(
    post: PlatformPostRecord,
    context: PublishingContext,
    filePath: string,
    size: number,
  ): Promise<PublishResult> {
    const privacy = post.privacyStatus || "SELF_ONLY";
    const initRes = await fetch("https://open.tiktokapis.com/v2/post/publish/video/init/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${context.accessToken}`,
        "Content-Type": "application/json; charset=UTF-8",
      },
      body: JSON.stringify({
        post_info: {
          title: (post.title || post.caption || "Orbit").slice(0, 150),
          privacy_level: privacy,
          disable_duet: false,
          disable_comment: false,
          disable_stitch: false,
        },
        source_info: {
          source: "FILE_UPLOAD",
          video_size: size,
          chunk_size: size,
          total_chunk_count: 1,
        },
      }),
    });
    const initBody = await initRes.json();
    if (!initRes.ok || !initBody?.data?.upload_url) {
      const c = classifyHttpError(initRes.status, JSON.stringify(initBody));
      return {
        success: false,
        published: false,
        message: "TikTok Direct Post init failed",
        method: "api",
        errorCategory: c.category,
        retryable: c.retryable,
        httpStatus: initRes.status,
        responseSummary: redactSummary(initBody),
      };
    }
    const uploadUrl = initBody.data.upload_url as string;
    const publishId = String(initBody.data.publish_id || "");
    const buf = fs.readFileSync(filePath);
    const put = await fetch(uploadUrl, {
      method: "PUT",
      headers: {
        "Content-Type": "video/mp4",
        "Content-Range": `bytes 0-${buf.length - 1}/${buf.length}`,
      },
      body: buf,
    });
    if (!put.ok) {
      return {
        success: false,
        published: false,
        message: "TikTok Direct Post transfer failed",
        method: "api",
        errorCategory: "network",
        retryable: true,
        httpStatus: put.status,
      };
    }

    // Poll status — only mark published when TikTok reports PUBLISH_COMPLETE
    for (let i = 0; i < 20; i++) {
      await new Promise((r) => setTimeout(r, 2000));
      const statusRes = await fetch(
        "https://open.tiktokapis.com/v2/post/publish/status/fetch/",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${context.accessToken}`,
            "Content-Type": "application/json; charset=UTF-8",
          },
          body: JSON.stringify({ publish_id: publishId }),
        },
      );
      const statusBody = await statusRes.json();
      const status = statusBody?.data?.status;
      if (status === "PUBLISH_COMPLETE") {
        return {
          success: true,
          published: true,
          platformPostId: publishId,
          message: "TikTok Direct Post completed",
          method: "api",
          responseSummary: redactSummary(statusBody),
        };
      }
      if (status === "FAILED") {
        return {
          success: false,
          published: false,
          message: "TikTok reported FAILED",
          method: "api",
          errorCategory: "permanent_platform",
          retryable: false,
          responseSummary: redactSummary(statusBody),
        };
      }
    }
    return {
      success: false,
      published: false,
      message: "TikTok processing still pending — reconcile later; do not retry blindly",
      method: "api",
      errorCategory: "media_processing",
      retryable: false,
      externalUploadId: publishId,
    };
  }

  async getExternalStatus(externalPostId: string): Promise<ExternalPublishStatus> {
    return {
      status: "unknown",
      platformPostId: externalPostId,
      detail: "Use status fetch with an active token / reconcile manually for drafts",
    };
  }
}
