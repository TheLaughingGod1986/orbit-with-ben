# Familiar thing in danger

Standing strategy for every new Orbit film, locked 23 Sep 2026. Fill the blanks. Do not invent a second shape.

The lane is a familiar thing, and what space does to it. Moon leaving. A star you could not stand on. The last star going out. Wonder, not dread. Abstract cosmology, conspiracy, leaked-file disclosure, astrology, and celebrity tags stay off the channel.

## The week

Three Shorts and one long. Not eight or nine uploads.

The Shorts in a week promote more than one film. Past videos that already won stay in the week. The new long is one of the films being promoted, not the only one. Each Short points at the long it is about.

| Day | Type | Job |
|---|---|---|
| Mon | Short | Promotes one film, new or already out |
| Wed | Short | Promotes a different film |
| Fri | Short | Promotes a third film |
| Sun | Long, about 8–9 min | The new full film. One of the week’s Shorts teases this one. |

Week one is in [the week plan](WEEK_PLAN_3_SHORTS_1_LONG_2026-09-23.md). Monday promotes the new Moon film. Wednesday promotes the Last Star long. Friday promotes the Neutron Star long.

## Short hook

Same two-line shape every time. New words for each film. No greeting. No buildup.

Line 1 is 5 to 7 words. The familiar thing in danger. Spoken in the first second. **The danger fills the frame and is already moving at 0 seconds. Orbit is not in the 0-second frame.** (Changed 24 Sep 2026, per `audits/CHANNEL_AUDIT_2026-09-24/AUDIT.md`. The two Orbit-first opens measured so far got 0% Shorts-feed traffic. `gate_shorts_open.py` fails Orbit at 0 s.)

Line 2 is the stay line. What they get if they stay. Orbit arrives from about 1.5 seconds, caught up in the danger (pulled, tipping, freezing), and reacts while it is said. Orbit caught in the danger is the reason to stay. Orbit looking at the camera over a still frame reads as a channel ident.

**The Orbit-first test.** Three Shorts built to the 23 Sep version (Orbit looking at the camera at 0 s) are already scheduled: Fri 2 Oct (`Ih2zhZTbIR0`), Mon 5 Oct (the Moon cover Short) and Wed 7 Oct (`pL339HhjDwo`). Let them air as a labelled test. Do not re-edit them. Compare their stayed-to-watch at 48 hours with the world-first Andromeda Shorts (25 Sep–1 Oct). If the Orbit-first Shorts hold more, bring the open back. If not, it stays retired.

The Moon week lines, not to be rewritten:

> The Moon is leaving us.
> Stay here and I will show you what Earth looks like without it.

Picture: Orbit looking up as the Moon drifts back.

Then one hard fact. The film that Short promotes is named on screen around 9–14 seconds. The last 4 seconds return to the opening picture so the Short loops. The end card points at that film.

The spoken Short is 22–27 seconds. The two lines are the opening. They are not stretched into a minute.

Captions cover every line. Studio Related points at the long that Short is promoting, once that film has an id. A Moon Short points at the Moon film. A Neutron Short points at the Neutron film. Do not send the whole week to one long. No new Short pin. No `/go/`. The thumb is the picture, yellow on the hook words and white on the rest. Orbit is not on the thumb.

The voice is Ben Orbit Narrator. The video model does not speak.

## Long hook

The first 30 seconds use the same first sentence, then name the payoff. Why it is happening, what it was like before, and what happens next.

The Moon week line:

> The Moon is leaving us. In this film I will show you why it is drifting, what Earth was like when it was close, and what happens when it is gone.

The first 3 seconds of picture are the danger itself. No title card. Orbit enters on the reaction beats, not in that opening, and not on every shot. Chapter cards use the script’s own act titles. One phone-readable name per beat, so the story still reads with the sound off. Cards are a soft starfield, with about 1.5 seconds of breath and the music still playing.

The end is a moving picture. Music fades. No baked subscribe.

## Packaging

The title is one concrete promise. A higher score does not win if the title is fear or a conspiracy. The description opens on the real subject. Tags are search terms for this film.

- No hashtags in titles. They go in the description.
- Never give a new upload the title of an existing public video, even for a "part 2". Two identical titles compete for the same search and look like a re-upload.
- The long title is the phrase people search, in the question shape that worked (*What Happens When the Last Star Dies?*). Not *Everything you need to know about…*.
- The long thumbnail makes the same promise as its title, in the channel's own lane: wonder, not a threat.
- Longs go out as a normal publish, not a Premiere, until subscribers are in the hundreds.

## Measure (set 24 Sep 2026, runs to 22 Oct)

This strategy holds unchanged for four weeks. No new "locked" strategy doc before 22 Oct. The weekly review asks one question: did stayed-to-watch go up?

- Record stayed-to-watch for every Short in Studio at 48 hours, next to its first frame.
- Aim for more than 45% by mid-October and 60% after that. The 10 Sep channel figure was 31.7%.
- A Short under 35% goes in the log as a note on its first two seconds. It is not re-uploaded or remade.
- Views are the result, not the target. A good week has one Short still getting views on day three.
- A new long is only made on a topic whose Short already cleared 200 views and 40% stayed.
- Nothing already public is re-uploaded, remade or replaced. Fix it before it goes out. The four silent Moon Shorts re-uploaded on 24 Sep got 2–6 views, against 100–290 for the Moon Shorts that went out with a voice.

## Before anything is filmed

Every Short export passes `python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check <mp4> --air-date YYYY-MM-DD` before upload: narrator audible (a silent file fails), no Orbit at 0 s, a different opening frame from the last 14 days, under 40 s. Then watch it once on a phone with the sound on.

A long script scores at least 90. A 22–27 second Short is not padded to chase that long-film score. The reviewer caps a Short this size below 90. QA watches the moving picture. UAT watches the open voiceover. Then it can be uploaded. A live film is not remade by swapping the file.

The locked Monday script is [Only the Moon Can Cover the Sun](MONDAY_MOON_SHORT_ONLY_THE_MOON_CAN_COVER_THE_SUN.md).

## Fill-in for the next film

1. Name the familiar thing and the danger.
2. Write line 1 in 5 to 7 words.
3. Write the stay line.
4. Pick the three films this week’s Shorts will promote. Include past videos that already won, and the new long.
5. Write the long’s first 30 seconds, with the payoff named.
6. Keep the week shape above. Each Short names its own film on screen.
