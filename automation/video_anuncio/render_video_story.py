#!/usr/bin/env python3
"""Story/Reels de anúncio (padrão aprovado 27/10/2026): 1080x1920, 15s, 3 telas.
Uso: python3 render_video_story.py produto.json produto.jpg saida.mp4
produto.json: {"titulo":"iPHONE 15","gancho":"PELA METADE DO PREÇO?","nome_msg":"nome real do anúncio",
               "de":7209.00,"por":3779.10}   (preços reais conferidos no ML no dia)
Zonas seguras: nada importante nos 250px do topo e 340px da base (botão 'Saiba mais' do Meta).
Gancho com 'metade' só se desconto >= 45%; senão use ex.: 'COM {pct}% DE DESCONTO'."""
import asyncio, json, os, shutil, subprocess, sys, tempfile
from playwright.async_api import async_playwright
FPS, T = 30, 15
def brl(v): return f"{v:,.0f}".replace(",", ".")
async def main(pj, img, out):
    p = json.load(open(pj)); de, por = float(p["de"]), float(p["por"])
    pct = round((de - por) / de * 100)
    gancho = p["gancho"].replace("{pct}", str(pct))
    html = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.html"), encoding="utf-8").read()
    for k, v in {"TITULO": p["titulo"], "GANCHO": gancho, "PCT": pct, "DE": brl(de), "POR": brl(por),
                 "ECON": brl(de - por), "NOME_MSG": p["nome_msg"]}.items():
        html = html.replace("{{%s}}" % k, str(v))
    tmp = tempfile.mkdtemp(); here = os.path.dirname(os.path.abspath(__file__))
    shutil.copytree(os.path.join(here, "assets"), os.path.join(tmp, "assets"))
    shutil.copy(img, os.path.join(tmp, "produto.jpg")); open(os.path.join(tmp, "v.html"), "w", encoding="utf-8").write(html)
    os.makedirs(os.path.join(tmp, "f"))
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto("file://" + os.path.join(tmp, "v.html")); await pg.wait_for_timeout(800)
        for i in range(T * FPS):
            await pg.evaluate(f"setT({i/FPS})"); await pg.screenshot(path=os.path.join(tmp, "f", f"{i:04d}.png"))
        await b.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f", "%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out], check=True)
    shutil.rmtree(tmp)
asyncio.run(main(*sys.argv[1:4]))
