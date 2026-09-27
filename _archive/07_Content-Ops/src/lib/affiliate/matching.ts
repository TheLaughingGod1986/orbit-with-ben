import {
  MAX_AFFILIATE_LINKS_PER_VIDEO,
  RELEVANCE_WEIGHTS,
  type AffiliateRecommendationSet,
  type ProductMatchInput,
  type ScoredRecommendation,
  type VideoMatchInput,
} from "./types";
import {
  familyForbiddenForPlan,
  getTopicSlotPlan,
  inferCreatorTopicKey,
  productFamilyOf,
  type ProductFamily,
  type TopicSlotPlan,
} from "./topic-product-map";

function parseKeywords(raw: string[] | string | null | undefined): string[] {
  if (!raw) return [];
  if (Array.isArray(raw)) return raw.map((k) => k.toLowerCase());
  try {
    const parsed = JSON.parse(raw) as unknown;
    if (Array.isArray(parsed)) return parsed.map((k) => String(k).toLowerCase());
  } catch {
    /* fall through */
  }
  return raw
    .split(/[,;|]/)
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean);
}

function normalize(text: string): string {
  return text.toLowerCase().replace(/[^a-z0-9\s-]/g, " ").replace(/\s+/g, " ").trim();
}

function tokenize(...parts: Array<string | null | undefined>): Set<string> {
  const tokens = new Set<string>();
  for (const part of parts) {
    if (!part) continue;
    for (const t of normalize(part).split(" ")) {
      if (t.length >= 3) tokens.add(t);
    }
  }
  return tokens;
}

/** Map common topic phrases → canonical tag slugs. */
const TOPIC_TAG_ALIASES: Record<string, string[]> = {
  "black hole": ["black-hole", "physics", "cosmology", "relativity"],
  "black holes": ["black-hole", "physics", "cosmology"],
  fermi: ["fermi", "aliens", "seti", "astronomy"],
  "fermi paradox": ["fermi", "aliens", "seti", "astronomy"],
  alien: ["aliens", "seti"],
  aliens: ["aliens", "seti"],
  seti: ["seti", "aliens", "fermi"],
  mars: ["mars", "nasa", "astronomy"],
  moon: ["moon", "nasa", "astronomy"],
  telescope: ["telescope", "astronomy", "beginner"],
  telescopes: ["telescope", "astronomy"],
  astronomy: ["astronomy"],
  cosmology: ["cosmology", "physics"],
  physics: ["physics"],
  relativity: ["relativity", "physics"],
  quantum: ["quantum", "physics"],
  exoplanet: ["exoplanets", "astronomy"],
  exoplanets: ["exoplanets", "astronomy"],
  spacex: ["spacex", "starship", "nasa"],
  starship: ["starship", "spacex"],
  nasa: ["nasa"],
  lego: ["lego", "kids"],
  ai: ["ai"],
  "artificial intelligence": ["ai"],
  mathematics: ["mathematics"],
  maths: ["mathematics"],
  math: ["mathematics"],
  engineering: ["engineering"],
  orbital: ["orbital-mechanics", "physics"],
  orbit: ["orbital-mechanics", "astronomy"],
  binoculars: ["binoculars", "astronomy", "beginner"],
  astrophotography: ["astrophotography", "telescope"],
  beginner: ["beginner", "astronomy"],
  kids: ["kids"],
  book: ["books"],
  books: ["books"],
  jupiter: ["astronomy", "planets"],
  saturn: ["astronomy"],
  jwst: ["jwst", "astronomy", "nasa"],
  "james webb": ["jwst", "astronomy", "nasa"],
  webb: ["jwst", "astronomy", "nasa"],
  "cosmic dawn": ["jwst", "cosmology", "astronomy"],
  europa: ["europa", "astronomy", "nasa"],
  "icy moon": ["europa", "astronomy"],
  "icy moons": ["europa", "astronomy"],
  "ocean world": ["europa", "astronomy"],
  "ocean worlds": ["europa", "astronomy"],
};

function inferTagsFromText(text: string): Set<string> {
  const n = normalize(text);
  const tags = new Set<string>();
  for (const [phrase, mapped] of Object.entries(TOPIC_TAG_ALIASES)) {
    if (n.includes(phrase)) {
      for (const t of mapped) tags.add(t);
    }
  }
  return tags;
}

export type RelevanceStrategy = {
  scoreAffiliateRelevance(
    video: VideoMatchInput,
    product: ProductMatchInput,
  ): { score: number; reasons: string[] };
};

/**
 * Deterministic first-pass matcher.
 * Future LLM strategy can implement the same RelevanceStrategy interface.
 */
