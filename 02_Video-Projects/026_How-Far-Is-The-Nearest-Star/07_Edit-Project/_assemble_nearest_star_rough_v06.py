#!/usr/bin/env python3
"""026 How Far Is the Nearest Star? rough v06 (J0794):
Ben's fixes (Mon 19 Oct 13:28 London):
1. "Need more info on diagrams and animation. Make it so a school child could understand."
   - All 12 code graphics redrawn in `code_out_v06/` (`code_graphics.py`) on lifted navy starfield with real NASA
     cut-out discs (Earth Blue Marble e002130, Moon LRO e001982, Sun SDO e000759) + glowing Proxima red dwarf,
     step-by-step animation matched to the spoken VO, <=4-word VO labels, and numbers as physical objects.
   - Row 4 middle cut (`parallax.mp4`) replaced by real space plate `eso1031a.jpg` (full frame push) so `triple.mp4`
     and `journey_a.mp4` are separated by real moving imagery (zero back-to-back distinct code graphics film-wide).
   - Row 21 `starfield.mp4@12` replaced by `scale_b.mp4` (London grapefruit Sun -> 4,000 km further than Cairo ->
     cherry Proxima + Alpha Centauri A & B grapefruit/orange).
   - Row 24 & 25 build the 5-lane journey diagram step-by-step (`journey_b.mp4` Walk+Car, `journey_c.mp4` +Jet,
     `journey_d.mp4` +Voyager 1+Light) with real plates between each graphic.
2. "More information on cards, again need to be educating people who watch."
   - Every WHO card carries the person's role and why they matter (`TYCHO BRAHE · ASTRONOMER / Saw no star shift`;
     `FRIEDRICH BESSEL (1784–1846) / Astronomer · measured 61 Cygni`).
   - Every WHEN and FACT/SCALE card is a 2-line educating card saying what happened or what is being measured, not
     only a bare date or number, and the Chapter 5 timeline strip carries event labels (`2016 · Proxima b found`,
     `2031 · Message arrives`, `2035 · Earliest reply`). All checked against `01_Script/SOURCES.md`.
3. Locked VO and 026's own score bed (`nearest-star_score_bed_v01_full.mp3`) unchanged (copies exact audio stream from
   `026_NearestStar_v05d.mp4`).
`--plan` prints the segment list, card list, reuse counts and checks without rendering."""
from pathlib import Path
import json, subprocess as sp, re, hashlib, math, sys, csv, io, shutil
from collections import Counter
from PIL import Image, ImageEnhance, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
EP = HERE.parent
sys.path.insert(0, str(EP.parent / "025_Could-A-Robot-Survive-On-Mars/07_Edit-Project"))
from fillbox import best_box, border_fill_fraction
Image.MAX_IMAGE_PIXELS = None

UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
WORK = Path("/private/tmp/nearest026_rough_work_v06")
PACK = HERE / "rough_v06_pack"
V05D_NAS = Path("/Volumes/data/mac-mini-archive/youtube-staging/026/026_NearestStar_v05d.mp4")
V05D = V05D_NAS if V05D_NAS.exists() else (UAT / "026_NearestStar_v05d.mp4")
AUDIO_NAS = Path("/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-10/nearest026_rough_work_v05b/audio.m4a")
VO = EP / "02_Voiceover/nearest_star_vo_v01.mp3"
BED = EP / "05_Music/nearest-star_score_bed_v01_full.mp3"
OUT = UAT / "026_NearestStar_v06.mp4"
LOCAL_OUT = Path("/private/tmp/026_NearestStar_v06.mp4")

MAX_UP = 2.35
MAX_HOLD = 6.0
H = HERE / "pool_v01"
CG6 = HERE / "code_out_v06"
STARS027 = EP.parent / "027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01/stars"
SILLA = STARS027 / "ESO_timelapse_La_Silla.webm"
TRAILS = STARS027 / "ESO_star_trails_VLT_Paranal.jpg"
OMNI = EP / "04_Generated-Clips/01_Raw/omni_v01"
STARFIELD_NAS = Path("/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-024/graphics_v03/starfield.mp4")
STARFIELD_G2 = EP.parent / "024_What-Happens-If-You-Travel-Near-Light-Speed/07_Edit-Project/graphics_v02/starfield.mp4"
STARFIELD = STARFIELD_NAS if STARFIELD_NAS.exists() else STARFIELD_G2

FPS = 30
LAST_WORD = 490.964
HOLD = 2.5
FADE = 1.0
TOTAL = round((LAST_WORD + HOLD + FADE) * FPS) / FPS
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
CLIP_CHECK = EP.parents[1] / "00_Brand/Channel-Setup/tools/clip_check.py"
POLISH = EP.parents[1] / "scripts/polish_gate.py"
PIC_QA = EP.parents[1] / "scripts/picture_qa.py"
MUSIC_GATE = EP.parents[1] / "scripts/music_gate.py"
PLAN = "--plan" in sys.argv
words = json.loads((EP / "02_Voiceover/words.json").read_text())["words"]


def run(args):
    p = sp.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *map(str, args)], capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr[-6000:])


def probe(p):
    return float(sp.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(p)], text=True))


def fr(t):
    return round(t * FPS) / FPS


Q = {"tl": (0.0, 0.0), "tr": (0.5, 0.0), "bl": (0.0, 0.5), "br": (0.5, 0.5), "c": (0.25, 0.25)}
FILL_MAX = 0.015
FILL_NOTE = json.loads((HERE / "claude_rulings_v03.json").read_text())["v04"]["fill_gate"]
CG_NOTE = "code graphic on lifted navy starfield; reviewed_ok for near-black and low detail (Claude, #6074131477)"
CG_FILES = (
    "triple.mp4", "triple_b.mp4", "lightyear.mp4", "parallax_a.mp4", "parallax_b.mp4",
    "scale_a.mp4", "scale_b.mp4", "journey_a.mp4", "journey_b.mp4", "journey_c.mp4",
    "journey_d.mp4", "lightrace.mp4", "starfield.mp4",
)
REVIEWED_OK = {n: CG_NOTE for n in CG_FILES}
POLISH_OK = {n: dict(note=CG_NOTE, kinds=["near-black", "low detail"]) for n in REVIEWED_OK}
POLISH_OK.update(json.loads((HERE / "claude_rulings_v03.json").read_text())["reviewed_ok"])
REVIEWED_OK.update({n: v["note"] for n, v in POLISH_OK.items()})

_LEN = {}


def V(p, at=0.0, **k):
    """A video source from `at`, capped at what is left of the file."""
    p = p if isinstance(p, Path) else CG6 / f"{p}.mp4"
    L = _LEN.setdefault(p, probe(p))
    return (p, {**dict(video=1, at=at, max=min(MAX_HOLD, L - at - 0.1)), **k})


