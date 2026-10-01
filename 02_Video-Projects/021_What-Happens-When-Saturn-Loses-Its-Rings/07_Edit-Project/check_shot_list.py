#!/usr/bin/env python3
"""Check a Saturn shot list CSV against NASA_POOL_v01 and the cut rules, then write its credit block.

Usage: python3 check_shot_list.py shot_list_v03b.csv [--vo-end 523.6]

CSV columns (header row required):
  row       running number
  vo_in     seconds into saturn_long_vo_v03b_tightened_LOCK.m4a (e.g. 12.4)
  vo_out    seconds
  source    NASA | AI | OMNI | GODDARD | CARD
  id        NASA ID for NASA rows; clip file name for AI / OMNI / GODDARD; card title for CARD
  src_in    seconds into the clip used (AI / OMNI / GODDARD only; blank for stills)
  src_out   seconds into the clip used
  move      camera move on a still, e.g. "push 6%" (required for NASA rows)
  vo_text   the words spoken over this row
  caption   on-screen text, if any

Exit code 0 only when every check passes. On a pass it writes <csv>_credits.txt,
built from nasa_pool_v01.json (the lines were copied from each photojournal page).
"""
import csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
POOL = {e["nasa_id"]: e for e in json.load(open(os.path.join(HERE, "nasa_pool_v01.json")))}

MIN_S, MAX_S = 3.5, 6.5          # picture change every 4–6 s, small tolerance
OMNI_MIN = 3.0                   # Orbit reaction beats may be shorter (Ben, 1 Oct: the approved tumble is 3.0 s)
GODDARD_MAX_SHOTS = 2            # SVS 12672: up to two separate stretches, never sliced further
END_HOLD_MAX = 22.0              # last row only: the scripted 15–20 s end hold
CARD_MAX = 2.5                   # chapter cards ~1.5 s

AURORA = {"PIA13402", "PIA13404", "PIA11396", "PIA09185", "PIA17900", "PIA17668", "PIA01269", "PIA21899"}
HUBBLE_SEASONS = {"PIA03156", "PIA03158", "PIA03159", "PIA03160", "PIA03161", "PIA03162"}
# words that must not sit over the wrong evidence
RAIN_WORDS = re.compile(r"\brain|raining|pour", re.I)
THIN_WORDS = re.compile(r"\bthin", re.I)
# hook promises: these words must be covered by a clip whose id contains the tag
PROMISES = [(re.compile(r"when they were new", re.I), "young"),
            (re.compile(r"nothing around it", re.I), "bare")]


def is_orbit(src, rid):
    """Orbit reaction beats: Omni clips, or an approved Orbit fallback such as veo_orbit_tumble_v03_fallback_0-3s.mp4."""
    return src == "OMNI" or "orbit" in rid.lower()


