#!/usr/bin/env python3
"""Save a verified chapter additively to its own working-film folder."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image, ImageDraw

SRC=Path('/Users/ben/_desk/J2452-sleep-scratch/public_saturn_v03')
DEST=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/j2452/public_chapters_v01/021_saturn_v03')

def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    global SRC, DEST
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=SRC)
    parser.add_argument('--destination', type=Path, default=DEST)
    args = parser.parse_args()
    SRC, DEST = args.source, args.destination
    allowed = Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/j2452/public_chapters_v01')
    assert DEST.parent.resolve() == allowed.resolve(), 'Save only inside this film chapter folder'
    read=json.loads((SRC/'READBACK.json').read_text())
    build=json.loads((SRC/'BUILD.json').read_text())
    assert read['gate_exit_codes'] in ([0,0],[1,0]), read['gate_exit_codes']
    assert all(x['classification']=='in the public film' for x in read['inherited_findings'])
    assert float(read['levels']['input_tp']) <= -6, 'Encoded narration exceeds peak ceiling'
    assert read['full_decode_exit']==0 and read['decoded_frames']==build['expected_frames']
    assert sha(Path(read['output']))==read['sha256']==build['sha256']
    assert Path('/Volumes/data').is_mount(), 'NAS not mounted'
    # Keep the five individual bright-window frames together in one review sheet.
    sheet=Image.new('RGB',(960,5*294),'#161616'); draw=ImageDraw.Draw(sheet)
    for k,w in enumerate(read['brightest_two_second_windows']):
        im=Image.open(w['frame']).convert('RGB'); im.thumbnail((480,270))
        sheet.paste(im,(0,k*294))
        draw.text((490,k*294+12),f"{w['start_s']:.2f}-{w['end_s']:.2f}s\nMean luma {w['mean_luma']:.2f}",fill='white')
    sheet.save(SRC/'BRIGHTEST_WINDOWS.jpg',quality=90)
    DEST.mkdir(parents=True,exist_ok=False)
    files=[Path(read['output']),SRC/'BRIGHTEST_WINDOWS.jpg']
    copies=[]
    for p in files:
        target=DEST/p.name
        with p.open('rb') as src,target.open('xb') as dst: shutil.copyfileobj(src,dst,1048576)
        digest=sha(target)
        assert digest==sha(p), 'Destination hash mismatch'
        copies.append(dict(path=str(target),sha256=digest,bytes=target.stat().st_size))
    record=dict(status='CHAPTER_SAVED_NOT_FINAL_UAT',build=build,readback=read,copies=copies,
                notes='Public-film charts and labels retained; dissolves only on compilation edits. Second chapter precedes darkening ramp, so identity darkening. Four-second breath, single bed and final sound gates are still owed. Any pixel FAIL retained here is inherited, never presented as PASS. Join QA passes with warnings for Chief review.')
    (DEST/'CHAPTER.json').write_text(json.dumps(record,indent=2)+'\n')
    assert json.loads((DEST/'CHAPTER.json').read_text())==record
    (SRC/'NAS_COPY.json').write_text(json.dumps(dict(destination=str(DEST),copies=copies,record_sha256=sha(DEST/'CHAPTER.json')),indent=2)+'\n')
    print(json.dumps(copies,indent=2))

if __name__=='__main__': main()
