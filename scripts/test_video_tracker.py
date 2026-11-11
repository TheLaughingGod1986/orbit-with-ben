#!/usr/bin/env python3
"""Tests for the five-lane per-video Studio tracker (Ben, 24 Oct 2026)."""
from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import video_tracker as vt  # noqa: E402
import channel_pins  # noqa: E402

# These tests hand the board History of Science's films as one pipeline document. They are about that shape, so
# they say so, whatever the real channel does this week (J2622).
PIN = channel_pins.one_file("hos")


def setUpModule():
    PIN.start()


def tearDownModule():
    PIN.stop()

ROOT = Path(__file__).resolve().parents[1]
HOS_PIPE = Path("/tmp/hos-sparse/00_Brand/Channel-Setup/PIPELINE.json")


def live_fixture():
    if not HOS_PIPE.exists():
        raise unittest.SkipTest("HOS PIPELINE not at /tmp/hos-sparse (sparse-fetch it for integration checks)")
    from kanban_snapshot import release_record
    hos = json.loads(HOS_PIPE.read_text())
    owb = [json.loads(p.read_text()) for p in sorted((ROOT / "02_Video-Projects").glob("*/status.json"))]
    for film in owb:
        rec = release_record(str(film.get("film", "")))
        if rec:
            film["release"] = rec
    briefs = json.loads((ROOT / "05_Analytics" / "kanban" / "film_briefs.json").read_text())["films"]
    jobs = json.loads((ROOT / "jobs" / "queue.json").read_text())["jobs"]
    try:
        with urllib.request.urlopen("https://studio-kanban.vercel.app/api/checks", timeout=15) as r:
            checks = json.loads(r.read().decode()).get("checks") or {}
    except Exception as e:
        raise unittest.SkipTest(f"checks API unavailable: {e}")
    return vt.build_videos(hos=hos, owb=owb, briefs=briefs, jobs=jobs, checks=checks,
                           now=datetime(2026, 10, 24, 22, 0, tzinfo=timezone.utc))


class ParseNotes(unittest.TestCase):
    def test_recorded_watch_format_is_not_guessed_from_opaque_url_or_title(self):
        self.assertEqual(vt.watch_format({'file':'OWB UAT/030_apophis_short_v13a/030_apophis_short_v13a_PHONE.mp4'}),'short')
        self.assertEqual(vt.watch_format({'file':'project/10_Shorts/one/master.mp4'}),'short')
        self.assertEqual(vt.watch_format({'url':'https://example.test/short.mp4','title':'A Short'}),'')
        self.assertEqual(vt.watch_format({'file':'long_with_shorts_bumper.mp4'}),'')

    def test_project_watch_short_is_corrected_without_changing_deep_link_or_review(self):
        args=dict(key='OWB:030',channel='OWB',number='030',title='Apophis',vtype='long',air='',brief={},release=None,
                  upload_rows=[],jobs=[],check=None,watch={'file':'030_apophis_short_v13a_PHONE.mp4','version':'v13a','url':'https://example.test/watch'},
                  override_lane=None,now=datetime.now(timezone.utc))
        card=vt._card(**args)
        self.assertEqual((card['key'],card['checkId'],card['type']),('OWB:030','OWB-030','short'))
        self.assertTrue(card['cutFormatCorrected'])
        self.assertEqual(card['watch'],args['watch'])
        args.update(release={'videoId':'realLong000','state':'live'})
        self.assertEqual(vt._card(**args)['type'],'long','an unrelated watch link cannot relabel a known published video')

    def test_timecoded_list(self):
        notes = vt.parse_change_notes(
            "HOS 007 Vaccine: Ben's 3 changes\n"
            "(1) 0:38: the wooden figures look like they fall through the shelf.\n"
            "(2) 2:40: it should be a scratch, not a needle.\n"
            "(3) 4:22: arm artefact when the doctor places it.\n"
        )
        self.assertEqual([n["t"] for n in notes], ["0:38", "2:40", "4:22"])
        self.assertIn("shelf", notes[0]["text"])


