import math, asyncio, sys
from playwright.async_api import async_playwright

LOGO=__import__("os").path.abspath(__import__("os").path.join(__import__("os").path.dirname(__file__),"assets/logo.png"))
Y="#FFCC00"; K="#0D0D0F"; G="#1A1A1F"; W="#FFFFFF"; T="#A9A9B3"; GR="#20D07A"

def brl(v, dec=True):
    s=f"{v:,.2f}" if dec else f"{v:,.0f}"
    return s.replace(",","X").replace(".",",").replace("X",".")

def calc(o,p):
    pct=int(math.floor((1-p/o)*100)); eco=o-p
    return pct, eco

BASE=f"""
@font-face{{font-family:'ID';src:local('Inter Display Black'),local('InterDisplay-Black');font-weight:900}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:{K};font-family:'Inter','Inter Display',sans-serif;color:{W};-webkit-font-smoothing:antialiased}}
.d{{font-family:'Inter Display','Inter',sans-serif;font-weight:900;letter-spacing:-.02em}}
.canvas{{position:relative;overflow:hidden;background:
 radial-gradient(900px 600px at 85% -5%, rgba(255,204,0,.16), transparent 60%),
 linear-gradient(180deg,{K} 0%,#121216 100%)}}
.swoosh{{position:absolute;left:-10%;width:130%;height:420px;pointer-events:none}}
.top{{position:absolute;left:56px;right:56px;top:52px;display:flex;align-items:center;justify-content:space-between}}
.brand{{display:flex;align-items:center;gap:18px}}
.brand img{{width:84px;height:84px;border-radius:20px;display:block}}
.brand .n{{font-size:30px;line-height:1;font-weight:900;letter-spacing:.02em;text-transform:uppercase}}
.brand .n small{{display:block;font-size:17px;font-weight:600;letter-spacing:.18em;color:{T};margin-top:7px}}
.tag{{background:{Y};color:{K};font-weight:900;font-size:25px;letter-spacing:.06em;padding:15px 26px;border-radius:14px;transform:skewX(-8deg);text-transform:uppercase}}
.tag span{{display:inline-block;transform:skewX(8deg)}}
.panel{{position:absolute;background:{W};border-radius:36px;box-shadow:0 30px 70px rgba(0,0,0,.55);overflow:hidden}}
.panel img{{position:absolute;inset:6%;width:88%;height:88%;object-fit:contain;mix-blend-mode:multiply}}
.badge{{position:absolute;background:{GR};color:{K};border-radius:26px;text-align:center;transform:rotate(-7deg);box-shadow:0 14px 34px rgba(32,208,122,.35)}}
.badge b{{display:block;font-family:'Inter Display';font-weight:900;letter-spacing:-.03em;line-height:.9}}
.badge i{{display:block;font-style:normal;font-weight:800;letter-spacing:.14em;font-size:24px}}
.old{{color:{T};font-size:34px;font-weight:700}}
.old s{{text-decoration-thickness:3px}}
.price{{color:{Y};font-family:'Inter Display';font-weight:900;letter-spacing:-.045em;line-height:.85}}
.price sup{{font-size:.42em;letter-spacing:-.02em;vertical-align:top;position:relative;top:.12em;margin-left:.05em}}
.por{{font-size:30px;font-weight:800;letter-spacing:.14em;color:{T}}}
.eco{{display:inline-block;background:rgba(32,208,122,.14);border:2px solid {GR};color:{GR};font-weight:800;border-radius:999px}}
.copy{{color:{W};font-weight:800;letter-spacing:-.01em}}
.cta{{position:absolute;left:0;right:0;bottom:0;background:{Y};color:{K};display:flex;align-items:center;justify-content:space-between}}
.cta .a{{font-family:'Inter Display';font-weight:900;letter-spacing:-.02em;line-height:1.02;text-transform:uppercase}}
.cta .s{{font-weight:700;opacity:.82}}
.arrow{{background:{K};color:{Y};border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900}}
"""

