const page = await figma.getNodeByIdAsync('5:3'); await figma.setCurrentPageAsync(page);
const vars = await figma.variables.getLocalVariablesAsync(); const V = {}; for (const v of vars) V[v.name] = v;
const styles = await figma.getLocalTextStylesAsync(); const TS = {}; for (const s of styles) TS[s.name] = s;
const ES = {}; for (const s of await figma.getLocalEffectStylesAsync()) ES[s.name] = s;
const FONTS = [['Noto Serif Gujarati', 'SemiBold'], ['Noto Serif Gujarati', 'Medium'], ['Hind Vadodara', 'Regular'], ['Hind Vadodara', 'Medium'], ['Hind Vadodara', 'SemiBold'], ['Noto Sans Gujarati', 'Regular'], ['Noto Sans Gujarati', 'Medium'], ['Noto Sans Gujarati', 'SemiBold']];
await Promise.all(FONTS.map(([family, style]) => figma.loadFontAsync({ family, style })));
const paint = (n, op) => figma.variables.setBoundVariableForPaint({ type: 'SOLID', color: { r: 0, g: 0, b: 0 }, opacity: op === undefined ? 1 : op }, 'color', V[n]);
const DIG = /[૦-૯]+/g;
const fixDigits = (t) => { const segs = t.getStyledTextSegments(['fontName']); for (const sg of segs) { if (sg.fontName.family !== 'Hind Vadodara') continue; const sub = t.characters.slice(sg.start, sg.end); DIG.lastIndex = 0; let m; while ((m = DIG.exec(sub))) t.setRangeFontName(sg.start + m.index, sg.start + m.index + m[0].length, { family: 'Noto Sans Gujarati', style: sg.fontName.style }); } };
const T = async (str, style, color, o = {}) => { const t = figma.createText(); t.fontName = { family: 'Hind Vadodara', style: 'Regular' }; t.characters = str; await t.setTextStyleIdAsync(TS[style].id); t.fills = [paint(color)]; if (o.align) t.textAlignHorizontal = o.align; fixDigits(t); if (o.name) t.name = o.name; if (o.parent) { o.parent.appendChild(t); if (o.fill) { t.textAutoResize = 'HEIGHT'; t.layoutSizingHorizontal = 'FILL'; } } return t; };
const TD = (str, fam, sty, size, color, parent, name, lh) => { const t = figma.createText(); t.fontName = { family: fam, style: sty }; t.characters = str; t.fontSize = size; t.lineHeight = { unit: 'PERCENT', value: lh || 120 }; t.fills = [paint(color)]; if (name) t.name = name; if (parent) parent.appendChild(t); fixDigits(t); return t; };
const AL = (dir, o = {}) => { const f = figma.createAutoLayout(dir, { name: o.name || 'Frame', itemSpacing: o.gap === undefined ? 0 : o.gap }); if (o.pad !== undefined) { const p = Array.isArray(o.pad) ? o.pad : [o.pad, o.pad, o.pad, o.pad]; f.paddingTop = p[0]; f.paddingRight = p[1]; f.paddingBottom = p[2]; f.paddingLeft = p[3]; } f.fills = o.fill ? [paint(o.fill, o.op)] : []; if (o.radius !== undefined) f.cornerRadius = o.radius; if (o.stroke) { f.strokes = [paint(o.stroke, o.sop)]; f.strokeWeight = o.sw || 1; f.strokeAlign = 'INSIDE'; } if (o.parent) { o.parent.appendChild(f); if (o.fillW) f.layoutSizingHorizontal = 'FILL'; } if (o.w) { f.resize(o.w, 10); f.layoutSizingHorizontal = 'FIXED'; f.layoutSizingVertical = 'HUG'; } if (o.counter) f.counterAxisAlignItems = o.counter; return f; };
const board = (name, x, y, w) => { const b = AL('VERTICAL', { name, gap: 40, pad: 64, fill: 'surface/page' }); b.resize(w || 1600, 100); b.layoutSizingHorizontal = 'FIXED'; b.layoutSizingVertical = 'HUG'; b.x = x; b.y = y; return b; };
const head = async (b, grp, title, intro) => { const h = AL('VERTICAL', { name: 'Heading', gap: 10, parent: b, fillW: true }); await T('COMPONENTS · ' + grp, 'Text/Eyebrow', 'text/eyebrow', { parent: h }); await T(title, 'Desktop/Heading XL', 'text/heading', { parent: h }); if (intro) await T(intro, 'Text/Body', 'text/muted', { parent: h, fill: true }); };
const recolor = (node, colorVar) => { for (const v of node.findAll(n => n.type === 'VECTOR' || n.type === 'ELLIPSE' || n.type === 'RECTANGLE' || n.type === 'BOOLEAN_OPERATION')) { if (v.strokes && v.strokes.length) v.strokes = [paint(colorVar)]; if (v.fills && v.fills.length) v.fills = [paint(colorVar)]; } };
const IC = {}; for (const c of page.findAllWithCriteria({ types: ['COMPONENT'] })) if (c.name.startsWith('Icon/')) IC[c.name.slice(5)] = c;
const icon = (n, color, size, parent) => { const i = IC[n].createInstance(); i.resize(size, size); recolor(i, color); if (parent) parent.appendChild(i); return i; };
const slot = (w, h, file, parent, radius, fit) => { const f = figma.createFrame(); f.name = 'Image slot · ' + file + (fit ? ' · ' + fit : ''); f.resize(w, h); f.fills = [paint('surface/alt', 0.35)]; f.strokes = [paint('border/strong', 0.6)]; f.strokeWeight = 1; f.dashPattern = [3, 3]; f.cornerRadius = radius || 0; f.clipsContent = true; if (parent) parent.appendChild(f); return f; };
const notes = async (b, items) => { const n = AL('VERTICAL', { name: 'Current → proposed', gap: 8, pad: 32, fill: 'surface/alt', radius: 16, parent: b, fillW: true }); await T('Current → proposed', 'Text/Label', 'text/eyebrow', { parent: n }); for (const s of items) await T('• ' + s, 'Text/Small', 'text/primary', { parent: n, fill: true }); return n; };
const finishSet = (set, dir, bg, wrap) => { set.layoutMode = dir; if (wrap) set.layoutWrap = 'WRAP'; set.itemSpacing = 24; set.counterAxisSpacing = 24; set.paddingLeft = set.paddingRight = set.paddingTop = set.paddingBottom = 32; set.fills = [paint(bg)]; set.cornerRadius = 16; if (wrap) { set.layoutSizingHorizontal = 'FILL'; set.counterAxisSizingMode = 'AUTO'; } else { set.primaryAxisSizingMode = 'AUTO'; set.counterAxisSizingMode = 'AUTO'; } };
const holder = async (b, title) => { const h = AL('VERTICAL', { name: title + ' holder', gap: 12, parent: b, fillW: true }); await T(title, 'Desktop/Heading M', 'text/heading', { parent: h }); return h; };
const comp = (name, dir, o = {}) => { const c = figma.createComponent(); c.name = name; c.layoutMode = dir; c.itemSpacing = o.gap || 0; const p = o.pad === undefined ? [0, 0, 0, 0] : (Array.isArray(o.pad) ? o.pad : [o.pad, o.pad, o.pad, o.pad]); c.paddingTop = p[0]; c.paddingRight = p[1]; c.paddingBottom = p[2]; c.paddingLeft = p[3]; c.fills = o.fill ? [paint(o.fill, o.op)] : []; if (o.radius !== undefined) c.cornerRadius = o.radius; if (o.stroke) { c.strokes = [paint(o.stroke, o.sop)]; c.strokeWeight = o.sw || 1; c.strokeAlign = 'INSIDE'; } if (o.w) { c.resize(o.w, o.h || 10); c.primaryAxisSizingMode = dir === 'VERTICAL' ? (o.h ? 'FIXED' : 'AUTO') : 'FIXED'; c.counterAxisSizingMode = dir === 'VERTICAL' ? 'FIXED' : (o.h ? 'FIXED' : 'AUTO'); } else { c.primaryAxisSizingMode = 'AUTO'; c.counterAxisSizingMode = 'AUTO'; } if (o.counter) c.counterAxisAlignItems = o.counter; if (o.primary) c.primaryAxisAlignItems = o.primary; return c; };
const existing = (name) => page.children.find(n => n.name === name);
const chakra = await figma.getNodeByIdAsync('9:409');
const created = [];
// ---- Correction to an EXISTING component (C3 phone strip). Run only after call 1 reported the long text AND the correction was reviewed and approved. ----
{ const STRIP = await figma.getNodeByIdAsync('14:52'); const ph = STRIP.children.find(c => c.name === 'Device=Phone'); const msg = ph && ph.findOne(n => n.type === 'TEXT' && n.name === 'Message'); const SHORT = 'પ્રાણ પ્રતિષ્ઠા મહોત્સવ · ૨–૮ ફેબ્રુ.';
  if (msg && msg.characters !== SHORT) try { const segs = msg.getStyledTextSegments(['fontName']); await Promise.all(segs.map(sg => figma.loadFontAsync(sg.fontName))); msg.componentPropertyReferences = {}; msg.characters = SHORT; await msg.setTextStyleIdAsync(TS['Text/Label'].id); fixDigits(msg); created.push('stripFixed:' + msg.id); await ph.screenshot({ scale: 1 }); } catch (e) { created.push('stripFixFailed:' + String(e).slice(0, 80)); } }
