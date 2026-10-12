# HANDOVER — master index (all of Ben's repos)

Written 12 Oct 2026 ~15:00 London by Chief of Staff (Grok Bot). Ben's ask: any other LLM (Claude, Codex, Cursor, Gemini…) must be able to pick up **all** work from the GitHub repos alone. Start here.

## Repos
| Repo | What | Read first | Visibility |
|---|---|---|---|
| [orbit-with-ben](https://github.com/TheLaughingGod1986/orbit-with-ben) | Orbit With Ben YouTube studio (+ shared Mini tooling: jobs, relay, routing, analytics for both channels) | `AGENTS.md`, this file | public |
| [history-of-science](https://github.com/TheLaughingGod1986/history-of-science) | History of Science YouTube studio | `AGENTS.md`, `HANDOVER.md` | public |
| [oppti-website-auditor](https://github.com/TheLaughingGod1986/oppti-website-auditor) | OpptiAI Website Auditor (free SEO audit plugin, gateway to the others), v1 plan in `docs/` | `HANDOVER.md` | private |
| [WP-Alt-text-plugin](https://github.com/TheLaughingGod1986/WP-Alt-text-plugin) | OpptiAI Alt Text (WP.org `beepbeep-ai-alt-text-generator`) | `AGENTS.md`, `HANDOVER.md` | public |
| [beepbeep-titles](https://github.com/TheLaughingGod1986/beepbeep-titles) | OpptiAI Titles (WP.org `opptiai-titles`) | `HANDOVER.md` | public |
| [oppti-backend](https://github.com/TheLaughingGod1986/oppti-backend) | Shared backend (Render; Supabase `femyykcbrleehnyapxbu`, Stripe, Loops, PostHog) | `AGENTS.md`, `HANDOVER.md` | public |

Other repos exist (e.g. oppti-internal-linking, Channel Scout); they follow the same rules.

## Studio standing rules added 9–12 Oct 2026 (already in AGENTS.md unless marked NEW)
- **Who decides:** Chief of Staff (Grok Bot) owns reviews, PASS, merges, final OKs, `AGENTS.md` and the Never list. Ben gets only real money (past £0), irreversible actions, his own voice/logins/devices, and channel-direction changes. Updates to Ben are results only and say plainly when nothing is needed.
- **Credit floors are zero (Ben, 12 Oct 2026 14:46) — NEW, supersedes the "Credit holds until 30 Oct" ElevenLabs gating:** use all subscription credit down to 0 — ElevenLabs (~11,935 credits left on 12 Oct, resets 30 Oct), Google Flow (52 credits on AI Ultra), Vertex free trial (£4.93; stop at the £0.10 billing-lag margin because billing account is a Paid account). **Never** buy credits, top up, upgrade, enable overage or let anything spill onto the card. HOS PR #287 records this in HOS.
- **Mini runs 24/7 (Ben, 12 Oct):** never idles; reviews done the moment they land; no fixed start times (jobs start when inputs are ready, `--after`); when work runs out the queue refills (`scripts/refill.py`, `jobs/backlog.json`) with: new video ideas, weekly per-channel audits with competitor analysis, and polish on finished films. **The aim is to improve the numbers every month.**
- **Model routing + fallback chain:** `AGENTS.md` → "Who does what" and `scripts/routing.py` (`CHAINS`). Claude jobs: Claude Code → Cursor on `claude-opus-5-5` → Gemini `agy` → Codex `gpt-6-astra`. Chief chain: Grok Bot → Cursor → Codex (`scripts/chief_relay.py`).
- **Four a month per channel** (`scripts/channel_balance.py`), one focus film at a time, Ben's watch before upload with a watch-by date.
- **Buffer is the only social route;** posts scheduled at the YouTube go-public time only; TikTok paused; no pinned comment on Shorts.
- **Takedowns = make private, never delete** (Chief's call, Ben told). Never delete anything on either Mac or the NAS; never reset or stash.
- **Uploads:** `PUBLISHING_DRY_RUN=false` only on the one real upload command line; never replace an armed Test & Compare.
- **Git:** never force-push; new PRs; merge when green or none required. Never merge/close the thread PRs (OWB #99, HOS #180).

## Pending decisions (open with Ben, 12 Oct 2026)
1. **Long film + standalone Shorts (asked 14:46):** Ben asked about an hour-long film a month and standalone ~20 s story Shorts. Chief's recommendation: a standalone Shorts test (2 per week per channel for 4 weeks) plus one 45–60 min compilation to test the long format. **No decision yet** — direction change, so it waits for Ben.
2. **Make the public repos private?** Unanswered. Don't change visibility unasked.
3. **Key rotation:** pending.
4. From the 9 Oct handover: use a long's own opening as one of its Shorts; HOS fewer feed-style / more search-titled Shorts (Test B partly covers it); handing the HOS write lane back from Cursor (HOS #234).

## Where current state lives (read these, not chat)
- OWB: `python3 scripts/studio.py board`, `STATUS.md`, `JOBS.md` / `jobs/queue.json`, each film's `status.json`, thread PR #99 (`scripts/owb_thread.py read`).
- HOS: `STATUS.md`, desk thread HOS #180, `AGENTS.md` → "The desk".
- 9 Oct handover snapshot (now historical, board wins): `docs/handover/STUDIO_HANDOVER_2026-10-09.md` in orbit-with-ben.
- Open PRs 12 Oct: OWB #143 (024 SOURCES rows + relay plist env), #139 (024 J0143 covers), #107, #105 (drafts). HOS #286, #285, #284, #274, #272, #271, #270.

## OpptiAI (plugins) — summary
Full rules, release state and the Auditor param compatibility are in each Oppti repo's `HANDOVER.md`. Short version: Alt Text next 4.6.141, Titles next 1.0.29 (both carry Auditor hooks; accept `source=auditor&finding=` and `auditor_source=`); Auditor v1 in progress, Ben reviews on his MacBook before WP.org; October target 10 new regulars.

## What does NOT live in any repo (gaps a new agent must know)
- **Logins and sessions on the Mac mini:** Chrome/CDP browsers (Orbit Studio on port 9223; HOS/Flow on 9222, signed into Ben's personal channel), YouTube Studio, Google Flow (AI Ultra), Buffer, ElevenLabs, Vertex/Google Cloud console, WordPress.org (beepbeepv2), PostHog, Stripe, Supabase, Vercel, Render. CLI auths on the mini: `gh`, Cursor `agent`, `codex`, Antigravity `agy`, Claude Code. A new agent needs Ben to sign in or hand these over; they cannot be recreated from git.
- **Secrets (names only, never values):** `07_Content-Ops/.env` on the mini (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`, `YT_ANALYTICS_REFRESH_TOKEN_OWB`/`_HOS`, `BUFFER_API_KEY`, `BLOB_READ_WRITE_TOKEN`, `ELEVENLABS_API_KEY`, `PUBLISHING_DRY_RUN=true`); Vercel project env (`orbit-content-ops`, Channel Scout incl. Google Ads refresh token); Render env for `oppti-backend` (Supabase service key, Stripe keys, Loops key, PostHog key); WordPress.org SVN password; Gmail account benoats@googlemail.com. Key rotation is still pending with Ben.
- **Mini launchd jobs** (defined in-repo under `launchd/`, but only running on the mini): `com.owb.chief-relay` (every 10 min, 24/7), analytics snapshot 06:40, Buffer mirror check 07:05, `studio.py stale` every 15 min, refill/escalate in the relay. J0053 (point launchd at the repo's `chief_relay.py`) may still be open — check `launchctl list | grep owb` on the mini.
- **Routines that run on Grok Bot's server (Chief of Staff), not in git:** Oppti Desk group room (Growth, Marketing, Analysis, QA, Plugin Dev agents and their prompts); Marketing daily social pass (weekdays, "Always go"); OpptiAI new-signup watch + chase/reply emails (Supabase `licenses` watermark, chase log); Mac mini health check; studio review pass on PR #99 / HOS #180. A replacement agent has to recreate these as its own scheduled tasks (cron/launchd or its platform's scheduler) from the descriptions here.
- **Grok Bot box files** (`/workspace` on the Grok Bot box, not reachable by others): `/workspace/oppti-briefs/` (patches, release zips, briefs — the Auditor ones are copied into `oppti-website-auditor/docs/`), `/workspace/oppti-signups/chase-log.md` + `watermark.json` (customer emails; deliberately not committed to public repos), `/workspace/oppti-growth-plan/GROWTH_PLAN_2026-10.md`.
- **Chief memory:** Ben's preferences are now written into these HANDOVER files; anything not here was not decided.

## How to resume (any agent)
1. Read this file, then the repo's `AGENTS.md` (docs-in-force order, Never list).
2. Studio: `python3 scripts/studio.py board` and `python3 scripts/jobs.py next --agent <you> --can <yours> --git`. Read PR #99 / HOS #180 for decisions only.
3. Oppti: read `oppti-website-auditor/HANDOVER.md`, then `gh pr list` in the four Oppti repos.
4. Recreate the server-side routines listed above as your own scheduled tasks; ask Ben for the logins you need. A stand-in never makes a protected call (merge/PASS/final OK/AGENTS.md) unless Ben names it the new Chief.
5. Keep this file current: when a standing rule changes, update `AGENTS.md` and this file in the same PR.
