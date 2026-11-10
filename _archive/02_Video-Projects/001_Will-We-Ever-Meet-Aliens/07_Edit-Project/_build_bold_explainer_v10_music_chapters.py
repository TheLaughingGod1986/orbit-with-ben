#!/usr/bin/env python3
"""Bold Explainer v12 — upload-ready, no-repeat picture and VO-synced branding.

Preserves approved Bold v06 timeline timing and Overlay-Rig Orbit choreography.
Adds:
  - Seedance beds play once; unique stable board motion fills leftover VO
  - Chapter cards are locked, stable stills
  - Hook-first animated Orbit brand introduction, aligned to “This is Orbit”
  - Animated Orbit like/subscribe outro
  - Audible ducked music, ambience, chapter transitions and Orbit servo/blips

Hard rule: never stream_loop / restart scenery clips in one video.
"""
from __future__ import annotations

import json
import hashlib
import subprocess
import tempfile
from pathlib import Path


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
TIMELINE = ROOT / "07_Edit-Project/bold-explainer-v06-final-timeline.json"
ANIMATED = ROOT / "04_Generated-Clips/03_Polished/bold_rebuild_v05/animated"
CHAPTERS = ROOT / "04_Generated-Clips/03_Polished/chapter_cards"
BRAND_INTRO = ROOT / "04_Generated-Clips/03_Polished/brand/orbit_brand_intro_bold-v05_2s.mp4"
BRAND_FALLBACK = ROOT / "04_Generated-Clips/03_Polished/brand/orbit_brand_intro_v03_free.png"
BRAND_OUTRO = ROOT / "04_Generated-Clips/03_Polished/brand/orbit_brand_outro_subscribe_v02.png"
BRAND = BRAND_INTRO  # preferred; render_brand falls back to PNG if missing
RIG = Path("/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v03/loops")
RIG_PROXY = ROOT / "07_Edit-Project/_orbit_proxy"

MASTER_VOICE = ROOT / "02_Voiceover/05_Master/aliens_voiceover_bold-v06_ivc_kDch_master.wav"
MUSIC_A = ROOT / "05_Music/aliens_score_cinematic_v19.wav"
MUSIC_B = ROOT / "05_Music/aliens_score_ambient_v16.wav"
SFX = ROOT / "06_Sound-Effects"
SFX_BED = SFX / "aliens_sfx_bed_v19.wav"
SPACE_AMBIENCE = SFX / "aliens_space_ambience_v19.wav"
CHAPTER_WHOOSH = SFX / "sfx_whoosh_v19.wav"
SHIMMER = SFX / "sfx_shimmer_v19.wav"
BRAND_CHIME = SFX / "sfx_brand_chime_v11.wav"
ORBIT_SERVO = SFX / "sfx_orbit_servo_v19.wav"
ORBIT_BLIP = SFX / "sfx_orbit_blip_v19.wav"

OUT = ROOT / "09_Final-Export/aliens_BOLD_EXPLAINER_v13_VO_SYNC_UPLOAD_READY_MASTER.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v13_PROOF_vo_synced_intro_45s.mp4"
CHAPTER_PROOF = ROOT / "09_Final-Export/aliens_v13_PROOF_stable_cards_45s.mp4"
MANIFEST = ROOT / "07_Edit-Project/bold-explainer-v13-vo-sync-upload-ready-timeline.json"

FPS = 30
BRAND_HOLD = 2.0
# “This is Orbit” begins at approximately 19.883 seconds in the locked VO.
# The ident has a 0.2-second visual fade, so start it 0.233 seconds earlier.
# The card is fully visible on the first consonant without moving the VO.
BRAND_SYNC_START = 19.650
OUTRO_HOLD = 10.0
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


def orbit_asset(name: str) -> Path:
    """Prefer lossless 8-bit alpha edit proxies; preserve 12-bit masters."""
    proxy = RIG_PROXY / name
    return proxy if proxy.exists() else RIG / name


USED_ANIMATED_HASHES: set[str] = set()


