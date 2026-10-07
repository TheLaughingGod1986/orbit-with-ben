#!/usr/bin/env python3
"""Studio job queue: any agent that is up can do any job it is able to, whoever was meant to (7 Oct 2026).

Jobs used to be addressed to an agent by name in prose on the studio thread ("Chief, please ..."). When that agent
was down (Grok Bot out of credit), its jobs sat. Here a job says what it NEEDS, not who does it, and whichever agent
is alive and able claims it. The thread stays for discussion and reports; this queue is the work list.

  needs   mini    the Mac mini: media, ffmpeg, picture, edit, YouTube/Studio, launchd (Grok Bot or Cursor)
          gemini  a facts-and-numbers check run through Gemini (Antigravity `agy`) on the Mini
          cloud   a Claude cloud session: reviews, scripts, shot lists, code, the tracker
          ben     only Ben: money, a sign-in, a decision
          any     whoever is free

  python3 scripts/jobs.py add --needs mini --title "Sun 022 first cut" --body-file brief.md --film 022 --stage edit \\
          --ref 6036709461 --by claude --git
  python3 scripts/jobs.py next --agent cursor --can mini,gemini,any --git      # claims the oldest job it can do
  python3 scripts/jobs.py done J0003 --agent cursor --result "cut v01 at OWB UAT/..." --ref 1a2b3c4 --git
  python3 scripts/jobs.py block J0003 --agent cursor --reason "needs Ben: Vertex credit" --git
  python3 scripts/jobs.py release J0003 --agent cursor --note "stopping point; rows 1-40 done" --git
  python3 scripts/jobs.py renew J0003 --agent cursor --eta 120 --git           # still working: push the ETA out
  python3 scripts/jobs.py list [--all]                                          # open and claimed jobs (JOBS.md too)

`next` exits 10 when nothing is waiting for that agent, so a loop can stop quietly.
Rules: a claim lasts until its ETA. A claim past its ETA counts as stalled, and the next able agent may take it over
(the takeover is noted). A job with --after waits until that job is done. A job with --film/--stage also claims that
stage on the studio board in the same commit (and releases it on done/release/block), so the board and the queue
always agree. Mutating commands take --git: pull, write, commit only the queue files (+ the film's status.json and
STATUS.md), push, and retry if another agent raced the push.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import studio  # noqa: E402

ROOT = studio.ROOT
QUEUE = ROOT / "jobs" / "queue.json"
JOBS_MD = ROOT / "JOBS.md"
NEEDS = ["mini", "gemini", "cloud", "ben", "any"]
EX_NONE = 10
DEFAULT_ETA = 120


def now():
    return studio.now()


def load(path: pathlib.Path = QUEUE) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {"next_id": 1, "jobs": []}


def save(data: dict, path: pathlib.Path = QUEUE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def find(data: dict, jid: str) -> dict | None:
    return next((j for j in data["jobs"] if j["id"] == jid.upper()), None)


def stalled(job: dict, at: dt.datetime) -> bool:
    return job["status"] == "claimed" and bool(job.get("eta")) and studio.parse(job["eta"]) < at


def log(job: dict, at: dt.datetime, agent: str, what: str) -> None:
    job.setdefault("history", []).append({"at": studio.iso(at), "by": agent, "what": what})


# ----------------------------------------------------------------------------- pure operations
def do_add(data: dict, *, title: str, needs: str, body: str, by: str, at: dt.datetime, ref: str = "", film: str = "",
           stage: str = "", after: str = "", repo: str = "owb", eta_min: int = DEFAULT_ETA) -> dict:
    if needs not in NEEDS:
        raise ValueError(f"needs must be one of {', '.join(NEEDS)}")
    if bool(film) != bool(stage):
        raise ValueError("--film and --stage go together")
    if stage and stage not in studio.STAGES:
        raise ValueError(f"stage must be one of {', '.join(studio.STAGES)}")
    if after and not find(data, after):
        raise ValueError(f"--after {after}: no such job")
    job = {"id": f"J{data['next_id']:04d}", "title": title, "needs": needs, "repo": repo, "body": body, "ref": ref,
           "film": film, "stage": stage, "after": after.upper() if after else "", "eta_min": eta_min,
           "status": "open", "by": "", "since": "", "eta": "", "created_by": by, "created_at": studio.iso(at),
           "result": "", "history": []}
    log(job, at, by, "added")
    data["next_id"] += 1
    data["jobs"].append(job)
    return job


def claimable(data: dict, job: dict, can: set[str], at: dt.datetime) -> bool:
    if job["needs"] not in can:
        return False
    if job["status"] == "open" or stalled(job, at):
        dep = find(data, job["after"]) if job.get("after") else None
        return dep is None or dep["status"] == "done"
    return False


def do_next(data: dict, agent: str, can: set[str], at: dt.datetime, eta_min: int | None = None) -> dict | None:
    """Claim the oldest job this agent can do (open, or stalled past its ETA). None when nothing is waiting."""
    for job in sorted(data["jobs"], key=lambda j: j["id"]):
        if job.get("by") == agent and job["status"] == "claimed":
            return job  # finish what you hold before taking more
    for job in sorted(data["jobs"], key=lambda j: j["id"]):
        if claimable(data, job, can, at):
            took = stalled(job, at)
            prev = job.get("by", "")
            job.update(status="claimed", by=agent, since=studio.iso(at),
                       eta=studio.iso(at + dt.timedelta(minutes=eta_min or job.get("eta_min") or DEFAULT_ETA)))
            log(job, at, agent, f"claimed (took over a stalled claim by {prev})" if took else "claimed")
            return job
    return None


def _mine(job: dict, agent: str) -> None:
    if job["status"] != "claimed" or job.get("by") != agent:
        raise ValueError(f"{job['id']} is {job['status']}" + (f" by {job['by']}" if job.get("by") else "") + f", not claimed by {agent}")


def do_done(job: dict, agent: str, result: str, at: dt.datetime, ref: str = "") -> None:
    _mine(job, agent)
    job.update(status="done", result=result, eta="")
    if ref:
        job["done_ref"] = ref
    log(job, at, agent, "done: " + result)


def do_block(job: dict, agent: str, reason: str, at: dt.datetime) -> None:
    _mine(job, agent)
    job.update(status="blocked", result=reason, eta="")
    log(job, at, agent, "blocked: " + reason)


def do_release(job: dict, agent: str, note: str, at: dt.datetime) -> None:
    _mine(job, agent)
    job.update(status="open", by="", since="", eta="")
    log(job, at, agent, "released" + (": " + note if note else ""))


def do_renew(job: dict, agent: str, eta_min: int, at: dt.datetime) -> None:
    _mine(job, agent)
    job["eta"] = studio.iso(at + dt.timedelta(minutes=eta_min))
    log(job, at, agent, f"renewed to {job['eta']}")


def do_reopen(job: dict, agent: str, note: str, at: dt.datetime) -> None:
    if job["status"] not in ("blocked", "done", "cancelled"):
        raise ValueError(f"{job['id']} is {job['status']}; only blocked, done or cancelled jobs reopen")
    job.update(status="open", by="", since="", eta="")
    log(job, at, agent, "reopened" + (": " + note if note else ""))


def do_cancel(job: dict, agent: str, note: str, at: dt.datetime) -> None:
    if job["status"] == "done":
        raise ValueError(f"{job['id']} is already done")
    job.update(status="cancelled", by="", eta="")
    log(job, at, agent, "cancelled" + (": " + note if note else ""))


# ----------------------------------------------------------------------------- board link (film/stage claims)
def board_claim(job: dict, agent: str, at: dt.datetime) -> str | None:
    if not job.get("film"):
        return None
    path = studio.film_dir(studio.FILMS, job["film"]) / "status.json"
    d = studio.load(path)
    mins = max(1, int((studio.parse(job["eta"]) - at).total_seconds() // 60))
    err = studio.do_claim(d, job["stage"], agent, mins, f"{job['id']} {job['title']}", at)
    if err:
        return err
    studio.save(path, d)
    return None


def board_release(job: dict, agent: str, state: str, ref: str = "") -> None:
    if not job.get("film"):
        return
    path = studio.film_dir(studio.FILMS, job["film"]) / "status.json"
    d = studio.load(path)
    if any(c["stage"] == job["stage"] and c["by"] == agent for c in d.get("claims", [])):
        studio.do_release(d, job["stage"], agent, state, ref)
        studio.save(path, d)


# ----------------------------------------------------------------------------- JOBS.md
def render(data: dict, at: dt.datetime) -> str:
    L = ["# Studio job queue", "", "Generated by `python3 scripts/jobs.py` from `jobs/queue.json`. Don't edit by hand.",
         "Any agent able to do a job may claim it: `jobs.py next --agent <you> --can <what you can do>`.", "",
         "| Job | Needs | Status | Who | ETA (UTC) | Title | Ref |", "|---|---|---|---|---|---|---|"]
    live = [j for j in data["jobs"] if j["status"] in ("open", "claimed", "blocked")]
    for j in sorted(live, key=lambda j: j["id"]):
        st = "**stalled**" if stalled(j, at) else j["status"] + (f" (after {j['after']})" if j.get("after") and j["status"] == "open" else "")
        film = f"{j['film']} {j['stage']} · " if j.get("film") else ""
        L.append(f"| {j['id']} | {j['needs']} | {st} | {j.get('by') or '–'} | {j.get('eta') or '–'} | {film}{j['title']} | {j.get('ref') or ''} |")
    if not live:
        L.append("| – | | nothing waiting | | | | |")
    done = [j for j in data["jobs"] if j["status"] in ("done", "cancelled")][-10:]
    if done:
        L += ["", "Recently finished:", ""] + [f"- {j['id']} {j['status']}: {j['title']} ({j.get('result') or ''})" for j in reversed(done)]
    return "\n".join(L) + "\n"


# ----------------------------------------------------------------------------- git transaction
def with_git(apply, message: str, tries: int = 3):
    """Pull, apply, commit only the queue files and any touched film board files, push; retry on a push race."""
    for _ in range(tries):
        if studio.git("pull", "-q", "--rebase", "--autostash", "origin", "main").returncode != 0:
            return None, "git pull failed; resolve the working tree first"
        data = load()
        before = json.dumps(data, sort_keys=True)
        out, err, touched = apply(data)
        if err:
            return None, err
        if json.dumps(data, sort_keys=True) == before and not touched:
            return out, None  # nothing changed (e.g. `next` with nothing waiting): no commit, no push
        save(data)
        JOBS_MD.write_text(render(data, now()))
        paths = [str(QUEUE), str(JOBS_MD)]
        if touched:
            studio.write_status(studio.FILMS)
            paths += [str(p) for p in touched] + [str(studio.status_path(studio.FILMS))]
        studio.git("add", *paths)
        if studio.git("commit", "-q", "-m", message, "--", *paths).returncode != 0:
            return None, "git commit failed"
        if studio.git("push", "-q", "origin", "HEAD:main").returncode == 0:
            return out, None
        studio.git("reset", "-q", "HEAD~1")
        studio.git("checkout", "-q", "--", *paths)
    return None, "push kept racing; try again"


def film_status_path(job: dict):
    return studio.film_dir(studio.FILMS, job["film"]) / "status.json" if job.get("film") else None


def show(job: dict) -> str:
    who = (f" by {job['by']}" if job.get("by") else "") + (f" until {job['eta']}" if job.get("eta") else "")
    lines = [f"{job['id']} [{job['needs']}] {job['status']}{who}",
             f"title: {job['title']}"]
    if job.get("film"):
        lines.append(f"board: {job['film']} {job['stage']}")
    if job.get("ref"):
        lines.append(f"ref: {job['ref']}")
    if job.get("body"):
        lines += ["", job["body"]]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--title", required=True)
    a.add_argument("--needs", required=True, choices=NEEDS)
    a.add_argument("--body", default="")
    a.add_argument("--body-file", type=pathlib.Path)
    a.add_argument("--ref", default="")
    a.add_argument("--film", default="")
    a.add_argument("--stage", default="")
    a.add_argument("--after", default="")
    a.add_argument("--repo", default="owb", choices=["owb", "hos"])
    a.add_argument("--eta", type=int, default=DEFAULT_ETA, help="minutes a claim lasts before it counts as stalled")
    a.add_argument("--by", required=True)
    n = sub.add_parser("next")
    n.add_argument("--agent", required=True)
    n.add_argument("--can", required=True, help="comma list from: " + ",".join(NEEDS))
    n.add_argument("--eta", type=int, default=None)
    n.add_argument("--peek", action="store_true", help="show what you would get, claim nothing")
    for name in ("done", "block", "release", "renew", "reopen", "cancel", "show"):
        p = sub.add_parser(name)
        p.add_argument("id")
        p.add_argument("--agent", default="")
        p.add_argument("--result", default="")
        p.add_argument("--reason", default="")
        p.add_argument("--note", default="")
        p.add_argument("--ref", default="")
        p.add_argument("--eta", type=int, default=DEFAULT_ETA)
    lst = sub.add_parser("list")
    lst.add_argument("--all", action="store_true")
    for p in sub.choices.values():
        p.add_argument("--git", action="store_true")
    args = ap.parse_args(argv)
    at = now()

    if args.cmd == "list":
        data = load()
        for j in data["jobs"]:
            if args.all or j["status"] in ("open", "claimed", "blocked"):
                print(f"{j['id']} [{j['needs']}] {'stalled' if stalled(j, at) else j['status']}"
                      f"{' by ' + j['by'] if j.get('by') else ''}  {j['title']}")
        return 0
    if args.cmd == "show":
        job = find(load(), args.id)
        if not job:
            sys.exit(f"jobs: no {args.id}")
        print(show(job))
        return 0

    def apply(data):
        touched = []
        try:
            if args.cmd == "add":
                body = args.body_file.read_text() if args.body_file else args.body
                job = do_add(data, title=args.title, needs=args.needs, body=body, by=args.by, at=at, ref=args.ref,
                             film=args.film, stage=args.stage, after=args.after, repo=args.repo, eta_min=args.eta)
                return job, None, touched
            if args.cmd == "next":
                can = {c.strip() for c in args.can.split(",") if c.strip()}
                if args.peek:
                    job = next((j for j in sorted(data["jobs"], key=lambda j: j["id"]) if claimable(data, j, can, at)), None)
                    return job, None, touched
                job = do_next(data, args.agent, can, at, args.eta)
                if job and job.get("film") and job["history"][-1]["what"].startswith("claimed"):
                    err = board_claim(job, args.agent, at)
                    if err:
                        do_release(job, args.agent, f"board stage held: {err}", at)
                        return None, f"{job['id']}: the board stage is held ({err}); left open", touched
                    touched.append(film_status_path(job))
                return job, None, touched
            job = find(data, args.id)
            if not job:
                return None, f"no {args.id}", touched
            if args.cmd == "done":
                do_done(job, args.agent, args.result or "done", at, args.ref)
                board_release(job, args.agent, "review", args.ref)
            elif args.cmd == "block":
                do_block(job, args.agent, args.reason or args.result, at)
                board_release(job, args.agent, "blocked")
            elif args.cmd == "release":
                do_release(job, args.agent, args.note, at)
                board_release(job, args.agent, "doing")
            elif args.cmd == "renew":
                do_renew(job, args.agent, args.eta, at)
                if job.get("film"):
                    board_claim(job, args.agent, at)
            elif args.cmd == "reopen":
                do_reopen(job, args.agent or "claude", args.note, at)
            elif args.cmd == "cancel":
                do_cancel(job, args.agent or "claude", args.note, at)
            if job.get("film"):
                touched.append(film_status_path(job))
            return job, None, touched
        except ValueError as e:
            return None, str(e), touched

    if args.git and not (args.cmd == "next" and args.peek):
        who = getattr(args, "agent", "") or getattr(args, "by", "")
        what = " ".join(x for x in ("jobs:", args.cmd, getattr(args, "id", "") or (args.title if args.cmd == "add" else ""), "by", who) if x)
        job, err = with_git(apply, what)
    else:
        data = load()
        job, err, touched = apply(data)
        if not err and not (args.cmd == "next" and args.peek):
            save(data)
            JOBS_MD.write_text(render(data, at))
            if touched:  # the film's status.json was written by board_claim / board_release
                studio.write_status(studio.FILMS)
    if err:
        print(f"jobs: {err}", file=sys.stderr)
        return 1
    if args.cmd == "next" and not job:
        print("jobs: nothing waiting for you")
        return EX_NONE
    print(show(job) if job else "ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
