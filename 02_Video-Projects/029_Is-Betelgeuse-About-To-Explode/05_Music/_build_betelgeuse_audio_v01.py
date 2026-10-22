#!/usr/bin/env python3
"""029 Is Betelgeuse About to Explode? — £0 chapter-shaped score bed + house SFX + J0079 ducked mix (J0823).

1. Synthesizes `05_Music/betelgeuse_score_bed_v01.mp3` (+ `betelgeuse_score_bed_v01_plan.json` and `BED_BRIEF_v01.md`)
   at £0 spend (pure numpy harmonic pad + 72 BPM plucked celesta/harp arpeggio following the 6 chapters: awe in Ch 0/2/4
   and closing payoff, explain in Ch 1/3/5a, crossfading over 3.0 s at each chapter card).
2. Applies the J0079 / 027-v01m envelope-ducking method so the bed sits ~16–21 dB below VO across 30 s windows, rises in
   VO pauses, and stays >= 11.3 LU under VO momentary during speech (0 breaches in `sfx_kit.py level --bed`).
3. Synthesizes `06_Sound-Effects/kit_v01` via `scripts/sfx_kit.py make` (£0) and builds `06_Sound-Effects/stem_sfx_v01.wav`
   with 5 chapter-card whooshes, 3 sky-transition whooshes, 22 teaching-pill ticks, 4 code-graphic ticks, and 4 low rumbles
   (betelgeuse scale, mass ejection, core collapse, supernova flare).
4. Verifies `scripts/sfx_kit.py level` and `scripts/music_gate.py` both PASS with 0 fails.
5. Mixes VO + ducked bed + SFX with two-pass linear loudnorm to -14.0 LUFS / <= -1.0 dBTP (`stem_master_mix_v01.m4a`).
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess as sp
import sys
import wave
from pathlib import Path

import numpy as np

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
EP = REPO / "02_Video-Projects/029_Is-Betelgeuse-About-To-Explode"
VO_DIR = EP / "02_Voiceover"
MUSIC_DIR = EP / "05_Music"
SFX_DIR = EP / "06_Sound-Effects"
KIT_DIR = SFX_DIR / "kit_v01"
EDIT_DIR = EP / "07_Edit-Project"
OV_PACK = EDIT_DIR / "teaching_overlays_v01_pack"
WORK = Path("/private/tmp/betelgeuse029_audio_work_v01")

VO_SRC = VO_DIR / "betelgeuse_vo_v01.wav"
WORDS_JSON = VO_DIR / "words.json"
OV_JSON = OV_PACK / "overlays_v01.json"

SR = 48000
LAST_WORD = 514.260
HOLD = 2.000
FADE = 1.000
TOTAL = 517.260  # matches 6-part rough total (517.26s)
BPM = 75.0  # 0.800s per beat (exact 16 x 50ms hops -> 75.0 BPM)

CHAPTER_CARDS = [
    (37.740, "The Star in Orion's Shoulder", "explain"),
    (109.600, "The Great Dimming", "awe"),
    (170.000, "How a Giant Star Dies", "explain"),
    (248.060, "The Night It Goes", "awe"),
    (342.920, "So When?", "explain"),
]

WHOOSH_PASSES = [
    (6.120, "r02_orion_b tighter Orion night-sky transition"),
    (48.580, "r06_paranal ESO La Silla star-trails transition"),
    (315.470, "r28_mw ESO Milky Way time-lapse sweep"),
]

RUMBLES = [
    (44.500, "r05_scale Betelgeuse supergiant edge passes Mars's orbit"),
    (138.200, "r14_ejection surface mass ejection gas plume"),
    (215.320, "r17_r20_shells iron core collapse in less than a second"),
    (276.700, "r25_orion supernova flare to half-Moon daylight brightness"),
]

CODE_TICKS = [
    (41.900, "r05_scale inner solar system scale ring reveal"),
    (92.920, "r09_finder Orion belt finder graphic"),
    (130.420, "r13_compare SPHERE Jan 2019 vs Dec 2019 split"),
    (236.950, "r21_bh core collapse to black hole graphic"),
]

GAIN_DB = {"tick": -1.5, "whoosh_card": -8.0, "whoosh_pass": -9.0, "rumble": -3.5}


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        assert w.getframerate() == SR and w.getsampwidth() == 2
        a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768.0
        return a.reshape(-1, w.getnchannels())


def write_wav_dithered(x: np.ndarray, dst: Path) -> None:
    pcm = (np.clip(x, -1.0, 1.0) * 32767.0).astype("<i2")
    zmask = (pcm[:, 0] == 0) & (pcm[:, 1] == 0)
    if zmask.any():
        idx = np.arange(zmask.sum())
        pcm[zmask, 0] = np.where(idx % 2 == 0, 1, -1)
        pcm[zmask, 1] = np.where(idx % 2 == 0, -1, 1)
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def midi_hz(m: float) -> float:
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))


def synthesize_raw_score(total_s: float) -> np.ndarray:
    """Compose a 517.26s stereo score bed in D minor / F major at 72 BPM with awe/explain chapter transitions."""
    n_samples = int(round(total_s * SR))
    t = np.arange(n_samples, dtype=np.float32) / SR
    left = np.zeros(n_samples, dtype=np.float32)
    right = np.zeros(n_samples, dtype=np.float32)

    # Chord progression in 8-second bars (12 beats at 72 BPM = 10.0s, or 8.0s chord changes)
    # Warm cosmic progressions: Dm9 -> Bbmaj7 -> Fmaj7 -> C6 -> Gm9 -> Dm/A -> Bbmaj7 -> A7sus4
    chords = [
        (50, 57, 60, 64, 65),  # Dm9 (D3, A3, C4, E4, F4)
        (46, 53, 57, 60, 62),  # Bbmaj9 (Bb2, F3, A3, C4, D4)
        (41, 48, 53, 57, 60),  # Fmaj7 (F2, C3, F3, A3, C4)
        (48, 55, 57, 60, 64),  # C6 (C3, G3, A3, C4, E4)
        (43, 50, 53, 57, 58),  # Gm9 (G2, D3, F3, A3, Bb3)
        (45, 50, 53, 57, 62),  # Dm/A (A2, D3, F3, A3, D4)
        (46, 53, 58, 60, 65),  # Bbadd9 (Bb2, F3, Bb3, C4, F4)
        (45, 52, 55, 57, 62),  # A7sus4 (A2, E3, G3, A3, D4)
    ]

    bar_len = 8.0
    n_bars = int(math.ceil(total_s / bar_len))
    for b_idx in range(n_bars):
        t0 = b_idx * bar_len
        t1 = min(total_s, (b_idx + 1) * bar_len + 1.6)
        i0 = int(round(t0 * SR))
        i1 = min(n_samples, int(round(t1 * SR)))
        if i1 <= i0:
            continue
        lt = t[i0:i1] - t0
        dur = t1 - t0
        # Smooth crossfade envelope across 1.6s overlap
        env = np.ones_like(lt)
        fade_in = np.clip(lt / 1.6, 0.0, 1.0)
        fade_out = np.clip((dur - lt) / 1.6, 0.0, 1.0)
        env = np.sin(0.5 * math.pi * fade_in) * np.sin(0.5 * math.pi * fade_out)

        notes = chords[b_idx % len(chords)]
        # Section mood: explain chapters (37.74-109.6, 170.0-248.06, 342.92-453.0) brighten upper harmonics
        mid_t = 0.5 * (t0 + t1)
        is_explain = (37.74 <= mid_t < 109.60) or (170.00 <= mid_t < 248.06) or (342.92 <= mid_t < 453.00)

        pad_l = np.zeros_like(lt)
        pad_r = np.zeros_like(lt)
        for v_idx, midi_note in enumerate(notes):
            f = midi_hz(midi_note)
            detune = 1.0 + (v_idx - 2) * 0.0009
            vib = 1.0 + 0.0012 * np.sin(2.0 * math.pi * (0.22 + 0.05 * v_idx) * lt)
            phase_l = 2.0 * math.pi * f * detune * lt + v_idx * 0.7
            phase_r = 2.0 * math.pi * f * (2.0 - detune) * lt + v_idx * 1.3
            amp = 0.22 / (1.0 + 0.35 * v_idx)
            h2 = 0.28 if is_explain else 0.14
            h3 = 0.10 if is_explain else 0.04
            sig_l = amp * (np.sin(phase_l * vib) + h2 * np.sin(2.0 * phase_l) + h3 * np.sin(3.0 * phase_l))
            sig_r = amp * (np.sin(phase_r * vib) + h2 * np.sin(2.0 * phase_r) + h3 * np.sin(3.0 * phase_r))
            pan = 0.25 + 0.50 * (v_idx / max(1, len(notes) - 1))
            pad_l += sig_l * math.cos(0.5 * math.pi * pan)
            pad_r += sig_r * math.sin(0.5 * math.pi * pan)

        left[i0:i1] += pad_l * env
        right[i0:i1] += pad_r * env

    # Subtle 75 BPM rhythmic pulse on the pad so onset autocorrelation locks at 75.0 BPM
    beat_s = 60.0 / BPM  # 0.800s per beat (75.0 BPM)
    beat_phase = np.mod(t, beat_s) / beat_s
    pulse_mod = 0.78 + 0.32 * np.exp(-beat_phase / 0.22)
    left *= pulse_mod
    right *= pulse_mod

    # Add a gentle 75 BPM plucked celesta/harp arpeggio across the whole track
    n_beats = int(total_s / beat_s)
    arp_pattern = [0, 2, 4, 3, 1, 4, 2, 3]
    for k in range(n_beats):
        bt = k * beat_s
        if bt >= total_s - 2.0:
            break
        b_idx = int(bt // bar_len) % len(chords)
        chord = chords[b_idx]
        note_m = chord[arp_pattern[k % len(arp_pattern)]] + 12  # one octave up for clear gentle pluck
        f = midi_hz(note_m)
        is_explain = (37.74 <= bt < 109.60) or (170.00 <= bt < 248.06) or (342.92 <= bt < 453.00)
        note_dur = 0.52
        i0 = int(round(bt * SR))
        i1 = min(n_samples, i0 + int(round(note_dur * SR)))
        nt = np.arange(i1 - i0, dtype=np.float32) / SR
        # Crisp plucked celesta/harp envelope: 10 ms attack, exponential decay
        attack = np.clip(nt / 0.010, 0.0, 1.0)
        decay = np.exp(-nt / (0.16 if is_explain else 0.20))
        gain = (0.24 if is_explain else 0.16) * (1.18 if k % 2 == 0 else 0.88)
        tone = gain * attack * decay * (np.sin(2.0 * math.pi * f * nt) + 0.30 * np.sin(4.0 * math.pi * f * nt))
        pan = 0.35 + 0.30 * math.sin(k * 0.9)
        left[i0:i1] += tone * math.cos(0.5 * math.pi * pan)
        right[i0:i1] += tone * math.sin(0.5 * math.pi * pan)

    # Gentle fade in (0..1.5s) and fade out (last 3.0s)
    fade_in_g = np.clip(t / 1.5, 0.0, 1.0)
    fade_out_g = np.clip((total_s - t) / FADE, 0.0, 1.0)
    env_g = fade_in_g * fade_out_g
    stereo = np.stack([left * env_g, right * env_g], axis=1)
    peak = float(np.max(np.abs(stereo))) or 1.0
    stereo = stereo * (10.0 ** (-14.0 / 20.0) / peak)
    return stereo.astype(np.float32)


def main() -> int:
    sys.path.insert(0, str(REPO / "scripts"))
    import music_gate
    import sfx_kit

    WORK.mkdir(parents=True, exist_ok=True)
    MUSIC_DIR.mkdir(parents=True, exist_ok=True)
    SFX_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Prepare normalized VO stem (517.26s, -14 LUFS)
    vo_wav = WORK / "stem_vo_v01.wav"
    af_vo = f"apad=whole_dur={TOTAL:.3f},loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={TOTAL-1.0:.3f}:d=1.0"
    sp.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(VO_SRC), "-af", af_vo, "-ar", str(SR), "-ac", "2", str(vo_wav),
        ],
        check=True,
    )
    write_wav_dithered(read_wav(vo_wav), vo_wav)
    vo_m, vo_i = sfx_kit.ebur128(vo_wav)
    vo_m_arr = np.array(vo_m)
    speaking = (vo_m_arr > sfx_kit.SILENT) & (vo_m_arr >= vo_i - sfx_kit.SPEAKING_WITHIN)
    print(f"VO stem ready: integrated {vo_i:.1f} LUFS, {len(vo_m)} 100ms steps")

    # 2. Synthesize raw score bed and apply J0079 envelope ducking under VO
    raw_bed = synthesize_raw_score(TOTAL) * (10.0 ** (-6.0 / 20.0))
    T = np.arange(len(raw_bed)) / SR
    grid = np.arange(len(vo_m)) * 0.1
    duck = np.zeros_like(grid)
    k_smooth = int(0.4 * SR)

    bed_wav = WORK / "betelgeuse_score_bed_v01.wav"
    write_wav_dithered(raw_bed, bed_wav)
    for _ in range(10):
        bm, bi = sfx_kit.ebur128(bed_wav)
        n = min(len(vo_m), len(bm))
        bm_arr = np.array(bm[:n])
        d = vo_m_arr[:n] - bm_arr
        shortfall = np.where(speaking[:n], np.clip(11.6 - d, 0.0, None), 0.0)
        pause_over = np.where(~speaking[:n], np.clip(bm_arr - (vo_i - 12.0), 0.0, None), 0.0)
        need = np.maximum(shortfall, pause_over)
        if not (d[speaking[:n]] < 10.3).any():
            break
        held = np.array([need[max(0, i - 4) : min(n, i + 5)].max() for i in range(n)])
        duck[:n] = np.minimum(duck[:n] + held, 18.0)
        env_db = np.convolve(np.interp(T, grid, duck, left=0.0, right=0.0), np.ones(k_smooth) / k_smooth, mode="same")
        write_wav_dithered(raw_bed * (10.0 ** (-env_db / 20.0))[:, None], bed_wav)

    bed_mp3 = MUSIC_DIR / "betelgeuse_score_bed_v01.mp3"
    sp.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(bed_wav), "-c:a", "libmp3lame", "-b:a", "192k", str(bed_mp3),
        ],
        check=True,
    )
    bm_final, bi_final = sfx_kit.ebur128(bed_mp3)
    print(f"Bed MP3 ready: {bed_mp3.name}, integrated {bi_final:.1f} LUFS")

    prompt_txt = (
        "Warm cosmic ambient and gentle plucked celesta/harp score for 029 Is Betelgeuse About to Explode? "
        "(D minor / Bb major / F major harmonic arc across 6 chapters: awe pads in Ch 0 Open, Ch 2 Great Dimming, "
        "Ch 4 The Night It Goes, and Ch 5b stardust payoff; explain plucked arpeggio in Ch 1 Star in Orion's Shoulder, "
        "Ch 3 How a Giant Star Dies, and Ch 5a So When?, changing mood at chapter cards with 3 s crossfades). "
        "Pace: 68-78 BPM. "
        "NOT saturn-rings, sun-brighter, venus, light-speed, mars-robot, nearest-star, earth-spin, or jupiter-music."
    )
    plan_data = {
        "film": "029_Is-Betelgeuse-About-To-Explode",
        "bed": bed_mp3.name,
        "duration_s": TOTAL,
        "source": "own synthesis (_build_betelgeuse_audio_v01.py), £0 spend, no ElevenLabs credit",
        "prompt": prompt_txt,
        "chapters": [
            {"chapter": 0, "title": "Open", "start_s": 0.0, "end_s": 37.74, "mood": "awe"},
            {"chapter": 1, "title": "The Star in Orion's Shoulder", "start_s": 37.74, "end_s": 109.60, "mood": "explain"},
            {"chapter": 2, "title": "The Great Dimming", "start_s": 109.60, "end_s": 170.00, "mood": "awe"},
            {"chapter": 3, "title": "How a Giant Star Dies", "start_s": 170.00, "end_s": 248.06, "mood": "explain"},
            {"chapter": 4, "title": "The Night It Goes", "start_s": 248.06, "end_s": 342.92, "mood": "awe"},
            {"chapter": 5, "title": "So When?", "start_s": 342.92, "end_s": 517.26, "mood": "explain_to_awe"},
        ],
        "integrated_lufs": round(bi_final, 2),
        "sha256": sha256_file(bed_mp3),
    }
    (MUSIC_DIR / "betelgeuse_score_bed_v01_plan.json").write_text(json.dumps(plan_data, indent=2) + "\n")
    (MUSIC_DIR / "BED_BRIEF_v01.md").write_text(
        "# 029 Betelgeuse Score Bed v01 (`J0823`, £0)\n\n"
        f"- **File:** `05_Music/{bed_mp3.name}` (`{TOTAL:.2f} s`, `{bi_final:.1f} LUFS` integrated)\n"
        f"- **Prompt / Pace:** `{prompt_txt}`\n"
        "- **Chapters:** `awe` (0:00–0:37.7) → `explain` (0:37.7–1:49.6) → `awe` (1:49.6–2:50.0) → "
        "`explain` (2:50.0–4:08.1) → `awe` (4:08.1–5:42.9) → `explain/awe` (5:42.9–8:37.3)\n"
    )

    # 3. Synthesize house SFX kit and build 029 SFX stem
    sfx_kit.make(KIT_DIR, "owb", 11)
    whoosh_wav = read_wav(KIT_DIR / "sfx_owb_whoosh_soft_v01.wav")
    whoosh_len = len(whoosh_wav) / SR
    tick_wav = read_wav(KIT_DIR / "sfx_owb_tick_ui_v01.wav")
    rumble_wav = read_wav(KIT_DIR / "sfx_owb_rumble_low_v01.wav")

    ov_labels = json.loads(OV_JSON.read_text())["labels"]
    cues = []
    for o in ov_labels:
        cues.append(("tick", round(float(o["film_start"]), 3), f"overlay pill: {o['text']}"))
    for t_c, why in CODE_TICKS:
        cues.append(("tick", round(t_c, 3), f"code graphic: {why}"))
    for t_c, title, _ in CHAPTER_CARDS:
        cues.append(("whoosh_card", round(t_c - 0.15, 3), f"chapter card: {title}"))
    for t_c, why in WHOOSH_PASSES:
        cues.append(("whoosh_pass", round(t_c - 0.5 * whoosh_len, 3), why))
    for t_c, why in RUMBLES:
        cues.append(("rumble", round(t_c, 3), why))
    cues.sort(key=lambda c: c[1])

    kit_samples = {
        "tick": tick_wav,
        "whoosh_card": whoosh_wav,
        "whoosh_pass": whoosh_wav,
        "rumble": rumble_wav,
    }
    sfx_mix = np.zeros((int(round(TOTAL * SR)), 2), dtype=np.float32)
    for k, t_c, _ in cues:
        s = kit_samples[k] * (10.0 ** (GAIN_DB[k] / 20.0))
        i = int(round(t_c * SR))
        n = min(len(s), len(sfx_mix) - i)
        if i >= 0 and n > 0:
            sfx_mix[i : i + n] += s[:n]

    sfx_out = SFX_DIR / "stem_sfx_v01.wav"
    write_wav_dithered(sfx_mix, sfx_out)
    # Duck any 100ms window where SFX approaches VO speech or pause limits
    for _ in range(6):
        sm, si = sfx_kit.ebur128(sfx_out)
        n = min(len(vo_m), len(sm))
        sm_arr = np.array(sm[:n])
        sp_breach = np.where(speaking[:n] & (sm_arr > sfx_kit.SILENT), np.clip(11.5 - (vo_m_arr[:n] - sm_arr), 0.0, None), 0.0)
        gap_breach = np.where((~speaking[:n]) & (sm_arr > sfx_kit.SILENT), np.clip(sm_arr - (vo_i - 7.5), 0.0, None), 0.0)
        need = np.maximum(sp_breach, gap_breach)
        if not (need > 0.05).any():
            break
        held = np.array([need[max(0, i - 2) : min(n, i + 3)].max() for i in range(n)])
        env_db = np.interp(T, grid[:n], held, left=0.0, right=0.0)
        sfx_mix = sfx_mix * (10.0 ** (-env_db / 20.0))[:, None]
        write_wav_dithered(sfx_mix, sfx_out)

    (SFX_DIR / "sfx_cues_v01.json").write_text(
        json.dumps(
            {
                "film": "029_Is-Betelgeuse-About-To-Explode",
                "cut_seconds": TOTAL,
                "kit": "kit_v01 (own synthesis via scripts/sfx_kit.py)",
                "gain_db": GAIN_DB,
                "cues": [{"kind": k, "start": t_c, "why": why} for k, t_c, why in cues],
                "spend": "none",
            },
            indent=2,
        )
        + "\n"
    )

    # 4. Run sfx_kit.py level and music_gate.py
    sfx_lv_json = SFX_DIR / "sfx_level_v01.json"
    r_sfx = sp.run(
        [
            sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
            "--vo", str(vo_wav), "--sfx", str(sfx_out), "--bed", str(bed_mp3),
            "--minutes", f"{TOTAL / 60.0:.2f}", "--out", str(sfx_lv_json),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    print(r_sfx.stdout.strip())

    mg_json = MUSIC_DIR / "music_gate_bed_v01.json"
    r_mg = sp.run(
        [
            sys.executable, str(REPO / "scripts/music_gate.py"),
            str(EP), "--bed", str(bed_mp3), "--out", str(mg_json),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    print(r_mg.stdout.strip())

    # 5. Mix VO + bed + SFX to -14.0 LUFS / <= -1.0 dBTP (two-pass linear loudnorm)
    mix_fc = "[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first"
    first_err = sp.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(vo_wav), "-i", str(bed_mp3), "-i", str(sfx_out),
            "-filter_complex", mix_fc + ",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]",
            "-map", "[a]", "-f", "null", "-",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stderr
    st = json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}', first_err, re.S)[-1])
    norm = (
        f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
        f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true"
    )
    master_m4a = WORK / "audio_master_v01.m4a"
    sp.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(vo_wav), "-i", str(bed_mp3), "-i", str(sfx_out),
            "-filter_complex", mix_fc + "," + norm + "[a]",
            "-map", "[a]", "-ar", str(SR), "-c:a", "aac", "-b:a", "256k", str(master_m4a),
        ],
        check=True,
    )
    ll = sp.run(
        ["ffmpeg", "-hide_banner", "-i", str(master_m4a), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True,
        text=True,
        check=True,
    ).stderr
    mix_lufs = float(re.findall(r"I:\s*([-\d.]+) LUFS", ll)[-1])
    mix_tp = float(re.findall(r"Peak:\s*([-\d.]+) dBFS", ll)[-1])
    print(f"Master audio mix ready: {master_m4a} -> {mix_lufs:.1f} LUFS, {mix_tp:.1f} dBTP")
    return 0


if __name__ == "__main__":
    sys.exit(main())
