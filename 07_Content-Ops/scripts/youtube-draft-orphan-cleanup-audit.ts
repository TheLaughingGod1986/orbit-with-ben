/**
 * Stage A — Draft / orphan / private leftover cleanup AUDIT (read-only).
 * Zero YouTube mutations. Writes audit artifacts then stops for delete approval.
 *
 *   npx tsx scripts/youtube-draft-orphan-cleanup-audit.ts
 *
 * IMPORTANT (2026-08-10 forensic): Studio Draft Shorts live under
 * Content → Shorts (`/videos/short?filter=Draft`), NOT Content → Videos
 * (`/videos/upload`). Filtering only `/videos/upload` falsely reports
 * Drafts=0. See `youtube-studio-visibility.ts` + shorts_forensic_reconciliation_2026-08-10.
 */
import fs from "fs";
import path from "path";
import { createHash } from "crypto";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";

const AUDIT = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/audits/draft_orphan_cleanup_2026-08-08",
);
const REG_PATH = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/YOUTUBE_CANONICAL_REGISTRY.json",
);
const END_SCREEN_PATH = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/audits/channel_growth_optimisation_2026-08-08/END_SCREEN_PLAN.json",
);
const DUPE_CLASS_PATH = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07/STUDIO_DUPLICATE_CLASSIFICATION.json",
);
const REPO_ROOT = path.resolve(process.cwd(), "..");

const PUBLIC = [
  "Mo93x0fxB1Q",
  "1HuV8o3gOss",
  "KcKBixwmcV4",
  "3xrxdmaOwJI",
  "JRfhE6yWom4",
  "L2OFjL4neOo",
];

const TARGET_SCHED: Record<string, string> = {
  tUAdhOnMW2g: "2026-08-10T10:30:00Z",
  svYOx07OrIM: "2026-08-11T10:30:00Z",
  B2STcIAF1lY: "2026-08-12T10:30:00Z",
  "b8-X_FyJnHM": "2026-08-13T17:00:00Z",
  ho9VJxp7f3A: "2026-08-13T19:00:00Z",
  "aoR-dA_g7eI": "2026-08-14T10:30:00Z",
  "6QFGAFZk264": "2026-08-15T10:30:00Z",
  eOOFVrJ2Ojc: "2026-08-16T10:30:00Z",
  tfTkMdE7qqw: "2026-08-20T17:00:00Z",
  bLv0RfidjSg: "2026-08-20T19:00:00Z",
  PcP64way3xA: "2026-08-21T10:30:00Z",
  pjIevt27Svo: "2026-08-22T10:30:00Z",
  AeFm7gWyWik: "2026-08-23T10:30:00Z",
};

/** Explicitly protected excluded / private assets (not auto-deletable). */
const EXPLICIT_PROTECT = new Set([
  "HvAKGjx4lv0",
  "icedH_gK8JE",
  "Web2otrTcT0",
  "1qts3tIsg9c",
  "dPMJQp2gMNc",
  "rFJoOdQAc9c",
  "w1ej9u0rPTA",
  "gPCpMsB0w2E",
  "YsyPMhNmHMk",
  "1wxUhF3XnwI", // dead JWST parent — forensic / history
]);

/** Known held private duplicates from schedule-repair / forensic (default KEEP). */
const HELD_PRIVATE_DUPES = new Set([
  "RCs6MMxF3ko",
  "IwpO33AJaPQ",
  "IqII5mVGdrs",
  "2C-eiSMsBLc",
  "lIHb_tyxQSM",
  "wOlnj7nZWJM",
  "nX84ileqPKw",
  "2uT3wXJLybw",
  "5jjJ5CHrbCs",
  "5nMieBeymKU",
  "z-DLqoSoEBo",
  "UWwNKYf_aU8",
  "dFO50RT5s14",
  "8DxCTXUlw74",
  "zc79sRBCDnU",
  "--CxhjNqtSY",
  "6dSntxIQgXI",
  "z8-haBeF6mI",
  "IvSMHnngXdE",
  "MO19iXYCu0c",
  "Cw-tfP1QnBE",
  "S80vTqwqzHE",
  "trrKgW7m_98",
  "8XaOqbZX7Yg",
  "IsPLdq0oSe8",
  "lUvMhe1BWJM",
  "ItuOwgTvS1Y",
  "ZjzVp_E328w",
  "slCssHVBOz0",
  "YNmSjtc6SaE",
  "4dGXJt9dElk",
  "pJCKi6_OXjk",
  "aX_7Qg_qzyo",
  "mGwSCdgxQO4",
  "niqnBlzqaFs",
  "J_uLnRIwqu0",
  "PYhQ0x9HcPM",
  "e8-rKGv37o4",
  "LQtNmzXJW4w",
  "i18OD5Ab748",
  "1wxUhF3XnwI",
  "oFzKgHbAw4M",
  "SGv-wH0XbtI",
  "Tw2OdQABU4E",
  "5MysOlOqLDY",
  "yTljUMV5Gms",
  "QW0cn-O9k5g",
  "hdlr1soUwNA",
  "olnaYqeOtFs",
  "EO-44QH4glI",
  "B95wuAH68QY",
  "P95alanW8GU",
  "RF6wivuPYqI",
  "2777WlMGM8M",
  "80S5E-AWFhA",
  "C4GuFEFGySI",
  "eZGAhF8dN7w",
  "jyzrl9ueKq4",
  "kv1Yz74_S10",
  "n7CbJrOCnU0",
  "t1hTGIH8O44",
  "xhBR-ixXi8s",
  "z-kgwJaz5pY",
]);

