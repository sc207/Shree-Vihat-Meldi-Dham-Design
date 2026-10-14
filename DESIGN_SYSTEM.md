# DESIGN_SYSTEM.md

How the website looks and speaks. Values come from the design files (`design/project/ds/vihatmeldimandir/tokens.json`,
`components/bundle.css`, `site.css`). When this file and the files disagree, **the files win** — fix this file.

## Foundations

- **Language:** Gujarati only (`<html lang="gu">`), Gujarati numerals in running text (૦–૯). Phone numbers stay in Latin digits (99095 52020).
- **Fonts:** display/headings **Noto Serif Gujarati**; body/UI **Hind Vadodara** (fallback Noto Sans Gujarati). Loaded from Google Fonts in each
  page's `<helmet>`; for local renders install them with npm (see [TESTING.md](TESTING.md)). Gujarati needs tall leading: body 1.75.
  "Baloo Bhai 2" (poster) is for printed/social collateral only — never on the website.
- **Colour rules that matter most:** maroon `#741a32` is the brand/action colour; gold `#b78a35` is decorative only (never body text on light grounds) —
  readable gold is `--gold-ink` on light and `--gold-soft` on dark; logo red `#e31e24` only in the logo; WhatsApp green only inside its glyph.
- **One easing curve** (`--ease-temple`); motion is disabled under `prefers-reduced-motion`.
- **Lotus chakra ornament** (`.vm-hero__mandala`): stays in the banner's top-right corner, half visible, opacity 15 %.
- **One chakra drawing only (since v108).** Every chakra uses the lotus mandala (`viewBox="-200 -200 400 400"`, the drawing in `.vm-hero__mandala`):
  banner corner, closing devotional band (`.vm-devotional__mandala`), the dark "નવું મંદિર" band on Home (`.vm-mandala`), the CTA card corner (`.vm-cta__orn`)
  and the photo-slot tile (`.vx-slot`, as a data-URI). The old oval-petal chakra is retired — never copy it back from an old version or from Figma.
- **Banner light belongs to the picture (since v109).** On banners with a picture the gold light is `.vm-hero__art::before` and the breathing halo
  `.vm-hero__halo` is centred in the picture box (`translate`, breathing via `scale`), so both follow the picture at every width and orientation.
  Never position a light or halo with banner- or viewport-relative coordinates, and never animate `transform` on an element whose position uses `transform`.
  The closing devotional band's light is a band-wide ambient light (centred behind title and deities) and stays as it is.

### Colour tokens (from `project/ds/vihatmeldimandir/tokens.json`)

