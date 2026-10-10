(() => {
  const W = innerWidth, out = { docW: document.documentElement.scrollWidth, pageH: document.documentElement.scrollHeight, issues: [] };
  const vis = e => { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false; const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const inScroller = e => { for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) { const cs = getComputedStyle(p); if (cs.overflowX !== 'visible' || cs.overflow !== 'visible') return true; if (cs.position === 'fixed') return true; } return false; };
  const label = e => { const c = (e.className && typeof e.className === 'string') ? '.' + e.className.trim().split(/\s+/)[0] : ''; const sec = e.closest('section,header,footer,nav,main'); const sc = sec ? (sec.getAttribute('aria-labelledby') || (typeof sec.className === 'string' ? sec.className.split(' ')[0] : sec.tagName)) : ''; return e.tagName.toLowerCase() + c + ' [' + sc + '] "' + (e.textContent || e.alt || '').trim().replace(/\s+/g, ' ').slice(0, 28) + '"'; };
  const add = (kind, e) => out.issues.push(kind + ' ' + label(e));
  const all = [...document.querySelectorAll('.vm-root *')].filter(e => !(e instanceof SVGElement) && vis(e));
  for (const e of all) {
    const r = e.getBoundingClientRect();
    if ((r.right > W + 1 || r.left < -1) && !inScroller(e)) {
      // ignore decorative absolutely-positioned layers (chakra, halo, glows)
      const cs = getComputedStyle(e); if (!(cs.position === 'absolute' && (e.getAttribute('aria-hidden') === 'true' || !e.textContent.trim()))) add('past-edge', e);
    }
    const cs = getComputedStyle(e);
    if (e.children.length === 0 && e.textContent.trim() && (cs.overflow !== 'visible' || cs.overflowX !== 'visible') && cs.overflowX !== 'auto' && cs.overflowX !== 'scroll') {
      if (e.scrollWidth > e.clientWidth + 1) add('clipped-x', e);
      if (e.scrollHeight > e.clientHeight + 2 && cs.webkitLineClamp === 'none') add('clipped-y', e);
    }
    if (e.tagName === 'IMG' && e.naturalWidth && cs.objectFit === 'fill') { const a = r.width / r.height, n = e.naturalWidth / e.naturalHeight; if (Math.abs(a / n - 1) > 0.03) add('distorted ' + a.toFixed(2) + '/' + n.toFixed(2), e); }
  }
  // button labels breaking inside a button: measure each text run on its own (icons and intentional two-line labels are not breaks)
  for (const b of document.querySelectorAll('.vm-root .vm-btn, .vm-root button, .vm-root .vm-chip')) {
    if (!vis(b)) continue;
    const w = document.createTreeWalker(b, NodeFilter.SHOW_TEXT); let tn;
    while ((tn = w.nextNode())) { if (tn.nodeValue.trim().length < 2) continue; const rg = document.createRange(); rg.selectNodeContents(tn); const lh = parseFloat(getComputedStyle(tn.parentElement).fontSize) * 0.6;
      const tops = [...rg.getClientRects()].filter(x => x.width > 1).map(x => x.top); if (tops.length > 1 && Math.max(...tops) - Math.min(...tops) > lh) { add('label-breaks', b); break; } }
  }
  // year split from its month, or a lone year/word line
  const tw = document.createTreeWalker(document.querySelector('.vm-root'), NodeFilter.SHOW_TEXT); let n;
  while ((n = tw.nextNode())) { const t = n.nodeValue; let i = t.indexOf('૨૦૨૭'); if (i < 1 || !vis(n.parentElement)) continue; let j = i - 1; while (j > 0 && /\s|,/.test(t[j])) j--; const r1 = document.createRange(); r1.setStart(n, j); r1.setEnd(n, j + 1); const r2 = document.createRange(); r2.setStart(n, i); r2.setEnd(n, i + 4); const a = r1.getBoundingClientRect(), c = r2.getBoundingClientRect(); if (a.height && c.height && Math.abs(a.top - c.top) > 4) add('year-split', n.parentElement); }
  out.issues = [...new Set(out.issues)];
  return out;
})()
