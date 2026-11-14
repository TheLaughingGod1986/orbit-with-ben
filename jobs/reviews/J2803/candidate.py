"""EXPERIMENT ONLY. Not a production gate or authority to clear a failed bed.
Remove the common log-energy component before existing temporal normalization.
The fixed +1 in log1p prevents exact gain invariance at low energy; this is
an uncalibrated feature proposal, requiring wider music validation.
"""
import numpy as np
import music_gate as mg

def frames(x):
    n=len(x)//mg.SR
    if n<4:return np.zeros((0,mg.BANDS),np.float32)
    spec=np.abs(np.fft.rfft(x[:n*mg.SR].reshape(n,mg.SR)*np.hanning(mg.SR),axis=1))**2
    edges=np.geomspace(60,3800,mg.BANDS+1).astype(int)
    e=np.log1p(np.stack([spec[:,a:b].sum(1) for a,b in zip(edges[:-1],edges[1:])],1))
    e-=e.mean(1,keepdims=True)
    e-=e.mean(0)
    return e/(np.linalg.norm(e,axis=1,keepdims=True)+1e-9)
