#!/usr/bin/env python3
"""Index NASA STS-125 footage and build R27 candidates. No motion review/KEEP.

Preserve the original plus catalog and NASA terms in --media-root first.
Never overwrite existing media. Run with /usr/bin/python3 (Pillow).
"""
import argparse
import io
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from harvest_solar import sha, run, probe


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--media-root',required=True,type=Path)
    ap.add_argument('--pool',required=True,type=Path)
    a=ap.parse_args(); root=a.media_root.resolve()
    src=root/'hubble_sm4_highlights.webm'; page=root/'svs13160.html'; terms=root/'NASA_MEDIA_TERMS.html'
    url=(root/'source_url.txt').read_text().strip()
    assert src.exists() and url.split('/')[-1] in page.read_text()
    assert 'educational or informational purposes' in terms.read_text()
    info=probe(src);vs=next(s for s in info['streams'] if s['codec_type']=='video')
    assert (vs['width'],vs['height'])==(1280,720)
    run(['ffmpeg','-v','error','-xerror','-i',str(src),'-map','0:v:0','-f','null','-'])
    # Real archival material is 4:3 pillarboxed within the published 16:9 file.
    # Keep the complete telescope; feather its sides into a blurred duplicate.
    mask=root/'feather_mask_v02.png'; credit=root/'NASA_credit.png'
    if mask.exists() or credit.exists(): raise FileExistsError('Output already exists')
    im=Image.new('L',(1440,1080));d=ImageDraw.Draw(im)
    for x in range(1440):
        d.line((x,0,x,1079),fill=int(255*min(1,x/56,(1439-x)/56)))
    im.save(mask)
    im=Image.new('RGBA',(1920,1080));d=ImageDraw.Draw(im)
    d.text((36,1024),'NASA',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',30),fill='white',stroke_width=1,stroke_fill=(10,15,25,200));im.save(credit)
    base='crop=960:720:160:0,split=2[fg][bg];[bg]scale=1920:1440:flags=lanczos,crop=1920:1080,boxblur=40:2[b];[fg]scale=1440:1080:flags=lanczos,setsar=1[f];[1:v]format=gray[m];[f][m]alphamerge[fa];[b][fa]overlay=240:0:shortest=1,eq=brightness=0.015:saturation=1.02,noise=alls=4:allf=t,fps=25[p];[p][2:v]overlay=0:0:shortest=1[out]'
    specs=[dict(key='approach',source_start=112.,duration=4.,film_start=272.94),dict(key='release',source_start=661.,duration=3.48,film_start=276.94)]
    plates=[]; sheet=Image.new('RGB',(1440,620),(29,35,49));sd=ImageDraw.Draw(sheet)
    for n,s in enumerate(specs):
        out=root/('plate_031_r27_'+s['key']+('_v03.mp4' if s['key']=='release' else '_v01.mp4'))
        cmd=['ffmpeg','-v','error','-n','-ss',str(s['source_start']),'-i',str(src),'-loop','1','-i',str(mask),'-loop','1','-i',str(credit),'-t',str(s['duration']),'-filter_complex',base,'-map','[out]','-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
        if s['key']=='release':
            cmd[cmd.index('-filter_complex')+1]=base.replace('crop=960:720:160:0','crop=928:696:176:12')
        run(cmd);pi=probe(out);pv=pi['streams'][0];actual=float(pi['format']['duration'])
        assert abs(actual-s['duration'])<.021
        assert (pv['width'],pv['height'],pv['r_frame_rate'],pv['pix_fmt'])==(1920,1080,'25/1','yuv420p')
        assert not any(v['codec_type']=='audio' for v in pi['streams'])
        run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'])
        plates.append(dict(row=27,**s,path=str(out),sha256=sha(out),bytes=out.stat().st_size,encoded_duration_s=actual,full_decode=True,foreground_scale=(1440/928 if s['key']=='release' else 1.5),background_scale=(1920/928 if s['key']=='release' else 2.),source_crop_xywh=([176,12,928,696] if s['key']=='release' else [160,0,960,720]),command=cmd,status='technical_candidate_pending_motion_and_full_QA'))
        for c,t in enumerate([.12,actual/2,actual-.12]):
            raw=run(['ffmpeg','-v','error','-ss',str(t),'-i',str(out),'-frames:v','1','-f','image2pipe','-vcodec','png','-'])
            im=Image.open(io.BytesIO(raw)).convert('RGB');im.thumbnail((480,270));sheet.paste(im,(c*480,n*310));sd.text((c*480+10,n*310+278),s['key']+' '+str(round(t,2)),fill='white')
        (root/('cuts_'+s['key']+'.json')).write_text(json.dumps([dict(row=27,timeline_in=0,timeline_out=actual,source=str(src),kind='footage',framing=dict(offset=s['source_start']))],indent=2)+'\n')
    contact=root/'CONTACT_v01.jpg';sheet.save(contact,quality=94)
    pool=json.loads(a.pool.read_text());asset_id='svs-13160-sts125-sm4-highlights'
    assert not any(x['asset_id']==asset_id for x in pool['assets'])
    record=dict(asset_id=asset_id,rows=[27],title='NASA Resource Reel: Hubble 25th Anniversary – Highlights from STS-125',source_page='https://svs.gsfc.nasa.gov/13160/',source_url=url,local_path=str(src),sha256=sha(src),bytes=src.stat().st_size,width=1280,height=720,fps=vs['r_frame_rate'],duration_s=float(info['format']['duration']),source_evidence_path=str(page),source_evidence_sha256=sha(page),licence='NASA factual educational use under NASA media guidelines',licence_status='NASA_resource_reel_origin_and_item_context_checked',licence_policy='https://www.nasa.gov/nasa-brand-center/images-and-media/',licence_evidence_path=str(terms),licence_evidence_sha256=sha(terms),credit="NASA's Goddard Space Flight Center",rights_obligations='Acknowledge NASA; no endorsement or promotional NASA marks; source audio excluded. Recheck any separately credited third-party component before using another interval.',review_status='static_candidate_not_KEEP',planned_appearances=1,planned_source_stretches=2,max_appearances=5,review_note='Real approach/release servicing footage, not Hubble animation or IMAX feature. Two adjacent cuts form one film window. Retain all of 4:3 image with feathered blur fill; no looping or speed change. Source has archival softness, to review at full size. Source audio is not used.')
    pool['assets'].append(record);pool['hubble_plates_v01']=plates;pool['hubble_contact_sheet']=str(contact);pool['hubble_contact_sheet_sha256']=sha(contact)
    pool.setdefault('search_checkpoints_v01',[]).append(dict(input='R27a Hubble servicing footage',date='2026-11-06',candidates_examined=1,active_minutes=12,outcome='One NASA archival reel; inspected approach/release stills. Excluded separate simulated deployment result; no repeated exhausted search.',budget_status='Stopped with candidate; moving review required'))
    a.pool.write_text(json.dumps(pool,indent=2)+'\n')
    (a.pool.parent/'HARVEST_HUBBLE_TECHNICAL_CHECK_v01.json').write_text(json.dumps(dict(job='J2141',spend_gbp=0,original=dict(path=str(src),sha256=sha(src),full_decode=True),plates=plates,contact_sheet=str(contact),contact_sheet_sha256=sha(contact),audio_perception=False,motion_perception=False,status='technical_checks_only_not_KEEP_or_film_PASS'),indent=2)+'\n')
    print('Hubble original and two row plates decoded/hashed; no KEEP')

if __name__=='__main__': main()
