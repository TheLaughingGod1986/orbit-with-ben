#!/usr/bin/env python3
"""Conform checked sentence drafts to v02 timings and mux unchanged locked VO.
This is an unfinished editorial draft without music or perceptual QA.
"""
import argparse,hashlib,json,pathlib,subprocess,traceback
BATCHES=['early_v01','geography_v01','aircraft_v01','detection_v01','synthesis_v01','convoys_v01','carrier_v01','ending_v01']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd):subprocess.run([str(v) for v in cmd],check=True)
def main():
 p=argparse.ArgumentParser();p.add_argument('--media',required=True,type=pathlib.Path);p.add_argument('--done',required=True,type=pathlib.Path);a=p.parse_args();code=1
 try:
  edit=pathlib.Path(__file__).resolve().parent;old=json.loads((edit/'EDL_v01.json').read_text());new=json.loads((edit/'EDL_v02.json').read_text());expected={r['shot_id']:r for r in old['rows']};have={};checks=[]
  audio=a.media/'02_Voiceover/atlantic_black_pit_vo_v01.wav'
  if sha(audio)!=new['audio_sha256']:raise ValueError('Source VO hash mismatch')
  for batch in BATCHES:
   folder=a.media/'03_Picture/maps'/batch;m=json.loads((folder/'MANIFEST.json').read_text());check=json.loads((folder/'TECHNICAL_CHECK.json').read_text())
   if m['audio_sha256']!=new['audio_sha256']:raise ValueError('Stale batch voice')
   if sha(pathlib.Path(check['video']))!=check['sha256']:raise ValueError('Sequence hash mismatch')
   for r in m['rows']:
    if r['shot_id'] in have:raise ValueError('Duplicate sentence')
    for key in ['narration','picture_id','cut_start_s','cut_end_s']:
     if r[key]!=expected[r['shot_id']][key]:raise ValueError('Stale row '+r['shot_id'])
    path=pathlib.Path(r['video'])
    if sha(path)!=r['sha256']:raise ValueError('Clip hash mismatch')
    have[r['shot_id']]=r
   checks.append(check)
  for folder in sorted((a.media/'03_Picture/maps/early_layout_fixes_v01').glob('L010.*')):
   m=json.loads((folder/'MANIFEST.json').read_text())
   for r in m['rows']:
    if r['shot_id'] not in have or sha(pathlib.Path(r['video']))!=r['sha256']:raise ValueError('Invalid layout override')
    for key in ['narration','picture_id','cut_start_s','cut_end_s']:
     if r[key]!=expected[r['shot_id']][key]:raise ValueError('Stale layout override')
    have[r['shot_id']]=r
  required=[r for r in new['rows'] if r['line_id']!='L001']
  if set(have)!={r['shot_id'] for r in required}:raise ValueError('Missing or unexpected picture rows')
  if len({r['video'] for r in have.values()})!=len(have):raise ValueError('Reused clip path: caption collision')
  out=a.media/'07_Edit/full_draft_v01';out.mkdir(parents=True,exist_ok=True);conform=out/'conform';conform.mkdir(exist_ok=True)
  opening=a.media/'03_Picture/maps/M001/M001_opening_draft_v01.mp4';paths=[opening];records=[]
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(opening)]));frames0=int(probe['streams'][0]['nb_read_frames']);want0=round(required[0]['cut_start_s']*25)
  if frames0!=want0:raise ValueError('Opening does not meet first sentence frame')
  for r in required:
   src=have[r['shot_id']];path=pathlib.Path(src['video']);frames=round(r['cut_end_s']*25)-round(r['cut_start_s']*25)
   changed=frames!=src['frames']
   if changed:
    path=conform/(r['shot_id']+'.mp4');run(['ffmpeg','-v','error','-y','-i',src['video'],'-vf',f'tpad=stop_mode=clone:stop_duration=3,trim=end_frame={frames},setpts=PTS-STARTPTS','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',path])
   paths.append(path);records.append({'shot_id':r['shot_id'],'video':str(path),'frames':frames,'sha256':sha(path),'source_frames':src['frames'],'length_conformed':changed})
   print('CHECKED',r['shot_id'],frames,flush=True)
  frames=frames0+sum(r['frames'] for r in records);duration=frames/25
  if frames!=round(new['rows'][-1]['cut_end_s']*25):raise ValueError('Total frame mismatch')
  concat=out/'concat.txt';concat.write_text(''.join("file '"+str(path)+"'\n" for path in paths))
  video=out/'atlantic_full_editorial_DRAFT_v01.mp4'
  run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',concat,'-i',audio,'-map','0:v:0','-map','1:a:0','-c:v','copy','-af','apad=pad_dur=2','-c:a','aac','-b:a','192k','-t',duration,'-movflags','+faststart',video])
  run(['ffmpeg','-v','error','-i',video,'-f','null','-'])
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]));v=next(s for s in probe['streams'] if s['codec_type']=='video')
  if (v['width'],v['height'],int(v['nb_read_frames']))!=(1920,1080,frames):raise ValueError('Full draft dimensions or frames wrong')
  result={'state':'full_editorial_draft_no_music_no_perceptual_QA','video':str(video),'sha256':sha(video),'source_audio_sha256':new['audio_sha256'],'edl_sha256':sha(edit/'EDL_v02.json'),'duration_s':duration,'frames':frames,'fps':25,'width':1920,'height':1080,'sentence_rows':len(new['rows']),'opening_frames':frames0,'sentence_clips':records,'decode':'success','music':'absent','audio_perception':False,'moving_video_perception':False,'conform_method':'Trim or clone final picture frames to v02 length. Entire original narration muxed once, unedited; final 2 seconds padded silence. Animation timing is draft; no quality approval.','remaining':['Film-specific music and sound treatment','Editorial pacing and close-view/motion review','Capable full watch/listen quality pass','Reconcile voice review and final package','Chief decision and Ben watch submission']}
  (out/'TECHNICAL_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');(edit/'FULL_DRAFT_v01.json').write_text(json.dumps(result,indent=2)+'\n');print('COMPLETE',video,flush=True);code=0
 except Exception:traceback.print_exc()
 finally:a.done.parent.mkdir(parents=True,exist_ok=True);a.done.write_text(str(code)+'\n')
 return code
if __name__=='__main__':raise SystemExit(main())
