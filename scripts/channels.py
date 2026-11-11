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
            # Whether a channel's content lives in the studio's own root is the registry's to say, not the channel's:
            # a channel's settings file reads the same whichever studio it is plugged into.
            out.append(dict(c, home=bool(entry.get("home")), _source=str(src)))
    else:
        for p in sorted(base.glob("*/channel.json")):
            c = _check(json.loads(p.read_text()), p)
            if c["slug"] != p.parent.name:
                raise ValueError(f"{p}: slug != folder")
            out.append(c)
    out.sort(key=lambda c: (c.get("order", 99), c["slug"]))
    if sum(1 for c in out if c.get("home")) > 1:
        raise ValueError(f"{directory}: at most one channel can be home")
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


def home() -> str | None:
    """The channel whose content lives in the studio's own root (the registry marks it `home`), or None when none
    does: the studio in a repo of its own, with every channel a folder beside it (plan decision 1). Engine code asks
    one of the questions below instead: which channel a record that names none belongs to (`default`), where a
    channel is checked out (`checkout`), where the studio's own repo is (`studio_checkout`)."""
    return next((c["slug"] for c in _load() if c.get("home")), None)


def default() -> str:
    """The channel of a job or file that names none (old queue rows, backlog items without `repo`): the registry's
    `studio.default_channel`. It is a field of its own so the answer does not depend on which channel, if any, the
    studio's repo is also home to. A registry without the field (or naming a channel that is not plugged in) gives
    the home channel, else the first channel in order."""
    kept = _studio_section().get("default_channel")
    return kept if kept in slugs() else home() or slugs()[0]


