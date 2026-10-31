#!/usr/bin/env python3
"""Gate every scheduled Short before it airs (7 Oct 2026).

`youtube:package` hard-stops a Short that fails gate_shorts_open.py, but Shorts uploaded before that rule,
or by hand in Studio, never went through it, and the open-gate library didn't know about them, so new Shorts
weren't compared against them. The Mini's 06:40 tracker job runs this after its snapshot:

  - every Short in the snapshot that is private with a publishAt in the next --days days
  - its export file from social/UPLOADS.json (repo-relative, resolved under --media-root)
  - `gate_shorts_open.py check <file> --air-date <London date> --id <id>`
  - with --add, a Short missing from the library is registered as `scheduled` (so later Shorts are compared to it)
  - a FAIL that a recorded waiver covers exactly (<export stem>_gate.json beside the file) reads "PASS (waived)"
  - a missing export the Chief has already ruled on (UPLOADS.json "knownNoFile": "<why, with the ruling>") reads
    "KNOWN", not NO FILE, so a settled case stops raising the alarm every morning (J1320, 31 Oct 2026)
  - NAS files (26 Oct 2026): macOS privacy stops the launchd job reading /Volumes (EPERM, "Operation not permitted"),
    while agent sessions can. `--stage` (run from an agent session) copies each upcoming Short's NAS export, its
    sidecar meta and every NAS file the meta names into --cache, with the meta rewritten to the local copies; the
    06:40 run then checks the staged copy. A NAS file with no staged copy reads "NOT CHECKED", never FAIL.

It writes a Markdown report (--out) and always exits 0: it reports, it never blocks the tracker. Claude reads the
report at 07:10 and decides on any FAIL (reschedule or replace a scheduled Short; nothing here touches YouTube).

  python3 gate_upcoming.py --snapshot 05_Analytics/owb/snapshots/2026-10-08.json \\
      --uploads 00_Brand/Channel-Setup/social/UPLOADS.json --media-root ~/YouTube/orbit-with-ben \\
      --out 05_Analytics/owb/UPCOMING_SHORTS_GATE.md --add
"""
from __future__ import annotations

import argparse
import hashlib
import json
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
    """Scheduled Shorts airing within `days`, soonest first. publishAt comes from the snapshot, else UPLOADS.json."""
    reg = uploads.get("videos", {})
    out = []
    for v in snapshot.get("videos", []):
        if v.get("format") != "short" or v.get("privacy") != "private":
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
                        "length_test": bool(entry.get("lengthTest")),
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

    now = datetime.now(timezone.utc)
    uploads = json.loads(a.uploads.read_text())
    rows = upcoming(json.loads(a.snapshot.read_text()), uploads, now, a.days)
    if a.stage:
        for r in rows:
            f = (a.media_root / r["file"]).expanduser() if r["file"] else None
            if not f or not readable(f):
                print(f"{r['id']}: export not readable here, not staged")
                continue
            print(stage_one(r["id"], f, a.cache))
        return 0
    lines = [
        "# Upcoming Shorts: gate check",
        "",
        f"Written by `gate_upcoming.py` at {now.astimezone(LONDON):%Y-%m-%d %H:%M} London for Shorts scheduled in the next {a.days} days. Don't edit by hand.",
        "",
    ]
    if not rows:
        lines += ["No scheduled Shorts in the window.", ""]
    else:
        lines += ["| Airs (London) | Short | In library | Gate |", "|---|---|---|---|"]
        details = []
        missing = [t for t in ("ffprobe", "ffmpeg") if not shutil.which(t)]
        if missing:   # a tool problem on this machine, not a fault in any Short: say so instead of FAIL (8 Oct 2026)
            details.append(f"### Not checked: {', '.join(missing)} not on PATH\n\nFix the job's PATH and re-run; no Short was judged.\n")
        for r in rows:
            f = (a.media_root / r["file"]).expanduser() if r["file"] else None
            lib = in_library(r["id"])
            want = uploads.get("videos", {}).get(r["id"], {}).get("sha256")
            hit = staged(r["id"], f, a.cache, want) if f else None
            meta_arg: list[str] = []
            if hit:
                f, meta_arg = hit[0], ["--meta", str(hit[1])]
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
                if a.add and not lib:
                    code, out = run([sys.executable, str(GATE), "add", "--id", r["id"], "--date", r["air"], "--title", r["title"],
                                     "--file", str(f), "--status", "scheduled", "--source", "gate_upcoming"])
                    lib = code == 0 and in_library(r["id"])
                    if code:
                        details.append(f"### {r['id']}: library add failed\n\n```\n{out[-1500:]}\n```\n")
                # The one Chief-OK'd 50-60 s length-test Short (UPLOADS.json "lengthTest": true; AGENTS.md Packaging, 11 Oct 2026)
                # Run with --report-only so already-uploaded scheduled Shorts keep their existing PASS verdict while
                # listing any new 60% stayed-to-watch rules they would fail under Details (J0918, 24 Oct 2026).
                code, out = run([sys.executable, str(GATE), "check", str(f), "--air-date", r["air"], "--id", r["id"], "--report-only"]
                                + meta_arg + (["--length-test"] if r.get("length_test") else []))
                used = waived(f, fail_lines(out)) if code else None
                stayed_notes = report_only_lines(out)
                verdict = "PASS" if code == 0 else ("PASS (waived)" if used else "**FAIL**")
                if used:
                    details.append(f"### {r['id']}: FAIL waived\n\n" + "\n".join(f"- {w['fail']}: waived by {w.get('waived_by', '?')}" for w in used) + "\n")
                elif code:
                    details.append(f"### {r['id']}: FAIL\n\n```\n{out[-3000:]}\n```\n")
                if stayed_notes:
                    details.append(f"### {r['id']}: report-only (would fail 60% stayed gate)\n\n" + "\n".join(f"- {n}" for n in stayed_notes) + "\n")
            lines.append(f"| {r['air']} {london_time(r['publishAt'])} | [{r['title']}](https://youtu.be/{r['id']}) `{r['id']}` | {'yes' if lib else '**no**'} | {verdict} |")
        lines.append("")
        if details:
            lines += ["## Details", ""] + details
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text("\n".join(lines) + "\n")
    print(f"gate_upcoming: {len(rows)} scheduled Short(s) checked -> {a.out}")
    return 0


def london_time(iso: str) -> str:
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(LONDON).strftime("%H:%M")


if __name__ == "__main__":
    sys.exit(main())
