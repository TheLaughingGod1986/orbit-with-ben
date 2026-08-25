#!/usr/bin/env python3
"""Rebuild Short covers scene-first.

The first pass grabbed a blind frame at 42% of duration, which often landed on an
Orbit close-up or on top of the video's own burned-in caption. This scans the
whole clip and scores every candidate frame so the cover is a scene, not the
mascot, and our punch text lands on clean picture.
"""
import glob
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageStat

FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
P = "/Users/ben/code/Orbit-YouTube/02_Video-Projects"
OUT = Path("/tmp/covers/rebuild")
OUT.mkdir(parents=True, exist_ok=True)

LS = f"{P}/005_The-Last-Star-In-The-Universe/10_Shorts/06_Final-Exports"
EU = f"{P}/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/06_Final-Exports"
NS = f"{P}/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/10_Shorts/06_Final-Exports"
OO = f"{P}/_Experiments/omni-oort-1min-test/10_Shorts/06_Final-Exports"
AL = f"{P}/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports"
BH = f"{P}/002_What-Happens-If-You-Fall-Into-A-Black-Hole/10_Shorts/06_Final-Exports"
EX = f"{P}/003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/06_Final-Exports"
JW = f"{P}/004_JWST-Discoveries-That-Change-Everything/10_Shorts/06_Final-Exports"

