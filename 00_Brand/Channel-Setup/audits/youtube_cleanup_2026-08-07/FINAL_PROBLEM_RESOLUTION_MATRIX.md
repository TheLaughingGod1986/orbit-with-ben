# FINAL PROBLEM RESOLUTION MATRIX

Audited (UTC): 2026-08-06T23:31:49.529Z

Counts: FIXED=1 · FIXED WITH MONITORING=7 · PARTIALLY FIXED=9 · NOT FIXED=9 · UNVERIFIABLE=2

| # | Problem | Previous evidence | Current evidence | Status | Residual risk |
|---:|---|---|---|---|---|
| 1 | Competing public long-form uploads | RCs6MMxF3ko privatized; 3xrxdmaOwJI public (FINAL_SHELF_VERIFY) | RCs6MMxF3ko PUBLIC; 3xrxdmaOwJI PRIVATE; oEmbed confirms | **NOT FIXED** | High — smooth-CFR shelf inverted approved canon |
| 2 | Duplicate public Shorts | IwpO privatized; JRfh/L2OF public | IwpO33AJaPQ PUBLIC; JRfhE6yWom4+L2OFjL4neOo PRIVATE; also extra public Fermi Shorts ['IwpO33AJaPQ', 'RCs6MMxF3ko', 'UWwNKYf_aU8', 'dPMJQp2gMNc', 'rFJoOdQAc9c', 'z-DLqoSoEBo'] | **NOT FIXED** | High |
| 3 | Canonical Shorts demoted/privatized/replaced | POST_OAUTH PASS restored JRfh/L2OF | Canonical BH Shorts private again | **NOT FIXED** | High |
| 4 | Duplicate scheduled uploads | Held twins to Dec 31; NF01 kept Aug 7 | Held twins still Dec 31; active go-lives distinct IDs — PASS for known BH set | **FIXED WITH MONITORING** | Medium — many private twin titles remain uploadable via CDP scripts |
| 5 | Scheduled publishing collisions | Same-slot NF01 collision held | No same-minute collision for NF01; Aug 11 two Shorts same day | **FIXED WITH MONITORING** | Low for known BH; calendar dense Aug 11–25 |
| 6 | CDP/browser automation creating replacements | Four DISABLED__ smooth scripts | DISABLED__ exit hard; MANY other CDP upload/replace scripts still reachable under Schedule/ and audits/ | **PARTIALLY FIXED** | Critical — alternate CDP paths still runnable |
| 7 | Upload retry creating multiple YouTube IDs | Package path hardened + tests | youtube:package has ambiguous-stop; youtube:upload lacks recovery/fingerprint gates | **PARTIALLY FIXED** | High if youtube:upload used |
| 8 | Thin/incomplete metadata on replacement batches | Zero-tag held batch documented | Held IDs still missing tags/lang; public dupes IwpO/RCs6 tags=0 | **PARTIALLY FIXED** | Medium |
| 9 | Incorrect/inconsistent category | Adapter defaults category 27 | Canonical Fermi long=27; most Shorts+smooth long still categoryId 22 | **PARTIALLY FIXED** | Medium for discovery |
| 10 | Incorrect/inconsistent language | Adapter defaults en-GB | Live assets mostly defaultLanguage=en not en-GB; BH long audio en-US | **PARTIALLY FIXED** | Low-Medium |
| 11 | Missing notifySubscribers behaviour | Adapter sets notifySubscribers on public insert | Code present; cannot re-verify historical uploads | **FIXED WITH MONITORING** | Low for new package uploads |
| 12 | Missing/insufficient OAuth permissions | force-ssl documented required | OAUTH_VERIFY_LAST forceSslGranted=false; scopes upload+readonly only | **NOT FIXED** | Critical — videos.update unavailable |
| 13 | videos.update unavailable | 403 scope insufficient historically | Still unavailable without force-ssl | **NOT FIXED** | Critical |
| 14 | Canonical IDs not persisted immediately | Package upload persists registry | Code+tests; live shelf still drifted outside package path | **FIXED WITH MONITORING** | Medium if CDP used |
| 15 | Local registries disagreeing with YouTube | Aligned at POST_OAUTH | Registry still says BH trio public; live private; unexpected public extras | **NOT FIXED** | High |
| 16 | Old duplicate IDs remaining eligible for upload | Recovery blocks + registry | Fingerprint/content-id gates in package; CDP scripts can still upload | **PARTIALLY FIXED** | High |
| 17 | Held assets accidentally becoming publishable | Dec 31 holds | Held five still private+Dec31; PASS | **FIXED WITH MONITORING** | Low unless visibility CDP run |
| 18 | Public videos wrong privacy status | Shelf PASS | Shelf FAIL — 5/6 expected public wrong for BH; 2 expected private are public | **NOT FIXED** | Critical |
| 19 | Incorrect related-video relationships for Shorts | Studio finish required → 3xrxdmaOwJI | API cannot read Related; Studio not re-checked this audit | **UNVERIFIABLE** | Medium |
| 20 | Missing Studio finishing steps | STUDIO_MANUAL_FINISH.md remains | Still listed as remaining manual work | **PARTIALLY FIXED** | Medium |
| 21 | Incorrect made-for-kids settings | madeForKids false on samples | All sampled known IDs madeForKids=false | **FIXED** | Low |
| 22 | Incorrect thumbnails on episodes | Deferred historically | No automatic thumb replace; mapping not fully verified this audit | **UNVERIFIABLE** | Medium |
| 23 | Stale schedule records | Cadence docs vs API | Live schedule inventory captured; local cadence docs modified uncommitted — possible drift | **FIXED WITH MONITORING** | Medium |
| 24 | Hidden alternate publishing commands | youtube:package approved | youtube:upload still in package.json without recovery gates; docs mention it | **NOT FIXED** | High |
| 25 | Bulk replacement scripts remaining reachable | Four DISABLED__ | Only smooth-CFR quartet quarantined; JWST replace + audits/_replace_shorts_v02_youtube.py etc still present | **NOT FIXED** | Critical |
| 26 | Ambiguous upload failures causing blind retries | Package path stops + search-before-retry | Covered in youtube:package + tests; not in youtube:upload | **PARTIALLY FIXED** | Medium |
| 27 | Multiple packages pointing at same planned slot | NF01 collision held | Active vs held title pairs exist by design; Aug calendar dense | **FIXED WITH MONITORING** | Medium |
| 28 | One content package producing more than one YouTube ID | ONE VIDEO=ONE UPLOAD rule + registry | Rule+tests; live evidence shows many historical multi-IDs per title; risk remains via CDP | **PARTIALLY FIXED** | High |

Allowed statuses only: FIXED · FIXED WITH MONITORING · PARTIALLY FIXED · NOT FIXED · UNVERIFIABLE
