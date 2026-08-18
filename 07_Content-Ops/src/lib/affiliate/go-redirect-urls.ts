import { getEnv } from "@/lib/env";

/**
 * Bare /go redirect helpers — kept free of social-channels / film-topic-book-map
 * imports so placement tables can stamp YouTube description URLs without a
 * circular module graph (description → editorial-trust → film-map → urls).
 */

export function getAffiliateRedirectBaseUrl(): string {
  const fromEnv = process.env.AFFILIATE_REDIRECT_BASE_URL?.trim();
  if (fromEnv) return fromEnv.replace(/\/$/, "");
  try {
    const env = getEnv();
    return `${env.APP_BASE_URL.replace(/\/$/, "")}/go`;
  } catch {
    return "http://localhost:3000/go";
  }
}

/** Public tracked redirect: `${APP_BASE_URL}/go/{slug}` (or AFFILIATE_REDIRECT_BASE_URL). */
export function buildOrbitRedirectUrl(productSlug: string): string {
  return `${getAffiliateRedirectBaseUrl()}/${encodeURIComponent(productSlug)}`;
}

/**
 * YouTube description `/go/` door — always stamps `utm_source=youtube` so live
 * description clicks are not recorded as `other` after the missing-source default.
 * Fills medium/campaign/content only when absent (does not overwrite existing).
 * Do not use for social doors (threads / instagram / facebook use buildSocialGoUrl).
 */
export function buildYouTubeDescriptionGoUrl(args: {
  productSlug: string;
  videoSlug?: string | null;
}): string {
  const base = buildOrbitRedirectUrl(args.productSlug);
  let url: URL;
  try {
    url = new URL(base);
  } catch {
    return base;
  }
  url.searchParams.set("utm_source", "youtube");
  if (!url.searchParams.has("utm_medium")) {
    url.searchParams.set("utm_medium", "affiliate");
  }
  if (!url.searchParams.has("utm_campaign") && args.videoSlug?.trim()) {
    url.searchParams.set("utm_campaign", args.videoSlug.trim());
  }
  if (!url.searchParams.has("utm_content")) {
    url.searchParams.set("utm_content", args.productSlug);
  }
  return url.toString();
}
