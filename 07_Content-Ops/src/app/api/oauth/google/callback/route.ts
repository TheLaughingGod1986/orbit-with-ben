import { NextRequest, NextResponse } from "next/server";
import { getEnv } from "@/lib/env";
import { getPublicBaseUrl, oauthCallbackUrl } from "@/lib/public-base-url";
import { consumeOAuthState } from "@/lib/oauth/state";
import { encryptSecret } from "@/lib/security/token-crypto";
import { prisma } from "@/lib/storage/prisma";
import { YOUTUBE_SCOPES } from "@/lib/publishing/adapters/youtube";
import { encryptionKeyErrorCode } from "@/lib/oauth/callback-errors";

/**
 * Provider redirect. Authenticity is the one-shot OAuth `state` token below —
 * not the operator cookie, which this cross-site navigation may not carry.
 * Starting a Connect still requires an operator session (`../start/route.ts`).
 */
export async function GET(req: NextRequest) {
  try {
    return await handleGoogleCallback(req);
  } catch (err) {
    console.error("[oauth/google] callback failed", err);
    return NextResponse.redirect(
      `${getPublicBaseUrl(req)}/settings/connections?error=connection_save_failed`,
    );
  }
}

async function handleGoogleCallback(req: NextRequest) {
  const url = new URL(req.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const oauthError = url.searchParams.get("error");
  const env = getEnv();
  const base = getPublicBaseUrl(req);

  if (oauthError) {
    return NextResponse.redirect(
      `${base}/settings/connections?error=${encodeURIComponent(oauthError)}`,
    );
  }
  if (!code || !state) {
    return NextResponse.redirect(`${base}/settings/connections?error=missing_code`);
  }

  const consumed = await consumeOAuthState({ platform: "youtube_shorts", state });
  if (!consumed.ok) {
    return NextResponse.redirect(
      `${base}/settings/connections?error=${encodeURIComponent(consumed.error)}`,
    );
  }

  const keyError = encryptionKeyErrorCode();
  if (keyError) {
    return NextResponse.redirect(`${base}/settings/connections?error=${keyError}`);
  }

  const redirectUri = oauthCallbackUrl("google", req);
  const tokenRes = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      code,
      client_id: env.GOOGLE_CLIENT_ID!,
      client_secret: env.GOOGLE_CLIENT_SECRET!,
      redirect_uri: redirectUri,
      grant_type: "authorization_code",
    }),
  });
  const tokenBody = await tokenRes.json();
  if (!tokenRes.ok || !tokenBody.access_token) {
    console.error("[oauth/google] token exchange failed", {
      status: tokenRes.status,
      error: tokenBody?.error,
      description: tokenBody?.error_description,
      redirectUri,
    });
    return NextResponse.redirect(`${base}/settings/connections?error=token_exchange_failed`);
  }

  const channelRes = await fetch(
    "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
    { headers: { Authorization: `Bearer ${tokenBody.access_token}` } },
  );
  const channelBody = await channelRes.json();
  const channel = channelBody.items?.[0];
  const externalUserId = channel?.id || "unknown";

  const expiresAt = new Date(Date.now() + Number(tokenBody.expires_in || 3600) * 1000);
  await prisma.platformConnection.upsert({
    where: {
      platform_externalUserId: {
        platform: "youtube_shorts",
        externalUserId,
      },
    },
    create: {
      platform: "youtube_shorts",
      externalUserId,
      channelId: channel?.id,
      accountId: channel?.id,
      accountName: channel?.snippet?.title,
      accountUsername: channel?.snippet?.customUrl,
      accountType: "youtube_channel",
      avatarUrl: channel?.snippet?.thumbnails?.default?.url,
      profileUrl: channel?.id
        ? `https://www.youtube.com/channel/${channel.id}`
        : null,
      connectionStatus: "connected",
      grantedScopes: JSON.stringify(YOUTUBE_SCOPES),
      accessTokenEncrypted: encryptSecret(tokenBody.access_token),
      refreshTokenEncrypted: tokenBody.refresh_token
        ? encryptSecret(tokenBody.refresh_token)
        : null,
      accessTokenExpiresAt: expiresAt,
      lastValidatedAt: new Date(),
    },
    update: {
      channelId: channel?.id,
      accountName: channel?.snippet?.title,
      accountUsername: channel?.snippet?.customUrl,
      avatarUrl: channel?.snippet?.thumbnails?.default?.url,
      connectionStatus: "connected",
      grantedScopes: JSON.stringify(YOUTUBE_SCOPES),
      accessTokenEncrypted: encryptSecret(tokenBody.access_token),
      refreshTokenEncrypted: tokenBody.refresh_token
        ? encryptSecret(tokenBody.refresh_token)
        : undefined,
      accessTokenExpiresAt: expiresAt,
      lastValidatedAt: new Date(),
      disconnectedAt: null,
      lastConnectionError: null,
    },
  });

  await prisma.platformSettings.updateMany({
    where: { platform: "youtube_shorts" },
    data: {
      connectionStatus: "connected",
      tokenStatus: "configured",
      accountDisplayName: channel?.snippet?.title,
      profileUrl: channel?.id
        ? `https://www.youtube.com/channel/${channel.id}`
        : undefined,
    },
  });

  return NextResponse.redirect(
    `${base}${consumed.redirectPath || "/settings/connections"}?connected=youtube`,
  );
}
