import { NextRequest, NextResponse } from "next/server";
import { getEnv, hasXOAuth } from "@/lib/env";
import { oauthCallbackUrl } from "@/lib/public-base-url";
import { createOAuthState } from "@/lib/oauth/state";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export async function GET(req: NextRequest) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  if (!hasXOAuth()) {
    return NextResponse.json({ error: "X OAuth not configured" }, { status: 400 });
  }
  const env = getEnv();
  const redirectUri = oauthCallbackUrl("x", req);
  const { state, codeChallenge } = await createOAuthState({
    platform: "x",
    withPkce: true,
  });
  const url = new URL("https://twitter.com/i/oauth2/authorize");
  url.searchParams.set("response_type", "code");
  url.searchParams.set("client_id", env.X_CLIENT_ID!);
  url.searchParams.set("redirect_uri", redirectUri);
  url.searchParams.set("scope", "tweet.read tweet.write users.read offline.access");
  url.searchParams.set("state", state);
  url.searchParams.set("code_challenge", codeChallenge!);
  url.searchParams.set("code_challenge_method", "S256");
  return NextResponse.redirect(url.toString());
}
