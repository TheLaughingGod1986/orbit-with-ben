#!/usr/bin/env python3
"""024 Light Speed v05 audio (J0129 items 6-7, the Chief's v04 FAIL #99 6097002634), on the v05 picture.
- The bed's 3:48-4:13 hush rides +3 dB (3 s ramps), so it stays a hush but is audible.
- ebur128 short-term (3 s) loudness of the VO and the bed as laid; while the VO runs, the bed must sit >= 10 LU under it in
  every window where the VO runs (half the window or more inside words). Where it doesn't, the bed is ridden down by the
  shortfall (+0.5 LU margin, held across the 3 s window, 0.5 s smoothing), measured again, up to six passes, at most
  12 dB in all.
- Mix to -14 LUFS (two-pass loudnorm, linear), true peak <= -1.0 dBTP, muxed onto the v05 picture; phone copy to OWB UAT.
Writes full_rough_v05_pack/audio_v05.json and audio_windows_v05.json.
  python3 _mix_light_speed_v05_audio.py [--measure-only]"""
from pathlib import Path
import json, re, shutil, subprocess as sp, sys
import numpy as np
HERE=Path(__file__).resolve().parent; EP=HERE.parent
WORK=Path('/private/tmp/light024_full_work_v05'); PACK=HERE/'full_rough_v05_pack'
VO=EP/'02_Voiceover/light_speed_vo_v01.mp3'; BED=EP/'05_Music/light-speed_score_bed_v01_full.mp3'
OUT=Path('/private/tmp/024_LightSpeed_full_rough_v05.mp4')
UAT=Path.home()/'Library/Mobile Documents/com~apple~CloudDocs/OWB UAT'; PHONE=UAT/'024_LightSpeed_v05_PHONE.mp4'
SR=48000; LAST_WORD=487.544; HOLD=2.5; FADE=1.0; FPS=30; TOTAL=round((LAST_WORD+HOLD+FADE)*FPS)/FPS
BED_VOL=0.095; HUSH=(228.0,253.0); HUSH_DB=3.0; RAMP=3.0; GAP_LU=10.0; MARGIN=0.5; MAX_DUCK=12.0
words=json.loads((EP/'02_Voiceover/words.json').read_text())['words']

def ff(*a):
 p=sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*map(str,a)],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-4000:])
