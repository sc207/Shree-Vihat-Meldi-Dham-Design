# Task brief — complete design audit and refinement (supplied by the owner, 10 Oct 2026)

Status: **not started.** Run it in a new session, in phases. The owner's brief is reproduced verbatim below the line.
Read these project notes first — where the brief is generic, they say how it applies here. Project rules in [CLAUDE.md](../CLAUDE.md) win.

## Agreed scope and order (owner, 10 Oct 2026)

Order: (1) Seva desktop empty right column first — fix, then the owner inspects before approving; (2) this audit; (3) approved fixes in small versions.

First audit task, as the owner worded it:

> Run the complete design audit in `tasks/full-design-audit.md`, covering all 24 boards.
> Perform Phases A–C only. Do not modify, fix, or redesign anything yet.
> 1. Inspect every board and its relevant responsive layouts.
> 2. Identify confirmed visual bugs, UX problems, animation and transition issues, image and artwork placement problems, typography and Gujarati rendering issues, accessibility concerns, and design inconsistencies.
> 3. Investigate the likely root cause of each issue.
> 4. Prioritise findings by severity and user impact.
> 5. Provide screenshots of the actual issues wherever possible, with the board name and viewport size.
> 6. Give me a consolidated audit report and proposed fix plan before changing anything.
>
> Preserve the Gujarati-only requirement, all approved content and artwork, the existing visual identity, and v106 as the fallback.
> Do not claim that a page, device, browser, animation, or performance metric has been tested unless it was actually verified. Clearly label anything that remains unverified.
> Wait for my approval before beginning Phase D or making any changes.

Do not fix all 24 boards in one pass: diagnose first, then targeted changes in small approved batches.

## How this brief applies to this project

1. **Gujarati only.** The brief mentions "Gujarati and English content"; this site has Gujarati content only. Do not add English.
2. **Approval and versions.** Phases A–C (inventory, priorities, root causes) end in a **report to the owner** with screenshots. Fixes then go in
   small batches, each previewed, approved and published as its own version (NEXT_SESSION.md §8). v106 stays the rollback point.
3. **What to test on.** 24 boards in `design/project` (desktop 1440, tablets 834/1180, phone landscape 844, phones 390). Pages are fluid: test the brief's
   width ranges with `tools/serve.py` + `tools/check_layout.py --widths …` (it overrides the board width), in normal and large (અ+) text.
   Reuse `tools/fullcheck.js`, `frame_heights.py` and `pixel_regress.py`. Earlier verified results are in [TESTING.md](../TESTING.md) and [CHANGELOG.md](../CHANGELOG.md):
   re-check them, but do not re-open approved decisions without a confirmed defect.
4. **Limits — record as "not verified", never claim:** only Chromium is available (no Firefox/WebKit/real devices); Core Web Vitals cannot be measured
   (no hosted site, no field data); no screen-reader run. Keyboard focus order and reduced-motion can be checked in Chromium.
5. **The header/hero trade-off in brief §3** ("adjusting the menubar to show the full temple artwork cropped some text") is **not in the previous session's
   records.** Ask the owner which page and screen size, or find it by checking every hero at all widths, before changing anything.
