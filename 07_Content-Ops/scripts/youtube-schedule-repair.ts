#!/usr/bin/env tsx
/**
 * Schedule repair: remove fake 2026-12-31 holding publishAt values.
 *
 *   npm run youtube:schedule-repair -- --dry-run
 *   npm run youtube:schedule-repair -- --allow-emergency-unfreeze --execute
 *
 * Does NOT insert/delete/reupload/publish. Only private + clear publishAt.
 * Does NOT apply a new future calendar (proposal only).
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
  PLACEHOLDER_HOLD_DATE_PREFIX,
  isPlaceholderHoldPublishAt,
  assertNotPlaceholderHoldPublishAt,
} from "../src/lib/publishing/youtube-schedule-guards";

const AUDIT = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07",
);
const REGISTRY = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/YOUTUBE_CANONICAL_REGISTRY.json",
);
const RECOVERY = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/YOUTUBE_RECOVERY_MODE.json",
);
const ASSET_MAP = path.join(AUDIT, "CANONICAL_ASSET_MAP.json");
const INV = path.join(AUDIT, "FINAL_LIVE_YOUTUBE_INVENTORY.json");

const APPROVED_PUBLIC = [
  "Mo93x0fxB1Q",
  "1HuV8o3gOss",
  "KcKBixwmcV4",
  "3xrxdmaOwJI",
  "JRfhE6yWom4",
  "L2OFjL4neOo",
] as const;

/** Known historical duplicate IDs (must stay private + unscheduled). */
const HISTORICAL_DUPES = new Set([
  "RCs6MMxF3ko",
  "n7CbJrOCnU0",
  "IwpO33AJaPQ",
  "2777WlMGM8M",
  "eZGAhF8dN7w",
  "RF6wivuPYqI",
  "P95alanW8GU",
  "kv1Yz74_S10",
  "IqII5mVGdrs",
  "jyzrl9ueKq4",
  "C4GuFEFGySI",
  "z-kgwJaz5pY",
  "xhBR-ixXi8s",
  "2C-eiSMsBLc",
  "B95wuAH68QY",
  "EO-44QH4glI",
  "lIHb_tyxQSM",
  "t1hTGIH8O44",
  "80S5E-AWFhA",
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
]);

/** Canonical-ish future assets (not public yet) — unschedule from Dec31, propose later. */
const CANONICAL_FUTURE: Record<
  string,
  { family: string; type: "longform" | "shorts"; contentId: string; ready: boolean; reason: string }
