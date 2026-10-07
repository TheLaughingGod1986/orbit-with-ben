#!/usr/bin/env python3
"""Pre-delivery clip check: VO sentence ends vs row/card cut points (Orbit playbook lessons, 1 Oct 2026).

Usage:
  python3 00_Brand/Channel-Setup/tools/clip_check.py <shot_list.csv> [--words vo_words.json] [--vo-end SEC]
  python3 …/clip_check.py <shot_list.csv> --words vo_words.json --json
  add --repeat-ok 6 for a repeat the script makes on purpose (it must be in the script, not a stumble)

Checks (docs/ORBIT_PLAYBOOK_LESSONS.md §2):
  - No vo_text ends mid-sentence at a picture→CARD or picture→picture boundary (unless next row continues).
  - CARD rows: previous spoken row must end a sentence; with --words, breath before card is 0.5–0.8 s.
  - With --words: last spoken word ends before the end-hold; end hold covers ≥2 s after last word.
  - Repeated / stumbled consecutive phrases in vo_text (same 4+ word run twice in a row).

Exit 0 only when every check passes. Assemblers should call this before delivery to Ben.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

BREATH_MIN, BREATH_MAX = 0.5, 0.8
END_AFTER_VO_MIN = 2.0  # picture/music past last word before fade (2–3 s band; fail under 2)
SENTENCE_END = re.compile(r'[.!?…]["\']?\s*$')
WORD_RE = re.compile(r"[a-z0-9']+")


def norm_tokens(text: str) -> list[str]:
    text = (text or "").lower().replace("’", "'").replace("—", " ").replace("-", " ")
    out = []
    for t in WORD_RE.findall(text):
        t = t.strip("'")
        t = {"disk": "disc", "metres": "meters", "kilometres": "kilometers", "colour": "color",
             "jewelry": "jewellery", "grey": "gray"}.get(t, t)
        if t:
            out.append(t)
    return out


def load_words(path: str) -> list[tuple[str, float, float]]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    raw = []
    if isinstance(d, dict):
        for seg in d.get("segments", []):
            raw += seg.get("words", [])
        if not raw:  # flat files, e.g. 022's words.json: {"file", "text", "words": [{word, start, end}, ...]}
            raw = d.get("words", [])
    else:
        raw = d
    out = []
    for w in raw:
        for t in norm_tokens(str(w.get("word", w.get("text", "")))):
            out.append((t, float(w["start"]), float(w["end"])))
    if not out:
        sys.exit(f"No words with timestamps in {path}")
    return out


def sentence_finished(text: str) -> bool:
    t = (text or "").strip()
    if not t or t.startswith("["):
        return True  # stage direction / silence row
    return bool(SENTENCE_END.search(t))


def phrase_ngrams(tokens: list[str], n: int = 4) -> set[tuple[str, ...]]:
    if len(tokens) < n:
        return set()
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def match_row_word_end(words: list[tuple[str, float, float]], vo_text: str, cursor: int) -> tuple[float | None, int]:
    """Advance through transcript; return (last_word_end, new_cursor) for this row's tokens."""
    want = norm_tokens(vo_text)
    if not want:
        return None, cursor
    i = cursor
    last_end = None
    for tok in want:
        found = None
        for j in range(i, min(i + 40, len(words))):
            if words[j][0] == tok or (
                len(tok) > 3 and (words[j][0].startswith(tok) or tok.startswith(words[j][0]))
            ):
                found = j
                break
        if found is None:
            return None, cursor  # caller treats as soft miss
        last_end = words[found][2]
        i = found + 1
    return last_end, i


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("shot_list")
    ap.add_argument("--words", help="Whisper / word-timestamp JSON for the locked VO")
    ap.add_argument("--vo-end", type=float, default=None, help="Locked VO duration (s); warn if list ends early")
    ap.add_argument("--json", action="store_true", help="Print machine-readable result")
    ap.add_argument("--repeat-ok", default="", help="comma list of rows whose repeat of the previous row is written "
                    "in the script on purpose (e.g. 022 row 6: 'It is not the spots. It is not the warming.')")
    a = ap.parse_args()
    repeat_ok = {x.strip() for x in a.repeat_ok.split(",") if x.strip()}

    rows = list(csv.DictReader(open(a.shot_list, newline="", encoding="utf-8")))
    if not rows:
        sys.exit("Empty shot list")

    errs: list[str] = []
    warns: list[str] = []
    words = load_words(a.words) if a.words else None
    wcursor = 0
    last_spoken_word_end: float | None = None
    prev_tokens: list[str] = []

    for k, r in enumerate(rows):
        src = (r.get("source") or "").strip().upper()
        text = (r.get("vo_text") or "").strip()
        try:
            vo_in, vo_out = float(r["vo_in"]), float(r["vo_out"])
        except (KeyError, ValueError):
            errs.append(f"row {r.get('row', k)}: vo_in/vo_out missing or not a number")
            continue

        # repeated / stumbled phrase vs previous spoken row
        toks = norm_tokens(text)
        if toks and prev_tokens and str(r.get("row", k)) not in repeat_ok:
            overlap = phrase_ngrams(toks) & phrase_ngrams(prev_tokens)
            if overlap:
                sample = " ".join(next(iter(overlap)))
                errs.append(
                    f"row {r.get('row', k)}: repeated/stumbled phrase vs previous row ("
                    f"…{sample}…). Re-check VO before delivery."
                )
        if toks and not text.startswith("["):
            prev_tokens = toks

        if words is not None and toks and not text.startswith("["):
            end, wcursor = match_row_word_end(words, text, wcursor)
            if end is not None:
                last_spoken_word_end = end
                # picture row should not cut before its last word finishes
                if src != "CARD" and vo_out + 0.05 < end:
                    errs.append(
                        f"row {r.get('row', k)}: cut at {vo_out:.2f}s clips VO word ending {end:.2f}s"
                    )

        if src == "CARD":
            # find previous spoken picture row
            prev = None
            for j in range(k - 1, -1, -1):
                if (rows[j].get("source") or "").strip().upper() != "CARD":
                    prev = rows[j]
                    break
            if prev is None:
                errs.append(f"row {r.get('row', k)}: CARD with no previous picture row")
                continue
            prev_text = (prev.get("vo_text") or "").strip()
            if prev_text and not prev_text.startswith("[") and not sentence_finished(prev_text):
                errs.append(
                    f"row {r.get('row', k)}: CARD before VO sentence finishes "
                    f"(previous row ends: {prev_text[-48:]!r})"
                )
            if words is not None and last_spoken_word_end is not None:
                breath = vo_in - last_spoken_word_end
                if breath < BREATH_MIN - 0.05:
                    errs.append(
                        f"row {r.get('row', k)}: breath before card {breath:.2f}s < {BREATH_MIN}s "
                        f"(need {BREATH_MIN}–{BREATH_MAX}s after last word)"
                    )
                elif breath > BREATH_MAX + 0.15:
                    warns.append(
                        f"row {r.get('row', k)}: breath before card {breath:.2f}s > {BREATH_MAX}s "
                        f"(target {BREATH_MIN}–{BREATH_MAX}s)"
                    )

        # mid-list picture rows that end mid-sentence while next row is CARD already handled;
        # also flag picture→picture where this row ends mid-sentence and next starts a new sentence
        # without continuing (heuristic: this row lacks sentence end and next does not lowercase-continue)
        if src not in ("CARD",) and k + 1 < len(rows):
            nxt = rows[k + 1]
            nxt_src = (nxt.get("source") or "").strip().upper()
            nxt_text = (nxt.get("vo_text") or "").strip()
            if (
                text
                and not text.startswith("[")
                and not sentence_finished(text)
                and nxt_src == "CARD"
            ):
                errs.append(
                    f"row {r.get('row', k)}: line clipped by CARD boundary "
                    f"(ends mid-sentence: {text[-48:]!r})"
                )
            elif (
                text
                and not text.startswith("[")
                and not sentence_finished(text)
                and nxt_text
                and nxt_text[0].isupper()
                and not nxt_text.startswith("[")
            ):
                # likely a hard cut mid-thought into a new sentence
                warns.append(
                    f"row {r.get('row', k)}: may clip mid-sentence before next row "
                    f"({text[-40:]!r} → {nxt_text[:40]!r})"
                )

    # end hold: picture/music past last VO word
    if words is not None and last_spoken_word_end is not None:
        try:
            list_end = float(rows[-1]["vo_out"])
        except (KeyError, ValueError):
            list_end = 0.0
        after = list_end - last_spoken_word_end
        if after < END_AFTER_VO_MIN - 0.05:
            errs.append(
                f"end hold only {after:.2f}s after last VO word (need ≥{END_AFTER_VO_MIN}s, target 2–3 s then fade)"
            )

    if a.vo_end is not None:
        try:
            list_end = float(rows[-1]["vo_out"])
        except (KeyError, ValueError):
            list_end = 0.0
        # list may include end hold past VO; failing early end is the problem
        if list_end + 0.05 < a.vo_end:
            errs.append(f"shot list ends at {list_end:.2f}s but VO runs to {a.vo_end:.2f}s")

    result = {
        "file": a.shot_list,
        "rows": len(rows),
        "passed": not errs,
        "errors": errs,
        "warnings": warns,
    }
    if a.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"clip_check: {len(rows)} rows — {'PASS' if not errs else 'FAIL'}")
        for e in errs:
            print(" - FAIL:", e)
        for w in warns:
            print(" - WARN:", w)
        if not errs:
            print("OK: sentence/card boundaries and end-after-VO checks clear.")
    sys.exit(0 if not errs else 1)


if __name__ == "__main__":
    main()
