#!/usr/bin/env tsx
/**
 * Final visibility repair + approved 13-slot schedule apply.
 *
 *   npm run youtube:final-schedule-closure -- --dry-run
 *   npm run youtube:final-schedule-closure -- --allow-emergency-unfreeze --execute
 *
 * Phases: BEFORE snapshot → privatize HvAKGjx4lv0 → clear excluded publishAts
 * → apply 13 schedules one-by-one (stop on fail) → AFTER artifacts.
 *
 * No upload / delete / re-upload / CDP. Existing IDs only.
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";
import { hasForceSslScope, parseGrantedScopes } from "../src/lib/publishing/youtube-oauth";
import { assertYouTubeMutationAllowed } from "../src/lib/publishing/youtube-freeze";
import { assertNotPlaceholderHoldPublishAt } from "../src/lib/publishing/youtube-schedule-guards";

const AUDIT = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07",
);
const CALENDAR = path.join(AUDIT, "PROPOSED_CANONICAL_RELEASE_CALENDAR.json");
const REGISTRY = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/YOUTUBE_CANONICAL_REGISTRY.json",
);
const RECOVERY = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/YOUTUBE_RECOVERY_MODE.json",
);

const APPROVED_PUBLIC = [
  "Mo93x0fxB1Q",
  "1HuV8o3gOss",
  "KcKBixwmcV4",
  "3xrxdmaOwJI",
  "JRfhE6yWom4",
  "L2OFjL4neOo",
] as const;

const NOT_READY = [
  "HvAKGjx4lv0",
  "icedH_gK8JE",
  "Web2otrTcT0",
  "1qts3tIsg9c",
  "dPMJQp2gMNc",
  "rFJoOdQAc9c",
] as const;

const HELD_CLEAR = ["w1ej9u0rPTA", "gPCpMsB0w2E", "YsyPMhNmHMk"] as const;

const WATCH = Array.from(
  new Set([...APPROVED_PUBLIC, ...NOT_READY, ...HELD_CLEAR]),
);

function flag(name: string) {
  return process.argv.includes(`--${name}`);
}

function nowIso() {
  return new Date().toISOString();
}

function norm(s: string | null | undefined) {
  return (s || "").replace(/\.\d{3}Z$/, "Z") || null;
}

function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
}

async function token(): Promise<{ accessToken: string; scopes: string[] }> {
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
  const accessToken = decryptSecret(fresh!.accessTokenEncrypted!);
  const scopes = parseGrantedScopes(
    (fresh as { grantedScopes?: string | null })?.grantedScopes ||
      (connection as { grantedScopes?: string | null }).grantedScopes ||
      "[]",
  );
  return { accessToken, scopes };
}

async function getVideos(accessToken: string, ids: string[]) {
  const map = new Map<string, any>();
  for (let i = 0; i < ids.length; i += 40) {
    const chunk = ids.slice(i, i + 40);
    const res = await fetch(
      `https://www.googleapis.com/youtube/v3/videos?part=status,snippet,statistics&id=${chunk.join(",")}`,
      { headers: { Authorization: `Bearer ${accessToken}` } },
    );
    const body = await res.json();
    if (!res.ok) throw new Error(JSON.stringify(body));
    for (const it of body.items || []) map.set(it.id, it);
  }
  return map;
}

async function updateStatus(
  accessToken: string,
  id: string,
  status: Record<string, unknown>,
  dryRun: boolean,
) {
  if (dryRun) return { dryRun: true, ok: true, id, status, body: { status } };
  const res = await fetch("https://www.googleapis.com/youtube/v3/videos?part=status", {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id, status }),
  });
  const body = await res.json();
  return { ok: res.ok, statusCode: res.status, id, body, status };
}

async function samplePrivacy(accessToken: string, id: string, n: number) {
  const samples: Array<{ privacy: string | null; publishAt: string | null }> = [];
  for (let i = 0; i < n; i++) {
    if (i) await sleep(600);
    const check = await getVideos(accessToken, [id]);
    const it = check.get(id);
    samples.push({
      privacy: it?.status?.privacyStatus || null,
      publishAt: it?.status?.publishAt || null,
    });
  }
  return samples;
}

/** Private + clear publishAt (unlisted→private workaround only if publishAt persists). */
async function setPrivateUnscheduled(
  accessToken: string,
  id: string,
  madeForKids: boolean,
  dryRun: boolean,
  priorStatus?: Record<string, unknown>,
) {
  const statusPayload: Record<string, unknown> = {
    privacyStatus: "private",
    license: priorStatus?.license || "youtube",
    embeddable: priorStatus?.embeddable === true,
    publicStatsViewable: priorStatus?.publicStatsViewable === true,
    selfDeclaredMadeForKids: false,
    madeForKids,
  };
  let result = await updateStatus(accessToken, id, statusPayload, dryRun);
  if (dryRun) {
    return {
      ok: true,
      after: { privacy: "private", publishAt: null },
      result,
      clearedViaUnlistedHop: false,
      samples: [],
    };
  }
  if (!result.ok) {
    const err = JSON.stringify((result as any).body?.error || (result as any).body || {});
    if (/quotaExceeded/i.test(err)) {
      throw new Error(`YouTube quotaExceeded while updating ${id}`);
    }
    return { ok: false, after: null, result, clearedViaUnlistedHop: false, samples: [] };
  }
  // Prefer update-response private, then confirm with sparse samples (avoid quota burn).
  await sleep(2500);
  let samples = await samplePrivacy(accessToken, id, 5);
  let privacyVotes = samples.filter((s) => s.privacy === "private").length;
  let anyPublishAt = samples.some((s) => Boolean(s.publishAt));
  let hopped = false;

  if (anyPublishAt) {
    hopped = true;
    await updateStatus(
      accessToken,
      id,
      { ...statusPayload, privacyStatus: "unlisted" },
      false,
    );
    result = await updateStatus(accessToken, id, statusPayload, false);
    await sleep(2500);
    samples = await samplePrivacy(accessToken, id, 5);
    privacyVotes = samples.filter((s) => s.privacy === "private").length;
    anyPublishAt = samples.some((s) => Boolean(s.publishAt));
  }

  const updateSaidPrivate =
    ((result as any).body?.status?.privacyStatus || "") === "private";
  // Require majority private samples and no publishAt; update response must be private.
  const ok = updateSaidPrivate && privacyVotes >= 3 && !anyPublishAt;
  const last = samples[samples.length - 1] || { privacy: null, publishAt: null };
  return {
    ok,
    after: {
      privacy: privacyVotes >= 3 ? "private" : last.privacy,
      publishAt: anyPublishAt ? last.publishAt : null,
      privacyVotes,
      sampleCount: samples.length,
    },
    result,
    clearedViaUnlistedHop: hopped,
    samples,
  };
}

