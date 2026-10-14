#!/usr/bin/env python3
"""026 Nearest Star Omni Orbit beats, SHOT_LIST_v01 rows 11 and 24 (J0085, Claude #99 6077058676).

One take each, no retry loop. Vertex Omni at `global` on the free-trial credit only (£5 floor), never AI Studio prepaid.
Start frames come from _composite_nearest_star_orbit_starts_v01.py (orbit_source sidecars, so the guard runs).
Both starts are star fields with no planet in frame. Read the Vertex balance before each take; stop at
the £5 floor plus HOS's reserve (£16 on 9 Oct). Run one row per call: `python _mint_nearest_star_omni_v01.py <id>`.
A take that misses keeps the row's listed fallback; no second take without Claude.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = HERE.parent / "04_Generated-Clips/01_Raw/omni_v01"
STARTS = OUT / "starts"
SHEETS = OUT / "sheets"
REPORT = HERE / "omni_gen_report_v01.json"
PROJECT = "gen-lang-client-0538779324"
LOCATION = "global"
MODEL = "gemini-omni-flash-preview"
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_gemini_omni import generate_omni_clip  # noqa: E402

ORBIT_LOCK = (
    " IDENTITY LOCK: Exactly one solid matte orange floating robot (Orbit) — one large black "
    "curved visor as the whole face, two cream circular eyes with dark pupils, stubby orange "
    "arms with dark three-finger hands, one antenna with glowing bulb, one soft underside glow, "
    "NO LEGS. Orbit stays small in frame. Not a toy, not a second face, not a second Orbit, no HUD, no text, no logo."
)

ROWS = [
    {
        "row": "11",
        "id": "orbit_thumb_omni_v01",
        "start": "orbit_thumb_start_v01.png",
        "fallback": "`parallax` code graphic holds row 11",
        "prompt": (
            "Deep space star field, exactly as in the start frame: a bright blue-white star upper left and a small "
            "red star beside it, thousands of faint stars. No planet, no globe, no ground. Orbit hovers small at the "
            "lower right, facing the bright stars. He slowly raises one small hand at arm's length in front of his "
            "visor, like a thumb held up to the sky. He closes one eye, then opens it and closes the other, and the "
            "small red star seems to hop sideways against the background stars. Orbit tilts his visor, delighted. "
            "The camera barely drifts."
            + ORBIT_LOCK + " No text, no logo. Silent picture only."
        ),
    },
    {
        "row": "24",
        "id": "orbit_walk_omni_v01",
        "start": "orbit_walk_start_v01.png",
        "fallback": "`journey` code graphic holds row 24",
        "prompt": (
            "Deep space, a dense field of stars on black, exactly as in the start frame. No planet, no globe, no "
            "ground. Orbit hovers small on the left. With great determination he sets off, drifting forwards to the "
            "right in small brave bobs. After a moment he stops, turns his visor to look back over his shoulder at "
            "how little distance he has covered, then shakes with a happy laugh. The star field stays still; the "
            "camera barely drifts."
            + ORBIT_LOCK + " No text, no logo. Silent picture only."
        ),
    },
]


def sheet(mp4: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.parent / f"_tmp_{dest.stem}"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "default=nk=1:nw=1", str(mp4)], text=True).strip() or 6)
    frames = []
    for i, t in enumerate(dur * k for k in (0.05, 0.2, 0.4, 0.6, 0.8, 0.95)):
        f = tmp / f"f{i}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1",
                        "-vf", "scale=320:-2", str(f)], check=True)
        frames.append(f)
    subprocess.run(["ffmpeg", "-y", "-v", "error", *[x for f in frames for x in ("-i", str(f))],
                    "-filter_complex", "hstack=inputs=6", "-frames:v", "1", str(dest)], check=True)
    shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    from google import genai

    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    report = {"startedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"), "engine": "vertex_omni",
              "project": PROJECT, "location": LOCATION, "model": MODEL,
              "request": "Claude #99 6077058676 (J0085): one take each", "rows": []}
    if REPORT.exists():
        report["rows"] = [x for x in json.loads(REPORT.read_text()).get("rows", []) if x.get("status") == "ok"]
    only = {a for a in sys.argv[1:]}
    for r in ROWS:
        if only and r["id"] not in only:
            continue
        report["rows"] = [x for x in report["rows"] if x["id"] != r["id"]]
        dest = OUT / f"{r['id']}.mp4"
        entry = {k: r[k] for k in ("row", "id", "start", "fallback", "prompt")}
        if dest.exists():
            sh = SHEETS / f"{r['id']}_6frame.jpg"
            entry.update(status="skip", note="take already exists; no second take without Claude",
                         sheet=sh.name if sh.exists() else None, bytes=dest.stat().st_size,
                         sha256=subprocess.check_output(["shasum", "-a", "256", str(dest)], text=True).split()[0])
            report["rows"].append(entry)
            continue
        t0 = time.time()
        try:
            meta = generate_omni_clip(client, r["prompt"], dest, orbit_ref=STARTS / r["start"], orbit_shot=True,
                                      model=MODEL, aspect_ratio="16:9")
            sh = SHEETS / f"{r['id']}_6frame.jpg"
            sheet(dest, sh)
            entry.update(meta)
            entry.update(status="ok", wall_seconds=round(time.time() - t0, 1), sheet=sh.name,
                         bytes=dest.stat().st_size,
                         sha256=subprocess.check_output(["shasum", "-a", "256", str(dest)], text=True).split()[0])
        except BaseException as e:  # noqa: BLE001 — no retry, record and move on
            entry.update(status="fail", seconds=round(time.time() - t0, 1), error=f"{type(e).__name__}: {e}")
            if any(s in str(e).lower() for s in ("prepayment", "billing", "402", "resource_exhausted", "quota")):
                report["rows"].append(entry)
                report["stop"] = "billing"
                break
        report["rows"].append(entry)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    report["finishedAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if all(x["status"] in ("ok", "skip") for x in report["rows"]) else 1


if __name__ == "__main__":
    sys.exit(main())
