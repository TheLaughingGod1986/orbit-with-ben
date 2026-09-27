import { prisma } from "@/lib/storage/prisma";
import { getEnv, isDryRun } from "@/lib/env";
import { getPublishingAdapter } from "@/lib/publishing/adapters";
import {
  claimDueJob,
  completeJobSuccess,
  failJob,
  recordAttempt,
} from "@/lib/publishing/jobs";
import { decryptSecret } from "@/lib/security/token-crypto";
import { redactSummary } from "@/lib/publishing/errors";
import { detectDuplicates, canForceRepost } from "@/lib/publishing/duplicates";
import { isBufferOnlyPlatform } from "@/lib/publishing/buffer-mirror";

const workerId = process.env.PUBLISHING_WORKER_ID || "orbit-local-worker";
const POLL_MS = 5_000;

async function heartbeat(lastJobId?: string) {
  await prisma.workerHeartbeat.upsert({
    where: { workerId },
    create: {
      workerId,
      lastHeartbeatAt: new Date(),
      lastJobId,
      status: "online",
    },
    update: {
      lastHeartbeatAt: new Date(),
      lastJobId,
      status: "online",
    },
  });
}

async function processJob(
  job: NonNullable<Awaited<ReturnType<typeof claimDueJob>>>,
) {
  const attemptNumber = job.attemptCount + 1;
  await prisma.publishingJob.update({
    where: { id: job.id },
    data: { attemptCount: attemptNumber, status: "publishing" },
  });

  const post = job.platformPost;
  const connection = job.platformConnection;

  // Social posts go through Buffer (STUDIO_PLAYBOOK.md §12), never from this worker.
  if (isBufferOnlyPlatform(post.platform)) {
    const message = `${post.platform} posts go through Buffer (scripts/buffer-mirror.ts), not the worker`;
    await recordAttempt({
      jobId: job.id,
      attemptNumber,
      status: "failed",
      errorCategory: "configuration",
      errorMessage: message,
      retryable: false,
    });
    await failJob({
      jobId: job.id,
      attemptCount: attemptNumber,
      maxAttempts: job.maxAttempts,
      errorMessage: message,
      retryable: false,
    });
    await prisma.publishingJob.update({
      where: { id: job.id },
      data: { status: "manual_action_required" },
    });
    return;
  }

  const adapter = getPublishingAdapter(post.platform);
  const dryRun = isDryRun() || job.dryRun;

  if (!connection || connection.connectionStatus === "disconnected") {
    await recordAttempt({
      jobId: job.id,
      attemptNumber,
      status: "failed",
      errorCategory: "configuration",
      errorMessage: "No active platform connection",
      retryable: false,
    });
    await failJob({
      jobId: job.id,
      attemptCount: attemptNumber,
      maxAttempts: job.maxAttempts,
      errorMessage: "No active platform connection",
      retryable: false,
    });
    await prisma.publishingJob.update({
      where: { id: job.id },
      data: { status: "manual_action_required" },
    });
    return;
  }

  // Refresh if expired
  if (
    connection.accessTokenExpiresAt &&
    connection.accessTokenExpiresAt.getTime() < Date.now() + 60_000 &&
    adapter.refreshConnection
  ) {
    const refreshed = await adapter.refreshConnection(connection);
    if (!refreshed.ok) {
      await prisma.platformConnection.update({
        where: { id: connection.id },
        data: {
          connectionStatus: "expired",
          lastConnectionError: refreshed.message,
        },
      });
      await failJob({
        jobId: job.id,
        attemptCount: attemptNumber,
        maxAttempts: job.maxAttempts,
        errorMessage: `Token refresh failed: ${refreshed.message}`,
        retryable: false,
        errorCode: "authentication",
      });
      return;
    }
  }

  const fresh = await prisma.platformConnection.findUnique({ where: { id: connection.id } });
  if (!fresh?.accessTokenEncrypted) {
    await failJob({
      jobId: job.id,
      attemptCount: attemptNumber,
      maxAttempts: job.maxAttempts,
      errorMessage: "Missing access token",
      retryable: false,
      errorCode: "authentication",
    });
    return;
  }

  const accessToken = decryptSecret(fresh.accessTokenEncrypted);
  const validation = await adapter.validatePost({
    ...post,
    scheduledAt: post.scheduledAt || job.scheduledAt,
    exportPath: post.shortClip.exportPath,
    mediaFilePath: post.mediaFilePath || post.shortClip.exportPath,
    thumbnailPath: post.shortClip.thumbnailPath,
  });
  if (!validation.ok) {
    await recordAttempt({
      jobId: job.id,
      attemptNumber,
      status: "failed",
      errorCategory: "validation",
      errorMessage: validation.errors.join("; "),
      retryable: false,
    });
    await failJob({
      jobId: job.id,
      attemptCount: attemptNumber,
      maxAttempts: job.maxAttempts,
      errorMessage: validation.errors.join("; "),
      retryable: false,
      errorCode: "validation",
    });
    return;
  }

  // Duplicate protection
  const existing = await prisma.platformPost.findMany({
    where: {
      platform: post.platform,
      id: { not: post.id },
      OR: [{ shortClipId: post.shortClipId }, { platformUrl: { not: null } }],
    },
    include: { shortClip: true },
  });
  const warnings = detectDuplicates({
    shortClipId: post.shortClipId,
    platform: post.platform,
    title: post.title,
    caption: post.caption,
    fileChecksum: post.mediaChecksum || post.shortClip.fileChecksum,
    scheduledAt: post.scheduledAt,
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
  const force = canForceRepost(warnings, post.repostReason);
  if (!force.ok) {
    await failJob({
      jobId: job.id,
      attemptCount: attemptNumber,
      maxAttempts: job.maxAttempts,
      errorMessage: force.error || "Duplicate blocked",
      retryable: false,
      errorCode: "validation",
    });
    return;
  }

  // If already published with external ID, reconcile instead of republishing
  if (job.externalPostId || post.platformPostId) {
    const status = await adapter.getExternalStatus(
      job.externalPostId || post.platformPostId!,
      fresh,
    );
    if (status.status === "published" || status.status === "scheduled") {
      await completeJobSuccess({
        jobId: job.id,
        externalPostId: status.platformPostId,
        externalPostUrl: status.platformUrl,
        responseSummary: redactSummary(status),
        status: status.status === "scheduled" ? "awaiting_platform_processing" : "published",
      });
      await prisma.platformPost.update({
        where: { id: post.id },
        data: {
          uploadStatus: status.status === "scheduled" ? "scheduled" : "published",
          publishedAt: status.status === "published" ? new Date() : post.publishedAt,
          platformPostId: status.platformPostId,
          platformUrl: status.platformUrl,
        },
      });
      return;
    }
  }

  await prisma.publishingJob.update({ where: { id: job.id }, data: { status: "uploading" } });

  const result = await adapter.publish(
    {
      ...post,
      scheduledAt: post.scheduledAt || job.scheduledAt,
      exportPath: post.shortClip.exportPath,
      mediaFilePath: post.mediaFilePath || post.shortClip.exportPath,
      thumbnailPath: post.shortClip.thumbnailPath,
    },
    fresh,
    {
      dryRun,
      workerId,
      jobId: job.id,
      attemptNumber,
      accessToken,
      refreshToken: fresh.refreshTokenEncrypted
        ? decryptSecret(fresh.refreshTokenEncrypted)
        : undefined,
    },
  );

  await recordAttempt({
    jobId: job.id,
    attemptNumber,
    status: result.published
      ? result.scheduledOnPlatform
        ? "scheduled"
        : "published"
      : result.success
        ? "ok"
        : "failed",
    httpStatus: result.httpStatus,
    errorCategory: result.errorCategory,
    errorMessage: result.published ? undefined : result.message,
    retryable: result.retryable,
    requestId: result.requestId,
    responseSummary: result.responseSummary,
  });

  if (result.published && result.platformPostId) {
    const onPlatformSchedule = Boolean(result.scheduledOnPlatform);
    await completeJobSuccess({
      jobId: job.id,
      externalPostId: result.platformPostId,
      externalPostUrl: result.platformUrl,
      externalUploadId: result.externalUploadId,
      responseSummary: result.responseSummary,
      // Terminal for the worker — YouTube owns the remaining schedule clock.
      status: onPlatformSchedule ? "awaiting_platform_processing" : "published",
    });
    await prisma.platformPost.update({
      where: { id: post.id },
      data: {
        uploadStatus: onPlatformSchedule ? "scheduled" : "published",
        publishedAt: onPlatformSchedule ? null : new Date(),
        scheduledAt: result.scheduledFor
          ? new Date(result.scheduledFor)
          : post.scheduledAt,
        platformPostId: result.platformPostId,
        platformUrl: result.platformUrl,
        publishingMethod: "api",
      },
    });
    await prisma.platformConnection.update({
      where: { id: fresh.id },
      data: { lastSuccessfulPublishAt: new Date() },
    });
    return;
  }

  if (result.requiresManualCompletion || result.method === "draft_upload") {
    await prisma.publishingJob.update({
      where: { id: job.id },
      data: {
        status: "manual_action_required",
        lockedAt: null,
        lockedBy: null,
        externalUploadId: result.externalUploadId,
        lastErrorMessage: result.message,
        responseSummary: result.responseSummary,
        completedAt: new Date(),
      },
    });
    await prisma.platformPost.update({
      where: { id: post.id },
      data: {
        uploadStatus: "ready",
        notes: result.message,
      },
    });
    return;
  }

  if (result.method === "dry_run" && result.success) {
    await prisma.publishingJob.update({
      where: { id: job.id },
      data: {
        status: "dry_run_complete",
        lockedAt: null,
        lockedBy: null,
        completedAt: new Date(),
        responseSummary: result.responseSummary,
      },
    });
    return;
  }

  await failJob({
    jobId: job.id,
    attemptCount: attemptNumber,
    maxAttempts: job.maxAttempts,
    errorCode: result.errorCategory,
    errorMessage: result.message,
    retryable: Boolean(result.retryable),
    responseSummary: result.responseSummary,
  });
}

async function loop() {
  getEnv();
  console.log(`[worker] starting ${workerId} dryRun=${isDryRun()}`);
  await heartbeat();
  for (;;) {
    try {
      await heartbeat();
      const job = await claimDueJob(workerId);
      if (job) {
        console.log(`[worker] claimed job ${job.id} platform=${job.platformPost.platform}`);
        await processJob(job);
        await heartbeat(job.id);
      }
    } catch (err) {
      console.error("[worker] error", err instanceof Error ? err.message : err);
    }
    await new Promise((r) => setTimeout(r, POLL_MS));
  }
}

const isMain =
  typeof process.argv[1] === "string" && process.argv[1].includes("publishing-worker");

if (isMain) {
  loop().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}

export { processJob, heartbeat, claimDueJob };
