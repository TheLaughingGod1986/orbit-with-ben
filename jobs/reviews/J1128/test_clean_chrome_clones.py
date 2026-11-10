import pathlib,tempfile,time,unittest,os
from clean_chrome_clones import candidates
class Selection(unittest.TestCase):
 def test_preserve_live_recent_links_and_unrelated(self):
  with tempfile.TemporaryDirectory() as t:
   root=pathlib.Path(t)
   for name in ['code_sign_clone.old','code_sign_clone.live','code_sign_clone.new','unrelated']:
    p=root/name;p.mkdir();(p/'Google Chrome.app.bundle').mkdir();os.utime(p,(1,1))
   os.utime(root/'code_sign_clone.new',(time.time(),time.time()))
   (root/'code_sign_clone.link').symlink_to(root/'code_sign_clone.old',target_is_directory=True)
   self.assertEqual([p.name for p in candidates(root,[str(root/'code_sign_clone.live')+'/bin'],time.time())],['code_sign_clone.old'])
if __name__=='__main__':unittest.main()
