#!/usr/bin/env python3
"""
Broadcast v19 — cinematic documentary mix (Netflix / BBC Earth feel).

Priority: VO → music → space ambience → Orbit SFX → chapter transitions.

Philosophy:
  - Calm wonder, not trailer boom
  - Music audible but always subordinate (~20–30% of VO when speaking)
  - Soft invisible sidechain duck (no pumping)
  - Intentional hush windows at major questions
  - Restrained Orbit robotics (only significant moments)
  - Branded understated chapter whoosh + shimmer
  - Emotional arc across sections
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDIT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "09_Final-Export"
WORK = EDIT / "_mix_work_v19"
WORK.mkdir(parents=True, exist_ok=True)

VIDEO_PIC = OUT_DIR / "aliens_broadcast_v18_retention_pic.mp4"
VIDEO_FALLBACK = OUT_DIR / "aliens_broadcast_v18_retention.mp4"
VO_SRC = ROOT / "02_Voiceover/05_Master/aliens_voiceover_master_storyteller_v04.wav"
EDL_PATH = EDIT / "SECTION_EDL_v18_retention.json"
MARKERS_FALLBACK = EDIT / "VO_MARKERS_v08.json"

MUSIC_OUT = WORK / "score_bed.wav"
SFX_OUT = WORK / "sfx_bed.wav"
ORBIT_SFX_OUT = WORK / "orbit_robotics.wav"
AMB_OUT = WORK / "space_ambience.wav"
VO_SWEET = WORK / "vo_sweetened.wav"
MIX_OUT = WORK / "final_mix.wav"
VIDEO_OUT = OUT_DIR / "aliens_broadcast_v19_cinematic_mix.mp4"
PROOF_OUT = OUT_DIR / "aliens_v19_PROOF_cinematic_mix_90s.mp4"
# Also refresh the “current” retention export audio
VIDEO_LATEST = OUT_DIR / "aliens_broadcast_v18_retention.mp4"

# Relative gains — music ~20–30% of VO feel under narration; swells in gaps
MUSIC_UNDER_VO = 1.35
MUSIC_IN_GAPS = 2.00
MUSIC_CHAPTER = 2.10
MUSIC_CTA = 1.80
MUSIC_HUSH = 0.18          # intentional near-silence
AMBIENCE_LEVEL = 0.18      # ~10–15% of VO feel
SFX_WHOOSH = 0.12
SFX_SHIMMER = 0.16
ORBIT_SERVO = 0.05
ORBIT_BLIP = 0.04
VO_LEVEL = 1.0

# Key hush windows (start, end) — drama / scale / Fermi / silence-of-sky
HUSH_WINDOWS: list[tuple[float, float]] = [
    (31.2, 33.0),     # cold-open: pause before the big question lands
    (178.8, 181.2),   # Fermi: “…where are they?”
    (247.8, 250.2),   # Great Filter: serious beat
    (576.8, 580.0),   # Conclusion: “silence of the sky”
    (621.0, 623.2),   # Pre-CTA breath before invite
]


def ffprobe_dur(path: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        capture_output=True, text=True, check=True,
    )
    return float(r.stdout.strip())


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def load_broadcast():
    spec = importlib.util.spec_from_file_location("b", EDIT / "_build_broadcast_noloop_v02.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SECTION_MOOD: dict[str, float] = {
    "01_cold-open": 0.92,
    "02_galaxy-scale": 1.08,
    "03_exoplanets": 1.12,
    "04_fermi-paradox": 0.78,
    "05_great-filter": 0.72,
    "06_explanations": 0.88,
    "07_detection": 1.00,
    "08_first-contact": 1.10,
    "09_conclusion": 1.05,
    "cta": 1.15,
}


def gain_at_time(t: float, markers: list[dict]) -> float:
    """Resolve music gain at t — hush wins, then chapter swell, then section mood."""
    for a, b in HUSH_WINDOWS:
        if a <= t < b:
            return MUSIC_HUSH
    for m in markers:
        st = float(m["start_s"])
        en = st + float(m["duration_s"])
        if not (st <= t < en):
            continue
        kind = m["kind"]
        sec = m.get("section") or ""
        mood = SECTION_MOOD.get(sec, 1.0)
        if kind == "lead":
            return MUSIC_CHAPTER * 0.85
        if kind == "chapter_gap":
            return MUSIC_IN_GAPS
        if kind == "cta":
            return MUSIC_CTA
        if kind == "vo":
            g = MUSIC_UNDER_VO * mood
            # Gentle pre-chapter lift on long sections
            if en - st > 40 and t >= en - 1.4:
                g *= 1.12
            return g
    return MUSIC_UNDER_VO


def build_gain_segments(duration: float, markers: list[dict]) -> list[tuple[float, float, float]]:
    """Non-overlapping (start, end, gain) covering 0…duration."""
    pts = {0.0, duration}
    for m in markers:
        st = float(m["start_s"])
        en = st + float(m["duration_s"])
        pts.add(max(0.0, min(duration, st)))
        pts.add(max(0.0, min(duration, en)))
        if m["kind"] == "vo" and en - st > 40:
            pts.add(max(0.0, min(duration, en - 1.4)))
    for a, b in HUSH_WINDOWS:
        pts.add(max(0.0, min(duration, a)))
        pts.add(max(0.0, min(duration, b)))
    ordered = sorted(pts)
    segs: list[tuple[float, float, float]] = []
    for i in range(len(ordered) - 1):
        a, b = ordered[i], ordered[i + 1]
        if b - a < 0.02:
            continue
        g = round(gain_at_time((a + b) * 0.5, markers), 4)
        if segs and abs(segs[-1][2] - g) < 0.001:
            segs[-1] = (segs[-1][0], b, g)
        else:
            segs.append((a, b, g))
    return segs


def apply_gain_envelope(raw: Path, duration: float, segments: list[tuple[float, float, float]], out: Path) -> None:
    """Apply reliable per-segment gains via atrim + concat (no nested if())."""
    parts: list[str] = []
    labels: list[str] = []
    for i, (a, b, g) in enumerate(segments):
        # Crossfade-ish soft edges via short afade on longer segments
        fade = min(0.25, (b - a) * 0.2)
        parts.append(
            f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,"
            f"volume={g:.4f},"
            f"afade=t=in:st=0:d={fade:.3f},"
            f"afade=t=out:st={max(0.0, b - a - fade):.3f}:d={fade:.3f}[s{i}]"
        )
        labels.append(f"[s{i}]")
    fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(segments)}:v=0:a=1[out]"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(raw),
        "-filter_complex", fc,
        "-map", "[out]",
        "-c:a", "pcm_s16le",
        "-t", f"{duration:.3f}",
        str(out),
    ])


def build_score(duration: float, markers: list[dict]) -> Path:
    """Evolving ambient orchestral pad — curious → expansive → serious → hopeful."""
    raw = WORK / "score_raw.wav"
    segments = build_gain_segments(duration, markers)

    # Layered pad at unity internal level — envelope applied after
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            f"sine=frequency=55.00:sample_rate=48000:duration={duration:.3f}[drone];"
            f"sine=frequency=82.41:sample_rate=48000:duration={duration:.3f}[fifth];"
            f"sine=frequency=110.00:sample_rate=48000:duration={duration:.3f}[oct];"
            f"sine=frequency=164.81:sample_rate=48000:duration={duration:.3f}[third];"
            f"sine=frequency=220.00:sample_rate=48000:duration={duration:.3f}[airtone];"
            f"sine=frequency=329.63:sample_rate=48000:duration={duration:.3f}[softstr];"
            f"sine=frequency=523.25:sample_rate=48000:duration={duration:.3f}[shim];"
            f"anoisesrc=color=pink:sample_rate=48000:duration={duration:.3f}[pn];"
            f"[pn]highpass=f=120,lowpass=f=900,volume=0.055,aformat=channel_layouts=stereo[air];"
            f"[drone]aformat=channel_layouts=stereo,volume=0.34[d1];"
            f"[fifth]aformat=channel_layouts=stereo,volume=0.20[f1];"
            f"[oct]aformat=channel_layouts=stereo,volume=0.11[o1];"
            f"[third]aformat=channel_layouts=stereo,volume=0.07,"
            f"tremolo=f=0.10:d=0.30[t1];"
            f"[airtone]aformat=channel_layouts=stereo,volume=0.045,"
            f"tremolo=f=0.11:d=0.35[a1];"
            f"[softstr]aformat=channel_layouts=stereo,volume=0.035,"
            f"tremolo=f=0.10:d=0.45,afade=t=in:st=0:d=8[s1];"
            f"[shim]aformat=channel_layouts=stereo,volume=0.022,"
            f"tremolo=f=0.12:d=0.55,afade=t=in:st=2:d=6[sh1];"
            f"[d1][f1][o1][t1][a1][s1][sh1][air]amix=inputs=8:normalize=0:dropout_transition=0,"
            f"highpass=f=40,lowpass=f=4200,"
            f"equalizer=f=1800:t=q:w=1.2:g=-4.5,"
            f"equalizer=f=2800:t=q:w=1.0:g=-3.0,"
            f"equalizer=f=120:t=q:w=0.8:g=1.5,"
            f"afade=t=in:st=0:d=1.8,"
            f"afade=t=out:st={max(0.0, duration - 4.5):.3f}:d=4.5"
        ),
        "-c:a", "pcm_s16le", str(raw),
    ])
    apply_gain_envelope(raw, duration, segments, MUSIC_OUT)
    return MUSIC_OUT


def build_ambience_gain_segments(duration: float, markers: list[dict]) -> list[tuple[float, float, float]]:
    pts = {0.0, duration}
    for m in markers:
        st = float(m["start_s"])
        en = st + float(m["duration_s"])
        pts.add(max(0.0, min(duration, st)))
        pts.add(max(0.0, min(duration, en)))
    for a, b in HUSH_WINDOWS:
        pts.add(max(0.0, min(duration, a)))
        pts.add(max(0.0, min(duration, b)))
    ordered = sorted(pts)
    segs: list[tuple[float, float, float]] = []

    def amb_gain(t: float) -> float:
        for a, b in HUSH_WINDOWS:
            if a <= t < b:
                return AMBIENCE_LEVEL * 0.22
        for m in markers:
            if m["kind"] != "chapter_gap":
                continue
            st = float(m["start_s"])
            en = st + float(m["duration_s"])
            if st <= t < en:
                return AMBIENCE_LEVEL * 0.65
        return AMBIENCE_LEVEL

    for i in range(len(ordered) - 1):
        a, b = ordered[i], ordered[i + 1]
        if b - a < 0.02:
            continue
        g = round(amb_gain((a + b) * 0.5), 4)
        if segs and abs(segs[-1][2] - g) < 0.001:
            segs[-1] = (segs[-1][0], b, g)
        else:
            segs.append((a, b, g))
    return segs


def _whoosh(path: Path, dur: float = 1.05) -> None:
    """Soft cinematic whoosh — branded chapter signature."""
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            f"anoisesrc=color=white:sample_rate=48000:duration={dur},"
            f"highpass=f=280,lowpass=f=2800,"
            f"afade=t=in:st=0:d=0.18,afade=t=out:st={dur - 0.55:.3f}:d=0.55,"
            f"volume=0.9,aformat=channel_layouts=stereo"
        ),
        "-c:a", "pcm_s16le", str(path),
    ])


def _brand_shimmer(path: Path) -> None:
    """Light branded synth shimmer (~1.2s) — elegant, understated."""
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            "sine=frequency=523.25:sample_rate=48000:duration=1.25[a];"
            "sine=frequency=659.25:sample_rate=48000:duration=1.25[b];"
            "sine=frequency=783.99:sample_rate=48000:duration=1.25[c];"
            "[a][b][c]amix=inputs=3:normalize=0,"
            "afade=t=in:st=0:d=0.06,afade=t=out:st=0.28:d=0.95,"
            "highpass=f=300,lowpass=f=5000,volume=0.42,aformat=channel_layouts=stereo"
        ),
        "-c:a", "pcm_s16le", str(path),
    ])


def _orbit_servo(path: Path) -> None:
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            "sine=frequency=380:sample_rate=48000:duration=0.32[a];"
            "sine=frequency=610:sample_rate=48000:duration=0.32[b];"
            "anoisesrc=color=pink:sample_rate=48000:duration=0.32[n];"
            "[n]bandpass=f=850:width_type=h:width=600,volume=0.28[n1];"
            "[a]aformat=channel_layouts=stereo,afade=t=in:st=0:d=0.02,"
            "afade=t=out:st=0.10:d=0.22,volume=0.38[a1];"
            "[b]aformat=channel_layouts=stereo,afade=t=in:st=0.03:d=0.03,"
            "afade=t=out:st=0.12:d=0.20,volume=0.22[b1];"
            "[n1]aformat=channel_layouts=stereo,afade=t=in:st=0:d=0.03,"
            "afade=t=out:st=0.15:d=0.17[n2];"
            "[a1][b1][n2]amix=inputs=3:normalize=0,"
            "highpass=f=200,lowpass=f=2800,volume=1.0"
        ),
        "-c:a", "pcm_s16le", str(path),
    ])


def _orbit_blip(path: Path) -> None:
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            "sine=frequency=760:sample_rate=48000:duration=0.14[a];"
            "sine=frequency=1140:sample_rate=48000:duration=0.14[b];"
            "[a][b]amix=inputs=2:normalize=0,"
            "afade=t=in:st=0:d=0.004,afade=t=out:st=0.03:d=0.11,"
            "highpass=f=450,volume=0.55,aformat=channel_layouts=stereo"
        ),
        "-c:a", "pcm_s16le", str(path),
    ])


def build_ambience(duration: float, markers: list[dict]) -> Path:
    """Subtle space bed — ducked further in hush windows."""
    raw = WORK / "ambience_raw.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            f"anoisesrc=color=brown:sample_rate=48000:duration={duration:.3f}[n];"
            f"sine=frequency=42:sample_rate=48000:duration={duration:.3f}[d];"
            f"sine=frequency=73:sample_rate=48000:duration={duration:.3f}[h];"
            f"[n]highpass=f=35,lowpass=f=380,volume=0.58,aformat=channel_layouts=stereo[n1];"
            f"[d]aformat=channel_layouts=stereo,volume=0.14,tremolo=f=0.10:d=0.28[d1];"
            f"[h]aformat=channel_layouts=stereo,volume=0.05,tremolo=f=0.11:d=0.35[h1];"
            f"[n1][d1][h1]amix=inputs=3:normalize=0,"
            f"afade=t=in:st=0:d=2.5,"
            f"afade=t=out:st={max(0.0, duration - 4.0):.3f}:d=4.0"
        ),
        "-c:a", "pcm_s16le", str(raw),
    ])
    apply_gain_envelope(raw, duration, build_ambience_gain_segments(duration, markers), AMB_OUT)
    return AMB_OUT


def orbit_cue_times(edl_data: dict, bmod) -> list[tuple[float, str]]:
    """Sparse Orbit cues — only significant reactions / section entries."""
    shots = []
    for s in edl_data["shots"]:
        shots.append({
            "kind": s["kind"],
            "path": Path(s["clip"]),
            "start_s": float(s["start_s"]),
            "duration_s": float(s["duration_s"]),
            "section": s.get("section"),
            "orbit": s.get("orbit"),
        })
    windows = bmod._build_emotion_windows(edl_data["markers"], shots)

    significant = {"surprise", "scared", "wonder", "excited", "thinking", "invite"}
    cues: list[tuple[float, str]] = []
    last_t = -99.0
    MIN_GAP = 11.0  # restraint — most personality is visual

    for i, w in enumerate(windows):
        t = float(w["start"])
        emo = w.get("emotion") or ""
        # Always allow a soft cue after chapter cards (re-enter frame feel)
        after_chapter = any(
            abs(t - float(m["start_s"]) - float(m["duration_s"])) < 1.2
            for m in edl_data["markers"] if m["kind"] == "chapter_gap"
        )
        if emo not in significant and not after_chapter:
            if i % 7 != 0:
                continue
        if t - last_t < MIN_GAP:
            continue
        kind = "blip" if emo in ("surprise", "scared", "wonder", "excited") else "servo"
        cues.append((t + 0.08, kind))
        last_t = t
    return cues


def build_orbit_robotics(duration: float, cues: list[tuple[float, str]]) -> Path:
    servo = WORK / "sfx_orbit_servo.wav"
    blip = WORK / "sfx_orbit_blip.wav"
    _orbit_servo(servo)
    _orbit_blip(blip)

    if not cues:
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={duration:.3f}",
            "-c:a", "pcm_s16le", "-t", f"{duration:.3f}", str(ORBIT_SFX_OUT),
        ])
        return ORBIT_SFX_OUT

    inputs: list[str] = [
        "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={duration:.3f}",
    ]
    fc_parts: list[str] = []
    for i, (t, kind) in enumerate(cues, start=1):
        path = servo if kind == "servo" else blip
        gain = ORBIT_SERVO if kind == "servo" else ORBIT_BLIP
        inputs += ["-i", str(path)]
        ms = int(round(max(0.0, t) * 1000))
        fc_parts.append(f"[{i}:a]volume={gain:.3f},adelay={ms}|{ms}[e{i}]")

    n = 1 + len(cues)
    labels = "[0:a]" + "".join(f"[e{i}]" for i in range(1, len(cues) + 1))
    fc = ";".join(fc_parts) + ";" if fc_parts else ""
    fc += f"{labels}amix=inputs={n}:normalize=0:dropout_transition=0[out]"

    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        *inputs,
        "-filter_complex", fc,
        "-map", "[out]", "-c:a", "pcm_s16le",
        "-t", f"{duration:.3f}",
        str(ORBIT_SFX_OUT),
    ])
    return ORBIT_SFX_OUT


def build_sfx(duration: float, markers: list[dict]) -> Path:
    whoosh = WORK / "sfx_whoosh.wav"
    shimmer = WORK / "sfx_shimmer.wav"
    _whoosh(whoosh)
    _brand_shimmer(shimmer)

    events: list[tuple[float, Path, float]] = []
    for m in markers:
        st = float(m["start_s"])
        kind = m["kind"]
        if kind == "lead":
            events.append((max(0.05, st + 0.05), shimmer, SFX_SHIMMER * 0.85))
        elif kind == "chapter_gap":
            # Whoosh + delayed shimmer = brand signature (~0.5–1.5s)
            events.append((st + 0.05, whoosh, SFX_WHOOSH))
            events.append((st + 0.35, shimmer, SFX_SHIMMER))
        elif kind == "cta":
            events.append((st + 0.08, whoosh, SFX_WHOOSH * 0.7))
            events.append((st + 0.28, shimmer, SFX_SHIMMER * 0.9))

    inputs: list[str] = [
        "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={duration:.3f}",
    ]
    fc_parts: list[str] = []
    for i, (t, path, gain) in enumerate(events, start=1):
        inputs += ["-i", str(path)]
        ms = int(round(t * 1000))
        fc_parts.append(f"[{i}:a]volume={gain:.3f},adelay={ms}|{ms}[e{i}]")

    n = 1 + len(events)
    labels = "[0:a]" + "".join(f"[e{i}]" for i in range(1, len(events) + 1))
    fc = ";".join(fc_parts) + ";" if fc_parts else ""
    fc += f"{labels}amix=inputs={n}:normalize=0:dropout_transition=0[out]"

    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        *inputs,
        "-filter_complex", fc,
        "-map", "[out]", "-c:a", "pcm_s16le",
        "-t", f"{duration:.3f}",
        str(SFX_OUT),
    ])
    return SFX_OUT


def sweeten_vo(vo_path: Path) -> Path:
    """Intimate, warm, clear — never heavily processed."""
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(vo_path),
        "-af",
        (
            # Gentle noise shelf + warmth
            "highpass=f=75,"
            "equalizer=f=180:t=q:w=0.9:g=-1.2,"
            "equalizer=f=350:t=q:w=1.0:g=0.8,"
            "equalizer=f=2400:t=q:w=1.0:g=1.6,"
            "equalizer=f=4500:t=q:w=1.1:g=0.6,"
            "equalizer=f=7500:t=q:w=1.2:g=-1.8,"
            # Soft de-ess
            "deesser=i=0.12:m=0.45:f=0.55:s=o,"
            # Gentle glue — keep natural dynamics
            "acompressor=threshold=-22dB:ratio=1.8:attack=12:release=180:makeup=1.5,"
            "loudnorm=I=-16:TP=-1.5:LRA=9,"
            "aresample=48000,"
            "aformat=sample_rates=48000:channel_layouts=stereo"
        ),
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le",
        str(VO_SWEET),
    ])
    return VO_SWEET


def mix_all(
    duration: float,
    vo: Path,
    music: Path,
    ambience: Path,
    sfx: Path,
    orbit: Path,
) -> Path:
    """VO first. Soft sidechain — mix= keeps some unducked bed (invisible)."""
    filt = (
        f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={VO_LEVEL},asplit=3[vo][sc1][sc2];"
        f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.55[mus];"
        f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[amb];"
        f"[3:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[sfx];"
        f"[4:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[orb];"
        # Soft duck — long release, modest ratio, partial mix (no pumping)
        f"[mus][sc1]sidechaincompress="
        f"threshold=0.08:ratio=2.8:attack=100:release=1100:makeup=1:"
        f"knee=6:level_sc=1:mix=0.65[ducked_m];"
        f"[amb][sc2]sidechaincompress="
        f"threshold=0.09:ratio=2.4:attack=140:release=1200:makeup=1:"
        f"knee=6:level_sc=1:mix=0.60[ducked_a];"
        f"[vo][ducked_m][ducked_a][sfx][orb]amix=inputs=5:duration=longest:normalize=0:dropout_transition=0,"
        f"alimiter=limit=0.96,"
        f"afade=t=out:st={max(0.0, duration - 3.0):.3f}:d=3.0,"
        f"aformat=sample_rates=48000:channel_layouts=stereo"
    )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(vo),
        "-i", str(music),
        "-i", str(ambience),
        "-i", str(sfx),
        "-i", str(orbit),
        "-filter_complex", filt,
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le",
        "-t", f"{duration:.3f}",
        str(MIX_OUT),
    ])
    return MIX_OUT


def mux(video: Path, audio: Path, out: Path, dur: float | None = None) -> None:
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(video), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
    ]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    else:
        cmd += ["-shortest"]
    cmd.append(str(out))
    run(cmd)


def publish_stems() -> None:
    music_dir = ROOT / "05_Music"
    sfx_dir = ROOT / "06_Sound-Effects"
    music_dir.mkdir(parents=True, exist_ok=True)
    sfx_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(MUSIC_OUT, music_dir / "aliens_score_cinematic_v19.wav")
    shutil.copy2(SFX_OUT, sfx_dir / "aliens_sfx_bed_v19.wav")
    shutil.copy2(ORBIT_SFX_OUT, sfx_dir / "aliens_orbit_robotics_v19.wav")
    shutil.copy2(AMB_OUT, sfx_dir / "aliens_space_ambience_v19.wav")
    for name in ("sfx_orbit_servo.wav", "sfx_orbit_blip.wav", "sfx_whoosh.wav", "sfx_shimmer.wav"):
        src = WORK / name
        if src.exists():
            shutil.copy2(src, sfx_dir / name.replace(".wav", "_v19.wav"))


def measure_lufs(path: Path) -> dict[str, str]:
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "loudnorm=print_format=summary", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    out = {}
    for line in r.stderr.splitlines():
        if "Input Integrated" in line:
            out["I"] = line.split(":")[-1].strip()
        elif "Input True Peak" in line:
            out["TP"] = line.split(":")[-1].strip()
        elif "Input LRA" in line:
            out["LRA"] = line.split(":")[-1].strip()
    return out


def main() -> None:
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"

    video_in = VIDEO_PIC if VIDEO_PIC.exists() else VIDEO_FALLBACK
    if not video_in.exists():
        raise SystemExit(f"Missing picture: {video_in}")
    if not VO_SRC.exists():
        raise SystemExit(f"Missing VO: {VO_SRC}")

    bmod = load_broadcast()
    edl_data = json.loads(EDL_PATH.read_text())
    markers = edl_data.get("markers") or json.loads(MARKERS_FALLBACK.read_text())
    duration = min(ffprobe_dur(video_in), ffprobe_dur(VO_SRC) + 0.5)

    print(f"Duration {duration:.2f}s — cinematic score…")
    segs = build_gain_segments(duration, markers)
    print(f"  {len(segs)} music gain segments (hush windows applied)")
    music = build_score(duration, markers)
    print("Space ambience…")
    ambience = build_ambience(duration, markers)
    print("Chapter transitions…")
    sfx = build_sfx(duration, markers)
    print("Orbit robotics (restrained)…")
    cues = orbit_cue_times(edl_data, bmod)
    print(f"  {len(cues)} Orbit cues (min gap 11s)")
    orbit = build_orbit_robotics(duration, cues)
    print("VO sweetening…")
    vo = sweeten_vo(VO_SRC)
    print("Final mix (soft sidechain)…")
    mix = mix_all(duration, vo, music, ambience, sfx, orbit)
    publish_stems()

    print("Loudness check…")
    for label, p in [("mix", mix), ("vo", vo), ("music", music), ("amb", ambience)]:
        m = measure_lufs(p)
        print(f"  {label}: I={m.get('I')}  TP={m.get('TP')}  LRA={m.get('LRA')}")

    if mode == "proof":
        mux(video_in, mix, PROOF_OUT, dur=90.0)
        print(f"\nDONE → {PROOF_OUT}")
        return

    print("Muxing v19 cinematic…")
    mux(video_in, mix, VIDEO_OUT)
    mux(video_in, mix, VIDEO_LATEST)  # refresh current retention cut with new audio
    mux(video_in, mix, PROOF_OUT, dur=90.0)

    print(f"\nDONE → {VIDEO_OUT}")
    print(f"  also refreshed → {VIDEO_LATEST}")
    print(f"  size {VIDEO_OUT.stat().st_size / 1e6:.1f} MB")
    print(f"  duration {ffprobe_dur(VIDEO_OUT):.2f}s")
    print(f"  proof → {PROOF_OUT}")


if __name__ == "__main__":
    main()
