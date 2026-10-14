#!/usr/bin/env python3
"""Packaging panel (Ben, 14 Oct 2026): "get other models to critique the titles and thumbnails and rest of packaging."

Before the Chief passes a title, thumbnail or upload package, three other models critique it independently: Codex,
Gemini (agy) and Cursor. This queues one critique job addressed to each (jobs.py --for), all reading the same brief, and
one Claude job that reads the three critiques and decides (keep, change, or test the best alternative as B). Critiques
go to 05_Analytics/tests/panels/<slug>/<agent>.md; the decision to .../DECISION.md.

  python3 scripts/packaging_panel.py --slug owb-024-lightspeed --what "024 Light Speed upload package" \\
      --files 02_Video-Projects/024_.../11_Upload-Package/PACKAGE_MANIFEST.json 00_Brand/.../thumb_A.jpg --git

A critic sees only the brief and the files, never another critic's notes, so the three opinions stay independent.
"""
import argparse, datetime as dt, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jobs  # noqa: E402

CRITICS = ("codex", "gemini", "cursor")
PANELS = "05_Analytics/tests/panels"

RUBRIC = """Score each 1–10 and give **one concrete rewrite** for anything under 8:
1. **Title:** curiosity gap, clarity, would someone type it (search), under about 60 characters, no clickbait we can't pay off.
2. **Thumbnail at phone size** (look at it at 168×94): one subject, a clear emotion or danger, 2–3 words at most, strong contrast,
   readable, and nothing important under the bottom-right duration badge.
3. **Title + thumbnail together:** do they add to each other, or repeat the same words?
4. **First 30 seconds / Short hook** (when a script or cut is given): does it answer or sharpen the promise at once?
5. **Description first line and chapters:** do they work for search without spoiling the payoff?
Then: **"Which would you click, and why?"** (one line) and **"The single change that would most raise CTR."**
Be blunt and specific; no praise padding. Don't change any files except your own critique."""


def brief(what: str, files: list, slug: str, agent: str) -> str:
    fl = "\n".join(f"- `{f}`" for f in files) or "- (see the film's 11_Upload-Package and 08_Thumbnail folders)"
    return (f"**Packaging panel: {what}** (Ben, 14 Oct 2026: other models critique titles, thumbnails and packaging before the Chief passes them).\n\n"
            f"You are one of three independent critics. Don't read the other critics' files in `{PANELS}/{slug}/`.\n\n"
            f"Look at:\n{fl}\n\n{RUBRIC}\n\n"
            f"Write your critique to `{PANELS}/{slug}/{agent}.md` (start it with the date and your name), commit only that file "
            f"to main from a clean worktree, and mark this job done with your one-line 'single change'. No spend, no YouTube changes.")


def decision(what: str, slug: str) -> str:
    return (f"**Packaging panel decision: {what}.** Read the three critiques in `{PANELS}/{slug}/` "
            f"({', '.join(c + '.md' for c in CRITICS)}). If one is missing after 24 h, decide with what's there.\n"
            "Weigh them; where two or more agree, act on it. Write `DECISION.md` in the same folder:\n"
            "- keep / change: each change with its exact new text;\n"
            "- for the thumbnail, either 'keep' or the best alternative to build as Test & Compare B (a `thumb` job for Codex, logged in THUMB_LEDGER.json).\n"
            "Post a 3-line summary on #99 and queue any build or Studio job it needs. The Chief's PASS stands on DECISION.md.")


def queue(data: dict, what: str, files: list, slug: str, by: str = "claude", at=None) -> list:
    at = at or jobs.now()
    out = []
    for agent in CRITICS:
        out.append(jobs.do_add(data, title=f"Packaging panel ({agent}): {what}", needs="mini", body=brief(what, files, slug, agent),
                               by=by, at=at, for_agent=agent, kind="review", eta_min=30))
    out.append(jobs.do_add(data, title=f"Packaging panel decision: {what}", needs="cloud", body=decision(what, slug), by=by,
                           at=at, kind="review", after=out[-1]["id"], eta_min=30))
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--slug", required=True, help="folder name under 05_Analytics/tests/panels, e.g. owb-024-lightspeed")
    p.add_argument("--what", required=True, help="what is being judged, e.g. '024 Light Speed upload package'")
    p.add_argument("--files", nargs="*", default=[])
    p.add_argument("--by", default="claude")
    p.add_argument("--git", action="store_true")
    o = p.parse_args(argv)
    if o.git:
        out, err = jobs.with_git(lambda d: (", ".join(j["id"] for j in queue(d, o.what, o.files, o.slug, o.by)), None, []),
                                 f"jobs: packaging panel {o.slug} by {o.by}")
        print(err or f"queued {out}")
        return 1 if err else 0
    d = jobs.load()
    print(", ".join(j["id"] for j in queue(d, o.what, o.files, o.slug, o.by)))
    jobs.save(d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
