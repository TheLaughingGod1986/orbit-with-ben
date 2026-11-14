#!/usr/bin/env python3
"""J2427 (Ben, 8 Nov 2026: "The 8 that passed, what is left to schedule these?"). A cut Ben OK'd whose upload or swap is
already recorded in UPLOADS.json leaves Passed: it shows as scheduled (or drops out when the video has its own card or
aired over a day ago). Cases are the real ones from 8 Nov: S6 Titan v11 = ffYKoNVPoqg, AR1 v06 = 93JL_IK57EM (the UAT
copy's _PHONE suffix), 031 Short 1 = C8lPx5N2DwM (own card), Apophis v13 -> v13a gJwNJN_yMKU (only id in the result).

board_check must treat those settled ask/approved entries as satisfied (no false FAIL for a missing Ready/Approved
card) while still flagging a genuinely missing card or a dead Play link."""
from __future__ import annotations

import datetime as dt
import sys
import unittest
from board_site import site_url
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import board_check  # noqa: E402
import jobs as J  # noqa: E402
import video_tracker as vt  # noqa: E402
import channel_pins  # noqa: E402

# These tests hand the board History of Science's films as one pipeline document. They are about that shape, so
# they say so, whatever the real channel does this week (J2622).
PIN = channel_pins.one_file("hos")


def setUpModule():
    PIN.start()


def tearDownModule():
    PIN.stop()

NOW = dt.datetime(2026, 11, 9, 9, 0, tzinfo=dt.timezone.utc)
URL = site_url() + "/api/watch?v=x&e=1&s=y"

FILES = {
    "file": {
        "owb_sa_s6_titan_v11.mp4": {"videoId": "ffYKoNVPoqg", "kind": "short", "publishAt": "2026-11-10T11:30:00.000Z", "privacyStatus": "private"},
        "owb_ar1_2024_yr4_moon_v06.mp4": {"videoId": "93JL_IK57EM", "kind": "short", "publishAt": "2026-11-27T11:30Z", "privacyStatus": "private"},
        "031_short_testA_opening_flip_v01.mp4": {"videoId": "C8lPx5N2DwM", "kind": "short", "publishAt": "2026-12-05T11:30:00Z", "privacyStatus": "private"},
        "unscheduled_v02.mp4": {"videoId": "AAAAAAAAAAA", "kind": "short", "publishAt": "", "privacyStatus": "private"},
    },
    "id": {},
}
FILES["id"] = {r["videoId"]: r for r in FILES["file"].values()}
FILES["id"]["gJwNJN_yMKU"] = {"videoId": "gJwNJN_yMKU", "kind": "short", "publishAt": "2026-11-20T11:30:00Z", "privacyStatus": "private"}
FILES["id"]["VBaYRPp85Sw"] = {"videoId": "VBaYRPp85Sw", "kind": "long", "publishAt": "", "privacyStatus": "public"}


def job(jid, status="done", **kw):
    return {"id": jid, "status": status, "title": "x", "body": "", "repo": "owb", "needs": "mini", "history": [], **kw}


def asked(jid, file, version, number, airs):
    j = job(jid)
    J.do_awaits(j, "chief", NOW, what=f"watch {file}", file=f"OWB UAT/{file}", version=version, due="2026-11-06 20:00",
                airs=airs, title=file, number=number, vtype="short")
    return j


def ok(jid, version):
    return {f"OWB-{jid}": {"verdict": "ok", "version": version, "at": "2026-11-05T22:07:31Z", "handled": False}}


def build(jobs, checks, videos_extra=None, files=FILES):
    asks = vt.ask_entries(jobs)
    for e in asks:
        e["watch"] = {"url": URL}
    appr = vt.approved_entries(jobs)
    for e in appr:
        e["watch"] = {"url": URL}
    owb = videos_extra or []
    return {v["key"]: v for v in vt.build_videos(
        hos={"films": []}, owb=owb, briefs={}, jobs=[j for j in jobs if j["status"] in vt.LIVE_STATUSES], checks=checks,
        uploads={}, overrides={}, now=NOW, public={}, titles={}, asks=asks, approved=appr, alljobs=jobs, watch={},
        files=files)["videos"]}


