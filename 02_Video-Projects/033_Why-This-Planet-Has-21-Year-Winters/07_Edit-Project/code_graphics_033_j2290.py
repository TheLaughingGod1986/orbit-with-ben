#!/usr/bin/env python3
"""J2290 £0 code graphics for film 033. No Orbit character, no Omni/Veo/Flow.

R29 is the seasonal dial Chief locked as the Option B fallback.
R55 is a pressure gauge on a Uranus plate whose NASA title is Uranus.
PIA00141's catalogue title is Miranda and PIA01361's is a moon montage, so
they are not graded here as a Uranus cloud deck. Neighbours of both rows
stay NASA plates in the stills lock, so these graphics are not back-to-back
with another code graphic.

Real globes only: Voyager PIA18182 (Uranus), NASA PIA18033 (catalogue title
Earth), Voyager PIA01490 (Miranda), Galileo PIA00405 (the Moon). A computer
render is not used as a planet body.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
HARVEST = ROOT / "03_Reference-Material" / "harvest_J2290_v01"
OUT = HERE / "code_graphics_J2290"
NAS_URANUS = Path("/Volumes/data/mac-mini-archive/scratch/J1199/plates/s4_uranus/PIA18182.jpg")
W, H, FPS = 1920, 1080, 12
NAVY = (24, 44, 74)
GOLD = (255, 207, 64, 255)
WHITE = (249, 248, 243, 255)
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
UA = "OrbitWithBenStudio/1.0 (film 033 code graphic source)"


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size)


def ease(t: float, a: float, b: float) -> float:
    if t <= a:
        return 0.0
    if t >= b:
        return 1.0
    x = (t - a) / (b - a)
    return x * x * (3 - 2 * x)


def cover(path: Path, mix: float = 0.62) -> Image.Image:
    im = Image.open(path).convert("RGB")
    scale = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left, top = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((left, top, left + W, top + H))
    base = Image.new("RGB", (W, H), NAVY)
    return Image.blend(base, im, mix).convert("RGBA")


def globe(path: Path, diameter: int) -> Image.Image:
    im = Image.open(path).convert("RGB")
    side = min(im.size)
    left, top = (im.width - side) // 2, (im.height - side) // 2
    im = im.crop((left, top, left + side, top + side)).resize((diameter, diameter), Image.Resampling.LANCZOS)
    circle = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(circle).ellipse((2, 2, diameter - 3, diameter - 3), fill=255)
    # Drop the near-black sky that otherwise rings the body. Oceans stay.
    sky = im.convert("L").point(lambda p: 0 if p < 12 else 255)
    from PIL import ImageChops
    im.putalpha(ImageChops.multiply(circle, sky))
    return im


def text(d: ImageDraw.ImageDraw, xy, words: str, size=64, fill=GOLD) -> None:
    if len(words.split()) > 4:
        raise ValueError("label over 4 words: " + words)
    d.text(xy, words, font=font(size), fill=fill, stroke_width=4, stroke_fill=(10, 20, 36, 230))


def credit(d: ImageDraw.ImageDraw, line: str) -> None:
    d.text((36, H - 52), line, font=font(28), fill=(220, 226, 234, 210))


def luma(im: Image.Image) -> float:
    g = im.convert("L")
    hist = g.histogram()
    total = sum(hist) or 1
    return sum(i * v for i, v in enumerate(hist)) / total


def render(name: str, seconds: float, draw) -> dict:
    frames = max(1, round(seconds * FPS))
    dest = OUT / name
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0", "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart",
        str(dest),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    mid_luma = None
    try:
        for i in range(frames):
            t = i / FPS
            frame = draw(t, seconds).convert("RGB")
            if i == frames // 2:
                mid_luma = luma(frame)
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError("ffmpeg failed for " + name)
    except BaseException:
        proc.kill()
        raise
    data = dest.read_bytes()
    return {
        "file": name,
        "seconds": seconds,
        "fps": FPS,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "mid_frame_mean_luma": round(mid_luma or 0, 1),
        "orbit_character": False,
        "review_status": "DRAFT_NOT_KEEP",
    }


def fetch_moon() -> Path:
    dest = HARVEST / "PIA00405.jpg"
    if dest.exists() and dest.stat().st_size > 10000:
        return dest
    HARVEST.mkdir(parents=True, exist_ok=True)
    url = "https://images-assets.nasa.gov/image/PIA00405/PIA00405~orig.jpg"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())
    return dest


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    uranus_path = NAS_URANUS if NAS_URANUS.exists() else HARVEST / "PIA00032.jpg"
    earth_path = HARVEST / "PIA18033.jpg"
    miranda_path = HARVEST / "PIA01490.jpg"
    limb_path = HARVEST / "PIA01488.jpg" if (HARVEST / "PIA01488.jpg").exists() else uranus_path
    hubble_path = HARVEST / "PIA01280.jpg" if (HARVEST / "PIA01280.jpg").exists() else uranus_path
    moon_path = fetch_moon()
    g_u = globe(uranus_path, 620)
    g_u_m = globe(uranus_path, 460)
    g_u_s = globe(uranus_path, 480)
    g_e = globe(earth_path, 460)
    g_e_s = globe(earth_path, 120)
    g_m = globe(miranda_path, 220)
    g_moon = globe(moon_path, 460)
    plate_u = cover(uranus_path, 0.58)
    plate_limb = cover(limb_path, 0.5)
    plate_h = cover(hubble_path, 0.5)
    plate_mir = cover(miranda_path, 0.55)

    def r29(t, dur):
        im = plate_u.copy()
        im.alpha_composite(g_u, (140, 200))
        d = ImageDraw.Draw(im)
        cx, cy, rad = 1360, 500, 250
        d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), outline=GOLD, width=8)
        d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=WHITE)
        # Quarter-orbit winter wedge grows in the second stage.
        sweep = 90 * ease(t, 4.15, 8.2)
        if sweep > 1:
            d.pieslice((cx - rad + 18, cy - rad + 18, cx + rad - 18, cy + rad - 18), -90, -90 + sweep, fill=(255, 207, 64, 90))
        ang = -math.pi / 2 + (t / dur) * math.tau
        px, py = cx + math.cos(ang) * (rad - 4), cy + math.sin(ang) * (rad - 4)
        d.ellipse((px - 12, py - 12, px + 12, py + 12), fill=GOLD)
        if t > 0.35:
            text(d, (1180, 80), "84-YEAR ORBIT", 60)
        if t > 4.3:
            text(d, (1140, 800), "21-YEAR WINTER", 60)
        if t > 8.4:
            text(d, (1188, 880), "1/4 OF ORBIT", 52, WHITE)
        credit(d, "NASA")
        return im

    def r55(t, dur):
        im = plate_limb.copy()
        d = ImageDraw.Draw(im)
        text(d, (80, 70), "NO SOLID SURFACE", 72)
        top, bot, x = 240, 960, 1500
        d.rounded_rectangle((x, top, x + 70, bot), radius=30, outline=WHITE, width=6)
        depth = ease(t, 0.4, dur - 0.6)
        y = top + 8 + (bot - top - 16) * depth
        if y > top + 9:
            d.rectangle((x + 8, top + 8, x + 62, y), fill=(255, 150, 70, 230) if depth > 0.45 else (120, 190, 220, 230))
        d.polygon([(x - 24, y), (x - 4, y - 12), (x - 4, y + 12)], fill=GOLD)
        if t > 0.5:
            text(d, (80, 200), "CLOUDS −224.2 °C", 48, WHITE)
        if depth > 0.55:
            text(d, (80, 860), "DEEP HEAT", 56)
        credit(d, "NASA")
        return im

    def r03(t, dur):
        im = plate_u.copy()
        # Shadow sweeps the left of the globe. The counter is the idea.
        d = ImageDraw.Draw(im)
        im.alpha_composite(g_u, (180, 180))
        shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shade)
        sweep = ease(t, 0.2, dur - 0.4)
        sd.pieslice((180, 180, 800, 800), 90, 90 + 180 * sweep, fill=(8, 16, 32, 150))
        im.alpha_composite(shade)
        n = int(round(21 * ease(t, 0.4, dur - 0.8)))
        text(d, (980, 380), f"{n} EARTH YEARS", 80)
        credit(d, "NASA")
        return im

    def r05(t, dur):
        im = Image.new("RGBA", (W, H), NAVY + (255,))
        im.alpha_composite(g_e, (200, 280))
        im.alpha_composite(g_u_m, (1160, 280))
        d = ImageDraw.Draw(im)
        # Protractor arcs. Earth stops at 23 degrees, Uranus continues to 98.
        e = 23.44 * ease(t, 0.3, 3.4)
        u = 97.77 * ease(t, 0.3, 5.2)
        d.arc((230, 310, 630, 710), -90, -90 + e, fill=GOLD, width=10)
        d.arc((1190, 310, 1590, 710), -90, -90 + u, fill=GOLD, width=10)
        text(d, (180, 80), "EARTH 23.44°", 56, WHITE)
        text(d, (1080, 80), "URANUS 97.77°", 56)
        if t > 5.0:
            text(d, (620, 900), "4× EARTH'S TILT", 64)
        credit(d, "NASA")
        return im

    def r14(t, dur):
        im = plate_u.copy()
        im.alpha_composite(g_u, (650, 160))
        d = ImageDraw.Draw(im)
        span = ease(t, 0.3, 4.8)
        x0, x1, y = 700, 700 + 520 * span, 470
        d.line((700, y, x1, y), fill=GOLD, width=8)
        d.line((700, y - 30, 700, y + 30), fill=GOLD, width=6)
        d.line((x1, y - 30, x1, y + 30), fill=GOLD, width=6)
        text(d, (700, 80), "51,118 KM", 72)
        if t > 5.2:
            for i in range(4):
                im.alpha_composite(g_e_s, (700 + i * 140, 760))
            text(d, (700, 920), "4× EARTH WIDE", 56, WHITE)
        credit(d, "NASA")
        return im

    def r26(t, dur):
        im = plate_u.copy()
        im.alpha_composite(g_u, (650, 180))
        d = ImageDraw.Draw(im)
        tilt = 97.77 * ease(t, 0.4, 4.0)
        ang = math.radians(tilt - 90)
        cx, cy = 960, 490
        dx, dy = math.cos(ang) * 340, math.sin(ang) * 340
        d.line((cx - dx, cy - dy, cx + dx, cy + dy), fill=GOLD, width=8)
        text(d, (80, 70), "97.77° TILT", 72)
        if t > 4.3:
            text(d, (80, 880), "RETROGRADE SPIN", 60, WHITE)
        credit(d, "NASA")
        return im

    def r35(t, dur):
        im = plate_h.copy()
        d = ImageDraw.Draw(im)
        parts = [(0.825, (210, 220, 230, 255), "82.5% H₂"), (0.152, (180, 190, 200, 255), "15.2% HE"), (0.023, (80, 200, 170, 255), "2.3% METHANE")]
        x = 180
        grow = ease(t, 0.3, 3.2)
        for frac, col, _ in parts:
            w = 900 * frac * grow
            d.rectangle((x, 180, x + w, 280), fill=col)
            x += w
        if t > 1.2:
            text(d, (180, 80), "2.3% METHANE", 64)
        if t > 4.2:
            # Red stops, blue-green continues.
            d.line((200, 480, 700, 700), fill=(220, 60, 50, 255), width=14)
            d.line((700, 700, 1500, 420), fill=(80, 220, 190, 255), width=14)
            text(d, (180, 860), "RED LIGHT ABSORBED", 48)
            text(d, (1100, 860), "BLUE-GREEN OUT", 48, WHITE)
        credit(d, "NASA")
        return im

    def r43(t, dur):
        im = plate_h.copy()
        d = ImageDraw.Draw(im)
        box = (1180, 220, 1780, 820)
        d.arc(box, 200, 340, fill=WHITE, width=16)
        sweep = 140 * ease(t, 0.3, 3.4)
        d.arc(box, 200, 200 + sweep, fill=GOLD, width=18)
        text(d, (80, 80), "900 KM/H", 80)
        if t > 3.6:
            text(d, (80, 200), "560 MPH", 64, WHITE)
        credit(d, "NASA")
        return im

    def r46(t, dur):
        im = plate_u.copy()
        im.alpha_composite(g_u, (650, 180))
        d = ImageDraw.Draw(im)
        cx, cy = 960, 490
        spin = ease(t, 0.3, 3.5)
        ang = math.radians(-90 + 97.77 * spin)
        d.line((cx - math.cos(ang) * 360, cy - math.sin(ang) * 360, cx + math.cos(ang) * 360, cy + math.sin(ang) * 360), fill=WHITE, width=8)
        if t > 4.6:
            mag = math.radians(-90 + 97.77 + 58.6 * ease(t, 4.6, 8.5))
            d.line((cx - math.cos(mag) * 300, cy - math.sin(mag) * 300, cx + math.cos(mag) * 300, cy + math.sin(mag) * 300), fill=GOLD, width=8)
            text(d, (60, 70), "58.6° MAGNETIC TILT", 56)
        if t > 9.2:
            # Offset mark, one third of the way from centre.
            ox, oy = cx + 110, cy - 40
            d.ellipse((ox - 16, oy - 16, ox + 16, oy + 16), fill=GOLD)
            text(d, (60, 880), "1/3 RADIUS OFFSET", 52, WHITE)
        credit(d, "NASA")
        return im

    def r52(t, dur):
        im = Image.new("RGBA", (W, H), NAVY + (255,))
        im.alpha_composite(g_u, (650, 160))
        d = ImageDraw.Draw(im)
        if t > 1.0:
            d.pieslice((700, 210, 1220, 730), -40, 40, fill=(40, 70, 110, 230))
            text(d, (60, 70), "HYDROGEN HELIUM CLOUDS", 44, WHITE)
        if t > 4.8:
            d.pieslice((760, 270, 1160, 670), -30, 30, fill=(40, 120, 140, 240))
            text(d, (60, 150), "≥ 80% FLUID", 64)
        if t > 9.2:
            d.ellipse((920, 450, 1000, 530), fill=(180, 140, 90, 255))
            text(d, (60, 880), "SMALL ROCKY CORE", 52)
        credit(d, "NASA")
        return im

    def r54(t, dur):
        im = Image.new("RGBA", (W, H), NAVY + (255,))
        d = ImageDraw.Draw(im)
        grow = ease(t, 0.3, 3.2)
        d.rectangle((520, 780 - 520 * grow, 640, 780), fill=(140, 200, 220, 255))
        d.rectangle((1100, 780 - 700 * grow, 1220, 780), fill=(220, 110, 60, 255))
        text(d, (400, 80), "CLOUDS −224.2 °C", 48, WHITE)
        text(d, (980, 80), "CORE 4,982 °C", 48)
        if t > 3.4:
            text(d, (520, 900), "5,000 °C HOTTER", 64)
        return im

    def r59(t, dur):
        im = Image.new("RGBA", (W, H), NAVY + (255,))
        im.alpha_composite(g_m, (280, 340))
        im.alpha_composite(g_moon, (1100, 250))
        d = ImageDraw.Draw(im)
        text(d, (180, 80), "MIRANDA 500 KM", 60)
        if t > 5.6:
            text(d, (180, 880), "1/7 THE MOON", 72, WHITE)
        credit(d, "NASA")
        return im

    def r08(t, dur):
        im = plate_u.copy()
        im.alpha_composite(g_u_s, (220, 260))
        d = ImageDraw.Draw(im)
        drop = ease(t, 0.4, 6.5)
        d.rounded_rectangle((1280, 200, 1360, 860), radius=28, outline=WHITE, width=6)
        y = 220 + 600 * drop
        d.rectangle((1290, y, 1350, 848), fill=(120, 200, 220, 255))
        text(d, (80, 70), "−224.2 °C", 80)
        if t > 6.8:
            text(d, (80, 880), "COLDER THAN NEPTUNE", 52, WHITE)
        credit(d, "NASA")
        return im

    def r61(t, dur):
        im = plate_mir.copy()
        d = ImageDraw.Draw(im)
        grow = ease(t, 0.4, 4.0)
        d.rectangle((1500, 860 - 640 * grow, 1560, 860), fill=GOLD)
        text(d, (70, 70), "12× GRAND CANYON", 64)
        credit(d, "NASA")
        return im

    jobs = [
        ("code_graphic_033_r29_seasonal_dial.mp4", 12.44, r29, "R29", "Between NASA R28 and NASA R30"),
        ("code_graphic_033_r55_pressure_gauge.mp4", 12.34, r55, "R55", "Between NASA R54 and NASA R56. Gauge, not an Orbit character."),
        ("code_graphic_033_r03_winter_counter.mp4", 5.19, r03, "R03", "Chapter open counter"),
        ("code_graphic_033_r05_tilt_gauge.mp4", 7.06, r05, "R05", "Earth PIA18033 and Uranus PIA18182"),
        ("code_graphic_033_r08_hook_temp_drop.mp4", 10.04, r08, "R08", "Uranus globe only; Neptune is named, not faked"),
        ("code_graphic_033_r14_diameter_scale.mp4", 10.39, r14, "R14", "Uranus caliper and four Earth globes"),
        ("code_graphic_033_r26_retrograde_tilt.mp4", 8.30, r26, "R26", "Tilt on real Uranus. No simulated Venus body."),
        ("code_graphic_033_r35_methane_spectrum.mp4", 8.16, r35, "R35", "Methane fraction, then the reflected colour"),
        ("code_graphic_033_r43_wind_gauge.mp4", 6.96, r43, "R43", "Wind arc over Hubble Uranus"),
        ("code_graphic_033_r46_corkscrew_magnet.mp4", 14.12, r46, "R46", "Spin axis, then 58.6° magnetic tilt"),
        ("code_graphic_033_r52_interior_mantle.mp4", 13.90, r52, "R52", "Cutaway inside the real Uranus globe"),
        ("code_graphic_033_r54_core_vs_cloud_temp.mp4", 5.77, r54, "R54", "Cloud versus core temperature"),
        ("code_graphic_033_r59_miranda_size_scale.mp4", 11.30, r59, "R59", "Miranda PIA01490 and the Moon PIA00405"),
        ("code_graphic_033_r61_canyon_depth_scale.mp4", 8.37, r61, "R61", "Depth bar over the Miranda plate"),
    ]
    clips = []
    for name, seconds, fn, row, note in jobs:
        print("render", name, flush=True)
        rec = render(name, seconds, fn)
        rec.update(row=row, note=note)
        clips.append(rec)
        print(" ", rec["mid_frame_mean_luma"], rec["sha256"][:12], flush=True)
    # The stills lock's filename for the R26 tilt. Same picture as the shot-list name.
    src = OUT / "code_graphic_033_r26_retrograde_tilt.mp4"
    alias = OUT / "code_graphic_033_r26_axial_tilt_97deg.mp4"
    alias.write_bytes(src.read_bytes())
    manifest = {
        "job": "J2290",
        "spend_gbp": 0,
        "orbit_character": False,
        "fps": FPS,
        "font": FONT,
        "r29": "Option B seasonal dial. No Orbit character. Neighbours R28 and R30 stay NASA.",
        "r55": "CODE pressure gauge over PIA01488 (NASA title: Uranus upper atmosphere) when that file is the limb plate, else PIA18182. PIA00141 is Miranda and PIA01361 is a moon montage in the NASA catalogue, so they are not used as a Uranus cloud deck. Neighbours R54 and R56 stay NASA.",
        "r26_alias": "code_graphic_033_r26_axial_tilt_97deg.mp4 is the same bytes as code_graphic_033_r26_retrograde_tilt.mp4",
        "magnetic_name": "The lock's code_graphic_033_r52_magnetic_offset_59deg.mp4 is the R46 corkscrew graphic. R52 is the interior cutaway, so the two are not the same file.",
        "appearance_cap": "These files are code graphics. They do not add a raw still appearance. svs20390 was not used.",
        "sources": {
            "uranus": str(uranus_path),
            "earth": str(earth_path),
            "miranda": str(miranda_path),
            "limb": str(limb_path),
            "hubble": str(hubble_path),
            "moon": str(moon_path),
        },
        "clips": clips,
    }
    (OUT / "CODE_GRAPHICS_J2290.json").write_text(json.dumps(manifest, indent=2) + "\n")
    # JSON copy next to the lock, where the PR can see it. The mp4s stay gitignored.
    (HERE / "CODE_GRAPHICS_J2290.json").write_text(json.dumps(manifest, indent=2) + "\n")
    low = [c["file"] for c in clips if c["mid_frame_mean_luma"] < 28]
    print("DONE", len(clips), "low_luma", low, flush=True)
    if low:
        raise SystemExit("near-black frames: " + ", ".join(low))


if __name__ == "__main__":
    main()
