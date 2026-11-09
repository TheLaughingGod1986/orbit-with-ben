#!/usr/bin/env python3
"""Reproduce and verify PR #575 harvested plates and row composites on MacBook (£0).

Uses SHA-256 verified source assets in /Users/ben/_desk/J2141-plates-source-macbook-v01
and verified overlay graphics on MacBook / NAS. Never overwrites existing output
files. Performs full ffmpeg decode, ffprobe stream/duration/no-audio verification,
near-black luma checks (mean >= 28, p95 >= 50), animated variation checks, and
static frame sampling. Claims no audio or motion perception.
"""
import argparse
import hashlib
import io
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
NAS_CARDS_DIR = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_cards_v01"
)
SOURCE_DIR = Path("/Users/ben/_desk/J2141-plates-source-macbook-v01")
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(args, stdin=None):
    res = subprocess.run(args, input=stdin, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(res.stderr[-2000:].decode(errors="replace"))
    return res.stdout


def probe(path: Path) -> dict:
    out = run([
        "ffprobe", "-v", "error", "-count_frames", "-show_streams",
        "-show_format", "-of", "json", str(path)
    ])
    return json.loads(out)


def luma_stats(im: Image.Image):
    rgb = im.convert("RGB")
    vals = [0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in rgb.getdata()]
    vals.sort()
    return round(sum(vals) / len(vals), 2), round(vals[int(len(vals) * 0.95)], 2)


def make_credit(path: Path, text: str, y: int = 1036, size: int = 28, stroke: bool = False):
    if path.exists():
        return
    im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT_PATH, size)
    if stroke:
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            draw.text((36 + dx, y + dy), text, font=font, fill=(0, 0, 0, 180))
        draw.text((36, y), text, font=font, fill=(255, 255, 255, 220))
    else:
        draw.text((36, y), text, font=font, fill=(255, 255, 255, 210))
    im.save(path)


def make_feather(path: Path, w: int, h: int, rx: int = 50, ry: int = 35):
    if path.exists():
        return
    im = Image.new("L", (w, h))
    px = im.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = int(255 * min(1.0, x / rx, (w - 1 - x) / rx, y / ry, (h - 1 - y) / ry))
    im.save(path)


def render_push_plate(source: Path, dest: Path, credit: Path, crop_box: tuple, frames: int, max_zoom: float, eq_filter: str):
    if dest.exists():
        return
    with Image.open(source) as opened:
        base = opened.convert("RGB").crop(crop_box)
    width, height = base.size
    encoder = subprocess.Popen([
        "ffmpeg", "-v", "error", "-n",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", "25", "-i", "pipe:0",
        "-i", str(credit),
        "-filter_complex", f"[0:v]{eq_filter}[plate];[plate][1:v]overlay=0:0:format=auto[out]",
        "-map", "[out]", "-an", "-frames:v", str(frames),
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-pix_fmt", "yuv420p", "-r", "25", "-movflags", "+faststart", str(dest),
    ], stdin=subprocess.PIPE)
    try:
        for idx in range(frames):
            zoom = 1.0 + max_zoom * idx / (frames - 1)
            cw = width / zoom
            ch = height / zoom
            left = (width - cw) / 2.0
            top = (height - ch) / 2.0
            frame = base.crop((round(left), round(top), round(left + cw), round(top + ch))).resize(
                (1920, 1080), Image.Resampling.LANCZOS
            )
            encoder.stdin.write(frame.tobytes())
    finally:
        encoder.stdin.close()
        rc = encoder.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg push encode failed for {dest.name}: {rc}")


