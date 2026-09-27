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
import { decryptSecret } from "@/lib/security/token-crypto";
import { classifyHttpError, redactSummary } from "@/lib/publishing/errors";
import { getMediaStagingProvider } from "@/lib/publishing/media/staging";
import { probeVideo, validateForPlatform } from "@/lib/publishing/media/ffprobe";

function baseCaps(extra: Partial<PlatformCapabilities> = {}): PlatformCapabilities {
  return {
    canConnect: true,
    canUploadVideo: false,
    canPublishDirectly: false,
    canUploadDraft: false,
    canScheduleNatively: false,
    canSetThumbnail: false,
    canSetPrivacy: false,
    canReadPublishStatus: true,
    canRetrievePostUrl: true,
    canDeletePost: false,
    requiresAppReview: true,
    requiresManualCompletion: true,
    limitations: [],
    ...extra,
  };
}

export class InstagramPublishingAdapter implements PublishingAdapter {
  platform = "instagram_reels" as const;
  id = "instagram";
  label = "Instagram Reels";

  getCapabilities(connection?: PlatformConnectionRecord | null): PlatformCapabilities {
    const connected =
      connection?.connectionStatus === "connected" &&
      Boolean(connection.instagramBusinessAccountId);
    return baseCaps({
      canUploadVideo: connected,
      canPublishDirectly: connected,
      canSetThumbnail: connected,
      requiresManualCompletion: !connected,
      limitations: [
        "Requires Instagram professional account linked to a Facebook Page",
        "App Review usually required for content publishing permissions",
        "Uses resumable upload for local files (or public video URL when staged)",
        ...(connected ? [] : ["Select an Instagram professional account after Meta OAuth"]),
      ],
    });
  }

  async validateConnection(connection: PlatformConnectionRecord): Promise<ConnectionValidationResult> {
    const caps = this.getCapabilities(connection);
    if (!connection.accessTokenEncrypted) {
      return { ok: false, status: "expired", capabilities: caps, errors: ["Missing Meta token"], warnings: [] };
    }
    if (!connection.instagramBusinessAccountId) {
      return {
        ok: false,
        status: "requires_attention",
        capabilities: caps,
        errors: [
          "Your Facebook account is connected, but no eligible Instagram professional account is selected.",
        ],
        warnings: [],
      };
    }
    return {
      ok: true,
      status: "connected",
      accountName: connection.accountName || undefined,
      accountUsername: connection.accountUsername || undefined,
      capabilities: this.getCapabilities(connection),
      errors: [],
      warnings: [],
    };
  }

