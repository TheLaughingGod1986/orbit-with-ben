import { ManualPublishingAdapter } from "@/lib/publishing/adapters/manual";
import { YouTubePublishingAdapter } from "@/lib/publishing/adapters/youtube";
import {
  InstagramPublishingAdapter,
  FacebookPublishingAdapter,
} from "@/lib/publishing/adapters/meta";
import { TikTokPublishingAdapter } from "@/lib/publishing/adapters/tiktok";
import { XPublishingAdapter } from "@/lib/publishing/adapters/x";
import { ThreadsPublishingAdapter } from "@/lib/publishing/adapters/threads";
import {
  LegacyAdapterPost,
  LegacyPublishResult,
  LegacyPublishStatus,
  PublishingAdapter,
} from "@/lib/publishing/types";
import {
  hasGoogleOAuth,
  hasMetaOAuth,
  hasTikTokOAuth,
  hasThreadsOAuth,
  hasXOAuth,
} from "@/lib/env";

export type {
  PublishResult,
  PublishStatus,
  AdapterPost,
  PublishingAdapter as LegacyPublishingAdapterInterface,
} from "@/lib/publishing/adapters-legacy-types";

export {
  ManualPublishingAdapter,
  YouTubePublishingAdapter,
  InstagramPublishingAdapter,
  FacebookPublishingAdapter,
  TikTokPublishingAdapter,
  XPublishingAdapter,
  ThreadsPublishingAdapter,
};

/** Compatibility wrapper so existing tests can call publish/getStatus without connection context. */
class LegacyFacade {
  constructor(private adapter: PublishingAdapter) {}

  get id() {
    return this.adapter.id;
  }
  get label() {
    return this.adapter.label;
  }

  async validate(post: LegacyAdapterPost) {
    if (this.adapter instanceof ManualPublishingAdapter) {
      return this.adapter.validate(post);
    }
    return this.adapter.validatePost({
      id: post.id,
      platform: post.platform,
      title: post.title,
      caption: post.caption,
      uploadStatus: post.uploadStatus,
      exportPath: post.exportPath,
    });
  }

  async publish(post: LegacyAdapterPost): Promise<LegacyPublishResult> {
    if (this.adapter instanceof ManualPublishingAdapter) {
      return this.adapter.legacyPublish(post);
    }
    // Without a real connection, refuse to fake success.
    return {
      success: false,
      message:
        "API publishing requires a connected account. Use Settings → Connections, or export a manual upload package.",
      method: "manual",
    };
  }

  async getStatus(): Promise<LegacyPublishStatus> {
    if (this.adapter instanceof ManualPublishingAdapter) {
      return this.adapter.legacyGetStatus();
    }
    if (this.adapter.platform === "youtube_shorts") {
      return hasGoogleOAuth()
        ? {
            status: "unknown",
            detail: "Google OAuth credentials detected. Connect the channel on /settings/connections.",
            connection: "api_available",
          }
        : {
            status: "unknown",
            detail: "YouTube API credentials not configured.",
            connection: "manual_upload_required",
          };
    }
    if (this.adapter.platform === "tiktok") {
      return hasTikTokOAuth()
        ? {
            status: "unknown",
            detail: "TikTok credentials present; connect account and confirm draft/direct scopes.",
            connection: "api_unavailable",
          }
        : {
            status: "unknown",
            detail: "No live API status — track URLs manually after upload.",
            connection: "manual_upload_required",
          };
    }
    if (this.adapter.platform === "instagram_reels" || this.adapter.platform === "facebook_reels") {
      return hasMetaOAuth()
        ? {
            status: "unknown",
            detail: "Meta app credentials present; unrestricted Reels publishing requires review + Page/IG selection.",
            connection: "api_unavailable",
          }
        : {
            status: "unknown",
            detail: "No live API status — track URLs manually after upload.",
            connection: "manual_upload_required",
          };
    }
    if (this.adapter.platform === "x") {
      return hasXOAuth()
        ? {
            status: "unknown",
            detail: "X credentials present; confirm write access plan before publishing.",
            connection: "api_available",
          }
        : {
            status: "unknown",
            detail: "No live API status — track URLs manually after upload.",
            connection: "manual_upload_required",
          };
    }
    if (this.adapter.platform === "threads") {
      return hasThreadsOAuth()
        ? {
            status: "unknown",
            detail: "Threads credentials present; connect after product approval.",
            connection: "api_unavailable",
          }
        : {
            status: "unknown",
            detail: "No live API status — track URLs manually after upload.",
            connection: "manual_upload_required",
          };
    }
    return {
      status: "unknown",
      detail: "No live API status — track URLs manually after upload.",
      connection: "manual_upload_required",
    };
  }
}

export function getPublishingAdapter(platform: string): PublishingAdapter {
  switch (platform) {
    case "youtube_shorts":
      return new YouTubePublishingAdapter();
    case "meta":
    case "instagram_reels":
      return new InstagramPublishingAdapter();
    case "instagram_feed":
      // Feed captions use the same Meta connection; publish path is manual until Graph feed is wired.
      return new ManualPublishingAdapter("instagram_feed", "Instagram Feed");
    case "facebook_reels":
      return new FacebookPublishingAdapter();
    case "facebook_page":
      return new ManualPublishingAdapter("facebook_page", "Facebook Page");
    case "tiktok":
      return new TikTokPublishingAdapter();
    case "x":
      return new XPublishingAdapter();
    case "threads":
      return new ThreadsPublishingAdapter();
    default:
      return new ManualPublishingAdapter(platform, platform);
  }
}

/** Legacy entry used by settings page + tests. */
export function getAdapterForPlatform(platform: string): LegacyFacade {
  return new LegacyFacade(getPublishingAdapter(platform));
}

export class YouTubeAdapter extends LegacyFacade {
  constructor() {
    super(new YouTubePublishingAdapter());
  }
}
export class TikTokAdapter extends LegacyFacade {
  constructor() {
    super(new TikTokPublishingAdapter());
  }
}
export class MetaAdapter extends LegacyFacade {
  constructor() {
    super(new InstagramPublishingAdapter());
  }
}
export class XAdapter extends LegacyFacade {
  constructor() {
    super(new XPublishingAdapter());
  }
}
