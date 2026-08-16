#!/usr/bin/env tsx
/**
 * Additive film → topic-book DESCRIPTION_PRIMARY wiring (no DB reset, no YouTube publish).
 *
 *   npm run affiliate:apply-urls          # ensure live amazon.co.uk destinations
 *   npm run affiliate:wire-topic-books    # approve one /go/{slug} book per long film
 *   npm run affiliate:wire-topic-books -- --dry-run
 *
 * Social Media Manager reads approved DESCRIPTION_PRIMARY placements.
 * Shorts stay at zero affiliate links. Telescope / Brilliant / LEGO unplaced.
 * AMAZON_ASSOCIATE_TAG is never committed — stamped at /go redirect time.
 */

import { prisma } from "../src/lib/storage/prisma";
import {
  wireTopicBookPlacements,
  filmTopicBookPlacementTableRows,
} from "../src/lib/affiliate";

async function main() {
  const dryRun = process.argv.includes("--dry-run");
  const result = await wireTopicBookPlacements({ dryRun });

  console.log(dryRun ? "Dry run — would wire:" : "Wired topic books:");
  console.log(
    JSON.stringify(
      {
        appliedLiveUrls: result.appliedLiveUrls,
        clearedBlocklistPlacements: result.clearedBlocklistPlacements,
        skipped: result.skipped,
        wired: result.wired.map((w) => ({
          filmKey: w.filmKey,
          title: w.title,
          youtubeVideoId: w.youtubeVideoId,
          productSlug: w.productSlug,
          goPath: w.goPath,
          amazonUrl: w.amazonUrl,
          createdVideo: w.createdVideo,
          placementId: w.placementId,
        })),
      },
      null,
      2,
    ),
  );

  console.log("\nPlacement table (for PR / Social Media Manager):");
  for (const row of filmTopicBookPlacementTableRows()) {
    console.log(
      `| ${row.filmTitle} | ${row.youtubeId} | \`${row.productSlug}\` | ${row.amazonUrl} | \`${row.goPath}\` |`,
    );
  }

  if (!dryRun && result.wired.length) {
    console.log(
      "\nDescriptions are generated in Content Ops only — not published to YouTube.com.",
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
