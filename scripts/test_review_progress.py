import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import chief_relay as cr

class ReviewProgress(unittest.TestCase):
    def test_own_review_steps_are_separate_and_only_current_chief_can_report(self):
        at=dt.datetime.now(dt.timezone.utc)
        with tempfile.TemporaryDirectory() as folder, mock.patch.object(cr,'STATE',Path(folder)), mock.patch.object(cr,'is_elected_chief',side_effect=lambda a,t:a=='codex'):
            cr.write_json(cr.d('active.json'),{'job':'J1','agent':'codex','expiresAt':cr.iso(at+dt.timedelta(minutes=10)),'progress':{'step':0,'of':3}})
            cr.review_progress('codex','J1',1,'Inputs checked',at)
            self.assertEqual(cr.read_json(cr.d('active.json'))['progress']['step'],1)
            for agent,job,step in [('gemini','J1',2),('codex','J2',2),('codex','J1',0),('codex','J1',4)]:
                with self.assertRaises(ValueError):cr.review_progress(agent,job,step,'invalid',at)
            with self.assertRaises(ValueError):cr.review_progress('codex','J1',2,'Expired',at+dt.timedelta(minutes=11))
            self.assertEqual(cr.read_json(cr.d('active.json'))['progress']['step'],1)
