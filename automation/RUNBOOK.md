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
1. 04:00 Preparo: pré-checagem, escolha das ofertas, links um a um, atualizar historico.json (commit/push).
2. 05:00 WhatsApp: agendar lotes na Importar Lote (1/grupo/hora).
3. 06:30 IG/FB: carrossel 19:00 + 5 Stories (09:00, 11:30, 14:00, 16:30, 20:30) via Metricool.
4. 07:30 Verificação (Já Agendadas, Metricool) + resumo final.
Alertas a cada ~30 min com %. Gatilho diário só é religado com aprovação do usuário.

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
