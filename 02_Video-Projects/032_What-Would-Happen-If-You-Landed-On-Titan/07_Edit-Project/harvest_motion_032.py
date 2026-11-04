#!/usr/bin/env python3
"""Bounded download of two official candidates. Not a licence or motion review."""
import hashlib,json,subprocess,urllib.request
from pathlib import Path
OUT=Path('/Users/benjaminoats/_desk/cache/J2089/additional_v01');OUT.mkdir(exist_ok=True,parents=True)
INPUTS=[
 ('huygens_descent','https://archives.esac.esa.int/psa/ftp/CASSINI-HUYGENS/DISR/HP-SSA-DISR-2-3-EDR-RDR-V1.3/EXTRAS/MOVIES/TITAN_DESCENT_MOVIE/HUYGENS_MOVIE_HIRES_SILENT.WMV','https://archives.esac.esa.int/psa/ftp/CASSINI-HUYGENS/DISR/HP-SSA-DISR-2-3-EDR-RDR-V1.3/EXTRAS/MOVIES/TITAN_DESCENT_MOVIE/TITAN_DESCENT_MOVIE.TXT','ESA/NASA/JPL/University of Arizona', [1,16,51]),
 ('dragonfly_at_titan','https://dragonfly.jhuapl.edu/Gallery/files/videos/1080/DragonflyatTitan2025.mp4','https://dragonfly.jhuapl.edu/Gallery/','NASA/Johns Hopkins APL (confirm asset credit)',[5,37,44,45,47,48,49]),
]
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
records=[]
for aid,url,page,credit,rows in INPUTS:
 dest=OUT/(aid+Path(url).suffix.lower());r={'asset_id':aid,'download_url':url,'source_page':page,'credit':credit,'rows':rows,'review_status':'CANDIDATE_NOT_KEEP','licence_status':'PENDING_ASSET_SPECIFIC_TERMS','intervals':'UNSELECTED','motion_perception':'NOT_PERFORMED'}
 try:
  if not dest.exists():
   total=0
   with urllib.request.urlopen(url,timeout=45) as source,dest.with_suffix(dest.suffix+'.part').open('wb') as f:
    while True:
     b=source.read(1024*1024)
     if not b:break
     total+=len(b)
     if total>250*1024*1024:raise RuntimeError('250 MiB per-candidate limit exceeded')
     f.write(b)
   dest.with_suffix(dest.suffix+'.part').rename(dest)
  r.update(local_path=str(dest),sha256=digest(dest),bytes=dest.stat().st_size)
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)]));r['probe']=probe
  duration=float(probe['format']['duration']);r['duration']=duration
  r['candidate_stills']=[]
  for n,t in enumerate([duration*.2,duration*.5,duration*.8]):
   still=OUT/(aid+f'_sample_{n}.jpg');subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(dest),'-frames:v','1','-vf','scale=960:-2',str(still)],check=True)
   r['candidate_stills'].append({'time':t,'path':str(still)})
  r['download_status']='DOWNLOADED_AND_PROBED'
 except Exception as e:r['download_status']='ERROR';r['error']=str(e)
 records.append(r);(OUT/'MOTION_CANDIDATES_v01.json').write_text(json.dumps(records,indent=2)+'\n');print(aid,r['download_status'],r.get('error',''),flush=True)