export const deterministicRelevanceStrategy: RelevanceStrategy = {
  scoreAffiliateRelevance(video, product) {
    const reasons: string[] = [];
    let score = 0;

    if (!product.active) {
      return { score: 0, reasons: ["inactive product"] };
    }
    if (product.programStatus && product.programStatus !== "ACTIVE") {
      return { score: 0, reasons: ["programme inactive"] };
    }

    const episodeType = video.episodeType || video.category || "";
    if (
      product.unsuitableFor?.length &&
      episodeType &&
      product.unsuitableFor.some(
        (u) => normalize(u) === normalize(episodeType) || normalize(episodeType).includes(normalize(u)),
      )
    ) {
      return { score: 0, reasons: ["unsuitable for episode type"] };
    }

    const videoCorpus = [
      video.title,
      video.workingTitle,
      video.topic,
      video.category,
      video.summary,
      video.primaryKeyword,
      ...(video.chapterTitles || []),
      ...(video.tags || []),
      ...parseKeywords(video.secondaryKeywords),
      // Light script sample for keyword hits only (first 2k chars)
      (video.script || "").slice(0, 2000),
    ]
      .filter(Boolean)
      .join(" ");

    const videoTags = new Set<string>([
      ...inferTagsFromText(videoCorpus),
      ...(video.tags || []).map((t) => normalize(t).replace(/\s+/g, "-")),
    ]);
    const productTags = new Set(product.tagSlugs.map((t) => normalize(t).replace(/\s+/g, "-")));

    const topicNorm = normalize(video.topic);
    const primaryKw = normalize(video.primaryKeyword || "");

    // Exact primary topic / keyword ↔ product tags or category
    const primaryHits = [...productTags].filter(
      (t) =>
        topicNorm.includes(t.replace(/-/g, " ")) ||
        primaryKw.includes(t.replace(/-/g, " ")) ||
        videoTags.has(t),
    );
    if (primaryHits.length > 0) {
      const exact =
        primaryHits.some(
          (t) =>
            topicNorm === t.replace(/-/g, " ") ||
            topicNorm.includes(t.replace(/-/g, " ")) ||
            primaryKw.includes(t.replace(/-/g, " ")),
        ) || [...inferTagsFromText(video.topic)].some((t) => productTags.has(t));
      if (exact) {
        score += RELEVANCE_WEIGHTS.exactPrimaryTopic;
        reasons.push(`exact topic match (+${RELEVANCE_WEIGHTS.exactPrimaryTopic})`);
      } else {
        score += RELEVANCE_WEIGHTS.relatedTopic;
        reasons.push(`related topic (+${RELEVANCE_WEIGHTS.relatedTopic})`);
      }
    } else {
      // Related via shared inferred tags
      const overlap = [...productTags].filter((t) => videoTags.has(t));
      if (overlap.length > 0) {
        score += RELEVANCE_WEIGHTS.relatedTopic;
        reasons.push(`related tags: ${overlap.slice(0, 3).join(", ")} (+${RELEVANCE_WEIGHTS.relatedTopic})`);
      }
    }

    // Tag exact bonus
    const exactTagHits = [...productTags].filter((t) => videoTags.has(t));
    if (exactTagHits.length > 0) {
      const bonus = Math.min(
        RELEVANCE_WEIGHTS.tagExact * exactTagHits.length,
        RELEVANCE_WEIGHTS.tagExact * 2,
      );
      score += bonus;
      reasons.push(`tag overlap (+${bonus})`);
    }

    // Category alignment
    const catNorm = normalize(product.category);
    const videoCat = normalize(video.category || "");
    const videoTokens = tokenize(videoCorpus);
    if (
      (videoCat && (videoCat.includes(catNorm) || catNorm.includes(videoCat))) ||
      [...tokenize(product.category, product.subcategory, product.name)].some((t) =>
        videoTokens.has(t),
      )
    ) {
      score += RELEVANCE_WEIGHTS.category;
      reasons.push(`category (+${RELEVANCE_WEIGHTS.category})`);
    }

    // Keyword hits in title/description
    const productTokens = tokenize(product.name, product.description, product.category);
    let keywordHits = 0;
    for (const t of productTokens) {
      if (videoTokens.has(t)) keywordHits += 1;
    }
    if (keywordHits >= 2) {
      score += RELEVANCE_WEIGHTS.keywordHit;
      reasons.push(`keyword hits (+${RELEVANCE_WEIGHTS.keywordHit})`);
    }

    // Editorial gate: featured / evergreen / priority must not promote unrelated junk.
    // Require at least one content signal (topic, tag, category, or keyword hit).
    const hasEditorialSignal = reasons.some((r) =>
      /exact topic|related topic|related tags|tag overlap|category|keyword hits/.test(r),
    );
    if (!hasEditorialSignal) {
      return { score: 0, reasons: ["no editorial relevance — excluded"] };
    }

    if (product.evergreen) {
      score += RELEVANCE_WEIGHTS.evergreenGeneral;
      reasons.push(`evergreen (+${RELEVANCE_WEIGHTS.evergreenGeneral})`);
    }

    if (product.featured) {
      score += RELEVANCE_WEIGHTS.manuallyFeatured;
      reasons.push(`featured (+${RELEVANCE_WEIGHTS.manuallyFeatured})`);
    }

    if (product.priority > 0) {
      const boost = Math.min(product.priority * RELEVANCE_WEIGHTS.priorityBoost, 8);
      score += boost;
      reasons.push(`priority (+${boost})`);
    }

    return { score, reasons };
  },
};

