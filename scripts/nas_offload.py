#!/usr/bin/env python3
"""Move old render scratch off the Mac mini to the NAS so the disk keeps its 20 GB headroom
(Ben, 28 Oct 2026: "The external storage we can use our NAS for now").

This runs the AGENTS.md "Render scratch" / "NAS archive" rule that agents used to do by hand:
  1. pick folders in /private/tmp nobody has touched for --min-age-h hours (default 48: macOS purges /private/tmp
     after about 3 days unused, so anything older is at risk there anyway), biggest benefit first, oldest first;
  2. rsync each one to /Volumes/data/mac-mini-archive/mini-tmp-scratch/<date>/<name>/;
  3. SHA-256 every file on both sides and write SHA256SUMS.txt next to the NAS copy;
  4. only on a full match (same files, same sizes, same hashes) empty the Mini folder and leave MOVED_TO_NAS.txt in it.
It stops once the disk is back over --target-gb free or --max-gb has moved this run.

Never deletes anything on the NAS. Does nothing when the share is not mounted (writing into an unmounted
/Volumes/data would land on the Mini disk). Dry run unless --apply.

  python3 scripts/nas_offload.py                 # what it would move
  python3 scripts/nas_offload.py --apply         # move it
  python3 scripts/nas_offload.py --apply --json  # the relay's call
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys

HOME = pathlib.Path.home()
NAS_MOUNT = pathlib.Path(os.environ.get("NAS_MOUNT", "/Volumes/data"))
NAS_ARCHIVE = "mac-mini-archive"
SCRATCH_ROOT = pathlib.Path(os.environ.get("SCRATCH_ROOT", "/private/tmp"))
MARKER = "MOVED_TO_NAS.txt"
# System and tool folders in /private/tmp that are never render scratch.
SKIP_PREFIXES = ("com.apple", "launchd", "tmux", "powerlog", "ollama", "pip-", "npm-", "node-compile", "claude",
                 "codex", "gemini", "cursor", "playwright", "pytest", "_MEI", ".", "boost_interprocess")
# Scheduled-Short export paths that a 'superseded' sweep must never offload before the Short airs (J1320).
SCHEDULED_SHORT_KEEP_PATHS = (
    "00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s4_uranus_v01.mp4",
    "02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/mon09_night_cold/06_Final-Exports/mon09_night_cold_v01.mp4",
    "02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/thu12_length_test_dust/06_Final-Exports/thu12_length_test_dust_v01.mp4",
    "02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports/fri13_ingenuity_72_v02.mp4",
)


def scheduled_short_keep_paths(repo_root: pathlib.Path | None = None) -> set[str]:
    """Repo-relative or absolute paths of scheduled (non-retired, non-superseded) Short exports to keep on disk."""
    root = repo_root or pathlib.Path(__file__).resolve().parent.parent
    keep = set(SCHEDULED_SHORT_KEEP_PATHS)
    for rel_uploads in (
        "00_Brand/Channel-Setup/social/UPLOADS.json",
        "00_Brand/Channel-Setup/social/hos/UPLOADS.json",
    ):
        up_path = root / rel_uploads
        if not up_path.is_file():
            continue
        try:
            videos = json.loads(up_path.read_text()).get("videos", {})
        except ValueError:
            continue
        for rec in videos.values():
            if not isinstance(rec, dict) or rec.get("retired") or rec.get("supersededBy"):
                continue
            fl = rec.get("file")
            if fl:
                keep.add(str(fl))
    return keep


def free_mb(path: pathlib.Path = HOME) -> int:
    return shutil.disk_usage(str(path)).free // (1024 * 1024)


def nas_ready(mount: pathlib.Path = NAS_MOUNT, check_mount: bool = True) -> tuple[bool, str]:
    """The share is usable only if it is a real mount (not a leftover folder on the Mini disk) with the archive in it."""
    if check_mount and not os.path.ismount(mount):
        return False, f"{mount} is not mounted"
    arch = mount / NAS_ARCHIVE
    if not arch.is_dir():
        return False, f"{arch} not found"
    probe = arch / f".offload_probe_{os.getpid()}"
    try:
        probe.write_text("ok")
        probe.unlink()
    except OSError as e:
        return False, f"{arch} not writable ({e.__class__.__name__})"
    return True, "ok"


def tree_files(root: pathlib.Path) -> list[pathlib.Path]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = [x for x in dirnames if not os.path.islink(os.path.join(dirpath, x))]
        for f in filenames:
            p = pathlib.Path(dirpath, f)
            if not p.is_symlink() and p.is_file():
                out.append(p)
    return out


def scan(root: pathlib.Path) -> tuple[int, float]:
    """(bytes, newest mtime) for a folder tree."""
    size, newest = 0, 0.0
    for p in tree_files(root):
        try:
            st = p.stat()
        except OSError:
            continue
        size += st.st_size
        newest = max(newest, st.st_mtime)
    try:
        newest = max(newest, root.stat().st_mtime)
    except OSError:
        pass
    return size, newest


def candidates(root: pathlib.Path, min_age_h: float, min_mb: int, now: float) -> list[dict]:
    rows = []
    if not root.is_dir():
        return rows
    uid = os.getuid()
    for c in sorted(root.iterdir()):
        if not c.is_dir() or c.is_symlink() or c.name.startswith(SKIP_PREFIXES):
            continue
        try:
            if c.stat().st_uid != uid:
                continue
        except OSError:
            continue
        if (c / MARKER).exists() and len(list(c.iterdir())) == 1:
            continue  # already moved
        size, newest = scan(c)
        age_h = (now - newest) / 3600
        if size < min_mb * 1024 * 1024 or age_h < min_age_h:
            continue
        rows.append({"path": str(c), "mb": size // (1024 * 1024), "age_h": round(age_h, 1)})
    # Oldest first: it is the closest to macOS's purge and the least likely to be wanted again.
    return sorted(rows, key=lambda r: -r["age_h"])


def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest(root: pathlib.Path, skip=(MARKER, "SHA256SUMS.txt")) -> dict[str, tuple[int, str]]:
    return {str(p.relative_to(root)): (p.stat().st_size, sha256(p)) for p in tree_files(root) if p.name not in skip}


def dest_for(src: pathlib.Path, nas: pathlib.Path, today: str) -> pathlib.Path:
    base = nas / NAS_ARCHIVE / "mini-tmp-scratch" / today
    d, n = base / src.name, 2
    while d.exists():  # never write into (or over) something already on the NAS
        d, n = base / f"{src.name}__{n}", n + 1
    return d


def copy_tree(src: pathlib.Path, dst: pathlib.Path) -> None:
    dst.mkdir(parents=True, exist_ok=False)
    if shutil.which("rsync"):
        r = subprocess.run(["rsync", "-a", "--no-links", f"{src}/", f"{dst}/"], capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f"rsync failed: {(r.stderr or r.stdout)[-300:]}")
    else:
        for p in tree_files(src):
            q = dst / p.relative_to(src)
            q.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, q)


def empty_local(src: pathlib.Path, dst: pathlib.Path, mb: int, at: str) -> None:
    for c in src.iterdir():
        if c.is_dir() and not c.is_symlink():
            shutil.rmtree(c)
        else:
            c.unlink()
    (src / MARKER).write_text(f"Moved to the NAS {at} by scripts/nas_offload.py ({mb:,} MB, sha256 checked).\n{dst}\n"
                              f"SHA256SUMS.txt in that folder lists every file.\n")


def offload_one(src: pathlib.Path, nas: pathlib.Path, today: str, at: str) -> dict:
    size, _ = scan(src)
    before = manifest(src)
    if not before:
        return {"path": str(src), "ok": False, "why": "no files"}
    dst = dest_for(src, nas, today)
    copy_tree(src, dst)
    after = manifest(dst)
    if after != before:
        missing = sorted(set(before) - set(after))[:3]
        diff = sorted(k for k in before if k in after and before[k] != after[k])[:3]
        return {"path": str(src), "nas": str(dst), "ok": False,
                "why": f"sha256 mismatch: kept the Mini copy (missing {missing}, differ {diff})"}
    # Re-check the source did not change while copying (a worker still writing into it).
    if manifest(src) != before:
        return {"path": str(src), "nas": str(dst), "ok": False, "why": "folder changed while copying: kept the Mini copy"}
    (dst / "SHA256SUMS.txt").write_text("".join(f"{h}  {k}\n" for k, (_, h) in sorted(after.items())))
    empty_local(src, dst, size // (1024 * 1024), at)
    return {"path": str(src), "nas": str(dst), "ok": True, "mb": size // (1024 * 1024), "files": len(after)}


def offload(apply: bool, target_gb: float = 20, max_gb: float = 60, min_age_h: float = 48, min_mb: int = 200,
            root: pathlib.Path = SCRATCH_ROOT, nas: pathlib.Path = NAS_MOUNT, check_mount: bool = True,
            free=free_mb) -> dict:
    now = dt.datetime.now(dt.timezone.utc)
    rep = {"before_mb": free(), "target_mb": int(target_gb * 1024), "moved": [], "kept": [], "would": [], "nas": "ok"}
    rep["after_mb"] = rep["before_mb"]
    if rep["before_mb"] >= rep["target_mb"]:
        return rep
    ok, why = nas_ready(nas, check_mount)
    if not ok:
        rep["nas"] = why
        return rep
    budget = int(max_gb * 1024)
    for c in candidates(root, min_age_h, min_mb, now.timestamp()):
        if free() >= rep["target_mb"] or budget <= 0:
            break
        if not apply:
            rep["would"].append(c)
            budget -= c["mb"]
            continue
        try:
            r = offload_one(pathlib.Path(c["path"]), nas, now.date().isoformat(), now.strftime("%Y-%m-%d %H:%MZ"))
        except Exception as e:  # one bad folder never stops the rest; the Mini copy stays
            r = {"path": c["path"], "ok": False, "why": f"{e.__class__.__name__}: {str(e)[:200]}"}
        (rep["moved"] if r["ok"] else rep["kept"]).append(r)
        budget -= c["mb"]
    rep["after_mb"] = free()
    return rep


def summary(rep: dict) -> str:
    if rep["nas"] != "ok":
        return f"NAS offload skipped: {rep['nas']} ({rep['before_mb']:,} MB free)."
    if rep["before_mb"] >= rep["target_mb"]:
        return f"{rep['before_mb']:,} MB free: no offload needed."
    mv = sum(r["mb"] for r in rep["moved"])
    parts = [f"moved {len(rep['moved'])} scratch folder(s), {mv:,} MB, to the NAS (sha256 checked)"] if rep["moved"] else []
    if rep["would"]:
        parts.append(f"would move {len(rep['would'])} folder(s), {sum(r['mb'] for r in rep['would']):,} MB")
    if rep["kept"]:
        parts.append(f"kept {len(rep['kept'])} on the Mini: " + "; ".join(f"{pathlib.Path(r['path']).name} ({r['why']})"
                                                                         for r in rep["kept"][:3]))
    if not parts:
        parts.append("nothing in /private/tmp old enough to move")
    return f"NAS offload: {'; '.join(parts)}. {rep['before_mb']:,} -> {rep['after_mb']:,} MB free."


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="move (default: dry run)")
    ap.add_argument("--target-gb", type=float, default=20, help="stop once this much is free (default 20)")
    ap.add_argument("--max-gb", type=float, default=60, help="move at most this much per run (default 60)")
    ap.add_argument("--min-age-h", type=float, default=48, help="only folders untouched this long (default 48)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    rep = offload(a.apply, a.target_gb, a.max_gb, a.min_age_h)
    print(json.dumps(rep, indent=1) if a.json else summary(rep))
    return 1 if rep["kept"] else 0


if __name__ == "__main__":
    sys.exit(main())
