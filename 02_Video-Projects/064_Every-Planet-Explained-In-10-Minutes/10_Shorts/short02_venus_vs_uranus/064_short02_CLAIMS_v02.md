# OWB:064 Short 2 — Claims and quote-check inputs v02 (`064_short02_CLAIMS_v02.md`)

Prepared by `claudecode` (J3913) for Gemini (`agy --model gemini-4-argon-high`) under the dependent review J3914. **Status: inputs only. Not yet run, nothing passed.** Gemini opens each URL, confirms or corrects the exact quote, and flags any claim the quote does not support. Each flag gets resolved in a versioned note (`064_short02_QUOTECHECK_v02.md`) before lock. Gemini doesn't rewrite spoken lines; the writer does.

| # | Spoken claim (v02 / v02b) | Direct URL to open | Exact quote expected (verify verbatim) | What to check |
|---|---|---|---|---|
| C1 | Venus's **surface** is 464 °C | https://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html | "Average temperature: 737 K (464 C)" (in the surface/atmosphere block) | That the figure is the surface (average) temperature; whether "average" must be spoken |
| C2 | Venus air is 96.5 % carbon dioxide | same | "Major: 96.5% Carbon Dioxide (CO2), 3.5% Nitrogen (N2)" | Verbatim percentage |
| C3 | Venus air at 92 bars | same | "Surface pressure: 92 bars" | That 92 bars is surface pressure |
| C4 | Venus's air traps heat in a runaway greenhouse | https://science.nasa.gov/venus/venus-facts/ | "Its thick atmosphere traps heat in a runaway greenhouse effect, making it the hottest planet in our solar system." | Verbatim; whether the page attributes the surface heat to the greenhouse effect |
| C5 | Uranus has no true surface | https://science.nasa.gov/uranus/facts/ | "As an ice giant, Uranus doesn't have a true surface." | Verbatim; whether v02b's "no surface" (without "true") stays accurate |
| C6 | Uranus's atmosphere minimum −224 °C (spoken "minus 224"; −224.2 °C on screen) | same | "Uranus' planetary atmosphere, with a minimum temperature of 49K (-224.2 degrees Celsius) makes it even colder than Neptune in some places." | That the figure is an **atmospheric minimum**, not a surface or average reading; whether rounding −224.2 to "minus 224" is acceptable when the overlay/description gives −224.2 |
| C7 | Colder than Neptune **in some places** | same | (same sentence as C6) | The qualifier is kept in v02; v02b drops this claim |
| C8 | v02b: "that's its coldest air" | same | (same sentence as C6) | Whether "coldest air" fairly restates "minimum temperature" of the atmosphere |
| C9 | v02b: "thick carbon dioxide air" | NSSDC Venus page + science.nasa.gov/venus/venus-facts/ | C2 + C4 | That "carbon dioxide air" doesn't imply 100 % CO2 |

**Removed claims (v01 → v02), no check needed:** "Rolling sideways into 21-year winters" (removed as a possible implied cause of the minimum); "Closer in" (removed because it could suggest distance is the cause).

**Description/listing:** the draft manifest text still holds v01 claims (21-year winter, 97.77°). The listing job rewrites it once the script locks; Gemini checks it then.
