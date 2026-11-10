#!/usr/bin/env python3
"""Start a new channel: make its folder, ready to become a repo the studio can drive.

    python3 scripts/channel_new.py <slug> --label ABC --name "Channel Name" [--handle @Handle] [--wip 2] [--into DIR]

Ben, 10 Nov 2026: "We want a system that we can start plugging in repos that will be channels and start building
up new channels." This makes `<DIR>/<slug>/` from `channels/_template/`, writes its `studio/channel.json`, and
runs `channel_check.py` on the result. It makes a folder on this machine and nothing else: it does not create a
GitHub repo, sign in to YouTube or touch the registry. Those are the next steps it prints.

A new channel starts on the picture route that cannot bill (`flow_only`) and with two films in work at most.
Both are one line each in `studio/channel.json` to change later.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import channel_check  # noqa: E402
import channels  # noqa: E402
import studio  # noqa: E402

TEMPLATE = HERE.parent / "channels" / "_template"
RENAME = {"gitignore": ".gitignore"}  # a real .gitignore in the template would apply to this repo


def settings(slug: str, label: str, name: str, handle: str = "", wip: int = 2, order: int = 99) -> dict:
    return {
        "slug": slug,
        "label": label,
        "name": name,
        "short": name,
        "home": False,
        "order": order,
        "youtube": {"handle": handle},
        "repo": {"url": "", "env": f"{label}_REPO", "checkouts": [slug]},
        "nas_folder": slug,
        "title_match": rf"\b{re.escape(label)}\b|{re.escape(name.lower())}",
        "wip": {"limit": wip, "line": f"next_{slug.replace('-', '_')}"},
        "stages": list(studio.STAGES),
        "pipeline": {"kind": "film_status", "path": "02_Video-Projects/*/status.json"},
        "uat_dir": {"env": f"{label}_UAT_DIR", "icloud": f"{label} UAT"},
        "picture_route": "flow_only",
    }


def create(parent: pathlib.Path, slug: str, label: str, name: str, handle: str = "", wip: int = 2,
           registered: list[dict] | None = None) -> pathlib.Path:
    """Make the channel's folder under `parent` and return it. ValueError, with nothing written, if it cannot be made."""
    registered = channels.all_channels() if registered is None else registered
    c = settings(slug, label, name, handle, wip, order=max([x.get("order", 0) for x in registered] + [0]) + 1)
    problems = channel_check.settings_problems(c) + channel_check.clashes(c, registered)
    if problems:
        raise ValueError("; ".join(problems))
    root = pathlib.Path(parent) / slug
    if root.exists():
        raise ValueError(f"{root} already exists")
    shutil.copytree(TEMPLATE, root)
    for old, new in RENAME.items():
        (root / old).rename(root / new)
    for path in root.rglob("*.md"):
        text = path.read_text()
        path.write_text(text.replace("{{NAME}}", name).replace("{{LABEL}}", label).replace("{{SLUG}}", slug))
    (root / "studio" / "channel.json").write_text(json.dumps(c, indent=2) + "\n")
    must, _todo = channel_check.check(root)
    if must:  # the template itself is wrong: leave nothing half-made
        shutil.rmtree(root)
        raise ValueError("the template does not pass channel_check: " + "; ".join(must))
    return root


NEXT = """
Next, in this order:
  1. Ben: create the GitHub repo for it, and do the channel's YouTube sign-in and voice.
  2. In {root}: git init, commit, push to that repo. Put its address in studio/channel.json (repo.url).
  3. Here: add one line to channels/channels.json,
       {{"slug": "{slug}", "env": "{label}_REPO", "checkouts": ["{slug}"]}}
     then `python3 scripts/channels.py sync` and `python3 scripts/channel_check.py --all`.
  4. Write the channel's rules in studio/RULES.md before its first script.

The studio can drive a third channel once both counts in scripts/channel_ratchet.json are at zero
(docs/MULTI_CHANNEL_PLAN.md). Until then the folder is ready and waiting.
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", help="lower-case short name, e.g. deep-sea")
    ap.add_argument("--label", required=True, help="2 to 6 capitals: the film-key prefix, e.g. SEA")
    ap.add_argument("--name", required=True, help="the channel's public name")
    ap.add_argument("--handle", default="", help="its YouTube handle, if it has one yet")
    ap.add_argument("--wip", type=int, default=2, help="films it may have in work at once (default 2)")
    ap.add_argument("--into", default=str(pathlib.Path.home() / "YouTube"), help="folder to make it in")
    args = ap.parse_args(argv)
    try:
        root = create(pathlib.Path(args.into), args.slug, args.label, args.name, args.handle, args.wip)
    except ValueError as e:
        print(f"not made: {e}")
        return 1
    print(channel_check.report(args.slug, *channel_check.check(root)))
    print(NEXT.format(root=root, slug=args.slug, label=args.label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
