import { NextRequest, NextResponse } from "next/server";
import { getEnv } from "@/lib/env";
import { getPublicBaseUrl, oauthCallbackUrl } from "@/lib/public-base-url";
import { consumeOAuthState } from "@/lib/oauth/state";
import { encryptSecret } from "@/lib/security/token-crypto";
import { prisma } from "@/lib/storage/prisma";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export async function GET(req: NextRequest) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const env = getEnv();
  const base = getPublicBaseUrl(req);
  const url = new URL(req.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  if (!code || !state) {
    return NextResponse.redirect(`${base}/settings/connections?error=missing_code`);
  }
  const consumed = await consumeOAuthState({ platform: "meta", state });
  if (!consumed.ok) {
    return NextResponse.redirect(`${base}/settings/connections?error=${encodeURIComponent(consumed.error)}`);
  }
  if (!env.ORBIT_TOKEN_ENCRYPTION_KEY) {
    return NextResponse.redirect(`${base}/settings/connections?error=encryption_key_required`);
  }

  const redirectUri = oauthCallbackUrl("meta", req);
  const tokenUrl = new URL("https://graph.facebook.com/v21.0/oauth/access_token");
  tokenUrl.searchParams.set("client_id", env.META_APP_ID!);
  tokenUrl.searchParams.set("client_secret", env.META_APP_SECRET!);
  tokenUrl.searchParams.set("redirect_uri", redirectUri);
  tokenUrl.searchParams.set("code", code);
  const tokenRes = await fetch(tokenUrl);
  const tokenBody = await tokenRes.json();
  if (!tokenRes.ok || !tokenBody.access_token) {
    return NextResponse.redirect(`${base}/settings/connections?error=token_exchange_failed`);
  }

  const meRes = await fetch(
    `https://graph.facebook.com/v21.0/me?fields=id,name&access_token=${encodeURIComponent(tokenBody.access_token)}`,
  );
  const me = await meRes.json();
  const pagesRes = await fetch(
    `https://graph.facebook.com/v21.0/me/accounts?fields=id,name,access_token,instagram_business_account{id,username,name}&access_token=${encodeURIComponent(tokenBody.access_token)}`,
  );
  const pagesBody = await pagesRes.json();
  const pages = pagesBody.data || [];
  const firstPage = pages[0];
  const ig = firstPage?.instagram_business_account;

  const externalUserId = String(me.id || "unknown");
  await prisma.platformConnection.upsert({
    where: { platform_externalUserId: { platform: "meta", externalUserId } },
    create: {
      platform: "meta",
      externalUserId,
      accountId: me.id,
      accountName: me.name,
      accountType: "facebook_user",
      pageId: firstPage?.id || null,
      instagramBusinessAccountId: ig?.id || null,
      accountUsername: ig?.username || null,
      connectionStatus: firstPage ? "connected" : "requires_attention",
      grantedScopes: JSON.stringify([
        "pages_show_list",
        "instagram_content_publish",
      ]),
      accessTokenEncrypted: encryptSecret(tokenBody.access_token),
      accessTokenExpiresAt: tokenBody.expires_in
        ? new Date(Date.now() + Number(tokenBody.expires_in) * 1000)
        : null,
      lastValidatedAt: new Date(),
      metadataJson: JSON.stringify({ pages }),
      lastConnectionError: firstPage
        ? null
        : "Connected, but no manageable Facebook Page was found.",
    },
    update: {
      accountName: me.name,
      pageId: firstPage?.id || null,
      instagramBusinessAccountId: ig?.id || null,
      accountUsername: ig?.username || null,
      connectionStatus: firstPage ? "connected" : "requires_attention",
      accessTokenEncrypted: encryptSecret(tokenBody.access_token),
      lastValidatedAt: new Date(),
      metadataJson: JSON.stringify({ pages }),
      disconnectedAt: null,
      lastConnectionError: firstPage
        ? null
        : "Connected, but no manageable Facebook Page was found.",
    },
  });

  // Mirror lightweight connection rows for IG/FB platforms used by jobs
  if (firstPage) {
    await prisma.platformConnection.upsert({
      where: {
        platform_externalUserId: {
          platform: "facebook_reels",
          externalUserId: String(firstPage.id),
        },
      },
      create: {
        platform: "facebook_reels",
        externalUserId: String(firstPage.id),
        pageId: firstPage.id,
        accountName: firstPage.name,
        accountType: "facebook_page",
        connectionStatus: "connected",
        accessTokenEncrypted: encryptSecret(firstPage.access_token || tokenBody.access_token),
        lastValidatedAt: new Date(),
      },
      update: {
        accountName: firstPage.name,
        connectionStatus: "connected",
        accessTokenEncrypted: encryptSecret(firstPage.access_token || tokenBody.access_token),
        disconnectedAt: null,
      },
    });
  }
  if (ig?.id) {
    await prisma.platformConnection.upsert({
      where: {
        platform_externalUserId: {
          platform: "instagram_reels",
          externalUserId: String(ig.id),
        },
      },
      create: {
        platform: "instagram_reels",
        externalUserId: String(ig.id),
        pageId: firstPage?.id,
        instagramBusinessAccountId: ig.id,
        accountName: ig.name,
        accountUsername: ig.username,
        accountType: "instagram_professional",
        connectionStatus: "connected",
        accessTokenEncrypted: encryptSecret(firstPage?.access_token || tokenBody.access_token),
        grantedScopes: JSON.stringify(["instagram_content_publish"]),
        lastValidatedAt: new Date(),
      },
      update: {
        instagramBusinessAccountId: ig.id,
        accountUsername: ig.username,
        connectionStatus: "connected",
        accessTokenEncrypted: encryptSecret(firstPage?.access_token || tokenBody.access_token),
        disconnectedAt: null,
      },
    });
  }

  return NextResponse.redirect(`${base}/settings/connections?connected=meta`);
}