class LaneRules(unittest.TestCase):
    def test_change_check_wins_over_open_fix_job(self):
        lane = vt.derive_lane(
            youtube=None,
            check={"verdict": "change", "fixes": [{"t": "0:38", "text": "shelf"}], "handled": False},
            jobs=[{"id": "J1", "status": "open", "title": "HOS 007 Vaccine: Ben's 3 changes on master v03"}],
            brief={"you": "Rewatch v03"},
        )
        self.assertEqual(lane, "changes")

    def test_ben_ok_with_release_jobs_is_progress(self):
        lane = vt.derive_lane(
            youtube=None,
            check={"verdict": "ok", "handled": False},
            jobs=[{"id": "J1", "status": "open", "title": "029 Betelgeuse: Private upload"}],
            brief={"you": "Rewatch v03b"},
        )
        self.assertEqual(lane, "progress")

    def test_scheduled_upload_is_done(self):
        lane = vt.derive_lane(
            youtube={"videoId": "F-jImX5h7ws", "state": "scheduled", "publishAt": "2026-11-29T18:00:00Z"},
            check={"verdict": "ok", "handled": False},
            jobs=[{"id": "J1", "status": "blocked", "title": "Studio finish"}],
            brief={},
        )
        self.assertEqual(lane, "done")

    def test_stuck_flag_when_ok_and_no_job(self):
        flags = vt.flags_for(
            key="OWB:029", lane="ready",
            check={"verdict": "ok", "handled": False},
            jobs=[], brief={"you": "Rewatch"},
            now=datetime(2026, 10, 24, tzinfo=timezone.utc),
        )
        self.assertTrue(any(f["kind"] == "stuck" for f in flags))

    def test_ok_note(self):
        note = vt.ok_note_for("progress", {"verdict": "ok", "version": "v03b", "at": "2026-10-23T22:44:31.887Z"})
        self.assertEqual(note, "You OK'd v03b on Fri 23 Oct. Nothing needed from you.")
        self.assertEqual(vt.ok_note_for("ready", {"verdict": "ok"}), "")
        self.assertEqual(vt.ok_note_for("progress", {"verdict": "change"}), "")


    def test_okd_brief_flag_is_chief_only(self):
        flags = vt.flags_for(key="OWB:029", lane="progress",
                             check={"verdict": "ok", "handled": False},
                             jobs=[{"id": "J1", "status": "open"}], brief={"you": "Watch v03b and OK."},
                             now=datetime.now(timezone.utc))
        self.assertTrue(flags)
        for f in flags:
            self.assertEqual(f.get("audience"), "chief", msg=f)
            self.assertNotIn("your OK", f["text"])


class CurrentApprovalBlocker(unittest.TestCase):
    def test_current_ruling_and_correction_replace_historical_failure(self):
        source={'id':'J0956','status':'blocked','after':'J0988',
                'approved_from':{'version':'v07','card':'OWB:S:Neptune'},
                'result':'Chief ruled: preserve v07 approval; correction queued as J0988.',
                'history':[{'at':'2026-10-26T18:00Z','what':'blocked: parked for Chief: old audio failure'}]}
        entry=vt.approved_entries([source])[0]
        self.assertNotIn('old audio failure',entry['blockedWhy'])
        state,line,warn=vt.approved_state(entry,{'J0988':{'id':'J0988','status':'open','title':'Neptune technical correction'}},datetime(2026,10,26,tzinfo=timezone.utc))
        self.assertEqual(state,'blocked')
        self.assertIn('J0988: Neptune technical correction',line)
        self.assertIn('Chief ruled',line)
        self.assertNotIn('old audio failure',warn)
        self.assertEqual(source['approved_from']['version'],'v07')


