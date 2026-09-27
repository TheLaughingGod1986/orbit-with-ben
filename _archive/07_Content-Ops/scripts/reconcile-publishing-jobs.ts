#!/usr/bin/env tsx
import { prisma } from "../src/lib/storage/prisma";
import { getPublishingAdapter } from "../src/lib/publishing/adapters";

async function main() {
  const jobs = await prisma.publishingJob.findMany({
    where: {
      OR: [
        { status: "awaiting_platform_processing" },
        { lastErrorMessage: { contains: "timeout" } },
        { status: "failed_retryable", externalPostId: { not: null } },
      ],
    },
    include: { platformConnection: true, platformPost: true },
    take: 50,
  });

  for (const job of jobs) {
    if (!job.externalPostId || !job.platformConnection) {
      console.log(JSON.stringify({ jobId: job.id, action: "needs_manual_review" }));
      continue;
    }
    const adapter = getPublishingAdapter(job.platformPost.platform);
    const status = await adapter.getExternalStatus(job.externalPostId, job.platformConnection);
    console.log(
      JSON.stringify({
        jobId: job.id,
        externalPostId: job.externalPostId,
        status: status.status,
        detail: status.detail,
      }),
    );
    if (status.status === "published" && status.platformPostId) {
      await prisma.publishingJob.update({
        where: { id: job.id },
        data: {
          status: "published",
          externalPostUrl: status.platformUrl,
          completedAt: new Date(),
          lockedAt: null,
          lockedBy: null,
        },
      });
      await prisma.platformPost.update({
        where: { id: job.platformPostId },
        data: {
          uploadStatus: "published",
          publishedAt: new Date(),
          platformPostId: status.platformPostId,
          platformUrl: status.platformUrl,
        },
      });
    }
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => prisma.$disconnect());