// ===== Call 2: C6 · Cards, C7 · Festival (idempotent) =====
const hexc = h => ({ r: parseInt(h.slice(1, 3), 16) / 255, g: parseInt(h.slice(3, 5), 16) / 255, b: parseInt(h.slice(5, 7), 16) / 255 });
const ring = (dark) => [{ type: 'DROP_SHADOW', color: Object.assign(hexc(dark ? '#F2C66D' : '#B25E12'), { a: 1 }), offset: { x: 0, y: 0 }, radius: 0, spread: 5, visible: true, blendMode: 'NORMAL', showShadowBehindNode: false }, { type: 'DROP_SHADOW', color: Object.assign(hexc(dark ? '#481022' : '#FBF7EF'), { a: 1 }), offset: { x: 0, y: 0 }, radius: 0, spread: 3, visible: true, blendMode: 'NORMAL', showShadowBehindNode: false }];
const abs = (node, parent, x, y) => { parent.appendChild(node); node.layoutPositioning = 'ABSOLUTE'; node.x = x; node.y = y; return node; };
const rule = (parent, color, op) => { const r = figma.createRectangle(); r.name = 'Rule'; r.resize(100, 1); r.fills = [paint(color, op)]; parent.appendChild(r); r.layoutSizingHorizontal = 'FILL'; return r; };
const svg = (s, color, size, parent, name) => { const n = figma.createNodeFromSvg(s); n.name = name || 'Ornament'; n.resize(size, size); recolor(n, color); if (parent) parent.appendChild(n); return n; };
const LOTUS = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#B78A35" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5c2.2 2.6 2.2 6.4 0 9-2.2-2.6-2.2-6.4 0-9z"/><path d="M12 14c-2.6-2.4-5.6-3-8-2 1.2 3 4.6 4.2 8 2z"/><path d="M12 14c2.6-2.4 5.6-3 8-2-1.2 3-4.6 4.2-8 2z"/><path d="M6 18h12"/></svg>';
const DIAM = '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 10 10"><path d="M5 0L10 5L5 10L0 5Z" fill="#E2C27A"/></svg>';
const metaRow = async (parent, ic, txt, dark) => { const r = AL('HORIZONTAL', { name: 'Meta · ' + ic, gap: 10, parent, counter: 'CENTER', fillW: true }); icon(ic, dark ? 'text/on-dark-accent' : 'text/eyebrow', 18, r); await T(txt, 'Text/Small', dark ? 'text/on-dark-muted' : 'text/muted', { parent: r, fill: true }); return r; };
const shots = [];

