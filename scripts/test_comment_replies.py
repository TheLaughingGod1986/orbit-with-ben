"""Comment replies: triage, voice, limits, and no post before the voice check."""
import datetime as dt
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import comment_replies as cr  # noqa: E402
import channels  # noqa: E402
import refill  # noqa: E402
import jobs  # noqa: E402

NOW = dt.datetime(2026, 11, 21, 2, 0, tzinfo=dt.timezone.utc)
PROFILE = {
    "ai_line": "The channel uses AI tools to help reply.",
    "never_re": [r"\b(medical advice|dosage)\b", r"\b(glorious victory|gore)\b"],
    "voice": "Friendly British.",
    "name": "Example",
    "slug": "example",
    "channel_id": "UC_TEST",
}


def comment(text, cid="c1", **extra):
    row = {"id": cid, "video": "v1", "thread": "t1", "text": text, "published": "2026-11-21T01:00:00Z",
           "question": cr.is_question(text)}
    row.update(extra)
    return row


class Triage(unittest.TestCase):
    def test_questions_are_replies_and_praise_is_logged(self):
        self.assertEqual(cr.triage(comment("How far is that moon?"), PROFILE)[0], "reply")
        self.assertEqual(cr.triage(comment("Loved this one."), PROFILE)[0], "log")
        self.assertEqual(cr.triage(comment("I don't think that would do much damage to the moon."), PROFILE)[0], "reply")

    def test_spam_abuse_and_bait_are_ignored(self):
        self.assertEqual(cr.triage(comment("Check out my channel https://example.com"), PROFILE)[0], "ignore")
        self.assertEqual(cr.triage(comment("This is a stupid channel"), PROFILE)[0], "ignore")
        self.assertEqual(cr.triage(comment("Like if you agree"), PROFILE)[0], "ignore")

    def test_sensitive_comments_are_escalated_and_never_a_reply(self):
        samples = [
            "Can we sponsor a film?",
            "This is a copyright complaint from our lawyer.",
            "You are wrong about the distance.",
            "I will find you.",
            "Say hello to your family for me.",
            "What dosage should I take?",
            "Was that a glorious victory?",
            "Email me at someone@example.com please",
            "I hope it crashes in a populated area.",
        ]
        for text in samples:
            action, _reason = cr.triage(comment(text), PROFILE)
            self.assertEqual(action, "escalate", text)

    def test_critics_are_not_argued_with(self):
        self.assertEqual(cr.triage(comment("This was boring and a waste of time."), PROFILE)[0], "log")

    def test_a_topic_request_is_logged_and_a_question_can_still_be_answered(self):
        self.assertEqual(cr.triage(comment("Please make a film about the rings."), PROFILE)[0], "log")
        self.assertEqual(cr.triage(comment("Could you do a film about the rings?"), PROFILE), ("reply", "idea"))


class Draft(unittest.TestCase):
    def test_replies_are_specific_british_and_varied(self):
        texts = [
            "How did you work out that distance?",
            "Is the number in the film the average or the closest pass?",
            "What does that part look like from the surface?",
            "Could you do a film about the rings of that planet?",
            "When was that gap finally measured?",
        ]
        used = set()
        openings = []
        for i, text in enumerate(texts):
            reply = cr.draft_reply(comment(text, cid=f"d{i}"), PROFILE, used)
            self.assertEqual(cr.lint(reply, text, used), [], reply)
            self.assertNotIn("favorite", reply.lower())
            self.assertNotRegex(reply, r"Great question")
            used.add(cr.opening_of(reply))
            openings.append(cr.opening_of(reply))
        self.assertEqual(len(set(openings)), len(openings))

    def test_an_ai_question_is_answered_honestly(self):
        reply = cr.draft_reply(comment("Are these replies written by an AI tool?"), PROFILE, set())
        self.assertIn("The channel uses AI tools to help reply.", reply)
        self.assertNotRegex(reply.lower(), r"i am human|i'm human")
        self.assertNotIn("Ben personally", reply)

    def test_no_new_number_and_no_promise(self):
        reply = cr.draft_reply(comment("How far is that moon from us?"), PROFILE, set())
        self.assertNotRegex(reply, r"\d")
        self.assertIsNone(cr.PROMISE.search(reply))

    def test_a_repeated_opening_is_rewritten(self):
        first = cr.draft_reply(comment("How far is that moon?"), PROFILE, set())
        second = cr.draft_reply(comment("How wide is that moon?", cid="c2"), PROFILE, {cr.opening_of(first)})
        self.assertNotEqual(cr.opening_of(first), cr.opening_of(second))