let activeStrategy: RelevanceStrategy = deterministicRelevanceStrategy;

export function setRelevanceStrategy(strategy: RelevanceStrategy): void {
  activeStrategy = strategy;
}

export function getRelevanceStrategy(): RelevanceStrategy {
  return activeStrategy;
}

export function scoreAffiliateRelevance(
  video: VideoMatchInput,
  product: ProductMatchInput,
): { score: number; reasons: string[] } {
  return activeStrategy.scoreAffiliateRelevance(video, product);
}

/**
 * Return strongest recommendations using Creator topic → 4-slot menu when known.
 * Matching may still return up to 4 card candidates. Empty a slot rather than force.
 * Description auto-insert remains Auditor-capped separately.
 */
export function recommendProductsForVideo(
  video: VideoMatchInput,
  products: ProductMatchInput[],
  options?: {
    maxLinks?: number;
    minScore?: number;
    filmLooksAtNightSky?: boolean;
    adultInvestigation?: boolean;
    kidsUnder10?: boolean;
  },
): AffiliateRecommendationSet {
  const maxLinks = options?.maxLinks ?? MAX_AFFILIATE_LINKS_PER_VIDEO;
  const minScore = options?.minScore ?? 15;
  const topicKey = inferCreatorTopicKey(video);
  const plan = getTopicSlotPlan(topicKey);

  const scored: ScoredRecommendation[] = products
    .map((product) => {
      const { score, reasons } = scoreAffiliateRelevance(video, product);
      const family = productFamilyOf(product);
      const forbidden = familyForbiddenForPlan(family, plan, {
        filmLooksAtNightSky: options?.filmLooksAtNightSky,
        adultInvestigation: options?.adultInvestigation,
        kidsUnder10: options?.kidsUnder10,
      });
      if (forbidden) {
        return {
          product,
          relevanceScore: 0,
          reasons: [
            ...reasons,
            plan?.leaveEmptyIf
              ? `topic map leave-empty: ${plan.leaveEmptyIf}`
              : "topic map leave-empty",
          ],
          role: "secondary" as const,
        };
      }
      // Soft boost when product family matches a planned slot
      let adjusted = score;
      const slotReasons = [...reasons];
      if (plan && family && score >= minScore) {
        if (plan.primary === family) {
          adjusted += 12;
          slotReasons.push("topic-map primary family (+12)");
        } else if (plan.secondary.includes(family)) {
          adjusted += 6;
          slotReasons.push("topic-map secondary family (+6)");
        } else if (plan.evergreen === family) {
          adjusted += 4;
          slotReasons.push("topic-map evergreen family (+4)");
        }
      }
      return {
        product,
        relevanceScore: adjusted,
        reasons: slotReasons,
        role: "secondary" as const,
      };
    })
    .filter((s) => s.relevanceScore >= minScore)
    .sort((a, b) => {
      if (b.relevanceScore !== a.relevanceScore) return b.relevanceScore - a.relevanceScore;
      if (a.product.featured !== b.product.featured) return a.product.featured ? -1 : 1;
      return a.product.name.localeCompare(b.product.name);
    });

  if (plan) {
    return assignSlotsFromTopicPlan(scored, plan, maxLinks);
  }

  return assignSlotsLegacy(scored, maxLinks);
}

function pickByFamily(
  list: ScoredRecommendation[],
  used: Set<string>,
  family: ProductFamily | null,
  role: ScoredRecommendation["role"],
): ScoredRecommendation | null {
  if (!family) return null;
  for (const item of list) {
    if (used.has(item.product.id)) continue;
    if (productFamilyOf(item.product) !== family) continue;
    used.add(item.product.id);
    return { ...item, role };
  }
  return null;
}

function pickAny(
  list: ScoredRecommendation[],
  used: Set<string>,
  role: ScoredRecommendation["role"],
  predicate?: (s: ScoredRecommendation) => boolean,
): ScoredRecommendation | null {
  for (const item of list) {
    if (used.has(item.product.id)) continue;
    if (predicate && !predicate(item)) continue;
    used.add(item.product.id);
    return { ...item, role };
  }
  return null;
}

