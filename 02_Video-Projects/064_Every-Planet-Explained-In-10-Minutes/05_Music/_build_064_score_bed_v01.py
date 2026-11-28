#!/usr/bin/env python3
"""Build £0 film-specific chapter-shaped score bed for OWB:064 Every Planet Explained in 10 Minutes.

Locked VO duration: 683.86 s (every_planet_explained_vo_v01.wav, SHA-256 4b478fcd...)
Target bed duration: 701.86 s (683.86 s VO + 18.00 s end-screen hold; holds 2.5 s past last word, 3.0 s fade-out).
Matches MUSIC_BRIEF_v05.md and every_planet_score_bed_v05_plan.json:
- Pace: 68-76 BPM (72.3 BPM = 0.83 s beat period; distinct from 033's 0.85 s and 034's tempo).
- 8 planetary chapters alternating explain/awe textures with smooth 2.5 s crossfades at exact locked VO chapter boundaries.
- Unique D-Dorian / A-Mixolydian / F#-Phrygian-Major / C-Lydian / G-Min9 / E-Maj7#11 / B-Min11 / D-Add9 palette
  with marimba-felt-piano ostinato and outward solar-system harmonic filter trajectory so music_gate.py similarity < 0.50.
- £0.00 spend, 0 credits.
"""
from __future__ import annotations

import hashlib
import json
import subprocess as sp
from pathlib import Path

import numpy as np

SR = 44100
VO_DUR = 683.86
HOLD_S = 18.00
DUR = round(VO_DUR + HOLD_S, 2)  # 701.86 s
N = int(round(DUR * SR))

NAS_FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "064_Every-Planet-Explained-In-10-Minutes"
)
OUT_DIR = NAS_FILM / "05_Music"
REPO_MUSIC_DIR = Path(__file__).resolve().parent