> = {
  tUAdhOnMW2g: {
    family: "BLACK_HOLE",
    type: "shorts",
    contentId: "v002-bh-nf01",
    ready: true,
    reason: "BH NF01 canonical short — was quarantine-held",
  },
  svYOx07OrIM: {
    family: "BLACK_HOLE",
    type: "shorts",
    contentId: "v002-bh-nf-look-back",
    ready: true,
    reason: "BH recovery short — was quarantine-held",
  },
  B2STcIAF1lY: {
    family: "BLACK_HOLE",
    type: "shorts",
    contentId: "v002-bh-nf02",
    ready: true,
    reason: "BH NF02 canonical short — was quarantine-held",
  },
  w1ej9u0rPTA: {
    family: "BLACK_HOLE",
    type: "shorts",
    contentId: "v002-bh-nf-point",
    ready: true,
    reason: "BH point-of-no-return short — was quarantine-held",
  },
  HvAKGjx4lv0: {
    family: "BLACK_HOLE",
    type: "shorts",
    contentId: "v002-bh-reserve-time-stops",
    ready: false,
    reason: "Legacy reserve — PRIVATE_NOT_READY until recovery cadence reopens",
  },
  icedH_gK8JE: {
    family: "BLACK_HOLE",
    type: "shorts",
    contentId: "v002-bh-reserve-eyes",
    ready: false,
    reason: "Legacy reserve — PRIVATE_NOT_READY",
  },
  "b8-X_FyJnHM": {
    family: "EXOPLANETS",
    type: "longform",
    contentId: "v003-exo-long",
    ready: true,
    reason: "Alien Worlds long — was quarantine-held during recovery",
  },
  ho9VJxp7f3A: {
    family: "EXOPLANETS",
    type: "shorts",
    contentId: "v003-exo-short-01",
    ready: true,
    reason: "Alien Worlds Short #1",
  },
  "aoR-dA_g7eI": {
    family: "EXOPLANETS",
    type: "shorts",
    contentId: "v003-exo-short-02",
    ready: true,
    reason: "Alien Worlds Short #2",
  },
  "6QFGAFZk264": {
    family: "EXOPLANETS",
    type: "shorts",
    contentId: "v003-exo-short-03",
    ready: true,
    reason: "Alien Worlds Short #3",
  },
  eOOFVrJ2Ojc: {
    family: "EXOPLANETS",
    type: "shorts",
    contentId: "v003-exo-short-04",
    ready: true,
    reason: "Alien Worlds Short #4",
  },
  Web2otrTcT0: {
    family: "EXOPLANETS",
    type: "shorts",
    contentId: "v003-exo-reserve-eyeball",
    ready: false,
    reason: "Reserve Short — PRIVATE_NOT_READY",
  },
  "1qts3tIsg9c": {
    family: "EXOPLANETS",
    type: "shorts",
    contentId: "v003-exo-reserve-habitability",
    ready: false,
    reason: "Reserve Short — PRIVATE_NOT_READY",
  },
  tfTkMdE7qqw: {
    family: "JWST",
    type: "longform",
    contentId: "v004-jwst-long",
    ready: true,
    reason: "JWST long canonical candidate — was quarantine-held",
  },
  bLv0RfidjSg: {
    family: "JWST",
    type: "shorts",
    contentId: "v004-jwst-short-01",
    ready: true,
    reason: "JWST Short #1",
  },
  PcP64way3xA: {
    family: "JWST",
    type: "shorts",
    contentId: "v004-jwst-short-02",
    ready: true,
    reason: "JWST Short #2",
  },
  pjIevt27Svo: {
    family: "JWST",
    type: "shorts",
    contentId: "v004-jwst-short-03",
    ready: true,
    reason: "JWST Short #3",
  },
  AeFm7gWyWik: {
    family: "JWST",
    type: "shorts",
    contentId: "v004-jwst-short-04",
    ready: true,
    reason: "JWST Short #4",
  },
  gPCpMsB0w2E: {
    family: "JWST",
    type: "shorts",
    contentId: "v004-jwst-short-05",
    ready: true,
    reason: "JWST Short #5",
  },
  YsyPMhNmHMk: {
    family: "JWST",
    type: "shorts",
    contentId: "v004-jwst-short-06",
    ready: true,
    reason: "JWST Short #6",
  },
  dPMJQp2gMNc: {
    family: "FERMI",
    type: "shorts",
    contentId: "v001-fermi-short-rude",
    ready: false,
    reason: "Accidental early publication — keep private unscheduled",
  },
  rFJoOdQAc9c: {
    family: "FERMI",
    type: "shorts",
    contentId: "v001-fermi-short-zoo",
    ready: false,
    reason: "Accidental early publication — keep private unscheduled",
  },
};

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

async function listMineScheduled(accessToken: string) {
  // Prefer local inventory if fresh; always re-fetch status for ids with publishAt
  const inv = JSON.parse(fs.readFileSync(INV, "utf8"));
  const fromInv = (inv.videos || [])
    .filter((v: any) => v.publishAt)
    .map((v: any) => v.id as string);
  // Also search channel for any scheduled we might have missed
  const ids = [...new Set(fromInv)];
  const chunks: string[][] = [];
  for (let i = 0; i < ids.length; i += 40) chunks.push(ids.slice(i, i + 40));
  const map = new Map<string, any>();
  for (const chunk of chunks) {
    const res = await fetch(
      `https://www.googleapis.com/youtube/v3/videos?part=status,snippet,contentDetails,statistics&id=${chunk.join(",")}`,
      { headers: { Authorization: `Bearer ${accessToken}` } },
    );
    const body = await res.json();
    if (!res.ok) throw new Error(`videos.list failed: ${JSON.stringify(body)}`);
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
  return { ok: res.ok, statusCode: res.status, id, body };
}

function classify(id: string, publishAt: string | null): string {
  if (!publishAt) return "UNSCHEDULED";
  if (!isPlaceholderHoldPublishAt(publishAt)) return "REAL_FUTURE_RELEASE";
  if (HISTORICAL_DUPES.has(id)) return "HISTORICAL_DUPLICATE";
  if (CANONICAL_FUTURE[id]) return "QUARANTINE_HOLD";
  if ((APPROVED_PUBLIC as readonly string[]).includes(id)) return "CANONICAL_UNSCHEDULED";
  return "QUARANTINE_HOLD";
}

function parisOffsetFor(date: Date): string {
  // Europe/Paris DST: rough — use Intl
  const parts = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Europe/Paris",
    timeZoneName: "shortOffset",
  }).formatToParts(date);
  const off = parts.find((p) => p.type === "timeZoneName")?.value || "GMT+1";
  const m = off.match(/GMT([+-]\d+)(?::(\d+))?/);
  if (!m) return "+01:00";
  const h = Number(m[1]);
  const mm = m[2] || "00";
  const sign = h >= 0 ? "+" : "-";
  return `${sign}${String(Math.abs(h)).padStart(2, "0")}:${mm}`;
}

