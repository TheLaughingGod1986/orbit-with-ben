"""Ben's one-tap board buttons (25 Oct 2026): no code prompt, cookie session, one-time pairing link (benauth.js)."""
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent / "05_Analytics/kanban/board_site"
sys.path.insert(0, str(HERE))
import board_pair_link as bpl  # noqa: E402


class PageNeverAsksForACode(unittest.TestCase):
    def test_no_prompt_anywhere(self):
        for f in ("tracker_app.js", "shim.js"):
            js = (SITE / f).read_text()
            self.assertNotIn("prompt(", js, f)
            self.assertIn('credentials: "same-origin"', js, f)

    def test_checks_api_uses_benauth_and_has_dry_run(self):
        js = (SITE / "api/checks.js").read_text()
        self.assertIn("const how = tapAuth(req);", js)
        self.assertIn("if (!how) return res.status(401)", js)
        self.assertIn("b.dryRun", js)
        self.assertLess(js.index("if (b.dryRun)"), js.index("await save(state)"))

    def test_no_dialogs_on_the_buttons(self):
        # Ben, 25 Oct 13:34: Approve / Request changes / comment / Send to the Chief just go, with a toast, never a dialog
        for f in ("tracker_app.js", "shim.js"):
            js = (SITE / f).read_text()
            for bad in ("alert(", "confirm(", "isn't linked", "NOT_LINKED"):
                self.assertNotIn(bad, js, f"{f}: {bad}")
            self.assertIn('toast("Sent ✓")', js, f)
        page = (SITE.parent / "studio_kanban.html").read_text()
        self.assertNotIn("alert(", page)
        self.assertNotIn("confirm(", page)


@unittest.skipUnless(shutil.which("node"), "node not installed")
class OpenTapsNode(unittest.TestCase):
    """A browser without the cookie (Home Screen copy, Gmail in-app browser) is accepted, cookied and audited."""

    HANDLER = """import handler from "./api/checks.js";
const posted = [], patched = [];
let body = "x\\n\\n```json\\n" + JSON.stringify({ checks: {}, history: [], pairs: [], audit: __AUDIT__ }) + "\\n```\\n";
globalThis.fetch = async (url, init = {}) => {
  if (/comments$/.test(url)) { posted.push(JSON.parse(init.body).body); return { ok: true, json: async () => ({}) }; }
  if (init.method === "PATCH") { body = JSON.parse(init.body).body; patched.push(body); return { ok: true, json: async () => ({ updated_at: "t2" }) }; }
  return { ok: true, json: async () => ({ updated_at: "t1", body }) };
};
process.env.BOARD_KEY = "k1"; process.env.BOARD_GH_TOKEN = "t";
__ENV__
const headers = Object.assign({ host: "studio-kanban.vercel.app", origin: "https://studio-kanban.vercel.app",
  "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
  "x-forwarded-for": "203.0.113.7" }, __HDR__);
const out = { headers: {} };
const res = { setHeader(k, v) { out.headers[k.toLowerCase()] = v; }, status(c) { out.status = c; return this; }, json(j) { out.json = j; return this; } };
await handler({ method: "POST", headers, query: {}, body: __BODY__ }, res);
console.log(JSON.stringify({ status: out.status, json: out.json, cookie: out.headers["set-cookie"] || "", posted, patched }));"""

    def run_handler(self, body, hdr=None, env="", audit="[]"):
        code = (self.HANDLER.replace("__BODY__", json.dumps(body)).replace("__HDR__", json.dumps(hdr or {}))
                .replace("__ENV__", env).replace("__AUDIT__", audit))
        out = subprocess.run(["node", "--input-type=module", "-e", code], cwd=SITE, capture_output=True, text=True, check=True)
        return json.loads(out.stdout.strip().splitlines()[-1])   # the handler's own log lines come first

    doc = {"film": "OWB:S3", "version": "v04", "verdict": "ok", "fixes": [], "note": "", "at": "2026-10-25T13:40:00Z"}

    def test_dry_run_from_uncookied_phone_succeeds(self):
        r = self.run_handler({"id": "OWB-S3", "dryRun": True, "doc": self.doc})
        self.assertEqual(r["status"], 200)
        self.assertTrue(r["json"]["ok"]); self.assertEqual(r["json"]["auth"], "open")
        self.assertTrue(r["json"]["wouldPost"].startswith("[Ben] OK S3 v04"))
        self.assertIn("new device: iPhone web app / in-app browser, ip#", r["json"]["wouldPost"])
        self.assertNotIn("203.0.113.7", json.dumps(r))
        self.assertIn("studio_ben=v1.", r["cookie"]); self.assertIn("Max-Age=34560000; HttpOnly", r["cookie"])
        self.assertEqual(r["posted"], []); self.assertEqual(r["patched"], [])

    def test_real_tap_posts_ben_ok_and_audits(self):
        r = self.run_handler({"id": "OWB-S3", "doc": self.doc})
        self.assertEqual(r["status"], 200)
        self.assertEqual(len(r["posted"]), 1)
        self.assertTrue(r["posted"][0].startswith("[Ben] OK S3 v04"))
        self.assertIn("new device", r["posted"][0])
        self.assertIn('"audit":[{', r["patched"][0]); self.assertIn('"device":"iPhone', r["patched"][0])
        self.assertNotIn("203.0.113.7", r["patched"][0] + r["posted"][0])

    def test_cookied_tap_is_not_marked_new(self):
        r0 = self.node_session()
        r = self.run_handler({"id": "OWB-S3", "doc": self.doc}, {"cookie": "studio_ben=" + r0})
        self.assertTrue(r["posted"][0].startswith("[Ben] OK S3 v04"))
        self.assertNotIn("new device", r["posted"][0])
        self.assertNotIn('"device"', r["patched"][0])

    def node_session(self):
        out = subprocess.run(["node", "--input-type=module", "-e", 'import { makeSession } from "./benauth.js"; console.log(makeSession("k1"));'],
                             cwd=SITE, capture_output=True, text=True, check=True)
        return out.stdout.strip()

    def test_kill_switch_locks_again(self):
        r = self.run_handler({"id": "OWB-S3", "dryRun": True, "doc": self.doc}, env='process.env.BOARD_OPEN_TAPS = "0";')
        self.assertEqual(r["status"], 401); self.assertEqual(r["cookie"], "")

    def test_cross_site_post_refused(self):
        r = self.run_handler({"id": "OWB-S3", "dryRun": True, "doc": self.doc}, {"origin": "https://evil.example"})
        self.assertEqual(r["status"], 401)

    def test_rate_limit(self):
        import datetime
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        audit = json.dumps([{"at": now, "id": "OWB-001", "op": "ok"}] * 20)
        r = self.run_handler({"id": "OWB-S3", "doc": self.doc}, audit=audit)
        self.assertEqual(r["status"], 429); self.assertEqual(r["posted"], [])


