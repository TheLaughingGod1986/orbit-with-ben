#!/usr/bin/env python3
"""Bounded R23 composite candidate. A still pan is not native source motion.

Uses the reviewed alpha export unchanged over its own feathered/blurred photo.
This is a silent layout preview, never an assembly-ready or cleared source.
The planned PIA08733 moving plate is unavailable: this uses the inset source
only as a decorative contrast trial and does not replace that planned plate.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
HERE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    if args.out.exists():
        ap.error('Use a fresh directory; existing media must remain unchanged')
    manifest = json.loads((HERE/'LANDING_RECORD_RENDER_MANIFEST_v01.json').read_text())
    source = Path(manifest['source'])
    overlay = Path(manifest['render'])
    assert sha(source) == manifest['source_sha256']
    assert sha(overlay) == manifest['sha256']
    args.out.mkdir(parents=True)
    # Background is visibly defocused decoration. The scientific inset retains
    # its exact reviewed scale, endpoints, pixels and typography.
    with Image.open(source) as im:
        background = im.convert('RGB').crop(manifest['crop'])
    background = background.resize((1944, 1944), Image.Resampling.LANCZOS)
    background = background.crop((0, 432, 1944, 1512)).filter(ImageFilter.GaussianBlur(65))
    background = Image.blend(background, Image.new('RGB', background.size, (37,52,73)), .72)
    decoder = subprocess.Popen(['ffmpeg','-v','error','-i',str(overlay),'-f','rawvideo','-pix_fmt','rgba','pipe:1'],stdout=subprocess.PIPE)
    video = args.out/'032_r23_composite_preview_v01.mp4'
    encoder = subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
    metrics=[]
    try:
        for i in range(108):
            raw=decoder.stdout.read(1920*1080*4)
            assert len(raw)==1920*1080*4, 'Truncated overlay'
            alpha=Image.frombytes('RGBA',(1920,1080),raw)
            x=round(24*i/107)
            bg=background.crop((x,0,x+1920,1080)).convert('RGBA')
            bg.alpha_composite(alpha)
            rgb=np.array(bg.convert('RGB'))
            # Fine, deterministic grain added only after compositing.
            rng=np.random.default_rng(2089+i)
            grain=rng.integers(-2,3,(1080,1920,1),dtype=np.int16)
            rgb=np.clip(rgb.astype(np.int16)+grain,0,255).astype(np.uint8)
            image=Image.fromarray(rgb)
            if i in [12,54,72,95]:
                image.save(args.out/f'frame_{i:03}.png')
            luma=rgb[:,:,0]*.2126+rgb[:,:,1]*.7152+rgb[:,:,2]*.0722
            metrics.append(dict(frame=i,mean_luma=round(float(luma.mean()),2),p95=round(float(np.percentile(luma,95)),2)))
            encoder.stdin.write(rgb.tobytes())
        assert decoder.stdout.read(1)==b'', 'Unexpected extra frames'
        assert decoder.wait()==0
        encoder.stdin.close()
        assert encoder.wait()==0
    except BaseException:
        decoder.kill();encoder.kill();decoder.wait();encoder.wait()
        raise
    subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
    result=dict(job='J2089',row=23,status='COMPOSITE_CANDIDATE_REQUIRES_REVIEW',
        review_of_overlay='J2304',source=str(source),source_sha256=sha(source),
        overlay=str(overlay),overlay_sha256=sha(overlay),video=str(video),sha256=sha(video),
        dimensions=[1920,1080],fps=30,frames=108,seconds=3.6,audio=False,
        film_interval_proposal=[232.0,235.6],
        background='Same R23 source, cropped without white surround, blurred 65px, 72% navy grade; 24px horizontal decorative pan; grain +/-2',
        inset='Reviewed export unchanged: 408x408 native Titan inset; no upscale',
        metrics=metrics,stills={p.name:sha(p) for p in args.out.glob('frame_*.png')},
        holds=['Not native moving footage: still pan only',
            'Decorative inset-source background differs from planned PIA08733 plate; no shot-list substitution approved',
            'Per-asset rights clearance unresolved; no new permission asserted',
            'Final VO sync, contrast, actual reuse, neighbouring imagery and all film gates require review',
            'Silent layout candidate only; never ship standalone',
            'No perceived motion/audio or film-stage approval claimed'])
    (HERE/'R23_COMPOSITE_PREVIEW_v01.json').write_text(json.dumps(result,indent=2)+'\n')
    print(video)
if __name__=='__main__':main()
