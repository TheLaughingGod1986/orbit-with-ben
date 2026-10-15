# Gemini Quote Pass (v01) — What Happens When Earth's Magnetic Field Flips? (031)

- **Job:** J0318
- **Model:** Gemini (`gemini-4-argon-high`)
- **Date:** 15 Oct 2026
- **Target:** `02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/01_Script/SOURCES.md` (19 rows)

---

## Row 1

- **Claim:** The north magnetic pole has been racing from Canada across the Arctic toward Siberia at up to about 50–55 km a year (faster than a marathon every year, 42.195 km).
- **Must quote:** Yes (`DATA`, `SCALE`, `WHEN`)
- **URLs opened:**
  - `https://www.ncei.noaa.gov/products/world-magnetic-model` (named)
  - `https://www.bgs.ac.uk/discovering-geology/earth-hazards/geomagnetism/` (named — returned HTTP 404)
  - `https://www.ncei.noaa.gov/products/wandering-geomagnetic-poles` (linked from NOAA WMM page)
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Magnetic_north_and_the_elongating_blob` (extra)
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` (extra)
- **Verdict:** PARTIAL
- **Verbatim quotes:**
  - `https://www.ncei.noaa.gov/products/world-magnetic-model` : `"The World Magnetic Model (WMM) is the standard model for navigation, attitude, and heading referencing systems that use the geomagnetic field."`
  - `https://www.ncei.noaa.gov/products/wandering-geomagnetic-poles` : `"In 1831, James Clark Ross located the north dip pole position in northern Canada. Natural Resources Canada (NRCan) tracked the North Magnetic Pole, which is slowly drifting across the Canadian Arctic, by periodically carrying out magnetic surveys to reestablish the Pole's location from 1948 to 1994."`
  - `https://www.ncei.noaa.gov/products/wandering-geomagnetic-poles` : `"The most recent survey determined that the Pole is moving approximately north-northwest at 55km per year."`
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Magnetic_north_and_the_elongating_blob` : `"Unlike our geographic north pole, which is in a fixed location, magnetic north wanders. This has been known since it was first measured in 1831, and subsequently mapped drifting slowly from the Canadian Arctic towards Siberia. However, since the 1990s, this drift has turned into more of a sprint – going from its historic wandering of 0–15 km a year to its present speed of 50–60 km a year."`
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` : `"The position of Earth’s magnetic north pole was first precisely located in 1831. Since then, it’s gradually drifted north-northwest by more than 600 miles (1,100 kilometers), and its forward speed has increased from about 10 miles (16 kilometers) per year to about 34 miles (55 kilometers) per year."`
- **Anything the page does not say / notes:**
  - The named BGS URL `https://www.bgs.ac.uk/discovering-geology/earth-hazards/geomagnetism/` returns HTTP 404, and the named NOAA WMM overview page `https://www.ncei.noaa.gov/products/world-magnetic-model` does not itself state `"from Canada across the Arctic toward Siberia at up to about 50–55 km a year"`; those details are on the linked NOAA subpage `https://www.ncei.noaa.gov/products/wandering-geomagnetic-poles`, ESA Swarm, and NASA Science.
  - `"faster than a marathon every year, 42.195 km"` is our own comparison based on the quoted `50–60 km a year` / `55km per year`.

---

## Row 2

- **Claim:** Life on Earth has survived hundreds of magnetic flips; the fossil record shows no correlation between geomagnetic reversals and mass extinctions.
- **Must quote:** Yes (`FACT`)
- **URLs opened:**
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` (named)
  - `https://www.usgs.gov/faqs/do-earths-magnetic-poles-flip` (named — returned HTTP 202 empty body / AWS WAF challenge)
  - `https://geomag.bgs.ac.uk/education/reversals.html` (extra)
- **Verdict:** OK
- **Verbatim quotes:**
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` : `"Paleomagnetic records tell us Earth’s magnetic poles have reversed 183 times in the last 83 million years, and at least several hundred times in the past 160 million years."`
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` : `"Plant and animal fossils from the period of the last major pole reversal don’t show any big changes. Deep ocean sediment samples indicate glacial activity was stable. In fact, geologic and fossil records from previous reversals show nothing remarkable, such as doomsday events or major extinctions."`
  - `https://geomag.bgs.ac.uk/education/reversals.html` : `"Similarly, reversal patterns do not match patterns in species extinction during geological history."`
- **Anything the page does not say / notes:**
  - None; all elements of the claim are supported verbatim on the named NASA Science page (and corroborated on BGS `reversals.html`).

---

## Row 3

- **Claim:** In August 1905 (published 1906), French physicist Bernard Brunhes (1867–1910) found ancient lava and baked clay at Pontfarein, central France, magnetised in the opposite direction to today's field.
- **Must quote:** Yes (`WHO`, `WHEN`, `FACT`)
- **URLs opened:**
  - `https://api.archives-ouvertes.fr/search/?q=jpa-00241149&fl=title_s,abstract_s,uri_s,files_s,producedDate_s,authFullName_s,journalTitle_s,volume_s,page_s` (public HAL bibliographic API for Brunhes 1906, `doi:10.1051/jphystap:019060050070500`; `hal.science` full PDF blocked by Anubis challenge, no public abstract)
  - `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1051/jphystap:019060050070500?fields=title,abstract,year,authors,openAccessPdf` (public metadata record for Brunhes 1906; no abstract)
  - `https://api.openalex.org/works/https://doi.org/10.1016/B978-044452748-6.00095-X` (public metadata record for Laj & Channell 2007, *Treatise on Geophysics* vol. 5; closed access, no public abstract)
  - `https://eos.org/articles/centenary-discovery-earths-magnetic-field-reversals` (extra — Kornprobst & Lénat 2014, *Eos* 95(44), 401)
  - `https://en.wikipedia.org/wiki/Bernard_Brunhes` (extra)
