/**
 * Video Auditor editorial trust gate.
 *
 * Matching may still surface up to 4 candidates on the Affiliate card for editors.
 * Auto-insert, description generation, and APPROVED placements must pass this gate.
 * Relevance and trust beat “max 4 links in the description.”
 *
 * Hard rule: would we still name this product if there were no commission?
 */

import type { ProductMatchInput, VideoMatchInput } from "./types";
import { isWiredTopicBookForVideo } from "./film-topic-book-map";

/** Candidates visible on the video Affiliate Monetisation card (editor options). */
export const MAX_AFFILIATE_CARD_CANDIDATES = 4;

/** Hard cap for links that may enter a long-form YouTube description. */
export const MAX_AFFILIATE_DESCRIPTION_LINKS = 2;

/** At most one primary affiliate link per long-form film. */
export const MAX_AFFILIATE_DESCRIPTION_PRIMARY = 1;

/**
 * Quiet disclosure — last line of the affiliate block (Creator voice).
 * Do not place the affiliate block in the first screen of the description.
 */
export const EDITORIAL_TRUST_DISCLOSURE =
  "Some of these links are affiliate links. We only share things we’d still point you to with no commission.";

export const VIDEO_AFFILIATE_TYPES = [
  "SHORT",
  "COMPANION_SHORT",
  "WONDER",
  "EXPLAINER",
  "HOW_TO",
  "UNKNOWN_LONGFORM",
] as const;
export type VideoAffiliateType = (typeof VIDEO_AFFILIATE_TYPES)[number];

export type TrustGateFailureCode =
  | "NO_COMMISSION_FAIL"
  | "SHORTS_ZERO_AFFILIATE"
  | "NOT_NAMED_IN_VIDEO"
  | "DOES_NOT_HELP_VIEWER"
  | "WONDER_REQUIRES_NAMED_BOOK_OR_PAPER"
  | "EXPLAINER_LIMIT"
  | "HOW_TO_REQUIRES_SHOWN_TOOL"
  | "TOO_MANY_LINKS"
  | "STACK_NOT_COMPANION"
  | "HIGH_COMMISSION_JUNK"
  | "UNIVERSAL_SPAM_LINK"
  | "SALESY_TONE"
  | "COMPETES_WITH_CTA"
  | "INACTIVE_PRODUCT"
  | "REJECTED";

export type TrustGateResult = {
  pass: boolean;
  failures: TrustGateFailureCode[];
  reasons: string[];
  videoType: VideoAffiliateType;
  /** Would we still name this with no commission? */
  wouldRecommendWithoutCommission: boolean;
  namedInVideo: boolean;
};

export type EditorialTrustProductInput = ProductMatchInput & {
  /**
   * Editor/auditor assertion: product was named on screen or in the VO of THIS video.
   * When omitted, the gate infers from script/summary/title token overlap.
   */
  namedInVideo?: boolean;
  /** Explicit no-commission trust answer from editor. Default: inferred (true unless junk). */
  wouldRecommendWithoutCommission?: boolean;
  /** Product helps the viewer do the thing the film showed (see sky / read paper / understand). */
  helpsViewerDoTheThing?: boolean;
  /** Free or cheap companion (paper, PDF, low-cost book) — only valid second link. */
  isFreeOrCheapCompanion?: boolean;
  /** Shown on screen (required for how-to tools). */
  shownOnScreen?: boolean;
  /** Same link pasted on every video regardless of topic. */
  isUniversalSpamLink?: boolean;
};

export type EditorialTrustVideoInput = VideoMatchInput & {
  /** Force video type when known (e.g. from format metadata). */
  videoAffiliateType?: VideoAffiliateType | null;
  /** True when this is a Short / companion Short (zero affiliate links). */
  isShort?: boolean;
  isCompanionShort?: boolean;
};

const JUNK_CATEGORY_RE =
  /\b(crypto|nft|supplement|protein|vpn|hosting|mystery\s*box|merch\s*drop|space\s*merch|weight\s*loss|forex|betting|casino|mlm)\b/i;

