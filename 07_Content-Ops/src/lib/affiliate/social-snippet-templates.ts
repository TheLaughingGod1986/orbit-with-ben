/**
 * Social Media Manager copy patterns — fixtures + deterministic templates
 * for affiliate-aware live-channel snippets (Threads, Instagram, Facebook Page).
 *
 * House rules still apply: max one soft mention, never open on a product,
 * tracked URLs = youtube.com / youtu.be / Orbit /go/ only.
 * Never auto-post — fixtures ship with approvedForPublish: false.
 */

export type SocialSnippetPostStyle = "thursday_film" | "how_to";

export type SocialSnippetTemplateVars = {
  /** Line 1 — the wonder. Never a product. */
  wonder: string;
  /** Optional middle line(s) — what Orbit shows / context. */
  body?: string | null;
  /** YouTube film URL or Orbit /go/{slug} — the only door. */
  doorUrl: string;
  /** Soft product label for how-to tone (never line 1). */
  productLabel?: string | null;
};

/** Door placeholder used in fixture captions before a real YouTube URL is known. */
export const FIXTURE_DOOR_PLACEHOLDER_JWST = "[JWST YouTube URL]" as const;
export const FIXTURE_DOOR_PLACEHOLDER_FILM = "[YouTube film URL]" as const;
export const FIXTURE_DOOR_PLACEHOLDER_TELESCOPE_GO =
  "https://orbitwithben.com/go/beginner-telescope" as const;

/**
 * First live captions — JWST Thursday film (pictures from space).
 * Soft mention copy: “the one explainer I used under the film.”
 *
 * /go/ slug for that mention MUST be `jwst-book` once that product exists
 * (verified Amazon UK JWST / cosmic-dawn books — other agent). Until then
 * `softMentionProductSlug` stays unset — do NOT use beginner-astronomy-book
 * (Turn Left at Orion is an observing guidebook; fails trust gate on JWST wonder films)
 * or beginner-telescope.
 *
 * LEGO stays out. Never raw Amazon URLs. Never auto-post.
 * Threads: hold until Thu 20 Aug 2026 18:00 Europe/London.
 */
export const FIXTURE_JWST_LIVE = {
  filmTopic: "JWST",
  filmLabel: "JWST Thursday film (pictures from space)",
  /**
   * Unset until `jwst-book` product exists. Soft mention stays in caption copy;
   * door is YouTube (“under the film”) until this is set.
   */
  softMentionProductSlug: null as string | null,
  softMentionProductLabel: null as string | null,
  /** Intended /go/{slug} once the JWST explainer book product is seeded. */
  softMentionGoSlugWhenReady: "jwst-book" as const,
  /** Explicit bans for this film’s social pack (trust gate + wrong product). */
  forbidProductSlugs: [
    "beginner-telescope",
    "beginner-astronomy-book",
    "space-lego",
  ] as const,
  forbidProductLabels: ["Turn Left at Orion"] as const,
  forbidFamilies: ["telescope", "lego"] as const,
  autoPost: false as const,
  approvedForPublish: false as const,
  /**
   * Earliest Threads publish (Europe/London). 18:00 BST = 17:00 UTC.
   * Instagram / Facebook Page: same Thursday night after the film is up.
   */
  threadsEarliestPublishAtIso: "2026-08-20T17:00:00.000Z",
  threadsEarliestPublishLabel: "Thu 20 Aug 2026 18:00 Europe/London",

  wonder: "JWST keeps finding galaxies that should not be there yet.",
  bodyFacebook:
    "Orbit walks through what the pictures actually show, and what they do not.",
  bodyThreads: "Orbit walks through what the pictures actually show.",

  softLineThreads: "Film is up. I left the one explainer I used under it.",
  softLineInstagram:
    "Full film on YouTube. I left the one explainer I used under it.",
  softLineFacebook:
    "Film is up. If you want the one explainer I used, it is under the film.",

  threadsCaptionWithoutUrl: [
    "JWST keeps finding galaxies that should not be there yet.",
    "",
    "Orbit walks through what the pictures actually show.",
    "",
    "Film is up. I left the one explainer I used under it.",
  ].join("\n"),

  instagramCaptionWithoutUrl: [
    "JWST keeps finding galaxies that should not be there yet. Orbit walks through what the pictures actually show, and what they do not.",
    "",
    "Full film on YouTube. I left the one explainer I used under it.",
  ].join("\n"),

  facebookCaptionWithoutUrl: [
    "JWST keeps finding galaxies that should not be there yet.",
    "",
    "Orbit walks through what the pictures actually show, and what they do not.",
    "",
    "Film is up. If you want the one explainer I used, it is under the film.",
  ].join("\n"),
} as const;

