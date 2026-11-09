#!/usr/bin/env python3
"""031 historical WHEN call-outs; £0, alpha over graded moving plates.

Entrance rules match date_graphics. These are date stamps, not the remaining
progressive timeline. Place clear of WHO cards and subject; no approval implied.
"""
from date_graphics import frame
from evidence_graphics import main as render

SPECS = [
    dict(row=5, mode='brunhes1905', start_s=36.14, duration_s=3.6,
         source_rows=[3], alpha=True, labels=['1905', 'PONTFAREIN, FRANCE']),
    dict(row=10, mode='matuyama1929', start_s=89.94, duration_s=3.6,
         source_rows=[4], alpha=True, labels=['1929']),
    dict(row=20, mode='gauss1830s', start_s=209.10, duration_s=3.6,
         source_rows=[8], alpha=True, labels=['1830s']),
]


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
