#!/usr/bin/env tsx
/**
 * Full YouTube catalogue forensic inventory + classification (read-only).
 *
 *   npm run youtube:forensic-inventory
 *   npm run youtube:forensic-inventory -- --out ../00_Brand/.../youtube_cleanup_2026-08-07
 *
 * Does NOT mutate YouTube. Writes BEFORE_REPAIR inventory + maps + plan drafts.
 */
import fs from "fs";
import path from "path";
import { createHash } from "crypto";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";
import { loadCanonicalRegistry } from "../src/lib/publishing/youtube-registry";
import { loadYouTubeRecoveryConfig } from "../src/lib/publishing/youtube-recovery";

function arg(name: string): string | undefined {
  const i = process.argv.indexOf(`--${name}`);
  return i === -1 ? undefined : process.argv[i + 1];
}

const DEFAULT_OUT = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07",
);

const CHANNEL_ID = "UC_esArsDKd3GJvOkeO0DUog";

/** Approved canonical shelf from FINAL_SHELF_VERIFY / REPORT.md (post smooth-CFR quarantine). */
const APPROVED_CANONICAL: Record<
  string,
  { contentId: string; family: string; contentType: "longform" | "shorts"; role: string }
> = {
  Mo93x0fxB1Q: {
    contentId: "v001-fermi-long",
    family: "FERMI",
    contentType: "longform",
    role: "canonical_long",
  },
  "1HuV8o3gOss": {
    contentId: "v001-fermi-short-01",
    family: "FERMI",
    contentType: "shorts",
    role: "canonical_short",
  },
  KcKBixwmcV4: {
    contentId: "v001-fermi-short-02",
    family: "FERMI",
    contentType: "shorts",
    role: "canonical_short",
  },
  "3xrxdmaOwJI": {
    contentId: "v002-bh-long",
    family: "BLACK_HOLE",
    contentType: "longform",
    role: "canonical_long",
  },
  JRfhE6yWom4: {
    contentId: "v002-bh-short-01",
    family: "BLACK_HOLE",
    contentType: "shorts",
    role: "canonical_short",
  },
  L2OFjL4neOo: {
    contentId: "v002-bh-short-02",
    family: "BLACK_HOLE",
    contentType: "shorts",
    role: "canonical_short",
  },
  tUAdhOnMW2g: {
    contentId: "v002-bh-nf01",
    family: "BLACK_HOLE",
    contentType: "shorts",
    role: "canonical_scheduled",
  },
};

/** Verified HIGH duplicates of approved canonicals (from prior audit + fingerprint groups). */
const VERIFIED_DUPLICATES: Record<
  string,
  { of: string; contentId: string; family: string; reason: string }
> = {
  RCs6MMxF3ko: {
    of: "3xrxdmaOwJI",
    contentId: "v002-bh-long",
    family: "BLACK_HOLE",
    reason: "Competing smooth-CFR BH long; same title+duration fingerprint as canonical 3xrxdmaOwJI",
  },
  IwpO33AJaPQ: {
    of: "JRfhE6yWom4",
    contentId: "v002-bh-short-01",
    family: "BLACK_HOLE",
    reason: "Smooth-CFR replace of event-horizon Short; demotes canonical JRfhE6yWom4",
  },
  IqII5mVGdrs: {
    of: "L2OFjL4neOo",
    contentId: "v002-bh-short-02",
    family: "BLACK_HOLE",
    reason: "Same-title falling Short held as Dec 31 duplicate of public L2OFjL4neOo",
  },
  "2C-eiSMsBLc": {
    of: "tUAdhOnMW2g",
    contentId: "v002-bh-nf01",
    family: "BLACK_HOLE",
    reason: "Same-slot NF01 duplicate held to 31 Dec",
  },
  lIHb_tyxQSM: {
    of: "svYOx07OrIM",
    contentId: "v002-bh-nf-look-back",
    family: "BLACK_HOLE",
    reason: "Zero-tag replace-batch twin of Would You Look Back",
  },
  wOlnj7nZWJM: {
    of: "B2STcIAF1lY",
    contentId: "v002-bh-nf02",
    family: "BLACK_HOLE",
    reason: "Zero-tag replace-batch twin of What You Would See",
  },
  "2uT3wXJLybw": {
    of: "w1ej9u0rPTA",
    contentId: "v002-bh-nf-point",
    family: "BLACK_HOLE",
    reason: "Zero-tag replace-batch twin of Point of No Return",
  },
};

const HELD_DEC31 = new Set([
  "2C-eiSMsBLc",
  "IqII5mVGdrs",
  "lIHb_tyxQSM",
  "wOlnj7nZWJM",
  "2uT3wXJLybw",
]);

