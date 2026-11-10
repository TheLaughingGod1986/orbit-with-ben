#!/usr/bin/env python3
"""Bold Explainer v09 — final polish master.

Fixes / adds:
  - Remove left→right white sweep bar
  - Reliable post-hook brand bumper (bold animated logo)
  - Chapter intro cards at major board starts (duration-preserving)
  - Like & subscribe outro + existing CTA voiceover
  - Seedance beds when available; smooth locked pan otherwise
  - Stronger Orbit presence (soft-shadow host + in-scene beats)
"""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
TIMELINE = ROOT / "07_Edit-Project/bold-explainer-v06-final-timeline.json"
ANIMATED = ROOT / "04_Generated-Clips/03_Polished/bold_rebuild_v05/animated"
SCENES = ROOT / "04_Generated-Clips/03_Polished/bold_rebuild_v05/scenes"
CHAPTERS = ROOT / "04_Generated-Clips/03_Polished/chapter_cards"
BRAND_INTRO = ROOT / "04_Generated-Clips/03_Polished/brand/orbit_brand_intro_bold-v05_2s.mp4"
BRAND_FALLBACK = ROOT / "04_Generated-Clips/03_Polished/brand/orbit_brand_intro_v03_free.png"
BRAND_OUTRO = ROOT / "04_Generated-Clips/03_Polished/brand/orbit_brand_outro_subscribe_v01.mp4"
END_SCREEN = ROOT / "08_Thumbnail/aliens_v10_like_subscribe_end-screen.png"
LOOPS = ROOT / "04_Generated-Clips/03_Polished/orbit_narrator/rgba/loops_polished_v25"
INSCENE = {
    "explain": ROOT / "04_Generated-Clips/03_Polished/orbit_explaining_talk_v01_polished.mp4",
    "surprise": ROOT / "04_Generated-Clips/03_Polished/orbit_surprised_reaction_v01_polished.mp4",
    "ending": ROOT / "04_Generated-Clips/03_Polished/orbit_ending_goodbye_v01_polished.mp4",
}
CTA_VO = ROOT / "02_Voiceover/04_Section-Exports/aliens_vo_section-10_cta_subscribe_v02.wav"
AUDIO_MASTER = ROOT / "09_Final-Export/aliens_BOLD_EXPLAINER_v06_FINAL_POLISHED_MASTER.mp4"
MUSIC_A = ROOT / "05_Music/aliens_score_cinematic_v19.wav"

OUT = ROOT / "09_Final-Export/aliens_BOLD_EXPLAINER_v09_FINAL_POLISHED_MASTER.mp4"
OUT_ALIAS = ROOT / "09_Final-Export/aliens_v15_FULL_INTEGRATED_CONCEPT_MASTER.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v09_PROOF_final_polish_90s.mp4"
MANIFEST = ROOT / "07_Edit-Project/bold-explainer-v09-final-timeline.json"

FPS = 30
OUTRO_HOLD = 10.0
ORBIT_H = 580
ORBIT_X = 1220
ORBIT_Y = 430
ORBIT_PANELS = (1, 2, 3)
POSE_CYCLE = [
    "orbit_present_idle.mov",
    "orbit_thinking_idle.mov",
    "orbit_amazed_idle.mov",
    "orbit_neutral_idle.mov",
    "orbit_wave_idle.mov",
    "orbit_present_talk.mov",
    "orbit_thinking_talk.mov",
]
INSCENE_BEATS = {
    "scene-005": "explain",
    "scene-016": "surprise",
    "scene-068": "surprise",
    "scene-095": "ending",
    "scene-096": "ending",
}
# Replace opening moments of these boards with chapter cards (audio-safe)
CHAPTER_AT_BOARD = {
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


def render_seedance_bed(source: Path, output: Path, duration: float) -> None:
    source_duration = probe_duration(source)
    loops = max(1, int(duration // source_duration) + 2)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-stream_loop", str(loops), "-i", str(source), "-an",
        "-vf",
        (
            "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,"
            "crop=1920:1080,"
            f"fps={FPS},trim=duration={duration:.6f},setpts=PTS-STARTPTS,"
            "eq=saturation=1.03:contrast=1.01,format=yuv420p"
        ),
        "-frames:v", str(max(1, round(duration * FPS))),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", str(output),
    ])


def render_smooth_still_bed(png: Path, output: Path, duration: float, scene_number: int) -> None:
    """Locked smooth pan — NO sweep bar."""
    frames = max(1, round(duration * FPS))
    direction = scene_number % 4
    if direction == 0:
        x_expr, y_expr = f"(iw-ow)*t/{duration:.6f}", "0"
    elif direction == 1:
        x_expr, y_expr = f"(iw-ow)*(1-t/{duration:.6f})", "0"
    elif direction == 2:
        x_expr, y_expr = "0", f"(ih-oh)*t/{duration:.6f}"
    else:
        x_expr, y_expr = "(iw-ow)/2", f"(ih-oh)*(1-t/{duration:.6f})"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(png), "-an",
        "-vf",
        (
            "scale=2100:1180:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop=1920:1080:x='{x_expr}':y='{y_expr}',"
            f"fps={FPS},trim=duration={duration:.6f},setpts=PTS-STARTPTS,"
            "eq=saturation=1.04:contrast=1.02,"
            "noise=alls=2:allf=t+u,format=yuv420p"
        ),
        "-frames:v", str(frames),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", str(output),
    ])


