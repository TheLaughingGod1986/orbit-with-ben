#!/usr/bin/env python3
"""Studio board: where every film is, who is working on what, and which jobs have stalled.

Each film keeps one 02_Video-Projects/<film>/status.json. The board is read from those files, so no agent needs to
read the whole thread to learn the state of the work. The thread is for decisions; status.json is for state.

  python3 scripts/studio.py board                                   # one line per film, plus open claims
  python3 scripts/studio.py claim 027 sources --by chief/gemini --eta 60 --note "SOURCES draft"
  python3 scripts/studio.py release 027 sources --by chief/gemini --state review --ref 1a2b3c4
  python3 scripts/studio.py set 027 vo todo --next "Claude Locked: VO after Gemini check"
  python3 scripts/studio.py stale [--seen ~/_desk/state/stale_seen.txt]  # exit 1 and list claims past their ETA
                                                                    # (--seen: each stall reported once)
  python3 scripts/studio.py status                                  # rewrite STATUS.md (claim/release/set do it too)
  add --git to claim/release/set: pull, write, commit and push to main in one go (retries if the push races)

Claims are the one way to say "I'm on this", for Mini jobs and cloud sessions alike. A claim fails (exit 75) while
another live claim holds the same film and stage. A claim past its ETA counts as stalled: `stale` reports it, and a
new claim may take it over (the takeover is noted). Run `claim --git` before any spend; the push is the lock, so two
agents racing for the same stage can't both win.

Stages, in order: topic script sources vo shots picture edit thumbs upload.
States: todo, doing, review, done, skip, blocked.
"""
import argparse, datetime as dt, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILMS = ROOT / "02_Video-Projects"
STAGES = ["topic", "script", "sources", "vo", "shots", "picture", "edit", "thumbs", "upload"]
STATES = ["todo", "doing", "review", "done", "skip", "blocked"]
MARK = {"todo": ".", "doing": ">", "review": "?", "done": "+", "skip": "-", "blocked": "!"}
EX_HELD = 75


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%MZ")


def parse(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%MZ").replace(tzinfo=dt.timezone.utc)


def film_dir(films, key):
    hits = [d for d in sorted(films.iterdir()) if d.is_dir() and d.name.split("_")[0] == key]
    if len(hits) != 1:
        sys.exit(f"studio: no single film folder for '{key}' under {films}")
    return hits[0]


def load(path):
    if path.exists():
        return json.loads(path.read_text())
    return {"film": path.parent.name.split("_")[0], "title": "", "air": "", "stages": {}, "claims": [], "next": ""}


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def stalled(claim, at):
    return parse(claim["eta"]) < at


def do_claim(data, stage, by, eta_min, note, at):
    for c in data["claims"]:
        if c["stage"] == stage and c["by"] != by:
            if not stalled(c, at):
                return f"held by {c['by']} since {c['at']} (ETA {c['eta']})"
            note = f"{note} (took over stalled claim by {c['by']}, ETA {c['eta']})".strip()
    data["claims"] = [c for c in data["claims"] if c["stage"] != stage]
    data["claims"].append({"stage": stage, "by": by, "at": iso(at), "eta": iso(at + dt.timedelta(minutes=eta_min)),
                           "note": note})
    data["stages"].setdefault(stage, {})["state"] = "doing"
    return None


def do_release(data, stage, by, state, ref):
    mine = [c for c in data["claims"] if c["stage"] == stage and c["by"] == by]
    if not mine:
        return f"no claim on {stage} by {by}"
    data["claims"] = [c for c in data["claims"] if c not in mine]
    do_set(data, stage, state, ref, None)
    return None


def do_set(data, stage, state, ref, nxt):
    s = data["stages"].setdefault(stage, {})
    s["state"] = state
    if ref:
        s["ref"] = ref
    if nxt is not None:
        data["next"] = nxt


def board(films, at):
    rows = []
    head = f"{'film':<5} {'air':<10} " + " ".join(f"{s[:4]:<4}" for s in STAGES) + "  next"
    rows.append(head)
    claims = []
    for d in sorted(films.iterdir()):
        p = d / "status.json"
        if not p.exists():
            continue
        data = load(p)
        cells = " ".join(f"{MARK.get(data['stages'].get(s, {}).get('state', 'todo'), '.'):<4}" for s in STAGES)
        rows.append(f"{data['film']:<5} {data.get('air', ''):<10} {cells}  {data.get('next', '')}")
        for c in data["claims"]:
            flag = "STALLED" if stalled(c, at) else "live"
            claims.append(f"  {data['film']} {c['stage']:<8} {c['by']:<16} since {c['at']}  ETA {c['eta']}  {flag}  {c['note']}")
    rows.append("")
    rows.append("key: + done  ? review  > doing  . todo  - skip  ! blocked")
    rows.append("claims:" if claims else "claims: none")
    return "\n".join(rows + claims)


LABEL = {"todo": "", "doing": "doing", "review": "review", "done": "done", "skip": "skip", "blocked": "BLOCKED"}


def render_md(films):
    """STATUS.md: the board as a page Ben can read on GitHub. Built only from status.json (no clock), so CI can
    check it is current."""
    out = ["# Orbit With Ben: studio status", "",
           "Generated by `python3 scripts/studio.py status` from each film's `status.json`. Don't edit by hand.", "",
           "| Film | Airs | Done | Now | Next |", "|---|---|---|---|---|"]
    claims = []
    for p in sorted(films.glob("*/status.json")):
        d = load(p)
        st = d["stages"]
        done = sum(st.get(s, {}).get("state") in ("done", "skip") for s in STAGES)
        now_ = ", ".join(f"{s} ({LABEL[st[s]['state']]})" for s in STAGES
                         if st.get(s, {}).get("state") in ("doing", "review", "blocked")) or "-"
        title = f"{d['film']} {d.get('title', '')}".strip()
        out.append(f"| {title} | {d.get('air', '') or '-'} | {done}/{len(STAGES)} | {now_} | {d.get('next', '') or '-'} |")
        claims += [f"| {d['film']} | {c['stage']} | {c['by']} | {c['at']} | {c['eta']} | {c['note'] or '-'} |"
                   for c in d["claims"]]
    out += ["", "## Who is working on what", ""]
    if claims:
        out += ["A claim past its ETA counts as stalled; the Mini's watchdog posts it to the thread.", "",
                "| Film | Stage | By | Since (UTC) | ETA (UTC) | Note |", "|---|---|---|---|---|---|"] + claims
    else:
        out.append("No open claims.")
    out += ["", f"Stages: {', '.join(STAGES)}.", ""]
    return "\n".join(out)


def status_path(films):
    return films.parent / "STATUS.md"


def write_status(films):
    status_path(films).write_text(render_md(films))


def stale_list(films, at, seen=None):
    """Stalled claims as lines. With `seen` (a local file), report each stall once: lines already in the file are
    skipped and new ones are appended, so the 15-minute watchdog doesn't repeat itself."""
    out = []
    for p in sorted(films.glob("*/status.json")):
        data = load(p)
        out += [f"{data['film']} {c['stage']} by {c['by']}: ETA {c['eta']} passed ({c['note']})"
                for c in data["claims"] if stalled(c, at)]
    if seen is None:
        return out
    seen = pathlib.Path(seen)
    old = set(seen.read_text().splitlines()) if seen.exists() else set()
    new = [line for line in out if line not in old]
    if new:
        seen.parent.mkdir(parents=True, exist_ok=True)
        with seen.open("a") as f:
            f.write("".join(line + "\n" for line in new))
    return new


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)


