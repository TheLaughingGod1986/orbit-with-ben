# Studio settings audit — History of Science — 2026-11-21

Audited 2026-11-21 20:04–20:12 UTC (`J3255`, Gemini worker, superseding the read-only pass on PR #1099) and followed up 2026-11-21 21:14–21:23 UTC (`J3325`, Gemini acting Chief) in the signed-in History of Science YouTube Studio browser (CDP port 9460) and read back via the channel's read-only YouTube Data API login (`YT_ANALYTICS_REFRESH_TOKEN_HOS`). Channel `UCXp7HkBIl1LgaznXuZHJyRg`, `@HistoryOfScienceYT`. £0. No live video's visibility, schedule, title, description, thumbnail, or active A/B test was modified. Monetisation was not applied.

## For Ben

- **Country** is already United Kingdom (`GB`). Left unchanged.
- **Automatic dubbing** is **off** (Studio shows `Enable`). Adds non-English views and watch hours, though dubbed views earn less. Orbit With Ben is **on**; Field Order History is **off**. Pick one policy; left off.
- **Third-party AI training** (*"Allow third-party companies to train AI models using my channel content"*) is **off** (matches Field Order History; Orbit With Ben is **on**). Rights switch; left off.
- **Contact email (business)** is **empty** on `Customisation > Profile`. Add a business enquiry email if you want one shown on the About page (not invented here).

## Safe Reversible Fixes Applied & Verified (21 Nov 2026)

1. **`Channel > Basic info > Keywords`** (`J3255`): populated from **empty → 15 canonical terms (194/500)** matching `00_Brand/Channel-Setup/channel_keywords.txt` (`history of science`, `science`, `discovery`, `documentary`, `cartoon science`, `explained`, `curiosity`, `physics`, `astronomy`, `experiments`, `scientific method`, `inventors`, `universe`, `big questions`, `History of Science`), saved, reloaded Studio, and verified both in Studio (`194/500`) and on YouTube Data API read-back.
2. **`Upload defaults > Advanced settings > Title and description language`** (`J3255`): changed **Unset (`Select`) → `English (United Kingdom)`**, saved, reloaded Studio, and verified **`English (United Kingdom)`** (matching `studio/RULES.md` and `STUDIO_PLAYBOOK.md` line 386).
3. **`Customisation > Home tab > Channel trailer (non-subscribers)`** (`J3325`, 21:17 UTC): added channel trailer section and set **`AL_-qlWko_g`** (*How Did We Discover the Periodic Table?*, HOS's highest-viewed public long at 162 views) for people who haven't subscribed, published, reloaded Studio, and verified both in Studio and via YouTube Data API (`brandingSettings.channel.unsubscribedTrailer = "AL_-qlWko_g"`).
4. **Series playlist `PLEbpfUzWzcXU`** (`J3325`, 21:22 UTC): added missing 12 Nov public long **`ETynHpIYLeY`** (*How Was the First Vaccine Made? (And Why It's Named After a Cow)*) strictly via the Playlists manager (`Content > Playlists > PLEbpfUzWzcXU > Videos` → `Edit in YouTube`, never opening `ETynHpIYLeY`'s `/edit` page) and positioned it in film order at **pos 6**, immediately after `VbPubYd6Fbs` (pos 5) and before the scheduled compilation `uAomPaOBrM8` (pos 7; 8 items total). Verified after Studio Playlists reload (`1–8 of many`, `A/B test running` badge intact on `ETynHpIYLeY`) and via YouTube Data API (`playlistItems` positions 0–7 confirmed; `ETynHpIYLeY` `snippet`/`status`/`contentDetails` and `etag` byte-identical to pre-change baseline).

## Channel

| Setting | Current | Recommended | Why | Changed |
|---|---|---|---|---|
| Country | United Kingdom (`GB`) | Keep United Kingdom | Target audience is Anglosphere adults. Country changes stay with Ben. | no |
| Keywords | **15 terms, 194/500** (was empty): `history of science`, `science`, `discovery`, `documentary`, `cartoon science`, `explained`, `curiosity`, `physics`, `astronomy`, `experiments`, `scientific method`, `inventors`, `universe`, `big questions`, `History of Science` | Keep | Populated from canonical `00_Brand/Channel-Setup/channel_keywords.txt`. Verified after Studio reload and via YouTube Data API. | yes |
| Default language (channel API) | `null` (`snippet.defaultLanguage` & `brandingSettings.channel.defaultLanguage` unset; HOS API token in OWB `.env` is read-only) | Set channel defaultLanguage to `en-GB` on next HOS write-token session | Upload defaults now set both Video language and Title & description language to `English (United Kingdom)`. | no |
| Handle | `@HistoryOfScienceYT` | Keep | Matches channel identity (never `@HistoryOfScience`). | no |
| Description | Set (3D cartoon films about how we discovered what we know; includes honest AI-picture / human-voice disclosure line). | Keep | Clear, aligned with HOS rules. | no |
| Links | 3 links set on `Customisation > Profile`: `Instagram` (`instagram.com/historyofscienceyt/`), `Threads` (`threads.com/@historyofscienceyt`), `Orbit with Ben` (`youtube.com/@OrbitWithBen`). None use `/go/`. | Keep (note: HOS Threads posting is paused, link is harmless) | Cross-links cleanly without retired `/go/` links. | no |
| Contact email (business) | **Empty** | Add a business email (Ben's call) | Blank on `Customisation > Profile`; not invented. | no |
| Profile picture & banner | Both set (`Change` / `Remove`) | Keep | Present on `Customisation > Profile` (Studio spec: banner ≥2048×1152 ≤6 MB; picture ≥98×98 ≤4 MB). | no |
| Video watermark | Not set (`Upload`) | **Keep unset** | Explicit HOS rule (`STUDIO_PLAYBOOK.md` line 387: *"No branding watermark (no subscribe graphics)."*). Corrects PR #1099's suggestion. | no |
| Made for kids | No, set this channel as not Made for Kids | Keep | Hard HOS Never-list rule. | no |
| Automatic captions filter | *"Don't show potentially inappropriate words"* off | Keep off | Keeps scientific/historical auto captions accurate. | no |
| Automatic dubbing | **Off** (`Enable` button shown) | Ben's call | Watch hours versus lower-earning dubbed views. Differs from Orbit (on). | no |
| Interest-based ads | Not disabled (`Disable interest-based ads` unchecked) | Keep | Preserves personalised ad monetisation once eligible. | no |
| Clips / remixing (channel) | *"Allow viewers to clip my content"*: **On** | Keep on | Aids organic sharing. Per-video Shorts remixing is set to *"Allow video and audio remixing"*. | no |
| Video quality enhancements | Visual enhancement **On**; Audio enhancement **On** | Keep | Applies to future uploads only. | no |
| Third-party AI training | **Off** | Ben's call (keep off unless Ben aligns across channels) | Rights switch; matches Field Order History (Orbit is on). | no |
| Google Ads linking | Not linked | Keep | No ad spend without Ben. | no |
| Feature eligibility | Standard: **Enabled** · Intermediate: **Enabled** (>15 min videos, custom thumbnails, live streaming) · Advanced: **Enabled** (higher daily upload/live caps, external links, pinned comments, monetisation eligibility) | Keep | All three tiers enabled. | no |
| Monetisation (`Earn`) | Not eligible (data as of 16 Nov 2026): **6** subscribers (500 / 1,000), **3** uploads in last 90 days (3/3), **4** qualified watch hours in last 365 days (3,000 / 4,000), **1.2k** qualified Shorts views in last 90 days (3m / 10m). | Do not apply | Below thresholds; Apply not clicked. | no |
| Home layout — trailer & returning featured | **Non-subscriber trailer set to `AL_-qlWko_g`** (*How Did We Discover the Periodic Table?*, was unset); returning featured unset | Keep `AL_-qlWko_g` as non-subscriber trailer | Set and published on `Customisation > Home tab` (`J3325`); verified after Studio reload and via YouTube Data API (`unsubscribedTrailer=AL_-qlWko_g`). | yes |
| Home layout — sections | Channel trailer (`AL_-qlWko_g`) → For you → Videos (7) → Short videos (35) → Past live streams (3) → Created playlists (3) → Posts (0) → Collaborations (0) | Keep trailer; optional future Featured Playlist shelf for `PLEbpfUzWzcXU` | Channel trailer now leads the Home tab for non-subscribers (`J3325`). | yes |
| Playlists | One public series playlist: `PLEbpfUzWzcXU` (*How Did We Discover…? Atoms, the Periodic Table, Germs and X-Rays \| History of Science*, **8 items** [was 7], manual sort, description set). Order: `AL_-qlWko_g` (0), `GHZDsiH7L7A` (1), `frP_YrNShsU` (2), `_C92tIJCk8A` (3), `wwcjcFfC-5M` (4), `VbPubYd6Fbs` (5), **`ETynHpIYLeY` (6)**, `uAomPaOBrM8` (7). | Keep in film order | Added missing 12 Nov public long `ETynHpIYLeY` before `uAomPaOBrM8` strictly via Playlists manager (`J3325`, never opening `/edit`); verified via Studio reload (`A/B test running` intact) and YouTube Data API. | yes |
| Community & comments | Comments on new content: **On**, Moderation: **Basic**. Live chat moderation: **None**. Viewer posts: **Off**. Blocked words: empty. Hold comments with hashtags and URLs: **Off**. Channel guidelines: empty. | Keep comments On / Basic | Matches `STUDIO_PLAYBOOK.md` line 386. | no |
| Subtitles (channel) | Auto English captions active; manual `en-GB` `.srt` uploaded on all 7 checked public videos (`cap=true` on 7/7). | Keep uploading `en-GB` `.srt` per `STUDIO_PLAYBOOK.md` line 393 | 100% coverage on recent public videos. | no |
| Currency | `GBP – British Pound` | Keep | Display preference only. | no |

## Upload defaults

Updated in Studio (`Settings > Upload defaults`), saved, reloaded, and verified. The HOS uploader also enforces Education, English (UK), altered content Yes, and not Made for Kids on every API upload.

| Setting | Current | Recommended | Why | Changed |
|---|---|---|---|---|
| Visibility | **Private** | Keep **Private** | Matches `STUDIO_PLAYBOOK.md` line 386 (upload private, schedule after approval). | no |
| Category | **Education** (ID `27`) | Keep **Education** (`27`) | Matches HOS contract and uploader. | no |
| Licence | Standard YouTube licence | Keep | Matches `STUDIO_PLAYBOOK.md` line 386. | no |
| Comments | On, Moderation: Basic | Keep On / Basic | Matches `STUDIO_PLAYBOOK.md` line 386. | no |
| Publish to subscriptions feed & notify subscribers | Not a separate switch in Upload defaults dialog; controlled per video / `publishAt` | Keep On at scheduled publish | Packages schedule via `publishAt` on Private uploads. | no |
| Embedding allowed | Not a separate switch in Upload defaults dialog; **True** on all 7 checked public videos | Keep On | Matches `STUDIO_PLAYBOOK.md` line 386. | no |
| Title template | Empty | Keep empty | Titles are authored per film. | no |
| Description template | Empty | Keep empty | API upload packages populate full chapters, sources, archive credits, and honest how-it's-made line without colliding with a default template. | no |
| Tags | Empty | Keep empty | Tags are set per film by the upload package. | no |
| Video language | English (United Kingdom) | Keep English (United Kingdom) | Matches HOS rule (`English (UK)`). | no |
| Caption certification | *"This content has never aired on television in the US"* | Keep | Accurate for original YouTube content. | no |
| Title and description language | **English (United Kingdom)** (was Unset / `Select`) | Keep **English (United Kingdom)** | Changed Unset → `English (United Kingdom)` to match Video language and HOS rule. Verified after reload. | yes |
| Automatic chapters | **On** (*Allow automatic chapters and key moments*) | Keep On | Longs carry explicit `0:00` story-beat chapters; automatic chapters act as fallback. | no |
| Automatic concepts / places | Per-video setting; not in Upload defaults dialog | Keep default | Visible on per-video edit pages. | no |
| Audience — Made for kids / Age restriction | Channel default: **Not Made for Kids**; Age restriction **Off** on all checked videos | Keep | Hard HOS Never-list rule. | no |
| Altered / synthetic content disclosure | Per-video setting (not in Upload defaults dialog); **Yes** verified on all 7 checked public videos | Keep **Yes** on every upload | Matches HOS disclosure rule (`studio/RULES.md`). | no |
| Show likes count | **On** | Keep On | Matches `STUDIO_PLAYBOOK.md` line 386. | no |

## Spot-check: last 5 public videos (+ 2 newest public longs)

Read-only check via Studio (`/edit`, `/translations`) and YouTube Data API on 21 Nov 2026. All 7 videos are Public, `categoryId=27` (Education), `defaultLanguage=en-GB`, `defaultAudioLanguage=en-GB`, `embeddable=True`, `license=youtube`, `selfDeclaredMadeForKids=False`, `cap=true`, altered/synthetic content = **Yes**, Shorts remixing = **Allow video and audio remixing**.

| Type & Date | Video ID & Title | Description first line | Chapters | Playlist | Captions (`API cap`) | End screen / Cards / Test & Compare |
|---|---|---|---|---|---|---|
| Short · 21 Nov | `Bks_JLId1ew` — *How Do Plants Make Oxygen?* | `The Willow Tree That Was Made of Air` | N/A (Short) | None (Shorts stay out of long playlist) | `en-GB` (`cap=true`) | Related video set; End screen/Cards/Test & Compare N/A on Shorts |
| Short · 20 Nov | `l8bxm9L3zl8` — *How Does a Blood Pressure Cuff Work?* | `A blood pressure cuff squeezes your arm until the blood stops getting in, then lets go...` | N/A (Short) | None | `en-GB` (`cap=true`) | Related video set |
| Short · 18 Nov | `ChbsigHD5_o` — *How Do Plants Clean the Air?* | `The Willow Tree That Was Made of Air` | N/A (Short) | None | `en-GB` (`cap=true`) | Related video set |
| Short · 17 Nov | `xgx2lYHhYZM` — *Why Is It Called a Vaccine?* | `Why Vaccines Are Named After a Cow` | N/A (Short) | None | `en-GB` (`cap=true`) | Related video set |
| Short · 16 Nov | `xzKoHg0E0_U` — *What Is Dalton's Atomic Theory?* | `What's Really Inside an Atom?` | N/A (Short) | None | `en-GB` (`cap=true`) | Related video set |
| Long · 12 Nov | `ETynHpIYLeY` — *How Was the First Vaccine Made? (And Why It's Named After a Cow)* | `How was the first vaccine made? Every vaccine is named after a cow — here is how...` | Explicit `0:00` chapters | **In `PLEbpfUzWzcXU` (pos 6)** — added via Playlists manager (`J3325`) before `uAomPaOBrM8` (pos 7) | `en-GB` (`cap=true`) | End screen & Cards present on edit page; **A/B title test Running…** (2 arms; untouched — verified intact in Studio & API byte-identical after `J3325`) |
| Long · 5 Nov | `VbPubYd6Fbs` — *The Willow Tree That Was Made of Air* | `A fully grown tree is built almost entirely out of thin air. So where does a tree's weight...` | Explicit `0:00` chapters | In `PLEbpfUzWzcXU` (pos 5) | `en-GB` (`cap=true`) | End screen & Cards present on edit page; **A/B title test Results ready** (untouched) |
