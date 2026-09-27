import type { OpportunityScoreBreakdown, ProductMatchInput, VideoMatchInput } from "./types";
import { recommendProductsForVideo } from "./matching";

function clamp(n: number, min = 0, max = 100): number {
  return Math.max(min, Math.min(max, Math.round(n)));
}

/**
 * Affiliate Opportunity Score 0–100.
 * Example: “Best Telescope for Beginners” ≈ 98; speculative science ≈ 45.
 */
export function scoreAffiliateOpportunity(
  video: VideoMatchInput,
  products: ProductMatchInput[],
  opts?: { views?: number | null },
): OpportunityScoreBreakdown {
  const recs = recommendProductsForVideo(video, products, { minScore: 10 });
  const topScore = recs.all[0]?.relevanceScore ?? 0;
  const suitableCount = recs.all.length;
  const partners = new Set(
    products.filter((p) => p.active).map((p) => p.programSlug || "unknown"),
  ).size;

  const title = `${video.title} ${video.workingTitle || ""} ${video.primaryKeyword || ""}`.toLowerCase();

  // Search / commercial intent signals
  let searchIntent = 25;
  if (/best |review|vs\.? |compared|recommend|buy|for beginners|setup|gear|kit/.test(title)) {
    searchIntent = 95;
  } else if (/how to|guide|explained|what is/.test(title)) {
    searchIntent = 70;
  } else if (/what would happen|could humans|survive|what if/.test(title)) {
    searchIntent = 40;
  }

  const commercialRelevance = clamp(
    suitableCount === 0 ? 10 : 30 + topScore * 0.8 + (suitableCount >= 3 ? 15 : suitableCount * 5),
  );

  const topicRelevance = clamp(20 + topScore * 0.9);

  const avgPrice =
    products.filter((p) => p.active && p.price != null).reduce((s, p) => s + (p.price || 0), 0) /
    Math.max(1, products.filter((p) => p.active && p.price != null).length);
  const likelyPrice = clamp(
    !avgPrice ? 40 : avgPrice >= 200 ? 85 : avgPrice >= 50 ? 70 : avgPrice >= 15 ? 55 : 35,
  );

  const partnerCoverage = clamp(partners === 0 ? 5 : partners * 22);

  const views = opts?.views ?? 0;
  const viewPotential = clamp(
    views <= 0 ? 40 : views >= 100_000 ? 90 : views >= 10_000 ? 70 : views >= 1_000 ? 55 : 35,
  );

  const evergreenHits = products.filter((p) => p.active && p.evergreen).length;
  const evergreenPotential = clamp(
    /telescope|beginner|astronomy|book|binocular|gear/.test(title)
      ? 90
      : evergreenHits >= 2
        ? 70
        : 45,
  );

  // Weighted blend → 0–100
  const total = clamp(
    commercialRelevance * 0.22 +
      searchIntent * 0.2 +
      topicRelevance * 0.18 +
      likelyPrice * 0.1 +
      partnerCoverage * 0.1 +
      viewPotential * 0.1 +
      evergreenPotential * 0.1,
  );

  return {
    commercialRelevance,
    searchIntent,
    topicRelevance,
    likelyPrice,
    partnerCoverage,
    viewPotential,
    evergreenPotential,
    total,
  };
}
