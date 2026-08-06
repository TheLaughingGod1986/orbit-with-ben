#!/usr/bin/env tsx
/**
 * Non-destructive shelf verification vs FINAL_SHELF_VERIFY.json
 *
 *   npm run youtube:shelf-verify
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";
import { loadYouTubeRecoveryConfig } from "../src/lib/publishing/youtube-recovery";

const AUDIT = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07",
);
const BASELINE = path.join(AUDIT, "FINAL_SHELF_VERIFY.json");

type Expected = {
  id: string;
  privacy: string;
  publishAt: string | null;
  role: string;
};

const EXPECTED: Expected[] = [
  { id: "Mo93x0fxB1Q", privacy: "public", publishAt: null, role: "fermi_long" },
  { id: "1HuV8o3gOss", privacy: "public", publishAt: null, role: "fermi_short" },
  { id: "KcKBixwmcV4", privacy: "public", publishAt: null, role: "fermi_short" },
  { id: "3xrxdmaOwJI", privacy: "public", publishAt: null, role: "bh_long_canonical" },
  { id: "JRfhE6yWom4", privacy: "public", publishAt: null, role: "bh_short_canonical" },
  { id: "L2OFjL4neOo", privacy: "public", publishAt: null, role: "bh_short_canonical" },
  { id: "IwpO33AJaPQ", privacy: "private", publishAt: null, role: "privatized_dupe" },
  { id: "RCs6MMxF3ko", privacy: "private", publishAt: null, role: "privatized_dupe_long" },
  { id: "2C-eiSMsBLc", privacy: "private", publishAt: "2026-12-31T11:30:00Z", role: "held" },
  { id: "IqII5mVGdrs", privacy: "private", publishAt: "2026-12-31T11:30:00Z", role: "held" },
  { id: "lIHb_tyxQSM", privacy: "private", publishAt: "2026-12-31T11:30:00Z", role: "held" },
  { id: "wOlnj7nZWJM", privacy: "private", publishAt: "2026-12-31T11:30:00Z", role: "held" },
  { id: "2uT3wXJLybw", privacy: "private", publishAt: "2026-12-31T11:30:00Z", role: "held" },
  { id: "tUAdhOnMW2g", privacy: "private", publishAt: "2026-08-07T10:30:00Z", role: "canonical_nf01" },
];

async function main() {
  getEnv();
  const connection = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!connection?.accessTokenEncrypted) {
    console.error("No YouTube connection");
    process.exit(2);
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

  const ids = EXPECTED.map((e) => e.id);
  const res = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=status,snippet,statistics&id=${ids.join(",")}`,
    { headers: { Authorization: `Bearer ${token}` } },
  );
  const body = await res.json();
  const byId = new Map((body.items || []).map((it: any) => [it.id as string, it]));

  const rows = EXPECTED.map((exp) => {
    const it = byId.get(exp.id) as any;
    if (!it) {
      return {
        id: exp.id,
        role: exp.role,
        status: "FAIL",
        expected: exp,
        actual: null,
        detail: "Video not returned by API",
      };
    }
    const actual = {
      privacy: it.status?.privacyStatus as string,
      publishAt: (it.status?.publishAt as string) || null,
      views: it.statistics?.viewCount,
      title: it.snippet?.title,
    };
    const privacyOk = actual.privacy === exp.privacy;
    const publishOk =
      exp.publishAt == null ? actual.publishAt == null : actual.publishAt === exp.publishAt;
    // Held videos may stay private with Dec 31 publishAt — allow private without publishAt only as WARNING
    let status: "PASS" | "WARNING" | "FAIL" = privacyOk && publishOk ? "PASS" : "FAIL";
    let detail = "";
    if (exp.role === "held" && privacyOk && actual.publishAt?.startsWith("2026-12-31")) {
      status = "PASS";
    } else if (exp.role === "canonical_nf01" && actual.publishAt === "2026-08-07T10:30:00Z") {
      // may already have gone public if past air time
      if (actual.privacy === "public" && !actual.publishAt) {
        status = "WARNING";
        detail = "NF01 already public (scheduled time passed) — still canonical; not a duplicate";
      } else if (privacyOk && publishOk) status = "PASS";
    } else if (!privacyOk || !publishOk) {
      detail = `expected privacy=${exp.privacy} publishAt=${exp.publishAt}; got privacy=${actual.privacy} publishAt=${actual.publishAt}`;
    }
    return { id: exp.id, role: exp.role, status, expected: exp, actual, detail };
  });

  const publicCount = rows.filter((r) => r.actual && (r.actual as any).privacy === "public").length;
  const unexpectedPublic = rows.filter(
    (r) =>
      r.actual &&
      (r.actual as any).privacy === "public" &&
      !["fermi_long", "fermi_short", "bh_long_canonical", "bh_short_canonical"].includes(r.role) &&
      r.role !== "canonical_nf01",
  );

  const recovery = loadYouTubeRecoveryConfig();
  const baselineExists = fs.existsSync(BASELINE);

  const summary = {
    ok: rows.every((r) => r.status !== "FAIL") && unexpectedPublic.length === 0,
    verifiedAt: new Date().toISOString(),
    publicCount,
    expectedPublic: 6,
    recoveryMode: recovery.recoveryMode,
    baselineFile: baselineExists ? BASELINE : null,
    rows,
    unexpectedPublic: unexpectedPublic.map((r) => r.id),
  };

  fs.mkdirSync(AUDIT, { recursive: true });
  const jsonPath = path.join(AUDIT, "POST_OAUTH_SHELF_VERIFY.json");
  fs.writeFileSync(jsonPath, JSON.stringify(summary, null, 2) + "\n");

  const md = [
    "# Post-OAuth shelf verification",
    "",
    `Verified: ${summary.verifiedAt}`,
    "",
    `Overall: **${summary.ok ? "PASS" : "FAIL"}**`,
    "",
    `| ID | Role | Status | Privacy | publishAt | Views |`,
    `|----|------|--------|---------|-----------|------:|`,
    ...rows.map((r) => {
      const a = r.actual as any;
      return `| ${r.id} | ${r.role} | ${r.status} | ${a?.privacy ?? "—"} | ${a?.publishAt ?? "—"} | ${a?.views ?? "—"} |`;
    }),
    "",
    `Public count: ${publicCount} (expected 6 canonical, NF01 may add +1 after go-live)`,
    unexpectedPublic.length
      ? `Unexpected public: ${unexpectedPublic.map((r) => r.id).join(", ")}`
      : "No unexpected public duplicates in the watched set.",
    "",
  ].join("\n");
  fs.writeFileSync(path.join(AUDIT, "POST_OAUTH_SHELF_VERIFY.md"), md);

  console.log(JSON.stringify(summary, null, 2));
  console.error(`Wrote ${jsonPath}`);
  process.exit(summary.ok ? 0 : 1);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => prisma.$disconnect());
