#!/usr/bin/env python3
"""Build an existing-house-music sleep bed; no generation or source overwrite."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path

def run(args):
    return subprocess.run(['ffmpeg','-hide_banner','-nostdin','-n',*args],capture_output=True,text=True,check=True).stderr

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def measure(path):
    log=run(['-i',str(path),'-af','loudnorm=I=-35:TP=-9:LRA=5:print_format=json','-f','null','-'])
    return json.loads(re.findall(r'\{[^{}]+\}',log,re.S)[-1])

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    source=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01_full.wav')
    inventory=json.loads(Path('jobs/reviews/J2452/narration_v03/ALL_CHAPTERS.json').read_text())
    # Twelve four-second inter-film breaths and the final twenty-second fade.
    duration=round(sum(c['duration_s'] for c in inventory['chapters'])+12*4+20,6)
    loop=a.out/'drone_loop_78s_v01.wav'
    # Phase: play 12..78, then blend 78..90 into 0..12. End meets start at t=12.
    graph='[0:a]atrim=0:90,asetpts=PTS-STARTPTS,lowpass=f=2800,highpass=f=55,asplit=3[m][t][h];[m]atrim=12:78,asetpts=PTS-STARTPTS[mid];[t]atrim=78:90,asetpts=PTS-STARTPTS[tail];[h]atrim=0:12,asetpts=PTS-STARTPTS[head];[tail][head]acrossfade=d=12:c1=qsin:c2=qsin[join];[mid][join]concat=n=2:v=0:a=1[out]'
    run(['-i',str(source),'-filter_complex',graph,'-map','[out]','-ar','48000','-ac','2','-c:a','pcm_s24le',str(loop)])
    levels=measure(loop);gain=-35-float(levels['input_i'])
    normalized=a.out/'drone_loop_78s_minus35_v01.wav'
    run(['-i',str(loop),'-af',f'volume={gain:.8f}dB','-c:a','pcm_s24le',str(normalized)])
    bed=a.out/'sleep_bed_provisional_timeline_v01.wav'
    # Final timing can change with picture transitions. Rebuild this cheap audio-only step then.
    run(['-stream_loop','-1','-i',str(normalized),'-t',str(duration),'-af',f'afade=t=in:d=2,afade=t=out:st={duration-20}:d=20','-c:a','pcm_s24le',str(bed)])
    saved=measure(bed)
    silence=run(['-i',str(bed),'-af','silencedetect=n=-60dB:d=3','-f','null','-'])
    gaps=[float(x) for x in re.findall(r'silence_duration: ([0-9.]+)',silence)]
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(bed)],text=True))
    actual=float(probe['format']['duration'])
    assert abs(actual-duration)<.001
    assert -35.5<=float(saved['input_i'])<=-34.5
    assert float(saved['input_tp'])<=-10
    assert not gaps, gaps
    report=dict(status='MUSIC_INTERMEDIATE_ONLY_NOT_FINAL_MIX',source=str(source),source_sha256=digest(source),source_interval_s=[0,90],loop_period_s=78,crossfade_s=12,crossfade_curve='qsin equal-power',filters=['lowpass 2800 Hz','highpass 55 Hz'],gain_db=gain,proposed_timeline=dict(narration_s=inventory['total_narration_duration_s'],breaths_s=48,final_fade_s=20,duration_s=duration),saved_duration_s=actual,saved_levels=saved,silence_threshold_db=-60,silence_gaps_over_3s=gaps,outputs=[dict(path=str(x),sha256=digest(x)) for x in [loop,normalized,bed]],limitations='No listening claim. Beatless/mood fit remains Ben watch. Picture join timing may change; re-render audio-only bed to final duration. No per-join +2 dB envelope yet; final mix loudness/peak/silence not checked.')
    (a.out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__': main()
