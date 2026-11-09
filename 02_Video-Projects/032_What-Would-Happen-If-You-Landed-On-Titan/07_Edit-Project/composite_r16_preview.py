#!/usr/bin/env python3
"""Silent R16 layout trial using J2177's Cassini alternative, not descent footage."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from code_graphics import font

HERE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    if args.out.exists():
        ap.error('Fresh directory required; preserve earlier versions')
    pool = json.loads((HERE/'HARVEST_POOL_v01.json').read_text())
    source = next(x for x in pool['assets'] if x['asset_id']=='PIA21610')
    overlay = next(x for x in json.loads((HERE/'MECHANISM_RENDER_MANIFEST_v01.json').read_text())['clips'] if x['id']=='r16_descent_147m')
    assert sha(source['local_path']) == source['sha256']
    assert sha(overlay['render']) == overlay['sha256']
    args.out.mkdir(parents=True)
    photo = Image.open(source['local_path']).convert('RGB')
    decoder = subprocess.Popen(['ffmpeg','-v','error','-i',overlay['render'],'-f','rawvideo','-pix_fmt','rgba','pipe:1'],stdout=subprocess.PIPE)
    video = args.out/'032_r16_cassini_counter_draft_v01.mp4'
    encoder = subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(video)],stdin=subprocess.PIPE)
    try:
        for i in range(108):
            # One 960x540 window, 20 native pixels of continuous vertical pan.
            y = 230 + 20*i/107
            bg = photo.transform((1920,1080),Image.Transform.EXTENT,(80,y,1040,y+540),Image.Resampling.BICUBIC)
            rgb = np.asarray(bg).astype(np.float32)
            # Neutral lifted grade: no false orange colour introduced into IR data.
            rgb = np.clip(rgb*.78+22,0,255).astype(np.uint8)
            bg = Image.fromarray(rgb).convert('RGBA')
            raw = decoder.stdout.read(1920*1080*4)
            assert len(raw)==1920*1080*4
            bg.alpha_composite(Image.frombytes('RGBA',(1920,1080),raw))
            draw = ImageDraw.Draw(bg)
            draw.text((56,980),'CASSINI • NEAR-INFRARED',font=font(29),fill='white',stroke_width=1,stroke_fill=(35,35,35))
            draw.text((56,1020),'NASA/JPL-Caltech/Space Science Institute',font=font(27),fill='white',stroke_width=1,stroke_fill=(35,35,35))
            rgb = np.asarray(bg.convert('RGB')).astype(np.int16)
            rgb = np.clip(rgb+np.random.default_rng(2089+i).integers(-2,3,(1080,1920,1)),0,255).astype(np.uint8)
            if i in (12,54,72,95): Image.fromarray(rgb).save(args.out/f'frame_{i:03}.png')
            encoder.stdin.write(rgb.tobytes())
        assert decoder.stdout.read(1)==b''
        assert decoder.wait()==0
        encoder.stdin.close()
        assert encoder.wait()==0
    except BaseException:
        decoder.kill(); encoder.kill(); decoder.wait(); encoder.wait()
        raise
    subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
    record=dict(job='J2089',row=16,status='DRAFT_NOT_FOR_ASSEMBLY',source=source['local_path'],source_sha256=source['sha256'],overlay=overlay['render'],overlay_sha256=overlay['sha256'],overlay_review='J2177',video=str(video),sha256=sha(video),frames=108,fps=30,duration=3.6,dimensions=[1920,1080],audio=False,crop_start=[80,230,1040,770],crop_end=[80,250,1040,790],upscale=2.0,source_motion='STILL_PAN_NOT_NATIVE',proposed_film_window=[154.0,157.6],proposed_appearance_rows=[16,28],holds=['Per-asset rights unresolved','Individual composite/motion review and polish required','Final VO sync and reuse checks required','Cassini cloud context, never represented as Huygens descent imagery','No frame-0 substitution or approval'])
    (HERE/'R16_COMPOSITE_PREVIEW_v01.json').write_text(json.dumps(record,indent=2)+'\n')
    print(video)

if __name__=='__main__': main()
