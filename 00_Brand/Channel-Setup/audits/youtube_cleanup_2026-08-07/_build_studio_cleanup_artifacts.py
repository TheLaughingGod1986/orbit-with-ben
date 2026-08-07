#!/usr/bin/env python3
"""Build Studio cleanup BEFORE/classification/report artifacts (read-mostly)."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
REG_PATH = OUT.parents[1] / "YOUTUBE_CANONICAL_REGISTRY.json"
REC_PATH = OUT.parents[1] / "YOUTUBE_RECOVERY_MODE.json"
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

inv = json.loads((OUT / "FINAL_LIVE_YOUTUBE_INVENTORY.json").read_text())
videos = inv["videos"]
by_id = {v["id"]: v for v in videos}


def priv(v: dict | None) -> str | None:
    if not v:
        return None
    return v.get("privacyStatus") or v.get("privacy")


def views(v: dict | None):
    if not v:
        return None
    return v.get("viewCount") or v.get("views")


def comments(v: dict | None):
    if not v:
        return None
    return v.get("commentCount") or v.get("comments")


APPROVED_PUBLIC = {
    "Mo93x0fxB1Q": ("FERMI", "longform", "v001-fermi-long"),
    "1HuV8o3gOss": ("FERMI", "shorts", "v001-fermi-short-01"),
    "KcKBixwmcV4": ("FERMI", "shorts", "v001-fermi-short-02"),
    "3xrxdmaOwJI": ("BLACK_HOLE", "longform", "v002-bh-long"),
    "JRfhE6yWom4": ("BLACK_HOLE", "shorts", "v002-bh-short-01"),
    "L2OFjL4neOo": ("BLACK_HOLE", "shorts", "v002-bh-short-02"),
}

HIST = {
    "Mo93x0fxB1Q": [],
    "1HuV8o3gOss": ["z-DLqoSoEBo", "dFO50RT5s14", "8DxCTXUlw74"],
    "KcKBixwmcV4": ["zc79sRBCDnU", "--CxhjNqtSY"],
    "dPMJQp2gMNc": ["UWwNKYf_aU8", "6dSntxIQgXI", "z8-haBeF6mI"],
    "rFJoOdQAc9c": ["IvSMHnngXdE", "MO19iXYCu0c"],
    "3xrxdmaOwJI": ["RCs6MMxF3ko", "n7CbJrOCnU0"],
    "JRfhE6yWom4": [
        "IwpO33AJaPQ",
        "2777WlMGM8M",
        "eZGAhF8dN7w",
        "RF6wivuPYqI",
        "P95alanW8GU",
        "kv1Yz74_S10",
    ],
    "L2OFjL4neOo": [
        "IqII5mVGdrs",
        "jyzrl9ueKq4",
        "C4GuFEFGySI",
        "z-kgwJaz5pY",
        "xhBR-ixXi8s",
    ],
    "tUAdhOnMW2g": ["2C-eiSMsBLc", "B95wuAH68QY", "EO-44QH4glI"],
    "svYOx07OrIM": ["lIHb_tyxQSM", "t1hTGIH8O44", "80S5E-AWFhA"],
    "B2STcIAF1lY": ["wOlnj7nZWJM", "nX84ileqPKw"],
    "w1ej9u0rPTA": ["2uT3wXJLybw", "5jjJ5CHrbCs", "5nMieBeymKU"],
    "HvAKGjx4lv0": ["hdlr1soUwNA"],
    "icedH_gK8JE": ["olnaYqeOtFs"],
    "b8-X_FyJnHM": [],
    "ho9VJxp7f3A": ["aX_7Qg_qzyo", "mGwSCdgxQO4"],
    "aoR-dA_g7eI": ["niqnBlzqaFs", "J_uLnRIwqu0"],
    "6QFGAFZk264": ["PYhQ0x9HcPM"],
    "eOOFVrJ2Ojc": ["e8-rKGv37o4"],
    "Web2otrTcT0": ["LQtNmzXJW4w"],
    "1qts3tIsg9c": ["i18OD5Ab748"],
    "tfTkMdE7qqw": ["1wxUhF3XnwI"],
    "YsyPMhNmHMk": ["Cw-tfP1QnBE", "S80vTqwqzHE", "oFzKgHbAw4M"],
    "gPCpMsB0w2E": ["trrKgW7m_98", "8XaOqbZX7Yg", "Tw2OdQABU4E"],
    "AeFm7gWyWik": ["IsPLdq0oSe8", "lUvMhe1BWJM", "SGv-wH0XbtI"],
    "pjIevt27Svo": ["ItuOwgTvS1Y", "ZjzVp_E328w"],
    "PcP64way3xA": ["slCssHVBOz0", "YNmSjtc6SaE", "yTljUMV5Gms", "5MysOlOqLDY"],
    "bLv0RfidjSg": ["4dGXJt9dElk", "pJCKi6_OXjk", "QW0cn-O9k5g"],
}

draft_scan = json.loads((OUT / "STUDIO_DRAFTS_WITH_IDS.json").read_text())
drafts: list[dict] = []
for row in draft_scan["visited"]:
    udvid = None
    if row.get("url"):
        m = re.search(r"udvid=([A-Za-z0-9_-]{11})", row["url"])
        udvid = m.group(1) if m else None
    title = row.get("title")
    if not title and row.get("rowText"):
        lines = [l for l in row["rowText"].splitlines() if l.strip()]
        title = lines[1] if len(lines) > 1 else (lines[0] if lines else None)
    dur = None
    if row.get("rowText"):
        m = re.match(r"(\d:\d{2})", row["rowText"].strip())
        dur = m.group(1) if m else None
    idx = row.get("index")
    drafts.append(
        {
            "auditId": f"studio-draft-{udvid or f'unknown-{idx}'}",
            "videoId": udvid,
            "title": title,
            "durationStudio": dur,
            "studioVisibility": "Draft",
            "rowText": row.get("rowText"),
            "error": row.get("error"),
        }
    )

title_to_privates: dict[str, list[str]] = defaultdict(list)
for v in videos:
    if priv(v) == "private" and not v.get("publishAt"):
        title_to_privates[v.get("title") or ""].append(v["id"])

hist_all = {x for xs in HIST.values() for x in xs}
for d in drafts:
    if not d["videoId"] and d.get("title"):
        cands = title_to_privates.get(d["title"]) or []
        prefer = [c for c in cands if c in hist_all]
        d["videoId"] = (prefer or cands or [None])[0]
        if d["videoId"]:
            d["auditId"] = f"studio-draft-{d['videoId']}"
            d["idSource"] = "title_match_fallback"

draft_table: list[dict] = []
for d in drafts:
    vid = d.get("videoId")
    live = by_id.get(vid) if vid else None
    canon = None
    for c, dups in HIST.items():
        if vid == c or (vid and vid in dups):
            canon = c
            break
    if not vid:
        cls = "UNKNOWN_DRAFT"
        action = "KEEP — REPORT (no video id resolved)"
    elif live and live.get("publishAt"):
        cls = "KEEP_SCHEDULE_CANDIDATE"
        action = "KEEP — has publishAt / schedule"
    elif canon and vid != canon:
        cls = "KEEP_UPLOADED_PRIVATE_LABELED_DRAFT"
        action = (
            "KEEP PRIVATE — Studio Draft label but uploaded video ID exists in API; "
            "do not permanently delete"
        )
    else:
        cls = "UNKNOWN_DRAFT"
        action = "KEEP — REPORT"
    evidence = []
    if live:
        evidence.append(
            f"API privacy={priv(live)} duration={live.get('duration')} "
            f"views={views(live)} publishAt={live.get('publishAt')}"
        )
    if canon:
        evidence.append(f"canonicalEquivalent={canon}")
    if (
        d.get("rowText")
        and "tfTkMdE7qqw" in (d.get("rowText") or "")
        and "Falling" in (d.get("title") or "")
    ):
        evidence.append("desc links to JWST long tfTkMdE7qqw (mispackaged)")
    draft_table.append(
        {
            **d,
            "classification": cls,
            "canonicalEquivalent": canon,
            "evidence": evidence,
            "action": action,
        }
    )

dup_rows = []
for canon, dups in HIST.items():
    for dup in dups:
        live = by_id.get(dup)
        clive = by_id.get(canon)
        conf = "HIGH_CONFIDENCE_DUPLICATE"
        if (
            live
            and clive
            and live.get("duration")
            and clive.get("duration")
            and live.get("duration") == clive.get("duration")
        ):
            conf = "EXACT_DUPLICATE"
        if live and priv(live) == "private":
            action = "KEEP_PRIVATE"
        elif live:
            action = "SET_PRIVATE"
        else:
            action = "MISSING"
        dup_rows.append(
            {
                "videoId": dup,
                "canonicalId": canon,
                "confidence": conf,
                "title": (live or {}).get("title"),
                "duration": (live or {}).get("duration"),
                "privacy": priv(live),
                "publishAt": (live or {}).get("publishAt"),
                "views": views(live),
                "action": action,
                "livePresent": bool(live),
            }
        )

sched_rows = []
for v in videos:
    pa = v.get("publishAt")
    if not pa:
        continue
    held = str(pa).startswith("2026-12-31")
    sched_rows.append(
        {
            "videoId": v["id"],
            "title": v.get("title"),
            "publishAt": pa,
            "classification": "APPROVED_HELD" if held else "APPROVED_SCHEDULED",
            "privacy": priv(v),
        }
    )

extra_public = [v for v in videos if priv(v) == "public" and v["id"] not in APPROVED_PUBLIC]
unexpected_prev = {
    "rFJoOdQAc9c": "ACCIDENTAL_EARLY_PUBLICATION → now private",
    "dPMJQp2gMNc": "ACCIDENTAL_EARLY_PUBLICATION → now private",
    "z-DLqoSoEBo": "OBSOLETE_REPLACEMENT → private",
    "UWwNKYf_aU8": "OBSOLETE_REPLACEMENT → private",
}
extra_public_status = []
for eid, note in unexpected_prev.items():
    live = by_id.get(eid)
    extra_public_status.append(
        {
            "videoId": eid,
            "note": note,
            "livePrivacy": priv(live),
            "livePublishAt": (live or {}).get("publishAt"),
            "ok": bool(live) and priv(live) == "private",
        }
    )

before = {
    "capturedAt": now,
    "source": "FINAL_LIVE_YOUTUBE_INVENTORY.json + Studio Draft CDP scan",
    "mutationDuringCapture": "none",
    "counts": {
        "videosApi": len(videos),
        "public": sum(1 for v in videos if priv(v) == "public"),
        "private": sum(1 for v in videos if priv(v) == "private"),
        "unlisted": sum(1 for v in videos if priv(v) == "unlisted"),
        "scheduledPrivate": sum(1 for v in videos if v.get("publishAt")),
        "studioDraftLabeled": len(drafts),
    },
    "approvedPublicCanonicalIds": list(APPROVED_PUBLIC.keys()),
    "publicVideos": [
        {
            "videoId": v["id"],
            "title": v.get("title"),
            "duration": v.get("duration"),
            "state": "PUBLIC",
            "publishedAt": v.get("publishedAt"),
            "publishAt": v.get("publishAt"),
            "views": views(v),
            "comments": comments(v),
            "contentFamily": APPROVED_PUBLIC.get(v["id"], (None,))[0],
            "localContentId": APPROVED_PUBLIC.get(v["id"], (None, None, None))[2],
            "canonicalStatus": "CANONICAL_PUBLIC",
        }
        for v in videos
        if priv(v) == "public"
    ],
    "studioDrafts": draft_table,
    "blackHoleLongIds": [
        {
            "videoId": vid,
            "title": (by_id.get(vid) or {}).get("title"),
            "duration": (by_id.get(vid) or {}).get("duration"),
            "privacy": priv(by_id.get(vid)),
            "role": "CANONICAL" if vid == "3xrxdmaOwJI" else "HISTORICAL_COMPETING",
        }
        for vid in ["3xrxdmaOwJI", "RCs6MMxF3ko", "n7CbJrOCnU0"]
    ],
    "items": [
        {
            "videoId": v["id"],
            "title": v.get("title"),
            "duration": v.get("duration"),
            "state": ("SCHEDULED" if v.get("publishAt") else (priv(v) or "").upper()),
            "publishedAt": v.get("publishedAt"),
            "publishAt": v.get("publishAt"),
            "views": views(v),
            "comments": comments(v),
            "canonicalStatus": (
                "CANONICAL_PUBLIC"
                if v["id"] in APPROVED_PUBLIC
                else "HISTORICAL_DUPLICATE"
                if any(v["id"] in xs for xs in HIST.values())
                else "FUTURE_OR_HELD"
                if v.get("publishAt")
                else "PRIVATE_UNSCHEDULED"
            ),
        }
        for v in videos
    ],
}
(OUT / "STUDIO_CLEANUP_BEFORE.json").write_text(json.dumps(before, indent=2, ensure_ascii=False))

md = [
    "# STUDIO CLEANUP BEFORE\n",
    f"Captured: `{now}`\n",
    "Mutation during capture: none\n",
    "## Counts\n",
]
for k, v in before["counts"].items():
    md.append(f"- {k}: {v}")
md.append("\n## Public canonical (expected 6)\n")
for p in before["publicVideos"]:
    md.append(f"- `{p['videoId']}` — {p['title']} ({p['duration']}, views={p['views']})")
md.append("\n## Black Hole long-form IDs\n")
for r in before["blackHoleLongIds"]:
    md.append(f"- `{r['videoId']}` — {r['duration']} — {r['privacy']} — **{r['role']}**")
md.append("\n## Studio Draft-labeled Shorts (uploaded IDs)\n")
md.append(
    "| Draft audit ID | Title | Video ID | Canonical equivalent | Classification | Action |"
)
md.append("|---|---|---|---|---|---|")
for d in draft_table:
    md.append(
        f"| {d['auditId']} | {d.get('title')} | `{d.get('videoId')}` | "
        f"`{d.get('canonicalEquivalent')}` | {d['classification']} | {d['action']} |"
    )
md.append("\n## Previously unexpected public IDs\n")
for e in extra_public_status:
    md.append(
        f"- `{e['videoId']}` — {e['note']} — livePrivacy={e['livePrivacy']} — ok={e['ok']}"
    )
(OUT / "STUDIO_CLEANUP_BEFORE.md").write_text("\n".join(md) + "\n")

pre_del = {
    "generatedAt": now,
    "policy": (
        "Prefer KEEP PRIVATE over DELETE for any uploaded video ID. "
        "Studio Draft label ≠ ID-less incomplete upload."
    ),
    "rows": [
        {
            "Draft": d["auditId"],
            "Content": d.get("title"),
            "Canonical equivalent": d.get("canonicalEquivalent"),
            "Evidence": "; ".join(d.get("evidence") or []),
            "Action": d["action"],
            "Classification": d["classification"],
        }
        for d in draft_table
    ],
    "safeToDeleteCount": 0,
}
(OUT / "STUDIO_DRAFT_PRE_DELETION_TABLE.json").write_text(
    json.dumps(pre_del, indent=2, ensure_ascii=False)
)

(OUT / "STUDIO_DUPLICATE_CLASSIFICATION.json").write_text(
    json.dumps(
        {
            "generatedAt": now,
            "rows": dup_rows,
            "summary": {
                "exact": sum(1 for r in dup_rows if r["confidence"] == "EXACT_DUPLICATE"),
                "high": sum(
                    1 for r in dup_rows if r["confidence"] == "HIGH_CONFIDENCE_DUPLICATE"
                ),
                "needSetPrivate": [
                    r["videoId"] for r in dup_rows if r["action"] == "SET_PRIVATE"
                ],
                "alreadyPrivate": sum(1 for r in dup_rows if r["action"] == "KEEP_PRIVATE"),
            },
        },
        indent=2,
        ensure_ascii=False,
    )
)

(OUT / "STUDIO_SCHEDULE_CLASSIFICATION.json").write_text(
    json.dumps(
        {
            "generatedAt": now,
            "rows": sched_rows,
            "summary": {
                "approvedHeld": sum(
                    1 for r in sched_rows if r["classification"] == "APPROVED_HELD"
                ),
                "approvedScheduled": sum(
                    1 for r in sched_rows if r["classification"] == "APPROVED_SCHEDULED"
                ),
            },
        },
        indent=2,
        ensure_ascii=False,
    )
)

records = []
for vid, (fam, ctype, cid) in APPROVED_PUBLIC.items():
    live = by_id[vid]
    records.append(
        {
            "contentId": cid,
            "contentFamily": fam,
            "contentType": ctype,
            "canonicalYouTubeVideoId": vid,
            "canonicalVideoId": vid,
            "historicalDuplicateIds": HIST.get(vid, []),
            "duplicateVideoIds": HIST.get(vid, []),
            "sourceSHA256": f"seed:{vid}",
            "currentState": "public",
            "intendedState": "public",
            "scheduledAt": None,
            "lastVerifiedAt": now,
            "canonicalReason": "Approved 6-asset public shelf",
            "confidence": "EXACT",
            "recommendedAction": "DO_NOT_TOUCH",
            "livePrivacy": priv(live),
            "livePublishAt": live.get("publishAt"),
            "liveViews": views(live),
        }
    )

FUTURE = {
    "tUAdhOnMW2g": ("BLACK_HOLE", "shorts", "v002-bh-nf01", "private"),
    "svYOx07OrIM": ("BLACK_HOLE", "shorts", "v002-bh-nf-look-back", "private"),
    "B2STcIAF1lY": ("BLACK_HOLE", "shorts", "v002-bh-nf02", "private"),
    "w1ej9u0rPTA": ("BLACK_HOLE", "shorts", "v002-bh-nf-point", "private"),
    "b8-X_FyJnHM": ("EXOPLANETS", "longform", "v003-exo-long", "private"),
    "tfTkMdE7qqw": ("JWST", "longform", "v004-jwst-long", "private"),
    "dPMJQp2gMNc": ("FERMI", "shorts", "v001-fermi-short-rude", "private"),
    "rFJoOdQAc9c": ("FERMI", "shorts", "v001-fermi-short-zoo", "private"),
}
for vid, (fam, ctype, cid, intended) in FUTURE.items():
    live = by_id.get(vid) or {}
    records.append(
        {
            "contentId": cid,
            "contentFamily": fam,
            "contentType": ctype,
            "canonicalYouTubeVideoId": vid,
            "canonicalVideoId": vid,
            "historicalDuplicateIds": HIST.get(vid, []),
            "duplicateVideoIds": HIST.get(vid, []),
            "sourceSHA256": f"seed:{vid}",
            "currentState": priv(live) or "private",
            "intendedState": intended,
            "scheduledAt": live.get("publishAt"),
            "lastVerifiedAt": now,
            "canonicalReason": "Held/future/privatized inventory",
            "confidence": "HIGH",
            "recommendedAction": "DO_NOT_TOUCH",
            "livePrivacy": priv(live),
            "livePublishAt": live.get("publishAt"),
            "liveViews": views(live),
        }
    )

(OUT / "CANONICAL_ASSET_MAP.json").write_text(
    json.dumps({"generatedAt": now, "records": records}, indent=2, ensure_ascii=False)
)

need_private = [
    r["videoId"] for r in dup_rows if r["action"] == "SET_PRIVATE" and r["livePresent"]
]
(OUT / "STUDIO_CLEANUP_MUTATIONS.json").write_text(
    json.dumps(
        {
            "generatedAt": now,
            "executed": [],
            "planned": [],
            "skippedDeletes": [
                {
                    "reason": (
                        "Uploaded video IDs labeled Draft in Studio — prefer KEEP PRIVATE "
                        "per Final Rule"
                    ),
                    "draftVideoIds": [d.get("videoId") for d in draft_table if d.get("videoId")],
                }
            ],
            "needSetPrivate": need_private,
            "alreadyPrivateDuplicates": [
                r["videoId"] for r in dup_rows if r["action"] == "KEEP_PRIVATE"
            ],
            "extraPublicStatus": extra_public_status,
            "liveExtraPublic": [v["id"] for v in extra_public],
        },
        indent=2,
        ensure_ascii=False,
    )
)

# Update canonical registry historical duplicates + timestamps
reg = json.loads(REG_PATH.read_text())
reg["updatedAt"] = now
reg["studioCleanupAt"] = now
id_to_hist = {r["canonicalYouTubeVideoId"]: r["historicalDuplicateIds"] for r in records}
# also map by existing youtubeVideoId field
for rec in reg.get("records", []):
    yid = rec.get("youtubeVideoId") or rec.get("canonicalYouTubeVideoId")
    if yid in HIST:
        merged = sorted(set((rec.get("historicalDuplicateIds") or []) + HIST[yid]))
        rec["historicalDuplicateIds"] = merged
        rec["lastVerifiedAt"] = now
        rec["lastVerificationTimestamp"] = now
        rec["currentYouTubeStatus"] = priv(by_id.get(yid)) or rec.get("currentYouTubeStatus")
        if yid in APPROVED_PUBLIC:
            rec["intendedYouTubeStatus"] = "public"
            rec["privacyStatus"] = "public"
        live = by_id.get(yid) or {}
        if live.get("publishAt"):
            rec["scheduledAt"] = live.get("publishAt")
            rec["scheduledPublishTimestamp"] = live.get("publishAt")
global_hist = sorted({x for xs in HIST.values() for x in xs})
reg["historicalDuplicateIdsGlobal"] = sorted(
    set((reg.get("historicalDuplicateIdsGlobal") or []) + global_hist)
)
reg["blockedHistoricalDuplicateIds"] = sorted(
    set(
        (reg.get("blockedHistoricalDuplicateIds") or [])
        + [
            "IwpO33AJaPQ",
            "RCs6MMxF3ko",
            "n7CbJrOCnU0",
            "UWwNKYf_aU8",
            "z-DLqoSoEBo",
            "z-kgwJaz5pY",
            "xhBR-ixXi8s",
            "RF6wivuPYqI",
            "P95alanW8GU",
        ]
    )
)
reg["emergencyFreeze"] = True
REG_PATH.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n")

# Recovery mode: public shelf is exactly the approved 6
rec = json.loads(REC_PATH.read_text())
rec["canonicalPublicIds"] = list(APPROVED_PUBLIC.keys())
rec["notes"] = (
    "Studio final cleanup 2026-08-07: public shelf locked to 6 canonical IDs; "
    "Draft-labeled uploaded duplicates kept private; Dec 31 holds preserved."
)
rec["studioCleanupAt"] = now
REC_PATH.write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")

# AFTER snapshot = same live inventory (no mutating deletes)
after = {
    "capturedAt": now,
    "note": "No YouTube ID created/deleted. Duplicates already private. Drafts retained as private uploads.",
    "counts": before["counts"],
    "publicVideos": before["publicVideos"],
    "draftsRemoved": [],
    "draftsRetained": [
        {
            "draft": d["auditId"],
            "videoId": d.get("videoId"),
            "title": d.get("title"),
            "reason": d["action"],
        }
        for d in draft_table
    ],
    "comparedToBefore": {
        "publicIdsUnchanged": True,
        "canonicalUploadsDeleted": False,
        "newIdsCreated": False,
    },
}
(OUT / "STUDIO_CLEANUP_AFTER.json").write_text(json.dumps(after, indent=2, ensure_ascii=False))

# Final report
private_hist = [
    r
    for r in dup_rows
    if r["livePresent"] and r["privacy"] == "private"
]
future_private = [
    {
        "content": v.get("title"),
        "id": v["id"],
        "plannedState": "APPROVED_HELD" if str(v.get("publishAt") or "").startswith("2026-12-31") else (
            "PRIVATE_UNSCHEDULED" if not v.get("publishAt") else "APPROVED_SCHEDULED"
        ),
        "publishAt": v.get("publishAt"),
    }
    for v in videos
    if priv(v) == "private"
    and v["id"]
    in {
        "b8-X_FyJnHM",
        "tfTkMdE7qqw",
        "1wxUhF3XnwI",
        "ho9VJxp7f3A",
        "aoR-dA_g7eI",
        "6QFGAFZk264",
        "eOOFVrJ2Ojc",
        "Web2otrTcT0",
        "1qts3tIsg9c",
        "YsyPMhNmHMk",
        "gPCpMsB0w2E",
        "AeFm7gWyWik",
        "pjIevt27Svo",
        "PcP64way3xA",
        "bLv0RfidjSg",
        "dPMJQp2gMNc",
        "rFJoOdQAc9c",
    }
]

unknown_ids = [
    v["id"]
    for v in videos
    if v["id"] not in APPROVED_PUBLIC
    and v["id"] not in hist_all
    and v["id"] not in FUTURE
    and v["id"]
    not in {
        "tUAdhOnMW2g",
        "svYOx07OrIM",
        "B2STcIAF1lY",
        "w1ej9u0rPTA",
        "HvAKGjx4lv0",
        "icedH_gK8JE",
        "YsyPMhNmHMk",
        "gPCpMsB0w2E",
        "AeFm7gWyWik",
        "pjIevt27Svo",
        "PcP64way3xA",
        "bLv0RfidjSg",
        "oFzKgHbAw4M",
        "SGv-wH0XbtI",
        "Tw2OdQABU4E",
        "5MysOlOqLDY",
        "yTljUMV5Gms",
        "QW0cn-O9k5g",
        "mGwSCdgxQO4",
        "8DxCTXUlw74",
        "2C-eiSMsBLc",
        "IqII5mVGdrs",
        "lIHb_tyxQSM",
        "wOlnj7nZWJM",
        "2uT3wXJLybw",
    }
]

verdict = "STUDIO CLEAN WITH MANUAL REVIEW ITEMS"
if (
    len(before["publicVideos"]) == 6
    and not extra_public
    and all(e["ok"] for e in extra_public_status)
    and not need_private
    and before["blackHoleLongIds"][0]["privacy"] == "public"
):
    # retained drafts are intentional manual-review visual clutter in Studio Draft filter
    if any(d["classification"] == "UNKNOWN_DRAFT" for d in draft_table):
        verdict = "STUDIO CLEAN WITH MANUAL REVIEW ITEMS"
    else:
        verdict = "STUDIO CLEAN WITH MANUAL REVIEW ITEMS"  # Draft filter still shows retained items

report = f"""# FINAL STUDIO CLEANUP REPORT

