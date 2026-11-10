# J2486 — Design review: 023 Venus thumbnail B "465°C" (`VBaYRPp85Sw`)

**Verdict: FIX.** Do not arm the test with this file. J1198 stays waiting.

- Reviewed: `02_Video-Projects/023_What-Happened-To-Venus/08_Thumbnail/tc_B_465c/venus_tc_B_465c_VBaYRPp85Sw.jpg` at full size (1280×720), plus `venus_tc_B_465c_preview_sheet.jpg` and `venus_tc_A_vs_B_465c_sheet.jpg` at 168×94 next to A (MELTS LEAD) and the ended B (EARTH'S TWIN). Also the base plate and the builder script.
- Reviewer: macbook-2, Claude session, 10 Nov 2026. Independence note: J2484 was also logged under `macbook-2`, but its history says that run was "on gemini". This is a different model and a fresh session that judged the picture by eye, not from the builder's notes. If Chief wants a different agent id on it, the two FIX items below are objective enough to check quickly.
- Nothing was changed in Studio. £0.

## 1. Rubric (§2.B), by eye

| Check | Result | What I saw |
|---|---|---|
| HOOK | PASS, with a note | "465°C" is a number, not the object's name or a dare. Next to the title *What Happened to Venus?* it reads as the stakes, and it is the text Chief specified. It does not repeat the title. |
| BAND | PASS | One token, top-left, over cloud only. No letter touches the lander or the mountain. Yellow, heavy outline. Clear of the bottom-right corner. |
| GRADE | PASS on the numbers (245.5, near-black 15%) | See item 2: the number passes but the look is too hot. |
| PHONE | PASS | At 168×94 "465°C" is readable and the lander reads as a machine on a red glow. The text is smaller than A's two-line block, but legible. |

## 2. Saturation 245/255: rich or garish?

**Too hot. Part of the FIX.** The whole frame is one orange-red hue at near-full saturation. The sky and ground still read as a moody landscape, but the lander's underside and the ground beneath it are neon red and are the brightest, most saturated thing in the frame. Beside A (161.8) and the ended B (154.1) on the same sheet it is clearly the loudest of the three, and the loud part is exactly the part that is wrong on accuracy (item 3). Aim for about 170–200 after the fix, with the sky amber kept and the red pulled back.

**Not done:** the comparison with two competitors' thumbnails from the same search. This run had no competitor thumbnails to hand and did not fetch any. The fix job's reviewer should put the new file beside two search results for "what happened to venus".

## 3. Accuracy: FIX

The lander looks red-hot. Its whole lower section (under the brake ring, the legs, the base) glows bright red-orange from inside, with pink-white hot spots, and it lights the rocks around it. Cracks in the foreground rocks glow like lava embers. The upper sphere has a red hot patch too. The builder's own notes call it "incandescent", and the grade script adds more red there on purpose (`thermal_boost` +48 red around the lander, `sphere_glow` +34 red on the sphere).

465°C does not make metal glow visibly (that starts at about 525°C), and Venus's surface does not show glowing cracks. So the picture says "melting", not "hot".

**Fix:** the lander is lit only by the amber sky. No self-glow from the lander, no lit ground under it, no glowing cracks in the rocks. Keep the amber cast. Options, both £0:
1. Regrade from the same plate: drop `thermal_boost` and `sphere_glow`, and in the lander and foreground region pull strong reds toward the sky's amber and down in brightness until the underside is in shadow like the rest of the craft. Only works if the result still looks natural at full size; the glow is in the plate itself.
2. A new plate without the glow (see item 4 for what must be recorded this time).

After the fix the stakes must still read at phone size without the red glow. Heat haze, the heavy sky and the lone lander can carry it.

## 4. Provenance of the base plate: FIX (partly established)

What the file itself shows (C2PA manifest embedded in `venus_surface_glowing_lander_plate.jpg`, sha256 on record `8f5f2b84…2aac`):
- "Created by Google Generative AI", digital source type `trainedAlgorithmicMedia`.
- "Applied imperceptible SynthID watermark."
- Signed by Google C2PA Media Services, time-stamped **2026-11-10 04:43:59Z**, which is inside the J2484 run (file written 04:45 local record).
- 1376×768.

So the plate is an AI image made by a Google image model during J2484. It is **not** one of the "existing approved 023 Venus surface / Venera lander plates" that J2484's brief allowed, and META.json's "£0" was not backed by anything.

What could not be established: which tool or account made it (Gemini CLI's built-in image tool, Flow, Vertex) and that it cost nothing. No prompt, no log and no tool name is in the repo. I have written the known facts into `META.json` under `plate_provenance` with `status: "UNRESOLVED"`.

**Fix:** the fix job records the tool, the model, the prompt and the cost line for whichever plate it uses, in META.json. If the tool for this plate cannot be named and shown to be inside a subscription with no spend, do not use this plate. Note for Chief: an AI-generated Venera-style lander is on a thumbnail here; the video's altered-content disclosure covers the film, and Chief should say whether an AI plate is acceptable for a thumbnail at all, since J2484's brief asked for approved plates or a deterministic composite.

## 5. Orbit, extra words, corner

PASS. No Orbit. No words other than "465°C". Text is top-left; the bottom-right corner is plain rock.

## Not checked

- sha256 of the JPG against SHA256.txt (`shasum` needs approval in this worker run). Not needed for a FIX verdict; the fix produces a new file and a new hash.
- NAS mirror copy (the NAS path is outside this session's allowed folders). Same: only needed on KEEP.

## FIX list for the next job

1. Remove the lander's self-glow, the lit ground and the glowing rock cracks; keep the amber sky cast.
2. Bring mean saturation down to about 170–200; no neon red.
3. Record the plate's tool, model, prompt and £0 evidence in META.json, or use a plate whose source is recorded.
4. Re-run `thumb_preview.py long --score`, rebuild both sheets, new SHA256.txt, copy to the NAS mirror.
5. A fresh design review, including two competitors from the same search, before J1198 is reopened.

## Queue commands not run

`jobs.py` needs approval in this worker run, so these were not run. Chief, please run them:

```bash
python3 scripts/jobs.py add --title "023 Venus VBaYRPp85Sw: fix thumbnail B 465°C (no glowing lander, saturation 170-200, plate source recorded) per J2486" --needs macbook --repo owb --film 023 --stage thumbs --body "See jobs/reviews/J2486/REVIEW.md, FIX list 1-5. £0. Nothing in Studio. J1198 stays waiting until the fixed file passes a fresh design review." --git
python3 scripts/jobs.py done J2486 --agent macbook-2 --result "FIX (not KEEP): lander glows red-hot (465°C does not glow), saturation 245 too hot, plate is a Google generative AI image (C2PA, 10 Nov 04:43Z) with tool and cost unrecorded. Review in jobs/reviews/J2486/REVIEW.md. J1198 left waiting." --git
```
