import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project'))
import mechanism_graphics as m
out=Path('/Users/benjaminoats/_desk/cache/J2089/mechanism_previews_v02')
old=json.loads(Path('/Users/benjaminoats/_desk/cache/J2089/mechanism_previews_v01/MECHANISM_MANIFEST_v01.json').read_text())
old={s['id']:s for s in old['clips']}
checks=[]
for s in m.SPECS:
    if s['id'] not in ['r10_spectrum','r32_scalemap']:
        assert hashlib.sha256((out/('code_graphic_032_'+s['id']+'_v01.png')).read_bytes()).hexdigest()==old[s['id']]['preview_sha256'],s['id']
        continue
    for n in range(109):
        im=m.frame(s,n/30); box=im.getchannel('A').getbbox()
        assert box is None or (box[0]>=96 and box[1]>=54 and box[2]<=1824 and box[3]<=1026),(s['id'],n,box)
    assert m.frame(s,0).getbbox() is None and m.frame(s,3.6).getbbox() is None
    assert m.frame(s,.8).tobytes()!=m.frame(s,1.5).tobytes()
    preview=out/('code_graphic_032_'+s['id']+'_v01.png')
    assert m.frame(s).tobytes()==m.Image.open(preview).tobytes()
    checks.append(dict(id=s['id'],samples=109,preview_sha256=hashlib.sha256(preview.read_bytes()).hexdigest(),safe_area=True,transparent_entry_exit=True,changing_frames=True))
s=next(s for s in m.SPECS if s['id']=='r10_spectrum')
assert m.frame(s,1.19).getpixel((1120,680))[3]==0
assert m.frame(s,1.21).getpixel((1120,680))[3]>0
# New prism's incoming ray meets left face at x~647.6, not old x610.
record=dict(job='J2089',checks=checks,unchanged_other_previews=15,notch_arrival_threshold=.75,rendered=False,status='REQUIRES_STILL_REVIEW',perceived_audio=False,perceived_motion=False)
(out/'FIX_VERIFICATION_v01.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