  async validatePost(post: PlatformPostRecord) {
    const errors: string[] = [];
    const warnings: string[] = [];
    if (!post.caption && !post.title) errors.push("Caption required");
    const file = post.mediaFilePath || post.exportPath;
    if (!file) errors.push("Video file missing");
    else {
      const probe = await probeVideo(file);
      const check = validateForPlatform("instagram_reels", probe);
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
    if (!connection.instagramBusinessAccountId) {
      return {
        success: false,
        published: false,
        message: "No Instagram professional account selected",
        method: "api",
        errorCategory: "configuration",
        retryable: false,
      };
    }
    if (context.dryRun) {
      return {
        success: true,
        published: false,
        message: "Dry-run: Instagram Reel container/publish not sent",
        method: "dry_run",
      };
    }

    const staging = getMediaStagingProvider();
    const filePath = post.mediaFilePath || post.exportPath!;
    const staged = await staging.stageMedia(filePath);
    const igId = connection.instagramBusinessAccountId;
    const caption = post.caption || post.title || "";

    let containerId: string;
    if (staged.publicUrl) {
      const createUrl = new URL(`https://graph.facebook.com/v21.0/${igId}/media`);
      createUrl.searchParams.set("media_type", "REELS");
      createUrl.searchParams.set("caption", caption);
      createUrl.searchParams.set("video_url", staged.publicUrl);
      createUrl.searchParams.set("share_to_feed", "true");
      createUrl.searchParams.set("access_token", context.accessToken);
      const createRes = await fetch(createUrl, { method: "POST" });
      const createBody = await createRes.json();
      if (!createRes.ok || !createBody.id) {
        const c = classifyHttpError(createRes.status, JSON.stringify(createBody));
        return {
          success: false,
          published: false,
          message: "Instagram container creation failed",
          method: "api",
          errorCategory: c.category,
          retryable: c.retryable,
          httpStatus: createRes.status,
          responseSummary: redactSummary(createBody),
        };
      }
      containerId = String(createBody.id);
    } else {
      const resumable = await createIgResumableReel({
        igId,
        caption,
        filePath: staged.localPath,
        accessToken: context.accessToken,
      });
      if (!resumable.ok) {
        return {
          success: false,
          published: false,
          message: resumable.message,
          method: "api",
          errorCategory: resumable.errorCategory || "media_processing",
          retryable: Boolean(resumable.retryable),
          httpStatus: resumable.httpStatus,
          responseSummary: resumable.responseSummary,
          requiresManualCompletion: resumable.requiresManualCompletion,
        };
      }
      containerId = resumable.containerId!;
    }

    const ready = await pollIgContainer(containerId, context.accessToken);
    if (!ready.ok) {
      return {
        success: false,
        published: false,
        message: ready.message,
        method: "api",
        errorCategory: "media_processing",
        retryable: true,
        externalUploadId: containerId,
      };
    }

    const publishUrl = new URL(`https://graph.facebook.com/v21.0/${igId}/media_publish`);
    publishUrl.searchParams.set("creation_id", containerId);
    publishUrl.searchParams.set("access_token", context.accessToken);
    const pubRes = await fetch(publishUrl, { method: "POST" });
    const pubBody = await pubRes.json();
    if (!pubRes.ok || !pubBody.id) {
      const c = classifyHttpError(pubRes.status, JSON.stringify(pubBody));
      return {
        success: false,
        published: false,
        message: "Instagram publish failed",
        method: "api",
        errorCategory: c.category,
        retryable: c.retryable,
        httpStatus: pubRes.status,
        responseSummary: redactSummary(pubBody),
        externalUploadId: containerId,
      };
    }

    const mediaId = String(pubBody.id);
    let permalink: string | undefined;
    try {
      const per = await fetch(
        `https://graph.facebook.com/v21.0/${mediaId}?fields=permalink&access_token=${encodeURIComponent(context.accessToken)}`,
      );
      const perBody = await per.json();
      permalink = perBody.permalink;
    } catch {
      /* optional */
    }

    return {
      success: true,
      published: true,
      platformPostId: mediaId,
      platformUrl: permalink,
      externalUploadId: containerId,
      message: "Instagram Reel published",
      method: "api",
      responseSummary: redactSummary({ id: mediaId }),
    };
  }

  async getExternalStatus(
    externalPostId: string,
    connection: PlatformConnectionRecord,
  ): Promise<ExternalPublishStatus> {
    if (!connection.accessTokenEncrypted) return { status: "unknown", detail: "No token" };
    const token = decryptSecret(connection.accessTokenEncrypted);
    const res = await fetch(
      `https://graph.facebook.com/v21.0/${externalPostId}?fields=id,permalink&access_token=${encodeURIComponent(token)}`,
    );
    const body = await res.json();
    if (!res.ok) return { status: "failed", detail: redactSummary(body), platformPostId: externalPostId };
    return {
      status: "published",
      platformPostId: externalPostId,
      platformUrl: body.permalink,
      detail: "Found",
    };
  }
}

export class FacebookPublishingAdapter implements PublishingAdapter {
  platform = "facebook_reels" as const;
  id = "facebook";
  label = "Facebook Reels";

  getCapabilities(connection?: PlatformConnectionRecord | null): PlatformCapabilities {
    const connected = connection?.connectionStatus === "connected" && Boolean(connection.pageId);
    return baseCaps({
      canUploadVideo: connected,
      canPublishDirectly: connected,
      requiresManualCompletion: !connected,
      limitations: [
        "Publishes to a Facebook Page only",
        ...(connected ? [] : ["Select a manageable Facebook Page after Meta OAuth"]),
      ],
    });
  }

  async validateConnection(connection: PlatformConnectionRecord): Promise<ConnectionValidationResult> {
    const caps = this.getCapabilities(connection);
    if (!connection.pageId) {
      return {
        ok: false,
        status: "requires_attention",
        capabilities: caps,
        errors: ["Your Facebook account is connected, but no manageable Page was found/selected."],
        warnings: [],
      };
    }
    return {
      ok: true,
      status: "connected",
      accountName: connection.accountName || undefined,
      capabilities: caps,
      errors: [],
      warnings: [],
    };
  }

