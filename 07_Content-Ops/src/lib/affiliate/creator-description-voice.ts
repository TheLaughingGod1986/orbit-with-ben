/**
 * Video Creator — official Orbit affiliate description voice.
 * Placeholders only ({brilliant_link}, etc.). No hard-coded affiliate IDs.
 * Do not invent salesy variants.
 */

export const CREATOR_AFFILIATE_DISCLOSURE =
  "Some of these links are affiliate links. We only share things we’d still point you to with no commission.";

/** Prefer this header; alternate is also allowed. */
export const CREATOR_SECTION_HEADERS = {
  primary: "If you want to go further",
  alternate: "Orbit’s next steps (not a shop)",
} as const;

/** Phrases that must never appear in Orbit affiliate description copy. */
export const CREATOR_BANNED_DESCRIPTION_PHRASES = [
  "buy now",
  "must-have",
  "must have",
  "limited",
  "limited time",
  "support the channel by shopping",
  "support the channel by buying",
  "countdown",
  "bundle",
  "act now",
  "shop now",
  "% off",
  "percent off",
] as const;

/** Default product intros (Creator templates). */
export const CREATOR_PRODUCT_TEMPLATES = {
  brilliant:
    "If this film left you wanting the math under the pictures, Brilliant is where I’d send you to practice. Not more videos. A problem you work until it clicks.",
  telescope:
    "The objects in this film are not only on a screen. A first telescope is how a lot of people meet Saturn’s rings or the Moon’s craters for real. Start simple. Learn the night. Upgrade later.",
  books:
    "A film can open a question. A good book sits with the uncertainty longer. This is the one I’d keep on the desk after this episode.",
  lego:
    "Some ideas are easier to hold when you can build them. This set is a small model of a real machine. Useful for kids, and for anyone who thinks with their hands.",
  binoculars:
    "The objects in this film are not only on a screen. Starting under the night sky with binoculars is how a lot of people learn the night before a first telescope.",
  paper: "The paper named in this film:",
  general: "If you want to go further on what this film opened:",
} as const;

/** Topic-tuned book first lines (replace the generic books intro when topic matches). */
export const CREATOR_BOOK_TOPIC_FIRST_LINES: Record<string, string> = {
  "black-holes":
    "How we actually know a black hole is there, without turning it into a horror story.",
  black_holes:
    "How we actually know a black hole is there, without turning it into a horror story.",
  mars: "Mars as a world we can measure, not a poster.",
  telescopes:
    "Why a mirror collects light, and what that lets you see from a back garden.",
  jwst: "What Webb changed about cosmic dawn, written at the pace of a desk, not a trailer.",
  relativity: "The part of spacetime you can follow with a pencil.",
  kids: "A first book that treats kids as curious, not as a market.",
  starship: "How a rocket actually leaves Earth, without the press-conference fog.",
  cosmology:
    "The universe at the largest scale, including the parts we still cannot close.",
  fermi:
    "Seventy-five ways to read the silence — the desk book for the Fermi Paradox.",
  europa:
    "Oceans under the ice of Europa and the outer moons — habitability without a backyard scope.",
  exoplanets:
    "A film can open a question. A good book sits with the uncertainty longer. This is the one I’d keep on the desk after this episode.",
};

/** Topic-tuned LEGO first lines. */
export const CREATOR_LEGO_TOPIC_FIRST_LINES: Record<string, string> = {
  jwst:
    "Webb is a real machine. Building a small one is a good way to remember the unfolding mirrors, not just the pictures it sends home.",
  mars: "A rover you can hold is a decent way to feel how careful a landing has to be.",
  starship: "A stack of tanks and engines, at a scale you can walk around on a table.",
  kids: "Hubble or Webb as a model, so the “eye in space” is not only a phrase.",
  telescopes:
    "Hubble or Webb as a model, so the “eye in space” is not only a phrase.",
};

export type CreatorTemplateMap = Record<string, string>;

