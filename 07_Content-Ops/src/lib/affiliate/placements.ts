import { prisma } from "@/lib/storage/prisma";
import {
  dedupeRecommendations,
  recommendProductsForVideo,
} from "./matching";
import { loadActiveProductsForMatching, toProductMatchInput } from "./products";
import type { PlacementType, VideoMatchInput } from "./types";
import { placementActionSchema } from "./schemas";
import {
  MAX_AFFILIATE_CARD_CANDIDATES,
  evaluateEditorialTrustGate,
  type EditorialTrustProductInput,
  type EditorialTrustVideoInput,
} from "./editorial-trust-gate";

function videoToMatchInput(video: {
  id: string;
  title: string;
  workingTitle: string | null;
  slug: string;
  topic: string;
  category: string | null;
  summary: string | null;
  script: string | null;
  primaryKeyword: string | null;
  secondaryKeywords: string | null;
  youtubeVideoId?: string | null;
}): VideoMatchInput {
  return {
    id: video.id,
    title: video.title,
    workingTitle: video.workingTitle,
    slug: video.slug,
    topic: video.topic,
    category: video.category,
    summary: video.summary,
    script: video.script,
    primaryKeyword: video.primaryKeyword,
    secondaryKeywords: video.secondaryKeywords,
    youtubeVideoId: video.youtubeVideoId,
  };
}

function toTrustVideo(
  video: ReturnType<typeof videoToMatchInput>,
  opts?: { isShort?: boolean; isCompanionShort?: boolean },
): EditorialTrustVideoInput {
  return {
    ...video,
    isShort: opts?.isShort,
    isCompanionShort: opts?.isCompanionShort,
  };
}

/**
 * Matching may surface up to 4 candidates for the editor card.
 * Does not mean 4 links enter the description.
 */
export async function generateRecommendationsForVideo(videoId: string) {
  const video = await prisma.longFormVideo.findUnique({ where: { id: videoId } });
  if (!video) throw new Error("Video not found");
  const products = await loadActiveProductsForMatching();
  const matchInput = videoToMatchInput(video);
  const set = recommendProductsForVideo(matchInput, products);
  const recommendations = dedupeRecommendations(set.all).slice(
    0,
    MAX_AFFILIATE_CARD_CANDIDATES,
  );

  const trustVideo = toTrustVideo(matchInput);
  const gated = recommendations.map((r) => {
    const gate = evaluateEditorialTrustGate(trustVideo, r.product);
    return { ...r, trustGate: gate };
  });

  return {
    video: matchInput,
    recommendations: gated,
    /** Candidates that would pass auto-insert / approve right now */
    trustPassing: gated.filter((r) => r.trustGate.pass),
    set,
  };
}

function placementTypeForRole(
  role: "primary" | "secondary" | "evergreen",
  index: number,
): PlacementType {
  if (role === "primary" || index === 0) return "DESCRIPTION_PRIMARY";
  return "DESCRIPTION_SECONDARY";
}

/**
 * Regenerate placements for the editor card (up to 4 candidates as PENDING).
 * Auto-approve only when the editorial trust gate passes — never stack junk.
 */
