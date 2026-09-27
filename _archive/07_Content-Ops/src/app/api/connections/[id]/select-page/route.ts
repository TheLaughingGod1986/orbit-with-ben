import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/storage/prisma";
import { encryptSecret } from "@/lib/security/token-crypto";
import { z } from "zod";
import { requireOperatorApi } from "@/lib/security/operator-auth";

const bodySchema = z.object({
  pageId: z.string().min(1),
  instagramBusinessAccountId: z.string().optional().nullable(),
});

export async function POST(
  req: NextRequest,
  ctx: { params: Promise<{ id: string }> },
) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const { id } = await ctx.params;
  const json = await req.json();
  const parsed = bodySchema.safeParse(json);
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.message }, { status: 400 });
  }

  const conn = await prisma.platformConnection.findUnique({ where: { id } });
  if (!conn || conn.platform !== "meta") {
    return NextResponse.json({ error: "Meta connection not found" }, { status: 404 });
  }

  let pages: Array<{
    id: string;
    name?: string;
    access_token?: string;
    instagram_business_account?: { id: string; username?: string; name?: string };
  }> = [];
  try {
    pages = conn.metadataJson ? JSON.parse(conn.metadataJson).pages || [] : [];
  } catch {
    pages = [];
  }
  const page = pages.find((p) => p.id === parsed.data.pageId);
  if (!page) {
    return NextResponse.json({ error: "Selected Page not found on this connection" }, { status: 400 });
  }

  const igId =
    parsed.data.instagramBusinessAccountId || page.instagram_business_account?.id || null;
  const ig =
    igId && page.instagram_business_account?.id === igId
      ? page.instagram_business_account
      : pages
          .map((p) => p.instagram_business_account)
          .find((a) => a?.id === igId) || page.instagram_business_account;

  const updated = await prisma.platformConnection.update({
    where: { id },
    data: {
      pageId: page.id,
      accountName: page.name || conn.accountName,
      instagramBusinessAccountId: ig?.id || null,
      accountUsername: ig?.username || null,
      connectionStatus: "connected",
      lastConnectionError: ig
        ? null
        : "Page selected, but no linked Instagram professional account was found.",
      lastValidatedAt: new Date(),
    },
  });

  if (page.access_token) {
    await prisma.platformConnection.upsert({
      where: {
        platform_externalUserId: {
          platform: "facebook_reels",
          externalUserId: page.id,
        },
      },
      create: {
        platform: "facebook_reels",
        externalUserId: page.id,
        pageId: page.id,
        accountName: page.name,
        accountType: "facebook_page",
        connectionStatus: "connected",
        accessTokenEncrypted: encryptSecret(page.access_token),
        lastValidatedAt: new Date(),
      },
      update: {
        accountName: page.name,
        connectionStatus: "connected",
        accessTokenEncrypted: encryptSecret(page.access_token),
        disconnectedAt: null,
      },
    });
  }

  if (ig?.id && page.access_token) {
    await prisma.platformConnection.upsert({
      where: {
        platform_externalUserId: {
          platform: "instagram_reels",
          externalUserId: ig.id,
        },
      },
      create: {
        platform: "instagram_reels",
        externalUserId: ig.id,
        pageId: page.id,
        instagramBusinessAccountId: ig.id,
        accountName: ig.name,
        accountUsername: ig.username,
        accountType: "instagram_professional",
        connectionStatus: "connected",
        accessTokenEncrypted: encryptSecret(page.access_token),
        lastValidatedAt: new Date(),
      },
      update: {
        pageId: page.id,
        accountUsername: ig.username,
        connectionStatus: "connected",
        accessTokenEncrypted: encryptSecret(page.access_token),
        disconnectedAt: null,
      },
    });
  }

  return NextResponse.json({
    ok: true,
    message: "Page selection saved",
    connection: {
      id: updated.id,
      pageId: updated.pageId,
      instagramBusinessAccountId: updated.instagramBusinessAccountId,
    },
  });
}
