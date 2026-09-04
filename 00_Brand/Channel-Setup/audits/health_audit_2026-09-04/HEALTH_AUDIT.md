# Channel health audit — 2026-09-04

Live Studio CDP + anonymous playability. Channel `UC_esArsDKd3GJvOkeO0DUog` (Orbit with Ben).

## Verdict

**Mostly healthy.** Mystery punches are uploaded and correctly scheduled. Last Star keepers are Public. One schedule collision was found and fixed during this audit. Related links on the three new mystery punches still do not persist (open Studio bug / processing race).

| Area | Status |
|------|--------|
| Mystery punches 15–17 Sep 11:30 UK | PASS — Scheduled |
| Last Star keepers (view-bearing) | PASS — Public + anon playable |
| Protected leftover schedule | FIXED this audit — now 18 Sep 11:30 (was colliding on 13 Sep) |
| Related → Neutron long on mystery punches | FAIL / open — Select+Save reverts to None |
| Debug private draft | WARN — 0-view leftover still Private (safe to delete) |
| Neutron long Premiere | PASS — Premiere set (~6 days out) |
| TikTok | N/A — paused |

## Mystery punches (PASS schedules)

| ID | Title | Schedule | Related |
|----|-------|----------|---------|
| `3QrICn9Kp00` | Why Does Light Leave Exhausted? | **15 Sept 2026 11:30** | **None** (open) |
| `mAAMsbhm88w` | Could a Probe Get Closer Than You? | **16 Sept 2026 11:30** | **None** (open) |
| `BX-z1EkgANg` | What Happens One Second After Contact? | **17 Sept 2026 11:30** | **None** (open) |

Anon status correctly `LOGIN_REQUIRED` / Private until publishAt.

Existing Neutron Shorts (e.g. `fhJP6eMoU0Q`, `o7ykyTDZKiE`) **do** keep Related → Neutron long, so the Related feature works on this channel — only these three new IDs refuse to stick after Save+reload.

## Last Star keepers (PASS)

All Public in Studio; anonymous `playabilityStatus=OK`:

- `xRxhb3vSru4` — What Remains After the Last Star Dies?
- `SdNXS1PD_Yk` / `CkSECfUfH2Y` — The Sky Is Already Running Out of Light (duplicate public copies)
- `IVbO9XkkDps` / `KX-XU_AODoI` — The Day the Last Star Goes Out (duplicate public copies)

Mobile “Private” padlocks from earlier were stale / mid-edit — not current state.

## Bug found + fixed: 13 Sep double-book

Before this audit:

- `o7ykyTDZKiE` (*Your Last Clear Image Near a Neutron Star*) → **13 Sept 11:30**
- `0j_pgYbCe5E` (*Why the Solar System Is Bigger Than You Were Taught*) → **also 13 Sept 11:30**

Two Shorts on the same slot. Docs claimed leftover was already on 18 Sep; live Studio still had 13 Sep.

**Fixed:** `0j_pgYbCe5E` moved to **18 Sept 2026 11:30**. Related still Last Star film. Verified after Save+reload.

## Still open

1. **Related on mystery punches** — automation picks Neutron long and Saves; reload shows None. Retry manually in Studio after Checks fully settle, or leave until closer to air (other Neutron Shorts already funnel the Premiere).
2. **Debug draft** `GMoB0CPfdZQ` — Private, 0 views, filename title. Safe to delete in Studio (automation delete did not complete).
3. **Duplicate Sky/Day public IDs** — hygiene only; both copies Public. Do not Private the high-view ones.
4. **Repo continuity** — mystery LIVE artifacts live on branch `cursor/neutron-mystery-shorts-15-17-24c1` (PR #48). Working tree had moved to 013 Moon branch; stash preserved Moon WIP.

## Not bugs

- Scheduled mystery Shorts appearing Private anonymously before air time.
- Neutron long `LIVE_STREAM_OFFLINE` / “Premieres in N days”.
- Europa Private staging Shorts with 0 views.
- Studio “Scheduled” filter returning empty while edit pages show Scheduled (Studio UI quirk).