6. **Known items to fold in:** Seva desktop empty right column (owner's first task); canvas to-do note PDF line (approved). Known canvas-only limits
   (8000 px board cap, festival-week heights) are not website defects.
7. **CSS hygiene:** site.css already has 20 `!important` rules and 8 reduced-motion blocks; add new rules at the end, scoped, without `!important`
   unless overriding an inline style; do not refactor existing rules unless a confirmed defect needs it.
8. **Content:** never change wording, names, dates or facts; never invent trust content; placeholders stay.

---

Use this master prompt in Claude Design for your Shri Vihat Meldi Dham website. It instructs Claude to perform a complete professional UI/UX audit of every page, inspect actual design problems, test responsive behaviour, animations, transitions, typography, artwork placement, accessibility, and usability — then fix the issues without damaging the existing design or content.

# MASTER PROMPT — COMPLETE WEBSITE DESIGN AUDIT, BUG DETECTION & PROFESSIONAL UI/UX REFINEMENT

## Project: Shri Vihat Meldi Dham, Sanand, Gujarat

Act as a **Senior UI/UX Designer, Design Systems Architect, Responsive Web Specialist, Motion Designer, Accessibility Auditor, Visual QA Engineer, and Frontend Design Reviewer**.

Your task is to conduct a complete, systematic, page-by-page design audit of the entire existing Shri Vihat Meldi Dham website. Verify everything carefully, identify every design defect and usability problem you can find, and fix confirmed issues professionally.

This is not a request to redesign the website from scratch. It is a request to make the existing website more polished, consistent, beautiful, accessible, responsive, smooth, intuitive, and production-ready while preserving its established visual identity.

**The objective is simple: every page should look intentional, work beautifully on every supported device, feel smooth and professional, and be effortless for devotees and visitors to use.**

---

# 1. FIRST: INSPECT THE ENTIRE WEBSITE

Before changing anything, inspect the complete website from beginning to end.

- Identify every existing page, section, navigation item, menu, footer, modal, card, form, button, link, image, illustration, icon, and interactive element.
- Review the full page height, not just the initial viewport.
- Inspect the actual rendered design and behaviour wherever preview or browser inspection is available.
- Check the desktop, tablet, and mobile layouts separately.
- Review shared components and global styles, including headers, navigation, page containers, typography, spacing, backgrounds, buttons, and footers.
- Inspect the relationship between the header/menu height and the content below it.
- Look for overlapping elements, clipped content, hidden text, unexpected whitespace, misaligned sections, broken layouts, and inconsistent component styling.
- Verify that the design remains coherent when moving from one page to another.

Do not assume that a component works correctly just because it looks acceptable in a static screenshot.

Check the actual available implementation, styles, responsive rules, and interactions wherever possible.

Create an internal checklist of all pages and components so that no page is skipped.

**Important:** Audit the complete existing design before making modifications. Do not make random cosmetic changes before understanding the underlying layout and design system.

# 2. PRESERVE THE EXISTING IDENTITY AND APPROVED DESIGN

The website represents Shri Vihat Meldi Dham, Sanand, Gujarat. Its spiritual identity, Gujarati content, temple imagery, devotional atmosphere, and established visual direction must remain intact.

Preserve the existing approved:

- Page structure and information hierarchy.
- Gujarati and English content.
- Temple photographs, founder imagery, deity artwork, and other meaningful assets.
- Existing page-specific designs and layouts that already work correctly.
- Navigation destinations and functional links.
- Festival information, dates, timings, announcements, and other factual content.
- Existing design decisions that have already been reviewed and approved.

Maintain the established design language, including its maroon, antique gold, saffron, and ivory palette, appropriate Gujarati typography, elegant devotional atmosphere, and refined ornamental details.

Use the existing project styles and assets as the source of truth rather than introducing an unrelated visual theme.

Do not replace meaningful temple artwork with generic stock images, random illustrations, emoji, or AI-generated substitutes.

Do not remove content simply to make a page fit the viewport.

Do not change Gujarati wording, spelling, religious terminology, names, dates, or factual information as part of a visual refinement task.

If an existing element is already correct, leave it alone.

# 3. LAYOUT, PAGE HEIGHT AND CONTENT VISIBILITY

Audit every page for structural and visual layout defects.

Check:

- Whether the complete temple, deity, founder, or other important artwork is visible in its intended composition.
- Whether headers and navigation bars consume excessive vertical space.
- Whether content is hidden behind fixed or sticky navigation.
- Whether headings, Gujarati characters, matras, subtitles, and body text are clipped.
- Whether sections have incorrect heights or widths.
- Whether page content extends beyond the viewport unexpectedly.
- Whether horizontal scrolling appears unintentionally.
- Whether content is cut off at section boundaries.
- Whether images, cards, text, and decorative elements overlap.
- Whether the footer is reachable and displayed correctly.
- Whether there is excessive empty space or cramped content.
- Whether the first viewport communicates the page's purpose clearly.

### Special requirement: Fix the header and hero layout properly

Previously, adjusting the menubar to show the full temple artwork caused some text to become cropped. Do not repeat this trade-off.

The correct solution must preserve both the complete intended artwork and the readability of the text.

Investigate the actual cause before changing anything. Consider the header's height, hero container sizing, image aspect ratio, background positioning, object-fit behaviour, typography, responsive breakpoints, padding, and available viewport height.

Do not solve this by arbitrarily shrinking text, compressing the hero, hiding content, or moving elements into awkward positions.

Choose a robust layout solution that works across the entire website, not a one-off patch for a single screenshot.

# 4. IMAGE, TEMPLE ARTWORK AND ILLUSTRATION AUDIT

Review every visual asset individually.

Check:

- Correct image selection for its section.
- Appropriate image size, aspect ratio, and resolution.
- Correct positioning, cropping, alignment, and focal point.
- Whether the full subject is visible when required.
- Whether faces, temple domes, deity artwork, architectural details, or important text are accidentally cropped.
- Whether transparent PNG artwork has unwanted backgrounds, halos, or visible edges.
- Whether image overlays, gradients, shadows, and background colours are appropriate.
- Whether images have sufficient contrast against surrounding content.
- Whether artwork appears stretched, pixelated, blurred, distorted, or disproportionately scaled.
- Whether decorative art interferes with readable text or clickable elements.
- Whether image loading creates layout shifts.
- Whether mobile cropping differs from the intended composition.

Use `object-fit`, `object-position`, `background-size`, and `background-position` appropriately for the actual purpose of each asset.

Do not apply one universal cropping rule to every image. A temple photograph, a founder portrait, a deity illustration, a decorative mandala, and a small icon have different requirements.

Where necessary, use device-specific positioning or separate responsive layout rules without unnecessarily duplicating assets.

**Rule:** Important spiritual artwork must remain visually respectful, correctly proportioned, and intentionally placed. Decorative artwork must support the content rather than compete with it.

# 5. TYPOGRAPHY AND GUJARATI LANGUAGE RENDERING

Audit typography across all pages and screen sizes.

Check:

- Gujarati font rendering and correct vowel marks and matras.
- Gujarati conjuncts, character spacing, line height, and word wrapping.
- English typography, font weights, and hierarchy.
- Heading sizes and responsive scaling.
- Body text readability.
- Line lengths and paragraph spacing.
- Button labels, navigation text, captions, dates, and timings.
- Text clipping, overflow, unwanted ellipses, and broken words.
- Font loading and fallback behaviour.
- Contrast and readability over images or coloured backgrounds.
- Consistency between similar headings and components.

Preserve the established Gujarati and English font choices where possible.

Do not use letter spacing that breaks Gujarati character rendering or makes the text visually unnatural.

Avoid excessively small text, oversized headings that overwhelm the page, overly long text lines, and unnecessary use of decorative fonts.

Use a consistent typographic hierarchy with responsive sizes and comfortable line heights.

Every piece of text must remain readable without requiring users to zoom in.

# 6. RESPONSIVE DESIGN — MOBILE, TABLET AND DESKTOP

Treat responsive design as a core requirement, not a final cosmetic adjustment.

Test representative viewport widths, including:

- Small mobile: 320–360 px.
- Standard mobile: 375–430 px.
- Large mobile: 431–600 px.
- Tablet: 601–900 px.
- Small laptop: 901–1200 px.
- Desktop: 1201–1440 px.
- Wide desktop: 1441 px and above.

These are testing ranges, not mandatory breakpoint values. Choose breakpoints according to the actual content and layout.

At every relevant width, verify:

- Header and navigation behaviour.
- Mobile menu opening, closing, and usability.
- Hero image and text composition.
- Section spacing and page height.
- Grid and card column changes.
- Button size and placement.
- Image and artwork positioning.
- Forms, inputs, labels, and validation messages.
- Footer layout.
- Modals, dropdowns, tooltips, and floating actions.
- Gujarati text wrapping.
- Touch target sizes and spacing.
- No unintended horizontal scrolling.
- No overlapping or clipped content.
- No controls that become inaccessible on mobile.

Ensure the website feels deliberately designed for mobile rather than merely compressed from desktop.

Use fluid layouts, flexible containers, responsive typography, suitable max-widths, and content-driven breakpoints.

Do not blindly force every device to display the same composition. Adapt layouts where necessary while preserving the same visual identity and information hierarchy.

# 7. HEADER, NAVIGATION AND WAYFINDING

Inspect every navigation state.

Verify:

- The logo and temple identity are correctly positioned.
- Menu labels are understandable and consistent.
- Active-page indicators are clear.
- Dropdowns open in the correct direction and remain within the viewport.
- Menus do not obscure important content.
- Sticky or fixed navigation does not cover headings or anchor destinations.
- Mobile menus are easy to open, navigate, and close.
- Keyboard users can reach and operate navigation.
- Focus indicators are visible.
- Navigation remains usable at different zoom levels.
- Links have clear destinations and do not lead to unexpected pages.

Keep the navigation elegant and appropriately compact, but never at the cost of readability or accessible interaction.

# 8. ANIMATIONS, TRANSITIONS AND MOTION QUALITY

Audit every animation and transition on the website.

This includes entrance animations, scroll effects, hover states, image reveals, button interactions, menu transitions, background effects, floating elements, parallax, and page transitions.

For every animation, evaluate:

- Whether it serves a real purpose.
- Whether the timing feels natural.
- Whether the easing is smooth and appropriate.
- Whether the beginning and end states are visually stable.
- Whether elements jump, flicker, shake, or abruptly change size.
- Whether motion creates layout shifts.
- Whether animations interfere with reading or clicking.
- Whether effects trigger too frequently during scrolling.
- Whether several simultaneous animations compete for attention.
- Whether animation performance remains smooth on mobile devices.
- Whether animations cause content to remain invisible if a script fails.

Use restrained, polished motion appropriate to a premium devotional website.

Recommended starting points, to be adjusted to the existing design:

- Small interaction transitions: approximately 150–220 ms.
- Standard interface transitions: approximately 200–320 ms.
- Subtle section reveals: approximately 350–650 ms.
- Smooth, restrained easing rather than abrupt linear motion.

These are guidelines, not rigid requirements. Avoid delaying interactions just to make them look animated.

Prefer opacity and transform for suitable effects rather than repeatedly animating layout-heavy properties.

Do not animate every element. Motion should establish hierarchy, provide feedback, and add refinement.

Respect `prefers-reduced-motion`. When users request reduced motion, minimise nonessential movement and disable unnecessary parallax or scroll-triggered effects.

Ensure that all content remains visible and usable even when animations are disabled.

# 9. INTERACTION AND MICRO-INTERACTION AUDIT

Test every visible interactive element.

Check:

- Buttons in default, hover, active, focus, disabled, and loading states.
- Link hover and focus behaviour.
- Cards that appear clickable.
- Dropdowns and selectors.
- Accordions and expandable sections.
- Modals and dismiss controls.
- Mobile menu interactions.
- Forms and their error and success states.
- WhatsApp shortcuts and social links.
- Image galleries or lightboxes, if present.
- Back-to-top controls, if present.
- Floating buttons and other persistent actions.

A control must behave consistently with its appearance and label.

Do not leave buttons that look functional but do nothing. Do not make decorative elements appear clickable unnecessarily.

Make interactive feedback clear but subtle. Avoid excessive scaling, aggressive shadows, flashing effects, or animations that make buttons feel unstable.

For touch devices, provide reliable tap behaviour without depending on hover.

# 10. USER EXPERIENCE — MAKE THE WEBSITE EASIER TO USE

Evaluate the experience from the perspective of a first-time visitor, a devotee looking for festival information, and a visitor using a mobile phone.

Ask these questions for every page:

- Can users understand the purpose of the page immediately?
- Is the most important information visible at the right time?
- Is the content ordered logically?
- Can users find festival dates, schedules, darshan information, contact details, and other available information without unnecessary effort?
- Are headings and labels clear?
- Are primary actions easy to recognise?
- Is the difference between primary and secondary actions obvious?
- Are related items grouped together?
- Is there unnecessary duplication?
- Are users forced to scroll excessively to find essential information?
- Does the page contain distracting or unnecessary decorative elements?
- Are important actions comfortable to use with one hand on mobile?
- Is the design consistent enough that users know what to expect?

Reduce cognitive load through clear hierarchy, predictable navigation, meaningful grouping, sufficient spacing, readable text, and consistent controls.

Do not add new features merely to make the design appear more sophisticated.

Do not remove useful information or introduce unnecessary interactions.

**The best design is not the one with the most effects. It is the one that helps people accomplish their goals with the least confusion.**

# 11. SPACING, ALIGNMENT AND DESIGN SYSTEM CONSISTENCY

Audit the entire design system for consistency.

Check:

- Page margins and container widths.
- Section padding and vertical rhythm.
- Spacing between headings, descriptions, buttons, and images.
- Card padding and alignment.
- Grid gaps.
- Border radius consistency.
- Border thickness and colour.
- Shadow softness and depth.
- Button dimensions.
- Icon sizes and alignment.
- Background colour transitions.
- Repeated component styles.
- Consistency between equivalent sections on different pages.

Establish or refine a coherent spacing scale, typography scale, colour tokens, radius system, elevation system, and reusable component styles where appropriate.

Correct inconsistencies through shared styles or components whenever possible.

Avoid adding arbitrary values for each individual section if a consistent design token can solve the problem.

Do not force every section to look identical. Preserve appropriate page-specific visual variation within the shared design language.

# 12. COLOUR, CONTRAST AND VISUAL HIERARCHY

Review all text, controls, backgrounds, borders, icons, overlays, and decorative elements.

Use the existing maroon, antique gold, saffron, ivory, and complementary tones thoughtfully.

Check:

- Text contrast against every background.
- Readability of muted text.
- Button contrast and visible labels.
- Text over photographs and gradients.
- Gold text on light backgrounds.
- Decorative details that compete with important content.
- Visual hierarchy between headings, supporting text, and actions.
- Consistency of semantic colours, if present.

Where applicable, target WCAG 2.2 AA contrast ratios:

- Normal text: at least 4.5:1.
- Large text: at least 3:1.
- Important interface components and graphical indicators: generally at least 3:1 against adjacent colours.

Do not sacrifice readability to preserve a particular shade. When a colour combination fails, adjust the foreground, background, overlay, or treatment while retaining the overall brand identity.

# 13. ACCESSIBILITY AND INCLUSIVE DESIGN

Perform a practical accessibility review.

Check:

- Semantic heading hierarchy.
- Appropriate HTML landmarks.
- Accessible names for buttons and icon-only controls.
- Alternative text for meaningful images.
- Empty alternative text for purely decorative images where appropriate.
- Keyboard navigation.
- Visible keyboard focus.
- Logical focus order.
- Adequate touch target sizes.
- Form labels and understandable error messages.
- Sufficient colour contrast.
- Reduced-motion support.
- Zoom and text resizing.
- Accessible dropdowns and modal behaviour.
- Screen-reader clarity.
- Whether information is conveyed by colour alone.

Aim for WCAG 2.2 AA where applicable.

Avoid unnecessarily complicated interactions and ensure that essential information remains available without animation, hover, or colour perception.

# 14. PERFORMANCE AND VISUAL STABILITY

Review design-related performance issues that affect the user experience.

Check:

- Oversized image assets.
- Inappropriate image dimensions.
- Missing image dimensions that cause layout shifts.
- Lazy loading for appropriate below-the-fold images.
- Priority loading for the actual above-the-fold hero image.
- Excessive animation or scroll-event work.
- Expensive blur, shadow, filter, and backdrop-filter effects.
- Unnecessary visual effects on low-powered devices.
- Font-loading flashes and layout shifts.
- Content that appears late or jumps after loading.
- Responsive images where suitable.
- Layout stability during page load and interaction.

Do not lazy-load the primary hero image if that would unnecessarily delay the most important visible content.

Do not remove meaningful effects indiscriminately. Improve implementation and loading behaviour while preserving the intended appearance.

If performance measurement tools are available, inspect Core Web Vitals, particularly LCP, INP, and CLS. Treat the following as good target thresholds at the 75th percentile, when sufficient real-user data exists:

- LCP: 2.5 seconds or less.
- INP: 200 milliseconds or less.
- CLS: 0.1 or less.

If these metrics cannot be measured, state that they were not verified rather than claiming the website passes.

# 15. FORMS, CONTENT SECTIONS AND EDGE CASES

Where forms, schedules, event listings, announcements, or other data-driven sections exist, check how the design handles:

- Long Gujarati headings.
- Long English text.
- Missing optional images.
- Images with different aspect ratios.
- Empty states.
- Loading states.
- Error messages.
- Success confirmations.
- Unusually long names.
- Small screens and landscape orientation.
- Browser zoom.
- Dynamic content that increases section height.
- Missing or unavailable data.

Do not invent content or replace factual information with placeholder content.

Make sure longer content does not break the design or conceal actions.

# 16. CROSS-BROWSER AND REAL-DEVICE VALIDATION

Where browser testing tools are available, verify the design in:

- Chrome.
- Firefox.
- Safari or an equivalent WebKit environment.
- Android mobile browser behaviour.
- iOS Safari behaviour, where test access exists.

Pay particular attention to viewport height, safe-area insets, sticky navigation, font rendering, image sizing, touch interactions, and fixed-position elements.

Test portrait and landscape orientations where relevant.

Do not claim to have tested a browser or physical device unless the test was actually performed.

If a test environment is unavailable, record it as unverified and identify what should be checked later.

# 17. TECHNICAL AND REGRESSION SAFETY

This is a design-refinement task, not permission to rewrite the application.

- Preserve the existing framework, architecture, routing, and project conventions.
- Preserve working functionality and established component behaviour.
- Avoid unnecessary dependencies.
- Avoid introducing global CSS rules that unintentionally break other pages.
- Avoid using `!important` as a substitute for fixing the underlying style conflict.
- Avoid duplicating components or styles without a good reason.
- Reuse shared tokens and components when practical.
- Keep responsive styles scoped appropriately.
- Preserve all approved copy, imagery, and page content.
- Do not change backend logic, authentication, data models, or business logic for cosmetic reasons.
- Do not overwrite unrelated user changes.
- Do not delete working code just because it is difficult to understand.
- Keep the implementation maintainable and explain any significant structural change.

After every meaningful change, check the affected page and the shared components that might be impacted.

A fix is not complete if it solves one page but breaks three others.

# 18. REQUIRED AUDIT AND FIXING WORKFLOW

Follow this workflow in order.

## Phase A — Full inventory and baseline

Inspect every available page and shared component.

Record existing problems, inconsistent patterns, responsive issues, motion defects, image-placement problems, and accessibility concerns.

Distinguish between confirmed defects and possible improvements.

## Phase B — Prioritisation

Classify each issue as:

- **P0 — Critical:** content is inaccessible, a page is broken, major text or artwork is clipped, or an essential interaction is unusable.
- **P1 — High:** substantial responsive, navigation, readability, or usability problems.
- **P2 — Medium:** inconsistent spacing, awkward transitions, image alignment, typography, or component behaviour.
- **P3 — Polish:** minor decorative, aesthetic, or refinement opportunities.

Prioritise problems according to actual user impact, not how easy they are to fix.

## Phase C — Root-cause analysis

Before modifying each issue, determine why it occurs.

For example, if a heading is clipped, inspect the container height, overflow rules, font metrics, line height, and breakpoint behaviour.

If the temple image is cropped, inspect its source aspect ratio, container sizing, object positioning, and responsive rules.

If a menu hides the hero, inspect the relationship between navigation height, positioning, and content offset.

Fix the underlying cause rather than adding a temporary workaround.

## Phase D — Implementation

Apply targeted changes in priority order.

Fix critical and high-impact issues first, followed by consistency improvements and visual polish.

Use reusable styles where appropriate and avoid unnecessary redesign.

## Phase E — Regression testing

After modifications, retest:

- Every affected page.
- Every changed shared component.
- Desktop and mobile layouts.
- Header and hero combinations.
- Navigation and buttons.
- Animation and transition states.
- Text rendering and image cropping.
- Keyboard interactions and reduced-motion behaviour.

Repeat the test at nearby viewport widths to catch breakpoint edge cases.

## Phase F — Final review

Inspect the entire website from the top of every page to the footer.

Compare the final result against the original baseline.

Confirm that existing content, imagery, and functionality remain intact and that no new layout defects have been introduced.

# 19. ACCEPTANCE CRITERIA

Consider the audit complete only when:

1. Every available page has been inspected.
2. All identified P0 and P1 design defects that can be fixed safely have been addressed.
3. No known major content clipping or unintended horizontal overflow remains in tested viewports.
4. Temple and other meaningful artwork are properly positioned and proportioned.
5. Gujarati and English typography remain readable across supported widths.
6. Headers and menus do not obscure important content.
7. Transitions are smooth, purposeful, and responsive to reduced-motion preferences.
8. Visible controls provide clear and consistent interaction feedback.
9. Navigation, spacing, colours, and component styles remain coherent.
10. Important content remains accessible by keyboard and on touch devices.
11. Images and fonts do not introduce avoidable layout shifts.
12. No unrelated functionality or approved content has been damaged.
13. Every claimed fix has been checked in the available test environment.
14. Remaining unverified items are explicitly documented.

Do not claim perfection or complete verification when some pages, browsers, devices, or interactions could not actually be tested.

# 20. FINAL REPORT

When finished, provide a concise but complete audit report containing:

### A. Overall assessment

- What was inspected.
- Which pages and viewports were actually tested.
- The most important findings.

### B. Issues discovered and fixed

For each significant issue, include:

- Page or component.
- Problem.
- Root cause.
- Fix applied.
- Verification performed.

### C. Responsive review

Summarise the tested viewport widths and any remaining issues.

### D. Motion and interaction review

Report problems found in transitions, animation timing, hover states, scrolling effects, and interactive controls.

### E. Accessibility and performance

List the checks actually performed and the findings. Clearly distinguish measured results from visual estimates.

### F. Outstanding issues

List anything that could not be verified, any unresolved defects, and any improvement requiring a separate decision.

### G. Final status

Classify each issue as fixed, verified, partially verified, unresolved, or not tested.

Do not report an item as verified simply because its CSS was edited.

---

# FINAL INSTRUCTION

Start by inspecting the entire existing website. Then audit, diagnose, prioritise, fix, and retest systematically.

Be meticulous about small details, but be conservative with already-approved design decisions.

**Do not redesign everything. Do not change things just for the sake of changing them. Do not make the page look good on desktop while breaking mobile. Do not sacrifice Gujarati readability to fit artwork. Do not sacrifice artwork to accommodate the navigation bar. Do not add unnecessary animations or visual clutter.**

The desired result is a refined, premium, spiritually appropriate, visually consistent, fully responsive, accessible, and easy-to-use Shri Vihat Meldi Dham website.

Work through the complete scope wherever the available tools and project access permit. If the audit is too large for one pass, complete it in clearly defined phases, preserve the audit checklist, and continue until every page has been reviewed.

Begin with the audit. Make only evidence-based changes, and verify every fix you can actually test.

## How to use this prompt effectively

I recommend giving Claude these additional instructions alongside the master prompt:

- Inspect before editing: Have Claude examine every page first, so it doesn't prematurely change a design that is already correct.
- Fix in phases: Prioritise layout breakage, cropped temple artwork, and mobile usability before subtle shadows or animations.
- Protect the approved version: If you are working in Claude Design with an approved reference or published version, preserve that reference and make changes in a separate working copy or use the project's established versioning workflow.
- Require actual verification: Ask for screenshots or previews at mobile, tablet, and desktop sizes where available. A code review alone cannot prove that a rendered design is correct.

One especially important requirement for your website: the header, temple artwork, and Gujarati text must work together as a single responsive composition. Claude should fix their underlying layout relationship rather than repeatedly adjusting the menu height and accidentally cropping something else.