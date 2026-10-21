#!/usr/bin/env python3
"""024 Light Speed full rough v06 (J0792):
1. All diagrams redrawn in graphics_v06 (`code_graphics.py`) so a 12-year-old with the sound off understands:
   real NASA Blue Marble Earth disc, moving spacecraft hull with engine plume, two clocks with live tick counters,
   growing 20 YEARS vs 3 YEARS bars, shrinking 10 LIGHT-YEARS vs 1.5 LIGHT-YEARS distance bars, turnaround trajectory
   diagram, labelled muon column (660 meters vs ground), labelled GPS clock drift bars, and energy vs speed curve.
2. Orbit back in and given a job across 5 beats (8 cuts, 38.4 s total, outside the first 30 s) at the places where
   the idea turns:
   - Row 15 (2:21.4): Orbit watches the light clock tick slower (`orbit_lightclock_omni_v01` @ 4.5s).
   - Row 21 (3:53.1) & Row 22 (4:00.7): Orbit sets out toward the target star and rides the 3-year ship trip (`orbit_thumb_omni_v01` @ 1.5s & 5.2s).
   - Row 25 (4:40.0): Orbit flies across the shrunken 1.5 light-year star gap (`orbit_walk_omni_v01` @ 0.5s & 4.5s).
   - Row 26 (4:51.7) & Row 27 (5:12.7): Orbit turns around and returns above Earth's night city lights (`orbit_returns_omni_v01` @ 0.5s & 5.2s).
   - Row 37 (7:22.4): Orbit floats in deep space as the ship clock drifts from home (`orbit_lightclock_omni_v01` @ 0.2s).
3. Zero back-to-back code graphics anywhere in the film: real moving imagery or Orbit sits between every code graphic.
4. Copies the locked v05 audio stream from `024_LightSpeed_full_rough_v05d.mp4` and adds the 5 chapter cards, subscribe
   cue, and row 2/8/11/17/18/35/36 VO labels on real footage shots.
`--plan` prints the segment list and checks without rendering."""
from pathlib import Path
import json, subprocess as sp, re, hashlib, math, sys, csv, io, shutil
from collections import Counter, defaultdict
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None

HERE = Path(__file__).resolve().parent
EP = HERE.parent
sys.path.insert(0, str(EP.parents[1] / "scripts"))
from still_motion import push as still_push

UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
WORK = Path("/private/tmp/light024_full_work_v06")
PACK = HERE / "full_rough_v06_pack"
V05D = HERE / "024_LightSpeed_full_rough_v05d.mp4"
VO = EP / "02_Voiceover/light_speed_vo_v01.mp3"
BED = EP / "05_Music/light-speed_score_bed_v01_full.mp3"
OUT = Path("/private/tmp/024_LightSpeed_full_rough_v06.mp4")

MAX_UP = 2.35
MAX_HOLD = 6.0
G2 = HERE / "graphics_v02"
G5 = HERE / "graphics_v05"
G6 = Path("/private/tmp/light024_graphics_v06")
H = HERE / "nasa_pool_v01/024_harvest_v01"
OM24 = EP / "04_Generated-Clips/01_Raw/omni_v01"
OM26 = EP.parent / "026_How-Far-Is-The-Nearest-Star/04_Generated-Clips/01_Raw/omni_v01"

FPS = 30
LAST_WORD = 487.544
HOLD = 2.5
FADE = 1.0
TOTAL = round((LAST_WORD + HOLD + FADE) * FPS) / FPS
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
CLIP_CHECK = EP.parents[1] / "00_Brand/Channel-Setup/tools/clip_check.py"
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
SF2 = G2 / "starfield.mp4"
EV = H / "Earth_Views_from_the_International_Space_Station.mp4"
ART = H / "KSC-20221116-MH-AJN01-0001-Artemis_I_Isolated_Launch_Views-3314595.mp4"
NHQ = H / "NHQ_2019_0626_Earth_Views_from_the_ISS.mp4"
NHQC = (88, 104, 1096, 616)
GPS = "GPS_Block_IIIA.jpg"
GAIA = "Gaia’s_sky_in_colour_ESA393127.jpg"
BM = "GSFC_20171208_Archive_e002130.jpg"
EVA = "iss038e020263.jpg"

OM_LC = OM24 / "orbit_lightclock_omni_v01.mp4"
OM_RET = OM24 / "orbit_returns_omni_v01.mp4"
OM_STAR = OM26 / "orbit_thumb_omni_v01.mp4"
OM_WALK = OM26 / "orbit_walk_omni_v01.mp4"


