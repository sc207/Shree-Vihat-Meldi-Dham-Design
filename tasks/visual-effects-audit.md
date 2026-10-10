# Brief — visual effects, artwork and responsive audit (supplied by the owner, 10 Oct 2026, 18:10 IST)

Owner's message: "given above prompt and reference check — added ss for your reference. this kind of mistakes in everywhere and i pretty sure other kind of issues will be in design too."

Screenshot: [visual-effects/owner_glow_768_vs_1024.png](visual-effects/owner_glow_768_vs_1024.png) — PranPratishtha hero at 768×1024 (glow circled, away from the deities) vs 1024×768.

Project rules in [CLAUDE.md](../CLAUDE.md) still apply: fixes are prepared and shown first; each published version needs the owner's approval.

---

## Part 1 (verbatim)

The issue in your screenshot is a responsive positioning and animation problem. The yellow glow behind Mataji is not staying aligned with the artwork when the screen changes from `768 × 1024` to `1024 × 768`. This usually happens when decorative effects, artwork, and responsive layouts use different positioning or scaling rules.

For your design in Claude, the fix should cover the entire design system, not just the yellow glow. That includes illustrations, divine light effects, animations, backgrounds, responsive layouts, typography, buttons, and overlapping elements.

## 1. What needs to be fixed

Maa durga ai png hd logo free download

1. Artwork and glow alignment

Keep the yellow light anchored to the exact position behind Mataji. The artwork and glow should share the same positioning container and scale together across screen sizes.

Glowing yellow luminous color with bokeh

2. Background effects and decorative art

Fix radial gradients, ambient glows, mandala patterns, particles, shadows, and decorative overlays so they don't drift, stretch, or become detached from their intended elements.

Spiritual App UI Design Midjourney Prompt - promptsideas.com

3. Responsive layout

Correct image scaling, spacing, element overlap, clipping, alignment, text wrapping, and component positioning across desktop, tablet, and mobile.

## 2. The most important technical fix: anchor the glow to Mataji

Avoid positioning the glow using viewport-based values such as `left: 68vw` or fixed pixel offsets. Those values can shift the glow away from Mataji when the layout changes.

Instead, place the glow and artwork inside one shared, positioned wrapper.

HTMLWrap linesCopy codePreview

```

<div class="mataji-art">
  <div class="mataji-glow" aria-hidden="true"></div>
  <img
    class="mataji-image"
    src="/images/mataji.png"
    alt="Mataji"
  />
</div>
```

css
```

.mataji-art {
  position: relative;
  isolation: isolate;
  width: min(100%, 420px);
  aspect-ratio: 4 / 5;
  margin-inline: auto;
}

.mataji-glow {
  position: absolute;

  /* Coordinates relative to the artwork wrapper */
  left: 50%;
  top: 44%;
  width: 65%;
  aspect-ratio: 1;

  transform: translate(-50%, -50%);
  border-radius: 50%;

  background: radial-gradient(
    circle,
    rgba(255, 190, 70, 0.30) 0%,
    rgba(255, 150, 35, 0.14) 38%,
    rgba(255, 130, 30, 0.04) 62%,
    transparent 74%
  );

  filter: blur(18px);
  z-index: 0;
  pointer-events: none;
}

.mataji-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  z-index: 1;
  display: block;
}
```

Important: The example coordinates (`50%`, `44%`) are starting values, not measurements from your original artwork. Adjust them to match the actual image. If the image contains transparent padding, account for the visible figure's position inside the image canvas.

This approach anchors the glow to the artwork container rather than the screen. CSS positioning and aspect ratios help maintain that relationship as dimensions change. MDN

+1

## 3. Master prompt for Claude — fix the entire design

Copy the following prompt into Claude in the same conversation where you are developing the website. Include your screenshot and, ideally, your current source files.

Writing

# Complete Responsive Design, Artwork, Animation and Visual Effects Audit

Act as a senior frontend engineer, responsive UI specialist, animation engineer, and visual QA expert.

I need you to audit and fix my **entire existing website design**, including all pages, components, illustrations, animations, decorative effects, and responsive layouts. Do not fix only the issue shown in the screenshot.

## 1\. Primary issue

In the supplied screenshot, a yellow/golden ambient glow intended to sit behind Mataji moves away from its intended position when the viewport changes from 768 × 1024 (portrait) to 1024 × 768 (landscape).

The glow must remain visually aligned with the intended position behind Mataji at every supported screen size.

Identify the actual root cause in my code before changing anything. Check whether the issue is caused by viewport-relative coordinates, fixed dimensions, independent positioning contexts, image scaling, transparent image padding, transforms, animation keyframes, overflow, stacking contexts, or conflicting responsive CSS.

