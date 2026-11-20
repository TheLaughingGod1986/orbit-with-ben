#!/usr/bin/env python3
"""Mix original candidate score underneath locked VO, retaining picture packets."""
import argparse,json,pathlib,re,subprocess,traceback
from score_candidate import sha

def run(args,log):
 with log.open('w') as f:subprocess.run(args,stdout=f,stderr=f,check=True)

def loudness(src,log):
 run(['ffmpeg','-nostats','-hide_banner','-i',str(src),'-vn','-af','loudnorm=print_format=json','-f','null','-'],log)
 return json.loads(re.findall(r'{[^{}]*"input_i"[^{}]*}',log.read_text(),re.S)[-1])

def packet_hash(src):
 return subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()

def main():
 p=argparse.ArgumentParser();p.add_argument('--media',type=pathlib.Path,required=True);p.add_argument('--done',type=pathlib.Path,required=True);a=p.parse_args();code=1
 try:
  root=a.media; src=root/'07_Edit/picture_polish_v02/atlantic_picture_polish_DRAFT_v02.mp4'
  evidence=json.loads((src.parent/'TECHNICAL_CHECK.json').read_text())
  if sha(src)!=evidence['sha256']:raise ValueError('Picture source changed')
  score=root/'05_Music/original_score_candidate_v01/atlantic_original_score_candidate_v01.wav'
  provenance=json.loads((score.parent/'SCORE_PROVENANCE.json').read_text())
  if sha(score)!=provenance['sha256']:raise ValueError('Score source changed')
  out=root/'07_Edit/score_mix_candidate_v03';out.mkdir(exist_ok=False)
  vo=loudness(src,out/'voice_loudness.log');bed=loudness(score,out/'raw_score_loudness.log')
  # Bed 16 LU beneath original VO. Constant gain preserves VO timing/phrasing.
  bed_gain=float(vo['input_i'])-16-float(bed['input_i'])
  quiet=out/'atlantic_score_under_vo_v01.wav'
  run(['ffmpeg','-v','error','-n','-i',str(score),'-af',f'volume={bed_gain}dB','-c:a','pcm_s24le',str(quiet)],out/'score_gain.log')
  dst=out/'atlantic_score_mix_CANDIDATE_v03.mp4'
  filt='[0:a]volume=2dB[vo];[1:a]volume=2dB[bed];[vo][bed]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.891251:level=false:latency=true,atrim=duration=1443.04[a]'
  run(['ffmpeg','-v','error','-n','-i',str(src),'-i',str(quiet),'-filter_complex',filt,'-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',str(dst)],out/'mix.log')
  run(['ffmpeg','-v','error','-i',str(dst),'-f','null','-'],out/'decode.log')
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(dst)]))
  v=next(s for s in probe['streams'] if s['codec_type']=='video')
  if (v['width'],v['height'],int(v['nb_read_frames']),v['avg_frame_rate'])!=(1920,1080,36076,'25/1'):raise ValueError('Picture format/count changed')
  vh=packet_hash(src)
  if vh!=packet_hash(dst):raise ValueError('Picture packets changed')
  mixed=loudness(dst,out/'mix_loudness.log');q=loudness(quiet,out/'bed_loudness.log')
  if float(mixed['input_tp'])>-.8:raise ValueError('Mix peak exceeded headroom')
  report={'state':'technical_checks_complete_perceptual_review_required','video':str(dst),'sha256':sha(dst),'picture_source_sha256':evidence['sha256'],'score_source_sha256':provenance['sha256'],'duration_s':float(probe['format']['duration']),'frames':36076,'fps':25,'picture_packets_unchanged':True,'decode':'success','source_voice_lufs':float(vo['input_i']),'bed_lufs':float(q['input_i']),'bed_below_voice_lu':float(vo['input_i'])-float(q['input_i']),'voice_gain_db':2,'bed_gain_db':bed_gain,'mix_loudness':mixed,'audio_perception':False,'moving_video_perception':False,'approval':False,'pending':['Listen to original score and mix for fit, fatigue, transitions and speech clarity','Watch all motion, pacing and labels; fix low-contrast carrier label','Reconcile voice review PR1014','Complete channel quality review before Ben watch']}
  (out/'TECHNICAL_CHECK.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True);code=0
 except Exception:traceback.print_exc()
 finally:a.done.write_text(str(code)+'\n')
 return code
if __name__=='__main__':raise SystemExit(main())
