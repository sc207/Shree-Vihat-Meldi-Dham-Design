# ભગવાન શ્રી કરમશીબાપા — photo in HD (v146) and in focus (v147), 16 Oct 2026

**Owner:** "karamshi bapa image actually looks like ai generated … suresh bapa image how their skin tone and actual looks original. same hd and
humanize image set for karamshibapa image. if have same image in other pages also fix over there" — then, with a screenshot of the blessing photo:
"make it feels image and person skin real just like we have fixed the suresh bapa image made it hd and glow skin and all".

## What was found

Image 27 (the owner's photo of 14 Oct, `tasks/bapa-photo/originals/…bust…png`) was published exactly as supplied in v110 — no processing.
At full size its skin already shows a generated "crackle" texture and smoothing; the seated photo from the same set looks the same.
સુરેશબાપા's photos looked real after HD because their originals were camera photos.

## Options shown to the owner — [pictures/options_A_B_C.png](pictures/options_A_B_C.png)

| | Picture | Result |
|---|---|---|
| A | keep 27 as it is | — |
| **B** | **27 through the same HD step as સુરેશબાપા's (x4plus, halved) + photographic finish** | **chosen by the owner** |
| C | his genuine camera photo 08 (white background) cut out, whites' blue cast corrected, on the same golden glow — no AI | prepared, not used: `export/alt_C_real-photo-08_natural-glow_not-used.webp`, `scripts/compose_karamshi.py` |

## B — how 38 was made

1. `tasks/deity-hd/scripts/sr_onnx.py RealESRGAN_x4plus.pth 27_src.png 27_x4plus.png --tile 128` (4344×5792, 505 s on 2 CPU cores)
2. `scripts/photo_finish.py 27_src.png 27_x4plus.png OUT 0.45 3.2` — halved to exactly 2× (2172×2896), gentle large-radius clarity on mid-tones,
   fine monochrome grain (stronger on the subject than on the glow)
3. saved at 1.5× = 1629×2172 WebP q90 (257 KB): every frame ≥ 1.36× the pixels needed, even on 3× phones; same 3:4 shape as 27, so no frame changes.

Asset `/_blob/12fd255804899d0ead71c2e9e83930e0` (copy in `design/assets/`), replacing 27 in 14 places on 9 pages
(`tools/examples/apply_v146_karamshibapa_hd.py`). Before/after: [History face, real screen pixels](pictures/v146_history_face_before_after.png).

## v147 — the blessing hand and the face in focus

**Owner** (after v146): "it looks good. just now sharp that image as you can see if we zoom see blessing hand it does not looks in focus. so do it
as we did in suresh bapa." — then: "as like blessing hand also focus on face so it looks more better and also check if sharpness required or not".

Check (focus ratio = fine detail ÷ medium detail of the brightness, at 2×; a soft area scores low whatever its content):

| Area | 38 (v146) | 39 (v147) | |
|---|---|---|---|
| fingers | 0.32 | 0.45 | soft in the supplied photo already |
| whole hand | 0.35 | 0.51 | |
| face | 0.56 | 0.79 | sharpest part; light touch on request |
| eyes | 0.51 | 0.70 | |
| turban | 0.46 | 0.56 | checked at 1:1: folds crisp — **no sharpening needed**; rises only from the 2× size |
| clothes | 0.45 | 0.53 | no sharpening needed |

How 39 was made (`scripts/make_38_sharp.py SRC X4PLUS OUT`, masks in `scripts/hand_focus.py`):
1. the same x4plus result halved to exactly 2× (2172×2896) — kept at 2× like સુરેશબાપા's 34 (38 was shrunk to 1.5×);
2. hand, rings and wrist: edge sharpening at two radii (1.2 px creases, 3 px outlines; 0.9 / 1.3), each pixel kept inside its 9×9 neighbourhood's
   own range so no bright or dark rims appear; limited to skin and the two rings — without that a light line appeared round the thumb and fingertips;
3. face, eyes, moustache and ear-rings: the same at 0.4 / 0.9 (0.9 / 1.3 made the skin crackle harsh);
4. the photographic finish of 38 (clarity 0.45, grain 2.6 instead of 3.2 because there is no shrink afterwards), WebP q90 → 448 KB.

Tried and not used: Richardson–Lucy deconvolution (dark rims round the fingers); x4plus on a pre-shrunk hand (smoother, creases lost).
Colour unchanged (mean RGB of face and palm within 0.5); shrunk back to the original 32.5 dB (38: 34.2 — the difference is the added edge contrast and grain).

Asset `/_blob/3cc36279d9180905d49a932af9ea9e1a` (`export/39_…_hand-focus.webp`, copy in `design/assets/`), replacing 38 in the same 14 places
(`tools/examples/apply_v147_karamshibapa_hand_focus.py`). Before/after: [History on a phone, pinch-zoomed 2×](pictures/v147_hand_face_zoom_before_after.png).

## Note

The site's version count jumped from v138 to v146: the editor saved seven times (v139–v145) while the owner had the canvas open; those saves only
re-wrote no-break spaces as `&nbsp;` (checked character by character). v146 was built on those live files.
