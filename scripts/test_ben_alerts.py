#!/usr/bin/env python3
"""Tests for scripts/ben_alerts.py (J3292: direct urgent alerts to Ben).

Verifies:
  - Trigger (a): video airing within 24 h pulled, unscheduled or replaced (any channel) fires once,
    repeats once at half remaining time, never fires a third time, and stops when resolved/done.
  - Trigger (b): awaits_ben UAT watch with deadline within 12 h (any channel) fires once,
    repeats once at half remaining time, never fires a third time, and stops when ticked/done.
  - Combined pull + watch produces one plain-English London-time alert with board link.
  - Delivery: board red-banner payload + thread fallback when phone is unconfigured; ntfy push when configured
    locally without ever exposing the topic/secret in board output.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ben_alerts as ba  # noqa: E402


def utc(y, m, d, H, M=0, S=0) -> dt.datetime:
    return dt.datetime(y, m, d, H, M, S, tzinfo=dt.timezone.utc)


def watch_job(jid="J3274", *, repo="owb", film="024", status="blocked", title="Muons",
              version="v06", due="2026-11-21T10:45:00Z", airs="2026-11-21T11:30:00Z",
              vtype="short", card="", what="Watch the fixed cut"):
    entry = {
        "what": what,
        "file": "UAT/cut.mp4",
        "version": version,
        "due": due,
        "airs": airs,
        "title": title,
        "number": film,
        "type": vtype,
    }
    if card:
        entry["card"] = card
    return {"id": jid, "repo": repo, "film": film, "status": status, "title": what, "awaits_ben": entry}


class WatchTriggerTests(unittest.TestCase):
    def test_watch_fires_once_repeats_once_at_half_time_and_stops_when_done(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = Path(tmp) / "state.json"
            cfg = Path(tmp) / "config.json"
            sent_thread = []
            # Deadline 10:45Z; start at 04:45Z (6 h remaining -> midpoint repeat at 07:45Z).
            t0 = utc(2026, 11, 21, 4, 45)
            jobs = [watch_job(due="2026-11-21T10:45:00Z", airs="2026-11-21T11:30:00Z")]

            # First trigger -> fires once.
            r1 = ba.evaluate(at=t0, jobs=jobs, state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent_thread.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(len(r1["sent"]), 1)
            self.assertFalse(r1["sent"][0]["repeat"])
            self.assertEqual(len(r1["board"]["active"]), 1)
            self.assertEqual(r1["board"]["active"][0]["sendCount"], 1)
            self.assertIn("Muons Short", r1["sent"][0]["message"])
            self.assertIn("10:45", r1["sent"][0]["message"])
            self.assertIn("today's 11:30 slot", r1["sent"][0]["message"])
            self.assertIn("board.oppti.dev/#review", r1["sent"][0]["message"])
            self.assertEqual(len(sent_thread), 1)

            # Before half remaining time (07:44Z) -> does not fire again.
            r2 = ba.evaluate(at=utc(2026, 11, 21, 7, 44), jobs=jobs, state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent_thread.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(len(r2["sent"]), 0)
            self.assertEqual(len(r2["board"]["active"]), 1)

            # At half remaining time (07:45Z) -> repeats once.
            self.assertTrue(ba.has_due_work(utc(2026, 11, 21, 7, 45), state_file=st))
            r3 = ba.evaluate(at=utc(2026, 11, 21, 7, 45), jobs=jobs, state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent_thread.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(len(r3["sent"]), 1)
            self.assertTrue(r3["sent"][0]["repeat"])
            self.assertTrue(r3["sent"][0]["message"].startswith("Reminder:"))
            self.assertEqual(r3["board"]["active"][0]["sendCount"], 2)
            self.assertEqual(len(sent_thread), 2)

            # Later (09:30Z, 10:30Z) -> never sends a third time, banner stays until done.
            self.assertFalse(ba.has_due_work(utc(2026, 11, 21, 9, 30), state_file=st))
            r4 = ba.evaluate(at=utc(2026, 11, 21, 9, 30), jobs=jobs, state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent_thread.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(len(r4["sent"]), 0)
            self.assertEqual(len(r4["board"]["active"]), 1)

            # Job done / awaits_ben cleared -> stops and clears banner immediately.
            jobs_done = [{"id": "J3274", "repo": "owb", "film": "024", "status": "done", "title": "done"}]
            r5 = ba.evaluate(at=utc(2026, 11, 21, 9, 45), jobs=jobs_done, state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent_thread.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(len(r5["sent"]), 0)
            self.assertEqual(r5["board"]["active"], [])

    def test_watch_stops_before_repeat_when_ben_ticks_ok_or_job_finishes(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = Path(tmp) / "state.json"
            cfg = Path(tmp) / "config.json"
            sent = []
            t0 = utc(2026, 11, 21, 5, 0)
            jobs = [watch_job(jid="J9001", repo="hos", film="008", title="Franklin", version="v05",
                              due="2026-11-21T11:00:00Z", airs="2026-11-21T18:00:00Z", vtype="long", card="HOS:008")]

            r1 = ba.evaluate(at=t0, jobs=jobs, state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(len(r1["sent"]), 1)
            self.assertEqual(len(sent), 1)

            # Ben ticks OK at 06:00Z -> alert resolves; midpoint at 08:00Z must NOT fire a repeat.
            checks = {"HOS-008": {"verdict": "ok", "version": "v05", "at": "2026-11-21T06:00:00Z"}}
            r2 = ba.evaluate(at=utc(2026, 11, 21, 6, 0), jobs=jobs, checks=checks, state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(r2["board"]["active"], [])
            r3 = ba.evaluate(at=utc(2026, 11, 21, 8, 30), jobs=jobs, checks=checks, state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(len(r3["sent"]), 0)
            self.assertEqual(len(sent), 1)

    def test_watch_ignores_deadlines_over_12h_or_already_past(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = Path(tmp) / "state.json"
            cfg = Path(tmp) / "config.json"
            t0 = utc(2026, 11, 21, 6, 0)
            jobs = [
                watch_job(jid="J1", due="2026-11-21T18:01:00Z"),  # 12h 01m away -> too early
                watch_job(jid="J2", due="2026-11-21T05:59:00Z"),  # already past -> stale
            ]
            res = ba.evaluate(at=t0, jobs=jobs, state_file=st, config_file=cfg, notify_fn=lambda m: True)
            self.assertEqual(res["sent"], [])
            self.assertEqual(res["board"]["active"], [])


class PullTriggerTests(unittest.TestCase):
    def test_pulled_video_within_24h_fires_once_repeats_once_and_stops_when_done(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = Path(tmp) / "state.json"
            cfg = Path(tmp) / "config.json"
            sent = []
            # 1. Baseline snapshot: Short is scheduled for Sat 21 Nov 11:30Z.
            t_base = utc(2026, 11, 21, 3, 0)
            scheduled_videos = [{
                "key": "OWB:024:S:gc1hWQQJOq4", "channel": "OWB", "number": "024",
                "title": "Muons", "type": "short",
                "youtube": {"state": "scheduled", "videoId": "gc1hWQQJOq4", "publishAt": "2026-11-21T11:30:00Z", "privacy": "private"},
            }]
            r0 = ba.evaluate(at=t_base, videos=scheduled_videos, state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent.append(m) or True)
            self.assertEqual(r0["sent"], [])

            # 2. At 04:54Z, video is pulled (publishAt cleared, containment notes music_gate failure) and fixed watch armed for 10:45Z.
            t_pull = utc(2026, 11, 21, 4, 54)
            pulled_uploads = {
                "OWB": {
                    "gc1hWQQJOq4": {
                        "kind": "short", "title": "Muons", "privacyStatus": "private",
                        "publishAt": None, "unscheduledAt": "2026-11-21T04:54:00Z",
                        "containment": "J3273: publishAt cleared; music_gate 0.830 failed",
                    }
                }
            }
            watch_jobs = [watch_job(jid="J3274", repo="owb", film="024", title="Muons", version="v06",
                                    due="2026-11-21T10:45:00Z", airs="2026-11-21T11:30:00Z")]
            r1 = ba.evaluate(at=t_pull, jobs=watch_jobs, videos=[], uploads=pulled_uploads,
                             state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent.append(m) or True, site_url="https://board.oppti.dev")
            # Combined into ONE crisp alert (not duplicate pull + watch alerts).
            self.assertEqual(len(r1["sent"]), 1)
            msg = r1["sent"][0]["message"]
            self.assertEqual(
                msg,
                "Muons Short pulled (music failed a check). The fixed version needs your watch by 10:45 to keep today's 11:30 slot: board.oppti.dev/#review",
            )
            self.assertEqual(len(r1["board"]["active"]), 1)

            # 3. Before midpoint (~07:49:30Z): no repeat.
            r2 = ba.evaluate(at=utc(2026, 11, 21, 7, 0), jobs=watch_jobs, videos=[], uploads=pulled_uploads,
                             state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(r2["sent"], [])

            # 4. At midpoint (07:50Z): repeats ONCE.
            r3 = ba.evaluate(at=utc(2026, 11, 21, 7, 50), jobs=watch_jobs, videos=[], uploads=pulled_uploads,
                             state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(len(r3["sent"]), 1)
            self.assertTrue(r3["sent"][0]["repeat"])
            self.assertEqual(len(sent), 2)

            # 5. Later (09:30Z): NEVER fires a third time.
            r4 = ba.evaluate(at=utc(2026, 11, 21, 9, 30), jobs=watch_jobs, videos=[], uploads=pulled_uploads,
                             state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(r4["sent"], [])

            # 6. Replacement video is scheduled into the 11:30Z slot and watch job done -> alert clears.
            refilled_videos = [{
                "key": "OWB:024:S:2YiV_zDgLJg", "channel": "OWB", "number": "024",
                "title": "Muons", "type": "short",
                "youtube": {"state": "scheduled", "videoId": "2YiV_zDgLJg", "publishAt": "2026-11-21T11:30:00Z", "privacy": "private"},
            }]
            done_jobs = [{"id": "J3274", "repo": "owb", "film": "024", "status": "done", "title": "done"}]
            r5 = ba.evaluate(at=utc(2026, 11, 21, 9, 45), jobs=done_jobs, videos=refilled_videos,
                             uploads=pulled_uploads, state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(r5["sent"], [])
            self.assertEqual(r5["board"]["active"], [])

    def test_pull_outside_24h_and_normal_go_live_do_not_alert(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = Path(tmp) / "state.json"
            cfg = Path(tmp) / "config.json"
            sent = []
            t0 = utc(2026, 11, 21, 8, 0)
            videos = [
                {"key": "HOS:009", "channel": "HOS", "number": "009", "title": "Gravity", "type": "long",
                 "youtube": {"state": "scheduled", "videoId": "far123", "publishAt": "2026-11-23T18:00:00Z", "privacy": "private"}},
                {"key": "WW2:002", "channel": "WW2", "number": "002", "title": "Atlantic", "type": "long",
                 "youtube": {"state": "scheduled", "videoId": "live123", "publishAt": "2026-11-21T17:00:00Z", "privacy": "private"}},
            ]
            ba.evaluate(at=t0, videos=videos, state_file=st, config_file=cfg, notify_fn=lambda m: sent.append(m) or True)

            # far123 unscheduled (>24h away), live123 goes Public normally -> ZERO alerts.
            videos_after = [
                {"key": "WW2:002", "channel": "WW2", "number": "002", "title": "Atlantic", "type": "long",
                 "youtube": {"state": "live", "videoId": "live123", "publishAt": "2026-11-21T17:00:00Z", "privacy": "public"}},
            ]
            res = ba.evaluate(at=utc(2026, 11, 21, 17, 5), videos=videos_after, state_file=st, config_file=cfg,
                              notify_fn=lambda m: sent.append(m) or True)
            self.assertEqual(res["sent"], [])
            self.assertEqual(sent, [])

    def test_replaced_within_24h_on_third_channel_and_record_pull_job_stop(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = Path(tmp) / "state.json"
            cfg = Path(tmp) / "config.json"
            sent = []
            t0 = utc(2026, 11, 21, 6, 0)
            ba.record_pull(
                channel="WW2", video_id="abc999", title="Atlantic Black Pit", slot_at="2026-11-21T17:00:00Z",
                reason="audio failed a check", change="replaced", vtype="long", film="002", job="J8800",
                watch_due="2026-11-21T16:00:00Z", at=t0, state_file=st,
            )
            open_jobs = [{"id": "J8800", "repo": "ww2", "film": "002", "status": "open", "title": "fix"}]
            r1 = ba.evaluate(at=t0, jobs=open_jobs, state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(len(r1["sent"]), 1)
            self.assertIn("Atlantic Black Pit Long replaced", r1["sent"][0]["message"])
            self.assertIn("16:00", r1["sent"][0]["message"])

            # Linked job finishes before midpoint -> no repeat, banner clears.
            done_jobs = [{"id": "J8800", "repo": "ww2", "film": "002", "status": "done", "title": "fix"}]
            r2 = ba.evaluate(at=utc(2026, 11, 21, 12, 0), jobs=done_jobs, state_file=st, config_file=cfg,
                             notify_fn=lambda m: sent.append(m) or True, site_url="https://board.oppti.dev")
            self.assertEqual(r2["sent"], [])
            self.assertEqual(r2["board"]["active"], [])

    def test_explicit_uploads_unscheduled_metadata_detected_on_first_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = Path(tmp) / "state.json"
            cfg = Path(tmp) / "config.json"
            uploads = {
                "HOS": {
                    "vidX": {
                        "kind": "short", "title": "Franklin Kite", "privacyStatus": "private",
                        "publishAt": None,
                        "previousPublishAt": "2026-11-21T11:30:00Z",
                        "unscheduledAt": "2026-11-21T05:00:00Z",
                        "pullReason": "gate_shorts_open failed",
                    }
                }
            }
            res = ba.evaluate(at=utc(2026, 11, 21, 5, 5), uploads=uploads, state_file=st, config_file=cfg,
                              notify_fn=lambda m: True, site_url="https://board.oppti.dev")
            self.assertEqual(len(res["sent"]), 1)
            self.assertIn("Franklin Kite Short pulled (video failed a check)", res["sent"][0]["message"])


class DeliveryAndTimezoneTests(unittest.TestCase):
    def test_ntfy_delivery_uses_local_config_and_never_leaks_topic_in_board(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = Path(tmp) / "state.json"
            cfg = Path(tmp) / "config.json"
            secret_url = "https://ntfy.sh/private-random-topic-secret-999"
            cfg.write_text(json.dumps({"ntfyUrl": secret_url}))
            pushes = []
            threads = []
            jobs = [watch_job(due="2026-11-21T10:45:00Z", airs="2026-11-21T11:30:00Z")]

            res = ba.evaluate(
                at=utc(2026, 11, 21, 6, 0), jobs=jobs, state_file=st, config_file=cfg,
                notify_fn=lambda m: threads.append(m) or True,
                post_fn=lambda url, body, headers: pushes.append((url, body, headers)) or True,
                site_url="https://board.oppti.dev",
            )
            self.assertEqual(len(pushes), 1)
            self.assertEqual(pushes[0][0], secret_url)
            self.assertEqual(pushes[0][2]["Click"], "https://board.oppti.dev/#review")
            self.assertEqual(pushes[0][2]["Priority"], "high")
            self.assertEqual(len(threads), 1)
            self.assertTrue(res["board"]["phoneConfigured"])
            self.assertEqual(res["board"]["phoneRoute"], "ntfy")
            # Secret URL must never appear in board payload or persisted state.
            self.assertNotIn("private-random-topic-secret-999", json.dumps(res["board"]))
            self.assertNotIn("private-random-topic-secret-999", st.read_text())

    def test_bst_london_time_formatting(self):
        # July is BST (UTC+1): 09:45Z -> 10:45 London, 10:30Z -> 11:30 London.
        at = utc(2026, 7, 10, 6, 0)
        ev = {
            "kind": "watch", "title": "Muons", "type": "short", "channel": "OWB",
            "deadlineAt": "2026-07-10T09:45:00Z", "slotAt": "2026-07-10T10:30:00Z", "href": "#review",
        }
        full, _ = ba.format_message(ev, at, site_url="https://board.oppti.dev")
        self.assertIn("by 10:45", full)
        self.assertIn("today's 11:30 slot", full)


if __name__ == "__main__":
    unittest.main()
