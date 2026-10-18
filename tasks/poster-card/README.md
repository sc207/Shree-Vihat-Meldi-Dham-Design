# મંગલારોહણ poster and the website news card — 18 Oct 2026

The owner's poster canvas: `https://claude.ai/artifact/MwLPukDNTAnXfDDuQ8npsp` (Design type), boards Poster A3 (1123×1587),
Social 4:5 (1080×1350), Logo, Car sticker — and, since 18 Oct, **Website card 1200×900 (4:3)** (`Card.dc.html`, canvas version
`1792327325-e6ff`). A copy of the canvas files is in [canvas/](canvas/). Its images are the website's own assets (same SHA-256:
render = `ade906…`, વિહત માઁ = `9e5538…`, મેલડી માઁ = `11b539…`, temple mark = `6cb430…`).

## Why a separate card board

The news card "મહોત્સવની તૈયારી — સેવા નોંધણી શરૂ" (Home `vm-update` cards and the Gallery news grid) shows its picture with
`object-fit: cover` in a landscape box: 371×278 (laptop), 472×314 (1024 px, 3:2), 377×260 (tablet), 358×269 / 288×216 (phones).
The portrait poster boards cut off the મંગલારોહણ wordmark and cut through both Matas ([portrait-in-card-1440](pictures/portrait-in-card-1440.webp),
[390](pictures/portrait-in-card-390.webp)); shown whole they become a small picture with side bars.

## The card board

Same colours, frame, fonts and images as the poster. Left: lotus, મંગલારોહણ (Shrikhand 94 px), મૂર્તિ પ્રાણ પ્રતિષ્ઠા મહોત્સવ, the date,
temple mark with શ્રી વિહત મેલડી ધામ · સાણંદ. Right: the arch with the new temple and both Matas whole. The top-left corner has no
ornament and no text, because the website's "મહોત્સવ" label sits there; all content stays inside y 122–778 so the 3:2 box at
1024 px crops nothing. Rendered: [card-1200x900](pictures/card-1200x900.webp); inside the news card at 1440, 1024, 834, 390, 320 and
Gallery 768: [card-fit-4x3](pictures/card-fit-4x3.webp) (local preview made with [card_fit.py](card_fit.py); fonts from the fontsource
GitHub repo).

## Status

**Not on the website.** Putting it into the news card (Home boards + Gallery news) needs the owner's approval; it would be its own
version: upload the 1200×900 render as an asset of the website artifact and point the card's `<img>` to it on every Home board and in
the Gallery news data.
