# WW2 Documentary Channel (Prepared Template — Name Selected by Ben)

A third channel prepared in the studio's add-a-channel layout (`J2989`, 17 Nov 2026). **Nothing is created on YouTube, signed in, or added to `channels/channels.json` yet.** Ben chooses the public name from the three verified options below and creates the Brand Account channel himself.

## Three Verified Name & Handle Options (Checked Live on YouTube, 17 Nov 2026)

| Option | Channel Name | YouTube Handle | Live Check (`17 Nov 2026`) | Positioning |
|---|---|---|---|---|
| **1 (Placeholder in `channel.json`)** | **Field Order History** | `@FieldOrderHistory` | **FREE (`HTTP 404`, 0 channel collisions)** | Operational directives meeting weather, fuel, mud, and steel; authoritative British documentary tone; scales beyond WW2 later if desired. |
| **2** | **Gridline History** | `@GridlineHistory` | **FREE (`HTTP 404`, 0 military/history collisions)** | Named after War Office / Ordnance Survey operational map gridlines; highlights our code-drawn tactical & logistics maps alongside archive photography (`@TheWarAtlas` is taken). |
| **3** | **Iron & Compass** | `@IronAndCompass` | **FREE (`HTTP 404`, 0 military/history collisions)** | Classic maritime, air, and land documentary marque covering engineering, navigation, and strategy without copying `WW2 Dossier`, `WW2 Combat Files`, or `Military Studio`. |

## Folder Layout

| Path | What it holds |
|---|---|
| `studio/channel.json` | Channel settings (`slug: "ww2"`, `label: "WW2"`, `wip: 2`, `picture_route: "flow_only"`, `shorts.planned_per_long: 0`, `film_status`). Swap `name`, `short`, `youtube.handle`, and `title_match` in one commit if Ben picks Option 2 or 3. |
| `studio/RULES.md` | Channel rules on top of `AGENTS.md`: YouTube July 2025/2026 monetisation & authenticity policy, US/UK archive-photo provenance check per image, code-drawn map rules, fixed packaging style, voice budget guardrails, and Never additions. |
| `00_Brand/LAUNCH_PLAN.md` | Full launch & pilot plan: 3 name options, 10 sourced topics (`<=70` chars, `3+` `100k+` neighbours each, first 3 marked), packaging spec + 3 thumbnail briefs, 3-film pilot plan (`~25 min` each, voice character budget), and studio registration steps. |
| `00_Brand/VIDEO_BACKLOG.json` | Structured JSON backlog for films `001`–`010` (`WW2:001`–`WW2:010`). |
| `02_Video-Projects/001_...` – `010_...` | Ten prepared film folders with `status.json` (`stages: {}`, unlocked until Ben locks on `#plan`), plus `PILOT_PLAN.md` inside `001`, `002`, and `003`. |

## Studio Steps to Register This Third Channel (Listed Only — Not Done Yet)

Matching the board's **Channels → Add a channel** card (`05_Analytics/kanban/board_site/studio_app.js`) and `scripts/channel_new.py` (`scripts/channel_ratchet.json` is already at `0 + 0`):

1. **You (Ben):** Pick the channel name/handle above and lock your chosen pilot topics on the Studio board (`#plan`).
2. **Claude / Studio:** Channel folder (`channels/ww2/`), `studio/channel.json`, and `studio/RULES.md` are prepared from `channels/_template/` and pass `python3 scripts/channel_check.py channels/ww2` (`0` must-fix). *(Prepared in `J2989`.)*
3. **You (Ben):** Create the new YouTube **Brand Account** channel (not your personal channel), create its GitHub repo (`TheLaughingGod1986/<repo>`), sign in to its YouTube Studio on the Mac mini (assigning its dedicated CDP port, e.g. `9224`), and confirm `Ben Orbit Narrator` on the shared ElevenLabs account.
4. **Claude / Studio:** Initialise git in the channel folder, push to the new GitHub repo, fill `repo.url` (and `cadence`, e.g. `Tue 18:00` & `Sat 18:00`) in `studio/channel.json`, add `{"slug": "ww2", "env": "WW2_REPO", "checkouts": ["ww2"]}` to `channels/channels.json`, and run `python3 scripts/channels.py sync` + `python3 scripts/channel_check.py --all`.
5. **Claude / Studio:** Finalise `studio/RULES.md` with Ben's chosen name and publish schedule before queuing the first script (`WW2:001`).

Verify this folder at any time:

```bash
python3 scripts/channel_check.py channels/ww2
```
