#!/usr/bin/env python3
"""Sub-pixel still pushes and pans for long assemblers (Claude, thread #6066196876: the standard from 025 v03 / 023 v05 on).

Never use ffmpeg zoompan on a still: it steps whole pixels, about 1 px off trend per frame, which is the 'wobbly' look Ben saw
on 023. Each frame here is a float crop box resampled from the plate, so the move is smooth. scripts/polish_gate.py checks it.

  from still_motion import push, pan
  push(plate_img, seconds, dest, pct=0.05)           # centre push-in by pct over the shot
  pan(panorama_img_1080_high, seconds, dest, (0.1, 0.6))  # slide the 1920 window across that fraction of the width

Plates for push() should be oversized (025 uses 2112x1188) so the push never upsamples past the source."""
import subprocess as sp
from PIL import Image

W, H, FPS = 1920, 1080, 30
ENC = ['-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '19', '-threads', '4']


def render(im, box, frames, dest, enc=ENC, fps=FPS):
    """Write `frames` frames to dest; box(n) returns the float (left, top, right, bottom) crop of im for frame n."""
    p = sp.Popen(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                  '-r', str(fps), '-i', '-', '-vf', 'setsar=1,format=yuv420p', '-frames:v', str(frames), *map(str, enc), str(dest)],
                 stdin=sp.PIPE)
    im = im.convert('RGB')
    for n in range(frames):
        p.stdin.write(im.resize((W, H), Image.Resampling.BICUBIC, box=box(n)).tobytes())
    p.stdin.close()
    if p.wait():
        raise RuntimeError(f'still_motion render failed: {dest}')


def push(im, seconds, dest, pct=0.05, **kw):
    frames = round(seconds * kw.get('fps', FPS))
    pw, ph = im.size

    def box(n):
        z = 1 + pct * n / frames
        w, h = pw / z, ph / z
        return ((pw - w) / 2, (ph - h) / 2, (pw + w) / 2, (ph + h) / 2)
    render(im, box, frames, dest, **kw)


def pan(im, seconds, dest, span, **kw):
    frames = round(seconds * kw.get('fps', FPS))
    if im.height != H:
        im = im.resize((round(im.width * H / im.height), H), Image.Resampling.LANCZOS)
    x0, x1 = (f * (im.width - W) for f in span)
    render(im, lambda n: (x0 + (x1 - x0) * n / frames, 0.0, x0 + (x1 - x0) * n / frames + W, float(H)), frames, dest, **kw)
