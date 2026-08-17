import {
  DEFAULT_AMAZON_DISCLOSURE,
  type ScoredRecommendation,
} from "./types";
import { buildYouTubeDescriptionGoUrl } from "./urls";
import {
  descriptionViolatesEditorialTone,
  filterDescriptionLinksThroughTrustGate,
  hasEditorialTrustDisclosure,
  type EditorialTrustProductInput,
  type EditorialTrustVideoInput,
} from "./editorial-trust-gate";
import {
  buildCreatorDescriptionTemplateMap,
  CREATOR_AFFILIATE_DISCLOSURE,
  CREATOR_SECTION_HEADERS,
  descriptionContainsCreatorBannedPhrase,
  resolveTopicTunedIntro,
} from "./creator-description-voice";
import {
  inferCreatorTopicKey,
  productFamilyOf,
  type ProductFamily,
} from "./topic-product-map";

export type DescriptionTemplateMap = Record<string, string>;

/** Creator voice defaults — editable via AffiliateDescriptionTemplate admin rows. */
export const DEFAULT_AFFILIATE_TEMPLATES: DescriptionTemplateMap =
  buildCreatorDescriptionTemplateMap();

export type AffiliateDescriptionLink = {
  productName: string;
  productSlug: string;
  category: string;
  programSlug?: string;
  url: string;
  role?: ScoredRecommendation["role"] | "companion";
  templateKey?: string;
  trustProduct?: EditorialTrustProductInput;
};

function familyFromLink(
  link: AffiliateDescriptionLink,
): ProductFamily | "binoculars" | "paper" | "general" {
  const fam = productFamilyOf({
    category: link.category,
    programSlug: link.programSlug,
    name: link.productName,
  });
  if (fam) return fam;
  const cat = link.category.toLowerCase();
  if (/paper|journal|arxiv/i.test(cat)) return "paper";
  if (/binocular/i.test(cat)) return "binoculars";
  return "general";
}

function pickTemplateKey(link: AffiliateDescriptionLink): string {
  if (link.templateKey) return link.templateKey;
  return familyFromLink(link);
}

function descriptionAlreadyHasDisclosure(description: string): boolean {
  if (hasEditorialTrustDisclosure(description)) return true;
  const lower = description.toLowerCase();
  return (
    lower.includes("some of these links are affiliate") ||
    lower.includes("some links are affiliate") ||
    lower.includes("affiliate link") ||
    lower.includes("amazon associate") ||
    lower.includes("may receive a commission") ||
    lower.includes("earns from qualifying purchases")
  );
}

function needsAmazonDisclosure(links: AffiliateDescriptionLink[]): boolean {
  return links.some(
    (l) =>
      l.programSlug === "amazon-associates-uk" ||
      /amazon\.(co\.uk|com)/i.test(l.url),
  );
}

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/** Absolute or path-only `/go/{slug}` with optional query (YouTube description paste). */
export function orbitGoUrlPatternForSlug(productSlug: string): RegExp {
  const escaped = escapeRegExp(productSlug);
  return new RegExp(
    `(?:https?:\\/\\/[^\\s<>"']+)?\\/go\\/${escaped}(?:\\?[^\\s<>"']*)?`,
    "gi",
  );
}

export function goUrlHasYoutubeUtmSource(urlText: string): boolean {
  try {
    const u = /^https?:\/\//i.test(urlText)
      ? new URL(urlText)
      : new URL(urlText, "https://example.invalid");
    return (
      (u.searchParams.get("utm_source") || "").trim().toLowerCase() === "youtube"
    );
  } catch {
    return /(?:^|[?&])utm_source=youtube(?:&|$)/i.test(urlText);
  }
}

/**
 * Upgrade a matched `/go/{slug}` to a stamped YouTube description URL.
 * Keeps existing medium/campaign/content; always sets utm_source=youtube.
 * Already-stamped youtube matches are returned unchanged.
 */
export function stampMatchAsYouTubeDescriptionGoUrl(
  rawMatch: string,
  args: { productSlug: string; videoSlug?: string | null },
): string {
  if (goUrlHasYoutubeUtmSource(rawMatch)) return rawMatch;
  const stamped = buildYouTubeDescriptionGoUrl(args);
  try {
    const isAbsolute = /^https?:\/\//i.test(rawMatch);
    const existing = isAbsolute
      ? new URL(rawMatch)
      : new URL(rawMatch, "https://example.invalid");
    const target = new URL(stamped);
    for (const key of ["utm_medium", "utm_campaign", "utm_content"] as const) {
      const v = existing.searchParams.get(key);
      if (v) target.searchParams.set(key, v);
    }
    target.searchParams.set("utm_source", "youtube");
    return target.toString();
  } catch {
    return stamped;
  }
}

/**
 * In-place upgrade of bare/unstamped `/go/{slug}` doors in a YouTube description.
 * Does not insert a new affiliate block. Leaves utm_source=youtube URLs alone.
 */
