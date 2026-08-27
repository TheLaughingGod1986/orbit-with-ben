import {
  buildSocialUtmParams,
  normalizeAffiliateClickSource,
  type AffiliateClickSource,
} from "./social-channels";
import { isPlaceholderAffiliateUrl } from "./live-product-urls";
import {
  buildOrbitRedirectUrl,
  getAffiliateRedirectBaseUrl,
} from "./go-redirect-urls";

export {
  buildOrbitRedirectUrl,
  buildYouTubeDescriptionGoUrl,
  getAffiliateRedirectBaseUrl,
} from "./go-redirect-urls";

/**
 * Resolve affiliate IDs from env / admin config.
 * Never hard-code real affiliate IDs in source or seed.
 */
export function getAmazonAssociateTag(): string | null {
  return process.env.AMAZON_ASSOCIATE_TAG?.trim() || null;
}

/**
 * Merchant URL used for /go 302. Prefer stored affiliateUrl when it is a real URL;
 * otherwise build from destinationUrl (tag stamped by applyProgrammeAffiliateId).
 */
export function resolveAffiliateRedirectBase(args: {
  destinationUrl: string;
  affiliateUrl?: string | null;
}): string {
  const aff = args.affiliateUrl?.trim() || "";
  if (aff && !isPlaceholderAffiliateUrl(aff)) return aff;
  return args.destinationUrl;
}

export function getBrilliantAffiliateId(): string | null {
  return process.env.BRILLIANT_AFFILIATE_ID?.trim() || null;
}

function applyUtmToUrl(
  rawUrl: string,
  utm: {
    utm_source: string;
    utm_medium: string;
    utm_campaign: string;
    utm_content?: string;
  },
): string {
  let url: URL;
  try {
    url = new URL(rawUrl);
  } catch {
    try {
      const base = getAffiliateRedirectBaseUrl().replace(/\/go\/?$/, "");
      url = new URL(rawUrl.startsWith("/") ? rawUrl : `/${rawUrl}`, `${base}/`);
    } catch {
      return rawUrl;
    }
  }
  url.searchParams.set("utm_source", utm.utm_source);
  url.searchParams.set("utm_medium", utm.utm_medium);
  url.searchParams.set("utm_campaign", utm.utm_campaign);
  if (utm.utm_content) url.searchParams.set("utm_content", utm.utm_content);
  return url.toString();
}

/**
 * Build destination URL with UTM params while preserving existing programme tracking.
 */
export function buildTrackedAffiliateUrl(args: {
  affiliateUrl: string;
  videoSlug?: string | null;
  productSlug: string;
  utmSource?: string;
  utmMedium?: string;
  utmCampaign?: string;
  utmContent?: string;
}): string {
  let url: URL;
  try {
    url = new URL(args.affiliateUrl);
  } catch {
    return args.affiliateUrl;
  }

  const source = normalizeAffiliateClickSource(args.utmSource);
  const medium = args.utmMedium ?? "affiliate";
  const campaign = args.utmCampaign ?? args.videoSlug ?? "orbit";
  const content = args.utmContent ?? args.productSlug;

  if (!url.searchParams.has("utm_source")) url.searchParams.set("utm_source", source);
  if (!url.searchParams.has("utm_medium")) url.searchParams.set("utm_medium", medium);
  if (!url.searchParams.has("utm_campaign")) url.searchParams.set("utm_campaign", campaign);
  if (!url.searchParams.has("utm_content")) url.searchParams.set("utm_content", content);

  return url.toString();
}

/**
 * Orbit /go/{slug} link for social posts with channel UTMs.
 * Never a merchant URL.
 */
export function buildSocialGoUrl(args: {
  productSlug: string;
  platform: string;
  videoSlug: string;
  hasAffiliateMention?: boolean;
}): string {
  const utm = buildSocialUtmParams({
    platform: args.platform,
    videoSlug: args.videoSlug,
    productSlug: args.productSlug,
    hasAffiliateMention: args.hasAffiliateMention !== false,
  });
  return applyUtmToUrl(buildOrbitRedirectUrl(args.productSlug), utm);
}

/**
 * YouTube film URL with social UTMs (still never a merchant URL).
 */
export function buildSocialYouTubeUrl(args: {
  youtubeUrl: string;
  platform: string;
  videoSlug: string;
  productSlug?: string | null;
  hasAffiliateMention?: boolean;
}): string {
  const utm = buildSocialUtmParams({
    platform: args.platform,
    videoSlug: args.videoSlug,
    productSlug: args.productSlug,
    hasAffiliateMention: Boolean(args.hasAffiliateMention && args.productSlug),
  });
  return applyUtmToUrl(args.youtubeUrl, utm);
}

export type { AffiliateClickSource };

/**
 * Apply programme affiliate tag to a destination URL when the env ID is present.
 */
export function applyProgrammeAffiliateId(
  affiliateUrl: string,
  programmeSlug: string,
): string {
  try {
    const url = new URL(affiliateUrl);
    if (programmeSlug === "amazon-associates-uk") {
      const tag = getAmazonAssociateTag();
      if (tag) url.searchParams.set("tag", tag);
    }
    if (programmeSlug === "brilliant") {
      const id = getBrilliantAffiliateId();
      if (id && !url.searchParams.has("ref")) {
        url.searchParams.set("ref", id);
      }
    }
    return url.toString();
  } catch {
    return affiliateUrl;
  }
}
