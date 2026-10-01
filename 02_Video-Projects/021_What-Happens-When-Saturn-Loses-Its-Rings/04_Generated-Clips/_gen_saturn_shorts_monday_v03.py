#!/usr/bin/env python3
"""Monday Short still v03 — CoS run#7 FAIL on v02 + try0 stripped curtains.

Vertex edit of v01 (keep composition). Every ice curtain ends at Saturn's
southern cloud tops, fading into the atmosphere. NOTHING in the black below.

Self-check gates BOTH:
  1) void below southern limb is empty
  2) curtains still present on the planet face (not stripped like try0)

If Vertex strips curtains, fall back to surgical void-erase of v01 (still an
edit of v01 — keeps every curtain on-disk). Eyeball before UAT pack.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

import numpy as np
from google import genai
from google.genai import types
from PIL import Image, ImageFilter

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
V01 = EP / "04_Generated-Clips" / "shorts_stills_v01" / "monday_saturn_rings_streaming_v01.png"
OUT = EP / "04_Generated-Clips" / "shorts_stills_v03"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_shorts_stills_v03_for_ben_ok"
)
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/cursor_agent_stores/bc-bb6a84a0-ea11-5101-b43f-34c5b13867e0/files/artifacts"
)

PROJECT = "gen-lang-client-0538779324"
LOCATION = "us-central1"
MODEL = "gemini-2.5-flash-image"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chunk_write(src: Path | bytes, dest: Path, retries: int = 10) -> None:
    data = src if isinstance(src, (bytes, bytearray)) else Path(src).read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries):
        try:
            tmp = dest.with_suffix(dest.suffix + ".partial")
            with open(tmp, "wb") as o:
                for i in range(0, len(data), 500 * 1024):
                    o.write(data[i : i + 500 * 1024])
                    o.flush()
            tmp.replace(dest)
            time.sleep(0.25)
            if dest.stat().st_size == len(data) and sha256(dest) == hashlib.sha256(data).hexdigest():
                return
        except OSError as e:
            print(f"  chunk retry {attempt}: {e}", flush=True)
            time.sleep(1.2 * (attempt + 1))
    raise RuntimeError(f"chunk_write failed {dest}")


def warm_disk_mask(img: Image.Image) -> Image.Image:
    """Butterscotch Saturn disk — excludes near-white ice curtains."""
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    chroma = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    warm = (r > 95) & (g > 75) & (b < 145) & ((r + g) > (b + 50)) & (r > b + 15)
    ice = (luma > 150) & (chroma < 45)
    m = warm & (~ice) & (luma > 60) & (luma < 210)
    mask = Image.fromarray((m * 255).astype(np.uint8))
    mask = mask.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(5))
    mask = mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(7))
    return mask


def ice_curtain_mask(img: Image.Image) -> np.ndarray:
    """Pale vertical ice / sparkle (curtains + ring ice), not warm bands."""
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    chroma = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    # curtains are bright pale / cool-white sparkle, not butterscotch
    return (luma > 125) & (chroma < 75) & (b + 30 >= r * 0.5) & (abs(r - g) < 55)


def south_limb(disk: Image.Image) -> int:
    m = np.asarray(disk) > 128
    ys = np.where(m.any(axis=1))[0]
    return int(ys.max()) if len(ys) else 0


def curtain_column_signature(ice: np.ndarray, y0: int, y1: int, x0: int, x1: int) -> np.ndarray:
    band = ice[y0:y1, x0:x1]
    return band.sum(axis=0).astype(np.float64)


def score_still(path: Path, v01_sig: np.ndarray | None = None) -> dict:
    img = Image.open(path).convert("RGB")
    w, h = img.size
    disk = warm_disk_mask(img)
    south = south_limb(disk)
    if south < int(h * 0.5):
        return {"pass": False, "reason": "south_limb_too_high", "south_y": south}

    ice = ice_curtain_mask(img)
    x0, x1 = int(w * 0.12), int(w * 0.88)

    # void below southern limb
    yv0 = min(h - 1, south + 2)
    void = ice[yv0:h, x0:x1]
    void_count = int(void.sum())
    void_ratio = void_count / max(void.size, 1)

    # curtains on southern face (ring underside → south limb)
    yf0, yf1 = int(h * 0.40), south
    face = ice[yf0:yf1, x0:x1]
    face_count = int(face.sum())
    sig = curtain_column_signature(ice, yf0, yf1, x0, x1)
    # verticality: columns with ice
    active_cols = int((sig > (yf1 - yf0) * 0.08).sum())

    corr = None
    curtain_keep = face_count > 8000 and active_cols >= 6
    if v01_sig is not None and v01_sig.shape == sig.shape and v01_sig.std() > 0 and sig.std() > 0:
        corr = float(np.corrcoef(v01_sig, sig)[0, 1])
        curtain_keep = curtain_keep and corr >= 0.55

    void_ok = void_ratio < 0.004 and void_count < 900
    ok = bool(void_ok and curtain_keep and south > int(h * 0.55))
    return {
        "pass": ok,
        "south_y": south,
        "south_frac": round(south / h, 3),
        "void_ice": void_count,
        "void_ratio": round(void_ratio, 5),
        "face_ice": face_count,
        "active_cols": active_cols,
        "col_corr_v01": None if corr is None else round(corr, 3),
        "void_ok": void_ok,
        "curtain_keep": curtain_keep,
    }


def surgical_void_erase(src: Path, dest: Path) -> dict:
    """Edit v01: erase ice curtains ONLY below southern limb; feather at limb."""
    img = Image.open(src).convert("RGB")
    arr = np.asarray(img).astype(np.float32).copy()
    h, w = arr.shape[:2]
    disk = warm_disk_mask(img)
    south = south_limb(disk)
    ice = ice_curtain_mask(img)

    # sample clean void corner for fill (top-right / bottom corners away from curtains)
    fill = arr[int(h * 0.85) : h, int(w * 0.75) : w].reshape(-1, 3)
    # prefer dark pixels
    fill_luma = 0.299 * fill[:, 0] + 0.587 * fill[:, 1] + 0.114 * fill[:, 2]
    dark = fill[fill_luma < 25]
    if len(dark) < 50:
        dark = fill
    rng = np.random.default_rng(42)

    # hard erase below south+2
    y0 = min(h - 1, south + 2)
    for y in range(y0, h):
        row_ice = ice[y]
        xs = np.where(row_ice)[0]
        for x in xs:
            # keep faint stars: only erase brighter ice
            luma = 0.299 * arr[y, x, 0] + 0.587 * arr[y, x, 1] + 0.114 * arr[y, x, 2]
            if luma < 35:
                continue
            sample = dark[rng.integers(0, len(dark))]
            # tiny star chance
            if rng.random() < 0.004:
                sample = np.array([180, 180, 190], dtype=np.float32)
            arr[y, x] = sample

    # soft fade last ~18px ON the disk: ice → underlying warm (pull toward local blur)
    fade = 18
    y_fade0 = max(0, south - fade)
    blurred = np.asarray(img.filter(ImageFilter.GaussianBlur(radius=6))).astype(np.float32)
    for y in range(y_fade0, south + 1):
        t = (y - y_fade0) / max(fade, 1)  # 0 at top of fade → 1 at south
        strength = 0.35 + 0.65 * t  # stronger fade near limb
        row_ice = ice[y]
        xs = np.where(row_ice)[0]
        for x in xs:
            # only fade ice that is over/near disk columns
            arr[y, x] = (1 - strength) * arr[y, x] + strength * blurred[y, x]

    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    out.save(dest)
    return {"method": "surgical_void_erase", "south_y": south, "fade_px": fade}


PROMPT = (
    "IMAGE EDIT of the attached vertical 9:16 Saturn Short opening still. "
    "KEEP this EXACT composition pixel-faithfully: Saturn position/size, diagonal rings, "
    "AND every ice curtain currently falling from the underside of the rings across "
    "Saturn's face — same number, same columns, same sparkle. "
    "CHANGE ONLY the portion of each curtain that continues PAST the planet's southern "
    "limb into black space: erase those void tails completely and replace with clean "
    "near-black starfield. "
    "On the planet itself, each curtain must FADE into the southern butterscotch cloud "
    "tops (ice falls INTO Saturn). "
    "HARD RULES: do NOT delete curtains on the planet face; do NOT redesign; do NOT "
    "move Saturn; do NOT remove the streaming ring-rain look. "
    "The black void UNDER the southern limb must have ZERO curtains / grain trails / mist. "
    "No Orbit, no text, no logos. Premium CGI 9:16."
)


def save_response(response, dest: Path) -> None:
    for part in response.candidates[0].content.parts or []:
        data = getattr(getattr(part, "inline_data", None), "data", None)
        if data:
            dest.write_bytes(data)
            return
    raise RuntimeError("no image")


def v01_face_sig() -> np.ndarray:
    img = Image.open(V01).convert("RGB")
    w, h = img.size
    disk = warm_disk_mask(img)
    south = south_limb(disk)
    ice = ice_curtain_mask(img)
    return curtain_column_signature(ice, int(h * 0.40), south, int(w * 0.12), int(w * 0.88))


def main() -> None:
    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT
    os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)

    OUT.mkdir(parents=True, exist_ok=True)
    work = OUT / "_work"
    rejected = OUT / "_rejected"
    work.mkdir(exist_ok=True)
    rejected.mkdir(exist_ok=True)

    base_sig = v01_face_sig()
    base_score = score_still(V01, base_sig)
    print("v01 score", base_score, flush=True)

    candidates: list[tuple[Path, dict, str]] = []

    # A) Vertex edit tries
    for i in range(4):
        dest = work / f"monday_v03_vertex_try_{i}.png"
        print(f"vertex try {i}", flush=True)
        ok_gen = False
        for attempt in range(4):
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=[
                        "Base image to edit (keep composition + keep curtains on planet):",
                        types.Part.from_bytes(data=V01.read_bytes(), mime_type="image/png"),
                        PROMPT,
                    ],
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                        image_config=types.ImageConfig(aspect_ratio="9:16"),
                    ),
                )
                save_response(response, dest)
                ok_gen = True
                break
            except Exception as e:
                print(f"  gen retry {attempt}: {e}", flush=True)
                time.sleep(6 * (attempt + 1))
        if not ok_gen:
            continue
        im = Image.open(dest)
        if im.size[0] >= im.size[1]:
            print("  not portrait, skip", im.size, flush=True)
            continue
        sc = score_still(dest, base_sig)
        print(f"  score {sc}", flush=True)
        crop = im.crop((0, int(im.size[1] * 0.55), im.size[0], im.size[1]))
        crop.save(work / f"monday_v03_vertex_try_{i}_bottom.png")
        candidates.append((dest, sc, f"vertex_try_{i}"))
        if sc["pass"]:
            break

    # B) Surgical edit of v01 (keeps curtains; clears void)
    surg = work / "monday_v03_surgical.png"
    print("surgical void-erase of v01", flush=True)
    meta = surgical_void_erase(V01, surg)
    print("  surgical meta", meta, flush=True)
    sc_s = score_still(surg, base_sig)
    print(f"  score {sc_s}", flush=True)
    Image.open(surg).crop((0, int(1344 * 0.55), 768, 1344)).save(work / "monday_v03_surgical_bottom.png")
    candidates.append((surg, sc_s, "surgical_void_erase"))

    # pick best: pass preferred; else best curtain_keep with lowest void
    passed = [c for c in candidates if c[1].get("pass")]
    if passed:
        # prefer surgical if both pass (pixel-faithful), else first pass
        surg_pass = [c for c in passed if c[2] == "surgical_void_erase"]
        best_path, best_sc, best_tag = surg_pass[0] if surg_pass else passed[0]
    else:
        # do not pack
        report = {
            "error": "SELF-CHECK FAIL — curtains stripped or void dirty",
            "candidates": [
                {"tag": t, "path": str(p), "score": s} for p, s, t in candidates
            ],
        }
        (OUT / "FAIL_REPORT.json").write_text(json.dumps(report, indent=2) + "\n")
        raise SystemExit("SELF-CHECK FAIL — not packing UAT")

    # archive non-winners
    for p, s, t in candidates:
        if p != best_path and p.exists():
            dest = rejected / f"{t}_{'PASS' if s.get('pass') else 'FAIL'}.png"
            if not dest.exists():
                chunk_write(p, dest)

    final = OUT / "monday_saturn_rings_streaming_v03.png"
    chunk_write(best_path, final)

    # eyeball artifacts
    im = Image.open(final)
    crop = im.crop((0, int(im.size[1] * 0.55), im.size[0], im.size[1]))
    crop_path = OUT / "monday_v03_bottom_qa.png"
    crop.save(crop_path)
    face = im.crop((int(im.size[0] * 0.12), int(im.size[1] * 0.38), int(im.size[0] * 0.88), best_sc["south_y"]))
    face_path = OUT / "monday_v03_face_qa.png"
    face.save(face_path)

    # side-by-side vs v01 south band
    v01 = Image.open(V01).convert("RGB")
    if v01.size != im.size:
        v01 = v01.resize(im.size, Image.Resampling.LANCZOS)
    y0, y1 = int(im.size[1] * 0.45), int(im.size[1] * 0.85)
    band = Image.new("RGB", (im.size[0] * 2 + 8, y1 - y0), (20, 20, 20))
    band.paste(v01.crop((0, y0, im.size[0], y1)), (0, 0))
    band.paste(im.crop((0, y0, im.size[0], y1)), (im.size[0] + 8, 0))
    band_path = OUT / "monday_v01_vs_v03_south.png"
    band.save(band_path)

    # final re-score on packed file
    final_sc = score_still(final, base_sig)
    print("FINAL score", final_sc, flush=True)
    if not final_sc["pass"]:
        raise SystemExit(f"FINAL self-check FAIL after pack: {final_sc}")

    # pack UAT only after pass
    if UAT.exists():
        for old in UAT.iterdir():
            if old.is_file():
                old.unlink()
    UAT.mkdir(parents=True, exist_ok=True)
    for p in (final, crop_path, face_path, band_path):
        chunk_write(p, UAT / p.name)
        chunk_write(p, ART / p.name)

    manifest = {
        "engine": "vertex+surgical" if best_tag == "surgical_void_erase" else "vertex",
        "project": PROJECT,
        "model": MODEL,
        "winner": best_tag,
        "ben_order": "CoS run#7 — Monday v03: curtains end at southern cloud tops (edit v01)",
        "base": V01.name,
        "base_sha256": sha256(V01),
        "file": final.name,
        "sha256": sha256(final),
        "bytes": final.stat().st_size,
        "self_check": final_sc,
        "candidates": [{"tag": t, "sha256": sha256(p), **s} for p, s, t in candidates],
        "stop": "WAIT Ben OK — no Shorts Veo",
        "finishedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    chunk_write((OUT / "MANIFEST.json").read_bytes(), UAT / "MANIFEST.json")
    readme = f"""# Saturn Monday Short still v03 — Ben OK

| File | Brief |
|---|---|
| `monday_saturn_rings_streaming_v03.png` | Edit of v01; ice curtains end at southern cloud tops; void below empty |
| `monday_v03_bottom_qa.png` | Bottom crop for void check |
| `monday_v03_face_qa.png` | Face crop — curtains must still be visible |
| `monday_v01_vs_v03_south.png` | v01 (left) vs v03 (right) south band |

Winner: `{best_tag}`. Self-check: void clean + curtains kept. **WAIT Ben OK. No Shorts Veo.**
"""
    (OUT / "README.md").write_text(readme)
    chunk_write(readme.encode(), UAT / "README.md")
    print(json.dumps({"MONDAY_V03_DONE": True, **manifest}, indent=2), flush=True)


if __name__ == "__main__":
    main()
