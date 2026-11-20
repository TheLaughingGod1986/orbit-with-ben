#!/usr/bin/env python3
"""Prepare licensed archive originals and a word-aligned EDL. No render or approval."""
import subprocess
import argparse,csv,difflib,hashlib,html,json,pathlib,re,urllib.parse,wave
from PIL import Image

def fetch(url):
    return subprocess.check_output(['curl','--fail','--silent','--show-error','--location','--max-time','45',url])

def tokens(text):return re.findall(r"[a-z0-9]+",text.lower().replace('’',"'"))

def main():
    a=argparse.ArgumentParser();a.add_argument('--media',type=pathlib.Path,required=True);a.add_argument('--harvest',action='store_true');args=a.parse_args()
    film=pathlib.Path(__file__).resolve().parents[1];out=film/'07_Edit';media=args.media
    assets=json.loads((film/'03_Picture/archive_assets_v03.json').read_text()); records=[]
    if args.harvest:
        archive=media/'03_Picture/archive';archive.mkdir(parents=True,exist_ok=True)
        for key,asset in assets.items():
            record={'key':key,**asset,'checked_at':'2026-11-18','status':'unresolved'}
            try:
                page=fetch(asset['url']).decode();(archive/f'{key}_catalogue.html').write_text(page)
                if 'commons.wikimedia.org' in asset['url']:
                    if 'public domain' not in page.lower():raise ValueError('Public-domain evidence missing')
                    m=re.search(r'class="fullImageLink"[^>]*>\s*<a href="([^"]+)"',page)
                    if not m:raise ValueError('Original image link missing')
                    url=html.unescape(m[1])
                else:
                    links=re.findall(r'(?:href|src)="([^"]+\.(?:jpg|JPG|jpeg)(?:\?[^"]*)?)"',page)
                    links=[urllib.parse.urljoin(asset['url'],html.unescape(x)) for x in links if asset['id'].lower().replace('-','') in x.lower().replace('-','') or asset['id'].lower() in x.lower()]
                    if not links:raise ValueError('No identifiable catalogue image link')
                    url=sorted(links,key=lambda x:('download' in x.lower(),'large' in x.lower()),reverse=True)[0]
                try:data=fetch(url)
                except Exception:
                    alternate=re.search(r'https://thumb.wikimedia.org/[^\"<> ]+/1280px-[^\"<> ]+',page)
                    if not alternate:raise
                    url=html.unescape(alternate[0]);data=fetch(url)
                path=archive/f'{key}.jpg';path.write_bytes(data)
                with Image.open(path) as im:im.verify()
                with Image.open(path) as im:size=list(im.size)
                record.update(status='downloaded_pending_visual_review',file=str(path),download_url=url,sha256=hashlib.sha256(data).hexdigest(),pixels=size,catalogue_sha256=hashlib.sha256(page.encode()).hexdigest())
            except Exception as e:record['error']=str(e)
            records.append(record);print(key,record['status'],record.get('error',''),flush=True)
        (out/'ARCHIVE_HARVEST.json').write_text(json.dumps(records,indent=2)+'\n')
    stt=json.loads((media/'02_Voiceover/stt/atlantic_black_pit_vo_v01/stt_raw.json').read_text())
    observed=[];times=[]
    for w in stt['words']:
        if w.get('type')!='word':continue
        for t in tokens(w['text']):observed.append(t);times.append((w['start'],w['end']))
    rows=list(csv.DictReader((film/'03_Picture/SHOT_LIST_v03.csv').open()));expected=[];spans=[]
    for r in rows:
        start=len(expected);expected.extend(tokens(r['narration']));spans.append((start,len(expected)))
    matches={}
    for block in difflib.SequenceMatcher(None,expected,observed,autojunk=False).get_matching_blocks():
        for k in range(block.size):matches[block.a+k]=block.b+k
    edl=[]
    for row,(start,end) in zip(rows,spans):
        hit=[i for i in range(start,end) if i in matches]
        if not hit:raise ValueError('No timing anchors for '+row['shot_id'])
        first,last=hit[0],hit[-1];t0=times[matches[first]][0];t1=times[matches[last]][1]
        edl.append({**row,'speech_start_s':round(t0,3),'speech_end_s':round(t1,3),'boundary_review':first!=start or last!=end-1,'matched_tokens':len(hit),'expected_tokens':end-start})
    with wave.open(str(media/'02_Voiceover/atlantic_black_pit_vo_v01.wav')) as wav:
        duration=wav.getnframes()/wav.getframerate()
    for i,row in enumerate(edl):
        row['cut_start_s']=0 if i==0 else round((edl[i-1]['speech_end_s']+row['speech_start_s'])/2,3)
        row['cut_end_s']=round((row['speech_end_s']+edl[i+1]['speech_start_s'])/2,3) if i+1<len(edl) else round(duration+2,3)
        if row['cut_end_s']<=row['cut_start_s']:raise ValueError('Nonpositive shot '+row['shot_id'])
    payload={'state':'assembly_plan_not_picture_approval','audio_sha256':hashlib.sha256((media/'02_Voiceover/atlantic_black_pit_vo_v01.wav').read_bytes()).hexdigest(),'alignment':'Exact lexical anchors from Scribe; unmatched boundary tokens require manual timing verification; cuts in inter-sentence gaps. No audio perception claimed.','rows':edl}
    (out/'EDL_v01.json').write_text(json.dumps(payload,indent=2)+'\n')
    print('EDL',len(edl),'rows;',sum(r['boundary_review'] for r in edl),'boundaries to check')
if __name__=='__main__':main()
