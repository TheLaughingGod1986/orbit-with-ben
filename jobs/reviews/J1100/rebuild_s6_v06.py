"""Rebuild only S6's silent tail from the pre-caption plate; preserve accepted AAC."""
import sys,json,subprocess,hashlib,shutil,importlib.util
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from finish_j1100_s2_v05 import ff,sha,dump
base=Path('/Users/benjaminoats/_desk/renders')
key='S6_028_X768qs8sNQs'
src=base/'J1100-S6-final02'/key/(key+'_v05.mp4')
raw=base/'J1100-S6-raw02'/key
work=Path('/private/tmp/j1100_s6_02_'+key)
out=Path('/private/tmp/J1100-v06')/key
out.mkdir(parents=True,exist_ok=True)
assert shutil.disk_usage('/private/tmp').free>20_000_000_000
prep=json.loads((raw/'locked_preparation.json').read_text())
end=round(prep['vo_splice_map']['vo_end_s']*30)
frames=round(prep['vo_splice_map']['total_duration_s']*30)
assert frames-end==30
# Use the actual uncaptained composed picture. No removal, inpainting or reuse of a captioned frame.
fc=f'[0:v]trim=end_frame={end},setpts=N/(30*TB)[b];[1:v]noise=alls=4:allf=t:all_seed=1032,split=3[r0][s0][e0];[r0]trim=end_frame=30,reverse,trim=end_frame=25,setpts=N/(30*TB)[r];[s0]trim=start_frame=2:end_frame=3,loop=loop=3:size=1:start=0,trim=end_frame=4,setpts=N/(30*TB)[s];[e0]trim=end_frame=1,setpts=N/(30*TB)[e];[b][r][s][e]concat=n=4:v=1:a=0,format=yuv420p[v]'
final=out/(key+'_v06.mp4')
assert not final.exists(), 'Never overwrite an existing output'
ff(['-i',src,'-i',work/'picture.mp4','-filter_complex',fc,'-map','[v]','-map','0:a','-frames:v',frames,'-c:v','libx264','-preset','fast','-crf','18','-c:a','copy','-movflags','+faststart',final])
ff(['-i',final,'-vf','scale=720:1280:flags=lanczos','-c:v','libx264','-preset','fast','-crf','20','-c:a','copy',out/(key+'_v06_PHONE.mp4')])
def ah(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
assert ah(src)==ah(final)
record=json.loads((src.parent/'FINISH_COMPLETE.json').read_text())
record.update(status='UNREVIEWED v06; caption-free tail; gates and Gemini listening outstanding',input_sha256=sha(src),tail_source_sha256=sha(work/'picture.mp4'),tail_start_frame=end,aac_packets_unchanged=True,files={p.name:sha(p) for p in out.glob('*.mp4')})
spec=importlib.util.spec_from_file_location('legacy', '/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/mon30_comets/_assemble_mon30_comets_v03.py')
legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
record['loop']=legacy.loop_measures(final)
record['loop_pass']=max(record['loop'].values())<2
record['I_LUFS'],record['TP_dBTP']=legacy.ebur128_stats(final)
record['endpoint']='caption-free original picture frames, reversed; no hook or spoken captions in tail'
record['inherited_v05_corrections']=record.pop('corrections',[])
dump(out/'FINISH_COMPLETE.json',record)
# Checker input metadata and symlink refer to accepted v05 stems, never copied/re-generated audio.
source=Path('/private/tmp/J1100-v06-source')/key
source.mkdir(parents=True,exist_ok=True)
for name in ['locked_preparation.json','input_hashes.json','stem_vo.wav','stem_bed.wav','stem_sfx.wav']:
 (source/name).symlink_to(raw/name)
(source/final.name).symlink_to(src)
print(final,flush=True)