SW=f"""<svg class="swoosh" viewBox="0 0 1200 420" preserveAspectRatio="none"><path d="M0 330 C 300 190, 700 120, 1200 140 L1200 175 C 760 160, 340 235, 0 395 Z" fill="{Y}" opacity=".10"/><path d="M0 380 C 340 250, 760 200, 1200 215 L1200 232 C 780 222, 380 290, 0 420 Z" fill="{Y}" opacity=".18"/></svg>"""

def top(tag):
    return f"""<div class="top"><div class="brand"><img src="file://{LOGO}"><div class="n d">Alpha Ofertas</div></div><div class="tag"><span>{tag}</span></div></div>"""

def NOTE(o,fs,mt):
    n=o.get('note')
    return f'<div style="font-size:{fs}px;font-weight:800;color:#fff;opacity:.92;margin-top:{mt}px;letter-spacing:-.01em">{n}</div>' if n else ''

def feed(o):
    pct,eco=calc(o['old'],o['price']); i,c=brl(o['price']).split(",")
    return f"""<html><head><meta charset="utf-8"><style>{BASE}</style></head><body><div class="canvas" style="width:1080px;height:1350px">{SW.replace('class="swoosh"','class="swoosh" style="top:1010px;opacity:.9"')}
{top(o['tag'])}
<div class="panel" style="left:56px;right:56px;top:180px;height:590px"><img src="{o['img']}"></div>
<div class="badge" style="right:30px;top:140px;width:250px;padding:24px 0 20px"><b style="font-size:96px">{pct}%</b><i>OFF</i></div>
<div style="position:absolute;left:64px;top:796px;right:64px">
 <div class="d" style="font-size:40px;line-height:1.08;letter-spacing:-.025em;max-height:44px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis">{o['name']}</div>
 <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-top:18px">
  <div><div class="old">DE <s>R$ {brl(o['old'])}</s></div>
  <div style="display:flex;align-items:flex-start;gap:16px;margin-top:10px"><div class="por" style="padding-top:52px">POR</div><div class="price" style="font-size:150px"><span style="font-size:.38em;letter-spacing:0;margin-right:6px">R$</span>{i}<sup>,{c}</sup></div></div></div>
  <div style="padding-bottom:10px"><div class="eco" style="font-size:26px;padding:12px 22px;white-space:nowrap;line-height:1.15;text-align:center">ECONOMIZE<br>R$ {brl(eco,False)}</div></div>
 </div>
 {NOTE(o,28,12)}
 <div class="copy" style="font-size:31px;margin-top:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{o['copy']}</div>
</div>
<div class="cta" style="height:150px;padding:0 56px"><div><div class="a" style="font-size:42px">Mais ofertas no nosso grupo</div><div class="s" style="font-size:24px;margin-top:8px">Link na bio &nbsp;•&nbsp; Entre e receba antes</div></div><div class="arrow" style="width:84px;height:84px;font-size:46px">→</div></div>
</div></body></html>"""

def story(o):
    pct,eco=calc(o['old'],o['price']); i,c=brl(o['price']).split(",")
    return f"""<html><head><meta charset="utf-8"><style>{BASE}</style></head><body><div class="canvas" style="width:1080px;height:1920px">{SW.replace('class="swoosh"','class="swoosh" style="top:1400px;opacity:.9"')}
{top(o['tag'])}
<div class="panel" style="left:56px;right:56px;top:210px;height:770px"><img src="{o['img']}"></div>
<div class="badge" style="right:28px;top:170px;width:276px;padding:28px 0 24px"><b style="font-size:110px">{pct}%</b><i style="font-size:28px">OFF</i></div>
<div style="position:absolute;left:64px;right:64px;top:1030px">
 <div class="d" style="font-size:46px;line-height:1.08;max-height:100px;overflow:hidden">{o['name']}</div>
 <div class="old" style="margin-top:26px;font-size:38px">DE <s>R$ {brl(o['old'])}</s></div>
 <div style="display:flex;align-items:flex-start;gap:18px;margin-top:8px"><div class="por" style="padding-top:62px;font-size:34px">POR</div><div class="price" style="font-size:190px"><span style="font-size:.38em;letter-spacing:0;margin-right:6px">R$</span>{i}<sup>,{c}</sup></div></div>
 <div class="eco" style="font-size:34px;padding:15px 30px;margin-top:20px">ECONOMIZE R$ {brl(eco,False)}</div>
 {NOTE(o,32,24)}
</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:330px;background:{Y};color:{K};padding:44px 60px;text-align:center">
 <div class="d" style="font-size:50px;line-height:1.02;text-transform:uppercase">Essa e outras ofertas<br>no nosso grupo</div>
 <div style="margin-top:22px;display:inline-flex;align-items:center;gap:16px;background:{K};color:{Y};border-radius:999px;padding:20px 44px;font-family:'Inter Display';font-weight:900;font-size:40px;text-transform:uppercase">👇 Entre agora</div>
</div></div></body></html>"""

