#!/usr/bin/env python3
"""J2141 R41 free NASA limb fallback. Preserves sources and earlier versions."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr)
    return p.stdout

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--pool', type=Path, default=HERE/'HARVEST_POOL_v01.json')
    ap.add_argument('--report', type=Path, required=True)
    a = ap.parse_args()
    pool = json.loads(a.pool.read_text())
    source = next(x for x in pool['assets'] if x['asset_id']=='eol-sunsetchina-iss-20120413')
    original = Path(source['local_path'])
    evidence = []
    for path_key, hash_key in [('local_path','sha256'),('source_evidence_path','source_evidence_sha256'),('catalog_excerpt_path','catalog_excerpt_sha256'),('licence_evidence_path','licence_evidence_sha256')]:
        p = Path(source[path_key])
        assert sha(p)==source[hash_key], f'Changed input {p}'
        evidence.append(dict(path=str(p),sha256=sha(p)))
    a.out.mkdir(parents=True,exist_ok=True)
    dest = a.out/'plate_031_r41_atmosphere_v02.mp4'
    if dest.exists():
        raise FileExistsError(dest)
    credit = a.out/'NASA_credit.png'
    if credit.exists():
        raise FileExistsError(credit)
    im = Image.new('RGBA',(1920,1080))
    ImageDraw.Draw(im).text((36,1024),'NASA',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',28),fill=(255,255,255,210))
    im.save(credit)
    # 1024x576 crop keeps the blue limb and sun; 1.875x scale, no optical flow.
    # 110 house frames cover R41 plus 0.02 s assembly trim, never retime VO.
    vf = '[0:v:0]setpts=PTS-STARTPTS,crop=1024:576:0:96,scale=1920:1080:flags=lanczos,eq=brightness=0.015:saturation=1.06,noise=alls=4:allf=t,fps=25[plate];[plate][1:v:0]overlay=0:0:shortest=1[out]'
    cmd = ['ffmpeg','-v','error','-n','-ss','3.6','-i',str(original),'-loop','1','-i',str(credit),'-frames:v','110','-filter_complex',vf,'-map','[out]','-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)]
    run(cmd)
    run(['ffmpeg','-v','error','-xerror','-i',str(dest),'-f','null','-'])
    info = json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(dest)]))
    v = next(s for s in info['streams'] if s['codec_type']=='video')
    assert (v['width'],v['height'],v['r_frame_rate'],v['pix_fmt'],int(v['nb_read_frames']))==(1920,1080,'25/1','yuv420p',110)
    assert not any(s['codec_type']=='audio' for s in info['streams'])
    assert abs(float(info['format']['duration'])-4.4)<.001
    samples = []
    sheet = Image.new('RGB',(960,540),(30,44,61))
    for i,t in enumerate([0,.8,1.6,2.4,3.2,4.36]):
        p = a.out/f'encoded_{i}.png'
        run(['ffmpeg','-v','error','-n','-ss',str(t),'-i',str(dest),'-frames:v','1',str(p)])
        with Image.open(p) as frame:
            frame.thumbnail((320,270))
            sheet.paste(frame,((i%3)*320,(i//3)*270))
        samples.append(dict(time_s=t,path=str(p),sha256=sha(p)))
    contact = a.out/'CONTACT_v01.jpg'
    sheet.save(contact,quality=92)
    record = dict(job='J2141',row=41,spend_gbp=0,asset_id=source['asset_id'],path=str(dest),sha256=sha(dest),bytes=dest.stat().st_size,film_start_s=418.86,film_end_s=423.24,encoded_duration_s=4.4,assembly_tail_trim_s=.02,source_interval_s=[3.6,8.0],crop_xywh=[0,96,1024,576],scale=1.875,fps=25,native_fps=12,native_time_lapse=True,no_loop=True,no_interpolation=True,audio=False,credit='NASA',identity='Sunset over China, not sunrise',input_checks=evidence,full_decode=True,format_checks=True,command=cmd,samples=samples,contact_sheet=str(contact),contact_sha256=sha(contact),status='technical_candidate_not_KEEP',motion_perception=False,audio_perception=False)
    a.report.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(dict(path=str(dest),full_decode=True,frames=110,status=record['status'])))

if __name__=='__main__':
    main()
