#!/usr/bin/env python3
"""The board's Channels section (Ben, 10 Nov 2026: "show what repos are plugged in ... and the ability that we can
just add another repo"): one card per registered channel, with the answer of channel_check.py."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import channel_cards  # noqa: E402
import channel_check  # noqa: E402
import channel_new  # noqa: E402
import channels  # noqa: E402


def third(tmp, **change):
    """A third channel made the way a real one is (channel_new.py), plugged into the registry for the test."""
    root = channel_new.create(Path(tmp), "night-sky", "SKY", "Night Sky", "@NightSky", 2)
    file = root / "studio" / "channel.json"
    c = json.loads(file.read_text())
    c.update(change)
    file.write_text(json.dumps(c, indent=2) + "\n")
    base = channels._load()
    return root, mock.patch.object(channels, "_load", lambda directory=None: base + (c,))


class Cards(unittest.TestCase):
    def test_every_registered_channel_gets_a_card_and_keeps_what_the_page_already_reads(self):
        cards = channel_cards.cards()
        self.assertEqual([c["slug"] for c in cards], channels.slugs())
        for c, registered in zip(cards, channels.all_channels()):
            self.assertEqual({k: c[k] for k in channel_cards.KEEP}, {k: registered.get(k) for k in channel_cards.KEEP})
            self.assertTrue(c["handle"].startswith("@"))
            self.assertRegex(c["repo"], r"^[\w.-]+/[\w.-]+$")
            self.assertIsInstance(c["wip"], int)
        # A channel whose files are on this machine: in the studio's root while it is the home channel, in its own
        # checkout once the studio and the channels are apart.
        own = next(c for c in cards if c["slug"] == channels.default())
        self.assertEqual((own["here"], own["ready"], own["must"]), (True, True, []))
        self.assertEqual(own["todo"], channel_check.check(channels.checkout(own["slug"]))[1][:channel_cards.MAX_LINES])
        self.assertEqual([c["slug"] for c in cards if c["home"]], [channels.home()] if channels.home() else [])

    def test_a_third_channel_made_by_folder_shows_up_ready_with_what_is_left(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, plugged = third(tmp)
            with plugged, mock.patch.dict(os.environ, {"SKY_REPO": str(root)}):
                cards = channel_cards.cards()
        sky = cards[-1]
        self.assertEqual(len(cards), len(channels.slugs()) + 1)
        self.assertEqual((sky["slug"], sky["label"], sky["name"], sky["handle"], sky["wip"]),
                         ("night-sky", "SKY", "Night Sky", "@NightSky", 2))
        self.assertEqual((sky["here"], sky["ready"], sky["must"]), (True, True, []))
        self.assertEqual(sky["repo"], "")                      # no GitHub address yet
        self.assertTrue(any("repo.url" in line for line in sky["todo"]))

    def test_a_channel_the_studio_cannot_drive_says_why(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, plugged = third(tmp, picture_route="anything")
            with plugged, mock.patch.dict(os.environ, {"SKY_REPO": str(root)}):
                sky = channel_cards.cards()[-1]
        self.assertEqual((sky["here"], sky["ready"]), (True, False))
        self.assertTrue(sky["must"])
        self.assertEqual(sky["todo"], [])

    def test_a_channel_that_is_not_on_this_machine_is_not_checked_and_is_not_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            _root, plugged = third(tmp)
            with plugged, mock.patch.dict(os.environ, {"SKY_REPO": str(Path(tmp) / "nowhere")}):
                sky = channel_cards.cards()[-1]
        self.assertEqual((sky["here"], sky["ready"], sky["must"], sky["todo"], sky["rules"]), (False, None, [], [], None))
        self.assertNotIn("error", sky)

    def test_one_channel_that_cannot_be_read_does_not_take_the_others_off_the_board(self):
        real = channel_check.check

        gone = channels.default()

        def check(root):
            if Path(root) == channels.checkout(gone):
                raise OSError("disk gone")
            return real(root)
        with mock.patch.object(channel_check, "check", check):
            cards = channel_cards.cards()
        self.assertEqual([c["slug"] for c in cards], channels.slugs())
        card = next(c for c in cards if c["slug"] == gone)
        self.assertEqual((card["ready"], card["error"]), (None, "disk gone"))
        self.assertEqual(card["name"], channels.get(gone)["name"])

    def test_the_repo_name_is_read_from_a_github_address(self):
        self.assertEqual(channel_cards.repo_name("https://github.com/someone/night-sky.git"), "someone/night-sky")
        self.assertEqual(channel_cards.repo_name("git@github.com:someone/night-sky.git"), "someone/night-sky")
        self.assertEqual(channel_cards.repo_name("https://github.com/someone/night-sky/"), "someone/night-sky")
        self.assertEqual(channel_cards.repo_name(""), "")
        self.assertEqual(channel_cards.repo_name(None), "")

    def test_the_publisher_reads_its_own_fresh_copy_not_the_working_checkout(self):
        # 10 Nov 2026: on the Mini the second channel read "not checked here". Its working checkout was not where the
        # card looked (a checkout can be on a job's branch, or behind). The publisher passes its own copies instead.
        with tempfile.TemporaryDirectory() as tmp:
            root, plugged = third(tmp)
            with plugged, mock.patch.dict(os.environ, {"SKY_REPO": str(Path(tmp) / "nowhere")}):
                self.assertIs(channel_cards.cards()[-1]["here"], False)
                sky = channel_cards.cards({"night-sky": root})[-1]
        self.assertEqual((sky["here"], sky["ready"]), (True, True))

    def test_the_publishers_copies_hold_what_the_check_looks_at(self):
        import board_publish
        for sparse in map(board_publish.sparse, channels.slugs()):
            self.assertIn("/studio/", sparse)
            for page in channel_check.GENERATED_PAGES:
                self.assertIn("/" + page, sparse)
            self.assertTrue(any(p.startswith("/studio-core/") for p in sparse))

    def test_room_for_another_channel_is_both_counts_added(self):
        counts = json.loads((Path(__file__).resolve().parent / "channel_ratchet.json").read_text())
        room = channel_cards.room()
        self.assertEqual(room["left"], counts["total"] + counts["home_total"])
        self.assertGreaterEqual(room["from"], room["left"])     # the count only falls

    def test_the_board_publisher_carries_the_cards(self):
        text = (Path(__file__).resolve().parent / "board_publish.py").read_text()
        self.assertIn('board["channels"] = channel_cards.cards(fresh)', text)
        self.assertIn('board["channelRoom"] = channel_cards.room()', text)
        # the plain names are set first, so a failure of the cards never loses a channel from the filters
        self.assertLess(text.index('for c in channels.all_channels()]'), text.index("channel_cards.cards(fresh)"))


if __name__ == "__main__":
    unittest.main()
