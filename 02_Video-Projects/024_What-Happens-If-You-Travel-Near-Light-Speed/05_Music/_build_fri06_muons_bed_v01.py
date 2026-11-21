#!/usr/bin/env python3
"""£0 own-synthesis Short bed for OWB 024 fri06_muons_ground (J3136).

The locked long bed light-speed_score_bed_v01_full.mp3 scores 0.83 against the
archived OWB 013 moon-leaving part 2 bed. This writes a new Short bed that is
not that recording: a clock pulse and a bright inharmonic pluck, no piano and
no pad. Nothing is downloaded or sent to a paid generator.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import music_gate as mg  # noqa: E402

MUSIC = Path(__file__).resolve().parent
BED_MP3 = MUSIC / "fri06_muons_ground_score_bed_v01.mp3"
BED_WAV = MUSIC / "fri06_muons_ground_score_bed_v01.wav"
PLAN = MUSIC / "fri06_muons_ground_score_bed_v01_plan.json"
OTHERS = REPO / "jobs/reviews/J3136/owb_comparison_beds.txt"
SR = 48000
SECONDS = 36.0
BPM = 80

PROMPT = (
    "Instrumental Short underscore for Orbit with Ben, the muon Short from the Light Speed film. "
    "A dry clock pulse and a bright inharmonic pluck, one note per beat, narrow and ticking, "
    "with a quiet low fifth that never drops out. It sits under British narration about particles "
    "that reach the ground. Pace: 72-88 BPM, steady. "
    "NOT the Light Speed long bed, NOT Moon Leaving lunar piano, NOT Jupiter music, NOT Saturn ring chimes, "
    "NOT Sun golden strings, NOT the Mars robot's lonely felt piano, NOT the Nearest Star's glassy celesta, "
    "NOT Venus heat drones. No vocals, no choir, no drums, no EDM, no trailer hit, no pad wash."
)


def synth(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = int(SECONDS * SR)
    t = np.arange(n) / SR
    y = np.zeros(n, np.float64)
    # Floor that never opens a 6 s hole: two close low tones, always on.
    y += 0.16 * np.sin(2 * np.pi * 98.0 * t)
    y += 0.07 * np.sin(2 * np.pi * 98.0 * 1.498 * t)
    beat = 60.0 / BPM
    partials = (1.0, 2.71, 4.37, 6.09, 8.83)
    for i, t0 in enumerate(np.arange(0.0, SECONDS - 0.2, beat)):
        s0 = int(t0 * SR)
        length = int(0.42 * SR)
        if s0 + length > n:
            length = n - s0
        tt = np.arange(length) / SR
        env = np.minimum(tt / 0.008, 1.0) * np.exp(-tt / (0.09 + (i % 3) * 0.02))
        f0 = 520.0 + (i % 6) * 70.0 + (40.0 if i % 2 else 0.0)
        tone = np.zeros(length)
        for k, ratio in enumerate(partials):
            amp = 0.55 / (k + 1) ** 1.15
            # Odd beats push the energy up; even beats keep it in the mid bands.
            if i % 2:
                amp *= 1.8 if k >= 3 else 0.35
            else:
                amp *= 1.6 if k <= 1 else 0.25
            tone += amp * np.sin(2 * np.pi * f0 * ratio * tt + rng.random() * 0.2)
        # A short high tick on every other beat so the 1 s spectrum keeps moving.
        if i % 2 == 0:
            tick_n = min(int(0.03 * SR), length)
            tick_t = np.arange(tick_n) / SR
            tick = np.sin(2 * np.pi * (2400 + (i % 5) * 180) * tick_t) * np.exp(-tick_t / 0.012)
            tone[:tick_n] += 0.9 * tick
        y[s0:s0 + length] += 0.28 * env * tone
    # Gentle fade only in the last 8 s, past the 22.2 s Short.
    fade_from = int(28.0 * SR)
    ramp = np.ones(n)
    ramp[fade_from:] = np.linspace(1.0, 0.2, n - fade_from)
    y *= ramp
    peak = np.max(np.abs(y)) + 1e-9
    y = (y / peak * 0.45).astype(np.float32)
    return np.column_stack([y, y * 0.97])


def write_wav(path: Path, stereo: np.ndarray) -> None:
    import wave
    pcm = np.clip(stereo, -1, 1)
    pcm = (pcm * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def load_others() -> list[np.ndarray]:
    frames = []
    for line in OTHERS.read_text().splitlines():
        p = Path(line.strip())
        if not p.is_file():
            raise SystemExit(f"missing comparison bed {p}")
        frames.append(mg.frames(mg.decode(p)))
    return frames


def max_sim(bed_frames: np.ndarray, others: list[np.ndarray]) -> float:
    return max(mg.similarity(bed_frames, o) for o in others)


def main() -> None:
    if not OTHERS.is_file():
        raise SystemExit(f"missing {OTHERS}")
    print("decoding 31 comparison beds", flush=True)
    others = load_others()
    best = None
    for seed in range(7):
        stereo = synth(seed)
        mono8 = stereo[:: SR // mg.SR, 0]
        fa = mg.frames(mono8.astype(np.float32))
        score = max_sim(fa, others)
        print(f"seed {seed} rough max similarity {score:.4f}", flush=True)
        if best is None or score < best[0]:
            best = (score, seed, stereo)
        if score < 0.55:
            break
    score, seed, stereo = best
    if score >= 0.75:
        raise SystemExit(f"no seed under 0.75 (best {score:.3f})")
    write_wav(BED_WAV, stereo)
    import subprocess
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(BED_WAV), "-codec:a", "libmp3lame", "-q:a", "2", str(BED_MP3)],
        check=True,
    )
    plan = {
        "created_at": "2026-11-19T23:20:00+00:00",
        "project": "light-speed",
        "audio_file": BED_MP3.name,
        "status": "own-synthesis",
        "model_id": None,
        "credits": 0,
        "spend": "£0",
        "source": "own synthesis (02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/05_Music/_build_fri06_muons_bed_v01.py), no third-party samples",
        "job": "J3136",
        "seed": seed,
        "seconds": SECONDS,
        "bpm": BPM,
        "replaces_for_short": "light-speed_score_bed_v01_full.mp3",
        "reason": "v05 Short bed scored 0.830 against archived moon-leaving-part02_score_bed_v01.mp3",
        "prompt": PROMPT,
        "by": "macbook",
    }
    PLAN.write_text(json.dumps(plan, indent=2) + "\n")
    # Confirm with the gate's own decoder, not the rough resample.
    fa = mg.frames(mg.decode(BED_MP3))
    confirmed = max_sim(fa, others)
    print(json.dumps({"seed": seed, "rough": round(score, 4), "confirmed_mp3": round(confirmed, 4), "wav": str(BED_WAV)}))
    if confirmed >= 0.80:
        raise SystemExit(f"confirmed similarity {confirmed:.3f} is not under 0.80")


if __name__ == "__main__":
    main()
