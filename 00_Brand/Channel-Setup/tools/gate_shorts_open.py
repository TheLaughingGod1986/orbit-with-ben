#!/usr/bin/env python3
"""Shorts open gate — run on every Short export BEFORE upload (10 Sep 2026 audit fix).

Hard FAILs (mirror `orbit-auditor-ship-gate.mdc` · `orbit-shorts-punch-first.mdc`):

  1. duration ≥ 40 s                                  (existing lock)
  2. first frame (0.3 s) within 10 dHash bits of any   (new — Europa week shipped six
     Short published / scheduled ±14 days of air date   Shorts on one plate; feed saw
                                                        the same video six days running)
  3. Orbit in frame at 0 s                             (new — `TE_HDKAnqms` / `mAAMsbhm88w`
                                                        Orbit-first opens got 0 % feed traffic)
  4. no audio stream, or mean volume below −40 dB      (24 Sep 2026 — four Moon Shorts aired
                                                        with the whole file at about −90 dB)

Warning (not a FAIL until calibrated on real exports):

  5. picture barely changes in the first second        (24 Sep 2026 — still globe + caption
                                                        opens held 15–17 % stayed; the moving
                                                        plume open held 46 %)

Orbit detection is a colour/shape heuristic (matte-orange body + black visor holding
cream eyes). It is calibrated on the 10 Sep frames (Orbit ≥ 0.004 · world ≤ 0.0003) and
it always writes a contact sheet; a human still eyeballs the 0 s frame before upload.

Usage
  python3 gate_shorts_open.py check <short.mp4> --air-date 2026-09-16 [--json]
  python3 gate_shorts_open.py add --id <yt id> --date 2026-09-16 --title "…" (--file <mp4> | --frame <png/jpg>)
  python3 gate_shorts_open.py fetch --id <yt id> --date … --title …     # public Short via yt-dlp
  python3 gate_shorts_open.py list [--days 14] [--air-date …]
  python3 gate_shorts_open.py compare                                     # pairwise table of library

Library: 00_Brand/Channel-Setup/audits/shorts_open_library/library.json (+ frames/<id>.jpg)
Exit code 0 = PASS, 1 = FAIL, 2 = tool error.
"""
from __future__ import annotations

import argparse
import colorsys
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]  # tools → Channel-Setup → 00_Brand → orbit-with-ben
LIB_DIR = ROOT / "00_Brand/Channel-Setup/audits/shorts_open_library"
LIB_JSON = LIB_DIR / "library.json"
FRAMES = LIB_DIR / "frames"

OPEN_T = 0.3  # seconds — first real frame after any fade-in
LOOKBACK_DAYS = 14
DHASH_FAIL_BITS = 10
DHASH_WARN_BITS = 16
DUR_FAIL = 40.0
DUR_BAND = (22.0, 27.0)
VISOR_FAIL = 0.003
VISOR_WARN = 0.001
SHEET_TIMES = (0.0, 0.3, 1.0, 2.0, 3.0, 4.0)
# Voiced Orbit Shorts measure about −19 to −28 dB mean; the silent Moon uploads were about −90.
AUDIO_FAIL_DB = -40.0
OPEN_AUDIO_S = 1.5  # the hook line must be audible inside this window
OPEN_AUDIO_WARN_DB = -45.0
# Motion in the first second: mean absolute grey-level change (0–100 scale) summed over
# 0.25 s steps from 0.0 to 1.0 s. Set 24 Sep 2026 on synthetic 9:16 clips cut from the
# Europa long thumbnail: still 0.0 · still + changing caption 0.3 · Ken Burns 1.5 %/s 3.2 ·
# Ken Burns 4.5 %/s 8.3 · fast push-in 44 · handheld shake 39. A zoom on a still image
# warns; a real move clears it easily. Warn only until real exports are measured.
MOTION_TIMES = (0.0, 0.25, 0.5, 0.75, 1.0)
MOTION_WARN = 10.0


