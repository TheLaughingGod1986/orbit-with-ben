#!/usr/bin/env python3
"""The channels plugged into the studio (docs/MULTI_CHANNEL_PLAN.md, phase 1; Ben, 5 Nov 2026: "this workflow system
to work for multiple channels, so we just plug in new channels").

Each channel is a folder `channels/<slug>/channel.json` (see channels/README.md). Engine code asks this module instead
of naming a channel:

  channels.slugs()                  ['owb', 'hos'] in order
  channels.label("hos")             'HOS'          (film-key prefix: HOS:013)
  channels.of_job(job)              'hos'          from job.repo, else its title, else the home channel
  channels.label_of_job(job)        'HOS'
  channels.film_keys(text)          {'OWB:033', 'HOS:013'} named in a title or result
  channels.repo_path("hos")         the checkout ($HOS_REPO, else the first ~/YouTube folder that exists)

  python3 scripts/channels.py       list them, and which file each came from
  python3 scripts/channels.py sync  refresh the cached copies from the channels' own checkouts
"""
from __future__ import annotations

import functools
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "channels"
REQUIRED = ("slug", "label", "name", "repo", "title_match", "wip")


def _checkout(entry: dict, home_dir: pathlib.Path | None = None) -> pathlib.Path | None:
    """Where a registry entry's own repo is checked out on this machine, or None."""
    if entry.get("home"):
        return ROOT
    env = os.environ.get(entry.get("env") or "")
    cands = [pathlib.Path(env)] if env else []
    names = entry.get("checkouts") or [entry["slug"]]
    cands += [(home_dir or pathlib.Path.home()) / "YouTube" / n for n in names]
    cands += [ROOT.parent / n for n in names]
    return next((c for c in cands if (c / "studio" / "channel.json").is_file()), None)


def _check(c: dict, where) -> dict:
    missing = [k for k in REQUIRED if k not in c]
    if missing:
        raise ValueError(f"{where}: bad channel file (missing {missing})")
    return c


@functools.lru_cache(maxsize=None)
def _load(directory: str = str(DIR)) -> tuple:
    """Every channel, in order. With a registry (channels/channels.json) each channel's settings come from its own
    repo's studio/channel.json, or the cached channels/<slug>/channel.json when that repo isn't here. Without one
    (tests), every channels/*/channel.json."""
    base = pathlib.Path(directory)
    reg = base / "channels.json"
    out = []
    if reg.is_file():
        for entry in json.loads(reg.read_text())["channels"]:
            co = _checkout(entry) if base == DIR else None
            src = (co / "studio" / "channel.json") if co else base / entry["slug"] / "channel.json"
            if entry.get("home") and not co:
                src = ROOT / "studio" / "channel.json"
            c = _check(json.loads(src.read_text()), src)
            if c["slug"] != entry["slug"]:
                raise ValueError(f"{src}: slug {c['slug']!r} but the registry says {entry['slug']!r}")
            out.append(dict(c, _source=str(src)))
    else:
        for p in sorted(base.glob("*/channel.json")):
            c = _check(json.loads(p.read_text()), p)
            if c["slug"] != p.parent.name:
                raise ValueError(f"{p}: slug != folder")
            out.append(c)
    out.sort(key=lambda c: (c.get("order", 99), c["slug"]))
    if sum(1 for c in out if c.get("home")) != 1:
        raise ValueError(f"{directory}: exactly one channel must be home")
    return tuple(out)


def sync() -> list[str]:
    """Copy each non-home channel's studio/channel.json from its checkout into the cached channels/<slug>/channel.json."""
    reg = json.loads((DIR / "channels.json").read_text())["channels"]
    done = []
    for entry in reg:
        co = None if entry.get("home") else _checkout(entry)
        if co:
            dest = DIR / entry["slug"] / "channel.json"
            dest.parent.mkdir(parents=True, exist_ok=True)
            text = (co / "studio" / "channel.json").read_text()
            if not dest.is_file() or dest.read_text() != text:
                dest.write_text(text)
                done.append(entry["slug"])
    _load.cache_clear()
    return done


def all_channels() -> list[dict]:
    return [dict(c) for c in _load()]


def get(slug: str) -> dict:
    s = str(slug or "").lower()
    for c in _load():
        if c["slug"] == s or c["label"].lower() == s:
            return dict(c)
    raise KeyError(f"no channel {slug!r} (have {', '.join(slugs())})")


def slugs() -> list[str]:
    return [c["slug"] for c in _load()]


def labels() -> list[str]:
    return [c["label"] for c in _load()]


def home() -> str:
    return next(c["slug"] for c in _load() if c.get("home"))


def label(slug: str) -> str:
    return get(slug)["label"]


def name(slug: str) -> str:
    return get(slug)["name"]


def of_job(job: dict) -> str:
    """The job's channel: its `repo` when that is a channel, else the first channel whose title_match fits its title,
    else the home channel (the old 'HOS if repo == hos or HOS in the title, else OWB')."""
    repo = str(job.get("repo") or "").lower()
    if repo in slugs():
        if repo != home():
            return repo
    title = str(job.get("title") or "")
    for c in _load():
        if not c.get("home") and re.search(c["title_match"], title, re.I):
            return c["slug"]
    return repo or home()


def label_of_job(job: dict) -> str:
    return label(of_job(job))


@functools.lru_cache(maxsize=None)
def key_re() -> re.Pattern:
    """`OWB:033`, `HOS 013`, `hos-013` ... for every channel's label."""
    return re.compile(r"\b(" + "|".join(map(re.escape, labels())) + r")\s*[:·-]?\s*(\d{3})\b", re.I)


@functools.lru_cache(maxsize=None)
def strict_key_re() -> re.Pattern:
    """A film key as stored: `OWB:033`."""
    return re.compile(r"(?:" + "|".join(map(re.escape, labels())) + r"):\d{3}")


def film_keys(text: str) -> set[str]:
    return {ch.upper() + ":" + no for ch, no in key_re().findall(str(text or ""))}


def wip_line(slug: str) -> str:
    """The key in jobs/WIP.json that holds this channel's waiting line (rule G)."""
    return get(slug)["wip"].get("line") or f"next_{slug}"


def repo_path(slug: str, home_dir: pathlib.Path | None = None) -> pathlib.Path:
    """The channel's checkout: its env var, else the first ~/YouTube/<name> that exists, else the first name."""
    r = get(slug)["repo"]
    if os.environ.get(r.get("env", "")):
        return pathlib.Path(os.environ[r["env"]])
    base = (home_dir or pathlib.Path.home()) / "YouTube"
    cands = [base / n for n in r.get("checkouts") or [slug]]
    return next((c for c in cands if c.is_dir()), cands[0])


def main() -> int:
    if sys.argv[1:] == ["sync"]:
        changed = sync()
        print("cached copies refreshed: " + (", ".join(changed) or "none changed"))
        return 0
    for c in _load():
        print(f"{c['slug']:<5} {c['label']:<4} {c['name']:<22} {'home ' if c.get('home') else ''}"
              f"wip {c['wip'].get('limit')} line {c['wip'].get('line')}  ({c.get('_source', '')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
