# Episode template

Copy this folder to start a new film:

```bash
cp -R 02_Video-Projects/_template_NNN_Episode-Slug 02_Video-Projects/<NNN_Slug>
```

Then follow `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` in order. It stops for Ben's OK at each step.

1. **Topic:** data pick + competition check. Fill `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`. Ben picks.
2. **Script:** `01_Script/<slug>_script_master_v01.md`, 8–9 min, with `[VISUAL MUST]` / `[TEACH]` on every scene and `[ORBIT ACTS]` on 1–2 beats. Run:
   ```bash
   cd 07_Content-Ops
   npm run review:script -- --file ../02_Video-Projects/<NNN_Slug>/01_Script/<script>.md   # ≥90
   npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>                     # PASS
   ```
3. **Voice:** ElevenLabs Ben Orbit Narrator (`04_Audio/tools/orbit_voice.py`) → `02_Voiceover/`.
4. **Picture:** Google AI Studio. Veo for the world, Omni only when Orbit moves. Stills first, then 2–3 Veo Fast money shots, muted → `04_Generated-Clips/` → edit in `07_Edit-Project/` → export `09_Final-Export/`.
5. **Shorts:** three a week, 22–27 s, following the first-two-seconds rules → `10_Shorts/`. Every export must pass `gate_shorts_open.py`.
6. **Thumbnails:** `08_Thumbnail/`, per `THUMBNAIL_AND_TITLE_RULES.md`, checked with `thumb_preview.py`.
7. **Upload:** `11_Upload-Package/` → `npm run youtube:package`, then Studio finish. Tick `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`.
