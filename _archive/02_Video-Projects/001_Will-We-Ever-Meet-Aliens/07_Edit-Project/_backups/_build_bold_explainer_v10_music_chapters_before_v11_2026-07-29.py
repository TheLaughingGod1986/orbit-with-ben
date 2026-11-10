#!/usr/bin/env python3
"""Bold Explainer v10 — animated beds + chapter cards + cinematic music.

Preserves approved Bold v06 timeline timing and Overlay-Rig Orbit choreography.
Adds:
  - Seedance beds when available (smooth pan fallback otherwise)
  - Chapter intro cards at major board starts (polished v02/v01 cards)
  - Remixed cinematic music bed + chapter whooshes under narration
"""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
TIMELINE = ROOT / "07_Edit-Project/bold-explainer-v06-final-timeline.json"
ANIMATED = ROOT / "04_Generated-Clips/03_Polished/bold_rebuild_v05/animated"
CHAPTERS = ROOT / "04_Generated-Clips/03_Polished/chapter_cards"
BRAND_INTRO = ROOT / "04_Generated-Clips/03_Polished/brand/orbit_brand_intro_bold-v05_2s.mp4"
BRAND_FALLBACK = ROOT / "04_Generated-Clips/03_Polished/brand/orbit_brand_intro_v03_free.png"
BRAND = BRAND_INTRO  # preferred; render_brand falls back to PNG if missing
RIG = Path("/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v03/loops")

MASTER_VOICE = ROOT / "02_Voiceover/05_Master/aliens_voiceover_bold-v06_ivc_kDch_master.wav"
MUSIC_A = ROOT / "05_Music/aliens_score_cinematic_v19.wav"
MUSIC_B = ROOT / "05_Music/aliens_score_ambient_v16.wav"
SFX = ROOT / "06_Sound-Effects"
SFX_BED = SFX / "aliens_sfx_bed_v19.wav"
SPACE_AMBIENCE = SFX / "aliens_space_ambience_v19.wav"
CHAPTER_WHOOSH = SFX / "sfx_whoosh_v19.wav"
SHIMMER = SFX / "sfx_shimmer_v19.wav"
BRAND_CHIME = SFX / "sfx_brand_chime_v11.wav"

OUT = ROOT / "09_Final-Export/aliens_BOLD_EXPLAINER_v10_MUSIC_CHAPTERS_MASTER.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v10_PROOF_music_chapters_90s.mp4"
CHAPTER_PROOF = ROOT / "09_Final-Export/aliens_v10_PROOF_chapter_cards_45s.mp4"
MANIFEST = ROOT / "07_Edit-Project/bold-explainer-v10-music-chapters-timeline.json"

FPS = 30
BRAND_HOLD = 2.0
TWO_PANEL_ORBIT = {2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 16, 17, 19, 21, 22, 24}
CHAPTER_AT_BOARD = {
    1: "chapter_01_01_cold-open_v01.mp4",
    2: "chapter_02_02_galaxy-scale_v01.mp4",
    4: "chapter_04_04_fermi-paradox_v01.mp4",
    5: "chapter_03_03_exoplanets_v01.mp4",
    7: "chapter_06_06_explanations_v01.mp4",
    10: "chapter_05_05_great-filter_v01.mp4",
    16: "chapter_07_07_detection_v01.mp4",
    21: "chapter_08_08_first-contact_v01.mp4",
    24: "chapter_09_09_conclusion_v01.mp4",
}


def run(args: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, capture_output=capture)


def probe_duration(path: Path) -> float:
    result = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nk=1:nw=1", str(path),
    ], capture=True)
    return float(result.stdout.strip())


def animated_for_png(png_path: Path) -> Path | None:
    candidate = ANIMATED / f"{Path(png_path).stem}_seedance-mini.mp4"
    if candidate.exists() and candidate.stat().st_size > 100_000:
        return candidate
    return None


