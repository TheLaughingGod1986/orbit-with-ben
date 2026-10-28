#!/usr/bin/env python3
"""J1032 locked v07 assembly. Produces UNREVIEWED media; never publishes or passes it.
Run from a clean job worktree; media resolve against --media-root, output on durable desk.
Existing outputs are never overwritten. Final gates and multimodal listening are separate.
"""
import argparse, hashlib, importlib.util, json, math, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

LOCK = '51df8a7cc95959cb895121a2cd007e20352f910dd5ac40f0600b1b9120f058dc'
ROOT = Path(__file__).resolve().parents[2]
FONT = '/System/Library/Fonts/Supplemental/Arial Black.ttf'
W,H,FPS = 1080,1920,30

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()

def run(args): subprocess.run([str(x) for x in args],check=True)
def ff(args): run(['ffmpeg','-nostdin','-y','-v','error',*args])
def dump(p,obj): p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def load_module(p):
    spec=importlib.util.spec_from_file_location('legacy_mix',p)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def text(im,rows,y,size=70,yellow=False,alpha=255):
    d=ImageDraw.Draw(im)
    for row in rows:
        fs=size
        while True:
            font=ImageFont.truetype(FONT,fs)
            box=d.textbbox((0,0),row,font=font,stroke_width=5)
            if box[2]-box[0]<960 or fs<=28: break
            fs-=2
        width=box[2]-box[0]
        d.text(((W-width)/2-box[0],y-box[1]),row,font=font,
               fill=(255,214,0,alpha) if yellow else (255,255,255,alpha),
               stroke_width=5,stroke_fill=(0,0,0,alpha))
        y+=size+14

