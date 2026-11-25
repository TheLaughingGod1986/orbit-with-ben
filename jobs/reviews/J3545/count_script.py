"""Independently reproduce OWB 064 v04 spoken counts, opening timing, and chapter estimates."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
SCRIPT_REL = "02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/01_Script/every_planet_explained_script_master_v04.md"

if len(sys.argv) > 1 and sys.argv[1].startswith("--git-ref="):
    ref = sys.argv[1].split("=", 1)[1]
    raw = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{ref}:{SCRIPT_REL}"])
else:
    raw = (ROOT / SCRIPT_REL).read_bytes()

text = raw.decode("utf-8")
chapters = [("Mercury", [])]
for line in text.splitlines():
    s = line.strip()
    if s.startswith("[CHAPTER CARD:"):
        chapters.append((s.split(": ", 1)[1].split(" — ")[0], []))
    elif s and not s.startswith(("#", "[", "<!--")):
        chapters[-1][1].append(s)


def counts(s: str) -> dict:
    return {
        "spoken_words": sum(bool(re.search(r"[A-Za-z0-9]", w)) for w in s.split()),
        "whitespace_tokens": len(s.split()),
        "expanded_words": len(re.findall(r"[A-Za-z0-9']+", s)),
        "characters": len(s),
    }


spoken = " ".join(" ".join(lines) for _, lines in chapters)
p1 = chapters[0][1][0]
sents = re.split(r"(?<=[?.!])\s+", p1)
s1, s2, s3 = sents[0], sents[1], sents[2]
s1_exp = len(re.findall(r"[A-Za-z0-9']+", s1))
s2_exp = len(re.findall(r"[A-Za-z0-9']+", s2))
s3_exp = len(re.findall(r"[A-Za-z0-9']+", s3))

result = {
    "script_sha256": hashlib.sha256(raw).hexdigest(),
    "bytes": len(raw),
    **counts(spoken),
    "first_sentence": s1,
    "first_sentence_expanded_words": s1_exp,
    "first_sentence_est_s_at_145wpm": round(s1_exp * 60 / 145, 2),
    "first_sentence_est_s_at_130wpm": round(s1_exp * 60 / 130, 2),
    "answer_sentence": s2,
    "answer_end_est_s_at_145wpm": round((s1_exp + s2_exp) * 60 / 145, 2),
    "payoff_sentence3_end_est_s_at_145wpm": round((s1_exp + s2_exp + s3_exp) * 60 / 145, 2),
    "markers": {
        "DATA": text.count("DATA:"),
        "SCALE": text.count("SCALE:"),
        "WHO": text.count("WHO:"),
        "WHEN": text.count("WHEN:"),
        "FACT": text.count("FACT:"),
        "NUMBER_OBJECT": text.count("NUMBER OBJECT"),
        "CHAPTER_CARD": text.count("[CHAPTER CARD:"),
        "SUBSCRIBE_BEAT": text.count("[SUBSCRIBE BEAT]"),
        "ORBIT_ACTS": text.count("[ORBIT ACTS:"),
        "VISUAL_MUST": text.count("[VISUAL MUST:"),
        "TEACH": text.count("[TEACH:"),
    },
    "timing_basis": "145 alphanumeric tokens/minute; 6.5 seconds transition/breath per chapter; 18 seconds final picture/music hold. Estimates only, no audio rendered.",
    "chapters": [],
}

t = 0.0
for name, lines in chapters:
    c = counts(" ".join(lines))
    duration = c["spoken_words"] * 60 / 145 + 6.5
    result["chapters"].append({
        "name": name,
        **c,
        "start_s": round(t, 2),
        "speech_s": round(c["spoken_words"] * 60 / 145, 2),
        "end_s": round(t + duration, 2),
    })
    t += duration

result["estimated_total_s"] = round(t + 18, 2)
print(json.dumps(result, indent=2))