def approved_window(rid):
    """A clip named ..._A-Bs.mp4 is approved only between A and B seconds."""
    m = re.search(r"_(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)s\.\w+$", rid)
    return (float(m.group(1)), float(m.group(2))) if m else None


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    path = args[0]
    vo_end = float(args[args.index("--vo-end") + 1]) if "--vo-end" in args else 523.6
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    errs, nasa_used, clip_ranges = [], [], {}

    def err(r, msg):
        errs.append(f"row {r.get('row', '?')}: {msg}")

    prev_out = 0.0
    for k, r in enumerate(rows):
        last = k == len(rows) - 1
        try:
            a, b = float(r["vo_in"]), float(r["vo_out"])
        except (KeyError, ValueError):
            err(r, "vo_in/vo_out missing or not a number")
            continue
        if abs(a - prev_out) > 0.05:
            err(r, f"gap or overlap: starts {a:.2f}, previous row ended {prev_out:.2f}")
        prev_out = b
        d = b - a
        src = (r.get("source") or "").strip().upper()
        rid = (r.get("id") or "").strip()
        text = r.get("vo_text") or ""

        if src == "CARD":
            if d > CARD_MAX:
                err(r, f"chapter card {d:.1f}s > {CARD_MAX}s")
        elif last:
            if d > END_HOLD_MAX:
                err(r, f"end hold {d:.1f}s > {END_HOLD_MAX}s")
            if src == "NASA" and not (r.get("move") or "").strip():
                err(r, "end hold on a still needs a move (slow push), not a freeze")
        elif not ((OMNI_MIN if is_orbit(src, rid) else MIN_S) <= d <= MAX_S):
            err(r, f"duration {d:.1f}s outside {MIN_S}–{MAX_S}s")

        if src == "NASA":
            if rid not in POOL:
                err(r, f"{rid} is not in nasa_pool_v01.json")
            nasa_used.append(rid)
            if not (r.get("move") or "").strip():
                err(r, "NASA still with no move")
            if rid in AURORA and RAIN_WORDS.search(text):
                err(r, f"{rid} is an aurora, not ring rain, but sits under: {text.strip()[:60]}")
            if rid in HUBBLE_SEASONS and THIN_WORDS.search(text):
                err(r, f"{rid} shows seasonal tilt, not thinning, but sits under: {text.strip()[:60]}")
        elif src in ("AI", "OMNI", "GODDARD"):
            try:
                si, so = float(r["src_in"]), float(r["src_out"])
            except (KeyError, ValueError):
                err(r, f"{src} row needs src_in/src_out")
                continue
            win = approved_window(rid)
            if win and (si < win[0] - 0.01 or so > win[1] + 0.01):
                err(r, f"{rid} is approved only for {win[0]:g}-{win[1]:g}s, row uses {si:g}-{so:g}s")
            if abs((so - si) - d) > 0.1:
                err(r, f"clip span {so - si:.2f}s != row length {d:.2f}s (no slow-mo or stretch)")
            for (pi, po, prow) in clip_ranges.get(rid, []):
                if si < po and pi < so:
                    err(r, f"reuses {rid} {si}-{so}s, already used {pi}-{po}s in row {prow}")
            clip_ranges.setdefault(rid, []).append((si, so, r.get("row")))
        elif src != "CARD":
            err(r, f"unknown source '{src}'")

        for pat, tag in PROMISES:
            if pat.search(text) and tag not in rid.lower():
                err(r, f"hook promise '{pat.pattern}' must sit over a '{tag}' clip, got {src} {rid}")

    dup = sorted({i for i in nasa_used if nasa_used.count(i) > 1})
    if dup:
        errs.append("NASA IDs used more than once: " + ", ".join(dup))
    if prev_out + 0.05 < vo_end:
        errs.append(f"list ends at {prev_out:.2f}s, VO runs to {vo_end}s")
    gd = clip_ranges.get(next((r["id"] for r in rows if (r.get("source") or "").upper() == "GODDARD"), ""), [])
    if len(gd) > GODDARD_MAX_SHOTS:
        errs.append(f"Goddard video used in {len(gd)} rows; at most {GODDARD_MAX_SHOTS} separate stretches")

    picture_rows = [r for r in rows if (r.get("source") or "").upper() != "CARD"]
    print(f"{len(rows)} rows, {len(picture_rows)} pictures, {len(set(nasa_used))} NASA IDs, ends {prev_out:.2f}s")
    if errs:
        print(f"FAIL: {len(errs)} problem(s)")
        for e in errs:
            print(" -", e)
        sys.exit(1)

    seen, lines = set(), []
    for i in nasa_used:
        if i in seen:
            continue
        seen.add(i)
        e = POOL[i]
        lines.append(f"{e['title']} ({i}): {e['credit']}")
    if any((r.get("source") or "").upper() == "GODDARD" for r in rows):
        # svs.gsfc.nasa.gov/12672 "Saturn's Rings Are Disappearing": credit as the page asks.
        # Its soundtrack is licensed music and narration: use the picture only, muted.
        lines.append("Ring rain animation (SVS 12672, Saturn's Rings Are Disappearing): NASA's Goddard Space Flight Center")
    out = os.path.splitext(path)[0] + "_credits.txt"
    open(out, "w", encoding="utf-8").write("Images courtesy of NASA. Use does not imply endorsement.\n" + "\n".join(lines) + "\n")
    print(f"PASS. Credit block written to {out}")


if __name__ == "__main__":
    main()