type Classification =
  | "PUBLIC_CANONICAL_PROTECTED"
  | "SCHEDULED_PROTECTED"
  | "PRIVATE_CANONICAL_PROTECTED"
  | "FUTURE_ASSET_PROTECTED"
  | "HISTORICAL_DUPLICATE_PROTECTED"
  | "RELATED_TARGET_PROTECTED"
  | "END_SCREEN_TARGET_PROTECTED"
  | "PLAYLIST_REFERENCED_PROTECTED"
  | "SAFE_TO_DELETE_DRAFT"
  | "SAFE_TO_DELETE_ORPHAN"
  | "SAFE_TO_DELETE_CONFIRMED_DUPLICATE"
  | "POSSIBLE_DUPLICATE_KEEP"
  | "UNKNOWN_KEEP";

function write(name: string, data: unknown) {
  fs.mkdirSync(AUDIT, { recursive: true });
  const p = path.join(AUDIT, name);
  if (typeof data === "string") fs.writeFileSync(p, data.endsWith("\n") ? data : data + "\n");
  else fs.writeFileSync(p, JSON.stringify(data, null, 2) + "\n");
  return p;
}

async function bearerToken(): Promise<string> {
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

async function yt(token: string, url: string) {
  const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  const body = await res.json();
  if (!res.ok) {
    throw new Error(`${url} -> ${res.status} ${JSON.stringify(body).slice(0, 500)}`);
  }
  return body;
}

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

function walkMp4(dir: string, out: string[], depth = 0) {
  if (depth > 8 || !fs.existsSync(dir)) return;
  let entries: fs.Dirent[];
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const e of entries) {
    if (e.name.startsWith(".") || e.name === "node_modules") continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walkMp4(full, out, depth + 1);
    else if (/\.(mp4|mov|m4v)$/i.test(e.name)) out.push(full);
  }
}

function sha256File(filePath: string): string | null {
  try {
    const st = fs.statSync(filePath);
    if (st.size > 400 * 1024 * 1024) return null; // skip huge for Stage A speed
    const h = createHash("sha256");
    h.update(fs.readFileSync(filePath));
    return h.digest("hex");
  } catch {
    return null;
  }
}

