# Studio settings audit — Field Order History — 2026-11-21

Updated 2026-11-21 19:43–19:56 UTC (J3320, Gemini acting Chief) after Ben confirmed the Field Order History Studio window (port 9224) was signed in to `UCu94mInMFosxu3W0H6jlI6Q` (`@FieldOrderHistory`), and read back 2026-11-22 00:04 UTC (`J3335`, Gemini acting Chief). Read and updated via the channel's YouTube Data API login (`YOUTUBE_REFRESH_TOKEN_WW2`) and the signed-in Studio window on port 9224. £0. Neither pilot's schedule, privacy, title, description, thumbnail or video file was changed. Monetisation was not applied.

## For Ben

- **Country** is already United Kingdom (`GB`). Left unchanged.
- **Automatic dubbing** — **Channel policy (Ben, 21 Nov 2026: off on every channel; revisit after monetisation).** Already **off** (shows `Enable`; read back off 22 Nov 00:04 UTC in `J3335`, unchanged). Matches Orbit With Ben (turned off in `J3335`) and History of Science (off).
- **Third-party AI training** — **Channel policy (Ben, 21 Nov 2026: off on every channel).** Already **off** (`aria-checked="false"`; read back off 22 Nov 00:04 UTC in `J3335`, unchanged). Matches Orbit With Ben (turned off in `J3335`) and History of Science (off).
- **Advanced features** (`Channel > Feature eligibility`) shows **Eligible** (Standard and Intermediate are already **Enabled**). Enabling Advanced features requires identity/video verification or channel history (unlocks higher daily upload caps, external links in descriptions, pinned comments, and monetisation eligibility). Identity verification stays with Ben; not urgent for tomorrow's launch.
- **Video watermark** is not set (`Upload`). Add a 150×150 subscribe watermark once the graphic is ready.

## Channel

Channel `UCu94mInMFosxu3W0H6jlI6Q`, `@FieldOrderHistory`. Created 18 Nov 2026.

| Setting | Current | Recommended | Why | Changed |
|---|---|---|---|---|
| Country | United Kingdom (`GB`) | Keep United Kingdom | Anglosphere adult audience. Country changes stay with Ben. | no |
| Keywords | 14 terms, 237/500: `Field Order History`, `World War 2`, `Second World War`, `WW2 documentary`, `military history`, `history documentary`, `WW2 logistics`, `military engineering`, `D-Day`, `Normandy`, `Mulberry harbours`, `Battle of the Atlantic`, `U-boats`, `WW2 operations` | Keep | Set via `channels.update` (`brandingSettings.channel.keywords`), read back via API and confirmed in Studio `Channel > Basic info`. | yes |
| Default language | English (United Kingdom) (`en-GB`) | Keep `en-GB` | Set via `channels.update` (`brandingSettings.channel.defaultLanguage`), read back on both `brandingSettings.channel.defaultLanguage` and `snippet.defaultLanguage`. | yes |
| Handle | `@FieldOrderHistory` | Keep | Matches channel identity. | no |
| Description | Set (World War 2 documentaries — how WW2 was engineered, supplied and fought; Tuesday & Saturday cadence). | Keep | Already live on channel profile. | no |
| Profile picture & banner | Both set (`Change` / `Remove`) | Keep | Present on `Customisation > Profile`. | no |
| Links | None | Add once channel has external destinations | No `/go/` or affiliate links. | no |
| Contact email | A business email is saved | Keep | Present on `Customisation > Profile` (address not copied here). | no |
| Video watermark | Not set (`Upload`) | Add a 150×150 subscribe watermark when art is ready | Growth setting; no image uploaded. | no |
| Made for kids | No, channel is set as not Made for Kids | Keep | Matches channel rules and both pilots. | no |
| Automatic captions filter | "Don't show potentially inappropriate words" off | Keep | Keeps auto captions readable (matches Orbit). | no |
| Automatic dubbing | Off (`Enable` button shown; read back off 22 Nov 00:04 UTC, `J3335`) | **Keep Off** (Ben, 21 Nov 2026: off on every channel; revisit after monetisation) | January plan targets English-speaking adults, dubbed views earn less, and unreviewed dubs are a quality risk. Matches OWB & HOS. | no |
| Interest-based ads | Not disabled | Keep | Do not turn off personalised ads. | no |
| Clips | Allow viewers to clip my content: On | Keep | Matches Orbit. | no |
| Video quality enhancements | Visual enhancement On; Audio enhancement On | Keep | Applies to future uploads only (matches Orbit). | no |
| Third-party AI training | Off (`aria-checked="false"`; read back off 22 Nov 00:04 UTC, `J3335`) | **Keep Off** (Ben, 21 Nov 2026: off on every channel) | One policy across OWB, HOS & FOH; no growth effect. | no |
| Google Ads linking | Not linked | Keep | No ad spend without Ben. | no |
| Feature eligibility | Standard: Enabled. Intermediate: Enabled (videos >15 min, custom thumbnails, live streaming). Advanced: Eligible (not yet verified). | Ben's call when ready for Advanced verification | Standard + Intermediate cover launch; Advanced verification stays with Ben. | no |
| Monetisation | Not eligible (data as of 16 Nov 2026: 0/1,000 subscribers, 0/4,000 qualified watch hours in last 365 days, 0/10m Shorts views in last 90 days). | Do not apply | Below thresholds; Apply not clicked. | no |
| Home tab & trailer | Default sections (For you, Videos, Short videos, Past live streams, Created playlists, Posts, Collaborations). No trailer yet. | Set Pilot 1 as non-subscriber trailer after it goes public Sun 22 Nov 17:00 London | No public videos yet. | no |
| Playlists | One Private series playlist `PLPPi-oWEDYtA` ("How WW2 Was Engineered, Supplied and Fought"), two-line description, `en-GB`, containing Pilot 1 (`ek9F61FVYqY`, pos 0) then Pilot 2 (`J9WGu8aPnHI`, pos 1). | Make `PLPPi-oWEDYtA` Public right after Pilot 1 goes live Sun 22 Nov 17:00 London | Prepared Private while both pilots are scheduled Private; Sunday first-day check flips it Public. | yes |
| Community moderation | Comments on new content: On, Moderation: Basic. Live chat moderation: None. Blocked words: empty. Hold comments with hashtags and URLs: Off. Redirects: subscribed channels only. | Keep | Matches Orbit (`On`, `Basic` moderation). | no |
| Currency | GBP – British Pound | Keep | Display only. | no |