const RECOVERY_SCHEDULED_CANONICAL = [
  { id: "tUAdhOnMW2g", day: "2026-08-07", title: "Time Appears to Stop at a Black Hole" },
  { id: "svYOx07OrIM", day: "2026-08-08", title: "Would You Look Back?" },
  { id: "B2STcIAF1lY", day: "2026-08-09", title: "What You Would See Falling Into a Black Hole" },
  { id: "w1ej9u0rPTA", day: "2026-08-10", title: "The Point of No Return Explained" },
];

type YtVideo = {
  videoId: string;
  title: string;
  description: string;
  privacyStatus: string;
  publishAt: string | null;
  publishedAt: string | null;
  duration: string | null;
  categoryId: string | null;
  defaultLanguage: string | null;
  defaultAudioLanguage: string | null;
  madeForKids: boolean | null;
  selfDeclaredMadeForKids: boolean | null;
  embeddable: boolean | null;
  license: string | null;
  tags: string[];
  thumbnails: Record<string, { url: string; width?: number; height?: number }>;
  uploadStatus: string | null;
  processingStatus: string | null;
  viewCount: number;
  likeCount: number;
  commentCount: number;
  contentType: "shorts" | "longform" | "unknown";
  titleDurationFingerprint: string;
};

function parseDurationSeconds(iso: string | null | undefined): number | null {
  if (!iso) return null;
  const m = iso.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
  if (!m) return null;
  return (
    (parseInt(m[1] || "0", 10) || 0) * 3600 +
    (parseInt(m[2] || "0", 10) || 0) * 60 +
    (parseInt(m[3] || "0", 10) || 0)
  );
}

