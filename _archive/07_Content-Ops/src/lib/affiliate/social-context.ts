import { prisma } from "@/lib/storage/prisma";
import { startOfWeek, endOfWeek } from "date-fns";
import type { PlatformId } from "@/config/platforms";
import type { AffiliateSocialContext } from "./social-copy";
import { scoreAffiliateRelevance } from "./matching";
import { toProductMatchInput } from "./products";
import { videoToMatchInput } from "./placements";

/**
 * Build affiliate social context from a long-form video's approved placements.
 * Returns null when there is nothing editorial to soft-mention.
 */
export async function resolveAffiliateSocialContextForVideo(args: {
  videoId: string;
  clipHook?: string | null;
  clipTitle?: string | null;
  clipTranscript?: string | null;
}): Promise<AffiliateSocialContext | null> {
  const video = await prisma.longFormVideo.findUnique({
    where: { id: args.videoId },
    include: {
      affiliatePlacements: {
        where: {
          status: { in: ["APPROVED", "ACTIVE"] },
          placementType: {
            in: ["DESCRIPTION_PRIMARY", "DESCRIPTION_SECONDARY", "SHORT_DESCRIPTION"],
          },
        },
        include: {
          affiliateProduct: {
            include: {
              affiliateProgram: true,
              tags: { include: { tag: true } },
            },
          },
        },
        orderBy: [{ position: "asc" }, { relevanceScore: "desc" }],
      },
    },
  });
  if (!video || video.affiliatePlacements.length === 0) return null;

  // One soft mention max — use the strongest primary placement only (never stack brands)
  const primary =
    video.affiliatePlacements.find((p) => p.placementType === "DESCRIPTION_PRIMARY") ||
    video.affiliatePlacements[0];
  const product = toProductMatchInput(primary.affiliateProduct);
  const match = scoreAffiliateRelevance(
    videoToMatchInput({
      ...video,
      // Blend clip text so “natural object” reflects the short, not only the long
      summary: [video.summary, args.clipHook, args.clipTitle, args.clipTranscript]
        .filter(Boolean)
        .join("\n"),
    }),
    product,
  );

  const clipCorpus = [args.clipHook, args.clipTitle, args.clipTranscript, video.topic, video.title]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
  const naturalTokens = product.tagSlugs.concat(
    product.category.split(/\s+/).map((s) => s.toLowerCase()),
    product.name.toLowerCase().split(/\s+/),
  );
  const hasNaturalObject = naturalTokens.some(
    (t) => t.length >= 4 && clipCorpus.includes(t.replace(/-/g, " ")),
  );

  const platformsMentionedThisWeek = await platformsWithAffiliateMentionThisWeek();

  return {
    productLabel: product.name,
    productSlug: product.slug,
    brandNames: [primary.affiliateProduct.affiliateProgram.name, product.name],
    hasNaturalObject,
    productRelevantToVideo: match.score >= 15,
    hasApprovedPlacement: true,
    youtubeUrl: video.youtubeUrl,
    longTitle: video.title,
    platformsMentionedThisWeek,
    includeQuietDisclosure: false,
    preferGoLink: false,
  };
}

/**
 * Heuristic: platforms that already have a SHORT_DESCRIPTION / caption placement
 * updated this week count as “already mentioned”.
 */
async function platformsWithAffiliateMentionThisWeek(): Promise<PlatformId[]> {
  const now = new Date();
  const weekStart = startOfWeek(now, { weekStartsOn: 1 });
  const weekEnd = endOfWeek(now, { weekStartsOn: 1 });

  const rows = await prisma.affiliatePlacement.findMany({
    where: {
      placementType: "SHORT_DESCRIPTION",
      status: { in: ["APPROVED", "ACTIVE"] },
      updatedAt: { gte: weekStart, lte: weekEnd },
    },
    select: { id: true },
  });

  // We don't store platform on placement yet — approximate via posts updated this week
  // that reference affiliate soft-mention notes in caption. Keep conservative:
  // if any SHORT_DESCRIPTION placement was touched this week, treat all short platforms
  // as already-used unless caller overrides. Prefer empty when none.
  if (!rows.length) return [];

  // Conservative weekly budget: one soft mention across Shorts-like platforms per week
  // when a short-description placement was already written.
  return ["youtube_shorts", "tiktok", "instagram_reels"] as PlatformId[];
}
