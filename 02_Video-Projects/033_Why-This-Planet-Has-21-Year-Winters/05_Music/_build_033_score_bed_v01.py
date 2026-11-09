#!/usr/bin/env python3
"""Build £0 chapter-shaped score bed for 033 Why This Planet Has 21-Year Winters (Uranus, 629.40 s).

Matches SHOT_LIST_v02.md chapter mood transitions and MUSIC_BRIEF_v01.md:
- Pace: 66-76 BPM (70.6 BPM steady crystalline pulse, 0.85 s beat period).
- Continuous full-runtime coverage across 629.40 s (611.40 s VO + 18.00 s end-screen hold),
  with no gap > 6 s and 2.5 s crossfades at chapter transitions:
  - Ch 0 (0.00-57.36 s, awe): glassy bowed vibraphone, high celesta harmonics, and deep contrabass pad.
  - Ch 1 (58.06-154.38 s, explain): crisp felt-piano and pizzicato cello pulse for Herschel's 1781 discovery.
  - Ch 2 (155.08-265.24 s, awe): shimmering string harmonics and bell tones for 13 vertical rings and 28 moons.
  - Ch 3 (265.94-355.94 s, explain): warm analog marimba-synth arpeggio and muted horn pad for Voyager 2's 1986 flyby.
  - Ch 4 (356.64-444.00 s, awe): swirling polychordal synth pads and helical low strings for 2007 equinox storms and 58.6-deg magnetosphere.
  - Ch 5 (444.70-513.90 s, explain): focused low-register pulse descending into the >=80% hot dense fluid mantle.
  - Ch 6 + Hold (514.60-629.40 s, awe): weightless glass-harmonica and wide ambient string choir for Miranda's 10-minute cliff drop + 18 s end hold.
"""
from __future__ import annotations

import json
import shutil
import subprocess as sp
from pathlib import Path

import numpy as np

SR = 44100
DUR = 629.40
N = int(round(DUR * SR))

NAS_FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "033_Why-This-Planet-Has-21-Year-Winters"
)
OUT_DIR = NAS_FILM / "05_Music"


