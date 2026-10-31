"""J1338: only 14.766667–18.4s rebuilt; other decoded frames from v08. No added grain or sharpening."""
from pathlib import Path
import sys,subprocess,json,hashlib,importlib.util
import numpy as np
from PIL import Image,ImageFilter,ImageOps
REPO=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
AUD='00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10'
BASE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('old',BASE/'caption_helpers_j1338.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
old.SHORTS={'ar2':{'words':REPO/AUD/'02_Voiceover/apophis_ar2_vo_v01_words.json','hook':[['ISS','CRASHES'],['~2031']]}}
OUT=Path('/private/tmp/J1338-render');OUT.mkdir(exist_ok=True)
EVID=Path(__file__).parent/'j1338_evidence';EVID.mkdir(exist_ok=True)
SRC=Path('/Volumes/data/mac-mini-archive/jobs/J1324/masters/owb_apophis_ar2_v08.mp4')
MASTER=OUT/'owb_apophis_ar2_v10.mp4'
words=old.load_words(old.SHORTS['ar2']['words']);caps=old.caption_track(words,18.4);hook=old.hook_image(old.SHORTS['ar2']['hook'],'~2031')
def changed(t):return 14.7666666666<=t<18.4

def plate(t):
    # Only late is rendered: sunlit station from accepted source 540–543.2 s.
    late=14.7666666666<=t<18.4
    u=1+t if t<2.4 else t-18.4 if t>=18.4 else (t-14.7666666667)*3.2/(18.4-14.7666666667)
    idx=round(u*30)+1
    name=f'iss_day_{min(120,idx):04d}.jpg' if late else f'iss_frames_new_{idx:04d}.jpg'
    src=Image.open((OUT if late else Path('/private/tmp/J1321-media'))/name).convert('RGB')
    if late:src=src # full 1280x720 native image; no crop/enlargement
    # Global exposure curve, not a key: every dark station component survives.
    gamma=1.0
    src=src.point([min(255,round(27+228*(v/255)**gamma)) for v in range(256)]*3)
    sharp=src.resize((1080,608),Image.Resampling.LANCZOS)
    # Only the same source fills the frame. Soft fill, sharp full-width native view.
    bg=ImageOps.fit(src,(270,480)).filter(ImageFilter.GaussianBlur(24)).resize((1080,1920),Image.Resampling.BICUBIC)
    # Match boundary colour continuously rather than feather an inset over another scene.
    # A narrow vertical blend joins the native image to its own defocused fill.
    fr=sharp.convert('RGBA')
    alpha=np.ones((608,1080),dtype=np.uint8)*255
    for y in range(60):
        value=round(255*(y/60)**2*(3-2*y/60))
        alpha[y]=value;alpha[-1-y]=value
    fr.putalpha(Image.fromarray(alpha))
    im=bg.convert('RGBA');im.alpha_composite(fr,(0,650))
    # Continuous restrained push also runs through the forward loop preroll.
    im=im.convert('RGB');z=1.0+u*.04;cw=1080/z;ch=1920/z
    im=im.transform((1080,1920),Image.Transform.EXTENT,((1080-cw)/2,(1920-ch)/2,(1080+cw)/2,(1920+ch)/2),Image.Resampling.BICUBIC).convert('RGBA')
    if t<2:im.alpha_composite(hook)
    for a,b,cap in caps:
        if a<=t<b and t<18.4:im.alpha_composite(cap);break
    return im.convert('RGB')
if '--previews' in sys.argv:
    for t,name in [(0,'frame0'),(15.8,'late')]:plate(t).save(EVID/f'ar2_v10_{name}_preview.jpg',quality=95)
    sys.exit()
assert not MASTER.exists(),'refuse overwrite'
dec=subprocess.Popen(['ffmpeg','-v','error','-i',str(SRC),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-i',str(SRC),'-map','0:v','-map','1:a','-c:v','libx264','-preset','veryfast','-crf','16','-c:a','copy','-movflags','+faststart',str(MASTER)],stdin=subprocess.PIPE)
unchanged=hashlib.sha256();n=0
while True:
    buf=dec.stdout.read(1080*1920*3)
    if not buf:break
    assert len(buf)==1080*1920*3
    t=n/30
    if changed(t):buf=plate(t).tobytes()
    else:unchanged.update(buf)
    enc.stdin.write(buf);n+=1
    if n%90==0:print(n,flush=True)
enc.stdin.close();assert enc.wait()==0 and dec.wait()==0
(EVID/'render_receipt.json').write_text(json.dumps({'frames':n,'unchanged_decoded_input_sha256':unchanged.hexdigest(),'changed_intervals':[[14.7666666667,18.4]],'source_intervals':[[540,543.2]],'audio':'AAC stream copy from AR2 v08','sharp_upscale':{'open':1080/1280,'late':1080/1280}},indent=2)+'\n')
print(MASTER,flush=True)
