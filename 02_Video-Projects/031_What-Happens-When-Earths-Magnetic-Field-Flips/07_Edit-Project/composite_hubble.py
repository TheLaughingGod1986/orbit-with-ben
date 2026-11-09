#!/usr/bin/env python3
"""R27 source-linked composites. Use /usr/bin/python3; never overwrite media."""
import argparse, json, io, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from harvest_solar import sha, run, probe


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',required=True,type=Path)
    a=ap.parse_args(); root=a.out.resolve();root.mkdir(parents=True,exist_ok=True)
    here=Path(__file__).resolve().parent
    pool=json.loads((here/'HARVEST_POOL_v01.json').read_text())
    asset=next(x for x in pool['assets'] if x['asset_id']=='svs-13160-sts125-sm4-highlights')
    for key,hkey in [('local_path','sha256'),('source_evidence_path','source_evidence_sha256'),('licence_evidence_path','licence_evidence_sha256')]:
        assert sha(Path(asset[key]))==asset[hkey],key
    specs=[dict(key='orbits',source_start=116.,film_start=280.42,duration=4.32,frames=108,overlay_manifest='CODE_SAA_v01.json',collection='graphics',overlay_mode='hubble_saa',overlay_delay=0.,fg_x=0,fg_y=135,fg_w=1080,fg_h=810),
           dict(key='pause',source_start=668.8,film_start=284.74,duration=4.28,frames=107,overlay_manifest='CODE_CARDS_v01.json',collection='cards',overlay_mode='FACT',overlay_delay=.02,fg_x=840,fg_y=0,fg_w=1080,fg_h=810)]
    records=[];sheet=Image.new('RGB',(1440,640),(31,38,51));sd=ImageDraw.Draw(sheet)
    for n,s in enumerate(specs):
        m=json.loads((here/s['overlay_manifest']).read_text())
        ov=next(x for x in m[s['collection']] if x['row']==27 and x.get('mode',x.get('kind'))==s['overlay_mode'])
        assert abs(s['film_start']+s['overlay_delay']-ov['start_s'])<.00001
        assert sha(Path(ov['path']))==ov['sha256']
        out=root/f"composite_031_r27_{s['key']}_v02.mp4"
        mask=root/f"feather_{s['key']}.png";credit=root/f"credit_{s['key']}.png"
        for p in (out,mask,credit):
            if p.exists():raise FileExistsError(p)
        w,h=s['fg_w'],s['fg_h']
        im=Image.new('L',(w,h));px=im.load()
        for y in range(h):
            for x in range(w):px[x,y]=int(255*min(1,x/50,(w-1-x)/50,y/35,(h-1-y)/35))
        im.save(mask)
        im=Image.new('RGBA',(1920,1080));ImageDraw.Draw(im).text((36,1024),'NASA',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',30),fill='white',stroke_width=1,stroke_fill=(10,15,25,200));im.save(credit)
        filt=(f'[0:v]setpts=PTS-STARTPTS,crop=928:696:176:12,fps=25,split=2[fg][bg];'
              f'[bg]scale=1920:1440:flags=lanczos,crop=1920:1080,boxblur=40:2[b];'
              f'[fg]scale={w}:{h}:flags=lanczos,setsar=1[f];[1:v]format=gray[m];[f][m]alphamerge[fa];'
              f"[b][fa]overlay={s['fg_x']}:{s['fg_y']}:shortest=1,eq=brightness=0.015:saturation=1.02,noise=alls=4:allf=t[p];"
              f"[2:v]setpts=PTS-STARTPTS+{s['overlay_delay']}/TB[o];[p][o]overlay=0:0:eof_action=pass[q];[q][3:v]overlay=0:0:shortest=1[out]")
        cmd=['ffmpeg','-v','error','-n','-ss',str(s['source_start']),'-i',asset['local_path'],'-loop','1','-i',str(mask),'-i',ov['path'],'-loop','1','-i',str(credit),'-filter_complex',filt,'-map','[out]','-an','-frames:v',str(s['frames']),'-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
        run(cmd);info=probe(out);vs=next(x for x in info['streams'] if x['codec_type']=='video')
        assert (vs['width'],vs['height'],vs['r_frame_rate'],vs['pix_fmt'],int(vs['nb_frames']))==(1920,1080,'25/1','yuv420p',s['frames'])
        assert abs(float(info['format']['duration'])-s['duration'])<.001
        assert not any(x['codec_type']=='audio' for x in info['streams'])
        run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'])
        cuts=root/f"cuts_{s['key']}.json";cuts.write_text(json.dumps([dict(row=27,timeline_in=0,timeline_out=s['duration'],source=asset['local_path'],kind='footage',framing=dict(offset=s['source_start']))],indent=2)+'\n')
        samples=[]
        for c,t in enumerate([.2,s['duration']/2,s['duration']-.2]):
            raw=run(['ffmpeg','-v','error','-ss',str(t),'-i',str(out),'-frames:v','1','-f','image2pipe','-vcodec','png','-']);im=Image.open(io.BytesIO(raw)).convert('RGB');p=root/f"sample_{s['key']}_{c}.png";im.save(p);samples.append(dict(time_s=t,path=str(p),sha256=sha(p)));im.thumbnail((480,270));sheet.paste(im,(c*480,n*320));sd.text((c*480+8,n*320+280),s['key']+' '+str(round(t,2)),fill='white')
        gate=root/f"polish_{s['key']}.json"
        r=subprocess.run(['python3',str(here.parents[2]/'scripts/polish_gate.py'),str(out),'--cuts',str(cuts),'--out',str(gate)],capture_output=True,text=True)
        if r.returncode not in (0,1):raise RuntimeError(r.stderr)
        records.append(dict(**s,path=str(out),sha256=sha(out),bytes=out.stat().st_size,source_asset_id=asset['asset_id'],source_sha256=asset['sha256'],overlay=ov,command=cmd,full_decode=True,source_crop_xywh=[176,12,928,696],max_upscale=1920/928,samples=samples,polish=dict(exit_code=r.returncode,stdout=r.stdout,report=str(gate),sha256=sha(gate)),status='technical_candidate_not_KEEP'))
    contact=root/'CONTACT_v01.jpg';sheet.save(contact,quality=94)
    record=dict(job='J2141',spend_gbp=0,composites=records,contact_sheet=str(contact),contact_sheet_sha256=sha(contact),motion_perception=False,audio_perception=False,status='partial_component_checks_not_film_approval',reuse_note='New nonoverlapping source stretches 116.00–120.32 and 668.80–673.08. Existing R27 approach/release remain; four distinct stretches in same row, total <=5 per source. No loops or slowdown.')
    (here/'COMPOSITE_HUBBLE_TECHNICAL_CHECK_v01.json').write_text(json.dumps(record,indent=2)+'\n')
    pool['hubble_composites_v01']=records
    asset['planned_source_stretches']=4
    pool['search_checkpoints_v01']=[x for x in pool.get('search_checkpoints_v01',[]) if x.get('input')!='R27 remaining overlay plates']
    pool['search_checkpoints_v01'].append(dict(input='R27 remaining overlay plates',date='2026-11-07',candidates_examined=1,active_minutes=8,outcome='Existing NASA reel: excluded 664.48–673.08 uninterrupted proposal because sampled cabin cut; selected 116.00–120.32 and 668.80–673.08, static checks only.',budget_status='Stopped with candidates; no new archive search'))
    (here/'HARVEST_POOL_v01.json').write_text(json.dumps(pool,indent=2)+'\n')
    print('R27 two composites built/decoded/hashed; read polish reports; no KEEP')

if __name__=='__main__': main()
