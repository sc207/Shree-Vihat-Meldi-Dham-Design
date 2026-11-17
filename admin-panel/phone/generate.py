import re,base64
exec(open('gen.py',encoding='utf-8').read().split("# keep first five screens from v1")[0])  # css, icons, helpers from v2
def gn(n):return ''.join('૦૧૨૩૪૫૬૭૮૯'[int(c)] for c in str(n))
G=[gn(i) for i in range(1,40)]
def idr(on,name,l,pill,pc):return f'<div class="rr" style="min-height:64px"><span class="cb {"on" if on else ""}">{"✓" if on else ""}</span><span class="m"><b>{name}</b><small>{l}</small></span><span class="s"><span class="pill {pc}">{pill}</span></span><span class="ib" style="width:40px;height:40px">{ic("eye")}</span></div>'

def pl(t,a,b):
    p=int(100*a/b) if b else 0
    return f'<div class="tg" style="display:grid;gap:6px"><div style="display:flex;align-items:center;gap:10px"><span class="m"><b>{t}</b><small>{"ફાળવેલા "+G[a-1] if a else "ફાળવેલા ૦"} · {"જોઈએ "+G[b-1] if b else "જરૂરિયાત નક્કી નથી"}</small></span><span class="step"><span>−</span><b>{G[b-1] if b else "—"}</b><span>+</span></span></div>{f"<div class=meter><i style=width:{p}%></i></div>" if b else ""}</div>'

def rail(on):
    it=[('dash','ડેશબોર્ડ'),('reg','નોંધણી'),('ctl','નિયંત્રણ'),('pin','પધરામણી'),('menu','વધુ')]
    return '<div class="rail">'+''.join(f'<div class="{"on" if i==on else ""}">{ic(k)}{t}</div>' for i,(k,t) in enumerate(it))+'</div>'

def lr(av,n,l,p,pc):return f'<div class="rr" style="min-height:56px;padding:7px 10px"><span class="av" style="width:36px;height:36px">{av}</span><span class="m"><b>{n}</b><small>{l}</small></span><span class="pill {pc}">{p}</span></div>'

WDAY=['મંગળ','બુધ','ગુરુ','શુક્ર','શનિ','રવિ','સોમ']
def days(on=0,sub=None,off=(),lab='મહોત્સવનો દિવસ · ફેબ્રુઆરી ૨૦૨૭'):
    d=['૨','૩','૪','૫','૬','૭','૮']
    return f'<div style="display:grid;gap:6px"><div class="dlab">{lab}</div><div class="days">'+''.join(f'<span class="{"on" if i==on else ""}"><small>{WDAY[i]}</small>{x}</span>' for i,x in enumerate(d))+'</div></div>'
RED='data:image/png;base64,'+base64.b64encode(open('emb-red-96.png','rb').read()).decode()
LIGHT='data:image/png;base64,'+base64.b64encode(open('emb-light-96.png','rb').read()).decode()
css+='''
/* v3: full phone set */
.lg{width:38px;height:38px;flex:none;object-fit:contain}
.bar{gap:8px;padding:9px 12px}
.card{box-shadow:0 1px 2px rgba(80,40,20,.05)}
.grp{margin:38px 0 14px;font:700 22px/1.3 "Noto Serif Gujarati",serif;color:var(--mar);border-bottom:2px solid var(--gold);padding-bottom:6px;display:flex;gap:12px;align-items:baseline}
.grp small{font:500 13px "Hind Vadodara";color:var(--mut)}
.item h2{font-size:15px;display:flex;gap:8px;align-items:baseline}.item h2 i{font-style:normal;background:var(--mar);color:#fff;border-radius:6px;font-size:11.5px;padding:1px 7px}
.item p.why{min-height:38px;font-size:12.5px;margin-bottom:8px}
.idx{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 8px}.idx a{font-size:13px;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:5px 12px;color:var(--mar);text-decoration:none;font-weight:600}
.ta{min-height:76px;align-items:flex-start;padding-top:10px}
.fl small{font-weight:400;color:var(--mut);font-size:12px}
.sheet{max-height:86%}
.hl{font-weight:700;font-size:14px;margin-top:2px}
.login{flex:1;display:flex;flex-direction:column}
.lhead{background:linear-gradient(135deg,var(--mar),var(--mar2));color:#fff;padding:26px 20px 30px;display:grid;justify-items:center;gap:6px;text-align:center;border-radius:0 0 26px 26px}
.lhead img{width:74px;height:74px}.lhead b{font:700 20px/1.3 "Noto Serif Gujarati",serif}.lhead small{opacity:.85;font-size:13px}
.lform{padding:20px 20px 0;display:grid;gap:12px}
.lform h3{margin:0;font:700 20px "Noto Serif Gujarati",serif;color:var(--mar)}
.link{color:var(--mar);font-weight:600;text-decoration:underline;font-size:14px}
.err{background:var(--badbg);color:var(--bad);border-radius:12px;padding:9px 12px;font-size:13.5px;font-weight:600}
.okb{background:var(--okbg);color:var(--ok);border-radius:12px;padding:9px 12px;font-size:13.5px;font-weight:600}
.infob{background:var(--infobg);color:var(--info);border-radius:12px;padding:9px 12px;font-size:13.5px}
.otp{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}.otp span{height:52px;border:1px solid #d9cbb1;border-radius:12px;background:#fff;display:grid;place-items:center;font-size:20px;font-weight:700}
.stepper6{display:grid;grid-template-columns:repeat(6,1fr);gap:4px}.stepper6 span{height:6px;border-radius:3px;background:#e6dac4}.stepper6 .d{background:var(--ok)}.stepper6 .c{background:var(--mar)}
.st3{display:flex;align-items:center;gap:6px;font-size:12px;font-weight:600;color:var(--mut)}.st3 i{font-style:normal;width:24px;height:24px;border-radius:50%;border:1.5px solid #cdbfa8;display:grid;place-items:center;flex:none}.st3 i.d{background:var(--ok);border-color:var(--ok);color:#fff}.st3 i.c{border-color:var(--mar);color:var(--mar)}.st3 u{flex:1;height:2px;background:#e0d3bb;text-decoration:none}
.idcard{width:216px;height:344px;border-radius:14px;overflow:hidden;background:#fff;border:1px solid #d8cbb2;justify-self:center;display:flex;flex-direction:column;box-shadow:0 6px 18px rgba(60,20,30,.18)}
.idcard .h{background:linear-gradient(135deg,var(--mar),var(--mar2));color:#fff;text-align:center;padding:10px 8px 26px;font-size:11px}.idcard .h img{width:30px;height:30px}.idcard .h b{display:block;font:700 13px "Noto Serif Gujarati",serif}
.idcard .p{width:84px;height:100px;border-radius:42px 42px 10px 10px;border:3px solid var(--gold);background:#f4e6c8;margin:-20px auto 0;display:grid;place-items:center;color:#7a5a10;font-weight:700;font-size:22px}
.idcard .n{text-align:center;font-weight:700;font-size:15px;margin-top:6px}.idcard .r{text-align:center;font-size:11px;color:var(--mut)}
.idcard .b{margin-top:auto;background:var(--ok);color:#fff;padding:8px 10px;display:flex;align-items:center;gap:8px;font-size:11.5px}.idcard .b i{width:44px;height:44px;background:#fff;border-radius:6px;flex:none;background-image:repeating-linear-gradient(45deg,#222 0 3px,#fff 3px 6px)}
.cam{flex:1;background:#1c1014;display:grid;place-items:center;position:relative}.cam i{width:230px;height:230px;border:3px solid #f3d58a;border-radius:24px;box-shadow:0 0 0 2000px rgba(0,0,0,.35)}.cam span{position:absolute;bottom:26px;color:#fff;font-weight:600;font-size:14px;text-align:center;left:20px;right:20px}
.sk{height:14px;border-radius:7px;background:linear-gradient(90deg,#efe5d2,#f7f0e2,#efe5d2)}
.empty{display:grid;justify-items:center;gap:8px;padding:34px 20px;text-align:center}.empty img{width:70px;height:70px;opacity:.55}.empty b{font-size:16px}.empty p{margin:0;color:var(--mut);font-size:13.5px}
.offbar{background:#3a2a2e;color:#fff;font-size:13px;font-weight:600;padding:8px 14px;flex:none}
.toast{position:absolute;left:14px;right:14px;bottom:86px;background:var(--mar2);color:#fff;border-radius:14px;padding:12px 14px;font-weight:600;font-size:14px;display:flex;gap:10px;align-items:center;box-shadow:0 8px 20px rgba(0,0,0,.25)}.toast i{color:#f3d58a;font-style:normal}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;text-align:center;font-size:12.5px}.cal span{height:40px;border-radius:10px;display:grid;place-items:center;background:var(--card);border:1px solid var(--line);position:relative}.cal .h{border:0;background:none;height:20px;color:var(--mut);font-size:11px}.cal .o{background:none;border:0;color:#c9bca6}.cal .on{background:var(--mar);color:#fff;border-color:var(--mar)}.cal .e::after{content:"";position:absolute;bottom:5px;width:5px;height:5px;border-radius:50%;background:var(--gold)}
.bars{display:flex;align-items:flex-end;gap:6px;height:90px;padding:0 4px}.bars i{flex:1;background:var(--gold);border-radius:4px 4px 0 0}
.rolec{border:1.5px solid var(--line);border-radius:12px;padding:9px 12px;display:flex;gap:10px;align-items:center;background:var(--card)}.rolec.on{border-color:var(--mar);background:#f8ece6}.rolec b{display:block;font-size:14px}.rolec small{color:var(--mut);font-size:12px}.rolec i{width:20px;height:20px;border-radius:50%;border:1.5px solid #b9a98c;flex:none}.rolec.on i{border:6px solid var(--mar)}
'''
css+='''
/* v4: calmer, bigger, simpler */
:root{--bg:#f6f3ee;--card:#fff;--line:#ebe5da;--ink:#1e1a1b;--mut:#6a6165}
body{font-size:16px}
.ph,.phl{background:var(--bg)}
.bar{background:#fff;padding:10px 14px;gap:10px;border-bottom:1px solid var(--line)}
.bar .t small{display:none}
.bar .t b{font:700 20px/1.3 "Hind Vadodara",sans-serif;color:var(--ink)}
.lg{width:34px;height:34px}
.ib,.back{width:44px;height:44px;border:0;background:#f4efe8}
.body{padding:14px 16px 0;gap:12px}
.card{border-radius:16px;border-color:var(--line);box-shadow:0 1px 3px rgba(40,20,10,.06)}
.nav{background:#fff;padding:6px 8px 12px}.nav div{font-size:12px;gap:3px}.nav svg{width:23px;height:23px}
.nav .on{background:#f7e9eb}
.row{min-height:62px;padding:0 14px;gap:14px}.row .l{font-size:16px}.row .l small{font-size:13.5px}
.row .n{width:38px;height:38px;border-radius:12px;font-size:17px}
.rr{min-height:74px;padding:12px 14px;gap:12px}.rr .m b{font-size:16.5px}.rr .m small{font-size:13.5px}
.rr .m small+small,.rr .s small{display:none}
.av{width:46px;height:46px;border-radius:50%;font-size:15px}
.pill{font-size:13px;padding:3px 10px}
.seg{background:#ece6dc;border-radius:14px;padding:4px}.seg span{font-size:14.5px;padding:10px 4px;border-radius:10px;color:#4a4246}
.seg .on{background:#fff;color:var(--mar);box-shadow:0 1px 3px rgba(0,0,0,.14)}
.tabs span{font-size:14.5px;padding:9px 15px;background:#fff}
.btn{height:52px;font-size:16px;border-radius:14px}.btn.sm{height:44px;font-size:14.5px}
.inp{height:52px;font-size:16px;border-radius:14px}.fl{font-size:14.5px;gap:6px}.fl small{font-size:13px}
.act{min-height:58px;font-size:16px;padding:0 14px}
.kv{font-size:15.5px;grid-template-columns:116px 1fr;padding:14px;gap:10px}.kv span{font-size:14px}
.sec{font-size:16px}.sec a{font-size:14px}.lab{font-size:13.5px}.note{font-size:13.5px}
.search .in{height:50px;font-size:15.5px;border-radius:14px;background:#fff}
.hero{padding:16px;border-radius:18px}.hero b{font-size:19px}.hero .chips span{font-size:13px;padding:4px 11px}
.kpis div{padding:11px 12px;border-radius:14px}.kpis b{font-size:22px}.kpis small{font-size:13px}
.cnt b{font-size:20px}.cnt small{font-size:12.5px}.cnt div{padding:9px 10px;border-radius:14px}
.tiles .tile{padding:9px 9px;border-radius:14px}.tile small{font-size:12px}.tile b{font-size:15px}
.tg{min-height:64px;padding:10px 14px}.tg .m b{font-size:16px}.tg .m small{font-size:13.5px}.lv{font-size:12px;line-height:19px}
.acc .hd{min-height:64px;font-size:16.5px;padding:0 14px}.acc .hd span{display:grid}.acc .hd small{font-size:13.5px;font-weight:400}
.fold{min-height:58px;font-size:16px;padding:0 14px}
.at{padding:12px 14px}.at .top b{font-size:16.5px}.at .top small{font-size:13.5px}.bt span{height:50px;font-size:16px;border-radius:14px}
.sum b{font-size:22px}.sum small{font-size:13px}
.sheet{padding:8px 18px 18px;gap:12px}.sheet h3{font:700 20px/1.3 "Hind Vadodara",sans-serif;color:var(--ink)}
.warnb,.err,.okb,.infob{font-size:14.5px;border-radius:14px;padding:11px 14px}
.count{font-size:14px}
.dlab{font-size:13.5px;color:var(--mut);font-weight:600}
.days{gap:6px}.days span{height:60px;border-radius:14px;background:#fff;font-size:19px;display:grid;align-content:center;justify-items:center;line-height:1.15;border-color:var(--line)}
.days span small{order:-1;font-size:11.5px;color:var(--mut);font-weight:600}
.days .on{background:var(--mar);border-color:var(--mar)}.days .on small{color:#f3dcd0}
.gridm div{min-height:88px;font-size:13.5px;border-radius:16px}.gridm.q{grid-template-columns:repeat(4,1fr)}.gridm.q div{min-height:82px;font-size:13px}
.qr{min-height:58px;font-size:16.5px;border-radius:16px}
.idh b{font:700 19px/1.3 "Hind Vadodara",sans-serif;color:var(--ink)}.idh small{font-size:14px}
.lhead b{font-size:22px}.lform h3{font:700 22px "Hind Vadodara",sans-serif;color:var(--ink)}
.selbar{font-size:15px;border-radius:16px}.selbar b{font-size:14.5px;padding:11px 14px}
.rolec b{font-size:15.5px}.rolec small{font-size:13px}
.tbl{font-size:14.5px}.tbl th{font-size:13px}
.photo{align-self:center;width:150px;height:180px;border-radius:20px;background:#f1e4c6;justify-self:center;display:grid;place-items:center;color:#7a5a10;font-size:46px;font-weight:700;border:3px solid #fff;box-shadow:0 4px 14px rgba(40,20,10,.15)}
.newtag{font-size:11.5px;background:#e3ecf8;color:#2b4f8a;border-radius:6px;padding:1px 7px;font-weight:700;margin-left:6px}
.lbar b{font:700 18px "Hind Vadodara",sans-serif;color:var(--ink)}
'''
def bar3(sm,title,right=('search','bell'),back=False):
    r=''.join(f'<div class="ib">{ic(k)}{"<i></i>" if k=="bell" else ""}</div>' for k in right)
    l=f'<div class="back">{ic("back")}</div>' if back else f'<img class="lg" src="{RED}" alt="">'
    return f'<div class="bar">{l}<div class="t"><small>{sm}</small><b>{title}</b></div>{r}</div>'
def P(sm,title,body,n=None,right=('search','bell'),back=False,foot='',over='',pre=''):
    return f'<div class="ph">{pre}{bar3(sm,title,right,back)}<div class="body">{body}</div>{foot}{nav(n) if n is not None else ""}{over}</div>'
