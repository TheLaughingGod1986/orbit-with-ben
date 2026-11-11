#!/usr/bin/env python3
"""J2452 Moon: finished-master cuts on the existing clean narration clock.

No source rebuilding, chart removal, source audio, or gate overrides. Run with
the existing J2141-venv Python. Outputs are versioned and never overwritten.
"""
import argparse
import hashlib
import shutil
import json
import math
import subprocess as sp
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
OUT = Path('/Users/ben/_desk/J2452-sleep-scratch/public_moon_v02')
MASTER = Path('/Volumes/data/mac-mini-archive/Desktop/MOON_LEAVING_FULL_v04_WATCH_THIS.mp4')
NARR = Path('/Users/ben/_desk/J2452-sleep-scratch/narration_013_v01/chapter_013_narration_v01.wav')

def run(args):
    sp.run(['ffmpeg', '-v', 'error', '-nostdin', '-n', *args], check=True, timeout=480)

def enc():
    return ['-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-threads', '4', '-pix_fmt', 'yuv420p', '-r', '30', '-video_track_timescale', '90000']

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    global OUT
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=OUT)
    parser.add_argument('--reuse-slices',type=Path)
    args=parser.parse_args()
    OUT=args.out
    OUT.mkdir(exist_ok=False)
    chapter = json.loads((ROOT/'jobs/reviews/J2452/picture_timeline_v01.json').read_text())['chapters'][0]
    # Video ends from actual final_j.txt stream probes; raw narration tails
    # continue past these boundaries. Stop before breath/card/outro pictures.
    picture_ends = [20.62625, 89.25, 233.958333, 376.666667, 474.97675, 498.666667]
    slices = chapter['slices']
    cumulative = 0
    paths, lengths, cuts, holds = [], [], [], []
    for i, (s, end) in enumerate(zip(slices, picture_ends)):
        target_end = round(s['chapter_out_s']*30)
        frames = target_end - cumulative
        duration = frames/30
        src_in = s['master_in_s']
        available = min(end, s['master_out_s'])-src_in
        dest = OUT/f'slice_{i:02d}.mp4'
        if args.reuse_slices:
            old=args.reuse_slices/dest.name
            count=int(sp.check_output(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=nb_read_frames','-of','csv=p=0',str(old)]).strip())
            if count != frames: raise ValueError((old,count,frames))
            shutil.copy2(old,dest)
            if sha(old) != sha(dest): raise ValueError('slice copy hash mismatch')
        else:
            run(['-reinit_filter', '0', '-ss', str(src_in), '-i', str(MASTER), '-t', str(duration),
                 '-vf', f'trim=duration={available},setpts=PTS-STARTPTS,scale=1920:1080,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=1,format=yuv420p',
                 *enc(), str(dest)])
        paths.append(dest); lengths.append(duration)
        cuts.append(dict(row=f'slice-{i}', timeline_in=cumulative/30, timeline_out=target_end/30,
                         source=MASTER.name, framing=dict(offset=src_in), src_w=1920, upscale=1))
        holds.append(dict(slice=i, master_in_s=src_in, master_picture_end_s=min(end,s['master_out_s']),
                          narration_master_out_s=s['master_out_s'], hold_s=max(0,duration-available)))
        cumulative=target_end
        print('saved slice', i, flush=True)
    # 0.4-second dissolves with cloned handles consume exactly 0.2 seconds
    # from each side of a new cut. The narration clock is never overlapped.
    pieces=[]; joins=[]
    clock=0
    for i,(src,d) in enumerate(zip(paths,lengths)):
        a=.2 if i else 0; b=d-(.2 if i<len(paths)-1 else 0)
        interior=OUT/f'interior_{i:02d}.mp4'
        run(['-ss',str(a),'-i',str(src),'-t',str(b-a),*enc(),str(interior)])
        pieces.append(interior)
        clock+=d
        if i==len(paths)-1: continue
        dest=OUT/f'join_{i:02d}.mp4'
        graph=f'[0:v]trim=start={d-.2}:end={d},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.2[a];[1:v]trim=end=0.2,setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration=0.2[b];[a][b]xfade=transition=fade:duration=0.4:offset=0,format=yuv420p[v]'
        run(['-i',str(src),'-i',str(paths[i+1]),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-t','0.4',*enc(),str(dest)])
        pieces.append(dest)
        joins.append(dict(row=f'join-{i}',timeline_in=clock-.2,timeline_out=clock+.2,
                          source=f'new-dissolve-{i}',framing=dict(offset=0),src_w=1920,upscale=1))
        print('saved join', i, flush=True)
    listing=OUT/'concat.txt'; listing.write_text(''.join(f"file '{p}'\n" for p in pieces))
    picture=OUT/'picture_undarkened.mp4'
    run(['-f','concat','-safe','0','-i',str(listing),'-c','copy',str(picture)])
    title=Image.new('RGBA',(1920,1080)); draw=ImageDraw.Draw(title)
    draw.text((90,940),'I · The Drifting Moon',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf',42),fill=(234,230,223,166))
    title.save(OUT/'title.png')
    final=OUT/'013_moon_undarkened_v01.mp4'
    run(['-i',str(picture),'-loop','1','-i',str(OUT/'title.png'),'-i',str(NARR),
         '-filter_complex_threads','1','-filter_complex',
         '[1:v]format=rgba,fade=t=in:st=0:d=1.5:alpha=1,fade=t=out:st=4.5:d=1.5:alpha=1[t];[0:v][t]overlay=0:0:enable=lt(t\\,6),format=yuv420p[v]',
         '-map','[v]','-map','2:a','-t',str(cumulative/30),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4',
         '-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-c:a','aac','-b:a','192k','-ar','48000',str(final)])
    # Full-duration pixel sampling every two seconds, including endpoints.
    full=[dict(row=f'pixel-{k}',timeline_in=k,timeline_out=min(k+2,cumulative/30),
               source=MASTER.name,framing=dict(offset=k),src_w=1920,upscale=1) for k in range(0,math.ceil(cumulative/30),2)]
    changed=[*joins,dict(row='quiet-title',timeline_in=0,timeline_out=6,source='quiet-title',framing=dict(offset=0),src_w=1920,upscale=1)]
    for i,h in enumerate(holds):
        if h['hold_s']>0:
            end=cuts[i]['timeline_out']; changed.append(dict(row=f'tail-hold-{i}',timeline_in=end-h['hold_s'],timeline_out=end,source=f'tail-hold-{i}',framing=dict(offset=0),src_w=1920,upscale=1))
    for name,data in [('full_pixel_cuts.json',full),('changed_cuts.json',changed),('source_cuts.json',cuts)]:
        (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
    report=dict(status='CANDIDATE_GATES_PENDING',film='013',output=str(final),sha256=sha(final),
                expected_frames=cumulative,duration_s=cumulative/30,source_master=str(MASTER),
                narration_sha256=sha(NARR),planned_ranges=chapter['planned_ranges'],slices=slices,tail_holds=holds,
                darkening='Identity: entire Moon chapter precedes 19:30 ramp; brightness ratio 1.0 by identical file, no second encode.',
                breath='Four-second inter-film breath remains for final join, outside this narration chapter.',
                covers='Actual corrected slices exclude all source Orbit/agenda/act cards; no new footage used.',
                inherited='Charts/labels and untouched public-master stretches retained under 11 Nov 09:29Z ruling.')
    (OUT/'BUILD.json').write_text(json.dumps(report,indent=2)+'\n')
    print(final,flush=True)

if __name__=='__main__': main()
