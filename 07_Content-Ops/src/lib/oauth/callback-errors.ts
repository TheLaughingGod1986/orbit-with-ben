import { validateEncryptionKey } from "@/lib/security/token-crypto";

/**
 * Stable error codes carried on `/settings/connections?error=<code>` so a failed
 * Connect says what broke instead of leaving the card on "not connected".
 */
export const OAUTH_ERROR_MESSAGES: Record<string, string> = {
  missing_code: "The provider returned no authorization code. Click Connect again.",
  invalid_state:
    "OAuth state token not recognised. Click Connect again — do not reopen an old callback URL.",
  state_platform_mismatch:
    "OAuth state belongs to a different platform. Click Connect on the card you want.",
  state_already_used: "This callback link was already used. Click Connect again.",
  state_expired: "The Connect link expired (10 minutes). Click Connect again.",
  missing_code_verifier:
    "The PKCE verifier for this Connect attempt was lost. Click Connect again.",
  encryption_key_required:
    "ORBIT_TOKEN_ENCRYPTION_KEY is not set on this deploy, so tokens cannot be stored. Add it and redeploy.",
  encryption_key_invalid:
    "ORBIT_TOKEN_ENCRYPTION_KEY must be 32 bytes base64 (openssl rand -base64 32).",
  token_exchange_failed:
    "The provider rejected the code exchange. Check the client id/secret and that the redirect URI registered with the provider matches this deploy exactly. Server logs hold the provider response.",
  connection_save_failed:
    "Tokens arrived but could not be saved. Check the database and encryption key, then reconnect.",
  access_denied: "Permission was declined at the provider. Click Connect again and accept all scopes.",
};

/** Human sentence for a redirect error code; unknown codes pass through as-is. */
export function describeOAuthError(raw: string): string {
  return OAUTH_ERROR_MESSAGES[raw] || raw;
}

/** Encryption-key readiness, checked before a token exchange so failures are visible. */
export function encryptionKeyErrorCode():
  | "encryption_key_required"
  | "encryption_key_invalid"
  | null {
  const raw = process.env.ORBIT_TOKEN_ENCRYPTION_KEY;
  if (!raw || !raw.trim()) return "encryption_key_required";
  try {
    validateEncryptionKey(raw);
    return null;
  } catch {
    return "encryption_key_invalid";
  }
}
