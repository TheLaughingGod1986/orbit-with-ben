# Orbit Thursday week ship

**Locked:** 15 Sep 2026 (Moon Leaving night). End-to-end ops for one Orbit With Ben Cosmic Journey week — Premiere long, Scout/VidIQ listing polish, seven companion Shorts, calendar, playlists, and Studio Related.

Picture/cut UAT stays on **Orbit Auditor** — see [`.cursor/rules/orbit-auditor-ship-gate.mdc`](../../.cursor/rules/orbit-auditor-ship-gate.mdc) and [`00_Brand/Channel-Setup/ORBIT_HOUSE_AND_UAT_BIBLE.md`](../../00_Brand/Channel-Setup/ORBIT_HOUSE_AND_UAT_BIBLE.md). This playbook is calendar + Studio + listing + Shorts pack ops **after** a long is KEEP/LOCK.

Related Shorts funnel rules: [`.cursor/rules/orbit-shorts-related-video.mdc`](../../.cursor/rules/orbit-shorts-related-video.mdc) · [`00_Brand/Channel-Setup/SHORTS_FUNNEL_AND_CROSSPOST.md`](../../00_Brand/Channel-Setup/SHORTS_FUNNEL_AND_CROSSPOST.md). YouTube API upload path: [`YOUTUBE_PACKAGE_UPLOAD.md`](YOUTUBE_PACKAGE_UPLOAD.md).

## Locks (standing)

- Channel `UC_esArsDKd3GJvOkeO0DUog` · Studio Google `benoats86@gmail.com`.
- One Thursday long Premiere **18:00 Europe/London**.
- That week’s Shorts: **7 punches** from that film only, **Fri–Thu 11:30 Europe/London** (`publishAt` = 10:30Z while BST).
- Short CTA: **Related video = that Thursday long only**. Zero `/go/` on Shorts. No Orbit on Short thumbs. Exact long listing title on Short last card.
- New Shorts: **no new pinned comments** unless Ben overrides for that pack (Related is the primary Short → long click).
- Longs: pins OK; `/go/` only when the cut names the product in VO and on screen.
- Cursor cloud for any repo work: **best model for the job — never Auto**.
- Large video upload: run **YouTube Data API on the Mac Mini** (box CopyFromBox truncates ~768KB). Tokens live under Mini `~/Desktop/Moon_Leaving_Premiere_Upload/direct-upload/.secrets/` (or the week’s upload folder).
- Never paste passwords in chat. Ben signs into Studio / VidIQ / Flow himself.

## Phase 0 — Gate

1. Auditor HARD PASS on the full long; Ben KEEP/LOCK (or explicit ship).
2. Park house lessons in the Orbit repo if new failures were fixed this cut.
3. Confirm Desktop/iCloud deliverable path + sha256 on Mini.

## Phase 1 — Long listing (Scout + VidIQ)

1. **Channel Scout** live niche scan (`POST /api/discover` with site Origin, seed = primary topic). Keep **usable** searchTerms only; discard stopword fragments (`the moon`, `of the`, …).
2. **VidIQ** Research For You / Optimize when signed in; if login wall, use last on-box Orbit VidIQ shots — never invent volumes.
3. Title: prefer Scout-backed phrasing; do not retitle a locked Premiere without Ben.
4. Tags: Scout usable + VidIQ broad For You (e.g. documentary / facts / nasa) inside ~500 char budget. Education category `27`.
5. Description: first-line hook (not title-echo), chapters, hashtags. Zero `/go/` unless affiliate gate passes.
6. Thumb: picture + short hook, no Orbit. Lock A through Premiere unless Ben A/B’s.

## Phase 2 — Upload Premiere (Mini API)

1. Resumable upload: `privacyStatus=private`, `publishAt` = Thursday 17:00Z (18:00 London BST).
2. Set custom thumb via API.
3. Verify channel id = Orbit With Ben before upload.
4. Studio: confirm real **Premiere** chrome (API schedule ≠ Premiere by itself).
5. Add long to **Start Here — Biggest Mysteries of Space** (`PLI1AApUz3qz8`) plus topic playlist if one fits.
6. Do not change premiere time after lock.

## Phase 3 — Shorts pack build

1. Seven titles + yellow CTR thumbs locked with Ben before cut when possible.
2. Prefer **iCloud / Mini rough punches** as true plates. If box cuts used wrong plates, rebuild **on Mini** (ffmpeg + PIL) — do not rely on CopyFromBox for multi‑MB mp4s.
3. House: picture-first ~1s; 22–27s; mid captions; exact long title last card; no Orbit on thumb; zero `/go/`.
4. Pack folder on Mini Desktop: `cuts/` + `thumbs/` + pack markdown with sha256 + schedule slots.
5. Auditor scores the pack before public; Ben may greenlight schedule after upload private.

## Phase 4 — Shorts upload + calendar

1. Upload each Short private + `publishAt` Fri→Thu 11:30 London.
2. Set yellow thumbs via API.
3. **Studio-only:** Related video → Thursday Premiere id on every Short.
4. Pin comment only if Ben overrode for this pack; otherwise skip (API may 403 without comment scope anyway).
5. Clear calendar conflicts: Private leftover Shorts that steal the Fri–Thu 11:30 slots (keep Neutron/other scheduled weeks unless Ben says clear).
6. Premiere stays first on the week calendar.

## Phase 5 — Growth hygiene (same week)

1. All public longs in Start Here.
2. Education category on longs.
3. Channel keywords leave alone if already set.
4. Studio leftovers checklist: Featured shelves, end screens Subscribe + playlist, subscribed trailer, channel `/go` links, Europa-style first-line hook polish.

## Do not

- Upload Shorts before plates are true (no provisional wrong-part cuts).
- Dump Shorts Public immediately on finish — always schedule.
- Put `/go/` on Shorts.
- Mix HOS / Oppti Studio accounts with Orbit.
- Fake VidIQ metrics when auth fails.
- Merge Scout/product PRs that invent VidIQ numbers.

## Roles

- **Chief of Staff:** runs this playbook, Scout+VidIQ listing pass, Mini API upload, calendar, briefs.
- **Orbit Creator:** Studio Premiere chrome, Related pills, listing paste when needed.
- **Orbit Auditor:** cut/thumb ship gate only (see Video Auditor ship gate docs above).
- **Money King:** `/go/` longs only when affiliate gate passes.