Do not guess at the cause when the source code can establish it.

## 2\. Audit the entire project

First, inspect the existing project structure, framework, stylesheets, reusable components, image assets, animation libraries, and responsive breakpoints.

Search all relevant files for:

- Absolute and fixed positioning
- Hardcoded pixel offsets and viewport units
- Fixed width and height combinations
- Incorrect or missing aspect ratios
- Images using inappropriate object-fit or object-position settings
- Transparent padding inside PNG, WebP, or SVG artwork
- CSS transforms and transform-origin issues
- Animation keyframes that move or scale elements unintentionally
- Scroll-triggered, JavaScript-driven, and requestAnimationFrame animations
- Conflicting media queries and duplicated CSS declarations
- Incorrect z-index and stacking contexts
- Overflow clipping and elements escaping their containers
- Layout shifts during image, font, or animation loading
- SVG viewBox, preserveAspectRatio, filter, mask, and transform problems
- Canvas dimensions and device-pixel-ratio handling, if applicable
- Parallax effects and scroll-linked positioning
- Background images, gradients, shadows, glows, particles, and mandala patterns
- Inconsistent spacing, typography, buttons, cards, navigation, and overlays

Audit every page and reusable component, not just the hero section.

## 3\. Implement robust responsive positioning

Use a shared, positioned parent container for visual elements that must remain aligned, such as:

- Mataji artwork and its golden glow
- Deity illustrations and halos
- Background decorations and their associated content
- Decorative SVGs and their corresponding sections
- Particles or effects attached to specific artwork

Use percentage-based coordinates relative to the correct parent, appropriate aspect ratios, CSS Grid or Flexbox for layout, and responsive sizing with min(), max(), and clamp() where appropriate.

Do not use viewport-relative offsets to position effects that must remain attached to a particular image or component.

Keep the artwork's proportions correct. Use object-fit: contain when the full illustration must remain visible. Use cover only when intentional cropping is part of the design.

Account for transparent padding inside image files. The visual center of the figure may differ from the geometric center of the image canvas.

If the source artwork and its glow must scale together, keep them within the same coordinate system. Do not independently position the glow using unrelated viewport coordinates.

Use a different responsive composition when necessary, but preserve the intended visual relationship between the artwork and its effects.

## 4\. Fix all visual effects

Review and correct:

- Golden and yellow ambient lighting
- Halos and radial gradients
- Glow blur and shadow spread
- Animated light intensity and opacity
- Background gradients and textures
- Mandala artwork and ornamental patterns
- Floating particles, sparkles, and decorative elements
- Image overlays, masks, filters, and blending modes
- Parallax and scroll animations
- Hover, entrance, transition, and loading effects

Effects must stay within their intended component, retain their correct visual hierarchy, and avoid obscuring important text or illustrations.

Preserve the original devotional atmosphere, maroon/gold color palette, and artistic direction. Do not redesign the website unnecessarily.

## 5\. Fix animation behavior

For every animation, verify:

- The correct transform origin
- Stable positioning throughout the animation
- No unintended translation, scaling, rotation, or layout movement
- No jump when an animation starts, repeats, reverses, or ends
- No mismatch between CSS animation coordinates and responsive coordinates
- No hydration or initial-render flash, if the framework uses hydration
- No drift after resizing or changing orientation
- No duplicate animation loops or event listeners
- Correct cleanup of JavaScript animation loops and resize observers
- Smooth performance without unnecessary layout recalculation

Prefer transform and opacity animations when suitable. Do not animate layout-affecting properties unnecessarily.

If an animation changes the position or scale of an element, verify that its entire visual group remains aligned.

Respect the user's reduced-motion preference using prefers-reduced-motion or the equivalent mechanism in the existing framework.

## 6\. Fix responsive layout issues throughout the website

Test and correct the complete design at these viewport sizes:

- 320 × 568
- 360 × 800
- 375 × 812
- 390 × 844
- 430 × 932
- 768 × 1024
- 1024 × 768
- 1280 × 800
- 1366 × 768
- 1440 × 900
- 1920 × 1080

Also test intermediate widths and heights, browser zoom where practical, and orientation changes.

Check for:

- Horizontal scrolling
- Content overlapping or disappearing
- Images stretching or cropping incorrectly
- Text overflow and awkward line wrapping
- Buttons becoming clipped or difficult to tap
- Decorative effects moving out of position
- Broken spacing and inconsistent alignment
- Navigation and modal overflow
- Unexpected changes caused by scrollbar appearance
- Mobile browser viewport-height behavior
- Layout shifts during loading
- Incorrect stacking order

