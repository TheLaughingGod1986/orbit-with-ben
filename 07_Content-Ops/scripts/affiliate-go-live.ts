#!/usr/bin/env tsx
/**
 * Affiliate go-live helper.
 *
 *   npm run affiliate:verify          # readiness report
 *   npm run affiliate:verify -- --probe
 *   npm run affiliate:apply-urls      # write live destination URLs into DB
 *   npm run affiliate:apply-urls -- --dry-run
 */

import { prisma } from "../src/lib/storage/prisma";
import {
  applyLiveProductUrls,
  getAffiliateGoLiveReport,
} from "../src/lib/affiliate/go-live-service";

async function main() {
  const args = process.argv.slice(2);
  const cmd = process.env.npm_lifecycle_event || "";
  const apply =
    cmd.includes("apply-urls") || args.includes("apply-urls") || args.includes("--apply-urls");
  const dryRun = args.includes("--dry-run");
  const probe = args.includes("--probe");

  if (apply) {
    const result = await applyLiveProductUrls({ dryRun });
    console.log(dryRun ? "Dry run — would update:" : "Updated:");
    console.log(JSON.stringify(result, null, 2));
    if (!dryRun && result.updated.length) {
      console.log(
        "\nNext: set AMAZON_ASSOCIATE_TAG / BRILLIANT_AFFILIATE_ID, then npm run affiliate:verify",
      );
    }
  }

  const report = await getAffiliateGoLiveReport({ probeGoRoute: probe });
  console.log("\n=== Affiliate go-live ===");
  console.log(report.summary);
  console.log(
    `Tracked redirects: ${report.readyForTrackedRedirects ? "YES" : "NO"} · Paid traffic: ${report.readyForPaidTraffic ? "YES" : "NO"}`,
  );
  console.log("");
  for (const c of report.checks) {
    const mark =
      c.status === "pass" ? "✓" : c.status === "warn" ? "!" : c.status === "manual" ? "…" : "✗";
    console.log(`${mark} [${c.status}] ${c.label}`);
    console.log(`    ${c.detail}`);
  }

  const blockingFails = report.checks.filter((c) => c.blocking && c.status === "fail");
  process.exit(blockingFails.length ? 1 : 0);
}

main()
  .catch((err) => {
    console.error(err);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
