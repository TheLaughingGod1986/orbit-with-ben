#!/usr/bin/env python3
"""Saturn week Shorts VO — Mon Saturn tease + Fri Black Dwarf. Ben Orbit Narrator only."""
from __future__ import annotations

import hashlib
import subprocess
import sys
import time
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
TOOLS = REPO / "04_Audio" / "tools"
sys.path.insert(0, str(TOOLS))

from el_auth import load_token  # noqa: E402
from el_client import request  # noqa: E402
from orbit_voice import MODEL_ID, VOICE_ID, VOICE_SETTINGS  # noqa: E402

JOBS = [
    {
        "name": "monday_saturn",
        "txt": REPO
        / "02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/10_Shorts/monday_saturn_tease/monday_saturn_short_vo_v01.txt",
        "mp3": REPO
        / "02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/10_Shorts/monday_saturn_tease/monday_saturn_short_vo_v01.mp3",
        "wav": REPO
        / "02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/10_Shorts/monday_saturn_tease/monday_saturn_short_vo_v01.wav",
        "listen": Path(
            "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/monday_saturn_short_vo_v01_LISTEN.wav"
        ),
        "status": REPO
        / "02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/10_Shorts/monday_saturn_tease/VO_STATUS.md",
        "label": "Monday Saturn Short",
    },
    {
        "name": "friday_black_dwarf",
        "txt": REPO
        / "02_Video-Projects/005_The-Last-Star-In-The-Universe/10_Shorts/friday_2026-10-16_last_star/friday_black_dwarf_short_vo_v01.txt",
        "mp3": REPO
        / "02_Video-Projects/005_The-Last-Star-In-The-Universe/10_Shorts/friday_2026-10-16_last_star/friday_black_dwarf_short_vo_v01.mp3",
        "wav": REPO
        / "02_Video-Projects/005_The-Last-Star-In-The-Universe/10_Shorts/friday_2026-10-16_last_star/friday_black_dwarf_short_vo_v01.wav",
        "listen": Path(
            "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/friday_black_dwarf_short_vo_v01_LISTEN.wav"
        ),
        "status": REPO
        / "02_Video-Projects/005_The-Last-Star-In-The-Universe/10_Shorts/friday_2026-10-16_last_star/VO_STATUS.md",
        "label": "Friday Black Dwarf Short",
    },
]


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def speak(token: str, mode: str, text: str, dest: Path) -> None:
    code, body, _hdrs = request(
        "POST",
        f"/v1/text-to-speech/{VOICE_ID}",
        token,
        mode,
        data={"text": text, "model_id": MODEL_ID, "voice_settings": VOICE_SETTINGS},
        query="output_format=mp3_44100_128",
        accept="audio/mpeg",
        timeout=600,
    )
    if code != 200:
        raise SystemExit(f"TTS failed {code}: {body[:400]!r}")
    dest.write_bytes(body)


def run_one(job: dict, token: str, mode: str) -> None:
    text = job["txt"].read_text().strip()
    if not text:
        raise SystemExit(f"empty spoken text: {job['txt']}")
    job["mp3"].parent.mkdir(parents=True, exist_ok=True)
    print(f"{job['name']} chars={len(text)} words={len(text.split())}", flush=True)
    speak(token, mode, text, job["mp3"])
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(job["mp3"]),
            "-c:a",
            "pcm_s16le",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(job["wav"]),
        ],
        check=True,
    )
    job["listen"].parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(job["wav"]), str(job["listen"])], check=True)
    dur = probe_dur(job["wav"])
    sha = hashlib.sha256(job["wav"].read_bytes()).hexdigest()
    job["status"].write_text(
        f"""# VO status — {job['label']}

| Field | Value |
|---|---|
| Status | DONE |
| Voice | Ben Orbit Narrator (`{VOICE_ID}`) |
| Model | `{MODEL_ID}` |
| Duration | {dur:.2f}s |
| Words | {len(text.split())} |
| Master path | `{job['wav']}` |
| Listen path | `{job['listen']}` |
| SHA-256 (wav) | `{sha}` |
| Updated | {time.strftime('%Y-%m-%d %H:%M %Z')} |
"""
    )
    print(f"SAVED {job['wav']} {dur:.2f}s sha={sha}", flush=True)


def main() -> None:
    token, mode = load_token()
    print(f"auth={mode} voice={VOICE_ID} model={MODEL_ID}", flush=True)
    for job in JOBS:
        run_one(job, token, mode)
    print("SHORTS_VO_DONE", flush=True)


if __name__ == "__main__":
    main()
