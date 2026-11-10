#!/usr/bin/env python3
"""Rebuild approved Bold v06 with animated beds.

Uses Seedance clips when present; otherwise smooth pan (no shaky zoompan).
Preserves v06 timeline, Orbit choreography, and exact final audio mix.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
TIMELINE = ROOT / "07_Edit-Project/bold-explainer-v06-final-timeline.json"
ANIMATED = ROOT / "04_Generated-Clips/03_Polished/bold_rebuild_v05/animated"
BRAND = ROOT / "04_Generated-Clips/03_Polished/brand/orbit_brand_intro_v03_free.png"
RIG = Path("/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v03/loops")
AUDIO_MASTER = ROOT / "09_Final-Export/aliens_BOLD_EXPLAINER_v06_FINAL_POLISHED_MASTER.mp4"
OUT = ROOT / "09_Final-Export/aliens_BOLD_EXPLAINER_v07_ANIMATED_BEDS_MASTER.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v07_ANIMATED_BEDS_PROOF_90s.mp4"
MANIFEST = ROOT / "07_Edit-Project/bold-explainer-v07-animated-timeline.json"

FPS = 30
BRAND_HOLD = 2.0
TWO_PANEL_ORBIT = {2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 16, 17, 19, 21, 22, 24}


def run(args: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, capture_output=capture)


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
            "eq=saturation=1.02:contrast=1.01,format=yuv420p"
        ),
        "-frames:v", str(max(1, round(duration * FPS))),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", str(output),
    ])


def render_smooth_still_bed(png: Path, output: Path, duration: float, scene_number: int) -> None:
    """Stable continuous pan — replaces shaky zoompan. Not Seedance, but locked."""
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
        "-loop", "1", "-i", str(png),
        "-f", "lavfi", "-i", f"color=c=white:s=480x1080:r={FPS}:d={duration:.6f}",
        "-filter_complex",
        (
            "[0:v]scale=2112:1188:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop=1920:1080:x='{x_expr}':y='{y_expr}',"
            f"fps={FPS},trim=duration={duration:.6f},setpts=PTS-STARTPTS,"
            "eq=saturation=1.03:contrast=1.015[base];"
            f"[1:v]format=rgba,colorchannelmixer=aa=0.014,"
            f"trim=duration={duration:.6f},setpts=PTS-STARTPTS[sweep];"
            "[base][sweep]overlay=x='-w+mod(t*120,W+w)':y=0:format=auto,"
            "format=yuv420p[v]"
        ),
        "-map", "[v]", "-an",
        "-frames:v", str(frames),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", str(output),
    ])


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
    if orbit is None:
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


def main() -> None:
    timeline_doc = json.loads(TIMELINE.read_text())
    items = timeline_doc["timeline"]
    seedance_count = 0
    fallback_count = 0

    with tempfile.TemporaryDirectory(prefix="orbit-bold-v07-") as temp:
        work = Path(temp)
        parts: list[Path] = []
        rebuilt: list[dict] = []

        for index, item in enumerate(items, start=1):
            asset = item["asset_id"]
            duration = float(item["duration"])
            start = float(item["start"])
            print(f"[{index}/{len(items)}] {asset} {duration:.2f}s", flush=True)

            if asset == "brand-card":
                brand = work / "brand.mp4"
                render_brand(brand)
                parts.append(brand)
                rebuilt.append({**item, "kind": "brand"})
                continue

            scene_number = int(asset.split("-")[1])
            png = Path(item["source"])
            bed = work / f"{asset}_bed.mp4"
            final = work / f"{asset}_final.mp4"
            seedance = animated_for_png(png)
            if seedance is not None:
                render_seedance_bed(seedance, bed, duration)
                kind = "seedance"
                seedance_count += 1
                motion_source = str(seedance)
            else:
                render_smooth_still_bed(png, bed, duration, scene_number)
                kind = "smooth-still-fallback"
                fallback_count += 1
                motion_source = str(png)

            orbit, fade_in, fade_out = orbit_meta(item.get("orbit_pose"), scene_number)
            overlay_orbit(bed, final, orbit, duration, start, fade_in, fade_out)
            parts.append(final)
            rebuilt.append({
                **item,
                "kind": kind,
                "motion_source": motion_source,
                "motion_sha256": file_hash(Path(motion_source)),
            })

        concat = work / "concat.txt"
        concat.write_text("".join(f"file '{path}'\n" for path in parts))
        silent = work / "silent.mp4"
        print("Concat picture…", flush=True)
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat),
            "-c", "copy", str(silent),
        ])

        print("Mux audio from Bold v06 master…", flush=True)
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(silent), "-i", str(AUDIO_MASTER),
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

    manifest = {
        "version": "bold-explainer-v07-animated-beds",
        "based_on": str(TIMELINE),
        "audio_from": str(AUDIO_MASTER),
        "output": str(OUT),
        "proof": str(PROOF),
        "duration": probe_duration(OUT),
        "seedance_count": seedance_count,
        "smooth_fallback_count": fallback_count,
        "timeline": rebuilt,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({
        "output": str(OUT),
        "proof": str(PROOF),
        "duration": manifest["duration"],
        "seedance_count": seedance_count,
        "smooth_fallback_count": fallback_count,
        "manifest": str(MANIFEST),
    }, indent=2))


if __name__ == "__main__":
    main()
