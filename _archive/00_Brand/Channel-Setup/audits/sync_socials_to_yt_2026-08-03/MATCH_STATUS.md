# Social match to YouTube — 2026-08-03

## Source of truth

**Target for socials = 4** public YouTube Shorts:

| YouTube ID | Short | Visibility |
|---|---|---|
| `1HuV8o3gOss` | Where Is Everybody? (v02) | **public** |
| `dPMJQp2gMNc` | Space Is Rude About Distance (v02) | **public** |
| `rFJoOdQAc9c` | What If Aliens Are Watching Us? (v02) | **public** |
| `KcKBixwmcV4` | First Alien Clue (v02) | **public** |

## Live matrix (latest)

| Platform | Live | Match? | Notes |
|---|---:|---|---|
| YouTube | 4 | ✓ | Old v01s privatized |
| Instagram | 4 | ✓ | All four Reels live |
| Facebook Page | 4 | ✓ | Page reels tab shows all four |
| Threads | 3–4 | △ | Everybody / Watching / Clue on **profile**. Distance **is published** (permalinks below) but Threads is **not listing it on the profile grid** |
| TikTok | 3 | ✗ | Everybody / Distance / Watching live. **Clue blocked** by Studio `status_code: 21` community-guideline temp ban (+ Content check lite daily limit) |

### Threads Distance permalinks (live, not on profile grid)

- https://www.threads.com/@orbitwithben/post/DblNwwOjOcl
- https://www.threads.com/@orbitwithben/post/DblMYecDCGa

### TikTok blocker (confirmed network)

```json
{
  "endpoint": "POST /tiktok/web/project/post/v1/",
  "status_code": 21,
  "status_msg": "Due to multiple Community Guideline violations, you’re temporarily prevented from posting. View details in your app notifications."
}
```

UI also shows: “You've reached your check limit for today. Try again tomorrow.”

## Next actions

1. **TikTok Clue** — retry tomorrow after the ban / check-limit window. Use `TikTok/auto/studio_upload.py` (Content check lite toggle hardened). File: `aliens_short-04_hidden-clues_v02.mp4`.
2. **Threads Distance** — post exists via permalink; if it still never appears on the profile grid, try a phone-app post or a softened title (Threads may be soft-hiding “Rude About Distance” from the grid). Optional: delete duplicate Distance permalinks once one shows on profile.
3. Re-verify matrix after TikTok ban lifts.
