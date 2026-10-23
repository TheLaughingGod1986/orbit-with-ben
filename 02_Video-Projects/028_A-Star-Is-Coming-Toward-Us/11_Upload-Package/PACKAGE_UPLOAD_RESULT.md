# 028 Gliese 710 — Package Upload Result & Read-Back (J0890)

- **Date:** 2026-10-23T20:40:27Z
- **Job:** J0890 (`028 Gliese 710: Private upload of master v03 for Sun 29 Nov 18:00 London, read back, record`)
- **Authorisation:** Chief PASS on J0889 (`69d46502e`)
- **Result JSON:** `PACKAGE_UPLOAD_RESULT_2026-10-23T20-40-27-397Z.json`

## 1. Upload & Schedule Summary

- **Video ID:** `F-jImX5h7ws` (`https://youtu.be/F-jImX5h7ws`)
- **Studio Edit URL:** `https://studio.youtube.com/video/F-jImX5h7ws/edit`
- **Master File:** `/Volumes/data/mac-mini-archive/youtube-staging/028/028_Gliese710_full_master_v03.mp4`
- **Master SHA-256:** `a9780e548a2775f4e7a1acecb6ac24308927f0b58ab1d606e67d27741e3db824`
- **Title:** `What Happens When a Star Passes Through Our Solar System?`
- **Privacy Status:** `private`
- **Scheduled Publish Time (`publishAt`):** `2026-11-29T18:00:00.000Z` (Sun 29 Nov 2026 18:00 London)
- **Primary Thumbnail (`thumbnails.set`):** **Set** (`02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/08_Thumbnail/abc_v01/gliese_thumb_A.jpg` — `STAR VISITOR`)
- **Registered in `00_Brand/Channel-Setup/social/UPLOADS.json`:** Yes (`F-jImX5h7ws`, `2026-10-23T20:40:27.216Z`)
- **Buffer Mirror (`buffer` block):**
  ```json
  {
    "sent": false,
    "deferred": "goes public 2026-11-29T18:00:00.000Z, beyond Buffer's 7-day window: the daily check schedules it nearer the time",
    "planOnly": false,
    "errors": [],
    "warnings": [],
    "results": []
  }
  ```

## 2. YouTube Data API v3 Read-Back (`videos?part=snippet,status,contentDetails&id=F-jImX5h7ws`)

```json
{
  "id": "F-jImX5h7ws",
  "title": "What Happens When a Star Passes Through Our Solar System?",
  "categoryId": "28",
  "tagsCount": 8,
  "thumbnails": [
    "default",
    "medium",
    "high",
    "standard",
    "maxres"
  ],
  "maxresThumbUrl": "https://i9.ytimg.com/vi/F-jImX5h7ws/maxresdefault.jpg?sqp=CKCM79YG&rs=AOn4CLA4Qx6ojG_F6sVR7F1-DJGGMGYuLA",
  "privacyStatus": "private",
  "publishAt": "2026-11-29T18:00:00Z",
  "madeForKids": false,
  "selfDeclaredMadeForKids": false
}
```

## 3. Studio-Only Finish Steps Remaining (`pending_studio`)

1. **Test & Compare (Thumbnail ABC):** Not available via YouTube Data API. Arm in Studio (`https://studio.youtube.com/video/F-jImX5h7ws/edit`) with `gliese_thumb_A.jpg` (`STAR VISITOR`), `gliese_thumb_B.jpg` (`COMET NUDGE`), and `gliese_thumb_C.jpg` (`SUN'S NEIGHBOUR`).
2. **First / Pinned Comment:** Data API `commentThreads.insert` returned 403 (`forbidden` on private scheduled video) and has no official pin endpoint. Post and pin `Pinned-Comments/gliese_pinned_v01.txt` in Studio Comments (`https://studio.youtube.com/video/F-jImX5h7ws/comments`).
3. **End Screen + Cards:** Studio only — add subscribe + best next video.
4. **Captions (`en-GB`):** Upload `Captions/gliese_long_v03_en-GB.srt` (126 cues) in Studio Subtitles.
