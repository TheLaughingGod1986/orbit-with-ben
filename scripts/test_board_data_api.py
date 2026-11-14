#!/usr/bin/env python3
"""The board reads its data through its own server, for signed-in viewers only once the repo is private (J2532).

`05_Analytics/kanban/board_site/api/data.js` is the one function. These tests hold it to its brief:
  - while the data's repo is public, anyone reads it, as before;
  - once it is private, a viewer with no cookie and no board key gets 401 and GitHub is not read for them;
  - Ben's cookie or his board key reads it, with the server's token, and the token never comes back in an answer;
  - a copy is held (the branch's commit 20 s, a branch file 45 s) and "not changed" is answered with 304;
  - a file is only read at the commit the branch is on, so invented commits cannot spend the token's allowance;
  - the three pages ask this function first and stop on 401 instead of trying GitHub.
The last class opens the built pages in a real browser with GitHub's public addresses blocked. It runs where
Playwright is installed (the cloud sessions and the Mini) and is skipped elsewhere.

    python3 scripts/test_board_data_api.py
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent / "05_Analytics/kanban/board_site"
NODE = shutil.which("node")
SHA_A, SHA_B = "a" * 40, "b" * 40

# A stand-in for GitHub. `world.private` hides the repo from requests without the token, as GitHub does.
HARNESS = r"""
import handler, { forget, HOLD_S, FILES, dataRepo } from "./api/data.js";
import { makeSession } from "./benauth.js";
const TOKEN = "tok-never-shown";
process.env.BOARD_KEY = "k1"; process.env.BOARD_GH_TOKEN = TOKEN;
const world = { private: false, head: "__A__", calls: [], rawDown: false };
const answer = (status, body) => ({ ok: status >= 200 && status < 300, status, json: async () => JSON.parse(body), text: async () => body });
globalThis.fetch = async (url, init = {}) => {
  const auth = ((init.headers || {}).authorization || "") === "Bearer " + TOKEN;
  world.calls.push((init.method || "GET") + " " + url.replace(/^https:\/\//, "") + (auth ? " +token" : ""));
  if (world.private && !auth) return answer(404, "{}");
  if (/^https:\/\/raw\.githubusercontent\.com\//.test(url)) return world.rawDown ? answer(503, "") : answer(200, JSON.stringify({ from: "raw", url }));
  if (/git\/ref\/heads\/board-data$/.test(url)) return answer(200, JSON.stringify({ object: { sha: world.head } }));
  const m = /contents\/([\w.]+)\?ref=([\w-]+)$/.exec(url);
  if (m) return answer(200, JSON.stringify({ file: m[1], at: m[2] }));
  return answer(404, "{}");
};
const cookie = "studio_ben=" + makeSession("k1");
async function get(query, headers = {}, method = "GET") {
  const out = { headers: {} };
  const res = { setHeader(k, v) { out.headers[k.toLowerCase()] = v; }, status(c) { out.status = c; return this; },
    json(j) { out.body = JSON.stringify(j); return this; }, send(b) { out.body = b; return this; }, end() { out.body = ""; return this; } };
  await handler({ method, headers, query }, res);
  return out;
}
const results = {};
__BODY__
console.log(JSON.stringify(results));
"""


def run(body: str) -> dict:
    code = HARNESS.replace("__BODY__", body).replace("__A__", SHA_A)
    out = subprocess.run([NODE, "--input-type=module", "-e", code], cwd=SITE, capture_output=True, text=True)
    if out.returncode:
        raise AssertionError(out.stderr[-2000:])
    return json.loads(out.stdout.strip().splitlines()[-1])


@unittest.skipUnless(NODE, "node not installed")
class ContentEtags(unittest.TestCase):
    def test_same_length_different_content_is_not_304(self):
        r = run("""
let body = '{"value":1}';
const original = globalThis.fetch;
globalThis.fetch = async (url, init) => /contents/.test(url) ? answer(200, body) : original(url, init);
const first = await get({f:'updates'});
forget(); body = '{"value":2}';
results.changed = await get({f:'updates'}, {'if-none-match': first.headers.etag});
results.same = await get({f:'updates'}, {'if-none-match': 'W/' + results.changed.headers.etag + ', "other"'});
results.calls = world.calls;
""")
        self.assertEqual(r['changed']['status'], 200)
        self.assertEqual(r['same']['status'], 304)

    def test_tracker_content_etag_survives_new_board_commit(self):
        r = run("""
const original = globalThis.fetch;
globalThis.fetch = async (url, init) => /contents/.test(url) ? answer(200, '{"channels":[]}') : original(url, init);
const first = await get({f:'tracker', sha:'__A__'});
forget(); world.head = 'b'.repeat(40);
results.same = await get({f:'tracker', sha: world.head}, {'if-none-match': first.headers.etag});
""")
        self.assertEqual(r['same']['status'], 304)


@unittest.skipUnless(NODE, "node not installed")
class WhoMayRead(unittest.TestCase):
    def test_while_the_repo_is_public_anyone_reads_as_before(self):
        r = run(f"""
results.ref = await get({{ f: "ref" }});
results.board = await get({{ f: "board", sha: "{SHA_A}" }});
results.macbook = await get({{ f: "macbook" }});
results.calls = world.calls;""")
        self.assertEqual(r["ref"]["status"], 200)
        self.assertEqual(json.loads(r["ref"]["body"]), {"object": {"sha": SHA_A}})
        self.assertEqual(json.loads(r["board"]["body"]), {"file": "board.json", "at": SHA_A})
        self.assertEqual(json.loads(r["macbook"]["body"]), {"file": "heartbeat.json", "at": "macbook-heartbeat"})
        # shared copies are allowed while the data is public
        self.assertIn("public", r["ref"]["headers"]["cache-control"])
        self.assertIn("immutable", r["board"]["headers"]["cache-control"])
        self.assertNotIn("vary", r["board"]["headers"])

    def test_once_private_a_stranger_gets_401_and_github_is_not_read_for_them(self):
        r = run(f"""
world.private = true;
results.ref = await get({{ f: "ref" }});
results.board = await get({{ f: "board", sha: "{SHA_A}" }});
results.tracker = await get({{ f: "tracker" }});
results.macbook = await get({{ f: "macbook" }});
results.wrongKey = await get({{ f: "board" }}, {{ "x-board-key": "nope" }});
results.calls = world.calls;""")
        for name in ("ref", "board", "tracker", "macbook", "wrongKey"):
            self.assertEqual(r[name]["status"], 401, name)
            self.assertEqual(json.loads(r[name]["body"]), {"error": "sign in", "signIn": True}, name)
            self.assertEqual(r[name]["headers"]["cache-control"], "no-store", name)
        # the only request made was the one that asks "is it public?", and it carried no token
        self.assertEqual(len(r["calls"]), 1, r["calls"])
        self.assertTrue(r["calls"][0].startswith("HEAD raw.githubusercontent.com/"), r["calls"])
        self.assertNotIn("+token", r["calls"][0])

    def test_once_private_bens_cookie_or_board_key_reads_with_the_servers_token(self):
        r = run(f"""
world.private = true;
results.cookie = await get({{ f: "board", sha: "{SHA_A}" }}, {{ cookie }});
results.key = await get({{ f: "tracker", sha: "{SHA_A}" }}, {{ "x-board-key": "k1" }});
results.ref = await get({{ f: "ref" }}, {{ cookie }});
results.calls = world.calls;""")
        self.assertEqual(json.loads(r["cookie"]["body"]), {"file": "board.json", "at": SHA_A})
        self.assertEqual(json.loads(r["key"]["body"]), {"file": "tracker.json", "at": SHA_A})
        self.assertEqual(r["ref"]["status"], 200)
        reads = [c for c in r["calls"] if "api.github.com" in c]
        self.assertTrue(reads and all(c.endswith("+token") for c in reads), r["calls"])
        for name in ("cookie", "key", "ref"):
            # a private answer is never kept where another viewer could be given it
            self.assertTrue(r[name]["headers"]["cache-control"].startswith("private"), name)
            self.assertEqual(r[name]["headers"]["vary"], "Cookie, x-board-key", name)
            self.assertNotIn("tok-never-shown", json.dumps(r[name]))

    def test_the_setting_forces_private_before_the_move(self):
        r = run("""
process.env.BOARD_PRIVATE = "1";
results.stranger = await get({ f: "ref" });
results.ben = await get({ f: "ref" }, { cookie });
results.calls = world.calls;""")
        self.assertEqual(r["stranger"]["status"], 401)
        self.assertEqual(r["ben"]["status"], 200)
        self.assertFalse([c for c in r["calls"] if c.startswith("HEAD")], "no need to ask GitHub whether it is public")

    def test_if_public_cannot_be_confirmed_it_counts_as_private(self):
        r = run("""
world.rawDown = true;
results.stranger = await get({ f: "ref" });
results.ben = await get({ f: "ref" }, { cookie });""")
        self.assertEqual(r["stranger"]["status"], 401)
        self.assertEqual(r["ben"]["status"], 200)

    def test_the_repo_comes_from_a_setting_at_the_move(self):
        r = run("""
results.now = dataRepo({});
results.moved = dataRepo({ BOARD_DATA_REPO: "TheLaughingGod1986/studio" });
results.nonsense = dataRepo({ BOARD_DATA_REPO: "https://example.com/x y" });
process.env.BOARD_DATA_REPO = "TheLaughingGod1986/studio";
await get({ f: "ref" });
results.calls = world.calls;""")
        self.assertEqual(r["now"], "TheLaughingGod1986/orbit-with-ben")
        self.assertEqual(r["moved"], "TheLaughingGod1986/studio")
        self.assertEqual(r["nonsense"], "TheLaughingGod1986/orbit-with-ben")
        self.assertTrue(all("TheLaughingGod1986/studio/" in c for c in r["calls"]), r["calls"])


@unittest.skipUnless(NODE, "node not installed")
class WhatItCosts(unittest.TestCase):
    def test_a_copy_is_held_so_many_viewers_mean_few_github_reads(self):
        r = run(f"""
for (let i = 0; i < 25; i++) {{ await get({{ f: "ref" }}); await get({{ f: "board", sha: "{SHA_A}" }}); await get({{ f: "macbook" }}); }}
results.calls = world.calls;
results.hold = HOLD_S;""")
        api = [c for c in r["calls"] if "api.github.com" in c]
        self.assertEqual(len(api), 3, api)   # one commit read, one board.json, one heartbeat, for 75 requests
        self.assertGreaterEqual(r["hold"]["ref"], 20)
        self.assertTrue(30 <= r["hold"]["branch"] <= 60, r["hold"])

    def test_not_changed_is_answered_with_304(self):
        r = run(f"""
const first = await get({{ f: "ref" }});
results.again = await get({{ f: "ref" }}, {{ "if-none-match": first.headers.etag }});
world.head = "{SHA_B}"; forget();
results.moved = await get({{ f: "ref" }}, {{ "if-none-match": first.headers.etag }});
const file = await get({{ f: "board", sha: "{SHA_B}" }});
results.file = await get({{ f: "board", sha: "{SHA_B}" }}, {{ "if-none-match": file.headers.etag }});""")
        self.assertEqual(r["again"]["status"], 304)
        self.assertEqual(r["again"]["body"], "")
        self.assertEqual(r["moved"]["status"], 200)
        self.assertEqual(json.loads(r["moved"]["body"]), {"object": {"sha": SHA_B}})
        self.assertEqual(r["file"]["status"], 304)

    def test_304_is_never_given_to_a_stranger_once_private(self):
        r = run("""
const first = await get({ f: "ref" });
world.private = true; forget();
results.stranger = await get({ f: "ref" }, { "if-none-match": first.headers.etag });""")
        self.assertEqual(r["stranger"]["status"], 401)

    def test_an_invented_commit_reads_nothing_new_from_github(self):
        r = run(f"""
await get({{ f: "board", sha: "{SHA_A}" }});
const before = world.calls.length;
const made = [];
for (let i = 0; i < 20; i++) made.push(await get({{ f: "board", sha: i.toString(16).padStart(40, "c") }}));
results.extra = world.calls.slice(before);
results.one = made[0];""")
        self.assertEqual(r["extra"], [], "invented commits must not reach GitHub")
        self.assertEqual(json.loads(r["one"]["body"]), {"file": "board.json", "at": SHA_A})   # the commit the branch is on
        self.assertEqual(r["one"]["headers"]["x-board-sha"], SHA_A)
        self.assertEqual(r["one"]["headers"]["cache-control"], "no-store")                  # and it is not kept under the wrong name

    def test_what_is_asked_for_is_checked(self):
        r = run(f"""
results.none = await get({{}});
results.other = await get({{ f: "../../secrets" }});
results.proto = await get({{ f: "constructor" }});
results.badSha = await get({{ f: "board", sha: "main" }});
results.shaOnHeartbeat = await get({{ f: "macbook", sha: "{SHA_A}" }});
results.post = await get({{ f: "ref" }}, {{}}, "POST");
results.calls = world.calls;""")
        for name in ("none", "other", "proto", "badSha", "shaOnHeartbeat"):
            self.assertEqual(r[name]["status"], 400, name)
        self.assertEqual(r["post"]["status"], 405)
        self.assertEqual(r["calls"], [])

    def test_an_error_page_from_github_is_not_passed_on(self):
        r = run("""
const real = globalThis.fetch;
globalThis.fetch = async (url, init) => /contents\\//.test(url)
  ? { ok: true, status: 200, text: async () => "<html>rate limited</html>", json: async () => ({}) } : real(url, init);
results.board = await get({ f: "board" });""")
        self.assertEqual(r["board"]["status"], 502)
        self.assertNotIn("html", r["board"]["body"])


class ThePagesAskTheirOwnServer(unittest.TestCase):
    PAGES = ("studio_app.js", "ai_app.js", "tracker_loader.js")

    def test_every_page_reads_through_the_function_first(self):
        for name in self.PAGES:
            js = (SITE / name).read_text()
            self.assertIn('fetch("/api/data?" + query', js, name)
            self.assertIn('own("f=ref", "no-cache")', js, name)
            self.assertIn('credentials: "same-origin"', js, name)
            self.assertIn('"x-board-key": key', js, name)
        self.assertIn('own("f=board"', (SITE / "studio_app.js").read_text())
        self.assertIn('own("f=macbook", "no-store")', (SITE / "studio_app.js").read_text())
        self.assertIn('own("f=board"', (SITE / "ai_app.js").read_text())
        self.assertIn('own("f=tracker"', (SITE / "tracker_loader.js").read_text())

    def test_a_401_stops_the_read_and_shows_the_sign_in_line(self):
        for name in self.PAGES:
            js = (SITE / name).read_text()
            self.assertIn("if (r.status === 401) throw Object.assign(new Error(\"sign in\"), { signIn: true });", js, name)
            self.assertIn("if (e && e.signIn) throw e; return old();", js, name)   # never falls back to GitHub on 401
            self.assertIn("Open your board link on this device to sign in", js, name)

    def test_github_is_only_ever_the_fallback(self):
        """Each public GitHub address a page still names is used inside a fallback, after the function."""
        for name in self.PAGES:
            js = (SITE / name).read_text()
            for line in js.splitlines():
                if "fetch(" not in line or line.strip().startswith("//"):
                    continue
                if any(w in line for w in ("DATA_REF", "DATA_AT", "MACBOOK", "REF,", "AT(sha)", "BRANCH")):
                    self.assertTrue("() =>" in line or "oldRef" in line, f"{name}: a GitHub read outside a fallback: {line.strip()[:120]}")

    def test_the_page_version_follows_the_function(self):
        self.assertIn('HERE / "api" / "data.js"', (SITE / "build.py").read_text())

    def test_the_move_notes_say_what_ben_ticks_and_what_it_costs(self):
        doc = (HERE.parent / "docs" / "BOARD_PRIVATE_DATA.md").read_text()
        for must in ("api/data.js", "BOARD_DATA_REPO", "BOARD_GH_TOKEN", "Contents", "Read-only", "free plan"):
            self.assertIn(must, doc, must)


ONE_FILM = r"\b1\s+To do"   # the stand-in board holds one film, in the To do lane of the Videos tab


def playwright_here() -> bool:
    if not NODE:
        return False
    return subprocess.run([NODE, "-e", "require('playwright')"], capture_output=True).returncode == 0


@unittest.skipUnless(playwright_here(), "Playwright not installed")
class InARealBrowser(unittest.TestCase):
    """The done-when of J2532: with GitHub's public file addresses blocked, every page loads its data when signed in
    and shows the sign-in line when not."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        dist = Path(cls.tmp.name) / "dist"
        subprocess.run([sys.executable, str(SITE / "build.py"), "--out", str(dist)], check=True, capture_output=True)
        out = subprocess.run([NODE, str(HERE / "board_data_browser_check.cjs"), str(dist)], capture_output=True, text=True, timeout=240)
        if out.returncode:
            raise AssertionError((out.stdout + out.stderr)[-3000:])
        cls.seen = json.loads(out.stdout.strip().splitlines()[-1])

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_signed_in_and_private_every_page_loads_its_data(self):
        s = self.seen["private, signed in"]
        self.assertRegex(s["studio"], ONE_FILM)
        self.assertNotIn("private", s["studio"])
        self.assertIn("checks every minute", s["ai"])
        self.assertIn("Latest saved snapshot fetched", s["tracker"])

    def test_not_signed_in_and_private_every_page_shows_the_sign_in_line(self):
        s = self.seen["private, not signed in"]
        self.assertIn("This board is private. Open your board link on this device to sign in", s["studio"])
        self.assertNotRegex(s["studio"], ONE_FILM)
        self.assertIn("This page is private. Open your board link on this device to sign in", s["ai"])
        self.assertIn("This page is private. Open your board link on this device to sign in", s["tracker"])

    def test_while_public_a_visitor_with_no_cookie_still_sees_the_board(self):
        s = self.seen["public, not signed in"]
        self.assertRegex(s["studio"], ONE_FILM)
        self.assertIn("checks every minute", s["ai"])
        self.assertIn("Latest saved snapshot fetched", s["tracker"])

    def test_no_page_reached_for_githubs_public_addresses(self):
        for name, s in self.seen.items():
            self.assertEqual(s["github"], [], f"{name}: a page asked GitHub directly")


if __name__ == "__main__":
    unittest.main()
