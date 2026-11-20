"""Service inventory must never run a wrapper or echo sensitive plist contents."""
import importlib.util
import json
import pathlib
import plistlib
import tempfile
import unittest

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


if __name__ == '__main__':
    unittest.main()
