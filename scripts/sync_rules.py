#!/usr/bin/env python3
"""Keep the rule copies in step with the two rule files, and catch rule lines that have gone stale.

  python3 scripts/sync_rules.py           # rewrite every SYNC block from its rule file
  python3 scripts/sync_rules.py --check   # CI: exit 1 if a block is out of date or a stale line is found

There are two sources since 11 Nov 2026 (J2527; Ben, 10 Nov: "this system will read the individual channel's rules
and guidance"). AGENTS.md holds the studio's rules, the same for every channel. studio/RULES.md holds this channel's
own. The Chief owns both (Ben to Claude 5 Oct 2026, handed to Chief 9 Oct, confirmed 10 Oct). A copy elsewhere sits
between markers that name the file and the section:

  <!-- SYNC: AGENTS.md#Never -->
  ...generated, do not edit by hand...
  <!-- /SYNC -->

  <!-- SYNC: studio/RULES.md#Teach on screen (Ben, 11 Oct 2026) -->
  ...
  <!-- /SYNC -->

The text after "#" names a "## " heading in that file; the block holds that section's body verbatim.
STALE lists phrases from superseded orders. Add one whenever an order changes, so old wording can't creep back.
"""
import argparse, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import channels  # noqa: E402

SOURCE = ROOT / "AGENTS.md"
# The channel whose own rules the copies quote: the one a record that names no channel belongs to. Its rules file is
# in its checkout, which is this repo while that channel is the studio's home, and a folder beside it once it is not
# (J2621). With that checkout not on this machine the path is this repo's, and the file is then simply missing.
CHANNEL_SOURCE = (channels.checkout(channels.default()) or ROOT) / channels.CHANNEL_RULES
SOURCES = {"AGENTS.md": SOURCE, "studio/RULES.md": CHANNEL_SOURCE}
TARGETS = [
    ".cursor/rules/orbit-studio.mdc",
    "00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md",
]
SCAN = [
    "AGENTS.md",
    "studio/RULES.md",
    "docs/ORBIT_PLAYBOOK_LESSONS.md",
    "docs/PRODUCTION_THREAD.md",
    "00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md",
    ".cursor/rules/*.mdc",
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
    (r"Three Shorts \(22–27 s\) on Mon, Wed and Fri", "4 Orbit Shorts a week Mon/Wed/Fri/Sat (Ben cadence lock, 7 Nov 2026)"),
    (r"\*\*Two [A-Z]{3} longs a week \(Ben, 4 Nov 2026\)\.\*\*", "Weekly publish cadence locked 7 Nov 2026 (every channel)"),
    (r"four columns: \*\*To do · In progress · Scheduled · Live\*\*",
     "Videos tab uses nine lanes Backlog→…→UAT→Passed→…→Post-live (Ben, 7 Nov 2026)"),
    (r"cut's card in \*\*Ready for OK\*\*",
     "Ben's watch lane is Videos → UAT (Ben, 7 Nov 2026)"),
    (r"Media on the Mini or the NAS reaches it only through the shared folder",
     "Working films live on studio-live; File Sharing shared is not the film library (7 Nov 2026)"),
    (r"The shared folder `~/_desk/shared` \(Mini\) = `/Volumes/shared` \(MacBook\) passes files between them",
     "File Sharing shared is empty / not the film library; use studio-live (7 Nov 2026)"),
    (r"## NAS archive \(5 Oct 2026\)",
     "Heading is Film folders on the NAS (studio-live + archive) (7 Nov 2026)"),
    (r"invent a Tailscale or SMB share|new Tailscale file share|/Volumes/shared` as the film",
     "Do not invent a third share; studio-live + mac-mini-archive only (7 Nov 2026)"),
]
BLOCK = re.compile(r"(<!-- SYNC: (?P<file>AGENTS\.md|studio/RULES\.md)#(?P<head>[^>]+?) -->\n)(?P<body>.*?)(<!-- /SYNC -->)", re.S)


def find_section(text, heading):
    m = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip("\n") + "\n" if m else None


def section(sources, name, heading):
    """The body of '## heading' in the rule file `name`. `sources` maps each rule file's name to its text."""
    body = find_section(sources[name], heading)
    if body is None:
        elsewhere = [other for other, text in sources.items() if other != name and find_section(text, heading) is not None]
        hint = f" (it is in {elsewhere[0]}: change the marker to name that file)" if elsewhere else ""
        sys.exit(f"sync_rules: {name} has no '## {heading}' section{hint}")
    return body


def sync(text, sources):
    if isinstance(sources, str):  # one text: the studio file alone, as callers passed before there were two
        sources = {"AGENTS.md": sources, "studio/RULES.md": ""}
    return BLOCK.sub(lambda m: m.group(1) + section(sources, m.group("file"), m.group("head").strip()) + m.group(5), text)


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
    source = {name: (path.read_text() if path.exists() else "") for name, path in SOURCES.items()}
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
    problems += stale_hits()
    for p in problems:
        print(p)
    if problems:
        return 1
    print("rules OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
