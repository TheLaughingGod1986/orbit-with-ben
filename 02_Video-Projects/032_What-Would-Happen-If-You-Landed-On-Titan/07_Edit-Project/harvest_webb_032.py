import urllib.request,hashlib,json
from pathlib import Path
from PIL import Image
out=Path('/Users/benjaminoats/_desk/cache/J2089/jwst_v01');out.mkdir(exist_ok=True)
page='https://science.nasa.gov/asset/webb/uranus-nircam-image/'
url='https://assets.science.nasa.gov/content/dam/science/missions/webb/science/2023/04/STScI-01GWQDPJTF1MY8ZGN4WBMWMACJ.png/jcr:content/renditions/Unannotated.png'
for name,u in [('nasa_source.html',page),('uranus_nircam_unannotated.png',url)]:
 with urllib.request.urlopen(u,timeout=40) as r: data=r.read()
 (out/name).write_bytes(data)
p=out/'uranus_nircam_unannotated.png'
with Image.open(p) as im:
 print(im.size);im.thumbnail((1200,1200));im.convert('RGB').save(out/'preview.jpg')
 imsize=Image.open(p).size
record={'asset_id':'weic2310a','row':52,'local_path':str(p),'source_page':page,'download_url':url,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'width':imsize[0],'height':imsize[1],'credit':'NASA, ESA, CSA, STScI, J. DePasquale (STScI)','licence':'CC BY 4.0','licence_source':'https://esawebb.org/copyright/','original_source':'https://esawebb.org/images/weic2310a/','review_status':'CANDIDATE_STILL_REVIEW_REQUIRED','motion_perception':'NOT_PERFORMED','source_evidence':str(out/'nasa_source.html')}
(out/'record.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
