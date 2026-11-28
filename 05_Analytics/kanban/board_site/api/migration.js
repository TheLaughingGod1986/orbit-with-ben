// J3012: temporary, opt-in access check in the actual board runtime.
// No caller-selected repository, ref or path; no private content leaves this handler.
import { benAuth } from "../benauth.js";

const REPO = "TheLaughingGod1986/studio";
const REF = "rehearsal/j3012";
const SHA = /^[0-9a-f]{40}$/;

export default async function handler(req, res, env = process.env) {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("Vary", "Cookie, x-board-key");
  if (env.BOARD_MIGRATION_PROBE !== "1") return res.status(404).json({ error: "not enabled" });
  let authenticated = false;
  try { authenticated = !!benAuth(req, env); } catch { /* malformed cookie */ }
  if (!authenticated) return res.status(401).json({ error: "sign in" });
  if (req.method !== "GET") return res.status(405).json({ error: "GET only" });
  if (!env.BOARD_GH_TOKEN) return res.status(503).json({ error: "server credential absent" });
  let stage = "repository";
  try {
    const read = async path => {
      // Cloudflare Workers fetch() supports "follow"|"manual" only ("error" throws TypeError);
      // "manual" never follows redirects and !r.ok below refuses any 3xx status.
      const r = await fetch(`https://api.github.com/repos/${REPO}${path}`, {
        method: "GET", redirect: "manual", signal: AbortSignal.timeout(8000),
        headers: { accept: "application/vnd.github+json", "user-agent": "studio-migration-probe",
          authorization: `Bearer ${env.BOARD_GH_TOKEN}` },
      });
      if (!r.ok) return { failure: r.status };
      return { value: await r.json() };
    };
    const repo = await read("");
    if (repo.failure) return res.status(502).json({ error: "upstream refused", stage, status: repo.failure });
    if (repo.value.full_name !== REPO || repo.value.private !== true)
      return res.status(502).json({ error: "private repository not confirmed", stage });
    stage = "ref";
    const ref = await read(`/git/ref/heads/${REF}`);
    if (ref.failure) return res.status(502).json({ error: "upstream refused", stage, status: ref.failure });
    const commit = ref.value.object?.sha;
    if (!SHA.test(commit || "") || ref.value.object?.type !== "commit")
      return res.status(502).json({ error: "invalid ref", stage });
    stage = "contents";
    const file = await read(`/contents/channels/channels.json?ref=${commit}`);
    if (file.failure) return res.status(502).json({ error: "upstream refused", stage, status: file.failure });
    if (file.value.type !== "file" || file.value.path !== "channels/channels.json" || !SHA.test(file.value.sha || ""))
      return res.status(502).json({ error: "invalid file metadata", stage });
    return res.status(200).json({ ok: true, private: true, ref: REF, commit, contentsRead: true });
  } catch {
    // Never echo an exception: a transport or upstream error can contain private values.
    return res.status(502).json({ error: "probe failed", stage });
  }
}