def with_git(path, change, message, films, tries=3):
    """Pull, apply the change, commit only status.json and STATUS.md, and push. If the push races another agent,
    start again from the new main. Other uncommitted work in the tree is autostashed by the pull and never committed."""
    for _ in range(tries):
        if git("pull", "-q", "--rebase", "--autostash", "origin", "main").returncode != 0:
            return "git pull failed; resolve the working tree first"
        data = load(path)
        err = change(data)
        if err:
            return err
        save(path, data)
        write_status(films)
        paths = [str(path), str(status_path(films))]
        git("add", *paths)
        if git("commit", "-q", "-m", message, "--", *paths).returncode != 0:
            return "git commit failed"
        if git("push", "-q", "origin", "HEAD:main").returncode == 0:
            return None
        git("reset", "-q", "HEAD~1")  # drop only our status commit; other work in the tree is untouched
        git("checkout", "-q", "--", *paths)
    return "push kept racing; try again"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--films", default=str(FILMS), help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("board")
    sub.add_parser("stale").add_argument("--seen", help="local file of stalls already reported; report each once")
    sub.add_parser("status").add_argument("--check", action="store_true", help="CI: exit 1 if STATUS.md is out of date")
    for name in ("claim", "release", "set"):
        p = sub.add_parser(name)
        p.add_argument("film")
        p.add_argument("stage", choices=STAGES)
        p.add_argument("--git", action="store_true")
        if name == "claim":
            p.add_argument("--by", required=True)
            p.add_argument("--eta", type=int, default=60, help="minutes until the claim counts as stalled")
            p.add_argument("--note", default="")
        if name == "release":
            p.add_argument("--by", required=True)
            p.add_argument("--state", choices=STATES, default="review")
            p.add_argument("--ref")
        if name == "set":
            p.add_argument("state", choices=STATES)
            p.add_argument("--ref")
            p.add_argument("--next")
    a = ap.parse_args(argv)
    films = pathlib.Path(a.films)
    at = now()
    if a.cmd == "board":
        print(board(films, at))
        return 0
    if a.cmd == "status":
        current = status_path(films).read_text() if status_path(films).exists() else ""
        if a.check:
            if current != render_md(films):
                print("STATUS.md is out of date: run python3 scripts/studio.py status")
                return 1
            print("STATUS.md OK")
            return 0
        write_status(films)
        print(f"wrote {status_path(films)}")
        return 0
    if a.cmd == "stale":
        hits = stale_list(films, at, a.seen)
        print("\n".join(hits) if hits else "no stalled claims")
        return 1 if hits else 0
    path = film_dir(films, a.film) / "status.json"
    if a.cmd == "claim":
        change = lambda d: do_claim(d, a.stage, a.by, a.eta, a.note, at)
        msg = f"studio: {a.film} {a.stage} claimed by {a.by}"
    elif a.cmd == "release":
        change = lambda d: do_release(d, a.stage, a.by, a.state, a.ref)
        msg = f"studio: {a.film} {a.stage} {a.state} by {a.by}"
    else:
        change = lambda d: do_set(d, a.stage, a.state, a.ref, a.next)
        msg = f"studio: {a.film} {a.stage} {a.state}"
    if a.git:
        err = with_git(path, change, msg, films)
    else:
        data = load(path)
        err = change(data)
        if not err:
            save(path, data)
            write_status(films)
    if err:
        print(f"studio: {err}", file=sys.stderr)
        return EX_HELD if a.cmd == "claim" and err.startswith("held") else 1
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
