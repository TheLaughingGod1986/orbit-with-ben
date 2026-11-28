"""Real gate modules with synthetic frames; no media, account or API calls."""
from contextlib import ExitStack
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import analytics_gate as module
from analytics_worktree import RecordError

ENGINE = Path(__file__).resolve().parent.parent


class GateAdapter(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.root = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.record, self.media = self.root / 'records', self.root / 'media'
        for root in (self.record, self.media):
            (root / 'studio').mkdir(parents=True)
            (root / 'studio/channel.json').write_text(json.dumps({'slug': 'space', 'analytics': {'open_gate_library': True}}))
        profile = self.media / module.TOOLS / 'channel_profile.py'
        profile.parent.mkdir(parents=True)
        profile.write_text("NAME='Fixture'\nHANDLE='Fixture'\nSLUG='fixture'\nROBOT_FRAME0_CHECK=False\nBACKGROUND_SSIM_CHECK=False\n")
        self.lib = self.record / module.LIBRARY
        self.lib.mkdir(parents=True)
        (self.lib / 'library.json').write_text('{"entries": []}')

    def test_validation_refuses_mismatched_owner_aliases_and_symlink_writes(self):
        module.validate(self.record, self.media, 'space')
        for record, media, slug in ((self.record, self.record, 'space'),
                                   (Path('relative'), self.media, 'space'),
                                   (self.record, self.media, 'other')):
            with self.assertRaises(RecordError):
                module.validate(record, media, slug)
        (self.lib / 'frames').symlink_to(self.media, target_is_directory=True)
        with self.assertRaisesRegex(RecordError, 'symlink'):
            module.validate(self.record, self.media, 'space')

    def test_real_add_writes_only_record_library_and_relative_frame_link(self):
        real_load = module.load
        def loader(name, path):
            gate = real_load(name, path)
            if name == 'analytics_short_gate':
                self.assertFalse(gate.channel.ROBOT_FRAME0_CHECK)
                gate.dhash = lambda *_: 123
                gate.thumb = lambda *_: [1, 2, 3]
                def frame(_src, _time, target):
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(b'fixture')
                gate.save_frame = frame
            return gate
        with patch.object(module, 'load', loader):
            self.assertEqual(module.run_gate(ENGINE, self.record, self.media, 'space',
                ['add', '--id', 'fixture1234', '--date', '2026-11-20', '--title', 'Fixture',
                 '--file', str(self.media / 'fixture.mp4'), '--status', 'scheduled'], child=True), 0)
        entry = json.loads((self.lib / 'library.json').read_text())['entries'][0]
        self.assertEqual(entry['frame'], str(module.LIBRARY / 'frames/fixture1234.jpg'))
        self.assertTrue((self.record / entry['frame']).is_file())
        self.assertFalse((self.media / module.LIBRARY).exists())
        self.assertNotIn('orbit', entry)

    def test_source_relative_vo_resolution_and_root_restored_on_add_failure(self):
        gate = module.load('gate_fixture', ENGINE / module.TOOLS / 'gate_shorts_open.py')
        def fail(*_):
            raise ValueError('fixture')
        gate.add_entry = fail
        module.configure_gate(gate, self.record, self.media)
        stem = self.media / 'audio/stem.wav'
        stem.parent.mkdir()
        stem.write_bytes(b'fixture')
        self.assertEqual(gate._resolve_candidate('audio/stem.wav', self.media / 'movie.mp4'), stem)
        with self.assertRaises(ValueError):
            gate.add_entry()
        self.assertEqual(gate.ROOT, self.media)

    def test_upcoming_uses_record_library_and_wraps_child_with_same_roots(self):
        real_load = module.load
        seen = []
        def loader(name, path):
            gate = real_load(name, path)
            if name == 'analytics_upcoming_gate':
                gate.run = lambda args: (seen.append(args) or (0, ''))
                def main(_):
                    self.assertEqual(gate.LIB_JSON, self.lib / 'library.json')
                    gate.run([sys.executable, str(gate.GATE), 'check', 'fixture.mp4'])
                    return 0
                gate.main = main
            return gate
        with patch.object(module, 'load', loader):
            self.assertEqual(module.run_gate(ENGINE, self.record, self.media, 'space', []), 0)
        command = seen[0]
        self.assertEqual(command[command.index('--record') + 1], str(self.record))
        self.assertEqual(command[command.index('--media') + 1], str(self.media))
        self.assertEqual(command[-4:], ['--child', '--', 'check', 'fixture.mp4'])

    def test_empty_upcoming_report_runs_real_code_without_changing_sources(self):
        snapshot, uploads, report = (self.root / n for n in ('snapshot.json', 'uploads.json', 'report.md'))
        snapshot.write_text('{"videos": []}')
        uploads.write_text('{"videos": {}}')
        before = (self.lib / 'library.json').read_bytes()
        self.assertEqual(module.run_gate(ENGINE, self.record, self.media, 'space',
            ['--snapshot', str(snapshot), '--uploads', str(uploads), '--media-root', str(self.media),
             '--out', str(report), '--add']), 0)
        self.assertIn('No scheduled Shorts', report.read_text())
        self.assertEqual((self.lib / 'library.json').read_bytes(), before)
        self.assertFalse((self.media / module.LIBRARY).exists())

    def test_retired_engine_refuses_before_loading_channel_or_writing(self):
        with patch.object(module, 'refusal', return_value='retired'), patch.object(module, 'load') as load:
            with self.assertRaisesRegex(RecordError, 'retired'):
                module.run_gate(ENGINE, self.record, self.media, 'space', [])
            load.assert_not_called()

    def test_child_refuses_other_mutators_and_restores_profile(self):
        previous = sys.modules.get('channel_profile')
        before = sys.path[:]
        with self.assertRaises(RecordError):
            module.run_gate(ENGINE, self.record, self.media, 'space', ['fetch'], child=True)
        self.assertIs(sys.modules.get('channel_profile'), previous)
        self.assertEqual(sys.path, before)


if __name__ == '__main__':
    unittest.main()
