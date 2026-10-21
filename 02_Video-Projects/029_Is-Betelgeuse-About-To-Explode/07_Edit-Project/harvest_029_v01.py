"""J0353: download only the pinned harvest sources; never generates media."""
import concurrent.futures as cf
import hashlib, json, re, subprocess, urllib.request
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parent
SHARED=Path('/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/harvest_v01')
SHARED.mkdir(parents=True,exist_ok=True)
boards=json.loads((ROOT/'PLATE_BOARDS_v02.json').read_text())
plates=[p for p in boards['plates'] if p['route']=='harvest']
assets={p['asset_id']:p for p in plates}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'OrbitWithBen/1.0 source verification'}),timeout=75) as r:return r.read()
def page_for(u):
    name=Path(urlparse(u).path).stem
    if 'images-assets.nasa.gov' in u:
        ident=u.split('/image/')[1].split('/')[0]; return 'https://images-api.nasa.gov/search?nasa_id='+ident
    if 'sdo.gsfc' in u:return 'https://sdo.gsfc.nasa.gov/data/rules.php'
    host= 'www.eso.org/public' if 'eso.org' in u else 'esahubble.org' if 'esahubble.org' in u else 'esawebb.org' if 'esawebb.org' in u else 'noirlab.edu/public'
    kind='videos' if Path(urlparse(u).path).suffix in ('.mp4','.m4v') else 'images'
    return f'https://{host}/{kind}/{name}/'
def one(item):
    aid,p=item; u=p['reference']; path=SHARED/(aid+Path(urlparse(u).path).suffix)
    out={'asset_id':aid,'source_url':u,'local_path':str(path),'plate_ids':[x['id'] for x in plates if x['asset_id']==aid],'credit':p.get('credit'),'board_licence':p.get('licence'),'source_page':page_for(u),'generation_authorized':False}
    try:
        if not path.exists():
            data=get(u); tmp=path.with_suffix(path.suffix+'.part'); tmp.write_bytes(data); tmp.rename(path)
        out['sha256']=hashlib.sha256(path.read_bytes()).hexdigest(); out['bytes']=path.stat().st_size
        if path.suffix in ('.mp4','.m4v'):
            probe=subprocess.run(['ffprobe','-v','quiet','-show_format','-show_streams','-of','json',str(path)],capture_output=True,text=True,check=True)
            out['probe']=json.loads(probe.stdout)
            thumb=SHARED/(aid+'_preview.jpg')
            subprocess.run(['ffmpeg','-v','error','-y','-ss','1','-i',str(path),'-frames:v','1',str(thumb)],check=True)
        else:
            from PIL import Image
            Image.MAX_IMAGE_PIXELS=400_000_000
            with Image.open(path) as im:out['width'],out['height']=im.size; im.verify()
        out['download_status']='downloaded'
    except Exception as e:out['download_status']='error';out['error']=str(e)
    try:
        raw=get(out['source_page']); evidence=SHARED/(aid+'_source.txt');evidence.write_bytes(raw)
        out['source_evidence_path']=str(evidence);out['source_evidence_sha256']=hashlib.sha256(raw).hexdigest()
        text=raw.decode('utf-8','replace')
        title=re.search(r'<title[^>]*>(.*?)</title>',text,re.S|re.I)
        out['page_title']=re.sub('<[^>]+>','',title.group(1)).strip() if title else None
        if 'images-api.nasa.gov' in out['source_page']:
            items=json.loads(text)['collection']['items'];out['nasa_metadata']=[v['data'] for v in items];out['page_title']=items[0]['data'][0].get('title') if items else None
        out['licence_mentions']=sorted(set(re.findall(r'.{0,90}(?:creativecommons.org|CC BY|public domain|copyright|[Uu]sage).{0,140}',text)))[:20]
    except Exception as e:out['metadata_error']=str(e)
    print(aid,out['download_status'],out.get('page_title'),out.get('metadata_error',''),flush=True)
    return out
if __name__=='__main__':
    with cf.ThreadPoolExecutor(max_workers=5) as ex: results=list(ex.map(one,assets.items()))
    (ROOT/'HARVEST_DOWNLOAD_v01.json').write_text(json.dumps({'job':'J0353','board_version':'v02','plate_count':len(plates),'generation_authorized':False,'assets':results,'plates':plates},indent=2)+'\n')
    (SHARED/'SHA256SUMS.txt').write_text(''.join(f"{a['sha256']}  {Path(a['local_path']).name}\n" for a in results if 'sha256'in a))