const JUNK_TAG_SLUGS = new Set([
  "crypto",
  "nft",
  "supplements",
  "vpn",
  "hosting",
  "merch",
  "mystery-box",
]);

const SALESY_RE =
  /\b(buy\s*now|must[- ]?have|limited\s*time|limited\s*offer|limited\b|50%\s*off|\d+%\s*off|shop\s*now|act\s*now|hurry|flash\s*sale|use\s*my\s*code|promo\s*code|support\s+the\s+channel\s+by\s+(shopping|buying)|countdown|bundle\s+deal|bundle\s+pressure)\b/i;

const WONDER_TITLE_RE =
  /\b(diamond\s+planet|three\s+suns|too[- ]early\s+galax|wonder|beautiful|stunning|impossible\s+world|what\s+if\s+earth)\b/i;

const EXPLAINER_TITLE_RE =
  /\b(jwst|james\s+webb|fermi|black\s+hole|explained|how\s+does|what\s+is|why\s+haven|paradox|relativity|quantum)\b/i;

const HOW_TO_TITLE_RE =
  /\b(how\s+to|tonight|telescope|find\s+jupiter|look\s+through|stargazing\s+guide|beginner.?s?\s+guide\s+to\s+the\s+sky)\b/i;

const BOOK_OR_PAPER_RE =
  /\b(books?|paper|journal|atlas|sky\s*atlas|jades|arxiv|study|essay)\b/i;

const SKY_APP_RE = /\b(app|planetarium|stellarium|sky\s*guide|star\s*walk)\b/i;

const TOOL_RE =
  /\b(telescope|binocular|mount|eyepiece|tripod|camera|adapter)\b/i;

function normalize(s: string): string {
  return s.toLowerCase().replace(/[^a-z0-9\s-]/g, " ").replace(/\s+/g, " ").trim();
}

function videoCorpus(video: EditorialTrustVideoInput): string {
  return [
    video.title,
    video.workingTitle,
    video.topic,
    video.category,
    video.summary,
    video.primaryKeyword,
    video.script,
    ...(video.chapterTitles || []),
    ...(video.tags || []),
  ]
    .filter(Boolean)
    .join("\n");
}

/**
 * Classify film for affiliate policy.
 * Shorts / companion Shorts → zero links.
 */
export function classifyVideoAffiliateType(
  video: EditorialTrustVideoInput,
): VideoAffiliateType {
  if (video.videoAffiliateType) return video.videoAffiliateType;
  if (video.isCompanionShort) return "COMPANION_SHORT";
  if (video.isShort) return "SHORT";

  const episode = normalize(video.episodeType || "");
  if (/short|shorts|companion/.test(episode)) {
    return /companion/.test(episode) ? "COMPANION_SHORT" : "SHORT";
  }

  const blob = normalize(
    `${video.title} ${video.workingTitle || ""} ${video.topic} ${video.category || ""} ${video.primaryKeyword || ""}`,
  );

  if (HOW_TO_TITLE_RE.test(blob)) return "HOW_TO";
  if (WONDER_TITLE_RE.test(blob)) return "WONDER";
  if (EXPLAINER_TITLE_RE.test(blob)) return "EXPLAINER";

  // Default long-form treated as explainer-adjacent (strict: at most one named item)
  return "UNKNOWN_LONGFORM";
}

export function isHighCommissionJunk(product: EditorialTrustProductInput): boolean {
  const hay = `${product.name} ${product.category} ${product.subcategory || ""} ${product.description || ""}`;
  if (JUNK_CATEGORY_RE.test(hay)) return true;
  if (product.tagSlugs.some((t) => JUNK_TAG_SLUGS.has(t.toLowerCase()))) return true;
  return false;
}

/**
 * Infer whether the product is named in THIS video's VO/script/on-screen text.
 * Requires a meaningful name token (≥4 chars) present in the corpus — not vague topic overlap.
 */
