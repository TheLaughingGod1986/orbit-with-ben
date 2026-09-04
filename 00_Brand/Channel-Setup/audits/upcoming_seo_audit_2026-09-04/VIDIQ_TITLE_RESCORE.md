# VidIQ title rescore — 2026-09-04

Credits available again (app showed **1,548 / 2,420**). Cursor MCP still had no live VidIQ server token this session, so titles were scored in the logged-in **app.vidiq.com** title-score chat (`type=short`, GB), then winners applied in Studio.

## Locked titles (verified after reload)

| ID | Score | Title |
|----|------:|-------|
| `3QrICn9Kp00` | 93 | Why Does Light Leave Exhausted Near a Neutron Star? |
| `mAAMsbhm88w` | 93 | Could a Probe Get Closer to a Neutron Star? |
| `BX-z1EkgANg` | 92 | One Second Near a Neutron Star Is Enough |
| `vCxXTYXSSqY` | 89 | How Heavy Is a Teaspoon of Neutron Star? |
| `Xza_jSHD4qw` | 93 | How Life Could Feed Under Europa With No Sun |
| `fhJP6eMoU0Q` | 92 | Your Atoms Near a Neutron Star Do Not Survive |

## Notes

- Probe Short already at 93 — left unchanged.
- Teaspoon density beat tops out at **89** among brand-safe options tested; shipped as best available (no fearbait chase).
- Studio Save only enables when title change is typed via real input events (CDP `Input.insertText`); plain DOM `execCommand` alone does not stick.
- MCP: `~/.cursor/mcp.json` now includes `vidIQ` → `https://mcp.vidiq.com/mcp`. Generate/reveal an API key under app.vidiq.com → Account → MCP and paste into headers for next session, or complete Cursor OAuth Authorize.

All verified: **True**
