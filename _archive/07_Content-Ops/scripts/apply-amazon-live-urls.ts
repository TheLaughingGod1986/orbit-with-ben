#!/usr/bin/env tsx
/**
 * Additive Amazon Associates UK live-URL apply (does not reset the DB).
 *
 *   npm run affiliate:apply-urls
 *   npm run affiliate:apply-urls -- --dry-run
 *
 * Updates existing rows and creates missing verified topic-book products.
 * Set AMAZON_ASSOCIATE_TAG in the operator env (see docs/AFFILIATE_MONETISATION_SYSTEM.md).
 * Never commit the tag. /go/{slug} stamps tag= at redirect time.
 */

import { prisma } from "../src/lib/storage/prisma";
import { applyLiveProductUrls } from "../src/lib/affiliate/apply-live-urls";

async function main() {
  const dryRun = process.argv.includes("--dry-run");
  const result = await applyLiveProductUrls({ dryRun });
  console.log(dryRun ? "Dry run — would apply:" : "Applied:");
  console.log(JSON.stringify(result, null, 2));
  if (!dryRun && (result.updated.length || result.created.length)) {
    console.log(
      "\nNext: ensure AMAZON_ASSOCIATE_TAG is set in env (see docs), then smoke-test /go/{slug}.",
    );
  }
}

main()
  .catch((err) => {
    console.error(err);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
