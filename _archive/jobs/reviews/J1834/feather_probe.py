import subprocess,pathlib,importlib.util,json
p=pathlib.Path('/Users/benjaminoats/_desk/cache/J1834')
s=importlib.util.spec_from_file_location('gate','00_Brand/Channel-Setup/tools/gate_shorts_open.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
results=[]
for t in [4,5]:
 out=p/f'feather_candidate_T{540+t}.mp4'
 filt="[0:v]split=2[b][f];[b]crop=720:720:280:0,scale=1080:1080,pad=1080:1920:0:420,fillborders=top=420:bottom=420:mode=reflect,boxblur=30:3[bg];[f]crop=460:460:450:180,scale=1080:1080,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y,H-1-Y)/48)'[fg];[bg][fg]overlay=0:420,setsar=1[v]"
 cmd=['ffmpeg','-v','error','-ss',str(t),'-i',str(p/'crew2_540_600.mp4'),'-t','2.4','-filter_complex',filt,'-map','[v]','-an','-c:v','libx264','-preset','fast','-crf','18','-y',str(out)]
 subprocess.run(cmd,check=True); val=g.frame0_diff_0_1_5s(out);results.append({'T':540+t,'metric':val,'command':cmd}); print(results[-1],flush=True)
(p/'feather_metrics.json').write_text(json.dumps(results,indent=2))