export function inferNamedInVideo(
  video: EditorialTrustVideoInput,
  product: EditorialTrustProductInput,
): boolean {
  if (typeof product.namedInVideo === "boolean") return product.namedInVideo;

  // Editorial programme: one desk book wired per long-form film (Social Media Manager).
  if (isWiredTopicBookForVideo(video, product.slug)) return true;

  const corpus = normalize(videoCorpus(video));
  if (!corpus) return false;

  const name = normalize(product.name);
  if (name.length >= 4 && corpus.includes(name)) return true;

  // Significant name tokens (skip generic words)
  const stop = new Set([
    "the",
    "and",
    "for",
    "with",
    "beginner",
    "advanced",
    "starter",
    "kit",
    "set",
    "guide",
  ]);
  const tokens = name.split(" ").filter((t) => t.length >= 4 && !stop.has(t));
  if (tokens.length && tokens.every((t) => corpus.includes(t))) return true;

  // Specific paper / atlas style titles often shortened in VO
  if (BOOK_OR_PAPER_RE.test(product.category) || BOOK_OR_PAPER_RE.test(product.name)) {
    const distinctive = tokens.filter((t) => t.length >= 5);
    if (distinctive.some((t) => corpus.includes(t))) return true;
  }

  return false;
}

export function inferHelpsViewer(
  video: EditorialTrustVideoInput,
  product: EditorialTrustProductInput,
  videoType: VideoAffiliateType,
): boolean {
  if (typeof product.helpsViewerDoTheThing === "boolean") {
    return product.helpsViewerDoTheThing;
  }
  // Default: if named in a how-to / explainer and not junk, assume helpful
  if (isHighCommissionJunk(product)) return false;
  if (videoType === "HOW_TO" && TOOL_RE.test(`${product.name} ${product.category}`)) {
    return true;
  }
  if (
    (videoType === "EXPLAINER" || videoType === "UNKNOWN_LONGFORM" || videoType === "WONDER") &&
    (BOOK_OR_PAPER_RE.test(`${product.name} ${product.category}`) ||
      SKY_APP_RE.test(`${product.name} ${product.category}`))
  ) {
    return true;
  }
  return false;
}

export function inferFreeOrCheapCompanion(product: EditorialTrustProductInput): boolean {
  if (typeof product.isFreeOrCheapCompanion === "boolean") {
    return product.isFreeOrCheapCompanion;
  }
  if (product.price == null) {
    return BOOK_OR_PAPER_RE.test(`${product.name} ${product.category}`);
  }
  return product.price <= 20 && BOOK_OR_PAPER_RE.test(`${product.name} ${product.category}`);
}

export function inferWouldRecommendWithoutCommission(
  product: EditorialTrustProductInput,
): boolean {
  if (typeof product.wouldRecommendWithoutCommission === "boolean") {
    return product.wouldRecommendWithoutCommission;
  }
  // Fail closed on junk; otherwise editorial default is yes only when not spam-shaped
  if (isHighCommissionJunk(product)) return false;
  if (product.isUniversalSpamLink) return false;
  return true;
}

function isBookPaperOrSkyApp(product: EditorialTrustProductInput): boolean {
  const hay = `${product.name} ${product.category} ${product.subcategory || ""}`;
  return BOOK_OR_PAPER_RE.test(hay) || SKY_APP_RE.test(hay);
}

function isShownTool(product: EditorialTrustProductInput): boolean {
  if (typeof product.shownOnScreen === "boolean") return product.shownOnScreen;
  // Without explicit shown flag, require namedInVideo for tools
  return false;
}

/**
 * Evaluate one product against the Video Auditor trust checklist for a video.
 */
