#!/usr/bin/env python3
"""A dry run of moving the studio into its own repo. It changes nothing outside a scratch folder.

    python3 scripts/studio_split.py                 build the layout in a temp folder, print what still stops the move
    python3 scripts/studio_split.py --json out.json the same as a file (one number: `left`)
    python3 scripts/studio_split.py --record FILE   also add today's result to a history file (one line a day)
    python3 scripts/studio_split.py --json jobs/reviews/studio_split/latest.json \\
            --record jobs/reviews/studio_split/history.jsonl --git      the daily run: record it on main and push
    python3 scripts/studio_split.py --streak FILE   how many days in a row the dry run has passed
    python3 scripts/studio_split.py --keep DIR      build the layout in DIR and leave it there to look at

Ben, 10 Nov 2026: "How can we get this project moving and finished?" The last step of docs/MULTI_CHANNEL_PLAN.md is
moving the studio (the engine, the job queue, the board) out of one channel's repo into its own, named `studio`,
private. That move is hard to undo, so it is rehearsed first, every day. The move happens after seven daily passes in
a row, and Ben is told the day before.

What a run does:
  1. Sorts every tracked file by ROUTES, the one table below: to the studio, or to the channel it belongs to.
  2. Builds that layout in a scratch folder: `studio/`, and one folder beside it for each channel.
  3. Checks what would break, and prints it in plain words under the headings in GROUPS.

It creates no repository, pushes nothing and moves nothing. It prints file names and counts, never the value of a key
or an address.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import channel_check  # noqa: E402
import channels  # noqa: E402

STUDIO, HOME_CHANNEL, BOTH, BUILT = "studio", "home channel", "both", "built by the studio"

# What goes where. First match wins. `{slug}` stands for any registered channel's slug, and the file then goes to
# that channel. Change the move here, and the plan (docs/MULTI_CHANNEL_PLAN.md) with it: the script and the plan must
# not drift apart.
ROUTES = (
    # The studio: the engine, the queue, the board, the rules, the checks.
    (r"scripts/", STUDIO, "the engine"),
    (r"jobs/", STUDIO, "one queue for every channel"),
    (r"JOBS\.md$", STUDIO, "the queue, as a page"),
    (r"channels/", STUDIO, "the registry of channels and the template for a new one"),
    (r"docs/", STUDIO, "the studio's plans"),
    (r"\.github/", STUDIO, "the checks"),
    (r"\.claude/|\.cursor/|\.cursorignore$", STUDIO, "agent settings and the generated copy of the rules"),
    (r"(AGENTS|CLAUDE|HANDOVER|README)\.md$", STUDIO, "the studio's rule book and front page"),
    (r"studio-core/", STUDIO, "the lock on shared tools (retires with the copies)"),
    (r"07_Content-Ops/", STUDIO, "the upload and social tools, shared by every channel"),
    (r"04_Audio/tools/", STUDIO, "the voice and sound tools, shared by every channel"),
    (r"00_Brand/Channel-Setup/tools/", STUDIO, "the gates and audits, shared by every channel"),
    (r"00_Brand/Channel-Setup/audits/start_studio_chrome_cdp\.sh$", STUDIO, "starts the Studio browsers, shared by every channel"),
    (r"00_Brand/Channel-Setup/STUDIO_PLAYBOOK\.md$", STUDIO, "the playbook, generated from the rule book"),
    # A channel's own numbers, kept beside the board today.
    (r"05_Analytics/{slug}/", "{slug}", "that channel's numbers: snapshots, Studio reads, first-day checks"),
    (r"05_Analytics/", STUDIO, "the board, the spend ledger and what the studio has learned"),
    # Built from other files on every run, so nobody keeps a copy.
    (r"STATUS\.md$", BUILT, "the status page"),
    # A file both need.
    (r"\.gitignore$", BOTH, "ignore rules"),
    # Everything else here is the home channel's content: films, brand, character, old work.
    (r"studio/", HOME_CHANNEL, "the channel's own settings and rules"),
    (r"02_Video-Projects/|00_Brand/|01_[^/]+/|04_Audio/|_archive/|_evidence/", HOME_CHANNEL, "films, brand and old work"),
)

GROUPS = (
    ("unrouted", "Files the table above does not place"),
    ("shared", "Shared tools the table would split between the studio and a channel"),
    ("names", "Studio code that still names a channel"),
    ("home", "Studio code that still reaches into a channel's folder from its own root"),
    ("registry", "The list of channels still needs one of them to be the studio's home"),
    ("keys", "Keys, tokens or filled-in .env files in what would move"),
    ("addresses", "Email addresses in what would become the studio repo"),
    ("tests", "Tests that fail once the studio and the channels are apart"),
)

# Shapes of keys. Built from pieces so this file does not match its own patterns.
_KEY_SHAPES = (
    ("s" + "k-" + r"(?:proj-|ant-)?[A-Za-z0-9_-]{24,}", True),
    ("AI" + "za" + r"[0-9A-Za-z_-]{35}", False),
    ("gh" + "p_" + r"[A-Za-z0-9]{36}", False),
    ("github" + "_pat_" + r"[A-Za-z0-9_]{40,}", False),
    ("xo" + "x[bap]-" + r"[A-Za-z0-9-]{20,}", False),
    ("-----BEGIN [A-Z ]*PRIVATE " + "KEY-----", False),
    ("ya" + r"29\.[A-Za-z0-9_-]{30,}", False),
)
KEY = re.compile("|".join(("(?<![A-Za-z0-9])" if word else "") + shape for shape, word in _KEY_SHAPES))
_KEY_PREFIXES = ("s" + "k-", "AI" + "za", "gh" + "p_", "github" + "_pat_", "xo" + "x", "PRIVATE " + "KEY-----", "ya" + "29.")
_BINARY_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp3", ".mp4", ".wav", ".mov", ".ico", ".woff", ".woff2", ".ttf")
# A web app's public identifier is shaped like a key and is not one: it is sent to every visitor's browser.
PUBLIC_ID_NEAR = re.compile(r"firebase:authUser:|securetoken\.googleapis\.com/v1/token\?key=")
ENV_FILE = re.compile(r"(^|/)\.env(\.[^/]*)?$")
ENV_EXAMPLE = (".example", ".sample", ".template")
TEXT_LIMIT = 2_000_000
SHOWN = 12   # lines listed under a heading; the count is always the full one


def resident(root: pathlib.Path) -> str | None:
    """The channel whose content lives in this repo today (its checkout is this folder), or None once none does."""
    here = pathlib.Path(root).resolve()
    return next((s for s in channels.slugs() if (channels.checkout(s) or pathlib.Path("/nowhere")).resolve() == here), None)


def tracked(root: pathlib.Path) -> list[str]:
    out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=True).stdout
    return sorted(p for p in out.decode("utf-8", "replace").split("\0") if p)


def route(path: str, slugs: list[str]) -> tuple[str, str] | None:
    """(where, why) for one tracked file, or None when the table does not place it."""
    any_slug = "(?P<slug>" + "|".join(re.escape(s) for s in slugs) + ")" if slugs else "(?P<slug>(?!))"
    for pattern, where, why in ROUTES:
        m = re.match(pattern.replace("{slug}", any_slug), path)
        if m:
            return (m.group("slug") if where == "{slug}" else where), why
    return None


def plan(files: list[str], slugs: list[str], home: str | None) -> dict:
    """{'studio': [...], <slug>: [...], 'built': [...], 'unrouted': [...]}. A file both need is in each list.

    `home` is the channel whose content is in this repo today, or None when none is (the studio already in a repo of
    its own). Then a file the table gives to the home channel has no place here, and is listed as unrouted."""
    out: dict = {STUDIO: [], BUILT: [], "unrouted": [], **{s: [] for s in slugs}}
    for f in files:
        r = route(f, slugs)
        if r is None:
            out["unrouted"].append(f)
        elif r[0] == BOTH:
            out[STUDIO].append(f)
            if home:
                out[home].append(f)
        elif r[0] == HOME_CHANNEL:
            out[home if home else "unrouted"].append(f)
        else:
            out[r[0]].append(f)
    return out


def shared_tools(root: pathlib.Path) -> list[str]:
    """The files both channels hold a hash-locked copy of today (studio-core/CORE_FILES.json)."""
    lock = root / "studio-core" / "CORE_FILES.json"
    if not lock.is_file():
        return []
    files = json.loads(lock.read_text()).get("files") or {}
    return sorted(files if isinstance(files, dict) else [f.get("path") for f in files if f.get("path")])


def _place(src: pathlib.Path, dest: pathlib.Path) -> None:
    """A copy, never a link: the tests run inside the scratch folder, and a test that rewrites a file in place must
    not reach the real one."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_symlink():              # a tracked link (some point at folders that only exist on the Mini): keep it a link
        os.symlink(os.readlink(src), dest)
    elif src.is_file():
        shutil.copy2(src, dest)


