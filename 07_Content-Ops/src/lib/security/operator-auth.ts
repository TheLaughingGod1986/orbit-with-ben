import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

export const OPERATOR_COOKIE = "orbit_ops_auth";
const COOKIE_MAX_AGE_SEC = 60 * 60 * 24 * 14; // 14 days

function operatorPassword(): string | null {
  const raw = process.env.CONTENT_OPS_OPERATOR_PASSWORD?.trim();
  return raw || null;
}

function signingSecret(): string | null {
  const password = operatorPassword();
  if (!password) return null;
  const pepper = process.env.ORBIT_TOKEN_ENCRYPTION_KEY?.trim() || "orbit-content-ops";
  return `${password}:${pepper}`;
}

/** Edge + Node compatible HMAC-SHA256 hex (Web Crypto). */
async function hmacSha256Hex(secret: string, message: string): Promise<string> {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(message));
  return Array.from(new Uint8Array(sig), (b) => b.toString(16).padStart(2, "0")).join("");
}

function timingSafeEqualHex(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let out = 0;
  for (let i = 0; i < a.length; i += 1) out |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return out === 0;
}

async function expectedToken(): Promise<string | null> {
  const secret = signingSecret();
  if (!secret) return null;
  return hmacSha256Hex(secret, "orbit-ops-session-v1");
}

/** True when CONTENT_OPS_OPERATOR_PASSWORD is set on this deploy. */
export function isOperatorPasswordConfigured(): boolean {
  return Boolean(operatorPassword());
}

export async function verifyOperatorPassword(candidate: string): Promise<boolean> {
  const expected = operatorPassword();
  if (!expected) return false;
  // Constant-time-ish compare via HMAC of both sides.
  const [a, b] = await Promise.all([
    hmacSha256Hex("orbit-password-check", candidate),
    hmacSha256Hex("orbit-password-check", expected),
  ]);
  return timingSafeEqualHex(a, b);
}

export function readOperatorTokenFromCookieHeader(cookieHeader: string | null): string | null {
  if (!cookieHeader) return null;
  const parts = cookieHeader.split(/;\s*/);
  for (const part of parts) {
    const eq = part.indexOf("=");
    if (eq === -1) continue;
    const name = part.slice(0, eq).trim();
    if (name !== OPERATOR_COOKIE) continue;
    return decodeURIComponent(part.slice(eq + 1).trim());
  }
  return null;
}

export async function isOperatorTokenValid(token: string | null | undefined): Promise<boolean> {
  const expected = await expectedToken();
  if (!expected || !token) return false;
  return timingSafeEqualHex(token, expected);
}

export async function isOperatorRequestAuthenticated(request: NextRequest): Promise<boolean> {
  const token =
    request.cookies.get(OPERATOR_COOKIE)?.value ??
    readOperatorTokenFromCookieHeader(request.headers.get("cookie"));
  return isOperatorTokenValid(token);
}

/** Server Components / Server Actions — reads Next cookies(). */
export async function isOperatorAuthenticated(): Promise<boolean> {
  if (!isOperatorPasswordConfigured()) return false;
  const jar = await cookies();
  return isOperatorTokenValid(jar.get(OPERATOR_COOKIE)?.value);
}

export async function setOperatorSessionCookie(): Promise<void> {
  const token = await expectedToken();
  if (!token) {
    throw new Error("CONTENT_OPS_OPERATOR_PASSWORD is not configured");
  }
  const jar = await cookies();
  jar.set(OPERATOR_COOKIE, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge: COOKIE_MAX_AGE_SEC,
  });
}

export async function clearOperatorSessionCookie(): Promise<void> {
  const jar = await cookies();
  jar.delete(OPERATOR_COOKIE);
}

/**
 * Fail closed: mutating work requires a valid operator session.
 * Throws Error with message starting "Unauthorized" for UI/API handling.
 */
export async function requireOperator(): Promise<void> {
  if (!isOperatorPasswordConfigured()) {
    throw new Error(
      "Unauthorized: CONTENT_OPS_OPERATOR_PASSWORD is not configured on this deploy",
    );
  }
  if (!(await isOperatorAuthenticated())) {
    throw new Error("Unauthorized: operator sign-in required");
  }
}

/** Route-handler gate: returns 401 response, or null when the operator may proceed. */
export async function requireOperatorApi(): Promise<NextResponse | null> {
  try {
    await requireOperator();
    return null;
  } catch {
    return unauthorizedJson();
  }
}

export function unauthorizedJson(): NextResponse {
  return NextResponse.json(
    { error: "Unauthorized: operator sign-in required" },
    { status: 401 },
  );
}

/**
 * Safe post-login redirect. Single leading slash only — rejects `//evil.com`
 * and absolute URLs (open redirect).
 */
export function safeOperatorNextPath(raw: string | null | undefined): string {
  const next = String(raw || "/").trim();
  if (/^\/(?!\/)/.test(next)) return next;
  return "/";
}

/** Paths that must stay public (affiliate clicks, legal). */
export function isPublicPath(pathname: string): boolean {
  if (pathname === "/login") return true;
  if (pathname.startsWith("/legal")) return true;
  if (pathname.startsWith("/go/")) return true;
  if (pathname.startsWith("/_next")) return true;
  if (pathname === "/favicon.ico") return true;
  return false;
}

/** Mutating API / OAuth token flows that require an operator session. */
export function isMutatingApiPath(method: string, pathname: string): boolean {
  if (pathname.startsWith("/go/")) return false;
  if (!pathname.startsWith("/api/")) return false;

  const upper = method.toUpperCase();
  if (pathname.match(/^\/api\/oauth\/[^/]+\/start$/)) return true;
  if (pathname.match(/^\/api\/oauth\/[^/]+\/callback$/)) return true;
  if (["POST", "PUT", "PATCH", "DELETE"].includes(upper)) return true;
  return false;
}