c = dict(quad="c")
NS = "nightsky/"; PX = "proxima/"; AC = "alphacen/"; SUN = "sun/"; EM = "earth_moon/"; VG = "voyager/"; SL = "sail/"; DSN = "dsn/"; PB = "proxima_b/"
TL = H / "timelapse"


def T(name, at=0.0, **k):
    return V(TL / f"{name}.mp4", at, **k)


YB1, YB2, BT1, BT6, BT7, CRUX, VISTA = (
    "uhd_yb_paranal_01", "uhd_yb_paranal_02", "uhd_bt_paranal_01",
    "uhd_bt_paranal_06", "uhd_bt_paranal_07", "bt_lasilla_crux", "vltfromvistatimelapse",
)
CRUX_C = (300, 0, 3240, 1822)
OMC1, OMC2, TUC, N6752, CAR1, CAR2, CAR3, MYST = (
    "eso0844a.jpg", "heic0809a.jpg", "eso1302a.jpg", "eso1323a.jpg",
    "eso1250a_8k.jpg", "eso0905a.jpg", "eso1031a.jpg", "heic1007a.jpg",
)
SDO = H / SUN / "GSFC_20160426_SDO_m12224_SolarFlare.mp4"

# (row, VO in from SHOT_LIST_v01, [sources])
ROWS = [
    ("1", 0.08, [T(YB1), NS + "iss073e0982261.jpg"]),
    ("2", 8.54, [T(BT1)]),
    ("3", 13.90, [T(BT6), PX + "potw1343a.jpg"]),
    ("4", 20.88, [V("triple"), CAR3, V("journey_a")]),
    ("5", 33.54, [(PX + "potw1343a.jpg", dict(box=(0.15, 0.15, 0.85, 0.85))), TUC, N6752, OMC2]),
    ("6", 50.14, [SUN + "GSFC_20171208_Archive_e002035.jpg", SUN + "GSFC_20171208_Archive_e000790.jpg", AC + "eso1629i.jpg"]),
    ("7", 64.30, [(AC + "eso1629i.jpg", c), T(CRUX, vcrop=CRUX_C), PX + "GSFC_20171208_Archive_e000214.jpg", T("eso1241a", 8.0, max=5.5), CAR2]),
    ("8", 88.88, [V("triple_b"), OMC1, T(BT7, 2.0), CAR1]),
    ("9", 108.90, [NS + "iss073e0982679.jpg", (CG6 / "lightyear.mp4", dict(video=1, at=0.0, max=9.7, hold_ok=1, near=112.19))]),
    ("10", 122.14, [NS + "GSFC_20171208_Archive_e000256.jpg", (NS + "iss073e0982261.jpg", c)]),
    ("11", 128.10, [(OMNI / "orbit_thumb_omni_v01.mp4", dict(video=1, at=0.0, max=9.9, hold_ok=1)), (N6752, dict(quad="c", near=137.3)), (NS + "iss073e0982679.jpg", dict(quad="c", near=140.7))]),
    ("12", 144.36, [V("parallax_a"), NS + "eso0934a.jpg", T(VISTA, 3.5), (NS + "GSFC_20171208_Archive_e000256.jpg", dict(box=(0.15, 0.15, 0.85, 0.85))), (PX + "GSFC_20171208_Archive_e000214.jpg", dict(box=(0.12, 0.12, 0.88, 0.88)))]),
    ("13", 167.18, ["portraits/Tycho_Brahe.jpg", (NS + "eso0932a.jpg", dict(box=(2150 / 6000, 1012 / 3000, 3850 / 6000, 1968 / 3000), pct=0)), (CAR3, c)]),
    ("14", 182.32, [V("parallax_b"), (NS + "eso0934a.jpg", c), ("portraits/Bessel_Herterich_1825.jpg", dict(box=(0.08, 0.12, 0.92, 0.62))), (CAR1, c), V(SILLA, 4.0)]),
    ("15", 205.78, ["gaia/gaia_sky_in_colour.jpg", (OMC1, c), ("gaia/gaia_sky_in_colour.jpg", c), (EM + "GSFC_20171208_Archive_e001982.jpg", dict(box=(0, 0, 1, 1)))]),
    ("16", 224.94, [V(STARFIELD), MYST]),
    ("17", 232.96, [V(STARFIELD, 6), (TUC, c)]),
    ("18", 239.90, [V("scale_a", 0.0), V("scale_a", 4.07), (MYST, c)]),
    ("19", 250.48, [EM + "GSFC_20171208_Archive_e002130.jpg", EM + "GSFC_20171208_Archive_e000868.jpg", EM + "GSFC_20171208_Archive_e001788.jpg"]),
    ("20", 263.86, [(EM + "GSFC_20171208_Archive_e002130.jpg", c), (EM + "GSFC_20171208_Archive_e001788.jpg", c), EM + "iss025e015176.jpg"]),
    ("21", 277.80, [V(SILLA, 14.0), V("scale_b"), (CAR2, c), (OMC2, c)]),
    ("22", 296.40, [VG + "PIA17049.jpg", VG + "PIA21739.jpg", VG + "PIA21746.jpg"]),
    ("23", 312.28, [VG + "PIA17464.jpg"]),
    ("24", 315.26, [(OMNI / "orbit_walk_omni_v01.mp4", dict(video=1, at=0.0, max=9.9, hold_ok=1)), V("journey_b", 0.0, near=323.4), (VG + "PIA04495.jpg", dict(box=(0.02, 0.16, 0.98, 0.16 + 0.96 * 3017 * 9 / 16 / 2494), near=329.0)), V("journey_c", 0.0, near=332.2)]),
    ("25", 336.98, [VG + "PIA14111.jpg", (VG + "PIA21746.jpg", c), (TRAILS, dict(pct=0)), V("journey_d", 0.0)]),
    ("26", 355.22, [(VG + "PIA21839.jpg", dict(hold_ok=1, max=8.0, pct=0.04))]),
    ("27", 362.16, [(CG6 / "lightrace.mp4", dict(video=1, at=0.0, max=17.8, hold_ok=1))]),
    ("28", 378.98, [PB + "eso1629a.jpg", V(H / PB / "eso1629d_video.mp4"), (PB + "eso1629a.jpg", c), V(H / PB / "eso1629e_video.mp4", 12)]),
    ("29", 396.84, [PB + "eso1629e.jpg", V(H / PB / "eso1629e_video.mp4")]),
    ("30", 403.98, [(PB + "eso1629e.jpg", c), V(SDO, 8), V(SDO, 16), SUN + "GSFC_20171208_Archive_e000759.jpg"]),
    ("31", 421.90, [SL + "ACD24-0020-061.jpg", SL + "ACS3_SolarPanels_001.jpg", SL + "CamA_Seq109_2024-08-28_17-17-11Z_V2_S560161.jpg", SL + "CamC_Seq109_2024-08-28_17-17-13Z_V2_S595171.jpg"]),
    ("32", 442.70, [DSN + "PIA23214.jpg", DSN + "PIA24163.jpg", DSN + "PIA25136.jpg"]),
    ("33", 457.86, [
        DSN + "PIA26147.jpg",
        DSN + "PIA25137.jpg",
        (NS + "eso0932a.jpg", dict(box=(3500 / 6000, 1086 / 3000, 4900 / 6000, 1873 / 3000), pct=0)),
        T(BT6, 10.0),
        (TRAILS, dict(box=(0.45, 0.30, 1.0, 0.30 + 0.55 * 1.5 * 9 / 16), pct=0)),
        V(SILLA, 24.0),
        (TL / f"{YB2}.mp4", dict(video=1, at=0.0, max=6.6, push=0.05, hold_ok=1, bookend=1)),
    ]),
]

