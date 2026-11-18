"""Replace estimated shot times with draft anchors from recorded Scribe words.

Fuzzy matches are review candidates, never proof that spoken facts are correct.
"""
import argparse
import difflib
import json
import re
from pathlib import Path


def tokens(text):
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower().replace('’', "'"))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--shots', type=Path, required=True)
    p.add_argument('--scribe', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    raw = json.loads(a.scribe.read_text())
    words = []
    for word in raw['words']:
        if word.get('type') == 'word':
            for text in tokens(word['text']):
                words.append(dict(text=text, start=word['start'], end=word['end']))
    rows, cursor = [], 0
    for line in a.shots.read_text().splitlines():
        cells = [cell.strip() for cell in line.split('|')]
        if len(cells) < 8 or not re.fullmatch(r'\*\*`S\d+[ab]?`\*\*', cells[1]):
            continue
        opening = cells[3].strip('*').strip('"')
        target = tokens(opening)[:8]
        best = (-1, None, None)
        for i in range(cursor, min(len(words), cursor + 160)):
            for length in range(max(3, len(target)-2), len(target)+5):
                found = [w['text'] for w in words[i:i+length]]
                score = difflib.SequenceMatcher(None, target, found).ratio()
                if score > best[0]:
                    best = score, i, length
        score, i, length = best
        if i is None or score < .65:
            raise RuntimeError(f'No reliable monotonic anchor for {cells[1]}: {best}')
        rows.append(dict(shot=cells[1].replace('*','').replace('`',''),
                         start_s=words[i]['start'], estimated_time=cells[2],
                         opening=opening, match_score=round(score,3),
                         matched_text=' '.join(w['text'] for w in words[i:i+length]),
                         visual=cells[4], collection=cells[5], archive_id=cells[6],
                         licence_as_briefed=cells[7], review='DRAFT_ANCHOR_REVIEW_REQUIRED'))
        cursor = i + length
    duration = raw.get('audio_duration_secs') or words[-1]['end']
    for i, row in enumerate(rows):
        row['end_s'] = rows[i+1]['start_s'] if i+1 < len(rows) else duration
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(dict(duration_s=duration, shots=rows,
        note='Estimated shot-list times superseded for assembly by these draft audio anchors. Check each anchor; no watch/listen claimed.'),indent=2)+'\n')
    print(f'{len(rows)} monotonic anchors, minimum score {min(r["match_score"] for r in rows):.3f}; last end {duration}s')


if __name__ == '__main__':
    main()
