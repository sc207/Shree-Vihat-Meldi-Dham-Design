# Website-wide sweep for small visual defects on every board at the brief's screen sizes, intermediate widths and large text.
# Checks per render: page wider than screen, clipped text, distorted images, labels breaking in buttons, year split (tools/fullcheck.js);
# text spilling out of its own box; lone item on the last row of a grid/wrap; one-word last line in headings; icon off-centre
# against its label; text blocks overlapping each other.
# Usage: python3 work/fx/sweep.py <port> <out.json>
import asyncio, sys, json
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch, boards

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8771
OUT = sys.argv[2] if len(sys.argv) > 2 else 'work/fx/sweep_8771.json'
FULL = open('tools/fullcheck.js').read()
PHONE_W = [(320, 568), (360, 800), (375, 812), (390, 844), (430, 932), (480, 900), (600, 960), (700, 1000)]
DESK_W = [(768, 1024), (820, 1180), (900, 1200), (1024, 768), (1100, 800), (1200, 800), (1280, 800), (1366, 768), (1440, 900), (1920, 1080), (844, 390), (932, 430)]
BIG = {320, 390, 768, 1024, 1440}
WF = 'html{scroll-behavior:auto!important} *{animation:none!important;transition:none!important} .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}'
JS = r'''() => {
  const out = [];
  const vis = e => { const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) return false; const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const hidden = e => e.closest('.vm-sr,[aria-hidden=true],[hidden],.vx-marquee,details:not([open]) > :not(summary)');
  const pinned = e => { for (let p = e; p && p !== document.body; p = p.parentElement) { const s = getComputedStyle(p).position; if (s === 'sticky' || s === 'fixed') return true; } return false; };
  const lab = e => { const sec = e.closest('section,header,footer,nav,aside'); const sc = sec ? (sec.id || sec.getAttribute('aria-labelledby') || (typeof sec.className === 'string' ? sec.className.split(' ').slice(0, 2).join('.') : sec.tagName)) : '';
    return e.tagName.toLowerCase() + (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : '') + ' [' + sc + '] "' + (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 30) + '"'; };
  const Y = r => Math.round(r.top + scrollY);
  // 1. text outside its own visible box
  const boxed = e => { const s = getComputedStyle(e); return (s.backgroundColor !== 'rgba(0, 0, 0, 0)') || parseFloat(s.borderLeftWidth) > 0 || parseFloat(s.borderTopWidth) > 0; };
  for (const e of document.querySelectorAll('.vm-root *')) {
    if (hidden(e) || e instanceof SVGElement || !boxed(e) || !vis(e)) continue;
    const r = e.getBoundingClientRect(); if (r.width < 8 || r.height < 8) continue;
    let sc = e.parentElement, inScroll = false; while (sc) { const o = getComputedStyle(sc).overflowX; if (o === 'auto' || o === 'scroll') { inScroll = true; break; } sc = sc.parentElement; }
    const tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n, worst = 0, txt = '';
    while ((n = tw.nextNode())) { if (!n.textContent.trim()) continue; let p = n.parentElement, own = false; while (p && p !== e) { if (boxed(p)) { own = true; break; } p = p.parentElement; } if (own || hidden(n.parentElement) || !vis(n.parentElement)) continue;
      let q0 = n.parentElement, scr = false; while (q0 && q0 !== e) { const o = getComputedStyle(q0).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden' || o === 'clip') { scr = true; break; } q0 = q0.parentElement; } if (scr) continue;
      const rg = document.createRange(); rg.selectNodeContents(n); for (const q of rg.getClientRects()) { if (q.width < 1) continue; const d = Math.max(r.left - q.left, q.right - r.right, r.top - q.top - 2, q.bottom - r.bottom - 2); if (d > worst) { worst = d; txt = n.textContent.trim().slice(0, 24); } } }
    if (worst > 1.5 && !inScroll) out.push({k: 'text-outside-box', el: lab(e), by: Math.round(worst), y: Y(r)});
  }
  // 2. lone item on the last row of a grid / wrapping row
  for (const e of document.querySelectorAll('.vm-root *')) {
    if (hidden(e) || e instanceof SVGElement || !vis(e)) continue; const s = getComputedStyle(e);
    if (!(s.display === 'grid' || (s.display === 'flex' && s.flexWrap === 'wrap'))) continue;
    const kids = [...e.children].filter(c => vis(c) && getComputedStyle(c).position !== 'absolute'); if (kids.length < 4) continue;
    const rows = {}; for (const c of kids) { const t = Math.round(c.getBoundingClientRect().top / 4); (rows[t] = rows[t] || []).push(c); }
    const rs = Object.keys(rows).map(Number).sort((a, b) => a - b).map(k => rows[k]); if (rs.length < 2) continue;
    const last = rs[rs.length - 1], prev = rs[rs.length - 2];
    const ws = kids.map(c => c.getBoundingClientRect().width), same = Math.max(...ws) / Math.min(...ws) < 1.6;
    if (last.length === 1 && prev.length >= 3 && same) out.push({k: 'lone-last-item', el: lab(e), rows: rs.map(r => r.length).join('+'), y: Y(e.getBoundingClientRect())});
  }
  // 3. one word alone on the last line of a heading
  for (const h of document.querySelectorAll('.vm-root h1, .vm-root h2, .vm-root h3')) {
    if (hidden(h) || !vis(h)) continue; const words = []; const tw = document.createTreeWalker(h, NodeFilter.SHOW_TEXT); let n;
    while ((n = tw.nextNode())) { const re = /\S+/g; let m; while ((m = re.exec(n.nodeValue))) { const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length); const q = rg.getBoundingClientRect(); if (q.width) words.push({w: m[0], top: Math.round(q.top)}); } }
    if (words.length < 3) continue; const lines = {}; for (const w of words) { const k = Math.round(w.top / 6); (lines[k] = lines[k] || []).push(w.w); }
    const L = Object.keys(lines).map(Number).sort((a, b) => a - b).map(k => lines[k]);
    if (L.length >= 2 && L[L.length - 1].length === 1 && L[L.length - 2].length >= 2) out.push({k: 'one-word-last-line', el: lab(h), lines: L.map(l => l.join(' ')).join(' / ').slice(0, 80), y: Y(h.getBoundingClientRect())});
  }
  // 4. icon off-centre against its label inside a button or link
  for (const b of document.querySelectorAll('.vm-root a, .vm-root button')) {
    if (hidden(b) || !vis(b) || pinned(b)) continue; const svg = b.querySelector(':scope > svg, :scope > span > svg'); if (!svg || !vis(svg)) continue;
    if (getComputedStyle(svg.parentElement).flexDirection === 'column') continue;
    const tw = document.createTreeWalker(b, NodeFilter.SHOW_TEXT); let n, tr = null; while ((n = tw.nextNode())) { if (n.nodeValue.trim().length > 1 && !hidden(n.parentElement)) { const rg = document.createRange(); rg.selectNodeContents(n); const rects = [...rg.getClientRects()].filter(q => q.width > 1); if (rects.length === 1) tr = rects[0]; break; } }
    if (!tr) continue; const sr = svg.getBoundingClientRect(); if (sr.top > tr.bottom || sr.bottom < tr.top) continue;   // icon above/below the label is a stacked layout
    const d = (sr.top + sr.height / 2) - (tr.top + tr.height / 2); if (Math.abs(d) > 3) out.push({k: 'icon-off-centre', el: lab(b), by: Math.round(d), y: Y(b.getBoundingClientRect())});
  }
  // 5. text blocks overlapping each other
  const texts = [...document.querySelectorAll('.vm-root *')].filter(e => !(e instanceof SVGElement) && !hidden(e) && !pinned(e) && [...e.childNodes].some(c => c.nodeType === 3 && c.nodeValue.trim()) && vis(e));
  const rects = texts.map(e => { const rg = document.createRange(); rg.selectNodeContents(e); return [...rg.getClientRects()].filter(q => q.width > 2 && q.height > 4); });
  for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
    const a = texts[i], b = texts[j]; if (a.contains(b) || b.contains(a)) continue;
    let hit = false; for (const p of rects[i]) { for (const q of rects[j]) { const ox = Math.min(p.right, q.right) - Math.max(p.left, q.left), oy = Math.min(p.bottom, q.bottom) - Math.max(p.top, q.top); if (ox > 3 && oy > 0.4 * Math.min(p.height, q.height)) { hit = true; break; } } if (hit) break; }
    if (hit) out.push({k: 'text-overlap', el: lab(a) + ' × ' + lab(b), y: Y(a.getBoundingClientRect())});
  }
  return out;
}'''

