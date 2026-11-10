#!/usr/bin/env python3
"""Final Orbit launch mix: clean VO, soft score, sparse intentional cues.

The approved v16 picture and voice remain unchanged. Continuous ambience and
texture beds are permanently excluded. Only music, chapter transitions,
branding and six restrained Orbit performance cues are added.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "001_Will-We-Ever-Meet-Aliens"
)
SOURCE = (
    ROOT
    / "09_Final-Export/"
    "aliens_BOLD_EXPLAINER_v16_VIDEO_ORBIT_VO_ONLY_UPLOAD_READY_MASTER.mp4"
)
MUSIC_A = ROOT / "05_Music/aliens_score_cinematic_v19.wav"
MUSIC_B = ROOT / "05_Music/aliens_score_ambient_v16.wav"
CHIME = ROOT / "06_Sound-Effects/sfx_brand_chime_v11.wav"
WHOOSH = ROOT / "06_Sound-Effects/sfx_whoosh_v19.wav"
SHIMMER = ROOT / "06_Sound-Effects/sfx_shimmer_v19.wav"
SERVO = ROOT / "06_Sound-Effects/sfx_orbit_servo_v19.wav"
BLIP = ROOT / "06_Sound-Effects/sfx_orbit_blip_v19.wav"
WAV = ROOT / "05_Music/aliens_v17_final_sparse_sound_master.wav"
OUTPUT = (
    ROOT
    / "09_Final-Export/"
    "aliens_BOLD_EXPLAINER_v17_FINAL_UPLOAD_READY_MASTER.mp4"
)
OPENING_PROOF = ROOT / "09_Final-Export/aliens_v17_PROOF_final_opening_60s.mp4"
MID_PROOF = ROOT / "09_Final-Export/aliens_v17_PROOF_final_midsection_60s.mp4"
REPORT = ROOT / "07_Edit-Project/aliens-v17-final-audio-report.json"

# v13 cue times shifted by the 1.900-second v14 pre-brand cut.
BRAND_TIME = 17.750
CHAPTER_TIMES = [19.750, 155.891, 223.380, 293.639, 425.326, 710.891, 871.366, 1041.078]
ORBIT_TIMES = [19.750, 235.479, 435.614, 719.673, 886.186, 1056.257]
OUTRO_TIME = 1101.667


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, capture_output=capture)


def probe_duration(path: Path) -> float:
    result = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        capture=True,
    )
    return float(result.stdout.strip())


def main() -> None:
    inputs = [SOURCE, MUSIC_A, MUSIC_B, CHIME, WHOOSH, SHIMMER, SERVO, BLIP]
    missing = [path for path in inputs if not path.exists()]
    if missing:
        raise SystemExit("Missing inputs:\n" + "\n".join(map(str, missing)))

    duration = probe_duration(SOURCE)
    filters = [
        f"[0:a]atrim=0:{duration},aformat=sample_rates=48000:channel_layouts=stereo[voice]",
        "[1:a]loudnorm=I=-28:LRA=9:TP=-3[music_a]",
        "[2:a]loudnorm=I=-28:LRA=9:TP=-3[music_b]",
        f"[music_a][music_b]acrossfade=d=4:c1=tri:c2=tri,atrim=0:{duration},"
        "aformat=sample_rates=48000:channel_layouts=stereo[music]",
        "[voice]asplit=2[voice_sc][voice_mix]",
        "[music][voice_sc]sidechaincompress="
        "threshold=0.020:ratio=7:attack=18:release=420[ducked_music]",
        f"[3:a]volume=0.42,adelay={round(BRAND_TIME * 1000)}|{round(BRAND_TIME * 1000)}[brand]",
    ]
    mix_labels = ["voice_mix", "ducked_music", "brand"]

    for index, cue in enumerate(CHAPTER_TIMES):
        name = f"chapter_{index}"
        delay = round(cue * 1000)
        filters.append(f"[4:a]volume=0.09,adelay={delay}|{delay}[{name}]")
        mix_labels.append(name)

    for index, cue in enumerate(ORBIT_TIMES):
        name = f"orbit_{index}"
        delay = round(cue * 1000)
        filters.append(f"[6:a]volume=0.20,adelay={delay}|{delay}[{name}]")
        mix_labels.append(name)

    for index, cue in enumerate([BRAND_TIME + 0.55, OUTRO_TIME + 0.70]):
        name = f"blip_{index}"
        delay = round(cue * 1000)
        filters.append(f"[7:a]volume=0.18,adelay={delay}|{delay}[{name}]")
        mix_labels.append(name)

    filters.append(
        f"[5:a]volume=0.16,adelay={round((OUTRO_TIME + 0.25) * 1000)}|"
        f"{round((OUTRO_TIME + 0.25) * 1000)}[outro_shimmer]"
    )
    mix_labels.append("outro_shimmer")
    filters.append(
        "".join(f"[{label}]" for label in mix_labels)
        + f"amix=inputs={len(mix_labels)}:weights='1 0.62 "
        + " ".join("1" for _ in mix_labels[2:])
        + "':normalize=0,volume=-0.5dB,"
        "alimiter=limit=0.88:level=false[out]"
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(SOURCE),
            "-i",
            str(MUSIC_A),
            "-i",
            str(MUSIC_B),
            "-i",
            str(CHIME),
            "-i",
            str(WHOOSH),
            "-i",
            str(SHIMMER),
            "-i",
            str(SERVO),
            "-i",
            str(BLIP),
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[out]",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-t",
            f"{duration}",
            "-c:a",
            "pcm_s24le",
            str(WAV),
        ]
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(SOURCE),
            "-i",
            str(WAV),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "256k",
            "-movflags",
            "+faststart",
            str(OUTPUT),
        ]
    )
    for start, length, target in [
        (0, 60, OPENING_PROOF),
        (690, 60, MID_PROOF),
    ]:
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                str(start),
                "-i",
                str(OUTPUT),
                "-t",
                str(length),
                "-c",
                "copy",
                "-movflags",
                "+faststart",
                str(target),
            ]
        )

    report = {
        "version": "v17-final-sparse-sound",
        "output": str(OUTPUT),
        "duration": probe_duration(OUTPUT),
        "voice_id": "kDch6ACCIpqgQ0NsU9kk",
        "continuous_ambience": False,
        "texture_bed": False,
        "music_loops": 0,
        "chapter_cues": len(CHAPTER_TIMES),
        "orbit_cues": len(ORBIT_TIMES),
        "proofs": [str(OPENING_PROOF), str(MID_PROOF)],
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