export async function regeneratePlacementsForVideo(
  videoId: string,
  opts?: { replaceAll?: boolean; autoApprove?: boolean },
) {
  const { recommendations, video } = await generateRecommendationsForVideo(videoId);
  const trustVideo = toTrustVideo(video);

  if (opts?.replaceAll) {
    await prisma.affiliatePlacement.deleteMany({
      where: { videoId, generatedAutomatically: true },
    });
  } else {
    await prisma.affiliatePlacement.deleteMany({
      where: {
        videoId,
        generatedAutomatically: true,
        manuallyApproved: false,
        status: { in: ["PENDING", "REJECTED"] },
      },
    });
  }

  const created = [];
  for (const [i, rec] of recommendations.entries()) {
    const placementType = placementTypeForRole(rec.role, i);
    const existing = await prisma.affiliatePlacement.findUnique({
      where: {
        videoId_affiliateProductId_placementType: {
          videoId,
          affiliateProductId: rec.product.id,
          placementType,
        },
      },
    });
    if (existing && existing.status === "REJECTED" && !opts?.replaceAll) {
      continue;
    }
    if (existing && existing.manuallyApproved && !opts?.replaceAll) {
      created.push(existing);
      continue;
    }

    const gate = evaluateEditorialTrustGate(trustVideo, rec.product);
    const canAutoApprove = Boolean(opts?.autoApprove) && gate.pass;

    const row = await prisma.affiliatePlacement.upsert({
      where: {
        videoId_affiliateProductId_placementType: {
          videoId,
          affiliateProductId: rec.product.id,
          placementType,
        },
      },
      create: {
        videoId,
        affiliateProductId: rec.product.id,
        placementType,
        position: i,
        relevanceScore: rec.relevanceScore,
        generatedAutomatically: true,
        manuallyApproved: canAutoApprove,
        status: canAutoApprove ? "APPROVED" : "PENDING",
      },
      update: {
        position: i,
        relevanceScore: rec.relevanceScore,
        generatedAutomatically: true,
        status: canAutoApprove ? "APPROVED" : "PENDING",
        manuallyApproved: canAutoApprove ? true : undefined,
      },
      include: {
        affiliateProduct: {
          include: { affiliateProgram: true, tags: { include: { tag: true } } },
        },
      },
    });
    created.push({ ...row, trustGate: gate });
  }

  return { recommendations, placements: created };
}

export class EditorialTrustGateError extends Error {
  failures: string[];
  constructor(message: string, failures: string[]) {
    super(message);
    this.name = "EditorialTrustGateError";
    this.failures = failures;
  }
}

async function loadTrustContext(videoId: string, productId: string) {
  const video = await prisma.longFormVideo.findUnique({ where: { id: videoId } });
  if (!video) throw new Error("Video not found");
  const productRow = await prisma.affiliateProduct.findUnique({
    where: { id: productId },
    include: {
      affiliateProgram: true,
      tags: { include: { tag: true } },
    },
  });
  if (!productRow) throw new Error("Product not found");
  return {
    trustVideo: toTrustVideo(videoToMatchInput(video)),
    product: toProductMatchInput(productRow) as EditorialTrustProductInput,
  };
}

export async function upsertPlacement(raw: unknown) {
  const input = placementActionSchema.parse(raw);
  const targetStatus = input.status ?? "APPROVED";

  if (targetStatus === "APPROVED" || targetStatus === "ACTIVE") {
    const { trustVideo, product } = await loadTrustContext(
      input.videoId,
      input.affiliateProductId,
    );
    const gate = evaluateEditorialTrustGate(trustVideo, product);
    if (!gate.pass) {
      throw new EditorialTrustGateError(
        `Editorial trust gate rejected approval: ${gate.reasons.join("; ")}`,
        gate.failures,
      );
    }

    // Description placements: enforce max 2 approved on the film
    if (
      input.placementType === "DESCRIPTION_PRIMARY" ||
      input.placementType === "DESCRIPTION_SECONDARY"
    ) {
      const approved = await prisma.affiliatePlacement.count({
        where: {
          videoId: input.videoId,
          status: { in: ["APPROVED", "ACTIVE"] },
          placementType: {
            in: ["DESCRIPTION_PRIMARY", "DESCRIPTION_SECONDARY"],
          },
          NOT: {
            affiliateProductId: input.affiliateProductId,
            placementType: input.placementType,
          },
        },
      });
      if (approved >= 2) {
        throw new EditorialTrustGateError(
          "Editorial trust gate: more than 2 affiliate links on a film is rejected",
          ["TOO_MANY_LINKS"],
        );
      }
    }

    // Shorts description type: always reject approve
    if (input.placementType === "SHORT_DESCRIPTION") {
      throw new EditorialTrustGateError(
        "Editorial trust gate: Shorts get zero affiliate links",
        ["SHORTS_ZERO_AFFILIATE"],
      );
    }
  }

  return prisma.affiliatePlacement.upsert({
    where: {
      videoId_affiliateProductId_placementType: {
        videoId: input.videoId,
        affiliateProductId: input.affiliateProductId,
        placementType: input.placementType,
      },
    },
    create: {
      videoId: input.videoId,
      affiliateProductId: input.affiliateProductId,
      placementType: input.placementType,
      position: input.position ?? 0,
      relevanceScore: input.relevanceScore ?? null,
      manuallyApproved: input.manuallyApproved ?? true,
      generatedAutomatically: input.generatedAutomatically ?? false,
      status: targetStatus,
    },
    update: {
      position: input.position,
      relevanceScore: input.relevanceScore,
      manuallyApproved: input.manuallyApproved,
      status: input.status,
    },
    include: {
      affiliateProduct: { include: { affiliateProgram: true } },
    },
  });
}