def animated_for_png(png_path: Path) -> Path | None:
    candidate = ANIMATED / f"{Path(png_path).stem}_seedance-mini.mp4"
    if candidate.exists() and candidate.stat().st_size > 100_000:
        digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
        if digest in USED_ANIMATED_HASHES:
            return None
        USED_ANIMATED_HASHES.add(digest)
        return candidate
    return None


def render_seedance_once(source: Path, output: Path, frames: int) -> None:
    """Play Seedance once at native timing — never stream_loop / restart motion."""
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(source), "-an",
        "-vf",
        (
            "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,"
            "crop=1920:1080,"
            f"fps={FPS},setpts=PTS-STARTPTS,"
            "eq=saturation=1.02:contrast=1.01,format=yuv420p"
        ),
        "-frames:v", str(max(1, frames)),
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "14",
        "-pix_fmt", "yuv420p", str(output),
    ])


def render_smooth_still_bed(
    png: Path,
    output: Path,
    duration: float,
    scene_number: int,
    *,
    frames: int | None = None,
) -> None:
    frame_count = frames if frames is not None else max(1, round(duration * FPS))
    dur = frame_count / FPS
    direction = scene_number % 4
    if direction == 0:
        x_expr = f"(iw-ow)*t/{dur:.6f}"
        y_expr = "(ih-oh)/2"
    elif direction == 1:
        x_expr = f"(iw-ow)*(1-t/{dur:.6f})"
        y_expr = "(ih-oh)/2"
    elif direction == 2:
        x_expr = "(iw-ow)/2"
        y_expr = f"(ih-oh)*t/{dur:.6f}"
    else:
        x_expr = "(iw-ow)/2"
        y_expr = f"(ih-oh)*(1-t/{dur:.6f})"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(png), "-an",
        "-vf",
        (
            "scale=2112:1188:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop=1920:1080:x='{x_expr}':y='{y_expr}',"
            f"fps={FPS},setpts=PTS-STARTPTS,"
            "eq=saturation=1.03:contrast=1.015,format=yuv420p"
        ),
        "-frames:v", str(frame_count),
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "14",
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
    total_frames = max(1, round(duration * FPS))
    source_frames = max(1, int(probe_duration(source) * FPS))
    seed_frames = min(source_frames, total_frames)
    still_frames = total_frames - seed_frames
    if still_frames <= 0:
        render_seedance_once(source, output, total_frames)
        return
    work = output.parent
    seed = work / f"{output.stem}_seed_once.mp4"
    still = work / f"{output.stem}_still_fill.mp4"
    render_seedance_once(source, seed, seed_frames)
    render_smooth_still_bed(png, still, still_frames / FPS, scene_number, frames=still_frames)
    concat_two(seed, still, output)

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
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "13",
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
            "-c:v", "libx264", "-tune", "stillimage", "-preset", "ultrafast", "-crf", "12",
            "-x264-params", "keyint=1:min-keyint=1:scenecut=0:bframes=0",
            "-pix_fmt", "yuv420p", str(output),
        ])
        return
    mp4 = CHAPTERS / chapter_mp4_name
    if not mp4.exists():
        raise SystemExit(f"Missing chapter card: {chapter_mp4_name}")
    render_video_bed(mp4, output, duration)


def render_brand(output: Path) -> None:
    """Post-hook brand ident with an independently animated Orbit wave."""
    if BRAND_INTRO.exists():
        wave = orbit_asset("orbit_wave-camera_animated-blink_6s_v01.mov")
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(BRAND_INTRO), "-ss", "0.35", "-i", str(wave),
            "-filter_complex",
            (
                f"[0:v]trim=duration={BRAND_HOLD},setpts=PTS-STARTPTS,"
                "scale=1920:1080:flags=lanczos,"
                "drawbox=x=650:y=70:w=620:h=555:color=0x050913:t=fill[brand];"
                f"[1:v]trim=duration={BRAND_HOLD},setpts=PTS-STARTPTS,"
                "scale=570:422:flags=lanczos,"
                "fade=t=in:st=0:d=0.18:alpha=1,"
                "fade=t=out:st=1.78:d=0.22:alpha=1[orbit];"
                "[brand][orbit]overlay=x=675:y=105:format=auto,"
                "format=yuv420p[out]"
            ),
            "-map", "[out]", "-an", "-t", f"{BRAND_HOLD}",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "13",
            "-pix_fmt", "yuv420p", str(output),
        ])
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
        "-frames:v", str(frames), "-c:v", "libx264", "-preset", "ultrafast",
        "-crf", "12", "-pix_fmt", "yuv420p", str(output),
    ])


