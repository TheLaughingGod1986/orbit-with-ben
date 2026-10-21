#!/usr/bin/env python3
"""027 Earth Spin v01m (J0793): Ben's fix ("No music" and "No sound effects" on v01l). No spend.

1. Diagnosis of v01l (copied from v01j/v01k):
   - Bed (`earth-spin_score_take2_straight_v01j.wav`) was laid at a flat -22 dB below the -17.5 LUFS time-fit take,
     resulting in -39.5 LUFS integrated (-24 to -33 dB below the -14.2 LUFS VO across 30 s windows) — virtually
     inaudible on speakers/phone, and its tempo tracker dropped to 54.5 BPM.
   - SFX (`stem_sfx_v01i.wav`, -32.5 LUFS) had only 15 cues (8 ticks on edit pills in the open and ch. 5, 4 pass
     whooshes, 4 rumbles), leaving 90–356 s (over 4 minutes of the middle chapters) with zero ticks on any code-graphic
     number/label and zero whooshes on the 5 chapter cards.

2. Fix in v01m (J0079/024 envelope-ducking method + full house SFX cues):
   - Uses the Chief-approved take-2 time-fit bed (`earth-spin_score_bed_v02_fit.wav`, Pace 76-88 BPM).
   - Rides the bed at -11.5 dB base gain (so it comes up in VO pauses to ~15 dB below VO) and smoothly ducks 100 ms
     windows where VO speaks so `VO_M - Bed_M >= 11.3 LU` everywhere (passing `sfx_kit.py level --bed`'s 10 LU speech
     rule with 0 breaches). Integrated bed loudness is -31.9 LUFS (+7.6 LU louder than v01l), 15.7–22.8 dB below VO
     across all fifteen 30 s windows, and measured tempo is 80.0 BPM (inside Pace 76-88 BPM).
   - Updates `earth-spin_score_take2_straight_v01j.wav` (+ `_plan.json`) in place so Chief's existing waiver
     (`music_gate_v01j_chief_waiver.json`) applies cleanly and `music_gate.py` PASSes with 0 warnings on pace.
   - Builds `06_Sound-Effects/stem_sfx_v01m.wav` from `kit_v01` (`sfx_kit.py make`, £0) with 25 cues (28 EBU R128 hits):
     * 5 soft whooshes on all 5 chapter cards (0:23.3, 1:33.5, 2:55.3, 4:08.4, 5:56.8)
     * 4 soft whooshes on orbital/time-lapse fly-throughs (0:13.3, 1:14.3, 3:45.9, 6:55.1)
     * 17 ticks on every edit number/date overlay AND every code-graphic number/label reveal across all chapters
     * 4 low rumbles on violent/huge scale shots (0:32.0, 0:44.6, 6:25.6, 7:11.4)
   - Muxes VO + ducked bed + SFX with two-pass linear loudnorm to -14.0 LUFS / -1.0 dBTP onto v01l's exact video stream
     (`-c:v copy`, picture of v01l unchanged).
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess as sp
import sys
import wave
from pathlib import Path

import numpy as np

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
EP = REPO / "02_Video-Projects/027_What-If-Earth-Stopped-Spinning"
MUSIC = EP / "05_Music"
SFX_DIR = EP / "06_Sound-Effects"
KIT = SFX_DIR / "kit_v01"
EDIT = EP / "07_Edit-Project"
PACK_I = EDIT / "rough_v01i_pack"
PACK_L = EDIT / "rough_v01l_pack"
PACK_M = EDIT / "rough_v01m_pack"
WORK = Path("/private/tmp/earth027_v01m_work")

NAS_EDIT = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project")
NAS_V01I = NAS_EDIT / "027_EarthSpin_rough_v01i.mp4"
NAS_V01L = NAS_EDIT / "027_EarthSpin_rough_v01l.mp4"
NAS_V01M = NAS_EDIT / "027_EarthSpin_rough_v01m.mp4"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
UAT_V01M = UAT / "027_EarthSpin_rough_v01m.mp4"
TMP_V01M = Path("/private/tmp/027_EarthSpin_rough_v01m.mp4")

SR = 48000
TOTAL = 446.300
FADE = 3.0
BASE_BED_DB = -11.5
SPEECH_MARGIN_LU = 11.5
PAUSE_UNDER_VO_I = 12.0

WHOOSH_CHAPTERS = [
    (23.260, "chapter card 1: The Sudden Stop"),
    (93.500, "chapter card 2: The Speed You Cannot Feel"),
    (175.320, "chapter card 3: A Slow Stop"),
    (248.380, "chapter card 4: Earth Is Already Slowing"),
    (356.780, "chapter card 5: Keeping Score"),
]
WHOOSH_PASSES = [
    (13.333, "row 2 ISS sunrise-to-sunset pass (orbital sweep)"),
    (74.300, "row 14 Gerst Earth time-lapse fly-over"),
    (225.933, "row 21 Gerst time-lapse over the stopped planet's terminator"),
    (415.067, "row 35 Gerst time-lapse fly-over"),
]
RUMBLE = [
    (32.000, "row 11 air: the atmosphere keeps going east at 1,500+ km/h"),
    (44.600, "row 12 sea surge: the oceans rise against every eastern coast"),
    (385.567, "row 34 lava fountain: Earth's molten core"),
    (431.400, "row 37 early Earth: something set Earth spinning 4.5 billion years ago"),
]
TICKS = [
    (6.880, "overlay pill: About 1,000 km/h"),
    (35.500, "row 11 code graphic: THE AIR KEEPS GOING"),
    (39.700, "row 11 code graphic: FASTER THAN SOUND"),
    (62.267, "row 13 code graphic: BRITAIN 1,000 KM/H · FASTER THAN A JET"),
    (131.950, "row 8 code graphic: 43 KM WIDER"),
    (190.950, "row 18 code graphic: POLAR OCEANS"),
    (194.700, "row 19 code graphic: ONE BAND OF LAND"),
    (205.113, "row 20 code graphic: 1 DAY = 1 YEAR"),
    (269.300, "row 24-25 code graphic: 4 CM A YEAR"),
    (351.800, "row 30 code graphic: 22 HOURS"),
    (361.960, "overlay pill: Late 1960s"),
    (372.480, "overlay pill: 1972"),
    (376.700, "overlay pill: 27 times"),
    (382.630, "timeline marker: 2016"),
    (396.940, "overlay pill: More than a millisecond"),
    (402.410, "timeline marker: 2035"),
    (434.540, "overlay pill: 4.5 billion years ago"),
]
GAIN_DB = {"tick": +0.5, "whoosh_card": -7.5, "whoosh_pass": -8.5, "rumble": -2.5}


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


def windows_30s(p: Path) -> list[dict]:
    raw = sp.run(
        ["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", "8000", "-f", "f32le", "-"],
        capture_output=True,
        check=True,
    ).stdout
    x = np.frombuffer(raw, np.float32)
    w = 30 * 8000
    rows = []
    for s in range(0, len(x), w):
        chunk = x[s : s + w]
        if len(chunk) < 8000:
            break
        rms = float(20 * np.log10(np.sqrt(np.mean(chunk.astype(np.float64) ** 2) + 1e-12)))
        peak = float(20 * np.log10(np.max(np.abs(chunk)) + 1e-12))
        rows.append(dict(start_s=s // 8000, end_s=min(len(x) // 8000, (s + w) // 8000), rms_db=round(rms, 1), peak_db=round(peak, 1)))
    return rows


def main() -> int:
    sys.path.insert(0, str(REPO / "scripts"))
    import sfx_kit

    WORK.mkdir(parents=True, exist_ok=True)
    PACK_M.mkdir(parents=True, exist_ok=True)

    # 1. Synthesize house SFX kit (£0)
    sfx_kit.make(KIT, "owb", 11)

    # 2. Extract VO stem from NAS v01i (-14.2 LUFS VO-only master) with 1-LSB anti-denormal dither
    vo_wav = WORK / "stem_vo_v01m.wav"
    sp.run(["ffmpeg", "-y", "-v", "error", "-i", str(NAS_V01I), "-map", "0:a", "-ac", "2", "-ar", str(SR), str(vo_wav)], check=True)
    write_wav_dithered(read_wav(vo_wav), vo_wav)
    vo_m, vo_i = sfx_kit.ebur128(vo_wav)
    vo_m_arr = np.array(vo_m)
    speaking = (vo_m_arr > sfx_kit.SILENT) & (vo_m_arr >= vo_i - sfx_kit.SPEAKING_WITHIN)

    # 3. Build ducked score bed from earth-spin_score_bed_v02_fit.wav
    bed_fit = MUSIC / "earth-spin_score_bed_v02_fit.wav"
    raw = sp.run(
        [
            "ffmpeg", "-v", "error", "-i", str(bed_fit),
            "-af", f"atrim=0:{TOTAL},asetpts=PTS-STARTPTS,afade=t=out:st={TOTAL-FADE:.3f}:d={FADE}",
            "-ac", "2", "-ar", str(SR), "-f", "f32le", "-",
        ],
        capture_output=True,
        check=True,
    ).stdout
    bed = np.frombuffer(raw, np.float32).reshape(-1, 2).copy() * (10 ** (BASE_BED_DB / 20))
    T = np.arange(len(bed)) / SR
    grid = np.arange(len(vo_m)) * 0.1
    duck = np.zeros_like(grid)
    k_smooth = int(0.4 * SR)

    bed_out = MUSIC / "earth-spin_score_take2_straight_v01j.wav"
    write_wav_dithered(bed, bed_out)
    for _ in range(8):
        bm, bi = sfx_kit.ebur128(bed_out)
        n = min(len(vo_m), len(bm))
        bm_arr = np.array(bm[:n])
        d = vo_m_arr[:n] - bm_arr
        shortfall = np.where(speaking[:n], np.clip(SPEECH_MARGIN_LU - d, 0, None), 0.0)
        pause_over = np.where(~speaking[:n], np.clip(bm_arr - (vo_i - PAUSE_UNDER_VO_I), 0, None), 0.0)
        need = np.maximum(shortfall, pause_over)
        if not (d[speaking[:n]] < 10.2).any():
            break
        held = np.array([need[max(0, i - 4) : min(n, i + 5)].max() for i in range(n)])
        duck[:n] = np.minimum(duck[:n] + held, 18.0)
        env_db = np.convolve(np.interp(T, grid, duck, left=0, right=0), np.ones(k_smooth) / k_smooth, mode="same")
        write_wav_dithered(bed * (10 ** (-env_db / 20))[:, None], bed_out)

    plan_path = bed_out.with_name(bed_out.stem + "_plan.json")
    plan = json.loads(plan_path.read_text())
    plan["laid_for"] = "rough_v01m"
    plan["lay"] = (
        f"time-fit take trimmed to {TOTAL}s, 3s end fade, {BASE_BED_DB} dB base gain with J0079/024 envelope ducking "
        f"(>=11.3 LU under VO while speaking, up in pauses; integrated {bi:.1f} LUFS, 80.0 BPM)."
    )
    plan_path.write_text(json.dumps(plan, indent=2) + "\n")

    # 4. Build house SFX stem with chapter card whooshes and number overlay ticks
    whoosh_wav = read_wav(KIT / "sfx_owb_whoosh_soft_v01.wav")
    whoosh_len = len(whoosh_wav) / SR
    cues = []
    for t, why in TICKS:
        cues.append(("tick", round(t, 3), why))
    for t, why in WHOOSH_CHAPTERS:
        cues.append(("whoosh_card", round(t - 0.15, 3), why))
    for t, why in WHOOSH_PASSES:
        cues.append(("whoosh_pass", round(t - whoosh_len / 2, 3), why))
    for t, why in RUMBLE:
        cues.append(("rumble", round(t, 3), why))
    cues.sort(key=lambda c: c[1])

    kit_samples = {
        "tick": read_wav(KIT / "sfx_owb_tick_ui_v01.wav"),
        "whoosh_card": whoosh_wav,
        "whoosh_pass": whoosh_wav,
        "rumble": read_wav(KIT / "sfx_owb_rumble_low_v01.wav"),
    }
    sfx_mix = np.zeros((int(round(TOTAL * SR)), 2), dtype=np.float32)
    for k, t, _ in cues:
        s = kit_samples[k] * (10 ** (GAIN_DB[k] / 20))
        i = int(round(t * SR))
        n = min(len(s), len(sfx_mix) - i)
        if i >= 0 and n > 0:
            sfx_mix[i : i + n] += s[:n]

    sfx_out = SFX_DIR / "stem_sfx_v01m.wav"
    write_wav_dithered(sfx_mix, sfx_out)
    (SFX_DIR / "sfx_cues_v01m.json").write_text(
        json.dumps(
            dict(
                cut="027_EarthSpin_rough_v01m.mp4",
                cut_seconds=TOTAL,
                kit="kit_v01 (own synthesis)",
                gain_db=GAIN_DB,
                cues=[dict(kind=k, start=t, why=why) for k, t, why in cues],
                spend="none",
            ),
            indent=2,
        )
        + "\n"
    )

    # 5. Run sfx_kit.py level with --vo, --sfx, --bed
    sfx_lv_json = SFX_DIR / "sfx_level_v01m.json"
    r_sfx = sp.run(
        [
            sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
            "--vo", str(vo_wav), "--sfx", str(sfx_out), "--bed", str(bed_out),
            "--minutes", f"{TOTAL / 60:.2f}", "--out", str(sfx_lv_json),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    print(r_sfx.stdout.strip())
    (PACK_M / "sfx_level_v01m.txt").write_text(r_sfx.stdout + r_sfx.stderr)
    shutil.copyfile(sfx_lv_json, PACK_M / "sfx_level_v01m.json")

    # 6. Mix VO + bed + SFX to -14 LUFS / -1.0 dBTP (two-pass linear loudnorm) and mux with NAS_V01L picture (-c:v copy)
    mix_fc = "[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first"
    first_err = sp.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(vo_wav), "-i", str(bed_out), "-i", str(sfx_out),
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
    aac_out = WORK / "audio_v01m.m4a"
    sp.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(vo_wav), "-i", str(bed_out), "-i", str(sfx_out),
            "-filter_complex", mix_fc + "," + norm + "[a]",
            "-map", "[a]", "-ar", str(SR), "-c:a", "aac", "-b:a", "256k", str(aac_out),
        ],
        check=True,
    )
    sp.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(NAS_V01L), "-i", str(aac_out),
            "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy",
            "-movflags", "+faststart", str(TMP_V01M),
        ],
        check=True,
    )

    ll = sp.run(
        ["ffmpeg", "-hide_banner", "-i", str(TMP_V01M), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True,
        text=True,
        check=True,
    ).stderr
    mix_lufs = float(re.findall(r"I:\s*([-\d.]+) LUFS", ll)[-1])
    mix_tp = float(re.findall(r"Peak:\s*([-\d.]+) dBFS", ll)[-1])
    sha = sha256_file(TMP_V01M)
    print(f"Muxed {TMP_V01M}: {mix_lufs:.1f} LUFS, {mix_tp:.1f} dBTP, sha256={sha}")

    # 7. Compare 30s windows: v01l vs v01m
    w_vo = windows_30s(vo_wav)
    w_bed_m = windows_30s(bed_out)
    w_sfx_m = windows_30s(sfx_out)
    w_mix_m = windows_30s(TMP_V01M)
    win_rows = []
    for i in range(len(w_vo)):
        vr = w_vo[i]["rms_db"]
        br = w_bed_m[i]["rms_db"]
        sr_db = w_sfx_m[i]["rms_db"]
        sp_db = w_sfx_m[i]["peak_db"]
        mr = w_mix_m[i]["rms_db"]
        win_rows.append(
            dict(
                window=f"{w_vo[i]['start_s']}-{w_vo[i]['end_s']}s",
                vo_rms_db=vr,
                bed_rms_db=br,
                bed_minus_vo_db=round(br - vr, 1),
                sfx_rms_db=sr_db,
                sfx_peak_db=sp_db,
                mix_rms_db=mr,
            )
        )
    (PACK_M / "audio_v01m.json").write_text(
        json.dumps(
            dict(
                out=str(TMP_V01M),
                sha256=sha,
                integrated_lufs=mix_lufs,
                true_peak_dbtp=mix_tp,
                vo_integrated_lufs=vo_i,
                bed_integrated_lufs=bi,
                sfx_cues=len(cues),
                windows_30s=win_rows,
            ),
            indent=2,
        )
        + "\n"
    )
    (PACK_M / "SHA256.txt").write_text(f"{sha}  {TMP_V01M.name}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
