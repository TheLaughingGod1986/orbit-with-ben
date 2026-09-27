import { NextRequest, NextResponse } from "next/server";
import { getEnv, hasGoogleOAuth } from "@/lib/env";
import { oauthCallbackUrl } from "@/lib/public-base-url";
import { createOAuthState } from "@/lib/oauth/state";
import { YOUTUBE_SCOPES } from "@/lib/publishing/adapters/youtube";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export async function GET(req: NextRequest) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  if (!hasGoogleOAuth()) {
    return NextResponse.json(
      { error: "GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET not configured" },
      { status: 400 },
    );
  }
  const env = getEnv();
  const redirectUri = oauthCallbackUrl("google", req);
  const { state } = await createOAuthState({
    platform: "youtube_shorts",
    redirectPath: "/settings/connections",
  });
  const url = new URL("https://accounts.google.com/o/oauth2/v2/auth");
  url.searchParams.set("client_id", env.GOOGLE_CLIENT_ID!);
  url.searchParams.set("redirect_uri", redirectUri);
  url.searchParams.set("response_type", "code");
  url.searchParams.set("scope", YOUTUBE_SCOPES.join(" "));
  url.searchParams.set("access_type", "offline");
  url.searchParams.set("include_granted_scopes", "true");
  url.searchParams.set("prompt", "consent");
  url.searchParams.set("state", state);
  return NextResponse.redirect(url.toString());
}
