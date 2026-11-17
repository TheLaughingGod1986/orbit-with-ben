# WW2 Documentary Channel Kit — Ready for Ben (`J2999`)

Everything needed to create and dress the new WW2 documentary YouTube channel in **under 10 minutes**, with **`£0` extra spend**. Nothing has been created, signed in, or uploaded.

---

## 1. Ben's Setup Checklist (Step by Step)

- [ ] **1. Create as a Brand Account channel (not on your personal channel identity):**
  1. Signed into your studio Google account on desktop, open **`https://www.youtube.com/channel_switcher`**.
  2. Click **Create a channel**, enter your chosen channel name below, and confirm. Creating it from `channel_switcher` puts the channel on its own **Brand Account** so your personal profile, Orbit With Ben, and History of Science stay completely separate in YouTube's recommendation graph and Studio permissions.
- [ ] **2. Pick the name and `@handle` (all 3 verified FREE on YouTube on 17 Nov 2026):**
  - **Recommended:** **`Field Order History`** · Handle: **`@FieldOrderHistory`**
  - **Alternative 1:** **`Gridline History`** · Handle: **`@GridlineHistory`**
  - **Alternative 2:** **`Iron & Compass`** · Handle: **`@IronAndCompass`**
- [ ] **3. Verify by phone (*Intermediate* + *Advanced* features) — Check the 2-per-year limit first:**
  1. In YouTube Studio, go to **Settings → Channel → Feature eligibility**.
  2. Enable **2. Intermediate features** (phone verification). **Why this is required before Pilot 1:** unverified channels cannot upload videos **over 15 minutes** (our pilots are **~25 minutes**) and cannot upload **custom thumbnails**.
  3. **Phone-number quota warning:** YouTube allows **one phone number to verify at most two channels per rolling 12-month year** (per verification method). If your primary number has already verified two channels in the last 12 months, use **Voice call** instead of SMS if offered, or use a second mobile number rather than burning retries.
  4. Start **3. Advanced features** right underneath (unlocks **Thumbnail Test & Compare**, clickable links, and higher daily limits — quick video selfie or existing Google account history, usually approved within 24 hours).