def card(x,st=''):return f'<div class="card" {f"style=\"{st}\"" if st else ""}>{x}</div>'
def rows(xs):return card(''.join(f'<div class="row"><span class="n {c}">{n}</span><span class="l">{t}{f"<small>{s}</small>" if s else ""}</span>{sv("chev")}</div>' for n,c,t,s in xs))
def acts(xs):return card(''.join((f'<div class="act"><span>{x}</span>{sv("chev")}</div>' if isinstance(x,str) else f'<div class="act"><span>{x[0]}</span><span class="val">{x[1]}</span>{sv("chev")}</div>') for x in xs))
def kv(xs):return '<div class="card kv">'+''.join(f'<span>{k}</span><b>{v}</b>' for k,v in xs)+'</div>'
def fl(l,v='',ph=True,hint='',cls=''):return f'<label class="fl">{l}<span class="inp {cls}" style="{"" if ph else "color:var(--ink)"}">{v}</span>{f"<small>{hint}</small>" if hint else ""}</label>'
def bt(sec,pri,danger=False):return f'<div style="display:flex;gap:8px"><span class="btn">{sec}</span><span class="btn pri" {"style=background:var(--bad);border-color:var(--bad)" if danger else ""}>{pri}</span></div>'
def foot(sec,pri):return f'<div class="foot">{f"<span class=btn>{sec}</span>" if sec else ""}<span class="btn pri">{pri}</span></div>'
def sheet(title,inner):return f'<div class="dim"></div><div class="sheet"><h3>{title}</h3>{inner}</div>'
def cnt(xs):return '<div class="cnt">'+''.join(f'<div class="{"w" if len(x)>2 else ""}"><b>{x[0]}</b><small>{x[1]}</small></div>' for x in xs)+'</div>'
def pill(t,c):return f'<span class="pill {c}">{t}</span>'
def lab(t):return f'<div class="lab">{t}</div>'
def note(t):return f'<p class="note">{t}</p>'
def sec(t,a=''):return f'<div class="sec">{t}{f"<a>{a}</a>" if a else ""}</div>'
def chips(xs):return '<b class="chipset">'+''.join(f'<i class="chip" style="font-style:normal">{x}</i>' for x in xs)+'</b>'
def tg(t,lv,lvc,stt,on,lock=False):return f'<div class="tg"><span class="m"><b>{t}</b><small><span class="lv {lvc}">{lv}</span>{stt}</small></span><span class="sw {"on" if on else ""} {"lock" if lock else ""}"></span></div>'
def foldo(t,s,inner):return f'<div class="card acc"><div class="hd"><span>{t} <small>{s}</small></span>{sv("up")}</div>{inner}</div>'
def at(n,s,p,pc,y=False,x=False):return f'<div class="at"><div class="top"><b>{n}<small>{s}</small></b>{pill(p,pc)}</div><div class="bt"><span class="y {"on" if y else ""}">હાજર</span><span class="x {"on" if x else ""}">ગેરહાજર</span></div></div>'
REGS=[('પ્ર','પ્રજ્ઞેશકુમાર ભૂપેન્દ્રભાઈ ચૌધરી','SEVA-000018 · ૨, ૩, ૪ ફેબ્રુ.','','નવી','p-info','ટીમ —'),('ભ','ભરતભાઈ પ્રજાપતિ','SEVA-000013 · ૨, ૩ ફેબ્રુ.','','સમીક્ષા થઈ','p-ok','WhatsApp નિષ્ફળ'),('ર','રમેશભાઈ પટેલ','SEVA-000001 · ૨, ૩ ફેબ્રુ.','','સમીક્ષા થઈ','p-ok','સ્વાગત ટીમ'),('કિ','કિરણબેન શાહ','SEVA-000004 · ૨ ફેબ્રુ.','','સમીક્ષા થઈ','p-ok','પ્રસાદ ટીમ'),('સં','સંગીતાબેન રાઠોડ','SEVA-000016 · ૭ ફેબ્રુ.','','રદ','p-mut',''),('વિ','વિપુલભાઈ જોષી','SEVA-000017 · ૮ ફેબ્રુ.','','નવી','p-info','ટીમ —')]
def reglist(k=6):return card(''.join(rr(*r) for r in REGS[:k]))
HERO='<div class="hero"><b>મૂર્તિ પ્રાણ પ્રતિષ્ઠા મહોત્સવ</b><div class="cd"><span><strong>૭૭</strong>દિવસ બાકી</span><span>૨–૮ ફેબ્રુ. ૨૦૨૭</span></div><div class="chips"><span>સેવા નોંધણી બંધ</span><span>WhatsApp કતાર · ૧ રાહમાં</span></div></div>'
TODO=[('૩','','સ્વીકાર બાકી','નવી નોંધણી તપાસો'),('૫','','સેવા બાકી',''),('૧','','તારીખ-સમય નક્કી કરવાની પધરામણી',''),('૧','','પધરામણીમાં ફરી સંપર્ક બાકી',''),('૧','','લીડર બાકી','')]
KP='<div class="kpis"><div><small>કુલ નોંધણી</small><b>૧૬</b></div><div><small>સ્વીકારેલી</small><b>૧૩</b></div><div><small>રદ</small><b>૨</b></div></div>'
def lhead(t='એડમિન પેનલ'):return f'<div class="lhead"><img src="{LIGHT}" alt=""><b>શ્રી વિહત મેલડી ધામ</b><small>{t} · સાણંદ</small></div>'
def LP(inner):return f'<div class="ph"><div class="login">{lhead()}<div class="lform">{inner}</div></div></div>'
SEGR=['બધી ૧૮','નવી ૩','સમીક્ષા ૧૩','રદ ૨']
SRCH='<div class="search"><div class="in">'+sv('search')+'નામ, મોબાઇલ કે SEVA-નંબર</div><div class="ib" style="border-radius:12px;width:46px;height:46px">'+ic('filter')+'</div></div>'
DSUB=['૪','૯','૯','૨','૨','૧','૨'];WD=['મંગળ','બુધ','ગુરુ','શુક્ર','શનિ','રવિ','સોમ']
CCT='<div class="tiles"><div class="tile ok"><small>વેબસાઇટ</small><b>જાહેર</b></div><div class="tile bad"><small>નોંધણી</small><b>બંધ</b></div><div class="tile ok"><small>WhatsApp</small><b>ટેસ્ટ</b></div><div class="tile"><small>કતાર</small><b>૧ રાહમાં</b></div></div>'
REGBODY=SRCH+seg(SEGR)+days(0)+'<div class="count"><span>મંગળવાર, ૨ ફેબ્રુ. · ૪ નોંધણી</span><span style="color:var(--mar);font-weight:600">પસંદ કરો</span></div>'
PERSON='<div class="card idh"><span class="ph0">ર</span><span style="flex:1"><b>રમેશભાઈ પટેલ</b><small>અમદાવાદ · 90••••••10</small><span class="pill p-ok" style="margin-top:4px">સમીક્ષા થઈ</span></span></div>'

# ---------------- v5 layer ----------------
I.update({
 'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'phone':'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1z"/>',
 'user':'<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 'check':'<path d="M4 12l5 5L20 6"/>',
 'cal':'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 'note':'<path d="M5 4h14v16H5z"/><path d="M8 9h8M8 13h8M8 17h5"/>',
 'rupee':'<path d="M7 5h10M7 9h10M15 5c0 4-3 4-6 4l7 10"/>',
})
css+='''
/* ---- v5: colour, stat card, fact rows, timeline, fab ---- */
:root{--sa:#B65E1E;--sabg:#FDF0E4;--gr:#2F6B45;--grbg:#E9F2EC;--gd:#8A6A18;--gdbg:#FAF1D9;--bl:#2B5C8A;--blbg:#E9F1F8;--rz:#9C3A4E;--rzbg:#FAEBEE}
.cnt,.kv,.nextup,.qa,.tl{flex:none}
.ico{width:36px;height:36px;border-radius:11px;display:grid;place-items:center;flex:none;background:var(--sabg);color:var(--sa)}
.ico svg{width:19px;height:19px;fill:none;stroke:currentColor;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
.ico.g{background:var(--grbg);color:var(--gr)}.ico.d{background:var(--gdbg);color:var(--gd)}
.ico.b{background:var(--blbg);color:var(--bl)}.ico.r{background:var(--rzbg);color:var(--rz)}
/* stat card: ONE card, 2x2, hairlines */
.cnt{display:grid;grid-template-columns:1fr 1fr;gap:0;background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:0 1px 3px rgba(40,20,10,.06)}
.cnt div{background:none;border:0;border-radius:0;padding:12px 13px;display:grid;grid-template-columns:36px 1fr;grid-template-rows:auto auto;column-gap:10px;align-items:center}
.cnt div:nth-child(odd){border-right:1px solid var(--line)}
.cnt div:nth-child(-n+2){border-bottom:1px solid var(--line)}
.cnt .ico{grid-row:1/3;align-self:center}
.cnt b{font-size:23px;line-height:1.05;align-self:end}
.cnt small{font-size:12.5px;color:var(--mut);line-height:1.25;align-self:start}
/* fact rows replace the key/value table */
.kv{display:block;padding:0;background:var(--card);border:1px solid var(--line);border-radius:16px;box-shadow:0 1px 3px rgba(40,20,10,.06);overflow:hidden}
.kv .f{display:grid;grid-template-columns:36px 1fr;gap:12px;align-items:center;min-height:58px;padding:9px 14px;border-top:1px solid var(--line)}
.kv .f:first-child{border-top:0}
.kv .f u{text-decoration:none;display:block;min-width:0}
.kv .f span{display:block;font-size:12.5px;color:var(--mut);line-height:1.25}
.kv .f b{display:block;font-size:16px;font-weight:600;line-height:1.3;word-break:break-word}
.kv .f .chipset{display:flex;gap:6px;flex-wrap:wrap;margin-top:2px}
.kv .f b>.pill{display:inline-flex;width:auto}
/* next-up strip */
.nextup{display:flex;gap:12px;align-items:center;background:var(--gdbg);border:1px solid #ecdcb2;border-radius:16px;padding:11px 13px}
.nextup b{display:block;font-size:15.5px;line-height:1.3}
.nextup small{display:block;font-size:13px;color:#6b5a35;margin-top:2px}
/* quick action buttons */
.qa{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.qa div{background:var(--card);border:1px solid var(--line);border-radius:14px;min-height:68px;display:grid;justify-items:center;align-content:center;gap:5px;font-size:12.5px;font-weight:600;color:var(--ink);box-shadow:0 1px 3px rgba(40,20,10,.06)}
.qa .ico{width:30px;height:30px;border-radius:9px}.qa .ico svg{width:17px;height:17px}
/* timeline */
.tl{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:12px 14px;display:grid;gap:0;box-shadow:0 1px 3px rgba(40,20,10,.06)}
.tl div{display:grid;grid-template-columns:20px 1fr auto;gap:10px;align-items:start;padding:7px 0;position:relative}
.tl div i{width:12px;height:12px;border-radius:50%;border:2px solid #d2c6b2;background:#fff;margin-top:4px;z-index:1}
.tl div.d i{background:var(--gr);border-color:var(--gr)}.tl div.c i{border-color:var(--mar);box-shadow:0 0 0 3px #f6e5e8}
.tl div:not(:last-child)::after{content:"";position:absolute;left:5px;top:20px;bottom:-4px;width:2px;background:#e6dcca}
.tl b{font-size:15px;font-weight:600}.tl small{font-size:12.5px;color:var(--mut);white-space:nowrap}
/* page purpose line */
.psub{background:#fff;border-bottom:1px solid var(--line);padding:0 16px 10px;font-size:13px;color:var(--mut);flex:none;line-height:1.35}
/* floating quick-add */
.fab{position:absolute;right:16px;bottom:92px;width:58px;height:58px;border-radius:50%;background:var(--mar);display:grid;place-items:center;box-shadow:0 8px 18px rgba(107,31,42,.35);z-index:5}
.fab svg{width:27px;height:27px;fill:none;stroke:#fff;stroke-width:2.2;stroke-linecap:round}
/* attendance row, compact */
.at{padding:10px 14px;display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;min-height:66px}
.at .top{display:block}.at .top b{display:block;font-size:16px}.at .top small{display:block;font-size:13px;color:var(--mut)}
.at .bt{display:flex;gap:0;border:1.5px solid var(--line);border-radius:12px;overflow:hidden;background:#fff}
.at .bt span{height:42px;min-width:62px;display:grid;place-items:center;font-size:14px;font-weight:700;color:var(--mut);border-radius:0;border:0}
.at .bt .y.on{background:var(--grbg);color:var(--gr)}.at .bt .x.on{background:var(--rzbg);color:var(--rz)}
.at .bt .y{border-right:1.5px solid var(--line)}
/* card preview: front and back side by side, the way the v11 design showed them */
.idpair{display:grid;grid-template-columns:1fr 1fr;gap:6px 12px;justify-items:center;flex:none}
.idpair small{font-size:12px;color:var(--mut);font-weight:600}
.idshot{width:170px;height:271px;border-radius:12px;display:block;box-shadow:0 6px 18px rgba(60,20,30,.22)}
/* the one action a row needs, inside the row (Zoho People does this on approval rows) */
.rr .s .qbtn{display:block;margin-top:7px;background:var(--mar);color:#fff;font-size:12.5px;font-weight:700;padding:10px 12px;border-radius:10px;line-height:20px;white-space:nowrap}
.idcard.sm{width:170px;height:271px}
.idcard.sm .h{padding:8px 6px 20px;font-size:9.5px}
.idcard.sm .h b{font-size:11px}
.idcard.sm .h img,.idcard.sm .h i{width:24px;height:24px}
.idcard.sm .p{width:64px;height:78px;border-radius:32px 32px 8px 8px;font-size:18px;margin:-16px auto 0}
.idcard.sm .n{font-size:13px}
.idcard.sm .r{font-size:10px}
.idcard.sm .b{font-size:10px;padding:6px 8px;gap:6px}
.idcard.sm .b i{width:34px;height:34px}
.idcard.bk .h{padding:8px 6px}
.idcard.bk .bd{padding:12px 10px;text-align:center;font-size:10.5px;line-height:1.55;color:var(--ink)}
.idcard.bk .bd b{display:block;font-size:12px;margin:5px 0}
/* v5.1 — nothing on a screen below 12px (the printed ID card and the sheet's own labels excepted) */
.bar .t small{font-size:12px}
.nav div{font-size:12px}
.nav em{font:600 11px/17px "Hind Vadodara";min-width:17px;height:17px;border-radius:9px}
.days span small{font-size:12px}
.rr .s small{font-size:12px}
.tile small{font-size:12px}
.sum small{font-size:12px}
.cal .h{font-size:12px}
.newtag{font-size:12px}
.lv{font-size:11.5px}
.rail div{font-size:11.5px}
.cnt small{font-size:12.5px}
/* tab and filter strips really scroll sideways; they are not just cut off */
.tabs{overflow-x:auto;overflow-y:hidden;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.lockb{display:inline-flex;align-items:center;gap:5px;opacity:.55}
.lockb svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:2}
'''
TINT=['','g','d','b']
CICO=['pin','clock','check','bell']
def cnt(xs):
    out=''
    for i,x in enumerate(xs):
        hi=len(x)>2 and x[2]
        icn=x[3] if len(x)>3 else CICO[i%4]
        t='d' if hi else TINT[i%4]
        out+=f'<div><i class="ico {t}">{ic(icn)}</i><b>{x[0]}</b><small>{x[1]}</small></div>'
    return '<div class="cnt">'+out+'</div>'
FKEY=[(('ઉપલબ્ધતા','સમય','તારીખ','નોંધણી સમય','હમણાં'),'clock','b'),
      (('સ્થળ','સરનામું','ગામ','શહેર'),'pin',''),
      (('મોબાઇલ','ફોન','સંપર્ક'),'phone','g'),
      (('ભક્ત','વિનંતી','સ્વયંસેવક','લીડ','આપનાર','વપરાશકર્તા'),'user',''),
      (('WhatsApp','સંદેશ','ટેમ્પલેટ','Meta','મોકલ','લિંક'),'msg','g'),
      (('ડેપ્યુટી','કોણ','આપનાર','નામ'),'user',''),
      (('સ્તર','ખાનગી','પરવાનગી'),'lock','r'),
      (('મર્યાદા','ક્ષમતા'),'check','d'),
      (('ટીમ','સેવા','ફાળવણી','વર્ણન'),'dash','d'),
      (('સ્થિતિ','હાલ','સંમતિ','પ્રયાસ','જવાબ'),'check','r')]
def fico(k):
    for keys,icn,t in FKEY:
        for kk in keys:
            if kk in k: return icn,t
    return 'note','d'
def kv(xs):
    out=''
    for k,v in xs:
        icn,t=fico(k)
        out+=f'<div class="f"><i class="ico {t}">{ic(icn)}</i><u><span>{k}</span><b>{v}</b></u></div>'
    return '<div class="kv">'+out+'</div>'
def nextup(t,s,icn='clock'):
    return f'<div class="nextup"><i class="ico d">{ic(icn)}</i><span><b>{t}</b><small>{s}</small></span></div>'
QT={'phone':'g','msg':'g','pin':'','cal':'b','print':'d','qr':'d','eye':'b','user':''}
def qa(xs):
    return '<div class="qa">'+''.join(f'<div><i class="ico {QT.get(k,"")}">{ic(k)}</i>{t}</div>' for k,t in xs)+'</div>'
def tl(xs):
    return '<div class="tl">'+''.join(f'<div class="{st}"><i></i><b>{t}</b><small>{w}</small></div>' for t,w,st in xs)+'</div>'
def at(n,s,p,pc,y=False,x=False):
    return f'<div class="at"><div class="top"><b>{n}</b><small>{s}</small></div><div class="bt"><span class="y {"on" if y else ""}">હાજર</span><span class="x {"on" if x else ""}">ગેરહાજર</span></div></div>'
