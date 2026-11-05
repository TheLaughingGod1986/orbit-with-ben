#!/usr/bin/env python3
"""Tests for scripts/nas_offload.py on throwaway folders: old render scratch reaches the NAS with every sha256
checked before the Mini copy goes, nothing on the NAS is ever deleted or a verified copy written into, and nothing
moves when the share is missing (Ben, 28 Oct 2026: "The external storage we can use our NAS for now"). Copies wait
for the NAS's 01:00-06:00 window and a failed copy is retried in place, not copied again (Ben, 4 Nov 2026)."""
import datetime
import fcntl
import os
import pathlib
import sys
import tempfile
import time
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import nas_offload as no  # noqa: E402

MB = 1024 * 1024


def make(folder: pathlib.Path, files: dict, age_h: float = 0) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    t = time.time() - age_h * 3600
    for name, size in files.items():
        p = folder / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(os.urandom(size))
        os.utime(p, (t, t))
    os.utime(folder, (t, t))


class Offload(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = pathlib.Path(self.tmp.name)
        self.scratch, self.nas = t / "private_tmp", t / "Volumes_data"
        self.scratch.mkdir()
        (self.nas / no.NAS_ARCHIVE).mkdir(parents=True)
        self.free_mb = 5 * 1024  # 5 GB free: under the 20 GB target

    def tearDown(self):
        self.tmp.cleanup()

    def run_offload(self, apply=True, hour=2, **kw):
        clock = lambda: datetime.datetime(2026, 11, 5, hour, 30)  # noqa: E731 (default: inside the NAS window)
        return no.offload(apply, root=self.scratch, nas=self.nas, check_mount=False, free=lambda: self.free_mb,
                          min_mb=1, clock=clock, lock=pathlib.Path(self.tmp.name) / "offload.lock", **kw)

    def day_dir(self):
        return self.nas / no.NAS_ARCHIVE / "mini-tmp-scratch" / datetime.datetime.now(datetime.timezone.utc).date().isoformat()

    def test_old_scratch_moves_with_checked_manifest_and_marker(self):
        old = self.scratch / "owb_029_r21_v03b"
        make(old, {"a.mov": 2 * MB, "sub/b.wav": MB}, age_h=72)
        rep = self.run_offload()
        self.assertEqual(len(rep["moved"]), 1, rep)
        dst = pathlib.Path(rep["moved"][0]["nas"])
        self.assertTrue((dst / "a.mov").exists() and (dst / "sub/b.wav").exists())
        sums = (dst / "SHA256SUMS.txt").read_text()
        self.assertIn("a.mov", sums)
        self.assertIn("sub/b.wav", sums)
        self.assertEqual(sorted(x.name for x in old.iterdir()), [no.MARKER])
        self.assertIn(str(dst), (old / no.MARKER).read_text())

    def test_recent_scratch_stays(self):
        make(self.scratch / "current_render", {"a.mov": 2 * MB}, age_h=5)
        rep = self.run_offload()
        self.assertEqual(rep["moved"], [])
        self.assertTrue((self.scratch / "current_render" / "a.mov").exists())

    def test_nothing_moves_when_disk_has_headroom(self):
        make(self.scratch / "old", {"a.mov": MB}, age_h=100)
        self.free_mb = 30 * 1024
        rep = self.run_offload()
        self.assertEqual(rep["moved"], [])
        self.assertTrue((self.scratch / "old" / "a.mov").exists())

    def test_missing_share_moves_nothing(self):
        make(self.scratch / "old", {"a.mov": MB}, age_h=100)
        (self.nas / no.NAS_ARCHIVE).rmdir()
        rep = self.run_offload()
        self.assertNotEqual(rep["nas"], "ok")
        self.assertTrue((self.scratch / "old" / "a.mov").exists())

    def test_unmounted_path_is_refused(self):
        ok, why = no.nas_ready(self.nas, check_mount=True)  # a plain folder, not a mount
        self.assertFalse(ok)
        self.assertIn("not mounted", why)

    def test_nas_appledouble_files_do_not_fail_the_check(self):
        # 5 Nov 2026: the Synology share adds ._name beside files with extended attributes.
        old = self.scratch / "old"
        make(old, {"a.mov": MB, "sub/b.wav": MB}, age_h=100)
        real = no.copy_tree

        def with_appledouble(src, dst):
            real(src, dst)
            (dst / "._a.mov").write_bytes(b"\0" * 4096)
            (dst / "._sub").write_bytes(b"\0" * 4096)  # a folder's AppleDouble too
        no.copy_tree = with_appledouble
        try:
            rep = self.run_offload()
        finally:
            no.copy_tree = real
        self.assertEqual(len(rep["moved"]), 1, rep)
        self.assertNotIn("._a.mov", (pathlib.Path(rep["moved"][0]["nas"]) / "SHA256SUMS.txt").read_text())

    def test_an_unexplained_extra_file_still_fails(self):
        old = self.scratch / "old"
        make(old, {"a.mov": MB}, age_h=100)
        real = no.copy_tree

        def extra(src, dst):
            real(src, dst)
            (dst / "._b.mov").write_bytes(b"x")  # no b.mov in the source: not AppleDouble of ours
        no.copy_tree = extra
        try:
            rep = self.run_offload()
        finally:
            no.copy_tree = real
        self.assertEqual(rep["moved"], [])
        self.assertTrue((old / "a.mov").exists())

    def test_bad_copy_keeps_the_mini_copy(self):
        old = self.scratch / "old"
        make(old, {"a.mov": MB}, age_h=100)
        real = no.copy_tree

        def corrupt(src, dst):
            real(src, dst)
            (dst / "a.mov").write_bytes(b"truncated")
        no.copy_tree = corrupt
        try:
            rep = self.run_offload()
        finally:
            no.copy_tree = real
        self.assertEqual(rep["moved"], [])
        self.assertIn("mismatch", rep["kept"][0]["why"])
        self.assertTrue((old / "a.mov").exists())
        self.assertFalse((old / no.MARKER).exists())

    def test_never_writes_over_an_existing_nas_folder(self):
        make(self.scratch / "old", {"a.mov": MB}, age_h=100)
        today = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).date().isoformat()
        prior = self.nas / no.NAS_ARCHIVE / "mini-tmp-scratch" / today / "old"
        make(prior, {"keep.mov": MB})
        before = (prior / "keep.mov").read_bytes()
        rep = self.run_offload()
        self.assertTrue(rep["moved"][0]["nas"].endswith("old__2"))
        self.assertEqual((prior / "keep.mov").read_bytes(), before)
        self.assertEqual(sorted(x.name for x in prior.iterdir()), ["keep.mov"])

    def test_dry_run_changes_nothing(self):
        make(self.scratch / "old", {"a.mov": MB}, age_h=100)
        rep = self.run_offload(apply=False)
        self.assertEqual(len(rep["would"]), 1)
        self.assertTrue((self.scratch / "old" / "a.mov").exists())
        self.assertFalse((self.nas / no.NAS_ARCHIVE / "mini-tmp-scratch").exists())

    def test_system_folders_and_moved_markers_are_skipped(self):
        make(self.scratch / "com.apple.launchd.x", {"a": MB}, age_h=100)
        moved = self.scratch / "done_before"
        moved.mkdir()
        (moved / no.MARKER).write_text("x")
        self.assertEqual(no.candidates(self.scratch, 48, 0, time.time()), [])

    def test_daytime_waits_for_the_nas_window_without_touching_the_nas(self):
        old = self.scratch / "old"
        make(old, {"a.mov": MB}, age_h=100)
        self.free_mb = 15 * 1024  # under the 20 GB target, over the 8 GB day floor
        (self.nas / no.NAS_ARCHIVE).rmdir()  # any NAS check would now report it missing
        rep = self.run_offload(hour=14)
        self.assertIn("window", rep["wait"])
        self.assertEqual((rep["moved"], rep["kept"], rep["nas"]), ([], [], "ok"))
        self.assertTrue((old / "a.mov").exists())
        self.assertIn("01:00-06:00", no.summary(rep))
        self.assertEqual(len(self.run_offload(apply=False, hour=14)["would"]), 1)  # a dry run still lists

    def test_daytime_runs_when_the_mini_is_nearly_full(self):
        make(self.scratch / "old", {"a.mov": MB}, age_h=100)
        self.free_mb = 5 * 1024
        self.assertEqual(len(self.run_offload(hour=14)["moved"]), 1)

    def test_a_second_offload_waits_for_the_first(self):
        make(self.scratch / "old", {"a.mov": MB}, age_h=100)
        with open(pathlib.Path(self.tmp.name) / "offload.lock", "a") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
            rep = self.run_offload()
        self.assertIn("already running", rep["wait"])
        self.assertTrue((self.scratch / "old" / "a.mov").exists())

    def test_a_retry_updates_its_own_failed_copy_instead_of_a_new_one(self):
        old = self.scratch / "J1468-wt"
        make(old, {"a.mov": 2 * MB, "sub/b.wav": MB}, age_h=100)
        failed = self.day_dir() / "J1468-wt"  # an earlier attempt that died part way: no SHA256SUMS.txt
        make(failed, {"a.mov": 1000, ".b.wav.lcUxeW1q9y": 0})
        rep = self.run_offload()
        self.assertEqual(rep["moved"][0]["nas"], str(failed), rep)
        self.assertEqual((failed / "a.mov").stat().st_size, 2 * MB)
        self.assertEqual(sorted(x.name for x in self.day_dir().iterdir()), ["J1468-wt"])
        self.assertEqual(sorted(x.name for x in old.iterdir()), [no.MARKER])

    def test_a_verified_copy_is_never_written_into(self):
        make(self.scratch / "old", {"a.mov": MB}, age_h=100)
        done = self.day_dir() / "old"
        make(done, {"a.mov": 10})
        (done / no.SUMS).write_text("x  a.mov\n")
        rep = self.run_offload()
        self.assertTrue(rep["moved"][0]["nas"].endswith("old__2"), rep)
        self.assertEqual((done / "a.mov").stat().st_size, 10)
        with self.assertRaises(RuntimeError):
            no.copy_tree(self.scratch / "old", done)

    def test_scheduled_short_keep_paths_includes_explicit_and_uploads(self):
        keep = no.scheduled_short_keep_paths()
        for rel in no.SCHEDULED_SHORT_KEEP_PATHS:
            self.assertIn(rel, keep)


if __name__ == "__main__":
    unittest.main()
