"""Reproduce full-frame loop failure without changing the gate or masking its result."""
from pathlib import Path
import subprocess,json,hashlib
src=Path('/Users/benjaminoats/_desk/renders/J1100-v06-preserved/S6_028_X768qs8sNQs/S6_028_X768qs8sNQs_v06.mp4')
out=Path('/Users/benjaminoats/_desk/reviews/J1100/loop_1031');out.mkdir(parents=True,exist_ok=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(src)]))
duration=float(probe['format']['duration'])
size=180*320
def seek(t):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{t:.3f}','-t','0.040','-i',str(src),'-vf','scale=180:320,format=gray','-f','rawvideo','-'])
 return raw[:size]
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-vf','scale=180:320,format=gray','-f','rawvideo','-'])
f=[raw[i:i+size] for i in range(0,len(raw),size)]
a,b=seek(.04),seek(duration-.08)
diff=[abs(x-y) for x,y in zip(a,b)]
bands=[]
for start in range(0,320,20):
 v=diff[start*180:(start+20)*180]
 bands.append({'rows':[start,start+20],'mean_abs_difference':sum(v)/len(v),'contribution_to_whole':sum(v)/size})
def mad(x,y):return sum(abs(i-j) for i,j in zip(x,y))/size
r={'input':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'duration':duration,'frames':len(f),'method':'Exact existing loop_measures seek/scale/gray commands; absolute signed difference over all pixels. No masked result substituted.','gate_whole':round(sum(diff)/size,2),'threshold':2.0,'gate_result':'FAIL','actual_first_last':mad(f[0],f[-1]),'horizontal_band_diagnostics':bands,'tail_neighbor_differences':[mad(f[i],f[i-1]) for i in range(len(f)-29,len(f))]}
(out/'measurement.json').write_text(json.dumps(r,indent=2)+'\n')
for t,name in [(.04,'opening'),(duration-.08,'tail')]:
 subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(src),'-frames:v','1','-vf','scale=360:640','-n',str(out/(name+'.png'))],check=True)
print(json.dumps(r,indent=2))
