#!/usr/bin/env python3
"""032 transparent teaching overlays, draft v01. Preview before Chief frame review.

No source image is modified. Composite these over approved graded moving plates.
Animation lasts 3.6 s: 0.4 s entry, 2.8 s hold, 0.4 s exit. The full-frame
preview background is illustrative only and MUST NOT enter the edit.
This first batch covers WHO, WHEN and FACT only; mechanism/DATA builds remain.
Run with the studio graphics venv. --render writes alpha-preserving MOVs only
for the individually named --approved ids (Chief review reference required).
"""
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
W,H,FPS,SECONDS=1920,1080,30,3.6
FONT='/Library/Fonts/Roboto-Bold.ttf'
REGULAR='/Library/Fonts/Roboto-Regular.ttf'
GOLD=(255,207,64,255); WHITE=(249,248,243,255)
SPECS=[
 {'id':'r07_who','row':7,'type':'WHO','lines':['Christiaan Huygens','1629–1695 · Dutch astronomer'],'source_rows':[17]},
 {'id':'r10_who','row':10,'type':'WHO','lines':['Gerard Kuiper','1905–1973 · Dutch-born astronomer'],'source_rows':[17]},
 {'id':'r07_when','row':7,'type':'WHEN','lines':['25 MARCH 1655'],'source_rows':[2],'year':1655},
 {'id':'r10_when','row':10,'type':'WHEN','lines':['1944'],'source_rows':[4],'year':1944},
 {'id':'r12_when','row':12,'type':'WHEN','lines':['NOVEMBER 1980'],'source_rows':[5],'year':1980},
 {'id':'r15_when','row':15,'type':'WHEN','lines':['14 JANUARY 2005'],'source_rows':[7],'year':2005},
 {'id':'r33_when','row':33,'type':'WHEN','lines':['2013'],'source_rows':[12],'year':2013},
 {'id':'r48_when','row':48,'type':'WHEN','lines':['NET JULY 2028'],'source_rows':[16],'year':2028},
 {'id':'r49_when','row':49,'type':'WHEN','lines':['LATE 2034'],'source_rows':[16],'year':2034},
 {'id':'r20_fact','row':20,'type':'FACT','lines':['WATER ICE IS ROCK'],'source_rows':[8]},
 {'id':'r23_fact','row':23,'type':'FACT','lines':['MOST DISTANT LANDING'],'source_rows':[7]},
 {'id':'r41_fact','row':41,'type':'FACT','lines':['NO OXYGEN TO BURN'],'source_rows':[14]},
 {'id':'r47_fact','row':47,'type':'FACT','lines':['IDEAL WAY TO TRAVEL'],'source_rows':[15]},
]
DATES=sorted([s for s in SPECS if 'year' in s],key=lambda s:s['year'])
def font(size,regular=False):return ImageFont.truetype(REGULAR if regular else FONT,size)
def frame(spec,t):
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    opacity=max(0,min(1,t/.4,(SECONDS-t)/.4))
    slide=round(28*(1-opacity));x=120;y=810+slide
    # No slab; shadow follows glyphs only.
    for n,line in enumerate(spec['lines']):
        f=font(66 if n==0 else 43,n>0)
        d.text((x,y+n*85),line,font=f,fill=GOLD if n==0 else WHITE,stroke_width=3,stroke_fill=(20,28,42,220))
    if spec['type']=='WHEN':
        left,right,ty=120,1770,970
        d.line((left,ty,right,ty),fill=(235,239,247,160),width=3)
        for s in DATES:
            if s['year']>spec['year']:break
            xx=left+(right-left)*(s['year']-1655)/(2034-1655)
            # Actual linear date spacing. Dense modern dates are deliberately not labelled
            # again here; the current date is in the large call-out above.
            d.ellipse((xx-7,ty-7,xx+7,ty+7),fill=GOLD if s==spec else WHITE)
    if opacity<1:im.putalpha(im.getchannel('A').point(lambda a:round(a*opacity)))
    return im

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--approved',nargs='*',default=[]);ap.add_argument('--review-ref');a=ap.parse_args()
    if a.render and (not a.approved or not a.review_ref):ap.error('Render requires named approved ids and Chief review reference')
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);manifest=[]
    sheet=Image.new('RGB',(960,240*math.ceil(len(SPECS)/2)),(32,45,65));sd=ImageDraw.Draw(sheet)
    for i,s in enumerate(SPECS):
        name='code_graphic_032_'+s['id']+'_v01';preview=out/(name+'.png');frame(s,1.8).save(preview)
        tile=Image.new('RGBA',(W,H),(40,58,79,255));tile.alpha_composite(frame(s,1.8));tile=tile.convert('RGB');tile.thumbnail((480,270))
        # Crop to teaching area so text is reviewable on contact sheet.
        tile=Image.new('RGBA',(W,400),(40,58,79,255));tile.alpha_composite(frame(s,1.8),(0,-700));tile=tile.convert('RGB').resize((480,100))
        x=(i%2)*480;y=(i//2)*240;sheet.paste(tile,(x,y+45));sd.text((x+12,y+12),s['id']+' · '+s['type'],fill='white')
        rec={**s,'preview':str(preview),'preview_sha256':hashlib.sha256(preview.read_bytes()).hexdigest(),'duration':SECONDS,'status':'RENDERED_UNDER_REVIEW_REF_NOT_COMPOSITED' if a.render and s['id'] in a.approved else 'DRAFT_REQUIRES_CHIEF_FRAME_REVIEW','needs_background':'approved graded moving real plate','alpha':True}
        if a.render and s['id'] in a.approved:
            dest=out/(name+'.mov');cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgba','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-an','-c:v','qtrle',str(dest)]
            proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
            try:
                for j in range(round(SECONDS*FPS)):proc.stdin.write(frame(s,j/FPS).tobytes())
                proc.stdin.close()
                if proc.wait():raise RuntimeError('ffmpeg render failed')
            except BaseException:proc.kill();raise
            rec.update(render=str(dest),review_ref=a.review_ref,sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
        manifest.append(rec)
    sheet.save(out/'teaching_previews.jpg',quality=95)
    (out/'OVERLAY_MANIFEST_v01.json').write_text(json.dumps({'status':'DRAFT','job':'J2089','font':FONT,'clips':manifest,'not_implemented':['all DATA/mechanism graphics','R26 airmix fallback','R46 lift_28x fallback']},indent=2)+'\n')
if __name__=='__main__':main()
