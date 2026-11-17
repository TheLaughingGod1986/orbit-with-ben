"""Read-only reproduction; no gate result is changed. Run from this checkout."""
import ast, hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'scripts'))
import music_gate as mg
import candidate
BASE=Path('/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/05_Music')
BED=BASE/'hos_009_score_joined_v01.wav'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def detail(a,b):
    m=a@b.T; rows=[]
    for lag in range(-(len(a)-20),len(b)-19):
        d=np.diagonal(m,offset=lag)
        if len(d)>=20: rows.append((float(d.mean()),lag,len(d)))
    s,lag,n=max(rows)
    return dict(score=s,lag=lag,overlap=n,a_start=max(0,-lag),b_start=max(0,lag))
def main():
    saved=json.loads(Path(__file__).with_name('RESULTS.json').read_text())
    files=[Path(row['file']) for row in saved['inventory']]
    roots=saved['roots']
    result={'gate_sha256':sha(Path(mg.__file__)),'bed_sha256':sha(BED),'roots':roots,'inventory':[],'controls':{}}
    x=mg.decode(BED); a=mg.frames(x); ca=candidate.frames(x)
    for p in files:
        actual=p
        if 'com~apple~CloudDocs' in str(p):
            mapped=Path('/Volumes/MiniWork/scratch/j2664/uat_materialized')/(p.parent.name+'__'+p.name)
            if mapped.exists():actual=mapped
        row={'file':str(p),'read_from':str(actual)}
        try:
            y=mg.decode(actual)
            row.update(sha256=sha(actual),**detail(a,mg.frames(y)))
            row['experimental']=detail(ca,candidate.frames(y))
            print(p.name,round(row['score'],3),flush=True)
        except Exception as e:row['error']=str(e)
        result['inventory'].append(row)
    c=result['controls']
    c['identical']=detail(a,a)
    c['same_audio_gain_minus12dB']=detail(a,mg.frames(x*10**(-12/20)))
    c['same_audio_trim37s_gain_minus12dB']=detail(a,mg.frames(x[37*mg.SR:]*10**(-12/20)))
    # Independent deterministic compositions: disjoint pitches, same envelope.
    # No shared audio samples, random seeds or note sequence. Analytical control,
    # not an auditory judgment about the production recordings.
    t=np.arange(120*mg.SR)/mg.SR
    def compose(notes):
        y=np.zeros_like(t)
        for i,note in enumerate(notes):
            sl=slice(i*10*mg.SR,(i+1)*10*mg.SR)
            u=t[sl]-i*10
            f=110*2**(note/12)
            y[sl]=(.1+.9*np.sin(np.pi*u/10)**2)*(np.sin(2*np.pi*f*u)+.3*np.sin(4*np.pi*f*u))
        return y.astype(np.float32)
    one=compose([0,4,7,12,7,4,0,7,4,12,4,0])
    two=compose([2,9,5,14,5,9,2,5,9,14,9,2])
    c['independent_disjoint_pitch_compositions']=detail(mg.frames(one),mg.frames(two))
    # Independent carriers with common slow loudness arc, no shared waveform.
    rng=np.random.default_rng(2795)
    u=np.arange(120*mg.SR)/mg.SR
    envv=.01+.49*(u/120)**2
    n1=(rng.standard_normal(len(u))*envv).astype(np.float32)
    n2=(rng.standard_normal(len(u))*envv).astype(np.float32)
    c['independent_noise_shared_envelope']=detail(mg.frames(n1),mg.frames(n2))
    for k,y in [('composition_a',one),('composition_b',two),('noise_a',n1),('noise_b',n2)]:
        result.setdefault('control_pcm_sha256',{})[k]=hashlib.sha256(y.tobytes()).hexdigest()
    result['experimental_controls']={
        'identical':detail(ca,ca),
        'gain':detail(ca,candidate.frames(x*10**(-12/20))),
        'trim_gain':detail(ca,candidate.frames(x[37*mg.SR:]*10**(-12/20))),
        'independent_compositions':detail(candidate.frames(one),candidate.frames(two)),
        'independent_noise_shared_envelope':detail(candidate.frames(n1),candidate.frames(n2)),
    }
    out=Path(__file__).with_name('RESULTS.json');out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'count':len(files),'errors':[r for r in result['inventory'] if 'error'in r],'matches':[r for r in result['inventory'] if r.get('score',0)>=.8],'controls':c},indent=2))
if __name__=='__main__':main()
