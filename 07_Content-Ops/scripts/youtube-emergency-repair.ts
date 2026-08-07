#!/usr/bin/env tsx
/**
 * Emergency repair mutations — ONLY after force-ssl + explicit allow flags.
 *
 *   npm run youtube:emergency-repair -- --dry-run
 *   npm run youtube:emergency-repair -- --allow-emergency-unfreeze --execute
 *
 * Mutations (non-destructive):
 * 1) Privatize accidental early Fermi Shorts: dPMJQp2gMNc, rFJoOdQAc9c
 * 2) DISABLED: Dec 31 placeholder holds are forbidden — use PRIVATE+unscheduled
 *    (see youtube:schedule-repair). Imminent schedules are listed for manual review only.
 * 3) Confirm approved 6 public + known BH dupes private
 *
 * Does NOT insert/delete/reupload. Does NOT run CDP.
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";
import { hasForceSslScope, parseGrantedScopes } from "../src/lib/publishing/youtube-oauth";
import { assertYouTubeMutationAllowed } from "../src/lib/publishing/youtube-freeze";
import { isPlaceholderHoldPublishAt } from "../src/lib/publishing/youtube-schedule-guards";

const AUDIT = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07",
);
/** @deprecated Placeholder holds forbidden — kept only to detect/reject legacy plans. */
const HOLD_AT = "2026-12-31T11:30:00Z";
const APPROVED_PUBLIC = [
  "Mo93x0fxB1Q",
  "1HuV8o3gOss",
  "KcKBixwmcV4",
  "3xrxdmaOwJI",
  "JRfhE6yWom4",
  "L2OFjL4neOo",
];
const BH_DUPES_PRIVATE = ["RCs6MMxF3ko", "IwpO33AJaPQ"];
const ACCIDENTAL_EARLY_PRIVATE = ["dPMJQp2gMNc", "rFJoOdQAc9c"];

function flag(name: string) {
  return process.argv.includes(`--${name}`);
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
  // Prisma field is grantedScopes (verify-oauth); never scopesGranted.
  const scopes = parseGrantedScopes(
    (fresh as { grantedScopes?: string | null })?.grantedScopes ||
      (connection as { grantedScopes?: string | null }).grantedScopes ||
      "[]",
  );
  return { accessToken, scopes };
}