def render_video_bed(source: Path, output: Path, duration: float) -> None:
    src_dur = probe_duration(source)
    loops = max(1, int(duration // max(src_dur, 0.1)) + 2)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-stream_loop", str(loops), "-i", str(source), "-an",
        "-vf",
        (
            "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,"
            "crop=1920:1080,"
            f"fps={FPS},trim=duration={duration:.6f},setpts=PTS-STARTPTS,"
            "format=yuv420p"
        ),
        "-frames:v", str(max(1, round(duration * FPS))),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", str(output),
    ])


def render_inscene_bed(kind: str, output: Path, duration: float) -> None:
    render_video_bed(INSCENE[kind], output, duration)


def render_brand(output: Path) -> None:
    """Use polished animated brand bumper; fall back to still."""
    if BRAND_INTRO.exists():
        render_video_bed(BRAND_INTRO, output, 2.0)
        return
    frames = round(2.0 * FPS)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(BRAND_FALLBACK), "-an",
        "-vf",
        (
            "scale=1920:1080:flags=lanczos,"
            "fade=t=in:st=0:d=0.18,fade=t=out:st=1.75:d=0.22,"
            "format=yuv420p"
        ),
        "-frames:v", str(frames),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "15",
        "-pix_fmt", "yuv420p", str(output),
    ])


def choose_orbit(scene_number: int) -> Path | None:
    board = (scene_number - 1) // 4 + 1
    panel = (scene_number - 1) % 4 + 1
    if board == 1:
        return None
    if panel not in ORBIT_PANELS:
        return None
    pose = LOOPS / POSE_CYCLE[(scene_number + board) % len(POSE_CYCLE)]
    return pose if pose.exists() else None


def overlay_orbit(
    bed: Path,
    output: Path,
    orbit: Path | None,
    duration: float,
    fade_in: bool,
    fade_out: bool,
) -> None:
    if orbit is None:
        run(["cp", str(bed), str(output)])
        return
    fade_bits = ""
    if fade_in:
        fade_bits += ",fade=t=in:st=0:d=0.30:alpha=1"
    if fade_out:
        fade_bits += f",fade=t=out:st={max(0.0, duration - 0.30):.4f}:d=0.30:alpha=1"
    filt = (
        "[0:v]format=yuv420p[bg];"
        f"[1:v]fps={FPS},format=rgba,"
        f"scale=-1:{ORBIT_H}:flags=lanczos,"
        "lut=a='if(lt(val\\,28)\\,0\\,if(gt(val\\,230)\\,255\\,val))',"
        f"trim=duration={duration:.4f},setpts=PTS-STARTPTS"
        f"{fade_bits}[orb];"
        "[orb]split[orbA][orbB];"
        "[orbB]colorchannelmixer=aa=0.40,hue=s=0,eq=brightness=-0.30,"
        "gblur=sigma=12[shadow];"
        f"[bg][shadow]overlay=x={ORBIT_X + 16}:y={ORBIT_Y + 24}:format=auto[bg2];"
        f"[bg2][orbA]overlay=x={ORBIT_X}:y='{ORBIT_Y}+6*sin(2*PI*t/4.6)':"
        "format=auto,format=yuv420p[v]"
    )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(bed),
        "-stream_loop", "-1", "-i", str(orbit),
        "-filter_complex", filt,
        "-map", "[v]", "-an",
        "-frames:v", str(max(1, round(duration * FPS))),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", str(output),
    ])


