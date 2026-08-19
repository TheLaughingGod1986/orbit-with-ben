/**
 * Live Orbit social channels for affiliate-aware copy.
 * Tracked URLs on social: YouTube film or Orbit /go/{slug} only.
 */

export const AFFILIATE_CLICK_SOURCES = [
  "youtube",
  "threads",
  "instagram",
  "facebook",
  "tiktok",
  "x",
  "other",
] as const;
export type AffiliateClickSource = (typeof AFFILIATE_CLICK_SOURCES)[number];

/** Platforms Ben asked to integrate for affiliate social copy. */
export const AFFILIATE_LIVE_SOCIAL_PLATFORMS = [
  "threads",
  "instagram_reels",
  "instagram_feed",
  "facebook_page",
] as const;

export type AffiliateLiveSocialPlatform =
  (typeof AFFILIATE_LIVE_SOCIAL_PLATFORMS)[number];

/**
 * Map Content Ops platform id → AffiliateClick.source / utm_source.
 * Reels and feed share the same public channel source.
 */
export function socialPlatformToClickSource(
  platform: string,
): AffiliateClickSource {
  switch (platform) {
    case "threads":
      return "threads";
    case "instagram_reels":
    case "instagram_feed":
    case "instagram":
      return "instagram";
    case "facebook_page":
    case "facebook_reels":
    case "facebook":
      return "facebook";
    case "tiktok":
      return "tiktok";
    case "x":
      return "x";
    case "youtube_shorts":
    case "youtube":
      return "youtube";
    default:
      return "other";
  }
}

/**
 * Normalise inbound utm_source / click source to a reporting bucket.
 * Missing / empty / whitespace → `other` (not youtube). Probe and health
 * checks must not inflate YouTube. Explicit `utm_source=youtube` still maps
 * to youtube; unknown values also fall through to `other`.
 */
export function normalizeAffiliateClickSource(
  raw: string | null | undefined,
): AffiliateClickSource {
  const s = (raw || "").trim().toLowerCase();
  if (!s) return "other";
  if (s === "instagram_reels" || s === "instagram_feed" || s === "ig") return "instagram";
  if (s === "facebook_page" || s === "facebook_reels" || s === "fb") return "facebook";
  if ((AFFILIATE_CLICK_SOURCES as readonly string[]).includes(s)) {
    return s as AffiliateClickSource;
  }
  return "other";
}

/**
 * UTM map for social → /go/ or YouTube links.
 * utm_source = threads | instagram | facebook | …
 * utm_medium = affiliate when a product is mentioned, else social
 * utm_campaign = video slug
 * utm_content = product slug when mentioned
 */
export function buildSocialUtmParams(args: {
  platform: string;
  videoSlug: string;
  productSlug?: string | null;
  hasAffiliateMention: boolean;
}): {
  utm_source: AffiliateClickSource;
  utm_medium: "affiliate" | "social";
  utm_campaign: string;
  utm_content?: string;
} {
  const utm_source = socialPlatformToClickSource(args.platform);
  return {
    utm_source,
    utm_medium: args.hasAffiliateMention ? "affiliate" : "social",
    utm_campaign: args.videoSlug,
    utm_content: args.productSlug || undefined,
  };
}
