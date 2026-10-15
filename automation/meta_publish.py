#!/usr/bin/env python3
"""Publica carrossel/Stories no Instagram e carrossel no Facebook pela API oficial da Meta (grátis).

Roda NO PC do usuário (device_bash), sem dependências (só stdlib).
Credenciais: arquivo meta.env (NUNCA no GitHub) em $META_ENV ou $HOME/mnt/data/meta.env
  IG_USER_ID=...   PAGE_ID=...   PAGE_TOKEN=...   (gerados por meta_setup.py)
Estado (o que já foi publicado): meta_state.json ao lado do meta.env.
Fila do dia: automation/fila-ig-AAAA-MM-DD.json no GitHub (main), lida via raw.githubusercontent.com.

Uso:
  python3 meta_publish.py --test                 # confere token, mostra @ do Instagram e nome da página
  python3 meta_publish.py --due [--lead 10]      # publica o que vence em até N min (padrão 10) e não passou de 6 h
  python3 meta_publish.py --status [--data AAAA-MM-DD]  # lista a fila do dia com o estado de cada item
  python3 meta_publish.py --due --dry            # só mostra o que publicaria

Formato da fila (lista "posts"):
  {"id":"car-19h","tipo":"carrossel","quando":"2026-10-15T19:00:00-03:00",
   "imagens":["2026-10-15/carrossel_1.jpg", ...],   # caminhos no repo, JPEG
   "legenda":"texto...","facebook":true}
  {"id":"st-0900","tipo":"story","quando":"2026-10-15T09:00:00-03:00","imagens":["2026-10-15/stories/story_1.jpg"]}
Saída: uma linha por item: OK/ERRO/PULADO + id. Código de saída 1 se algum ERRO.
"""
import os, sys, json, time, argparse, datetime as dt
import urllib.request, urllib.parse, urllib.error

GRAPH = "https://graph.facebook.com/v21.0"
RAW = "https://raw.githubusercontent.com/alphaofertasdv-creator/alpha-ofertas-media/main/"
BRT = dt.timezone(dt.timedelta(hours=-3))


def env_path():
    return os.environ.get("META_ENV") or os.path.join(os.path.expanduser("~"), "mnt", "data", "meta.env")


def load_env():
    cfg = {}
    for ln in open(env_path(), encoding="utf-8"):
        ln = ln.strip()
        if ln and not ln.startswith("#") and "=" in ln:
            k, v = ln.split("=", 1)
            cfg[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("IG_USER_ID", "PAGE_ID", "PAGE_TOKEN"):
        if not cfg.get(k):
            sys.exit(f"meta.env sem {k}. Rode meta_setup.py.")
    return cfg


def http(method, url, data=None, timeout=60):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            j = json.loads(e.read().decode())
            err = j.get("error", {})
            msg = f"{err.get('message')} (code {err.get('code')}/{err.get('error_subcode')})"
        except Exception:
            msg = f"HTTP {e.code}"
        raise RuntimeError(msg)


def g(path, token, **params):
    q = dict(params, access_token=token)
    return http("GET", f"{GRAPH}/{path}?" + urllib.parse.urlencode(q))


def p(path, token, **params):
    return http("POST", f"{GRAPH}/{path}", dict(params, access_token=token))


def wait_finished(cid, token, tries=30):
    for _ in range(tries):
        st = g(cid, token, fields="status_code,status").get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"container {cid} status {st}: {g(cid, token, fields='status').get('status')}")
        time.sleep(4)
    raise RuntimeError(f"container {cid} não ficou pronto a tempo")


