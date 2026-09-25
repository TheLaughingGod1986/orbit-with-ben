#!/usr/bin/env python3
"""021 Saturn rings VO — Ben Orbit Narrator only.

Auth: el_auth.load_token() — never print tokens.
Voice/model: orbit_voice (kDch6ACCIpqgQ0NsU9kk / eleven_v3).
"""
from __future__ import annotations

import hashlib
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

TXT = HERE / "parts/saturn_rings_vo_v01.txt"
MP3 = HERE / "parts/saturn_rings_vo_v01.mp3"
WAV = HERE / "parts/saturn_rings_vo_v01.wav"
STATUS = HERE / "VO_STATUS.md"


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def chunks(text: str, limit: int = 4500) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    size = 0
    for para in text.split("\n\n"):
        piece = para.strip()
        if not piece:
            continue
        extra = len(piece) + (2 if buf else 0)
        if buf and size + extra > limit:
            parts.append("\n\n".join(buf))
            buf = [piece]
            size = len(piece)
        else:
            buf.append(piece)
            size += extra
    if buf:
        parts.append("\n\n".join(buf))
    for part in parts:
        if len(part) > 5000:
            raise SystemExit(f"chunk still too long: {len(part)}")
    return parts


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
    parts = chunks(text)
    print(f"auth={mode} voice={VOICE_ID} model={MODEL_ID} chars={len(text)} chunks={len(parts)}", flush=True)
    wavs: list[Path] = []
    for i, part in enumerate(parts, start=1):
        mp3 = HERE / "parts" / f"saturn_rings_vo_v01_c{i}.mp3"
        wav = HERE / "parts" / f"saturn_rings_vo_v01_c{i}.wav"
        print(f"chunk {i} chars={len(part)}", flush=True)
        speak(token, mode, part, mp3)
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(mp3), "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(wav),
            ],
            check=True,
        )
        wavs.append(wav)
    concat = HERE / "parts" / "concat.txt"
    concat.write_text("".join(f"file '{w.name}'\n" for w in wavs))
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat),
            "-c", "copy", str(WAV),
        ],
        check=True,
        cwd=HERE / "parts",
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(WAV), "-c:a", "libmp3lame", "-b:a", "128k", str(MP3),
        ],
        check=True,
    )
    body = MP3.read_bytes()
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(MP3), "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(WAV),
        ],
        check=True,
    )
    dur = probe_dur(WAV)
    sha = hashlib.sha256(MP3.read_bytes()).hexdigest()
    STATUS.write_text(
        f"""# VO status — Saturn rings

| Field | Value |
|---|---|
| Status | DONE |
| Voice | Ben Orbit Narrator (`{VOICE_ID}`) |
| Model | `{MODEL_ID}` |
| Duration | {dur:.2f}s ({dur/60:.2f} min) |
| Words | {len(text.split())} |
| SHA-256 | `{sha}` |
| Updated | {time.strftime('%Y-%m-%d %H:%M %Z')} |
"""
    )
    print(f"SAVED {MP3} {len(body)} bytes {dur:.2f}s", flush=True)


if __name__ == "__main__":
    main()