def car(o,n):
    pct,eco=calc(o['old'],o['price']); i,c=brl(o['price']).split(",")
    if n==1:
        body=f"""<div class="panel" style="left:56px;right:56px;top:180px;height:700px"><img src="{o['img']}"></div>
<div class="badge" style="right:30px;top:140px;width:250px;padding:24px 0 20px"><b style="font-size:96px">{pct}%</b><i>OFF</i></div>
<div style="position:absolute;left:64px;right:64px;top:915px"><div class="d" style="font-size:44px;line-height:1.08;max-height:48px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{o['name']}</div>
<div class="old" style="margin-top:22px">DE <s>R$ {brl(o['old'])}</s></div>
<div style="display:flex;gap:16px;align-items:flex-start;margin-top:6px"><div class="por" style="padding-top:52px">POR</div><div class="price" style="font-size:160px"><span style="font-size:.38em;letter-spacing:0;margin-right:6px">R$</span>{i}<sup>,{c}</sup></div></div></div>
<div class="cta" style="height:96px;padding:0 56px"><div class="a" style="font-size:30px">Arraste e veja a oferta</div><div class="arrow" style="width:56px;height:56px;font-size:32px">→</div></div>"""
    elif n==2:
        body=f"""<div class="panel" style="left:56px;right:56px;top:180px;height:560px"><img src="{o['img']}"></div>
<div style="position:absolute;left:64px;right:64px;top:780px"><div class="d" style="font-size:54px;line-height:1.06">{o['name']}</div>
<div style="margin-top:34px;display:grid;gap:16px">{''.join(f'<div style="display:flex;gap:18px;align-items:center;font-size:36px;font-weight:700"><span style="background:{Y};color:{K};width:44px;height:44px;border-radius:12px;display:inline-flex;align-items:center;justify-content:center;font-weight:900">✓</span>{b}</div>' for b in o['bullets'])}</div>
<div class="price" style="font-size:96px;margin-top:40px"><span style="font-size:.4em;letter-spacing:0;margin-right:6px">R$</span>{i}<sup>,{c}</sup></div></div>
<div class="cta" style="height:96px;padding:0 56px"><div class="a" style="font-size:30px">Veja quanto você economiza</div><div class="arrow" style="width:56px;height:56px;font-size:32px">→</div></div>"""
    elif n==3:
        body=f"""<div style="position:absolute;left:64px;right:64px;top:250px;text-align:center">
<div class="d" style="font-size:46px;color:{T}">A OPORTUNIDADE</div>
<div class="old" style="font-size:56px;margin-top:70px">DE <s>R$ {brl(o['old'])}</s></div>
<div style="font-size:120px;color:{Y};font-weight:900;line-height:1;margin:8px 0">💬</div>
<div class="por" style="font-size:36px">POR APENAS</div>
<div class="price" style="font-size:230px;margin-top:10px"><span style="font-size:.34em;letter-spacing:0;margin-right:6px">R$</span>{i}<sup>,{c}</sup></div>
{NOTE(o,40,18)}
<div class="eco" style="font-size:48px;padding:26px 52px;margin-top:70px">VOCÊ ECONOMIZA R$ {brl(eco,False)}</div>
<div class="copy" style="font-size:38px;margin-top:70px;color:{T}">{pct}% abaixo do preço de lista.</div></div>
<div class="cta" style="height:96px;padding:0 56px"><div class="a" style="font-size:30px">Tem mais no final</div><div class="arrow" style="width:56px;height:56px;font-size:32px">→</div></div>"""
    else:
        lst=''.join(f'<div style="display:flex;gap:22px;align-items:center;font-size:44px;font-weight:800"><span style="font-size:52px">{e}</span>{t}</div>' for e,t in [("💰","Ofertas"),("🏷️","Cupons"),("🔥","Achadinhos"),("🛒","Promoções"),("⚡","Preços baixos")])
        body=f"""<div style="position:absolute;left:64px;right:64px;top:200px"><div class="d" style="font-size:78px;line-height:1.02;text-transform:uppercase">Quer receber<br><span style="color:{Y}">mais ofertas</span><br>assim?</div>
<div style="margin-top:36px;color:{T};font-size:34px;font-weight:700">Todos os dias no grupo:</div>
<div style="margin-top:28px;display:grid;gap:22px">{lst}</div></div>
<div class="cta" style="height:260px;padding:0 56px;flex-direction:column;justify-content:center;align-items:flex-start;gap:14px"><div class="a" style="font-size:66px">Entre no nosso grupo</div><div class="s" style="font-size:30px">Link na bio &nbsp;•&nbsp; 100% gratuito</div></div>"""
    return f"""<html><head><meta charset="utf-8"><style>{BASE}</style></head><body><div class="canvas" style="width:1080px;height:1350px">{SW.replace('class="swoosh"','class="swoosh" style="top:1010px;opacity:.9"')}{top(o['tag'] if n!=4 else 'GRUPO VIP')}{body}</div></body></html>"""