def _link_in(checkout: pathlib.Path, folder: pathlib.Path) -> None:
    """A folder that reads as a channel's checkout without being it: one link for each thing at its top. What the
    move adds to that channel (its numbers) can then be placed beside the links and never lands in the real checkout.
    Its `.git` is left out: nothing run in the scratch layout may reach the real repo's history or index."""
    folder.mkdir(parents=True)
    for entry in sorted(checkout.iterdir()):
        if entry.name != ".git":
            (folder / entry.name).symlink_to(entry.resolve(), target_is_directory=entry.is_dir())


def _own_folder(path: pathlib.Path, top: pathlib.Path) -> None:
    """Make every folder from `top` down to `path` a real one in the scratch layout. A link on the way (a folder the
    real checkout already has) becomes a folder of links to what it held, so a file placed under it stays in the
    scratch layout."""
    here = top
    for part in path.relative_to(top).parts:
        here = here / part
        if here.is_symlink():
            real = here.resolve()
            here.unlink()                 # the link, never what it points at
            here.mkdir()
            for entry in sorted(real.iterdir()):
                (here / entry.name).symlink_to(entry, target_is_directory=entry.is_dir())
        else:
            here.mkdir(exist_ok=True)


def build(scratch: pathlib.Path, root: pathlib.Path, placed: dict, home: str, others: dict) -> dict:
    """Make scratch/studio and one folder beside it for each channel. Returns {slug: folder} for the channels.

    `others`: {slug: its checkout or None}. A channel whose files are on this machine gets a folder of links to them;
    one that is not gets a folder holding only its settings (the cached copy), which is all the studio needs to list
    it. Either way its numbers, kept in the home repo today, are placed in its folder: that is where the move puts
    them."""
    studio = scratch / STUDIO
    for f in placed[STUDIO]:
        _place(root / f, studio / f)
    folders = {home: scratch / channels.get(home)["repo"]["checkouts"][0]}
    for f in placed[home]:
        _place(root / f, folders[home] / f)
    for slug, checkout in others.items():
        folder = scratch / (channels.get(slug)["repo"].get("checkouts") or [slug])[-1]
        if checkout:
            _link_in(pathlib.Path(checkout).resolve(), folder)
        else:
            cached = root / "channels" / slug / "channel.json"
            if cached.is_file():
                _place(cached, folder / "studio" / "channel.json")
        for f in placed.get(slug, []):
            _own_folder((folder / f).parent, folder)
            _place(root / f, folder / f)
        folders[slug] = folder
    return folders