/**
 * Fill Creator 4-slot menu. Empty a slot rather than force an unrelated product.
 */
function assignSlotsFromTopicPlan(
  scored: ScoredRecommendation[],
  plan: TopicSlotPlan,
  maxLinks: number,
): AffiliateRecommendationSet {
  const used = new Set<string>();

  let primaryFamily = plan.primary;
  if (plan.neverBrilliantPrimary && primaryFamily === "brilliant") {
    primaryFamily = plan.secondary.find((f) => f !== "brilliant") || null;
  }

  let primary =
    pickByFamily(scored, used, primaryFamily, "primary") ||
    // JWST: explainer book only (never telescope / LEGO on pictures-from-space films)
    (plan.topicKey === "jwst"
      ? pickByFamily(scored, used, "books", "primary")
      : null);

  // Kids: never allow Brilliant as primary even via fallback
  if (
    primary &&
    plan.neverBrilliantPrimary &&
    productFamilyOf(primary.product) === "brilliant"
  ) {
    used.delete(primary.product.id);
    primary =
      pickByFamily(scored, used, "lego", "primary") ||
      pickByFamily(scored, used, "books", "primary") ||
      pickByFamily(scored, used, "telescope", "primary");
  }

  const secondary: ScoredRecommendation[] = [];
  for (const fam of plan.secondary) {
    if (secondary.length >= 2) break;
    const next = pickByFamily(scored, used, fam, "secondary");
    if (next) secondary.push(next);
    // empty slot rather than force
  }

  let evergreen: ScoredRecommendation | null = null;
  if (plan.evergreen) {
    // “Brilliant if the book is primary; else the book”
    if (
      plan.topicKey === "black-holes" ||
      plan.topicKey === "relativity" ||
      plan.topicKey === "cosmology" ||
      plan.topicKey === "exoplanets"
    ) {
      const primaryFam = primary ? productFamilyOf(primary.product) : null;
      const evergreenFam =
        primaryFam === "books" ? "brilliant" : primaryFam === "brilliant" ? "books" : plan.evergreen;
      evergreen = pickByFamily(scored, used, evergreenFam, "evergreen");
    } else if (plan.neverBrilliantPrimary && plan.evergreen === "brilliant") {
      // Kids: Brilliant only as evergreen when not under-10 exclusion (already filtered)
      evergreen = pickByFamily(scored, used, "brilliant", "evergreen");
    } else {
      evergreen = pickByFamily(scored, used, plan.evergreen, "evergreen");
    }
  }

  // Do not back-fill empty slots with leaveEmpty families or random products
  const all = [primary, ...secondary, evergreen]
    .filter((x): x is ScoredRecommendation => x != null)
    .slice(0, maxLinks);

  return {
    primary: all.find((a) => a.role === "primary") || all[0] || null,
    secondary: all.filter((a) => a.role === "secondary").slice(0, 2),
    evergreen: all.find((a) => a.role === "evergreen") || null,
    all,
  };
}

function assignSlotsLegacy(
  scored: ScoredRecommendation[],
  maxLinks: number,
): AffiliateRecommendationSet {
  const used = new Set<string>();
  const primary = pickAny(scored, used, "primary");
  const secondary: ScoredRecommendation[] = [];
  while (secondary.length < 2) {
    const next = pickAny(scored, used, "secondary");
    if (!next) break;
    secondary.push(next);
  }
  const evergreen =
    pickAny(scored, used, "evergreen", (s) => s.product.evergreen) ||
    pickAny(scored, used, "evergreen", (s) =>
      /astronomy|beginner|telescope|books/i.test(
        `${s.product.category} ${s.product.tagSlugs.join(" ")}`,
      ),
    );

  const all = [primary, ...secondary, evergreen]
    .filter((x): x is ScoredRecommendation => x != null)
    .slice(0, maxLinks);

  return {
    primary: all.find((a) => a.role === "primary") || all[0] || null,
    secondary: all.filter((a) => a.role === "secondary").slice(0, 2),
    evergreen: all.find((a) => a.role === "evergreen") || null,
    all,
  };
}

/** Prevent duplicate product links in a description placement set. */
export function dedupeRecommendations(
  items: ScoredRecommendation[],
): ScoredRecommendation[] {
  const seen = new Set<string>();
  const out: ScoredRecommendation[] = [];
  for (const item of items) {
    if (seen.has(item.product.id) || seen.has(item.product.slug)) continue;
    seen.add(item.product.id);
    seen.add(item.product.slug);
    out.push(item);
  }
  return out;
}
