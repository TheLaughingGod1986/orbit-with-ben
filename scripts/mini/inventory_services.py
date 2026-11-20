#!/usr/bin/env python3
"""Read installed launchd definitions without running commands or disclosing their values.

This is an inventory, not proof that a service is safe. Guard/pause mentions may be
comments or dead code. Keep the raw report local; review selected rows for the runbook.
"""
import argparse
import hashlib
import json
import pathlib
import plistlib
import re
import shlex
from xml.parsers.expat import ExpatError

MAX_BYTES = 2_000_000


def read_small(path):
    with path.open('rb') as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError('input too large')
    return data


def expand_home(value, home):
    for prefix in ('${HOME}/', '$HOME/', '~/'):
        if value.startswith(prefix):
            return str(home / value[len(prefix):])
    return value


def inspect_service(path, old_engine, home):
    # Do not print exception strings, paths, argv, environment names/values or source.
    row = {'source_sha256': None, 'status': 'unreadable', 'needs_review': True}
    if re.fullmatch(r'[A-Za-z0-9_.-]{1,160}', path.name):
        row['source_name'] = path.name
    try:
        raw = read_small(path)
        row['source_sha256'] = hashlib.sha256(raw).hexdigest()
        doc = plistlib.loads(raw)
        label = doc.get('Label')
        if not isinstance(label, str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,160}', label):
            row['status'] = 'invalid_label'
            return row
        row['label'] = label
        args = doc.get('ProgramArguments', [])
        if not isinstance(args, list) or not all(isinstance(a, str) for a in args):
            row['status'] = 'invalid_arguments'
            return row
        row['status'] = 'read'
        row['old_engine_reference'] = str(old_engine) in raw.decode('utf-8', errors='ignore')
        # Binary plist strings must also be checked, without exposing any value.
        def strings(value):
            if isinstance(value, str):
                yield value
            elif isinstance(value, dict):
                for item in value.values():
                    yield from strings(item)
            elif isinstance(value, list):
                for item in value:
                    yield from strings(item)
        row['old_engine_reference'] |= any(str(old_engine) in expand_home(s, home) for s in strings(doc))
        tokens = list(args)
        if args and pathlib.Path(args[0]).name in ('sh', 'bash', 'zsh') and len(args) >= 3 and args[1] in ('-c', '-lc'):
            try:
                tokens = shlex.split(args[2])
            except ValueError:
                tokens = []
        program = doc.get('Program')
        if isinstance(program, str):
            tokens.insert(0, program)
        # Read only explicitly named script files or a direct executable wrapper.
        # No variable evaluation, command substitution, PATH search or shell execution.
        candidates = []
        for index, token in enumerate(tokens):
            expanded = expand_home(token, home)
            if '$' in expanded or '`' in expanded or not pathlib.Path(expanded).is_absolute():
                continue
            p = pathlib.Path(expanded)
            if p.suffix in ('.py', '.sh') or index == 0:
                candidates.append(p)
        inspected = []
        for candidate in dict.fromkeys(candidates):
            try:
                data = read_small(candidate)
                if b'\0' in data or not (data.startswith(b'#!') or candidate.suffix in ('.py', '.sh')):
                    continue
                source = data.decode('utf-8')
            except (OSError, ValueError, UnicodeError):
                continue
            inspected.append({
                'sha256': hashlib.sha256(data).hexdigest(),
                'old_engine_reference': str(old_engine) in source or str(old_engine).replace(str(home), '$HOME') in source,
                'guard_mentioned': 'engine_guard' in source,
                'pause_mentioned': '.pause' in source,
            })
        row['scripts'] = inspected
        row['command_resolved'] = bool(inspected)
        row['old_engine_reference'] |= any(s['old_engine_reference'] for s in inspected)
    except (OSError, ValueError, TypeError, AttributeError, plistlib.InvalidFileException, ExpatError):
        pass
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--directory', type=pathlib.Path, default=pathlib.Path.home() / 'Library/LaunchAgents')
    ap.add_argument('--old-engine', type=pathlib.Path, required=True)
    ap.add_argument('--prefix', action='append', required=True, help='installed plist filename prefix; repeat as needed')
    args = ap.parse_args()
    if not args.old_engine.is_absolute() or not args.directory.is_dir():
        ap.error('existing service directory and absolute old engine path required')
    paths = sorted(p for p in args.directory.glob('*.plist') if any(p.name.startswith(s) for s in args.prefix))
    rows = [inspect_service(p, args.old_engine, pathlib.Path.home()) for p in paths]
    print(json.dumps({'inventory_only': True, 'services': rows}, indent=2))
    return 0 if rows and all(r['status'] == 'read' for r in rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
