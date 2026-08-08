#!/usr/bin/env tsx
/**
 * Controlled P1 growth/SEO optimisation.
 *
 * Safety:
 * - Never mutates privacyStatus / publishAt
 * - Never uploads/deletes/creates video IDs
 * - Never speculative title/thumbnail rewrites
 * - Idempotent playlists + descriptions
 *
 *   npx tsx scripts/youtube-growth-optimise.ts --dry-run
 *   npx tsx scripts/youtube-growth-optimise.ts --allow-emergency-unfreeze --execute
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";
import { hasForceSslScope, parseGrantedScopes } from "../src/lib/publishing/youtube-oauth";
import { assertYouTubeMutationAllowed } from "../src/lib/publishing/youtube-freeze";
import {
  APPROVED_SCHEDULE,
  CHANNEL_DESCRIPTION_AFTER,
  CHANNEL_KEYWORDS,
  PLAYLIST_SPECS,
  PUBLIC_CANONICAL_IDS,
  assertNoScheduleFieldsInSnippetUpdate,
  buildRegistryRelationFixes,
  buildShortDescriptionPlans,
  descriptionAlreadyOptimised,
  formatChannelKeywordsForApi,
  playlistTitleCollisionKey,
  scoreGrowthReadiness,
} from "../src/lib/publishing/youtube-growth-optimisation";

const AUDIT = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/audits/channel_growth_optimisation_2026-08-08",
);
const REG_PATH = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/YOUTUBE_CANONICAL_REGISTRY.json",
);

function flag(name: string): boolean {
  return process.argv.includes(`--${name}`);
}

function nowIso(): string {
  return new Date().toISOString();
}

function writeJson(name: string, data: unknown) {
  fs.mkdirSync(AUDIT, { recursive: true });
  fs.writeFileSync(path.join(AUDIT, name), JSON.stringify(data, null, 2) + "\n");
}

function appendChangelog(entry: Record<string, unknown>) {
  const p = path.join(AUDIT, "OPTIMISATION_CHANGELOG.jsonl");
  fs.appendFileSync(p, JSON.stringify({ timestamp: nowIso(), ...entry }) + "\n");
}

async function bearerToken(): Promise<{ token: string; channelId: string }> {
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
  const scopes = parseGrantedScopes(connection.grantedScopes);
  if (!hasForceSslScope(scopes)) {
    throw new Error("UPLOAD BLOCKED: youtube.force-ssl missing — reconnect first");
  }
  const adapter = new YouTubePublishingAdapter();
  if (
    connection.accessTokenExpiresAt &&
    connection.accessTokenExpiresAt.getTime() < Date.now() + 60_000 &&
    adapter.refreshConnection
  ) {
    await adapter.refreshConnection(connection);
  }
  const fresh = await prisma.platformConnection.findUnique({ where: { id: connection.id } });
  const token = decryptSecret(fresh!.accessTokenEncrypted!);
  const ch = await yt(token, "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true");
  const channelId = ch.items?.[0]?.id;
  if (!channelId) throw new Error("No channel id");
  return { token, channelId };
}

async function yt(token: string, url: string, init?: RequestInit) {
  const res = await fetch(url, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(init?.body ? { "Content-Type": "application/json" } : {}),
      ...(init?.headers || {}),
    },
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(
      `${init?.method || "GET"} ${url} -> ${res.status} ${JSON.stringify(body).slice(0, 600)}`,
    ) as Error & { status?: number; body?: unknown };
    err.status = res.status;
    err.body = body;
    throw err;
  }
  return body;
}

async function fetchVideos(token: string, ids: string[]) {
  const items: any[] = [];
  for (let i = 0; i < ids.length; i += 50) {
    const chunk = ids.slice(i, i + 50);
    const body = await yt(
      token,
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,statistics,contentDetails&id=${chunk.join(",")}`,
    );
    items.push(...(body.items || []));
  }
  return items;
}

async function listPlaylists(token: string) {
  const out: any[] = [];
  let pageToken: string | undefined;
  do {
    const u = new URL("https://www.googleapis.com/youtube/v3/playlists");
    u.searchParams.set("part", "snippet,status,contentDetails");
    u.searchParams.set("mine", "true");
    u.searchParams.set("maxResults", "50");
    if (pageToken) u.searchParams.set("pageToken", pageToken);
    const body = await yt(token, u.toString());
    out.push(...(body.items || []));
    pageToken = body.nextPageToken;
  } while (pageToken);
  return out;
}

async function listPlaylistItemIds(token: string, playlistId: string): Promise<string[]> {
  const ids: string[] = [];
  let pageToken: string | undefined;
  do {
    const u = new URL("https://www.googleapis.com/youtube/v3/playlistItems");
    u.searchParams.set("part", "snippet,contentDetails");
    u.searchParams.set("playlistId", playlistId);
    u.searchParams.set("maxResults", "50");
    if (pageToken) u.searchParams.set("pageToken", pageToken);
    const body = await yt(token, u.toString());
    for (const it of body.items || []) {
      const vid = it.contentDetails?.videoId || it.snippet?.resourceId?.videoId;
      if (vid) ids.push(vid);
    }
    pageToken = body.nextPageToken;
  } while (pageToken);
  return ids;
}

type Integrity = {
  publicOk: boolean;
  scheduleOk: boolean;
  unexpectedPublic: string[];
  missingPublic: string[];
  missingScheduled: string[];
  unexpectedScheduled: string[];
  wrongTime: Array<{ id: string; expected: string; actual: string | null }>;
  collisions: number;
  placeholders: number;
  details: Record<string, { privacy: string; publishAt: string | null; title: string }>;
};

function evaluateIntegrity(items: any[]): Integrity {
  const byId = Object.fromEntries(items.map((v) => [v.id, v]));
  const publicIds = items
    .filter((v) => v.status?.privacyStatus === "public")
    .map((v) => v.id as string);
  const unexpectedPublic = publicIds.filter((id) => !(PUBLIC_CANONICAL_IDS as readonly string[]).includes(id));
  const missingPublic = (PUBLIC_CANONICAL_IDS as readonly string[]).filter(
    (id) => byId[id]?.status?.privacyStatus !== "public",
  );
  const scheduled = items.filter((v) => v.status?.publishAt);
  const unexpectedScheduled = scheduled
    .map((v) => v.id as string)
    .filter((id) => !APPROVED_SCHEDULE[id]);
  const missingScheduled = Object.keys(APPROVED_SCHEDULE).filter((id) => {
    const v = byId[id];
    return !(
      v &&
      v.status?.privacyStatus === "private" &&
      v.status?.publishAt === APPROVED_SCHEDULE[id]
    );
  });
  const wrongTime = Object.entries(APPROVED_SCHEDULE)
    .filter(([id, exp]) => {
      const v = byId[id];
      return v && v.status?.publishAt && v.status.publishAt !== exp;
    })
    .map(([id, exp]) => ({
      id,
      expected: exp,
      actual: byId[id]?.status?.publishAt || null,
    }));
  const slot: Record<string, string[]> = {};
  for (const v of scheduled) {
    (slot[v.status.publishAt] ||= []).push(v.id);
  }
  const collisions = Object.values(slot).filter((a) => a.length > 1).length;
  const placeholders = scheduled.filter((v: any) =>
    String(v.status?.publishAt || "").startsWith("2026-12-31"),
  ).length;
  const details: Integrity["details"] = {};
  for (const id of [
    ...(PUBLIC_CANONICAL_IDS as readonly string[]),
    ...Object.keys(APPROVED_SCHEDULE),
  ]) {
    const v = byId[id];
    if (!v) continue;
    details[id] = {
      privacy: v.status?.privacyStatus,
      publishAt: v.status?.publishAt || null,
      title: v.snippet?.title,
    };
  }
  return {
    publicOk: missingPublic.length === 0 && unexpectedPublic.length === 0,
    scheduleOk:
      missingScheduled.length === 0 &&
      unexpectedScheduled.length === 0 &&
      wrongTime.length === 0 &&
      collisions === 0 &&
      placeholders === 0,
    unexpectedPublic,
    missingPublic,
    missingScheduled,
    unexpectedScheduled,
    wrongTime,
    collisions,
    placeholders,
    details,
  };
}

async function updateVideoSnippetOnly(input: {
  token: string;
  item: any;
  description?: string;
  categoryId?: string;
  defaultLanguage?: string;
  defaultAudioLanguage?: string;
  tags?: string[];
  dry: boolean;
}) {
  const { token, item, dry } = input;
  const snippet = {
    title: item.snippet.title,
    description: input.description ?? item.snippet.description ?? "",
    categoryId: input.categoryId ?? item.snippet.categoryId,
    tags: input.tags ?? item.snippet.tags ?? [],
    defaultLanguage: input.defaultLanguage ?? item.snippet.defaultLanguage,
    defaultAudioLanguage:
      input.defaultAudioLanguage ?? item.snippet.defaultAudioLanguage,
  };
  const body = { id: item.id, snippet };
  assertNoScheduleFieldsInSnippetUpdate(body as any);
  if (dry) return { ok: true, dryRun: true, body };
  const res = await yt(token, "https://www.googleapis.com/youtube/v3/videos?part=snippet", {
    method: "PUT",
    body: JSON.stringify(body),
  });
  return { ok: true, dryRun: false, responseId: res.id };
}

async function main() {
  const dry = flag("dry-run") || !flag("execute");
  const execute = flag("execute");
  if (execute && !flag("allow-emergency-unfreeze")) {
    console.error("Live execute requires --allow-emergency-unfreeze (publishing freeze active)");
    process.exit(2);
  }
  if (execute) {
    assertYouTubeMutationAllowed({
      allowEmergencyUnfreeze: true,
      operation: "youtube-growth-optimise",
    });
  }

  fs.mkdirSync(AUDIT, { recursive: true });
  const { token, channelId } = await bearerToken();

  // ── Integrity gate (known IDs only) ──────────────────────────────
  const watchIds = [
    ...(PUBLIC_CANONICAL_IDS as readonly string[]),
    ...Object.keys(APPROVED_SCHEDULE),
  ];
  const beforeItems = await fetchVideos(token, watchIds);
  const beforeIntegrity = evaluateIntegrity(beforeItems);
  writeJson("LIVE_INTEGRITY_BEFORE.json", { fetchedAt: nowIso(), ...beforeIntegrity });

  if (!beforeIntegrity.publicOk || !beforeIntegrity.scheduleOk) {
    const blocked = {
      fetchedAt: nowIso(),
      beforeIntegrity,
      message: "OPTIMISATION BLOCKED — integrity failure",
    };
    writeJson("OPTIMISATION_BLOCKED_INTEGRITY_FAILURE.json", blocked);
    fs.writeFileSync(
      path.join(AUDIT, "OPTIMISATION_BLOCKED_INTEGRITY_FAILURE.md"),
      `# OPTIMISATION BLOCKED — Integrity Failure\n\n\`\`\`json\n${JSON.stringify(blocked, null, 2)}\n\`\`\`\n`,
    );
    console.error("OPTIMISATION_BLOCKED_INTEGRITY_FAILURE");
    process.exit(20);
  }

  const chBody = await yt(
    token,
    "https://www.googleapis.com/youtube/v3/channels?part=snippet,brandingSettings,statistics&mine=true",
  );
  const ch = chBody.items[0];
  const beforeKeywords = ch.brandingSettings?.channel?.keywords ?? null;
  const beforeDesc = ch.snippet?.description ?? "";
  writeJson("CHANNEL_BEFORE.json", {
    fetchedAt: nowIso(),
    id: channelId,
    title: ch.snippet?.title,
    description: beforeDesc,
    keywords: beforeKeywords,
    stats: ch.statistics,
  });

  const existingPlaylists = await listPlaylists(token);
  writeJson("PLAYLISTS_BEFORE.json", {
    fetchedAt: nowIso(),
    count: existingPlaylists.length,
    playlists: existingPlaylists.map((p: any) => ({
      id: p.id,
      title: p.snippet?.title,
      itemCount: p.contentDetails?.itemCount,
    })),
  });

  const byId = Object.fromEntries(beforeItems.map((v) => [v.id, v]));
  const descPlans = buildShortDescriptionPlans();
  const descActions = descPlans.map((plan) => {
    const item = byId[plan.youtubeId];
    const current = item?.snippet?.description || "";
    const already = descriptionAlreadyOptimised(current, plan.description);
    const needsLang =
      item &&
      (item.snippet?.defaultLanguage !== "en-GB" ||
        item.snippet?.defaultAudioLanguage !== "en-GB" ||
        item.snippet?.categoryId !== "27");
    return {
      ...plan,
      current,
      already,
      needsLang: Boolean(needsLang),
      action: already && !needsLang ? "skip" : already ? "lang_only" : "update_description",
    };
  });

  // BH long audio language fix (snippet only)
  const bhLong = byId["3xrxdmaOwJI"];
  const bhLongLangFix =
    bhLong &&
    (bhLong.snippet?.defaultAudioLanguage !== "en-GB" ||
      bhLong.snippet?.defaultLanguage !== "en-GB");

  const exoJwstLangFixes = Object.keys(APPROVED_SCHEDULE)
    .filter((id) => {
      const it = byId[id];
      if (!it) return false;
      return (
        it.snippet?.defaultLanguage !== "en-GB" ||
        it.snippet?.defaultAudioLanguage !== "en-GB" ||
        it.snippet?.categoryId !== "27"
      );
    })
    .map((id) => id);

  const plan = {
    dryRun: dry,
    execute,
    channel: {
      keywordsBefore: beforeKeywords,
      keywordsAfter: formatChannelKeywordsForApi(CHANNEL_KEYWORDS),
      descriptionBefore: beforeDesc,
      descriptionAfter: CHANNEL_DESCRIPTION_AFTER,
      descriptionChange: beforeDesc.trim() !== CHANNEL_DESCRIPTION_AFTER.trim(),
      keywordsChange: (beforeKeywords || "").trim() !== formatChannelKeywordsForApi(CHANNEL_KEYWORDS),
    },
    playlists: PLAYLIST_SPECS.map((spec) => {
      const hit = existingPlaylists.find(
        (p: any) =>
          playlistTitleCollisionKey(p.snippet?.title || "") ===
          playlistTitleCollisionKey(spec.title),
      );
      return {
        ...spec,
        existingId: hit?.id || null,
        create: !hit,
      };
    }),
    descriptions: descActions,
    bhLongLangFix: Boolean(bhLongLangFix),
    langCategoryTargets: exoJwstLangFixes,
  };
  writeJson(dry ? "OPTIMISATION_PLAN_DRY_RUN.json" : "OPTIMISATION_PLAN.json", plan);

  if (dry) {
    console.log(
      JSON.stringify(
        {
          mode: "DRY_RUN",
          integrity: "PASS",
          playlistCreates: plan.playlists.filter((p) => p.create).length,
          playlistReuse: plan.playlists.filter((p) => !p.create).length,
          descriptionUpdates: descActions.filter((d) => d.action === "update_description").length,
          langOnly: descActions.filter((d) => d.action === "lang_only").length,
          keywordsChange: plan.channel.keywordsChange,
          descriptionChange: plan.channel.descriptionChange,
          bhLongLangFix: plan.bhLongLangFix,
          langCategoryTargets: plan.langCategoryTargets.length,
        },
        null,
        2,
      ),
    );
    return;
  }

  // ── Batch 1: channel metadata ────────────────────────────────────
  if (plan.channel.keywordsChange || plan.channel.descriptionChange) {
    // Preserve full brandingSettings to avoid wiping banner/image fields.
    const brandingSettings = JSON.parse(JSON.stringify(ch.brandingSettings || {}));
    brandingSettings.channel = brandingSettings.channel || {};
    brandingSettings.channel.keywords = formatChannelKeywordsForApi(CHANNEL_KEYWORDS);
    await yt(
      token,
      "https://www.googleapis.com/youtube/v3/channels?part=snippet,brandingSettings",
      {
        method: "PUT",
        body: JSON.stringify({
          id: channelId,
          snippet: {
            title: ch.snippet.title,
            description: CHANNEL_DESCRIPTION_AFTER,
            defaultLanguage: ch.snippet.defaultLanguage || "en-GB",
            country: ch.snippet.country,
          },
          brandingSettings,
        }),
      },
    );
    appendChangelog({
      resource: "channel",
      youtubeId: channelId,
      field: "description+keywords",
      before: { description: beforeDesc, keywords: beforeKeywords },
      after: {
        description: CHANNEL_DESCRIPTION_AFTER,
        keywords: formatChannelKeywordsForApi(CHANNEL_KEYWORDS),
      },
      reason: "P1 channel SEO + subscriber CTA + JWST topical coverage",
      verification: "pending_readback",
    });
  }

  // ── Batch 2: playlists ───────────────────────────────────────────
  const playlistResults: any[] = [];
  for (const spec of plan.playlists) {
    let playlistId = spec.existingId as string | null;
    if (!playlistId) {
      const created = await yt(
        token,
        "https://www.googleapis.com/youtube/v3/playlists?part=snippet,status",
        {
          method: "POST",
          body: JSON.stringify({
            snippet: {
              title: spec.title,
              description: spec.description,
            },
            status: { privacyStatus: "public" },
          }),
        },
      );
      playlistId = created.id;
      appendChangelog({
        resource: "playlist",
        youtubeId: playlistId,
        field: "create",
        before: null,
        after: { title: spec.title },
        reason: `playlist architecture: ${spec.key}`,
        verification: "created",
      });
    } else {
      // Ensure description is up to date (idempotent update)
      await yt(token, "https://www.googleapis.com/youtube/v3/playlists?part=snippet", {
        method: "PUT",
        body: JSON.stringify({
          id: playlistId,
          snippet: {
            title: spec.title,
            description: spec.description,
          },
        }),
      });
    }

    const existingItems = await listPlaylistItemIds(token, playlistId!);
    const existingSet = new Set(existingItems);
    const added: string[] = [];
    const skipped: string[] = [];
    for (const videoId of spec.videoIds) {
      if (existingSet.has(videoId)) {
        skipped.push(videoId);
        continue;
      }
      await yt(token, "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet", {
        method: "POST",
        body: JSON.stringify({
          snippet: {
            playlistId,
            resourceId: { kind: "youtube#video", videoId },
          },
        }),
      });
      added.push(videoId);
      existingSet.add(videoId);
      appendChangelog({
        resource: "playlistItem",
        youtubeId: videoId,
        field: "playlistMembership",
        before: null,
        after: { playlistId, title: spec.title },
        reason: `add to ${spec.key}`,
        verification: "inserted",
      });
    }
    playlistResults.push({
      key: spec.key,
      playlistId,
      added,
      skipped,
      title: spec.title,
    });
  }
  writeJson("PLAYLIST_APPLY_RESULT.json", { appliedAt: nowIso(), playlistResults });

  // ── Batch 3: Short descriptions (+ lang/category where needed) ───
  const descResults: any[] = [];
  for (const action of descActions) {
    const item = byId[action.youtubeId];
    if (!item) {
      descResults.push({ id: action.youtubeId, ok: false, error: "missing" });
      continue;
    }
    if (action.action === "skip") {
      descResults.push({ id: action.youtubeId, skipped: true, reason: "already_optimised" });
      continue;
    }
    const beforeDescVid = item.snippet?.description || "";
    const beforeMeta = {
      description: beforeDescVid,
      defaultLanguage: item.snippet?.defaultLanguage || null,
      defaultAudioLanguage: item.snippet?.defaultAudioLanguage || null,
      categoryId: item.snippet?.categoryId || null,
      publishAt: item.status?.publishAt || null,
      privacy: item.status?.privacyStatus || null,
    };
    await updateVideoSnippetOnly({
      token,
      item,
      description: action.action === "lang_only" ? beforeDescVid : action.description,
      categoryId: "27",
      defaultLanguage: "en-GB",
      defaultAudioLanguage: "en-GB",
      dry: false,
    });
    // refresh local cache for later integrity
    item.snippet.description =
      action.action === "lang_only" ? beforeDescVid : action.description;
    item.snippet.defaultLanguage = "en-GB";
    item.snippet.defaultAudioLanguage = "en-GB";
    item.snippet.categoryId = "27";
    appendChangelog({
      resource: "video",
      youtubeId: action.youtubeId,
      field: "snippet.description+lang+category",
      before: beforeMeta,
      after: {
        description: item.snippet.description,
        defaultLanguage: "en-GB",
        defaultAudioLanguage: "en-GB",
        categoryId: "27",
        publishAt: beforeMeta.publishAt,
        privacy: beforeMeta.privacy,
      },
      reason: action.reason,
      verification: "pending_readback",
      scheduleUntouched: true,
      privacyUntouched: true,
    });
    descResults.push({ id: action.youtubeId, ok: true, action: action.action });
  }

  // BH long en-GB audio
  if (bhLong && bhLongLangFix) {
    const before = {
      defaultLanguage: bhLong.snippet?.defaultLanguage,
      defaultAudioLanguage: bhLong.snippet?.defaultAudioLanguage,
      publishAt: bhLong.status?.publishAt || null,
      privacy: bhLong.status?.privacyStatus,
    };
    await updateVideoSnippetOnly({
      token,
      item: bhLong,
      defaultLanguage: "en-GB",
      defaultAudioLanguage: "en-GB",
      categoryId: "27",
      dry: false,
    });
    appendChangelog({
      resource: "video",
      youtubeId: "3xrxdmaOwJI",
      field: "snippet.language",
      before,
      after: { defaultLanguage: "en-GB", defaultAudioLanguage: "en-GB", categoryId: "27" },
      reason: "align BH long audio language to en-GB",
      verification: "pending_readback",
      scheduleUntouched: true,
      privacyUntouched: true,
    });
  }

  // Remaining scheduled longs/shorts lang+category without description rewrite if not in descPlans
  const descIds = new Set(descActions.map((d) => d.youtubeId));
  for (const id of exoJwstLangFixes) {
    if (descIds.has(id)) continue;
    if (id === "3xrxdmaOwJI") continue;
    const item = byId[id];
    if (!item) continue;
    const before = {
      defaultLanguage: item.snippet?.defaultLanguage,
      defaultAudioLanguage: item.snippet?.defaultAudioLanguage,
      categoryId: item.snippet?.categoryId,
      publishAt: item.status?.publishAt || null,
      privacy: item.status?.privacyStatus,
    };
    await updateVideoSnippetOnly({
      token,
      item,
      defaultLanguage: "en-GB",
      defaultAudioLanguage: "en-GB",
      categoryId: "27",
      dry: false,
    });
    appendChangelog({
      resource: "video",
      youtubeId: id,
      field: "snippet.language+category",
      before,
      after: { defaultLanguage: "en-GB", defaultAudioLanguage: "en-GB", categoryId: "27" },
      reason: "metadata consistency en-GB + Education category",
      verification: "pending_readback",
      scheduleUntouched: true,
      privacyUntouched: true,
    });
  }
  writeJson("DESCRIPTION_APPLY_RESULT.json", { appliedAt: nowIso(), descResults });

  // ── Batch 4: local registry relations ────────────────────────────
  const reg = JSON.parse(fs.readFileSync(REG_PATH, "utf8"));
  const fixes = buildRegistryRelationFixes(reg.records || []);
  for (const fix of fixes) {
    const rec = (reg.records || []).find((r: any) => r.youtubeVideoId === fix.youtubeVideoId);
    if (!rec) continue;
    const before = rec.relatedLongFormVideoId;
    rec.relatedLongFormVideoId = fix.relatedLongFormVideoId;
    appendChangelog({
      resource: "registry",
      youtubeId: fix.youtubeVideoId,
      field: "relatedLongFormVideoId",
      before,
      after: fix.relatedLongFormVideoId,
      reason: fix.reason,
      verification: "local_only",
    });
  }
  reg.updatedAt = nowIso();
  reg.growthOptimisedAt = nowIso();
  fs.writeFileSync(REG_PATH, JSON.stringify(reg, null, 2) + "\n");
  writeJson("REGISTRY_RELATION_FIXES.json", { appliedAt: nowIso(), fixes });

  // ── Read-back + freeze verify ────────────────────────────────────
  const afterItems = await fetchVideos(token, watchIds);
  const afterIntegrity = evaluateIntegrity(afterItems);
  writeJson("LIVE_INTEGRITY_AFTER.json", { fetchedAt: nowIso(), ...afterIntegrity });

  const afterCh = await yt(
    token,
    "https://www.googleapis.com/youtube/v3/channels?part=snippet,brandingSettings,statistics&mine=true",
  );
  const afterPlaylists = await listPlaylists(token);
  writeJson("CHANNEL_AFTER.json", {
    fetchedAt: nowIso(),
    description: afterCh.items?.[0]?.snippet?.description,
    keywords: afterCh.items?.[0]?.brandingSettings?.channel?.keywords ?? null,
    stats: afterCh.items?.[0]?.statistics,
  });
  writeJson("PLAYLISTS_AFTER.json", {
    fetchedAt: nowIso(),
    count: afterPlaylists.length,
    playlists: afterPlaylists.map((p: any) => ({
      id: p.id,
      title: p.snippet?.title,
      itemCount: p.contentDetails?.itemCount,
    })),
  });

  if (!afterIntegrity.publicOk || !afterIntegrity.scheduleOk) {
    console.error("CRITICAL: integrity regression after optimisation");
    writeJson("INTEGRITY_REGRESSION.json", { beforeIntegrity, afterIntegrity });
    process.exit(30);
  }

  // Verify schedule bytes unchanged for approved IDs
  const scheduleMutations: any[] = [];
  for (const id of Object.keys(APPROVED_SCHEDULE)) {
    const b = beforeIntegrity.details[id];
    const a = afterIntegrity.details[id];
    if (!b || !a) continue;
    if (b.publishAt !== a.publishAt || b.privacy !== a.privacy) {
      scheduleMutations.push({ id, before: b, after: a });
    }
  }
  writeJson("SCHEDULE_FREEZE_VERIFY.json", {
    scheduleMutations,
    ok: scheduleMutations.length === 0,
  });
  if (scheduleMutations.length) {
    console.error("CRITICAL: schedule/privacy mutation detected");
    process.exit(31);
  }

  // Description read-back for planned IDs
  const afterById = Object.fromEntries(afterItems.map((v) => [v.id, v]));
  const descVerify = descPlans.map((p) => {
    const got = afterById[p.youtubeId]?.snippet?.description || "";
    const ok = descriptionAlreadyOptimised(got, p.description);
    const wrongParent = /youtu\.be\/1wxUhF3XnwI/.test(got);
    return {
      id: p.youtubeId,
      ok,
      wrongParentGone: !wrongParent,
      parentLink: (got.match(/youtu\.be\/([\w-]+)/) || [])[1] || null,
    };
  });
  writeJson("DESCRIPTION_READBACK.json", { verifiedAt: nowIso(), descVerify });

  const thinRemaining = descVerify.filter((d) => !d.ok).length;
  const wrongParentRemaining = descVerify.filter((d) => !d.wrongParentGone).length;
  const scores = scoreGrowthReadiness({
    playlists: afterPlaylists.length,
    keywordsSet: Boolean(afterCh.items?.[0]?.brandingSettings?.channel?.keywords),
    channelDescMentionsJwst: /James Webb|JWST/i.test(
      afterCh.items?.[0]?.snippet?.description || "",
    ),
    thinShortDescriptionsRemaining: thinRemaining,
    wrongParentLinksRemaining: wrongParentRemaining,
    orphanShortsInRegistry: buildRegistryRelationFixes(
      JSON.parse(fs.readFileSync(REG_PATH, "utf8")).records || [],
    ).length,
    studioManualRemaining: 6,
  });
  writeJson("SCORES_AFTER.json", { scoredAt: nowIso(), ...scores });

  console.log(
    JSON.stringify(
      {
        mode: "EXECUTE",
        integrityAfter: "PASS",
        scheduleMutations: 0,
        playlists: afterPlaylists.length,
        descriptionOk: descVerify.filter((d) => d.ok).length,
        descriptionTotal: descVerify.length,
        wrongParentRemaining,
        scores,
      },
      null,
      2,
    ),
  );
}

main()
  .catch((err) => {
    console.error(err);
    if (String(err.message || err).includes("quotaExceeded") || (err as any)?.status === 403) {
      writeJson("WAITING_FOR_YOUTUBE_API_QUOTA.json", {
        at: nowIso(),
        error: String(err.message || err).slice(0, 1000),
      });
      console.error("WAITING_FOR_YOUTUBE_API_QUOTA");
      process.exit(40);
    }
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
