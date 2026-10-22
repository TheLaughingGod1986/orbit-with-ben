#!/usr/bin/env python3
"""en-GB captions for the Nearest Star 026 long, timed to the v06 picture lock.

The locked script's wording (01_Script/nearest_star_script_master_v01.md) is aligned
to the locked long VO (02_Voiceover/words.json, same 97,688 bytes as
OWB UAT/026_NearestStar_Long_VO/words.json). Whisper spellings never reach the
captions. The word times already sit on the picture clock: "Look" at 0.08 s,
"Your two eyes are a ruler." at 141.40 s (2:21), last word "gap" at 490.964 s,
picture 494.476 s. Built from the Light Speed 024 builder (J0048). J0326, 15 Oct 2026.
"""
import difflib, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
SCRIPT = PROJ / "01_Script" / "nearest_star_script_master_v01.md"
WORDS = PROJ / "02_Voiceover" / "words.json"
OUT = HERE / "Captions" / "nearest_star_long_v06_en-GB.srt"
MAX = 84  # two lines of 42


def norm(w):
    w = w.lower().replace("%", " percent")
    w = (w.replace("kilometers", "kilometres").replace("centimeters", "centimetres")
         .replace("meters", "metres").replace("traveled", "travelled"))
    w = re.sub(r"[^a-z0-9 ]", "", w)
    w = w.replace("thirtyeight", "thirty eight").replace("seventyseven", "seventy seven")
    out = []
    for t in w.split():
        if not t:
            continue
        if t == "1":
            out.append("one")
        elif t == "11":
            out.append("eleven")
        elif t == "20":
            out.append("twenty")
        elif t == "1838":
            out += ["eighteen", "thirty", "eight"]
        elif t == "1977":
            out += ["nineteen", "seventy", "seven"]
        else:
            out.append(t)
    return out


def prose():
    """Spoken lines only. The next-week pickup is not in the v05d picture lock
    (assemble: last word 490.964, then a 2.5 s hold and a 1.0 s fade)."""
    out = []
    for line in SCRIPT.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "[", "<!--")) or s.startswith("Next week:"):
            continue
        out.append(s)
    return " ".join(out)


def split_long(s):
    """Split a long sentence near its middle, preferring a comma, so no cue is a two-word orphan."""
    if len(s) <= MAX:
        return [s]
    mid = len(s) // 2
    commas = [m.end() for m in re.finditer(r",\s", s)]
    good = [c for c in commas if len(s) * 0.25 <= c <= len(s) * 0.75]
    cut = min(good, key=lambda c: abs(c - mid)) if good else min(
        (m.start() + 1 for m in re.finditer(r"\s", s)), key=lambda c: abs(c - mid))
    return split_long(s[:cut].strip()) + split_long(s[cut:].strip())


def chunks(text):
    out = []
    for s in re.split(r"(?<=[.?!])\s+", text):
        out += split_long(s)
    return [c for c in out if c]


def srt_time(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def two_lines(s):
    if len(s) <= 42:
        return s
    mid = len(s) // 2
    sp = min((i for i, c in enumerate(s) if c == " "), key=lambda i: abs(i - mid))
    return s[:sp] + "\n" + s[sp + 1:]


def main():
    ws = json.loads(WORDS.read_text())["words"]
    wn, wi = [], []
    for k, w in enumerate(ws):
        for t in norm(w["text"]):
            wn.append(t); wi.append(k)
    caps = chunks(prose())
    sn, si = [], []
    for c, cap in enumerate(caps):
        for t in norm(cap):
            sn.append(t); si.append(c)
    m = {}
    for a, b, n in difflib.SequenceMatcher(None, sn, wn, autojunk=False).get_matching_blocks():
        for k in range(n):
            m[a + k] = wi[b + k]
    rows = []
    for c, cap in enumerate(caps):
        idx = [k for k in range(len(sn)) if si[k] == c and k in m]
        rows.append([ws[m[idx[0]]]["start"], ws[m[idx[-1]]]["end"]] if idx else [None, None])
    for c, r in enumerate(rows):
        if r[0] is None:
            prev = next((rows[j][1] for j in range(c - 1, -1, -1) if rows[j][1] is not None), 0.0)
            nxt = next((rows[j][0] for j in range(c + 1, len(rows)) if rows[j][0] is not None), prev + 2.0)
            r[0], r[1] = prev, max(prev + 1.0, nxt)
    for c in range(len(rows)):
        if c and rows[c][0] < rows[c - 1][1]:
            rows[c][0] = rows[c - 1][1]
        rows[c][1] = max(rows[c][1], rows[c][0] + 1.0)
        if c + 1 < len(rows) and rows[c + 1][0] is not None:
            rows[c][1] = min(rows[c][1] + 0.4, max(rows[c + 1][0], rows[c][0] + 1.0))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{two_lines(t)}\n"
                             for i, (t, (a, b)) in enumerate(zip(caps, rows), 1)) + "\n")
    print(f"{OUT.name}: {len(caps)} cues, last ends {rows[-1][1]:.1f} s; matched {len(m)}/{len(sn)} script words")


if __name__ == "__main__":
    main()
