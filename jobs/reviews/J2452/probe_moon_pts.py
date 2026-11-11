import json,subprocess,pathlib
base=pathlib.Path('/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/07_Edit-Project/parts/_work_full_v04')
rows=[];t=0
for line in (base/'final_j.txt').read_text().splitlines():
 p=base/pathlib.Path(line.split("'")[1]).name
 j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
 d=float(j['format']['duration']);rows.append(dict(file=str(p),concat_start_s=t,format_duration_s=d,streams=[{k:s.get(k) for k in ['codec_type','start_time','duration','time_base','nb_frames','sample_rate']} for s in j['streams']]))
 t+=d
out=pathlib.Path('/Users/ben/_desk/J2452-sleep-scratch/moon_pts_v01.json');out.write_text(json.dumps(dict(parts=rows,concat_duration_s=t),indent=2)+'\n');print(out);print(json.dumps(rows,indent=2))
