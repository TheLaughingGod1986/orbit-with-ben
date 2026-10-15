#!/usr/bin/env python3
"""027 Earth Spin v01i (J0265): the house SFX stem for the v01i cut (Polish pass 1), and its level check. No spend.

Kit: kit_v01 (scripts/sfx_kit.py make, own synthesis). The VO stem is v01i's own audio (VO only, -14 LUFS; no bed
until take 2), so the level check runs on the cut's real timeline. Writes, next to this script:
  stem_sfx_v01i.wav (48 kHz stereo, the cut's full length, gitignored), sfx_cues_v01i.json, sfx_level_v01i.json.
Cues sit on picture, never on plain cuts:
  tick    every label and timeline marker in v01i (overlays_v01i.json), on its in-time
  whoosh  the cut into a fast orbital or time-lapse fly-through, peaking on the cut
  rumble  under a huge or violent shot, starting with it
`--plan` prints the cues without rendering."""
from pathlib import Path
import json, subprocess as sp, sys, wave
import numpy as np

HERE = Path(__file__).resolve().parent
EP = HERE.parent
REPO = EP.parent.parent
KIT = HERE / "kit_v01"
PACK = EP / "07_Edit-Project/rough_v01i_pack"
MASTER = Path("/private/tmp/027_EarthSpin_rough_v01i.mp4")
WORK = Path("/private/tmp/earth027_sfx_v01i")
SR = 48000

GAIN_DB = {"tick": -2.0, "whoosh": -10.0, "rumble": -4.0}
FILES = {"tick": "sfx_owb_tick_ui_v01.wav", "whoosh": "sfx_owb_whoosh_soft_v01.wav", "rumble": "sfx_owb_rumble_low_v01.wav"}

# (kind, start s, why)
WHOOSH = [
    (13.333, "row 2 ISS sunrise-to-sunset pass (orbital sweep)"),
    (74.300, "row 14 Gerst Earth time-lapse fly-over"),
    (225.933, "row 21 Gerst time-lapse over the stopped planet's terminator"),
    (415.067, "row 35 Gerst time-lapse fly-over"),
]
RUMBLE = [
    (32.000, "row 11 air: the atmosphere keeps going east at 1,500+ km/h"),
    (44.600, "row 12 sea surge: the oceans rise against every eastern coast"),
    (385.567, "row 34 lava fountain: Earth's molten core"),
    (431.400, "row 37 early Earth: something set Earth spinning 4.5 billion years ago"),
]


def read_wav(p):
    with wave.open(str(p)) as w:
        assert w.getframerate() == SR and w.getsampwidth() == 2
        a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768.0
        return a.reshape(-1, w.getnchannels())


def cues():
    ov = json.loads((PACK / "overlays_v01i.json").read_text())
    ticks = sorted({round(x["start"], 3) for x in ov["labels"] if not x["file"].endswith("_timeline.png")})
    out = [("tick", t, next(x.get("text", "") for x in ov["labels"] if round(x["start"], 3) == t)) for t in ticks]
    whoosh_len = len(read_wav(KIT / FILES["whoosh"])) / SR
    out += [("whoosh", round(t - whoosh_len / 2, 3), why) for t, why in WHOOSH]
    out += [("rumble", t, why) for t, why in RUMBLE]
    return sorted(out, key=lambda c: c[1])


def main():
    cs = cues()
    if "--plan" in sys.argv:
        for k, t, why in cs:
            print(f"{int(t // 60)}:{t % 60:05.2f}  {k:6}  {why}")
        return 0
    WORK.mkdir(parents=True, exist_ok=True)
    dur = float(sp.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(MASTER)]))
    vo = WORK / "stem_vo_v01i.wav"
    sp.run(["ffmpeg", "-y", "-v", "error", "-i", str(MASTER), "-map", "0:a", "-ac", "2", "-ar", str(SR), str(vo)], check=True)
    mix = np.zeros((int(round(dur * SR)), 2), dtype=np.float32)
    kit = {k: read_wav(KIT / f) for k, f in FILES.items()}
    for k, t, _ in cs:
        s = kit[k] * 10 ** (GAIN_DB[k] / 20)
        i = int(round(t * SR)); n = min(len(s), len(mix) - i)
        mix[i:i + n] += s[:n]
    stem = HERE / "stem_sfx_v01i.wav"
    with wave.open(str(stem), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype("<i2").tobytes())
    (HERE / "sfx_cues_v01i.json").write_text(json.dumps(dict(
        cut=str(MASTER), cut_seconds=round(dur, 3), kit="kit_v01 (own synthesis)", gain_db=GAIN_DB,
        cues=[dict(kind=k, start=t, why=why) for k, t, why in cs], spend="none"), indent=2) + "\n")
    r = sp.run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "level", "--vo", str(vo), "--sfx", str(stem),
                "--minutes", f"{dur / 60:.2f}", "--out", str(HERE / "sfx_level_v01i.json")])
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