def _rewrite(path: pathlib.Path, doc: dict, inside: pathlib.Path) -> None:
    """Write a settings file again, only if it is one of the dry run's own copies under `inside`: never a file
    reached through a link into a real checkout."""
    if path.is_symlink() or not path.resolve().is_relative_to(inside.resolve()):
        raise RuntimeError(f"{path} is not one of the dry run's own copies: left alone")
    path.unlink()                     # a new file, whatever the old one was
    path.write_text(json.dumps(doc, indent=2) + "\n")


def _as_a_repo(studio: pathlib.Path) -> None:
    """The scratch studio as the git repo it will be: its files tracked, in one first commit (plan decision 3: the
    studio repo starts clean). Checks that ask git which files are tracked then run there as they do here."""
    def git(*args: str) -> None:
        subprocess.run(["git", "-C", str(studio), "-c", "user.name=dry run", "-c", "user.email=dry-run",
                        "-c", "commit.gpgsign=false", *args], capture_output=True, check=True, timeout=300)
    git("init", "-q", "-b", "main")
    git("add", "-A")
    git("commit", "-q", "--no-verify", "-m", "The studio, as the move would leave it")


def plug_in(studio: pathlib.Path, folders: dict) -> tuple[str, dict]:
    """Point the scratch studio's registry at the folders beside it. Returns (why it cannot list its channels or '',
    the environment to run it in).

    After the move every channel is a folder beside the studio, found the same way: by the variable its own settings
    file names, as History of Science is today. Today the registry marks one channel as the studio's own repo; that
    mark is taken off here, and the registry is the only place that says it (a channel's settings file does not)."""
    reg_file = studio / "channels" / "channels.json"
    if not reg_file.is_file():
        return "channels/channels.json is not in the studio folder", dict(os.environ)
    reg = json.loads(reg_file.read_text())
    env = dict(os.environ)
    for entry in reg["channels"]:
        entry.pop("home", None)
        own = folders[entry["slug"]] / "studio" / "channel.json"
        named = (json.loads(own.read_text()).get("repo") or {}).get("env") if own.is_file() else ""
        entry.setdefault("env", named or "STUDIO_SPLIT_" + re.sub(r"\W", "_", entry["slug"]).upper())
        env[entry["env"]] = str(folders[entry["slug"]])
    _rewrite(reg_file, reg, studio)
    probe = "import channels; print(len(channels.slugs()))"
    r = subprocess.run([sys.executable, "-c", probe], cwd=str(studio / "scripts"), env=env, capture_output=True,
                       text=True, timeout=120)
    if r.returncode == 0:
        return "", env
    last = (r.stderr.strip().splitlines() or ["the channel list could not be read"])[-1]
    # "ValueError: /tmp/.../channels: exactly one channel must be home" -> the loader's own words, without the path
    return "the loader says: " + re.sub(r"^\w+(?:Error|Exception): (?:\S*/\S*: )?", "", last)[:160], env