def render_outro(output: Path) -> None:
    """Ten-second animated Orbit call-to-action with end-screen-safe spacing."""
    wave = orbit_asset("orbit_wave-camera_animated-blink_6s_v01.mov")
    stretch = OUTRO_HOLD / probe_duration(wave)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-framerate", str(FPS), "-i", str(BRAND_OUTRO),
        "-i", str(wave), "-an",
        "-filter_complex",
        (
            f"[0:v]trim=duration={OUTRO_HOLD},setpts=PTS-STARTPTS,"
            "scale=1920:1080:flags=lanczos,"
            "drawbox=x=50:y=45:w=265:h=270:color=0x090d1c:t=fill[base];"
            f"[1:v]scale=580:430:flags=lanczos,setpts={stretch:.8f}*PTS,"
            f"trim=duration={OUTRO_HOLD},setpts=PTS-STARTPTS[orbit];"
            "[base][orbit]overlay=x=1290:y=525:format=auto,"
            "fade=t=in:st=0:d=0.45,"
            "fade=t=out:st=9.25:d=0.75,format=yuv420p[out]"
        ),
        "-map", "[out]", "-t", f"{OUTRO_HOLD}",
        "-frames:v", str(round(OUTRO_HOLD * FPS)),
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "13",
        "-pix_fmt", "yuv420p", str(output),
    ])


def concat_two(a: Path, b: Path, output: Path) -> None:
    """Frame-accurate concat (re-encode) so Seedance+still joins keep exact length."""
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(a), "-i", str(b),
        "-filter_complex",
        f"[0:v]fps={FPS},setpts=PTS-STARTPTS,format=yuv420p[v0];"
        f"[1:v]fps={FPS},setpts=PTS-STARTPTS,format=yuv420p[v1];"
        "[v0][v1]concat=n=2:v=1:a=0[v]",
        "-map", "[v]", "-an",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "14",
        "-pix_fmt", "yuv420p", str(output),
    ])


def orbit_meta(pose_name: str | None, scene_number: int) -> tuple[Path | None, bool, bool]:
    if not pose_name or pose_name == "brand-card":
        return None, False, False
    board = (scene_number - 1) // 4 + 1
    panel = (scene_number - 1) % 4 + 1
    chosen = (2, 3) if board in TWO_PANEL_ORBIT else (3,)
    return orbit_asset(pose_name), panel == chosen[0], panel == chosen[-1]


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
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "14",
        "-pix_fmt", "yuv420p", str(output),
    ])


