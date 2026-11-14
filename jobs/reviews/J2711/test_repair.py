import unittest,datetime
from repair_scheduled import allowed
from restore_truncated_tags import payload_for
class Guard(unittest.TestCase):
 def test_only_unchanged_future_scheduled_text(self):
  now=datetime.datetime(2026,11,12,tzinfo=datetime.timezone.utc)
  p=dict(id='x',status='scheduled',text='Hook',dueAt='2026-11-18T11:30:00Z',channelId='facebook')
  self.assertTrue(allowed(p,p,now))
  for state in ['sent','sending','draft','error']:
   changed={**p,'status':state};self.assertFalse(allowed(changed,changed,now))
  self.assertFalse(allowed(p,{**p,'text':'new'},now))
  tagged={**p,'text':'Hook #Mars'};self.assertFalse(allowed(tagged,tagged,now))
  self.assertFalse(allowed(p,p,now+datetime.timedelta(days=7)))
class Tags(unittest.TestCase):
 def test_only_first_fifteen_truncation_is_repaired(self):
  tags=[str(i) for i in range(19)];live=dict(title='Keep',description='Keep',categoryId='28',defaultAudioLanguage='en-GB',tags=tags[:15])
  result=payload_for(live,tags)
  self.assertEqual(result,{**live,'tags':tags});self.assertEqual(len(live['tags']),15)
  with self.assertRaises(AssertionError):payload_for({**live,'tags':['intentional retag']},tags)
if __name__=='__main__':unittest.main()
