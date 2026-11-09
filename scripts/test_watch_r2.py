import json, os, pathlib, shutil, subprocess, sys, tempfile, time, unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kanban_snapshot as ks  # noqa: E402

SIGN = pathlib.Path(__file__).resolve().parent.parent / "05_Analytics" / "kanban" / "board_site" / "r2sign.js"


@unittest.skipUnless(shutil.which("node"), "node not installed")
class SigV4(unittest.TestCase):
    """r2sign.js against AWS's own published SigV4 examples (S3 GET Object and ListObjects)."""

    def node(self, js):
        return subprocess.run(["node", "--input-type=module", "-e", js], capture_output=True, text=True, check=True).stdout

    def test_matches_aws_examples(self):
        out = self.node(f"""
import {{ signedHeaders }} from {json.dumps(SIGN.as_uri())};
const c = {{ accessKeyId: "AKIAIOSFODNN7EXAMPLE", secretAccessKey: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
  region: "us-east-1", date: new Date("2013-05-24T00:00:00Z"),
  payloadHash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" }};
const sig = h => h.authorization.split("Signature=")[1];
console.log(sig(signedHeaders({{ ...c, method: "GET", url: "https://examplebucket.s3.amazonaws.com/test.txt", headers: {{ Range: "bytes=0-9" }} }})));
console.log(sig(signedHeaders({{ ...c, method: "GET", url: "https://examplebucket.s3.amazonaws.com/?max-keys=2&prefix=J" }})));
""").split()
        self.assertEqual(out, ["f0e8bdb87c964420e857bd35b5d6ed310bd44f0170aba48dd91039c6036bdb41",
                               "34b48302e7b5fa45bde8084f4b7868a86f0a534bc59db6670ed5711ef69dc6f7"])

    def test_newest_watch_url_picks_the_latest_mp4_under_the_id(self):
        out = self.node(f"""
import {{ newestWatchUrl }} from {json.dumps(SIGN.as_uri())};
const xml = `<ListBucketResult><Contents><Key>watch/hos-007-v02/aa-old.mp4</Key><LastModified>2026-10-22T10:00:00Z</LastModified></Contents>
<Contents><Key>watch/hos-007-v02/bb-new_PHONE.mp4</Key><LastModified>2026-10-23T10:00:00Z</LastModified></Contents>
<Contents><Key>watch/hos-007-v02/cc.jpg</Key><LastModified>2026-10-24T10:00:00Z</LastModified></Contents></ListBucketResult>`;
let asked = "";
const f = async (url) => {{ asked = url; return {{ ok: true, text: async () => xml }}; }};
const cfg = {{ accountId: "acc", accessKeyId: "k", secretAccessKey: "s", publicUrl: "https://pub.r2.dev", bucket: "owb-media" }};
console.log(await newestWatchUrl(cfg, "hos-007-v02", f));
console.log(asked.includes("prefix=watch%2Fhos-007-v02%2F"));
const none = async () => ({{ ok: true, text: async () => "<ListBucketResult></ListBucketResult>" }});
console.log(await newestWatchUrl(cfg, "x", none));
""").split()
        self.assertEqual(out, ["https://pub.r2.dev/watch/hos-007-v02/bb-new_PHONE.mp4", "true", "null"])


