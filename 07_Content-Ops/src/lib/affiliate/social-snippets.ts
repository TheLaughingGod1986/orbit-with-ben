/**
 * Deterministic affiliate-aware social snippets for live Orbit channels:
 * Threads, Instagram (Reels + feed), Facebook Page.
 *
 * Copy patterns from Social Media Manager (see social-snippet-templates.ts).
 * Never emits raw merchant URLs. Approval required before publish.
 */

import { PLATFORMS, type PlatformId } from "@/config/platforms";
import {
  AFFILIATE_LIVE_SOCIAL_PLATFORMS,
  socialPlatformToClickSource,
  type AffiliateLiveSocialPlatform,
} from "./social-channels";
import {
  buildSocialGoUrl,
  buildSocialYouTubeUrl,
} from "./urls";
import {
  containsBannedAffiliatePhrase,
  containsRawMerchantUrl,
  shouldIncludeAffiliateSoftMention,
} from "./social-copy-rules";
import { assertAffiliateSafeSocialCopy } from "./social-copy";
import {
  countCaptionLines,
  firstNonEmptyLine,
  lastNonEmptyLine,
  renderFacebookPageTemplate,
  renderInstagramFeedTemplate,
  renderInstagramReelsTemplate,
  renderThreadsTemplate,
  SOCIAL_SOFT_LINES,
  type SocialSnippetPostStyle,
  FIXTURE_JWST_LIVE,
} from "./social-snippet-templates";
import {
  facebookPageCaptionViolations,
  assertFacebookPageCaptionSafe,
} from "./facebook-page-rules";

export type AffiliateSocialSnippetInput = {
  videoSlug: string;
  videoTitle: string;
  topic: string;
  /** Line 1 wonder — never a product. Defaults to hook or topic. */
  hook?: string | null;
  /** Optional middle body (Facebook / IG feed Thursday-film pattern). */
  body?: string | null;
  youtubeUrl?: string | null;
  productLabel: string;
  productSlug: string;
  hasNaturalObject: boolean;
  productRelevantToVideo: boolean;
  hasApprovedPlacement: boolean;
  /** Platforms already used this week for soft mentions. */
  platformsMentionedThisWeek?: PlatformId[];
  /**
   * Prefer pointing at YouTube (“under the film”) vs embedding /go/.
   * Default true when a film URL exists.
   */
  preferYouTubePointer?: boolean;
  /** Thursday film vs how-to / telescope tone. Default thursday_film. */
  postStyle?: SocialSnippetPostStyle;
  /** When false, how-to posts use /go/ as the only door (no “Watch the film first”). */
  hasFilmThisWeek?: boolean;
  /**
   * Recent /go/ product slugs posted on Facebook Page (last ~3 days).
   * Same slug three days in a row with no new film → soft mention omitted.
   */
  recentFacebookGoSlugs?: string[];
};

export type AffiliateSocialSnippet = {
  platform: AffiliateLiveSocialPlatform;
  label: string;
  caption: string;
  /** Tracked URL embedded in the caption, if any (YouTube or /go/ only). */
  trackedUrl: string | null;
  clickSource: ReturnType<typeof socialPlatformToClickSource>;
  includeAffiliateMention: boolean;
  skipReason?: string;
  /** Must stay false until editor approves — never auto-post. */
  approvedForPublish: false;
  notes: string[];
  /** Template style used (Facebook / IG feed). */
  postStyle?: SocialSnippetPostStyle;
};

function isJwstLivePack(input: AffiliateSocialSnippetInput): boolean {
  return (
    input.postStyle !== "how_to" &&
    (/jwst|james webb|cosmic dawn|jades/i.test(
      `${input.topic} ${input.videoTitle} ${input.hook || ""}`,
    ) ||
      input.productSlug === FIXTURE_JWST_LIVE.softMentionGoSlugWhenReady ||
      input.productSlug === FIXTURE_JWST_LIVE.softMentionProductSlug)
  );
}

