#!/usr/bin/env python3
"""Build shot_list_v03b.csv for check_shot_list.py (Ben 1 Oct 15:08 London)."""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
POOL = {e["nasa_id"]: e for e in json.loads((HERE / "nasa_pool_v01.json").read_text())}
OUT = HERE / "shot_list_v03b.csv"
VO_END = 523.62
END_HOLD = 20.0

YOUNG = "veo_young_rings_v01.mp4"
BARE = "veo_bare_saturn_v05.mp4"
ICE = "edit_ice_chunks_v07.mp4"
GODDARD = "SVS_12672_ring_rain.mp4"
OMNI1 = "orbit_tumble_omni.mp4"
OMNI2 = "orbit_bare_omni.mp4"

AURORA = {
    "PIA13402", "PIA13404", "PIA11396", "PIA09185",
    "PIA17900", "PIA17668", "PIA01269", "PIA21899",
}
HUBBLE_SEASONS = {
    "PIA03156", "PIA03158", "PIA03159", "PIA03160", "PIA03161", "PIA03162",
}

# Contiguous picture/card rows. Durations 3.5–6.5 except CARD (≤2.5) and last end hold.
# Hook: young early stretch; later young late stretch. Bare same. Goddard once 3.5–6.5.
RAW: list[tuple] = [
    # open / hook
    (0.00, 4.32, "AI", ICE, 0.00, "Every half hour, Saturn's rings lose enough ice to fill an Olympic swimming pool.", "", ""),
    (4.32, 8.95, "NASA", "PIA08247", None, "It's raining into the planet right now. So how long do the rings have left?", "push 6%", ""),
    # Hook stretches widened to ≥3.5s for checker; promise phrases stay on young/bare clips
    (8.95, 12.50, "NASA", "PIA20496", None, "Stay with me, and you'll see where the ice goes,", "push 6%", ""),
    (12.50, 16.20, "AI", YOUNG, 0.00, "what the rings looked like when they were new,", "", ""),
    (16.20, 19.90, "AI", BARE, 0.00, "and Saturn with nothing around it at all.", "", ""),
    (19.90, 23.48, "NASA", "PIA11667", None, "Look along the sheet. It is not a solid disc. It is a crowd.", "push 6%", ""),
    (23.48, 28.64, "NASA", "PIA08248", None, "Chunks of ice, from grains to boulders, each on its own path,", "push 6%", ""),
    (28.64, 33.93, "NASA", "PIA08992", None, "packed so tightly that they read as one bright blade.", "push 6%", ""),
    (33.93, 39.45, "NASA", "PIA14943", None, "The blade is enormous sideways — tens of thousands of kilometres —", "push 6%", ""),
    (39.45, 44.00, "NASA", "PIA12654", None, "and absurdly thin the other way. In places the main rings are only about ten metres thick.", "push 6%", ""),
    (44.00, 49.12, "NASA", "PIA20498", None, "A playing field stood on edge, stretched around a world.", "push 6%", ""),
    (49.12, 54.50, "NASA", "PIA17156", None, "Why does something that wide look so finished, and so fragile?", "push 6%", ""),
    (54.50, 59.50, "NASA", "PIA17474", None, "Because you are seeing sunlight on ice, not a wall.", "push 6%", ""),
    (59.50, 64.50, "NASA", "PIA07872", None, "Photons bounce off clean water ice and come back almost white.", "push 6%", ""),
    (64.50, 69.50, "NASA", "PIA21628", None, "A little dust stains the older lanes a warmer colour.", "push 6%", ""),
    (69.50, 74.50, "NASA", "PIA06193", None, "The mass under that shine is small for the area it covers.", "push 6%", ""),
    (74.50, 79.50, "NASA", "PIA05075", None, "Cassini weighed the rings on its last orbits and found less than many maps had assumed —", "push 6%", ""),
    (79.50, 84.50, "NASA", "PIA00335", None, "on the order of two fifths of the little moon Mimas.", "push 6%", ""),
    (84.50, 89.50, "NASA", "PIA05076", None, "A lot of scenery. Not a lot of stuff. The mystery starts as a fall, not as a monument.", "push 6%", ""),
    (89.50, 94.50, "NASA", "PIA08963", None, "But the picture that brought you here is already the danger.", "push 6%", ""),
    (94.50, 99.50, "NASA", "PIA14629", None, "Does the fall ever stop? It does not stop while you are watching.", "push 6%", ""),
    (99.50, 104.50, "NASA", "PIA21339", None, "Gravity keeps every chunk moving. The smallest grains are already leaking inward.", "push 6%", ""),
    (104.50, 109.50, "NASA", "PIA01388", None, "What would you see if you waited? Not a collapse in the news.", "push 6%", ""),
    (109.50, 114.50, "NASA", "PIA08850", None, "A slow thinning. Then a planet that has spent the jewellery.", "push 6%", ""),
    (114.50, 118.16, "NASA", "PIA18295", None, "How long that takes is the question we are saving for the rain.", "push 5%", ""),
    # 118.16 is short 3.66 — OK
    (118.16, 122.80, "NASA", "PIA21058", None, "Now the question changes. What is that jewellery made of?", "push 6%", ""),
    (122.80, 127.50, "NASA", "PIA02275", None, "Come in close enough that the blade breaks into pieces.", "push 6%", ""),
    (127.50, 132.50, "NASA", "PIA21057", None, "Ice. Not rock. Water ice, the same bright mineral as a comet,", "push 6%", ""),
    (132.50, 137.50, "NASA", "PIA11569", None, "dirty in places and clean in others. Most of the mass sits in chunks you could hold,", "push 6%", ""),
    (137.50, 142.50, "NASA", "PIA01486", None, "or in boulders the size of a house.", "push 6%", ""),
    (142.50, 147.50, "NASA", "PIA09805", None, "Rocky dust rides with the ice and slowly stains it cream to tan.", "push 6%", ""),
    (147.50, 153.00, "NASA", "PIA21618", None, "Why call it a ring if it is only a crowd of snowballs? Because the crowd is flat.", "push 6%", ""),
    (153.00, 158.50, "NASA", "PIA12727", None, "Saturn's gravity, and the moons that shepherd the edges, pack the paths into a plane.", "push 6%", ""),
    (158.50, 163.50, "NASA", "PIA06092", None, "The gaps are emptier roads. The ice that remains still circles.", "push 6%", ""),
    (163.50, 168.50, "NASA", "PIA07616", None, "It does not sit. There is no roof.", "push 6%", ""),
    (168.50, 174.00, "OMNI", OMNI1, 0.00, "Drop through those ten metres and you are in open space again.", "", ""),
    (174.00, 179.00, "NASA", "PIA21621", None, "The atmosphere sits far below the inner edge, banded and pale.", "push 6%", ""),
    (179.00, 184.00, "NASA", "PIA12641", None, "The unknown is not the recipe. The unknown is the leak.", "push 6%", ""),
    (184.00, 189.00, "NASA", "PIA21886", None, "However bright the ice looks, brightness is not a promise that it stays.", "push 6%", ""),
    (189.00, 194.50, "NASA", "PIA08844", None, "That is the first answer: the famous sheet is only ice,", "push 6%", ""),
    (194.50, 200.00, "NASA", "PIA14623", None, "and it is already slipping away.", "push 6%", ""),
    (200.00, 205.50, "NASA", "PIA20502", None, "We make one of these every week. Subscribing is how the next one finds you.", "push 5%", ""),
    (205.50, 207.70, "CARD", "The Rain Into Saturn", None, "", "", ""),
    # Goddard once, 5.58s of the visualisation
    (207.70, 213.30, "GODDARD", GODDARD, 0.00, "Here is one way they go — the smallest grains get a charge.", "", ""),
    (213.30, 218.50, "NASA", "PIA16842", None, "Sunlight and the plasma around Saturn knock electrons about, and a tiny piece of ice stops being neutral.", "push 5%", "Illustration"),
    (218.50, 223.50, "NASA", "PIA13697", None, "Saturn's magnetic field already threads the ring plane. A charged grain feels that field.", "push 5%", "Saturn's magnetic field"),
    (223.50, 228.50, "NASA", "PIA08990", None, "It is lifted off its calm circle and guided down, along the magnetic path, into the upper atmosphere.", "push 6%", ""),
    (228.50, 233.50, "NASA", "PIA17150", None, "There the ice becomes vapour. Water, arriving from above. Ring rain.", "push 6%", ""),
    (233.50, 238.50, "NASA", "PIA18321", None, "We did not need a spacecraft inside that rain to know it was there.", "push 6%", ""),
    (238.50, 243.50, "NASA", "PIA21892", None, "Astronomers on Earth, using the Keck telescope, watched the glow of that water in Saturn's upper air", "push 5%", ""),
    (243.50, 248.50, "NASA", "PIA21345", None, "and measured how fast the ice was leaving.", "push 6%", ""),
    (248.50, 254.00, "NASA", "PIA21047", None, "At that magnetic rain rate alone, the sheet would last about three hundred million years.", "push 6%", ""),
    (254.00, 259.00, "NASA", "PIA21439", None, "But that is only one path down. Cassini went closer.", "push 5%", "illustration"),
    (259.00, 264.00, "NASA", "PIA22767", None, "In 2017 the orbiter flew twenty-two times through the gap", "push 5%", "illustration"),
    (264.00, 269.00, "NASA", "PIA22768", None, "between the innermost ring and the cloud tops.", "push 5%", "illustration"),
    (269.00, 274.00, "NASA", "PIA22766", None, "It was not sampling the magnetic rain from mid-latitudes.", "push 5%", "illustration"),
    (274.00, 279.50, "NASA", "PIA21440", None, "It was flying through something bigger: material pouring off the innermost ring —", "push 5%", "illustration"),
    (279.50, 284.50, "NASA", "PIA21895", None, "the D ring — straight into Saturn's equator.", "push 6%", ""),
    (284.50, 289.50, "NASA", "PIA21356", None, "That equatorial inflow is a heavier leak than the magnetic rain alone.", "push 6%", ""),
    (289.50, 295.00, "NASA", "PIA21903", None, "Add it to the books, and the sheet's remaining life drops to around a hundred million years.", "push 6%", ""),
    (295.00, 300.50, "NASA", "PIA21343", None, "So how long does the bright sheet have?", "push 6%", ""),
    (300.50, 306.00, "NASA", "PIA21046", None, "Put both measurements together and the honest answer is a range,", "push 6%", ""),
    (306.00, 311.50, "NASA", "PIA12677", None, "somewhere between about a hundred and three hundred million years.", "push 6%", ""),
    (311.50, 316.50, "NASA", "PIA08265", None, "A blink next to Saturn's four and a half billion years.", "push 6%", ""),
    (316.50, 321.50, "NASA", "PIA08869", None, "You would not see either leak as weather from a window.", "push 6%", ""),
    (321.50, 326.50, "NASA", "PIA11671", None, "The grains are too fine, and the fall is too spread out.", "push 6%", ""),
    (326.50, 331.50, "NASA", "PIA06175", None, "What you would see, if you could watch for an age,", "push 6%", ""),
    # RING picture under growing thinner — not Hubble seasons
    (331.50, 337.52, "NASA", "PIA02241", None, "is the sheet growing thinner, while Saturn's bands stay put.", "push 6%", ""),
    (337.52, 342.50, "NASA", "PIA01966", None, "Now look backward. The rain implies a beginning.", "push 6%", ""),
    (342.50, 347.00, "NASA", "PIA01969", None, "Wind the clock back along that same scale,", "push 6%", ""),
    # later young — remaining stretch after hook 0–2.84 → start 2.84
    # later young — after hook used 0.00–3.70; clip ends at 8.00 → max 4.30s
    (347.00, 351.30, "AI", YOUNG, 3.70, "and the sheet changes. More mass. Cleaner ice. A harder white,", "", ""),
    (351.30, 356.00, "NASA", "PIA01940", None, "because the dust had not had time to dirty it.", "push 6%", ""),
    # S3 / S5 / S5b spares for "when the rings were new"
    (356.00, 361.00, "NASA", "PIA07873", None, "Saturn would still have been the ringed one — only more so.", "push 6%", ""),
    (361.00, 366.00, "NASA", "PIA18278", None, "A broader blade. A brighter one.", "push 6%", ""),
    (366.00, 371.00, "NASA", "PIA17176", None, "The planet underneath was already the planet. The rings look like a late arrival.", "push 6%", ""),
    (371.00, 376.00, "NASA", "PIA11141", None, "Why \"new\", when Saturn itself is about four and a half billion years old?", "push 6%", ""),
    (376.00, 381.00, "NASA", "PIA10081", None, "Because a heavy, ancient ring would still be heavy, unless most of its mass has already gone in.", "push 5%", "Illustration"),
    (381.00, 386.00, "NASA", "PIA22418", None, "Most researchers read Cassini's low mass as young — a few hundred million years at most.", "push 6%", ""),
    (386.00, 391.00, "NASA", "PIA18274", None, "A few argue the rings could still be old, and hide their age another way.", "push 6%", ""),
    (391.00, 396.00, "NASA", "PIA18301", None, "The debate is open. The honest line is narrower than a slogan.", "push 6%", ""),
    (396.00, 401.00, "NASA", "PIA20497", None, "The rings you see are ice, they are already leaving, and their birthday is not settled.", "push 6%", ""),
    (401.00, 406.00, "NASA", "PIA06425", None, "What if a moon came too close, and came apart?", "push 6%", "an idea"),
    (406.00, 411.00, "NASA", "PIA12785", None, "That idea fits a young mass, and it is still an idea.", "push 6%", "an idea"),
    (411.00, 416.00, "NASA", "PIA12786", None, "Inside the Roche limit, Saturn's gravity can pull a moon into rubble,", "push 6%", "an idea"),
    (416.00, 421.00, "NASA", "PIA08903", None, "and rubble in a plane becomes a ring.", "push 6%", "an idea"),
    (421.00, 426.00, "NASA", "PIA06098", None, "Whatever their birthday, the rings you know are ice,", "push 6%", ""),
    (426.00, 428.50, "CARD", "Saturn Without Them", None, "", "", ""),
    # later bare — after hook used 0.00–3.70; clip ends 8.00 → max 4.30s
    (428.50, 432.80, "AI", BARE, 3.70, "Take the ice away, and stay with the planet.", "", ""),
    (432.80, 437.50, "NASA", "PIA18294", None, "Saturn is still there. Pale gold bands.", "push 6%", ""),
    (437.50, 442.50, "OMNI", OMNI2, 0.00, "A fast day, a little over ten hours,", "", ""),
    (442.50, 447.50, "NASA", "PIA14945", None, "written as soft stripes in a deep atmosphere.", "push 6%", ""),
    (447.50, 452.50, "NASA", "PIA20507", None, "The curve of the planet runs clean.", "push 6%", ""),
    (452.50, 457.50, "NASA", "PIA21052", None, "The shadow the rings used to cast on the clouds is gone.", "push 6%", ""),
    (457.50, 462.50, "NASA", "PIA21888", None, "The famous thing was never the body. It was the ice in orbit around the body.", "push 6%", ""),
    (462.50, 467.50, "NASA", "PIA20528", None, "What would you see, standing in that later sky? A giant,", "push 6%", ""),
    (467.50, 472.50, "NASA", "PIA21334", None, "banded and bright, ordinary once you stop using the rings as the definition.", "push 6%", ""),
    (472.50, 477.50, "NASA", "PIA21327", None, "You would feel the oddness in the absence. The planet does not notice.", "push 6%", ""),
    (477.50, 482.50, "NASA", "PIA11613", None, "The rain simply finishes, and the paths that carried it have nothing left to carry.", "push 6%", ""),
    (482.50, 487.50, "NASA", "PIA17148", None, "So the whole story fits in one breath. You would see a thin sheet of water ice,", "push 6%", ""),
    # RING under raining — not aurora
    (487.50, 492.50, "NASA", "PIA18367", None, "vast and bright, already raining into Saturn.", "push 6%", ""),
    (492.50, 498.00, "NASA", "PIA18313", None, "Magnetic rain measured from Earth, and a heavier equatorial leak Cassini flew through on its last dives.", "push 6%", ""),
    (498.00, 503.00, "NASA", "PIA17127", None, "The mass is too small for a forever-disc,", "push 6%", ""),
    (503.00, 508.50, "NASA", "PIA18314", None, "so the clock sits somewhere between about a hundred and three hundred million years.", "push 6%", ""),
    (508.50, 513.50, "NASA", "PIA12590", None, "The rings are a phase. Saturn is the thing that remains.", "push 6%", ""),
    (513.50, 518.50, "NASA", "PIA20530", None, "What else in the sky are you treating as permanent only because it is bright?", "push 6%", ""),
    (518.50, 523.62, "NASA", "PIA21350", None, "The rings are the clearest case. The mystery is how much of that sky is temporary. Next: What Happens When the Last Star Dies?", "push 5%", ""),
    (523.62, 523.62 + END_HOLD, "NASA", "PIA17218", None, "[END HOLD — music fades ~10s; picture fades last ~2s]", "slow push 7%", ""),
]


