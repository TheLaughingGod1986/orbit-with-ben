/**
 * Facebook Page feed (not Reels) — hard rejects from Social Media Manager.
 * Generator + tests must fail closed on these.
 */

import {
  FACEBOOK_PAGE_NEVER_PHRASES,
  firstNonEmptyLine,
  lastNonEmptyLine,
} from "./social-snippet-templates";
import {
  containsBannedAffiliatePhrase,
  containsRawMerchantUrl,
  isAllowedSocialTrackedUrl,
  opensOnProductOrBrand,
} from "./social-copy-rules";

export type FacebookPageValidationOptions = {
  brandNames?: string[];
  productSlug?: string;
  /** /go/ slugs posted on the Page in the last ~3 days */
  recentGoSlugs?: string[];
  hasFilmThisWeek?: boolean;
};

export type FacebookPageViolation =
  | "raw_merchant_url"
  | "banned_shop_phrase"
  | "opens_on_product"
  | "soft_mention_on_line_1"
  | "door_not_youtube_or_go"
  | "more_than_one_brand"
  | "link_in_comments_spam"
  | "pin_affiliate_comment"
  | "same_go_three_days_no_film"
  | "boost_or_catalog_language";

/**
 * Return violation codes for a Facebook Page feed caption.
 * Empty array = safe to keep (still requires editor approval before publish).
 */
export function facebookPageCaptionViolations(
  caption: string,
  opts: FacebookPageValidationOptions = {},
): FacebookPageViolation[] {
  const violations: FacebookPageViolation[] = [];
  const lower = caption.toLowerCase();

  if (containsRawMerchantUrl(caption)) {
    violations.push("raw_merchant_url");
  }

  if (
    containsBannedAffiliatePhrase(caption) ||
    FACEBOOK_PAGE_NEVER_PHRASES.some((p) => lower.includes(p))
  ) {
    if (
      /boost|catalog|carousel|store tab|product tag|shop now|buy now/.test(lower)
    ) {
      violations.push("boost_or_catalog_language");
    } else {
      violations.push("banned_shop_phrase");
    }
  }

  if (opensOnProductOrBrand(caption, opts.brandNames || [])) {
    violations.push("opens_on_product");
  }

  const first = firstNonEmptyLine(caption);
  if (
    /under the film|the one I use|explainer I used|small cut if you grab/i.test(
      first,
    )
  ) {
    violations.push("soft_mention_on_line_1");
  }

  const last = lastNonEmptyLine(caption);
  if (last && /^https?:\/\//i.test(last) && !isAllowedSocialTrackedUrl(last)) {
    violations.push("door_not_youtube_or_go");
  }
  // Any absolute URL in the post must be allowed
  const urls = caption.match(/https?:\/\/[^\s)]+/gi) || [];
  for (const u of urls) {
    if (!isAllowedSocialTrackedUrl(u)) {
      if (!violations.includes("raw_merchant_url")) {
        violations.push("raw_merchant_url");
      }
      if (!violations.includes("door_not_youtube_or_go")) {
        violations.push("door_not_youtube_or_go");
      }
    }
  }

  const brands = (opts.brandNames || []).filter(Boolean);
  if (brands.length >= 2) {
    const hit = brands.filter((b) => lower.includes(b.toLowerCase()));
    if (hit.length >= 2) {
      violations.push("more_than_one_brand");
    }
  }

  if (/link(s)? in comments/i.test(caption)) {
    violations.push("link_in_comments_spam");
  }

  if (/pin(ned)? (this )?affiliate|pin(ned)? comment.*(amazon|affiliate|buy)/i.test(caption)) {
    violations.push("pin_affiliate_comment");
  }

  if (
    opts.productSlug &&
    opts.hasFilmThisWeek === false &&
    (opts.recentGoSlugs || []).filter((s) => s === opts.productSlug).length >= 2
  ) {
    violations.push("same_go_three_days_no_film");
  }

  return [...new Set(violations)];
}

export function assertFacebookPageCaptionSafe(
  caption: string,
  opts: FacebookPageValidationOptions = {},
): void {
  const v = facebookPageCaptionViolations(caption, opts);
  if (v.length) {
    throw new Error(
      `Facebook Page caption violates Social Media Manager rules: ${v.join(", ")}`,
    );
  }
}
