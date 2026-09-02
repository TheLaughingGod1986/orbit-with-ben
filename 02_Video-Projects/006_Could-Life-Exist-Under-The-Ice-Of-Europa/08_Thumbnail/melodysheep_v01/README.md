# Long thumbs — MelodySheep v01

Steal from MelodySheep: cinematic 16:9 plate, huge ALL-CAPS title + smaller subtitle, no mascot.
House: yellow kicker / white rest, no Orbit, no generic CTA, no rounded pill.

| Film | Live id | Premiere | Applied | Hook |
|------|---------|----------|---------|------|
| Europa | `NbW5G1BpPY0` | Thu 3 Sep 18:00 | **A** | LIFE UNDER / THE ICE · MORE WATER THAN EARTH |
| Neutron | `Yk1tLh23rko` | Thu 10 Sep 18:00 | **A** | A TEASPOON / OF MOUNTAINS · NEAR A NEUTRON STAR |

**B** variants are on disk for Studio Test & Compare. Do not remint Last Star.
Do not change premiere dates while saving thumbs.

Rebuild:

```bash
uv run --with pillow python 00_Brand/Channel-Setup/tools/build_melodysheep_long_thumbs_v01.py
uv run --with playwright python scripts/apply_melodysheep_long_thumbs_v01.py
```
