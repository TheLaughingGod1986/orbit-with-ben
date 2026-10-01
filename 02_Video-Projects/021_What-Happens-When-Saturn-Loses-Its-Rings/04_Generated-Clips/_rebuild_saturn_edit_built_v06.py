#!/usr/bin/env python3
"""Rebuild edit-built v06 after sprite/grain fixes."""
from __future__ import annotations

import json
import time

import _gen_saturn_edit_built_v06 as m

OUT = m.OUT
UAT = m.UAT
ART = m.ART


def main() -> None:
    ice = m.build_ice_crowd()
    open_meta = m.build_opening()
    approvals = m.write_approvals()
    manifest = {
        "engine": "edit_built",
        "ben_order": approvals["ben_order"],
        "duration_seconds": m.DUR,
        "fps": m.FPS,
        "size": f"{m.W}x{m.H}",
        "approvals": approvals,
        "clips": [open_meta, ice],
        "stop": "WAIT Ben OK — contacts only; not in cut yet",
        "finishedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    lines = [
        "# SHA-256 — saturn_edit_built_v06",
        "",
        "| File | SHA-256 | Bytes |",
        "|---|---|---|",
    ]
    for c in manifest["clips"]:
        lines.append(f"| `{c['file']}` | `{c['sha256']}` | {c['bytes']} |")
        csha = m.sha256(OUT / c["contact"])
        lines.append(
            f"| `{c['contact']}` | `{csha}` | {(OUT / c['contact']).stat().st_size} |"
        )
    for a in approvals["approved_no_touch"]:
        lines.append(
            f"| `{a['file']}` (approved leave) | `{a['sha256']}` | {a['bytes']} |"
        )
    (OUT / "SHA256.md").write_text("\n".join(lines) + "\n")

    UAT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    for c in manifest["clips"]:
        for name in (c["file"], c["contact"]):
            m.chunk_write(OUT / name, UAT / name)
        m.chunk_write(OUT / c["contact"], ART / c["contact"])
    for name in ("MANIFEST.json", "SHA256.md", "README.md"):
        m.chunk_write(OUT / name, UAT / name)
        m.chunk_write(OUT / name, ART / name)
    print(json.dumps({"REBUILD_DONE": True, "manifest": manifest}, indent=2), flush=True)


if __name__ == "__main__":
    main()