def v(at, **k):
    return dict(video=1, at=at, **k)


def f(at, **k):
    return dict(video=1, at=at, fixed=1, **k)


X = dict(fixed=1)


def g(plate, **k):
    return dict(video=1, fixed=1, plate=plate, **k)


SF, LC, EN, TW, MU, GC, MD, GM, CT = (
    g(n) for n in ("starfield", "lightclock", "energy", "twinclocks", "muons", "gpsclocks", "mapdrift", "gammaclocks", "contraction")
)

S = [
    ("1", 0.0, SF2, v(12.0, hold_ok=1)),
    ("2", 6.5, EV, v(14.0)),
    ("2", 9.65, EV, f(75.0)),
    ("3", 13.03, "", LC),
    ("4", 18.9, BM, dict(fixed=1)),
    ("5", 23.2, GPS, {}),
    ("6", 28.3, "", dict(LC, fixed=0)),
    ("6", 32.5, "ACS3_LookingDown.png", dict(box=(0.0, 0.0, 0.5, 1.0), fixed=1)),
    ("6", 36.8, "", dict(EN, fixed=0)),
    ("7", 41.5, GPS, dict(quad="c")),
    ("7", 45.8, "", dict(GC, fixed=0)),
    ("8", 49.78, "PIA24573.jpg", X),
    ("8", 53.31, "", GC),
    ("8", 59.1, "PIA24573.jpg", dict(quad="c", fixed=1)),
    ("8", 62.13, "", GC),
    ("9", 67.09, "iss040e091231.jpg", dict(quad="c", fixed=1)),
    ("9", 71.68, "", MD),
    ("9", 75.6, "", dict(MD, fixed=0)),
    ("10", 79.77, "iss035e017673.jpg", X),
    ("11", 84.72, "EC00-0050-001.jpg", X),
    ("11", 88.04, "EC98-44444-004.jpg", X),
    ("11", 93.98, "ED07-0256-09.jpg", X),
    ("11", 98.74, "EC00-0050-001.jpg", dict(quad="c", fixed=1)),
    ("12", 103.85, "", LC),
    ("12", 107.16, "", LC),
    ("13", 110.29, NHQ, f(1200.0, vcrop=NHQC)),
    ("13", 113.97, NHQ, f(1203.68, vcrop=NHQC)),
    ("14", 118.68, "", LC),
    ("14", 121.61, "", LC),
    ("14", 126.82, ART, f(500.0)),
    ("14", 131.14, "", LC),
    ("14", 135.23, "", LC),
    ("14", 138.3, "", LC),
    ("15", 141.37, OM_LC, f(4.5)),
    ("15", 145.13, "", LC),
    ("15", 150.22, "", LC),
    ("15", 153.9, EVA, X),
    ("16", 156.67, "", GM),
    ("16", 161.6, "", GM),
    ("16", 167.15, "", GM),
    ("16", 170.97, "", GM),
    ("17", 176.02, "iss071e439624.jpg", X),
    ("17", 179.34, "", MU),
    ("17", 184.64, "iss071e439624.jpg", dict(quad="c", fixed=1)),
    ("17", 188.7, "", MU),
    ("17", 192.86, EV, f(50.0)),
    ("17", 195.09, "", MU),
    ("18", 199.05, "sts33-17-005a.jpg", X),
    ("18", 204.43, "", MU),
    ("18", 209.3, ART, f(620.0)),
    ("19", 213.06, "", SF),
    ("19", 215.99, "", SF),
    ("20", 219.57, "", SF),
    ("21", 224.01, ART, f(260.0)),
    ("21", 228.24, ART, f(380.0)),
    ("21", 233.07, OM_STAR, f(1.2)),
    ("22", 235.8, "", TW),
    ("22", 240.75, "iss040e085126.jpg", X),
    ("22", 245.95, NHQ, f(1740.0, vcrop=NHQC)),
    ("22", 248.75, "", TW),
    ("23", 253.66, "iss019e018483.jpg", dict(box=(0, 0, 1, 0.92), fixed=1)),
    ("24", 259.44, "", dict(SF, var="e")),
    ("24", 263.3, "", dict(SF, var="e")),
    ("25", 269.1, BM, dict(box=(0.15, 0.15, 0.85, 0.85), fixed=1)),
    ("25", 274.06, "", CT),
    ("25", 280.03, OM_WALK, f(0.5)),
    ("25", 283.93, OM_WALK, f(4.4)),
    ("26", 286.9, "", TW),
    ("26", 291.73, NHQ, f(2400.0, vcrop=NHQC)),
    ("26", 297.27, "", TW),
    ("26", 301.72, EVA, dict(quad="c", fixed=1)),
    ("26", 306.87, EV, f(110.0)),
    ("27", 312.71, OM_RET, f(5.0)),
    ("28", 317.05, "ED07-0256-09.jpg", dict(quad="c", fixed=1, hold_ok=1)),
    ("29", 323.91, "SSC-20240229-s00309.tif", X),
    ("30", 329.49, "", EN),
    ("30", 333.09, "SSC-2015-00064.jpg", X),
    ("30", 337.22, "GSFC_20171208_Archive_e001593.jpg", X),
    ("30", 342.04, "", EN),
    ("30", 346.28, "", EN),
    ("31", 351.35, "", EN),
    ("31", 356.29, "SSC-20240229-s00309.tif", dict(quad="c", fixed=1)),
    ("31", 359.17, "", EN),
    ("31", 363.27, "", EN),
    ("32", 368.51, "sts080-326-010.jpg", X),
    ("32", 373.6, "sts080-326-010.jpg", dict(quad="c", fixed=1)),
    ("33", 378.91, "NHQ201808120013.tif", X),
    ("33", 384.77, "NHQ201808120013.tif", dict(quad="c", fixed=1)),
    ("34", 389.28, "ACS3_SolarSailSunrise.png", X),
    ("34", 393.25, "ACS3_LookingDown.png", dict(box=(0.5, 0, 1, 1), fixed=1)),
    ("35", 398.77, "", SF),
    ("35", 402.06, "", SF),
    ("35", 406.67, GAIA, X),
    ("35", 412.49, GAIA, dict(quad="c", fixed=1)),
    ("35", 416.09, ART, f(800.0)),
    ("36", 420.54, NHQ, f(570.0, vcrop=NHQC)),
    ("36", 425.2, "iss040e085126.jpg", dict(quad="c", fixed=1)),
    ("36", 428.95, NHQ, f(1830.0, vcrop=NHQC)),
    ("36", 432.0, "iss040e091231.jpg", X),
    ("36", 435.0, "ACS3_SolarSailSunrise.png", dict(quad="c", fixed=1)),
    ("37", 438.57, "", dict(TW, var="e")),
    ("37", 442.42, EP.parents[0] / "023_What-Happened-To-Venus/04_Generated-Clips/01_Raw/omni_v01/orbit_looks_back_earth_omni_v01.mp4", f(1.5)),
    ("37", 446.0, "iss035e017673.jpg", dict(quad="c", fixed=1)),
    ("38", 448.61, "", dict(GC, var="d")),
    ("38", 453.98, "sts33-17-005a.jpg", dict(quad="c", fixed=1)),
    ("38", 457.42, EV, f(176.0, hold_ok=1)),
    ("39", 464.98, "SSC-2015-00064.jpg", dict(box=(0.3, 0.1, 1.0, 0.9), fixed=1)),
    ("39", 470.24, "EC98-44444-004.jpg", dict(box=(0.05, 0.25, 0.95, 0.85))),
    ("39", 475.69, "iss019e018483.jpg", dict(box=(0.12, 0.08, 0.72, 0.62))),
    ("39", 479.77, "GSFC_20171208_Archive_e001593.jpg", dict(box=(0.2, 0.05, 0.8, 0.95))),
    ("39", 483.48, "", dict(SF, var="i", fixed=0, hold_ok=1)),
]

