import { NextResponse } from "next/server";
import { prisma } from "@/lib/storage/prisma";
import { generateShortPlan } from "@/lib/content/generate-short-plan";
import { generatePlatformCopy } from "@/lib/platforms/generate-platform-copy";
import { scheduleClipAcrossPlatforms, suggestShortSlot } from "@/lib/publishing/schedule";
import { resolveAffiliateSocialContextForVideo } from "@/lib/affiliate/social-context";
import { assertAffiliateSafeSocialCopy } from "@/lib/affiliate/social-copy";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export async function POST(
  _req: Request,
  ctx: { params: Promise<{ id: string }> },
) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const { id } = await ctx.params;
  const video = await prisma.longFormVideo.findUnique({ where: { id } });
  if (!video) return NextResponse.json({ error: "Video not found" }, { status: 404 });
  if (!video.script?.trim()) {
    return NextResponse.json({ error: "Empty script — cannot propose clips" }, { status: 400 });
  }

  const plan = generateShortPlan({
    title: video.title,
    script: video.script,
    youtubeUrl: video.youtubeUrl,
  });
  if (plan.errors.length) {
    return NextResponse.json({ error: plan.errors.join("; ") }, { status: 400 });
  }

  const existing = await prisma.shortClip.count({ where: { longFormVideoId: id } });
  let created = 0;

  for (const proposed of plan.clips) {
    const clipNumber = existing + proposed.clipNumber;
    const clip = await prisma.shortClip.create({
      data: {
        longFormVideoId: id,
        clipNumber,
        workingTitle: proposed.workingTitle,
        hook: proposed.hook,
        hookCategory: proposed.hookCategory,
        transcript: proposed.transcript,
        sourceStartTime: proposed.sourceStartTime,
        sourceEndTime: proposed.sourceEndTime,
        targetDurationSeconds: proposed.targetDurationSeconds,
        visualDirection: proposed.visualDirection,
        onScreenText: proposed.onScreenText,
        endingLine: proposed.endingLine,
        callToAction: proposed.callToAction,
        whyItWorks: proposed.whyItWorks,
        status: "proposed",
        qualityScore: proposed.suitabilityScore,
        qualityBreakdown: JSON.stringify(proposed.qualityBreakdown),
        sortOrder: clipNumber,
      },
    });

    const affiliate = await resolveAffiliateSocialContextForVideo({
      videoId: video.id,
      clipHook: proposed.hook,
      clipTitle: proposed.workingTitle,
      clipTranscript: proposed.transcript,
    });

    const copies = generatePlatformCopy({
      shortTitle: proposed.workingTitle,
      hook: proposed.hook,
      topic: video.topic,
      transcript: proposed.transcript,
      youtubeUrl: video.youtubeUrl,
      longTitle: video.title,
      callToAction: proposed.callToAction,
      affiliate,
    });

    const youtubeAt = video.publicationDate
      ? suggestShortSlot({
          longFormPublicationDate: video.publicationDate,
          clipIndexZeroBased: clipNumber - 1,
        })
      : new Date();

    const schedule = scheduleClipAcrossPlatforms({ youtubeShortAt: youtubeAt });

    for (const copy of copies) {
      assertAffiliateSafeSocialCopy(copy.caption);
      const slot = schedule.find((s) => s.platform === copy.platform);
      await prisma.platformPost.create({
        data: {
          shortClipId: clip.id,
          platform: copy.platform,
          title: copy.title,
          caption: copy.caption,
          hashtags: JSON.stringify(copy.hashtags),
          callToAction: copy.callToAction,
          scheduledAt: slot?.scheduledAt,
          uploadStatus: "draft",
          publishingMethod: "manual",
          pinnedComment: copy.pinnedComment,
          coverText: copy.coverText,
          storyCaption: copy.storyCaption,
          commentPrompt: copy.commentPrompt,
        },
      });
    }
    created += 1;
  }

  return NextResponse.json({
    created,
    warnings: plan.warnings,
    note: "Clips proposed only — export after approval.",
  });
}