- **Verdict:** PARTIAL
- **Verbatim quotes:**
  - `https://api.archives-ouvertes.fr/search/?q=jpa-00241149&fl=title_s,abstract_s,uri_s,files_s,producedDate_s,authFullName_s,journalTitle_s,volume_s,page_s` : `"authFullName_s":["Bernard Brunhes"], "title_s":["Recherches sur la direction d'aimantation des roches volcaniques"], "journalTitle_s":"J. Phys. Theor. Appl.", "volume_s":"5", "page_s":"705-724", "producedDate_s":"1906", "abstract_s":["Pas de Résumé disponible"]`
  - `https://eos.org/articles/centenary-discovery-earths-magnetic-field-reversals` : `"The inscription reads “Bernard Brunhes (1867–1910). Director of the Puy de Dôme Observatory from 1900 to 1910. Bernard Brunhes discovered in 1906 the inversions of the Earth’s magnetic field."`
  - `https://eos.org/articles/centenary-discovery-earths-magnetic-field-reversals` : `"In the early years of the 20th century, physicist Bernard Brunhes, then director of the Geophysical Observatory of Puy de Dôme (now Observatoire de Physique du Globe de Clermont), measured for the first time reverse magnetization in samples from a basaltic lava flow and from the underlying backed argillaceous sediments from the village of Pontfarein (now Pont Farin) in the Cantal volcanic district (Auvergne, France). He correctly interpreted this observation as a consequence of the inversion of Earth’s magnetic field in the past [Brunhes, 1905a, 1905b and 1906]."`
  - `https://en.wikipedia.org/wiki/Bernard_Brunhes` : `"Antoine Joseph Bernard Brunhes (3 July 1867 – 10 May 1910) was a French geophysicist known for his pioneering work in paleomagnetism, in particular, his 1906 discovery of geomagnetic reversal."`
  - `https://en.wikipedia.org/wiki/Bernard_Brunhes` : `"In 1905, he found that rocks in an ancient lava flow at Pontfarin in the commune of Cézens (part of the Cantal département) were magnetised in a direction almost opposite to that of the present-day magnetic field."`
- **Anything the page does not say / notes:**
  - The month `"August"` (in `"August 1905"`) is not on the opened pages (which confirm `1905`, `1906`, `Bernard Brunhes (1867–1910)`, `French geophysicist` / `physicist`, `basaltic lava flow` and `underlying backed argillaceous sediments` at `Pontfarein` in Auvergne/Cantal, France, and reverse magnetisation).

---

## Row 4

- **Claim:** In 1929, Japanese geophysicist Motonori Matuyama (1884–1958) tested Quaternary volcanic rocks across Japan and Manchuria and showed that rocks older than about 780,000 years (early Pleistocene) were consistently reversed.
- **Must quote:** Yes (`WHO`, `WHEN`)
- **URLs opened:**
  - `https://doi.org/10.2183/pjab1912.5.203` (named — resolved to `https://www.jstage.jst.go.jp/article/pjab1912/5/5/5_5_203/_article/-char/en` and full open-access PDF `https://www.jstage.jst.go.jp/article/pjab1912/5/5/5_5_203/_pdf/-char/en`)
  - `https://en.wikipedia.org/wiki/Motonori_Matuyama` (extra)
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` (extra)
- **Verdict:** PARTIAL
- **Verbatim quotes:**
  - `https://www.jstage.jst.go.jp/article/pjab1912/5/5/5_5_203/_pdf/-char/en` : `"68. On the Direction of Magnetisation of Basalt in Japan, Tyôsen and Manchuria. By Motonori MATUYAMA. Kyoto Imperial University. (Rec. April 13, 1929. Comm. by T. TERADA, M.I.A., May 12, 1929.)"`
  - `https://www.jstage.jst.go.jp/article/pjab1912/5/5/5_5_203/_pdf/-char/en` : `"Since that time 139 specimens of basalt were collected from 36 places in Honsyû, Kyûsyû, Tyôsen and Manchuria, of which 38 specimens were already examined more accurately."`
  - `https://www.jstage.jst.go.jp/article/pjab1912/5/5/5_5_203/_pdf/-char/en` : `"There is a group of specimens, including that from Yakuno, whose directions of magnetisation falls around the present earth's field. A number of other specimens, including that from Genbudô, forms another group almost exactly antipodal to the former."`
  - `https://www.jstage.jst.go.jp/article/pjab1912/5/5/5_5_203/_pdf/-char/en` : `"One of the specimens from Kissyû, Tyôsen, is reported to be of Pleistcene2) while the other is definitely older, since it is surrounded and a part covered by the first. Thus we may consider that in the earlier part of the Quarternary period the earth's magnetic field in the area under consideration was probably in the state represented by the second group, which gradually changed to the state represented by the first group."`
  - `https://en.wikipedia.org/wiki/Motonori_Matuyama` : `"Motonori Matsuyama (松山 基範, Matsuyama Motonori; October 25, 1884 – January 27, 1958) was a Japanese geophysicist who was (in the late 1920s) the first to provide systematic evidence that the Earth's magnetic field had been reversed in the early Pleistocene and to suggest that long periods existed in the past in which the polarity was reversed."`
  - `https://en.wikipedia.org/wiki/Motonori_Matuyama` : `"The transition, about 0.78 Ma, to normal polarity (i.e., that of the present Earth's field) is the Brunhes-Matuyama or Matuyama-Brunhes reversal."`
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` : `"with the last one taking place about 780,000 years ago."`
- **Anything the page does not say / notes:**
  - The named 1929 paper (`https://doi.org/10.2183/pjab1912.5.203`) does not contain Matuyama's life years `"(1884–1958)"` or the modern radiometric age `"about 780,000 years"` (in 1929 Matuyama wrote `"Pleistcene"` and `"the earlier part of the Quarternary period"`). Both `(1884–1958)` and `0.78 Ma` / `about 780,000 years ago` are confirmed on the opened Wikipedia and NASA Science pages.

