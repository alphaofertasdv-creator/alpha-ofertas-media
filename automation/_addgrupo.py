import json,sys,re
grp,raw,cat=sys.argv[1],sys.argv[2],sys.argv[3]
p=json.load(open('/home/claude/alpha-ofertas-media/automation/plano-2026-10-15.json'))
rows=json.load(open(raw))
def tit(t):
    t=re.sub(r'\s+',' ',t).strip()
    if len(t)>95:
        t=t[:95].rsplit(' ',1)[0].rstrip(' ,;:-–')
    return t
ofs=[]
for r in rows:
    id,t,de,por,rat,link,img=r
    ofs.append(dict(id=id,link_afiliado=link,titulo=tit(t),de=de,por=por,rating=rat,imagem_url='https://http2.mlstatic.com/'+img if not img.startswith('http') else img,categoria=cat,slot=None))
p['grupos'][grp]={"ofertas":ofs,"pronto":True}
json.dump(p,open('/home/claude/alpha-ofertas-media/automation/plano-2026-10-15.json','w'),ensure_ascii=False,indent=1)
# historico
h=json.load(open('/home/claude/alpha-ofertas-media/automation/historico.json'))
for o in ofs: h.append(dict(id=o['id'],data='2026-10-15',chave='fill',link=o['link_afiliado'],uso='grupo:'+grp))
json.dump(h,open('/home/claude/alpha-ofertas-media/automation/historico.json','w'),ensure_ascii=False,indent=1)
print(grp,len(ofs))
