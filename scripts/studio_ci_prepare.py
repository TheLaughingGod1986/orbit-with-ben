#!/usr/bin/env python3
"""Render cutover CI files into a new staging directory; never install or run them.

The channel commit must be a full SHA. Apply the output only to an isolated
studio export, inspect its diff, and run the resulting checks before cutover.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKFLOWS = ('rules-check.yml', 'core-check.yml', 'notes-check.yml', 'content-ops.yml')


def once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('workflow template changed; expected exactly one adaptation target')
    return text.replace(old, new, 1)


def render(root, channel_sha, studio_repo):
    if not re.fullmatch(r'[0-9a-f]{40}', channel_sha):
        raise ValueError('channel commit must be a full lowercase SHA')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', studio_repo):
        raise ValueError('studio repo must be owner/name')
    registry = json.loads((root / 'channels/channels.json').read_text())
    slug = registry['studio']['default_channel']
    entry = next(e for e in registry['channels'] if e['slug'] == slug)
    manifest = root / ('studio/channel.json' if entry.get('home') else f'channels/{slug}/channel.json')
    channel = json.loads(manifest.read_text())['repo']
    url = channel['url']
    match = re.fullmatch(r'https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\.git', url)
    if not match:
        raise ValueError('channel must have a GitHub HTTPS repository URL')
    repo, env = match.group(1), channel['env']
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('invalid channel repository')
    if not re.fullmatch(r'[A-Z][A-Z0-9_]*', env):
        raise ValueError('invalid channel environment name')
    files = {}
    for name in WORKFLOWS:
        text = (root / '.github/workflows' / name).read_text()
        if name in ('rules-check.yml', 'notes-check.yml', 'content-ops.yml'):
            text = once(text, '\njobs:\n', '\nenv:\n  ' + env + ': ${{ github.workspace }}/.ci-channels/default\n\njobs:\n')
            checkout = ('      - name: Read pinned default-channel rules and records\n'
                        '        uses: actions/checkout@v4\n'
                        '        with:\n'
                        f'          repository: {repo}\n'
                        f'          ref: {channel_sha}\n'
                        '          path: .ci-channels/default\n'
                        '          persist-credentials: false\n')
            anchor = '      - uses: actions/setup-node@v4\n' if name == 'content-ops.yml' else '      - uses: actions/setup-python@v5\n'
            text = once(text, anchor, checkout + anchor)
        if name == 'rules-check.yml':
            text = once(text, '      - if: steps.scope.outputs.rules == \'true\'\n        run: python3 scripts/studio.py status --check\n',
                        '      # No resident channel: STATUS.md is generated, not tracked.\n')
        if name == 'core-check.yml':
            old_repo = registry['studio']['github']
            text = once(text, "github.repository == '" + old_repo + "'", "github.repository == '" + studio_repo + "'")
        files['.github/workflows/' + name] = text.encode()
    # The core workflow is hash-locked. Only refresh that exact staged member;
    # preserve every other member/hash and leave both live channel locks alone.
    lock = json.loads((root / 'studio-core/CORE_FILES.json').read_text())
    for path, body in files.items():
        if path in lock['files']:
            lock['files'][path] = hashlib.sha256(body).hexdigest()
    files['studio-core/CORE_FILES.json'] = (json.dumps(lock, indent=2, sort_keys=True) + '\n').encode()
    return files


def prepare(root, out, channel_sha, studio_repo):
    files = render(root, channel_sha, studio_repo)  # validate everything before writing
    out.mkdir(parents=True, exist_ok=False)
    for rel, body in files.items():
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
    return len(files)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--channel-sha', required=True)
    ap.add_argument('--studio-repo', required=True)
    ap.add_argument('--out', type=pathlib.Path, required=True)
    a = ap.parse_args()
    try:
        n = prepare(ROOT, a.out, a.channel_sha, a.studio_repo)
    except (ValueError, OSError, KeyError, StopIteration) as exc:
        ap.exit(1, f'Not prepared: {exc}\n')
    print(f'Prepared {n} files; no workflows installed or executed.')


if __name__ == '__main__':
    main()
