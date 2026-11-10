#!/usr/bin/env python3
"""
Broadcast v16 — polished mix on v15 corner-Orbit picture.

Adds:
  - richer calm ambient score (curious pad — brand: not trailer boom)
  - soft space ambience bed
  - chapter whooshes + brand/CTA chimes
  - subtle Orbit robotics cues (servo / soft blip) timed to B-roll Orbit windows
  - VO sweetening + sidechain duck under narration

Picture: 09_Final-Export/aliens_broadcast_v15_corner_orbit_pic.mp4
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
WORK = EDIT / "_mix_work_v16"
WORK.mkdir(parents=True, exist_ok=True)

VIDEO_PIC = OUT_DIR / "aliens_broadcast_v15_corner_orbit_pic.mp4"
VIDEO_FALLBACK = OUT_DIR / "aliens_broadcast_v15_corner_orbit.mp4"
VO_SRC = ROOT / "02_Voiceover/05_Master/aliens_voiceover_master_storyteller_v04.wav"
EDL_PATH = EDIT / "SECTION_EDL_v10_clean_cuts.json"
MARKERS_PATH = EDIT / "VO_MARKERS_v08.json"

MUSIC_OUT = WORK / "score_bed.wav"
SFX_OUT = WORK / "sfx_bed.wav"
ORBIT_SFX_OUT = WORK / "orbit_robotics.wav"
VO_SWEET = WORK / "vo_sweetened.wav"
MIX_OUT = WORK / "final_mix.wav"
VIDEO_OUT = OUT_DIR / "aliens_broadcast_v16_polished_mix.mp4"
PROOF_OUT = OUT_DIR / "aliens_v16_PROOF_polished_mix_90s.mp4"

# Levels — music/SFX present, Orbit robotics whisper-quiet
MUSIC_UNDER_VO = 0.15
MUSIC_IN_GAPS = 0.32
MUSIC_BRAND = 0.38
MUSIC_CTA = 0.36
AMBIENCE_LEVEL = 0.07
SFX_WHOOSH = 0.22
SFX_CHIME = 0.36
ORBIT_SERVO = 0.09
ORBIT_BLIP = 0.07
VO_LEVEL = 1.0


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


def build_score(duration: float, markers: list[dict]) -> Path:
    """Layered ambient pad — a little more musical than v11, still calm."""
    lifts: list[tuple[float, float, float]] = []
    for m in markers:
        st = float(m["start_s"])
        en = st + float(m["duration_s"])
        kind = m["kind"]
        if kind == "lead":
            lifts.append((st, en, MUSIC_BRAND))
        elif kind == "chapter_gap":
            lifts.append((st, max(st, en - 0.1), MUSIC_IN_GAPS))
        elif kind == "cta":
            lifts.append((st, en, MUSIC_CTA))

    expr = f"{MUSIC_UNDER_VO}"
    for a, b, g in reversed(lifts):
        expr = f"if(between(t\\,{a:.3f}\\,{b:.3f})\\,{g:.3f}\\,{expr})"

    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            # Root drone stack (C2 / G2 / C3 / E3) + soft fifth shimmer
            f"sine=frequency=65.41:sample_rate=48000:duration={duration:.3f}[d];"
            f"sine=frequency=98.00:sample_rate=48000:duration={duration:.3f}[f];"
            f"sine=frequency=130.81:sample_rate=48000:duration={duration:.3f}[o];"
            f"sine=frequency=164.81:sample_rate=48000:duration={duration:.3f}[e];"
            f"sine=frequency=196.00:sample_rate=48000:duration={duration:.3f}[h];"
            f"sine=frequency=392.00:sample_rate=48000:duration={duration:.3f}[sh];"
            f"anoisesrc=color=pink:sample_rate=48000:duration={duration:.3f}[n];"
            f"[n]lowpass=f=650,highpass=f=90,volume=0.045,aformat=channel_layouts=stereo[air];"
            f"[d]aformat=channel_layouts=stereo,volume=0.26[d1];"
            f"[f]aformat=channel_layouts=stereo,volume=0.16[f1];"
            f"[o]aformat=channel_layouts=stereo,volume=0.09[o1];"
            f"[e]aformat=channel_layouts=stereo,volume=0.06,tremolo=f=0.10:d=0.35[e1];"
            f"[h]aformat=channel_layouts=stereo,volume=0.05,tremolo=f=0.11:d=0.4[h1];"
            f"[sh]aformat=channel_layouts=stereo,volume=0.03,"
            f"tremolo=f=0.10:d=0.5,afade=t=in:st=0:d=4[sh1];"
            f"[d1][f1][o1][e1][h1][sh1][air]amix=inputs=7:normalize=0:dropout_transition=0,"
            f"lowpass=f=2400,highpass=f=32,"
            f"volume='{expr}',"
            f"afade=t=in:st=0:d=1.2,"
            f"afade=t=out:st={max(0.0, duration - 3.5):.3f}:d=3.5"
        ),
        "-c:a", "pcm_s16le", str(MUSIC_OUT),
    ])
    return MUSIC_OUT


def _whoosh(path: Path, dur: float = 0.85) -> None:
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            f"anoisesrc=color=white:sample_rate=48000:duration={dur},"
            f"highpass=f=400,lowpass=f=3500,"
            f"afade=t=in:st=0:d=0.12,afade=t=out:st={dur - 0.45:.3f}:d=0.45,"
            f"volume=1.0,aformat=channel_layouts=stereo"
        ),
        "-c:a", "pcm_s16le", str(path),
    ])


def _soft_chime(path: Path) -> None:
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            "sine=frequency=523.25:sample_rate=48000:duration=1.4[a];"
            "sine=frequency=659.25:sample_rate=48000:duration=1.4[b];"
            "[a][b]amix=inputs=2:normalize=0,"
            "afade=t=in:st=0:d=0.05,afade=t=out:st=0.35:d=1.0,"
            "volume=0.55,aformat=channel_layouts=stereo"
        ),
        "-c:a", "pcm_s16le", str(path),
    ])


def _orbit_servo(path: Path) -> None:
    """Short soft servo whir — futuristic, not cartoon."""
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            "sine=frequency=420:sample_rate=48000:duration=0.38[a];"
            "sine=frequency=680:sample_rate=48000:duration=0.38[b];"
            "anoisesrc=color=pink:sample_rate=48000:duration=0.38[n];"
            "[n]bandpass=f=900:width_type=h:width=700,volume=0.35[n1];"
            "[a]aformat=channel_layouts=stereo,afade=t=in:st=0:d=0.02,"
            "afade=t=out:st=0.12:d=0.26,volume=0.45[a1];"
            "[b]aformat=channel_layouts=stereo,afade=t=in:st=0.04:d=0.03,"
            "afade=t=out:st=0.14:d=0.24,volume=0.28[b1];"
            "[n1]aformat=channel_layouts=stereo,afade=t=in:st=0:d=0.03,"
            "afade=t=out:st=0.18:d=0.2[n2];"
            "[a1][b1][n2]amix=inputs=3:normalize=0,"
            "highpass=f=180,lowpass=f=3200,volume=1.0"
        ),
        "-c:a", "pcm_s16le", str(path),
    ])


def _orbit_blip(path: Path) -> None:
    """Tiny digital acknowledge tick."""
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            "sine=frequency=880:sample_rate=48000:duration=0.18[a];"
            "sine=frequency=1320:sample_rate=48000:duration=0.18[b];"
            "[a][b]amix=inputs=2:normalize=0,"
            "afade=t=in:st=0:d=0.005,afade=t=out:st=0.04:d=0.14,"
            "highpass=f=400,volume=0.7,aformat=channel_layouts=stereo"
        ),
        "-c:a", "pcm_s16le", str(path),
    ])


def build_ambience(duration: float) -> Path:
    """Continuous soft space bed — sits under everything."""
    out = WORK / "space_ambience.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            f"anoisesrc=color=brown:sample_rate=48000:duration={duration:.3f}[n];"
            f"sine=frequency=48:sample_rate=48000:duration={duration:.3f}[d];"
            f"[n]highpass=f=40,lowpass=f=400,volume=0.55,aformat=channel_layouts=stereo[n1];"
            f"[d]aformat=channel_layouts=stereo,volume=0.12,tremolo=f=0.10:d=0.3[d1];"
            f"[n1][d1]amix=inputs=2:normalize=0,"
            f"volume={AMBIENCE_LEVEL},"
            f"afade=t=in:st=0:d=2.0,"
            f"afade=t=out:st={max(0.0, duration - 3.0):.3f}:d=3.0"
        ),
        "-c:a", "pcm_s16le", str(out),
    ])
    return out


def orbit_cue_times(edl_data: dict, bmod) -> list[tuple[float, str]]:
    """Return (time, kind) cues — throttled so robotics never chatter."""
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
    cues: list[tuple[float, str]] = []
    last_t = -99.0
    for i, w in enumerate(windows):
        t = float(w["start"])
        if t - last_t < 5.0:
            continue
        kind = "servo" if i % 3 != 2 else "blip"
        # Emotion spikes get a tiny blip
        if w.get("emotion") in ("surprise", "scared", "wonder"):
            kind = "blip" if kind == "servo" else "servo"
        cues.append((t + 0.05, kind))
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
    chime = WORK / "sfx_chime.wav"
    _whoosh(whoosh)
    _soft_chime(chime)

    events: list[tuple[float, Path, float]] = []
    for m in markers:
        st = float(m["start_s"])
        kind = m["kind"]
        if kind == "lead":
            events.append((max(0.05, st + 0.08), chime, SFX_CHIME))
        elif kind == "chapter_gap":
            events.append((st + 0.08, whoosh, SFX_WHOOSH))
        elif kind == "cta":
            events.append((st + 0.1, whoosh, 0.16))
            events.append((st + 0.2, chime, 0.40))

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
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(vo_path),
        "-af",
        (
            "highpass=f=70,"
            "equalizer=f=220:t=q:w=1.0:g=-1.5,"
            "equalizer=f=2800:t=q:w=1.1:g=2.2,"
            "equalizer=f=5500:t=q:w=1.0:g=1.0,"
            "acompressor=threshold=-20dB:ratio=2.2:attack=8:release=120:makeup=2,"
            "loudnorm=I=-16:TP=-1.5:LRA=10,"
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
    filt = (
        f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={VO_LEVEL},asplit=2[vo][sc];"
        f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[mus];"
        f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[amb];"
        f"[3:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[sfx];"
        f"[4:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[orb];"
        # Duck music + ambience under VO; leave Orbit ticks mostly alone (already quiet)
        f"[mus][sc]sidechaincompress="
        f"threshold=0.05:ratio=6:attack=35:release=450:makeup=1:level_sc=1[ducked_m];"
        f"[amb][sc]sidechaincompress="
        f"threshold=0.06:ratio=4:attack=50:release=500:makeup=1:level_sc=1[ducked_a];"
        f"[vo][ducked_m][ducked_a][sfx][orb]amix=inputs=5:duration=longest:normalize=0:dropout_transition=0,"
        f"alimiter=limit=0.95,"
        f"afade=t=out:st={max(0.0, duration - 2.5):.3f}:d=2.5,"
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
    shutil.copy2(MUSIC_OUT, music_dir / "aliens_score_ambient_v16.wav")
    shutil.copy2(SFX_OUT, sfx_dir / "aliens_sfx_bed_v16.wav")
    shutil.copy2(ORBIT_SFX_OUT, sfx_dir / "aliens_orbit_robotics_v16.wav")
    for name in ("sfx_orbit_servo.wav", "sfx_orbit_blip.wav", "sfx_whoosh.wav", "sfx_chime.wav"):
        src = WORK / name
        if src.exists():
            shutil.copy2(src, sfx_dir / name.replace(".wav", "_v16.wav"))


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
    markers = edl_data.get("markers") or json.loads(MARKERS_PATH.read_text())
    duration = ffprobe_dur(video_in)

    print(f"Duration {duration:.2f}s — building score…")
    music = build_score(duration, markers)
    print("Building space ambience…")
    ambience = build_ambience(duration)
    print("Building chapter SFX…")
    sfx = build_sfx(duration, markers)
    print("Building Orbit robotics…")
    cues = orbit_cue_times(edl_data, bmod)
    print(f"  {len(cues)} Orbit cues")
    orbit = build_orbit_robotics(duration, cues)
    print("Sweetening VO…")
    vo = sweeten_vo(VO_SRC)
    print("Mixing (sidechain duck)…")
    mix = mix_all(duration, vo, music, ambience, sfx, orbit)
    publish_stems()

    if mode == "proof":
        print("Muxing 90s proof…")
        mux(video_in, mix, PROOF_OUT, dur=90.0)
        print(f"\nDONE → {PROOF_OUT}")
        return

    print("Muxing v16 full…")
    mux(video_in, mix, VIDEO_OUT)
    # Convenience 90s proof alongside
    mux(video_in, mix, PROOF_OUT, dur=90.0)

    print(f"\nDONE → {VIDEO_OUT}")
    print(f"  size {VIDEO_OUT.stat().st_size / 1e6:.1f} MB")
    print(f"  duration {ffprobe_dur(VIDEO_OUT):.2f}s")
    print(f"  proof → {PROOF_OUT}")


if __name__ == "__main__":
    main()
