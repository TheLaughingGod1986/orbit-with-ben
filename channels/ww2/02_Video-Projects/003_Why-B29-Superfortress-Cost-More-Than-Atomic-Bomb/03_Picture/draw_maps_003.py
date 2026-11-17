#!/usr/bin/env python3
"""Deterministic £0 code-drawn operational maps & engineering graphics builder for WW2:003 (J2998).

Renders all 12 graphics + 5 shot-specific sub-variants (17 total plates, 1920x1080 PNG + 6.0s 24fps MP4)
specified in `01_Script/SHOT_LIST.md` (`G1`-`G12`) onto `/Volumes/data/studio-live/ww2/.../03_Picture/maps/`.
Uses Natural Earth 1:50m public-domain (`CC0`) coastline, international boundary, and US state vectors
for authentic War Office / USAAF operational cartography in the Field Order History house palette.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import subprocess
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FPS = 24
DURATION_S = 6.0

DEFAULT_OUT_DIR = pathlib.Path(
    "/Volumes/data/studio-live/ww2/02_Video-Projects/"
    "003_Why-B29-Superfortress-Cost-More-Than-Atomic-Bomb/03_Picture/maps"
)
GEO_DIR = pathlib.Path("/Volumes/data/studio-live/ww2/00_Brand/geo")

# Field Order History documentary palette (lifted slate navy, warm slate land, signal yellow & tactical red)
BG_OCEAN = (24, 34, 46)
BG_PANEL = (30, 41, 56)
BG_CARD = (38, 51, 68)
LAND_FILL = (56, 68, 82)
LAND_HI = (72, 86, 102)
COAST_LINE = (132, 148, 166)
BORDER_LINE = (94, 110, 128)
GRID_LINE = (44, 58, 76)
WHITE = (248, 250, 252)
MUTED = (182, 194, 208)
SIGNAL_YELLOW = (255, 214, 0)     # #FFD600
TACTICAL_RED = (255, 69, 58)      # #FF453A
STEEL_CYAN = (100, 210, 255)
AMBER_ORANGE = (255, 159, 10)
SAFE_GREEN = (50, 215, 75)
DARK_KEY = (12, 16, 22)

FONT_COND = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf"
FONT_MONO = "/System/Library/Fonts/Menlo.ttc"

_FONT_CACHE: Dict[Tuple[str, int], ImageFont.FreeTypeFont] = {}
_GEO_CACHE: Dict[str, List] = {}
_BASEMAP_CACHE: Dict[Tuple, Image.Image] = {}


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    key = (path, size)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = ImageFont.truetype(path, size)
    return _FONT_CACHE[key]


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_geojson_coords(filename: str) -> List[Tuple[str, List]]:
    if filename in _GEO_CACHE:
        return _GEO_CACHE[filename]
    p = GEO_DIR / filename
    data = json.loads(p.read_text(encoding="utf-8"))
    geoms: List[Tuple[str, List]] = []
    for feat in data.get("features", []):
        g = feat.get("geometry") or {}
        gtype = g.get("type", "")
        coords = g.get("coordinates", [])
        if gtype == "Polygon":
            geoms.append(("poly", coords))
        elif gtype == "MultiPolygon":
            for poly in coords:
                geoms.append(("poly", poly))
        elif gtype == "LineString":
            geoms.append(("line", coords))
        elif gtype == "MultiLineString":
            for line in coords:
                geoms.append(("line", line))
    _GEO_CACHE[filename] = geoms
    return geoms


def make_projector(lon_min: float, lon_max: float, lat_min: float, lat_max: float, box: Tuple[int, int, int, int]):
    """Equirectangular-cosine-corrected projector supporting dateline wrap (lon in [0, 360] if lon_max > 180)."""
    x0, y0, x1, y1 = box
    bw = x1 - x0
    bh = y1 - y0
    wrap360 = lon_max > 180.0

    def proj(lon: float, lat: float) -> Tuple[float, float]:
        if wrap360 and lon < 0:
            lon += 360.0
        px = x0 + (lon - lon_min) / (lon_max - lon_min) * bw
        py = y1 - (lat - lat_min) / (lat_max - lat_min) * bh
        return (px, py)

    return proj


def render_geo_basemap(
    lon_min: float,
    lon_max: float,
    lat_min: float,
    lat_max: float,
    box: Tuple[int, int, int, int] = (70, 150, 1850, 995),
    show_states: bool = False,
    grid_step_lon: int = 15,
    grid_step_lat: int = 10,
) -> Image.Image:
    key = (lon_min, lon_max, lat_min, lat_max, box, show_states, grid_step_lon, grid_step_lat)
    if key in _BASEMAP_CACHE:
        return _BASEMAP_CACHE[key].copy()

    base = Image.new("RGB", (W, H), BG_PANEL)
    draw = ImageDraw.Draw(base)
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=BG_OCEAN)

    proj = make_projector(lon_min, lon_max, lat_min, lat_max, box)
    wrap360 = lon_max > 180.0

    # Graticule lines
    g_lon_start = int(math.ceil(lon_min / grid_step_lon) * grid_step_lon)
    for glon in range(g_lon_start, int(lon_max) + 1, grid_step_lon):
        gx, _ = proj(glon, (lat_min + lat_max) / 2)
        if x0 < gx < x1:
            draw.line([(gx, y0), (gx, y1)], fill=GRID_LINE, width=1)
            disp_lon = glon - 360 if glon > 180 else glon
            ew = "E" if disp_lon >= 0 else "W"
            lbl = f"{abs(disp_lon)}°{ew}"
            draw.text((gx + 5, y1 - 24), lbl, font=font(FONT_MONO, 15), fill=(95, 112, 132))

    g_lat_start = int(math.ceil(lat_min / grid_step_lat) * grid_step_lat)
    for glat in range(g_lat_start, int(lat_max) + 1, grid_step_lat):
        _, gy = proj((lon_min + lon_max) / 2, glat)
        if y0 < gy < y1:
            draw.line([(x0, gy), (x1, gy)], fill=GRID_LINE, width=1)
            ns = "N" if glat >= 0 else "S"
            draw.text((x0 + 8, gy - 20), f"{abs(glat)}°{ns}", font=font(FONT_MONO, 15), fill=(95, 112, 132))

    # Clip map layer to box
    map_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    mdraw = ImageDraw.Draw(map_layer)

    for _, rings in load_geojson_coords("ne_50m_land.geojson"):
        if not rings:
            continue
        ext = rings[0]
        lons = [(pt[0] + 360.0 if (wrap360 and pt[0] < 0) else pt[0]) for pt in ext]
        lats = [pt[1] for pt in ext]
        if max(lons) < lon_min - 5 or min(lons) > lon_max + 5:
            continue
        if max(lats) < lat_min - 5 or min(lats) > lat_max + 5:
            continue
        # Skip dateline-spanning wrap artifacts
        if max(lons) - min(lons) > 170.0:
            continue
        pts = [proj(pt[0], pt[1]) for pt in ext]
        if len(pts) >= 3:
            mdraw.polygon(pts, fill=LAND_FILL + (255,), outline=COAST_LINE + (255,))

    border_files = ["ne_50m_admin_0_boundary_lines_land.geojson"]
    if show_states:
        border_files.append("ne_50m_admin_1_states_provinces_lines.geojson")
    for bf in border_files:
        col = BORDER_LINE + (220,) if "admin_0" in bf else (80, 96, 114, 180)
        for _, line in load_geojson_coords(bf):
            if len(line) < 2:
                continue
            lons = [(pt[0] + 360.0 if (wrap360 and pt[0] < 0) else pt[0]) for pt in line]
            lats = [pt[1] for pt in line]
            if max(lons) < lon_min - 2 or min(lons) > lon_max + 2 or max(lats) < lat_min - 2 or min(lats) > lat_max + 2:
                continue
            if max(lons) - min(lons) > 120.0:
                continue
            pts = [proj(pt[0], pt[1]) for pt in line]
            mdraw.line(pts, fill=col, width=1)

    # Mask strictly inside box
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rectangle(box, fill=255)
    base.paste(map_layer.convert("RGB"), (0, 0), Image.composite(map_layer.split()[3], Image.new("L", (W, H), 0), mask))

    draw = ImageDraw.Draw(base)
    draw.rectangle(box, outline=(120, 138, 158), width=2)
    _BASEMAP_CACHE[key] = base
    return base.copy()


def draw_header(draw: ImageDraw.ImageDraw, tag: str, title: str, subtitle: str) -> None:
    draw.rectangle((0, 0, W, 128), fill=(20, 28, 38))
    draw.line([(0, 128), (W, 128)], fill=(82, 98, 118), width=2)
    # Left tactical accent bar
    draw.rectangle((70, 24, 78, 106), fill=SIGNAL_YELLOW)
    draw.text((96, 22), tag.upper(), font=font(FONT_MONO, 20), fill=SIGNAL_YELLOW)
    draw.text((96, 48), title, font=font(FONT_COND, 50), fill=WHITE)
    if subtitle:
        tw = draw.textlength(subtitle, font=font(FONT_MONO, 19))
        draw.text((W - 70 - tw, 84), subtitle, font=font(FONT_MONO, 19), fill=MUTED)


def draw_footer(draw: ImageDraw.ImageDraw, source_text: str) -> None:
    draw.text((70, 1028), source_text, font=font(FONT_MONO, 17), fill=(150, 165, 182))


def draw_badge(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[float, float],
    text: str,
    fg: Tuple[int, int, int] = WHITE,
    bg: Tuple[int, int, int] = (20, 28, 38),
    border: Tuple[int, int, int] = SIGNAL_YELLOW,
    size: int = 24,
    align: str = "center",
) -> None:
    f = font(FONT_BOLD, size)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 14, 8
    bx0 = xy[0] - (tw / 2 + pad_x) if align == "center" else (xy[0] if align == "left" else xy[0] - tw - 2 * pad_x)
    by0 = xy[1] - (th / 2 + pad_y)
    bx1 = bx0 + tw + 2 * pad_x
    by1 = by0 + th + 2 * pad_y
    draw.rounded_rectangle((bx0, by0, bx1, by1), radius=6, fill=bg, outline=border, width=2)
    draw.text((bx0 + pad_x, by0 + pad_y - bbox[1]), text, font=f, fill=fg)


def draw_arrow_curve(
    draw: ImageDraw.ImageDraw,
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    ctrl: Tuple[float, float],
    color: Tuple[int, int, int],
    progress: float = 1.0,
    width: int = 5,
    dashed: bool = False,
) -> Tuple[float, float]:
    steps = 80
    n = max(2, int(round(steps * max(0.02, min(1.0, progress)))))
    pts = []
    for i in range(n + 1):
        t = (i / steps)
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * ctrl[0] + t ** 2 * p1[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * ctrl[1] + t ** 2 * p1[1]
        pts.append((x, y))
    if dashed:
        for i in range(0, len(pts) - 1, 4):
            seg = pts[i:i + 3]
            if len(seg) >= 2:
                draw.line(seg, fill=color, width=width)
    else:
        draw.line(pts, fill=color, width=width)
    # Arrowhead at end
    ex, ey = pts[-1]
    px, py = pts[-2]
    ang = math.atan2(ey - py, ex - px)
    ah = 16
    a1 = (ex - ah * math.cos(ang - 0.45), ey - ah * math.sin(ang - 0.45))
    a2 = (ex - ah * math.cos(ang + 0.45), ey - ah * math.sin(ang + 0.45))
    draw.polygon([(ex, ey), a1, a2], fill=color)
    return (ex, ey)


def draw_city_dot(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[float, float],
    label: str,
    color: Tuple[int, int, int] = SIGNAL_YELLOW,
    dx: int = 12,
    dy: int = -12,
    size: int = 23,
) -> None:
    x, y = xy
    draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=DARK_KEY, outline=color, width=3)
    draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=color)
    if label:
        f = font(FONT_BOLD, size)
        draw.text((x + dx + 2, y + dy + 2), label, font=f, fill=DARK_KEY)
        draw.text((x + dx, y + dy), label, font=f, fill=WHITE)


def ease_out(t: float, a: float, b: float) -> float:
    if t <= a:
        return 0.0
    if t >= b:
        return 1.0
    u = (t - a) / (b - a)
    return 1.0 - (1.0 - u) ** 3


# ==============================================================================
# Individual Graphics G1 - G12 (+ shot-specific variants)
# ==============================================================================

def render_g01_cost(p: float, breakdown: bool = False) -> Image.Image:
    img = Image.new("RGB", (W, H), BG_PANEL)
    draw = ImageDraw.Draw(img)
    for gx in range(70, 1851, 120):
        draw.line([(gx, 150), (gx, 980)], fill=GRID_LINE, width=1)
    for gy in range(190, 981, 100):
        draw.line([(70, gy), (1850, gy)], fill=GRID_LINE, width=1)

    if not breakdown:
        draw_header(
            draw,
            "US WAR EXPENDITURE COMPARISON  |  1940-1945",
            "AMERICA'S MOST EXPENSIVE WW2 WEAPON PROGRAMME",
            "THEN-YEAR US DOLLARS (1940-1945)",
        )
        p1 = ease_out(p, 0.05, 0.45)
        p2 = ease_out(p, 0.35, 0.80)
        max_w = 1180
        # Bar 1: Manhattan Project $1.9B
        y1 = 300
        w1 = int(max_w * (1.89 / 3.0) * p1)
        draw.text((110, y1 - 52), "MANHATTAN PROJECT  (ATOMIC BOMB)", font=font(FONT_COND, 42), fill=MUTED)
        draw.rounded_rectangle((110, y1, 110 + max(12, w1), y1 + 115), radius=8, fill=(88, 112, 138), outline=COAST_LINE, width=2)
        if p1 > 0.2:
            val1 = 1.9 * p1
            draw.text((130 + w1, y1 + 22), f"${val1:.1f} BILLION", font=font(FONT_COND, 68), fill=WHITE)
            draw.text((130 + w1, y1 + 88), "$1.89B exact through Dec 1945", font=font(FONT_MONO, 20), fill=MUTED)

        # Bar 2: B-29 Programme $3.0B
        y2 = 585
        w2 = int(max_w * 1.0 * p2)
        draw.text((110, y2 - 52), "BOEING B-29 SUPERFORTRESS PROGRAMME", font=font(FONT_COND, 44), fill=SIGNAL_YELLOW)
        draw.rounded_rectangle((110, y2, 110 + max(12, w2), y2 + 130), radius=8, fill=SIGNAL_YELLOW, outline=WHITE, width=3)
        if p2 > 0.15:
            val2 = 3.0 * p2
            draw.text((130 + w2, y2 + 24), f"${val2:.1f} BILLION", font=font(FONT_COND, 78), fill=SIGNAL_YELLOW)
            draw.text((130 + w2, y2 + 98), "+58% MORE THAN THE ATOMIC BOMB", font=font(FONT_BOLD, 24), fill=TACTICAL_RED)

        if p > 0.72:
            draw.rounded_rectangle((110, 800, 1810, 945), radius=10, fill=BG_CARD, outline=(95, 115, 138), width=2)
            draw.text(
                (145, 825),
                "4 GIANT ASSEMBLY PLANTS   ·   3,970 BOMBERS BUILT   ·   1,664 ORDERED BEFORE FIRST FLIGHT",
                font=font(FONT_COND, 38),
                fill=WHITE,
            )
            draw.text(
                (145, 882),
                "Includes airframe R&D, Wright R-3350 engine tooling, modification centres & Twentieth Air Force basing",
                font=font(FONT_MONO, 21),
                fill=MUTED,
            )
    else:
        draw_header(
            draw,
            "INDUSTRIAL & R&D GAMBLE  |  PARALLEL PRODUCTION",
            "WHAT EACH GAMBLE BOUGHT  ($1.9B vs $3.0B)",
            "BUILT BEFORE PROVEN IN TEST",
        )
        # Left card: Manhattan Project
        p1 = ease_out(p, 0.05, 0.45)
        p2 = ease_out(p, 0.30, 0.75)
        if p1 > 0:
            draw.rounded_rectangle((90, 180, 920, 955), radius=12, fill=BG_CARD, outline=COAST_LINE, width=2)
            draw.rectangle((90, 180, 920, 275), fill=(48, 64, 84))
            draw.text((125, 200), "MANHATTAN PROJECT  —  $1.9 BILLION", font=font(FONT_COND, 46), fill=WHITE)
            items_l = [
                ("OAK RIDGE & HANFORD", "Uranium enrichment & plutonium production reactors"),
                ("LOS ALAMOS LAB", "Physics, metallurgy, implosion & weapon design"),
                ("130,000 WORKERS", "Built industrial plants before fission bomb was tested"),
                ("COMBAT OUTPUT (1945)", "Trinity test device + 2 combat atomic bombs"),
            ]
            for idx, (h_txt, s_txt) in enumerate(items_l):
                if p1 > idx * 0.2:
                    yy = 320 + idx * 145
                    draw.rectangle((125, yy + 6, 135, yy + 72), fill=STEEL_CYAN)
                    draw.text((155, yy), h_txt, font=font(FONT_COND, 36), fill=STEEL_CYAN)
                    draw.text((155, yy + 44), s_txt, font=font(FONT_BOLD, 22), fill=MUTED)

        if p2 > 0:
            draw.rounded_rectangle((1000, 180, 1830, 955), radius=12, fill=BG_CARD, outline=SIGNAL_YELLOW, width=3)
            draw.rectangle((1000, 180, 1830, 275), fill=(62, 58, 34))
            draw.text((1035, 200), "BOEING B-29 PROGRAMME  —  $3.0 BILLION", font=font(FONT_COND, 46), fill=SIGNAL_YELLOW)
            items_r = [
                ("4 ASSEMBLY PLANTS", "Wichita, Renton, Marietta & Omaha + subcontractors"),
                ("3,970 SUPERFORTRESSES", "Pressurised cabins, GE fire-control computers, 40,000+ parts"),
                ("R-3350 & MOD CENTRES", "Twin-turbo 2,200-hp engines & Kansas retrofit blitz"),
                ("CREWS & BASES", "Tens of thousands of trained aircrew + Marianas mega-fields"),
            ]
            for idx, (h_txt, s_txt) in enumerate(items_r):
                if p2 > idx * 0.2:
                    yy = 320 + idx * 145
                    draw.rectangle((1035, yy + 6, 1045, yy + 72), fill=SIGNAL_YELLOW)
                    draw.text((1065, yy), h_txt, font=font(FONT_COND, 36), fill=SIGNAL_YELLOW)
                    draw.text((1065, yy + 44), s_txt, font=font(FONT_BOLD, 22), fill=WHITE)

    draw_footer(draw, "SOURCES: Craven & Cate (USAF Official History, Vol. VI); NMUSAF; Schwartz, Atomic Audit ($1.89B Manhattan Project)")
    return img


def render_g02_range_map(p: float) -> Image.Image:
    box = (70, 150, 1850, 995)
    lon_min, lon_max, lat_min, lat_max = 115.0, 275.0, 5.0, 62.0
    img = render_geo_basemap(lon_min, lon_max, lat_min, lat_max, box=box, grid_step_lon=20, grid_step_lat=15)
    draw = ImageDraw.Draw(img)
    proj = make_projector(lon_min, lon_max, lat_min, lat_max, box)

    draw_header(
        draw,
        "JAN 1940 SPECIFICATION R-40B  |  PACIFIC DISTANCES",
        "WHY COASTAL BOMBERS COULD NOT FIGHT A PACIFIC WAR",
        "HAP ARNOLD'S 5,333-MILE REQUIREMENT",
    )

    seattle = proj(-122.3, 47.6)
    hawaii = proj(-157.9, 21.3)
    saipan = proj(145.7, 15.2)
    tokyo = proj(139.7, 35.7)

    # B-17 coastal combat radius (~800 mi) around Seattle & Hawaii
    p_b17 = ease_out(p, 0.05, 0.35)
    if p_b17 > 0:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        for center in (seattle, hawaii):
            rx = int(135 * p_b17)
            ry = int(125 * p_b17)
            od.ellipse((center[0] - rx, center[1] - ry, center[0] + rx, center[1] + ry), fill=(100, 210, 255, 42), outline=STEEL_CYAN + (220,), width=3)
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(img)
        draw_badge(draw, (seattle[0] - 115, seattle[1] + 145), "B-17 RADIUS ~800 MI", fg=STEEL_CYAN, border=STEEL_CYAN, size=22)

    # Pacific distances & R-40B 5,333-mile range arc
    p_vlr = ease_out(p, 0.35, 0.85)
    if p_vlr > 0:
        draw_arrow_curve(draw, hawaii, tokyo, ((hawaii[0] + tokyo[0]) / 2, 260), TACTICAL_RED, progress=p_vlr, width=5, dashed=True)
        draw_arrow_curve(draw, saipan, tokyo, (saipan[0] - 50, (saipan[1] + tokyo[1]) / 2), SIGNAL_YELLOW, progress=p_vlr, width=6)
        if p_vlr > 0.55:
            draw_badge(draw, (930, 315), "PEARL HARBOR -> TOKYO: 3,850 MI ONE WAY", fg=WHITE, border=TACTICAL_RED, size=24)
            draw_badge(draw, (535, 625), "MARIANAS -> TOKYO: 1,500 MI (3,000+ MI ROUND TRIP)", fg=SIGNAL_YELLOW, border=SIGNAL_YELLOW, size=23)

    draw_city_dot(draw, seattle, "SEATTLE / US WEST COAST", STEEL_CYAN, dx=-255, dy=-34)
    draw_city_dot(draw, hawaii, "PEARL HARBOR", STEEL_CYAN, dx=-165, dy=-32)
    draw_city_dot(draw, saipan, "MARIANAS", SIGNAL_YELLOW, dx=14, dy=8)
    draw_city_dot(draw, tokyo, "TOKYO", TACTICAL_RED, dx=14, dy=-26)

    if p > 0.65:
        draw.rounded_rectangle((1175, 760, 1820, 968), radius=10, fill=(20, 28, 38), outline=SIGNAL_YELLOW, width=3)
        draw.text((1205, 780), "SPECIFICATION R-40B  (29 JAN 1940)", font=font(FONT_COND, 36), fill=SIGNAL_YELLOW)
        draw.text((1205, 830), "• RANGE:  5,333 MILES  (>5,000 MI)", font=font(FONT_BOLD, 25), fill=WHITE)
        draw.text((1205, 872), "• PAYLOAD:  2,000 LB  (1 TON OF BOMBS)", font=font(FONT_BOLD, 25), fill=WHITE)
        draw.text((1205, 914), "• SPEED:  400 MPH  AT  30,000+ FT", font=font(FONT_BOLD, 25), fill=MUTED)

    draw_footer(draw, "SOURCES: Knaack (USAF Bomber Encyclopedia, p. 480); Craven & Cate Vol. VI (R-40B Very Long Range Specification, Jan 1940)")
    return img


def render_g03_pressurised_tunnel(p: float) -> Image.Image:
    img = Image.new("RGB", (W, H), BG_PANEL)
    draw = ImageDraw.Draw(img)
    for gx in range(70, 1851, 90):
        draw.line([(gx, 150), (gx, 980)], fill=GRID_LINE, width=1)
    for gy in range(180, 981, 90):
        draw.line([(70, gy), (1850, gy)], fill=GRID_LINE, width=1)

    draw_header(
        draw,
        "BOEING MODEL 345 ENGINEERING CUTAWAY  |  30,000 FT (-44°C)",
        "HOW BOEING BRIDGED TWO UNPRESSURISED BOMB BAYS",
        "FIRST PRESSURISED HEAVY BOMBER IN COMBAT SERVICE",
    )

    # Outer B-29 side fuselage silhouette (nose left -> tail right)
    # Nose x=150..520, Bomb bays x=520..1080, Waist cabin x=1080..1430, Tail cone & fin x=1430..1760
    fy_top, fy_bot = 455, 635
    fuselage_pts = [
        (145, 555), (165, 505), (235, 465), (360, 455),
        (1340, 455), (1660, 495), (1765, 515), (1765, 555),
        (1580, 595), (1320, 635), (340, 635), (195, 610), (150, 580),
    ]
    # Vertical tail fin
    fin_pts = [(1510, 480), (1645, 255), (1715, 255), (1748, 512)]
    draw.polygon(fin_pts, fill=(64, 78, 96), outline=WHITE, width=3)
    draw.polygon(fuselage_pts, fill=(52, 66, 82), outline=WHITE, width=3)

    p_cab = ease_out(p, 0.08, 0.45)
    p_tun = ease_out(p, 0.38, 0.78)

    if p_cab > 0:
        # Forward pressurised nose cabin
        draw.rounded_rectangle((175, 472, 520, 618), radius=24, fill=(38, 92, 128), outline=STEEL_CYAN, width=3)
        # Aft pressurised waist cabin
        draw.rounded_rectangle((1085, 472, 1410, 618), radius=12, fill=(38, 92, 128), outline=STEEL_CYAN, width=3)
        # Isolated tail gunner cabin
        draw.rounded_rectangle((1635, 504, 1752, 558), radius=10, fill=(38, 92, 128), outline=STEEL_CYAN, width=3)

        # Twin unpressurised bomb bays
        draw.rectangle((535, 518, 795, 630), fill=(48, 34, 38), outline=TACTICAL_RED, width=2)
        draw.rectangle((810, 518, 1070, 630), fill=(48, 34, 38), outline=TACTICAL_RED, width=2)
        for bx_mid, b_title in ((665, "FWD BOMB BAY"), (940, "AFT BOMB BAY")):
            tw1 = draw.textlength(b_title, font=font(FONT_COND, 26))
            tw2 = draw.textlength("(UNPRESSURISED)", font=font(FONT_COND, 21))
            draw.text((bx_mid - tw1 / 2, 544), b_title, font=font(FONT_COND, 26), fill=TACTICAL_RED)
            draw.text((bx_mid - tw2 / 2, 576), "(UNPRESSURISED)", font=font(FONT_COND, 21), fill=MUTED)

    # 28-inch padded crawl tunnel bridging over the two bomb bays
    if p_tun > 0:
        tx1 = int(515 + (1090 - 515) * p_tun)
        draw.rectangle((515, 470, tx1, 508), fill=SIGNAL_YELLOW, outline=WHITE, width=3)
        if p_tun > 0.6:
            draw.line([(802, 470), (802, 330)], fill=SIGNAL_YELLOW, width=3)
            draw_badge(
                draw,
                (802, 295),
                "28-INCH PADDED CRAWL TUNNEL  (35 FT LONG OVER BOMB BAYS)",
                fg=DARK_KEY,
                bg=SIGNAL_YELLOW,
                border=WHITE,
                size=25,
            )

    # Labels below
    if p > 0.50:
        cards = [
            (155, 710, 535, "PRESSURISED NOSE CABIN", "Pilots, bombardier, engineer, navigator, radio  |  8,000-ft cabin altitude", STEEL_CYAN),
            (575, 710, 1045, "TWIN OPEN BOMB BAYS", "Doors swing open at 30,000 ft (-44°C outside) — cannot hold cabin pressure", TACTICAL_RED),
            (1085, 710, 1465, "PRESSURISED WAIST CABIN", "3 blister gunners sighting remote turrets in warm flying clothes", STEEL_CYAN),
            (1495, 710, 1815, "ISOLATED TAIL", "Sealed tail compartment; entered only unpressurised", MUTED),
        ]
        for x0, y0, x1, h_t, b_t, col in cards:
            draw.rounded_rectangle((x0, y0, x1, 860), radius=8, fill=BG_CARD, outline=col, width=2)
            draw.text((x0 + 18, y0 + 16), h_t, font=font(FONT_COND, 30), fill=col)
            # Wrap body text cleanly
            words = b_t.split()
            lines, cur = [], ""
            for w in words:
                test = (cur + " " + w).strip()
                if draw.textlength(test, font=font(FONT_BOLD, 19)) <= (x1 - x0 - 32):
                    cur = test
                else:
                    lines.append(cur)
                    cur = w
            if cur:
                lines.append(cur)
            for li, ln in enumerate(lines[:3]):
                draw.text((x0 + 18, y0 + 58 + li * 26), ln, font=font(FONT_BOLD, 19), fill=WHITE)

    draw_footer(draw, "SOURCES: NMUSAF Official B-29 Fact Sheet; Knaack (1988, p. 480 — 8,000-ft cabin pressure & 28-inch crawl tunnel)")
    return img


def render_g04_fire_control(p: float) -> Image.Image:
    img = Image.new("RGB", (W, H), BG_PANEL)
    draw = ImageDraw.Draw(img)
    for gx in range(70, 1851, 100):
        draw.line([(gx, 150), (gx, 980)], fill=GRID_LINE, width=1)
    for gy in range(180, 981, 100):
        draw.line([(70, gy), (1850, gy)], fill=GRID_LINE, width=1)

    draw_header(
        draw,
        "GENERAL ELECTRIC CENTRAL STATION FIRE CONTROL",
        "ANALOGUE COMPUTER REMOTE GUN TURRETS",
        "4 REMOTE TWIN-.50 TURRETS + TAIL MOUNT",
    )

    # B-29 fuselage side diagram at bottom-left/center
    draw.rounded_rectangle((130, 560, 1220, 680), radius=45, fill=(56, 70, 88), outline=WHITE, width=3)
    draw.polygon([(1080, 570), (1185, 410), (1230, 410), (1220, 585)], fill=(56, 70, 88), outline=WHITE, width=3)

    # 3 plexiglass sighting blisters
    blisters = [(850, 555, "TOP BLISTER"), (780, 680, "SIDE BLISTERS"), (210, 575, "NOSE SIGHT")]
    for bx, by, lbl in blisters:
        draw.ellipse((bx - 28, by - 18, bx + 28, by + 18), fill=(70, 165, 220), outline=WHITE, width=2)

    # 4 remote twin-.50 turrets
    turrets = [
        (360, 552, "FWD UPPER TURRET"),
        (960, 552, "AFT UPPER TURRET"),
        (410, 685, "FWD LOWER TURRET"),
        (930, 685, "AFT LOWER TURRET"),
    ]
    for tx, ty, tlbl in turrets:
        draw.rectangle((tx - 24, ty - 14, tx + 24, ty + 14), fill=SIGNAL_YELLOW, outline=DARK_KEY, width=2)
        # Gun barrels
        gy_dir = -14 if ty < 600 else 14
        draw.line([(tx + 18, ty + gy_dir // 2), (tx + 68, ty + gy_dir)], fill=SIGNAL_YELLOW, width=4)

    # GE Central Computer box in center-top
    comp_box = (520, 210, 980, 395)
    draw.rounded_rectangle(comp_box, radius=10, fill=BG_CARD, outline=SIGNAL_YELLOW, width=3)
    draw.text((550, 228), "GE ANALOGUE COMPUTER", font=font(FONT_COND, 40), fill=SIGNAL_YELLOW)
    draw.text((550, 276), "1. Target Lead & Speed", font=font(FONT_BOLD, 22), fill=WHITE)
    draw.text((550, 306), "2. Bullet Gravity Drop & Air Density (30,000 ft)", font=font(FONT_BOLD, 22), fill=WHITE)
    draw.text((550, 336), "3. Parallax Offset (Blister -> Remote Turret)", font=font(FONT_BOLD, 22), fill=WHITE)

    # Enemy target top-right
    target = (1590, 295)
    p1 = ease_out(p, 0.1, 0.5)
    p2 = ease_out(p, 0.4, 0.85)
    if p1 > 0:
        # Sight line from blister to target
        draw_arrow_curve(draw, (850, 545), target, (1180, 390), STEEL_CYAN, progress=p1, width=4, dashed=True)
        draw_arrow_curve(draw, (850, 540), (750, 395), (810, 465), STEEL_CYAN, progress=p1, width=3)
        draw.ellipse((target[0] - 22, target[1] - 22, target[0] + 22, target[1] + 22), outline=TACTICAL_RED, width=3)
        draw.line([(target[0] - 32, target[1]), (target[0] + 32, target[1])], fill=TACTICAL_RED, width=2)
        draw.line([(target[0], target[1] - 32), (target[0], target[1] + 32)], fill=TACTICAL_RED, width=2)
        draw.text((1465, 225), "TRACKED FIGHTER TARGET", font=font(FONT_COND, 32), fill=TACTICAL_RED)

    if p2 > 0:
        # Computer servo commands to forward & aft upper turrets + deflected lead shot
        draw_arrow_curve(draw, (640, 395), (360, 540), (470, 455), SIGNAL_YELLOW, progress=p2, width=4)
        draw_arrow_curve(draw, (860, 395), (960, 540), (925, 465), SIGNAL_YELLOW, progress=p2, width=4)
        lead_pt = (1695, 265)
        draw_arrow_curve(draw, (395, 542), lead_pt, (1040, 365), TACTICAL_RED, progress=p2, width=4)
        draw_arrow_curve(draw, (995, 542), lead_pt, (1340, 395), TACTICAL_RED, progress=p2, width=4)
        if p2 > 0.6:
            draw_badge(draw, (1590, 435), "COMPUTED LEAD & PARALLAX INTERCEPT", fg=SIGNAL_YELLOW, border=TACTICAL_RED, size=22)

    if p > 0.65:
        draw.rounded_rectangle((1280, 560, 1830, 890), radius=10, fill=BG_CARD, outline=STEEL_CYAN, width=2)
        draw.text((1310, 585), "TURRET HAND-OVER", font=font(FONT_COND, 38), fill=STEEL_CYAN)
        draw.text((1310, 638), "• Gunners sit sealed inside warm", font=font(FONT_BOLD, 23), fill=WHITE)
        draw.text((1310, 670), "  pressurised cabins under blisters", font=font(FONT_BOLD, 23), fill=WHITE)
        draw.text((1310, 715), "• Single gunner can command multiple", font=font(FONT_BOLD, 23), fill=WHITE)
        draw.text((1310, 747), "  turrets & pass targets nose-to-tail", font=font(FONT_BOLD, 23), fill=WHITE)
        draw.text((1310, 795), "• First combat bomber fitted with", font=font(FONT_BOLD, 23), fill=SIGNAL_YELLOW)
        draw.text((1310, 827), "  centralised analogue fire control", font=font(FONT_BOLD, 23), fill=SIGNAL_YELLOW)

    draw_footer(draw, "SOURCES: NMUSAF Boeing B-29 Fact Sheet; Knaack (1988, pp. 480-482 — General Electric Central Fire Control System)")
    return img


def render_g05_procurement_timeline(p: float) -> Image.Image:
    img = Image.new("RGB", (W, H), BG_PANEL)
    draw = ImageDraw.Draw(img)
    for gy in range(220, 860, 120):
        draw.line([(130, gy), (1810, gy)], fill=GRID_LINE, width=1)

    draw_header(
        draw,
        "OFF-THE-DRAWING-BOARD GAMBLE  |  1940-1942",
        "1,664 BOMBERS ORDERED BEFORE ONE HAD FLOWN",
        "CUMULATIVE USAAF B-29 ORDERS",
    )

    milestones = [
        ("24 AUG 1940", 2, "2 XB-29 PROTOTYPES", "Contracted from paper Model 345", STEEL_CYAN, 260),
        ("MAY 1941", 250, "250 B-29s ORDERED", "16 months before first flight", AMBER_ORANGE, 740),
        ("DEC 1941 - SUMMER 1942", 1000, "PEARL HARBOR SURGE", "4-plant manufacturing pool formed", AMBER_ORANGE, 1220),
        ("21 SEP 1942", 1664, "1,664 ON ORDER!", "Day Eddie Allen flew first XB-29", SIGNAL_YELLOW, 1650),
    ]

    base_y = 820
    max_h = 520
    draw.line([(130, base_y), (1830, base_y)], fill=WHITE, width=3)

    for idx, (dt, count, h_lbl, sub_lbl, col, cx) in enumerate(milestones):
        prog = ease_out(p, idx * 0.18, idx * 0.18 + 0.35)
        if prog <= 0:
            continue
        bh = max(18, int((count / 1664.0) * max_h * prog))
        bw = 175
        draw.rounded_rectangle((cx - bw // 2, base_y - bh, cx + bw // 2, base_y), radius=6, fill=col, outline=WHITE, width=2)
        disp_n = int(round(count * prog))
        n_txt = f"{disp_n:,}"
        tw = draw.textlength(n_txt, font=font(FONT_COND, 56))
        draw.text((cx - tw / 2, base_y - bh - 66), n_txt, font=font(FONT_COND, 56), fill=col)

        # Date & note below axis
        dtw = draw.textlength(dt, font=font(FONT_COND, 32))
        draw.text((cx - dtw / 2, base_y + 18), dt, font=font(FONT_COND, 32), fill=WHITE)
        stw = draw.textlength(sub_lbl, font=font(FONT_BOLD, 20))
        draw.text((cx - stw / 2, base_y + 58), sub_lbl, font=font(FONT_BOLD, 20), fill=MUTED)

    if p > 0.72:
        draw_badge(
            draw,
            (620, 245),
            "NORMAL PROCUREMENT: TEST PROTOTYPE 1-2 YEARS FIRST   |   B-29: FACTORIES & BOMBERS BUILT AT ONCE",
            fg=SIGNAL_YELLOW,
            border=SIGNAL_YELLOW,
            size=23,
        )

    draw_footer(draw, "SOURCES: Knaack (1988, p. 481); Craven & Cate Vol. VI, pp. 241-246 (250 ordered May 1941; 1,664 ordered by 21 Sep 1942)")
    return img


def render_g06_plants_map(p: float, seattle_crash: bool = False) -> Image.Image:
    if seattle_crash:
        # Clean, sober tactical map of 18 Feb 1943 Seattle XB-29 (41-3) test flight path (zero graphic imagery)
        img = Image.new("RGB", (W, H), BG_OCEAN)
        draw = ImageDraw.Draw(img)
        # Stylized Puget Sound / Elliott Bay / Duwamish River / Lake Washington schematic cartography
        # Landmasses around Seattle
        draw.polygon([(420, 130), (1380, 130), (1380, 1000), (540, 1000), (520, 740), (610, 510), (490, 350)], fill=LAND_FILL, outline=COAST_LINE, width=2)
        # West Seattle peninsula
        draw.polygon([(220, 520), (490, 520), (515, 1000), (220, 1000)], fill=LAND_FILL, outline=COAST_LINE, width=2)
        # Lake Washington on right
        draw.polygon([(1120, 150), (1360, 150), (1340, 960), (1140, 960)], fill=BG_OCEAN, outline=COAST_LINE, width=2)
        # Duwamish Waterway channel
        draw.line([(535, 515), (615, 680), (685, 860), (720, 990)], fill=BG_OCEAN, width=22)
        for gx in range(100, 1821, 120):
            draw.line([(gx, 140), (gx, 995)], fill=GRID_LINE, width=1)
        for gy in range(180, 996, 120):
            draw.line([(80, gy), (1840, gy)], fill=GRID_LINE, width=1)

        draw_header(
            draw,
            "SEATTLE TEST FLIGHT ACCIDENT  |  18 FEBRUARY 1943",
            "SECOND PROTOTYPE XB-29 (41-3) ENGINE FIRE & RETURN TRACK",
            "CHIEF TEST PILOT EDMUND 'EDDIE' ALLEN",
        )

        boeing_field = (735, 790)
        turn_pt = (785, 255)
        frye_plant = (645, 525)

        # Runway bar at Boeing Field
        draw.line([(710, 745), (760, 835)], fill=WHITE, width=10)
        draw_city_dot(draw, boeing_field, "BOEING FIELD (TAKEOFF)", SIGNAL_YELLOW, dx=20, dy=-12, size=26)
        draw.text((255, 360), "ELLIOTT BAY", font=font(FONT_MONO, 22), fill=COAST_LINE)
        draw.text((1160, 440), "LAKE\nWASHINGTON", font=font(FONT_MONO, 22), fill=COAST_LINE)

        p1 = ease_out(p, 0.05, 0.45)
        p2 = ease_out(p, 0.42, 0.85)
        if p1 > 0:
            draw_arrow_curve(draw, boeing_field, turn_pt, (940, 520), SIGNAL_YELLOW, progress=p1, width=5)
            if p1 > 0.7:
                draw_badge(draw, (935, 255), "8 MIN INTO FLIGHT: NO. 1 ENGINE FIRE", fg=WHITE, bg=(120, 32, 32), border=TACTICAL_RED, size=22)

        if p2 > 0:
            draw_arrow_curve(draw, turn_pt, frye_plant, (630, 365), TACTICAL_RED, progress=p2, width=6, dashed=True)
            if p2 > 0.75:
                draw_city_dot(draw, frye_plant, "FRYE & CO. PLANT (3 MI SHORT OF RUNWAY)", TACTICAL_RED, dx=-495, dy=-34, size=24)

        # Sober fact summary panel on right
        draw.rounded_rectangle((1375, 200, 1845, 890), radius=10, fill=BG_CARD, outline=TACTICAL_RED, width=3)
        draw.text((1405, 225), "18 FEB 1943 — XB-29 41-3", font=font(FONT_COND, 38), fill=SIGNAL_YELLOW)
        facts = [
            ("CAUSE", "R-3350 overheating & magnesium fire spreading into main wing spar"),
            ("ABOARD (11)", "Boeing chief test pilot Eddie Allen + all 10 flight-test crew lost"),
            ("ON GROUND (21)", "20 Frye & Co. workers + 1 Seattle firefighter (Luther Bonner)"),
            ("TOTAL LOSS", "32 killed — triggered Truman Senate inquiry & NACA cooling overhaul"),
        ]
        for idx, (k, v) in enumerate(facts):
            yy = 300 + idx * 140
            draw.text((1405, yy), k, font=font(FONT_COND, 30), fill=TACTICAL_RED if idx == 3 else STEEL_CYAN)
            words = v.split()
            cur, li = "", 0
            for w in words:
                t = (cur + " " + w).strip()
                if draw.textlength(t, font=font(FONT_BOLD, 20)) <= 410:
                    cur = t
                else:
                    draw.text((1405, yy + 38 + li * 25), cur, font=font(FONT_BOLD, 20), fill=WHITE)
                    cur = w
                    li += 1
            if cur:
                draw.text((1405, yy + 38 + li * 25), cur, font=font(FONT_BOLD, 20), fill=WHITE)

        draw_footer(draw, "SOURCES: USAAF Accident Report XB-29 41-3 (NARA RG 342-FH); NMUSAF; Craven & Cate Vol. VI, p. 247")
        return img

    # Full US Four-Plant Production Map (3,970 Built)
    box = (70, 150, 1360, 995)
    img = render_geo_basemap(-127.0, -66.0, 24.0, 50.5, box=box, show_states=True, grid_step_lon=10, grid_step_lat=10)
    draw = ImageDraw.Draw(img)
    proj = make_projector(-127.0, -66.0, 24.0, 50.5, box)

    draw_header(
        draw,
        "FOUR-PLANT NATIONAL PRODUCTION POOL  |  1942-1945",
        "3,970 B-29 SUPERFORTRESSES BUILT ACROSS FOUR PLANTS",
        ">40,000 PARTS PER AIRCRAFT",
    )

    plants = [
        ("BOEING WICHITA (KS)", -97.33, 37.69, 1644, SIGNAL_YELLOW, (16, 10)),
        ("BOEING RENTON (WA)", -122.21, 47.48, 1119, SIGNAL_YELLOW, (18, -10)),
        ("BELL MARIETTA (GA)", -84.55, 33.95, 668, STEEL_CYAN, (16, -12)),
        ("MARTIN OMAHA (NE)", -95.93, 41.12, 536, AMBER_ORANGE, (16, -28)),
        ("BOEING SEATTLE (XB-29s)", -122.30, 47.53, 3, MUTED, (18, -42)),
    ]

    # Subcontractor feed lines into Wichita/Renton/Omaha/Marietta
    hubs = [proj(-87.6, 41.8), proj(-83.0, 42.3), proj(-84.5, 39.1), proj(-74.0, 40.7)]  # Chicago, Detroit, Lockland/Cincinnati, NJ
    p_lines = ease_out(p, 0.05, 0.45)
    if p_lines > 0:
        for hx, hy in hubs:
            draw.ellipse((hx - 5, hy - 5, hx + 5, hy + 5), fill=COAST_LINE)
            for _, plon, plat, cnt, _, _ in plants[:4]:
                px, py = proj(plon, plat)
                draw_arrow_curve(draw, (hx, hy), (px, py), ((hx + px) / 2, min(hy, py) - 25), (90, 120, 148), progress=p_lines, width=2, dashed=True)

    # Plant markers & right-hand production bar breakdown
    draw.rounded_rectangle((1390, 150, 1850, 995), radius=10, fill=BG_CARD, outline=SIGNAL_YELLOW, width=3)
    draw.text((1420, 178), "PLANT OUTPUT TOTALS", font=font(FONT_COND, 40), fill=SIGNAL_YELLOW)

    for idx, (name, lon, lat, count, col, off) in enumerate(plants):
        prog = ease_out(p, 0.15 + idx * 0.12, 0.48 + idx * 0.12)
        if prog <= 0:
            continue
        px, py = proj(lon, lat)
        r = max(8, int(math.sqrt(count) * 0.65 * prog))
        draw.ellipse((px - r, py - r, px + r, py + r), fill=col, outline=DARK_KEY, width=3)
        if count >= 500:
            draw_city_dot(draw, (px, py), f"{name}: {count:,}", col, dx=off[0], dy=off[1], size=22)

        # Right panel row
        ry = 250 + idx * 122
        draw.text((1420, ry), name, font=font(FONT_COND, 30), fill=WHITE)
        bw = max(6, int(380 * (count / 1644.0) * prog))
        draw.rounded_rectangle((1420, ry + 38, 1420 + bw, ry + 68), radius=4, fill=col)
        draw.text((1420, ry + 74), f"{int(round(count * prog)):,} aircraft", font=font(FONT_MONO, 19), fill=col)

    if p > 0.75:
        draw.line([(1420, 868), (1820, 868)], fill=MUTED, width=2)
        draw.text((1420, 885), "TOTAL BUILT:  3,970", font=font(FONT_COND, 50), fill=SIGNAL_YELLOW)
        draw.text((1420, 945), "Plus Lockland & Dodge R-3350 plants", font=font(FONT_MONO, 17), fill=MUTED)

    draw_footer(draw, "SOURCES: NMUSAF B-29 Fact Sheet; Knaack (1988, p. 498 — 1,644 Wichita, 1,119 Renton, 668 Marietta, 536 Omaha, 3 Seattle)")
    return img


def render_g07_engine_fire(p: float) -> Image.Image:
    img = Image.new("RGB", (W, H), BG_PANEL)
    draw = ImageDraw.Draw(img)
    for gx in range(70, 1851, 90):
        draw.line([(gx, 150), (gx, 980)], fill=GRID_LINE, width=1)
    for gy in range(180, 981, 90):
        draw.line([(70, gy), (1850, gy)], fill=GRID_LINE, width=1)

    draw_header(
        draw,
        "WRIGHT R-3350 DUPLEX-CYCLONE  |  18 CYLINDERS  ·  2,200 HP",
        "WHY B-29 ENGINE FIRES BURNED THROUGH THE WING IN 90 SECONDS",
        "TIGHT NACELLE COWLING & MAGNESIUM HOUSING",
    )

    # Nacelle aerodynamic cowling outline (airflow left -> right toward main wing spar)
    cowling_top = [(260, 390), (420, 330), (980, 340), (1460, 410)]
    cowling_bot = [(260, 690), (420, 750), (980, 740), (1460, 670)]
    draw.polygon(cowling_top + list(reversed(cowling_bot)), fill=(44, 56, 72), outline=WHITE, width=3)

    # Propeller hub & blades at left
    draw.polygon([(195, 510), (260, 485), (260, 595), (195, 570)], fill=COAST_LINE, outline=WHITE, width=2)
    draw.rounded_rectangle((222, 220, 246, 860), radius=8, fill=(160, 175, 190), outline=WHITE, width=2)

    # Front cylinder row (9 cylinders, cooled)
    draw.rounded_rectangle((410, 355, 545, 725), radius=10, fill=(56, 128, 168), outline=STEEL_CYAN, width=3)
    draw.text((428, 515), "FRONT\nROW (9)", font=font(FONT_COND, 32), fill=WHITE)

    # Rear cylinder row (9 cylinders, starved of air -> overheated)
    p_heat = ease_out(p, 0.15, 0.55)
    rear_col = (int(90 + 145 * p_heat), int(75 - 25 * p_heat), 55)
    draw.rounded_rectangle((575, 355, 710, 725), radius=10, fill=rear_col, outline=AMBER_ORANGE, width=3)
    draw.text((592, 515), "REAR\nROW (9)", font=font(FONT_COND, 32), fill=WHITE)

    # Magnesium rear accessory drive housing & supercharger casing
    p_fire = ease_out(p, 0.45, 0.85)
    mag_col = (245, 65, 48) if p_fire > 0.3 else (110, 96, 82)
    draw.rounded_rectangle((745, 415, 995, 665), radius=12, fill=mag_col, outline=SIGNAL_YELLOW, width=3)
    draw.text((772, 492), "MAGNESIUM ALLOY\nACCESSORY HOUSING\n(>3,000°F FIRE)", font=font(FONT_COND, 30), fill=WHITE)

    # Aluminium main wing spar behind firewall
    draw.rectangle((1150, 395, 1365, 685), fill=(95, 110, 126), outline=SIGNAL_YELLOW, width=4)
    draw.text((1175, 500), "ALUMINIUM\nMAIN WING\nSPAR", font=font(FONT_COND, 36), fill=SIGNAL_YELLOW)

    # Cooling airflow arrows blocked at front row
    for ay in (405, 675):
        draw_arrow_curve(draw, (95, ay), (405, ay), (250, ay), STEEL_CYAN, progress=min(1.0, p * 2.2), width=5)
    draw.text((88, 318), "COOLING\nAIRFLOW", font=font(FONT_COND, 28), fill=STEEL_CYAN)

    if p_fire > 0:
        draw_arrow_curve(draw, (995, 540), (1148, 540), (1070, 540), TACTICAL_RED, progress=p_fire, width=8)
        if p_fire > 0.5:
            draw_badge(
                draw,
                (1070, 265),
                "CO2 EXTINGUISHERS CANNOT STOP MAGNESIUM  ->  WING SPAR FAILS IN 60-90 SECONDS",
                fg=WHITE,
                bg=(145, 28, 28),
                border=SIGNAL_YELLOW,
                size=24,
            )

    # Bottom sequence callouts
    steps = [
        ("1. TIGHT COWLING", "Front cylinders block cooling air to rear row on heavy climb", STEEL_CYAN),
        ("2. EXHAUST VALVES FAIL", "Overheated rear valves warp, snap, and spark oil backfires", AMBER_ORANGE),
        ("3. MAGNESIUM IGNITES", "Burns above 3,000°F right in front of the aluminium wing spar", TACTICAL_RED),
    ]
    for idx, (st, desc, col) in enumerate(steps):
        if p > 0.25 + idx * 0.2:
            bx = 110 + idx * 575
            draw.rounded_rectangle((bx, 815, bx + 545, 965), radius=8, fill=BG_CARD, outline=col, width=2)
            draw.text((bx + 20, 832), st, font=font(FONT_COND, 32), fill=col)
            words = desc.split()
            cur, li = "", 0
            for w_tok in words:
                test = (cur + " " + w_tok).strip()
                if draw.textlength(test, font=font(FONT_BOLD, 20)) <= 505:
                    cur = test
                else:
                    draw.text((bx + 20, 882 + li * 28), cur, font=font(FONT_BOLD, 20), fill=WHITE)
                    cur = w_tok
                    li += 1
            if cur:
                draw.text((bx + 20, 882 + li * 28), cur, font=font(FONT_BOLD, 20), fill=WHITE)

    draw_footer(draw, "SOURCES: Craven & Cate Vol. VI, p. 247; NACA Cleveland Altitude Wind Tunnel (1944, GRC-1944-C-05552)")
    return img


def render_g08_matterhorn_map(p: float) -> Image.Image:
    box = (70, 150, 1340, 995)
    img = render_geo_basemap(80.0, 138.0, 10.0, 40.0, box=box, grid_step_lon=10, grid_step_lat=10)
    draw = ImageDraw.Draw(img)
    proj = make_projector(80.0, 138.0, 10.0, 40.0, box)

    draw_header(
        draw,
        "OPERATION MATTERHORN  |  JUNE 1944 - JAN 1945",
        "FLYING EVERY GALLON OVER THE HIMALAYAS TO STRIKE JAPAN",
        "INDIA -> THE HUMP -> CHENGDU -> KYUSHU",
    )

    kharagpur = proj(87.3, 22.3)
    chengdu = proj(104.1, 30.7)
    bangkok = proj(100.5, 13.75)
    yawata = proj(130.8, 33.87)

    # Himalaya ridge highlight
    hx, hy = proj(94.5, 28.5)
    draw_badge(draw, (hx - 20, hy - 42), "THE HUMP (HIMALAYAS)", fg=SIGNAL_YELLOW, border=AMBER_ORANGE, size=20)

    p1 = ease_out(p, 0.08, 0.48)
    p2 = ease_out(p, 0.45, 0.85)
    if p1 > 0:
        draw_arrow_curve(draw, kharagpur, chengdu, (94.0 and (kharagpur[0] + chengdu[0]) / 2 - 30, (kharagpur[1] + chengdu[1]) / 2 - 55), AMBER_ORANGE, progress=p1, width=6)
        draw_arrow_curve(draw, kharagpur, bangkok, ((kharagpur[0] + bangkok[0]) / 2 - 20, (kharagpur[1] + bangkok[1]) / 2 + 25), STEEL_CYAN, progress=p1, width=4, dashed=True)

    if p2 > 0:
        draw_arrow_curve(draw, chengdu, yawata, ((chengdu[0] + yawata[0]) / 2, min(chengdu[1], yawata[1]) - 65), TACTICAL_RED, progress=p2, width=6)

    draw_city_dot(draw, kharagpur, "KHARAGPUR BASES (INDIA)", SIGNAL_YELLOW, dx=-90, dy=20, size=22)
    draw_city_dot(draw, chengdu, "CHENGDU STAGING FIELDS", SIGNAL_YELLOW, dx=-95, dy=-34, size=22)
    draw_city_dot(draw, bangkok, "BANGKOK (5 JUN 1944)", STEEL_CYAN, dx=14, dy=4, size=20)
    draw_city_dot(draw, yawata, "YAWATA STEEL WORKS (15 JUN 1944)", TACTICAL_RED, dx=-355, dy=-36, size=22)

    # Right-side Hump Fuel Tanker Pyramid Counter
    draw.rounded_rectangle((1370, 150, 1850, 995), radius=10, fill=BG_CARD, outline=AMBER_ORANGE, width=3)
    draw.text((1400, 178), "IMPOSSIBLE LOGISTICS", font=font(FONT_COND, 42), fill=AMBER_ORANGE)
    draw.text((1400, 232), "Zero sea or road supply to Chengdu.", font=font(FONT_BOLD, 21), fill=WHITE)
    draw.text((1400, 260), "Stripped B-29s used as fuel tankers.", font=font(FONT_BOLD, 21), fill=MUTED)

    # 7 Hump tanker bars -> 1 combat sortie bar
    n_trips = int(round(7 * ease_out(p, 0.25, 0.75)))
    draw.text((1400, 325), "HUMP TANKER TRIPS NEEDED:", font=font(FONT_COND, 32), fill=SIGNAL_YELLOW)
    for i in range(7):
        by = 375 + i * 50
        active = i < n_trips
        col = AMBER_ORANGE if active else (55, 68, 84)
        draw.rounded_rectangle((1400, by, 1815, by + 36), radius=5, fill=col, outline=WHITE if active else BORDER_LINE, width=1)
        draw.text((1418, by + 6), f"HUMP SUPPLY FLIGHT #{i + 1}", font=font(FONT_MONO, 18), fill=DARK_KEY if active else MUTED)

    if p > 0.65:
        draw.rounded_rectangle((1400, 755, 1815, 855), radius=8, fill=TACTICAL_RED, outline=WHITE, width=3)
        draw.text((1422, 772), "=  1 COMBAT SORTIE", font=font(FONT_COND, 44), fill=WHITE)
        draw.text((1422, 820), "6-7 Hump trips per raid on Japan", font=font(FONT_BOLD, 20), fill=SIGNAL_YELLOW)
        draw.text((1400, 885), "• 300,000+ Chinese workers built fields", font=font(FONT_BOLD, 20), fill=WHITE)
        draw.text((1400, 918), "• Yawata: 68 launched, 47 bombed, 7 lost", font=font(FONT_BOLD, 20), fill=MUTED)

    draw_footer(draw, "SOURCES: Craven & Cate Vol. V, Ch. 3-5, pp. 75-112 (Operation Matterhorn Hump fuel ratio & 15 June 1944 Yawata raid)")
    return img


def render_g09_pacific_map(p: float, cities_mode: bool = False) -> Image.Image:
    if not cities_mode:
        box = (70, 150, 1340, 995)
        img = render_geo_basemap(122.0, 165.0, 10.0, 41.0, box=box, grid_step_lon=10, grid_step_lat=10)
        draw = ImageDraw.Draw(img)
        proj = make_projector(122.0, 165.0, 10.0, 41.0, box)

        draw_header(
            draw,
            "XXI BOMBER COMMAND  |  MARIANA ISLANDS  (1944-1945)",
            "1,500 MILES OVER OPEN WATER TO TOKYO",
            "DIRECT SEA SUPPLY + IWO JIMA EMERGENCY STRIP",
        )

        tinian = proj(145.63, 15.05)
        saipan = proj(145.75, 15.20)
        guam = proj(144.78, 13.45)
        iwo = proj(141.32, 24.78)
        tokyo = proj(139.75, 35.68)
        sea_entry = proj(163.5, 16.5)

        p1 = ease_out(p, 0.05, 0.45)
        p2 = ease_out(p, 0.38, 0.85)
        if p1 > 0:
            draw_arrow_curve(draw, sea_entry, tinian, ((sea_entry[0] + tinian[0]) / 2, tinian[1] - 35), STEEL_CYAN, progress=p1, width=6)
            if p1 > 0.6:
                draw_badge(draw, (1125, 760), "DIRECT US TANKER & CARGO SHIPS", fg=STEEL_CYAN, border=STEEL_CYAN, size=21)

        if p2 > 0:
            draw_arrow_curve(draw, tinian, tokyo, (iwo[0] + 25, iwo[1]), SIGNAL_YELLOW, progress=p2, width=6)

        draw_city_dot(draw, saipan, "SAIPAN & TINIAN (NORTH FIELD)", SIGNAL_YELLOW, dx=-355, dy=-32, size=23)
        draw_city_dot(draw, guam, "GUAM", SIGNAL_YELLOW, dx=16, dy=6, size=21)
        draw_city_dot(draw, iwo, "IWO JIMA (HALFWAY — 2,251 LANDINGS)", SAFE_GREEN, dx=-430, dy=-12, size=22)
        draw_city_dot(draw, tokyo, "TOKYO (~1,500 MILES)", TACTICAL_RED, dx=18, dy=-16, size=25)

        # Right-hand operational facts card
        draw.rounded_rectangle((1370, 150, 1850, 995), radius=10, fill=BG_CARD, outline=SIGNAL_YELLOW, width=3)
        draw.text((1400, 180), "TINIAN NORTH FIELD", font=font(FONT_COND, 42), fill=SIGNAL_YELLOW)
        cards = [
            ("SEABEE MEGA-BASE", "4 parallel 8,500-ft coral runways (+2 at West Field) — world's busiest bomber base"),
            ("1,500-MILE CORRIDOR", "3,000-mile overwater round trip; engine trouble meant ditching at sea"),
            ("IWO JIMA LIFELINE", "Captured Feb-Mar 1945; first landing 'Dinah Might' (4 Mar 1945)"),
            ("24,761 AIRMEN SAVED", "2,251 emergency B-29 landings on Iwo Jima by war's end"),
        ]
        for idx, (k, v) in enumerate(cards):
            yy = 265 + idx * 175
            col = SAFE_GREEN if idx >= 2 else WHITE
            draw.text((1400, yy), k, font=font(FONT_COND, 32), fill=SIGNAL_YELLOW if idx < 2 else SAFE_GREEN)
            words = v.split()
            cur, li = "", 0
            for w in words:
                t = (cur + " " + w).strip()
                if draw.textlength(t, font=font(FONT_BOLD, 21)) <= 415:
                    cur = t
                else:
                    draw.text((1400, yy + 40 + li * 27), cur, font=font(FONT_BOLD, 21), fill=col)
                    cur = w
                    li += 1
            if cur:
                draw.text((1400, yy + 40 + li * 27), cur, font=font(FONT_BOLD, 21), fill=col)

        draw_footer(draw, "SOURCES: Craven & Cate Vol. V, Ch. 16 & Ch. 18 (pp. 507-525, 592-597 — Tinian North Field & 2,251 Iwo Jima landings)")
        return img

    # Cities mode (S55, S56): March-August 1945 Low-Altitude Campaign across 60+ Japanese Cities
    box = (70, 150, 1310, 995)
    img = render_geo_basemap(128.5, 142.5, 30.5, 41.5, box=box, grid_step_lon=4, grid_step_lat=4)
    draw = ImageDraw.Draw(img)
    proj = make_projector(128.5, 142.5, 30.5, 41.5, box)

    draw_header(
        draw,
        "MARCH - AUGUST 1945 CAMPAIGN  |  XXI BOMBER COMMAND",
        "OVER 60 JAPANESE CITIES STRUCK & SHIMONOSEKI PORT MINING",
        "LOW-ALTITUDE NIGHT INCENDIARY & OIL CAMPAIGN",
    )

    cities = [
        ("TOKYO (9-10 MAR)", 139.77, 35.68, True),
        ("YOKOHAMA", 139.64, 35.44, False),
        ("NAGOYA", 136.91, 35.18, True),
        ("OSAKA", 135.50, 34.69, True),
        ("KOBE", 135.19, 34.69, True),
        ("KAWASAKI", 139.70, 35.53, False),
        ("SHIZUOKA", 138.38, 34.98, False),
        ("HAMAMATSU", 137.73, 34.71, False),
        ("TOYAMA", 137.21, 36.70, False),
        ("SENDAI", 140.87, 38.27, False),
        ("AOMORI", 140.74, 40.82, False),
        ("OKAYAMA", 133.93, 34.66, False),
        ("KURE", 132.56, 34.25, False),
        ("HIROSHIMA (6 AUG)", 132.46, 34.39, True),
        ("FUKUOKA", 130.40, 33.59, False),
        ("YAWATA", 130.80, 33.87, False),
        ("NAGASAKI (9 AUG)", 129.87, 32.75, True),
        ("KAGOSHIMA", 130.56, 31.60, False),
        ("MATSUYAMA", 132.77, 33.84, False),
        ("KOCHI", 133.53, 33.56, False),
        ("GIFU", 136.76, 35.42, False),
        ("YOKKAICHI", 136.62, 34.97, False),
        ("WAKAYAMA", 135.17, 34.23, False),
        ("HIMEJI", 134.69, 34.82, False),
        ("FUKUI", 136.22, 36.06, False),
        ("KOFU", 138.57, 35.66, False),
        ("HITACHI", 140.65, 36.60, False),
        ("UTSUNOMIYA", 139.88, 36.56, False),
    ]
    n_vis = max(1, int(round(len(cities) * ease_out(p, 0.05, 0.80))))
    for name, lon, lat, major in cities[:n_vis]:
        cx, cy = proj(lon, lat)
        r = 10 if major else 6
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=TACTICAL_RED if major else AMBER_ORANGE, outline=WHITE, width=2)

    # Selected non-overlapping labels
    tx_tok, ty_tok = proj(139.77, 35.68)
    draw_city_dot(draw, (tx_tok, ty_tok), "TOKYO", TACTICAL_RED, dx=16, dy=-22, size=22)
    draw.text((tx_tok + 16, ty_tok + 4), "(15.8 SQ MI BURNED)", font=font(FONT_BOLD, 17), fill=SIGNAL_YELLOW)
    draw_city_dot(draw, proj(136.91, 35.18), "NAGOYA", TACTICAL_RED, dx=14, dy=10, size=20)
    draw_city_dot(draw, proj(135.50, 34.69), "OSAKA / KOBE", TACTICAL_RED, dx=-155, dy=20, size=20)
    draw_city_dot(draw, proj(132.46, 34.39), "HIROSHIMA", SIGNAL_YELLOW, dx=-55, dy=-38, size=20)
    draw_city_dot(draw, proj(129.87, 32.75), "NAGASAKI", SIGNAL_YELLOW, dx=14, dy=8, size=20)
    sx, sy = proj(130.94, 33.95)
    draw.line([(sx, sy), (sx - 68, sy - 92)], fill=STEEL_CYAN, width=2)
    draw.ellipse((sx - 5, sy - 5, sx + 5, sy + 5), fill=STEEL_CYAN)
    draw_badge(draw, (sx - 82, sy - 114), "SHIMONOSEKI MINING", fg=STEEL_CYAN, border=STEEL_CYAN, size=18)

    # Right summary card (strictly factual, sober historical tone)
    draw.rounded_rectangle((1345, 150, 1850, 995), radius=10, fill=BG_CARD, outline=TACTICAL_RED, width=3)
    draw.text((1375, 180), "OPERATION MEETINGHOUSE", font=font(FONT_COND, 40), fill=SIGNAL_YELLOW)
    draw.text((1375, 232), "9-10 MARCH 1945  (TOKYO)", font=font(FONT_MONO, 20), fill=MUTED)
    rows = [
        ("279 B-29s OVER TARGET", "334 launched at 5,000-8,000 ft at night"),
        ("15.8 SQUARE MILES BURNED", "Dense urban-industrial districts destroyed"),
        ("80,000 - 100,000 KILLED", "Mostly civilians; 14 B-29s lost"),
        ("66 URBAN AREAS STRUCK", "Extended across Japan, Mar-Aug 1945, plus oil raids & port mining"),
    ]
    for idx, (h_t, s_t) in enumerate(rows):
        yy = 295 + idx * 165
        draw.rectangle((1375, yy + 6, 1383, yy + 72), fill=TACTICAL_RED if idx < 3 else AMBER_ORANGE)
        draw.text((1400, yy), h_t, font=font(FONT_COND, 34), fill=WHITE)
        words = s_t.split()
        cur, li = "", 0
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=font(FONT_BOLD, 20)) <= 420:
                cur = t
            else:
                draw.text((1400, yy + 42 + li * 26), cur, font=font(FONT_BOLD, 20), fill=MUTED)
                cur = w
                li += 1
        if cur:
            draw.text((1400, yy + 42 + li * 26), cur, font=font(FONT_BOLD, 20), fill=MUTED)

    draw_footer(draw, "SOURCES: US Strategic Bombing Survey Summary Report (1946, p. 16); Craven & Cate Vol. V, pp. 614-617; Frank (1999)")
    return img


def render_g10_jet_stream(p: float) -> Image.Image:
    img = Image.new("RGB", (W, H), BG_PANEL)
    draw = ImageDraw.Draw(img)
    for gx in range(70, 1851, 100):
        draw.line([(gx, 150), (gx, 980)], fill=GRID_LINE, width=1)

    draw_header(
        draw,
        "30,000 FEET OVER HONSHU  |  NOV 1944 - FEB 1945",
        "THE 150-230 MPH JET STREAM THAT WRECKED HIGH-ALTITUDE PRECISION",
        "<5% OF BOMBS WITHIN 1,000 FT OF TARGET",
    )

    # Jet stream roaring ribbon across upper half (y=210..440)
    p_wind = ease_out(p, 0.05, 0.45)
    draw.rounded_rectangle((90, 185, 1830, 445), radius=14, fill=(36, 62, 92), outline=STEEL_CYAN, width=2)
    draw.text((120, 202), "30,000 FT SUBTROPICAL JET STREAM   (WEST -> EAST:  150 TO 200+ MPH)", font=font(FONT_COND, 38), fill=STEEL_CYAN)
    for wy in (270, 330, 390):
        end_x = int(140 + 1620 * p_wind)
        draw_arrow_curve(draw, (140, wy), (end_x, wy), ((140 + end_x) / 2, wy - 14), STEEL_CYAN, progress=1.0, width=5)

    # Downwind vs Upwind comparison panels
    p_cases = ease_out(p, 0.35, 0.85)
    if p_cases > 0:
        # Left card: Downwind
        draw.rounded_rectangle((90, 485, 935, 965), radius=12, fill=BG_CARD, outline=SIGNAL_YELLOW, width=3)
        draw.text((125, 510), "CASE A: FLYING DOWNWIND", font=font(FONT_COND, 42), fill=SIGNAL_YELLOW)
        draw.text((125, 570), "450 - 500 MPH GROUNDSPEED", font=font(FONT_COND, 54), fill=WHITE)
        draw.text((125, 645), "• Bomber airspeed (~280 mph) + 200 mph tailwind", font=font(FONT_BOLD, 23), fill=WHITE)
        draw.text((125, 685), "• Exceeds Norden bombsight tracking rate", font=font(FONT_BOLD, 23), fill=TACTICAL_RED)
        draw.text((125, 725), "• Bombs overshoot aiming point by >1 mile", font=font(FONT_BOLD, 23), fill=MUTED)
        # Visual bomb drift arc
        draw.line([(150, 810), (780, 810)], fill=SIGNAL_YELLOW, width=4)
        draw_arrow_curve(draw, (340, 810), (760, 925), (590, 825), TACTICAL_RED, progress=p_cases, width=4, dashed=True)
        draw.ellipse((515, 915, 535, 935), outline=WHITE, width=3)
        draw.text((445, 938), "TARGET", font=font(FONT_MONO, 16), fill=WHITE)
        draw.text((705, 932), "OVERSHOOT", font=font(FONT_MONO, 16), fill=TACTICAL_RED)

        # Right card: Upwind / Crosswind
        draw.rounded_rectangle((985, 485, 1830, 965), radius=12, fill=BG_CARD, outline=TACTICAL_RED, width=3)
        draw.text((1020, 510), "CASE B: FLYING UPWIND / CROSSWIND", font=font(FONT_COND, 42), fill=TACTICAL_RED)
        draw.text((1020, 570), "<120 MPH CRAWL OVER TARGET", font=font(FONT_COND, 54), fill=WHITE)
        draw.text((1020, 645), "• Nearly stationary over Japanese heavy AA guns", font=font(FONT_BOLD, 23), fill=TACTICAL_RED)
        draw.text((1020, 685), "• Severe fuel burn threatens 1,500-mile return", font=font(FONT_BOLD, 23), fill=WHITE)
        draw.text((1020, 725), "• 24 Nov 1944 Tokyo: only 24 of 111 hit plant area", font=font(FONT_BOLD, 23), fill=SIGNAL_YELLOW)
        draw.rounded_rectangle((1020, 795, 1795, 925), radius=8, fill=(52, 34, 38), outline=TACTICAL_RED, width=2)
        draw.text((1050, 820), "FIRST 2 MONTHS ACCURACY:  UNDER 5%", font=font(FONT_COND, 44), fill=SIGNAL_YELLOW)
        draw.text((1050, 875), "Fewer than 5% of bombs fell within 1,000 ft of aiming points", font=font(FONT_BOLD, 21), fill=WHITE)

    draw_footer(draw, "SOURCES: Craven & Cate Vol. V, Ch. 17, pp. 558-576; US Strategic Bombing Survey (Twentieth Air Force, 1946)")
    return img


def render_g11_tactical_or_losses(p: float, losses_mode: bool = False) -> Image.Image:
    img = Image.new("RGB", (W, H), BG_PANEL)
    draw = ImageDraw.Draw(img)

    if not losses_mode:
        draw_header(
            draw,
            "CURTIS LEMAY'S MARCH 1945 DOCTRINE PIVOT",
            "FROM 30,000-FT DAYLIGHT PRECISION TO 5,000-FT NIGHT RAIDS",
            "BELOW THE JET STREAM & WINTER CLOUD",
        )
        # Altitude scale on left (0 to 35,000 ft)
        y_ground = 935
        y_30k = 245
        y_7k = 775
        draw.rectangle((90, 935, 1830, 985), fill=LAND_FILL)
        draw.line([(190, 180), (190, 935)], fill=COAST_LINE, width=3)
        for alt, yy in [(30000, y_30k), (20000, 480), (10000, 710), (7000, y_7k), (0, y_ground)]:
            draw.line([(175, yy), (1830, yy)], fill=GRID_LINE, width=1)
            draw.text((82, yy - 12), f"{alt:,} FT", font=font(FONT_MONO, 17), fill=MUTED)

        # Jet stream band & cloud deck
        draw.rounded_rectangle((210, 215, 1810, 305), radius=8, fill=(38, 66, 98), outline=STEEL_CYAN, width=2)
        draw.text((235, 245), "30,000 FT:  150-200+ MPH JET STREAM  ·  HEAVY ENGINE CLIMB STRAIN  ·  2.5-3 TON LOAD  ·  <5% ACCURACY", font=font(FONT_COND, 30), fill=STEEL_CYAN)

        draw.rounded_rectangle((210, 505, 1810, 605), radius=18, fill=(68, 78, 92), outline=COAST_LINE, width=1)
        draw.text((765, 540), "WINTER CLOUD DECK  (15,000 - 22,000 FT)", font=font(FONT_COND, 30), fill=MUTED)

        p_low = ease_out(p, 0.25, 0.85)
        if p_low > 0:
            draw_arrow_curve(draw, (310, 260), (620, y_7k), (430, 620), SIGNAL_YELLOW, progress=p_low, width=6)
            ex = int(620 + 1140 * p_low)
            draw.line([(620, y_7k), (ex, y_7k)], fill=SIGNAL_YELLOW, width=7)
            if p_low > 0.45:
                draw.rounded_rectangle((620, 645, 1795, 750), radius=10, fill=(64, 52, 28), outline=SIGNAL_YELLOW, width=3)
                draw.text(
                    (648, 662),
                    "MARCH 1945 SHIFT:  5,000 - 8,000 FT INDIVIDUAL NIGHT RUNS",
                    font=font(FONT_COND, 38),
                    fill=SIGNAL_YELLOW,
                )
                draw.text(
                    (648, 708),
                    "Defensive guns stripped  ·  Cooler R-3350 engines  ·  6-8 TON (>2x) M69 incendiary load",
                    font=font(FONT_BOLD, 22),
                    fill=WHITE,
                )

        draw_footer(draw, "SOURCES: Craven & Cate Vol. V, Ch. 19, pp. 608-615; LeMay (1965); USSBS Twentieth Air Force Report")
        return img

    # Losses mode (S62): Twentieth Air Force 414 Combat-Mission Losses Breakdown
    draw_header(
        draw,
        "TWENTIETH AIR FORCE COMBAT-MISSION LOSSES  |  1944-1945",
        "NEARLY TWO-THIRDS OF B-29 LOSSES WERE NOT TO ENEMY FIRE",
        "414 B-29s LOST ON COMBAT MISSIONS AGAINST JAPAN",
    )

    p1 = ease_out(p, 0.08, 0.55)
    p2 = ease_out(p, 0.35, 0.82)

    # Stacked full-width summary bar (414 total = 267 mechanical/operational + 147 enemy action)
    bar_x0, bar_w_tot = 110, 1700
    w_mech = int(bar_w_tot * (267 / 414.0) * p1)
    w_enem = int(bar_w_tot * (147 / 414.0) * p2)

    draw.text((110, 210), "TOTAL COMBAT-MISSION LOSSES:  414 B-29 SUPERFORTRESSES", font=font(FONT_COND, 44), fill=WHITE)
    if w_mech > 0:
        draw.rounded_rectangle((bar_x0, 275, bar_x0 + w_mech, 405), radius=8, fill=AMBER_ORANGE, outline=WHITE, width=3)
        if p1 > 0.5:
            draw.text((bar_x0 + 28, 305), "267 MECHANICAL, ENGINE FIRE & OPERATIONAL  (64.5%)", font=font(FONT_COND, 42), fill=DARK_KEY)
    if w_enem > 0:
        sx = bar_x0 + int(bar_w_tot * (267 / 414.0))
        draw.rounded_rectangle((sx, 275, sx + w_enem, 405), radius=8, fill=TACTICAL_RED, outline=WHITE, width=3)
        if p2 > 0.5:
            draw.text((sx + 24, 305), "147 ENEMY ACTION (35.5%)", font=font(FONT_COND, 40), fill=WHITE)

    # Two detail cards below
    if p > 0.45:
        draw.rounded_rectangle((110, 475, 1160, 945), radius=12, fill=BG_CARD, outline=AMBER_ORANGE, width=3)
        draw.text((145, 505), "267 LOST TO ENGINE FIRES, FAILURES & ACCIDENTS", font=font(FONT_COND, 44), fill=AMBER_ORANGE)
        draw.text((145, 575), "• Wright R-3350 overheating & magnesium nacelle fires", font=font(FONT_BOLD, 25), fill=WHITE)
        draw.text((145, 625), "• Heavy-weight takeoff crashes & long overwater ditchings", font=font(FONT_BOLD, 25), fill=WHITE)
        draw.text((145, 675), "• Direct cost of rushing an unproved engine & airframe to war", font=font(FONT_BOLD, 25), fill=SIGNAL_YELLOW)
        draw.text((145, 795), "64.5%", font=font(FONT_COND, 110), fill=AMBER_ORANGE)
        draw.text((385, 845), "OF ALL COMBAT-MISSION LOSSES", font=font(FONT_COND, 36), fill=MUTED)

        draw.rounded_rectangle((1205, 475, 1810, 945), radius=12, fill=BG_CARD, outline=TACTICAL_RED, width=3)
        draw.text((1240, 505), "147 TO ENEMY FIRE", font=font(FONT_COND, 44), fill=TACTICAL_RED)
        draw.text((1240, 575), "• Japanese fighters &", font=font(FONT_BOLD, 25), fill=WHITE)
        draw.text((1240, 610), "  anti-aircraft artillery", font=font(FONT_BOLD, 25), fill=WHITE)
        draw.text((1240, 795), "35.5%", font=font(FONT_COND, 110), fill=TACTICAL_RED)

    draw_footer(draw, "SOURCES: Craven & Cate Vol. V, pp. 752-756; US Strategic Bombing Survey (414 losses: 147 enemy fire vs 267 operational)")
    return img


def render_g12_legacy(p: float, cruise_mode: bool = False) -> Image.Image:
    img = Image.new("RGB", (W, H), BG_PANEL)
    draw = ImageDraw.Draw(img)

    if not cruise_mode:
        draw_header(
            draw,
            "POST-WAR AVIATION LINEAGE  |  1945-1960s",
            "WHAT THE $3 BILLION B-29 GAMBLE LEFT BEHIND",
            "PRESSURISED CABINS · HIGH-ASPECT WING · LONG-RANGE FLIGHT",
        )
        # Root node at top center
        root = (660, 195, 1260, 335)
        draw.rounded_rectangle(root, radius=12, fill=(58, 52, 26), outline=SIGNAL_YELLOW, width=4)
        draw.text((715, 215), "BOEING MODEL 345 / B-29 SUPERFORTRESS", font=font(FONT_COND, 38), fill=SIGNAL_YELLOW)
        draw.text((715, 268), "Pressurised fuselage · 141-ft wing · Remote systems", font=font(FONT_BOLD, 21), fill=WHITE)

        children = [
            ("BOEING B-50\nSUPERFORTRESS", "Upgraded R-4360 engines,\ntaller tail, SAC deterrent", STEEL_CYAN, 260),
            ("C-97 & KC-97\nSTRATOFREIGHTER", "Double-deck military transport\n& strategic aerial tanker", SAFE_GREEN, 730),
            ("BOEING 377\nSTRATOCRUISER", "Pressurised transoceanic\nluxury commercial airliner", SIGNAL_YELLOW, 1200),
            ("TUPOLEV Tu-4\n(SOVIET UNION)", "Reverse-engineered bolt-for-bolt\nfrom 3 interned B-29s", TACTICAL_RED, 1660),
        ]
        for idx, (title_c, desc_c, col, cx) in enumerate(children):
            prog = ease_out(p, 0.12 + idx * 0.15, 0.45 + idx * 0.15)
            if prog <= 0:
                continue
            draw_arrow_curve(draw, (960, 335), (cx, 535), ((960 + cx) / 2, 435), col, progress=prog, width=4)
            if prog > 0.35:
                draw.rounded_rectangle((cx - 205, 540, cx + 205, 895), radius=10, fill=BG_CARD, outline=col, width=3)
                for li, ln in enumerate(title_c.split("\n")):
                    draw.text((cx - 180, 568 + li * 44), ln, font=font(FONT_COND, 38), fill=col)
                for li, ln in enumerate(desc_c.split("\n")):
                    draw.text((cx - 180, 695 + li * 32), ln, font=font(FONT_BOLD, 22), fill=WHITE)

        draw_footer(draw, "SOURCES: Knaack (1988, B-50 chapter); NMUSAF Fact Sheets (Boeing 377 Stratocruiser, C-97/KC-97, Tupolev Tu-4)")
        return img

    # Cruise mode (S64): High-Altitude Pressurised Cruise Above the Weather
    draw_header(
        draw,
        "MODERN AVIATION INHERITANCE  |  PRESSURISED FLIGHT",
        "SEALED CABINS CRUISING SMOOTHLY ABOVE THE WEATHER",
        "EXOTIC IN 1940 -> ORDINARY FOR MILLIONS TODAY",
    )
    # Stratosphere / high cruise band vs storm weather below 18,000 ft
    draw.rectangle((90, 935, 1830, 985), fill=LAND_FILL)
    draw.rounded_rectangle((90, 565, 1830, 825), radius=24, fill=(62, 72, 86), outline=COAST_LINE, width=2)
    draw.text((685, 675), "TURBULENCE, ICING & STORM WEATHER  (BELOW 18,000 FT)", font=font(FONT_COND, 34), fill=MUTED)

    p_flt = ease_out(p, 0.08, 0.85)
    end_x = int(200 + 1500 * p_flt)
    draw_arrow_curve(draw, (200, 325), (end_x, 325), ((200 + end_x) / 2, 325), SIGNAL_YELLOW, progress=1.0, width=6)
    draw_badge(
        draw,
        (960, 250),
        "30,000 - 38,000 FT:  SEALED CABIN AT 8,000-FT PRESSURE  ·  SMOOTH TRANSOCEANIC CRUISE",
        fg=SIGNAL_YELLOW,
        border=SIGNAL_YELLOW,
        size=25,
    )
    draw.text((95, 395), "1940: Oxygen masks & frostbite above 20,000 ft   ->   1944 B-29: Pressurised long-range cabin proven at scale", font=font(FONT_BOLD, 24), fill=WHITE)
    draw_footer(draw, "SOURCES: NMUSAF Boeing B-29 & Boeing 377 Stratocruiser Technical Histories")
    return img


GRAPHICS_SPECS: List[Tuple[str, str, List[str], str, Callable[[float], Image.Image]]] = [
    ("G1", "code_graphic_ww2_003_g01", ["S01", "S60"], "Cost comparison bar chart ($3.0B B-29 vs $1.9B Manhattan Project)", lambda p: render_g01_cost(p, False)),
    ("G1b", "code_graphic_ww2_003_g01_breakdown", ["S62a"], "Full industrial breakdown ($1.9B Manhattan vs $3.0B B-29)", lambda p: render_g01_cost(p, True)),
    ("G2", "code_graphic_ww2_003_g02", ["S06"], "1940 Pacific distances & R-40B 5,333-mile specification map", render_g02_range_map),
    ("G3", "code_graphic_ww2_003_g03", ["S12"], "B-29 pressurised cabins & 28-inch crawl tunnel cross-section", render_g03_pressurised_tunnel),
    ("G4", "code_graphic_ww2_003_g04", ["S14"], "General Electric central station analogue fire-control diagram", render_g04_fire_control),
    ("G5", "code_graphic_ww2_003_g05", ["S17"], "Off-the-drawing-board procurement timeline (1,664 ordered before first flight)", render_g05_procurement_timeline),
    ("G6", "code_graphic_ww2_003_g06", ["S18", "S61"], "Four-plant US B-29 production map (3,970 built)", lambda p: render_g06_plants_map(p, False)),
    ("G6s", "code_graphic_ww2_003_g06_seattle", ["S27"], "18 Feb 1943 Seattle XB-29 (41-3) flight-path map", lambda p: render_g06_plants_map(p, True)),
    ("G7", "code_graphic_ww2_003_g07", ["S22"], "Wright R-3350 rear-row cooling starvation & >3,000F magnesium fire diagram", render_g07_engine_fire),
    ("G8", "code_graphic_ww2_003_g08", ["S31", "S40"], "Operation Matterhorn map & 6-7 Hump trips per combat sortie counter", render_g08_matterhorn_map),
    ("G9", "code_graphic_ww2_003_g09", ["S43", "S44"], "Marianas 1,500-mile Pacific strike corridor & Iwo Jima emergency strip map", lambda p: render_g09_pacific_map(p, False)),
    ("G9c", "code_graphic_ww2_003_g09_cities", ["S55", "S56"], "March-August 1945 campaign map (60+ Japanese cities & Tokyo 15.8 sq mi)", lambda p: render_g09_pacific_map(p, True)),
    ("G10", "code_graphic_ww2_003_g10", ["S47", "S48", "S49"], "30,000-ft winter jet stream & 450-500 mph groundspeed drift diagram", render_g10_jet_stream),
    ("G11", "code_graphic_ww2_003_g11", ["S53", "S53a"], "High-altitude daylight vs LeMay 5,000-8,000 ft night profile comparison", lambda p: render_g11_tactical_or_losses(p, False)),
    ("G11l", "code_graphic_ww2_003_g11_losses", ["S62"], "Twentieth Air Force 414 B-29 losses breakdown (267 mechanical vs 147 enemy)", lambda p: render_g11_tactical_or_losses(p, True)),
    ("G12", "code_graphic_ww2_003_g12", ["S63"], "B-29 engineering lineage tree (B-50, C-97/KC-97, 377 Stratocruiser, Tu-4)", lambda p: render_g12_legacy(p, False)),
    ("G12c", "code_graphic_ww2_003_g12_cruise", ["S64"], "High-altitude pressurised cruise above storm weather", lambda p: render_g12_legacy(p, True)),
]


def encode_mp4(fn: Callable[[float], Image.Image], mp4_path: pathlib.Path) -> None:
    total_frames = int(round(FPS * DURATION_S))
    # Sample 36 distinct animation steps over first 3.5s, then hold final frame cleanly to 6.0s
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart",
        str(mp4_path),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    final_bytes: Optional[bytes] = None
    anim_frames = int(FPS * 3.5)
    for fi in range(total_frames):
        if fi < anim_frames:
            prog = (fi + 1) / float(anim_frames)
            frame_bytes = fn(prog).tobytes()
        else:
            if final_bytes is None:
                final_bytes = fn(1.0).tobytes()
            frame_bytes = final_bytes
        proc.stdin.write(frame_bytes)
    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg exited {rc} encoding {mp4_path}")


def build_all(out_dir: pathlib.Path, sheet_out: Optional[pathlib.Path] = None, skip_mp4: bool = False) -> List[Dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    records: List[Dict] = []
    thumbs: List[Tuple[str, Image.Image]] = []

    for idx, (gid, stem, shots, desc, fn) in enumerate(GRAPHICS_SPECS, 1):
        png_path = out_dir / f"{stem}.png"
        mp4_path = out_dir / f"{stem}.mp4"

        final_img = fn(1.0)
        final_img.save(png_path, format="PNG")
        if not skip_mp4:
            encode_mp4(fn, mp4_path)

        gray = np.asarray(final_img.convert("L"), dtype=np.float32)
        mean_luma = round(float(gray.mean()), 2)
        near_black_pct = round(float((gray < 28).mean() * 100.0), 2)

        rec = {
            "id": gid,
            "stem": stem,
            "shots": shots,
            "description": desc,
            "licence": "own (code-drawn in Python/Pillow + Natural Earth CC0 1:50m vectors, £0)",
            "png_filename": png_path.name,
            "png_dimensions": [W, H],
            "png_bytes": png_path.stat().st_size,
            "png_sha256": sha256_file(png_path),
            "mp4_filename": mp4_path.name if mp4_path.exists() else None,
            "mp4_duration_s": DURATION_S if mp4_path.exists() else None,
            "mp4_fps": FPS if mp4_path.exists() else None,
            "mp4_bytes": mp4_path.stat().st_size if mp4_path.exists() else None,
            "mp4_sha256": sha256_file(mp4_path) if mp4_path.exists() else None,
            "mean_luma": mean_luma,
            "near_black_pct": near_black_pct,
        }
        records.append(rec)
        thumbs.append((f"{gid} ({','.join(shots)})", final_img.resize((600, 338), Image.Resampling.LANCZOS)))
        print(
            f"[{idx:02d}/{len(GRAPHICS_SPECS):02d}] {gid:4s} -> {stem}.png/.mp4 "
            f"(luma={mean_luma}, near_black={near_black_pct}%, png_sha={rec['png_sha256'][:12]})"
        )

    if sheet_out and thumbs:
        cols = 3
        rows = math.ceil(len(thumbs) / cols)
        sheet = Image.new("RGB", (cols * 620 + 20, rows * 380 + 20), (16, 20, 26))
        sdraw = ImageDraw.Draw(sheet)
        for i, (lbl, th) in enumerate(thumbs):
            r, c = divmod(i, cols)
            x, y = 20 + c * 620, 20 + r * 380
            sheet.paste(th, (x, y + 28))
            sdraw.text((x, y + 2), lbl, font=font(FONT_MONO, 18), fill=SIGNAL_YELLOW)
        sheet_out.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(sheet_out, format="JPEG", quality=90)
        print(f"Wrote contact sheet: {sheet_out}")

    return records


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=pathlib.Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--manifest-json", type=pathlib.Path, default=None)
    ap.add_argument("--sheet-out", type=pathlib.Path, default=None)
    ap.add_argument("--skip-mp4", action="store_true")
    args = ap.parse_args()

    recs = build_all(args.out_dir, sheet_out=args.sheet_out, skip_mp4=args.skip_mp4)
    if args.manifest_json:
        args.manifest_json.parent.mkdir(parents=True, exist_ok=True)
        args.manifest_json.write_text(json.dumps(recs, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote manifest: {args.manifest_json} ({len(recs)} code-drawn maps/charts)")


if __name__ == "__main__":
    main()
