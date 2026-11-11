#!/usr/bin/env python3
"""Check the board's film notes, run every test that reads them, then commit and push them to main.

    python3 scripts/notes_push.py --check             # the checks only; exit 1 on a problem, nothing written
    python3 scripts/notes_push.py -m "notes: 032 ..."  # the checks, then commit film_briefs.json and push to main

Why (10 Nov 2026): a notes push at 03:00Z removed one film's note and ran only `test_kanban_snapshot.py`. Another test
read that note and failed, so main was red until 04:25Z. Notes go straight to main (the Mini publishes the board within
a minute), so nothing else stands between a bad note and a red main. This script is that step.

What it checks:
  1. the file is valid JSON in the form the board expects (two-space indent, one final newline);
  2. `kanban_snapshot.load_briefs()` accepts it (film keys, UAT links);
  3. every film has the fields the board draws, a known mood, and every step says who, what and when;
  4. every test file under scripts/ that reads the notes passes. The list is found by searching the test files, so a
     new test that reads the notes is run without anyone adding it here. `SKIP` names the few that mention the file
     without reading the real one.

Only `05_Analytics/kanban/film_briefs.json` is committed. The push goes through `studio.git_transaction`, the same
path the job queue uses: from main, fast-forwarded first. If someone else changed the notes in the meantime the push
is refused and the edit is left in the working tree, so one writer never overwrites another.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
NOTES = ROOT / "05_Analytics" / "kanban" / "film_briefs.json"
REQUIRED = ("updated", "mood", "line", "done", "holdup", "steps")
MOODS = ("good", "waiting", "held", "finished", "watched", "fixing", "ready")
WHEN = ("done", "job", "afterJob", "when", "whenText")
READS_NOTES = ("film_briefs", "load_briefs")
ALWAYS = ("test_kanban_snapshot.py",)
# Name the notes file but never read the real one, so they cannot be broken by a notes push. Both are slow.
SKIP = {
    "test_notes_push.py": "this script's own test",
    "test_listing_deliver.py": "writes its own empty notes file in a temporary folder",
    "test_video_tracker.py": "reads the real notes only in a helper that needs the second channel's checkout; 2 minutes",
}


def canonical(data) -> str:
    return json.dumps(data, indent=2) + "\n"


def problems(text: str, routed=()) -> list[str]:
    """Everything wrong with the notes file's text; empty when it is fine. `routed`: step kinds that need no `who`."""
    try:
        data = json.loads(text)
    except ValueError as e:
        return [f"not valid JSON: {e}"]
    out = []
    if text != canonical(data):
        out.append("not in the board's form: write it with json.dumps(data, indent=2) + '\\n'")
    films = data.get("films") if isinstance(data, dict) else None
    if not isinstance(films, dict) or not films:
        return out + ["no 'films' object, or it is empty"]
    for key, note in films.items():
        missing = [k for k in REQUIRED if k not in note]
        if missing:
            out.append(f"{key}: missing {', '.join(missing)}")
            continue
        if note["mood"] not in MOODS:
            out.append(f"{key}: mood {note['mood']!r} is not one of {', '.join(MOODS)}")
        for n, step in enumerate(note["steps"], 1):
            if not ((step.get("who") or step.get("kind") in routed) and step.get("what")):
                out.append(f"{key} step {n}: needs who (or a routed kind) and what")
            if not any(step.get(k) for k in WHEN):
                out.append(f"{key} step {n} ({step.get('what', '?')}): needs one of {', '.join(WHEN)}")
    return out


def tests_that_read_notes(folder: pathlib.Path = HERE) -> list[pathlib.Path]:
    found = {folder / name for name in ALWAYS if (folder / name).exists()}
    for path in folder.glob("test_*.py"):
        if path.name in SKIP:
            continue
        text = path.read_text(errors="replace")
        if any(word in text for word in READS_NOTES):
            found.add(path)
    return sorted(found)


def run_tests(paths, runner=subprocess.run) -> list[str]:
    """Names of the test files that failed."""
    failed = []
    for path in paths:
        done = runner([sys.executable, str(path)], cwd=str(ROOT), capture_output=True, text=True)
        if done.returncode:
            failed.append(path.name)
            sys.stderr.write((done.stderr or done.stdout or "")[-3000:] + "\n")
    return failed


def check(notes: pathlib.Path = NOTES) -> list[str]:
    sys.path.insert(0, str(HERE))
    import kanban_snapshot

    found = problems(notes.read_text(), routed=tuple(kanban_snapshot.routing_doc()))
    if found:
        return found
    try:
        kanban_snapshot.load_briefs()
    except SystemExit as e:
        return [str(e)]
    failed = run_tests(tests_that_read_notes())
    return [f"test failed: {name}" for name in failed]


def push(message: str, studio=None, notes: pathlib.Path = NOTES) -> str | None:
    """None when pushed (or there is nothing to push); else why not. The edit is handed back uncommitted on failure."""
    if studio is None:
        sys.path.insert(0, str(HERE))
        import studio
    if not studio.git("status", "--porcelain", "--", str(notes)).stdout.strip():
        return None
    mine = notes.read_text()
    based_on = studio.git("show", f"HEAD:{notes.relative_to(ROOT).as_posix()}").stdout
    # git_transaction starts from a clean tree, so the edit is set aside and written back inside it.
    if studio.git("checkout", "-q", "--", str(notes)).returncode:
        return "could not set the notes file aside; nothing changed"

    def write():
        if notes.read_text() != based_on:
            return None, "the notes changed on main since this edit was made; redo the edit on the new main", []
        notes.write_text(mine)
        return None, None, [notes]

    err = studio.git_transaction(write, message)[1]
    if err:
        notes.write_text(mine)
    return err


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the checks only")
    ap.add_argument("-m", "--message", help="commit message; with it, a clean check is followed by commit and push")
    args = ap.parse_args(argv)
    if not args.check and not args.message:
        ap.error("give --check, or -m <message> to push")
    found = check()
    if found:
        print("notes NOT pushed:" if args.message else "notes check failed:")
        for line in found:
            print(f"  - {line}")
        return 1
    if args.check:
        print("notes check: ok")
        return 0
    err = push(args.message)
    if err:
        print(f"notes NOT pushed: {err}")
        return 1
    print("notes pushed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