- [ ] **4. Upload the Profile Picture (`800×800`) and Banner (`2560×1440`):**
  1. Open **Customisation → Profile** (or *Branding* tab in YouTube Studio).
  2. Grab your chosen folder from **iCloud Drive → `WW2 UAT/00_Channel-Kit/<chosen_slug>/`** (already synced from the Mini) or on the NAS at **`/Volumes/data/studio-live/ww2/00_Brand/Channel-Kit/<chosen_slug>/`**:
     - **Picture (`800×800`, `< 4 MB`):** Upload `<slug>_profile_photo_800x800.png` *(archive-photo + compass bezel, matches our thumbnail style)* — or `<slug>_profile_drawn_800x800.png` if you prefer the clean drawn tactical monogram.
     - **Banner image (`2560×1440`, `< 6 MB`):** Upload `<slug>_banner_2560x1440.jpg` (or `.png` — both are under YouTube's 6 MB limit, with 100% of text and callouts inside the `1546×423` mobile/all-devices safe area).
- [ ] **5. Paste Channel Description, Keywords, About Links & Upload Defaults:**
  1. Under **Customisation → Basic info → Description**, paste the matching `channel_description_<slug>.txt` below (first line leads with high-volume search terms).
  2. Under **Links** and **Contact info**, follow Section 4 below (leave external links and contact address blank on Day 1 so nothing links back to your personal identity or other channels; add the 3 series playlists once created).
  3. Under **Settings → Channel → Basic info**, set **Country of residence: United Kingdom** and paste `channel_keywords.txt`.
  4. Under **Settings → Channel → Advanced settings**, select **No, set this channel as not 'Made for Kids'**.
  5. Under **Settings → Upload defaults**, set **Category: Education**, **Video language: English (United Kingdom)**, **Visibility: Private**, uncheck **Automatic chapters**, and paste `templates/default_upload_description.txt` (full guide in `UPLOAD_TEMPLATE.md`).
- [ ] **6. Tell the studio once the channel & `TheLaughingGod1986/ww2-channel` repo are ready:**
  - Tell us which of the 3 names/handles you picked (and once signed into Studio on the Mini's dedicated Chrome profile, we handle playlists, uploads, Test & Compare, and scheduling automatically).

---

## 2. Channel Art Ready to Upload (Recommended + Both Alternatives)

All art matches our WW2 packaging evidence (`studio/RULES.md` rule 2 + `J3005` 1,020-video study): **authentic public-domain wartime archive photography, bright/normal silver-warm tonal grade (`near-black < 15%`, never murky dark), `2–3` bold words in `#FFFFFF` + `#FFD600` signal yellow, and one `#FF3B30` tactical callout**.

- **Ready-to-upload files on iCloud Drive:** `WW2 UAT/00_Channel-Kit/<slug>/`
- **Master files & sources on NAS:** `/Volumes/data/studio-live/ww2/00_Brand/Channel-Kit/`
- **Safe-area & mobile-circle verification sheet:** `preview_sheet_safe_areas.jpg` (in both folders above)
- **Tracked vector emblems & reproducible builder in git:** `00_Brand/svg/*.svg`, `00_Brand/tools/build_channel_kit.py`, and `00_Brand/Channel-Kit/ART_MANIFEST.json`

| Option | Channel Name & Handle | Profile Picture (`800×800`, `< 4 MB`) | Banner (`2560×1440`, `< 6 MB`, Safe Area `1546×423`) | Verified Public-Domain Archive Source |
|---|---|---|---|---|
| **1 (Recommended)** | **Field Order History**<br>`@FieldOrderHistory` | `field_order_history_profile_photo_800x800.png` *(or `_drawn_`)* | `field_order_history_banner_2560x1440.jpg` *(and `.png`)*<br>Safe margins inside `1546×423`: L `47 px`, T `62 px`, R `131 px`, B `65 px` | **US Coast Guard / NARA `26-G-2517`** (`9 June 1944`, US Federal Public Domain) — Allied LSTs, barrage balloons & supply columns on Omaha Beach |
| **2 (Alternative 1)** | **Gridline History**<br>`@GridlineHistory` | `gridline_history_profile_photo_800x800.png` *(or `_drawn_`)* | `gridline_history_banner_2560x1440.jpg` *(and `.png`)*<br>Safe margins inside `1546×423`: L `47 px`, T `62 px`, R `134 px`, B `65 px` | **UK War Office / Imperial War Museums `BU 1024`** (`Sept 1944`, Crown Copyright Expired / Public Domain) — Aerial view of Mulberry B floating roadways at Arromanches |
| **3 (Alternative 2)** | **Iron & Compass**<br>`@IronAndCompass` | `iron_and_compass_profile_photo_800x800.png` *(or `_drawn_`)* | `iron_and_compass_banner_2560x1440.jpg` *(and `.png`)*<br>Safe margins inside `1546×423`: L `47 px`, T `62 px`, R `106 px`, B `65 px` | **US Navy / NHHC / NARA `80-G-266487`** (`13 May 1944`, US Federal Public Domain) — Destroyer escort `USS Ahrens (DE-575)` with `HF/DF` mast, photographed from `USS Bogue (CVE-9)` |

---

## 3. Channel Descriptions (Search-First Opening Line, Copy-Paste Ready)

YouTube displays the **first ~135 characters** in channel search results and directly beneath the `@handle` on mobile/desktop before *"…more"*. All three versions open with the niche's top search phrases (`World War 2 documentaries`, `military history`, `WW2`, `engineered`, `supplied`, `operations`).

### Option 1 (Recommended): `Field Order History` (`channel_description_field_order_history.txt` — `899` chars)

```text
World War 2 documentaries and military history — how WW2 was engineered, supplied, and fought across land, sea, and air.

Field Order History tells the real operational stories behind the Second World War: the machines, convoys, harbours, aircraft, radar, and battlefield logistics that decided campaigns long before the headlines were written.

Every documentary is built from verified wartime photography (US National Archives, Naval History and Heritage Command, Library of Congress, and UK Imperial War Museums), custom operational maps drawn from campaign records, and primary-source war diaries and technical reports.

What we cover:
• Engineering & weapons programmes — from floating D-Day harbours to the B-29 Superfortress
• Naval & air campaigns — Atlantic U-boat hunts, carrier logistics, and strategic bombing
• Supply lines, intelligence & deception — how fuel, tonnage, radar, and codebreaking won battles

New long-form WW2 documentaries every Tuesday and Saturday at 17:00 London (12:00 ET).
```

### Option 2: `Gridline History` (`channel_description_gridline_history.txt` — `805` chars)

See `00_Brand/Channel-Kit/channel_description_gridline_history.txt`.

### Option 3: `Iron & Compass` (`channel_description_iron_and_compass.txt` — `622` chars)

See `00_Brand/Channel-Kit/channel_description_iron_and_compass.txt`.

### Channel Keywords (*Settings → Channel → Basic info → Keywords*, `channel_keywords.txt`)

```text
"world war 2", "ww2 documentary", "military history", "war documentary", "second world war", "ww2 history", "ww2 engineering", "ww2 logistics", "naval history", "aviation history", "battle of the atlantic", "d-day history", "pacific war"
```

---

## 4. About Links & Contact Info (*Customisation → Basic info*)

Keep this channel **100% isolated** from Orbit With Ben, History of Science, and personal accounts so YouTube's recommendation graph treats it purely as a military/WW2 documentary channel:

1. **Before the first upload (Day 0 setup):**
   - Leave **Links** empty (do not add placeholder URLs or links to other studio channels).
   - Leave **Contact info** blank until/unless you want a dedicated business-enquiries inbox solely for this channel.
2. **As soon as the core series playlists exist (Pilot 1–3 launch week, `PLAYBOOK.md` §4):**
   Add these Links in YouTube Studio (*Customisation → Basic info → Links*, max 5):

   | Order | Link Title (`≤ 30` chars) | URL |
   |---|---|---|
   | 1 | `Subscribe` | `https://www.youtube.com/@FieldOrderHistory?sub_confirmation=1` *(swap handle if Option 2 or 3)* |
   | 2 | `Engineering That Won the War` | *(Paste YouTube playlist URL once created with Pilot 1 `WW2:001` & Pilot 3 `WW2:003`)* |
   | 3 | `The Supply War` | *(Paste YouTube playlist URL once created with Pilot 2 `WW2:002`)* |
   | 4 | `Deception & Intelligence` | *(Paste YouTube playlist URL once first deception film `WW2:008` is added)* |

---

## 5. Default Upload Template & Altered-Content Rule

Full copy-paste skeleton, worked Pilot 1 example, tag rules, and Studio defaults live in:
- **`00_Brand/Channel-Kit/UPLOAD_TEMPLATE.md`**
- **`00_Brand/Channel-Kit/templates/default_upload_description.txt`**
- **`00_Brand/Channel-Kit/templates/upload_defaults.json`**
