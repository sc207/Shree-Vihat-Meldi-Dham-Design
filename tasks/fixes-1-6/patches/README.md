# Patches for items 1–6 (on v109 `1791922103-42cb`)

- `*.site-css.diff` — the stylesheet change of each item (each item appends one commented block at the end of `project/site.css`;
  item 4 and later diffs are relative to the previous item, in order 1 → 2 → 3 → 4 → 5 → 6.1 … 6.5).
- Page-file (`.dc.html`) changes are made by `../scripts/apply_item2.py` … `apply_item6.py` (exact-string replacements, each asserted).
  Rebuild from v109: copy `design/project` to a working folder, append item 1 (`item1_seva_column.site-css.diff`), then run the scripts in order
  (`apply_item6.py <folder> 1` … `5`). The result equals `../project/` (checksums in `../project-SHA256SUMS.txt`).
- Which page files each item touches: see `../REPORT.md` §5.
