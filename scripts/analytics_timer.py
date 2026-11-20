#!/usr/bin/env python3
"""Detached-engine analytics timer; installed only after migration acceptance.

The parent bounds the entire run, including filesystem probes and Git work.
Only named status is logged; child diagnostics and credential values stay private.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

import channels
from analytics_auxiliary import auxiliary
from analytics_collection import Command, collection_session, execute
from analytics_worktree import RecordError
from engine_guard import refusal


PROBE = '''import pathlib,sys,tempfile
p = pathlib.Path(sys.argv[1])
p.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryFile(dir=p) as f:
    f.write(b'probe'); f.flush(); f.seek(0)
    assert f.read() == b'probe'
'''


def pick_cache(preferred: Path, fallback: Path, run=execute) -> Path:
    for path in (preferred, fallback):
        if not path.is_absolute():
            raise RecordError('Analytics cache must be absolute')
    for path in dict.fromkeys((preferred, fallback)):
        command = Command('cache-probe', (sys.executable, '-c', PROBE, str(path)),
                          Path('/'), dict(os.environ), 5)
        if run(command) == 0:
            return path
    raise RecordError('Analytics cache and internal fallback are unavailable')


def worker(args) -> int:
    if refusal() or channels.studio_slug():
        raise RecordError('Timer requires an active detached engine')
    if not args.records.is_absolute() or not args.credentials.is_absolute():
        raise RecordError('Analytics records and credential file must be absolute')
    # No record fallback: an inaccessible worktree may hold unpushed commits.
    # Cache alone is disposable and may use the internal-disk fallback.
    cache = pick_cache(args.cache, args.safe_cache)
    phase = auxiliary(args.credentials, cache, 'field-order-dispatch.ts',
                      gate_timeout=args.gate_timeout)
    failed = collection_session(args.records, args.credentials, phase, board=not args.no_board)
    return 1 if failed else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--records', type=Path, required=True)
    ap.add_argument('--credentials', type=Path, required=True)
    ap.add_argument('--cache', type=Path, required=True)
    ap.add_argument('--safe-cache', type=Path, required=True)
    ap.add_argument('--gate-timeout', type=int, default=600)
    ap.add_argument('--no-board', action='store_true')
    ap.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    arguments = list(sys.argv[1:] if argv is None else argv)
    args = ap.parse_args(arguments)
    if not 1 <= args.gate_timeout <= 1800:
        ap.error('gate timeout must be between 1 and 1800 seconds')
    if args.worker:
        try:
            return worker(args)
        except Exception:
            # Library or API exceptions can contain sensitive diagnostics.
            return 1
    code = execute(Command('analytics-timer', (sys.executable, str(Path(__file__).absolute()),
                           *arguments, '--worker'), Path('/'), dict(os.environ), 2700))
    print('Analytics timer complete' if code == 0 else
          'Analytics timer failed or timed out; inspect records before retrying')
    return code


if __name__ == '__main__':
    raise SystemExit(main())