_rr0=rr
def rr(av,name,l1,l2,pill,pc,right=''):
    h=_rr0(av,name,l1,l2,pill,pc,right)
    if pill=='નવી':
        i=h.rfind('</span></div>')
        h=h[:i]+'<span class="qbtn">સ્વીકારો</span>'+h[i:]
    return h
SUBS={'ડેશબોર્ડ':'મહોત્સવની આજની સ્થિતિ અને આજે કરવાનાં કામ',
 'સેવા નોંધણીઓ':'વેબસાઇટ પરથી આવેલી સેવા નોંધણી',
 'પધરામણી':'ભક્તોના ઘર અને દુકાને બાપા/ભુવાજીની પધરામણી',
 'નોંધણી નિયંત્રણ':'નવી નોંધણી ચાલુ છે કે બંધ, અને શા માટે',
 'નિયંત્રણ કેન્દ્ર':'બધા ચાલુ/બંધ સ્વિચ એક જગ્યાએ',
 'WhatsApp સંદેશા':'કયો સંદેશ કોને ગયો, કતાર અને મર્યાદા',
 'ભક્ત યાદી':'મંદિરની કાયમી ભક્ત નોંધણી',
 'સેવા યાદી':'મહોત્સવની સેવાઓ અને જરૂરી સંખ્યા',
 'ટીમ':'દરેક સેવાની ટીમ, લીડર અને સભ્યો',
 'ઓળખકાર્ડ':'સેવા ઓળખપત્ર છાપો અને સોંપો',
 'મહોત્સવ દિવસ · હાજરી':'QR કે નામથી હાજરી નોંધો',
 'અહેવાલ':'નોંધણી, એડમિન અને વેબસાઇટના આંકડા',
 'સેટિંગ':'પેનલની ગોઠવણ, વપરાશકર્તા અને ઓડિટ',
 'નિમંત્રણ':'ગામ પ્રમાણે નિમંત્રણ અને કાર્ડ વિતરણ'}
FABS={'સેવા નોંધણીઓ':1,'પધરામણી':1,'ભક્ત યાદી':1,'સેવા યાદી':1,'ટીમ':1}
def P(sm,title,body,n=None,right=('search','bell'),back=False,foot='',over='',pre=''):
    sub=f'<div class="psub">{SUBS[title]}</div>' if (not back and title in SUBS) else ''
    fb=f'<div class="fab">{ic("plus")}</div>' if (n is not None and not over and title in FABS) else ''
    if fb: right=tuple(('search' if k=='plus' else k) for k in right)
    return f'<div class="ph">{pre}{bar3(sm,title,right,back)}{sub}<div class="body">{body}</div>{foot}{fb}{nav(n) if n is not None else ""}{over}</div>'
# ------------- end v5 layer -------------

