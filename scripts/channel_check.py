#!/usr/bin/env python3
"""Can the studio drive this channel? The contract a channel's repo has to meet.

    python3 scripts/channel_check.py <checkout>   one channel checkout
    python3 scripts/channel_check.py --all        every registered channel whose checkout is on this machine

Ben, 10 Nov 2026: "We want a system that we can start plugging in repos that will be channels." A channel is a
repo with a `studio/` folder. The studio reads that folder and never needs to know the channel's name. This check
is what "plugged in" means: it runs before a channel joins `channels/channels.json`, and it is meant to run in the
channel's own CI once the studio has its own repo (docs/MULTI_CHANNEL_PLAN.md, decision 6).

Two lists come back.

Must (exit 1 if any): without these the studio cannot run the channel.
  - `studio/channel.json` is there, is valid JSON and has every field, each of the right shape;
  - the place it says its films' progress lives exists and can be read;
  - nothing under `studio/` holds a personal email address (the repos are public).

To do (printed, never fails): where the channel still differs from the three-repo layout. Each becomes a "must"
when both of today's channels have got there.
  - its own rules file, `studio/RULES.md`;
  - one status file per film, rather than one big pipeline file;
  - no generated status page committed to the repo;
  - no copied studio tools (`studio-core/`);
  - the GitHub address of its repo filled in.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
SETTINGS = pathlib.PurePosixPath("studio/channel.json")
RULES = pathlib.PurePosixPath("studio/RULES.md")
PIPELINE_KINDS = ("film_status", "pipeline_json")
PICTURE_ROUTES = ("flow_only", "flow_first")
# The same pattern as scripts/test_email_ratchet.py (a test there keeps the two in step).
ADDRESS = re.compile(r"[A-Za-z0-9._%+-]+@(gmail|googlemail|outlook|hotmail|live|icloud|yahoo|protonmail|proton)\\?\.(com|me|co\.uk)")
GENERATED_PAGES = ("STATUS.md", "00_Brand/Channel-Setup/kanban/index.html")
# A publishing slot, "Sun 18:00". The same pattern as scripts/channels.py (a test keeps the two in step).
SLOT = re.compile(r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([01]\d|2[0-3]):([0-5]\d)")


def _text(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def settings_problems(c) -> list[str]:
    """What is wrong with a channel's settings (the parsed studio/channel.json). Empty when the studio can use them."""
    if not isinstance(c, dict):
        return ["studio/channel.json must be a JSON object"]
    out = []

    def need(ok: bool, message: str) -> None:
        if not ok:
            out.append(message)

    need(isinstance(c.get("slug"), str) and re.fullmatch(r"[a-z][a-z0-9-]{1,30}", c.get("slug", "")) is not None,
         "slug: lower-case letters, digits and hyphens, 2 to 31 characters (it is what jobs carry in `repo`)")
    need(isinstance(c.get("label"), str) and re.fullmatch(r"[A-Z][A-Z0-9]{1,5}", c.get("label", "")) is not None,
         "label: 2 to 6 capitals or digits (it is the film-key prefix, as in ABC:012)")
    need(_text(c.get("name")), "name: the channel's public name")
    repo = c.get("repo")
    need(isinstance(repo, dict) and isinstance(repo.get("url"), str) and isinstance(repo.get("checkouts"), list)
         and all(_text(x) for x in repo.get("checkouts", [])) and bool(repo.get("checkouts")),
         "repo: needs `url` (may be empty until the GitHub repo exists) and `checkouts`, the folder names to look for")
    try:
        re.compile(c.get("title_match") or "(")
    except re.error:
        out.append("title_match: must be a regular expression that marks a job title as this channel's")
    wip = c.get("wip")
    need(isinstance(wip, dict) and isinstance(wip.get("limit"), int) and not isinstance(wip.get("limit"), bool)
         and wip.get("limit", 0) >= 1 and _text(wip.get("line")),
         "wip: needs `limit` (a whole number, 1 or more) and `line` (the name of its waiting line)")
    stages = c.get("stages")
    need(stages == "from pipeline" or (isinstance(stages, list) and stages and all(_text(s) for s in stages)),
         "stages: the production stages in order, or \"from pipeline\"")
    pipe = c.get("pipeline")
    need(isinstance(pipe, dict) and pipe.get("kind") in PIPELINE_KINDS and _text(pipe.get("path")),
         f"pipeline: needs `kind` ({' or '.join(PIPELINE_KINDS)}) and `path`")
    uat = c.get("uat_dir")
    need(isinstance(uat, dict) and _text(uat.get("icloud")), "uat_dir: needs `icloud`, the watch folder's name")
    need(c.get("picture_route") in PICTURE_ROUTES, f"picture_route: {' or '.join(PICTURE_ROUTES)}")
    # Five optional settings. Left out, the channel has no YouTube Studio browser yet, its NAS folder is its slug,
    # the board holds no places for Shorts that are not made yet, it has no publishing days of its own and its
    # TikTok posts are not held to Buffer.
    port = (c.get("youtube") or {}).get("studio_port") if isinstance(c.get("youtube"), dict) else None
    need(port in (None, "") or (isinstance(port, str) and port.isdigit()),
         "youtube.studio_port: the browser port of its YouTube Studio, as digits in a string, e.g. \"9224\"")
    need("nas_folder" not in c or (_text(c["nas_folder"]) and "/" not in c["nas_folder"]),
         "nas_folder: its folder name under studio-live on the NAS (one name, no slashes)")
    planned = (c.get("shorts") or {}).get("planned_per_long") if isinstance(c.get("shorts", {}), dict) else "bad"
    need(planned is None or (isinstance(planned, int) and not isinstance(planned, bool) and planned >= 0),
         "shorts.planned_per_long: how many Shorts each long video gets a place for on the board (a whole number, 0 or more)")
    cadence = c.get("cadence")
    need(cadence is None or (isinstance(cadence, dict) and bool(cadence) and set(cadence) <= {"long", "short"}
                             and all(isinstance(slots, list) and slots
                                     and all(isinstance(s, str) and SLOT.fullmatch(s) for s in slots)
                                     for slots in cadence.values())),
         "cadence: its publishing slots in London time, in the order they are filled, as "
         "{\"long\": [\"Sun 18:00\"], \"short\": [\"Mon 11:30\"]}")
    social = c.get("social")
    need(social is None or (isinstance(social, dict) and social.get("tiktok") in (None, "buffer")),
         "social.tiktok: \"buffer\" when its TikTok posts go through Buffer only; leave it out otherwise")
    desk = c.get("desk")
    number = desk.get("number") if isinstance(desk, dict) else None
    need(desk is None or (isinstance(desk, dict) and _text(desk.get("tool")) and desk["tool"].endswith(".py")
                          and not desk["tool"].startswith(("/", "~")) and ".." not in desk["tool"].split("/")
                          and isinstance(number, int) and not isinstance(number, bool) and number > 0),
         "desk: when the channel runs its own desk, {\"tool\": the desk tool's path inside its repo (a .py file), "
         "\"number\": the number of the desk's thread}; leave it out otherwise")
    return out