function normalizeTitle(t: string): string {
  return t
    .toLowerCase()
    .replace(/[#|]/g, " ")
    .replace(/[^a-z0-9]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function classifyContentType(duration: string | null, title: string): "shorts" | "longform" | "unknown" {
  const s = parseDurationSeconds(duration);
  if (s != null && s > 0 && s <= 60) return "shorts";
  if (s != null && s > 60) return "longform";
  if (/#shorts/i.test(title)) return "shorts";
  return "unknown";
}

async function getToken(): Promise<string> {
  getEnv();
  const connection = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!connection?.accessTokenEncrypted) throw new Error("No YouTube connection");
  const adapter = new YouTubePublishingAdapter();
  if (
    connection.accessTokenExpiresAt &&
    connection.accessTokenExpiresAt.getTime() < Date.now() + 60_000 &&
    adapter.refreshConnection
  ) {
    await adapter.refreshConnection(connection);
  }
  const fresh = await prisma.platformConnection.findUnique({ where: { id: connection.id } });
  return decryptSecret(fresh!.accessTokenEncrypted!);
}

async function ytGet(token: string, url: string): Promise<any> {
  const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  const body = await res.json();
  if (!res.ok) {
    throw new Error(`YouTube API ${res.status}: ${JSON.stringify(body).slice(0, 500)}`);
  }
  return body;
}

async function listAllUploadIds(token: string): Promise<{ ids: string[]; channel: any }> {
  const ch = await ytGet(
    token,
    "https://www.googleapis.com/youtube/v3/channels?part=contentDetails,snippet,statistics,status&mine=true",
  );
  const channel = ch.items?.[0];
  if (!channel) throw new Error("No channel for mine=true");
  const uploadsPlaylistId = channel.contentDetails?.relatedPlaylists?.uploads;
  const ids: string[] = [];
  let pageToken = "";
  do {
    const url =
      `https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId=${uploadsPlaylistId}` +
      (pageToken ? `&pageToken=${pageToken}` : "");
    const page = await ytGet(token, url);
    for (const it of page.items || []) {
      const id = it.contentDetails?.videoId;
      if (id) ids.push(id);
    }
    pageToken = page.nextPageToken || "";
  } while (pageToken);
  return { ids, channel };
}

async function fetchVideos(token: string, ids: string[]): Promise<YtVideo[]> {
  const out: YtVideo[] = [];
  for (let i = 0; i < ids.length; i += 50) {
    const chunk = ids.slice(i, i + 50);
    const body = await ytGet(
      token,
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails,statistics,processingDetails&id=${chunk.join(",")}`,
    );
    for (const it of body.items || []) {
      const duration = it.contentDetails?.duration || null;
      const title = it.snippet?.title || "";
      const contentType = classifyContentType(duration, title);
      const fp = `${normalizeTitle(title)}|${duration || "?"}`;
      out.push({
        videoId: it.id,
        title,
        description: it.snippet?.description || "",
        privacyStatus: it.status?.privacyStatus || "unknown",
        publishAt: it.status?.publishAt || null,
        publishedAt: it.snippet?.publishedAt || null,
        duration,
        categoryId: it.snippet?.categoryId || null,
        defaultLanguage: it.snippet?.defaultLanguage || null,
        defaultAudioLanguage: it.snippet?.defaultAudioLanguage || null,
        madeForKids: it.status?.madeForKids ?? null,
        selfDeclaredMadeForKids: it.status?.selfDeclaredMadeForKids ?? null,
        embeddable: it.status?.embeddable ?? null,
        license: it.status?.license || null,
        tags: it.snippet?.tags || [],
        thumbnails: it.snippet?.thumbnails || {},
        uploadStatus: it.status?.uploadStatus || null,
        processingStatus: it.processingDetails?.processingStatus || null,
        viewCount: Number(it.statistics?.viewCount || 0),
        likeCount: Number(it.statistics?.likeCount || 0),
        commentCount: Number(it.statistics?.commentCount || 0),
        contentType,
        titleDurationFingerprint: fp,
      });
    }
  }
  return out;
}

function scanLocalContent(repoRoot: string) {
  const projectsRoot = path.join(repoRoot, "02_Video-Projects");
  const episodes: any[] = [];
  if (!fs.existsSync(projectsRoot)) return { episodes, fingerprints: [] as any[] };

  const dirs = fs
    .readdirSync(projectsRoot)
    .filter((d) => /^\d{3}_/.test(d))
    .sort();

  const fingerprints: any[] = [];

  for (const dir of dirs) {
    const epRoot = path.join(projectsRoot, dir);
    const family =
      dir.includes("Aliens") || dir.includes("Fermi")
        ? "FERMI"
        : dir.includes("Black-Hole")
          ? "BLACK_HOLE"
          : dir.includes("Exoplanets")
            ? "EXOPLANETS"
            : dir.includes("JWST")
              ? "JWST"
              : dir.includes("Last-Star")
                ? "LAST_STAR"
                : dir.slice(0, 20);

    const shortsIndexPath = path.join(epRoot, "10_Shorts", "SHORTS_UPLOAD_INDEX.json");
    const shortsIndex = fs.existsSync(shortsIndexPath)
      ? JSON.parse(fs.readFileSync(shortsIndexPath, "utf8"))
      : null;

    const packageDir = path.join(epRoot, "11_Upload-Package");
    const finalExport = path.join(epRoot, "09_Final-Export");
    const mp4s: string[] = [];
    const walk = (p: string, depth = 0) => {
      if (!fs.existsSync(p) || depth > 4) return;
      for (const ent of fs.readdirSync(p, { withFileTypes: true })) {
        if (ent.name.startsWith(".") || ent.name === "node_modules") continue;
        const full = path.join(p, ent.name);
        if (ent.isDirectory()) walk(full, depth + 1);
        else if (/\.mp4$/i.test(ent.name) && !/quarantine|reject|_work_/i.test(full)) {
          mp4s.push(full);
        }
      }
    };
    walk(finalExport);
    walk(path.join(epRoot, "10_Shorts", "06_Final-Exports"));

    for (const mp4 of mp4s.slice(0, 40)) {
      try {
        const st = fs.statSync(mp4);
        if (st.size > 800_000_000) {
          fingerprints.push({
            path: mp4,
            size: st.size,
            sha256: null,
            note: "skipped_large",
          });
          continue;
        }
        // Hash first+last 2MB + size for speed on large masters
        const fd = fs.openSync(mp4, "r");
        const head = Buffer.alloc(Math.min(2_000_000, st.size));
        fs.readSync(fd, head, 0, head.length, 0);
        const tailLen = Math.min(2_000_000, st.size);
        const tail = Buffer.alloc(tailLen);
        fs.readSync(fd, tail, 0, tailLen, Math.max(0, st.size - tailLen));
        fs.closeSync(fd);
        const sha256 = createHash("sha256")
          .update(head)
          .update(tail)
          .update(`|${st.size}|${path.basename(mp4)}`)
          .digest("hex");
        fingerprints.push({ path: mp4, size: st.size, sha256, partial: true });
      } catch (e: any) {
        fingerprints.push({ path: mp4, error: String(e?.message || e).slice(0, 120) });
      }
    }

    const ytIds = new Set<string>();
    const collectIds = (obj: any) => {
      if (!obj || typeof obj !== "object") return;
      for (const [k, v] of Object.entries(obj)) {
        if (
          typeof v === "string" &&
          /^[A-Za-z0-9_-]{11}$/.test(v) &&
          /(youtube|video_id|related)/i.test(k)
        ) {
          ytIds.add(v);
        } else if (typeof v === "object") collectIds(v);
      }
    };
    collectIds(shortsIndex);

    episodes.push({
      dir,
      family,
      packageDir: fs.existsSync(packageDir) ? packageDir : null,
      shortsIndexPath: fs.existsSync(shortsIndexPath) ? shortsIndexPath : null,
      youtubeIdsReferenced: [...ytIds],
      mp4Count: mp4s.length,
      sampleMp4s: mp4s.slice(0, 12),
    });
  }

  return { episodes, fingerprints };
}

function buildDuplicateGroups(videos: YtVideo[]) {
  const byFp = new Map<string, YtVideo[]>();
  for (const v of videos) {
    const list = byFp.get(v.titleDurationFingerprint) || [];
    list.push(v);
    byFp.set(v.titleDurationFingerprint, list);
  }
  return [...byFp.entries()]
    .filter(([, list]) => list.length > 1)
    .map(([fp, list]) => ({
      fingerprint: fp,
      ids: list.map((v) => v.videoId),
      titles: list.map((v) => v.title),
      privacies: list.map((v) => v.privacyStatus),
      publishAts: list.map((v) => v.publishAt),
      views: list.map((v) => v.viewCount),
      confidence: "HIGH" as const,
      signal: "exact_title_duration_fingerprint",
    }));
}

type Classification =
  | "CANONICAL_PUBLIC"
  | "CANONICAL_SCHEDULED"
  | "CANONICAL_PRIVATE"
  | "DUPLICATE_PUBLIC"
  | "DUPLICATE_SCHEDULED"
  | "DUPLICATE_PRIVATE"
  | "BAD_METADATA"
  | "WRONG_UPLOAD"
  | "MISSING_CANONICAL"
  | "PERMANENTLY_DELETED"
  | "UNKNOWN_REQUIRES_REVIEW";

function classifyVideo(v: YtVideo): {
  classification: Classification;
  confidence: string;
  proposedAction: string;
  contentId: string | null;
  family: string | null;
} {
  const approved = APPROVED_CANONICAL[v.videoId];
  const dupe = VERIFIED_DUPLICATES[v.videoId];
  const isScheduled = Boolean(v.publishAt) && v.privacyStatus === "private";
  const isDec31 =
    HELD_DEC31.has(v.videoId) || (v.publishAt || "").startsWith("2026-12-31");

  if (approved) {
    if (v.privacyStatus === "public") {
      return {
        classification: "CANONICAL_PUBLIC",
        confidence: "EXACT",
        proposedAction: "DO_NOT_TOUCH",
        contentId: approved.contentId,
        family: approved.family,
      };
    }
    if (isScheduled || (approved.role === "canonical_scheduled" && v.privacyStatus === "private")) {
      const shouldBePublicNow =
        approved.role !== "canonical_scheduled" && !v.publishAt;
      if (shouldBePublicNow && v.privacyStatus === "private") {
        return {
          classification: "CANONICAL_PRIVATE",
          confidence: "EXACT",
          proposedAction: "RESTORE_PUBLIC — accidentally demoted canonical",
          contentId: approved.contentId,
          family: approved.family,
        };
      }
      return {
        classification: "CANONICAL_SCHEDULED",
        confidence: "EXACT",
        proposedAction: approved.role === "canonical_scheduled" ? "DO_NOT_TOUCH" : "CLEAR_SCHEDULE_THEN_PUBLIC",
        contentId: approved.contentId,
        family: approved.family,
      };
    }
    if (v.privacyStatus === "private") {
      return {
        classification: "CANONICAL_PRIVATE",
        confidence: "EXACT",
        proposedAction: "RESTORE_PUBLIC — accidentally privatized canonical",
        contentId: approved.contentId,
        family: approved.family,
      };
    }
    if (v.privacyStatus === "unlisted") {
      return {
        classification: "CANONICAL_PRIVATE",
        confidence: "HIGH",
        proposedAction: "REVIEW — canonical unexpectedly unlisted",
        contentId: approved.contentId,
        family: approved.family,
      };
    }
  }

  if (dupe) {
    if (v.privacyStatus === "public") {
      return {
        classification: "DUPLICATE_PUBLIC",
        confidence: "HIGH",
        proposedAction: "PRIVATE — verified duplicate of " + dupe.of,
        contentId: dupe.contentId,
        family: dupe.family,
      };
    }
    if (isScheduled && !isDec31) {
      return {
        classification: "DUPLICATE_SCHEDULED",
        confidence: "HIGH",
        proposedAction: "HOLD_TO_2026-12-31 or PRIVATE",
        contentId: dupe.contentId,
        family: dupe.family,
      };
    }
    return {
      classification: "DUPLICATE_PRIVATE",
      confidence: "HIGH",
      proposedAction: isDec31 ? "DO_NOT_TOUCH — already held" : "KEEP_PRIVATE",
      contentId: dupe.contentId,
      family: dupe.family,
    };
  }

  // Recovery-scheduled canonical go-lives (not yet in APPROVED_CANONICAL map as public)
  const recovery = RECOVERY_SCHEDULED_CANONICAL.find((r) => r.id === v.videoId);
  if (recovery) {
    if (v.privacyStatus === "public") {
      return {
        classification: "CANONICAL_PUBLIC",
        confidence: "HIGH",
        proposedAction: "DO_NOT_TOUCH — recovery go-live completed",
        contentId: `v002-bh-${recovery.id}`,
        family: "BLACK_HOLE",
      };
    }
    return {
      classification: "CANONICAL_SCHEDULED",
      confidence: "HIGH",
      proposedAction: "DO_NOT_TOUCH — recovery schedule",
      contentId: `v002-bh-${recovery.id}`,
      family: "BLACK_HOLE",
    };
  }

  // Metadata smell on otherwise unknown
  const badMeta: string[] = [];
  if (/v0\d|DISABLED|tmp_|test_|untitled/i.test(v.title)) badMeta.push("title_leak");
  if (/TODO|placeholder|lorem ipsum|as an ai/i.test(v.description)) badMeta.push("desc_placeholder");
  if (v.contentType === "longform" && v.categoryId && v.categoryId !== "27") badMeta.push("category");
  if (badMeta.length && v.privacyStatus === "public") {
    return {
      classification: "BAD_METADATA",
      confidence: "MEDIUM",
      proposedAction: "MANUAL_REVIEW — " + badMeta.join(","),
      contentId: null,
      family: null,
    };
  }

  return {
    classification: "UNKNOWN_REQUIRES_REVIEW",
    confidence: "LOW",
    proposedAction: "DO_NOT_TOUCH — classify manually",
    contentId: null,
    family: null,
  };
}

function familyFromTitle(title: string): string {
  const t = title.toLowerCase();
  if (/fermi|alien|zoo hypothesis|where is everybody|space is rude/.test(t)) return "FERMI";
  if (/black hole|event horizon|spaghett|falling in|point of no return|time appears/.test(t))
    return "BLACK_HOLE";
  if (/exoplanet|glass rain|diamond|three suns|eyeball/.test(t)) return "EXOPLANETS";
  if (/jwst|james webb|infrared|galaxies appeared/.test(t)) return "JWST";
  if (/last star|heat death/.test(t)) return "LAST_STAR";
  return "OTHER";
}

async function main() {
  const outDir = path.resolve(arg("out") || DEFAULT_OUT);
  fs.mkdirSync(outDir, { recursive: true });
  const repoRoot = path.resolve(process.cwd(), "..");
  const token = await getToken();

  const listed = await listAllUploadIds(token);
  const ids: string[] = listed.ids;
  const channel = listed.channel;
  const videos = await fetchVideos(token, ids);

  const byPrivacy = {
    public: videos.filter((v) => v.privacyStatus === "public").length,
    private: videos.filter((v) => v.privacyStatus === "private" && !v.publishAt).length,
    unlisted: videos.filter((v) => v.privacyStatus === "unlisted").length,
    scheduled: videos.filter((v) => Boolean(v.publishAt)).length,
  };

  const classifications = videos.map((v) => {
    const c = classifyVideo(v);
    return {
      videoId: v.videoId,
      title: v.title,
      content: c.contentId || familyFromTitle(v.title),
      family: c.family || familyFromTitle(v.title),
      currentState: v.publishAt
        ? `scheduled:${v.privacyStatus}:${v.publishAt}`
        : v.privacyStatus,
      classification: c.classification,
      confidence: c.confidence,
      proposedAction: c.proposedAction,
      views: v.viewCount,
      likes: v.likeCount,
      comments: v.commentCount,
      duration: v.duration,
      categoryId: v.categoryId,
      defaultLanguage: v.defaultLanguage,
      defaultAudioLanguage: v.defaultAudioLanguage,
      madeForKids: v.madeForKids,
      tagsCount: v.tags.length,
      contentType: v.contentType,
      fingerprint: v.titleDurationFingerprint,
    };
  });

  const duplicateGroups = buildDuplicateGroups(videos);
  const local = scanLocalContent(repoRoot);
  const registry = loadCanonicalRegistry();
  const recovery = loadYouTubeRecoveryConfig();

  const inventory = {
    generatedAt: new Date().toISOString(),
    channel: {
      id: channel.id,
      title: channel.snippet?.title,
      stats: channel.statistics,
      status: channel.status,
    },
    counts: {
      total: videos.length,
      ...byPrivacy,
      shorts: videos.filter((v) => v.contentType === "shorts").length,
      longform: videos.filter((v) => v.contentType === "longform").length,
    },
    videos,
    classifications,
    duplicateGroups,
    approvedCanonicalIds: Object.keys(APPROVED_CANONICAL),
    verifiedDuplicateIds: Object.keys(VERIFIED_DUPLICATES),
    heldDec31: [...HELD_DEC31],
    recoveryScheduledCanonical: RECOVERY_SCHEDULED_CANONICAL,
    oauthNote:
      "Inventory used youtube.readonly. videos.update requires youtube.force-ssl (currently missing).",
  };

  const beforeJson = path.join(outDir, "FULL_YOUTUBE_INVENTORY_BEFORE_REPAIR.json");
  fs.writeFileSync(beforeJson, JSON.stringify(inventory, null, 2) + "\n");

  const md = [
    "# Full YouTube Inventory — BEFORE REPAIR",
    "",
    `Generated: ${inventory.generatedAt}`,
    "",
    `Channel: ${channel.snippet?.title} (\`${channel.id}\`)`,
    "",
    "## Counts",
    "",
    `| Bucket | Count |`,
    `|--------|------:|`,
    `| Total | ${inventory.counts.total} |`,
    `| Public | ${inventory.counts.public} |`,
    `| Private (no publishAt) | ${inventory.counts.private} |`,
    `| Unlisted | ${inventory.counts.unlisted} |`,
    `| Scheduled (has publishAt) | ${inventory.counts.scheduled} |`,
    `| Shorts (≤60s) | ${inventory.counts.shorts} |`,
    `| Long-form | ${inventory.counts.longform} |`,
    "",
    "## Classification summary",
    "",
    ...summarizeClass(classifications),
    "",
    "## Full classification table",
    "",
    `| Video ID | Content | Current state | Classification | Confidence | Proposed action |`,
    `|----------|---------|---------------|----------------|------------|-----------------|`,
    ...classifications.map(
      (c) =>
        `| ${c.videoId} | ${c.content} | ${c.currentState} | ${c.classification} | ${c.confidence} | ${c.proposedAction.replace(/\|/g, "/")} |`,
    ),
    "",
    `Duplicate fingerprint groups: ${duplicateGroups.length}`,
    "",
  ].join("\n");
  fs.writeFileSync(path.join(outDir, "FULL_YOUTUBE_INVENTORY_BEFORE_REPAIR.md"), md);

  // Local map
  const localMap = {
    generatedAt: new Date().toISOString(),
    episodes: local.episodes,
    fingerprints: local.fingerprints,
    registryRecords: registry.records,
    recovery,
  };
  fs.writeFileSync(path.join(outDir, "LOCAL_YOUTUBE_CONTENT_MAP.json"), JSON.stringify(localMap, null, 2) + "\n");

  // Content families
  const families: Record<string, any> = {};
  for (const c of classifications) {
    const fam = c.family || "OTHER";
    if (!families[fam]) families[fam] = { family: fam, assets: [] };
    families[fam].assets.push({
      videoId: c.videoId,
      contentId: c.content,
      classification: c.classification,
      contentType: c.contentType,
      title: c.title,
    });
  }
  for (const ep of local.episodes) {
    const fam = ep.family;
    if (!families[fam]) families[fam] = { family: fam, assets: [] };
    families[fam].localEpisode = ep.dir;
    families[fam].localYoutubeIds = ep.youtubeIdsReferenced;
  }
  fs.writeFileSync(path.join(outDir, "CONTENT_FAMILIES.json"), JSON.stringify(families, null, 2) + "\n");

  // Canonical asset map
  const canonicalMap = Object.entries(APPROVED_CANONICAL).map(([id, meta]) => {
    const live = videos.find((v) => v.videoId === id);
    const dupes = Object.entries(VERIFIED_DUPLICATES)
      .filter(([, d]) => d.of === id || d.contentId === meta.contentId)
      .map(([did]) => did);
    // Also include verified where of matches
    const more = Object.entries(VERIFIED_DUPLICATES)
      .filter(([, d]) => d.of === id)
      .map(([did]) => did);
    const duplicateVideoIds = [...new Set([...dupes, ...more])];
    const cls = classifications.find((c) => c.videoId === id);
    return {
      contentId: meta.contentId,
      contentFamily: meta.family,
      contentType: meta.contentType,
      canonicalVideoId: id,
      duplicateVideoIds,
      canonicalReason:
        "Approved FINAL_SHELF_VERIFY / REPORT.md / YOUTUBE_CANONICAL_REGISTRY (smooth-CFR path quarantined)",
      confidence: "EXACT",
      recommendedAction: cls?.proposedAction || "DO_NOT_TOUCH",
      livePrivacy: live?.privacyStatus || null,
      livePublishAt: live?.publishAt || null,
      liveViews: live?.viewCount ?? null,
    };
  });
  // Add recovery scheduled shorts as canonical content items
  for (const r of RECOVERY_SCHEDULED_CANONICAL) {
    if (APPROVED_CANONICAL[r.id]) continue;
    const live = videos.find((v) => v.videoId === r.id);
    const twin = Object.entries(VERIFIED_DUPLICATES)
      .filter(([, d]) => d.of === r.id)
      .map(([id]) => id);
    canonicalMap.push({
      contentId: `v002-recovery-${r.id}`,
      contentFamily: "BLACK_HOLE",
      contentType: "shorts",
      canonicalVideoId: r.id,
      duplicateVideoIds: twin,
      canonicalReason: `RECOVERY_7_DAY scheduled go-live ${r.day}`,
      confidence: "HIGH",
      recommendedAction: "DO_NOT_TOUCH — recovery schedule",
      livePrivacy: live?.privacyStatus || null,
      livePublishAt: live?.publishAt || null,
      liveViews: live?.viewCount ?? null,
    });
  }
  fs.writeFileSync(path.join(outDir, "CANONICAL_ASSET_MAP.json"), JSON.stringify({ generatedAt: new Date().toISOString(), records: canonicalMap }, null, 2) + "\n");

  // Proposed repair plan
  const safe: any[] = [];
  const manual: any[] = [];
  const doNotTouch: any[] = [];

  for (const c of classifications) {
    const live = videos.find((v) => v.videoId === c.videoId)!;
    const entry = {
      videoId: c.videoId,
      before: {
        privacy: live.privacyStatus,
        publishAt: live.publishAt,
        title: live.title,
        categoryId: live.categoryId,
        defaultLanguage: live.defaultLanguage,
        defaultAudioLanguage: live.defaultAudioLanguage,
        tagsCount: live.tags.length,
      },
      after: null as any,
      reason: c.proposedAction,
      evidence: c.classification + "/" + c.confidence,
      confidence: c.confidence,
      rollbackMethod: "videos.update privacyStatus/publishAt back to before values (requires force-ssl) or Studio CDP",
    };

    if (c.classification === "DUPLICATE_PUBLIC" && (c.confidence === "HIGH" || c.confidence === "EXACT")) {
      entry.after = { privacy: "private", publishAt: null };
      safe.push(entry);
    } else if (
      c.classification === "CANONICAL_PRIVATE" &&
      APPROVED_CANONICAL[c.videoId] &&
      APPROVED_CANONICAL[c.videoId].role !== "canonical_scheduled" &&
      (c.confidence === "EXACT" || c.confidence === "HIGH")
    ) {
      entry.after = { privacy: "public", publishAt: null };
      safe.push(entry);
    } else if (
      c.classification === "CANONICAL_SCHEDULED" &&
      APPROVED_CANONICAL[c.videoId]?.role === "canonical_long" &&
      live.publishAt
    ) {
      // Canonical long accidentally scheduled — clear schedule + public
      entry.after = { privacy: "public", publishAt: null };
      entry.reason = "CLEAR accidental schedule on canonical long + restore public";
      safe.push(entry);
    } else if (c.proposedAction.startsWith("DO_NOT_TOUCH")) {
      doNotTouch.push(entry);
    } else if (c.classification === "UNKNOWN_REQUIRES_REVIEW" || c.confidence === "MEDIUM" || c.confidence === "LOW") {
      manual.push(entry);
    } else if (c.classification === "DUPLICATE_PRIVATE" || c.classification === "DUPLICATE_SCHEDULED") {
      if (HELD_DEC31.has(c.videoId) || (live.publishAt || "").startsWith("2026-12-31")) {
        doNotTouch.push(entry);
      } else if (c.classification === "DUPLICATE_SCHEDULED") {
        entry.after = { privacy: "private", publishAt: "2026-12-31T11:30:00Z" };
        safe.push(entry);
      } else {
        doNotTouch.push(entry);
      }
    } else {
      manual.push(entry);
    }
  }

  // Metadata repairs for canonicals (category/language only — objective)
  const metadataRepairs: any[] = [];
  for (const id of Object.keys(APPROVED_CANONICAL)) {
    const live = videos.find((v) => v.videoId === id);
    if (!live) continue;
    const changes: string[] = [];
    const after: any = {};
    if (APPROVED_CANONICAL[id].contentType === "longform" && live.categoryId !== "27") {
      changes.push(`categoryId ${live.categoryId} → 27`);
      after.categoryId = "27";
    }
    if (live.defaultLanguage && live.defaultLanguage !== "en-GB") {
      changes.push(`defaultLanguage ${live.defaultLanguage} → en-GB`);
      after.defaultLanguage = "en-GB";
    }
    if (live.defaultAudioLanguage && live.defaultAudioLanguage !== "en-GB") {
      changes.push(`defaultAudioLanguage ${live.defaultAudioLanguage} → en-GB`);
      after.defaultAudioLanguage = "en-GB";
    }
    if (live.madeForKids === true) {
      changes.push("madeForKids true → false (verify)");
      manual.push({
        videoId: id,
        before: { madeForKids: true },
        after: { madeForKids: false },
        reason: "Unexpected madeForKids=true on educational Orbit video",
        evidence: "API status.madeForKids",
        confidence: "MEDIUM",
        rollbackMethod: "videos.update status.madeForKids",
      });
    }
    if (changes.length) {
      metadataRepairs.push({
        videoId: id,
        before: {
          categoryId: live.categoryId,
          defaultLanguage: live.defaultLanguage,
          defaultAudioLanguage: live.defaultAudioLanguage,
        },
        after,
        reason: changes.join("; "),
        evidence: "Orbit Education/en-GB lock",
        confidence: "HIGH",
        rollbackMethod: "videos.update snippet fields to before",
      });
    }
  }
  for (const m of metadataRepairs) {
    if (Object.keys(m.after).length) safe.push({ ...m, type: "metadata" });
  }

  const planMd = [
    "# PROPOSED REPAIR PLAN",
    "",
    `Generated: ${new Date().toISOString()}`,
    "",
    "**No permanent deletions.** Mutations are privacy/schedule/metadata only.",
    "",
    `OAuth: \`youtube.force-ssl\` required for API updates. If missing, use Studio CDP visibility helpers for SAFE AUTOMATIC visibility repairs only.`,
    "",
    "## SAFE AUTOMATIC REPAIR",
    "",
    safe.length === 0
      ? "_None pending._"
      : [
          `| Video ID | Before | After | Reason | Confidence |`,
          `|----------|--------|-------|--------|------------|`,
          ...safe.map(
            (s) =>
              `| ${s.videoId} | ${JSON.stringify(s.before).replace(/\|/g, "/")} | ${JSON.stringify(s.after).replace(/\|/g, "/")} | ${String(s.reason).replace(/\|/g, "/")} | ${s.confidence} |`,
          ),
        ].join("\n"),
    "",
    "## MANUAL REVIEW",
    "",
    `Count: ${manual.length}`,
    "",
    manual.length
      ? manual
          .slice(0, 40)
          .map((m) => `- \`${m.videoId}\` — ${m.reason} (${m.confidence})`)
          .join("\n") + (manual.length > 40 ? `\n- … +${manual.length - 40} more` : "")
      : "_None._",
    "",
    "## DO NOT TOUCH",
    "",
    `Count: ${doNotTouch.length} (canonical OK / already held / ambiguous)`,
    "",
    "## Validation",
    "",
    `- Permanent delete operations in plan: **0**`,
    `- Re-upload operations in plan: **0**`,
    `- Safe visibility mutations: ${safe.filter((s) => s.after?.privacy).length}`,
    `- Safe metadata mutations: ${safe.filter((s) => s.type === "metadata").length}`,
    "",
  ].join("\n");

  fs.writeFileSync(path.join(outDir, "PROPOSED_REPAIR_PLAN.md"), planMd);
  fs.writeFileSync(
    path.join(outDir, "PROPOSED_REPAIR_PLAN.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), safe, manual, doNotTouch, metadataRepairs }, null, 2) +
      "\n",
  );

  // Rollback state
  const rollback = {
    generatedAt: new Date().toISOString(),
    videos: videos.map((v) => ({
      videoId: v.videoId,
      privacyStatus: v.privacyStatus,
      publishAt: v.publishAt,
      title: v.title,
      description: v.description,
      categoryId: v.categoryId,
      defaultLanguage: v.defaultLanguage,
      defaultAudioLanguage: v.defaultAudioLanguage,
      tags: v.tags,
      madeForKids: v.madeForKids,
      embeddable: v.embeddable,
    })),
  };
  fs.writeFileSync(path.join(outDir, "PRE_REPAIR_ROLLBACK_STATE.json"), JSON.stringify(rollback, null, 2) + "\n");
  fs.writeFileSync(
    path.join(outDir, "ROLLBACK_PLAN.md"),
    [
      "# ROLLBACK PLAN",
      "",
      "Source of truth: `PRE_REPAIR_ROLLBACK_STATE.json`",
      "",
      "1. For each mutated videoId, restore `privacyStatus` + `publishAt` from the rollback JSON.",
      "2. Prefer API `videos.update` with force-ssl; else Studio CDP visibility dialog.",
      "3. Never delete to roll back.",
      "4. Never re-upload to roll back.",
      "5. Registry changes: restore `YOUTUBE_CANONICAL_REGISTRY.json` from git.",
      "",
      "Mutations that cannot be rolled back (none planned): permanent delete, analytics reset.",
      "",
    ].join("\n"),
  );

  console.log(
    JSON.stringify(
      {
        ok: true,
        outDir,
        counts: inventory.counts,
        safeRepairs: safe.length,
        manualReview: manual.length,
        doNotTouch: doNotTouch.length,
        classSummary: Object.fromEntries(
          [...new Set(classifications.map((c) => c.classification))].map((k) => [
            k,
            classifications.filter((c) => c.classification === k).length,
          ]),
        ),
      },
      null,
      2,
    ),
  );
}

function summarizeClass(classifications: { classification: string }[]): string[] {
  const counts = new Map<string, number>();
  for (const c of classifications) {
    counts.set(c.classification, (counts.get(c.classification) || 0) + 1);
  }
  return [
    `| Classification | Count |`,
    `|----------------|------:|`,
    ...[...counts.entries()]
      .sort((a, b) => b[1] - a[1])
      .map(([k, n]) => `| ${k} | ${n} |`),
  ];
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => prisma.$disconnect());