S={}
S['A · લૉગિન']=[
('લૉગિન','ઉપર મંદિરનો લોગો અને નામ; એક જ મોટું બટન.',LP('<h3>એડમિન લૉગિન</h3>'+fl('વપરાશકર્તા નામ')+fl('પાસવર્ડ','••••••••',hint='')+'<span class="btn pri">લૉગિન</span><span class="link">પાસવર્ડ કે ચકાસણી કોડ ખોવાઈ ગયો?</span>'+note('આ ખાનગી વ્યવસ્થાપન ક્ષેત્ર છે. દરેક કાર્ય ઓડિટ ઇતિહાસમાં નોંધાય છે.'))),
('બીજું પગલું · ચકાસણી કોડ','૬ મોટાં ખાનાં; આંકડાનું કીબોર્ડ ખૂલે.',LP('<h3>ચકાસણી કોડ</h3>'+note('ઓથેન્ટિકેટર એપનો ૬ અંકનો કોડ લખો.')+'<div class="otp"><span>૪</span><span>૧</span><span>૭</span><span></span><span></span><span></span></div><span class="btn pri">ચકાસો</span><span class="link">રિકવરી કોડ વાપરો</span>')),
('ખોટો પાસવર્ડ','ભૂલ ફોર્મની ઉપર, સાદા શબ્દોમાં.',LP('<h3>એડમિન લૉગિન</h3><div class="err">નામ કે પાસવર્ડ ખોટો છે. ફરી પ્રયત્ન કરો.</div>'+fl('વપરાશકર્તા નામ','admin',False)+fl('પાસવર્ડ','••••••')+'<span class="btn pri">લૉગિન</span><span class="link">પાસવર્ડ કે ચકાસણી કોડ ખોવાઈ ગયો?</span>')),
('રિકવરી કોડ','એક ખાનું; કોડ એક જ વાર ચાલે.',LP('<h3>રિકવરી કોડ</h3>'+note('સાચવી રાખેલા રિકવરી કોડમાંથી એક લખો. દરેક કોડ એક જ વાર ચાલે.')+fl('રિકવરી કોડ','xxxx-xxxx')+'<span class="btn pri">ચકાસો</span><span class="link">પાછા: ચકાસણી કોડ</span>')),
('પાસવર્ડ ખોવાયો','શું કરવું તે ૩ પગલાંમાં.',LP('<h3>પાસવર્ડ ખોવાયો</h3>'+card(''.join(f'<div class="row"><span class="n">{n}</span><span class="l" style="font-weight:500">{t}</span></div>' for n,t in [('૧','સુપર એડમિનનો સંપર્ક કરો.'),('૨','તેઓ તમારો પાસવર્ડ ફરી સેટ કરશે.'),('૩','નવા પાસવર્ડથી લૉગિન કરી તેને બદલો.')]))+'<span class="btn">લૉગિન પર પાછા</span>')),
]
S['B · ડેશબોર્ડ, સૂચનાઓ, શોધ, મેનુ']=[
('ડેશબોર્ડ','ત્રણ જ વસ્તુ: મહોત્સવ, આજે કરવાનું, ઝડપી કામ. ચાર્ટ «અહેવાલ»માં.',P('','ડેશબોર્ડ',HERO+cnt([('૧૮','કુલ નોંધણી',0,'reg'),('૧૩','સ્વીકારેલી',0,'check'),('૩','સ્વીકાર બાકી',1,'bell'),('૨','પધરામણી',0,'pin')])+sec('આજે કરવાનું')+rows(TODO[:4]),0)),
('સૂચનાઓ (ઘંટડી)','નીચેથી ખૂલતી શીટ; હરોળ દબાવો તો સીધું કામ.',P('શ્રી વિહત મેલડી ધામ','ડેશબોર્ડ',HERO,0,over=sheet('સૂચનાઓ',rows([('૩','','નવી નોંધણી સ્વીકાર બાકી',''),('૧','','પધરામણી: આજે ફરી સંપર્ક',''),('૨','r','WhatsApp પુષ્ટિ પહોંચી નથી','')])+'<span class="btn">બંધ કરો</span>'))),
('શોધ','ખૂલતાં જ કીબોર્ડ; નોંધણી, ભક્ત અને પધરામણી એક સાથે.',P('બધે શોધો','શોધ','<div class="search"><div class="in" style="color:var(--ink)">'+sv('search')+'રમેશ</div></div>'+lab('નોંધણી · ૨')+card(rr(*REGS[2])+rr('ર','રમેશભાઈ સોલંકી','SEVA-000011 · અમદાવાદ','૮ ફેબ્રુ. · આખો દિવસ','સમીક્ષા થઈ','p-ok'))+lab('ભક્ત · ૧')+card(rr('ર','રમેશભાઈ પટેલ','DEV-000003 · 90••••••10','','સક્રિય','p-ok'))+lab('પધરામણી · ૦')+note('આ નામની કોઈ પધરામણી નથી.'),None,(),True)),
('«વધુ» મેનુ','લોગો સાથે; ચિહ્નવાળાં ખાનાં, જૂથ પ્રમાણે.',None),
]
S['C · સેવા નોંધણી']=[
('નોંધણી યાદી','ત્રણ પાતળી પટ્ટી, પછી તરત નામ; ૬ નામ એક સ્ક્રીન પર.',P('કામ · ૧૮ નોંધણી','સેવા નોંધણીઓ',REGBODY+reglist(5),1,('dl','bell'))),
('ફિલ્ટર','બધાં ફિલ્ટર એક શીટમાં; યાદી ઉપર ભીડ નહીં.',P('કામ · ૧૮ નોંધણી','સેવા નોંધણીઓ',REGBODY,1,('dl','bell'),over=sheet('ફિલ્ટર',lab('સેવા')+tabs(['બધી','સેવા બાકી','સ્વાગત','ભોજન-પ્રસાદ','જળ સેવા'])+lab('WhatsApp સંદેશ')+tabs(['બધા','પહોંચ્યો','નિષ્ફળ','કોઈ સંદેશ નથી'])+lab('ફોટો')+seg(['બધા','ફોટો બાકી'])+lab('સમય')+seg(['બધા','સવાર','બપોર','આખો દિવસ'])+lab('ક્રમ')+seg(['નવી પહેલાં','નામ','SEVA નંબર'])+bt('સાફ કરો','૪ નોંધણી બતાવો')))),
('ઘણી પસંદ કરવી','«પસંદ કરો» દબાવ્યા પછી જ ટિક દેખાય; કામ નીચેની પટ્ટીમાં.',f'<div class="ph">{bar3("૨ પસંદ કર્યા","પસંદ કરો",(),True)}<div class="body">'+card(''.join(f'<div class="rr"><span class="cb {"on" if i<2 else ""}">{"✓" if i<2 else ""}</span><span class="m"><b>{r[1]}</b><small>{r[2]}</small><small>{r[3]}</small></span><span class="s">{pill(r[4],r[5])}</span></div>' for i,r in enumerate(REGS)))+'</div><div class="selbar"><span>૨ પસંદ કર્યા</span><b>સ્વીકારો</b><b style="background:transparent;color:#fff;border:1px solid rgba(255,255,255,.4)">સેવા સોંપો</b></div></div>'),
('નોંધણીની વિગત','આખી સ્ક્રીન; «સ્વીકારો» હંમેશાં નીચે.',P('SEVA-000001 · સમીક્ષા થઈ','નોંધણીની વિગત',PERSON+cnt([('૨ દિવસ','ઉપલબ્ધતા',0,'clock'),('બાકી','સેવા ફાળવણી',1,'dash'),('ગયો','WhatsApp સંદેશ',0,'msg'),('બાકી','ઓળખકાર્ડ',0,'reg')])+nextup('સમીક્ષા થઈ ગઈ છે — હવે સ્વીકારવાનું બાકી','સ્વીકાર્યા પછી ભક્તને WhatsApp પર જાણ થશે','check')+qa([('phone','ફોન'),('msg','WhatsApp'),('eye','ખાનગી'),('print','ઓળખકાર્ડ')])+kv([('ઉપલબ્ધતા',chips(['૩ ફેબ્રુ. સવાર','૪ ફેબ્રુ. બપોર']))])+acts(['સેવા અને ટીમ સોંપો','વિગત સુધારો','ફેરફાર ઇતિહાસ']),None,(),True,foot('રદ કરો','સ્વીકારો'))),
('સેવા અને ટીમ સોંપો','સેવા અને ટીમ અલગ; બંને હાથથી પસંદ થાય.',P('SEVA-000001','નોંધણીની વિગત',PERSON,None,(),True,over=sheet('સેવા અને ટીમ સોંપો',lab('સેવા')+tabs(['સ્વાગત','ભોજન-પ્રસાદ','જળ સેવા','પાર્કિંગ'],0)+lab('ટીમ')+card(''.join(f'<div class="row" style="min-height:48px"><span class="cb {"on" if i==0 else ""}" style="border-radius:50%">{"✓" if i==0 else ""}</span><span class="l" style="font-weight:500">{t}</span><span class="val">{v}</span></div>' for i,(t,v) in enumerate([('સ્વાગત ટીમ','૧ / ૫'),('પ્રસાદ સેવા ટીમ','૧ / ૫'),('ટીમ વગર','')])))+fl('કારણ (ઓડિટમાં રહેશે) *','કારણ લખો')+bt('રદ કરો','સોંપો')))),
('વિગત સુધારો','એક સાદી યાદી: શું બદલવું છે તે પસંદ કરો. ફોટો અને દિવસ પણ અહીંથી.',P('','વિગત સુધારો',PERSON+card('<div class="hd" style="display:flex;align-items:center;gap:12px;min-height:60px;padding:0 14px;font-weight:700">ફોટો</div>'+'<div style="display:flex;gap:12px;align-items:center;padding:0 14px 14px"><span style="width:62px;height:76px;border-radius:12px;font-size:24px;background:#f1e4c6;color:#7a5a10;font-weight:700;display:grid;place-items:center;border:2px solid #fff;box-shadow:0 2px 8px rgba(40,20,10,.15);flex:none">ર</span><span style="display:grid;gap:8px;flex:1"><span class="btn sm">નવો ફોટો લો</span><span class="btn sm">ફોટો કાઢો</span></span></div>')+card(''.join(f'<div class="fold" style="{"border-top:1px solid var(--line)" if i else ""}"><span>{t} <small>· {v}</small></span>{sv("down")}</div>' for i,(t,v) in enumerate([('નામ અને સંપર્ક','રમેશભાઈ પટેલ · અમદાવાદ'),('સેવાના દિવસ અને સમય','૩ ફેબ્રુ. સવાર · ૪ ફેબ્રુ. બપોર'),('નોંધણીની તારીખ અને સમય','૦૧/૧૨/૨૦૨૬, ૧૧:૩૨')])))+fl('કારણ (ઓડિટમાં રહેશે) *','કારણ લખો')+note('બધા ફેરફાર એક જ વાર «સાચવો»થી થાય છે અને ઓડિટમાં રહે છે.'),None,(),True,foot('રદ કરો','સાચવો'))),
('ફોટો બદલો','નવો ફોટો લો અથવા પસંદ કરો; મોટો પ્રિવ્યૂ. (નવું)',P('','ફોટો બદલો','<div class="photo">ર</div>'+'<span class="btn pri" style="flex:none">કૅમેરાથી ફોટો લો</span><span class="btn">ગેલેરીમાંથી પસંદ કરો</span><span class="btn" style="border-color:var(--bad);color:var(--bad)">ફોટો કાઢો</span>'+fl('કારણ (ઓડિટમાં રહેશે) *','કારણ લખો')+note('ફોટો ખાનગી રહે છે. તે નાનો કરીને સચવાય છે.'),None,(),True,foot('રદ કરો','સાચવો'))),
('સેવાના દિવસ અને સમય','દરેક દિવસ એક હરોળ; સમય ચાર બટનથી.',P('','દિવસ અને સમય',card(''.join(f'<div class="tg" style="display:grid;gap:6px"><b style="font-size:14.5px">{d} ફેબ્રુ. · {w}</b>{seg(["નહીં","સવાર","બપોર","આખો દિવસ"],o)}</div>' for d,w,o in [('૨','મંગળવાર',0),('૩','બુધવાર',1),('૪','ગુરુવાર',2),('૫','શુક્રવાર',0)]))+fl('કારણ *','કારણ લખો'),None,(),True,foot('રદ કરો','સાચવો'))),
('નામ અને સંપર્ક','એક કૉલમ, મોટાં ખાનાં; કારણ ફરજિયાત.',P('','નામ અને સંપર્ક',fl('પૂરું નામ','રમેશભાઈ પટેલ',False)+fl('મોબાઇલ','90••••••10',False,'બદલવા પૂરો નંબર લખો')+fl('ગામ / શહેર','અમદાવાદ',False)+fl('ઉંમર','•••',False)+fl('કારણ (ઓડિટમાં રહેશે) *','કારણ લખો',cls='ta'),None,(),True,foot('રદ કરો','સાચવો'))),
('સ્વીકારો · ખાતરી','નાની શીટ; શું થશે તે એક લીટીમાં.',P('SEVA-000018 · નવી','નોંધણીની વિગત',PERSON,None,(),True,over=sheet('નોંધણી સ્વીકારવી?','<div class="okb">સ્વીકાર્યા પછી ભક્તને WhatsApp પર જાણ થશે (સંમતિ હોય તો).</div>'+bt('રદ કરો','હા, સ્વીકારો')))),
('રદ કરો · કારણ','કારણ ગોળીથી પસંદ થાય અથવા લખાય.',P('SEVA-000018 · નવી','નોંધણીની વિગત',PERSON,None,(),True,over=sheet('નોંધણી રદ કરવી?','<div class="err">નોંધણી નંબર ફરી વપરાશે નહીં. ઇતિહાસ સચવાય છે.</div>'+lab('કારણ *')+'<div class="chipset">'+''.join(f'<span class="tabs" style="margin:0;padding:0;-webkit-mask-image:none"><span>{x}</span></span>' for x in ['ભક્તે ના પાડી','બે વાર નોંધણી','ખોટી વિગત','અન્ય'])+'</div>'+fl('નોંધ','વધુ વિગત (વૈકલ્પિક)')+bt('પાછા','હા, રદ કરો',True)))),
('ફોટો અને સંપર્ક બતાવો','ખાનગી વિગત માગો ત્યારે જ; જોયાની નોંધ.',P('SEVA-000001','નોંધણીની વિગત',PERSON,None,(),True,over=sheet('ખાનગી વિગત બતાવવી?','<div class="infob">પૂરો મોબાઇલ, સરનામું, ઉંમર અને ફોટો દેખાશે. કોણે ક્યારે જોયું તેની નોંધ ઓડિટમાં રહેશે.</div>'+bt('રદ કરો','બતાવો')))),
]
S['D · નોંધણી નિયંત્રણ']=[
('નોંધણી નિયંત્રણ','આજે ૭ સ્ક્રીન; હવે હાલની સ્થિતિ અને ૪ બંધ પટ્ટી.',P('કામ','નોંધણી નિયંત્રણ','<div class="err" style="display:flex;justify-content:space-between;align-items:center">બંધ — નવી નોંધણી સ્વીકારાતી નથી<span class="pill p-bad">બંધ</span></div>'+card(''.join(f'<div class="row" style="min-height:52px"><span class="n {c}">{n}</span><span class="l">{t}<small>{s}</small></span>{pill(p,pc)}</div>' for n,c,t,s,p,pc in [('૧','r','વેબસાઇટ પરનું નોંધણી સ્વિચ','વેબસાઇટ ખાનગી છે','રોકે છે','p-bad'),('૨','','હાથે બંધ કરવું','','રોકતું નથી','p-ok'),('૩','','ક્ષમતા (મર્યાદા)','જગ્યા બાકી છે','રોકતું નથી','p-ok')]))+foldo('દૈનિક સ્વીકાર મર્યાદા','નક્કી નથી','<div class="tg"><span class="m"><b>દરરોજ મહત્તમ નવી નોંધણી</b><small>આજે ૧૮</small></span><span class="step"><span>−</span><b>—</b><span>+</span></span></div>')+card(f'<div class="fold"><span>કુલ મર્યાદા <small>· નક્કી નથી</small></span>{sv("down")}</div><div class="fold" style="border-top:1px solid var(--line)"><span>મહોત્સવના દિવસ <small>· ૭ ખુલ્લા</small></span>{sv("down")}</div><div class="fold" style="border-top:1px solid var(--line)"><span>ફેરફાર ઇતિહાસ</span>{sv("down")}</div>')+note('ચાલુ/બંધ સ્વિચ «નિયંત્રણ કેન્દ્ર»માં છે.'),2)),
('મહોત્સવના દિવસ','દરેક દિવસ એક હરોળ: ખુલ્લો/બંધ અને બે સમયની મર્યાદા.',P('નોંધણી નિયંત્રણ','મહોત્સવના દિવસ',days(0,WD)+card('<div class="tg"><span class="m"><b>૨ ફેબ્રુઆરી · મંગળવાર</b><small>વેબસાઇટ પર બુકિંગ</small></span><span class="sw on"></span></div>'+''.join(f'<div class="tg" style="display:grid;gap:6px"><div style="display:flex;align-items:center;gap:10px"><span class="m"><b>{t}</b><small>સોંપાયેલા {a} · મર્યાદા નક્કી નથી</small></span><span class="step"><span>−</span><b>—</b><span>+</span></span></div></div>' for t,a in [('સવારથી બપોર સુધી','૪'),('બપોરથી રાત સુધી','૨')]))+note('બંધ દિવસ ફોર્મ પર ગ્રે દેખાશે. ફેરફાર માટે કારણ પૂછાશે.'),None,(),True)),
]
S['E · નિયંત્રણ કેન્દ્ર']=[
('નિયંત્રણ કેન્દ્ર','૫ વિભાગ બંધ પટ્ટીમાં, દરેક પર સાર.',P('કામ','નિયંત્રણ કેન્દ્ર',CCT+''.join(card(f'<div class="acc"><div class="hd"><span>{t} <small>{s}</small></span>{sv("down")}</div></div>') for t,s in [('વેબસાઇટ','જાહેર · ૭ વિભાગ ચાલુ'),('સેવા નોંધણી','બંધ'),('WhatsApp','ટેસ્ટ મોડ · મોકલવાનું ચાલુ'),('મોડ્યુલ','૪ ચાલુ · ૨ બંધ'),('સિસ્ટમ સ્થિતિ','બધું બરાબર')]),2)),
('વેબસાઇટ વિભાગ ખુલ્લો','ટૉગલ હરોળ ૫૮ px; સ્તર નાના લેબલમાં.',P('કામ','નિયંત્રણ કેન્દ્ર',CCT+foldo('વેબસાઇટ','જાહેર',tg('વેબસાઇટ જાહેર','માલિક સ્તર','o','જાહેર',True)+tg('ઇમરજન્સી ખાનગી','ફક્ત સ્થિતિ','n','બંધ · Render માં જ બદલાય',False,True)+tg('ઉદ્ઘાટન સમારોહ પેજ','માલિક સ્તર','o','બંધ',False)+f'<div class="tg"><span class="m"><b>વિભાગ બતાવો / છુપાવો</b><small>૭ માંથી ૭ ચાલુ</small></span>{sv("chev")}</div>')+card(f'<div class="acc"><div class="hd"><span>સેવા નોંધણી <small>· બંધ</small></span>{sv("down")}</div></div>'),2)),
('ખાતરી (ટૉગલ બદલતાં)','કોડ અને «હા» એક લીટીમાં; બટન હંમેશાં દેખાય.',P('કામ','નિયંત્રણ કેન્દ્ર',CCT,2,over=sheet('વેબસાઇટ જાહેર: ચાલુ → બંધ?','<div class="warnb">મુલાકાતીઓને તરત «ટૂંક સમયમાં» પાનું દેખાશે. સેવા નોંધણી પણ બંધ થશે.</div>'+fl('કારણ (ઓડિટમાં રહેશે) *','કારણ લખો')+'<div class="two">'+fl('ચકાસણી કોડ *','• • • • • •')+fl('"હા" લખો *','')+'</div>'+bt('રદ કરો','હા, બંધ કરો')))),
('તાળાવાળો ટૉગલ','કેમ બંધ છે અને ક્યાંથી બદલાય તે સાદા શબ્દોમાં.',P('કામ','નિયંત્રણ કેન્દ્ર',CCT,2,over=sheet('સાચું મોકલવું (Live)',kv([('હાલની સ્થિતિ',pill('ટેસ્ટ મોડ','p-warn')),('સ્તર','માલિક સ્તર'),('કોણ બદલી શકે','સુપર એડમિન')])+'<div class="warnb">હમણાં બદલી શકાતું નથી: Cloud API સેટ નથી (સર્વર મર્યાદા).</div>'+lab('તાજેતરના ફેરફાર')+note('હજી કોઈ ફેરફાર નથી.')+'<span class="btn">બંધ કરો</span>'))),
('ઇમરજન્સી સ્ટોપ ચાલુ','લાલ પટ્ટી ઉપર ચોંટેલી; નોંધણી ચાલુ છે તે લખેલું.',P('કામ','નિયંત્રણ કેન્દ્ર','<div class="err">WhatsApp ઇમરજન્સી સ્ટોપ ચાલુ છે. કોઈ સંદેશ જતો નથી; નોંધણી ચાલુ છે.</div>'+CCT.replace('<div class="tile ok"><small>WhatsApp</small><b>ટેસ્ટ</b>','<div class="tile bad"><small>WhatsApp</small><b>સ્ટોપ</b>')+foldo('WhatsApp','ઇમરજન્સી સ્ટોપ',tg('સંદેશા મોકલવાનું','તરત','n','ઇમરજન્સી સ્ટોપ ચાલુ છે',False,True)+f'<div class="tg"><span class="m"><b>ઇમરજન્સી સ્ટોપ</b><small><span class="lv n">તરત</span>ચાલુ</small></span><span class="sw on" style="background:var(--bad)"></span></div>'+f'<div class="tg"><span class="m"><b>સંદેશ કતાર</b><small>૧ રાહમાં · કંઈ ખોવાતું નથી</small></span>{sv("chev")}</div>'),2)),
]
QROWS=[('૧','','રાહમાં',''),('૨','r','નિષ્ફળ',''),('૧','r','પરિણામ અજાણ્યું',''),('૨','','પહોંચ્યા','')]
WT=['સ્થિતિ','કતાર <small>૧</small>','ઝુંબેશ','ટેમ્પલેટ','સંમતિ નોંધ']
def q(n,s,t,p,pc):return rr(n[0],n,s,t,p,pc)
S['F · WhatsApp સંદેશા']=[
('WhatsApp · સ્થિતિ','મોડ, ૨૪ કલાકની મર્યાદા અને કતારનો સાર એક સ્ક્રીન પર.',P('કામ','WhatsApp સંદેશા',tabs(WT)+card('<div style="display:flex;justify-content:space-between;align-items:center"><b>કયો સંદેશ આપમેળે જાય</b>'+pill('ટેસ્ટ મોડ','p-warn')+'</div>'+seg(['નોંધણી','નિમંત્રણ','થોભાવેલ'],2)+note('થોભાવેલ: કોઈ સંદેશ જતો નથી; કતાર સચવાય છે. નોંધણી ચાલુ રહે.'),'padding:12px;display:grid;gap:8px')+card('<div style="display:flex;justify-content:space-between"><b>છેલ્લા ૨૪ કલાક</b><span>૦ / ૨૦૦</span></div><div class="meter"><i style="width:2%"></i></div>'+note('નોંધણી માટે અનામત ૫૦'),'padding:12px;display:grid;gap:6px')+sec('કતાર','બધું જુઓ')+rows(QROWS[:3])+acts(['મર્યાદા અને સમજૂતી']),4)),
('કતાર અને ફરી પ્રયાસ','ઉપર બે કામ, પછી સ્થિતિ ફિલ્ટર, પછી સંદેશા.',P('કામ','WhatsApp સંદેશા',tabs(WT,1)+'<div class="okb">WhatsApp ની ક્ષમતા પૂરી થાય તો પણ સેવા નોંધણી ચાલુ રહે છે.</div><div class="two"><span class="btn sm">કતાર રોકો</span><span class="btn sm" style="border-color:var(--bad);color:var(--bad)">ઇમરજન્સી સ્ટોપ</span></div>'+tabs(['બધા <small>૧૧</small>','રાહમાં <small>૧</small>','નિષ્ફળ <small>૨</small>','અજાણ્યું <small>૧</small>','પહોંચ્યા'])+card(q('જયંતીભાઈ રાવળ','SEVA-000007 · નોંધણી મળી','આજે ૧૧:૩૨','રાહમાં','p-info')+q('ભરતભાઈ પ્રજાપતિ','SEVA-000013 · નોંધણી સ્વીકાર','ગઈકાલે ૧૮:૦૫ · ૧૩૧૦૨૬','નિષ્ફળ','p-bad')+q('નીતાબેન ત્રિવેદી','SEVA-000014 · નોંધણી મળી','ગઈકાલે ૧૭:૪૦','અજાણ્યું','p-warn')+q('અશોકભાઈ મકવાણા','SEVA-000015 · નોંધણી સ્વીકાર','ગઈકાલે ૧૬:૧૦','પહોંચ્યો','p-ok')+q('રમેશભાઈ પટેલ','SEVA-000001 · સેવા ફાળવણી','૨૯ નવે.','પહોંચ્યો','p-ok')),4)),
('સંદેશની વિગત','સમયરેખા અને ફક્ત સલામત કામ.',P('SEVA-000013 · નોંધણી સ્વીકાર','સંદેશની વિગત',kv([('ભક્ત','ભરતભાઈ પ્રજાપતિ'),('સ્થિતિ',pill('નિષ્ફળ','p-bad')),('ટેમ્પલેટ','registration_confirmed'),('Meta જવાબ','૧૩૧૦૨૬ · પહોંચાડી ન શકાયો'),('પ્રયાસ','૧ / ૬')])+lab('સમયરેખા')+card(''.join(f'<div class="row" style="min-height:46px"><span class="l" style="font-weight:500">{t}</span><span class="val">{v}</span></div>' for t,v in [('કતારમાં મુકાયો','૧૮:૦૪'),('મોકલવાનો પ્રયાસ','૧૮:૦૫'),('Meta એ નકાર્યો','૧૮:૦૫')]))+'<div class="warnb">આ ભૂલમાં આપમેળે ફરી પ્રયાસ થતો નથી. નંબર તપાસો.</div>',None,(),True,foot('નોંધણી ખોલો','ફરી મોકલો'))),
('ઝુંબેશ','દરેક ઝુંબેશ એક હરોળ, પ્રગતિ સાથે.',P('કામ','WhatsApp સંદેશા',tabs(WT,2)+card(''.join(f'<div class="tg" style="display:grid;gap:6px"><div style="display:flex;justify-content:space-between;gap:8px"><b style="font-size:14.5px">{t}</b>{pill(p,pc)}</div><small style="color:var(--mut);font-size:12.5px">{s}</small><div class="meter"><i style="width:{w}%"></i></div></div>' for t,s,p,pc,w in [('મહોત્સવ નિમંત્રણ · સાણંદ','૧૨૦ માંથી ૪૫ મોકલાયા · રોજ ૧૫૦ સુધી','ચાલુ','p-ok',38),('ગામ યાદી · બાવળા','તપાસ બાકી · ૮૦ સંપર્ક','ડ્રાફ્ટ','p-mut',0)]))+'<span class="btn">+ નવી ઝુંબેશ</span>',4)),
('ટેમ્પલેટ','મંજૂર અને નકારેલા અલગ રંગમાં; દબાવો તો લખાણ.',P('કામ','WhatsApp સંદેશા',tabs(WT,3)+card(''.join(f'<div class="row" style="min-height:52px"><span class="l" style="font-weight:600;font-size:13.5px">{t}<small>{s}</small></span>{pill(p,pc)}</div>' for t,s,p,pc in [('registration_received_v2','નોંધણી મળી · ૩ વિગત','મંજૂર','p-ok'),('registration_confirmed','સ્વીકાર · ૩ વિગત','મંજૂર','p-ok'),('registration_corrected','સુધારો · ૩ વિગત','મંજૂર','p-ok'),('registration_cancelled','રદ · ૨ વિગત','મંજૂર','p-ok'),('assignment_update','સેવા ફાળવણી · ૫ વિગત','મંજૂર','p-ok'),('card_ready_v2','ઓળખકાર્ડ તૈયાર · ૫ વિગત','મંજૂર','p-ok'),('seva_reminder','સેવા યાદ · ૫ વિગત','મંજૂર','p-ok'),('card_ready','જૂનો','નકારેલો','p-bad')])),4)),
('સંમતિ નોંધ','કોણે ક્યારે હા કે ના કહી; ફક્ત વાંચવા.',P('કામ','WhatsApp સંદેશા',tabs(WT,4)+'<div class="search"><div class="in">'+sv('search')+'નામ કે SEVA-નંબર</div></div>'+card(q('રમેશભાઈ પટેલ','SEVA-000001 · ફોર્મમાં ટિક','૦૧/૧૨/૨૦૨૬','સંમતિ છે','p-ok')+q('સંગીતાબેન રાઠોડ','SEVA-000016 · STOP મોકલ્યું','૩૦/૧૧/૨૦૨૬','બંધ','p-bad')+q('વિપુલભાઈ જોષી','SEVA-000017 · ફોર્મમાં ટિક નથી','૦૧/૧૨/૨૦૨૬','સંમતિ નથી','p-mut')),4)),
]
S['F · WhatsApp સંદેશા']+=[
('મર્યાદા અને મોકલનાર','ત્રણ અલગ બાબત અલગ કાર્ડમાં; બદલવાનું એક જ બટન.',P('WhatsApp સંદેશા','મર્યાદા અને મોકલનાર',card('<div style="display:flex;justify-content:space-between"><b>પેનલની મર્યાદા</b><span>૦ / ૨૦૦</span></div><div class="meter"><i style="width:2%"></i></div>'+note('છેલ્લા ૨૪ કલાક (સરકતી ગણતરી). નોંધણી માટે અનામત ૫૦.'),'padding:12px;display:grid;gap:6px')+kv([('Meta ની મર્યાદા','તપાસેલી નથી'),('મોકલનાર','ટેસ્ટ મોડ · ૧ મંજૂર નંબર'),('સાચું મોકલવું','બંધ (નિયંત્રણ કેન્દ્ર)')])+'<div class="infob">ગ્રાહક-સેવા વિન્ડો (૨૪ કલાક) અલગ છે: નોંધણીના સંદેશા મંજૂર ટેમ્પલેટ છે, એટલે તેની જરૂર નથી.</div>',None,(),True,foot('','મર્યાદા બદલો'))),
('સમજૂતી','લાંબું લખાણ અહીં; રોજની સ્ક્રીન પર નહીં.',P('WhatsApp સંદેશા','સમજૂતી',lab('સંદેશનો પ્રવાહ')+card(''.join(f'<div class="row" style="min-height:48px"><span class="n">{n}</span><span class="l" style="font-size:14px">{t}<small>{x}</small></span></div>' for n,t,x in [('૧','નોંધણી સચવાય','WhatsApp ગમે તે સ્થિતિમાં હોય'),('૨','સંમતિ તપાસ','સંમતિ ન હોય તો સંદેશ બનતો નથી'),('૩','કતાર','એક ઘટના = એક સંદેશ'),('૪','ક્ષમતા મુજબ મોકલવું','જગ્યા ન હોય તો રાહ જુએ'),('૫','પરિણામ','પહોંચ્યો · ફરી પ્રયાસ · નિષ્ફળ')]))+lab('ફરી પ્રયાસના નિયમ')+card(''.join(f'<div class="row" style="min-height:46px"><span class="l" style="font-size:13.5px;font-weight:500">{t}</span><span class="val">{v}</span></div>' for t,v in [('કામચલાઉ ભૂલ','૧, ૫, ૧૫, ૬૦ મિનિટ'),('૧૩૧૦૪૯','૨૪ કલાક પછી એક વાર'),('૧૩૧૦૪૮','કતાર રોકાય'),('પરિણામ અજાણ્યું','આપમેળે ફરી નહીં')])),None,(),True)),
]
S['G · નિમંત્રણ']=[
('નિમંત્રણ · ૬ પગલાં','ઉપર ૬ પગલાંની પટ્ટી; હાલનું પગલું મોટું, બાકીના યાદીમાં.',P('કામ · મહોત્સવ નિમંત્રણ','નિમંત્રણ','<div class="stepper6"><span class="d"></span><span class="d"></span><span class="c"></span><span></span><span></span><span></span></div>'+card('<b>પગલું ૩ · તપાસ</b>'+note('૧૨૦ સંપર્ક · ૪ માં ભૂલ · ૨ એકસરખા')+'<span class="btn pri">તપાસ ખોલો</span>','padding:12px;display:grid;gap:8px')+card(''.join(f'<div class="row" style="min-height:50px"><span class="n {c}">{n}</span><span class="l">{t}<small>{s}</small></span>{pill(p,pc)}</div>' for n,c,t,s,p,pc in [('૧','','યાદી','૧૨૦ સંપર્ક','થયું','p-ok'),('૨','','સંમતિ','દરેક હરોળની સંમતિ','થયું','p-ok'),('૩','','તપાસ','૪ ભૂલ સુધારો','હવે','p-warn'),('૪','','મંજૂરી','ટ્રસ્ટની મંજૂરી','બાકી','p-mut'),('૫','','મોકલવું','રોજ ૧૫૦ સુધી','બાકી','p-mut'),('૬','','કાર્ડ વિતરણ','ગામ પ્રમાણે','બાકી','p-mut')])),4)),
('તપાસ','ભૂલવાળા સંપર્ક ઉપર; દરેક હરોળમાં સંમતિ દેખાય.',P('પગલું ૩','નિમંત્રણ · તપાસ','<div class="stepper6"><span class="d"></span><span class="d"></span><span class="c"></span><span></span><span></span><span></span></div>'+tabs(['ભૂલ <small>૪</small>','એકસરખા <small>૨</small>','બરાબર <small>૧૧૪</small>'])+card(rr('મ','મનુભાઈ પટેલ','નંબર ૯ અંકનો છે','સાણંદ','ભૂલ','p-bad')+rr('સ','સવિતાબેન','અટક નથી · સંમતિ છે','ગેપ્પરા','ભૂલ','p-bad')+rr('ર','રમેશભાઈ પટેલ','આ નંબર બે વાર છે','સાણંદ','એકસરખા','p-warn')+rr('જ','જશુભાઈ ઠાકોર','સંમતિ નથી → મોકલાશે નહીં','બાવળા','સંમતિ નથી','p-mut')),None,(),True,foot('પાછા','મંજૂરી માટે મોકલો'))),
('મોકલવું','રોજની મર્યાદા અને કેટલા દિવસ લાગશે તે ઉપર.',P('પગલું ૫','નિમંત્રણ મોકલવું','<div class="stepper6"><span class="d"></span><span class="d"></span><span class="d"></span><span class="d"></span><span class="c"></span><span></span></div>'+cnt([('૧૨૦','કુલ'),('૪૫','મોકલાયા'),('૭૫','બાકી'),('૧','દિવસ લાગશે')])+card('<div style="display:flex;justify-content:space-between"><b>આજે</b><span>૪૫ / ૧૫૦</span></div><div class="meter"><i style="width:30%"></i></div>'+note('૫૦ સંદેશ નોંધણી માટે અનામત રહે છે.'),'padding:12px;display:grid;gap:6px')+'<div class="warnb">ટેસ્ટ મોડ: ફક્ત મંજૂર નંબર પર જ જાય છે.</div>',None,(),True,foot('રોકો','આજના મોકલો'))),
('કાર્ડ વિતરણ','ગામ પ્રમાણે એક-એક કાર્ડ; કોને સોંપ્યા તે નોંધ.',P('પગલું ૬','કાર્ડ વિતરણ','<div class="stepper6"><span class="d"></span><span class="d"></span><span class="d"></span><span class="d"></span><span class="d"></span><span class="c"></span></div>'+card(''.join(f'<div class="tg" style="display:grid;gap:6px"><div style="display:flex;justify-content:space-between"><b style="font-size:14.5px">{g}</b>{pill(p,pc)}</div><small style="color:var(--mut);font-size:12.5px">{s}</small><div class="meter"><i style="width:{w}%"></i></div></div>' for g,s,p,pc,w in [('સાણંદ','૨૦૦ કાર્ડ · જવાબદાર: જયંતીભાઈ','આપ્યા','p-ok',100),('ગેપ્પરા','૧૨૦ માંથી ૬૦ વહેંચાયા','ચાલુ','p-warn',50),('બાવળા','૮૦ કાર્ડ · જવાબદાર નક્કી નથી','બાકી','p-mut',0)])),None,(),True)),
]
PT=['ચાલુ <small>૬</small>','સમય નક્કી કરવાનો <small>૧</small>','ફરી સંપર્ક <small>૧</small>','પૂર્ણ','રદ']
PC=cnt([('૧','સમય નક્કી કરવાનો',1),('૧','ફરી સંપર્ક',1),('૦','આજે'),('૩','આગામી')])
PH='<div class="card idh"><span class="ph0" style="height:60px;font-size:15px">૯:૦૦</span><span style="flex:1"><b>પટેલ સ્ટોર</b><small>દુકાનનું ઉદ્ઘાટન · બુધ, ૨ ડિસે.</small></span>'+pill('નક્કી','p-ok')+'</div>'
ST3='<div class="st3"><i class="d">✓</i>વિનંતી<u></u><i class="c">૨</i>તારીખ નક્કી<u></u><i>૩</i>પૂર્ણ</div>'
S['H · પધરામણી']=[
('પધરામણી · યાદી','ચાર આંકડા એક લીટીમાં; સમય ડાબે.',P('પધરામણી','પધરામણી',PC+seg(['યાદી','અઠવાડિયું','મહિનો'])+tabs(PT)+lab('બુધ, ૨ ડિસે.')+card(rr('૯:૦૦','પટેલ સ્ટોર','દુકાનનું ઉદ્ઘાટન · સાણંદ','','નક્કી','p-ok'))+lab('શનિ, ૫ ડિસે.')+card(rr('૧૬:૦૦','હેતલ પટેલ','ગૃહપ્રવેશ · સાણંદ','','નક્કી','p-ok'))+lab('તારીખ બાકી')+card(rr('—','કિરણ ઠાકોર','નવો વ્યવસાય · ચાંગોદર','માંગેલું: ૨૦ ડિસે. · સવારે','વિનંતી','p-info')),3,('plus','bell'))),
('અઠવાડિયું','૭ દિવસની પટ્ટી; દિવસ દબાવો તો તેની મુલાકાત.',P('પધરામણી','પધરામણી',seg(['યાદી','અઠવાડિયું','મહિનો'],1)+'<div class="count"><span class="link">‹ પાછળ</span><b>૩૦ નવે. – ૬ ડિસે.</b><span class="link">આગળ ›</span></div><div class="days">'+''.join(f'<span class="{"on" if i==2 else ""}">{d}<small>{w}</small></span>' for i,(d,w) in enumerate([('૩૦','સોમ'),('૧','મંગળ'),('૨','બુધ'),('૩','ગુરુ'),('૪','શુક્ર'),('૫','શનિ'),('૬','રવિ')]))+'</div>'+lab('બુધ, ૨ ડિસે. · ૧ પધરામણી')+card(rr('૯:૦૦','પટેલ સ્ટોર','દુકાનનું ઉદ્ઘાટન · સાણંદ','','નક્કી','p-ok'))+lab('શનિ, ૫ ડિસે. · ૧ પધરામણી')+card(rr('૧૬:૦૦','હેતલ પટેલ','ગૃહપ્રવેશ · સાણંદ','','નક્કી','p-ok')),3,('plus','bell'))),
('મહિનો','કૅલેન્ડર; ટપકું = પધરામણી છે.',P('પધરામણી','પધરામણી',seg(['યાદી','અઠવાડિયું','મહિનો'],2)+'<div class="count"><span class="link">‹</span><b>ડિસેમ્બર ૨૦૨૬</b><span class="link">›</span></div><div class="cal">'+''.join(f'<span class="h">{x}</span>' for x in ['સો','મં','બુ','ગુ','શુ','શ','ર'])+'<span class="o">૩૦</span>'+''.join(f'<span class="{"on e" if d==2 else ("e" if d in (5,10,20) else "")}">{gn(d)}</span>' for d in range(1,28))+'</div>'+lab('બુધ, ૨ ડિસે.')+card(rr('૯:૦૦','પટેલ સ્ટોર','દુકાનનું ઉદ્ઘાટન · સાણંદ','','નક્કી','p-ok')),3,('plus','bell'))),
('પધરામણીની વિનંતી નોંધો','એક કૉલમ; ભક્ત પહેલાં શોધો.',P('નવી','પધરામણીની વિનંતી',fl('ભક્ત *','નામ કે મોબાઇલથી શોધો',hint='ન મળે તો «નવો ભક્ત» ઉમેરો')+'<span class="btn sm">+ નવો ભક્ત ઉમેરો</span>'+'<div class="two">'+fl('તારીખ *','૨૦/૧૨/૨૦૨૬',False)+fl('સમય','સવારે',False)+'</div>'+lab('હેતુ *')+tabs(['ગૃહપ્રવેશ','દુકાનનું ઉદ્ઘાટન','વાસ્તુ પૂજા','જન્મદિવસ'],0)+card(''.join(f'<div class="fold" style="{"border-top:1px solid var(--line)" if i else ""}"><span>{t} <small>· {v}</small></span>{sv("down")}</div>' for i,(t,v) in enumerate([('સ્થળ અને Maps','ભક્તની નોંધણી પ્રમાણે આપોઆપ'),('નોંધ અને સંપર્ક','મરજિયાત')]))),None,(),True,foot('રદ કરો','વિનંતી સાચવો'))),
('પધરામણીની વિગત','૩ પગલાંની પટ્ટી; આગળનું કામ નીચે ચોંટેલું.',P('PAD-000001 · નક્કી','પધરામણી',PH+nextup('તારીખ નક્કી છે — હવે પૂર્ણ કરવાનું બાકી','બુધ, ૨ ડિસે. · સવારે ૯:૦૦')+qa([('phone','ફોન'),('msg','WhatsApp'),('pin','Maps'),('cal','કૅલેન્ડર')])+kv([('સ્થળ','પટેલ સ્ટોર, સાણંદ'),('વિનંતી કરનાર','રમેશભાઈ પટેલ · ફોન પર')])+tl([('વિનંતી આવી','૨૮ નવે.','d'),('તારીખ નક્કી થઈ','૩૦ નવે.','d'),('પધરામણી','૨ ડિસે. ૯:૦૦','c')])+acts(['તારીખ/સમય બદલો','ભક્તની પ્રોફાઇલ ખોલો']),None,(),True,foot('રદ કરો','પૂર્ણ કરો'))),
('તારીખ અને સમય નક્કી કરો','ટકરાવ હોય તો તરત ચેતવણી.',P('PAD-000003','પધરામણી',PH,None,(),True,over=sheet('તારીખ અને સમય નક્કી કરો','<div class="two">'+fl('તારીખ *','૨૦/૧૨/૨૦૨૬',False)+fl('સમય *','૦૯:૩૦',False)+'</div><div class="warnb">સમય ટકરાવ: એ દિવસે ૦૯:૦૦ વાગ્યે બીજી પધરામણી છે (૬૦ મિનિટની અંદર).</div>'+fl('નોંધ','')+bt('રદ કરો','નક્કી કરો')))),
('ફરી સંપર્ક નોંધો','ક્યારે ફરી ફોન કરવો તે ગોળીથી.',P('PAD-000004','પધરામણી',PH,None,(),True,over=sheet('ફરી સંપર્ક નોંધો',lab('ક્યારે ફરી સંપર્ક કરવો')+seg(['આવતીકાલે','૩ દિવસ','૭ દિવસ','તારીખ'],1)+fl('નોંધ *','શું વાત થઈ')+bt('રદ કરો','સાચવો')))),
('પૂર્ણ / રદ','પૂર્ણ: એક ખાતરી. રદ: કારણ ફરજિયાત.',P('PAD-000001','પધરામણી',PH,None,(),True,over=sheet('પધરામણી રદ કરવી?',lab('કારણ *')+tabs(['ભક્તે ના પાડી','તારીખ ન મળી','બે વાર વિનંતી','અન્ય'],0)+fl('નોંધ','')+bt('પાછા','હા, રદ કરો',True)))),
('હેતુઓ','સાદી યાદી; ચાલુ/બંધ ટૉગલથી.',P('પધરામણી','હેતુઓ',card(''.join(f'<div class="tg"><span class="m"><b>{t}</b><small>{s}</small></span><span class="sw {"on" if o else ""}"></span></div>' for t,s,o in [('ગૃહપ્રવેશ','૨ પધરામણી',1),('દુકાનનું ઉદ્ઘાટન','૨ પધરામણી',1),('વાસ્તુ પૂજા','૧ પધરામણી',1),('જન્મદિવસ','૧ પધરામણી',1),('અન્ય','૦',0)]))+'<span class="btn">+ હેતુ ઉમેરો</span>',None,(),True)),
]
S['I · ભક્ત યાદી']=[
('ભક્ત યાદી','શોધ ઉપર; «+» ઉપર જમણે.',P('પધરામણી · ૩ ભક્ત','ભક્ત યાદી','<div class="search"><div class="in">'+sv('search')+'નામ, મોબાઇલ કે ભક્ત નંબર</div></div>'+seg(['સક્રિય','આર્કાઇવ','સંભવિત એકસરખા'])+card(rr('કાં','કાંતાબેન ઠાકોર','DEV-000002 · 90••••••11','સાણંદ · પધરામણી ૨','સક્રિય','p-ok')+rr('ર','રમેશભાઈ પટેલ','DEV-000003 · 90••••••10','અમદાવાદ · પધરામણી ૧','સક્રિય','p-ok')+rr('અ','અનામી ભક્ત','DEV-000001 · મોબાઇલ નથી','','સક્રિય','p-ok')),4,('plus','bell'))),
('ભક્તની પ્રોફાઇલ','વ્યક્તિ ઉપર, તેની પધરામણી નીચે.',P('DEV-000002','ભક્ત','<div class="card idh"><span class="ph0" style="height:60px">કાં</span><span style="flex:1"><b>કાંતાબેન ઠાકોર</b><small>સાણંદ · 90••••••11</small></span></div>'+kv([('મોબાઇલ','90••••••11'),('સરનામું','ખાનગી — બતાવવા દબાવો'),('ઉમેર્યા','૨૮/૧૧/૨૦૨૬')])+sec('પધરામણી · ૨','+ વિનંતી')+card(rr('૯:૦૦','દુકાનનું ઉદ્ઘાટન','PAD-000001 · ૨ ડિસે.','','નક્કી','p-ok')+rr('—','વાસ્તુ પૂજા','PAD-000006 · તારીખ બાકી','','વિનંતી','p-info'))+acts(['વિગત બદલો','સંપર્ક વિગત બતાવો','આર્કાઇવ કરો']),None,(),True)),
('ભક્ત ઉમેરો','એકસરખું નામ મળે તો તરત બતાવે.',P('નવો','ભક્ત ઉમેરો',fl('પૂરું નામ *','કાંતાબેન ઠાકોર',False)+fl('મોબાઇલ','૧૦ અંક')+'<div class="warnb">આ નામ જેવો ભક્ત પહેલેથી છે: કાંતાબેન ઠાકોર (DEV-000002). <span class="link">ખોલો</span></div>'+fl('ગામ / શહેર','')+fl('સરનામું','',cls='ta')+fl('નોંધ',''),None,(),True,foot('રદ કરો','સાચવો'))),
]
SV=[('સ્વાગત અને માર્ગદર્શન','૩ ફાળવણી'),('ભોજન-પ્રસાદ સેવા','૨ ફાળવણી'),('જળ સેવા','૧ ફાળવણી'),('પાર્કિંગ વ્યવસ્થા','૧ ફાળવણી'),('સુરક્ષા અને વ્યવસ્થા','૧ ફાળવણી'),('આરોગ્ય સેવા','૧ ફાળવણી')]
MT=['સેવા યાદી','ક્ષમતા પ્લાનર','ટીમ','હાજરી','ઓળખકાર્ડ']
S['J · સેવા યાદી અને ક્ષમતા પ્લાનર']=[
('સેવા યાદી','હરોળમાં નામ અને ફાળવણી; કામ દબાવ્યા પછી.',P('મહોત્સવ તૈયારી · ૬ ચાલુ','સેવા યાદી',seg(['ચાલુ ૬','બંધ ૦'])+card(''.join(f'<div class="row" style="min-height:56px"><span class="l">{t}<small>{s}</small></span>{pill("ચાલુ","p-ok")}{sv("chev")}</div>' for t,s in SV)),4,('plus','bell'))),
('સેવાની વિગત','સેવા દબાવો: કોણ સોંપાયું છે અને કામ.',P('મહોત્સવ તૈયારી · ચાલુ','સ્વાગત અને માર્ગદર્શન',kv([('વર્ણન','ભક્તોનો આવકાર અને માર્ગદર્શન'),('ફાળવણી','૩ સ્વયંસેવક'),('ટીમ','સ્વાગત ટીમ')])+sec('સોંપાયેલા · ૩')+card(rr('ર','રમેશભાઈ પટેલ','SEVA-000001 · ૩, ૪ ફેબ્રુ.','','સોંપાયેલ','p-ok')+rr('જ','જયંતીભાઈ રાવળ','SEVA-000007 · ૨, ૩ ફેબ્રુ.','','સોંપાયેલ','p-ok'))+acts(['વિગત બદલો','ટીમ બનાવો','પ્લાનરમાં જુઓ','સેવા બંધ કરો']),None,(),True)),
('સેવા ઉમેરો / બદલો','નામ, વર્ણન અને કારણ; ટીમ અલગથી બને.',P('મહોત્સવ તૈયારી','સેવા યાદી','',4,('plus','bell'),over=sheet('નવી સેવા',fl('સેવાનું નામ *','દા.ત. ફૂલ સેવા')+fl('વર્ણન','')+fl('કારણ (ઓડિટમાં રહેશે) *','કારણ લખો')+note('ટીમ આપમેળે બનતી નથી. સેવા બન્યા પછી «ટીમ બનાવો».')+bt('રદ કરો','સેવા બનાવો')))),
('સેવા બંધ કરો','ફાળવણી ભૂંસાતી નથી તે લખેલું.',P('મહોત્સવ તૈયારી','સેવા યાદી','',4,('plus','bell'),over=sheet('આરોગ્ય સેવા બંધ કરવી?','<div class="warnb">નવી ફાળવણી નહીં થાય. હાલની ૧ ફાળવણી સચવાય છે.</div>'+fl('કારણ *','કારણ લખો')+bt('રદ કરો','હા, બંધ કરો')))),
('ક્ષમતા પ્લાનર','ઉપર દિવસ; દરેક ટીમ એક હરોળ.',P('મહોત્સવ તૈયારી','ક્ષમતા પ્લાનર',days(1,['૦/૦','૧/૫','૦/૦','૦/૦','૦/૦','૦/૦','૦/૦'])+seg(['સવારથી બપોર','બપોરથી રાત'])+cnt([('૪','ઉપલબ્ધ'),('૫','જોઈએ'),('૧','ફાળવેલા'),('૪','ખૂટે છે',1)])+card(pl('પ્રસાદ સેવા ટીમ',1,5)+pl('પાણી સેવા ટીમ',0,0)+pl('સ્વાગત ટીમ',0,0)+pl('પાર્કિંગ ટીમ',0,0))+note('લોકોને ફાળવવાનું ટીમના પાનામાં થાય છે. «આપમેળે ભરો» બંધ છે (મંજૂરી બાકી).'),4)),
]
S['K · ટીમ']=[
('ટીમ યાદી','દરેક ટીમ એક હરોળ: લીડર, સભ્યો, ખૂટતા.',P('મહોત્સવ તૈયારી · ૨ ટીમ','ટીમ','<div class="search"><div class="in">'+sv('search')+'ટીમ શોધો</div></div>'+card(''.join(f'<div class="tg" style="display:grid;gap:6px"><div style="display:flex;justify-content:space-between;gap:8px"><b style="font-size:15px">{t}</b>{pill(p,pc)}</div><small style="color:var(--mut);font-size:12.5px">{s}</small><div class="meter"><i style="width:{w}%"></i></div></div>' for t,s,p,pc,w in [('પ્રસાદ સેવા ટીમ','લીડર: જયંતીભાઈ રાવળ · સોંપાયેલા ૧ / ૫','ઘટ','p-warn',20),('પાણી સેવા ટીમ','લીડર બાકી · સોંપાયેલા ૩','લીડર બાકી','p-bad',60)])),4,('plus','bell'))),
('ટીમ · જરૂરિયાત','ફક્ત પસંદ કરેલો દિવસ ખુલ્લો.',None),
('ટીમ · સભ્યો','લીડર અને નાયબ લીડર ઉપર; સભ્યો નીચે.',P('ટીમ · લીડર: જયંતીભાઈ રાવળ','પ્રસાદ સેવા ટીમ',seg(['હાજરી','સભ્યો','જરૂરિયાત','ઇતિહાસ'],1)+lab('જવાબદાર વ્યક્તિઓ')+card(''.join(f'<div class="row" style="min-height:54px"><span class="l">{t}<small>{s}</small></span><span class="val link">{a}</span></div>' for t,s,a in [('ટીમ લીડર','જયંતીભાઈ રાવળ · SEVA-000007','બદલો'),('નાયબ લીડર','કોઈની નિમણૂક નથી','નિમણૂક કરો'),('ટીમ મેનેજર','કોઈની નિમણૂક નથી','નિમણૂક કરો')]))+sec('સભ્યો · ૧','+ સ્વયંસેવક સોંપો')+card(rr('જ','જયંતીભાઈ રાવળ','SEVA-000007 · ૨, ૩ ફેબ્રુ.','','સોંપાયેલ','p-ok'))+acts(['WhatsApp ગ્રુપ','હાજરી શીટ છાપો','ટીમ બંધ કરો']),4,('bell',),True)),
('સ્વયંસેવક સોંપો','ઉપલબ્ધ લોકો જ દેખાય; ટિક કરીને સોંપો.',P('૩ ફેબ્રુ. · સવાર','સ્વયંસેવક સોંપો','<div class="search"><div class="in">'+sv('search')+'નામ કે SEVA-નંબર</div></div>'+note('આ દિવસ અને સમય માટે ઉપલબ્ધ ૪ · જોઈએ ૫')+card(''.join(f'<div class="rr" style="min-height:60px"><span class="cb {"on" if i<2 else ""}">{"✓" if i<2 else ""}</span><span class="m"><b>{n}</b><small>{s}</small></span></div>' for i,(n,s) in enumerate([('રમેશભાઈ પટેલ','SEVA-000001 · સ્વાગત'),('કિરણબેન શાહ','SEVA-000004 · ભોજન-પ્રસાદ'),('ભરતભાઈ પ્રજાપતિ','SEVA-000013 · સેવા બાકી'),('અશોકભાઈ મકવાણા','SEVA-000015 · સેવા બાકી')]))),None,(),True,foot('રદ કરો','૨ ને સોંપો'))),
('ટીમ ઉમેરો','ટીમ હાથથી બને; સેવા પસંદ કરો.',P('મહોત્સવ તૈયારી','ટીમ','',4,over=sheet('ટીમ ઉમેરો',fl('ટીમનું નામ *','દા.ત. ફૂલ સેવા ટીમ')+lab('સેવા *')+tabs(['સ્વાગત','ભોજન-પ્રસાદ','જળ સેવા','પાર્કિંગ'],1)+fl('વર્ણન','')+bt('રદ કરો','ટીમ બનાવો')))),
]
IDT=['બધી <small>૧૩</small>','તૈયાર નથી <small>૬</small>','સમીક્ષા <small>૧</small>','છાપવા મંજૂર <small>૧</small>','છપાયું','લઈ લીધું']
IDL=card(idr(0,'રમેશભાઈ પટેલ','SEVA-000001 · સ્વાગત','તૈયાર નથી','p-mut')+idr(0,'કાંતાબેન ઠાકોર','SEVA-000002 · ભોજન-પ્રસાદ','તૈયાર નથી','p-mut')+idr(0,'પ્રજ્ઞેશકુમાર શાહ','SEVA-000003 · સેવા બાકી','તૈયાર નથી','p-mut')+idr(0,'જયંતીભાઈ રાવળ','SEVA-000007 · સ્વાગત','સમીક્ષા માટે','p-info')+idr(0,'હીનાબેન દેસાઈ','SEVA-000008 · ભોજન-પ્રસાદ','છાપવા મંજૂર','p-ok')+idr(0,'દિનેશભાઈ ચૌહાણ','SEVA-000009 · જળ સેવા','લેવા તૈયાર','p-ok')+idr(0,'મહેશભાઈ સોલંકી','SEVA-000011 · સુરક્ષા','છપાયું','p-ok'))
IDCARD=f'<div class="idcard"><div class="h"><img src="{LIGHT}" alt=""><b>શ્રી વિહત મેલડી ધામ</b>મંગલારોહણ · ૨–૮ ફેબ્રુ. ૨૦૨૭</div><div class="p">ર</div><div class="n">રમેશભાઈ પટેલ</div><div class="r">સ્વયંસેવક · ૩, ૪ ફેબ્રુ.</div><div class="b"><i></i><span><b>સ્વાગત અને માર્ગદર્શન</b><br>SEVA-000001</span></div></div>'
import base64 as _b64, os as _os
def _card(f):
    p=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),f)
    return 'data:image/jpeg;base64,'+_b64.b64encode(open(p,'rb').read()).decode()
