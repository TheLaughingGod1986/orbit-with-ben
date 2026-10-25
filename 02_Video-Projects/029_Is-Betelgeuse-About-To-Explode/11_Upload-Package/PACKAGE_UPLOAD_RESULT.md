# 029 Betelgeuse — Package Upload Result & Read-Back (J0922)

- **Date:** 2026-10-25T02:57:29Z
- **Job:** J0922 (`029 Betelgeuse: Private upload of the release master for Sun 6 Dec 18:00 London (after Chief PASS on J0921), read back, record`)
- **Authorisation:** Chief PASS on J0921 (`b3a7f6432` / `926dd979a`, Chief ruling `6384887788`)
- **Result JSON:** `PACKAGE_UPLOAD_RESULT_2026-10-25T02-57-29-461Z.json`

## 1. Upload & Schedule Summary

- **Video ID:** `vP1BbqZ_dnM` (`https://youtu.be/vP1BbqZ_dnM`)
- **Studio Edit URL:** `https://studio.youtube.com/video/vP1BbqZ_dnM/edit`
- **Master File:** `/Volumes/data/mac-mini-archive/youtube-staging/029/029_Betelgeuse_full_rough_v03b.mp4`
- **Master SHA-256:** `54e04d3bfcb42bcf9066a0613254f10c978435b148d158468711e25908060c93`
- **Title:** `Is Betelgeuse About to Explode?`
- **Privacy Status:** `private`
- **Scheduled Publish Time (`publishAt`):** `2026-12-06T18:00:00.000Z` (Sun 6 Dec 2026 18:00 London)
- **Primary Thumbnail (`thumbnails.set`):** **Set** (`02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/08_Thumbnail/abc_v01/betelgeuse_thumb_A.jpg` — `BRIGHT AS MOON`)
- **Registered in `00_Brand/Channel-Setup/social/UPLOADS.json`:** Yes (`vP1BbqZ_dnM`, `2026-10-25T02:57:29.370Z`)
- **Buffer Mirror (`buffer` block):**
  ```json
  {
    "sent": false,
    "deferred": "goes public 2026-12-06T18:00:00.000Z, beyond Buffer's 7-day window: the daily check schedules it nearer the time",
    "planOnly": false,
    "errors": [],
    "warnings": [],
    "results": []
  }
  ```

## 2. YouTube Data API v3 Read-Back (`videos?part=snippet,status,contentDetails&id=vP1BbqZ_dnM`)

```json
{
  "id": "vP1BbqZ_dnM",
  "title": "Is Betelgeuse About to Explode?",
  "categoryId": "28",
  "tagsCount": 8,
  "thumbnails": [
    "default",
    "medium",
    "high",
    "standard",
    "maxres"
  ],
  "maxresThumbUrl": "https://i9.ytimg.com/vi/vP1BbqZ_dnM/maxresdefault.jpg?sqp=CITf9dYG&rs=AOn4CLAQ72AMXyi8H7LDt-Kj_hTvexMF-g",
  "privacyStatus": "private",
  "publishAt": "2026-12-06T18:00:00Z",
  "madeForKids": false,
  "selfDeclaredMadeForKids": false,
  "duration": "PT9M3S"
}
```

## 3. Studio-Only Finish Steps Remaining (`pending_studio` — J0923)

1. **Test & Compare (Thumbnail ABC):** Not available via YouTube Data API. Arm in Studio (`https://studio.youtube.com/video/vP1BbqZ_dnM/edit`) with `betelgeuse_thumb_A.jpg` (`BRIGHT AS MOON`), `betelgeuse_thumb_B.jpg` (`PAST MARS`), and `betelgeuse_thumb_C.jpg` (`IT WAS DUST`).
2. **First / Pinned Comment:** Data API `commentThreads.insert` returned 403 (`forbidden` on private scheduled video) and has no official pin endpoint. Post and pin `Pinned-Comments/betelgeuse_pinned_v01.txt` in Studio Comments (`https://studio.youtube.com/video/vP1BbqZ_dnM/comments`).
3. **End Screen + Cards:** Studio only — add subscribe + best next video.
4. **Captions (`en-GB`):** Upload `Captions/betelgeuse_long_v03b_en-GB.srt` (174 cues) in Studio Subtitles.
