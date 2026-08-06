import { beforeAll, describe, expect, it, vi } from "vitest";
import {
  encryptSecret,
  decryptSecret,
  hashState,
  pkceChallenge,
  randomUrlSafe,
  validateEncryptionKey,
} from "../src/lib/security/token-crypto";
import { buildIdempotencyKey } from "../src/lib/publishing/idempotency";
import { backoffMs, classifyHttpError, redactSummary } from "../src/lib/publishing/errors";
import { youtubeCapabilities, YouTubePublishingAdapter, resolveYouTubeSchedule } from "../src/lib/publishing/adapters/youtube";
import { TikTokPublishingAdapter } from "../src/lib/publishing/adapters/tiktok";
import { ThreadsPublishingAdapter } from "../src/lib/publishing/adapters/threads";
import { MockStagingProvider } from "../src/lib/publishing/media/staging";
import { prisma } from "../src/lib/storage/prisma";
import { createOAuthState, consumeOAuthState } from "../src/lib/oauth/state";
import { claimDueJob, enqueuePublishingJob } from "../src/lib/publishing/jobs";

const TEST_KEY = Buffer.from("0123456789abcdef0123456789abcdef").toString("base64");

beforeAll(() => {
  process.env.ORBIT_TOKEN_ENCRYPTION_KEY = TEST_KEY;
  process.env.PUBLISHING_DRY_RUN = "true";
});

describe("token encryption", () => {
  it("round-trips secrets with fresh IVs", () => {
    validateEncryptionKey(TEST_KEY);
    const a = encryptSecret("access-token-one");
    const b = encryptSecret("access-token-one");
    expect(a).not.toEqual(b);
    expect(decryptSecret(a)).toBe("access-token-one");
    expect(decryptSecret(b)).toBe("access-token-one");
  });

  it("rejects bad key length", () => {
    expect(() => validateEncryptionKey("short")).toThrow(/32 bytes/);
  });
});

describe("oauth state", () => {
  it("creates single-use state with PKCE and rejects reuse/expiry", async () => {
    const created = await createOAuthState({
      platform: "youtube_shorts",
      withPkce: true,
      redirectPath: "/settings/connections",
    });
    expect(created.state.length).toBeGreaterThan(20);
    expect(created.codeChallenge).toBe(pkceChallenge(created.codeVerifier!));

    const first = await consumeOAuthState({
      platform: "youtube_shorts",
      state: created.state,
    });
    expect(first.ok).toBe(true);
    if (first.ok) expect(first.codeVerifier).toBe(created.codeVerifier);

    const second = await consumeOAuthState({
      platform: "youtube_shorts",
      state: created.state,
    });
    expect(second.ok).toBe(false);

    const expiredState = randomUrlSafe(32);
    await prisma.oAuthState.create({
      data: {
        platform: "youtube_shorts",
        stateHash: hashState(expiredState),
        expiresAt: new Date(Date.now() - 1000),
      },
    });
    const expired = await consumeOAuthState({
      platform: "youtube_shorts",
      state: expiredState,
    });
    expect(expired.ok).toBe(false);
  });
});

describe("idempotency and errors", () => {
  it("builds stable keys and classifies retryable errors", () => {
    const k1 = buildIdempotencyKey({
      platform: "youtube_shorts",
      platformConnectionId: "c1",
      platformPostId: "p1",
      mediaChecksum: "abc",
      scheduleVersion: "v1",
    });
    const k2 = buildIdempotencyKey({
      platform: "youtube_shorts",
      platformConnectionId: "c1",
      platformPostId: "p1",
      mediaChecksum: "abc",
      scheduleVersion: "v1",
    });
    expect(k1).toBe(k2);
    expect(classifyHttpError(429).retryable).toBe(true);
    expect(classifyHttpError(401).retryable).toBe(false);
    expect(classifyHttpError(400, "bad caption").retryable).toBe(false);
    expect(backoffMs(2)).toBeGreaterThanOrEqual(5 * 60_000);
    expect(redactSummary({ access_token: "secret", ok: true })).toContain("[REDACTED]");
  });
});

