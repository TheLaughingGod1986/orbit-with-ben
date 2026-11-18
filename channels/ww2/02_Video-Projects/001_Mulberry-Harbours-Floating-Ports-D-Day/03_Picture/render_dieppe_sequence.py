"""Narration-timed Dieppe explanatory sequence, not a reconstruction.

Uses the locked Scribe clock and inherited J2991 S7 claims 4-5. No new
historical claims, archive photographs, generated people, or narration edits.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from draw_engineering import W, H, PAPER, INK, WATER, ACCENT, text, arrow

# Exact starts from existing Scribe words, not estimated reading speed.
SCENES = [
    (88.10, 'date'), (97.92, 'operation'), (105.16, 'assault'),
    (113.54, 'force'), (118.34, 'canadians'), (123.28, 'tanks'),
    (126.84, 'hours'), (131.16, 'headlands'), (138.30, 'shingle'),
    (145.96, 'wall'), (150.40, 'trapped'), (154.96, 'withdrawal'),
    (158.56, 'casualties'), (164.94, 'proportion'), (168.58, 'end'),
]


def frame(kind, p):
    im = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(im)
    text(d, (80, 45), 'DIEPPE: THE COST OF A DEFENDED PORT', 49)
    text(d, (80, 125), 'Own explanatory illustration | Not a tactical map or reconstruction', 29)
    d.line((80, 190, 1840, 190), fill=INK, width=2)
    text(d, (80, 1008), 'Source: C. P. Stacey, Six Years of War (1955)', 26)
    if kind in ('date', 'operation', 'assault', 'headlands', 'shingle', 'wall', 'trapped', 'withdrawal'):
        d.rectangle((120, 260, 1800, 650), fill=WATER)
        d.rectangle((120, 650, 1800, 930), fill='#c6b99a')
        d.rectangle((120, 815, 1800, 840), fill=INK)
        text(d, (1370, 865), 'TOWN', 35)
        text(d, (1370, 740), 'BEACH', 35)
        text(d, (140, 285), 'SEA', 35)
        if kind in ('date', 'operation'):
            text(d, (420, 390), '19 AUGUST 1942' if kind == 'date' else 'OPERATION JUBILEE', 65)
            text(d, (570, 510), 'DIEPPE' if kind == 'date' else 'Combined Operations', 43, ACCENT)
            # A growing underline provides restrained continuous motion.
            d.line((430, 595, 430 + int(1000*p), 595), fill=ACCENT, width=7)
        elif kind == 'assault':
            arrow(d, (920, 310), (920, 390+int(220*p)))
            text(d, (260, 440), 'DIRECT ASSAULT', 44)
            text(d, (260, 520), 'Seize and hold', 34)
        elif kind == 'headlands':
            for pts in [[(120, 390), (430, 390), (570, 650), (120, 650)],
                        [(1410, 390), (1800, 390), (1800, 650), (1300, 650)]]:
                d.polygon(pts, fill='#a29f8d')
            text(d, (650, 370), 'TWO HEADLANDS', 44)
            # No weapon positions or firing arcs are invented.
            d.line((620, 490, 620+int(650*p), 490), fill=ACCENT, width=7)
        elif kind in ('shingle', 'wall', 'trapped'):
            for i in range(70):
                x=155+(i*83)%1570; y=670+(i*37)%125
                d.ellipse((x, y, x+17, y+11), fill='#9d927b')
            x=650+int(160*min(p, .6)) if kind == 'shingle' else 746
            d.rounded_rectangle((x, 700, x+200, 765), radius=18, fill=INK)
            d.rectangle((x+60, 670, x+140, 700), fill=INK)
            label={'shingle': 'LOOSE FLINT COBBLES', 'wall': 'SIX-FOOT SEA WALL', 'trapped': 'LOST OR TRAPPED'}[kind]
            text(d, (470, 385), label, 54, ACCENT)
            if kind == 'wall':
                arrow(d, (1130, 530), (1130, 650+int(160*p)))
            elif kind == 'trapped':
                d.line((x-30, 680, x+230, 790), fill=ACCENT, width=7)
        else:
            arrow(d, (920, 620), (920, 590-int(270*p)))
            text(d, (340, 420), 'THE SURVIVING CRAFT PULLED BACK', 44)
    elif kind in ('force', 'canadians', 'tanks'):
        title={'force':'6,086 MEN EMBARKED', 'canadians':'NEARLY 5,000 CANADIANS', 'tanks':'29 CHURCHILL TANKS'}[kind]
        text(d, (210, 290), title, 64, ACCENT)
        text(d, (210, 390), '2nd Canadian Infantry Division' if kind == 'canadians' else 'Operation Jubilee', 37)
        # Icons are units in a labelled count display, not actual landing positions.
        n=29 if kind == 'tanks' else 60
        for i in range(min(n, int(n*p)+1)):
            x=230+(i%15)*102; y=530+(i//15)*90
            if kind == 'tanks':
                d.rounded_rectangle((x, y+20, x+72, y+55), radius=9, fill=INK)
                d.rectangle((x+20, y+3, x+50, y+20), fill=INK)
            else:
                d.ellipse((x+20,y,x+44,y+24),fill=INK)
                d.rounded_rectangle((x+10,y+30,x+54,y+70),radius=8,fill=INK)
        text(d, (210, 930), '29 icons = 29 tanks' if kind == 'tanks' else 'People icons are illustrative, not a count scale', 28)
    elif kind == 'hours':
        text(d, (230, 300), 'WITHIN THREE HOURS', 68, ACCENT)
        d.arc((660, 450, 1200, 940), -90, -90+max(1,int(270*p)), fill=INK, width=23)
        text(d, (835, 620), '3', 120)
    else:
        text(d, (150, 280), '3,623 MEN', 76, ACCENT)
        text(d, (150, 390), 'Killed, wounded, or captured', 44)
        d.rectangle((150, 570, 1770, 700), fill='#d5cfbf')
        extent=3623/6086
        bar_progress=1 if kind == 'proportion' else p
        d.rectangle((150, 570, 150+int(1620*extent*bar_progress), 700), fill=ACCENT)
        text(d, (150, 760), 'Almost 60 percent' if kind == 'proportion' else 'Out of 6,086 embarked', 53)
        text(d, (150, 880), 'One total: includes wounded and prisoners; not deaths alone', 29)
        if kind == 'proportion':
            d.line((150, 840, 150+int(620*p), 840), fill=ACCENT, width=5)
    return im


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--vo', type=Path)
    ap.add_argument('--render', action='store_true')
    a=ap.parse_args(); a.out.mkdir(parents=True, exist_ok=True)
    records=[]
    for i, ((start,kind),(end,_)) in enumerate(zip(SCENES,SCENES[1:])):
        first=round(start*25); last=round(end*25); count=last-first
        key=f'dieppe_{i+1:02}_{kind}_v08'
        still=a.out/(key+'.jpg'); frame(kind, .9).save(still, quality=92)
        rec=dict(scene=kind,film_start_frame=first,film_end_frame=last,
                 start_s=first/25,end_s=last/25,frames=count,still=still.name,
                 source='J2991 SOURCES.md S7 / claims 4–5',status='DRAFT_NOT_QUALITY_APPROVED')
        if a.render:
            target=a.out/(key+'.mp4')
            proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','25','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-threads','2','-pix_fmt','yuv420p',str(target)],stdin=subprocess.PIPE)
            for n in range(count):proc.stdin.write(frame(kind,n/max(count-1,1)).tobytes())
            proc.stdin.close()
            if proc.wait():raise RuntimeError('encode failed: '+kind)
            subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
            rec.update(file=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),technical='FULLY_DECODED')
        records.append(rec)
        print(key, count, flush=True)
    sequence_start=records[0]['start_s']
    sequence_end=records[-1]['end_s']
    sequence_duration=sequence_end-sequence_start
    manifest=dict(start_s=sequence_start,end_s=sequence_end,fps=25,scenes=records,
                  timing='25fps nearest frame; continuous narration, no words edited',
                  review='STILLS_AND_TECHNICAL_ONLY_NO_AUDIO_OR_MOTION_VERDICT')
    if a.render:
        listing=a.out/'concat.txt'
        listing.write_text(''.join("file '"+r['file']+"'\n" for r in records))
        silent=a.out/'dieppe_sequence_silent_v08.mp4'
        subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(silent)],check=True)
        if a.vo:
            preview=a.out/'dieppe_narration_preview_v08.mp4'
            subprocess.run(['ffmpeg','-v','error','-y','-i',str(silent),'-ss',str(sequence_start),'-i',str(a.vo),'-map','0:v','-map','1:a','-t',str(sequence_duration),'-c:v','copy','-c:a','aac','-b:a','192k',str(preview)],check=True)
            subprocess.run(['ffmpeg','-v','error','-i',str(preview),'-f','null','-'],check=True)
            manifest['preview']=dict(file=preview.name,sha256=hashlib.sha256(preview.read_bytes()).hexdigest())
    (a.out/'dieppe_sequence_manifest_v08.json').write_text(json.dumps(manifest,indent=2)+'\n')


if __name__=='__main__':main()