/** Resolve JWST soft-mention product for /go + UTMs — never observing guidebook or telescope. */
function jwstEffectiveProduct(input: AffiliateSocialSnippetInput): {
  productSlug: string;
  productLabel: string;
  preferYouTubePointer: boolean;
  notes: string[];
} {
  const forbidden = (
    FIXTURE_JWST_LIVE.forbidProductSlugs as readonly string[]
  ).includes(input.productSlug);
  const readySlug = FIXTURE_JWST_LIVE.softMentionProductSlug;
  const notes: string[] = [];

  if (forbidden) {
    notes.push(
      `JWST live pack rejects ${input.productSlug} (never telescope / Turn Left at Orion / LEGO).`,
    );
  }

  if (readySlug) {
    return {
      productSlug: readySlug,
      productLabel:
        FIXTURE_JWST_LIVE.softMentionProductLabel ||
        FIXTURE_JWST_LIVE.softMentionGoSlugWhenReady,
      preferYouTubePointer: input.preferYouTubePointer !== false,
      notes,
    };
  }

  // TODO: jwst-book product not seeded yet — soft mention stays in copy; door is YouTube only
  notes.push(
    `TODO: JWST soft-mention /go/ slug is ${FIXTURE_JWST_LIVE.softMentionGoSlugWhenReady} — product unset until seeded; door is YouTube under the film.`,
  );
  return {
    productSlug: FIXTURE_JWST_LIVE.softMentionGoSlugWhenReady,
    productLabel: FIXTURE_JWST_LIVE.softMentionGoSlugWhenReady,
    preferYouTubePointer: true,
    notes,
  };
}

function truncate(s: string, max: number): string {
  if (s.length <= max) return s;
  return s.slice(0, max - 1).trimEnd() + "…";
}

function wonderLine(input: AffiliateSocialSnippetInput): string {
  return (
    input.hook?.trim() ||
    `A calm look at ${input.topic} — from our film “${input.videoTitle}”.`
  );
}

function bodyLine(input: AffiliateSocialSnippetInput): string {
  return (
    input.body?.trim() ||
    SOCIAL_SOFT_LINES.bodyFallback(input.topic, input.videoTitle)
  );
}

function resolveDoor(args: {
  input: AffiliateSocialSnippetInput;
  platform: AffiliateLiveSocialPlatform;
  includeAffiliateMention: boolean;
}): { url: string; doorIsGo: boolean; hasFilm: boolean } {
  const preferYt = args.input.preferYouTubePointer !== false;
  const hasFilm =
    args.input.hasFilmThisWeek !== false && Boolean(args.input.youtubeUrl);

  if (preferYt && hasFilm && args.input.youtubeUrl) {
    return {
      url: buildSocialYouTubeUrl({
        youtubeUrl: args.input.youtubeUrl,
        platform: args.platform,
        videoSlug: args.input.videoSlug,
        productSlug: args.includeAffiliateMention
          ? args.input.productSlug
          : null,
        hasAffiliateMention: args.includeAffiliateMention,
      }),
      doorIsGo: false,
      hasFilm: true,
    };
  }

  return {
    url: buildSocialGoUrl({
      productSlug: args.input.productSlug,
      platform: args.platform,
      videoSlug: args.input.videoSlug,
      hasAffiliateMention: args.includeAffiliateMention,
    }),
    doorIsGo: true,
    hasFilm: false,
  };
}

/**
 * Generate copy-ready snippets for Threads, Instagram Reels, Instagram Feed, Facebook Page.
 * Distinct from facebook_reels. Uses Social Media Manager templates.
 */
export function generateAffiliateSocialSnippets(
  input: AffiliateSocialSnippetInput,
): AffiliateSocialSnippet[] {
  return AFFILIATE_LIVE_SOCIAL_PLATFORMS.map((platform) =>
    buildSnippetForPlatform(platform, input),
  );
}