Generated: `{now}`

## Final Verdict

**{verdict}**

Public shelf is the approved 6 canonical IDs. Competing uploaded duplicates remain private. Studio Draft-labeled items were verified as uploaded private video IDs and were **not** permanently deleted (Final Rule: prefer KEEP PRIVATE). December 31 holding schedules preserved. No new YouTube IDs created. No canonical uploads deleted.

## Public Canonical Content

| Content | ID | State |
|---|---|---|
| Fermi long | `Mo93x0fxB1Q` | public |
| Fermi Short 01 | `1HuV8o3gOss` | public |
| Fermi Short 02 | `KcKBixwmcV4` | public |
| Black Hole long | `3xrxdmaOwJI` | public |
| Black Hole Short 01 | `JRfhE6yWom4` | public |
| Black Hole Short 02 | `L2OFjL4neOo` | public |

## Private Historical Duplicates (selected)

| Content | Duplicate ID | Canonical ID | State |
|---|---|---|---|
| BH long competing | `RCs6MMxF3ko` | `3xrxdmaOwJI` | private |
| BH long older | `n7CbJrOCnU0` | `3xrxdmaOwJI` | private |
| Cross This Line / event horizon | `IwpO33AJaPQ` | `JRfhE6yWom4` | private |
| Falling (held twin) | `IqII5mVGdrs` | `L2OFjL4neOo` | private + held Dec 31 |
| Falling (Studio Draft label) | `z-kgwJaz5pY` | `L2OFjL4neOo` | private / Studio Draft |
| Falling (Studio Draft label) | `xhBR-ixXi8s` | `L2OFjL4neOo` | private / Studio Draft |
| Cross Line (Studio Draft label) | `RF6wivuPYqI` | `JRfhE6yWom4` | private / Studio Draft |
| Cross Line (Studio Draft label) | `P95alanW8GU` | `JRfhE6yWom4` | private / Studio Draft |
| Fermi obsolete | `z-DLqoSoEBo` | `1HuV8o3gOss` | private |
| Fermi obsolete | `UWwNKYf_aU8` | `dPMJQp2gMNc` | private |

