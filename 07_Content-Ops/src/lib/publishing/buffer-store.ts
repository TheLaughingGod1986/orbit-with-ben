/**
 * Where the Buffer mirror remembers what it posted: the BufferMirrorPost table, so the
 * Mac upload and the daily Vercel job share one record. Each video is posted once per channel.
 */
import type { PrismaClient } from "@prisma/client";
import type { BufferChannel, Ledger, LedgerEntry, Plan } from "@/lib/publishing/buffer-mirror";

export type MirrorRow = {
  youtubeVideoId: string;
  channel: string;
  bufferPostId: string;
  kind: string;
  title: string;
  dueAt: Date | null;
  mode: string;
  updatedAt?: Date;
};

export interface BufferStore {
  load(): Promise<Ledger>;
  /** postId null removes the channel's row. */
  record(plan: Pick<Plan, "videoId" | "kind" | "title" | "timing">, channel: BufferChannel, postId: string | null): Promise<void>;
}

export function rowsToLedger(rows: MirrorRow[]): Ledger {
  const videos: Record<string, LedgerEntry> = {};
  for (const r of rows) {
    const entry = (videos[r.youtubeVideoId] ??= {
      kind: r.kind === "short" ? "short" : "long",
      title: r.title,
      dueAt: r.dueAt ? r.dueAt.toISOString() : null,
      mode: r.mode === "shareNow" ? "shareNow" : "customScheduled",
      channels: {},
    });
    entry.channels[r.channel as BufferChannel] = {
      postId: r.bufferPostId,
      recordedAt: (r.updatedAt ?? new Date(0)).toISOString(),
    };
  }
  return { version: 1, videos };
}

export function createPrismaBufferStore(prisma: PrismaClient): BufferStore {
  return {
    async load() {
      return rowsToLedger(await prisma.bufferMirrorPost.findMany());
    },
    async record(plan, channel, postId) {
      const key = { youtubeVideoId_channel: { youtubeVideoId: plan.videoId, channel } };
      if (!postId) {
        await prisma.bufferMirrorPost.deleteMany({ where: { youtubeVideoId: plan.videoId, channel } });
        return;
      }
      const existing = await prisma.bufferMirrorPost.findUnique({ where: key });
      const dueAt =
        plan.timing.mode === "customScheduled" ? new Date(plan.timing.dueAt) : plan.timing.mode === "shareNow" ? null : existing?.dueAt ?? null;
      const mode = plan.timing.mode === "shareNow" ? "shareNow" : existing?.mode ?? "customScheduled";
      await prisma.bufferMirrorPost.upsert({
        where: key,
        create: { youtubeVideoId: plan.videoId, channel, bufferPostId: postId, kind: plan.kind, title: plan.title, dueAt, mode },
        update: { bufferPostId: postId, kind: plan.kind, title: plan.title, dueAt, mode },
      });
    },
  };
}
