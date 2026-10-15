# 026 picture lock v05d — master copies (J0323, 15 Oct 2026)

Picture lock is the Chief-passed v05d (PR #152 `158fba69`, J0148). Same bytes in all three places:

`69c89d83abe51131a95fd2d3ad77af236366c7613f7c15ba92b4e2945da94cfc`

| Copy | Path |
|---|---|
| Project | `07_Edit-Project/026_NearestStar_v05d.mp4` |
| OWB UAT (Ben's watch) | `OWB UAT/026_NearestStar_v05d.mp4` |
| NAS youtube-staging | `/Volumes/data/mac-mini-archive/youtube-staging/026/026_NearestStar_v05d.mp4` |

8 min 14 s (494.476 s), 1920×1080, 30 fps, 14,803 frames, video + audio. The file that lived only at `/private/tmp/026_NearestStar_v05d_PHONE.mp4` had been purged. It was rebuilt from the NAS v05b master (`43f93eec…`, hash matched the pack) with `_overlay_nearest_star_v05c.py` then `_overlay_nearest_star_v05d.py`. The v05c hash matched `f118c755…` and the v05d hash matched the Chief-passed file above. Audio MD5 is unchanged from v05c.

Dry-run PASS (15 Oct 2026): Private, `publishAt` 2026-11-15T18:00:00Z, no video id. Result: `11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-15T19-25-50-698Z.json`. Final OK is parked for Chief. Captions and the trailer are still unset in this package.
