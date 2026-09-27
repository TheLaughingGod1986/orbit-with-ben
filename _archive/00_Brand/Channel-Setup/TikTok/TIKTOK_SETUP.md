# Orbit TikTok — Setup pack

Mirror of YouTube brand for TikTok discovery. Pillar stays YouTube.

## Identity (apply on create)

| Field | Value |
|---|---|
| Display name | **Orbit with Ben** |
| Preferred handle | **@OrbitWithBen** |
| Fallbacks | `@OrbitWithBenYT` · `@MeetOrbit` · `@OrbitExplores` · `@HelloOrbit` · `@OrbitCosmos` |
| Bio (≤80) | `Space stories. Big questions. Full films on YT ↓` |
| Website | https://www.youtube.com/@OrbitWithBen |
| Avatar | Same Orbit mascot as YouTube (`avatar_800x800.png`) |

## Assets

```
00_Brand/Channel-Setup/TikTok/
  avatar_800x800.png      # upload this
  avatar_800x800.jpg
  avatar_200x200.jpg
  bio.txt
  bio_alt.txt
  bio_alt2.txt
  TIKTOK_META.json
  _create_orbit_tiktok.py
  audit/                  # screenshots from create run
```

## Soft CTA rule

TikTok is discovery only. Captions: “Watch the full story on Orbit with Ben” — never hard sell, never watermarked re-uploads.

## Create

```bash
/usr/bin/python3 00_Brand/Channel-Setup/TikTok/_create_orbit_tiktok.py
```

Uses Google session from `/Users/ben/code/youtube/.playwright-youtube-profile` (`benoats86@gmail.com`).
