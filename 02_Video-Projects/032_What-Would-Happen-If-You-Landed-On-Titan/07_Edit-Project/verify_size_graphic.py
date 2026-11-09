#!/usr/bin/env python3
"""Measure R09's geometry/alpha/source integrity; no picture verdict."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
import size_graphic as graphic


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    record = json.loads(args.manifest.read_text())
    for asset in record['assets']:
        assert graphic.sha(asset['path']) == asset['sha256']
    assert graphic.sha(record['preview']) == record['preview_sha256']
    frames = []
    for i in range(109):
        t = i/30
        frame = graphic.frame(t)
        bbox = frame.getchannel('A').getbbox()
        if i in (0,108):
            assert bbox is None
        else:
            assert bbox and bbox[0] >= 95 and bbox[1] >= 54
            assert bbox[2] <= 1825 and bbox[3] <= 1026
        diameters = graphic.diameters(t)
        for diameter, asset in zip(diameters, graphic.SPECS):
            assert abs(diameter - diameters[-1]*asset['km']/5150) < 1
        frames.append(dict(frame=i, bbox=bbox, diameters=diameters))
    assert graphic.frame(.7).tobytes() != graphic.frame(1.5).tobytes()
    # Missing-review/rights attempts stop before creating files or starting ffmpeg.
    cmd = [sys.executable, str(Path(graphic.__file__)), '--out', '/private/tmp/J2089-guard-unused', '--render']
    probe = subprocess.run(cmd, capture_output=True, text=True)
    assert probe.returncode == 2 and 'Render needs named approval' in probe.stderr
    output = dict(job='J2089', status='MEASUREMENTS_ONLY', source_hashes='MATCH',
                  preview_hash='MATCH', ratio_rounding_error_px='<1',
                  render_without_approval_exit=probe.returncode, frames=frames,
                  verified_frame_count=len(frames), motion_perception=False,
                  not_verified=['Mercury rights clearance','row still approval',
                                'final composite and current film gates'])
    args.out.write_text(json.dumps(output, indent=2)+'\n')
    print('109 frames: safe bounds, common linear ratios, clear entry/exit; source and preview hashes match; unapproved render rejected.')


if __name__ == '__main__':
    main()
