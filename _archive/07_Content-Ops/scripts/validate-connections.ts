#!/usr/bin/env tsx
import { prisma } from "../src/lib/storage/prisma";
import { getPublishingAdapter } from "../src/lib/publishing/adapters";

async function main() {
  const connections = await prisma.platformConnection.findMany({
    where: { disconnectedAt: null },
  });
  if (!connections.length) {
    console.log("No active connections.");
    return;
  }
  for (const conn of connections) {
    const adapter = getPublishingAdapter(conn.platform === "meta" ? "instagram_reels" : conn.platform);
    const result = await adapter.validateConnection(conn);
    console.log(
      JSON.stringify({
        id: conn.id,
        platform: conn.platform,
        ok: result.ok,
        status: result.status,
        accountName: result.accountName || conn.accountName,
        errors: result.errors,
        warnings: result.warnings,
      }),
    );
    await prisma.platformConnection.update({
      where: { id: conn.id },
      data: {
        connectionStatus: result.status,
        lastValidatedAt: new Date(),
        lastConnectionError: result.errors[0] || null,
      },
    });
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => prisma.$disconnect());
