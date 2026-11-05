#!/usr/bin/env python3
"""Rule H: finished-work decisions go to the review lane, not the Chief (Ben, 5 Nov 2026: "Yes ok" to "reviews go to
the review agents ... the Chief keeps only system code, money, publishing and the rulebook").

For every live job waiting on a Chief decision that isn't one of the Chief's own calls:
  - a blocked worker job "parked for Chief" gets a linked `kind: review` job; the parent's result points at it, so the
    relay stops queueing it for the Chief, and the board shows it waiting for that review;
  - a `kind: chief` review/verification job becomes `kind: review` in place.
Any agent that is up takes review jobs (Claude first, then Cursor-on-Claude, Gemini, Codex; on the Mini, the MacBook or
Claude's hourly run), so several run at once.

The Chief keeps (left alone here): code or system changes (scripts/, the relay, dispatch, the board site, rules),
money (spend, credits, prices), publishing (upload, visibility, schedule, Studio finish on a live video) and AGENTS.md.

  python3 scripts/review_lane.py            # what it would move
  python3 scripts/review_lane.py --apply --git
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jobs  # noqa: E402
import workflow_state as workflow  # noqa: E402

CHIEF_ONLY = re.compile(
    r"relay|dispatch|rollout|frontend|publisher|tab-reuse|runner|film-first|require --film|workflow handoff|"
    r"\bspend\b|£|credit|price|top-?up|"
    r"publish|upload|visibility|schedul|end screen|altered-content|studio finish|pinned comment|"
    r"AGENTS\.md|never list|rulebook|"
    r"Short gaps|monthly improvement report", re.I)
CODE_PR = re.compile(r"\bPR\s?#?\d+", re.I)

RUBRIC = """Rule H review (Ben, 5 Nov 2026). Decide in one go, as the review lane, not the Chief:
1. Read the original job ({parent}), its brief, result, history and evidence (repo files, PRs, review notes).
2. Check the deliverable against its brief and AGENTS.md: the film's script/VO locks, SOURCES.md for every number,
   Teach-on-screen/Polish/Packaging rules, thumbnail gate (HOOK/BAND/GRADE/PHONE), picture_qa / polish_gate /
   music_gate results where they apply. Do every check a tool can prove; the watched/heard step is Ben's final watch.
3. Write jobs/reviews/<this job id>/REVIEW.md: KEEP or FIX, with the evidence and, for FIX, an exact fix list.
4. Apply it with jobs.with_git (one commit): KEEP -> release {parent} (clear its hold, status open, history note
   'review <this id> KEEP: <next step>') or close it done if the deliverable is final; FIX -> reopen {parent} with the
   fix list. A records/data PR (only 02_Video-Projects/, jobs/, 05_Analytics data files) with green checks may be
   merged; never merge a PR touching scripts/, .github/, AGENTS.md or the board site, never spend, publish or change
   a schedule: those go back to the Chief as a short 'parked for Chief: <exact decision>' on {parent}.
5. Finish this job with the verdict in --result."""


def chief_only(j: dict) -> bool:
    text = " ".join(str(j.get(k) or "") for k in ("title", "result", "remaining_action"))
    if CHIEF_ONLY.search(text):
        return True
    # A PR without a film is system code; a film's PR (thumbnails, packages, pictures) is records.
    return bool(CODE_PR.search(text) and not j.get("film"))


def candidates(data: dict) -> list:
    """[(job, action)]: action 'link' (worker job parked for Chief) or 'rekind' (a kind: chief review job)."""
    out = []
    for j in data.get("jobs", []):
        if j.get("status") not in workflow.LIVE or chief_only(j) or j.get("for") == "chief":
            continue
        if j.get("kind") != "chief" and workflow.is_review(j):
            # Not when a live job already decides it (a review_of link, or a ruling job naming it in its title).
            if not any(x.get("status") in workflow.LIVE and x is not j and (x.get("review_of") == j["id"] or
                       re.search(r"\b" + re.escape(j["id"]) + r"\b", str(x.get("title") or ""))) for x in data["jobs"]):
                out.append((j, "link"))
        elif j.get("kind") == "chief" and j.get("status") in ("open", "blocked") and not j.get("handoff"):
            out.append((j, "rekind"))
    return out


def apply(data: dict, at: dt.datetime, agent: str = "claude") -> list:
    moved = []
    for j, action in candidates(data):
        if action == "link":
            r = jobs.do_add(data, title=f"Review {j['id']}: {j['title']}"[:140], needs=j.get("needs") or "any",
                            kind="review", by=agent, at=at, body=RUBRIC.format(parent=j["id"]) +
                            "\n\nWhat the worker asked the Chief: " + str(j.get("result") or "")[:1500],
                            film=(j.get("film") or "") if j.get("stage") else "",
                            stage=(j.get("stage") or "") if j.get("film") else "", repo=j.get("repo") or "owb")
            r["review_of"] = j["id"]
            if j.get("urgent"):
                r["urgent"] = j["urgent"]
            j["result"] = f"waiting for review {r['id']} (rule H): " + str(j.get("result") or "")[len("parked for Chief: "):][:300]
            jobs.log(j, at, agent, f"rule H: decision moved from the Chief to review {r['id']}")
            moved.append((j["id"], r["id"]))
        else:
            j["kind"] = "review"
            if str(j.get("title", "")).startswith("Chief: "):
                j["title"] = j["title"][len("Chief: "):]
            if j.get("status") == "blocked" and not j.get("hold"):
                j.update(status="open", by="", since="", eta="")
            j["body"] = RUBRIC.format(parent=j.get("recheck_of") or j["id"]) + "\n\n" + str(j.get("body") or "")
            jobs.log(j, at, agent, "rule H: Chief review moved to the review lane")
            moved.append((j["id"], j["id"]))
    return moved


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--git", action="store_true")
    ap.add_argument("--agent", default="claude")
    a = ap.parse_args(argv)
    if not a.apply:
        import json
        data = json.loads((Path(__file__).resolve().parents[1] / "jobs" / "queue.json").read_text())
        for j, action in candidates(data):
            print(action, j["id"], j.get("kind"), str(j.get("title"))[:80])
        return 0
    at = dt.datetime.now(dt.timezone.utc)
    box = {}

    def go(data):
        box["moved"] = apply(data, at, a.agent)
        return ("ok", "", [])
    if a.git:
        jobs.with_git(go, f"{a.agent}: rule H, move Chief reviews to the review lane")
    print(box.get("moved"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
