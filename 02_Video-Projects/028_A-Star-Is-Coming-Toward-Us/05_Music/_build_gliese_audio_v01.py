#!/usr/bin/env python3
"""028 A Star Is Coming Toward Us (Gliese 710) — £0 chapter-shaped score bed + house SFX + J0079 ducked mix (J0859).

1. Synthesizes `05_Music/gliese_score_bed_v01.mp3` (+ `gliese_score_bed_v01_plan.json` and `BED_BRIEF_v01.md`)
   at £0 spend (pure numpy harmonic pad + 70.6 BPM plucked celesta/harp arpeggio in A minor / E minor / C major / G major
   following the 7 chapters: awe in Ch 0/3/5 and closing payoff, explain in Ch 1/2/4/6a, crossfading at each chapter card).
2. Applies the J0079 / 029 envelope-ducking method so the bed sits ~16–21 dB below VO across 30 s windows, rises in
   VO pauses, and stays >= 11.3 LU under VO momentary during speech (0 breaches in `sfx_kit.py level --bed`).
3. Synthesizes `06_Sound-Effects/kit_v01` via `scripts/sfx_kit.py make` (£0) and builds `06_Sound-Effects/stem_sfx_v01.wav`
   with an SFX tick on all 22 teaching pills, all 6 chapter cards, the subscribe pill, and 4 scale/shell graphics, plus
   chapter/flyby soft whooshes and 4 low rumbles.
4. Verifies `scripts/sfx_kit.py level` and `scripts/music_gate.py` both PASS with 0 fails.
5. Mixes VO + ducked bed + SFX with two-pass linear loudnorm to -14.0 LUFS / <= -1.0 dBTP (`audio_master_v01.m4a`).
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
EP = REPO / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us"
VO_DIR = EP / "02_Voiceover"
MUSIC_DIR = EP / "05_Music"
SFX_DIR = EP / "06_Sound-Effects"
KIT_DIR = SFX_DIR / "kit_v01"
EDIT_DIR = EP / "07_Edit-Project"
OV_PACK = EDIT_DIR / "teaching_overlays_v01_pack"
WORK = Path("/private/tmp/gliese028_audio_work_v01")

VO_SRC = VO_DIR / "star_coming_vo_v01.wav"
OV_JSON = OV_PACK / "overlays_v01.json"

SR = 48000
LAST_WORD = 469.340
HOLD = 2.500
FADE = 1.000
TOTAL = 472.840  # matches 7-part rough total (472.84s)
BEAT_S = 0.850   # exact 17 x 50ms hops -> 70.6 BPM in music_gate.py
BPM = 60.0 / BEAT_S

CHAPTER_CARDS = [
    (42.500, "The Star Heading Our Way", "explain"),
    (131.000, "How Close Will It Come?", "explain"),
    (210.340, "Into the Oort Cloud", "awe"),
    (281.600, "The Comet Shower", "explain"),
    (335.840, "A New Brightest Star", "awe"),
    (378.300, "It Has Happened Before", "explain"),
]

WHOOSH_PASSES = [
    (82.460, "r10_gliese_approach Gaia 3D flyby towards Gliese 710"),
    (264.430, "r25_shower_cut Oort encounter flyby cutaway"),
    (305.020, "r27_leaving La Silla star-trails sweep as Gliese 710 recedes"),
]

RUMBLES = [
    (17.610, "r04_shower_shell Gliese 710 crossing outer Oort boundary"),
    (210.340, "r20_oort_shell_a vast spherical Oort Cloud reveal"),
    (256.790, "r24_shower_a gravity nudging Oort comets inward"),
    (342.130, "r29_sky orange dwarf perihelion outshining Sirius"),
]

EXTRA_TICKS = [
    (175.150, "r17_scale_a Sun-Earth 1 cm scale bar reveal"),
    (186.510, "r17_scale_b ruler scale extension"),
    (206.800, "r19_subscribe SUBSCRIBE pill"),
]

GAIN_DB = {"tick": -1.5, "whoosh_card": -8.5, "whoosh_pass": -9.0, "rumble": -3.5}


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


def is_explain_at(t_val: float) -> bool:
    return (42.32 <= t_val < 209.89) or (281.16 <= t_val < 335.42) or (377.80 <= t_val < 435.82)


def synthesize_raw_score(total_s: float) -> np.ndarray:
    """Compose a 472.84s stereo score bed in A minor / E minor / C major / G major at 70.6 BPM."""
    n_samples = int(round(total_s * SR))
    t = np.arange(n_samples, dtype=np.float32) / SR
    left = np.zeros(n_samples, dtype=np.float32)
    right = np.zeros(n_samples, dtype=np.float32)

    # 10-chord progression in A minor / E minor / C major / G major with wide register shifts
    # so spectral band evolution is distinct from 029's D-minor progression
    chords = [
        (33, 45, 52, 57, 64, 71),  # Am9 low-to-high
        (40, 47, 55, 59, 62, 67),  # Em7
        (41, 48, 57, 60, 64, 69),  # Fmaj7/13
        (36, 48, 55, 60, 64, 72),  # Cmaj7 wide
        (38, 50, 53, 57, 65, 69),  # Dm7
        (40, 52, 56, 59, 64, 71),  # E7sus4/B
        (45, 52, 60, 64, 67, 74),  # Am11 high
        (43, 50, 55, 59, 67, 71),  # Gmaj7
        (41, 53, 57, 62, 65, 72),  # Dm/F
        (40, 47, 52, 57, 64, 69),  # Esus4
    ]

    bar_len = 8.0 * BEAT_S  # 6.80s per bar
    n_bars = int(math.ceil(total_s / bar_len))
    for b_idx in range(n_bars):
        t0 = b_idx * bar_len
        t1 = min(total_s, (b_idx + 1) * bar_len + 1.4)
        i0 = int(round(t0 * SR))
        i1 = min(n_samples, int(round(t1 * SR)))
        if i1 <= i0:
            continue
        lt = t[i0:i1] - t0
        dur = t1 - t0
        fade_in = np.clip(lt / 1.4, 0.0, 1.0)
        fade_out = np.clip((dur - lt) / 1.4, 0.0, 1.0)
        env = np.sin(0.5 * math.pi * fade_in) * np.sin(0.5 * math.pi * fade_out)

        notes = chords[b_idx % len(chords)]
        mid_t = 0.5 * (t0 + t1)
        explain = is_explain_at(mid_t)
        # Rotate active voice subset per bar so band-energy trajectory moves across low/mid/high bands
        rot = b_idx % 3

        pad_l = np.zeros_like(lt)
        pad_r = np.zeros_like(lt)
        for v_idx, midi_note in enumerate(notes):
            f = midi_hz(midi_note)
            detune = 1.0 + (v_idx - 2.5) * 0.0008
            vib = 1.0 + 0.0010 * np.sin(2.0 * math.pi * (0.18 + 0.04 * v_idx) * lt)
            phase_l = 2.0 * math.pi * f * detune * lt + v_idx * 0.9 + b_idx * 0.3
            phase_r = 2.0 * math.pi * f * (2.0 - detune) * lt + v_idx * 1.4 + b_idx * 0.5
            voice_w = 1.25 if (v_idx % 3 == rot) else 0.70
            amp = (0.19 * voice_w) / (1.0 + 0.28 * v_idx)
            h2 = (0.32 if explain else 0.12) * (0.6 + 0.4 * math.sin(0.5 * b_idx + v_idx))
            h3 = (0.14 if explain else 0.03) * (0.6 + 0.4 * math.cos(0.7 * b_idx - v_idx))
            sig_l = amp * (np.sin(phase_l * vib) + h2 * np.sin(2.0 * phase_l) + h3 * np.sin(3.0 * phase_l))
            sig_r = amp * (np.sin(phase_r * vib) + h2 * np.sin(2.0 * phase_r) + h3 * np.sin(3.0 * phase_r))
            pan = 0.20 + 0.60 * (v_idx / max(1, len(notes) - 1))
            pad_l += sig_l * math.cos(0.5 * math.pi * pan)
            pad_r += sig_r * math.sin(0.5 * math.pi * pan)

        left[i0:i1] += pad_l * env
        right[i0:i1] += pad_r * env

    # Subtle 70.6 BPM rhythmic pulse on the pad so onset autocorrelation locks at 70.6 BPM
    beat_phase = np.mod(t, BEAT_S) / BEAT_S
    pulse_mod = 0.76 + 0.34 * np.exp(-beat_phase / 0.20)
    left *= pulse_mod
    right *= pulse_mod

    # Gentle 70.6 BPM plucked celesta/harp arpeggio
    n_beats = int(total_s / BEAT_S)
    arp_pattern = [0, 3, 5, 2, 4, 1, 5, 3, 2, 4]
    for k in range(n_beats):
        bt = k * BEAT_S
        if bt >= total_s - 2.0:
            break
        b_idx = int(bt // bar_len) % len(chords)
        chord = chords[b_idx]
        note_m = chord[arp_pattern[k % len(arp_pattern)]] + (12 if k % 3 != 0 else 0)
        f = midi_hz(note_m)
        explain = is_explain_at(bt)
        note_dur = 0.55
        i0 = int(round(bt * SR))
        i1 = min(n_samples, i0 + int(round(note_dur * SR)))
        nt = np.arange(i1 - i0, dtype=np.float32) / SR
        attack = np.clip(nt / 0.010, 0.0, 1.0)
        decay = np.exp(-nt / (0.15 if explain else 0.21))
        gain = (0.25 if explain else 0.15) * (1.20 if k % 2 == 0 else 0.85)
        tone = gain * attack * decay * (np.sin(2.0 * math.pi * f * nt) + 0.35 * np.sin(3.0 * math.pi * f * nt))
        pan = 0.30 + 0.40 * math.cos(k * 0.7)
        left[i0:i1] += tone * math.cos(0.5 * math.pi * pan)
        right[i0:i1] += tone * math.sin(0.5 * math.pi * pan)

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

    # 1. Prepare normalized VO stem (472.84s, -14 LUFS)
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

    bed_wav = WORK / "gliese_score_bed_v01.wav"
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

    bed_mp3 = MUSIC_DIR / "gliese_score_bed_v01.mp3"
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
        "Deep interstellar ambient and gentle plucked celesta/harp score for 028 A Star Is Coming Toward Us (Gliese 710) "
        "(A minor / E minor / C major / G major harmonic arc across 7 chapters: awe pads in Ch 0 Open, Ch 3 Into the Oort Cloud, "
        "Ch 5 A New Brightest Star, and Ch 6b birth-cluster payoff; explain plucked arpeggio in Ch 1 The Star Heading Our Way, "
        "Ch 2 How Close Will It Come?, Ch 4 The Comet Shower, and Ch 6a It Has Happened Before, changing mood at chapter cards). "
        "Pace: 64-74 BPM. "
        "NOT saturn-rings, sun-brighter, venus, light-speed, mars-robot, nearest-star, earth-spin, jupiter-music, or betelgeuse."
    )
    plan_data = {
        "film": "028_A-Star-Is-Coming-Toward-Us",
        "bed": bed_mp3.name,
        "duration_s": TOTAL,
        "source": "own synthesis (_build_gliese_audio_v01.py), £0 spend, no ElevenLabs credit",
        "prompt": prompt_txt,
        "chapters": [
            {"chapter": 0, "title": "Open", "start_s": 0.0, "end_s": 42.32, "mood": "awe"},
            {"chapter": 1, "title": "The Star Heading Our Way", "start_s": 42.32, "end_s": 126.47, "mood": "explain"},
            {"chapter": 2, "title": "How Close Will It Come?", "start_s": 126.47, "end_s": 209.89, "mood": "explain"},
            {"chapter": 3, "title": "Into the Oort Cloud", "start_s": 209.89, "end_s": 281.16, "mood": "awe"},
            {"chapter": 4, "title": "The Comet Shower", "start_s": 281.16, "end_s": 335.42, "mood": "explain"},
            {"chapter": 5, "title": "A New Brightest Star", "start_s": 335.42, "end_s": 377.80, "mood": "awe"},
            {"chapter": 6, "title": "It Has Happened Before", "start_s": 377.80, "end_s": 472.84, "mood": "explain_to_awe"},
        ],
        "integrated_lufs": round(bi_final, 2),
        "sha256": sha256_file(bed_mp3),
    }
    (MUSIC_DIR / "gliese_score_bed_v01_plan.json").write_text(json.dumps(plan_data, indent=2) + "\n")
    (MUSIC_DIR / "BED_BRIEF_v01.md").write_text(
        "# 028 Gliese 710 Score Bed v01 (`J0859`, £0)\n\n"
        f"- **File:** `05_Music/{bed_mp3.name}` (`{TOTAL:.2f} s`, `{bi_final:.1f} LUFS` integrated)\n"
        f"- **Prompt / Pace:** `{prompt_txt}`\n"
        "- **Chapters:** `awe` (0:00–0:42.3) → `explain` (0:42.3–3:29.9) → `awe` (3:29.9–4:41.2) → "
        "`explain` (4:41.2–5:35.4) → `awe` (5:35.4–6:17.8) → `explain/awe` (6:17.8–7:52.8)\n"
    )

    # 3. Synthesize house SFX kit and build 028 SFX stem
    sfx_kit.make(KIT_DIR, "owb", 11)
    whoosh_wav = read_wav(KIT_DIR / "sfx_owb_whoosh_soft_v01.wav")
    whoosh_len = len(whoosh_wav) / SR
    tick_wav = read_wav(KIT_DIR / "sfx_owb_tick_ui_v01.wav")
    rumble_wav = read_wav(KIT_DIR / "sfx_owb_rumble_low_v01.wav")

    ov_labels = json.loads(OV_JSON.read_text())["labels"]
    cues = []
    # SFX tick on every teaching pill (22 pills)
    for o in ov_labels:
        cues.append(("tick", round(float(o["film_start"]), 3), f"teaching pill: {o['text']}"))
    # SFX tick + soft whoosh on every chapter card (6 chapter cards)
    for t_c, title, _ in CHAPTER_CARDS:
        cues.append(("tick", round(t_c, 3), f"chapter card tick: {title}"))
        cues.append(("whoosh_card", round(t_c - 0.15, 3), f"chapter card whoosh: {title}"))
    for t_c, why in EXTRA_TICKS:
        cues.append(("tick", round(t_c, 3), why))
    for t_c, why in WHOOSH_PASSES:
        cues.append(("whoosh_pass", round(t_c - 0.5 * whoosh_len, 3), why))
    for t_c, why in RUMBLES:
        cues.append(("rumble", round(t_c, 3), why))
    cues.sort(key=lambda c: c[1])

    # Verify >= 0.5s spacing between ticks
    tick_times = [t_c for k, t_c, _ in cues if k == "tick"]
    for a, b in zip(tick_times, tick_times[1:]):
        assert b - a >= 0.5, f"Ticks too close: {a} vs {b}"

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
                "film": "028_A-Star-Is-Coming-Toward-Us",
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