| Token | Value | Use |
|---|---|---|
| `--maroon` | #741a32 | Temple Maroon — the primary brand colour. Headings, primary buttons, active navigation, links. 10.2:1 on ivory. Identical in both themes (brand constant). |
| `--maroon-deep` | #5c1227 | Pressed / hover state of maroon fills. Ivory text on it is 12.5:1. |
| `--burgundy` | #481022 | Deep Burgundy — dark sections: hero at dusk, heritage chapters, footer. Pair with ivory text (14.3:1) or gold-soft (8.9:1). |
| `--gold` | #b78a35 | Antique Gold — decorative ONLY: hairline rules, ornament strokes, icon outlines, small diamonds. 2.9:1 on ivory, so never body text on light grounds. On burgundy it reads 4.9:1 and may carry 18px+ labels. |
| `--gold-soft` | #e2c27a | Gold for TEXT on burgundy and maroon grounds: eyebrows, dates, numerals in dark sections (8.9:1 on burgundy). |
| `--ivory` | #fbf7ef | Warm Ivory — the literal page colour. Also the text colour on maroon and burgundy. |
| `--cream` | #f2e6d2 | Temple Cream — the literal secondary ground for alternating sections and form panels. |
| `--charcoal` | #29272a | Charcoal — the literal primary text colour. |
| `--muted-brown` | #74675e | Muted Brown as specified in the brief. 5.1:1 on ivory but only 4.4:1 on cream — for secondary text on cream use ink-muted instead. |
| `--saffron` | #b4461a | Dhaja saffron — the temple flag. Tiny accents only: the live/‘નવું’ dot, the flag glyph, one word of emphasis per page at most. 5.1:1 on ivory. |
| `--logo-red` | #e31e24 | Exact ink of the supplied logo artwork. Reserved for the logo and mark; never for UI, text or buttons. |
| `--whatsapp` | #25d366 | WhatsApp's own green — only inside the WhatsApp glyph disc. Never as a text colour or button fill. |
| `--whatsapp-deep` | #0f6b3f | Fill of the ‘WhatsApp સમુદાયમાં જોડાઓ’ button. White text on it is 6.6:1. |
| `--surface` | day #fbf7ef · night #1c0a10 | Page background. Ivory by day; near-black sanctum by night. |
| `--surface-alt` | day #f2e6d2 · night #26101a | Alternating section ground and form panels. |
| `--surface-raised` | day #fffdf8 · night #2e1520 | Cards, accordions, form inputs, header after scroll. |
| `--surface-inverse` | day #481022 · night #0f0508 | Dark storytelling sections inside a light page (hero at dusk, heritage, footer). |
| `--ink` | day #29272a · night #f6eedf | Body text on surface, surface-alt and surface-raised (13.9:1 day, 16.6:1 night). |
| `--ink-muted` | day #675a51 · night #c9b8a6 | Secondary text — captions, meta, dates — on surface, surface-alt and surface-raised (≥4.9:1 in both themes). |
| `--ink-inverse` | day #fbf7ef · night #f6eedf | Text on surface-inverse, maroon and burgundy. |
| `--ink-inverse-muted` | day #d9c6b3 · night #c9b8a6 | Secondary text on surface-inverse (≥8:1). |
| `--accent` | day {maroon} · night #e2c27a | Interactive colour: primary button fill, links, active nav, selected chips. Maroon by day, gold-soft by night. |
| `--accent-hover` | day {maroon-deep} · night #efd394 | Hover/pressed accent. |
| `--on-accent` | day #fbf7ef · night #2a0b14 | Text and icons on an accent fill (10.2:1 day, 10.6:1 night). |
| `--heading` | day {maroon} · night #f3dfb4 | Display and section headings on surface and surface-alt. |
| `--gold-ink` | day #86621f · night #d9b266 | Gold that may be READ: eyebrows, small ornament labels, numerals on light grounds (5.2:1 on ivory, 4.5:1 on cream). |
| `--line` | day #e4d6be · night #3e2029 | Hairline dividers and card borders — decorative, not a control boundary. |
| `--line-strong` | day #9c8a73 · night #946f77 | Input and checkbox borders — control boundaries (3.1:1 on their grounds). |
| `--focus` | day #b25e12 · night #f2c66d | The focus ring: 2px solid, 3px offset, on every interactive element. ≥4.3:1 on ivory, ≥6:1 on maroon; ≥11:1 at night. |
| `--success` | day #1f5f5b · night #7cc7be | Form success (registration received). Always with a check icon and words — never colour alone. |
| `--danger` | day #b03a1e · night #f09a7e | Form errors. Always with an alert icon and a Gujarati sentence explaining the fix. |
| `--scrim` | day rgba(28,10,16,0.62) · night rgba(15,5,8,0.72) | Overlay behind the mobile menu and the gallery lightbox. |

### Type scale

| Style | Family | Size / line-height / weight | Use |
|---|---|---|---|
| display-xl | display | 88px / 1.12 / 600 | One per page: the hero headline. Fluid clamp(44px, 7vw, 88px). |
| display-l | display | 64px / 1.16 / 600 | Inner page heroes and the closing devotional line. clamp(38px, 5.5vw, 64px). |
| heading-xl | display | 44px / 1.25 / 600 | Section headings. clamp(30px, 4vw, 44px). |
| heading-l | display | 32px / 1.3 / 600 | Sub-sections, chapter titles in the history book. clamp(26px, 3vw, 32px). |
| numeral | display | 56px / 1 / 500 | Gujarati numerals for dates and countdown units. |
| heading-m | body | 22px / 1.4 / 600 | Card titles, event names, FAQ questions. |
| body-l | body | 20px / 1.75 / 400 | Lead paragraphs under a section heading. Max 60ch. |
| body-m | body | 17px / 1.75 / 400 | Default body copy. Max 68ch. Gujarati needs the tall 1.75 leading for matras. |
| body-s | body | 15px / 1.65 / 400 | Card descriptions, form help text, footer links. |
| caption | body | 13px / 1.5 / 500 | Image captions and meta. ink-muted. |
| eyebrow | body | 15px / 1.4 / 600 | The line above a section heading, in gold-ink (gold-soft on dark). |
| label | body | 15px / 1.3 / 600 | Buttons, nav links, form labels. |
| poster-display | poster | 104px / 1.05 / 800 | Printed posters and WhatsApp/Instagram announcement graphics only — never on the website, which speaks in the display serif. |

