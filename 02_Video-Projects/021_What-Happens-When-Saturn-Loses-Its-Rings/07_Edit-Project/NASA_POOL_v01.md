# Saturn (021): verified NASA picture pool v01

Built 1 Oct 2026 from images.nasa.gov for shot list v03. There are 153 pictures, each assigned to one script section. **Every ID resolves** on images-api.nasa.gov, and the titles, dates and sizes come from NASA's own metadata.

## How the pool was checked

**Search.** 80 Saturn searches returned 1,552 unique results.

**What was dropped:**
- anything whose title or opening description names a moon, Earth, Mars, a Saturn V rocket or another target;
- anything from MSFC, JSC or KSC (those are Saturn V rockets).

**Looked at by eye** on contact sheets. Also dropped:
- charts, labelled diagrams and split or multi-panel figures;
- thin science strips;
- anything with a moon visible in frame.

## Rules for shot list v03

1. **Use only IDs from this file** for NASA pictures. If a line needs something that isn't here, flag it rather than picking one by hand.
2. **Each ID is used once in the whole film**, with no repeats. The Goddard ring-rain video is used once, as one continuous shot.
3. **A section can borrow** a spare picture from a neighbouring section, but that picture is then gone for good.
4. **Most pictures are about 1020 px square.** On a 16:9 timeline:
   - frame them on black with a slow push of 5–8 %, or crop gently;
   - never upscale past about 1.5x;
   - never stretch, and never slow-mo or freeze-pad to cover length.
5. **Captions must match the picture.** Aurora is not ring rain. The Hubble 1996–2000 sequence shows the rings tilting with the seasons, not thinning. The Grand Finale illustrations are labelled as illustrations.
6. **AI shots are allowed only where already approved:**
   - ice crowd v07 (open);
   - the young-rings shot;
   - bare Saturn v05;
   - Orbit through Omni only, using the canonical still.

   Any new AI shot needs Ben's OK first.
7. **Credits are already in `nasa_pool_v01.json`** (the `credit` field). Each one was copied from that picture's photojournal page on 1 Oct, and `credit_source` links the page. Don't type credits by hand. `check_shot_list.py` writes the credit block for the IDs actually used. PIA05389 was removed because its page gives no credit.
8. **Length.** The VO runs 523.6 s. At 4–6 s per picture, that needs about 95–110 picture rows plus five chapter cards, so 80 rows is too few. Only the last row may run long (the scripted 15–20 s end hold), and it needs a slow push rather than a freeze.
9. **The hook's promises.** "When they were new" sits over the young-rings clip, and "nothing around it at all" sits over bare Saturn v05. Those are planned previews: the hook uses one stretch of each clip, and the later section uses a different stretch. No overlap.
10. **Run `python3 check_shot_list.py shot_list_v03b.csv` before anything goes for review.** It checks:
    - the pool and no repeats;
    - 3.5–6.5 s rows;
    - no gaps;
    - no clip reuse or stretching;
    - aurora and seasons captions;
    - the hook's promises.

    The column layout is at the top of the script. Paste its output with the shot list.

Links:
- Detail page: `https://images.nasa.gov/details/<ID>`
- Full file: `https://images-assets.nasa.gov/image/<ID>/<ID>~orig.jpg`
- `fetch_nasa_pool.py` downloads all of them and builds contact sheets per section.

Section timings come from word counts against the locked 8:43.6 VO, at about one picture per 5 s.


## S1: Open: the rings are falling (~33 s, about 7 pictures)

Approved ice crowd v07 carries the first 3 s. NASA pictures follow as the ice sheet in close-up; none of them shows ice actually falling, so keep the 'falling' claim on the AI open and the VO.