---

## Row 5

- **Claim:** The last full magnetic reversal (the Brunhes–Matuyama reversal) happened about 780,000 years ago — more than twice as long as modern *Homo sapiens* (~300,000 years) have walked the Earth.
- **Must quote:** Yes (`WHEN`, `DATA`, `SCALE`)
- **URLs opened:**
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` (named)
  - `https://www.usgs.gov/faqs/do-earths-magnetic-poles-flip` (named — returned HTTP 202 WAF challenge)
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=28593953&retmode=xml` (public PubMed abstract for named paper Hublin et al. 2017, *Nature* 546, 289–292, `doi:10.1038/nature22336`; *Nature* landing page paywalled)
  - `https://en.wikipedia.org/wiki/Geomagnetic_reversal` (extra)
- **Verdict:** OK
- **Verbatim quotes:**
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` : `"The time intervals between reversals have fluctuated widely, but average about 300,000 years, with the last one taking place about 780,000 years ago."`
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=28593953&retmode=xml` (used public abstract for Hublin et al. 2017) : `"We identified a mosaic of features including facial, mandibular and dental morphology that aligns the Jebel Irhoud material with early or recent anatomically modern humans and more primitive neurocranial and endocranial morphology. In combination with an age of 315 ± 34 thousand years (as determined by thermoluminescence dating), this evidence makes Jebel Irhoud the oldest and richest African Middle Stone Age hominin site that documents early stages of the H. sapiens clade in which key features of modern morphology were established."`
  - `https://en.wikipedia.org/wiki/Geomagnetic_reversal` : `"The latest, the Brunhes–Matuyama reversal, occurred 780,000 years ago"`
- **Anything the page does not say / notes:**
  - `"more than twice as long as modern Homo sapiens (~300,000 years) have walked the Earth"` is our own comparison from the quoted numbers (`780,000 years ago` vs `315 ± 34 thousand years` / `~300,000 years`).

---

## Row 6

- **Claim:** About 3,000 km (~2,890 km) beneath the surface lies the liquid iron-and-nickel outer core, hotter than the surface of the Sun, whose convective electric currents generate Earth's magnetic field (the geodynamo).
- **Must quote:** Yes (`DATA`)
- **URLs opened:**
  - `https://www.bgs.ac.uk/discovering-geology/earth-hazards/geomagnetism/` (named — returned HTTP 404)
  - `https://www.usgs.gov/faqs/how-does-earths-magnetic-field-work` (named — returned HTTP 202 WAF challenge)
  - `https://geomag.bgs.ac.uk/education/reversals.html` (extra — active BGS geomagnetism education page)
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Swarm_probes_weakening_of_Earth_s_magnetic_field` (extra)
  - `https://www.nasa.gov/missions/station/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/` (extra)
- **Verdict:** PARTIAL
- **Verbatim quotes:**
  - `https://geomag.bgs.ac.uk/education/reversals.html` : `"The source of the magnetic field is the iron-rich liquid outer core of the Earth."`
  - `https://geomag.bgs.ac.uk/education/reversals.html` : `"At the top of the liquid core, some 3000 km beneath our feet and below the rocky mantle, the fluid may travel at horizontal speeds of tens of kilometres per year. The motion of this metal fluid across existing magnetic field lines of force produces electrical currents and these, in turn, generate more magnetic field."`
  - `https://geomag.bgs.ac.uk/education/reversals.html` : `"This is a world where the crushing forces and core temperatures similar to that of the surface of the Sun take our scientific understanding to the limit."`
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Swarm_probes_weakening_of_Earth_s_magnetic_field` : `"The magnetic field is largely generated by an ocean of superheated, swirling liquid iron that makes up the outer core around 3000 km beneath our feet. Acting as a spinning conductor in a bicycle dynamo, it creates electrical currents, which in turn, generate our continuously changing electromagnetic field."`
  - `https://www.nasa.gov/missions/station/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/` : `"That’s because the field originates from Earth’s outer core: molten, iron-rich and in vigorous motion 1800 miles below the surface. These churning metals act like a massive generator, called the geodynamo, creating electric currents that produce the magnetic field."`
- **Anything the page does not say / notes:**
  - The named URL `https://www.bgs.ac.uk/discovering-geology/earth-hazards/geomagnetism/` is HTTP 404. On the active BGS geomagnetism, ESA, and NASA pages, `"~2,890 km"`, `"nickel"`, and `"hotter than the surface of the Sun"` are not present (BGS `reversals.html` says `"some 3000 km"`, `"iron-rich liquid outer core"`, and `"core temperatures similar to that of the surface of the Sun"`).

---

## Row 7

- **Claim:** Over the last 83 million years, Earth's magnetic field has reversed 183 times, recorded like a magnetic barcode in volcanic rock spreading across the ocean floor.
- **Must quote:** Yes (`WHEN`, `DATA`, `FACT`)
- **URLs opened:**
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` (named)
  - `https://geomag.bgs.ac.uk/education/earthmag.html` (extra)
- **Verdict:** OK
- **Verbatim quotes:**
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` : `"Paleomagnetic records tell us Earth’s magnetic poles have reversed 183 times in the last 83 million years, and at least several hundred times in the past 160 million years."`
  - `https://geomag.bgs.ac.uk/education/earthmag.html` : `"At these locations molten mantle comes to the surface and solidifies to form new oceanic crust, preserving in it the strength and direction of the contemporary ambient magnetic field. As new material is extruded, the existing crust is pushed away on either side of the ridge, with the direction of the ambient magnetic field at time of formation frozen into it. Marine and aeromagnetic surveys reveal a series of stripes in the total intensity anomalies which run parallel to and symmetrically about the central ridge and these are interpreted as alternating blocks of normal and reversely magnetised oceanic crust."`
