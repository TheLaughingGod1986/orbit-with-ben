"""refill.py: the Mini never runs dry, and parked reviews escalate instead of sitting."""
import datetime as dt, pathlib, sys, unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jobs  # noqa: E402
import refill  # noqa: E402

T0 = dt.datetime(2026, 10, 12, 10, 0, tzinfo=dt.timezone.utc)
H = dt.timedelta(hours=1)
ITEMS = [{"key": k, "title": k, "needs": "mini", "body": "", "kind": "assembly", "every_h": 12} for k in "abcd"]


def empty():
    return {"next_id": 1, "jobs": []}


class Refill(unittest.TestCase):
    def test_tops_up_to_three_ready(self):
        d = empty()
        self.assertEqual(len(refill.do_refill(d, ITEMS, T0)), 3)
        self.assertEqual(len(refill.ready(d, T0)), 3)

    def test_parked_jobs_dont_count_as_ready_and_key_not_duplicated(self):
        d = empty()
        refill.do_refill(d, ITEMS, T0)
        for j in d["jobs"]:
            jobs.do_block(j, "cursor", "parked for Chief: x", T0) if j["status"] == "claimed" else None
            j["status"] = "blocked"
        added = refill.do_refill(d, ITEMS, T0 + H)
        self.assertEqual([d["jobs"][-1]["backlog"]], ["d"])
        self.assertEqual(len(added), 1)

    def test_cooldown(self):
        d = empty()
        refill.do_refill(d, ITEMS[:1], T0)
        d["jobs"][0]["status"] = "done"
        jobs.do_add(d, title="pipeline", needs="mini", body="", by="chief", at=T0)  # something is ready
        self.assertEqual(refill.do_refill(d, ITEMS[:1], T0 + H), [])
        self.assertEqual(len(refill.do_refill(d, ITEMS[:1], T0 + 13 * H)), 1)

    def test_backlog_file_is_valid(self):
        for it in refill.load_backlog():
            self.assertIn(it["needs"], jobs.NEEDS)
            self.assertIn(it["kind"], jobs.routing.KINDS)
            self.assertNotEqual(it["kind"], "video")  # backlog never spends on generation


class Escalate(unittest.TestCase):
    def test_escalates_once_after_stale_hours(self):
        d = empty()
        j = jobs.do_add(d, title="r", needs="mini", body="", by="chief", at=T0)
        j["status"] = "blocked"
        j["result"] = "parked for Chief: review"
        jobs.log(j, T0, "cursor", "blocked: parked for Chief: review")
        self.assertEqual(refill.do_escalate(d, T0 + H), [])
        self.assertEqual(len(refill.do_escalate(d, T0 + 3 * H)), 1)
        self.assertEqual(refill.do_escalate(d, T0 + 4 * H), [])


class NeverEmpty(unittest.TestCase):
    def test_nothing_ready_adds_the_oldest_key_despite_cooldown(self):
        d = empty()
        refill.do_refill(d, ITEMS[:1], T0)
        d["jobs"][0]["status"] = "done"
        self.assertEqual(len(refill.do_refill(d, ITEMS[:1], T0 + H)), 1)  # cooldown waived: queue was empty

    def test_parked_key_can_run_again(self):
        d = empty()
        refill.do_refill(d, ITEMS[:1], T0)
        d["jobs"][0]["status"] = "blocked"
        self.assertEqual(len(refill.do_refill(d, ITEMS[:1], T0 + H)), 1)

    def test_two_parked_hold_the_key_even_when_nothing_is_ready(self):
        d = empty()
        for t in (T0, T0 + H):
            refill.do_refill(d, ITEMS[:1], t)
            d["jobs"][-1].update(status="blocked", result="parked for Chief: review")
        self.assertEqual(refill.do_refill(d, ITEMS[:1], T0 + 30 * H), [])
        d["jobs"][0].update(status="done", result="Chief PASS")
        self.assertEqual(len(refill.do_refill(d, ITEMS[:1], T0 + 31 * H)), 1)

    def test_paused_item_is_never_added(self):
        d = empty()
        items = [dict(ITEMS[0], paused="pipeline full"), ITEMS[1]]
        refill.do_refill(d, items, T0)
        self.assertEqual({j["backlog"] for j in d["jobs"]}, {"b"})

    def test_backlog_has_weekly_audits_and_ideas_for_both_channels(self):
        keys = {it["key"]: it for it in refill.load_backlog()}
        for k in ("owb-weekly-audit", "hos-weekly-audit", "owb-ideas", "hos-ideas"):
            self.assertIn(k, keys)
        self.assertEqual(keys["owb-weekly-audit"]["every_h"], 168)
        for it in refill.load_backlog():
            self.assertNotIn(it["kind"], ("video", "vo"))  # never spends on generation or TTS


class Daily(unittest.TestCase):
    ITEM = {"key": "ctr", "title": "ctr", "needs": "mini", "body": "", "kind": "studio", "daily_at": "07:00"}

    def test_added_once_a_day_after_its_time_and_urgent(self):
        d = empty()
        early = dt.datetime(2026, 10, 13, 5, 30, tzinfo=dt.timezone.utc)   # 06:30 London
        self.assertEqual(refill.do_refill(d, [self.ITEM], early), [])
        late = early + H                                                      # 07:30 London
        added = refill.do_refill(d, [self.ITEM], late)
        self.assertEqual(len(added), 1)
        self.assertEqual(d["jobs"][-1]["urgent"], 0)
        d["jobs"][-1]["status"] = "done"
        self.assertEqual(refill.do_refill(d, [self.ITEM], late + 3 * H), [])  # same day: not again
        self.assertEqual(len(refill.do_refill(d, [self.ITEM], late + 24 * H)), 1)  # next day


class NoArbitraryHolds(unittest.TestCase):
    def test_no_start_time_can_be_set(self):
        d = empty()
        j = jobs.do_add(d, title="r", needs="mini", body="", by="chief", at=T0)
        with self.assertRaises(ValueError):
            jobs.do_schedule(j, "chief", "2026-10-12 15:00", T0, "Flow AI Ultra credit renews")
        with self.assertRaises(ValueError):
            jobs.do_add(d, title="x", needs="mini", body="", by="chief", at=T0, not_before="2026-10-12 15:00", reset="x")

if __name__ == "__main__":
    unittest.main()
