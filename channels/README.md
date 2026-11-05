# Channels

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
- `pipeline`: where its film state lives.
- `home`: true for the channel whose repo holds the engine today. In phase 3 that moves to its own repo.

To add a channel, copy a folder, change the values, and open a PR. Phase 2 moves each folder into its channel's own
repo as `studio/`.
