/**
 * Controlled P1 growth/SEO optimisation plan builders.
 * Pure helpers — no network. Mutations live in scripts/youtube-growth-optimise.ts.
 *
 * Safety invariants enforced by callers:
 * - never touch privacyStatus / publishAt
 * - never delete / upload / create video IDs
 * - never rewrite KEEP titles
 * - playlist + description mutations must be idempotent
 */

export const PUBLIC_CANONICAL_IDS = [
  "Mo93x0fxB1Q",
  "1HuV8o3gOss",
  "KcKBixwmcV4",
  "3xrxdmaOwJI",
  "JRfhE6yWom4",
  "L2OFjL4neOo",
] as const;

export const APPROVED_SCHEDULE: Record<string, string> = {
  tUAdhOnMW2g: "2026-08-10T10:30:00Z",
  svYOx07OrIM: "2026-08-11T10:30:00Z",
  B2STcIAF1lY: "2026-08-12T10:30:00Z",
  "b8-X_FyJnHM": "2026-08-13T17:00:00Z",
  ho9VJxp7f3A: "2026-08-13T19:00:00Z",
  "aoR-dA_g7eI": "2026-08-14T10:30:00Z",
  "6QFGAFZk264": "2026-08-15T10:30:00Z",
  eOOFVrJ2Ojc: "2026-08-16T10:30:00Z",
  tfTkMdE7qqw: "2026-08-20T17:00:00Z",
  bLv0RfidjSg: "2026-08-20T19:00:00Z",
  PcP64way3xA: "2026-08-21T10:30:00Z",
  pjIevt27Svo: "2026-08-22T10:30:00Z",
  AeFm7gWyWik: "2026-08-23T10:30:00Z",
};

export const PARENT_LONG_BY_FAMILY: Record<string, string> = {
  FERMI: "Mo93x0fxB1Q",
  BLACK_HOLE: "3xrxdmaOwJI",
  EXOPLANETS: "b8-X_FyJnHM",
  JWST: "tfTkMdE7qqw",
};

/** Compact semantic channel keywords (space-separated; multi-word quoted). */
export const CHANNEL_KEYWORDS =
  '"Orbit With Ben" space astronomy universe astrophysics "black holes" exoplanets "James Webb Space Telescope" JWST "alien life" cosmology "space science" "space discoveries" "science documentary" "science explained" "space documentary"';

export const CHANNEL_DESCRIPTION_AFTER = `Space stories and cosmic mysteries with Orbit — astronomy, the universe, alien worlds, black holes, James Webb discoveries, and big science questions. Wonder over clickbait. New films every week.

I'm Orbit: a small orange exploration robot on a never-ending mission to understand our universe. This channel is Pixar-warm storytelling with documentary bones — one big question at a time.

We explore:
• Cosmic mysteries — dark matter, origins, strange physics
• Alien worlds — Fermi paradox, biosignatures, the search for life
• Black holes & extreme space — what happens at the edge
• Deep-sky discoveries — James Webb Space Telescope and the early universe
• Future humanity — Mars, AI, and where we might go next

Tone: curious, careful, a little witty. Science over speculation. No conspiracy. No certainty cosplay.

Subscribe if you want the next mystery — not the loudest one.

Big questions. Deep universe.

———
Orbit with Ben
Animated space storytelling · @OrbitWithBen`;

export type PlaylistSpec = {
  key: string;
  title: string;
  description: string;
  /** Ordered video IDs — long anchor first, then supporting Shorts. */
  videoIds: string[];
  primaryIntent: string;
  journeyPurpose: string;
};