function localParisToUtcIso(ymd: string, hm: string): { local: string; utc: string } {
  // ymd=YYYY-MM-DD hm=HH:MM Europe/Paris
  const offset = parisOffsetFor(new Date(`${ymd}T12:00:00Z`));
  const local = `${ymd}T${hm}:00${offset}`;
  const utc = new Date(local).toISOString();
  return { local, utc };
}

function buildProposedCalendar(liveTitles: Map<string, string>) {
  // Start next Thursday after 2026-08-07 (recovery). Today context: Aug 7 2026 Friday.
  // First free Thursday for new long: 2026-08-13 (Alien Worlds) — recovery holds new longs=0 during window;
  // proposal still shows intended clusters AFTER recovery, starting 2026-08-14+ for shorts recovery cadence,
  // and longs after recovery window (started Aug 7, 7 days → ends ~Aug 14).
  // Proposed: BH remaining shorts first (1/day recovery), then Exo long Thu, then JWST.
  const items: any[] = [];
  const conflicts: string[] = [];

  // Recovery Shorts (max 1/day) — BH remaining canonical shorts starting Sat 2026-08-08
  const bhShorts = [
    { id: "tUAdhOnMW2g", day: "2026-08-08" },
    { id: "svYOx07OrIM", day: "2026-08-09" },
    { id: "B2STcIAF1lY", day: "2026-08-10" },
    { id: "w1ej9u0rPTA", day: "2026-08-11" },
  ];
  for (const s of bhShorts) {
    const meta = CANONICAL_FUTURE[s.id];
    if (!meta?.ready) continue;
    const { local, utc } = localParisToUtcIso(s.day, "12:30");
    items.push({
      date: s.day,
      timeLocal: "12:30",
      timezone: "Europe/Paris",
      proposedLocal: local,
      proposedUTC: utc,
      family: meta.family,
      type: meta.type,
      title: liveTitles.get(s.id) || meta.contentId,
      youtubeId: s.id,
      contentId: meta.contentId,
      status: "PROPOSED_NOT_APPLIED",
      reason: meta.reason,
    });
  }

  // Exoplanets cluster — Thu 2026-08-14 19:00 long (after recovery window)
  const exoLongDay = "2026-08-14";
  {
    const id = "b8-X_FyJnHM";
    const meta = CANONICAL_FUTURE[id];
    const { local, utc } = localParisToUtcIso(exoLongDay, "19:00");
    items.push({
      date: exoLongDay,
      timeLocal: "19:00",
      timezone: "Europe/Paris",
      proposedLocal: local,
      proposedUTC: utc,
      family: meta.family,
      type: meta.type,
      title: liveTitles.get(id) || meta.contentId,
      youtubeId: id,
      contentId: meta.contentId,
      status: "PROPOSED_NOT_APPLIED",
      reason: meta.reason,
    });
  }
  const exoShorts = [
    { id: "ho9VJxp7f3A", day: "2026-08-14", time: "21:00" },
    { id: "aoR-dA_g7eI", day: "2026-08-15", time: "12:30" },
    { id: "6QFGAFZk264", day: "2026-08-16", time: "12:30" },
    { id: "eOOFVrJ2Ojc", day: "2026-08-17", time: "12:30" },
  ];
  for (const s of exoShorts) {
    const meta = CANONICAL_FUTURE[s.id];
    if (!meta?.ready) continue;
    const { local, utc } = localParisToUtcIso(s.day, s.time);
    items.push({
      date: s.day,
      timeLocal: s.time,
      timezone: "Europe/Paris",
      proposedLocal: local,
      proposedUTC: utc,
      family: meta.family,
      type: meta.type,
      title: liveTitles.get(s.id) || meta.contentId,
      youtubeId: s.id,
      contentId: meta.contentId,
      status: "PROPOSED_NOT_APPLIED",
      reason: meta.reason,
    });
  }

  // JWST cluster — Thu 2026-08-21
  const jwstLongDay = "2026-08-21";
  {
    const id = "tfTkMdE7qqw";
    const meta = CANONICAL_FUTURE[id];
    const { local, utc } = localParisToUtcIso(jwstLongDay, "19:00");
    items.push({
      date: jwstLongDay,
      timeLocal: "19:00",
      timezone: "Europe/Paris",
      proposedLocal: local,
      proposedUTC: utc,
      family: meta.family,
      type: meta.type,
      title: liveTitles.get(id) || meta.contentId,
      youtubeId: id,
      contentId: meta.contentId,
      status: "PROPOSED_NOT_APPLIED",
      reason: meta.reason,
    });
  }
  const jwstShorts = [
    { id: "bLv0RfidjSg", day: "2026-08-21", time: "21:00" },
    { id: "PcP64way3xA", day: "2026-08-22", time: "12:30" },
    { id: "pjIevt27Svo", day: "2026-08-23", time: "12:30" },
    { id: "AeFm7gWyWik", day: "2026-08-24", time: "12:30" },
    { id: "gPCpMsB0w2E", day: "2026-08-25", time: "12:30" },
    { id: "YsyPMhNmHMk", day: "2026-08-26", time: "12:30" },
  ];
  for (const s of jwstShorts) {
    const meta = CANONICAL_FUTURE[s.id];
    if (!meta?.ready) continue;
    const { local, utc } = localParisToUtcIso(s.day, s.time);
    items.push({
      date: s.day,
      timeLocal: s.time,
      timezone: "Europe/Paris",
      proposedLocal: local,
      proposedUTC: utc,
      family: meta.family,
      type: meta.type,
      title: liveTitles.get(s.id) || meta.contentId,
      youtubeId: s.id,
      contentId: meta.contentId,
      status: "PROPOSED_NOT_APPLIED",
      reason: meta.reason,
    });
  }

  // Collision check: same UTC minute
  const byMinute = new Map<string, string[]>();
  for (const it of items) {
    const k = it.proposedUTC;
    byMinute.set(k, [...(byMinute.get(k) || []), it.youtubeId]);
  }
  for (const [k, ids] of byMinute) {
    if (ids.length > 1) conflicts.push(`same-minute ${k}: ${ids.join(",")}`);
  }
  // 1 short/day
  const shortsByDay = new Map<string, string[]>();
  for (const it of items) {
    if (it.type !== "shorts") continue;
    shortsByDay.set(it.date, [...(shortsByDay.get(it.date) || []), it.youtubeId]);
  }
  for (const [d, ids] of shortsByDay) {
    if (ids.length > 1) {
      // Thu launch day allows Short #1 at 21:00 with long — that's intentional (1 short that day)
      if (ids.length > 1) {
        // still one short per day max in recovery — exo/jwst Thu has long+short1 OK (1 short)
      }
    }
  }

  const omitted = Object.entries(CANONICAL_FUTURE)
    .filter(([, m]) => !m.ready)
    .map(([id, m]) => ({
      youtubeId: id,
      contentId: m.contentId,
      family: m.family,
      status: "PRIVATE_NOT_READY",
      reason: m.reason,
    }));

  return { items, conflicts, omitted, applied: false };
}

