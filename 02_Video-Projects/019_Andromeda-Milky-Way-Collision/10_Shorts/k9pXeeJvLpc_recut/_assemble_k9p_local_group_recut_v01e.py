#!/usr/bin/env python3
"""k9pXeeJvLpc Local Group Short recut v01e (from v01d) — Ben-approved (5 Oct 2026).

Fixes vs Studio cut:
- Captions from actual Local Group VO (not milkomeda / inheritance-not-doom)
- No ghost "What Else Is Coming" chapter card
- Clean VO tail (chapter 06 house take, ends on "others?")
- Same Andromeda plates/stills, shorter holds + gentle push
- £0 generation; no upload
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "04_Audio/tools"))

from onscreen_captions import render_beat_png, render_cta_png  # noqa: E402
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

W, H = 1080, 1920
FPS = 30
PLATES = HERE / "plates"
WORK = HERE / "work"
OUT = HERE / "06_Final-Exports"
FRAMES = HERE / "frame_sheet_v01e"
CH06 = REPO / (
    "02_Video-Projects/019_Andromeda-Milky-Way-Collision/02_Voiceover/parts/"
    "andromeda_collision_vo_v03_06_what-else-is-coming.mp3"
)
# STT times on ch06 (absolute): Local Group block 1.62 → 24.88
VO_START = 1.55
VO_END = 25.15  # pad past "others?"
LONG_TITLE = "What Happens When Andromeda Hits the Milky Way?"
# v01d: no raw video id on the end card (Claude 5991609023); title only
PILL_CY = 1250  # v01d: pill centre under the caption block

# Caption beats relative to trimmed VO (t=0 at VO_START)
# yellow = hook word line
BEATS = [
    # v01c: re-timed to Scribe word times on the trimmed VO (ch06 minus 1.55 s)
    (0.00, 2.55, [("local group", "yellow"), ("isn't a quiet suburb", "white")]),
    (2.95, 6.10, [("small family", "white"), ("two big spirals", "yellow")]),
    (6.40, 9.10, [("triangulum", "yellow"), ("third major player", "white")]),  # v01e: wide Orbit shot, caption at house y=720 is clear of him
    (9.30, 13.25, [("smaller satellites", "white"), ("shaping the path", "yellow")]),
    (13.40, 15.60, [("gravity", "yellow"), ("and mass", "white")]),
    (16.95, 20.45, [("milky way + andromeda", "white"), ("destiny", "yellow")]),
    (20.55, 23.45, [("or one possible future", "white"), ("among others?", "yellow")]),
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def still_push(src: Path, dest: Path, length: float, zoom_end: float = 1.08) -> None:
    # Pre-scale with PIL to 1080x1920 so zoompan cannot explode memory on large PNGs.
    frames = max(1, int(round(length * FPS)))
    staged = WORK / f"_still_{dest.stem}.png"
    im = Image.open(src).convert("RGB")
    # cover-crop to 9:16
    tw, th = im.size
    target_aspect = W / H
    if tw / th > target_aspect:
        nw = int(th * target_aspect)
        left = (tw - nw) // 2
        im = im.crop((left, 0, left + nw, th))
    else:
        nh = int(tw / target_aspect)
        top = (th - nh) // 2
        im = im.crop((0, top, tw, top + nh))
    im = im.resize((W, H), Image.Resampling.LANCZOS)
    staged.parent.mkdir(parents=True, exist_ok=True)
    im.save(staged)
    vf = (
        f"zoompan=z='min({zoom_end},1+(on/{max(frames-1,1)})*({zoom_end}-1))':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
        f"setsar=1,format=yuv420p"
    )
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-loop", "1", "-i", str(staged),
            "-frames:v", str(frames),
            "-vf", vf, "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            str(dest),
        ]
    )


def motion_clip(src: Path, dest: Path, length: float, start: float = 0.3) -> None:
    vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={FPS},format=yuv420p"
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-ss", f"{start:.3f}", "-i", str(src),
            "-t", f"{length:.3f}", "-an", "-vf", vf,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            str(dest),
        ]
    )


def end_card(dest: Path, length: float = 3.0) -> None:
    """Related-long end card on Local Group still — no ghost chapter text."""
    bg = PLATES / "OPEN_01_local_group.png"
    card = WORK / "end_card_base.png"
    im = Image.open(bg).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    # darken
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    im = Image.blend(im, dark, 0.45)
    draw = ImageDraw.Draw(im)
    font_t = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Black.ttf", 46)
    font_id = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Black.ttf", 36)
    # pill
    pad_x, pad_y = 48, 36
    # wrap title
    words = LONG_TITLE.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), trial, font=font_t)
        if bbox[2] - bbox[0] > W - 160 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    line_h = 56
    block_h = line_h * len(lines)
    box_w = W - 120
    box_h = block_h + pad_y * 2
    x0 = (W - box_w) // 2
    y0 = PILL_CY - box_h // 2
    draw.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], radius=18, fill=(0, 0, 0, 210))
    y = y0 + pad_y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_t)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y), line, font=font_t, fill=(255, 255, 255))
        y += line_h
    im.save(card)
    still_push(card, dest, length, zoom_end=1.03)


def whoosh(dest: Path) -> None:
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", "anoisesrc=color=pink:duration=0.4:sample_rate=48000",
            "-af", "highpass=f=300,lowpass=f=2200,afade=t=in:st=0:d=0.02,afade=t=out:st=0.1:d=0.28,volume=0.5",
            str(dest),
        ]
    )


def main() -> None:
    global WORK
    WORK = HERE / "work_v01e"
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)
    caps = WORK / "caps"
    caps.mkdir(exist_ok=True)

    # 1) Clean VO from house chapter take
    vo = WORK / "vo_local_group_clean.wav"
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-ss", f"{VO_START:.3f}", "-to", f"{VO_END:.3f}",
            "-i", str(CH06),
            "-af", "afade=t=in:st=0:d=0.02,afade=t=out:st=23.2:d=0.35",
            "-ar", "48000", "-ac", "2", str(vo),
        ]
    )
    vo_dur = dur(vo)
    print(f"VO clean {vo_dur:.2f}s", flush=True)

    # 2) Picture beds — shorter holds (~3.6–4.2s) + gentle motion; same plates family
    segs: list[Path] = []
    # v01e (Claude 5991688273): drop the Omni close-up entirely. Hold the on-model
    # wide Orbit shot (omni_still) through beat 3, cut to the Andromeda+satellites
    # galaxy plate at 9.20 s for beat 4 ("smaller satellites", 9.30 s).
    pic_budget = max(1.0, vo_dur - 2.8)  # leave ~2.8s for end card
    P0_LEN = 3.51
    ORBIT_CUT = 9.20
    rest = round((pic_budget - ORBIT_CUT) / 3, 3)
    plan = [
        ("p0", "still", PLATES / "OPEN_01_local_group.png", P0_LEN),
        ("p1", "still", PLATES / "omni_still.png", round(ORBIT_CUT - P0_LEN, 3)),  # wide Orbit, beats 2-3
        ("p3", "still", PLATES / "SCIENCE_A_andromeda_smudge_spiral.png", rest),  # beat 4 galaxy plate
        ("p4", "still", PLATES / "veo_still.png", rest),
        ("p5", "still", PLATES / "SCIENCE_C_disks_stars_miss.png", rest),
    ]
    t_cursor = 0.0
    for name, kind, src, length in plan:
        dest = WORK / f"{name}.mp4"
        still_push(src, dest, length, zoom_end=1.05 if name == "p1" else 1.07)
        segs.append(dest)
        print(f"  {name} {kind} {length:.2f}s @ {t_cursor:.2f}", flush=True)
        t_cursor += length

    end = WORK / "p_end.mp4"
    end_len = max(2.5, vo_dur - t_cursor + 0.4)
    end_card(end, end_len)
    segs.append(end)
    print(f"  end card {end_len:.2f}s", flush=True)

    # concat picture
    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in segs))
    picture = WORK / "picture_raw.mp4"
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "concat", "-safe", "0", "-i", str(lst),
            "-c", "copy", str(picture),
        ]
    )
    # ensure exact vo_dur + small pad for end card visibility
    target = max(vo_dur + 0.15, dur(picture))
    picture_fit = WORK / "picture.mp4"
    # pad or trim
    pd = dur(picture)
    if pd < target:
        pad = target - pd
        run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-i", str(picture),
                "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:d={pad:.3f}:r={FPS}",
                "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
                "-map", "[v]", "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                str(picture_fit),
            ]
        )
    else:
        run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-i", str(picture), "-t", f"{target:.3f}",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-an",
                str(picture_fit),
            ]
        )
    print(f"picture {dur(picture_fit):.2f}s", flush=True)

    # 3) Caption PNGs + overlay filter
    overlay_inputs = []
    filter_parts = []
    vlabel = "[0:v]"
    for i, beat in enumerate(BEATS):
        a, b, lines = beat[:3]
        yc = beat[3] if len(beat) > 3 else 720
        png = caps / f"beat_{i:02d}.png"
        render_beat_png(png, lines, pointsize=88, y_center=yc)
        overlay_inputs += ["-i", str(png)]
        idx = i + 1
        out = f"[v{i}]"
        filter_parts.append(
            f"{vlabel}[{idx}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'{out}"
        )
        vlabel = out
    # soft CTA in last 2.2s of VO (before end card dominates)
    cta = caps / "cta.png"
    render_cta_png(cta, "full film linked →", pointsize=44, y=1500)
    overlay_inputs += ["-i", str(cta)]
    cta_i = len(BEATS) + 1
    cta_a = max(0.0, vo_dur - 2.4)
    cta_b = vo_dur - 0.15
    filter_parts.append(
        f"{vlabel}[{cta_i}:v]overlay=0:0:enable='between(t,{cta_a:.3f},{cta_b:.3f})'[vc]"
    )
    filter_parts.append("[vc]format=yuv420p[vout]")
    fc = ";".join(filter_parts)

    pictured = WORK / "picture_captioned.mp4"
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(picture_fit), *overlay_inputs,
            "-filter_complex", fc,
            "-map", "[vout]", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            str(pictured),
        ]
    )

    # 4) Whoosh + mux VO
    wh = WORK / "whoosh.wav"
    whoosh(wh)
    final = OUT / "k9pXeeJvLpc_local_group_recut_v01e.mp4"
    # mix: VO full + whoosh at 0
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(pictured),
            "-i", str(vo),
            "-i", str(wh),
            "-filter_complex",
            (
                f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[vo];"
                f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.45,"
                f"apad=whole_dur={dur(pictured):.3f}[wh];"
                f"[vo][wh]amix=inputs=2:duration=first:dropout_transition=0[a]"
            ),
            "-map", "0:v", "-map", "[a]",
            *shorts_encode_args(fps=FPS),
            "-shortest",
            str(final),
        ]
    )
    print(f"FINAL {final} {dur(final):.2f}s", flush=True)

    # 5) Frame sheet
    for t in (0.4, 2.0, 5.0, 9.0, 13.0, 17.0, 21.0, min(dur(final) - 0.3, 24.0)):
        run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-ss", f"{t:.2f}", "-i", str(final), "-frames:v", "1",
                str(FRAMES / f"recut_t{t:.1f}.jpg"),
            ]
        )
    meta = {
        "source_id": "k9pXeeJvLpc",
        "title": "Our Galaxy's Final Destination (Local Group recut v01e)",
        "vo": str(vo),
        "vo_source": str(CH06),
        "vo_trim": [VO_START, VO_END],
        "vo_dur_s": round(vo_dur, 3),
        "final": str(final),
        "final_dur_s": round(dur(final), 3),
        "beats": BEATS,
        "plates": [str(p[2]) for p in plan],
        "fixes": [
            "captions from Local Group VO",
            "no What Else Is Coming ghost",
            "clean VO tail ending on others?",
            "shorter holds + gentle push",
            "£0 no upload",
            "v01d: end card title only, pill y=1250",
            "v01e: omni close-up dropped; wide on-model Orbit still held 3.51-9.20 s through beat 3",
            "v01e: cut to Andromeda+satellites plate at 9.20 s for beat 4",
            "v01e: beat 3 caption back at y=720 (clear of Orbit in wide shot)",
        ],
    }
    (HERE / "RECUT_v01e_REPORT.json").write_text(json.dumps(meta, indent=2) + "\n")
    (HERE / "RECUT_v01e_REPORT.md").write_text(
        f"""# k9pXeeJvLpc Local Group recut v01e\n\nv01e = v01d with Claude 5991688273 fixes: the Omni close-up is dropped entirely (its right eye was malformed). The on-model wide Orbit still (both eyes round with pupils) holds 3.51–9.20 s through beat 3, then cuts to the Andromeda + satellites galaxy plate for beat 4 ("smaller satellites"). Beat 3 caption back at y=720, clear of Orbit. Kept from v01d: end card title only, pill at y={PILL_CY}; open-motion warn accepted.

- **Final:** `{final}`
- **Duration:** {dur(final):.2f}s
- **VO:** chapter 06 house take trimmed {VO_START:.2f}–{VO_END:.2f}s → clean end on “others?”
- **Captions:** Local Group VO beats (yellow hooks). No milkomeda / inheritance-not-doom. No ghost chapter card.
- **Picture:** OPEN_01_local_group + cleaned Studio plates + omni night-sky + SCIENCE_A/B stills; ~3.6–4.0s holds with gentle push.
- **Spend:** £0. **Upload:** not done.
- **Frame sheet:** `{FRAMES}`
"""
    )
    print("REPORT written", flush=True)


if __name__ == "__main__":
    main()
