#!/usr/bin/env python3
"""Assemble Friday Black Dwarf Short v02 — Claude FAIL 5968302935.

Orbit PiP placeholder OUT. Retry Vertex Omni 2–3×; if still down, cut Orbit beat
and stay on the cooling world picture. NASA stills on word timings + credits.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "04_Audio/tools"))

import build_yellow_white_short_thumbs_v04 as t4  # noqa: E402
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

STILL = (
    REPO
    / "02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/04_Generated-Clips/shorts_stills_v02/friday_black_dwarf_cooling_v02.png"
)
VO = HERE / "friday_black_dwarf_short_vo_v01.wav"
ORBIT_REF = REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
STILLS = HERE / "_work_v02_stills"

OUT = HERE / "06_Final-Exports"
WORK = HERE / "_work_v02"
COVER_DIR = HERE / "08_Covers"

W, H = 1080, 1920
FPS = 30
LONG_TITLE = "What Happens When the Last Star Dies?"
AIR = "2026-10-16"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)

# Absolute cut points from Claude word gaps
T_NEBULA = 4.92
T_SIRIUS = 6.85
T_COOL = 8.90
T_XDF = 15.50
T_END = 19.10


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def dur(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip()
    return float(out)


def whoosh(dest: Path) -> None:
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", "anoisesrc=color=pink:duration=0.45:sample_rate=48000",
            "-af", "highpass=f=300,lowpass=f=2200,afade=t=in:st=0:d=0.02,afade=t=out:st=0.12:d=0.33,volume=0.55",
            str(dest),
        ]
    )


def still_motion(src: Path, dest: Path, length: float, *, zoom_end: float = 1.06, y_drift: float = 0.0) -> None:
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
        f"zoompan=z='min({zoom_end},1.01+0.0007*on)':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)+{y_drift}*on':"
        f"d=1:s={W}x{H}:fps={FPS}"
    )
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-loop", "1", "-i", str(src),
            "-vf", vf, "-t", f"{length:.3f}", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            str(dest),
        ]
    )


def greying_sphere(dest: Path, length: float) -> None:
    """Cooling beat: crossfade base → grey_a → grey_b → grey_c over length."""
    a = STILLS / "sphere_base.png"
    b = STILLS / "sphere_grey_a.png"
    c = STILLS / "sphere_grey_b.png"
    d = STILLS / "sphere_grey_c.png"
    # four equal holds with short xfade
    seg = max(0.8, length / 4.0)
    parts = []
    for i, src in enumerate([a, b, c, d]):
        p = WORK / f"_grey_seg_{i}.mp4"
        still_motion(src, p, seg + 0.25, zoom_end=1.05 + 0.01 * i, y_drift=0.04)
        parts.append(p)
    # xfade chain
    if len(parts) == 1:
        run(["ffmpeg", "-y", "-v", "error", "-i", str(parts[0]), "-t", f"{length:.3f}", "-c", "copy", str(dest)])
        return
    xd = 0.25
    filt = []
    inputs = []
    for i, p in enumerate(parts):
        inputs += ["-i", str(p)]
    # progressive xfade
    cur = "[0:v]"
    offset = seg - xd
    for i in range(1, len(parts)):
        out = f"[g{i}]" if i < len(parts) - 1 else "[vout]"
        filt.append(f"{cur}[{i}:v]xfade=transition=fade:duration={xd}:offset={offset:.3f}{out}")
        cur = f"[g{i}]"
        offset += seg - xd
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            *inputs,
            "-filter_complex", ";".join(filt),
            "-map", "[vout]",
            "-t", f"{length:.3f}",
            "-an", "-r", str(FPS),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            str(dest),
        ]
    )


def make_orbit_start(dest: Path) -> Path:
    bg = Image.open(STILL).convert("RGBA").resize((W, H), Image.Resampling.LANCZOS)
    orbit = Image.open(ORBIT_REF).convert("RGBA")
    ow = int(W * 0.38)
    oh = int(orbit.height * ow / orbit.width)
    orbit = orbit.resize((ow, oh), Image.Resampling.LANCZOS)
    x = (W - ow) // 2
    y = int(H * 0.52)
    bg.alpha_composite(orbit, (x, y))
    out = dest.with_suffix(".png")
    bg.convert("RGB").save(out, quality=95)
    return out


def try_omni(start: Path, dest: Path, attempts: int = 3) -> dict:
    """Vertex Omni ONLY. Never AI Studio / GEMINI_API_KEY."""
    meta: dict = {"status": "skipped", "backend": "vertex", "attempts": []}
    prior = WORK / "orbit_omni_vertex_error.json"
    if prior.exists():
        try:
            data = json.loads(prior.read_text())
            atts = data.get("attempts") or []
            if len(atts) >= 3 and all(a.get("status") == "fail" for a in atts):
                data["status"] = "fail"
                data["backend"] = "vertex"
                data["note"] = "reused prior 3 Vertex 500 failures this session; Orbit beat cut"
                return data
        except Exception:
            pass
    try:
        from orbit_gemini_omni import generate_omni_clip  # noqa: WPS433
        from google import genai  # noqa: WPS433
    except Exception as e:  # noqa: BLE001
        return {"status": "import_fail", "backend": "vertex", "error": str(e)}

    if dest.exists() and dest.stat().st_size > 200_000:
        return {"status": "keep", "backend": "vertex", "path": str(dest), "bytes": dest.stat().st_size}

    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    project = os.environ.get("GOOGLE_CLOUD_PROJECT") or "gen-lang-client-0538779324"
    location = os.environ.get("GOOGLE_CLOUD_LOCATION") or "us-central1"
    prompt = (
        "Silent picture only. Exactly one matte orange floating robot (Orbit): one large black "
        "curved visor, two cream eyes with dark pupils, stubby arms, one antenna, one soft "
        "underside glow, no legs. He drifts up toward a cooling white-hot sphere that is greying "
        "on one edge, reaches a hand toward it, then pulls back from the heat. Continuous motion. "
        "No text, no logo, no second Orbit, no second face. Thin starfield background."
    )
    for i in range(attempts):
        t0 = time.time()
        try:
            client = genai.Client(vertexai=True, project=project, location=location)
            generate_omni_clip(
                client,
                prompt,
                dest,
                orbit_ref=start,
                aspect_ratio="9:16",
            )
            attempt = {
                "n": i + 1,
                "status": "ok",
                "seconds": round(time.time() - t0, 1),
                "bytes": dest.stat().st_size if dest.exists() else 0,
            }
            meta["attempts"].append(attempt)
            if dest.exists() and dest.stat().st_size > 200_000:
                meta.update(
                    {
                        "status": "ok",
                        "backend": "vertex",
                        "project": project,
                        "location": location,
                        "path": str(dest),
                        "bytes": dest.stat().st_size,
                        "attempt_used": i + 1,
                    }
                )
                return meta
        except Exception as e:  # noqa: BLE001
            attempt = {
                "n": i + 1,
                "status": "fail",
                "seconds": round(time.time() - t0, 1),
                "error": f"{type(e).__name__}: {e}",
            }
            meta["attempts"].append(attempt)
            time.sleep(2.0)
    meta["status"] = "fail"
    meta["backend"] = "vertex"
    meta["project"] = project
    meta["location"] = location
    (WORK / "orbit_omni_vertex_error.json").write_text(json.dumps(meta, indent=2) + "\n")
    return meta


def hook_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    words = [("NOT", WHITE), ("YET", YELLOW)]
    size = 86
    font = ImageFont.truetype(FONT, size)
    gap = 18
    widths = []
    for word, _ in words:
        box = draw.textbbox((0, 0), word, font=font, stroke_width=6)
        widths.append(box[2] - box[0])
    total = sum(widths) + gap
    while total > W - 48 and size > 48:
        size -= 2
        font = ImageFont.truetype(FONT, size)
        widths = []
        for word, _ in words:
            box = draw.textbbox((0, 0), word, font=font, stroke_width=6)
            widths.append(box[2] - box[0])
        total = sum(widths) + gap
    x = (W - total) // 2
    y = int(H * 0.34)
    for (word, color), ww in zip(words, widths):
        draw.text((x, y), word, font=font, fill=color, stroke_width=6, stroke_fill=(0, 0, 0, 255))
        x += ww + gap
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, 40)
    words = LONG_TITLE.replace("?", "").split()
    mid = len(words) // 2
    rows = [" ".join(words[:mid]), " ".join(words[mid:]) + "?"]
    y = int(H * 0.20)
    for row in rows:
        box = draw.textbbox((0, 0), row, font=font, stroke_width=5)
        x = (W - (box[2] - box[0])) // 2
        draw.text((x, y), row, font=font, fill=WHITE, stroke_width=5, stroke_fill=(0, 0, 0, 255))
        y += 52
    im.save(dest)


def build_cover() -> Path:
    COVER_DIR.mkdir(parents=True, exist_ok=True)
    cover = COVER_DIR / "cover_friday-black-dwarf.jpg"
    if cover.exists() and cover.stat().st_size > 20_000:
        return cover
    plate = COVER_DIR / "_plate.png"
    Image.open(STILL).convert("RGB").resize((W, H), Image.Resampling.LANCZOS).save(plate)
    job = {
        "id": "friday-black-dwarf",
        "plate": plate,
        "out_dir": COVER_DIR,
        "lines": ["NOT", "YET"],
        "yellow": {"YET"},
        "hero": 1,
        "related": "REXYxuLOBoI",
        "uk": "2026-10-16T11:30:00+01:00",
        "role": "friday_black_dwarf",
    }
    t4.compose(job)
    im = Image.open(cover).convert("RGB")
    crop_h = int(t4.W * 9 / 16)
    y0 = (t4.H - crop_h) // 2
    im.crop((0, y0, t4.W, y0 + crop_h)).save(COVER_DIR / "cover_friday-black-dwarf_16x9.jpg", quality=90)
    return cover


def assemble() -> tuple[Path, dict]:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    needed = [
        STILL, VO,
        STILLS / "ring_nebula_9x16.png",
        STILLS / "sirius_ab_9x16.png",
        STILLS / "xdf_e001651_9x16.png",
        STILLS / "sphere_base.png",
        STILLS / "sphere_grey_a.png",
        STILLS / "sphere_grey_b.png",
        STILLS / "sphere_grey_c.png",
    ]
    for p in needed:
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")

    vo_s = dur(VO)
    loop_s = 3.3
    # Try Omni for Orbit beat inside open window; else world-only open
    orbit_wanted_s = 3.0  # within 1.5–4.5-ish of Stay line
    start = make_orbit_start(WORK / "orbit_start")
    omni_dest = WORK / "orbit_omni.mp4"
    omni_meta = try_omni(start, omni_dest, attempts=3)

    use_omni = omni_meta.get("status") in {"ok", "keep"} and omni_dest.exists() and omni_dest.stat().st_size > 200_000
    if use_omni:
        head_s = 1.5
        orbit_s = min(orbit_wanted_s, T_NEBULA - head_s)
        still_motion(STILL, WORK / "head.mp4", head_s, zoom_end=1.04, y_drift=0.15)
        run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-i", str(omni_dest),
                "-t", f"{orbit_s:.3f}",
                "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1",
                "-an", "-r", str(FPS),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                str(WORK / "orbit.mp4"),
            ]
        )
        # pad/trim open to T_NEBULA
        open_used = head_s + orbit_s
        if open_used < T_NEBULA - 0.05:
            still_motion(STILL, WORK / "open_pad.mp4", T_NEBULA - open_used, zoom_end=1.03, y_drift=0.1)
            open_parts = [WORK / "head.mp4", WORK / "orbit.mp4", WORK / "open_pad.mp4"]
        else:
            open_parts = [WORK / "head.mp4", WORK / "orbit.mp4"]
        orbit_mode = "omni"
    else:
        # CUT Orbit beat — stay on world picture for whole open (Claude fallback)
        still_motion(STILL, WORK / "open.mp4", T_NEBULA, zoom_end=1.05, y_drift=0.12)
        open_parts = [WORK / "open.mp4"]
        orbit_mode = "cut_omni_down"
        orbit_s = 0.0
        head_s = T_NEBULA

    nebula_s = T_SIRIUS - T_NEBULA
    sirius_s = T_COOL - T_SIRIUS
    cool_s = T_XDF - T_COOL
    xdf_s = T_END - T_XDF

    still_motion(STILLS / "ring_nebula_9x16.png", WORK / "nebula.mp4", nebula_s, zoom_end=1.08)
    still_motion(STILLS / "sirius_ab_9x16.png", WORK / "sirius.mp4", sirius_s, zoom_end=1.06)
    greying_sphere(WORK / "cool.mp4", cool_s)
    still_motion(STILLS / "xdf_e001651_9x16.png", WORK / "xdf.mp4", xdf_s, zoom_end=1.07)
    still_motion(STILL, WORK / "endhold.mp4", max(0.5, (vo_s + 0.1) - T_END - loop_s + loop_s), zoom_end=1.04, y_drift=0.08)
    # endhold covers from T_END through before loop; then loop
    end_s = max(0.4, vo_s + 0.1 - T_END - loop_s)
    if end_s < 0.4:
        end_s = 0.5
    still_motion(STILL, WORK / "endhold.mp4", end_s, zoom_end=1.04, y_drift=0.08)
    still_motion(STILL, WORK / "loop.mp4", loop_s, zoom_end=1.05, y_drift=0.12)

    parts = open_parts + [
        WORK / "nebula.mp4",
        WORK / "sirius.mp4",
        WORK / "cool.mp4",
        WORK / "xdf.mp4",
        WORK / "endhold.mp4",
        WORK / "loop.mp4",
    ]
    concat = WORK / "concat.txt"
    concat.write_text("\n".join(f"file '{p}'" for p in parts) + "\n")
    silent = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(silent)])
    pic_s = dur(silent)

    # Trim into 22–27 band if needed (trim loop only)
    if pic_s > 27.0:
        target = 26.9
        trim_loop = max(2.5, loop_s - (pic_s - target))
        still_motion(STILL, WORK / "loop.mp4", trim_loop, zoom_end=1.05, y_drift=0.12)
        loop_s = trim_loop
        parts = open_parts + [
            WORK / "nebula.mp4",
            WORK / "sirius.mp4",
            WORK / "cool.mp4",
            WORK / "xdf.mp4",
            WORK / "endhold.mp4",
            WORK / "loop.mp4",
        ]
        concat.write_text("\n".join(f"file '{p}'" for p in parts) + "\n")
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(silent)])
        pic_s = dur(silent)

    hook = WORK / "hook.png"
    title = WORK / "title.png"
    hook_png(hook)
    title_png(title)
    whoosh(WORK / "whoosh.m4a")

    title_start, title_end = 9.0, min(14.0, pic_s - loop_s)
    final = OUT / "friday_black_dwarf_why_none_yet_v02.mp4"
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(silent),
            "-i", str(hook),
            "-i", str(title),
            "-i", str(VO),
            "-i", str(WORK / "whoosh.m4a"),
            "-filter_complex",
            (
                f"[1:v]format=rgba,scale={W}:{H}[hk];"
                f"[2:v]format=rgba,scale={W}:{H}[ttl];"
                f"[0:v][hk]overlay=0:0:enable='between(t,0,2.2)'[v1];"
                f"[v1][ttl]overlay=0:0:enable='between(t,{title_start:.3f},{title_end:.3f})',format=yuv420p[v];"
                f"[3:a]volume=1,apad[va];[4:a]adelay=0|0,volume=0.45[wh];"
                f"[va][wh]amix=inputs=2:duration=first:dropout_transition=0[a]"
            ),
            "-map", "[v]", "-map", "[a]",
            *shorts_encode_args(fps=FPS),
            "-t", f"{pic_s:.3f}",
            "-movflags", "+faststart",
            str(final),
        ]
    )
    meta = {
        "file": str(final),
        "version": "v02",
        "duration_s": dur(final),
        "vo_s": vo_s,
        "picture_s": pic_s,
        "cuts_s": [0.0, T_NEBULA, T_SIRIUS, T_COOL, T_XDF, T_END],
        "orbit_mode": orbit_mode,
        "orbit_s": orbit_s if use_omni else 0.0,
        "omni": omni_meta,
        "title_on_screen": LONG_TITLE,
        "title_window_s": [title_start, title_end],
        "hook": "NOT YET",
        "air": AIR,
        "claude_fix": "5968302935",
        "orbit_pip_placeholder": False,
        "vo": str(VO),
    }
    (OUT / "friday_black_dwarf_why_none_yet_v02_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)
    return final, meta


def main() -> None:
    final, meta = assemble()
    cover = build_cover()
    print("COVER", cover, flush=True)
    gate = subprocess.run(
        [
            sys.executable,
            str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
            "check", str(final), "--air-date", AIR, "--json",
        ],
        capture_output=True,
        text=True,
    )
    print(gate.stdout)
    print(gate.stderr, file=sys.stderr)
    (OUT / "friday_black_dwarf_why_none_yet_v02_gate.json").write_text(gate.stdout or gate.stderr or "{}\n")
    if meta.get("orbit_mode") != "omni":
        print("NOTE: Orbit beat CUT — Omni unavailable after retries; world picture only on open.", flush=True)
    if gate.returncode not in (0, 1):
        raise SystemExit(f"gate tool error {gate.returncode}")
    raise SystemExit(gate.returncode)


if __name__ == "__main__":
    main()
