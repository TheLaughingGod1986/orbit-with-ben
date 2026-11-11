# Channels

**Phase 2 (6 Nov 2026):** each channel's settings now live in its own repo at `studio/channel.json`. Orbit With Ben's own file is `studio/channel.json` at this repo's root. `channels.json` here lists the plugged-in channels and where to find their checkouts. `channels/<slug>/channel.json` is the cached copy, used when a channel's repo isn't checked out on the machine; refresh it with `python3 scripts/channels.py sync`. The rest of this file describes the fields.

**The studio's own name (11 Nov 2026):** `channels.json` also has a `studio` section with one field, `prefix`. It is not a channel's name. It is the short name the studio installed on the machines under: launchd labels (`com.<prefix>.*`), state and log files, and the `<PREFIX>_AGENT` and `<PREFIX>_THREAD_PR` variables. The studio's code reads it with `channels.studio_prefix()`, `channels.studio_env(name)` and `channels.studio_label(name)` and never spells it. Changing it here renames nothing on a machine, so rename there first.

One folder per channel plugged into the studio (docs/MULTI_CHANNEL_PLAN.md, phase 1). The engine reads these through
`scripts/channels.py` and never names a channel itself.

`channel.json` holds:

- `slug`: what jobs carry in `repo` (`owb`, `hos`).
- `label`: the film-key prefix (`OWB:033`).
- `name`, `youtube`: the channel's public identity.
- `repo`: where its files live. This is the GitHub URL, the env var that overrides the checkout, and the folder
  names to look for under `~/YouTube`.
- `title_match`: a regex that marks a job's title as this channel when `repo` is missing.
- `wip`: its share of the WIP places.
- `stages`: the production stages, in order.
- `picture_route`: where video and image jobs are minted. `flow_only` uses Flow on the AI Ultra credits, with no priced
  Vertex fallback (HOS). `flow_first` uses Flow, then Vertex inside the spend rules (OWB).
- `shorts.planned_per_long`: how many Shorts each long video gets a place for on the board before they are made.
  Left out, or 0, the board shows only the Shorts that exist. A new channel starts at 0.
- `cadence`: its locked publishing slots in London time, in the order they are filled:
  `{"long": ["Sun 18:00", "Wed 18:00"], "short": ["Mon 11:30", ...]}`. `scripts/approved_deliver.py` gives each
  cut Ben has passed the next free one. Changing a channel's days is Ben's call. Left out, an approved cut is
  given the default channel's days, and `channel_check.py` lists it as still to do.
- `social.tiktok`: `"buffer"` when the channel's TikTok posts go through Buffer only. Left out otherwise.
- `desk`: for a channel that runs its own desk (where its Chief and reviewers talk): `{"tool": the desk tool's path
  inside its repo, "number": the number of the desk's thread}`. The relay's brief then sends an agent to that desk's
  inbox before the shared queue, and tells it how to report there. Left out otherwise. Read with `channels.desk(slug)`.
- `pipeline`: where its film state lives.
- `home`: not read from a channel's file any more (J2621, 11 Nov 2026). Whether a channel's content lives in the
  studio's own root is the registry's to say: `{"slug": ..., "home": true}` in `channels.json`. At most one channel
  can be, and none is once the studio has a repo of its own: then every channel is read through its checkout, and
  the registry's `studio` section answers what the home channel used to (`default_channel` for a job that names
  none, `github` and `checkouts` for the studio's own repo). The field in a channel's file is left as it is.

To add a channel (10 Nov 2026): `python3 scripts/channel_new.py <slug> --label ABC --name "Channel Name"` makes its
folder from `channels/_template/` with a filled-in `studio/channel.json`, and runs `scripts/channel_check.py` on it.
The command prints the steps after that: Ben creates the GitHub repo and does the YouTube sign-in and voice, the
folder is pushed there, and one line goes in `channels.json`. `python3 scripts/channel_check.py --all` says, for
every channel checked out on the machine, whether the studio can drive it and what is still to do.

`channels/_template/` is not a channel: it has no `channel.json` of its own and is not in the registry.
