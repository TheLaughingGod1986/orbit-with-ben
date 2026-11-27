#!/usr/bin/env python3
"""Merge a batch of channel-repo pull requests safely (the Chief's PR sweep).

Why (25 Nov 2026): 30 finished ww2-channel PRs waited over a day for a Chief merge, against rule 6 ("Nothing waits
>24 hours on a review"). Batch-merging them by hand showed three traps, which this tool closes:
  - status.json clashes: resolved by a 3-way JSON merge that keeps both sides; lists of records with an `id`
    (a film's `shorts`) are merged by id, so a PR that updates a record never adds a second copy of it;
  - a text file that several PRs rewrote (film 014's SCRIPT.md, v01 then v02): the newer PR's version wins, never a
    stitched copy of both;
  - nothing is pushed unless the merged tree has no conflict markers, no duplicate record ids and passes
    `channel_check.py`.

Usage (from anywhere; the repo checkout must be clean and on main):
    python3 scripts/channel_pr_sweep.py --repo ~/YouTube/ww2-channel  87:macbook/J3486  88:macbook/J3485 ...
    python3 scripts/channel_pr_sweep.py --repo ... --push   # push main once every check passes

Each PR is `<number>:<head branch>`, oldest first. Merge commits keep each PR's head, so GitHub marks it merged.
Only the elected Chief runs this (AGENTS.md: merges are a Chief call). A PR that cannot be resolved is left open and
reported; a PR touching `studio/RULES.md`, `AGENTS.md` or `.github/` is skipped unless --rules is given (read it first).
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import subprocess
import sys

MISSING = object()
GUARDED = ("studio/RULES.md", "AGENTS.md", "CLAUDE.md", ".github/")


def merge3(base, ours, theirs, theirs_newer: bool = True):
    """3-way merge of JSON values. Both sides' additions are kept; a scalar both sides changed goes to the newer side."""
    if ours == theirs:
        return ours
    if ours is MISSING:
        return theirs
    if theirs is MISSING:
        return ours
    if base is not MISSING and ours == base:
        return theirs
    if base is not MISSING and theirs == base:
        return ours
    if isinstance(ours, dict) and isinstance(theirs, dict):
        b = base if isinstance(base, dict) else {}
        out = {}
        for k in list(ours) + [k for k in theirs if k not in ours]:
            v = merge3(b.get(k, MISSING), ours.get(k, MISSING), theirs.get(k, MISSING), theirs_newer)
            if v is not MISSING:
                out[k] = v
        return out
    if isinstance(ours, list) and isinstance(theirs, list):
        def keyed(xs):
            return bool(xs) and all(isinstance(x, dict) and x.get("id") for x in xs)
        if keyed(ours) and keyed(theirs):
            bm = {x["id"]: x for x in base} if isinstance(base, list) and keyed(base) else {}
            om, tm = {x["id"]: x for x in ours}, {x["id"]: x for x in theirs}
            ids = [x["id"] for x in ours] + [x["id"] for x in theirs if x["id"] not in om]
            return [merge3(bm.get(i, MISSING), om.get(i, MISSING), tm.get(i, MISSING), theirs_newer) for i in ids]
        out = list(ours)
        out += [x for x in theirs if x not in out]
        return out
    return theirs if theirs_newer else ours


def duplicate_ids(doc) -> list[str]:
    """Record ids that appear twice in one list anywhere in a JSON document."""
    found = []
    if isinstance(doc, dict):
        for v in doc.values():
            found += duplicate_ids(v)
    elif isinstance(doc, list):
        ids = [x.get("id") for x in doc if isinstance(x, dict) and x.get("id")]
        found += [i for i, n in collections.Counter(ids).items() if n > 1]
        for v in doc:
            found += duplicate_ids(v)
    return found


def git(repo: pathlib.Path, *args, check=True) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout


def show(repo, stage: int, path: str):
    r = subprocess.run(["git", "-C", str(repo), "show", f":{stage}:{path}"], capture_output=True, text=True)
    if r.returncode:
        return MISSING
    try:
        return json.loads(r.stdout)
    except ValueError:
        return MISSING


def resolve(repo: pathlib.Path, path: str) -> str:
    """Resolve one conflicted path in place; return '' or why it could not be resolved."""
    full = repo / path
    if path.endswith(".json"):
        base, ours, theirs = show(repo, 1, path), show(repo, 2, path), show(repo, 3, path)
        if ours is MISSING and theirs is MISSING:
            return "unreadable JSON on both sides"
        doc = merge3(base, ours, theirs, theirs_newer=True)
        full.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    else:
        # The PR being merged is newer than what it conflicts with (PRs go oldest first): its version wins.
        r = subprocess.run(["git", "-C", str(repo), "checkout", "--theirs", "--", path], capture_output=True, text=True)
        if r.returncode:  # deleted on their side
            r = subprocess.run(["git", "-C", str(repo), "rm", "-q", "--", path], capture_output=True, text=True)
            if r.returncode:
                return r.stderr.strip()
            return ""
    git(repo, "add", "--", path)
    return ""


