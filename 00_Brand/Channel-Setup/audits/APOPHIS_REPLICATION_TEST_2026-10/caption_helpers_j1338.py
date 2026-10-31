# Caption functions preserved verbatim from J1321 (994571421).
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920
FONT='/System/Library/Fonts/Supplemental/Arial Black.ttf'
WHITE=(245,248,255,255)
YELLOW=(255,213,64,255)
def fit_font(draw, text, size, max_w, stroke):
    size = int(size)
    while size > 28:
        font = ImageFont.truetype(FONT, size)
        box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if box[2] - box[0] <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT, 28)

def centred(draw, y, text, font, fill, stroke):
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (box[2] - box[0])) / 2 - box[0]
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(8, 16, 28, 255))
    return box[3] - box[1]

def hook_image(lines, yellow) -> Image.Image:
    """Hook stays above the c37 keep band (rows 105–375 of 480, about 22–78%)."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ceiling = int(H * 0.19)
    max_w = int(W * 0.88)
    size = 150
    while size > 48:
        font = ImageFont.truetype(FONT, size)
        heights = []
        fits = True
        for row in lines:
            widths = [d.textbbox((0, 0), w, font=font, stroke_width=8) for w in row]
            space = d.textlength(' ', font=font)
            total = sum((b[2] - b[0] for b in widths)) + space * (len(row) - 1)
            if total > max_w:
                fits = False
            heights.append(max((b[3] - b[1] for b in widths)))
        block = sum(heights) + 18 * (len(lines) - 1)
        if fits and 40 + block <= ceiling:
            break
        size -= 2
    font = ImageFont.truetype(FONT, size)
    y = 40
    for row in lines:
        widths = [d.textbbox((0, 0), w, font=font, stroke_width=8) for w in row]
        space = d.textlength(' ', font=font)
        total = sum((b[2] - b[0] for b in widths)) + space * (len(row) - 1)
        x = (W - total) / 2
        for w, b in zip(row, widths):
            d.text((x - b[0], y), w, font=font, fill=YELLOW if w == yellow else WHITE, stroke_width=8, stroke_fill=(8, 16, 28, 255))
            x += b[2] - b[0] + space
        y += max((b[3] - b[1] for b in widths)) + 18
    return im

def caption_track(words, end):
    groups, cur = ([], [])
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w['word'][-1:] in '.,?!':
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    out = []
    for i, g in enumerate(groups):
        start = g[0]['start']
        stop = groups[i + 1][0]['start'] if i + 1 < len(groups) else min(end, g[-1]['end'] + 0.45)
        text = ' '.join((w['word'] for w in g)).upper().replace(' ,', ',')
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        centred(d, int(H * 0.86), text, fit_font(d, text, 58, int(W * 0.72), 6), WHITE, 6)
        out.append((start, stop, im))
    return out

def load_words(path: Path):
    raw = json.loads(path.read_text())
    words = []
    for w in raw:
        text = (w.get('text') or w.get('word') or '').strip()
        if not text or w.get('type') not in (None, 'word'):
            continue
        words.append({'word': text, 'start': float(w['start']), 'end': float(w['end'])})
    return words

