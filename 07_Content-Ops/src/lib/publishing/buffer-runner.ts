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
import { isOwnBlobUrl, type HostFile, type StoredMedia } from "@/lib/publishing/media-host";
import type { MediaHint } from "@/lib/publishing/media-finder";
import {
  type Ledger,
  type BufferChannel,
  type ChannelIds,
  type Plan,
  type PlanAction,
  type SocialCopy,
  type YouTubeVideo,
  MEDIA_MAX_AGE_MS,
  entryMedia,
  isShort,
  planBufferMirror,
  reconcileEntry,
} from "@/lib/publishing/buffer-mirror";

export type MirrorDeps = {
  youtubeToken: () => Promise<string>;
  fetchVideos: (token: string, ids: string[]) => Promise<Map<string, YouTubeVideo>>;
  listScheduled: (token: string, now: Date) => Promise<YouTubeVideo[]>;
  /** Uploads that went public in the last 24 h (published straight away, or after the last check). */
  listRecentlyPublic?: (token: string, now: Date) => Promise<YouTubeVideo[]>;
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
  /** Deletes a Blob copy. Absent: Blob copies are kept. */
  deleteMedia?: (url: string) => Promise<void>;
  /** Lists the mirror's Blob files, to adopt untracked ones and sweep orphans. */
  listMedia?: () => Promise<StoredMedia[]>;
};

/** A file older than this that no Buffer post links to is an orphan. */
const ORPHAN_AGE_MS = 2 * 24 * 60 * 60 * 1000;

/** social/<11-character YouTube id><random suffix>.<ext> → the YouTube id. */
export function videoIdFromBlobPath(pathname: string): string | null {
  const m = /^social\/([\w-]{11})/.exec(pathname);
  return m ? m[1] : null;
}

export type MirrorRequest = {
  videoId: string;
  kind?: "short" | "long";
  longId?: string | null;
  standalone?: boolean;
  mediaPath?: string | null;
  mediaUrl?: string;
  thumbPath?: string | null;
  thumbUrl?: string;
  /** A long's vertical trailer: a Reel on Instagram and Facebook. */
  trailerPath?: string | null;
  trailerUrl?: string;
  /** Hook, question, alt text and cover frame (UPLOADS.json `social`). */
  social?: SocialCopy;
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

/** Blob copies this run uploaded. */
export type MirrorOutcome = { plan: Plan; results: ActionResult[]; sent: boolean; hosted: string[] };

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

type MediaRole = "media" | "thumb" | "trailer";

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

  // The files this video can use: a Short's mp4, or a long's thumbnail and trailer.
  const files: { role: MediaRole; localPath: string | null; url: string | undefined; want: "video" | "image" }[] = short
    ? [{ role: "media", localPath: req.mediaPath ?? null, url: req.mediaUrl, want: "video" }]
    : [
        { role: "thumb", localPath: req.thumbPath ?? null, url: req.thumbUrl, want: "image" },
        { role: "trailer", localPath: req.trailerPath ?? null, url: req.trailerUrl, want: "video" },
      ];
  const urls = new Map<MediaRole, string | undefined>();
  const planWith = () =>
    planBufferMirror({
      video,
      channelIds: deps.channelIds,
      ledger,
      now,
      kind,
      mediaUrl: urls.get("media"),
      thumbUrl: urls.get("thumb"),
      trailerUrl: urls.get("trailer"),
      social: req.social,
      parentLong: long ? { id: long.id, goesPublicAt: long.privacyStatus === "public" ? long.publishedAt : long.publishAt } : null,
      standalone: req.standalone,
      allowLate: req.allowLate,
    });

  // Plan once with stand-in URLs, so a refused video never gets its files uploaded.
  const standIn = (f: (typeof files)[number]) => `${DRY_HOST}/${video.id}-${f.role}${path.extname(f.localPath ?? "").toLowerCase()}`;
  for (const f of files) urls.set(f.role, f.url ?? (f.localPath ? standIn(f) : undefined));
  let plan = planWith();
  const hosted: string[] = [];
  // Dry, or no Buffer key: plan only, and upload nothing.
  if (plan.errors.length || req.dryRun || !deps.client) {
    return { plan, results: [], sent: false, hosted };
  }

  // Upload only the files a new post will actually use.
  const creates = JSON.stringify(plan.actions.filter((a) => a.action === "create_post"));
  const used = files.filter((f) => urls.get(f.role) && creates.includes(urls.get(f.role)!));
  const toHost = used.filter((f) => !f.url && f.localPath);
  if (toHost.length && !deps.host) {
    plan.errors.push("No Blob store token (BLOB_READ_WRITE_TOKEN), so the media can't be hosted");
    plan.actions = [];
    return { plan, results: [], sent: false, hosted };
  }
  // A file we uploaded but no post will use is deleted again straight away.
  const dropHosted = async () => {
    if (deps.deleteMedia) for (const u of hosted) await deps.deleteMedia(u).catch(() => undefined);
  };
  try {
    for (const f of toHost) {
      const suffix = f.role === "media" ? "" : `-${f.role}`;
      const url = await deps.host!(f.localPath!, `social/${video.id}${suffix}${path.extname(f.localPath!).toLowerCase()}`);
      hosted.push(url);
      urls.set(f.role, url);
    }
  } catch (e) {
    await dropHosted();
    throw e;
  }
  if (toHost.length) plan = planWith();
  for (const f of used) {
    const problem = await deps.checkUrl(urls.get(f.role)!, f.want);
    if (problem) plan.errors.push(problem);
  }
  if (plan.errors.length) {
    plan.actions = [];
    await dropHosted();
    return { plan, results: [], sent: false, hosted };
  }
  const results = await executeActions(plan, deps.client, deps.store);
  if (hosted.length) {
    if (results.some((r) => r.ok && r.action === "create_post")) {
      const current = await deps.store.load();
      await deps.store.setMedia(video.id, [...entryMedia(current.videos[video.id]), ...hosted]);
    } else await dropHosted();
  }
  return { plan, results, sent: true, hosted };
}

