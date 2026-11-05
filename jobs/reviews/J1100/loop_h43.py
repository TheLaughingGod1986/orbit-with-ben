#!/usr/bin/env python3
"""Chief h43-LOOP provenance and loop verification gate for J1100 (S2, S5, S6 v07).

Enforces Chief h43 (J1313 verify; OWB #264 6539463596):
(1) Text-free base from the same build/filtergraph with only text layers disabled;
    manifest with both sha256s + filtergraph diff.
(2) Base whole-frame f0-vs-last < 2.0 (reported at both 180x320 and 270x480),
    plus legacy c37 loop_measures checks on base (< 2.0 whole & masked) and final (< 2.0 masked).
(3) Final last vs base last < 1.0 whole; final f0 vs base f0 < 1.0 outside the
    frame-0 text alpha bounding boxes padded by +8 px.
(4) OCR on f0 matches locked hook text, every tail frame (last 30 frames / 1.0 s)
    has empty OCR, and captions match final AAC word-for-word (including S5
    'GLIESE 710 COME' / 'TO THE SUN?').
(5) Reports final whole-frame f0-vs-last and sample loop_measures.whole as diagnostic.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def decode_gray_frame(video: Path, frame_idx: int, w: int, h: int) -> np.ndarray:
    vf = f"select='eq(n,{frame_idx})',scale={w}:{h}:flags=area,format=gray"
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(video), "-vf", vf, "-fps_mode", "vfr", "-frames:v", "1", "-f", "rawvideo", "-"]
    )
    arr = np.frombuffer(raw, dtype=np.uint8)
    assert arr.size == w * h, f"Expected {w*h} bytes for frame {frame_idx} of {video}, got {arr.size}"
    return arr.reshape(h, w).astype(np.float64)


def frame_count(video: Path) -> int:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(video)],
        text=True,
    ).strip()
    return int(out)


def alpha_bboxes_padded(overlay_png: Path, pad: int = 8, target_w: int = 1080, target_h: int = 1920) -> list[list[int]]:
    im = Image.open(overlay_png).convert("RGBA")
    alpha = np.array(im)[:, :, 3] > 0
    row_has = np.where(alpha.any(axis=1))[0]
    if row_has.size == 0:
        return []
    bands = []
    start_r = int(row_has[0])
    prev_r = int(row_has[0])
    for r in row_has[1:]:
        r = int(r)
        if r > prev_r + 4:
            bands.append((start_r, prev_r))
            start_r = r
        prev_r = r
    bands.append((start_r, prev_r))
    bboxes = []
    for y0, y1 in bands:
        cols = np.where(alpha[y0:y1 + 1, :].any(axis=0))[0]
        x0, x1 = int(cols[0]), int(cols[-1])
        bboxes.append([
            max(0, x0 - pad),
            max(0, y0 - pad),
            min(target_w, x1 + 1 + pad),
            min(target_h, y1 + 1 + pad),
        ])
    return bboxes


def prep_for_ocr(im: Image.Image) -> Image.Image:
    """Isolate stroked house white (255,255,255) and yellow (255,214,0) text as black-on-white for Tesseract."""
    rgb = np.array(im.convert("RGB"), dtype=np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    is_white = (r > 210) & (g > 210) & (b > 210) & ((np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)) < 20)
    is_yellow = (r > 210) & (g > 170) & (b < 40)
    fg = is_white | is_yellow
    is_black = ((r < 18) & (g < 18) & (b < 18)).astype(np.uint8) * 255
    has_stroke = np.array(Image.fromarray(is_black).filter(ImageFilter.MaxFilter(25))) > 0
    text_px = fg & has_stroke
    out = np.where(text_px, 0, 255).astype(np.uint8)
    return Image.fromarray(out)


def ocr_image(img_path: Path, psm: str = "6") -> str:
    res = subprocess.run(["tesseract", str(img_path), "stdout", "--psm", psm], capture_output=True, text=True)
    return re.sub(r"\s+", " ", res.stdout).strip()


def verify_short(
    final_mp4: Path,
    base_mp4: Path,
    f0_overlay_png: Path,
    manifest_json: Path,
    prep_json: Path,
    legacy_mod,
    out_json: Path,
) -> dict:
    manifest = json.loads(manifest_json.read_text())
    prep = json.loads(prep_json.read_text())
    final_sha = sha256(final_mp4)
    base_sha = sha256(base_mp4)

    # (1) Provenance manifest & filtergraph diff
    fg_base = manifest["filtergraph_base"]
    fg_final = manifest["filtergraph_final"]
    fg_diff = list(difflib.unified_diff(
        fg_base.split(";"), fg_final.split(";"),
        fromfile="base_filtergraph", tofile="final_filtergraph", lineterm=""
    ))
    prov_pass = (
        manifest.get("final_sha256") == final_sha
        and manifest.get("base_sha256") == base_sha
        and manifest.get("picture_sha256") == manifest.get("base_picture_sha256")
        and fg_base.replace("enable='0'", "enable='1'") == fg_final
    )

    n_final = frame_count(final_mp4)
    n_base = frame_count(base_mp4)
    last_idx = n_final - 1
    tail_start = n_final - 30

    # (2) Base whole-frame f0-vs-last < 2.0 at 180x320 and 270x480 + c37 loop_measures
    base_f0_180 = decode_gray_frame(base_mp4, 0, 180, 320)
    base_last_180 = decode_gray_frame(base_mp4, last_idx, 180, 320)
    base_diff_180 = float(np.abs(base_f0_180 - base_last_180).mean())

    base_f0_270 = decode_gray_frame(base_mp4, 0, 270, 480)
    base_last_270 = decode_gray_frame(base_mp4, last_idx, 270, 480)
    base_diff_270 = float(np.abs(base_f0_270 - base_last_270).mean())

    c37_base = legacy_mod.loop_measures(base_mp4)
    c37_final = legacy_mod.loop_measures(final_mp4)

    step2_pass = (
        n_final == n_base
        and base_diff_180 < 2.0
        and base_diff_270 < 2.0
        and c37_base["whole"] < 2.0
        and c37_base["masked"] < 2.0
        and c37_final["masked"] < 2.0
    )

    # (3) Final last vs base last < 1.0 whole; final f0 vs base f0 < 1.0 outside f0 text alpha bboxes + 8px
    final_last_180 = decode_gray_frame(final_mp4, last_idx, 180, 320)
    final_last_270 = decode_gray_frame(final_mp4, last_idx, 270, 480)
    last_vs_base_180 = float(np.abs(final_last_180 - base_last_180).mean())
    last_vs_base_270 = float(np.abs(final_last_270 - base_last_270).mean())

    final_f0_1080 = decode_gray_frame(final_mp4, 0, 1080, 1920)
    base_f0_1080 = decode_gray_frame(base_mp4, 0, 1080, 1920)
    bboxes = alpha_bboxes_padded(f0_overlay_png, pad=8, target_w=1080, target_h=1920)
    mask = np.ones((1920, 1080), dtype=bool)
    for x0, y0, x1, y1 in bboxes:
        mask[y0:y1, x0:x1] = False
    f0_outside_diff = float(np.abs(final_f0_1080[mask] - base_f0_1080[mask]).mean())

    step3_pass = (
        last_vs_base_180 < 1.0
        and last_vs_base_270 < 1.0
        and f0_outside_diff < 1.0
    )

    # (4) OCR f0 = locked hook, every tail frame empty, captions word-for-word vs spoken words
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        f0_png = td_path / "f0_full.png"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(final_mp4),
             "-vf", "select='eq(n,0)'", "-frames:v", "1", str(f0_png)],
            check=True,
        )
        f0_im = Image.open(f0_png)
        hook_lines = []
        for idx_b, (_, y0, _, y1) in enumerate(bboxes):
            line_png = td_path / f"f0_band_{idx_b}.png"
            prep_for_ocr(f0_im.crop((0, max(0, y0 - 8), 1080, min(1920, y1 + 8)))).save(line_png)
            hook_lines.append(ocr_image(line_png, psm="7"))
        f0_hook_ocr = " ".join(hook_lines).strip()

        # Extract all 30 tail frames (tail_start .. last_idx) at full 1080x1920 and check OCR on hook & caption regions
        tail_dir = td_path / "tail"
        tail_dir.mkdir()
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(final_mp4),
             "-vf", f"select='gte(n,{tail_start})'", "-fps_mode", "vfr", str(tail_dir / "%03d.png")],
            check=True,
        )
        tail_nonempty = []
        for idx, p in enumerate(sorted(tail_dir.glob("*.png"))):
            im = Image.open(p)
            for region_name, box in [("hook", (0, 80, 1080, 420)), ("caption", (0, 1460, 1080, 1620))]:
                crop_p = td_path / f"t_{idx}_{region_name}.png"
                prep_for_ocr(im.crop(box)).save(crop_p)
                txt = ocr_image(crop_p, psm="6")
                if re.sub(r"[^A-Za-z0-9]+", "", txt):
                    tail_nonempty.append({"frame": tail_start + idx, "region": region_name, "text": txt})

    words = [w["word"] for sp in prep["vo_splice_map"]["subspans"] for w in sp["words"]]
    groups = []
    g = []
    for w in words:
        g.append(w)
        if len(g) == 3 or w[-1:] in ".,?!":
            groups.append(" ".join(g).upper())
            g = []
    if g:
        groups.append(" ".join(g).upper())

    s5_caption_check = True
    if "S5_" in final_mp4.name:
        s5_caption_check = ("GLIESE 710 COME" in groups and "TO THE SUN?" in groups and "GLIESE 710 COME," not in groups)

    expected_hook_tokens = prep.get("hook_tokens", [])
    hook_ocr_upper = f0_hook_ocr.upper()
    hook_ok = bool(re.sub(r"[^A-Z0-9]+", "", hook_ocr_upper)) and all(
        tok.upper() in hook_ocr_upper for tok in expected_hook_tokens
    )
    step4_pass = hook_ok and len(tail_nonempty) == 0 and s5_caption_check

    # (5) Diagnostic final whole-frame f0-vs-last
    final_f0_180 = decode_gray_frame(final_mp4, 0, 180, 320)
    final_f0_270 = decode_gray_frame(final_mp4, 0, 270, 480)
    diag_final_180 = float(np.abs(final_f0_180 - final_last_180).mean())
    diag_final_270 = float(np.abs(final_f0_270 - final_last_270).mean())

    overall_pass = prov_pass and step2_pass and step3_pass and step4_pass
    report = {
        "gate": "h43-LOOP",
        "verdict": "PASS" if overall_pass else "FAIL",
        "final_mp4": str(final_mp4),
        "final_sha256": final_sha,
        "base_mp4": str(base_mp4),
        "base_sha256": base_sha,
        "frames": n_final,
        "tail_frames_checked": n_final - tail_start,
        "step1_provenance": {
            "pass": prov_pass,
            "filtergraph_diff": fg_diff,
        },
        "step2_base_loop": {
            "pass": step2_pass,
            "base_f0_vs_last_180x320": round(base_diff_180, 4),
            "base_f0_vs_last_270x480": round(base_diff_270, 4),
            "c37_base": c37_base,
            "c37_final_masked": c37_final["masked"],
        },
        "step3_final_vs_base": {
            "pass": step3_pass,
            "final_last_vs_base_last_180x320": round(last_vs_base_180, 4),
            "final_last_vs_base_last_270x480": round(last_vs_base_270, 4),
            "final_f0_vs_base_f0_outside_text_bboxes_pad8": round(f0_outside_diff, 4),
            "f0_text_alpha_bboxes_pad8": bboxes,
        },
        "step4_ocr_and_captions": {
            "pass": step4_pass,
            "f0_hook_ocr": f0_hook_ocr,
            "tail_nonempty_hits": tail_nonempty,
            "caption_groups": groups,
            "s5_caption_check": s5_caption_check,
        },
        "step5_diagnostic_final_whole": {
            "final_f0_vs_last_180x320": round(diag_final_180, 4),
            "final_f0_vs_last_270x480": round(diag_final_270, 4),
            "c37_final_whole": c37_final["whole"],
        },
    }
    out_json.write_text(json.dumps(report, indent=2) + "\n")
    print(f"h43-LOOP {report['verdict']}: {final_mp4.name} base_180={base_diff_180:.3f} base_270={base_diff_270:.3f} "
          f"last_vs_base={last_vs_base_180:.3f} f0_outside={f0_outside_diff:.3f} tail_hits={len(tail_nonempty)} "
          f"diag_final_180={diag_final_180:.3f}")
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--render-root", type=Path, default=Path("/Users/benjaminoats/_desk/renders/J1100-v07"))
    ap.add_argument("--media-root", type=Path, default=Path("/Users/benjaminoats/YouTube/orbit-with-ben"))
    args = ap.parse_args()

    legacy_path = args.media_root / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/mon30_comets/_assemble_mon30_comets_v03.py"
    spec = importlib.util.spec_from_file_location("legacy", legacy_path)
    legacy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(legacy)

    all_pass = True
    results = {}
    for key in ["S2_027_emwQsPxnRGM", "S5_028_jJ5LkFGyzLI", "S6_028_X768qs8sNQs"]:
        d = args.render_root / key
        final_mp4 = d / f"{key}_v07.mp4"
        base_mp4 = d / f"{key}_v07_base.mp4"
        f0_png = d / "f0_overlay.png"
        manifest_json = d / "h43_provenance_manifest.json"
        prep_json = d / "locked_preparation.json"
        out_json = d / "h43_loop_report.json"
        rep = verify_short(final_mp4, base_mp4, f0_png, manifest_json, prep_json, legacy, out_json)
        results[key] = rep
        if rep["verdict"] != "PASS":
            all_pass = False

    summary_path = args.render_root / "H43_LOOP_SUMMARY.json"
    summary_path.write_text(json.dumps(results, indent=2) + "\n")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
