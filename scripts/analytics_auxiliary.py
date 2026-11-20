"""Bounded gate/dispatch phase for the detached analytics collection session."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import sys
from typing import Callable
from zoneinfo import ZoneInfo

import channels
from analytics_collection import Command, execute
from analytics_session import Session
from analytics_worktree import RecordError


def auxiliary(credential_file: Path, cache: Path, dispatch_script: str,
              run: Callable[[Command], int] = execute, *, gate_timeout: int = 600,
              day: str | None = None):
    """Build collect's required callback; the timer supplies its dispatch script.

    Frames are disposable local files in the persistent record worktree. The
    library JSON contains the hashes and thumbnail arrays used for comparison;
    it is the durable Git record. Existing source frames are never moved.
    """
    if (not credential_file.is_absolute() or not cache.is_absolute()
            or not re.fullmatch(r'[a-z][a-z0-9-]*\.ts', dispatch_script)
            or not 1 <= gate_timeout <= 1800):
        raise RecordError('Invalid analytics auxiliary configuration')
    selected_day = day or datetime.now(ZoneInfo('Europe/London')).date().isoformat()
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', selected_day):
        raise RecordError('Invalid analytics gate date')

    def phase(session: Session, env: dict[str, str]) -> list[str]:
        failed = []
        engine = session.records['studio'].worktree
        source = session.sources['studio']
        ops = engine / '07_Content-Ops'
        runner = source / '07_Content-Ops/node_modules/tsx/dist/cli.mjs'
        # Queue writes use the separately verified shared queue from the session,
        # never the detached channel/engine records or the media checkout.
        dispatch = Command('dispatch', ('node', f'--env-file={credential_file}', str(runner),
            str(ops / 'scripts' / dispatch_script)), ops, env.copy(), 180)
        if run(dispatch):
            failed.append('dispatch')
        for slug, record in session.records.items():
            if slug == 'studio' or not channels.get(slug).get('analytics', {}).get('open_gate_library'):
                continue
            data = record.worktree / '05_Analytics' / slug
            snapshot = data / 'snapshots' / (selected_day + '.json')
            uploads = record.worktree / '00_Brand/Channel-Setup/social/UPLOADS.json'
            if not snapshot.is_file() or not uploads.is_file():
                failed.append(f'gate-input:{slug}')
                continue
            args = (sys.executable, str(engine / 'scripts/analytics_gate.py'),
                '--engine', str(engine), '--record', str(record.worktree),
                '--media', str(session.sources[slug]), '--channel', slug, '--',
                '--snapshot', str(snapshot), '--uploads', str(uploads),
                '--media-root', str(session.sources[slug]),
                '--out', str(data / 'UPCOMING_SHORTS_GATE.md'), '--add', '--cache', str(cache))
            if run(Command(f'gate:{slug}', args, engine, env.copy(), gate_timeout)):
                failed.append(f'gate:{slug}')
        return failed
    return phase
