#!/usr/bin/env python3
"""Verify recorded gate exits and actual AAC identity; grants no creative approval."""
import hashlib,json,subprocess
from pathlib import Path
D=Path('/Users/benjaminoats/_desk/renders/J1100-S6-final02/S6_028_X768qs8sNQs')
OLD=Path('/Users/benjaminoats/_desk/renders/J1100-S6-final/S6_028_X768qs8sNQs/S6_028_X768qs8sNQs_v05.mp4')
def audio_hash(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
def main():
 s=json.loads((D/'FINAL_MEASUREMENTS.json').read_text())
 for k in ['shorts','picture','polish','sfx','music']:assert s[k]['exit_code']==0,(k,s[k])
 assert s['dark_pass'] and s['ocr_pass']
 a=s['audio_and_loop'];assert a['audio_pass'] and a['loop_pass'];assert -14.5<=a['I_LUFS']<=-13.5 and a['TP_dBTP']<=-1.6
 v=D/'S6_028_X768qs8sNQs_v05.mp4';old=audio_hash(OLD);new=audio_hash(v);assert old==new
 r={'status':'Automated gate evidence only; Gemini listening and Chief review separate','final_master':str(v),'sha256':hashlib.sha256(v.read_bytes()).hexdigest(),'diagnostic_audio_review_target':str(OLD),'aac_packet_hash_unchanged':True,'aac_packet_sha256':new,'gate_exits':{k:s[k]['exit_code'] for k in ['shorts','picture','polish','sfx','music']},'dark_pass':s['dark_pass'],'ocr_pass':s['ocr_pass']}
 (D/'FINAL_VERIFIED.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