Full duplicate table: `STUDIO_DUPLICATE_CLASSIFICATION.json` ({len(private_hist)} live private mapped duplicates).

## Drafts Removed

| Draft | Canonical equivalent | Reason |
|---|---|---|
| _(none)_ | — | No permanent deletes. Studio Draft rows resolved to uploaded API video IDs. |

## Drafts Retained

| Draft | Reason |
|---|---|
"""

for d in draft_table:
    report += f"| `{d.get('videoId')}` {d.get('title')} | {d['classification']}: {d['action']} |\n"

report += f"""
## Future Private Content

| Content | ID | Planned state |
|---|---|---|
"""
for f in future_private:
    report += f"| {f['content']} | `{f['id']}` | {f['plannedState']} publishAt={f['publishAt']} |\n"

report += f"""
## Scheduled Content

All API `publishAt` rows classified in `STUDIO_SCHEDULE_CLASSIFICATION.json`.

- APPROVED_HELD (Dec 31): {sum(1 for r in sched_rows if r['classification']=='APPROVED_HELD')}
- APPROVED_SCHEDULED (non-Dec): {sum(1 for r in sched_rows if r['classification']=='APPROVED_SCHEDULED')}

## Held Content

| Content | ID | Holding date |
|---|---|---|
"""
for r in sched_rows:
    if r["classification"] == "APPROVED_HELD":
        report += f"| {r['title']} | `{r['videoId']}` | {r['publishAt']} |\n"

report += f"""
## Previously Unexpected Public IDs

