"""Compare implicit grayscale conversion with explicit legal-range luma at the failing Sun window.

These probes diagnose the measurement; no tolerance is relaxed.
"""
import subprocess as s,numpy as np
src='/Users/ben/_desk/J2452-sleep-scratch/public_sun_v03/022_sun_undarkened_v03.mp4';dst='/Users/ben/_desk/J2452-sleep-scratch/sun_grade_probes_v04/round8_442.mp4'
for vf in ['fps=4,scale=160:90,format=gray','fps=4,scale=160:90:in_range=tv:out_range=pc:flags=area+accurate_rnd,format=gray','fps=4,extractplanes=y,scale=160:90:flags=area,lut=y=(val-16)*255/219']:
 vals=[]
 for p,t in [(src,442),(dst,0)]:
  r=s.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',p,'-t','2','-vf',vf,'-pix_fmt','gray','-f','rawvideo','-']);vals.append(np.frombuffer(r,np.uint8).mean())
 print(vf,vals,vals[1]/vals[0])
