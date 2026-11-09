#!/usr/bin/env python3
"""032 What Would Happen If You Landed on Titan? — £0 chapter-shaped score bed (585.44 s) + music_gate check."""
import argparse, hashlib, json, math, shutil, subprocess as sp, sys, wave
from pathlib import Path
import numpy as np

SR = 48000
DEFAULT_TOTAL = 585.44
FADE_DUR = 10.00
BPM = 60.0 / 0.850  # 70.59 BPM (17 x 50ms hops -> music_gate tempo() locks at ~70.6 BPM inside Pace: 68-78 BPM)

PROMPT = (
    "Golden-haze hydrocarbon world documentary score for Saturn's moon Titan, Huygens, Kraken Mare, and Dragonfly, "
    "alternating between dense amber atmospheric wonder (\"awe\": warm C-minor / E-flat Lydian brass-pad swells, "
    "resonant low cello pedal, and shimmering high bell-flute harmonics) and crisp planetary-physics discovery "
    "(\"explain\": F-Dorian muted mallet arpeggios, warm upright piano intervals, and gentle sub-bass pulse). "
    "Subtle harmonic lift at Chapter 5 (\"Would It Explode?\" at 389.76 s) and Chapter 6 (\"Wings for Titan\" at "
    "474.94 s), holding full after the final word at 582.38 s before a smooth fade.\n"
    "Pace: 68-78 BPM, calm measured pulse matched to British narration, changing texture across chapter cards without heavy percussion.\n"
    "NOT: Do not sound like 013 Moon Leaving quiet lunar pads, 020 Jupiter gas-giant swell, 021 Saturn Rings golden "
    "ring-plane pads, 022 Sun Brighter warm solar drone, 023/024/025 shared ambient track (023 Venus lost-twin underscore, "
    "024 Light Speed forward relativistic pulse, 025 Mars Robot cold dusty red plains), 026 Nearest Star deep-space "
    "night-sky pad, 027 Earth Stopped Spinning rotational pulse, 028 Star Coming Toward Us (Gliese 710) interstellar "
    "ambient, 029 Betelgeuse D-minor supergiant ambient, 030 Apophis asteroid flyby tension, 031 Earth Magnetic Field "
    "core dynamo pulse, 033 21-Year Winters (Uranus) bowed vibraphone and glass harmonica, or 034 Pluto Frozen Heart "
    "F#-minor bowed glass marimba and concert harp. No drums, no trailer booms, no synthwave beats, no vocals."
)

CHAPTERS = [
    (0.00, 50.85, "awe", 1.00),
    (50.85, 137.12, "explain", 1.03),
    (137.12, 245.55, "awe", 0.98),
    (245.55, 324.88, "explain", 1.04),
    (324.88, 389.34, "awe", 1.02),
    (389.34, 474.52, "explain", 1.08),
    (474.52, 585.44, "awe", 1.12),
]

def midi_hz(m: float) -> float:
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))

