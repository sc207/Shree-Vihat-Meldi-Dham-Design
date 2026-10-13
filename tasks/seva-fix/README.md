# Seva desktop help column — working version on v109 (not published)

- Base: live v109 `1791922103-42cb` (repo `668bb3a`, checksums verified 14 Oct 2026).
- Change: 3 rules appended at the end of `project/site.css` ([seva_on_v109.diff](seva_on_v109.diff)); no other file.
- Root cause: on desktop (≥1000 px) the form is ~2,100 px tall and the help column ~1,000 px, so the right half is empty beside section 3;
  the section's `overflow: hidden` also creates a scroll container that would stop a sticky card from following.
- Fix: the column stretches to the form's height, the last card "સહાયની જરૂર છે?" is sticky below the compact header, and the section
  uses `overflow: clip` (same clipping, no scroll container).
- Checks (Chromium only, 14 Oct 2026): 24/26 scroll positions at 1440/1024 — card never overlaps a field or the form (64 px gap), stays in its
  column, stops 96 px above the footer; empty-right-column positions 6–7 → 0 at 1024/1100/1280/1440; other sticky/fixed elements unchanged;
  no decorative element reaches outside the section; static page identical outside the card (1 px antialiasing at 1024); all other 22 boards
  pixel-identical (MenuMobile load noise confirmed by self-compare); check_layout 22 runs 0 problems; frames unchanged; wording identical.
- Not verified: Safari/WebKit (sticky inside `overflow: clip` needs Safari 16+; older Safari keeps v109 behaviour), real devices, Claude Design canvas
  (the canvas does not scroll the board, so the sticky effect is not visible there).
- Status: awaiting the owner's review. Publishing needs a separate approval.