# id -> (source pattern, punch lines)
JOBS = [
    # scheduled
    ("DN4L1DkerMM", f"{LS}/last-star_punch-02_star-birth-ends_v05_captions.mp4", ["RUNNING OUT", "OF STARS"]),
    ("wIh3armF7_k", f"{LS}/last-star_punch-03*.mp4", ["THE LAST", "STAR"]),
    ("SdNXS1PD_Yk", f"{LS}/last-star_punch-01_universe-almost-dark_v05_titlecta.mp4", ["RUNNING OUT", "OF LIGHT"]),
    ("IVbO9XkkDps", f"{LS}/last-star_punch-04_last-star-dies_v04_worldlast_lock.mp4", ["THE FINAL", "LIGHT"]),
    ("xRxhb3vSru4", f"{LS}/last-star_punch-05_what-remains_v05_titlecta.mp4", ["WHAT", "REMAINS?"]),
    ("GjcZB8826J8", f"{EX}/exoplanets_short-20s_glass-rain_v01_cfr_fixed.mp4", ["GLASS", "RAIN"]),
    ("QptlHs1HuYI", f"{AL}/aliens_punch-p01_where-is-everybody_v03_cfr_fixed.mp4", ["WHERE IS", "EVERYONE?"]),
    ("Q16DKNvq2OY", f"{OO}/oort_punch-01_fly-past-blue-world_v01.mp4", ["EARTH, FROM", "THE DARK"]),
    ("oN_jm9PTDOQ", f"{OO}/oort_punch-02_sun-bright-pin_v01.mp4", ["THE SUN,", "SHRUNK"]),
    ("0j_pgYbCe5E", f"{OO}/oort_punch-03_far-edge-spark_v01.mp4", ["IT DOESN'T", "END HERE"]),
    ("FbRFvSApfOQ", f"{EU}/europa_punch-01_ocean-we-cannot-see_v03_diamond.mp4", ["MORE WATER", "THAN EARTH"]),
    ("EcsunqhN0jQ", f"{EU}/europa_punch-02_cold-should-win_v02_diamond.mp4", ["IT SHOULDN'T", "EXIST"]),
    ("k0PjH2I0OxY", f"{EU}/europa_punch-03_what-would-life-eat_v02_diamond.mp4", ["WHAT WOULD", "LIFE EAT?"]),
    ("0eqTVgrlU-s", f"{EU}/europa_punch-04_no-daylight-kitchen_v02_diamond.mp4", ["LIFE WITHOUT", "SUNLIGHT"]),
    ("Fv-lSwB_Z-o", f"{EU}/europa_punch-05_sample-without-drilling_v02_diamond.mp4", ["AN OCEAN", "IN SPACE"]),
    ("KPO68c-U42E", f"{EU}/europa_punch-06_clipper-on-its-way_v02_diamond.mp4", ["ALREADY", "FLYING"]),
    ("gN2qAv8m9Wc", f"{EU}/europa_punch-07_do-not-contaminate_v02_diamond.mp4", ["COULD WE", "KILL IT?"]),
    ("TE_HDKAnqms", f"{EU}/europa_punch-08_life-under-ice_v02_diamond.mp4", ["LIFE UNDER", "ICE"]),
    ("fhJP6eMoU0Q", f"{NS}/neutron_star_short-01_line-of-atoms_punch_v03.mp4", ["TORN INTO", "ATOMS"]),
    ("vCxXTYXSSqY", f"{NS}/neutron_star_short-02_teaspoon-mountains_punch_v02.mp4", ["ONE", "TEASPOON"]),
    ("va5ATScn3rs", f"{NS}/neutron_star_short-03_sky-would-lean_punch_v04.mp4", ["THE SKY", "LEANS"]),
    ("o7ykyTDZKiE", f"{NS}/neutron_star_short-04_last-clear-image_punch_v03.mp4", ["YOUR LAST", "IMAGE"]),
    ("Rp_8J6_6IIk", f"{NS}/neutron_star_short-05_too-fast-to-feel_punch_v03.mp4", ["TOO FAST", "TO FEEL"]),
    ("92vmMxSNmlk", f"{NS}/neutron_star_short-06_you-dont-stand_punch_v05.mp4", ["YOU CAN'T", "STAND HERE"]),
    # public
    ("68uTDP2esso", f"{JW}/jwst_short-01*too-big*.mp4", ["TOO BIG,", "TOO SOON"]),
    ("4-ZEpKD1yak", f"{JW}/jwst_short-05_what-webb-sees_v01.mp4", ["INFRARED", "EYES"]),
    ("P32uaiserG0", f"{JW}/jwst_short-06_universe-already-busy_v03.mp4", ["OLDER THAN", "WE THOUGHT?"]),
    ("P-li_ZWk4lg", f"{JW}/*textbook-gap*.mp4", ["TEXTBOOK", "VS REALITY"]),
    ("ZnsJTCcrTlA", f"{JW}/*black-holes-too-soon*.mp4", ["TOO BIG,", "TOO FAST"]),
    ("l1d1ypHxLk0", f"{JW}/*galaxies-too-early*.mp4", ["TOO EARLY"]),
    ("PV50PX-bE4g", f"{LS}/last-star_punch-01_universe-almost-dark_v04_diamond.mp4", ["NO LIGHT"]),
    ("03v4f1hlvtQ", f"{AL}/*zoo-hypothesis*.mp4", ["LEFT ALONE", "ON PURPOSE?"]),
    ("QRi6Dxq0hz0", f"{EX}/exoplanets_short-06_habitability_retention_v2_cfr_fixed.mp4", ["SMELLING", "ALIEN LIFE"]),
    ("OlwENQcY-jg", f"{EX}/*eyeball*.mp4", ["A GIANT", "EYE"]),
    ("tEOHYQbcgOw", f"{EX}/exoplanets_short-04_hot-jupiter_retention_v2_cfr_fixed.mp4", ["NIGHTS HOTTER", "THAN DAY"]),
    ("MDvAKtmKauw", f"{EX}/*three-suns*.mp4", ["THREE SUNS"]),
    ("M-VN84HCNls", f"{EX}/exoplanets_short-02_diamond_retention_v2_cfr_fixed.mp4", ["DIAMOND", "PLANETS"]),
    ("SC2WGTl_V5Q", f"{EX}/*glass-rain*.mp4", ["MOLTEN GLASS", "RAIN"]),
    ("iQUbmlaj4vk", f"{AL}/*space-is-rude*.mp4", ["A REPLY TAKES", "GENERATIONS"]),
    ("5-sofIhR0lI", f"{BH}/*look*back*.mp4", ["LOOKING", "BACK"]),
    ("kBkWtBMKPqE", f"{BH}/*feel*.mp4", ["FEELS LIKE", "NOTHING"]),
    ("9ez9BeqGBtE", f"{BH}/blackhole_punch-p01_cross-this-line_v03_cfr_fixed.mp4", ["ONE-WAY", "LINE"]),
    ("ykmoxRJ6BOI", f"{AL}/*clue-already-here*.mp4", ["ALREADY", "RECORDED?"]),
    ("f8V6wCjWwHA", f"{AL}/aliens_punch-p01_where-is-everybody_v03_cfr_fixed.mp4", ["ZERO", "SIGNALS"]),
    ("B2STcIAF1lY", f"{BH}/*what-you-would-see*.mp4", ["WHAT YOU'D", "SEE"]),
    # found 25 Aug: public Short absent from the uploads playlist, missed by every audit
    ("tUAdhOnMW2g", f"{BH}/blackhole_nf01_time-appears-to-stop_v03_smooth_normal.mp4", ["TIME", "STOPS"]),
]