function buildSnippetForPlatform(
  platform: AffiliateLiveSocialPlatform,
  input: AffiliateSocialSnippetInput,
): AffiliateSocialSnippet {
  const postStyle: SocialSnippetPostStyle = input.postStyle || "thursday_film";
  const jwstLive = isJwstLivePack(input);
  const gate = shouldIncludeAffiliateSoftMention({
    platform,
    hasNaturalObject: input.hasNaturalObject,
    canNameSpecificFilm: Boolean(input.youtubeUrl || input.videoTitle),
    platformMentionedThisWeek: input.platformsMentionedThisWeek?.includes(platform),
    productRelevantToVideo: input.productRelevantToVideo,
    hasApprovedPlacement: input.hasApprovedPlacement,
  });

  const clickSource = socialPlatformToClickSource(platform);
  const notes: string[] = [
    "Affiliate social: max one soft mention; never raw merchant URLs.",
    "Requires the same approval flow as description placements before publish.",
    "Templates: Social Media Manager (Facebook Page / Threads / Instagram).",
  ];

  let includeAffiliateMention = gate.include;
  let skipReason = gate.include ? undefined : gate.reason;

  // Same /go/ three days in a row with no new film — omit soft mention on Facebook Page
  if (
    includeAffiliateMention &&
    platform === "facebook_page" &&
    input.hasFilmThisWeek === false &&
    (input.recentFacebookGoSlugs || []).filter((s) => s === input.productSlug)
      .length >= 2
  ) {
    includeAffiliateMention = false;
    skipReason = "platform_already_mentioned_this_week";
    notes.push(
      "Skipped soft mention: same /go/ posted repeatedly with no new film.",
    );
  } else if (!gate.include) {
    notes.push(`Affiliate soft mention skipped (${gate.reason}).`);
  }

  // JWST pictures-from-space: explainer soft mention — never observing guidebook / telescope
  let effectiveInput = input;
  if (jwstLive) {
    const jwstProduct = jwstEffectiveProduct(input);
    notes.push(...jwstProduct.notes);
    effectiveInput = {
      ...input,
      productSlug: jwstProduct.productSlug,
      productLabel: jwstProduct.productLabel,
      preferYouTubePointer: jwstProduct.preferYouTubePointer,
    };
  }

  const door = resolveDoor({
    input: effectiveInput,
    platform,
    includeAffiliateMention,
  });

  // Never emit forbidden /go/ slugs on JWST captions
  if (
    jwstLive &&
    door.doorIsGo &&
    (FIXTURE_JWST_LIVE.forbidProductSlugs as readonly string[]).some((s) =>
      door.url.includes(`/go/${s}`),
    )
  ) {
    includeAffiliateMention = false;
    skipReason = "video_not_about_product";
    notes.push("Blocked forbidden JWST /go/ slug — fell back without merchant door.");
  }

  const wonder = wonderLine(input);
  let caption = "";

  if (jwstLive) {
    notes.push(
      "JWST live pack: soft mention = “the one explainer I used under the film” (never telescope / Turn Left at Orion / LEGO).",
      FIXTURE_JWST_LIVE.softMentionProductSlug
        ? `Book slug: ${FIXTURE_JWST_LIVE.softMentionProductSlug}.`
        : `Book slug TODO: ${FIXTURE_JWST_LIVE.softMentionGoSlugWhenReady} (unset until product exists).`,
      "Never auto-post — approvedForPublish stays false until editor approves.",
    );
    if (platform === "threads") {
      notes.push(
        `Threads: hold until ${FIXTURE_JWST_LIVE.threadsEarliestPublishLabel}.`,
      );
    }
  }

  switch (platform) {
    case "facebook_page":
      caption = renderFacebookPageTemplate({
        style: postStyle,
        wonder: jwstLive ? FIXTURE_JWST_LIVE.wonder : wonder,
        body: jwstLive
          ? FIXTURE_JWST_LIVE.bodyFacebook
          : postStyle === "thursday_film"
            ? bodyLine(input)
            : null,
        doorUrl: door.url,
        hasFilmThisWeek: door.hasFilm,
        includeSoftMention: includeAffiliateMention,
      });
      notes.push(platformNotes(platform));
      break;
    case "instagram_feed":
      caption = renderInstagramFeedTemplate({
        style: postStyle,
        wonder: jwstLive ? FIXTURE_JWST_LIVE.wonder : wonder,
        body: jwstLive
          ? FIXTURE_JWST_LIVE.bodyFacebook
          : postStyle === "thursday_film"
            ? bodyLine(input)
            : null,
        doorUrl: door.url,
        hasFilmThisWeek: door.hasFilm,
        includeSoftMention: includeAffiliateMention,
        jwstLive: jwstLive && includeAffiliateMention,
      });
      notes.push(platformNotes(platform));
      break;
    case "instagram_reels":
      caption = renderInstagramReelsTemplate({
        wonder: jwstLive ? FIXTURE_JWST_LIVE.wonder : wonder,
        doorUrl: door.url,
        includeSoftMention: includeAffiliateMention,
        doorIsGo: door.doorIsGo,
      });
      notes.push(platformNotes(platform));
      break;
    case "threads":
      caption = renderThreadsTemplate({
        wonder: jwstLive ? FIXTURE_JWST_LIVE.wonder : wonder,
        body: jwstLive ? FIXTURE_JWST_LIVE.bodyThreads : null,
        doorUrl: door.url,
        includeSoftMention: includeAffiliateMention,
        doorIsGo: door.doorIsGo,
        jwstLive: jwstLive && includeAffiliateMention,
      });
      notes.push(platformNotes(platform));
      break;
    default:
      caption = `${wonder}\n\n${door.url}`;
  }

  const max = PLATFORMS[platform].maxCaptionLength || 2200;
  caption = truncate(caption, max);

  // Hard structural checks
  const first = firstNonEmptyLine(caption);
  if (first.includes("/go/") || /go\/[a-z0-9-]+/i.test(first)) {
    // Never put /go/ on line 1 (Shorts/Reels/any)
    caption = truncate(`${wonder}\n\n${door.url}`, max);
    includeAffiliateMention = false;
    notes.push("Stripped /go/ from line 1 — wonder must come first.");
  }

  try {
    assertAffiliateSafeSocialCopy(caption);
  } catch {
    caption = truncate(wonder, max);
    includeAffiliateMention = false;
    notes.push("Stripped unsafe copy — fell back to wonder-only.");
  }

  if (containsRawMerchantUrl(caption) || containsBannedAffiliatePhrase(caption)) {
    caption = truncate(wonder, max);
    includeAffiliateMention = false;
    notes.push("Stripped unsafe URL/language — fell back to science-only caption.");
  }

  if (platform === "facebook_page") {
    const violations = facebookPageCaptionViolations(caption, {
      brandNames: [input.productLabel, "Amazon", "Brilliant", "LEGO"],
      productSlug: input.productSlug,
      recentGoSlugs: input.recentFacebookGoSlugs,
      hasFilmThisWeek: input.hasFilmThisWeek !== false && Boolean(input.youtubeUrl),
    });
    if (violations.length) {
      try {
        assertFacebookPageCaptionSafe(caption, {
          brandNames: [input.productLabel],
        });
      } catch {
        // Fail closed to wonder + door only (no soft mention, no shop energy)
        caption = renderFacebookPageTemplate({
          style: "thursday_film",
          wonder,
          body: bodyLine(input),
          doorUrl: door.url,
          hasFilmThisWeek: door.hasFilm,
          includeSoftMention: false,
        });
        includeAffiliateMention = false;
        notes.push(
          `Facebook Page house reject: ${violations.join(", ")} — soft mention removed.`,
        );
      }
    }
  }

  // Final: link must be youtube or /go/ only
  if (containsRawMerchantUrl(caption)) {
    caption = truncate(wonder, max);
    notes.push("Merchant URL rejected — wonder only.");
  }

  return {
    platform,
    label: PLATFORMS[platform].label,
    caption,
    trackedUrl: door.url,
    clickSource,
    includeAffiliateMention,
    skipReason: includeAffiliateMention ? undefined : skipReason,
    approvedForPublish: false,
    notes,
    postStyle:
      platform === "facebook_page" || platform === "instagram_feed"
        ? postStyle
        : undefined,
  };
}

