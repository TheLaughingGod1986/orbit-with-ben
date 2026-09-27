/**
 * Runs the Buffer mirror end to end (STUDIO_PLAYBOOK.md §12):
 * - mirrorVideo: after an upload, host the media, plan from the live YouTube record,
 *   create the Buffer posts and record them. Called by the package upload and the CLI.
 * - runBufferCheck: keep Buffer in step with YouTube (moved times, pulled videos), and mirror
 *   scheduled uploads that never went through youtube:package, using media-finder to find their
 *   local file. Called daily by the Mac LaunchAgent dev.orbit.buffer-check.
 * Everything external is injected, so the flow is testable without YouTube or Buffer.
 */
import path from "path";
import type { BufferClient } from "@/lib/publishing/buffer-api";
import type { BufferStore } from "@/lib/publishing/buffer-store";
import type { HostFile } from "@/lib/publishing/media-host";
import type { MediaHint } from "@/lib/publishing/media-finder";
import {
  BUFFER_CHANNELS,
  type BufferChannel,
  type ChannelIds,
  type Plan,
  type PlanAction,
  type YouTubeVideo,
  isShort,
  planBufferMirror,
  reconcileEntry,
} from "@/lib/publishing/buffer-mirror";

export type MirrorDeps = {
  youtubeToken: () => Promise<string>;
  fetchVideos: (token: string, ids: string[]) => Promise<Map<string, YouTubeVideo>>;
  listScheduled: (token: string, now: Date) => Promise<YouTubeVideo[]>;
  /** null plans only (no API key). */
  client: BufferClient | null;
  store: BufferStore;
  /** null when no Blob token: a local file can't be hosted. */
  host: HostFile | null;
  checkUrl: (url: string, want: "video" | "image") => Promise<string | null>;
  channelIds: ChannelIds;
  now: () => Date;
  /** Local file for an upload made outside youtube:package (media-finder). Absent: report only. */
  findMedia?: (videoId: string) => MediaHint | null;
};

export type MirrorRequest = {
  videoId: string;
  kind?: "short" | "long";
  longId?: string | null;
  standalone?: boolean;
  mediaPath?: string | null;
  mediaUrl?: string;
  thumbPath?: string | null;
  thumbUrl?: string;
  allowLate?: boolean;
  dryRun?: boolean;
};

export type ActionResult = {
  channel: BufferChannel;
  action: PlanAction["action"];
  ok: boolean;
  postId?: string | null;
  error?: string;
  reason?: string;
};

export type MirrorOutcome = { plan: Plan; results: ActionResult[]; sent: boolean; hostedUrl: string | null };

const DRY_HOST = "https://dry-run.invalid/social";

export async function executeActions(
  plan: Pick<Plan, "videoId" | "kind" | "title" | "timing" | "actions">,
  client: BufferClient,
  store: BufferStore,
): Promise<ActionResult[]> {
  const results: ActionResult[] = [];
  for (const a of plan.actions) {
    try {
      if (a.action === "skip") {
        results.push({ channel: a.channel, action: a.action, ok: true, reason: a.reason });
      } else if (a.action === "create_post") {
        const post = await client.createPost(a.input);
        await store.record(plan, a.channel, post.id);
        results.push({ channel: a.channel, action: a.action, ok: true, postId: post.id });
      } else if (a.action === "edit_post") {
        await client.editPost(a.input);
        await store.record(plan, a.channel, a.input.postId);
        results.push({ channel: a.channel, action: a.action, ok: true, postId: a.input.postId });
      } else {
        try {
          await client.deletePost(a.input.postId);
        } catch (e) {
          // Already gone in Buffer: forget it here too.
          if (!/NotFound/i.test((e as Error).message)) throw e;
        }
        await store.record(plan, a.channel, null);
        results.push({ channel: a.channel, action: a.action, ok: true, postId: null });
      }
    } catch (e) {
      results.push({ channel: a.channel, action: a.action, ok: false, error: (e as Error).message });
    }
  }
  return results;
}