// ---------------- C6 ----------------
if (!existing('C6 · Cards')) {
  const B = board('C6 · Cards', 8700, 0, 1600);
  await head(B, '6', 'Cards', 'One card family: the same edges, padding and type on every card. Programme, news, contact and link cards.');
  const EV = { Light: ['૨–૭', 'ફેબ્રુઆરી ૨૦૨૭', 'ભાગવત સપ્તાહ', 'પોથી યાત્રાથી સુદામા ચરિત્ર સુધી — શ્રી કૃષ્ણ જન્મોત્સવ, શ્રી રામ પ્રાગટ્ય, શ્રી ગોવર્ધન પૂજા અને રુક્મિણી વિવાહ સહિત આઠ પાવન પ્રસંગોનું રસપાન.', ['clock', 'સમય: દિવસવાર કાર્યક્રમ મુજબ'], ['map-pin', 'મંદિર પરિસર, સાણંદ']], Feature: ['૮', 'ફેબ્રુઆરી · સોમવાર', 'મૂર્તિ પ્રાણ પ્રતિષ્ઠા', 'કળશ પૂજા, શ્રી યંત્ર પૂજા, ધર્મ ધજા પૂજા, માતાજીનો પ્રથમ શણગાર અને પ્રથમ આરતી — કુલ ૧૭ પ્રકારની પૂજા સાથે માઁની પ્રતિષ્ઠા.', ['clock', 'શુભ મુહૂર્ત · બપોરે ૧૨:૩૯'], ['map-pin', 'નવું મંદિર, સાણંદ']] };
  // Event card: Tone × Layout
  { const h = await holder(B, 'Event card'); const items = [];
    for (const layout of ['Stacked', 'Wide']) for (const tone of ['Light', 'Feature']) {
      const dark = tone === 'Feature', [num, mon, title, desc, m1, m2] = EV[tone], wide = layout === 'Wide';
      const c = comp(`Tone=${tone}, Layout=${layout}`, wide ? 'HORIZONTAL' : 'VERTICAL', { w: wide ? 754 : 371, pad: wide ? [36, 40, 36, 40] : [40, 32, 32, 32], gap: wide ? 40 : 16, radius: 12, fill: dark ? 'surface/feature' : 'surface/raised', stroke: dark ? undefined : 'border/default' }); h.appendChild(c);
      const left = wide ? AL('VERTICAL', { name: 'Head', gap: 16, parent: c }) : c; if (wide) left.layoutSizingHorizontal = 'FILL';
      const top = AL('HORIZONTAL', { name: 'Date row', parent: left, fillW: true, counter: 'CENTER' }); top.primaryAxisAlignItems = 'SPACE_BETWEEN';
      const dg = AL('HORIZONTAL', { name: 'Date', gap: 8, parent: top, counter: 'MAX' }); TD(num, 'Noto Serif Gujarati', 'SemiBold', 40, dark ? 'text/on-dark' : 'text/heading', dg, 'Days', 110); TD(mon, 'Noto Serif Gujarati', 'SemiBold', 17, dark ? 'text/on-dark-accent' : 'text/eyebrow', dg, 'Month', 140);
      svg(LOTUS, dark ? 'text/on-dark-accent' : 'border/ornament', 30, top, 'Lotus');
      await T(title, 'Desktop/Heading M', dark ? 'text/on-dark' : 'text/heading', { parent: left, name: 'Title', fill: true });
      const right = wide ? AL('VERTICAL', { name: 'Detail', gap: 16, parent: c }) : c; if (wide) right.layoutSizingHorizontal = 'FILL';
      await T(desc, 'Text/Small', dark ? 'text/on-dark-muted' : 'text/muted', { parent: right, name: 'Description', fill: true });
      rule(right, dark ? 'text/on-dark' : 'border/default', dark ? 0.2 : 1);
      await metaRow(right, m1[0], m1[1], dark); await metaRow(right, m2[0], m2[1], dark);
      items.push(c);
    }
    const set = figma.combineAsVariants(items, h); set.name = 'Event card'; finishSet(set, 'HORIZONTAL', 'surface/alt', true); set.counterAxisAlignItems = 'MIN';
    set.description = 'Stacked: three across at 1440 / 1180. Wide: at 834 / 844 the main event (Feature) comes first, full width, in two columns; the other two follow side by side. Phone: stacked. Radius 12; padding 40 / 32 (phone 24).'; created.push(set.id); }

  // News card: Media
  { const h = await holder(B, 'News card'); const items = [];
    const soon = page.findOne(n => n.type === 'COMPONENT_SET' && n.name === 'Photo coming soon');
    for (const media of ['Photo', 'Coming soon', 'Text only']) {
      const c = comp('Media=' + media, 'VERTICAL', { w: 371, radius: 12, fill: 'surface/raised', stroke: 'border/default' }); c.clipsContent = true; h.appendChild(c);
      if (media !== 'Text only') {
        const m = AL('VERTICAL', { name: 'Media', parent: c, fillW: true }); m.resize(371, 232); m.layoutSizingVertical = 'FIXED'; m.clipsContent = true;
        if (media === 'Photo' || !soon) { const s = slot(371, 232, media === 'Photo' ? 'news photo (from the trust)' : 'coming soon', m, 0, 'FILL'); s.strokes = []; s.layoutSizingHorizontal = 'FILL'; }
        else { const i = soon.children.find(v => v.name === 'Ratio=Wide').createInstance(); m.appendChild(i); i.resize(371, 232); i.layoutSizingHorizontal = 'FILL'; i.cornerRadius = 0; }
        const tag = AL('HORIZONTAL', { name: 'Tag', pad: [3, 12, 3, 12], radius: 999, fill: 'surface/page' }); await T('નિર્માણ કાર્ય', 'Text/Caption', 'text/heading', { parent: tag }); abs(tag, m, 12, 12);
      }
      const body = AL('VERTICAL', { name: 'Body', gap: 8, pad: 24, parent: c, fillW: true });
      const meta = AL('HORIZONTAL', { name: 'Meta', parent: body, fillW: true, counter: 'CENTER' }); meta.primaryAxisAlignItems = 'SPACE_BETWEEN';
      await T(media === 'Text only' ? '[જાહેરાતની તારીખ]' : '[તારીખ]', 'Text/Caption', 'text/muted', { parent: meta, name: 'Date' });
      if (media === 'Text only') { const nw = AL('HORIZONTAL', { name: 'New', gap: 6, parent: meta, counter: 'CENTER' }); const d = figma.createEllipse(); d.resize(8, 8); d.fills = [paint('text/accent-flag')]; nw.appendChild(d); await T('નવું', 'Text/Caption', 'text/accent-flag', { parent: nw }); }
      await T(media === 'Text only' ? 'મૂર્તિ પ્રાણ પ્રતિષ્ઠા મહોત્સવ — તા. ૨ થી ૮ ફેબ્રુઆરી, ૨૦૨૭' : '[નિર્માણ કાર્ય પ્રગતિ — શીર્ષક]', 'Desktop/Heading M', 'text/heading', { parent: body, name: 'Title', fill: true });
      await T(media === 'Text only' ? 'ભાગવત સપ્તાહ (૨–૭ ફેબ્રુઆરી) અને નવચંડી મહા યજ્ઞ (૪–૮ ફેબ્રુઆરી). ૮ ફેબ્રુઆરી, સોમવારે બપોરે ૧૨:૩૯ વાગ્યે મૂર્તિ પ્રાણ પ્રતિષ્ઠા. યજ્ઞ નોંધણી માટે પૂછપરછ: 99095 52020.' : '[એક વાક્યમાં સારાંશ]', 'Text/Small', 'text/muted', { parent: body, name: 'Summary', fill: true });
      const lk = AL('HORIZONTAL', { name: 'Link', gap: 8, parent: body, counter: 'CENTER' }); lk.paddingTop = 8; await T('સંપૂર્ણ જાહેરાત', 'Text/Label', 'text/link', { parent: lk }); icon('arrow-right', 'text/link', 16, lk);
      items.push(c);
    }
    const set = figma.combineAsVariants(items, h); set.name = 'News card'; finishSet(set, 'HORIZONTAL', 'surface/alt'); set.counterAxisAlignItems = 'MIN';
    set.description = 'One white card for every news item: media (photo or the “coming soon” tile) → tag → date → title → one-line summary → link. Text only: announcements, and the compact list on phone.'; created.push(set.id); }

  // Contact rows
  { const h = await holder(B, 'Contact rows'); const c = comp('Contact rows', 'VERTICAL', { w: 470, radius: 12, fill: 'surface/raised', stroke: 'border/default' }); h.appendChild(c);
    const ROWS = [['map-pin', 'સરનામું', 'ગેપ્પરા, સાણંદ', 'ગુજરાત ૩૮૨૧૧૦', null], ['phone', 'ફોન', '99095 52020', null, 'WhatsApp સંદેશ'], ['car', 'પાર્કિંગ', 'ઉપલબ્ધ · નિઃશુલ્ક', null, null], ['clock', 'દર્શન સમય', 'સવારે ૬ – રાત્રે ૧૦', 'દરરોજ · આરતી સવારે ૭ અને સાંજે ૭', 'દર્શન અને યાત્રાની વિગત']];
    for (const [i, [ic, lab, val, note, link]] of ROWS.entries()) {
      const r = AL('HORIZONTAL', { name: 'Row · ' + lab, gap: 16, pad: [20, 24, 20, 24], parent: c, fillW: true, counter: 'CENTER' }); if (i) { r.strokes = [paint('border/default')]; r.strokeTopWeight = 1; r.strokeBottomWeight = 0; r.strokeLeftWeight = 0; r.strokeRightWeight = 0; }
      const ci = AL('HORIZONTAL', { name: 'Icon', radius: 999, fill: 'surface/alt', parent: r, counter: 'CENTER' }); ci.primaryAxisAlignItems = 'CENTER'; ci.resize(48, 48); ci.primaryAxisSizingMode = 'FIXED'; ci.counterAxisSizingMode = 'FIXED'; icon(ic, 'text/heading', 22, ci);
      const tx = AL('VERTICAL', { name: 'Text', gap: 2, parent: r }); tx.layoutSizingHorizontal = 'FILL';
      await T(lab, 'Text/Caption', 'text/eyebrow', { parent: tx }); TD(val, 'Hind Vadodara', 'SemiBold', 19, 'text/primary', tx, 'Value', 150); if (note) await T(note, 'Text/Small', 'text/muted', { parent: tx, fill: true }); if (link) { const l = await T(link, 'Text/Small', 'text/link', { parent: tx }); l.textDecoration = 'UNDERLINE'; }
    }
    c.description = 'Contact page: one card of four rows instead of a 2 × 2 grid. Wording unchanged.'; created.push(c.id); }

  // Link card: State
  { const h = await holder(B, 'Link card (404, related pages)'); const items = [];
    for (const st of ['Default', 'Hover', 'Focus']) {
      const c = comp('State=' + st, 'HORIZONTAL', { w: 371, pad: [20, 24, 20, 24], gap: 16, radius: 12, fill: 'surface/raised', stroke: st === 'Hover' ? 'action/primary' : 'border/default', counter: 'CENTER' }); h.appendChild(c); if (st === 'Focus') c.effects = ring(false);
      const tx = AL('VERTICAL', { name: 'Text', gap: 4, parent: c }); tx.layoutSizingHorizontal = 'FILL';
      TD('મૂર્તિ પ્રાણ પ્રતિષ્ઠા મહોત્સવ', 'Hind Vadodara', 'SemiBold', 18, 'text/heading', tx, 'Title', 140); await T('તા. ૨ થી ૮ ફેબ્રુઆરી, ૨૦૨૭ — દિવસવાર કાર્યક્રમ અને રાત્રિ કાર્યક્રમ', 'Text/Small', 'text/muted', { parent: tx, fill: true, name: 'Description' });
      icon('arrow-right', 'text/link', 20, c); items.push(c);
    }
    const set = figma.combineAsVariants(items, h); set.name = 'Link card'; finishSet(set, 'HORIZONTAL', 'surface/page'); set.description = 'Title, one-line description, arrow. Hover: maroon border. Focus: 2 px focus ring.'; created.push(set.id); }
  await notes(B, ['Event cards: at 834 / 844 the row broke 2 + 1 and left the main event alone; the Wide layout puts it first, full width (section 844 → 744 px tall).', 'News: the first card was a white card while the others were a dashed box with floating text; now one card structure with the same padding.', 'Contact: the 2 × 2 grid squeezed the text (“૭” alone on a line, wrapped link, half-empty parking card); now one card of rows.', 'Link card unchanged.']);
  shots.push(B);
}