def render_seedance_once(source: Path, output: Path, duration: float) -> None:
    """Play Seedance once at native timing — never stream_loop / restart motion."""
    play = min(probe_duration(source), duration)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(source), "-an",
        "-vf",
        (
            "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,"
            "crop=1920:1080,"
            f"fps={FPS},trim=duration={play:.6f},setpts=PTS-STARTPTS,"
            "eq=saturation=1.02:contrast=1.01,format=yuv420p"
        ),
        "-frames:v", str(max(1, round(play * FPS))),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", str(output),
    ])


def render_seedance_bed(
    source: Path,
    png: Path,
    output: Path,
    duration: float,
    scene_number: int,
) -> None:
    """No-repeat bed: Seedance once, then unique still-board pan for leftover VO time."""
    source_duration = probe_duration(source)
    play = min(source_duration, duration)
    leftover = duration - play
    if leftover <= 0.05:
        render_seedance_once(source, output, duration)
        return
    work = output.parent
    seed = work / f"{output.stem}_seed_once.mp4"
    still = work / f"{output.stem}_still_fill.mp4"
    render_seedance_once(source, seed, play)
    render_smooth_still_bed(png, still, leftover, scene_number)
    concat_two(seed, still, output)


def render_smooth_still_bed(png: Path, output: Path, duration: float, scene_number: int) -> None:
    frames = max(1, round(duration * FPS))
    direction = scene_number % 4
    if direction == 0:
        x_expr = f"(iw-ow)*t/{duration:.6f}"
        y_expr = "(ih-oh)/2"
    elif direction == 1:
        x_expr = f"(iw-ow)*(1-t/{duration:.6f})"
        y_expr = "(ih-oh)/2"
    elif direction == 2:
        x_expr = "(iw-ow)/2"
        y_expr = f"(ih-oh)*t/{duration:.6f}"
    else:
        x_expr = "(iw-ow)/2"
        y_expr = f"(ih-oh)*(1-t/{duration:.6f})"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(png), "-an",
        "-vf",
        (
            "scale=2112:1188:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop=1920:1080:x='{x_expr}':y='{y_expr}',"
            f"fps={FPS},trim=duration={duration:.6f},setpts=PTS-STARTPTS,"
            "eq=saturation=1.03:contrast=1.015,format=yuv420p"
        ),
        "-frames:v", str(frames),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", str(output),
    ])


def render_video_bed(source: Path, output: Path, duration: float) -> None:
    """Play a video plate once. Pad with last frame only if needed for exact edit length
    of non-scenery assets (brand). Scenery must use render_seedance_bed instead.
    """
    source_duration = max(0.1, probe_duration(source))
    play = min(source_duration, duration)
    pad = max(0.0, duration - play)
    vf = (
        "scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0B0810,"
        f"fps={FPS},trim=duration={play:.6f},setpts=PTS-STARTPTS,format=yuv420p"
    )
    if pad > 0.05:
        vf += f",tpad=stop_mode=clone:stop_duration={pad:.6f}"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(source), "-an",
        "-vf", vf,
        "-frames:v", str(max(1, round(duration * FPS))),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
        "-pix_fmt", "yuv420p", str(output),
    ])


def chapter_png_for(chapter_mp4_name: str) -> Path | None:
    """Map chapter_02_…_v01.mp4 → chapter_02_….png (locked still source)."""
    stem = Path(chapter_mp4_name).stem
    for suffix in ("_v02", "_v01"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    png = CHAPTERS / f"{stem}.png"
    return png if png.exists() else None


def render_chapter_bed(chapter_mp4_name: str, output: Path, duration: float) -> None:
    """Locked chapter card — prefer PNG still (no fades / no re-encode jitter)."""
    png = chapter_png_for(chapter_mp4_name)
    if png is not None:
        frames = max(1, round(duration * FPS))
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-framerate", str(FPS), "-i", str(png), "-an",
            "-vf", f"scale=1920:1080:flags=neighbor,fps={FPS},format=yuv420p",
            "-frames:v", str(frames),
            "-c:v", "libx264", "-tune", "stillimage", "-preset", "veryfast", "-crf", "14",
            "-x264-params", "keyint=1:min-keyint=1:scenecut=0:bframes=0",
            "-pix_fmt", "yuv420p", str(output),
        ])
        return
    mp4 = CHAPTERS / chapter_mp4_name
    if not mp4.exists():
        raise SystemExit(f"Missing chapter card: {chapter_mp4_name}")
    render_video_bed(mp4, output, duration)