def build_audio_mix(
    work: Path,
    duration: float,
    chapter_times: list[float],
    orbit_times: list[float],
    brand_time: float,
    outro_time: float,
) -> Path:
    """VO + audible ducked music + ambience + transitions + Orbit motion cues."""
    bed = work / "music-bed.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(MUSIC_A), "-i", str(MUSIC_B),
        "-filter_complex",
        (
            "[0:a]atrim=0:635.475,asetpts=PTS-STARTPTS,"
            "loudnorm=I=-30:LRA=11:TP=-3[a0];"
            "[1:a]atrim=0:635.475,asetpts=PTS-STARTPTS,"
            "loudnorm=I=-30:LRA=11:TP=-3[a1];"
            "[a0][a1]acrossfade=d=4:c1=tri:c2=tri,"
            f"atrim=duration={duration:.6f},volume=1.0[bed]"
        ),
        "-map", "[bed]", "-ar", "48000", "-ac", "2",
        "-c:a", "pcm_s24le", str(bed),
    ])

    # Delayed whooshes, shimmer, brand chime and restrained mascot sounds.
    filters = [
        f"[0:a]atrim=duration={duration:.6f},volume=1.0[space]",
        f"[1:a]atrim=duration={duration:.6f},volume=4.0[texture]",
    ]
    inputs = [
        "-i", str(SPACE_AMBIENCE),
        "-i", str(SFX_BED),
        "-i", str(CHAPTER_WHOOSH),
        "-i", str(SHIMMER),
        "-i", str(BRAND_CHIME),
        "-i", str(ORBIT_SERVO),
        "-i", str(ORBIT_BLIP),
    ]
    mix_names = ["space", "texture"]

    for idx, t in enumerate(chapter_times):
        delay_ms = max(0, int(round(t * 1000)))
        name = f"whoosh{idx}"
        filters.append(
            f"[2:a]volume=0.20,adelay={delay_ms}|{delay_ms}[{name}]"
        )
        mix_names.append(name)

    # Soft shimmer after first chapter + near end
    for idx, t in enumerate([chapter_times[0] + 6.0 if chapter_times else 20.0, max(0.0, duration - 28.0)]):
        delay_ms = max(0, int(round(t * 1000)))
        name = f"shim{idx}"
        filters.append(f"[3:a]volume=1.0,adelay={delay_ms}|{delay_ms}[{name}]")
        mix_names.append(name)

    filters.append(
        f"[4:a]volume=0.8,adelay={int(brand_time*1000)}|{int(brand_time*1000)}[chime]"
    )
    mix_names.append("chime")

    # A soft servo only when Orbit enters a new run, not continuously.
    for idx, t in enumerate(orbit_times):
        delay_ms = max(0, int(round(t * 1000)))
        name = f"servo{idx}"
        filters.append(f"[5:a]volume=1.4,adelay={delay_ms}|{delay_ms}[{name}]")
        mix_names.append(name)

    for idx, t in enumerate([brand_time + 0.55, outro_time + 0.7]):
        delay_ms = max(0, int(round(t * 1000)))
        name = f"blip{idx}"
        filters.append(f"[6:a]volume=1.4,adelay={delay_ms}|{delay_ms}[{name}]")
        mix_names.append(name)

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
            "amix=inputs=3:weights='1 0.62 0.78':normalize=0,"
            "volume=-0.5dB,alimiter=limit=0.88:level=false[a]"
        ),
        "-map", "[a]", "-ar", "48000", "-ac", "2",
        "-t", f"{duration:.6f}",
        "-c:a", "pcm_s24le", str(final_audio),
    ])
    return final_audio


