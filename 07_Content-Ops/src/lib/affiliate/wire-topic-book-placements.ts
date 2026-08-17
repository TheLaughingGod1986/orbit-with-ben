/**
 * Additive wire: one APPROVED DESCRIPTION_PRIMARY topic book per long-form film.
 * Does not reset the DB. Does not publish to YouTube.com.
 * Shorts get zero affiliate links. Telescope / Brilliant / LEGO stay unplaced.
 */

import { prisma } from "@/lib/storage/prisma";
import { londonDateTime } from "@/lib/publishing/schedule";
import {
  FILM_TOPIC_BOOK_WIRES,
  TOPIC_BOOK_DESCRIPTION_BLOCKLIST_SLUGS,
  isWiredTopicBookForVideo,
  resolveTopicBookWireForVideo,
  verifiedFilmTopicBookWires,
  youtubeIdsForWire,
  type FilmTopicBookWire,
} from "./film-topic-book-map";
import { liveUrlForSlug } from "./live-product-urls";
import { applyLiveProductUrls } from "./apply-live-urls";
import { buildYouTubeDescriptionGoUrl } from "./urls";
import {
  appendAffiliateSectionToDescription,
  buildAffiliateDescriptionSection,
} from "./description";
import { loadDescriptionTemplates } from "./description-service";
import { inferCreatorTopicKey } from "./topic-product-map";

export type WireTopicBookResult = {
  appliedLiveUrls: Awaited<ReturnType<typeof applyLiveProductUrls>>;
  wired: Array<{
    filmKey: string;
    videoId: string;
    youtubeVideoId: string | null;
    title: string;
    productSlug: string;
    placementId: string;
    goPath: string;
    amazonUrl: string;
    descriptionPreview: string;
    createdVideo: boolean;
  }>;
  skipped: Array<{ filmKey: string; reason: string }>;
  clearedBlocklistPlacements: number;
};

function youtubeUrlFor(id: string | null): string | null {
  return id ? `https://www.youtube.com/watch?v=${id}` : null;
}

async function findExistingVideo(wire: FilmTopicBookWire) {
  const ids = youtubeIdsForWire(wire);
  if (ids.length) {
    const byId = await prisma.longFormVideo.findFirst({
      where: { youtubeVideoId: { in: ids } },
    });
    if (byId) return byId;
  }

  const bySlug = await prisma.longFormVideo.findUnique({
    where: { slug: wire.slug },
  });
  if (bySlug) return bySlug;

  const all = await prisma.longFormVideo.findMany({
    select: {
      id: true,
      title: true,
      workingTitle: true,
      slug: true,
      youtubeVideoId: true,
      topic: true,
      category: true,
      summary: true,
      script: true,
      primaryKeyword: true,
      secondaryKeywords: true,
      status: true,
      youtubeUrl: true,
      projectFolder: true,
      publicationDate: true,
    },
  });
  return (
    all.find((v) => resolveTopicBookWireForVideo(v)?.key === wire.key) || null
  );
}

async function upsertFilmVideo(wire: FilmTopicBookWire): Promise<{
  video: { id: string; title: string; youtubeVideoId: string | null; slug: string };
  createdVideo: boolean;
}> {
  const existing = await findExistingVideo(wire);
  const publicationDate = wire.scheduledDate
    ? londonDateTime(wire.scheduledDate, "19:00")
    : existing?.publicationDate || undefined;

  if (existing) {
    const updated = await prisma.longFormVideo.update({
      where: { id: existing.id },
      data: {
        title: existing.title || wire.title,
        workingTitle: existing.workingTitle || wire.workingTitle || wire.title,
        topic: existing.topic || wire.topic,
        category: existing.category || wire.category,
        primaryKeyword: existing.primaryKeyword || wire.primaryKeyword,
        secondaryKeywords:
          existing.secondaryKeywords || JSON.stringify(wire.secondaryKeywords),
        summary: existing.summary || wire.summary,
        youtubeVideoId: existing.youtubeVideoId || wire.youtubeVideoId,
        youtubeUrl:
          existing.youtubeUrl || youtubeUrlFor(wire.youtubeVideoId),
        projectFolder: existing.projectFolder || wire.projectFolder || null,
        status: existing.status === "published" ? "published" : wire.status,
        ...(publicationDate && !existing.publicationDate
          ? { publicationDate }
          : {}),
      },
    });
    return {
      video: {
        id: updated.id,
        title: updated.title,
        youtubeVideoId: updated.youtubeVideoId,
        slug: updated.slug,
      },
      createdVideo: false,
    };
  }

  const created = await prisma.longFormVideo.create({
    data: {
      title: wire.title,
      workingTitle: wire.workingTitle || wire.title,
      slug: wire.slug,
      topic: wire.topic,
      category: wire.category,
      status: wire.status,
      summary: wire.summary,
      script: `${wire.title}\n\n${wire.summary}\n\nDesk book for this film: topic wire ${wire.productSlug}.`,
      youtubeUrl: youtubeUrlFor(wire.youtubeVideoId),
      youtubeVideoId: wire.youtubeVideoId,
      projectFolder: wire.projectFolder || null,
      primaryKeyword: wire.primaryKeyword,
      secondaryKeywords: JSON.stringify(wire.secondaryKeywords),
      publicationDate: publicationDate || null,
      durationSeconds: null,
    },
  });
  return {
    video: {
      id: created.id,
      title: created.title,
      youtubeVideoId: created.youtubeVideoId,
      slug: created.slug,
    },
    createdVideo: true,
  };
}