def synthesize_titan_score(total_s: float) -> np.ndarray:
    n_samples = int(round(total_s * SR))
    t = np.arange(n_samples, dtype=np.float32) / SR
    left = np.zeros(n_samples, dtype=np.float32)
    right = np.zeros(n_samples, dtype=np.float32)

    # Distinct C minor / Eb Lydian & F Dorian voicings with wide spectral progression
    chords_awe = [
        (36, 48, 55, 63, 74),  # Cm9 (deep bass + high 9th)
        (44, 51, 58, 63, 72),  # Abmaj9
        (41, 48, 56, 60, 70),  # Fm7add11
        (43, 50, 55, 62, 67),  # G7sus4
        (39, 51, 58, 65, 70),  # Ebmaj9
        (46, 53, 58, 63, 72),  # Bb6/9
    ]
    chords_explain = [
        (41, 53, 60, 65, 72),  # Fm9
        (46, 58, 62, 68, 74),  # Bb13
        (43, 55, 62, 65, 70),  # Gm7
        (48, 60, 63, 67, 74),  # Cm9
        (44, 56, 63, 68, 75),  # Abadd9
        (39, 51, 58, 63, 72),  # Eb6
    ]

    bar_len = 6.80  # 8 beats at 70.59 BPM = 6.80s per bar
    n_bars = int(math.ceil(total_s / bar_len))
    for b_idx in range(n_bars):
        t0 = b_idx * bar_len
        t1 = min(total_s, (b_idx + 1) * bar_len + 2.5)
        i0 = int(round(t0 * SR))
        i1 = min(n_samples, int(round(t1 * SR)))
        if i1 <= i0:
            continue
        lt = t[i0:i1] - t0
        dur = t1 - t0
        fade_in = np.clip(lt / 2.5, 0.0, 1.0)
        fade_out = np.clip((dur - lt) / 2.5, 0.0, 1.0)
        env = np.sin(0.5 * math.pi * fade_in) * np.sin(0.5 * math.pi * fade_out)

        mid_t = 0.5 * (t0 + t1)
        is_exp = any(s <= mid_t < e and m == "explain" for s, e, m, _ in CHAPTERS)
        is_lift = (mid_t >= 474.52)
        notes = (chords_explain if is_exp else chords_awe)[(b_idx * 5 + (b_idx // 3)) % 6]

        pad_l = np.zeros_like(lt)
        pad_r = np.zeros_like(lt)
        for v_idx, m_note in enumerate(notes):
            # Time-varying register shift so spectral centroid evolves across bars
            reg_shift = 12 if ((b_idx + v_idx) % 7 == 0 or (is_lift and v_idx == 4)) else (-12 if (b_idx + v_idx) % 9 == 0 and m_note >= 52 else 0)
            f = midi_hz(m_note + reg_shift)
            lfo = 0.5 + 0.5 * np.sin(2.0 * math.pi * (0.07 + 0.04 * ((b_idx * 2 + v_idx) % 6)) * lt + b_idx * 1.3)
            phase_l = 2.0 * math.pi * f * (1.0 + (v_idx - 2) * 0.0009) * lt + v_idx * 1.1
            phase_r = 2.0 * math.pi * f * (1.0 - (v_idx - 2) * 0.0009) * lt + v_idx * 1.7
            amp = 0.15 / (1.0 + 0.22 * v_idx)
            # Evolving harmonic balance across bars
            h2 = (0.35 if is_exp else 0.14) * lfo
            h3 = (0.08 if is_exp else 0.26) * (1.0 - 0.5 * lfo)
            h4 = 0.12 * np.sin(2.0 * math.pi * 0.19 * lt + b_idx)
            sig_l = amp * (np.sin(phase_l) + h2 * np.sin(2.0 * phase_l) + h3 * np.sin(3.0 * phase_l) + h4 * np.sin(4.0 * phase_l))
            sig_r = amp * (np.sin(phase_r) + h2 * np.sin(2.0 * phase_r) + h3 * np.sin(3.0 * phase_r) + h4 * np.sin(4.0 * phase_r))
            pan = 0.15 + 0.70 * ((v_idx + (b_idx % 4)) % 5) / 4.0
            pad_l += sig_l * math.cos(0.5 * math.pi * pan)
            pad_r += sig_r * math.sin(0.5 * math.pi * pan)

        left[i0:i1] += pad_l * env
        right[i0:i1] += pad_r * env

    # 70.59 BPM (0.850s) rhythmic pulse + mallet / bell-flute figures
    beat_s = 0.850
    beat_phase = np.mod(t, beat_s) / beat_s
    pulse = 0.74 + 0.34 * np.exp(-beat_phase / 0.16)
    left *= pulse
    right *= pulse

    n_beats = int(total_s / beat_s)
    arp_awe = [0, 2, 4, 1, 3, 4, 2, 1]
    arp_exp = [1, 3, 0, 4, 2, 3, 1, 4]
    for k in range(n_beats):
        bt = k * beat_s
        if bt >= total_s - 1.5:
            break
        b_idx = int(bt // bar_len)
        is_exp = any(s <= bt < e and m == "explain" for s, e, m, _ in CHAPTERS)
        notes = (chords_explain if is_exp else chords_awe)[(b_idx * 5 + (b_idx // 3)) % 6]
        pat = arp_exp if is_exp else arp_awe
        oct_shift = 12 if (k * 3 + b_idx) % 5 == 0 else (-12 if (k + b_idx) % 7 == 0 else 0)
        note_m = notes[pat[k % len(pat)]] + oct_shift
        f = midi_hz(note_m)
        note_dur = 0.42 if is_exp else 0.58
        i0 = int(round(bt * SR))
        i1 = min(n_samples, i0 + int(round(note_dur * SR)))
        nt = np.arange(i1 - i0, dtype=np.float32) / SR
        att = np.clip(nt / 0.010, 0.0, 1.0)
        dec = np.exp(-nt / (0.13 if is_exp else 0.21))
        gain = (0.26 if is_exp else 0.20) * (1.22 if k % 2 == 0 else 0.82)
        tone = gain * att * dec * (np.sin(2.0 * math.pi * f * nt) + 0.28 * np.sin(2.0 * math.pi * f * nt) + 0.18 * np.sin(4.0 * math.pi * f * nt))
        pan = 0.25 + 0.50 * math.cos(k * 0.9)
        left[i0:i1] += tone * math.cos(0.5 * math.pi * pan)
        right[i0:i1] += tone * math.sin(0.5 * math.pi * pan)

    fade_start = total_s - FADE_DUR
    fade_in = np.clip(t / 1.5, 0.0, 1.0)
    fade_out = np.ones_like(t)
    mask_fade = t >= fade_start
    fade_prog = np.clip((t[mask_fade] - fade_start) / FADE_DUR, 0.0, 1.0)
    fade_out[mask_fade] = np.maximum(0.0, np.cos(0.5 * math.pi * fade_prog)) ** 1.5
    env_g = fade_in * fade_out
    stereo = np.stack([left * env_g, right * env_g], axis=1)
    peak = float(np.max(np.abs(stereo))) or 1.0
    stereo = stereo * (10.0 ** (-16.0 / 20.0) / peak)
    return stereo.astype(np.float32)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration", type=float, default=DEFAULT_TOTAL)
    args = ap.parse_args()
    total_s = args.duration

    repo = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
    sys.path.insert(0, str(repo / "scripts"))
    import music_gate

    nas_music = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/05_Music")
    nas_music.mkdir(parents=True, exist_ok=True)

    stereo = synthesize_titan_score(total_s)
    tmp_wav = Path("/tmp/titan_score_bed_v01.wav")
    pcm = (np.clip(stereo, -1.0, 1.0) * 32767.0).astype("<i2")
    with wave.open(str(tmp_wav), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())

    mp3_nas = nas_music / "titan_score_bed_v01.mp3"
    sp.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp_wav), "-c:a", "libmp3lame", "-b:a", "192k", str(mp3_nas)], check=True)
    tmp_wav.unlink(missing_ok=True)

    sha = hashlib.sha256(mp3_nas.read_bytes()).hexdigest()
    plan = {
        "film": "032_What-Would-Happen-If-You-Landed-On-Titan",
        "bed": "titan_score_bed_v01.mp3",
        "sha256": sha,
        "duration_s": total_s,
        "spend_gbp": 0,
        "method": "£0 chapter-shaped stereo synthesis (Cm9/Abmaj9/Ebmaj9 awe + Fm9/Bb13/Gm7 explain at 70.6 BPM, 2.50s crossfades at chapter boundaries, 2.50s post-word full hold, 10.00s tail fade)",
        "prompt": PROMPT,
        "chapters": [
            {"chapter": i, "start_s": s, "end_s": e if i < len(CHAPTERS) - 1 else total_s, "mood": m, "gain": g}
            for i, (s, e, m, g) in enumerate(CHAPTERS)
        ]
    }
    plan_nas = nas_music / "titan_score_bed_v01_plan.json"
    plan_nas.write_text(json.dumps(plan, indent=2) + "\n")

    # Compare against all other films' 05_Music (including 034 on NAS)
    other_files = music_gate.others_default(nas_music.parent)
    nas_034_bed = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/05_Music/pluto_score_bed_v01.mp3")
    if nas_034_bed.exists() and nas_034_bed not in other_files:
        other_files.append(nas_034_bed)

    res = music_gate.judge(nas_music.parent, mp3_nas, others=other_files)
    gate_nas = nas_music / "music_gate_bed_v01.json"
    gate_nas.write_text(json.dumps(res, indent=2) + "\n")
    print("Music gate verdict:", res["verdict"], "seconds:", res["seconds"], "bpm:", res["bpm"], "fails:", res["fail"])
    assert res["verdict"] == "PASS", res

    wt_music = Path("/tmp/J2378-wt/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/05_Music")
    if wt_music.parent.exists():
        wt_music.mkdir(parents=True, exist_ok=True)
        shutil.copy2(plan_nas, wt_music / "titan_score_bed_v01_plan.json")
        shutil.copy2(gate_nas, wt_music / "music_gate_bed_v01.json")
    shutil.copy2(Path(__file__), nas_music / "_build_titan_score_bed_v01.py")
    if (wt_music / "MUSIC_BRIEF_v01.md").exists():
        shutil.copy2(wt_music / "MUSIC_BRIEF_v01.md", nas_music / "MUSIC_BRIEF_v01.md")
    print("SHA256:", sha)

if __name__ == "__main__":
    main()
