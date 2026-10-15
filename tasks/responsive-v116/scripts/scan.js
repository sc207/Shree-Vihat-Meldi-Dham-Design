// Responsive / UI scan of one rendered page. Returns {docW, issues:[...], notes:[...]}.
// issues = defects (must be looked at); notes = advisories (tap size 24–43 px on phones, soft images, long lines).
(() => {
  const W = innerWidth, H = innerHeight, phone = W <= 760;
  const out = { W, docW: document.documentElement.scrollWidth, issues: [], notes: [] };
  const root = document.querySelector('.vm-root');
  const cs = e => getComputedStyle(e);
  const hidden = e => { for (let p = e; p && p !== document.body; p = p.parentElement) { const s = cs(p); if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) return true; if (p.hasAttribute && p.hasAttribute('hidden')) return true; if (p.parentElement && p.parentElement.tagName === 'DETAILS' && !p.parentElement.open && p.tagName !== 'SUMMARY') return true; } return false; };
  const deco = e => !!e.closest('[aria-hidden="true"],.vm-sr,svg,script,style,.vx-marquee');
  const where = e => { const sec = e.closest('section,header,footer,nav,main,aside,dialog,[role=dialog]'); let s = ''; if (sec) s = sec.id || sec.getAttribute('aria-labelledby') || (typeof sec.className === 'string' ? sec.className.trim().split(/\s+/)[0] : sec.tagName); return s; };
  const lab = e => { const c = (typeof e.className === 'string' && e.className.trim()) ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : ''; return e.tagName.toLowerCase() + c + ' [' + where(e) + '] "' + (e.textContent || e.getAttribute('aria-label') || e.alt || '').trim().replace(/\s+/g, ' ').slice(0, 26) + '"'; };
  const add = (k, e, extra) => out.issues.push(k + ' ' + lab(e) + (extra ? ' ' + extra : ''));
  const note = (k, e, extra) => out.notes.push(k + ' ' + lab(e) + (extra ? ' ' + extra : ''));
  const inScroller = e => { for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) { const s = cs(p); if (s.overflowX !== 'visible') return true; if (s.position === 'fixed') return true; } return false; };
  const els = [...root.querySelectorAll('*')].filter(e => !(e instanceof SVGElement) && !hidden(e));

  // 1 past the screen edge / 2 clipped text / 3 distorted images
  for (const e of els) {
    const r = e.getBoundingClientRect(); if (r.width === 0 || r.height === 0) continue; const s = cs(e);
    if ((r.right > W + 1 || r.left < -1) && !inScroller(e) && !(s.position === 'absolute' && (deco(e) || !e.textContent.trim()))) add('past-edge', e, Math.round(r.left) + '..' + Math.round(r.right));
    if (!deco(e) && e.children.length === 0 && e.textContent.trim() && (s.overflowX === 'hidden' || s.overflowX === 'clip' || s.overflow === 'hidden')) {
      if (e.scrollWidth > e.clientWidth + 1 && s.textOverflow !== 'ellipsis') add('clipped-x', e, e.scrollWidth + '>' + e.clientWidth);
      if (e.scrollHeight > e.clientHeight + 2 && s.webkitLineClamp === 'none') add('clipped-y', e, e.scrollHeight + '>' + e.clientHeight);
    }
    if (e.tagName === 'IMG' && e.naturalWidth && s.objectFit === 'fill') { const a = r.width / r.height, n = e.naturalWidth / e.naturalHeight; if (Math.abs(a / n - 1) > 0.03) add('distorted', e, a.toFixed(2) + '/' + n.toFixed(2)); }
    // image softness on 2x screens (content images only)
    if (e.tagName === 'IMG' && e.naturalWidth && !deco(e) && r.width > 60) {
      const sc = s.objectFit === 'cover' ? Math.max(r.width / e.naturalWidth, r.height / e.naturalHeight) : s.objectFit === 'contain' ? Math.min(r.width / e.naturalWidth, r.height / e.naturalHeight) : r.width / e.naturalWidth;
      if (1 / sc < 1.5) note('soft-2x', e, 'sharp to ' + (1 / sc).toFixed(2) + 'x');
    }
  }
  // 4 text spilling out of its own visible box (pill, button, card)
  const boxed = e => { const s = cs(e); return (s.backgroundColor !== 'rgba(0, 0, 0, 0)' && s.backgroundColor !== 'transparent') || parseFloat(s.borderLeftWidth) > 0 || parseFloat(s.borderTopWidth) > 0; };
  for (const e of els) {
    if (deco(e) || !boxed(e)) continue; const r = e.getBoundingClientRect(); if (r.width < 8 || r.height < 8) continue;
    const tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n, worst = 0, txt = '';
    while ((n = tw.nextNode())) {
      if (!n.textContent.trim() || hidden(n.parentElement) || deco(n.parentElement)) continue;
      let p = n.parentElement, own = false; while (p && p !== e) { if (boxed(p)) { own = true; break; } p = p.parentElement; } if (own) continue;
      const rg = document.createRange(); rg.selectNodeContents(n);
      for (const q of rg.getClientRects()) { if (q.width < 1) continue; const d = Math.max(r.left - q.left, q.right - r.right, r.top - q.top - 2, q.bottom - r.bottom - 2); if (d > worst) { worst = d; txt = n.textContent.trim().slice(0, 24); } }
    }
    if (worst > 1.5) add('spill', e, 'by ' + Math.round(worst) + 'px "' + txt + '"');
  }
  // 5 tiny text / 6 low contrast (solid backgrounds only)
  const lum = c => { const m = c.match(/[\d.]+/g); if (!m) return null; const [r, g, b] = m.slice(0, 3).map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const alpha = c => { const m = c.match(/[\d.]+/g); return m && m.length > 3 ? +m[3] : 1; };
  const bgOf = e => { for (let p = e; p; p = p.parentElement) { const s = cs(p); if (s.backgroundImage !== 'none') return null; if (alpha(s.backgroundColor) >= 0.99) return s.backgroundColor; if (alpha(s.backgroundColor) > 0.05) return null; } return 'rgb(255,255,255)'; };
  const seenT = new Set(), seenC = new Set();
  for (const e of els) {
    if (deco(e)) continue; const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()); if (!own) continue;
    const s = cs(e), fs = parseFloat(s.fontSize), r = e.getBoundingClientRect(); if (r.width === 0) continue;
    const zoom = parseFloat(s.zoom) || 1; const efs = fs * (e.closest('.is-big') ? 1 : 1) ;
    if (efs < 12 && !seenT.has(lab(e))) { seenT.add(lab(e)); add('tiny-text ' + efs.toFixed(1) + 'px', e); }
    const bg = bgOf(e); if (!bg || alpha(s.color) < 0.99) continue;
    const L1 = lum(s.color), L2 = lum(bg); if (L1 === null || L2 === null) continue;
    const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05); const large = fs >= 24 || (fs >= 18.66 && +s.fontWeight >= 700);
    if (ratio < (large ? 3 : 4.5) && !seenC.has(lab(e))) { seenC.add(lab(e)); add('contrast ' + ratio.toFixed(2), e, s.color + ' on ' + bg); }
  }
  // 7 tap targets (interactive, visible, not inline links in running text)
  const inlineLink = e => { if (e.tagName !== 'A') return false; const p = e.parentElement; const ps = cs(p); if (!/^(P|LI|DD|SPAN|SMALL|TD)$/.test(p.tagName)) return false; return cs(e).display === 'inline' && [...p.childNodes].some(n => n !== e && n.textContent.trim()); };
  const seenK = new Set();
  for (const e of root.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,summary,[role=button],[role=tab],label[for]')) {
    if (hidden(e) || e.closest('.vm-sr') || inlineLink(e)) continue; const r = e.getBoundingClientRect(); if (r.width === 0 || r.height === 0) continue;
    if (e.tagName === 'INPUT' && (e.type === 'radio' || e.type === 'checkbox') && e.closest('label')) continue; // the label is the target
    const k = lab(e); if (seenK.has(k)) continue; seenK.add(k);
    const w = Math.round(r.width), h = Math.round(r.height);
    if (w < 24 || h < 24) add('tap<24 ' + w + 'x' + h, e); else if (phone && (w < 44 || h < 44)) note('tap<44 ' + w + 'x' + h, e);
  }
  // 8 text-on-text overlap (leaf text boxes intersecting, not nested; fixed/sticky layers excluded)
  const fixedLayer = e => { for (let p = e; p && p !== document.body; p = p.parentElement) { const ps = cs(p).position; if (ps === 'fixed' || ps === 'sticky') return true; } return false; };
  const leaves = els.filter(e => !deco(e) && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && !fixedLayer(e)).map(e => { const rg = document.createRange(); rg.selectNodeContents(e); return { e, rs: [...rg.getClientRects()].filter(q => q.width > 2 && q.height > 2).map(q => ({ l: q.left, r: q.right, t: q.top + scrollY, b: q.bottom + scrollY })) }; }).filter(x => x.rs.length);
  leaves.sort((a, b) => a.rs[0].t - b.rs[0].t);
  const seenO = new Set();
  for (let i = 0; i < leaves.length; i++) for (let j = i + 1; j < leaves.length; j++) {
    const A = leaves[i], B = leaves[j]; if (B.rs[0].t > A.rs[A.rs.length - 1].b + 60) break; if (A.e.contains(B.e) || B.e.contains(A.e)) continue;
    let hit = 0; for (const a of A.rs) for (const b of B.rs) { const ox = Math.min(a.r, b.r) - Math.max(a.l, b.l), oy = Math.min(a.b, b.b) - Math.max(a.t, b.t); if (ox > 3 && oy > Math.min(a.b - a.t, b.b - b.t) * 0.35) hit = 1; }
    if (hit) { const k = lab(A.e) + ' × ' + lab(B.e); if (!seenO.has(k)) { seenO.add(k); out.issues.push('overlap ' + k); } }
  }
  // 9 long lines (characters per line) on wide screens
  if (W >= 1024) for (const p of root.querySelectorAll('p,li,dd')) {
    if (hidden(p) || deco(p)) continue; const t = p.textContent.trim(); if (t.length < 160) continue; const rg = document.createRange(); rg.selectNodeContents(p);
    const tops = new Set([...rg.getClientRects()].filter(q => q.width > 2).map(q => Math.round(q.top))); const cpl = t.length / Math.max(1, tops.size);
    if (cpl > 110) note('long-line ' + Math.round(cpl) + 'cpl', p);
  }
  out.issues = [...new Set(out.issues)]; out.notes = [...new Set(out.notes)];
  return out;
})()
