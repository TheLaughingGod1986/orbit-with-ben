# 027 v01i master copies (J0267, 15 Oct 2026)

sha256 `f74ca3e8a27b3897fd4942ebcd6f70462aee039146ccce1780216c42802be38b` (as `SHA256.txt`).

| Copy | Path | sha256 checked |
|---|---|---|
| OWB UAT (iCloud Drive) | `OWB UAT/027_EarthSpin_rough_v01i.mp4` | match, 15 Oct 13:08 UK |
| Film folder | `02_Video-Projects/027_.../07_Edit-Project/027_EarthSpin_rough_v01i.mp4` | match, 15 Oct 13:08 UK |
| NAS | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/027_EarthSpin_rough_v01i.mp4` | match, 15 Oct 13:12 UK |

The NAS file was written while `umount -f /Volumes/data` was stuck, through a second mount of the same export (`192.168.1.119:/volume1/data`) at `/Volumes/data-j0267`. That second mount was removed after the hash matched. A sha256 manifest sits beside the file: `027_EarthSpin_rough_v01i.mp4.sha256`.

`/private/tmp/027_EarthSpin_rough_v01i.mp4` matches the same hash and is scratch only. The NAS copy and the OWB UAT copy are the masters.