/**
 * Telescope / observing how-to caption — HELD until a real observing post.
 * Not for Thursday JWST. Soft door = film URL or /go/beginner-telescope.
 * Never raw Amazon. Never LEGO. Never more than one brand.
 */
export const FIXTURE_TELESCOPE_OBSERVING_HELD = {
  status: "held" as const,
  holdReason:
    "Hold until a real observing / how-to post — not the Thursday JWST pictures-from-space film.",
  postStyle: "how_to" as const,
  productSlug: "beginner-telescope",
  productLabel: "Celestron FirstScope",
  autoPost: false as const,
  approvedForPublish: false as const,
  wonder: "I spent a night on this patch of sky. This is what it looked like.",
  softLineWithFilm:
    "If you want that kind of view, I left the one I use under the film. I get a small cut if you grab it.",
  softLineWithoutFilm:
    "If you want that kind of view, I left the one I use here. I get a small cut if you grab it.",
  ctaWithFilm: "Watch the film first.",
  captionWithFilmWithoutUrl: [
    "I spent a night on this patch of sky. This is what it looked like.",
    "",
    "If you want that kind of view, I left the one I use under the film. I get a small cut if you grab it.",
    "",
    "Watch the film first.",
  ].join("\n"),
} as const;

/** Facebook Page Thursday-film alias (JWST live). */
export const FIXTURE_FACEBOOK_PAGE_THURSDAY_FILM = {
  wonder: FIXTURE_JWST_LIVE.wonder,
  body: FIXTURE_JWST_LIVE.bodyFacebook,
  softLine: FIXTURE_JWST_LIVE.softLineFacebook,
  doorPlaceholder: FIXTURE_DOOR_PLACEHOLDER_FILM,
  captionWithoutUrl: FIXTURE_JWST_LIVE.facebookCaptionWithoutUrl,
} as const;

/** How-to Facebook Page alias — telescope observing (held). */
export const FIXTURE_FACEBOOK_PAGE_HOWTO = {
  wonder: FIXTURE_TELESCOPE_OBSERVING_HELD.wonder,
  softLineWithFilm: FIXTURE_TELESCOPE_OBSERVING_HELD.softLineWithFilm,
  softLineWithoutFilm: FIXTURE_TELESCOPE_OBSERVING_HELD.softLineWithoutFilm,
  ctaWithFilm: FIXTURE_TELESCOPE_OBSERVING_HELD.ctaWithFilm,
  doorPlaceholderFilm: FIXTURE_DOOR_PLACEHOLDER_FILM,
  doorPlaceholderGo: "[https://orbit…/go/telescope]",
  captionWithFilmWithoutUrl:
    FIXTURE_TELESCOPE_OBSERVING_HELD.captionWithFilmWithoutUrl,
} as const;

/**
 * Honest comment reply when someone asks “what telescope?” —
 * one reply, film description or /go/, disclose once, stop.
 */
export const FIXTURE_COMMENT_REPLY_TELESCOPE = {
  withFilm:
    "I left the one I use under the film (description). Some links are affiliate.",
  withoutFilm:
    "I left the one I use here: {{doorUrl}} — some links are affiliate.",
} as const;

/** Soft lines used by generators (never line 1). */
export const SOCIAL_SOFT_LINES = {
  thursdayFilmUnderFilm: FIXTURE_JWST_LIVE.softLineFacebook,
  thursdayFilmGoOnly:
    "Film context above. If you want the one explainer I used:",
  howtoUnderFilm: FIXTURE_TELESCOPE_OBSERVING_HELD.softLineWithFilm,
  howtoGoOnly: FIXTURE_TELESCOPE_OBSERVING_HELD.softLineWithoutFilm,
  howtoWatchFirst: FIXTURE_TELESCOPE_OBSERVING_HELD.ctaWithFilm,
  threadsExtraUnderFilm: FIXTURE_JWST_LIVE.softLineThreads,
  threadsExtraGo: "If you want to look at this yourself:",
  reelsCaptionUnderFilm: FIXTURE_JWST_LIVE.softLineInstagram,
  reelsCaptionGo: "If you want to look at this yourself:",
  bodyFallback: (topic: string, title: string) =>
    `Orbit walks through what the pictures actually show for ${topic} — and what they do not. (“${title}”)`,
} as const;

