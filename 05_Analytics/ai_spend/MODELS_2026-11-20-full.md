# Model ids — full CLI check, 20 Nov 2026 (J3237, Cursor)

Read on the Mac mini, 20 Nov 2026, about 16:20–16:35 GMT. £0. No image or video was generated. The morning Gemini note stays at `MODELS_2026-11-20.md` (J3218). This file is the full check the 15 Oct note was.

## What changed in routing

QA, listing and facts now start on Gemini 4 Neon (`gemini-argon` → `gemini-4-neon-high`). Script, review and chief stay on Claude. Charts and thumbnails stay on Codex Astra. Assembly stays on Cursor Grok 4.7, then Codex `gpt-6.1-sol`. Image and video model ids are unchanged. Studio still lists Grok Bot first; its first Mini lane is already Cursor on Grok 4.7, and Grok Bot is marked down until 17:33Z, so it was not taken out of the table.

`AGENTS.md` "Who does what" still prints Claude first on the QA and listing rows. That file is the Chief's. The model ids in those rows already include `gemini-argon`, so `test_routing.py` passes. Chief reorders the rows when this lands.

## Probes (subscription text only)

| Probe | Result |
|---|---|
| `agy --model gemini-4-carbon-high --sandbox -p "Reply with the single word OK"` | **PASS** `OK`, exit 0, about 15 s |
| Same model, four spoken lines on why the Moon stays in orbit, 120 s limit | **FAIL** exit 3, print timeout at 120 s, no usable lines |
| `agy --model gemini-4-neon-high`, the same four-line task | **PASS** exit 0. Four lines, 11, 11, 10 and 12 words. No title, no numbers |
| `agent -p --trust --model grok-4.7 "Reply with the single word OK"` | **PASS** `OK`, exit 0 |
| Same id, write a Python `rms` function only | **PASS** exit 0. `return (sum(x * x for x in samples) / len(samples)) ** 0.5` |
| `agent -p --trust --model claude-fable-5-2-high` one-word reply, run from `/tmp` | **REFUSED** "Claude Fable 5.2 is not included in your weekly usage. Buy credits or switch to a Grok model." Nothing was bought |
| `codex exec --sandbox read-only -m gpt-6.1-terra` one-word reply | **REFUSED** usage limit, try again at Nov 24th, 2026 11:26 PM. Mini clock is GMT, so the flag uses 23:26Z. Nothing was bought |
| Neon audio and moving-video | Not re-run. This morning's note records PASS on `gemini-4-neon-high` (audio 0.99–1.00, video exact, both directions) |

Carbon does not replace Neon for scripts. Neon finished the short script; Carbon did not finish inside two minutes.

## Codex (`codex` 0.160.0, `~/.codex/models_cache.json` fetched 2026-11-20T15:12:26Z)

There is **no `gpt-6.2-sol`** in this cache. The Neon card's comparison with "GPT-6.2 Sol" is not an installed Codex id.

| id | Display | Description in the cache | Priority | Visible |
|---|---|---|---|---|
| `gpt-6.1-terra` | GPT-6.1 Terra | Efficient model that excels at visual understanding and computer use. | 1 | list |
| `gpt-6.1-sol` | GPT-6.1-Sol | Previous generation model for coding and everyday work. | (after Terra) | list |
| `gpt-6-astra` | GPT-6-Astra | Previous generation model for complex coding and professional work. | | list |
| `gpt-6-sol` | GPT-6-Sol | Legacy model for coding and everyday work. | | list |
| `gpt-6-luna` | GPT-6-Luna | Fast and affordable model for easier tasks. | | list |
| `gpt-5.6-sol` | GPT-5.6-Sol | Legacy model for coding and everyday work. | | list |
| `gpt-5.6-terra` | GPT-5.6-Terra | Legacy balanced model for agentic coding. | | list |
| `gpt-5.6-luna` | GPT-5.6-Luna | Legacy fast model for simpler tasks. | | list |
| `gpt-reserve` | GPT-Reserve | Fast and affordable agentic coding model. | | hidden |
| `codex-auto-review` | Codex Auto Review | Automatic approval review model for Codex. | | hidden |

