# v110 — new photo of ભગવાન શ્રી કરમશીબાપા (14 Oct 2026)

Owner's request (phone screenshot of the "૦૧ · મુખ્ય પૃષ્ઠ" board, two new photos): use the photo that fits instead of the close-up, in good quality.

- `originals/` — the owner's two photos as received (1086×1448 PNG each). **Used:** `karamshibapa_blessing_bust_owner-2026-10-14.png` (half-length, blessing
  hand, 3:4 like the arch frames). **Not used:** `karamshibapa_blessing_seated_owner-2026-10-14.png` (full seated figure; the face would be very small in the
  small arches) — kept for the gallery if the owner wants it later.
- `export/27_portrait_karamshibapa_blessing-glow.webp` — the published image: WebP q92, method 6, 1086×1448, 138,656 bytes,
  sha256 `24bd8184e0b7376fbae0936d49e66e713bb29866c595b3e804a28599173f5bb9`; asset `/_blob/0719d6d6a37c83a09b9880ba4507c70f` (copy in `design/assets/`).
  Face-area PSNR vs. the original 39.9 dB (visually identical). No AI enlargement: native resolution is sharp at ≥ 2.47× on every frame (≥ 2.73× on phones).
- Page change: `tools/examples/apply_v110_karamshibapa_photo.py <project>` — swaps the image address in 9 page files (14 places); nothing else.
- `scripts/measure_frames.py PORT BLOBID [OUTDIR]` — frame boxes, crop and sharpness limit per frame; `scripts/shots_pair.py BASE NEW OUTDIR` — before/after of the
  sections; `scripts/diff_inside_frames.py BASE NEW BLOBID` — changed pixels must lie inside the photo frames (home ribbon motion masked).
- Results: `diff_inside_frames.log`, `layout_home.log` + `layout_hg.log` (72 runs, 0 new problems), `pixel.log` (15 other boards identical; MenuMobile = known noise).
- `pictures/` — before/after (v109 → v110) for Home phone/desktop, History desktop/phone, Gallery banner, Home photo strip, and every frame at once.
