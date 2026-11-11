#!/usr/bin/env python3
"""Assemble checkpointed clean narration and existing bed, audio only."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
from build_sleep_bed import digest, measure, run

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--bed',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    chapters=json.loads(Path('jobs/reviews/J2452/narration_v03/ALL_CHAPTERS.json').read_text())['chapters']
    args=[];graph=[];labels=[];timeline=[];pos=0
    for i,c in enumerate(chapters):
        assert digest(c['output'])==c['sha256']
        report=json.loads(Path(c['report']).read_text())
        args+=['-i',c['output']]
        d=c['duration_s'];pad=4 if i<12 else 20
        graph.append(f'[{i}:a]apad=pad_dur={pad},atrim=duration={d+pad},asetpts=PTS-STARTPTS[n{i}]');labels.append(f'[n{i}]')
        timeline.append(dict(chapter=i+1,film=c['film'],start_s=round(pos,6),narration_end_s=round(pos+d,6),next_start_s=round(pos+d+pad,6),source_master_ranges=report.get('used_ranges',report.get('source_recipes')),report=c['report'],narration=c['output'],narration_sha256=c['sha256']))
        pos+=d+pad
    args+=['-i',str(a.bed)]
    graph.append(''.join(labels)+'concat=n=13:v=0:a=1[vo]')
    swells=[]
    for c in timeline[:-1]:
        start=c['narration_end_s']-3
        swells.append(f'if(between(t,{start},{start+4}),(t-{start})/4,if(between(t,{start+4},{start+6}),1,if(between(t,{start+6},{start+10}),({start+10}-t)/4,0)))')
    expr='1+0.2589254118*('+ '+'.join(swells)+')'
    graph.append(f"[13:a]volume='{expr}':eval=frame[bed]")
    graph.append('[vo][bed]amix=inputs=2:duration=first:normalize=0[mix]')
    raw=a.out/'sleep_mix_pre_master_v01.wav'
    run([*args,'-filter_complex',';'.join(graph),'-map','[mix]','-ar','48000','-c:a','pcm_s24le',str(raw)])
    first=run(['-i',str(raw),'-af','loudnorm=I=-20:TP=-6.2:LRA=5:print_format=json','-f','null','-'])
    levels=json.loads(re.findall(r'\{[^{}]+\}',first,re.S)[-1]);f='loudnorm=I=-20:TP=-6.2:LRA=5:linear=true:'+':'.join(f'{k}={levels[v]}' for k,v in [('measured_I','input_i'),('measured_TP','input_tp'),('measured_LRA','input_lra'),('measured_thresh','input_thresh'),('offset','target_offset')])
    output=a.out/'sleep_audio_master_candidate_v01.wav';run(['-i',str(raw),'-af',f,'-ar','48000','-c:a','pcm_s24le',str(output)])
    log=run(['-i',str(output),'-af','loudnorm=I=-20:TP=-6.2:LRA=5:print_format=json,silencedetect=n=-60dB:d=3','-f','null','-'])
    saved=json.loads(re.findall(r'\{[^{}]+\}',log,re.S)[-1]);gaps=re.findall(r'silence_duration: ([0-9.]+)',log)
    actual=float(json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(output)],text=True))['format']['duration'])
    assert abs(actual-pos)<.001
    assert -20.5<=float(saved['input_i'])<=-19.5
    assert float(saved['input_tp'])<=-6
    assert float(saved['input_lra'])<=5
    assert not gaps,gaps
    report=dict(status='AUDIO_CANDIDATE_ONLY_PICTURE_AND_FINAL_AV_QA_PENDING',output=str(output),sha256=digest(output),duration_s=actual,saved_levels=saved,silence_threshold_db=-60,silence_over_3s=gaps,chapters=timeline,bed=str(a.bed),bed_sha256=digest(a.bed),inter_film_breath_s=4,bed_join_envelope='2 dB lift; 4 s rise, 2 s hold, 4 s fall',final_fade_s=20,limitations='No listening claim. Picture timing must match this timeline or audio must be rebuilt. Final AAC true peak and full AV gates still pending.')
    (a.out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