Live exec could not compare Terra with Sol: the CLI is out of usage until 24 Nov 23:26Z. Astra stays on charts and thumbnails (Ben, 14 Oct). Sol stays the assembly Codex id. Terra is not a thumbnail model; it is a computer-use model, and it was not probed.

Codex is flagged in `scripts/credit_flags.json` and marked down on this Mini until that reset. Gemini is the acting Chief while Claude and Grok Bot are also down.

## Cursor (`agent` 2026.11.19-f005e9d, `agent --list-models`, 288 lines)

Routed ids:

| Routing key | CLI id | On the list today | This run |
|---|---|---|---|
| `cursor-grok-4-7` | `grok-4.7` | Not bare. List has `grok-4.7-low/-medium/-high/-xhigh` and `-fast` | Bare id accepted. Reply OK. Code probe OK |
| `cursor-claude-opus-5-5` | `claude-opus-5-5` | Not bare. List has `claude-opus-5-5-low` through `-max` and `-fast` | Not probed. The lane is flagged until 9 Dec (J2595) |
| `cursor-auto` | (none) | `auto` | Flagged until 9 Dec, because an unnamed Cursor start uses Opus 5.5 |

Newer families on the list, not routed:

- `claude-fable-5-2-*` — every row is marked **NO ZDR**. The one-word reply was refused for weekly usage. Do not route to Fable.
- `claude-fable-5`, `claude-fable-5-1`, and their thinking rows — also NO ZDR. The 15 Oct note already left Fable unused.
- `claude-opus-5-thinking-*`, `claude-haiku-5-5-*`, `claude-sonnet-5-5-*`
- `gemini-4-neon-*`, `gemini-4-carbon-*`, `gemini-4-hydrogen-*` (Cursor's own copies; the studio Gemini lane is `agy`)
- `muse-wonder-1.0-*`, `muse-spark-1.3-*`
- No `gpt-6.2`, no `gpt-6.1-sol`, no `gpt-6-astra` on this Cursor list.

## Gemini (`agy` 1.5.13, `agy models`, 26 entries)

Same list as `MODELS_2026-11-20.md`: Neon, Carbon, Argon and Hydrogen tiers, three orchestrators, Gemini 3.8 Flash, Claude Opus 5.5, Claude Sonnet 5.5, and `gpt-oss-120b-medium`. Hard lane remains `gemini-4-neon-high`. Fallback remains `gemini-4-argon-high`.

## Claude Code (`claude` 2.1.326)

Installed. `claude -p --bare --model not-a-real-model` returned "Not logged in". No model catalogue was read. The help text names aliases `fable`, `opus` and `sonnet` for the latest model. Fable stays off the table: Cursor marks it NO ZDR, and the Fable 5.2 reply was refused.

## Vertex (publisher list, us-central1, names only, no generation)

Image and video ids the studio can name today:

| id | Against the current lane |
|---|---|
| `gemini-2.5-flash-image` | **Still the routed Vertex still.** Keep it. |
| `gemini-3-pro-image` | Newer. Not switched. A still would spend Vertex credit. |
| `gemini-3.1-flash-image`, `gemini-3.1-flash-image-preview`, `gemini-3.1-flash-lite-image` | Newer flash image ids. Not switched. |
| `gemini-nano-banana-2.1` | Newer than the name "Nano Banana 2". Not switched. |
| `veo-3.1-fast-generate-001` | **Still the routed fast video id.** |
| `veo-3.1-generate-001` | **Still the quality id.** |
| `veo-3.1-lite-generate-001` | Extra lite id. Not switched. |
| `gemini-omni-flash-preview` | **Still the Orbit Omni id.** |
| `gemini-omni-1.1-flash-preview`, `gemini-omni-1.2-flash` | Newer Omni ids. Not switched. Orbit jobs name Omni themselves. |

Flow's browser picker was not opened. No Flow generation. The routed Flow names stay Veo 3.1 and Nano Banana 2.

## Decisions left with Ben or the Chief

- **Ben, one line, no change made:** the complex-task Gemini lane stays Neon, and Codex still designs thumbnails. Carbon lost the short script. Terra was not probed, and it is not a thumbnail model. No GPT-6.2 Sol is installed.
- **Chief:** reorder the QA, listing and facts rows in `AGENTS.md` so they match the Neon-first chains. Do not merge a picture-model switch until a later job generates one still and one clip against the ids above.
