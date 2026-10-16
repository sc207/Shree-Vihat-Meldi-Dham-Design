# Image check of the whole site — v126–v128 (16 Oct 2026)

**Owner's request** (after v125, the ધામ પરિવાર pictures): "also check other images have this issue" — the issue being pictures that are
not aligned / not set properly / not HD. Each fix was published as its own version (CLAUDE.md rule 3: the request hands the decision over).

## How every picture was checked

- `scripts/measure_images.py PORT OUT.json` — every `<img>` on every board: 9 desktop pages at 1920 / 1440 / 1180 / 1024 / 834 / 768 px,
  12 phone pages at 430 / 390 / 360 / 320 px, plus the three home boards at their own size. For each: drawn size, real pixels, `object-fit`,
  how much is cropped, and **sharpness = real pixels ÷ pixels needed** (2× screens; 3× for phones). Below ~0.8 a picture looks soft.
- `scripts/summarise.py OUT.json` — worst placement per image. `scripts/measure_lightbox.py` — the same for the Gallery photo viewer.
- `scripts/shot_placements.py` — screenshot of every frame an image sits in, to judge cropping and alignment by eye.
- Results: [results/measure_v125.json](results/measure_v125.json) (before), [results/measure_v127.json](results/measure_v127.json) (after),
  [results/lightbox_sizes_v125.json](results/lightbox_sizes_v125.json), viewer tests `results/viewer_v125.json` / `viewer_v126.json`.

## Findings (on v125) and what was done

| Image | Worst sharpness | Where | Verdict |
|---|---|---|---|
| Gallery photo viewer (all photos) | — | Gallery, GalleryMobile | **Fixed in v126** — opened at the top of the page (off-screen for 240 of 242 test openings), photo 214 px wide on phones, ✕ below a 900 px laptop screen |
| 13 સુરેશબાપા smiling cut-out 470×501 | 0.45 | Gallery tall tile, viewer 0.50 | **Fixed in v127** → 32 (940×1002) |
| 11 સુરેશબાપા candid 585×882 | 0.65 (viewer), 0.77 (tile) | Gallery, History small portrait | **Fixed in v127** → 33 (1170×1764) |
| 09 કરમશીબાપા seated poster 784×1045 | 0.77 (viewer) | Gallery news card, tile, viewer | **Left as supplied** — both upscalers drew new dark outlines on his face and neck ([picture](pictures/upscaler_09_karamshibapa_rejected.png)); needs a larger original from the trust |
| 14 new-temple render 2400×1881 | 0.66 | NewTemple 834 px zoomed crop only (≥ 0.82 elsewhere) | Left — slightly soft in one tablet crop; AI sharpening could invent carving details on an architectural design |
| 10 સુરેશબાપા blessing 1100×1019 | 0.64 on 3× phones (0.87–0.96 on 2×) | Home pair + strip, History arch, Gallery | **Fixed in v128** → 34 (2200×2038), same method as v127 |
| 27, 08, 12, 15, 01, 02, 28–31, logos, QR | ≥ 0.91 | everywhere | Sharp |

Gallery grid, Home and History pairs and the news cards were also checked by eye for cropping and alignment: no other problem
([gallery grid](pictures/gallery_grid_1440_v125.png)).

## v126 — gallery viewer

`site.css` block (script `tools/examples/apply_v126_gallery_viewer.py`): `position: fixed`, centred, `overflow-y: auto`, z-index 95 (same idea as
the phone menu `.vm-mnav`); image area `min(680px, 100dvh − 176px)`; ≤ 760 px: 16 px margins, 12 px panel padding, photo `width: 100%` with
`max-height: 100dvh − 150px`; landscape phones (`max-height: 500px`): compact panel.
Test `scripts/test_viewer.py PORT OUTDIR [--shots]`: 11 photos × 11 screen sizes × 2 text sizes — panel and ✕ on screen **242/242** (v125: 2/242).
Pictures: [phone, lower photo](pictures/v126_viewer_phone_lower_photo.png) · [phone, top photo](pictures/v126_viewer_phone_top_photo.png) ·
[laptop 1440×900](pictures/v126_viewer_desktop_1440x900.png). **v131** completed it: Escape and a tap on the dark area close it, focus moves to ✕ and back to the photo
(`scripts/test_viewer_keys.py`: 84/84 checks; v129: 64 fail).

## v127 — two portraits in HD

Method (`scripts/make_hd_portrait.py SRC X4PLUS OUT`): Real-ESRGAN **x4plus** (run without PyTorch: `tasks/deity-hd/scripts/sr_onnx.py`),
then halved with Lanczos → exactly **2×** the original. Halving keeps the sharper edges and removes most invented fine detail. Cut-out alpha
= the original alpha enlarged 2×. WebP quality 90, method 6.

Faithfulness checks (`scripts/portrait_compare.py NAME x0 y0 x1 y1`):
- face crops at 1:1 against a plain enlargement — eyes, moustache, wrinkles, tilak, ear-ring, ring and beads unchanged
  ([13](pictures/upscaler_13_sureshbapa_cutout.png), [11](pictures/upscaler_11_sureshbapa_candid.png), [hand](pictures/v127_candid_hand_detail.png));
- shrunk back to the original size the HD versions match the originals at 36.5 / 36.6 dB PSNR;
- realesr-general-x4v3 rejected (smoothed the skin: 33.7 / 35.0 dB, visibly "plastic");
- cut-out edge on light and dark grounds: no fringe ([picture](pictures/v127_cutout_edges_check.png)).

In place: [cut-out tile](pictures/v127_sureshbapa_cutout_tile_before_after.png) · [candid tile](pictures/v127_sureshbapa_candid_tile_before_after.png).
Checks: `check_layout.py` History/Gallery + phone 44 runs, 0 new problems; frames 0 to change; wording unchanged; server checksums match.

## v128 — the blessing photo in HD

The re-measure after v127 ([results/measure_v127.json](results/measure_v127.json)) left 10 at 0.64 on 3× phones, so it got the same treatment:
34 = exactly 2× (x4plus halved). Face: [comparison](pictures/upscaler_10_sureshbapa_blessing.png) (38.9 dB shrunk back), hand and rings:
[detail](pictures/v128_blessing_hand_detail.png). In place: [Home pair](pictures/v128_blessing_home_before_after.png) ·
[History, phone](pictures/v128_blessing_history_phone_before_after.png). Swapped in 14 places on 9 boards; layout check 66 runs, 0 new problems.

After v128 every picture on the site is at least 0.91 of the pixels a 2× / 3× screen needs, except 09 (left as supplied, see above) and the
zoomed tablet crop of 14.

## Still open

- 09 કરમશીબાપા seated poster: ask the trust for a larger original (at least 1600 px wide).
- Real sites should serve several sizes per image (`srcset`) — see DEVELOPER_HANDOFF.md §5.
