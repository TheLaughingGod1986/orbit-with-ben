"""Production timer orchestration with fake collectors and real local Git records."""
from contextlib import ExitStack
from pathlib import Path
import argparse
import json
import os
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import analytics_timer as timer
import analytics_session as sessions
from analytics_auxiliary import auxiliary
from analytics_collection import collection_session


class TimerRecords(unittest.TestCase):
    def test_failure_isolated_and_pending_push_retried_through_timer(self):
        with ExitStack() as stack:
            root = Path(stack.enter_context(tempfile.TemporaryDirectory()))
            stack.enter_context(patch.dict(os.environ, {
                'GIT_AUTHOR_NAME': 'Studio tests', 'GIT_COMMITTER_NAME': 'Studio tests',
                'GIT_AUTHOR_EMAIL': 'studio-test', 'GIT_COMMITTER_EMAIL': 'studio-test',
                'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_NOSYSTEM': '1'}))
            def git(repo, *args):
                p = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, p.stderr)
                return p.stdout.strip()
            def write(base, name, text='{}'):
                target = base / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text)
            sources, remotes = {}, {}
            for slug in ('studio', 'space', 'science'):
                remote, source = root / (slug + '.git'), root / 'sources' / slug
                git(root, 'init', '--bare', str(remote))
                git(root, 'clone', str(remote), str(source))
                git(source, 'checkout', '-b', 'main')
                write(source, '.gitignore', 'node_modules/\n')
                if slug == 'studio':
                    write(source, 'channels/channels.json', '{"studio":{"github":"owner/studio"}}')
                    write(source, 'jobs/queue.json', '{"jobs":[]}')
                    write(source, '07_Content-Ops/scripts/placeholder.ts', '// fixture')
                    write(source, '07_Content-Ops/.gitignore', '/node_modules\n')
                    write(source, '05_Analytics/dashboard/index.html', 'before')
                else:
                    write(source, 'studio/channel.json', json.dumps({'slug': slug}))
                    write(source, f'05_Analytics/{slug}/snapshots/before.json')
                    write(source, '00_Brand/Channel-Setup/social/UPLOADS.json')
                git(source, 'add', '.')
                git(source, 'commit', '-m', 'seed')
                git(source, 'push', 'origin', 'main')
                sources[slug], remotes[slug] = source, remote
            write(sources['studio'], '07_Content-Ops/node_modules/tsx/dist/cli.mjs', '// fixture')
            credential = root / 'local.env'
            credential.write_text('')
            stack.enter_context(patch.object(timer, 'refusal', return_value=None))
            stack.enter_context(patch.object(sessions, 'refusal', return_value=None))
            stack.enter_context(patch('analytics_worktree.refusal', return_value=None))
            channel = timer.channels
            stack.enter_context(patch.object(channel, 'ROOT', sources['studio']))
            stack.enter_context(patch.object(channel, 'studio_slug', return_value=None))
            stack.enter_context(patch.object(channel, 'studio_checkout', return_value=sources['studio']))
            stack.enter_context(patch.object(channel, 'studio_github', return_value='owner/studio'))
            stack.enter_context(patch.object(channel, 'studio_repo', return_value={
                'url': 'https://github.com/owner/studio.git', 'env': 'STUDIO_REPO'}))
            stack.enter_context(patch.object(channel, 'slugs', return_value=['space', 'science']))
            stack.enter_context(patch.object(channel, 'checkout', side_effect=sources.get))
            stack.enter_context(patch.object(channel, 'get', side_effect=lambda s: {
                'repo': {'url': f'https://github.com/owner/{s}.git', 'env': s.upper() + '_REPO'},
                'analytics': {'open_gate_library': s == 'space'}}))
            # Production requires GitHub identities; this fixture permits only its exact local remotes.
            def verify(source, expected):
                self.assertEqual(source, sources[Path(expected).stem])
                self.assertEqual(git(source, 'remote', 'get-url', 'origin'), str(remotes[source.name]))
            stack.enter_context(patch.object(sessions, 'verify_source', side_effect=verify))
            commands = []
            def run(command):
                commands.append(command.name)
                if command.name.startswith('snapshot:'):
                    slug = command.name.split(':')[1]
                    write(Path(command.env[slug.upper() + '_REPO']),
                          f'05_Analytics/{slug}/snapshots/2026-11-20.json', '{"videos":[]}')
                elif command.name == 'dispatch':
                    self.assertEqual(command.env['FIELD_ORDER_QUEUE_REPO'], str(sources['studio']))
                elif command.name == 'gate:space':
                    record = Path(command.env['SPACE_REPO'])
                    self.assertEqual(command.args[command.args.index('--media-root') + 1], str(sources['space']))
                    write(record, '00_Brand/Channel-Setup/audits/shorts_open_library/library.json')
                    write(record, '05_Analytics/space/UPCOMING_SHORTS_GATE.md', 'checked')
                elif command.name == 'report':
                    for slug in ('space', 'science'):
                        write(Path(command.env[slug.upper() + '_REPO']), f'05_Analytics/{slug}/REPORT.md', 'report')
                    write(command.cwd.parent, '05_Analytics/dashboard/index.html', 'after')
                elif command.name == 'board':
                    self.assertEqual(command.env['SPACE_REPO'], str(sources['space']))
                return 0
            stack.enter_context(patch.object(timer, 'auxiliary', side_effect=lambda *a, **kw:
                auxiliary(*a, **kw, run=run, day='2026-11-20')))
            stack.enter_context(patch.object(timer, 'collection_session', side_effect=lambda *a, **kw:
                collection_session(*a, **kw, run=run, lock=root / 'session.lock')))
            args = argparse.Namespace(records=root / 'records', credentials=credential,
                cache=root / 'cache', safe_cache=root / 'safe', gate_timeout=30, no_board=False)
            hook = remotes['science'] / 'hooks/pre-receive'
            hook.write_text('#!/bin/sh\nexit 1\n')
            hook.chmod(0o755)
            self.assertEqual(timer.worker(args), 1)
            pending = git(root / 'records/science', 'rev-parse', 'HEAD')
            self.assertNotEqual(git(remotes['science'], 'rev-parse', 'main'), pending)
            self.assertEqual(git(remotes['space'], 'show', 'main:05_Analytics/space/REPORT.md'), 'report')
            self.assertEqual(commands, ['snapshot:space', 'snapshot:science', 'dispatch', 'gate:space', 'report', 'board'])
            hook.unlink()
            commands.clear()
            self.assertEqual(timer.worker(args), 0)
            self.assertEqual(git(remotes['science'], 'rev-parse', 'main'), pending)
            for source in sources.values():
                self.assertEqual(git(source, 'status', '--porcelain'), '')
            self.assertFalse((sources['space'] / '05_Analytics/space/REPORT.md').exists())
            self.assertEqual((sources['studio'] / '05_Analytics/dashboard/index.html').read_text(), 'before')


if __name__ == '__main__':
    unittest.main()
