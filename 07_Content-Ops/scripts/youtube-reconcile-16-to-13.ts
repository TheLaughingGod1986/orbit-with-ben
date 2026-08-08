#!/usr/bin/env tsx
/**
 * Quota-safe 16→13 schedule reconciliation.
 *
 *   npm run youtube:reconcile-16-to-13 -- --dry-run
 *   npm run youtube:reconcile-16-to-13 -- --allow-emergency-unfreeze --execute
 *
 * Phase 1 stops with exit 20 if quotaExceeded (zero mutations).
 * Does NOT layer 13 on top of 16 — unschedules obsolete first, then updates 13.
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

const APPROVED_PUBLIC = new Set([
  "Mo93x0fxB1Q",
  "1HuV8o3gOss",
  "KcKBixwmcV4",
  "3xrxdmaOwJI",
  "JRfhE6yWom4",
  "L2OFjL4neOo",
]);

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
] as const;

const APPROVED_UTC: Record<string, string> = {
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
function isQuota(body: unknown) {
  return /quotaExceeded/i.test(JSON.stringify(body || {}));
}

async function token() {
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
      `https://www.googleapis.com/youtube/v3/videos?part=status,snippet&id=${chunk.join(",")}`,
      { headers: { Authorization: `Bearer ${accessToken}` } },
    );
    const body = await res.json();
    if (isQuota(body)) throw Object.assign(new Error("quotaExceeded"), { quota: true, body });
    if (!res.ok) throw new Error(JSON.stringify(body));
    for (const it of body.items || []) map.set(it.id, it);
  }
  return map;
}

// NOTE: intentionally no search.list forMine — burns daily quota across the full catalogue.

async function updateStatus(
  accessToken: string,
  id: string,
  status: Record<string, unknown>,
  dryRun: boolean,
) {
  if (dryRun) return { ok: true, dryRun: true, id, status, body: { status } };
  const res = await fetch("https://www.googleapis.com/youtube/v3/videos?part=status", {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id, status }),
  });
  const body = await res.json();
  if (isQuota(body)) throw Object.assign(new Error("quotaExceeded"), { quota: true, body });
  return { ok: res.ok, statusCode: res.status, id, body, status };
}

async function setPrivateUnscheduled(
  accessToken: string,
  id: string,
  madeForKids: boolean,
  dryRun: boolean,
  prior?: any,
) {
  const payload = {
    privacyStatus: "private",
    license: prior?.license || "youtube",
    embeddable: prior?.embeddable === true,
    publicStatsViewable: prior?.publicStatsViewable === true,
    selfDeclaredMadeForKids: false,
    madeForKids,
  };
  let result = await updateStatus(accessToken, id, payload, dryRun);
  if (dryRun) return { ok: true, after: { privacy: "private", publishAt: null } };
  if (!result.ok) return { ok: false, after: null, result };
  await sleep(800);
  let it = (await getVideos(accessToken, [id])).get(id);
  if (it?.status?.publishAt) {
    await updateStatus(accessToken, id, { ...payload, privacyStatus: "unlisted" }, false);
    result = await updateStatus(accessToken, id, payload, false);
    await sleep(800);
    it = (await getVideos(accessToken, [id])).get(id);
  }
  return {
    ok: it?.status?.privacyStatus === "private" && !it?.status?.publishAt,
    after: {
      privacy: it?.status?.privacyStatus || null,
      publishAt: it?.status?.publishAt || null,
    },
    result,
  };
}

/** Serialized Hv gate: 3 consecutive private+null reads. */
async function hvStabilityGate(accessToken: string, dryRun: boolean) {
  const log: any = { startedAt: nowIso(), reads: [], dryRun };
  const fetchOnce = async () => {
    const it = (await getVideos(accessToken, ["HvAKGjx4lv0"])).get("HvAKGjx4lv0");
    const row = {
      at: nowIso(),
      privacy: it?.status?.privacyStatus || null,
      publishAt: it?.status?.publishAt || null,
    };
    log.reads.push(row);
    return { it, row };
  };

  let { it, row } = await fetchOnce();
  log.initial = row;
  if (row.privacy !== "private" || row.publishAt) {
    if (!dryRun) {
      const madeForKids = it?.status?.madeForKids === true;
      const upd = await updateStatus(
        accessToken,
        "HvAKGjx4lv0",
        {
          privacyStatus: "private",
          license: it?.status?.license || "youtube",
          embeddable: it?.status?.embeddable === true,
          publicStatsViewable: it?.status?.publicStatsViewable === true,
          selfDeclaredMadeForKids: false,
          madeForKids,
        },
        false,
      );
      log.write = {
        ok: upd.ok,
        responsePrivacy: (upd as any).body?.status?.privacyStatus || null,
      };
      if (!upd.ok) {
        log.pass = false;
        log.reason = "HV write failed";
        return log;
      }
    } else {
      log.write = { ok: true, dryRun: true, responsePrivacy: "private" };
    }
  } else {
    log.write = { skipped: true, reason: "already private+null on first read" };
  }

  const confirm = async () => {
    const consecutive: any[] = [];
    for (let i = 0; i < 3; i++) {
      await sleep(900);
      const r = await fetchOnce();
      consecutive.push(r.row);
      if (r.row.privacy !== "private" || r.row.publishAt) return { ok: false, consecutive };
    }
    return { ok: true, consecutive };
  };

  let cycle = await confirm();
  if (!cycle.ok) {
    log.firstCycleFail = cycle.consecutive;
    // one additional stabilization cycle only (max 6 reads after mutation)
    cycle = await confirm();
    log.secondCycle = cycle.consecutive;
  }
  log.pass = cycle.ok;
  log.final = cycle.consecutive[cycle.consecutive.length - 1] || null;
  if (!cycle.ok) log.reason = "HV_STABILITY_FAIL";
  return log;
}