Do not introduce a separate arbitrary pixel adjustment for every viewport. Prefer fluid, constraint-based layouts and meaningful breakpoints.

## 7\. Establish consistent layering

Create a predictable stacking system for each visual section. For example:

- Background textures and patterns
- Ambient glow and lighting
- Decorative illustrations
- Primary artwork
- Text and interactive content
- Navigation, dialogs, and other overlays

Use isolation or dedicated stacking contexts when needed. Ensure decorative layers use pointer-events: none so they cannot block buttons, links, or touch interactions.

Avoid adding increasingly large z-index values to mask underlying positioning errors.

## 8\. Preserve the design and existing functionality

Do not replace working artwork with placeholders or unrelated stock images.

Do not remove animations merely to hide bugs. Repair them while preserving the intended motion and appearance.

Do not rewrite the application from scratch unless there is a clear technical reason.

Keep the existing framework, routing, functionality, accessibility, and project conventions intact.

Reuse existing assets and components. Do not introduce new dependencies unless they are genuinely necessary.

If a visual asset itself contains incorrect spacing, transparency, or proportions, identify the problem and propose or implement an appropriate asset-level fix.

## 9\. Verify with actual visual testing

Do not declare the work complete simply because the code compiles.

Run the available build, lint, type-check, and automated tests.

Use browser-based visual testing if available. Capture screenshots at the specified viewport sizes and compare them.

Specifically compare the same artwork and its glow at 768 × 1024 and 1024 × 768. Check portrait-to-landscape transitions, repeated resizing, and initial page loading.

Verify that the glow remains anchored to the intended point behind Mataji, the image preserves its proportions, and no other decorative element drifts.

Inspect console errors, missing assets, animation warnings, and horizontal overflow.

If browser automation or screenshot tooling is unavailable, clearly identify which checks could not be performed. Never claim that a visual issue has been verified without actually testing it.

## 10\. Required workflow and final report

Work in this order:

1. Inspect the complete project and identify the actual causes.
2. Create a prioritized list of confirmed issues.
3. Implement fixes across the affected shared components and pages.
4. Remove obsolete or conflicting CSS only after checking its dependencies.
5. Run available automated checks and responsive visual tests.
6. Fix any regressions introduced by your changes.
7. Summarize the results.

In your final report, provide:

- Root causes found
- Files changed and what each change accomplishes
- Responsive and animation issues fixed
- Any remaining known issues
- Tests actually executed and their results
- Any visual checks that still require manual verification

Start by inspecting the existing codebase. Make the fixes directly in the project rather than returning only generic recommendations.

Prioritize correctness, visual consistency, maintainability, accessibility, and responsive behavior across the entire website.

## 4. Recommended implementation checklist

Use this to verify that Claude's changes actually solve the problems.

## Design QA checklist

### 0/16

Artwork and effects

[ ]Glow stays behind Mataji at every tested viewport

[ ]Illustrations and effects share a coordinate system

[ ]Transparent padding and image alignment are accounted for

[ ]Blur, shadows, gradients and masks render correctly

Responsive design

[ ]Portrait and landscape layouts both work

[ ]No horizontal overflow or clipped content

[ ]Images retain correct proportions

[ ]Typography, spacing and buttons adapt correctly

Animation

[ ]No drift after resizing or rotating the device

[ ]No flicker, jumps or misplaced animation origins

[ ]No duplicate loops or stale resize listeners

[ ]Reduced-motion preferences are respected

Quality assurance

[ ]All pages and reusable components reviewed

[ ]Build, lint and type checks run where available

[ ]Screenshots compared at target viewport sizes

[ ]Remaining limitations documented honestly

 Copy checklist

## 5. One additional rule that matters

Do not treat every visual element as a separate responsive object. Effects that belong to the same artwork should move and scale as a group; independent content should flow through the layout normally.

Also, test both the initial render and the resized state. Some visual bugs are caused not by the CSS layout itself, but by animations or JavaScript calculations that continue using old dimensions after the viewport changes. For motion accessibility, the implementation should honor the browser's reduced-motion preference. MDN

+2

The prompt above gives Claude a project-wide audit and repair plan rather than a one-off patch. To confirm the actual fix, Claude will need access to the relevant source code and a way to inspect the rendered page at multiple viewport sizes.

---

## Part 2 (verbatim)

Add this instruction to your prompt in Claude. It makes it clear that Claude must inspect every page, every section, and every small visual issue, not just the Mataji glow problem.

Writing

