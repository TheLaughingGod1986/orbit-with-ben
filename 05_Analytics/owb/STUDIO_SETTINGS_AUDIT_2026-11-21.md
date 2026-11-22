# Studio settings audit — Orbit With Ben — 2026-11-21

Audited 2026-11-21 20:04–20:12 UTC (`J3255`, Gemini worker, superseding the read-only pass on PR #1099) and updated 2026-11-22 00:05 UTC (`J3335`, Gemini acting Chief, implementing Ben's 21 Nov 2026 settings decisions) in the signed-in Orbit With Ben YouTube Studio browser (CDP port 9223) and read back via the channel's YouTube Data API login (`YOUTUBE_REFRESH_TOKEN`). Channel `UC_esArsDKd3GJvOkeO0DUog`, `@OrbitWithBen`. £0. No live video's visibility, schedule, title, description, thumbnail, existing published dub track, or active A/B test was modified. Monetisation was not applied.

## For Ben

- **Country** is already United Kingdom (`GB`). Left unchanged.
- **Automatic dubbing** — **Channel policy (Ben, 21 Nov 2026: off on every channel; revisit after monetisation).** Turned **off** on Orbit With Ben (`J3335`, 22 Nov 00:05 UTC; saved, hard-reloaded, and verified off). Existing dub tracks already on published videos were left untouched. Matches History of Science and Field Order History (both read back off).
- **Third-party AI training** — **Channel policy (Ben, 21 Nov 2026: off on every channel).** Turned **off** on Orbit With Ben (`J3335`, 22 Nov 00:05 UTC; saved, hard-reloaded, and verified off). Matches History of Science and Field Order History (both read back off).
- **Google Ads account linking**: a *"Promotions account link"* (`648-474-5368`, permissions: All, status: **Linked**) is attached under `Settings > Channel > Advanced settings`. Left untouched (verified still Linked after `J3335`; no ad spend or unlinking without Ben).
- **Video watermark** is not set (`Upload`). Recommendation: upload a 150×150 subscribe watermark once art is ready (unlike History of Science, Orbit's playbook does not forbid a branding watermark).

## Safe Reversible Fixes Applied & Verified (21–22 Nov 2026)

1. **`Upload defaults > Basic info > Visibility`** (`J3255`): changed **`Unlisted` → `Private`**, saved, reloaded Studio, and verified **`Private`**. Prevents accidental link-accessible manual uploads and aligns with the upload-private-then-schedule rule.
2. **`Upload defaults > Advanced settings > Title and description language`** (`J3255`): changed **`English` → `English (United Kingdom)`**, saved, reloaded Studio, and verified **`English (United Kingdom)`** (matching Video language `English (United Kingdom)`).
3. **Series playlist `PLdoEpeiktw_Y`** (`J3255`, *Real Worlds: Solar System, Moons and Alien Planets Explained*): added newest public long `c5AdqQsnnys` (*How Far Is the Nearest Star? (You Can't See It, and It Has a Planet)*, pos 11; verified `count=12` on YouTube Data API read-back) without touching the video's visibility, schedule, or running A/B title test.
4. **`Channel > Advanced settings > Automatic dubbing`** (`J3335`, 22 Nov 00:05 UTC, Ben's 21 Nov 2026 decision): unchecked **`Allow automatic dubbing`** (`On` → **`Off`** for future uploads), saved, hard-reloaded Studio, and verified **`aria-checked="false"`** (Made for Kids still No, Google Ads link `648-474-5368` untouched, existing published dub tracks untouched).
5. **`Channel > Advanced settings > Third-party training`** (`J3335`, 22 Nov 00:05 UTC, Ben's 21 Nov 2026 decision): unchecked **`Allow third-party companies to train AI models using my channel content`** (`On` / All third-party companies → **`Off`**), saved, hard-reloaded Studio, and verified **`aria-checked="false"`**.

## Channel

| Setting | Current | Recommended | Why | Changed |
|---|---|---|---|---|
| Country | United Kingdom (`GB`) | Keep United Kingdom | Target audience is Anglosphere adults. Country changes stay with Ben. | no |
| Keywords | 16 terms, 234/500: `Orbit With Ben`, `space`, `astronomy`, `universe`, `astrophysics`, `black holes`, `exoplanets`, `James Webb Space Telescope`, `JWST`, `alien life`, `cosmology`, `space science`, `space discoveries`, `science documentary`, `science explained`, `space documentary` | Keep | Matches channel focus and stays well under the 500-character limit. | no |
| Default language (channel API) | `en` (`snippet.defaultLanguage` & `brandingSettings.channel.defaultLanguage`) | Keep `en` (or `en-GB` on next channel update) | English set at channel level; upload defaults now both `English (United Kingdom)`. | no |
| Handle | `@OrbitWithBen` | Keep | Matches channel identity. | no |
| Description | Set (Space stories and cosmic mysteries with Orbit; Pixar-warm storytelling with documentary bones). | Keep | Complete and clear. | no |
| Links | 3 social links: `IG` (`instagram.com/orbitwithben/`), `FB` (`facebook.com/people/Orbit-with-Ben/61592833318203/`), `Threads` (`threads.com/@orbitwithben`). None use `/go/`. | Keep | Matches active social channels; retired `/go/` affiliate links stay off. | no |
| Contact email (business) | A business email is saved (not copied here) | Keep | Present on `Customisation > Profile`. | no |
| Profile picture & banner | Both set (`Change` / `Remove`) | Keep | Present on `Customisation > Profile` (Studio spec: banner ≥2048×1152 ≤6 MB; picture ≥98×98 ≤4 MB). | no |
| Video watermark | Not set (`Upload`) | Add a 150×150 subscribe watermark when graphic is ready | Optional growth setting for Orbit; Ben's call / art needed. | no |
| Made for kids | No, set this channel as not Made for Kids | Keep | Channel rule and every video checked. | no |
| Automatic captions filter | *"Don't show potentially inappropriate words"* off | Keep off | Keeps science/astronomy auto captions accurate and unredacted. | no |
| Automatic dubbing | **Off** (was On; turned off 22 Nov 00:05 UTC, `J3335`; existing published dub tracks untouched) | **Keep Off** (Ben, 21 Nov 2026: off on every channel; revisit after monetisation) | January plan targets English-speaking adults, dubbed views earn less, and unreviewed dubs are a quality risk. Verified after hard reload; matches HOS & FOH. | yes |
| Interest-based ads | Not disabled (`Disable interest-based ads` unchecked) | Keep | Preserves personalised ad monetisation once eligible. | no |
| Clips / remixing (channel) | *"Allow viewers to clip my content"*: **On** | Keep on | Aids organic sharing. Per-video Shorts remixing is set to *"Allow video and audio remixing"*. | no |
| Video quality enhancements | Visual enhancement **On**; Audio enhancement **On** | Keep | Applies to future uploads only. | no |
| Third-party AI training | **Off** (was On — All third-party companies; turned off 22 Nov 00:05 UTC, `J3335`) | **Keep Off** (Ben, 21 Nov 2026: off on every channel) | One policy across OWB, HOS & FOH; no growth effect. Verified after hard reload. | yes |
| Google Ads linking | Linked (`Promotions account link`, `648-474-5368`, All permissions) | Ben's call | Paid-promotion link; untouched. | no |
| Feature eligibility | Standard: **Enabled** · Intermediate: **Enabled** (>15 min videos, custom thumbnails, live streaming) · Advanced: **Enabled** (higher daily upload/live caps, external links, pinned comments, monetisation eligibility) | Keep | All three tiers enabled. | no |
| Monetisation (`Earn`) | Not eligible (data as of 16 Nov 2026): **18** subscribers (500 / 1,000), **3** uploads in last 90 days (3/3), **7** qualified watch hours in last 365 days (3,000 / 4,000), **6.3k** qualified Shorts views in last 90 days (3m / 10m). | Do not apply | Below thresholds; Apply not clicked. | no |
| Home layout — trailer | Set for non-subscribers: *JWST Found Galaxies That Shouldn't Exist Yet* (`ziKBPJ6FY0U`) | Keep (or rotate to top-retaining long such as *What Happened to Venus?* on Chief call) | Real public long set for non-subscribers. | no |
| Home layout — featured video (returning) | No separate returning-subscriber featured video section configured | Optional: add a featured video for returning viewers when next tentpole airs | Returning viewers currently see the playlist and *For you* shelves first. | no |
| Home layout — sections | Trailer → Single playlist (`What Would Happen If…`, 11) → For you → Videos (17) → Short videos (92) → Past live streams (5) → Created playlists (4) → Posts (1) → Collaborations (0) → Single playlist (`Real Worlds`, 11) | Keep; consider moving `Real Worlds` above `Past live streams` on next layout pass | Both editorial playlists are already featured on Home. | no |
| Playlists | Two public cluster playlists (cleaned up in J2460): `PLdoEpeiktw_Y` (*Real Worlds: Solar System, Moons and Alien Planets Explained*, now **12** videos after adding `c5AdqQsnnys`) and `PLOw2VKzGCOWU` (*What Would Happen If…: Black Holes, Neutron Stars and Extreme Space*, 11 videos), both with descriptions. | Keep both public and ensure every new long is added on upload | Added missing 15 Nov long `c5AdqQsnnys` to `PLdoEpeiktw_Y` (verified count 12 via API). | yes |
| Community & comments | Comments on new content: **On**, Moderation: **Basic**. Live chat moderation: **Basic**. Viewer posts: **On** (Subscribers ≥1 day, Moderation: Basic). Blocked words: empty. Hold comments with hashtags and URLs: **Off**. Channel guidelines: set. | Keep | Balanced moderation for growth without over-filtering comments. | no |
| Subtitles (channel) | Auto English captions active; manual `en-GB` `.srt` uploaded on most recent Shorts and longs (`cap=true` on 5 of 7 checked). | Keep uploading `en-GB` `.srt` with every package | `93JL_IK57EM` (Short) and `Js6EQJ8qDi8` (Mars long) currently have `cap=false` (auto captions only). | no |
| Currency | `GBP – British Pound` | Keep | Display preference only. | no |

## Upload defaults

Updated in Studio (`Settings > Upload defaults`), saved, reloaded, and verified. API upload packages (`youtube:package`) also set privacy, category, language, and altered-content metadata per upload.

| Setting | Current | Recommended | Why | Changed |
|---|---|---|---|---|
| Visibility | **Private** (was `Unlisted`) | Keep **Private** | Changed `Unlisted` → `Private` so manual uploads never bypass scheduling or subscriber notifications. Verified after reload. | yes |
| Category | **Science and technology** (ID `28`) | Keep **Science and technology** (`28`) | Matches OWB's uploader contract (`07_Content-Ops/scripts/channel-youtube.ts`: `categoryId: "28"`) and all live OWB videos. Note: J3255's prompt mentioned Education, so kept `28` to avoid diverging from the uploader without Chief sign-off. | no |
| Licence | Standard YouTube licence | Keep | Standard rights protection. | no |
| Comments | On, Moderation: Basic | Keep On / Basic | Encourages engagement while holding obvious spam. | no |
| Publish to subscriptions feed & notify subscribers | Not a separate switch in Upload defaults dialog; controlled per video / `publishAt` | Keep On at scheduled publish | Packages schedule via `publishAt` on Private uploads, triggering subscriber notification when public. | no |
| Embedding allowed | Not a separate switch in Upload defaults dialog; **True** on all 7 checked public videos | Keep On | Supports external shares and social embeds. | no |
| Title template | Empty | Keep empty | Titles are authored per film. | no |
| Description template | Short channel pitch (*"Big questions. Deep universe. 🚀 ... Subscribe to Orbit With Ben..."*) | Keep or replace with empty/minimal template on Chief call | API packages overwrite description with full per-film chapters, Sources line, image credits, and honest how-it's-made line. Left untouched so manual uploads still have channel copy. | no |
| Tags | 20 channel tags (282/500) | Keep | Per-film tags replace these on API uploads; sensible fallback for manual uploads. | no |
| Video language | English (United Kingdom) | Keep English (United Kingdom) | Matches Ben's British narration. | no |
| Caption certification | None | Keep None (or *"never aired on US TV"*) | Not US broadcast television. | no |
| Title and description language | **English (United Kingdom)** (was `English`) | Keep **English (United Kingdom)** | Changed `English` → `English (United Kingdom)` to match Video language. Verified after reload. | yes |
| Automatic chapters | **On** (*Allow automatic chapters and key moments*) | Keep On | Longs carry explicit `0:00` chapters in descriptions; automatic chapters act as fallback. | no |
| Automatic concepts / places | Per-video setting (*Help viewers explore key places/concepts*); not in Upload defaults dialog | Keep default | Visible on per-video edit pages. | no |
| Audience — Made for kids / Age restriction | Channel default: **Not Made for Kids**; Age restriction **Off** on all checked videos | Keep | Required by channel rules. | no |
| Altered / synthetic content disclosure | Per-video setting (not in Upload defaults dialog); **Yes** verified on all 7 checked public videos | Keep **Yes** on every upload | Matches OWB disclosure rule (`STUDIO_PLAYBOOK.md` & `studio/RULES.md`). | no |
| Show likes count | **On** | Keep On | Social proof for growth. | no |

## Spot-check: last 5 public videos (+ 2 newest public longs)

Read-only check via Studio (`/edit`, `/translations`) and YouTube Data API on 21 Nov 2026. All 7 videos are Public, `categoryId=28` (Science & Technology), `embeddable=True`, `license=youtube`, `selfDeclaredMadeForKids=False`, altered/synthetic content = **Yes**, Shorts remixing = **Allow video and audio remixing**.

| Type & Date | Video ID & Title | Description first line | Chapters | Playlist | Captions (`API cap`) | End screen / Cards / Test & Compare |
|---|---|---|---|---|---|---|
| Short · 21 Nov | `2YiV_zDgLJg` — *Muons Shouldn't Reach the Ground. They Do.* | `What Happens If You Travel Near Light Speed?` | N/A (Short) | None (Shorts stay out of long playlists) | `en-GB` (`cap=true`) | Related video set; End screen/Cards/Test & Compare N/A on Shorts |
| Short · 20 Nov | `93JL_IK57EM` — *Will Asteroid 2024 YR4 Hit the Moon in 2032?* | `Will Asteroid 2024 YR4 Hit the Moon in 2032?` | N/A (Short) | None | Auto only (`cap=false`) | Related video set; no manual `en-GB` track uploaded |
| Short · 19 Nov | `HXacmpYkXcA` — *How Close Will the Supermoon Get on November 24?* | `On November 24, 2026 at 14:54 UTC, the first of three consecutive full Supermoons reaches...` | N/A (Short) | None | `en-GB` (`cap=true`) | Related video set |
| Short · 18 Nov | `dH_yCRmzkMo` — *If Voyager Needs 75,000 Years, How Far Is the Nearest Star?* | `How Far Is the Nearest Star?` | N/A (Short) | None | `en-GB` (`cap=true`) | Related video set |
| Short · 17 Nov | `9q_OvQ1Rd8Y` — *How Far From Earth Is Voyager 1 Right Now?* | `Voyager 1 Is About to Be One Light-Day Away` | N/A (Short) | None | `en-GB` (`cap=true`) | Related video set |
| Long · 15 Nov | `c5AdqQsnnys` — *How Far Is the Nearest Star? (You Can't See It, and It Has a Planet)* | `How far is the nearest star? Proxima Centauri, a small red dwarf 4.24 light-years away...` | Explicit `0:00` chapters | **Added to `PLdoEpeiktw_Y` (pos 11)** | `en-GB` (`cap=true`) | End screen & Cards present on edit page; **A/B title test Running…** (2 arms; untouched) |
| Long · 8 Nov | `Js6EQJ8qDi8` — *Could a Robot Survive on Mars? (One Lasted 14 Years)* | `Could a robot survive on Mars? NASA's Opportunity rover was built to last ninety days...` | Explicit `0:00` chapters | In 2 playlists (`PLdoEpeiktw_Y`, `PLOw2VKzGCOWU`) | Auto only (`cap=false`; video lang `en-US`, title lang `en`) | End screen & Cards present on edit page; **A/B title test Running…** (3 arms; untouched) |
