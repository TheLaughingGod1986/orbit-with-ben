/**
 * Buffer mirror (STUDIO_PLAYBOOK.md §12, added 27 Sep 2026).
 *
 * Every YouTube upload is mirrored to Instagram, Facebook and Threads through Buffer,
 * at exactly the time the video goes public on YouTube, with the same title, the
 * description's opening paragraph and the tags as hashtags. This module turns the live
 * YouTube record into Buffer `create_post` inputs. It makes no network calls: the CLI
 * (`scripts/buffer-mirror.ts`) fetches YouTube and an agent sends the plan through the
 * Buffer MCP (`https://mcp.buffer.com/mcp`).
 *
 * Nothing else posts to social. The app's own Meta/Threads/TikTok/X adapters are
 * blocked in the publishing worker (`isBufferOnlyPlatform`).
 */

export const BUFFER_CHANNELS = ["instagram", "facebook", "threads"] as const;
export type BufferChannel = (typeof BUFFER_CHANNELS)[number];

/** App platforms that no longer publish directly. Social goes through Buffer. */
const BUFFER_ONLY_PLATFORMS = new Set([
  "meta",
  "instagram_reels",
  "instagram_feed",
  "facebook_reels",
  "facebook_page",
  "threads",
  "tiktok",
  "x",
]);

export function isBufferOnlyPlatform(platform: string): boolean {
  return BUFFER_ONLY_PLATFORMS.has(platform);
}

/** Hashtags per post. Instagram caps at 5; Threads takes one topic tag. */
export const HASHTAG_LIMIT: Record<BufferChannel, number> = { instagram: 5, facebook: 3, threads: 1 };
export const TEXT_LIMIT: Record<BufferChannel, number> = { instagram: 2200, facebook: 5000, threads: 500 };

/** A Short is anything this short; the channel's Shorts are under 40 s. */
export const SHORT_MAX_SECONDS = 60;
/** Buffer needs a future time. Closer than this, wait until the video is public and mirror it then. */
export const MIN_LEAD_MS = 10 * 60 * 1000;
/** A video public for longer than this is back catalogue, not a new upload. */
export const LATE_WINDOW_MS = 24 * 60 * 60 * 1000;

export type YouTubeVideo = {
  id: string;
  title: string;
  description: string;
  tags: string[];
  durationSeconds: number;
  privacyStatus: "public" | "private" | "unlisted" | string;
  /** Scheduled go-public time (private videos only). */
  publishAt: string | null;
  /** When YouTube published it (public videos). */
  publishedAt: string | null;
  containsSyntheticMedia: boolean;
};

export type LedgerEntry = {
  kind: "short" | "long";
  title: string;
  dueAt: string | null;
  mode: "customScheduled" | "shareNow";
  channels: Partial<Record<BufferChannel, { postId: string; recordedAt: string }>>;
  /** Public Blob copy of the video or thumbnail. Deleted once Buffer has sent every post. */
  media?: string;
};

export type Ledger = { version: 1; videos: Record<string, LedgerEntry> };

export type ChannelIds = Partial<Record<BufferChannel, string>>;

export type PlanAction =
  | { action: "create_post"; channel: BufferChannel; input: Record<string, unknown> }
  | { action: "edit_post"; channel: BufferChannel; input: { postId: string; mode: "customScheduled"; dueAt: string } }
  | { action: "delete_post"; channel: BufferChannel; input: { postId: string } }
  | { action: "skip"; channel: BufferChannel; reason: string };

export type Plan = {
  videoId: string;
  kind: "short" | "long";
  title: string;
  youtubeUrl: string;
  timing: { mode: "customScheduled"; dueAt: string } | { mode: "shareNow"; dueAt: null } | { mode: "none"; reason: string };
  actions: PlanAction[];
  errors: string[];
  warnings: string[];
};

export type PlanOptions = {
  video: YouTubeVideo;
  channelIds: ChannelIds;
  ledger: Ledger;
  now: Date;
  kind?: "short" | "long";
  /** Public URL of the Short's mp4 (required for Shorts). */
  mediaUrl?: string;
  /** Public URL of the long's thumbnail (Instagram image post for longs). */
  thumbUrl?: string;
  /** The long this Short belongs to. A Short never goes out before its long is public. */
  parentLong?: { id: string; goesPublicAt: string | null } | null;
  /** The Short has no long (e.g. a Wednesday test Short). */
  standalone?: boolean;
  /** Mirror a video that has been public for more than a day. */
  allowLate?: boolean;
};