IDPAIR=('<div class="idpair">'
        '<img class="idshot" src="'+_card('card-front.jpg')+'" alt="">'
        '<img class="idshot" src="'+_card('card-back.jpg')+'" alt="">'
        '<small>આગળ</small><small>પાછળ</small></div>')
S['L · ઓળખકાર્ડ']=[
('ઓળખકાર્ડ યાદી','એક ફિલ્ટર પટ્ટી; ટિક હરોળની અંદર.',P('કામ · ૧૩ કાર્ડ','ઓળખકાર્ડ',tabs(IDT)+'<div class="warnb">સ્વીકાર બાકી: ૩ · ફોટો નથી: ૪</div>'+IDL,1,('print','bell'))),
('પસંદ કર્યા પછી','પટ્ટી નીચે આવે; આગળનું એક જ પગલું ઘેરું.',None),
('કાર્ડ પ્રિવ્યૂ','v11 નું ખરું કાર્ડ, આગળ અને પાછળ બંને એકસાથે; કામ નીચે.',P('SEVA-000060 · તૈયાર નથી','કાર્ડ પ્રિવ્યૂ',IDPAIR+note('આગળના QR માં ફક્ત SEVA નંબર છે, પાછળનો વેબસાઇટનો. કાર્ડ પર દબાવો તો પૂરા કદમાં ખૂલે.')+acts(['ફોટો બદલો','કાર્ડનો ઇતિહાસ']),None,(),True,foot('છાપો','સમીક્ષા માટે તૈયાર'))),
('કાર્ડ સોંપવું','કોણે અને ક્યારે આપ્યું તે નોંધાય.',P('SEVA-000060 · લેવા તૈયાર','કાર્ડ પ્રિવ્યૂ',IDPAIR,None,(),True,over=sheet('કાર્ડ સોંપ્યું?',kv([('સ્વયંસેવક','અંકિત શાહ'),('આપનાર','તમે (સુપર એડમિન)'),('સમય','હમણાં')])+fl('નોંધ','')+bt('રદ કરો','હા, સોંપ્યું')))),
('ફરી છાપવું','કારણ ફરજિયાત; જૂનું કાર્ડ રદ ગણાય.',P('SEVA-000060','કાર્ડ પ્રિવ્યૂ',IDPAIR,None,(),True,over=sheet('કાર્ડ ફરી છાપવું?',lab('કારણ *')+tabs(['ખોવાયું','સેવા બદલાઈ','નામમાં ભૂલ','ફોટો બદલાયો'],1)+'<div class="warnb">જૂનું કાર્ડ રદ ગણાશે.</div>'+bt('રદ કરો','ફરી છાપવા મૂકો')))),
('A4 શીટ છાપો','કેટલાં કાર્ડ અને પાનાં તે ઉપર; પ્રિન્ટ નીચે.',P('૨ કાર્ડ · ૧ પાનું','A4 શીટ','<div style="background:#fff;border:1px solid var(--line);border-radius:8px;aspect-ratio:210/297;width:250px;justify-self:center;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);gap:6px;padding:14px">'+''.join(f'<i style="border-radius:5px;background:{"linear-gradient(180deg,#6b1830 30%,#fff 30%)" if i<2 else "#f3ecdf"};border:1px solid #e3d6bf"></i>' for i in range(9))+'</div>'+note('A4, ૯ કાર્ડ પ્રતિ પાનું, ૫૪×૮૬ મિમી. છાપતી વખતે «Actual size» રાખો.'),None,(),True,foot('પાછા','છાપો / PDF'))),
]
ATB=days(0,WD)+seg(['સવાર','બપોર'])+'<div class="search"><div class="in" style="color:var(--ink);font-weight:600;justify-content:space-between">પ્રસાદ સેવા ટીમ'+sv('down')+'</div></div>'
ATS='<div class="card sum"><div><b>૫</b><small>અપેક્ષિત</small></div><div><b style="color:var(--ok)">૨</b><small>હાજર</small></div><div><b style="color:var(--bad)">૧</b><small>ગેરહાજર</small></div><div><b>૨</b><small>હાજરી બાકી</small></div></div>'
QRB=f'<div class="qr">{sv("qr")}QR સ્કેન કરો</div>'
S['M · મહોત્સવ દિવસ · હાજરી']=[
('હાજરી','ચાર આંકડા, QR બટન, દરેક નામ નીચે બે મોટા બટન.',P('મહોત્સવ તૈયારી','મહોત્સવ દિવસ · હાજરી',ATB+ATS+QRB+card(at('રમેશભાઈ પટેલ','SEVA-000001','હાજરી બાકી','p-mut')+at('કિરણબેન શાહ','SEVA-000004','હાજર','p-ok',True)),4,('print',))),
('ગેરહાજર · કારણ','કારણ ગોળીથી; લખવું ઓછું.',P('મહોત્સવ તૈયારી','મહોત્સવ દિવસ · હાજરી',ATB+ATS,4,('print',),over=sheet('રમેશભાઈ પટેલ ગેરહાજર?',lab('કારણ *')+tabs(['બીમાર','બહારગામ','જાણ નથી','અન્ય'],0)+fl('નોંધ','')+bt('રદ કરો','ગેરહાજર નોંધો',True)))),
('QR સ્કેન','આખી સ્ક્રીન કૅમેરા; નંબર લખવાનો રસ્તો નીચે.',f'<div class="ph">{bar3("૨ ફેબ્રુ. · સવાર","QR સ્કેન કરો",(),True)}<div class="cam"><i></i><span>ઓળખકાર્ડનો આગળનો QR ચોકઠામાં રાખો</span></div><div class="foot"><span class="btn pri" style="background:var(--card);color:var(--mar)">SEVA નંબર લખો</span></div></div>'),
('સ્કેન પછી','વ્યક્તિ અને તેની ફરજ; એક દબાવો = હાજર.',P('૨ ફેબ્રુ. · સવાર','QR સ્કેન કરો','',None,(),True,over=sheet('રમેશભાઈ પટેલ','<div class="okb">આ સમય માટે ફરજ છે: સ્વાગત ટીમ · ૨ ફેબ્રુ. સવાર</div>'+kv([('SEVA નંબર','SEVA-000001'),('હાલ','હાજરી બાકી')])+bt('ગેરહાજર','હાજર નોંધો')+'<span class="link" style="justify-self:center">બીજો સ્કેન કરો</span>'))),
('સ્કેન · ફરજ નથી','ખોટા દિવસે આવે તો સ્પષ્ટ જવાબ; કોઈ હાજર નોંધાતું નથી.',P('૨ ફેબ્રુ. · સવાર','QR સ્કેન કરો','',None,(),True,over=sheet('વિપુલભાઈ જોષી','<div class="warnb">આ દિવસ અને સમય માટે ફરજ નથી. તેમની ફરજ: ૮ ફેબ્રુ. · આખો દિવસ.</div>'+bt('બંધ કરો','બીજો સ્કેન કરો')))),
('બધી ટીમ','ટીમ પ્રમાણે એક-એક હરોળ; સરવાળો ઉપર.',P('મહોત્સવ તૈયારી','મહોત્સવ દિવસ · હાજરી',days(0,WD)+seg(['સવાર','બપોર'])+'<div class="card sum"><div><b>૧૨</b><small>અપેક્ષિત</small></div><div><b style="color:var(--ok)">૭</b><small>હાજર</small></div><div><b style="color:var(--bad)">૨</b><small>ગેરહાજર</small></div><div><b>૩</b><small>હાજરી બાકી</small></div></div>'+QRB+card(''.join(f'<div class="row" style="min-height:54px"><span class="l">{t}<small>{s}</small></span>{pill(p,pc)}{sv("chev")}</div>' for t,s,p,pc in [('પ્રસાદ સેવા ટીમ','૫ માંથી ૨ હાજર · ૧ ગેરહાજર','૨ બાકી','p-warn'),('પાણી સેવા ટીમ','૩ માંથી ૩ હાજર','પૂરું','p-ok'),('સ્વાગત ટીમ','૪ માંથી ૨ હાજર · ૧ ગેરહાજર','૧ બાકી','p-warn')]))+note('એક વ્યક્તિની બે ટીમમાં ફરજ હોય તો કુલમાં બે ફરજ ગણાય.'),4,('print',))),
]
S['N · WhatsApp ગ્રુપ']=[
('WhatsApp ગ્રુપ','ગ્રુપ, હેતુ અને કેટલા જોડાયા.',P('મહોત્સવ તૈયારી · ૩ ગ્રુપ','WhatsApp ગ્રુપ','<div class="infob">પેનલ ગ્રુપ બનાવતી નથી અને કોઈને ઉમેરતી નથી. લિંક વ્યક્તિ મોકલે છે.</div>'+card(''.join(f'<div class="row" style="min-height:58px"><span class="l">{t}<small>{s}</small></span>{pill(p,pc)}{sv("chev")}</div>' for t,s,p,pc in [('પ્રસાદ સેવા ટીમ','ટીમ · ૩ માંથી ૧ જોડાયા','ટીમ','p-info'),('સ્વયંસેવક જાહેરાત','સમુદાય જાહેરાત · ૧૩ માંથી ૮','સમુદાય','p-ok'),('સ્વાગત સેવા','સેવા · લિંક નથી','સેવા','p-mut')])),4,('plus','bell'))),
('ગ્રુપની વિગત','લિંક છુપાયેલી; જોવાની નોંધ. દરેક સભ્યની સ્થિતિ.',P('ટીમ · લીડ: જયંતીભાઈ રાવળ','પ્રસાદ સેવા ટીમ',kv([('Invite લિંક','chat.whatsapp.com/••••••'),('લીડ','જયંતીભાઈ રાવળ'),('ડેપ્યુટી','—')])+'<div class="two"><span class="btn sm">પૂરી લિંક જુઓ</span><span class="btn sm">લિંક reset</span></div>'+tabs(['બધા <small>૩</small>','લિંક મોકલવાની બાકી <small>૧</small>','લિંક મોકલી <small>૧</small>','જોડાયા <small>૧</small>'])+card(rr('જ','જયંતીભાઈ રાવળ','SEVA-000007','','જોડાયા','p-ok')+rr('ર','રમેશભાઈ પટેલ','SEVA-000001 · ટીમ લીડરે જાતે','','લિંક મોકલી','p-info')+rr('કિ','કિરણબેન શાહ','SEVA-000004','','બાકી','p-mut')),None,(),True)),
]
RT=['અહેવાલ','એડમિન એનાલિટિક્સ','વેબસાઇટ એનાલિટિક્સ']
def fo(t,s=''):return card(f'<div class="acc"><div class="hd"><span>{t} <small>{s}</small></span>{sv("down")}</div></div>')
S['O · અહેવાલ']=[
('અહેવાલ','૪ આંકડા, પછી દરેક ટેબલ બંધ પટ્ટીમાં.',P('વ્યવસ્થા','અહેવાલ',tabs(RT)+cnt([('૧૮','કુલ નોંધણી'),('૧૩','પાકી'),('૩','સમીક્ષા બાકી',1),('૨','રદ')])+foldo('મહોત્સવ દિવસ મુજબ','૭ દિવસ','<table class="tbl"><tr><th>તારીખ</th><th>સ્વીકારેલી</th><th>બાકી</th><th>રદ</th></tr>'+''.join(f'<tr><td>{d} ફેબ્રુ.</td><td>{a}</td><td>{b}</td><td>૦</td></tr>' for d,a,b in [('૨','૩','૧'),('૩','૭','૨'),('૪','૭','૨'),('૫','૨','૦'),('૬','૨','૦'),('૭','૧','૦'),('૮','૧','૧')])+'</table>')+fo('સેવા, ટીમ, WhatsApp અને પધરામણી','૪ કોષ્ટક'),4,('dl','print'))),
('એડમિન એનાલિટિક્સ','કોણે કેટલું કામ કર્યું; ફક્ત સરવાળા.',P('વ્યવસ્થા','અહેવાલ',tabs(RT,1)+seg(['૭ દિવસ','૩૦ દિવસ','બધું'])+cnt([('૪૬','ફેરફાર'),('૧૩','સ્વીકાર'),('૨','રદ'),('૪','લૉગિન')])+card('<div style="padding:10px 12px 0;font-weight:700;font-size:14px">રોજનાં કામ</div><div style="padding:6px 12px 12px"><div class="bars">'+''.join(f'<i style="height:{h}%"></i>' for h in [20,45,30,80,55,25,95])+'</div></div>')+fo('વિભાગ મુજબ','૬ વિભાગ')+fo('એડમિન મુજબ','૩ એડમિન'),4,('dl','print'))),
('વેબસાઇટ એનાલિટિક્સ','મુલાકાત અને ફોર્મ; વ્યક્તિની માહિતી નહીં.',P('વ્યવસ્થા','અહેવાલ',tabs(RT,2)+seg(['૭ દિવસ','૩૦ દિવસ','બધું'])+cnt([('૪૨૦','મુલાકાત'),('૬૫','ફોર્મ ખોલ્યું'),('૧૮','નોંધણી'),('૨૮%','પૂરું કર્યું')])+card('<div style="padding:10px 12px 0;font-weight:700;font-size:14px">રોજની મુલાકાત</div><div style="padding:6px 12px 12px"><div class="bars">'+''.join(f'<i style="height:{h}%"></i>' for h in [40,35,60,50,90,70,45])+'</div></div>')+fo('પાના મુજબ','૧૦ પાનાં')+fo('ઉપકરણ મુજબ','ફોન ૮૨%'),4,('dl','print'))),
]
STT=['સેટિંગ','વેબસાઇટ સ્થિતિ','એડમિન વપરાશકર્તા','ઓડિટ ઇતિહાસ']
ROLES=[('સુપર એડમિન','બધું; માલિક સ્તરના સ્વિચ અને એડમિન બનાવવા'),('એડમિન','રોજનું બધું કામ; ચાલુ/બંધ «તરત» સ્વિચ'),('નોંધણી વ્યવસ્થાપક','નોંધણી, સેવા, ઓળખકાર્ડ'),('ટીમ સંયોજક','ફક્ત પોતાની ટીમ અને હાજરી'),('ફક્ત જોનાર','જોઈ શકે, બદલી ન શકે')]
S['P · સેટિંગ, વપરાશકર્તા, ઓડિટ, ખાતું']=[
('સેટિંગ','નામ અને હાલનું મૂલ્ય એક હરોળમાં.',P('વ્યવસ્થા','સેટિંગ',tabs(STT)+lab('નિમંત્રણ અને પધરામણી')+acts([('નિમંત્રણ પછી ફોલો-અપ','૩ દિવસ'),('પધરામણી સમયનો ટકરાવ','૬૦ મિનિટ'),('પધરામણી સંભવિત બેવડી વિનંતી','૭ દિવસ')])+lab('નોંધણી ફોર્મ')+acts([('ફોર્મમાં «ઉંમર» બતાવવી','બતાવો'),('ફોર્મમાં «સરનામું» બતાવવું','બતાવો'),('એક નોંધણીને વધુમાં વધુ સેવા','મર્યાદા નથી')])+lab('બીજા સેટિંગ ક્યાં છે')+acts(['નોંધણીની મર્યાદા અને તારીખ મુજબ ક્ષમતા','બધા ON/OFF: નિયંત્રણ કેન્દ્ર']),4)),
('મૂલ્ય બદલો','નાની શીટ: મૂલ્ય, મર્યાદા અને સાચવો.',P('વ્યવસ્થા','સેટિંગ',tabs(STT),4,over=sheet('પધરામણી સમયનો ટકરાવ',note('આટલી મિનિટની અંદર બે પધરામણી હોય તો ચેતવણી દેખાશે (બંધ થતી નથી).')+'<div style="display:flex;justify-content:center"><span class="step"><span>−</span><b style="min-width:70px;font-size:22px">૬૦</b><span>+</span></span></div>'+note('૧ થી ૬૦૦ વચ્ચે · સામાન્ય મૂલ્ય: ૬૦')+bt('રદ કરો','સાચવો')))),
('વેબસાઇટ સ્થિતિ','ફક્ત જોવા માટે; બદલવા નિયંત્રણ કેન્દ્ર.',P('વ્યવસ્થા','સેટિંગ',tabs(STT,1)+card(''.join(f'<div class="row" style="min-height:52px"><span class="l">{t}<small>{s}</small></span>{pill(p,pc)}</div>' for t,s,p,pc in [('વેબસાઇટ','મુલાકાતીઓ જોઈ શકે છે','જાહેર','p-ok'),('સેવા નોંધણી','વેબસાઇટ પરનું ફોર્મ','બંધ','p-bad'),('ઉદ્ઘાટન સમારોહ પેજ','','બંધ','p-mut'),('ડેટાબેઝ','છેલ્લી તપાસ ૧ મિનિટ પહેલાં','બરાબર','p-ok'),('સંમતિ લખાણ','આવૃત્તિ ૨','મંજૂર','p-ok')]))+'<span class="btn">નિયંત્રણ કેન્દ્ર ખોલો</span>',4)),
('એડમિન વપરાશકર્તા','દરેક એડમિન એક હરોળ: ભૂમિકા અને ૨-પગલાં.',P('વ્યવસ્થા','સેટિંગ',tabs(STT,2)+seg(['વપરાશકર્તા','ભૂમિકા','સત્રો'])+card(rr('સુ','u-demo-super-admin','સુપર એડમિન · ૨-પગલાં ચાલુ','છેલ્લું લૉગિન: આજે','સક્રિય','p-ok')+rr('એ','u-demo-admin','એડમિન · ૨-પગલાં ચાલુ','છેલ્લું લૉગિન: ગઈકાલે','સક્રિય','p-ok')+rr('ટી','u-demo-team','ટીમ સંયોજક · પ્રસાદ સેવા ટીમ','૨-પગલાં બાકી','બાકી','p-warn'))+'<span class="btn">+ નવો એડમિન વપરાશકર્તા</span>',4)),
('નવો એડમિન વપરાશકર્તા','ભૂમિકા કાર્ડથી પસંદ; ઓછી પરવાનગી પહેલેથી પસંદ.',P('એડમિન વપરાશકર્તા','નવો વપરાશકર્તા',fl('પૂરું નામ *','')+fl('વપરાશકર્તા નામ *','')+lab('ભૂમિકા *')+''.join(f'<div class="rolec {"on" if i==4 else ""}"><i></i><span><b>{t}</b><small>{s}</small></span></div>' for i,(t,s) in enumerate(ROLES)),None,(),True,foot('પાછા','વપરાશકર્તા બનાવો'))),
('ભૂમિકા અને પરવાનગી','ઉપર સાર; વિગત વિભાગ પ્રમાણે બંધ પટ્ટીમાં.',P('વ્યવસ્થા','સેટિંગ',tabs(STT,2)+seg(['વપરાશકર્તા','ભૂમિકા','સત્રો'],1)+card(''.join(f'<div class="row" style="min-height:52px"><span class="l">{t}<small>{s}</small></span></div>' for t,s in ROLES))+lab('વિગતવાર પરવાનગી')+fo('નોંધણી','૮ પરવાનગી')+fo('ટીમ અને હાજરી','૬ પરવાનગી')+fo('WhatsApp','૫ પરવાનગી'),4)),
('સત્રો','કયા ઉપકરણ પર લૉગિન છે; એક દબાવો = બંધ.',P('વ્યવસ્થા','સેટિંગ',tabs(STT,2)+seg(['વપરાશકર્તા','ભૂમિકા','સત્રો'],2)+card(''.join(f'<div class="row" style="min-height:58px"><span class="l">{t}<small>{s}</small></span><span class="val link">{a}</span></div>' for t,s,a in [('આ ફોન · Chrome','u-demo-super-admin · હમણાં','આ સત્ર'),('Windows · Chrome','u-demo-super-admin · ૨ કલાક પહેલાં','બંધ કરો'),('Android · Chrome','u-demo-admin · ગઈકાલે','બંધ કરો')]))+'<span class="btn" style="border-color:var(--bad);color:var(--bad)">બીજાં બધાં સત્ર બંધ કરો</span>',4)),
('ઓડિટ ઇતિહાસ','કોણે, ક્યારે, શું; વિભાગ ફિલ્ટર એક પટ્ટીમાં.',P('વ્યવસ્થા','સેટિંગ',tabs(STT,3)+tabs(['બધા','નોંધણી','નિયંત્રણ કેન્દ્ર','ટીમ','WhatsApp','પધરામણી'])+lab('આજે')+card(''.join(f'<div class="row" style="min-height:56px"><span class="l" style="font-size:14px">{t}<small>{s}</small></span></div>' for t,s in [('નોંધણી સ્વીકાર (પેનલ): બંધ','૧૧:૪૨ · u-demo-admin · કારણ: ગણતરી તપાસ'),('SEVA-000013 સ્વીકારી','૧૧:૩૦ · u-demo-super-admin'),('પ્રસાદ સેવા ટીમ: જરૂરિયાત ૫','૧૧:૧૨ · u-demo-admin')]))+lab('ગઈકાલે')+card(''.join(f'<div class="row" style="min-height:56px"><span class="l" style="font-size:14px">{t}<small>{s}</small></span></div>' for t,s in [('ઓળખકાર્ડ સોંપ્યું: SEVA-000009','૧૮:૨૦ · u-demo-admin'),('ખાનગી વિગત જોઈ: SEVA-000001','૧૭:૦૫ · u-demo-super-admin')])),4)),
('મારું ખાતું','લોગો નહીં, વ્યક્તિ ઉપર; અક્ષર મોટા કરવાનું અહીં.',P('વ્યવસ્થા','મારું ખાતું','<div class="card me"><span class="av">સુ</span><span style="flex:1"><b>u-demo-super-admin</b><br><small style="color:var(--mut)">સુપર એડમિન · શ્રી વિહત મેલડી ધામ</small></span></div>'+acts([('અક્ષરનું માપ (અ+)','સામાન્ય'),'પાસવર્ડ બદલો',('બે-પગલાંની ચકાસણી','ચાલુ'),'રિકવરી કોડ','મારાં સત્રો'])+'<span class="btn" style="border-color:var(--bad);color:var(--bad)">લૉગઆઉટ</span>',None,(),True)),
]
S['Q · સ્થિતિઓ']=[
('લોડ થાય છે','ખાલી સ્ક્રીન નહીં; હરોળના આકાર દેખાય.',P('કામ','સેવા નોંધણીઓ',SRCH+seg(SEGR)+card(''.join('<div class="rr"><span class="av" style="background:#efe5d2"></span><span class="m" style="display:grid;gap:7px"><span class="sk" style="width:70%"></span><span class="sk" style="width:45%;height:10px"></span></span></div>' for _ in range(6))),1,('dl','bell'))),
('ખાલી યાદી','લોગો, એક વાક્ય અને આગળનું કામ.',P('પધરામણી','પધરામણી',seg(['યાદી','અઠવાડિયું','મહિનો'])+f'<div class="empty"><img src="{RED}" alt=""><b>હજી કોઈ પધરામણી નથી</b><p>ફોન પર વિનંતી આવે ત્યારે અહીં નોંધો.</p><span class="btn pri" style="flex:none">પધરામણીની વિનંતી નોંધો</span></div>',3,('plus','bell'))),
('ભૂલ','શું થયું અને ફરી પ્રયત્નનું બટન.',P('કામ','સેવા નોંધણીઓ','<div class="warnb"><b>યાદી લાવી શકાઈ નથી.</b><br>ઇન્ટરનેટ તપાસો અને ફરી પ્રયત્ન કરો.</div><span class="btn">ફરી પ્રયત્ન કરો</span>',1,('dl','bell'))),
('પરવાનગી નથી','તાળું, કારણ અને કોને પૂછવું.',P('વ્યવસ્થા','અહેવાલ',f'<div class="empty"><span style="width:64px;height:64px;border-radius:50%;background:#f1e7d6;display:grid;place-items:center;color:var(--mar)">{sv("lock")}</span><b>આ પાનું જોવાની પરવાનગી નથી</b><p>તમારી ભૂમિકા: ટીમ સંયોજક. જરૂર હોય તો સુપર એડમિનને કહો.</p><span class="btn">ડેશબોર્ડ પર પાછા</span></div>',4)),
('ઇન્ટરનેટ નથી','ઉપર ઘેરી પટ્ટી; છેલ્લું જોયેલું દેખાય, સાચવવું બંધ.',P('કામ','સેવા નોંધણીઓ',REGBODY+reglist(3),1,('dl','bell'),pre='<div class="offbar">ઇન્ટરનેટ નથી · ફેરફાર સચવાશે નહીં</div>')),
('સત્ર પૂરું થવાનું','૨ મિનિટ પહેલાં પૂછે; લખેલું ખોવાય નહીં.',P('કામ','ડેશબોર્ડ',HERO,0,over=sheet('સત્ર પૂરું થવાનું છે',note('સલામતી માટે ૨ મિનિટમાં આપમેળે લૉગઆઉટ થશે.')+bt('લૉગઆઉટ','ચાલુ રાખો')))),
('બીજા કોઈએ બદલ્યું','તમારો ફેરફાર રોકાય; નવી સ્થિતિ બતાવે.',P('કામ','નિયંત્રણ કેન્દ્ર',CCT,2,over=sheet('બીજા કોઈએ હમણાં બદલ્યું','<div class="warnb">«નોંધણી સ્વીકાર (પેનલ)» ૧૧:૪૨ વાગ્યે u-demo-admin એ બંધ કર્યું. તમારો ફેરફાર થયો નથી.</div>'+bt('બંધ કરો','નવી સ્થિતિ જુઓ')))),
('સફળતાની જાણ (toast)','નીચેની બારની ઉપર, ૩ સેકન્ડ; «પાછું લો» શક્ય હોય ત્યાં.',P('કામ · ૧૮ નોંધણી','સેવા નોંધણીઓ',REGBODY+reglist(4),1,('dl','bell'),over='<div class="toast"><i>✓</i><span style="flex:1">SEVA-000018 સ્વીકારી</span></div>')),
]
# reuse v2 screens for the None entries
v2=open('phone-ux-v2.html',encoding='utf-8').read()
def v2ph(title):
    i=v2.index(f'. {title}</h2>');a=v2.index('<div class="ph">',i);j=v2.index('<div class="item',a) if '<div class="item' in v2[a:] else v2.index('</div><div class="rules">',a)
    b=v2.rindex('</div>',a,j);return v2[a:b]