- **Anything the page does not say / notes:**
  - `"like a magnetic barcode"` is our own analogy for the alternating magnetic stripes in volcanic oceanic crust (BGS `earthmag.html` calls them `"a series of stripes"` and `"a crude tape recorder"`).

---

## Row 8

- **Claim:** Since German mathematician Carl Friedrich Gauss (1777–1855) began direct magnetic intensity measurements in the 1830s, Earth's global magnetic field strength has dropped by about 9% (9–10%).
- **Must quote:** Yes (`WHO`, `WHEN`, `DATA`, `SCALE`)
- **URLs opened:**
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Swarm_probes_weakening_of_Earth_s_magnetic_field` (named)
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` (extra)
  - `https://web.archive.org/web/20230512145930id_/https://science.nasa.gov/science-news/science-at-nasa/2003/29dec_magneticfield/` (extra — NASA Science "Earth's Inconstant Magnetic Field")
  - `https://geomag.bgs.ac.uk/education/earthmag.html` (extra)
  - `https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss` (extra)
- **Verdict:** OK
- **Verbatim quotes:**
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Swarm_probes_weakening_of_Earth_s_magnetic_field` : `"Over the last 200 years, the magnetic field has lost around 9% of its strength on a global average."`
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` : `"In the past 200 years, Earth’s magnetic field has weakened about nine percent on a global average."`
  - `https://web.archive.org/web/20230512145930id_/https://science.nasa.gov/science-news/science-at-nasa/2003/29dec_magneticfield/` : `"And globally the magnetic field has weakened 10% since the 19th century."`
  - `https://geomag.bgs.ac.uk/education/earthmag.html` : `"Magnetic observations prior to the establishment of observatories and an absolute method of measuring magnetic intensity by Gauss in the 1830s were made, amongst others, by mariners engaged in merchant and naval shipping."`
  - `https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss` : `"Johann Carl Friedrich Gauss (/ɡaʊs/; German: Gauß; 30 April 1777 – 23 February 1855) was a German polymath active as a mathematician, astronomer, geodesist, and physicist, who contributed to many fields in mathematics and science."`
- **Anything the page does not say / notes:**
  - The named ESA page gives `"around 9% of its strength on a global average"` over the last 200 years; Gauss's name, `1830s`, life years `(1777–1855)`, and `10%` are confirmed verbatim on the opened BGS, Wikipedia, and NASA pages.

---

## Row 9

- **Claim:** Launched in November 2013, ESA's three Swarm spacecraft map the magnetic field and track the South Atlantic Anomaly (SAA) over Brazil and the South Atlantic.
- **Must quote:** Yes (`WHEN`)
- **URLs opened:**
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm` (named)
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Swarm_probes_weakening_of_Earth_s_magnetic_field` (extra)
  - `https://www.nasa.gov/missions/station/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/` (extra)
- **Verdict:** PARTIAL
- **Verbatim quotes:**
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm` : `"ESA’s three-satellite Swarm mission is dedicated to unravelling one of the most mysterious aspects of our planet: the magnetic field."`
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm` : `"Date: 22 November 2013 Site: Plesetsk Cosmodrome, Russia"`
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Swarm_probes_weakening_of_Earth_s_magnetic_field` : `"A large region of reduced magnetic intensity has developed between Africa and South America and is known as the South Atlantic Anomaly."`
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Swarm_probes_weakening_of_Earth_s_magnetic_field` : `"Scientists from the Swarm Data, Innovation and Science Cluster (DISC) have used data from ESA’s Swarm satellite constellation to better understand this anomaly."`
  - `https://www.nasa.gov/missions/station/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/` : `"But over South America and the southern Atlantic Ocean, an unusually weak spot in the field – called the South Atlantic Anomaly, or SAA – allows these particles to dip closer to the surface than normal."`
- **Anything the page does not say / notes:**
  - The word `"Brazil"` is not on the opened ESA or NASA pages (they say `"between Africa and South America"` and `"over South America and the southern Atlantic Ocean"`).

---

## Row 10

- **Claim:** Over the South Atlantic Anomaly, a reverse-flux patch on the liquid outer core lets inner Van Allen belt radiation dip from ~1,000 km down to about 200 km altitude — half the ~400 km orbit height of the International Space Station.
- **Must quote:** Yes (`DATA`, `SCALE`)
- **URLs opened:**
  - `https://www.nasa.gov/missions/station/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/` (named)
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Swarm_probes_weakening_of_Earth_s_magnetic_field` (named)
  - `https://geomag.bgs.ac.uk/education/reversals.html` (extra)
  - `https://en.wikipedia.org/wiki/South_Atlantic_Anomaly` (extra)
- **Verdict:** PARTIAL
- **Verbatim quotes:**
  - `https://www.nasa.gov/missions/station/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/` : `"The innermost belt begins about 400 miles from the surface of Earth, which keeps its particle radiation a healthy distance from Earth and its orbiting satellites."`
  - `https://www.nasa.gov/missions/station/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/` : `"But over South America and the southern Atlantic Ocean, an unusually weak spot in the field – called the South Atlantic Anomaly, or SAA – allows these particles to dip closer to the surface than normal."`
  - `https://www.nasa.gov/missions/station/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/` : `"More specifically, a localized field with reversed polarity grows strongly in the SAA region, thus making the field intensity very weak, weaker than that of the surrounding regions."`
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Swarm_probes_weakening_of_Earth_s_magnetic_field` : `"A large region of reduced magnetic intensity has developed between Africa and South America and is known as the South Atlantic Anomaly."`
  - `https://geomag.bgs.ac.uk/education/reversals.html` : `"It is the growth in area of such a reversed flux patch under the south Atlantic that is primarily responsible for the decay in the main dipolar field. This reverse patch is also responsible for the minimum in field strength called the South Atlantic Anomaly, now centred over south America."`
  - `https://en.wikipedia.org/wiki/South_Atlantic_Anomaly` : `"The South Atlantic Anomaly (SAA) is an area where Earth's inner Van Allen radiation belt comes closest to Earth's surface, dipping down to an altitude of 200 kilometres (120 mi)."`