# ----------------------------------------------------------------------------- ffmpeg
def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


def duration_s(path: Path) -> float:
    out = run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
    ).stdout.decode().strip()
    return float(out)


def is_video(path: Path) -> bool:
    return path.suffix.lower() in {".mp4", ".mov", ".m4v", ".webm", ".mkv"}


def raw_frame(path: Path, w: int, h: int, t: float | None, pix: str) -> bytes:
    cmd = ["ffmpeg", "-v", "error"]
    if t is not None and is_video(path):
        cmd += ["-ss", f"{t:.3f}"]
    cmd += ["-i", str(path), "-frames:v", "1", "-vf", f"scale={w}:{h}:flags=area", "-f", "rawvideo", "-pix_fmt", pix, "-"]
    data = run(cmd).stdout
    need = w * h * (1 if pix == "gray" else 3)
    if len(data) < need:
        raise RuntimeError(f"short frame from {path} ({len(data)} < {need})")
    return data[:need]


def save_frame(path: Path, t: float | None, out: Path, w: int = 270) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if t is not None and is_video(path):
        cmd += ["-ss", f"{t:.3f}"]
    cmd += ["-i", str(path), "-frames:v", "1", "-vf", f"scale={w}:-2", "-q:v", "4", str(out)]
    run(cmd)


# ----------------------------------------------------------------------------- hashes
def dhash(path: Path, t: float | None = OPEN_T) -> int:
    g = raw_frame(path, 9, 8, t, "gray")
    bits = 0
    for y in range(8):
        for x in range(8):
            bits = (bits << 1) | (1 if g[y * 9 + x] > g[y * 9 + x + 1] else 0)
    return bits


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def orbit_score(path: Path, t: float | None = OPEN_T) -> dict:
    """Orange body + black visor holding cream eyes → 'visor' fraction."""
    W, H = 72, 128
    d = raw_frame(path, W, H, t, "rgb24")
    cls = bytearray(W * H)
    o = k = 0
    for i in range(W * H):
        r, g, b = d[3 * i], d[3 * i + 1], d[3 * i + 2]
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        h *= 360
        if 12 <= h <= 42 and s >= 0.5 and v >= 0.45:
            cls[i] = 1  # orange
            o += 1
        elif v < 0.18:
            cls[i] = 2  # dark (visor / space)
            k += 1
        elif v > 0.75 and s < 0.35:
            cls[i] = 3  # cream / white (eyes / stars)
    R = 4
    vis = 0
    for y in range(H):
        for x in range(W):
            if cls[y * W + x] != 2:
                continue
            has_o = has_w = False
            for dy in range(-R, R + 1):
                yy = y + dy
                if not 0 <= yy < H:
                    continue
                row = yy * W
                for dx in range(-R, R + 1):
                    xx = x + dx
                    if not 0 <= xx < W:
                        continue
                    c = cls[row + xx]
                    if c == 1:
                        has_o = True
                    elif c == 3:
                        has_w = True
                if has_o and has_w:
                    break
            if has_o and has_w:
                vis += 1
    n = W * H
    return {"orange_frac": round(o / n, 4), "dark_frac": round(k / n, 4), "visor_frac": round(vis / n, 4)}


def motion_first_second(path: Path) -> float:
    """How much the picture changes between 0 and 1 s (a still or slow drift reads near 0)."""
    W, H = 72, 128
    frames = [raw_frame(path, W, H, t, "gray") for t in MOTION_TIMES]
    total = 0.0
    for a, b in zip(frames, frames[1:]):
        total += sum(abs(x - y) for x, y in zip(a, b)) / (W * H) / 255 * 100
    return round(total, 2)


# ----------------------------------------------------------------------------- library
def load_lib() -> dict:
    if LIB_JSON.exists():
        return json.loads(LIB_JSON.read_text())
    return {"about": "first-frame dHash of every Orbit Short (live + scheduled) — gate_shorts_open.py", "entries": []}


