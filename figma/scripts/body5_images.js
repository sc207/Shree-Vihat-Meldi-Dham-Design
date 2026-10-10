// ===== Call 5: fill the "Image slot · NN_…" frames from the 26 dropped originals =====
// Changes ONLY the fills of image-slot frames (plus one image child inside a slot when a deity must sit at the bottom).
// Nothing else is moved, renamed, resized or deleted. Originals are matched to INVENTORY.csv by name AND pixel size.
const INV = [["01","01_deity_vihat-maa_cutout__9e553826353008ace0348667feebc15c",1200,1500],["02","02_deity_meldi-maa_cutout__11b539b692a86f3ebd187f4cdccda6f2",1200,1500],["03","03_deity_vihat-maa_glow__5db2fa3066346bbda071d80127890079",760,905],["04","04_deity_meldi-maa_glow__67db8acad0ff4fc9a1690e90a08d539b",670,921],["05","05_deity_lakhnechi-maa_glow__e31c2f7a518cb9d094489412d6c323c8",380,534],["06","06_deity_goga-maharaj_glow__713e6519487a5ab4a26d821bbca861a8",393,534],["07","07_portrait_karamshibapa_closeup-glow__692526c97fb81800db3adb90c432cc9a",1100,985],["08","08_portrait_karamshibapa_standing-white__01d1d891218823b7fc6777885d8634d1",1000,1497],["09","09_portrait_karamshibapa_seated-poster__361278fe9fd6e85e999500f1f74013a3",784,1045],["10","10_portrait_sureshbapa_blessing-glow__4e30bcd6319bfef6bce709ce0ef4afb1",1100,1019],["11","11_portrait_sureshbapa_candid__e1b6930a984c9f3a8eb9b9783ae97fe9",585,882],["12","12_portrait_sureshbapa_seated-poster__ea3a22f667e1db20db6134f406df44bb",960,1279],["13","13_portrait_sureshbapa_smiling-cutout__f784ff0d57da00d73030819bb850bb43",470,501],["14","14_temple_new-temple-render__ade906fff7b8cbe4a63f246237926871",2400,1881],["15","15_banner_dham-family__cd5574347256c288677d3f0e7b95dbc2",1800,1199],["16","16_logo_mark-red__e1c9cc4c85b15c1aea37fad5675f6596",708,708],["17","17_logo_mark-ivory__6cb43041a704672ae77ed549a7399de9",708,708],["18","18_logo_lockup-ivory_footer__b3915972ce74551f3675e24488a5ed84",2914,812],["19","19_qr_whatsapp-channel__d359256f876ef152e1aa584ebb20b4e8",624,624],["20","20_unused_logo_lockup-red__935458ac98acacb809b0d1329e9b374e",2914,812],["21","21_unused_deity_vihat-maa_cutout-large__95787e5469dde0e0ecebc09bef4a4a4a",1768,2000],["22","22_unused_deity_meldi-maa_cutout-large__a6fe6bdb26e6dded27110709664aea5a",1446,2000],["23","23_unused_gaadi_cutout__41bb877f7d1d833f978493c6366d07a1",531,470],["24","24_unused_diya_cutout__70db10d832218539d0ef40367176309a",478,521],["25","25_unused_naag_cutout-small__624e213ce2a19b887b8069e53658baea",183,275],["26","26_unused_poster_karamshibapa-e-j-vihat__d142fc2cdd2cad709f1a711292912aac",960,1279]];
const byNo = {}; for (const [no, base, w, h] of INV) byNo[no] = { no, base, w, h, id: base.split('__')[1] };
const strip = s => s.replace(/\.(webp|png|jpe?g)$/i, '').trim();
const imgFill = n => ('fills' in n && Array.isArray(n.fills)) ? n.fills.find(f => f.type === 'IMAGE') : null;
const inInstance = n => { for (let p = n.parent; p && p.type !== 'PAGE'; p = p.parent) if (p.type === 'INSTANCE') return true; return false; };
const boardOf = n => { let b = n; while (b.parent && b.parent.type !== 'PAGE') b = b.parent; return b; };

// 1. Find the dropped originals (any page), identify each one against the inventory.
// Searches the Components page only (Figma: never use loadAllPagesAsync; switch pages at most once per call). The README says to drop the images here.
const cands = [];
for (const n of page.findAll(n => /^\d\d_/.test(strip(n.name)) && !!imgFill(n))) cands.push({ n, page: page.name, base: strip(n.name), hash: imgFill(n).imageHash });
if (!cands.length) return { error: 'No dropped images found on the Components page. Nothing was changed. Drag the 26 files from the ZIP onto the Components page (Assets section) first; images on other pages are not searched.' };
const accepted = {}, rejected = [], extra = [], dupes = [], ambiguous = new Set(), groups = {};
for (const c of cands) {
  const no = c.base.slice(0, 2), want = byNo[no];
  if (!want) { extra.push({ name: c.n.name, page: c.page }); continue; }
  const how = c.base === want.base ? 'exact name' : (c.base.includes(want.id) ? 'id in name' : 'number only');
  let size = null; try { size = await figma.getImageByHash(c.hash).getSizeAsync(); } catch (e) { }
  const sizeOk = size ? (size.width === want.w && size.height === want.h) : how !== 'number only';
  if (!sizeOk) { rejected.push({ name: c.n.name, page: c.page, how, size: size ? size.width + 'x' + size.height : 'unknown', expected: want.w + 'x' + want.h }); continue; }
  (groups[no] = groups[no] || []).push({ ...c, how, size: size || { width: want.w, height: want.h } });
}
for (const [no, list] of Object.entries(groups)) {
  const hashes = [...new Set(list.map(c => c.hash))];
  if (hashes.length === 1) { accepted[no] = list[0]; continue; }
  const exact = [...new Set(list.filter(c => c.how === 'exact name').map(c => c.hash))];
  dupes.push({ no, layers: list.map(c => c.n.name + ' (' + c.page + ')') });
  if (exact.length === 1) accepted[no] = list.find(c => c.hash === exact[0]); else ambiguous.add(no); // two different pictures under one number: do not guess
}
const missingFiles = INV.map(r => r[0]).filter(no => !accepted[no] && !ambiguous.has(no));

