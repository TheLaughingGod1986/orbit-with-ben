#!/usr/bin/env python3
"""Orbit Shorts on-screen caption renderer — finalverdict-style kinetic text.

Bold lowercase yellow/white beats, soft shadow, no brand chrome.
Used by *_shorts_v02 builders.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Canvas
W, H = 1080, 1920

# Colors
YELLOW = (255, 230, 0, 255)  # #FFE600
WHITE = (255, 255, 255, 255)
STROKE = (10, 12, 18, 255)  # #0A0C12
SHADOW = (0, 0, 0, 190)

FONT_CANDIDATES = [
    Path("/System/Library/Fonts/Supplemental/Arial Black.ttf"),
    Path("/Library/Fonts/Arial Black.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    Path("/System/Library/Fonts/Supplemental/Impact.ttf"),
]

ColorName = str  # "yellow" | "white"
LineSpec = tuple[str, ColorName]


def resolve_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def _rgba(name: ColorName) -> tuple[int, int, int, int]:
    return YELLOW if name == "yellow" else WHITE


def _text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=0)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def render_beat_png(
    path: Path,
    lines: Sequence[LineSpec],
    *,
    pointsize: int = 92,
    y_center: int = 780,
    line_gap: int = 18,
    shadow_blur: int = 6,
    shadow_offset: tuple[int, int] = (3, 5),
    stroke_width: int = 4,
) -> Path:
    """Render one caption beat (1–3 lowercase lines) onto a transparent 1080×1920 PNG."""
    path = Path(path)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    font = resolve_font(pointsize)

    # Measure stack — auto-shrink so long hooks stay inside the frame
    probe = ImageDraw.Draw(img)
    font_size = pointsize
    cleaned: list[LineSpec] = []
    heights: list[int] = []
    widths: list[int] = []
    max_w = W - 80
    while font_size >= 42:
        font = resolve_font(font_size)
        cleaned, heights, widths = [], [], []
        overflow = False
        for raw, color in lines:
            text = " ".join(str(raw).strip().lower().split())
            if not text:
                continue
            tw, th = _text_size(probe, text, font)
            if tw > max_w:
                overflow = True
                break
            widths.append(tw)
            heights.append(th)
            cleaned.append((text, color))
        if not overflow and cleaned:
            break
        font_size -= 6
    if not cleaned:
        img.save(path)
        return path

    total_h = sum(heights) + line_gap * (len(cleaned) - 1)
    y = y_center - total_h // 2

    # Shadow layer
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    yy = y
    for (text, _), th in zip(cleaned, heights):
        tw, _ = _text_size(sdraw, text, font)
        x = (W - tw) // 2
        sdraw.text(
            (x + shadow_offset[0], yy + shadow_offset[1]),
            text,
            font=font,
            fill=SHADOW,
        )
        yy += th + line_gap
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=shadow_blur))
    img = Image.alpha_composite(img, shadow)

    draw = ImageDraw.Draw(img)
    yy = y
    for (text, color), th in zip(cleaned, heights):
        tw, _ = _text_size(draw, text, font)
        x = (W - tw) // 2
        draw.text(
            (x, yy),
            text,
            font=font,
            fill=_rgba(color),
            stroke_width=stroke_width,
            stroke_fill=STROKE,
        )
        yy += th + line_gap

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    return path


def render_cta_png(
    path: Path,
    text: str = "watch the full film →",
    *,
    pointsize: int = 48,
    y: int = 1580,
) -> Path:
    """Soft end CTA — lowercase white, no pill card. Funnels to the pillar long."""
    return render_beat_png(
        path,
        [(text, "white")],
        pointsize=pointsize,
        y_center=y,
        stroke_width=3,
        shadow_blur=5,
    )


def punch_first(phrases: Iterable[str], *, hook: str | None = None) -> list[str]:
    """Put the monster hook first — strongest phrase leads the first 1–2s.

    If ``hook`` is provided, that phrase (case-insensitive match) is moved to index 0.
    Otherwise the phrase with the most visceral tokens / question mark wins.
    """
    items = [str(p).strip() for p in phrases if str(p).strip()]
    if len(items) <= 1:
        return items

    if hook:
        hook_l = hook.strip().lower()
        # Prefer exact / phrase-contains-hook over hook-contains-phrase
        # (avoids hook "never come back" selecting bare "come back")
        for i, p in enumerate(items):
            pl = p.lower()
            if pl == hook_l or hook_l in pl:
                return [items[i]] + items[:i] + items[i + 1 :]
        for i, p in enumerate(items):
            pl = p.lower()
            if pl and pl in hook_l and len(pl) >= 8:
                return [items[i]] + items[:i] + items[i + 1 :]

    visceral = (
        "never",
        "everybody",
        "watching",
        "glass",
        "diamond",
        "die",
        "alone",
        "stop",
        "cross",
        "look back",
        "clue",
        "life?",
        "rude",
        "sideways",
        "eyeball",
        "no return",
        "?",
    )

    def score(p: str) -> tuple[int, int, int]:
        pl = p.lower()
        hit = sum(1 for v in visceral if v in pl)
        q = 1 if "?" in p else 0
        # Prefer punchy length (2–4 words) over long explainers
        n = len(re.findall(r"[a-z0-9']+", pl))
        length_bonus = 2 if 1 <= n <= 4 else (1 if n <= 6 else 0)
        return (hit + q * 2 + length_bonus, -n, -len(p))

    ranked = sorted(range(len(items)), key=lambda i: score(items[i]), reverse=True)
    best = ranked[0]
    if best == 0:
        return items
    return [items[best]] + items[:best] + items[best + 1 :]


def _phrase_lines(phrase: str, *, beat_index: int) -> list[LineSpec]:
    parts = [x.strip() for x in str(phrase).replace("\\n", "\n").split("\n") if x.strip()]
    lines: list[LineSpec] = []
    for j, part in enumerate(parts):
        color: ColorName = "yellow" if (beat_index + j) % 2 == 0 else "white"
        lines.append((part, color))
    return lines


def auto_beats_from_phrases(
    phrases: Iterable[str],
    *,
    duration: float,
    hook_end: float = 7.0,
    punch_first_hook: bool | str = True,
) -> list[dict]:
    """Split a list of short phrases across the opening hook window.

    Each phrase becomes one beat. Multi-word phrases can include ``\\n`` for stacked lines.
    Colors alternate yellow → white → yellow…

    ``punch_first_hook``: True = auto-rank monster hook first; str = force that phrase first;
    False = keep author order.
    """
    items = [p for p in phrases if str(p).strip()]
    if not items:
        return []
    if punch_first_hook is True:
        items = punch_first(items)
    elif isinstance(punch_first_hook, str) and punch_first_hook.strip():
        items = punch_first(items, hook=punch_first_hook)

    window = min(max(hook_end, 3.0), max(duration - 4.5, 3.0))
    # First beat gets a slightly longer dwell (stop-the-scroll)
    if len(items) == 1:
        weights = [1.0]
    else:
        weights = [1.35] + [1.0] * (len(items) - 1)
    total_w = sum(weights)
    beats: list[dict] = []
    t = 0.0
    for i, phrase in enumerate(items):
        lines = _phrase_lines(phrase, beat_index=i)
        span = window * (weights[i] / total_w)
        t1 = window if i == len(items) - 1 else min(t + span, window)
        beats.append({"start": round(t, 3), "end": round(t1, 3), "lines": lines})
        t = t1
    return beats


def _norm_token(s: str) -> str:
    return re.sub(r"[^a-z0-9']+", "", s.lower())


def align_phrases_to_words(
    phrases: Iterable[str],
    words: Sequence[dict],
    *,
    duration: float,
    hook_end: float = 8.0,
    punch_first_hook: bool | str = True,
    min_dwell: float = 0.85,
    pad_after: float = 0.15,
) -> list[dict]:
    """Build caption beats timed to VO word timestamps (ElevenLabs Scribe shape).

    Each word dict needs ``text`` / ``start`` / ``end``. Phrases are matched by
    token subsequence; unmatched phrases fall back to even spacing in leftover gaps.
    """
    items = [p for p in phrases if str(p).strip()]
    if not items:
        return []
    if punch_first_hook is True:
        items = punch_first(items)
    elif isinstance(punch_first_hook, str) and punch_first_hook.strip():
        items = punch_first(items, hook=punch_first_hook)

    window = min(max(hook_end, 3.0), max(duration - 4.5, 3.0))
    clean_words: list[dict] = []
    for w in words:
        if w.get("type") and w.get("type") != "word":
            continue
        text = _norm_token(str(w.get("text") or ""))
        if not text:
            continue
        clean_words.append(
            {
                "text": text,
                "start": float(w.get("start", 0)),
                "end": float(w.get("end", w.get("start", 0))),
            }
        )

    # Always lead with the monster hook on-screen (stop-scroll), even if VO
    # says that line later. Remaining phrases try VO alignment after the hook.
    hook_dwell = min(2.0, max(1.2, window / max(len(items), 1)))
    beats: list[dict] = [
        {
            "start": 0.0,
            "end": round(hook_dwell, 3),
            "lines": _phrase_lines(items[0], beat_index=0),
            "synced": False,
            "punch": True,
        }
    ]

    if len(items) == 1 or not clean_words:
        if len(items) > 1:
            rest = auto_beats_from_phrases(
                items[1:],
                duration=duration,
                hook_end=hook_end,
                punch_first_hook=False,
            )
            # Shift rest into the remaining window
            for i, b in enumerate(rest):
                span = b["end"] - b["start"]
                start = max(hook_dwell, b["start"] + hook_dwell * 0.0)
                # remap evenly after hook
                slot = (window - hook_dwell) / len(rest)
                start = hook_dwell + i * slot
                end = window if i == len(rest) - 1 else start + slot
                beats.append(
                    {
                        "start": round(start, 3),
                        "end": round(end, 3),
                        "lines": _phrase_lines(items[i + 1], beat_index=i + 1),
                        "synced": False,
                    }
                )
        return beats

    word_tokens = [w["text"] for w in clean_words]
    used_until = -1

    def find_phrase(phrase: str, start_at: int) -> tuple[int, float, float] | None:
        tokens = [_norm_token(t) for t in re.findall(r"[A-Za-z0-9']+", phrase)]
        tokens = [t for t in tokens if t]
        if not tokens:
            return None
        for i in range(start_at, len(word_tokens) - len(tokens) + 1):
            if word_tokens[i : i + len(tokens)] == tokens:
                return (i, clean_words[i]["start"], clean_words[i + len(tokens) - 1]["end"])
        if len(tokens) >= 2:
            first, last = tokens[0], tokens[-1]
            for i, tok in enumerate(word_tokens):
                if i < start_at or tok != first:
                    continue
                for j in range(i, min(i + len(tokens) + 4, len(word_tokens))):
                    if word_tokens[j] == last:
                        return (i, clean_words[i]["start"], clean_words[j]["end"])
        for tok in sorted(tokens, key=len, reverse=True):
            if len(tok) < 4:
                continue
            for i in range(start_at, len(word_tokens)):
                if word_tokens[i] == tok:
                    return (i, clean_words[i]["start"], clean_words[i]["end"])
        return None

    # If the punch phrase also appears in VO, mark punch beat synced but keep t=0
    punch_hit = find_phrase(items[0], 0)
    if punch_hit:
        beats[0]["synced"] = True
        used_until = punch_hit[0]

    rest_count = len(items) - 1
    if rest_count == 0:
        return beats

    # Collect VO hits for remaining phrases (must be after hook_dwell when possible)
    hits: list[tuple[float, float] | None] = []
    for phrase in items[1:]:
        found = find_phrase(phrase, max(0, used_until + 1))
        if found is None:
            found = find_phrase(phrase, 0)
        if found:
            used_until = max(used_until, found[0])
            ws, we = found[1], found[2]
            # Clamp into post-hook window; if VO said it during punch, place just after
            start = max(hook_dwell, min(ws, window - min_dwell))
            end = max(start + min_dwell, min(we + pad_after, window))
            hits.append((start, end))
        else:
            hits.append(None)

    # Fill missing with even spacing in leftover gaps
    missing = sum(1 for h in hits if h is None)
    slot = (window - hook_dwell) / max(rest_count, 1)
    cursor = hook_dwell
    for i, phrase in enumerate(items[1:]):
        if hits[i] is not None:
            start, end = hits[i]  # type: ignore[misc]
            start = max(start, cursor)
            if end <= start:
                end = min(start + min_dwell, window)
            beats.append(
                {
                    "start": round(start, 3),
                    "end": round(end, 3),
                    "lines": _phrase_lines(phrase, beat_index=i + 1),
                    "synced": True,
                }
            )
            cursor = end
        else:
            start = max(cursor, hook_dwell + i * slot)
            end = window if i == rest_count - 1 else min(start + slot, window)
            beats.append(
                {
                    "start": round(start, 3),
                    "end": round(end, 3),
                    "lines": _phrase_lines(phrase, beat_index=i + 1),
                    "synced": False,
                }
            )
            cursor = end

    # Resolve forward overlaps only (preserve punch-first order)
    for i in range(1, len(beats)):
        if beats[i]["start"] < beats[i - 1]["end"]:
            beats[i]["start"] = round(beats[i - 1]["end"], 3)
            if beats[i]["end"] <= beats[i]["start"]:
                beats[i]["end"] = round(min(beats[i]["start"] + min_dwell, window), 3)
    return beats


def load_words_json(path: Path) -> list[dict]:
    """Load Scribe/STT JSON — accepts raw words list or ``{words: [...]}``."""
    data = json.loads(Path(path).read_text())
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("words", "alignment", "tokens"):
            if isinstance(data.get(key), list):
                return data[key]
        tr = data.get("transcription") or data.get("result") or {}
        if isinstance(tr, dict) and isinstance(tr.get("words"), list):
            return tr["words"]
    return []


def ffmpeg_overlay_filter(
    beats: Sequence[dict],
    *,
    cta_start: float,
    beat_input_start: int = 1,
    has_cta: bool = True,
) -> str:
    """Build filter_complex tail that overlays beat PNGs + optional CTA on [base].

    Inputs: 0 = video, then beat PNGs starting at beat_input_start, then CTA last.
    """
    parts: list[str] = []
    label = "base"
    idx = beat_input_start
    for i, beat in enumerate(beats):
        nxt = f"b{i}"
        t0 = float(beat["start"])
        t1 = float(beat["end"])
        parts.append(
            f"[{label}][{idx}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'"
            f":format=auto[{nxt}]"
        )
        label = nxt
        idx += 1

    # fps=30 on the *final* label so PNG loops and the picture share a CFR clock.
    # Skipping this (and encoding with VideoToolbox) is what made social playback
    # stutter while audio stayed smooth.
    if has_cta:
        parts.append(
            f"[{label}][{idx}:v]overlay=0:0:enable='gte(t,{cta_start:.3f})'"
            f":format=auto,fps=30,format=yuv420p,setsar=1[v]"
        )
    else:
        parts.append(f"[{label}]fps=30,format=yuv420p,setsar=1[v]")
    return ";".join(parts)


def vertical_base_filter(*, framed: bool = False) -> str:
    """Full-bleed vertical grade. framed=False removes the old white card border."""
    core = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=22:1,eq=brightness=-0.32:saturation=0.9[bgv];"
        "[fg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,setsar=1[fgv];"
        "[bgv][fgv]overlay=0:0:format=auto"
    )
    if framed:
        return core + ",drawbox=x=28:y=(h-574)/2:w=1024:h=574:color=white@0.15:t=2,fps=30[base]"
    return core + ",fps=30[base]"