function snapRow(id: string, it: any, reg: any) {
  const rec =
    (reg.records || []).find(
      (r: any) => (r.youtubeVideoId || r.canonicalYouTubeVideoId) === id,
    ) || null;
  return {
    videoId: id,
    title: it?.snippet?.title || rec?.title || null,
    privacyStatus: it?.status?.privacyStatus || null,
    publishAt: it?.status?.publishAt || null,
    publishedAt: it?.snippet?.publishedAt || null,
    contentId: rec?.internalContentId || null,
    contentFamily: rec?.contentFamily || null,
    sourceFingerprint: rec?.sourceFileFingerprint || null,
    canonicalStatus: APPROVED_PUBLIC.includes(id as any)
      ? "public_canonical"
      : NOT_READY.includes(id as any)
        ? "not_ready"
        : HELD_CLEAR.includes(id as any)
          ? "held_or_extra"
          : "scheduled_candidate",
    views: it?.statistics?.viewCount ?? null,
  };
}

function writeMdTable(title: string, rows: any[]) {
  const lines = [
    `# ${title}`,
    "",
    `Generated: \`${nowIso()}\``,
    "",
    "| videoId | title | privacy | publishAt | contentId | family | canonical |",
    "|---|---|---|---|---|---|---|",
    ...rows.map(
      (r) =>
        `| \`${r.videoId}\` | ${r.title || "—"} | ${r.privacyStatus} | \`${r.publishAt || "null"}\` | \`${r.contentId || "—"}\` | ${r.contentFamily || "—"} | ${r.canonicalStatus} |`,
    ),
    "",
  ];
  return lines.join("\n");
}