export function evaluateEditorialTrustGate(
  video: EditorialTrustVideoInput,
  product: EditorialTrustProductInput,
): TrustGateResult {
  const failures: TrustGateFailureCode[] = [];
  const reasons: string[] = [];
  const videoType = classifyVideoAffiliateType(video);

  if (!product.active || product.programStatus === "INACTIVE") {
    failures.push("INACTIVE_PRODUCT");
    reasons.push("Product or programme is inactive");
  }

  const wouldRecommendWithoutCommission = inferWouldRecommendWithoutCommission(product);
  if (!wouldRecommendWithoutCommission) {
    failures.push("NO_COMMISSION_FAIL");
    reasons.push(
      "Would not name this product if there were no commission — hard reject",
    );
  }

  if (isHighCommissionJunk(product)) {
    failures.push("HIGH_COMMISSION_JUNK");
    reasons.push(
      "High-commission junk pattern (crypto, supplements, VPN, mystery box, generic merch, …)",
    );
  }

  if (product.isUniversalSpamLink) {
    failures.push("UNIVERSAL_SPAM_LINK");
    reasons.push("Same link pasted on every video regardless of topic");
  }

  if (videoType === "SHORT" || videoType === "COMPANION_SHORT") {
    failures.push("SHORTS_ZERO_AFFILIATE");
    reasons.push("All Shorts / companion Shorts: zero affiliate links");
  }

  const namedInVideo = inferNamedInVideo(video, product);
  if (!namedInVideo) {
    failures.push("NOT_NAMED_IN_VIDEO");
    reasons.push(
      "Must be named on screen or in the VO of THIS video — not “related” or “viewers also bought”",
    );
  }

  const helps = inferHelpsViewer(video, product, videoType);
  if (!helps) {
    failures.push("DOES_NOT_HELP_VIEWER");
    reasons.push(
      "Curious viewer is not better off — product does not help do the thing the film showed",
    );
  }

  if (videoType === "WONDER") {
    if (!(namedInVideo && isBookPaperOrSkyApp(product))) {
      failures.push("WONDER_REQUIRES_NAMED_BOOK_OR_PAPER");
      reasons.push(
        "Wonder films: zero unless a specific book or paper is named on screen",
      );
    }
  }

  if (videoType === "EXPLAINER" || videoType === "UNKNOWN_LONGFORM") {
    if (!(namedInVideo && isBookPaperOrSkyApp(product))) {
      failures.push("EXPLAINER_LIMIT");
      reasons.push(
        "Explainer films: at most one book, paper, or sky app that was actually used or named",
      );
    }
  }

  if (videoType === "HOW_TO") {
    const shown = namedInVideo || isShownTool(product);
    if (!(shown && TOOL_RE.test(`${product.name} ${product.category}`))) {
      failures.push("HOW_TO_REQUIRES_SHOWN_TOOL");
      reasons.push("How-to films: one relevant tool max, only if shown / named");
    }
  }

  return {
    pass: failures.length === 0,
    failures: [...new Set(failures)],
    reasons,
    videoType,
    wouldRecommendWithoutCommission,
    namedInVideo,
  };
}

export type DescriptionLinkCandidate = {
  product: EditorialTrustProductInput;
  role?: "primary" | "secondary" | "evergreen" | "companion";
  introTone?: string;
};

/**
 * Filter & order candidates for a YouTube description under the trust gate.
 * Shorts → []. Long-form → max 1 primary (+ optional free/cheap companion), never >2.
 */