def _pipeline_problems(root: pathlib.Path, pipe: dict) -> list[str]:
    path = pipe["path"]
    if pipe["kind"] == "pipeline_json":
        file = root / path
        if not file.is_file():
            return [f"pipeline: {path} is not in the checkout"]
        try:
            films = json.loads(file.read_text()).get("films")
        except (ValueError, AttributeError):
            return [f"pipeline: {path} is not valid JSON"]
        return [] if isinstance(films, list) else [f"pipeline: {path} has no `films` list"]
    fixed = path.split("*")[0].rstrip("/")
    if not (root / fixed).is_dir():
        return [f"pipeline: the folder {fixed}/ is not in the checkout"]
    bad = []
    for file in sorted(root.glob(path)):
        try:
            film = json.loads(file.read_text())
            if not isinstance(film.get("stages"), dict):
                bad.append(f"{file.relative_to(root)}: no `stages`")
        except (ValueError, AttributeError):
            bad.append(f"{file.relative_to(root)}: not valid JSON")
    return [f"pipeline: {b}" for b in bad[:5]] + ([f"pipeline: and {len(bad) - 5} more" ] if len(bad) > 5 else [])


def check(root: pathlib.Path) -> tuple[list[str], list[str]]:
    """(must fix, still to do) for the channel checked out at `root`."""
    root = pathlib.Path(root)
    file = root / SETTINGS
    if not file.is_file():
        return [f"{SETTINGS} is missing: a channel is a repo with that file in it"], []
    try:
        c = json.loads(file.read_text())
    except ValueError as e:
        return [f"{SETTINGS} is not valid JSON: {e}"], []
    must = settings_problems(c)
    if not must:
        must += _pipeline_problems(root, c["pipeline"])
    for path in sorted((root / "studio").rglob("*")):
        if path.is_file():
            try:
                if ADDRESS.search(path.read_text(errors="replace")):
                    must.append(f"{path.relative_to(root)} holds a personal email address: say \"the studio account\"")
            except OSError:
                continue
    if must:
        return must, []
    todo = []
    if not (root / RULES).is_file():
        todo.append(f"{RULES}: the channel's own rules (titles, voice, picture). It can add to the studio's rules, never remove one")
    if c["pipeline"]["kind"] != "film_status":
        todo.append("one status file per film instead of one pipeline file (fewer merge conflicts)")
    pages = [p for p in GENERATED_PAGES if (root / p).is_file()]
    if pages:
        todo.append("generated pages are committed (" + ", ".join(pages) + "): the studio should build them, not the repo hold them")
    if (root / "studio-core").is_dir():
        todo.append("studio-core/: copied studio tools, to retire when the studio has its own repo")
    if not _text(c["repo"]["url"]):
        todo.append("repo.url is empty: put the GitHub address in once the repo exists")
    if not c.get("cadence"):
        todo.append("cadence: no publishing days of its own yet (Ben's call). Until it has them, an approved cut "
                    "is given the default channel's days")
    return [], todo


