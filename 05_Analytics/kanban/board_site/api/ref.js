// Which commit the board-data branch is on, for every page's once-a-minute data check (Ben, 29 Oct 2026 dashboard
// audit). The pages used to ask api.github.com themselves: unauthenticated, that is 60 requests an hour per IP, so a
// phone with the hub, /board and /ai open ran out within the hour (403 "rate limit exceeded") and fell back to the
// branch URL, which raw.githubusercontent serves up to 5 minutes stale. Here one authenticated read (env
// BOARD_GH_TOKEN, as api/checks.js) serves every viewer, and Vercel's edge cache holds the answer for 20 s, so GitHub
// sees at most a few calls a minute however many pages are open. Same shape as GitHub's ref ({object: {sha}}), so the
// pages read it unchanged and fall back to api.github.com if this fails.

const REF = "https://api.github.com/repos/TheLaughingGod1986/orbit-with-ben/git/ref/heads/board-data";

export default async function handler(req, res) {
  const headers = { accept: "application/vnd.github+json", "user-agent": "studio-kanban" };
  if (process.env.BOARD_GH_TOKEN) headers.authorization = `Bearer ${process.env.BOARD_GH_TOKEN}`;
  try {
    let r = await fetch(REF, { headers });
    if (!r.ok && headers.authorization) {  // a token without access to this repo: the public read still works
      delete headers.authorization;
      r = await fetch(REF, { headers });
    }
    if (!r.ok) return res.status(502).json({ error: `GitHub ${r.status}` });
    const sha = (((await r.json()) || {}).object || {}).sha || "";
    if (!/^[0-9a-f]{40}$/.test(sha)) return res.status(502).json({ error: "no sha" });
    res.setHeader("Cache-Control", "public, s-maxage=20, stale-while-revalidate=40");
    return res.status(200).json({ object: { sha } });
  } catch (e) {
    return res.status(502).json({ error: "GitHub unreachable" });
  }
}