class RealYouTubeState(unittest.TestCase):
    """Board must match YouTube (Ben, 24 Oct 23:23): public read wins, old films and Shorts get real titles."""
    NOW = datetime(2026, 10, 24, 22, 0, tzinfo=timezone.utc)
    PUBLIC = {
        "GHZDsiH7L7A": {"channel": "HOS", "title": "What's Really Inside an Atom?", "format": "long", "publishedAt": "2026-10-15T17:00:00Z"},
        "_C92tIJCk8A": {"channel": "HOS", "title": "How Did We Discover Germs?", "format": "long", "publishedAt": "2026-09-03T17:00:00Z"},
        "h8HGfyShEHI": {"channel": "OWB", "title": "Is the Sun Getting Brighter?", "format": "long", "publishedAt": "2026-10-18T17:00:00Z"},
        "LCZRHUyTiq0": {"channel": "HOS", "title": "What Are Cathode Rays?", "format": "short", "publishedAt": "2026-10-23T10:30:00Z"},
    }

    def build(self, **kw):
        args = dict(
            hos={"films": [{"id": "004", "title": "What's Really Inside an Atom?", "air": "2026-10-15"}]},
            owb=[{"film": "022", "title": "Is the Sun Getting Brighter?", "air": "2026-10-18"},
                 {"film": "031", "title": "", "air": ""}],
            briefs={}, jobs=[], checks={}, now=self.NOW, public=self.PUBLIC,
            titles={"031": "What Happens When Earths Magnetic Field Flips"},
            uploads={"OWB:022": [{"videoId": "h8HGfyShEHI", "privacyStatus": "private", "publishAt": "2026-10-18T17:00:00Z"}]},
            overrides={"youtube": {"HOS:001": "_C92tIJCk8A"}},
        )
        args.update(kw)
        return {v["key"]: v for v in vt.build_videos(**args)["videos"]}

    def test_scheduled_that_aired_is_public_done(self):
        v = self.build()["OWB:022"]
        self.assertEqual((v["lane"], v["youtube"]["state"]), ("done", "live"))
        self.assertTrue(v["line"].startswith("Public on YouTube since"))

    def test_past_schedule_without_public_read_is_still_scheduled(self):
        v=self.build(public={})["OWB:022"]
        self.assertEqual((v["youtube"]["state"],v["youtube"]["privacy"]),("scheduled","private"))
        self.assertNotIn("bySchedule",v["youtube"])

    def test_title_match_moves_aired_hos_long_to_done(self):
        v = self.build()["HOS:004"]
        self.assertEqual((v["lane"], v["youtube"]["videoId"]), ("done", "GHZDsiH7L7A"))

    def test_forced_id_adds_missing_old_film(self):
        v = self.build()["HOS:001"]
        self.assertEqual((v["lane"], v["title"], v["number"]), ("done", "How Did We Discover Germs?", "001"))

    def test_untitled_film_gets_folder_title(self):
        self.assertEqual(self.build()["OWB:031"]["title"], "What Happens When Earths Magnetic Field Flips")

    def test_public_short_without_record_gets_one_card(self):
        by = self.build()
        shorts = [v for v in by.values() if v["shortId"] == "LCZRHUyTiq0"]
        self.assertEqual(len(shorts), 1)
        self.assertEqual(shorts[0]["title"], "What Are Cathode Rays?")

    # --- A Short that belongs to no film (J2515, 10 Nov 2026: the Titan Short that aired that day had no card) ---
    LONE = {"videoId": "LoneShort01", "kind": "short", "film": "", "channel": "OWB", "long": "",
            "file": "00_Brand/x/06_Final-Exports/owb_sa_s6_titan_v11.mp4", "packageDir": "00_Brand/x/owb_sa_s6_titan",
            "privacyStatus": "private", "publishAt": "2026-11-10T11:30:00Z",
            "title": "What Would Standing on Saturn's Moon Titan Feel Like?", "supersededBy": ""}

    def lone(self, **kw):
        key = vt.lone_short_key("OWB", "LoneShort01")
        out = self.build(uploads={key: [dict(self.LONE)]}, **kw)
        return key, [v for v in out.values() if (v.get("youtube") or {}).get("videoId") == "LoneShort01"
                     or v.get("shortId") == "LoneShort01"]

    def test_a_short_with_no_film_gets_exactly_one_card_before_it_airs(self):
        key, cards = self.lone()
        self.assertEqual(len(cards), 1)
        card = cards[0]
        self.assertEqual((card["key"], card["type"], card["channel"], card["number"]), (key, "short", "OWB", ""))
        self.assertEqual(card["title"], "What Would Standing on Saturn's Moon Titan Feel Like?")
        self.assertEqual((card["youtube"]["state"], card["youtube"]["privacy"]), ("scheduled", "private"))
        self.assertEqual(card["shortId"], "LoneShort01")
        self.assertFalse(card.get("parent"))

    def test_it_keeps_that_one_card_and_its_key_once_it_is_public(self):
        public = dict(self.PUBLIC, LoneShort01={"channel": "OWB", "title": "The Title On YouTube", "format": "short",
                                                "publishedAt": "2026-11-10T11:30:00Z"})
        key, cards = self.lone(public=public)
        self.assertEqual([c["key"] for c in cards], [key])       # not a second card from the public read
        self.assertEqual((cards[0]["youtube"]["state"], cards[0]["title"], cards[0]["lane"]),
                         ("live", "The Title On YouTube", "done"))

    def test_the_copy_a_swap_replaced_gets_no_card(self):
        key = vt.lone_short_key("OWB", "LoneShort01")
        old = dict(self.LONE, videoId="OldCopy0001", publishAt="", supersededBy="LoneShort01")
        out = self.build(uploads={key: [dict(self.LONE)], vt.lone_short_key("OWB", "OldCopy0001"): [old]})
        ids = [(v.get("youtube") or {}).get("videoId") for v in out.values()]
        self.assertIn("LoneShort01", ids)
        self.assertNotIn("OldCopy0001", ids)

    def test_a_job_that_names_its_video_id_is_on_its_card(self):
        job = {"id": "J9001", "status": "open", "needs": "mini", "title": "Swap the Titan Short LoneShort01 to v12"}
        key, cards = self.lone(jobs=[job])
        self.assertEqual(len(cards), 1)
        self.assertIn("J9001", json.dumps(cards[0]))

    def test_a_short_that_belongs_to_a_long_is_unchanged(self):
        upload = {"videoId": "FilmShort001", "kind": "short", "film": "022", "channel": "OWB",
                  "file": "x/10_Shorts/sun/022_short.mp4", "privacyStatus": "private",
                  "publishAt": "2026-11-30T11:30:00Z", "supersededBy": ""}
        out = self.build(uploads={"OWB:022:S:FilmShort001": [upload], vt.lone_short_key("OWB", "LoneShort01"): [dict(self.LONE)]})
        card = out["OWB:022:S:FilmShort001"]
        self.assertEqual((card["type"], card["parent"], card["number"]), ("short", "OWB:022", "022"))

    def test_the_register_gives_a_filmless_short_a_row_and_a_filmless_long_none(self):
        with tempfile.TemporaryDirectory() as t:
            reg = Path(t) / "00_Brand" / "Channel-Setup" / "social"
            reg.mkdir(parents=True)
            (reg / "UPLOADS.json").write_text(json.dumps({"videos": {
                "LoneShort01": {"kind": "short", "standalone": True, "title": "Titan", "privacyStatus": "private",
                                "publishAt": "2026-11-10T11:30:00Z", "packageDir": "00_Brand/x/owb_sa_s6_titan"},
                "LoneLong001": {"kind": "long", "packageDir": "00_Brand/x/owb_compilation"},
                "RetiredSh01": {"kind": "short", "retired": True, "packageDir": "00_Brand/x/old"},
            }}))
            idx = vt.uploads_index(Path(t))
        label = vt.channels.home_label()
        self.assertEqual(list(idx), [vt.lone_short_key(label, "LoneShort01")])
        row = idx[vt.lone_short_key(label, "LoneShort01")][0]
        self.assertEqual((row["film"], row["channel"], row["title"], row["publishAt"]),
                         ("", label, "Titan", "2026-11-10T11:30:00Z"))

    def test_ready_needs_a_playable_cut(self):
        by = self.build(
            hos={"films": [{"id": "009", "title": "Why Doesn't the Moon Fall to Earth?", "air": "2026-11-26"},
                           {"id": "006", "title": "Willow", "air": "2026-11-05"}]},
            briefs={"HOS:009": {"you": "Your final OK on Sun 22 Nov.", "youShort": "your final OK Sun 22 Nov", "youWhen": "2026-11-22"},
                    "HOS:006": {"you": "Watch v06 and OK it."}},
            watch={"HOS:006": {"url": "https://studio-kanban.vercel.app/api/watch?v=hos-006-v06", "version": "v06"}},
            jobs=[{"id": "J0862", "status": "blocked", "title": "HOS 009 + 010: Shorts voiceover from the v02 Shorts scripts, park for Chief", "taskKeys": ["HOS:009"]}],
            overrides={"jobFilms": {"J0862": ["HOS:009"]}},
        )
        self.assertEqual(by["HOS:009"]["lane"], "progress")
        self.assertTrue(by["HOS:009"]["line"].startswith("No cut to watch yet"))
        self.assertEqual(by["HOS:009"]["version"], "")  # v02 was the Shorts scripts, not a cut
        self.assertEqual((by["HOS:006"]["lane"], by["HOS:006"]["version"]), ("ready", "v06"))

    def test_short_slug_titles_are_clean(self):
        self.assertEqual(vt.clean_short_slug("friday_2026-10-16_last_star"), "Last star")
        self.assertEqual(vt.clean_short_slug("mon30_comets"), "Comets")
        self.assertEqual(vt.short_title_from_path({"file": "x/10_Shorts/wednesday_neutron_cover/a.mp4"}), "Neutron")


