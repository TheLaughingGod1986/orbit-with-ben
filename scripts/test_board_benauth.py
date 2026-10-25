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
        self.assertIn("const how = benAuth(req);", js)
        self.assertIn("if (!how) return res.status(401)", js)
        self.assertIn("b.dryRun", js)
        self.assertLess(js.index("if (b.dryRun)"), js.index("await save(state)"))


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
