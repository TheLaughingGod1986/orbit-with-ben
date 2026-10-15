#!/usr/bin/env python3
"""J0250: deterministic, no-spend panel B using the existing house composer.
Source and output JPEGs stay outside git. Run with --source and --out.
"""
import argparse
import json
from PIL import ImageDraw, ImageOps
import _build_light_speed_covers_j0143_v02 as base
import _build_light_speed_thumbs_v01 as house


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=base.Path, required=True)
    parser.add_argument('--out', type=base.Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    im, ship = base.plate(args.source)
    im = ImageOps.mirror(im)
    ship = [base.W - 1 - ship[2], ship[1], base.W - 1 - ship[0], ship[3]]
    draw = ImageDraw.Draw(im)
    font = house.font(115)
    cap = draw.textbbox((0, 0), 'H', font=font)
    cap_height = cap[3] - cap[1]
    assert cap_height >= 82
    text = '7 YEARS GONE'
    width = house.line_w(draw, text, font)
    assert width < base.W - 70
    x = (base.W - width) / 2
    top = 65
    y = top - cap[1]
    house.draw_line(draw, x + 3, y + 4, text, font, house.BLACK)
    house.draw_line(draw, x, y, text, font, house.WHITE)
    house.draw_line(draw, x, y, '7 YEARS', font, house.YELLOW)
    box = [round(x)-7, top-7, round(x+width)+7, top+cap_height+11]
    assert box[3] < ship[1]
    output = args.out / '024_panel_b_7_years_gone.jpg'
    im.save(output, quality=95, subsampling=0)
    meta = {'job': 'J0250', 'approval': 'pending Chief review',
            'source': args.source.name, 'source_sha256': base.sha(args.source),
            'output': output.name, 'sha256': base.sha(output),
            'transform': 'existing j0143_v02 crop and cyan grade, then horizontal mirror',
            'copy': text, 'yellow': '7 YEARS', 'white': 'GONE',
            'font': 'Arial Black', 'cap_height': cap_height,
            'text_box': box, 'ship_box': ship, 'spend': 0,
            'orientation_note': 'Mirroring puts the exhaust on the left; the nose consequently points right. The brief describes this as right-to-left, but its explicit mirror/exhaust-left instruction is followed.'}
    (args.out / 'J0250_META.json').write_text(json.dumps(meta, indent=2) + '\n')
    print(output)


if __name__ == '__main__':
    main()
