import { NextResponse } from "next/server";
import { prisma } from "@/lib/storage/prisma";
import { assertPostTransition } from "@/lib/publishing/status";
import { canForceRepost, detectDuplicates } from "@/lib/publishing/duplicates";
import { getAdapterForPlatform } from "@/lib/publishing/adapters";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export async function PATCH(
  req: Request,
  ctx: { params: Promise<{ id: string }> },
) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const { id } = await ctx.params;
  const body = await req.json();
  const post = await prisma.platformPost.findUnique({
    where: { id },
    include: { shortClip: true },
  });
  if (!post) return NextResponse.json({ error: "Post not found" }, { status: 404 });

  if (body.uploadStatus && body.uploadStatus !== post.uploadStatus) {
    try {
      assertPostTransition(post.uploadStatus, body.uploadStatus);
    } catch (err) {
      return NextResponse.json(
        { error: err instanceof Error ? err.message : "Invalid transition" },
        { status: 400 },
      );
    }
  }

  if (body.uploadStatus === "scheduled" || body.uploadStatus === "published") {
    const existing = await prisma.platformPost.findMany({
      where: {
        platform: post.platform,
        id: { not: post.id },
        OR: [
          { shortClipId: post.shortClipId },
          { platformUrl: { not: null } },
        ],
      },
      include: { shortClip: true },
    });

    const warnings = detectDuplicates({
      shortClipId: post.shortClipId,
      platform: post.platform,
      title: body.title ?? post.title,
      caption: body.caption ?? post.caption,
      fileChecksum: post.shortClip.fileChecksum,
      scheduledAt: body.scheduledAt ? new Date(body.scheduledAt) : post.scheduledAt,
      existing: existing.map((e) => ({
        id: e.id,
        shortClipId: e.shortClipId,
        platform: e.platform,
        title: e.title,
        caption: e.caption,
        platformUrl: e.platformUrl,
        scheduledAt: e.scheduledAt,
        publishedAt: e.publishedAt,
        fileChecksum: e.shortClip.fileChecksum,
      })),
    });

    const force = canForceRepost(warnings, body.repostReason);
    if (!force.ok) {
      return NextResponse.json({ error: force.error, warnings }, { status: 409 });
    }
  }

  const adapter = getAdapterForPlatform(post.platform);
  if (body.uploadStatus === "published") {
    const validation = await adapter.validate({
      id: post.id,
      platform: post.platform,
      title: post.title,
      caption: post.caption,
      exportPath: post.shortClip.exportPath,
      uploadStatus: body.uploadStatus,
    });
    if (!validation.ok) {
      return NextResponse.json({ error: validation.errors.join("; ") }, { status: 400 });
    }
  }

  const updated = await prisma.platformPost.update({
    where: { id },
    data: {
      uploadStatus: body.uploadStatus ?? post.uploadStatus,
      platformUrl: body.platformUrl !== undefined ? body.platformUrl : post.platformUrl,
      platformPostId: body.platformPostId ?? post.platformPostId,
      scheduledAt: body.scheduledAt ? new Date(body.scheduledAt) : post.scheduledAt,
      publishedAt:
        body.uploadStatus === "published"
          ? body.publishedAt
            ? new Date(body.publishedAt)
            : new Date()
          : post.publishedAt,
      notes: body.notes ?? post.notes,
      repostReason: body.repostReason ?? post.repostReason,
      title: body.title ?? post.title,
      caption: body.caption ?? post.caption,
      approvedForPublish:
        body.approvedForPublish !== undefined ? Boolean(body.approvedForPublish) : post.approvedForPublish,
      privacyStatus: body.privacyStatus !== undefined ? body.privacyStatus : post.privacyStatus,
      madeForKids: body.madeForKids !== undefined ? body.madeForKids : post.madeForKids,
      containsSyntheticMedia:
        body.containsSyntheticMedia !== undefined
          ? body.containsSyntheticMedia
          : post.containsSyntheticMedia,
    },
  });

  return NextResponse.json(updated);
}
