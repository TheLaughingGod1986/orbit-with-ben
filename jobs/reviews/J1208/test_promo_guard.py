import copy
import json
import os
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import promo_guard as g

NOW = datetime(2026, 11, 4, tzinfo=timezone.utc)
AT = NOW.isoformat()


def evidence():
    return {
        'credits': {'at': AT, 'account': g.ACCOUNT, 'vertex_eligible': True, 'rows': [
            {'id': 'monthly-1', 'type': 'CREDIT_TYPE_MONTHLY', 'status': 'Available', 'remaining_gbp': '10'},
            {'id': 'trial', 'type': 'Free Trial', 'status': 'Expired', 'remaining_gbp': '200'}]},
        'link': {'at': AT, 'project': g.PROJECT, 'account': g.ACCOUNT, 'enabled': True},
        'service': {'at': AT, 'project': g.PROJECT, 'model': g.MODEL, 'region': g.REGION, 'served': True},
        'price': {'at': AT, 'model': g.MODEL, 'region': g.REGION, 'resolution': '1080p', 'audio': False,
                  'currency': 'GBP', 'unit': 'second', 'per_second': '0.10', 'margin': '0.10',
                  'sku': 'test-sku', 'source_url': 'https://cloud.google.com/skus/'},
        'usage': {'at': AT, 'pending_since': '2026-11-01T00:00:00+00:00', 'all_projects_checked': True,
                  'source': 'verified billing usage cutoff fixture', 'unlogged_upper_bound_gbp': '0'},
        'duration': {s: {'source_seconds': 8, 'preroll': [0, 1.15], 'opening': [1.15, 3.85], 'reverse': False, 'speed': 1} for s in ('s5', 's6')},
        'ledger_sha256': g.digest([])}


