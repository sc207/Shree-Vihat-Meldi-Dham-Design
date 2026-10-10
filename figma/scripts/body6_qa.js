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
