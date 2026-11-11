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
  channels.analytics_dir("hos")     where its numbers are kept (snapshots, Studio reads, first-day checks)
  channels.uploads_file("hos")      its register of uploads, or None when its checkout is not on this machine

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


def default() -> str:
    """The channel of a job or file that names none (old queue rows, backlog items without `repo`). Today that is
    the channel this repo belongs to. When the studio has its own repo this becomes a field in the registry, and
    this is the one line that moves."""
    return home()


def queue_key() -> str:
    """The key in board.json under which the studio's job queue is published (jobs, done, focus). The queue is the
    studio's, not a channel's; kanban_snapshot.py writes it under the home channel's slug for the board page."""
    return home()


def studio_records(*parts: str) -> pathlib.Path:
    """Where the studio keeps records that belong to no one channel: the AI spend ledger, the thumbnail test ledger.
    Today a folder beside the channels' numbers in this repo. When the studio has its own repo this is the one line
    that moves."""
    return ROOT.joinpath("05_Analytics", *parts)


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


def label_of_repo(repo) -> str:
    """The label for a record's `repo` (or channel) field: that channel's when it names one, else the default
    channel's. Unlike `of_job` it never reads a title."""
    r = str(repo or "").lower()
    return label(r if r in slugs() else default())


def planned_shorts(slug: str) -> int:
    """How many Shorts the board plans for each upcoming long of this channel: `shorts.planned_per_long` in its
    studio/channel.json, 0 when it names none. A checkout that is behind its main branch may not have the field
    yet; then the studio's cached copy of the file (channels/<slug>/channel.json) answers."""
    c = get(slug)
    for doc in (c, _cached(c["slug"])):
        shorts = doc.get("shorts")
        n = shorts.get("planned_per_long") if isinstance(shorts, dict) else None
        if isinstance(n, int) and not isinstance(n, bool) and n >= 0:
            return n
    return 0


def _cached(slug: str) -> dict:
    try:
        return json.loads((DIR / slug / "channel.json").read_text())
    except (OSError, ValueError):
        return {}


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


def studio_port(slug: str) -> str:
    """The CDP port of the browser signed in to this channel's YouTube Studio ('' if it has none yet)."""
    return str((get(slug).get("youtube") or {}).get("studio_port") or "")


def youtube_id(slug: str) -> str:
    """The channel's YouTube channel id (UC...), '' if its file names none."""
    return str((get(slug).get("youtube") or {}).get("id") or "")


def reach_port(slug: str) -> int | None:
    """The CDP port the monthly Studio Reach read uses for this channel, or None when its file names none (it need
    not be the Studio port: a channel can keep a separate browser for the read)."""
    port = (get(slug).get("youtube") or {}).get("reach_port")
    return int(port) if port else None


def sound_kit(slug: str) -> str:
    """The name of the channel's house sound kit (a recipe in sfx_kit.KITS), '' if its file names none."""
    return str(get(slug).get("sound_kit") or "")


def nas_folder(slug: str) -> str:
    """The channel's folder name under studio-live on the NAS. A channel that names none uses its slug."""
    return get(slug).get("nas_folder") or get(slug)["slug"]


def pipeline(slug: str) -> dict:
    """How the channel keeps its film state: {'kind': 'film_status' | 'pipeline_json', 'path': ...} ({} if unset).
    Code that reads a channel's films or their history branches on the kind, never on which channel it is."""
    return dict(get(slug).get("pipeline") or {})


def checkout(slug: str) -> pathlib.Path | None:
    """Where the channel is checked out on this machine, or None. The home channel's checkout is this repo."""
    if get(slug).get("home"):
        return ROOT
    path = repo_path(slug)
    return path if (path / "studio" / "channel.json").is_file() else None


def of_path(path) -> str:
    """The channel whose checkout holds this file or folder (a film folder, a status.json), else the default one."""
    p = pathlib.Path(path).resolve()
    for slug in slugs():
        co = checkout(slug)
        if co and (p == co.resolve() or co.resolve() in p.parents):
            return slug
    return default()


def analytics_dir(slug: str) -> pathlib.Path:
    """Where the channel's numbers are kept: the daily snapshots, the Studio reads, the first-day checks. Today that
    is one folder per channel in this repo. When the studio has its own repo this is the one line that moves."""
    return ROOT / "05_Analytics" / get(slug)["slug"]


def uploads_file(slug: str) -> pathlib.Path | None:
    """The channel's register of uploads (video id, kind, publish time), or None when its checkout is not here."""
    base = checkout(slug)
    return base / "00_Brand" / "Channel-Setup" / "social" / "UPLOADS.json" if base else None


def studio_checkout(home_dir: pathlib.Path | None = None) -> pathlib.Path:
    """The checkout that carries the studio's own data (the board branch, the job queue). Today that is the home
    channel's repo. When the studio has its own repo this is the one line that moves."""
    return repo_path(home(), home_dir)


def studio_slug() -> str:
    """The channel whose repo carries the studio's own code and data (the scripts, the job queue), for code that
    must clone or pull that repo. Today that is the home channel. When the studio has its own repo this goes, with
    studio_checkout()."""
    return home()


def studio_github() -> str:
    """`owner/name` on GitHub of the repo that carries the studio's board and threads (today the home channel's)."""
    return re.sub(r"^https://github\.com/|\.git$", "", get(home())["repo"]["url"])


def home_label() -> str:
    """The label a record gets when it names no channel (the old `or "OWB"`)."""
    return label(home())


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
