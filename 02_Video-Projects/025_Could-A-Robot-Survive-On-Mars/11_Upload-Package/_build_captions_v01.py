#!/usr/bin/env python3
"""en-GB captions for the Mars Robot 025 long: the locked script's wording (01_Script/mars_robot_script_master_v01.md)
timed to the v03f film (07_Edit-Project/full_rough_v03f_pack/mars_robot_words_list.json) by aligning words. Whisper spellings
never reach the captions. Built from the Light Speed 024 builder, Cursor, 9 Oct 2026 (J0066)."""
import difflib, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
SCRIPT = PROJ / "01_Script" / "mars_robot_script_master_v01.md"
WORDS = PROJ / "07_Edit-Project" / "full_rough_v03f_pack" / "mars_robot_words_list.json"
OUT = HERE / "Captions" / "mars_robot_long_v03f_en-GB.srt"
MAX = 84  # two lines of 42


def norm(w):
    w = w.lower().replace("%", " percent")
    w = re.sub(r"[^a-z0-9 ]", "", w)
    nums = {"10": "ten", "90": "ninety", "99": "ninetynine", "9999": "ninetynine point ninetynine",
            "660": "six hundred and sixty"}
    return [x for t in w.split() if t for x in nums.get(t, t).split()]


def prose():
    out = []
    for line in SCRIPT.read_text().splitlines():
        s = line.strip()
        if s and not s.startswith(("#", "[", "<!--")):
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
    ws = json.loads(WORDS.read_text())
    ws = ws["words"] if isinstance(ws, dict) else ws
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
    # fill unmatched captions between their neighbours, then make times monotonic and non-overlapping
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
                             for i, (t, (a, b)) in enumerate(zip(caps, rows), 1)))
    print(f"{OUT.name}: {len(caps)} cues, last ends {rows[-1][1]:.1f} s; matched {len(m)}/{len(sn)} script words")


if __name__ == "__main__":
    main()
