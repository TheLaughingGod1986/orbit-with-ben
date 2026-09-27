import { NextResponse } from "next/server";
import { prisma } from "@/lib/storage/prisma";
import { getPublishingAdapter } from "@/lib/publishing/adapters";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export async function POST(
  _req: Request,
  ctx: { params: Promise<{ id: string }> },
) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const { id } = await ctx.params;
  const connection = await prisma.platformConnection.findUnique({ where: { id } });
  if (!connection) return NextResponse.json({ error: "Not found" }, { status: 404 });

  const adapter = getPublishingAdapter(connection.platform);
  const result = await adapter.validateConnection(connection);
  await prisma.platformConnection.update({
    where: { id },
    data: {
      connectionStatus: result.status,
      lastValidatedAt: new Date(),
      lastConnectionError: result.ok ? null : result.errors.join("; "),
      accountName: result.accountName || connection.accountName,
      accountUsername: result.accountUsername || connection.accountUsername,
      capabilitiesJson: JSON.stringify(result.capabilities),
    },
  });

  return NextResponse.json({
    ok: result.ok,
    message: result.ok
      ? `Validated: ${result.accountName || connection.accountName || connection.platform}`
      : result.errors.join("; "),
    capabilities: result.capabilities,
  });
}