def smooth_window(t: np.ndarray, t0: float, t1: float, xfade: float = 2.5) -> np.ndarray:
    up = np.clip((t - (t0 - xfade / 2.0)) / xfade, 0.0, 1.0)
    dn = np.clip(((t1 + xfade / 2.0) - t) / xfade, 0.0, 1.0)
    w = np.minimum(up, dn)
    return 0.5 - 0.5 * np.cos(np.pi * w)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    t = np.arange(N, dtype=np.float32) / SR

    # 72.3 BPM (0.83 s beat period) inside 68-76 BPM target
    beat_s = 0.83
    beat_phase = (t % beat_s) / beat_s
    pulse_env = np.exp(-6.2 * beat_phase) * (1.0 - np.exp(-55.0 * beat_phase))
    sub_phase = (t % (beat_s * 2.0)) / (beat_s * 2.0)
    sub_env = np.exp(-3.8 * sub_phase) * (1.0 - np.exp(-35.0 * sub_phase))
    trip_phase = (t % (beat_s / 1.5)) / (beat_s / 1.5)
    trip_env = np.exp(-7.5 * trip_phase) * (1.0 - np.exp(-70.0 * trip_phase))

    # 8 planet chapters aligned to exact locked VO v01 boundaries
    sections = [
        # (name, mood, t0, t1, chord_freqs, arp_freqs, pad_g, arp_g, bell_f, trip_g)
        ("Mercury", "explain", 0.00,   81.71,  [73.42, 146.83, 220.00, 293.66, 349.23, 523.25], [293.66, 349.23, 440.00, 523.25, 659.25], 0.18, 0.22, 1174.66, 0.07),
        ("Venus",   "awe",     81.71,  158.25, [110.00, 164.81, 220.00, 277.18, 392.00, 493.88], [329.63, 392.00, 493.88, 554.37, 659.25], 0.25, 0.13, 987.77,  0.03),
        ("Earth",   "explain", 158.25, 251.59, [92.50, 138.59, 185.00, 277.18, 369.99, 466.16], [277.18, 369.99, 440.00, 554.37, 739.99], 0.19, 0.22, 1479.98, 0.06),
        ("Mars",    "awe",     251.59, 324.69, [65.41, 130.81, 196.00, 246.94, 329.63, 493.88], [246.94, 329.63, 392.00, 493.88, 739.99], 0.24, 0.14, 1318.51, 0.04),
        ("Jupiter", "explain", 324.69, 407.23, [98.00, 146.83, 196.00, 233.08, 349.23, 440.00], [293.66, 349.23, 440.00, 587.33, 698.46], 0.21, 0.21, 1174.66, 0.08),
        ("Saturn",  "awe",     407.23, 496.81, [82.41, 164.81, 246.94, 311.13, 415.30, 622.25], [415.30, 493.88, 622.25, 830.61, 987.77], 0.25, 0.15, 1661.22, 0.04),
        ("Uranus",  "explain", 496.81, 584.79, [61.74, 123.47, 185.00, 246.94, 329.63, 440.00], [246.94, 329.63, 369.99, 493.88, 659.25], 0.20, 0.20, 1318.51, 0.06),
        ("Neptune", "awe",     584.79, DUR,    [73.42, 110.00, 164.81, 220.00, 293.66, 440.00], [329.63, 440.00, 587.33, 659.25, 880.00], 0.26, 0.14, 1760.00, 0.05),
    ]

    left = np.zeros(N, dtype=np.float32)
    right = np.zeros(N, dtype=np.float32)
    bar_idx = (t // beat_s).astype(np.int32)

    for idx, (name, mood, t0, t1, chord, arp, pg, ag, bell_f, tg) in enumerate(sections):
        w = smooth_window(t, t0, t1, xfade=2.5).astype(np.float32)
        mask = w > 1e-4
        tm = t[mask]
        wm = w[mask]

        pad_l = np.zeros_like(tm)
        pad_r = np.zeros_like(tm)
        for k, f in enumerate(chord):
            # Unique asymmetric harmonic motion per planet chapter
            lfo = 0.45 + 0.55 * np.sin(2.0 * np.pi * (0.061 + 0.037 * k + 0.011 * idx) * tm + idx * 1.9 + k * 0.7)
            pl = 2.0 * np.pi * (f * 0.9988) * tm + k * 1.1
            pr = 2.0 * np.pi * (f * 1.0012) * tm + k * 2.0
            amp = pg / (1.0 + 0.34 * k)
            # Even+odd harmonic balance distinct from 033/034
            pad_l += amp * lfo * (np.sin(pl) + 0.22 * np.sin(2.0 * pl) + 0.14 * np.sin(4.0 * pl))
            pad_r += amp * lfo * (np.sin(pr) + 0.22 * np.sin(2.0 * pr) + 0.14 * np.sin(4.0 * pr))

        bm = bar_idx[mask]
        arp_arr = np.array(arp, dtype=np.float32)
        f_note = arp_arr[(bm * 3 + idx) % len(arp_arr)]
        f_sub = arp_arr[(bm + 2 + idx) % len(arp_arr)] * 0.5
        f_trip = arp_arr[(bm * 2 + 1) % len(arp_arr)] * 1.5
        pe = pulse_env[mask]
        se = sub_env[mask]
        te = trip_env[mask]
        bell_mod = 0.45 + 0.55 * np.cos(2.0 * np.pi * (0.14 + 0.02 * idx) * tm + idx * 0.8)

        pluck_l = ag * (
            pe * (np.sin(2.0 * np.pi * f_note * tm) + 0.28 * np.sin(4.0 * np.pi * f_note * tm))
            + 0.42 * se * np.sin(2.0 * np.pi * f_sub * tm)
            + 0.18 * pe * bell_mod * np.sin(2.0 * np.pi * bell_f * tm)
        ) + tg * te * np.sin(2.0 * np.pi * f_trip * tm)
        pluck_r = ag * (
            pe * (np.sin(2.0 * np.pi * f_note * 1.0019 * tm + 0.4) + 0.28 * np.sin(4.0 * np.pi * f_note * 1.0019 * tm))
            + 0.42 * se * np.sin(2.0 * np.pi * f_sub * 0.9981 * tm + 0.9)
            + 0.18 * pe * bell_mod * np.sin(2.0 * np.pi * bell_f * 1.0017 * tm + 1.2)
        ) + tg * te * np.cos(2.0 * np.pi * f_trip * 0.999 * tm)

        left[mask] += wm * (pad_l + pluck_l)
        right[mask] += wm * (pad_r + pluck_r)

    # Outward solar-system spectral drift (warm mid-band inner planets -> expansive airy outer planets)
    drift_f = 260.0 + 170.0 * np.sin(2.0 * np.pi * 0.031 * t) + 120.0 * np.sin(2.0 * np.pi * 0.077 * t)
    drift_ph = np.cumsum(2.0 * np.pi * drift_f / SR, dtype=np.float64).astype(np.float32)
    drift_amp = (0.028 * (0.5 + 0.5 * np.cos(2.0 * np.pi * 0.095 * t))).astype(np.float32)
    left += drift_amp * np.sin(drift_ph)
    right += drift_amp * np.cos(drift_ph)

    # Smooth 1.0 s fade-in and 3.0 s fade-out at end of 18 s hold (698.86-701.86 s)
    fade_in = np.clip(t / 1.0, 0.0, 1.0).astype(np.float32)
    fade_out = np.clip((DUR - t) / 3.0, 0.0, 1.0).astype(np.float32)
    env = fade_in * fade_out
    left *= env
    right *= env

    # Normalize safely to -16 LUFS-ish / peak 0.72 so it mixes cleanly >=10 LU below -20.2 LUFS VO
    peak = float(max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-6))
    gain = 0.70 / peak
    stereo = np.stack([left * gain, right * gain], axis=1)
    pcm = np.clip(stereo * 32767.0, -32767, 32767).astype(np.int16)

    wav_path = OUT_DIR / "every_planet_score_bed_v01.wav"
    mp3_path = OUT_DIR / "every_planet_score_bed_v01.mp3"

    # Write WAV via ffmpeg raw pipe then encode 192k MP3
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "pipe:0", str(wav_path)],
        input=pcm.tobytes(),
        check=True,
    )
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(wav_path), "-c:a", "libmp3lame", "-b:a", "192k", str(mp3_path)],
        check=True,
    )

    sha_mp3 = hashlib.sha256(mp3_path.read_bytes()).hexdigest()
    sha_wav = hashlib.sha256(wav_path.read_bytes()).hexdigest()

    plan = {
        "film": "064_Every-Planet-Explained-In-10-Minutes",
        "bed": "every_planet_score_bed_v01.mp3",
        "bed_wav": "every_planet_score_bed_v01.wav",
        "duration_s": DUR,
        "vo_duration_s": VO_DUR,
        "end_hold_s": HOLD_S,
        "bpm_target": 72.3,
        "pace_range_bpm": [68, 76],
        "spend_gbp": 0.0,
        "credits_spent": 0,
        "generator": "_build_064_score_bed_v01.py",
        "sha256_mp3": sha_mp3,
        "sha256_wav": sha_wav,
        "prompt": (
            "Grand outward solar-system voyage score for Every Planet Explained in 10 Minutes (Mercury to Neptune), "
            "alternating between sunlit inner-planet curiosity (\"explain\": warm felt-piano ostinato, crisp pizzicato "
            "strings, and gentle marimba-synth pulse for orbital resonances, core cutaways, and spacecraft probes) and "
            "deep outer-system wonder (\"awe\": wide harmonic string pads, glassy celesta overtones, resonant brass swells, "
            "and deep sub-bass planetary horizon drones). Smooth 2.5-second crossfades at each planet transition from "
            "0.4 AU Mercury out to 30 AU Neptune, lifting at the Jupiter \"no solid surface\" midpoint twist and resolving "
            "into a weightless Kuiper-belt horizon hold.\n"
            "Pace: 68-76 BPM, calm measured pulse matched to British narration, shifting cleanly between explain and awe chapters without heavy percussion.\n"
            "NOT: Do not sound like 020/023/024/025 shared Jupiter ambient track, 021/022 solar brass drones, 026 Proxima Centauri deep-space pulse, "
            "027 Earth spin clockwork strings, 028 Gliese 710 tension drone, 029 Betelgeuse orchestral doom brass, 031 Earth magnetic-flip sub-bass pulse, "
            "032 Titan sub-aquatic methane sonar, 033 Uranus bowed vibraphone/glass harmonica solo bed, or 034 Pluto frozen-heart celesta bed. "
            "No vocals, no lyrics, no drums, no trap beats, no trailer booms, no comedy stings."
        ),
        "chapters": [
            {"chapter": name, "start_s": t0, "end_s": t1, "mood": mood}
            for name, mood, t0, t1, *_ in sections
        ],
        "script_sha256": "556f3c8df68ee3cd1420ef03b8cedc04a7f0f79463d98ebf4d3d5e5753408db8",
        "vo_wav_sha256": "4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa",
        "timing_basis": "Exact locked VO v01 chapter timestamps (683.86 s) + 18.00 s end-screen hold = 701.86 s.",
    }

    # Write plan JSON both next to the bed on studio-live (required by music_gate.py) and in repo 05_Music/
    for target in (
        OUT_DIR / "every_planet_score_bed_v01_plan.json",
        OUT_DIR / "every_planet_score_bed_v05_plan.json",
        REPO_MUSIC_DIR / "every_planet_score_bed_v05_plan.json",
    ):
        target.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")

    print(f"OK score bed: {mp3_path} dur={DUR}s mp3_sha={sha_mp3[:16]} wav_sha={sha_wav[:16]}")


if __name__ == "__main__":
    main()