- **Anything the page does not say / notes:**
  - The named NASA page says the innermost Van Allen belt begins `"about 400 miles from the surface of Earth"` (~640 km), not `"~1,000 km"`, and does not state `"about 200 km altitude"` (which is on Wikipedia SAA) or `"~400 km orbit height of the International Space Station"` (it only says `"The International Space Station, which is in low-Earth orbit, also passes through the SAA"`).
  - `"half the ~400 km orbit height"` is our own comparison.

---

## Row 11

- **Claim:** When the Hubble Space Telescope passes through the South Atlantic Anomaly (up to ~10 times a day), it switches off its sensitive cameras so radiation does not blind them; ISS laptops and Japan's Hitomi observatory (2016) also experienced glitches after passing through the zone.
- **Must quote:** Yes (`WHEN`, `FACT`)
- **URLs opened:**
  - `https://www.nasa.gov/missions/station/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/` (named)
  - `https://hst-docs.stsci.edu/hsp/past-hst-proposal-opportunities/the-hubble-space-telescope-primer-for-cycle-26/hst-cycle-26-primer-orbital-constraints` (named Hubble SAA documentation)
  - `https://science.nasa.gov/missions/hubble/hubble-achieves-milestone-100000th-exposure/` (named NASA Hubble SAA page)
  - `https://global.jaxa.jp/press/2016/04/20160428_hitomi.html` (named JAXA Hitomi report)
  - `https://en.wikipedia.org/wiki/South_Atlantic_Anomaly` (extra)
  - `https://en.wikipedia.org/wiki/Hitomi_(satellite)` (extra)
- **Verdict:** PARTIAL
- **Verbatim quotes:**
  - `https://www.nasa.gov/missions/station/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/` : `"In order to avoid losing instruments or an entire satellite, operators commonly shut down non-essential components as they pass through the SAA."`
  - `https://www.nasa.gov/missions/station/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/` : `"The International Space Station, which is in low-Earth orbit, also passes through the SAA. It is well-protected, and astronauts are safe from harm while inside. However, the ISS has other passengers affected by the higher radiation levels: instruments Mounted on the exterior of the ISS"`
  - `https://hst-docs.stsci.edu/hsp/past-hst-proposal-opportunities/the-hubble-space-telescope-primer-for-cycle-26/hst-cycle-26-primer-orbital-constraints` : `"No astronomical or calibration observations are possible (except for some specialized and infrequently executed WFC3 observations) during spacecraft passage through the SAA because of high background induced in the scientific instruments and FGSs. As the HST orbit precesses and the Earth rotates, the southern part of the HST orbit intersects the SAA each day for seven to nine orbits in a row (so-called “SAA-impacted” orbits)."`
  - `https://science.nasa.gov/missions/hubble/hubble-achieves-milestone-100000th-exposure/` : `"...Hubble's low-Earth orbit and that it cannot observe for about 50 percent of each orbit because of the Earth's occultation (when Earth blocks Hubble's view) and the South Atlantic Anomaly (a high radiation belt through which Hubble cannot observe)."`
  - `https://en.wikipedia.org/wiki/South_Atlantic_Anomaly` : `"NASA has reported that modern laptop computers have crashed when Space Shuttle flights passed through the anomaly"` and `"The SAA is believed to have started a series of events leading to the destruction of the Hitomi, Japan's most powerful X-ray observatory."`
  - `https://global.jaxa.jp/press/2016/04/20160428_hitomi.html` : `"On March 26, 2016 (Japan Standard Time), an anomaly occurred in the operations of the X-ray Astronomy Satellite 'Hitomi' (ASTRO-H)."`
- **Anything the page does not say / notes:**
  - STScI states Hubble intersects the SAA `"each day for seven to nine orbits in a row"` rather than `"up to ~10 times a day"`.
  - The named NASA Goddard SAA article mentions `"instruments Mounted on the exterior of the ISS"` rather than `"ISS laptops"` (Wikipedia SAA mentions `"Space Shuttle flights"` laptop crashes).
  - JAXA's official Hitomi report (`https://global.jaxa.jp/press/2016/04/20160428_hitomi.html`) attributes the 2016 loss of Hitomi to attitude control / IRU and thruster software issues without blaming the SAA (though Wikipedia SAA notes `"The SAA is believed to have started a series of events leading to the destruction of the Hitomi"`).

---

## Row 12

- **Claim:** Since 1970 the South Atlantic Anomaly has widened and split into two lobes.
- **Must quote:** Yes (`WHEN`)
- **URLs opened:**
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Swarm_probes_weakening_of_Earth_s_magnetic_field` (named)
  - `https://www.nasa.gov/missions/station/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/` (extra)
- **Verdict:** OK
- **Verbatim quotes:**
  - `https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Swarm_probes_weakening_of_Earth_s_magnetic_field` : `"From 1970 to 2020, the minimum field strength in this area has dropped from around 24 000 nanoteslas to 22 000, while at the same time the area of the anomaly has grown and moved westward at a pace of around 20 km per year. Over the past five years, a second centre of minimum intensity has emerged southwest of Africa – indicating that the South Atlantic Anomaly could split up into two separate cells."`
  - `https://www.nasa.gov/missions/station/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/` : `"However, recent observations and forecasts show that the region is expanding westward and continuing to weaken in intensity. It is also splitting – recent data shows the anomaly’s valley, or region of minimum field strength, has split into two lobes, creating additional challenges for satellite missions."`
