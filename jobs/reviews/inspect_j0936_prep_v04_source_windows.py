#!/usr/bin/env python3
import hashlib, json, re, shutil, subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
MAPS_V03 = ROOT / "jobs/reviews/J0936_v04_PREP_v03_maps.json"
OUT_DIR = Path("/Users/benjaminoats/_desk/reviews/J1015/source_windows")
OUT_DIR.mkdir(parents=True, exist_ok=True)
J1017_DIR = Path("/Users/benjaminoats/_desk/reviews/J1017/source_windows")
J1017_DIR.mkdir(parents=True, exist_ok=True)

data = json.loads(MAPS_V03.read_text())

# Update S1 s00, s01, s_loop to the reconciled center_086 gold Sun opening + close-up flare s01
s1_shots = data["shorts"]["S1_026_A6TW_6CXhcs"]["shot_plan"]
c86_path = "/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-10/nearest026_rough_work_v05b/center_086.mp4"
c86_sha = hashlib.sha256(Path(c86_path).read_bytes()).hexdigest()
s1_shots[0].update({
    "row": "s00_sdo_gold_sun",
    "asset_key": "026_center_086",
    "underlying_id": "GSFC_20160426_SDO_m12224_SolarFlare.mp4",
    "source_path": c86_path,
    "source_in": 0.100,
    "source_out": 2.480,
    "source_dur": 2.380,
    "source_speed": 1.00,
    "upscale": 2.08,
    "crop_filter": "crop=520:924:680+38*t:78,eq=brightness=0.06:contrast=1.14:saturation=1.12,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
    "source_sha256": c86_sha,
})
s1_shots[1].update({
    "row": "s01_sdo_flare_limb",
    "asset_key": "028_sdo_solar_flare",
    "underlying_id": "sdo_solar_flare.mp4",
    "source_path": "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/nasa_pool_v01/028_harvest_v01/sdo_solar_flare.mp4",
    "source_in": 24.200,
    "source_out": 26.120,
    "source_dur": 1.920,
    "source_speed": 1.00,
    "upscale": 1.78,
    "crop_filter": "crop=608:1080:656:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
})
s1_shots[-1].update({
    "row": "s_loop",
    "asset_key": "026_center_086",
    "underlying_id": "loop_GSFC_20160426_SDO_m12224_SolarFlare.mp4",
    "source_path": f"reversed first 1.000s of s00 ({c86_path})",
    "source_in": 1.100,
    "source_out": 0.100,
    "source_dur": 1.000,
    "source_speed": 1.00,
    "upscale": 2.08,
    "source_sha256": c86_sha,
})

# Update S4 s02_sdo_sun to 51.000-54.553s (clean gold 171A/193A window with zero internal wavelength change)
s4_shots = data["shorts"]["S4_028_DETI0HV2jlI"]["shot_plan"]
s4_shots[1].update({
    "source_in": 51.000,
    "source_out": 54.553,
    "source_dur": 3.553,
    "source_speed": 1.00,
    "upscale": 1.78,
    "crop_filter": "crop=608:1080:656:0,eq=brightness=0.02:contrast=1.08:saturation=1.08,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
})

# Explicit 9:16 crop filters for every body shot
DEFAULT_CROP_916 = "crop=ih*9/16:ih,scale=180:320:flags=area,fps=30"

tess = shutil.which("tesseract") or "/opt/homebrew/bin/tesseract"
BANNED_RE = re.compile(
    r"(https?://|www\.|\.int\b|\.gov\b|esa\.int|copyright|all rights reserved|tycho|brahe|"
    r"shrinking|grapefruit|cherry|4,000|equator|gliese|sirius|million|light-year|centimeter|neptune)",
    re.I,
)

