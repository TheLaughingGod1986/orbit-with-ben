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
  const consumed = await consumeOAuthState({ platform: "tiktok", state });
  if (!consumed.ok) {
    return NextResponse.redirect(`${base}/settings/connections?error=${encodeURIComponent(consumed.error)}`);
  }
  if (!env.ORBIT_TOKEN_ENCRYPTION_KEY) {
    return NextResponse.redirect(`${base}/settings/connections?error=encryption_key_required`);
  }

  const redirectUri = oauthCallbackUrl("tiktok", req);
  const tokenRes = await fetch("https://open.tiktokapis.com/v2/oauth/token/", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_key: env.TIKTOK_CLIENT_KEY!,
      client_secret: env.TIKTOK_CLIENT_SECRET!,
      code,
      grant_type: "authorization_code",
      redirect_uri: redirectUri,
      ...(consumed.codeVerifier ? { code_verifier: consumed.codeVerifier } : {}),
    }),
  });
  const tokenBody = await tokenRes.json();
  const access = tokenBody.access_token || tokenBody?.data?.access_token;
  const openId = tokenBody.open_id || tokenBody?.data?.open_id || "unknown";
  const refresh = tokenBody.refresh_token || tokenBody?.data?.refresh_token;
  const scope = tokenBody.scope || tokenBody?.data?.scope || "";
  if (!tokenRes.ok || !access) {
    return NextResponse.redirect(`${base}/settings/connections?error=token_exchange_failed`);
  }

  // Fetch basic profile for display + Orbit profile URL
  let accountName: string | null = "OrbitWithBen";
  let accountUsername: string | null = "orbitwithben";
  let profileUrl: string | null = "https://www.tiktok.com/@orbitwithben";
  try {
    const userRes = await fetch(
      "https://open.tiktokapis.com/v2/user/info/?fields=open_id,union_id,avatar_url,display_name,username",
      { headers: { Authorization: `Bearer ${access}` } },
    );
    if (userRes.ok) {
      const userBody = await userRes.json();
      const user = userBody?.data?.user || userBody?.user || userBody?.data || {};
      if (user.display_name) accountName = String(user.display_name);
      if (user.username) {
        accountUsername = String(user.username).replace(/^@/, "");
        profileUrl = `https://www.tiktok.com/@${accountUsername}`;
      }
    }
  } catch {
    // Keep Orbit defaults when user.info is unavailable
  }

  await prisma.platformConnection.upsert({
    where: { platform_externalUserId: { platform: "tiktok", externalUserId: String(openId) } },
    create: {
      platform: "tiktok",
      externalUserId: String(openId),
      accountId: String(openId),
      accountType: "tiktok_user",
      accountName,
      accountUsername,
      profileUrl,
      connectionStatus: "connected",
      grantedScopes: JSON.stringify(String(scope).split(",").filter(Boolean)),
      accessTokenEncrypted: encryptSecret(access),
      refreshTokenEncrypted: refresh ? encryptSecret(refresh) : null,
      accessTokenExpiresAt: new Date(Date.now() + Number(tokenBody.expires_in || 86400) * 1000),
      lastValidatedAt: new Date(),
    },
    update: {
      connectionStatus: "connected",
      accountName,
      accountUsername,
      profileUrl,
      grantedScopes: JSON.stringify(String(scope).split(",").filter(Boolean)),
      accessTokenEncrypted: encryptSecret(access),
      refreshTokenEncrypted: refresh ? encryptSecret(refresh) : undefined,
      lastValidatedAt: new Date(),
      disconnectedAt: null,
    },
  });

  await prisma.platformSettings.upsert({
    where: { platform: "tiktok" },
    create: {
      platform: "tiktok",
      enabled: true,
      accountDisplayName: accountName || "OrbitWithBen",
      profileUrl: profileUrl || "https://www.tiktok.com/@orbitwithben",
      defaultHashtags: JSON.stringify(["OrbitWithBen", "Space", "Astronomy"]),
      defaultCallToAction: "Watch the full story on Orbit with Ben.",
      publishingMethod: "api",
      connectionStatus: "connected",
      tokenStatus: "valid",
      defaultVisibility: "public",
    },
    update: {
      accountDisplayName: accountName || "OrbitWithBen",
      profileUrl: profileUrl || "https://www.tiktok.com/@orbitwithben",
      publishingMethod: "api",
      connectionStatus: "connected",
      tokenStatus: "valid",
    },
  });

  return NextResponse.redirect(`${base}/settings/connections?connected=tiktok`);
}
