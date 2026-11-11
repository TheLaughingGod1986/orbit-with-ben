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
import argparse, datetime as dt, json, os, pathlib, subprocess, sys
import fcntl


def _channels():
    """scripts/channels.py, found whether `studio` is run as a script or imported from elsewhere."""
    here = str(pathlib.Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    import channels
    return channels


def _board_name() -> str:
    """The name, for the STATUS.md heading, of the channel whose films this board tracks."""
    channels = _channels()
    return channels.name(channels.board_channel())


def _films() -> pathlib.Path:
    """The film folders this board tracks: in the board channel's own checkout, not under the studio's root (J2619)."""
    channels = _channels()
    return channels.films_dir(channels.board_channel())


ROOT = pathlib.Path(__file__).resolve().parent.parent
FILMS = _films()
STAGES = ["topic", "script", "sources", "vo", "shots", "picture", "edit", "thumbs", "upload"]
STATES = ["todo", "doing", "review", "done", "skip", "blocked"]
MARK = {"todo": ".", "doing": ">", "review": "?", "done": "+", "skip": "-", "blocked": "!"}
EX_HELD = 75


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%MZ")


def parse(s):
    # All producers use ISO timestamps, including seconds, fractions and UTC offsets.
    value = dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    if value.tzinfo is None:
        value = value.replace(tzinfo=dt.timezone.utc)
    return value.astimezone(dt.timezone.utc)


def film_dir(films, key):
    # A job may name its film as "OWB:026" as well as "026" (8 Nov 2026: three such jobs stopped every MacBook claim).
    key = str(key).split(":")[-1]
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
    out = [f"# {_board_name()}: studio status", "",
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


# A picture run appends its spend rows to this tracked file as it works (the Flow runners' `export_ai_spend`, which
# is made to write the shared checkout's own ledger). Until 11 Nov 2026 those unsaved rows made every queue write on
# the Mini refuse ("requires a clean working tree") for as long as a batch ran: workers committed them by hand four
# times in ten minutes and one could not claim its job at all.
SPEND_LEDGER = "05_Analytics/ai_spend/ledger.jsonl"


def _replace(path, lines):
    """Write the ledger in one step. A run reads this file while it works: it must never see it missing or half
    written (it stops on a ledger whose last line is unfinished)."""
    tmp = path.with_name(path.name + f".{os.getpid()}.tmp")
    tmp.write_text("".join(line + "\n" for line in lines))
    os.replace(tmp, path)


def _row_key(line):
    try:
        row = json.loads(line)
    except ValueError:
        return line
    return ("id", row["id"]) if isinstance(row, dict) and row.get("id") else line


def settle_spend_rows():
    """Commit and push the rows a picture run added to the spend ledger and left unsaved. Returns an error, or None.

    Only called when that file is the one thing changed in the checkout. Rows are only ever added: a ledger that was
    edited or cut is refused. Nothing is written when main's ledger has not moved (the usual case). When it has, the
    file becomes main's rows followed by ours, written whole each time. A run may add a row while this works: it is
    kept if seen, and the run's own export puts back any row of its own that is missing, so none is lost.
    """
    path = ROOT / SPEND_LEDGER
    head = git("show", f"HEAD:{SPEND_LEDGER}")
    if head.returncode:
        return "metadata --git requires a clean working tree and index"
    text = path.read_text()
    if text and not text.endswith("\n"):
        return "the spend ledger's last line is unfinished (a run may be writing it); nothing changed, try again"
    was, now = head.stdout.splitlines(), text.splitlines()
    if now[:len(was)] != was:
        return "the spend ledger was edited, not only added to; settle it by hand before any queue write"
    ours = now[len(was):]
    for line in ours:
        try:
            if not isinstance(json.loads(line), dict):
                raise ValueError
        except ValueError:
            return "the spend ledger has an unreadable new row; settle it by hand before any queue write"
    if git("fetch", "-q", "origin", "refs/heads/main").returncode:
        return "metadata fetch failed; no changes applied"
    base = git("rev-parse", "FETCH_HEAD").stdout.strip()
    if git("merge-base", "--is-ancestor", "HEAD", base).returncode:
        return "main has unpublished/diverged commits; no changes applied"
    theirs = git("show", f"{base}:{SPEND_LEDGER}").stdout.splitlines()
    if theirs == was:  # main's ledger has not moved: the fast-forward does not touch the file
        if git("merge", "-q", "--ff-only", base).returncode:
            return "main fast-forward failed; no changes applied"
    else:
        if theirs[:len(was)] != was:
            return "main's spend ledger was edited, not only added to; settle it by hand before any queue write"
        seen = {_row_key(line) for line in theirs}
        ours = [line for line in ours if _row_key(line) not in seen]
        entry = git("ls-tree", base, "--", SPEND_LEDGER).stdout.split()      # mode, "blob", sha, path
        if len(entry) < 3:
            return "main has no spend ledger; settle it by hand before any queue write"
        # The file and the index are set to main's version, so the fast-forward has nothing to write to the file.
        # The index is set from main's own blob, not from the file: a run may add a row to the file at any moment.
        _replace(path, theirs)
        git("update-index", "--cacheinfo", f"{entry[0]},{entry[2]},{SPEND_LEDGER}")
        moved = not git("merge", "-q", "--ff-only", base).returncode
        known = seen | {_row_key(line) for line in ours}
        late = [line for line in path.read_text().splitlines() if _row_key(line) not in known]  # added meanwhile
        if not moved:
            _replace(path, now + [line for line in late if _row_key(line) not in {_row_key(x) for x in now}])
            git("reset", "-q", "--", SPEND_LEDGER)
            return "main fast-forward failed; no changes applied"
        _replace(path, theirs + ours + late)
    git("add", "--", SPEND_LEDGER)
    if not git("diff", "--cached", "--quiet", "--", SPEND_LEDGER).returncode:
        return None                                   # every row was already on main
    if git("commit", "-q", "-m", "ai_spend: rows a picture run wrote to the shared ledger (saved by the next queue write)",
           "--", SPEND_LEDGER).returncode:
        git("reset", "-q", "--", SPEND_LEDGER)
        return "spend ledger commit failed; rows kept in the file"
    commit = git("rev-parse", "HEAD").stdout.strip()
    parents = git("rev-list", "--parents", "-n", "1", commit).stdout.split()
    changed = git("diff-tree", "--no-commit-id", "--name-only", "-r", commit).stdout.splitlines()
    if parents != [commit, base] or changed != [SPEND_LEDGER] or git("push", "-q", "origin", f"{commit}:refs/heads/main").returncode:
        git("reset", "-q", "--soft", base)            # the rows stay in the file, unsaved, for the next write
        git("reset", "-q", "--", SPEND_LEDGER)
    return None


def git_transaction(write, message, tries=3):
    """Fail closed outside clean main; push only the verified metadata commit.

    No rebase, autostash or worker-branch switch. A push that loses a race drops
    only its own verified metadata commit (`reset --keep` to the base it was made
    on), fast-forwards to the new main and re-applies the change, up to `tries`
    times; the last loss leaves the commit for explicit reconciliation. Other
    unpublished commits are never replayed or dropped.
    """
    common = git("rev-parse", "--git-common-dir")
    if common.returncode:
        return None, "not a Git checkout"
    lock = pathlib.Path(common.stdout.strip())
    if not lock.is_absolute():
        lock = ROOT / lock
    with (lock / "studio-metadata.lock").open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        branch = git("symbolic-ref", "--quiet", "--short", "HEAD")
        if branch.returncode or branch.stdout.strip() != "main":
            return None, "metadata --git requires clean main; worker branch unchanged"
        # A second worktree forced onto main (`git worktree add --force <dir> main`, Codex J2210, 5 Nov 2026) moves
        # main under the shared checkout, whose stale index then reads as a staged reverse of every newer commit
        # (PR #520) and blocks every later metadata write. Refuse in both until the extra worktree is removed.
        branches = [l[7:] for l in git("worktree", "list", "--porcelain").stdout.splitlines() if l.startswith("branch ")]
        if branches.count("refs/heads/main") > 1:
            return None, ("metadata --git refused: main is checked out in more than one worktree; remove the extra one "
                          "(git worktree list) and use `git worktree add --detach <dir> origin/main` instead")
        state = git("status", "--porcelain")
        if not state.returncode and state.stdout.splitlines() == [f" M {SPEND_LEDGER}"]:
            problem = settle_spend_rows()             # a picture run's unsaved rows are saved, not a reason to stop
            if problem:
                return None, problem
            state = git("status", "--porcelain")      # a row added since then stays for the next write
            if not state.returncode and state.stdout.splitlines() == [f" M {SPEND_LEDGER}"]:
                state = subprocess.CompletedProcess(state.args, 0, "", "")
        if state.returncode or state.stdout.strip():
            return None, "metadata --git requires a clean working tree and index"
        for attempt in range(max(1, tries)):
            result, retry = _metadata_attempt(write, message)
            if not retry or attempt == max(1, tries) - 1:
                return result
            # Another machine pushed first (5 Nov 2026: the Mini and the MacBook both write the queue). Our own
            # verified commit, and nothing else, goes; the change is re-applied on the new main. Never replayed.
            if git("reset", "-q", "--keep", retry).returncode:
                return None, "metadata push rejected; local commit preserved; reconcile main before retry"
        return result


def _metadata_attempt(write, message):
    """((out, err), base to return to when the push lost a race, else None)."""
    if git("fetch", "-q", "origin", "refs/heads/main").returncode:
        return (None, "metadata fetch failed; no changes applied"), None
    base = git("rev-parse", "FETCH_HEAD").stdout.strip()
    head = git("rev-parse", "HEAD").stdout.strip()
    if git("merge-base", "--is-ancestor", head, base).returncode:
        return (None, "main has unpublished/diverged commits; no changes applied"), None
    if git("merge", "-q", "--ff-only", base).returncode:
        return (None, "main fast-forward failed; no changes applied"), None
    out, err, paths = write()
    if err or not paths:
        return (out, err), None
    paths = [str(pathlib.Path(p).resolve().relative_to(ROOT.resolve())) for p in paths]
    if git("add", "--", *paths).returncode:
        return (None, "metadata git add failed; changes preserved"), None
    if git("commit", "-q", "-m", message, "--", *paths).returncode:
        return (None, "metadata git commit failed; changes preserved"), None
    commit = git("rev-parse", "HEAD").stdout.strip()
    parents = git("rev-list", "--parents", "-n", "1", commit).stdout.split()
    changed = git("diff-tree", "--no-commit-id", "--name-only", "-r", commit)
    if parents != [commit, base] or changed.returncode or not set(changed.stdout.splitlines()) <= set(paths):
        return (None, "metadata commit verification failed; not pushed, changes preserved"), None
    if git("push", "-q", "origin", f"{commit}:refs/heads/main").returncode:
        return (None, "metadata push rejected; local commit preserved; reconcile main before retry"), base
    return (out, None), None


def with_git(path, change, message, films, tries=3):
    """Commit studio metadata only, from clean main. A lost push race re-applies on the new main."""
    def write():
        data = load(path)
        err = change(data)
        if err:
            return None, err, []
        save(path, data)
        write_status(films)
        return None, None, [path, status_path(films)]
    return git_transaction(write, message, tries)[1]


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