Families: **display** = "Noto Serif Gujarati", "Noto Serif", Georgia, serif · **body** = "Hind Vadodara", "Noto Sans Gujarati", system-ui, sans-serif · **poster** = "Baloo Bhai 2", "Hind Vadodara", sans-serif

**Spacing:** `--space-xs` 4px · `--space-sm` 8px · `--space-md` 16px · `--space-lg` 24px · `--space-xl` 40px · `--space-2xl` 64px · `--space-3xl` 104px · `--space-4xl` 152px

**Radius:** `--radius-sm` 8px · `--radius-md` 12px · `--radius-lg` 16px · `--radius-arch` 999px · `--radius-pill` 999px

**Duration:** `--motion-fast` 180ms · `--motion-normal` 420ms · `--motion-slow` 900ms · `--motion-ambient` 28s

**Easing:** `--ease-temple` cubic-bezier(0.22, 1, 0.36, 1)

**Layout:** `--content-max` 1320px · `--text-max` 680px · `--header-height` 88px · `--header-height-compact` 68px

### Image inventory (27 originals; `design/assets/<blob-id>.<ext>`, pages use `/_blob/<blob-id>`)

| # | Original file name (keep unchanged) | Blob id | Pixels | Used on |
|---|---|---|---|---|
| 01 | `01_deity_vihat-maa_cutout` | `9e553826353008ace0348667feebc15c` | 1200×1500 | Contact, Darshan, Gallery, History, Main, NewTemple, PranPratishtha |
| 02 | `02_deity_meldi-maa_cutout` | `11b539b692a86f3ebd187f4cdccda6f2` | 1200×1500 | Contact, Darshan, Gallery, History, Main, NewTemple, PranPratishtha |
| 03 | `03_deity_vihat-maa_glow` | `5db2fa3066346bbda071d80127890079` | 760×905 | Gallery, History |
| 04 | `04_deity_meldi-maa_glow` | `67db8acad0ff4fc9a1690e90a08d539b` | 670×921 | Gallery, History |
| 05 | `05_deity_lakhnechi-maa_glow` | `e31c2f7a518cb9d094489412d6c323c8` | 380×534 | Gallery, History |
| 06 | `06_deity_goga-maharaj_glow` | `713e6519487a5ab4a26d821bbca861a8` | 393×534 | Gallery, History |
| 07 | `07_portrait_karamshibapa_closeup-glow` | `692526c97fb81800db3adb90c432cc9a` | 1100×985 | — (not used since v110; replaced by 27) |
| 08 | `08_portrait_karamshibapa_standing-white` | `01d1d891218823b7fc6777885d8634d1` | 1000×1497 | Gallery |
| 09 | `09_portrait_karamshibapa_seated-poster` | `361278fe9fd6e85e999500f1f74013a3` | 784×1045 | Gallery |
| 10 | `10_portrait_sureshbapa_blessing-glow` | `4e30bcd6319bfef6bce709ce0ef4afb1` | 1100×1019 | Gallery, History, Main |
| 11 | `11_portrait_sureshbapa_candid` | `e1b6930a984c9f3a8eb9b9783ae97fe9` | 585×882 | Gallery, History |
| 12 | `12_portrait_sureshbapa_seated-poster` | `ea3a22f667e1db20db6134f406df44bb` | 960×1279 | Gallery |
| 13 | `13_portrait_sureshbapa_smiling-cutout` | `f784ff0d57da00d73030819bb850bb43` | 470×501 | Gallery |
| 14 | `14_temple_new-temple-render` | `ade906fff7b8cbe4a63f246237926871` | 2400×1881 | Gallery, History, Main, NewTemple, PranPratishtha |
| 15 | `15_banner_dham-family` | `cd5574347256c288677d3f0e7b95dbc2` | 1800×1199 | Gallery |
| 16 | `16_logo_mark-red` | `e1c9cc4c85b15c1aea37fad5675f6596` | 708×708 | Contact, Darshan, Gallery, History, Main, NewTemple, NotFound, Offline, PranPratishtha, Seva |
| 17 | `17_logo_mark-ivory` | `6cb43041a704672ae77ed549a7399de9` | 708×708 | Contact, Darshan, Gallery, History, Main, Menu, NewTemple, NotFound, PranPratishtha, Seva |
| 18 | `18_logo_lockup-ivory_footer` | `b3915972ce74551f3675e24488a5ed84` | 2914×812 | Contact, Darshan, Gallery, History, Main, NewTemple, NotFound, PranPratishtha, Seva |
| 19 | `19_qr_whatsapp-channel` | `d359256f876ef152e1aa584ebb20b4e8` | 624×624 | Contact, Darshan, Gallery, History, Main, NewTemple, PranPratishtha |
| 20 | `20_unused_logo_lockup-red` | `935458ac98acacb809b0d1329e9b374e` | 2914×812 | — (not used) |
| 21 | `21_unused_deity_vihat-maa_cutout-large` | `95787e5469dde0e0ecebc09bef4a4a4a` | 1768×2000 | — (not used) |
| 22 | `22_unused_deity_meldi-maa_cutout-large` | `a6fe6bdb26e6dded27110709664aea5a` | 1446×2000 | — (not used) |
| 23 | `23_unused_gaadi_cutout` | `41bb877f7d1d833f978493c6366d07a1` | 531×470 | — (not used) |
| 24 | `24_unused_diya_cutout` | `70db10d832218539d0ef40367176309a` | 478×521 | — (not used) |
| 25 | `25_unused_naag_cutout-small` | `624e213ce2a19b887b8069e53658baea` | 183×275 | — (not used) |
| 26 | `26_unused_poster_karamshibapa-e-j-vihat` | `d142fc2cdd2cad709f1a711292912aac` | 960×1279 | — (not used) |
| 27 | `27_portrait_karamshibapa_blessing-glow` | `0719d6d6a37c83a09b9880ba4507c70f` | 1086×1448 | Gallery (banner), History, Main — owner's photo, added 14 Oct 2026 (v110) |