## Complete Website-Wide Visual Audit and Fix — Every Page, Every Detail

Go through **the entire website, page by page, section by section, and component by component**. Find and fix every small visual issue, design inconsistency, responsive bug, animation problem, and positioning error you can identify, including issues similar to the yellow glow moving away from Mataji when the screen size changes.

**Do not limit your work to the screenshot or the specific issue I reported. Treat this as a complete website-wide design quality audit and repair task.**

### What you must do

1. **Inspect every page:** Review all routes, screens, sections, reusable components, modals, menus, cards, forms, headers, footers, and responsive layouts. Create a list of all pages and verify each one instead of checking only the homepage.

2. **Find small visual imperfections:** Look for slightly misaligned elements, inconsistent spacing, uneven margins, incorrect padding, misplaced icons, awkward text wrapping, inconsistent font sizes, unexpected line heights, imperfect centering, incorrect border radii, inconsistent shadows, and mismatched colors.

3. **Fix all responsive positioning problems:** Check every screen-dependent element at mobile, tablet, laptop, and desktop sizes, in both portrait and landscape orientations. Ensure images, illustrations, decorative elements, and their associated effects remain correctly positioned when the viewport changes.

4. **Audit every artwork and visual effect:** Inspect all images, illustrations, SVGs, background graphics, golden glows, halos, gradients, shadows, blur effects, particles, mandalas, overlays, masks, and decorative elements. Ensure they remain correctly aligned, scaled, layered, and clipped across all supported screen sizes.

5. **Audit every animation and transition:** Check entrance animations, hover effects, floating effects, rotating elements, pulsing glows, scroll animations, parallax, carousels, loading transitions, and looping animations. Fix jitter, flickering, sudden jumps, drifting positions, incorrect transform origins, inconsistent timing, and animation behavior after resizing.

6. **Check element relationships:** When an effect belongs to an image, keep them in a shared positioning context so they move and scale together. Avoid independent viewport-based positioning for elements that must stay visually connected.

7. **Inspect typography and content:** Check headings, paragraphs, buttons, labels, navigation items, line breaks, text alignment, readability, overflow, and content spacing at different viewport widths.

8. **Inspect layout and layering:** Fix unintended overlaps, incorrect z-index values, clipped elements, overflow, misplaced backgrounds, inconsistent section heights, broken grids, misaligned flex layouts, and elements that disappear behind other content.

9. **Check loading and interaction states:** Inspect the initial page render, image loading, font loading, transitions, dropdowns, dialogs, sticky elements, scrolling behavior, and viewport changes. Fix layout shifts, visual flashes, and misplaced effects that appear after loading or interaction.

10. **Maintain a consistent design system:** Ensure shared components use consistent spacing, colors, typography, borders, shadows, animation behavior, and responsive breakpoints. Fix the underlying shared component or styling rule when possible instead of applying isolated patches to individual pages.

### Mandatory testing process

- Build a complete inventory of all website pages and reusable components.
- Inspect each page at multiple viewport sizes and orientations.
- Check intermediate widths, not just predefined breakpoints.
- Test resizing and portrait-to-landscape transitions.
- Compare screenshots and inspect visual differences wherever browser testing is available.
- Run the available build, lint, type checks, and automated tests.
- Recheck affected pages after every shared CSS or component change to catch regressions.
- Maintain a checklist of identified issues, fixes, and verification results.

### Important rules

- Do not stop after fixing the Mataji glow.
- Do not inspect only the homepage.
- Do not ignore issues simply because they seem small.
- Do not replace the existing design with an unrelated redesign.
- Do not remove intended artistic effects or animations to hide their bugs.
- Do not introduce random pixel offsets or unnecessary one-off media queries as temporary workarounds.
- Do not claim that a page or issue has been tested unless you actually tested it.
- If a page or state cannot be accessed or verified, clearly report that limitation.
- Preserve existing functionality, artwork, brand identity, accessibility, and the intended visual style.

### Definition of completion

The task is complete only when every accessible page has been reviewed, all identified visual issues have been fixed where feasible, shared fixes have been checked for regressions, and the available responsive tests have been performed.

Provide a final report listing:

- Every page reviewed.
- All issues discovered and fixed.
- Files and shared components changed.
- Responsive and animation tests performed.
- Any unresolved issues or limitations.

**Start by exploring the entire codebase and creating a complete page inventory. Then systematically inspect, fix, and verify the whole website. Be thorough and proactive: identify problems I have not explicitly mentioned and fix them too.**

Tip: If Claude has browser access, ask it to inspect the live rendered website as well as the source code. Source-code review alone cannot reliably catch every visual defect.