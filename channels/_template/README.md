# {{NAME}}

A channel plugged into the studio. This repo holds the channel's content and its own rules. It holds no studio
code: the queue, the workers, the board and the gates live in the studio and read this repo through `studio/`.

| Path | What it is |
|---|---|
| `studio/channel.json` | The channel's settings: its name, its film-key prefix (`{{LABEL}}:012`), how many films it may have in work, its stages, where its progress lives. |
| `studio/RULES.md` | This channel's own rules for agents: titles, voice, picture, Shorts. They add to the studio's rules and never remove one. |
| `02_Video-Projects/NNN_Slug/` | One folder per film, with a `status.json` the studio keeps up to date. |
| `00_Brand/` | The channel's look: logo, colours, thumbnail style. |

Media (video, audio, images) is never committed. It lives on the NAS under `studio-live/{{SLUG}}/`.

Check the studio can drive this channel:

```bash
python3 <studio checkout>/scripts/channel_check.py .
```
