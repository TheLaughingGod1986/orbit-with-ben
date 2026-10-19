#!/usr/bin/env python3
"""Publish the Studio Kanban's data so the board updates itself (Ben, 9 Oct: "the board should just update whenever a
task is done or something progressed").

The board page (05_Analytics/kanban/board_site, hosted on Vercel) reads one file at runtime and re-reads it every 60 s:
  board.json on the branch `board-data` of this repo (a single parentless commit, force-pushed, like mini-heartbeat).

It also carries the Channel Tracker's data (Ben, 10 Oct: the tracker as a phone web app at /tracker on the same site):
  tracker.json on the same branch is 05_Analytics/dashboard/data.json from main, byte for byte. The 06:40 snapshot job
  (07_Content-Ops/launchd/analytics-snapshot.sh) pushes that file to main and then kicks this script, so the tracker page
  has the new snapshot within a minute; the every-minute run below would pick it up anyway.

This script builds board.json from main with scripts/kanban_snapshot.py (the same documents Claude used to write into the
claude.ai artifact store: board/hos, board/owb, board/briefs, board/credits) and pushes it only when something changed.

Triggers (all on the Mini):
  - scripts/jobs.py runs it in the background after every queue change (add, claim, progress, done, block, release, ...)
  - launchd com.owb.board-publish every minute (Ben, 11 Oct 22:09: "let's update this board a bit more often"; was
    5 min). It picks up cloud pushes to main, HOS PIPELINE.json, the Mini heartbeat and Ben's board buttons. A run
    where nothing moved is cheap: three `git ls-remote` calls and the CDN-cached checks stamp, compared with the last
    run (quick_key); the full rebuild (fetch, worktrees, kanban_snapshot) runs only when one of them moved, or every
    FULL_EVERY_S anyway (local-only inputs such as the UAT folder's watch links).
Ben's buttons (Approve / Request changes / Undo, stored by the site's /api/checks): every run reads the store's small
change stamp from the CDN and re-reads the ticks only when it moved (and hourly regardless), so a tap is on the board
within one run, about a minute. Running every minute doesn't add Blob operations: the stamp is a CDN hit, and the
list call stays hourly plus once per real tap (at most once a minute). This script never posts anywhere; the [Ben] comments on #99/#180 come from the site.
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
CHECKS_EVERY_S = 60 * 60  # Ben's OK/change ticks: a full re-read (one Blob list call) at least hourly, as a safety net
CHECKS_MIN_GAP_S = 60     # ...and a stamp-triggered re-read at most once a minute (the stamp can lag a write by 60 s)
CHECK_FIELDS = ("checks", "checksAt", "checksVersion", "stampUrl")
FULL_EVERY_S = 5 * 60     # a full rebuild at least this often even when no ref moved (local-only inputs, date gates)

OWB_SPARSE = ["/scripts/", "/jobs/", "/05_Analytics/kanban/", "/05_Analytics/ai_spend/", "/02_Video-Projects/*/status.json",
              "/02_Video-Projects/*/11_Upload-Package/PACKAGE_UPLOAD_RESULT*.json",  # actual schedules, excluding dry runs
              "/00_Brand/Channel-Setup/social/UPLOADS.json",  # watch links: private YouTube uploads
              "/05_Analytics/dashboard/data.json"]  # the Channel Tracker's data, published as tracker.json
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
    git(path, "sparse-checkout", "set", "--no-cone", *sparse)  # every run, so a new pattern reaches old worktrees
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


TRACKER_SRC = "05_Analytics/dashboard/data.json"


def tracker_text() -> str | None:
    """The tracker's data.json from the origin/main worktree, unchanged, or the last good copy if main's is missing or
    broken (so a bad commit never blanks the page). None only before the first good read."""
    keep = STATE / "tracker.json"
    try:
        text = (WT / "owb" / TRACKER_SRC).read_text()
        if isinstance(json.loads(text).get("channels"), list):
            keep.write_text(text)
            return text
        log("tracker data.json has no channels list; kept the last good copy")
    except (OSError, ValueError, AttributeError) as e:
        log(f"tracker data.json not read ({e}); kept the last good copy")
    try:
        return keep.read_text()
    except OSError:
        return None


def stamp_version(url: str) -> str | None:
    """The checks store's change stamp (board/checks/stamp.json, a public Blob URL served from the CDN, so no Blob
    operation on a cache hit). None when it can't be read; the caller then keeps the hourly re-read."""
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            v = json.loads(r.read().decode()).get("version")
        return v if isinstance(v, str) else None
    except Exception as e:  # noqa: BLE001
        log(f"checks stamp not read: {e}")
        return None


