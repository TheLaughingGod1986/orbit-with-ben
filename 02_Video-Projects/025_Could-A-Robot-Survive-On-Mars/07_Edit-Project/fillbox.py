"""Find where a NASA plate is actually filled, so a crop never shows mosaic edges, white margins or black gaps.
A pixel is unfilled when it is near-black (<12) or near-white (>245) and connected to the border (flood fill),
so dark shadows and bright sky inside the picture still count as filled."""
from PIL import Image
import numpy as np
Image.MAX_IMAGE_PIXELS = None
LO, HI = 12, 245
W = 600  # analysis width


def _dilate(a):
    b = a.copy()
    b[1:] |= a[:-1]; b[:-1] |= a[1:]; b[:, 1:] |= a[:, :-1]; b[:, :-1] |= a[:, 1:]
    return b


def border_connected(edge):
    cur = np.zeros_like(edge)
    cur[0] = edge[0]; cur[-1] = edge[-1]; cur[:, 0] = edge[:, 0]; cur[:, -1] = edge[:, -1]
    while True:
        nxt = _dilate(cur) & edge
        if (nxt == cur).all():
            return cur
        cur = nxt


def mask(im):
    sm = im.convert('L')
    sc = W / sm.width
    sm = sm.resize((W, max(1, round(sm.height * sc))), Image.Resampling.BILINEAR)
    a = np.asarray(sm)
    edge = (a < LO) | (a > HI)
    unfilled = _dilate(_dilate(border_connected(edge)))
    return ~unfilled, sc


def best_box(im, aspect=16 / 9, min_h_px=1080 / 2.35):
    """Largest fully filled box of the given aspect, as fractions (x0,y0,x1,y1) of the image; None if under min_h_px."""
    m, sc = mask(im)
    H, Wd = m.shape
    ii = np.pad(m.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    for h in range(H, 0, -2):
        w = round(h * aspect)
        if w > Wd:
            continue
        if h / sc < min_h_px:
            return None
        s = ii[h:, w:] - ii[:-h, w:] - ii[h:, :-w] + ii[:-h, :-w]
        ys, xs = np.nonzero(s == h * w)
        if len(ys):
            cy, cx = (H - h) / 2, (Wd - w) / 2
            k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
            y, x = ys[k], xs[k]
            return (x / Wd, y / H, (x + w) / Wd, (y + h) / H)
    return None


def pan_band(im, min_h_px=1080 / 2.35):
    """For a wide panorama: the tallest horizontal band (y0,y1) and the widest x-run (x0,x1) inside it that is fully filled,
    with the run at least 16:9 wide. Fractions of the image."""
    m, sc = mask(im)
    H, Wd = m.shape
    best = None
    for h in range(H, 0, -2):
        if h / sc < min_h_px:
            break
        need = round(h * 16 / 9)
        for y in range(0, H - h + 1, 2):
            cols = m[y:y + h].all(0)
            run = 0; bx = None
            for x, ok in enumerate(cols):
                run = run + 1 if ok else 0
                if run >= need and (bx is None or run > bx[1] - bx[0]):
                    bx = (x - run + 1, x + 1)
            if bx and (best is None or (bx[1] - bx[0]) * h > best[0]):
                best = ((bx[1] - bx[0]) * h, y, y + h, bx)
        if best and best[2] - best[1] == h:
            break
    if not best:
        return None
    _, y0, y1, (x0, x1) = best
    return (x0 / Wd, y0 / H, x1 / Wd, y1 / H)


def border_fill_fraction(path_or_im):
    """Share of the frame that is near-black/near-white AND connected to the border (the fill gate metric)."""
    im = Image.open(path_or_im) if not isinstance(path_or_im, Image.Image) else path_or_im
    a = np.asarray(im.convert('L'))
    edge = (a < LO) | (a > HI)
    return float(border_connected(edge).mean())