async function getVideos(accessToken: string, ids: string[]) {
  const res = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=status,snippet&id=${ids.join(",")}`,
    { headers: { Authorization: `Bearer ${accessToken}` } },
  );
  const body = await res.json();
  if (!res.ok) throw new Error(JSON.stringify(body));
  return new Map((body.items || []).map((it: any) => [it.id as string, it]));
}

async function updateStatus(
  accessToken: string,
  id: string,
  status: Record<string, unknown>,
  dryRun: boolean,
) {
  if (dryRun) return { dryRun: true, id, status };
  const res = await fetch(
    "https://www.googleapis.com/youtube/v3/videos?part=status",
    {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id, status }),
    },
  );
  const body = await res.json();
  return { ok: res.ok, statusCode: res.status, id, body };
}

async function main() {
  const dryRun = flag("dry-run") || !flag("execute");
  const allow = flag("allow-emergency-unfreeze");
  // Dry-run is read + plan only; live execute requires explicit unfreeze flag.
  if (!dryRun) {
    assertYouTubeMutationAllowed({
      allowEmergencyUnfreeze: allow,
      operation: "youtube:emergency-repair",
    });
  } else if (!allow) {
    console.error(
      "Note: dry-run planning only. Live execute requires --allow-emergency-unfreeze --execute after force-ssl.",
    );
  }

  const { accessToken, scopes } = await token();
  if (!hasForceSslScope(scopes)) {
    console.error("BLOCKED: youtube.force-ssl not granted. Reconnect OAuth first.");
    process.exit(2);
  }

  // Discover schedules to hold: next 72h + NF cluster + Aug 11 collision +
  // any non-Dec31 publishAt through end of recovery window (unsafe until reconciled).
  const invPath = path.join(AUDIT, "FINAL_LIVE_YOUTUBE_INVENTORY.json");
  const inv = fs.existsSync(invPath) ? JSON.parse(fs.readFileSync(invPath, "utf8")) : null;
  const now = Date.now();
  const horizon72 = now + 72 * 60 * 60 * 1000;
  const recoveryEnd = Date.parse("2026-08-14T00:00:00Z");
  const toHold = new Set<string>();
  for (const v of inv?.videos || []) {
    if (v.privacyStatus !== "private" || !v.publishAt) continue;
    if (String(v.publishAt).startsWith("2026-12-31")) continue;
    const t = Date.parse(v.publishAt);
    if (!Number.isFinite(t) || t < now) continue;
    if (t <= horizon72 || t <= recoveryEnd) toHold.add(v.id);
  }
  for (const id of [
    "tUAdhOnMW2g",
    "svYOx07OrIM",
    "B2STcIAF1lY",
    "w1ej9u0rPTA",
    "HvAKGjx4lv0",
    "8DxCTXUlw74",
  ]) {
    toHold.add(id);
  }
  const imminent = Array.from(toHold);

  const watch = Array.from(
    new Set([
      ...APPROVED_PUBLIC,
      ...BH_DUPES_PRIVATE,
      ...ACCIDENTAL_EARLY_PRIVATE,
      ...imminent,
      "z-DLqoSoEBo",
      "UWwNKYf_aU8",
    ]),
  );
  const beforeMap = await getVideos(accessToken, watch);
  const mutations: any[] = [];

  const plan = [
    ...APPROVED_PUBLIC.map((id) => ({
      id,
      action: "ensure_public",
      status: { privacyStatus: "public", selfDeclaredMadeForKids: false },
    })),
    ...BH_DUPES_PRIVATE.map((id) => ({
      id,
      action: "ensure_private_dupe",
      status: { privacyStatus: "private", selfDeclaredMadeForKids: false },
    })),
    ...ACCIDENTAL_EARLY_PRIVATE.map((id) => ({
      id,
      action: "privatize_accidental_early",
      status: { privacyStatus: "private", selfDeclaredMadeForKids: false },
    })),
    // Dec 31 placeholder holds are forbidden. Imminent schedules are NOT mutated here.
    // Use: npm run youtube:schedule-repair to clear placeholders → private+unscheduled.
    ...imminent.map((id) => ({
      id,
      action: "report_imminent_no_placeholder_hold",
      status: {
        privacyStatus: "private",
        selfDeclaredMadeForKids: false,
      },
      skipMutation: true,
      note: `Do not assign ${HOLD_AT}. Clear via schedule-repair or set a real approved publishAt.`,
    })),
  ];

  for (const step of plan) {
    const before = beforeMap.get(step.id) as any;
    const beforeSnap = before
      ? {
          privacy: before.status?.privacyStatus,
          publishAt: before.status?.publishAt || null,
          title: before.snippet?.title,
        }
      : null;
    // Skip ensure_public if already public without publishAt
    if (step.action === "ensure_public" && beforeSnap?.privacy === "public" && !beforeSnap.publishAt) {
      mutations.push({ ...step, skipped: true, reason: "already_public", before: beforeSnap });
      continue;
    }
    if (step.action === "ensure_private_dupe" && beforeSnap?.privacy === "private" && !beforeSnap.publishAt) {
      mutations.push({ ...step, skipped: true, reason: "already_private", before: beforeSnap });
      continue;
    }
    if (
      step.action === "privatize_accidental_early" &&
      beforeSnap?.privacy === "private" &&
      !beforeSnap.publishAt
    ) {
      mutations.push({ ...step, skipped: true, reason: "already_private", before: beforeSnap });
      continue;
    }
    if ((step as { skipMutation?: boolean }).skipMutation) {
      mutations.push({
        ...step,
        skipped: true,
        reason: "placeholder_holds_forbidden",
        before: beforeSnap,
        isPlaceholder: isPlaceholderHoldPublishAt(beforeSnap?.publishAt),
      });
      continue;
    }
    // Merge madeForKids from existing when present
    const status = {
      ...step.status,
      madeForKids: before?.status?.madeForKids === true ? true : false,
      selfDeclaredMadeForKids: false,
    };
    const result = await updateStatus(accessToken, step.id, status, dryRun);
    mutations.push({ ...step, status, before: beforeSnap, result, dryRun });
  }

  const afterMap = dryRun ? beforeMap : await getVideos(accessToken, watch);
  const log = {
    executedAt: new Date().toISOString(),
    dryRun,
    allowEmergencyUnfreeze: allow,
    forceSsl: true,
    mutations,
    after: Object.fromEntries(
      [...afterMap.entries()].map(([id, it]: any) => [
        id,
        {
          privacy: it.status?.privacyStatus,
          publishAt: it.status?.publishAt || null,
          title: it.snippet?.title,
        },
      ]),
    ),
  };
  fs.mkdirSync(AUDIT, { recursive: true });
  fs.writeFileSync(
    path.join(AUDIT, "EMERGENCY_REPAIR_MUTATION_LOG.json"),
    JSON.stringify(log, null, 2),
  );
  console.log(JSON.stringify({ ok: true, dryRun, mutationCount: mutations.length, logPath: "EMERGENCY_REPAIR_MUTATION_LOG.json" }, null, 2));
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
