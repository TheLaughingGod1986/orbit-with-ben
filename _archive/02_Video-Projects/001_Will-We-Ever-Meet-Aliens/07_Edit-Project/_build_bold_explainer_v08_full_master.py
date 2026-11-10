#!/usr/bin/env python3
"""Bold Explainer v08 — full ~18min master.

Picture:
  - Seedance-animated illustrated boards (real motion, no shaky Ken Burns)
  - Smooth local fallback only if a Seedance clip is still missing
  - Orbit on ~70% of panels (soft shadow, polished blink loops)
  - Full-frame Seedance Orbit performances at key story beats

Audio:
  - Remux approved Bold v06 final mix (narration-led 18min script)
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
SCENES = ROOT / "04_Generated-Clips/03_Polished/bold_rebuild_v05/scenes"
BRAND = ROOT / "04_Generated-Clips/03_Polished/brand/orbit_brand_intro_v03_free.png"
LOOPS = ROOT / "04_Generated-Clips/03_Polished/orbit_narrator/rgba/loops_polished_v25"
INSCENE = {
    "explain": ROOT / "04_Generated-Clips/03_Polished/orbit_explaining_talk_v01_polished.mp4",
    "surprise": ROOT / "04_Generated-Clips/03_Polished/orbit_surprised_reaction_v01_polished.mp4",
    "ending": ROOT / "04_Generated-Clips/03_Polished/orbit_ending_goodbye_v01_polished.mp4",
}
AUDIO_MASTER = ROOT / "09_Final-Export/aliens_BOLD_EXPLAINER_v06_FINAL_POLISHED_MASTER.mp4"
OUT = ROOT / "09_Final-Export/aliens_BOLD_EXPLAINER_v08_FULL_ANIMATED_MASTER.mp4"
OUT_ALIAS = ROOT / "09_Final-Export/aliens_v15_FULL_INTEGRATED_CONCEPT_MASTER.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v08_PROOF_animated_orbit_90s.mp4"
MANIFEST = ROOT / "07_Edit-Project/bold-explainer-v08-full-timeline.json"

FPS = 30
BRAND_HOLD = 2.0
ORBIT_H = 580
ORBIT_X = 1220
ORBIT_Y = 430

# After board 1 (hook), put Orbit on 3 of 4 panels → ~70% presence
ORBIT_PANELS = (1, 2, 3)  # panels within each board (1-indexed)
POSE_CYCLE = [
    "orbit_present_idle.mov",
    "orbit_thinking_idle.mov",
    "orbit_amazed_idle.mov",
    "orbit_neutral_idle.mov",
    "orbit_wave_idle.mov",
    "orbit_present_talk.mov",
    "orbit_thinking_talk.mov",
]

# Full-frame Orbit replaces the illustrated bed on these scene asset_ids
INSCENE_BEATS = {
    "scene-005": "explain",   # first post-brand beat — “This is Orbit”
    "scene-016": "surprise",  # Fermi / where-is-everyone reaction
    "scene-068": "surprise",  # Wow caution beat
    "scene-095": "ending",    # closing fly-away energy
    "scene-096": "ending",
}


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
            "eq=saturation=1.03:contrast=1.01,format=yuv420p"
        ),
        "-frames:v", str(max(1, round(duration * FPS))),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", str(output),
    ])


def render_smooth_still_bed(png: Path, output: Path, duration: float, scene_number: int) -> None:
    """Fallback: smooth continuous pan (no zoompan shake) + light grain/sheen."""
    frames = max(1, round(duration * FPS))
    # Continuous sub-pixel pan via crop expression — locked, not handheld
    direction = scene_number % 4
    if direction == 0:
        x_expr = f"(iw-ow)*t/{duration:.6f}"
        y_expr = "0"
    elif direction == 1:
        x_expr = f"(iw-ow)*(1-t/{duration:.6f})"
        y_expr = "0"
    elif direction == 2:
        x_expr = "0"
        y_expr = f"(ih-oh)*t/{duration:.6f}"
    else:
        x_expr = "(iw-ow)/2"
        y_expr = f"(ih-oh)*(1-t/{duration:.6f})"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(png),
        "-f", "lavfi", "-i", f"color=c=white:s=420x1080:r={FPS}:d={duration:.6f}",
        "-filter_complex",
        (
            "[0:v]scale=2100:1180:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop=1920:1080:x='{x_expr}':y='{y_expr}',"
            f"fps={FPS},trim=duration={duration:.6f},setpts=PTS-STARTPTS,"
            "eq=saturation=1.04:contrast=1.02,noise=alls=2:allf=t+u[base];"
            f"[1:v]format=rgba,colorchannelmixer=aa=0.018,"
            f"trim=duration={duration:.6f},setpts=PTS-STARTPTS[sweep];"
            "[base][sweep]overlay=x='-w+mod(t*160,W+w)':y=0:format=auto,"
            "format=yuv420p[v]"
        ),
        "-map", "[v]", "-an",
        "-frames:v", str(frames),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", str(output),
    ])


def render_inscene_bed(kind: str, output: Path, duration: float) -> None:
    source = INSCENE[kind]
    src_dur = probe_duration(source)
    loops = max(1, int(duration // src_dur) + 2)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-stream_loop", str(loops), "-i", str(source), "-an",
        "-vf",
        (
            "scale=1920:1080:flags=lanczos,"
            f"fps={FPS},trim=duration={duration:.6f},setpts=PTS-STARTPTS,"
            "format=yuv420p"
        ),
        "-frames:v", str(max(1, round(duration * FPS))),
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
        "-frames:v", str(frames),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "15",
        "-pix_fmt", "yuv420p", str(output),
    ])


def choose_orbit(scene_number: int) -> Path | None:
    board = (scene_number - 1) // 4 + 1
    panel = (scene_number - 1) % 4 + 1
    if board == 1:
        return None  # clean hook
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


def main() -> None:
    assert AUDIO_MASTER.exists(), AUDIO_MASTER
    for p in INSCENE.values():
        assert p.exists(), p
    timeline_doc = json.loads(TIMELINE.read_text())
    items = timeline_doc["timeline"]

    seedance_ready = len(list(ANIMATED.glob("scene-*_seedance-mini.mp4")))
    print(f"Seedance clips ready: {seedance_ready}/96")

    with tempfile.TemporaryDirectory(prefix="orbit-bold-v08-") as temp:
        work = Path(temp)
        parts: list[Path] = []
        rebuilt: list[dict] = []
        orbit_count = 0
        inscene_count = 0
        fallback_count = 0

        for idx, item in enumerate(items):
            asset = item["asset_id"]
            duration = float(item["duration"])
            print(f"[{idx+1}/{len(items)}] {asset} {duration:.2f}s", flush=True)

            if asset == "brand-card":
                brand = work / "brand.mp4"
                render_brand(brand)
                parts.append(brand)
                rebuilt.append({**item, "kind": "brand"})
                continue

            scene_number = int(asset.split("-")[1])
            bed = work / f"{asset}_bed.mp4"
            final = work / f"{asset}_final.mp4"
            kind = "seedance"
            orbit_name = None

            if asset in INSCENE_BEATS:
                render_inscene_bed(INSCENE_BEATS[asset], bed, duration)
                kind = f"inscene-{INSCENE_BEATS[asset]}"
                inscene_count += 1
                # Full-frame Orbit already in picture — no overlay
                run(["cp", str(bed), str(final)])
            else:
                png = Path(item["source"])
                animated = animated_for_png(png)
                if animated is not None:
                    render_seedance_bed(animated, bed, duration)
                else:
                    # Prefer still-named scene file if timeline path differs
                    if not png.exists():
                        matches = sorted(SCENES.glob(f"scene-{scene_number:03d}_*.png"))
                        png = matches[0]
                    render_smooth_still_bed(png, bed, duration, scene_number)
                    kind = "smooth-still-fallback"
                    fallback_count += 1

                orbit = choose_orbit(scene_number)
                # Fade on first/last orbit panel of a board for polish
                panel = (scene_number - 1) % 4 + 1
                fade_in = orbit is not None and panel == ORBIT_PANELS[0]
                fade_out = orbit is not None and panel == ORBIT_PANELS[-1]
                overlay_orbit(bed, final, orbit, duration, fade_in, fade_out)
                if orbit is not None:
                    orbit_count += 1
                    orbit_name = orbit.name

            parts.append(final)
            rebuilt.append({
                **item,
                "kind": kind,
                "orbit_pose": orbit_name,
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
        run(["cp", str(OUT), str(OUT_ALIAS)])
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(OUT), "-t", "90",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", str(PROOF),
        ])

        for t in (8, 22, 48, 75):
            qc = ROOT / f"09_Final-Export/_qc_v08_{t}s.png"
            run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", str(t), "-i", str(PROOF), "-frames:v", "1", str(qc),
            ])

    manifest = {
        "version": "bold-explainer-v08-full-animated",
        "based_on": str(TIMELINE),
        "audio_from": str(AUDIO_MASTER),
        "output": str(OUT),
        "alias": str(OUT_ALIAS),
        "proof": str(PROOF),
        "duration": probe_duration(OUT),
        "seedance_ready_at_build": seedance_ready,
        "orbit_overlay_count": orbit_count,
        "inscene_orbit_count": inscene_count,
        "smooth_fallback_count": fallback_count,
        "timeline": rebuilt,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({
        "output": str(OUT),
        "proof": str(PROOF),
        "duration": manifest["duration"],
        "orbit_overlay_count": orbit_count,
        "inscene_orbit_count": inscene_count,
        "smooth_fallback_count": fallback_count,
        "seedance_ready_at_build": seedance_ready,
    }, indent=2))


if __name__ == "__main__":
    main()
