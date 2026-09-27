import { NextRequest, NextResponse } from "next/server";
import { getEnv, hasMetaOAuth } from "@/lib/env";
import { oauthCallbackUrl } from "@/lib/public-base-url";
import { createOAuthState } from "@/lib/oauth/state";
import { requireOperatorApi } from "@/lib/security/operator-auth";

const META_SCOPES = [
  "pages_show_list",
  "pages_read_engagement",
  "pages_manage_posts",
  "instagram_basic",
  "instagram_content_publish",
  "business_management",
].join(",");

export async function GET(req: NextRequest) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  if (!hasMetaOAuth()) {
    return NextResponse.json({ error: "META_APP_ID / META_APP_SECRET not configured" }, { status: 400 });
  }
  const env = getEnv();
  const redirectUri = oauthCallbackUrl("meta", req);
  const { state } = await createOAuthState({ platform: "meta", redirectPath: "/settings/connections" });
  const url = new URL("https://www.facebook.com/v21.0/dialog/oauth");
  url.searchParams.set("client_id", env.META_APP_ID!);
  url.searchParams.set("redirect_uri", redirectUri);
  url.searchParams.set("state", state);
  url.searchParams.set("scope", META_SCOPES);
  return NextResponse.redirect(url.toString());
}
