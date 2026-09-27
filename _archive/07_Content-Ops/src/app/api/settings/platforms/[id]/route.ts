import { NextResponse } from "next/server";
import { prisma } from "@/lib/storage/prisma";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export async function PATCH(
  req: Request,
  ctx: { params: Promise<{ id: string }> },
) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const { id } = await ctx.params;
  const body = await req.json();
  const updated = await prisma.platformSettings.update({
    where: { id },
    data: {
      enabled: body.enabled ?? undefined,
      accountDisplayName: body.accountDisplayName ?? undefined,
      profileUrl: body.profileUrl ?? undefined,
      defaultCallToAction: body.defaultCallToAction ?? undefined,
      defaultHashtags: body.defaultHashtags ?? undefined,
      publishingMethod: body.publishingMethod ?? undefined,
      defaultVisibility: body.defaultVisibility ?? undefined,
    },
  });
  return NextResponse.json(updated);
}