def story2(o):
    pct,eco=calc(o['old'],o['price']); i,c=brl(o['price']).split(",")
    note=o.get('note')
    nt=f'<div style="font-size:30px;font-weight:800;opacity:.92;margin-top:12px;letter-spacing:-.01em">{note}</div>' if note else ''
    return f"""<html><head><meta charset="utf-8"><style>{BASE}
.top2{{position:absolute;left:56px;right:56px;top:215px;display:flex;align-items:center;justify-content:space-between}}
</style></head><body><div class="canvas" style="width:1080px;height:1920px">
{SW.replace('class="swoosh"','class="swoosh" style="top:1180px;opacity:.9"')}
{top(o['tag']).replace('class="top"','class="top2"')}
<div class="panel" style="left:56px;right:56px;top:350px;height:600px"><img src="{o['img']}"></div>
<div class="badge" style="right:28px;top:318px;width:250px;padding:22px 0 18px"><b style="font-size:100px">{pct}%</b><i style="font-size:26px">OFF</i></div>
<div style="position:absolute;left:64px;right:64px;top:975px">
 <div class="d" style="font-size:44px;line-height:1.06;max-height:96px;overflow:hidden">{o['name']}</div>
 <div class="old" style="margin-top:14px;font-size:34px">DE <s>R$ {brl(o['old'])}</s></div>
 <div style="display:flex;align-items:flex-start;gap:16px;margin-top:6px"><div class="por" style="padding-top:52px;font-size:30px">POR</div><div class="price" style="font-size:158px"><span style="font-size:.38em;letter-spacing:0;margin-right:6px">R$</span>{i}<sup>,{c}</sup></div></div>
 <div style="display:flex;align-items:center;gap:20px;margin-top:16px"><div class="eco" style="font-size:30px;padding:12px 26px;white-space:nowrap">ECONOMIZE R$ {brl(eco,False)}</div>{('<div style="font-size:28px;font-weight:800;opacity:.92">'+note+'</div>') if note else ''}</div>
</div>
<div style="position:absolute;left:44px;right:44px;top:1430px;height:230px;background:{Y};border-radius:36px;color:{K};padding:30px 40px;box-shadow:0 20px 50px rgba(0,0,0,.5)">
 <div class="d" style="font-size:50px;line-height:1.02;text-transform:uppercase">Entre no nosso grupo de ofertas</div>
 <div style="font-weight:800;font-size:28px;margin-top:10px;opacity:.85">Toque no botão de link 👇</div>
</div>
</div></body></html>"""


