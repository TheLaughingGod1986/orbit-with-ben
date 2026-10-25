#!/usr/bin/env python3
"""Read-only J0921 package evidence checks; not a Chief approval."""
import hashlib, json, re
from pathlib import Path
from PIL import Image

p = Path(__file__).resolve().parents[1]
m = json.loads((p / "PACKAGE_MANIFEST.json").read_text())
checks = {}
checks["title_length"] = 0 < len(m["title"]) <= 60
checks["audience_private"] = m["madeForKids"] is False and m["privacy"] == "private"
checks["disclosure"] = m["syntheticDisclosure"] is True
checks["unscheduled_review"] = m["status"] == "review" and not m.get("schedule")
d = (p / m["descriptionFile"]).read_text()
checks["description_length"] = len(d) < 5000
checks["description_order"] = d.index("Chapters") < d.index("Sources:") < d.index("Image credits:") < d.index("Pictures:")
checks["five_sources"] = d[d.index("Sources:") : d.index("Image credits:")].count("https://") == 5
checks["no_affiliates"] = "/go/" not in d
checks["tags"] = len((p / m["tagsFile"]).read_text().split(",")) == 8

thumbs = []
for t in m["thumbnailAbc"]:
    q = p / t
    im = Image.open(q)
    thumbs.append(im.size == (1280, 720) and q.stat().st_size < 2 * 1024 * 1024)
checks["three_thumbnails"] = len(thumbs) == 3 and all(thumbs)

s = (p / m["captionsFile"]).read_text()
cues = s.strip().split("\n\n")
prev = 0
capok = True
for cue in cues:
    lines = cue.splitlines()
    ts = lines[1].split(" --> ")
    def sec(t):
        h, mi, se = t.replace(",", ".").split(":")
        return 3600 * int(h) + 60 * int(mi) + float(se)
    a, b = map(sec, ts)
    capok &= a >= prev and b > a and b < 542.230 and len(lines[2:]) <= 2 and all(len(x) <= 42 for x in lines[2:])
    prev = b
checks["caption_timing_and_wrapping"] = bool(capok)

w = json.loads((p.parent / "07_Edit-Project/full_rough_v03b_pack/betelgeuse_words_list.json").read_text())
t = " ".join(x["text"] for x in w)
for pat, rep in [(r"\bcenter\b", "centre"), (r"\bmoon\b", "Moon"), (r"\bsun\b", "Sun")]:
    t = re.sub(pat, rep, t)
caption = " ".join(" ".join(c.splitlines()[2:]) for c in cues)
checks["caption_words_complete"] = t == caption

v = Path(m["video"])
h = hashlib.sha256()
with v.open("rb") as f:
    for b in iter(lambda: f.read(1024 * 1024), b""):
        h.update(b)
checks["master_hash"] = h.hexdigest() == m["masterSha256"]
checks["trailer_exists"] = (p / m["trailer"]).exists()

report = {
    "job": "J0921",
    "checks": checks,
    "caption_cues": len(cues),
    "master_sha256": h.hexdigest(),
    "all_checks_ok": all(checks.values()),
    "scope": "Mechanical checks only. Chief review, caption upload and Studio read-back remain required. OWB has no lint:package command.",
}
(p / "Review/VALIDATION.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["all_checks_ok"] else 1)
