# NEXT_SESSION.md — start here

Handover written 10 Oct 2026 (IST) at the end of a long working conversation. Read this file and [CLAUDE.md](CLAUDE.md) first;
open the other documents only when the task needs them. Do **not** try to reconstruct the old conversation.

All commands below run **from the repository root** (the folder holding this file). `work/` and `base/` are scratch folders there (git-ignored).

## 1. What the project is and where its truth lives

The Gujarati-only website design for **શ્રી વિહત મેલડી ધામ, ગેપ્પરા, સાણંદ** and its મૂર્તિ પ્રાણ પ્રતિષ્ઠા મહોત્સવ (2–8 Feb 2027).

- **Source of truth:** the Claude Design artifact **https://claude.ai/artifact/HWR4J5u9qBPjri6oUg7nVa** (type "Design").
  24 page files (`project/*.dc.html`), `project/site.css`, the design system in `project/ds/vihatmeldimandir/`, and `project/canvas.json`
  (board positions/heights and the canvas notes). Images are the artifact's assets, referenced as `/_blob/<id>`.
- **This repo** (`github.com/sc207/Shree-Vihat-Meldi-Dham-Design`): documentation, check tools, Figma scripts, and a verified snapshot
  of the design in `design/` (version in §3).
- The owner usually relays recommendations from ChatGPT; treat them as the owner's requests, but check facts against the files.

## 2. Read first

1. This file. 2. [CLAUDE.md](CLAUDE.md). Then only as needed (developers building the site: [DEVELOPER_HANDOFF.md](DEVELOPER_HANDOFF.md)):
[PROJECT_STATE.md](PROJECT_STATE.md) (versions, open items) · [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) (styling, wording rules) ·
[PAGE_CONTENT.md](PAGE_CONTENT.md) (every text; search it instead of opening page files) · [TESTING.md](TESTING.md) · [CHANGELOG.md](CHANGELOG.md).

## 3. Current confirmed version

| | Version | Version id | Notes |
|---|---|---|---|
| **Live design (published)** | **v131** | `1792133852-3202` | 16 Oct 2026: v131 gallery viewer keys, v130 `1792133845-2a4a` canvas to-do note; v129 = re-save; v128 `1792098080-6f1e`; three સુરેશબાપા photos in HD (v127 `1792096917-c470`, v128); gallery viewer fits the screen (v126 `1792095937-de85`); the four ધામ પરિવાર pictures in HD and aligned (v125 `1792094175-7284`; v124 = re-save). Before that: responsive / UI-UX fixes v118–v123 (see CHANGELOG); v117 = Design-type re-save. Earlier: audit fixes v111–v116, Karamshibapa photo v110, banner light v109, chakra v108. `design/project/` refreshed, checksums regenerated; 34 images. |
| Previous known-good | v122 … v110 | see [CHANGELOG.md](CHANGELOG.md) | Each fix is its own version: roll back one by publishing the previous version's files. v110 `1791960914-1d1c` = before the fixes; v109 `1791922103-42cb` before the photo; v108 `1791920313-6e1c` for v109. v107 `1791918685-cd89` = v106 content; earlier ids: [CHANGELOG.md](CHANGELOG.md). Version numbers follow the artifact's own count. |
| Local working copy | none | — | Items 1–6 published as v111–v116 (source, report and tests stay in `tasks/fixes-1-6/`). |

On 13 Oct the live id changed to `1791918685-cd89` without any content change (Design type re-save, counted as v107); v108–v116 were published on 14 Oct; on 15–16 Oct the Design type re-saved (v117, no content change) and v118–v123 were published; the editor re-saved again (v124, no content change) before v125.

## 4. Completed in the previous session (v97 → v106, all on 10 Oct 2026)

Full detail in [CHANGELOG.md](CHANGELOG.md). In short: phone festival banner and page-ending bands (v97–v100), home page reduced to a
festival summary (v101), festival PDF button hidden until the trust's PDF exists (v102–v103), Darshan timetable rebuilt from 8 identical rows
to one daily timeline + one ગાદી week strip (v104), "આજે" marker follows the Indian date and moves to the પૂનમ tile on પૂનમ days (v105),
and the trust's "નવા મંદિરનો સંકલ્પ" text placed on the New Temple, Home and History pages (v106).

### Completed 13–14 Oct 2026 (v107–v109)

