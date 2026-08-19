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
  if (!code || !state) return NextResponse.redirect(`${base}/settings/connections?error=missing_code`);
  const consumed = await consumeOAuthState({ platform: "x", state });
  if (!consumed.ok || !consumed.codeVerifier) {
    return NextResponse.redirect(`${base}/settings/connections?error=invalid_state`);
  }
  if (!env.ORBIT_TOKEN_ENCRYPTION_KEY) {
    return NextResponse.redirect(`${base}/settings/connections?error=encryption_key_required`);
  }

  const redirectUri = oauthCallbackUrl("x", req);
  const basic = Buffer.from(`${env.X_CLIENT_ID}:${env.X_CLIENT_SECRET}`).toString("base64");
  const tokenRes = await fetch("https://api.twitter.com/2/oauth2/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Basic ${basic}`,
    },
    body: new URLSearchParams({
      code,
      grant_type: "authorization_code",
      redirect_uri: redirectUri,
      code_verifier: consumed.codeVerifier,
    }),
  });
  const tokenBody = await tokenRes.json();
  if (!tokenRes.ok || !tokenBody.access_token) {
    return NextResponse.redirect(`${base}/settings/connections?error=token_exchange_failed`);
  }

  const meRes = await fetch("https://api.x.com/2/users/me", {
    headers: { Authorization: `Bearer ${tokenBody.access_token}` },
  });
  const meBody = await meRes.json();
  const user = meBody.data;
  const externalUserId = String(user?.id || "unknown");

  await prisma.platformConnection.upsert({
    where: { platform_externalUserId: { platform: "x", externalUserId } },
    create: {
      platform: "x",
      externalUserId,
      accountId: user?.id,
      accountName: user?.name,
      accountUsername: user?.username,
      accountType: "x_user",
      profileUrl: user?.username ? `https://x.com/${user.username}` : null,
      connectionStatus: "connected",
      grantedScopes: JSON.stringify(String(tokenBody.scope || "").split(" ").filter(Boolean)),
      accessTokenEncrypted: encryptSecret(tokenBody.access_token),
      refreshTokenEncrypted: tokenBody.refresh_token
        ? encryptSecret(tokenBody.refresh_token)
        : null,
      accessTokenExpiresAt: new Date(Date.now() + Number(tokenBody.expires_in || 7200) * 1000),
      lastValidatedAt: new Date(),
    },
    update: {
      accountName: user?.name,
      accountUsername: user?.username,
      connectionStatus: "connected",
      grantedScopes: JSON.stringify(String(tokenBody.scope || "").split(" ").filter(Boolean)),
      accessTokenEncrypted: encryptSecret(tokenBody.access_token),
      refreshTokenEncrypted: tokenBody.refresh_token
        ? encryptSecret(tokenBody.refresh_token)
        : undefined,
      lastValidatedAt: new Date(),
      disconnectedAt: null,
    },
  });

  return NextResponse.redirect(`${base}/settings/connections?connected=x`);
}
