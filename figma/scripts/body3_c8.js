// ===== Call 3: C8 · Page endings (idempotent) =====
const abs = (node, parent, x, y) => { parent.appendChild(node); node.layoutPositioning = 'ABSOLUTE'; node.x = x; node.y = y; return node; };
const rule = (parent, color, op) => { const r = figma.createRectangle(); r.name = 'Rule'; r.resize(100, 1); r.fills = [paint(color, op)]; parent.appendChild(r); r.layoutSizingHorizontal = 'FILL'; return r; };
const WA = await figma.getNodeByIdAsync('9:556');
const setLabel = (inst, label) => { const p = inst.componentProperties; const o = {}; for (const k of Object.keys(p)) if (k.startsWith('Label')) o[k] = label; inst.setProperties(o); return inst; };
const DIAM = '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 10 10"><path d="M5 0L10 5L5 10L0 5Z" fill="#B78A35"/></svg>';
const PAGES = ['મુખ્ય પૃષ્ઠ', 'દર્શન અને યાત્રા', 'નવું મંદિર', 'પ્રાણ પ્રતિષ્ઠા', 'સેવા નોંધણી', 'ગેલેરી અને સમાચાર', 'મંદિરનો ઇતિહાસ', 'સંપર્ક'];
const FEST = ['કાર્યક્રમની રૂપરેખા', 'સેવા નોંધણી', 'જાહેરાતો', 'સામાન્ય પ્રશ્નો'];
const CONTACT = ['99095 52020', 'WhatsApp પર સંદેશ', 'ગેપ્પરા, સાણંદ, ગુજરાત ૩૮૨૧૧૦'];
const shots = [];
if (!existing('C8 · Page endings')) {
  const B = board('C8 · Page endings', 12100, 0, 1700);
  await head(B, '8', 'Page endings', 'Approved 10 Oct 2026. Content pages (Home, Darshan, New Temple, Festival, Gallery, History, Contact) end with WhatsApp band → devotional band → footer. Seva registration form and 404 end with the footer only; 404 keeps a clear route back to the home page. On phone the bands stay proportionate to the screen.');
  // WhatsApp band
  { const h = await holder(B, 'WhatsApp band — one style everywhere (white card on cream)'); const items = [];
    for (const dev of ['Desktop', 'Phone']) { const D = dev === 'Desktop';
      const c = comp('Device=' + dev, D ? 'HORIZONTAL' : 'VERTICAL', { w: D ? 1192 : 358, pad: D ? 64 : [28, 20, 28, 20], gap: D ? 48 : 16, radius: 16, fill: 'surface/raised', stroke: 'border/default', counter: 'CENTER' }); h.appendChild(c);
      const g = AL('HORIZONTAL', { name: 'Glyph', radius: 999, fill: 'action/whatsapp', parent: c, counter: 'CENTER' }); g.primaryAxisAlignItems = 'CENTER'; const gs = D ? 96 : 56; g.resize(gs, gs); g.primaryAxisSizingMode = 'FIXED'; g.counterAxisSizingMode = 'FIXED'; icon('whatsapp', 'text/on-dark', D ? 44 : 30, g);
      const cp = AL('VERTICAL', { name: 'Copy', gap: 10, parent: c, counter: D ? 'MIN' : 'CENTER' }); cp.layoutSizingHorizontal = 'FILL';
      const al = D ? 'LEFT' : 'CENTER';
      await T('સમાચાર સીધા આપના ફોન પર', 'Text/Eyebrow', 'text/eyebrow', { parent: cp, align: al }); await T('WhatsApp ચેનલમાં જોડાઓ', (D ? 'Desktop' : 'Phone') + '/Heading L', 'text/heading', { parent: cp, align: al }); await T('મહોત્સવનો કાર્યક્રમ, દર્શનનો સમય, સેવાનો લાભ અને ધામની દરેક જાહેરાત — સૌથી પહેલાં આપ સુધી.', 'Text/Body', 'text/muted', { parent: cp, fill: true, align: al });
      const ck = AL('HORIZONTAL', { name: 'Checklist', gap: D ? 20 : 14, parent: cp, counter: 'CENTER' }); if (!D) { ck.layoutWrap = 'WRAP'; ck.counterAxisSpacing = 4; ck.primaryAxisAlignItems = 'CENTER'; ck.resize(318, 24); ck.primaryAxisSizingMode = 'FIXED'; ck.counterAxisSizingMode = 'AUTO'; } for (const s of ['સત્તાવાર જાહેરાતો', 'મહોત્સવના સમાચાર', 'સેવા માટે આમંત્રણ']) { const r = AL('HORIZONTAL', { name: s, gap: 6, parent: ck, counter: 'CENTER' }); icon('check', 'text/eyebrow', 16, r); await T(s, 'Text/Small', 'text/primary', { parent: r }); }
      if (D) { const q = AL('VERTICAL', { name: 'QR', gap: 8, parent: c, counter: 'CENTER' }); slot(120, 120, '19_qr_whatsapp-channel', q, 8, 'FIT'); await T('ફોનના કૅમેરાથી સ્કૅન કરો', 'Text/Caption', 'text/muted', { parent: q, align: 'CENTER' }); }
      const ac = AL('VERTICAL', { name: 'Action', gap: 8, parent: c, counter: 'CENTER' }); if (!D) ac.layoutSizingHorizontal = 'FILL';
      const b = setLabel(WA.defaultVariant.createInstance(), 'ચેનલમાં જોડાઓ'); ac.appendChild(b); if (!D) b.layoutSizingHorizontal = 'FILL';
      await T('ફક્ત ધામની સત્તાવાર જાહેરાતો', 'Text/Caption', 'text/muted', { parent: ac, align: 'CENTER' });
      items.push(c); }
    const set = figma.combineAsVariants(items, h); set.name = 'WhatsApp band'; finishSet(set, 'VERTICAL', 'surface/alt'); set.description = 'Same white card on every page (the festival page used a maroon card). Phone: compact (28 / 20 px padding, 56 px glyph), no QR code (you cannot scan your own screen), full-width button; section padding 48 px. Measured on phone: 723 → 566 px including the section.'; created.push(set.id); }
  // Devotional band
  { const h = await holder(B, 'Devotional band'); const items = [];
    for (const dev of ['Desktop', 'Phone']) { const D = dev === 'Desktop', W = D ? 1440 : 390;
      const c = comp('Device=' + dev, 'VERTICAL', { w: W, pad: D ? [104, 16, 0, 16] : [64, 16, 0, 16], gap: D ? 22 : 16, fill: 'surface/inverse', counter: 'CENTER' }); c.clipsContent = true; h.appendChild(c);
      const ch = chakra.createInstance(); const cs = D ? 720 : 420; ch.resize(cs, cs); ch.opacity = 0.12; abs(ch, c, (W - cs) / 2, D ? 40 : 30);
      await T('॥ ૐ ॥', 'Text/Eyebrow', 'text/on-dark-accent', { parent: c, align: 'CENTER' });
      await T('જય શ્રી વિહત મેલડી માઁ', (D ? 'Desktop' : 'Phone') + '/Display L', 'text/on-dark', { parent: c, align: 'CENTER' });
      const sh = TD('યા દેવી સર્વભૂતેષુ શક્તિરૂપેણ સંસ્થિતા ।\nનમસ્તસ્યૈ નમસ્તસ્યૈ નમસ્તસ્યૈ નમો નમઃ ॥', 'Noto Serif Gujarati', 'Medium', D ? 22 : 16, 'text/on-dark-accent', c, 'Shloka', 160); sh.textAlignHorizontal = 'CENTER';
      const vr = AL('HORIZONTAL', { name: 'Values', gap: D ? 20 : 16, parent: c, counter: 'CENTER' }); if (!D) { vr.layoutWrap = 'WRAP'; vr.counterAxisSpacing = 6; vr.primaryAxisAlignItems = 'CENTER'; vr.resize(358, 30); vr.primaryAxisSizingMode = 'FIXED'; vr.counterAxisSizingMode = 'AUTO'; }
      const VALS = ['આસ્થા', 'પરંપરા', 'સેવા', 'સંસ્કૃતિ', 'પ્રાણ પ્રતિષ્ઠા'];
      for (const [i, v] of VALS.entries()) { if (D && i) { const d = figma.createNodeFromSvg(DIAM); d.name = 'Diamond'; d.resize(6, 6); recolor(d, 'border/ornament'); vr.appendChild(d); } TD(v, 'Hind Vadodara', 'SemiBold', 17, 'text/on-dark-accent', vr, v, 140); }
      const art = AL('HORIZONTAL', { name: 'Deity pair', gap: D ? 24 : 14, parent: c, counter: 'MAX' }); art.paddingTop = D ? 24 : 16; slot(D ? 150 : 90, D ? 190 : 112, '01_deity_vihat-maa_cutout', art, 0, 'FIT'); slot(D ? 150 : 90, D ? 190 : 112, '02_deity_meldi-maa_cutout', art, 0, 'FIT');
      items.push(c); }
    const set = figma.combineAsVariants(items, h); set.name = 'Devotional band'; finishSet(set, 'VERTICAL', 'surface/page'); set.description = 'Burgundy, chakra centred behind at 12 %. Phone: 64 px top padding, 16 px shloka, values separated by space only so no line starts with a dot (488 → 407 px).'; created.push(set.id); }
  // Footer
  { const h = await holder(B, 'Footer — desktop and compact phone'); const items = [];
    const col = async (parent, title, list, accentFirst) => { const c = AL('VERTICAL', { name: title, gap: 10, parent }); await T(title, 'Text/Eyebrow', 'text/on-dark-accent', { parent: c, name: 'Heading (h2, styled small)' }); for (const [i, s] of list.entries()) await T(s, 'Text/Small', accentFirst && i === 0 ? 'text/on-dark' : 'text/on-dark-muted', { parent: c }); return c; };
    for (const dev of ['Desktop', 'Phone']) { const D = dev === 'Desktop';
      const c = comp('Device=' + dev, 'VERTICAL', { w: D ? 1440 : 390, pad: D ? [64, 124, 24, 124] : [48, 16, 24, 16], gap: D ? 40 : 28, fill: 'surface/footer' }); h.appendChild(c);
      const brand = async (parent) => { const b = AL('VERTICAL', { name: 'Brand', gap: 14, parent }); slot(D ? 260 : 220, D ? 73 : 62, '18_logo_lockup-ivory_footer', b, 0, 'FIT'); await T('॥ ભગવાન શ્રી કરમશીબાપાના આશીર્વાદથી ॥', 'Text/Small', 'text/on-dark-muted', { parent: b }); const so = AL('HORIZONTAL', { name: 'Social', gap: 12, parent: b }); for (const n of ['instagram', 'whatsapp']) { const s = AL('HORIZONTAL', { name: n, radius: 999, stroke: 'text/on-dark', sop: 0.35, parent: so, counter: 'CENTER' }); s.primaryAxisAlignItems = 'CENTER'; s.resize(44, 44); s.primaryAxisSizingMode = 'FIXED'; s.counterAxisSizingMode = 'FIXED'; icon(n, 'text/on-dark-accent', 20, s); } const w = setLabel(WA.defaultVariant.createInstance(), 'WhatsApp ચેનલમાં જોડાઓ'); b.appendChild(w); return b; };
      if (D) { const top = AL('HORIZONTAL', { name: 'Top', gap: 64, parent: c, fillW: true }); const b = await brand(top); b.layoutSizingHorizontal = 'FILL'; for (const [t, l] of [['પૃષ્ઠો', PAGES], ['મહોત્સવ', FEST], ['સંપર્ક', CONTACT]]) { const k = await col(top, t, l, t === 'સંપર્ક'); k.resize(200, 10); k.layoutSizingHorizontal = 'FIXED'; k.layoutSizingVertical = 'HUG'; } }
      else { await col(c, 'સંપર્ક', CONTACT, true); await brand(c); const two = AL('HORIZONTAL', { name: 'Links (two columns)', gap: 20, parent: c, fillW: true }); for (const [t, l] of [['પૃષ્ઠો', PAGES], ['મહોત્સવ', FEST]]) { const k = await col(two, t, l, false); k.layoutSizingHorizontal = 'FILL'; } }
      rule(c, 'border/ornament', 0.25);
      const bt = AL(D ? 'HORIZONTAL' : 'VERTICAL', { name: 'Bottom', gap: 6, parent: c, fillW: true }); if (D) bt.primaryAxisAlignItems = 'SPACE_BETWEEN'; await T('© ૨૦૨૬ શ્રી વિહત મેલડી ધામ, સાણંદ. સર્વ હક્ક સ્વાધીન.', 'Text/Caption', 'text/on-dark-muted', { parent: bt }); await T('॥ જય શ્રી વિહત મેલડી માઁ ॥', 'Text/Caption', 'text/on-dark-accent', { parent: bt });
      items.push(c); }
    const set = figma.combineAsVariants(items, h); set.name = 'Footer'; finishSet(set, 'VERTICAL', 'surface/page'); set.description = 'Desktop unchanged. Phone: contact first, then brand, then pages and festival links in two columns (about 1,000 px instead of 1,300). Column headings are level-2 headings styled small.'; created.push(set.id); }
  // Rule card
  { const h = await holder(B, 'Page-ending rule — approved'); const r = AL('VERTICAL', { name: 'Rule', gap: 8, pad: 32, radius: 16, fill: 'surface/raised', stroke: 'border/default', parent: h, fillW: true });
    for (const s of ['Content pages — Home, Darshan, New Temple, Festival, Gallery, History, Contact: WhatsApp band (seva enquiries and contact action) → devotional band (Gujarati devotional closing) → footer (navigation, contact details, essential links).', 'Seva registration form: footer only, so nothing distracts from the form.', '404: footer only, with a clear route back to the home page (the banner’s “મુખ્ય પૃષ્ઠ પર જાઓ” button and the four link cards).', 'Today the WhatsApp band is missing on New Temple and History, and the devotional band on Darshan and Contact; Gate C adds them.', 'On phone the bands stay proportionate: WhatsApp section 723 → 566 px, devotional band 488 → 407 px.']) await T('• ' + s, 'Text/Body', 'text/primary', { parent: r, fill: true }); }
  await notes(B, ['WhatsApp band: one white card everywhere (the festival page used a maroon card); compact on phone (723 → 566 px with its section).', 'Devotional band on phone: the values line no longer starts with “•”; 488 → 407 px.', 'Phone footer about 1,300 → 1,000 px: contact first, links in two columns; footer headings re-levelled (the outline skipped from h2 to h4).', 'Page endings follow one rule (approved 10 Oct 2026).']);
  shots.push(B);
}
for (const b of shots) await b.screenshot({ scale: 0.4 });
return { created, boards: shots.map(b => ({ id: b.id, name: b.name, size: [Math.round(b.width), Math.round(b.height)] })) };
