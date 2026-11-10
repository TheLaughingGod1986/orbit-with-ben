#!/usr/bin/env python3
"""No new personal email address in a tracked file. Both repos are public (security pass, 9 Nov 2026).

On 10 Nov 2026 a search found Google account addresses in 46 tracked files here: run evidence that recorded which
account a browser was signed in to, plate boards copied from a template that named it, old hand-over notes. They are
public and stay public until Ben decides what to do about them. This test stops the number growing.

`email_ratchet.json` lists the files that already contain one. The rules:
  - a file not on the list must contain none. Write "the studio Ultra account", the channel name or "Ben's account";
  - a listed file that no longer contains one must come off the list (`--lower` does it), so a clean-up stays clean;
  - the list never grows by hand. If a new file truly must carry an address, that is Ben's call, not a worker's.

Only personal mail domains count (Gmail, Outlook, iCloud and the like). `noreply@anthropic.com`, `press@nasa.gov` and
other organisation addresses do not.

    python3 scripts/test_email_ratchet.py            # the test
    python3 scripts/test_email_ratchet.py --report   # the files that contain one today (paths only, never the address)
    python3 scripts/test_email_ratchet.py --lower    # drop listed files that are now clean; never adds one
"""
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
LIST = HERE / "email_ratchet.json"
DOMAINS = "gmail|googlemail|outlook|hotmail|live|icloud|yahoo|protonmail|proton"
# One pattern for git grep (extended regex) and for Python.
PATTERN = rf"[A-Za-z0-9._%+-]+@({DOMAINS})\.(com|me|co\.uk)"
ADDRESS = re.compile(PATTERN)


def files_with_an_address(root: pathlib.Path = ROOT) -> list[str]:
    """Tracked text files under `root` that contain a personal address. Paths only."""
    done = subprocess.run(["git", "-C", str(root), "grep", "-lIE", PATTERN], capture_output=True, text=True)
    if done.returncode not in (0, 1):  # 1 means no match
        raise RuntimeError(f"git grep failed: {done.stderr.strip()}")
    return sorted(line for line in done.stdout.splitlines() if line)


def allowed() -> list[str]:
    return json.loads(LIST.read_text())["files"]


def judge(found: list[str], listed: list[str]) -> tuple[list[str], list[str]]:
    """(new files that must not have one, listed files that are now clean)."""
    return sorted(set(found) - set(listed)), sorted(set(listed) - set(found))


class WhatCounts(unittest.TestCase):
    def test_personal_mail_domains_count(self):
        for domain in ("gmail.com", "googlemail.com", "outlook.com", "icloud.com", "proton.me", "yahoo.co.uk"):
            self.assertTrue(ADDRESS.search("signed in as someone" + "@" + domain), domain)

    def test_organisation_addresses_and_links_do_not(self):
        for text in ("Co-Authored-By: Claude <noreply" + "@" + "anthropic.com>", "press" + "@" + "nasa.gov",
                     "https://www.icloud.com/iclouddrive/abc", "user@example.com", "@gmail.com with nothing before it"):
            self.assertFalse(ADDRESS.search(text), text)

    def test_only_tracked_files_are_searched(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            git = ["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@example.com"]
            subprocess.run(git + ["init", "-q"], check=True)
            (root / "evidence.json").write_text('{"account": "someone' + "@" + 'gmail.com"}\n')
            (root / "clean.md").write_text("the studio Ultra account\n")
            (root / "untracked.txt").write_text("other" + "@" + "gmail.com\n")
            subprocess.run(git + ["add", "evidence.json", "clean.md"], check=True)
            self.assertEqual(files_with_an_address(root), ["evidence.json"])


class Judge(unittest.TestCase):
    def test_a_new_file_is_named(self):
        self.assertEqual(judge(["a.json", "new.md"], ["a.json"]), (["new.md"], []))

    def test_a_cleaned_file_must_come_off_the_list(self):
        self.assertEqual(judge([], ["a.json"]), ([], ["a.json"]))


class Ratchet(unittest.TestCase):
    def test_no_new_file_has_an_address_and_the_list_is_current(self):
        new, clean = judge(files_with_an_address(), allowed())
        self.assertFalse(new, "\nThese files contain a personal email address and both repos are public. Write "
                              "\"the studio Ultra account\" (or the channel's name) instead:\n  " + "\n  ".join(new))
        self.assertFalse(clean, "\nThese files no longer contain an address. Lock that in with "
                                "`python3 scripts/test_email_ratchet.py --lower`:\n  " + "\n  ".join(clean))

    def test_the_list_holds_paths_only(self):
        self.assertFalse(ADDRESS.search(LIST.read_text()))
        self.assertEqual(allowed(), sorted(set(allowed())))


def write_list(files: list[str]) -> None:
    doc = json.loads(LIST.read_text()) if LIST.exists() else {}
    doc["_note"] = ("Files that already contained a personal email address on 10 Nov 2026. Paths only. This list may "
                    "only get shorter: scripts/test_email_ratchet.py refuses any file that is not on it.")
    doc["files"] = sorted(files)
    LIST.write_text(json.dumps(doc, indent=2) + "\n")


def main(argv) -> int:
    if "--report" in argv:
        found = files_with_an_address()
        print("\n".join(found))
        print(f"{len(found)} files", file=sys.stderr)
        return 0
    if "--lower" in argv or "--init" in argv:
        found = files_with_an_address()
        keep = found if "--init" in argv else sorted(set(found) & set(allowed()))
        write_list(keep)
        print(f"{len(keep)} files listed")
        return 0
    unittest.main(argv=[argv[0]] + [a for a in argv[1:] if not a.startswith("--")])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
