"""Temporary ledgers only: report writers must share the exporter's lock."""
import contextlib
import fcntl
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import ai_spend


class WriterTests(unittest.TestCase):
    def append(self, target, row=None):
        with patch.object(ai_spend, 'LEDGER', target), contextlib.redirect_stdout(io.StringIO()):
            ai_spend.append(row or {'kind': 'spend', 'pool': 'flow', 'amount': 100}, False)

    def test_append_preserves_export_receipts_and_fsyncs_file_and_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'ledger.jsonl'
            receipt = {'id': 'flow:spend:take1', 'kind': 'spend', 'pool': 'flow', 'amount': 100}
            target.write_text(json.dumps(receipt)+'\n')
            with patch.object(ai_spend.os, 'fsync', wraps=os.fsync) as sync:
                self.append(target)
                self.assertEqual(sync.call_count, 2)
            rows = [json.loads(line) for line in target.read_text().splitlines()]
            self.assertEqual(rows[0], receipt)
            self.assertEqual(len(rows), 2)

    def test_recovered_old_receipt_does_not_replace_latest_balance(self):
        rows = [
            {'at':'2026-11-07T10:00:00Z','kind':'record','pool':'flow','left':9000},
            {'at':'2026-11-06T10:00:00Z','kind':'record','pool':'flow','left':10000},
            {'at':'2026-11-06T10:00:00Z','kind':'spend','pool':'flow','amount':100,'film':'HOS:009'},
        ]
        doc = ai_spend.build_doc(rows)
        self.assertEqual(doc['pools']['flow']['latest']['left'], 9000)
        self.assertEqual(doc['pools']['flow']['spent_logged'], 100)
        self.assertEqual(doc['pools']['flow']['series'][-1][1], 9000)

    def test_corrupt_or_duplicate_receipts_never_append(self):
        fixtures = [b'{', b'{bad}\n', b'null\n', b'{"id":"same"}\n{"id":"same"}\n']
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'ledger.jsonl'
            for data in fixtures:
                target.write_bytes(data)
                with self.assertRaises(ValueError): self.append(target)
                self.assertEqual(target.read_bytes(), data)
            target.write_text('{"id":"same"}\n')
            before = target.read_bytes()
            with self.assertRaises(ValueError): self.append(target, {'id':'same'})
            self.assertEqual(target.read_bytes(), before)

    def test_exporter_destination_lock_blocks_cli_even_through_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); target = root/'ledger.jsonl'; target.touch()
            alias = root/'alias.jsonl'; alias.symlink_to(target)
            # The exporter uses this exact resolved destination lock path.
            with target.with_name(target.name+'.lock').open('a+') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                code = ('import sys; from pathlib import Path; import ai_spend; '
                        'ai_spend.LEDGER=Path(sys.argv[1]); '
                        'ai_spend.append({"kind":"spend","pool":"flow","amount":100},False)')
                probe = subprocess.run([sys.executable, '-c', code, str(alias)],
                                       cwd=Path(ai_spend.__file__).parent, capture_output=True, text=True)
                self.assertNotEqual(probe.returncode, 0)
                self.assertIn('BlockingIOError', probe.stderr)
                self.assertEqual(target.read_bytes(), b'')
            self.append(alias)
            self.assertEqual(len(target.read_text().splitlines()), 1)
            self.assertFalse(alias.with_name(alias.name+'.lock').exists())


if __name__ == '__main__': unittest.main()
