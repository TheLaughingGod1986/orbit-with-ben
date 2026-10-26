#!/usr/bin/env python3
"""Keep the rule copies in step with AGENTS.md, and catch rule lines that have gone stale.

  python3 scripts/sync_rules.py           # rewrite every SYNC block from AGENTS.md
  python3 scripts/sync_rules.py --check   # CI: exit 1 if a block is out of date or a stale line is found

AGENTS.md is the source (Chief owns it: Ben to Claude 5 Oct 2026, handed to Chief 9 Oct, confirmed 10 Oct). A copy elsewhere sits between markers:

  <!-- SYNC: AGENTS.md#Never -->
  ...generated, do not edit by hand...
  <!-- /SYNC -->

The text after "#" names the AGENTS.md "## " heading; the block holds that section's body verbatim.
STALE lists phrases from superseded orders. Add one whenever an order changes, so old wording can't creep back.
"""
import argparse, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "AGENTS.md"
TARGETS = [
    ".cursor/rules/orbit-studio.mdc",
    "00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md",
    ".cursor/rules/orbit-build-long.mdc",    # Audit rules (Orbit Auditor, 26 Oct 2026)
    ".cursor/rules/orbit-build-shorts.mdc",  # Audit rules (Orbit Auditor, 26 Oct 2026)
]
# Sections that must exist in AGENTS.md and be mirrored in every listed copy (Ben, 26 Oct 2026: audit findings are
# written into the rules where workers read them, not just reported).
REQUIRED = {
    "Audit rules (Orbit Auditor, 26 Oct 2026)": [
        ".cursor/rules/orbit-build-long.mdc",
        ".cursor/rules/orbit-build-shorts.mdc",
        "00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md",
    ],
}
SCAN = [
    "AGENTS.md",
    "docs/ORBIT_PLAYBOOK_LESSONS.md",
    "docs/PRODUCTION_THREAD.md",
    "00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md",
    ".cursor/rules/*.mdc",
    "02_Video-Projects/_template_NNN_Episode-Slug/10_Shorts/README.md",
    "02_Video-Projects/_template_NNN_Episode-Slug/11_Upload-Package/PRODUCTION_CHECKLIST_V2.md",
    "00_Brand/Channel-Setup/templates/PRODUCTION_CHECKLIST_V2.md",
]
# (pattern, why it is stale)
STALE = [
    (r"[Ss]tandalone fact Shorts (run )?18–24", "Shorts are 22 s or longer (Keeper score, 26 Oct 2026)"),
    (r"only Short → long link", "Shorts link the long by Related video and description link (Keeper score, 26 Oct 2026)"),
    (r"Stop (and wait )?for Ben's OK", "sign-offs go to Claude first (3 Oct 2026)"),
    (r"Stop for Ben at the sign-off points", "sign-offs go to Claude first (3 Oct 2026)"),
    (r"NEEDS BEN\*\* → Chief of Staff", "NEEDS BEN goes to Claude first (3 Oct 2026)"),
    (r"Home: Google AI Studio", "picture runs on Vertex (free credit), never AI Studio prepaid"),
    (r"\*\*Tools:\*\* Google AI Studio", "picture runs on Vertex (free credit), never AI Studio prepaid"),
    (r"Ben OKs anything public", "Claude gives the final OK (3 Oct 2026)"),
    (r"until Ben reviews", "Claude reviews KEEP (3 Oct 2026)"),
    (r"shot list (goes )?to \**Ben before generation", "shot lists go to Claude (3 Oct 2026)"),
    (r"back catalogue needs Ben's OK", "back catalogue goes to Claude (3 Oct 2026)"),
    (r"edit_post` with Ben's OK", "queued Buffer edits go to Claude (3 Oct 2026)"),
    (r"\*\*Claude owns `AGENTS\.md`", "Chief owns AGENTS.md and the Never list (Ben, 9-10 Oct 2026)"),
    (r"relay never counts as Ben's word", "a Chief relay of Ben's OK counts (Ben, 10 Oct 2026)"),
    (r"with the £5 floor|stop at £5 left|down to £5 \+", "Vertex trial runs to £0 (Ben, 10 Oct 2026 22:50)"),
    (r"Who does what \(7 Oct 2026\)", "routing table is 'Who does what (11 Oct 2026)' (Ben, 11 Oct 2026)"),
    (r"Claude\*\* \| Cloud sessions \| .*Can't reach the Mini", "Claude Code is on the Mini; routing by job kind (11 Oct 2026)"),
    (r"Standing order \(Ben, 2–3 Oct 2026\): ask Claude first", "ask Chief first; Chief holds Claude's old role (9 Oct 2026)"),
    (r"Otherwise code jobs when Ben starts it", "Codex is a routed worker (gpt-6-astra for charts), 11 Oct 2026"),
    (r"lower-right (subscribe )?cue|subscribe cue in the lower-right|clear of the subscribe cue",
     "never burn SUBSCRIBE into a video; end screens do that (Audit rules, Orbit Auditor 26 Oct 2026)"),
    (r"no end card(,| or) CTA", "Shorts end on a burned-in end card: exact long title + yellow long id (Audit rules, 26 Oct 2026)"),
    (r"Last 4 s loop to the opening\.$", "the last ~4 s also carry the burned-in end card (Audit rules, 26 Oct 2026)"),
]
BLOCK = re.compile(r"(<!-- SYNC: AGENTS\.md#(?P<head>[^>]+?) -->\n)(?P<body>.*?)(<!-- /SYNC -->)", re.S)


def section(text, heading):
    m = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        sys.exit(f"sync_rules: AGENTS.md has no '## {heading}' section")
    return m.group(1).strip("\n") + "\n"


def sync(text, source):
    return BLOCK.sub(lambda m: m.group(1) + section(source, m.group("head").strip()) + m.group(4), text)


def stale_hits():
    hits = []
    for pattern in SCAN:
        for path in sorted(ROOT.glob(pattern)):
            for n, line in enumerate(path.read_text().splitlines(), 1):
                for rx, why in STALE:
                    if re.search(rx, line, re.I):
                        hits.append(f"{path.relative_to(ROOT)}:{n}: stale ({why}): {line.strip()[:120]}")
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    source = SOURCE.read_text()
    problems = []
    for rel in TARGETS:
        path = ROOT / rel
        text = path.read_text()
        if not BLOCK.search(text):
            problems.append(f"{rel}: no SYNC block")
            continue
        new = sync(text, source)
        if new != text:
            if a.check:
                problems.append(f"{rel}: SYNC block out of date (run python3 scripts/sync_rules.py)")
            else:
                path.write_text(new)
                print(f"synced {rel}")
    for head, copies in REQUIRED.items():
        section(source, head)  # exits if AGENTS.md lost the section
        for rel in copies:
            if f"<!-- SYNC: AGENTS.md#{head} -->" not in (ROOT / rel).read_text():
                problems.append(f"{rel}: missing the SYNC block for AGENTS.md#{head}")
    problems += stale_hits()
    for p in problems:
        print(p)
    if problems:
        return 1
    print("rules OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
