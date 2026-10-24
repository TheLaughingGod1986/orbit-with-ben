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

## 4. Studio finish — J0894, Codex, 24 October 2026

Authorised by the J0894 job brief; £0 spent. Read back in the Orbit Studio browser (CDP 9223) after saving and reloading. No privacy or schedule controls were changed. Studio still shows **Scheduled**; the existing 29 November 18:00Z schedule remains the upload record above.

- **Captions:** set this video's language to **English (United Kingdom)** (it was unset). Uploaded `Captions/gliese_long_v03_en-GB.srt` using **With timing**, then **Done**. Reopened the subtitle editor: English (United Kingdom), timed captions, first two cues “There is a star coming towards us.” / “So how close will it get, and should you worry?”. The supplied file has 126 cues; the editor virtualises rows, so only its visible cues were read back.
- **Thumbnail test:** selected **Thumbnail only**, uploaded `gliese_thumb_A.jpg`, `gliese_thumb_B.jpg`, `gliese_thumb_C.jpg` to slots 1–3, selected **Set test**, then saved the details page. Reopening A/B testing after reload prompted **Run a new test? Your current test will be deleted.** Selected **Cancel** and left the existing test alone. No title test or title edit.
- **End screen:** saved the 1 video + 1 subscribe template. Reopened editor confirms **Subscribe: Orbit With Ben** and **Video: Best for viewer**, with the selected element spanning **7:57:25–8:17:25** (last 20 seconds, Studio frame time). Studio warns that end screens will not display on private videos.
- **Card:** saved **How Far Is the Nearest Star?** (`c5AdqQsnnys`, OWB 026) at **1:30:00**. Reopened Cards confirms that title and time. This related long is scheduled before 028. Optional teaser/custom copy left empty.
- **Pinned comment: blocked until 29 November 2026 18:05 London.** Studio Comments shows no comments and no new-comment composer for this scheduled private video. The upload record already reports API 403. `Pinned-Comments/gliese_pinned_v01.txt` remains the exact copy to post and pin after go-public. No comment was posted.

Next: Chief reviews this record/PR; after go-public, post and pin the supplied comment and read it back. This worker makes no final OK or PASS.
