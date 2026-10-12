#!/usr/bin/env python3
"""Assemble Friday 16 Oct Black Dwarf Short for Claude review.

Does not upload or schedule. World from approved cooling v02 still.
Orbit beat: try Omni from a composited start frame; if Omni fails, fall back to
a gentle still-float of Orbit over the cooling plate and flag it in meta.
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
ENV = REPO / "02_Video-Projects/019_Andromeda-Milky-Way-Collision/07_Edit-Project/.env"

OUT = HERE / "06_Final-Exports"
WORK = HERE / "_work_v01"
COVER_DIR = HERE / "08_Covers"

W, H = 1080, 1920
FPS = 30
LONG_TITLE = "What Happens When the Last Star Dies?"
AIR = "2026-10-16"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)


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
    # Mid-action cooling: slight push + optional vertical drift.
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


def make_orbit_start(dest: Path) -> Path:
    """Composite Orbit onto the cooling still as Omni I2V start (9:16)."""
    bg = Image.open(STILL).convert("RGBA").resize((W, H), Image.Resampling.LANCZOS)
    orbit = Image.open(ORBIT_REF).convert("RGBA")
    # Scale Orbit down so the cooling sphere stays hero.
    ow = int(W * 0.38)
    oh = int(orbit.height * ow / orbit.width)
    orbit = orbit.resize((ow, oh), Image.Resampling.LANCZOS)
    x = (W - ow) // 2
    y = int(H * 0.52)
    bg.alpha_composite(orbit, (x, y))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(b"")  # touch
    out = dest.with_suffix(".png")
    bg.convert("RGB").save(out, quality=95)
    return out


def try_omni(start: Path, dest: Path) -> dict:
    """Vertex Omni ONLY. Never AI Studio / GEMINI_API_KEY (never-list)."""
    meta = {"status": "skipped", "backend": "vertex"}
    # One-shot already done this session: reuse recorded Vertex error if present.
    prior = WORK / "orbit_omni_vertex_error.json"
    if os.environ.get("ORBIT_OMNI_SKIP") == "1" and prior.exists():
        try:
            data = json.loads(prior.read_text())
            data.setdefault("backend", "vertex")
            data["status"] = data.get("status") or "fail"
            data["note"] = "reused prior Vertex attempt this session (ORBIT_OMNI_SKIP=1)"
            return data
        except Exception as e:  # noqa: BLE001
            return {"status": "fail", "backend": "vertex", "error": f"prior_read: {e}"}
    try:
        from orbit_gemini_omni import generate_omni_clip  # noqa: WPS433
        from google import genai  # noqa: WPS433
    except Exception as e:  # noqa: BLE001
        meta = {"status": "import_fail", "backend": "vertex", "error": str(e)}
        return meta
    if dest.exists() and dest.stat().st_size > 200_000:
        return {"status": "keep", "backend": "vertex", "path": str(dest), "bytes": dest.stat().st_size}
    try:
        # Strip AI Studio keys — never route Omni through GEMINI_API_KEY.
        os.environ.pop("GEMINI_API_KEY", None)
        os.environ.pop("GOOGLE_API_KEY", None)
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
        project = os.environ.get("GOOGLE_CLOUD_PROJECT") or "gen-lang-client-0538779324"
        location = os.environ.get("GOOGLE_CLOUD_LOCATION") or "us-central1"
        client = genai.Client(vertexai=True, project=project, location=location)
        prompt = (
            "Silent picture only. Exactly one matte orange floating robot (Orbit): one large black "
            "curved visor, two cream eyes with dark pupils, stubby arms, one antenna, one soft "
            "underside glow, no legs. He drifts up toward a cooling white-hot sphere that is greying "
            "on one edge, reaches a hand toward it, then pulls back from the heat. Continuous motion. "
            "No text, no logo, no second Orbit, no second face. Thin starfield background."
        )
        t0 = time.time()
        generate_omni_clip(
            client,
            prompt,
            dest,
            orbit_ref=start,
            aspect_ratio="9:16",
        )
        meta = {
            "status": "ok",
            "backend": "vertex",
            "project": project,
            "location": location,
            "path": str(dest),
            "seconds": round(time.time() - t0, 1),
            "bytes": dest.stat().st_size,
        }
    except Exception as e:  # noqa: BLE001
        meta = {
            "status": "fail",
            "backend": "vertex",
            "project": os.environ.get("GOOGLE_CLOUD_PROJECT") or "gen-lang-client-0538779324",
            "location": os.environ.get("GOOGLE_CLOUD_LOCATION") or "us-central1",
            "error": f"{type(e).__name__}: {e}",
        }
        (WORK / "orbit_omni_vertex_error.json").write_text(json.dumps(meta, indent=2) + "\n")
    return meta


def orbit_still_float(start: Path, dest: Path, length: float = 3.5) -> None:
    """Fallback: gentle float of the composited start frame (interim if Omni down)."""
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
        f"zoompan=z='min(1.05,1.0+0.0005*on)':x='iw/2-(iw/zoom/2)':"
        f"y='ih/2-(ih/zoom/2)-0.35*on':d=1:s={W}x{H}:fps={FPS}"
    )
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-loop", "1", "-i", str(start),
            "-vf", vf, "-t", f"{length:.3f}", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            str(dest),
        ]
    )


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
    cover = COVER_DIR / "cover_friday-black-dwarf.jpg"
    im = Image.open(cover).convert("RGB")
    crop_h = int(t4.W * 9 / 16)
    y0 = (t4.H - crop_h) // 2
    im.crop((0, y0, t4.W, y0 + crop_h)).save(COVER_DIR / "cover_friday-black-dwarf_16x9.jpg", quality=90)
    return cover


def assemble() -> tuple[Path, dict]:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for p in (STILL, VO, ORBIT_REF):
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")

    vo_s = dur(VO)
    # Claude 5968102643: trim ~0.7s from loop hold only (was 4.0 → 3.3); don't touch VO.
    # Target ~26.9s inside 22–27 band (was 27.6 FAIL).
    loop_s = 3.3
    head_s = 1.5
    orbit_s = 3.5
    total = min(max(vo_s + 0.1, 22.0), 27.0)  # ~26.9 when vo≈26.8
    teach_s = total - head_s - orbit_s - loop_s
    if teach_s < 6.0:
        teach_s = 6.0
        total = head_s + orbit_s + teach_s + loop_s

    still_motion(STILL, WORK / "head.mp4", head_s, zoom_end=1.04, y_drift=0.15)
    still_motion(STILL, WORK / "teach.mp4", teach_s, zoom_end=1.08, y_drift=0.05)
    still_motion(STILL, WORK / "loop.mp4", loop_s, zoom_end=1.05, y_drift=0.12)

    start = make_orbit_start(WORK / "orbit_start")
    omni_dest = WORK / "orbit_omni.mp4"
    omni_meta = try_omni(start, omni_dest)
    if omni_meta.get("status") in {"ok", "keep"} and omni_dest.exists():
        # trim/normalize to orbit_s
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
        orbit_mode = "omni"
    else:
        orbit_still_float(start, WORK / "orbit.mp4", orbit_s)
        orbit_mode = "still_float_fallback"

    concat = WORK / "concat.txt"
    concat.write_text(
        "\n".join(
            f"file '{p}'"
            for p in [WORK / "head.mp4", WORK / "orbit.mp4", WORK / "teach.mp4", WORK / "loop.mp4"]
        )
        + "\n"
    )
    silent = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(silent)])
    pic_s = dur(silent)

    hook = WORK / "hook.png"
    title = WORK / "title.png"
    hook_png(hook)
    title_png(title)
    whoosh(WORK / "whoosh.m4a")

    title_start, title_end = 9.0, min(14.0, pic_s - loop_s)
    final = OUT / "friday_black_dwarf_why_none_yet_v01.mp4"
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
        "duration_s": dur(final),
        "vo_s": vo_s,
        "picture_s": pic_s,
        "head_s": head_s,
        "orbit_s": orbit_s,
        "teach_s": teach_s,
        "loop_s": loop_s,
        "orbit_in_s": head_s,
        "orbit_mode": orbit_mode,
        "omni": omni_meta,
        "title_on_screen": LONG_TITLE,
        "title_window_s": [title_start, title_end],
        "hook": "NOT YET",
        "air": AIR,
        "still": str(STILL),
        "vo": str(VO),
    }
    (OUT / "friday_black_dwarf_why_none_yet_v01_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
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
    (OUT / "friday_black_dwarf_why_none_yet_v01_gate.json").write_text(gate.stdout or gate.stderr or "{}\n")
    # Soft note if Orbit used still-float
    if meta.get("orbit_mode") != "omni":
        print("NOTE: Orbit beat used still_float_fallback — Omni unavailable/failed; Claude soft note.", flush=True)
    if gate.returncode not in (0, 1):
        raise SystemExit(f"gate tool error {gate.returncode}")
    raise SystemExit(gate.returncode)


if __name__ == "__main__":
    main()