- **Anything the page does not say / notes:**
  - None; `From 1970 to 2020 ... the area of the anomaly has grown` is verbatim on the named ESA page, and `has split into two lobes` is verbatim on the NASA page.

---

## Row 13

- **Claim:** Deep ocean sediment cores over the past 100,000 years show that today's magnetic field is still stronger than the long-term average, and often dips without flipping.
- **Must quote:** No (checked per instructions)
- **URLs opened:**
  - `https://gfzpublic.gfz.de/pubman/faces/ViewItemOverviewPage.jsp?itemId=item_234298` (named Constable & Korte 2006 record, `doi:10.1016/j.epsl.2006.03.038`; publisher abstract not publicly available)
  - `https://www.usgs.gov/faqs/do-earths-magnetic-poles-flip` (named — HTTP 202 WAF challenge)
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` (extra)
  - `https://web.archive.org/web/20230512145930id_/https://science.nasa.gov/science-news/science-at-nasa/2003/29dec_magneticfield/` (extra)
- **Verdict:** OK
- **Verbatim quotes:**
  - `https://gfzpublic.gfz.de/pubman/faces/ViewItemOverviewPage.jsp?itemId=item_234298` : `"Title: Is the Earth's magnetic field reversing?"`
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` : `"Deep ocean sediment samples indicate glacial activity was stable."`
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` : `"In fact, paleomagnetic studies show the field is about as strong as it’s been in the past 100,000 years, and is twice as intense as its million-year average."`
  - `https://web.archive.org/web/20230512145930id_/https://science.nasa.gov/science-news/science-at-nasa/2003/29dec_magneticfield/` : `"According to Glatzmaier, the ongoing 10% decline doesn't mean that a reversal is imminent. 'The field is increasing or decreasing all the time,' he says. 'We know this from studies of the paleomagnetic record.' Earth's present-day magnetic field is, in fact, much stronger than normal. The dipole moment, a measure of the intensity of the magnetic field, is now 8 × 1022 amps × m2. That's twice the million-year average of 4× 1022 amps × m2."`
- **Anything the page does not say / notes:**
  - Constable & Korte (2006) is closed-access without a public abstract on GFZ/Semantic Scholar, and USGS returned HTTP 202; every part of the claim is supported verbatim on the opened NASA Science pages.

---

## Row 14

- **Claim:** About 41,000 years ago, during the Laschamp geomagnetic excursion, Earth's magnetic shield dropped to about 6% of today's strength during the transition (recorded ring by ring in ancient New Zealand swamp kauri trees via radiocarbon spikes), taking a few hundred years to drop and lasting around a thousand years.
- **Must quote:** Yes (`WHEN`, `DATA`, `SCALE`, `FACT`)
- **URLs opened:**
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=33602851&retmode=xml` (public PubMed abstract for named paper Cooper et al. 2021, *Science* 371(6531), 811–818, `doi:10.1126/science.abb8677`)
  - `https://ora.ox.ac.uk/objects/uuid:4df59a07-09d9-4573-a310-97f20e83490d/files/swm117p610` (full open-access PDF of Cooper et al. 2021 in the Oxford University Research Archive)