export async function setPlacementStatus(
  placementId: string,
  status: "APPROVED" | "REJECTED" | "ACTIVE" | "REMOVED" | "PENDING",
) {
  if (status === "APPROVED" || status === "ACTIVE") {
    const existing = await prisma.affiliatePlacement.findUnique({
      where: { id: placementId },
      include: {
        video: true,
        affiliateProduct: {
          include: {
            affiliateProgram: true,
            tags: { include: { tag: true } },
          },
        },
      },
    });
    if (!existing) throw new Error("Placement not found");

    if (existing.placementType === "SHORT_DESCRIPTION") {
      throw new EditorialTrustGateError(
        "Editorial trust gate: Shorts get zero affiliate links",
        ["SHORTS_ZERO_AFFILIATE"],
      );
    }

    const trustVideo = toTrustVideo(videoToMatchInput(existing.video));
    const product = toProductMatchInput(existing.affiliateProduct);
    const gate = evaluateEditorialTrustGate(trustVideo, product);
    if (!gate.pass) {
      throw new EditorialTrustGateError(
        `Editorial trust gate rejected approval: ${gate.reasons.join("; ")}`,
        gate.failures,
      );
    }

    if (
      existing.placementType === "DESCRIPTION_PRIMARY" ||
      existing.placementType === "DESCRIPTION_SECONDARY"
    ) {
      const approved = await prisma.affiliatePlacement.count({
        where: {
          videoId: existing.videoId,
          status: { in: ["APPROVED", "ACTIVE"] },
          placementType: {
            in: ["DESCRIPTION_PRIMARY", "DESCRIPTION_SECONDARY"],
          },
          id: { not: placementId },
        },
      });
      if (approved >= 2) {
        throw new EditorialTrustGateError(
          "Editorial trust gate: more than 2 affiliate links on a film is rejected",
          ["TOO_MANY_LINKS"],
        );
      }
    }
  }

  return prisma.affiliatePlacement.update({
    where: { id: placementId },
    data: {
      status,
      manuallyApproved: status === "APPROVED" || status === "ACTIVE",
    },
  });
}

export async function removePlacement(placementId: string) {
  return prisma.affiliatePlacement.update({
    where: { id: placementId },
    data: { status: "REMOVED" },
  });
}

export async function listPlacementsForVideo(videoId: string) {
  return prisma.affiliatePlacement.findMany({
    where: { videoId, status: { not: "REMOVED" } },
    include: {
      affiliateProduct: {
        include: { affiliateProgram: true, tags: { include: { tag: true } } },
      },
    },
    orderBy: [{ position: "asc" }, { createdAt: "asc" }],
  });
}

/**
 * Description insertion uses only APPROVED/ACTIVE placements that still pass the trust gate.
 * PENDING candidates stay on the editor card only.
 */
export async function getActiveDescriptionPlacements(videoId: string) {
  const video = await prisma.longFormVideo.findUnique({ where: { id: videoId } });
  if (!video) return [];

  const placements = await prisma.affiliatePlacement.findMany({
    where: {
      videoId,
      status: { in: ["APPROVED", "ACTIVE"] },
      placementType: { in: ["DESCRIPTION_PRIMARY", "DESCRIPTION_SECONDARY"] },
    },
    include: {
      affiliateProduct: {
        include: { affiliateProgram: true, tags: { include: { tag: true } } },
      },
    },
    orderBy: [{ position: "asc" }, { createdAt: "asc" }],
  });

  const trustVideo = toTrustVideo(videoToMatchInput(video));
  return placements.filter((p) => {
    const gate = evaluateEditorialTrustGate(
      trustVideo,
      toProductMatchInput(p.affiliateProduct),
    );
    return gate.pass;
  });
}

export { videoToMatchInput, toProductMatchInput, toTrustVideo };
