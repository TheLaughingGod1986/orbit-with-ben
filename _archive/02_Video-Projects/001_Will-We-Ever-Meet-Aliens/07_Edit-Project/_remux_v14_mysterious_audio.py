#!/usr/bin/env python3
"""Remux v14 full cinematic master with an audible mysterious music bed.

Picture stays untouched. VO stays king. Music/ambience sit under narration
with soft ducking — calm documentary atmosphere, not trailer boom.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDIT = ROOT / "07_Edit-Project"
WORK = EDIT / "_mix_work_v14_full"
WORK.mkdir(parents=True, exist_ok=True)

PIC_IN = ROOT / "09_Final-Export/aliens_v14_FULL_CINEMATIC_MASTER_18m50s_FINAL.mp4"
VO = ROOT / "02_Voiceover/05_Master/aliens_voiceover_v10_ivc_kDch_full_master.wav"
EDL = EDIT / "aliens_v14_full_cinematic_edl.json"
WHOOSH = ROOT / "06_Sound-Effects/sfx_whoosh_v19.wav"
CHIME = ROOT / "06_Sound-Effects/sfx_brand_chime_v11.wav"
SHIMMER = ROOT / "06_Sound-Effects/sfx_shimmer_v19.wav"

OUT = ROOT / "09_Final-Export/aliens_v14_FULL_CINEMATIC_MASTER_18m50s_MUSIC.mp4"
OUT_FINAL = ROOT / "09_Final-Export/aliens_v14_FULL_CINEMATIC_MASTER_18m50s_FINAL.mp4"
OUT_ALIAS = ROOT / "09_Final-Export/aliens_v13_FULL_CINEMATIC_MASTER_18m50s_FINAL.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v14_PROOF_mysterious_audio_90s.mp4"

SCORE = WORK / "mysterious_score.wav"
AMB = WORK / "space_ambience.wav"
SFX = WORK / "chapter_sfx.wav"
VO_SWEET = WORK / "vo_sweetened.wav"
MIX = WORK / "final_mix.wav"
PIC_ONLY = WORK / "picture_only.mp4"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def probe(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(r.stdout.strip())


def build_score(duration: float) -> Path:
    """Slow evolving mysterious pad — audible but calm."""
    # Louder internal layers than v19 stem so under-VO bed is actually felt
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            f"sine=frequency=49.00:sample_rate=48000:duration={duration:.3f}[d1];"
            f"sine=frequency=73.42:sample_rate=48000:duration={duration:.3f}[d2];"
            f"sine=frequency=98.00:sample_rate=48000:duration={duration:.3f}[d3];"
            f"sine=frequency=146.83:sample_rate=48000:duration={duration:.3f}[d4];"
            f"sine=frequency=196.00:sample_rate=48000:duration={duration:.3f}[d5];"
            f"sine=frequency=293.66:sample_rate=48000:duration={duration:.3f}[d6];"
            f"sine=frequency=392.00:sample_rate=48000:duration={duration:.3f}[sh];"
            f"anoisesrc=color=pink:sample_rate=48000:duration={duration:.3f}[pn];"
            f"[pn]highpass=f=100,lowpass=f=800,volume=0.08,aformat=channel_layouts=stereo[air];"
            f"[d1]aformat=channel_layouts=stereo,volume=0.55[a];"
            f"[d2]aformat=channel_layouts=stereo,volume=0.38[b];"
            f"[d3]aformat=channel_layouts=stereo,volume=0.22[c];"
            f"[d4]aformat=channel_layouts=stereo,volume=0.14,tremolo=f=0.10:d=0.35[d];"
            f"[d5]aformat=channel_layouts=stereo,volume=0.09,tremolo=f=0.11:d=0.40[e];"
            f"[d6]aformat=channel_layouts=stereo,volume=0.06,tremolo=f=0.12:d=0.45[f];"
            f"[sh]aformat=channel_layouts=stereo,volume=0.035,"
            f"tremolo=f=0.10:d=0.55,afade=t=in:st=3:d=8[g];"
            f"[a][b][c][d][e][f][g][air]amix=inputs=8:normalize=0:dropout_transition=0,"
            f"highpass=f=35,lowpass=f=3800,"
            f"equalizer=f=1800:t=q:w=1.1:g=-5,"
            f"equalizer=f=2800:t=q:w=1.0:g=-3.5,"
            f"volume=0.85,"
            f"afade=t=in:st=0:d=2.5,"
            f"afade=t=out:st={max(0.0, duration - 6):.3f}:d=6"
        ),
        "-c:a", "pcm_s16le", str(SCORE),
    ])
    return SCORE


def build_ambience(duration: float) -> Path:
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-filter_complex",
        (
            f"anoisesrc=color=brown:sample_rate=48000:duration={duration:.3f}[n];"
            f"sine=frequency=40:sample_rate=48000:duration={duration:.3f}[d];"
            f"sine=frequency=67:sample_rate=48000:duration={duration:.3f}[h];"
            f"[n]highpass=f=30,lowpass=f=350,volume=0.65,aformat=channel_layouts=stereo[n1];"
            f"[d]aformat=channel_layouts=stereo,volume=0.18,tremolo=f=0.10:d=0.30[d1];"
            f"[h]aformat=channel_layouts=stereo,volume=0.07,tremolo=f=0.11:d=0.35[h1];"
            f"[n1][d1][h1]amix=inputs=3:normalize=0,"
            f"volume=0.22,"
            f"afade=t=in:st=0:d=3,"
            f"afade=t=out:st={max(0.0, duration - 5):.3f}:d=5"
        ),
        "-c:a", "pcm_s16le", str(AMB),
    ])
    return AMB


def build_sfx(duration: float, markers: list[float]) -> Path:
    """Soft whoosh+shimmer at brand/section boundaries."""
    if not WHOOSH.exists():
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={duration:.3f}",
            "-c:a", "pcm_s16le", "-t", f"{duration:.3f}", str(SFX),
        ])
        return SFX

    events: list[tuple[float, Path, float]] = []
    whoosh = WHOOSH
    chime = CHIME if CHIME.exists() else WHOOSH
    shimmer = SHIMMER if SHIMMER.exists() else chime
    for i, t in enumerate(markers):
        events.append((t + 0.05, whoosh, 0.14 if i else 0.18))
        events.append((t + 0.28, shimmer, 0.16 if i else 0.22))

    inputs: list[str] = ["-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={duration:.3f}"]
    fc_parts: list[str] = []
    for i, (t, path, gain) in enumerate(events, start=1):
        inputs += ["-i", str(path)]
        ms = int(round(max(0.0, t) * 1000))
        fc_parts.append(f"[{i}:a]volume={gain:.3f},adelay={ms}|{ms}[e{i}]")
    n = 1 + len(events)
    labels = "[0:a]" + "".join(f"[e{i}]" for i in range(1, len(events) + 1))
    fc = ";".join(fc_parts) + ";" + f"{labels}amix=inputs={n}:normalize=0:dropout_transition=0[out]"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        *inputs, "-filter_complex", fc, "-map", "[out]",
        "-c:a", "pcm_s16le", "-t", f"{duration:.3f}", str(SFX),
    ])
    return SFX


def sweeten_vo(duration: float) -> Path:
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(VO),
        "-af",
        (
            "highpass=f=75,"
            "equalizer=f=180:t=q:w=0.9:g=-1.0,"
            "equalizer=f=2400:t=q:w=1.0:g=1.5,"
            "equalizer=f=7500:t=q:w=1.2:g=-1.5,"
            "deesser=i=0.12:m=0.45:f=0.55:s=o,"
            "acompressor=threshold=-22dB:ratio=1.8:attack=12:release=180:makeup=1.4,"
            "loudnorm=I=-16:TP=-1.5:LRA=9,"
            f"apad=pad_dur=12,atrim=0:{duration:.3f},"
            "aformat=sample_rates=48000:channel_layouts=stereo"
        ),
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(VO_SWEET),
    ])
    return VO_SWEET


def mix_all(duration: float) -> Path:
    # Music ~ audible under VO; soft duck; ambience quieter; sfx light
    filt = (
        f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0,asplit=3[vo][sc1][sc2];"
        f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.15[mus];"
        f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[amb];"
        f"[3:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[sfx];"
        f"[mus][sc1]sidechaincompress="
        f"threshold=0.08:ratio=2.8:attack=110:release=1100:makeup=1:"
        f"knee=6:level_sc=1:mix=0.62[ducked_m];"
        f"[amb][sc2]sidechaincompress="
        f"threshold=0.09:ratio=2.4:attack=140:release=1200:makeup=1:"
        f"knee=6:level_sc=1:mix=0.55[ducked_a];"
        f"[vo][ducked_m][ducked_a][sfx]amix=inputs=4:duration=longest:normalize=0:dropout_transition=0,"
        f"alimiter=limit=0.95,"
        f"afade=t=out:st={max(0.0, duration - 3.5):.3f}:d=3.5,"
        f"aformat=sample_rates=48000:channel_layouts=stereo"
    )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(VO_SWEET),
        "-i", str(SCORE),
        "-i", str(AMB),
        "-i", str(SFX),
        "-filter_complex", filt,
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le",
        "-t", f"{duration:.3f}", str(MIX),
    ])
    return MIX


def main() -> None:
    assert PIC_IN.exists(), PIC_IN
    assert VO.exists(), VO
    duration = probe(PIC_IN)
    print(f"Picture {duration:.1f}s — extracting video…")
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(PIC_IN), "-c:v", "copy", "-an", str(PIC_ONLY),
    ])

    markers = [0.0]
    if EDL.exists():
        data = json.loads(EDL.read_text())
        for shot in data.get("edl", []):
            if shot.get("kind") in ("brand", "cta") or (
                shot.get("kind") == "card" and "chapter" in str(shot.get("source", "")).lower()
            ):
                markers.append(float(shot["start"]))
        # section-ish starts from edl section changes
        last = None
        for shot in data.get("edl", []):
            sec = shot.get("section")
            if sec and sec != last and sec not in ("hook",):
                markers.append(float(shot["start"]))
                last = sec
    markers = sorted(set(round(m, 3) for m in markers if 0 <= m < duration - 1))[:12]
    print(f"SFX markers: {markers}")

    print("Building mysterious score…")
    build_score(duration)
    print("Building space ambience…")
    build_ambience(duration)
    print("Building transition SFX…")
    build_sfx(duration, markers)
    print("Sweetening VO…")
    sweeten_vo(duration)
    print("Mixing (soft duck under VO)…")
    mix_all(duration)

    print("Muxing final…")
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(PIC_ONLY), "-i", str(MIX),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
        "-movflags", "+faststart", "-shortest",
        str(OUT),
    ])
    run(["cp", str(OUT), str(OUT_FINAL)])
    run(["cp", str(OUT), str(OUT_ALIAS)])
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(OUT), "-t", "90", "-c", "copy", str(PROOF),
    ])

    # Loudness check
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-ss", "120", "-t", "30", "-i", str(OUT),
         "-af", "loudnorm=print_format=summary", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    for line in r.stderr.splitlines():
        if "Input Integrated" in line or "Input LRA" in line:
            print(" ", line.strip())
    # Music-only check
    r2 = subprocess.run(
        ["ffmpeg", "-hide_banner", "-t", "20", "-i", str(SCORE),
         "-af", "loudnorm=print_format=summary", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    for line in r2.stderr.splitlines():
        if "Input Integrated" in line:
            print("  score", line.strip())

    print(f"\nDONE → {OUT}")
    print(f"proof → {PROOF}")


if __name__ == "__main__":
    main()
