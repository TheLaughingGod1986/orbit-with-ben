# Playback lag on YouTube / Shorts / social

## What viewers are seeing

Audio is smooth. Picture stutters, hitching, or “lags.” Comments landed on
the YouTube channel. Same files go out to TikTok / Instagram / Facebook, so
the glitch follows the master — it is not a YouTube-only CDN bug.

## Root cause

1. **Apple `h264_videotoolbox` on Shorts** (`-c:v h264_videotoolbox` + `-r 30`
   and no `fps=` filter). VideoToolbox writes irregular timestamps (VFR).
   Platforms transcode VFR by dropping/duplicating **video** frames; AAC
   audio is left alone. That is exactly “smooth audio, glitchy video.”
2. **Missing `fps=30` on the caption overlay graph** so still PNG loops and
   the picture track do not share a clock.
3. **Long-form upload mux with `-c:v copy`** after a VFR picture pass, which
   bakes the bad timestamps into the file that gets uploaded.
4. **CapCut “original frame rate”** (README used to allow this). AI clips
   (Veo / Seedance) are often VFR; “original” preserves that.

Re-uploading as a **new** YouTube video would fix the file but reset views,
watch time and make the item look brand-new. Do not do that.

## Reality check (Aug 2026 Studio)

YouTube Studio on this channel **does not expose a Replace / Replace video
file control** (Details ⋮ menu is Download / Delete / Promote only). Official
Help says you can’t replace a video file while keeping the URL:

https://support.google.com/youtube/answer/55770

So `_replace_media_in_place.py` / `_replace_file_on_yt.py` will correctly
**abort** rather than upload a new id.

What still works:

1. **Remaster locals** (`fix_published_playback_lag.py --apply`) — done on Mac.
2. **Future exports** use CFR libx264 so new uploads won’t lag.
3. **Still-scheduled / private** items can be deleted + re-uploaded with the
   remastered file at the **same `publishAt`** (new id, but no public views to
   lose). Do this only with an explicit go-ahead.
4. **Already-public** videos keep their VFR masters on YouTube unless you
   accept a new upload (resets views). Prefer leaving them and fixing forward.

## Fix existing published videos (keep views)

On the machine that has the masters (mp4s are gitignored):

```bash
# 1. Rewrite picture to constant 30 fps libx264. Audio is copied (unchanged).
python3 04_Audio/tools/fix_published_playback_lag.py --apply

# 2. Preview which Studio videos will be updated (same ids)
python3 00_Brand/Channel-Setup/audits/_replace_media_in_place.py --dry-run

# 3. Push the new bytes onto the ORIGINAL videos
python3 00_Brand/Channel-Setup/audits/_replace_media_in_place.py
# alias used in the mobile runbook:
# python3 00_Brand/Channel-Setup/audits/_replace_file_on_yt.py
```

YouTube Studio **Replace** keeps: video id, URL, views, watch time, likes,
comments, publish date. The video may be briefly unavailable while YouTube
reprocesses. Analytics stay on the same item.

**Do not run** `00_Brand/Channel-Setup/audits/_replace_shorts_v02_youtube.py`
for this. That script uploads a new id and deletes the old one.

### Manual Studio fallback

1. [YouTube Studio](https://studio.youtube.com) → Content → the video
2. Details → **Replace** (under the thumbnail, or ⋮ → Replace)
3. Choose the remastered mp4 (same filename after `--apply`)
4. Confirm **Replace video** — do not “Upload videos”

### TikTok / Instagram / Facebook

Those apps do **not** offer a view-preserving file replace on a live post.
YouTube is the canonical copy. Re-post social only if you accept a new post
id there. Never delete-and-reupload the YouTube original to “match” social.

## Prevent it on the next export

| Setting | Required |
|---|---|
| Encoder | `libx264` only (never VideoToolbox / NVENC for **delivery**) |
| Frame rate | Constant 30 fps Shorts; 24/25/30/60 CFR long-form |
| Filter | `fps=<rate>,format=yuv420p` on the **final** picture |
| Mux | `-fps_mode cfr` + x264 `force-cfr=1` + `-movflags +faststart` |
| Audio | Copy AAC when already 48 kHz; otherwise AAC 256k |

Shared helpers:

- `04_Audio/tools/orbit_cfr_delivery.py` — probe + encode args + remaster
- Shorts builders import `shorts_encode_args()`
- Content Ops `probeVideo()` **blocks** VFR / VideoToolbox before publish

CapCut: export **30 fps**, not “original.”


## Mac: open logged-in Studio for Replace

Chrome refuses `--remote-debugging-port` on the default profile path. Clone it
once, then keep that window signed in (passkey / 2FA may be required):

```bash
SRC="$HOME/Library/Application Support/Google/Chrome"
DST="$HOME/.orbit-chrome-youtube-studio"
rsync -a --exclude 'Singleton*' --exclude 'BrowserMetrics*' --exclude 'Crashpad' \
  --exclude 'ShaderCache' --exclude 'GrShaderCache' --exclude 'GraphiteDawnCache' \
  "$SRC/" "$DST/"
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --remote-allow-origins='*' \
  --user-data-dir="$DST" --profile-directory=Default \
  'https://studio.youtube.com/'
```

When `http://127.0.0.1:9222/json/list` shows a `studio.youtube.com` tab (not
accounts.google.com), run `_replace_media_in_place.py`. It connects over CDP
and will not create new video ids.

Scheduled publish times (including Exoplanets Shorts and the 21–26 Aug
cadence) stay on the original ids — Replace does not touch schedule.

## Scheduled / private re-upload (Aug 2026)

Because Studio cannot Replace files, still-scheduled private items were
re-uploaded via API with the remastered CFR master at the same `publishAt`:

```bash
cd 07_Content-Ops
npx tsx scripts/youtube-reupload-scheduled-cfr.ts --dry-run
npx tsx scripts/youtube-reupload-scheduled-cfr.ts --execute --approved-by-user
```

Journal: `00_Brand/Channel-Setup/audits/playback_lag_scheduled_reupload/`.
Already-public videos were left alone.
