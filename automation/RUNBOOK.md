# Alpha Ofertas — Rotina diária (executar sozinha, sem perguntar)

Idioma: português do Brasil. Fuso: America/Sao_Paulo (UTC-3). A rotina roda em ETAPAS ENCADEADAS (ver 'Etapas' abaixo) e roda ao vivo no Chrome do usuário (ferramentas `mcp__claude-in-chrome__*` ou `mcp__remote-devices__*`) e no app local da Central de Promoções (http://localhost:8501).
O usuário NÃO vai responder durante a execução: decida sozinho, registre o que fez e entregue um resumo final. Nunca invente preço, link, desconto ou dado. Se algo não puder ser verificado, NÃO publique aquele item.

## 0. Pré-checagem (abortar com aviso se falhar)
- Chrome acessível (tabs_context_mcp). Mercado Livre logado em /afiliados/linkbuilder. Metricool acessível (getBrandSettings, blogId 7353400). Se o ML estiver deslogado ou o Chrome inacessível: NÃO gere links, NÃO publique nada, e termine com um resumo dizendo exatamente o que faltou. O usuário faz login; você nunca digita senha, nem cria conta.
- Clonar/atualizar o repo `alphaofertasdv-creator/alpha-ofertas-media` (ferramenta add_repo com acesso push, depois clone). Usar a pasta `automation/` para os geradores.

## 1. Escolha das ofertas do dia (ML)
- Fonte: páginas de ofertas por categoria do ML (`/ofertas?container_id=MLB779362-1&category=MLBxxxx&page=N`).
- Regras: preço tirado da PÁGINA DO PRODUTO (`/p/MLB<id>`, fonte da verdade); desconto real >= 20%; marcas conhecidas; nota >= 4,6 quando houver; categorias variadas (alternar categorias parecidas); sem repetir produto nos últimos 7 dias (consultar tabela `produtos_postados` do app local e `automation/historico.json`).
- Preço: usar o preço normal à vista (“no Pix” se for o principal; senão “em outros meios”). “Com Saldo no Mercado Pago” é condicional: NÃO usar. Parcelamento só se sem juros.
- Item que o linkbuilder recusar (“não cumpre os requisitos do Programa”) é descartado.

## 2. Links de afiliado (um por vez, nunca em paralelo)
- Em /afiliados/linkbuilder gerar o link de cada produto individualmente; ler o link no TEXTAREA. Conferir cada link: abrir o meli.la e confirmar que o 1º `/p/MLB` do perfil é o produto certo. Conferir link ↔ produto ↔ preço ↔ foto antes de usar. Registrar em `automation/historico.json` (id, data, grupo/uso).

## 3. WhatsApp (sistema local, Streamlit “Importar Lote”)
- Cadência APROVADA: 1 envio por grupo por HORA (Intervalo 60), ~5-6 ofertas/grupo/dia (8 grupos; grupo de teste NÃO usar). ~170 posts verificados/dia não é realista. Na Importar Lote: Desconto mínimo 20, Máx. por categoria 5 (3 descarta itens), Dias sem repetir 7.
- Só agende horários FUTUROS: confira a hora real com `date`/current_time antes (já houve erro de relógio).
- Usar a página “Importar Lote” (http://localhost:8501) com o JSON do importador: id_produto, link_produto, link_afiliado, titulo, preco_original, preco_atual, preco_pix, parcelas, valor_parcela, avaliacao, categoria, imagem_url, frete_gratis, cupom_codigo, cupom_descricao. Agendar cada oferta para o grupo/nicho certo e o horário do slot.
- Formato da mensagem: `Título 🔥 [Oferta Mercado Livre]` / `De: R$ X` (só se desconto real >= 20%) / `🔥 Por: R$ Y NO PIX` (+ `ou em até Nx de R$ Z no cartão` só se sem juros) / `🛍️ PEGAR PROMOÇÃO:` / link meli.la.
- Se não houver oferta boa o suficiente para um slot/nicho (ex.: Pesca & Camping), deixe o slot vazio — qualidade antes de quantidade.
- Posts já enviados não podem ser editados. Nunca excluir agendamentos existentes. Fazer backup do app.db antes de qualquer escrita direta.

## 4. Instagram + Facebook (Metricool, blogId 7353400)
Escolher 6 das ofertas do dia (variadas): 1 para o carrossel (`"car":1`) e 5 para Stories (`"story":1..5`). Montar `ofertas_hoje.json` no formato de `automation/exemplo_ofertas.json` (name, old, price, tag, note, bullets, car/story, copy). Baixar a foto de alta resolução do produto (`https://http2.mlstatic.com/D_NQ_NP_2X_<id>-F.webp`) e converter para `<chave>.jpg` em uma pasta de imagens.

Gerar as imagens (Playwright/Chromium já instalado, fontes Inter do sistema):
```
python automation/render_carousel.py ofertas_hoje.json IMGDIR OUT/carrossel   # 4 slides 1080x1350
python automation/render_stories.py  ofertas_hoje.json IMGDIR OUT/stories     # 5 stories 1080x1920
```
Conferir visualmente cada PNG (Read na imagem): texto cortado, preço certo, foto certa. Corrigir antes de publicar.

Hospedagem das imagens: copiar para `YYYY-MM-DD/` e `YYYY-MM-DD/stories/` do repo, `git push`, usar `https://raw.githubusercontent.com/alphaofertasdv-creator/alpha-ofertas-media/main/...`.

Agendar no Metricool (createScheduledPost: parâmetros `blogId`, `date` no formato `2026-10-11T19:00:00-03:00`, `info` = JSON do post; updateScheduledPost exige `blogId`, `id` e `uuid`):
- Carrossel: 4 imagens, Instagram + Facebook, autoPublish true, às 19:00.
- Stories: 5 imagens, Instagram, `instagramData:{"type":"STORY","autoPublish":true}`, às 09:00, 11:30, 14:00, 16:30, 20:30. Sem texto no post.
- Se o horário já passou, usar o próximo horário livre de 30 em 30 min; nunca no mesmo minuto de outro post.
- Legenda do carrossel (exatamente neste formato):
```
🔥 <Nome do produto>
De R$ <de> por R$ <por> (<X>% OFF)<, ou em até Nx de R$ Y sem juros no cartão — só se existir>.

📲 Quer mais ofertas como essa? Entre nos nossos grupos pelo link da bio.
💬 Comente OFERTA ou EU QUERO que a gente te manda o link dos grupos no direct.

*Preços e estoque podem mudar a qualquer momento.
#ofertas #promoção #mercadolivre #<marca> #achadinhos
```
- O link dos grupos (único link usado em Instagram/Story/DM): https://alphaofertas.netlify.app
- A DM automática (comentário e resposta de Story) já é feita pelo Dealism para QUALQUER post/story. Não mexer nas automações do Dealism. O ManyChat está desligado: não ligar.


## Avisos no WhatsApp (grupo AVISO CLAUDE) — OBRIGATÓRIO
Sempre que houver ERRO, travamento, ferramenta indisponível, login pedido (Mercado Livre/Metricool/Dealism), pedido de permissão/aprovação, ou o término da rotina, envie uma mensagem curta em pt-BR ao grupo de avisos do próprio usuário:
- groupId: `120363431585808670@g.us` (nome "AVISO CLAUDE")
- Como enviar: abra uma aba nova em `http://localhost:3000/groups` no Chrome do usuário (a API local do WhatsApp) e, nessa aba, rode no javascript_tool:
  `fetch('/send-group-message',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({groupId:'120363431585808670@g.us',message:'<texto>'})}).then(r=>r.text())`
  Resposta esperada: `{"success":true,...}`. (Se `/groups` não responder, o Docker do WhatsApp está parado: avise no resumo final.)
- Mensagem: começar com ⚠️ (problema/pedido de ação) ou ✅ (concluído), dizer o que aconteceu e o que o usuário precisa fazer (ex.: "⚠️ Mercado Livre deslogado — faça login e me avise").
- SEMPRE enviar: (1) ao INÍCIO, logo após a pré-checagem: `🚀 Rotina Alpha Ofertas iniciada às HH:MM` (ou ⚠️ se a pré-checagem falhar); (2) a cada problema relevante ao longo da execução (sem spam: no máximo 1 mensagem por problema); (3) ao FIM: `✅ Rotina finalizada às HH:MM` + 3-4 linhas de resumo (WhatsApp: quantas ofertas agendadas; carrossel: produto/preço/horário; Stories: horários), ou `⚠️` com o que falhou/ficou de fora e o que o usuário precisa fazer. Nunca enviar nada para os grupos de ofertas fora do agendamento normal.

## Progresso a cada 30 minutos (grupo AVISO CLAUDE)
- Anote a hora de início. Depois do aviso de início, a cada ~30 minutos de execução (sempre que concluir uma etapa/lote e já tiverem passado 30 min desde o último aviso), envie ao grupo: `⏳ Rotina Alpha Ofertas: ~XX% concluída (HH:MM). Feito: <resumo>. Falta: <resumo>.`
- Estimativa de % (pesos): pré-checagem 5% · escolha das ofertas 15% · links verificados 30% · WhatsApp agendado 30% · imagens + carrossel/Stories no Metricool 15% · resumo/avisos 5%. Dentro de cada etapa, proporcional ao que já foi feito (ex.: 120 de 240 links = 15%). Nunca passe de 99% antes do aviso final de conclusão.
- Se uma etapa passar de 30 min sem terminar, envie o aviso mesmo assim durante a etapa (verifique a hora com `date` entre os lotes).

## 5. Resumo final (obrigatório)
Terminar com mensagem curta em pt-BR: o que foi agendado (WhatsApp: quantos por grupo; carrossel: produto/preço/horário; Stories: produto/preço/horário), o que ficou de fora e por quê, e qualquer erro. Se falhar tudo, diga o motivo e o que o usuário deve fazer.

## Regras fixas
- Nunca digitar senhas/credenciais, nem criar contas. Nunca excluir dados permanentemente. Nunca enviar mensagem em nome do usuário além do que está neste manual.
- Template visual aprovado: não alterar os geradores sem pedido do usuário.
- Prioridade: dado correto > volume. Em dúvida, não publique o item e registre no resumo.

## Lições operacionais
- Linkbuilder: o botão “Gerar” só responde a clique por ref (find → ref), não por coordenada; faça scrollTo(0,0) antes de cada URL. Aba em segundo plano congela: use aba em primeiro plano.
- Colar JSON na Importar Lote via textarea auxiliar (helper) e não digitando. Saída de JS trunca ~1000 chars.
- Não usar preco_pix (parse instável). Preço = página do produto.
- Alertas: aba em http://localhost:3000/groups precisa estar em primeiro plano (navegue-a antes de enviar).
- Páginas de busca do ML não servem; use /ofertas por categoria. Pesca/Moda Fem têm poucas ofertas de marca: deixe slots vazios.
- Títulos: não truncar em 60 chars no meio de palavra.

## Etapas encadeadas (cada uma avisa início/fim no AVISO CLAUDE)
Meta WhatsApp: 1 oferta por HORA em cada um dos 8 grupos, 08:00 até 18:00 (até 11 por grupo; grupos com pouca oferta de marca, como Pesca e Moda Feminina, podem ter menos: qualidade antes de volume). Só horários futuros.
Plano do dia: `automation/plano-AAAA-MM-DD.json` com `{"ig":{carrossel, stories[5], pronto:bool}, "grupos":{<grupo>:{"ofertas":[{id,link_afiliado,titulo,de,por,rating,imagem_url,categoria,slot}], "pronto":bool}}, "completo":bool}`. Commit/push depois de cada grupo concluído (protege contra perda de contexto).
1a. 04:00 Preparo A: pré-checagem; PRIMEIRO escolher as 6 ofertas do Instagram (1 carrossel + 5 Stories) e marcar `ig.pronto`; depois grupos Tech, Saúde, Casa, Academia (links um a um, preço da página do produto).
1b. 04:50 Preparo B: grupos Moda Masculina, Moda Feminina, Pesca & Camping, Achados do Dia; ao fim `completo=true`; atualizar historico.json.
2. 05:30 WhatsApp: agenda na Importar Lote os grupos já `pronto`; se faltar grupo, espera/repete (consulta o plano a cada 5 min) até 07:30; depois verificação 100%.
3. 06:30 IG/FB: gerar imagens (checar TODAS visualmente), carrossel 19:00 + 5 Stories (09:00, 11:30, 14:00, 16:30, 20:30) via Metricool; avisar horários reais no grupo. Depende só de `ig.pronto`.
4. 07:30 Verificação final (WhatsApp + Metricool) + resumo no AVISO CLAUDE.
Alertas a cada ~30 min com %. Travou/captcha/aceite → ⚠️ PRECISO DE VOCÊ.

## Travas e pedidos de aprovação (OBRIGATÓRIO)
- Se QUALQUER coisa travar e exigir clique/aceite do usuário no computador (pedido de permissão do Claude/Chrome, login, captcha, popup, extensão pedindo acesso, ferramenta bloqueada, tela inesperada), PARE de tentar em loop e envie NA HORA ao grupo AVISO CLAUDE: `⚠️ PRECISO DE VOCÊ: <o que está pedindo e onde (app/aba)>. Etapa: <nome>. Aceite/resolva e eu continuo.` Depois aguarde e tente de novo; se continuar travado após ~10 min, reenvie 1 lembrete (máx. 1 a cada 10 min). Se não conseguir enviar o alerta (Docker do WhatsApp parado), registre no resumo.

## Aviso dos Stories agendados (OBRIGATÓRIO, etapa 3)
- Depois de agendar o carrossel e os 5 Stories no Metricool, envie ao AVISO CLAUDE: `📲 Agendado hoje: Carrossel HH:MM (<produto>) · Stories: HH:MM <produto> / HH:MM <produto> / ...` com os horários e produtos REAIS lidos de getScheduledPosts (não de memória).

## Verificação 100% de preço/link/texto (OBRIGATÓRIA antes de qualquer envio) — aprendida em 11/10
Em 11/10, 6 de 35 postagens agendadas estavam com preço defasado (preço muda entre a escolha e a conferência). Por isso:
1. Etapa 2 (WhatsApp) termina com a verificação; a etapa 4 (07:30) repete. Fonte: banco `app.db` (via device_bash em `$HOME/mnt/data/app.db`, SOMENTE LEITURA, nunca escrever direto: gerou "disk I/O error"/journal). Query: schedules(status='pending') JOIN campaigns(message, link) JOIN groups.
2. Para cada pendente: extrair "De/Por" da mensagem e abrir a página do produto (`/p/MLB…` ou `/up/MLBU…`) por NAVEGAÇÃO normal, com 3 s entre páginas (nunca fetch em rajada: disparou captcha do ML). Ler `.ui-pdp-price__second-line` (Por) e `.ui-pdp-price__original-value` (De). Comparar com a mensagem; recalcular desconto (>= 20%).
3. Divergiu (preço ≠, desconto < 20%, produto indisponível): a Central NÃO edita texto (só data/hora ou excluir). Correção = excluir a postagem pendente errada (aba Já Agendadas → lixeira → confirmar; só pendentes) e reagendar pela Importar Lote com o preço atual (Dias sem repetir = 0 para esse reenvio; prévia deve mostrar horário/preço certos). Se desconto < 20%, não reagendar.
4. Se aparecer captcha/“Por segurança, complete esta etapa”: NÃO tentar resolver; alerta ⚠️ PRECISO DE VOCÊ no AVISO CLAUDE e aguardar.
5. Resultado da verificação vai no resumo (quantas conferidas, quantas corrigidas).
6. Grupo na Importar Lote: escolher clicando na opção (digitar “Pesca” selecionou Academia).

## Imagens do Instagram: texto/emoji quebrado (corrigido em 12/10)
- Em 11/10 o slide 4 do carrossel saiu com mojibake ("PreÃ§os", "GRÃ¢TIS", emojis em símbolos): o HTML era gravado sem charset. Corrigido nos geradores (`<meta charset="utf-8">` + `open(...,encoding="utf-8")`). Não reverter.
- OBRIGATÓRIO: abrir (Read) TODOS os PNGs gerados (4 slides + 5 stories) e confirmar acentos/emojis/preço antes de publicar. Se aparecer qualquer caractere estranho, corrigir e regerar; não agendar imagem com texto quebrado.

## Modo sem o usuário (ele dorme até tarde) — não parar por bloqueio
- Captcha/aceite/travamento: envie o alerta ⚠️, mas NÃO fique parado: tente de novo a cada 10 min e, entre as tentativas, avance com tudo o que não dependa do bloqueio (ex.: captcha do ML → continue agendando o que já está no plano; gerar imagens; Metricool).
- Prioridade se faltar tempo: (1) carrossel + Stories, (2) WhatsApp dos horários mais próximos, (3) resto. Nunca agende item com preço não verificado: melhor slot vazio.
- Aba do Chrome que não responde (JS timeout): abra aba nova e siga. Docker/WhatsApp local fora do ar: avise no resumo (não há como alertar no grupo).
- Se nada puder ser feito, o resumo final diz exatamente o que faltou e o que o usuário deve fazer ao acordar.

## Instagram/Facebook: um nicho diferente por post (regra do usuário, 12/10)
- NUNCA repetir o mesmo tipo de produto em dias seguidos. Nichos: Tech/Celular, Saúde & Beleza, Casa & Eletrodomésticos, Academia & Suplementos (ex.: creatina), Moda Masculina (tênis, roupa), Moda Feminina, Pesca & Camping, Achados do Dia.
- CARROSSEL: 1 produto de UM nicho por dia, rodando entre os nichos: escolha o nicho que está há mais tempo sem carrossel (consulte `automation/historico.json`, campos `uso`="carrossel" e `chave`/nicho; ontem 11/10 e hoje 12/10 foram celular/Tech, então Tech fica de fora por vários dias). Dentro do nicho, produto diferente (ex.: um dia tênis, outro eletrodoméstico, outro creatina).
- STORIES: 5 Stories, cada um de um NICHO DIFERENTE, e diferente do nicho do carrossel (1 de cada nicho; rodar os nichos de dia para dia para todos aparecerem).
- Mesmas regras de qualidade: preço da página do produto, desconto >= 20%, marca conhecida, não repetir produto em 7 dias.
- Ao registrar no historico.json de carrossel/Stories, gravar também o campo `nicho`.

## ATUALIZAÇÃO 12/10 — MOVIMENTO NOS GRUPOS (SOBREPÕE regras anteriores de cadência e filtros)
Objetivo do usuário: os grupos precisam ter envio e movimento o dia inteiro.
**Cadência:** 1 envio a cada 30 MINUTOS em cada um dos 8 grupos, das 08:00 às 20:00 (25 horários por grupo). Na Importar Lote: Intervalo 30, Primeiro 08:00, Último 20:00 (ou o trecho do lote). Se não houver ofertas verificadas para todos os horários, ESPALHE as disponíveis ao longo do dia (não gaste tudo de manhã); priorize não deixar a tarde/noite vazias. Nunca invente/relaxe a verificação de preço para encher horário.
**Filtros ampliados:**
1. Mais fontes (além de `/ofertas?container_id=MLB779362-1&category=...`): páginas de mais vendidos, ofertas relâmpago/do dia, cupons e páginas de marcas/lojas oficiais do Mercado Livre; varrer várias páginas (page=1..N) de cada categoria e subcategorias. Toda oferta continua sendo verificada na PÁGINA do produto.
2. Desconto mínimo 15% (antes 20%). Ordem de preferência: >= 20% primeiro; usar 15–19% para completar horários. Na Importar Lote: Desconto mínimo 15. (Exige-se preço original real na página.)
4. Não repetir o mesmo produto por 4 dias (antes 7). Pode repetir antes disso SE o preço atual caiu ainda mais (>= 5% menor que o postado). Na Importar Lote: Dias sem repetir 4.
Mantidos: marca conhecida/boa reputação (nota >= 4,6 quando houver), verificação 100% de preço/link, captcha = alerta, nicho diferente no carrossel/Stories.
**Rodadas ao longo do dia (porque são ~200 postagens):** além das etapas 1a/1b/2 (madrugada), há reforços às 08:30 (horários 13:00–16:30), 11:30 (17:00–20:00) e 14:30 (reposição de buracos e noite): cada reforço busca ofertas, gera links um a um, agenda e verifica 100%, só em horários futuros, e avisa no AVISO CLAUDE.

## Falhas de envio no WhatsApp (adicionado 12/10)
Caso real: em 12/10 o envio das 12:00 (Tech, Power Bank Baseus) falhou com `500: {"message":"Error in workflow"}` (n8n), `attempts=1`, sem nova tentativa. Dias anteriores (06/10 e 08/10) também tiveram falhas. Regra a partir de agora:
- Toda etapa de verificação/reforço (07:30, 08:30, 11:30, 14:30) consulta app.db (somente leitura): `select s.id,s.run_at,g.name,c.title,s.last_error from schedules s join groups g on g.id=s.group_id join campaigns c on c.id=s.campaign_id where s.status='failed' and date(s.run_at)=date('now','localtime')`.
- Para cada falha de hoje: (1) conferir se n8n/whatsapp_service respondem (GET http://localhost:3000/groups em aba em primeiro plano); (2) reverificar preço/link na página do produto; (3) se ainda válido e ainda dá tempo (<= 20:00), reagendar na Importar Lote no PRÓXIMO horário livre do mesmo grupo (Dias sem repetir 0); (4) nunca reenviar duplicado: se `sent_at` preenchido, não é falha; (5) avisar no AVISO CLAUDE: `⚠️ Falha de envio HH:MM <grupo> <produto>: <erro> → reagendado HH:MM` (ou motivo de não reagendar).
- Se 2+ falhas com "Error in workflow" aparecem em menos de 1 hora, tratar como n8n com problema: ⚠️ PRECISO DE VOCÊ (verificar o n8n/Docker) em vez de reagendar em massa.

## AJUSTES 12/10 NOITE — preço atual no momento do envio + banco de ofertas
**1. Rechecagem dos próximos envios (reforços 08:30, 11:30, 14:30 e Etapa 4 07:30).** O preço verificado às 05:30 pode mudar até o envio (caso real 12/10: Tênis Reserva planejado R$ 194,15, página R$ 259,19). Em cada reforço, além de preencher buracos: liste as postagens PENDENTES dos próximos ~3 horas (app.db somente leitura: schedules status='pending' com run_at entre agora e agora+3h, com campaigns.message e link) e reconfira cada uma na PÁGINA do produto (navegação normal, ~3 s entre páginas, captcha = alerta). Se preço/desconto diverge (>1%) ou produto indisponível: excluir o agendamento pela Central (lixeira → 'Confirmar exclusão') e reimportar com o texto/preço corrigido no MESMO horário (Importar Lote, Dias sem repetir 0), ou deixar o horário vazio se o desconto ficou < 15%. Avisar no AVISO CLAUDE: `🔁 Preço atualizado antes do envio: <produto> R$ X → R$ Y (<grupo> HH:MM)`. Nunca deixar passar um envio com preço divergente. Quem fica a menos de 15 min do envio e não deu tempo de reconferir: priorize reconferir esses primeiro.
**2. Banco de ofertas (`automation/banco-ofertas.json`).** Ao fim de cada dia, ofertas boas e verificadas que SOBRARAM (não agendadas) são gravadas com {id, link_afiliado, titulo, categoria, nicho, de, por, rating, imagem_url, data_verificacao}. No dia seguinte, o preparo (1a/1b) pode usá-las para completar horários SOMENTE depois de reverificar preço/desconto/link na página do produto de hoje (preço antigo nunca é usado). Descartar do banco itens com mais de 5 dias, que repitam (regra de 4 dias do histórico) ou que não passem na reverificação.
**3. Prioridade de horários.** Horários próximos do envio têm prioridade de verificação. Horários vazios são melhores que oferta com preço velho.

## PADRÃO DE AVISOS (12/10 noite) — SUBSTITUI os formatos de aviso anteriores
Objetivo: o usuário lê em 5 segundos, no celular, e entende o que aconteceu e se precisa fazer algo. Vale para TODAS as etapas, reforços e a vigia. Português simples, sem jargão (nada de "app.db", "n8n workflow", "Importar Lote", IDs; diga "agendamento", "grupo Tech", "envio das 12:00"). Máximo ~6 linhas. Uma ideia por mensagem. Sempre no AVISO CLAUDE.

**Três níveis (o emoji da 1ª linha diz tudo):**
- 🔴 *PRECISO DE VOCÊ* — só quando a rotina NÃO consegue seguir sozinha. Formato:
  `🔴 PRECISO DE VOCÊ`
  `O que aconteceu: <1 frase simples>`
  `O que fazer: <passo concreto, ex.: "abra o Chrome e resolva o captcha do Mercado Livre">`
  `Depois disso: <o que a rotina faz sozinha>`
  Repetir no máximo a cada 10 min enquanto não resolvido.
- 🟡 *ATENÇÃO (já resolvido ou sem ação sua)* — algo deu errado/mudou e a rotina tratou. Formato:
  `🟡 <o que houve em 1 frase>` + `✔ Resolvido: <o que foi feito>` + (se couber) `Sem ação sua.`
  Ex.: `🟡 O envio das 12:00 no grupo Tech falhou (erro do sistema de envio).` / `✔ Reenviado às 12:06.` Ex. preço: `🟡 Preço mudou: Tênis Reserva R$ 194,15 → R$ 259,19 (grupo Moda Masc. 12:00)` / `✔ Texto corrigido antes do envio.`
- 🟢 *TUDO CERTO* — só nos marcos: início do dia e resumo final. Nada de aviso de progresso por % (removido).

**Resumo final do dia (07:30, Etapa 4) — formato fixo:**
```
🟢 RESUMO DO DIA dd/mm
📅 WhatsApp: X de Y envios agendados (08:00–20:00)
   Tech N · Saúde N · Casa N · Academia N · Moda M. N · Moda F. N · Pesca N · Achados N
📸 Instagram: Carrossel 19:00 – <produto> (<nicho>) · Stories: 09:00 <produto>, 11:30 ..., (nicho de cada)
🔎 Conferidos na página do produto: X · Corrigidos: Y
⚠️ Horários vazios: <lista curta ou "nenhum">
👉 Você precisa fazer algo? NÃO / SIM: <o quê>
```
**Resumo da noite (último reforço 14:30 ou fim do dia):** mesma ideia curta com quantos envios saíram, quantos falharam e foram reenviados.

**Menos ruído:** NÃO mandar avisos de progresso a cada 30 min nem de início de cada etapa. Mandar: (1) 🟢 início do dia (04:00, 1 linha), (2) 🟡/🔴 quando houver algo, (3) o resumo final das 07:30, (4) os horários reais dos Stories/carrossel (📲 uma mensagem), (5) um resumo curto ao fim de cada reforço SÓ se algo foi corrigido/agendado. Se nada aconteceu, silêncio.

## REGRA "NENHUM GRUPO FICA SEM OFERTA" (13/10) — SOBREPÕE filtros anteriores só quando faltar oferta
Diagnóstico 13/10 (09:46): o preparo da madrugada achou só 82 ofertas verificadas para 200 horários (41%); Pesca & Camping 4, Moda Feminina 7, Tech 14, Saúde 9. Causas: (1) filtros estritos por nicho (desconto ≥15%, nota ≥4,6/marca conhecida, 4 dias sem repetir, máx 5 por categoria) com histórico de 223 produtos já usados; (2) nichos pequenos (Pesca, Moda Fem.) têm poucas ofertas boas por dia; (3) o gargalo é a velocidade: cada oferta exige página do produto + link de afiliado gerado um a um (~3 s entre páginas), então a madrugada não alcança 200.
**Regra:** todo horário de 30 min de cada grupo, das 08:00 às 20:00, deve ter oferta. Ordem de preenchimento por grupo: (1) ofertas do nicho com os filtros normais; (2) se faltar, relaxar na ordem: desconto mínimo 10% (preferir ≥15%), nota ≥4,5, repetição 2 dias (preço igual ou menor), máx. por categoria 8; (3) se ainda faltar, preencher com ofertas de nichos VIZINHOS (Pesca ← esporte/outdoor/ferramentas/automotivo/viagem; Moda Fem. ← beleza/bolsas/acessórios/calçados/lingerie; Moda Masc. ← calçados/relógios/acessórios; Casa ← cozinha/organização/jardim/ferramentas; Tech ← games/áudio/informática/acessórios celular; Saúde ← beleza/cuidados/farmácia/bem-estar; Academia ← esporte/suplementos/roupas fitness) e, por último, melhores "Achados" gerais. NUNCA relaxar: preço verificado na PÁGINA do produto, link de afiliado correto, produto disponível, original/preço de lista real.
**Prioridade de horário:** preencher primeiro os horários mais próximos de agora e ir adiante; distribuir ofertas entre os grupos em rodízio (não completar um grupo e deixar outros vazios).
**Meta de volume:** buscar pelo menos 2x o necessário (≥50 candidatas por grupo) para sobrar após a verificação. Usar `banco-ofertas.json` e sobras de dias anteriores (reverificando preço). Guardar o excedente no banco.
**Aviso:** ao fim de cada rodada, se ainda houver horário vazio num grupo, 🟡 com a lista curta ("Pesca: 15:30, 16:00 sem oferta") e o motivo em uma frase.

## AJUSTES 13/10 NOITE (balanço do dia)
Balanço 13/10: WhatsApp 170 enviados, 0 falhas, 24 pendentes normais (19:00–20:00). Instagram: 4 Stories publicados, carrossel 19:00 e Story 20:30 pendentes. Falhas de execução: nenhuma.
Problemas: (1) 6 horários vazios entre 09:00 e 10:30 (Pesca 09:00/09:30/10:00, Moda Feminina 10:00, Achados 09:30/10:00): faltou oferta nos grupos fracos e o reforço só preencheu depois das 10:30. (2) O Vigia encerrava em ~25 s em vez de ficar 60 min.
Regras novas:
- Grupos "fracos" (Pesca & Camping, Moda Feminina, Achados do Dia): na Etapa 1b começar por eles, buscar 2x o necessário, já usar nichos vizinhos/achados para horários 08:00–12:30.
- Etapa 2 (05:30) e Etapa 4 (07:30): NÃO apenas listar buracos — PREENCHER todo horário vazio antes das 11:00 (e os demais futuros) pela REGRA NENHUM GRUPO FICA SEM OFERTA. Nenhum buraco antes das 11:00 deve sobrar às 08:00.
- Existe o grupo "teste agendador wpp" na Central: IGNORAR. Só valem os 8 grupos "AlphaOfertas | ...".
- Vigia: roda a cada 30 min (:28 e :58, das 07:28 às 19:58), uma checagem por execução; falha encontrada é corrigida e reenviada uma única vez (alvo: run_at + 5 min; se já passou, logo após corrigir).

## REGRA DOS TEXTOS DO CARROSSEL/STORIES (13/10 noite)
PROIBIDO nos bullets/textos das imagens do Instagram: "Nota X no Mercado Livre", estrelas, avaliações, "Mercado Livre" ou "% abaixo do preço de lista". O público quer saber COMO É O PRODUTO.
Os 3 bullets (`bullets`) devem ser DETALHES REAIS DO ITEM, lidos da página do produto (ficha técnica/descrição): material, tamanho/capacidade/voltagem/potência, cor, modelo, quantidade/kit, o que acompanha, principal diferencial de uso (ex.: tênis → "Cabedal em mesh respirável", "Solado de borracha antiderrapante", "Para corrida e treino"). Curtos (até ~35 caracteres), sem inventar nada que não esteja na página.
Os geradores (render_carousel.py / render_stories.py) agora RECUSAM bullets com nota/estrela/Mercado Livre/% abaixo da lista; se der erro, reescrever os bullets e regerar.

## 4-B. INSTAGRAM/FACEBOOK PELA API DA META (substitui o Metricool — plano do Metricool estourou em 14/10)
**Qual modo usar:** na PC, `curl -sL https://raw.githubusercontent.com/alphaofertasdv-creator/alpha-ofertas-media/main/automation/meta_publish.py | python3 - --test` (device_bash). Se imprimir `OK Instagram @...` → usar ESTE modo e NÃO agendar no Metricool. Se der erro/sem meta.env → avisar no AVISO CLAUDE "API Meta não configurada" e usar o Metricool (que provavelmente está sem cota).
**Como funciona:** a API não agenda; publica na hora. Então a rotina da manhã só monta a FILA e quem publica são as vigias.
1. Gerar imagens como na seção 4 (conferir visualmente). Converter p/ JPEG (a Meta só aceita JPEG): `cd automation && python3 to_jpg.py AAAA-MM-DD` e commitar/dar push dos `.jpg` em `AAAA-MM-DD/` e `AAAA-MM-DD/stories/`.
2. Criar `automation/fila-ig-AAAA-MM-DD.json` e dar push (formato abaixo). Legenda do carrossel = a mesma da seção 4. Stories sem legenda. Horários fixos: carrossel 19:00 (facebook:true) e Stories 09:00, 11:30, 14:00, 16:30, 20:30 (se a fila for criada depois de um horário, só inclua os que ainda não passaram).
```
{"posts":[
 {"id":"st-0900","tipo":"story","quando":"AAAA-MM-DDT09:00:00-03:00","imagens":["AAAA-MM-DD/stories/story_1_<chave>.jpg"]},
 {"id":"car-1900","tipo":"carrossel","quando":"AAAA-MM-DDT19:00:00-03:00","facebook":true,
  "imagens":["AAAA-MM-DD/carrossel_1.jpg","AAAA-MM-DD/carrossel_2.jpg","AAAA-MM-DD/carrossel_3.jpg","AAAA-MM-DD/carrossel_4.jpg"],"legenda":"..."}]}
```
3. **Publicação (Vigia A/B, a cada execução, ANTES de checar o WhatsApp):** `curl -sL <raw>/automation/meta_publish.py | python3 - --due` na PC. Publica o que vence em até 10 min (as vigias rodam em :28 e :58, ~2 min antes de :30/:00). Imprime OK/ERRO/PULADO por item; cada item tem até 3 tentativas. Se ERRO → alerta no AVISO CLAUDE com a mensagem. A vigia B precisa rodar até 20:28 (Story das 20:30).
4. Conferir a fila e o que foi publicado: `... | python3 - --status`. No resumo da manhã e da noite listar só o que o `--status` mostra (não de memória).
5. Credenciais ficam só na PC em `C:\whatsapp_scheduler\data\meta.env` (IG_USER_ID, PAGE_ID, PAGE_TOKEN). NUNCA ler, imprimir, copiar ou commitar esse arquivo. O Claude não digita senhas nem tokens.
