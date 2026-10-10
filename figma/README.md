# figma/ — Gate A build scripts (paused)

Figma file key `0AYx0wwuBl0zZZ57xjJbIu` (pages: Read-me & Foundations `5:2`, Components `5:3`, Pages `0:1`).
`state.json` is the ledger: node ids, what is built (foundations, C1–C3), what remains (C4–C8, read-me board, images, QA), locked decisions,
safeguards, run order, and the website versions that Figma must later be synced with (`figma_sync_todo`).

- `scripts/callN.js` = `scripts/prelude.js` + `scripts/bodyN_*.js`, each sent as ONE `use_figma` call (Starter plan: 20 calls/month; read-only calls count).
- Run order: call1 → inspect its screenshots → call2 → call3 → call4 → inspect; call5 only after the owner has dropped the 26 original images
  (original file names) onto the Components page; call6 builds a report-only "QA · Phone widths" board.
- `call2_with_strip_fix.js` / `fix_strip.js` only if call 1 shows the long phone-strip text **and** the owner approves the correction.
- Before any of this: one read-only check of the allowance; if blocked, stop. Load the Figma "figma-use" skill before calling `use_figma`.
- These scripts describe the Gate A design as applied to the website in v97 (10 Oct 2026). Website changes v99–v106 are not in them yet (`figma_sync_todo`).
- The owner drops the images with their ORIGINAL names `<NN_name>__<blob-id>.<ext>`. To recreate that ZIP from this repo:
  `python3 tools/rebuild_image_zip.py design/assets figma/scripts/body5_images.js images.zip` (byte-identical to the original).
- Paths inside `state.json` such as `gateA/…`, `apply_*/`, `zipout/` refer to the old session's workspace and are not in this repo
  (equivalents: `tools/examples/`, `design/`, `tools/rebuild_image_zip.py`).