export const PLAYLIST_SPECS: PlaylistSpec[] = [
  {
    key: "start-here",
    title: "Start Here — Biggest Mysteries of Space",
    description:
      "Begin with Orbit's Cosmic Journey: the Fermi Paradox, falling into a black hole, strange alien worlds, and what the James Webb Space Telescope found at cosmic dawn. Cinematic space storytelling — wonder over clickbait.",
    videoIds: ["Mo93x0fxB1Q", "3xrxdmaOwJI", "b8-X_FyJnHM", "tfTkMdE7qqw"],
    primaryIntent: "onboarding / broad discovery",
    journeyPurpose: "Give new viewers the four long-form anchors in narrative order.",
  },
  {
    key: "black-holes",
    title: "Black Holes Explained",
    description:
      "What happens if you fall into a black hole? Event horizons, time dilation, and the strangest moments from Orbit's black hole journey — full film plus supporting Shorts.",
    videoIds: [
      "3xrxdmaOwJI",
      "JRfhE6yWom4",
      "L2OFjL4neOo",
      "tUAdhOnMW2g",
      "svYOx07OrIM",
      "B2STcIAF1lY",
    ],
    primaryIntent: "black holes / event horizon",
    journeyPurpose: "Long-form anchor → strongest Shorts → remaining BH Shorts.",
  },
  {
    key: "exoplanets",
    title: "Alien Worlds & Exoplanets",
    description:
      "Diamond crusts, glass rain sideways, three suns, and glowing hot nights — Orbit explores the strangest exoplanets we've ever found. Full Alien Worlds film plus Shorts.",
    videoIds: [
      "b8-X_FyJnHM",
      "ho9VJxp7f3A",
      "aoR-dA_g7eI",
      "6QFGAFZk264",
      "eOOFVrJ2Ojc",
    ],
    primaryIntent: "exoplanets / alien worlds",
    journeyPurpose: "Exo long → vivid Short hooks in publish order.",
  },
  {
    key: "jwst",
    title: "James Webb Space Telescope Discoveries",
    description:
      "Galaxies that appeared too early, black holes that grew too fast, and infrared eyes on cosmic dawn — what JWST actually found, told with Orbit's careful curiosity.",
    videoIds: [
      "tfTkMdE7qqw",
      "bLv0RfidjSg",
      "PcP64way3xA",
      "pjIevt27Svo",
      "AeFm7gWyWik",
    ],
    primaryIntent: "JWST / early universe",
    journeyPurpose: "JWST long → discovery Shorts.",
  },
  {
    key: "alien-life",
    title: "Alien Life & The Search for Extraterrestrials",
    description:
      "Why haven't we found aliens yet? The Fermi Paradox, quiet skies, and the possibility that the first clue is already in an archive — Orbit's alien-life cluster.",
    videoIds: ["Mo93x0fxB1Q", "1HuV8o3gOss", "KcKBixwmcV4"],
    primaryIntent: "Fermi paradox / alien life",
    journeyPurpose: "Fermi long → public Shorts that already prove Shorts-feed traction.",
  },
];

export type ShortDescriptionPlan = {
  youtubeId: string;
  family: string;
  parentLongId: string;
  beforeMarker?: string;
  description: string;
  reason: string;
};

function shortDesc(opts: {
  hook: string;
  context: string;
  parentLongId: string;
  hashtags: string;
}): string {
  return `${opts.hook}

${opts.context}

Watch the full film:
https://youtu.be/${opts.parentLongId}

${opts.hashtags}`.trim();
}