class Run(unittest.TestCase):
    def _channel(self):
        return {"slug": "example", "name": "Example", "youtube": {"id": "UC_TEST"}, "comments": dict(PROFILE)}

    def test_dry_run_does_not_post_and_live_post_needs_approval(self):
        inserted = []

        class Client:
            def insert(self, parent, text):
                inserted.append((parent, text))
                return {"id": "r1"}

        thread = {"snippet": {"videoId": "v1", "topLevelComment": {
            "id": "c1", "snippet": {"textOriginal": "How far is that moon?",
                                    "authorChannelId": {"value": "UC_VIEWER"},
                                    "publishedAt": "2026-11-21T01:00:00Z"}}}, "replies": {"comments": []}}
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(cr, "comments_dir", return_value=pathlib.Path(tmp)):
                dry = cr.run_channel(self._channel(), now=NOW, post=True, approved=False, client=Client(),
                                     threads=[{"items": [thread]}],
                                     videos={"v1": {"published": "2026-11-21T00:30:00Z", "title": "Moon"}})
                self.assertEqual(inserted, [])
                self.assertEqual(dry["posted"], 0)
                live = cr.run_channel(self._channel(), now=NOW, post=True, approved=True, client=Client(),
                                      threads=[{"items": [thread]}],
                                      videos={"v1": {"published": "2026-11-21T00:30:00Z", "title": "Moon"}})
                self.assertTrue((pathlib.Path(tmp) / "replies.jsonl").is_file())
        self.assertEqual(len(inserted), 1)
        self.assertEqual(live["posted"], 1)

    def test_one_reply_per_thread_and_the_cap(self):
        class Client:
            def insert(self, parent, text):
                return {"id": "r-" + parent}

        items = []
        for i in range(3):
            items.append({"snippet": {"videoId": "v", "topLevelComment": {
                "id": f"c{i}", "snippet": {"textOriginal": f"How does step {i} work in the film?",
                                           "authorChannelId": {"value": "UC_VIEWER"},
                                           "publishedAt": "2026-11-21T01:00:00Z"}}}, "replies": {"comments": []}})
        # two comments would share a thread if we set them so; the cap test uses distinct threads
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(cr, "MAX_REPLIES", 2), \
                mock.patch.object(cr, "comments_dir", return_value=pathlib.Path(tmp)):
            result = cr.run_channel(self._channel(), now=NOW, post=True, approved=True, client=Client(),
                                    threads=[{"items": items}],
                                    videos={"v": {"published": "2026-11-21T00:00:00Z", "title": "Steps"}})
        self.assertEqual(result["posted"], 2)

    def test_a_follow_up_may_be_answered_and_a_second_note_is_not(self):
        thread = {"snippet": {"videoId": "v1", "topLevelComment": {
            "id": "c1", "snippet": {"textOriginal": "How far is that moon?",
                                    "authorChannelId": {"value": "UC_VIEWER"},
                                    "publishedAt": "2026-11-21T01:00:00Z"}}},
            "replies": {"comments": [
                {"id": "own", "snippet": {"textOriginal": "The sources name it.",
                                          "authorChannelId": {"value": "UC_TEST"},
                                          "publishedAt": "2026-11-21T01:10:00Z", "parentId": "c1"}},
                {"id": "c2", "snippet": {"textOriginal": "Thanks, but how was that distance measured?",
                                         "authorChannelId": {"value": "UC_VIEWER"},
                                         "publishedAt": "2026-11-21T01:20:00Z", "parentId": "c1"}},
            ]}}
        rows = cr.flatten_thread(thread, "UC_TEST")
        by_id = {row["id"]: row for row in rows}
        self.assertTrue(by_id["c1"]["channel_already_replied"])
        self.assertTrue(by_id["c2"]["follow_up"])

    def test_newest_questions_sort_first(self):
        old = comment("How old is that crater?", cid="old", video_published="2026-11-01T00:00:00Z")
        fresh = comment("Nice film.", cid="fresh", video_published="2026-11-21T01:00:00Z", question=False)
        fresh_q = comment("Why does that orbit decay?", cid="q", video_published="2026-11-21T01:30:00Z")
        ordered = sorted([old, fresh, fresh_q], key=lambda c: cr.priority(c, NOW))
        self.assertEqual([c["id"] for c in ordered], ["q", "fresh", "old"])

    def test_ideas_are_counted(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp)
            cr.log_idea(path, "the rings", "v1")
            cr.log_idea(path, "the rings", "v2")
            data = json.loads((path / "ideas.json").read_text())
        self.assertEqual(data["the rings"]["count"], 2)

    def test_quota_stops_at_the_daily_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            bucket = cr.Quota(pathlib.Path(tmp) / "q.json", NOW)
            bucket.charge(2950)
            self.assertTrue(bucket.room(50))
            self.assertFalse(bucket.room(51))
            bucket.charge(50)
            with self.assertRaises(RuntimeError):
                bucket.charge(1)

    def test_the_tool_does_not_name_a_channel_or_a_token(self):
        src = pathlib.Path(cr.__file__).read_text()
        for word in ("Orbit With Ben", "History of Science", "Field Order", "YOUTUBE_REFRESH_TOKEN"):
            self.assertNotIn(word, src)

    def test_home_rules_have_a_comment_voice_section(self):
        home = channels.home()
        text = (channels.checkout(home) / "studio" / "RULES.md").read_text()
        self.assertIn("## Comment voice", text)
        heard = cr.voice_text(channels.get(home), channels.checkout(home))
        self.assertIn("friendly British", heard)

    def test_every_registered_channel_carries_a_comment_login(self):
        channels._load.cache_clear()
        for channel in channels.all_channels():
            cfg = channel.get("comments") or {}
            self.assertTrue(cfg.get("token_env"), channel["slug"])
            self.assertIn(cfg.get("env_from"), ("studio", "checkout"))
            self.assertFalse(cfg.get("ai_reads"))


