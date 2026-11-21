#!/usr/bin/env python3
"""Recompute current blocking gates for scheduled Shorts and longs in the next 14 days.

The upload path uses the same publishing_gates.evaluate function. Findings are written
as Markdown plus a JSON sidecar for scheduled_gates.py, which queues Chief fixes.
No YouTube writes. Missing media/tools remain explicit coverage failures.
Legacy --stage and --add remain available for the Shorts library/analytics adapter.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
GATE = HERE / "gate_shorts_open.py"
LIB_JSON = HERE.parents[0] / "audits" / "shorts_open_library" / "library.json"
LONDON = ZoneInfo("Europe/London")
CACHE = Path("~/_desk/cache/gate-media").expanduser()
NAS = "/Volumes/"


def london_date(iso: str) -> str:
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(LONDON).date().isoformat()


def upcoming(snapshot: dict, uploads: dict, now: datetime, days: int) -> list[dict]:
    """Scheduled videos airing within `days`, soonest first. publishAt comes from the snapshot, else UPLOADS.json."""
    reg = uploads.get("videos", {})
    out = []
    for v in snapshot.get("videos", []):
        if v.get("privacy") != "private":
            continue
        entry = reg.get(v["id"], {})
        if entry.get("retired"):
            continue
        at = v.get("publishAt") or entry.get("publishAt")
        if not at:
            continue
        when = datetime.fromisoformat(at.replace("Z", "+00:00"))
        if now <= when <= now + timedelta(days=days):
            out.append({"id": v["id"], "title": v.get("title", ""), "publishAt": at, "air": london_date(at), "file": entry.get("file"),
                        "length_test": bool(entry.get("lengthTest")), "format": v.get("format", "long"),
                        "known_no_file": entry.get("knownNoFile") or ""})
    return sorted(out, key=lambda r: r["publishAt"])


def in_library(vid: str) -> bool:
    if not LIB_JSON.exists():
        return False
    return any(e["id"] == vid for e in json.loads(LIB_JSON.read_text()).get("entries", []))


def fail_lines(output: str) -> list[str]:
    """The FAIL reasons in a `gate_shorts_open.py check` printout (indented lines, not the file's summary line)."""
    return [ln.strip()[len("FAIL"):].strip() for ln in output.splitlines() if ln.startswith(" ") and ln.strip().startswith("FAIL ")]


def report_only_lines(output: str) -> list[str]:
    """60% stayed-to-watch findings printed under `--report-only` (`warn  [report-only] ...`) for already-scheduled Shorts."""
    tag = "warn  [report-only]"
    return [ln.strip()[len(tag):].strip() for ln in output.splitlines() if ln.startswith(" ") and ln.strip().startswith(tag)]


def waived(export: Path, fails: list[str]) -> list[dict] | None:
    """Waivers recorded beside the export (<stem>_gate.json, `waivers: [{fail, waived_by}]`) that cover every current
    FAIL exactly. A waiver is for one exact finding on one exact file: a changed number means a changed cut, so it
    no longer counts. Returns the waivers used, or None if any FAIL is not covered."""
    side = export.with_name(export.stem + "_gate.json")
    if not fails or not side.exists():
        return None
    try:
        data = json.loads(side.read_text())
    except ValueError:
        return None
    records = data if isinstance(data, list) else [data]
    book = {w.get("fail", "").strip(): w for r in records for w in r.get("waivers", []) or []}
    used = [book.get(f) for f in fails]
    return used if all(used) else None


def readable(p: Path) -> bool:
    try:
        with open(p, "rb") as fh:
            fh.read(1)
        return True
    except OSError:
        return False


def export_path(media_root: Path, rel: str | None) -> Path | None:
    """Resolve `rel` under `media_root` and collapse `..` so `../../../../Volumes/...` starts with `/Volumes/`."""
    return Path(os.path.abspath((media_root / rel).expanduser())) if rel else None


def sidecar(export: Path) -> Path | None:
    """The export's <stem>_meta.json, where gate_shorts_open.py looks for it first."""
    for c in (export.with_name(f"{export.stem}_meta.json"), export.parent.parent / f"{export.stem}_meta.json"):
        try:
            if c.is_file():
                return c
        except OSError:
            pass
    return None


def nas_refs(obj) -> list[str]:
    """Every string in a meta that points at the NAS."""
    if isinstance(obj, str):
        return [obj] if obj.startswith(NAS) else []
    if isinstance(obj, dict):
        return [x for v in obj.values() for x in nas_refs(v)]
    if isinstance(obj, list):
        return [x for v in obj for x in nas_refs(v)]
    return []


def rewrite(obj, mapping: dict):
    if isinstance(obj, str):
        return mapping.get(obj, obj)
    if isinstance(obj, dict):
        return {k: rewrite(v, mapping) for k, v in obj.items()}
    if isinstance(obj, list):
        return [rewrite(v, mapping) for v in obj]
    return obj


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def stage_one(vid: str, export: Path, cache: Path) -> str:
    """Copy a Short's NAS files into cache/<vid>/ and write stage.json. Returns a one-line result."""
    meta_p = sidecar(export)
    meta = json.loads(meta_p.read_text()) if meta_p else {}
    refs = sorted({r for r in nas_refs(meta) if Path(r).is_file()})
    if not str(export).startswith(NAS) and not refs:
        return f"{vid}: local, nothing to stage"
    d = cache / vid
    d.mkdir(parents=True, exist_ok=True)
    local_export = export
    if str(export).startswith(NAS):
        local_export = d / export.name
        shutil.copy2(export, local_export)
        side = export.with_name(export.stem + "_gate.json")
        if side.is_file():
            shutil.copy2(side, d / side.name)
    mapping = {}
    for r in refs:
        dst = d / "refs" / Path(r).name
        dst.parent.mkdir(exist_ok=True)
        shutil.copy2(r, dst)
        mapping[r] = str(dst)
    meta_out = d / "meta.json"
    meta_out.write_text(json.dumps(rewrite(meta, mapping), indent=2))
    (d / "stage.json").write_text(json.dumps({"source": str(export), "export": str(local_export), "meta": str(meta_out),
                                               "sha256": sha256(local_export), "refs": len(refs),
                                               "staged": datetime.now(timezone.utc).isoformat()}, indent=2))
    return f"{vid}: staged {local_export.name} + {len(refs)} NAS file(s)"


def staged(vid: str, export: Path, cache: Path, want_sha: str | None) -> tuple[Path, Path] | None:
    """(export, meta) from a stage of this exact file, or None. A stage of another cut never counts."""
    st = cache / vid / "stage.json"
    if not st.is_file():
        return None
    try:
        rec = json.loads(st.read_text())
    except ValueError:
        return None
    if rec.get("source") != str(export) or (want_sha and rec.get("sha256") != want_sha):
        return None
    e, m = Path(rec["export"]), Path(rec["meta"])
    return (e, m) if readable(e) and m.is_file() else None


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--snapshot", type=Path, required=True)
    ap.add_argument("--uploads", type=Path, required=True)
    ap.add_argument("--media-root", type=Path, required=True, help="checkout that holds the export files (media is not in git)")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--add", action="store_true", help="register Shorts missing from the open-gate library as scheduled")
    ap.add_argument("--cache", type=Path, default=CACHE, help="local copies of NAS files (default ~/_desk/cache/gate-media)")
    ap.add_argument("--stage", action="store_true", help="copy upcoming Shorts' NAS files into --cache, then exit (run from an agent session)")
    a = ap.parse_args(argv)

    sys.path.insert(0, str(HERE.parents[2] / "scripts"))
    from publishing_gates import evaluate
    findings = []
    now = datetime.now(timezone.utc)
    uploads = json.loads(a.uploads.read_text())
    rows = upcoming(json.loads(a.snapshot.read_text()), uploads, now, a.days)
    if a.stage:
        for r in rows:
            f = export_path(a.media_root, r["file"])
            if not f or not readable(f):
                print(f"{r['id']}: export not readable here, not staged")
                continue
            print(stage_one(r["id"], f, a.cache))
        return 0
    lines = [
        "# Upcoming videos: blocking gate check",
        "",
        f"Written by `gate_upcoming.py` at {now.astimezone(LONDON):%Y-%m-%d %H:%M} London for videos scheduled in the next {a.days} days. Don't edit by hand.",
        "",
    ]
    if not rows:
        lines += ["No scheduled Shorts or longs in the window.", ""]
    else:
        lines += ["| Airs (London) | Video | In Shorts library | Gate |", "|---|---|---|---|"]
        details = []
        missing = [t for t in ("ffprobe", "ffmpeg") if not shutil.which(t)]
        if missing:   # a tool problem on this machine, not a fault in any Short: say so instead of FAIL (8 Oct 2026)
            details.append(f"### Not checked: {', '.join(missing)} not on PATH\n\nFix the job's PATH and re-run; no Short was judged.\n")
        for r in rows:
            f = export_path(a.media_root, r["file"])
            lib = in_library(r["id"])
            want = uploads.get("videos", {}).get(r["id"], {}).get("sha256")
            hit = staged(r["id"], f, a.cache, want) if f else None
            if hit:
                f = hit[0]
            blocked = []
            if f and not hit:
                if str(f).startswith(NAS) and not readable(f):
                    blocked = [str(f)]
                elif readable(f):
                    m = sidecar(f)
                    try:
                        refs = nas_refs(json.loads(m.read_text())) if m else []
                    except ValueError:
                        refs = []
                    blocked = [x for x in refs if Path(x).is_file() and not readable(Path(x))]
            if blocked:
                verdict = "NOT CHECKED"
                details.append(f"### {r['id']}: NOT CHECKED (NAS not readable from this job)\n\nmacOS privacy blocks this job from: `{blocked[0]}`"
                               f"{' and ' + str(len(blocked) - 1) + ' more' if len(blocked) > 1 else ''}. From an agent session run "
                               "`gate_upcoming.py --stage` (same arguments), then re-run. No Short was judged.\n")
            elif r["file"] and not f.exists() and r.get("known_no_file"):
                verdict = "KNOWN"
                details.append(f"### {r['id']}: KNOWN, no local export\n\nExport not found: `{r['file']}`. Already ruled on: {r['known_no_file']}\n")
            elif not f or not f.exists():
                verdict = "NO FILE" if r["file"] else "NOT REGISTERED"
                details.append(f"### {r['id']}: {verdict}\n\n{'Export not found: `' + r['file'] + '`' if r['file'] else 'Not in social/UPLOADS.json, so its export file is unknown.'}\n")
            elif missing:
                verdict = "NOT CHECKED"
            else:
                if a.add and r["format"] == "short" and not lib:
                    code, out = run([sys.executable, str(GATE), "add", "--id", r["id"], "--date", r["air"], "--title", r["title"],
                                     "--file", str(f), "--status", "scheduled", "--source", "gate_upcoming"])
                    lib = code == 0 and in_library(r["id"])
                    if code:
                        details.append(f"### {r['id']}: library add failed\n\n```\n{out[-1500:]}\n```\n")
                result = evaluate(f, a.media_root, r["format"], r["air"], video_id=r["id"],
                                  length_test=r.get("length_test", False),
                                  meta_path=hit[1] if hit else None, short_run=run)
                verdict = "PASS" if result["ok"] else "**FAIL**"
                output = "\n".join(f"{c['gate']}: {c['output']}" for c in result['checks'])
                details.append(f"### {r['id']}: {verdict}\n\n```\n{output}\n```\n")
            findings.append(dict(id=r['id'], publishAt=r['publishAt'], ok=verdict == 'PASS',
                                 output=details[-1] if verdict != 'PASS' and details else verdict))
            lines.append(f"| {r['air']} {london_time(r['publishAt'])} | [{r['title']}](https://youtu.be/{r['id']}) `{r['id']}` | {'yes' if lib else '**no**'} | {verdict} |")
        lines.append("")
        if details:
            lines += ["## Details", ""] + details
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text("\n".join(lines) + "\n")
    a.out.with_suffix(".json").write_text(json.dumps(findings, indent=2))
    print(f"gate_upcoming: {len(rows)} scheduled video(s) checked -> {a.out}")
    return 0


def london_time(iso: str) -> str:
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(LONDON).strftime("%H:%M")


if __name__ == "__main__":
    sys.exit(main())
