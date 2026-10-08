#!/usr/bin/env python3
"""Picture QA: the one image-quality check every long runs before Claude's review and Ben's watch (Ben, 8 Oct 2026:
"let's clean up the QA on image quality", after a dated computer model at 2:54 of 025 v03c got through).

  python3 scripts/picture_qa.py <video.mp4> --cuts <cuts.json> --pool <pool.json> [--pool <more.json>] --out-dir <pack>
                                [--reviewed-ok <json>] [--no-jitter]
  python3 scripts/picture_qa.py --cuts <cuts.json> --pool <pool.json> --out-dir <dir>      # source checks only, no video

Every cut is judged and reported at its film time (m:ss), the way Ben reports a problem.

What a cut is (from the cut list and the pool, before any pixel is looked at):
  - kind of picture  FAIL a computer model or reconstruction, simulation still, diagram, chart, graph, schematic, annotated
                     or labelled image, screenshot, wireframe. These look dated or like a textbook, not like the film.
                     WARN an artist's concept, illustration, render, animation still, map or mosaic: often right, so Claude
                     looks at it full size.
                     WARN a source the pool has no title for: nobody can tell what it is.
  - sharpness        FAIL upscaled more than 2.35x. WARN more than 2x (may look soft; rover frames are often 1024 px, so up to
                     2x is normal).
  - reuse            FAIL one picture used more than twice in the long.
How it looks (needs the video; scripts/polish_gate.py's checks): low detail, split panels and gutters, near-black,
noise with no picture under it, and a wobbly still push.

A source Claude has ruled on (--reviewed-ok {source: {"note", "kinds": ["kind of picture", "low detail", ...]}}) passes
on the kinds named for it and is listed as reviewed.

Writes <out-dir>/picture_qa.json, PICTURE_QA.md (FAIL first, then the WARN list Claude looks at full size) and, with a
video, picture_qa_review.jpg (every FAIL and WARN frame at 960 px, labelled m:ss). Exit 1 if any cut fails."""
from __future__ import annotations

import argparse
import json
import re
import subprocess as sp
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

UPSCALE_FAIL, UPSCALE_WARN = 2.35, 2.0  # rover frames are often 1024 px, so up to 2x is normal
MAX_REUSE = 2
KIND_FAIL = re.compile(r"computer[- ]?(reconstruction|model|generated|simulation|graphic)|\bsimulation\b|\bdiagram|\bchart\b|"
                       r"\bgraph\b|\bschematic|\bannotated\b|\blabell?ed\b|\bscreen ?shot|\bwireframe|\bcad\b|\binfographic", re.I)
OWN = re.compile(r"omni|veo|flow|code_graphic|orbit_|_card|title", re.I)  # our own clips and graphics: Claude reviews them in their own pack
KIND_WARN = re.compile(r"\bartist|\billustration|\bconcept\b|\brender|\banimation\b|\bmap\b|\bmosaic\b|\bcomposite\b", re.I)


def mmss(t: float) -> str:
    t = int(round(t))
    return f"{t // 60}:{t % 60:02d}"


def stem(name: str) -> str:
    return Path(str(name)).stem.split("~")[0].lower()


def load_pool(paths) -> dict:
    """{source stem: title} from pool files (a list of entries, or {"items"/"entries": [...]}, or {id: entry})."""
    out = {}
    for p in paths or []:
        d = json.loads(Path(p).read_text())
        items = d if isinstance(d, list) else d.get("items") or d.get("entries") or [dict(v, id=k) for k, v in d.items() if isinstance(v, dict)]
        for e in items:
            title = e.get("title") or ""
            for k in ("file_id", "nasa_id", "id", "file", "source"):
                if e.get(k):
                    out[stem(e[k])] = title
    return out


def source_checks(cuts: list, pool: dict) -> list:
    uses = Counter(c["source"] for c in cuts)
    rows = []
    for k, c in enumerate(cuts):
        mid = (c["timeline_in"] + c["timeline_out"]) / 2
        title = pool.get(stem(c["source"]))
        fail, warn = [], []
        if title is None and OWN.search(c["source"]):
            title = "our own clip or graphic"
        elif title is None:
            warn.append("kind of picture: no title in the pool, so nobody can tell what it is")
        elif KIND_FAIL.search(title):
            fail.append(f"kind of picture: '{title}' is a {KIND_FAIL.search(title).group(0).lower()}, which looks dated or like a textbook")
        elif KIND_WARN.search(title):
            warn.append(f"kind of picture: '{title}' ({KIND_WARN.search(title).group(0).lower()}), look at it full size")
        up = c.get("upscale")
        if up is None:
            warn.append("sharpness: upscale not recorded in the cut list")
        elif up > UPSCALE_FAIL:
            fail.append(f"sharpness: upscaled {up:.2f}x (limit {UPSCALE_FAIL}x)")
        elif up > UPSCALE_WARN:
            warn.append(f"sharpness: upscaled {up:.2f}x, may look soft")
        if uses[c["source"]] > MAX_REUSE:
            fail.append(f"reuse: used {uses[c['source']]} times (limit {MAX_REUSE})")
        rows.append(dict(cut=k, row=c.get("row"), source=c["source"], title=title, t=round(mid, 2), at=mmss(mid),
                         fail=fail, warn=warn))
    return rows


