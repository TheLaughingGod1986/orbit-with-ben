#!/usr/bin/env python3
"""Build the clean Orbit upload mix: narrator plus soft cinematic music only.

Preserves the approved v14 picture without re-encoding. Removes all continuous
space ambience, texture beds and incidental sound effects. Uses the clean kDch
Instant Voice Clone master and two original music movements with one crossfade.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "001_Will-We-Ever-Meet-Aliens"
)
VIDEO = (
    ROOT
    / "09_Final-Export/"
    "aliens_BOLD_EXPLAINER_v14_TIGHT_VO_SYNC_UPLOAD_READY_MASTER.mp4"
)
VOICE = (
    ROOT
    / "02_Voiceover/05_Master/"
    "aliens_voiceover_bold-v06_ivc_kDch_master.wav"
)
MUSIC_A = ROOT / "05_Music/aliens_score_cinematic_v19.wav"
MUSIC_B = ROOT / "05_Music/aliens_score_ambient_v16.wav"
WAV_MASTER = ROOT / "05_Music/aliens_v15_clean_vo_soft_music_master.wav"
OUTPUT = (
    ROOT
    / "09_Final-Export/"
    "aliens_BOLD_EXPLAINER_v15_CLEAN_VO_SOFT_MUSIC_UPLOAD_READY_MASTER.mp4"
)
PROOF = ROOT / "09_Final-Export/aliens_v15_PROOF_clean_vo_soft_music_60s.mp4"
REPORT = ROOT / "07_Edit-Project/aliens-v15-clean-audio-report.json"

CUT_START = 17.750
CUT_END = 19.650
CROSSFADE = 4.0


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, capture_output=capture)


def duration(path: Path) -> float:
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
    missing = [path for path in (VIDEO, VOICE, MUSIC_A, MUSIC_B) if not path.exists()]
    if missing:
        raise SystemExit("Missing inputs:\n" + "\n".join(map(str, missing)))

    target_duration = duration(VIDEO)
    music_length = duration(MUSIC_A)
    music_b_length = duration(MUSIC_B)

    # The voice and both music files are lossless WAV sources. Music is set to
    # a restrained -28 LUFS before the final 0.62 mix weight, landing near
    # -32 LUFS before additional narration ducking.
    graph = (
        "[0:a]asplit=2[va][vb];"
        f"[va]atrim=0:{CUT_START},asetpts=PTS-STARTPTS[va0];"
        f"[vb]atrim=start={CUT_END},asetpts=PTS-STARTPTS[vb0];"
        f"[va0][vb0]concat=n=2:v=0:a=1,apad=whole_dur={target_duration},"
        f"atrim=0:{target_duration},"
        "aformat=sample_rates=48000:channel_layouts=stereo[voice];"
        f"[1:a]atrim=0:{music_length},asetpts=PTS-STARTPTS,"
        "loudnorm=I=-28:LRA=9:TP=-3[music_a];"
        f"[2:a]atrim=0:{music_b_length},asetpts=PTS-STARTPTS,"
        "loudnorm=I=-28:LRA=9:TP=-3[music_b];"
        f"[music_a][music_b]acrossfade=d={CROSSFADE}:c1=tri:c2=tri,"
        f"atrim=0:{target_duration},"
        "aformat=sample_rates=48000:channel_layouts=stereo[music];"
        "[voice]asplit=2[voice_sc][voice_mix];"
        "[music][voice_sc]sidechaincompress="
        "threshold=0.020:ratio=7:attack=18:release=420[ducked_music];"
        "[voice_mix][ducked_music]"
        "amix=inputs=2:weights='1 0.62':normalize=0,"
        "volume=-0.5dB,alimiter=limit=0.88:level=false[out]"
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(VOICE),
            "-i",
            str(MUSIC_A),
            "-i",
            str(MUSIC_B),
            "-filter_complex",
            graph,
            "-map",
            "[out]",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-t",
            f"{target_duration}",
            "-c:a",
            "pcm_s24le",
            str(WAV_MASTER),
        ]
    )

    # Preserve the approved v14 video bit-for-bit; replace only its soundtrack.
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(VIDEO),
            "-i",
            str(WAV_MASTER),
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
            "-shortest",
            "-movflags",
            "+faststart",
            str(OUTPUT),
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
            str(OUTPUT),
            "-t",
            "60",
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            "-movflags",
            "+faststart",
            str(PROOF),
        ]
    )

    report = {
        "version": "v15-clean-vo-soft-music",
        "video_source": str(VIDEO),
        "voice_source": str(VOICE),
        "voice_id": "kDch6ACCIpqgQ0NsU9kk",
        "music_sources": [str(MUSIC_A), str(MUSIC_B)],
        "duration": duration(OUTPUT),
        "removed": [
            "continuous_space_ambience",
            "texture_noise_bed",
            "incidental_sound_effects",
        ],
        "music_policy": {
            "source_target_lufs": -28,
            "mix_weight": 0.62,
            "narration_sidechain_ducking": True,
            "crossfade_seconds": CROSSFADE,
            "loops": 0,
        },
        "output": str(OUTPUT),
        "proof": str(PROOF),
        "wav_master": str(WAV_MASTER),
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