async def run(b, board, W, H, big):
    ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30', big_text=big))
    pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    await pg.goto(f'http://127.0.0.1:{PORT}/{board}.dc.html'); await pg.wait_for_timeout(900)
    await pg.add_style_tag(content=WF % (W, W)); await pg.wait_for_timeout(350)
    full = await pg.evaluate(FULL); mine = await pg.evaluate(JS); await ctx.close()
    issues = [{'k': i.split(' ')[0], 'el': i} for i in full['issues']] + mine
    if full['docW'] > W: issues.append({'k': 'page-wider-than-screen', 'el': f"docW {full['docW']}"})
    issues += [{'k': 'js-error', 'el': e} for e in errs]
    return issues

async def main():
    res = {}
    async with async_playwright() as p:
        b = await launch(p)
        for name, bw, fh in boards('design/project'):
            if name in ('HomeTablet', 'HomeTabletL', 'HomePhoneL'): sizes = [{'HomeTablet': (834, 1112), 'HomeTabletL': (1180, 820), 'HomePhoneL': (844, 390)}[name]]
            elif bw <= 760: sizes = PHONE_W if name not in ('MenuMobile', 'OfflineMobile') else [(320, 568), (390, 844), (430, 932)]
            else: sizes = DESK_W
            for W, H in sizes:
                for big in ((False, True) if W in BIG or name.startswith('HomeTablet') or name == 'HomePhoneL' else (False,)):
                    key = f'{name}|{W}x{H}|{"big" if big else "std"}'
                    res[key] = await run(b, name, W, H, big)
                    if res[key]: print(key, len(res[key]), sorted({i['k'] for i in res[key]}), flush=True)
            json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=0)
        await b.close()
    json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=0)
    print('runs', len(res))

asyncio.run(main())