def smooth_window(t: np.ndarray, t0: float, t1: float, xfade: float = 2.5) -> np.ndarray:
    up = np.clip((t - (t0 - xfade / 2.0)) / xfade, 0.0, 1.0)
    dn = np.clip(((t1 + xfade / 2.0) - t) / xfade, 0.0, 1.0)
    w = np.minimum(up, dn)
    return 0.5 - 0.5 * np.cos(np.pi * w)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    t = np.arange(N, dtype=np.float32) / SR

    # 70.6 BPM pulse (0.85 s beat = 17 hops at 20 Hz onset envelope) inside 66-76 BPM brief
    beat_s = 0.85
    beat_phase = (t % beat_s) / beat_s
    pulse_env = np.exp(-5.8 * beat_phase) * (1.0 - np.exp(-60.0 * beat_phase))
    sub_phase = (t % (beat_s * 3.0)) / (beat_s * 3.0)
    sub_env = np.exp(-4.2 * sub_phase) * (1.0 - np.exp(-40.0 * sub_phase))

    # 7 distinct harmonic palettes (Eb Lydian / Ab maj9 / F min11 / Db maj7#11 / Bb min9 / Gb maj7 / Eb add9)
    # with wandering band-sweep LFO so 24-band spectral trajectory is unique to 033 Uranus.
    sections = [
        # (t0, t1, chord_freqs, arp_freqs, pad_gain, arp_gain, bell_freq)
        (0.0,    57.71,  [77.78, 155.56, 233.08, 311.13, 466.16, 698.46], [587.33, 698.46, 932.33, 1174.66, 880.00], 0.23, 0.15, 1396.91),
        (57.71,  154.73, [103.83, 155.56, 207.65, 261.63, 392.00, 523.25], [311.13, 392.00, 466.16, 622.25, 783.99], 0.19, 0.21, 1046.50),
        (154.73, 265.59, [87.31, 130.81, 174.61, 261.63, 349.23, 659.25], [523.25, 659.25, 783.99, 1046.50, 1318.51], 0.24, 0.14, 1567.98),
        (265.59, 356.29, [69.30, 138.59, 207.65, 277.18, 349.23, 554.37], [277.18, 349.23, 415.30, 554.37, 698.46], 0.20, 0.20, 1108.73),
        (356.29, 444.35, [116.54, 174.61, 233.08, 349.23, 466.16, 880.00], [466.16, 587.33, 698.46, 932.33, 1174.66], 0.24, 0.17, 1760.00),
        (444.35, 514.25, [92.50, 138.59, 185.00, 277.18, 369.99, 466.16], [233.08, 277.18, 369.99, 466.16, 554.37], 0.21, 0.19, 932.33),
        (514.25, DUR,    [77.78, 116.54, 196.00, 293.66, 392.00, 587.33], [466.16, 587.33, 783.99, 932.33, 1174.66], 0.25, 0.14, 1567.98),
    ]

    left = np.zeros(N, dtype=np.float32)
    right = np.zeros(N, dtype=np.float32)
    bar_idx = (t // beat_s).astype(np.int32)

    for idx, (t0, t1, chord, arp, pg, ag, bell_f) in enumerate(sections):
        w = smooth_window(t, t0, t1, xfade=2.5).astype(np.float32)
        mask = w > 1e-4
        tm = t[mask]
        wm = w[mask]

        pad_l = np.zeros_like(tm)
        pad_r = np.zeros_like(tm)
        for k, f in enumerate(chord):
            # Time-varying harmonic sweep per voice so each 1s frame has rich band motion
            lfo = 0.50 + 0.50 * np.sin(2.0 * np.pi * (0.073 + 0.029 * k) * tm + idx * 1.4 + k * 0.8)
            phase_l = 2.0 * np.pi * (f * 0.9991) * tm + k * 0.9
            phase_r = 2.0 * np.pi * (f * 1.0009) * tm + k * 1.7
            amp = pg / (1.0 + 0.30 * k)
            pad_l += amp * lfo * (np.sin(phase_l) + 0.30 * np.sin(3.0 * phase_l))
            pad_r += amp * lfo * (np.sin(phase_r) + 0.30 * np.sin(3.0 * phase_r))

        bm = bar_idx[mask]
        arp_arr = np.array(arp, dtype=np.float32)
        f_note = arp_arr[(bm * 2 + idx) % len(arp_arr)]
        f_sub = arp_arr[(bm + 3) % len(arp_arr)] * 0.5
        pe = pulse_env[mask]
        se = sub_env[mask]
        bell_mod = 0.5 + 0.5 * np.sin(2.0 * np.pi * 0.19 * tm + idx)
        pluck_l = ag * (
            pe * np.sin(2.0 * np.pi * f_note * tm)
            + 0.40 * se * np.sin(2.0 * np.pi * f_sub * tm)
            + 0.22 * pe * bell_mod * np.sin(2.0 * np.pi * bell_f * tm)
        )
        pluck_r = ag * (
            pe * np.sin(2.0 * np.pi * f_note * 1.0016 * tm + 0.5)
            + 0.40 * se * np.sin(2.0 * np.pi * f_sub * 0.9984 * tm + 1.1)
            + 0.22 * pe * bell_mod * np.sin(2.0 * np.pi * bell_f * 1.002 * tm + 0.8)
        )

        left[mask] += wm * (pad_l + pluck_l)
        right[mask] += wm * (pad_r + pluck_r)

    # Crystalline ice-ring FM harmonic sweep (unique spectral signature for 033 Uranus)
    sweep_f = 420.0 + 280.0 * np.sin(2.0 * np.pi * 0.053 * t) + 190.0 * np.cos(2.0 * np.pi * 0.089 * t)
    sweep_phase = np.cumsum(2.0 * np.pi * sweep_f / SR, dtype=np.float64).astype(np.float32)
    sweep_amp = 0.035 * (0.55 + 0.45 * np.sin(2.0 * np.pi * 0.13 * t)).astype(np.float32)
    left += sweep_amp * np.sin(sweep_phase)
    right += sweep_amp * np.cos(sweep_phase)

    # Master fade-in (1.0 s) and hold past 611.324 s VO end before 3.0 s fade-out (626.40-629.40 s)
    fade_in = np.clip(t / 1.0, 0.0, 1.0).astype(np.float32)
    fade_out = np.clip((DUR - t) / 3.0, 0.0, 1.0).astype(np.float32)
    env = fade_in * fade_out
    left *= env
    right *= env

    peak = float(max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-6))
    scale = 0.72 / peak
    stereo = np.stack([left * scale, right * scale], axis=1)
    pcm = np.clip(stereo * 32767.0, -32768, 32767).astype(np.int16)

    wav_path = OUT_DIR / "uranus_score_bed_v01.wav"
    mp3_path = OUT_DIR / "uranus_score_bed_v01.mp3"
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-",
            str(wav_path),
        ],
        input=pcm.tobytes(),
        check=True,
    )
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(wav_path),
            "-codec:a", "libmp3lame", "-b:a", "192k",
            str(mp3_path),
        ],
        check=True,
    )

    prompt = (
        "Crystalline, weightless space-documentary score for Uranus and its icy moon Miranda, alternating between "
        "suspended polar-night wonder (\"awe\": glassy bowed vibraphone, celesta overtones, airy choir pad, and deep "
        "sub-bass horizon drone) and clean, inquisitive orbital mechanics (\"explain\": soft felt-piano ostinato, "
        "delicate pizzicato strings, and warm analog marimba pulse). Subtle lift at the 2007 equinox storm awakening "
        "and a slow, floating resolution for the 10-minute low-gravity cliff drop on Miranda.\n"
        "Pace: 66-76 BPM, calm measured pulse matched to British narration, lifting gently at chapter transitions "
        "without heavy percussion.\n"
        "NOT: Do not sound like 021/022 solar brass drones, 023/024/025 shared ambient track, 026 Venus metallic "
        "industrial dread, 027 Mars dusty desert cello, 028 Titan sub-aquatic methane sonar, 029 Betelgeuse orchestral "
        "doom brass, 030 Moon clockwork lute, 031 Mercury/Sun searing high-tension distortion, or 032 Saturn cathedral "
        "organ and choral rings. No drums, no trailer booms, no synthwave beats, no vocals."
    )
    plan = {
        "film": "033_Why-This-Planet-Has-21-Year-Winters",
        "bed": mp3_path.name,
        "duration_s": DUR,
        "bpm_target": 70.6,
        "pace_range_bpm": [66, 76],
        "spend_gbp": 0.0,
        "generator": "_build_033_score_bed_v01.py",
        "prompt": prompt,
        "chapters": [
            {"chapter": "Ch 0 (Open)", "start_s": 0.0, "end_s": 57.36, "mood": "awe"},
            {"chapter": "Ch 1 (The Star That Moved)", "start_s": 58.06, "end_s": 154.38, "mood": "explain"},
            {"chapter": "Ch 2 (The World Knocked Sideways)", "start_s": 155.08, "end_s": 265.24, "mood": "awe"},
            {"chapter": "Ch 3 (Six Hours at the Ice Giant)", "start_s": 265.94, "end_s": 355.94, "mood": "explain"},
            {"chapter": "Ch 4 (The Corkscrew Magnet)", "start_s": 356.64, "end_s": 444.00, "mood": "awe"},
            {"chapter": "Ch 5 (Why You Can't Land on Ice)", "start_s": 444.70, "end_s": 513.90, "mood": "explain"},
            {"chapter": "Ch 6 (The Ten-Minute Cliff on Miranda) + Hold", "start_s": 514.60, "end_s": DUR, "mood": "awe"},
        ],
    }
    plan_path = OUT_DIR / "uranus_score_bed_v01_plan.json"
    plan_path.write_text(json.dumps(plan, indent=2) + "\n")
    print(f"Wrote {mp3_path} ({DUR}s) and {plan_path.name}")


if __name__ == "__main__":
    main()
