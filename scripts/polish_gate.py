#!/usr/bin/env python3
"""Polish gate for a long's rough cut (Claude, thread #6066030404): fails row frames that look unfinished, and still pushes that wobble.

  python3 scripts/polish_gate.py <video.mp4> --cuts <cuts.json> --out <polish_gate.json> [--no-jitter]

cuts.json is the assembler's list of {row, timeline_in, timeline_out, source, framing}. Each row is judged on its middle frame:
  (a) low detail: FAIL below the absolute floor on both luma std and edge density (calibrated on the frames Claude rejected
      as empty in 025 v02d, #6066196876); luma std < 18 or edge density below the film's 5th percentile is a WARN ("look at these");
  (b) split panel: a straight seam or gutter running the full height or width of the frame;
  (c) near-black or noise: mean luma < 28 (or 95th percentile < 50), or fine-grain noise with little structure under it;
  (d) push jitter (stills only): consecutive frames of the push are phase-correlated on a centre patch; FAIL if the shift
      reverses against the trend or jumps more than 0.35 px off it. That is the 'wobbly' look Ben saw on 023.
Exit 1 if any row fails; warnings never fail."""
import argparse, json, subprocess as sp, sys
from pathlib import Path
import numpy as np

STD_MIN = 18.0
EDGE_PCT = 5
# Floor = lower of 025 v02d's PIA22223 (flat green, 201.0 s / 216.3 s) and PIA22929 (noise, 297.4 s) on each measure, x 1.2.
FLOOR_CAL = dict(video='025_MarsRobot_full_rough_v02d.mp4', factor=1.2,
                 frames=[dict(source='PIA22223.jpg', t=201.0, std=12.1, edge=0.0223),
                         dict(source='PIA22223.jpg', t=216.3, std=11.2, edge=0.0216),
                         dict(source='PIA22929.jpg', t=297.4, std=26.54, edge=0.5735)])
STD_FLOOR = round(min(f['std'] for f in FLOOR_CAL['frames']) * FLOOR_CAL['factor'], 2)    # 13.44
EDGE_FLOOR = round(min(f['edge'] for f in FLOOR_CAL['frames']) * FLOOR_CAL['factor'], 4)  # 0.0259
DARK_MEAN, DARK_P95 = 28.0, 50.0
JIT_PX = 0.35
W, H = 960, 540  # analysis size for still checks
PATCH = 512      # full-res centre patch for jitter


def frame_gray(video, t, w=W, h=H):
    raw = sp.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', str(video), '-frames:v', '1',
                  '-vf', f'scale={w}:{h},format=gray', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w).astype(np.float32)


def box_blur(a, k=5):
    p = k // 2
    c = np.pad(a, p, mode='edge').cumsum(0).cumsum(1)
    c = np.pad(c, ((1, 0), (1, 0)))
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


def edge_density(a):
    gx = np.abs(np.diff(a, axis=1))[:-1]
    gy = np.abs(np.diff(a, axis=0))[:, :-1]
    return float(((gx + gy) > 24).mean())


def seams(a):
    """Full-height (axis 0) / full-width (axis 1) straight seams or gutters, ignoring the outer 4%."""
    hits = []
    for axis, name in ((1, 'vertical'), (0, 'horizontal')):
        b = a if axis == 1 else a.T
        n = b.shape[1]
        lo, hi = int(n * 0.04), int(n * 0.96)
        d = np.abs(np.diff(b, axis=1))               # rows x (n-1)
        med = np.median(d, axis=0)                     # a seam is a step present in nearly every row
        base = np.median(med[lo:hi]) + 1e-3
        for x in range(lo, hi - 1):
            if med[x] > 10 and med[x] > 5 * base and (d[:, x] > 6).mean() > 0.9:
                hits.append(dict(kind=f'{name} seam', at=round(x / n, 3), step=round(float(med[x]), 1)))
        colstd = b.std(axis=0)
        colmean = b.mean(axis=0)
        for x in range(lo + 3, hi - 3):
            if colstd[x] < 2.5 and np.all(colstd[x - 3:x + 4] < 4) and abs(colmean[x] - np.median(colmean)) > 20:
                hits.append(dict(kind=f'{name} gutter', at=round(x / n, 3)))
                break
    # one hit per position band is enough
    out, seen = [], set()
    for h in hits:
        key = (h['kind'].split()[0], round(h['at'], 2))
        if key not in seen:
            seen.add(key); out.append(h)
    return out


def noise(a):
    hf = a - box_blur(a, 5)
    lf = box_blur(a, 15)
    return float(hf.std()), float(lf.std())


def phase_shift(a, b, win):
    fa, fb = np.fft.fft2(a * win), np.fft.fft2(b * win)
    r = fa * np.conj(fb)
    r /= np.abs(r) + 1e-9
    c = np.fft.ifft2(r).real
    y, x = np.unravel_index(np.argmax(c), c.shape)
    def sub(cm, c0, cp):
        den = cm - 2 * c0 + cp
        return 0.0 if abs(den) < 1e-12 else 0.5 * (cm - cp) / den
    n0, n1 = c.shape
    dy = y + sub(c[(y - 1) % n0, x], c[y, x], c[(y + 1) % n0, x])
    dx = x + sub(c[y, (x - 1) % n1], c[y, x], c[y, (x + 1) % n1])
    if dy > n0 / 2: dy -= n0
    if dx > n1 / 2: dx -= n1
    return dx, dy


