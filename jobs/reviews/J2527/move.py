"""J2527 step 2: move Orbit With Ben's own rules from AGENTS.md to studio/RULES.md. Every line goes whole to one file.

A record of how the move was made, kept so it can be read and re-run. It reads AGENTS.md at the commit named in
BEFORE, WRITES AGENTS.md and studio/RULES.md in the working tree, and prints the check: no old line lost or changed,
and every new line listed. Do not run it on main to "refresh" the rules: both files have their own life after the move."""
import subprocess, sys
from collections import Counter
from pathlib import Path

BEFORE = "e1f9c99238b9e945a9b55f29cccb5214b0eb196c"   # main when the move was made; the record stays runnable after the merge
old = subprocess.run(["git", "show", f"{BEFORE}:AGENTS.md"], capture_output=True, text=True, check=True).stdout.split("\n")
if old and old[-1] == "":
    old.pop()
L = lambda n: old[n - 1]                       # 1-indexed, as in docs/RULES_SPLIT.md
def rng(a, b): return list(range(a, b + 1))

# --- anchors: fail loudly if main has moved under us
EXPECT = {1: "# AGENTS.md", 3: "Read this first", 7: "**The channel:**", 9: "**The job:**", 11: "## Docs in force", 24: "## Where things live",
          45: "## Commands", 79: "## Standing lessons", 85: "3. **Production:**", 86: "4. **Thread", 97: "6. **YouTube state changes",
          111: "     - **All subscription credit floors", 112: "     - **ElevenLabs has no floor", 116: "## Teach on screen", 333: "## Packaging panel",
          580: "**Budget:**", 651: "## Never", 659: "  - Premiere a long.", 663: "  - Put Orbit at frame 0", 664: "- **Subscribe asks:**",
          665: "- **Titles:**", 668: "  - Use Kling", 670: "  - Omni the whole film", 672: "  - Use any voice other than", 681: "- **Social:**",
          685: "- **Secrets:**", 687: "## Missing footage fallback", 702: "## Changing the rules"}
for n, start in EXPECT.items():
    assert L(n).startswith(start), f"line {n} is not what the plan expects: {L(n)[:60]!r}"
assert len(old) == 704, len(old)

CHANNEL_ROWS = rng(28, 34) + [37, 42]
LESSONS = [83, 84] + rng(87, 96) + rng(98, 110) + [113, 114]
SECTIONS = rng(116, 332)                         # Teach on screen ... Topic pick, with their blank lines
NEVER = [659, 663, 664, 665, 668, 670, 672] + rng(681, 684)
DOCS = rng(11, 22)
channel = set([7, 8, 9] + DOCS + [23] + CHANNEL_ROWS + [81, 82] + LESSONS + SECTIONS + NEVER)
relocated = {111, 112}                           # two budget rules filed under "Music": to Budget, de-indented

NEW = {
 "pointer": "**Then read `studio/RULES.md`.** It holds this channel's own rules: what its films teach, look and sound like, how they are titled and packaged, and the lines it adds to the Never list. This file holds the studio's rules, which are the same for every channel. Both are in force. A channel can add a rule and can never remove a studio rule (Ben, 10 Nov 2026: *\"this system will read the individual channel's rules and guidance\"*; `docs/RULES_SPLIT.md` shows what went where).",
 "docs_h": "## Docs in force",
 "docs": "This file first. Then the channel's rules file, `studio/RULES.md`, and the docs it lists in its own order of precedence. Where a channel's doc and this file disagree, this file wins. Anything listed in neither, and everything in `_archive/`, is history only. Don't follow it.",
 "where": "This channel's own folders (`00_Brand/`, `01_Orbit-Character/`, `02_Video-Projects/`, `04_Audio/tools/`) are listed in `studio/RULES.md`.",
 "lessons": "These are the studio's. Lessons 1, 2, 5 and 7 (neighbour, edit, the Shorts feed, picture and music QA) are this channel's own and keep their numbers in `studio/RULES.md`.",
 "never": "A channel adds its own lines to this list in its `studio/RULES.md` (\"Never (this channel's additions)\"). Those add to this list and remove nothing from it.",
 "changing": "The docs numbered 1–8 are listed in `studio/RULES.md`. A channel's own rules are changed the same way, in that file.",
}