  async validatePost(post: PlatformPostRecord) {
    const errors: string[] = [];
    const warnings: string[] = [];
    if (!post.caption && !post.title) errors.push("Description/caption required");
    const file = post.mediaFilePath || post.exportPath;
    if (!file) errors.push("Video file missing");
    else {
      const probe = await probeVideo(file);
      const check = validateForPlatform("facebook_reels", probe);
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
    if (!connection.pageId) {
      return {
        success: false,
        published: false,
        message: "No Facebook Page selected",
        method: "api",
        errorCategory: "configuration",
        retryable: false,
      };
    }
    if (context.dryRun) {
      return {
        success: true,
        published: false,
        message: "Dry-run: Facebook Reel not sent",
        method: "dry_run",
      };
    }

    const staging = getMediaStagingProvider();
    const filePath = post.mediaFilePath || post.exportPath!;
    const staged = await staging.stageMedia(filePath);
    const description = post.caption || post.title || "";

    if (staged.publicUrl) {
      const url = new URL(`https://graph.facebook.com/v21.0/${connection.pageId}/videos`);
      url.searchParams.set("file_url", staged.publicUrl);
      url.searchParams.set("description", description);
      url.searchParams.set("published", "true");
      url.searchParams.set("access_token", context.accessToken);
      const res = await fetch(url, { method: "POST" });
      const body = await res.json();
      if (!res.ok || !body.id) {
        const c = classifyHttpError(res.status, JSON.stringify(body));
        return {
          success: false,
          published: false,
          message: "Facebook video publish failed",
          method: "api",
          errorCategory: c.category,
          retryable: c.retryable,
          httpStatus: res.status,
          responseSummary: redactSummary(body),
          requiresManualCompletion: true,
        };
      }
      const id = String(body.id);
      return {
        success: true,
        published: true,
        platformPostId: id,
        platformUrl: `https://www.facebook.com/reel/${id}`,
        message: "Facebook video/Reel publish recorded",
        method: "api",
        responseSummary: redactSummary({ id }),
      };
    }

    const reel = await publishFacebookReelResumable({
      pageId: connection.pageId,
      filePath: staged.localPath,
      description,
      accessToken: context.accessToken,
    });
    if (!reel.ok) {
      return {
        success: false,
        published: false,
        message: reel.message,
        method: "api",
        errorCategory: reel.errorCategory || "media_processing",
        retryable: Boolean(reel.retryable),
        httpStatus: reel.httpStatus,
        responseSummary: reel.responseSummary,
        requiresManualCompletion: true,
      };
    }
    return {
      success: true,
      published: true,
      platformPostId: reel.videoId!,
      platformUrl: `https://www.facebook.com/reel/${reel.videoId}`,
      message: "Facebook Reel published via resumable upload",
      method: "api",
      responseSummary: redactSummary({ id: reel.videoId }),
    };
  }

  async getExternalStatus(externalPostId: string): Promise<ExternalPublishStatus> {
    return {
      status: "published",
      platformPostId: externalPostId,
      platformUrl: `https://www.facebook.com/reel/${externalPostId}`,
      detail: "Assumed published when ID known; reconcile if needed",
    };
  }
}

async function pollIgContainer(
  containerId: string,
  token: string,
  maxAttempts = 30,
): Promise<{ ok: boolean; message: string }> {
  for (let i = 0; i < maxAttempts; i++) {
    const res = await fetch(
      `https://graph.facebook.com/v21.0/${containerId}?fields=status_code&access_token=${encodeURIComponent(token)}`,
    );
    const body = await res.json();
    const code = body.status_code;
    if (code === "FINISHED") return { ok: true, message: "ready" };
    if (code === "ERROR") return { ok: false, message: redactSummary(body) };
    await new Promise((r) => setTimeout(r, 2000));
  }
  return { ok: false, message: "Instagram container processing timed out" };
}

type ResumableResult = {
  ok: boolean;
  message: string;
  containerId?: string;
  videoId?: string;
  errorCategory?: PublishResult["errorCategory"];
  retryable?: boolean;
  httpStatus?: number;
  responseSummary?: string;
  requiresManualCompletion?: boolean;
};

async function createIgResumableReel(args: {
  igId: string;
  caption: string;
  filePath: string;
  accessToken: string;
}): Promise<ResumableResult> {
  const fs = await import("fs/promises");
  const buf = await fs.readFile(args.filePath);
  const createUrl = new URL(`https://graph.facebook.com/v21.0/${args.igId}/media`);
  createUrl.searchParams.set("media_type", "REELS");
  createUrl.searchParams.set("upload_type", "resumable");
  createUrl.searchParams.set("caption", args.caption);
  createUrl.searchParams.set("share_to_feed", "true");
  createUrl.searchParams.set("access_token", args.accessToken);
  const createRes = await fetch(createUrl, { method: "POST" });
  const createBody = await createRes.json();
  if (!createRes.ok || !createBody.id) {
    const c = classifyHttpError(createRes.status, JSON.stringify(createBody));
    return {
      ok: false,
      message: "Instagram resumable container creation failed",
      errorCategory: c.category,
      retryable: c.retryable,
      httpStatus: createRes.status,
      responseSummary: redactSummary(createBody),
    };
  }
  const containerId = String(createBody.id);
  const uploadUri =
    createBody.uri || createBody.upload_url || createBody.video_upload?.uri;
  if (!uploadUri) {
    return {
      ok: false,
      message: "Instagram resumable upload URI missing from container response",
      containerId,
      errorCategory: "configuration",
      retryable: false,
      responseSummary: redactSummary(createBody),
      requiresManualCompletion: true,
    };
  }
  const upRes = await fetch(uploadUri, {
    method: "POST",
    headers: {
      Authorization: `OAuth ${args.accessToken}`,
      offset: "0",
      file_size: String(buf.byteLength),
      "Content-Type": "application/octet-stream",
    },
    body: buf,
  });
  if (!upRes.ok) {
    const text = await upRes.text();
    const c = classifyHttpError(upRes.status, text);
    return {
      ok: false,
      message: "Instagram resumable binary upload failed",
      containerId,
      errorCategory: c.category,
      retryable: c.retryable,
      httpStatus: upRes.status,
      responseSummary: redactSummary(text),
    };
  }
  return { ok: true, message: "uploaded", containerId };
}

async function publishFacebookReelResumable(args: {
  pageId: string;
  filePath: string;
  description: string;
  accessToken: string;
}): Promise<ResumableResult> {
  const fs = await import("fs/promises");
  const buf = await fs.readFile(args.filePath);
  const startUrl = new URL(`https://graph.facebook.com/v21.0/${args.pageId}/video_reels`);
  startUrl.searchParams.set("upload_phase", "start");
  startUrl.searchParams.set("file_size", String(buf.byteLength));
  startUrl.searchParams.set("access_token", args.accessToken);
  const startRes = await fetch(startUrl, { method: "POST" });
  const startBody = await startRes.json();
  if (!startRes.ok || !startBody.video_id || !startBody.upload_url) {
    const c = classifyHttpError(startRes.status, JSON.stringify(startBody));
    return {
      ok: false,
      message: "Facebook Reel upload session start failed",
      errorCategory: c.category,
      retryable: c.retryable,
      httpStatus: startRes.status,
      responseSummary: redactSummary(startBody),
    };
  }
  const videoId = String(startBody.video_id);
  const upRes = await fetch(String(startBody.upload_url), {
    method: "POST",
    headers: {
      Authorization: `OAuth ${args.accessToken}`,
      offset: "0",
      file_size: String(buf.byteLength),
      "Content-Type": "application/octet-stream",
    },
    body: buf,
  });
  if (!upRes.ok) {
    const text = await upRes.text();
    const c = classifyHttpError(upRes.status, text);
    return {
      ok: false,
      message: "Facebook Reel binary upload failed",
      videoId,
      errorCategory: c.category,
      retryable: c.retryable,
      httpStatus: upRes.status,
      responseSummary: redactSummary(text),
    };
  }
  const finishUrl = new URL(`https://graph.facebook.com/v21.0/${args.pageId}/video_reels`);
  finishUrl.searchParams.set("upload_phase", "finish");
  finishUrl.searchParams.set("video_id", videoId);
  finishUrl.searchParams.set("video_state", "PUBLISHED");
  finishUrl.searchParams.set("description", args.description);
  finishUrl.searchParams.set("access_token", args.accessToken);
  const finishRes = await fetch(finishUrl, { method: "POST" });
  const finishBody = await finishRes.json();
  if (!finishRes.ok) {
    const c = classifyHttpError(finishRes.status, JSON.stringify(finishBody));
    return {
      ok: false,
      message: "Facebook Reel finish/publish failed",
      videoId,
      errorCategory: c.category,
      retryable: c.retryable,
      httpStatus: finishRes.status,
      responseSummary: redactSummary(finishBody),
    };
  }
  return { ok: true, message: "published", videoId };
}