/**
 * Phrases / patterns that must never appear on the Facebook Page feed
 * (reject in generator + tests). Extends general affiliate bans.
 */
export const FACEBOOK_PAGE_NEVER_PHRASES = [
  "shop now",
  "shop today",
  "buy now",
  "add to cart",
  "use my code",
  "use code",
  "promo code",
  "discount code",
  "% off",
  "percent off",
  "haul",
  "unboxing",
  "link in comments",
  "links in comments",
  "link in bio",
  "links in bio",
  "product carousel",
  "boosted catalog",
  "boost this as",
  "store tab",
  "product tag",
  "amazon associate",
  "swipe up to buy",
  "tiktok shop",
] as const;

export type JwstLivePlatform = "threads" | "instagram" | "facebook_page";

/**
 * Render the locked Social Media Manager JWST live caption for a platform.
 * Door must be YouTube or /go/{book-slug} — never a merchant URL.
 * Always draft-only (caller must keep approvedForPublish false).
 */
export function renderJwstLiveCaption(args: {
  platform: JwstLivePlatform;
  doorUrl: string;
}): string {
  const door = args.doorUrl.trim() || FIXTURE_DOOR_PLACEHOLDER_JWST;
  switch (args.platform) {
    case "threads":
      return `${FIXTURE_JWST_LIVE.threadsCaptionWithoutUrl}\n${door}`;
    case "instagram":
      return `${FIXTURE_JWST_LIVE.instagramCaptionWithoutUrl}\n${door}`;
    case "facebook_page":
      return `${FIXTURE_JWST_LIVE.facebookCaptionWithoutUrl}\n${door}`;
    default:
      return `${FIXTURE_JWST_LIVE.facebookCaptionWithoutUrl}\n${door}`;
  }
}

/** True when Threads may publish the JWST live pack (after scheduled London time). */
export function isJwstThreadsPublishAllowed(now: Date = new Date()): boolean {
  return now.getTime() >= Date.parse(FIXTURE_JWST_LIVE.threadsEarliestPublishAtIso);
}

/**
 * Render held telescope observing caption (draft only — do not auto-post).
 * Prefer film URL; /go/beginner-telescope when no film that week.
 */
export function renderTelescopeObservingHeldCaption(args: {
  doorUrl: string;
  hasFilm: boolean;
}): { caption: string; status: "held"; approvedForPublish: false } {
  const door = args.doorUrl.trim();
  if (args.hasFilm) {
    return {
      caption: `${FIXTURE_TELESCOPE_OBSERVING_HELD.captionWithFilmWithoutUrl}\n${door}`,
      status: "held",
      approvedForPublish: false,
    };
  }
  return {
    caption: [
      FIXTURE_TELESCOPE_OBSERVING_HELD.wonder,
      "",
      FIXTURE_TELESCOPE_OBSERVING_HELD.softLineWithoutFilm,
      door,
    ].join("\n"),
    status: "held",
    approvedForPublish: false,
  };
}

/**
 * Render Facebook Page feed caption (3–5 short lines).
 * First line = wonder. Soft mention never in line 1. Last line = door URL.
 */
export function renderFacebookPageTemplate(args: {
  style: SocialSnippetPostStyle;
  wonder: string;
  body?: string | null;
  doorUrl: string;
  /** When false and how-to: door is /go/ only (no “Watch the film first”). */
  hasFilmThisWeek: boolean;
  includeSoftMention: boolean;
}): string {
  const wonder = args.wonder.trim();
  const body = args.body?.trim() || null;
  const door = args.doorUrl.trim();
  const lines: string[] = [wonder];

  if (args.style === "thursday_film") {
    if (body) {
      lines.push("", body);
    }
    if (args.includeSoftMention) {
      lines.push(
        "",
        args.hasFilmThisWeek
          ? SOCIAL_SOFT_LINES.thursdayFilmUnderFilm
          : SOCIAL_SOFT_LINES.thursdayFilmGoOnly,
      );
    } else if (args.hasFilmThisWeek) {
      lines.push("", "Film is up.");
    }
    lines.push(door);
  } else {
    // how_to
    if (args.includeSoftMention) {
      lines.push(
        "",
        args.hasFilmThisWeek
          ? SOCIAL_SOFT_LINES.howtoUnderFilm
          : SOCIAL_SOFT_LINES.howtoGoOnly,
      );
      if (args.hasFilmThisWeek) {
        lines.push("", SOCIAL_SOFT_LINES.howtoWatchFirst);
      }
    } else if (args.hasFilmThisWeek) {
      lines.push("", SOCIAL_SOFT_LINES.howtoWatchFirst);
    }
    lines.push(door);
  }

  return lines.join("\n").trim();
}