export function filterDescriptionLinksThroughTrustGate(args: {
  video: EditorialTrustVideoInput;
  candidates: DescriptionLinkCandidate[];
}): {
  accepted: DescriptionLinkCandidate[];
  rejected: Array<DescriptionLinkCandidate & { gate: TrustGateResult }>;
  videoType: VideoAffiliateType;
} {
  const videoType = classifyVideoAffiliateType(args.video);
  const rejected: Array<DescriptionLinkCandidate & { gate: TrustGateResult }> = [];

  if (videoType === "SHORT" || videoType === "COMPANION_SHORT") {
    for (const c of args.candidates) {
      const gate = evaluateEditorialTrustGate(args.video, c.product);
      rejected.push({ ...c, gate });
    }
    return { accepted: [], rejected, videoType };
  }

  const passed: DescriptionLinkCandidate[] = [];
  for (const c of args.candidates) {
    // Salesy intro tone check on candidate copy
    if (c.introTone && SALESY_RE.test(c.introTone)) {
      rejected.push({
        ...c,
        gate: {
          pass: false,
          failures: ["SALESY_TONE"],
          reasons: ["Salesy tone (“buy now / limited / % off”) is not documentary"],
          videoType,
          wouldRecommendWithoutCommission: inferWouldRecommendWithoutCommission(c.product),
          namedInVideo: inferNamedInVideo(args.video, c.product),
        },
      });
      continue;
    }

    const gate = evaluateEditorialTrustGate(args.video, c.product);
    if (!gate.pass) {
      rejected.push({ ...c, gate });
      continue;
    }
    passed.push(c);
  }

  // One primary; second only if free/cheap companion
  const accepted: DescriptionLinkCandidate[] = [];
  let primaryTaken = false;
  let companionTaken = false;

  for (const c of passed) {
    if (accepted.length >= MAX_AFFILIATE_DESCRIPTION_LINKS) {
      rejected.push({
        ...c,
        gate: {
          pass: false,
          failures: ["TOO_MANY_LINKS"],
          reasons: ["More than 2 affiliate links on a film is rejected"],
          videoType,
          wouldRecommendWithoutCommission: true,
          namedInVideo: true,
        },
      });
      continue;
    }

    const companion = inferFreeOrCheapCompanion(c.product) || c.role === "companion";

    if (!primaryTaken) {
      accepted.push({ ...c, role: "primary" });
      primaryTaken = true;
      continue;
    }

    if (!companionTaken && companion) {
      accepted.push({ ...c, role: "companion" });
      companionTaken = true;
      continue;
    }

    rejected.push({
      ...c,
      gate: {
        pass: false,
        failures: ["STACK_NOT_COMPANION"],
        reasons: [
          "Never a stack — a second link is only allowed as a free/cheap companion (e.g. paper + book)",
        ],
        videoType,
        wouldRecommendWithoutCommission: true,
        namedInVideo: true,
      },
    });
  }

  return { accepted, rejected, videoType };
}

/** Detect salesy / stacked-disclosure spam in a description body. */
export function descriptionViolatesEditorialTone(description: string): TrustGateFailureCode[] {
  const failures: TrustGateFailureCode[] = [];
  if (SALESY_RE.test(description)) failures.push("SALESY_TONE");

  const lower = description.toLowerCase();
  const stacked =
    (/#ad\b/.test(lower) ? 1 : 0) +
      (/\bsponsored\b/.test(lower) ? 1 : 0) +
      (/\baffiliate\b/.test(lower) ? 1 : 0) >=
    3;
  if (stacked) failures.push("SALESY_TONE");

  return failures;
}

/**
 * Ensure affiliate block does not outrank the film title / subscribe CTA.
 * Returns true when the first non-empty line looks like an affiliate pitch.
 * Creator voice: affiliate block must not be the first screen.
 */
export function affiliateCompetesWithPrimaryCta(description: string): boolean {
  const first = description
    .split(/\n/)
    .map((l) => l.trim())
    .find((l) => l.length > 0);
  if (!first) return false;
  if (/^if you want to go further/i.test(first)) return true;
  if (/^orbit’s next steps \(not a shop\)/i.test(first)) return true;
  if (/^orbit's next steps \(not a shop\)/i.test(first)) return true;
  if (/^some (of these )?links are affiliate/i.test(first)) return true;
  if (/^(🚀|🔭|🧠|📚|✨)/.test(first)) return true;
  if (/^(buy|shop|check out my|affiliate)/i.test(first)) return true;
  return false;
}

export function hasEditorialTrustDisclosure(description: string): boolean {
  const lower = description.toLowerCase();
  const hasAffiliatePhrase =
    lower.includes("some of these links are affiliate") ||
    lower.includes("some links are affiliate");
  const hasTrustPhrase =
    lower.includes("no commission") ||
    lower.includes("we’d still point you") ||
    lower.includes("we'd still point you") ||
    lower.includes("we’d recommend") ||
    lower.includes("we'd recommend");
  return hasAffiliatePhrase && hasTrustPhrase;
}

/**
 * Approve-path gate: throw or return failure when a placement cannot be APPROVED.
 */
export function assertPlacementApproximatelyTrusted(
  video: EditorialTrustVideoInput,
  product: EditorialTrustProductInput,
): TrustGateResult {
  return evaluateEditorialTrustGate(video, product);
}
