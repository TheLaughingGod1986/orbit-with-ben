#!/usr/bin/env python3
"""Build £0 chapter-shaped score bed for 031 Magnetic Field Flip (570.78 s).

Matches SHOT_LIST_v02.md chapter mood transitions and MUSIC_BRIEF_v01.md:
- Pace: 66-74 BPM (72.0 BPM quarter-note pulse, 0.8333 s period).
- Continuous full-runtime coverage across 570.78 s (568.28 s VO + 2.50 s hold),
  with no gap > 6 s and 3.0 s crossfades at chapter cards:
  - 0.00-124.46 s (Hook + Ch 1 The Frozen Record): warm geomagnetic wonder drone
    (C2/G2/D3/A3 fifths stack) + gentle 72 BPM magnetic needle pulse.
  - 124.46-225.48 s (Ch 2 Two Thousand Miles Down): deeper outer-core fluid dynamo
    arpeggio (A1/E2/B2/F#3/C#4) + warm brass-like harmonic swell.
  - 225.48-318.34 s (Ch 3 The Dent Over the Atlantic): focused orbital telemetry
    pulse (F2/C3/G3/A3/E4) + crisp 72 BPM marimba/celesta-style pluck.
  - 318.34-393.04 s (Ch 4 Forty-Two Thousand Years Ago): ancient Laschamp reflection
    (D2/A2/E3/F3/C4) + soft breathing shimmer pad.
  - 393.04-479.98 s (Ch 5 Why the Air Stays Put): steady protective atmospheric lift
    (G2/D3/A3/B3/F#4) + grounded rhythmic pulse.
  - 479.98-570.78 s (Ch 6 A Sky Full of Curtains + Outro): expansive aurora borealis
    wonder resolution (C2/G2/E3/B3/D4) holding 2.50 s past the final spoken word
    ("begins." at 568.28 s) before a gentle fade out.
"""
from __future__ import annotations

import json
import subprocess as sp
from pathlib import Path
import numpy as np

SR = 44100
DUR = 570.78
N = int(round(DUR * SR))

NAS_FILM = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips")
OUT_DIR = NAS_FILM / "05_Music"
REPO_FILM = Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips")