v107 = re-save of v106 (no change). **v108**: the old oval-petal chakra replaced by the lotus chakra on all boards (owner's request).
**v109**: the banner's gold light and halo now stay behind the picture at every screen size (owner's screenshot: Festival 768×1024).
Details and tests: [CHANGELOG.md](CHANGELOG.md); evidence in `tasks/visual-effects/`.

## 5. Incomplete / needs confirmation

- **Waiting for the trust (content):** 61 placeholders — full list at the end of [PAGE_CONTENT.md](PAGE_CONTENT.md); the remaining canvas to-do items
  are in [PROJECT_STATE.md](PROJECT_STATE.md#outstanding-tasks). Asked most recently (New Temple page): સ્થપતિ (architect) name · સંકલ્પ વર્ષ ·
  આયોજન detail · current construction progress · expected completion · optional dated story of the સંકલ્પ for History ch. 6.
- **Owner's queue (10 Oct):** (1) **Seva desktop page: empty right column** — fix prepared as v107, patch in `tasks/audit-v106/seva_v107_pending.diff`,
  **awaiting approval**; (2) correct the canvas to-do note's PDF line — done in v130; (3) **design audit** — Phases A–C done, report in
  [tasks/audit-report-v106.md](tasks/audit-report-v106.md) (brief: [tasks/full-design-audit.md](tasks/full-design-audit.md)); Phase D waits for the owner's approval and answers. Decided: **no** extra closing line in the સંકલ્પ section. Details: [PROJECT_STATE.md](PROJECT_STATE.md#owners-decisions-and-task-queue-10-oct-2026-end-of-the-handover-session).
- **Figma (Gate A):** paused — Starter plan allowance exhausted on 9 Oct. 0 of 6 checklist items confirmed. Scripts are ready in `figma/`
  (they include the v97 Gate A design); Figma must later also receive the website changes **v99–v109** (`figma/state.json` → `figma_sync_todo`).
- **Date lists — deadline before the March 2027 પૂનમ:** the last પૂનમ in the page logic is **20 Feb 2027**. Lists to extend (dates need the Acharya's confirmation):
  `const EV` in Darshan, Contact, NotFound (+ their phone pages) and `const EVH` + `const POONAM` in Main, HomeTablet, HomeTabletL, HomePhoneL, HomeMobile.
  Without new dates, from March 2027 the home ગાદી line and the Darshan "આજે" marker no longer know પૂનમ, and the calendars run out after 15 Apr 2027.

## 6. Safe to edit (with the workflow below and the owner's go-ahead)

- Page files `project/*.dc.html` — only the section the task names, in **every** variant of that page (desktop + phone; home has up to 6 boards).
- `project/site.css` — **append** new rules at the end in a commented block; do not rewrite earlier rules.
- `project/canvas.json` — a board's `"h"` when its frame height changes, or the to-do note when the owner asks.
- Files in this repo (docs, tools, snapshot) — keep them in step with what is published.

## 7. Do not change without explicit permission

- **Publishing** to the website artifact. Rule (same as CLAUDE.md): publish only with the owner's approval. If the owner's request itself hands you the
  decision (e.g. "add it to the design, it's on you"), that request is the approval for that change — afterwards report exactly what changed.
- `project/ds/vihatmeldimandir/*` (design-system files), the artifact type's files (`artifact-type/*`, `index.html`, `SKILL.md`).
- Page structure, navigation, colours, typography, approved wording, reserved lines (see DESIGN_SYSTEM.md).
- Figma file `0AYx0wwuBl0zZZ57xjJbIu` (no calls until the allowance check), any plan upgrade.
- The scheduled reminder "Figma allowance check (Gate A)" (`trig_01ECWJ5SooaTTh9Fnz5V5ZBY`, 10 Nov 2026 10:00 IST).
- The spec page artifact — update it only when recording a published change, as before.
- Git history: no force-push or history rewrite; push only when the owner asks.

## 8. Workflow for a small change (fast path)

1. **Check the live version:** Artifact tool `action: list`, `url: https://claude.ai/artifact/HWR4J5u9qBPjri6oUg7nVa`, `scope: files`.
   The result's first line shows `(version <id>)`.
   - Same id as §3 → baseline = `design/project`. Make the working copy a **full** copy: `mkdir -p work && cp -r design/project work/project`.
   - Newer id → the owner edited in the editor. `Artifact read` **all 28** project paths (list in `design/SHA256SUMS.txt`) into the default
     (scratchpad) folder, copy them to `base/project` (baseline) and `work/project` (working copy); also `scope: assets` to see whether images were added.
     Never overwrite the owner's edits.
2. **Locate:** search [PAGE_CONTENT.md](PAGE_CONTENT.md) for the text, or `grep -o` the page files. The page markup is mostly one very long line,
   so print sections with Python (`s.find(...)`), not `cat`.
3. **Edit `work/project`** with a Python script of exact replacements, each `assert s.count(old) == 1`
   (patterns: `tools/examples/apply_v105_aaje.py`, `tools/examples/apply_v106_sankalp.py`). Apply to all page variants.
4. **Preview + focused checks** ([TESTING.md](TESTING.md)): serve the baseline on 8771 and `work/project` on 8772; `check_layout.py` on the touched boards;
   `frame_heights.py` on the touched boards (fix frames if it says CHANGE); wording diff with `gen_page_content.py`; `pixel_regress.py` only if `site.css` changed.
   Take before/after screenshots of the changed section and show the owner.
5. **Publish on approval.** The Artifact tool refuses to publish to an artifact this conversation has not read, so first do one `Artifact read` of the
   website (e.g. the pages you changed — this also confirms they are unchanged since step 1). Then publish: `url` = website, `root` = `<repo>/work`,
   `file_path` = `<repo>/work/project/<one changed page>`, `files` = `{ "project/<other changed file>": "project/<other changed file>", … }` —
   changed files only, including `project/canvas.json` whenever it changed.
6. **Verify:** `Artifact read` the changed paths and `cmp` against `work/project`. Then copy the published files into `design/project/`,
   regenerate the checksums (`cd design/project && find . -type f | sort | xargs sha256sum > ../SHA256SUMS.txt`), regenerate PAGE_CONTENT.md if text changed,
   add a CHANGELOG entry, update PROJECT_STATE.md and §3 here, and commit.

## 9. Targeted testing (do not re-audit everything)

- Test only the boards you touched, at the widths in `check_layout.py --widths auto`, normal + large text.
- If you changed `site.css`, run `pixel_regress.py` once over all boards: untouched boards must be identical
  (home boards' moving text ribbon is known noise — rerun the same version on both ports to confirm).
- If the change depends on time (calendar, countdown, today marker), add a clock check with `clock_script()` from `tools/_common.py`.
- Do not repeat the full-site audits listed in [TESTING.md](TESTING.md#last-verified-results) unless the owner asks.

## 10. External dependencies and limits

- **Artifact tool** (claude.ai): read/list/publish the website artifact; works from any conversation of the owner. If it is not available in a session,
  stop and tell the owner — the live design cannot be checked or changed without it.
- **Local previews:** need the Design runtime (`Artifact read` path `artifact-type/dc-runtime.js` from the website artifact; default out folder is fine) and
  the fonts via npm (`npm install --prefix work …`, see TESTING.md). Google Fonts and most websites are blocked in the sandbox; npm/pip/GitHub work.
- **Figma MCP:** Starter plan = 20 tool calls per month, **read-only calls count too**. Exhausted 9 Oct 2026; reset date unknown.
  The reminder (10 Nov 2026, 10:00 IST) wakes the **old** conversation, not a new one — ask the owner, or check it with `list_triggers`.
- **GitHub:** the repo is public-readable, so a new session can clone it once the handover has been pushed. Pushing needs the owner's GitHub account
  linked to Claude (claude.ai → Settings → Connectors) and the owner's go-ahead.
- Canva is connected but not used for this project.

## 11. First action in the new session

1. Confirm you are in the right repository and it is current: `git remote -v` shows `github.com/sc207/Shree-Vihat-Meldi-Dham-Design`,
   and `git fetch origin && git status -sb` shows `main...origin/main` with nothing ahead/behind. Confirm you have read this file and CLAUDE.md.
   Work from the repository files, not from chat history.
2. Check the snapshot: `(cd design/project && sha256sum -c --quiet ../SHA256SUMS.txt) && (cd design/assets && sha256sum -c --quiet SHA256SUMS.txt) && echo OK`.
3. Run the live-version check (§8 step 1) and report the live version id and whether it still equals v109 `1791922103-42cb`.
4. Report anything missing from the handover, then **wait for the owner's next task** (open: approval of Seva v107; answers to the audit report's questions). Do not modify anything before that.
5. Before any audit work, read [tasks/full-design-audit.md](tasks/full-design-audit.md) in full (agreed scope: Phases A–C only, report and fix plan first;
   the website stays unchanged until the owner approves the findings and fixes).
