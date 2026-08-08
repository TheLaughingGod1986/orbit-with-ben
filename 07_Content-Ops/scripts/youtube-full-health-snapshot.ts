#!/usr/bin/env tsx
/**
 * READ-ONLY full-channel health snapshot.
 * Known-ID videos.list only — no search.list forMine. Zero mutations.
 *
 *   npx tsx scripts/youtube-full-health-snapshot.ts
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";

const AUDIT = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/audits/full_channel_health_2026-08-08",
);
const PREV_PATH = path.join(AUDIT, "LIVE_YOUTUBE_SNAPSHOT.json");
const REG_PATH = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/YOUTUBE_CANONICAL_REGISTRY.json",
);

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

const EXCLUDED = [
  "HvAKGjx4lv0",
  "icedH_gK8JE",
  "Web2otrTcT0",
  "1qts3tIsg9c",
  "dPMJQp2gMNc",
  "rFJoOdQAc9c",
  "w1ej9u0rPTA",
  "gPCpMsB0w2E",
  "YsyPMhNmHMk",
];

async function bearerToken(): Promise<string> {
  getEnv();
  const connection = await prisma.platformConnection.findFirst({
    where: {
      platform: "youtube_shorts",
      connectionStatus: "connected",
      disconnectedAt: null,
    },
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

async function main() {
  fs.mkdirSync(AUDIT, { recursive: true });
  const prev = fs.existsSync(PREV_PATH)
    ? JSON.parse(fs.readFileSync(PREV_PATH, "utf8"))
    : { videos: [] };
  const reg = fs.existsSync(REG_PATH)
    ? JSON.parse(fs.readFileSync(REG_PATH, "utf8"))
    : {};

  const ids = new Set<string>([
    ...PUBLIC,
    ...Object.keys(TARGET_SCHED),
    ...EXCLUDED,
    ...(prev.videos || []).map((v: { youtubeId: string }) => v.youtubeId),
    ...(reg.records || []).map((r: { youtubeId?: string }) => r.youtubeId).filter(Boolean),
    ...(reg.historicalDuplicateIdsGlobal || []),
    ...(reg.blockedHistoricalDuplicateIds || []),
  ]);

  const tok = await bearerToken();

  const chBody = await yt(
    tok,
    "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,brandingSettings,topicDetails,contentDetails&mine=true",
  );
  const chItem = (chBody.items || [])[0];
  const channel = {
    id: chItem?.id,
    title: chItem?.snippet?.title,
    customUrl: chItem?.snippet?.customUrl,
    description: chItem?.snippet?.description,
    country: chItem?.snippet?.country,
    publishedAt: chItem?.snippet?.publishedAt,
    stats: chItem?.statistics,
    keywords: chItem?.brandingSettings?.channel?.keywords ?? null,
    unsubscribedTrailer: chItem?.brandingSettings?.channel?.unsubscribedTrailer ?? null,
    defaultLanguage: chItem?.snippet?.defaultLanguage ?? null,
    topicCategories: chItem?.topicDetails?.topicCategories ?? [],
    banner: chItem?.brandingSettings?.image?.bannerExternalUrl ?? null,
  };

  const playlists: Array<{
    id: string;
    title: string;
    itemCount: number;
    privacy: string | null;
  }> = [];
  let pageToken: string | undefined;
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
    pageToken = body.nextPageToken;
  } while (pageToken);

  const idList = [...ids];
  const items: any[] = [];
  for (let i = 0; i < idList.length; i += 50) {
    const chunk = idList.slice(i, i + 50);
    const body = await yt(
      tok,
      `https://www.googleapis.com/youtube/v3/videos?part=status,snippet,statistics,contentDetails&id=${chunk.join(",")}`,
    );
    items.push(...(body.items || []));
  }

  const prevById = Object.fromEntries(
    (prev.videos || []).map((v: any) => [v.youtubeId, v]),
  );

  const videos = items.map((v: any) => {
    const p = prevById[v.id] || {};
    const privacy = v.status?.privacyStatus;
    const publishAt = v.status?.publishAt || null;
    let livePass = true;
    let detail = "ok";
    if (PUBLIC.includes(v.id)) {
      livePass = privacy === "public" && !publishAt;
      detail = livePass
        ? "public_canonical_ok"
        : `expected_public got ${privacy} publishAt=${publishAt}`;
    } else if (TARGET_SCHED[v.id]) {
      livePass = privacy === "private" && publishAt === TARGET_SCHED[v.id];
      detail = livePass
        ? "scheduled_exact"
        : `expected ${TARGET_SCHED[v.id]} private got ${privacy} ${publishAt}`;
    } else if (EXCLUDED.includes(v.id)) {
      livePass = privacy === "private" && !publishAt;
      detail = livePass
        ? "excluded_private_null"
        : `excluded violation ${privacy} ${publishAt}`;
    }
    return {
      youtubeId: v.id,
      title: v.snippet?.title,
      privacyStatus: privacy,
      publishAt,
      publishedAt: v.snippet?.publishedAt,
      duration: v.contentDetails?.duration,
      categoryId: v.snippet?.categoryId,
      description: v.snippet?.description || "",
      tags: v.snippet?.tags || [],
      thumbnails: v.snippet?.thumbnails || {},
      stats: v.statistics || {},
      contentFamily: p.contentFamily || null,
      contentType: p.contentType || null,
      contentId: p.contentId || null,
      relatedLong: p.relatedLong || null,
      classification: p.classification || null,
      expected: p.expected || null,
      livePass,
      detail,
      views: Number(v.statistics?.viewCount || 0),
      likes: Number(v.statistics?.likeCount || 0),
      comments: Number(v.statistics?.commentCount || 0),
      defaultLanguage: v.snippet?.defaultLanguage || null,
      defaultAudioLanguage: v.snippet?.defaultAudioLanguage || null,
      madeForKids: v.status?.madeForKids ?? null,
      uploadStatus: v.status?.uploadStatus || null,
      embeddable: v.status?.embeddable ?? null,
    };
  });

  const byId = Object.fromEntries(videos.map((v) => [v.youtubeId, v]));
  const publicIds = videos.filter((v) => v.privacyStatus === "public").map((v) => v.youtubeId);
  const scheduled = videos.filter((v) => v.publishAt);
  const unexpectedPublic = publicIds.filter((id) => !PUBLIC.includes(id));
  const missingPublic = PUBLIC.filter((id) => !(byId[id] && byId[id].privacyStatus === "public"));
  const missingScheduled = Object.keys(TARGET_SCHED).filter((id) => {
    const v = byId[id];
    return !(v && v.privacyStatus === "private" && v.publishAt === TARGET_SCHED[id]);
  });
  const unexpectedScheduled = scheduled
    .map((v) => v.youtubeId)
    .filter((id) => !TARGET_SCHED[id]);
  const wrongTime = Object.entries(TARGET_SCHED)
    .filter(([id, exp]) => {
      const v = byId[id];
      return v && v.publishAt && v.publishAt !== exp;
    })
    .map(([id, exp]) => ({ id, expected: exp, actual: byId[id]?.publishAt }));
  const slotMap: Record<string, string[]> = {};
  for (const v of scheduled) {
    (slotMap[v.publishAt!] ||= []).push(v.youtubeId);
  }
  const collisions = Object.values(slotMap).filter((a) => a.length > 1).length;
  const placeholders = scheduled.filter((v) => (v.publishAt || "").startsWith("2026-12-31")).length;
  const excludedViolations = EXCLUDED.map((id) => {
    const v = byId[id];
    const privacy = v?.privacyStatus ?? "MISSING";
    const publishAt = v?.publishAt ?? null;
    return { id, privacy, publishAt, ok: privacy === "private" && !publishAt };
  });

  const scheduledExact = Object.keys(TARGET_SCHED).filter(
    (id) => byId[id]?.publishAt === TARGET_SCHED[id] && byId[id]?.privacyStatus === "private",
  ).length;

  const integrity = {
    watchedIds: idList.length,
    returned: videos.length,
    publicCount: publicIds.length,
    expectedPublic: PUBLIC.length,
    missingPublic,
    unexpectedPublic,
    scheduledCount: scheduledExact,
    expectedScheduled: Object.keys(TARGET_SCHED).length,
    missingScheduled,
    unexpectedScheduled,
    wrongTime,
    collisions,
    placeholders,
    excludedViolations,
    shelfOk: missingPublic.length === 0 && unexpectedPublic.length === 0,
    shelfUnexpectedPublic: unexpectedPublic,
  };

  const out = {
    fetchedAt: new Date().toISOString(),
    mutation: "NONE",
    quota: {
      method: "known-id videos.list + channels.list + playlists.list mine",
      searchListForMine: false,
    },
    channel,
    playlists,
    integrity,
    videos,
  };

  fs.writeFileSync(path.join(AUDIT, "LIVE_YOUTUBE_SNAPSHOT.json"), JSON.stringify(out, null, 2) + "\n");
  console.log(
    JSON.stringify(
      {
        fetchedAt: out.fetchedAt,
        returned: videos.length,
        publicCount: integrity.publicCount,
        scheduledExact: integrity.scheduledCount,
        unexpectedPublic: integrity.unexpectedPublic,
        missingPublic: integrity.missingPublic,
        missingScheduled: integrity.missingScheduled,
        wrongTime: integrity.wrongTime,
        collisions: integrity.collisions,
        placeholders: integrity.placeholders,
        playlists: playlists.length,
        excludedAllOk: excludedViolations.every((x) => x.ok),
        shelfOk: integrity.shelfOk,
        channelStats: channel.stats,
      },
      null,
      2,
    ),
  );
}

main()
  .catch((err) => {
    console.error(err);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