class UploadedOkLeavesPassed(unittest.TestCase):
    def test_titan_ok_with_recorded_upload_is_scheduled(self):
        v = build([asked("J1199", "owb_sa_s6_titan_v11.mp4", "v11", "", "2026-11-10 11:30")], ok("J1199", "v11"))["OWB:ASK:J1199"]
        self.assertEqual(v["lane"], "done")
        self.assertEqual(v["youtube"]["videoId"], "ffYKoNVPoqg")
        self.assertEqual(v["youtube"]["state"], "scheduled")
        self.assertNotIn("approved", v)

    def test_phone_copy_name_matches_the_upload(self):
        v = build([asked("J1356", "owb_ar1_2024_yr4_moon_v06_PHONE.mp4", "v06", "", "2026-11-27 11:30")], ok("J1356", "v06"))["OWB:ASK:J1356"]
        self.assertEqual((v["lane"], v["youtube"]["videoId"]), ("done", "93JL_IK57EM"))

    def test_without_an_upload_it_stays_passed(self):
        v = build([asked("J2426", "owb_ar2_iss_v13.mp4", "v13", "", "2026-11-25 11:30")], ok("J2426", "v13"))["OWB:ASK:J2426"]
        self.assertEqual(v["lane"], "approved")

    def test_unscheduled_upload_stays_passed(self):
        v = build([asked("J2500", "unscheduled_v02.mp4", "v02", "", "2026-11-25 11:30")], ok("J2500", "v02"))["OWB:ASK:J2500"]
        self.assertEqual(v["lane"], "approved")

    def test_ask_card_dropped_when_the_video_has_its_own_card(self):
        j = asked("J2395", "031_short_testA_opening_flip_v01.mp4", "v01", "031", "2026-12-05 11:30")
        own = {"key": "OWB:031:S:C8lPx5N2DwM", "lane": "done", "youtube": {"videoId": "C8lPx5N2DwM", "state": "scheduled"}}
        asks = vt.ask_entries([j])
        videos = [own]
        checks = ok("J2395", "v01")
        vt.add_asks(videos, asks, checks, NOW, FILES)
        self.assertEqual([v["key"] for v in videos], ["OWB:031:S:C8lPx5N2DwM"])

    def test_done_swap_found_by_the_one_live_id_in_its_result(self):
        j = job("J0974", approved_from={"job": "J0974", "what": "swap Apophis Short to v13", "file": "OWB UAT/030_apophis_short_v13_PHONE.mp4",
                                         "version": "v13", "airs": "2026-11-20T11:30Z", "type": "short", "number": "030"},
                result="Delivered v13a gJwNJN_yMKU Private + 2026-11-20T11:30Z; old BbsyFrV8kCY Private unscheduled. Related VBaYRPp85Sw reopened.")
        j["history"] = [{"at": "2026-10-26T09:00Z", "by": "mini", "what": "done: delivered"}]
        v = build([j], {})["OWB:OK:J0974"]
        self.assertEqual((v["lane"], v["youtube"]["videoId"]), ("done", "gJwNJN_yMKU"))

    def test_aired_ok_card_drops_out(self):
        j = job("J0975", approved_from={"job": "J0975", "file": "OWB UAT/owb_sa_s6_titan_v11.mp4", "version": "v11",
                                         "airs": "2026-11-10T11:30Z", "type": "short"}, result="uploaded")
        later = NOW + dt.timedelta(days=3)
        appr = vt.approved_entries([j])
        videos: list = []
        vt.add_approved(videos, appr, {}, later, FILES)
        self.assertEqual(videos, [])

    def test_two_live_ids_of_the_same_kind_are_not_guessed(self):
        e = {"file": "x.mp4", "type": "short"}
        self.assertIsNone(vt.matched_upload(e, FILES, "ffYKoNVPoqg and 93JL_IK57EM"))


