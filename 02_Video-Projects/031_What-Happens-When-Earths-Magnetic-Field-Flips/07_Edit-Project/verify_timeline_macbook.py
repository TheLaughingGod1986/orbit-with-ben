#!/usr/bin/env python3
"""Recheck J2141 timeline media and locked cues; creates static contact sheet.

Technical evidence only. Does not approve moving-plate composites or film QA.
"""
import hashlib
import io
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent

def main():
    manifest = json.loads((HERE/'CODE_TIMELINE_MACBOOK_v01.json').read_text())
    words_path = HERE.parent/'02_Voiceover/stt/magnetic_field_flip_vo_v02a/stt_raw.json'
    assert hashlib.sha256(words_path.read_bytes()).hexdigest() == manifest['locked_words_sha256']
    words = [w for w in json.loads(words_path.read_text())['words'] if w.get('type') == 'word']
    checks = []
    sheet = Image.new('RGB', (1600, 5*210), (28, 43, 63))
    for row_index, record in enumerate(manifest['graphics']):
        media = Path(record['path'])
        digest = hashlib.sha256(media.read_bytes()).hexdigest()
        assert digest == record['sha256']
        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(media)]))
        assert len(probe['streams']) == 1
        stream = probe['streams'][0]
        assert (stream['width'], stream['height'], stream['pix_fmt'], stream['r_frame_rate']) == (1920,1080,'argb','25/1')
        assert abs(float(probe['format']['duration']) - record['duration_s']) < .02
        start = record['start_s']
        cue = [w['text'] for w in words if abs(w['start'] - start) < .001]
        assert cue == [record['current']+','], (cue,record)
        decoded = subprocess.run(['ffmpeg','-v','error','-i',str(media),'-f','null','-'],capture_output=True,check=True)
        assert not decoded.stderr
        samples = []
        for j, seconds in enumerate([0,.6,1.4,2.4,3.56]):
            png = subprocess.check_output(['ffmpeg','-v','error','-ss',str(seconds),'-i',str(media),'-frames:v','1','-f','image2pipe','-c:v','png','-'])
            frame = Image.open(io.BytesIO(png)).convert('RGBA')
            bbox = frame.getchannel('A').getbbox()
            if seconds == 0: assert bbox is None
            else: assert bbox and bbox[0] >= 100 and bbox[2] <= 1820 and bbox[3] < 600
            bg = Image.new('RGBA',frame.size,(28,43,63,255)); bg.alpha_composite(frame)
            tile = bg.convert('RGB').resize((320,180))
            sheet.paste(tile,(j*320,row_index*210))
            ImageDraw.Draw(sheet).text((j*320+8,row_index*210+184),f"R{record['row']} +{seconds:.2f}s", fill='white')
            samples.append(dict(seconds=seconds,alpha_bbox=bbox,decoded_rgba_sha256=hashlib.sha256(frame.tobytes()).hexdigest()))
        checks.append(dict(row=record['row'],path=str(media),sha256=digest,locked_cue=cue,full_decode='PASS',format='PASS',duration_s=float(probe['format']['duration']),samples=samples))
    contact = Path(manifest['graphics'][0]['path']).parent/'CONTACT_TECHNICAL_v01.jpg'
    sheet.save(contact,quality=92)
    report = dict(job='J2141',status='technical_checks_only',spend_gbp=0,checks=checks,contact_sheet=str(contact),contact_sheet_sha256=hashlib.sha256(contact.read_bytes()).hexdigest(),limitations=['Static samples only; no playback or audio perception claimed.','Moving graded plates, subject clearance, WHEN overlap replacement and film gates remain unfinished.'])
    (HERE/'CODE_TIMELINE_MACBOOK_TECHNICAL_CHECK_v01.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'{len(checks)} timeline candidates verified; {contact}')

if __name__ == '__main__':
    main()
