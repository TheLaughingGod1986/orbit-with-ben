/**
 * Canonical public destination URLs for Orbit affiliate products.
 *
 * Affiliate programme tags/IDs are NEVER stored here — applied at /go redirect
 * from AMAZON_ASSOCIATE_TAG / BRILLIANT_AFFILIATE_ID.
 *
 * Only confirmed amazon.co.uk product pages (or explicit inactive stubs).
 * Do not invent ASINs — leave TODO notes in seed for unconfirmed Amazon products.
 */

export type LiveProductUrlSpec = {
  slug: string;
  /** Optional display name update when applying live URLs. */
  name?: string;
  description?: string;
  destinationUrl: string;
  /**
   * Optional pre-built affiliate URL. Prefer omit/empty — /go builds from
   * destinationUrl + AMAZON_ASSOCIATE_TAG (or Brilliant env) at redirect time.
   */
  affiliateUrl?: string;
  /** Reassign product to this programme when applying (e.g. telescope → Amazon UK). */
  programmeSlug?: string;
  tags?: string[];
  /** When false, product stays inactive (e.g. LEGO until programme access). */
  active?: boolean;
  /** Catalogue fields used when creating a missing row (additive apply, no DB reset). */
  category?: string;
  price?: number;
  estimatedCommission?: number;
  featured?: boolean;
  evergreen?: boolean;
  priority?: number;
  notes: string;
};

/**
 * Confirmed Amazon Associates UK product pages (verified listings).
 * Other catalogue slugs keep seed placeholders / TODOs until an ASIN is confirmed.
 */
