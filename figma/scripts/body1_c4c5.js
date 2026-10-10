// ===== Call 1: C4 · Page banners & headings, C5 · Images & frames (idempotent: skips a board that already exists) =====
const STRIP = await figma.getNodeByIdAsync('14:52'), HEADER = await figma.getNodeByIdAsync('14:129'), BTN = await figma.getNodeByIdAsync('9:490'), BTND = await figma.getNodeByIdAsync('9:541');
const variant = (set, name) => set.children.find(c => c.name === name);
const setLabel = (inst, label, arrow) => { const p = inst.componentProperties; const o = {}; for (const k of Object.keys(p)) { if (k.startsWith('Label')) o[k] = label; if (arrow !== undefined && k.startsWith('Arrow')) o[k] = arrow; } inst.setProperties(o); return inst; };
const abs = (node, parent, x, y) => { parent.appendChild(node); node.layoutPositioning = 'ABSOLUTE'; node.x = x; node.y = y; return node; };
const NB = (s) => s.replace('પ્રાણ પ્રતિષ્ઠા', 'પ્રાણ પ્રતિષ્ઠા');
const shots = [];
// ---- C3 check (read-only): report the phone strip text. If it shows the long text, the correction (fix_strip.js) is proposed for review and applied only after approval ----
const stripPhone = variant(STRIP, 'Device=Phone'); const stripMsg = stripPhone && stripPhone.findOne(n => n.type === 'TEXT' && n.name === 'Message'); const stripCheck = stripMsg ? stripMsg.characters : 'not found';