def save_lib(lib: dict) -> None:
    LIB_DIR.mkdir(parents=True, exist_ok=True)
    lib["updated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    lib["entries"].sort(key=lambda e: (e["date"], e["id"]))
    LIB_JSON.write_text(json.dumps(lib, indent=2, ensure_ascii=False) + "\n")


def upsert(lib: dict, entry: dict) -> None:
    lib["entries"] = [e for e in lib["entries"] if e["id"] != entry["id"]]
    lib["entries"].append(entry)


def window(lib: dict, air: date, days: int) -> list[dict]:
    lo, hi = air - timedelta(days=days), air + timedelta(days=days)
    out = []
    for e in lib["entries"]:
        d = date.fromisoformat(e["date"])
        if lo <= d <= hi and e.get("status", "live") != "retired":
            out.append(e)
    return out


def add_entry(lib: dict, vid: str, d: str, title: str, src: Path, source: str, t: float | None, status: str = "live") -> dict:
    h = dhash(src, t)
    sc = orbit_score(src, t)
    frame = FRAMES / f"{vid}.jpg"
    save_frame(src, t, frame)
    entry = {
        "id": vid,
        "date": d,
        "title": title,
        "dhash": f"{h:016x}",
        "orbit": sc,
        "source": source,
        "frame": str(frame.relative_to(ROOT)),
        "status": status,
        "added_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    upsert(lib, entry)
    return entry


# ----------------------------------------------------------------------------- audio
def has_audio(path: Path) -> bool:
    out = run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(path)]
    ).stdout.decode().strip()
    return bool(out)


def mean_volume_db(path: Path, start: float = 0.0, length: float | None = None) -> float:
    cmd = ["ffmpeg", "-v", "info", "-nostats", "-ss", f"{start:.3f}"]
    if length is not None:
        cmd += ["-t", f"{length:.3f}"]
    cmd += ["-i", str(path), "-vn", "-af", "volumedetect", "-f", "null", "-"]
    err = run(cmd).stderr.decode(errors="replace")
    for line in err.splitlines():
        if "mean_volume:" in line:
            return float(line.split("mean_volume:")[1].split("dB")[0])
    return -91.0  # volumedetect prints nothing for pure digital silence on some builds