CSS3=f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0A0A0C;font-family:'Inter','Inter Display',sans-serif;color:#fff;-webkit-font-smoothing:antialiased}}
.d{{font-family:'Inter Display','Inter',sans-serif;font-weight:900;letter-spacing:-.025em}}
.cv{{position:relative;width:1080px;height:1920px;overflow:hidden;background:
 radial-gradient(1100px 900px at 85% 18%, rgba(255,204,0,.20), transparent 62%),
 radial-gradient(900px 700px at 0% 70%, rgba(255,204,0,.07), transparent 60%),
 linear-gradient(180deg,#0A0A0C,#111116 55%,#0A0A0C)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:60px 60px;-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 20%,#000 75%,transparent 100%)}}
.big{{position:absolute;left:-30px;top:500px;font-family:'Inter Display';font-weight:900;font-size:520px;letter-spacing:-.06em;color:transparent;-webkit-text-stroke:2px rgba(255,255,255,.05);line-height:.8;white-space:nowrap;transform:rotate(-8deg)}}
.chip{{display:inline-flex;align-items:center;gap:10px;border-radius:999px;font-weight:800;letter-spacing:.04em;white-space:nowrap}}
.glass{{background:linear-gradient(180deg,rgba(255,255,255,.09),rgba(255,255,255,.035));border:1.5px solid rgba(255,255,255,.14);border-radius:40px;box-shadow:0 30px 70px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.12)}}
.price{{color:#FFCC00;font-family:'Inter Display';font-weight:900;letter-spacing:-.05em;line-height:.85;text-shadow:0 0 60px rgba(255,204,0,.28)}}
.price sup{{font-size:.4em;letter-spacing:-.02em;vertical-align:top;position:relative;top:.1em;margin-left:.05em}}
"""
def story3(o):
    pct,eco=calc(o['old'],o['price']); i,c=brl(o['price']).split(",")
    note=o.get('note') or ''
    chips=''.join(f'<span class="chip" style="background:rgba(10,10,12,.9);color:#fff;font-size:26px;padding:12px 22px;border:1.5px solid rgba(255,255,255,.18)">{t}</span>' for t in [x.strip() for x in note.replace(' • ','|').split('|') if x.strip()])
    return f"""<html><head><meta charset="utf-8"><style>{CSS3}</style></head><body><div class="cv">
<div class="grid"></div><div class="big">ALPHA</div>
<div style="position:absolute;left:56px;right:56px;top:212px;display:flex;align-items:center;justify-content:space-between">
 <div style="display:flex;align-items:center;gap:18px"><img src="file://{LOGO}" style="width:80px;height:80px;border-radius:22px;box-shadow:0 10px 30px rgba(255,204,0,.25)"><div class="d" style="font-size:30px;text-transform:uppercase;letter-spacing:.02em;line-height:1">Alpha Ofertas</div></div>
 <span class="chip" style="background:#FFCC00;color:#0D0D0F;font-size:25px;padding:14px 24px;font-weight:900">{o['tag']}</span>
</div>
<div style="position:absolute;left:56px;right:56px;top:340px;height:660px;border-radius:48px;background:radial-gradient(520px 420px at 50% 45%,#FFFFFF,#ECECF0 70%,#DADADF);box-shadow:0 40px 90px rgba(0,0,0,.6),0 0 0 2px rgba(255,255,255,.08);overflow:hidden">
 <div style="position:absolute;left:50%;bottom:60px;width:520px;height:46px;margin-left:-260px;background:radial-gradient(closest-side,rgba(0,0,0,.28),transparent);filter:blur(6px)"></div>
 <img src="{o['img']}" style="position:absolute;inset:7%;width:86%;height:86%;object-fit:contain;mix-blend-mode:multiply">
 <div style="position:absolute;left:28px;bottom:26px;display:flex;gap:12px">{chips}</div>
</div>
<div style="position:absolute;right:34px;top:300px;width:250px;height:250px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#3BE894,#20D07A 60%,#14B263);color:#0D0D0F;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-8deg);box-shadow:0 20px 50px rgba(32,208,122,.45),0 0 0 10px rgba(32,208,122,.18),0 0 0 11px rgba(32,208,122,.35)">
 <div class="d" style="font-size:104px;line-height:.9;letter-spacing:-.05em">{pct}%</div><div style="font-weight:900;letter-spacing:.2em;font-size:28px;margin-top:4px">OFF</div></div>
<div style="position:absolute;left:64px;right:64px;top:1028px"><div class="d" style="font-size:42px;line-height:1.06;max-height:90px;overflow:hidden">{o['name']}</div></div>
<div class="glass" style="position:absolute;left:56px;right:56px;top:1146px;height:262px;padding:26px 40px">
 <div style="display:flex;justify-content:space-between;align-items:center"><div style="color:#A9A9B3;font-weight:700;font-size:32px">DE <s style="text-decoration-thickness:3px">R$ {brl(o['old'])}</s></div>
 <span class="chip" style="background:rgba(32,208,122,.16);border:2px solid #20D07A;color:#3BE894;font-size:27px;padding:10px 22px">ECONOMIZE R$ {brl(eco,False)}</span></div>
 <div style="display:flex;align-items:flex-start;gap:18px;margin-top:12px"><div style="padding-top:50px;color:#A9A9B3;font-weight:800;letter-spacing:.14em;font-size:28px">POR</div><div class="price" style="font-size:168px"><span style="font-size:.36em;letter-spacing:0;margin-right:8px">R$</span>{i}<sup>,{c}</sup></div></div>
</div>
<div style="position:absolute;left:44px;right:44px;top:1442px;height:262px;border-radius:44px;background:linear-gradient(135deg,#FFD83A,#FFCC00 55%,#F2B800);color:#0D0D0F;padding:26px 36px;box-shadow:0 30px 70px rgba(255,204,0,.28)">
 <div style="display:flex;align-items:center;justify-content:space-between"><div><div style="font-weight:800;font-size:30px;letter-spacing:.18em;text-transform:uppercase;opacity:.8">Responda este Story com</div><div class="d" style="font-size:112px;line-height:.95;text-transform:uppercase;letter-spacing:-.03em;margin-top:2px">OFERTA</div></div><div style="font-size:44px;background:#0D0D0F;width:92px;height:92px;border-radius:50%;display:flex;align-items:center;justify-content:center">💬</div></div>
 <div style="position:absolute;left:36px;right:36px;bottom:20px;height:64px;background:#0D0D0F;border-radius:22px;display:flex;align-items:center;justify-content:center;font-weight:900;letter-spacing:.08em;font-size:26px;color:#FFCC00">RECEBA O LINK DOS GRUPOS NO DIRECT</div>
</div>
</div></body></html>"""

import json,os
# uso: python render_stories.py ofertas.json IMGDIR OUTDIR  (5 stories das ofertas com "story":N ou as 5 primeiras chaves)
OFJ,IMGD,OUT=sys.argv[1],sys.argv[2],sys.argv[3]
os.makedirs(OUT,exist_ok=True)
OF=json.load(open(OFJ))
order=[k for k,v in sorted(OF.items(), key=lambda kv: kv[1].get('story',99)) ][:5]
async def main():
    out={}
    for n,k in enumerate(order,1):
        o={**OF[k],'img':os.path.abspath(f'{IMGD}/{k}.jpg'),'n':n}; out[f'story_{n}_{k}']=story3(o)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for k,h in out.items():
            hp=f'{OUT}/{k}.html'; open(hp,"w",encoding="utf-8").write(h)
            pg=await b.new_page(viewport={'width':1080,'height':1920})
            await pg.goto(f'file://{os.path.abspath(hp)}'); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'{OUT}/{k}.png'); await pg.close()
        await b.close()
asyncio.run(main())