- **Verdict:** OK
- **Verbatim quotes:**
  - `https://ora.ox.ac.uk/objects/uuid:4df59a07-09d9-4573-a310-97f20e83490d/files/swm117p610` (p. 9, Editor's summary) : `"Cooper et al. created a precisely dated radiocarbon record around the time of the Laschamps geomagnetic reversal about 41,000 years ago from the rings of New Zealand swamp kauri trees. This record reveals a substantial increase in the carbon-14 content of the atmosphere culminating during the period of weakening magnetic field strength preceding the polarity switch."`
  - `https://ora.ox.ac.uk/objects/uuid:4df59a07-09d9-4573-a310-97f20e83490d/files/swm117p610` (p. 1) : `"One of the best opportunities to study the impacts of extreme changes in Earth’s magnetic field is the Laschamps Excursion (hereafter Laschamps)—a recent, relatively short-duration (<1000 year) reversal ~41 thousand years ago (ka) (4). Sedimentary and volcanic deposits indicate a weakening of the magnetic field intensity to <28% of current levels during the reversed phase of the Laschamps and, notably, as little as 0 to 6% during the preceding transition as polarity switched (Fig. 1 and supplementary materials) (1, 2, 5)."`
  - `https://ora.ox.ac.uk/objects/uuid:4df59a07-09d9-4573-a310-97f20e83490d/files/swm117p610` (p. 3) : `"Notably, the steep rise in Δ14C commences at 42.35 ka, with a peak value of 782 per mil (‰) occurring at 41.8 ka, 300 years before the full Laschamps reversal."`
  - `https://ora.ox.ac.uk/objects/uuid:4df59a07-09d9-4573-a310-97f20e83490d/files/swm117p610` (p. 7) : `"Although the immediate impacts associated with the geomagnetic transition were likely on the order of the duration (800 years), many of the above synchronous changes persisted for millennia."`
- **Anything the page does not say / notes:**
  - None; every number and detail in the claim is verbatim in Cooper et al. (2021) (note the paper spells the event `"Laschamps"` with a final *s*).

---

## Row 15

- **Claim:** During a magnetic reversal, the field never vanishes completely; smaller backup multipoles remain at roughly 10–20% of normal strength.
- **Must quote:** Yes (`DATA`)
- **URLs opened:**
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` (named)
  - `https://www.usgs.gov/faqs/do-earths-magnetic-poles-flip` (named — HTTP 202 WAF challenge)
  - `https://geomag.bgs.ac.uk/education/reversals.html` (extra)
  - `https://web.archive.org/web/20230628070448id_/https://websites.pmc.ucsc.edu/~glatz/geodynamo.html` (extra)
- **Verdict:** PARTIAL
- **Verbatim quotes:**
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` : `"During a pole reversal, the magnetic field weakens, but it doesn’t completely disappear. The magnetosphere, together with Earth’s atmosphere, continue protecting Earth from cosmic rays and charged solar particles, though there may be a small amount of particulate radiation that makes it down to Earth’s surface. The magnetic field becomes jumbled, and multiple magnetic poles can emerge in unexpected places."`
  - `https://geomag.bgs.ac.uk/education/reversals.html` : `"In such simulations, the strength of the main dipole appears to weaken, perhaps to about 10% of its normal value (but not vanish) and the existing poles may wander across the globe and be joined by other temporary North and South magnetic poles (the 'non-dipole field')."`
  - `https://web.archive.org/web/20230628070448id_/https://websites.pmc.ucsc.edu/~glatz/geodynamo.html` : `"The intensity of the magnetic dipole moment decreased by about a factor of ten during the reversal and recovered immediately after, similar to what is seen in the Earth's paleomagnetic reversal record."`
- **Anything the page does not say / notes:**
  - The named NASA Science page does not state `"10–20%"`. BGS `reversals.html` confirms `"about 10% of its normal value"` (and Glatzmaier says `"by about a factor of ten"`), while `"20%"` is not on the opened pages.

---

## Row 16

- **Claim:** Earth's atmosphere has a shielding mass (~1,000 g/cm²) equivalent to a layer of water 10 metres deep covering the planet, stopping fast space particles in the stratosphere long before they reach the ground.
- **Must quote:** Yes (`DATA`, `SCALE`)
- **URLs opened:**
  - `https://geomag.bgs.ac.uk/education/reversals.html` (named BGS geomagnetic reversal FAQ)
  - `https://ntrs.nasa.gov/api/citations/20030063010/downloads/20030063010.pdf` (named NASA Space Radiation report — Wilson et al., NASA Langley Research Center, *Overview of Atmospheric Ionizing Radiation (AIR)*)
  - `https://faculty.washington.edu/stn/ess_460560/homework/HW_wk_2_nuclear_physics.pdf` (extra)
- **Verdict:** PARTIAL
- **Verbatim quotes:**
  - `https://geomag.bgs.ac.uk/education/reversals.html` : `"Indeed the atmosphere shields us from high-energy radiation as effectively as a concrete layer some 13 feet thick."`
  - `https://ntrs.nasa.gov/api/citations/20030063010/downloads/20030063010.pdf` (p. 44) : `"Note that the count rates near the surface ( ~1,000 g/cm2 ) are nearly independent of solar modulation and geomagnetic cutoff. The proton mean free path to nuclear absorption is on the order of several tens of g/cm2 so that relatively few of the protons beyond 100 g/cm2 depths are primary particles."`
  - `https://ntrs.nasa.gov/api/citations/20030063010/downloads/20030063010.pdf` (Table 12, p. 66) : `"Altitude, km: 0 | Air depth, g/cm2: 1034"`
  - `https://faculty.washington.edu/stn/ess_460560/homework/HW_wk_2_nuclear_physics.pdf` : `"We define ‘shielding thickness’ in units of g/cm2 – think of the cumulative mass of a column of material with a cross-sectional area 1 cm2. Given a shielding thickness Z, the equivalent length l (in centimeters) in a material of density ρ (g/cm3) is given by: Z = ρ l"` and `"the shielding depth at sea level is 1033.2 g/cm-2."`
- **Anything the page does not say / notes:**
  - Neither the BGS geomagnetic reversal FAQ nor the NASA AIR report states `"equivalent to a layer of water 10 metres deep"` verbatim; BGS `reversals.html` instead says `"as effectively as a concrete layer some 13 feet thick"`, although physically `~1,000 g/cm²` divided by water's density (`1 g/cm³`) equals `1,000 cm` = `10 m` of water.

---

## Row 17

- **Claim:** Mars lost most of its atmosphere over billions of years largely because of its low gravity (about a third of Earth's, ~38%); a flip on Earth takes only a few thousand years (1,000–10,000 years), far too brief to strip a heavy planet's atmosphere.
- **Must quote:** Yes (`DATA`)
- **URLs opened:**
  - `https://science.nasa.gov/mission/maven/` (named)
  - `https://www.nasa.gov/news-release/nasa-mission-reveals-speed-of-solar-wind-stripping-martian-atmosphere/` (named MAVEN release)
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` (named)
  - `https://web.archive.org/web/20230512145930id_/https://science.nasa.gov/science-news/science-at-nasa/2003/29dec_magneticfield/` (extra)
  - `https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html` (extra — NASA NSSDC Mars Fact Sheet)
  - `https://en.wikipedia.org/wiki/Geomagnetic_reversal` (extra)
- **Verdict:** OK
- **Verbatim quotes:**
  - `https://www.nasa.gov/news-release/nasa-mission-reveals-speed-of-solar-wind-stripping-martian-atmosphere/` : `"MAVEN data have enabled researchers to determine the rate at which the Martian atmosphere currently is losing gas to space via stripping by the solar wind."`
  - `https://www.nasa.gov/news-release/nasa-mission-reveals-speed-of-solar-wind-stripping-martian-atmosphere/` : `"We’ve seen that the atmospheric erosion increases significantly during solar storms, so we think the loss rate was much higher billions of years ago when the sun was young and more active."`
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` : `"No one knows exactly when the next pole reversal may occur, but scientists know they don’t happen overnight: they take place over hundreds to thousands of years."`
  - `https://web.archive.org/web/20230512145930id_/https://science.nasa.gov/science-news/science-at-nasa/2003/29dec_magneticfield/` : `"Reversals take a few thousand years to complete, and during that time--contrary to popular belief--the magnetic field does not vanish."`
  - `https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html` : `"Surface gravity (mean) (m/s2): Mars 3.73 | Earth 9.82 | Ratio (Mars/Earth) 0.380"`
  - `https://en.wikipedia.org/wiki/Geomagnetic_reversal` : `"Most estimates for the duration of a polarity transition are between 1,000 and 10,000 years"`
- **Anything the page does not say / notes:**
  - Every number in the claim (`billions of years`, Mars/Earth surface gravity ratio `0.380` [38%, about a third], `a few thousand years`, `1,000 and 10,000 years`) is verbatim on the opened pages. Note that NASA's MAVEN release emphasises solar-wind stripping after Mars lost its magnetic field, while `0.380` is on the NASA NSSDC Mars Fact Sheet.

---

## Row 18

- **Claim:** During a 1,000 to 10,000 year reversal transition, models of the liquid core show Earth's magnetic field breaks into 4, 6, or 8 poles at once across mid and low latitudes, bringing auroras down toward the equator over 40 to 400 human generations.
- **Must quote:** Yes (`DATA`, `SCALE`)
- **URLs opened:**
  - `https://web.archive.org/web/20230512145930id_/https://science.nasa.gov/science-news/science-at-nasa/2003/29dec_magneticfield/` (named — NASA Science, "Earth's Inconstant Magnetic Field", 29 Dec 2003)
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` (extra)
  - `https://en.wikipedia.org/wiki/Geomagnetic_reversal` (extra)
  - `https://ora.ox.ac.uk/objects/uuid:4df59a07-09d9-4573-a310-97f20e83490d/files/swm117p610` (extra — Cooper et al. 2021, Fig. 5D)
- **Verdict:** PARTIAL
- **Verbatim quotes:**
  - `https://web.archive.org/web/20230512145930id_/https://science.nasa.gov/science-news/science-at-nasa/2003/29dec_magneticfield/` : `"Reversals take a few thousand years to complete, and during that time--contrary to popular belief--the magnetic field does not vanish. 'It just gets more complicated,' says Glatzmaier. Magnetic lines of force near Earth's surface become twisted and tangled, and magnetic poles pop up in unaccustomed places. A south magnetic pole might emerge over Africa, for instance, or a north pole over Tahiti."`
  - `https://web.archive.org/web/20230512145930id_/https://science.nasa.gov/science-news/science-at-nasa/2003/29dec_magneticfield/` : `"And, as a bonus, Tahiti could be a great place to see the Northern Lights. In such a time, Larry Newitt's job would be different. Instead of shivering in Resolute Bay, he could enjoy the warm South Pacific, hopping from island to island, hunting for magnetic poles while auroras danced overhead."`
  - `https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/` : `"The magnetic field becomes jumbled, and multiple magnetic poles can emerge in unexpected places."`
  - `https://en.wikipedia.org/wiki/Geomagnetic_reversal` : `"Most estimates for the duration of a polarity transition are between 1,000 and 10,000 years"`
- **Anything the page does not say / notes:**
  - The specific numbers `"4, 6, or 8 poles"` are not on the named NASA article (which says `"magnetic poles pop up in unaccustomed places. A south magnetic pole might emerge over Africa, for instance, or a north pole over Tahiti"`, and NASA "Flip Flop" says `"multiple magnetic poles"`).
  - `"over 40 to 400 human generations"` is our own comparison calculated from `1,000 and 10,000 years` divided by 25 years per generation.

---

## Row 19

- **Claim:** WHO years: Bernard Brunhes (1867–1910), Motonori Matuyama (1884–1958), and Carl Friedrich Gauss (1777–1855).
- **Must quote:** Yes (`WHO`)
- **URLs opened:**
  - `https://eos.org/articles/centenary-discovery-earths-magnetic-field-reversals`
  - `https://en.wikipedia.org/wiki/Bernard_Brunhes`
  - `https://en.wikipedia.org/wiki/Motonori_Matuyama`
  - `https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss`
- **Verdict:** OK
- **Verbatim quotes:**
  - `https://eos.org/articles/centenary-discovery-earths-magnetic-field-reversals` : `"The inscription reads “Bernard Brunhes (1867–1910). Director of the Puy de Dôme Observatory from 1900 to 1910."`
  - `https://en.wikipedia.org/wiki/Bernard_Brunhes` : `"Antoine Joseph Bernard Brunhes (3 July 1867 – 10 May 1910) was a French geophysicist known for his pioneering work in paleomagnetism, in particular, his 1906 discovery of geomagnetic reversal."`
  - `https://en.wikipedia.org/wiki/Motonori_Matuyama` : `"Motonori Matsuyama (松山 基範, Matsuyama Motonori; October 25, 1884 – January 27, 1958) was a Japanese geophysicist"` and `"The Japanese geophysicist Motonori Matsuyama (1884–1958, as spelled and pronounced but mistransliterated in his own publications and others as Matuyama)"`
  - `https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss` : `"Johann Carl Friedrich Gauss (/ɡaʊs/; German: Gauß; 30 April 1777 – 23 February 1855) was a German polymath active as a mathematician, astronomer, geodesist, and physicist"`
- **Anything the page does not say / notes:**
  - None; all three names and birth/death years are verified verbatim on the opened pages.

---

## Summary Counts (J0318, 15 Oct 2026)

- **OK:** 9 (rows 2, 5, 7, 8, 12, 13, 14, 17, 19)
- **PARTIAL:** 10 (rows 1, 3, 4, 6, 9, 10, 11, 15, 16, 18)
- **FLAG:** 0
- **TO VERIFY remaining:** 0
