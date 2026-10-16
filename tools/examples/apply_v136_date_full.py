"""v136: owner 16 Oct 2026 — પ્રાણ પ્રતિષ્ઠા date in the date strip written in full: "૮ ફેબ્રુ., સોમવાર" → "૮ ફેબ્રુઆરી, સોમવાર"
(under "પ્રાણ પ્રતિષ્ઠા · બપોરે ૧૨:૩૯"; the box beside it already says "૨ – ૮ ફેબ્રુઆરી ૨૦૨૭"). Festival page only (desktop + phone),
as asked. The Home banner has the same strip but keeps "૮ ફેબ્રુ." — there the full form wraps both boxes onto two lines on sideways phones
(HomePhoneL +28 px) and runs past the strip on 320 px phones. Other short forms in compact calendars and day tabs stay.
usage: python3 tools/examples/apply_v136_date_full.py <project folder>"""
import os, sys
OLD, NEW = '૮ ફેબ્રુ., સોમવાર', '૮ ફેબ્રુઆરી, સોમવાર'
for page in ('PranPratishtha', 'PranPratishthaMobile'):
    p = os.path.join(sys.argv[1], page + '.dc.html'); s = open(p, encoding='utf-8').read()
    assert s.count(OLD) == 1, (page, s.count(OLD)); open(p, 'w', encoding='utf-8').write(s.replace(OLD, NEW)); print('updated', page)