/** Idempotent Short description upgrades (thin copy + wrong JWST parent links). */
export function buildShortDescriptionPlans(): ShortDescriptionPlan[] {
  const bh = PARENT_LONG_BY_FAMILY.BLACK_HOLE;
  const exo = PARENT_LONG_BY_FAMILY.EXOPLANETS;
  const jwst = PARENT_LONG_BY_FAMILY.JWST;

  return [
    {
      youtubeId: "JRfhE6yWom4",
      family: "BLACK_HOLE",
      parentLongId: bh,
      reason: "thin BH Short description — deepen to Fermi package depth",
      description: shortDesc({
        hook: "Cross the event horizon and there is no path home — the point of no return around a black hole.",
        context:
          "One moment from Orbit's full black hole journey: event horizons, time dilation, and what physics still cannot promise.",
        parentLongId: bh,
        hashtags: "#BlackHoles #EventHorizon #Space #Shorts #OrbitWithBen",
      }),
    },
    {
      youtubeId: "L2OFjL4neOo",
      family: "BLACK_HOLE",
      parentLongId: bh,
      reason: "thin BH Short description — deepen",
      description: shortDesc({
        hook: "Falling into a black hole wouldn't feel like falling — spacetime plays a stranger trick than the movies.",
        context:
          "One moment from the full black hole documentary with Orbit — spaghettification, gravity, and honest uncertainty.",
        parentLongId: bh,
        hashtags: "#BlackHoles #Space #Astronomy #Shorts #OrbitWithBen",
      }),
    },
    {
      youtubeId: "tUAdhOnMW2g",
      family: "BLACK_HOLE",
      parentLongId: bh,
      reason: "thin scheduled BH Short description — deepen before go-live",
      description: shortDesc({
        hook: "Near a black hole, time appears to stop — not because clocks break, but because spacetime bends.",
        context:
          "One moment from Orbit's full black hole journey. Curious science storytelling, not fearbait.",
        parentLongId: bh,
        hashtags: "#BlackHoles #TimeDilation #Space #Shorts #OrbitWithBen",
      }),
    },
    {
      youtubeId: "svYOx07OrIM",
      family: "BLACK_HOLE",
      parentLongId: bh,
      reason: "thin scheduled BH Short description — deepen",
      description: shortDesc({
        hook: "Would you look back while falling into a black hole — and what would the universe look like behind you?",
        context:
          "One moment from the full black hole film with Orbit. Watch the longer journey when you want the whole picture.",
        parentLongId: bh,
        hashtags: "#BlackHoles #Space #Astronomy #Shorts #OrbitWithBen",
      }),
    },
    {
      youtubeId: "B2STcIAF1lY",
      family: "BLACK_HOLE",
      parentLongId: bh,
      reason: "thin scheduled BH Short description — deepen",
      description: shortDesc({
        hook: "What would you actually see falling into a black hole — and what would the outside universe see of you?",
        context:
          "One moment from Orbit's Cosmic Journey into black holes, event horizons, and extreme gravity.",
        parentLongId: bh,
        hashtags: "#BlackHoles #EventHorizon #Space #Shorts #OrbitWithBen",
      }),
    },
    {
      youtubeId: "ho9VJxp7f3A",
      family: "EXOPLANETS",
      parentLongId: exo,
      reason: "thin Exo Short description — deepen",
      description: shortDesc({
        hook: "It rains glass sideways on this alien world — a real exoplanet atmosphere, not science fiction.",
        context:
          "One strange world from Orbit's full Alien Worlds film about the strangest planets we've ever found.",
        parentLongId: exo,
        hashtags: "#Exoplanets #AlienWorlds #Space #Shorts #OrbitWithBen",
      }),
    },
    {
      youtubeId: "aoR-dA_g7eI",
      family: "EXOPLANETS",
      parentLongId: exo,
      reason: "thin Exo Short description — deepen",
      description: shortDesc({
        hook: "We found planets that may forge diamond in their depths — carbon-rich alien worlds beyond our Solar System.",
        context:
          "One strange world from the full Alien Worlds documentary with Orbit.",
        parentLongId: exo,
        hashtags: "#Exoplanets #AlienWorlds #Astronomy #Shorts #OrbitWithBen",
      }),
    },
    {
      youtubeId: "6QFGAFZk264",
      family: "EXOPLANETS",
      parentLongId: exo,
      reason: "thin Exo Short description — deepen",
      description: shortDesc({
        hook: "Three suns in the sky — real alien worlds orbiting multiple stars.",
        context:
          "One strange world from Orbit's Cosmic Journey through exoplanets and alien atmospheres.",
        parentLongId: exo,
        hashtags: "#Exoplanets #AlienWorlds #Space #Shorts #OrbitWithBen",
      }),
    },
    {
      youtubeId: "eOOFVrJ2Ojc",
      family: "EXOPLANETS",
      parentLongId: exo,
      reason: "thin Exo Short description — deepen",
      description: shortDesc({
        hook: "The hottest nights in the universe — tidally locked worlds that never truly cool.",
        context:
          "One strange world from the full Alien Worlds film with Orbit.",
        parentLongId: exo,
        hashtags: "#Exoplanets #HotJupiter #Space #Shorts #OrbitWithBen",
      }),
    },
    {
      youtubeId: "bLv0RfidjSg",
      family: "JWST",
      parentLongId: jwst,
      reason: "WRONG parent long link (1wxUhF3XnwI) + thin description — fix to tfTkMdE7qqw",
      beforeMarker: "1wxUhF3XnwI",
      description: shortDesc({
        hook: "These galaxies appeared too early — JWST's early-universe surprise in under a minute.",
        context:
          "One discovery from Orbit's full James Webb Space Telescope film about cosmic dawn and honest uncertainty.",
        parentLongId: jwst,
        hashtags: "#JWST #JamesWebb #EarlyUniverse #Shorts #OrbitWithBen",
      }),
    },
    {
      youtubeId: "PcP64way3xA",
      family: "JWST",
      parentLongId: jwst,
      reason: "WRONG parent long link + thin description — fix to tfTkMdE7qqw",
      beforeMarker: "1wxUhF3XnwI",
      description: shortDesc({
        hook: "How did black holes get so big so fast in the early universe? JWST keeps forcing the question.",
        context:
          "One discovery from Orbit's full JWST documentary — real observations, no certainty cosplay.",
        parentLongId: jwst,
        hashtags: "#JWST #BlackHoles #EarlyUniverse #Shorts #OrbitWithBen",
      }),
    },
    {
      youtubeId: "pjIevt27Svo",
      family: "JWST",
      parentLongId: jwst,
      reason: "WRONG parent long link + thin description — fix to tfTkMdE7qqw",
      beforeMarker: "1wxUhF3XnwI",
      description: shortDesc({
        hook: "Why JWST pictures don't match the textbook — infrared eyes rewriting cosmic dawn.",
        context:
          "One discovery from the full James Webb film with Orbit.",
        parentLongId: jwst,
        hashtags: "#JWST #Astronomy #Space #Shorts #OrbitWithBen",
      }),
    },
    {
      youtubeId: "AeFm7gWyWik",
      family: "JWST",
      parentLongId: jwst,
      reason: "WRONG parent long link + thin description — fix to tfTkMdE7qqw",
      beforeMarker: "1wxUhF3XnwI",
      description: shortDesc({
        hook: "What JWST's infrared eyes can see that Hubble never could — cooler dust, earlier light, deeper time.",
        context:
          "One discovery from Orbit's Cosmic Journey into James Webb Space Telescope findings.",
        parentLongId: jwst,
        hashtags: "#JWST #JamesWebb #Infrared #Shorts #OrbitWithBen",
      }),
    },
  ];
}

