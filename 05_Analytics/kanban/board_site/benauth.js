// Ben's buttons with no code to type (Ben, 25 Oct 2026: "Just need to approve no need for code").
//
// Before: Approve / Request changes sent the board code (env BOARD_KEY) from the phone's localStorage, saved from a
// #k= link. Safari wipes script-written storage (ITP, 7 days without a visit) and a Home Screen copy has its own, so
// the code went missing and the page asked Ben to paste it.
//
// Now: the phone holds a long-lived, HttpOnly session cookie ("studio_ben", 400 days, renewed on every board load) that
// script can't read and ITP doesn't cap. It's set once by either
//   - a one-time "link this phone" link, /api/pair?n=<nonce>&e=<unix expiry>&s=<sig>, minted on the Mac mini by
//     scripts/board_pair_link.py: sig = base64url(HMAC-SHA256(HMAC-SHA256(WATCH_LINK_SECRET, "studio-pair-v1"),
//     "<n>.<e>")). Each nonce works once (recorded in the #219 store) and the link expires within 7 days; or
//   - any request that still carries the old board code (x-board-key), so a phone that has it upgrades silently.
// The cookie is "v1.<issued unix>.<HMAC-SHA256(HMAC-SHA256(BOARD_KEY, "studio-session-v1"), "v1.<issued>")>":
// nothing secret in it, and rotating BOARD_KEY in Vercel logs every phone out. An anonymous visitor to the public board
// has neither, so their taps get 401 and post nothing.
import { createHmac, timingSafeEqual } from "node:crypto";

export const COOKIE = "studio_ben";
export const COOKIE_MAX_AGE_S = 400 * 86400;     // the longest any browser keeps a cookie; renewed on each load
export const PAIR_MAX_AHEAD_S = 7 * 86400;

const b64 = (key, msg) => createHmac("sha256", key).update(msg).digest("base64url");
const same = (a, b) => { const x = Buffer.from(String(a)), y = Buffer.from(String(b)); return x.length === y.length && timingSafeEqual(x, y); };

export function keyOk(given, ...keys) {
  return !!given && keys.some(k => !!k && same(given, k));
}

// ---- one-time pairing links
export function pairKey(watchSecret) { return createHmac("sha256", watchSecret).update("studio-pair-v1").digest(); }
export function signPair(watchSecret, n, e) { return b64(pairKey(watchSecret), `${n}.${e}`); }
export function pairOk(n, e, s, watchSecret, nowS = Math.floor(Date.now() / 1000)) {
  if (!watchSecret || !/^[A-Za-z0-9_-]{16,64}$/.test(String(n || "")) || !/^\d{9,11}$/.test(String(e || ""))
      || !/^[A-Za-z0-9_-]{20,64}$/.test(String(s || ""))) return false;
  const exp = Number(e);
  if (exp <= nowS || exp > nowS + PAIR_MAX_AHEAD_S) return false;
  return same(signPair(watchSecret, n, exp), s);
}

// ---- session cookie
function sessionKey(boardKey) { return createHmac("sha256", boardKey).update("studio-session-v1").digest(); }
export function makeSession(boardKey, nowS = Math.floor(Date.now() / 1000)) {
  const body = `v1.${nowS}`;
  return `${body}.${b64(sessionKey(boardKey), body)}`;
}
export function sessionValid(value, boardKey) {
  const m = /^v1\.(\d{9,11})\.([A-Za-z0-9_-]{20,64})$/.exec(String(value || ""));
  return !!(boardKey && m && same(b64(sessionKey(boardKey), `v1.${m[1]}`), m[2]));
}
export function readCookie(req, name = COOKIE) {
  const raw = String((req.headers && req.headers.cookie) || "");
  for (const part of raw.split(/;\s*/)) {
    const i = part.indexOf("=");
    if (i > 0 && part.slice(0, i) === name) return decodeURIComponent(part.slice(i + 1));
  }
  return "";
}
export function cookieHeader(value, maxAge = COOKIE_MAX_AGE_S) {
  return `${COOKIE}=${value}; Path=/; Max-Age=${maxAge}; HttpOnly; Secure; SameSite=Lax`;
}

// Is this request Ben's? Cookie first, then the old board code header. Returns "cookie", "key" or "".
export function benAuth(req, env = process.env) {
  if (sessionValid(readCookie(req), env.BOARD_KEY)) return "cookie";
  if (keyOk(req.headers && req.headers["x-board-key"], env.BOARD_KEY)) return "key";
  return "";
}

// Renew (or first set) the cookie on any request that proved it's Ben. Keeps the original issue time.
export function renewCookie(res, req, how, env = process.env) {
  if (!how || !env.BOARD_KEY) return;
  const cur = readCookie(req);
  res.setHeader("Set-Cookie", cookieHeader(how === "cookie" && sessionValid(cur, env.BOARD_KEY) ? cur : makeSession(env.BOARD_KEY)));
}