MORE=v2ph('«વધુ» મેનુ').replace('<div class="bar"><div class="t">',f'<div class="bar"><img class="lg" src="{RED}" alt=""><div class="t">')
TEAMREQ=v2ph('ટીમ પાનું');IDSEL=v2ph('ઓળખકાર્ડ').replace('<div class="bar"><div class="t">',f'<div class="bar"><img class="lg" src="{RED}" alt=""><div class="t">')
fill={'«વધુ» મેનુ':MORE,'ટીમ · જરૂરિયાત':TEAMREQ,'પસંદ કર્યા પછી':IDSEL}
# landscape
def LS(on,title,top,body,over=''):return f'<div class="phl">{rail(on)}<div class="lmain"><div class="lbar"><img class="lg" style="width:30px;height:30px" src="{RED}" alt=""><b>{title}</b>{top}</div><div class="lbody">{body}</div></div>{over}</div>'
LSR='<div class="search" style="flex:1"><div class="in" style="height:40px">'+sv('search')+'નામ, મોબાઇલ કે SEVA-નંબર</div></div><div style="width:250px">'+seg(SEGR)+'</div>'
L=[
('ફોન આડો · ડેશબોર્ડ','hero ડાબે, «આજે કરવાનું» જમણે; scroll વગર.',LS(0,'ડેશબોર્ડ','<span style="flex:1"></span><div class="ib" style="width:40px;height:40px">'+ic('search')+'</div><div class="ib" style="width:40px;height:40px">'+ic('bell')+'<i></i></div>','<div class="two" style="grid-template-columns:1fr 1.15fr">'+'<div style="display:grid;gap:8px;align-content:start">'+HERO+KP+'</div>'+card(''.join(f'<div class="row" style="min-height:46px"><span class="n {c}">{n}</span><span class="l">{t}</span>{sv("chev")}</div>' for n,c,t,s in TODO))+'</div>')),
('ફોન આડો · નોંધણી યાદી','ચિહ્ન નીચે નામ; ફિલ્ટર ઉપરની પટ્ટીમાં; યાદી ૨ કૉલમ.',LS(1,'સેવા નોંધણીઓ',LSR,'<div style="display:grid;grid-template-columns:1fr 150px;gap:10px;align-items:center">'+days(0,DSUB)+'<span class="count" style="justify-content:flex-end;gap:12px"><span>૪ નોંધણી</span><span style="color:var(--mar);font-weight:600">પસંદ કરો</span></span></div><div class="two">'+card(lr('પ્ર','પ્રજ્ઞેશકુમાર ચૌધરી','SEVA-000018 · ૨, ૩, ૪ ફેબ્રુ.','નવી','p-info')+lr('ર','રમેશભાઈ પટેલ','SEVA-000001 · ૨, ૩ ફેબ્રુ.','સમીક્ષા થઈ','p-ok')+lr('સં','સંગીતાબેન રાઠોડ','SEVA-000016 · ૭ ફેબ્રુ.','રદ','p-mut'))+card(lr('ભ','ભરતભાઈ પ્રજાપતિ','SEVA-000013 · ૨, ૩ ફેબ્રુ.','સમીક્ષા થઈ','p-ok')+lr('કિ','કિરણબેન શાહ','SEVA-000004 · ૨ ફેબ્રુ.','સમીક્ષા થઈ','p-ok')+lr('વિ','વિપુલભાઈ જોષી','SEVA-000017 · ૮ ફેબ્રુ.','નવી','p-info'))+'</div>')),
('ફોન આડો · નોંધણીની વિગત','યાદી ડાબે રહે; વિગત જમણે; બટન હંમેશાં દેખાય.',LS(1,'સેવા નોંધણીઓ',LSR,'',over='<div class="dim"></div><div class="lsheet"><div class="l">'+PERSON.replace('class="card idh"','class="idh" style="padding:0"')+acts(['સેવા અને ટીમ સોંપો','ઉપલબ્ધતા સુધારો','વિગત સુધારો'])+'</div><div class="r">'+'<div class="kv" style="padding:0">'+''.join(f'<span>{k}</span><b>{v}</b>' for k,v in [('ઉપલબ્ધતા',chips(['૩ ફેબ્રુ. સવાર','૪ ફેબ્રુ. બપોર'])),('સેવા','સ્વાગત અને માર્ગદર્શન'),('ટીમ','સ્વાગત ટીમ'),('WhatsApp','પહોંચ્યો')])+'</div>'+bt('રદ કરો','સ્વીકારો')+'</div></div>')),
('ફોન આડો · ખાતરી','ડાબે શું થશે, જમણે ખાનાં અને બટન.',LS(2,'નિયંત્રણ કેન્દ્ર','','',over='<div class="dim"></div><div class="lsheet"><div class="l"><h3 style="margin:0;font:700 18px/1.3 \'Noto Serif Gujarati\',serif;color:var(--mar)">વેબસાઇટ જાહેર: ચાલુ → બંધ?</h3><div class="warnb" style="background:#fff">મુલાકાતીઓને તરત «ટૂંક સમયમાં» પાનું દેખાશે.</div>'+note('ફક્ત સુપર એડમિન. ફેરફાર ઓડિટમાં નોંધાશે.')+'</div><div class="r">'+fl('કારણ *','કારણ લખો')+'<div class="two">'+fl('ચકાસણી કોડ *','• • • • • •')+fl('"હા" લખો *','')+'</div>'+bt('રદ કરો','હા, બંધ કરો')+'</div></div>')),
('ફોન આડો · હાજરી','ફિલ્ટર ઉપર; નામ ૨ કૉલમમાં, બટન નામની બાજુમાં.',LS(4,'મહોત્સવ દિવસ · હાજરી','<div style="flex:1">'+days(0)+'</div><div style="width:150px">'+seg(['સવાર','બપોર'])+'</div>','<div style="display:grid;grid-template-columns:1fr 200px;gap:10px;align-items:center">'+ATS+QRB+'</div><div class="two">'+''.join(card(f'<div class="rr" style="min-height:58px;padding:7px 10px"><span class="m"><b>{n}</b><small>{s}</small></span><span class="bt" style="width:170px"><span class="y {"on" if y else ""}" style="height:42px">હાજર</span><span class="x {"on" if x else ""}" style="height:42px">ગેરહાજર</span></span></div>') for n,s,y,x in [('રમેશભાઈ પટેલ','SEVA-000001',0,0),('કિરણબેન શાહ','SEVA-000004',1,0),('જયંતીભાઈ રાવળ','SEVA-000007',0,1),('ભરતભાઈ પ્રજાપતિ','SEVA-000013',0,0)])+'</div>')),
]
out=[];idx=[];total=0
for g,items in S.items():
    code=g.split(' ')[0];gid='g'+code
    idx.append(f'<a href="#{gid}">{g}</a>')
    out.append(f'<h2 class="grp" id="{gid}">{g}<small>{len(items)} સ્ક્રીન</small></h2><div class="grid">')
    for i,(t,why,h) in enumerate(items,1):
        if h is None:h=fill[t]
        out.append(f'<div class="item"><h2><i>{code}{i}</i>{t}</h2><p class="why">{why}</p>{h}</div>');total+=1
    out.append('</div>')
