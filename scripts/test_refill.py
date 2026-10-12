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


if __name__ == "__main__":
    unittest.main()
