/**
 * Canonical long-form film → one topic book (Amazon Associates UK).
 * Social Media Manager + description placements use this map.
 *
 * Only verified amazon.co.uk /dp/ products (see live-product-urls.ts).
 * Never invent ASINs. Never hard-code AMAZON_ASSOCIATE_TAG.
 */

import { liveUrlForSlug, isAmazonUkDestinationUrl } from "./live-product-urls";
import { buildYouTubeDescriptionGoUrl } from "./go-redirect-urls";

export type FilmTopicBookWire = {
  /** Stable key for logging / tests */
  key: string;
  productSlug: string;
  /** Live YouTube id when known; null for scheduled-not-yet-uploaded films */
  youtubeVideoId: string | null;
  /** Extra ids that may appear in older project files */
  alternateYoutubeIds?: string[];
  /** Preferred Content Ops title */
  title: string;
  workingTitle?: string;
  /** Substrings (lowercase) used to match existing LongFormVideo.title / workingTitle */
  titleMatchers: string[];
  slug: string;
  topic: string;
  category: string;
  primaryKeyword: string;
  secondaryKeywords: string[];
  summary: string;
  projectFolder?: string;
  /** London air date when known (YYYY-MM-DD) */
  scheduledDate?: string;
  status: "published" | "scheduled";
};

/**
 * One book per film. Shorts are never wired here.
 * Telescope / Brilliant / LEGO are intentionally absent.
 */
export const FILM_TOPIC_BOOK_WIRES: FilmTopicBookWire[] = [
  {
    key: "alien-worlds",
    productSlug: "exoplanet-book",
    youtubeVideoId: "b8-X_FyJnHM",
    title: "Alien Worlds: The Strangest Planets We've Ever Found",
    workingTitle: "Exoplanets: Strangest Alien Worlds",
    titleMatchers: ["alien worlds", "strangest planets", "exoplanet"],
    slug: "2026-alien-worlds-strangest-planets",
    topic: "Exoplanets",
    category: "Space Documentary",
    primaryKeyword: "exoplanets",
    secondaryKeywords: ["alien worlds", "habitable zone", "hot jupiter"],
    summary:
      "A calm tour of the strangest exoplanets in the data — diamond crusts, glass rain, and worlds with three suns.",
    projectFolder: "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds",
    status: "published",
  },
  {
    key: "black-hole",
    productSlug: "black-hole-book",
    youtubeVideoId: "3xrxdmaOwJI",
    alternateYoutubeIds: ["n7CbJrOCnU0"],
    title: "What Happens If You Fall Into a Black Hole?",
    workingTitle: "What Happens If You Fall Into a Black Hole?",
    titleMatchers: ["fall into a black hole", "black hole"],
    slug: "2026-what-happens-if-you-fall-into-a-black-hole",
    topic: "Black Holes",
    category: "Space Documentary",
    primaryKeyword: "black hole",
    secondaryKeywords: ["event horizon", "spaghettification", "relativity"],
    summary: "A calm journey past the event horizon — what the pictures and the maths actually say.",
    projectFolder: "02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole",
    status: "published",
  },
  {
    key: "fermi-paradox",
    productSlug: "fermi-paradox-book",
    youtubeVideoId: "Mo93x0fxB1Q",
    title: "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained",
    workingTitle: "Will We Ever Meet Aliens?",
    titleMatchers: ["fermi paradox", "will we ever meet aliens", "haven't we found aliens"],
    slug: "2026-08-will-we-ever-meet-aliens",
    topic: "Fermi Paradox",
    category: "Space Documentary",
    primaryKeyword: "fermi paradox",
    secondaryKeywords: ["are we alone", "great filter", "seti"],
    summary:
      "A calm look at the Fermi Paradox, cosmic distances, the Great Filter, and what first contact might actually look like.",
    projectFolder: "02_Video-Projects/001_Will-We-Ever-Meet-Aliens",
    status: "published",
  },
  {
    key: "jwst",
    productSlug: "jwst-book",
    youtubeVideoId: null,
    title: "What the James Webb Telescope Discovered That Changes Everything",
    workingTitle: "JWST Discoveries That Change Everything",
    titleMatchers: ["james webb", "jwst", "webb telescope"],
    slug: "2026-08-jwst-discoveries-that-change-everything",
    topic: "JWST",
    category: "Space Documentary",
    primaryKeyword: "james webb",
    secondaryKeywords: ["jwst", "cosmic dawn", "early galaxies"],
    summary:
      "What Webb changed about cosmic dawn — early galaxies and the pictures that rewrote the timeline.",
    projectFolder: "02_Video-Projects/004_JWST-Discoveries-That-Change-Everything",
    scheduledDate: "2026-08-20",
    status: "scheduled",
  },
  {
    key: "end-of-universe",
    productSlug: "cosmology-end-book",
    youtubeVideoId: null,
    title: "The End of the Universe (Astrophysically Speaking)",
    workingTitle: "End of the Universe",
    titleMatchers: ["end of the universe", "end of everything", "heat death"],
    slug: "2026-08-end-of-the-universe",
    topic: "Cosmology",
    category: "Space Documentary",
    primaryKeyword: "end of the universe",
    secondaryKeywords: ["cosmology", "heat death", "big rip", "vacuum decay"],
    summary:
      "Five astrophysical endings for the cosmos — heat death, vacuum decay, the big rip, and what the maths still cannot close.",
    scheduledDate: "2026-08-27",
    status: "scheduled",
  },
  {
    key: "europa",
    productSlug: "europa-icy-moons-book",
    youtubeVideoId: null,
    title: "Europa and the Ocean Worlds Under the Ice",
    workingTitle: "Europa / Icy Moons",
    titleMatchers: ["europa", "icy moon", "ocean world"],
    slug: "2026-09-europa-ocean-worlds",
    topic: "Europa",
    category: "Space Documentary",
    primaryKeyword: "europa",
    secondaryKeywords: ["icy moons", "ocean worlds", "enceladus"],
    summary:
      "Under the ice of Europa and the outer moons — oceans that may have existed as long as Earth.",
    scheduledDate: "2026-09-03",
    status: "scheduled",
  },
];

