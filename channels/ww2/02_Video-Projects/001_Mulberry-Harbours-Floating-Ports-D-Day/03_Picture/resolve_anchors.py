"""Resolve four known ASR spelling/number variants without changing narration.

Produces edit timing evidence from existing Scribe words, not a listening verdict.
"""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

OVERRIDES = {
    "S01": "At dawn on the seventh of June",
    "S14": "Crucially Beckett left the center of each eighty foot span open",
    "S19": "A Mulberry harbor had five interlocking rings",
    "S24": "Across Britain forty five thousand workers from over three hundred firms",
}

def tokens(value):
    return re.findall(r"[a-z]+(?:'[a-z]+)?", value.lower().replace("’", "'"))

def resolve(anchors, transcript):
    words = []
    for word in transcript["words"]:
        if word.get("type") == "word":
            words.extend({"text": token, "start": word["start"], "end": word["end"]}
                         for token in tokens(word["text"]))
    result = copy.deepcopy(anchors)
    evidence = []
    for row in result["shots"]:
        phrase = OVERRIDES.get(row["shot"], row["matched_text"])
        target = tokens(phrase)
        # Verify locally, rather than choosing a repeated phrase elsewhere.
        matches = [i for i, word in enumerate(words)
                   if abs(word["start"] - row["start_s"]) <= 2
                   and [w["text"] for w in words[i:i+len(target)]] == target]
        if len(matches) != 1:
            raise ValueError(f'{row["shot"]}: expected one local exact phrase, got {len(matches)}')
        i = matches[0]
        evidence.append({"shot": row["shot"], "previous_start_s": row["start_s"],
                         "start_s": words[i]["start"], "anchor_text": phrase,
                         "override": row["shot"] in OVERRIDES,
                         "status": "EXACT_TRANSCRIPT_TIMING_MATCH"})
        row["start_s"] = words[i]["start"]
        row["anchor_evidence"] = evidence[-1]
        row["review"] = "TRANSCRIPT_TIMING_VERIFIED_NOT_LISTENED"
    for i, row in enumerate(result["shots"]):
        row["end_s"] = result["shots"][i+1]["start_s"] if i+1 < len(result["shots"]) else result["duration_s"]
        if row["end_s"] <= row["start_s"]:
            raise ValueError(f'Nonpositive shot {row["shot"]}')
        row["transcript_text"] = " ".join(w["text"] for w in transcript["words"]
            if w.get("type") == "word" and row["start_s"] <= w["start"] < row["end_s"])
    result["note"] = "All anchors verified against existing Scribe text/timestamps; not a claims, pronunciation, audio or motion verdict. No narration changed."
    return result, evidence

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anchors", type=Path, required=True)
    parser.add_argument("--scribe", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result, evidence = resolve(json.loads(args.anchors.read_text()), json.loads(args.scribe.read_text()))
    result["scribe_sha256"] = hashlib.sha256(args.scribe.read_bytes()).hexdigest()
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(f"{len(evidence)} exact local anchors; {sum(r['override'] for r in evidence)} spelling/number overrides")
