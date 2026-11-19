#!/usr/bin/env python3
"""Isolated Git records for the detached analytics timer (not yet installed).

No API calls, checkout resets, force pushes, or shared-checkout commits. Each
instance owns one detached worktree and a fixed set of analytics record paths.
The timer must serialize its use and supply registry-validated source checkouts.
"""
from __future__ import annotations

import pathlib
import subprocess

from engine_guard import refusal


class RecordError(RuntimeError):
    pass


def scopes(channel: str) -> tuple[str, ...]:
    if channel == 'studio':
        return ('05_Analytics/dashboard',)
    if channel not in ('owb', 'hos', 'ww2'):
        raise RecordError('Unknown analytics record owner')
    paths = (f'05_Analytics/{channel}',)
    if channel == 'owb':
        paths += ('00_Brand/Channel-Setup/audits/shorts_open_library/library.json',)
    return paths


class Records:
    def __init__(self, source: pathlib.Path, worktree: pathlib.Path, channel: str):
        self.source = source.resolve()
        self.worktree = worktree.resolve()
        self.paths = scopes(channel)
        if self.source == self.worktree or self.source in self.worktree.parents:
            raise RecordError('Analytics requires a separate worktree outside the source checkout')

    @staticmethod
    def git(repo: pathlib.Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        try:
            result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True,
                                    text=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RecordError('Analytics Git operation unavailable or timed out') from exc
        if check and result.returncode:
            # Do not expose credential-bearing remote URLs from Git diagnostics.
            raise RecordError(f'Analytics Git {args[0]} failed (exit {result.returncode})')
        return result

    def allowed(self, name: str) -> bool:
        return any(name == p or name.startswith(p + '/') for p in self.paths)

    def verify(self) -> None:
        if refusal():
            raise RecordError("Analytics code belongs to a retired or unverifiable engine")
        actual = self.git(self.worktree, 'rev-parse', '--show-toplevel').stdout.strip()
        if pathlib.Path(actual).resolve() != self.worktree:
            raise RecordError('Record destination is not a worktree root')
        for repo in (self.source, self.worktree):
            common = pathlib.Path(self.git(repo, 'rev-parse', '--git-common-dir').stdout.strip())
            common = (repo / common).resolve()
            if repo == self.source:
                source_common = common
            elif common != source_common:
                raise RecordError('Analytics worktree belongs to another repository')
        if self.git(self.worktree, 'symbolic-ref', '-q', 'HEAD', check=False).returncode == 0:
            raise RecordError('Analytics worktree must be detached')
        for name in ('rebase-merge', 'rebase-apply', 'MERGE_HEAD', 'CHERRY_PICK_HEAD'):
            path = self.git(self.worktree, 'rev-parse', '--git-path', name).stdout.strip()
            if (self.worktree / path).exists():
                raise RecordError('Unfinished Git operation requires inspection')
        for scope in self.paths:
            path = self.worktree / scope
            for part in (path, *path.parents):
                if part == self.worktree:
                    break
                if part.is_symlink():
                    raise RecordError('Analytics record scope cannot traverse a symlink')

    def check_changes(self) -> None:
        changed = set()
        for args in (('diff', '--no-renames', '--name-only', '-z'), ('diff', '--cached', '--no-renames', '--name-only', '-z'),
                     ('ls-files', '--others', '--exclude-standard', '-z')):
            changed.update(self.git(self.worktree, *args).stdout.split('\0'))
        if any(name and not self.allowed(name) for name in changed):
            raise RecordError('Unrelated changes in analytics worktree; nothing staged')

    def check_commits(self) -> None:
        # Inspect every pending commit, not only its net diff (add-then-delete is
        # still foreign history and must never hitch a ride on a tracker push).
        commits = self.git(self.worktree, 'rev-list', 'origin/main..HEAD').stdout.split()
        for commit in commits:
            if len(self.git(self.worktree, 'rev-list', '--parents', '-n', '1', commit).stdout.split()) != 2:
                raise RecordError('Unexpected root or merge in analytics pending history')
            names = self.git(self.worktree, 'diff-tree', '--no-renames', '--no-commit-id', '--name-only',
                             '-r', '-z', commit).stdout.split('\0')
            if any(name and not self.allowed(name) for name in names):
                raise RecordError('Unrelated pending commit in analytics worktree')

    def save(self, message: str) -> None:
        self.verify()
        self.check_changes()
        self.check_commits()
        # Literal, fixed ownership scopes. A missing optional path is harmless.
        for scope in self.paths:
            tracked = self.git(self.worktree, 'ls-files', '--', f':(literal){scope}').stdout
            if tracked or (self.worktree / scope).exists():
                self.git(self.worktree, 'add', '-A', '--', f':(literal){scope}')
        if self.git(self.worktree, 'diff', '--cached', '--quiet', check=False).returncode:
            self.git(self.worktree, 'commit', '-q', '-m', message)

    def catch_up(self) -> None:
        self.git(self.worktree, 'fetch', '-q', 'origin', 'main')
        self.check_commits()
        if self.git(self.worktree, 'rebase', '-q', 'origin/main', check=False).returncode:
            self.git(self.worktree, 'rebase', '--abort')
            raise RecordError('Analytics rebase conflicted; local record commit preserved')

    def prepare(self) -> None:
        if refusal():
            raise RecordError("Analytics code belongs to a retired or unverifiable engine")
        if not self.worktree.exists():
            self.git(self.source, 'fetch', '-q', 'origin', 'main')
            self.worktree.parent.mkdir(parents=True, exist_ok=True)
            self.git(self.source, 'worktree', 'add', '-q', '--detach', str(self.worktree), 'origin/main')
        self.save('Channel tracker: records recovered from earlier run')
        self.catch_up()
        self.verify()

    def publish(self, message: str, attempts: int = 3) -> None:
        if not 1 <= attempts <= 3:
            raise RecordError('Analytics push attempts must be between one and three')
        self.save(message)
        # Retry even when there are no new working-tree changes: the previous
        # run may have committed successfully but failed to push.
        for _ in range(attempts):
            self.verify()
            self.catch_up()
            if self.git(self.worktree, 'push', '-q', 'origin', 'HEAD:main', check=False).returncode == 0:
                return
        raise RecordError('Analytics push failed; local record commits retained for retry')
