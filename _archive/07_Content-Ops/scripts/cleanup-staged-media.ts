#!/usr/bin/env tsx
/**
 * Cleanup helper for temporary staged media metadata.
 * Local mode does not upload to third parties; this clears expired staging markers
 * stored under AppSetting keys prefixed with staged_media:
 */
import { prisma } from "../src/lib/storage/prisma";

async function main() {
  const rows = await prisma.appSetting.findMany({
    where: { key: { startsWith: "staged_media:" } },
  });
  const cutoff = Date.now() - 24 * 60 * 60 * 1000;
  let removed = 0;
  for (const row of rows) {
    try {
      const parsed = JSON.parse(row.value) as { createdAt?: string };
      const created = parsed.createdAt ? Date.parse(parsed.createdAt) : 0;
      if (created && created < cutoff) {
        await prisma.appSetting.delete({ where: { id: row.id } });
        removed += 1;
      }
    } catch {
      await prisma.appSetting.delete({ where: { id: row.id } });
      removed += 1;
    }
  }
  console.log(JSON.stringify({ scanned: rows.length, removed }));
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => prisma.$disconnect());