`Used on` names the page family (Main = all home boards; each page includes its phone version). Images 20–26 are supplied but unused; 07 unused since v110.
The owner's originals for 27 (and an unused seated full-length photo) are in `tasks/bapa-photo/originals/`.
Keep the **original file names** unchanged (they are also how the Figma script matches images).

### Image handling rules

- Deities and portraits sit in the **arch frame** (`.vm-arch`, top corners `--radius-arch`), with `.vx-portrait-fix` keeping faces in frame.
- The new-temple render (14) is cropped with `.vx-crop` frames; `.vx-flag-fix` keeps the flag inside the crop.
- Phone festival banner: **one** image (14, whole, 190 px tall, below the buttons); desktop/tablet keep the deity pair (01 + 02).
- Missing photos use the "photo coming soon" tile (cream, faint chakra, `[placeholder]` caption) — never a stock photo.
- Logos: 16 (red mark) on light grounds, 17 (ivory mark) on dark, 18 (ivory lockup) in the footer. 19 = WhatsApp channel QR (hidden on small screens).

## Layout and responsive behaviour

- **Boards** (canvas artboards): desktop 1440 · tablet portrait 834 (`HomeTablet`) · tablet landscape 1180 (`HomeTabletL`) · phone landscape 844 (`HomePhoneL`) ·
  phone 390 (`…Mobile`). The real site is fluid; boards are fixed-size previews. Content max width 1320 px; prose max ~68ch.
- **Breakpoints in use** (site.css / bundle.css): phone ≤ 760 · tablet 761–899 / 761–1023 / 761–1099 · stacked facts and hero art hidden ≤ 999 ·
  two-column splits from 768 (`.vm-grid--split` 5:7) · 3-column grids from 1100 · small phones ≤ 360 · short landscape (`max-height: 500px`).