# ----------------------------------------------------------------------------- check
def contact_sheet(path: Path, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    dur = duration_s(path)
    with tempfile.TemporaryDirectory() as td:
        tiles = []
        for i, t in enumerate(SHEET_TIMES):
            if t >= dur - 0.05:
                continue
            p = Path(td) / f"t{i}.png"
            save_frame(path, t, p, w=216)
            tiles.append(p)
        if len(tiles) == 1:
            shutil.copy(tiles[0], out)
            return
        inputs = []
        for p in tiles:
            inputs += ["-i", str(p)]
        run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", f"hstack=inputs={len(tiles)}", str(out)])


def check(path: Path, air: date, days: int, lib: dict, sheet_dir: Path | None, self_id: str | None = None) -> dict:
    res: dict = {"file": str(path), "air_date": air.isoformat(), "fails": [], "warns": []}
    dur = duration_s(path)
    res["duration_s"] = round(dur, 2)
    if dur >= DUR_FAIL:
        res["fails"].append(f"duration {dur:.1f}s ≥ {DUR_FAIL:.0f}s")
    elif not (DUR_BAND[0] <= dur <= DUR_BAND[1] + 0.5):
        res["warns"].append(f"duration {dur:.1f}s outside {DUR_BAND[0]:.0f}–{DUR_BAND[1]:.0f}s band")

    if not has_audio(path):
        res["audio"] = {"stream": False}
        res["fails"].append("no audio stream — the narrator is missing")
    else:
        whole = mean_volume_db(path)
        opening = mean_volume_db(path, 0.0, OPEN_AUDIO_S)
        res["audio"] = {"stream": True, "mean_db": whole, "open_mean_db": opening}
        if whole < AUDIO_FAIL_DB:
            res["fails"].append(f"soundtrack mean {whole:.1f} dB < {AUDIO_FAIL_DB:.0f} dB — silent or near-silent file")
        elif opening < OPEN_AUDIO_WARN_DB:
            res["warns"].append(f"first {OPEN_AUDIO_S:.1f}s mean {opening:.1f} dB — hook line may start late")

    motion = motion_first_second(path)
    res["motion_0_1s"] = motion
    if motion < MOTION_WARN:
        res["warns"].append(
            f"picture barely changes in the first second (motion {motion:.1f} < {MOTION_WARN:.0f}) — "
            "trim the clip's ease-in so frame 0 is already mid-action"
        )

    h = dhash(path)
    res["dhash"] = f"{h:016x}"
    near = []
    for e in window(lib, air, days):
        if self_id and e["id"] == self_id:
            continue
        dist = hamming(h, int(e["dhash"], 16))
        if dist <= DHASH_WARN_BITS:
            near.append({"id": e["id"], "date": e["date"], "title": e["title"], "bits": dist, "source": e.get("source", "")})
    near.sort(key=lambda x: x["bits"])
    res["near_opens"] = near
    for n in near:
        approx = " [studio capture — approximate]" if n["source"] == "studio_player_capture" else ""
        if n["bits"] <= DHASH_FAIL_BITS:
            res["fails"].append(f"open plate {n['bits']} bits from {n['id']} ({n['date']} · {n['title']}){approx}")
        else:
            res["warns"].append(f"open plate {n['bits']} bits from {n['id']} ({n['date']}){approx}")

    sc = orbit_score(path)
    res["orbit"] = sc
    if sc["visor_frac"] >= VISOR_FAIL:
        res["fails"].append(f"Orbit in frame at 0 s (visor {sc['visor_frac']:.4f} ≥ {VISOR_FAIL}) — picture-first lock")
    elif sc["visor_frac"] >= VISOR_WARN:
        res["warns"].append(f"possible Orbit at 0 s (visor {sc['visor_frac']:.4f}) — eyeball the sheet")

    if sheet_dir is not None:
        sheet = sheet_dir / f"{path.stem}_open_sheet.jpg"
        contact_sheet(path, sheet)
        res["contact_sheet"] = str(sheet)
    res["verdict"] = "FAIL" if res["fails"] else "PASS"
    return res


# ----------------------------------------------------------------------------- cli
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="gate one or more Short exports")
    c.add_argument("files", nargs="+", type=Path)
    c.add_argument("--air-date", default=date.today().isoformat())
    c.add_argument("--days", type=int, default=LOOKBACK_DAYS)
    c.add_argument("--sheet-dir", type=Path, default=Path(tempfile.gettempdir()) / "orbit_shorts_gate")
    c.add_argument("--id", default=None, help="candidate's own YouTube id (skips its library entry on re-check)")
    c.add_argument("--json", action="store_true")

    a = sub.add_parser("add", help="register a published/scheduled Short from a local file or frame")
    a.add_argument("--id", required=True)
    a.add_argument("--date", required=True, help="air date YYYY-MM-DD (UK)")
    a.add_argument("--title", required=True)
    g = a.add_mutually_exclusive_group(required=True)
    g.add_argument("--file", type=Path)
    g.add_argument("--frame", type=Path, help="0.3 s frame image (e.g. Studio player capture)")
    a.add_argument("--source", default=None)
    a.add_argument("--status", default="live", choices=["live", "scheduled", "retired"])

    f = sub.add_parser("fetch", help="register a PUBLIC Short by downloading its first second")
    f.add_argument("--id", required=True)
    f.add_argument("--date", required=True)
    f.add_argument("--title", required=True)

    s = sub.add_parser("status", help="mark an entry live/scheduled/retired (retired = private, no longer compared)")
    s.add_argument("--id", required=True)
    s.add_argument("--status", required=True, choices=["live", "scheduled", "retired"])

    l = sub.add_parser("list")
    l.add_argument("--air-date", default=date.today().isoformat())
    l.add_argument("--days", type=int, default=LOOKBACK_DAYS)
    l.add_argument("--all", action="store_true")

    sub.add_parser("compare", help="pairwise dHash distances inside the library")

    ns = ap.parse_args(argv)
    lib = load_lib()

    if ns.cmd == "check":
        air = date.fromisoformat(ns.air_date)
        results = [check(p.resolve(), air, ns.days, lib, ns.sheet_dir, ns.id) for p in ns.files]
        if ns.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            for r in results:
                db = r["audio"].get("mean_db")
                audio = f"{db:.1f}dB" if db is not None else "none"
                print(f"{r['verdict']}  {Path(r['file']).name}  dur={r['duration_s']}s  audio={audio}  motion={r['motion_0_1s']}  dhash={r['dhash']}  visor={r['orbit']['visor_frac']}")
                for x in r["fails"]:
                    print(f"   FAIL  {x}")
                for x in r["warns"]:
                    print(f"   warn  {x}")
                if r.get("contact_sheet"):
                    print(f"   sheet {r['contact_sheet']}")
        return 1 if any(r["fails"] for r in results) else 0

    if ns.cmd == "add":
        src = (ns.file or ns.frame).resolve()
        t = OPEN_T if ns.file else None
        e = add_entry(lib, ns.id, ns.date, ns.title, src, ns.source or ("local_export" if ns.file else "frame"), t, ns.status)
        save_lib(lib)
        print(json.dumps(e, indent=2, ensure_ascii=False))
        return 0

    if ns.cmd == "fetch":
        if not shutil.which("yt-dlp"):
            print("yt-dlp missing", file=sys.stderr)
            return 2
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / f"{ns.id}.mp4"
            run(
                ["yt-dlp", "-q", "--no-warnings", "-f", "bv*[height<=720]/b", "--download-sections", "*0-2",
                 "--force-keyframes-at-cuts", "-o", str(out), f"https://www.youtube.com/shorts/{ns.id}"]
            )
            e = add_entry(lib, ns.id, ns.date, ns.title, out, "yt-dlp_public", OPEN_T, "live")
        save_lib(lib)
        print(json.dumps(e, indent=2, ensure_ascii=False))
        return 0

    if ns.cmd == "status":
        for e in lib["entries"]:
            if e["id"] == ns.id:
                e["status"] = ns.status
                save_lib(lib)
                print(json.dumps(e, indent=2, ensure_ascii=False))
                return 0
        print("id not in library", file=sys.stderr)
        return 2

    if ns.cmd == "list":
        air = date.fromisoformat(ns.air_date)
        rows = lib["entries"] if ns.all else window(lib, air, ns.days)
        for e in rows:
            print(f"{e['date']}  {e['id']}  {e['dhash']}  visor={e['orbit']['visor_frac']:.4f}  {e.get('status','live'):9s} {e['title']}")
        return 0

    if ns.cmd == "compare":
        es = [e for e in lib["entries"] if e.get("status") != "retired"]
        for i, a_ in enumerate(es):
            for b_ in es[i + 1:]:
                bits = hamming(int(a_["dhash"], 16), int(b_["dhash"], 16))
                if bits <= DHASH_WARN_BITS:
                    tag = "FAIL" if bits <= DHASH_FAIL_BITS else "warn"
                    print(f"{tag} {bits:2d} bits  {a_['id']} ({a_['date']})  ↔  {b_['id']} ({b_['date']})")
        return 0
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr.decode(errors="replace"))
        raise SystemExit(2)
