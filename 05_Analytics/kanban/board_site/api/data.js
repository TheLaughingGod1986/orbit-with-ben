// The board's data, read through the site's own server (J2532; docs/MULTI_CHANNEL_PLAN.md decision 8).
//
// Why. The pages used to read board.json, tracker.json and the MacBook's heartbeat straight from GitHub's public file
// addresses. The studio repo will be private (Ben, 10 Nov 2026), and from a private repo those addresses answer
// nothing. Here the server reads with its own token (env BOARD_GH_TOKEN, as api/checks.js) and hands the data on.
//
//   GET /api/data?f=ref                  which commit the board-data branch is on: {object: {sha}}
//   GET /api/data?f=board&sha=<commit>   board.json at that commit (it never changes, so it is kept for good)
//   GET /api/data?f=tracker&sha=<commit> tracker.json at that commit
//   GET /api/data?f=macbook              the MacBook worker's heartbeat.json (its own branch, read at most every 45 s)
//   without sha, board and tracker are read from the branch itself and held 45 s.
//
// Who may read. While the data's repo is public, anyone: the board works as it always has. Once it is private, only a
// signed-in viewer (Ben's cookie or his board key, benauth.js); everyone else gets 401 and the pages show the sign-in
// line. Without that rule the site would publish what the repo hides. "Public" is decided here, not by a setting that
// could be forgotten at the move: GitHub's public file address must answer for the board's own file with no token.
// If that cannot be confirmed the data is treated as private. BOARD_PRIVATE=1 forces private (to try it before the move).
//
// Cost. A copy is held in this function's memory (the branch's commit 20 s, a branch file 45 s, a file at a commit
// until the function sleeps), and a request that names the copy it already has gets 304 "not changed". GitHub sees at
// most 3 commit reads a minute from one running copy of this function, and one file read per new commit.
// A file is only ever read at the commit the branch is on now (or one already held): a request that names any other
// commit gets the current one, marked not to be kept. So nobody can spend the token's allowance by inventing commits.
//
// The repo is env BOARD_DATA_REPO (owner/name); until the move it is orbit-with-ben.
import { benAuth } from "../benauth.js";

export const DEFAULT_REPO = "TheLaughingGod1986/orbit-with-ben";
export const FILES = {
  ref: { branch: "board-data" },
  board: { branch: "board-data", path: "board.json", pinned: true },
  tracker: { branch: "board-data", path: "tracker.json", pinned: true },
  macbook: { branch: "macbook-heartbeat", path: "heartbeat.json" },
};
export const HOLD_S = { ref: 20, branch: 45, publicYes: 600, publicNo: 60 };
const SHA = /^[0-9a-f]{40}$/;
const KEEP_PINNED = 4;   // files at a commit kept in memory: the newest board and tracker, and the ones before

const held = new Map();  // key -> {at, etag, body, type}
let seen = { at: 0, open: false, repo: "" };

export function dataRepo(env = process.env) {
  const r = String(env.BOARD_DATA_REPO || "").trim();
  return /^[\w.-]+\/[\w.-]+$/.test(r) ? r : DEFAULT_REPO;
}

// For tests: forget everything held.
export function forget() { held.clear(); seen = { at: 0, open: false, repo: "" }; }

// Is the data's repo public? True only when GitHub's public file address answers for the board's own file, no token.
export async function repoIsPublic(env = process.env, now = Date.now()) {
  if (String(env.BOARD_PRIVATE || "").trim() === "1") return false;
  const repo = dataRepo(env);
  if (seen.repo === repo && now - seen.at < (seen.open ? HOLD_S.publicYes : HOLD_S.publicNo) * 1000) return seen.open;
  let open = false;
  try {
    const r = await fetch(`https://raw.githubusercontent.com/${repo}/${FILES.board.branch}/${FILES.board.path}`,
      { method: "HEAD", headers: { "user-agent": "studio-kanban" } });
    open = r.status === 200;
  } catch (e) { /* not confirmed: private */ }
  seen = { at: now, open, repo };
  return open;
}

// One GitHub read with the server's token. A token that cannot see this repo (today's can only comment) is dropped
// and the read is tried once more without it, which works while the repo is public.
async function github(url, accept, env) {
  const headers = { accept, "user-agent": "studio-kanban" };
  if (env.BOARD_GH_TOKEN) headers.authorization = `Bearer ${env.BOARD_GH_TOKEN}`;
  let r = await fetch(url, { headers });
  if (!r.ok && headers.authorization) {
    delete headers.authorization;
    r = await fetch(url, { headers });
  }
  return r;
}

