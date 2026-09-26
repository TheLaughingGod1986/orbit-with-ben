# Channel audit fix log — 24 Sep 2026

## Prepared, not applied (25 Sep 2026 cloud agent)

Studio / live YouTube were **not** touched. Branch work only.

### Thumbnail refresh (see `../THUMBNAIL_TITLE_AUDIT_2026-09-25/REFRESH_LOG.md`)

- Batch A Shorts: 2 built (`9lLZMy8rBJo`, `CkSECfUfH2Y`); 6 **NEEDS PLATE** (Orbit or wrong subject; masters/yt-dlp unavailable).
- Batch B longs: Test & Compare variants built for Neutron, Last Star, Europa, Fermi; Andromeda straight replacement `WHEN THEY MEET`. Black Hole **NEEDS PLATE** (Orbit on current). Jupiter thumbs missing from sparse checkout — preview deferred.
- Left alone: `2fsQcea-voM`, `ziKBPJ6FY0U`, `b8-X_FyJnHM`.
- Contact sheet + artifacts under audit `refresh/` and `/opt/cursor/artifacts/thumb-refresh-2026-09-25/`.

### Titles (propose only)

| id | proposed | applied? |
|---|---|---|
| `P9Jiw-MwUEU` | Is Andromeda Already in Our Sky? | no |
| `xQlV9G9lqLI` | Stars Almost Never Hit When Galaxies Collide | no |
| `68uTDP2esso` | note only: The Early Universe Is Hiding a Massive Secret | no |

### Studio fix list from AUDIT.md §4

| # | item | status |
|---|---|---|
| 1 | Andromeda long retitle | not applied (needs Content Ops `.env` / Studio) |
| 2–3 | scheduled Short retitles in `STUDIO_FIXES.json` | not applied |
| 4 | Andromeda thumb → WHEN THEY MEET | **file prepared**, not uploaded |
| 5–6 | Andromeda Short retitles | proposals only |
| 7 | phone sound check of Andromeda Shorts | not done here |

### Captions (backlog #4)

Jupiter and Andromeda locked VO scripts **not in this checkout** — caption txts not produced. See `captions/README.md`.

### Jupiter pinned comment (backlog #1)

Proposed final ready in `REFRESH_LOG.md`. `PINNED_COMMENTS.json` still has Ben’s draft question; `commentId` empty until `--create` after public.

### Shorts sweep

Graded other public Shorts; failures listed in `REFRESH_LOG.md` / `refresh/sweep/SWEEP_GRADE.json`. **Not built.**
