#!/usr/bin/env tsx
/**
 * Apply the approved PROPOSED_CANONICAL_RELEASE_CALENDAR to existing YouTube IDs.
 *
 *   npm run youtube:apply-approved-schedule -- --dry-run
 *   npm run youtube:apply-approved-schedule -- --allow-emergency-unfreeze --execute
 *
 * Does NOT insert/delete/reupload. Only videos.update privacy=private + publishAt.
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
  assertNotPlaceholderHoldPublishAt,
  assertScheduleCadence,
  isPlaceholderHoldPublishAt,
} from "../src/lib/publishing/youtube-schedule-guards";

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

const APPROVED_PUBLIC = new Set([
  "Mo93x0fxB1Q",
  "1HuV8o3gOss",
  "KcKBixwmcV4",
  "3xrxdmaOwJI",
  "JRfhE6yWom4",
  "L2OFjL4neOo",
]);

function flag(name: string) {
  return process.argv.includes(`--${name}`);
}

function nowIso() {
  return new Date().toISOString();
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
      `https://www.googleapis.com/youtube/v3/videos?part=status,snippet&id=${chunk.join(",")}`,
      { headers: { Authorization: `Bearer ${accessToken}` } },
    );
    const body = await res.json();
    if (!res.ok) throw new Error(JSON.stringify(body));
    for (const it of body.items || []) map.set(it.id, it);
  }
  return map;
}

async function updateSchedule(
  accessToken: string,
  id: string,
  publishAtIso: string,
  madeForKids: boolean,
  dryRun: boolean,
) {
  assertNotPlaceholderHoldPublishAt(publishAtIso);
  const status = {
    privacyStatus: "private",
    publishAt: publishAtIso.replace(/\.\d{3}Z$/, "Z"),
    selfDeclaredMadeForKids: false,
    madeForKids,
  };
  if (dryRun) return { dryRun: true, ok: true, id, status };
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

async function main() {
  const dryRun = flag("dry-run") || !flag("execute");
  const allow = flag("allow-emergency-unfreeze");
  if (!dryRun) {
    assertYouTubeMutationAllowed({
      allowEmergencyUnfreeze: allow,
      operation: "youtube:apply-approved-schedule",
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
      status: string;
    }>;
    conflicts?: string[];
  };

  if ((cal.conflicts || []).length) {
    throw new Error(`Calendar has unresolved conflicts: ${cal.conflicts!.join("; ")}`);
  }

  const items = cal.items;
  // Preflight cadence
  const shortsByDay = new Map<string, number>();
  const byMinute = new Map<string, string[]>();
  for (const it of items) {
    if (APPROVED_PUBLIC.has(it.youtubeId)) {
      throw new Error(`Refusing to reschedule public canonical ${it.youtubeId}`);
    }
    assertNotPlaceholderHoldPublishAt(it.proposedUTC);
    const cadence = assertScheduleCadence({
      format: it.type === "longform" ? "longform" : "shorts",
      publishAtIso: it.proposedUTC,
      shortsOnSameDay: shortsByDay.get(it.date) || 0,
      maxShortsPerDay: 1,
      maxLongsPerWeek: 1,
      isHistoricalDuplicate: false,
      sameMinuteCollision: (byMinute.get(it.proposedUTC) || []).length > 0,
    });
    if (!cadence.ok) {
      // Thu launch day: long + short #1 same day is intentional (1 short that day)
      const onlyShortDayIssue =
        cadence.errors.length === 1 && /Short\/day/i.test(cadence.errors[0] || "");
      if (!(it.type === "shorts" && onlyShortDayIssue && (shortsByDay.get(it.date) || 0) === 0)) {
        // If shortsOnSameDay is 0, Short/day shouldn't fire — unless we're incrementing wrong.
      }
      if (cadence.errors.some((e) => /placeholder|historical|minute|valid|future/i.test(e))) {
        throw new Error(`${it.youtubeId}: ${cadence.errors.join("; ")}`);
      }
      if (/Short\/day/i.test(cadence.errors.join(" ")) && (shortsByDay.get(it.date) || 0) >= 1) {
        throw new Error(`${it.youtubeId}: ${cadence.errors.join("; ")}`);
      }
    }
    if (it.type === "shorts") {
      shortsByDay.set(it.date, (shortsByDay.get(it.date) || 0) + 1);
    }
    byMinute.set(it.proposedUTC, [...(byMinute.get(it.proposedUTC) || []), it.youtubeId]);
  }
  for (const [k, ids] of byMinute) {
    if (ids.length > 1) throw new Error(`same-minute collision ${k}: ${ids.join(",")}`);
  }
  for (const [d, n] of shortsByDay) {
    if (n > 1) throw new Error(`more than 1 Short on ${d}`);
  }

  const { accessToken, scopes } = await token();
  if (!hasForceSslScope(scopes)) {
    console.error(JSON.stringify({ ok: false, failure: "OAUTH BLOCKS SCHEDULE APPLY" }));
    process.exit(2);
  }

  const ids = items.map((i) => i.youtubeId);
  const beforeMap = await getVideos(accessToken, [...ids, ...APPROVED_PUBLIC]);
  const mutations: any[] = [];

  for (const it of items) {
    const before = beforeMap.get(it.youtubeId);
    if (!before) {
      mutations.push({ youtubeId: it.youtubeId, failed: true, error: "video not found" });
      continue;
    }
    if (before.status?.privacyStatus === "public") {
      mutations.push({
        youtubeId: it.youtubeId,
        failed: true,
        error: "refusing to schedule currently-public video",
      });
      continue;
    }
    const madeForKids = before.status?.madeForKids === true;
    const publishAt = it.proposedUTC.replace(/\.\d{3}Z$/, "Z");
    const result = await updateSchedule(
      accessToken,
      it.youtubeId,
      publishAt,
      madeForKids,
      dryRun,
    );
    // Prefer update response body (videos.list can briefly omit publishAt).
    let afterSnap: { privacy?: string; publishAt?: string | null } | null = null;
    if (dryRun) {
      afterSnap = { privacy: "private", publishAt, projected: true } as any;
    } else if (result.ok) {
      const fromUpdate = (result as any).body?.status;
      afterSnap = {
        privacy: fromUpdate?.privacyStatus || "private",
        publishAt: fromUpdate?.publishAt || publishAt,
      };
      // Confirm with a short retry list
      for (let attempt = 0; attempt < 3; attempt++) {
        await new Promise((r) => setTimeout(r, 400 * (attempt + 1)));
        const check = await getVideos(accessToken, [it.youtubeId]);
        const a = check.get(it.youtubeId);
        const got = a?.status?.publishAt || null;
        if (got) {
          afterSnap = {
            privacy: a?.status?.privacyStatus,
            publishAt: got,
          };
          break;
        }
      }
      const norm = (s: string | null | undefined) => (s || "").replace(/\.\d{3}Z$/, "Z");
      if (norm(afterSnap?.publishAt) !== norm(publishAt)) {
        mutations.push({
          ...it,
          publishAt,
          before: {
            privacy: before.status?.privacyStatus,
            publishAt: before.status?.publishAt || null,
          },
          after: afterSnap,
          result,
          failed: true,
          error: `publishAt mismatch got=${afterSnap?.publishAt}`,
        });
        continue;
      }
    } else {
      mutations.push({
        youtubeId: it.youtubeId,
        publishAt,
        result,
        failed: true,
        error: `update failed status=${(result as any).statusCode}`,
      });
      continue;
    }
    mutations.push({
      youtubeId: it.youtubeId,
      contentId: it.contentId,
      family: it.family,
      type: it.type,
      title: it.title,
      publishAt,
      proposedLocal: it.proposedLocal,
      before: {
        privacy: before.status?.privacyStatus,
        publishAt: before.status?.publishAt || null,
      },
      after: afterSnap,
      result,
      dryRun,
      failed: false,
    });
  }

  const afterMap = dryRun
    ? beforeMap
    : await getVideos(accessToken, [...ids, ...APPROVED_PUBLIC]);

  const appliedCalendar = {
    generatedAt: cal && (cal as any).generatedAt,
    appliedAt: nowIso(),
    approvedBy: "user",
    dryRun,
    items: items.map((it) => ({
      ...it,
      status: dryRun ? "DRY_RUN" : "APPLIED",
      livePublishAt: afterMap.get(it.youtubeId)?.status?.publishAt || null,
      livePrivacy: afterMap.get(it.youtubeId)?.status?.privacyStatus || null,
    })),
  };

  if (!dryRun) {
    fs.writeFileSync(CALENDAR, JSON.stringify({ ...cal, ...appliedCalendar, applied: true }, null, 2));
    // md update
    const md = [
      "# APPROVED CANONICAL RELEASE CALENDAR (APPLIED)",
      "",
      `Applied: \`${nowIso()}\``,
      "",
      "Timezone: Europe/Paris",
      "",
      "| Date | Time | Family | Type | Title | YouTube ID | publishAt UTC | Live |",
      "|---|---|---|---|---|---|---|---|",
      ...appliedCalendar.items.map((it) => {
        const live = `${it.livePrivacy}/${it.livePublishAt || "—"}`;
        return `| ${it.date} | ${it.timeLocal} | ${it.family} | ${it.type} | ${it.title} | \`${it.youtubeId}\` | ${it.proposedUTC} | ${live} |`;
      }),
      "",
      "Public canonicals were not modified.",
      "",
    ].join("\n");
    fs.writeFileSync(path.join(AUDIT, "PROPOSED_CANONICAL_RELEASE_CALENDAR.md"), md);
    fs.writeFileSync(
      path.join(AUDIT, "APPLIED_CANONICAL_RELEASE_CALENDAR.json"),
      JSON.stringify(appliedCalendar, null, 2),
    );

    const reg = JSON.parse(fs.readFileSync(REGISTRY, "utf8"));
    reg.updatedAt = nowIso();
    reg.scheduleAppliedAt = nowIso();
    const byId = new Map(items.map((i) => [i.youtubeId, i]));
    for (const rec of reg.records || []) {
      const yid = rec.youtubeVideoId || rec.canonicalYouTubeVideoId;
      const hit = byId.get(yid);
      if (hit) {
        rec.scheduledAt = hit.proposedUTC.replace(/\.\d{3}Z$/, "Z");
        rec.scheduledPublishTimestamp = rec.scheduledAt;
        rec.privacyStatus = "private";
        rec.currentYouTubeStatus = "private";
        rec.intendedYouTubeStatus = "scheduled";
        rec.youtubeState = "scheduled";
        rec.lastVerifiedAt = nowIso();
        rec.notes = `${rec.notes || ""} | approved calendar applied ${nowIso()}`.trim();
      }
    }
    // Ensure records exist for scheduled IDs missing from registry
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
        scheduledPublishTimestamp: it.proposedUTC.replace(/\.\d{3}Z$/, "Z"),
        scheduledAt: it.proposedUTC.replace(/\.\d{3}Z$/, "Z"),
        publishedAt: null,
        privacyStatus: "private",
        currentYouTubeStatus: "private",
        intendedYouTubeStatus: "scheduled",
        historicalDuplicateIds: [],
        lastVerifiedAt: nowIso(),
        lastApiResponseStatus: "schedule_applied",
        notes: "Created during approved calendar apply",
      });
    }
    fs.writeFileSync(REGISTRY, JSON.stringify(reg, null, 2) + "\n");

    const recovery = JSON.parse(fs.readFileSync(RECOVERY, "utf8"));
    recovery.notes =
      "Approved calendar applied 2026-08-07. Dec31 placeholders remain forbidden. Public shelf unchanged.";
    recovery.scheduleAppliedAt = nowIso();
    recovery.approvedScheduledIds = items.map((i) => i.youtubeId);
    fs.writeFileSync(RECOVERY, JSON.stringify(recovery, null, 2) + "\n");
  }

  const publicCheck = [...APPROVED_PUBLIC].map((id) => {
    const it = afterMap.get(id);
    return {
      id,
      privacy: it?.status?.privacyStatus,
      publishAt: it?.status?.publishAt || null,
      ok: it?.status?.privacyStatus === "public" && !it?.status?.publishAt,
    };
  });

  const failed = mutations.filter((m) => m.failed);
  const out = {
    ok: failed.length === 0 && publicCheck.every((p) => p.ok !== false),
    dryRun,
    applied: !dryRun,
    count: items.length,
    failed: failed.length,
    mutations,
    publicCheck,
  };
  fs.writeFileSync(
    path.join(AUDIT, "SCHEDULE_APPLY_RESULT.json"),
    JSON.stringify(out, null, 2),
  );
  console.log(
    JSON.stringify(
      {
        ok: out.ok,
        dryRun,
        applied: !dryRun,
        count: items.length,
        failed: failed.length,
        publicOk: publicCheck.every((p) => p.ok),
      },
      null,
      2,
    ),
  );
  if (!out.ok) process.exit(1);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
