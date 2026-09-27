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
  if (adapter.revokeConnection) {
    await adapter.revokeConnection(connection);
  }

  await prisma.platformConnection.update({
    where: { id },
    data: {
      connectionStatus: "disconnected",
      disconnectedAt: new Date(),
      accessTokenEncrypted: null,
      refreshTokenEncrypted: null,
      lastConnectionError: null,
    },
  });

  // Cancel future jobs for this connection
  await prisma.publishingJob.updateMany({
    where: {
      platformConnectionId: id,
      status: { in: ["pending", "scheduled", "failed_retryable"] },
    },
    data: {
      status: "cancelled",
      lastErrorMessage: "Connection disconnected",
      completedAt: new Date(),
    },
  });

  return NextResponse.json({
    message: "Disconnected. Historical publish records retained.",
  });
}