def render_scene(item: dict, work: Path) -> tuple[Path, dict]:
    """Render a complete scene in one pass to avoid intermediate join bumps."""
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
    total_frames = max(1, round(duration * FPS))

    chapter_name = CHAPTER_AT_BOARD.get(board) if panel == 1 else None
    chapter_frames = 0
    if chapter_name and (CHAPTERS / chapter_name).exists():
        raw = min(probe_duration(CHAPTERS / chapter_name), max(2.2, duration * 0.30), duration - 1.4)
        chapter_frames = max(0, min(round(raw * FPS), total_frames - round(1.4 * FPS)))

    remaining_frames = total_frames - chapter_frames
    chapter_dur = chapter_frames / FPS
    remaining = remaining_frames / FPS
    png = Path(item["source"])
    animated = animated_for_png(png)
    if asset == "scene-005":
        # Narration resumes after the ident with “This is Orbit.”
        orbit = orbit_asset("orbit_wave-camera_animated-blink_6s_v01.mov")
        fade_in, fade_out = True, True
    else:
        orbit, fade_in, fade_out = orbit_meta(item.get("orbit_pose"), scene_number)
    # Don't fade orbit in over a chapter card join
    if chapter_frames > 0:
        fade_in = False

    command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    filters: list[str] = []
    next_input = 0

    if animated is not None:
        source_duration = max(0.1, probe_duration(animated))
        stretch = remaining / source_duration
        command += ["-i", str(animated)]
        filters.append(
            "[0:v]scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,"
            "crop=1920:1080,"
            f"setpts={stretch:.8f}*PTS,fps={FPS},"
            f"trim=duration={remaining:.6f},setpts=PTS-STARTPTS,"
            "eq=saturation=1.02:contrast=1.01,format=yuv420p[content]"
        )
        meta["kind"] = "seedance"
        meta["motion_source"] = str(animated)
        meta["seedance_policy"] = "single_play_slowed_to_narration_no_loop"
    else:
        direction = scene_number % 4
        if direction == 0:
            x_expr, y_expr = f"(iw-ow)*t/{remaining:.6f}", "(ih-oh)/2"
        elif direction == 1:
            x_expr, y_expr = f"(iw-ow)*(1-t/{remaining:.6f})", "(ih-oh)/2"
        elif direction == 2:
            x_expr, y_expr = "(iw-ow)/2", f"(ih-oh)*t/{remaining:.6f}"
        else:
            x_expr, y_expr = "(iw-ow)/2", f"(ih-oh)*(1-t/{remaining:.6f})"
        command += ["-loop", "1", "-framerate", str(FPS), "-i", str(png)]
        filters.append(
            "[0:v]scale=2112:1188:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop=1920:1080:x='{x_expr}':y='{y_expr}',fps={FPS},"
            f"trim=duration={remaining:.6f},setpts=PTS-STARTPTS,"
            "eq=saturation=1.03:contrast=1.015,format=yuv420p[content]"
        )
        meta["kind"] = "smooth-still"
        meta["motion_source"] = str(png)
    next_input = 1

    scene_label = "content"
    if orbit and orbit.exists():
        command += [
            "-stream_loop", "-1", "-ss", f"{(start + chapter_dur) % 6:.3f}",
            "-i", str(orbit),
        ]
        orbit_chain = (
            f"[{next_input}:v]trim=duration={remaining:.6f},setpts=PTS-STARTPTS"
        )
        if fade_in:
            orbit_chain += ",fade=t=in:st=0:d=0.35:alpha=1"
        if fade_out:
            orbit_chain += (
                f",fade=t=out:st={max(0.0, remaining - 0.35):.4f}:"
                "d=0.35:alpha=1"
            )
        orbit_chain += "[orbit]"
        filters.append(orbit_chain)
        filters.append(
            "[content][orbit]overlay=x=1300:y='625+8*sin(2*PI*t/4.8)':"
            "format=auto[scene]"
        )
        scene_label = "scene"
        next_input += 1
        meta["orbit_pose"] = orbit.name

    if chapter_frames > 0:
        chapter_png = chapter_png_for(chapter_name)
        if chapter_png is None:
            raise SystemExit(f"Missing locked chapter PNG for {chapter_name}")
        command += [
            "-loop", "1", "-framerate", str(FPS), "-i", str(chapter_png),
        ]
        filters.append(
            f"[{next_input}:v]scale=1920:1080:flags=neighbor,fps={FPS},"
            f"trim=duration={chapter_dur:.6f},setpts=PTS-STARTPTS,"
            "format=yuv420p[chapter]"
        )
        filters.append(
            f"[chapter][{scene_label}]concat=n=2:v=1:a=0,format=yuv420p[out]"
        )
        meta["chapter"] = chapter_name
        meta["chapter_duration"] = round(chapter_dur, 3)
    else:
        filters.append(f"[{scene_label}]null,format=yuv420p[out]")

    command += [
        "-filter_complex", ";".join(filters),
        "-map", "[out]", "-an",
        "-frames:v", str(total_frames),
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "14",
        "-pix_fmt", "yuv420p", str(final),
    ]
    run(command)
    return final, meta


