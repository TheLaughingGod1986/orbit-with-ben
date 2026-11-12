#!/usr/bin/env python3
"""Independent saved AAC loudness, true-peak, silence and duration read-back."""
import json,re,subprocess as sp,hashlib
from pathlib import Path
S=(Path.home()/'_desk/J2452-sleep-scratch/final_join_v01');p=S/'sleep_audio_encoded_v05.m4a'
log=S/'AAC_V05_READBACK.log'
with log.open('w') as f:
 sp.run(['ffmpeg','-nostdin','-v','info','-i',str(p),'-af','ebur128=peak=true,silencedetect=noise=-60dB:d=3','-f','null','-'],stdout=f,stderr=sp.STDOUT,check=True,timeout=240)
t=log.read_text();summary=t.rsplit('Summary:',1)[-1];i=float(re.search(r'I:\s*([-\d.]+) LUFS',summary)[1]);peak=float(re.search(r'Peak:\s*([-\d.]+) dBFS',summary)[1]);sil=re.findall(r'silence_duration:\s*([\d.]+)',t)
d=float(sp.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)]));h=hashlib.sha256(p.read_bytes()).hexdigest()
r=dict(status='PASS' if -20.7<=i<=-19.5 and peak<=-6 and not sil and abs(d-6502.333333)<.05 else 'FAIL',path=str(p),sha256=h,duration_s=d,integrated_lufs=i,true_peak_dbtp=peak,silence_over_3s=sil,encoder='native AAC fast coder, 192kbps',basis='Independent full saved AAC decode with EBU R128 oversampled true peak and -60dB silence detection. No listening claim.')
(S/'AAC_V05_READBACK.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
