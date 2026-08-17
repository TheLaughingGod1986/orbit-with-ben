import { prisma } from "@/lib/storage/prisma";
import {
  appendAffiliateSectionToDescription,
  buildAffiliateDescriptionSection,
  DEFAULT_AFFILIATE_TEMPLATES,
  type AffiliateDescriptionLink,
  type DescriptionTemplateMap,
} from "./description";
import {
  getActiveDescriptionPlacements,
  toProductMatchInput,
  videoToMatchInput,
} from "./placements";
import { buildYouTubeDescriptionGoUrl } from "./urls";
import { filterDescriptionLinksThroughTrustGate } from "./editorial-trust-gate";

export async function loadDescriptionTemplates(): Promise<DescriptionTemplateMap> {
  const rows = await prisma.affiliateDescriptionTemplate.findMany({
    where: { active: true },
  });
  const map: DescriptionTemplateMap = { ...DEFAULT_AFFILIATE_TEMPLATES };
  for (const row of rows) {
    map[row.key] = row.body;
  }
  return map;
}

export async function buildDescriptionLinksFromVideo(
  videoId: string,
): Promise<AffiliateDescriptionLink[]> {
  const video = await prisma.longFormVideo.findUnique({ where: { id: videoId } });
  const placements = await getActiveDescriptionPlacements(videoId);

  const links = placements.map((p) => ({
    productName: p.affiliateProduct.name,
    productSlug: p.affiliateProduct.slug,
    category: p.affiliateProduct.category,
    programSlug: p.affiliateProduct.affiliateProgram.slug,
    url: buildYouTubeDescriptionGoUrl({
      productSlug: p.affiliateProduct.slug,
      videoSlug: video?.slug,
    }),
    role:
      p.placementType === "DESCRIPTION_PRIMARY"
        ? ("primary" as const)
        : ("secondary" as const),
    trustProduct: toProductMatchInput(p.affiliateProduct),
  }));

  if (!video) return links.slice(0, 2);

  const { accepted } = filterDescriptionLinksThroughTrustGate({
    video: videoToMatchInput(video),
    candidates: links.map((l) => ({
      product: l.trustProduct,
      role: l.role === "primary" ? "primary" : "secondary",
    })),
  });
  const ok = new Set(accepted.map((a) => a.product.id));
  return links.filter((l) => ok.has(l.trustProduct.id)).slice(0, 2);
}

/**
 * Extend a YouTube description with trust-gated approved affiliate links only.
 */
export async function generateYouTubeDescriptionWithAffiliates(args: {
  baseDescription: string;
  videoId: string;
  useRedirectUrls?: boolean;
}): Promise<string> {
  const video = await prisma.longFormVideo.findUnique({ where: { id: args.videoId } });
  const [links, templates] = await Promise.all([
    buildDescriptionLinksFromVideo(args.videoId),
    loadDescriptionTemplates(),
  ]);
  return appendAffiliateSectionToDescription({
    description: args.baseDescription,
    links,
    templates,
    useRedirectUrls: args.useRedirectUrls !== false,
    trustVideo: video ? videoToMatchInput(video) : undefined,
  });
}

export async function previewAffiliateDescriptionBlock(videoId: string): Promise<string> {
  const video = await prisma.longFormVideo.findUnique({
    where: { id: videoId },
    select: { slug: true, topic: true, title: true },
  });
  const [links, templates] = await Promise.all([
    buildDescriptionLinksFromVideo(videoId),
    loadDescriptionTemplates(),
  ]);
  return buildAffiliateDescriptionSection({
    links,
    templates,
    videoSlug: video?.slug,
    videoTopic: video?.topic,
    videoTitle: video?.title,
  });
}

export { appendAffiliateSectionToDescription, buildAffiliateDescriptionSection };
