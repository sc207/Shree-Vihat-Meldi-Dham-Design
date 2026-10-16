# ભગવાન શ્રી કરમશીબાપા — photo in HD (v146, 16 Oct 2026)

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

## Note

The site's version count jumped from v138 to v146: the editor saved seven times (v139–v145) while the owner had the canvas open; those saves only
re-wrote no-break spaces as `&nbsp;` (checked character by character). v146 was built on those live files.