// ---------------- C4 ----------------
if (!existing('C4 · Banners & headings')) {
  const B = board('C4 · Banners & headings', 5200, 0, 1700);
  await head(B, '4', 'Page banners and section headings', 'One banner system for every inner page. Content is aligned to the top, so the breadcrumb starts 120 px below the banner top and the title always sits in the same place.');

  // Section heading: Align × Device
  { const h = await holder(B, 'Section heading'); const items = [];
    for (const align of ['Center', 'Left']) for (const dev of ['Desktop', 'Phone']) {
      const W = dev === 'Desktop' ? 1192 : 358;
      const c = comp(`Align=${align}, Device=${dev}`, align === 'Left' && dev === 'Desktop' ? 'HORIZONTAL' : 'VERTICAL', { w: W, gap: align === 'Center' ? 12 : 16, counter: align === 'Center' ? 'CENTER' : (dev === 'Desktop' ? 'MAX' : 'MIN'), primary: align === 'Left' && dev === 'Desktop' ? 'SPACE_BETWEEN' : 'MIN' }); h.appendChild(c);
      const stack = align === 'Left' && dev === 'Desktop' ? AL('VERTICAL', { name: 'Text', gap: 8, parent: c }) : c;
      const e = await T('મહોત્સવના કાર્યક્રમો', 'Text/Eyebrow', 'text/eyebrow', { parent: stack, name: 'Eyebrow', align: align === 'Center' ? 'CENTER' : 'LEFT' });
      const t = await T('સાત દિવસ, ત્રણ પાવન અવસર', (dev === 'Desktop' ? 'Desktop' : 'Phone') + '/Heading XL', 'text/heading', { parent: stack, name: 'Heading', align: align === 'Center' ? 'CENTER' : 'LEFT' });
      let lead = null;
      if (align === 'Center') { const o = AL('HORIZONTAL', { name: 'Ornament', gap: 12, parent: c, counter: 'CENTER' }); for (const k of [0, 1, 2]) { if (k === 1) { const d = figma.createNodeFromSvg('<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 10 10"><path d="M5 0L10 5L5 10L0 5Z" fill="#B78A35"/></svg>'); d.name = 'Diamond'; o.appendChild(d); recolor(d, 'border/ornament'); } else { const l = figma.createRectangle(); l.name = 'Rule'; l.resize(48, 1); l.fills = [paint('border/ornament')]; o.appendChild(l); } }
        lead = await T('ટ્રસ્ટ દ્વારા જાહેર થયેલ સત્તાવાર કાર્યક્રમ. સમયમાં કોઈ ફેરફાર થાય તો અહીં જાણ કરવામાં આવશે.', 'Text/Lead', 'text/muted', { parent: c, name: 'Lead', align: 'CENTER' }); lead.textAutoResize = 'HEIGHT'; lead.resize(Math.min(W, 680), lead.height); }
      else { const b = setLabel(variant(BTN, 'Type=Secondary, State=Default, Size=' + (dev === 'Desktop' ? 'Default' : 'Small')).createInstance(), 'સંપૂર્ણ કાર્યક્રમ', true); c.appendChild(b); }
      items.push({ c, e, t, lead });
    }
    const set = figma.combineAsVariants(items.map(i => i.c), h); set.name = 'Section heading'; finishSet(set, 'VERTICAL', 'surface/page');
    const kE = set.addComponentProperty('Eyebrow', 'TEXT', 'મહોત્સવના કાર્યક્રમો'), kH = set.addComponentProperty('Heading', 'TEXT', 'સાત દિવસ, ત્રણ પાવન અવસર');
    items.forEach(i => { i.e.componentPropertyReferences = { characters: kE }; i.t.componentPropertyReferences = { characters: kH }; });
    set.description = 'One heading style for every section. Eyebrow 15 px gold-ink, Heading XL (44 / 30 px) maroon, optional lead max 680 px. Centre adds the gold rule and diamond. No section numbers.'; created.push(set.id); }

  // Page banner: Size × Device
  { const h = await holder(B, 'Page banner — Feature (with page art) and Standard (text only)'); const items = [];
    for (const size of ['Feature', 'Standard']) for (const dev of ['Desktop', 'Phone']) {
      const D = dev === 'Desktop', W = D ? 1440 : 390;
      const c = comp(`Size=${size}, Device=${dev}`, 'VERTICAL', { w: W, fill: 'surface/inverse' }); c.clipsContent = true; h.appendChild(c);
      const glow = figma.createEllipse(); glow.name = 'Glow'; glow.resize(D ? 900 : 420, D ? 700 : 420); glow.fills = [{ type: 'GRADIENT_RADIAL', gradientTransform: [[1, 0, 0], [0, 1, 0]], gradientStops: [{ position: 0, color: { r: 0.455, g: 0.102, b: 0.196, a: 0.85 } }, { position: 1, color: { r: 0.455, g: 0.102, b: 0.196, a: 0 } }] }]; abs(glow, c, D ? 520 : 0, D ? 0 : 60);
      const ch = chakra.createInstance(); ch.name = 'Lotus chakra (15 %)'; const cs = D ? 720 : 420; ch.resize(cs, cs); ch.opacity = 0.15; abs(ch, c, W - cs / 2, D ? -180 : -60);
      const s = variant(STRIP, 'Device=' + dev).createInstance(); c.appendChild(s); s.layoutSizingHorizontal = 'FILL';
      const hd = variant(HEADER, 'Mode=Over hero, Device=' + dev).createInstance(); c.appendChild(hd); hd.layoutSizingHorizontal = 'FILL';
      const body = AL(D && size === 'Feature' ? 'HORIZONTAL' : 'VERTICAL', { name: 'Body', gap: D ? 40 : 28, pad: D ? [32, 124, 72, 124] : [32, 16, 40, 16], parent: c, fillW: true });
      if (D && size === 'Feature') { body.primaryAxisAlignItems = 'SPACE_BETWEEN'; body.counterAxisAlignItems = 'CENTER'; }
      const copy = AL('VERTICAL', { name: 'Copy', gap: 16, parent: body }); if (D) { copy.resize(size === 'Feature' ? 600 : 860, 10); copy.layoutSizingHorizontal = 'FIXED'; copy.layoutSizingVertical = 'HUG'; } else copy.layoutSizingHorizontal = 'FILL';
      const crumb = AL('HORIZONTAL', { name: 'Breadcrumb', gap: 8, parent: copy, counter: 'CENTER' }); await T('મુખ્ય પૃષ્ઠ', 'Text/Caption', 'text/on-dark-muted', { parent: crumb }); icon('chevron-right', 'text/on-dark-muted', 14, crumb);
      const cur = await T(size === 'Feature' ? 'પ્રાણ પ્રતિષ્ઠા' : 'સેવા નોંધણી', 'Text/Caption', 'text/on-dark', { parent: crumb, name: 'Current page' });
      const tg = D ? copy : AL('VERTICAL', { name: 'Title group', gap: 10, parent: copy, fillW: true }); // phone: eyebrow sits with the title
      await T('॥ જય શ્રી વિહત મેલડી માઁ ॥', 'Text/Eyebrow', 'text/on-dark-accent', { parent: tg, name: 'Eyebrow' });
      const title = await T(NB(size === 'Feature' ? 'મૂર્તિ પ્રાણ પ્રતિષ્ઠા મહોત્સવ' : 'સેવા માટે નોંધણી કરો'), (D ? 'Desktop' : 'Phone') + '/Display L', 'text/on-dark', { parent: tg, name: 'Title', fill: true });
      if (size === 'Standard') { await T('માઁના મહોત્સવમાં સેવા આપવી એ પણ ભક્તિ છે. નીચેની વિગતો ભરવા વિનંતી — ત્રણ પગલાં, આશરે ૩ મિનિટ.', 'Text/Lead', 'text/on-dark-muted', { parent: copy, name: 'Lead', fill: true }); }
      else {
        // Date panel. Desktop: two cells side by side. Phone: two rows, label left and date right, so a date never breaks and the year never sits alone.
        const dp = AL(D ? 'HORIZONTAL' : 'VERTICAL', { name: 'Date panel', radius: 12, stroke: 'text/on-dark-accent', sop: 0.35, parent: copy }); if (!D) dp.layoutSizingHorizontal = 'FILL';
        const DATES = D ? [['ભવ્ય મહોત્સવ', '૨ – ૮ ફેબ્રુઆરી ૨૦૨૭'], ['પ્રાણ પ્રતિષ્ઠા · બપોરે ૧૨:૩૯', '૮ ફેબ્રુ., સોમવાર']] : [['ભવ્ય મહોત્સવ', '૨ – ૮ ફેબ્રુઆરી ૨૦૨૭'], ['પ્રાણ પ્રતિષ્ઠા', '૮ ફેબ્રુ., સોમવાર']];
        for (const [i, [lab, val]] of DATES.entries()) {
          const cell = AL(D ? 'VERTICAL' : 'HORIZONTAL', { name: D ? 'Cell' : 'Row', gap: D ? 2 : 16, pad: D ? [12, 20, 12, 20] : [12, 18, 12, 18], parent: dp });
          if (!D) { cell.layoutSizingHorizontal = 'FILL'; cell.primaryAxisAlignItems = 'SPACE_BETWEEN'; cell.counterAxisAlignItems = 'BASELINE'; cell.layoutWrap = 'WRAP'; cell.counterAxisSpacing = 2; } // 320 px: the whole date moves under its label
          if (i) { cell.strokes = [paint('text/on-dark-accent', 0.35)]; cell.strokeLeftWeight = D ? 1 : 0; cell.strokeTopWeight = D ? 0 : 1; cell.strokeRightWeight = 0; cell.strokeBottomWeight = 0; }
          await T(lab, 'Text/Caption', 'text/on-dark-accent', { parent: cell, name: 'Label' }); TD(val, 'Noto Serif Gujarati', 'SemiBold', D ? 22 : 20, 'text/on-dark', cell, 'Value', 130);
        }
        const pill = AL('HORIZONTAL', { name: 'Countdown pill', gap: 10, pad: [8, 16, 8, 14], radius: 999, stroke: 'text/on-dark', sop: 0.3, parent: copy, counter: 'CENTER' }); const dot = figma.createEllipse(); dot.resize(8, 8); dot.fills = [paint('text/on-dark-accent')]; pill.appendChild(dot); await T('પ્રાણ પ્રતિષ્ઠાને ૧૨૧ દિવસ બાકી', 'Text/Small', 'text/on-dark', { parent: pill, name: 'Countdown (live)' });
        const row = AL('HORIZONTAL', { name: 'Actions', gap: 12, parent: copy }); if (!D) row.layoutSizingHorizontal = 'FILL';
        const b1 = setLabel(variant(BTND, 'Type=Light, State=Default, Size=Default').createInstance(), 'સેવા નોંધણી કરો', true), b2 = setLabel(variant(BTND, 'Type=Outline light, State=Default, Size=Default').createInstance(), 'કાર્યક્રમ જુઓ', false); row.appendChild(b1); row.appendChild(b2); if (!D) { const n1 = b1.width, n2 = b2.width; row.layoutWrap = 'WRAP'; row.counterAxisSpacing = 12; b1.layoutSizingHorizontal = 'FILL'; b2.layoutSizingHorizontal = 'FILL'; b1.minWidth = n1; b2.minWidth = n2; } // share a row only when both labels fit; a label never breaks
        if (D) { const art = AL('HORIZONTAL', { name: 'Page art (deity pair) — desktop and tablet only', gap: 16, parent: body, counter: 'MAX' });
          slot(256, 320, '01_deity_vihat-maa_cutout', art, 0, 'FIT'); slot(256, 320, '02_deity_meldi-maa_cutout', art, 0, 'FIT'); }
        else { // phone (approved 10 Oct): one image — the new-temple render, whole, standing on the bottom edge below the buttons
          body.itemSpacing = 24; body.paddingBottom = 0;
          const art = AL('HORIZONTAL', { name: 'Page art (new-temple render) — phone only', parent: body, fillW: true }); art.primaryAxisAlignItems = 'CENTER';
          slot(242, 190, '14_temple_new-temple-render', art, 0, 'FIT'); }
      }
      if (D) { c.counterAxisSizingMode = 'FIXED'; }
      items.push({ c, title, cur });
    }
    const set = figma.combineAsVariants(items.map(i => i.c), h); set.name = 'Page banner'; finishSet(set, 'VERTICAL', 'surface/page');
    set.description = 'Feature: New Temple, Festival, Gallery, History (page art on the right on desktop/tablet; on phone the festival banner shows one image instead of the deity pair: the new-temple render, whole, 190 px tall, below the buttons, standing on the bottom edge; dates in two rows). Desktop at least 680 px + 44 px strip. Standard: Darshan, Seva, Contact, 404 (text only; at least 460 px + strip). Breadcrumb 120 px below the banner top on every page. Keep “પ્રાણ પ્રતિષ્ઠા” together (non-breaking space). Chakra top-right, half visible, 15 %. Phone: eyebrow 10 px above the title and 16 px between groups on every inner page; buttons share a row only when both labels fit, otherwise each takes a full row, and a label never breaks inside a button; the 220 px cap applies to pictures only (the History contents list and the Gallery collage keep their full height). Wording is the approved site wording — no new devotional lines.'; created.push(set.id); }
  await notes(B, ['Banner heights were 423–792 px with the title anywhere from 228 to 378 px down. Now two sizes, top-aligned: the title is always in the same place.', 'Festival title broke as “મૂર્તિ પ્રાણ / પ્રતિષ્ઠા મહોત્સવ”. Display L is 60 px and “પ્રાણ પ્રતિષ્ઠા” never splits, so it fits one line on desktop.', 'Announcement strip on every inner page (was 4 of 8); phone uses the short text.', 'Phone festival banner 1,053 → 770 px (approved 10 Oct): the deity pair is replaced on phone by one image, the new-temple render shown whole below the buttons; the dates sit in two rows so the year never wraps; buttons in one row. Desktop and tablet keep the full composition with the deity pair.', 'Regression check on all 8 phone banners (preview, 10 Oct): breadcrumb at the same place on every page, no clipped Gujarati. Two problems found and fixed — the History contents list ran past the banner, and long button labels broke inside buttons on Darshan and New Temple.', 'Section heading unchanged: one style everywhere, no section numbers.']);
  shots.push(B);
}

