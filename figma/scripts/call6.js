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
// ===== Call 6: review screenshots of every component board + phone-width test at 320 / 360 / 390 / 430 (Components page) =====
// REPORT ONLY. Reads C1–C8; adds (or rebuilds) only its own board "QA · Phone widths" with instances.
// It never edits a component to make a test pass: failures are marked FAIL on the board and returned; any correction is proposed separately and applied only after review.
const names = ['C1 · Icons & ornament', 'C2 · Buttons, chips & fields', 'C3 · Navigation', 'C4 · Banners & headings', 'C5 · Images & frames', 'C6 · Cards', 'C7 · Festival', 'C8 · Page endings'];
const out = { boards: [], widths: [] };
for (const nm of names) {
  const b = page.children.find(n => n.name === nm); if (!b) { out.boards.push({ board: nm, missing: true }); continue; }
  const texts = b.findAllWithCriteria({ types: ['TEXT'] });
  const thin = texts.filter(t => t.width < 8 && t.characters.length > 2).map(t => t.id);
  const digitsInHind = texts.filter(t => /[૦-૯]/.test(t.characters) && t.getStyledTextSegments(['fontName']).some(sg => sg.fontName.family === 'Hind Vadodara' && /[૦-૯]/.test(t.characters.slice(sg.start, sg.end)))).map(t => t.id);
  out.boards.push({ board: nm, size: [Math.round(b.width), Math.round(b.height)], texts: texts.length, collapsedText: thin, digitsNotInNotoSans: digitsInHind });
  await b.screenshot({ scale: 0.3 });
}

// ---- Phone-width test: every phone variant as an instance at 4 widths ----
const old = page.children.find(n => n.name === 'QA · Phone widths'); if (old) old.remove(); // only ever this script's own output
let maxY = 0; for (const n of page.children) maxY = Math.max(maxY, n.y + n.height);
const QA = board('QA · Phone widths', 0, Math.ceil(maxY + 600), 2200); QA.layoutSizingHorizontal = 'HUG';
await head(QA, 'QA', 'Phone widths: 320 · 360 · 390 · 430', 'Every phone variant placed at four widths. Report only: the components above are never changed by this test. Failures are marked FAIL in red; corrections are proposed separately and applied only after review. This board can be deleted afterwards.');
const WIDTHS = [320, 360, 390, 430];
const roleOr = (n, rgb) => V[n] ? paint(n) : { type: 'SOLID', color: rgb };
const summary = { tested: 0, passed: 0, failed: 0 };
const IGNORE = /Glow|chakra|Chakra|Halo|halo/;
const targets = [];
for (const set of page.findAllWithCriteria({ types: ['COMPONENT_SET'] })) for (const v of set.children) if (/Device=Phone|Size=Phone/.test(v.name)) targets.push({ label: set.name + ' · ' + v.name.replace(/,?\s*Device=Phone|,?\s*Size=Phone/, '').replace(/^,\s*/, ''), comp: v });
for (const nm of ['Phone menu', 'Bottom action bar', 'Contact rows']) { const c = page.findOne(n => n.type === 'COMPONENT' && n.name === nm && n.parent.type !== 'COMPONENT_SET'); if (c) targets.push({ label: nm, comp: c }); }
const groups = [['Navigation', /^(Announcement strip|Header|Phone menu|Bottom action bar)/], ['Banners & headings', /^(Page banner|Section heading)/], ['Festival & cards', /^(Countdown|Contact rows|Event card|News card|Festival day card|Link card)/], ['Page endings', /^(WhatsApp band|Devotional band|Footer)/]];
for (const [gname, re] of groups) {
  const G = AL('VERTICAL', { name: 'Group · ' + gname, gap: 48, pad: 32, radius: 16, fill: 'surface/alt', parent: QA });
  await T(gname, 'Desktop/Heading L', 'text/heading', { parent: G });
  for (const t of targets.filter(t => re.test(t.label))) {
    const row = AL('VERTICAL', { name: 'Row · ' + t.label, gap: 12, parent: G });
    await T(t.label, 'Text/Label', 'text/muted', { parent: row });
    const line = AL('HORIZONTAL', { name: 'Widths', gap: 40, parent: row, counter: 'MIN' });
    for (const w of WIDTHS) {
      const cell = AL('VERTICAL', { name: w + ' px', gap: 8, parent: line }); await T(w + ' px', 'Text/Caption', 'text/muted', { parent: cell });
      const inst = t.comp.createInstance(); cell.appendChild(inst);
      const ww = w - Math.max(0, Math.round(390 - t.comp.width)); // components drawn for the 358 px content column keep their 16 px page margins
      try { inst.layoutSizingHorizontal = 'FIXED'; inst.resize(ww, inst.height); if (inst.layoutMode && inst.layoutMode !== 'NONE') inst.layoutSizingVertical = 'HUG'; } catch (e) { inst.resize(ww, inst.height); }
      // checks
      const box = inst.absoluteBoundingBox, issues = [];
      for (const d of inst.findAll(n => n.visible !== false && !IGNORE.test(n.name))) {
        const r = d.absoluteBoundingBox; if (!r) continue;
        if (r.x + r.width > box.x + box.width + 1 || r.x < box.x - 1) issues.push('past edge: ' + d.name + (d.type === 'TEXT' ? ' “' + d.characters.slice(0, 24) + '”' : ''));
        if (d.type === 'TEXT' && typeof d.fontSize === 'number') {
          let p = d.parent, inButton = false; for (let k = 0; k < 4 && p; k++, p = p.parent) if (p.type === 'INSTANCE' && /State=/.test(p.name)) { inButton = true; break; }
          if (inButton && d.height > d.fontSize * 1.9) issues.push('button label breaks: “' + d.characters + '”');
          if (/૨૦૨૭/.test(d.characters) && d.height > d.fontSize * 1.9 && d.textAutoResize !== 'WIDTH_AND_HEIGHT') issues.push('check year line: “' + d.characters.slice(0, 30) + '”');
        }
      }
      const uniq = [...new Set(issues)]; summary.tested++;
      const mark = figma.createText(); mark.fontName = { family: 'Hind Vadodara', style: 'SemiBold' }; mark.fontSize = 14; cell.appendChild(mark);
      if (uniq.length) {
        summary.failed++; out.widths.push({ component: t.label, screen: w, width: ww, height: Math.round(inst.height), status: 'FAIL', issues: uniq.slice(0, 8) });
        mark.characters = 'FAIL · ' + uniq.slice(0, 2).join(' · ') + (uniq.length > 2 ? ' · +' + (uniq.length - 2) : ''); mark.fills = [roleOr('state/danger', { r: 0.70, g: 0.11, b: 0.11 })];
        mark.textAutoResize = 'HEIGHT'; mark.resize(Math.max(ww, 200), mark.height);
        cell.strokes = [roleOr('state/danger', { r: 0.70, g: 0.11, b: 0.11 })]; cell.strokeWeight = 2; cell.strokeAlign = 'OUTSIDE';
      } else { summary.passed++; mark.characters = 'PASS'; mark.fills = [roleOr('state/success', { r: 0.12, g: 0.37, b: 0.36 })]; }
    }
  }
  await G.screenshot({ scale: 0.4 });
}
out.widthsTested = targets.length + ' phone variants × ' + WIDTHS.length + ' widths'; out.summary = summary; out.note = 'Report only — no component was changed. Review FAIL items before any correction is applied.';
out.qaBoard = QA.id;
return out;
