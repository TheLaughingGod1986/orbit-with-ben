#!/usr/bin/env python3
"""Sun 022: build SHOT_LIST v01 from the locked VO timings, the verified NASA pool and the three code graphics.

Claude, 7 Oct 2026. No shot list existed (Grok out of credit), and the first cut is due Thu 8-Fri 9 for the Sat 10
review. Run it on any machine (no media needed):

  python3 _build_shot_list_v01.py            # writes shot_list_v01.csv and SHOT_LIST_v01.md beside this file

How it works
  - Cut points: every anchor below (a script beat with its own picture) starts a new shot on the anchor's first word.
  - Between anchors, shots are cut every 4-6 s on the gap before a word, preferring sentence ends, so no cut lands
    mid-word (lessons §2: never clip a line). Inside the first 20 s, preview cuts may be as short as 1.5 s.
  - Pictures between anchors come from that chapter's pool list in order, with no still used more than 3 times and
    no SVS clip in more than 2 stretches (the open/end SDO motion excepted, as the script asks for the return).
  - Every rule is checked before anything is written; it exits 1 and writes nothing if one fails.

Columns (Saturn's shot_list format, plus three): row, vo_in, vo_out, source, id, src_in, src_out, move, vo_text,
caption, chapter, grade, fallback.
  source  NASA (still) | GODDARD (SVS motion, muted) | CODE (code_graphics.py output) | OMNI (Vertex Omni, Orbit) |
          EDIT (two-disc composite built in the edit)
  grade   a colour/brightness instruction for the young or future Sun (plan: grade one SDO disc, no red giant)
  fallback what to use if the row's source isn't available (Omni down: stay on the world pictures)
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORDS = json.loads((HERE.parent / "02_Voiceover" / "words.json").read_text())
POOL = {e["nasa_id"]: e for e in json.loads((HERE / "nasa_pool_v01.json").read_text())}
VO_END = WORDS["duration_s"]
END_HOLD = 16.0          # plan: 15-20 s end hold on moving picture, end screen added in Studio
MIN_S, MAX_S, TARGET = 3.5, 6.5, 5.0
HOOK_END, HOOK_MIN = 20.0, 1.5
STILL_MAX_USES = 3
SVS_MAX_STRETCHES = 2
CARD_S = 2.5             # lower-third chapter card over the chapter's first shot

ws = WORDS["words"]
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower())
SEQ = [norm(w["word"]) for w in ws]


def at(phrase: str) -> float:
    p = [norm(x) for x in phrase.split()]
    hits = [i for i in range(len(SEQ)) if SEQ[i:i + len(p)] == p]
    if len(hits) != 1:
        raise SystemExit(f"anchor phrase {phrase!r} found {len(hits)} times in words.json")
    return ws[hits[0]]["start"]


# ----------------------------------------------------------------------------- chapters (VO start of first line)
CHAPTERS = [
    ("open", None, 0.0),
    ("ch1", "The Climb You Cannot See", at("The motion is real")),
    ("ch2", "Brighter While It Runs Down", at("The fuel is hydrogen")),
    ("sub", None, at("We make one of these")),
    ("ch3", "When the Light Was Less", at("But the sun over your street")),  # bridge line, card on "Wind the clock back"
    ("ch4", "Ten Percent More", at("Now run today's pace")),
    ("ch5", "The Sun You Already Have", at("However bright that future")),  # bridge line, card on "You are standing"
    ("end", None, at("The bigger question")),
]
CARDS = {"ch1": at("The motion is real"), "ch2": at("The fuel is hydrogen"), "ch3": at("Wind the clock back"),
         "ch4": at("Now run today's pace"), "ch5": at("You are standing in the middle")}

# ----------------------------------------------------------------------------- anchors: (phrase, source, id, move/src, grade, fallback)
# The 'today' Sun in visible light: SDO HMI continuum full disc, 6 Feb 2019 (PIA21218, "Spotless February"); crop the
# timestamp. Was GSFC e002035, which is an AIA 335 A extreme-UV disc in false cyan, not white light (Gemini J0008).
WHITE = "PIA21218"
ANCHORS = [
    # Open: frame 0 is real SDO motion, prominence mid-rise (VISUAL MUST). Quick preview cuts allowed to 20 s.
    ("The sun is getting brighter why does", "GODDARD", "SVS 11517", "stretch 1: prominence material already rising off the limb at frame 0", "", "SVS 13778 (mute)"),
    ("You are looking at the light", "NASA", "iss074e0494675", "push 4%", "", ""),
    ("and a prominence is already lifting", "GODDARD", "SVS 13778", "stretch 2: prominence lifting off the limb (mute: licensed music)", "", "GSFC_20171208_Archive_e002168"),
    ("The danger is not that ribbon", "NASA", "GSFC_20171208_Archive_e002168", "push 5%", "", ""),
    ("It is not the spots", "NASA", "PIA19876", "push 4% towards the spot group (crop the caption line)", "", ""),
    ("It is not the warming", "NASA", "s85e5052", "pan L-R 4%", "", ""),
    ("In this film I will show you", "NASA", WHITE, "push 4%", "", ""),
    # Ch1: the wrong clock; the zoom graphic carries 'a slow upward line beside an eleven-year wobble'
    ("The motion is real", "GODDARD", "SVS 13778", "stretch 1: prominence eruption (mute: licensed music)", "", "GSFC_20171208_Archive_e002168"),
    ("So is the sun getting brighter", "NASA", WHITE, "push 5%", "", ""),
    ("By a slow rise in the light", "CODE", "zoom_nolabels.mp4", "0-12 s (no baked captions: VISUAL MUST)", "", ""),
    ("What if the spots were", "GODDARD", "SVS 3548", "solar minimum, then cut to SVS 3549 maximum", "", ""),
    ("Spots darken a patch", "GODDARD", "SVS 3549", "solar maximum", "", ""),
    ("The warming measured on earth", "NASA", "iss017e011603", "pan R-L 4%", "", ""),
    ("Now the strange question", "NASA", WHITE, "pull 5%", "", ""),
    # Ch2: the core graphic in two stretches; interior flows behind
    ("The fuel is hydrogen", "GODDARD", "SVS 31400", "stretch 1: churning interior flows", "", ""),
    ("Deep inside", "CODE", "core_nolabels.mp4", "0-12 s: H to He, core tightening (no text)", "", ""),
    ("The radiation that leaves the surface", "NASA", "iss074e0494675", "pan L-R 4%", "", ""),
    ("Here is the turn", "GODDARD", "SVS 31400", "stretch 2", "", ""),
    ("So the core contracts", "CODE", "core_nolabels.mp4", "second pass from 6 s: the core tightens and the light floods out", "", ""),
    ("That is the first payoff", "GODDARD", "SVS 11112", "gradient Sun", "", ""),
    ("What would you see across", "NASA", WHITE, "push 6%", "", ""),
    ("We make one of these", "GODDARD", "SVS 5649", "stretch 1: restless disc (no on-screen text)", "", ""),
    ("But the sun over your street", "NASA", "s09-11-675", "push 4%", "", ""),
    # Ch3: young dim Sun = one graded SDO disc against early-Earth and wet-rock pictures; Orbit beat via Omni
    ("Wind the clock back", "NASA", WHITE, "pull 5%", "young Sun: -30% brightness, slightly cooler (orange-ward)", ""),
    ("Solar models put the early sun", "GODDARD", "SVS 11853", "faint young Sun stretch, picture only (mute, no text frames)", "", "NASA GSFC_20171208_Archive_e000888"),
    ("Then the paradox arrives", "NASA", "GSFC_20171208_Archive_e000888", "push 5%", "", ""),
    ("The usual repair", "NASA", "s36-07-012", "pan L-R 4%", "", ""),
    ("What would you have seen from that shore", "OMNI", "Orbit young-Sun shore",
     "Orbit hangs small against the dimmer disc, visor tilted up, one hand lifted (ORBIT ACTS); 5-6 s, one take",
     "dim young disc in plate", "NASA s04-41-1206 push 4% (Omni down: stay on the world)"),
    ("Until the two suns sit side by side", "EDIT", "two-disc compare", f"{WHITE} twice, same framing: left graded young, right today",
     "left -30% and cooler; right as shot", ""),
    # Ch4: today's pace forward; larger, brighter disc over thin sea and cloud; Orbit beat 2
    ("Now run today's pace", "NASA", WHITE, "push 5%", "", ""),
    ("More light warms the surface", "NASA", "iss072e769023", "push 4%", "", ""),
    ("Water vapor is itself", "NASA", "sts064-83-099", "pan R-L 4%", "", ""),
    ("Could a shoreline survive", "OMNI", "Orbit brighter-Sun cloud",
     "Orbit tips towards the brighter disc, then towards a thin bright skin of cloud; small, low in frame; 5-6 s",
     "future Sun: +10% brightness, scale 1.04", "NASA iss071e364425 push 4% (Omni down: stay on the world)"),
    ("The disk swells only slowly", "NASA", WHITE, "push 4%", "future Sun: +10% brightness, scale 1.04 (no red giant)", ""),
    ("The blue can last", "NASA", "iss071e439624", "pan L-R 4%", "", ""),
    ("However bright that future", "NASA", "s39-610-037", "push 4%", "", ""),
    # Ch5: recap of three clocks; end returns to the opening Sun in motion, held for the end screen
    ("You are standing in the middle", "GODDARD", "SVS 5649", "stretch 2", "", ""),
    # words.json hears "Free clocks" at 457.04 s where the script says "Three clocks": the anchor stays as heard; the
    # row's text is corrected below, and the pickup take replaces the audio (J0007).
    ("Free clocks", "CODE", "clocks.mp4", "0-10 s: three clocks lit in turn", "", ""),
    ("The sun is getting brighter because", "NASA", WHITE, "push 5%", "", ""),
    ("What if the real question", "NASA", "iss071e439624", "pull 4%", "", ""),
    ("The bigger question", "NASA", "as08-16-2588", "push 4%", "", ""),
    ("Next door", "GODDARD", "SVS 11517", "stretch 3: back to the opening eruption, a later stretch, in motion; hold to the end", "", ""),
]

PICTURE_SWAPS = {
    # "This one was over in a day" (pickup, J0010) needs the one-day prominence (PIA22123: Nov. 29-30, 2017) on screen
    "It can hang, fall back": {"source": "NASA", "id": "PIA22123", "move": "drift up 4% (continues row 10)", "grade": "",
                               "caption": "PICKUP: lay sun_pickup_over_in_a_day_v01 over \"In a day, it is over.\""},
    "Roughly 30 % dimmer": {"source": "NASA", "id": WHITE, "move": "pull 4%", "grade": "young Sun: -30% brightness, slightly cooler (orange-ward)"},
    "The 10 % sun is further off": {"source": "NASA", "id": "GSFC_20171208_Archive_e002131", "move": "push 4% (city lights)", "grade": ""},
    "A 10th of 1 % up and down": {"source": "NASA", "id": "PIA19876", "move": "pull 4% from the spot group", "grade": ""},
    "Earth has lived the dimmer half": {"source": "NASA", "id": "s04-41-1206", "move": "pan L-R 4%", "grade": ""},
    "star that brightens while it burns": {"source": "NASA", "id": WHITE, "move": "push 5%", "grade": ""},
}

# Pool lists per chapter for the shots between anchors (order = preference). White-light lines prefer the white disc.
PLAYLIST = {
    "open": ["PIA22123", "GSFC_20171208_Archive_e001363", "GSFC_20171208_Archive_e000896"],
    "ch1": ["PIA22123", "GSFC_20171208_Archive_e001052", "GSFC_20171208_Archive_e000970", "PIA19876", "GSFC_20171208_Archive_e000923",
            "PIA20881", "s85e5052", "GSFC_20171208_Archive_e001363", "PIA22662"],
    "ch2": ["PIA20881", "PIA22662", "PIA22645", "PIA21764", "GSFC_20171208_Archive_e001978", "PIA22360", "PIA15377", "PIA22724",
            "GSFC_20171208_Archive_e000808", "GSFC_20171208_Archive_e000393"],
    "sub": ["GSFC_20171208_Archive_e001517"],
    "ch3": ["as4-01-750", "s04-41-1206", "sl4-142-4577", "S66-25771", "GSFC_20171208_Archive_e000888", "ast-27-2339"],
    "ch4": ["S06-46-617", "iss071e364425", "iss072e617674", "s44-94-051", "GSFC_20171208_Archive_e002131", "STS067-709-007",
            "as08-16-2588", "sts065-86-095", "GSFC_20171208_Archive_e002130"],
    "ch5": ["GSFC_20171208_Archive_e000414", "GSFC_20171208_Archive_e001517", "PIA17669", "GSFC_20171208_Archive_e000759",
            "GSFC_20171208_Archive_e000991", "s09-11-675"],
    "end": ["GSFC_20171208_Archive_e002131", "iss071e439624"],
}
MOVES = ["push 5%", "pan L-R 4%", "pull 5%", "pan R-L 4%", "drift up 4%"]
SUNSPOT = {"PIA21783", "GSFC_20171208_Archive_e000923", "PIA19876", "GSFC_20171208_Archive_e000922", "GSFC_20171208_Archive_e000920"}
WOBBLE_OK = [(at("It is not the spots"), at("It is not the warming")), (at("The motion is real"), at("Now the strange question")),
             (at("Overhead is the star"), at("Free clocks"))]  # the recap: row 95 names the 0.1% wobble "with the spots"


def chapter_of(t: float) -> str:
    cur = "open"
    for name, _, start in CHAPTERS:
        if t + 1e-6 >= start:
            cur = name
    return cur


def text_between(a: float, b: float) -> str:
    return " ".join(w["word"] for w in ws if a - 1e-6 <= w["start"] < b - 1e-6)


def split_span(a: float, b: float) -> list[float]:
    """Cut times strictly inside (a, b): 4-6 s apart, each on a word onset, preferring sentence ends."""
    cuts, t = [], a
    while b - t > MAX_S:
        lo, hi = t + MIN_S, min(t + MAX_S, b - MIN_S)
        if hi < lo:
            hi = b - MIN_S if b - MIN_S > t + 1.5 else t + MAX_S
        cands = [i for i in range(1, len(ws)) if lo <= ws[i]["start"] <= hi]
        if not cands:
            break
        def score(i):
            ends = ws[i - 1]["word"].rstrip().endswith((".", "?", "!"))
            gap = ws[i]["start"] - ws[i - 1]["end"]
            return (ends, round(gap, 2), -abs(ws[i]["start"] - (t + TARGET)))
        best = max(cands, key=score)
        cuts.append(ws[best]["start"])
        t = ws[best]["start"]
    return cuts


def build() -> list[dict]:
    anchor_t = sorted(((at(p), (p, src, id_, mv, gr, fb)) for p, src, id_, mv, gr, fb in ANCHORS), key=lambda x: x[0])
    if anchor_t[0][0] != 0.0:
        raise SystemExit("the first anchor must start at 0.0 (frame 0)")
    bounds = [t for t, _ in anchor_t] + [VO_END]
    uses: dict[str, int] = {}
    stretches: dict[str, int] = {}
    pos = {k: 0 for k in PLAYLIST}
    rows: list[dict] = []
    for k, (t0, (phrase, src, id_, mv, gr, fb)) in enumerate(anchor_t):
        t1 = bounds[k + 1]
        last = k == len(anchor_t) - 1
        # The end hold runs on the last anchor's moving picture; earlier spans are cut every 4-6 s.
        cuts = [] if (last or src in ("CODE", "OMNI", "EDIT")) and (t1 - t0) <= 12.5 else split_span(t0, t1)
        pieces = list(zip([t0] + cuts, cuts + [t1]))
        for j, (a, b) in enumerate(pieces):
            ch = chapter_of(a)
            if j == 0:
                row = {"source": src, "id": id_, "move": mv if src == "NASA" else "", "src_in": "" if src == "NASA" else mv,
                       "grade": gr, "fallback": fb}
            else:
                lst = PLAYLIST.get(ch) or PLAYLIST["ch5"]
                for _ in range(len(lst) * 2):
                    cand = lst[pos[ch] % len(lst)]
                    pos[ch] += 1
                    if uses.get(cand, 0) < STILL_MAX_USES and (not rows or rows[-1]["id"] != cand) and cand not in SUNSPOT:
                        break
                row = {"source": "NASA", "id": cand, "move": MOVES[len(rows) % len(MOVES)], "src_in": "", "grade": "", "fallback": ""}
            if row["source"] == "NASA":
                uses[row["id"]] = uses.get(row["id"], 0) + 1
            if row["source"] == "GODDARD" and j == 0:
                stretches[row["id"]] = stretches.get(row["id"], 0) + 1
            vo_out = b if not (last and j == len(pieces) - 1) else round(VO_END + END_HOLD, 2)
            rows.append({"vo_in": round(a, 2), "vo_out": round(vo_out, 2), **row, "src_out": "", "vo_text": text_between(a, b),
                         "caption": "", "chapter": ch})
    # chapter cards ride on the first shot at or after each card time (lower third, ~2.5 s, 0.7 s breath before)
    for ch, t in CARDS.items():
        r = next(r for r in rows if r["vo_in"] >= t - 0.01)
        title = dict((n, c) for n, c, _ in CHAPTERS)[ch]
        r["caption"] = f"CHAPTER CARD (lower third, {CARD_S} s): {title}"
    # Picture swaps after Gemini's picture-vs-words check (J0008, GEMINI_PICTURE_CHECK_v01.md; Claude's rulings, 7 Oct).
    # Applied after the cut so the timing stays on the lock; each prefix must match exactly one row.
    for prefix, swap in PICTURE_SWAPS.items():
        hits = [r for r in rows if r["vo_text"].startswith(prefix)]
        if len(hits) != 1:
            raise SystemExit(f"picture swap {prefix!r} matched {len(hits)} rows")
        hits[0].update(swap)
    # VO pickups laid over the lock (Claude order #99 6037545918; take sun_pickup_three_clocks_v01, J0007 PASS c6ba945)
    for r in rows:
        if r["vo_text"].startswith("Free clocks."):
            r["vo_text"] = "Three clocks." + r["vo_text"][len("Free clocks."):]
            r["caption"] = (r["caption"] + "; " if r["caption"] else "") + \
                "PICKUP: lay sun_pickup_three_clocks_v01 over this row (match loudness and room tone at both joins)"
    for i, r in enumerate(rows, 1):
        r["row"] = i
    return rows, uses, stretches


def check(rows, uses, stretches) -> list[str]:
    bad = []
    if rows[0]["vo_in"] != 0.0 or rows[0]["source"] != "GODDARD":
        bad.append("frame 0 must be real SDO motion (GODDARD), not a still or Orbit")
    for a, b in zip(rows, rows[1:]):
        if abs(a["vo_out"] - b["vo_in"]) > 0.01:
            bad.append(f"rows {a['row']}-{b['row']} don't meet ({a['vo_out']} vs {b['vo_in']})")
    if abs(rows[-1]["vo_out"] - (VO_END + END_HOLD)) > 0.01:
        bad.append("the last row must carry the end hold")
    for r in rows[:-1]:
        d = r["vo_out"] - r["vo_in"]
        lo = HOOK_MIN if r["vo_in"] < HOOK_END else (3.0 if r["source"] in ("OMNI", "CODE", "EDIT") else MIN_S)
        hi = 12.5 if r["source"] in ("CODE", "OMNI", "EDIT") else MAX_S
        if hi == MAX_S and d < 2 * MIN_S:
            hi = 7.0   # a span under 7 s can't be cut into two shots of 3.5 s or more
        if not lo - 1e-6 <= d <= hi + 1e-6:
            bad.append(f"row {r['row']} ({r['source']} {r['id']}) runs {d:.2f} s, outside {lo}-{hi} s")
        if r["source"] == "NASA" and r["id"] not in POOL:
            bad.append(f"row {r['row']}: {r['id']} isn't in nasa_pool_v01.json")
        if r["source"] == "NASA" and not r["move"]:
            bad.append(f"row {r['row']}: still with no camera move")
        if r["id"] in SUNSPOT and not any(a - 0.01 <= r["vo_in"] < b for a, b in WOBBLE_OK):
            bad.append(f"row {r['row']}: sunspot picture outside the wobble lines (it illustrates 0.1%, never the climb)")
        if r["source"] == "OMNI" and r["vo_in"] < 1.0:
            bad.append("Orbit at frame 0")
    for k, n in uses.items():
        if n > STILL_MAX_USES and k != WHITE:
            bad.append(f"{k} used {n} times (max {STILL_MAX_USES})")
    for k, n in stretches.items():
        if n > SVS_MAX_STRETCHES:
            bad.append(f"{k} cut into {n} stretches (max {SVS_MAX_STRETCHES})")
    cards = sum(1 for r in rows if r["caption"].startswith("CHAPTER CARD"))
    if cards != 5:
        bad.append(f"{cards} chapter cards, expected 5")
    if rows[-1]["source"] != "GODDARD":
        bad.append("the end must return to the opening Sun in motion")
    return bad


def main() -> int:
    rows, uses, stretches = build()
    bad = check(rows, uses, stretches)
    if bad:
        print("shot list v01: FAIL")
        for b in bad:
            print(" -", b)
        return 1
    cols = ["row", "vo_in", "vo_out", "source", "id", "src_in", "src_out", "move", "vo_text", "caption", "chapter", "grade", "fallback"]
    with open(HERE / "shot_list_v01.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})
    write_md(rows, uses)
    by = {}
    for r in rows:
        by[r["source"]] = by.get(r["source"], 0) + 1
    print(f"shot list v01: PASS · {len(rows)} rows · VO {VO_END:.2f} s + {END_HOLD:.0f} s end hold · " + ", ".join(f"{k} {v}" for k, v in sorted(by.items())))
    return 0


def write_md(rows, uses):
    L = [
        "# Sun 022: SHOT_LIST v01 (Claude, 7 Oct 2026)",
        "",
        "**Film:** 022 *Is the Sun Getting Brighter?* · airs **Sun 18 Oct 18:00 London** · cut review **Sat 10 Oct** · final OK **Tue 13 Oct**  ",
        f"**VO lock:** `02_Voiceover/words.json` ({VO_END:.2f} s, {len(ws)} words) · **Script:** `01_Script/sun_brighter_script_master_v02.md`  ",
        "**Built by:** `_build_shot_list_v01.py` (re-run it after any change; it checks every rule below and writes nothing on a FAIL). "
        "The machine-readable list is `shot_list_v01.csv` (Saturn's columns, plus chapter, grade and fallback).",
        "",
        "Written by Claude because no shot list existed and Grok is out of credit. **Claude PASSes it as written**; the assembler "
        "(Cursor while Grok is out) builds the first cut from the CSV, Thu 8-Fri 9 Oct.",
        "",
        "## Rules this list keeps",
        "",
        "| Rule | How |",
        "|---|---|",
        "| Frame 0 | Real SDO motion, **SVS 11517** (304+171 A), prominence material already rising. No fade, no title, no Orbit. (Was SVS 10925, an X5.4 flare close-up, not a prominence: Gemini J0008.) |",
        "| Pace | A new picture every 4-6 s, cut on the gap before a word (never mid-word). Preview cuts from 1.5 s inside the first 20 s. |",
        "| Chapter cards | Lower third, ~2.5 s, over the chapter's first shot, with the 0.7 s breath before it. No full-screen card. |",
        "| Stills | 16:9 fill with feathered blur, upscale at most about 2.35x, Ken Burns move as listed. Crop the SDO corner timestamp with the push. |",
        "| SVS motion | Muted, clean stretches with no on-screen text, credit 'NASA's Goddard Space Flight Center' + instrument. Max 2 stretches per clip. |",
        "| Sunspots | Only over the 0.1% wobble lines, never the 1% climb. |",
        "| Young / future Sun | One SDO disc **graded** (young -30% and cooler; future +10%, scale 1.04). **No red giant.** |",
        "| Orbit | Two Omni beats only (ch.3 and ch.4), small in frame, Vertex free credit only. **If Omni is down, use each row's fallback** and stay on the world pictures (plan, 3 Oct). |",
        "| Code graphics | `code_graphics.py` outputs: `zoom_nolabels.mp4` (ch.1), `core_nolabels.mp4` (ch.2, two passes), `clocks.mp4` (ch.5). |",
        f"| End | Back to the opening Sun in motion (SVS 11517, a later stretch), held {END_HOLD:.0f} s past the last word; end screen added in Studio. |",
        "| Mix | -14 LUFS, music the full runtime, fade under the last line. |",
        "",
        "## Shots",
        "",
        "| # | VO in-out (s) | Source | Picture | Move / stretch | Over the words | Card | Grade / fallback |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        words = r["vo_text"] if len(r["vo_text"]) <= 90 else r["vo_text"][:87] + "…"
        extra = " · ".join(x for x in (r["grade"], ("fallback: " + r["fallback"]) if r["fallback"] else "") if x)
        card = r["caption"].split(": ", 1)[1] if r["caption"] else ""
        L.append(f"| {r['row']} | {r['vo_in']:.2f}-{r['vo_out']:.2f} | {r['source']} | {r['id']} | {r['move'] or r['src_in']} | {words.replace('|', '/')} | {card} | {extra} |")
    L += ["", "## Credits", "", "Stills: from `nasa_pool_v01.json` (one line per picture used). SVS: NASA's Goddard Space Flight Center (Scientific Visualization Studio), per clip page.", ""]
    for k in sorted(uses):
        e = POOL[k]
        L.append(f"- {k}: {e['title']} · {e['credit']}")
    (HERE / "SHOT_LIST_v01.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    sys.exit(main())