export function upgradeYouTubeDescriptionGoUrls(args: {
  description: string;
  productSlugs: string[];
  videoSlug?: string | null;
}): { description: string; foundAnyGo: boolean; upgradedAny: boolean } {
  let text = args.description;
  let foundAnyGo = false;
  let upgradedAny = false;
  for (const productSlug of args.productSlugs) {
    const pattern = orbitGoUrlPatternForSlug(productSlug);
    text = text.replace(pattern, (match) => {
      foundAnyGo = true;
      if (goUrlHasYoutubeUtmSource(match)) return match;
      upgradedAny = true;
      return stampMatchAsYouTubeDescriptionGoUrl(match, {
        productSlug,
        videoSlug: args.videoSlug,
      });
    });
  }
  return { description: text, foundAnyGo, upgradedAny };
}

/** Strip a leading disclosure line if an older generator put it first. */
function stripLeadingDisclosure(description: string): string {
  const lines = description.split("\n");
  const first = lines[0]?.trim() || "";
  if (
    /^some (of these )?links are affiliate/i.test(first) ||
    /^as an amazon associate/i.test(first)
  ) {
    return lines.slice(1).join("\n").replace(/^\n+/, "").trim();
  }
  return description.trim();
}

/**
 * Insert affiliate block AFTER chapters + subscribe CTA, BEFORE playlist / next film / hashtags.
 * Never in the first screen of the description.
 */
export function insertAffiliateBlockAfterPrimaryCta(
  description: string,
  affiliateBlock: string,
): string {
  const body = description.trimEnd();
  if (!body) return affiliateBlock.trim();
  if (!affiliateBlock.trim()) return body;

  const lines = body.split("\n");
  let cut = lines.length;

  for (let i = 0; i < lines.length; i++) {
    const t = lines[i].trim();
    if (
      /^playlist\b/i.test(t) ||
      /^next film\b/i.test(t) ||
      /^watch next\b/i.test(t) ||
      /^more from orbit\b/i.test(t) ||
      /^more orbit\b/i.test(t) ||
      /^#\w/.test(t)
    ) {
      cut = i;
      break;
    }
  }

  const before = lines.slice(0, cut).join("\n").trimEnd();
  const after = lines.slice(cut).join("\n").trim();
  if (after) {
    return `${before}\n\n${affiliateBlock.trim()}\n\n${after}`.trim();
  }
  return `${before}\n\n${affiliateBlock.trim()}`.trim();
}

/**
 * Build the affiliate block for a YouTube long-form description (Creator voice).
 * Disclosure is always the **last** line of the block.
 * Orbit redirect URLs by default — never raw merchant IDs in templates.
 */
export function buildAffiliateDescriptionSection(args: {
  links: AffiliateDescriptionLink[];
  templates?: DescriptionTemplateMap;
  useRedirectUrls?: boolean;
  topicKey?: string | null;
  videoTopic?: string | null;
  videoTitle?: string | null;
  videoSlug?: string | null;
  headerVariant?: "primary" | "alternate";
}): string {
  if (!args.links.length) return "";
  const templates = {
    ...DEFAULT_AFFILIATE_TEMPLATES,
    ...args.templates,
  };
  const useRedirect = args.useRedirectUrls !== false;
  const topicKey =
    args.topicKey ??
    inferCreatorTopicKey({
      topic: args.videoTopic,
      title: args.videoTitle,
    });

  const header =
    args.headerVariant === "alternate"
      ? templates.section_header_alt || CREATOR_SECTION_HEADERS.alternate
      : templates.section_header || CREATOR_SECTION_HEADERS.primary;

  if (descriptionContainsCreatorBannedPhrase(header)) return "";

  const lines: string[] = [header, ""];

  for (const link of args.links) {
    const key = pickTemplateKey(link);
    const family = familyFromLink(link);
    const intro =
      family === "books" || family === "lego"
        ? resolveTopicTunedIntro({
            family,
            topicKey,
            templates,
          })
        : templates[key] ||
          resolveTopicTunedIntro({
            family:
              family === "binoculars"
                ? "binoculars"
                : family === "paper"
                  ? "paper"
                  : "general",
            topicKey,
            templates,
          });

    if (
      descriptionViolatesEditorialTone(intro).length ||
      descriptionContainsCreatorBannedPhrase(intro)
    ) {
      continue;
    }
    const url = useRedirect
      ? buildYouTubeDescriptionGoUrl({
          productSlug: link.productSlug,
          videoSlug: args.videoSlug,
        })
      : link.url;
    lines.push(intro);
    lines.push(url);
    lines.push("");
  }

  while (lines.length && lines[lines.length - 1] === "") lines.pop();

  const disclosure = templates.disclosure || CREATOR_AFFILIATE_DISCLOSURE;
  lines.push("");
  lines.push(disclosure);

  const section = lines.join("\n").trimEnd();
  if (descriptionContainsCreatorBannedPhrase(section)) return "";
  return section;
}

