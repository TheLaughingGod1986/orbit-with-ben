#!/usr/bin/env python3
"""Pre-render sentence sheet: the picture under every spoken sentence, before anything is rendered (J0086, 9 Oct 2026).

Usage:
  python3 scripts/sentence_sheet.py <film dir> --shots <cuts.json | shot_list.csv> --words <VO words json> --out <sheet.png|jpg>
      [--search <dir> ...]   extra folders to find sources in, searched first, in the order given

One tile per sentence, in film order, 4 across and 24 to a page (<out stem>_p01, _p02, ...):
  - the frame that sits under the sentence, taken from the source itself, not a render: a still is the still (quad and
    vcrop framing applied, centre-cropped to 16:9); a clip is its in-point frame; a code graphic (a source under a
    code_out*/graphics* folder) is the mid frame of the stretch it plays;
  - when more than one cut plays under the sentence, the main frame is the one on screen longest and the others sit
    small beneath it;
  - the sentence, its m:ss, and the row and source name of the main frame.
A <out stem>.json lists the same per sentence. Claude rules row by row: does this picture show what he's saying?

--shots takes the assembler's cuts JSON (row, timeline_in, timeline_out, source, framing) or a shot list CSV
(row, source, vo_in, vo_out). Sources are found by file name: --search folders first, then the film folder (newest
copy wins when a name appears twice).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess as sp
import sys
import tempfile
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
COLS, PER_PAGE = 4, 24
TW, TH = 480, 270
SMALL_W, SMALL_H = 116, 65
TEXT_H = 150
TILE_H = TH + SMALL_H + 8 + TEXT_H
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}
CODE_DIRS = re.compile(r"^(code_out|graphics)", re.I)
QUAD = {"tl": (0.0, 0.0), "tr": (0.5, 0.0), "bl": (0.0, 0.5), "br": (0.5, 0.5), "c": (0.25, 0.25)}
SENT_END = re.compile(r"[.!?…][\"'”’)]*$")
FONT_PATHS = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/Library/Fonts/Arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    for p in (FONT_PATHS if bold else FONT_PATHS[1:]):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def mmss(t: float) -> str:
    return f"{int(t // 60)}:{int(t % 60):02d}"


def load_words(path: Path) -> list[dict]:
    d = json.loads(path.read_text(encoding="utf-8"))
    raw = []
    if isinstance(d, dict):
        for seg in d.get("segments", []):
            raw += seg.get("words", [])
        raw = raw or d.get("words", [])
    else:
        raw = d
    out = [dict(text=str(w.get("text", w.get("word", ""))).strip(), start=float(w["start"]), end=float(w["end"]))
           for w in raw if str(w.get("text", w.get("word", ""))).strip()]
    if not out:
        sys.exit(f"No timed words in {path}")
    return out


def sentences(words: list[dict]) -> list[dict]:
    out, cur = [], []
    for w in words:
        cur.append(w)
        if SENT_END.search(w["text"]):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return [dict(text=" ".join(w["text"] for w in s), start=s[0]["start"], end=s[-1]["end"]) for s in out]


def load_shots(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        d = json.loads(path.read_text(encoding="utf-8"))
        d = d.get("cuts", d) if isinstance(d, dict) else d
        return [dict(row=str(c.get("row", "")), t_in=float(c["timeline_in"]), t_out=float(c["timeline_out"]),
                     source=c["source"], framing=c.get("framing") or {}) for c in d]
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    return [dict(row=str(r.get("row", "")), t_in=float(r["vo_in"]), t_out=float(r["vo_out"]),
                 source=(r.get("source") or "").strip(), framing={}) for r in rows]


class Finder:
    def __init__(self, search: list[Path], film: Path):
        self.search, self.film, self._film_index = search, film, None

    def find(self, name: str) -> Path | None:
        if not name or name.upper() == "CARD":
            return None
        p = Path(name)
        if p.is_absolute() and p.exists():
            return p
        for d in self.search:
            hits = sorted(d.rglob(p.name), key=lambda x: -x.stat().st_mtime)
            if hits:
                return hits[0]
        if self._film_index is None:
            self._film_index = {}
            for root, _, files in os.walk(self.film):
                for f in files:
                    fp = Path(root) / f
                    old = self._film_index.get(f)
                    if old is None or fp.stat().st_mtime > old.stat().st_mtime:
                        self._film_index[f] = fp
        return self._film_index.get(p.name)


def cover(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.Resampling.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def placeholder(w: int, h: int, msg: str) -> Image.Image:
    im = Image.new("RGB", (w, h), (70, 20, 20))
    ImageDraw.Draw(im).text((8, h // 2 - 8), msg[:60], fill="white", font=font(14))
    return im


_cache: dict = {}


def frame(src: Path | None, shot: dict, name: str, w: int, h: int, tmp: Path) -> tuple[Image.Image, str]:
    """Frame for one cut and how it was taken (still / in-point / mid)."""
    if src is None:
        return placeholder(w, h, f"not found: {name}"), "missing"
    fr = shot["framing"]
    code = any(CODE_DIRS.match(part) for part in src.parts[-3:-1])
    if src.suffix.lower() in VIDEO_EXT:
        at = float(fr.get("offset", fr.get("at", 0.0)) or 0.0)
        how = "in-point"
        if code:
            at += (shot["t_out"] - shot["t_in"]) / 2
            how = "mid"
        key = (src, round(at, 2), json.dumps(fr, sort_keys=True))
        if key not in _cache:
            dst = tmp / f"f{len(_cache):04}.png"
            r = sp.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{at:.3f}", "-i", str(src),
                        "-frames:v", "1", str(dst)], capture_output=True, text=True)
            _cache[key] = Image.open(dst).convert("RGB") if r.returncode == 0 and dst.exists() else None
        im = _cache[key]
        if im is None:
            return placeholder(w, h, f"no frame: {name}"), "missing"
        vc = fr.get("vcrop")
        if vc:
            im = im.crop((vc[0], vc[1], vc[0] + vc[2], vc[1] + vc[3]))
    else:
        key = (src, None, json.dumps(fr, sort_keys=True))
        if key not in _cache:
            try:
                base = Image.open(src).convert("RGB")
                base.thumbnail((2400, 2400))
                _cache[key] = base
            except Exception:
                _cache[key] = None
        im = _cache[key]
        if im is None:
            return placeholder(w, h, f"unreadable: {name}"), "missing"
        how = "still"
    q = fr.get("quad")
    if q in QUAD:
        fx, fy = QUAD[q]
        im = im.crop((int(im.width * fx), int(im.height * fy), int(im.width * (fx + .5)), int(im.height * (fy + .5))))
    return cover(im, w, h), how


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("film")
    ap.add_argument("--shots", required=True)
    ap.add_argument("--words", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--search", action="append", default=[])
    a = ap.parse_args()

    film = Path(a.film).resolve()
    shots = sorted(load_shots(Path(a.shots)), key=lambda s: s["t_in"])
    sents = sentences(load_words(Path(a.words)))
    finder = Finder([Path(s).resolve() for s in a.search], film)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    f_head, f_body, f_small = font(17, bold=True), font(17), font(13)

    tiles, record, missing = [], [], set()
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for k, s in enumerate(sents, 1):
            under = [(min(s["end"], c["t_out"]) - max(s["start"], c["t_in"]), c) for c in shots
                     if c["t_in"] < s["end"] and c["t_out"] > s["start"]]
            if not under:
                under = [(0.0, min(shots, key=lambda c: abs(c["t_in"] - s["start"])))]
            main_cut = max(under, key=lambda x: x[0])[1]
            others = [c for _, c in sorted(under, key=lambda x: x[1]["t_in"]) if c is not main_cut]
            src = finder.find(main_cut["source"])
            if src is None:
                missing.add(main_cut["source"])
            tile = Image.new("RGB", (TW, TILE_H), (18, 18, 22))
            img, how = frame(src, main_cut, main_cut["source"], TW, TH, tmp)
            tile.paste(img, (0, 0))
            d = ImageDraw.Draw(tile)
            x = 0
            for c in others[:4]:
                osrc = finder.find(c["source"])
                if osrc is None:
                    missing.add(c["source"])
                small, _ = frame(osrc, c, c["source"], SMALL_W, SMALL_H, tmp)
                tile.paste(small, (x, TH + 4))
                x += SMALL_W + 4
            if len(others) > 4:
                d.text((x + 2, TH + 24), f"+{len(others) - 4}", fill="white", font=f_head)
            y = TH + SMALL_H + 10
            d.text((6, y), f"{k}.  {mmss(s['start'])}   row {main_cut['row']}  ·  {how}", fill=(255, 196, 120), font=f_head)
            d.text((6, y + 21), main_cut["source"][:58], fill=(160, 160, 170), font=f_small)
            lines = textwrap.wrap(s["text"], 50)
            if len(lines) > 5:
                lines = lines[:4] + [lines[4][:46] + " …"]
            for i, line in enumerate(lines):
                d.text((6, y + 40 + i * 20), line, fill="white", font=f_body)
            tiles.append(tile)
            record.append(dict(n=k, at=mmss(s["start"]), start=round(s["start"], 2), end=round(s["end"], 2),
                               text=s["text"], row=main_cut["row"], source=main_cut["source"], frame=how,
                               path=str(src) if src else None,
                               also=[dict(row=c["row"], source=c["source"], at=mmss(c["t_in"])) for c in others]))

    pages = [tiles[i:i + PER_PAGE] for i in range(0, len(tiles), PER_PAGE)]
    written = []
    for p, chunk in enumerate(pages, 1):
        rows = -(-len(chunk) // COLS)
        sheet = Image.new("RGB", (COLS * TW + (COLS + 1) * 8, rows * TILE_H + (rows + 1) * 8 + 40), (8, 8, 10))
        ImageDraw.Draw(sheet).text((10, 10), f"{film.name}  ·  sentence sheet  ·  page {p}/{len(pages)}  ·  "
                                   f"{Path(a.shots).name}", fill="white", font=f_head)
        for i, t in enumerate(chunk):
            sheet.paste(t, (8 + (i % COLS) * (TW + 8), 48 + (i // COLS) * (TILE_H + 8)))
        dest = out.with_name(f"{out.stem}_p{p:02}{out.suffix}")
        sheet.save(dest, quality=85) if dest.suffix.lower() in (".jpg", ".jpeg") else sheet.save(dest)
        written.append(dest)
    out.with_suffix(".json").write_text(json.dumps(dict(film=film.name, shots=str(a.shots), words=str(a.words),
                                                        sentences=record, missing=sorted(missing)), indent=2))
    print(f"sentence_sheet: {len(sents)} sentences, {len(shots)} cuts, {len(pages)} page(s)")
    for w in written:
        print(" ", w)
    if missing:
        print("WARN: sources not found:", ", ".join(sorted(missing)))


if __name__ == "__main__":
    main()
