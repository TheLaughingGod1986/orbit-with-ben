"""Locked, registry-validated record session for the pending detached timer.

Not an entrypoint: collection/gate orchestration must use this context before
it can be installed. Credentials and media stay in source checkouts; record
checkout overrides are passed only to child processes, never to this loader.
"""
from __future__ import annotations

from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import re

import channels
from analytics_worktree import Records, RecordError
from engine_guard import refusal


def repository_id(url: str) -> str:
    # Accept the two ordinary credential-free GitHub remote forms only.
    match = re.fullmatch(r'(?:https://github\.com/|git@github\.com:)([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?', url)
    if not match:
        raise RecordError('Analytics requires a credential-free GitHub repository identity')
    return match[1].lower()


def verify_source(path: Path, expected: str) -> None:
    if not path.is_dir():
        raise RecordError('Analytics source checkout missing')
    top = Records.git(path, 'rev-parse', '--show-toplevel').stdout.strip()
    if Path(top).resolve() != path.resolve():
        raise RecordError('Analytics source must be a repository root')
    actual = Records.git(path, 'remote', 'get-url', 'origin').stdout.strip()
    if repository_id(actual) != repository_id(expected):
        raise RecordError('Analytics source repository does not match registry')


def validate_channel(path: Path, slug: str) -> None:
    try:
        identity = json.loads((path / 'studio/channel.json').read_text())['slug']
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise RecordError('Analytics channel manifest unavailable') from exc
    if identity != slug:
        raise RecordError('Analytics channel manifest identity mismatch')
    history = path / '05_Analytics' / slug / 'snapshots'
    if not history.is_dir() or not any(history.glob('*.json')):
        raise RecordError('Stage existing channel snapshot history before cutover')
    # Scope roots must not lead outside the record repository.
    for folder in (history, history.parent, history.parent.parent):
        if folder.is_symlink():
            raise RecordError('Analytics history cannot traverse a symlink')


class Session:
    def __init__(self, directory: Path):
        self.directory = directory.resolve()
        self.sources: dict[str, Path] = {}
        self.records: dict[str, Records] = {}
        self.overrides: dict[str, str] = {}

    def preflight(self) -> None:
        if refusal() or channels.studio_slug():
            raise RecordError('Analytics session requires an active detached engine')
        engine = channels.ROOT.resolve()
        queue = channels.studio_checkout().resolve()
        verify_source(engine, channels.studio_repo()['url'])
        verify_source(queue, channels.studio_repo()['url'])
        if refusal(queue) or not (queue / 'jobs/queue.json').is_file():
            raise RecordError('Active shared studio queue unavailable')
        try:
            identity = json.loads((queue / 'channels/channels.json').read_text())['studio']['github']
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise RecordError('Shared queue registry unavailable') from exc
        if identity != channels.studio_github():
            raise RecordError('Shared queue engine identity mismatch')
        self.sources = {'studio': engine}
        self.overrides = {'FIELD_ORDER_QUEUE_REPO': str(queue)}
        used_env = {'FIELD_ORDER_QUEUE_REPO', channels.studio_repo().get('env')}
        for slug in channels.slugs():
            source = channels.checkout(slug)
            if source is None:
                raise RecordError('Analytics channel checkout unavailable')
            source = source.resolve()
            meta = channels.get(slug)['repo']
            name = meta.get('env', '')
            if not re.fullmatch(r'[A-Z][A-Z0-9_]*', name) or name in used_env:
                raise RecordError('Analytics channel needs a unique checkout environment variable')
            used_env.add(name)
            verify_source(source, meta['url'])
            validate_channel(source, slug)
            self.sources[slug] = source
            self.overrides[name] = str(self.directory / slug)
        roots = list(self.sources.values())
        if len(set(roots)) != len(roots) or any(
                a in b.parents or b in a.parents for i, a in enumerate(roots) for b in roots[i + 1:]):
            raise RecordError('Analytics source repositories must be separate')
        if any(self.directory == p or p in self.directory.parents or self.directory in p.parents for p in roots + [queue]):
            raise RecordError('Analytics scratch must be outside source and queue checkouts')
        # Construct all owners before any worktree mutation; unsupported owners fail closed.
        self.records = {slug: Records(source, self.directory / slug, slug)
                        for slug, source in self.sources.items()}

    def prepare(self) -> None:
        self.preflight()
        for slug, record in self.records.items():
            record.prepare()
            if slug != 'studio':
                # A source may be ahead of origin/main; validate the actual detached records too.
                validate_channel(record.worktree, slug)

    def environment(self, base: dict[str, str] | None = None) -> dict[str, str]:
        return dict(os.environ if base is None else base, **self.overrides)

    def publish(self, message: str) -> list[str]:
        failed = []
        for slug, record in self.records.items():
            try:
                record.publish(message)
            except RecordError:
                # One failed remote must not discard another channel's completed records.
                failed.append(slug)
        return failed


@contextmanager
def locked_session(directory: Path, lock: Path | None = None):
    # The fixed default is independent of selected scratch: concurrent timers
    # cannot evade serialization by choosing different record worktrees.
    lock = lock or Path.home() / '_desk/locks/analytics-records.lock'
    lock.parent.mkdir(parents=True, exist_ok=True)
    with lock.open('a') as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RecordError('Analytics record session already running') from exc
        try:
            session = Session(directory)
            session.prepare()
            yield session
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)