def concat_two(a: Path, b: Path, output: Path) -> None:
    lst = output.with_suffix(".txt")
    lst.write_text(f"file '{a}'\nfile '{b}'\n")
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c", "copy", str(output),
    ])


def render_scene_picture(
    item: dict,
    work: Path,
) -> tuple[Path, dict]:
    asset = item["asset_id"]
    duration = float(item["duration"])
    meta: dict = {**item}

    if asset == "brand-card":
        out = work / "brand.mp4"
        render_brand(out)
        meta["kind"] = "brand"
        return out, meta

    scene_number = int(asset.split("-")[1])
    board = (scene_number - 1) // 4 + 1
    panel = (scene_number - 1) % 4 + 1
    bed = work / f"{asset}_bed.mp4"
    final = work / f"{asset}_final.mp4"

    # Chapter card replaces the first stretch of panel 1 (audio-safe)
    chapter_name = CHAPTER_AT_BOARD.get(board) if panel == 1 else None
    chapter_dur = 0.0
    if chapter_name:
        chapter_src = CHAPTERS / chapter_name
        if chapter_src.exists():
            chapter_dur = min(probe_duration(chapter_src), max(2.2, duration * 0.28), duration - 1.5)
            chapter_dur = max(0.0, chapter_dur)

    remaining = duration - chapter_dur
    parts: list[Path] = []

    if chapter_dur > 0.05:
        chap_part = work / f"{asset}_chapter.mp4"
        render_video_bed(CHAPTERS / chapter_name, chap_part, chapter_dur)
        parts.append(chap_part)
        meta["chapter"] = chapter_name

    if asset in INSCENE_BEATS and remaining > 0.05:
        scene_part = work / f"{asset}_inscene.mp4"
        render_inscene_bed(INSCENE_BEATS[asset], scene_part, remaining)
        parts.append(scene_part)
        meta["kind"] = f"inscene-{INSCENE_BEATS[asset]}"
        # no orbit overlay on full-frame performances
        if len(parts) == 1:
            run(["cp", str(parts[0]), str(final)])
        else:
            concat_two(parts[0], parts[1], final)
        return final, meta

    # Illustrated / Seedance bed for remaining
    png = Path(item["source"])
    if not png.exists():
        matches = sorted(SCENES.glob(f"scene-{scene_number:03d}_*.png"))
        png = matches[0]
    animated = animated_for_png(png)
    scene_bed = work / f"{asset}_scenebed.mp4"
    if animated is not None:
        render_seedance_bed(animated, scene_bed, remaining)
        meta["kind"] = "seedance"
    else:
        render_smooth_still_bed(png, scene_bed, remaining, scene_number)
        meta["kind"] = "smooth-still"

    orbit = choose_orbit(scene_number)
    fade_in = orbit is not None and panel == ORBIT_PANELS[0] and chapter_dur <= 0.05
    fade_out = orbit is not None and panel == ORBIT_PANELS[-1]
    scene_final = work / f"{asset}_scene_final.mp4"
    overlay_orbit(scene_bed, scene_final, orbit, remaining, fade_in, fade_out)
    if orbit:
        meta["orbit_pose"] = orbit.name

    if chapter_dur > 0.05:
        concat_two(parts[0], scene_final, final)
    else:
        run(["cp", str(scene_final), str(final)])
    return final, meta


def render_outro(work: Path) -> tuple[Path, Path]:
    """Picture + audio for like/subscribe endcard."""
    pic = work / "outro_pic.mp4"
    # Prefer animated outro clip; else still end screen
    src = BRAND_OUTRO if BRAND_OUTRO.exists() else END_SCREEN
    if src.suffix.lower() == ".mp4":
        render_video_bed(src, pic, OUTRO_HOLD)
    else:
        frames = round(OUTRO_HOLD * FPS)
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-i", str(src), "-an",
            "-vf",
            (
                "scale=1920:1080:flags=lanczos,"
                f"fade=t=in:st=0:d=0.25,fade=t=out:st={OUTRO_HOLD-0.35:.2f}:d=0.35,"
                "format=yuv420p"
            ),
            "-frames:v", str(frames),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
            "-pix_fmt", "yuv420p", str(pic),
        ])

    audio = work / "outro_audio.wav"
    # CTA VO + soft music bed, loudnorm-ish
    music = MUSIC_A if MUSIC_A.exists() else AUDIO_MASTER
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(CTA_VO),
        "-stream_loop", "-1", "-i", str(music),
        "-filter_complex",
        (
            f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"apad=whole_dur={OUTRO_HOLD:.3f},atrim=0:{OUTRO_HOLD:.3f},"
            "volume=1.0[vo];"
            f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"atrim=0:{OUTRO_HOLD:.3f},volume=0.07[mus];"
            "[vo][mus]amix=inputs=2:weights='1 0.55':normalize=0,"
            "alimiter=limit=0.90:level=false[a]"
        ),
        "-map", "[a]", "-t", f"{OUTRO_HOLD:.3f}",
        "-c:a", "pcm_s24le", str(audio),
    ])
    return pic, audio


