#!/usr/bin/env python3
"""Venus 023 — Omni generate queue (Claude PASS 5982425011).

Vertex Omni only (gemini-omni-flash-preview). Free-trial credit; £5 lag floor.
One take each + at most one remint if frame sheet fails. No Veo/Flow/ElevenLabs.
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

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
EP = REPO / "02_Video-Projects/023_What-Happened-To-Venus"
EDIT = EP / "07_Edit-Project"
OUT = EP / "04_Generated-Clips/01_Raw/omni_v01"
STARTS = OUT / "starts"
SHEETS = OUT / "sheets"
REPORT = EDIT / "omni_gen_report_v01.json"
IDENTITY = REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
TOOLS = REPO / "04_Audio/tools"
FLOOR_GBP = 5.0
PROJECT = "gen-lang-client-0538779324"
LOCATION = "global"  # Omni on Vertex is global-only (us-central1 -> 500)
MODEL = "gemini-omni-flash-preview"

sys.path.insert(0, str(TOOLS))
from orbit_gemini_omni import generate_omni_clip  # noqa: E402

ORBIT_LOCK = (
    " IDENTITY LOCK: Exactly one solid matte orange floating robot (Orbit) — one large black "
    "curved visor as the whole face, two cream circular eyes with dark pupils, stubby orange "
    "arms with dark three-finger hands, one antenna with glowing bulb, one soft underside glow, "
    "NO LEGS. Not a toy, not a second face, not a second Orbit, no HUD, no text, no logo."
)

PLATES = [
    {
        "id": "venus_early_ocean_cloud_omni_v01",
        "file": "venus_early_ocean_cloud_omni_v01.mp4",
        "start": "venus_early_ocean_cloud_start.png",
        "orbit": False,
        "prompt": (
            "Possible early Venus only — not documentary fact. Soft daylight under a shining "
            "white cloud deck. A shallow calm sea under bright cloud shade. Mild weather. "
            "No cities, no life, no plants, no animals, no shoreline settlements, no readable "
            "text, no logo, no title, no Orbit. Premium cinematic 3D space documentary grade. "
            "Continuous gentle camera drift. Silent picture only."
        ),
    },
    {
        "id": "venus_early_steam_lid_omni_v01",
        "file": "venus_early_steam_lid_omni_v01.mp4",
        "start": "venus_early_steam_lid_start.png",
        "orbit": False,
        "prompt": (
            "Possible early Venus only — hot dim sky with a thick steam and cloud lid overhead. "
            "Bare rock ground. No shoreline, no ocean, no puddles, no cities, no life, no text, "
            "no logo, no Orbit. Oppressive humid heat feel. Premium cinematic 3D. Continuous "
            "slow camera drift. Silent picture only."
        ),
    },
    {
        "id": "orbit_between_two_venus_omni_v01",
        "file": "orbit_between_two_venus_omni_v01.mp4",
        "start": "orbit_between_two_venus_start.png",
        "orbit": True,
        "prompt": (
            "Deep space. Two Venus worlds flank the frame: left a soft cloud-bright milder world, "
            "right a hotter steam-lidded world. Orbit floats small between them, visor tilted, "
            "turns from the left world toward the right world, asking without words."
            + ORBIT_LOCK
            + " Continuous motion. No text, no logo. Silent picture only."
        ),
    },
    {
        "id": "orbit_looks_back_earth_omni_v01",
        "file": "orbit_looks_back_earth_omni_v01.mp4",
        "start": "orbit_looks_back_earth_start.png",
        "orbit": True,
        "prompt": (
            "Near cloud-white Venus. Orbit is small in the dark, quiet, looking toward a "
            "BRIGHT BLUE POINT OF LIGHT that is Earth — a distant pinprick, NOT a blue planet "
            "edge, NOT a blue crescent, NOT a blue disk filling the frame. Cloud-white Venus "
            "fills behind him. He notices; he is not afraid."
            + ORBIT_LOCK
            + " Continuous subtle hover. No text, no logo. Silent picture only."
        ),
    },
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def six_frame_sheet(mp4: Path, dest: Path) -> None:
    """6 frames across full clip duration."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.parent / f"_tmp_{dest.stem}"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    # probe duration
    probe = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nk=1:nw=1", str(mp4),
        ],
        text=True,
    ).strip()
    dur = max(float(probe or "6"), 1.0)
    times = [dur * t for t in (0.05, 0.2, 0.4, 0.6, 0.8, 0.95)]
    frames = []
    for i, t in enumerate(times):
        f = tmp / f"f{i}.png"
        run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-ss", f"{t:.3f}", "-i", str(mp4),
                "-frames:v", "1", "-vf", "scale=320:-2",
                str(f),
            ]
        )
        frames.append(f)
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            *[x for f in frames for x in ("-i", str(f))],
            "-filter_complex", "hstack=inputs=6",
            "-frames:v", "1",
            str(dest),
        ]
    )
    shutil.rmtree(tmp, ignore_errors=True)


