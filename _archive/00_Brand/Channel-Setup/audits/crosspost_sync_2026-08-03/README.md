# Cross-post sync — 2026-08-03

## Verdict

| Platform | Status |
|----------|--------|
| YouTube | OK — 3 live + 13 scheduled |
| Meta (IG/FB) | COMPLETE — 3 live + 13 scheduled at YT times (verified in Suite UI) |
| Threads | 3 live posted; LaunchAgent `dev.orbit.threads-live-shorts` posts remaining at YT go-live |
| TikTok | **BLOCKED** — Community Guideline temporary posting ban (`status_code: 21`) |

## TikTok blocker

API `POST /tiktok/web/project/post/v1/` returns HTTP 200 with:

```text
status_code: 21
status_msg: Due to multiple Community Guideline violations, you're temporarily
prevented from posting. View details in your app notifications.
```

Schedule/Post CTA clicks look fine in the UI but nothing publishes.

### TikTok Studio now

- Zoo — 3 Aug 12:30pm
- Distance — 2 Aug 12:30pm
- Fermi — 1 Aug 5:00pm
- Drifted exo Aug 21–26 **deleted**
- Missing until unban: clue (today 12:30), BH Aug 5–10, exo Aug 12–17

### After unban

1. Open TikTok mobile → Notifications → clear/resolve restriction  
2. Upload clue + 6 BH + 6 exo with `_upload_missing_v02_cdp.py` scheduler (verify schedule values, then click Schedule)  
3. Confirm Aug 1–3 aliens actually published (they still show 0 views)

## Key artifacts

- `PLATFORM_STATUS.json` — current matrix  
- `META_SCHEDULE_V03.json` — Meta 13/13 ok  
- `TIKTOK_POSTING_BLOCKED.json` — ban evidence  
- `../_fix_meta_schedule_v03.py` — Meta date/time helper  
- `../TikTok/_upload_missing_v02_cdp.py` — TikTok upload helper  
