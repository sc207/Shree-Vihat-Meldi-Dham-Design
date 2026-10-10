# EXAMPLE kept for reference: the exact script that produced this published version.
# Pattern: exact-string replacements, each asserted to occur once, applied to every page variant; new CSS appended to site.css;
# frame heights updated in the page root, data-props and canvas.json. Its default path points to the old session —
# ALWAYS pass your work folder WITH a trailing slash (paths are built as folder + file name):
#   python3 tools/examples/apply_v105_aaje.py work/project/
# Only meaningful against the version it was written for (it asserts the old text is present, so it stops safely otherwise).
# v105: (1) on a પૂનમ date, "આજે" moves to the પૂનમ tile (dates come from the page's own panchang list);
#       (2) "આજે" follows the Indian date (Asia/Kolkata, UTC+5:30, no daylight saving), like the calendar and the home page.
import sys
P = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/-home-claude/dd84a57e-267c-5f0e-ba89-c24b2694ae3a/scratchpad/apply_poonam/project/'
OLD_LI = '<li class="is-gadi is-poonam">'
NEW_LI = '<li class="is-gadi is-poonam {{tp}}">'
OLD_D = 'var d = new Date().getDay();'
NEW_D = 'var d = new Date(Date.now() + 330 * 6e4).getUTCDay(); // weekday in India (UTC+5:30), same clock as the calendar below'
OLD_JS = "for (var i = 0; i < 7; i++) { v['t' + i] = i === d ? 'is-today' : ''; }"
NEW_JS = ("// on a પૂનમ date the ગાદી is on, so “આજે” marks the પૂનમ tile instead of the weekday\n"
          "v.tp = EV.some((e) => e[4] === 'is-poonam' && e[0] === today) ? 'is-today' : '';\n"
          "for (var i = 0; i < 7; i++) { v['t' + i] = (i === d && !v.tp) ? 'is-today' : ''; }")
for fn in ('Darshan.dc.html', 'DarshanMobile.dc.html'):
    s = open(P + fn, encoding='utf-8').read()
    assert s.count(OLD_LI) == 1 and s.count(OLD_JS) == 1 and s.count(OLD_D) == 1, fn
    s = s.replace(OLD_LI, NEW_LI).replace(OLD_JS, NEW_JS).replace(OLD_D, NEW_D)
    open(P + fn, 'w', encoding='utf-8').write(s); print(fn, 'patched')
