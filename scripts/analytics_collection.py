"""Collect detached analytics inside the serialized record session.

Preparation API only: the timer must supply its required gate/dispatch phase.
No installed entrypoint and no implicit omission of that phase.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import signal
import subprocess
import sys
from typing import Callable

import channels
from analytics_session import Session, locked_session
from analytics_worktree import RecordError


@dataclass(frozen=True)
class Command:
    name: str
    args: tuple[str, ...]
    cwd: Path
    env: dict[str, str]
    timeout: int


def execute(command: Command) -> int:
    """Bound a whole subprocess group, including children spawned by Node.

    Do not log command output: API errors can contain credentials. The caller
    records only the named step and its exit status; persisted analytics are
    the result, not a copy of a child's environment or API diagnostics.
    """
    try:
        process = subprocess.Popen(command.args, cwd=command.cwd, env=command.env,
                                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL, start_new_session=True)
    except OSError:
        return 127
    try:
        return process.wait(timeout=command.timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        return 124


def credential_environment(base: dict[str, str]) -> dict[str, str]:
    # Node --env-file does not replace inherited variables. Only the selected
    # local file may supply the analytics OAuth identity for this run.
    return {k: v for k, v in base.items() if k not in {
        'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'YOUTUBE_REFRESH_TOKEN'
    } and not k.startswith(('YT_ANALYTICS_REFRESH_TOKEN_', 'YT_CHANNEL_ID_'))}


def collect(session: Session, credential_file: Path,
            after_snapshots: Callable[[Session, dict[str, str]], list[str]],
            run: Callable[[Command], int] = execute, *, board: bool = True) -> list[str]:
    """Run collectors, required auxiliary phase, reports and scoped publication.

    Call only inside locked_session. Nonzero collectors do not suppress other
    channels or publication of successful records. The auxiliary phase must
    return named failures (and itself bound any external commands).
    """
    if not callable(after_snapshots):
        raise RecordError('Analytics requires a gate and dispatch phase')
    if not credential_file.is_absolute() or not credential_file.is_file():
        raise RecordError('Analytics requires an existing absolute local credential file')
    # Credentials must remain outside every generated record worktree.
    credential_file = credential_file.resolve()
    if any(credential_file == r.worktree or r.worktree in credential_file.parents
           for r in session.records.values()):
        raise RecordError('Analytics credentials cannot live in record worktrees')
    source = session.sources['studio']
    engine = session.records['studio'].worktree
    ops = engine / '07_Content-Ops'
    runner = source / '07_Content-Ops/node_modules/tsx/dist/cli.mjs'
    if not runner.is_file():
        raise RecordError('Install existing Content Ops dependencies before analytics cutover')
    # Worktree-local module resolution; the target is installed code, not data.
    modules = ops / 'node_modules'
    expected = source / '07_Content-Ops/node_modules'
    if modules.exists() or modules.is_symlink():
        if not modules.is_symlink() or modules.resolve() != expected.resolve():
            raise RecordError('Analytics worktree has an unexpected dependency directory')
    else:
        modules.symlink_to(expected, target_is_directory=True)
    env = credential_environment(session.environment())
    failed: list[str] = []

    def call(name: str, script: str, args: tuple[str, ...] = (), timeout: int = 600) -> None:
        command = Command(name, ('node', f'--env-file={credential_file}', str(runner),
                                str(ops / 'scripts' / script), *args), ops, env.copy(), timeout)
        if run(command):
            failed.append(name)

    for slug in session.records:
        if slug != 'studio':
            call(f'snapshot:{slug}', 'analytics-snapshot.ts', ('--channel', slug))
    failed.extend(after_snapshots(session, env.copy()))
    call('report', 'analytics-report.ts')
    failed.extend(f'publish:{owner}' for owner in session.publish('Channel tracker: daily analytics records'))
    if board:
        # Publisher builds from remote records, not these analytics worktrees.
        # Revert checkout overrides to real source repositories for this call.
        publisher_env = credential_environment(dict(os.environ))
        for slug, path in session.sources.items():
            meta = channels.studio_repo() if slug == 'studio' else channels.get(slug)['repo']
            publisher_env[meta['env']] = str(path)
        if run(Command('board', (sys.executable, str(source / 'scripts/board_publish.py'), '--quiet'),
                       source, publisher_env, 300)):
            failed.append('board')
    return failed


def collection_session(directory: Path, credential_file: Path,
                       after_snapshots: Callable[[Session, dict[str, str]], list[str]],
                       run: Callable[[Command], int] = execute, *, board: bool = True,
                       lock: Path | None = None) -> list[str]:
    """Keep the same lock through collection, pending-push retry and board work."""
    with locked_session(directory, lock) as session:
        return collect(session, credential_file, after_snapshots, run, board=board)
