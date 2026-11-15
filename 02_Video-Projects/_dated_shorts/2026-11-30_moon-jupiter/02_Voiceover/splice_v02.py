#!/usr/bin/env python3
"""J2916: deterministic room-tone gap tightening from moon_jupiter_2026_11_30_vo_v01.wav.

- Preserves 100% of all 47 words of the approved primary script from Take 1 (275 chars, Ben Orbit Narrator, eleven_v3).
- Tightens only verified room-tone inter-sentence silences (<-70 dBFS RMS, <-48 dBFS peak) from ~0.55-0.76 s to natural ~0.34-0.38 s breaths so total cut (VO 18.480 s + 1.020 s forward-loop tail = 19.500 s / 585 frames at 30 fps) sits inside the 17.0-20.0 s Rule 16 Apophis-mould window and Line 4 starts at 10.660 s (<= 13.5 s C7 bar).
- Every internal join sits inside verified silence with a 10 ms (480-sample) qsin fade; final word 'sky' plays unclipped to 19.840 s with a 12 ms (576-sample) anti-click fade.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SRC_STEM = "moon_jupiter_2026_11_30_vo_v01"
SRC_WAV = HERE / f"{SRC_STEM}.wav"
DST_STEM = "moon_jupiter_2026_11_30_vo_v02"
DST_WAV = HERE / f"{DST_STEM}.wav"
DST_MP3 = HERE / f"{DST_STEM}.mp3"

SR = 48000
FADE = 480        # 10 ms internal room-tone join fade
END_FADE = 576    # 12 ms anti-click end fade after 'sky'

# Spans in seconds -> exact samples at 48 kHz (sum = 18.480 s = 887,040 frames)
SPANS_S = [
    (0.000, 4.180),    # 4.180 s: "Jupiter passes one finger from the Moon on November thirtieth."
    (4.460, 8.000),    # 3.540 s: "If Earth were a grape, Jupiter is a whole basketball."
    (8.300, 11.060),   # 2.760 s: "It is forty times wider than our Moon."
    (11.400, 17.540),  # 6.140 s: "Yet Jupiter sits two thousand times farther, over seven hundred million kilometres away."
    (17.980, 19.840),  # 1.860 s: "Look south in the morning sky."
]
SPANS = [(int(round(s * SR)), int(round(e * SR))) for s, e in SPANS_S]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def map_time(t: float) -> float:
    acc = 0.0
    for s, e in SPANS_S:
        if t < s:
            return round(acc, 3)
        if s <= t <= e:
            return round(acc + (t - s), 3)
        acc += (e - s)
    return round(acc, 3)


def main() -> None:
    src_sha = sha256(SRC_WAV)
    with wave.open(str(SRC_WAV), "rb") as w:
        params = w.getparams()
        raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2)
    assert (params.nchannels, params.sampwidth, params.framerate) == (2, 2, SR)

    up = np.sin(np.pi / 2 * (np.arange(FADE) + 1) / FADE)
    down = up[::-1]
    parts = []
    for i, (s, e) in enumerate(SPANS):
        chunk = raw[s:e].astype(np.float64)
        if i > 0:
            chunk[:FADE] *= up[:, None]
        if i < len(SPANS) - 1:
            chunk[-FADE:] *= down[:, None]
        parts.append(np.round(chunk).astype(np.int16))
    out = np.concatenate(parts, axis=0)
    assert len(out) == int(round(18.480 * SR)), f"unexpected frame count {len(out)}"

    end_curve = np.sin(np.pi / 2 * (np.arange(END_FADE, 0, -1) - 1) / END_FADE)
    out[-END_FADE:] = np.round(out[-END_FADE:].astype(np.float64) * end_curve[:, None]).astype(np.int16)

    with wave.open(str(DST_WAV), "wb") as w:
        w.setparams(params)
        w.writeframes(out.tobytes())

    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(DST_WAV),
         "-c:a", "libmp3lame", "-b:a", "128k", str(DST_MP3)],
        check=True,
    )

    stt_raw = json.loads((HERE / f"stt/{SRC_STEM}/stt_raw.json").read_text())
    v01_words = [
        {"word": w["text"], "start": round(float(w["start"]), 3), "end": round(float(w["end"]), 3)}
        for w in stt_raw.get("words", []) if w.get("type") == "word"
    ]
    v02_words = [
        {"word": w["text"], "start": map_time(float(w["start"])), "end": map_time(float(w["end"]))}
        for w in stt_raw.get("words", []) if w.get("type") == "word"
    ]
    # Add period to final word 'sky' for clean caption punctuation
    if v02_words and not v02_words[-1]["word"].endswith("."):
        v02_words[-1]["word"] = v02_words[-1]["word"] + "."
    (HERE / f"{SRC_STEM}_words.json").write_text(json.dumps(v01_words, indent=2) + "\n")
    (HERE / f"{DST_STEM}_words.json").write_text(json.dumps(v02_words, indent=2) + "\n")

    src_take = json.loads((HERE / f"{SRC_STEM}_TAKE.json").read_text())
    src_take["sha256_wav"] = src_sha
    (HERE / f"{SRC_STEM}_TAKE.json").write_text(json.dumps(src_take, indent=2) + "\n")

    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(DST_WAV), "-af", "volumedetect,ebur128", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    lufs = float(re.findall(r"I:\s+(-?[\d.]+)\s+LUFS", err)[-1])
    mean_db = float(re.findall(r"mean_volume: (-?[\d.]+)", err)[-1])
    max_db = float(re.findall(r"max_volume: (-?[\d.]+)", err)[-1])

    dst_take = dict(src_take)
    dst_take.update({
        "stem": DST_STEM,
        "splice_of": SRC_STEM,
        "splice_source_sha256_wav": src_sha,
        "splice_spans_s": SPANS_S,
        "duration_s": 18.480,
        "loudness": {
            "lufs_integrated": lufs,
            "mean_volume_db": mean_db,
            "max_volume_db": max_db,
        },
        "sha256_wav": sha256(DST_WAV),
        "sha256_mp3": sha256(DST_MP3),
    })
    (HERE / f"{DST_STEM}_TAKE.json").write_text(json.dumps(dst_take, indent=2) + "\n")
    print(f"Wrote {DST_WAV.name}: 18.480 s, LUFS {lufs}, words={len(v02_words)}")
    for w in v02_words:
        print(f"  {w['start']:6.3f} - {w['end']:6.3f}: {w['word']}")


if __name__ == "__main__":
    main()
