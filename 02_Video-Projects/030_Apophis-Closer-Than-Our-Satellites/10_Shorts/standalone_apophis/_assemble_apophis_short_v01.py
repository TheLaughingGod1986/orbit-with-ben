#!/usr/bin/env python3
"""030 Apophis standalone Short v01 (J0226, split from J0223). Does not upload or schedule. No spend.

Pattern: audits/STANDALONE_SHORTS_TEST_2026-10/_assemble_standalone_shorts_v01.py. The VO is pause-trimmed (gaps over
0.4 s, like _pause_trim_v01.py). Picture: the Veo rock (J0223) composited with a lighten blend over graded NASA plates,
which are dimmed under a soft matte of the rock so the plate doesn't show through its lit side; the Omni Orbit insert on
"Stay, and I'll show you how close"; J0225's DATA scale overlay landing on "36,000"; the last row runs the rock back to
frame 0 so "and watch..." loops. Audio: trimmed VO, the standalone-Shorts bed, house rumble at frame 0, one tick.
Usage: _assemble_apophis_short_v01.py [--test]   (--test renders a still sheet of each row only)
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SA = REPO / "00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10"
sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(SA))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import _assemble_standalone_shorts_v01 as sa  # noqa: E402

PLATES = Path("/private/tmp/owb_030_short/plates")
WORK = Path("/private/tmp/owb_030_short/build_v01")
KIT = Path("/private/tmp/owb_sa_shorts/sfx_kit_v01")
BED = SA / "05_Music/owb-standalone-shorts_score_bed_v01.mp3"
VO_DIR = HERE / "02_Voiceover"
STEM = "030_apophis_short_vo_v01"
VEO = HERE / "04_Generated-Clips/veo_v01/apophis_rock_tumble_veo_v01.mp4"
OMNI = HERE / "04_Generated-Clips/omni_v01/orbit_geo_sat_omni_v01.mp4"
OVERLAY = HERE / "code_graphics_v01/code_graphic_030short_r05_scale_v01.mov"
OUT = HERE / "06_Final-Exports"
FINAL_STEM = "030_apophis_short_v01"
AIR = "2026-10-22"

W, H, FPS = sa.W, sa.H, sa.FPS
HOOK_END, TITLE, HOLD, MAX_TOTAL = 2.2, (9.0, 14.0), 3.0, 25.5
LOOP_XFADE = 0.5
MAX_GAP, LEAD, TAIL = 0.40, 0.10, 0.35
VO_GAIN, BED_GAIN, BED_HOLD_GAIN, RUMBLE_GAIN = 1.0, 0.065, 0.35, 0.45
FIX = {"meters": "metres", "kilometers": "kilometres"}
SPEC = {"hook": (("CLOSER", "THAN"), ("SATELLITES",)), "yellow": "SATELLITES",
        "title": ("An Asteroid Will Skim Past", "Earth on Friday the 13th")}


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pause_trim() -> tuple[Path, list[dict], dict]:
    raw = json.loads((VO_DIR / "stt" / STEM / "stt_raw.json").read_text())
    words = [w for w in raw["words"] if w.get("type", "word") == "word"]
    src = VO_DIR / f"{STEM}.wav"
    total = sa.dur(src)
    keep, a = [], max(0.0, words[0]["start"] - LEAD)
    for prev, nxt in zip(words, words[1:]):
        if nxt["start"] - prev["end"] > MAX_GAP:
            keep.append((a, prev["end"] + MAX_GAP / 2))
            a = nxt["start"] - MAX_GAP / 2
    keep.append((a, min(total, words[-1]["end"] + TAIL)))

    def remap(t: float) -> float:
        out = 0.0
        for s, e in keep:
            if t <= e:
                return round(out + max(0.0, t - s), 3)
            out += e - s
        return round(out, 3)

    trim_dir = VO_DIR / "trim"
    trim_dir.mkdir(exist_ok=True)
    dest = trim_dir / f"{STEM}_trim.wav"
    parts = "".join(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
                    f"afade=t=out:st={e - s - 0.01:.3f}:d=0.01[p{i}];" for i, (s, e) in enumerate(keep))
    concat = "".join(f"[p{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[out]"
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", parts + concat, "-map", "[out]",
         "-ar", "48000", dest])
    mapped = []
    for w in words:
        word = w["text"].strip()
        core = word.rstrip(".,?!")
        mapped.append({"word": FIX.get(core.lower(), core) + word[len(core):],
                       "start": remap(w["start"]), "end": remap(w["end"])})
    (trim_dir / f"{STEM}_trim_words.json").write_text(json.dumps({"stem": STEM, "words": mapped}, indent=1) + "\n")
    meta = {"source_s": round(total, 2), "trimmed_s": round(sa.dur(dest), 2), "segments": len(keep),
            "max_gap_s": MAX_GAP}
    (trim_dir / "pause_trim_meta.json").write_text(json.dumps(meta, indent=1) + "\n")
    return dest, mapped, meta


def frames_of(video: Path, name: str, size: tuple[int, int], rgba: bool = False) -> list[Path]:
    d = WORK / f"frames_{name}"
    if not (d / ".done").exists():
        d.mkdir(parents=True, exist_ok=True)
        vf = f"scale={size[0]}:{size[1]}:flags=lanczos" + (",format=rgba" if rgba else "")
        args = ["ffmpeg", "-y", "-v", "error"] + (["-c:v", "prores"] if rgba else []) + ["-i", video, "-vf", vf]
        run(args + [d / ("%04d.png" if rgba else "%04d.jpg")] + ([] if rgba else ["-q:v", "2"]))
        (d / ".done").write_text("ok")
    return sorted(d.glob("*.png" if rgba else "*.jpg"))


def cropped(nasa_id: str, bottom: int = 40) -> Path:
    """The landscape ISS plates carry a white strip along the bottom edge; crop it off."""
    out = WORK / f"{nasa_id}_crop.jpg"
    im = Image.open(PLATES / f"{nasa_id}.jpg")
    im.crop((0, 0, im.width, im.height - bottom)).save(out, quality=95)
    return out


def grade(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = ImageEnhance.Color(im).enhance(1.18)
    return im


class Rock:
    """The Veo rock as a lighten layer plus a soft occluding matte; the Veo's own blue rim is keyed out."""

    def __init__(self, paths: list[Path]):
        self.paths = paths
        self.cache: dict[int, tuple[np.ndarray, np.ndarray]] = {}

    def layer(self, src_t: float, scale: float, dx: int, dy: int) -> tuple[np.ndarray, np.ndarray]:
        i = min(len(self.paths) - 1, max(0, int(round(src_t * 24))))
        key = (i, scale, dx, dy)
        if key in self.cache:
            return self.cache[key]
        im = Image.open(self.paths[i]).convert("RGB")
        # The rim's white core is neutral, so the blue key misses it; it is a smooth gradient and the rock is cratered.
        # A hard column ramp cuts a step into that gradient and reads as texture, so the mask is measured unramped.
        blk = np.asarray(im).astype(np.float32).mean(axis=2).reshape(H // 8, 8, W // 8, 8).std(axis=(1, 3))
        tex = Image.fromarray((np.clip((blk - 4.0) / 6.0, 0.0, 1.0) * 255).astype(np.uint8))
        tex = tex.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(1.5)).resize((W, H), Image.BILINEAR)
        edge = np.clip((np.arange(W, dtype=np.float32) - 32.0) / 48.0, 0.0, 1.0)
        tex = np.asarray(tex).astype(np.float32) / 255.0 * edge[None, :]
        im = Image.fromarray((np.asarray(im).astype(np.float32) * tex[..., None]).astype(np.uint8))
        if scale != 1.0:
            im = im.resize((round(W * scale), round(H * scale)), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), (0, 0, 0))
        canvas.paste(im, ((W - im.width) // 2 + dx, (H - im.height) // 2 + dy))
        a = np.asarray(canvas).astype(np.float32)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        grey = np.clip(1.0 - (b - r - 6.0) / 14.0, 0.0, 1.0)
        rock = a * grey[..., None]
        lum = rock.mean(axis=2)
        m = np.clip((lum - 8.0) / 30.0, 0.0, 1.0)
        small = Image.fromarray((m * 255).astype(np.uint8)).resize((W // 8, H // 8), Image.BILINEAR)
        small = small.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(10))
        occ = np.asarray(small.resize((W, H), Image.BILINEAR)).astype(np.float32) / 255.0
        occ = np.clip(occ * 2.2, 0.0, 1.0)
        out = (rock, occ)
        if len(self.cache) > 64:
            self.cache.clear()
        self.cache[key] = out
        return out


def comp(plate: Image.Image, rock: Rock, src_t: float, place: tuple[float, int, int]) -> Image.Image:
    p = np.asarray(plate).astype(np.float32)
    layer, occ = rock.layer(src_t, *place)
    p = p * (1.0 - 0.92 * occ[..., None])
    return Image.fromarray(np.maximum(p, layer).clip(0, 255).astype(np.uint8))


def main() -> None:
    test = "--test" in sys.argv
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    vo, words, trim_meta = pause_trim()
    t_of = {}
    for w in words:
        t_of.setdefault(w["word"].rstrip(".,?!").lower(), w)
    last_end = words[-1]["end"]
    total = round(min(last_end + HOLD, MAX_TOTAL), 3)
    nframes = int(round(total * FPS))
    stay = t_of["stay"]["start"]
    close_end = t_of["close"]["end"]
    n36 = t_of["36,000"]["start"]

    veo = Rock(frames_of(VEO, "veo", (W, H)))
    omni = frames_of(OMNI, "omni", (W, H))
    ov_frames = frames_of(OVERLAY, "overlay", (W, H), rgba=True)
    ov_start = round(n36 - 0.5, 3)
    ov_end = ov_start + len(ov_frames) / FPS
    loop_start = round(ov_end, 3)

    dusk = sa.Plate(cropped("iss023e057948"), "cover", 0.35, 0.42)
    night = sa.Plate(cropped("iss023e058455"), "cover", 0.55, 0.50)
    day = sa.Plate(PLATES / "iss034e048455.jpg", "cover", 0.50, 0.40)
    for pl in (dusk, night, day):
        pl.im = grade(pl.im)

    omni_src0 = 1.6
    # (start, end, label, plate, zoom_from, zoom_to, rock: (src_from, src_to, scale, dx, dy) or None, kind)
    rows = [
        (0.0, stay, "iss023e057948 + Veo rock", dusk, 1.0, 1.08, (0.0, 2.6, 1.0, 0, -120), "rock"),
        (stay, close_end + 0.15, "Omni Orbit + geo satellite", None, 1.0, 1.0, None, "orbit"),
        (close_end + 0.15, TITLE[0], "iss034e048455 + Veo rock", day, 1.0, 1.06, (2.6, 4.8, 0.82, 60, -330), "rock"),
        (TITLE[0], TITLE[1], "iss023e058455 + Veo rock (title)", night, 1.04, 1.12, (4.8, 8.0, 0.9, 40, 60), "rock"),
        (TITLE[1], loop_start, "iss034e048455 (DATA overlay)", day, 1.10, 1.22, None, "plate"),
        (loop_start, total, "iss023e057948 + Veo rock (loop to frame 0)", dusk, 1.08, 1.0, (2.6, 0.0, 1.0, 0, -120),
         "loop"),
    ]

    def picture(t: float) -> Image.Image:
        i = max(j for j, r in enumerate(rows) if r[0] <= t)
        s, e, _, plate, z0, z1, rk, kind = rows[i]
        k = (t - s) / max(e - s, 1e-3)
        if kind == "orbit":
            src = omni_src0 + (t - s)
            idx = min(len(omni) - 1, int(round(src * 24)))
            return Image.open(omni[idx]).convert("RGB")
        if i == 0:
            x = min(t / sa.OPEN_PUSH_S, 1.0)
            z = z0 * (1 + 0.12 * (1 - (1 - x) ** 2)) + (z1 - z0) * k
        else:
            z = z0 + (z1 - z0) * sa.ease(k)
        frame = plate.frame(z)
        if rk is not None:
            src_t = rk[0] + (rk[1] - rk[0]) * k
            frame = comp(frame, veo, src_t, rk[2:])
        if kind == "loop" and t - s < LOOP_XFADE:
            prev = rows[i - 1][3].frame(rows[i - 1][5])
            frame = Image.blend(prev, frame, sa.ease((t - s) / LOOP_XFADE))
        return frame

    hook, title = sa.hook_png(SPEC), sa.title_png(SPEC)
    caps = sa.captions(words, total)

    if test:
        times = [0.0, 1.0, stay + 0.8, close_end + 1.0, 11.0, ov_start + 2.0, loop_start + 1.0, total - 0.05]
        tiles = []
        for t in times:
            f = picture(t).convert("RGBA")
            if t < HOOK_END:
                f.alpha_composite(hook)
            if TITLE[0] <= t < TITLE[1]:
                f.alpha_composite(title)
            if ov_start <= t < ov_end:
                f.alpha_composite(Image.open(ov_frames[int((t - ov_start) * FPS)]).convert("RGBA"))
            tiles.append(f.convert("RGB").resize((270, 480)))
        sheet = Image.new("RGB", (270 * len(tiles), 480))
        for i, im in enumerate(tiles):
            sheet.paste(im, (270 * i, 0))
        sheet.save(WORK / "test_sheet.jpg", quality=88)
        print(json.dumps({"total": total, "stay": stay, "close_end": close_end, "n36": n36, "ov": [ov_start, ov_end],
                          "loop": loop_start, "trim": trim_meta, "sheet": str(WORK / "test_sheet.jpg")}))
        return

    raw = WORK / "picture.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-vf", "noise=alls=4:allf=t,format=yuv420p",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "14", str(raw)], stdin=subprocess.PIPE)
    for f in range(nframes):
        t = f / FPS
        frame = picture(t).convert("RGBA")
        if t < HOOK_END:
            frame.alpha_composite(hook)
        if TITLE[0] <= t < TITLE[1]:
            frame.alpha_composite(title)
        if ov_start <= t < ov_end:
            frame.alpha_composite(Image.open(ov_frames[min(len(ov_frames) - 1, int((t - ov_start) * FPS))])
                                  .convert("RGBA"))
        for a, b, im in caps:
            if a <= t < b:
                frame.alpha_composite(im)
                break
        enc.stdin.write(frame.convert("RGB").tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("picture encode failed")

    tick_at = ov_start + 0.5
    vo_stem, bed_stem, sfx_stem = WORK / "stem_vo.wav", WORK / "stem_bed.wav", WORK / "stem_sfx.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", vo, "-af", f"aresample=48000,volume={VO_GAIN},apad,atrim=0:{total}",
         "-ac", "2", vo_stem])
    hold_ramp = f"if(lt(t,{last_end}),{BED_GAIN},{BED_GAIN}+({BED_HOLD_GAIN}-{BED_GAIN})*min((t-{last_end})/0.6,1))"
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", BED, "-af",
         f"aresample=48000,atrim=0:{total},volume='{hold_ramp}':eval=frame,afade=t=in:st=0:d=0.3,"
         f"afade=t=out:st={total - 0.6:.3f}:d=0.6", "-ac", "2", bed_stem])
    run(["ffmpeg", "-y", "-v", "error", "-i", KIT / "sfx_owb_rumble_low_v01.wav", "-i", KIT / "sfx_owb_tick_ui_v01.wav",
         "-filter_complex",
         f"[0:a]aresample=48000,volume={RUMBLE_GAIN},afade=t=out:st=1.6:d=0.8,atrim=0:2.4[s0];"
         f"[1:a]aresample=48000,volume=0.3,adelay={int(tick_at * 1000)}:all=1[tk];"
         f"[s0][tk]amix=inputs=2:duration=longest:normalize=0,apad,atrim=0:{total}[a]",
         "-map", "[a]", "-ac", "2", sfx_stem])
    stems_dir = OUT / f"{FINAL_STEM}_stems"
    stems_dir.mkdir(exist_ok=True)
    for p in (vo_stem, bed_stem, sfx_stem):
        run(["cp", p, stems_dir / p.name])

    final = OUT / f"{FINAL_STEM}.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-i", vo_stem, "-i", bed_stem, "-i", sfx_stem,
         "-filter_complex", "[1:a][2:a][3:a]amix=inputs=3:duration=first:normalize=0,"
                            "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]",
         "-map", "0:v", "-map", "[a]", *shorts_encode_args(fps=FPS), "-t", f"{total:.3f}",
         "-movflags", "+faststart", final])

    sheet = OUT / f"{FINAL_STEM}_frames.jpg"
    times = sorted({round(min(x, total - 0.1), 2) for x in
                    [0.0, 1.0, 2.5, *(r[0] + 0.6 for r in rows[1:]), 11.0, ov_start + 2.0, total - 0.1]})
    tiles = []
    for i, t in enumerate(times):
        p = WORK / f"sheet_{i}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", final, "-frames:v", "1", "-vf", "scale=270:480", p])
        tiles.append(p)
    canvas = Image.new("RGB", (270 * len(tiles), 500), (0, 0, 0))
    dd = ImageDraw.Draw(canvas)
    for i, (p, t) in enumerate(zip(tiles, times)):
        canvas.paste(Image.open(p), (270 * i, 0))
        dd.text((270 * i + 6, 482), f"{t:.1f}s", fill=(255, 255, 255))
    canvas.save(sheet, quality=90)

    cuts = [{"row": i + 1, "start_s": round(r[0], 3), "end_s": round(r[1], 3), "picture": r[2], "kind": r[7],
             "zoom": [r[4], r[5]], **({"veo_src_s": [r[6][0], r[6][1]]} if r[6] else {})}
            for i, r in enumerate(rows)]
    cuts[1]["omni_src_s"] = [omni_src0, round(omni_src0 + rows[1][1] - rows[1][0], 3)]
    meta = {
        "job": "J0226", "air_provisional": AIR, "title_on_screen": " ".join(SPEC["title"]),
        "file": str(final.relative_to(REPO)), "frames": str(sheet.relative_to(REPO)), "sha256": sha256(final),
        "duration_s": sa.dur(final), "vo": str(vo.relative_to(REPO)), "pause_trim": trim_meta,
        "words": len(words), "last_word_end_s": last_end, "spoken": " ".join(w["word"] for w in words),
        "hook": f"CLOSER THAN / SATELLITES (yellow SATELLITES), 0-{HOOK_END} s", "title_window_s": TITLE,
        "overlay": {"file": str(OVERLAY.relative_to(REPO)), "row": "code_graphic_030short_r05_scale_v01",
                    "window_s": [ov_start, round(ov_end, 3)], "spoken": "Many satellites orbit at 36,000",
                    "word_36000_s": n36},
        "cuts": cuts,
        "audio": {"bed": str(BED.relative_to(REPO)), "bed_gain": BED_GAIN, "bed_hold_gain": BED_HOLD_GAIN,
                  "sfx": f"rumble at 0 s (gain {RUMBLE_GAIN}), one tick at {tick_at:.2f} s",
                  "stems": str(stems_dir.relative_to(REPO)), "mix": "-14 LUFS, -1.5 dBTP"},
        "grain": "noise=alls=4:allf=t", "spend": "none",
        "plates": "plates_v01.json (graded: contrast 1.10, colour 1.18)",
    }
    (OUT / f"{FINAL_STEM}_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(final), "--air-date", AIR], capture_output=True, text=True)
    (OUT / f"{FINAL_STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    level = subprocess.run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "level", "--vo", str(vo_stem),
                            "--sfx", str(sfx_stem), "--bed", str(bed_stem), "--minutes", f"{total / 60:.3f}"],
                           capture_output=True, text=True)
    (OUT / f"{FINAL_STEM}_sfx_level.txt").write_text(level.stdout + level.stderr)
    print(f"== {final.name} {meta['duration_s']:.2f}s gate={gate.returncode} level={level.returncode}")
    print(gate.stdout[-2500:], level.stdout[-1200:], flush=True)


if __name__ == "__main__":
    main()
