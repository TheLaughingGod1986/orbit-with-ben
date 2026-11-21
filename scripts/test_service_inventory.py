"""Service inventory must never run a wrapper or echo sensitive plist contents."""
import importlib.util
import json
import pathlib
import plistlib
import tempfile
import unittest
from unittest import mock
from types import SimpleNamespace

spec = importlib.util.spec_from_file_location('inventory', pathlib.Path(__file__).parent / 'mini/inventory_services.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Inventory(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = pathlib.Path(self.tmp.name)
        self.old = self.home / 'old engine'
        self.script = self.home / 'runner.sh'
        self.script.write_text('#!/bin/sh\ntouch EXECUTED\n# engine_guard; worker.pause\ncd "' + str(self.old) + '"\n')
        self.path = self.home / 'service.plist'

    def inspect(self, doc, binary=False):
        self.path.write_bytes(plistlib.dumps(doc, fmt=plistlib.FMT_BINARY if binary else plistlib.FMT_XML))
        return module.inspect_service(self.path, self.old, self.home)

    def test_resolves_home_wrapper_without_execution_or_disclosure(self):
        row = self.inspect({'Label': 'com.test.worker', 'ProgramArguments': ['/bin/zsh', '-lc', '$HOME/runner.sh'],
                            'EnvironmentVariables': {'PRIVATE': 'DO_NOT_DISCLOSE'}})
        self.assertTrue(row['command_resolved'])
        self.assertTrue(row['old_engine_reference'])
        self.assertTrue(row['scripts'][0]['guard_mentioned'])
        self.assertTrue(row['scripts'][0]['pause_mentioned'])
        self.assertTrue(row['needs_review'])
        out = json.dumps(row)
        for hidden in ('DO_NOT_DISCLOSE', str(self.home), 'touch EXECUTED', 'PRIVATE'):
            self.assertNotIn(hidden, out)
        self.assertFalse((self.home / 'EXECUTED').exists())

    def test_binary_plist_old_root_and_direct_program(self):
        row = self.inspect({'Label': 'com.test.worker', 'Program': str(self.script),
                            'WorkingDirectory': str(self.old)}, binary=True)
        self.assertTrue(row['old_engine_reference'])
        self.assertTrue(row['command_resolved'])

    def test_dynamic_shell_remains_unresolved(self):
        row = self.inspect({'Label': 'com.test.worker', 'ProgramArguments': ['/bin/sh', '-lc', '$(touch NEVER)']})
        self.assertFalse(row['command_resolved'])
        self.assertTrue(row['needs_review'])

    def test_invalid_label_and_environment_are_not_echoed(self):
        row = self.inspect({'Label': 'secret/value', 'EnvironmentVariables': {'TOKEN': 'hidden'}})
        self.assertEqual(row['status'], 'invalid_label')
        self.assertNotIn('secret', json.dumps(row))
        self.assertNotIn('hidden', json.dumps(row))

    def test_bad_plist_and_missing_script_fail_closed(self):
        self.path.write_bytes(b'not a plist')
        self.assertEqual(module.inspect_service(self.path, self.old, self.home)['status'], 'unreadable')
        row = self.inspect({'Label': 'com.test.worker', 'ProgramArguments': [str(self.home / 'missing.sh')]})
        self.assertFalse(row['command_resolved'])
        self.assertTrue(row['needs_review'])

    def test_malformed_xml_returns_safe_row_instead_of_aborting_inventory(self):
        self.path.write_bytes(b'<?xml version="1.0"?><plist><dict><key>bad & value</key></dict></plist>')
        row = module.inspect_service(self.path, self.old, self.home)
        self.assertEqual(row['status'], 'unreadable')
        self.assertEqual(row['source_name'], 'service.plist')
        self.assertNotIn('bad & value', json.dumps(row))

    def test_oversized_input_is_not_read_or_disclosed(self):
        self.path.write_bytes(b'x' * (module.MAX_BYTES + 1))
        self.assertEqual(module.inspect_service(self.path, self.old, self.home)['status'], 'unreadable')


class LoadedState(unittest.TestCase):
    def probe(self, code=0, out='', err=''):
        with mock.patch.object(module.platform, 'system', return_value='Darwin'), \
             mock.patch.object(module.os, 'getuid', return_value=501), \
             mock.patch.object(module.subprocess, 'run', return_value=SimpleNamespace(
                 returncode=code, stdout=out, stderr=err)) as run:
            row = module.loaded_state('com.test.worker')
        run.assert_called_once_with(['/bin/launchctl', 'print', 'gui/501/com.test.worker'],
                                    capture_output=True, text=True, timeout=5)
        return row

    def test_reads_only_top_level_state_without_disclosing_environment(self):
        row = self.probe(out='gui/501/com.test.worker = {\n\tstate = running\n'
                         '\tenvironment = {\n\t\tTOKEN = hidden\n\t\tstate = waiting\n\t}\n}')
        self.assertEqual(row, {'status': 'loaded', 'state': 'running'})
        self.assertNotIn('hidden', json.dumps(row))

    def test_missing_service_requires_exact_label_and_diagnostic(self):
        self.assertEqual(self.probe(code=113, err='Could not find service "com.test.worker" in domain for user gui: 501'),
                         {'status': 'not_loaded'})
        for error in ('Could not find domain for', 'Operation not permitted',
                      'Could not find service "another" in domain for user gui: 501'):
            self.assertEqual(self.probe(code=1, err=error), {'status': 'unavailable'})

    def test_unknown_or_nested_state_is_not_echoed(self):
        for output in ('\tstate = secret value\n', '\t\tstate = running\n', ''):
            self.assertEqual(self.probe(out=output), {'status': 'loaded', 'state': 'unknown'})

    def test_invalid_label_and_non_mac_do_not_spawn(self):
        with mock.patch.object(module.subprocess, 'run') as run:
            self.assertEqual(module.loaded_state('bad/secret'), {'status': 'invalid_label'})
            with mock.patch.object(module.platform, 'system', return_value='Linux'):
                self.assertEqual(module.loaded_state('com.test.worker'), {'status': 'unavailable'})
            run.assert_not_called()

    def test_timeout_and_launch_errors_do_not_disclose_diagnostics(self):
        with mock.patch.object(module.platform, 'system', return_value='Darwin'):
            for error in (OSError('hidden'), module.subprocess.TimeoutExpired('hidden', 5)):
                with mock.patch.object(module.subprocess, 'run', side_effect=error):
                    self.assertEqual(module.loaded_state('com.test.worker'), {'status': 'unavailable'})


if __name__ == '__main__':
    unittest.main()