def decode(src,extra=''):
 af=f'atrim=0:{TOTAL},asetpts=PTS-STARTPTS,apad=whole_dur={TOTAL}'+extra
 raw=sp.run(['ffmpeg','-v','error','-i',str(src),'-af',af,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True).stdout
 return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
def write(x,dst):
 sp.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-c:a','pcm_s24le',str(dst)],input=x.astype(np.float32).tobytes(),check=True)
def short_term(wav):
 """lavfi.r128.S (3 s window) every 100 ms, as (t, LUFS)."""
 txt=WORK/f'{Path(wav).stem}_S.txt'
 sp.run(['ffmpeg','-v','error','-i',str(wav),'-af',f'ebur128=metadata=1,ametadata=print:key=lavfi.r128.S:file={txt}','-f','null','-'],check=True)
 t=[];s=[]
 for a,b in re.findall(r'pts_time:([\d.]+)\s+lavfi\.r128\.S=([-\d.inf]+)',txt.read_text()):
  t.append(float(a));s.append(float(b) if 'inf' not in b else -120.0)
 return np.array(t),np.array(s)
def speaking(t):
 """True where the VO runs: at least half of the 3 s window ending at t is inside words."""
 st=np.array([w['start'] for w in words]);en=np.array([w['end'] for w in words])
 return np.array([float(np.clip(np.minimum(en,x)-np.maximum(st,x-3.0),0,None).sum())>=1.5 for x in t])
def gaps(vo_wav,bed_wav):
 tv,sv=short_term(vo_wav);tb,sb=short_term(bed_wav)
 n=min(len(tv),len(tb));t=tv[:n];d=sv[:n]-sb[:n];on=speaking(t)&(t>=3.0)
 return t,sv[:n],sb[:n],d,on

T=np.arange(int(TOTAL*SR))/SR
vo=decode(VO);write(vo,WORK/'vo_laid.wav')
bed=decode(BED,f',volume={BED_VOL},afade=t=out:st={TOTAL-FADE-1.5:.3f}:d={FADE+1.5}')
up=10**(HUSH_DB/20)-1
ride=1+up*np.clip(np.minimum((T-HUSH[0])/RAMP,(HUSH[1]-T)/RAMP)+1,0,1)*((T>HUSH[0]-RAMP)&(T<HUSH[1]+RAMP))
bed*=ride[:,None]
write(bed,WORK/'bed_rode.wav')
t,sv,sb,d,on=gaps(WORK/'vo_laid.wav',WORK/'bed_rode.wav')
before=dict(windows=int(on.sum()),under=int((on&(d<GAP_LU)).sum()),min_gap=round(float(d[on].min()),2))
grid=t.copy();duck=np.zeros_like(grid);k=int(0.5*SR);rode=bed
for _ in range(6):  # measure, add the shortfall, measure again
 cut=np.where(on,np.clip(GAP_LU+MARGIN-d,0,None),0.0)
 if not cut.any():break
 held=np.array([cut[max(0,i-30):i+1].max() for i in range(len(cut))])  # a window ending at t covers t-3..t: duck all of it
 duck=np.minimum(duck+np.interp(grid,t,held,left=0,right=0),MAX_DUCK)
 env_db=np.convolve(np.interp(T,grid,duck,left=0,right=0),np.ones(k)/k,mode='same')
 bed=rode*(10**(-env_db/20))[:,None]
 write(bed,WORK/'bed_ducked.wav')
 t,sv,sb,d,on=gaps(WORK/'vo_laid.wav',WORK/'bed_ducked.wav')
after=dict(windows=int(on.sum()),under=int((on&(d<GAP_LU)).sum()),min_gap=round(float(d[on].min()),2),
 max_duck_db=round(float(env_db.max()),2),ducked_seconds=round(float((env_db>0.5).sum()/SR),1))
bad=[dict(t=round(float(x),1),gap=round(float(g),2)) for x,g,o in zip(t,d,on) if o and g<GAP_LU]
(PACK/'audio_windows_v05.json').write_text(json.dumps(dict(gate_lu=GAP_LU,before=before,after=after,under_after=bad[:200],
 windows=[dict(t=round(float(x),1),vo=round(float(a),2),bed=round(float(b),2),gap=round(float(g),2),vo_on=bool(o)) for x,a,b,g,o in zip(t[::10],sv[::10],sb[::10],d[::10],on[::10])]),indent=1))
print('before',before);print('after',after)
if '--measure-only' in sys.argv:sys.exit(0)

mix='[0:a][1:a]amix=inputs=2:duration=first:normalize=0'
first=sp.run(['ffmpeg','-hide_banner','-i',str(WORK/'vo_laid.wav'),'-i',str(WORK/'bed_ducked.wav'),'-filter_complex',mix+',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]','-map','[a]','-f','null','-'],capture_output=True,text=True).stderr
st=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',first,re.S)[-1])
norm=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true"
ff('-i',WORK/'vo_laid.wav','-i',WORK/'bed_ducked.wav','-filter_complex',mix+','+norm+'[a]','-map','[a]','-ar','48000','-c:a','aac','-b:a','192k',WORK/'audio_v05b.m4a')
ff('-i',WORK/'picture.mp4','-i',WORK/'audio_v05b.m4a','-map','0:v','-map','1:a','-c','copy','-t',TOTAL,'-movflags','+faststart',OUT)
ll=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
lufs=float(re.findall(r'I:\s*([-\d.]+) LUFS',ll)[-1]);tp=float(re.findall(r'Peak:\s*([-\d.]+) dBFS',ll)[-1])
ff('-i',OUT,'-c:v','libx264','-profile:v','high','-preset','medium','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',WORK/PHONE.name)
PHONE.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(WORK/PHONE.name,PHONE)
res=dict(out=str(OUT),phone=str(PHONE),bed=BED.name,bed_volume=BED_VOL,hush=dict(span=HUSH,plus_db=HUSH_DB,ramp_s=RAMP),
 gate=dict(lu=GAP_LU,before=before,after=after),integrated_lufs=lufs,true_peak_dbtp=tp,
 lufs_pass=abs(lufs+14)<=0.5,tp_pass=tp<=-1.0,gate_pass=after['under']==0)
(PACK/'audio_v05.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=1))
