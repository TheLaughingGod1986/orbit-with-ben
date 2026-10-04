#!/usr/bin/env python3
"""022 Sun Short Mon 19 VO — Ben Orbit Narrator LOCK (orbit_voice)."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = Path("/Users/benjaminoats/YouTube/orbit-with-ben/04_Audio/tools")
sys.path.insert(0, str(TOOLS))

from el_auth import load_token  # noqa: E402
from el_client import request  # noqa: E402
from orbit_voice import MODEL_ID, VOICE_ID, VOICE_SETTINGS  # noqa: E402

TXT = HERE / "mon19_brighter_fuel_vo_v01.txt"
MP3 = HERE / "mon19_brighter_fuel_vo_v01.mp3"
WAV = HERE / "mon19_brighter_fuel_vo_v01.wav"
STATUS = HERE / "VO_STATUS.md"
CREDITS = HERE / "credits_before_after.json"


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def sub_chars(token: str, mode: str) -> dict:
    code, body, _ = request(
        "GET", "/v1/user/subscription", token, mode,
        accept="application/json", timeout=60,
    )
    if code != 200:
        raise SystemExit(f"subscription failed {code}: {body[:300]!r}")
    data = json.loads(body.decode() if isinstance(body, (bytes, bytearray)) else body)
    return {
        "character_count": data.get("character_count"),
        "character_limit": data.get("character_limit"),
        "tier": data.get("tier"),
        "status": data.get("status"),
    }


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


def main() -> None:
    text = TXT.read_text().strip()
    if not text:
        raise SystemExit("Spoken text empty")
    token, mode = load_token()
    before = sub_chars(token, mode)
    print(
        f"auth={mode} voice={VOICE_ID} model={MODEL_ID} "
        f"settings={VOICE_SETTINGS} chars={len(text)} words={len(text.split())} "
        f"credits_before={before['character_count']}/{before['character_limit']}",
        flush=True,
    )
    speak(token, mode, text, MP3)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(MP3), "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(WAV),
        ],
        check=True,
    )
    after = sub_chars(token, mode)
    dur = probe_dur(WAV)
    body = MP3.read_bytes()
    sha = hashlib.sha256(body).hexdigest()
    credits = {
        "before": before,
        "after": after,
        "delta_characters": (after["character_count"] or 0) - (before["character_count"] or 0),
        "spoken_chars": len(text),
        "spoken_words": len(text.split()),
        "duration_s": round(dur, 3),
        "sha256": sha,
        "updated": time.strftime("%Y-%m-%d %H:%M %Z"),
    }
    CREDITS.write_text(json.dumps(credits, indent=2) + "\n")
    STATUS.write_text(
        f"""# VO status — Sun 022 Short Mon 19 (brighter / fuel)

| Field | Value |
|---|---|
| Status | DONE |
| Script | SUN_SHORTS_SCRIPTS_v01.md §1 Mon 19 (prose only) |
| Voice | Ben Orbit Narrator (`{VOICE_ID}`) |
| Model | `{MODEL_ID}` |
| Settings | {VOICE_SETTINGS} |
| Duration | {dur:.2f}s |
| Words | {len(text.split())} |
| Spoken chars | {len(text)} |
| Credits before | {before['character_count']} / {before['character_limit']} |
| Credits after | {after['character_count']} / {after['character_limit']} |
| Credits delta | {credits['delta_characters']} |
| SHA-256 | `{sha}` |
| TXT | `{TXT}` |
| MP3 | `{MP3}` |
| WAV | `{WAV}` |
| Updated | {time.strftime('%Y-%m-%d %H:%M %Z')} |
"""
    )
    print(
        f"SAVED {MP3} {len(body)} bytes {dur:.2f}s sha={sha[:12]} "
        f"credits {before['character_count']}->{after['character_count']} "
        f"delta={credits['delta_characters']}",
        flush=True,
    )


if __name__ == "__main__":
    main()
