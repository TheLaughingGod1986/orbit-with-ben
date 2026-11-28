#!/usr/bin/env python3
"""J3266: under-pace raises only approved ready work; over-pace holds only low-priority work; a cap stops calls."""
import datetime as dt
import unittest

import plan_pace
import workflow_state as workflow

AT = dt.datetime(2026, 11, 21, 1, 0, tzinfo=dt.timezone.utc)
PLANS = {"subscriptions": [
    {"pools": ["elevenlabs"], "allowanceWindows": {"elevenlabs": {"verified": True, "end": "2026-11-30T10:50:31+00:00"}}},
    {"pools": ["claude"], "renews": "2026-12-08"},
]}


def job(i, **kw):
    row = {"id": i, "status": "open", "needs": "mini", "title": i, "created_at": "2026-11-20T00:00:00Z"}
    row.update(kw)
    return row


def state_for(pool, mode, spare=50000):
    return {"plans": {pool: {"id": pool, "state": mode, "spare": spare, "left": spare + plan_pace.ELEVENLABS_RESERVE}}}


class RaiseAndHold(unittest.TestCase):
    def tearDown(self):
        plan_pace.clear()

    def test_under_pace_raises_only_approved_ready_work(self):
        state = state_for("elevenlabs", "leftovers")
        parent = job("J0", status="done", kind="review", film="031")
        rows = [
            job("ready", kind="vo", film="031"),
            job("backlog", kind="vo", film="031", backlog="ideas"),
            job("blocked", kind="vo", film="031", status="blocked"),
            job("undated", kind="vo"),
            job("other", kind="assembly", film="031"),
            job("waiting", kind="vo", film="032", after="missing"),
            job("unblocked", kind="vo", film="032", after="J9"),
            parent,
            job("J9", status="done"),
            job("music", kind="vo", film="004", repo="ww2", title="WW2 score bed"),
            job("costly", kind="vo", film="033", title="Narration", body="about 9,500 credits"),
            job("dated", kind="vo", due="2026-12-01T18:00:00Z"),
            job("far", kind="vo", due="2027-02-01T18:00:00Z"),
        ]
        # The costly take does not fit once the spare is under 9,500.
        tight = state_for("elevenlabs", "leftovers", spare=4000)
        self.assertEqual(plan_pace.raised_ids(rows, state, AT), ["ready", "unblocked", "costly", "dated"])
        self.assertEqual(plan_pace.raised_ids(rows, tight, AT), ["ready", "unblocked", "dated"])
        self.assertNotIn("costly", plan_pace.raised_ids(
            [job("costly", kind="vo", film="033", body="about 9,500 credits")], tight, AT))
        self.assertIn("costly", plan_pace.raised_ids(
            [job("costly", kind="vo", film="033", body="about 9,500 credits")], state, AT))
        self.assertEqual(plan_pace.service_block(rows[9], AT), "no ElevenLabs music for WW2 in November")

    def test_over_pace_holds_only_low_priority_work(self):
        state = state_for("claude", "early_out")
        rows = [
            job("low", kind="script", film="031"),
            job("urgent", kind="script", film="031", urgent=1),
            job("soon", kind="script", film="031", due="2026-11-23T18:00:00Z"),
            job("voice", kind="vo", film="031"),
            job("later", kind="script", film="031", due="2027-01-01T18:00:00Z"),
        ]
        self.assertEqual(plan_pace.held_ids(rows, state, AT), ["low", "later"])
        self.assertTrue(plan_pace.blocks(rows[0], "claude", AT, rows, state))
        self.assertFalse(plan_pace.blocks(rows[0], "gemini", AT, rows, state))
        self.assertFalse(plan_pace.blocks(rows[1], "claude", AT, rows, state))
        self.assertFalse(plan_pace.blocks(rows[2], "claude", AT, rows, state))

    def test_queue_order_and_claim_follow_the_same_rules(self):
        plan_pace.use(state_for("elevenlabs", "leftovers"))
        voice = job("J1", kind="vo", film="031")
        other = job("J2", kind="assembly", film="031")
        self.assertLess(workflow.order(voice, {}, (), AT, (), {}, [voice, other]),
                        workflow.order(other, {}, (), AT, (), {}, [voice, other]))
        plan_pace.use(state_for("claude", "early_out"))
        low = job("J3", kind="script", film="031")
        urgent = job("J4", kind="script", film="031", urgent=1)
        rows = [low, urgent]
        self.assertFalse(workflow.claimable(low, rows, AT, "claude", ""))
        self.assertTrue(workflow.claimable(low, rows, AT, "gemini", ""))
        self.assertTrue(workflow.claimable(urgent, rows, AT, "claude", ""))
        plan_pace.clear()
        self.assertTrue(workflow.claimable(low, rows, AT, "claude", ""))