export function isShort(video: YouTubeVideo, kind?: "short" | "long"): boolean {
  if (kind) return kind === "short";
  return video.durationSeconds > 0 && video.durationSeconds <= SHORT_MAX_SECONDS;
}

/** ISO 8601 duration (PT1M5S) to seconds. */
export function parseIsoDuration(value: string | undefined | null): number {
  const m = /^P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?$/.exec(value || "");
  if (!m) return 0;
  const [, d, h, min, s] = m;
  return Number(d || 0) * 86400 + Number(h || 0) * 3600 + Number(min || 0) * 60 + Number(s || 0);
}

const URL_RE = /https?:\/\/\S+/gi;

/** The description's opening paragraph, without links, chapters or source lists. */
export function openingParagraph(description: string): string {
  const paragraphs = description
    .split(/\n\s*\n/)
    .map((p) => p.replace(URL_RE, "").replace(/\s+/g, " ").trim())
    .filter(Boolean);
  const first = paragraphs.find(
    (p) => !/^(\d{1,2}:)?\d{1,2}:\d{2}\b/.test(p) && !/^(sources?|references?|chapters?|music|credits?)\b/i.test(p) && !p.startsWith("#"),
  );
  return first ?? "";
}

export function toHashtag(tag: string): string | null {
  const words = tag
    .normalize("NFKD")
    .replace(/[^\p{L}\p{N}\s]/gu, " ")
    .split(/\s+/)
    .filter(Boolean);
  if (!words.length) return null;
  const body = words.map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join("");
  if (body.length > 30 || /^\d+$/.test(body)) return null;
  return `#${body}`;
}

export function hashtags(tags: string[], limit: number): string[] {
  const out: string[] = [];
  const seen = new Set<string>();
  for (const tag of tags) {
    const h = toHashtag(tag);
    if (!h || seen.has(h.toLowerCase())) continue;
    seen.add(h.toLowerCase());
    out.push(h);
    if (out.length >= limit) break;
  }
  return out;
}

function fit(parts: { title: string; body: string; tail: string[] }, limit: number): string {
  const tail = parts.tail.filter(Boolean);
  const join = (body: string) => [parts.title, body, ...tail].filter(Boolean).join("\n\n");
  let text = join(parts.body);
  if (text.length <= limit) return text;
  const room = limit - join("").length - 2;
  const body = room > 20 ? parts.body.slice(0, room - 1).replace(/\s+\S*$/, "") + "…" : "";
  text = join(body);
  return text.length <= limit ? text : text.slice(0, limit);
}

export function buildText(video: YouTubeVideo, channel: BufferChannel, kind: "short" | "long"): string {
  const tags = hashtags(video.tags, HASHTAG_LIMIT[channel]).join(" ");
  const lead = kind === "long" && channel === "instagram" ? "New film on YouTube. Link in bio." : "";
  return fit({ title: video.title.trim(), body: openingParagraph(video.description), tail: [lead, tags] }, TEXT_LIMIT[channel]);
}

export function checkPublicUrl(url: string | undefined, what: string): string | null {
  if (!url) return `${what}: no URL given`;
  let parsed: URL;
  try {
    parsed = new URL(url);
  } catch {
    return `${what}: not a URL`;
  }
  if (parsed.protocol !== "https:") return `${what}: must be https`;
  if (/(^|\.)(drive\.google\.com|docs\.google\.com|dropbox\.com|icloud\.com|youtube\.com|youtu\.be)$/i.test(parsed.hostname)) {
    return `${what}: ${parsed.hostname} is a share page, not a direct file. Host it on Vercel Blob (public) or Cloudinary.`;
  }
  if (/[?&](X-Amz-Signature|Signature|Expires|se|sig)=/i.test(parsed.search)) {
    return `${what}: signed URLs expire before the post goes out. Use a permanent public URL.`;
  }
  return null;
}

/** When the video goes public on YouTube, or why it can't be mirrored. */
export function resolveTiming(
  video: YouTubeVideo,
  now: Date,
  allowLate = false,
): Plan["timing"] {
  if (video.privacyStatus === "public") {
    const since = video.publishedAt ? now.getTime() - Date.parse(video.publishedAt) : Infinity;
    if (since > LATE_WINDOW_MS && !allowLate) {
      return { mode: "none", reason: "public for more than a day; this is back catalogue (pass --allow-late after Ben's OK)" };
    }
    return { mode: "shareNow", dueAt: null };
  }
  if (video.privacyStatus === "private" && video.publishAt) {
    const lead = Date.parse(video.publishAt) - now.getTime();
    if (lead < MIN_LEAD_MS) {
      return { mode: "none", reason: "goes public in under 10 minutes; rerun once it is public" };
    }
    return { mode: "customScheduled", dueAt: new Date(video.publishAt).toISOString() };
  }
  return { mode: "none", reason: `YouTube status is ${video.privacyStatus} with no scheduled publish time; nothing to mirror` };
}