def jitter(video, t0, t1, size):
    vw, vh = size
    x0, y0 = (vw - PATCH) // 2, (vh - PATCH) // 2
    raw = sp.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-i', str(video), '-t', f'{t1 - t0:.3f}',
                  '-vf', f'crop={PATCH}:{PATCH}:{x0}:{y0},format=gray', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, PATCH, PATCH).astype(np.float32)
    if len(fr) > 1 and np.array_equal(fr[0], fr[1]):  # ffmpeg's input seek can repeat the first frame; not in the film
        fr = fr[1:]
    if len(fr) < 6:
        return None
    win = np.outer(np.hanning(PATCH), np.hanning(PATCH)).astype(np.float32)
    steps = np.array([phase_shift(fr[i + 1], fr[i], win) for i in range(len(fr) - 1)])
    out = {}
    worst = 0.0; reversals = 0
    for k, ax in enumerate('xy'):
        s = steps[:, k]
        trend = float(np.median(s))
        dev = np.abs(s - trend)
        worst = max(worst, float(dev.max()))
        if abs(trend) > 0.2:
            reversals += int(((np.sign(s) != np.sign(trend)) & (np.abs(s) > 0.1)).sum())
        out[f'trend_{ax}'] = round(trend, 3)
    out.update(max_off_trend_px=round(worst, 3), reversals=reversals, frames=len(fr))
    out['fail'] = bool(worst > JIT_PX or reversals > 0)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video'); ap.add_argument('--cuts', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--no-jitter', action='store_true')
    a = ap.parse_args()
    video = Path(a.video); cuts = json.loads(Path(a.cuts).read_text())
    size = tuple(map(int, sp.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                                           '-of', 'csv=p=0', str(video)], text=True).strip().split(',')[:2]))
    rows = []
    for k, c in enumerate(cuts):
        mid = (c['timeline_in'] + c['timeline_out']) / 2
        g = frame_gray(video, mid)
        hf, lf = noise(g)
        rows.append(dict(cut=k, row=c['row'], source=c['source'], t=round(mid, 2), std=round(float(g.std()), 2),
                         mean=round(float(g.mean()), 2), p95=round(float(np.percentile(g, 95)), 1), edge=round(edge_density(g), 4),
                         hf=round(hf, 2), lf=round(lf, 2), seams=seams(g), video=bool(c.get('framing', {}).get('offset') is not None)))
    edge_floor = float(np.percentile([r['edge'] for r in rows], EDGE_PCT))
    for r, c in zip(rows, cuts):
        why, warn = [], []
        if r['std'] < STD_FLOOR and r['edge'] < EDGE_FLOOR:
            why.append(f"low detail: luma std {r['std']} < {STD_FLOOR} and edge density {r['edge']} < {EDGE_FLOOR} (absolute floor)")
        if r['std'] < STD_MIN: warn.append(f"low detail: luma std {r['std']} < {STD_MIN}")
        if r['edge'] < edge_floor: warn.append(f"low detail: edge density {r['edge']} < film p{EDGE_PCT} {edge_floor:.4f}")
        if r['seams']: why.append('split panel: ' + ', '.join(f"{s['kind']} at {s['at']}" for s in r['seams']))
        if r['mean'] < DARK_MEAN or r['p95'] < DARK_P95: why.append(f"near-black: mean {r['mean']}, p95 {r['p95']}")
        if r['hf'] > 6 and r['lf'] < 12: why.append(f"noise: grain {r['hf']} over structure {r['lf']}")
        if not a.no_jitter and not r['video'] and c['timeline_out'] - c['timeline_in'] > 1.2:
            j = jitter(video, c['timeline_in'] + 0.45, c['timeline_out'] - 0.45, size)
            r['jitter'] = j
            if j and j['fail']:
                why.append(f"push jitter: {j['max_off_trend_px']} px off trend, {j['reversals']} reversals")
        r['fail'] = why; r['warn'] = warn
        state = 'FAIL ' + '; '.join(why) if why else ('WARN ' + '; '.join(warn) if warn else 'ok')
        print(f"{r['row']:>4} {r['t']:7.1f}s {r['source'][:28]:28} {state}", flush=True)
    failed = [r for r in rows if r['fail']]
    warned = [r for r in rows if r['warn'] and not r['fail']]
    res = dict(rule=dict(low_detail=f'FAIL: luma std < {STD_FLOOR} and edge density < {EDGE_FLOOR} (absolute floor); '
                                    f'WARN: luma std < {STD_MIN} or edge density < film p{EDGE_PCT}',
                         split_panel='full-height/width seam or gutter',
                         near_black=f'mean < {DARK_MEAN} or p95 < {DARK_P95}', noise='grain std > 6 over structure std < 12',
                         jitter=f'centre-patch phase correlation: reversal against trend or > {JIT_PX} px off trend'),
               low_detail_floor=dict(std=STD_FLOOR, edge=EDGE_FLOOR, calibration=FLOOR_CAL),
               video=str(video), edge_floor=round(edge_floor, 4), verdict='FAIL' if failed else 'PASS',
               failed=[dict(row=r['row'], cut=r['cut'], t=r['t'], source=r['source'], why=r['fail']) for r in failed],
               warn=[dict(row=r['row'], cut=r['cut'], t=r['t'], source=r['source'], why=r['warn']) for r in warned], rows=rows)
    Path(a.out).write_text(json.dumps(res, indent=2))
    print(f"polish gate {res['verdict']}: {len(failed)} of {len(rows)} rows failed, {len(warned)} to look at -> {a.out}")
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