FORCED = {("twinclocks", "e"), ("starfield", "e"), ("starfield", "i"), ("gpsclocks", "d")}
CHAPTERS = [
    ("Your Clock Is Already Slow", 42.0),
    ("Why Light Sets the Limit", 110.7),
    ("The Trip", 224.4),
    ("The Price of Every Nine", 324.5),
    ("A One-Way Ticket to the Future", 399.2),
]

GAPS = [((a["end"] + b["start"]) / 2, b["start"] - a["end"]) for a, b in zip(words, words[1:])]


def snap(t):
    if t > LAST_WORD:
        return t
    for need in (0.30, 0.20, 0.10):
        c = [m for m, g in GAPS if g >= need and abs(m - t) <= 2.0]
        if c:
            return min(c, key=lambda m: abs(m - t))
    raise SystemExit(f"no VO pause near {t}")


def at(token, near):
    return min((w for w in words if w["text"].rstrip(".,").lower() == token.lower()), key=lambda w: abs(w["start"] - near))["start"]


# VO labels on real footage / stills (code graphics carry their own built-in labels in v06)
LABELS = [
    ("2", "1 year", at("one", 7.7), 10.9, 960, 830, 76, "SOURCES row 2: 1 ship year = 7.09 Earth years at 0.99c"),
    ("2", "7 years", at("seven", 11.0), 12.8, 960, 830, 76, "SOURCES row 2: 7 Earth years"),
    ("8", "about 46", at("forty-six", 61.0), 62.13, 1380, 150, 72, "Ashby 2003: GR +45.9 us/day"),
    ("11", "1971", at("1971", 85.2), 88.0, 330, 120, 84, "Hafele & Keating 1972 (flights 1971)"),
    ("17", "660 meters", at("660", 193.0), 195.0, 960, 820, 76, "Frisch & Smith 1963: ~660 m"),
    ("18", "1963", at("1963", 199.7), 203.6, 330, 120, 84, "Frisch & Smith 1963"),
    ("35", "over 20 years", at("twenty", 413.6), 416.0, 960, 110, 72, "SOURCES row 20: 22.4 yr crew time"),
    ("36", "100,000 years", at("hundred", 422.3), 426.2, 1350, 120, 72, "SOURCES row 20: ~100,000 yr on Earth"),
]