def inspect_shot(sid, s):
    if s["row"] == "s_loop":
        return None
    src = Path(s["source_path"])
    if not src.is_absolute():
        src = ROOT / src
    sin, sout = float(s["source_in"]), float(s["source_out"])
    sdur = round(sout - sin, 3)

    # 1. Decode ALL frames at 30fps across [sin, sout] in the 9:16 center crop (180x320 gray)
    # For S1 s00, use its 520:924 crop; for S3 s01 use x=1300; for S4 s01 use x=450..; for S5 s01 use x=620..; for S6 s01 use x=500..
    vf_gray = "crop=ih*9/16:ih,scale=180:320:flags=area,fps=30,format=gray"
    if sid == "S1_026_A6TW_6CXhcs" and s["row"] == "s00_sdo_gold_sun":
        vf_gray = "crop=520:924:680+38*t:78,eq=brightness=0.06:contrast=1.14:saturation=1.12,scale=180:320:flags=area,fps=30,format=gray"
    elif sid == "S3_028_bizlhspnVvY" and s["row"] == "s01_lasilla_ntt":
        vf_gray = "crop=608:1080:1300:0,eq=contrast=1.12:saturation=1.08,scale=180:320:flags=area,fps=30,format=gray"
    elif sid == "S4_028_DETI0HV2jlI" and s["row"] == "s01_paranal_mw_open":
        vf_gray = "crop=608:1080:450+63*t:0,eq=brightness=0.04:contrast=1.10:saturation=1.12,scale=180:320:flags=area,fps=30,format=gray"
    elif sid == "S5_028_jJ5LkFGyzLI" and s["row"] == "s01_sdo_sun_open":
        vf_gray = "crop=608:1080:590+40*t:0,scale=180:320:flags=area,fps=30,format=gray"
    elif sid == "S6_028_X768qs8sNQs" and s["row"] == "s01_lasilla_mw_open":
        vf_gray = "crop=608:1080:500+55*t:0,eq=brightness=0.06:contrast=1.10:saturation=1.15,scale=180:320:flags=area,fps=30,format=gray"

    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{sin:.3f}", "-t", f"{sdur:.3f}",
        "-i", str(src), "-vf", vf_gray, "-f", "rawvideo", "-"
    ])
    n_px = 180 * 320
    n_frames = len(raw) // n_px
    frames = np.frombuffer(raw[:n_frames * n_px], dtype=np.uint8).reshape(n_frames, n_px)
    lumas = frames.mean(axis=1)
    blks20 = (frames < 20).mean(axis=1)
    blks30 = (frames < 30).mean(axis=1)

    # Dark-run check: consecutive frames with >85% pixels < 20 luma
    dark_flags = blks20 > 0.85
    run_len = max_dark_run = 0
    for fl in dark_flags:
        if fl:
            run_len += 1
            max_dark_run = max(max_dark_run, run_len)
        else:
            run_len = 0

    # 2. Internal scene-cut check via scdet across complete [sin, sout]
    sc_err = subprocess.run([
        "ffmpeg", "-v", "info", "-nostats", "-ss", f"{sin:.3f}", "-t", f"{sdur:.3f}",
        "-i", str(src), "-vf", "crop=ih*9/16:ih,scale=72:128:flags=area,scdet=threshold=12:sc_pass=1",
        "-an", "-f", "null", "-"
    ], capture_output=True, text=True, errors="replace").stderr
    internal_cuts = [round(float(m.group(1)), 3) for m in re.finditer(r"lavfi\.scd\.time:\s*([0-9.]+)", sc_err) if float(m.group(1)) > 0.10]

    # 3. Dense 2fps (every 0.50s) frame extraction + Tesseract OCR across the complete window
    sample_offsets = list(np.arange(0.05, max(0.06, sdur - 0.04), 0.50))
    if not sample_offsets or abs(sample_offsets[-1] - (sdur - 0.08)) > 0.20:
        sample_offsets.append(max(0.05, round(sdur - 0.08, 3)))
    sample_times = [round(sin + off, 3) for off in sample_offsets]

    ocr_dir = Path(f"/tmp/ocr_win_{sid}_{s['row']}")
    if ocr_dir.exists():
        shutil.rmtree(ocr_dir)
    ocr_dir.mkdir(parents=True)

    vf_ocr = vf_gray.replace("180:320:flags=area,fps=30,format=gray", "360:640:flags=lanczos")
    ocr_records = []
    banned_hits = []
    tiles = []
    for idx_t, st in enumerate(sample_times):
        jpg_p = ocr_dir / f"f_{idx_t:02d}.jpg"
        rel_t = max(0.0, st - sin)
        vf_frame = re.sub(r"\*t\b", f"*{rel_t:.3f}", vf_ocr)
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-ss", f"{st:.3f}", "-i", str(src),
            "-frames:v", "1", "-vf", vf_frame, "-q:v", "3", str(jpg_p)
        ], check=True)
        got = subprocess.run([tess, str(jpg_p), "stdout", "--psm", "6", "-l", "eng"], capture_output=True, text=True, errors="replace")
        txt = re.sub(r"\s+", " ", (got.stdout or "")).strip()
        # Filter single-char/punctuation noise from star fields
        alpha_words = [w for w in re.findall(r"[A-Za-z]{3,}", txt)]
        if BANNED_RE.search(txt):
            banned_hits.append({"source_t": st, "ocr": txt})
        ocr_records.append({"source_t": st, "raw_ocr": txt, "alpha_3plus_words": alpha_words})
        tiles.append((st, jpg_p))

    return {
        "short_id": sid,
        "row": s["row"],
        "source_path": s["source_path"],
        "source_in": sin,
        "source_out": sout,
        "source_dur": sdur,
        "frames_decoded_30fps": int(n_frames),
        "start_mean_luma": round(float(lumas[0]), 2),
        "midpoint_mean_luma": round(float(lumas[len(lumas)//2]), 2),
        "end_mean_luma": round(float(lumas[-1]), 2),
        "window_min_luma": round(float(lumas.min()), 2),
        "window_max_luma": round(float(lumas.max()), 2),
        "window_mean_luma": round(float(lumas.mean()), 2),
        "start_black_frac": round(float(blks20[0]), 4),
        "midpoint_black_frac": round(float(blks20[len(blks20)//2]), 4),
        "end_black_frac": round(float(blks20[-1]), 4),
        "window_min_black_frac": round(float(blks20.min()), 4),
        "window_max_black_frac": round(float(blks20.max()), 4),
        "window_mean_black_frac": round(float(blks20.mean()), 4),
        "window_max_black30_frac": round(float(blks30.max()), 4),
        "dark_run_max_consecutive_frames": int(max_dark_run),
        "internal_scdet_cuts": internal_cuts,
        "ocr_2fps_sample_count": len(sample_times),
        "ocr_2fps_timestamps_s": sample_times,
        "ocr_banned_hits": banned_hits,
        "ocr_records": ocr_records,
        "clean_window_verified": (max_dark_run < 3 and len(internal_cuts) == 0 and len(banned_hits) == 0),
        "_tiles": tiles,
    }

tasks = []
for sid, sdata in data["shorts"].items():
    for s in sdata["shot_plan"]:
        if s["row"] != "s_loop":
            tasks.append((sid, s))

print(f"Inspecting {len(tasks)} body shots across full windows...")
with ThreadPoolExecutor(max_workers=6) as ex:
    results = list(ex.map(lambda p: inspect_shot(*p), tasks))

total_30fps = sum(r["frames_decoded_30fps"] for r in results)
total_2fps = sum(r["ocr_2fps_sample_count"] for r in results)
any_fails = [r for r in results if not r["clean_window_verified"]]
print(f"Done! Decoded {total_30fps} 30fps frames and OCR-scanned {total_2fps} 2fps frames across {len(results)} body shots. Fails: {len(any_fails)}")
for r in any_fails:
    print("FAIL:", r["short_id"], r["row"], "dark_run=", r["dark_run_max_consecutive_frames"], "cuts=", r["internal_scdet_cuts"], "banned=", r["ocr_banned_hits"])

# Build per-Short 2fps full-window contact sheets and master contact sheet
TW, TH = 135, 240
all_rows_imgs = []
for sid in data["shorts"]:
    s_res = [r for r in results if r["short_id"] == sid]
    max_cols = max(len(r["_tiles"]) for r in s_res)
    sheet = Image.new("RGB", (max_cols * TW, len(s_res) * (TH + 22)), (12, 12, 16))
    draw = ImageDraw.Draw(sheet)
    for r_i, r in enumerate(s_res):
        y0 = r_i * (TH + 22)
        hdr = f"{sid[:6]} {r['row']} [{r['source_in']:.2f}-{r['source_out']:.2f}s] {r['frames_decoded_30fps']}f luma={r['window_min_luma']:.0f}..{r['window_max_luma']:.0f} blk={r['window_max_black_frac']*100:.1f}% cuts={len(r['internal_scdet_cuts'])} ocr_hits={len(r['ocr_banned_hits'])}"
        draw.text((4, y0 + 3), hdr, fill=(230, 230, 230))
        for c_i, (st, jp) in enumerate(r["_tiles"]):
            im = Image.open(jp).resize((TW - 2, TH - 2))
            sheet.paste(im, (c_i * TW + 1, y0 + 21))
            draw.text((c_i * TW + 4, y0 + 24), f"{st:.2f}s", fill=(255, 214, 0))
    sp = OUT_DIR / f"{sid}_full_window_2fps.jpg"
    sheet.save(sp, quality=88)
    shutil.copy2(sp, J1017_DIR / sp.name)
    all_rows_imgs.append(sheet)

# Stack all 6 Short sheets into all_shots_full_window_2fps.jpg
max_w = max(im.width for im in all_rows_imgs)
tot_h = sum(im.height for im in all_rows_imgs)
master = Image.new("RGB", (max_w, tot_h), (12, 12, 16))
yc = 0
for im in all_rows_imgs:
    master.paste(im, (0, yc))
    yc += im.height
mp = OUT_DIR / "all_shots_full_window_2fps.jpg"
master.save(mp, quality=85)
shutil.copy2(mp, J1017_DIR / mp.name)
shutil.copy2(mp, OUT_DIR / "all_shots_start_mid_end.jpg")

# Strip _tiles before saving JSON
clean_results = []
for r in results:
    rc = dict(r)
    rc.pop("_tiles", None)
    clean_results.append(rc)

log_obj = {
    "method": "Complete source-window inspection: 100% of frames decoded at 30 fps across [source_in, source_out] for luma, black fraction (<20 and <30), dark-run (<20 luma on >85% area), and ffmpeg scdet internal cut detection, plus dense 2 fps (every 0.50 s) frame extraction and Tesseract OCR (--psm 6 -l eng) across the entire window of all 43 body shots.",
    "total_body_shots": len(clean_results),
    "total_30fps_frames_decoded": total_30fps,
    "total_2fps_ocr_frames_scanned": total_2fps,
    "any_failures": len(any_fails),
    "shots": clean_results,
}
log_path = OUT_DIR / "full_window_inspection_log.json"
log_path.write_text(json.dumps(log_obj, indent=2) + "\n")
shutil.copy2(log_path, J1017_DIR / log_path.name)
print("Saved log and sheets to:", OUT_DIR, "and", J1017_DIR)
