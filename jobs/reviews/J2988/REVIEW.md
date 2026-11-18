# J2988 Condition Verification Review — J2984 (`HOS 008 Short C v07: non-producer QA review of J2662 (PR #556) and HOS UAT staging for Ben's watch`)

- **Verification Job:** `J2988` (`Verify condition for J2984`)
- **Parent Job:** `J2984` (`HOS 008 Short C v07: non-producer QA review of J2662 (PR #556) and HOS UAT staging for Ben's watch`, `status: blocked`, `by: gemini`, `needs: mini`, `repo: hos`, `film: 008`, `stage: edit`, `kind: qa`)
- **Verifier:** `gemini` (`Gemini 4 Argon (High)`, specialist worker on the Mac mini via fallback chain on `--kind review`)
- **Checked At:** `2026-11-17T17:44Z`
- **Verdict:** **CONDITION NOT MET — KEEP `J2984` BLOCKED (`gemini` / `macbook` assembled `v07` in `J2662` and `J2984` brief forbids self-review; all non-producer QA reviewers are currently down/unavailable on the Mini: `claude` out of usage until `2026-11-17T17:50:00Z` and not woken on Mini NAS jobs, `claudecode` hit Fable usage limit at `2026-11-17T17:23:53Z` resetting `10am Europe/London` / `2026-11-18T10:00:00Z` with relay retry at `2026-11-17T18:29:37Z`, `codex` down until `2026-11-17T23:22:00Z`, and `cursor-claude-opus-5-5` out of credit until `2026-12-09T00:00:00Z` with `cursor` weekly limit reached; all HOS PR `#556` and NAS `v07`/`v03` deliverables verified intact; `£0.00` / `0` credits).**

---

## 1. Recorded Waiting Condition on `J2984`

At `2026-11-17T14:38Z`, `J2984`'s `hold` (`type: "credits"`, `check_at: "2026-11-17T16:36:39+00:00"`, `recheck_task: "J2988"`) stated:

```text
Non-producer QA reviewer required (gemini/macbook assembled v07 in J2662 and brief forbids self-review): claudecode down until 2026-11-17T15:31:13Z, claude down until 2026-11-17T17:50:00Z, codex down until 2026-11-17T23:22:00Z, cursor-claude-opus-5-5 out of credit. Pre-flight verified NAS SHA-256 (v07 a3404a314a44..., v03 9f25a16de5fc...) and HOS PR #556 @ 168f8915 green.
```

---

## 2. Element-by-Element Verification on the Mac mini (`2026-11-17T17:44Z`)