/** Keys seeded into AffiliateDescriptionTemplate (editable in admin). */
export function buildCreatorDescriptionTemplateMap(
  overrides?: Partial<CreatorTemplateMap>,
): CreatorTemplateMap {
  const map: CreatorTemplateMap = {
    section_header: CREATOR_SECTION_HEADERS.primary,
    section_header_alt: CREATOR_SECTION_HEADERS.alternate,
    brilliant: CREATOR_PRODUCT_TEMPLATES.brilliant,
    telescope: CREATOR_PRODUCT_TEMPLATES.telescope,
    binoculars: CREATOR_PRODUCT_TEMPLATES.binoculars,
    books: CREATOR_PRODUCT_TEMPLATES.books,
    lego: CREATOR_PRODUCT_TEMPLATES.lego,
    paper: CREATOR_PRODUCT_TEMPLATES.paper,
    general: CREATOR_PRODUCT_TEMPLATES.general,
    disclosure: CREATOR_AFFILIATE_DISCLOSURE,
    amazon_disclosure:
      "As an Amazon Associate I earn from qualifying purchases.",
    // Topic-tuned books
    books_black_holes: CREATOR_BOOK_TOPIC_FIRST_LINES["black-holes"],
    books_mars: CREATOR_BOOK_TOPIC_FIRST_LINES.mars,
    books_telescopes: CREATOR_BOOK_TOPIC_FIRST_LINES.telescopes,
    books_jwst: CREATOR_BOOK_TOPIC_FIRST_LINES.jwst,
    books_relativity: CREATOR_BOOK_TOPIC_FIRST_LINES.relativity,
    books_kids: CREATOR_BOOK_TOPIC_FIRST_LINES.kids,
    books_starship: CREATOR_BOOK_TOPIC_FIRST_LINES.starship,
    books_cosmology: CREATOR_BOOK_TOPIC_FIRST_LINES.cosmology,
    books_exoplanets: CREATOR_BOOK_TOPIC_FIRST_LINES.exoplanets,
    books_fermi: CREATOR_BOOK_TOPIC_FIRST_LINES.fermi,
    books_europa: CREATOR_BOOK_TOPIC_FIRST_LINES.europa,
    // Topic-tuned LEGO
    lego_jwst: CREATOR_LEGO_TOPIC_FIRST_LINES.jwst,
    lego_mars: CREATOR_LEGO_TOPIC_FIRST_LINES.mars,
    lego_starship: CREATOR_LEGO_TOPIC_FIRST_LINES.starship,
    lego_kids: CREATOR_LEGO_TOPIC_FIRST_LINES.kids,
    lego_telescopes: CREATOR_LEGO_TOPIC_FIRST_LINES.telescopes,
  };
  return { ...map, ...(overrides as CreatorTemplateMap) };
}

export function descriptionContainsCreatorBannedPhrase(text: string): boolean {
  const lower = text.toLowerCase();
  return CREATOR_BANNED_DESCRIPTION_PHRASES.some((p) => lower.includes(p));
}

/**
 * Resolve book/LEGO intro for a video topic key.
 */
export function resolveTopicTunedIntro(args: {
  family: "books" | "lego" | "brilliant" | "telescope" | "binoculars" | "paper" | "general";
  topicKey: string | null;
  templates: CreatorTemplateMap;
}): string {
  const { family, topicKey, templates } = args;
  if (family === "books" && topicKey) {
    const key = `books_${topicKey.replace(/-/g, "_")}`;
    const alt = `books_${topicKey}`;
    if (templates[key]) return templates[key];
    if (templates[alt]) return templates[alt];
    // black-holes hyphen form stored as books_black_holes
    if (topicKey === "black-holes" && templates.books_black_holes) {
      return templates.books_black_holes;
    }
  }
  if (family === "lego" && topicKey) {
    const key = `lego_${topicKey.replace(/-/g, "_")}`;
    if (templates[key]) return templates[key];
    if (templates[`lego_${topicKey}`]) return templates[`lego_${topicKey}`];
  }
  return templates[family] || templates.general || CREATOR_PRODUCT_TEMPLATES.general;
}
