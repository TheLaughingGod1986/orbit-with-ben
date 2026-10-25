// Signed, expiring Play links for /api/watch (Ben, 25 Oct 2026: Play opens the cut with no board code).
// Same HMAC as scripts/kanban_snapshot.py sign_watch_url(): base64url(HMAC-SHA256(WATCH_LINK_SECRET, "<id>.<expiry>")).
import { createHmac, timingSafeEqual } from "node:crypto";

const MAX_AHEAD_S = 24 * 3600;   // a signature may not claim more than a day ahead

export function signWatch(secret, v, e) {
  return createHmac("sha256", secret).update(`${v}.${e}`).digest("base64url");
}

export function signedOk(v, e, s, secret, nowS = Math.floor(Date.now() / 1000)) {
  if (!secret || !/^\d{9,11}$/.test(String(e || "")) || !/^[A-Za-z0-9_-]{20,64}$/.test(String(s || ""))) return false;
  const exp = Number(e);
  if (exp <= nowS || exp > nowS + MAX_AHEAD_S) return false;
  const want = Buffer.from(signWatch(secret, v, exp));
  const got = Buffer.from(String(s));
  return want.length === got.length && timingSafeEqual(want, got);
}