async function main() {
  const dryRun = flag("dry-run") || !flag("execute");
  const allow = flag("allow-emergency-unfreeze");

  const { accessToken, scopes } = await token();

  // ─── Phase 1: quota probe (single cheap read) ────────────────────
  {
    const res = await fetch(
      "https://www.googleapis.com/youtube/v3/videos?part=status&id=Mo93x0fxB1Q",
      { headers: { Authorization: `Bearer ${accessToken}` } },
    );
    const body = await res.json();
    const gate = {
      probedAt: nowIso(),
      quotaAvailable: !(res.status === 403 && isQuota(body)),
      probeStatus: res.status,
      quotaError: isQuota(body) ? body.error : null,
      mutations: 0,
    };
    fs.writeFileSync(
      path.join(AUDIT, "FINAL_RECONCILIATION_QUOTA_GATE.json"),
      JSON.stringify(gate, null, 2) + "\n",
    );
    if (!gate.quotaAvailable) {
      console.log(
        JSON.stringify({
          verdict: "WAITING FOR YOUTUBE API QUOTA",
          ...gate,
        }),
      );
      process.exit(20);
    }
  }

  if (!hasForceSslScope(scopes)) {
    console.error(JSON.stringify({ ok: false, failure: "OAUTH BLOCKS RECONCILE" }));
    process.exit(2);
  }
  if (!dryRun) {
    assertYouTubeMutationAllowed({
      allowEmergencyUnfreeze: allow,
      operation: "youtube:reconcile-16-to-13",
    });
  }

  const cal = JSON.parse(fs.readFileSync(CALENDAR, "utf8"));
  const calIds = (cal.items || []).map((i: any) => i.youtubeId as string);
  if (calIds.length !== 13) throw new Error(`calendar items=${calIds.length}`);
  for (const id of Object.keys(APPROVED_UTC)) {
    if (!calIds.includes(id)) throw new Error(`calendar missing ${id}`);
  }

  const reg = JSON.parse(fs.readFileSync(REGISTRY, "utf8"));
  const regById = new Map(
    (reg.records || []).map((r: any) => [r.youtubeVideoId || r.canonicalYouTubeVideoId, r]),
  );

  // ─── Phase 2: live scheduled inventory (quota-safe known IDs only) ─
  // Do NOT use search.list forMine — it burns quota across the whole catalogue.
  // Watchlist = approved 13 + excluded 9 + public 6 + known old-16 IDs from applied calendar.
  const knownOldIds: string[] = [];
  try {
    const appliedPath = path.join(AUDIT, "APPLIED_CANONICAL_RELEASE_CALENDAR.json");
    if (fs.existsSync(appliedPath)) {
      const applied = JSON.parse(fs.readFileSync(appliedPath, "utf8"));
      for (const it of applied.items || []) {
        if (it.youtubeId) knownOldIds.push(it.youtubeId);
      }
    }
  } catch {
    /* ignore */
  }
  const watchIds = Array.from(
    new Set([
      ...Object.keys(APPROVED_UTC),
      ...EXCLUDED,
      ...APPROVED_PUBLIC,
      ...knownOldIds,
    ]),
  ) as string[];
  const beforeMap = await getVideos(accessToken, watchIds);

  const liveScheduled = [...beforeMap.values()].filter((it) => it.status?.publishAt);
  const beforeRows = liveScheduled.map((it) => {
    const rec = regById.get(it.id);
    return {
      videoId: it.id,
      title: it.snippet?.title,
      privacyStatus: it.status?.privacyStatus,
      publishAt: it.status?.publishAt,
      contentId: rec?.internalContentId || null,
      contentFamily: rec?.contentFamily || null,
      sourceFingerprint: rec?.sourceFileFingerprint || null,
      canonicalStatus: APPROVED_PUBLIC.has(it.id)
        ? "public_canonical"
        : APPROVED_UTC[it.id]
          ? "approved_schedule_target"
          : EXCLUDED.includes(it.id as any)
            ? "excluded"
            : "unexpected_or_obsolete",
      registryState: rec?.youtubeState || null,
    };
  });

  fs.writeFileSync(
    path.join(AUDIT, "FINAL_RECONCILIATION_LIVE_BEFORE.json"),
    JSON.stringify({ fetchedAt: nowIso(), count: beforeRows.length, rows: beforeRows }, null, 2) +
      "\n",
  );

  // ─── Phase 4–5: reconciliation ───────────────────────────────────
  const liveById = new Map(beforeRows.map((r) => [r.videoId, r.publishAt as string]));
  const approvedSet = new Set(Object.keys(APPROVED_UTC));
  const liveSet = new Set(liveById.keys());
  const obsolete = [...liveSet].filter((id) => !approvedSet.has(id));
  const reconItems = [...new Set([...liveSet, ...approvedSet])].map((id) => {
    const live = liveById.get(id) || null;
    const approved = APPROVED_UTC[id] || null;
    let action = "BLOCKED_REVIEW";
    if (approved && live && norm(live) === norm(approved)) action = "KEEP_AS_IS";
    else if (approved && live && norm(live) !== norm(approved)) action = "UPDATE_TIME";
    else if (approved && !live) action = "MISSING_FROM_LIVE";
    else if (!approved && live) action = "UNSCHEDULE";
    return {
      youtubeId: id,
      livePublishAt: live,
      approvedPublishAt: approved,
      action,
      title: beforeMap.get(id)?.snippet?.title || null,
    };
  });

  // Validate obsolete trio
  for (const id of obsolete) {
    if (APPROVED_PUBLIC.has(id)) throw new Error(`obsolete id is public canonical: ${id}`);
    if (approvedSet.has(id)) throw new Error(`obsolete id in approved 13: ${id}`);
  }
  // Obsolete count is dynamic (LIVE - APPROVED). Do not hard-require 3.
  if (obsolete.length === 0) {
    console.log(JSON.stringify({ note: "No obsolete scheduled IDs — live already subset of approved" }));
  }
  for (const id of obsolete) {
    if (!id || APPROVED_PUBLIC.has(id) || approvedSet.has(id)) {
      const payload = {
        ok: false,
        reason: "OBSOLETE_ID_REVIEW_REQUIRED",
        obsolete,
        badId: id,
      };
      fs.writeFileSync(
        path.join(AUDIT, "FINAL_16_TO_13_RECONCILIATION.json"),
        JSON.stringify(payload, null, 2) + "\n",
      );
      console.error(JSON.stringify(payload));
      process.exit(1);
    }
  }

  const recon = {
    generatedAt: nowIso(),
    liveScheduledCount: liveSet.size,
    approvedCount: 13,
    obsoleteIds: obsolete,
    obsoleteClassification: "REMOVED_FROM_APPROVED_SCHEDULE",
    items: reconItems,
  };
  fs.writeFileSync(
    path.join(AUDIT, "FINAL_16_TO_13_RECONCILIATION.json"),
    JSON.stringify(recon, null, 2) + "\n",
  );
  fs.writeFileSync(
    path.join(AUDIT, "FINAL_16_TO_13_RECONCILIATION.md"),
    [
      "# Final 16→13 Reconciliation",
      "",
      `Generated: \`${nowIso()}\``,
      "",
      `Live scheduled: **${liveSet.size}** · Approved: **13** · Obsolete: **${obsolete.length}**`,
      "",
      "Obsolete IDs:",
      ...obsolete.map((id) => `- \`${id}\` — REMOVED_FROM_APPROVED_SCHEDULE`),
      "",
      "| YouTube ID | Live publishAt | Approved publishAt | Action |",
      "|---|---|---|---|",
      ...reconItems.map(
        (i) =>
          `| \`${i.youtubeId}\` | \`${i.livePublishAt}\` | \`${i.approvedPublishAt}\` | ${i.action} |`,
      ),
      "",
    ].join("\n"),
  );

  // ─── Phase 6: Hv stability ───────────────────────────────────────
  const hvLog = await hvStabilityGate(accessToken, dryRun);
  fs.writeFileSync(path.join(AUDIT, "HV_STABILITY_LOG.json"), JSON.stringify(hvLog, null, 2) + "\n");
  fs.writeFileSync(
    path.join(AUDIT, "HV_STABILITY_LOG.md"),
    [
      "# HvAKGjx4lv0 Stability Log",
      "",
      `pass: **${hvLog.pass}**`,
      "",
      "```json",
      JSON.stringify(hvLog, null, 2),
      "```",
      "",
    ].join("\n"),
  );
  if (!hvLog.pass) {
    console.error(JSON.stringify({ verdict: "RECONCILIATION FAILED", reason: "HV_STABILITY_FAIL", hvLog }));
    process.exit(1);
  }

  // ─── Phase 8A: unschedule obsolete ───────────────────────────────
  const mutationLog: any[] = [];
  for (const id of obsolete) {
    const before = beforeMap.get(id) || (await getVideos(accessToken, [id])).get(id);
    if (!before) throw new Error(`obsolete ${id} not found`);
    const cleared = await setPrivateUnscheduled(
      accessToken,
      id,
      before.status?.madeForKids === true,
      dryRun,
      before.status,
    );
    mutationLog.push({ phase: "unschedule_obsolete", videoId: id, ...cleared, dryRun });
    if (!cleared.ok) {
      console.error(
        JSON.stringify({
          verdict: "RECONCILIATION FAILED",
          reason: `failed to unschedule ${id}`,
          mutationLog,
        }),
      );
      process.exit(1);
    }
  }

  // ─── Phase 8B: apply 13 one-by-one ────────────────────────────────
  for (const [id, publishAt] of Object.entries(APPROVED_UTC)) {
    assertNotPlaceholderHoldPublishAt(publishAt);
    if (APPROVED_PUBLIC.has(id)) throw new Error(`refusing public canonical ${id}`);
    const live = (await getVideos(accessToken, [id])).get(id);
    if (!live) {
      mutationLog.push({ phase: "schedule", videoId: id, failed: true, error: "missing" });
      console.error(JSON.stringify({ verdict: "RECONCILIATION FAILED", stopped: id, mutationLog }));
      process.exit(1);
    }
    if (live.status?.privacyStatus === "public") {
      console.error(JSON.stringify({ verdict: "RECONCILIATION FAILED", reason: `${id} public` }));
      process.exit(1);
    }
    if (norm(live.status?.publishAt) === publishAt && live.status?.privacyStatus === "private") {
      mutationLog.push({ phase: "schedule", videoId: id, skipped: true, reason: "KEEP_AS_IS" });
      continue;
    }
    const madeForKids = live.status?.madeForKids === true;
    let result: any;
    try {
      result = await updateStatus(
        accessToken,
        id,
        {
          privacyStatus: "private",
          publishAt,
          selfDeclaredMadeForKids: false,
          madeForKids,
        },
        dryRun,
      );
    } catch (e: any) {
      if (e?.quota) {
        console.error(
          JSON.stringify({
            verdict: "WAITING FOR YOUTUBE API QUOTA",
            stoppedAt: id,
            succeededBefore: mutationLog.filter((m) => !m.failed),
          }),
        );
        process.exit(20);
      }
      throw e;
    }
    if (!dryRun && !result.ok) {
      mutationLog.push({ phase: "schedule", videoId: id, failed: true, result });
      console.error(JSON.stringify({ verdict: "RECONCILIATION FAILED", stoppedAt: id, mutationLog }));
      process.exit(1);
    }
    let got: string | null = dryRun ? publishAt : null;
    if (!dryRun) {
      for (let a = 0; a < 4; a++) {
        await sleep(400 * (a + 1));
        const check = (await getVideos(accessToken, [id])).get(id);
        got = check?.status?.publishAt || null;
        if (norm(got) === publishAt) break;
      }
      if (norm(got) !== publishAt) {
        mutationLog.push({
          phase: "schedule",
          videoId: id,
          failed: true,
          error: `publishAt mismatch got=${got}`,
        });
        console.error(JSON.stringify({ verdict: "RECONCILIATION FAILED", stoppedAt: id, mutationLog }));
        process.exit(1);
      }
    }
    mutationLog.push({
      phase: "schedule",
      videoId: id,
      publishAt,
      got,
      failed: false,
      dryRun,
    });
  }

  // ─── Phase 11: after verify ──────────────────────────────────────
  const afterWatch = Array.from(
    new Set([...Object.keys(APPROVED_UTC), ...EXCLUDED, ...obsolete, ...APPROVED_PUBLIC]),
  );
  const afterMap = dryRun ? beforeMap : await getVideos(accessToken, afterWatch);
  let afterScheduled = [...afterMap.values()]
    .filter((it) => it.status?.publishAt)
    .map((it) => ({
      videoId: it.id,
      publishAt: it.status.publishAt,
      privacy: it.status.privacyStatus,
      title: it.snippet?.title,
    }));
  // Dry-run: project obsolete clears + approved publishAts (zero live mutations).
  if (dryRun) {
    const obsoleteSet = new Set(obsolete);
    afterScheduled = Object.entries(APPROVED_UTC).map(([id, publishAt]) => ({
      videoId: id,
      publishAt,
      privacy: "private",
      title: beforeMap.get(id)?.snippet?.title,
      projected: true,
    }));
    void obsoleteSet;
  }

  fs.writeFileSync(
    path.join(AUDIT, "FINAL_RECONCILIATION_LIVE_AFTER.json"),
    JSON.stringify({ fetchedAt: nowIso(), dryRun, count: afterScheduled.length, rows: afterScheduled }, null, 2) +
      "\n",
  );

  const verify13 = Object.entries(APPROVED_UTC).map(([id, want]) => {
    const it = afterMap.get(id);
    const got = dryRun
      ? want
      : norm(it?.status?.publishAt);
    return {
      youtubeId: id,
      want,
      got,
      ok: got === want && (dryRun || it?.status?.privacyStatus === "private"),
    };
  });
  const excludedOk = EXCLUDED.map((id) => {
    if (dryRun && obsolete.includes(id)) {
      return { youtubeId: id, privacy: "private", publishAt: null, ok: true };
    }
    const it = afterMap.get(id);
    return {
      youtubeId: id,
      privacy: it?.status?.privacyStatus || null,
      publishAt: it?.status?.publishAt || null,
      ok: it?.status?.privacyStatus === "private" && !it?.status?.publishAt,
    };
  });

  const unexpected = afterScheduled.filter((r) => !APPROVED_UTC[r.videoId]);
  const health = {
    scheduled: verify13.filter((v) => v.ok).length,
    missing: verify13.filter((v) => !v.ok).length,
    unexpected: unexpected.length,
    collisions: 0,
    placeholderDates: afterScheduled.filter((r) =>
      String(r.publishAt || "").startsWith("2026-12-31"),
    ).length,
  };

  const ok =
    health.scheduled === 13 &&
    health.missing === 0 &&
    health.unexpected === 0 &&
    excludedOk.every((e) => e.ok) &&
    hvLog.pass;

  fs.writeFileSync(
    path.join(AUDIT, "FINAL_RECONCILIATION_MUTATION_LOG.json"),
    JSON.stringify(
      {
        ok,
        dryRun,
        verdict: ok
          ? dryRun
            ? "DRY_RUN_OK"
            : "SCHEDULE RECONCILED, CLEAN AND CANONICAL"
          : "RECONCILIATION FAILED",
        obsolete,
        mutationLog,
        verify13,
        excludedOk,
        health,
      },
      null,
      2,
    ) + "\n",
  );

  if (!dryRun && ok) {
    // Update registry + calendar applied flags
    for (const rec of reg.records || []) {
      const yid = rec.youtubeVideoId || rec.canonicalYouTubeVideoId;
      if (APPROVED_UTC[yid]) {
        rec.scheduledAt = APPROVED_UTC[yid];
        rec.scheduledPublishTimestamp = APPROVED_UTC[yid];
        rec.privacyStatus = "private";
        rec.youtubeState = "scheduled";
        rec.intendedYouTubeStatus = "scheduled";
        rec.lastVerifiedAt = nowIso();
      }
      if (obsolete.includes(yid) || EXCLUDED.includes(yid as any)) {
        rec.scheduledAt = null;
        rec.scheduledPublishTimestamp = null;
        rec.privacyStatus = "private";
        rec.youtubeState = "private";
        rec.intendedYouTubeStatus = "private";
        rec.lastVerifiedAt = nowIso();
      }
    }
    reg.updatedAt = nowIso();
    reg.scheduleReconciledAt = nowIso();
    fs.writeFileSync(REGISTRY, JSON.stringify(reg, null, 2) + "\n");
    const calOut = {
      ...cal,
      applied: true,
      proposalOnly: false,
      appliedAt: nowIso(),
      reconciledFrom: "16-to-13",
    };
    fs.writeFileSync(CALENDAR, JSON.stringify(calOut, null, 2) + "\n");
  }

  console.log(
    JSON.stringify(
      {
        ok,
        dryRun,
        verdict: ok
          ? dryRun
            ? "DRY_RUN_OK"
            : "SCHEDULE RECONCILED, CLEAN AND CANONICAL"
          : "RECONCILIATION FAILED",
        liveBefore: liveSet.size,
        obsolete,
        health,
        hvPass: hvLog.pass,
      },
      null,
      2,
    ),
  );
  if (!ok) process.exit(1);
}

main().catch((e) => {
  if ((e as any)?.quota) {
    console.log(JSON.stringify({ verdict: "WAITING FOR YOUTUBE API QUOTA", error: String(e) }));
    process.exit(20);
  }
  console.error(e);
  process.exit(1);
});
