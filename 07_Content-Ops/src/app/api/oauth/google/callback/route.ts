import { NextRequest, NextResponse } from "next/server";
import { getEnv } from "@/lib/env";
import { consumeOAuthState } from "@/lib/oauth/state";
import { encryptSecret } from "@/lib/security/token-crypto";
import { prisma } from "@/lib/storage/prisma";
import { YOUTUBE_SCOPES } from "@/lib/publishing/adapters/youtube";

export async function GET(req: NextRequest) {
  const url = new URL(req.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const oauthError = url.searchParams.get("error");
  const env = getEnv();
  const base = env.APP_BASE_URL;

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

  if (!env.ORBIT_TOKEN_ENCRYPTION_KEY) {
    return NextResponse.redirect(
      `${base}/settings/connections?error=${encodeURIComponent("ORBIT_TOKEN_ENCRYPTION_KEY required before connecting")}`,
    );
  }

  const redirectUri =
    env.GOOGLE_REDIRECT_URI || `${env.APP_BASE_URL}/api/oauth/google/callback`;
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
    return NextResponse.redirect(
      `${base}/settings/connections?error=${encodeURIComponent("token_exchange_failed")}`,
    );
  }

  const channelRes = await fetch(
    "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
    { headers: { Authorization: `Bearer ${tokenBody.access_token}` } },
  );
  const channelBody = await channelRes.json();
  const channel = channelBody.items?.[0];
  const externalUserId = channel?.id || "unknown";

  const expiresAt = new Date(Date.now() + Number(tokenBody.expires_in || 3600) * 1000);
  // Prefer scopes Google actually returned — never assume force-ssl was granted.
  const actualScopes =
    typeof tokenBody.scope === "string" && tokenBody.scope.trim()
      ? tokenBody.scope.split(/\s+/).filter(Boolean)
      : YOUTUBE_SCOPES;
  const scopesJson = JSON.stringify(actualScopes);
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
      grantedScopes: scopesJson,
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
      grantedScopes: scopesJson,
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
