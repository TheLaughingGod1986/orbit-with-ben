"""Focused experimental regressions. Does not exercise or alter production verdicts."""
import sys, unittest, subprocess, tempfile
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'scripts'))
import music_gate as mg
import candidate

class EnvelopeConfound(unittest.TestCase):
    def test_independent_waveforms_with_shared_envelope(self):
        rng=np.random.default_rng(2795)
        t=np.arange(120*mg.SR)/mg.SR
        envelope=.01+.49*(t/120)**2
        a=(rng.standard_normal(len(t))*envelope).astype(np.float32)
        b=(rng.standard_normal(len(t))*envelope).astype(np.float32)
        self.assertGreaterEqual(mg.similarity(mg.frames(a),mg.frames(b)),mg.SIM_FAIL)
        self.assertLess(mg.similarity(candidate.frames(a),candidate.frames(b)),mg.SIM_FAIL)

    def test_genuine_reuse_gain_and_offset(self):
        rng=np.random.default_rng(42)
        t=np.arange(120*mg.SR)/mg.SR
        y=np.zeros(len(t),np.float32)
        for i in range(30):
            u=t[i*4*mg.SR:(i+1)*4*mg.SR]-i*4
            f=110*2**(rng.integers(0,24)/12)
            y[i*4*mg.SR:(i+1)*4*mg.SR]=np.sin(2*np.pi*f*u)*np.exp(-.3*u)
        a=candidate.frames(y)
        for b in (y,y*.25,y[13*mg.SR:]*.25):
            with self.subTest(seconds=len(b)/mg.SR):
                self.assertGreaterEqual(mg.similarity(a,candidate.frames(b)),mg.SIM_FAIL)

    def test_reencoded_trimmed_recording(self):
        rng=np.random.default_rng(7)
        t=np.arange(90*mg.SR)/mg.SR
        x=np.zeros(len(t),np.float32)
        for i in range(30):
            sl=slice(i*3*mg.SR,(i+1)*3*mg.SR)
            f=110*2**(rng.integers(0,24)/12)
            x[sl]=.4*np.sin(2*np.pi*f*t[sl])
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'trimmed.mp3'
            subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar',str(mg.SR),'-ac','1','-i','-','-b:a','32k',str(path)],input=(x[13*mg.SR:]*.25).tobytes(),check=True)
            self.assertGreaterEqual(mg.similarity(candidate.frames(x),candidate.frames(mg.decode(path))),mg.SIM_FAIL)

if __name__=='__main__':unittest.main()
