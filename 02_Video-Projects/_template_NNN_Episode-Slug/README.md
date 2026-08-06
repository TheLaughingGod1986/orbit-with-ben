# Episode template — Growth System v2 + Google Flow Veo (Ultra)

Copy this folder to start a new long:

```bash
cp -R 02_Video-Projects/_template_NNN_Episode-Slug \
  02_Video-Projects/013_Moon-Leaving-Us
# then rename NNN + slug to match
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
   - CG → Google Flow Veo UI (Ultra):
     ```bash
     # One-time: python3 04_Audio/tools/orbit_flow_veo_ui.py --login
     cd 07_Edit-Project
     python3 _generate_veo_from_beats.py --beats beats.json --out-dir ../04_Generated-Clips/01_Raw
     ```
5. Edit → Shorts (3–5) → checklist → YouTube package upload  
6. After YouTube lock: thumb ABC + social mirror schedule  

## Engines

| Job | Tool |
|-----|------|
| CG | Google Flow Veo UI / Ultra (`orbit_flow_veo_ui.py`) |
| CG secondary | AI Studio UI (`--engine aistudio`) |
| CG last resort | Gemini API (`orbit_gemini_veo.py` — `--engine api`) |
| VO | ElevenLabs TTS only |
| Gate | `npm run gate:episode` |
| Brief | `npm run brief:next -- --file metrics.json` |