def overlays(s,work,total,key):
    words=[w for sp in s['vo_splice_map']['subspans'] for w in sp['words']]
    groups=[];g=[]
    for w in words:
        g.append(w)
        if len(g)==3 or w['word'][-1:] in '.,?!': groups.append(g);g=[]
    if g:groups.append(g)
    title=[];line=''
    for word in s['local_title'].split():
        if len(line+' '+word)>26: title.append(line);line=word
        else: line=(line+' '+word).strip()
    if line:title.append(line)
    card=s['single_teaching_overlay'];a,b=card['timeline_in'],card['timeline_out']
    folder=work/'overlays';folder.mkdir()
    # Match hook text/style to accepted preparation; repeat at loop for pixel continuity.
    accepted_overlay=Image.open(Path('/Users/benjaminoats/_desk/reviews/J1017/openings')/(key+'_v04_overlay.png')).convert('RGBA')
    accepted_overlay.paste((0,0,0,0),(0,1400,1080,1920))
    for n in range(math.ceil(total*FPS)):
        t=n/FPS;im=Image.new('RGBA',(W,H))
        if t<2 or t>=s['vo_splice_map']['vo_end_s']:
            im=accepted_overlay.copy()
        if 9<=t<14: text(im,title,820,58)
        if a<=t<b:
            q=min(1,(t-a)/.35,(b-t)/.35);q=max(0,q)
            # cubic ease on entry, alpha ease on exit, no still card >4 seconds.
            eased=1-(1-q)**3
            text(im,card['card_text'],int(840+18*(1-eased)),70,True,round(eased*255))
        for i,g in enumerate(groups):
            stop=groups[i+1][0]['start'] if i+1<len(groups) else g[-1]['end']+.05
            if 0<=t<s['vo_splice_map']['vo_end_s'] and g[0]['start']<=t<stop:
                text(im,[' '.join(w['word'] for w in g).upper()],1498,54);break
        # First/last caption also matches for loop. Exact pixel loop measured later.
        im.save(folder/f'{n:05d}.png')
    return folder

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--media-root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--preflight',action='store_true')
    args=ap.parse_args();media=args.media_root
    mp=ROOT/'jobs/reviews/J1100/maps_s2.json';assert sha(mp)==LOCK
    data=json.loads(mp.read_text());checked={}
    def resolve(p):
        p=Path(p);return p if p.is_absolute() else media/p
    for key,s in data['shorts'].items():
        au=s['vo_splice_map']['auditions']['full_vo_audition'];assert sha(au['wav_path'])==au['sha256']
        for r in s['shot_plan'][:-1]:
            p=resolve(r['source_path'])
            if str(p) not in checked:checked[str(p)]=sha(p)
            assert checked[str(p)]==r['source_sha256'],str(p)
    print('Preflight PASS: locked map, all six accepted WAVs and all source hashes',flush=True)
    if args.preflight:return
    assert shutil.disk_usage(media).free>=20_000_000_000,'Disk under 20 GB; archive first'
    args.out.mkdir(parents=True,exist_ok=True)
    legacy=load_module(media/'02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/mon30_comets/_assemble_mon30_comets_v03.py')
    for key,s in data['shorts'].items():
        out=args.out/key;out.mkdir(exist_ok=True)
        if (out/'RENDER_COMPLETE.json').exists():print('already rendered',key,flush=True);continue
        work=Path('/private/tmp')/('j1100_'+key)
        work.mkdir(exist_ok=True);legacy.WORK=work
        total=s['vo_splice_map']['total_duration_s'];plan=s['shot_plan'];parts=[]
        print('START',key,flush=True)
        for i,r in enumerate(plan):
            print('shot',key,r['row'],flush=True)
            dest=work/f's{i:02d}.mp4'
            if dest.exists():
                parts.append(dest);continue
            # Cumulative frame boundaries prevent per-shot rounding drift.
            frames=round(r['timeline_out']*FPS)-round(r['timeline_in']*FPS)
            if i==len(plan)-1:
                ff(['-t','1','-i',parts[0],'-an','-vf','reverse,fps=30,format=yuv420p','-frames:v',frames,'-c:v','libx264','-preset','veryfast','-crf','16',dest])
            else:
                vf=r.get('crop_filter','crop=ih*9/16:ih,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p')
                ff(['-ss',r['source_in'],'-t',r['source_dur']+.15,'-i',resolve(r['source_path']),'-an','-vf',vf,'-frames:v',frames,'-c:v','libx264','-preset','veryfast','-crf','16',dest])
            parts.append(dest)
        (work/'concat.txt').write_text(''.join(f"file '{p}'\n" for p in parts))
        ff(['-f','concat','-safe','0','-i',work/'concat.txt','-c','copy',work/'picture.mp4'])
        film=next((media/'02_Video-Projects').glob(s['film'].split(':')[1]+'_*'))
        bed=film/'05_Music'/({'026':'nearest-star_score_bed_v01_full.wav','027':'earth-spin_score_take2_straight_v01j.wav','028':'gliese_score_bed_v03.mp3'}[s['film'].split(':')[1]])
        if not bed.exists():raise RuntimeError(f'Confirm exact own-film bed path: {bed}')
        au=s['vo_splice_map']['auditions']['full_vo_audition']
        ff(['-i',au['wav_path'],'-af',f'apad=whole_dur={total}','-t',total,'-ac','2','-ar','48000',out/'stem_vo.wav'])
        vo_i=legacy.lufs(out/'stem_vo.wav')
        ff(['-stream_loop','-1','-ss',180 if s['film']=='OWB:026' else 0,'-i',bed,'-t',total,'-ac','2','-ar','48000',work/'bed_raw.wav'])
        gain=vo_i-22-legacy.lufs(work/'bed_raw.wav')
        ff(['-i',work/'bed_raw.wav','-af',f'volume={gain}dB',out/'stem_bed.wav'])
        kit=film/'06_Sound-Effects/kit_v01/sfx_owb_whoosh_soft_v01.wav'
        ff(['-i',kit,'-af',f'apad=whole_dur={total}','-t',total,'-ac','2','-ar','48000',work/'sfx_raw.wav'])
        gain=vo_i-24-legacy.lufs(work/'sfx_raw.wav')
        ff(['-i',work/'sfx_raw.wav','-af',f'volume={gain}dB',out/'stem_sfx.wav'])
        legacy.fit_mix(out/'stem_vo.wav',out/'stem_bed.wav',out/'stem_sfx.wav',total,work/'mix.wav')
        folder=overlays(s,work,total,key)
        final=out/(key+'_v05.mp4')
        ff(['-i',work/'picture.mp4','-framerate',30,'-i',folder/'%05d.png','-i',work/'mix.wav','-filter_complex','[0:v][1:v]overlay=0:0,format=yuv420p[v]','-map','[v]','-map','2:a','-c:v','libx264','-preset','fast','-crf','18','-c:a','aac','-b:a','192k','-t',total,'-movflags','+faststart',final])
        stats=legacy.ebur128_stats(final)
        dump(out/'audio_measurement.json',{'I_LUFS':stats[0],'TP_dBTP':stats[1],'pass':-14.5<=stats[0]<=-13.5 and stats[1]<=-1.6})
        ff(['-i',final,'-vf','scale=720:1280:flags=lanczos','-c:v','libx264','-preset','fast','-crf','20','-c:a','copy',out/(key+'_v05_PHONE.mp4')])
        dump(out/'locked_shots.json',plan);dump(out/'locked_preparation.json',s)
        dump(out/'input_hashes.json',{'map_sha256':LOCK,'accepted_vo_sha256':au['sha256'],'bed_path':str(bed),'bed_sha256':sha(bed),'source_hashes':checked})
        dump(out/'RENDER_COMPLETE.json',{'status':'UNREVIEWED; final gates and audio listening still required','map_sha256':LOCK,'files':{p.name:sha(p) for p in out.iterdir() if p.is_file()}})
        print('RENDERED UNREVIEWED',key,flush=True)

if __name__=='__main__':main()
