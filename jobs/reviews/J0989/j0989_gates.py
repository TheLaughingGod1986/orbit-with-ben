import pathlib,subprocess as sp,json,sys
R=pathlib.Path('/Users/benjaminoats/YouTube/orbit-with-ben');O=R/'02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports';S=O/'030_apophis_short_v13a';V=str(S)+'.mp4';E=pathlib.Path('/private/tmp/j0989-evidence');SA=R/'00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10'
commands={
'gate':['python3',R/'00_Brand/Channel-Setup/tools/gate_shorts_open.py','check',V,'--air-date','2026-10-28'],
'picture':['python3',R/'scripts/picture_qa.py',V,'--cuts',str(S)+'_cuts.json','--pool',str(S)+'_pool.json','--out-dir',O/'picture_qa_v13a'],
'polish':['python3',R/'scripts/polish_gate.py',V,'--cuts',str(S)+'_cuts.json','--out',str(S)+'_polish.json'],
'music':['python3',R/'scripts/music_gate.py',O.parents[2],'--bed',O.parents[2]/'05_Music/owb-standalone-shorts_score_bed_v01.mp3','--video',V,'--out',str(S)+'_music.json'],
'sfx':['python3',R/'scripts/sfx_kit.py','level','--vo',str(S)+'_stems/stem_vo.wav','--sfx',str(S)+'_stems/stem_sfx.wav','--bed',str(S)+'_stems/stem_bed.wav','--minutes',str(18.833333/60)]}
results={}
for k,c in commands.items():
 print('RUN',k,flush=True);p=sp.run(list(map(str,c)),cwd=R,capture_output=True,text=True);(E/(k+'.txt')).write_text(p.stdout+p.stderr);(O/(S.name+'_'+k+'.txt')).write_text(p.stdout+p.stderr);results[k]=p.returncode;print(k,p.returncode,(p.stdout+p.stderr)[-1500:],flush=True)
sys.path.insert(0,str(R/'scripts'));from short_c37 import finish_scan,loop_metrics
try:
 m=finish_scan(pathlib.Path(V),loop_metrics(pathlib.Path(V)));m={k:v for k,v in m.items() if k not in ['steps','frames_arr']};(E/'finish_loop.json').write_text(json.dumps(m,indent=2));results['finish_loop']=0
except BaseException as e:
 (E/'finish_loop.json').write_text(str(e));results['finish_loop']=1
(E/'gate_results.json').write_text(json.dumps(results,indent=2));print(results,flush=True)