async function clearCompetingDescriptionPlacements(
  videoId: string,
  keepProductId: string,
): Promise<number> {
  const competing = await prisma.affiliatePlacement.findMany({
    where: {
      videoId,
      placementType: { in: ["DESCRIPTION_PRIMARY", "DESCRIPTION_SECONDARY"] },
      NOT: { affiliateProductId: keepProductId },
    },
    include: { affiliateProduct: { select: { slug: true } } },
  });

  let cleared = 0;
  for (const row of competing) {
    const slug = row.affiliateProduct.slug;
    const isBlocklist = (
      TOPIC_BOOK_DESCRIPTION_BLOCKLIST_SLUGS as readonly string[]
    ).includes(slug);
    const isOtherDescription = true;
    // Always remove other description placements on this film — one book only.
    if (isBlocklist || isOtherDescription) {
      await prisma.affiliatePlacement.update({
        where: { id: row.id },
        data: { status: "REMOVED", manuallyApproved: false },
      });
      cleared += 1;
    }
  }

  // Never leave SHORT_DESCRIPTION affiliate placements
  const shortRows = await prisma.affiliatePlacement.updateMany({
    where: {
      videoId,
      placementType: "SHORT_DESCRIPTION",
      status: { in: ["PENDING", "APPROVED", "ACTIVE"] },
    },
    data: { status: "REMOVED", manuallyApproved: false },
  });
  cleared += shortRows.count;

  return cleared;
}

async function approvePrimaryBookPlacement(args: {
  videoId: string;
  productId: string;
  productSlug: string;
}) {
  // Editorial assertion: this is the desk book for the wired film.
  // Trust gate recognises film-topic-book-map (namedInVideo via isWiredTopicBookForVideo).
  return prisma.affiliatePlacement.upsert({
    where: {
      videoId_affiliateProductId_placementType: {
        videoId: args.videoId,
        affiliateProductId: args.productId,
        placementType: "DESCRIPTION_PRIMARY",
      },
    },
    create: {
      videoId: args.videoId,
      affiliateProductId: args.productId,
      placementType: "DESCRIPTION_PRIMARY",
      position: 0,
      relevanceScore: 100,
      generatedAutomatically: false,
      manuallyApproved: true,
      status: "APPROVED",
    },
    update: {
      position: 0,
      relevanceScore: 100,
      manuallyApproved: true,
      status: "APPROVED",
      generatedAutomatically: false,
    },
  });
}

function sampleBaseDescription(title: string): string {
  return [
    title,
    "",
    "Orbit walks through the pictures and the evidence.",
    "",
    "Chapters",
    "0:00 Cold open",
    "1:00 The question",
    "",
    "Subscribe for the next film.",
    "",
    "Playlist",
    "More Orbit documentaries",
    "",
    "#OrbitWithBen",
  ].join("\n");
}

/**
 * Apply live Amazon URLs (additive) then wire one approved book placement per film.
 */