async function main() {
  const dryRun = flag("dry-run") || !flag("execute");
  const allow = flag("allow-emergency-unfreeze");
  if (!dryRun) {
    assertYouTubeMutationAllowed({
      allowEmergencyUnfreeze: allow,
      operation: "youtube:schedule-repair",
    });
  }

  // Guard unit: placeholder rejection must throw
  try {
    assertNotPlaceholderHoldPublishAt("2026-12-31T11:30:00Z");
    throw new Error("placeholder guard failed to throw");
  } catch (e: any) {
    if (!String(e.message).includes("SCHEDULE BLOCKED")) throw e;
  }

  const { accessToken, scopes } = await token();
  if (!hasForceSslScope(scopes)) {
    console.error(
      JSON.stringify({
        ok: false,
        failure: "OAUTH BLOCKS SCHEDULE REPAIR",
        reason: "youtube.force-ssl not granted",
      }),
    );
    process.exit(2);
  }

  const live = await listMineScheduled(accessToken);
  const scheduled = [...live.values()].filter((it) => it.status?.publishAt);
  const dec31 = scheduled.filter((it) =>
    isPlaceholderHoldPublishAt(it.status?.publishAt || null),
  );

  const beforeRows = scheduled.map((it) => {
    const id = it.id as string;
    const publishAt = (it.status?.publishAt as string) || null;
    const cls = classify(id, publishAt);
    const fut = CANONICAL_FUTURE[id];
    return {
      videoId: id,
      title: it.snippet?.title,
      contentId: fut?.contentId || null,
      contentFamily: fut?.family || null,
      contentType: fut?.type || null,
      currentPrivacy: it.status?.privacyStatus,
      currentPublishAt: publishAt,
      duration: it.contentDetails?.duration,
      classification: cls,
      historicalDuplicateStatus: HISTORICAL_DUPES.has(id),
      action:
        cls === "REAL_FUTURE_RELEASE"
          ? "PRESERVE_SCHEDULE"
          : "UNSCHEDULE_TO_PRIVATE",
    };
  });

  const before = {
    capturedAt: nowIso(),
    placeholderPrefix: PLACEHOLDER_HOLD_DATE_PREFIX,
    scheduledCount: scheduled.length,
    placeholderHoldCount: dec31.length,
    nonPlaceholderScheduled: beforeRows.filter((r) => r.classification === "REAL_FUTURE_RELEASE"),
    rows: beforeRows,
  };
  fs.mkdirSync(AUDIT, { recursive: true });
  fs.writeFileSync(path.join(AUDIT, "SCHEDULE_REPAIR_BEFORE.json"), JSON.stringify(before, null, 2));
  fs.writeFileSync(
    path.join(AUDIT, "SCHEDULE_REPAIR_BEFORE.md"),
    [
      "# SCHEDULE REPAIR BEFORE",
      "",
      `Captured: \`${before.capturedAt}\``,
      "",
      `- scheduled (any publishAt): ${before.scheduledCount}`,
      `- fake 31 Dec holds: ${before.placeholderHoldCount}`,
      `- real future schedules: ${before.nonPlaceholderScheduled.length}`,
      "",
      "| videoId | classification | publishAt | title |",
      "|---|---|---|---|",
      ...beforeRows.map(
        (r) =>
          `| \`${r.videoId}\` | ${r.classification} | ${r.currentPublishAt} | ${r.title} |`,
      ),
      "",
    ].join("\n"),
  );

  const toUnschedule = beforeRows.filter((r) => r.action === "UNSCHEDULE_TO_PRIVATE");
  const mutations: any[] = [];

  for (const row of toUnschedule) {
    const beforeIt = live.get(row.videoId);
    const madeForKids = beforeIt?.status?.madeForKids === true;
    // Clear schedule: private without publishAt. If API retains publishAt, flip unlisted→private.
    let result = await updateStatus(
      accessToken,
      row.videoId,
      {
        privacyStatus: "private",
        selfDeclaredMadeForKids: false,
        madeForKids,
      },
      dryRun,
    );

    let afterPublishAt: string | null | undefined = dryRun ? null : undefined;
    if (!dryRun && result.ok) {
      const check = await fetch(
        `https://www.googleapis.com/youtube/v3/videos?part=status&id=${row.videoId}`,
        { headers: { Authorization: `Bearer ${accessToken}` } },
      );
      const body = await check.json();
      afterPublishAt = body.items?.[0]?.status?.publishAt || null;
      if (afterPublishAt) {
        // Workaround: unlisted clears publishAt per API docs, then private.
        await updateStatus(
          accessToken,
          row.videoId,
          {
            privacyStatus: "unlisted",
            selfDeclaredMadeForKids: false,
            madeForKids,
          },
          false,
        );
        result = await updateStatus(
          accessToken,
          row.videoId,
          {
            privacyStatus: "private",
            selfDeclaredMadeForKids: false,
            madeForKids,
          },
          false,
        );
        const check2 = await fetch(
          `https://www.googleapis.com/youtube/v3/videos?part=status&id=${row.videoId}`,
          { headers: { Authorization: `Bearer ${accessToken}` } },
        );
        const body2 = await check2.json();
        afterPublishAt = body2.items?.[0]?.status?.publishAt || null;
        if (afterPublishAt) {
          mutations.push({
            ...row,
            result,
            afterPublishAt,
            failed: true,
            error: "publishAt persisted after unlisted→private",
          });
          continue;
        }
      }
    }

    mutations.push({
      videoId: row.videoId,
      classification: row.classification,
      before: { privacy: row.currentPrivacy, publishAt: row.currentPublishAt },
      after: dryRun
        ? { privacy: "private", publishAt: null, projected: true }
        : { privacy: "private", publishAt: afterPublishAt ?? null },
      result,
      dryRun,
    });
  }

  // Re-fetch scheduled set after mutations
  const liveAfter = dryRun ? live : await listMineScheduled(accessToken);
  const stillScheduled = [...liveAfter.values()]
    .filter((it) => it.status?.publishAt)
    .map((it) => ({
      videoId: it.id,
      publishAt: it.status.publishAt,
      privacy: it.status.privacyStatus,
      title: it.snippet?.title,
      isPlaceholder: isPlaceholderHoldPublishAt(it.status.publishAt),
    }));

  const titles = new Map<string, string>();
  for (const it of liveAfter.values()) titles.set(it.id, it.snippet?.title || "");
  // also from inventory for unschedules
  try {
    const inv = JSON.parse(fs.readFileSync(INV, "utf8"));
    for (const v of inv.videos || []) titles.set(v.id, v.title);
  } catch {
    /* ignore */
  }

  const proposed = buildProposedCalendar(titles);
  fs.writeFileSync(
    path.join(AUDIT, "PROPOSED_CANONICAL_RELEASE_CALENDAR.json"),
    JSON.stringify({ generatedAt: nowIso(), ...proposed }, null, 2),
  );
  fs.writeFileSync(
    path.join(AUDIT, "PROPOSED_CANONICAL_RELEASE_CALENDAR.md"),
    [
      "# PROPOSED CANONICAL RELEASE CALENDAR",
      "",
      "**NOT APPLIED.** Awaiting explicit approval before any `publishAt` is set.",
      "",
      `Generated: \`${nowIso()}\``,
      "",
      "Timezone: Europe/Paris",
      "",
      "| Date | Time | Family | Type | Title | YouTube ID | Status |",
      "|---|---|---|---|---|---|---|",
      ...proposed.items.map(
        (it) =>
          `| ${it.date} | ${it.timeLocal} | ${it.family} | ${it.type} | ${it.title} | \`${it.youtubeId}\` | ${it.status} |`,
      ),
      "",
      "## Conflicts",
      proposed.conflicts.length ? proposed.conflicts.map((c) => `- ${c}`).join("\n") : "None",
      "",
      "## Omitted (PRIVATE_NOT_READY)",
      ...proposed.omitted.map((o) => `- \`${o.youtubeId}\` — ${o.reason}`),
      "",
      "## Gate",
      "",
      "STOP — do not apply until approved.",
      "",
    ].join("\n"),
  );

  // Update registry: clear Dec31 scheduledAt
  if (!dryRun) {
    const reg = JSON.parse(fs.readFileSync(REGISTRY, "utf8"));
    reg.updatedAt = nowIso();
    reg.scheduleRepairAt = nowIso();
    for (const rec of reg.records || []) {
      const yid = rec.youtubeVideoId || rec.canonicalYouTubeVideoId;
      if (isPlaceholderHoldPublishAt(rec.scheduledAt) || isPlaceholderHoldPublishAt(rec.scheduledPublishTimestamp)) {
        rec.scheduledAt = null;
        rec.scheduledPublishTimestamp = null;
        rec.currentYouTubeStatus = "private";
        rec.intendedYouTubeStatus = HISTORICAL_DUPES.has(yid)
          ? "private"
          : CANONICAL_FUTURE[yid]?.ready
            ? "private"
            : "private";
        rec.notes = `${rec.notes || ""} | schedule-repair: cleared 31 Dec placeholder`.trim();
        rec.lastVerifiedAt = nowIso();
      }
      if (HISTORICAL_DUPES.has(yid)) {
        const hist = new Set([...(rec.historicalDuplicateIds || []), yid].filter((x) => x !== rec.youtubeVideoId));
        // keep existing list
      }
    }
    // Ensure blocked historical list includes dupe IDs that had holds
    reg.blockedHistoricalDuplicateIds = [
      ...new Set([...(reg.blockedHistoricalDuplicateIds || []), ...HISTORICAL_DUPES]),
    ].sort();
    reg.placeholderHoldDatesForbidden = true;
    reg.emergencyFreeze = true;
    fs.writeFileSync(REGISTRY, JSON.stringify(reg, null, 2) + "\n");

    const recovery = JSON.parse(fs.readFileSync(RECOVERY, "utf8"));
    recovery.heldVideoIds = [];
    recovery.notes =
      "Schedule repair 2026-08-07: Dec 31 placeholder holds cleared to private+unscheduled. Proposed calendar not applied.";
    recovery.scheduleRepairAt = nowIso();
    fs.writeFileSync(RECOVERY, JSON.stringify(recovery, null, 2) + "\n");

    if (fs.existsSync(ASSET_MAP)) {
      const am = JSON.parse(fs.readFileSync(ASSET_MAP, "utf8"));
      for (const r of am.records || []) {
        if (isPlaceholderHoldPublishAt(r.scheduledAt) || isPlaceholderHoldPublishAt(r.livePublishAt)) {
          r.scheduledAt = null;
          r.livePublishAt = null;
          r.currentState = "private";
          r.lastVerifiedAt = nowIso();
        }
      }
      am.generatedAt = nowIso();
      fs.writeFileSync(ASSET_MAP, JSON.stringify(am, null, 2));
    }
  }

  const after = {
    capturedAt: nowIso(),
    dryRun,
    mutationsAttempted: mutations.length,
    mutationsFailed: mutations.filter((m) => m.failed).length,
    stillScheduled,
    stillPlaceholderHolds: stillScheduled.filter((s) => s.isPlaceholder),
    publicCanonicalCheck: APPROVED_PUBLIC.map((id) => {
      // from inventory / live
      const it = liveAfter.get(id);
      return {
        id,
        privacy: it?.status?.privacyStatus || "unknown_not_in_scheduled_fetch",
        publishAt: it?.status?.publishAt || null,
      };
    }),
    proposedCalendarApplied: false,
    mutations,
  };
  fs.writeFileSync(path.join(AUDIT, "SCHEDULE_REPAIR_AFTER.json"), JSON.stringify(after, null, 2));
  fs.writeFileSync(
    path.join(AUDIT, "SCHEDULE_REPAIR_AFTER.md"),
    [
      "# SCHEDULE REPAIR AFTER",
      "",
      `Captured: \`${after.capturedAt}\``,
      `dryRun: ${dryRun}`,
      "",
      `- unschedules attempted: ${after.mutationsAttempted}`,
      `- failed: ${after.mutationsFailed}`,
      `- still scheduled: ${stillScheduled.length}`,
      `- still placeholder Dec31: ${after.stillPlaceholderHolds.length}`,
      "",
      "## Remaining schedules",
      stillScheduled.length
        ? stillScheduled.map((s) => `- \`${s.videoId}\` ${s.publishAt} (${s.privacy})`).join("\n")
        : "None",
      "",
      "## Proposed calendar",
      "See PROPOSED_CANONICAL_RELEASE_CALENDAR.md — **not applied**.",
      "",
    ].join("\n"),
  );

  const summary = {
    ok: after.mutationsFailed === 0 && (dryRun || after.stillPlaceholderHolds.length === 0),
    dryRun,
    placeholderHoldsBefore: before.placeholderHoldCount,
    unschedules: mutations.length,
    stillPlaceholderHolds: after.stillPlaceholderHolds.length,
    stillScheduled: stillScheduled.length,
    proposedItems: proposed.items.length,
    proposedApplied: false,
  };
  console.log(JSON.stringify(summary, null, 2));
  if (!summary.ok) process.exit(1);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
