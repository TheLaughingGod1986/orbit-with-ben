#!/usr/bin/env python3
"""Saturn VO v02 — splice Ben's Olympic-pool open + Cassini 'around a hundred' into v01.

Keeps the locked Ben Orbit Narrator take for the body. Re-records only:
  1) opening through the stay-with-me promise (before Look along the sheet)
  2) Cassini lifetime line (Add it to the books … around a hundred million years)

Auth: el_auth.load_token() — never print tokens.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = HERE / "parts"
TOOLS = Path("/Users/benjaminoats/YouTube/orbit-with-ben/04_Audio/tools")
sys.path.insert(0, str(TOOLS))

from el_auth import load_token  # noqa: E402
from el_client import request  # noqa: E402
from orbit_voice import MODEL_ID, VOICE_ID, VOICE_SETTINGS  # noqa: E402

V01_WAV = PARTS / "saturn_rings_vo_v01.wav"
STT = PARTS / "_align_v01" / "saturn-rings-vo-v01_stt_raw.json"
OUT_WAV = PARTS / "saturn_rings_vo_v02.wav"
OUT_MP3 = PARTS / "saturn_rings_vo_v02.mp3"
OUT_M4A = PARTS / "saturn_rings_vo_v02.m4a"
WORK = PARTS / "_splice_v02"
UAT_DIR = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
)
STATUS = HERE / "VO_STATUS.md"

# STT anchors on v01 (scribe_v2, 2026-09-30)
LOOK_ALONG_START = 36.34  # "Look along the sheet…"
ADD_IT_START = 339.60  # "Add it to the books…"
AFTER_YEARS_START = 346.88  # "So how long does the bright sheet have?"

OPEN_TEXT = (
    "Every half hour, Saturn's rings lose enough ice to fill an Olympic swimming pool. "
    "It's raining into the planet right now. So how long do the rings have left? "
    "Stay with me, and you'll see where the ice goes, what the rings looked like when they were new, "
    "and Saturn with nothing around it at all."
)

CASSINI_TEXT = (
    "Add it to the books, and the sheet's remaining life drops to around a hundred million years."
)


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


def mp3_to_wav(mp3: Path, wav: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(mp3),
            "-c:a",
            "pcm_s16le",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(wav),
        ],
        check=True,
    )


def cut_wav(src: Path, dest: Path, start: float | None, end: float | None) -> None:
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-i", str(src)]
    if end is not None:
        # duration from start (or 0) to end
        t0 = start or 0.0
        cmd += ["-t", f"{end - t0:.3f}"]
    cmd += ["-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(dest)]
    subprocess.run(cmd, check=True)


def main() -> None:
    if not V01_WAV.is_file():
        raise SystemExit(f"missing {V01_WAV}")
    WORK.mkdir(parents=True, exist_ok=True)

    token, mode = load_token()
    print(
        f"auth={mode} voice={VOICE_ID} model={MODEL_ID} "
        f"look={LOOK_ALONG_START} add={ADD_IT_START} after={AFTER_YEARS_START}",
        flush=True,
    )

    open_mp3 = WORK / "open_v02.mp3"
    open_wav = WORK / "open_v02.wav"
    cassini_mp3 = WORK / "cassini_v02.mp3"
    cassini_wav = WORK / "cassini_v02.wav"

    print(f"TTS open chars={len(OPEN_TEXT)}", flush=True)
    speak(token, mode, OPEN_TEXT, open_mp3)
    mp3_to_wav(open_mp3, open_wav)
    print(f"  open {probe_dur(open_wav):.2f}s", flush=True)

    print(f"TTS cassini chars={len(CASSINI_TEXT)}", flush=True)
    speak(token, mode, CASSINI_TEXT, cassini_mp3)
    mp3_to_wav(cassini_mp3, cassini_wav)
    print(f"  cassini {probe_dur(cassini_wav):.2f}s", flush=True)

    mid = WORK / "mid_from_v01.wav"
    tail = WORK / "tail_from_v01.wav"
    cut_wav(V01_WAV, mid, LOOK_ALONG_START, ADD_IT_START)
    cut_wav(V01_WAV, tail, AFTER_YEARS_START, None)
    print(
        f"  mid {probe_dur(mid):.2f}s  tail {probe_dur(tail):.2f}s",
        flush=True,
    )

    concat = WORK / "concat.txt"
    pieces = [open_wav, mid, cassini_wav, tail]
    concat.write_text("".join(f"file '{p.resolve()}'\n" for p in pieces))
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-c",
            "copy",
            str(OUT_WAV),
        ],
        check=True,
    )

    # Phone-friendly masters
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(OUT_WAV),
            "-c:a",
            "libmp3lame",
            "-b:a",
            "128k",
            str(OUT_MP3),
        ],
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(OUT_WAV),
            "-c:a",
            "aac",
            "-b:a",
            "96k",
            str(OUT_M4A),
        ],
        check=True,
    )

    dur = probe_dur(OUT_WAV)
    sha_wav = hashlib.sha256(OUT_WAV.read_bytes()).hexdigest()
    sha_mp3 = hashlib.sha256(OUT_MP3.read_bytes()).hexdigest()
    sha_m4a = hashlib.sha256(OUT_M4A.read_bytes()).hexdigest()

    listen_wav = UAT_DIR / "saturn_long_vo_v02_LISTEN.wav"
    listen_m4a = UAT_DIR / "saturn_long_vo_v02_LISTEN.m4a"
    UAT_DIR.mkdir(parents=True, exist_ok=True)
    listen_wav.write_bytes(OUT_WAV.read_bytes())
    listen_m4a.write_bytes(OUT_M4A.read_bytes())

    meta = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "voice": VOICE_ID,
        "model": MODEL_ID,
        "duration_seconds": dur,
        "splices": {
            "open_text": OPEN_TEXT,
            "cassini_text": CASSINI_TEXT,
            "v01_mid": [LOOK_ALONG_START, ADD_IT_START],
            "v01_tail_from": AFTER_YEARS_START,
        },
        "sha256": {"wav": sha_wav, "mp3": sha_mp3, "m4a": sha_m4a},
        "bytes": {
            "wav": OUT_WAV.stat().st_size,
            "mp3": OUT_MP3.stat().st_size,
            "m4a": OUT_M4A.stat().st_size,
        },
        "listen": {"wav": str(listen_wav), "m4a": str(listen_m4a)},
        "stt_source": str(STT),
    }
    (WORK / "SPLICE_META.json").write_text(json.dumps(meta, indent=2) + "\n")

    STATUS.write_text(
        f"""# VO status — Saturn rings