async function main() {
  const dryRun = flag("dry-run") || !flag("execute");
  const allow = flag("allow-emergency-unfreeze");
  if (!dryRun) {
    assertYouTubeMutationAllowed({
      allowEmergencyUnfreeze: allow,
      operation: "youtube:final-schedule-closure",
    });
  }

  const cal = JSON.parse(fs.readFileSync(CALENDAR, "utf8")) as {
    items: Array<{
      youtubeId: string;
      proposedUTC: string;
      proposedLocal: string;
      family: string;
      type: string;
      title: string;
      contentId: string;
      date: string;
      timeLocal: string;
      weekday?: string;
      validation?: string;
    }>;
    omitted?: any[];
    notReady?: any[];
  };
  const items = cal.items;
  if (items.length !== 13) throw new Error(`Expected 13 calendar items, got ${items.length}`);

  const scheduleIds = items.map((i) => i.youtubeId);
  const allIds = Array.from(new Set([...WATCH, ...scheduleIds]));
  const reg = JSON.parse(fs.readFileSync(REGISTRY, "utf8"));

  const { accessToken, scopes } = await token();
  if (!hasForceSslScope(scopes)) {
    console.error(JSON.stringify({ ok: false, failure: "OAUTH BLOCKS SCHEDULE APPLY" }));
    process.exit(2);
  }

  // ─── PHASE 1: BEFORE ─────────────────────────────────────────────
  const beforeMap = await getVideos(accessToken, allIds);
  const beforeRows = allIds.map((id) => snapRow(id, beforeMap.get(id), reg));
  const beforePayload = {
    fetchedAt: nowIso(),
    dryRun,
    mutation: "none_yet",
    rows: beforeRows,
    scheduleTargets: scheduleIds,
    publicCanonicals: APPROVED_PUBLIC.map((id) => snapRow(id, beforeMap.get(id), reg)),
  };
  fs.writeFileSync(
    path.join(AUDIT, "FINAL_SCHEDULE_APPLY_BEFORE.json"),
    JSON.stringify(beforePayload, null, 2) + "\n",
  );
  fs.writeFileSync(
    path.join(AUDIT, "FINAL_SCHEDULE_APPLY_BEFORE.md"),
    writeMdTable("Final Schedule Apply — BEFORE", beforeRows),
  );

  const mutationLog: any[] = [];

  // ─── PHASE 2: Repair HvAKGjx4lv0 ──────────────────────────────────
  const hvBefore = beforeMap.get("HvAKGjx4lv0");
  if (!hvBefore) throw new Error("HvAKGjx4lv0 not found");
  const hvKids = hvBefore.status?.madeForKids === true;
  const hvRepair = await setPrivateUnscheduled(accessToken, "HvAKGjx4lv0", hvKids, dryRun);
  mutationLog.push({
    phase: "repair_HvAKGjx4lv0",
    videoId: "HvAKGjx4lv0",
    before: {
      privacy: hvBefore.status?.privacyStatus,
      publishAt: hvBefore.status?.publishAt || null,
    },
    after: hvRepair.after,
    ok: hvRepair.ok,
    dryRun,
  });
  if (!hvRepair.ok) {
    const stop = {
      ok: false,
      stopped: true,
      reason: "HvAKGjx4lv0 repair FAILED — calendar NOT applied",
      mutationLog,
    };
    fs.writeFileSync(
      path.join(AUDIT, "FINAL_SCHEDULE_MUTATION_LOG.json"),
      JSON.stringify(stop, null, 2) + "\n",
    );
    console.error(JSON.stringify(stop, null, 2));
    process.exit(1);
  }

  // Re-fetch Hv to confirm
  if (!dryRun) {
    await sleep(400);
    const hvCheck = await getVideos(accessToken, ["HvAKGjx4lv0"]);
    const hv = hvCheck.get("HvAKGjx4lv0");
    if (hv?.status?.privacyStatus !== "private" || hv?.status?.publishAt) {
      console.error(
        JSON.stringify({
          ok: false,
          stopped: true,
          reason: "HvAKGjx4lv0 re-fetch failed private+null gate",
          actual: {
            privacy: hv?.status?.privacyStatus,
            publishAt: hv?.status?.publishAt || null,
          },
        }),
      );
      process.exit(1);
    }
  }

  // ─── PHASE 3: shelf gate before any schedule mutations ───────────
  {
    const shelfMap = await getVideos(accessToken, [...APPROVED_PUBLIC, "HvAKGjx4lv0"]);
    const publicOk = APPROVED_PUBLIC.every(
      (id) =>
        shelfMap.get(id)?.status?.privacyStatus === "public" &&
        !shelfMap.get(id)?.status?.publishAt,
    );
    const unexpectedPublic: string[] = [];
    // only checking the six — full npm shelf-verify runs after apply
    if (!publicOk) {
      console.error(
        JSON.stringify({
          ok: false,
          stopped: true,
          reason: "Shelf gate FAILED after Hv repair — calendar NOT applied",
          publicCanonicals: APPROVED_PUBLIC.map((id) => ({
            id,
            privacy: shelfMap.get(id)?.status?.privacyStatus,
            publishAt: shelfMap.get(id)?.status?.publishAt || null,
          })),
          unexpectedPublic,
        }),
      );
      process.exit(1);
    }
    mutationLog.push({
      phase: "shelf_gate_pre_schedule",
      ok: true,
      publicCanonicals: 6,
      unexpectedPublic: [],
    });
  }

  // ─── PHASE 4 precheck: validate calendar vs live ─────────────────
  for (const it of items) {
    assertNotPlaceholderHoldPublishAt(it.proposedUTC);
    const live = beforeMap.get(it.youtubeId);
    if (!live) throw new Error(`${it.youtubeId} missing from live API`);
    if (live.status?.privacyStatus === "public") {
      throw new Error(`${it.youtubeId} is public — refuse schedule`);
    }
    if (APPROVED_PUBLIC.includes(it.youtubeId as any)) {
      throw new Error(`${it.youtubeId} is public canonical — refuse`);
    }
    if (new Date(it.proposedUTC).getTime() <= Date.now()) {
      throw new Error(`${it.youtubeId} proposedUTC is not in the future`);
    }
  }
  const byMinute = new Map<string, string[]>();
  for (const it of items) {
    const k = norm(it.proposedUTC)!;
    byMinute.set(k, [...(byMinute.get(k) || []), it.youtubeId]);
  }
  for (const [k, ids] of byMinute) {
    if (ids.length > 1) throw new Error(`minute collision ${k}: ${ids.join(",")}`);
  }

  // ─── Clear held/extra that must be private+unscheduled ───────────
  // Do this BEFORE applying so unexpected schedules don't linger if we stop mid-batch.
  // But user said: if Hv fails stop. Held clears are part of apply safety.
  // Order: clear excluded first that currently have publishAt, then apply 13.
  for (const id of HELD_CLEAR) {
    const before = beforeMap.get(id);
    if (!before) {
      mutationLog.push({ phase: "clear_held", videoId: id, failed: true, error: "not found" });
      console.error(JSON.stringify({ ok: false, stopped: true, reason: `${id} not found` }));
      process.exit(1);
    }
    const needsClear =
      before.status?.privacyStatus !== "private" || Boolean(before.status?.publishAt);
    if (!needsClear) {
      mutationLog.push({
        phase: "clear_held",
        videoId: id,
        skipped: true,
        reason: "already private+unscheduled",
        before: {
          privacy: before.status?.privacyStatus,
          publishAt: before.status?.publishAt || null,
        },
      });
      continue;
    }
    const kids = before.status?.madeForKids === true;
    const cleared = await setPrivateUnscheduled(accessToken, id, kids, dryRun);
    mutationLog.push({
      phase: "clear_held",
      videoId: id,
      before: {
        privacy: before.status?.privacyStatus,
        publishAt: before.status?.publishAt || null,
      },
      after: cleared.after,
      ok: cleared.ok,
      clearedViaUnlistedHop: cleared.clearedViaUnlistedHop,
      dryRun,
    });
    if (!cleared.ok) {
      console.error(
        JSON.stringify({
          ok: false,
          stopped: true,
          reason: `Failed to clear ${id} to private+unscheduled`,
          mutationLog,
        }),
      );
      process.exit(1);
    }
  }

  // ─── PHASES 6–9: Apply 13 one-by-one ─────────────────────────────
  let appliedCount = 0;
  for (const it of items) {
    const liveBefore = (await getVideos(accessToken, [it.youtubeId])).get(it.youtubeId);
    if (!liveBefore) {
      mutationLog.push({
        phase: "schedule",
        youtubeId: it.youtubeId,
        failed: true,
        error: "not found at apply time",
      });
      console.error(
        JSON.stringify({
          ok: false,
          stopped: true,
          reason: `${it.youtubeId} missing`,
          appliedBeforeStop: appliedCount,
          mutationLog,
        }),
      );
      process.exit(1);
    }
    if (liveBefore.status?.privacyStatus === "public") {
      mutationLog.push({
        phase: "schedule",
        youtubeId: it.youtubeId,
        failed: true,
        error: "currently public",
      });
      console.error(
        JSON.stringify({
          ok: false,
          stopped: true,
          reason: `${it.youtubeId} public`,
          appliedBeforeStop: appliedCount,
          mutationLog,
        }),
      );
      process.exit(1);
    }

    const publishAt = norm(it.proposedUTC)!;
    assertNotPlaceholderHoldPublishAt(publishAt);
    const madeForKids = liveBefore.status?.madeForKids === true;
    const result = await updateStatus(
      accessToken,
      it.youtubeId,
      {
        privacyStatus: "private",
        publishAt,
        selfDeclaredMadeForKids: false,
        madeForKids,
      },
      dryRun,
    );

    let afterSnap: { privacy?: string; publishAt?: string | null } | null = null;
    if (dryRun) {
      afterSnap = { privacy: "private", publishAt };
    } else if (!result.ok) {
      mutationLog.push({
        phase: "schedule",
        ...it,
        publishAt,
        result,
        failed: true,
        error: `update failed status=${(result as any).statusCode}`,
        before: {
          privacy: liveBefore.status?.privacyStatus,
          publishAt: liveBefore.status?.publishAt || null,
        },
      });
      console.error(
        JSON.stringify({
          ok: false,
          stopped: true,
          reason: `schedule update failed for ${it.youtubeId}`,
          appliedBeforeStop: appliedCount,
          mutationLog,
        }),
      );
      process.exit(1);
    } else {
      const fromUpdate = (result as any).body?.status;
      afterSnap = {
        privacy: fromUpdate?.privacyStatus || "private",
        publishAt: fromUpdate?.publishAt || publishAt,
      };
      for (let attempt = 0; attempt < 4; attempt++) {
        await sleep(350 * (attempt + 1));
        const check = await getVideos(accessToken, [it.youtubeId]);
        const a = check.get(it.youtubeId);
        const got = a?.status?.publishAt || null;
        if (got) {
          afterSnap = { privacy: a?.status?.privacyStatus, publishAt: got };
          break;
        }
      }
      if (norm(afterSnap?.publishAt) !== publishAt) {
        mutationLog.push({
          phase: "schedule",
          ...it,
          publishAt,
          before: {
            privacy: liveBefore.status?.privacyStatus,
            publishAt: liveBefore.status?.publishAt || null,
          },
          after: afterSnap,
          result,
          failed: true,
          error: `publishAt mismatch got=${afterSnap?.publishAt}`,
        });
        console.error(
          JSON.stringify({
            ok: false,
            stopped: true,
            reason: `publishAt mismatch for ${it.youtubeId}`,
            appliedBeforeStop: appliedCount,
            mutationLog,
          }),
        );
        process.exit(1);
      }
    }

    mutationLog.push({
      phase: "schedule",
      youtubeId: it.youtubeId,
      contentId: it.contentId,
      family: it.family,
      type: it.type,
      title: it.title,
      date: it.date,
      timeLocal: it.timeLocal,
      publishAt,
      proposedLocal: it.proposedLocal,
      before: {
        privacy: liveBefore.status?.privacyStatus,
        publishAt: liveBefore.status?.publishAt || null,
      },
      after: afterSnap,
      failed: false,
      dryRun,
    });
    appliedCount += 1;
  }

  // ─── Re-fetch AFTER ──────────────────────────────────────────────
  const afterMap = dryRun ? beforeMap : await getVideos(accessToken, allIds);
  // For dry-run, project scheduled/cleared states into after rows
  const projected = new Map<string, { privacy: string; publishAt: string | null }>();
  if (dryRun) {
    projected.set("HvAKGjx4lv0", { privacy: "private", publishAt: null });
    for (const id of HELD_CLEAR) projected.set(id, { privacy: "private", publishAt: null });
    for (const it of items) {
      projected.set(it.youtubeId, { privacy: "private", publishAt: norm(it.proposedUTC) });
    }
  }

  const afterRows = allIds.map((id) => {
    const base = snapRow(id, afterMap.get(id), reg);
    if (dryRun && projected.has(id)) {
      const p = projected.get(id)!;
      return { ...base, privacyStatus: p.privacy, publishAt: p.publishAt, projected: true };
    }
    return base;
  });

  const afterPayload = {
    fetchedAt: nowIso(),
    dryRun,
    rows: afterRows,
    scheduled: afterRows.filter((r) => r.publishAt),
  };
  fs.writeFileSync(
    path.join(AUDIT, "FINAL_SCHEDULE_APPLY_AFTER.json"),
    JSON.stringify(afterPayload, null, 2) + "\n",
  );
  fs.writeFileSync(
    path.join(AUDIT, "FINAL_SCHEDULE_APPLY_AFTER.md"),
    writeMdTable("Final Schedule Apply — AFTER", afterRows),
  );

  // Verify 13 exact mappings
  const required: Record<string, string> = Object.fromEntries(
    items.map((i) => [i.youtubeId, norm(i.proposedUTC)!]),
  );
  const verifyRows = items.map((it) => {
    const row = afterRows.find((r) => r.videoId === it.youtubeId)!;
    const got = norm(row.publishAt);
    const want = required[it.youtubeId];
    return {
      youtubeId: it.youtubeId,
      want,
      got,
      privacy: row.privacyStatus,
      ok: got === want && row.privacyStatus === "private",
      date: it.date,
      timeLocal: it.timeLocal,
      family: it.family,
      type: it.type,
      title: it.title,
      proposedLocal: it.proposedLocal,
    };
  });

  const excludedIds = [...NOT_READY, ...HELD_CLEAR];
  const excludedVerify = excludedIds.map((id) => {
    const row = afterRows.find((r) => r.videoId === id)!;
    return {
      youtubeId: id,
      privacy: row.privacyStatus,
      publishAt: row.publishAt,
      ok: row.privacyStatus === "private" && !row.publishAt,
    };
  });

  const scheduledUnexpected = afterRows.filter(
    (r) => r.publishAt && !required[r.videoId] && allIds.includes(r.videoId),
  );

  const approvedCalendar = {
    generatedAt: nowIso(),
    appliedAt: dryRun ? null : nowIso(),
    approvedBy: "user",
    dryRun,
    applied: !dryRun,
    timezone: "Europe/Paris",
    items: verifyRows.map((v) => ({
      ...items.find((i) => i.youtubeId === v.youtubeId),
      status: dryRun ? "DRY_RUN" : v.ok ? "APPLIED_VERIFIED" : "FAILED",
      livePublishAt: v.got,
      livePrivacy: v.privacy,
      liveOk: v.ok,
    })),
    excluded: excludedVerify,
    scheduleHealth: {
      scheduled: verifyRows.filter((v) => v.ok).length,
      missing: verifyRows.filter((v) => !v.ok).length,
      unexpected: scheduledUnexpected.length,
      collisions: 0,
      placeholderDates: verifyRows.filter((v) => (v.got || "").startsWith("2026-12-31")).length,
    },
  };

  fs.writeFileSync(
    path.join(AUDIT, "FINAL_APPROVED_RELEASE_CALENDAR.json"),
    JSON.stringify(approvedCalendar, null, 2) + "\n",
  );
  fs.writeFileSync(
    path.join(AUDIT, "FINAL_APPROVED_RELEASE_CALENDAR.md"),
    [
      "# Final Approved Release Calendar",
      "",
      `Applied: \`${approvedCalendar.appliedAt || "DRY_RUN"}\``,
      `Dry-run: ${dryRun}`,
      "",
      "| Date | Paris | UTC | Family | Type | Title | YouTube ID | Live verify |",
      "|---|---|---|---|---|---|---|---|",
      ...verifyRows.map(
        (v) =>
          `| ${v.date} | ${v.timeLocal} | \`${v.want}\` | ${v.family} | ${v.type} | ${v.title} | \`${v.youtubeId}\` | ${v.ok ? "PASS" : "FAIL"} (${v.privacy}/${v.got || "null"}) |`,
      ),
      "",
      "## Excluded (must be private + unscheduled)",
      "",
      ...excludedVerify.map(
        (e) =>
          `- \`${e.youtubeId}\`: ${e.privacy} / \`${e.publishAt || "null"}\` → ${e.ok ? "PASS" : "FAIL"}`,
      ),
      "",
    ].join("\n"),
  );

  const logPayload = {
    ok:
      verifyRows.every((v) => v.ok) &&
      excludedVerify.every((e) => e.ok) &&
      scheduledUnexpected.length === 0,
    dryRun,
    applied: !dryRun,
    appliedCount,
    mutationLog,
    verifyRows,
    excludedVerify,
    scheduledUnexpected,
  };
  fs.writeFileSync(
    path.join(AUDIT, "FINAL_SCHEDULE_MUTATION_LOG.json"),
    JSON.stringify(logPayload, null, 2) + "\n",
  );
  fs.writeFileSync(
    path.join(AUDIT, "FINAL_SCHEDULE_MUTATION_LOG.md"),
    [
      "# Final Schedule Mutation Log",
      "",
      `ok: **${logPayload.ok}** · dryRun: ${dryRun} · appliedCount: ${appliedCount}`,
      "",
      "## Mutations",
      "",
      ...mutationLog.map(
        (m, i) =>
          `${i + 1}. phase=\`${m.phase}\` id=\`${m.videoId || m.youtubeId}\` ok=${m.ok !== false && !m.failed} ${m.skipped ? "(skipped)" : ""}`,
      ),
      "",
    ].join("\n"),
  );

  // ─── Update local SoT when live execute succeeds ─────────────────
  if (!dryRun && logPayload.ok) {
    const calOut = {
      ...cal,
      proposalOnly: false,
      applied: true,
      appliedAt: nowIso(),
      approvedBy: "user",
      mutation: "videos.update status only",
      items: approvedCalendar.items,
      omitted: cal.omitted,
      notReady: cal.notReady,
    };
    fs.writeFileSync(CALENDAR, JSON.stringify(calOut, null, 2) + "\n");

    reg.updatedAt = nowIso();
    reg.scheduleAppliedAt = nowIso();
    const byId = new Map(items.map((i) => [i.youtubeId, i]));
    for (const rec of reg.records || []) {
      const yid = rec.youtubeVideoId || rec.canonicalYouTubeVideoId;
      const hit = byId.get(yid);
      if (hit) {
        rec.scheduledAt = norm(hit.proposedUTC);
        rec.scheduledPublishTimestamp = rec.scheduledAt;
        rec.privacyStatus = "private";
        rec.currentYouTubeStatus = "private";
        rec.intendedYouTubeStatus = "scheduled";
        rec.youtubeState = "scheduled";
        rec.relatedLongFormVideoId =
          rec.relatedLongFormVideoId ||
          (hit.family === "EXOPLANETS"
            ? "b8-X_FyJnHM"
            : hit.family === "JWST"
              ? "tfTkMdE7qqw"
              : hit.family === "BLACK_HOLE"
                ? "3xrxdmaOwJI"
                : rec.relatedLongFormVideoId);
        rec.lastVerifiedAt = nowIso();
        rec.notes = `${rec.notes || ""} | revised calendar applied ${nowIso()}`.trim();
      }
      if (HELD_CLEAR.includes(yid as any) || NOT_READY.includes(yid as any)) {
        rec.scheduledAt = null;
        rec.scheduledPublishTimestamp = null;
        rec.privacyStatus = "private";
        rec.currentYouTubeStatus = "private";
        rec.intendedYouTubeStatus = "private";
        rec.youtubeState = "private";
        rec.lastVerifiedAt = nowIso();
      }
    }
    // Ensure held/not-ready registry notes for missing IDs
    const existing = new Set(
      (reg.records || []).map((r: any) => r.youtubeVideoId || r.canonicalYouTubeVideoId),
    );
    for (const it of items) {
      if (existing.has(it.youtubeId)) continue;
      reg.records.push({
        internalContentId: it.contentId,
        contentFamily: it.family,
        contentType: it.type,
        sourceFileFingerprint: `seed:${it.youtubeId}`,
        title: it.title,
        youtubeVideoId: it.youtubeId,
        youtubeState: "scheduled",
        scheduledPublishTimestamp: norm(it.proposedUTC),
        scheduledAt: norm(it.proposedUTC),
        publishedAt: null,
        privacyStatus: "private",
        currentYouTubeStatus: "private",
        intendedYouTubeStatus: "scheduled",
        historicalDuplicateIds: [],
        lastVerifiedAt: nowIso(),
        lastApiResponseStatus: "schedule_applied",
        notes: "Created during revised calendar apply",
      });
    }
    fs.writeFileSync(REGISTRY, JSON.stringify(reg, null, 2) + "\n");

    const recovery = JSON.parse(fs.readFileSync(RECOVERY, "utf8"));
    recovery.notes =
      "Revised recovery calendar applied. Observation 7–9 Aug. BH Shorts 10–12 Aug. Exo 13–16. JWST 20–23. Dec31 placeholders forbidden. Public shelf unchanged.";
    recovery.scheduleAppliedAt = nowIso();
    recovery.approvedScheduledIds = scheduleIds;
    recovery.heldForLaterIds = ["w1ej9u0rPTA"];
    recovery.extraPrivateUnscheduledIds = ["gPCpMsB0w2E", "YsyPMhNmHMk"];
    fs.writeFileSync(RECOVERY, JSON.stringify(recovery, null, 2) + "\n");
  }

  console.log(
    JSON.stringify(
      {
        ok: logPayload.ok,
        dryRun,
        applied: !dryRun,
        appliedCount,
        scheduleHealth: approvedCalendar.scheduleHealth,
        hvRepair: mutationLog.find((m) => m.phase === "repair_HvAKGjx4lv0"),
        excludedOk: excludedVerify.every((e) => e.ok),
      },
      null,
      2,
    ),
  );
  if (!logPayload.ok) process.exit(1);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
