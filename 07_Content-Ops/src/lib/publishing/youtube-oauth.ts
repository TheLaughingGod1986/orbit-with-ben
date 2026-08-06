/**
 * YouTube OAuth scope helpers — never log tokens.
 */
import { getEnv } from "@/lib/env";

export const YT_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload";
export const YT_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly";
export const YT_FORCE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl";

export const REQUIRED_YOUTUBE_SCOPES = [
  YT_UPLOAD_SCOPE,
  YT_READONLY_SCOPE,
  YT_FORCE_SSL_SCOPE,
] as const;

export type OAuthFailureKind =
  | "missing_scope"
  | "expired_token"
  | "revoked_token"
  | "invalid_client"
  | "no_connection"
  | "network"
  | "unknown";

export function parseGrantedScopes(raw: string | null | undefined): string[] {
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) return parsed.map(String);
  } catch {
    /* space-delimited fallback */
  }
  return raw.split(/[\s,]+/).map((s) => s.trim()).filter(Boolean);
}

export function hasForceSslScope(scopes: string[]): boolean {
  return scopes.some((s) => s.includes("youtube.force-ssl"));
}

export function missingRequiredScopes(scopes: string[]): string[] {
  return REQUIRED_YOUTUBE_SCOPES.filter(
    (req) => !scopes.some((s) => s === req || s.includes(req.split("/").pop() || req)),
  );
}

export function classifyOAuthHttpError(status: number, bodyText: string): OAuthFailureKind {
  const lower = bodyText.toLowerCase();
  if (status === 401) {
    if (lower.includes("revoked")) return "revoked_token";
    return "expired_token";
  }
  if (status === 403) {
    if (lower.includes("access_token_scope_insufficient") || lower.includes("insufficient")) {
      return "missing_scope";
    }
    if (lower.includes("revoked")) return "revoked_token";
  }
  if (status === 400 && (lower.includes("invalid_client") || lower.includes("unauthorized_client"))) {
    return "invalid_client";
  }
  return "unknown";
}

/** Build Google consent URL for YouTube reconnect (force-ssl included). */
export function buildYouTubeOAuthAuthorizationUrl(input: {
  state: string;
  redirectUri?: string;
  scopes?: readonly string[];
}): string {
  const env = getEnv();
  if (!env.GOOGLE_CLIENT_ID) {
    throw new Error("GOOGLE_CLIENT_ID is not configured");
  }
  const redirectUri =
    input.redirectUri ||
    env.GOOGLE_REDIRECT_URI ||
    `${env.APP_BASE_URL}/api/oauth/google/callback`;
  const scopes = input.scopes || REQUIRED_YOUTUBE_SCOPES;
  const url = new URL("https://accounts.google.com/o/oauth2/v2/auth");
  url.searchParams.set("client_id", env.GOOGLE_CLIENT_ID);
  url.searchParams.set("redirect_uri", redirectUri);
  url.searchParams.set("response_type", "code");
  url.searchParams.set("scope", scopes.join(" "));
  url.searchParams.set("access_type", "offline");
  url.searchParams.set("include_granted_scopes", "true");
  url.searchParams.set("prompt", "consent");
  url.searchParams.set("state", input.state);
  return url.toString();
}

export function scopesFromTokenResponse(scopeField: unknown): string[] {
  if (typeof scopeField === "string" && scopeField.trim()) {
    return scopeField.split(/\s+/).filter(Boolean);
  }
  return [];
}
