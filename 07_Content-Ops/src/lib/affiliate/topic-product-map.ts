/**
 * Video Creator topic → 4-slot recommendation menu.
 * Matching may score/show up to 4 card candidates.
 * Auto-insert / approved description still follows Auditor (≤1 primary + optional companion).
 * Empty a slot rather than force a product.
 */

export type ProductFamily = "brilliant" | "telescope" | "books" | "lego";

export type TopicSlotPlan = {
  topicKey: string;
  label: string;
  /** Preferred primary family — leave null only if plan says so. */
  primary: ProductFamily | null;
  secondary: ProductFamily[];
  evergreen: ProductFamily | null;
  /** Never recommend these for this topic. */
  leaveEmpty: ProductFamily[];
  /** Kids films: Brilliant must not be primary. */
  neverBrilliantPrimary?: boolean;
  leaveEmptyIf?: string;
};

/**
 * Canonical topic keys inferred from video title/topic/keywords.
 */
export const CREATOR_TOPIC_SLOT_PLANS: TopicSlotPlan[] = [
  {
    topicKey: "black-holes",
    label: "black holes",
    primary: "books",
    secondary: ["brilliant"],
    evergreen: "brilliant",
    leaveEmpty: ["telescope", "lego"],
    leaveEmptyIf:
      "Telescope and LEGO. A backyard scope will not show a black hole. A brick model does not teach the evidence.",
  },
  {
    topicKey: "mars",
    label: "Mars",
    primary: "telescope",
    secondary: ["books", "lego"],
    evergreen: "brilliant",
    leaveEmpty: [],
    leaveEmptyIf:
      "Drop LEGO on a strictly adult investigation. Drop the scope if the film never looks at the night sky.",
  },
  {
    topicKey: "telescopes",
    label: "telescopes",
    primary: "telescope",
    secondary: ["books", "lego"],
    evergreen: "brilliant",
    leaveEmpty: [],
    leaveEmptyIf:
      "Drop LEGO if the film is mount/optics-only and a toy would undercut it.",
  },
  {
    topicKey: "jwst",
    label: "JWST",
    primary: "books",
    secondary: ["brilliant"],
    evergreen: "brilliant",
    leaveEmpty: ["telescope", "lego"],
    leaveEmptyIf:
      "Pictures-from-space / early-galaxies films: soft mention is a JWST / cosmic-dawn explainer book via /go/jwst-book (once seeded). Never Turn Left at Orion (observing guidebook) or a backyard telescope. LEGO stays out.",
  },
  {
    topicKey: "fermi",
    label: "Fermi Paradox / SETI",
    primary: "books",
    secondary: ["brilliant"],
    evergreen: "brilliant",
    leaveEmpty: ["telescope", "lego"],
    leaveEmptyIf:
      "Telescope and LEGO. The silence is not something you see through a backyard scope.",
  },
  {
    topicKey: "europa",
    label: "Europa / icy moons",
    primary: "books",
    secondary: ["brilliant"],
    evergreen: "brilliant",
    leaveEmpty: ["telescope"],
    leaveEmptyIf:
      "Telescope. Europa’s ocean is not a backyard target — recommend the ocean-worlds book.",
  },
  {
    topicKey: "relativity",
    label: "relativity",
    primary: "brilliant",
    secondary: ["books"],
    evergreen: "books",
    leaveEmpty: ["telescope", "lego"],
    leaveEmptyIf: "Telescope and LEGO. Do not fake a “see relativity” product.",
  },
  {
    topicKey: "kids",
    label: "kids astronomy",
    primary: "lego",
    secondary: ["books", "telescope"],
    evergreen: "brilliant",
    neverBrilliantPrimary: true,
    leaveEmpty: [],
    leaveEmptyIf:
      "Skip Brilliant if the audience is clearly under ~10; otherwise Brilliant as evergreen only. Never Brilliant as primary on a kids film.",
  },
  {
    topicKey: "starship",
    label: "Starship",
    primary: "books",
    secondary: ["lego", "brilliant"],
    evergreen: "brilliant",
    leaveEmpty: ["telescope"],
    leaveEmptyIf:
      "Telescope, unless the film actually goes to “watch a launch / see the sky they’re aimed at”.",
  },
  {
    topicKey: "cosmology",
    label: "cosmology",
    primary: "books",
    secondary: ["brilliant"],
    evergreen: "brilliant",
    leaveEmpty: ["telescope", "lego"],
    leaveEmptyIf:
      "Telescope and LEGO, unless it’s a kids cut of the same idea.",
  },
  {
    topicKey: "exoplanets",
    label: "exoplanets",
    primary: "books",
    secondary: ["brilliant"],
    evergreen: "brilliant",
    leaveEmpty: ["telescope"],
    leaveEmptyIf:
      "Do not sell a backyard scope as an exoplanet finder. LEGO only if an honest world-building set exists.",
  },
];

