#!/usr/bin/env python3
"""Publish the Studio Kanban's data so the board updates itself (Ben, 9 Oct: "the board should just update whenever a
task is done or something progressed").

The board page (05_Analytics/kanban/board_site, hosted on Vercel) reads one file at runtime and re-reads it every 60 s:
  board.json on the branch `board-data` of this repo (a single parentless commit, force-pushed, like mini-heartbeat).

This script builds that file from main with scripts/kanban_snapshot.py (the same documents Claude used to write into the
claude.ai artifact store: board/hos, board/owb, board/briefs, board/credits) and pushes it only when something changed.

Triggers (all on the Mini):
  - scripts/jobs.py runs it in the background after every queue change (add, claim, done, block, release, renew, ...)
  - launchd com.owb.board-publish every 5 min (picks up cloud pushes to main, HOS PIPELINE.json and the Mini
    heartbeat); a no-op when nothing changed
It never blocks or fails a job: the hook is fire-and-forget and every error here is logged and swallowed.

Each section keeps the time its content last changed (`changedAt`), so the page header shows the real last change,
not the last run.

  python3 scripts/board_publish.py              # build, push if changed
  python3 scripts/board_publish.py --dry-run    # build and print a summary; push nothing
  python3 scripts/board_publish.py --force      # push even if unchanged

State (never in git): ~/_desk/state/board/ (last.json, board.json, publish.log). Read-only sparse worktrees of both
repos at origin/main: ~/_desk/scratch/chief/board-wt/{owb,hos} (small; they share the main checkouts' .git).
"""
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import urllib.request

HOME = pathlib.Path.home()
OWB = pathlib.Path(os.environ.get("OWB_REPO", str(HOME / "YouTube" / "orbit-with-ben")))
HOS = pathlib.Path(os.environ.get("HOS_REPO", str(HOME / "YouTube" / "History Of Science")))
STATE = pathlib.Path(os.environ.get("BOARD_STATE", str(HOME / "_desk" / "state" / "board")))
WT = pathlib.Path(os.environ.get("BOARD_WT", str(HOME / "_desk" / "scratch" / "chief" / "board-wt")))
BRANCH = os.environ.get("BOARD_BRANCH", "board-data")
SITE = os.environ.get("BOARD_SITE_URL", "https://studio-kanban.vercel.app").rstrip("/")
CHECKS_EVERY_S = 60 * 60  # Ben's OK/change ticks: re-read from the site at most hourly (Blob free-tier list calls)

OWB_SPARSE = ["/scripts/", "/jobs/", "/05_Analytics/kanban/", "/05_Analytics/ai_spend/", "/02_Video-Projects/*/status.json"]
HOS_SPARSE = ["/00_Brand/Channel-Setup/PIPELINE.json"]
SECTIONS = ("hos", "owb", "briefs", "credits")
NAMES = {"chief": "Grok", "cursor": "Cursor", "codex": "Codex", "claude": "Claude"}


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso(t: dt.datetime) -> str:
    return t.isoformat().replace("+00:00", "Z")


def log(msg: str) -> None:
    try:
        STATE.mkdir(parents=True, exist_ok=True)
        with open(STATE / "publish.log", "a") as f:
            f.write(f"{iso(now())} {msg}\n")
    except OSError:
        pass


def git(repo: pathlib.Path, *args: str, inp: str | None = None, timeout: int = 120) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], input=inp, capture_output=True, text=True,
                          timeout=timeout, check=True).stdout.strip()


def digest(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def stable(section: str, doc: dict) -> dict:
    """The part of a section whose change counts as 'the board changed' (run times and the Mini's 10-min heartbeat don't)."""
    d = {k: v for k, v in doc.items() if k != "updatedAt"}
    if section == "owb" and isinstance(d.get("lanes"), dict):
        d["lanes"] = {k: ({kk: vv for kk, vv in v.items() if kk != "heartbeat"} if isinstance(v, dict) else v)
                      for k, v in d["lanes"].items()}
    return d


def worktree(repo: pathlib.Path, path: pathlib.Path, sparse: list[str]) -> None:
    """A sparse, detached worktree of origin/main, refreshed each run. Read-only use; never committed from."""
    git(repo, "fetch", "-q", "origin", "main")
    if not (path / ".git").exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        git(repo, "worktree", "prune")
        git(repo, "worktree", "add", "-q", "--detach", "--no-checkout", str(path), "origin/main")
        git(path, "sparse-checkout", "set", "--no-cone", *sparse)
    git(path, "checkout", "-q", "-f", "--detach", "origin/main")


def chief_args() -> list[str]:
    try:
        c = json.loads((HOME / "_desk" / "state" / "chief" / "current.json").read_text())
    except (OSError, ValueError):
        return []
    who = c.get("agent") or ""
    return ["--chief", NAMES.get(who, who), "--chief-since", c.get("since", "")] if who else []


def build(out: pathlib.Path) -> dict:
    worktree(OWB, WT / "owb", OWB_SPARSE)
    worktree(HOS, WT / "hos", HOS_SPARSE)
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(WT / "owb" / "scripts" / "kanban_snapshot.py"), "--hos", str(WT / "hos"),
                    "--db-out", str(out), *chief_args()], capture_output=True, text=True, timeout=300, check=True)
    return {s: json.loads((out / f"{s}.json").read_text()) for s in SECTIONS}