// 2. Fill the slots (main components and boards only — instances inherit from their main component).
const slots = page.findAll(n => /^Image slot · \d\d_/.test(n.name) && n.type === 'FRAME' && !inInstance(n));
const filled = [], skipped = [], unfilled = [], boards = new Set();
for (const s of slots) {
  const rest = s.name.slice('Image slot · '.length), no = rest.slice(0, 2), want = byNo[no], slotBase = rest.split(' · ')[0];
  if (!want || !want.base.startsWith(slotBase + '__')) { unfilled.push({ slot: s.name, why: 'slot name does not match the inventory' }); continue; }
  if (ambiguous.has(no)) { unfilled.push({ slot: s.name, why: 'two different files share number ' + no }); continue; }
  const src = accepted[no]; if (!src) { unfilled.push({ slot: s.name, why: 'file ' + no + ' not found or not verified' }); continue; }
  const child = s.children.find(k => k.name === 'Image · ' + no);
  const has = (imgFill(s) && imgFill(s).imageHash === src.hash) || (child && imgFill(child) && imgFill(child).imageHash === src.hash);
  if (has) { skipped.push(s.id); continue; }
  if (child) child.remove(); // only ever our own image child from an earlier run
  const W = s.width, H = s.height, iw = src.size.width, ih = src.size.height;
  const contain = /· FIT/.test(s.name) || /logo|qr/.test(slotBase), bottom = /· FIT bottom/.test(s.name);
  const m = s.name.match(/focus (\d+)\/(\d+)/);
  let mode;
  if (contain && bottom) {
    const k = Math.min(W / iw, H / ih), w = Math.round(iw * k), h = Math.round(ih * k);
    if (H - h > 1 || W - w > 1) { const r = figma.createRectangle(); r.name = 'Image · ' + no; r.resize(w, h); r.fills = [{ type: 'IMAGE', imageHash: src.hash, scaleMode: 'FILL' }]; s.appendChild(r); r.x = Math.round((W - w) / 2); r.y = H - h; s.fills = []; mode = 'contain, bottom'; }
    else { s.fills = [{ type: 'IMAGE', imageHash: src.hash, scaleMode: 'FIT' }]; mode = 'contain'; }
  } else if (contain) { s.fills = [{ type: 'IMAGE', imageHash: src.hash, scaleMode: 'FIT' }]; mode = 'contain'; }
  else if (m) {
    const k = Math.max(W / iw, H / ih), wf = W / (iw * k), hf = H / (ih * k), fx = +m[1] / 100, fy = +m[2] / 100;
    s.fills = [{ type: 'IMAGE', imageHash: src.hash, scaleMode: 'CROP', imageTransform: [[wf, 0, (1 - wf) * fx], [0, hf, (1 - hf) * fy]] }]; mode = `cover, focus ${m[1]} % / ${m[2]} %`;
  } else { s.fills = [{ type: 'IMAGE', imageHash: src.hash, scaleMode: 'FILL' }]; mode = 'cover'; }
  s.strokes = []; s.dashPattern = [];
  filled.push({ id: s.id, file: no, mode }); boards.add(boardOf(s));
}

// 3. Karamshibapa check (07_portrait_karamshibapa_closeup-glow).
const k07 = slots.filter(s => s.name.includes('07_portrait_karamshibapa_closeup-glow'));
const k07ok = k07.length > 0 && !!accepted['07'] && k07.every(s => { const c = s.children.find(k => k.name === 'Image · 07'); return (imgFill(s) && imgFill(s).imageHash === accepted['07'].hash) || (c && imgFill(c) && imgFill(c).imageHash === accepted['07'].hash); });

// 4. Screenshots: every board that changed, plus a close look at the arch frames.
for (const b of boards) await b.screenshot({ scale: 0.35 });
const arch = page.findOne(n => n.type === 'COMPONENT_SET' && n.name === 'Arch frame'); if (arch) await arch.screenshot({ scale: 1 });
return {
  originalsFound: cands.length, verified: Object.keys(accepted).sort(), missingFiles, rejected, extra, duplicates: dupes, ambiguous: [...ambiguous],
  karamshibapa: { file: byNo['07'].base, matchedLayer: accepted['07'] ? accepted['07'].n.name : null, slots: k07.map(s => s.id), filledCorrectly: k07ok },
  slots: slots.length, filled, skippedAlreadyCorrect: skipped, unfilled, boardsChanged: [...boards].map(b => b.name)
};
