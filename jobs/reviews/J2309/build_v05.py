#!/usr/bin/env python3
"""J2309 isolated v05 adapter. Uses the committed v04 builder; never writes v04.
Run only after checking that J2309-render is not already running.
This candidate is not approved: E1 and inherited Keeper conflicts require review.
"""
from pathlib import Path
import sys
SOURCE = Path('/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts/_assemble_029_shorts_v04.py')
s = SOURCE.read_text()
s = s.replace('HERE = Path(__file__).resolve().parent', f'HERE = Path({str(SOURCE.parent)!r})')
s = s.replace('PACK = HERE / "shorts_v04_pack"', 'PACK = Path("/private/tmp/J2309-codex-wt/jobs/reviews/J2309/pack")')
s = s.replace('WORK = Path("/private/tmp/betelgeuse029_shorts_v04")', 'WORK = Path("/private/tmp/J2309-render")')
s = s.replace('local = round(local + gap, 3)', 'local = round(local + (0.08 if si == 0 else gap), 3)')
# Load definitions without running the original CLI; overrides share its globals.
ns = {"__file__": str(SOURCE), "__name__": "j2309_builder"}
exec(compile(s, str(SOURCE), 'exec'), ns)

exec('# J2309: new local version; no delivery or scheduled-state writes.\nEND_CARD = 0.30\nVO_TAIL = 0.50\nspec = SHORTS[0]\nspec["stem"] = "029_short_wed09_great_dimming_v05"\nspec["sentences"] = [\n    {"a":109.92,"b":110.64}, {"a":113.32,"b":114.20},\n    {"a":115.00,"b":119.14}, {"a":119.68,"b":123.16},\n    {"a":127.54,"b":129.38}, {"a":133.54,"b":137.80},\n    {"a":138.44,"b":143.56}]\nSHORTS = [spec]\ndef layout_plates(plates, words, last, plan_total):\n    total = round(last + VO_TAIL + END_CARD, 2)\n    bounds = [0, 2.52, 4.77, 8.15, 11.82, 15.33, 18.03, round(total-0.30,2), total]\n    assert 22 <= total <= 27, (last,total)\n    assert max(b-a for a,b in zip(bounds,bounds[1:])) <= 4\n    return [{**p,"in":bounds[i],"out":bounds[i+1]} for i,p in enumerate(plates)]\ndef make_end(path):\n    Image.new("RGBA",(W,H),(0,0,0,0)).save(path)\n    return {"rows":[],"long_title":LONG_TITLE,"youtube_id":LONG_ID,"removed_for":"E1"}\ndef ship(*args):\n    print("J2309: delivery disabled pending explicit E1 review; no UAT claim.", flush=True)\n', ns)
if __name__ == "__main__":
    sys.exit(ns["main"]())
