import { prisma } from "@/lib/storage/prisma";
import { buildIdempotencyKey } from "@/lib/publishing/idempotency";
import { backoffMs } from "@/lib/publishing/errors";

/** Platforms that upload immediately with a native publishAt (do not wait until air time). */
const NATIVE_SCHEDULE_UPLOAD_NOW = new Set(["youtube_shorts"]);

export function usesNativeScheduleUploadNow(platform: string): boolean {
  return NATIVE_SCHEDULE_UPLOAD_NOW.has(platform);
}

export async function enqueuePublishingJob(input: {
  platformPostId: string;
  platformConnectionId?: string | null;
  scheduledAt?: Date | null;
  dryRun?: boolean;
  mediaChecksum?: string | null;
}) {
  const post = await prisma.platformPost.findUnique({ where: { id: input.platformPostId } });
  if (!post) throw new Error("PlatformPost not found");

  const scheduledAt = input.scheduledAt || post.scheduledAt;
  const connectionId = input.platformConnectionId || "none";
  const idempotencyKey = buildIdempotencyKey({
    platform: post.platform,
    platformConnectionId: connectionId,
    platformPostId: post.id,
    mediaChecksum: input.mediaChecksum || post.mediaChecksum,
    scheduleVersion: scheduledAt?.toISOString() || "immediate",
  });

  // YouTube: upload now with publishAt — claim immediately even when scheduledAt is future.
  const nativeNow =
    usesNativeScheduleUploadNow(post.platform) &&
    Boolean(scheduledAt && scheduledAt.getTime() > Date.now());
  const nextAttemptAt = nativeNow ? new Date() : scheduledAt || new Date();

  const existing = await prisma.publishingJob.findUnique({ where: { idempotencyKey } });
  if (existing && ["published", "awaiting_platform_processing"].includes(existing.status)) {
    return { job: existing, duplicate: true as const };
  }

  if (existing) {
    const updated = await prisma.publishingJob.update({
      where: { id: existing.id },
      data: {
        status: scheduledAt ? "scheduled" : "pending",
        scheduledAt,
        platformConnectionId: input.platformConnectionId || existing.platformConnectionId,
        dryRun: input.dryRun ?? existing.dryRun,
        nextAttemptAt,
      },
    });
    return { job: updated, duplicate: false as const };
  }

  const job = await prisma.publishingJob.create({
    data: {
      platformPostId: post.id,
      platformConnectionId: input.platformConnectionId || null,
      status: scheduledAt ? "scheduled" : "pending",
      scheduledAt,
      nextAttemptAt,
      idempotencyKey,
      dryRun: Boolean(input.dryRun),
    },
  });
  return { job, duplicate: false as const };
}

export async function claimDueJob(workerId: string, now = new Date()) {
  const staleBefore = new Date(now.getTime() - 15 * 60 * 1000);
  await prisma.publishingJob.updateMany({
    where: {
      lockedAt: { lt: staleBefore },
      status: { in: ["validating", "uploading", "processing", "publishing"] },
    },
    data: {
      lockedAt: null,
      lockedBy: null,
      status: "failed_retryable",
      lastErrorMessage: "Stale lock recovered",
      lastErrorRetryable: true,
      nextAttemptAt: now,
    },
  });

  const candidates = await prisma.publishingJob.findMany({
    where: {
      status: { in: ["pending", "scheduled", "failed_retryable"] },
      OR: [{ nextAttemptAt: null }, { nextAttemptAt: { lte: now } }],
      AND: [
        {
          OR: [
            { scheduledAt: null },
            { scheduledAt: { lte: now } },
            // YouTube native schedule: upload before air time with publishAt
            {
              platformPost: { platform: { in: [...NATIVE_SCHEDULE_UPLOAD_NOW] } },
            },
          ],
        },
      ],
      lockedAt: null,
    },
    orderBy: [{ nextAttemptAt: "asc" }, { createdAt: "asc" }],
    take: 5,
  });

  for (const candidate of candidates) {
    const updated = await prisma.publishingJob.updateMany({
      where: { id: candidate.id, lockedAt: null },
      data: {
        lockedAt: now,
        lockedBy: workerId,
        startedAt: candidate.startedAt || now,
        status: "validating",
      },
    });
    if (updated.count === 1) {
      return prisma.publishingJob.findUnique({
        where: { id: candidate.id },
        include: {
          platformPost: { include: { shortClip: true } },
          platformConnection: true,
        },
      });
    }
  }
  return null;
}

export async function completeJobSuccess(input: {
  jobId: string;
  externalPostId?: string;
  externalPostUrl?: string;
  externalUploadId?: string;
  responseSummary?: string;
  status?: string;
}) {
  return prisma.publishingJob.update({
    where: { id: input.jobId },
    data: {
      status: input.status || "published",
      completedAt: new Date(),
      lockedAt: null,
      lockedBy: null,
      externalPostId: input.externalPostId,
      externalPostUrl: input.externalPostUrl,
      externalUploadId: input.externalUploadId,
      responseSummary: input.responseSummary,
      lastErrorCode: null,
      lastErrorMessage: null,
      lastErrorRetryable: null,
    },
  });
}

export async function failJob(input: {
  jobId: string;
  attemptCount: number;
  maxAttempts: number;
  errorCode?: string;
  errorMessage: string;
  retryable: boolean;
  responseSummary?: string;
}) {
  const nextAttempt = input.retryable && input.attemptCount < input.maxAttempts;
  return prisma.publishingJob.update({
    where: { id: input.jobId },
    data: {
      status: nextAttempt
        ? "failed_retryable"
        : input.retryable
          ? "failed_permanent"
          : "failed_permanent",
      lockedAt: null,
      lockedBy: null,
      lastErrorCode: input.errorCode,
      lastErrorMessage: input.errorMessage,
      lastErrorRetryable: input.retryable,
      responseSummary: input.responseSummary,
      nextAttemptAt: nextAttempt
        ? new Date(Date.now() + backoffMs(input.attemptCount))
        : null,
      completedAt: nextAttempt ? null : new Date(),
    },
  });
}

export async function recordAttempt(input: {
  jobId: string;
  attemptNumber: number;
  status: string;
  httpStatus?: number;
  errorCategory?: string;
  errorMessage?: string;
  retryable?: boolean;
  requestId?: string;
  responseSummary?: string;
}) {
  return prisma.publishingAttempt.create({
    data: {
      publishingJobId: input.jobId,
      attemptNumber: input.attemptNumber,
      completedAt: new Date(),
      status: input.status,
      httpStatus: input.httpStatus,
      errorCategory: input.errorCategory,
      errorMessage: input.errorMessage,
      retryable: Boolean(input.retryable),
      requestId: input.requestId,
      responseSummary: input.responseSummary,
    },
  });
}