def key_findings(root: pathlib.Path, files: list[str]) -> list[str]:
    """File names only. A `.env` that is not an example counts whatever it holds."""
    out = []
    for f in files:
        if ENV_FILE.search(f) and not f.endswith(ENV_EXAMPLE):
            out.append(f"{f}: a .env file that is not an example")
            continue
        if f.lower().endswith(_BINARY_SUFFIXES):
            continue
        path = root / f
        try:
            sz = path.stat().st_size
            if sz < 20 or sz > TEXT_LIMIT:
                continue
            text = path.read_text(errors="strict")
        except (OSError, UnicodeDecodeError):
            continue
        if not any(p in text for p in _KEY_PREFIXES):
            continue
        hits = [m for m in KEY.finditer(text) if not PUBLIC_ID_NEAR.search(text[max(0, m.start() - 60):m.start()])]
        if hits:
            out.append(f"{f}: {len(hits)} key-shaped string{'s' if len(hits) != 1 else ''}")
    return out


def address_files(root: pathlib.Path, files: list[str]) -> list[str]:
    out = []
    for f in files:
        if f.lower().endswith(_BINARY_SUFFIXES):
            continue
        path = root / f
        try:
            sz = path.stat().st_size
            if sz < 5 or sz > TEXT_LIMIT * 4:
                continue
            text = path.read_text(errors="strict")
            n = len(channel_check.ADDRESS.findall(text)) if "@" in text else 0
        except (OSError, UnicodeDecodeError):
            continue
        if n:
            out.append(f"{f}: {n} place{'s' if n != 1 else ''}")
    return out


def code_counts() -> tuple[dict, dict]:
    """The two counts of scripts/channel_ratchet.json, per script, counted now (never read from the file)."""
    import test_channel_ratchet as ratchet
    return ({k: v for k, v in ratchet.counts().items() if v}, {k: v for k, v in ratchet.home_counts().items() if v})


FAILED = re.compile(r"^(?:FAIL|ERROR): (\S+) \((?:[\w.]*\.)?(test_\w+)\.", re.M)


