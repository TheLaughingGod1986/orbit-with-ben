# J3219: do the three December titles use the search queries? (macbook, 20 Nov 2026)

Part 2 of what the Chief left on J3219 (20 Nov 11:11Z). Read from the repo only. Nothing was changed: no manifest, no listing, nothing on YouTube. Spend: £0, 0 vidIQ credits.

The search numbers are the Chief's vidIQ pass of 20 Nov (monthly searches / competition, lower is easier). They were not re-read here.

| Film | Goes public | Title now | Query to carry | In the title? | Proposal |
|---|---|---|---|---|---|
| Sleep film (`_sleep_video_01`, `13q4_EoLEN4`, uploaded, private) | Sat 12 Dec 21:00 | Space Documentary for Sleep: A Slow Journey From the Moon to Andromeda | 'documentary for sleep' 123k/44; 'fall asleep documentary' 35k/35 | **Yes.** 'Documentary for Sleep' is there word for word, at the front, after 'Space' (which also makes 'space documentary', 460k/57) | **No change.** |
| 034 Pluto (not uploaded yet; package dry-run only) | Sun 13 Dec 18:00 | Why Pluto's Frozen Heart Has Zero Craters | 'pluto planet' 20k/43, up 76% | **No.** 'Pluto' is the second word and 'planet' is not in the title | **Change proposed**, below |
| 064 Every planet (script stage; no upload package yet) | Wed 16 Dec 18:00 | Every Planet Explained in 10 Minutes (Mercury to Neptune) | 'planet size comparison' 29k/50; 'solar system' 333k/68 (crowded) | **No.** Neither phrase is in the title | **Small change proposed**, below |

## The one-line proposals for Ben

1. **Pluto (13 Dec):** change the title to **"Pluto the Dwarf Planet: Why Its Frozen Heart Has Zero Craters"** (61 characters), so it starts with the words people type ('pluto planet', 20k searches a month and rising). OK?
2. **Every planet (16 Dec):** keep the front and swap the bracket: **"Every Planet Explained in 10 Minutes (The Whole Solar System)"** (61 characters), so 'solar system' is in the title. OK?
3. **Sleep film (12 Dec):** no change needed.

## Notes behind each line

**Sleep film.** The title already leads with the bigger of its two queries. The smaller one, 'fall asleep documentary', is not in the title, and its exact words are not in the description or the tags either (the tags have 'fall asleep to space', 'facts to fall asleep to' and 'sleep documentary'). The held B and C titles both carry 'Fall Asleep'. A cheap extra that needs no title change: add the tag 'fall asleep documentary' and use the words 'fall asleep' once in the description's first lines. That is a listing edit on a scheduled video, so it is the Chief's call, not done here.

**Pluto.**
- LEARNINGS rule 26 already asks for this shape: the plain search phrase first, then the stakes.
- The proposed wording says 'dwarf planet', not 'planet', so the title stays true. The bare phrase 'Pluto Planet: ...' would match the query exactly but reads oddly and calls Pluto a planet.
- It is 61 characters. Rule 26 allows 70; rule 15's 50-character target is passed, as it is for every search-first title.
- A shorter option if the Chief prefers: "Pluto, the Dwarf Planet With a Heart That Has Zero Craters" (58).
- Timing matters. The film is not uploaded yet, so today this is a one-line edit to `11_Upload-Package/PACKAGE_MANIFEST.json` (`title`, and slot 1 of `titleAbc`). The manifest lists a four-title Test & Compare. Under "title first, test second", the search-led title must be side A before that test is armed, because a set test cannot be edited afterwards.
- The description's first line already opens "Why does Pluto have a heart" and the film's tags were not checked for 'pluto planet' beyond a grep that found no 'pluto planet' or 'dwarf planet' tag. Adding both tags is free.

**Every planet.**
- The current front, 'Every Planet Explained', was the number 1 YouTube autocomplete for this topic in the J2875 review, so the front stays as it is. Only the bracket changes.
- 'solar system' is a crowded query (competition 68). The film will not rank for it alone, but the words help it sit beside the big solar-system videos in Suggested, which is where the J2875 neighbours are.
- 'planet size comparison' (29k/50) should not go in the title: the film is a tour, not a size comparison, and the title would promise something the film does not deliver. If the locked script has a size-comparison graphic, the phrase can go in the description and tags.
- An alternative that puts both in the front, at the cost of breaking the exact autocomplete phrase: "Every Planet in the Solar System Explained in 10 Minutes" (56). Not recommended for that reason.
- No upload package exists yet, so the change is to `status.json` `title` and the listing when it is written (J3023).

## Not done in this run

Part 1 (the top-10 results check for 'space mysteries', 'milky way' and 'andromeda galaxy', then the script, SOURCES.md and packaging brief for the winner) needs web access. WebSearch is refused in this lane (tested once, 20 Nov), and the vidIQ search tool costs credits that no written rule covers past the 25 already used. Nothing was drafted from memory.
