#!/usr/bin/env python3
"""028 Gliese 710 Omni Orbit beats, SHOT_LIST_v01 rows 8 and 23 (J0850, Chief price PASS).

Vertex Omni at `global` on the monthly promo credit (£71.02 Available, £0.00 Used).
Start frames come from _composite_028_orbit_starts_v01.py (orbit_source sidecars, so the guard runs).
Both starts are starfields with no planet in frame.
Max 1 take + 1 retry each (£2.60 cap); stop immediately on any billing/quota error.
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
REPORT = HERE / "omni_gen_report_8_23_v01.json"
PROJECT = "gen-lang-client-0538779324"
LOCATION = "global"
MODEL = "gemini-omni-flash-preview"
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_gemini_omni import generate_omni_clip  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

ORBIT_LOCK = (
    " IDENTITY LOCK: Exactly one solid matte orange floating robot (Orbit) — one large black "
    "curved visor as the whole face, two cream circular eyes with dark pupils, stubby orange "
    "arms with dark three-finger hands, one antenna with glowing bulb, one soft underside glow, "
    "NO LEGS. Orbit stays small in frame. Not a toy, not a second face, not a second Orbit, no HUD, no text, no logo."
)

ROWS = [
    {
        "row": 8,
        "id": "orbit_binoculars_omni_v01",
        "start": "orbit_binoculars_start_v01.png",
        "fallback": "`drift` code graphic holds row 8",
        "prompt": (
            "Dark grassy hilltop at night under a deep starfield with a faint warm orange star in the upper-left sky, "
            "exactly as in the start frame. No planet, no moon, no globe. Orbit hovers just above the dark hill crest, "
            "lifts a small pair of dark binoculars to his visor and sweeps the starry sky, pauses on the faint orange "
            "dot upper left, lowers the binoculars, and tilts his visor thoughtfully. The starfield and hill stay steady; "
            "the camera barely drifts."
            + ORBIT_LOCK
            + " No text, no numbers, no logo. Silent picture only."
        ),
    },
    {
        "row": 23,
        "id": "orbit_ice_omni_v01",
        "start": "orbit_ice_start_v01.png",
        "fallback": "`shell` code graphic end frame holds row 23",
        "prompt": (
            "Deep outer space on a dark starfield with slow, dark grey craggy lumps of ice floating around, "
            "exactly as in the start frame. No planet, no moon, no globe, no ground. Orbit floats calmly beside "
            "the dark lump of ice to his right, reaches out one small three-finger hand to tap the ice lump gently, "
            "and watches with curious cream eyes as the lump turns very slowly in the dark. The camera barely drifts."
            + ORBIT_LOCK
            + " No text, no numbers, no logo. Silent picture only."
        ),
    },
]


def sheet(mp4: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.parent / f"_tmp_{dest.stem}"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    dur = float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nk=1:nw=1", str(mp4)],
            text=True,
        ).strip()
        or 6
    )
    frames = []
    for i, t in enumerate(dur * k for k in (0.05, 0.2, 0.4, 0.6, 0.8, 0.95)):
        f = tmp / f"f{i}.png"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-vf", "scale=320:-2", str(f)],
            check=True,
        )
        frames.append(f)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", *[x for f in frames for x in ("-i", str(f))], "-filter_complex", "hstack=inputs=6", "-frames:v", "1", str(dest)],
        check=True,
    )
    shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    from google import genai

    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    os.environ["OWB_AGENT"] = "gemini"
    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    report = {
        "startedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "engine": "vertex_omni",
        "project": PROJECT,
        "location": LOCATION,
        "model": MODEL,
        "request": "Chief J0850 price PASS (Claude, acting Chief, 22 Oct 2026): 1 take + max 1 retry each (£2.60 cap)",
        "rows": [],
    }
    if REPORT.exists():
        report["rows"] = [x for x in json.loads(REPORT.read_text()).get("rows", []) if x.get("status") == "ok"]
    only = {a for a in sys.argv[1:]}
    for r in ROWS:
        if only and r["id"] not in only:
            continue
        report["rows"] = [x for x in report["rows"] if x["id"] != r["id"]]
        dest = OUT / f"{r['id']}.mp4"
        entry = {k: r[k] for k in ("row", "id", "start", "fallback", "prompt")}
        if dest.exists() and dest.stat().st_size > 200_000:
            sh = SHEETS / f"{r['id']}_6frame.jpg"
            if not sh.exists():
                sheet(dest, sh)
            entry.update(
                status="skip",
                note="take already exists; no second take without Chief",
                sheet=sh.name,
                bytes=dest.stat().st_size,
                sha256=subprocess.check_output(["shasum", "-a", "256", str(dest)], text=True).split()[0],
            )
            report["rows"].append(entry)
            continue
        t0 = time.time()
        try:
            meta = generate_omni_clip(
                client,
                r["prompt"],
                dest,
                orbit_ref=STARTS / r["start"],
                orbit_shot=True,
                model=MODEL,
                aspect_ratio="16:9",
            )
            veo.strip_audio(dest)
            sh = SHEETS / f"{r['id']}_6frame.jpg"
            sheet(dest, sh)
            entry.update(meta)
            entry.update(
                status="ok",
                wall_seconds=round(time.time() - t0, 1),
                sheet=sh.name,
                bytes=dest.stat().st_size,
                sha256=subprocess.check_output(["shasum", "-a", "256", str(dest)], text=True).split()[0],
            )
        except BaseException as e:  # noqa: BLE001
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