- Must work at **320, 360, 390, 430** px and tablet/desktop widths without sideways scrolling, clipped Gujarati, or broken button labels.
- Phone rules established in Gate A: buttons `white-space: nowrap`, button rows wrap; headings `text-wrap: balance`; a year never sits alone
  on a line (non-breaking space before ૨૦૨૭ — 75 occurrences in the pages); CTA cards 32 px / 24 px padding on phones.
- Large-text mode (button **અ+** in the header): adds class `is-big` to the page root (stored in `localStorage` key `vx-fs`) and zooms body text 1.14×.
  New components must be checked in both sizes.

## Page structure

Every content page, top to bottom:

1. Skip link "મુખ્ય સામગ્રી પર જાઓ".
2. Festival strip `.vm-notice` (inner pages): "મૂર્તિ પ્રાણ પ્રતિષ્ઠા મહોત્સવ · તા. ૨ થી ૮ ફેબ્રુઆરી, ૨૦૨૭ · વિગતો જુઓ" (shorter text on phones).
3. Banner `.vm-hero` with the header over it (`.vm-header--over-hero`): brand (mark + "શ્રી વિહત મેલડી ધામ / સાણંદ · ગુજરાત"), navigation, અ+ toggle, phone menu button.
4. Content sections `.vm-section` alternating ivory / cream (`--alt`) / dark (`--inverse`); section heading = eyebrow (`.vm-eyebrow`) + `h2.vm-h1` (+ `.vm-lead`).
5. **Page ending (approved rule):** WhatsApp band (`.vm-wa`) → devotional band (`.vm-devotional.vx-close`, "॥ ૐ ॥ / જય શ્રી વિહત મેલડી માઁ" + shloka) → footer (`.vm-footer`).
   Exceptions: the Seva form page and 404 end with the footer only (404 offers the way home).
6. Phones: fixed bottom action bar `.vx-abar` — દર્શન · મહોત્સવ · રસ્તો · ફોન કરો.

**Navigation (order):** મુખ્ય પૃષ્ઠ · દર્શન અને યાત્રા · નવું મંદિર · પ્રાણ પ્રતિષ્ઠા · સેવા નોંધણી · ગેલેરી અને સમાચાર · મંદિરનો ઇતિહાસ · સંપર્ક.
Page files: `Main` (home), `NewTemple`, `PranPratishtha` (festival), `Seva`, `Gallery`, `History`, `Contact`, `Darshan`, `NotFound` (404), plus phone-only `MenuMobile`, `OfflineMobile`.

**Live behaviour in the page logic (`DCLogic` class at the end of each page):** festival countdown (to 8 Feb 2027 12:39 IST), darshan open/closed card,
"આજે" ગાદી marker (Indian date; પૂનમ dates from the `EV` list), upcoming-days calendar (`EV` list, Oct 2026 – Apr 2027), festival day tabs, text-size toggle.
All date logic uses Indian time (UTC+5:30).

## Components

Design-system components (`vm-*`, from `bundle.css`): buttons (`vm-btn`, `--secondary`, `--light`, `--outline-light`, `--whatsapp`, `--block`), chips,
form fields, header/nav/phone menu, hero, section/heading, cards (event, contact), arch frame, gallery, journey timeline (`vm-journey`), FAQ, CTA card (`vm-cta`),
WhatsApp band, devotional band, footer, `vm-sr` (screen-reader-only text).
Site components (`vx-*`, in `site.css`) include: home festival summary (`vx-sumacts`, `vx-night(s)`), countdown (`vx-live`, `vx-cd`), festival plan/day cards
(`vx-plan`, `vx-day(s)`), Darshan timetable (`vx-tt`, `vx-tt__week`, `vx-ttc`), calendar (`vx-cal`), facts row (`vx-facts`), crops (`vx-crop`), history book
(`vx-book`), progress (`vx-prog`), New Temple સંકલ્પ layout (`vx-prose`, `vx-sk`), page strip/compact hero (`vx-hero-compact`), action bar (`vx-abar`).
Full class list: `grep -o 'class="[^"]*"' design/project/*.dc.html`.

CSS conventions: design-system CSS is never edited; site rules live in `site.css`; every new change is appended at the end as a block headed
`/* ════════ <what> (vNNN) ════════ */`, scoped as narrowly as possible (a new class on the section, not a global selector).

## Gujarati wording, names and spelling

