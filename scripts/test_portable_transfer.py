"""Filesystem-only transfer tests. No worker, publishing or generation calls."""
import copy
import datetime as dt
import hashlib
import pathlib
import tempfile
import unittest

import portable_transfer as transfer

T = dt.datetime(2026, 11, 4, tzinfo=dt.timezone.utc)


class Transfer(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.source = self.root / "source"
        self.source.mkdir()
        (self.source / "approved.txt").write_bytes(b"approved")
        self.rows = [dict(path="approved.txt", sha256=hashlib.sha256(b"approved").hexdigest())]
        self.contract = dict(inputs=self.rows, outputs=["approved.txt"], approval_ref="scope")
        self.args = dict(job="J1834", reservation="unique-123", host="registered-laptop",
                         direction="input", at=T, max_bytes=100)

    def receipt(self, **kw):
        return transfer.make_receipt(self.contract, self.rows, self.source, **dict(self.args, **kw))

    def verify(self, receipt, **kw):
        return transfer.verify_receipt(receipt, self.contract, self.source, **dict(self.args, **kw))

    def test_copy_and_receipt_rehash_on_receiving_host(self):
        bundle = transfer.copy_verified(self.rows, self.source, self.root, max_bytes=8, max_files=1)
        self.assertEqual((bundle / "approved.txt").read_bytes(), b"approved")
        receipt = self.receipt()
        self.verify(receipt)
        (self.source / "approved.txt").write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            self.verify(receipt)

    def test_copy_never_overwrites_existing_source_or_bundle(self):
        first = transfer.copy_verified(self.rows, self.source, self.root, max_bytes=8, max_files=1)
        second = transfer.copy_verified(self.rows, self.source, self.root, max_bytes=8, max_files=1)
        self.assertNotEqual(first, second)
        self.assertEqual((self.source / "approved.txt").read_bytes(), b"approved")

    def test_bad_hash_and_byte_limit_remove_partial_bundle_only(self):
        for budget, digest in [(7, self.rows[0]["sha256"]), (8, "a" * 64)]:
            with self.subTest(budget=budget):
                rows = [dict(path="approved.txt", sha256=digest)]
                with self.assertRaises(ValueError):
                    transfer.copy_verified(rows, self.source, self.root, max_bytes=budget, max_files=1)
                self.assertEqual(list(self.root.iterdir()), [self.source])

    def test_file_budget_and_invalid_budgets(self):
        for budget, files in [(8, 0), (-1, 1), (True, 1)]:
            with self.assertRaises(ValueError):
                transfer.copy_verified(self.rows, self.source, self.root, max_bytes=budget, max_files=files)

    def test_manifest_traversal_normalization_duplicate_and_collision(self):
        for path in ["../secret", "/secret", "a/../secret", "a\\b", "a//b", "./a", ".", ""]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                transfer.manifest([dict(path=path, sha256="a" * 64)])
        for rows in [self.rows * 2, self.rows + [dict(path="approved.txt/child", sha256="b" * 64)]]:
            with self.assertRaises(ValueError):
                transfer.manifest(rows)

    def test_symlink_file_parent_and_root_rejected(self):
        (self.source / "link").symlink_to(self.source / "approved.txt")
        (self.source / "directory").symlink_to(self.source, target_is_directory=True)
        for path in ["link", "directory/approved.txt"]:
            with self.subTest(path=path), self.assertRaises(OSError):
                transfer.verify_files([dict(self.rows[0], path=path)], self.source, max_bytes=100)
        alias = self.root / "alias"
        alias.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(OSError):
            transfer.verify_files(self.rows, alias, max_bytes=100)
        with self.assertRaises(ValueError):
            transfer.copy_verified(self.rows, self.source, alias, max_bytes=100, max_files=1)

    def test_fifo_is_rejected_without_blocking(self):
        import os
        os.mkfifo(self.source / "pipe")
        with self.assertRaises(ValueError):
            transfer.verify_files([dict(self.rows[0], path="pipe")], self.source, max_bytes=100)

    def test_receipt_is_bound_to_job_host_reservation_direction_and_contract(self):
        receipt = self.receipt()
        for field, value in dict(job="J1841", reservation="other", host="mini", direction="output").items():
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.verify(receipt, **{field:value})
        self.contract["approval_ref"] = "changed"
        with self.assertRaises(ValueError):
            self.verify(receipt)

    def test_stale_future_and_forged_receipts(self):
        receipt = self.receipt()
        for when in [T - dt.timedelta(seconds=1), T + dt.timedelta(minutes=5)]:
            with self.assertRaises(ValueError):
                self.verify(receipt, at=when)
        forged = copy.deepcopy(receipt)
        forged["bytes"] = 9
        with self.assertRaisesRegex(ValueError, "byte count"):
            self.verify(forged)
        forged = copy.deepcopy(receipt)
        forged["files"] = []
        with self.assertRaisesRegex(ValueError, "approved contract"):
            self.verify(forged)

    def test_outputs_require_exact_scoped_paths_and_local_hashes(self):
        receipt = self.receipt(direction="output")
        self.verify(receipt, direction="output")
        self.contract["outputs"] = ["extra.txt"]
        with self.assertRaisesRegex(ValueError, "scoped output"):
            self.receipt(direction="output")

    def test_roundtrip_output_receipt_is_rehashed_after_return(self):
        laptop = transfer.copy_verified(self.rows, self.source, self.root, max_bytes=8, max_files=1)
        receipt = transfer.make_receipt(self.contract, self.rows, laptop,
                                       **dict(self.args, direction="output"))
        returned = transfer.copy_verified(receipt["files"], laptop, self.root, max_bytes=8, max_files=1)
        transfer.verify_receipt(receipt, self.contract, returned, **dict(self.args, direction="output"))
        (returned / "approved.txt").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            transfer.verify_receipt(receipt, self.contract, returned, **dict(self.args, direction="output"))


if __name__ == "__main__":
    unittest.main()