export type AppendAffiliateOptions = {
  description: string;
  links: AffiliateDescriptionLink[];
  templates?: DescriptionTemplateMap;
  useRedirectUrls?: boolean;
  includeAmazonDisclosure?: boolean;
  trustVideo?: EditorialTrustVideoInput;
  headerVariant?: "primary" | "alternate";
};

/**
 * Place affiliate block **after** chapters + subscribe, **before** playlist / hashtags.
 * Disclosure is the last line of the affiliate block (Creator).
 * Shorts → no block.
 */
export function appendAffiliateSectionToDescription(
  args: AppendAffiliateOptions,
): string {
  if (args.trustVideo?.isShort) {
    return args.description.trimEnd();
  }

  let links = args.links;

  if (args.trustVideo) {
    const withTrust = links.filter((l) => l.trustProduct);
    if (!withTrust.length) {
      return args.description.trimEnd();
    }
    const { accepted } = filterDescriptionLinksThroughTrustGate({
      video: args.trustVideo,
      candidates: withTrust.map((l) => ({
        product: l.trustProduct!,
        role:
          l.role === "companion"
            ? "companion"
            : l.role === "primary"
              ? "primary"
              : "secondary",
      })),
    });
    const ok = new Set(accepted.map((a) => a.product.id));
    links = withTrust.filter((l) => ok.has(l.trustProduct!.id));
  }

  const seen = new Set<string>();
  const uniqueLinks = links
    .filter((l) => {
      if (seen.has(l.productSlug)) return false;
      seen.add(l.productSlug);
      return true;
    })
    .slice(0, 2);

  if (!uniqueLinks.length) return args.description.trimEnd();

  const topicKey = args.trustVideo
    ? inferCreatorTopicKey(args.trustVideo)
    : null;

  const videoSlug = args.trustVideo?.slug ?? null;

  let section = buildAffiliateDescriptionSection({
    links: uniqueLinks,
    templates: args.templates,
    useRedirectUrls: args.useRedirectUrls,
    topicKey,
    videoTopic: args.trustVideo?.topic,
    videoTitle: args.trustVideo?.title,
    videoSlug,
    headerVariant: args.headerVariant,
  });
  if (!section || descriptionViolatesEditorialTone(section).length) {
    return args.description.trimEnd();
  }

  const templates = { ...DEFAULT_AFFILIATE_TEMPLATES, ...args.templates };

  if (
    args.includeAmazonDisclosure !== false &&
    needsAmazonDisclosure(uniqueLinks)
  ) {
    const amazon = templates.amazon_disclosure || DEFAULT_AMAZON_DISCLOSURE;
    if (!section.includes(amazon)) {
      section = `${section}\n${amazon}`;
    }
  }

  const body = stripLeadingDisclosure(args.description.trimEnd());
  const { description: withGo, foundAnyGo } = upgradeYouTubeDescriptionGoUrls({
    description: body,
    productSlugs: uniqueLinks.map((l) => l.productSlug),
    videoSlug,
  });

  // Existing /go/{slug} door: upgrade bare → stamped in place; never duplicate the block.
  if (foundAnyGo) {
    if (!descriptionAlreadyHasDisclosure(withGo)) {
      return insertAffiliateBlockAfterPrimaryCta(
        withGo,
        templates.disclosure || CREATOR_AFFILIATE_DISCLOSURE,
      );
    }
    return withGo.trimEnd();
  }

  return insertAffiliateBlockAfterPrimaryCta(withGo, section);
}

export function recommendationsToDescriptionLinks(
  recommendations: ScoredRecommendation[],
  opts?: {
    affiliateUrlBySlug?: Record<string, string>;
    programSlugByProductId?: Record<string, string>;
  },
): AffiliateDescriptionLink[] {
  return recommendations.map((r) => ({
    productName: r.product.name,
    productSlug: r.product.slug,
    category: r.product.category,
    programSlug:
      opts?.programSlugByProductId?.[r.product.id] || r.product.programSlug,
    url:
      opts?.affiliateUrlBySlug?.[r.product.slug] ||
      `https://example.invalid/go/${r.product.slug}`,
    role: r.role,
    trustProduct: r.product,
  }));
}

/**
 * True when the affiliate header/disclosure appears before chapters + subscribe
 * (i.e. still in the “first screen” / film pitch region).
 */
export function affiliateBlockAppearsInFirstScreen(description: string): boolean {
  const lower = description.toLowerCase();
  const aff = lower.search(
    /if you want to go further|orbit['’]s next steps \(not a shop\)|some of these links are affiliate/,
  );
  if (aff < 0) return false;

  const chapters = lower.search(/\nchapters\b|^chapters\b/);
  const subscribe = lower.search(/subscribe for|subscribe to/);
  const ctaMarkers = [chapters, subscribe].filter((i) => i >= 0);
  if (ctaMarkers.length) {
    const ctaEnd = Math.max(...ctaMarkers);
    return aff < ctaEnd;
  }

  // No chapters/subscribe markers — treat first ~screen of chars as first screen
  return aff < 420;
}

export { CREATOR_AFFILIATE_DISCLOSURE, CREATOR_SECTION_HEADERS };