def verify_output(path: Path, expected_duration: float, row: int, source_asset_id: str, source_sha256: str):
    run(["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-f", "null", "-"])
    info = probe(path)
    vs = next(s for s in info["streams"] if s["codec_type"] == "video")
    if any(s["codec_type"] == "audio" for s in info["streams"]):
        raise RuntimeError(f"Audio stream present in {path}")
    if (vs["width"], vs["height"], vs["r_frame_rate"], vs["pix_fmt"]) not in (
        (1920, 1080, "25/1", "yuv420p"),
        (1920, 1080, "25/1", "yuvj420p"),
    ):
        raise RuntimeError(f"Unexpected stream format in {path}: {vs}")
    dur = float(info["format"]["duration"])
    if abs(dur - expected_duration) > 0.045:
        raise RuntimeError(f"Duration mismatch in {path}: {dur} vs {expected_duration}")
    frames = int(vs.get("nb_read_frames") or vs.get("nb_frames") or round(dur * 25))
    samples = []
    sample_times = [round(max(0.08, min(dur - 0.08, dur * frac)), 2) for frac in (0.1, 0.3, 0.5, 0.7, 0.9)]
    for t in sample_times:
        raw = run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(path), "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"])
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        mean_y, p95_y = luma_stats(im)
        if mean_y < 28.0 or p95_y < 50.0:
            raise RuntimeError(f"Near-black fail on {path.name} at {t}s: mean={mean_y}, p95={p95_y}")
        samples.append({
            "time_s": t,
            "mean_luma": mean_y,
            "p95_luma": p95_y,
            "decoded_rgb_sha256": hashlib.sha256(im.tobytes()).hexdigest(),
        })
    distinct_hashes = len({s["decoded_rgb_sha256"] for s in samples})
    if distinct_hashes < 3:
        raise RuntimeError(f"Expected animated variation in {path.name}, got {distinct_hashes} distinct frames")
    return {
        "id": path.stem,
        "row": row,
        "path": str(path),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "source_asset_id": source_asset_id,
        "source_sha256": source_sha256,
        "duration_s": dur,
        "frames": frames,
        "format": f"1920x1080 / 25 fps / {vs['pix_fmt']}",
        "audio": False,
        "full_decode": "PASS",
        "near_black_check": "PASS",
        "distinct_sample_frames": distinct_hashes,
        "samples": samples,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--report", type=Path, required=True)
    args = ap.parse_args()

    out_dir = args.out.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    pool = json.loads((HERE / "HARVEST_POOL_v01.json").read_text())
    assets = {(a.get("asset_id") or a.get("id")): a for a in pool["assets"]}

    def src_file(asset_id: str) -> tuple:
        a = assets[asset_id]
        p = Path(a.get("macbook_local_path") or "")
        if not p.is_file():
            p = SOURCE_DIR / f"{asset_id}__{Path(a['local_path']).name}"
        if not p.is_file():
            raise FileNotFoundError(f"Missing MacBook source for {asset_id}: {p}")
        digest = sha256(p)
        if digest != a["sha256"]:
            raise RuntimeError(f"Source SHA-256 mismatch for {asset_id}")
        return p, digest

    # Verify required overlays
    cards_manifest = json.loads((HERE / "CODE_CARDS_v01.json").read_text())
    cards_by_id = {c["id"]: c for c in cards_manifest["cards"]}
    for cid in ("code_graphic_031_r06_fact_v01", "code_graphic_031_r14_fact_v01", "code_graphic_031_r27_fact_v01"):
        cp = NAS_CARDS_DIR / f"{cid}.mov"
        if sha256(cp) != cards_by_id[cid]["sha256"]:
            raise RuntimeError(f"Card SHA mismatch for {cid}")

    r36_ov = Path("/Users/ben/_desk/J2141-scales-macbook-v01/code_graphic_031_r36_durations_v01.mov")
    scales_mac = json.loads((HERE / "CODE_SCALES_MACBOOK_v01.json").read_text())
    scales_by_id = {g["id"]: g for g in scales_mac["graphics"]}
    if sha256(r36_ov) != scales_by_id["code_graphic_031_r36_durations_v01"]["sha256"]:
        raise RuntimeError("R36 durations overlay SHA mismatch")

    r27_ov = Path("/Users/ben/_desk/J2141-hubble-saa-v01/code_graphic_031_r27_hubble_saa_v01.mov")
    hubble_saa_manifest = json.loads((HERE / "CODE_HUBBLE_SAA_v01.json").read_text())
    if sha256(r27_ov) != hubble_saa_manifest["graphics"][0]["sha256"]:
        raise RuntimeError("R27 hubble_saa overlay SHA mismatch")

    results = []

    # 1. R06 USGS lava plate + FACT card
    usgs_credit = out_dir / "credit_usgs.png"
    make_credit(usgs_credit, "USGS", y=1036, size=28, stroke=False)
    r06_src, r06_sha = src_file("commons_usgs_fissure20_overflight")
    r06_out = out_dir / "plate_031_r06_lava_v01.mp4"
    if not r06_out.exists():
        run([
            "ffmpeg", "-v", "error", "-n", "-i", str(r06_src),
            "-i", str(usgs_credit), "-i", str(NAS_CARDS_DIR / "code_graphic_031_r06_fact_v01.mov"),
            "-filter_complex",
            "[0:v]trim=start=6.0:end=12.68,setpts=PTS-STARTPTS,"
            "crop=1908:900:6:0,scale=2290:1080:flags=lanczos,crop=1920:1080:185:0,"
            "eq=brightness=0.015:saturation=1.05,noise=alls=4:allf=t,fps=25[plate];"
            "[plate][1:v]overlay=0:0:format=auto[graded];"
            "[2:v]setpts=PTS-STARTPTS+4.20/TB[card];"
            "[graded][card]overlay=0:0:eof_action=pass:format=auto[out]",
            "-map", "[out]", "-an", "-frames:v", "167",
            "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            "-pix_fmt", "yuv420p", "-r", "25", "-movflags", "+faststart", str(r06_out)
        ])
    results.append(verify_output(r06_out, 6.68, 6, "commons_usgs_fissure20_overflight", r06_sha))

    # 2. R07 USGS cooling basalt crust push plate
    r07_src, r07_sha = src_file("commons_usgs_kilauea_skylight")
    r07_out = out_dir / "plate_031_r07_crust_v01.mp4"
    render_push_plate(
        r07_src, r07_out, usgs_credit, (0, 270, 5184, 3186), 131, 0.08,
        "eq=brightness=0.012:saturation=1.06,noise=alls=4:allf=t"
    )
    results.append(verify_output(r07_out, 5.24, 7, "commons_usgs_kilauea_skylight", r07_sha))

    # 3. R08 USGS vesicular basalt specimen pan/reframe plate
    usgs_stroke_credit = out_dir / "credit_usgs_stroke.png"
    make_credit(usgs_stroke_credit, "USGS", y=1036, size=28, stroke=True)
    r08_src, r08_sha = src_file("usgs_vesicular_basalt_side")
    r08_out = out_dir / "plate_031_r08_specimen_v04.mp4"
    if not r08_out.exists():
        run([
            "ffmpeg", "-v", "error", "-n",
            "-loop", "1", "-i", str(r08_src),
            "-loop", "1", "-i", str(usgs_stroke_credit),
            "-filter_complex",
            "[0:v]crop=1400:788:x='1800+n+if(gte(n,72),100,0)':y=1420,"
            "scale=1920:1080:flags=lanczos,setsar=1,fps=25,eq=saturation=1.06:brightness=-0.01[p];"
            "[p][1:v]overlay=0:0:shortest=1[out]",
            "-map", "[out]", "-an", "-frames:v", "174",
            "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(r08_out)
        ])
    results.append(verify_output(r08_out, 6.96, 8, "usgs_vesicular_basalt_side", r08_sha))

    # 4. R33 NOAA sediment core push plate
    noaa_credit = out_dir / "credit_noaa.png"
    make_credit(noaa_credit, "Lisa Levin / NOAA", y=1036, size=28, stroke=True)
    r33_src, r33_sha = src_file("noaa_expl2290_tube_core")
    r33_out = out_dir / "plate_031_r33_core_v01.mp4"
    render_push_plate(
        r33_src, r33_out, noaa_credit, (0, 150, 1578, 1038), 111, 0.06,
        "eq=brightness=0.02:saturation=1.08"
    )
    results.append(verify_output(r33_out, 4.44, 33, "noaa_expl2290_tube_core", r33_sha))

    # 5. R45 NPS ammonite fossil push plate
    nps_credit = out_dir / "credit_nps.png"
    make_credit(nps_credit, "Frank Ruggles / NPS", y=1036, size=28, stroke=True)
    r45_src, r45_sha = src_file("nps_katm_pachydiscus_ammonite")
    r45_out = out_dir / "plate_031_r45_fossil_v01.mp4"
    render_push_plate(
        r45_src, r45_out, nps_credit, (40, 300, 3240, 2100), 165, 0.06,
        "eq=brightness=0.02:saturation=1.08"
    )
    results.append(verify_output(r45_out, 6.60, 45, "nps_katm_pachydiscus_ammonite", r45_sha))

    # 6. R41 NASA ISS limb fallback plate
    nasa_credit = out_dir / "credit_nasa.png"
    make_credit(nasa_credit, "NASA", y=1024, size=28, stroke=False)
    r41_src, r41_sha = src_file("eol-sunsetchina-iss-20120413")
    r41_out = out_dir / "plate_031_r41_atmosphere_v02.mp4"
    if not r41_out.exists():
        run([
            "ffmpeg", "-v", "error", "-n", "-ss", "3.6", "-i", str(r41_src),
            "-loop", "1", "-i", str(nasa_credit), "-frames:v", "110",
            "-filter_complex",
            "[0:v:0]setpts=PTS-STARTPTS,crop=1024:576:0:96,scale=1920:1080:flags=lanczos,"
            "eq=brightness=0.015:saturation=1.06,noise=alls=4:allf=t,fps=25[plate];"
            "[plate][1:v:0]overlay=0:0:shortest=1[out]",
            "-map", "[out]", "-an", "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(r41_out)
        ])
    results.append(verify_output(r41_out, 4.40, 41, "eol-sunsetchina-iss-20120413", r41_sha))

    # 7-9. Aurora plates (R04, R36, R50) + 10. R36 composite
    aurora_specs = [
        (4, "eol-europeaurora_iss_20120405", 8.0, 3.44, 64),
        (36, "eol-aurora_iss_20110911", 18.0, 4.88, 192),
        (50, "eol-aurora_iss_20110911", 4.0, 4.00, 192),
    ]
    for row, aid, start, dur, crop_y in aurora_specs:
        asrc, asha = src_file(aid)
        aout = out_dir / f"plate_031_r{row:02d}_aurora_v01.mp4"
        if not aout.exists():
            vf = (
                f"crop=1024:576:0:{crop_y},scale=1920:1080:flags=lanczos,"
                "eq=brightness=0.015:saturation=1.04,noise=alls=4:allf=t,fps=25"
            )
            run([
                "ffmpeg", "-v", "error", "-n", "-ss", str(start), "-i", str(asrc),
                "-loop", "1", "-i", str(nasa_credit), "-t", str(dur),
                "-filter_complex", f"[0:v:0]{vf}[plate];[plate][1:v:0]overlay=0:0:shortest=1[out]",
                "-map", "[out]", "-an", "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(aout)
            ])
        results.append(verify_output(aout, dur, row, aid, asha))

    r36_comp = out_dir / "composite_031_r36_durations_v02.mp4"
    if not r36_comp.exists():
        run([
            "ffmpeg", "-v", "error", "-n",
            "-i", str(out_dir / "plate_031_r36_aurora_v01.mp4"),
            "-i", str(r36_ov),
            "-filter_complex", "[0:v][1:v]overlay=-950:-300:shortest=1[out]",
            "-map", "[out]", "-an", "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(r36_comp)
        ])
    _, r36_sha = src_file("eol-aurora_iss_20110911")
    results.append(verify_output(r36_comp, 4.88, 36, "eol-aurora_iss_20110911", r36_sha))

    # 11-12. Solar plates (R14, R46) + 13. R14 composite
    sdo_credit = out_dir / "credit_nasa_sdo.png"
    make_credit(sdo_credit, "NASA/SDO", y=1024, size=28, stroke=True)
    solar_specs = [
        (14, "svs-3693-sdo-launching-filament", 6.0, 2.42, 2.44, (320, 0, 1600, 900)),
        (46, "svs-12706-sdo-x8-flare-171-304", 9.0, 2.34, 2.36, (0, 0, 1920, 1080)),
    ]
    for row, aid, start, dur, enc_dur, (cx, cy, cw, ch) in solar_specs:
        ssrc, ssha = src_file(aid)
        sout = out_dir / f"plate_031_r{row:02d}_solar_v01.mp4"
        if not sout.exists():
            vf = (
                f"crop={cw}:{ch}:{cx}:{cy},scale=1920:1080:flags=lanczos,"
                "eq=brightness=0.01:saturation=1.02,noise=alls=4:allf=t,fps=25"
            )
            run([
                "ffmpeg", "-v", "error", "-n", "-ss", str(start), "-i", str(ssrc),
                "-loop", "1", "-i", str(sdo_credit), "-t", str(dur),
                "-filter_complex", f"[0:v:0]{vf}[p];[p][1:v]overlay=0:0:shortest=1[out]",
                "-map", "[out]", "-an", "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(sout)
            ])
        results.append(verify_output(sout, enc_dur, row, aid, ssha))

    r14_comp = out_dir / "composite_031_r14_fact_v01.mp4"
    if not r14_comp.exists():
        run([
            "ffmpeg", "-v", "error", "-n",
            "-i", str(out_dir / "plate_031_r14_solar_v01.mp4"),
            "-i", str(NAS_CARDS_DIR / "code_graphic_031_r14_fact_v01.mov"),
            "-filter_complex", "[1:v]setpts=PTS-STARTPTS+0.48/TB[label];[0:v][label]overlay=0:-720:eof_action=pass:repeatlast=0[out]",
            "-map", "[out]", "-an", "-t", "2.44",
            "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(r14_comp)
        ])
    _, r14_sha = src_file("svs-3693-sdo-launching-filament")
    results.append(verify_output(r14_comp, 2.44, 14, "svs-3693-sdo-launching-filament", r14_sha))

    # 14-15. R27 Hubble plates (approach_v01, release_v03) + 16-17. R27 composites (orbits_v02, pause_v02)
    hubble_src, hubble_sha = src_file("svs-13160-sts125-sm4-highlights")
    feather_1440 = out_dir / "feather_1440x1080.png"
    make_feather(feather_1440, 1440, 1080, 50, 35)
    nasa_stroke = out_dir / "credit_nasa_stroke.png"
    make_credit(nasa_stroke, "NASA", y=1024, size=30, stroke=True)

    hubble_plate_specs = [
        ("plate_031_r27_approach_v01.mp4", 112.0, 4.00, "crop=960:720:160:0"),
        ("plate_031_r27_release_v03.mp4", 661.0, 3.48, "crop=928:696:176:12"),
    ]
    for fname, start, dur, crop_expr in hubble_plate_specs:
        hout = out_dir / fname
        if not hout.exists():
            filt = (
                f"{crop_expr},split=2[fg][bg];"
                "[bg]scale=1920:1440:flags=lanczos,crop=1920:1080,boxblur=40:2[b];"
                "[fg]scale=1440:1080:flags=lanczos,setsar=1[f];"
                "[1:v]format=gray[m];[f][m]alphamerge[fa];"
                "[b][fa]overlay=240:0:shortest=1,eq=brightness=0.015:saturation=1.02,noise=alls=4:allf=t,fps=25[p];"
                "[p][2:v]overlay=0:0:shortest=1[out]"
            )
            run([
                "ffmpeg", "-v", "error", "-n", "-ss", str(start), "-i", str(hubble_src),
                "-loop", "1", "-i", str(feather_1440), "-loop", "1", "-i", str(nasa_stroke),
                "-t", str(dur), "-filter_complex", filt, "-map", "[out]", "-an",
                "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(hout)
            ])
        results.append(verify_output(hout, dur, 27, "svs-13160-sts125-sm4-highlights", hubble_sha))

    feather_1080 = out_dir / "feather_1080x810.png"
    make_feather(feather_1080, 1080, 810, 50, 35)
    hubble_comp_specs = [
        ("composite_031_r27_orbits_v02.mp4", 116.0, 4.32, 108, r27_ov, 0.0, 0, 135),
        ("composite_031_r27_pause_v02.mp4", 668.8, 4.28, 107, NAS_CARDS_DIR / "code_graphic_031_r27_fact_v01.mov", 0.02, 840, 0),
    ]
    for fname, start, dur, nframes, ov_path, ov_delay, fg_x, fg_y in hubble_comp_specs:
        cout = out_dir / fname
        if not cout.exists():
            filt = (
                "[0:v]setpts=PTS-STARTPTS,crop=928:696:176:12,fps=25,split=2[fg][bg];"
                "[bg]scale=1920:1440:flags=lanczos,crop=1920:1080,boxblur=40:2[b];"
                "[fg]scale=1080:810:flags=lanczos,setsar=1[f];"
                "[1:v]format=gray[m];[f][m]alphamerge[fa];"
                f"[b][fa]overlay={fg_x}:{fg_y}:shortest=1,eq=brightness=0.015:saturation=1.02,noise=alls=4:allf=t[p];"
                f"[2:v]setpts=PTS-STARTPTS+{ov_delay}/TB[o];[p][o]overlay=0:0:eof_action=pass[q];"
                "[q][3:v]overlay=0:0:shortest=1[out]"
            )
            run([
                "ffmpeg", "-v", "error", "-n", "-ss", str(start), "-i", str(hubble_src),
                "-loop", "1", "-i", str(feather_1080), "-i", str(ov_path), "-loop", "1", "-i", str(nasa_stroke),
                "-filter_complex", filt, "-map", "[out]", "-an", "-frames:v", str(nframes),
                "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(cout)
            ])
        results.append(verify_output(cout, dur, 27, "svs-13160-sts125-sm4-highlights", hubble_sha))

    # Build contact sheet of all 17 reproduced plates/composites
    cols = 4
    rows_grid = (len(results) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 480, rows_grid * 300), (18, 24, 36))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(FONT_PATH, 20)
    for idx, rec in enumerate(results):
        mid_t = round(rec["duration_s"] * 0.5, 2)
        raw = run(["ffmpeg", "-v", "error", "-ss", str(mid_t), "-i", rec["path"], "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"])
        thumb = Image.open(io.BytesIO(raw)).convert("RGB").resize((464, 261), Image.Resampling.LANCZOS)
        gx = (idx % cols) * 480 + 8
        gy = (idx // cols) * 300 + 8
        sheet.paste(thumb, (gx, gy))
        draw.text((gx + 4, gy + 265), f"R{rec['row']:02d} {rec['id']} ({rec['duration_s']:.2f}s)", font=font, fill=(235, 240, 250))

    contact_path = out_dir / "CONTACT_PLATES_MACBOOK_v01.jpg"
    sheet.save(contact_path, quality=92)

    manifest_data = {
        "job": "J2141",
        "worker": "macbook",
        "spend_gbp": 0,
        "status": "macbook_reproduced_plates_and_composites_not_KEEP",
        "source_dir": str(SOURCE_DIR),
        "output_dir": str(out_dir),
        "contact_sheet": str(contact_path),
        "contact_sheet_sha256": sha256(contact_path),
        "plates_and_composites": results,
    }
    args.manifest.write_text(json.dumps(manifest_data, indent=2) + "\n")

    report_data = {
        "job": "J2141",
        "worker": "macbook",
        "spend_gbp": 0,
        "scope": "MacBook reproduction and verification of all 17 PR #575 harvested plates and row composites (R04, R06, R07, R08, R14, R27, R33, R36, R41, R45, R46, R50)",
        "technical_checks": "PASS",
        "near_black_all_17": "PASS",
        "actual_audio_review": False,
        "actual_motion_review": False,
        "count": len(results),
        "contact_sheet": str(contact_path),
        "contact_sheet_sha256": sha256(contact_path),
        "checks": results,
    }
    args.report.write_text(json.dumps(report_data, indent=2) + "\n")
    print(f"Verified {len(results)} plates and composites in {out_dir}")


if __name__ == "__main__":
    main()