def fetch_checks(prev: dict, at: dt.datetime, force: bool) -> tuple[dict, str]:
    last = prev.get("checksAt") or ""
    if not force and last and (at - dt.datetime.fromisoformat(last.replace("Z", "+00:00"))).total_seconds() < CHECKS_EVERY_S:
        return prev.get("checks") or {}, last
    try:
        with urllib.request.urlopen(f"{SITE}/api/checks?t={int(at.timestamp())}", timeout=15) as r:
            body = json.loads(r.read().decode())
        checks = body.get("checks") if isinstance(body, dict) else None
        if isinstance(checks, dict):
            return checks, iso(at)
    except Exception as e:  # noqa: BLE001 - the site being down must never stop the data
        log(f"checks not read: {e}")
    return prev.get("checks") or {}, last


def assemble(docs: dict, prev: dict, checks: dict, at: dt.datetime) -> tuple[dict, dict]:
    """board.json, plus each section's content hash. A section's updatedAt moves only when its content changed."""
    hashes, changed = {}, dict(prev.get("changedAt") or {})
    for s in SECTIONS:
        hashes[s] = digest(stable(s, docs[s]))
        if hashes[s] != (prev.get("hashes") or {}).get(s) or s not in changed:
            changed[s] = iso(at)
        docs[s]["updatedAt"] = changed[s]
    board = {"schema": 1, "dataChangedAt": max(changed.values()), "changedAt": changed, **docs, "checks": checks}
    return board, hashes


# The repo is git-connected to the Vercel project orbit-content-ops (root 07_Content-Ops), so every push to any branch
# would create a deployment there and eat the account's 100-a-day limit. A vercel.json in this branch's commit, at the
# repo root and at that project root, turns deployments off for it.
NO_DEPLOY = json.dumps({"git": {"deploymentEnabled": False}}) + "\n"


def push(board: dict, at: dt.datetime) -> str:
    body = json.dumps(board, ensure_ascii=False, separators=(",", ":")) + "\n"
    blob = git(OWB, "hash-object", "-w", "--stdin", inp=body)
    nd = git(OWB, "hash-object", "-w", "--stdin", inp=NO_DEPLOY)
    sub = git(OWB, "mktree", inp=f"100644 blob {nd}\tvercel.json\n")
    tree = git(OWB, "mktree", inp=f"040000 tree {sub}\t07_Content-Ops\n100644 blob {blob}\tboard.json\n100644 blob {nd}\tvercel.json\n")
    commit = git(OWB, "commit-tree", tree, "-m", f"board data {iso(at)}")
    git(OWB, "push", "-q", "-f", "origin", f"{commit}:refs/heads/{BRANCH}")
    return commit


def run_once(a) -> int:
    at = now()
    prev_path = STATE / "last.json"
    try:
        prev = json.loads(prev_path.read_text())
    except (OSError, ValueError):
        prev = {}
    docs = build(STATE / "out")
    checks, checks_at = fetch_checks(prev, at, a.force)
    board, hashes = assemble(docs, prev, checks, at)
    whole = digest(board)  # includes the heartbeat, so the page's "Mini last seen" stays current
    (STATE / "board.json").write_text(json.dumps(board, ensure_ascii=False, indent=1))
    summary = (f"{len(docs['hos']['pipeline']['films'])} HOS films, {len(docs['owb']['films'])} OWB films, "
               f"{len(docs['owb'].get('jobs') or [])} live jobs, {len(checks)} checks; last change {board['dataChangedAt']}")
    if a.dry_run:
        print(f"dry run: {summary}; would {'push' if whole != prev.get('whole') or a.force else 'skip (unchanged)'}")
        return 0
    if whole == prev.get("whole") and not a.force:
        if not a.quiet:
            print("unchanged")
        return 0
    commit = push(board, at)
    prev_path.write_text(json.dumps({"hashes": hashes, "changedAt": board["changedAt"], "whole": whole,
                                     "checks": checks, "checksAt": checks_at, "pushed": iso(at), "commit": commit}, indent=1))
    log(f"pushed {commit[:8]} to {BRANCH}: {summary}")
    if not a.quiet:
        print(f"pushed {commit[:8]} to {BRANCH}: {summary}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    STATE.mkdir(parents=True, exist_ok=True)
    with open(STATE / "publish.lock", "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            (STATE / "again").touch()  # the running publish goes round once more, so this change isn't lost
            return 0
        for _ in range(3):
            (STATE / "again").unlink(missing_ok=True)
            try:
                run_once(a)
            except Exception as e:  # noqa: BLE001 - never fail the caller (jobs.py, launchd)
                log(f"failed: {e!r} {getattr(e, 'stderr', '') or ''}".strip()[:600])
                if not a.quiet:
                    print(f"board_publish: {e}", file=sys.stderr)
                return 0
            if not (STATE / "again").exists():
                break
    return 0


if __name__ == "__main__":
    sys.exit(main())
