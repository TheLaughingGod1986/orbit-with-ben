#!/usr/bin/env python3
"""Three missing WHEN components; £0, alpha, not a complete timeline.

Reuse the established date-card animation without altering previous renders.
Each label is sourced in SOURCES.md and begins at its locked Scribe cue.
"""
from date_graphics import frame
from evidence_graphics import main as render

SPECS = [
    dict(row=5, mode='brunhes1905', start_s=36.14, duration_s=3.6,
         source_rows=[3], alpha=True, labels=['1905', 'CENTRAL FRANCE'],
         source_url='https://eos.org/articles/centenary-discovery-earths-magnetic-field-reversals'),
    dict(row=10, mode='matuyama1929', start_s=89.94, duration_s=3.24,
         source_rows=[4], alpha=True, labels=['1929'],
         source_url='https://doi.org/10.2183/pjab1912.5.203'),
    dict(row=11, mode='last_switch', start_s=109.06, duration_s=3.6,
         source_rows=[4], alpha=True, labels=['780,000 YEARS AGO'],
         source_url='https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/'),
]


def render_frame(spec, t):
    # Existing date renderer uses a 3.6s envelope; rescale its local time so
    # the shorter R10 card also fades out completely inside its own span.
    return frame(spec, t * 3.6 / spec['duration_s'])


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=render_frame)


if __name__ == '__main__':
    main()