export type RegistryRelationFix = {
  youtubeVideoId: string;
  relatedLongFormVideoId: string;
  reason: string;
};

export function buildRegistryRelationFixes(
  records: Array<{
    youtubeVideoId?: string | null;
    contentType?: string | null;
    contentFamily?: string | null;
    relatedLongFormVideoId?: string | null;
  }>,
): RegistryRelationFix[] {
  const fixes: RegistryRelationFix[] = [];
  for (const r of records) {
    const id = r.youtubeVideoId;
    if (!id || r.contentType !== "shorts") continue;
    const family = r.contentFamily || "";
    const expected = PARENT_LONG_BY_FAMILY[family];
    if (!expected) continue;
    if (r.relatedLongFormVideoId === expected) continue;
    fixes.push({
      youtubeVideoId: id,
      relatedLongFormVideoId: expected,
      reason: r.relatedLongFormVideoId
        ? `mismatch relatedLongFormVideoId ${r.relatedLongFormVideoId} → ${expected}`
        : `missing relatedLongFormVideoId → ${expected}`,
    });
  }
  return fixes;
}

export function formatChannelKeywordsForApi(keywords: string): string {
  return keywords.replace(/\s+/g, " ").trim();
}

export function assertNoScheduleFieldsInSnippetUpdate(body: {
  status?: unknown;
}): void {
  if (body.status !== undefined) {
    throw new Error("SAFETY: status must not be included in snippet-only growth updates");
  }
}

