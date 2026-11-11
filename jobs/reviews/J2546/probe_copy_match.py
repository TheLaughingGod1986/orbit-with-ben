import base64, json, sys, unittest, zlib
from pathlib import Path

REPO = Path("/Users/ben/_desk/worker/orbit-with-ben")
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
import gate_shorts_open as g  # noqa: E402

D = json.loads((REPO / "jobs/reviews/J2545/J2545_labelled_frames.json").read_text())
W, H = g.FB_W, g.FB_H
B = 6
NX = W // B


def blocks(px):
    """6x6 block means: list of rows (H//B) of NX values."""
    out = []
    for by in range(H // B):
        row = []
        for bx in range(NX):
            s = 0
            for y in range(by * B, by * B + B):
                o = y * W + bx * B
                s += sum(px[o:o + B])
            row.append(s / (B * B))
        out.append(row)
    return out


def pearson(a, b):
    n = len(a)
    if n < 12:
        return 0.0, 0.0
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((x - mb) ** 2 for x in b)
    if va < n * 4 or vb < n * 4:      # under 2 grey levels of spread: proves nothing
        return 0.0, (va / n) ** 0.5
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (va * vb) ** 0.5, (va / n) ** 0.5


def side_match(px, bl, u, low, s, top):
    """Correlation of one outer band's blocks with the picture band enlarged s times about the frame centre."""
    act, pred = [], []
    rows = range(0, (u - 2) // B) if top else range((low + 2 + B - 1) // B, H // B)
    for by in rows:
        cy = by * B + B / 2
        sy = (u + low) / 2 + (cy - H / 2) / s
        if not (u + 1 <= sy < low - 1):
            continue
        for bx in range(NX):
            cx = bx * B + B / 2
            sx = W / 2 + (cx - W / 2) / s
            x0, y0 = int(sx), int(sy)
            x1 = min(W - 1, x0 + 1)
            p = (px[y0 * W + x0] + px[y0 * W + x1] + px[(y0 - 1) * W + x0] + px[(y0 + 1) * W + x0]) / 4
            act.append(bl[by][bx])
            pred.append(p)
    # drop the fifth of blocks that differ most (a caption laid over the fill)
    if len(act) >= 20:
        ma, mp = sum(act) / len(act), sum(pred) / len(pred)
        idx = sorted(range(len(act)), key=lambda i: abs((act[i] - ma) - (pred[i] - mp)))
        keep = idx[:int(len(idx) * 0.8)]
        act, pred = [act[i] for i in keep], [pred[i] for i in keep]
    return pearson(act, pred)


def best_match(px):
    bl = blocks(px)
    best = (-1, None)
    for u in range(30, 82, 2):
        for low in (H - u - 2, H - u, H - u + 2):
            cover = H / (low - u)
            for s in (cover, cover * 1.25):
                rt, st = side_match(px, bl, u, low, s, True)
                rb, sb = side_match(px, bl, u, low, s, False)
                score = min(rt, rb)
                if score > best[0]:
                    best = (score, (u, low, round(s, 2), round(rt, 2), round(rb, 2), round(st, 1), round(sb, 1)))
    one = (-1, None)
    for u in range(30, 82, 2):
        low = H - u
        cover = H / (low - u)
        for s in (cover, cover * 1.25):
            for top in (True, False):
                r, sd = side_match(px, bl, u, low, s, top)
                if r > one[0]:
                    one = (r, (u, low, round(s, 2), "top" if top else "bot", round(sd, 1)))
    return best, one


class Probe(unittest.TestCase):
    def test_probe(self):
        for i, f in enumerate(D["frames"]):
            px = zlib.decompress(base64.b64decode(f["gray_108x192_zlib_b64"]))
            m = g.full_bleed_frame(px)
            best, one = best_match(px)
            print(f"{i:2d} {f['id']} t={f['t']} {f['label']:6s} old={m['kind']} both={best[0]:.2f} {best[1]} one={one[0]:.2f} {one[1]}")
