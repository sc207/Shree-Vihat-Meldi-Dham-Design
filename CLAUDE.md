# CLAUDE.md — Shri Vihat Meldi Dham website (Gujarati)

Permanent instructions for any Claude session working on this project. Start with [NEXT_SESSION.md](NEXT_SESSION.md).

## What this is

The official **Gujarati-only** website design for **શ્રી વિહત મેલડી ધામ, ગેપ્પરા, સાણંદ**, with the
મૂર્તિ પ્રાણ પ્રતિષ્ઠા મહોત્સવ (તા. ૨ થી ૮ ફેબ્રુઆરી, ૨૦૨૭; પ્રાણ પ્રતિષ્ઠા ૮ ફેબ્રુઆરી, બપોરે ૧૨:૩૯).

## Where the truth lives

| What | Where | Role |
|---|---|---|
| **Website design (source of truth)** | Claude Design artifact `https://claude.ai/artifact/HWR4J5u9qBPjri6oUg7nVa` (type "Design"), files under `project/` | The live design. Every published change is a numbered version there, with full history for rollback. |
| Snapshot of the design | `design/project/` + `design/assets/` in this repo | Verified byte-for-byte copy of the version named in [PROJECT_STATE.md](PROJECT_STATE.md). Backup and diff base — **not** a second source of truth. Refresh it after each published version. |
| Spec / review page | `https://claude.ai/artifact/XzsLf5Ef672Cwr1i9QDJNW` | Before/after pictures and decisions for review; not part of the website. Source: `tasks/spec-page/`. |
| Audit report page | `https://claude.ai/artifact/FJjnL8j4NB95mK2tcSjQuU` | Design audit of v106 with status updates; source `tasks/audit-v106/audit-page.html`. |
| Design-system origin | `https://claude.ai/artifact/7PGYwFXqvGuHKZiU2XFMbn` | The system copied into `project/ds/vihatmeldimandir/` (tokens + component CSS). |
| Figma library (later sync) | Figma file key `0AYx0wwuBl0zZZ57xjJbIu`; scripts in `figma/` | Gate A component work, paused by the Figma Starter plan's call limit. Not a prerequisite for website work. |

## Rules (from the project owner — do not relax them)

1. **Gujarati only** on the site. No invented content. Unknown facts stay as `[square-bracket placeholders]`.
2. Respectful temple language. Keep existing approved wording and the date format. No new devotional copy unless the trust supplies it.
3. **Publish only with the owner's approval.** If the owner's request itself hands you the decision (e.g. "add it to the design, it's on you"),
   that request is the approval for that change — afterwards report exactly what changed. Otherwise show the change (before/after pictures) first.
   One change = one published version. The previous version stays for rollback.
4. Do not touch Figma until the agreed allowance check (see [NEXT_SESSION.md](NEXT_SESSION.md)). Do not upgrade any plan. Do not edit or delete the scheduled reminder.
5. Preserve unrelated pages, existing design, copy and behaviour. Smallest possible change.
6. Removed items stay removed. Placeholders stay until the trust provides the content.
7. Never put passwords, tokens or keys in this repo.
8. If the live design version is newer than the one recorded in [PROJECT_STATE.md](PROJECT_STATE.md), the owner edited it in the editor:
   re-read the live files and build on them — never overwrite the owner's edits.

Content rules in detail (names, spellings, reserved lines, dates): [DESIGN_SYSTEM.md → Gujarati wording](DESIGN_SYSTEM.md#gujarati-wording-names-and-spelling).

## How to work (short version — full steps in NEXT_SESSION.md §8)

Run everything from the repository root. Scratch folders `work/` (your edited copy) and `base/` (baseline when live is newer) are git-ignored.

1. `Artifact list` (scope files) on the website URL → the result's first line shows `(version <id>)`; compare with PROJECT_STATE.md.
2. Make a **full** working copy: `cp -r design/project work/project` when the version matches; otherwise read all 28 live files (NEXT_SESSION.md §8).
3. Edit with a small Python script: exact-string replacements, each asserted to occur once (see `tools/examples/`).
   Desktop and phone pages are separate files (`Page.dc.html` + `PageMobile.dc.html`; home = `Main`, `HomeTablet`, `HomeTabletL`, `HomePhoneL`, `HomeMobile`, `HomeMobile2`).
   Change all variants. New CSS goes at the **end** of `project/site.css` as a commented block.
4. Preview locally (`tools/serve.py`), then run the focused checks in [TESTING.md](TESTING.md): `check_layout.py` and `frame_heights.py` on touched boards,
   a wording diff with `gen_page_content.py`, `pixel_regress.py` when CSS changed.
5. On approval: `Artifact read` the website once (the tool refuses to publish to an artifact the conversation has not read), publish
   (`url`, `root` = `<repo>/work`, `file_path`, `files` = changed files only), verify live checksums, refresh `design/`, update
   [CHANGELOG.md](CHANGELOG.md) and [PROJECT_STATE.md](PROJECT_STATE.md), commit.

## Commands

```bash
npm install --prefix work @fontsource/noto-serif-gujarati @fontsource/hind-vadodara        # Gujarati fonts for local renders
python3 tools/serve.py --project design/project --assets design/assets --runtime <path printed by Artifact read of artifact-type/dc-runtime.js> \
                       --fonts work/node_modules/@fontsource --port 8771                     # baseline (base/project if live is newer)
python3 tools/serve.py --project work/project --assets design/assets --runtime <same> --fonts work/node_modules/@fontsource --port 8772
python3 tools/check_layout.py --base 8771 --new 8772 --boards NewTemple,NewTempleMobile
python3 tools/frame_heights.py --port 8772 --project work/project --boards NewTemple,NewTempleMobile
python3 tools/pixel_regress.py --base 8771 --new 8772 --project work/project [--boards A,B]
python3 tools/gen_page_content.py design/project PAGE_CONTENT.md "design vNNN (<version-id>)"
(cd design/project && sha256sum -c --quiet ../SHA256SUMS.txt) && (cd design/assets && sha256sum -c --quiet SHA256SUMS.txt)
```

## Documentation map

- [NEXT_SESSION.md](NEXT_SESSION.md) — start here: state, first action, safe workflow
- [PROJECT_STATE.md](PROJECT_STATE.md) — versions, open tasks, known issues
- [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) — colours, type, layout, breakpoints, components, images, Gujarati wording rules
- [PAGE_CONTENT.md](PAGE_CONTENT.md) — every text on every page (generated), with all open placeholders
- [CHANGELOG.md](CHANGELOG.md) — what changed in each version and how it was tested
- [TESTING.md](TESTING.md) — tools, viewports, checks, known limitations, last results
- [tasks/audit-report-v106.md](tasks/audit-report-v106.md) — design audit findings (P0–P3), root causes and the proposed fix plan
- [DEVELOPER_HANDOFF.md](DEVELOPER_HANDOFF.md) — for the coding team: routes, one responsive page per route, canvas-only parts to strip, breakpoints, behaviour, images (`handoff/assets.json`), acceptance checks
- [tasks/responsive-v116/README.md](tasks/responsive-v116/README.md) — device scan (34 sizes) and fixes v118–v123