def render_brand(output: Path) -> None:
    """Post-hook brand: prefer animated intro MP4; fall back to still PNG."""
    if BRAND_INTRO.exists():
        render_video_bed(BRAND_INTRO, output, BRAND_HOLD)
        return
    frames = round(BRAND_HOLD * FPS)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(BRAND_FALLBACK), "-an",
        "-vf",
        (
            "scale=1920:1080:flags=lanczos,"
            "fade=t=in:st=0:d=0.18,fade=t=out:st=1.82:d=0.18,"
            "format=yuv420p"
        ),
        "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "15", "-pix_fmt", "yuv420p", str(output),
    ])


def concat_two(a: Path, b: Path, output: Path) -> None:
    lst = output.with_suffix(".txt")
    lst.write_text(f"file '{a}'\nfile '{b}'\n")
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c", "copy", str(output),
    ])


def orbit_meta(pose_name: str | None, scene_number: int) -> tuple[Path | None, bool, bool]:
    if not pose_name or pose_name == "brand-card":
        return None, False, False
    board = (scene_number - 1) // 4 + 1
    panel = (scene_number - 1) % 4 + 1
    chosen = (2, 3) if board in TWO_PANEL_ORBIT else (3,)
    return RIG / pose_name, panel == chosen[0], panel == chosen[-1]


def overlay_orbit(
    bed: Path,
    output: Path,
    orbit: Path | None,
    duration: float,
    timeline_start: float,
    fade_in: bool,
    fade_out: bool,
) -> None:
    if orbit is None or not orbit.exists():
        run(["cp", str(bed), str(output)])
        return
    filters = [
        "[0:v]format=yuv420p[bg]",
        f"[1:v]trim=duration={duration:.4f},setpts=PTS-STARTPTS",
    ]
    if fade_in:
        filters[-1] += ",fade=t=in:st=0:d=0.35:alpha=1"
    if fade_out:
        filters[-1] += f",fade=t=out:st={max(0.0, duration - 0.35):.4f}:d=0.35:alpha=1"
    filters[-1] += "[orbit]"
    filters.append(
        "[bg][orbit]overlay=x=1300:y='625+8*sin(2*PI*t/4.8)':format=auto[v]"
    )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(bed),
        "-stream_loop", "-1", "-ss", f"{timeline_start % 6:.3f}", "-i", str(orbit),
        "-filter_complex", ";".join(filters),
        "-map", "[v]", "-an",
        "-frames:v", str(max(1, round(duration * FPS))),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", str(output),
    ])