class AutoUpload(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.reg = self.tmp / "watch_uploads.json"
        self.film = self.tmp / "hos_007_master_v02_PHONE.mp4"
        self.film.write_bytes(b"x" * 10)
        self.env = self.tmp / ".env"
        self.env.write_text("BUFFER_API_KEY=a\nR2_ACCOUNT_ID=a\nR2_ACCESS_KEY_ID=b\nR2_SECRET_ACCESS_KEY=c\nR2_PUBLIC_URL=https://p.r2.dev\n")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_r2_ready_reads_the_env_file_and_needs_all_four_keys(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertTrue(ks.r2_ready(self.env))
            self.env.write_text("R2_ACCOUNT_ID=a\nR2_ACCESS_KEY_ID=b\nR2_PUBLIC_URL=\n")
            self.assertFalse(ks.r2_ready(self.env))
            self.assertFalse(ks.r2_ready(self.tmp / "missing.env"))

    def run_upload(self, code):
        done = subprocess.CompletedProcess([], code, "", "R2 upload 403: denied")
        with mock.patch.object(ks, "WATCH_LOCAL_REGISTER", self.reg), mock.patch.object(ks, "r2_ready", return_value=True), \
                mock.patch.dict(os.environ, {}, clear=True), mock.patch("subprocess.run", return_value=done) as run:
            ok = ks.auto_upload("hos-007-v02", self.film, "HOS UAT/007/hos_007_master_v02_PHONE.mp4")
        return ok, run.call_count

    def test_success_registers_the_cut(self):
        ok, calls = self.run_upload(0)
        self.assertTrue(ok)
        self.assertEqual(json.loads(self.reg.read_text())["files"], {"HOS UAT/007/hos_007_master_v02_PHONE.mp4": "hos-007-v02"})

    def test_no_r2_means_no_upload_even_with_the_old_blob_key(self):
        # 29 Oct 2026: the Vercel Blob fallback is gone, so WATCH_UPLOAD_KEY alone never starts an upload.
        with mock.patch.object(ks, "WATCH_LOCAL_REGISTER", self.reg), mock.patch.object(ks, "r2_ready", return_value=False), \
                mock.patch.dict(os.environ, {"WATCH_UPLOAD_KEY": "old"}, clear=True), mock.patch("subprocess.run") as run:
            self.assertFalse(ks.auto_upload("hos-007-v02", self.film, "HOS UAT/007/hos_007_master_v02_PHONE.mp4"))
        run.assert_not_called()

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_watch_upload_fails_loudly_without_r2(self):
        script = pathlib.Path(__file__).resolve().parent / "watch_upload.mjs"
        home = self.tmp / "home"
        home.mkdir()
        r = subprocess.run(["node", str(script), "hos-007-v02", str(self.film)], capture_output=True, text=True,
                           env={"PATH": os.environ.get("PATH", ""), "HOME": str(home), "ORBIT_REPO": str(self.tmp)},
                           cwd=str(self.tmp))
        if "no R2 keys" not in r.stderr and (script.parent.parent / "07_Content-Ops" / ".env").exists():
            self.skipTest("this checkout has a real 07_Content-Ops/.env with R2 keys")
        self.assertEqual(r.returncode, 2)
        self.assertIn("no R2 keys", r.stderr)
        self.assertIn("no Vercel Blob fallback", r.stderr)

    def test_a_failed_upload_is_not_retried_for_six_hours(self):
        self.assertEqual(self.run_upload(1), (False, 1))
        self.assertEqual(self.run_upload(0), (False, 0))   # backing off: no second upload
        reg = json.loads(self.reg.read_text())
        reg["failed"]["hos-007-v02"] = time.time() - ks.WATCH_RETRY_S - 1
        self.reg.write_text(json.dumps(reg))
        ok, calls = self.run_upload(0)
        self.assertEqual((ok, calls), (True, 1))
        self.assertNotIn("hos-007-v02", json.loads(self.reg.read_text()).get("failed", {}))


class MiniPaths(unittest.TestCase):
    """J0888: board_publish runs from a sparse worktree with no .env, and iCloud evicts the _PHONE copies."""

    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_env_falls_back_to_the_main_checkout(self):
        home = self.tmp / "home"
        env = home / "YouTube" / "orbit-with-ben" / "07_Content-Ops" / ".env"
        env.parent.mkdir(parents=True)
        env.write_text("R2_ACCOUNT_ID=a\nR2_ACCESS_KEY_ID=b\nR2_SECRET_ACCESS_KEY=c\nR2_PUBLIC_URL=https://p.r2.dev\n")
        with mock.patch.object(ks, "ROOT", self.tmp / "worktree"), mock.patch.dict(os.environ, {"HOME": str(home)}, clear=True):
            self.assertIn(env, ks.env_files())
            self.assertTrue(ks.r2_ready())
        with mock.patch.object(ks, "ROOT", self.tmp / "worktree"), mock.patch.dict(os.environ, {"HOME": str(self.tmp / "nobody")}, clear=True):
            self.assertFalse(ks.r2_ready())

    def test_a_local_file_is_ready_and_an_evicted_one_without_brctl_is_not(self):
        f = self.tmp / "cut_PHONE.mp4"
        f.write_bytes(b"x" * 4096)
        self.assertTrue(ks.materialise(f))
        fake = mock.Mock(st_size=90_000_000, st_blocks=0)
        with mock.patch.object(pathlib.Path, "stat", return_value=fake), mock.patch("shutil.which", return_value=None):
            self.assertFalse(ks.materialise(f, wait_s=0))


if __name__ == "__main__":
    unittest.main()
