"""Shared helpers for the check tools: browser launch, frozen/shifted clock, board list."""
import glob, os, re

# Freeze animations and let the page take its natural height (boards have a fixed height in the design).
FIX = ('*{animation:none!important;transition:none!important;caret-color:transparent!important} '
       '.vx-page::after{display:none!important} .vx-page{height:auto!important;min-height:0!important} '
       '*::before,*::after{animation:none!important;transition:none!important}')   # pseudo-element animations (journey marker, darshan aura) were not frozen
# The five daily times used to size frames (darshan card open/closed changes some heights).
DAILY_TIMES = ['2026-10-10T04:40:00+05:30', '2026-10-10T06:30:00+05:30', '2026-10-10T12:30:00+05:30',
               '2026-10-10T19:30:00+05:30', '2026-10-10T22:30:00+05:30']


def clock_script(iso, frozen=True, big_text=None):
    """Init script: set the page clock to `iso` (frozen = time stands still, so countdowns are repeatable).
    big_text True/False presets the અ+ large-text toggle (stored in localStorage 'vx-fs')."""
    body = ("const FIXED=new Date('%s').getTime();const RD=Date;class FD extends RD{constructor(...a){if(a.length)super(...a);else super(FIXED);} static now(){return FIXED;}};window.Date=FD;" % iso
            if frozen else
            "const off=new Date('%s').getTime()-Date.now();const RD=Date;class FD extends RD{constructor(...a){if(a.length)super(...a);else super(RD.now()+off);} static now(){return RD.now()+off;}};window.Date=FD;" % iso)
    if big_text is not None:
        body += "try{localStorage.setItem('vx-fs','%s')}catch(e){}" % ('1' if big_text else '0')
    return '(()=>{%s})()' % body


async def launch(p):
    """Chromium from Playwright's own install; falls back to the sandbox's pre-installed build."""
    try:
        return await p.chromium.launch()
    except Exception:
        for exe in sorted(glob.glob('/opt/pw-browsers/chromium*/chrome-linux/chrome')):
            return await p.chromium.launch(executable_path=exe)
        raise


def boards(project):
    """[(board name, board width, frame height)] read from each page's root element."""
    out = []
    for f in sorted(glob.glob(os.path.join(project, '*.dc.html'))):
        m = re.search(r'class="vm-root vx-page[^"]*" style="width: (\d+)px; height: (\d+)px', open(f, encoding='utf-8').read())
        out.append((os.path.basename(f)[:-8], int(m.group(1)), int(m.group(2))))
    return out