describe("capabilities", () => {
  it("does not claim YouTube publish without scopes", () => {
    const caps = youtubeCapabilities(true, []);
    expect(caps.canPublishDirectly).toBe(false);
  });

  it("separates TikTok draft vs direct", () => {
    const adapter = new TikTokPublishingAdapter();
    const draftOnly = adapter.getCapabilities({
      id: "1",
      platform: "tiktok",
      connectionStatus: "connected",
      grantedScopes: JSON.stringify(["video.upload"]),
    });
    expect(draftOnly.canUploadDraft).toBe(true);
    expect(draftOnly.canPublishDirectly).toBe(false);

    const direct = adapter.getCapabilities({
      id: "1",
      platform: "tiktok",
      connectionStatus: "connected",
      grantedScopes: JSON.stringify(["video.upload", "video.publish"]),
    });
    expect(direct.canPublishDirectly).toBe(true);
  });

  it("keeps Threads manual until connected with scopes", () => {
    const adapter = new ThreadsPublishingAdapter();
    const caps = adapter.getCapabilities(null);
    expect(caps.canPublishDirectly).toBe(false);
    expect(caps.requiresManualCompletion).toBe(true);
  });
});

describe("youtube dry-run publish", () => {
  it("never marks published without platform confirmation", async () => {
    const adapter = new YouTubePublishingAdapter();
    const result = await adapter.publish(
      {
        id: "post1",
        platform: "youtube_shorts",
        title: "Test Short",
        caption: "hello",
        uploadStatus: "ready",
        privacyStatus: "private",
        madeForKids: false,
        mediaFilePath: "/tmp/does-not-need-to-exist-for-dry-run.mp4",
      },
      {
        id: "conn1",
        platform: "youtube_shorts",
        connectionStatus: "connected",
        grantedScopes: JSON.stringify([
          "https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.readonly",
        ]),
        accessTokenEncrypted: encryptSecret("fake"),
      },
      {
        dryRun: true,
        workerId: "test",
        jobId: "job1",
        attemptNumber: 1,
        accessToken: "fake",
      },
    );
    expect(result.published).toBe(false);
    expect(result.method).toBe("dry_run");
    expect(result.platformPostId).toBeUndefined();
  });

  it("includes publishAt in dry-run when scheduled far enough ahead", async () => {
    const adapter = new YouTubePublishingAdapter();
    const publishAt = new Date(Date.now() + 2 * 60 * 60 * 1000);
    const result = await adapter.publish(
      {
        id: "post-sched",
        platform: "youtube_shorts",
        title: "Scheduled Short",
        caption: "hello",
        uploadStatus: "ready",
        privacyStatus: "private",
        madeForKids: false,
        scheduledAt: publishAt,
        mediaFilePath: "/tmp/does-not-need-to-exist-for-dry-run.mp4",
        contentFormat: "longform",
      },
      {
        id: "conn1",
        platform: "youtube_shorts",
        connectionStatus: "connected",
        grantedScopes: JSON.stringify([
          "https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.readonly",
        ]),
        accessTokenEncrypted: encryptSecret("fake"),
      },
      {
        dryRun: true,
        workerId: "test",
        jobId: "job-sched",
        attemptNumber: 1,
        accessToken: "fake",
      },
    );
    expect(result.success).toBe(true);
    expect(result.published).toBe(false);
    expect(result.scheduledOnPlatform).toBe(true);
    expect(result.scheduledFor).toBe(publishAt.toISOString());
    expect(result.responseSummary).toContain("publishAt");
    expect(result.responseSummary).toContain("categoryId");
    expect(result.responseSummary).toContain("en-GB");
  });

  it("dry-run public immediate upload sets notifySubscribers true", async () => {
    const adapter = new YouTubePublishingAdapter();
    const result = await adapter.publish(
      {
        id: "post-public",
        platform: "youtube_shorts",
        title: "Public Short",
        caption: "hello",
        uploadStatus: "ready",
        privacyStatus: "public",
        madeForKids: false,
        mediaFilePath: "/tmp/does-not-need-to-exist-for-dry-run.mp4",
      },
      {
        id: "conn1",
        platform: "youtube_shorts",
        connectionStatus: "connected",
        grantedScopes: JSON.stringify([
          "https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.readonly",
        ]),
        accessTokenEncrypted: encryptSecret("fake"),
      },
      {
        dryRun: true,
        workerId: "test",
        jobId: "job-public",
        attemptNumber: 1,
        accessToken: "fake",
      },
    );
    expect(result.success).toBe(true);
    expect(result.responseSummary).toContain('"notifySubscribers":true');
    expect(result.responseSummary).toContain('"categoryId":"27"');
  });
});

describe("youtube schedule helpers", () => {
  it("resolves publishAt only when far enough in the future", () => {
    const now = new Date("2026-08-05T12:00:00.000Z");
    expect(resolveYouTubeSchedule(null, now).usePublishAt).toBe(false);
    expect(resolveYouTubeSchedule(new Date("2026-08-05T12:10:00.000Z"), now).usePublishAt).toBe(
      false,
    );
    const far = resolveYouTubeSchedule(new Date("2026-08-05T14:00:00.000Z"), now);
    expect(far.usePublishAt).toBe(true);
    expect(far.publishAtIso).toBe("2026-08-05T14:00:00.000Z");
  });
});

