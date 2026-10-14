#!/usr/bin/env python3
"""Sun 022 Shorts: covers + upload packages for Mon 19 / Wed 21 / Fri 23 Oct (J0033).

Covers use build_yellow_white_short_thumbs_v04.compose() on clean NASA plates (no burned-in captions, no Orbit).
Packages follow the Saturn 021 Short layout. The Sun long has no YouTube id yet, so relatedVideoId and the
long's link are added once it is uploaded (LONG_ID below). Does not upload or schedule.

  python3 02_Video-Projects/022_Is-the-Sun-Getting-Brighter/10_Shorts/_build_sun_shorts_packages_v01.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

HERE = Path(__file__).resolve().parent
FILM = HERE.parent
ROOT = FILM.parents[1]
sys.path.insert(0, str(ROOT / "00_Brand/Channel-Setup/tools"))
import build_yellow_white_short_thumbs_v04 as v04  # noqa: E402

LONG_TITLE = "Is the Sun Getting Brighter?"
LONG_ID = ""  # set once the Sun long is uploaded
SVS = FILM / "04_Generated-Clips/svs"


def frame(src: Path, t: float, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(src), "-frames:v", "1", "-q:v", "2", str(out)],
        check=True,
    )
    return out


def young_sun_plate(out: Path) -> Path:
    """Dim, cold-graded SDO disc (PIA21218) over the ISS sea (iss017e011603, top 60%)."""
    sea = Image.open(HERE / "fri23_dimmer_sun/out_nasa/iss017e011603.jpg").convert("RGB")
    sea = sea.crop((0, 0, sea.width, int(sea.height * 0.60)))
    W, H = 1440, 2560
    plate = Image.new("RGB", (W, H), (0, 0, 0))
    sea_h = int(H * 0.42)
    sea_w = int(sea.width * sea_h / sea.height)
    sea = sea.resize((sea_w, sea_h), Image.Resampling.LANCZOS)
    x0 = max(0, (sea_w - W) // 2)
    sea = sea.crop((x0, 0, x0 + W, sea_h))
    sea = ImageEnhance.Brightness(sea).enhance(1.15)
    plate.paste(sea, (0, H - sea_h))
    disc = Image.open(FILM / "07_Edit-Project/nasa_pool_v01/S2/PIA21218.jpg").convert("L")
    # Find the limb from the bright pixels so the corner date stamp falls outside the circular mask.
    bbox = disc.point(lambda v: 255 if v > 40 else 0).getbbox()
    cx, cy = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2
    r = int(min(bbox[2] - bbox[0], bbox[3] - bbox[1]) / 2 * 0.98)
    disc = disc.crop((cx - r, cy - r, cx + r, cy + r))
    d = int(W * 0.78)
    disc = disc.resize((d, d), Image.Resampling.LANCZOS)
    disc = ImageOps.colorize(disc, black=(0, 0, 0), white=(235, 150, 70), mid=(120, 60, 25))
    disc = ImageEnhance.Brightness(disc).enhance(0.75)
    mask = Image.new("L", (d, d), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, d - 1, d - 1), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(3))
    plate.paste(disc, ((W - d) // 2, int(H * 0.14)), mask)
    out.parent.mkdir(parents=True, exist_ok=True)
    plate.save(out, quality=95)
    return out


SHORTS = [
    {
        "key": "mon19_brighter_fuel",
        "video": "06_Final-Exports/mon19_brighter_fuel_short_v02.mp4",
        "title": "Why Is the Sun Getting Brighter as It Runs Out of Fuel?",
        "schedule": "2026-10-19T10:30:00.000Z",
        "plate": lambda d: frame(SVS / "svs13778.mp4", 91.0, d / "_plate_svs13778_91s.jpg"),
        "lines": ["IT BURNS", "HARDER"],
        "yellow": {"HARDER"},
        "hero": 1,
        "credits": [
            "SVS 13778: NASA's Goddard Space Flight Center / SDO (https://svs.gsfc.nasa.gov/13778)",
        ],
        "tags": ["sun getting brighter", "is the sun getting brighter", "sun running out of fuel",
                 "nuclear fusion sun core", "sun", "space documentary"],
        "social": {
            "hook": "The Sun is running out of fuel, and it's getting brighter because of it.",
            "question": "Did you know the Sun was brighter today than when the dinosaurs lived?",
            "alt": "The Sun's disc with a prominence lifting off its edge, captioned IT'S BRIGHTER.",
        },
    },
    {
        "key": "wed21_robot_sun",
        "video": "06_Final-Exports/wed21_robot_sun_short_v01.mp4",
        "title": "Could a Robot Survive Touching the Sun?",
        "schedule": "2026-10-21T10:30:00.000Z",
        "plate": lambda d: frame(SVS / "svs14036_psp_alfven.mp4", 7.0, d / "_plate_svs14036_7s.jpg"),
        "lines": ["1,400°C", "SHIELD"],
        "yellow": {"1,400°C"},
        "hero": 0,
        "credits": None,  # from the meta JSON
        "tags": ["parker solar probe", "touching the sun", "parker solar probe heat shield",
                 "closest to the sun", "sun", "space documentary"],
        "social": {
            "hook": "Nothing we've built has flown this close to the Sun.",
            "question": "Would you send a probe closer still?",
            "alt": "NASA's Parker Solar Probe crossing the Sun's corona, captioned TOO CLOSE.",
        },
    },
    {
        "key": "fri23_dimmer_sun",
        "video": "06_Final-Exports/fri23_dimmer_sun_short_v02.mp4",
        "title": "Why Didn't Earth Freeze Under a Dimmer Young Sun?",
        "schedule": "2026-10-23T10:30:00.000Z",
        "plate": lambda d: young_sun_plate(d / "_plate_young_sun.jpg"),
        "lines": ["FROZEN?", "IT WASN'T"],
        "yellow": {"FROZEN"},
        "hero": 0,
        "credits": [
            "PIA21218 'Spotless February': NASA/SDO (https://images.nasa.gov/details/PIA21218)",
            "iss017e011603: NASA (https://images.nasa.gov/details/iss017e011603)",
            "GSFC_20171208_Archive_e002130: NASA Goddard (https://images.nasa.gov/details/GSFC_20171208_Archive_e002130)",
            "GSFC_20171208_Archive_e000888: NASA Goddard (https://images.nasa.gov/details/GSFC_20171208_Archive_e000888)",
            "iss071e439624: NASA (https://images.nasa.gov/details/iss071e439624)",
        ],
        "tags": ["faint young sun paradox", "young sun", "early earth", "why didn't earth freeze",
                 "sun getting brighter", "space documentary"],
        "social": {
            "hook": "Four billion years ago the Sun was about 30% dimmer. Earth should have frozen.",
            "question": "What do you think kept early Earth warm?",
            "alt": "A dim young Sun over a dark early sea, captioned 30% DIMMER.",
        },
    },
]


def description(s: dict, credits: list[str]) -> str:
    lines = [LONG_TITLE]
    if LONG_ID:
        lines.append(f"https://www.youtube.com/watch?v={LONG_ID}")
    lines += ["", "Credits:"] + credits
    return "\n".join(lines) + "\n"


def main() -> None:
    results = []
    for s in SHORTS:
        sd = HERE / s["key"]
        covers = sd / "08_Covers"
        plate = s["plate"](covers)
        cover = v04.compose({
            "id": s["key"], "plate": plate, "lines": s["lines"], "yellow": s["yellow"], "hero": s["hero"],
            "out_dir": covers, "related": LONG_ID, "uk": "", "role": "sun_022_short",
        })
        credits = s["credits"] or json.loads((sd / s["video"].replace(".mp4", "_meta.json")).read_text())["credits"]
        manifest = {
            "format": "shorts",
            "title": s["title"],
            "description": description(s, credits),
            "tags": s["tags"],
            "schedule": s["schedule"],
            **({"relatedVideoId": LONG_ID} if LONG_ID else {}),
            "privacy": "private",
            "madeForKids": False,
            "thumbnail": cover["file"],
            "social": s["social"],
        }
        pkg = sd / "11_Upload-Package"
        pkg.mkdir(parents=True, exist_ok=True)
        (pkg / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        results.append({"short": s["key"], "cover": cover["file"], "package": str(pkg), "video": str(sd / s["video"])})
    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