const TOPIC_PHRASES: Array<{ key: string; phrases: string[] }> = [
  { key: "black-holes", phrases: ["black hole", "black holes", "event horizon", "singularity"] },
  { key: "mars", phrases: ["mars", "martian", "perseverance", "curiosity rover"] },
  {
    key: "jwst",
    phrases: ["jwst", "james webb", "webb telescope", "cosmic dawn", "jades", "webb’s universe"],
  },
  {
    key: "fermi",
    phrases: ["fermi paradox", "fermi", "where is everybody", "great filter", "seti"],
  },
  {
    key: "europa",
    phrases: ["europa", "icy moon", "icy moons", "ocean world", "ocean worlds", "enceladus"],
  },
  {
    key: "telescopes",
    phrases: ["telescope", "telescopes", "back garden", "stargazing", "dobsonian"],
  },
  {
    key: "relativity",
    phrases: ["relativity", "spacetime", "space-time", "einstein"],
  },
  {
    key: "starship",
    phrases: ["starship", "spacex", "rocket launch", "leaving earth"],
  },
  {
    key: "exoplanets",
    phrases: ["exoplanet", "exoplanets", "habitable zone", "transit method", "alien worlds"],
  },
  {
    key: "cosmology",
    phrases: [
      "cosmology",
      "cosmic microwave",
      "large-scale structure",
      "dark energy",
      "end of the universe",
      "end of everything",
      "heat death",
      "big rip",
    ],
  },
  {
    key: "kids",
    phrases: ["kids", "children", "for kids", "junior", "young astronomer"],
  },
];

export function inferCreatorTopicKey(video: {
  title?: string | null;
  topic?: string | null;
  primaryKeyword?: string | null;
  summary?: string | null;
  category?: string | null;
  tags?: string[] | null;
}): string | null {
  const corpus = [
    video.title,
    video.topic,
    video.primaryKeyword,
    video.summary,
    video.category,
    ...(video.tags || []),
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();

  // Kids wins when clearly a kids film (even if astronomy is also present)
  if (
    /\bkids\b|\bchildren\b|for kids|junior astronomer/.test(corpus) &&
    /astronom|space|telescope|planet|mars|moon|star/.test(corpus)
  ) {
    return "kids";
  }

  for (const row of TOPIC_PHRASES) {
    if (row.key === "kids") continue;
    if (row.phrases.some((p) => corpus.includes(p))) return row.key;
  }
  if (TOPIC_PHRASES.find((r) => r.key === "kids")!.phrases.some((p) => corpus.includes(p))) {
    return "kids";
  }
  return null;
}

export function getTopicSlotPlan(topicKey: string | null): TopicSlotPlan | null {
  if (!topicKey) return null;
  return CREATOR_TOPIC_SLOT_PLANS.find((p) => p.topicKey === topicKey) || null;
}

/** Map product category / programme / tags → Creator product family. */
export function productFamilyOf(product: {
  category?: string | null;
  programSlug?: string | null;
  name?: string | null;
  tagSlugs?: string[];
}): ProductFamily | null {
  const blob = [
    product.category,
    product.programSlug,
    product.name,
    ...(product.tagSlugs || []),
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();

  if (product.programSlug === "brilliant" || /\bbrilliant\b|physics|mathematics/.test(blob)) {
    if (/book/.test(blob) && !/brilliant/.test(blob) && product.programSlug !== "brilliant") {
      /* fall through to books */
    } else if (product.programSlug === "brilliant" || /\bbrilliant\b/.test(blob)) {
      return "brilliant";
    } else if (/physics|mathematics/.test(blob) && !/book|telescope|lego/.test(blob)) {
      return "brilliant";
    }
  }
  if (/lego/.test(blob)) return "lego";
  if (/telescope|binocular/.test(blob)) return "telescope";
  if (/book|paper|journal/.test(blob)) return "books";
  if (product.programSlug === "brilliant") return "brilliant";
  return null;
}

/**
 * True when this product family is forbidden for the topic plan.
 */
export function familyForbiddenForPlan(
  family: ProductFamily | null,
  plan: TopicSlotPlan | null,
  opts?: { filmLooksAtNightSky?: boolean; adultInvestigation?: boolean; kidsUnder10?: boolean },
): boolean {
  if (!family || !plan) return false;
  if (plan.leaveEmpty.includes(family)) return true;

  // Contextual leave-empty hints (deterministic soft rules)
  if (plan.topicKey === "mars" && family === "lego" && opts?.adultInvestigation) return true;
  if (plan.topicKey === "mars" && family === "telescope" && opts?.filmLooksAtNightSky === false) {
    return true;
  }
  if (plan.topicKey === "jwst" && family === "telescope") {
    // Pictures-from-space JWST films never get a backyard scope soft mention
    return true;
  }
  if (plan.topicKey === "jwst" && family === "lego") return true;
  if (plan.topicKey === "kids" && family === "brilliant" && opts?.kidsUnder10) return true;
  if (plan.topicKey === "exoplanets" && family === "telescope") return true;
  if (plan.topicKey === "fermi" && family === "telescope") return true;
  if (plan.topicKey === "europa" && family === "telescope") return true;
  if (plan.topicKey === "starship" && family === "telescope" && opts?.filmLooksAtNightSky !== true) {
    return true;
  }
  return false;
}
