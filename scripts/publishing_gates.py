#!/usr/bin/env python3
"""Shared, fail-closed preflight for uploads and scheduled-video rechecks.

Inputs live in <export>_meta.json under publishing_gates (see docs/PUBLISHING_GATES.md).
Gate results are recomputed, never trusted from recorded PASS strings.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zoneinfo import ZoneInfo
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent


def run(command):
    try:
        p = subprocess.run(command, capture_output=True, text=True, timeout=600)
        return p.returncode, (p.stdout + p.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 2, f'gate unavailable: {type(exc).__name__}'


def evaluate(video: Path, repo: Path, fmt: str, air: str, *, video_id='', length_test=False,
             meta_path: Path | None = None, short_run=run) -> dict:
    """Run every applicable blocking check; unavailable evidence is a blocking finding too."""
    results = []
    video, repo = video.absolute(), repo.absolute()
    meta_path = meta_path or video.with_name(video.stem + '_meta.json')
    try:
        meta = json.loads(meta_path.read_text())
        inputs = meta.get('publishing_gates') or {}
        if not isinstance(inputs, dict):
            raise ValueError('publishing_gates must be an object')
    except (OSError, ValueError) as exc:
        return dict(ok=False, checks=[dict(gate='inputs', ok=False, output=f'Missing/invalid export metadata: {exc}')])

    try:
        digest = hashlib.sha256(video.read_bytes()).hexdigest()
        if meta.get('sha256') != digest:
            raise ValueError('export sha256 missing or does not match metadata')
    except (OSError, ValueError) as exc:
        results.append(dict(gate='identity', ok=False, output=str(exc)))

    def resolve(key):
        value = inputs.get(key)
        if not isinstance(value, str) or not value:
            raise ValueError(f'publishing_gates.{key} is required')
        p = Path(value).expanduser()
        return p if p.is_absolute() else (meta_path.parent / p).resolve()

    def record(name, command, runner=run):
        code, output = runner(command)
        # The gate itself applies its own narrow waiver format. Tool errors never pass.
        results.append(dict(gate=name, ok=code == 0, exit_code=code, output=output))

    if fmt == 'short':
        command = [sys.executable, str(repo / '00_Brand/Channel-Setup/tools/gate_shorts_open.py'),
                   'check', str(video), '--air-date', air, '--meta', str(meta_path)]
        if video_id:
            command += ['--id', video_id]
        if length_test:
            command += ['--length-test']
        record('shorts_open', command, short_run)
        # Preserve the exact-finding, named-Chief sidecar waiver format used by gate_upcoming.
        last = results[-1]
        if last['exit_code'] == 1:
            fails = [line.strip()[5:].strip() for line in last['output'].splitlines()
                     if line.startswith(' ') and line.strip().startswith('FAIL ')]
            try:
                data = json.loads(video.with_name(video.stem + '_gate.json').read_text())
                records = data if isinstance(data, list) else [data]
                book = {w.get('fail'): w for r in records for w in r.get('waivers', [])
                        if str(w.get('waived_by', '')).lower().startswith(('chief', '[chief]'))}
                if fails and all(f in book for f in fails):
                    last.update(ok=True, waived=[book[f] for f in fails])
            except (OSError, ValueError, TypeError, AttributeError):
                pass
    # Picture QA contains polish_gate, including the near-black and jitter checks.
    required = ['music', 'picture', 'sfx']
    try:
        config = json.loads((repo / 'studio/channel.json').read_text())
        extra = config.get('publishing_gates', {}).get('required', [])
        if not isinstance(extra, list):
            raise ValueError('channel required gates must be a list')
        required += [g for g in extra if g not in required]
    except (OSError, ValueError, AttributeError) as exc:
        results.append(dict(gate='channel', ok=False, output=str(exc)))
    with tempfile.TemporaryDirectory(prefix='publishing-gates-') as tmp:
        for name in required:
            try:
                if name == 'music':
                    command = [sys.executable, str(ROOT / 'scripts/music_gate.py'), str(resolve('film')),
                               '--bed', str(resolve('bed')), '--video', str(video)]
                elif name == 'picture':
                    command = [sys.executable, str(ROOT / 'scripts/picture_qa.py'), str(video),
                               '--cuts', str(resolve('cuts')), '--out-dir', tmp]
                    for key, flag in [('pool', '--pool'), ('reviewed_ok', '--reviewed-ok'), ('terminal_loop', '--terminal-loop')]:
                        if inputs.get(key):
                            command += [flag, str(resolve(key))]
                elif name == 'sfx':
                    command = [sys.executable, str(ROOT / 'scripts/sfx_kit.py'), 'level',
                               '--vo', str(resolve('vo')), '--sfx', str(resolve('sfx')), '--bed', str(resolve('bed'))]
                else:
                    raise ValueError(f'Unknown required gate {name!r}; add its runner before shipping')
                record(name, command)
            except (OSError, ValueError) as exc:
                results.append(dict(gate=name, ok=False, output=str(exc)))
    return dict(ok=all(c['ok'] for c in results), checks=results)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--video', type=Path, required=True)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--format', choices=['short', 'long'], required=True)
    p.add_argument('--air-date', default=datetime.now(ZoneInfo('Europe/London')).date().isoformat())
    p.add_argument('--id', default='')
    p.add_argument('--length-test', action='store_true')
    a = p.parse_args(argv)
    result = evaluate(a.video, a.repo, a.format, a.air_date, video_id=a.id, length_test=a.length_test)
    print(json.dumps(result, indent=2))
    return 0 if result['ok'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