class PlannedShortsBacklog(unittest.TestCase):
    """Upcoming longs get cadence Short cards on Videos → Backlog (Ben, 7 Nov 2026)."""
    NOW = datetime(2026, 11, 7, 10, 0, tzinfo=timezone.utc)

    def build(self, **kw):
        args = dict(
            hos={"films": [
                {"id": "012", "title": "Why Alchemy Never Found Gold", "air": "2026-12-24"},
                {"id": "014", "title": "How We Measured the Speed of Light", "air": "2026-12-31"},
                {"id": "015", "title": "Who Invented the Telescope?", "air": "2027-01-07"},
                {"id": "018", "title": "Why Did Phlogiston Fail?", "air": "2027-01-14"},
                {"id": "009", "title": "Why Doesn't the Moon Fall to Earth?", "air": "2026-11-26"},
            ]},
            owb=[
                {"film": "033", "title": "Why Knocked-Sideways Uranus Has 21-Year Winters", "air": "2026-12-09"},
                {"film": "040", "title": "Wrong Kind Of Aliens", "air": ""},
                {"film": "050", "title": "Why Saturn's Moon Iapetus Is Half Black and White", "air": ""},
            ],
            briefs={}, jobs=[], checks={}, uploads={}, public={}, now=self.NOW,
        )
        args.update(kw)
        return vt.build_videos(**args)

    def test_hos_upcoming_longs_get_four_planned_shorts_each(self):
        # 009 is in production (jobs → progress); the four dated backlog longs stay upcoming.
        out = self.build(
            jobs=[{"id": "J1", "status": "open", "title": "HOS 009 script", "taskKeys": ["HOS:009"]}],
            overrides={"jobFilms": {"J1": ["HOS:009"]}},
        )
        shorts = [v for v in out["videos"] if v["type"] == "short" and v["channel"] == "HOS" and v["lane"] == "upcoming"]
        by_parent = {}
        for v in shorts:
            by_parent.setdefault(v["parent"], []).append(v)
        for key in ("HOS:012", "HOS:014", "HOS:015", "HOS:018"):
            self.assertEqual(len(by_parent.get(key) or []), 4, msg=key)
            for i, card in enumerate(sorted(by_parent[key], key=lambda c: c["key"]), 1):
                self.assertEqual(card["key"], f"{key}:S:planned-{i}")
                self.assertEqual(card["parent"], key)
                self.assertEqual(card["channel"], "HOS")
                self.assertFalse((card.get("youtube") or {}).get("videoId"))
                self.assertEqual(card.get("shortId") or "", "")
                self.assertTrue(card["title"].startswith(f"Short {i} · "))
        self.assertEqual(sum(len(v) for k, v in by_parent.items() if k.startswith("HOS:")), 16)
        self.assertNotIn("HOS:009", by_parent)

    def test_orbit_dated_and_undated_upcoming_each_get_two(self):
        # Regression: undated Orbit backlog longs must not drop back to long-only (Ben, 7 Nov 2026).
        out = self.build()
        owb_shorts = [v for v in out["videos"] if v["type"] == "short" and v["channel"] == "OWB"]
        by_parent = {}
        for v in owb_shorts:
            by_parent.setdefault(v["parent"], []).append(v)
        self.assertEqual(set(by_parent), {"OWB:033", "OWB:040", "OWB:050"})

        dated = by_parent["OWB:033"]
        self.assertEqual(len(dated), 2)
        self.assertEqual({c["key"] for c in dated}, {"OWB:033:S:planned-1", "OWB:033:S:planned-2"})
        self.assertTrue(all(c.get("air", "").startswith("2026-12-09") for c in dated))
        self.assertTrue(all(not (c.get("youtube") or {}).get("videoId") for c in dated))
        self.assertTrue(all(not (c.get("shortId") or "") for c in dated))

        for parent in ("OWB:040", "OWB:050"):
            cards = by_parent[parent]
            self.assertEqual(len(cards), 2, msg=parent)
            self.assertEqual({c["key"] for c in cards}, {f"{parent}:S:planned-1", f"{parent}:S:planned-2"})
            self.assertTrue(all((c.get("air") or "") == "" for c in cards), msg=parent)
            self.assertTrue(all(not (c.get("youtube") or {}).get("videoId") for c in cards))
            self.assertTrue(all(not (c.get("shortId") or "") for c in cards))

    def test_in_production_long_gets_no_planned_shorts(self):
        out = self.build(
            jobs=[{"id": "J1", "status": "open", "title": "HOS 009 script", "taskKeys": ["HOS:009"]}],
            overrides={"jobFilms": {"J1": ["HOS:009"]}},
        )
        by = {v["key"]: v for v in out["videos"]}
        self.assertEqual(by["HOS:009"]["lane"], "progress")
        self.assertFalse(any(v.get("parent") == "HOS:009" for v in out["videos"]))

    def test_uploaded_shorts_suppress_planned_placeholders(self):
        out = self.build(
            uploads={"OWB:033:S:AbCdEfGhIjK": [{
                "videoId": "AbCdEfGhIjK", "kind": "short", "film": "033", "channel": "OWB",
                "file": "x/10_Shorts/wed_uranus/a.mp4", "privacyStatus": "private",
                "publishAt": "2026-12-10T11:30:00Z", "supersededBy": "",
            }]},
        )
        planned = [v for v in out["videos"] if vt.is_planned_short_key(v["key"]) and v.get("parent") == "OWB:033"]
        self.assertEqual(planned, [])
        real = [v for v in out["videos"] if v.get("key") == "OWB:033:S:AbCdEfGhIjK"]
        self.assertEqual(len(real), 1)
        self.assertEqual(real[0]["shortId"], "AbCdEfGhIjK")

    def test_a_scheduled_short_shows_its_youtube_title_not_its_folder_name(self):
        # 10 Nov 2026: scheduled Shorts showed as "Scale" and "028 short mon30 comets". The public read only knows
        # public videos; the daily snapshot has every scheduled video's real title.
        upload = {"videoId": "SchedShort01", "kind": "short", "film": "028", "channel": "OWB",
                  "file": "x/10_Shorts/mon30_comets/028_short_mon30_comets.mp4", "privacyStatus": "private",
                  "publishAt": "2026-11-30T11:30:00Z", "supersededBy": ""}
        kw = dict(owb=[{"film": "028", "title": "Gliese 710", "air": ""}], uploads={"OWB:028:S:SchedShort01": [upload]})
        card = lambda out: next(v for v in out["videos"] if v["key"] == "OWB:028:S:SchedShort01")
        real = "Why Will Gliese 710's Comets Arrive After It Has Gone?"
        self.assertEqual(card(self.build(**kw, scheduled_titles={"SchedShort01": real}))["title"], real)
        self.assertNotEqual(card(self.build(**kw))["title"], real)   # no snapshot: the folder name, as before
        public = {"SchedShort01": {"title": "The Public Title", "channel": "OWB", "format": "short", "publishedAt": ""}}
        self.assertEqual(card(self.build(**kw, public=public, scheduled_titles={"SchedShort01": real}))["title"],
                         "The Public Title")   # once public, the public read wins

    def test_a_swap_card_takes_the_real_title_of_the_video_in_its_slot(self):
        # 10 Nov 2026: Ben's Schedule showed "Jenner smallpox test HC v04", the working name of a re-cut.
        slots = {("HOS", "2026-11-13T11:30", "short"): ["What Did Jenner's Smallpox Test Prove?"],
                 ("OWB", "2026-11-13T11:30", "short"): ["A", "B"]}
        card = {"key": "HOS:OK:J1219", "channel": "HOS", "type": "short", "title": "Jenner smallpox test HC v04",
                "youtube": {"state": "scheduled", "videoId": "", "publishAt": "2026-11-13T11:30Z"}}
        self.assertEqual(vt.title_from_slot(card, slots), "What Did Jenner's Smallpox Test Prove?")
        self.assertEqual(vt.title_from_slot({**card, "channel": "OWB"}, slots), "")   # two videos in the slot: no guess
        self.assertEqual(vt.title_from_slot({**card, "type": "long"}, slots), "")      # nothing scheduled then
        self.assertEqual(vt.title_from_slot({**card, "youtube": {"videoId": "abc", "publishAt": "2026-11-13T11:30Z"}}, slots), "")
        self.assertEqual(vt.title_from_slot({**card, "youtube": None}, slots), "")

    def test_snapshot_slots_list_what_youtube_has_scheduled(self):
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d) / "aaa" / "snapshots"
            folder.mkdir(parents=True)
            (folder / "2026-11-10.json").write_text(json.dumps({"videos": [
                {"id": "s1", "title": "Scheduled Short", "format": "short", "privacy": "private", "publishAt": "2026-11-13T11:30:00Z"},
                {"id": "p1", "title": "Public Short", "format": "short", "privacy": "public", "publishAt": None},
                {"id": "u1", "title": "Unscheduled", "format": "short", "privacy": "private", "publishAt": None}]}))
            with mock.patch.object(vt.channels, "slugs", lambda: ["aaa"]), \
                    mock.patch.object(vt.channels, "analytics_dir", lambda slug: Path(d) / slug), \
                    mock.patch.object(vt.channels, "label", lambda slug: "Aaa"):
                self.assertEqual(vt.snapshot_slots(), {("AAA", "2026-11-13T11:30", "short"): ["Scheduled Short"]})

    def test_snapshot_titles_come_from_each_channels_newest_snapshot(self):
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for slug, day, rows in (("aaa", "2026-11-09", [{"id": "old", "title": "Yesterday's"}]),
                                    ("aaa", "2026-11-10", [{"id": "s1", "title": "Scheduled One"}, {"id": "x"}]),
                                    ("bbb", "2026-11-10", [{"id": "s2", "title": "Second Channel"}])):
                folder = root / slug / "snapshots"
                folder.mkdir(parents=True, exist_ok=True)
                (folder / f"{day}.json").write_text(json.dumps({"videos": rows}))
            with mock.patch.object(vt.channels, "slugs", lambda: ["aaa", "bbb", "ccc"]), \
                    mock.patch.object(vt.channels, "analytics_dir", lambda slug: root / slug), \
                    mock.patch.object(vt.channels, "label", lambda slug: slug):
                self.assertEqual(vt.snapshot_titles(), {"s1": "Scheduled One", "s2": "Second Channel"})

    def test_undated_long_with_live_shorts_gets_no_planned_placeholders(self):
        # Older shipped films (e.g. 005 Last Star, 019 Andromeda) stay long-only for planned cards.
        out = self.build(
            owb=[
                {"film": "005", "title": "The Last Star In The Universe", "air": ""},
                {"film": "040", "title": "Wrong Kind Of Aliens", "air": ""},
            ],
            uploads={"OWB:005:S:LiveShort001": [{
                "videoId": "LiveShort001", "kind": "short", "film": "005", "channel": "OWB",
                "file": "x/10_Shorts/last_star/a.mp4", "privacyStatus": "public",
                "publishAt": "", "supersededBy": "",
            }]},
            public={"LiveShort001": {
                "title": "Last Star Short", "channel": "OWB", "format": "short",
                "publishedAt": "2026-01-15T12:00:00Z",
            }},
        )
        planned_005 = [v for v in out["videos"] if vt.is_planned_short_key(v["key"]) and v.get("parent") == "OWB:005"]
        planned_040 = [v for v in out["videos"] if vt.is_planned_short_key(v["key"]) and v.get("parent") == "OWB:040"]
        self.assertEqual(planned_005, [])
        self.assertEqual({c["key"] for c in planned_040}, {"OWB:040:S:planned-1", "OWB:040:S:planned-2"})
        self.assertTrue(all((c.get("air") or "") == "" for c in planned_040))

    def test_youtube_id_on_long_suppresses_planned_shorts(self):
        # Guard is independent of lane: even an upcoming-shaped parent with a YouTube id
        # must not sprout planned Short placeholders (older shipped films).
        videos = [{
            "key": "OWB:019", "channel": "OWB", "number": "019", "title": "Andromeda",
            "type": "long", "lane": "upcoming", "air": "",
            "youtube": {"videoId": "ojk-dfOpAmw", "state": "live"},
        }]
        vt.add_planned_shorts(videos, uploads={}, film_lanes={}, now=self.NOW)
        planned = [v for v in videos if vt.is_planned_short_key(v.get("key") or "")]
        self.assertEqual(planned, [])

    def test_script_title_wins_when_provided(self):
        # Direct helper: build path only uses generic titles unless titles_by_parent is wired later.
        self.assertEqual(vt.planned_short_title(1, "Titan", "Could You Strike a Match on Titan?"),
                         "Could You Strike a Match on Titan?")
        self.assertEqual(vt.planned_short_title(2, "Titan", ""), "Short 2 · Titan")


