# Production status — 007 Neutron Star

| Field | Value |
|-------|-------|
| Slug | `007_Neutron-Star` |
| Queue | **LOCKED NEXT** — not Moon, not Simulation |
| Script review | passed (do not rewrite if master script is present) |
| VO | pending (ElevenLabs Ben Orbit Narrator) |
| CG | pending (Omni Flash / Flow, 1-min parts) |
| Runtime target | ~18–25 min documentary |
| Shorts | 4–8 punch-first after master |
| Air after | Europa Thu 3 Sept 2026 |

## Live / scheduled (do not rebuild)

- Live: Fermi · Black Hole · Alien Worlds
- Thu 20 Aug: JWST — leave as-is
- Thu 27 Aug: Last Star — `REXYxuLOBoI` (letter **O**, not zero)
- Thu 3 Sept: Europa

## Build

Omni 1-minute path (PR 18). Copy passed script into `01_Script/` if this GitHub snapshot is missing it. Then:

```bash
cd 07_Content-Ops && npm run gate:episode -- --project ../02_Video-Projects/007_Neutron-Star
```

Stop when `09_Final-Export/` has the open-end broadcast master.

## Blockers on cloud clones

- [ ] Passed script on disk (not always in git)
- [ ] ElevenLabs + Flow Omni credentials
- [ ] Do not start 013 Moon while this is open
