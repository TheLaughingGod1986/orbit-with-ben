#!/usr/bin/env python3
"""Part 02 VO — Ben Orbit Narrator (kDch6ACCIpqgQ0NsU9kk). Exact master-script lines."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path("/Users/ben/code/Orbit-YouTube")
TOOLS = REPO / "04_Audio/tools"
sys.path.insert(0, str(TOOLS))

from el_auth import load_token
from el_client import request
from orbit_voice import MODEL_ID, VOICE_ID, VOICE_SETTINGS

HERE = Path(__file__).resolve().parent
TXT = HERE / "parts/neutron_star_part-02_vo_v01.txt"
MP3 = HERE / "parts/neutron_star_part-02_vo_v01.mp3"
WAV = HERE / "parts/neutron_star_part-02_vo_v01.wav"


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def main() -> None:
    text = TXT.read_text().strip()
    token, mode = load_token()
    print(f"auth={mode} voice={VOICE_ID} model={MODEL_ID} chars={len(text)}", flush=True)
    code, body, _hdrs = request(
        "POST",
        f"/v1/text-to-speech/{VOICE_ID}",
        token,
        mode,
        data={"text": text, "model_id": MODEL_ID, "voice_settings": VOICE_SETTINGS},
        query="output_format=mp3_44100_128",
        accept="audio/mpeg",
        timeout=300,
    )
    if code != 200:
        raise SystemExit(f"TTS failed {code}: {body[:500]!r}")
    MP3.write_bytes(body)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(MP3), "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1", str(WAV),
        ],
        check=True,
    )
    d = probe_dur(MP3)
    print(f"SAVED {MP3} ({len(body)} bytes, {d:.2f}s)", flush=True)
    print(f"SAVED {WAV}", flush=True)


if __name__ == "__main__":
    main()
