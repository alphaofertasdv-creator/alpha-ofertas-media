#!/usr/bin/env python3
"""Configuração ÚNICA do token da Meta. Roda no PC do usuário; o Claude NÃO vê os segredos.

Antes: o usuário cria o arquivo  $HOME/mnt/data/meta.env  (pasta C:\\whatsapp_scheduler\\data\\meta.env) com:
  APP_ID=...        (painel do app em developers.facebook.com > Configurações do app > Básico)
  APP_SECRET=...    (mesma tela, botão Mostrar)
  SHORT_TOKEN=...   (token de usuário gerado no Graph API Explorer)
Depois:  python3 meta_setup.py
O script troca por token longo, descobre a Página e o Instagram ligados, e REESCREVE o meta.env com
  IG_USER_ID, PAGE_ID, PAGE_TOKEN (token de página que não expira), apagando APP_SECRET e SHORT_TOKEN.
Só mostra IDs e @ (nunca imprime tokens).
"""
import os, sys, json, urllib.request, urllib.parse, urllib.error

GRAPH = "https://graph.facebook.com/v21.0"
path = os.environ.get("META_ENV") or os.path.join(os.path.expanduser("~"), "mnt", "data", "meta.env")


def get(url):
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            m = json.loads(e.read().decode())["error"]["message"]
        except Exception:
            m = f"HTTP {e.code}"
        sys.exit(f"ERRO da Meta: {m}")


cfg = {}
for ln in open(path, encoding="utf-8"):
    ln = ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k, v = ln.split("=", 1)
        cfg[k.strip()] = v.strip().strip('"').strip("'")
for k in ("APP_ID", "APP_SECRET", "SHORT_TOKEN"):
    if not cfg.get(k):
        sys.exit(f"Falta {k} no meta.env")

q = urllib.parse.urlencode(dict(grant_type="fb_exchange_token", client_id=cfg["APP_ID"],
                                client_secret=cfg["APP_SECRET"], fb_exchange_token=cfg["SHORT_TOKEN"]))
long_tok = get(f"{GRAPH}/oauth/access_token?{q}")["access_token"]
pages = get(f"{GRAPH}/me/accounts?" + urllib.parse.urlencode(
    dict(fields="id,name,access_token,instagram_business_account", access_token=long_tok, limit=50)))["data"]
cand = [x for x in pages if x.get("instagram_business_account")]
if not cand:
    sys.exit("Nenhuma Página com Instagram profissional ligado. Veja se a conta do Instagram está ligada à Página e se você marcou a Página/Instagram ao gerar o token.")
if len(cand) > 1:
    print("Mais de uma Página com Instagram:", [(x["id"], x["name"]) for x in cand])
    want = cfg.get("PAGE_ID")
    cand = [x for x in cand if x["id"] == want] or sys.exit("Coloque PAGE_ID=<id> no meta.env e rode de novo.")
pg = cand[0]
ig = pg["instagram_business_account"]["id"]
un = get(f"{GRAPH}/{ig}?" + urllib.parse.urlencode(dict(fields="username", access_token=pg["access_token"]))).get("username")
open(path, "w", encoding="utf-8").write(
    f"IG_USER_ID={ig}\nPAGE_ID={pg['id']}\nPAGE_TOKEN={pg['access_token']}\n")
print(f"PRONTO. Página: {pg['name']} ({pg['id']}) | Instagram: @{un} ({ig}). meta.env regravado sem segredos temporários.")