def tree_problems(repo: pathlib.Path, channel_check: pathlib.Path | None) -> list[str]:
    out = []
    for f in git(repo, "ls-files").splitlines():
        p = repo / f
        if not p.is_file() or p.suffix not in (".json", ".md", ".txt", ".srt", ".py"):
            continue
        try:
            text = p.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        if "\n<<<<<<< " in "\n" + text or "\n>>>>>>> " in "\n" + text:
            out.append(f"conflict marker in {f}")
        if p.name == "status.json":
            try:
                dups = duplicate_ids(json.loads(text))
            except ValueError:
                out.append(f"invalid JSON in {f}")
                continue
            if dups:
                out.append(f"duplicate record ids {sorted(set(dups))} in {f}")
    if channel_check and channel_check.is_file():
        r = subprocess.run([sys.executable, str(channel_check), str(repo)], capture_output=True, text=True)
        if r.returncode:
            out.append("channel_check failed: " + (r.stdout + r.stderr).strip().splitlines()[-1][:300])
    return out


def sweep(repo: pathlib.Path, prs: list[tuple[int, str]], *, allow_rules=False, push=False,
          channel_check: pathlib.Path | None = None, log=print) -> dict:
    if git(repo, "status", "--porcelain").strip():
        raise RuntimeError("the checkout has local changes; sweep from a clean main")
    git(repo, "fetch", "-q", "origin", "main")
    git(repo, "checkout", "-q", "-B", "main", "origin/main")
    merged, skipped = [], []
    for num, branch in prs:
        git(repo, "fetch", "-q", "origin", f"+refs/heads/{branch}:refs/remotes/origin/{branch}")
        changed = git(repo, "diff", "--name-only", f"main...origin/{branch}").split()
        guarded = [f for f in changed if f.startswith(GUARDED)]
        if guarded and not allow_rules:
            skipped.append((num, "touches " + ", ".join(guarded) + " (read it, then --rules)"))
            log(f"PR {num}: skipped, touches {', '.join(guarded)}")
            continue
        msg = f"Merge pull request #{num} from {branch}"
        r = subprocess.run(["git", "-C", str(repo), "-c", "user.name=Chief sweep", "merge", "--no-ff", "-q", "-m", msg,
                            f"origin/{branch}"], capture_output=True, text=True)
        if r.returncode == 0:
            merged.append(num)
            log(f"PR {num}: clean")
            continue
        why = [f"{p}: {e}" for p in git(repo, "diff", "--name-only", "--diff-filter=U").split() if (e := resolve(repo, p))]
        left = git(repo, "diff", "--name-only", "--diff-filter=U").split()
        if why or left:
            git(repo, "merge", "--abort", check=False)
            skipped.append((num, "; ".join(why + left)))
            log(f"PR {num}: left open, unresolved {why + left}")
            continue
        git(repo, "-c", "user.name=Chief sweep", "commit", "-q", "--no-edit")
        merged.append(num)
        log(f"PR {num}: resolved")
    problems = tree_problems(repo, channel_check) if merged else []
    for p in problems:
        log("PROBLEM: " + p)
    pushed = False
    if push and merged and not problems:
        git(repo, "push", "-q", "origin", "HEAD:main")
        pushed = True
        log(f"pushed main with {len(merged)} PR(s)")
    elif push and problems:
        log("not pushed: fix the problems above on this local main, re-run the checks, then push")
    return {"merged": merged, "skipped": skipped, "problems": problems, "pushed": pushed}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", required=True, type=pathlib.Path)
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--rules", action="store_true", help="also merge PRs that touch rules files (read them first)")
    ap.add_argument("prs", nargs="+", help="<number>:<head branch>, oldest first")
    a = ap.parse_args(argv)
    prs = []
    for item in a.prs:
        num, _, branch = item.partition(":")
        if not num.isdigit() or not branch:
            ap.error(f"expected <number>:<branch>, got {item!r}")
        prs.append((int(num), branch))
    check = pathlib.Path(__file__).resolve().parent / "channel_check.py"
    res = sweep(a.repo.expanduser().resolve(), sorted(prs), allow_rules=a.rules, push=a.push, channel_check=check)
    print(json.dumps({k: v for k, v in res.items()}, default=str))
    return 1 if res["problems"] or (a.push and res["merged"] and not res["pushed"]) else 0


if __name__ == "__main__":
    sys.exit(main())