def main() -> int:
    fields = ["row", "vo_in", "vo_out", "source", "id", "src_in", "src_out", "move", "vo_text", "caption"]
    out_rows = []
    used = []
    for a, b, source, rid, src_in, text, move, caption in RAW:
        d = round(b - a, 2)
        if source == "NASA":
            assert rid in POOL, f"not in pool: {rid}"
            assert rid not in used, f"duplicate NASA {rid}"
            used.append(rid)
            if rid in HUBBLE_SEASONS and re.search(r"\bthin", text, re.I):
                raise SystemExit(f"Hubble seasons under thin: {rid}")
            if rid in AURORA and re.search(r"\brain|raining|pour", text, re.I):
                raise SystemExit(f"aurora under rain: {rid}")
        si = so = ""
        if source in ("AI", "OMNI", "GODDARD"):
            assert src_in is not None
            si = f"{float(src_in):.2f}"
            so = f"{float(src_in) + d:.2f}"
        out_rows.append({
            "vo_in": f"{a:.2f}",
            "vo_out": f"{b:.2f}",
            "source": source,
            "id": rid,
            "src_in": si,
            "src_out": so,
            "move": move if source == "NASA" else "",
            "vo_text": text,
            "caption": caption,
        })

    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, r in enumerate(out_rows, 1):
            w.writerow({"row": i, **r})

    print(f"wrote {OUT} ({len(out_rows)} rows, {len(used)} NASA)")
    r = subprocess.run(
        [sys.executable, str(HERE / "check_shot_list.py"), str(OUT), "--vo-end", str(VO_END)],
        cwd=str(HERE),
        capture_output=True,
        text=True,
    )
    print(r.stdout, end="")
    print(r.stderr, end="")
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