function createInput(opts: {
  video: YouTubeVideo;
  channel: BufferChannel;
  channelId: string;
  kind: "short" | "long";
  timing: Extract<Plan["timing"], { mode: "customScheduled" | "shareNow" }>;
  mediaUrl?: string;
  thumbUrl?: string;
  youtubeUrl: string;
}): Record<string, unknown> {
  const { video, channel, kind } = opts;
  const input: Record<string, unknown> = {
    channelId: opts.channelId,
    schedulingType: "automatic",
    mode: opts.timing.mode,
    text: buildText(video, channel, kind),
  };
  if (opts.timing.mode === "customScheduled") input.dueAt = opts.timing.dueAt;

  if (kind === "short") {
    const video0 = { video: { url: opts.mediaUrl, ...(channel === "instagram" ? { metadata: { thumbnailOffset: 0 } } : {}) } };
    input.assets = [video0];
    if (channel === "instagram") {
      input.metadata = { instagram: { type: "reel", shouldShareToFeed: true, isAiGenerated: video.containsSyntheticMedia } };
    } else if (channel === "facebook") {
      input.metadata = { facebook: { type: "reel" } };
    }
    return input;
  }

  // Longs: a YouTube link card on Facebook and Threads; the thumbnail as an image on Instagram.
  if (channel === "instagram") {
    input.assets = [{ image: { url: opts.thumbUrl, metadata: { altText: video.title } } }];
    input.metadata = { instagram: { type: "post", shouldShareToFeed: true, isAiGenerated: video.containsSyntheticMedia } };
  } else if (channel === "facebook") {
    input.assets = [];
    input.metadata = { facebook: { type: "post", linkAttachment: { url: opts.youtubeUrl } } };
  } else {
    input.assets = [];
    input.metadata = { threads: { linkAttachment: { url: opts.youtubeUrl } } };
  }
  return input;
}

export function planBufferMirror(opts: PlanOptions): Plan {
  const { video, ledger, channelIds, now } = opts;
  const kind = isShort(video, opts.kind) ? "short" : "long";
  const youtubeUrl = kind === "short" ? `https://youtube.com/shorts/${video.id}` : `https://youtu.be/${video.id}`;
  const timing = resolveTiming(video, now, opts.allowLate);
  const errors: string[] = [];
  const warnings: string[] = [];
  const actions: PlanAction[] = [];
  const entry = ledger.videos[video.id];

  if (timing.mode === "none") {
    // Already mirrored: only keep Buffer in step (moved time, or no longer going public).
    if (entry) {
      actions.push(...reconcileEntry(video.id, entry, video, now));
      warnings.push(timing.reason);
    } else {
      errors.push(timing.reason);
    }
    return { videoId: video.id, kind, title: video.title, youtubeUrl, timing, actions, errors, warnings };
  }

  // Media and the long-first rule only matter when something new is being posted.
  const needsCreate = BUFFER_CHANNELS.some((c) => !entry?.channels[c]);
  if (kind === "short" && needsCreate) {
    const mediaErr = checkPublicUrl(opts.mediaUrl, "--media-url");
    if (mediaErr) errors.push(mediaErr);
    if (!opts.standalone) {
      if (!opts.parentLong) {
        errors.push("A Short needs --long <youtube id> (or --standalone for a Short with no long)");
      } else {
        const longAt = opts.parentLong.goesPublicAt ? Date.parse(opts.parentLong.goesPublicAt) : NaN;
        const shortAt = timing.mode === "customScheduled" ? Date.parse(timing.dueAt) : now.getTime();
        if (Number.isNaN(longAt)) {
          errors.push(`Long ${opts.parentLong.id} is not public or scheduled; a Short never goes out before its long`);
        } else if (shortAt < longAt) {
          errors.push(`Short goes public before its long ${opts.parentLong.id}; move the Short on YouTube first`);
        }
      }
    }
  } else if (!entry?.channels.instagram) {
    const thumbErr = checkPublicUrl(opts.thumbUrl, "--thumb-url");
    if (thumbErr) warnings.push(`${thumbErr}; Instagram is skipped for this long`);
  }

  for (const channel of BUFFER_CHANNELS) {
    const rec = entry?.channels[channel];
    if (rec) {
      if (timing.mode === "customScheduled" && entry?.dueAt !== timing.dueAt) {
        actions.push({ action: "edit_post", channel, input: { postId: rec.postId, mode: "customScheduled", dueAt: timing.dueAt } });
      } else {
        actions.push({ action: "skip", channel, reason: "already in Buffer for this video" });
      }
      continue;
    }
    const channelId = channelIds[channel];
    if (!channelId) {
      errors.push(`No Buffer channel id for ${channel} in social/BUFFER_CHANNELS.json`);
      continue;
    }
    if (kind === "long" && channel === "instagram" && checkPublicUrl(opts.thumbUrl, "--thumb-url")) {
      actions.push({ action: "skip", channel, reason: "no public thumbnail URL" });
      continue;
    }
    actions.push({
      action: "create_post",
      channel,
      input: createInput({ video, channel, channelId, kind, timing, mediaUrl: opts.mediaUrl, thumbUrl: opts.thumbUrl, youtubeUrl }),
    });
  }

  if (errors.length) {
    // Never hand over a half-valid plan.
    return { videoId: video.id, kind, title: video.title, youtubeUrl, timing, actions: [], errors, warnings };
  }
  return { videoId: video.id, kind, title: video.title, youtubeUrl, timing, actions, errors, warnings };
}

