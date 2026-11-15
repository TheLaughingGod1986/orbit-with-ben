# Chief Review & Ruling: J2891 (`HOS: learn from our data, add two new films to the backlog`)

- **Date:** 2026-11-15T23:35Z
- **Reviewer:** Gemini (`gemini`, elected acting Chief; `claude` out of usage until `2026-11-16T07:50:00Z`, `chief` marked down until `2026-11-16T02:20:07Z`, `codex` marked down until `2026-11-17T23:22:00Z`)
- **Job:** `J2891` (`backlog: hos-ideas`, `kind: script`, `repo: hos`)
- **Existing Chief ruling on studio thread:** `#6894682062` (`[Chief]` Grok Bot, `2026-11-15T12:59:32Z`): *"J2891 (HOS topics job): reassigned to Gemini (agy). It has web search and research is its lane in the routing table. Backup is Claude after its reset (17:50Z). Relay: please move J2891 to Gemini in the queue on your next pass. Topic picks still go to Ben as a shortlist with a recommendation. Nothing gets started from it."*
- **Verdict:** **REOPEN & REROUTE TO MINI GEMINI ARGON (`needs: "mini"`, `mini_only: true`, `for: "gemini"`, `model: "gemini-argon"`)** — executing Chief Grok Bot's posted ruling `#6894682062` per `AGENTS.md` ("One ruling per parked job", 10 Nov 2026).

---

## 1. Evidence Reviewed

1. **Worker block (`macbook`, `#6894356248` / `#6894374915`, `2026-11-15T12:33Z`):**
   - `macbook` claimed `J2891` twice because `J2891` was queued with `needs: "any"` and no `mini_only` guard.
   - The unattended MacBook slot lacks web/YouTube search (`WebSearch`, `WebFetch`, and `curl` refused), so the blocking neighbour pass (`studio/RULES.md`: `neighbours.py` gate PASS with `>=3` education videos with `1M+` views and `public_search.py` evidence) could not be run without inventing view counts.
   - Nothing was written, no branch or PR was opened, and £0 was spent.
2. **Existing Chief ruling (`#6894682062`, `2026-11-15T12:59:32Z`):**
   - Chief Grok Bot already ruled on `#99` (`#6894682062`) to reassign `J2891` to `gemini` (`agy`) in the queue, with topic proposals remaining unlocked candidates (nothing started in production).
   - Per `AGENTS.md` ("One ruling per parked job", 10 Nov 2026): *"If a Chief decision is already posted, it stands: record it on the job and queue what it asks for; do not rule again... Whoever rules also closes the job in the queue (`jobs.py done`, or reopens it), so the relay stops listing it as a duty."*
3. **Current HOS numbering and open topic PRs:**
   - On `main` in `history-of-science`: `02_Video-Projects/000`–`018`, `099`, `100` (Bird Magnetic Compass), `101` (Deep-Sea Hydrothermal Vents); `00_Brand/Channel-Setup/ideas/` holds `011`–`095`.
   - Open PRs in `history-of-science` / `orbit-with-ben`:
     - HOS PR `#572` / OWB PR `#881` (`J2748`, reviews `J2775`/`J2776`): `HOS:102` (Ozone Hole) and `HOS:103` (Why Is the Sky Blue?).
     - HOS PR `#581` / OWB PR `#916` (`J2809`, reviews `J2810`/`J2811`): `HOS:104` (Speed of Light) and `HOS:105` (Venus Flytrap / Carnivorous Plants).
     - HOS PR `#588` / OWB PR `#930` (`J2835`, reviews `J2836`/`J2837`): `HOS:106` (Where Do Eels Come From?) and `HOS:107` (Why Do Leaves Change Colour in Autumn?).
   - Therefore, the next free HOS film numbers for `J2891` are **`108` and `109`**.

---

## 2. Ruling & Required Follow-Up Recorded on `J2891`

1. **Reopen and reroute `J2891` in place to Mini Gemini Argon (`needs: "mini"`, `mini_only: true`, `for: "gemini"`, `model: "gemini-argon"`):**
   - Keeps `J2891` as the live `backlog: "hos-ideas"` job so `refill.py` does not spawn duplicate `hos-ideas` copies while `J2891` is completed.
   - Setting `needs: "mini"` and `mini_only: true` prevents the restricted MacBook Claude slot from claiming `J2891` a third time and routes it directly to the Mini where `public_search.py` and `neighbours.py` run cleanly.
2. **Deliverables required from the Mini `gemini` worker to close `J2891`:**
   - **Data pass:** Read `05_Analytics/hos/channel_daily.json`, `05_Analytics/hos/studio_ctr.json`, `05_Analytics/hos/REPORT.md`, `05_Analytics/hos/snapshots/2026-11-15.json`, and `05_Analytics/LEARNINGS.md` (rules 1–31). Rank all eligible public HOS longs and Shorts consistently by views/day since publish, CTR, average % viewed, and Shorts stayed-to-watch, stating the snapshot timestamp and elapsed-day denominator, and write down the 3 best and 3 worst with exact numbers and shared patterns (treating low-view patterns as hypotheses).
   - **Two new non-overlapping backlog topics (`HOS:108` and `HOS:109`):**
     - Do not repeat any topic in `02_Video-Projects/` (`000`–`018`, `099`–`101`), open PRs `#572` (`102` Ozone Hole, `103` Blue Sky), `#581` (`104` Speed of Light, `105` Venus Flytrap), or `#588` (`106` Eels, `107` Autumn Leaves), `00_Brand/Channel-Setup/ideas/` (`011`–`095`), or `jobs/WIP.json` (`next_hos`).
     - In a clean worktree of `history-of-science`, create `02_Video-Projects/108_<Slug>/` and `02_Video-Projects/109_<Slug>/` from `02_Video-Projects/_template_NNN_Episode-Slug/` with `TOPIC.md`, `status.json` (all stages `todo`), `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`, `11_Upload-Package/evidence_<date>_public_search.json`, and `11_Upload-Package/evidence_<date>_neighbours.json` (`neighbours.py` PASS with `>=3` education videos `>=1M` views per topic; £0 spend).
     - Keep all historical/scientific claims explicitly marked unverified pending `SOURCES.md` and the `facts` lane before any future script lock.
     - Append `HOS:108` and `HOS:109` to `jobs/WIP.json` `next_hos` (Rule G waiting line only; nothing started in production) and queue their substantive `kind: review` Rule-E topic go/no-go jobs (`--after J2891`), then close `J2891` with `jobs.py done J2891` naming both topics, the data line behind each, and the review job IDs.
   - **Guards:** £0 / 0 credits spent; no script lock, VO, or picture generation; no Studio or publish change; nothing for Ben.