def queue_key() -> str:
    """The key in board.json under which the studio's job queue is published (jobs, done, focus). The queue is the
    studio's, not a channel's; kanban_snapshot.py writes it under the default channel's slug for the board page."""
    return default()


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
    else the default channel (the old 'HOS if repo == hos or HOS in the title, else OWB')."""
    repo = str(job.get("repo") or "").lower()
    own = default()
    if repo in slugs():
        if repo != own:
            return repo
    title = str(job.get("title") or "")
    for c in _load():
        if c["slug"] != own and re.search(c["title_match"], title, re.I):
            return c["slug"]
    return repo or own


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


WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
SLOT = re.compile(r"(" + "|".join(WEEKDAYS) + r") ([01]\d|2[0-3]):([0-5]\d)")  # "Sun 18:00"


def cadence(slug: str) -> dict:
    """The channel's locked publishing slots (Ben, 7 Nov 2026): {'long': [(weekday, hour, minute), ...], 'short':
    [...]}, London time, Mon=0 … Sun=6, in the order the channel fills them. From `cadence` in its
    studio/channel.json, written as "Sun 18:00"; {} when it names none. A checkout that is behind its main branch
    may not have the field yet; then the studio's cached copy of the file answers. A slot that does not read as a
    weekday and a time is an error, never a slot quietly dropped: these decide the day a video goes out."""
    c = get(slug)
    for doc in (c, _cached(c["slug"])):
        kept = doc.get("cadence")
        if not isinstance(kept, dict):
            continue
        out = {}
        for kind in ("long", "short"):
            slots = kept.get(kind) or []
            out[kind] = []
            for slot in slots if isinstance(slots, list) else [slots]:
                m = SLOT.fullmatch(slot) if isinstance(slot, str) else None
                if not m:
                    raise ValueError(f"{c['slug']}: cadence.{kind} slots read like \"Sun 18:00\", not {slot!r}")
                out[kind].append((WEEKDAYS.index(m.group(1)), int(m.group(2)), int(m.group(3))))
        if any(out.values()):
            return out
    return {}


def tiktok_by_buffer(slug: str) -> bool:
    """True when the channel's TikTok posts go through Buffer only (`social.tiktok` is "buffer" in its
    studio/channel.json, or in the cached copy when its checkout is behind)."""
    c = get(slug)
    for doc in (c, _cached(c["slug"])):
        social = doc.get("social")
        if isinstance(social, dict) and "tiktok" in social:
            return social["tiktok"] == "buffer"
    return False


def desk(slug: str) -> dict:
    """The channel's desk, when it runs one: {'tool': the desk tool's path inside its checkout, 'number': the number
    of the desk's thread}. {} when it has none. From `desk` in its studio/channel.json, or the studio's cached copy
    when its checkout is behind. A desk is where a channel's own Chief and reviewers talk; the relay sends an agent
    to its inbox before the shared queue."""
    c = get(slug)
    for doc in (c, _cached(c["slug"])):
        kept = doc.get("desk")
        if isinstance(kept, dict) and kept.get("tool"):
            return {"tool": str(kept["tool"]), "number": kept.get("number")}
    return {}


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


def board_channel() -> str:
    """The channel whose films the stage board tracks (studio.py: one status.json per film, claims, STATUS.md): the
    first channel that keeps its film state that way (pipeline kind film_status), else the default channel."""
    return next((c["slug"] for c in _load() if (c.get("pipeline") or {}).get("kind") == "film_status"), default())


def films_dir(slug: str, in_checkout: pathlib.Path | None = None) -> pathlib.Path:
    """The folder that holds the channel's film folders, in the channel's own checkout (where that checkout would be
    when it is not on this machine): the part of its pipeline path before the first wildcard. `in_checkout` asks for
    the same folder inside another copy of that channel's repo (the relay's, found from its own home folder)."""
    kept = str(pipeline(slug).get("path") or "")
    head = kept.split("*", 1)[0].strip("/") if "*" in kept else "02_Video-Projects"
    return (in_checkout or checkout(slug) or repo_path(slug)) / head


def checkout(slug: str) -> pathlib.Path | None:
    """Where the channel is checked out on this machine, or None. A home channel's checkout is the studio's root."""
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
    """Where the channel's numbers are kept: the daily snapshots, the Studio reads, the first-day checks. While one
    channel's content lives in the studio's root, every channel's numbers are a folder each beside the board there.
    With no home channel each channel keeps its own, in its checkout (where that would be when it is not on this
    machine)."""
    own = get(slug)["slug"]
    return (ROOT if home() else checkout(own) or repo_path(own)) / "05_Analytics" / own


def uploads_file(slug: str) -> pathlib.Path | None:
    """The channel's register of uploads (video id, kind, publish time), or None when its checkout is not here."""
    base = checkout(slug)
    return base / "00_Brand" / "Channel-Setup" / "social" / "UPLOADS.json" if base else None


CHANNEL_RULES = "studio/RULES.md"


def rule_files(checkout) -> list[str]:
    """The rule files an agent reads in a channel's checkout, in order: the studio's AGENTS.md, then the channel's own
    studio/RULES.md when the checkout has one (J2527, 11 Nov 2026: the rule book is two files). A channel that has
    not split its rules yet, or a checkout that is not on this machine, is told only AGENTS.md."""
    return ["AGENTS.md"] + ([CHANNEL_RULES] if (pathlib.Path(checkout) / CHANNEL_RULES).is_file() else [])


def rules_phrase(checkout) -> str:
    """How a prompt names those files: "AGENTS.md", or "AGENTS.md and then studio/RULES.md"."""
    return " and then ".join(rule_files(checkout))


def studio_checkout(home_dir: pathlib.Path | None = None) -> pathlib.Path:
    """The checkout that carries the studio's own data (the board branch, the job queue). While a channel's content
    lives in the studio's root that is the home channel's repo. With none it is the studio's own: the registry's
    `studio.env` variable when set, else the first folder under ~/YouTube named in its `studio.checkouts` (else after
    its repo on GitHub) that exists, else the first name."""
    own = home()
    if own:
        return repo_path(own, home_dir)
    repo = studio_repo()
    if os.environ.get(repo["env"]):
        return pathlib.Path(os.environ[repo["env"]])
    cands = [(home_dir or pathlib.Path.home()) / "YouTube" / n for n in repo["checkouts"] or [STUDIO_KEY]]
    return next((c for c in cands if c.is_dir()), cands[0])


