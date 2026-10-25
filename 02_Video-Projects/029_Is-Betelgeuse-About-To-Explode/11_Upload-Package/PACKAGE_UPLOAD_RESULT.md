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

## 4. Studio finish — J0923, Cursor, 25 October 2026

Authorised by the J0923 job brief (Chief ruling `6384887788`). £0. Read back in the Orbit Studio browser (CDP 9223, channel `UC_esArsDKd3GJvOkeO0DUog`) after saving and reloading. No privacy or `publishAt` control was changed. Studio still shows **Scheduled**. The Data API read-back after the caption insert was `privacyStatus=private`, `publishAt=2026-12-06T18:00:00Z`.

- **Captions:** video language set to **English (United Kingdom)** (it was unset). Studio's "Upload manual / With timing" dialog parsed the SRT and then `update_captions` returned 400 because it targeted the automatic track (`kind: asr`, `lang: en`). The supplied file was inserted with the Data API as a manual track: id `AUieDabr7MaAWY9EtVpQvzX_rdrNcZM58lFM2EGSJc8OjkyyhXfdq7Yv-r8MTKLaJxwd3DjDqHz1JD7riwo`, language `en-GB`, trackKind `standard`, status `serving`, not a draft. A download of that track matches `Captions/betelgeuse_long_v03b_en-GB.srt` (174 cues, first cue "Look at Orion this winter at / the orange star on its shoulder."). The existing automatic English track was left in place. The language dialog's "Make this the default for my channel" box was already ticked, and Confirm was clicked with it ticked, so the channel upload default may now be English (United Kingdom). `defaultAudioLanguage` on this video is `en-GB`. After the language save, Studio listed 20 translation languages with Audio "Processing…" (auto-dub). Those audio tracks were not removed.
- **Thumbnail test:** Thumbnail only. Slots 1–3 are `betelgeuse_thumb_A.jpg` (BRIGHT AS MOON), `betelgeuse_thumb_B.jpg` (PAST MARS) and `betelgeuse_thumb_C.jpg` (IT WAS DUST). Set test, then saved the details page. Title stayed `Is Betelgeuse About to Explode?`. Reopening A/B testing showed **Run a new test? Your current test will be deleted.** Selected **Cancel** and left the test. The details preview is still BRIGHT AS MOON. Visibility stayed Scheduled. Ledger row `T010` records A and B (both house). C is the third house variant in the same Studio test; the ledger only has an A/B pair.
- **End screen:** the 1 video + 1 subscribe template. Read back after reload: **Subscribe: Orbit With Ben** and **Video: Best for viewer**, **8:42:07–9:02:07** (last 20 seconds; the timeline ends at 9:02:07). Studio warns that end screens will not display on private videos. The Save button was grey on the read-back, so nothing was left unsaved.
- **Card:** saved **What Happens When a Star Passes Through Our Solar System?** (`F-jImX5h7ws`, OWB 028) at **1:30:00**. Reopened Cards confirms that title and time. This related long is scheduled before 029. Teaser shows the video title; no custom message was typed.
- **Pinned comment: blocked until Sun 6 Dec 2026 18:05 London.** Studio Comments shows no comments and no new-comment composer on this scheduled private video. The upload record already reports API 403. `Pinned-Comments/betelgeuse_pinned_v01.txt` is the copy to post and pin after go-public. No comment was posted.

Next: post and pin that comment after go-public, and read it back. This worker makes no final OK or PASS.