| ID | NASA title | Date | Size | What it shows and why it fits |
|---|---|---|---|---|
| [PIA08247](https://images.nasa.gov/details/PIA08247) | Opposition Surge on the A Ring | 2006-08-21 | 1008x1008 | Bright opposition spot on the A ring, fine ringlets. Ice lit straight on. |
| [PIA08248](https://images.nasa.gov/details/PIA08248) | Opposition Surge on the B Ring | 2006-08-21 | 1008x1008 | Same effect on the B ring, soft grey texture. Pairs with PIA08247 but use only one in the open. |
| [PIA20496](https://images.nasa.gov/details/PIA20496) | Surge in the Ring | 2016-08-29 | 1024x1024 | Ring curve with the bright surge spot, Saturn's limb top right. |
| [PIA08992](https://images.nasa.gov/details/PIA08992) | Surging Across the Rings | 2007-07-26 | 1020x1020 | Rings in front of Saturn's limb, the surge spot moving across. |
| [PIA14629](https://images.nasa.gov/details/PIA14629) | Ever-Changing Ring | 2012-10-08 | 1006x648 | The F ring as one thin bright thread on black. |
| [PIA08963](https://images.nasa.gov/details/PIA08963) | Odd Ring Out | 2007-06-15 | 809x1015 | Thin outer ringlet beside the bright main rings. |

## S2: A thin bright blade, edge-on (~35 s, about 7 pictures)

This is where the pool is strongest. PIA11667 and PIA03158 are big enough to push in slowly.

| ID | NASA title | Date | Size | What it shows and why it fits |
|---|---|---|---|---|
| [PIA11667](https://images.nasa.gov/details/PIA11667) | The Rite of Spring | 2009-09-21 | 7227x3847 | Equinox mosaic, Aug 2009: the rings are almost a line and Saturn is lit side-on. 7227 px wide. The hero picture for 'absurdly thin the other way'. |
| [PIA03158](https://images.nasa.gov/details/PIA03158) | A Change of Seasons on Saturn - October, 1996 | 2001-07-21 | 3000x1500 | Hubble, Oct 1996: rings nearly edge-on across Saturn's middle. |
| [PIA01273](https://images.nasa.gov/details/PIA01273) | Hubble again views Saturn Rings Edge-on | 1998-08-02 | 892x459 | Hubble 1995 ring-plane crossing: rings a hairline. A few moon dots are visible; crop them out or skip this one. |
| [PIA12654](https://images.nasa.gov/details/PIA12654) | Slender Rings | 2010-06-14 | 1016x1016 | Crescent Saturn with the rings as a thin line at the bottom. |
| [PIA20498](https://images.nasa.gov/details/PIA20498) | Barely Bisected Rings | 2016-09-12 | 1020x1020 | Saturn with the rings seen nearly edge-on, 2016. |
| [PIA17156](https://images.nasa.gov/details/PIA17156) | Crescent Saturn | 2014-03-17 | 1016x1016 | Thin crescent; the rings make a dark band below it. |
| [PIA21339](https://images.nasa.gov/details/PIA21339) | Ring-Bow | 2017-07-24 | 1020x1020 | Ring arcs curving round the lit limb. |
| [PIA14943](https://images.nasa.gov/details/PIA14943) | Translucent Arcs | 2018-08-13 | 1933x998 | Colour arcs of the main rings, wide and low-angle. |
| [PIA11563](https://images.nasa.gov/details/PIA11563) | Narrowing Ring Shadow | 2009-08-21 | 1018x1018 | The rings' shadow narrowing on the planet near equinox. |
| [PIA11671](https://images.nasa.gov/details/PIA11671) | Inner B Ring Terminus | 2009-09-21 | 1170x902 | Wide B ring texture at equinox, low sun. |
| [PIA11613](https://images.nasa.gov/details/PIA11613) | Post-Equinox Color | 2009-10-30 | 982x889 | Post-equinox colour: Saturn with the rings as a thin dark band. |
| [PIA08869](https://images.nasa.gov/details/PIA08869) | The Inner Rings | 2007-02-01 | 700x1008 | The inner rings in tight curves, grey. |

## S3: Sunlight on ice; small mass (~41 s, about 8 pictures)

Ring colour and composition. PIA05075 and PIA05076 are Cassini UVIS maps (turquoise means purer ice, red means dirtier), which fits 'dust stains older lanes'.

| ID | NASA title | Date | Size | What it shows and why it fits |
|---|---|---|---|---|
| [PIA06193](https://images.nasa.gov/details/PIA06193) | The Greatest Saturn Portrait ...Yet | 2005-02-24 | 8888x4544 | The great Cassini portrait, 2004: the whole system in true colour. 8888 px. Strong for 'a lot of scenery'. |
| [PIA05075](https://images.nasa.gov/details/PIA05075) | Saturn A Ring From the Inside Out | 2004-07-09 | 2304x1608 | UVIS A ring: turquoise ice and red dirty lanes. The literal 'composition' picture. |
| [PIA05076](https://images.nasa.gov/details/PIA05076) | Saturn C and B Rings From the Inside Out | 2004-07-09 | 2140x1482 | UVIS C and B rings as colour bands, the same idea. |
| [PIA01486](https://images.nasa.gov/details/PIA01486) | Composition Differences within Saturn Rings | 1998-10-30 | 1098x857 | Voyager enhanced colour: orange and blue lanes show composition differences. |
| [PIA07872](https://images.nasa.gov/details/PIA07872) | Small Particles in Saturn Rings | 2005-05-23 | 3200x2400 | Radio occultation map of small particles across the rings, coloured. |
| [PIA07873](https://images.nasa.gov/details/PIA07873) | Radio Occultation: Unraveling Saturn Rings | 2005-05-23 | 3200x2400 | The same radio map with Saturn's disc beside it. |
| [PIA06425](https://images.nasa.gov/details/PIA06425) | Saturn Rings, Cold and Colder | 2004-09-02 | 746x792 | Infrared temperature colours on the rings (CIRS): cold blue and green. |
| [PIA01940](https://images.nasa.gov/details/PIA01940) | Saturn Rings in Infrared | 2006-10-11 | 718x415 | Rings in infrared. Low resolution (718 px), so keep it small or skip it. |
| [PIA17474](https://images.nasa.gov/details/PIA17474) | Jewel of the Solar System | 2013-10-25 | 3600x2700 | 'Jewel of the Solar System', 2013: the whole planet in soft natural colour. 3600 px. |
| [PIA21628](https://images.nasa.gov/details/PIA21628) | Colorful Structure at Fine Scales | 2017-09-07 | 1959x1000 | Fine colour structure in the rings: cream and tan lanes. Literal 'dust warms some lanes'. |
| [GSFC_20171208_Archive_e002157](https://images.nasa.gov/details/GSFC_20171208_Archive_e002157) | Saturn's Rings in Ultraviolet Light | 2017-12-08 | see file | Hubble ultraviolet Saturn: pastel planet, bright rings. Credit: NASA and E. Karkoschka (Univ. of Arizona). |
| [PIA18295](https://images.nasa.gov/details/PIA18295) | Translucent Rings | 2014-12-08 | 1020x1020 | Translucent rings in front of a grey Saturn. |
| [PIA20502](https://images.nasa.gov/details/PIA20502) | View from Above | 2016-10-31 | 1020x1020 | View from above the north pole: rings all round, hexagon on top. |
| [PIA06175](https://images.nasa.gov/details/PIA06175) | Panoramic Rings | 2005-02-11 | 5890x1000 | Panorama strip of the rings, 5890 x 1000. Only works as a slow pan. |
| [PIA00335](https://images.nasa.gov/details/PIA00335) | Full-disk Color Image of Crescent Saturn with Rings and Ring Shadows | 1999-06-19 | 800x550 | Voyager crescent with rings and ring shadows. |
| [PIA02241](https://images.nasa.gov/details/PIA02241) | Saturn Rings | 2000-02-07 | 1760x800 | Voyager: the rings in grey on black. |
| [PIA01969](https://images.nasa.gov/details/PIA01969) | Saturn and its Rings | 1999-05-21 | 894x569 | Voyager, gold Saturn behind the rings. |
| [PIA01966](https://images.nasa.gov/details/PIA01966) | Saturn and its Ring System | 1999-05-06 | 850x820 | Voyager, pink-toned close crop of the rings over the planet. |

## S4: Orbit beat and 'the fall does not stop' (~30 s)

Orbit is Omni only (canonical still). Behind and after him, use S1 or S5 pictures not used elsewhere. NASA has nothing of its own for this beat.


## S5: Ice, not rock: close through the crowd (~44 s, about 9 pictures)

Cassini's ring-grazing close-ups from 2017, the sharpest ring pictures that exist. They are mostly grey, so alternate them with the colour pictures from S3.

| ID | NASA title | Date | Size | What it shows and why it fits |
|---|---|---|---|---|
| [PIA21058](https://images.nasa.gov/details/PIA21058) | Saturn B Ring, Finer Than Ever | 2017-01-30 | 1020x1020 | B ring, finer than ever (2017): dense parallel lanes. |
| [PIA21057](https://images.nasa.gov/details/PIA21057) | Straw in the B Ring Edge | 2017-01-30 | 1020x1020 | 'Straw' texture at the B ring edge: visible clumping. |
| [PIA21059](https://images.nasa.gov/details/PIA21059) | The Propeller Belts in Saturn A Ring | 2017-01-30 | 1020x1020 | Propeller belts in the A ring: fine streaks. |
| [PIA21618](https://images.nasa.gov/details/PIA21618) | Textures in the C Ring | 2017-07-24 | 1024x1024 | Textures in the C ring: broad soft bands. |
| [PIA21619](https://images.nasa.gov/details/PIA21619) | More Textures in the C Ring | 2017-07-24 | 1024x1024 | More C-ring textures, with a bright lane on the left. |
| [PIA11569](https://images.nasa.gov/details/PIA11569) | Behold B Ring Clumps | 2009-08-31 | 1020x1020 | B ring clumps at equinox: diagonal lanes. |
| [PIA23171](https://images.nasa.gov/details/PIA23171) | Texture in the Outer Cassini Division | 2019-06-13 | 1024x1024 | Texture in the outer Cassini Division (2019). |
| [PIA21894](https://images.nasa.gov/details/PIA21894) | Lone Propeller | 2017-09-15 | 1024x1024 | Lone propeller (Sept 2017): flat lanes. |
| [PIA21437](https://images.nasa.gov/details/PIA21437) | Earhart Propeller in Saturn A Ring | 2017-03-30 | 1024x1024 | The 'Earhart' propeller in the A ring. |
| [PIA21448](https://images.nasa.gov/details/PIA21448) | Propeller Belts of Saturn | 2017-05-10 | 1024x1024 | Propeller belts: grainy close-up. |
| [PIA17125](https://images.nasa.gov/details/PIA17125) | Earhart in the A Ring | 2013-08-19 | 1016x1016 | Earhart in the A ring, wider. |
| [PIA11672](https://images.nasa.gov/details/PIA11672) | Giant Propeller in A Ring | 2009-09-21 | 456x432 | Giant propeller in the A ring. Small (456 px), so frame it, don't fill the screen. |
| [PIA02275](https://images.nasa.gov/details/PIA02275) | Saturn Rings - High Resolution | 2000-05-23 | 707x730 | Voyager high-resolution ring curves, spokes visible. |
| [PIA01962](https://images.nasa.gov/details/PIA01962) | High-resolution View of Saturn Rings | 1999-04-25 | 750x825 | Voyager high-resolution ring lanes. |
| [PIA01380](https://images.nasa.gov/details/PIA01380) | A View of Saturn B-ring | 1998-11-17 | 936x724 | Voyager B ring curves. |
| [PIA09805](https://images.nasa.gov/details/PIA09805) | Saturn Outer C Ring | 2008-01-01 | 1020x1020 | Outer C ring curves, grey. |
| [PIA08855](https://images.nasa.gov/details/PIA08855) | Scintillating C Ring | 2007-01-16 | 1020x1020 | Scintillating C ring over the dark planet. |
| [PIA02274](https://images.nasa.gov/details/PIA02274) | Saturn B-ring | 2000-05-23 | 408x539 | Voyager rings, with the planet clipped bottom right. Small (408 px). |

## S5b: The crowd is flat: gaps and edges (part of S5's ~44 s, about 4 pictures)

For 'the gaps are emptier roads'. No shepherd moons are visible in these.

| ID | NASA title | Date | Size | What it shows and why it fits |
|---|---|---|---|---|
| [PIA06092](https://images.nasa.gov/details/PIA06092) | Cassini Captures the Cassini Division | 2004-07-01 | 768x768 | The Cassini Division in close-up (2004). |
| [PIA07616](https://images.nasa.gov/details/PIA07616) | The Cassini Division Edge | 2005-10-26 | 1024x1024 | The Cassini Division edge. |
| [PIA06093](https://images.nasa.gov/details/PIA06093) | Two Waves in One Spectacular Image of Saturn Rings | 2004-07-01 | 768x768 | Two density waves in one picture. |
| [PIA08331](https://images.nasa.gov/details/PIA08331) | New Rings for Cassini Division | 2006-10-11 | 1024x1024 | New ringlets found in the Cassini Division. |
| [PIA12727](https://images.nasa.gov/details/PIA12727) | A-Ring Structures | 2010-09-23 | 1016x1016 | A-ring structures, with a sharp edge into black. |
| [PIA08912](https://images.nasa.gov/details/PIA08912) | A Ring Waves | 2007-04-06 | 1020x1020 | A-ring waves and a clean dark gap. |
| [PIA01953](https://images.nasa.gov/details/PIA01953) | Outer Edge of Saturn A-ring | 1999-04-11 | 765x755 | Voyager: the outer edge of the A ring. |
| [PIA06535](https://images.nasa.gov/details/PIA06535) | Outer B Ring Edge | 2004-12-03 | 1024x1024 | Outer B ring edge: bright curves. |
| [PIA02269](https://images.nasa.gov/details/PIA02269) | Saturn Ring System | 2000-05-23 | 766x771 | Voyager: the ring system curving into black. |
| [PIA02227](https://images.nasa.gov/details/PIA02227) | Two-image Mosaic of Saturn Rings | 1999-12-10 | 1023x1280 | Voyager two-picture mosaic: ring arc beside the planet. |
| [PIA01374](https://images.nasa.gov/details/PIA01374) | Saturn Ring System | 1998-11-13 | 500x500 | Voyager ring system over the planet. Small (500 px). |
| [PIA00534](https://images.nasa.gov/details/PIA00534) | Wide-Angle Image of Saturn Rings | 1997-05-24 | 942x650 | Voyager wide-angle rings: horizontal lanes. |
| [PIA20506](https://images.nasa.gov/details/PIA20506) | Ring Details on Display | 2016-11-07 | 1020x1020 | Ring details: a clean arc. |
| [PIA12766](https://images.nasa.gov/details/PIA12766) | In a Thin Ring | 2011-05-16 | 1002x510 | A thin ring alone on black. |

## S6: Drop through ten metres into open space (~27 s, about 5 pictures)

Rings and atmosphere in one frame. PIA21621 is the closest thing to the scripted 'atmosphere far below'.

| ID | NASA title | Date | Size | What it shows and why it fits |
|---|---|---|---|---|
| [PIA21621](https://images.nasa.gov/details/PIA21621) | Haze on the Horizon | 2017-07-24 | 1011x885 | 'Haze on the Horizon', 2017: Saturn's glowing limb under faint rings. The best match for this beat. |
| [PIA12641](https://images.nasa.gov/details/PIA12641) | Rings Through Atmosphere | 2010-05-26 | 1020x1020 | Rings seen through the edge of the atmosphere. |
| [PIA09908](https://images.nasa.gov/details/PIA09908) | Northward Through the Rings | 2008-05-23 | 508x508 | 'Northward through the rings': rings over the limb. |
| [PIA08844](https://images.nasa.gov/details/PIA08844) | Saturnian Squiggles | 2007-01-01 | 884x1018 | Dark planet with a ring shadow curve. |
| [PIA21886](https://images.nasa.gov/details/PIA21886) | Cassini's 'Inside-Out' Rings | 2017-08-25 | 630x630 | 'Inside-out rings' (2017 Grand Finale view from under the rings). |
| [PIA17185](https://images.nasa.gov/details/PIA17185) | Glare on the Window | 2018-03-05 | 1010x1013 | Rings and limb in blue-grey: 'Glare on the Window'. |
| [PIA12557](https://images.nasa.gov/details/PIA12557) | Saturn Bright Through Rings | 2010-02-25 | 762x762 | Saturn bright through the rings. |
| [PIA14623](https://images.nasa.gov/details/PIA14623) | Night Side Rings | 2012-08-27 | 1005x994 | The rings' night side, cut by the planet's shadow. |
| [PIA18367](https://images.nasa.gov/details/PIA18367) | Criss-Crossed Rings | 2016-04-25 | 1020x1020 | Criss-crossed rings over the planet. |

## S7: Magnetic ring rain, Keck (~54 s, about 11 pictures)

PIA16842 is NASA's own illustration of the 2013 Keck ring-rain discovery (charged water flowing from the rings into the atmosphere). It is the only literal ring-rain picture. The aurora pictures show Saturn's magnetic field meeting the atmosphere, so use them for 'Saturn's magnetic field already threads the ring plane' and never caption them as rain. Keck itself: NASA has no picture of the telescope; any Keck image is a W. M. Keck Observatory licence, so leave it out unless Ben clears it. The Goddard ring-rain video can be used once, as one continuous shot, not sliced.

| ID | NASA title | Date | Size | What it shows and why it fits |
|---|---|---|---|---|
| [PIA16842](https://images.nasa.gov/details/PIA16842) | Saturn Ring Rain Artist Concept | 2013-04-10 | 4465x4115 | Artist concept of ring rain: charged water flowing from the rings into the atmosphere. 4465 px. The hero picture for this section. |
| [PIA13697](https://images.nasa.gov/details/PIA13697) | Saturn Hot Plasma Explosions | 2010-12-14 | 641x359 | Animation still: Saturn's magnetic field lines bending over the ring plane. Literal 'magnetic paths'. |
| [PIA13402](https://images.nasa.gov/details/PIA13402) | Glowing Southern Lights | 2010-09-23 | 2560x1600 | Infrared false colour: blue rings, red planet, green aurora at the pole. Magnetic field into atmosphere. |
| [PIA13404](https://images.nasa.gov/details/PIA13404) | Dancing Southern Lights of Saturn | 2010-09-23 | 640x481 | Green aurora above red and violet bands. |
| [PIA11396](https://images.nasa.gov/details/PIA11396) | Saturn Polar Aurora | 2008-11-12 | 1400x1127 | Infrared aurora ring around the pole (VIMS). |
| [PIA09185](https://images.nasa.gov/details/PIA09185) | Saturn North Pole Hexagon and Aurora | 2007-03-27 | 448x448 | Aurora over the north-pole hexagon, infrared. |
| [PIA17900](https://images.nasa.gov/details/PIA17900) | Dance of Saturn Auroras | 2014-02-11 | 878x720 | Hubble ultraviolet aurora oval, blue. |
| [PIA17668](https://images.nasa.gov/details/PIA17668) | Saturn Colorful Aurora | 2014-02-11 | 1501x943 | Colourful aurora at the limb (VIMS). |
| [PIA01269](https://images.nasa.gov/details/PIA01269) | Hubble Provides Clear Images of Saturn Aurora | 1998-08-02 | 819x900 | Hubble 1998 aurora. It has a caption bar, so crop that off. |
| [PIA21899](https://images.nasa.gov/details/PIA21899) | Polar Lights at Saturn Bid Cassini Farewell | 2017-10-16 | 450x450 | Cassini's last aurora view, ultraviolet, 14 Sept 2017. It has latitude lines, so frame it as data. |

## S8: Cassini's Grand Finale; then the 100–300 million year range (~48 s, about 10 pictures)

The real Grand Finale pictures. The four NASA illustrations are wide (3000 x 1266), so they suit 16:9. Only PIA21895 and PIA21896 are from the final day; caption them that way only if the VO is on the final plunge.

| ID | NASA title | Date | Size | What it shows and why it fits |
|---|---|---|---|---|
| [PIA21439](https://images.nasa.gov/details/PIA21439) | Cassini Grand Finale Dive Illustration | 2017-04-04 | 3000x1266 | Illustration: Cassini diving between the rings and the planet. |
| [PIA22767](https://images.nasa.gov/details/PIA22767) | Grand Finale: Cassini in the Gap (Illustration) | 2018-10-02 | 3000x1266 | Illustration: Cassini in the gap, above the cloud tops. |
| [PIA21440](https://images.nasa.gov/details/PIA21440) | Cassini versus Saturn Illustration | 2017-04-04 | 3000x1266 | Illustration: Cassini over the atmosphere, rings behind. |
| [PIA22766](https://images.nasa.gov/details/PIA22766) | Cassini orbiting Saturn (Illustration) | 2018-10-02 | 3000x1266 | Illustration: Cassini orbiting Saturn, sun flare at the limb. |
| [PIA22768](https://images.nasa.gov/details/PIA22768) | Grand Finale: One of Cassini's Last Dives (Illustration) | 2018-10-03 | 2550x3300 | Illustration: one of the last dives (portrait 2550 x 3300, so crop to 16:9). |
| [PIA21345](https://images.nasa.gov/details/PIA21345) | So Far from Home | 2017-09-11 | 3545x1834 | 'So Far from Home': one of Cassini's last looks at Saturn and the main rings from a distance, Sept 2017. 3545 px. |
| [PIA21892](https://images.nasa.gov/details/PIA21892) | Saturn: Before the Plunge | 2017-09-15 | 1009x1012 | 'Saturn: Before the Plunge', 13 Sept 2017: crescent limb, among Cassini's last pictures. |
| [PIA21895](https://images.nasa.gov/details/PIA21895) | Impact Site: Cassini's Final Image | 2017-09-15 | 505x508 | The last picture Cassini's cameras took: the night side where it would enter hours later, lit by ringshine. |
| [PIA21896](https://images.nasa.gov/details/PIA21896) | Impact Site: Infrared Image | 2017-09-15 | 1000x550 | The impact site in infrared, red. 1000 x 550. |
| [PIA21343](https://images.nasa.gov/details/PIA21343) | Top of the World | 2017-08-28 | 1024x1024 | 'Top of the World': the north pole on 26 Apr 2017, the day the Grand Finale began. |
| [PIA21351](https://images.nasa.gov/details/PIA21351) | The North | 2017-10-30 | 1020x1020 | The hexagon from the last weeks. |
| [PIA21350](https://images.nasa.gov/details/PIA21350) | Goodbye to the Dark Side | 2017-10-02 | 1020x1020 | 'Goodbye to the Dark Side': rings over the dark limb. |
| [PIA21356](https://images.nasa.gov/details/PIA21356) | So Long, C Ring | 2017-11-13 | 1020x1020 | 'So Long, C Ring': flat ring lanes. |
| [PIA21903](https://images.nasa.gov/details/PIA21903) | Final Frontier | 2018-02-19 | 1135x396 | 'Final Frontier': wide shot of the limb, 1135 x 396 (panoramic). |
| [PIA21047](https://images.nasa.gov/details/PIA21047) | Staring at Saturn | 2016-09-15 | 1441x1173 | 'Staring at Saturn', 2016: full disc in colour. |
| [PIA08990](https://images.nasa.gov/details/PIA08990) | D-Ring Structure | 2007-07-24 | 1024x1024 | D ring structure: faint lanes. This is the ring the inflow comes from. |
| [PIA17150](https://images.nasa.gov/details/PIA17150) | Dusty D Ring | 2014-02-24 | 1020x1020 | 'Dusty D Ring' beside the planet's limb. |
| [PIA18313](https://images.nasa.gov/details/PIA18313) | Faint D Ring | 2015-04-27 | 1020x1020 | Faint D ring under the bright C ring. |
| [PIA18321](https://images.nasa.gov/details/PIA18321) | Spirals in the D Ring | 2015-06-29 | 1020x1020 | Spirals in the D ring. |
| [PIA01388](https://images.nasa.gov/details/PIA01388) | Saturn Faint Inner D-ring | 1999-01-05 | 460x724 | Voyager: the faint inner D ring. Small, so frame it. |

## S9: Slow thinning over deep time (~21 s, about 4 pictures)

Hubble 1996–2000 sequence: the rings open year by year as Saturn's seasons turn. That is tilt, not thinning, so use it as 'watch for an age' and never as proof of loss. Pick at most two of the five; the rest are spare.

| ID | NASA title | Date | Size | What it shows and why it fits |
|---|---|---|---|---|
| [PIA03156](https://images.nasa.gov/details/PIA03156) | A Change of Seasons on Saturn | 2001-07-21 | 3000x2270 | Montage of five Hubble Saturns 1996–2000, rings opening. |
| [PIA03159](https://images.nasa.gov/details/PIA03159) | A Change of Seasons on Saturn - October, 1997 | 2001-07-21 | 1152x576 | Hubble Oct 1997. |
| [PIA03160](https://images.nasa.gov/details/PIA03160) | A Change of Seasons on Saturn - October, 1998 | 2001-07-21 | 3000x1500 | Hubble Oct 1998. |
| [PIA03161](https://images.nasa.gov/details/PIA03161) | A Change of Seasons on Saturn - October, 1999 | 2001-07-21 | 3000x1500 | Hubble Oct 1999. |
| [PIA03162](https://images.nasa.gov/details/PIA03162) | A Change of Seasons on Saturn - October, 2000 | 2001-07-21 | 3000x1500 | Hubble Oct 2000: rings wide open. |
| [PIA08850](https://images.nasa.gov/details/PIA08850) | The Vanishing Rings | 2007-01-09 | 1008x1008 | 'The Vanishing Rings': ring shadow and planet, grey. |
| [PIA08265](https://images.nasa.gov/details/PIA08265) | Saturn Hides the Rings | 2006-09-12 | 1020x1020 | 'Saturn Hides the Rings': planet in front of the rings. |
| [PIA11141](https://images.nasa.gov/details/PIA11141) | Saturn … Four Years On | 2008-12-30 | 4613x2233 | 'Saturn … Four Years On', 2008: full disc, 4613 px. |

## S10: When the rings were new (~65 s, about 13 pictures)

The approved young-rings AI shot carries the 'whiter, wider' picture. NASA can only show today's rings at their brightest. This section is short on NASA pictures; fill it from the spares in S3, S5 and S5b, never by reusing a shot.

| ID | NASA title | Date | Size | What it shows and why it fits |
|---|---|---|---|---|
| [PIA10081](https://images.nasa.gov/details/PIA10081) | Saturn Recycling Rings | 2007-12-12 | 3587x3002 | 'Saturn Recycling Rings' artist concept (2007): blue-white ice clumps in a ring, Saturn's limb behind. Its message is that clumps break up and re-form, which fits 'a few argue the rings could still be old'. If it is used in S5 instead, use it there only. |
| [PIA17176](https://images.nasa.gov/details/PIA17176) | Tis the Season | 2013-12-23 | 1009x1009 | Crescent Saturn in colour with rings, 2013. |
| [PIA18278](https://images.nasa.gov/details/PIA18278) | Ring King | 2014-08-18 | 1020x1020 | 'Ring King': the whole system from above, hexagon on top. |
| [PIA18274](https://images.nasa.gov/details/PIA18274) | Vortex and Rings | 2014-07-07 | 1021x944 | Vortex and rings from above. |
| [PIA20497](https://images.nasa.gov/details/PIA20497) | A Dark Bend | 2016-09-05 | 1024x1024 | 'A Dark Bend': ring edge and a shadow line. |
| [PIA22418](https://images.nasa.gov/details/PIA22418) | Gravity's Rainbow | 2018-04-23 | 1016x1013 | 'Gravity's Rainbow': ring colours, shot Aug 2009. NASA's caption says the rings are mostly water ice and the cause of their colour is still debated. |
| [PIA18301](https://images.nasa.gov/details/PIA18301) | Study in Scarlet | 2015-02-09 | 1024x1024 | 'Study in Scarlet': bright ring curves. |
| [PIA18294](https://images.nasa.gov/details/PIA18294) | Darkness | 2014-12-22 | 839x811 | 'Darkness': crescent and thin ring arc. |

## S11: Roche rubble: an idea (~24 s, about 5 pictures)

The script labels this as an idea. NASA has no picture of a moon breaking up. Use F-ring clumps and streamers as 'rubble in a plane', plus a labelled AI shot if Ben approves one.

| ID | NASA title | Date | Size | What it shows and why it fits |
|---|---|---|---|---|
| [PIA12785](https://images.nasa.gov/details/PIA12785) | F Ring Bright Core Clumps | 2010-07-20 | 2100x1000 | F ring bright core clumps: a jagged line of lumps. |
| [PIA12786](https://images.nasa.gov/details/PIA12786) | Fan in the F Ring | 2010-07-20 | 2100x1000 | Fan in the F ring: streamers off the core. |
| [PIA08903](https://images.nasa.gov/details/PIA08903) | F Ring Strands | 2007-03-23 | 872x329 | F-ring strands on black. |
| [PIA17148](https://images.nasa.gov/details/PIA17148) | Splitting the F Ring | 2014-02-10 | 1016x1016 | 'Splitting the F Ring': the ring beside the main rings. |
| [PIA06098](https://images.nasa.gov/details/PIA06098) | Wide View of Saturn F Ring | 2004-07-01 | 1024x1024 | Wide F ring arc on black (2004). |
| [PIA18277](https://images.nasa.gov/details/PIA18277) | Clumpy Ringlets | 2014-08-25 | 1020x1020 | Clumpy ringlets in the Encke gap. |

## S12: Saturn without them (~51 s, about 10 pictures)

The approved bare-Saturn Veo v05 and the Omni Orbit shot carry 'empty space where the sheet was'. NASA pictures with the rings near edge-on or out of frame make Saturn read as almost bare. Bands and the hexagon fit 'pale gold bands, a fast day'.

| ID | NASA title | Date | Size | What it shows and why it fits |
|---|---|---|---|---|
| [PIA21334](https://images.nasa.gov/details/PIA21334) | Saturnian Dawn | 2017-06-26 | 1020x1020 | 'Saturnian Dawn': lit limb, rings a faint line. |
| [PIA21337](https://images.nasa.gov/details/PIA21337) | Good Old Summer Time | 2017-07-31 | 1020x1020 | 'Good Old Summer Time': the north pole cap, rings out of frame. |
| [PIA20507](https://images.nasa.gov/details/PIA20507) | Saturn Watercolor Swirls | 2016-11-14 | 1020x1020 | Watercolour swirls: the pole and limb, no rings. |
| [PIA20530](https://images.nasa.gov/details/PIA20530) | Sliver of Saturn | 2017-04-03 | 1020x1020 | 'Sliver of Saturn': crescent with a thin ring line. |
| [PIA12633](https://images.nasa.gov/details/PIA12633) | Saturn Silhouette | 2010-05-14 | 1020x1020 | 'Saturn Silhouette': thin crescent, rings a line at the bottom. |
| [PIA12677](https://images.nasa.gov/details/PIA12677) | Quarter Saturn | 2010-07-15 | 1016x994 | 'Quarter Saturn': half disc, the rings a line through the middle. |
| [PIA17127](https://images.nasa.gov/details/PIA17127) | Impressionistic Saturn | 2013-11-18 | 1020x1020 | Impressionistic Saturn: dark limb and lit edge. |
| [PIA18314](https://images.nasa.gov/details/PIA18314) | Serene Saturn | 2015-05-11 | 1024x1024 | 'Serene Saturn': planet and rings from above. |
| [PIA21327](https://images.nasa.gov/details/PIA21327) | Hail the Hexagon | 2017-05-08 | 1020x1020 | 'Hail the Hexagon': the hexagon at the top. |
| [PIA14945](https://images.nasa.gov/details/PIA14945) | Spring at the North Pole | 2013-04-29 | 745x745 | The hexagon in natural colour, close up. |
| [PIA17652](https://images.nasa.gov/details/PIA17652) | In Full View: Saturn Streaming Hexagon | 2013-12-04 | 1024x1024 | The hexagon in false colour: purple and pink, strong. |
| [PIA14646](https://images.nasa.gov/details/PIA14646) | Hexagon and Rings | 2013-02-04 | 1016x1016 | Hexagon and rings, grey. |
| [PIA21052](https://images.nasa.gov/details/PIA21052) | Over Saturn Turbulent North | 2016-12-06 | 1024x1024 | Over the turbulent north: storms, no rings. |
| [PIA21888](https://images.nasa.gov/details/PIA21888) | Dreamy Swirls on Saturn | 2017-09-12 | 974x908 | Dreamy swirls: cloud bands only, cream. Literal 'soft stripes'. |
| [PIA20528](https://images.nasa.gov/details/PIA20528) | Watercolor World | 2017-04-17 | 1024x1024 | 'Watercolor World': the limb and its bands. |
| [PIA21341](https://images.nasa.gov/details/PIA21341) | Cloudy Waves (False Color) | 2017-08-14 | 985x998 | Cloud waves, false colour. |
| [PIA18290](https://images.nasa.gov/details/PIA18290) | Mixing Paints | 2014-11-17 | 1020x1020 | 'Mixing Paints': bands and swirls, grey. |
| [PIA18280](https://images.nasa.gov/details/PIA18280) | Painted Saturn | 2014-09-29 | 1024x1024 | 'Painted Saturn': the full disc from above. |
| [PIA18311](https://images.nasa.gov/details/PIA18311) | Swirls and Shadows | 2015-05-04 | 1022x1022 | Swirls and shadows: ring shadow across the bands. |
| [PIA21046](https://images.nasa.gov/details/PIA21046) | Saturn, Approaching Northern Summer | 2016-09-15 | 2012x1024 | Saturn approaching northern summer, full colour, 2012 px wide. |
| [PIA08304](https://images.nasa.gov/details/PIA08304) | Golden Night on Saturn | 2006-11-07 | 1020x1020 | 'Golden Night on Saturn': golden rings over the dark side. |
| [PIA12590](https://images.nasa.gov/details/PIA12590) | Shadow and Ringshine | 2010-03-16 | 853x813 | 'Shadow and Ringshine': rings in sharp blades over the dark limb. |
| [PIA10476](https://images.nasa.gov/details/PIA10476) | Saturn by Ringshine | 2008-09-24 | 1017x978 | 'Saturn by Ringshine': the dark side lit by the rings. |

## S13: Recap and end hold (~45 s plus a 15–20 s hold, about 9 pictures)

PIA17218 is Cassini's last full mosaic of Saturn and the rings, shot two days before the plunge. It is 6000 x 2500, so it can be the end hold with a slow push. If Ben keeps the scripted callback to the opening shot, that is a deliberate return, not reuse, but say so in the cut notes.

| ID | NASA title | Date | Size | What it shows and why it fits |
|---|---|---|---|---|
| [PIA17218](https://images.nasa.gov/details/PIA17218) | A Farewell to Saturn | 2017-11-21 | 6000x2500 | 'A Farewell to Saturn': Cassini's last full mosaic of Saturn and the rings, two days before the plunge. 6000 x 2500. The end-hold picture. |

## Gaps the pool cannot fill

- **Ice actually falling into Saturn.** No NASA photo exists. Use PIA16842 (illustration), the approved AI open, and the Goddard video once.
- **Keck telescope.** No NASA image. Any Keck picture is a W. M. Keck Observatory licence and needs Ben's OK.
- **A moon breaking up (Roche).** No NASA image. Use F-ring rubble, or a labelled AI shot with Ben's OK.
- **Young, whiter rings.** These exist only as the approved AI shot. S10 is long (about 65 s), so it borrows spares from S3, S5 and S5b.