// ---------------- C7 ----------------
if (!existing('C7 · Festival')) {
  const B = board('C7 · Festival', 10400, 0, 1600);
  await head(B, '7', 'Festival components', 'Building blocks of the detailed programme on the festival page (approved to stay complete). Gujarati digits follow the numeral rule.');
  // Countdown block: State × Device
  { const h = await holder(B, 'Countdown'); const items = [];
    for (const st of ['Counting', 'Done']) for (const dev of ['Desktop', 'Phone']) {
      const D = dev === 'Desktop';
      const c = comp(`State=${st}, Device=${dev}`, 'VERTICAL', { w: D ? 928 : 358, pad: D ? [20, 32, 28, 32] : [16, 12, 20, 12], gap: 16, radius: 16, fill: 'surface/inverse', stroke: 'text/on-dark-accent', sop: 0.3 }); h.appendChild(c);
      const top = AL(D ? 'HORIZONTAL' : 'VERTICAL', { name: 'Top', gap: 6, parent: c, fillW: true }); if (D) { top.primaryAxisAlignItems = 'SPACE_BETWEEN'; top.counterAxisAlignItems = 'CENTER'; }
      const tg = AL('HORIZONTAL', { name: 'Tag', gap: 8, parent: top, counter: 'CENTER' }); const d = figma.createEllipse(); d.resize(8, 8); d.fills = [paint('text/on-dark-accent')]; tg.appendChild(d); await T(st === 'Done' ? 'પાવન અવસર' : 'પ્રાણ પ્રતિષ્ઠાને બાકી સમય', 'Text/Label', 'text/on-dark-accent', { parent: tg });
      if (st === 'Counting') await T('શનિવાર, ૧૦ ઑક્ટોબર ૨૦૨૬ · રાત્રે ૨:૪૫', 'Text/Caption', 'text/on-dark-muted', { parent: top, name: 'Now (live)' });
      if (st === 'Counting') { const g = AL('HORIZONTAL', { name: 'Cells', parent: c, fillW: true, counter: 'CENTER' }); g.primaryAxisAlignItems = 'SPACE_BETWEEN';
        for (const [i, [n, u]] of [['૧૨૧', 'દિવસ'], ['૦૯', 'કલાક'], ['૫૩', 'મિનિટ']].entries()) { if (i) svg(DIAM, 'text/on-dark-accent', 8, g, 'Diamond'); const cell = AL('VERTICAL', { name: u, gap: 4, parent: g, counter: 'CENTER' }); cell.layoutSizingHorizontal = 'FILL'; TD(n, 'Noto Serif Gujarati', 'Medium', D ? 56 : 40, 'text/on-dark', cell, 'Value', 110).textAlignHorizontal = 'CENTER'; await T(u, 'Text/Caption', 'text/on-dark-accent', { parent: cell, align: 'CENTER' }); } }
      else { await T('મૂર્તિ પ્રાણ પ્રતિષ્ઠા સંપન્ન', (D ? 'Desktop' : 'Phone') + '/Heading L', 'text/on-dark', { parent: c, fill: true }); await T('તા. ૮ ફેબ્રુઆરી, ૨૦૨૭ના શુભ મુહૂર્તે નવા મંદિરમાં માઁ બિરાજમાન થયાં. આપ સહુ ભક્તોની હાજરી, સેવા અને સહયોગ બદલ હૃદયપૂર્વક આભાર.', 'Text/Body', 'text/on-dark-muted', { parent: c, fill: true }); await T('॥ જય શ્રી વિહત મેલડી માઁ ॥', 'Text/Eyebrow', 'text/on-dark-accent', { parent: c }); }
      items.push(c);
    }
    const set = figma.combineAsVariants(items, h); set.name = 'Countdown'; finishSet(set, 'HORIZONTAL', 'surface/page', true); set.counterAxisAlignItems = 'MIN';
    set.description = 'Days · hours · minutes (no seconds). Done after 12:39 on 8 Feb 2027. Refresh every 30–60 s (not every second).'; created.push(set.id); }
  // Countdown pill: State
  { const h = await holder(B, 'Countdown pill (hero)'); const items = [];
    for (const [st, txt] of [['Counting', 'પ્રાણ પ્રતિષ્ઠાને ૧૨૧ દિવસ બાકી'], ['Soon', 'આવતીકાલે બપોરે ૧૨:૩૯ વાગ્યે મૂર્તિ પ્રાણ પ્રતિષ્ઠા'], ['Done', 'મૂર્તિ પ્રાણ પ્રતિષ્ઠા સંપન્ન · જય શ્રી વિહત મેલડી માઁ']]) {
      const c = comp('State=' + st, 'HORIZONTAL', { pad: [8, 16, 8, 14], gap: 10, radius: 999, stroke: 'text/on-dark', sop: 0.3, counter: 'CENTER' }); h.appendChild(c); const d = figma.createEllipse(); d.resize(8, 8); d.fills = [paint('text/on-dark-accent')]; c.appendChild(d); await T(txt, 'Text/Small', 'text/on-dark', { parent: c }); items.push(c); }
    const set = figma.combineAsVariants(items, h); set.name = 'Countdown pill'; finishSet(set, 'HORIZONTAL', 'surface/inverse'); set.description = 'Counting → Soon on 7 Feb (“આવતીકાલે…”) and 8 Feb before 12:39 (“આજે…”) → Done.'; created.push(set.id); }
  // Day card: Type
  { const h = await holder(B, 'Festival day card'); const items = [];
    const DAY = { Regular: ['૨', 'ફેબ્રુઆરી', 'મંગળવાર', 'દિવસ ૧', 'મહોત્સવનો શુભારંભ', [['સવારે ૯ થી ૧૨', 'પોથી યાત્રા'], ['બપોરે ૧૨:૩૯', 'દીપ પ્રાગટ્ય'], ['બપોરે ૨ થી ૫', 'ભાગવત કથા — પ્રારંભ']], ['રાત્રે', 'ભવ્ય લોક ડાયરો', 'ગોપાલ સાધુ · ભૂમિ આહીર']], Main: ['૮', 'ફેબ્રુઆરી', 'સોમવાર', 'દિવસ ૭', 'મૂર્તિ પ્રાણ પ્રતિષ્ઠા', [['[સમય]', 'નવચંડી મહા યજ્ઞ — પૂર્ણાહુતિ']], ['રાત્રે ૯', 'માતાજીની રમેલ', 'કલાકારોનાં નામ ટૂંક સમયમાં']], Closing: ['૯', 'ફેબ્રુઆરી', 'મંગળવાર', 'સમાપન', 'મહોત્સવનું સમાપન', [['સવારે ૧૦', 'માતાજીના પ્યાલા']], null] };
    for (const type of ['Regular', 'Main', 'Closing']) {
      const dark = type === 'Main', [n, mon, wd, chip, title, rows, night] = DAY[type];
      const c = comp('Type=' + type, 'VERTICAL', { w: 283, pad: [22, 20, 20, 20], gap: 14, radius: 16, fill: dark ? 'surface/feature' : 'surface/raised', stroke: dark ? 'text/on-dark-accent' : 'border/default', sop: dark ? 0.4 : 1 }); h.appendChild(c);
      const hd = AL('HORIZONTAL', { name: 'Head', parent: c, fillW: true, counter: 'CENTER' }); hd.primaryAxisAlignItems = 'SPACE_BETWEEN';
      const dg = AL('HORIZONTAL', { name: 'Date', gap: 10, parent: hd, counter: 'CENTER' }); TD(n, 'Noto Serif Gujarati', 'SemiBold', 40, dark ? 'text/on-dark' : 'text/heading', dg, 'Day', 110); const ds = AL('VERTICAL', { name: 'Month', parent: dg }); await T(mon, 'Text/Caption', dark ? 'text/on-dark' : 'text/primary', { parent: ds }); await T(wd, 'Text/Caption', dark ? 'text/on-dark-muted' : 'text/muted', { parent: ds });
      const cp = AL('HORIZONTAL', { name: 'Day label', pad: [3, 10, 3, 10], radius: 999, fill: dark ? 'text/on-dark' : 'surface/alt', op: dark ? 0.12 : 1, parent: hd }); await T(chip, 'Text/Caption', dark ? 'text/on-dark' : 'text/heading', { parent: cp, name: 'Label' });
      rule(c, dark ? 'text/on-dark' : 'border/default', dark ? 0.2 : 1);
      await T(title, 'Desktop/Heading M', dark ? 'text/on-dark' : 'text/heading', { parent: c, name: 'Title', fill: true });
      if (dark) { const mu = AL('VERTICAL', { name: 'Muhurat', gap: 2, pad: [12, 16, 12, 16], radius: 12, stroke: 'text/on-dark-accent', sop: 0.4, parent: c, fillW: true }); await T('મૂર્તિ પ્રાણ પ્રતિષ્ઠા · શુભ મુહૂર્ત', 'Text/Caption', 'text/on-dark-accent', { parent: mu }); TD('બપોરે ૧૨:૩૯', 'Noto Serif Gujarati', 'SemiBold', 28, 'text/on-dark', mu, 'Time', 125);
        await T('શ્રી ગણેશ પૂજા, કળશ પૂજા, શ્રી યંત્ર પૂજા, ધર્મ ધજા પૂજા, ધ્વજસ્તંભ પૂજા, માતાજીનો પ્રથમ શણગાર અને પ્રથમ આરતી સહિત કુલ ૧૭ પ્રકારની પૂજા.', 'Text/Small', 'text/on-dark-muted', { parent: c, fill: true }); }
      for (const [tm, it] of rows) { const r = AL('HORIZONTAL', { name: 'Row', gap: 12, parent: c, fillW: true }); const a = await T(tm, 'Text/Caption', dark ? 'text/on-dark-accent' : 'text/eyebrow', { parent: r }); a.textAutoResize = 'HEIGHT'; a.resize(92, a.height); await T(it, 'Text/Small', dark ? 'text/on-dark' : 'text/primary', { parent: r, fill: true }); }
      if (night) { const nb = AL('VERTICAL', { name: 'Night', gap: 8, pad: [14, 16, 14, 16], radius: 12, fill: 'surface/footer', parent: c, fillW: true }); const nh = AL('HORIZONTAL', { name: 'Night head', gap: 8, parent: nb, counter: 'CENTER' }); icon('moon', 'text/on-dark-accent', 16, nh); const tp = AL('HORIZONTAL', { name: 'Time', pad: [1, 8, 1, 8], radius: 999, stroke: 'text/on-dark-accent', sop: 0.5, parent: nh }); await T(night[0], 'Text/Caption', 'text/on-dark-accent', { parent: tp }); await T(night[1], 'Text/Label', 'text/on-dark-accent', { parent: nh }); await T(night[2], 'Text/Small', 'text/on-dark', { parent: nb, fill: true }); }
      items.push(c);
    }
    const set = figma.combineAsVariants(items, h); set.name = 'Festival day card'; finishSet(set, 'HORIZONTAL', 'surface/alt'); set.counterAxisAlignItems = 'MIN';
    set.description = 'Regular · Main (8 Feb, maroon, muhurat callout) · Closing (9 Feb: “સમાપન”, never “દિવસ ૮”). Radius 16. Night block lists the confirmed artists only.'; created.push(set.id); }
  // Day tab: State + strip example
  { const h = await holder(B, 'Day tabs (phone) and muhurat marker'); const items = [];
    for (const st of ['Default', 'Selected', 'Main']) { const sel = st === 'Selected';
      const c = comp('State=' + st, 'VERTICAL', { w: 45, h: 56, gap: 1, fill: sel ? 'action/primary' : 'surface/raised', counter: 'CENTER', primary: 'CENTER' }); h.appendChild(c); if (st === 'Main') { c.strokes = [paint('border/ornament')]; c.strokeWeight = 1.5; c.strokeAlign = 'INSIDE'; }
      TD(st === 'Main' ? '૮' : '૨', 'Noto Serif Gujarati', 'SemiBold', 20, sel ? 'action/on-accent' : 'text/heading', c, 'Day', 110).textAlignHorizontal = 'CENTER'; await T(st === 'Main' ? 'સોમ' : 'મંગળ', 'Text/Caption', sel ? 'action/on-accent' : 'text/muted', { parent: c, name: 'Weekday', align: 'CENTER' }); items.push(c); }
    const set = figma.combineAsVariants(items, h); set.name = 'Day tab'; finishSet(set, 'HORIZONTAL', 'surface/page'); created.push(set.id);
    const strip = AL('HORIZONTAL', { name: 'Day tab strip · example (358 px)', radius: 12, stroke: 'border/default', parent: h }); strip.resize(358, 56); strip.primaryAxisSizingMode = 'FIXED'; strip.clipsContent = true;
    const DAYS = [['૨', 'મંગળ'], ['૩', 'બુધ'], ['૪', 'ગુરુ'], ['૫', 'શુક્ર'], ['૬', 'શનિ'], ['૭', 'રવિ'], ['૮', 'સોમ'], ['૯', 'મંગળ']];
    for (const [i, [dn, wd]] of DAYS.entries()) { const v = set.children.find(x => x.name === 'State=' + (i === 0 ? 'Selected' : i === 6 ? 'Main' : 'Default')); const inst = v.createInstance(); strip.appendChild(inst); inst.layoutSizingHorizontal = 'FILL'; const ts = inst.findAll(n => n.type === 'TEXT'); await Promise.all(ts.map(t => figma.loadFontAsync(t.fontName))); ts[0].characters = dn; ts[1].characters = wd; fixDigits(ts[1]); }
    const mk = []; for (const dev of ['Desktop', 'Phone']) { const c = comp('Device=' + dev, 'HORIZONTAL', { pad: [0, 14, 0, 12], gap: 8, radius: 999, fill: 'surface/inverse', stroke: 'border/ornament', counter: 'CENTER' }); c.strokeWeight = 1.5; c.resize(80, dev === 'Desktop' ? 44 : 36); c.primaryAxisSizingMode = 'AUTO'; c.counterAxisSizingMode = 'FIXED'; h.appendChild(c); svg(DIAM, 'text/on-dark-accent', 9, c, 'Diamond'); TD(dev === 'Desktop' ? 'બપોરે ૧૨:૩૯' : '૧૨:૩૯', 'Hind Vadodara', 'SemiBold', dev === 'Desktop' ? 16 : 14, 'text/on-dark-accent', c, 'Time'); mk.push(c); }
    const ms = figma.combineAsVariants(mk, h); ms.name = 'Muhurat marker'; finishSet(ms, 'HORIZONTAL', 'surface/page'); ms.counterAxisAlignItems = 'CENTER'; ms.description = 'Phone shows “◆ ૧૨:૩૯” — the time is never hidden.'; created.push(ms.id); }
  await notes(B, ['9 Feb card said “દિવસ ૮”, contradicting “સાત દિવસ” and the 2–8 Feb decision; it now says “સમાપન”.', 'Phone week chart showed only a dark dot for the muhurat; the marker now always shows “૧૨:૩૯”.', 'Phone day tabs were 41 px wide with 11 px labels; now one segmented strip of 8 tabs ≥ 44 px with 14 px weekdays.', 'Day card radius 18 → 16 (back on the radius scale). Countdown unchanged: days / hours / minutes, no seconds.']);
  shots.push(B);
}
for (const b of shots) await b.screenshot({ scale: 0.4 });
return { created, boards: shots.map(b => ({ id: b.id, name: b.name, size: [Math.round(b.width), Math.round(b.height)] })) };
