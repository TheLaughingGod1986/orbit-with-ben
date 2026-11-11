"""J2546 probe 2: per labelled frame, the row-detail profile and the straightest brightness steps.

    python3 -m unittest discover -s jobs/reviews/J2546 -p "probe_features.py"

Columns: index, id, t, label, kind the check on main gives, then
  det   median row detail in 16 bins of 12 rows, top to bottom (0-9, then + for 10 or more)
  std   median row pixel spread in the same bins, divided by 4 (0-9, +)
  up/lo the row in the upper / lower half where most columns step by 6 grey levels or more between rows y-2 and
        y+1, with that share of columns
"""
import base64, json, sys, unittest, zlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
import gate_shorts_open as g  # noqa: E402

D = json.loads((REPO / "jobs/reviews/J2545/J2545_labelled_frames.json").read_text())
W, H = g.FB_W, g.FB_H


def med(v):
    v = sorted(v)
    return v[len(v) // 2]


def digit(x):
    return str(int(x)) if x < 10 else "+"


def step_share(px, y, need=6):
    a, b = (y - 2) * W, (y + 1) * W
    return sum(1 for x in range(W) if abs(px[a + x] - px[b + x]) >= need) / W


class Probe(unittest.TestCase):
    def test_probe(self):
        for i, f in enumerate(D["frames"]):
            px = zlib.decompress(base64.b64decode(f["gray_108x192_zlib_b64"]))
            m = g.full_bleed_frame(px)
            det, _ = g._fb_row_stats(px)
            rstd = [g._fb_std(px, y, y + 1) for y in range(H)]
            dp = "".join(digit(med(det[b * 12:(b + 1) * 12])) for b in range(16))
            sp = "".join(digit(med(rstd[b * 12:(b + 1) * 12]) / 4) for b in range(16))
            up = max(range(20, 92), key=lambda y: step_share(px, y))
            lo = max(range(100, 172), key=lambda y: step_share(px, y))
            print(f"{i:2d} {f['id']} {f['t']:5.1f} {f['label']:6s} {str(f['kind'])[:14]:14s} old={str(m['kind']):8s} "
                  f"det={dp} std={sp} up={up}:{step_share(px, up):.2f} lo={lo}:{step_share(px, lo):.2f}")