def main() -> None:
    assert AUDIO_MASTER.exists(), AUDIO_MASTER
    assert CTA_VO.exists(), CTA_VO
    for p in INSCENE.values():
        assert p.exists(), p

    timeline_doc = json.loads(TIMELINE.read_text())
    items = timeline_doc["timeline"]
    seedance_ready = len(list(ANIMATED.glob("scene-*_seedance-mini.mp4")))
    print(f"Seedance clips ready: {seedance_ready}/96", flush=True)

    with tempfile.TemporaryDirectory(prefix="orbit-bold-v09-") as temp:
        work = Path(temp)
        parts: list[Path] = []
        rebuilt: list[dict] = []
        chapters = 0
        for idx, item in enumerate(items):
            print(f"[{idx+1}/{len(items)}] {item['asset_id']} {float(item['duration']):.2f}s", flush=True)
            part, meta = render_scene_picture(item, work)
            if meta.get("chapter"):
                chapters += 1
            parts.append(part)
            rebuilt.append(meta)

        concat = work / "concat.txt"
        concat.write_text("".join(f"file '{p}'\n" for p in parts))
        body_pic = work / "body_pic.mp4"
        print("Concat body picture…", flush=True)
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat),
            "-c", "copy", str(body_pic),
        ])

        # Mux body with approved narration mix
        body = work / "body.mp4"
        print("Mux body audio…", flush=True)
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(body_pic), "-i", str(AUDIO_MASTER),
            "-map", "0:v:0", "-map", "1:a:0", "-shortest",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-c:a", "aac", "-b:a", "256k", str(body),
        ])

        # Outro like/subscribe
        print("Build like/subscribe outro…", flush=True)
        outro_pic, outro_audio = render_outro(work)
        outro = work / "outro.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(outro_pic), "-i", str(outro_audio),
            "-map", "0:v:0", "-map", "1:a:0", "-shortest",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-c:a", "aac", "-b:a", "256k", str(outro),
        ])

        print("Append outro…", flush=True)
        final_list = work / "final.txt"
        final_list.write_text(f"file '{body}'\nfile '{outro}'\n")
        # Re-encode join for clean A/V
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(final_list),
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-c:a", "aac", "-b:a", "256k",
            "-movflags", "+faststart", str(OUT),
        ])
        run(["cp", str(OUT), str(OUT_ALIAS)])
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(OUT), "-t", "90",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", str(PROOF),
        ])

        for t in (8, 18.5, 22, 48, 105):
            qc = ROOT / f"09_Final-Export/_qc_v09_{str(t).replace('.', '_')}s.png"
            run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", str(t), "-i", str(OUT), "-frames:v", "1", str(qc),
            ])
        # endcard QC
        dur = probe_duration(OUT)
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{max(0, dur - 5):.2f}", "-i", str(OUT), "-frames:v", "1",
            str(ROOT / "09_Final-Export/_qc_v09_outro.png"),
        ])

    summary = {
        "version": "bold-explainer-v09-final-polish",
        "output": str(OUT),
        "proof": str(PROOF),
        "duration": probe_duration(OUT),
        "seedance_ready": seedance_ready,
        "chapter_cards_inserted": chapters,
        "outro_seconds": OUTRO_HOLD,
        "cta_vo": str(CTA_VO),
        "notes": [
            "Removed white sweep bar",
            "Post-hook brand uses bold animated bumper",
            "Chapter cards at major board starts (duration-preserving)",
            "Like/subscribe outro appended with existing CTA VO",
            "fal Seedance balance exhausted — remaining beds use smooth pan",
        ],
        "timeline": rebuilt,
    }
    MANIFEST.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in summary if k != "timeline"}, indent=2))


if __name__ == "__main__":
    main()
