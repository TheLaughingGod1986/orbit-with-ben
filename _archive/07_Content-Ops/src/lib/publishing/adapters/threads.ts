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
import { getMediaStagingProvider } from "@/lib/publishing/media/staging";

/**
 * Threads Graph API is officially supported by Meta.
 * Practical enablement still requires Threads product access + scopes on the app.
 */
export class ThreadsPublishingAdapter implements PublishingAdapter {
  platform = "threads" as const;
  id = "threads";
  label = "Threads";

  getCapabilities(connection?: PlatformConnectionRecord | null): PlatformCapabilities {
    const env = getEnv();
    const appReady = Boolean(env.THREADS_APP_ID && env.THREADS_APP_SECRET);
    const connected = connection?.connectionStatus === "connected";
    const scopes = connection?.grantedScopes ? JSON.parse(connection.grantedScopes) : [];
    const canPublish =
      appReady &&
      connected &&
      scopes.some((s: string) => s.includes("threads_content_publish"));
    return {
      canConnect: appReady,
      canUploadVideo: canPublish,
      canPublishDirectly: canPublish,
      canUploadDraft: false,
      canScheduleNatively: false,
      canSetThumbnail: false,
      canSetPrivacy: false,
      canReadPublishStatus: canPublish,
      canRetrievePostUrl: canPublish,
      canDeletePost: false,
      requiresAppReview: true,
      requiresManualCompletion: !canPublish,
      limitations: [
        !appReady
          ? "Threads app credentials not configured — retain manual export"
          : !connected
            ? "Connect Threads OAuth after Meta Threads product is enabled"
            : !canPublish
              ? "threads_content_publish scope missing or app not approved"
              : "Respect Threads rate limits (≈250 posts / 24h)",
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
    if (!caps.canPublishDirectly) {
      return {
        ok: false,
        status: "requires_attention",
        capabilities: caps,
        errors: caps.limitations,
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
      warnings: [],
    };
  }

  async validatePost(post: PlatformPostRecord) {
    const text = post.caption || post.title || "";
    const errors: string[] = [];
    if (!text.trim()) errors.push("Threads text required");
    return { ok: errors.length === 0, errors, warnings: [] };
  }

  async publish(
    post: PlatformPostRecord,
    connection: PlatformConnectionRecord,
    context: PublishingContext,
  ): Promise<PublishResult> {
    const caps = this.getCapabilities(connection);
    if (!caps.canPublishDirectly || !connection.externalUserId) {
      return {
        success: false,
        published: false,
        message: caps.limitations[0] || "Threads publishing unavailable",
        method: "manual",
        errorCategory: "configuration",
        retryable: false,
        requiresManualCompletion: true,
      };
    }
    if (context.dryRun) {
      return {
        success: true,
        published: false,
        message: "Dry-run: Threads publish not sent",
        method: "dry_run",
      };
    }

    const userId = connection.externalUserId;
    const text = post.caption || post.title || "";
    let mediaType = "TEXT";
    let videoUrl: string | undefined;
    const file = post.mediaFilePath || post.exportPath;
    if (file) {
      const staged = await getMediaStagingProvider().stageMedia(file);
      if (staged.publicUrl) {
        mediaType = "VIDEO";
        videoUrl = staged.publicUrl;
      }
    }

    const createParams = new URLSearchParams({
      media_type: mediaType,
      text,
      access_token: context.accessToken,
    });
    if (videoUrl) createParams.set("video_url", videoUrl);

    const createRes = await fetch(`https://graph.threads.net/v1.0/${userId}/threads`, {
      method: "POST",
      body: createParams,
    });
    const createBody = await createRes.json();
    if (!createRes.ok || !createBody.id) {
      const c = classifyHttpError(createRes.status, JSON.stringify(createBody));
      return {
        success: false,
        published: false,
        message: "Threads container create failed",
        method: "api",
        errorCategory: c.category,
        retryable: c.retryable,
        httpStatus: createRes.status,
        responseSummary: redactSummary(createBody),
      };
    }

    const publishRes = await fetch(`https://graph.threads.net/v1.0/${userId}/threads_publish`, {
      method: "POST",
      body: new URLSearchParams({
        creation_id: createBody.id,
        access_token: context.accessToken,
      }),
    });
    const publishBody = await publishRes.json();
    if (!publishRes.ok || !publishBody.id) {
      const c = classifyHttpError(publishRes.status, JSON.stringify(publishBody));
      return {
        success: false,
        published: false,
        message: "Threads publish failed",
        method: "api",
        errorCategory: c.category,
        retryable: c.retryable,
        httpStatus: publishRes.status,
        responseSummary: redactSummary(publishBody),
      };
    }
    const id = String(publishBody.id);
    const username = connection.accountUsername || "user";
    return {
      success: true,
      published: true,
      platformPostId: id,
      platformUrl: `https://www.threads.net/@${username}/post/${id}`,
      message: "Published to Threads",
      method: "api",
      responseSummary: redactSummary({ id }),
    };
  }

  async getExternalStatus(
    externalPostId: string,
    connection: PlatformConnectionRecord,
  ): Promise<ExternalPublishStatus> {
    const username = connection.accountUsername || "user";
    return {
      status: "published",
      platformPostId: externalPostId,
      platformUrl: `https://www.threads.net/@${username}/post/${externalPostId}`,
      detail: "URL constructed from ID",
    };
  }
}
