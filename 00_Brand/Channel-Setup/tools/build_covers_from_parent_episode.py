#!/usr/bin/env python3
"""Source Shorts covers from the parent episode when the Short itself is Orbit-dominated.

Some Shorts have Orbit on screen almost end to end, so no frame in the Short
works as a scene-first cover. The cover does not have to come from the Short:
the parent episode is the same topic and full of Orbit-free scenery. This picks
distinct, high-detail, Orbit-free frames from the parent film and composes the
same punch text over them — no re-render, no new generation.

Existing covers are archived to _superseded/ rather than overwritten.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageStat

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from build_scene_first_short_covers import (  # noqa: E402
    FONT, JOBS, compose, orange_fraction,
)

REPO = TOOLS.parents[2]
PROJ = REPO / "02_Video-Projects"
COVERS = REPO / "00_Brand/Channel-Setup/assets/shorts_covers_2026-08-25"
ARCHIVE = COVERS / "_superseded"

# Prefer silent-picture cuts: no burned-in captions to clash with the punch text.
PARENTS = {
    "neutron": PROJ / "007_What-Happens-To-Your-Body-Near-A-Neutron-Star/09_Final-Export/neutron_star_broadcast_v03.mp4",
    "europa": PROJ / "006_Could-Life-Exist-Under-The-Ice-Of-Europa/09_Final-Export/europa_v02_HAND_OPEN_END_UPLOAD.mp4",
    "laststar": PROJ / "005_The-Last-Star-In-The-Universe/07_Edit-Project/_work_v05/picture_silent.mp4",
    "oort": PROJ / "_Experiments/omni-oort-1min-test/04_Master/_work_v02_veo/picture.mp4",
}

# Scheduled Shorts whose own footage is >=55% Orbit-dominated frames.
TARGETS = [
    ("92vmMxSNmlk", "neutron"),
    ("fhJP6eMoU0Q", "neutron"),
    ("SdNXS1PD_Yk", "laststar"),
    ("IVbO9XkkDps", "laststar"),
    ("Fv-lSwB_Z-o", "europa"),
    # k0PjH2I0OxY keeps its own frame: a wide under-ice ocean with a small
    # in-scene Orbit already reads scene-first, and every clean Europa parent
    # frame is either Clipper (taken by KPO68c-U42E) or another ice globe
    # (taken by FbRFvSApfOQ and the Europa long).
    ("Q16DKNvq2OY", "oort"),
    ("oN_jm9PTDOQ", "oort"),
    ("0j_pgYbCe5E", "oort"),
]

# Detail ranking is not topic-aware, so curate where the literal beat is known.
PICKS = {
    "92vmMxSNmlk": 164,   # the neutron star surface itself
    "fhJP6eMoU0Q": 432,   # matter drawn into filaments
    "Fv-lSwB_Z-o": 348,   # plume venting off the ice into space
}

TEXT = {vid: lines for vid, _pat, lines in JOBS}


def vertical_slice(im):
    w, h = im.size
    cw = int(h * 9 / 16)
    return im.crop(((w - cw) // 2, 0, (w + cw) // 2, h))


def candidates(master, step=4, min_detail=34, max_orange=0.012, min_mean=34):
    """Orbit-free, bright, high-detail frames across the parent film, best first.

    min_mean matters: the darkest frames score well on contrast but read as an
    empty black tile at feed size.
    """
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(master),
                        "-vf", f"fps=1/{step},scale=256:144", f"{td}/f_%05d.png"], check=True)
        out = []
        for i, fp in enumerate(sorted(Path(td).glob("f_*.png"))):
            sl = vertical_slice(Image.open(fp).convert("RGB"))
            orange = orange_fraction(sl)
            if orange > max_orange:
                continue
            st = ImageStat.Stat(sl)
            detail = sum(st.stddev) / 3
            mean = sum(st.mean) / 3
            if detail < min_detail or mean < min_mean:
                continue
            out.append({"t": i * step, "orange": orange, "detail": detail,
                        "mean": round(mean, 1)})
    out.sort(key=lambda c: -c["detail"])
    return out


def crop_frame(master, t, dest_png):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(master),
                    "-frames:v", "1", str(dest_png)], check=True)
    im = Image.open(dest_png).convert("RGB")
    vertical_slice(im).resize((1080, 1920), Image.LANCZOS).save(dest_png)


def main():
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    pools, report = {}, []

    for key, master in PARENTS.items():
        if not master.exists():
            print(f"MISSING parent: {key} -> {master}")
            continue
        cands = candidates(master)
        # space picks apart so two Shorts never share a beat
        spaced, last = [], -999
        for c in cands:
            if all(abs(c["t"] - s["t"]) >= 12 for s in spaced):
                spaced.append(c)
        pools[key] = spaced
        print(f"{key}: {len(cands)} clean frames, {len(spaced)} well-spaced")

    for vid, key in TARGETS:
        lines = TEXT.get(vid)
        pool = pools.get(key)
        if not lines or not pool:
            report.append({"vid": vid, "status": "no_pool_or_text"})
            continue
        if vid in PICKS:
            t = PICKS[vid]
            pick = next((c for c in pool if c["t"] == t), {"t": t, "orange": 0.0, "detail": 0.0})
            pool[:] = [c for c in pool if c["t"] != t]
        else:
            pick = pool.pop(0)
        cover = COVERS / f"cover_{vid}.jpg"
        if cover.exists():
            shutil.move(str(cover), str(ARCHIVE / f"cover_{vid}_from-short.jpg"))
        with tempfile.TemporaryDirectory() as td:
            frame = Path(td) / "f.png"
            crop_frame(PARENTS[key], pick["t"], frame)
            compose(str(frame), 0, lines, cover)
        report.append({"vid": vid, "parent": key, "t": pick["t"],
                       "orange_pct": round(pick["orange"] * 100, 2),
                       "detail": round(pick["detail"], 1), "status": "built"})
        print(f"  {vid}  <- {key} t={pick['t']}s  orange={pick['orange']*100:.2f}%  {lines}")

    (COVERS / "PARENT_SOURCED.json").write_text(json.dumps(report, indent=2))
    built = sum(1 for r in report if r["status"] == "built")
    print(f"\nbuilt {built} / {len(TARGETS)} from parent episodes")


if __name__ == "__main__":
    main()