class GuardTests(unittest.TestCase):
    def test_available_monthly_only(self):
        r = g.assess(evidence(), [], NOW)
        self.assertEqual(r['available_gbp'], '10')
        self.assertEqual(r['per_take_gbp'], '0.88')

    def test_rejects_missing_or_wrong_evidence(self):
        cases = [('link', 'account', 'other'), ('service', 'served', False),
                 ('credits', 'vertex_eligible', False), ('price', 'currency', 'USD'),
                 ('price', 'audio', True), ('price', 'margin', '0.01'),
                 ('usage', 'all_projects_checked', False), ('price', 'per_second', 'NaN'),
                 ('price', 'per_second', '0.30'), ('credits', 'at', '2026-11-03T23:54:59Z')]
        for section, key, value in cases:
            with self.subTest(section=section, key=key):
                e = evidence(); e[section][key] = value
                with self.assertRaises(g.Stop): g.assess(e, [], NOW)

    def test_used_and_duplicate_rows(self):
        e = evidence(); e['credits']['rows'][0]['status'] = 'Used'
        with self.assertRaises(g.Stop): g.assess(e, [], NOW)
        e = evidence(); e['credits']['rows'].append(copy.deepcopy(e['credits']['rows'][0]))
        with self.assertRaises(g.Stop): g.assess(e, [], NOW)

    def test_exact_reserve_boundary(self):
        e = evidence(); e['credits']['rows'][0]['remaining_gbp'] = '2.76'
        g.assess(e, [], NOW)
        e['credits']['rows'][0]['remaining_gbp'] = '2.75'
        with self.assertRaises(g.Stop): g.assess(e, [], NOW)

    def test_unpriced_legacy_pending_is_not_zero(self):
        rows = [{'at': AT, 'pool': 'vertex', 'kind': 'spend', 'amount': 0, 'what': 'Omni unpriced, billed late'}]
        with self.assertRaises(g.Stop): g.assess(evidence(), rows, NOW)

    def test_forward_duration_required(self):
        e = evidence(); e['duration']['s5']['reverse'] = True
        with self.assertRaises(g.Stop): g.assess(e, [], NOW)

    def test_atomic_reserve_reconcile_once_and_legacy_compatibility(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); lock = root / 'vertex.lock'; lock.mkdir(); (lock / 'owner.txt').write_text(f'pid={os.getpid()}\n')
            ledger = root / 'ledger.jsonl'; ledger.touch()
            with patch.object(g, 'LOCK_ROOT', lock.parent), patch.dict(os.environ, DESK_LOCK_HELD_DIR=str(lock)):
                g.reserve(ledger, evidence(), NOW)
                rows = [json.loads(x) for x in ledger.read_text().splitlines()]
                self.assertEqual(len(rows), 2)
                self.assertEqual(g.assess(evidence(), rows, NOW)['pending_gbp'], '1.76')
                # Restart never reserves a second set, even after balance refresh.
                e = evidence(); e['ledger_sha256'] = g.digest(rows)
                with self.assertRaises(g.Stop): g.reserve(ledger, e, NOW)
                self.assertEqual(len(ledger.read_text().splitlines()), 2)
                g.begin_take(ledger, e, 's5', NOW)
                g.reconcile(ledger, 'J1208:s5', None, NOW)
                with self.assertRaises(g.Stop): g.reconcile(ledger, 'J1208:s5', None, NOW)
                rows = [json.loads(x) for x in ledger.read_text().splitlines()]
                self.assertEqual(g.assess(evidence(), rows, NOW)['pending_gbp'], '1.76')
                # ai_spend's old normal-spend projection counts exactly once.
                self.assertAlmostEqual(sum(r['amount'] for r in rows if r['kind'] == 'spend'), 0.88)

    def test_missing_lock_and_changed_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / 'ledger'; ledger.touch()
            with patch.dict(os.environ, DESK_LOCK_HELD_DIR=tmp):
                with self.assertRaises(g.Stop): g.reserve(ledger, evidence(), NOW)
            lock = Path(tmp) / 'vertex.lock'; lock.mkdir(); (lock / 'owner.txt').write_text(f'pid={os.getpid()}\n')
            with patch.object(g, 'LOCK_ROOT', lock.parent), patch.dict(os.environ, DESK_LOCK_HELD_DIR=str(lock)):
                e = evidence(); e['ledger_sha256'] = 'stale'
                with self.assertRaises(g.Stop): g.reserve(ledger, e, NOW)
                self.assertEqual(ledger.read_text(), '')

    def test_actual_overrun_is_recorded_then_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); lock = root / 'vertex.lock'; lock.mkdir(); (lock / 'owner.txt').write_text(f'pid={os.getpid()}\n')
            ledger = root / 'ledger'; ledger.touch()
            with patch.object(g, 'LOCK_ROOT', lock.parent), patch.dict(os.environ, DESK_LOCK_HELD_DIR=str(lock)):
                g.reserve(ledger, evidence(), NOW)
                rows = [json.loads(x) for x in ledger.read_text().splitlines()]
                e = evidence(); e['ledger_sha256'] = g.digest(rows)
                g.begin_take(ledger, e, 's5', NOW)
                with self.assertRaises(g.Stop): g.reconcile(ledger, 'J1208:s5', '1.20', NOW)
                rows = [json.loads(x) for x in ledger.read_text().splitlines()]
                self.assertEqual(rows[-1]['amount'], 1.2)
                self.assertTrue(rows[-1]['budget_overrun'])
                with self.assertRaises(g.Stop): g.assess(evidence(), rows, NOW)

    def test_cutoff_cannot_skip_spend_after_balance(self):
        e = evidence(); e['usage']['pending_since'] = '2026-11-04T00:00:01Z'
        e['usage']['at'] = '2026-11-04T00:00:02Z'
        with self.assertRaises(g.Stop): g.assess(e, [], datetime(2026,11,4,0,0,2,tzinfo=timezone.utc))

    def test_unknown_kind_unreserved_job_and_malformed_evidence(self):
        for row in ({'pool': 'vertex', 'kind': 'unknown'},
                    {'pool': 'vertex', 'kind': 'spend', 'job': 'J1208', 'amount': 1, 'at': AT}):
            with self.assertRaises(g.Stop): g.assess(evidence(), [row], NOW)
        with self.assertRaises(g.Stop): g.assess({}, [], NOW)

    def test_crash_after_start_never_retries_but_s6_can_start_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); lock=root/'vertex.lock'; lock.mkdir(); (lock/'owner.txt').write_text(f'pid={os.getpid()}\n')
            ledger=root/'ledger'; ledger.touch()
            def fresh():
                e=evidence(); e['ledger_sha256']=g.digest([json.loads(x) for x in ledger.read_text().splitlines()]); return e
            with patch.object(g, 'LOCK_ROOT', root), patch.dict(os.environ, DESK_LOCK_HELD_DIR=str(lock)):
                g.reserve(ledger, fresh(), NOW)
                g.begin_take(ledger, fresh(), 's5', NOW)
                with self.assertRaises(g.Stop): g.begin_take(ledger, fresh(), 's5', NOW)
                with self.assertRaises(g.Stop): g.reconcile(ledger, 'J1208:s5', 0, NOW)
                g.reconcile(ledger, 'J1208:s5', None, NOW)
                self.assertEqual(g.begin_take(ledger, fresh(), 's6', NOW), 'J1208:s6')
                with self.assertRaises(g.Stop): g.begin_take(ledger, fresh(), 's6', NOW)

    def test_bad_owner_and_truncated_ledger_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); lock=root/'vertex.lock'; lock.mkdir(); owner=lock/'owner.txt'; owner.write_text('pid=999999999\n')
            ledger=root/'ledger'; ledger.write_text('{}')
            with patch.object(g, 'LOCK_ROOT', root), patch.dict(os.environ, DESK_LOCK_HELD_DIR=str(lock)):
                with self.assertRaises(g.Stop): g.reserve(ledger, evidence(), NOW)
                owner.write_text(f'pid={os.getpid()}\n')
                with self.assertRaises(g.Stop): g.reserve(ledger, evidence(), NOW)
                self.assertEqual(ledger.read_text(), '{}')
                with self.assertRaises(g.Stop): g.reserve(root/'missing', evidence(), NOW)
                self.assertFalse((root/'missing').exists())


if __name__ == '__main__': unittest.main()