export const LIVE_PRODUCT_URLS: LiveProductUrlSpec[] = [
  {
    slug: "beginner-astronomy-book",
    name: "Turn Left at Orion",
    description:
      "Consolmagno & Davis — hundreds of night-sky objects for a home telescope. Orbit’s beginner desk book.",
    destinationUrl:
      "https://www.amazon.co.uk/Turn-Left-Orion-Hundreds-Telescope/dp/1108457568",
    programmeSlug: "amazon-associates-uk",
    tags: ["books", "astronomy", "beginner", "telescope"],
    category: "Astronomy books",
    price: 14.99,
    estimatedCommission: 0.6,
    evergreen: true,
    priority: 2,
    notes:
      "Verified amazon.co.uk ASIN 1108457568 (Consolmagno / Davis, 5th ed.). Tag from AMAZON_ASSOCIATE_TAG at /go — never commit the tag.",
  },
  {
    slug: "beginner-telescope",
    name: "Celestron FirstScope (Cometron 76)",
    description:
      "Celestron FirstScope tabletop Dobsonian — a practical first telescope for clear nights.",
    // Verified live amazon.co.uk product page (Cometron FirstScope 76, ASIN B00DV6SBRO).
    // Classic 21024 FirstScope (B001UQ6E4Y) returned bot/503 during verification — use Cometron listing.
    // AstroMaster 70AZ: no verified amazon.co.uk ASIN at wire-up time — do not invent one.
    destinationUrl:
      "https://www.amazon.co.uk/Celestron-21023-Cometron-FirstScope-Telescope/dp/B00DV6SBRO",
    programmeSlug: "amazon-associates-uk",
    tags: ["telescope", "beginner", "astronomy"],
    category: "Beginner telescopes",
    price: 179,
    estimatedCommission: 9,
    featured: true,
    evergreen: true,
    priority: 5,
    notes:
      "Verified amazon.co.uk ASIN B00DV6SBRO (Celestron Cometron FirstScope 76). Tag from AMAZON_ASSOCIATE_TAG at /go.",
  },
  {
    slug: "space-lego",
    destinationUrl: "https://example.invalid/dest/space-lego",
    programmeSlug: "amazon-associates-uk",
    tags: ["lego", "kids", "nasa", "spacecraft"],
    category: "Space LEGO",
    price: 49.99,
    estimatedCommission: 1.5,
    priority: 1,
    active: false,
    notes:
      "LEGO stays inactive — do not put on social or descriptions until LEGO Affiliate access. Programme slug `lego` is INACTIVE.",
  },
  {
    slug: "fermi-paradox-book",
    name: "Where Is Everybody? — Fermi Paradox (Stephen Webb)",
    description:
      "Stephen Webb — seventy-five solutions to the Fermi Paradox. The desk book for the silence.",
    destinationUrl:
      "https://www.amazon.co.uk/Universe-Teeming-EVERYBODY-Science-Fiction/dp/3319132350",
    programmeSlug: "amazon-associates-uk",
    tags: ["books", "fermi", "aliens", "seti", "astronomy"],
    category: "Space books",
    price: 29.99,
    estimatedCommission: 0.9,
    featured: false,
    evergreen: false,
    priority: 6,
    notes:
      "Verified amazon.co.uk ASIN 3319132350 (Webb, 2nd ed., ISBN 978-3-319-13235-8). Film: Fermi Paradox. Tag from AMAZON_ASSOCIATE_TAG at /go.",
  },
  {
    slug: "jwst-book",
    name: "Webb’s Universe (Maggie Aderin-Pocock)",
    description:
      "Maggie Aderin-Pocock — Webb’s images and what they reveal about cosmic history. A book, not a backyard telescope.",
    destinationUrl:
      "https://www.amazon.co.uk/Unseen-Universe-Telescope-Images-History/dp/1789295726",
    programmeSlug: "amazon-associates-uk",
    tags: ["books", "jwst", "nasa", "astronomy"],
    category: "Space books",
    price: 25,
    estimatedCommission: 0.8,
    featured: false,
    evergreen: false,
    priority: 6,
    notes:
      "Verified amazon.co.uk ASIN 1789295726 (Aderin-Pocock, Webb’s Universe, ISBN 9781789295726). Film: JWST. Not a telescope product. Tag from AMAZON_ASSOCIATE_TAG at /go.",
  },
  {
    slug: "black-hole-book",
    name: "A Brief History of Black Holes (Becky Smethurst)",
    description:
      "Dr Becky Smethurst — how we know black holes are real, without the horror-story fog.",
    destinationUrl:
      "https://www.amazon.co.uk/Brief-History-Black-Holes-everything/dp/1529086744",
    programmeSlug: "amazon-associates-uk",
    tags: ["books", "black-hole", "physics", "cosmology"],
    category: "Space books",
    price: 10.99,
    estimatedCommission: 0.4,
    featured: false,
    evergreen: false,
    priority: 7,
    notes:
      "Verified amazon.co.uk ASIN 1529086744 (Smethurst paperback, ISBN 9781529086744). Film: What Happens If You Fall Into a Black Hole? Tag from AMAZON_ASSOCIATE_TAG at /go.",
  },
  {
    slug: "cosmology-end-book",
    name: "The End of Everything (Katie Mack)",
    description:
      "Katie Mack — five astrophysical endings for the universe, written with wit and clear physics.",
    destinationUrl:
      "https://www.amazon.co.uk/End-Everything-Astrophysically-Speaking/dp/0141989580",
    programmeSlug: "amazon-associates-uk",
    tags: ["books", "cosmology", "physics"],
    category: "Space books",
    price: 10.89,
    estimatedCommission: 0.4,
    featured: false,
    evergreen: false,
    priority: 6,
    notes:
      "Verified amazon.co.uk ASIN 0141989580 (Mack, The End of Everything, ISBN 9780141989587). Film: End of the Universe. Tag from AMAZON_ASSOCIATE_TAG at /go.",
  },
  {
    slug: "exoplanet-book",
    name: "The Planet Factory (Elizabeth Tasker)",
    description:
      "Elizabeth Tasker — exoplanets and the search for a second Earth, from formation to alien landscapes.",
    destinationUrl:
      "https://www.amazon.co.uk/Planet-Factory-Exoplanets-Search-Second/dp/147291774X",
    programmeSlug: "amazon-associates-uk",
    tags: ["books", "exoplanets", "astronomy"],
    category: "Space books",
    price: 12.99,
    estimatedCommission: 0.5,
    featured: false,
    evergreen: false,
    priority: 6,
    notes:
      "Verified amazon.co.uk ASIN 147291774X (Tasker paperback, ISBN 9781472917744). Film: Alien Worlds. Tag from AMAZON_ASSOCIATE_TAG at /go.",
  },
  {
    slug: "europa-icy-moons-book",
    name: "Alien Oceans (Kevin Hand)",
    description:
      "Kevin Hand — the search for life in the ocean worlds of Europa and the outer solar system.",
    destinationUrl:
      "https://www.amazon.co.uk/Alien-Oceans-Search-Depths-Space/dp/0691227284",
    programmeSlug: "amazon-associates-uk",
    tags: ["books", "europa", "astronomy", "nasa"],
    category: "Space books",
    price: 17.99,
    estimatedCommission: 0.6,
    featured: false,
    evergreen: false,
    priority: 5,
    notes:
      "Verified amazon.co.uk ASIN 0691227284 (Hand, Alien Oceans, ISBN 9780691227283). Film: Europa / icy moons. Tag from AMAZON_ASSOCIATE_TAG at /go.",
  },
];

export function liveUrlForSlug(slug: string): LiveProductUrlSpec | undefined {
  return LIVE_PRODUCT_URLS.find((u) => u.slug === slug);
}

export function isPlaceholderAffiliateUrl(url: string): boolean {
  return !url?.trim() || /example\.invalid/i.test(url) || /PLACEHOLDER/i.test(url);
}

/** True when destination is a real amazon.co.uk product page (not a placeholder). */
export function isAmazonUkDestinationUrl(url: string): boolean {
  try {
    const u = new URL(url);
    return (
      (u.hostname === "www.amazon.co.uk" || u.hostname === "amazon.co.uk") &&
      !isPlaceholderAffiliateUrl(url)
    );
  } catch {
    return false;
  }
}

/** Active Amazon UK live destinations (excludes inactive stubs like LEGO). */
export function activeAmazonUkLiveProducts(): LiveProductUrlSpec[] {
  return LIVE_PRODUCT_URLS.filter(
    (s) => s.active !== false && isAmazonUkDestinationUrl(s.destinationUrl),
  );
}