def studio_slug() -> str | None:
    """The channel whose repo carries the studio's own code and data (the scripts, the job queue), for code that
    must clone or pull that repo: the home channel, or None when the studio has a repo of its own and no channel's
    repo carries it."""
    return home()


@functools.lru_cache(maxsize=None)
def _section_of(path: str, stamp: int) -> dict:
    return json.loads(pathlib.Path(path).read_text()).get("studio") or {}


def _studio_section() -> dict:
    """The `studio` section of the registry: what is the studio's own and no channel's. {} when there is no registry.
    Read once for each version of the file: `default()` asks here for every job the board and the queue handle."""
    path = DIR / "channels.json"
    try:
        stamp = path.stat().st_mtime_ns
    except OSError:
        return {}
    return dict(_section_of(str(path), stamp))


STUDIO_KEY = "studio"


def studio_key() -> str:
    """The key the studio's own repo goes under where code keeps one thing per repo (a clone, a copy of its main
    branch): the home channel's slug while a channel's repo carries the studio, else "studio". Never a channel to
    ask the loader about: `studio_slug()` says whether there is one."""
    return home() or STUDIO_KEY


def studio_name() -> str:
    """What a brief calls the checkout that carries the studio: the home channel's name while there is one, else the
    registry's `studio.name` ("the studio" when it gives none)."""
    own = home()
    return name(own) if own else str(_studio_section().get("name") or "the studio")


def studio_short() -> str:
    """The short word a brief uses for the studio's own queue ("the OWB queue"): the home channel's label while
    there is one, else the registry's `studio.label` ("studio" when it gives none)."""
    own = home()
    return label(own) if own else str(_studio_section().get("label") or STUDIO_KEY)


def studio_repo() -> dict:
    """Where the studio's own repo is cloned from and found, shaped like a channel's `repo` block ({'url', 'env',
    'checkouts'}): the home channel's while there is one, else built from the registry's `studio` section."""
    own = home()
    if own:
        return dict(get(own)["repo"])
    kept = _studio_section()
    github = str(kept.get("github") or "")
    return {"url": f"https://github.com/{github}.git" if github else "", "env": str(kept.get("env") or ""),
            "checkouts": list(kept.get("checkouts") or ([github.rsplit("/", 1)[-1]] if github else []))}


def studio_github() -> str:
    """`owner/name` on GitHub of the repo that carries the studio's board and threads: the registry's `studio.github`
    (11 Nov 2026), so asking needs no channel to be "home". A registry without the field gives the home channel's
    repo, as before."""
    return str(_studio_section().get("github") or re.sub(r"^https://github\.com/|\.git$", "", get(home())["repo"]["url"]))


def home_label() -> str:
    """The label a record gets when it names no channel (the old `or "OWB"`): the default channel's."""
    return label(default())


@functools.lru_cache(maxsize=None)
def studio_prefix() -> str:
    """The studio's own short name, from the `studio` section of channels/channels.json. It is not a channel's: it
    prefixes what the studio installed on the machines under one name (launchd labels, state and log files, two
    environment variables). Engine code asks here instead of spelling it, so the studio can move to its own repo
    without a rename on any machine."""
    return str(_studio_section()["prefix"])


def studio_env(name: str) -> str:
    """The studio's own environment variable for `name`: studio_env("AGENT") is the variable the relay sets to say
    which agent it woke."""
    return f"{studio_prefix().upper()}_{name}"


def studio_label(name: str) -> str:
    """The launchd label of one of the studio's own background jobs: studio_label("chief-relay")."""
    return f"com.{studio_prefix()}.{name}"


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
