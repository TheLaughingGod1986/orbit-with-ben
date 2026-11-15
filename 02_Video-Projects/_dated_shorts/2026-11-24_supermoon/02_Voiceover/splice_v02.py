#!/usr/bin/env python3
"""J2478: deterministic C7 Trim 1 + room-tone gap tightening from supermoon_2026_11_24_c7_trim1_vo_v01.wav.

- Input: supermoon_2026_11_24_c7_trim1_vo_v01.wav (sha256 95a24bc9c4b1352f333c121e96d88483afd7688229e037ba9a51958feeb9f385, 20.000 s, 960,000 frames at 48 kHz s16 stereo).
- Output: supermoon_2026_11_24_vo_v02.wav (18.600 s, 892,800 frames at 48 kHz s16 stereo; planned cut = 19.600 s with 1.000 s loop tail).
- All cuts are inside verified room-tone silence (< -67 dB RMS, < -50 dB peak).
- Every join has a 10 ms (480-sample) qsin fade-out/fade-in; the end of 'as…' has a 160 ms (7,680-sample) qsin fade-out so the last 20 ms sits well below -45 dBFS (per CHIEF_H40_VO_LOCK.md).
- Also writes shifted Scribe word timings to supermoon_2026_11_24_vo_v02_words.json and supermoon_2026_11_24_vo_v02_TAKE.json.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SRC_WAV = HERE / "supermoon_2026_11_24_c7_trim1_vo_v01.wav"
SRC_SHA = "95a24bc9c4b1352f333c121e96d88483afd7688229e037ba9a51958feeb9f385"
DST_STEM = "supermoon_2026_11_24_vo_v02"
DST_WAV = HERE / f"{DST_STEM}.wav"
DST_MP3 = HERE / f"{DST_STEM}.mp3"

SR = 48000
FADE = 480         # 10 ms join fade
END_FADE = 7680    # 160 ms end fade on "as…"

# Spans in seconds -> frames at 48 kHz (sum = 18.600 s = 892,800 frames)
SPANS_S = [
    (0.030, 4.450),    # 4.420 s: "The Moon swings two Earths closer on November twenty-fourth."
    (4.950, 8.650),    # 3.700 s: "If Earth were a nickel, the Moon is a coffee bean."
    (8.900, 11.700),   # 2.800 s: "Normally thirty Earths fit between us."
    (11.850, 17.300),  # 5.450 s: "This Supermoon passes three hundred and sixty thousand kilometres up."
    (17.770, 20.000),  # 2.230 s: "Look east at sunset, as…"
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
    assert sha256(SRC_WAV) == SRC_SHA, f"{SRC_WAV} sha256 mismatch"
    with wave.open(str(SRC_WAV), "rb") as w:
        params = w.getparams()
        raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2)
    assert (params.nchannels, params.sampwidth, params.framerate, params.nframes) == (2, 2, SR, 960000)

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
    assert len(out) == int(round(18.600 * SR)), f"unexpected frame count {len(out)}"

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

    # Check end fade levels
    tail20 = out[-int(0.02 * SR):].astype(np.float64) / 32768.0
    tail10 = out[-int(0.01 * SR):].astype(np.float64) / 32768.0
    db20 = 20 * np.log10(max(np.max(np.abs(tail20)), 1e-7))
    db10 = 20 * np.log10(max(np.max(np.abs(tail10)), 1e-7))

    # Map word timings from Scribe stt_raw.json
    stt_raw = json.loads((HERE / "stt/supermoon_2026_11_24_c7_trim1_vo_v01/stt_raw.json").read_text())
    words = []
    for w in stt_raw.get("words", []):
        if w.get("type") != "word":
            continue
        words.append({
            "word": w["text"],
            "start": map_time(float(w["start"])),
            "end": map_time(float(w["end"])),
        })
    (HERE / f"{DST_STEM}_words.json").write_text(json.dumps(words, indent=2) + "\n")
    (HERE / "supermoon_2026_11_24_c7_trim1_vo_v01_words.json").write_text(
        json.dumps(
            [{"word": w["text"], "start": float(w["start"]), "end": float(w["end"])}
             for w in stt_raw.get("words", []) if w.get("type") == "word"],
            indent=2,
        ) + "\n"
    )
    stt_v01 = json.loads((HERE / "stt/supermoon_2026_11_24_vo_v01/stt_raw.json").read_text())
    (HERE / "supermoon_2026_11_24_vo_v01_words.json").write_text(
        json.dumps(
            [{"word": w["text"], "start": float(w["start"]), "end": float(w["end"])}
             for w in stt_v01.get("words", []) if w.get("type") == "word"],
            indent=2,
        ) + "\n"
    )

    # Loudness & TAKE.json
    src_take = json.loads((HERE / "supermoon_2026_11_24_c7_trim1_vo_v01_TAKE.json").read_text())
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(DST_WAV), "-af", "volumedetect,ebur128", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    import re
    lufs = float(re.findall(r"I:\s+(-?[\d.]+)\s+LUFS", err)[-1])
    mean_db = float(re.findall(r"mean_volume: (-?[\d.]+)", err)[-1])
    max_db = float(re.findall(r"max_volume: (-?[\d.]+)", err)[-1])

    dst_take = dict(src_take)
    dst_take.update({
        "stem": DST_STEM,
        "splice_of": "supermoon_2026_11_24_c7_trim1_vo_v01",
        "splice_source_sha256_wav": SRC_SHA,
        "splice_spans_s": SPANS_S,
        "duration_s": 18.600,
        "loudness": {
            "lufs_integrated": lufs,
            "mean_volume_db": mean_db,
            "max_volume_db": max_db,
        },
        "sha256_wav": sha256(DST_WAV),
        "sha256_mp3": sha256(DST_MP3),
        "tail_peak_last20ms_dbfs": round(db20, 1),
        "tail_peak_last10ms_dbfs": round(db10, 1),
        "credits": {"before": src_take["credits"]["after"], "after": src_take["credits"]["after"], "counter_delta": 0},
    })
    (HERE / f"{DST_STEM}_TAKE.json").write_text(json.dumps(dst_take, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {DST_WAV.name}: 18.600 s, sha256={sha256(DST_WAV)}, LUFS={lufs}, last20ms={db20:.1f} dBFS, last10ms={db10:.1f} dBFS")
    for w in words:
        print(f"  {w['start']:6.3f} - {w['end']:6.3f}  {w['word']}")


if __name__ == "__main__":
    main()