/** Families / slugs that must never share a description with the topic book. */
export const TOPIC_BOOK_DESCRIPTION_BLOCKLIST_SLUGS = [
  "beginner-telescope",
  "astronomy-binoculars",
  "brilliant-physics",
  "brilliant-mathematics",
  "space-lego",
  "beginner-astronomy-book",
] as const;

export function youtubeIdsForWire(wire: FilmTopicBookWire): string[] {
  const ids = [
    wire.youtubeVideoId,
    ...(wire.alternateYoutubeIds || []),
  ].filter((id): id is string => Boolean(id));
  return [...new Set(ids)];
}

export function resolveTopicBookWireForVideo(video: {
  youtubeVideoId?: string | null;
  title?: string | null;
  workingTitle?: string | null;
  slug?: string | null;
}): FilmTopicBookWire | null {
  const yt = (video.youtubeVideoId || "").trim();
  if (yt) {
    const byId = FILM_TOPIC_BOOK_WIRES.find((w) => youtubeIdsForWire(w).includes(yt));
    if (byId) return byId;
  }

  const slug = (video.slug || "").toLowerCase();
  if (slug) {
    const bySlug = FILM_TOPIC_BOOK_WIRES.find((w) => w.slug === slug);
    if (bySlug) return bySlug;
  }

  const titleBlob = `${video.title || ""} ${video.workingTitle || ""}`.toLowerCase();
  if (!titleBlob.trim()) return null;

  for (const wire of FILM_TOPIC_BOOK_WIRES) {
    if (wire.titleMatchers.some((m) => titleBlob.includes(m))) return wire;
  }
  return null;
}

/** True when this product is the single desk book wired for the film. */
export function isWiredTopicBookForVideo(
  video: {
    youtubeVideoId?: string | null;
    title?: string | null;
    workingTitle?: string | null;
    slug?: string | null;
  },
  productSlug: string,
): boolean {
  const wire = resolveTopicBookWireForVideo(video);
  return Boolean(wire && wire.productSlug === productSlug);
}

/** Wires whose live amazon.co.uk destination is confirmed (skip if listing missing). */
export function verifiedFilmTopicBookWires(): FilmTopicBookWire[] {
  return FILM_TOPIC_BOOK_WIRES.filter((w) => {
    const live = liveUrlForSlug(w.productSlug);
    return (
      live &&
      live.active !== false &&
      isAmazonUkDestinationUrl(live.destinationUrl)
    );
  });
}

export function filmTopicBookPlacementTableRows(): Array<{
  filmTitle: string;
  youtubeId: string;
  productSlug: string;
  amazonUrl: string;
  goPath: string;
}> {
  return verifiedFilmTopicBookWires().map((w) => {
    const live = liveUrlForSlug(w.productSlug)!;
    return {
      filmTitle: w.title,
      youtubeId: w.youtubeVideoId || "(scheduled — id pending)",
      productSlug: w.productSlug,
      amazonUrl: live.destinationUrl,
      // YouTube description paste field — must include utm_source=youtube
      goPath: buildYouTubeDescriptionGoUrl({
        productSlug: w.productSlug,
        videoSlug: w.slug,
      }),
    };
  });
}
