"""Render cleared archival source plates; these are building blocks, not a cut.

Each source is hash checked. Small scans stay in a framed plate at <=1.5x,
including the 1.04x camera move. Never repeats source frames to fill a paragraph.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps


def render(record, source_dir, out_dir):
    source = source_dir / record['file']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == record['sha256']
    assert record['status'] == 'ELIGIBLE_WITH_STATED_SUBJECT_UNDER_CHIEF_RULING'
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert('RGB')
        width, height = image.size
        assert (width, height) == (record['width'], record['height'])
        small = width <= 800
        # Keep the complete original on small sources, including scan marks.
        if small:
            base_scale = min(1.4, 1536 / width, 810 / height)
            size = (round(width * base_scale), round(height * base_scale))
            canvas = Image.new('RGB', (1920, 1080), '#e2dfd6')
            xy = ((1920-size[0])//2, (1080-size[1])//2-15)
            canvas.paste(image.resize(size, Image.Resampling.LANCZOS), xy)
            ImageDraw.Draw(canvas).rectangle((xy[0]-2,xy[1]-2,xy[0]+size[0]+1,xy[1]+size[1]+1), outline='#69665e', width=2)
        else:
            base_scale = max(1920/width, 1080/height)
            canvas = ImageOps.fit(image, (1920, 1080), Image.Resampling.LANCZOS)
        maximum_scale = base_scale * 1.04
        assert maximum_scale <= 2.35
    key = source.stem
    plate = out_dir / (key + '_plate.png')
    canvas.save(plate)
    # Fixed credit remains legible while source picture moves.
    credit = Image.new('RGBA', (1920,1080))
    d = ImageDraw.Draw(credit)
    font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 23)
    text = 'IWM ' + record['fields_verbatim']['catalogue_number'] + ' / Crown copyright expired / via Wikimedia Commons'
    bounds=d.textbbox((0,0),text,font=font)
    d.rectangle((34,1013,60+bounds[2],1058),fill=(20,20,20,190))
    d.text((47,1023),text,font=font,fill='white')
    label = out_dir / (key + '_credit.png')
    credit.save(label)
    output=out_dir/(key+'_motion_v07.mp4')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-i',str(plate),'-i',str(label),'-filter_complex',"[0:v]zoompan=z='1+0.04*on/299':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=25[m];[m][1:v]overlay=0:0,format=yuv420p[v]",'-map','[v]','-t','12','-an','-c:v','libx264','-preset','veryfast','-crf','20','-threads','2','-movflags','+faststart',str(output)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'],check=True)
    return dict(file=output.name,source=record['file'],source_sha256=record['sha256'],sha256=hashlib.sha256(output.read_bytes()).hexdigest(),presentation='framed' if small else 'full-frame',maximum_upscale=round(maximum_scale,4),duration_s=12,frames=300,technical='ENCODED_AND_FULLY_DECODED',review='NO_MOTION_PERCEPTION_REVIEW',editorial_use=record['editorial_use'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    records=json.loads(Path(__file__).with_name('archive_cleared_v07.json').read_text())['records']
    results=[]
    for r in records:
        results.append(render(r,args.sources,args.out))
        (args.out/'archive_motion_manifest_v07.json').write_text(json.dumps(results,indent=2)+'\n')
        print(results[-1]['file'],flush=True)


if __name__=='__main__':
    main()