## Upload defaults

Updated in Studio (`Settings > Upload defaults`), saved, and verified after reload.

| Setting | Current | Recommended | Why | Changed |
|---|---|---|---|---|
| Title template | Empty | Keep empty | Titles are written per film. | no |
| Description template | Empty | Keep empty | Upload packages supply full per-film chapters, sources, credits and how-made line. | no |
| Visibility | Private | Keep Private | Changed from unset (`Select`) to `Private` so manual uploads never publish accidentally. | yes |
| Tags | Empty | Keep empty | Tags are set per film. | no |
| Automatic chapters | On ("Allow automatic chapters and key moments") | Keep On | Long films carry explicit chapters in descriptions. | no |
| Licence | Standard YouTube licence | Keep | Standard licence. | no |
| Category | Education | Keep Education | Changed from `None` to `Education` (matches both pilots, category 27). | yes |
| Video language | English (United Kingdom) | Keep English (United Kingdom) | Changed from unset (`Select`) to `English (United Kingdom)`. | yes |
| Caption certification | None | Keep None | Not US broadcast television. | no |
| Title and description language | English (United Kingdom) | Keep English (United Kingdom) | Changed from unset (`Select`) to `English (United Kingdom)`. | yes |
| Comments | On, Moderation: Basic | Keep On / Basic | Matches Orbit. | no |
| Show likes count | On | Keep On | Matches Orbit. | no |

## Scheduled pilots

No public videos yet. Both scheduled pilots were inspected in Studio and via Data API; schedule, privacy, title, description, thumbnail and file were left untouched.

| Film | Video ID | State & schedule | Language / Category / Altered / Made for kids | Comments | End screen | Playlist |
|---|---|---|---|---|---|---|
| 001 Mulberry harbours | `ek9F61FVYqY` | Private, scheduled Sun 22 Nov 2026 17:00 UTC | `en-GB` (video + title/desc) / Education (27) / Altered content: Yes / Not Made for Kids / Age restriction: None / Embedding: On / Notify subscribers: On / Auto chapters, places & concepts: On / Remixing: Video & audio | On, Moderation: **Basic** (changed from None) | **Subscribe: Field Order History** + **Video: Best for viewer** (`27:16:18–27:36:18`, saved & verified after reload) | `PLPPi-oWEDYtA` (pos 0) |
| 002 Atlantic black pit | `J9WGu8aPnHI` | Private, scheduled Wed 25 Nov 2026 17:00 UTC | `en-GB` (video + title/desc) / Education (27) / Altered content: Yes / Not Made for Kids / Age restriction: None / Embedding: On / Notify subscribers: On / Auto chapters, places & concepts: On / Remixing: Video & audio | On, Moderation: **Basic** (changed from None) | **Subscribe: Field Order History** + **Video: Best for viewer** (`23:43:01–24:03:01`, saved & verified after reload) | `PLPPi-oWEDYtA` (pos 1) |

**End screen note (acting Chief call):** YouTube Studio refuses to save a Subscribe-only end screen (`"At least one element must be a video or playlist"`). Using `1 video (Best for viewer) + 1 subscribe` saves cleanly on both pilots without exposing any private video; once Pilot 2 goes public on Wed 25 Nov, `Best for viewer` automatically serves cross-recommendations between the two films without a second edit.
