import { NextResponse } from "next/server";
import { prisma } from "@/lib/storage/prisma";
import { enqueuePublishingJob } from "@/lib/publishing/jobs";
import { isDryRun } from "@/lib/env";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export async function POST(
  req: Request,
  ctx: { params: Promise<{ id: string }> },
) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const { id } = await ctx.params;
  const body = await req.json().catch(() => ({}));
  const post = await prisma.platformPost.findUnique({
    where: { id },
    include: { shortClip: true },
  });
  if (!post) return NextResponse.json({ error: "Post not found" }, { status: 404 });

  if (!post.approvedForPublish && body.force !== true) {
    return NextResponse.json(
      { error: "Post not approved for publish. Set approvedForPublish or pass force with care." },
      { status: 400 },
    );
  }

  const connection = await prisma.platformConnection.findFirst({
    where: {
      platform: post.platform,
      connectionStatus: { in: ["connected", "requires_attention"] },
      disconnectedAt: null,
    },
    orderBy: { updatedAt: "desc" },
  });

  const { job, duplicate } = await enqueuePublishingJob({
    platformPostId: post.id,
    platformConnectionId: connection?.id,
    scheduledAt: body.publishNow ? new Date() : post.scheduledAt,
    dryRun: isDryRun() || Boolean(body.dryRun),
    mediaChecksum: post.mediaChecksum || post.shortClip.fileChecksum,
  });

  if (body.publishNow) {
    await prisma.platformPost.update({
      where: { id: post.id },
      data: { uploadStatus: "scheduled", scheduledAt: new Date() },
    });
  }

  return NextResponse.json({
    jobId: job.id,
    status: job.status,
    duplicate,
    note: connection
      ? "Job enqueued. Ensure `npm run worker` is running."
      : "No connection found — job will require manual action.",
  });
}
