#!/usr/bin/env python3
"""J3331: deterministic C7 Trim 2 room-tone splice from roman_2026_12_07_vo_v01.wav.

- Primary 48w Take 1 ran 21.840 s (natural 1.00x speed; even after room-tone tightening, 48w VO + 1.0 s loop > 20.0 s
  and 45w Trim 1 would still exceed Ben's 19.0 s target). Applies the pre-approved C7 Trim 2 from §4 of
  02_Video-Projects/_dated_shorts/2026-12-07_roman-telescope-first-images.md: drop spoken Line 2 (keeping
  'SCALE: Bigger than full Moon' on the animated DATA overlay) leaving Lines 1, 3, 4, and 5 (39 words, 4 sentences).
- 100% natural recorded speed (1.00x, zero atempo); every splice sits inside verified <-75 dBFS room-tone silence
  with 10 ms (480-sample) qsin joins and natural ~0.28-0.31 s breaths (<0.4 s per Rule 39).
- Output: 17.200 s VO (825,600 samples at 48 kHz) + 1.000 s forward-loop tail = 18.200 s total (546 frames at 30 fps),
  squarely inside Ben's 16.0-19.0 s Shorts gate band and Rule 16's 17.0-20.0 s band; Line 4 starts at 9.430 s (<= 13.5 s).
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
SRC_STEM = "roman_2026_12_07_vo_v01"
SRC_WAV = HERE / f"{SRC_STEM}.wav"
DST_STEM = "roman_2026_12_07_vo_v02"
DST_WAV = HERE / f"{DST_STEM}.wav"
DST_MP3 = HERE / f"{DST_STEM}.mp3"

SR = 48000
FADE = 480        # 10 ms internal room-tone join fade
END_FADE = 720    # 15 ms anti-click end fade after 'pixel'

# Spans in seconds -> exact samples at 48 kHz (sum = 17.200 s = 825,600 frames)
SPANS_S = [
    (0.000, 4.580),    # 4.580 s: "NASA's Roman telescope unveils its first images on December seventh."
    (8.580, 13.280),   # 4.700 s: "Its mirror matches Hubble's, yet captures a hundred Hubble views."
    (13.600, 18.280),  # 4.680 s: "A million miles out, it hunts dark energy and alien worlds."
    (18.600, 21.840),  # 3.240 s: "Watch NASA live, and claim your own pixel."
]
SPANS = [(int(round(s * SR)), int(round(e * SR))) for s, e in SPANS_S]

TRIM2_TEXT = (
    "NASA's Roman telescope unveils its first images on December seventh.\n"
    "Its mirror matches Hubble's, yet captures a hundred Hubble views.\n"
    "A million miles out, it hunts dark energy and alien worlds.\n"
    "Watch NASA live, and claim your own pixel.\n"
)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def map_time(t: float) -> float | None:
    acc = 0.0
    for s, e in SPANS_S:
        if s <= t <= e:
            return round(acc + (t - s), 3)
        acc += (e - s)
    return None


def main() -> None:
    (HERE / "roman_2026_12_07_spoken_v02_trim2.txt").write_text(TRIM2_TEXT)
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
    assert len(out) == int(round(17.200 * SR)), f"unexpected frame count {len(out)}"

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
    v02_words = []
    for w in stt_raw.get("words", []):
        if w.get("type") != "word":
            continue
        ms = map_time(float(w["start"]))
        me = map_time(float(w["end"]))
        if ms is not None and me is not None:
            v02_words.append({"word": w["text"], "start": ms, "end": me})
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
        "splice_rule": "C7 Trim 2 (39w, 4 sentences: Lines 1, 3, 4, 5; Line 2 Moon scale kept on DATA overlay)",
        "splice_source_sha256_wav": src_sha,
        "splice_spans_s": SPANS_S,
        "words": len(TRIM2_TEXT.split()),
        "text": TRIM2_TEXT.strip(),
        "duration_s": 17.200,
        "loudness": {
            "lufs_integrated": lufs,
            "mean_volume_db": mean_db,
            "max_volume_db": max_db,
        },
        "sha256_wav": sha256(DST_WAV),
        "sha256_mp3": sha256(DST_MP3),
    })
    (HERE / f"{DST_STEM}_TAKE.json").write_text(json.dumps(dst_take, indent=2) + "\n")
    print(f"Wrote {DST_WAV.name}: 17.200 s, LUFS {lufs}, words={len(v02_words)}")
    for w in v02_words:
        print(f"  {w['start']:6.3f} - {w['end']:6.3f}: {w['word']}")


if __name__ == "__main__":
    main()
