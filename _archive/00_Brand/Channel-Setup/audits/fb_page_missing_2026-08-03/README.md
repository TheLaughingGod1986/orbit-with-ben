# Facebook Page / social funnel — 2026-08-03

## Correct funnel (YT-first)

Shorts are **scheduled on YouTube**. When each goes live, LaunchAgent watchers
mirror to Instagram, Facebook Page, Threads, and TikTok:

- `Meta/AUTO_POST.md`
- `TikTok/AUTO_POST.md`
- `Threads/AUTO_POST.md`

Do **not** manually post those shorts to FB/IG/Threads/TikTok ahead of the
YouTube `schedule_iso`.

Aliens 01–03 (Europe/London):

| Short | Title | YouTube go-live |
|------|------|-----------------|
| 01 | Where Is Everybody? | 2026-08-04 12:30 |
| 02 | Space Is Rude About Distance | 2026-08-11 12:30 |
| 03 | What If Aliens Are Watching Us? | 2026-08-18 12:30 |

## Cleanup done

1. Premature **Facebook Page** reels for 01–03 deleted (Page Reels empty again).
2. Premature **Instagram** reels deleted:
   `Dbkjz74gTje`, `DbkkMoxjwpt`, `DbkkmlLEwbH`
3. Premature **Threads** video posts for the same three titles deleted.
4. Cleared ledger keys `yt:1HuV8o3gOss`, `yt:dPMJQp2gMNc`, `yt:rFJoOdQAc9c`
   from `META_POSTED.json` + `THREADS_POSTED.json`.
5. Meta/Threads `is_live()` now respects future `schedule_iso` (same as TikTok).
6. Aliens index flags for 01–03 reset to `scheduled` / not `published_now`.

Artifacts: `audits/premature_social_cleanup_2026-08-03/`,
`audits/fb_page_retry_2026-08-03/V18D_DELETE.json`.

## Still recommended

1. Re-login `~/.orbit-chrome-meta-dev` on `:9223` with `--remote-allow-origins=*`.
2. Suite → **Connect a Facebook Page** → Orbit with Ben so Meta auto-posts hit the Page.
3. Optional: delete leftover legacy IG `/p/Cq1MAN9I4pb/` when rate limits allow.
