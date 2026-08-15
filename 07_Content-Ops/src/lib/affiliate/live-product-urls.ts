/**
 * Canonical public destination URLs for Orbit affiliate products.
 * Affiliate programme tags/IDs are NEVER stored here — applied at /go redirect
 * from AMAZON_ASSOCIATE_TAG / BRILLIANT_AFFILIATE_ID.
 *
 * Replace search/category URLs with exact ASINs / FLO SKUs after editorial pick.
 */

export type LiveProductUrlSpec = {
  slug: string;
  destinationUrl: string;
  /** Defaults to destinationUrl; tag/ref appended at redirect time for Amazon/Brilliant. */
  affiliateUrl?: string;
  notes: string;
};

export const LIVE_PRODUCT_URLS: LiveProductUrlSpec[] = [
  {
    slug: "beginner-telescope",
    destinationUrl: "https://www.firstlightoptics.com/telescopes/beginner-telescopes.html",
    notes:
      "FLO beginner telescopes category — swap to the exact scope Orbit names on screen when locked.",
  },
  {
    slug: "astronomy-binoculars",
    destinationUrl: "https://www.amazon.co.uk/s?k=astronomy+binoculars",
    notes: "Amazon UK search — replace with the specific binoculars ASIN after editorial pick.",
  },
  {
    slug: "beginner-astronomy-book",
    destinationUrl: "https://www.amazon.co.uk/s?k=beginner+astronomy+book",
    notes: "Amazon UK search — replace with the desk book ASIN Orbit would lend a friend.",
  },
  {
    slug: "brilliant-physics",
    destinationUrl: "https://brilliant.org/courses/physics/",
    notes: "Brilliant physics path — ref= from BRILLIANT_AFFILIATE_ID at redirect.",
  },
  {
    slug: "brilliant-mathematics",
    destinationUrl: "https://brilliant.org/courses/math/",
    notes: "Brilliant maths path — ref= from BRILLIANT_AFFILIATE_ID at redirect.",
  },
  {
    slug: "mars-book",
    destinationUrl: "https://www.amazon.co.uk/s?k=mars+planet+book",
    notes: "Amazon UK search — replace with the Mars book ASIN used in descriptions.",
  },
  {
    slug: "space-lego",
    destinationUrl: "https://www.lego.com/en-gb/themes/space",
    notes: "LEGO Space theme — programme inactive until Affiliate access; URL is public catalogue.",
  },
  {
    slug: "astrophotography-starter-kit",
    destinationUrl: "https://www.firstlightoptics.com/cameras.html",
    notes: "FLO cameras/astro entry — swap to the exact kit when named on a how-to film.",
  },
];

export function liveUrlForSlug(slug: string): LiveProductUrlSpec | undefined {
  return LIVE_PRODUCT_URLS.find((u) => u.slug === slug);
}

export function isPlaceholderAffiliateUrl(url: string): boolean {
  return /example\.invalid/i.test(url) || /PLACEHOLDER/i.test(url);
}