def clashes(c: dict, registered: list[dict]) -> list[str]:
    """Why this channel cannot join the registry beside the ones already in it."""
    out = []
    for other in registered:
        if other.get("slug") == c.get("slug"):
            out.append(f"slug {c['slug']!r} is already registered")
        if other.get("label") == c.get("label"):
            out.append(f"label {c['label']!r} is already used by {other.get('slug')}")
    return out


def report(name: str, must: list[str], todo: list[str]) -> str:
    if must:
        return f"{name}: the studio cannot drive it yet.\n" + "\n".join(f"  - {m}" for m in must)
    if todo:
        return (f"{name}: the studio can drive it. Still to do for the three-repo layout:\n"
                + "\n".join(f"  - {t}" for t in todo))
    return f"{name}: the studio can drive it. Nothing left to do."


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("checkout", nargs="?", help="path to a channel's checkout")
    ap.add_argument("--all", action="store_true", help="every registered channel whose checkout is on this machine")
    args = ap.parse_args(argv)
    if bool(args.checkout) == bool(args.all):
        ap.error("give one checkout, or --all")
    targets = []
    if args.all:
        sys.path.insert(0, str(HERE))
        import channels

        for slug in channels.slugs():
            path = channels.checkout(slug)
            if path:
                targets.append((slug, path))
            else:
                print(f"{slug}: its checkout is not on this machine; not checked")
    else:
        targets.append((pathlib.Path(args.checkout).resolve().name, pathlib.Path(args.checkout)))
    failed = False
    for name, path in targets:
        must, todo = check(path)
        failed = failed or bool(must)
        print(report(name, must, todo))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
