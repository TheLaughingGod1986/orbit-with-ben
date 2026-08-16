import { prisma } from "@/lib/storage/prisma";
import {
  applyProgrammeAffiliateId,
  buildTrackedAffiliateUrl,
  resolveAffiliateRedirectBase,
} from "./urls";
import {
  normalizeAffiliateClickSource,
  type AffiliateClickSource,
} from "./social-channels";

export type RecordClickInput = {
  productSlug: string;
  videoId?: string | null;
  videoSlug?: string | null;
  placementId?: string | null;
  source?: string | null;
  medium?: string | null;
  campaign?: string | null;
  content?: string | null;
  userAgent?: string | null;
  referrer?: string | null;
};

/**
 * Resolve product, record click, return tracked destination URL.
 * `source` is normalised to youtube | threads | instagram | facebook | …
 */
export async function recordAffiliateClickAndResolve(input: RecordClickInput): Promise<{
  destinationUrl: string;
  clickId: string;
  productId: string;
  productName: string;
  source: AffiliateClickSource;
}> {
  const product = await prisma.affiliateProduct.findUnique({
    where: { slug: input.productSlug },
    include: { affiliateProgram: true },
  });
  if (!product || !product.active) {
    throw new Error("Affiliate product not found or inactive");
  }
  if (product.affiliateProgram.status !== "ACTIVE") {
    throw new Error("Affiliate programme is not active");
  }

  const source = normalizeAffiliateClickSource(input.source);

  let videoId = input.videoId ?? null;
  if (!videoId && input.videoSlug) {
    const video = await prisma.longFormVideo.findUnique({
      where: { slug: input.videoSlug },
      select: { id: true },
    });
    videoId = video?.id ?? null;
  }

  let campaign = input.campaign ?? null;
  if (!campaign && videoId) {
    const video = await prisma.longFormVideo.findUnique({
      where: { id: videoId },
      select: { slug: true },
    });
    campaign = video?.slug ?? null;
  }

  // Prefer destination when affiliateUrl is empty/placeholder — tag from env at redirect.
  const baseMerchantUrl = resolveAffiliateRedirectBase({
    destinationUrl: product.destinationUrl,
    affiliateUrl: product.affiliateUrl,
  });
  const withProgrammeId = applyProgrammeAffiliateId(
    baseMerchantUrl,
    product.affiliateProgram.slug,
  );
  const destinationUrl = buildTrackedAffiliateUrl({
    affiliateUrl: withProgrammeId,
    videoSlug: campaign,
    productSlug: product.slug,
    utmSource: source,
    utmMedium: input.medium ?? "affiliate",
    utmCampaign: campaign ?? undefined,
    utmContent: input.content ?? product.slug,
  });

  const click = await prisma.affiliateClick.create({
    data: {
      affiliateProductId: product.id,
      videoId,
      placementId: input.placementId ?? null,
      source,
      medium: input.medium ?? "affiliate",
      campaign,
      content: input.content ?? product.slug,
      destinationUrl,
      userAgent: input.userAgent ?? null,
      referrer: input.referrer ?? null,
    },
  });

  if (input.placementId) {
    await prisma.affiliatePlacement.update({
      where: { id: input.placementId },
      data: { clicks: { increment: 1 } },
    });
  } else if (videoId) {
    const placement = await prisma.affiliatePlacement.findFirst({
      where: {
        videoId,
        affiliateProductId: product.id,
        status: { in: ["APPROVED", "ACTIVE", "PENDING"] },
      },
    });
    if (placement) {
      await prisma.affiliatePlacement.update({
        where: { id: placement.id },
        data: { clicks: { increment: 1 } },
      });
    }
  }

  return {
    destinationUrl,
    clickId: click.id,
    productId: product.id,
    productName: product.name,
    source,
  };
}

export { normalizeAffiliateClickSource };
export type { AffiliateClickSource };
