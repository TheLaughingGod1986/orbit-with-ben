#!/usr/bin/env python3
"""
Build Broadcast v11 — same picture as v10, cinematic audio mix.

Adds:
  - calm ambient score bed (curious pad — brand: not trailer boom)
  - soft chapter whooshes + brand/CTA chimes
  - light VO sweetening (presence + gentle compression)
  - sidechain duck so music sits under narration

Picture: 09_Final-Export/aliens_broadcast_v10_clean_cuts.mp4
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDIT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "09_Final-Export"
WORK = EDIT / "_mix_work_v11"
WORK.mkdir(parents=True, exist_ok=True)

VIDEO_IN = OUT_DIR / "aliens_broadcast_v10_clean_cuts.mp4"
VO_SRC = ROOT / "02_Voiceover/05_Master/aliens_voiceover_master_storyteller_v04.wav"
MARKERS_PATH = EDIT / "VO_MARKERS_v08.json"

MUSIC_OUT = WORK / "score_bed.wav"
SFX_OUT = WORK / "sfx_bed.wav"
VO_SWEET = WORK / "vo_sweetened.wav"
MIX_OUT = WORK / "final_mix.wav"
VIDEO_OUT = OUT_DIR / "aliens_broadcast_v11_cinematic_mix.mp4"

# Brand: calm cinematic pad under VO — audible but never competing
MUSIC_UNDER_VO = 0.12
MUSIC_IN_GAPS = 0.30
MUSIC_BRAND = 0.36
MUSIC_CTA = 0.34
SFX_LEVEL = 0.24
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


def load_markers() -> list[dict]:
    return json.loads(MARKERS_PATH.read_text())


def build_score(duration: float, markers: list[dict]) -> Path:
    """Layered ambient pad + slow harmonic motion. Curious, not epic."""
    lifts: list[tuple[float, float, float]] = []  # start, end, gain
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

    base = MUSIC_UNDER_VO
    expr = f"{base}"
    for a, b, g in reversed(lifts):
        # commas escaped for ffmpeg volume expression
        expr = f"if(between(t\\,{a:.3f}\\,{b:.3f})\\,{g:.3f}\\,{expr})"

    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            f"sine=frequency=65.41:sample_rate=48000:duration={duration:.3f}[d];"
            f"sine=frequency=98.00:sample_rate=48000:duration={duration:.3f}[f];"
            f"sine=frequency=130.81:sample_rate=48000:duration={duration:.3f}[o];"
            f"sine=frequency=196.00:sample_rate=48000:duration={duration:.3f}[h];"
            f"anoisesrc=color=pink:sample_rate=48000:duration={duration:.3f}[n];"
            f"[n]lowpass=f=700,highpass=f=120,volume=0.05,aformat=channel_layouts=stereo[air];"
            f"[d]aformat=channel_layouts=stereo,volume=0.24[d1];"
            f"[f]aformat=channel_layouts=stereo,volume=0.15[f1];"
            f"[o]aformat=channel_layouts=stereo,volume=0.08[o1];"
            f"[h]aformat=channel_layouts=stereo,volume=0.05,tremolo=f=0.12:d=0.4[h1];"
            f"[d1][f1][o1][h1][air]amix=inputs=5:normalize=0:dropout_transition=0,"
            f"lowpass=f=2200,highpass=f=35,"
            f"volume='{expr}',"
            f"afade=t=in:st=0:d=1.0,"
            f"afade=t=out:st={max(0.0, duration - 3.2):.3f}:d=3.2"
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
            events.append((max(0.05, st + 0.08), chime, 0.38))
        elif kind == "chapter_gap":
            events.append((st + 0.08, whoosh, SFX_LEVEL))
        elif kind == "cta":
            events.append((st + 0.1, whoosh, 0.18))
            events.append((st + 0.2, chime, 0.42))

    inputs: list[str] = [
        "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={duration:.3f}",
    ]
    fc_parts: list[str] = []
    for i, (t, path, gain) in enumerate(events, start=1):
        inputs += ["-i", str(path)]
        lab = f"e{i}"
        ms = int(round(t * 1000))
        fc_parts.append(f"[{i}:a]volume={gain:.3f},adelay={ms}|{ms}[{lab}]")

    n = 1 + len(events)
    labels = ["[0:a]"] + [f"[e{i}]" for i in range(1, len(events) + 1)]
    fc = ";".join(fc_parts)
    if fc:
        fc += ";"
    fc += f"{''.join(labels)}amix=inputs={n}:normalize=0:dropout_transition=0[out]"

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
    """Presence + gentle compression so the read feels less flat."""
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
        "-ar", "48000",
        "-ac", "2",
        "-c:a", "pcm_s16le",
        str(VO_SWEET),
    ])
    return VO_SWEET


def mix_all(duration: float, vo: Path, music: Path, sfx: Path) -> Path:
    filt = (
        f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={VO_LEVEL},asplit=2[vo][sc];"
        f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[mus];"
        f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[sfx];"
        f"[mus][sc]sidechaincompress="
        f"threshold=0.05:ratio=6:attack=40:release=420:makeup=1:level_sc=1[ducked];"
        f"[vo][ducked][sfx]amix=inputs=3:duration=longest:normalize=0:dropout_transition=0,"
        f"alimiter=limit=0.95,"
        f"afade=t=out:st={max(0.0, duration - 2.5):.3f}:d=2.5,"
        f"aformat=sample_rates=48000:channel_layouts=stereo"
    )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(vo),
        "-i", str(music),
        "-i", str(sfx),
        "-filter_complex", filt,
        "-ar", "48000",
        "-ac", "2",
        "-c:a", "pcm_s16le",
        "-t", f"{duration:.3f}",
        str(MIX_OUT),
    ])
    return MIX_OUT


def mux(video: Path, audio: Path, out: Path) -> None:
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(video),
        "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(out),
    ])


def main() -> None:
    if not VIDEO_IN.exists():
        raise SystemExit(f"Missing picture: {VIDEO_IN}")
    if not VO_SRC.exists():
        raise SystemExit(f"Missing VO: {VO_SRC}")

    duration = ffprobe_dur(VIDEO_IN)
    markers = load_markers()

    print(f"Duration {duration:.2f}s — building score…")
    music = build_score(duration, markers)
    print("Building SFX bed…")
    sfx = build_sfx(duration, markers)
    print("Sweetening VO…")
    vo = sweeten_vo(VO_SRC)
    print("Mixing (sidechain duck)…")
    mix = mix_all(duration, vo, music, sfx)
    print("Muxing v11…")
    mux(VIDEO_IN, mix, VIDEO_OUT)

    draft = EDIT / "capcut_draft" / "draft_content.json"
    if draft.exists():
        data = json.loads(draft.read_text())
        data["final_video"] = str(VIDEO_OUT)
        data["notes"] = (
            "v11 cinematic mix: ambient score + chapter whooshes + VO presence, "
            "sidechain-ducked under narration. Picture = v10 clean cuts."
        )
        draft.write_text(json.dumps(data, indent=2) + "\n")

    print(f"\nDONE → {VIDEO_OUT}")
    print(f"  size {VIDEO_OUT.stat().st_size / 1e6:.1f} MB")
    print(f"  duration {ffprobe_dur(VIDEO_OUT):.2f}s")


if __name__ == "__main__":
    main()