segs = []
for i, (row, t, src, o) in enumerate(S):
    tin = t if (i == 0 or o.get("fixed")) else snap(t)
    segs.append(dict(row=row, timeline_in=fr(tin), src=src if isinstance(src, Path) else H / src, o=dict(o)))
for a, b in zip(segs, segs[1:]):
    a["timeline_out"] = b["timeline_in"]
segs[-1]["timeline_out"] = TOTAL

# Check that no two distinct code graphics run back-to-back (same plate continuing across VO cuts is one graphic)
PAD = 0.25
SAME = 10.0
runs = []
for s in segs:
    p = s["o"].get("plate")
    if p and runs and runs[-1][0] == p and runs[-1][1][-1] is segs[segs.index(s) - 1]:
        runs[-1][1].append(s)
    elif p:
        runs.append([p, [s]])

# Verify no two runs are back-to-back
for (p1, ss1), (p2, ss2) in zip(runs, runs[1:]):
    if abs(ss1[-1]["timeline_out"] - ss2[0]["timeline_in"]) < 0.05:
        raise SystemExit(f"Back-to-back code graphics: {p1} ends at {ss1[-1]['timeline_out']} where {p2} starts!")

claimed = defaultdict(list)
dur_of = {}
last_var = {}
alloc = []
pending = list(runs)
while pending:
    plate, ss = pending.pop(0)
    L = ss[-1]["timeline_out"] - ss[0]["timeline_in"] + 2 * PAD
    best = None
    forced = ss[0]["o"].get("var")
    for var in ([forced] if forced else "abcdefgh"):
        if not forced and (plate, var) in FORCED:
            continue
        # Use G6 for redrawn graphics, or G5 for unchanged starfield variants (except starfield_e which is redrawn in G6)
        fp = (G6 / f"{plate}_{var}.mp4") if (G6 / f"{plate}_{var}.mp4").exists() else (G5 / f"{plate}_{var}.mp4")
        if not fp.exists() and PLAN:
            dur = 26.0
        elif not fp.exists():
            continue
        else:
            dur = dur_of[fp] if fp in dur_of else dur_of.setdefault(fp, probe(fp))
        used = claimed[(plate, var)]
        off = PAD if not used else max(max(e for _, e in used) + PAD, max(st for st, _ in used) + SAME)
        if off + L > dur - 0.2:
            continue
        score = (var == last_var.get(plate), len(used), off)
        if best is None or score < best[0]:
            best = (score, var, off)
    if best is None and len(ss) > 1:
        k = len(ss) // 2
        pending[:0] = [[plate, ss[:k]], [plate, ss[k:]]]
        continue
    if best is None:
        raise SystemExit(f'no free stretch for {plate} run of {L:.1f}s at {ss[0]["timeline_in"]}')
    _, var, off = best
    claimed[(plate, var)].append((off, off + L))
    last_var[plate] = var
    for s in ss:
        fp6 = G6 / f"{plate}_{var}.mp4"
        s["src"] = fp6 if (fp6.exists() or plate != "starfield" or var == "e") else (G5 / f"{plate}_{var}.mp4")
        s["o"]["at"] = round(off + PAD + (s["timeline_in"] - ss[0]["timeline_in"]), 3)
    alloc.append(dict(plate=plate, variant=var, film_in=ss[0]["timeline_in"], film_out=ss[-1]["timeline_out"], offset=round(off + PAD, 3), cuts=len(ss)))