| Field | Value |
|---|---|
| Status | **DONE v02** (Olympic-pool open + Cassini “around a hundred”; body from v01) |
| Spoken text | `parts/saturn_rings_vo_v02.txt` |
| Voice | Ben Orbit Narrator (`{VOICE_ID}`) |
| Model | `{MODEL_ID}` via `orbit_voice.py` |
| Duration | {dur:.2f}s ({dur/60:.2f} min) |
| Master wav | `{OUT_WAV}` |
| Master mp3 | `{OUT_MP3}` |
| Master m4a | `{OUT_M4A}` ({OUT_M4A.stat().st_size} bytes) |
| Listen wav | `{listen_wav}` |
| Listen m4a | `{listen_m4a}` |
| SHA-256 (wav) | `{sha_wav}` |
| SHA-256 (mp3) | `{sha_mp3}` |
| SHA-256 (m4a) | `{sha_m4a}` |
| Updated | {time.strftime('%Y-%m-%d %H:%M %Z')} |

Do not force-commit `.wav`/`.mp3`/`.m4a` (gitignored). Ben listen = sign-off.
"""
    )
    print(json.dumps(meta, indent=2), flush=True)
    print(f"SAVED {OUT_WAV} {dur:.2f}s m4a={OUT_M4A.stat().st_size}", flush=True)


if __name__ == "__main__":
    main()