class ProjectionAndCaps(unittest.TestCase):
    def _rows(self, pool, start_left, end_left, total=121000):
        return [
            {"at": "2026-11-14T01:00:00Z", "kind": "record", "pool": pool, "left": start_left, "total": total},
            {"at": "2026-11-21T01:00:00Z", "kind": "record", "pool": pool, "left": end_left, "total": total},
        ]

    def test_seven_day_rate_lands_the_three_pace_states(self):
        flags = {}
        slow = plan_pace.compute(AT, self._rows("elevenlabs", 100000, 93000), PLANS, flags)
        el = slow["plans"]["elevenlabs"]
        self.assertEqual(el["state"], "leftovers")
        self.assertIn("on track to use", el["line"])
        self.assertIn("30 Nov", el["line"])
        self.assertLess(el["projectedPct"], 90)

        fast = plan_pace.compute(AT, self._rows("elevenlabs", 90000, 20000), PLANS, flags)
        burnt = fast["plans"]["elevenlabs"]
        self.assertEqual(burnt["state"], "early_out")
        self.assertTrue(burnt["line"].startswith("on track to use 100%"))

        # 7,000 used over 7 days, from 40,000 used up to 47,000 of 121,000, stays under a full month.
        steady = plan_pace.compute(AT, self._rows("elevenlabs", 81000, 40000), PLANS, flags)
        self.assertEqual(steady["plans"]["elevenlabs"]["state"], "on_track")
        self.assertRegex(steady["plans"]["elevenlabs"]["line"], r"on track to use \d+% by 30 Nov")

        self.assertEqual(slow["plans"]["vidiq"]["line"], "no reading yet")

    def test_weekly_note_uses_the_weekly_reset_not_the_five_hour_one(self):
        note = "5-hour 0% used (resets 13:12Z) session; weekly 22% used, resets Wed 25 Nov 00:17Z"
        rows = [
            {"at": "2026-11-18T12:00:00Z", "kind": "record", "pool": "gemini", "left": 95, "total": 100, "note": note},
            {"at": "2026-11-20T12:00:00Z", "kind": "record", "pool": "gemini", "left": 78, "total": 100, "note": note},
        ]
        plans = {"subscriptions": [{"pools": ["gemini"], "renews": "2026-12-12"}]}
        view = plan_pace.compute(AT, rows, plans, {})
        gemini = view["plans"]["gemini"]
        self.assertEqual(gemini["state"], "leftovers")
        self.assertIn("25 Nov", gemini["line"])
        self.assertLess(gemini["projectedPct"], 90)

    def test_one_reading_since_a_weekly_reset_counts_from_the_window_start(self):
        note = "weekly 15% used, resets Wednesday 10:00 AM"
        rows = [
            {"at": "2026-11-18T08:00:00Z", "kind": "record", "pool": "claude", "left": 30, "total": 100, "note": "weekly 70% used, resets Wednesday 10:00 AM"},
            {"at": "2026-11-20T08:00:00Z", "kind": "record", "pool": "claude", "left": 85, "total": 100, "note": note},
        ]
        view = plan_pace.compute(AT, rows, PLANS, {})
        claude = view["plans"]["claude"]
        self.assertEqual(claude["state"], "leftovers")
        self.assertIn("25 Nov", claude["line"])

    def test_a_credit_reading_without_a_total_keeps_the_last_total(self):
        rows = [
            {"at": "2026-11-13T01:00:00Z", "kind": "record", "pool": "flow", "left": 25050, "total": 25050},
            {"at": "2026-11-20T01:00:00Z", "kind": "record", "pool": "flow", "left": 23400},
        ]
        plans = {"subscriptions": [{"pools": ["flow"], "renews": "2026-12-12"}]}
        view = plan_pace.compute(AT, rows, plans, {})
        self.assertEqual(view["plans"]["flow"]["state"], "leftovers")
        self.assertLess(view["plans"]["flow"]["projectedPct"], 90)

    def test_a_pay_per_use_cap_stops_further_calls(self):
        unset = {"vertex": {"capGbp": None}, "vercel": {"capGbp": None}, "overage": {"capGbp": None}}
        self.assertTrue(plan_pace.allow("vertex", 0, unset)["stop"])
        self.assertFalse(plan_pace.allow("vertex", 0, unset)["ok"])
        capped = {"vertex": {"capGbp": 20}}
        under = plan_pace.allow("vertex", 5, capped)
        self.assertTrue(under["ok"] and not under["warning"] and not under["stop"])
        half = plan_pace.allow("vertex", 10, capped)
        self.assertTrue(half["ok"] and half["warning"] and not half["stop"])
        full = plan_pace.allow("vertex", 20, capped)
        self.assertTrue(full["stop"] and not full["ok"])
        view = plan_pace.compute(AT, [], {"subscriptions": []}, unset)
        self.assertTrue(all(cap["stop"] for cap in view["caps"]))
        self.assertIn("cap unset", view["caps"][0]["line"])
        self.assertIn("Ben:", view["proposal"])


if __name__ == "__main__":
    unittest.main()