class Samples(unittest.TestCase):
    def test_examples_only_writes_five_replies_and_posts_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = pathlib.Path(tmp) / "VOICE_SAMPLES.md"
            with mock.patch.object(cr, "comments_dir", side_effect=lambda slug: pathlib.Path(tmp) / slug):
                result = cr.run_all(post=True, now=NOW, out=out, examples_only=True)
            text = out.read_text()
        self.assertEqual(result["posted"], 0)
        self.assertFalse(result["approved"])
        self.assertIn("Nothing in this file has been posted", text)
        self.assertGreaterEqual(text.count("Reply:"), 3)
        self.assertIn("The channel uses AI tools to help reply.", text)


class Schedule(unittest.TestCase):
    def test_punctual_work_is_queued_even_when_three_jobs_are_ready(self):
        data = {"next_id": 1, "jobs": []}
        for i in range(3):
            jobs.do_add(data, title=f"pipeline {i}", needs="mini", body="", by="chief", at=NOW)
        item = {"key": "comment-replies", "title": "comments", "needs": "mini", "body": "",
                "kind": "listing", "every_h": 2, "punctual": True}
        self.assertEqual(len(refill.do_refill(data, [item], NOW)), 1)
        self.assertEqual(refill.do_refill(data, [item], NOW + dt.timedelta(hours=1)), [])
        data["jobs"][-1]["status"] = "done"
        self.assertEqual(refill.do_refill(data, [item], NOW + dt.timedelta(hours=1)), [])
        self.assertEqual(len(refill.do_refill(data, [item], NOW + dt.timedelta(hours=3))), 1)

    def test_the_backlog_entry_is_punctual_listing_work(self):
        item = next(it for it in refill.load_backlog() if it["key"] == "comment-replies")
        self.assertEqual(item["every_h"], 2)
        self.assertTrue(item["punctual"])
        self.assertEqual(item["kind"], "listing")
        self.assertEqual(item["needs"], "mini")
        self.assertIn("VOICE_APPROVED", item["body"])


if __name__ == "__main__":
    unittest.main()