class LiveMapping(unittest.TestCase):
    """Real queue + checks as of the 24 Oct rebuild brief."""

    @classmethod
    def setUpClass(cls):
        cls.doc = live_fixture()
        cls.by = {v["key"]: v for v in cls.doc["videos"]}

    def test_vaccine_in_changes_with_three_notes(self):
        v = self.by["HOS:007"]
        self.assertEqual(v["lane"], "changes")
        self.assertGreaterEqual(len(v["notes"]), 3)
        times = {n["t"] for n in v["notes"]}
        self.assertTrue({"0:38", "2:40", "4:22"} <= times)

    def test_willow_in_changes(self):
        self.assertEqual(self.by["HOS:006"]["lane"], "changes")
        self.assertGreaterEqual(len(self.by["HOS:006"]["notes"]), 3)

    def test_gliese_done_private_scheduled_london(self):
        v = self.by["OWB:028"]
        self.assertEqual(v["lane"], "done")
        self.assertEqual(v["youtube"]["videoId"], "F-jImX5h7ws")
        self.assertIn("29 Nov", v["youtube"]["publishAtLondon"])
        self.assertIn("18:00", v["youtube"]["publishAtLondon"])

    def test_betelgeuse_flagged(self):
        v = self.by["OWB:029"]
        self.assertTrue(v["flags"], msg=v)
        kinds = {f["kind"] for f in v["flags"]}
        self.assertTrue(kinds & {"chief", "stuck", "deadline"})

    def test_okd_card_never_asks_ben(self):
        # Ben, 25 Oct 01:00: a red "Brief still asks for your OK" on OK'd 029 read as an ask.
        for v in self.by.values():
            if v["lane"] in ("ready", "changes"):
                continue
            ben_flags = [f for f in v["flags"] if f.get("audience") != "chief"]
            for text in [v["line"]] + [f["text"] for f in ben_flags]:
                self.assertNotRegex(text, r"(?i)your (final )?ok|asks for your|needs your|approve", msg=v["key"])
        for f in self.by["OWB:029"]["flags"]:
            if "brief" in f["text"].lower():
                self.assertEqual(f.get("audience"), "chief")