def _age(last: str, at: dt.datetime) -> float:
    try:
        return (at - dt.datetime.fromisoformat(last.replace("Z", "+00:00"))).total_seconds()
    except ValueError:
        return float("inf")


def checks_due(prev: dict, at: dt.datetime, force: bool, stamp=stamp_version) -> bool:
    """Should this run re-read Ben's ticks from /api/checks (the one Blob list call)? Every run (scheduled every minute
    and after each queue change) looks at the cheap change stamp, so a button tap reaches board.json on the next run:
      - --force, the first run, or an hour since the last re-read: yes (the safety net)
      - the stamp's URL not known yet (key absent: a state file from before the stamp): yes, once, to learn it
      - the site gave no stamp URL (an older site deploy): only hourly, so the list calls stay as they were
      - the stamp's version moved since the last re-read (a tap, an undo, or the Chief marking one handled): yes,
        but at most once a minute
    """
    last = prev.get("checksAt") or ""
    if force or not last or _age(last, at) >= CHECKS_EVERY_S:
        return True
    if "stampUrl" not in prev:
        return True
    url = prev.get("stampUrl") or ""
    if not url or _age(last, at) < CHECKS_MIN_GAP_S:
        return False
    v = stamp(url)
    if v is None or v == prev.get("checksVersion"):
        return False
    log(f"checks: the board's buttons changed (stamp {v[-24:]}), re-reading")
    return True


def fetch_checks(prev: dict, at: dt.datetime, force: bool, stamp=stamp_version, due: bool | None = None) -> tuple[dict, str, dict]:
    """(checks, checksAt, {checksVersion, stampUrl}). Keeps the previous copy when nothing changed or the site is down.
    `due` is checks_due's answer when the caller already asked (so the stamp is read once per run)."""
    keep = (prev.get("checks") or {}, prev.get("checksAt") or "",
            {k: prev[k] for k in ("checksVersion", "stampUrl") if k in prev})
    if not (checks_due(prev, at, force, stamp) if due is None else due):
        return keep
    try:
        with urllib.request.urlopen(f"{SITE}/api/checks?t={int(at.timestamp())}", timeout=15) as r:
            body = json.loads(r.read().decode())
        checks = body.get("checks") if isinstance(body, dict) else None
        if isinstance(checks, dict):
            v, u = body.get("version"), body.get("stampUrl")
            return checks, iso(at), {"checksVersion": v if isinstance(v, str) else None,
                                     "stampUrl": u if isinstance(u, str) else ""}
    except Exception as e:  # noqa: BLE001 - the site being down must never stop the data
        log(f"checks not read: {e}")
    return keep


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


def tree_listing(board_blob: str, nd_blob: str, sub_tree: str, tracker_blob: str | None) -> str:
    """git mktree input for the board-data commit (entries sorted by name, as git wants)."""
    rows = [f"040000 tree {sub_tree}\t07_Content-Ops", f"100644 blob {board_blob}\tboard.json"]
    if tracker_blob:
        rows.append(f"100644 blob {tracker_blob}\ttracker.json")
    rows.append(f"100644 blob {nd_blob}\tvercel.json")
    return "\n".join(rows) + "\n"


def push(board: dict, at: dt.datetime, tracker: str | None = None) -> str:
    body = json.dumps(board, ensure_ascii=False, separators=(",", ":")) + "\n"
    blob = git(OWB, "hash-object", "-w", "--stdin", inp=body)
    nd = git(OWB, "hash-object", "-w", "--stdin", inp=NO_DEPLOY)
    sub = git(OWB, "mktree", inp=f"100644 blob {nd}\tvercel.json\n")
    tb = git(OWB, "hash-object", "-w", "--stdin", inp=tracker) if tracker else None
    tree = git(OWB, "mktree", inp=tree_listing(blob, nd, sub, tb))
    commit = git(OWB, "commit-tree", tree, "-m", f"board data {iso(at)}")
    git(OWB, "push", "-q", "-f", "origin", f"{commit}:refs/heads/{BRANCH}")
    return commit


