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
import { getEnv } from "@/lib/env";
import fs from "fs";

export class XPublishingAdapter implements PublishingAdapter {
  platform = "x" as const;
  id = "x";
  label = "X";

  getCapabilities(connection?: PlatformConnectionRecord | null): PlatformCapabilities {
    const env = getEnv();
    const oauthConfigured = Boolean(env.X_CLIENT_ID && env.X_CLIENT_SECRET);
    const connected = connection?.connectionStatus === "connected";
    const scopes = connection?.grantedScopes ? JSON.parse(connection.grantedScopes) : [];
    const canWrite = scopes.includes("tweet.write") || scopes.includes("tweet.write".toLowerCase());
    // Access-plan gate: without OAuth client we treat posting as unavailable.
    const planAllows = oauthConfigured;
    return {
      canConnect: oauthConfigured,
      canUploadVideo: connected && canWrite && planAllows,
      canPublishDirectly: connected && canWrite && planAllows,
      canUploadDraft: false,
      canScheduleNatively: false,
      canSetThumbnail: false,
      canSetPrivacy: false,
      canReadPublishStatus: connected,
      canRetrievePostUrl: true,
      canDeletePost: false,
      requiresAppReview: false,
      requiresManualCompletion: !(connected && canWrite && planAllows),
      limitations: [
        !oauthConfigured
          ? "Your X API access plan / app credentials do not include the required posting configuration."
          : !connected
            ? "Connect X OAuth before publishing"
            : !canWrite
              ? "tweet.write scope missing"
              : "Pay-per-use / write access must be active in the X developer portal",
      ],
    };
  }

  async validateConnection(connection: PlatformConnectionRecord): Promise<ConnectionValidationResult> {
    const caps = this.getCapabilities(connection);
    if (!caps.canConnect) {
      return {
        ok: false,
        status: "unsupported",
        capabilities: caps,
        errors: caps.limitations,
        warnings: [],
      };
    }
    if (!connection.accessTokenEncrypted) {
      return { ok: false, status: "expired", capabilities: caps, errors: ["Missing X token"], warnings: [] };
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
    const text = post.caption || post.title || "";
    if (!text.trim()) errors.push("Post text required");
    if (text.length > 280) errors.push("X post exceeds 280 characters");
    return { ok: errors.length === 0, errors, warnings: [] };
  }

  async publish(
    post: PlatformPostRecord,
    connection: PlatformConnectionRecord,
    context: PublishingContext,
  ): Promise<PublishResult> {
    const caps = this.getCapabilities(connection);
    if (!caps.canPublishDirectly) {
      return {
        success: false,
        published: false,
        message: caps.limitations[0] || "X publishing unavailable",
        method: "manual",
        errorCategory: "configuration",
        retryable: false,
        requiresManualCompletion: true,
      };
    }
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
    if (context.dryRun) {
      return {
        success: true,
        published: false,
        message: "Dry-run: X post not sent",
        method: "dry_run",
      };
    }

    let mediaIds: string[] = [];
    const file = post.mediaFilePath || post.exportPath;
    if (file && fs.existsSync(file) && fs.statSync(file).isFile()) {
      // Media upload requires eligible plan — attempt and fall back to text-only with clear error if blocked.
      const media = await uploadXMedia(context.accessToken, file);
      if (!media.ok) {
        return {
          success: false,
          published: false,
          message: media.message,
          method: "api",
          errorCategory: media.category,
          retryable: media.retryable,
          requiresManualCompletion: true,
        };
      }
      mediaIds = [media.mediaId!];
    }

    const body: Record<string, unknown> = {
      text: post.caption || post.title,
    };
    if (mediaIds.length) body.media = { media_ids: mediaIds };

    const res = await fetch("https://api.x.com/2/tweets", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${context.accessToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    const json = await res.json();
    if (!res.ok || !json?.data?.id) {
      const c = classifyHttpError(res.status, JSON.stringify(json));
      return {
        success: false,
        published: false,
        message: "X create tweet failed",
        method: "api",
        errorCategory: c.category,
        retryable: c.retryable,
        httpStatus: res.status,
        responseSummary: redactSummary(json),
      };
    }
    const id = String(json.data.id);
    const username = connection.accountUsername || "i";
    return {
      success: true,
      published: true,
      platformPostId: id,
      platformUrl: `https://x.com/${username}/status/${id}`,
      message: "Posted to X",
      method: "api",
      responseSummary: redactSummary({ id }),
    };
  }

  async getExternalStatus(externalPostId: string, connection: PlatformConnectionRecord): Promise<ExternalPublishStatus> {
    const username = connection.accountUsername || "i";
    return {
      status: "published",
      platformPostId: externalPostId,
      platformUrl: `https://x.com/${username}/status/${externalPostId}`,
      detail: "URL constructed from ID",
    };
  }
}

async function uploadXMedia(
  token: string,
  filePath: string,
): Promise<{
  ok: boolean;
  mediaId?: string;
  message: string;
  category?: PublishResult["errorCategory"];
  retryable?: boolean;
}> {
  // Simplified single-request media upload attempt against upload.twitter.com legacy endpoint
  // If plan blocks it, return configuration error — never fake success.
  try {
    const buf = fs.readFileSync(filePath);
    const form = new FormData();
    form.append("media", new Blob([buf]), "video.mp4");
    const res = await fetch("https://upload.twitter.com/1.1/media/upload.json?media_category=tweet_video", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: form,
    });
    const body = await res.json().catch(() => ({}));
    if (!res.ok || !body.media_id_string) {
      return {
        ok: false,
        message:
          "X media upload unavailable under the current API configuration/plan. Post text-only or use manual upload.",
        category: "configuration",
        retryable: false,
      };
    }
    return { ok: true, mediaId: String(body.media_id_string), message: "ok" };
  } catch (err) {
    return {
      ok: false,
      message: err instanceof Error ? err.message : "media upload failed",
      category: "network",
      retryable: true,
    };
  }
}
