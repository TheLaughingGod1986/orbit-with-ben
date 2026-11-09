import subprocess as sp,json,hashlib,pathlib,shutil
R=pathlib.Path('/Users/benjaminoats/YouTube/orbit-with-ben'); O=R/'02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports'; E=pathlib.Path('/private/tmp/j0989-evidence'); E.mkdir(exist_ok=True)
a=O/'030_apophis_short_v13.mp4'; b=O/'030_apophis_short_v13a.mp4'
def run(args): return sp.run(list(map(str,args)),capture_output=True,text=True,check=True)
assert hashlib.sha256(a.read_bytes()).hexdigest()=='2b276eb295dffbf4df0e81d874bce98295cfc8a3b94b4e6da945b162b5898abd'
assert not b.exists()
f='loudnorm=I=-14:TP=-2.3:LRA=11'
s=run(['ffmpeg','-hide_banner','-nostats','-i',a,'-af',f+':print_format=json','-f','null','-']).stderr
(E/'normalise_pass1.txt').write_text(s); m=json.loads(s[s.rindex('{'):s.rindex('}')+1])
f+=f":measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
# Dynamic normalization engages only as required by the peak constraint; no timing changes.
run(['ffmpeg','-nostdin','-v','error','-i',a,'-map','0:v:0','-map','0:a:0','-c:v','copy','-af',f+',aresample=48000','-c:a','aac','-b:a','320k','-ar','48000','-ac','2','-movflags','+faststart',b])
(E/'audio_filter.txt').write_text(f+'\n')
for label,p in [('v13',a),('v13a',b)]:
 (E/(label+'_ffprobe.json')).write_text(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',p]).stdout)
 (E/(label+'_frames.md5')).write_text(run(['ffmpeg','-v','error','-i',p,'-map','0:v:0','-f','framemd5','-']).stdout)
 (E/(label+'_audio.txt')).write_text(run(['ffmpeg','-nostats','-i',p,'-af','ebur128=peak=true','-f','null','-']).stderr)
assert (E/'v13_frames.md5').read_bytes()==(E/'v13a_frames.md5').read_bytes()
old=json.loads((O/'030_apophis_short_v13_meta.json').read_text());old['job']='J0989';old['version']='v13a';old['file']=str(b.relative_to(R));old['sha256']=hashlib.sha256(b.read_bytes()).hexdigest();old['audio_correction']='Audio-only two-pass loudnorm; video stream copied. See J0989 evidence.'
for suffix in ['cuts.json','pool.json']:
 shutil.copy2(O/('030_apophis_short_v13_'+suffix),O/('030_apophis_short_v13a_'+suffix))
shutil.copytree(O/'030_apophis_short_v13_stems',O/'030_apophis_short_v13a_stems')
old['audio']['stems']['vo']=str((O/'030_apophis_short_v13a_stems/stem_vo.wav').relative_to(R))
(O/'030_apophis_short_v13a_meta.json').write_text(json.dumps(old,indent=2)+'\n')
shutil.copy2(b,O/'030_apophis_short_v13a_PHONE.mp4')
print('BUILD COMPLETE',old['sha256'],flush=True)
print((E/'v13a_audio.txt').read_text()[-600:])
