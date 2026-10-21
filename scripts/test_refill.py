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
            j.update(status="blocked", result="parked for Chief: x")
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

    def test_a_backlog_key_is_posted_at_most_once_a_day(self):
        d = empty()
        for i in range(2):
            j = jobs.do_add(d, title=f"r{i}", needs="mini", body="", by="refill", at=T0)
            j.update(status="blocked", result="parked for Chief: review", backlog="a")
            jobs.log(j, T0 + i * H, "cursor", "blocked: parked for Chief: review")
        self.assertEqual([j["title"] for j in refill.do_escalate(d, T0 + 3 * H)], ["r0"])
        self.assertEqual(refill.do_escalate(d, T0 + 10 * H), [])
        self.assertEqual([j["title"] for j in refill.do_escalate(d, T0 + 28 * H)], ["r1"])


class NeverEmpty(unittest.TestCase):
    def test_nothing_ready_adds_the_oldest_key_despite_cooldown(self):
        d = empty()
        refill.do_refill(d, ITEMS[:1], T0)
        d["jobs"][0]["status"] = "done"
        self.assertEqual(len(refill.do_refill(d, ITEMS[:1], T0 + H)), 1)  # cooldown waived: queue was empty

    def test_nothing_ready_and_every_key_busy_adds_nothing(self):
        d = empty()
        refill.do_refill(d, ITEMS[:2], T0)
        d["jobs"][0].update(status="blocked", result="parked for Chief: review")
        d["jobs"][1].update(status="blocked", result="Storage prerequisite: 7.8 GiB free")
        self.assertEqual(refill.do_refill(d, ITEMS[:2], T0 + 30 * H), [])

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


class OneLiveCopyPerKey(unittest.TestCase):
    """J0811: 16-21 Oct the refill added 28-30 copies of each of 15 keys, because a parked copy freed its key."""

    def later(self, status, result=""):
        d = empty()
        refill.do_refill(d, ITEMS[:1], T0)
        d["jobs"][0].update(status=status, result=result)
        jobs.do_add(d, title="pipeline", needs="cloud", body="", by="chief", at=T0)  # not Mini-ready
        return refill.do_refill(d, ITEMS[:1], T0 + 13 * H)  # past every_h, nothing ready

    def test_open_copy_holds_the_key(self):
        self.assertEqual(self.later("open"), [])

    def test_claimed_copy_holds_the_key(self):
        self.assertEqual(self.later("claimed"), [])

    def test_parked_for_chief_holds_the_key(self):
        self.assertEqual(self.later("blocked", "parked for Chief: script review"), [])

    def test_any_blocked_copy_holds_the_key(self):
        self.assertEqual(self.later("blocked", "Storage prerequisite: 7.8 GiB free"), [])

    def test_done_or_cancelled_frees_it_after_every_h(self):
        self.assertEqual(len(self.later("done", "PASS")), 1)
        self.assertEqual(len(self.later("cancelled", "duplicate")), 1)

    def test_daily_item_waits_for_yesterdays_blocked_copy(self):
        item = dict(Daily.ITEM)
        d = empty()
        day1 = dt.datetime(2026, 10, 13, 7, 0, tzinfo=dt.timezone.utc)  # 08:00 London
        self.assertEqual(len(refill.do_refill(d, [item], day1)), 1)
        d["jobs"][-1].update(status="blocked", result="parked for Chief: CTR readout")
        self.assertEqual(refill.do_refill(d, [item], day1 + 24 * H), [])


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
