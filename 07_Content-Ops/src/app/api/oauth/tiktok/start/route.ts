import { NextRequest, NextResponse } from "next/server";
import { getEnv, hasTikTokOAuth } from "@/lib/env";
import { oauthCallbackUrl } from "@/lib/public-base-url";
import { createOAuthState } from "@/lib/oauth/state";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export async function GET(req: NextRequest) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  if (!hasTikTokOAuth()) {
    return NextResponse.json({ error: "TikTok OAuth not configured" }, { status: 400 });
  }
  const env = getEnv();
  const redirectUri = oauthCallbackUrl("tiktok", req);
  const { state, codeChallenge } = await createOAuthState({
    platform: "tiktok",
    withPkce: true,
  });
  const url = new URL("https://www.tiktok.com/v2/auth/authorize/");
  url.searchParams.set("client_key", env.TIKTOK_CLIENT_KEY!);
  url.searchParams.set("response_type", "code");
  url.searchParams.set("scope", "user.info.basic,video.upload,video.publish");
  url.searchParams.set("redirect_uri", redirectUri);
  url.searchParams.set("state", state);
  if (codeChallenge) {
    url.searchParams.set("code_challenge", codeChallenge);
    url.searchParams.set("code_challenge_method", "S256");
  }
  return NextResponse.redirect(url.toString());
}
