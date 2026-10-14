#!/usr/bin/env python3
"""Get the Mac mini working again when its disk is full or its checkouts can't pull (Ben, 14 Oct 2026: "we had it
working perfectly the other day. It just seems to have ground to a halt").

What stopped it (13-14 Oct): the Data volume had about 110 MB free, so every `git pull`, worktree and claim failed;
and local files in the shared checkouts (OWB qa_compilation_v04 records, HOS standalone-Shorts edits and VO concat
files) blocked the pull even when there was space. Every relay wake then stopped at step 1, so no job finished for a
day, the 06:40 analytics snapshot didn't run, and the relay itself (run from the shared checkout) never got its fixes.

Safe by design. It only:
  1. clears caches that rebuild themselves (Homebrew, npm, pip, uv) and prunes stale git worktree records;
  2. removes temporary worktrees under /tmp or /private/tmp that are clean and hold nothing that isn't pushed;
  3. unblocks each shared checkout's pull: untracked files that main also has move to ~/_desk/rescue/<date>/<repo>/
     (same paths, kept); edits to tracked files go into a named `git stash` (kept, not dropped); local commits that
     aren't on origin are pushed to a `rescue/mini-<date>-<repo>` branch first, and the checkout is reset to
     origin/main only after that push succeeded;
  4. lists the biggest folders, so render scratch can be moved to the NAS by the usual rule (AGENTS.md "Render
     scratch" and "NAS archive": rsync, sha256 on both sides, delete locally only on a full match). It never moves
     or deletes media itself and never touches the NAS.

  python3 scripts/mini_repair.py            # dry run: what it would do
  python3 scripts/mini_repair.py --apply    # do it
  # with the checkout itself stuck, fetch it without git:
  curl -fsSL https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/main/scripts/mini_repair.py | python3 - --apply

scripts/chief_relay.py runs the same steps by itself (at most every 30 min) when the disk is low or its pull fails.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import shutil
import subprocess
import sys

HOME = pathlib.Path.home()
OWB = pathlib.Path(os.environ.get("OWB_REPO", HOME / "YouTube" / "orbit-with-ben"))
HOS = pathlib.Path(os.environ.get("HOS_REPO", HOME / "YouTube" / "History Of Science"))
TMP_ROOTS = ("/tmp/", "/private/tmp/")


def free_mb(path: pathlib.Path = HOME) -> int:
    return shutil.disk_usage(str(path)).free // (1024 * 1024)


def run(cmd: list, cwd=None, timeout: int = 600) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as e:
        return subprocess.CompletedProcess(cmd, 127, "", str(e))


def git(repo: pathlib.Path, *args: str, timeout: int = 300) -> subprocess.CompletedProcess:
    return run(["git", "-C", str(repo), *args], timeout=timeout)


# ---- 1. caches ----

def cache_steps() -> list:
    """(name, command) for caches that rebuild themselves; only tools that are installed."""
    steps = []
    if shutil.which("brew"):
        steps.append(("Homebrew cache", ["brew", "cleanup", "-s", "--prune=all"]))
    if shutil.which("npm"):
        steps.append(("npm cache", ["npm", "cache", "clean", "--force"]))
    steps.append(("pip cache", [sys.executable, "-m", "pip", "cache", "purge"]))
    if shutil.which("uv"):
        steps.append(("uv cache", ["uv", "cache", "clean"]))
    return steps


# ---- 2. temporary worktrees ----

def worktrees(repo: pathlib.Path) -> list:
    """[{path, head, branch}] from `git worktree list --porcelain`, the main checkout excluded."""
    r = git(repo, "worktree", "list", "--porcelain")
    if r.returncode != 0:
        return []
    out, cur = [], {}
    for line in r.stdout.splitlines() + [""]:
        if not line.strip():
            if cur:
                out.append(cur)
            cur = {}
            continue
        k, _, v = line.partition(" ")
        cur[k] = v or True
    main = str(repo.resolve())
    return [{"path": w["worktree"], "head": w.get("HEAD", ""), "branch": w.get("branch", "")}
            for w in out if w.get("worktree") and str(pathlib.Path(w["worktree"]).resolve()) != main]


def removable(repo: pathlib.Path, wt: dict) -> tuple:
    """(ok, why): a temp worktree can go if it is clean and its HEAD is on some remote branch (nothing unpushed)."""
    path = wt["path"]
    if not any(path.startswith(r) for r in TMP_ROOTS):
        return False, "not under /tmp"
    if not pathlib.Path(path).exists():
        return True, "folder already gone (stale record)"
    st = git(pathlib.Path(path), "status", "--porcelain")
    if st.returncode != 0:
        return False, "git status failed (broken checkout: left for a person)"
    if st.stdout.strip():
        return False, "has uncommitted changes"
    if wt["head"]:
        on_remote = git(repo, "branch", "-r", "--contains", wt["head"])
        if on_remote.returncode != 0 or not on_remote.stdout.strip():
            return False, "has commits that aren't on origin"
    return True, "clean, everything pushed"


# ---- 3. unblock the shared checkout's pull ----

def unblock(repo: pathlib.Path, apply: bool, today: str) -> dict:
    """Bring a shared checkout to origin/main without losing anything. Returns what it did (or would do)."""
    name = repo.name.lower().replace(" ", "-")
    res = {"repo": str(repo), "actions": [], "ok": False}
    if not (repo / ".git").exists():
        res["actions"].append("not a git checkout: skipped")
        return res
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if branch != "main":
        res["actions"].append(f"on branch {branch!r}, not main: left alone")
        return res
    f = git(repo, "fetch", "-q", "origin", "main")
    if f.returncode != 0:
        res["actions"].append("fetch failed: " + (f.stderr.strip().splitlines() or ["?"])[-1][:160])
        return res
    if git(repo, "merge-base", "--is-ancestor", "origin/main", "HEAD").returncode == 0 and \
            git(repo, "merge-base", "--is-ancestor", "HEAD", "origin/main").returncode == 0:
        res["ok"] = True
        res["actions"].append("already at origin/main")
        return res
    changed = git(repo, "status", "--porcelain", "--untracked-files=no").stdout.strip()
    # Untracked files only block a pull when main has a file at the same path. Those move (same volume: no extra
    # space, unlike a stash of big VO wavs) to ~/_desk/rescue/<date>/<repo>/<same path>; other untracked files stay.
    on_main = set(git(repo, "ls-tree", "-r", "--name-only", "origin/main").stdout.splitlines())
    blocking = [p for p in git(repo, "ls-files", "--others", "--exclude-standard").stdout.splitlines() if p in on_main]
    ahead = git(repo, "rev-list", "--count", "origin/main..HEAD").stdout.strip()
    ahead = int(ahead) if ahead.isdigit() else 0
    if not changed and not blocking and not ahead:
        if apply:
            m = git(repo, "merge", "-q", "--ff-only", "origin/main")
            res["ok"] = m.returncode == 0
            res["actions"].append("fast-forwarded to origin/main" if res["ok"] else "fast-forward failed")
        else:
            res["actions"].append("would fast-forward to origin/main")
        return res
    if blocking:
        dest = HOME / "_desk" / "rescue" / today / name
        if apply:
            for p in blocking:
                (dest / p).parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(repo / p), str(dest / p))
        res["actions"].append(f"{'moved' if apply else 'would move'} {len(blocking)} untracked file(s) that main also has "
                              f"to {dest} (kept, not deleted)")
    if changed:
        msg = f"mini_repair {today}: local edits that blocked the pull"
        if apply:
            s = git(repo, "stash", "push", "-m", msg)
            if s.returncode != 0:
                res["actions"].append("stash failed: " + (s.stderr.strip().splitlines() or ["?"])[-1][:160])
                return res
            res["actions"].append(f"stashed local edits as {msg!r} (git stash list)")
        else:
            res["actions"].append(f"would stash {len(changed.splitlines())} local edit(s) as {msg!r}")
    if ahead:
        rescue = f"rescue/mini-{today}-{name}"
        if apply:
            p = git(repo, "push", "-q", "origin", f"HEAD:refs/heads/{rescue}")
            if p.returncode != 0:
                res["actions"].append(f"{ahead} local commit(s) not on origin and the rescue push failed: left as is")
                return res
            git(repo, "reset", "-q", "--hard", "origin/main")
            res["actions"].append(f"pushed {ahead} local commit(s) to {rescue}, then reset to origin/main")
        else:
            res["actions"].append(f"would push {ahead} local commit(s) to {rescue}, then reset to origin/main")
    elif apply:
        m = git(repo, "merge", "-q", "--ff-only", "origin/main")
        res["actions"].append("fast-forwarded to origin/main" if m.returncode == 0 else "fast-forward failed")
    if apply:
        res["ok"] = git(repo, "merge-base", "--is-ancestor", "origin/main", "HEAD").returncode == 0
    return res


# ---- 4. what's big ----

def biggest(roots=("/private/tmp", str(HOME)), n: int = 12) -> list:
    """[(MB, path)] for the largest folders one level down in each root (du -sk, 2 min cap each root)."""
    rows = []
    for root in roots:
        p = pathlib.Path(root)
        if not p.is_dir():
            continue
        try:
            kids = [str(c) for c in p.iterdir() if c.is_dir() and not c.is_symlink()]
        except OSError:
            continue
        if not kids:
            continue
        r = run(["du", "-sk", *kids], timeout=120)
        for line in r.stdout.splitlines():
            kb, _, path = line.partition("\t")
            if kb.isdigit():
                rows.append((int(kb) // 1024, path))
    return sorted(rows, reverse=True)[:n]


def repair(apply: bool, repos=None, do_caches: bool = True, scan: bool = True) -> dict:
    today = dt.date.today().isoformat()
    report = {"before_mb": free_mb(), "caches": [], "worktrees": [], "checkouts": [], "biggest": []}
    if do_caches:
        for name, cmd in cache_steps():
            if apply:
                before = free_mb()
                r = run(cmd)
                report["caches"].append(f"{name}: {'ok' if r.returncode == 0 else 'failed'} (+{free_mb() - before} MB)")
            else:
                report["caches"].append(f"{name}: would run {' '.join(cmd)}")
    for repo in repos or (OWB, HOS):
        if not (repo / ".git").exists():
            continue
        if apply:
            git(repo, "worktree", "prune")
        for wt in worktrees(repo):
            ok, why = removable(repo, wt)
            if ok and apply:
                r = git(repo, "worktree", "remove", "--force", wt["path"])
                why = why if r.returncode == 0 else "remove failed"
            report["worktrees"].append(f"{wt['path']}: {'remove' if ok else 'keep'} ({why})")
    for repo in repos or (OWB, HOS):
        if (repo / ".git").exists():
            report["checkouts"].append(unblock(repo, apply, today))
    if scan:
        report["biggest"] = [f"{mb:>8,} MB  {p}" for mb, p in biggest()]
    report["after_mb"] = free_mb()
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="do it (default: dry run)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    rep = repair(a.apply)
    if a.json:
        print(json.dumps(rep, indent=1))
        return 0
    print(f"{'Done' if a.apply else 'Dry run'}: {rep['before_mb']:,} MB free before, {rep['after_mb']:,} MB after.")
    for k in ("caches", "worktrees"):
        for line in rep[k]:
            print(f"  {k[:-1]}: {line}")
    for c in rep["checkouts"]:
        print(f"  checkout {c['repo']}: {'; '.join(c['actions'])}")
    if rep["biggest"]:
        print("Biggest folders (move old render scratch to the NAS by AGENTS.md 'Render scratch'; never delete on the NAS):")
        print("\n".join("  " + x for x in rep["biggest"]))
    if rep["after_mb"] < 20 * 1024:
        print(f"Still under 20 GB free ({rep['after_mb']:,} MB): move the version-before-last render scratch to the NAS.")
    stuck = [c for c in rep["checkouts"] if not c["ok"]]
    return 1 if a.apply and stuck else 0


if __name__ == "__main__":
    sys.exit(main())