def build_audio_mix(work: Path, duration: float, chapter_times: list[float]) -> Path:
    """VO + present cinematic bed (ducked) + soft SFX + chapter whooshes."""
    bed = work / "music-bed.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(MUSIC_A), "-i", str(MUSIC_B),
        "-filter_complex",
        (
            "[0:a]atrim=0:635.475,asetpts=PTS-STARTPTS[a0];"
            "[1:a]atrim=0:635.475,asetpts=PTS-STARTPTS[a1];"
            "[a0][a1]acrossfade=d=4:c1=tri:c2=tri,"
            f"aloop=loop=-1:size=2e9,atrim=duration={duration:.6f},"
            "volume=0.105[bed]"
        ),
        "-map", "[bed]", "-ar", "48000", "-ac", "2",
        "-c:a", "pcm_s24le", str(bed),
    ])

    # Delayed whooshes / shimmer / brand chime
    whoosh_labels = []
    filters = [
        f"[0:a]atrim=duration={duration:.6f},volume=0.016[space]",
        f"[1:a]atrim=duration={duration:.6f},volume=0.010[texture]",
    ]
    inputs = ["-i", str(SPACE_AMBIENCE), "-i", str(SFX_BED), "-i", str(CHAPTER_WHOOSH), "-i", str(SHIMMER), "-i", str(BRAND_CHIME)]
    mix_names = ["space", "texture"]

    for idx, t in enumerate(chapter_times):
        delay_ms = max(0, int(round(t * 1000)))
        name = f"whoosh{idx}"
        filters.append(
            f"[2:a]volume=0.20,adelay={delay_ms}|{delay_ms}[{name}]"
        )
        whoosh_labels.append(name)
        mix_names.append(name)

    # Soft shimmer after first chapter + near end
    for idx, t in enumerate([chapter_times[0] + 6.0 if chapter_times else 20.0, max(0.0, duration - 28.0)]):
        delay_ms = max(0, int(round(t * 1000)))
        name = f"shim{idx}"
        filters.append(f"[3:a]volume=0.08,adelay={delay_ms}|{delay_ms}[{name}]")
        mix_names.append(name)

    # Brand chime near post-hook brand (~board1 end / brand card)
    brand_t = next((c for c in chapter_times if c > 5), 12.0)
    filters.append(f"[4:a]volume=0.16,adelay={int(brand_t*1000)}|{int(brand_t*1000)}[chime]")
    mix_names.append("chime")

    filters.append(
        "".join(f"[{n}]" for n in mix_names)
        + f"amix=inputs={len(mix_names)}:normalize=0,alimiter=limit=0.90:level=false[fx]"
    )
    effects = work / "effects.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        *inputs,
        "-filter_complex", ";".join(filters),
        "-map", "[fx]", "-ar", "48000", "-ac", "2",
        "-t", f"{duration:.6f}",
        "-c:a", "pcm_s24le", str(effects),
    ])

    final_audio = work / "final-audio.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(MASTER_VOICE), "-i", str(bed), "-i", str(effects),
        "-filter_complex",
        (
            f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"apad=whole_dur={duration:.6f},atrim=0:{duration:.6f}[vo];"
            "[1:a][vo]sidechaincompress=threshold=0.022:ratio=7:"
            "attack=14:release=380[duckedmusic];"
            "[2:a][vo]sidechaincompress=threshold=0.018:ratio=5:"
            "attack=10:release=260[duckedfx];"
            "[vo][duckedmusic][duckedfx]"
            "amix=inputs=3:weights='1 0.62 0.70':normalize=0,"
            "volume=-0.5dB,alimiter=limit=0.88:level=false[a]"
        ),
        "-map", "[a]", "-ar", "48000", "-ac", "2",
        "-t", f"{duration:.6f}",
        "-c:a", "pcm_s24le", str(final_audio),
    ])
    return final_audio


def render_scene(item: dict, work: Path) -> tuple[Path, dict]:
    asset = item["asset_id"]
    duration = float(item["duration"])
    start = float(item["start"])
    meta = {**item}

    if asset == "brand-card":
        out = work / "brand.mp4"
        render_brand(out)
        meta["kind"] = "brand"
        return out, meta

    scene_number = int(asset.split("-")[1])
    board = (scene_number - 1) // 4 + 1
    panel = (scene_number - 1) % 4 + 1
    final = work / f"{asset}_final.mp4"

    chapter_name = CHAPTER_AT_BOARD.get(board) if panel == 1 else None
    chapter_dur = 0.0
    if chapter_name and (CHAPTERS / chapter_name).exists():
        chapter_dur = min(probe_duration(CHAPTERS / chapter_name), max(2.2, duration * 0.30), duration - 1.4)
        chapter_dur = max(0.0, chapter_dur)

    remaining = duration - chapter_dur
    png = Path(item["source"])
    scene_bed = work / f"{asset}_scenebed.mp4"
    animated = animated_for_png(png)
    if animated is not None:
        render_seedance_bed(animated, png, scene_bed, remaining, scene_number)
        meta["kind"] = "seedance"
        meta["motion_source"] = str(animated)
        meta["seedance_policy"] = "play_once_then_unique_still_fill"
    else:
        render_smooth_still_bed(png, scene_bed, remaining, scene_number)
        meta["kind"] = "smooth-still"
        meta["motion_source"] = str(png)

    orbit, fade_in, fade_out = orbit_meta(item.get("orbit_pose"), scene_number)
    # Don't fade orbit in over a chapter card join
    if chapter_dur > 0.05:
        fade_in = False
    scene_final = work / f"{asset}_scene_final.mp4"
    overlay_orbit(scene_bed, scene_final, orbit, remaining, start + chapter_dur, fade_in, fade_out)
    if orbit:
        meta["orbit_pose"] = orbit.name

    if chapter_dur > 0.05:
        chap_part = work / f"{asset}_chapter.mp4"
        render_chapter_bed(chapter_name, chap_part, chapter_dur)
        concat_two(chap_part, scene_final, final)
        meta["chapter"] = chapter_name
        meta["chapter_duration"] = round(chapter_dur, 3)
    else:
        run(["cp", str(scene_final), str(final)])
    return final, meta


