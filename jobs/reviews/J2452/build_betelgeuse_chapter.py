#!/usr/bin/env python3
"""Integrate checked Orbit covers on the corrected 029 chapter clock.

This saves a silent picture checkpoint, not an approved sleep chapter: source
charts, original in-film hard cuts, quiet title and breath remain unresolved.
"""
import argparse, json, subprocess
from pathlib import Path
from integrate_betelgeuse_cover_joins import sha, source_geometry
ROOT=Path(__file__).resolve().parents[3]
def run(args):
    subprocess.run(['ffmpeg','-hide_banner','-nostdin','-loglevel','error','-n',*args],check=True)
def enc():
    return ['-an','-c:v','libx264','-preset','fast','-crf','18','-r','30','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-video_track_timescale','90000']
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    timeline=json.loads((ROOT/'jobs/reviews/J2452/picture_timeline_v01.json').read_text())
    c=next(x for x in timeline['chapters'] if x['film']=='029')
    covers=json.loads((ROOT/'jobs/reviews/J2452/betelgeuse_orbit_readback_v01.json').read_text())
    master=Path(c['master']);assert sha(master)==covers['master_sha256']
    assert c['compilation_start_s']>timeline['darkening']['ramp_global_s'][1]
    a.out.mkdir(parents=True,exist_ok=False)
    pieces=[];records=[];mapped=[]
    for i,s in enumerate(c['slices']):
        nf=round((s['chapter_out_s']-s['chapter_in_s'])*30)
        geometry=source_geometry(master,s['master_in_s'],nf/30)
        args=['-reinit_filter','0','-ss',str(s['master_in_s']),'-i',str(master)]
        selected=[cv for cv in covers['covers'] if s['master_in_s']<=cv['master_in_s'] and cv['master_out_s']<=s['master_out_s']]
        graph='[0:v]fps=30,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1,colorchannelmixer=rr=.85:gg=.85:bb=.85,format=yuv420p,limiter=min=16:max=180:planes=1,format=rgb24[base];'
        base='base'
        for n,cv in enumerate(selected,1):
            assert sha(Path(cv['output']))==cv['sha256'];args+=['-i',cv['output']]
            start=cv['master_in_s']-s['master_in_s'];span=cv['master_out_s']-cv['master_in_s'];margin=10/30;fade=2
            on=start-margin;off=start+span+margin;padded=off-on+2*fade
            graph+=(f'[{n}:v]fps=30,setpts=PTS-STARTPTS,scale=in_color_matrix=bt601,format=rgba,tpad=start_mode=clone:start_duration={fade+margin}:stop_mode=clone:stop_duration={fade+margin},trim=duration={padded},format=rgba,fade=t=in:st=0:d=2:alpha=1,fade=t=out:st={padded-fade}:d=2:alpha=1,setpts=PTS+{on-fade}/TB[cover{n}];'
                f'[{base}][cover{n}]overlay=eof_action=pass:format=rgb[mix{n}];')
            base=f'mix{n}'
            mapped.append(dict(cover=cv['output'],sha256=cv['sha256'],chapter_in_s=s['chapter_in_s']+start,chapter_out_s=s['chapter_in_s']+start+span,opaque_in_s=s['chapter_in_s']+on,opaque_out_s=s['chapter_in_s']+off,reference_clock_note='Cover frame zero at nominal chapter_in_s; endpoint clones outside component'))
        graph+=f'[{base}]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]'
        dest=a.out/f'slice_{i:02d}.mp4'
        run([*args,'-filter_complex',graph,'-map','[v]','-frames:v',str(nf),*enc(),str(dest)])
        pieces.append(dest);records.append(dict(source=s,frames=nf,graph=graph,geometry=geometry,output=str(dest),sha256=sha(dest)))
        print('saved slice',i,flush=True)
    # Two-second dissolves at the two removed-block joins use endpoint handles.
    # Their total duration replaces the same two seconds of chapter time.
    joined=[]
    for i,src in enumerate(pieces):
        d=records[i]['frames']/30;left=1 if i else 0;right=1 if i<len(pieces)-1 else 0
        interior=a.out/f'interior_{i:02d}.mp4'
        run(['-ss',str(left),'-i',str(src),'-frames:v',str(records[i]['frames']-30*(left+right)),*enc(),str(interior)]);joined.append(interior)
        if not right:continue
        trans=a.out/f'join_{i:02d}.mp4'
        graph=f'[0:v]trim=start={d-1}:end={d},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1[a];[1:v]trim=end=1,setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration=1[b];[a][b]xfade=transition=fade:duration=2:offset=0,format=yuv420p[v]'
        run(['-i',str(src),'-i',str(pieces[i+1]),'-filter_complex',graph,'-map','[v]','-frames:v','60',*enc(),str(trans)]);joined.append(trans)
    listing=a.out/'concat.txt';listing.write_text(''.join("file '"+str(x)+"'\n" for x in joined))
    final=a.out/'029_picture_checkpoint.mp4';run(['-f','concat','-safe','0','-i',str(listing),'-c','copy',str(final)])
    run(['-i',str(final),'-f','null','-'])
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(final)]))
    frames=int(probe['streams'][0]['nb_read_frames']);assert frames==sum(x['frames'] for x in records)==round(c['duration_s']*30)
    narration=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',c['narration']]))
    assert abs(float(narration['format']['duration'])-frames/30)<.002
    report=dict(status='FULL_CHAPTER_PICTURE_CHECKPOINT_NOT_FINAL_QA',output=str(final),sha256=sha(final),frames=frames,duration_s=frames/30,chapter=c,source_master_sha256=covers['master_sha256'],slices=records,covers=mapped,removed_block_dissolves_s=[2,2],narration_duration_s=float(narration['format']['duration']),limitations=['Silent checkpoint, not UAT.','Bright source diagrams and original in-film hard cuts remain unresolved.','No quiet chapter title or four-second inter-film breath yet.','No whole-chapter picture_qa, final AV sync, final mux, compilation QA or NAS master/reel claim.'])
    (a.out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print(final,flush=True)
if __name__=='__main__':main()