@unittest.skipUnless(shutil.which("node"), "node not installed")
class BenAuthNode(unittest.TestCase):
    def node(self, code):
        out = subprocess.run(["node", "--input-type=module", "-e", code], cwd=SITE, capture_output=True, text=True, check=True)
        return json.loads(out.stdout)

    def test_python_link_matches_server_check(self):
        link, e = bpl.pair_link("test-secret", 7, nonce="abcdefghijklmnopqrstuv")
        q = dict(p.split("=", 1) for p in link.split("?", 1)[1].split("&"))
        r = self.node(f"""import {{ pairOk }} from "./benauth.js";
const q = {json.dumps(q)};
console.log(JSON.stringify({{ good: pairOk(q.n, q.e, q.s, "test-secret"), wrongSecret: pairOk(q.n, q.e, q.s, "x"),
  tampered: pairOk(q.n + "x", q.e, q.s, "test-secret"), expired: pairOk(q.n, q.e, q.s, "test-secret", Number(q.e) + 1),
  tooFar: pairOk(q.n, String(Number(q.e) + 86400 * 8), q.s, "test-secret") }}));""")
        self.assertEqual(r, {"good": True, "wrongSecret": False, "tampered": False, "expired": False, "tooFar": False})

    def test_session_cookie(self):
        r = self.node("""import { makeSession, sessionValid, benAuth, cookieHeader } from "./benauth.js";
const s = makeSession("k1");
const env = { BOARD_KEY: "k1" };
console.log(JSON.stringify({ ok: sessionValid(s, "k1"), rotated: sessionValid(s, "k2"), forged: sessionValid("v1.1761390000.AAAAAAAAAAAAAAAAAAAAAAAA", "k1"),
  cookie: benAuth({ headers: { cookie: "a=b; studio_ben=" + s } }, env), key: benAuth({ headers: { "x-board-key": "k1" } }, env),
  anon: benAuth({ headers: {} }, env), wrongKey: benAuth({ headers: { "x-board-key": "nope" } }, env),
  hdr: cookieHeader("v").includes("HttpOnly; Secure; SameSite=Lax") }));""")
        self.assertEqual(r, {"ok": True, "rotated": False, "forged": False, "cookie": "cookie", "key": "key",
                             "anon": "", "wrongKey": "", "hdr": True})

    def test_store_keeps_used_pair_nonces_until_expiry(self):
        r = self.node("""import { parseStore, renderStore } from "./api/checks.js";
const now = Date.now();
const body = renderStore({ checks: {}, history: [], pairs: [{ n: "old", e: Math.floor(now / 1000) - 10 }, { n: "live", e: Math.floor(now / 1000) + 99 }] }, now);
console.log(JSON.stringify(parseStore(body).pairs.map(p => p.n)));""")
        self.assertEqual(r, ["live"])


if __name__ == "__main__":
    unittest.main()