def ls_remote(repo: pathlib.Path, *refs: str) -> str:
    return git(repo, "ls-remote", "origin", *refs, timeout=30)


def quick_key(remote=ls_remote) -> str | None:
    """A cheap fingerprint of everything a rebuild reads that can move between runs: main and mini-heartbeat of
    orbit-with-ben, main of history-of-science (one ls-remote each, no fetch) and the Mini's acting-Chief file.
    None if a remote can't be read; the caller then does the full rebuild."""
    try:
        parts = [remote(OWB, "refs/heads/main", "refs/heads/mini-heartbeat"), remote(HOS, "refs/heads/main")]
    except Exception as e:  # noqa: BLE001
        log(f"quick check failed, full rebuild: {e!r}"[:300])
        return None
    try:
        parts.append((HOME / "_desk" / "state" / "chief" / "current.json").read_text())
    except OSError:
        parts.append("")
    return digest(parts)


def skip_quick(prev: dict, key: str | None, at: dt.datetime, checks_wanted: bool) -> bool:
    """True when this run can stop before the rebuild: no ref moved since the last full build, that build is under
    FULL_EVERY_S old, and Ben's ticks don't need a re-read."""
    return bool(key) and key == prev.get("key") and _age(prev.get("built") or "", at) < FULL_EVERY_S and not checks_wanted


def run_once(a) -> int:
    at = now()
    prev_path = STATE / "last.json"
    try:
        prev = json.loads(prev_path.read_text())
    except (OSError, ValueError):
        prev = {}
    key = None if a.force else quick_key()
    due = checks_due(prev, at, a.force)
    if not a.force and not a.dry_run and skip_quick(prev, key, at, due):
        if not a.quiet:
            print("unchanged (quick check)")
        return 0
    docs = build(STATE / "out")
    checks, checks_at, checks_meta = fetch_checks(prev, at, a.force, due=due)
    board, hashes = assemble(docs, prev, checks, at)
    tracker = tracker_text()
    whole = digest(board)  # includes the heartbeat, so the page's "Mini last seen" stays current
    if tracker:  # a new tracker snapshot is a change too (board.json alone stays as it was)
        whole = digest([whole, hashlib.sha256(tracker.encode()).hexdigest()])
    board["publishedAt"] = iso(at)  # the page's small "Updated HH:MM"; after the digest, so it never forces a push
    (STATE / "board.json").write_text(json.dumps(board, ensure_ascii=False, indent=1))
    summary = (f"{len(docs['hos']['pipeline']['films'])} HOS films, {len(docs['owb']['films'])} OWB films, "
               f"{len(docs['owb'].get('jobs') or [])} live jobs, {len(checks)} checks; last change {board['dataChangedAt']}"
               f"; tracker {'generated ' + str(json.loads(tracker).get('generatedAt')) if tracker else 'missing'}")
    if a.dry_run:
        print(f"dry run: {summary}; would {'push' if whole != prev.get('whole') or a.force else 'skip (unchanged)'}")
        return 0
    built = {"key": key, "built": iso(at)} if key else {"built": iso(at)}
    if whole == prev.get("whole") and not a.force:
        seen = {"checks": checks, "checksAt": checks_at, **checks_meta}
        # remember the re-read and this build's fingerprint; nothing to push
        prev_path.write_text(json.dumps({**prev, **seen, **built}, indent=1))
        if not a.quiet:
            print("unchanged")
        return 0
    commit = push(board, at, tracker)
    prev_path.write_text(json.dumps({"hashes": hashes, "changedAt": board["changedAt"], "whole": whole,
                                     "checks": checks, "checksAt": checks_at, **checks_meta, "pushed": iso(at),
                                     "commit": commit, **built}, indent=1))
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
