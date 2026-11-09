#!/usr/bin/env python3
"""034 Why Pluto's Frozen Heart Has Zero Craters — £0 chapter-shaped score bed (646.94 s) + music_gate check."""
import hashlib, json, math, shutil, subprocess as sp, sys, wave
from pathlib import Path
import numpy as np

SR = 48000
TOTAL = 646.94
FADE_START = 636.94
FADE_DUR = 10.00
BPM = 60.0 / 0.900  # 66.67 BPM (exact 18 x 50ms hops -> music_gate tempo() locks at 66.7 BPM inside Pace: 64-74 BPM)

PROMPT = (
    "Sub-zero Kuiper Belt space-documentary score for Pluto, Charon, and Sputnik Planitia, alternating between vast "
    "twilight horizon wonder (\"awe\": warm bowed glass marimba, high crystalline celesta harmonics, solo muted French "
    "horn, and deep velvety contrabass pad) and clean, curious astronomical discovery (\"explain\": delicate plucked "
    "concert harp, soft pizzicato violas, and warm analog Rhodes pulse). Gentle harmonic lift at the Chapter 4 midpoint "
    "twist (\"Wrong.\" at 377.40 s) as Sputnik Planitia's convecting nitrogen heart awakens, holding full past the final "
    "word at 628.82 s for 2.5 s before a smooth 10.0 s fade over 636.94-646.94 s.\n"
    "Pace: 64-74 BPM, calm measured pulse matched to British narration, lifting gently at chapter transitions without heavy percussion.\n"
    "NOT: Do not sound like 013 Moon Leaving quiet lunar pads, 020 Jupiter gas-giant swell, 021 Saturn Rings golden "
    "ring-plane pads, 022 Sun Brighter warm solar drone, 023/024/025 shared ambient track (023 Venus lost-twin underscore, "
    "024 Light Speed forward relativistic pulse, 025 Mars Robot cold dusty red plains), 026 Nearest Star deep-space "
    "night-sky pad, 027 Earth Stopped Spinning rotational pulse, 028 Star Coming Toward Us (Gliese 710) interstellar "
    "ambient, 029 Betelgeuse D-minor supergiant ambient, 030 Apophis asteroid flyby tension, 031 Earth Magnetic Field "
    "core dynamo pulse, 032 Landed on Titan sub-zero methane descent pad, or 033 21-Year Winters (Uranus) bowed vibraphone "
    "and glass harmonica. No drums, no trailer booms, no synthwave beats, no vocals."
)

CHAPTERS = [
    (0.00, 65.76, "awe", 1.00),
    (65.76, 161.44, "explain", 1.02),
    (161.44, 265.60, "awe", 0.98),
    (265.60, 374.90, "explain", 1.05),
    (374.90, 460.54, "awe", 1.12),     # Midpoint twist harmonic lift at 377.40 s
    (460.54, 545.34, "explain", 1.03),
    (545.34, 646.94, "awe", 1.00),
]

def midi_hz(m: float) -> float:
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))

