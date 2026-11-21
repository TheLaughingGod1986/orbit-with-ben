"""Run the existing Shorts gate with isolated channel records and source media.

This adapter leaves the shared gate code unchanged. Each subprocess loads the
channel's own profile, while the library and frame writes stay in its detached
record worktree. It is preparation for the detached timer, not installed yet.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys

from analytics_worktree import RecordError
from engine_guard import refusal

LIBRARY = Path('00_Brand/Channel-Setup/audits/shorts_open_library')
TOOLS = Path('00_Brand/Channel-Setup/tools')


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RecordError('Gate module unavailable')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(record: Path, media: Path, slug: str) -> None:
    if (not record.is_absolute() or not media.is_absolute() or record.resolve() == media.resolve()
            or record.resolve() in media.resolve().parents or media.resolve() in record.resolve().parents):
        raise RecordError('Gate requires separate absolute record and media roots')
    for root in (record, media):
        try:
            config = json.loads((root / 'studio/channel.json').read_text())
        except (OSError, ValueError) as exc:
            raise RecordError('Gate channel manifest unavailable') from exc
        if config.get('slug') != slug or config.get('analytics', {}).get('open_gate_library') is not True:
            raise RecordError('Gate record and media channel identity must match library owner')
    for path in (record / LIBRARY / 'library.json', record / LIBRARY / 'frames'):
        for part in (path, *path.parents):
            if part == record:
                break
            if part.is_symlink():
                raise RecordError('Gate records cannot traverse symlinks')
    if not (media / TOOLS / 'channel_profile.py').is_file():
        raise RecordError('Gate channel profile unavailable')


def configure_gate(gate, record: Path, media: Path) -> None:
    # ROOT is used for resolving narration/sidecar paths as well as frame links.
    # Keep it at the media source; override the two frame-link operations below.
    gate.ROOT = media
    gate.LIB_DIR = record / LIBRARY
    gate.LIB_JSON = gate.LIB_DIR / 'library.json'
    gate.FRAMES = gate.LIB_DIR / 'frames'
    original_add = gate.add_entry

    def add(*args, **kwargs):
        # add_entry emits a path relative to ROOT. A scoped switch ensures those
        # links remain channel-relative, never absolute scratch paths.
        gate.ROOT = record
        try:
            return original_add(*args, **kwargs)
        finally:
            gate.ROOT = media
    gate.add_entry = add


def run_gate(engine: Path, record: Path, media: Path, slug: str,
             arguments: list[str], *, child: bool = False) -> int:
    if refusal(engine):
        raise RecordError('Analytics gate engine is retired or unverifiable')
    validate(record, media, slug)
    tools = engine / TOOLS
    previous_path = sys.path[:]
    sys.path.insert(0, str(tools))
    # The engine's old default profile must never leak into another channel.
    previous = sys.modules.get('channel_profile')
    try:
        sys.modules['channel_profile'] = load('channel_profile', media / TOOLS / 'channel_profile.py')
        if child:
            # Only operations used by gate_upcoming are exposed by this adapter.
            if not arguments or arguments[0] not in ('add', 'check'):
                raise RecordError('Analytics gate permits add and check only')
            gate = load('analytics_short_gate', tools / 'gate_shorts_open.py')
            configure_gate(gate, record, media)
            return gate.main(arguments)
        gate = load('analytics_upcoming_gate', tools / 'gate_upcoming.py')
        gate.LIB_JSON = record / LIBRARY / 'library.json'
        original_run = gate.run

        def child_run(command):
            if len(command) < 2 or Path(command[1]) != gate.GATE:
                raise RecordError('Unexpected analytics gate subprocess')
            return original_run([sys.executable, str(Path(__file__).resolve()),
                '--engine', str(engine), '--record', str(record), '--media', str(media),
                '--channel', slug, '--child', '--', *command[2:]])
        gate.run = child_run
        return gate.main(arguments)
    finally:
        sys.path[:] = previous_path
        if previous is None:
            sys.modules.pop('channel_profile', None)
        else:
            sys.modules['channel_profile'] = previous


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('engine', 'record', 'media'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--channel', required=True)
    parser.add_argument('--child', action='store_true')
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    arguments = args.arguments[1:] if args.arguments[:1] == ['--'] else args.arguments
    try:
        return run_gate(args.engine, args.record, args.media, args.channel, arguments, child=args.child)
    except (RecordError, OSError, ValueError):
        # No raw child diagnostics or potentially credential-bearing paths.
        print('Analytics gate adapter failed; inspect channel layout and inputs.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