def sheet_ok(sheet: Path) -> bool:
    if not sheet.exists() or sheet.stat().st_size < 20_000:
        return False
    # basic: not almost-black
    try:
        from PIL import Image
        import statistics

        im = Image.open(sheet).convert("L").resize((64, 24))
        vals = list(im.getdata())
        mean = statistics.mean(vals)
        return mean > 8
    except Exception:
        return True


def make_client():
    from google import genai

    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    return genai.Client(vertexai=True, project=PROJECT, location=LOCATION)


def main() -> None:
    only = {a for a in sys.argv[1:] if not a.startswith("--")}
    OUT.mkdir(parents=True, exist_ok=True)
    SHEETS.mkdir(parents=True, exist_ok=True)
    client = make_client()
    report = {
        "startedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "engine": "vertex_omni",
        "project": PROJECT,
        "location": LOCATION,
        "model": MODEL,
        "floor_gbp": FLOOR_GBP,
        "credit_pre_gbp": 28.89,
        "plates": [],
    }
    for plate in PLATES:
        if only and plate["id"] not in only:
            continue
        dest = OUT / plate["file"]
        start = STARTS / plate["start"]
        sheet = SHEETS / f"{plate['id']}_6frame.jpg"
        entry = {"id": plate["id"], "file": plate["file"], "attempts": []}
        print(f"\n=== {plate['id']} ===", flush=True)
        if dest.exists() and dest.stat().st_size > 200_000 and sheet_ok(sheet):
            print(f"SKIP keep {dest.name}", flush=True)
            entry.update({"status": "keep", "bytes": dest.stat().st_size, "sheet": sheet.name})
            report["plates"].append(entry)
            continue
        attempts = 1
        # one remint allowed if sheet fails
        for attempt in range(1, 3):
            t0 = time.time()
            try:
                if dest.exists():
                    dest.unlink()
                meta = generate_omni_clip(
                    client,
                    plate["prompt"],
                    dest,
                    orbit_ref=start,
                    # Orbit shots: start frame must derive from ORBIT_REF (sidecar guard);
                    # identity_ref is never sent (Omni I2V takes one image). Claude 5984734583.
                    orbit_shot=plate["orbit"],
                    model=MODEL,
                    aspect_ratio="16:9",
                )
                six_frame_sheet(dest, sheet)
                ok = sheet_ok(sheet)
                att = {
                    "n": attempt,
                    "status": "ok" if ok else "sheet_fail",
                    "seconds": round(time.time() - t0, 1),
                    **meta,
                    "sheet": sheet.name,
                    "sheet_ok": ok,
                }
                entry["attempts"].append(att)
                print(f"attempt {attempt}: {att['status']} {meta}", flush=True)
                if ok:
                    entry.update(
                        {
                            "status": "ok",
                            "bytes": dest.stat().st_size,
                            "sheet": sheet.name,
                            "sha256": subprocess.check_output(
                                ["shasum", "-a", "256", str(dest)], text=True
                            ).split()[0],
                        }
                    )
                    break
                if attempt == 1:
                    print("sheet fail — remint once", flush=True)
                    continue
                entry["status"] = "sheet_fail"
            except Exception as e:
                att = {
                    "n": attempt,
                    "status": "fail",
                    "seconds": round(time.time() - t0, 1),
                    "error": f"{type(e).__name__}: {e}",
                }
                entry["attempts"].append(att)
                print(f"FAIL attempt {attempt}: {e}", flush=True)
                err_l = str(e).lower()
                if any(
                    s in err_l
                    for s in (
                        "prepayment credits are depleted",
                        "resource_exhausted",
                        "billing",
                        "quota",
                        "402",
                    )
                ):
                    entry["status"] = "billing_stop"
                    report["plates"].append(entry)
                    report["finishedAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
                    REPORT.write_text(json.dumps(report, indent=2) + "\n")
                    print("BILLING STOP — no further Omni spend", flush=True)
                    raise SystemExit(3)
                if attempt == 1:
                    time.sleep(3)
                    continue
                entry["status"] = "fail"
        report["plates"].append(entry)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")

    report["finishedAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    ok_n = sum(1 for p in report["plates"] if p.get("status") in {"ok", "keep"})
    print(f"\nDONE ok={ok_n}/{len(report['plates'])} report={REPORT}", flush=True)
    if ok_n < len([p for p in PLATES if not only or p["id"] in only]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
