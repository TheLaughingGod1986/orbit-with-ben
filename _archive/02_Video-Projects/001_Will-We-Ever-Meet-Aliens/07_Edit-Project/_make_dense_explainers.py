#!/usr/bin/env python3
"""Generate dense descriptive explainer cards for every major narration beat."""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
    "/04_Generated-Clips/03_Polished/unique_cards"
)
LOGO = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Logos/orbit_mark_cutout_72.png")
LOGO_FALLBACK = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Logos/orbit_youtube-avatar_800x800_v02.png")
W, H, FPS = 1920, 1080, 30

# (stem, eyebrow, title, lines, accent_rgb, dur)
CARDS = [
    ("card_look_up", "COLD OPEN", "LOOK UP",
     ["A clear night. A crowded sky.", "Thousands of stars — billions more beyond."], (255, 140, 70), 4.5),
    ("card_where_everybody", "THE HOOK", "WHERE IS EVERYBODY?",
     ["If the universe is so big and so old…", "why hasn’t anyone waved back?"], (255, 120, 80), 5.0),
    ("card_real_question", "NOT A MEME", "WILL WE EVER MEET ALIENS?",
     ["A real question about biology, distance, time…", "and what “meeting” even means."], (255, 160, 60), 5.0),
    ("card_rudely_big", "HARD TRUTH", "SPACE IS RUDELY BIG",
     ["Not poetic distance.", "Awkward. Inconvenient. Almost rude."], (255, 110, 70), 4.5),
    ("card_habitable_zone", "WORLDS", "THE HABITABLE ZONE",
     ["Not too hot. Not too cold.", "Where liquid water could exist."], (80, 180, 255), 5.0),
    ("card_buzz_or_alone", "DRAKE MATHS", "BUZZING… OR ALONE?",
     ["Optimistic numbers → a crowded radio sky.", "Pessimistic numbers → alone for practical purposes."], (255, 180, 70), 6.0),
    ("card_fermi_lunch", "THE PARADOX", "IF THEY’RE COMMON… WHERE?",
     ["Enrico Fermi’s lunchtime question.", "No greetings. No fleets. No obvious megastructures."], (70, 200, 220), 5.5),
    ("card_no_city_lights", "WHAT WE DON’T SEE", "NO CITY LIGHTS",
     ["No glowing nightside cities on exoplanets.", "No clear technological fingerprint — yet."], (90, 160, 255), 5.0),
    ("card_no_megastructures", "WHAT WE DON’T SEE", "NO MEGASTRUCTURES",
     ["No star-wrapping engines in plain sight.", "The sky looks natural… so far."], (100, 150, 255), 5.0),
    ("card_no_fleets", "WHAT WE DON’T SEE", "NO VISITING FLEETS",
     ["No armadas in the solar neighbourhood.", "Just silence — as far as we can tell."], (110, 140, 255), 5.0),
    ("card_chemistry_curiosity", "ONE IDEA", "CHEMISTRY → CURIOSITY",
     ["Life may be common.", "The jump to intelligence might be the hard part."], (255, 150, 80), 5.5),
    ("card_burn_bright", "ANOTHER IDEA", "BURN BRIGHT. BURN SHORT.",
     ["Technology may not last.", "Civilisations collapse, change, or go quiet."], (255, 100, 70), 5.5),
    ("card_do_not_disturb", "ZOO HYPOTHESIS", "DO NOT DISTURB",
     ["Advanced watchers. Younger species.", "A cosmic nature reserve with a quiet rule."], (120, 200, 255), 5.5),
    ("card_party_early", "ANOTHER IDEA", "WE MIGHT BE EARLY",
     ["13.8 billion years old…", "but maybe the party hasn’t really started."], (255, 190, 80), 5.0),
    ("card_thousand_years", "LOGISTICS", "1,000 LIGHT-YEARS",
     ["A message sent today arrives in a thousand years.", "Ships could outlast empires — and species."], (80, 170, 255), 5.5),
    ("card_not_handshake", "WHAT “MEET” MEANS", "NOT A HANDSHAKE",
     ["A spectrum. A chemical fingerprint.", "A patterned signal — proof someone existed."], (255, 170, 70), 5.5),
    ("card_seti_listen", "HOW WE LOOK", "SETI IS LISTENING",
     ["Artificial radio or optical signals.", "Narrow-band whispers nature rarely makes."], (90, 200, 255), 5.5),
    ("card_wow_1977", "CANDIDATE", "THE WOW! SIGNAL — 1977",
     ["Intriguing. Unsettling.", "Never repeated cleanly enough to settle it."], (255, 140, 60), 5.5),
    ("card_cosmic_blink", "HONEST SCALE", "A COSMIC BLINK",
     ["We have not listened to every star,", "at every frequency, for long enough."], (180, 190, 210), 5.5),
    ("card_biosignature", "NEXT FRONTIER", "BIOSIGNATURES",
     ["Not just finding planets —", "finding gases a living world might breathe."], (90, 220, 160), 5.5),
    ("card_line_on_graph", "FIRST CONTACT?", "A LINE ON A GRAPH",
     ["We may meet aliens first as data:", "a wobble… a molecule that shouldn’t be there."], (255, 180, 70), 5.5),
    ("card_ice_grain", "CLOSER TO HOME", "A MICROBE IN AN ICE GRAIN",
     ["Mars. Icy moons. No radios required.", "Life more than once would rewrite biology."], (140, 200, 255), 5.5),
    ("card_faceplate", "THE HONEST ASK", "FACE TO… FACEPLATE?",
     ["Physical travellers in our lifetime?", "The odds look long. The timescales are brutal."], (255, 120, 80), 5.5),
    ("card_this_century", "THE WINDOW", "THIS CENTURY MATTERS",
     ["Clear evidence of life beyond Earth", "is moving from philosophy toward measurement."], (255, 170, 60), 5.5),
    ("card_silence_us", "QUIETER LESSON", "THE SILENCE IS ABOUT US TOO",
     ["How long do we last?", "How carefully do we listen — without hype?"], (200, 160, 255), 5.5),
    ("card_maybe_signal", "POSSIBLE ANSWERS", "MAYBE AS A SIGNAL",
     ["Maybe a biosignature.", "Maybe never as a conversation."], (255, 160, 70), 5.0),
    ("card_invitation", "CLOSING", "THE SILENCE IS AN INVITATION",
     ["Not empty.", "An invitation to keep listening."], (255, 150, 60), 5.5),
]