| Requirement / Lane | Status | Direct Evidence Checked |
|---|---|---|
| **1. Non-producer exclusion rule (`J2984` brief)** | **ACTIVE** | - `J2984` brief explicitly requires: *"Producers to exclude from self-review: `macbook` / `gemini` assembled `v07` (`cursor` minted the Flow Veo plates). Route to `claude`, `cursor` on `claude-opus-5-5`, or `codex` first; if `gemini` is woken while non-producers are down, wait rather than self-reviewing."*<br>- Note: `J2984` currently retains `"for": "gemini", "model": "gemini-argon"` from its `2026-11-17T12:07Z` relay reroute; when a non-producer QA reviewer is available, `J2984` must also be handed back / rerouted to that non-producer (`claudecode`, `codex`, or `claude`). |
| **2. `claude` (`claude-opus-5-5`, primary `--kind qa`)** | **NOT MET (down until `2026-11-17T17:50:00Z`; cloud lane cannot stage local NAS file to iCloud `HOS UAT`)** | - `~/_desk/state/chief/claude_beat.json` (`fetched: 2026-11-17T17:36:43Z`): `out: true`, `until: "2026-11-17T17:50:00Z"`, `reason: "four runs a day to save usage (Ben, 11 Nov)"`.<br>- In addition, `J2984` is `needs: "mini"` because Step 3 copies `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_C_v07.mp4` to the Mini's `HOS UAT` watch folder (`~/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/`). |
| **3. `cursor` on `cursor-claude-opus-5-5` (fallback 1 on `--kind qa`)** | **NOT MET (out of credit + weekly limit)** | - `chief_relay.py status`: `cursor-claude-opus-5-5` flagged out of credit until `2026-12-09T00:00:00Z` (`"Claude Opus 5.5 is not included in your weekly usage. Buy credits or switch to a Grok model to continue."`).<br>- `~/_desk/state/chief/down/cursor.json`: `since: "2026-11-17T17:33:17Z"`, `until: "2026-11-17T18:33:17Z"`, `reason: "ActionRequiredError: Weekly usage limit reached. It resets in 2 days. Buy credits to keep going now."` |
| **4. `codex` on `gpt-6-astra` (fallback 3 on `--kind qa`)** | **NOT MET (down until `2026-11-17T23:22:00Z`)** | - `~/_desk/state/chief/down/codex.json`: `since: "2026-11-14T20:18:19Z"`, `until: "2026-11-17T23:22:00Z"`, `reason: "Codex hit usage limit until 2026-11-17T23:22:00Z (verified in J2829 probe)"`. |
| **5. `claudecode` on `mini-claude-opus-5-5` (fallback 4 on `--kind qa`)** | **NOT MET (hit Fable limit at `17:23:53Z`; resets `10am Europe/London` / `2026-11-18T10:00:00Z`, relay retry `2026-11-17T18:29:37Z`)** | - `~/_desk/state/chief/runs.jsonl`: `claudecode` ran on `J2986` at `2026-11-17T17:23:53Z` (`exit: 1`, `out_of_usage: true`).<br>- `~/_desk/state/chief/down/claudecode.json`: `since: "2026-11-17T17:29:37Z"`, `until: "2026-11-17T18:29:37Z"`, `reason: "out of usage, credit or signed out (its last run ended: \"You've hit your Fable limit · resets 10am (Europe/London). Switch to another model, or manage usage credits at https://claude.ai/settings/usage?from=cc_cli_limi\")"`. |
| **6. HOS PR `#556` & NAS `J2662` deliverables** | **VERIFIED INTACT & GREEN** | - `TheLaughingGod1986/history-of-science#556` (`macbook/J2662`, head `168f8915371c0799308d3ee3fa33f731a60b3421`): `state: OPEN`, all 6 CI checks `SUCCESS` (`no-desk-close`, `no-media`, `check`, `tests`, `atempo`).<br>- NAS master `10_Shorts/hos_008_short_C_v07.mp4`: SHA-256 `a3404a314a444a0fd987ca648c28425be8afb768f83748ee64e553951c8f06a8` (matches brief).<br>- NAS prior `10_Shorts/hos_008_short_C_v03.mp4`: SHA-256 `9f25a16de5fc7d454be7adbc0e301614c7b060cd28b10cd076bcd2b4a6642161` (untouched).<br>- NAS stems (`vo.wav` `50d65ab8...`, `bed.wav` `62a8c103...`, `sfx.wav` `ecd5b8b9...`, `05_Music/hos_008_short_C_v07_bed.wav` `cf4143ab...`) and 3 QA contact sheets (`hos_008_short_C_v07_open_sheet.jpg` `2cf9944b...`, `picture_qa_review_v07.jpg` `90135e64...`, `v07_1fps_sheet.jpg` `0e7288f4...`) verified byte-for-byte. |

---

## 3. Verification Outcome (`J2988`)

The waiting condition on `J2984` remains **NOT MET**:
- Keep `J2984` held (`type: input`, `--recheck J2988`, next check at `2026-11-17T18:35:00Z` after the `claudecode` `18:29:37Z` / `claude` `17:50:00Z` retry windows, or `2026-11-17T23:25:00Z` after `codex`'s `23:22:00Z` reset).
- Because `jobs.py wait J2984 --recheck J2988` and closing `J2988` require elected Chief authority (`chief_relay.elected_for("gemini", ...)` is `False` while Grok Bot `chief` is `UP`), park `J2988` at step `3/3` for the elected Chief to record `wait --recheck J2988` on `J2984` and mark `J2988` done.
