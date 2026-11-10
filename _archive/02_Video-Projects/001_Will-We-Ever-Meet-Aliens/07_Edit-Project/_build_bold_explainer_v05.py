#!/usr/bin/env python3
"""Build the narration-led, no-repeat Bold Explainer v05 review master."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
SCRIPT = ROOT / "01_Script/aliens_narration_bold_v05_18min.txt"
SCENES = ROOT / "04_Generated-Clips/03_Polished/bold_rebuild_v05/scenes"
BRAND = ROOT / "04_Generated-Clips/03_Polished/brand/orbit_brand_intro_v03_free.png"
RIG = Path("/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v03/loops")
VOICE = ROOT / "02_Voiceover/04_Section-Exports"
MASTER_VOICE = ROOT / "02_Voiceover/05_Master/aliens_voiceover_bold-v05_pvc_gentle-master.wav"
MUSIC_A = ROOT / "05_Music/aliens_score_cinematic_v19.wav"
MUSIC_B = ROOT / "05_Music/aliens_score_ambient_v16.wav"
OUT = ROOT / "09_Final-Export/aliens_BOLD_EXPLAINER_REBUILD_v05_review.mp4"
MANIFEST = ROOT / "07_Edit-Project/bold-explainer-v05-timeline.json"

VOICE_FILES = [
    VOICE / "aliens_vo_bold-v05_section-01_problem_pvc_raw_v02.mp3",
    VOICE / "aliens_vo_bold-v05_section-02_explanations_pvc_raw.mp3",
    VOICE / "aliens_vo_bold-v05_section-03_search_pvc_raw.mp3",
    VOICE / "aliens_vo_bold-v05_section-04_solution-cliffhanger_pvc_raw.mp3",
]

BOARD_LINES = [
    (1, 5), (7, 27), (29, 37), (39, 51), (53, 63), (65, 67),
    (69, 87), (89, 95), (97, 105), (107, 115), (117, 131), (133, 141),
    (143, 153), (155, 171), (173, 191), (193, 200), (201, 207),
    (209, 217), (219, 225), (227, 235), (237, 247), (249, 273),
    (275, 295), (297, 317),
]
SECTION_BOARDS = [range(1, 7), range(7, 14), range(14, 21), range(21, 25)]
SECTION_GAP = 0.55
BRAND_HOLD = 2.0
FPS = 30

TWO_PANEL_ORBIT = {
    2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 16, 17, 19, 21, 22, 24
}
POSES = [
    "orbit_present-left_animated-blink_6s_v01.mov",
    "orbit_thinking-left_animated-blink_6s_v01.mov",
    "orbit_amazed_animated-blink_6s_v01.mov",
    "orbit_neutral-left_animated-blink_6s_v01.mov",
    "orbit_wave-camera_animated-blink_6s_v01.mov",
]


def run(args: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        check=True,
        text=True,
        capture_output=capture,
    )


def probe_duration(path: Path) -> float:
    result = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nk=1:nw=1", str(path),
    ], capture=True)
    return float(result.stdout.strip())


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def script_line_words() -> list[int]:
    lines = SCRIPT.read_text().splitlines()
    return [
        sum(len(re.findall(r"\b[\w’'-]+\b", line)) for line in lines[start - 1:end])
        for start, end in BOARD_LINES
    ]


def detect_hook_split(audio: Path, expected: float) -> float:
    result = subprocess.run([
        "ffmpeg", "-hide_banner", "-i", str(audio), "-af",
        "silencedetect=noise=-36dB:d=0.20", "-f", "null", "-",
    ], text=True, capture_output=True)
    starts = [float(value) for value in re.findall(r"silence_start: ([0-9.]+)", result.stderr)]
    ends = [float(value) for value in re.findall(r"silence_end: ([0-9.]+)", result.stderr)]
    midpoints = [(a + b) / 2 for a, b in zip(starts, ends) if 8.0 <= (a + b) / 2 <= 30.0]
    if not midpoints:
        return expected
    return min(midpoints, key=lambda value: abs(value - expected))


def allocate_board_durations(section_durations: list[float], words: list[int]) -> list[float]:
    result = [0.0] * 24
    expected_hook = section_durations[0] * words[0] / sum(words[0:6])
    result[0] = detect_hook_split(VOICE_FILES[0], expected_hook)
    remaining = section_durations[0] - result[0]
    remaining_words = sum(words[1:6])
    for board in range(2, 7):
        result[board - 1] = remaining * words[board - 1] / remaining_words

    for section_index, boards in enumerate(SECTION_BOARDS[1:], start=1):
        board_list = list(boards)
        total_words = sum(words[board - 1] for board in board_list)
        for board in board_list:
            result[board - 1] = (
                section_durations[section_index] * words[board - 1] / total_words
            )

    for ending_board in (6, 13, 20):
        result[ending_board - 1] += SECTION_GAP
    return result


def make_audio_master(work: Path, split: float) -> None:
    wavs: list[Path] = []
    for index, source in enumerate(VOICE_FILES, start=1):
        wav = work / f"voice_{index:02d}.wav"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(source), "-ar", "48000", "-ac", "2",
            "-c:a", "pcm_s24le", str(wav),
        ])
        wavs.append(wav)

    first_with_brand_gap = work / "voice_01_brand-gap.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(wavs[0]),
        "-filter_complex",
        (
            f"[0:a]atrim=0:{split:.6f},asetpts=PTS-STARTPTS[pre];"
            f"anullsrc=r=48000:cl=stereo,atrim=duration={BRAND_HOLD:.3f}[gap];"
            f"[0:a]atrim=start={split:.6f},asetpts=PTS-STARTPTS[post];"
            "[pre][gap][post]concat=n=3:v=0:a=1[out]"
        ),
        "-map", "[out]", "-c:a", "pcm_s24le", str(first_with_brand_gap),
    ])
    wavs[0] = first_with_brand_gap

    silence = work / "section-gap.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", f"{SECTION_GAP:.3f}", "-c:a", "pcm_s24le", str(silence),
    ])
    concat_list = work / "voice-concat.txt"
    ordered = [wavs[0], silence, wavs[1], silence, wavs[2], silence, wavs[3]]
    concat_list.write_text("".join(f"file '{path}'\n" for path in ordered))
    unprocessed = work / "voice-unprocessed.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c:a", "pcm_s24le", str(unprocessed),
    ])
    MASTER_VOICE.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(unprocessed),
        "-af",
        "highpass=f=68,"
        "equalizer=f=100:width_type=q:width=12:g=-8,"
        "equalizer=f=200:width_type=q:width=12:g=-4,"
        "afftdn=nf=-48:nr=7:tn=1,lowpass=f=15500,"
        "loudnorm=I=-17:LRA=7:TP=-1.5",
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le", str(MASTER_VOICE),
    ])


def orbit_for_scene(scene_number: int) -> tuple[Path | None, bool, bool]:
    board = (scene_number - 1) // 4 + 1
    panel = (scene_number - 1) % 4 + 1
    if board == 1:
        return None, False, False
    chosen = (2, 3) if board in TWO_PANEL_ORBIT else (3,)
    if panel not in chosen:
        return None, False, False
    pose = RIG / POSES[(board - 2) % len(POSES)]
    return pose, panel == chosen[0], panel == chosen[-1]


def render_scene(
    source: Path,
    output: Path,
    duration: float,
    scene_number: int,
    timeline_start: float,
) -> None:
    frames = max(1, round(duration * FPS))
    direction = scene_number % 4
    zoom = (
        "min(1.085,1+0.00016*on)" if direction in (0, 1)
        else "max(1.0,1.085-0.00016*on)"
    )
    x = {
        0: "(iw-iw/zoom)/2",
        1: "0",
        2: "iw-iw/zoom",
        3: "(iw-iw/zoom)/2",
    }[direction]
    y = "(ih-ih/zoom)/2"
    background = (
        "scale=2200:1238:force_original_aspect_ratio=increase:flags=lanczos,"
        "crop=2200:1238,"
        f"zoompan=z='{zoom}':x='{x}':y='{y}':d=1:s=1920x1080:fps={FPS},"
        "eq=saturation=1.03:contrast=1.015,format=yuv420p"
    )
    orbit, fade_in, fade_out = orbit_for_scene(scene_number)
    command = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(source),
    ]
    if orbit is None:
        command += [
            "-an", "-vf", background, "-frames:v", str(frames),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
            "-pix_fmt", "yuv420p", str(output),
        ]
    else:
        command += ["-stream_loop", "-1", "-ss", f"{timeline_start % 6:.3f}", "-i", str(orbit)]
        orbit_filters = [
            f"[0:v]{background}[bg]",
            f"[1:v]trim=duration={duration:.4f},setpts=PTS-STARTPTS",
        ]
        if fade_in:
            orbit_filters[-1] += ",fade=t=in:st=0:d=0.35:alpha=1"
        if fade_out:
            orbit_filters[-1] += f",fade=t=out:st={max(0.0, duration - 0.35):.4f}:d=0.35:alpha=1"
        orbit_filters[-1] += "[orbit]"
        orbit_filters.append(
            "[bg][orbit]overlay=x=1300:y='625+8*sin(2*PI*t/4.8)':format=auto[v]"
        )
        command += [
            "-filter_complex", ";".join(orbit_filters), "-map", "[v]", "-an",
            "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "17", "-pix_fmt", "yuv420p", str(output),
        ]
    run(command)


def render_brand(output: Path) -> None:
    frames = round(BRAND_HOLD * FPS)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(BRAND), "-an",
        "-vf",
        (
            "scale=1920:1080:flags=lanczos,"
            "fade=t=in:st=0:d=0.18,fade=t=out:st=1.82:d=0.18,"
            "format=yuv420p"
        ),
        "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "15", "-pix_fmt", "yuv420p", str(output),
    ])


def build_music_mix(work: Path, duration: float) -> Path:
    bed = work / "music-bed.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(MUSIC_A), "-i", str(MUSIC_B),
        "-filter_complex",
        (
            "[0:a]atrim=0:635.475,asetpts=PTS-STARTPTS[a0];"
            "[1:a]atrim=0:635.475,asetpts=PTS-STARTPTS[a1];"
            "[a0][a1]acrossfade=d=4:c1=tri:c2=tri,"
            f"atrim=duration={duration:.6f},volume=0.075[bed]"
        ),
        "-map", "[bed]", "-ar", "48000", "-ac", "2",
        "-c:a", "pcm_s24le", str(bed),
    ])
    final_audio = work / "final-audio.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(MASTER_VOICE), "-i", str(bed),
        "-filter_complex",
        (
            "[1:a][0:a]sidechaincompress=threshold=0.025:ratio=8:"
            "attack=12:release=350[ducked];"
            "[0:a][ducked]amix=inputs=2:weights='1 0.55':normalize=0,"
            "volume=-0.8dB,alimiter=limit=0.87:level=false[a]"
        ),
        "-map", "[a]", "-ar", "48000", "-ac", "2",
        "-c:a", "pcm_s24le", str(final_audio),
    ])
    return final_audio


def main() -> None:
    missing = [path for path in [SCRIPT, BRAND, MUSIC_A, MUSIC_B, *VOICE_FILES] if not path.exists()]
    if missing:
        raise SystemExit("Missing required inputs:\n" + "\n".join(str(path) for path in missing))

    scene_files = sorted(SCENES.glob("scene-*.png"))
    if len(scene_files) != 96:
        raise SystemExit(f"Expected 96 scenes, found {len(scene_files)}")
    hashes = [file_hash(path) for path in scene_files]
    if len(set(hashes)) != len(hashes):
        raise SystemExit("Duplicate scene source detected; build refused")

    section_durations = [probe_duration(path) for path in VOICE_FILES]
    words = script_line_words()
    board_durations = allocate_board_durations(section_durations, words)
    hook_split = board_durations[0]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="orbit-bold-v05-") as temp:
        work = Path(temp)
        make_audio_master(work, hook_split)
        brand = work / "brand.mp4"
        render_brand(brand)
        scene_parts: list[Path] = []
        timeline: list[dict[str, object]] = []
        cursor = 0.0
        for board in range(1, 25):
            panel_duration = board_durations[board - 1] / 4
            for panel in range(1, 5):
                scene_number = (board - 1) * 4 + panel
                source = scene_files[scene_number - 1]
                part = work / f"scene-{scene_number:03d}.mp4"
                render_scene(source, part, panel_duration, scene_number, cursor)
                scene_parts.append(part)
                orbit, _, _ = orbit_for_scene(scene_number)
                timeline.append({
                    "asset_id": f"scene-{scene_number:03d}",
                    "board": board,
                    "source": str(source),
                    "sha256": hashes[scene_number - 1],
                    "start": round(cursor, 3),
                    "end": round(cursor + panel_duration, 3),
                    "duration": round(panel_duration, 3),
                    "orbit_pose": orbit.name if orbit else None,
                })
                cursor += panel_duration
            if board == 1:
                timeline.append({
                    "asset_id": "brand-card",
                    "source": str(BRAND),
                    "start": round(cursor, 3),
                    "end": round(cursor + BRAND_HOLD, 3),
                    "duration": BRAND_HOLD,
                    "orbit_pose": "brand-card",
                })
                cursor += BRAND_HOLD

        concat_list = work / "video-concat.txt"
        concat_list.write_text("".join(f"file '{path}'\n" for path in scene_parts))
        silent_video = work / "silent-video.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat_list),
            "-c", "copy", str(silent_video),
        ])

        voice_duration = probe_duration(MASTER_VOICE)
        silent_video_with_brand = work / "silent-video-with-brand.mp4"
        source_video_duration = probe_duration(silent_video)
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(silent_video), "-i", str(brand),
            "-filter_complex",
            (
                f"[0:v]trim=start=0:end={hook_split:.6f},setpts=PTS-STARTPTS[pre];"
                f"[1:v]trim=start=0:end={BRAND_HOLD:.6f},setpts=PTS-STARTPTS[brand];"
                f"[0:v]trim=start={hook_split:.6f}:end={source_video_duration:.6f},"
                "setpts=PTS-STARTPTS[post];"
                "[pre][brand][post]concat=n=3:v=1:a=0[v]"
            ),
            "-map", "[v]", "-an", "-r", str(FPS),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", str(silent_video_with_brand),
        ])
        final_audio = build_music_mix(work, voice_duration)
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(silent_video_with_brand), "-i", str(final_audio),
            "-map", "0:v:0", "-map", "1:a:0", "-shortest",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
            "-movflags", "+faststart", str(OUT),
        ])

    manifest = {
        "version": "bold-explainer-v05",
        "narration_led": True,
        "brand_after_hook_seconds": round(hook_split, 3),
        "brand_hold_seconds": BRAND_HOLD,
        "voice_sections": [str(path) for path in VOICE_FILES],
        "master_voice": str(MASTER_VOICE),
        "output": str(OUT),
        "scene_count": 96,
        "duplicate_scene_hashes": 0,
        "orbit_scene_count": sum(1 for item in timeline if item.get("orbit_pose") not in (None, "brand-card")),
        "timeline": timeline,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({
        "output": str(OUT),
        "duration": probe_duration(OUT),
        "scene_count": 96,
        "orbit_scene_count": manifest["orbit_scene_count"],
        "manifest": str(MANIFEST),
    }, indent=2))


if __name__ == "__main__":
    main()
