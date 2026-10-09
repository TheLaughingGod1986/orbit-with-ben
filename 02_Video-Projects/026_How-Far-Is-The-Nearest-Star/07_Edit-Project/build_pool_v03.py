#!/usr/bin/env python3
"""026 pool v03 = pool_v02 + Claude #6074250379 additions: 4 more ESO time-lapses
and 8 unannotated star-field plates. Files fetched into pool_v01/ (gitignored)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V02 = json.loads((HERE / "pool_v02.json").read_text())

ESO = "ESO (CC BY 4.0)"
HUB = "ESA/Hubble & NASA (CC BY 4.0)"

NEW = [
    dict(section="timelapse", source="eso", id="uhd_bt_paranal_06", file_id="uhd_bt_paranal_06",
         title="Yepun takes centre stage (time-lapse, UHD 13.4 s)", credit=ESO,
         rows="night-sky fill", orig="https://cdn.eso.org/videos/ultra_hd/uhd_bt_paranal_06.mp4",
         video=True, mute=True, note="clean full length; laser guide star appears ~10.5 s"),
    dict(section="timelapse", source="eso", id="uhd_bt_paranal_07", file_id="uhd_bt_paranal_07",
         title="Yepun in action (time-lapse, UHD 8.8 s)", credit=ESO,
         rows="night-sky fill", orig="https://cdn.eso.org/videos/ultra_hd/uhd_bt_paranal_07.mp4",
         video=True, mute=True, note="dome moves/blurs ~0.5-2 s; use 2.0-8.8 s"),
    dict(section="timelapse", source="eso", id="uhd_yb_paranal_02", file_id="uhd_yb_paranal_02",
         title="Auxiliary Telescope at work at Paranal (time-lapse, UHD 10.8 s)", credit=ESO,
         rows="night-sky fill", orig="https://cdn.eso.org/videos/ultra_hd/uhd_yb_paranal_02.mp4",
         video=True, mute=True, note="clean full length; sky brightens toward dawn after ~6 s"),
    dict(section="timelapse", source="eso", id="vltfromvistatimelapse", file_id="vltfromvistatimelapse",
         title="A VISTA on the VLT (time-lapse, 720p 29.4 s)", credit=ESO,
         rows="night-sky fill", orig="https://cdn.eso.org/videos/hd_and_apple/vltfromvistatimelapse.m4v",
         video=True, mute=True,
         note="clean only 3.5-14.0 s (dusk). ESO logo card 0-3 s and 26-29 s; 15-24 s near-black; "
              "daylight frame ~24 s then white flash. 1.5x upscale"),
    dict(section="starfield", source="eso", id="eso0844a", file_id="eso0844a",
         title="The globular cluster Omega Centauri", credit=ESO, rows="star-field fill",
         orig="https://cdn.eso.org/images/large/eso0844a.jpg", labels=False, size="8040x7560"),
    dict(section="starfield", source="esahubble", id="heic0809a", file_id="heic0809a",
         title="The majestic globular Omega Centauri", credit=HUB, rows="star-field fill",
         orig="https://cdn.esahubble.org/archives/images/large/heic0809a.jpg", labels=False, size="11936x10891"),
    dict(section="starfield", source="eso", id="eso1302a", file_id="eso1302a",
         title="The globular star cluster 47 Tucanae", credit=ESO, rows="star-field fill",
         orig="https://cdn.eso.org/images/large/eso1302a.jpg", labels=False, size="8246x8246"),
    dict(section="starfield", source="eso", id="eso1323a", file_id="eso1323a",
         title="The globular star cluster NGC 6752", credit=ESO, rows="star-field fill",
         orig="https://cdn.eso.org/images/large/eso1323a.jpg", labels=False, size="8221x8023"),
    dict(section="starfield", source="eso", id="eso1250a", file_id="eso1250a",
         title="The Carina Nebula imaged by the VLT Survey Telescope", credit=ESO, rows="star-field fill",
         orig="https://cdn.eso.org/images/large/eso1250a.jpg", labels=False, size="17383x18656",
         note="too large for ffmpeg's mjpeg decoder: pre-shrink with sips -Z 8000"),
    dict(section="starfield", source="eso", id="eso0905a", file_id="eso0905a",
         title="The Carina Nebula", credit=ESO, rows="star-field fill",
         orig="https://cdn.eso.org/images/large/eso0905a.jpg", labels=False, size="8408x8337"),
    dict(section="starfield", source="eso", id="eso1031a", file_id="eso1031a",
         title="The Carina Nebula around the Wolf-Rayet star WR 22", credit=ESO, rows="star-field fill",
         orig="https://cdn.eso.org/images/large/eso1031a.jpg", labels=False, size="8395x8261"),
    dict(section="starfield", source="esahubble", id="heic1007a", file_id="heic1007a",
         title="Hubble captures view of 'Mystic Mountain' (Carina)", credit=HUB, rows="star-field fill",
         orig="https://cdn.esahubble.org/archives/images/large/heic1007a.jpg", labels=False, size="2104x1937"),
]

if __name__ == "__main__":
    have = {e["id"] for e in V02}
    out = V02 + [e for e in NEW if e["id"] not in have]
    (HERE / "pool_v03.json").write_text(json.dumps(out, indent=1) + "\n")
    for e in NEW:
        assert (HERE / "pool_v01" / ("timelapse" if e.get("video") else "") / (e["file_id"] + (".mp4" if e.get("video") else ".jpg"))).exists(), e["id"]
    print(f"pool_v03.json: {len(out)} entries ({len(out) - len(V02)} new)")