class BoardCheckSettledUpload(unittest.TestCase):
    """False positives after settle_uploaded: ask/approved keys gone, card in Done or dropped."""

    def setUp(self):
        self.orig = board_check.file_on_mini
        board_check.file_on_mini = lambda rel: True

    def tearDown(self):
        board_check.file_on_mini = self.orig

    def site(self, url, follow=True):
        return 302 if not follow else 200

    def test_done_ask_card_without_ask_key_is_ok(self):
        # J1356.1: settle_uploaded left OWB:ASK:J1356.1 in Done with youtube scheduled, ask popped.
        # Empty files so satisfaction is the Done card key, not matched_upload.
        j = asked("J1356", "owb_ar1_2024_yr4_moon_v06_PHONE.mp4", "v06", "", "2026-11-27 11:30")
        J.do_awaits(j, "chief", NOW, what="watch AR1 v06b", file="OWB UAT/other_cut_v01.mp4",
                    version="v01", due="2026-11-06 20:00", airs="2026-11-27 11:30", title="AR1", add=True)
        card = {"key": "OWB:ASK:J1356.1", "lane": "done",
                "youtube": {"videoId": "93JL_IK57EM", "state": "scheduled", "publishAt": "2026-11-27T11:30Z"}}
        # Only the .1 card is Done; .2 has no upload and no card → still a real miss. Check .1 alone via cut_on_youtube.
        e1 = next(x for x in vt.ask_entries([j]) if x["id"] == "J1356.1")
        self.assertTrue(board_check.cut_on_youtube(e1, [card], files={}, card=None))
        res = board_check.check([j], {"checks": {}, "tracker": {"videos": [card]}}, site_status=self.site, files={})
        self.assertTrue(any("J1356.2: no card" in p for p in res["problems"]))
        self.assertFalse(any("J1356.1: no card" in p for p in res["problems"]))

    def test_matched_upload_satisfies_missing_ask_card(self):
        j = asked("J1356", "owb_ar1_2024_yr4_moon_v06_PHONE.mp4", "v06", "", "2026-11-27 11:30")
        res = board_check.check([j], {"checks": {}, "tracker": {"videos": []}}, site_status=self.site, files=FILES)
        self.assertTrue(res["ok"], res["problems"])

    def test_genuine_missing_ask_card_still_fails(self):
        j = asked("J2426", "owb_ar2_iss_v13.mp4", "v13", "", "2026-11-25 11:30")
        res = board_check.check([j], {"checks": {}, "tracker": {"videos": []}}, site_status=self.site, files={})
        self.assertFalse(res["ok"])
        self.assertTrue(any("J2426: no card on the published board" in p for p in res["problems"]))

    def test_approved_done_card_without_approved_key_is_ok(self):
        # J0974: settle moved OK card to Done and popped approved; result alone does not match read_back.
        j = job("J0974", approved_from={"job": "J0974", "what": "swap Apophis Short to v13",
                                         "file": "OWB UAT/030_apophis_short_v13_PHONE.mp4",
                                         "version": "v13", "airs": "2026-11-20T11:30Z", "type": "short"},
                result="Delivered v13a gJwNJN_yMKU Private + 2026-11-20T11:30Z; old BbsyFrV8kCY Private unscheduled.")
        j["history"] = [{"at": "2026-10-26T09:00Z", "by": "mini", "what": "done: delivered"}]
        card = {"key": "OWB:OK:J0974", "lane": "done",
                "youtube": {"videoId": "gJwNJN_yMKU", "state": "scheduled", "publishAt": "2026-11-20T11:30Z"}}
        # No UPLOADS match: Done card key alone must clear the approved check.
        res = board_check.check([j], {"checks": {}, "tracker": {"videos": [card]}}, site_status=self.site, files={})
        self.assertTrue(res["ok"], res["problems"])
        self.assertFalse(any("approved J0974" in p for p in res["problems"]))

    def test_approved_matched_upload_when_ok_card_dropped(self):
        j = job("J0974", approved_from={"job": "J0974", "what": "swap Apophis Short to v13",
                                         "file": "OWB UAT/030_apophis_short_v13_PHONE.mp4",
                                         "version": "v13", "airs": "2026-11-20T11:30Z", "type": "short"},
                result="Delivered v13a gJwNJN_yMKU Private + 2026-11-20T11:30Z; old BbsyFrV8kCY Private unscheduled.")
        j["history"] = [{"at": "2026-10-26T09:00Z", "by": "mini", "what": "done: delivered"}]
        # Job-keyed OK card dropped; matched_upload from the result id is enough (no Done stand-in required).
        res = board_check.check([j], {"checks": {}, "tracker": {"videos": []}}, site_status=self.site, files=FILES)
        self.assertTrue(res["ok"], res["problems"])

    def test_genuine_missing_approved_card_still_fails(self):
        j = job("J1100", status="open",
                approved_from={"job": "J1100", "what": "upload ISS short", "file": "OWB UAT/missing_cut_v01.mp4",
                               "version": "v01", "airs": "2026-11-25T11:30Z", "type": "short", "title": "ISS"})
        res = board_check.check([j], {"checks": {}, "tracker": {"videos": []}}, site_status=self.site, files={})
        self.assertFalse(res["ok"])
        self.assertTrue(any("approved J1100: no card in Approved, on its way" in p for p in res["problems"]))

    def test_ready_ask_still_flags_dead_play_link(self):
        j = asked("J2426", "owb_ar2_iss_v13.mp4", "v13", "", "2026-11-25 11:30")
        card = {"key": "OWB:ASK:J2426", "lane": "ready", "readyFor": "Ben", "ask": {"id": "J2426"},
                "watch": {"url": URL}}
        res = board_check.check([j], {"checks": {}, "tracker": {"videos": [card]}},
                                site_status=lambda url, follow=True: 500, files={})
        self.assertFalse(res["ok"])
        self.assertTrue(any("Play link answers 500" in p for p in res["problems"]))


if __name__ == "__main__":
    unittest.main()
