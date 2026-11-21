"""Real timer, TypeScript collector/report and local Git; offline transport only."""
from contextlib import ExitStack
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import analytics_timer as timer
import analytics_session as sessions
from analytics_collection import collection_session

SOURCE = Path(__file__).resolve().parents[1]
OPS = SOURCE / '07_Content-Ops'


@unittest.skipUnless((OPS / 'node_modules/tsx/dist/cli.mjs').is_file() and shutil.which('node'),
                     'Content Ops dependencies required for actual collector acceptance')
class CollectorRecords(unittest.TestCase):
    def test_actual_collectors_publish_only_owner_records_without_touching_sources(self):
        with ExitStack() as stack:
            root = Path(stack.enter_context(tempfile.TemporaryDirectory()))
            environment = {k: os.environ[k] for k in ('PATH', 'TMPDIR', 'SYSTEMROOT') if k in os.environ}
            environment.update(GIT_AUTHOR_NAME='Studio tests', GIT_COMMITTER_NAME='Studio tests',
                GIT_AUTHOR_EMAIL='studio-test', GIT_COMMITTER_EMAIL='studio-test',
                GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')
            stack.enter_context(patch.dict(os.environ, environment, clear=True))

            def git(repo, *args):
                result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout.strip()

            def write(base, name, value):
                dest = base / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(value)

            sources = {slug: root / 'sources' / slug for slug in ('studio', 'owb', 'hos', 'ww2')}
            engine = sources['studio']
            registry = {'studio': {'github': 'fixture/studio', 'env': 'STUDIO_REPO',
                'default_channel': 'owb', 'checkouts': ['studio']}, 'channels': []}
            for slug, source in sources.items():
                source.mkdir(parents=True)
                write(source, '.gitignore', 'node_modules/\n__pycache__/\n')
                os.environ[slug.upper() + '_REPO'] = str(source)
                if slug == 'studio':
                    continue
                registry['channels'].append({'slug': slug, 'env': slug.upper() + '_REPO', 'checkouts': [slug]})
                manifest = {'slug': slug, 'label': slug, 'name': slug, 'title_match': slug, 'wip': {},
                    'repo': {'url': f'https://github.com/fixture/{slug}.git', 'env': slug.upper() + '_REPO', 'checkouts': [slug]}}
                write(source, 'studio/channel.json', json.dumps(manifest))
                write(engine, f'channels/{slug}/channel.json', json.dumps(manifest))
                snapshot = {'channel': slug, 'channelId': 'fixture', 'date': '2026-01-01',
                    'takenAt': '2026-01-01T00:00:00Z', 'totals': {'subscribers': 0, 'views': 0, 'videos': 0},
                    'videos': [], 'analytics': None}
                write(source, f'05_Analytics/{slug}/snapshots/2026-01-01.json', json.dumps(snapshot))
            write(engine, 'channels/channels.json', json.dumps(registry))
            write(engine, 'jobs/queue.json', '{"jobs": []}')
            for name in ('channels.py', 'engine_guard.py'):
                write(engine, 'scripts/' + name, (SOURCE / 'scripts' / name).read_text())
            for name in ('package.json', 'tsconfig.json', 'scripts/analytics-snapshot.ts',
                         'scripts/analytics-report.ts', 'scripts/analytics-paths.ts'):
                write(engine, '07_Content-Ops/' + name, (OPS / name).read_text())
            shutil.copytree(OPS / 'src', engine / '07_Content-Ops/src')
            write(engine, '07_Content-Ops/.gitignore', '/node_modules\n')
            remotes = {}
            for slug, source in sources.items():
                remote = root / (slug + '.git')
                git(root, 'init', '--bare', str(remote))
                git(source, 'init', '-b', 'main')
                git(source, 'remote', 'add', 'origin', str(remote))
                git(source, 'add', '.')
                git(source, 'commit', '-m', 'seed')
                git(source, 'push', 'origin', 'main')
                remotes[slug] = remote
            (engine / '07_Content-Ops/node_modules').symlink_to((OPS / 'node_modules').resolve(), target_is_directory=True)
            preload = root / 'fake-api.mjs'
            shutil.copy2(OPS / 'tests/fixtures/analytics-api.mjs', preload)
            os.environ.update(NODE_OPTIONS=f'--import={preload}', FIXTURE_REQUEST_LOG=str(root / 'requests.jsonl'))
            credential = root / 'fixture.env'
            credential.write_text('GOOGLE_CLIENT_ID=fixture\nGOOGLE_CLIENT_SECRET=fixture\n'
                'YT_ANALYTICS_REFRESH_TOKEN_OWB=owb\nYT_ANALYTICS_REFRESH_TOKEN_HOS=hos\n'
                'YT_ANALYTICS_REFRESH_TOKEN_WW2=ww2\nYT_CHANNEL_ID_WW2=UC0000000000000000000000\n')
            stack.enter_context(patch.object(timer.channels, 'ROOT', engine))
            stack.enter_context(patch.object(timer.channels, 'DIR', engine / 'channels'))
            loader = timer.channels._load
            loader.cache_clear()
            stack.callback(loader.cache_clear)
            stack.enter_context(patch.object(timer.channels, '_load', side_effect=lambda: loader(str(engine / 'channels'))))

            # Production insists on GitHub remotes; this offline test permits exact fixture remotes only.
            def verify(source, expected):
                slug = Path(expected).stem
                self.assertEqual(source, sources[slug])
                self.assertEqual(git(source, 'remote', 'get-url', 'origin'), str(remotes[slug]))
            stack.enter_context(patch.object(sessions, 'verify_source', side_effect=verify))
            phases = []
            def after_snapshots(session, env):
                phases.append(tuple(session.records))
                self.assertEqual(env['FIELD_ORDER_QUEUE_REPO'], str(engine))
                return []  # gates/dispatch have their own offline acceptance suite
            stack.enter_context(patch.object(timer, 'auxiliary', return_value=after_snapshots))
            stack.enter_context(patch.object(timer, 'collection_session', side_effect=lambda *a, **kw:
                collection_session(*a, **kw, lock=root / 'session.lock')))
            args = argparse.Namespace(records=root / 'records', credentials=credential,
                cache=root / 'cache', safe_cache=root / 'safe', gate_timeout=30, no_board=True)
            self.assertEqual(timer.worker(args), 0)
            self.assertEqual(len(phases), 1)
            self.assertEqual(set(phases[0]), {'studio', 'owb', 'hos', 'ww2'})
            for slug, source in sources.items():
                self.assertEqual(git(source, 'status', '--porcelain'), '')
                changed = git(remotes[slug], 'diff', '--name-only', 'main~1', 'main').splitlines()
                scope = '05_Analytics/dashboard/' if slug == 'studio' else f'05_Analytics/{slug}/'
                self.assertTrue(changed)
                self.assertTrue(all(name.startswith(scope) for name in changed), changed)
            board = json.loads(git(remotes['studio'], 'show', 'main:05_Analytics/dashboard/data.json'))
            self.assertEqual(len(board['channels']), 2)
            detail = json.loads(git(remotes['ww2'], 'show', 'main:05_Analytics/ww2/detail.json'))
            self.assertEqual(detail['failures'], [])
            self.assertTrue((root / 'requests.jsonl').is_file())


if __name__ == '__main__':
    unittest.main()