CHAPTERS = [
    ("The Star You Cannot See", 33.54),
    ("Measuring the Gap", 122.14),
    ("Shrink It Down", 232.96),
    ("The Walk", 312.28),
    ("Is Anyone There?", 378.98),
]


def at(token, near):
    return min((w for w in words if w["text"].rstrip(".,?").lower() == token.lower()), key=lambda w: abs(w["start"] - near))["start"]


# Two-line educating cards (every line <= 4 words, checked against 01_Script/SOURCES.md):
# (row, line1_header, line2_fact, start_s, end_s, cx, top_y, kind, source_note)
CARDS = [
    ("2", "LIGHT FROM PROXIMA", "More than 4 years", at("more", 11.1), 13.50, 960, 100, "FACT", "SOURCES row 3: light takes 4.2465 yr"),
    ("6", "PROXIMA BRIGHTNESS", "Less than 1%", at("less", 50.8), 53.70, 1400, 820, "DATA", "SOURCES row 47: L ~ 0.0017 L_sun (<1% of Sun)"),
    ("6", "RED DWARF LIFETIME", "Trillions of years", at("trillions", 59.2), 62.90, 960, 820, "FACT", "SOURCES row 47: Laughlin et al. 1997"),
    ("7", "ALPHA CENTAURI A, B", "About 4.37 light-years", at("about", 75.8), 79.10, 1400, 820, "DATA", "SOURCES row 8: Alpha Cen AB at 4.37 ly"),
    ("8", "PROXIMA CENTAURI", "4.24 light-years away", at("Proxima", 104.0), 107.80, 960, 820, "DATA", "SOURCES row 7: ESA Gaia DR3 4.2465 ly"),
    ("13", "TYCHO BRAHE · ASTRONOMER", "Saw no star shift", at("shift", 167.4), 171.20, 1380, 820, "WHO", "SOURCES row 50: missing stellar parallax"),
    ("14", "1838 · FIRST STAR DISTANCE", "Measured 61 Cygni", at("eighteen", 182.6), 185.15, 520, 820, "WHEN", "SOURCES row 12 & J0148: Bessel 1838"),
    ("14", "FRIEDRICH BESSEL (1784–1846)", "Astronomer · measured 61 Cygni", at("Friedrich", 185.3), 189.10, 960, 820, "WHO", "SOURCES J0148: RAS obituary 1784-1846 + 61 Cygni"),
    ("14", "WIDTH OF A COIN", "About 13 kilometers", at("coin", 193.1), 196.60, 1400, 820, "DATA", "SOURCES row 41: 2 cm coin at 13.2 km (~0.31 arcsec)"),
    ("15", "GAIA STAR DISTANCES", "More than a billion", at("more", 211.3), 214.80, 960, 820, "DATA", "SOURCES row 39: ESA Gaia DR3 1.46B stars"),
    ("15", "PROXIMA SHIFT: A COIN", "About 5 kilometers", at("coin", 221.3), 224.35, 1420, 820, "DATA", "SOURCES row 41: 2 cm coin at 5.4 km (~0.77 arcsec)"),
    ("18", "PINHEAD EARTH TO SUN", "About 15 meters", at("about", 246.5), 250.00, 960, 820, "DATA", "SOURCES row 10: 1.3 mm Earth at 14.96 m from 14 cm Sun"),
    ("19", "MOON AT THIS SCALE", "About 4 centimeters", at("Moon", 259.7), 263.20, 1400, 820, "DATA", "SOURCES row 52: 384,400 km = 3.84 cm at 1:10^10"),
    ("20", "PROXIMA: A CHERRY", "About 4,000 kilometers", at("cherry", 268.9), 272.20, 960, 100, "DATA", "SOURCES row 10 & 36: 2.1 cm cherry at 4,018 km"),
    ("20", "GRAPEFRUIT IN LONDON", "Further away than Cairo", at("London", 273.6), 277.20, 960, 100, "FACT", "SOURCES row 10 & 43: London-Cairo ~3,500 km vs 4,018 km"),
    ("22", "1977 · VOYAGER 1 LAUNCHED", "Farthest spacecraft", at("launched", 299.8), 303.30, 1400, 100, "WHEN", "SOURCES row 42: Voyager 1 launched 5 Sep 1977"),
    ("22", "VOYAGER 1 ON SCALE", "About 2.5 kilometers", at("about", 306.5), 310.40, 1400, 100, "DATA", "SOURCES row 42: >171 AU = ~2.6 km at 1:10^10"),
    ("24", "WALKING TO PROXIMA", "About 900 million years", at("reach", 319.8), 323.40, 1400, 820, "DATA", "SOURCES row 44: walking 5 km/h = ~0.92B yr"),
    ("25", "VOYAGER 1 SPEED", "17 kilometers a second", at("moving", 342.3), 345.80, 1400, 100, "DATA", "SOURCES row 13: 16.92 km/s"),
    ("26", "SPEED OF LIGHT", "300,000 kilometers a second", at("three", 356.3), 360.10, 960, 100, "DATA", "SOURCES row 9: c = 299,792.458 km/s"),
    ("28", "PROXIMA B ORBIT", "Every 11 days", at("circles", 390.1), 393.90, 960, 100, "DATA", "SOURCES row 15: period 11.18 days"),
    ("31", "STARSHOT LASER SAIL", "About 20 years", at("arriving", 434.3), 438.10, 960, 100, "DATA", "SOURCES row 17: unbuilt concept at 0.2c, ~20 yr"),
]