def main() -> None:
    required = [
        TIMELINE, MASTER_VOICE, MUSIC_A, MUSIC_B, SPACE_AMBIENCE, SFX_BED,
        CHAPTER_WHOOSH, SHIMMER, BRAND_CHIME, BRAND_OUTRO,
        ORBIT_SERVO, ORBIT_BLIP,
    ]
    if not BRAND_INTRO.exists() and not BRAND_FALLBACK.exists():
        required.append(BRAND_FALLBACK)
    missing = [p for p in required if not p.exists()]
    if missing:
        raise SystemExit("Missing:\n" + "\n".join(str(p) for p in missing))

    timeline_doc = json.loads(TIMELINE.read_text())
    # Keep the total runtime and every later cue locked. Borrow the offset from
    # the following scene: extend the hook's closing visual through the quiet
    # beat, then show the brand card exactly as “This is Orbit” begins.
    items = [dict(item) for item in timeline_doc["timeline"]]
    brand_index = next(
        i for i, item in enumerate(items) if item["asset_id"] == "brand-card"
    )
    previous_item = items[brand_index - 1]
    brand_item = items[brand_index]
    following_item = items[brand_index + 1]
    brand_shift = BRAND_SYNC_START - float(brand_item["start"])
    if brand_shift <= 0 or float(following_item["duration"]) <= brand_shift:
        raise SystemExit("Invalid VO-sync shift for brand introduction")
    previous_item["duration"] = round(float(previous_item["duration"]) + brand_shift, 6)
    previous_item["end"] = round(BRAND_SYNC_START, 6)
    brand_item["start"] = round(BRAND_SYNC_START, 6)
    brand_item["end"] = round(BRAND_SYNC_START + BRAND_HOLD, 6)
    following_item["start"] = round(BRAND_SYNC_START + BRAND_HOLD, 6)
    following_item["duration"] = round(float(following_item["duration"]) - brand_shift, 6)
    USED_ANIMATED_HASHES.clear()
    seedance_ready = len(list(ANIMATED.glob("scene-*_seedance-mini.mp4")))
    print(f"Seedance clips ready: {seedance_ready}/96", flush=True)

    with tempfile.TemporaryDirectory(prefix="orbit-bold-v10-") as temp:
        work = Path(temp)
        parts: list[Path] = []
        rebuilt: list[dict] = []
        chapter_times: list[float] = []
        orbit_times: list[float] = []
        seedance_count = 0
        chapters = 0
        previous_pose: str | None = None
        brand_time = next(
            (float(item["start"]) for item in items if item["asset_id"] == "brand-card"),
            17.704,
        )

        for idx, item in enumerate(items, start=1):
            print(f"[{idx}/{len(items)}] {item['asset_id']} {float(item['duration']):.2f}s", flush=True)
            part, meta = render_scene(item, work)
            if meta.get("kind") == "seedance":
                seedance_count += 1
            if meta.get("chapter"):
                chapters += 1
                chapter_times.append(float(item["start"]))
            pose = (
                "orbit_wave-camera_animated-blink_6s_v01.mov"
                if item["asset_id"] == "scene-005"
                else item.get("orbit_pose")
            )
            if pose and pose != "brand-card" and pose != previous_pose:
                orbit_times.append(float(item["start"]))
            previous_pose = pose if pose and pose != "brand-card" else None
            parts.append(part)
            rebuilt.append(meta)

        outro_time = sum(round(float(item["duration"]) * FPS) for item in items) / FPS
        outro = work / "animated_orbit_outro.mp4"
        render_outro(outro)
        parts.append(outro)
        rebuilt.append({
            "asset_id": "orbit-outro",
            "start": round(outro_time, 3),
            "end": round(outro_time + OUTRO_HOLD, 3),
            "duration": OUTRO_HOLD,
            "kind": "animated-brand-outro",
            "motion_source": str(orbit_asset("orbit_wave-camera_animated-blink_6s_v01.mov")),
        })

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
        audio = build_audio_mix(
            work,
            pic_dur,
            chapter_times,
            orbit_times,
            brand_time,
            pic_dur - OUTRO_HOLD,
        )

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
        "version": "bold-explainer-v13-vo-sync-upload-ready",
        "based_on": str(TIMELINE),
        "output": str(OUT),
        "proof": str(PROOF),
        "chapter_proof": str(CHAPTER_PROOF),
        "duration": probe_duration(OUT),
        "seedance_count": seedance_count,
        "seedance_ready_at_build": seedance_ready,
        "chapter_cards_inserted": chapters,
        "chapter_times": chapter_times,
        "orbit_sound_times": orbit_times,
        "brand_time": brand_time,
        "outro_time": round(pic_dur - OUTRO_HOLD, 3),
        "rules": [
            "hook_before_brand",
            "brand_card_synced_to_this_is_orbit_vo",
            "no_repeated_background_video",
            "no_stream_loop_for_scenery",
            "stable_locked_chapter_cards",
            "animated_orbit_intro_and_outro",
            "audible_ducked_music_and_sound_design",
        ],
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