class FirstDayPanel(unittest.TestCase):
    """Ben, 10 Nov 2026: the first-day check's verdicts show on the board, from `launch_check.panel`."""
    NOW = datetime(2026, 11, 10, 18, 0, tzinfo=timezone.utc)

    def test_the_tracker_carries_the_panel_with_the_queue_it_was_given(self):
        import launch_check
        seen = {}

        def fake(now, queue):
            seen.update(now=now, queue=queue)
            return [{"id": "abc", "word": "Slow start"}]

        jobs = [{"id": "J1", "launch": "abc@6"}]
        with mock.patch.object(launch_check, "panel", fake):
            self.assertEqual(vt.first_day(jobs, self.NOW), [{"id": "abc", "word": "Slow start"}])
        self.assertEqual((seen["now"], seen["queue"]), (self.NOW, {"jobs": jobs}))

    def test_a_broken_panel_never_costs_the_board_its_videos(self):
        import launch_check
        with mock.patch.object(launch_check, "panel", side_effect=ValueError("bad record")), \
                mock.patch.object(vt.sys, "stderr", io.StringIO()) as err:
            self.assertEqual(vt.first_day([], self.NOW), [])
        self.assertIn("first-day panel not built: bad record", err.getvalue())

    def test_the_board_document_has_the_panel(self):
        import launch_check
        with mock.patch.object(launch_check, "panel", lambda now, queue: [{"id": "abc"}]):
            doc = vt.build_from_docs({}, {}, {})
        self.assertEqual(doc["firstDay"], [{"id": "abc"}])
        self.assertIn("videos", doc)