Use these forms in new or edited text (they are the site's standard). **Do not "correct" existing approved copy** that differs for a reason —
see the approved variants below the table. Searching tip: the pages put a **non-breaking space** before ૨૦૨૭ (`ફેબ્રુઆરી,\u00a0૨૦૨૭`),
so search for `ફેબ્રુઆરી,` or use a regex `ફેબ્રુઆરી,\s૨૦૨૭`.

| Use | Not |
|---|---|
| ભગવાન શ્રી કરમશીબાપા (respectful pronoun: તેઓશ્રી) | કરમશી બાપા, તેમના |
| ભુવાજી શ્રી સુરેશબાપા | |
| શ્રી વિહત મેલડી માઁ · માતાજી | |
| શ્રી વિહત મેલડી ધામ, ગેપ્પરા, સાણંદ (address: ગેપ્પરા, સાણંદ, ગુજરાત ૩૮૨૧૧૦) | સનંદ (ગેપ્પરા spelling still to be confirmed by the trust) |
| મૂર્તિ પ્રાણ પ્રતિષ્ઠા મહોત્સવ · તા. ૨ થી ૮ ફેબ્રુઆરી, ૨૦૨૭ | other date formats |
| પ્રાણ પ્રતિષ્ઠા ૮ ફેબ્રુઆરી, બપોરે ૧૨:૩૯ | |
| ૯ ફેબ્રુઆરી appears only as **સમાપન** | |
| Hours: દરરોજ સવારે ૬ થી રાત્રે ૧૦, વિરામ વિના; ગાદી and ભોજનશાળા: **અવિરત** | |
| Jaykaar: ॥ જય શ્રી વિહત મેલડી માઁ ॥ | |
| સામૂહિક | સમૂહિક |

Approved variants already on the site (keep as they are):
- Phone festival strip uses the short form "૨–૮ ફેબ્રુ." (8 phone pages); desktop strips use the full date.
- Quotations and verse keep their own wording: “કરમશીબાપા એ જ વિહત” (home/history) and the New Temple verse "… શ્રી સુરેશબાપાના સાનિધ્યથી …".
- Address lines read "ગેપ્પરા, સાણંદ, ગુજરાત ૩૮૨૧૧૦" (and "ગેપ્પરા, સાણંદ"); brand line "સાણંદ · ગુજરાત".
- Hours appear as "દરરોજ સવારે ૬ થી રાત્રે ૧૦", "સવારે ૬ – રાત્રે ૧૦" and "સવારે ૬:૦૦ – રાત્રે ૧૦:૦૦ · વિરામ વિના" (timetable).
- The festival heading "એક પાવન અવસર, સાત દિવસનો ઉત્સવ" is approved; it is not the reserved line below.

Reserved / not to be used on the site yet:
- "॥ ભગવાન કરમશી બાપાના પાવન આશીર્વાદથી ॥" — reserved for the opening of the promotional video, **not** the banner.
- "એક પાવન અવસર · માતાજીનાં દર્શન અને આશીર્વાદ" — not used yet.

Fixed facts and policies (do not contradict): યજ્ઞ registration is in person or by phone, payment in cash · the Seva form collects volunteer details only ·
no live darshan · removed items stay removed · contact phone 99095 52020 (tel:+919909552020) · WhatsApp channel
`https://whatsapp.com/channel/0029Vb8yWK3DZ4LbUcJhBt3w` · Instagram `jay_vihat_meldi_ma_dham_sanand`.
The "કાર્યક્રમ પત્રિકા (PDF)" button is hidden by the `.vx-patrika` rule until the trust's PDF exists (restore steps are in the comment above that rule).

Trust-supplied text is placed word-for-word; only spelling/honorific alignment to the forms above, and every such edit is reported to the owner.

## Accessibility

- Contrast is designed into the tokens (ratios listed per token above); focus ring `--focus`, 2 px, 3 px offset, on every interactive element.
- Gujarati `aria-label`s on landmarks and icon buttons; decorative SVG/ornaments `aria-hidden`; extra screen-reader wording via `.vm-sr`.
- Never rely on colour alone (e.g. ગાદી tiles also carry screen-reader text; form states use icon + sentence).
- Respect `prefers-reduced-motion`; the large-text mode must not clip or overflow.