export function descriptionAlreadyOptimised(
  current: string,
  planned: string,
): boolean {
  return current.trim() === planned.trim();
}

export function playlistTitleCollisionKey(title: string): string {
  return title.trim().toLowerCase();
}

export type TitleVerdict = "KEEP" | "MONITOR" | "RECOMMEND TEST LATER" | "FIX NOW";

export function classifyTitle(input: {
  title: string;
  youtubeId: string;
}): { verdict: TitleVerdict; note: string } {
  const t = input.title || "";
  if (!t.trim()) return { verdict: "FIX NOW", note: "empty title" };
  if (/terrify|you won't believe|shocking!!!/i.test(t)) {
    return { verdict: "FIX NOW", note: "fearbait / misleading tone" };
  }
  if (/TODO|PLACEHOLDER|UNTITLED/i.test(t)) {
    return { verdict: "FIX NOW", note: "placeholder title" };
  }
  if (t.length > 70) {
    return { verdict: "MONITOR", note: "may truncate on mobile — do not churn yet" };
  }
  if (input.youtubeId === "svYOx07OrIM" && t.length < 28) {
    return { verdict: "RECOMMEND TEST LATER", note: "short/vague — wait for CTR samples" };
  }
  return { verdict: "KEEP", note: "healthy / insufficient data to churn" };
}

export function scoreGrowthReadiness(input: {
  playlists: number;
  keywordsSet: boolean;
  channelDescMentionsJwst: boolean;
  thinShortDescriptionsRemaining: number;
  wrongParentLinksRemaining: number;
  orphanShortsInRegistry: number;
  studioManualRemaining: number;
}): { channelHealth: number; growthReadiness: number; subscores: Record<string, number> } {
  const subscores: Record<string, number> = {
    catalogueIntegrity: 96,
    scheduleIntegrity: 97,
    metadata: input.thinShortDescriptionsRemaining === 0 && input.wrongParentLinksRemaining === 0 ? 84 : 62,
    playlists: Math.min(95, 20 + input.playlists * 14),
    channelSeo: input.keywordsSet ? (input.channelDescMentionsJwst ? 78 : 70) : 44,
    topicalAuthority: 80,
    viewerFunnels: input.wrongParentLinksRemaining === 0 && input.orphanShortsInRegistry === 0 ? 82 : 48,
    subscriberConversion: input.channelDescMentionsJwst ? 58 : 42,
    branding: 80,
    studioConfiguration: Math.max(40, 85 - input.studioManualRemaining * 8),
    analyticsReadiness: 35,
  };
  const channelHealth = Math.round(
    Object.values(subscores).reduce((a, b) => a + b, 0) / Object.keys(subscores).length,
  );
  const growthKeys = [
    "channelSeo",
    "playlists",
    "viewerFunnels",
    "subscriberConversion",
    "metadata",
    "topicalAuthority",
    "studioConfiguration",
  ] as const;
  const growthReadiness = Math.round(
    growthKeys.reduce((a, k) => a + subscores[k], 0) / growthKeys.length,
  );
  return { channelHealth, growthReadiness, subscores };
}