def apply_reviewed(rows: list, reviewed: dict) -> None:
    for r in rows:
        ok = reviewed.get(r["source"])
        if not ok:
            continue
        passed = [w for w in r["fail"] + r["warn"] if any(w.startswith(kind) for kind in ok.get("kinds", []))]
        if passed:
            r["fail"] = [w for w in r["fail"] if w not in passed]
            r["warn"] = [w for w in r["warn"] if w not in passed]
            r["reviewed_ok"] = dict(note=ok.get("note", ""), passed=passed)


def merge_polish(rows: list, res: dict) -> None:
    """Fold polish_gate's per-cut fails and warnings into the rows (it has already applied --reviewed-ok)."""
    by_cut = {r["cut"]: r for r in rows}
    for f in res.get("failed", []):
        by_cut[f["cut"]]["fail"] += f["why"]
    for w in res.get("warn", []):
        by_cut[w["cut"]]["warn"] += w["why"]
    for o in res.get("reviewed_ok", []):
        r = by_cut[o["cut"]]
        r.setdefault("reviewed_ok", dict(note=o.get("note", ""), passed=[]))["passed"] += o.get("why", [])


def report_md(rows: list, verdict: str, video: str) -> str:
    fails = [r for r in rows if r["fail"]]
    warns = [r for r in rows if r["warn"] and not r["fail"]]
    L = [f"# Picture QA: {verdict}", "", f"{video or 'source checks only (no video)'} · {len(rows)} cuts · "
         f"{len(fails)} fail · {len(warns)} for Claude to look at full size", ""]
    def line(r, why):
        name = f"{r['source']}" + (f" ({r['title']})" if r.get("title") else "")
        return f"- **{r['at']}** row {r['row']} · {name}: " + "; ".join(why)
    if fails:
        L += ["## Fix before anyone watches", ""] + [line(r, r["fail"]) for r in fails] + [""]
    if warns:
        L += ["## Claude looks at these full size", ""] + [line(r, r["warn"]) for r in warns] + [""]
    oks = [r for r in rows if r.get("reviewed_ok")]
    if oks:
        L += ["## Passed on Claude's ruling", ""] + [line(r, [r["reviewed_ok"]["note"] or "reviewed"]) for r in oks] + [""]
    L += ["Claude's own look still covers every cut on the per-row sheet: would a viewer trust this as a real, sharp, "
          "finished picture of what the sentence says?", ""]
    return "\n".join(L)


def review_sheet(video: str, rows: list, out: Path) -> Path | None:
    from PIL import Image, ImageDraw
    pick = [r for r in rows if r["fail"] or r["warn"]]
    if not pick:
        return None
    w, h, cols = 960, 540, 2
    sheet = Image.new("RGB", (w * cols, h * ((len(pick) + cols - 1) // cols)), (20, 20, 20))
    for i, r in enumerate(pick):
        raw = sp.run(["ffmpeg", "-v", "error", "-ss", f"{r['t']:.3f}", "-i", video, "-frames:v", "1", "-vf", f"scale={w}:{h}",
                      "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
        im = Image.frombytes("RGB", (w, h), raw)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, w, 26], fill=(0, 0, 0))
        d.text((8, 6), f"{r['at']}  row {r['row']}  {'FAIL' if r['fail'] else 'WARN'}  {r['source']}", fill=(255, 80, 80) if r["fail"] else (255, 210, 0))
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(out, quality=85)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", nargs="?")
    ap.add_argument("--cuts", required=True)
    ap.add_argument("--pool", action="append", default=[])
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--reviewed-ok")
    ap.add_argument("--no-jitter", action="store_true")
    a = ap.parse_args(argv)
    cuts = json.loads(Path(a.cuts).read_text())
    reviewed = json.loads(Path(a.reviewed_ok).read_text()) if a.reviewed_ok else {}
    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    rows = source_checks(cuts, load_pool(a.pool))
    apply_reviewed(rows, reviewed)
    polish = None
    if a.video:
        import polish_gate
        polish = polish_gate.judge(a.video, cuts, reviewed, not a.no_jitter, log=lambda m: None)
        merge_polish(rows, polish)
    verdict = "FAIL" if any(r["fail"] for r in rows) else "PASS"
    res = dict(verdict=verdict, video=a.video or "", rules=dict(
        kind_fail=KIND_FAIL.pattern, kind_warn=KIND_WARN.pattern, upscale_fail=UPSCALE_FAIL, upscale_warn=UPSCALE_WARN,
        max_reuse=MAX_REUSE, pixels="scripts/polish_gate.py" if a.video else "not run (no video)"),
        failed=[r for r in rows if r["fail"]], warn=[r for r in rows if r["warn"] and not r["fail"]], rows=rows,
        polish=dict(edge_floor=polish["edge_floor"], low_detail_floor=polish["low_detail_floor"]) if polish else None)
    (out / "picture_qa.json").write_text(json.dumps(res, indent=2))
    (out / "PICTURE_QA.md").write_text(report_md(rows, verdict, a.video or ""))
    sheet = review_sheet(a.video, rows, out / "picture_qa_review.jpg") if a.video else None
    for r in res["failed"]:
        print(f"FAIL {r['at']:>6} row {r['row']} {r['source']}: {'; '.join(r['fail'])}")
    for r in res["warn"]:
        print(f"WARN {r['at']:>6} row {r['row']} {r['source']}: {'; '.join(r['warn'])}")
    print(f"picture QA {verdict}: {len(res['failed'])} of {len(rows)} cuts fail, {len(res['warn'])} to look at"
          f" -> {out / 'PICTURE_QA.md'}" + (f", {sheet}" if sheet else ""))
    return 1 if res["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