def failing_tests(output: str) -> dict:
    """{test file: [test names]} from unittest's text output."""
    out: dict = {}
    for test, module in FAILED.findall(output):
        out.setdefault(module + ".py", []).append(test)
    return out


def run_tests(studio: pathlib.Path, env: dict, timeout: int = 1500) -> dict:
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py"],
                       cwd=str(studio), env=env, capture_output=True, text=True, timeout=timeout)
    return failing_tests(r.stderr + r.stdout)


def check(root: pathlib.Path = ROOT, scratch: pathlib.Path | None = None, tests: bool = True) -> dict:
    slugs, home = channels.slugs(), resident(root)
    if home is None:
        raise SystemExit("no channel's content lives in this repo: the studio has already moved, there is nothing to rehearse")
    files = tracked(root)
    placed = plan(files, slugs, home)
    groups: dict = {key: [] for key, _ in GROUPS}
    groups["unrouted"] = placed["unrouted"]
    in_studio = set(placed[STUDIO])
    groups["shared"] = [f for f in shared_tools(root) if f in set(files) and f not in in_studio]
    names, reach = code_counts()
    groups["names"] = [f"{script}: {n} line{'s' if n != 1 else ''}" for script, n in sorted(names.items(), key=lambda kv: -kv[1])]
    groups["home"] = [f"{script}: {n} line{'s' if n != 1 else ''}" for script, n in sorted(reach.items(), key=lambda kv: -kv[1])]
    counts = {"names": sum(names.values()), "home": sum(reach.values())}
    groups["keys"] = key_findings(root, files)
    others = {s: channels.checkout(s) for s in slugs if s != home}
    for slug, checkout in others.items():
        if checkout:
            groups["keys"] += [f"{channels.get(slug)['name']}: {line}" for line in key_findings(checkout, tracked(checkout))]
    groups["addresses"] = address_files(root, placed[STUDIO])

    made = scratch is None
    scratch = pathlib.Path(tempfile.mkdtemp(prefix="studio-split-")) if made else pathlib.Path(scratch)
    tests_state = "not run"
    try:
        # When `made and not tests` (`--no-tests` without `--keep`), the temp folder is deleted at the end of this
        # call and only `plug_in` runs inside it, so only the registry and channel settings files need to be placed.
        for_scratch = ({
            STUDIO: [f for f in placed[STUDIO] if f.startswith("channels/") or f == "scripts/channels.py"],
            home: [f for f in placed[home] if f == "studio/channel.json"],
        } if (made and not tests) else placed)
        folders = build(scratch, root, for_scratch, home, others)
        why, env = plug_in(scratch / STUDIO, folders)
        if why:
            groups["registry"] = [why]
            tests_state = "not run: the studio cannot list its channels in the new layout yet"
        elif tests:
            _as_a_repo(scratch / STUDIO)
            failed = run_tests(scratch / STUDIO, env)
            groups["tests"] = [f"{name}: {len(which)} test{'s' if len(which) != 1 else ''}" for name, which in sorted(failed.items())]
            tests_state = "run"
    finally:
        if made:
            shutil.rmtree(scratch, ignore_errors=True)

    for key in groups:
        counts.setdefault(key, len(groups[key]))
    commit = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    dirty = bool(subprocess.run(["git", "-C", str(root), "status", "--porcelain"], capture_output=True, text=True).stdout.strip())
    return {
        "at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "commit": commit, "clean": not dirty,
        "left": sum(counts.values()),
        "counts": counts,
        "groups": [{"key": key, "title": title, "count": counts[key], "items": groups[key][:SHOWN]} for key, title in GROUPS],
        "tests": tests_state,
        "layout": {"studio": len(placed[STUDIO]), **{channels.get(s)["name"]: len(placed[s]) for s in slugs},
                   "built": len(placed[BUILT]),
                   "not on this machine": [channels.get(s)["name"] for s, co in others.items() if not co]},
    }


