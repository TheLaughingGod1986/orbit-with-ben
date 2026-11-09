import pathlib,subprocess as sp,numpy as np,json
from faster_whisper import WhisperModel
R=pathlib.Path('/Users/benjaminoats/YouTube/orbit-with-ben');O=R/'02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports';E=pathlib.Path('/private/tmp/j0989-evidence')
def pcm(v,sr=48000):return np.frombuffer(sp.check_output(['ffmpeg','-v','error','-i',str(O/f'030_apophis_short_{v}.mp4'),'-ar',str(sr),'-ac','1','-f','f32le','-']),dtype=np.float32)
a=pcm('v13');b=pcm('v13a');N=min(len(a),len(b));a=a[:N];b=b[:N]
# Search alignment over +/- 50 ms, using downsampling only for candidate selection.
rows=[]
for t in [0,3,6,9,12,15]:
 st=int((t+.1)*48000);en=min(N-2400,st+48000);x=a[st:en:8];scores=[]
 for lag in range(-2400,2401,8):
  y=b[st+lag:en+lag:8];scores.append(float(np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)+1e-12)))
 lag=range(-2400,2401,8)[int(np.argmax(scores))];rows.append({'time_s':t,'lag_samples':lag,'correlation':max(scores)})
assert all(r['lag_samples']==0 for r in rows),rows
rat=[]
for st in range(0,N-4800,4800):
 x=a[st:st+4800];y=b[st:st+4800];r=float(np.sqrt(np.mean(y*y))/(np.sqrt(np.mean(x*x))+1e-9));rat.append(20*np.log10(r+1e-9))
(E/'audio_alignment.json').write_text(json.dumps({'windows':rows,'gain_db_100ms_min':min(rat),'gain_db_100ms_max':max(rat),'sample_counts':{'old':len(pcm('v13')),'new':len(pcm('v13a'))},'note':'No alignment change at 8-sample search resolution. Original stems preserved; normalisation may change common mix gain.'},indent=2))
model=WhisperModel('small.en',device='cpu',compute_type='int8')
audio=pcm('v13a',16000)
segs,_=model.transcribe(audio,language='en',beam_size=5,temperature=0,condition_on_previous_text=False)
text=' '.join(s.text.strip() for s in segs)
(E/'asr_full.txt').write_text(text+'\n');print(text,flush=True)
print(rows,flush=True)