# --- the studio file
out = []
for n in range(1, len(old) + 1):
    if n in channel or n in relocated:
        if n == 11:                               # where "Docs in force" stood
            out += [NEW["docs_h"], "", NEW["docs"], ""]
        continue
    out.append(L(n))
    if n == 3:
        out += ["", NEW["pointer"]]
    if n == 43:                                   # last row of the table
        out += ["", NEW["where"]]
    if n == 80:                                   # blank line after the Standing lessons heading
        out += [NEW["lessons"], ""]
    if n == 580:                                  # the Budget paragraph
        out += [""] + [L(m).lstrip() for m in sorted(relocated)]
    if n == 685:
        out += ["", NEW["never"]]
    if n == 704:
        out += ["", NEW["changing"]]
studio = "\n".join(out) + "\n"
while "\n\n\n" in studio:
    studio = studio.replace("\n\n\n", "\n\n")

# --- the channel file
RH = {
 "title": "# Orbit With Ben: this channel's rules",
 "intro": "Read `AGENTS.md` first. It holds the studio's rules, which are the same for every channel. This file adds Orbit With Ben's own: what its films teach, look and sound like, and how they are titled and packaged. Where the two disagree, `AGENTS.md` wins. Nothing here removes a studio rule (Ben, 10 Nov 2026: *\"this system will read the individual channel's rules and guidance\"*).",
 "where_h": "## Where things live (this channel's folders)",
 "lessons_h": "## Standing lessons (this channel's)",
 "lessons_note": "Lessons 3, 4 and 6 are the studio's and stay in `AGENTS.md`.",
 "never_h": "## Never (this channel's additions)",
 "never_note": "These add to the Never list in `AGENTS.md`. They remove nothing from it.",
}
ch = [RH["title"], "", RH["intro"], "", L(7), "", L(9), ""]
ch += [L(n) for n in DOCS] + [""]
ch += [RH["where_h"], "", L(26), L(27)] + [L(n) for n in CHANNEL_ROWS] + [""]
ch += [RH["lessons_h"], "", L(81), "", RH["lessons_note"], ""] + [L(n) for n in LESSONS] + [""]
ch += [L(n) for n in SECTIONS]
ch += [RH["never_h"], "", RH["never_note"], "", L(658), L(659), L(663), L(664), L(665), L(667), L(668), L(670), L(672)] + [L(n) for n in rng(681, 684)]
rules = "\n".join(ch) + "\n"
while "\n\n\n" in rules:
    rules = rules.replace("\n\n\n", "\n\n")

Path("AGENTS.md").write_text(studio)
Path("studio/RULES.md").write_text(rules)

# --- the check: nothing lost, nothing changed, every added line declared
strip = lambda text: Counter(l.strip() for l in text.split("\n") if l.strip())
before, after = strip("\n".join(old)), strip(studio) + strip(rules)
lost = before - after
added = after - before
declared = Counter(list(NEW.values()) + list(RH.values()) + [L(26), L(27), L(658), L(667)])   # new lines, and headers both files need
undeclared = added - declared
print(f"old AGENTS.md: {len(old)} lines ({sum(before.values())} with text)")
print(f"new AGENTS.md: {len(studio.splitlines())} lines; studio/RULES.md: {len(rules.splitlines())} lines")
print(f"lines moved to the channel file: {len(channel - {8, 23, 82}) - sum(1 for n in channel if not L(n).strip())} with text")
print("lost or changed:", sum(lost.values())); [print("   LOST:", k[:110]) for k in lost]
print("added and declared:", sum((added & declared).values()))
print("added and NOT declared:", sum(undeclared.values())); [print("   EXTRA:", k[:110]) for k in undeclared]
sys.exit(1 if lost or undeclared else 0)
