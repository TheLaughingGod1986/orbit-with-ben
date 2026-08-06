# Quarantine — CDP replace / reupload scripts

**Date:** 2026-08-07  
**Reason:** These scripts created competing public BH longs, demoted canonical Shorts, and scheduled duplicate Shorts — contaminating recommendation signals.

## Disabled files

- `DISABLED__upload_smooth_cfr_v01.py`
- `DISABLED__upload_smooth_cfr_continue_v01.py`
- `DISABLED__replace_smooth_cfr_v01.py`
- `DISABLED__replace_smooth_cfr_v02.py`

Each raises `SystemExit` immediately if executed.

## Allowed path

`07_Content-Ops` → `npm run youtube:package` (YouTube Data API).  
CDP only for Studio-only finish (Related, pin, ABC, end screen).