for s in segs:
    if s["o"].get("video"):
        s["o"]["offset"] = s["o"].get("at", 0.0)


def framed(s):
    im = Image.open(s["src"]).convert("RGB")
    o = s["o"]
    if "box" in o:
        x0, y0, x1, y1 = o["box"]
        im = im.crop((int(im.width * x0), int(im.height * y0), int(im.width * x1), int(im.height * y1)))
    if "quad" in o:
        fx, fy = Q[o["quad"]]
        im = im.crop((int(im.width * fx), int(im.height * fy), int(im.width * (fx + 0.5)), int(im.height * (fy + 0.5))))
    return im


def vsize(p):
    if not p.exists() and PLAN:
        return (1920, 1080)
    return tuple(map(int, sp.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(p)], text=True).strip().split(",")[:2]))


def upscale(s):
    o = s["o"]
    if o.get("video"):
        w, h = vsize(s["src"])
        if o.get("vcrop"):
            w, h = o["vcrop"][2:]
        return w, max(1920 / w, 1080 / h)
    im = framed(s)
    return im.width, max(1920 / im.width, 1080 / im.height) * (1 + o.get("pct", 0.05))


stills = [s for s in segs if not s["o"].get("video")]
reuse = Counter(s["src"].name for s in stills)
vreuse = Counter(s["src"].name for s in segs if s["o"].get("video"))
problems = []
for name, n in reuse.items():
    uses = [s for s in stills if s["src"].name == name]
    if n > 2:
        problems.append(f"{name} used {n}x")
    if n == 2 and (uses[0]["o"].get("quad"), uses[0]["o"].get("box")) == (uses[1]["o"].get("quad"), uses[1]["o"].get("box")):
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
        if s["o"]["offset"] + d + 0.2 > L and not s["o"].get("bookend"):
            problems.append(f"{s['row']} {s['src'].name} runs {s['o']['offset']+d+0.2-L:.2f}s past its end")
for s in segs[1:]:
    c = s["timeline_in"]
    near = [w for w in words if w["start"] + 0.02 < c < w["end"] - 0.02]
    if near:
        problems.append(f"cut {c:.2f} ({s['row']}) inside '{near[0]['text']}' {near[0]['start']:.2f}-{near[0]['end']:.2f}")
for s in segs:
    if not s["src"].exists() and not PLAN:
        problems.append(f'missing {s["src"]}')
        continue
    s["src_w"], s["upscale"] = upscale(s)
    s["upscale"] = round(s["upscale"], 3)
    if s["upscale"] > MAX_UP:
        problems.append(f"{s['row']} {s['src'].name} upscale {s['upscale']:.2f} > {MAX_UP}")
ev = sorted({s["o"]["offset"] for s in segs if s["src"] == EV})
if len(ev) > 5:
    problems.append(f"Earth Views in {len(ev)} stretches {ev}")

print("reuse (stills):", dict(sorted(reuse.items(), key=lambda x: -x[1])))
print("reuse (video/graphics):", dict(sorted(vreuse.items(), key=lambda x: -x[1])))
if PLAN or problems:
    for a in alloc:
        print(f"alloc {a['plate']:12} {a['variant']} film {a['film_in']:7.2f}-{a['film_out']:7.2f} from {a['offset']:5.2f}s ({a['cuts']} cuts)")
    for s in segs:
        print(f"{s['row']:>4} {s['timeline_in']:8.2f} {s['timeline_out']-s['timeline_in']:5.2f}  {s['src'].name[:44]:44} up {s.get('upscale',0):4.2f} {json.dumps({k:v for k,v in s['o'].items() if k not in('fixed','video','at')})}")
    print("segments:", len(segs), "runtime", TOTAL)
    print("problems:", problems or "none")
    raise SystemExit(1 if problems else 0)