function platformNotes(platform: AffiliateLiveSocialPlatform): string {
  switch (platform) {
    case "threads":
      return "Threads: thought first, one extra line, one link (YouTube or /go/). No product thread.";
    case "instagram_reels":
      return "IG Reels: mention in caption only; sticker/bio → YouTube or /go/; never /go/ on line 1.";
    case "instagram_feed":
      return "IG Feed: same caption pattern as Facebook Page; one /go/ or YouTube door.";
    case "facebook_page":
      return "Facebook Page: 3–5 short lines; wonder first; last line = film or /go/; no shop now.";
    default:
      return "";
  }
}

/** Platforms required by Ben’s live-channel brief (for UI). */
export function affiliateLiveSocialPlatformIds(): AffiliateLiveSocialPlatform[] {
  return [...AFFILIATE_LIVE_SOCIAL_PLATFORMS];
}

export {
  countCaptionLines,
  firstNonEmptyLine,
  lastNonEmptyLine,
  FIXTURE_JWST_LIVE,
  FIXTURE_TELESCOPE_OBSERVING_HELD,
  FIXTURE_FACEBOOK_PAGE_THURSDAY_FILM,
  FIXTURE_FACEBOOK_PAGE_HOWTO,
  FIXTURE_COMMENT_REPLY_TELESCOPE,
  renderJwstLiveCaption,
  renderTelescopeObservingHeldCaption,
  isJwstThreadsPublishAllowed,
  renderFacebookPageTemplate,
  renderThreadsTemplate,
  renderInstagramReelsTemplate,
  renderTelescopeCommentReply,
} from "./social-snippet-templates";