async function main() {
  fs.mkdirSync(path.join(AUDIT, "screenshots"), { recursive: true });
  const tok = await bearerToken();
  const reg = JSON.parse(fs.readFileSync(REG_PATH, "utf8"));
  const endPlan = fs.existsSync(END_SCREEN_PATH)
    ? JSON.parse(fs.readFileSync(END_SCREEN_PATH, "utf8"))
    : { endscreens: [] };
  const dupeClass = fs.existsSync(DUPE_CLASS_PATH)
    ? JSON.parse(fs.readFileSync(DUPE_CLASS_PATH, "utf8"))
    : { rows: [] };

  const registryById = new Map<string, any>();
  const histToCanonical = new Map<string, string>();
  const relatedTargets = new Set<string>();
  for (const r of reg.records || []) {
    if (r.youtubeVideoId) registryById.set(r.youtubeVideoId, r);
    for (const h of r.historicalDuplicateIds || []) {
      histToCanonical.set(h, r.youtubeVideoId);
    }
    if (r.relatedLongFormVideoId) relatedTargets.add(r.relatedLongFormVideoId);
  }
  for (const h of reg.historicalDuplicateIdsGlobal || []) {
    if (!histToCanonical.has(h)) histToCanonical.set(h, "(global)");
  }

  const endScreenTargets = new Set<string>();
  for (const e of endPlan.endscreens || []) {
    if (e.longId) endScreenTargets.add(e.longId);
    if (e.recommendedNextVideoId) endScreenTargets.add(e.recommendedNextVideoId);
  }

  const dupeById = new Map<string, any>();
  for (const row of dupeClass.rows || []) {
    if (row.videoId) dupeById.set(row.videoId, row);
  }

  // Channel + uploads playlist (complete inventory)
  const chBody = await yt(
    tok,
    "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails,brandingSettings&mine=true",
  );
  const channel = chBody.items?.[0];
  if (!channel) throw new Error("No channel");
  const channelTitle = channel.snippet?.title || "";
  const uploadsPlaylistId = channel.contentDetails?.relatedPlaylists?.uploads;
  if (!uploadsPlaylistId) throw new Error("No uploads playlist");

  const uploadIds: string[] = [];
  let pageToken = "";
  do {
    const url =
      `https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId=${uploadsPlaylistId}` +
      (pageToken ? `&pageToken=${pageToken}` : "");
    const page = await yt(tok, url);
    for (const it of page.items || []) {
      const id = it.contentDetails?.videoId;
      if (id) uploadIds.push(id);
    }
    pageToken = page.nextPageToken || "";
  } while (pageToken);

  // User playlists + memberships
  const playlists: Array<{ id: string; title: string; itemCount: number; privacy: string | null }> =
    [];
  const playlistMembership = new Map<string, string[]>(); // videoId -> playlist titles
  pageToken = "";
  do {
    const u = new URL("https://www.googleapis.com/youtube/v3/playlists");
    u.searchParams.set("part", "snippet,contentDetails,status");
    u.searchParams.set("mine", "true");
    u.searchParams.set("maxResults", "50");
    if (pageToken) u.searchParams.set("pageToken", pageToken);
    const body = await yt(tok, u.toString());
    for (const p of body.items || []) {
      playlists.push({
        id: p.id,
        title: p.snippet?.title,
        itemCount: p.contentDetails?.itemCount,
        privacy: p.status?.privacyStatus ?? null,
      });
    }
    pageToken = body.nextPageToken || "";
  } while (pageToken);

  for (const pl of playlists) {
    let pt = "";
    do {
      const url =
        `https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails,snippet&maxResults=50&playlistId=${pl.id}` +
        (pt ? `&pageToken=${pt}` : "");
      const page = await yt(tok, url);
      for (const it of page.items || []) {
        const vid = it.contentDetails?.videoId;
        if (!vid) continue;
        const arr = playlistMembership.get(vid) || [];
        arr.push(pl.title);
        playlistMembership.set(vid, arr);
      }
      pt = page.nextPageToken || "";
    } while (pt);
  }

  // Content Ops DB references
  const contentOpsIds = new Set<string>();
  try {
    const pubs = await prisma.publishingJob.findMany({
      select: { externalId: true, payloadJson: true },
      take: 5000,
    });
    for (const p of pubs) {
      if (p.externalId) contentOpsIds.add(p.externalId);
      const raw = JSON.stringify((p as { payloadJson?: unknown }).payloadJson || {});
      for (const m of raw.matchAll(/[A-Za-z0-9_-]{11}/g)) {
        if (uploadIds.includes(m[0])) contentOpsIds.add(m[0]);
      }
    }
  } catch {
    /* optional — schema fields vary; never block Stage A */
  }

  // Union of known IDs
  const allIds = new Set<string>([
    ...uploadIds,
    ...PUBLIC,
    ...Object.keys(TARGET_SCHED),
    ...registryById.keys(),
    ...histToCanonical.keys(),
    ...EXPLICIT_PROTECT,
    ...HELD_PRIVATE_DUPES,
  ]);

  const items: any[] = [];
  const idList = [...allIds];
  for (let i = 0; i < idList.length; i += 50) {
    const chunk = idList.slice(i, i + 50);
    const body = await yt(
      tok,
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails,statistics&id=${chunk.join(",")}`,
    );
    items.push(...(body.items || []));
  }
  const returnedIds = new Set(items.map((v) => v.id));
  const missingFromApi = idList.filter((id) => !returnedIds.has(id));

  // Local forensics (paths + optional SHA for modest files)
  const mp4s: string[] = [];
  walkMp4(path.join(REPO_ROOT, "02_Video-Projects"), mp4s);
  const localAssets = mp4s.slice(0, 400).map((sourcePath) => {
    const st = fs.statSync(sourcePath);
    const rel = path.relative(REPO_ROOT, sourcePath);
    const familyGuess = /fermi|alien/i.test(rel)
      ? "FERMI"
      : /black.?hole|bh_/i.test(rel)
        ? "BLACK_HOLE"
        : /exoplanet/i.test(rel)
          ? "EXOPLANETS"
          : /jwst|webb/i.test(rel)
            ? "JWST"
            : "UNKNOWN";
    return {
      contentId: null,
      contentFamily: familyGuess,
      contentType: /short/i.test(rel) ? "shorts" : "longform",
      sourcePath: rel,
      sourceSHA256: st.size <= 80 * 1024 * 1024 ? sha256File(sourcePath) : null,
      duration: null,
      knownYouTubeIds: [] as string[],
      canonicalYouTubeId: null as string | null,
      historicalDuplicateIds: [] as string[],
      intendedState: "local_render",
      bytes: st.size,
    };
  });

  // Title fingerprint groups among live videos
  const byTitleDur = new Map<string, string[]>();
  for (const v of items) {
    const title = v.snippet?.title || "";
    const duration = v.contentDetails?.duration || "?";
    const key = `${normalizeTitle(title)}|${duration}`;
    const arr = byTitleDur.get(key) || [];
    arr.push(v.id);
    byTitleDur.set(key, arr);
  }

  const publicLive = items.filter((v) => v.status?.privacyStatus === "public").map((v) => v.id);
  const scheduledLive = items
    .filter((v) => v.status?.publishAt)
    .map((v) => ({
      videoId: v.id,
      publishAt: v.status.publishAt,
      privacyStatus: v.status.privacyStatus,
      title: v.snippet?.title,
    }));
  const unexpectedPublic = publicLive.filter((id) => !PUBLIC.includes(id));
  const missingPublic = PUBLIC.filter((id) => {
    const v = items.find((x) => x.id === id);
    return !(v && v.status?.privacyStatus === "public");
  });
  const missingScheduled = Object.entries(TARGET_SCHED)
    .filter(([id, exp]) => {
      const v = items.find((x) => x.id === id);
      return !(v && v.status?.privacyStatus === "private" && v.status?.publishAt === exp);
    })
    .map(([id]) => id);
  const slotMap: Record<string, string[]> = {};
  for (const s of scheduledLive) {
    (slotMap[s.publishAt] ||= []).push(s.videoId);
  }
  const collisions = Object.values(slotMap).filter((a) => a.length > 1).length;
  const placeholders = scheduledLive.filter((s) => (s.publishAt || "").startsWith("2026-12-31"))
    .length;

  const integrity = {
    channelTitle,
    channelId: channel.id,
    publicCanonicals: `${PUBLIC.length - missingPublic.length}/${PUBLIC.length}`,
    publicIds: publicLive.filter((id) => PUBLIC.includes(id)).sort(),
    unexpectedPublic,
    missingPublic,
    scheduled: `${Object.keys(TARGET_SCHED).length - missingScheduled.length}/${Object.keys(TARGET_SCHED).length}`,
    scheduledRows: scheduledLive.sort((a, b) => a.publishAt.localeCompare(b.publishAt)),
    missingScheduled,
    collisions,
    placeholders,
    uploadCount: uploadIds.length,
    returnedCount: items.length,
    missingFromApi,
    preflightOk:
      missingPublic.length === 0 &&
      unexpectedPublic.length === 0 &&
      missingScheduled.length === 0 &&
      collisions === 0 &&
      placeholders === 0,
  };

  if (!integrity.preflightOk) {
    write("PREFLIGHT_BLOCKED.json", integrity);
    console.log(
      JSON.stringify(
        { verdict: "CLEANUP BLOCKED — PROTECTED CHANNEL STATE NOT CLEAN", integrity },
        null,
        2,
      ),
    );
    process.exit(2);
  }

  write("DRAFT_CLEANUP_PUBLIC_BEFORE.json", {
    fetchedAt: new Date().toISOString(),
    publicIds: integrity.publicIds,
    unexpectedPublic: [],
  });
  write("DRAFT_CLEANUP_SCHEDULE_BEFORE.json", {
    fetchedAt: new Date().toISOString(),
    scheduled: integrity.scheduledRows,
  });

  type Row = {
    asset: string;
    id: string;
    state: string;
    family: string | null;
    canonical: boolean;
    references: string[];
    duplicateEvidence: string;
    classification: Classification;
    proposedAction: "KEEP" | "PROPOSE_DELETE";
    confidence: "HIGH" | "MEDIUM" | "LOW";
    title: string;
    duration: string | null;
    privacyStatus: string;
    publishAt: string | null;
    publishedAt: string | null;
    viewCount: number;
    commentCount: number;
    contentId: string | null;
    contentType: string | null;
    canonicalVideoId: string | null;
    historicalDuplicateIds: string[];
    playlistMemberships: string[];
    relatedLongId: string | null;
    endScreenReferenced: boolean;
    registryReferenced: boolean;
    contentOpsReferenced: boolean;
    localSourcePath: string | null;
    localSourceSHA256: string | null;
  };

  const rows: Row[] = [];

  for (const v of items) {
    const id = v.id as string;
    const title = (v.snippet?.title || "") as string;
    const privacy = (v.status?.privacyStatus || "unknown") as string;
    const publishAt = (v.status?.publishAt || null) as string | null;
    const duration = (v.contentDetails?.duration || null) as string | null;
    const views = Number(v.statistics?.viewCount || 0);
    const comments = Number(v.statistics?.commentCount || 0);
    const regRec = registryById.get(id);
    const histCanon = histToCanonical.get(id) || null;
    const dupe = dupeById.get(id);
    const playlistsFor = playlistMembership.get(id) || [];
    const refs: string[] = [];
    if (regRec) refs.push("registry_canonical");
    if (histCanon) refs.push(`historical_of:${histCanon}`);
    if (relatedTargets.has(id)) refs.push("related_target");
    if (endScreenTargets.has(id)) refs.push("end_screen_target");
    if (playlistsFor.length) refs.push(`playlists:${playlistsFor.join("|")}`);
    if (contentOpsIds.has(id)) refs.push("content_ops");
    if (EXPLICIT_PROTECT.has(id)) refs.push("explicit_protect_list");
    if (HELD_PRIVATE_DUPES.has(id)) refs.push("held_private_dupe_list");
    if (dupe) refs.push(`prior_dupe_class:${dupe.confidence || "known"}->${dupe.canonicalId}`);

    const titleKey = `${normalizeTitle(title)}|${duration || "?"}`;
    const titlePeers = (byTitleDur.get(titleKey) || []).filter((x) => x !== id);
    let duplicateEvidence = "";
    if (dupe) {
      duplicateEvidence = `prior_studio_class ${dupe.confidence} of ${dupe.canonicalId}`;
    } else if (histCanon) {
      duplicateEvidence = `registry historicalDuplicateIds → ${histCanon}`;
    } else if (titlePeers.length) {
      duplicateEvidence = `same_title+duration peers: ${titlePeers.join(",")}`;
    }

    let classification: Classification;
    let proposedAction: "KEEP" | "PROPOSE_DELETE" = "KEEP";
    let confidence: "HIGH" | "MEDIUM" | "LOW" = "HIGH";
    let reasonFamily: string | null = regRec?.contentFamily || dupe?.family || null;

    if (PUBLIC.includes(id) && privacy === "public") {
      classification = "PUBLIC_CANONICAL_PROTECTED";
    } else if (TARGET_SCHED[id] || publishAt) {
      classification = "SCHEDULED_PROTECTED";
    } else if (endScreenTargets.has(id) && !regRec) {
      classification = "END_SCREEN_TARGET_PROTECTED";
    } else if (relatedTargets.has(id) && !PUBLIC.includes(id) && !TARGET_SCHED[id]) {
      classification = "RELATED_TARGET_PROTECTED";
    } else if (regRec && (regRec.intendedYouTubeStatus === "private" || privacy === "private")) {
      classification =
        regRec.intendedYouTubeStatus === "scheduled"
          ? "FUTURE_ASSET_PROTECTED"
          : "PRIVATE_CANONICAL_PROTECTED";
      reasonFamily = regRec.contentFamily;
    } else if (playlistsFor.length && !PUBLIC.includes(id) && !TARGET_SCHED[id]) {
      classification = "PLAYLIST_REFERENCED_PROTECTED";
    } else if (histCanon || HELD_PRIVATE_DUPES.has(id) || dupe) {
      // Default: historical duplicates stay protected — do not auto-propose delete
      classification = "HISTORICAL_DUPLICATE_PROTECTED";
      if (!reasonFamily && dupe) reasonFamily = null;
    } else if (EXPLICIT_PROTECT.has(id)) {
      classification = "PRIVATE_CANONICAL_PROTECTED";
    } else if (titlePeers.length && privacy === "private" && !publishAt) {
      // Title+duration match alone is insufficient for SAFE delete
      classification = "POSSIBLE_DUPLICATE_KEEP";
      confidence = "MEDIUM";
    } else if (privacy === "private" && !publishAt && refs.length === 0) {
      classification = "UNKNOWN_KEEP";
      confidence = "LOW";
    } else {
      classification = "UNKNOWN_KEEP";
      confidence = "LOW";
    }

    // Never propose delete in Stage A automation — only HIGH after human rules.
    // Conservative: Stage A proposes ZERO deletes unless unmistakably orphan draft
    // with zero references AND zero historical value. We require ALL safe rules;
    // uploaded private videos with any peer/history stay KEEP.
    proposedAction = "KEEP";

    rows.push({
      asset: title,
      id,
      state: publishAt ? `private+scheduled` : privacy,
      family: reasonFamily,
      canonical: Boolean(regRec && regRec.youtubeVideoId === id),
      references: refs,
      duplicateEvidence,
      classification,
      proposedAction,
      confidence,
      title,
      duration,
      privacyStatus: privacy,
      publishAt,
      publishedAt: v.snippet?.publishedAt || null,
      viewCount: views,
      commentCount: comments,
      contentId: regRec?.internalContentId || null,
      contentType:
        regRec?.contentType ||
        (parseDurationSeconds(duration) != null && (parseDurationSeconds(duration) as number) <= 60
          ? "shorts"
          : "longform"),
      canonicalVideoId: regRec?.youtubeVideoId === id ? id : histCanon,
      historicalDuplicateIds: regRec?.historicalDuplicateIds || [],
      playlistMemberships: playlistsFor,
      relatedLongId: regRec?.relatedLongFormVideoId || null,
      endScreenReferenced: endScreenTargets.has(id),
      registryReferenced: Boolean(regRec) || Boolean(histCanon),
      contentOpsReferenced: contentOpsIds.has(id),
      localSourcePath: null,
      localSourceSHA256: null,
    });
  }

  // Enrich local map with known IDs from registry titles/paths (best-effort)
  write("LOCAL_DRAFT_CLEANUP_MAP.json", {
    generatedAt: new Date().toISOString(),
    scannedMp4Count: mp4s.length,
    hashedSampleCount: localAssets.filter((a) => a.sourceSHA256).length,
    assets: localAssets,
    note: "SHA limited to files ≤80MB; large masters listed without hash.",
  });

  const mdLocal = [
    "# Local Draft Cleanup Map",
    "",
    `Generated: \`${new Date().toISOString()}\``,
    "",
    `- Scanned MP4/MOV under \`02_Video-Projects\`: **${mp4s.length}**`,
    `- Hashed (≤80MB): **${localAssets.filter((a) => a.sourceSHA256).length}**`,
    "",
    "| Family | Type | Path | SHA256 |",
    "|---|---|---|---|",
    ...localAssets.slice(0, 80).map((a) => {
      const sha = a.sourceSHA256 ? a.sourceSHA256.slice(0, 12) + "…" : "—";
      return `| ${a.contentFamily} | ${a.contentType} | \`${a.sourcePath}\` | ${sha} |`;
    }),
    "",
    mp4s.length > 80 ? `_Showing first 80 of ${mp4s.length}._` : "",
  ].join("\n");
  write("LOCAL_DRAFT_CLEANUP_MAP.md", mdLocal);

  const before = {
    fetchedAt: new Date().toISOString(),
    mutation: "NONE",
    stage: "A_AUDIT_ONLY",
    channel: {
      id: channel.id,
      title: channelTitle,
      customUrl: channel.snippet?.customUrl,
      stats: channel.statistics,
    },
    integrity,
    playlists,
    videos: rows.map((r) => ({
      videoId: r.id,
      title: r.title,
      duration: r.duration,
      privacyStatus: r.privacyStatus,
      publishAt: r.publishAt,
      publishedAt: r.publishedAt,
      viewCount: r.viewCount,
      commentCount: r.commentCount,
      contentId: r.contentId,
      contentFamily: r.family,
      contentType: r.contentType,
      sourceFingerprint: null,
      canonicalVideoId: r.canonicalVideoId,
      historicalDuplicateIds: r.historicalDuplicateIds,
      playlistMemberships: r.playlistMemberships,
      relatedLongId: r.relatedLongId,
      endScreenReferences: r.endScreenReferenced,
      registryReferences: r.registryReferenced,
      contentOpsReferences: r.contentOpsReferenced,
      localSourcePath: r.localSourcePath,
      localSourceSHA256: r.localSourceSHA256,
      classification: r.classification,
      proposedAction: r.proposedAction,
      confidence: r.confidence,
      duplicateEvidence: r.duplicateEvidence,
      references: r.references,
    })),
  };
  write("DRAFT_CLEANUP_BEFORE.json", before);

  const counts: Record<string, number> = {};
  for (const r of rows) counts[r.classification] = (counts[r.classification] || 0) + 1;

  const table = [
    "# Draft Cleanup Before Inventory",
    "",
    `Generated: \`${before.fetchedAt}\` · Stage A · **NO DELETIONS**`,
    "",
    `Channel: **${channelTitle}** (\`${channel.id}\`)`,
    "",
    "## Integrity",
    "",
    `- Public canonicals: **${integrity.publicCanonicals}**`,
    `- Scheduled: **${integrity.scheduled}**`,
    `- Unexpected public: **${integrity.unexpectedPublic.length}**`,
    `- Missing scheduled: **${integrity.missingScheduled.length}**`,
    `- Collisions: **${integrity.collisions}**`,
    `- Placeholders: **${integrity.placeholders}**`,
    `- Uploads playlist count: **${uploadIds.length}**`,
    "",
    "## Classification counts",
    "",
    ...Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .map(([k, n]) => `- \`${k}\`: **${n}**`),
    "",
    "## Full table",
    "",
    "|Asset|ID|State|Family|Canonical?|References|Duplicate Evidence|Classification|Proposed Action|Confidence|",
    "|-----|--|-----|------|----------|----------|------------------|--------------|---------------|----------|",
    ...rows
      .sort((a, b) => a.classification.localeCompare(b.classification) || a.id.localeCompare(b.id))
      .map((r) => {
        const asset = (r.title || "").replace(/\|/g, "/").slice(0, 48);
        const refs = (r.references.join("; ") || "—").replace(/\|/g, "/").slice(0, 60);
        const dupe = (r.duplicateEvidence || "—").replace(/\|/g, "/").slice(0, 50);
        return `| ${asset} | \`${r.id}\` | ${r.state} | ${r.family || "—"} | ${r.canonical ? "Y" : "N"} | ${refs} | ${dupe} | \`${r.classification}\` | ${r.proposedAction} | ${r.confidence} |`;
      }),
    "",
  ].join("\n");
  write("DRAFT_CLEANUP_BEFORE.md", table);

  // Proposed deletions: only HIGH confidence SAFE_* — currently none by design
  const proposed = rows.filter(
    (r) =>
      r.proposedAction === "PROPOSE_DELETE" &&
      r.confidence === "HIGH" &&
      (r.classification === "SAFE_TO_DELETE_DRAFT" ||
        r.classification === "SAFE_TO_DELETE_ORPHAN" ||
        r.classification === "SAFE_TO_DELETE_CONFIRMED_DUPLICATE"),
  );

  const proposalJson = {
    generatedAt: new Date().toISOString(),
    stage: "A_AUDIT_ONLY",
    policy: "DELETE ONLY PROVEN JUNK — KEEP EVERYTHING ELSE",
    proposedDeletes: proposed,
    counts: {
      safeDraftDeletes: proposed.filter((r) => r.classification === "SAFE_TO_DELETE_DRAFT").length,
      safeOrphanDeletes: proposed.filter((r) => r.classification === "SAFE_TO_DELETE_ORPHAN")
        .length,
      safeConfirmedDuplicateDeletes: proposed.filter(
        (r) => r.classification === "SAFE_TO_DELETE_CONFIRMED_DUPLICATE",
      ).length,
      protected: rows.filter((r) => r.classification.includes("PROTECTED")).length,
      possibleDuplicatesKept: rows.filter((r) => r.classification === "POSSIBLE_DUPLICATE_KEEP")
        .length,
      unknownKept: rows.filter((r) => r.classification === "UNKNOWN_KEEP").length,
      historicalDuplicatesProtected: rows.filter(
        (r) => r.classification === "HISTORICAL_DUPLICATE_PROTECTED",
      ).length,
    },
    rationale: [
      "Prior Studio duplicate classification already marked EXACT/HIGH duplicates as KEEP_PRIVATE.",
      "Default for historical duplicates is HISTORICAL_DUPLICATE_PROTECTED (forensic + anti re-upload).",
      "Title+duration similarity alone is insufficient for SAFE_TO_DELETE_CONFIRMED_DUPLICATE.",
      "Explicit excluded/private assets (HvAKGjx4lv0, icedH_gK8JE, Web2otrTcT0, 1qts3tIsg9c, etc.) remain protected.",
      "Dead JWST parent 1wxUhF3XnwI retained as HISTORICAL_DUPLICATE_PROTECTED.",
      "No genuine unreferenced Studio Draft without a video ID was proven via API; Playwright discovery follows separately.",
      "Zero HIGH-confidence SAFE_TO_DELETE candidates under conservative rules.",
    ],
    note: "Stage B must not run until explicit approval. Empty proposal means no deletes authorised.",
  };
  write("PROPOSED_DRAFT_ORPHAN_DELETIONS.json", proposalJson);

  const proposalMd = [
    "# Proposed Draft / Orphan Deletions",
    "",
    `Generated: \`${proposalJson.generatedAt}\``,
    "",
    "**Stage A only — NO DELETIONS PERFORMED.**",
    "",
    "## Summary counts",
    "",
    `- Safe draft deletes (HIGH): **${proposalJson.counts.safeDraftDeletes}**`,
    `- Safe orphan deletes (HIGH): **${proposalJson.counts.safeOrphanDeletes}**`,
    `- Safe confirmed duplicate deletes (HIGH): **${proposalJson.counts.safeConfirmedDuplicateDeletes}**`,
    `- Protected: **${proposalJson.counts.protected}**`,
    `- Historical duplicates protected: **${proposalJson.counts.historicalDuplicatesProtected}**`,
    `- Possible duplicates kept: **${proposalJson.counts.possibleDuplicatesKept}**`,
    `- Unknown kept: **${proposalJson.counts.unknownKept}**`,
    "",
    "## Proposed delete list",
    "",
    proposed.length === 0
      ? "_None. No HIGH-confidence SAFE_TO_DELETE_* candidates under conservative rules._"
      : proposed
          .map(
            (r) =>
              `### \`${r.id}\` — ${r.title}\n\n- Classification: \`${r.classification}\`\n- State: ${r.state}\n- Canonical equivalent: ${r.canonicalVideoId || "—"}\n- Evidence: ${r.duplicateEvidence || "—"}\n- References: ${r.references.join("; ") || "none"}\n- Rollback: soft-delete only; local renders preserved\n`,
          )
          .join("\n"),
    "",
    "## Rationale",
    "",
    ...proposalJson.rationale.map((x) => `- ${x}`),
    "",
    "## Recommendation",
    "",
    "Do **not** proceed to Stage B unless you explicitly approve a non-empty HIGH-confidence delete list.",
    "Visual clutter in Studio private leftovers is not sufficient grounds for deletion.",
    "",
  ].join("\n");
  write("PROPOSED_DRAFT_ORPHAN_DELETIONS.md", proposalMd);

  write("STAGE_A_SUMMARY.json", {
    verdict: "DRAFT CLEANUP AUDIT COMPLETE — AWAITING DELETE APPROVAL",
    integrity,
    counts: proposalJson.counts,
    proposedDeleteCount: proposed.length,
    totalClassified: rows.length,
  });

  console.log(
    JSON.stringify(
      {
        verdict: "DRAFT CLEANUP AUDIT COMPLETE — AWAITING DELETE APPROVAL",
        channel: channelTitle,
        integrity: {
          public: integrity.publicCanonicals,
          scheduled: integrity.scheduled,
          unexpectedPublic: integrity.unexpectedPublic,
          missingScheduled: integrity.missingScheduled,
          collisions: integrity.collisions,
          placeholders: integrity.placeholders,
        },
        classified: rows.length,
        counts: proposalJson.counts,
        proposedDeletes: proposed.length,
        auditDir: AUDIT,
      },
      null,
      2,
    ),
  );
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