def prep_still(s):
    im = framed(s)
    im = ImageEnhance.Color(im).enhance(1.06)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    scale = max(2112 / im.width, 1188 / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    x = (im.width - 2112) // 2
    y = (im.height - 1188) // 2
    return im.crop((x, y, x + 2112, y + 1188))


def pill(text, px, dst):
    fnt = ImageFont.truetype(FONT, px)
    w = int(fnt.getlength(text))
    h = int(px * 1.55)
    padx = int(px * 0.55)
    img = Image.new("RGBA", (w + 2 * padx, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w + 2 * padx - 1, h - 1), radius=int(px * 0.32), fill=(23, 36, 55, 220))
    d.text((padx, int(px * 0.22)), text, font=fnt, fill="white")
    img.save(dst)
    return img.size


WORK.mkdir(parents=True, exist_ok=True)
PACK.mkdir(parents=True, exist_ok=True)
(PACK / "graphics_alloc_v06.json").write_text(json.dumps(alloc, indent=2))
ENC = ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-threads", "4"]


def okkey(s):
    return json.dumps([s["timeline_in"], s["timeline_out"], str(s["src"]), s["src"].stat().st_mtime, s["o"]], default=str, sort_keys=True)


if "--finish-only" not in sys.argv:
    from concurrent.futures import ThreadPoolExecutor

    def build_seg(item):
        i, s = item
        pre = 0.2 if i else 0
        post = 0.2 if i < len(segs) - 1 else 0
        frames = round((s["timeline_out"] - s["timeline_in"] + pre + post) * FPS)
        dest = WORK / f"seg_{i:03}.mp4"
        if dest.exists() and (WORK / f"seg_{i:03}.ok").exists() and (WORK / f"seg_{i:03}.ok").read_text() == okkey(s):
            print("reuse", i, s["row"], flush=True)
            return
        print("seg", i, s["row"], s["timeline_in"], s["timeline_out"], s["src"].name, flush=True)
        o = s["o"]
        if o.get("video"):
            off = o["offset"]
            vc = o.get("vcrop")
            push = f",scale=w='2*trunc(960*(1+{o['push']}*t/{frames/FPS:.3f}))':h=-2:eval=frame,crop=1920:1080" if o.get("push") else ""
            pad = ",tpad=stop_mode=clone:stop_duration=2" if o.get("bookend") else ""
            vf = (f"crop={vc[2]}:{vc[3]}:{vc[0]}:{vc[1]}," if vc else "") + "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30" + push + ",setsar=1" + pad
            run(["-ss", max(0, off - pre), "-i", s["src"], "-vf", vf + ",format=yuv420p", "-frames:v", frames, *ENC, dest])
        else:
            still_push(prep_still(s), frames / FPS, dest, pct=o.get("pct", 0.05))
        got = round(probe(dest) * FPS)
        if got < frames - 1:
            raise RuntimeError(f'seg {i} {s["row"]}: {got} frames < {frames}')
        (WORK / f"seg_{i:03}.ok").write_text(okkey(s))

    with ThreadPoolExecutor(max_workers=6) as ex:
        list(ex.map(build_seg, enumerate(segs)))

    if not (WORK / "picture_raw.mp4").exists() or "--rebuild-raw" in sys.argv:
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
                run(["-ss", length - 0.4, "-i", p, "-i", nxt, "-filter_complex", "[0:v]setpts=PTS-STARTPTS[a];[1:v]trim=duration=0.4,setpts=PTS-STARTPTS[b];[a][b]xfade=transition=fade:duration=0.4:offset=0,format=yuv420p[v]", "-map", "[v]", "-frames:v", 12, *ENC, trans])
                out_items.append(trans)
            return out_items

        with ThreadPoolExecutor(max_workers=6) as ex:
            chunk_lists = list(ex.map(build_chunk, enumerate(segs)))
        chunks = [c for sub in chunk_lists for c in sub]
        (WORK / "concat.txt").write_text("".join(f"file '{p}'\n" for p in chunks))
        run(["-f", "concat", "-safe", "0", "-i", WORK / "concat.txt", "-c", "copy", WORK / "picture_raw.mp4"])
    else:
        print("reuse picture_raw.mp4", flush=True)

    # Chapter lower-thirds (2.5 s from the chapter's first word), 4 s subscribe cue, and real-footage VO labels
    def first_word(t):
        return next(w["start"] for w in words if w["start"] >= t - 0.5)

    font = ImageFont.truetype(FONT, 62)
    ov = []
    for k, (title, t) in enumerate(CHAPTERS):
        w = int(font.getlength(title)) + 70
        img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((90, 860, 90 + w, 990), radius=15, fill=(23, 36, 55, 220))
        d.text((125, 886), title, font=font, fill="white")
        p = WORK / f"card_{k}.png"
        img.save(p)
        a = first_word(t)
        ov.append((p, a, a + 2.5, 0, 0, "card", title))

    sub_at = next(w["start"] for w in words if w["text"].startswith("Subscribing"))
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f2 = ImageFont.truetype(FONT, 44)
    d.rounded_rectangle((1440, 900, 1830, 990), radius=45, fill=(204, 0, 0, 235))
    d.text((1500, 918), "SUBSCRIBE", font=f2, fill="white")
    p = WORK / "subscribe.png"
    img.save(p)
    ov.append((p, sub_at, sub_at + 4.0, 0, 0, "subscribe", "SUBSCRIBE"))

    lbl_records = []
    for k, (r, t_txt, a, b, cx, y, px, note) in enumerate(LABELS):
        name = f"code_graphic_024_row{r}_{k:02}.png"
        p = WORK / name
        w, h = pill(t_txt, px, p)
        shutil.copyfile(p, PACK / name)
        x = cx - w // 2
        ov.append((p, a, b, x, y, "label", t_txt))
        lbl_records.append(dict(file=name, row=r, text=t_txt, start=round(a, 3), end=round(b, 3), x=x, y=y, size=[w, h], check=note))

    inputs = ["-i", WORK / "picture_raw.mp4"]
    fc = "[0:v]null[v0];"
    for k, (p, a, b, x, y, kind, _) in enumerate(ov):
        dur = b - a
        inputs += ["-loop", "1", "-framerate", "30", "-t", f"{TOTAL:.3f}", "-i", p]
        fc += f"[{k+1}:v]format=rgba,fade=t=in:st={a:.3f}:d=0.30:alpha=1,fade=t=out:st={max(a,b-0.30):.3f}:d=0.30:alpha=1[o{k}];"
        if kind == "label":
            fc += f"[v{k}][o{k}]overlay=x={x}:y='{y}+22*max(0\\,1-(t-{a:.3f})/0.35)':eval=frame:enable='between(t,{a:.3f},{b:.3f})'[v{k+1}];"
        else:
            fc += f"[v{k}][o{k}]overlay=x=0:y=0:enable='between(t,{a:.3f},{b:.3f})'[v{k+1}];"
    fc += f"[v{len(ov)}]fade=t=out:st={TOTAL-FADE:.3f}:d={FADE},format=yuv420p[v]"
    (WORK / "fc.txt").write_text(fc)
    run([*inputs, "-/filter_complex", WORK / "fc.txt", "-map", "[v]", "-t", TOTAL, *ENC, WORK / "picture.mp4"])
    (PACK / "overlays_v06.json").write_text(json.dumps(dict(
        cards=[dict(file=Path(p).name, start=round(a, 3), end=round(b, 3), title=txt) for p, a, b, _, _, kind, txt in ov if kind != "label"],
        labels=lbl_records,
    ), indent=2))

    # Copy the locked v05 audio stream from 024_LightSpeed_full_rough_v05d.mp4
    run(["-i", WORK / "picture.mp4", "-i", V05D, "-map", "0:v", "-map", "1:a", "-c", "copy", "-t", TOTAL, "-movflags", "+faststart", OUT])

runtime = probe(OUT)
ll = sp.run(["ffmpeg", "-hide_banner", "-i", str(OUT), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
lufs = float(re.findall(r"I:\s*([-\d.]+) LUFS", ll)[-1])
checks = sp.run(["ffmpeg", "-hide_banner", "-i", str(OUT), "-vf", "blackdetect=d=0.1:pix_th=0.10:pic_th=0.98,freezedetect=n=-50dB:d=1", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
(PACK / "ffmpeg_checks.txt").write_text("\n".join(l for l in checks.splitlines() if "black_" in l or "freeze" in l))
cuts = [
    dict(
        row=s["row"],
        timeline_in=s["timeline_in"],
        timeline_out=s["timeline_out"],
        source=s["src"].name,
        framing={k: v for k, v in s["o"].items() if k in ("quad", "offset", "vcrop", "box")},
        src_w=s["src_w"],
        upscale=s["upscale"],
    )
    for s in segs
]
(PACK / "cuts_v06.json").write_text(json.dumps(cuts, indent=2))
reuse_rows = {n: [s["row"] for s in stills if s["src"].name == n] for n in sorted(reuse, key=lambda n: (-reuse[n], n))}
(PACK / "reuse_v06.json").write_text(json.dumps(dict(stills=dict(sorted(reuse.items(), key=lambda x: (-x[1], x[0]))), rows=reuse_rows, video=dict(sorted(vreuse.items(), key=lambda x: (-x[1], x[0])))), indent=2))

buf = io.StringIO()
wr = csv.writer(buf)
wr.writerow(["row", "source", "vo_in", "vo_out", "vo_text"])
for c in cuts:
    text = " ".join(w["text"] for w in words if c["timeline_in"] <= (w["start"] + w["end"]) / 2 < c["timeline_out"])
    wr.writerow([c["row"], c["source"], f"{c['timeline_in']:.3f}", f"{c['timeline_out']:.3f}", text or "[no VO]"])
(PACK / "light_speed_full_v06_assembled.csv").write_text(buf.getvalue())
(PACK / "light_speed_words_list.json").write_text(json.dumps(words))
cc = sp.run([sys.executable, str(CLIP_CHECK), str(PACK / "light_speed_full_v06_assembled.csv"), "--words", str(PACK / "light_speed_words_list.json")], capture_output=True, text=True)
(PACK / "clip_check_py.txt").write_text(cc.stdout + cc.stderr)
inside = [c["timeline_in"] for c in cuts[1:] if any(w["start"] + 0.02 < c["timeline_in"] < w["end"] - 0.02 for w in words)]
align = dict(runtime=runtime, expected=TOTAL, vo_last_word_end=LAST_WORD, hold_after_last_word=HOLD, fade=FADE, cuts=len(cuts), cuts_inside_a_word=inside, longest_shot=max(c["timeline_out"] - c["timeline_in"] for c in cuts), max_upscale=max(c["upscale"] for c in cuts))
(PACK / "align_vs_vo.json").write_text(json.dumps(align, indent=2))

frames = PACK / "frames"
frames.mkdir(exist_ok=True)


def grab(t, dst, w=480):
    run(["-ss", f"{t:.3f}", "-i", OUT, "-frames:v", "1", "-vf", f"scale={w}:{w*9//16}", dst])


tiles = []
for k, c in enumerate(cuts):
    mid = (c["timeline_in"] + c["timeline_out"]) / 2
    dst = frames / f"row_{k:03}.jpg"
    grab(mid, dst)
    tiles.append((dst, f"{c['row']} {mid:.1f}s {c['source'][:22]}"))


def sheet(name, items, cols=6):
    rows_n = math.ceil(len(items) / cols)
    board = Image.new("RGB", (cols * 320, rows_n * 200), (18, 18, 22))
    d = ImageDraw.Draw(board)
    for i, (p, label) in enumerate(items):
        x = i % cols * 320
        y = i // cols * 200
        board.paste(Image.open(p).resize((320, 180)), (x, y))
        d.text((x + 6, y + 182), label, fill="white")
    board.save(PACK / (name + ".jpg"), quality=90)


sheet("per_row_sheet_v06", tiles)


def tsheet(name, times):
    items = []
    for i, t in enumerate(times):
        p = WORK / f"f_{name}_{i}.jpg"
        grab(t, p)
        items.append((p, f"{t:.2f}s"))
    sheet(name, items, cols=3)


tsheet("frame0_sheet", [0, 0.2, 0.4, 0.6, 0.8, 1])
tsheet("sheet_0_8s", [0, 1, 2, 3, 4, 5, 6, 6.4, 6.6, 7, 7.5, 8])
om = [c for c in cuts if "omni" in c["source"]]
tsheet("sheet_omni", [t for c in om for t in (c["timeline_in"] + 0.5, (c["timeline_in"] + c["timeline_out"]) / 2, c["timeline_out"] - 0.5)])
tsheet("sheet_end", [LAST_WORD - 1, LAST_WORD + 0.5, LAST_WORD + 1.5, LAST_WORD + 2.5, TOTAL - 0.5, TOTAL - 0.05])

h = hashlib.sha256()
with OUT.open("rb") as fh:
    for b in iter(lambda: fh.read(1 << 20), b""):
        h.update(b)
(PACK / "SHA256.txt").write_text(f"{h.hexdigest()}  {OUT.name}\n")
summary = dict(out=str(OUT), audio="v05 stream copied", sha256=h.hexdigest(), runtime=runtime, lufs=lufs, clip_check_exit=cc.returncode, align=align, reuse_stills=dict(reuse), graphics_alloc=alloc)
(PACK / "summary_v06.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=1))
print(cc.stdout + cc.stderr)