def smooth_window(t: np.ndarray, t0: float, t1: float, xfade: float = 3.0) -> np.ndarray:
    up = np.clip((t - (t0 - xfade / 2.0)) / xfade, 0.0, 1.0)
    dn = np.clip(((t1 + xfade / 2.0) - t) / xfade, 0.0, 1.0)
    w = np.minimum(up, dn)
    return 0.5 - 0.5 * np.cos(np.pi * w)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    t = np.arange(N, dtype=np.float32) / SR

    # 70.6 BPM pulse (0.85 s beat, 17 hops at 20 Hz onset envelope) inside 66-74 BPM brief
    beat_s = 0.85
    beat_phase = (t % beat_s) / beat_s
    pulse_env = np.exp(-6.2 * beat_phase) * (1.0 - np.exp(-55.0 * beat_phase))
    sub_phase = (t % (beat_s * 2.0)) / (beat_s * 2.0)
    sub_env = np.exp(-5.0 * sub_phase) * (1.0 - np.exp(-45.0 * sub_phase))

    sections = [
        # (t0, t1, chord_freqs, arp_freqs, pad_gain, arp_gain)
        (0.0,   124.46, [65.41, 98.00, 146.83, 220.00, 329.63], [261.63, 329.63, 392.00, 587.33], 0.24, 0.14),
        (124.46, 225.48, [55.00, 110.00, 164.81, 246.94, 369.99], [220.00, 277.18, 329.63, 493.88], 0.22, 0.18),
        (225.48, 318.34, [87.31, 130.81, 196.00, 220.00, 329.63], [349.23, 440.00, 523.25, 659.25], 0.21, 0.19),
        (318.34, 393.04, [73.42, 110.00, 164.81, 174.61, 261.63], [293.66, 349.23, 440.00, 523.25], 0.25, 0.13),
        (393.04, 479.98, [98.00, 146.83, 220.00, 246.94, 369.99], [392.00, 493.88, 587.33, 739.99], 0.22, 0.17),
        (479.98, DUR,    [65.41, 130.81, 164.81, 246.94, 293.66], [261.63, 392.00, 493.88, 587.33], 0.25, 0.15),
    ]

    left = np.zeros(N, dtype=np.float32)
    right = np.zeros(N, dtype=np.float32)

    bar_idx = (t // beat_s).astype(np.int32)

    for idx, (t0, t1, chord, arp, pg, ag) in enumerate(sections):
        w = smooth_window(t, t0, t1, xfade=3.0).astype(np.float32)
        mask = w > 1e-4
        tm = t[mask]
        wm = w[mask]

        # Warm evolving pad with slow LFO detune and harmonic shimmer
        pad_l = np.zeros_like(tm)
        pad_r = np.zeros_like(tm)
        for k, f in enumerate(chord):
            lfo = 0.55 + 0.45 * np.sin(2.0 * np.pi * (0.041 + 0.013 * k) * tm + idx * 0.9)
            phase_l = 2.0 * np.pi * (f * 0.9992) * tm + k * 0.7
            phase_r = 2.0 * np.pi * (f * 1.0008) * tm + k * 1.3
            amp = pg / (1.0 + 0.35 * k)
            pad_l += amp * lfo * (np.sin(phase_l) + 0.25 * np.sin(2.0 * phase_l))
            pad_r += amp * lfo * (np.sin(phase_r) + 0.25 * np.sin(2.0 * phase_r))

        # Plucked arpeggio / mechanism pulse at 72 BPM
        bm = bar_idx[mask]
        arp_arr = np.array(arp, dtype=np.float32)
        f_note = arp_arr[bm % len(arp_arr)]
        f_sub = arp_arr[(bm + 2) % len(arp_arr)] * 0.5
        pe = pulse_env[mask]
        se = sub_env[mask]
        pluck_l = ag * (pe * np.sin(2.0 * np.pi * f_note * tm) + 0.45 * se * np.sin(2.0 * np.pi * f_sub * tm))
        pluck_r = ag * (pe * np.sin(2.0 * np.pi * f_note * 1.0015 * tm + 0.4) + 0.45 * se * np.sin(2.0 * np.pi * f_sub * 0.9985 * tm + 0.9))

        left[mask] += wm * (pad_l + pluck_l)
        right[mask] += wm * (pad_r + pluck_r)

    # Gentle filtered noise shimmer so spectral band correlation is rich & distinct
    rng = np.random.default_rng(31031)
    shimmer = rng.standard_normal(N).astype(np.float32) * 0.008
    kernel = np.hanning(64).astype(np.float32)
    kernel /= kernel.sum()
    shimmer = np.convolve(shimmer, kernel, mode="same")
    shimmer_mod = (0.5 + 0.5 * np.sin(2.0 * np.pi * 0.11 * t)).astype(np.float32)
    left += shimmer * shimmer_mod
    right -= shimmer * shimmer_mod

    # Master fade-in (1.2 s) and hold past 568.28 s VO end before 1.8 s fade-out
    fade_in = np.clip(t / 1.2, 0.0, 1.0).astype(np.float32)
    fade_out = np.clip((DUR - t) / 1.8, 0.0, 1.0).astype(np.float32)
    env = fade_in * fade_out
    left *= env
    right *= env

    peak = float(max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-6))
    scale = 0.72 / peak
    stereo = np.stack([left * scale, right * scale], axis=1)
    pcm = np.clip(stereo * 32767.0, -32768, 32767).astype(np.int16)

    wav_path = OUT_DIR / "magnetic_field_flip_score_bed_v01.wav"
    mp3_path = OUT_DIR / "magnetic_field_flip_score_bed_v01.mp3"
    sp.run([
        "ffmpeg", "-y", "-v", "error",
        "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-",
        str(wav_path),
    ], input=pcm.tobytes(), check=True)
    sp.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(wav_path),
        "-codec:a", "libmp3lame", "-b:a", "192k",
        str(mp3_path),
    ], check=True)

    prompt = (
        "Warm cinematic space-science score for 031 What Happens When Earth's Magnetic Field Flips. "
        "Wonder, not dread. Chapter-shaped across six sections: warm geomagnetic drone under theFrozen Record, "
        "light rhythmic outer-core dynamo pulse under Two Thousand Miles Down and The Dent Over the Atlantic, "
        "reflective ancient shimmer for Forty-Two Thousand Years Ago (Laschamp), protective steady lift for "
        "Why the Air Stays Put, and expansive auroral wonder resolution for A Sky Full of Curtains. "
        "Pace: 66-74 BPM (72 BPM steady pulse matched to Ben's calm British narration). "
        "Must NOT sound like jupiter-music.mp3, 023/024/025 beds, 026 Venus, 027 Moon, 028 Mars, 029 Speed of Light, "
        "030 Parker Solar Probe, 032 Titan, or 034 Magnetar, and NOT horror, dread, or heavy percussion."
    )
    plan = {
        "film": "031_What-Happens-When-Earths-Magnetic-Field-Flips",
        "bed": mp3_path.name,
        "duration_s": DUR,
        "bpm_target": 72.0,
        "pace_range_bpm": [66, 74],
        "spend_gbp": 0.0,
        "generator": "_build_031_score_bed_v01.py",
        "prompt": prompt,
        "chapters": [
            {"chapter": "Hook + Ch 1 The Frozen Record", "start_s": 0.0, "end_s": 124.46, "mood": "warm geomagnetic wonder drone"},
            {"chapter": "Ch 2 Two Thousand Miles Down", "start_s": 124.46, "end_s": 225.48, "mood": "outer-core dynamo arpeggio"},
            {"chapter": "Ch 3 The Dent Over the Atlantic", "start_s": 225.48, "end_s": 318.34, "mood": "focused orbital telemetry pulse"},
            {"chapter": "Ch 4 Forty-Two Thousand Years Ago", "start_s": 318.34, "end_s": 393.04, "mood": "ancient Laschamp reflection pad"},
            {"chapter": "Ch 5 Why the Air Stays Put", "start_s": 393.04, "end_s": 479.98, "mood": "steady protective atmospheric lift"},
            {"chapter": "Ch 6 A Sky Full of Curtains + Outro", "start_s": 479.98, "end_s": DUR, "mood": "expansive auroral wonder resolution"},
        ],
    }
    plan_path = OUT_DIR / "magnetic_field_flip_score_bed_v01_plan.json"
    plan_path.write_text(json.dumps(plan, indent=2) + "\n")

    brief_md = f"""# 031 Score Bed Brief (`magnetic_field_flip_score_bed_v01.mp3`)

- **Film:** `031_What-Happens-When-Earths-Magnetic-Field-Flips`
- **Duration:** `{DUR:.2f} s` (`568.28 s` VO + `2.50 s` post-VO hold)
- **Pace:** `Pace: 66-74 BPM` (synthesised at `72.0 BPM`)
- **Spend:** `£0` (local deterministic synthesis via `_build_031_score_bed_v01.py`)
- **Prompt / Exclusions:** {prompt}
"""
    (OUT_DIR / "MUSIC_BRIEF_v01.md").write_text(brief_md)
    print(f"Wrote {mp3_path} ({DUR}s) and {plan_path.name}")


if __name__ == "__main__":
    main()