/** Record what Buffer returned, so the same video is never posted twice. */
export function recordPost(
  ledger: Ledger,
  plan: Pick<Plan, "videoId" | "kind" | "title" | "timing">,
  channel: BufferChannel,
  postId: string | null,
  now: Date,
): Ledger {
  const prev = ledger.videos[plan.videoId];
  const dueAt = plan.timing.mode === "customScheduled" ? plan.timing.dueAt : prev?.dueAt ?? null;
  const channels = { ...(prev?.channels ?? {}) };
  if (postId) channels[channel] = { postId, recordedAt: now.toISOString() };
  else delete channels[channel];
  const videos = { ...ledger.videos };
  if (Object.keys(channels).length === 0) {
    delete videos[plan.videoId];
  } else {
    videos[plan.videoId] = {
      kind: plan.kind,
      title: plan.title,
      dueAt,
      mode: plan.timing.mode === "shareNow" ? "shareNow" : prev?.mode ?? "customScheduled",
      channels,
      ...(prev?.media ? { media: prev.media } : {}),
    };
  }
  return { ...ledger, videos };
}

/** Remember (or forget, with null) the Blob copy behind a mirrored video. */
export function setEntryMedia(ledger: Ledger, videoId: string, url: string | null): Ledger {
  const prev = ledger.videos[videoId];
  if (!prev) return ledger;
  const next: LedgerEntry = { ...prev };
  if (url) next.media = url;
  else delete next.media;
  return { ...ledger, videos: { ...ledger.videos, [videoId]: next } };
}

/** Keep a Blob copy while any post may still need it; 14 days after go-public it goes regardless. */
export const MEDIA_MAX_AGE_MS = 14 * 24 * 60 * 60 * 1000;

/**
 * Keep Buffer in step with YouTube after the fact: a moved publish time moves the
 * Buffer posts, and a video that no longer goes public takes them down.
 */
export function reconcileEntry(videoId: string, entry: LedgerEntry, video: YouTubeVideo | null, now: Date): PlanAction[] {
  const recorded = BUFFER_CHANNELS.filter((c) => entry.channels[c]);
  const alreadyOut = entry.mode === "shareNow" || (entry.dueAt !== null && Date.parse(entry.dueAt) <= now.getTime());
  if (alreadyOut) return [];
  if (video && video.id !== videoId) throw new Error(`reconcile: ${video.id} is not ${videoId}`);
  if (video?.privacyStatus === "public") return [];
  if (video?.privacyStatus === "private" && video.publishAt) {
    const dueAt = new Date(video.publishAt).toISOString();
    if (dueAt === entry.dueAt || Date.parse(dueAt) <= now.getTime()) return [];
    return recorded.map((channel) => ({
      action: "edit_post",
      channel,
      input: { postId: entry.channels[channel]!.postId, mode: "customScheduled", dueAt },
    }));
  }
  // Gone, or no longer scheduled to go public: take the Buffer posts down.
  return recorded.map((channel) => ({ action: "delete_post", channel, input: { postId: entry.channels[channel]!.postId } }));
}
