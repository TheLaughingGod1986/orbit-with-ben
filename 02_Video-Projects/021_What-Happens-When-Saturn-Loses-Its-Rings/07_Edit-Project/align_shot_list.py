#!/usr/bin/env python3
"""Re-time a shot list from the locked VO's real word timestamps, so every picture sits under its own words.

  python3 align_shot_list.py shot_list_v03h.csv vo_words.json -o shot_list_v03i.csv [--card 1.5] [--breath 0.65] [--hold 15]

vo_words.json: word timestamps of the LOCKED VO file (seconds into that file), either
  - whisper / faster-whisper JSON ({"segments":[{"words":[{"word","start","end"}]}]}), or
  - a plain list [{"word","start","end"}, ...].
  e.g. `whisper saturn_rings_vo_v03b_tightened_LOCK.wav --model medium --word_timestamps True --output_format json`

How times are set:
  - Each picture row's words are matched to the transcript in order (fuzzy, so disc/disk and STT slips are fine).
  - A row starts where its first word starts; it runs until the next row starts. The picture changes on the phrase.
  - A CARD row is placed after the previous row's last word + a music-only breath; the VO pauses for breath+card
    (the assembler inserts that silence). The picture before the card holds through the breath.
  - BREATH rows from v03h are dropped (the breath is folded into the row before the card).
  - The last row is the end hold: from the last word's end, for --hold seconds.
  - Clip rows (AI/OMNI/GODDARD) keep src_in and get src_out = src_in + new length; a clip that is too short is reported.
Then run check_shot_list.py on the output: rows it flags as too long need a second picture (split the row), too short
need merging. Nothing else in the list changes.
"""
import argparse, csv, difflib, json, re, sys

NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven",
       "8": "eight", "9": "nine", "10": "ten", "22": "twentytwo", "100": "hundred", "300": "three hundred"}


def norm_tokens(text):
    text = text.lower().replace("’", "'").replace("—", " ").replace("-", " ")
    out = []
    for t in re.findall(r"[a-z0-9']+", text):
        t = t.strip("'")
        t = {"disk": "disc", "metres": "meters", "kilometres": "kilometers", "colour": "color",
             "jewelry": "jewellery", "grey": "gray"}.get(t, t)
        out.extend(NUM.get(t, t).split())
    return [t for t in out if t]


def load_words(path):
    d = json.load(open(path, encoding="utf-8"))
    words = []
    if isinstance(d, dict):
        for seg in d.get("segments", []):
            words += seg.get("words", [])
    else:
        words = d
    out = []
    for w in words:
        for t in norm_tokens(str(w.get("word", w.get("text", "")))):
            out.append((t, float(w["start"]), float(w["end"])))
    if not out:
        sys.exit("No words with timestamps found in " + path)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("shot_list"); ap.add_argument("words"); ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--card", type=float, default=1.5); ap.add_argument("--breath", type=float, default=0.65)
    ap.add_argument("--hold", type=float, default=15.0)
    a = ap.parse_args()

    rows = [r for r in csv.DictReader(open(a.shot_list, newline="", encoding="utf-8"))
            if (r.get("source") or "").upper() != "BREATH"]
    fields = list(rows[0].keys())
    words = load_words(a.words)
    tw = [w[0] for w in words]

    # script tokens tagged with their row index (picture rows with words only; the end-hold row has none)
    st, owner = [], []
    for i, r in enumerate(rows):
        if (r.get("source") or "").upper() == "CARD" or r["vo_text"].strip().startswith("["):
            continue
        for t in norm_tokens(r["vo_text"]):
            st.append(t); owner.append(i)
    sm = difflib.SequenceMatcher(None, st, tw, autojunk=False)
    first, last, matched, total = {}, {}, {}, {}
    for i in owner:
        total[i] = total.get(i, 0) + 1
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            i, w = owner[blk.a + k], words[blk.b + k]
            first.setdefault(i, w[1]); last[i] = w[2]; matched[i] = matched.get(i, 0) + 1

    problems = []
    for i in total:
        if matched.get(i, 0) < max(1, 0.5 * total[i]):
            problems.append(f"row {rows[i]['row']}: only {matched.get(i, 0)}/{total[i]} words found in the transcript")
    if problems:
        print("Alignment too weak, check the transcript is of the LOCKED VO:\n - " + "\n - ".join(problems))
        sys.exit(1)

    # VO time -> timeline time: each card inserts breath + card of VO silence
    speech = [i for i in range(len(rows)) if i in first]
    out, shift, t_prev_end = [], 0.0, 0.0
    for idx, r in enumerate(rows):
        src = (r.get("source") or "").upper()
        r = dict(r)
        if src == "CARD":
            # card goes after the previous speech row's last word + breath
            prev = max([j for j in speech if j < idx], default=None)
            vo_end = last[prev] if prev is not None else 0.0
            # extend the previous picture row through the breath
            if out:
                out[-1]["vo_out"] = f"{vo_end + shift + a.breath:.2f}"
            cin = vo_end + shift + a.breath
            r["vo_in"], r["vo_out"] = f"{cin:.2f}", f"{cin + a.card:.2f}"
            # VO resumes after the card: timeline shift grows by (breath + card) minus any natural pause already there
            nxt = min([j for j in speech if j > idx], default=None)
            gap = (first[nxt] - vo_end) if nxt is not None else 0.0
            shift += max(0.0, a.breath + a.card - gap)
            out.append(r)
            continue
        if idx in first:
            start = (first[idx] + shift) if out else 0.0
            if out and (out[-1].get("source") or "").upper() != "CARD":
                out[-1]["vo_out"] = f"{start:.2f}"
            elif out and (out[-1].get("source") or "").upper() == "CARD":
                start = float(out[-1]["vo_out"])
            r["vo_in"], r["vo_out"] = f"{start:.2f}", f"{last[idx] + shift:.2f}"
            t_prev_end = last[idx] + shift
            out.append(r)
        else:  # end hold (no words)
            if out and (out[-1].get("source") or "").upper() != "CARD":
                out[-1]["vo_out"] = f"{t_prev_end:.2f}"
            r["vo_in"], r["vo_out"] = f"{t_prev_end:.2f}", f"{t_prev_end + a.hold:.2f}"
            out.append(r)

    notes = []
    for r in out:
        r["row"] = str(out.index(r) + 1)
        src = (r.get("source") or "").upper()
        if src in ("AI", "OMNI", "GODDARD") and r.get("src_in"):
            d = float(r["vo_out"]) - float(r["vo_in"])
            r["src_out"] = f"{float(r['src_in']) + d:.2f}"
            m = re.search(r"_(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)s\.\w+$", r["id"])
            if m and float(r["src_out"]) > float(m.group(2)) + 0.01:
                notes.append(f"row {r['row']}: {r['id']} needs {d:.2f}s but is approved only to {m.group(2)}s")
    w = csv.DictWriter(open(a.out, "w", newline="", encoding="utf-8"), fieldnames=fields)
    w.writeheader(); w.writerows(out)
    print(f"wrote {a.out}: {len(out)} rows, VO words matched {sum(matched.values())}/{len(st)}, "
          f"timeline ends {float(out[-1]['vo_out']):.2f}s")
    for n in notes:
        print(" -", n)
    print("Now run: python3 check_shot_list.py", a.out, f"--vo-end {float(out[-1]['vo_in']):.2f}")


if __name__ == "__main__":
    main()
