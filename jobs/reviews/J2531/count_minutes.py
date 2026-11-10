#!/usr/bin/env python3
"""J2531: count which commits on main start which workflow, before and after the change.

Reads `git log --first-parent` for main (no network, no gh), matches every commit's changed files against each
workflow's `paths` / `paths-ignore` the way GitHub does, and prints the counts MINUTES.md is built from.

    python3 jobs/reviews/J2531/count_minutes.py [--since 2026-11-03T20:30:00Z] [--until ...] [--top]

One run per commit is an upper bound: a push of several commits starts one run, not several.
"""
import argparse
import collections
import re
import subprocess

RULES_OLD = ["AGENTS.md", ".cursor/rules/**", "docs/**", "00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md",
             "scripts/sync_rules.py", "scripts/studio.py", "scripts/test_*.py", "scripts/picture_qa.py",
             "scripts/terminal_loop.py", "scripts/fixtures/terminal_loop/**", "04_Audio/tools/vo_take.py",
             "04_Audio/tools/test_vo_take.py", "00_Brand/Channel-Setup/tools/gate_shorts_open.py",
             "00_Brand/Channel-Setup/tools/test_gate_background.py",
             "00_Brand/Channel-Setup/tools/test_gate_duration.py", "00_Brand/Channel-Setup/tools/gate_upcoming.py",
             "00_Brand/Channel-Setup/tools/test_gate_upcoming.py", "00_Brand/Channel-Setup/tools/testdata/**",
             "02_Video-Projects/*/status.json", "STATUS.md", ".github/workflows/rules-check.yml"]
RULES_NEW = [p for p in RULES_OLD if p not in ("02_Video-Projects/*/status.json", "STATUS.md")]
NOTES_OLD = ["05_Analytics/kanban/film_briefs.json", "scripts/notes_push.py", ".github/workflows/notes-check.yml"]
NOTES_NEW = NOTES_OLD[1:]
OPS = ["07_Content-Ops/**", ".github/workflows/content-ops.yml"]

# Data: written by the queue, the board, the tracker and the relay, never by a code change.
DATA = ["jobs/**", "STATUS.md", "02_Video-Projects/*/status.json", "05_Analytics/**", "06_Launch/**"]

# Billed minutes per run: every job is rounded up to a whole minute. Durations seen on pull-request heads, 10 Nov.
MINUTES = {"Rules check": 2, "Studio core check": 1, "Notes check": 1, "Content Ops checks": 2}


def rx(glob):
    out = ""
    i = 0
    while i < len(glob):
        if glob.startswith("**", i):
            out += ".*"
            i += 2
        elif glob[i] == "*":
            out += "[^/]*"
            i += 1
        else:
            out += re.escape(glob[i])
            i += 1
    return re.compile("^" + out + "$")


def any_match(files, globs):
    pats = [rx(g) for g in globs]
    return any(p.match(f) for f in files for p in pats)


def all_match(files, globs):
    pats = [rx(g) for g in globs]
    return bool(files) and all(any(p.match(f) for p in pats) for f in files)


def is_pr_merge(subject):
    return subject.startswith("Merge pull request #") or re.search(r"\(#\d+\)$", subject) is not None


def commits(since, until):
    cmd = ["git", "log", "origin/main", "--first-parent", "--diff-merges=first-parent", "--name-only",
           "--format=@@%H|%s", "--since", since]
    if until:
        cmd += ["--until", until]
    cur = None
    for line in subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.splitlines():
        if line.startswith("@@"):
            if cur:
                yield cur
            sha, subject = line[2:].split("|", 1)
            cur = (sha, subject, [])
        elif line.strip() and cur:
            cur[2].append(line.strip())
    if cur:
        yield cur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026-11-03T20:30:00Z")
    ap.add_argument("--until", default="")
    ap.add_argument("--top", action="store_true", help="list the folders of commits that are not data-only")
    a = ap.parse_args()

    n = collections.Counter()
    old = collections.Counter()
    old_data = collections.Counter()
    new = collections.Counter()
    new_skipped = collections.Counter()
    tops = collections.Counter()
    for sha, subject, files in commits(a.since, a.until):
        n["commits"] += 1
        data_only = all_match(files, DATA)
        merge = is_pr_merge(subject)
        n["data-only"] += data_only
        n["pull-request merges"] += merge
        n["empty"] += not files
        n["code pushed straight to main"] += (not data_only and not merge and bool(files))
        if a.top and not data_only:
            for f in files:
                if not all_match([f], DATA):
                    tops["/".join(f.split("/")[:2])] += 1
        before = {"Studio core check": True, "Rules check": any_match(files, RULES_OLD),
                  "Notes check": any_match(files, NOTES_OLD), "Content Ops checks": any_match(files, OPS)}
        code = bool(files) and not data_only  # what `paths-ignore: DATA` lets through
        after = {"Studio core check": code, "Rules check": any_match(files, RULES_NEW),
                 "Notes check": any_match(files, NOTES_NEW), "Content Ops checks": any_match(files, OPS)}
        for w in MINUTES:
            if before[w]:
                old[w] += 1
                old_data[w] += data_only
            if after[w]:
                if merge:
                    new_skipped[w] += 1  # the job's `if` skips it: no runner, no minutes
                else:
                    new[w] += 1

    for k, v in n.items():
        print(f"{k}: {v}")
    print("\nworkflow | push runs before | of them data-only | min before | push runs after | skipped (merge) | min after")
    tb = ta = 0
    for w, m in MINUTES.items():
        tb += old[w] * m
        ta += new[w] * m
        print(f"{w} | {old[w]} | {old_data[w]} | {old[w] * m} | {new[w]} | {new_skipped[w]} | {new[w] * m}")
    print(f"total push minutes: before {tb}, after {ta}")
    if a.top:
        print()
        for k, v in tops.most_common(40):
            print(v, k)


if __name__ == "__main__":
    main()
