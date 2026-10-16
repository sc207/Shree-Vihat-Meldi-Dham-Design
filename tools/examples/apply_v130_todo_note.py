"""v130: canvas to-do note (canvas.json → notes.todo) brought up to date — owner-approved correction (10 Oct) plus one new request.
1. PDF line: the button has been hidden since v102, the note still said "તૈયાર છે" → same form as the Facebook line.
2. New line: a larger original of the કરમશીબાપા seated photo (09, 784×1045 — too small for the photo viewer; AI enlargement changed his face).
3. maxH 1377 → 1480 so the extra line is not cut off (nothing on the canvas below the note). No page changes.
usage: python3 tools/examples/apply_v130_todo_note.py <project folder>"""
import json, os, sys
p = os.path.join(sys.argv[1], 'canvas.json'); s = open(p, encoding='utf-8').read()
R = [('• કાર્યક્રમ પત્રિકાની PDF — \\"કાર્યક્રમ પત્રિકા (PDF)\\" બટન તૈયાર છે, લિંક મૂકવાની બાકી', '• કાર્યક્રમ પત્રિકાની PDF (હાલ બટન છુપાવેલું છે)'),
     ('• નિર્માણ કાર્યના તારીખ સાથેના ફોટા (નવું મંદિર → નિર્માણ પ્રગતિ), મહોત્સવના વાસ્તવિક ફોટા\\n',
      '• નિર્માણ કાર્યના તારીખ સાથેના ફોટા (નવું મંદિર → નિર્માણ પ્રગતિ), મહોત્સવના વાસ્તવિક ફોટા\\n'
      '• પરમ પૂજ્ય ભગવાન શ્રી કરમશીબાપાના આસન પર બિરાજમાન ફોટાની મોટી મૂળ ફાઇલ (હાલનો ફોટો નાનો છે)\\n'),
     ('"maxH": 1377,', '"maxH": 1480,')]
for a, b in R:
    assert s.count(a) == 1, (a[:40], s.count(a)); s = s.replace(a, b)
json.loads(s)   # still valid JSON
open(p, 'w', encoding='utf-8').write(s); print('updated', p)
