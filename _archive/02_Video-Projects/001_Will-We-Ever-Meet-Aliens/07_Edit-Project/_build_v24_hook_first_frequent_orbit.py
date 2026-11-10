#!/usr/bin/env python3
"""Build v24: immediate hook, delayed brand sting, and more frequent Orbit."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDIT = ROOT / "07_Edit-Project"
BASE_SCRIPT = EDIT / "_build_v23_interactive_orbit.py"
CACHE = EDIT / "_render_cache_v24"
MIX_DIR = EDIT / "_mix_work_v24"
SOURCE_BED = EDIT / "_render_cache_v21/picture_bed_no_orbit.mp4"
SOURCE_MIX = EDIT / "_mix_work_v19/final_mix.wav"
HOOK_FIRST_BED = CACHE / "picture_bed_hook-first.mp4"
HOOK_FIRST_MIX = MIX_DIR / "final_mix_hook-first.wav"
OUT = ROOT / "09_Final-Export/aliens_broadcast_v24_hook-first_frequent-orbit.mp4"
OUT_PIC = ROOT / "09_Final-Export/aliens_broadcast_v24_hook-first_frequent-orbit_pic.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v24_PROOF_hook-first_frequent-orbit_120s.mp4"
PROOF_PIC = ROOT / "09_Final-Export/_v24_proof_picture.mp4"
MANIFEST = EDIT / "ORBIT_PERFORMANCES_v24.json"

# The original 0.75-second brand sting is moved after the opening question.
# Reordering the exact same interval in both picture and mix retains sync and
# leaves every shot after 11.822 seconds at its original timeline position.
BRAND_DURATION = 0.75
INSERT_AT_SOURCE = 11.822


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def make_hook_first_sources() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    MIX_DIR.mkdir(parents=True, exist_ok=True)

    if not HOOK_FIRST_BED.exists():
        fc = (
            f"[0:v]trim=start={BRAND_DURATION}:end={INSERT_AT_SOURCE},"
            "setpts=PTS-STARTPTS[a];"
            f"[0:v]trim=start=0:end={BRAND_DURATION},setpts=PTS-STARTPTS[b];"
            f"[0:v]trim=start={INSERT_AT_SOURCE},setpts=PTS-STARTPTS[c];"
            "[a][b][c]concat=n=3:v=1:a=0[v]"
        )
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(SOURCE_BED), "-filter_complex", fc, "-map", "[v]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(HOOK_FIRST_BED),
        ])

    if not HOOK_FIRST_MIX.exists():
        fc = (
            f"[0:a]atrim=start={BRAND_DURATION}:end={INSERT_AT_SOURCE},"
            "asetpts=PTS-STARTPTS[a];"
            f"[0:a]atrim=start=0:end={BRAND_DURATION},asetpts=PTS-STARTPTS[b];"
            f"[0:a]atrim=start={INSERT_AT_SOURCE},asetpts=PTS-STARTPTS[c];"
            "[a][b][c]concat=n=3:v=0:a=1[aout]"
        )
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(SOURCE_MIX), "-filter_complex", fc, "-map", "[aout]",
            "-c:a", "pcm_s24le", "-ar", "48000", "-ac", "2",
            str(HOOK_FIRST_MIX),
        ])


def load_base():
    spec = importlib.util.spec_from_file_location("orbit_v23", BASE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EXTRA_EVENTS = [
    {"section": "02_galaxy-scale",  "start": 73.334,  "end": 78.158,  "pattern": "watch",   "purpose": "stay with the habitable-world visual"},
    {"section": "03_exoplanets",    "start": 133.558, "end": 141.558, "pattern": "react",   "purpose": "react to the Drake possibilities"},
    {"section": "04_fermi-paradox", "start": 182.828, "end": 186.828, "pattern": "think",   "purpose": "consider the paradox"},
    {"section": "05_great-filter",  "start": 255.878, "end": 262.937, "pattern": "think",   "purpose": "weigh the filter's timing"},
    {"section": "06_explanations",  "start": 337.724, "end": 345.724, "pattern": "watch",   "purpose": "follow the quiet-civilisation theory"},
    {"section": "07_detection",     "start": 431.191, "end": 439.191, "pattern": "present", "purpose": "guide the search methods"},
    {"section": "08_first-contact", "start": 513.000, "end": 519.000, "pattern": "watch",   "purpose": "watch the implications unfold"},
    {"section": "08_first-contact", "start": 539.000, "end": 546.000, "pattern": "react",   "purpose": "react to possible first evidence"},
    {"section": "09_conclusion",    "start": 566.660, "end": 574.660, "pattern": "think",   "purpose": "reflect on what the silence says about us"},
]


def configure(module) -> None:
    module.BED = HOOK_FIRST_BED
    module.MIX = HOOK_FIRST_MIX
    module.OUT = OUT
    module.OUT_PIC = OUT_PIC
    module.PROOF = PROOF
    module.PROOF_PIC = PROOF_PIC
    module.MANIFEST = MANIFEST
    module.EVENTS = sorted(module.EVENTS + EXTRA_EVENTS, key=lambda item: item["start"])


def update_manifest() -> None:
    data = json.loads(MANIFEST.read_text())
    data.update({
        "version": 24,
        "rule": "hook first; delayed brand sting; frequent interactive lower-right host",
        "hook_first": True,
        "brand_sting_start_seconds": round(INSERT_AT_SOURCE - BRAND_DURATION, 3),
        "brand_sting_duration_seconds": BRAND_DURATION,
        "source_version_preserved": 23,
        "output": str(OUT),
    })
    MANIFEST.write_text(json.dumps(data, indent=2))


def main(mode: str) -> None:
    make_hook_first_sources()
    module = load_base()
    configure(module)
    module.main(mode)
    update_manifest()


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "proof")
