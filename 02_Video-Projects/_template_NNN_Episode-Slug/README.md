# Episode template — Growth System v2 + Gemini Veo

Copy this folder to start a new long:

```bash
cp -R 02_Video-Projects/_template_NNN_Episode-Slug \
  02_Video-Projects/007_Neutron-Star
# Locked next long is 007 Neutron Star. Do not start 013 Moon.
```

## Order (blocking)

1. Fill `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` and sign off  
2. Write `01_Script/*_script_master_v01.md` with cold open + markers  
3. Gate:
   ```bash
   cd 07_Content-Ops
   npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>
   ```
4. **PASS only then:**
   - VO → ElevenLabs Ben Orbit Narrator → `02_Voiceover/`
   - CG → Gemini Veo:
     ```bash
     export GEMINI_API_KEY=...
     cd 07_Edit-Project
     cp .env.example .env   # paste key
     python3 _generate_veo_from_beats.py --beats beats.json --out-dir ../04_Generated-Clips/01_Raw
     ```
5. Edit → Shorts (3–5) → checklist → YouTube package upload  
6. After YouTube lock: thumb ABC + social mirror schedule  

## Engines

| Job | Tool |
|-----|------|
| CG | Gemini Veo (`orbit_gemini_veo.py`) |
| VO | ElevenLabs TTS only |
| Gate | `npm run gate:episode` |
| Brief | `npm run brief:next -- --file metrics.json` |

Docs: `YOUTUBE_GROWTH_SYSTEM_V2.md` · `docs/GEMINI_VEO_CG.md`