class PastNotes(unittest.TestCase):
    """Ben, 8 Nov 2026: a re-sent cut lists what he flagged last time."""
    NOW = datetime(2026, 11, 9, tzinfo=timezone.utc)

    def test_a_change_on_an_older_version_shows_under_the_new_cut(self):
        old = {"verdict": "change", "version": "v02", "at": "2026-11-08T10:42:51Z",
               "fixes": [{"t": "", "text": "like a rectangle and blurry above and below"}]}
        self.assertEqual(vt.past_notes((old, "v03")),
                         [{"version": "v02", "at": "2026-11-08T10:42:51Z",
                           "notes": [{"t": "", "text": "like a rectangle and blurry above and below"}]}])
        self.assertEqual(vt.past_notes((old, "v02")), [], "the cut still being fixed isn't a past problem")
        self.assertEqual(vt.past_notes(({"verdict": "ok", "version": "v01"}, "v03")), [])

    def test_a_fix_job_under_its_own_id_carries_the_old_notes_via_prev(self):
        checks = {"OWB-J2395.3": {"verdict": "change", "version": "v02", "at": "2026-11-08T10:42:51Z",
                                  "fixes": [{"t": "", "text": "blurry above and below"}]}}
        card = vt.apply_ask({"key": "OWB:ASK:J2418", "title": "Short 2"},
                            {"id": "J2418", "job": "J2418", "jobStatus": "blocked", "what": "Watch 031 Short 2 v03",
                             "file": "OWB UAT/x.mp4", "version": "v03", "channel": "OWB", "prev": ["OWB-J2395.3"],
                             "fixed": ["Rebuilt full-screen 1080x1920"]}, checks, self.NOW)
        self.assertEqual(card["pastNotes"][0]["notes"][0]["text"], "blurry above and below")
        self.assertEqual(card["fixedNotes"], ["Rebuilt full-screen 1080x1920"])


if __name__ == "__main__":
    unittest.main()
