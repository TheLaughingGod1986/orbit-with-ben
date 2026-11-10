#!/usr/bin/env python3
"""Build a 120-second proof using only genuine moving footage.

The hook and post-brand narration are separate ElevenLabs generations, so the
two-second ident cannot interrupt a spoken sentence.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
POLISHED = ROOT / "04_Generated-Clips/03_Polished"
RIG = Path("/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v03/loops")
HOOK = ROOT / "02_Voiceover/04_Section-Exports/aliens_vo_bold-v07_hook_ivc_kDch_v01.mp3"
POST = ROOT / "02_Voiceover/04_Section-Exports/aliens_vo_bold-v07_section-01_post-brand_ivc_kDch_v01.mp3"
BRAND = POLISHED / "brand/orbit_brand_intro_bold-v05_2s.mp4"
MUSIC = ROOT / "05_Music/aliens_score_cinematic_v19.wav"
CHIME = ROOT / "06_Sound-Effects/sfx_brand_chime_v11.wav"
OUT = ROOT / "09_Final-Export/aliens_v07c_PROFESSIONAL_MOTION_PROOF_120s.mp4"
PROOF_VOICE = ROOT / "02_Voiceover/05_Master/aliens_voiceover_bold-v07_motion-proof.wav"

FPS = 30
TOTAL = 120.0
HOOK_DURATION = 16.614
BRAND_DURATION = 2.0

# Every source appears exactly once. Durations deliberately follow the
# narration: possibility -> silence -> distance -> travel -> galactic scale.
SEGMENTS = [
    ("broll/aliens_scene-001_v01.mp4", 6.000),
    ("broll/aliens_scene-002_v01.mp4", 5.500),
    ("broll/aliens_scene-013_v01.mp4", 5.114),
    ("__BRAND__", 2.000),
    ("broll/aliens_scene-006_v01.mp4", 6.500),
    ("broll/aliens_scene-008_v01.mp4", 6.500),
    ("broll_mystery/mystery_A5_silence-void_v01_v01.mp4", 6.500),
    ("broll/aliens_scene-021_v01.mp4", 6.500),
    ("broll/aliens_scene-020_v01.mp4", 6.500),
    ("broll/aliens_scene-055_v01.mp4", 6.500),
    ("broll/aliens_scene-046_v01.mp4", 6.500),
    ("broll/aliens_scene-011_v01.mp4", 6.500),
    ("broll/aliens_scene-030_v01.mp4", 6.500),
    ("broll/aliens_scene-060_v01.mp4", 6.500),
    ("broll/aliens_scene-012_v01.mp4", 6.500),
    ("broll/aliens_scene-050_v01.mp4", 6.500),
    ("broll/aliens_scene-017_v01.mp4", 6.500),
    ("broll/aliens_scene-038_v01.mp4", 6.500),
    ("broll/aliens_scene-065_v01.mp4", 6.500),
    ("broll/aliens_scene-061_v01.mp4", 3.886),
]

ORBIT_APPEARANCES = [
    (18.614, "orbit_wave-camera_animated-blink_6s_v01.mov"),
    (38.114, "orbit_thinking-left_animated-blink_6s_v01.mov"),
    (57.614, "orbit_present-left_animated-blink_6s_v01.mov"),
    (77.114, "orbit_amazed_animated-blink_6s_v01.mov"),
    (103.114, "orbit_neutral-left_animated-blink_6s_v01.mov"),
]


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nk=1:nw=1", str(path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return float(result.stdout.strip())


def render_moving_source(source: Path, output: Path, target: float) -> None:
    source_duration = duration(source)
    stretch = target / source_duration
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(source), "-an",
        "-vf",
        (
            "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,"
            "crop=1920:1080,"
            f"setpts={stretch:.8f}*PTS,"
            f"fps={FPS},trim=duration={target:.6f},"
            "setpts=PTS-STARTPTS,format=yuv420p"
        ),
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-r", str(FPS), str(output),
    ])


def make_voice(work: Path) -> Path:
    silence = work / "brand_silence.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", f"{BRAND_DURATION:.3f}", "-c:a", "pcm_s24le", str(silence),
    ])
    hook_wav = work / "hook.wav"
    post_wav = work / "post.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(HOOK), "-af", f"atrim=duration={HOOK_DURATION:.6f}",
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le", str(hook_wav),
    ])
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(POST), "-t", f"{TOTAL - HOOK_DURATION - BRAND_DURATION:.6f}",
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le", str(post_wav),
    ])
    concat = work / "voice_concat.txt"
    concat.write_text(
        f"file '{hook_wav}'\nfile '{silence}'\nfile '{post_wav}'\n"
    )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(concat),
        "-af", "highpass=f=65,lowpass=f=15800,loudnorm=I=-17:LRA=7:TP=-1.5",
        "-t", f"{TOTAL:.3f}", "-ar", "48000", "-ac", "2",
        "-c:a", "pcm_s24le", str(PROOF_VOICE),
    ])
    return PROOF_VOICE


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    PROOF_VOICE.parent.mkdir(parents=True, exist_ok=True)
    assert abs(sum(value for _, value in SEGMENTS) - TOTAL) < 0.001
    assert len({name for name, _ in SEGMENTS}) == len(SEGMENTS)

    with tempfile.TemporaryDirectory(prefix="orbit_v07_motion_") as temp:
        work = Path(temp)
        rendered: list[Path] = []
        for index, (name, target) in enumerate(SEGMENTS):
            source = BRAND if name == "__BRAND__" else POLISHED / name
            part = work / f"part_{index:02d}.mp4"
            render_moving_source(source, part, target)
            rendered.append(part)

        concat = work / "video_concat.txt"
        concat.write_text("".join(f"file '{part}'\n" for part in rendered))
        bed = work / "moving_bed.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat),
            "-c", "copy", str(bed),
        ])

        command = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(bed),
        ]
        for _, loop_name in ORBIT_APPEARANCES:
            command += ["-i", str(RIG / loop_name)]
        command += [
            "-i", str(make_voice(work)),
            "-stream_loop", "-1", "-i", str(MUSIC),
            "-i", str(CHIME),
        ]

        filters: list[str] = []
        previous = "0:v"
        for input_index, (start, _) in enumerate(ORBIT_APPEARANCES, start=1):
            filters.append(
                f"[{input_index}:v]trim=duration=6,"
                "scale=522:387:flags=lanczos,"
                "fade=t=in:st=0:d=0.3:alpha=1,"
                "fade=t=out:st=5.7:d=0.3:alpha=1,"
                f"setpts=PTS-STARTPTS+{start:.6f}/TB[o{input_index}]"
            )
            output_label = f"v{input_index}"
            filters.append(
                f"[{previous}][o{input_index}]overlay=x=1360:y=650:"
                f"enable='between(t,{start:.6f},{start + 6:.6f})':"
                f"format=auto[{output_label}]"
            )
            previous = output_label

        voice_index = 1 + len(ORBIT_APPEARANCES)
        music_index = voice_index + 1
        chime_index = music_index + 1
        filters += [
            f"[{voice_index}:a]volume=1.0[vo]",
            f"[{music_index}:a]atrim=duration={TOTAL},volume=0.075,"
            "afade=t=in:st=0:d=2,afade=t=out:st=116:d=4[music]",
            f"[{chime_index}:a]atrim=duration=2,volume=0.28,"
            f"adelay={round(HOOK_DURATION * 1000)}|{round(HOOK_DURATION * 1000)}[chime]",
            "[vo][music][chime]amix=inputs=3:duration=first:normalize=0,"
            "alimiter=limit=0.92[aout]",
        ]
        command += [
            "-filter_complex", ";".join(filters),
            "-map", f"[{previous}]", "-map", "[aout]",
            "-t", f"{TOTAL:.3f}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", str(OUT),
        ]
        run(command)

    print(OUT)


if __name__ == "__main__":
    main()