async function readRef(repo, branch, env) {
  const r = await github(`https://api.github.com/repos/${repo}/git/ref/heads/${branch}`, "application/vnd.github+json", env);
  if (!r.ok) throw new Error(`GitHub ${r.status}`);
  const sha = (((await r.json()) || {}).object || {}).sha || "";
  if (!SHA.test(sha)) throw new Error("no sha");
  return { sha, body: JSON.stringify({ object: { sha } }), etag: `"${sha}"`, type: "application/json; charset=utf-8" };
}

async function readFile(repo, path, ref, env, open) {
  let r = await github(`https://api.github.com/repos/${repo}/contents/${path}?ref=${encodeURIComponent(ref)}`,
    "application/vnd.github.raw+json", env);
  if (!r.ok && open) r = await fetch(`https://raw.githubusercontent.com/${repo}/${ref}/${path}`, { headers: { "user-agent": "studio-kanban" } });
  if (!r.ok) throw new Error(`GitHub ${r.status}`);
  const body = await r.text();
  // Reject obvious error pages without parsing the large board file on the free Function CPU budget.
  if (!/^\s*[\[{]/.test(body)) throw new Error("GitHub answered with something that is not the file");
  return { body, etag: `"${SHA.test(ref) ? ref : "b"}-${path}-${body.length}"`, type: "application/json; charset=utf-8" };
}

async function holdFor(key, seconds, now, load) {
  const have = held.get(key);
  if (have && (seconds === Infinity || now - have.at < seconds * 1000)) return have;
  const got = await load();
  held.delete(key);
  held.set(key, { at: now, ...got });
  const pinned = [...held.keys()].filter(k => k.startsWith("at:"));
  for (const k of pinned.slice(0, Math.max(0, pinned.length - KEEP_PINNED))) held.delete(k);
  return held.get(key);
}

function cacheHeader(open, kind) {
  if (kind === "pinned") return open ? "public, max-age=31536000, s-maxage=300, immutable" : "private, max-age=31536000, immutable";
  const s = kind === "ref" ? HOLD_S.ref : HOLD_S.branch;
  return open ? `public, max-age=0, s-maxage=${s}, stale-while-revalidate=${2 * s}` : `private, max-age=${s}`;
}

export default async function handler(req, res) {
  const env = process.env, q = req.query || {};
  if (req.method !== "GET" && req.method !== "HEAD") return res.status(405).json({ error: "GET only" });
  const f = String(q.f || ""), file = Object.prototype.hasOwnProperty.call(FILES, f) ? FILES[f] : null;
  const sha = String(q.sha || "");
  if (!file) return res.status(400).json({ error: "f must be one of " + Object.keys(FILES).join(", ") });
  if (sha && (!file.pinned || !SHA.test(sha))) return res.status(400).json({ error: "sha must be a 40-character commit, for board or tracker" });
  let open = false;
  try {
    open = await repoIsPublic(env);
    if (!open && !benAuth(req, env)) {
      res.setHeader("Cache-Control", "no-store");
      return res.status(401).json({ error: "sign in", signIn: true });
    }
    const repo = dataRepo(env), now = Date.now();
    const at = c => `at:${repo}:${c}:${file.path}`;
    let got, kind = f === "ref" ? "ref" : sha ? "pinned" : "branch";
    if (f === "ref") got = await holdFor(`ref:${repo}`, HOLD_S.ref, now, () => readRef(repo, file.branch, env));
    else if (!sha) got = await holdFor(`branch:${repo}:${file.branch}:${file.path}`, HOLD_S.branch, now, () => readFile(repo, file.path, file.branch, env, open));
    else {
      let commit = sha;
      if (!held.has(at(sha))) {
        const head = (await holdFor(`ref:${repo}`, HOLD_S.ref, now, () => readRef(repo, file.branch, env))).sha;
        if (head !== sha) { commit = head; kind = "moved"; }   // not the commit the branch is on: serve the one it is on
      }
      got = await holdFor(at(commit), Infinity, now, () => readFile(repo, file.path, commit, env, open));
      res.setHeader("X-Board-Sha", commit);
    }
    res.setHeader("Cache-Control", kind === "moved" ? "no-store" : cacheHeader(open, kind));
    if (!open) res.setHeader("Vary", "Cookie, x-board-key");
    res.setHeader("ETag", got.etag);
    if (String((req.headers || {})["if-none-match"] || "") === got.etag) return res.status(304).end();
    res.setHeader("Content-Type", got.type);
    return res.status(200).send(req.method === "HEAD" ? "" : got.body);
  } catch (e) {
    res.setHeader("Cache-Control", "no-store");
    return res.status(502).json({ error: String((e && e.message) || "GitHub unreachable").slice(0, 80) });
  }
}