def synthesize_pluto_score(total_s: float) -> np.ndarray:
    n_samples = int(round(total_s * SR))
    t = np.arange(n_samples, dtype=np.float32) / SR
    left = np.zeros(n_samples, dtype=np.float32)
    right = np.zeros(n_samples, dtype=np.float32)

    chords_awe = [
        (54, 61, 66, 69, 76),  # F#m9
        (50, 57, 62, 66, 73),  # Dmaj9
        (45, 52, 61, 64, 71),  # Amaj7
        (49, 56, 61, 64, 73),  # C#m7
        (47, 54, 59, 62, 69),  # Bm9
        (52, 59, 64, 68, 73),  # E6
    ]
    chords_explain = [
        (57, 64, 69, 73, 78),  # A6/9
        (52, 59, 66, 68, 76),  # Eadd9
        (54, 61, 64, 69, 76),  # F#m7add11
        (50, 57, 64, 66, 74),  # Dadd9
        (47, 54, 61, 66, 73),  # Bm11
        (49, 56, 64, 68, 73),  # C#m9
    ]

    bar_len = 7.20  # 8 beats at 66.67 BPM = 7.20s per bar
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
        is_lift = (374.90 <= mid_t < 460.54)
        notes = (chords_explain if is_exp else chords_awe)[b_idx % 6]

        pad_l = np.zeros_like(lt)
        pad_r = np.zeros_like(lt)
        for v_idx, m_note in enumerate(notes):
            f = midi_hz(m_note + (12 if is_lift and v_idx == 4 else 0))
            shimmer = 0.5 + 0.5 * np.sin(2.0 * math.pi * (0.11 + 0.03 * ((b_idx + v_idx) % 5)) * lt + b_idx)
            phase_l = 2.0 * math.pi * f * (1.0 + (v_idx - 2) * 0.0007) * lt + v_idx * 0.9
            phase_r = 2.0 * math.pi * f * (1.0 - (v_idx - 2) * 0.0007) * lt + v_idx * 1.4
            amp = 0.16 / (1.0 + 0.25 * v_idx)
            h_glass = (0.22 if not is_exp else 0.10) * shimmer
            h_rhodes = (0.30 if is_exp else 0.12) * (1.0 - 0.4 * shimmer)
            sig_l = amp * (np.sin(phase_l) + h_rhodes * np.sin(2.0 * phase_l) + h_glass * np.sin(3.0 * phase_l))
            sig_r = amp * (np.sin(phase_r) + h_rhodes * np.sin(2.0 * phase_r) + h_glass * np.sin(3.0 * phase_r))
            pan = 0.20 + 0.60 * ((v_idx + (b_idx % 3)) % 5) / 4.0
            pad_l += sig_l * math.cos(0.5 * math.pi * pan)
            pad_r += sig_r * math.sin(0.5 * math.pi * pan)

        left[i0:i1] += pad_l * env
        right[i0:i1] += pad_r * env

    # 66.67 BPM (0.900s) rhythmic pulse + plucked harp / glass marimba figures
    beat_s = 0.900
    beat_phase = np.mod(t, beat_s) / beat_s
    pulse = 0.72 + 0.36 * np.exp(-beat_phase / 0.18)
    left *= pulse
    right *= pulse

    n_beats = int(total_s / beat_s)
    arp_awe = [0, 3, 4, 2, 4, 1, 3, 2]
    arp_exp = [0, 2, 1, 4, 3, 2, 4, 1]
    for k in range(n_beats):
        bt = k * beat_s
        if bt >= total_s - 1.5:
            break
        b_idx = int(bt // bar_len)
        is_exp = any(s <= bt < e and m == "explain" for s, e, m, _ in CHAPTERS)
        notes = (chords_explain if is_exp else chords_awe)[b_idx % 6]
        pat = arp_exp if is_exp else arp_awe
        note_m = notes[pat[k % len(pat)]] + (12 if (k + b_idx) % 3 == 0 else 0)
        f = midi_hz(note_m)
        note_dur = 0.48 if is_exp else 0.62
        i0 = int(round(bt * SR))
        i1 = min(n_samples, i0 + int(round(note_dur * SR)))
        nt = np.arange(i1 - i0, dtype=np.float32) / SR
        att = np.clip(nt / 0.008, 0.0, 1.0)
        dec = np.exp(-nt / (0.14 if is_exp else 0.22))
        gain = (0.28 if is_exp else 0.22) * (1.20 if k % 2 == 0 else 0.85)
        tone = gain * att * dec * (np.sin(2.0 * math.pi * f * nt) + 0.35 * np.sin(3.0 * math.pi * f * nt) + 0.15 * np.sin(5.0 * math.pi * f * nt))
        pan = 0.30 + 0.40 * math.sin(k * 1.1)
        left[i0:i1] += tone * math.cos(0.5 * math.pi * pan)
        right[i0:i1] += tone * math.sin(0.5 * math.pi * pan)

    fade_in = np.clip(t / 1.5, 0.0, 1.0)
    fade_out = np.ones_like(t)
    mask_fade = t >= FADE_START
    fade_prog = np.clip((t[mask_fade] - FADE_START) / FADE_DUR, 0.0, 1.0)
    fade_out[mask_fade] = np.maximum(0.0, np.cos(0.5 * math.pi * fade_prog)) ** 1.5
    env_g = fade_in * fade_out
    stereo = np.stack([left * env_g, right * env_g], axis=1)
    peak = float(np.max(np.abs(stereo))) or 1.0
    stereo = stereo * (10.0 ** (-16.0 / 20.0) / peak)
    return stereo.astype(np.float32)

def main():
    repo = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
    sys.path.insert(0, str(repo / "scripts"))
    import music_gate

    nas_music = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/05_Music")
    local_music = repo / "02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/05_Music"
    nas_music.mkdir(parents=True, exist_ok=True)
    local_music.mkdir(parents=True, exist_ok=True)

    stereo = synthesize_pluto_score(TOTAL)
    tmp_wav = Path("/tmp/pluto_score_bed_v01.wav")
    pcm = (np.clip(stereo, -1.0, 1.0) * 32767.0).astype("<i2")
    with wave.open(str(tmp_wav), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())

    mp3_local = local_music / "pluto_score_bed_v01.mp3"
    sp.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp_wav), "-c:a", "libmp3lame", "-b:a", "192k", str(mp3_local)], check=True)
    tmp_wav.unlink(missing_ok=True)

    sha = hashlib.sha256(mp3_local.read_bytes()).hexdigest()
    plan = {
        "film": "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters",
        "bed": "pluto_score_bed_v01.mp3",
        "sha256": sha,
        "duration_s": TOTAL,
        "spend_gbp": 0,
        "method": "£0 chapter-shaped stereo synthesis (F#m9/Dmaj9/Amaj7 awe + A6/9/Eadd9 explain at 66.7 BPM, 2.50s crossfades at R08/R20/R33/R45/R54/R64, 2.50s post-word full hold 628.82-631.32s, 10.00s fade 636.94-646.94s)",
        "prompt": PROMPT,
        "chapters": [
            {"chapter": i, "start_s": s, "end_s": e, "mood": m, "gain": g}
            for i, (s, e, m, g) in enumerate(CHAPTERS)
        ]
    }
    plan_local = local_music / "pluto_score_bed_v01_plan.json"
    plan_local.write_text(json.dumps(plan, indent=2) + "\n")

    res = music_gate.judge(local_music.parent, mp3_local)
    gate_local = local_music / "music_gate_bed_v01.json"
    gate_local.write_text(json.dumps(res, indent=2) + "\n")
    print("Music gate verdict:", res["verdict"], "seconds:", res["seconds"], "bpm:", res["bpm"], "fails:", res["fail"])
    assert res["verdict"] == "PASS", res

    shutil.copy2(mp3_local, nas_music / "pluto_score_bed_v01.mp3")
    shutil.copy2(plan_local, nas_music / "pluto_score_bed_v01_plan.json")
    shutil.copy2(gate_local, nas_music / "music_gate_bed_v01.json")
    # Also copy into worktree /tmp/J2372-wt (JSON + script only, no MP3 in git!)
    wt_music = Path("/tmp/J2372-wt/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/05_Music")
    shutil.copy2(plan_local, wt_music / "pluto_score_bed_v01_plan.json")
    shutil.copy2(gate_local, wt_music / "music_gate_bed_v01.json")
    shutil.copy2(Path(__file__), wt_music / "_build_pluto_score_bed_v01.py")
    shutil.copy2(Path(__file__), nas_music / "_build_pluto_score_bed_v01.py")
    print("SHA256:", sha)

if __name__ == "__main__":
    main()
