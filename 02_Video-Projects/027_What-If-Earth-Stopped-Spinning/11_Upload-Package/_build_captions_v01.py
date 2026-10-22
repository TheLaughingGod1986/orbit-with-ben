#!/usr/bin/env python3
"""en-GB captions for the Earth Spin 027 long, timed to the v01m picture.

v01m is the v01l picture with the music and SFX mix (J0793). Word times are unchanged.

The locked script's wording (01_Script/earth_spin_script_master_v01.md) is aligned
to the picture-order VO (02_Voiceover/words_v02order.json). words.json is the v01
take order; the picture speaks the v02 order (assembler nt()), and row 4, the
"In this film..." agenda, is cut. Whisper spellings never reach the captions.
Word times are the picture clock: "Right" at 0.16 s, "once." at 22.56 s,
"measured." at 44.18 s, last word "down." at 442.82 s, picture 446.3 s.
Built from the Nearest Star 026 builder (J0326). J0327, 15 Oct 2026.
"""
import difflib, json, re, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
SCRIPT = PROJ / "01_Script" / "earth_spin_script_master_v01.md"
WORDS = PROJ / "02_Voiceover" / "words_v02order.json"
OUT = HERE / "Captions" / "earth_spin_long_v01m_en-GB.srt"
MAX = 84  # two lines of 42
PICTURE_END = 446.3  # v01m container duration. Last cue must end within 1 s and not past it.

# Spoken year-words in words_v02order.json. 1851 is stored as the digits on both sides.
YEARS = {
    "1960s": ["nineteen", "sixties"],
    "1972": ["nineteen", "seventy", "two"],
    "2016": ["twenty", "sixteen"],
    "2035": ["twenty", "thirty", "five"],
}


def norm(w):
    w = unicodedata.normalize("NFKD", w)
    w = "".join(c for c in w if not unicodedata.combining(c))
    w = w.lower().replace("%", " percent").replace("-", " ")
    w = (w.replace("kilometers", "kilometres").replace("centimeters", "centimetres")
         .replace("meters", "metres").replace("modeled", "modelled")
         .replace("neighbor", "neighbour"))
    w = re.sub(r"[^a-z0-9 ]", "", w)
    out = []
    for t in w.split():
        if not t:
            continue
        out += YEARS.get(t, [t])
    return out


def prose():
    """Spoken lines in picture order: open, Sudden Stop, Speed, then the subscribe beat through the end.
    The agenda line is not in the v01l picture."""
    buckets = {"open": [], "speed": [], "sudden": [], "tail": []}
    cur = "open"
    for line in SCRIPT.read_text().splitlines():
        s = line.strip()
        if s.startswith("[CHAPTER CARD: The Speed"):
            cur = "speed"
            continue
        if s.startswith("[CHAPTER CARD: The Sudden"):
            cur = "sudden"
            continue
        if s.startswith("[SUBSCRIBE BEAT]"):
            cur = "tail"
            continue
        if not s or s.startswith(("#", "[", "<!--")) or s.startswith("In this film"):
            continue
        buckets[cur].append(s)
    return " ".join(buckets["open"] + buckets["sudden"] + buckets["speed"] + buckets["tail"])


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
    if rows and rows[-1][1] < PICTURE_END - 1.0:
        rows[-1][1] = round(PICTURE_END - 0.1, 3)
    if rows and rows[-1][1] > PICTURE_END:
        rows[-1][1] = PICTURE_END
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{two_lines(t)}\n"
                             for i, (t, (a, b)) in enumerate(zip(caps, rows), 1)) + "\n")
    missed = [sn[i] for i in range(len(sn)) if i not in m]
    print(f"{OUT.name}: {len(caps)} cues, last ends {rows[-1][1]:.1f} s; matched {len(m)}/{len(sn)} script words")
    if missed:
        print("unmatched:", " ".join(missed[:40]))


if __name__ == "__main__":
    main()