/**
 * Instagram feed — JWST live shape differs from Facebook (wonder+body one para).
 * Generic thursday_film still uses Facebook shape unless `jwstLive` is true.
 */
export function renderInstagramFeedTemplate(args: {
  style: SocialSnippetPostStyle;
  wonder: string;
  body?: string | null;
  doorUrl: string;
  hasFilmThisWeek: boolean;
  includeSoftMention: boolean;
  /** Use Social Media Manager JWST Instagram live fixture shape. */
  jwstLive?: boolean;
}): string {
  if (args.jwstLive && args.style === "thursday_film") {
    return renderJwstLiveCaption({
      platform: "instagram",
      doorUrl: args.doorUrl,
    });
  }
  return renderFacebookPageTemplate(args);
}

/**
 * Threads: thought first, optional body, soft line, one link (YouTube or /go/).
 * Never a product thread. Soft mention never line 1. /go/ never line 1.
 */
export function renderThreadsTemplate(args: {
  wonder: string;
  doorUrl: string;
  includeSoftMention: boolean;
  doorIsGo: boolean;
  /** Optional middle line (JWST live uses body). */
  body?: string | null;
  /** Use Social Media Manager JWST Threads live fixture shape. */
  jwstLive?: boolean;
}): string {
  if (args.jwstLive) {
    return renderJwstLiveCaption({
      platform: "threads",
      doorUrl: args.doorUrl,
    });
  }
  const wonder = args.wonder.trim();
  const door = args.doorUrl.trim();
  const body = args.body?.trim() || null;
  if (!args.includeSoftMention) {
    return body ? `${wonder}\n\n${body}\n\n${door}` : `${wonder}\n\n${door}`;
  }
  if (args.doorIsGo) {
    return body
      ? `${wonder}\n\n${body}\n\n${SOCIAL_SOFT_LINES.threadsExtraGo}\n${door}`
      : `${wonder}\n\n${SOCIAL_SOFT_LINES.threadsExtraGo}\n${door}`;
  }
  return body
    ? `${wonder}\n\n${body}\n\n${SOCIAL_SOFT_LINES.threadsExtraUnderFilm}\n${door}`
    : `${wonder}\n\n${SOCIAL_SOFT_LINES.threadsExtraUnderFilm}\n${door}`;
}

/**
 * IG Reels: science thought + soft mention in caption only.
 * Door URL at end (YouTube or /go/). Never /go/ on line 1.
 */
export function renderInstagramReelsTemplate(args: {
  wonder: string;
  doorUrl: string;
  includeSoftMention: boolean;
  doorIsGo: boolean;
}): string {
  const wonder = args.wonder.trim();
  const door = args.doorUrl.trim();
  if (!args.includeSoftMention) {
    return `${wonder}\n\nFull film:\n${door}`;
  }
  if (args.doorIsGo) {
    return `${wonder}\n\n${SOCIAL_SOFT_LINES.reelsCaptionGo}\n${door}`;
  }
  return `${wonder}\n\n${SOCIAL_SOFT_LINES.reelsCaptionUnderFilm}\n${door}`;
}

/** Build comment-reply fixture text (disclose once, stop). */
export function renderTelescopeCommentReply(args: {
  doorUrl?: string | null;
  hasFilm: boolean;
}): string {
  if (args.hasFilm) return FIXTURE_COMMENT_REPLY_TELESCOPE.withFilm;
  const url =
    args.doorUrl?.trim() || FIXTURE_DOOR_PLACEHOLDER_TELESCOPE_GO;
  return FIXTURE_COMMENT_REPLY_TELESCOPE.withoutFilm.replace("{{doorUrl}}", url);
}

/**
 * Count non-empty lines (Facebook Page target: 3–5 short lines + door).
 * Door URL counts as the last line.
 */
export function countCaptionLines(caption: string): number {
  return caption
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean).length;
}

export function firstNonEmptyLine(caption: string): string {
  return (
    caption
      .split("\n")
      .map((l) => l.trim())
      .find((l) => l.length > 0) || ""
  );
}

export function lastNonEmptyLine(caption: string): string {
  const lines = caption
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean);
  return lines[lines.length - 1] || "";
}
