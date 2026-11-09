import datetime as dt
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import board_publish as bp

class ChiefVisibility(unittest.TestCase):
    def test_only_live_leased_review_is_active_and_next_excludes_it(self):
        at=dt.datetime(2026,10,26,21,tzinfo=dt.timezone.utc)
        with tempfile.TemporaryDirectory() as folder:
            state=Path(folder)
            active={'job':'J0956','agent':'codex','pid':os.getpid(),'expiresAt':bp.iso(at+dt.timedelta(minutes=5))}
            (state/'active.json').write_text(json.dumps(active))
            (state/'inbox.json').write_text(json.dumps({'jobs':[{'id':'J0956'},{'id':'J0974'},{'id':'DONE'}]}))
            jobs=[{'id':'J0956','status':'blocked'},{'id':'J0974','status':'blocked'},{'id':'DONE','status':'done'}]
            result=bp.chief_work(at,state,'codex',jobs)
            self.assertEqual(result['active']['job'],'J0956')
            self.assertEqual(result['next'],[{'id':'J0974'}])
            self.assertIsNone(bp.chief_work(at+dt.timedelta(minutes=6),state,'codex',jobs)['active'])
            self.assertIsNone(bp.chief_work(at,state,'gemini',jobs)['active'])
            with mock.patch.object(bp.os,'kill',side_effect=ProcessLookupError):
                self.assertIsNone(bp.chief_work(at,state,'codex',jobs)['active'])

    def test_missing_runtime_state_is_idle(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(bp.chief_work(bp.now(),Path(folder),'codex',[])['next'],[])
            self.assertIsNone(bp.chief_work(bp.now(),Path(folder),'codex',[])['active'])
