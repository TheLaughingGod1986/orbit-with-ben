import { prisma } from "@/lib/storage/prisma";
import { resolveAffiliateSocialContextForVideo } from "./social-context";
import {
  generateAffiliateSocialSnippets,
  type AffiliateSocialSnippet,
} from "./social-snippets";
import { assertAffiliateSafeSocialCopy } from "./social-copy";

/**
 * Build live-channel social snippets for a long-form video from its
 * strongest approved placement. Editor must approve before publish.
 */
export async function getAffiliateSocialSnippetsForVideo(
  videoId: string,
): Promise<{
  snippets: AffiliateSocialSnippet[];
  videoSlug: string;
  placementApproved: boolean;
} | null> {
  const video = await prisma.longFormVideo.findUnique({ where: { id: videoId } });
  if (!video) return null;

  const affiliate = await resolveAffiliateSocialContextForVideo({
    videoId,
    clipHook: video.summary,
    clipTitle: video.title,
    clipTranscript: video.script,
  });

  if (!affiliate) {
    return {
      snippets: [],
      videoSlug: video.slug,
      placementApproved: false,
    };
  }

  const snippets = generateAffiliateSocialSnippets({
    videoSlug: video.slug,
    videoTitle: video.title,
    topic: video.topic,
    hook: video.summary,
    youtubeUrl: video.youtubeUrl,
    productLabel: affiliate.productLabel,
    productSlug: affiliate.productSlug,
    hasNaturalObject: affiliate.hasNaturalObject,
    productRelevantToVideo: affiliate.productRelevantToVideo,
    hasApprovedPlacement: affiliate.hasApprovedPlacement,
    platformsMentionedThisWeek: affiliate.platformsMentionedThisWeek,
    preferYouTubePointer: true,
  });

  for (const s of snippets) {
    assertAffiliateSafeSocialCopy(s.caption);
  }

  return {
    snippets,
    videoSlug: video.slug,
    placementApproved: affiliate.hasApprovedPlacement,
  };
}

/**
 * Push approved snippets into PlatformPost drafts for the publishing pipeline.
 * Never sets approvedForPublish / ready without explicit editor intent —
 * creates/updates as draft only.
 */
export async function enqueueAffiliateSocialSnippetsAsDrafts(args: {
  videoId: string;
  clipId: string;
  platforms?: string[];
}): Promise<{ upserted: number }> {
  const pack = await getAffiliateSocialSnippetsForVideo(args.videoId);
  if (!pack?.placementApproved) {
    throw new Error("Approve an affiliate description placement before social drafts");
  }

  const wanted = new Set(
    args.platforms || pack.snippets.map((s) => s.platform),
  );
  let upserted = 0;

  for (const snippet of pack.snippets) {
    if (!wanted.has(snippet.platform)) continue;
    assertAffiliateSafeSocialCopy(snippet.caption);

    const existing = await prisma.platformPost.findFirst({
      where: { shortClipId: args.clipId, platform: snippet.platform },
    });

    const data = {
      caption: snippet.caption,
      title: null as string | null,
      callToAction: null as string | null,
      uploadStatus: "draft" as const,
      approvedForPublish: false,
      publishingMethod: "manual",
      notes: [
        "Affiliate social snippet — draft only until editor approves publish.",
        ...snippet.notes,
      ].join(" · "),
    };

    if (existing) {
      await prisma.platformPost.update({ where: { id: existing.id }, data });
    } else {
      await prisma.platformPost.create({
        data: {
          shortClipId: args.clipId,
          platform: snippet.platform,
          ...data,
        },
      });
    }
    upserted += 1;
  }

  return { upserted };
}
