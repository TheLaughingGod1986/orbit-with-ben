"""Offline boundary checks for the opt-in production-credential probe (J3012)."""
import json
import shutil
import subprocess
import unittest
from pathlib import Path

SITE = Path(__file__).resolve().parents[1] / "05_Analytics/kanban/board_site"
HARNESS = r'''
import handler from './api/migration.js';
import { makeSession } from './benauth.js';
process.env.BOARD_KEY = 'test-board-key';
process.env.BOARD_GH_TOKEN = 'test-private-token';
process.env.BOARD_MIGRATION_PROBE = '1';
const sha = 'a'.repeat(40), calls = [], out = {headers: {}};
let failure = '', mode = '', method = 'GET';
let headers = {'x-board-key': 'test-board-key'};
globalThis.fetch = async (url, init) => {
  calls.push({url, method: init.method, auth: init.headers.authorization === 'Bearer test-private-token',
    redirect: init.redirect, bounded: !!init.signal});
  if (mode === 'throw') throw new Error('test-private-token sensitive upstream body');
  let stage = url.includes('/contents/') ? 'contents' : url.includes('/git/ref/') ? 'ref' : 'repository';
  let value = stage === 'repository' ? {full_name:'TheLaughingGod1986/studio',private:mode !== 'public'} :
    stage === 'ref' ? {object:{sha,type:'commit'}} :
    {type:'file',path:'channels/channels.json',sha,content:'private-file-body'};
  if (mode === 'bad-ref' && stage === 'ref') value.object.sha = 'invalid';
  if (mode === 'bad-file' && stage === 'contents') value.path = 'wrong';
  if (mode === 'redirect' && stage === 'repository') return {ok: false, status: 302, json:async()=>({})};
  return {ok: stage !== failure, status: stage === failure ? 403 : 200, json:async()=>value};
};
__SETUP__
const res = {setHeader(k,v){out.headers[k]=v;},status(s){out.status=s;return this;},json(v){out.body=v;return this;}};
await handler({method,headers,query:{repo:'attacker/other',ref:'evil',path:'secret'}},res);
console.log(JSON.stringify({out,calls}));
'''


@unittest.skipUnless(shutil.which("node"), "node required")
class Probe(unittest.TestCase):
    def run_probe(self, setup=""):
        p = subprocess.run(["node", "--input-type=module", "-e", HARNESS.replace("__SETUP__", setup)],
                           cwd=SITE, capture_output=True, text=True, timeout=20)
        self.assertEqual(p.returncode, 0, p.stderr)
        result = json.loads(p.stdout)
        self.assertNotIn("test-private-token", json.dumps(result))
        self.assertNotIn("private-file-body", json.dumps(result))
        self.assertEqual(result["out"]["headers"]["Cache-Control"], "no-store")
        return result

    def test_disabled_by_default(self):
        r = self.run_probe("delete process.env.BOARD_MIGRATION_PROBE;")
        self.assertEqual(r["out"]["status"], 404)
        self.assertEqual(r["calls"], [])

    def test_no_auth_or_malformed_cookie_never_reads(self):
        for h in ["{}", "{cookie:'studio_ben=%ZZ'}", "{'x-board-key':'wrong'}"]:
            with self.subTest(h=h):
                r = self.run_probe("headers=" + h + "; process.env.BOARD_OPEN_TAPS='1';")
                self.assertEqual(r["out"]["status"], 401)
                self.assertEqual(r["calls"], [])

    def test_method_and_missing_server_credential(self):
        for setup, status in [("method='POST';", 405), ("method='HEAD';", 405),
                              ("delete process.env.BOARD_GH_TOKEN;", 503)]:
            r = self.run_probe(setup)
            self.assertEqual(r["out"]["status"], status)
            self.assertEqual(r["calls"], [])

    def test_real_auth_shapes_read_only_fixed_target(self):
        for setup in ["", "headers={cookie:'studio_ben='+makeSession('test-board-key')};"]:
            r = self.run_probe(setup)
            self.assertEqual(r["out"]["status"], 200)
            self.assertTrue(r["out"]["body"]["contentsRead"])
            self.assertEqual(len(r["calls"]), 3)
            for c in r["calls"]:
                self.assertEqual(c["method"], "GET")
                self.assertTrue(c["auth"] and c["bounded"])
                self.assertEqual(c["redirect"], "manual")
                self.assertTrue(c["url"].startswith('https://api.github.com/repos/TheLaughingGod1986/studio'))
                self.assertNotIn('evil', c["url"])
            self.assertTrue(r["calls"][-1]["url"].endswith('?ref=' + 'a' * 40))

    def test_failure_never_retries_anonymously(self):
        for stage, count in [("repository", 1), ("ref", 2), ("contents", 3)]:
            r = self.run_probe(f"failure='{stage}';")
            self.assertEqual(r["out"]["status"], 502)
            self.assertEqual(r["out"]["body"]["stage"], stage)
            self.assertEqual(len(r["calls"]), count)
            self.assertTrue(all(c["auth"] for c in r["calls"]))

    def test_public_or_invalid_results_do_not_pass(self):
        for mode in ["public", "bad-ref", "bad-file", "throw", "redirect"]:
            r = self.run_probe(f"mode='{mode}';")
            self.assertEqual(r["out"]["status"], 502)
            self.assertNotIn("ok", r["out"]["body"])
            if mode == "redirect":
                self.assertEqual(r["out"]["body"].get("status"), 302)
                self.assertEqual(len(r["calls"]), 1)

    def test_cloudflare_route_stays_disabled_until_enabled(self):
        code = r'''
import worker from './cf_worker.js';
globalThis.fetch = () => {throw new Error('unexpected upstream access');};
delete process.env.BOARD_MIGRATION_PROBE;
let r = await worker.fetch(new Request('https://board.example/api/migration'), {});
const disabled = r.status;
r = await worker.fetch(new Request('https://board.example/api/migration'), {BOARD_MIGRATION_PROBE:'1'});
console.log(JSON.stringify({disabled, anonymous:r.status, cache:r.headers.get('cache-control')}));
'''
        p = subprocess.run(["node", "--input-type=module", "-e", code], cwd=SITE,
                           capture_output=True, text=True, timeout=20)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout), {"disabled": 404, "anonymous": 401, "cache": "no-store"})

    def test_cloudflare_probe_does_not_reuse_removed_bindings(self):
        code = r'''
import worker from './cf_worker.js';
let calls = 0;
globalThis.fetch = async () => { calls++; return {ok:false,status:403}; };
const request = () => new Request('https://board.example/api/migration',
  {headers:{'x-board-key':'test-key'}});
const enabled = {BOARD_MIGRATION_PROBE:'1', BOARD_KEY:'test-key', BOARD_GH_TOKEN:'test-token'};
const statuses = [];
statuses.push((await worker.fetch(request(), enabled)).status);
// The adapter still holds prior process.env strings, but these requests must not use them.
statuses.push((await worker.fetch(request(), {BOARD_KEY:'test-key',BOARD_GH_TOKEN:'test-token'})).status);
statuses.push((await worker.fetch(request(), {BOARD_MIGRATION_PROBE:'1',BOARD_GH_TOKEN:'test-token'})).status);
statuses.push((await worker.fetch(request(), {BOARD_MIGRATION_PROBE:'1',BOARD_KEY:'test-key'})).status);
console.log(JSON.stringify({statuses,calls}));
'''
        p = subprocess.run(["node", "--input-type=module", "-e", code], cwd=SITE,
                           capture_output=True, text=True, timeout=20)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout), {"statuses": [502, 404, 401, 503], "calls": 1})


if __name__ == "__main__":
    unittest.main()