idx.append('<a href="#gR">R · ફોન આડો</a><a href="#rules">નિયમ</a>')
out.append(f'<h2 class="grp" id="gR">R · ફોન આડો (૮૪૪×૩૯૦)<small>{len(L)} સ્ક્રીન</small></h2><div class="grid">')
for i,(t,why,h) in enumerate(L,1):
    out.append(f'<div class="item wide"><h2><i>R{i}</i>{t}</h2><p class="why">{why}</p>{h}</div>');total+=1
out.append('</div>')
rules='''<div class="rules" id="rules"><h2>ફોન માટેના નિયમ (દરેક પાનાને લાગુ)</h2><ol><li><b>આંકડા એક જ કાર્ડમાં (૨×૨).</b> દરેક પાના પર ઉપર એક સફેદ કાર્ડ: ચાર આંકડા, દરેકની આગળ આછા રંગનો આઇકન ચોરસ, નીચે નામ. ચાર નાનાં ખાનાં એક લીટીમાં નહીં.</li><li><b>વિગત = સમજાય એવી હરોળ, કોષ્ટક નહીં.</b> «નામ : કિંમત» ટેબલની જગ્યાએ આઇકન + નાનું નામ + મોટી કિંમત. ઉપર «હવે શું કરવાનું» એક પટ્ટી, પછી ફોન/WhatsApp/Maps/કૅલેન્ડરનાં ચાર બટન, અને નીચે ટપકાંવાળી <b>સમયરેખા</b>.</li><li><b>ફોર્મમાં પહેલાં ૩–૪ ખાનાં જ.</b> બાકીનું ઘડી કરેલા ભાગમાં, અને ભાગના નામ પાસે જ લખેલું હોય કે અંદર શું છે. એક જ «સાચવો», એક જ કારણ.</li><li><b>પાનાનું નામ નીચે એક લીટી.</b> પટ્ટીની નીચે ૧૩px માં પાનું શેના માટે છે તે એક લીટીમાં (મુખ્ય પાનાં પર જ).</li><li><b>યાદીનાં પાનાં પર ગોળ «+».</b> નીચે જમણે ઊડતું બટન — નવી નોંધણી, પધરામણી, ભક્ત, સેવા, ટીમ.</li>
<li><b>લોગો અને નામ ઉપરની પટ્ટીમાં.</b> મુખ્ય પાનાં પર ડાબે મંદિરનો લોગો; અંદરનાં પાનાં પર તેની જગ્યાએ «પાછા». લૉગિન, «વધુ» અને ખાલી યાદીમાં પણ લોગો. અલગ મોટું શીર્ષક, સમજૂતીનું વાક્ય અને «અ+» બટન ફોન પર નહીં («અ+» મારા ખાતામાં).</li>
<li><b>ટૅબ એક જ લીટીમાં.</b> વિભાગની ટૅબ અને ફિલ્ટર એક-એક પટ્ટી; વધુ હોય તો એ પટ્ટી બાજુમાં સરકે (પાનું નહીં). ગોળીઓ વીંટાઈને ૩–૫ લીટી ન થાય.</li>
<li><b>પહેલી સ્ક્રીન પર કામ.</b> ઉપરનો ભાગ ૨૨૦ px થી વધુ નહીં; પહેલી હરોળ સ્ક્રીનના ઉપરના અડધા ભાગમાં.</li>
<li><b>હરોળ, કાર્ડ નહીં.</b> એક વ્યક્તિ = એક હરોળ (૫૬–૭૬ px). પૂરી વિગત આખી સ્ક્રીનમાં ખૂલે.</li>
<li><b>લાંબાં પાનાં બંધ પટ્ટીમાં.</b> ૩ સ્ક્રીનથી લાંબું કોઈ પાનું નહીં; દરેક પટ્ટી પર ટૂંકો સાર; એક ખૂલે તો બીજી બંધ.</li>
<li><b>દિવસ માટે એક જ પટ્ટી.</b> ૨ થી ૮ ફેબ્રુ. નાં ૭ ખાનાં, બધે એક જ રીતે.</li>
<li><b>મુખ્ય બટન નીચે.</b> આખી પહોળાઈ, ૪૮ px, સ્ક્રીન પર એક જ ઘેરું બટન; જોખમી કામ લાલ. બીજાં કામ યાદી તરીકે.</li>
<li><b>ફોર્મ એક કૉલમમાં.</b> ખાનાં ૪૬ px; પસંદગી ગોળીથી, લખવું ઓછું; ભૂલ ખાનાની નીચે.</li>
<li><b>શીટ નાની.</b> ખાતરી અને નાનાં ફોર્મ નીચેથી ખૂલતી શીટમાં; બટન હંમેશાં દેખાય; કીબોર્ડ ખૂલે તો પણ.</li>
<li><b>પસંદગીની પટ્ટી જરૂર હોય ત્યારે જ.</b> કંઈ પસંદ ન હોય ત્યારે બટન-પટ્ટી છુપાયેલી.</li>
<li><b>સમજૂતી ઓછી.</b> લાંબા ખુલાસા અલગ «સમજૂતી» પાને; સ્ક્રીન પર સ્થિતિ અને કામ.</li>
<li><b>ફોન આડો.</b> ડાબી પટ્ટીમાં ચિહ્ન અને નામ; ફિલ્ટર ઉપરની પટ્ટીમાં; યાદી ૨ કૉલમ; વિગત અને ખાતરી ડાબે-જમણે વહેંચાય.</li>
<li><b>સ્પર્શ અને વાંચન.</b> દરેક બટન ઓછામાં ઓછું ૪૪ px; લખાણ ૧૨ px થી નાનું નહીં; રંગ સાથે શબ્દ પણ (ફક્ત રંગથી સ્થિતિ નહીં).</li>
</ol><p class="note" style="font-size:13.5px">નિયમ, ડેટા, પરવાનગી અને શબ્દો બદલાતા નથી; ફક્ત ફોન પરની ગોઠવણ. ટૅબ્લેટ અને લેપટોપનો દેખાવ જેમ છે તેમ રહે. નવા શબ્દ (દા.ત. શીટનાં શીર્ષક, ગોળી પરનાં કારણ) માલિકની મંજૂરી પછી જ પેનલમાં જાય.</p></div>'''
html=f'''<!doctype html>
<html lang="gu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Admin phone design A-Z (v5)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hind+Vadodara:wght@400;500;600;700&family=Noto+Serif+Gujarati:wght@600;700&display=swap">
<style>{css}</style></head><body><div class="wrap">
<h1>શ્રી વિહત મેલડી ધામ — એડમિન પેનલ · ફોન ડિઝાઇન (A થી Z) — v5</h1>
<p class="lead">દરેક પાનું, ફોર્મ, શીટ અને સ્થિતિ ફોન માટે: {total} સ્ક્રીન ({total-len(L)} ફોન ઊભો ૩૯૦×૮૪૪, {len(L)} ફોન આડો ૮૪૪×૩૯૦). રંગ, ફોન્ટ, લોગો અને શબ્દો પેનલના પોતાના. ડેટા નકલી છે.</p>
<div class="idx">{''.join(idx)}</div>
{''.join(out)}{rules}</div></body></html>'''
import re as _r
html=html.replace(f'<img class="lg" src="{RED}" alt="">','<i class="lg lr"></i>')
html=_r.sub(r'<img class="lg" style="([^"]*)" src="'+_r.escape(RED)+r'" alt="">',r'<i class="lg lr" style="\1"></i>',html)
html=html.replace(f'<img src="{RED}" alt="">','<i class="lr"></i>').replace(f'<img src="{LIGHT}" alt="">','<i class="ll"></i>')
assert RED not in html and LIGHT not in html
html=html.replace('</style>','.lr,.ll{display:block;background:center/contain no-repeat}.lr{background-image:url('+RED+')}.ll{background-image:url('+LIGHT+')}.lhead i{width:74px;height:74px}.idcard .h i{width:30px;height:30px;margin:0 auto}.empty i.lr{width:70px;height:70px;opacity:.55}</style>',1)
open('phone-design-v5.html','w',encoding='utf-8').write(html);print(len(html),total)