export type CheckOutcome = {
  checked: number;
  changes: { videoId: string; kind: "short" | "long"; title: string; timing: Plan["timing"]; actions: PlanAction[]; results: ActionResult[] }[];
  /** Scheduled uploads that weren't in Buffer and were mirrored (or, dry, would be) by this run. */
  autoMirrored: { videoId: string; title: string; source: string; sent: boolean; results: ActionResult[]; warnings: string[] }[];
  /** Scheduled uploads still not in Buffer, and why. */
  unmirrored: { videoId: string; title: string; publishAt: string | null; reason: string }[];
  /** Blob copies removed (or, dry, that would be) because Buffer no longer needs them. */
  mediaCleaned: { videoId: string; url: string; reason: string; deleted: boolean; error?: string }[];
  sent: boolean;
};

/**
 * Delete the Blob copies Buffer no longer needs: every post for the video has been sent
 * (or is gone), the video's posts were all removed, or it went public more than 14 days ago.
 * A post that errored keeps its copy (so it can be retried) until the 14 days are up.
 */
async function cleanMedia(
  before: Ledger,
  deps: MirrorDeps,
  now: Date,
  send: boolean,
): Promise<CheckOutcome["mediaCleaned"]> {
  const out: CheckOutcome["mediaCleaned"] = [];
  const after = await deps.store.load();
  const candidates: { videoId: string; url: string; reason: string }[] = [];
  const media = (id: string) => entryMedia(after.videos[id]);
  // Files the record doesn't know about: link them to their video, or sweep them once old.
  if (deps.listMedia) {
    const known = new Set(Object.keys(after.videos).flatMap(media));
    for (const blob of await deps.listMedia()) {
      if (known.has(blob.url)) continue;
      const id = videoIdFromBlobPath(blob.pathname);
      const entry = id ? after.videos[id] : undefined;
      if (id && entry) {
        // A copy uploaded for a video that is in Buffer: keep it with that video's posts.
        const next = [...media(id), blob.url];
        entry.media = next.length === 1 ? next[0] : next;
        known.add(blob.url);
        if (send) await deps.store.setMedia(id, next);
      } else if (now.getTime() - blob.uploadedAt.getTime() > ORPHAN_AGE_MS) {
        candidates.push({ videoId: id ?? "?", url: blob.url, reason: "orphaned: no Buffer post uses it" });
      }
    }
  }
  for (const [id, entry] of Object.entries(before.videos)) {
    if (!after.videos[id]) for (const url of entryMedia(entry)) candidates.push({ videoId: id, url, reason: "its Buffer posts were removed" });
  }
  for (const [id, entry] of Object.entries(after.videos)) {
    const urls = media(id);
    if (!urls.length) continue;
    const recorded = Object.values(entry.channels).map((c) => c!.recordedAt);
    const since = entry.dueAt ?? recorded.sort().at(-1) ?? null;
    if (since && now.getTime() - Date.parse(since) > MEDIA_MAX_AGE_MS) {
      for (const url of urls) candidates.push({ videoId: id, url, reason: "went public more than 14 days ago" });
      continue;
    }
    if (!deps.client) continue;
    // Nothing can have been sent before it's due: don't spend Buffer's request limit asking.
    const due = entry.mode === "shareNow" || (entry.dueAt !== null && Date.parse(entry.dueAt) <= now.getTime());
    if (!due) continue;
    const statuses = await Promise.all(
      Object.values(entry.channels).map((c) => deps.client!.getPostStatus(c!.postId).catch(() => "unknown")),
    );
    if (statuses.length && statuses.every((st) => st === "sent" || st === null)) {
      for (const url of urls) candidates.push({ videoId: id, url, reason: "every Buffer post has been sent" });
    }
  }
  for (const c of candidates) {
    if (!isOwnBlobUrl(c.url)) continue;
    if (!send || !deps.deleteMedia) {
      out.push({ ...c, deleted: false });
      continue;
    }
    try {
      await deps.deleteMedia(c.url);
      if (after.videos[c.videoId]) {
        const rest = media(c.videoId).filter((u) => u !== c.url);
        const e = after.videos[c.videoId];
        if (rest.length) e.media = rest.length === 1 ? rest[0] : rest;
        else delete e.media;
        await deps.store.setMedia(c.videoId, rest);
      }
      out.push({ ...c, deleted: true });
    } catch (e) {
      out.push({ ...c, deleted: false, error: (e as Error).message });
    }
  }
  return out;
}

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
  const autoMirrored: CheckOutcome["autoMirrored"] = [];
  const unmirrored: CheckOutcome["unmirrored"] = [];
  const mirrorFound = async (v: YouTubeVideo, needsRegistry: boolean) => {
    const miss = (reason: string) => unmirrored.push({ videoId: v.id, title: v.title, publishAt: v.publishAt, reason });
    const hint = deps.findMedia?.(v.id) ?? null;
    if (!hint || (needsRegistry && !hint.registered)) {
      miss(
        needsRegistry
          ? `went public without a schedule and isn't in social/UPLOADS.json: if it should go to social, run buffer-mirror.ts mirror --video ${v.id} … within 24 h of going public`
          : `no local file recorded: run buffer-mirror.ts register --video ${v.id} --media <mp4> --long <longId> (or --thumb <jpg> for a long)`,
      );
      return;
    }
    try {
      const outcome = await mirrorVideo(
        {
          videoId: v.id,
          longId: hint.longId,
          standalone: hint.standalone,
          mediaPath: hint.mediaPath,
          thumbPath: hint.thumbPath,
          trailerPath: hint.trailerPath,
          social: hint.social,
          dryRun: !send,
        },
        deps,
      );
      if (outcome.plan.errors.length) {
        miss(`${outcome.plan.errors.join("; ")} (from ${hint.source})`);
        return;
      }
      autoMirrored.push({ videoId: v.id, title: v.title, source: hint.source, sent: outcome.sent, results: outcome.results, warnings: outcome.plan.warnings });
    } catch (e) {
      miss((e as Error).message);
    }
  };
  const scheduled = await deps.listScheduled(token, now);
  for (const v of scheduled.filter((x) => !ledger.videos[x.id])) await mirrorFound(v, false);
  // Went public without a schedule, or after yesterday's check: shared now, but only for an
  // upload this pipeline knows (UPLOADS.json), so an old video made public again never reaches social.
  if (deps.listRecentlyPublic) {
    const seen = new Set(scheduled.map((v) => v.id));
    for (const v of await deps.listRecentlyPublic(token, now)) {
      if (!ledger.videos[v.id] && !seen.has(v.id)) await mirrorFound(v, true);
    }
  }

  const mediaCleaned = await cleanMedia(ledger, deps, now, send);

  return { checked: ids.length, changes, autoMirrored, unmirrored, mediaCleaned, sent: send };
}