// ---------------- C5 ----------------
if (!existing('C5 · Images & frames')) {
  const B = board('C5 · Images & frames', 7000, 0, 1600);
  await head(B, '5', 'Images and frames', 'Deities are always shown whole; portraits keep the face in the upper third; the temple render is never cropped through the flag. Image slots fill automatically from the 26 original files once they are dropped into the Assets section.');

  // Arch frame: Kind × Size
  { const h = await holder(B, 'Arch frame'); const items = [];
    for (const kind of ['Deity', 'Portrait']) for (const size of ['Large', 'Phone']) {
      const L = size === 'Large', W = L ? 298 : 161, H = L ? 372 : 201, ring = L ? 9 : 5;
      const c = comp(`Kind=${kind}, Size=${size}`, 'VERTICAL', { gap: L ? 16 : 10, counter: 'CENTER' }); h.appendChild(c);
      const outer = AL('VERTICAL', { name: 'Ring', pad: ring, fill: 'surface/page', stroke: 'border/default', parent: c }); outer.topLeftRadius = outer.topRightRadius = W / 2 + ring; outer.bottomLeftRadius = outer.bottomRightRadius = 8 + ring;
      const arch = figma.createFrame(); arch.name = 'Arch'; arch.resize(W, H); arch.topLeftRadius = arch.topRightRadius = W / 2; arch.bottomLeftRadius = arch.bottomRightRadius = 8; arch.fills = [paint('surface/alt')]; arch.strokes = [paint('border/ornament')]; arch.strokeWeight = 1.5; arch.strokeAlign = 'INSIDE'; arch.clipsContent = true; outer.appendChild(arch);
      const im = slot(W, H, kind === 'Deity' ? '01_deity_vihat-maa_cutout' : '07_portrait_karamshibapa_closeup-glow', arch, 0, kind === 'Deity' ? 'FIT bottom' : 'FILL focus 50/18'); im.strokes = []; im.x = 0; im.y = 0;
      const cap = AL('VERTICAL', { name: 'Caption', gap: 2, parent: c, counter: 'CENTER' });
      if (kind === 'Portrait') await T('પરમ પૂજ્ય', 'Text/Eyebrow', 'text/eyebrow', { parent: cap, name: 'Honorific', align: 'CENTER' });
      const nm = await T(kind === 'Deity' ? 'જય શ્રી વિહત માઁ' : 'ભગવાન શ્રી કરમશીબાપા', (L ? 'Desktop' : 'Phone') + '/Heading M', 'text/heading', { parent: cap, name: 'Name', align: 'CENTER' });
      items.push({ c, nm });
    }
    const set = figma.combineAsVariants(items.map(i => i.c), h); set.name = 'Arch frame'; finishSet(set, 'HORIZONTAL', 'surface/page', true); set.counterAxisAlignItems = 'MAX';
    set.description = 'Deity: whole figure (FIT), bottom-anchored on the warm glow — never cropped. Portrait: FILL with the face in the upper third (focus 50 % / 18 %), never zoomed past the frame. Ring: Large 1.5 gold + 9 ivory + 1 line; Phone 1.5 + 5 + 1 so it stays inside the 16 px margin; pairs 24 px apart.'; created.push(set.id); }

  // Photo tile with caption: Ratio
  { const h = await holder(B, 'Photo tile with caption (gallery, home strip)'); const items = [];
    for (const [ratio, W, H] of [['Tall', 380, 475], ['Wide', 560, 350]]) {
      const c = comp('Ratio=' + ratio, 'VERTICAL', { w: W, h: H, radius: 12, fill: 'surface/alt', primary: 'MAX' }); c.clipsContent = true; h.appendChild(c);
      const im = slot(W, H, '10_portrait_sureshbapa_blessing-glow', null, 0, 'FILL'); im.strokes = []; abs(im, c, 0, 0);
      const tag = AL('HORIZONTAL', { name: 'Tag', pad: [3, 12, 3, 12], radius: 999, fill: 'surface/page' }); await T('પરમ પૂજ્ય', 'Text/Caption', 'text/heading', { parent: tag, name: 'Tag label' }); abs(tag, c, 14, 14);
      const capf = AL('VERTICAL', { name: 'Caption', gap: 8, pad: [56, 16, 14, 16], parent: c, fillW: true }); capf.fills = [{ type: 'GRADIENT_LINEAR', gradientTransform: [[0, 1, 0], [-1, 0, 1]], gradientStops: [{ position: 0, color: { r: 0.122, g: 0.031, b: 0.063, a: 0 } }, { position: 0.38, color: { r: 0.122, g: 0.031, b: 0.063, a: 0.62 } }, { position: 1, color: { r: 0.122, g: 0.031, b: 0.063, a: 0.9 } }] }];
      const t = TD('પરમ પૂજ્ય ભુવાજી શ્રી સુરેશબાપા', 'Hind Vadodara', 'Medium', 16, 'text/on-dark', capf, 'Caption text', 140); const r = figma.createRectangle(); r.name = 'Gold rule'; r.resize(26, 2); r.fills = [paint('border/ornament')]; capf.appendChild(r);
      items.push({ c, t });
    }
    const set = figma.combineAsVariants(items.map(i => i.c), h); set.name = 'Photo tile'; finishSet(set, 'HORIZONTAL', 'surface/page'); set.counterAxisAlignItems = 'MAX';
    const k = set.addComponentProperty('Caption', 'TEXT', 'પરમ પૂજ્ય ભુવાજી શ્રી સુરેશબાપા'); items.forEach(i => i.t.componentPropertyReferences = { characters: k });
    set.description = 'Caption 16 px ivory over a fade: transparent → 62 % at 38 % → 90 % burgundy-night. Measured 7.5 : 1 on a light photo (was 3.1 : 1).'; created.push(set.id); }

  // Photo coming soon: Ratio
  { const h = await holder(B, '“Photo coming soon” tile — one style for news, gallery, history and the construction diary'); const items = [];
    for (const [ratio, W, H] of [['Wide', 560, 350], ['Tall', 380, 475], ['Square', 360, 360]]) {
      const c = comp('Ratio=' + ratio, 'VERTICAL', { w: W, h: H, radius: 12, fill: 'surface/alt', gap: 10, counter: 'CENTER', primary: 'CENTER' }); c.clipsContent = true; h.appendChild(c);
      const ch = chakra.createInstance(); const cs = Math.round(Math.min(W, H) * 0.86); ch.resize(cs, cs); ch.opacity = 0.14; abs(ch, c, (W - cs) / 2, (H - cs) / 2);
      icon('camera', 'text/eyebrow', 32, c); const t = await T('[નિર્માણ કાર્યનો તાજો ફોટો]', 'Text/Small', 'text/muted', { parent: c, name: 'Label', align: 'CENTER' });
      items.push({ c, t });
    }
    const set = figma.combineAsVariants(items.map(i => i.c), h); set.name = 'Photo coming soon'; finishSet(set, 'HORIZONTAL', 'surface/page'); set.counterAxisAlignItems = 'MAX';
    const k = set.addComponentProperty('Label', 'TEXT', '[નિર્માણ કાર્યનો તાજો ફોટો]'); items.forEach(i => i.t.componentPropertyReferences = { characters: k });
    set.description = 'Shown while a real photo is awaited. Cream ground, faint lotus chakra, gold-ink camera, the [bracket] label. No dashed borders — they read as wireframes.'; created.push(set.id); }

  // Temple crop rule
  { const h = await holder(B, 'Temple render — crops'); const row = AL('HORIZONTAL', { name: 'Crop rule', gap: 32, parent: h, fillW: true, counter: 'CENTER' });
    const f = figma.createFrame(); f.name = 'Crop example · shikhar and flag'; f.resize(360, 450); f.cornerRadius = 8; f.fills = [paint('surface/alt')]; f.clipsContent = true; row.appendChild(f);
    const im = slot(1200, 940, '14_temple_new-temple-render', f, 0, 'FIT'); im.strokes = []; im.x = -420; im.y = 24;
    const g = figma.createRectangle(); g.name = '24 px air above the flag'; g.resize(360, 24); g.fills = [paint('text/accent-flag', 0.18)]; f.appendChild(g); g.x = 0; g.y = 0;
    const tx = AL('VERTICAL', { name: 'Rules', gap: 8, parent: row }); tx.layoutSizingHorizontal = 'FILL';
    for (const s of ['The full temple render is always completely visible (hero, new-temple band, gallery, festival banner on the phone).', 'Detail crops keep at least 24 px of air above the ધજા (flag) — today the flag runs into the frame on the New Temple page.', 'Deity artwork is never cropped or redrawn; portraits are never zoomed past the frame.', 'Every image keeps its original file; slots fill from the 26 files in the Assets section.']) await T('• ' + s, 'Text/Body', 'text/primary', { parent: tx, fill: true }); }
  await notes(B, ['Phone arch pairs reached 6 px from the screen edge because of the 10 px ring; phone ring is now 6 px and pairs sit 24 px apart.', 'Karamshibapa’s portrait on the phone history page was zoomed until the face was cut at the moustache; portraits now fill the arch with the face in the upper third.', 'Captions over photos measured 2.3–3.3 : 1; the stronger fade measures 7.5 : 1.', 'Dashed “wireframe” placeholders replaced by one cream “coming soon” tile.', 'Flag touched the top of the crop; 24 px of air above it.']);
  shots.push(B);
}
const c3 = await figma.getNodeByIdAsync('14:37');
for (const b of [c3, ...shots]) await b.screenshot({ scale: 0.4 });
return { stripPhoneText: stripCheck, created, boards: shots.map(b => ({ id: b.id, name: b.name, size: [Math.round(b.width), Math.round(b.height)] })) };