TEXT_BOX = (0.05, 0.06, 0.95, 0.26)   # where our punch text lands
CAPTION_BOX = (0.05, 0.52, 0.95, 0.95)  # where the clip's own captions live


def orange_fraction(im):
    """Fraction of pixels that look like Orbit's matte-orange body."""
    px = im.load()
    w, h = im.size
    hit = 0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            if r > 110 and r > g * 1.30 and g > b * 1.10 and (r - b) > 55:
                hit += 1
    return hit / ((w // 2) * (h // 2))


def near_white_fraction(im, box):
    w, h = im.size
    crop = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    g = crop.convert("L")
    px = g.load()
    cw, ch = g.size
    hit = sum(1 for y in range(0, ch, 2) for x in range(0, cw, 2) if px[x, y] > 232)
    return hit / ((cw // 2) * (ch // 2))


def band_stddev(im, box):
    w, h = im.size
    crop = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    return sum(ImageStat.Stat(crop).stddev) / 3


def score(im):
    detail = sum(ImageStat.Stat(im).stddev) / 3
    mean = sum(ImageStat.Stat(im).mean) / 3
    orange = orange_fraction(im)
    centre = orange_fraction(im.crop((int(im.width * 0.2), int(im.height * 0.25),
                                      int(im.width * 0.8), int(im.height * 0.8))))
    caption = near_white_fraction(im, CAPTION_BOX)
    text_busy = band_stddev(im, TEXT_BOX)
    s = (
        min(detail, 60) * 1.0
        - orange * 260
        - centre * 300
        - caption * 900
        - max(0.0, text_busy - 30) * 1.2
    )
    if mean < 12:          # nearly black frame
        s -= 40
    return s, dict(detail=round(detail, 1), orange=round(orange, 4),
                   centre=round(centre, 4), caption=round(caption, 4),
                   text_busy=round(text_busy, 1), mean=round(mean, 1))


def resolve(pattern):
    m = sorted(g for g in glob.glob(pattern) if "_pre_cfr" not in g)
    return m[-1] if m else None


def duration(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", f], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1


def fit_font(d, lines, margin=60, width=1080, start=118, floor=72):
    """Largest size at which the longest line still clears both margins."""
    for size in range(start, floor - 1, -2):
        f = ImageFont.truetype(FONT, size)
        if max(d.textlength(l, font=f) for l in lines) <= width - 2 * margin:
            return f
    return ImageFont.truetype(FONT, floor)


def compose(src, t, lines, dest):
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "f.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", src,
                        "-frames:v", "1", str(raw)], check=True)
        img = Image.open(raw).convert("RGB")
    if img.size != (1080, 1920):
        img = img.resize((1080, 1920), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    fnt = fit_font(d, lines)
    x, y = 60, 130
    for line in lines:
        for dx, dy in [(6, 6), (4, 4)]:
            d.text((x + dx, y + dy), line, font=fnt, fill=(0, 0, 0))
        d.text((x, y), line, font=fnt, fill=(255, 255, 255))
        y = d.textbbox((x, y), line, font=fnt)[3] + 14
    img.save(dest, quality=88)
    if dest.stat().st_size > 2 * 1024 * 1024:
        img.save(dest, quality=75)


def main():
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg not found")
    report = []
    for vid, pattern, lines in JOBS:
        src = resolve(pattern)
        if not src:
            report.append((vid, "NO SOURCE", pattern, None))
            continue
        dur = duration(src)
        if dur <= 0:
            report.append((vid, "NO DURATION", src, None))
            continue
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src,
                            "-vf", "fps=3,scale=216:384", f"{td}/f_%04d.png"], check=True)
            frames = sorted(Path(td).glob("f_*.png"))
            best = None
            for i, fp in enumerate(frames):
                t = i / 3.0
                if t < dur * 0.08 or t > dur * 0.94:
                    continue
                s, dbg = score(Image.open(fp).convert("RGB"))
                if best is None or s > best[0]:
                    best = (s, t, dbg)
        if best is None:
            report.append((vid, "NO FRAME", src, None))
            continue
        dest = OUT / f"cover_{vid}.jpg"
        compose(src, best[1], lines, dest)
        report.append((vid, "ok", Path(src).name, (round(best[1], 2), best[2])))
        print(f"{vid}  t={best[1]:5.2f}s  {best[2]}  ← {Path(src).name}")

    print()
    bad = [r for r in report if r[1] != "ok"]
    print(f"built {len(report) - len(bad)} / {len(report)}")
    for r in bad:
        print("PROBLEM", r[:3])


if __name__ == "__main__":
    main()