export async function wireTopicBookPlacements(opts?: {
  dryRun?: boolean;
  skipApplyLiveUrls?: boolean;
}): Promise<WireTopicBookResult> {
  const appliedLiveUrls = opts?.skipApplyLiveUrls
    ? { updated: [], created: [], skipped: [], missing: [] }
    : await applyLiveProductUrls({ dryRun: opts?.dryRun });

  const wired: WireTopicBookResult["wired"] = [];
  const skipped: WireTopicBookResult["skipped"] = [];
  let clearedBlocklistPlacements = 0;

  const wires = verifiedFilmTopicBookWires();
  const templates = opts?.dryRun ? undefined : await loadDescriptionTemplates();

  for (const wire of FILM_TOPIC_BOOK_WIRES) {
    if (!wires.some((w) => w.key === wire.key)) {
      skipped.push({
        filmKey: wire.key,
        reason: `No verified amazon.co.uk live URL for ${wire.productSlug}`,
      });
      continue;
    }

    const live = liveUrlForSlug(wire.productSlug)!;
    const product = await prisma.affiliateProduct.findUnique({
      where: { slug: wire.productSlug },
      include: { affiliateProgram: true },
    });
    if (!product || !product.active) {
      skipped.push({
        filmKey: wire.key,
        reason: `Product ${wire.productSlug} missing or inactive — run affiliate:apply-urls`,
      });
      continue;
    }

    if (opts?.dryRun) {
      wired.push({
        filmKey: wire.key,
        videoId: "(dry-run)",
        youtubeVideoId: wire.youtubeVideoId,
        title: wire.title,
        productSlug: wire.productSlug,
        placementId: "(dry-run)",
        goPath: `/go/${wire.productSlug}`,
        amazonUrl: live.destinationUrl,
        descriptionPreview: "",
        createdVideo: false,
      });
      continue;
    }

    const { video, createdVideo } = await upsertFilmVideo(wire);
    clearedBlocklistPlacements += await clearCompetingDescriptionPlacements(
      video.id,
      product.id,
    );

    // Sanity: wire recognition for trust / Social Media Manager
    if (
      !isWiredTopicBookForVideo(
        {
          youtubeVideoId: video.youtubeVideoId,
          title: video.title,
          slug: video.slug,
        },
        wire.productSlug,
      )
    ) {
      skipped.push({
        filmKey: wire.key,
        reason: "Film↔book map did not resolve after upsert",
      });
      continue;
    }

    const placement = await approvePrimaryBookPlacement({
      videoId: video.id,
      productId: product.id,
      productSlug: product.slug,
    });

    const topicKey = inferCreatorTopicKey({
      title: wire.title,
      topic: wire.topic,
      primaryKeyword: wire.primaryKeyword,
      summary: wire.summary,
    });
    const links = [
      {
        productName: product.name,
        productSlug: product.slug,
        category: product.category,
        programSlug: product.affiliateProgram.slug,
        url: buildYouTubeDescriptionGoUrl({
          productSlug: product.slug,
          videoSlug: video.slug,
        }),
        role: "primary" as const,
        trustProduct: {
          id: product.id,
          name: product.name,
          slug: product.slug,
          description: product.description,
          category: product.category,
          active: product.active,
          featured: product.featured,
          priority: product.priority,
          evergreen: product.evergreen,
          tagSlugs: [],
          programSlug: product.affiliateProgram.slug,
          programStatus: product.affiliateProgram.status,
        },
      },
    ];
    const block = buildAffiliateDescriptionSection({
      links,
      templates: templates || undefined,
      topicKey,
      videoSlug: video.slug,
    });
    const descriptionPreview = appendAffiliateSectionToDescription({
      description: sampleBaseDescription(wire.title),
      links,
      templates: templates || undefined,
      trustVideo: {
        title: wire.title,
        topic: wire.topic,
        primaryKeyword: wire.primaryKeyword,
        summary: wire.summary,
        youtubeVideoId: wire.youtubeVideoId,
        slug: video.slug,
      },
    });

    // Ensure Creator voice constraints on the preview
    if (!block.includes(`/go/${product.slug}`)) {
      skipped.push({
        filmKey: wire.key,
        reason: "Description block missing /go link",
      });
      continue;
    }

    wired.push({
      filmKey: wire.key,
      videoId: video.id,
      youtubeVideoId: video.youtubeVideoId,
      title: video.title,
      productSlug: product.slug,
      placementId: placement.id,
      goPath: `/go/${product.slug}`,
      amazonUrl: live.destinationUrl,
      descriptionPreview,
      createdVideo,
    });
  }

  return {
    appliedLiveUrls,
    wired,
    skipped,
    clearedBlocklistPlacements,
  };
}

export { FILM_TOPIC_BOOK_WIRES, verifiedFilmTopicBookWires };