describe("media staging mock", () => {
  it("is explicitly non-production", async () => {
    const mock = new MockStagingProvider();
    const staged = await mock.stageMedia("/tmp/x.mp4");
    expect(staged.mode).toBe("mock");
    expect(staged.publicUrl).toMatch(/example\.test\/mock/);
  });
});

describe("publishing jobs locking", () => {
  it("enqueues idempotently and allows only one claim", async () => {
    const video = await prisma.longFormVideo.findFirst({ include: { clips: { include: { posts: true } } } });
    const post = video?.clips[0]?.posts[0];
    if (!post) {
      // Seed may be missing in fresh CI — create minimal rows
      const v = await prisma.longFormVideo.create({
        data: {
          title: "Lock Test",
          slug: `lock-test-${Date.now()}`,
          topic: "Test",
          status: "published",
        },
      });
      const clip = await prisma.shortClip.create({
        data: {
          longFormVideoId: v.id,
          clipNumber: 1,
          workingTitle: "Clip",
          status: "exported",
        },
      });
      const createdPost = await prisma.platformPost.create({
        data: {
          shortClipId: clip.id,
          platform: "youtube_shorts",
          caption: "x",
          uploadStatus: "ready",
          approvedForPublish: true,
          privacyStatus: "private",
          madeForKids: false,
        },
      });
      const first = await enqueuePublishingJob({
        platformPostId: createdPost.id,
        scheduledAt: new Date(Date.now() - 1000),
        dryRun: true,
      });
      const second = await enqueuePublishingJob({
        platformPostId: createdPost.id,
        scheduledAt: first.job.scheduledAt,
        dryRun: true,
      });
      expect(second.job.id).toBe(first.job.id);

      const a = await claimDueJob("worker-a");
      const b = await claimDueJob("worker-b");
      expect(a?.id).toBe(first.job.id);
      expect(b?.id).not.toBe(a?.id);
      return;
    }

    const first = await enqueuePublishingJob({
      platformPostId: post.id,
      scheduledAt: new Date(Date.now() - 1000),
      dryRun: true,
    });
    const again = await enqueuePublishingJob({
      platformPostId: post.id,
      scheduledAt: first.job.scheduledAt,
      dryRun: true,
    });
    expect(again.job.idempotencyKey).toBe(first.job.idempotencyKey);

    const claimed = await claimDueJob(`worker-${Date.now()}`);
    expect(claimed).toBeTruthy();
    const claimed2 = await claimDueJob(`worker-other-${Date.now()}`);
    if (claimed2) expect(claimed2.id).not.toBe(claimed!.id);
  });

  it("claims future YouTube schedules immediately for publishAt upload", async () => {
    // Isolate from leftover due jobs in shared dev.db
    await prisma.publishingJob.updateMany({
      where: {
        status: { in: ["pending", "scheduled", "failed_retryable"] },
        lockedAt: null,
      },
      data: { status: "cancelled", lastErrorMessage: "test isolation" },
    });

    const v = await prisma.longFormVideo.create({
      data: {
        title: "Future YT",
        slug: `future-yt-${Date.now()}`,
        topic: "Test",
        status: "published",
      },
    });
    const clip = await prisma.shortClip.create({
      data: {
        longFormVideoId: v.id,
        clipNumber: 99,
        workingTitle: "Future clip",
        status: "exported",
      },
    });
    const createdPost = await prisma.platformPost.create({
      data: {
        shortClipId: clip.id,
        platform: "youtube_shorts",
        title: "Future",
        caption: "x",
        uploadStatus: "ready",
        approvedForPublish: true,
        privacyStatus: "private",
        madeForKids: false,
      },
    });
    const future = new Date(Date.now() + 3 * 24 * 60 * 60 * 1000);
    const { job } = await enqueuePublishingJob({
      platformPostId: createdPost.id,
      scheduledAt: future,
      dryRun: true,
    });
    expect(job.status).toBe("scheduled");
    expect(job.nextAttemptAt!.getTime()).toBeLessThanOrEqual(Date.now() + 5_000);

    const claimed = await claimDueJob(`worker-future-${Date.now()}`);
    expect(claimed?.id).toBe(job.id);
  });
});

describe("optional integration gates", () => {
  it("keeps live platform tests off by default", () => {
    expect(process.env.RUN_YOUTUBE_INTEGRATION_TESTS || "false").toBe("false");
    expect(process.env.RUN_META_INTEGRATION_TESTS || "false").toBe("false");
  });
});

// silence unused vi import if tree-shaken oddly
void vi;
