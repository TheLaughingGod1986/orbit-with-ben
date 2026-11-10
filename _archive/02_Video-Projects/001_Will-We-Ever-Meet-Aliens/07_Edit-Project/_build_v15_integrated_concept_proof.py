#!/usr/bin/env python3
"""90s proof: illustrated science world + Orbit feeling *in* the picture.

Replaces flat unique-cards + tiny corner sticker with:
  1. Bold Explainer illustrated scenes (Ken Burns + grain)
  2. Full-frame Seedance Orbit performances (already lit into space)
  3. Larger soft-shadow Orbit host on selected boards (reads as co-present)

This is the visual direction of the concept art reference — not a full
19-minute remaster. Review the proof, then we can rebuild the master.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
SCENES = ROOT / "04_Generated-Clips/03_Polished/bold_rebuild_v05/scenes"
BRAND = ROOT / "04_Generated-Clips/03_Polished/brand/orbit_brand_intro_v03_free.png"
ORBIT_INSCENE = {
    "explain": ROOT / "04_Generated-Clips/03_Polished/orbit_explaining_talk_v01_polished.mp4",
    "surprise": ROOT / "04_Generated-Clips/03_Polished/orbit_surprised_reaction_v01_polished.mp4",
    "ending": ROOT / "04_Generated-Clips/03_Polished/orbit_ending_goodbye_v01_polished.mp4",
}
ORBIT_LOOP = ROOT / (
    "04_Generated-Clips/03_Polished/orbit_narrator/rgba/loops_polished_v25/"
    "orbit_present_idle.mov"
)
# Prefer current cinematic mix so VO matches what user has been reviewing
AUDIO = ROOT / "07_Edit-Project/_mix_work_v14_full/final_mix.wav"
FALLBACK_AUDIO = ROOT / "09_Final-Export/aliens_BOLD_EXPLAINER_v06_FINAL_POLISHED_MASTER.mp4"
OUT = ROOT / "09_Final-Export/aliens_v15_PROOF_integrated_concept_90s.mp4"
FPS = 30


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def probe(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nk=1:nw=1", str(path),
        ],
        text=True,
    )
    return float(out.strip())


def render_board(
    source: Path,
    output: Path,
    duration: float,
    *,
    zoom_in: bool = True,
    orbit: Path | None = None,
    orbit_scale: int = 620,
    orbit_x: int = 1180,
    orbit_y: int = 420,
) -> None:
    """Illustrated still → living plate, optional large soft-shadow Orbit."""
    frames = max(1, round(duration * FPS))
    z = "min(1.10,1+0.00018*on)" if zoom_in else "max(1.0,1.10-0.00018*on)"
    bg = (
        "scale=2300:1294:force_original_aspect_ratio=increase:flags=lanczos,"
        "crop=2300:1294,"
        f"zoompan=z='{z}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':"
        f"d=1:s=1920x1080:fps={FPS},"
        "eq=saturation=1.04:contrast=1.02,"
        "noise=alls=3:allf=t+u,format=rgba"
    )
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(source),
    ]
    if orbit is None:
        cmd += [
            "-an", "-vf", bg.replace(",format=rgba", ",format=yuv420p"),
            "-frames:v", str(frames),
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-pix_fmt", "yuv420p", str(output),
        ]
        run(cmd)
        return

    cmd += ["-stream_loop", "-1", "-i", str(orbit)]
    # Soft contact shadow + mild cyan rim so Orbit shares the illustrated light
    filt = (
        f"[0:v]{bg}[bg];"
        f"[1:v]fps={FPS},format=rgba,"
        f"scale=-1:{orbit_scale}:flags=lanczos,"
        "lut=a='if(lt(val\\,28)\\,0\\,if(gt(val\\,230)\\,255\\,val))',"
        f"trim=duration={duration:.4f},setpts=PTS-STARTPTS,"
        "fade=t=in:st=0:d=0.35:alpha=1,"
        f"fade=t=out:st={max(0.0, duration - 0.35):.4f}:d=0.35:alpha=1[orb];"
        # Drop-shadow plate under Orbit
        "[orb]split[orbA][orbB];"
        "[orbB]colorchannelmixer=aa=0.45,"
        "hue=s=0,eq=brightness=-0.35,"
        "gblur=sigma=14[shadow];"
        f"[bg][shadow]overlay=x={orbit_x + 18}:y={orbit_y + 28}:format=auto[bg2];"
        f"[bg2][orbA]overlay=x={orbit_x}:y='{orbit_y}+7*sin(2*PI*t/4.5)':"
        "format=auto,format=yuv420p[v]"
    )
    cmd += [
        "-filter_complex", filt, "-map", "[v]", "-an",
        "-frames:v", str(frames),
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p", str(output),
    ]
    run(cmd)


def render_inscene(source: Path, output: Path, duration: float) -> None:
    """Full-frame Seedance Orbit already living inside cinematic space."""
    src_dur = probe(source)
    # Loop/pad if we need longer than source
    if duration <= src_dur + 0.05:
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(source), "-t", f"{duration:.4f}",
            "-an", "-vf",
            f"scale=1920:1080:flags=lanczos,fps={FPS},format=yuv420p",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-pix_fmt", "yuv420p", str(output),
        ])
    else:
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-stream_loop", "-1", "-i", str(source),
            "-t", f"{duration:.4f}",
            "-an", "-vf",
            f"scale=1920:1080:flags=lanczos,fps={FPS},format=yuv420p",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-pix_fmt", "yuv420p", str(output),
        ])


def render_brand(output: Path, duration: float = 2.0) -> None:
    frames = round(duration * FPS)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(BRAND), "-an",
        "-vf",
        (
            "scale=1920:1080:flags=lanczos,"
            "fade=t=in:st=0:d=0.18,fade=t=out:st=1.75:d=0.22,"
            "format=yuv420p"
        ),
        "-frames:v", str(frames),
        "-c:v", "libx264", "-preset", "fast", "-crf", "15",
        "-pix_fmt", "yuv420p", str(output),
    ])


def main() -> None:
    assert ORBIT_LOOP.exists(), ORBIT_LOOP
    for p in ORBIT_INSCENE.values():
        assert p.exists(), p
    audio = AUDIO if AUDIO.exists() else FALLBACK_AUDIO

    # Beat map (~90s) — illustrated world first, Orbit as co-star
    beats: list[tuple[str, Path | None, float, dict]] = [
        ("board", SCENES / "scene-001_crowded-night-sky_v01.png", 5.0, {"zoom_in": True}),
        ("board", SCENES / "scene-002_worlds-everywhere_v01.png", 5.0, {"zoom_in": False}),
        ("board", SCENES / "scene-003_signal-no-reply_v01.png", 5.5, {
            "zoom_in": True, "orbit": ORBIT_LOOP, "orbit_scale": 560, "orbit_x": 1280, "orbit_y": 480,
        }),
        ("brand", None, 2.0, {}),
        # "This is Orbit" — full-frame, already in the nebula
        ("inscene", ORBIT_INSCENE["explain"], 7.5, {}),
        ("board", SCENES / "scene-004_fermi-empty-galaxy_v01.png", 5.0, {
            "zoom_in": True, "orbit": ORBIT_LOOP, "orbit_scale": 600, "orbit_x": 1220, "orbit_y": 450,
        }),
        ("board", SCENES / "scene-013_board-04-panel-1_v01.png", 5.5, {"zoom_in": False}),
        ("inscene", ORBIT_INSCENE["surprise"], 4.8, {}),
        ("board", SCENES / "scene-065_board-17-panel-1_v01.png", 6.0, {
            "zoom_in": True, "orbit": ORBIT_LOOP, "orbit_scale": 580, "orbit_x": 1250, "orbit_y": 470,
        }),
        ("board", SCENES / "scene-066_board-17-panel-2_v01.png", 5.5, {"zoom_in": False}),
        ("board", SCENES / "scene-073_board-19-panel-1_v01.png", 6.0, {
            "zoom_in": True, "orbit": ORBIT_LOOP, "orbit_scale": 640, "orbit_x": 1160, "orbit_y": 400,
        }),
        ("board", SCENES / "scene-074_board-19-panel-2_v01.png", 6.0, {"zoom_in": False}),
        ("board", SCENES / "scene-081_board-21-panel-1_v01.png", 6.5, {
            "zoom_in": True, "orbit": ORBIT_LOOP, "orbit_scale": 600, "orbit_x": 1240, "orbit_y": 460,
        }),
        ("board", SCENES / "scene-084_board-21-panel-4_v01.png", 6.0, {"zoom_in": True}),
        ("inscene", ORBIT_INSCENE["ending"], 8.0, {}),
    ]

    with tempfile.TemporaryDirectory(prefix="orbit_v15_concept_") as td:
        td = Path(td)
        parts: list[Path] = []
        t = 0.0
        for i, (kind, src, dur, opts) in enumerate(beats):
            part = td / f"part_{i:03d}.mp4"
            print(f"[{i+1}/{len(beats)}] {kind} {dur:.1f}s  (t={t:.1f})")
            if kind == "brand":
                render_brand(part, dur)
            elif kind == "inscene":
                assert src is not None
                render_inscene(src, part, dur)
            else:
                assert src is not None and src.exists(), src
                render_board(src, part, dur, **opts)
            parts.append(part)
            t += dur

        concat = td / "concat.txt"
        concat.write_text("".join(f"file '{p}'\n" for p in parts))
        pic = td / "picture.mp4"
        print(f"Concat ~{t:.1f}s…")
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat),
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS), str(pic),
        ])

        print("Mux audio…")
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(pic), "-i", str(audio),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
            "-shortest", "-movflags", "+faststart", str(OUT),
        ])

        # QC stills
        for ss in (3, 18, 28, 45, 70):
            qc = ROOT / f"09_Final-Export/_qc_v15_concept_{ss}s.png"
            run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", str(ss), "-i", str(OUT), "-frames:v", "1", str(qc),
            ])
        print(f"DONE → {OUT}")
        print(f"duration target ~{t:.1f}s")


if __name__ == "__main__":
    main()
