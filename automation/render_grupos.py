import asyncio, os, sys
from playwright.async_api import async_playwright
LOGO=os.path.abspath(os.path.join(os.path.dirname(__file__),"assets/logo.png"))
OUT=sys.argv[1] if len(sys.argv)>1 else "."
G=[("⚙️","Tech & Setup"),("✨","Saúde & Beleza"),("🏡","Casa & Móveis"),("💪","Academia & Suplementos"),("👔","Moda Masculina"),("👗","Moda Feminina"),("🎣","Pesca & Camping"),("🛒","Achados do Dia")]
CSS="""
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0A0A0C;font-family:'Inter','Inter Display',sans-serif;color:#fff;-webkit-font-smoothing:antialiased}
.d{font-family:'Inter Display','Inter',sans-serif;font-weight:900;letter-spacing:-.025em}
.cv{position:relative;width:1080px;overflow:hidden;background:radial-gradient(1000px 700px at 90% 0%,rgba(255,204,0,.22),transparent 62%),radial-gradient(800px 600px at 0% 80%,rgba(255,204,0,.08),transparent 60%),linear-gradient(180deg,#0A0A0C,#111116 55%,#0A0A0C)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:60px 60px}
.glass{background:linear-gradient(180deg,rgba(255,255,255,.09),rgba(255,255,255,.035));border:1.5px solid rgba(255,255,255,.14);box-shadow:0 20px 50px rgba(0,0,0,.4)}
.y{color:#FFCC00}
"""
def head(top):
    return f'''<div style="position:absolute;left:56px;right:56px;top:{top}px;display:flex;align-items:center;justify-content:space-between">
<div style="display:flex;align-items:center;gap:18px"><img src="file://{LOGO}" style="width:84px;height:84px;border-radius:22px;box-shadow:0 10px 30px rgba(255,204,0,.25)"><div class="d" style="font-size:30px;text-transform:uppercase">Alpha Ofertas</div></div>
</div>'''
def cards(top,fs,h,gap):
    items=''.join(f'<div class="glass" style="display:flex;align-items:center;gap:22px;height:{h}px;padding:0 30px;border-radius:30px;font-size:{fs}px;font-weight:800"><span style="font-size:{fs+8}px;width:{fs+16}px;text-align:center">{e}</span><span>{t}</span></div>' for e,t in G)
    return f'<div style="position:absolute;left:56px;right:56px;top:{top}px;display:grid;grid-template-columns:1fr 1fr;gap:{gap}px">{items}</div>'
def feed():
    return f'''<html><head><meta charset="utf-8"><style>{CSS}.cv{{height:1350px}}</style></head><body><div class="cv"><div class="grid"></div>
{head(52)}
<div style="position:absolute;left:64px;right:64px;top:190px"><div class="d" style="font-size:70px;line-height:1.02;text-transform:uppercase">Você gosta de<br><span class="y">ofertas?</span></div>
<div style="margin-top:22px;font-size:34px;font-weight:700;color:#C9C9D3;line-height:1.3">Temos grupos de ofertas para cada interesse. Escolha o seu e receba ofertas todos os dias:</div></div>
{cards(540,30,104,18).replace('grid-template-columns:1fr 1fr','grid-template-columns:1fr 1fr')}
<div style="position:absolute;left:44px;right:44px;bottom:44px;height:190px;border-radius:44px;background:linear-gradient(135deg,#FFD83A,#FFCC00 55%,#F2B800);color:#0D0D0F;padding:28px 40px;box-shadow:0 30px 70px rgba(255,204,0,.25)">
<div class="d" style="font-size:52px;line-height:1;text-transform:uppercase">Clique no link da bio</div><div style="margin-top:12px;font-weight:800;font-size:30px">e entre no grupo que você mais gosta 👆</div></div>
</div></body></html>'''
def story():
    return f'''<html><head><meta charset="utf-8"><style>{CSS}.cv{{height:1920px}}</style></head><body><div class="cv"><div class="grid"></div>
{head(212)}
<div style="position:absolute;left:64px;right:64px;top:370px"><div class="d" style="font-size:88px;line-height:1.0;text-transform:uppercase">Você gosta de<br><span class="y">ofertas?</span></div>
<div style="margin-top:28px;font-size:40px;font-weight:700;color:#C9C9D3;line-height:1.3">Escolha seu grupo e receba ofertas todos os dias:</div></div>
{cards(740,34,128,20)}
<div style="position:absolute;left:64px;right:64px;top:1390px;text-align:center"><div class="d" style="font-size:58px;line-height:1.05;text-transform:uppercase">Clique no link abaixo<br><span class="y">e entre no grupo</span></div><div style="margin-top:20px;font-size:70px;line-height:1" class="y">⬇</div></div>
</div></body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for name,h,html in (("grupos_feed",1350,feed()),("grupos_story",1920,story())):
            hp=f"{OUT}/{name}.html"; open(hp,"w",encoding="utf-8").write(html)
            pg=await b.new_page(viewport={'width':1080,'height':h}); await pg.goto(f"file://{os.path.abspath(hp)}"); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f"{OUT}/{name}.png"); await pg.close(); os.remove(hp)
        await b.close()
asyncio.run(main())
