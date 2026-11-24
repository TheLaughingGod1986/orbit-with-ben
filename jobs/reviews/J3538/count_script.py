"""Reproduce v03 spoken counts and estimated chapter timings, without narration."""
from pathlib import Path
import hashlib, json, re
ROOT = Path(__file__).resolve().parents[3]
p = ROOT / '02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/01_Script/every_planet_explained_script_master_v03.md'
text = p.read_text()
chapters = [('Mercury', [])]
for line in text.splitlines():
    line = line.strip()
    if line.startswith('[CHAPTER CARD:'):
        chapters.append((line.split(': ', 1)[1].split(' — ')[0], []))
    elif line and not line.startswith(('#', '[', '<!--')):
        chapters[-1][1].append(line)
def counts(s):
    return {'spoken_words': sum(bool(re.search('[A-Za-z0-9]', w)) for w in s.split()), 'whitespace_tokens': len(s.split()), 'characters': len(s)}
spoken = ' '.join(' '.join(lines) for _, lines in chapters)
result = {'script_sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size, **counts(spoken), 'timing_basis': '145 alphanumeric tokens/minute; 6.5 seconds transition/breath per chapter; 18 seconds final picture/music hold. Estimates only, no audio rendered.', 'chapters': []}
t = 0
for name, lines in chapters:
    c = counts(' '.join(lines)); duration = c['spoken_words'] * 60 / 145 + 6.5
    result['chapters'].append({'name': name, **c, 'start_s': round(t, 2), 'speech_s': round(c['spoken_words']*60/145, 2), 'end_s': round(t+duration, 2)})
    t += duration
result['estimated_total_s'] = round(t+18, 2)
print(json.dumps(result, indent=2))
