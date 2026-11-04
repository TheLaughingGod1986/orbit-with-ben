#!/usr/bin/env python3
"""J2016 bounded still-transform repair. No generation, approvals or publishing."""
import importlib.util,json,subprocess,sys,hashlib,math
from pathlib import Path
from PIL import Image
R=Path('/Users/benjaminoats/YouTube/orbit-with-ben'); W=Path('/private/tmp/J2016-wt'); A=R/'00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10'; E=Path(__file__).parent
sys.path.insert(0,str(R/'scripts'))
from short_c37 import loop_metrics,finish_scan
s=importlib.util.spec_from_file_location('asm',A/'assemble_j1321.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def sha(p):
 with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def run(c):return subprocess.run(list(map(str,c)),capture_output=True,text=True,check=True)
def ah(p):return run(['ffmpeg','-v','error','-i',p,'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).stdout.strip()
def gate(name,c,ev):
 p=subprocess.run(list(map(str,c)),capture_output=True,text=True);(ev/(name+'.txt')).write_text(p.stdout+p.stderr);print(name,p.returncode,flush=True);return p.returncode

def build(ar,old,new):
 ev=E/(ar+'_'+new);ev.mkdir(exist_ok=False)
 prior=Path('/Users/benjaminoats/_desk/handoff/J1471')/(ar+'_'+old);d=json.loads((prior/'DELIVERY.json').read_text());src=Path(d['master']);assert sha(src)==d['sha256']
 out=Path('/Users/benjaminoats/_desk/cache/J2016')/(ar+'_'+new);out.mkdir(parents=True,exist_ok=False)
 target=out/(src.stem.rsplit('_',1)[0]+'_'+new+'.mp4');cuts=json.loads((prior/'cuts.json').read_text());pool=json.loads((prior/'pool.json').read_text())
 meta=json.loads(run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',src]).stdout);n=int(meta['streams'][0]['nb_frames']);spec=m.SHORTS[ar];vo=m.dur(spec['wav']);tail=round(vo*30);caps=m.caption_track(m.load_words(spec['words']),vo);hook=m.hook_image(spec['hook'],spec['yellow']);title=m.title_image(spec['title']);ta,tb=spec['title_at'];tb=min(tb,round(vo-.08,3));stamp=m.credit_image(['2017','NASA/Aubrey Gemignani'])
 affected=([0,4,6] if ar=='ar1' else [1] if ar=='ar2' else [1,5]);movers={}
 for i in affected:
  asset=cuts[i]['framing']['actual_asset'];assert sha(asset['path'])==asset['sha256'];mov=m.Mover(Path(asset['path']));mov.im=m.lift_if_dark(mov.im);movers[i]=mov
  cuts[i]['framing']['J2016_transform']='Continuous subpixel translation at 0.15 output pixels/frame, fixed zoom; original source and overlay clocks retained'
  cuts[i]['framing'].pop('recipe',None);cuts[i]['framing'].pop('motion_recipe',None)
 # Explicit mappings preserve row boundaries; opening and preroll share motion time u.
 N=1080*1920*3;dec=subprocess.Popen(['ffmpeg','-v','error','-i',str(src),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE);picture=out/'picture.mp4';enc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p',str(picture)],stdin=subprocess.PIPE)
 changed=[]
 for f in range(n):
  data=dec.stdout.read(N);assert len(data)==N;t=f/30;i=next((j for j,c in enumerate(cuts) if round(c['timeline_in']*30)<=f<round(c['timeline_out']*30)),None)
  if i in affected:
   mov=movers[i];z=cuts[i]['upscale'];local=(f-round(cuts[i]['timeline_in']*30))/30
   if ar=='ar1' and i in (0,6):
    u=1+t if i==0 else (f-tail)/30;cx=.46+(.15*30*u)/(z*mov.w);cy=.45
    fr=mov.frame(cx,cy,z).convert('RGBA');rgb,alpha,origin=m.rocklib.render_crop(u);sprite=m.rocklib.paste_full(rgb,alpha,origin)
    # Subpixel position removes integer truncation while retaining the original path.
    dx=-260+150*u;sprite=sprite.transform(sprite.size,Image.AFFINE,(1,0,-dx,0,1,-40),Image.BICUBIC);fr.alpha_composite(sprite)
   else:
    cx,cy=({('ar1',4):(.50,.45),('ar2',1):(.46,.50),('ar3',1):(.56,.48),('ar3',5):(.4169,.50)})[(ar,i)]
    if ar=='ar3' and i==5:
     z=1920/mov.h;cuts[i]['upscale']=z
    cx+=.15*30*local/(z*mov.w);fr=mov.frame(cx,cy,z).convert('RGBA')
   if f<tail:
    for ov in cuts[i].get('overlays',[]):
     if ov['timeline_in']<=t<ov['timeline_out']:
      frames=sorted(Path(ov['sequence']).parent.glob('frame_*.png'));fr.alpha_composite(m.load_graphic(frames,t-ov['timeline_in']));break
    if t<2:fr.alpha_composite(hook)
    if ta<=t<tb:fr.alpha_composite(title)
    for a,b,cap in caps:
     if a<=t<b:fr.alpha_composite(cap);break
   data=fr.convert('RGB').tobytes();changed.append(f)
  enc.stdin.write(data)
  if f%60==0:print(ar,f,n,flush=True)
 enc.stdin.close();assert enc.wait()==0;assert dec.wait()==0
 run(['ffmpeg','-v','error','-n','-i',picture,'-i',src,'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',target]);assert ah(src)==ah(target);assert sha(src)==d['sha256']
 for i in affected:cuts[i]['framing']['J2016_transform']+='; native 30 fps rock rotation and fractional x translation' if ar=='ar1' and i in (0,6) else ''
 (ev/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n');(ev/'pool.json').write_text(json.dumps(pool,indent=2)+'\n')
 receipt={'job':'J2016','master':str(target),'sha256':sha(target),'source':str(src),'source_sha256':sha(src),'audio_packet_hash_before':ah(src),'audio_packet_hash_after':ah(target),'frames':n,'changed_rows':affected,'audio_listened':False,'moving_video_viewed':False,'status':'technical candidate only; not approved','gates':{}}
 (ev/'DELIVERY.json').write_text(json.dumps(receipt,indent=2)+'\n')
 base=json.loads((A/'J1468_evidence/DELIVERY.json').read_text())[int(ar[-1])-1];py=sys.executable
 cmds={'picture_complete_metadata':[py,R/'scripts/picture_qa.py',target,'--cuts',ev/'cuts.json','--pool',ev/'pool.json','--out-dir',ev/'picture_complete_metadata'],'polish_complete_metadata':[py,R/'scripts/polish_gate.py',target,'--cuts',ev/'cuts.json','--out',ev/'polish_complete_metadata.json'],'shorts_gate':[py,R/'00_Brand/Channel-Setup/tools/gate_shorts_open.py','check',target,'--vo',base['stems']['stem_vo.wav'],'--script',A/'02_Voiceover'/f'{ar}_locked_v01.txt','--json','--sheet-dir',out/'shorts_gate'],'music_gate':[py,R/'scripts/music_gate.py',A,'--bed',A/'05_Music/owb-standalone-shorts_score_bed_v01.mp3','--video',target,'--out',ev/'music_gate.json'],'sfx_level':[py,R/'scripts/sfx_kit.py','level','--vo',base['stems']['stem_vo.wav'],'--sfx',base['stems']['stem_sfx.wav'],'--bed',base['stems']['stem_bed.wav'],'--minutes',base['seconds']/60,'--out',ev/'sfx_level.json']}
 for name,c in cmds.items():receipt['gates'][name]=gate(name,c,ev);(ev/'DELIVERY.json').write_text(json.dumps(receipt,indent=2)+'\n')
 lm=loop_metrics(target);lp={k:v for k,v in lm.items() if k not in ('steps','frames_arr')}
 try:finish_scan(target,lm);lp['finish_result']='PASS'
 except SystemExit as ex:lp['finish_result']='FAIL';lp['reason']=str(ex)
 (ev/'loop.json').write_text(json.dumps(lp,indent=2)+'\n');print(ar,'complete',lp['finish_result'],flush=True)
if __name__=='__main__':
 for args in [('ar2','v11','v12'),('ar3','v08','v10'),('ar1','v04','v05')]:build(*args)