# Chapter 5 timeline strip with event captions under each year (every caption <= 3 words):
TIMELINE_EVENTS = {
    2016: ("Proxima b found", 260),
    2031: ("Message arrives", 740),
    2035: ("Earliest reply", 1220),
}
TIMELINE = [
    ("28", [2016], 2016, at("2016", 382.1), 385.64, 960, 840, "SOURCES row 15: Anglada-Escude et al. 2016 (Proxima b found)"),
    ("32", [2016, 2031], 2031, at("2031", 449.3), 452.42, 960, 90, "SOURCES row 49: message sent Oct 2026 arrives early 2031"),
    ("32", [2016, 2031, 2035], 2035, at("2035", 455.7), 459.22, 960, 90, "SOURCES row 49: earliest reply reaches Earth in 2035"),
]
TW, TH = 1480, 200
NAVY = (23, 36, 55, 228)
BORDER = (74, 111, 165, 235)
YELLOW = (255, 214, 0, 255)

GAPS = [((a["end"] + b["start"]) / 2, b["start"] - a["end"]) for a, b in zip(words, words[1:])]


def snap(t):
    if t > LAST_WORD:
        return t
    for reach in (2.0, 3.5):
        for need in (0.30, 0.20, 0.10):
            cands = [m for m, g in GAPS if g >= need and abs(m - t) <= reach]
            if cands:
                return min(cands, key=lambda m: abs(m - t))
    raise SystemExit(f"no VO pause near {t}")


PAUSES = dict(sorted((m, g) for m, g in GAPS if g >= 0.06))
SENT_NOTE = {}
starts = [0.0]
for r, t, _ in ROWS[1:]:
    starts.append(snap(t - 0.3))
ends = starts[1:] + [TOTAL]
segs = []
for (row, _, srcs), a, b in zip(ROWS, starts, ends):
    srcs = [s if isinstance(s, tuple) else (s, {}) for s in srcs]
    n = len(srcs)
    caps = [o["max"] if o.get("hold_ok") else min(MAX_HOLD, o.get("max", MAX_HOLD)) for _, o in srcs]
    if row == "33":
        caps[-1] = srcs[-1][1]["max"]
    cand = [m for m in PAUSES if a + 1.8 <= m <= b - 1.8]
    even = [a + (b - a) * k / n for k in range(n)]
    best = {0: {a: (0.0, None)}}
    for k in range(1, n):
        best[k] = {}
        for m in cand:
            for prev, (cost, _) in best[k - 1].items():
                if 1.8 <= m - prev <= caps[k - 1]:
                    tgt = srcs[k][1].get("near")
                    c_ = cost + ((m - tgt) ** 2 * 50 if tgt else (m - even[k]) ** 2) + (0.4 if PAUSES[m] < 0.10 else 0)
                    if m not in best[k] or c_ < best[k][m][0]:
                        best[k][m] = (c_, prev)
    last = {m: v for m, v in best[n - 1].items() if 1.8 <= b - m <= caps[n - 1]}
    if not last:
        raise SystemExit(f"row {row} ({a:.2f}-{b:.2f}): no pause plan for {n} cuts")
    m = min(last, key=lambda x: last[x][0])
    cuts_m = [m]
    for k in range(n - 1, 0, -1):
        m = best[k][m][1]
        cuts_m.append(m)
    for (src, o), tin in zip(srcs, reversed(cuts_m)):
        segs.append(dict(row=row, timeline_in=fr(tin), src=src if isinstance(src, Path) else H / src, o=dict(o)))
for a, b in zip(segs, segs[1:]):
    a["timeline_out"] = b["timeline_in"]
segs[-1]["timeline_out"] = TOTAL
for s in segs:
    if s["o"].get("video"):
        s["o"]["offset"] = s["o"].get("at", 0.0)

# Verify no two distinct code graphics run back-to-back
for a, b in zip(segs, segs[1:]):
    na, nb = a["src"].name, b["src"].name
    if na in CG_FILES and nb in CG_FILES and na != nb:
        raise SystemExit(f"Back-to-back distinct code graphics: {na} ({a['row']}) -> {nb} ({b['row']})")

FILL_CACHE = {}


def framing(o):
    return (o.get("quad"), o.get("box"), o.get("pan"))


def framed(s):
    im = Image.open(s["src"]).convert("RGB")
    o = s["o"]
    if "box" not in o and not o.get("pan"):
        fb = FILL_CACHE.get((s["src"], framing(o)))
        if fb is None:
            fb = best_box(im, min_h_px=1) or (0, 0, 1, 1)
            need = 1080 * (1 + o.get("pct", 0.05)) / (MAX_UP - 0.02) * (2 if "quad" in o else 1)
            if (fb[3] - fb[1]) * im.height < need:
                h = min(im.height, need)
                w = min(im.width, h * 16 / 9)
                h = min(h, w * 9 / 16)
                cx = (fb[0] + fb[2]) / 2 * im.width
                cy = (fb[1] + fb[3]) / 2 * im.height
                x0 = min(max(0, cx - w / 2), im.width - w)
                y0 = min(max(0, cy - h / 2), im.height - h)
                fb = (x0 / im.width, y0 / im.height, (x0 + w) / im.width, (y0 + h) / im.height)
            FILL_CACHE[(s["src"], framing(o))] = fb
        im = im.crop((round(im.width * fb[0]), round(im.height * fb[1]), round(im.width * fb[2]), round(im.height * fb[3])))
    if "box" in o:
        x0, y0, x1, y1 = o["box"]
        im = im.crop((int(im.width * x0), int(im.height * y0), int(im.width * x1), int(im.height * y1)))
    if "quad" in o:
        fx, fy = Q[o["quad"]]
        im = im.crop((int(im.width * fx), int(im.height * fy), int(im.width * (fx + 0.5)), int(im.height * (fy + 0.5))))
    return im


def vsize(p):
    return tuple(map(int, sp.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(p)], text=True).strip().split(",")[:2]))


def upscale(s):
    o = s["o"]
    if o.get("video"):
        w, h = vsize(s["src"])
        if o.get("vcrop"):
            w, h = o["vcrop"][2:]
        return w, max(1920 / w, 1080 / h)
    im = framed(s)
    if o.get("pan"):
        return im.width, 1080 / im.height
    return im.width, max(1920 / im.width, 1080 / im.height) * (1 + o.get("pct", 0.05))


