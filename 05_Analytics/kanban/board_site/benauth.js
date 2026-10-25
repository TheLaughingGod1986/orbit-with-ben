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
// has neither; since 25 Oct 13:34 their taps are accepted as "open" taps unless BOARD_OPEN_TAPS=0 (see the end of this file).
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

// ---- open taps (Ben, 25 Oct 2026 13:34: "I should just be able to click add comment, sent to agent or approve
// without this confirmation"). With env BOARD_OPEN_TAPS unset or "1" (the default), a tap from a browser with no
// studio_ben cookie (a Home Screen copy, the Gmail in-app browser, a new phone) is accepted: no dialog, no linking
// step. That browser is given the 400-day cookie on the same response (and on its next board load), and the post plus
// the #219 audit list say "new device" with a short device name and a hashed IP, so a stray tap is easy to spot and undo.
// Guards: same-origin only (Origin / Referer must be this board), at most OPEN_TAPS_PER_HOUR unlinked taps an hour.
// To lock the board again: set BOARD_OPEN_TAPS=0 in Vercel and redeploy; unlinked taps then get 401 as before.
export const OPEN_TAPS_PER_HOUR = 20;
export function openTaps(env = process.env) { return String(env.BOARD_OPEN_TAPS ?? "1").trim() !== "0"; }

export function sameOrigin(req) {
  const h = req.headers || {}, host = String(h["x-forwarded-host"] || h.host || "").toLowerCase();
  const src = String(h.origin || h.referer || "");
  if (!host || !src) return false;
  try { return new URL(src).host.toLowerCase() === host; } catch (e) { return false; }
}

// Short, readable device name from the user agent ("iPhone Safari", "iPhone Gmail app", "Mac Chrome", …).
export function deviceName(ua) {
  const u = String(ua || "");
  const os = /iPhone/.test(u) ? "iPhone" : /iPad/.test(u) ? "iPad" : /Android/.test(u) ? "Android"
    : /Macintosh|Mac OS X/.test(u) ? "Mac" : /Windows/.test(u) ? "Windows" : /Linux/.test(u) ? "Linux" : "unknown device";
  const app = /GSA\//.test(u) ? "Google app" : /Gmail|GoogleMail/i.test(u) ? "Gmail app" : /CriOS|Chrome\//.test(u) ? "Chrome"
    : /FxiOS|Firefox\//.test(u) ? "Firefox" : /EdgiOS|Edg\//.test(u) ? "Edge"
    : /Version\/[\d.]+.*Safari\//.test(u) ? "Safari" : /AppleWebKit/.test(u) && /Mobile\//.test(u) ? "web app / in-app browser" : "browser";
  return `${os} ${app}`;
}

// The repo is public, so the IP is never written in clear: first 10 chars of HMAC(BOARD_KEY, ip).
export function clientIp(req) {
  const h = req.headers || {};
  return String(h["x-real-ip"] || String(h["x-forwarded-for"] || "").split(",")[0] || "").trim();
}
export function ipTag(ip, boardKey) {
  return ip ? "ip#" + createHmac("sha256", String(boardKey || "studio")).update("ip-v1:" + ip).digest("hex").slice(0, 10) : "ip#unknown";
}

// Ben's request? Like benAuth, but when open taps are on, a same-origin request without the cookie counts as "open".
export function tapAuth(req, env = process.env) {
  const how = benAuth(req, env);
  if (how) return how;
  return openTaps(env) && sameOrigin(req) ? "open" : "";
}

// Give a browser the cookie: renew for cookie/key, first issue for "open".
export function setBenCookie(res, req, how, env = process.env) {
  if (!how || !env.BOARD_KEY) return;
  if (how === "open") return res.setHeader("Set-Cookie", cookieHeader(makeSession(env.BOARD_KEY)));
  return renewCookie(res, req, how, env);
}