def report(res: dict) -> str:
    lines = [f"Dry run of the move at {res['at']} (commit {res['commit']}{'' if res['clean'] else ', with uncommitted changes'})."]
    lay = res["layout"]
    lines.append("Where the files would go: " + ", ".join(f"{name} {n}" for name, n in lay.items() if isinstance(n, int)) + ".")
    if lay.get("not on this machine"):
        lines.append("Not on this machine, so only their settings were plugged in: " + ", ".join(lay["not on this machine"]) + ".")
    if not res["left"]:
        lines.append("PASS. Nothing stops the move.")
        return "\n".join(lines)
    lines.append(f"{res['left']} thing{'s' if res['left'] != 1 else ''} still stop{'' if res['left'] != 1 else 's'} the move.")
    for g in res["groups"]:
        if not g["count"]:
            continue
        lines.append(f"\n{g['title']}: {g['count']}")
        lines += [f"  - {item}" for item in g["items"]]
        if g["key"] in ("names", "home"):
            pass   # the count is lines; the list is scripts
        elif g["count"] > len(g["items"]):
            lines.append(f"  - and {g['count'] - len(g['items'])} more")
    lines.append(f"\nTests in the new layout: {res['tests']}.")
    return "\n".join(lines)


def record(path: pathlib.Path, res: dict) -> None:
    """One line a day: a later run on the same day replaces that day's line."""
    day = res["at"][:10]
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.is_file() else []
    rows = [r for r in rows if r.get("day") != day] + [{"day": day, "at": res["at"], "left": res["left"], "commit": res["commit"],
                                                       "counts": res["counts"], "tests": res["tests"]}]
    rows.sort(key=lambda r: r["day"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))


def streak(path: pathlib.Path, today: dt.date | None = None) -> int:
    """Days in a row, ending today or yesterday, on which the dry run passed with its tests run. A missed day ends it."""
    if not path.is_file():
        return 0
    rows = {r["day"]: r for r in (json.loads(line) for line in path.read_text().splitlines() if line.strip())}
    day = today or dt.datetime.now(dt.timezone.utc).date()
    if day.isoformat() not in rows:
        day -= dt.timedelta(days=1)
    n = 0
    while True:
        r = rows.get(day.isoformat())
        if not r or r.get("left") != 0 or r.get("tests") != "run":
            return n
        n += 1
        day -= dt.timedelta(days=1)


def save(res: dict, json_path=None, history=None, git: bool = False) -> str | None:
    """Write the result (`json_path`) and the day's line (`history`). With `git`, do it on a clean main and push, so
    the count of days in a row outlives the machine that ran it. Returns what went wrong, or None."""
    def write() -> list:
        paths = []
        if json_path:
            json_path.parent.mkdir(parents=True, exist_ok=True)
            json_path.write_text(json.dumps(res, indent=2) + "\n")
            paths.append(json_path.resolve())
        if history:
            record(history, res)
            paths.append(history.resolve())
        return paths
    if not git:
        write()
        return None
    if not (json_path or history):
        return "--git needs --record or --json: there is nothing to commit"
    import studio
    return studio.git_transaction(lambda: (None, None, write()),
                                  f"dry run of the move: {res['left']} left on {res['at'][:10]}")[1]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", type=pathlib.Path, help="write the result here as JSON")
    ap.add_argument("--record", type=pathlib.Path, help="add today's result to this history file")
    ap.add_argument("--streak", type=pathlib.Path, help="print the days in a row the dry run has passed, and stop")
    ap.add_argument("--keep", type=pathlib.Path, help="build the layout here and leave it (the folder must not exist)")
    ap.add_argument("--no-tests", action="store_true", help="skip running the tests in the new layout")
    ap.add_argument("--git", action="store_true",
                    help="commit --json and --record on a clean main and push (the daily run)")
    a = ap.parse_args(argv)
    if a.streak:
        print(streak(a.streak))
        return 0
    if a.keep and a.keep.exists():
        print(f"not run: {a.keep} already exists")
        return 2
    res = check(ROOT, a.keep, tests=not a.no_tests)
    print(report(res))
    err = save(res, a.json, a.record, a.git)
    if err:
        print(f"not recorded: {err}", file=sys.stderr)
        return 2
    return 0 if res["left"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