def check_image(url):
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            ct = r.headers.get("Content-Type", "")
            if "jpeg" not in ct:
                raise RuntimeError(f"imagem não é JPEG ({ct}): {url}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"imagem inacessível HTTP {e.code}: {url}")


def pub_ig_carrossel(cfg, imgs, legenda):
    t, ig = cfg["PAGE_TOKEN"], cfg["IG_USER_ID"]
    kids = []
    for u in imgs:
        c = p(f"{ig}/media", t, image_url=u, is_carousel_item="true")["id"]
        wait_finished(c, t)
        kids.append(c)
    c = p(f"{ig}/media", t, media_type="CAROUSEL", children=",".join(kids), caption=legenda)["id"]
    wait_finished(c, t)
    return p(f"{ig}/media_publish", t, creation_id=c)["id"]


def pub_ig_story(cfg, img):
    t, ig = cfg["PAGE_TOKEN"], cfg["IG_USER_ID"]
    c = p(f"{ig}/media", t, image_url=img, media_type="STORIES")["id"]
    wait_finished(c, t)
    return p(f"{ig}/media_publish", t, creation_id=c)["id"]


def pub_fb_fotos(cfg, imgs, legenda):
    t, pg = cfg["PAGE_TOKEN"], cfg["PAGE_ID"]
    ids = [p(f"{pg}/photos", t, url=u, published="false")["id"] for u in imgs]
    att = {f"attached_media[{i}]": json.dumps({"media_fbid": x}) for i, x in enumerate(ids)}
    return p(f"{pg}/feed", t, message=legenda, **att)["id"]


def fetch_fila(day):
    url = f"{RAW}automation/fila-ig-{day}.json?t={int(time.time())}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--due", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--lead", type=int, default=10, help="minutos de antecedência permitidos")
    ap.add_argument("--data", help="AAAA-MM-DD (padrão: hoje em Brasília)")
    a = ap.parse_args()
    cfg = load_env()
    sp = os.path.join(os.path.dirname(env_path()), "meta_state.json")
    state = json.load(open(sp)) if os.path.exists(sp) else {}

    if a.test:
        t = cfg["PAGE_TOKEN"]
        ig = g(cfg["IG_USER_ID"], t, fields="username,media_count")
        pg = g(cfg["PAGE_ID"], t, fields="name")
        print(f"OK Instagram @{ig.get('username')} ({ig.get('media_count')} posts) | Página: {pg.get('name')}")
        try:
            lim = g(f"{cfg['IG_USER_ID']}/content_publishing_limit", t, fields="quota_usage,config")
            print("Limite de publicações/24h:", json.dumps(lim.get("data", lim), ensure_ascii=False))
        except RuntimeError as e:
            print("aviso (limite):", e)
        return

    now = dt.datetime.now(BRT)
    day = a.data or now.strftime("%Y-%m-%d")
    fila = fetch_fila(day)
    if not fila:
        print(f"PULADO sem fila-ig-{day}.json no GitHub")
        return
    erro = False
    for post in fila["posts"]:
        pid, key = post["id"], f"{day}/{post['id']}"
        quando = dt.datetime.fromisoformat(post["quando"])
        st = state.get(key, {})
        if a.status:
            print(f"{post['quando'][11:16]} {pid:10} {post['tipo']:9} {'PUBLICADO ' + str(st.get('ig', st.get('fb', ''))) if st.get('ok') else ('ERRO: ' + st['erro'] if st.get('erro') else 'pendente')}")
            continue
        if st.get("ok"):
            continue
        delta = (quando - now).total_seconds() / 60
        if delta > a.lead:
            continue
        if delta < -360:
            print(f"PULADO {pid}: passou de 6 h do horário ({post['quando']})")
            continue
        if st.get("tent", 0) >= 3:
            print(f"PULADO {pid}: 3 tentativas já falharam ({st.get('erro')})")
            continue
        imgs = [RAW + i for i in post["imagens"]]
        if a.dry:
            print(f"DRY publicaria {pid} ({post['tipo']}, {len(imgs)} img) agendado {post['quando']}")
            continue
        try:
            for u in imgs:
                check_image(u)
            res = {}
            if post["tipo"] == "carrossel":
                res["ig"] = pub_ig_carrossel(cfg, imgs, post["legenda"])
                if post.get("facebook"):
                    try:
                        res["fb"] = pub_fb_fotos(cfg, imgs, post["legenda"])
                    except RuntimeError as e:
                        res["fb_erro"] = str(e)
            else:
                res["ig"] = pub_ig_story(cfg, imgs[0])
            state[key] = dict(ok=True, quando_real=now.isoformat(timespec="seconds"), **res)
            extra = f" | FB falhou: {res['fb_erro']}" if res.get("fb_erro") else ""
            print(f"OK {pid} {post['tipo']} ig={res['ig']}{extra}")
        except Exception as e:
            tent = st.get("tent", 0) + 1
            state[key] = dict(ok=False, erro=str(e), tent=tent)
            print(f"ERRO {pid}: {e} (tentativa {tent}/3)")
            erro = True
        json.dump(state, open(sp, "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if erro else 0)


if __name__ == "__main__":
    main()
