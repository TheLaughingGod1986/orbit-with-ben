"""Frame stills and sheets for full_rough_v03_pack from the rendered v03 (no re-render).
Same layout as the v02 pack; adds full-size grabs of row 43c for the lat/long grid check.
usage: python3 _sheets_venus_full_v03.py [pack_dir]"""
import json,math,subprocess as sp,sys,tempfile,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
PACK=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'full_rough_v03_pack'
OUT=Path.home()/'Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/023_Venus_full_rough_v03.mp4'
TOTAL=513.0;LAST_WORD=509.5
WORK=Path(tempfile.mkdtemp(prefix='venus_v03_sheets_'))
want=(PACK/'SHA256.txt').read_text().split()[0]
h=hashlib.sha256()
with OUT.open('rb') as f:
 for b in iter(lambda:f.read(1<<20),b''):h.update(b)
if h.hexdigest()!=want:raise SystemExit(f'sha mismatch {h.hexdigest()} != {want}')
def run(a):sp.run(['ffmpeg','-y','-loglevel','error',*map(str,a)],check=True)
cuts=json.loads((PACK/'cuts_v03.json').read_text())
frames=PACK/'frames';frames.mkdir(exist_ok=True)
def grab(t,dst,w=480):run(['-ss',f'{t:.3f}','-i',OUT,'-frames:v','1','-vf',f'scale={w}:{w*9//16}',dst])
tiles=[]
for k,c in enumerate(cuts):
 mid=(c['timeline_in']+c['timeline_out'])/2;dst=frames/f"row_{k:03}.jpg";grab(mid,dst);tiles.append((dst,f"{c['row']} {mid:.1f}s {c['source'][:22]}"))
def sheet(name,items,cols=6):
 rows_n=math.ceil(len(items)/cols);board=Image.new('RGB',(cols*320,rows_n*200),(18,18,22));d=ImageDraw.Draw(board)
 for i,(p,label) in enumerate(items):
  x=i%cols*320;y=i//cols*200;board.paste(Image.open(p).resize((320,180)),(x,y));d.text((x+6,y+182),label,fill='white')
 board.save(PACK/(name+'.jpg'),quality=90)
sheet('per_row_sheet_v03',tiles)
def tsheet(name,times):
 items=[]
 for i,t in enumerate(times):p=WORK/f'f_{name}_{i}.jpg';grab(t,p);items.append((p,f'{t:.2f}s'))
 sheet(name,items,cols=3)
tsheet('frame0_sheet',[0,.2,.4,.6,.8,1])
r51=[c for c in cuts if c['row']=='51'];r56=[c for c in cuts if c['row']=='56']
tsheet('sheet_rows_51_56',[r51[0]['timeline_in']+1,r51[0]['timeline_in']+3,r51[1]['timeline_in']+1,r51[1]['timeline_in']+2.5,
 r56[0]['timeline_in']+2,r56[1]['timeline_in']+1,r56[1]['timeline_in']+3,r56[1]['timeline_out']-0.5,TOTAL-0.5])
tsheet('sheet_cards_sub',[o['start']+1.0 for o in json.loads((PACK/'overlays_v03.json').read_text())])
tsheet('sheet_end',[LAST_WORD-1,LAST_WORD+0.5,LAST_WORD+1.5,LAST_WORD+2.5,TOTAL-0.5,TOTAL-0.05])
c43=[c for c in cuts if c['row']=='43c'][0]
for tag,t in (('in',c43['timeline_in']+0.5),('mid',(c43['timeline_in']+c43['timeline_out'])/2),('out',c43['timeline_out']-0.5)):
 grab(t,PACK/f'row_43c_{tag}_1920.jpg',w=1920)
print('frames',len(tiles),'pack',PACK)
