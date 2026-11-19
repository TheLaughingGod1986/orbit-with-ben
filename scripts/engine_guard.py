"""Refuse retired engine entry points after an explicitly armed repository cutover.

The local marker is absent until the drained cutover window. It contains only
{"version": 1, "github": "owner/repository"}; no paths or credentials. Install it
on each worker machine, after updating all retained engine copies with this guard.
It is not a lock: existing writers must still be drained before changing it.
"""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent


def refusal(root=None, marker=None):
    root = pathlib.Path(root) if root is not None else ROOT
    marker = pathlib.Path(marker) if marker is not None else pathlib.Path.home() / '_desk/state/active-studio.json'
    try:
        body = marker.read_text()
    except FileNotFoundError:
        return None  # no cutover has been armed
    except OSError:
        return 'Cannot read the active studio marker; no engine work started.'
    try:
        active = json.loads(body)
        expected = active['github']
        if active.get('version') != 1 or not isinstance(expected, str) or not re.fullmatch(
                r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', expected):
            raise ValueError('invalid marker')
        local = json.loads((root / 'channels/channels.json').read_text())['studio']['github']
        if not isinstance(local, str):
            raise ValueError('invalid registry')
    except (OSError, ValueError, KeyError, TypeError):
        return 'Invalid active studio marker or engine registry; no engine work started.'
    if local != expected:
        return 'This engine repository is retired; run the active studio checkout. No engine work started.'
    return None


def require_active(root=None, marker=None):
    why = refusal(root, marker)
    if why:
        # No untrusted marker contents or local paths are printed.
        raise SystemExit(why)
