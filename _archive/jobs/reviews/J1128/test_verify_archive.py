import tempfile, pathlib, unittest
from verify_archive import verified
class Verify(unittest.TestCase):
 def test_sidecars_and_payload(self):
  with tempfile.TemporaryDirectory() as t:
   s=pathlib.Path(t)/"s";d=pathlib.Path(t)/"d";s.mkdir();d.mkdir()
   (s/"a").write_bytes(b"payload")
   (d/"._a").write_bytes(bytes.fromhex("0005160700020000"))
   before={"a":(7,"hash")};after={**before,"._a":(8,"metadata")}
   self.assertTrue(verified(s,d,before,after))
   self.assertFalse(verified(s,d,before,{**after,"a":(7,"wrong")}))
   self.assertFalse(verified(s,d,before,{"._a":(8,"metadata")}))
   self.assertFalse(verified(s,d,before,{**after,"extra":(1,"x")}))
   (d/"._a").write_bytes(b"not metadata")
   self.assertFalse(verified(s,d,before,after))
if __name__=="__main__":unittest.main()
