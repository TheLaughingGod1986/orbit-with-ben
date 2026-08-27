# Episode template — Growth System v2 + AI Studio picture economy

Copy this folder to start a new long:

```bash
cp -R 02_Video-Projects/_template_NNN_Episode-Slug \
  02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star
# Locked next long (7–9 min). Do not use empty 007_Neutron-Star scaffold. Do not start 013 Moon.
```

## Order (blocking)

1. Fill `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` and sign off  
2. Write `01_Script/*_script_master_v01.md` with cold open + markers (Orbit in 1–2 inquisitive beats only)  
3. Gate:
   ```bash
   cd 07_Content-Ops
   npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>
   ```
4. **PASS only then:**
   - VO → ElevenLabs Ben Orbit Narrator → `02_Voiceover/`
   - CG → **Google AI Studio**: stills first (open world · two science · Orbit ref) → **2–3 Veo Fast** money shots → **Omni only** if Orbit must move. Mute Veo audio. See `OMNI_LONGFORM_PLAYBOOK.md`.
5. Edit on Mac → Shorts (4–8, 22–27s, picture thumb no Orbit) → checklist → YouTube package  
6. After YouTube lock: long thumbs = picture + SEA hook (no Orbit) · Short thumbs = picture no Orbit · social mirror  

## Engines

| Job | Tool |
|-----|------|
| WORLD CG | AI Studio **Veo** (Fast; one Quality hero if it earns the thumb) |
| Orbit motion | AI Studio **Omni only** (1–2 scenes) |
| VO | ElevenLabs TTS only |
| Gate | `npm run gate:episode` |
| Brief | `npm run brief:next -- --file metrics.json` |

Do **not** Omni the whole film. No Kling / ElevenLabs Image & Video / Seedance for new CG.

Docs: `YOUTUBE_GROWTH_SYSTEM_V2.md` · `OMNI_LONGFORM_PLAYBOOK.md` · `docs/GEMINI_VEO_CG.md`
