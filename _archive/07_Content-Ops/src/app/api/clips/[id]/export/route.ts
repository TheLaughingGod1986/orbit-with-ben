import { NextResponse } from "next/server";
import path from "path";
import { prisma } from "@/lib/storage/prisma";
import { exportCaptions } from "@/lib/content/captions";
import { createExportPackage, slugify } from "@/lib/content/export-package";
import { generatePlatformCopy } from "@/lib/platforms/generate-platform-copy";
import { parseTimestampToSeconds } from "@/lib/validation/schemas";
import { PlatformId } from "@/config/platforms";
import { resolveAffiliateSocialContextForVideo } from "@/lib/affiliate/social-context";
import { applyAffiliateSocialConstraints } from "@/lib/affiliate/social-copy";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export async function POST(
  _req: Request,
  ctx: { params: Promise<{ id: string }> },
) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const { id } = await ctx.params;
  const clip = await prisma.shortClip.findUnique({
    where: { id },
    include: { longFormVideo: true, posts: true },
  });
  if (!clip) return NextResponse.json({ error: "Clip not found" }, { status: 404 });
  if (["proposed", "rejected"].includes(clip.status)) {
    return NextResponse.json(
      { error: "Approve the clip before exporting" },
      { status: 400 },
    );
  }
  if (!clip.transcript?.trim()) {
    return NextResponse.json({ error: "Missing transcript" }, { status: 400 });
  }

  let startSeconds = 0;
  let endSeconds: number | undefined;
  try {
    if (clip.sourceStartTime) startSeconds = parseTimestampToSeconds(clip.sourceStartTime);
    if (clip.sourceEndTime) endSeconds = parseTimestampToSeconds(clip.sourceEndTime);
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Invalid timestamps" },
      { status: 400 },
    );
  }

  const captions = exportCaptions({
    transcript: clip.transcript,
    startSeconds: 0,
    endSeconds:
      endSeconds && endSeconds > startSeconds
        ? endSeconds - startSeconds
        : clip.targetDurationSeconds || undefined,
  });

  const affiliate = await resolveAffiliateSocialContextForVideo({
    videoId: clip.longFormVideoId,
    clipHook: clip.hook,
    clipTitle: clip.workingTitle,
    clipTranscript: clip.transcript,
  });

  const rawCopies =
    clip.posts.length > 0
      ? clip.posts.map((p) => ({
          platform: p.platform as PlatformId,
          title: p.title || undefined,
          caption: p.caption || "",
          hashtags: p.hashtags ? (JSON.parse(p.hashtags) as string[]) : [],
          callToAction: p.callToAction || "",
          pinnedComment: p.pinnedComment || undefined,
          coverText: p.coverText || undefined,
          storyCaption: p.storyCaption || undefined,
          commentPrompt: p.commentPrompt || undefined,
          notes: [] as string[],
        }))
      : generatePlatformCopy({
          shortTitle: clip.workingTitle,
          hook: clip.hook || clip.workingTitle,
          topic: clip.longFormVideo.topic,
          transcript: clip.transcript,
          youtubeUrl: clip.longFormVideo.youtubeUrl,
          longTitle: clip.longFormVideo.title,
          callToAction: clip.callToAction,
          affiliate,
        });

  // Always sanitize stored/generated social copy beside affiliate placements
  const copies = applyAffiliateSocialConstraints(rawCopies, affiliate).copies;

  const exportRoot = path.join(process.cwd(), "content", "exports");
  const scheduledDates: Partial<Record<PlatformId, string>> = {};
  const publishingStatus: Partial<Record<PlatformId, string>> = {};
  for (const p of clip.posts) {
    const platform = p.platform as PlatformId;
    if (p.scheduledAt) scheduledDates[platform] = p.scheduledAt.toISOString();
    publishingStatus[platform] = p.uploadStatus;
  }

  const { dir, manifest } = await createExportPackage({
    exportRoot,
    slug: clip.longFormVideo.slug,
    clipId: clip.id,
    clipNumber: clip.clipNumber,
    clipSlug: slugify(clip.workingTitle),
    sourceVideoTitle: clip.longFormVideo.title,
    sourceVideoPath: clip.longFormVideo.finalVideoPath,
    sourceStartTime: clip.sourceStartTime,
    sourceEndTime: clip.sourceEndTime,
    platforms: copies,
    captions,
    scheduledDates,
    publishingStatus,
  });

  await prisma.shortClip.update({
    where: { id },
    data: {
      exportPath: dir,
      status: clip.status === "editing" || clip.status === "approved" ? "exported" : clip.status,
    },
  });

  return NextResponse.json({ dir, manifest });
}