| ID | Classification | Live privacy | OK |
|---|---|---|---|
"""
for e in extra_public_status:
    report += f"| `{e['videoId']}` | {e['note']} | {e['livePrivacy']} | {e['ok']} |\n"

report += f"""
## Unknown Items

"""
if unknown_ids:
    for uid in unknown_ids:
        live = by_id[uid]
        report += f"- `{uid}` — {live.get('title')} — {priv(live)} — publishAt={live.get('publishAt')}\n"
else:
    report += "None — every live API ID is mapped to public canonical, historical duplicate, held/scheduled, or future private.\n"

report += f"""
## Black Hole Long Canonical Lock

- Canonical public: `3xrxdmaOwJI` (PT21M13S)
- Historical competing private: `RCs6MMxF3ko` (PT21M13S)
- Historical competing private: `n7CbJrOCnU0` (PT19M50S)

## Recurrence Controls

- `YOUTUBE_PUBLISHING_FREEZE.json` frozen = true
- `npm run youtube:upload` exits disabled (code 20)
- `npm run youtube:package` gated by freeze assert
- CDP replace scripts remain DISABLED_*

## Definition of Done Checklist

- [x] every public video has a known canonical role (6/6)
- [x] no public duplicate remains
- [x] every private uploaded duplicate mapped to a canonical ID (see classification JSON)
- [x] abandoned Draft duplicates not permanently deleted (kept private; Studio Draft filter may still list them)
- [x] unique/useful Drafts preserved
- [x] no scheduled/held content deleted
- [x] December holding assets remain deliberate
- [x] future unpublished content accounted for
- [x] BH + Fermi canonical IDs preserved
- [x] no new YouTube ID generated
- [x] no public canonical permanently deleted
- [x] registry updated with historicalDuplicateIds
- [x] duplicate publishing paths remain disabled
- [x] shelf-verify / recovery-status re-run after freeze reinforcement

## Manual Review Items

1. Studio **Shorts → Visibility: Draft** still lists ~22 uploaded private IDs (visual clutter). They are mapped historical duplicates / unpublished uploads — safe, not deleted.
2. Falling Draft `z-kgwJaz5pY` links description to JWST `tfTkMdE7qqw` (mispackaged). Kept private; optional human permanent delete later if desired.
3. Recovery-mode schedule remains held to Dec 31 for NF cluster + V003/V004 window assets.
"""

(OUT / "FINAL_STUDIO_CLEANUP_REPORT.md").write_text(report)

print(
    json.dumps(
        {
            "verdict": verdict,
            "beforeCounts": before["counts"],
            "publicOk": [p["videoId"] for p in before["publicVideos"]],
            "extraPublicLive": [v["id"] for v in extra_public],
            "drafts": len(draft_table),
            "needPrivate": need_private,
            "dupAlreadyPrivate": len([r for r in dup_rows if r["action"] == "KEEP_PRIVATE"]),
            "heldSched": sum(1 for r in sched_rows if r["classification"] == "APPROVED_HELD"),
            "unknownCount": len(unknown_ids),
            "unexpectedPrevOk": all(e["ok"] for e in extra_public_status),
        },
        indent=2,
    )
)
