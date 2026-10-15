#!/usr/bin/env python3
"""Studio core: one copy of the tooling both channels share (Ben, 15 Oct 2026: "unify HOS and OWB but keeping their
own rules").

orbit-with-ben is the canonical home. `studio-core/CORE_FILES.json` lists every shared file with its sha256, and the
same lock file sits in history-of-science. Each repo's CI runs `check`, so a core file edited in one repo only fails CI
there: change it here, then `push` it to the other checkout, and both stay identical. Channel rules (strategy,
thumbnail and title rules, production locks, the contract code, channel ids) are never core.

  python3 scripts/core_sync.py check                         # this repo's core files match the lock (CI)
  python3 scripts/core_sync.py lock                          # after changing a core file here (canonical repo only)
  python3 scripts/core_sync.py add <path>...                 # make a file core (must be identical in both repos first)
  python3 scripts/core_sync.py diff --other <checkout>       # which core files differ in another checkout
  python3 scripts/core_sync.py push --to <checkout>          # copy the core files, this script and the lock there
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCK = pathlib.Path("studio-core") / "CORE_FILES.json"
SELF = pathlib.Path("scripts") / "core_sync.py"
CANONICAL = "orbit-with-ben"


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(root: pathlib.Path = ROOT) -> dict:
    return json.loads((root / LOCK).read_text())


def save(data: dict, root: pathlib.Path = ROOT) -> None:
    (root / LOCK).parent.mkdir(parents=True, exist_ok=True)
    (root / LOCK).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def problems(root: pathlib.Path, data: dict) -> list:
    """Lines for every core file that is missing or differs from the lock in `root`."""
    out = []
    for rel, want in sorted(data["files"].items()):
        p = root / rel
        if not p.is_file():
            out.append(f"missing  {rel}")
        elif sha(p) != want:
            out.append(f"changed  {rel}")
    return out


def cmd_check(_a) -> int:
    bad = problems(ROOT, load())
    if bad:
        print("Studio core drift. A shared file was edited in one repo only. Make the change in orbit-with-ben, run "
              "`core_sync.py lock`, then `core_sync.py push --to <history-of-science checkout>`:")
        print("\n".join("  " + b for b in bad))
        return 1
    print(f"core OK ({len(load()['files'])} shared files)")
    return 0


def cmd_lock(_a) -> int:
    data = load()
    data["files"] = {rel: sha(ROOT / rel) for rel in data["files"] if (ROOT / rel).is_file()}
    data["files"][str(SELF)] = sha(ROOT / SELF)
    save(data)
    print(f"locked {len(data['files'])} files")
    return 0


def cmd_add(a) -> int:
    data = load()
    for rel in a.paths:
        if not (ROOT / rel).is_file():
            print(f"no such file: {rel}")
            return 1
        data["files"][rel] = sha(ROOT / rel)
    save(data)
    return cmd_lock(a)


def cmd_diff(a) -> int:
    other = pathlib.Path(a.other).resolve()
    bad = problems(other, load())
    print("\n".join(bad) if bad else f"{other} matches the core lock")
    return 1 if bad else 0


def cmd_push(a) -> int:
    if not (ROOT / "jobs" / "queue.json").is_file() and not a.force:   # only orbit-with-ben carries the job queue
        print(f"push runs from the canonical repo ({CANONICAL}), not from {ROOT}")
        return 1
    if problems(ROOT, load()):
        print("this checkout doesn't match its own lock; run `core_sync.py lock` first")
        return 1
    dest = pathlib.Path(a.to).resolve()
    data = load()
    for rel in list(data["files"]) + [str(LOCK)]:
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dest / rel)
    print(f"pushed {len(data['files'])} core files and the lock to {dest}; commit them there")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    sub.add_parser("lock")
    p = sub.add_parser("add")
    p.add_argument("paths", nargs="+")
    p = sub.add_parser("diff")
    p.add_argument("--other", required=True)
    p = sub.add_parser("push")
    p.add_argument("--to", required=True)
    p.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    return {"check": cmd_check, "lock": cmd_lock, "add": cmd_add, "diff": cmd_diff, "push": cmd_push}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
