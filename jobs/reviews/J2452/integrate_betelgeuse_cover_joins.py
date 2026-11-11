#!/usr/bin/env python3
"""Build bounded cover-join candidates, never a completed chapter or UAT cut."""
import argparse, hashlib, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def run(args):
    return subprocess.run(args,check=True,capture_output=True,text=True)
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def source_geometry(master,start,duration):
    frames=json.loads(run(['ffprobe','-v','error','-read_intervals',f'{start}%+{duration}',
        '-select_streams','v','-show_frames','-show_entries',
        'frame=best_effort_timestamp_time,width,height,pix_fmt,color_space','-of','json',str(master)]).stdout)['frames']
    assert frames and all((f['width'],f['height'],f['pix_fmt'])==(1920,1080,'yuv420p') for f in frames), 'reinit_filter=0 requires fixed input geometry'
    times=[float(f['best_effort_timestamp_time']) for f in frames]
    assert all(b>a for a,b in zip(times,times[1:])), 'Non-monotonic source PTS'
    return dict(frames_checked=len(frames),geometry=[1920,1080,'yuv420p'],colour_spaces=sorted({f.get('color_space','unknown') for f in frames}),pts_strictly_increasing=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    r=json.loads((ROOT/'jobs/reviews/J2452/betelgeuse_orbit_readback_v01.json').read_text())
    a.out.mkdir(parents=True,exist_ok=False)
    master=Path(r['master']);assert sha(master)==r['master_sha256']
    results=[]
    for n,c in enumerate(r['covers'],1):
        cover=Path(c['output']);assert sha(cover)==c['sha256']
        start=c['master_in_s']-4; span=c['master_out_s']-c['master_in_s']; frames=round((span+8)*30)
        # The concatenated master changes colour metadata at source cuts. Keep the
        # bounded, fixed-size graph alive so these changes cannot reset cover PTS.
        # Ten-frame opaque safety margin includes quantisation/VFR boundary error.
        # All fades happen outside the nominal Orbit interval. Endpoint padding
        # holds only the replacement, never a source frame containing Orbit.
        geometry=source_geometry(master,start,frames/30)
        margin=10/30; fade=2; on=4-margin; off=4+span+margin
        padded=off-on+2*fade
        graph=(f'[0:v]fps=30,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1,colorchannelmixer=rr=.85:gg=.85:bb=.85,format=yuv420p,limiter=min=16:max=180:planes=1,format=rgb24[base];'
               f'[1:v]fps=30,setpts=PTS-STARTPTS,scale=in_color_matrix=bt601,format=rgba,tpad=start_mode=clone:start_duration={fade+margin}:stop_mode=clone:stop_duration={fade+margin},trim=duration={padded},format=rgba,fade=t=in:st=0:d=2:alpha=1,fade=t=out:st={padded-fade}:d=2:alpha=1,setpts=PTS+{on-fade}/TB[cover];'
               '[base][cover]overlay=eof_action=pass:format=rgb,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]')
        dest=a.out/f'join_{n:02d}_candidate.mp4'
        run(['ffmpeg','-hide_banner','-nostdin','-loglevel','error','-n','-reinit_filter','0','-ss',str(start),'-i',str(master),'-i',str(cover),'-filter_complex',graph,'-map','[v]','-frames:v',str(frames),'-an','-c:v','libx264','-preset','fast','-crf','18','-r','30','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-video_track_timescale','90000',str(dest)])
        run(['ffmpeg','-hide_banner','-nostdin','-loglevel','error','-i',str(dest),'-f','null','-'])
        probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(dest)]).stdout)['streams'][0]
        assert int(probe['nb_read_frames'])==frames
        results.append(dict(output=str(dest),sha256=sha(dest),frames=frames,duration_s=frames/30,master_range_s=[start,start+frames/30],nominal_orbit_local_s=[4,4+span],fully_opaque_local_s=[on,off],fade_duration_s=fade,cover_sha256=c['sha256'],cover_matrix_conversion='untagged component default BT.601 to output BT.709',graph=graph,source_geometry=geometry,status='JOIN_CANDIDATE_NOT_CHAPTER_QA'))
        print(f'join {n}: {frames} frames decoded',flush=True)
    report=dict(status='TWO_LOCAL_JOIN_CANDIDATES_NOT_FINAL_CHAPTER',joins=results,limitations=['No audio; narration clock unchanged by these local picture tests.','Adjacent source diagrams remain: these candidates do not resolve the chapter bright-graphic recipe.','No whole-chapter, final compilation, loudness, silence or UAT claim.','Inspect exact output frames at opaque and dissolve endpoints before adoption.'])
    (a.out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