def main() -> None:
    required = [TIMELINE, MASTER_VOICE, MUSIC_A, MUSIC_B, SPACE_AMBIENCE, SFX_BED, CHAPTER_WHOOSH, SHIMMER, BRAND_CHIME]
    if not BRAND_INTRO.exists() and not BRAND_FALLBACK.exists():
        required.append(BRAND_FALLBACK)
    missing = [p for p in required if not p.exists()]
    if missing:
        raise SystemExit("Missing:\n" + "\n".join(str(p) for p in missing))

    timeline_doc = json.loads(TIMELINE.read_text())
    items = timeline_doc["timeline"]
    seedance_ready = len(list(ANIMATED.glob("scene-*_seedance-mini.mp4")))
    print(f"Seedance clips ready: {seedance_ready}/96", flush=True)

    with tempfile.TemporaryDirectory(prefix="orbit-bold-v10-") as temp:
        work = Path(temp)
        parts: list[Path] = []
        rebuilt: list[dict] = []
        chapter_times: list[float] = []
        seedance_count = 0
        chapters = 0

        for idx, item in enumerate(items, start=1):
            print(f"[{idx}/{len(items)}] {item['asset_id']} {float(item['duration']):.2f}s", flush=True)
            part, meta = render_scene(item, work)
            if meta.get("kind") == "seedance":
                seedance_count += 1
            if meta.get("chapter"):
                chapters += 1
                chapter_times.append(float(item["start"]))
            parts.append(part)
            rebuilt.append(meta)

        concat = work / "concat.txt"
        concat.write_text("".join(f"file '{p}'\n" for p in parts))
        silent = work / "silent.mp4"
        print("Concat picture…", flush=True)
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat),
            "-c", "copy", str(silent),
        ])
        pic_dur = probe_duration(silent)
        print(f"Picture duration: {pic_dur:.3f}s | chapters={chapters}", flush=True)

        print("Build music + whoosh mix…", flush=True)
        audio = build_audio_mix(work, pic_dur, chapter_times)

        print("Mux master…", flush=True)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(silent), "-i", str(audio),
            "-map", "0:v:0", "-map", "1:a:0", "-shortest",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-c:a", "aac", "-b:a", "256k",
            "-movflags", "+faststart", str(OUT),
        ])
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(OUT), "-t", "90",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", str(PROOF),
        ])
        # Chapter-focused proof: first chapter card region if available
        if chapter_times:
            start = max(0.0, chapter_times[0] - 1.0)
            run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", f"{start:.3f}", "-i", str(OUT), "-t", "45",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", str(CHAPTER_PROOF),
            ])

    manifest = {
        "version": "bold-explainer-v10-music-chapters",
        "based_on": str(TIMELINE),
        "output": str(OUT),
        "proof": str(PROOF),
        "chapter_proof": str(CHAPTER_PROOF),
        "duration": probe_duration(OUT),
        "seedance_count": seedance_count,
        "seedance_ready_at_build": seedance_ready,
        "chapter_cards_inserted": chapters,
        "chapter_times": chapter_times,
        "music": [str(MUSIC_A), str(MUSIC_B)],
        "timeline": rebuilt,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({
        "output": str(OUT),
        "proof": str(PROOF),
        "chapter_proof": str(CHAPTER_PROOF),
        "duration": manifest["duration"],
        "seedance_count": seedance_count,
        "chapters": chapters,
    }, indent=2))


if __name__ == "__main__":
    main()