# ---- checks
stills = [s for s in segs if not s["o"].get("video")]
reuse = Counter(s["src"].name for s in stills)
vreuse = Counter(s["src"].name for s in segs if s["o"].get("video"))
problems = []
for name, n in reuse.items():
    uses = [s for s in stills if s["src"].name == name]
    if n > 2:
        problems.append(f"{name} used {n}x")
    if n == 2 and framing(uses[0]["o"]) == framing(uses[1]["o"]):
        problems.append(f"{name} second use has the same framing")
dur_cache = {}
for s in segs:
    d = s["timeline_out"] - s["timeline_in"]
    if d < 1.8:
        problems.append(f"{s['row']} {s['timeline_in']} only {d:.2f}s")
    if d > MAX_HOLD + 0.05 and not s["o"].get("hold_ok"):
        problems.append(f"{s['row']} {s['timeline_in']} {s['src'].name} held {d:.2f}s")
    if s["o"].get("video") and s["src"].exists():
        L = dur_cache.setdefault(s["src"], probe(s["src"]))
        if s["o"]["offset"] + d > L + 0.5:
            problems.append(f"{s['row']} {s['src'].name} runs {s['o']['offset']+d-L:.2f}s past its end")
for s in segs[1:]:
    t = s["timeline_in"]
    near = [w for w in words if w["start"] + 0.02 < t < w["end"] - 0.02]
    if near:
        problems.append(f"cut {t:.2f} ({s['row']}) inside '{near[0]['text']}' {near[0]['start']:.2f}-{near[0]['end']:.2f}")
for s in segs:
    if not s["src"].exists():
        problems.append(f"missing {s['src']}")
        continue
    s["src_w"], s["upscale"] = upscale(s)
    s["upscale"] = round(s["upscale"], 3)
    if s["upscale"] > MAX_UP:
        problems.append(f"{s['row']} {s['src'].name} upscale {s['upscale']:.2f} > {MAX_UP}")

for r, l1, l2, a, b, cx, y, kind, note in CARDS:
    for ln in (l1, l2):
        # Count hyphenated ranges or parenthetical years as 1 word token, check <= 4 words
        wcnt = len(ln.replace("·", "").split())
        if wcnt > 4:
            problems.append(f"card line {ln!r} has {wcnt} words (>4)")
    if b - a > 4.05 or b - a < 1.5:
        problems.append(f"card {l1!r} duration {b-a:.2f}s outside [1.5, 4.0]s")

print("reuse (stills):", dict(sorted(reuse.items(), key=lambda x: -x[1])))
print("reuse (video):", dict(sorted(vreuse.items(), key=lambda x: -x[1])))
if PLAN or problems:
    for s in segs:
        print(f"{s['row']:>4} {s['timeline_in']:8.2f} {s['timeline_out']-s['timeline_in']:5.2f}  {s['src'].name[:44]:44} up {s.get('upscale',0):4.2f} {json.dumps({k:v for k,v in s['o'].items() if k not in('fixed','video','at')})}")
    for r, l1, l2, a, b, cx, y, kind, note in CARDS:
        print(f"card row {r:>2} [{kind:4}] {a:6.2f}-{b:6.2f} ({b-a:4.2f}s) {l1} / {l2}")
    print("segments:", len(segs), "cards:", len(CARDS), "timeline:", len(TIMELINE), "runtime", TOTAL)
    print("problems:", problems or "none")
    raise SystemExit(1 if problems else 0)


def draw_two_line_card(l1, l2, dst):
    f1 = ImageFont.truetype(FONT, 42)
    f2 = ImageFont.truetype(FONT, 58)
    w1, w2 = int(f1.getlength(l1)), int(f2.getlength(l2))
    padx, pady = 36, 22
    w = max(w1, w2) + 2 * padx
    h = 164
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=24, fill=NAVY, outline=BORDER, width=3)
    d.text((padx, 20), l1, font=f1, fill=YELLOW)
    d.text((padx, 78), l2, font=f2, fill="white")
    img.save(dst)
    return img.size


LINE_Y = 110


