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

It writes a Markdown report (--out) and always exits 0: it reports, it never blocks the tracker. Claude reads the
report at 07:10 and decides on any FAIL (reschedule or replace a scheduled Short; nothing here touches YouTube).

  python3 gate_upcoming.py --snapshot 05_Analytics/owb/snapshots/2026-10-08.json \\
      --uploads 00_Brand/Channel-Setup/social/UPLOADS.json --media-root ~/YouTube/orbit-with-ben \\
      --out 05_Analytics/owb/UPCOMING_SHORTS_GATE.md --add
"""
from __future__ import annotations

import argparse
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
            out.append({"id": v["id"], "title": v.get("title", ""), "publishAt": at, "air": london_date(at), "file": entry.get("file")})
    return sorted(out, key=lambda r: r["publishAt"])


def in_library(vid: str) -> bool:
    if not LIB_JSON.exists():
        return False
    return any(e["id"] == vid for e in json.loads(LIB_JSON.read_text()).get("entries", []))


def fail_lines(output: str) -> list[str]:
    """The FAIL reasons in a `gate_shorts_open.py check` printout (indented lines, not the file's summary line)."""
    return [ln.strip()[len("FAIL"):].strip() for ln in output.splitlines() if ln.startswith(" ") and ln.strip().startswith("FAIL ")]


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
    a = ap.parse_args(argv)

    now = datetime.now(timezone.utc)
    rows = upcoming(json.loads(a.snapshot.read_text()), json.loads(a.uploads.read_text()), now, a.days)
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
            if not f or not f.exists():
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
                code, out = run([sys.executable, str(GATE), "check", str(f), "--air-date", r["air"], "--id", r["id"]])
                used = waived(f, fail_lines(out)) if code else None
                verdict = "PASS" if code == 0 else ("PASS (waived)" if used else "**FAIL**")
                if used:
                    details.append(f"### {r['id']}: FAIL waived\n\n" + "\n".join(f"- {w['fail']}: waived by {w.get('waived_by', '?')}" for w in used) + "\n")
                elif code:
                    details.append(f"### {r['id']}: FAIL\n\n```\n{out[-3000:]}\n```\n")
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