def font(size: int, bold=True):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()


def make_card(eyebrow: str, title: str, lines: list[str], accent: tuple[int, int, int]) -> Image.Image:
    bg0 = (10, 12, 22)
    img = Image.new("RGB", (W, H), bg0)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(
            int(bg0[0] + 12 * t),
            int(bg0[1] + 14 * t),
            int(bg0[2] + 22 * t),
        ))
    # soft star dust
    import random
    rng = random.Random(hash(title) & 0xFFFF)
    for _ in range(90):
        x, y = rng.randint(40, W - 40), rng.randint(40, H - 40)
        c = rng.randint(40, 90)
        d.ellipse([x, y, x + 2, y + 2], fill=(c, c + 8, c + 18))

    d.rectangle([100, 280, 136, 720], fill=accent)
    d.text((170, 200), eyebrow, fill=accent, font=font(28))
    # wrap title if long
    title_font = font(64 if len(title) < 28 else 52)
    d.text((170, 260), title, fill=(255, 255, 255), font=title_font)
    y = 400
    for line in lines:
        d.text((170, y), line, fill=(200, 210, 225), font=font(34, bold=False))
        y += 58

    # Wordmark only — living companion Orbit is composited bottom-left.
    d.text((W - 200, H - 72), "ORBIT", fill=(255, 150, 50), font=font(22))
    return img


def encode(png: Path, mp4: Path, dur: float):
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-framerate", str(FPS), "-i", str(png),
        "-t", f"{dur:.3f}", "-vf", "format=yuv420p",
        "-c:v", "libx264", "-tune", "stillimage", "-preset", "medium", "-crf", "18",
        "-an", str(mp4),
    ], check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for stem, eyebrow, title, lines, accent, dur in CARDS:
        png = OUT / f"{stem}.png"
        mp4 = OUT / f"{stem}_v01.mp4"
        make_card(eyebrow, title, lines, accent).save(png)
        encode(png, mp4, dur)
        print("OK", mp4.name)


if __name__ == "__main__":
    main()