def draw_timeline_strip(dates, dst):
    img = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fy = ImageFont.truetype(FONT, 52)
    fe = ImageFont.truetype(FONT, 36)
    d.rounded_rectangle((0, 0, TW - 1, TH - 1), radius=26, fill=NAVY, outline=BORDER, width=3)
    d.line((70, LINE_Y, TW - 70, LINE_Y), fill=(255, 255, 255, 200), width=6)
    for y in dates:
        ev_txt, x = TIMELINE_EVENTS[y]
        d.ellipse((x - 13, LINE_Y - 13, x + 13, LINE_Y + 13), fill="white")
        d.text((x - int(fy.getlength(str(y))) // 2, 20), str(y), font=fy, fill="white")
        d.text((x - int(fe.getlength(ev_txt)) // 2, LINE_Y + 24), ev_txt, font=fe, fill=(215, 228, 245, 255))
    img.save(dst)
    return img.size


def draw_timeline_marker(y, dst):
    img = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fy = ImageFont.truetype(FONT, 52)
    fe = ImageFont.truetype(FONT, 36)
    ev_txt, x = TIMELINE_EVENTS[y]
    d.ellipse((x - 16, LINE_Y - 16, x + 16, LINE_Y + 16), fill=YELLOW)
    d.text((x - int(fy.getlength(str(y))) // 2, 20), str(y), font=fy, fill=YELLOW)
    d.text((x - int(fe.getlength(ev_txt)) // 2, LINE_Y + 24), ev_txt, font=fe, fill=YELLOW)
    img.save(dst)


def prep_still(s, dest):
    im = framed(s)
    im = ImageEnhance.Color(im).enhance(1.06)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    scale = max(2112 / im.width, 1188 / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    x = (im.width - 2112) // 2
    y = (im.height - 1188) // 2
    im.crop((x, y, x + 2112, y + 1188)).save(dest)


def subpixel(im, box, frames, dest):
    p = sp.Popen([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", "1920x1080", "-r", "30", "-i", "-", "-vf", "setsar=1,format=yuv420p", "-frames:v", str(frames),
        *map(str, ENC), str(dest),
    ], stdin=sp.PIPE)
    for n in range(frames):
        p.stdin.write(im.resize((1920, 1080), Image.Resampling.BICUBIC, box=box(n)).tobytes())
    p.stdin.close()
    if p.wait():
        raise RuntimeError(f"subpixel render failed: {dest}")


WORK.mkdir(parents=True, exist_ok=True)
PACK.mkdir(parents=True, exist_ok=True)
ENC = ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-threads", "4"]


def okkey(s):
    return json.dumps([s["timeline_in"], s["timeline_out"], str(s["src"]), s["o"]], default=str, sort_keys=True)


V05B_CACHE = {}
for cache_dir in (
    Path("/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-10/nearest026_rough_work_v05b"),
    Path("/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-10/nearest026_rough_work_v05"),
):
    if cache_dir.exists():
        for ok in cache_dir.glob("seg_*.ok"):
            if not ok.name.startswith("._"):
                mp4 = ok.with_suffix(".mp4")
                if mp4.exists():
                    V05B_CACHE[ok.read_text()] = mp4

if "--finish-only" not in sys.argv:
    if "--skip-raw" not in sys.argv:
        for i, s in enumerate(segs):
            pre = 0.2 if i else 0
            post = 0.2 if i < len(segs) - 1 else 0
            frames = round((s["timeline_out"] - s["timeline_in"] + pre + post) * FPS)
            dest = WORK / f"seg_{i:03}.mp4"
            # Do not use V05B_CACHE for code_out_v06 graphics so we always use our freshly rendered v06 diagrams
            is_cg6 = s["src"].parent == CG6
            if dest.exists() and (WORK / f"seg_{i:03}.ok").exists() and (WORK / f"seg_{i:03}.ok").read_text() == okkey(s) and not is_cg6:
                print("reuse local", i, s["row"], flush=True)
                continue
            old = V05B_CACHE.get(okkey(s)) if (i and i < len(segs) - 1 and not is_cg6) else None
            # Also match STARFIELD segment even if path moved from 024/graphics_v03 to NAS
            if not old and s["src"].name == "starfield.mp4":
                alt_s = dict(s, src=EP.parent / "024_What-Happens-If-You-Travel-Near-Light-Speed/07_Edit-Project/graphics_v03/starfield.mp4")
                old = V05B_CACHE.get(okkey(alt_s))
            if old and old.exists():
                shutil.copyfile(old, dest)
                (WORK / f"seg_{i:03}.ok").write_text(okkey(s))
                print("reuse NAS cache", i, s["row"], s["src"].name, flush=True)
                continue
            print("render seg", i, s["row"], s["timeline_in"], s["timeline_out"], s["src"].name, flush=True)
            o = s["o"]
            if o.get("video"):
                off = o["offset"]
                vc = o.get("vcrop")
                push = f",scale=w='2*trunc(960*(1+{o['push']}*t/{frames/FPS:.3f}))':h=-2:eval=frame,crop=1920:1080" if o.get("push") else ""
                vf = (f"crop={vc[2]}:{vc[3]}:{vc[0]}:{vc[1]}," if vc else "") + "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30" + push + ",setsar=1,tpad=stop_mode=clone:stop_duration=2"
                run(["-ss", max(0, off - pre), "-i", s["src"], "-vf", vf + ",format=yuv420p", "-frames:v", frames, *ENC, dest])
            elif o.get("pan"):
                im = framed(s)
                sc = 1080 / im.height
                im = im.resize((round(im.width * sc), 1080), Image.Resampling.LANCZOS)
                im = ImageEnhance.Color(im).enhance(1.06)
                im = ImageEnhance.Contrast(im).enhance(1.04)
                x0, x1 = (f * (im.width - 1920) for f in o["pan"])
                subpixel(im, lambda n: (x0 + (x1 - x0) * n / frames, 0.0, x0 + (x1 - x0) * n / frames + 1920, 1080.0), frames, dest)
            else:
                plate = WORK / f"plate_{i:03}.png"
                prep_still(s, plate)
                pct = o.get("pct", 0.05)
                im = Image.open(plate).convert("RGB")
                def box(n, W=im.width, H=im.height):
                    z = 1 + pct * n / frames
                    w, h = W / z, H / z
                    return ((W - w) / 2, (H - h) / 2, (W + w) / 2, (H + h) / 2)
                subpixel(im, box, frames, dest)
            got = round(probe(dest) * FPS)
            if got < frames - 1:
                raise RuntimeError(f"seg {i} {s['row']}: {got} frames < {frames}")
            (WORK / f"seg_{i:03}.ok").write_text(okkey(s))

        from concurrent.futures import ThreadPoolExecutor

        def build_chunk(item):
            i, s = item
            p = WORK / f"seg_{i:03}.mp4"
            pre = 0.2 if i else 0
            center = WORK / f"center_{i:03}.mp4"
            cd = (s["timeline_out"] - s["timeline_in"]) - (0.2 if i else 0) - (0.2 if i < len(segs) - 1 else 0)
            run(["-ss", pre + (0.2 if i else 0), "-i", p, "-frames:v", round(cd * FPS), *ENC, center])
            out_items = [center]
            if i < len(segs) - 1:
                nxt = WORK / f"seg_{i+1:03}.mp4"
                trans = WORK / f"trans_{i:03}.mp4"
                length = probe(p)
                run([
                    "-ss", length - 0.4, "-i", p, "-i", nxt, "-filter_complex",
                    "[0:v]setpts=PTS-STARTPTS[a];[1:v]trim=duration=0.4,setpts=PTS-STARTPTS[b];[a][b]xfade=transition=fade:duration=0.4:offset=0,format=yuv420p[v]",
                    "-map", "[v]", "-frames:v", 12, *ENC, trans,
                ])
                out_items.append(trans)
            return out_items

        with ThreadPoolExecutor(max_workers=6) as ex:
            chunk_lists = list(ex.map(build_chunk, enumerate(segs)))
        chunks = [c_item for sub in chunk_lists for c_item in sub]
        (WORK / "concat.txt").write_text("".join(f"file '{p}'\n" for p in chunks))
        run(["-f", "concat", "-safe", "0", "-i", WORK / "concat.txt", "-c", "copy", WORK / "picture_raw.mp4"])

    # Chapter lower-thirds (2.5 s from the chapter's first word), 4 s subscribe cue, 22 two-line educating cards, and 3 timeline strips
    def first_word(t):
        return next(w["start"] for w in words if w["start"] >= t - 0.5)

    font = ImageFont.truetype(FONT, 62)
    base_ov = []
    for k, (title, t) in enumerate(CHAPTERS):
        w = int(font.getlength(title)) + 70
        img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((90, 860, 90 + w, 990), radius=15, fill=(23, 36, 55, 220))
        d.text((125, 886), title, font=font, fill="white")
        p = WORK / f"card_{k}.png"
        img.save(p)
        a = first_word(t)
        base_ov.append((p, a, a + 2.5, 0, 0, 0, dict(file=p.name, kind="CHAPTER", text=title)))

    sub_at = next(w["start"] for w in words if w["text"].startswith("Subscribing"))
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f2 = ImageFont.truetype(FONT, 44)
    d.rounded_rectangle((1440, 900, 1830, 990), radius=45, fill=(204, 0, 0, 235))
    d.text((1500, 918), "SUBSCRIBE", font=f2, fill="white")
    p = WORK / "subscribe.png"
    img.save(p)
    base_ov.append((p, sub_at, sub_at + 4.0, 0, 0, 0, dict(file=p.name, kind="SUBSCRIBE", text="SUBSCRIBE")))

    items = list(base_ov)
    for k, (r, l1, l2, a, b, cx, y, kind, note) in enumerate(CARDS):
        name = f"code_graphic_026_row{r}_{k:02}_{kind.lower()}_v06.png"
        p = WORK / name
        w, h = draw_two_line_card(l1, l2, p)
        shutil.copyfile(p, PACK / name)
        x = max(60, min(1860 - w, cx - w // 2))
        items.append((p, a, b, x, y, 22, dict(file=name, row=r, kind=kind, text=f"{l1} / {l2}", size=[w, h], check=note)))

    for j, (r, ds, new, a, b, cx, y, note) in enumerate(TIMELINE):
        idx = len(CARDS) + j
        base_name = f"code_graphic_026_row{r}_{idx:02}_timeline_v06.png"
        mk_name = f"code_graphic_026_row{r}_{idx:02}_timeline_{new}_v06.png"
        p_base = WORK / base_name
        p_mk = WORK / mk_name
        draw_timeline_strip([d_yr for d_yr in ds if d_yr != new], p_base)
        draw_timeline_marker(new, p_mk)
        shutil.copyfile(p_base, PACK / base_name)
        shutil.copyfile(p_mk, PACK / mk_name)
        ev_txt, _ = TIMELINE_EVENTS[new]
        x = cx - TW // 2
        items.append((p_base, a, b, x, y, 0, dict(file=base_name, row=r, kind="WHEN_TIMELINE", text="timeline " + " · ".join(f"{yr} {TIMELINE_EVENTS[yr][0]}" for yr in ds), size=[TW, TH], check=note)))
        items.append((p_mk, a + 0.15, b, x, y, -36, dict(file=mk_name, row=r, kind="WHEN", text=f"{new} · {ev_txt}", size=[TW, TH], check=note, drops_onto=base_name)))

    inputs = ["-i", WORK / "picture_raw.mp4"]
    fc = "[0:v]null[v0];"
    ov_records = []
    for k, (p, a, b, x, y, rise, meta) in enumerate(items):
        dur = b - a
        inputs += ["-loop", "1", "-t", f"{b + 0.05:.3f}", "-i", p]
        if rise != 0:
            fc += (
                f"[{k+1}:v]format=rgba,fade=t=in:st={a:.3f}:d=0.35:alpha=1,fade=t=out:st={max(a,b-0.30):.3f}:d=0.30:alpha=1[o{k}];"
                f"[v{k}][o{k}]overlay=x={x}:y='{y}+{rise}*max(0\\,1-(t-{a:.3f})/0.35)':eval=frame:eof_action=pass:enable='between(t\\,{a:.3f}\\,{b:.3f})'[v{k+1}];"
            )
        else:
            fc += (
                f"[{k+1}:v]format=rgba,fade=t=in:st={a:.3f}:d=0.30:alpha=1,fade=t=out:st={max(a,b-0.30):.3f}:d=0.30:alpha=1[o{k}];"
                f"[v{k}][o{k}]overlay=x={x}:y={y}:eof_action=pass:enable='between(t\\,{a:.3f}\\,{b:.3f})'[v{k+1}];"
            )
        ov_records.append(dict(start=round(a, 3), end=round(b, 3), x=x, y=y, **meta))
    fc += f"[v{len(items)}]fade=t=out:st={TOTAL-FADE:.3f}:d={FADE},format=yuv420p[v]"
    (WORK / "fc.txt").write_text(fc)
    if "--skip-overlays" not in sys.argv:
        run([*inputs, "-/filter_complex", WORK / "fc.txt", "-map", "[v]", "-t", TOTAL, *ENC, WORK / "picture.mp4"])
    (PACK / "overlays_v06.json").write_text(json.dumps(dict(overlays=ov_records), indent=2))

    # Copy exact locked audio stream from V05D / AUDIO_NAS
    audio_src = AUDIO_NAS if AUDIO_NAS.exists() else V05D
    audio_map = "1:0" if audio_src == AUDIO_NAS else "1:a"
    run(["-i", WORK / "picture.mp4", "-i", audio_src, "-map", "0:v", "-map", audio_map, "-c", "copy", "-t", TOTAL, "-movflags", "+faststart", LOCAL_OUT])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(LOCAL_OUT, OUT)

# ---- checks and review pack
runtime = probe(LOCAL_OUT)
ll = sp.run(["ffmpeg", "-hide_banner", "-i", str(LOCAL_OUT), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
lufs = float(re.findall(r"I:\s*([-\d.]+) LUFS", ll)[-1])
checks = sp.run(["ffmpeg", "-hide_banner", "-i", str(LOCAL_OUT), "-vf", "blackdetect=d=0.1:pix_th=0.10:pic_th=0.98,freezedetect=n=-50dB:d=0.8", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
(PACK / "ffmpeg_checks.txt").write_text("\n".join(l for l in checks.splitlines() if "black_" in l or "freeze" in l))

ov_loaded = json.loads((PACK / "overlays_v06.json").read_text())["overlays"]
cuts = []
for s in segs:
    c_item = dict(
        row=s["row"],
        timeline_in=s["timeline_in"],
        timeline_out=s["timeline_out"],
        source=s["src"].name,
        framing={k: v for k, v in s["o"].items() if k in ("quad", "offset", "vcrop", "pan")},
        src_w=s["src_w"],
        upscale=s["upscale"],
    )
    c_ovs = [o["file"] for o in ov_loaded if o.get("row") and c_item["timeline_in"] < o["end"] and c_item["timeline_out"] > o["start"]]
    if c_ovs:
        c_item["overlays"] = c_ovs
    cuts.append(c_item)
(PACK / "cuts_v06.json").write_text(json.dumps(cuts, indent=2))

reuse_rows = {n: [s["row"] for s in stills if s["src"].name == n] for n in sorted(reuse, key=lambda n: (-reuse[n], n))}
(PACK / "reuse_v06.json").write_text(json.dumps(dict(stills=dict(sorted(reuse.items(), key=lambda x: (-x[1], x[0]))), rows=reuse_rows, video=dict(sorted(vreuse.items(), key=lambda x: (-x[1], x[0])))), indent=2))

buf = io.StringIO()
wr = csv.writer(buf)
wr.writerow(["row", "source", "vo_in", "vo_out", "vo_text"])
for c_item in cuts:
    text = " ".join(w["text"] for w in words if c_item["timeline_in"] <= (w["start"] + w["end"]) / 2 < c_item["timeline_out"])
    wr.writerow([c_item["row"], c_item["source"], f"{c_item['timeline_in']:.3f}", f"{c_item['timeline_out']:.3f}", text or "[no VO]"])
(PACK / "nearest_star_rough_v06_assembled.csv").write_text(buf.getvalue())
(PACK / "nearest_star_words_list.json").write_text(json.dumps(words))
cc = sp.run([sys.executable, str(CLIP_CHECK), str(PACK / "nearest_star_rough_v06_assembled.csv"), "--words", str(PACK / "nearest_star_words_list.json")], capture_output=True, text=True)
(PACK / "clip_check_py.txt").write_text(cc.stdout + cc.stderr)
inside = [c_item["timeline_in"] for c_item in cuts[1:] if any(w["start"] + 0.02 < c_item["timeline_in"] < w["end"] - 0.02 for w in words)]
align = dict(runtime=runtime, expected=TOTAL, vo_last_word_end=LAST_WORD, hold_after_last_word=HOLD, fade=FADE, cuts=len(cuts), cuts_inside_a_word=inside, longest_shot=max(c_item["timeline_out"] - c_item["timeline_in"] for c_item in cuts), max_upscale=max(c_item["upscale"] for c_item in cuts))
(PACK / "align_vs_vo.json").write_text(json.dumps(align, indent=2))

frames = PACK / "frames"
frames.mkdir(exist_ok=True)


def grab(t, dst, w=480):
    run(["-ss", f"{t:.3f}", "-i", LOCAL_OUT, "-frames:v", "1", "-vf", f"scale={w}:{w*9//16}", dst])


tiles = []
for k, c_item in enumerate(cuts):
    mid = (c_item["timeline_in"] + c_item["timeline_out"]) / 2
    dst = frames / f"row_{k:03}.jpg"
    grab(mid, dst)
    tiles.append((dst, f"{c_item['row']} {mid:.1f}s {c_item['source'][:22]}"))


def sheet(name, items_list, cols=6):
    rows_n = math.ceil(len(items_list) / cols)
    board = Image.new("RGB", (cols * 320, rows_n * 200), (18, 18, 22))
    d = ImageDraw.Draw(board)
    for i, (p, label) in enumerate(items_list):
        x = i % cols * 320
        y = i // cols * 200
        board.paste(Image.open(p).resize((320, 180)), (x, y))
        d.text((x + 6, y + 182), label, fill="white")
    board.save(PACK / (name + ".jpg"), quality=90)


sheet("per_row_sheet_v06", tiles)
fill = [dict(row=c_item["row"], cut=k, source=c_item["source"], frac=round(border_fill_fraction(frames / f"row_{k:03}.jpg"), 4)) for k, c_item in enumerate(cuts)]
for f in fill:
    if f["frac"] > FILL_MAX and f["source"] in REVIEWED_OK:
        f.update(status="reviewed_ok", note=REVIEWED_OK[f["source"]])
fill_fail = [f for f in fill if f["frac"] > FILL_MAX and "status" not in f]
fill_reviewed = [f for f in fill if f.get("status") == "reviewed_ok"]
(PACK / "fill_gate_v06.json").write_text(json.dumps(dict(rule="fail if near-black(<12)/near-white(>245) pixels touching the border cover > 1.5% of the row frame", verdict="WARN" if fill_fail else "PASS", note=FILL_NOTE, fail=fill_fail, reviewed_ok=fill_reviewed, rows=fill), indent=2))
freezes = [l for l in checks.splitlines() if "freeze_duration" in l]


def tsheet(name, times):
    items_list = []
    for i, t in enumerate(times):
        p = WORK / f"f_{name}_{i}.jpg"
        grab(t, p)
        items_list.append((p, f"{t:.2f}s"))
    sheet(name, items_list, cols=3)


tsheet("frame0_sheet", [0, 0.2, 0.4, 0.6, 0.8, 1])
tsheet("sheet_0_8s", [0, 1, 2, 3, 4, 5, 6, 6.4, 6.6, 7, 7.5, 8])
om = [c_item for c_item in cuts if c_item["source"].startswith("orbit_")]
if om:
    tsheet("sheet_omni", [t for c_item in om for t in (c_item["timeline_in"] + 0.5, (c_item["timeline_in"] + c_item["timeline_out"]) / 2, c_item["timeline_out"] - 0.5)])

h = hashlib.sha256()
with LOCAL_OUT.open("rb") as f_in:
    for b in iter(lambda: f_in.read(1 << 20), b""):
        h.update(b)
(PACK / "SHA256.txt").write_text(f"{h.hexdigest()}  {OUT.name}\n")

(PACK / "polish_reviewed_ok_v06.json").write_text(json.dumps(POLISH_OK, indent=2))
pg = sp.run([sys.executable, str(POLISH), str(LOCAL_OUT), "--cuts", str(PACK / "cuts_v06.json"), "--out", str(PACK / "polish_gate_v06.json"), "--reviewed-ok", str(PACK / "polish_reviewed_ok_v06.json")], capture_output=True, text=True)
(PACK / "polish_gate_v06.txt").write_text(pg.stdout + pg.stderr)

pq = sp.run([sys.executable, str(PIC_QA), str(LOCAL_OUT), "--cuts", str(PACK / "cuts_v06.json"), "--pool", str(HERE / "pool_v03.json"), "--pool", str(HERE / "pool_v03_titles.json"), "--reviewed-ok", str(PACK / "polish_reviewed_ok_v06.json"), "--out-dir", str(PACK / "picture_qa_v06")], capture_output=True, text=True)
(PACK / "picture_qa_v06.txt").write_text(pq.stdout + pq.stderr)

mg = sp.run([sys.executable, str(MUSIC_GATE), str(EP), "--bed", str(BED), "--video", str(LOCAL_OUT), "--out", str(PACK / "music_gate_v06.json")], capture_output=True, text=True)
(PACK / "music_gate_v06.txt").write_text(mg.stdout + mg.stderr)

summary = dict(
    out=str(OUT),
    sha256=h.hexdigest(),
    runtime=runtime,
    lufs=lufs,
    clip_check_exit=cc.returncode,
    polish_gate="PASS" if pg.returncode == 0 else "FAIL",
    picture_qa="PASS" if pq.returncode == 0 else "FAIL",
    music_gate="PASS" if mg.returncode == 0 else "FAIL",
    align=align,
    reuse_stills=dict(reuse),
)
(PACK / "summary_v06.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=1))
print(cc.stdout + cc.stderr)
print(pg.stdout + pg.stderr)
print(pq.stdout + pq.stderr)
print(mg.stdout + mg.stderr)