export async function mirrorVideo(req: MirrorRequest, deps: MirrorDeps): Promise<MirrorOutcome> {
  const token = await deps.youtubeToken();
  const ids = req.longId ? [req.videoId, req.longId] : [req.videoId];
  const videos = await deps.fetchVideos(token, ids);
  const video = videos.get(req.videoId);
  if (!video) throw new Error(`${req.videoId} not found on the channel`);
  const long = req.longId ? videos.get(req.longId) : undefined;
  if (req.longId && !long) throw new Error(`long ${req.longId} not found on the channel`);

  const ledger = await deps.store.load();
  const now = deps.now();
  const short = isShort(video, req.kind);
  const kind = short ? "short" : "long";
  const localPath = short ? req.mediaPath : req.thumbPath;
  const givenUrl = short ? req.mediaUrl : req.thumbUrl;
  const entry = ledger.videos[video.id];
  const needsMedia = BUFFER_CHANNELS.some((c) => !entry?.channels[c]) && (short || !entry?.channels.instagram);

  const planWith = (url: string | undefined) =>
    planBufferMirror({
      video,
      channelIds: deps.channelIds,
      ledger,
      now,
      kind,
      mediaUrl: short ? url : undefined,
      thumbUrl: short ? undefined : url,
      parentLong: long ? { id: long.id, goesPublicAt: long.privacyStatus === "public" ? long.publishedAt : long.publishAt } : null,
      standalone: req.standalone,
      allowLate: req.allowLate,
    });

  // Plan once with a stand-in URL, so a refused video never gets its file uploaded.
  let url = givenUrl;
  if (!url && localPath) url = `${DRY_HOST}/${video.id}${path.extname(localPath).toLowerCase()}`;
  let plan = planWith(url);
  let hostedUrl: string | null = null;
  if (plan.errors.length || req.dryRun) {
    return { plan, results: [], sent: false, hostedUrl };
  }

  if (needsMedia && !givenUrl && localPath) {
    if (!deps.host) {
      plan.errors.push("No Blob store token (BLOB_READ_WRITE_TOKEN), so the media can't be hosted");
      plan.actions = [];
      return { plan, results: [], sent: false, hostedUrl };
    }
    hostedUrl = await deps.host(localPath, `social/${video.id}${path.extname(localPath).toLowerCase()}`);
    url = hostedUrl;
    plan = planWith(url);
  }
  if (needsMedia && url && plan.actions.some((a) => a.action === "create_post")) {
    const problem = await deps.checkUrl(url, short ? "video" : "image");
    if (problem) {
      plan.errors.push(problem);
      plan.actions = [];
    }
  }
  if (plan.errors.length || !deps.client) return { plan, results: [], sent: false, hostedUrl };
  return { plan, results: await executeActions(plan, deps.client, deps.store), sent: true, hostedUrl };
}

export type CheckOutcome = {
  checked: number;
  changes: { videoId: string; kind: "short" | "long"; title: string; timing: Plan["timing"]; actions: PlanAction[]; results: ActionResult[] }[];
  /** Scheduled uploads that weren't in Buffer and were mirrored (or, dry, would be) by this run. */
  autoMirrored: { videoId: string; title: string; source: string; sent: boolean; results: ActionResult[]; warnings: string[] }[];
  /** Scheduled uploads still not in Buffer, and why. */
  unmirrored: { videoId: string; title: string; publishAt: string | null; reason: string }[];
  sent: boolean;
};

export async function runBufferCheck(deps: MirrorDeps, opts: { dryRun?: boolean } = {}): Promise<CheckOutcome> {
  const token = await deps.youtubeToken();
  const ledger = await deps.store.load();
  const now = deps.now();
  const ids = Object.keys(ledger.videos);
  const videos = ids.length ? await deps.fetchVideos(token, ids) : new Map<string, YouTubeVideo>();
  const send = !opts.dryRun && Boolean(deps.client);
  const changes: CheckOutcome["changes"] = [];

  for (const id of ids) {
    const entry = ledger.videos[id];
    const video = videos.get(id) ?? null;
    const actions = reconcileEntry(id, entry, video, now);
    if (!actions.length) continue;
    const timing: Plan["timing"] =
      video?.privacyStatus === "private" && video.publishAt
        ? { mode: "customScheduled", dueAt: new Date(video.publishAt).toISOString() }
        : { mode: "none", reason: "no longer going public" };
    const plan = { videoId: id, kind: entry.kind, title: entry.title, timing, actions };
    const results = send ? await executeActions(plan, deps.client!, deps.store) : [];
    changes.push({ videoId: id, kind: entry.kind, title: entry.title, timing, actions, results });
  }

  // Uploads made outside youtube:package: find the local file and mirror them too.
  const scheduled = await deps.listScheduled(token, now);
  const autoMirrored: CheckOutcome["autoMirrored"] = [];
  const unmirrored: CheckOutcome["unmirrored"] = [];
  for (const v of scheduled.filter((x) => !ledger.videos[x.id])) {
    const miss = (reason: string) => unmirrored.push({ videoId: v.id, title: v.title, publishAt: v.publishAt, reason });
    const hint = deps.findMedia?.(v.id) ?? null;
    if (!hint) {
      miss(`no local file recorded: run buffer-mirror.ts register --video ${v.id} --media <mp4> --long <longId> (or --thumb <jpg> for a long)`);
      continue;
    }
    try {
      const outcome = await mirrorVideo(
        {
          videoId: v.id,
          longId: hint.longId,
          standalone: hint.standalone,
          mediaPath: hint.mediaPath,
          thumbPath: hint.thumbPath,
          dryRun: !send,
        },
        deps,
      );
      if (outcome.plan.errors.length) {
        miss(`${outcome.plan.errors.join("; ")} (from ${hint.source})`);
        continue;
      }
      autoMirrored.push({ videoId: v.id, title: v.title, source: hint.source, sent: outcome.sent, results: outcome.results, warnings: outcome.plan.warnings });
    } catch (e) {
      miss((e as Error).message);
    }
  }

  return { checked: ids.length, changes, autoMirrored, unmirrored, sent: send };
}
