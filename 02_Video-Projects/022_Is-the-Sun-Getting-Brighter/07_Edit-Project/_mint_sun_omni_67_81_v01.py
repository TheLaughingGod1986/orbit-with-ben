#!/usr/bin/env python3
"""Sun 022 Omni Orbit beats, shot list rows 67 and 81 (J0012, Claude #99 6042034289).

One take each, no retry loop. Vertex Omni at `global` on the free-trial credit only, never AI Studio prepaid.
Start frames come from _composite_sun_orbit_starts_v01.py (orbit_source sidecars, so the guard runs).
A take that misses (wrong look, text in frame, Orbit large) keeps the row's listed fallback; no second take without Claude.
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
REPORT = HERE / "omni_gen_report_67_81_v01.json"
# Row 67 prompt v01b: the first submit (17:25Z) was refused as content_blocked before any take; one plainer resubmit.
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
SUN_LOCK = " The Sun stays a glowing star exactly as in the start frame: not a planet, no rings, no bands, no surface map."

ROWS = [
    {
        "row": 67,
        "id": "sun_orbit_row67_omni_v01",
        "start": "sun_orbit_row67_start_v01.png",
        "fallback": "NASA s04-41-1206 push 4%",
        "prompt": (
            "Calm space view. Top right, part off frame, a dim warm orange glowing star in the black sky. "
            "Below, a blue ocean and white cloud horizon stays as in the start frame. "
            "Orbit floats small near the dim star, visor tilted up towards it, and slowly lifts one hand. "
            "The camera barely drifts." + SUN_LOCK + ORBIT_LOCK + " No text, no logo. Silent picture only."
        ),
    },
    {
        "row": 81,
        "id": "sun_orbit_row81_omni_v01",
        "start": "sun_orbit_row81_start_v01.png",
        "fallback": "NASA iss071e364425 push 4%",
        "prompt": (
            "Space above Earth's horizon in the far future. Top left, part off frame, a brighter white-hot Sun. "
            "Below, a thin bright skin of cloud along the horizon stays as in the start frame. Orbit stays small and "
            "low in frame, tips towards the brighter disc, then turns and tips towards the thin bright skin of cloud. "
            "The camera barely drifts." + SUN_LOCK + ORBIT_LOCK + " No text, no logo. Silent picture only."
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
              "request": "Claude #99 6042034289 (J0012): one take each", "rows": []}
    for r in ROWS:
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
