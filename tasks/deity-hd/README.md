# ધામ પરિવાર pictures in HD, aligned — v125 (16 Oct 2026)

**Owner's request** (with a screenshot of the History chapter 2 row): "images not alligned and set properly. make sure those images should be HD
and if not make it hd that looks good and does not seems downgrade image quality".
The request handed the decision to Claude, so it was published as its own version: **v125 `1792094175-7284`** (v124 `1792093482-e8c1` was an
editor re-save with no content change; live files were checked byte-for-byte against v123 before publishing).

## What was wrong

| # | Picture | Original | Problem in the 4:5 arch frame |
|---|---|---|---|
| 03 | જય શ્રી વિહત માઁ | 760×905, painting on caramel | fills the frame; buffalo's feet cut by cover-cropping |
| 04 | જય શ્રી મેલડી માઁ | 670×921, painting on caramel | fills the frame; goat's feet cut |
| 05 | જય શ્રી લાખણેચી માઁ | 380×534, dark ring background | too small for the frame (blurry on 2× screens), figure lower and smaller |
| 06 | જય શ્રી ગોગા મહારાજ | 393×534, dark ring background | same as 05 |

Four sizes, four baselines, two backgrounds in one row.

## What was done

All four rebuilt **the same way** at **1200×1500** (exactly the 4:5 arch frame, so the browser crops nothing):

- one warm-gold background (`#b9793d → #ad6633 → #8e4c24`), a soft light `#f6cf8a` behind the head, a soft ground shadow;
- every figure 80 % of the picture height, standing on the same baseline (95.2 %), centred, and inside the arch top (checked pixel by pixel);
- વિહત માઁ and મેલડી માઁ from the HD cut-outs 21 (1768×2000) and 22 (1446×2000) — the same paintings as 03/04;
- લાખણેચી માઁ and ગોગા મહારાજ enlarged ×4 with **Real-ESRGAN x4plus** (compared with realesr-general-x4v3 and x4plus_anime_6B on the face —
  x4plus kept the painting's lines and colours most faithfully; [pictures/07_upscaler_comparison.png](pictures/07_upscaler_comparison.png)),
  then cut out with **IS-Net** and an alpha clean-up (soft edge 60–180) that removed a faint grey patch under the elephant.

New images (WebP, quality 90): 28 `6a5dfa42bf4395ad0c91358b6d58b309` · 29 `8c6bc0f2d3dd302001ff1f0156ef263c` ·
30 `64fea5310ba43b3bb3862a6fbc35b15d` · 31 `707057297d216df873c2b29940cce2e3` (files in [export/](export/) and `design/assets/`).
Pages changed (image addresses only): `History`, `HistoryMobile`, `Gallery` (grid, lightbox data, banner trio), `GalleryMobile`.
Old 03–06 stay in the artifact's image store for rollback.

## Pictures

- [01 History row, desktop](pictures/01_history_row_desktop_before_after.png) · [02 History row, phone](pictures/02_history_row_phone_before_after.png)
- [03 phone zoom, લાખણેચી માઁ + ગોગા મહારાજ](pictures/03_phone_lakhnechi_goga_zoom.png)
- [04 Gallery tiles, desktop](pictures/04_gallery_tiles_desktop_before_after.png) · [05 Gallery tiles, phone](pictures/05_gallery_tiles_phone_before_after.png)
  (the bottom bar over two phone tiles is the page's fixed bar, same before and after) · [06 Gallery banner trio](pictures/06_gallery_banner_before_after.png)

## Tests

- `tools/check_layout.py --boards History,HistoryMobile,Gallery,GalleryMobile`: 44 runs (1440 → 320 px, normal + large text), 0 new problems.
- `tools/frame_heights.py` on the same boards: 0 to change. Wording diff (`gen_page_content.py`): no text change.
- No page refers to 03–06 any more. Published files read back byte-identical; the server's image checksums match `design/assets/`.

## Rebuild (from the repository root)

```bash
# 1. upscale (models are not in the repo: official Real-ESRGAN release weights; no PyTorch needed)
python3 tasks/deity-hd/scripts/sr_onnx.py RealESRGAN_x4plus.pth lakh_src.png lakh_x4plus.png --tile 128
# 2. cut out (isnet-general-use.onnx, the DIS / rembg model)
python3 tasks/deity-hd/scripts/cutout.py isnet-general-use.onnx lakh_x4plus.png lakh_cut.png
# 3. compose all four (uses 21/22 from design/assets and the saved cut-outs in cutouts/, lossless) -> OUTDIR/{vihat,meldi,lakhnechi,goga}.png
python3 tasks/deity-hd/scripts/compose.py OUTDIR
# 4. WebP: Image.open(png).save(webp, quality=90, method=6)  -> byte-identical to export/
python3 tools/examples/apply_v125_deity_hd.py <project folder>   # swaps the four image addresses
```

`lakh_src.png` / `goga_src.png` = images 05 / 06 from `design/assets/`. Needs `onnx`, `onnxruntime`, `numpy`, `Pillow`
(`pip install --break-system-packages …`).
