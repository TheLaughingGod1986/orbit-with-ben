#!/usr/bin/env tsx
/**
 * Re-upload remastered CFR masters for still-scheduled/private YouTube items.
 * Never touches public videos. Upload first, then delete old id, then update ledgers.
 *
 *   npx tsx scripts/youtube-reupload-scheduled-cfr.ts --dry-run
 *   npx tsx scripts/youtube-reupload-scheduled-cfr.ts --execute --approved-by-user
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";

const ROOT = path.resolve(process.cwd(), "..");
const AUDIT = path.join(ROOT, "00_Brand/Channel-Setup/audits/playback_lag_scheduled_reupload");
const VIS = "/tmp/orbit-playback-lag/visibility_audit.json";
const MIN_LEAD_MS = 20 * 60 * 1000; // publishAt must be >= 20 min out

function flag(name: string) {
  return process.argv.includes(`--${name}`);
}
function writeJson(file: string, value: unknown) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + "\n");
}

async function token(): Promise<string> {
  getEnv();
  const connection = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!connection?.accessTokenEncrypted) throw new Error("No connected YouTube account");
  const adapter = new YouTubePublishingAdapter();
  if (connection.accessTokenExpiresAt && connection.accessTokenExpiresAt.getTime() < Date.now() + 120_000) {
    const refreshed = await adapter.refreshConnection?.(connection);
    if (!refreshed?.ok) throw new Error(`Token refresh failed: ${JSON.stringify(refreshed)}`);
  }
  const fresh = await prisma.platformConnection.findUnique({ where: { id: connection.id } });
  if (!fresh?.accessTokenEncrypted) throw new Error("token missing");
  return decryptSecret(fresh.accessTokenEncrypted);
}

async function getVideos(accessToken: string, ids: string[]) {
  const map = new Map<string, any>();
  for (let i = 0; i < ids.length; i += 50) {
    const chunk = ids.slice(i, i + 50);
    const url = `https://www.googleapis.com/youtube/v3/videos?part=status,snippet,statistics,contentDetails&id=${chunk.join(",")}`;
    const res = await fetch(url, { headers: { Authorization: `Bearer ${accessToken}` } });
    const body = await res.json();
    if (!res.ok) throw new Error(`videos.list ${res.status}: ${JSON.stringify(body)}`);
    for (const item of body.items || []) map.set(item.id, item);
  }
  return map;
}

async function deleteVideo(accessToken: string, id: string) {
  const res = await fetch(`https://www.googleapis.com/youtube/v3/videos?id=${encodeURIComponent(id)}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (!res.ok) throw new Error(`videos.delete ${id} ${res.status}: ${await res.text()}`);
}

async function uploadScheduled(
  accessToken: string,
  input: {
    filePath: string;
    title: string;
    description: string;
    tags: string[];
    categoryId: string;
    publishAtIso: string;
    madeForKids: boolean;
    defaultLanguage?: string;
    defaultAudioLanguage?: string;
  },
) {
  const size = fs.statSync(input.filePath).size;
  const initUrl = new URL("https://www.googleapis.com/upload/youtube/v3/videos");
  initUrl.searchParams.set("uploadType", "resumable");
  initUrl.searchParams.set("part", "snippet,status");
  initUrl.searchParams.set("notifySubscribers", "false");

  const metaRes = await fetch(initUrl.toString(), {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json; charset=UTF-8",
      "X-Upload-Content-Type": "video/mp4",
      "X-Upload-Content-Length": String(size),
    },
    body: JSON.stringify({
      snippet: {
        title: input.title.slice(0, 100),
        description: input.description || "",
        categoryId: input.categoryId || "27",
        tags: (input.tags || []).slice(0, 15),
        defaultLanguage: input.defaultLanguage || "en",
        defaultAudioLanguage: input.defaultAudioLanguage || "en-GB",
      },
      status: {
        privacyStatus: "private",
        publishAt: input.publishAtIso,
        selfDeclaredMadeForKids: Boolean(input.madeForKids),
      },
    }),
  });
  if (!metaRes.ok) throw new Error(`upload init ${metaRes.status}: ${await metaRes.text()}`);
  const uploadUrl = metaRes.headers.get("location");
  if (!uploadUrl) throw new Error("missing resumable location");

  // Stream in 8MB chunks to avoid huge memory for long-form
  const fh = await fs.promises.open(input.filePath, "r");
  try {
    let offset = 0;
    const chunkSize = 8 * 1024 * 1024;
    let finalBody: any = null;
    while (offset < size) {
      const len = Math.min(chunkSize, size - offset);
      const buf = Buffer.alloc(len);
      await fh.read(buf, 0, len, offset);
      const end = offset + len - 1;
      const res = await fetch(uploadUrl, {
        method: "PUT",
        headers: {
          "Content-Type": "video/mp4",
          "Content-Length": String(len),
          "Content-Range": `bytes ${offset}-${end}/${size}`,
        },
        body: buf,
      });
      if (res.status === 308) {
        offset += len;
        continue;
      }
      const body = await res.json().catch(() => ({}));
      if (!res.ok || !body.id) throw new Error(`upload put ${res.status}: ${JSON.stringify(body)}`);
      finalBody = body;
      offset = size;
    }
    if (!finalBody?.id) throw new Error("upload finished without video id");
    return finalBody as { id: string };
  } finally {
    await fh.close();
  }
}

function updateLedgers(oldId: string, newId: string, publishAt: string | null) {
  const changes: string[] = [];
  // SHORTS_UPLOAD_INDEX.json files
  const projects = path.join(ROOT, "02_Video-Projects");
  for (const indexPath of fs
    .readdirSync(projects, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => path.join(projects, d.name, "10_Shorts", "SHORTS_UPLOAD_INDEX.json"))
    .filter((p) => fs.existsSync(p))) {
    const raw = fs.readFileSync(indexPath, "utf8");
    if (!raw.includes(oldId)) continue;
    const data = JSON.parse(raw);
    let touched = false;
    if (data.long_id === oldId) {
      data.long_id = newId;
      touched = true;
    }
    if (data.related_to_long === oldId) {
      data.related_to_long = newId;
      touched = true;
    }
    if (data.canonical_long_id === oldId) {
      data.canonical_long_id = newId;
      touched = true;
    }
    if (Array.isArray(data.shorts)) {
      for (const s of data.shorts) {
        if (s.youtube_video_id === oldId) {
          s.youtube_video_id = newId;
          s.previous_youtube_video_id = oldId;
          s.cfr_reupload_at = new Date().toISOString();
          touched = true;
        }
        if (s.video_id === oldId) {
          s.video_id = newId;
          touched = true;
        }
      }
    }
    if (touched) {
      data.updated = new Date().toISOString();
      fs.writeFileSync(indexPath, JSON.stringify(data, null, 2) + "\n");
      changes.push(indexPath);
    }
  }

  const schedPath = path.join(ROOT, "00_Brand/Channel-Setup/YOUTUBE_CANONICAL_LIVE_SCHEDULE.json");
  if (fs.existsSync(schedPath)) {
    const sched = JSON.parse(fs.readFileSync(schedPath, "utf8"));
    let touched = false;
    for (const e of sched.entries || []) {
      if (e.youtubeId === oldId) {
        e.youtubeId = newId;
        e.previousYoutubeId = oldId;
        e.cfrReuploadAt = new Date().toISOString();
        if (publishAt) e.publishAt = publishAt;
        touched = true;
      }
      if (e.parentLongId === oldId) {
        e.parentLongId = newId;
        touched = true;
      }
    }
    if (touched) {
      fs.writeFileSync(schedPath, JSON.stringify(sched, null, 2) + "\n");
      changes.push(schedPath);
    }
  }
  return changes;
}

async function main() {
  const dryRun = flag("dry-run") || !flag("execute");
  const approved = flag("approved-by-user");
  if (!dryRun && !approved) throw new Error("Execution requires --execute --approved-by-user");

  const auditRows = JSON.parse(fs.readFileSync(VIS, "utf8")) as Array<any>;
  const candidates = auditRows.filter((r) => {
    const vis = (r.studio?.visibility || "") as string;
    return vis === "Scheduled" || vis === "Private" || vis === "Unlisted";
  });

  const accessToken = await token();
  const ids = candidates.map((c) => c.video_id);
  const live = await getVideos(accessToken, ids);

  const plan: any[] = [];
  const skipped: any[] = [];
  const now = Date.now();

  for (const c of candidates) {
    const item = live.get(c.video_id);
    if (!item) {
      skipped.push({ id: c.video_id, reason: "not_found_on_api" });
      continue;
    }
    const privacy = item.status?.privacyStatus as string;
    const publishAt = item.status?.publishAt as string | undefined;
    const views = Number(item.statistics?.viewCount || 0);
    const title = item.snippet?.title || c.title || "";
    const filePath = c.file as string;

    if (privacy === "public") {
      skipped.push({ id: c.video_id, reason: "api_public", title });
      continue;
    }
    if (!publishAt) {
      skipped.push({ id: c.video_id, reason: "no_publishAt", privacy, title });
      continue;
    }
    const when = new Date(publishAt).getTime();
    if (!(when > now + MIN_LEAD_MS)) {
      skipped.push({ id: c.video_id, reason: "publishAt_too_soon_or_past", publishAt, title });
      continue;
    }
    if (views > 0) {
      skipped.push({ id: c.video_id, reason: "has_views", views, title });
      continue;
    }
    if (!filePath || !fs.existsSync(filePath)) {
      skipped.push({ id: c.video_id, reason: "missing_file", filePath, title });
      continue;
    }

    plan.push({
      oldId: c.video_id,
      kind: c.kind,
      filePath,
      sizeMb: Math.round(fs.statSync(filePath).size / 1e6),
      title,
      description: item.snippet?.description || "",
      tags: item.snippet?.tags || [],
      categoryId: item.snippet?.categoryId || "27",
      publishAt,
      madeForKids: Boolean(item.status?.selfDeclaredMadeForKids),
      defaultLanguage: item.snippet?.defaultLanguage || "en",
      defaultAudioLanguage: item.snippet?.defaultAudioLanguage || "en-GB",
      privacy,
      views,
    });
  }

  writeJson(path.join(AUDIT, "plan.json"), {
    ranAt: new Date().toISOString(),
    dryRun,
    planCount: plan.length,
    skippedCount: skipped.length,
    plan,
    skipped,
  });
  console.log(`Plan ${plan.length} reuploads; skipped ${skipped.length} → ${path.join(AUDIT, "plan.json")}`);
  for (const p of plan) console.log(`  ${p.oldId} ${p.kind} ${p.publishAt} ${p.sizeMb}MB | ${p.title.slice(0, 50)}`);
  for (const s of skipped) console.log(`  SKIP ${s.id} ${s.reason}`);

  if (dryRun) {
    console.log("Dry-run only. Re-run with --execute --approved-by-user");
    return;
  }

  const results: any[] = [];
  for (const job of plan) {
    console.log(`\n==> ${job.oldId} ← ${path.basename(job.filePath)}`);
    try {
      // refresh token periodically for long uploads
      const access = await token();
      const uploaded = await uploadScheduled(access, {
        filePath: job.filePath,
        title: job.title,
        description: job.description,
        tags: job.tags,
        categoryId: job.categoryId,
        publishAtIso: job.publishAt,
        madeForKids: job.madeForKids,
        defaultLanguage: job.defaultLanguage,
        defaultAudioLanguage: job.defaultAudioLanguage,
      });
      const newId = uploaded.id;
      console.log(`  uploaded ${newId}`);

      // verify schedule
      const check = await getVideos(access, [newId]);
      const snap = check.get(newId);
      const okSched =
        snap?.status?.privacyStatus === "private" && snap?.status?.publishAt === job.publishAt;
      if (!okSched) {
        throw new Error(
          `new video schedule mismatch: privacy=${snap?.status?.privacyStatus} publishAt=${snap?.status?.publishAt}`,
        );
      }

      const ledger = updateLedgers(job.oldId, newId, job.publishAt);
      console.log(`  ledger ${ledger.length} files`);

      await deleteVideo(access, job.oldId);
      console.log(`  deleted old ${job.oldId}`);

      results.push({
        ok: true,
        oldId: job.oldId,
        newId,
        publishAt: job.publishAt,
        title: job.title,
        ledger,
      });
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      console.error(`  FAIL ${msg}`);
      results.push({ ok: false, oldId: job.oldId, error: msg.slice(0, 500) });
    }
    writeJson(path.join(AUDIT, "results.json"), {
      ranAt: new Date().toISOString(),
      ok: results.filter((r) => r.ok).length,
      fail: results.filter((r) => !r.ok).length,
      results,
    });
  }

  console.log(`\nDone ok=${results.filter((r) => r.ok).length} fail=${results.filter((r) => !r.ok).length}`);
  if (results.some((r) => !r.ok)) process.exitCode = 1;
}

main()
  .then(() => prisma.$disconnect())
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
