#!/usr/bin/env python3
"""R20/R29 sourced date call-outs; alpha components, not a full timeline. £0."""
from date_graphics import frame
from evidence_graphics import main as render

SPECS = [
    dict(row=20, mode='gauss1830s', start_s=209.10, duration_s=3.6,
         source_rows=[8], alpha=True, labels=['1830s']),
    dict(row=29, mode='saa1970', start_s=301.44, duration_s=3.6,
         source_rows=[12], alpha=True, labels=['1970']),
]


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
