# Continuar o desenvolvimento dos apps (passagem para outro agente)

> **Atualização de 08/11/2026:** registro completo em [`ENTREGA-08-11-2026.md`](ENTREGA-08-11-2026.md).
> O **Agiliza+** gera o laudo no modelo timbrado da POLITEC e em PDF (Sprint 16); o **Passivo** tem timbre
> provisório (Sprint 10); o **Mapa** recuperou situação, custeio/investimento e mapa SESP (Sprint 11); o
> **TEIA** tem a ficha do Nelson e a classificação de 1 a 4 (Sprint 5). Próximos sprints de código, nesta
> ordem: Necropsia 11, Comissão 9, Agiliza 17 e Passivo 9. Rode `baixar_feedback.py` só app por app: sem
> filtro, ele apaga a seção escrita à mão no `FEEDBACK.md` do RNC.
>
> **Plano de execução agêntica:** [`PLANO-IMPLEMENTACAO-AGENTICA.md`](PLANO-IMPLEMENTACAO-AGENTICA.md) — ondas, cartões por app, testes, prompts e o que depende de humano.
>
> **Atualização de 03/11/2026 (rodada de implementação):** foram fechados os
> itens de código do feedback de **TEIA** (vítima/investigado/réu preso,
> protocolo, 36 regionais e reiteração), **Controle de Aquisições** (painel
> compacto), **Adiantamento** (afastamento, urgência e recurso de 24 h),
> **Gestão de Documentos** (anexo opcional, data de entrada e cobrança),
> **Segunda via da CIN** (fotos das impressões digitais e confronto), **RNC**
> (relação para impressão, responsáveis e Minhas RNCs), **Agiliza** (outras informações,
> foto/cor, ajuda dos arquivos e histórico com Abrir), **Custódia** (endereço
> hierárquico, confirmação física e painel de ocupação) e **Passivo** (cabeçalho,
> 3 mapas, abas e .docx). A regressão global
> passou: `testar.py` 21/21 e todos os cenários (126 no total). O
> diagnóstico e a lista do que falta estão em
> [`ANALISE-GLOBAL-PENDENCIAS.md`](ANALISE-GLOBAL-PENDENCIAS.md).
>
> **Atualização de 03/11/2026 (segunda etapa):** o curso tem **21 apps ativos**
> e o `distribuicao-casos-dna` foi **arquivado** em `Apps/_arquivados/`. O TEIA
> é o projeto do **Nelson e da Helen Coelho Gonçalves**. Entregas desta etapa: Sprint 8 da
> `trilha-custodia-necropsia` (sete etapas, assinatura, sepultamento e
> recebimento), importador `.xlsx` e Google Planilhas da
> `rnc-nao-conformidade`, carga da pasta e gestão dos laudos no `agiliza-mais`,
> dashboard orçamentário no `tap-portfolio-projetos` e o layout novo do TEIA
> no PC e no celular. Os testes por app estão no fim deste arquivo.
>
> **Atualização de 03/11/2026:** o TEIA é a nova etapa do projeto do Nelson e
> Luciana, com MVP, testes, hub e repositório próprios. O estado anterior, os
> testes (21/21 e 92/92) e o prompt de continuação estão em
> `Apps/CONTINUAR-IDENTIDADE.md`. Este arquivo é o histórico por app.

> **Atualização de 02/11/2026:** cada app passou a ser autônomo (`nucleo/`, `construir.py` e `testes/` próprios, sem base comum) e vai ganhar identidade própria. O que foi feito, o que falta e o prompt de continuação estão em `Apps/CONTINUAR-IDENTIDADE.md`. O diagnóstico e o plano de cada app estão em `Apps/PLANO-USABILIDADE.md`.


Atualizado em **03/11/2026, fim do dia** (histórico; ver `CONTINUAR-IDENTIDADE.md` para o estado atual).

**Estado geral: a maior parte dos 21 apps ativos com o MVP completo** (Sprints 1 a 6 ou 7, com
roteiro de aceite em `modelos/`). **Em 03/11/2026, fim do dia, os 21 apps estão minimamente funcionais de ponta a ponta**; o que sobra depende de pessoas (Sprint 0, aceite, piloto), de serviço externo (Apps Script do agendamento) ou é refinamento. Em 03/11/2026 os quatro apps maiores avançaram
(commits `fb0005b`, `0b67e02`, `ca57d14` e `0556119`). Situação ao fim do dia:

| App | Feito | Falta |
|---|---|---|
| `mapa-distribuicao-credor` | S1 a S7 | Testes contra o gabarito (S4, S5, S6, que depende do `mapa-manual-referencia.xlsx` do Sprint 0) e S8 (aceite, GitHub Pages, piloto, LEIA-ME) |
| `inscricoes-cursos` | S1 a S8 | Teste no Outlook e no celular (S3), acessibilidade do formulário (S8) e S9 (publicação, aceite, piloto) |
| `equipamentos-google-earth` | S1 a S10, com a tela do município, conflitos campo a campo e foto no balão do `.kmz` | Teste manual no Google Earth e S11 (aceite e piloto) |
| `agiliza-mais` | S1 a S11 (`src/sprint4.js`), com a requisição em PDF lida pelo pdf.js e o caso de exemplo embutido | OCR simulado (registrar no `PROJETO.md`), S12 (aceite e piloto) e S13 (opcional) |

O que depende de serviço externo (Apps Script, `LockService`, `MailApp`, gatilho,
banco, biblioteca de QR) está marcado como **a implementar** no `sprint.md`, com o
passo a passo dentro do app: **três cliques no nome do app, no rodapé**.

Este arquivo registra o que já foi feito nos 20 apps anteriores (o TEIA está em `CONTINUAR-IDENTIDADE.md`)
de `Apps/` e o que falta em cada um, para que outro agente de IA continue de onde
paramos. Leia também `AGENTS.md` (seção 3.8), `Apps/README.md` e
`Apps/IDENTIDADE-VISUAL.md`.

## 0. Próximo ciclo: o feedback dos alunos

Cada app tem um formulário de feedback (`Aula 8/feedback/<app>.html`), que grava na coleção `feedback_apps` do Firestore. Para continuar um app:

1. `python Apps/_base/baixar_feedback.py <app>` escreve o `Apps/<app>/FEEDBACK.md` (prioridades, telas com erro ou ajuste, o que falta, regras que não batem).
2. Abra um sprint novo no `sprint.md` do app com os itens do `FEEDBACK.md`, na ordem das prioridades.
3. Siga a sequência de sempre: fontes em `src/`, `python construir.py`, `testes/testar.py`, `testes/cenarios.py` e um cenário novo para cada item.

As respostas podem ser lidas na página `Aula 8/feedback/index.html`. Os formulários são regerados por `python "Aula 8/gerar_feedback.py"` quando as telas de um app mudam.

**Acessibilidade (03/11/2026):** Lighthouse de acessibilidade com 100 nos 21 apps e no formulário de feedback, depois de escurecer o âmbar do tema claro (`--ambar:#8a5000` no `nucleo/visual.css` de todos) e tirar a opacidade das etapas vazias da Comissão de Ética e dos meses vazios do Metas BI.

### 0.0a RNC: ID da planilha e setores (04/11/2026)

Pedido da Sabrina pelo WhatsApp: o app criava um código em vez de usar o da planilha. Commit `0588c5f`, detalhe no Sprint 8 de `rnc-nao-conformidade/sprint.md`.

- O "ID ocorrência" passou a ser a fonte de verdade. Antes, os fictícios (`DLF/2026-001` a `020`) ocupavam os números reais e a linha da planilha era descartada como "já existente". Agora o fictício é substituído, e a RNC importada antes com código gerado é renumerada.
- Os setores são padronizados pelo catálogo `SETORES_POLITEC` (11 unidades; siglas assumidas em `PREMISSAS.md`, seção 18). Texto sem unidade fica como `ADEF`, e o nome de pessoa sai da coluna de envolvidos (RN07).
- Testes do RNC: `#/testes` 18/18, cenários 11/11 (`s11` e `s12` novos), e o app passa em `_base/testar.py` e `_base/testar_sprints.py`.
- Pendente: confirmar as siglas com a Sabrina e enviar a versão para o repositório dela, se ela continuar por lá.

### 0.0 Mudanças da segunda etapa de 03/11/2026

- **trilha-custodia-necropsia**: Sprint 8 com sete etapas, resultado da identificação, busca de familiares, liberação com assinatura no canvas, sepultamento pelo Estado, entrega e recebimento do laudo, confirmação de lacre só pelo Gestor ADM, perfil Médico Legista e `#/resumo`. A versão 02/11/2026 da Silmara está em `entregas/2026-11-02/`.
- **rnc-nao-conformidade**: leitor de `.xlsx` com PizZip (sem nova dependência), 23 colunas oficiais traduzidas (nome e e-mail descartados pela RN07), ficha com os metadados e sincronização com o Google Planilhas por CSV público. A CSP libera só `docs.google.com`; a planilha precisa ser pública.
- **agiliza-mais**: **Carregar a pasta do caso** no `#/inicio` e ações de continuar, renomear, mover para pasta e excluir nos laudos em preenchimento. O `CASO TESTE 2/README.md` descreve os arquivos e o `.dotx` institucional (ainda sem marcadores).
- **tap-portfolio-projetos**: loja `orcamentos` e `#/dashboard` por ano e eixo (empenhado, liquidado, saldo, percentual), com edição, exclusão, exportação CSV e importação `.xlsx`/`.csv`. O seed tem 15 lançamentos fictícios.
- **metas-bi-ocr**: mês de referência escolhido no importador; editar, renomear e excluir cada linha da conferência; excluir um mês importado (mês aprovado não é excluído).
- **teia-triagem-emails**: layout refeito para PC e celular (fila com encaixe, barra de ações, KPI clicável, menu compacto, rolagem no topo ao trocar de tela).
- **controle-aquisicoes** e **equipamentos-google-earth**: gráficos limitados a 640 px e 720 px para não crescerem com a largura do cartão.
- **distribuicao-casos-dna**: arquivado em `Apps/_arquivados/`; saiu do painel, do hub, dos formulários e dos testes.

### 0.0.1 Feedback recebido em 03/11/2026 (18 respostas em 16 apps)

**Sprints abertos** com os itens do feedback, na ordem das prioridades: adiantamento 8, agiliza-mais 14, cin-segunda-via 7, comissao-etica 8, controle-aquisicoes 8, custodia-definitiva 8, equipamentos-google-earth 12, gestao-documentos 8, inscricoes-cursos 10, metas-bi-ocr 8, rnc-nao-conformidade 7, teia-triagem-emails 4, mapa-distribuicao-credor 9, renovacao-contratos-horus 8, passivo-ambiental 8, tap-portfolio-projetos 8 e agendamento-cin 9 (aguardando resposta). O que depende de decisão do setor está em `Apps/PREMISSAS.md`, seção "Feedback de 03/11/2026".

`python Apps/_base/baixar_feedback.py` escreveu os `FEEDBACK.md` de adiantamento
(2), agiliza-mais, cin-segunda-via, comissao-etica-denuncias,
controle-aquisicoes, custodia-definitiva, equipamentos-google-earth,
gestao-documentos, inscricoes-cursos, metas-bi-ocr, rnc-nao-conformidade (2),
teia-triagem-emails, mapa-distribuicao-credor, renovacao-contratos-horus,
passivo-ambiental e tap-portfolio-projetos. O `agendamento-cin` ainda não tem
resposta; os demais apps também não receberam resposta.

Fechados nesta etapa: mês escolhido e edição no Metas; importador `.xlsx` e
Google Planilhas no RNC; carga da pasta e gestão dos laudos no Agiliza;
dashboard orçamentário no TAP; layout do TEIA; tamanho dos gráficos do Controle
e do Mapa de Equipamentos. Na primeira execução dos sprints, também ficaram
prontos no Agiliza a revisão simplificada, os textos editáveis por caso, a
biblioteca com tipo de dispositivo, os quesitos opcionais e o carregamento de
`.docx`/`.dotx`; e no RNC as categorias oficiais, o complemento em 5 dias úteis
e o documento para impressão/PDF; no Mapa, a situação do processo, os dígitos da
dotação, a tabela grupos/empresas e o alinhamento do mapa.

Backlog do próximo ciclo (o que não foi feito):

- **adiantamento**: bloquear o pedido quando o servidor estiver de férias ou licença-prêmio.
- **agiliza-mais**: modelo Word timbrado da POLITEC já formatado; revisão só com "revisei" e "concluir"; tipo de dispositivo e IA de texto na biblioteca; cor do aparelho editável; textos editáveis; quesitos opcionais; revisar o histórico.
- **cin-segunda-via**: envio de fotos das impressões digitais; troca de perfil mais rápida.
- **comissao-etica-denuncias**: texto do artigo na sugestão e confirmação padrão; lista de membros na admissibilidade e fundamento padrão; apagar oitiva e encerrar oitivas; ajustes nas minutas; envio por e-mail.
- **custodia-definitiva**: endereçamento hierárquico (contêiner, estante, prateleira, nível e posição) com confirmação física; painel por contêiner e saturação.
- **gestao-documentos**: anexo opcional, data de entrada na lista e cobrança perto do vencimento.
- **inscricoes-cursos**: perfis por diretoria/coordenação/gerência e termo de convocação de instrutores e monitores.
- **metas-bi-ocr**: filtro por gerência; conferir o fluxo de aprovar e gerar a planilha com dados reais; extrair o cartão Pendentes.
- **rnc-nao-conformidade**: gerar a RNC no modelo oficial, nomenclatura das categorias (ADM, AMB, PES, REA, EQP, MPA), documentos por setor e login.
- **teia-triagem-emails**: retirar nível e número da cobrança; incluir vítima, investigado, réu preso; alerta de reiteração; lista de regionais.
- **controle-aquisicoes**: reduzir a fonte do painel.
- **equipamentos-google-earth**: testar no Google Earth (depende de pessoa).
- **mapa-distribuicao-credor**: importar o PDF do pregoeiro, novo mapa orçamentário no modelo da SESP, dígitos da dotação, situação do processo, empresa ganhadora do grupo e alinhamento do mapa.
- **renovacao-contratos-horus**: fiscais e gestores por contrato, aviso por e-mail no laranja/vermelho com confirmação de leitura, edição do contrato, objeto na instrução e importação da planilha do setor.
- **passivo-ambiental**: corrigir o editor de mapas, três mapas obrigatórios, abas de metodologia/considerações/valoração/quesitos, exportação .docx e cabeçalho.
- **tap-portfolio-projetos**: objetivos estratégicos reais, fluxo de pendência → análise → autoridade, avisos por e-mail e prazo de 5 dias.

### 0.0.2 Novo app · Gestão de Identificados (`gestao_identificados`)

Projeto da **Kesia Melo** (NIHDE), criado em 03/11/2026 a partir do envio e de
cinco áudios. O app tem painel com a pergunta do MVP, lista, cadastro, ficha com
os quatro exames, identificação, família, sepultamento pelo município,
identificação após sepultamento, relatório e CSV. MVP nos Sprints 0 a 4;
`python testes/testar.py` e os quatro cenários passam. O módulo de desaparecidos
está em `desaparecidos.html` (painel do CNPD/MJ com 381 registros) e na rota
`#/desaparecidos`, ligado pelo painel do app e pelo hub; a base pública fica
separada do cadastro dos corpos e o contrato está em
`docs/CONTRATO-DESAPARECIDOS.md`. O repositório
[gestao_identificados](https://github.com/renato0503/gestao_identificados) foi
criado e publicado; a Kesia (`krllmsoares-del`) recebeu convite de escrita e
precisa aceitar. Pendente: confirmar o nome oficial do NIHDE e o escopo dos dados
físicos, integrar com o Atena e o piloto de 90 dias no IML de Cuiabá.

## 0.1 Links para os alunos

`Apps/LINKS-ALUNOS.md` (gerado por `python Apps/_base/gerar_links_alunos.py`) traz, por app, a equipe, o link do app, o hub (`processo.html`), o formulário de feedback e o repositório. Os links apontam para o GitHub Pages do repositório `Aula_politec` (os repositórios separados não têm Pages). As mudanças só aparecem no site depois do `git push origin main`.

## 1. Como o projeto funciona (o mínimo para começar)

- Cada app é **um único `index.html` gerado**, offline, com IndexedDB, backup
  `.json`, perfis, dados fictícios e a tela `#/testes`.
- **Nunca edite o `index.html`.** As fontes são:
  - comuns: `Apps/_base/base.html`, `visual.css`, `icones.js`, `js_comum.js`;
  - por app: `app.json` (título, `visual`, banco, perfis, rotas), `src/app.js`
    (Sprints 1 e 2), `src/sprint3.js`, `src/sprint4.js`... (um arquivo por sprint,
    juntados em ordem depois do `app.js`), `src/app.css` (opcional),
    `exemplos/seed.json` (gerado por `exemplos/gerar_exemplos.py`).
- Uma tela é `TELAS["#/rota"] = async params => "html"` e os eventos ficam em
  `TELAS_DEPOIS["#/rota"] = params => {...}`. Um sprint novo pode **redefinir**
  uma tela antiga no seu arquivo (ex.: `custodia-definitiva/src/sprint3.js`) ou
  **embrulhar** a tela anterior guardando a função original (ex.:
  `trilha-custodia-necropsia/src/sprint3.js`).
- Regras de negócio viram funções puras com `teste("nome", ()=>...)`; elas rodam
  em `#/testes` e no `testar.py`.
- Cada sprint tem um **cenário de interface** em
  `Apps/_base/cenarios/sprintN.py` (`@cenario("<app>")`), que usa a tela como uma
  pessoa e confere o "Pronto quando" do `sprint.md`.
- Store novo no banco: acrescente em `app.json → db.stores` **e suba
  `db.versao`** (senão o IndexedDB não cria o store).
- Ao concluir um sprint: marque `[x]` nos itens do `sprint.md`, acrescente a
  linha na tabela **Andamento**, atualize `sprint` e `descricao` das rotas no
  `app.json` e a tabela de andamento do `Apps/README.md`.

### Comandos

```powershell
python Apps/_base/construir.py [<app>]          # gera o index.html (todos ou um)
python Apps/_base/testar.py [<app>]             # estrutura: zero rede, #/testes 100%, rotas, tema
python Apps/_base/testar_sprints.py [<app>]     # cenários de cada sprint
python Apps/_base/painel.py; python Apps/_base/hub_apps.py   # painel e hub
node Apps/agendamento-cin/testes/testar_code_gs.js            # só o agendamento
```

No Git Bash, rotas como `#/corpo/C-0001` passadas como argumento viram caminho de
arquivo; use `MSYS_NO_PATHCONV=1` ou rode pelo PowerShell.

## 2. O que foi feito nesta etapa (30/10/2026)

### 2.1 Identidade visual SESP/MT e POLITEC/MT (os 20 apps anteriores)

- Nova base visual em `Apps/_base/visual.css` (separada do `base.html`): faixa do
  Governo de Mato Grosso, SESP e POLITEC; cabeçalho com degradê azul
  institucional, textura e filete acento/dourado/verde; emblema do app; menu com
  ícones; cartões, KPIs, tabelas, selos, formulários, rodapé institucional e
  cabeçalho de impressão.
- `Apps/_base/icones.js` com 48 ícones e a escolha automática do ícone de cada
  tela.
- Bloco `visual` em cada `app.json` (acento, emblema, layout `lateral`/`topo`,
  padrão do cabeçalho, estilo `institucional`/`claro`, setor). Detalhes e tabela
  dos 20 apps em `Apps/IDENTIDADE-VISUAL.md`.
- **Tema claro como padrão** em todos os apps; o escuro só entra pelo botão Tema.
- **Tamanho da fonte**: A−, 100% e A+ no cabeçalho (80% a 150%), guardado por app.
- **Faixa de aviso removida** de todos os apps (chave `aviso` tirada dos `app.json`).
- Componentes novos reutilizáveis: `.busca-grande`, `.duas-colunas`,
  `.linha-do-tempo`, `.etapas`, `.barra`, `.chips`, `.check-lista`,
  `.documento-a4`.

### 2.2 Sprint 3 em dois apps novos

- **custodia-definitiva**: acervo com busca por lacre, protocolo, categoria e
  contêiner (todas as palavras), filtros combinados (categoria, contêiner,
  situação, onde está, período), exportação CSV do filtro; ficha com
  movimentação (transferência com RN02/RN03, saída para perícia, retorno), linha
  do tempo e CSV do histórico. Cenário `s3_busca_csv_e_historico` (8/8).
- **trilha-custodia-necropsia**: transições de situação com regras e motivo,
  identificação com método, histórico da situação, painel e lista só com
  iniciais (RN05), filtros rápidos e dias no IML, busca por protocolo, nome,
  documento ou lacre (RN04). Cenário `s3_situacao_identificacao_e_busca` (11/11).

### 2.3 Verificação

`python Apps/_base/testar.py` passa nos 20 apps anteriores e `python Apps/_base/testar_sprints.py`
passa nos cenários de todos os sprints (ver o resultado no fim da seção 4).

## 3. Pendências gerais

1. **Sprint 3 dos 6 apps novos**: concluído em 30/10/2026. `passivo-ambiental`,
   `renovacao-contratos-horus`, `documentapolitec`, `gestao-documentos`,
   `controle-aquisicoes` e `distribuicao-casos-dna` têm o Sprint 3 feito.
2. **Manual de marca oficial**: as cores institucionais foram definidas por
   aproximação. Pedir o manual à ASCOM da SESP/POLITEC e trocar `--mt-*` em
   `visual.css`. Se houver brasão ou logotipo autorizado, entra no `.emblema` ou na
   `.faixa-gov` (hoje há só os quadrados da bandeira e o ícone do app).
3. **Dado fictício do TCIN**: corrigido em 30/10/2026. A lista `CASOS` de
   `trilha-custodia-necropsia/exemplos/gerar_exemplos.py` agora traz situação e
   nome juntos, e corpo "aguardando identificação" ou "não identificado" nasce
   sem nome e sem documento. O seed foi regerado e o `index.html` reconstruído;
   os testes do app e do Sprint 3 passam.
4. **KPI com texto longo** (ex.: nome da categoria na ficha do vestígio) fica com
   fonte grande; se incomodar, use um valor curto ou uma classe menor.
5. Telas antigas que ainda usam `<ol class="linha-tempo">` (adiantamento) podem
   migrar para `.linha-do-tempo`.
6. **Sprint 0**: os 77 itens que dependiam de decisão institucional, documento
   oficial ou medição do processo real foram **elucubrados** em 30/10/2026 e
   estão em [PREMISSAS.md](PREMISSAS.md), com o valor assumido, onde ele aparece
   no app e o que precisa ser confirmado. Nenhum item bloqueia o
   desenvolvimento. As referências que faltavam (modelos de DFD, ETP, TR, TAP,
   ata, laudo, caixa, marcos, plano de trabalho, esquema do Hórus) foram criadas
   nas pastas `modelos/` e `horus/` dos apps. **O que ainda depende de pessoas
   está na coluna "O que confirmar" de cada premissa**.
7. Publicação: esta etapa foi enviada ao GitHub em 30/10/2026 (identidade
   visual dos 20 apps, Sprint 3 da custódia definitiva e da TCIN, kit visual e
   este registro). Os arquivos da Aula 4 que já estavam modificados ficaram de
   fora do commit.

## 4. Estado e próximo passo de cada app

### Controle de Adiantamentos (`adiantamento`)

- **Visual**: acento `#0b6e4f`, emblema `moeda`, layout `lateral`, padrão `linhas`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6, 7.
- **Situação**: MVP completo até o Sprint 7. O roteiro de aceite está em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Validar as 12 etapas da tabela AS-IS com a DAS e com a contabilidade da SESP.
  - [ ] Confirmar qual Orientação Técnica da CGE/MT vale (02/2026 ou 06/2025).
  - [ ] Anexar os documentos citados (AS-IS e TO-BE em .docx, planilha de controle).
  - [ ] Acrescentar os feriados de MT e do município (Cuiabá) à lista.
  - [ ] Linha de base: anotar as datas dos pedidos de 4 semanas (proposta dos alunos).

### Agendamento CIN (`agendamento-cin`)

- **Visual**: acento `#1559b7`, emblema `calendario`, layout `topo`, padrão `ondas`, cabeçalho `claro`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6, 7, 8.
- **Situação**: MVP completo até o Sprint 8. Roteiro de aceite em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Pedir à TI a autorização para publicar um app da web do Apps Script com a conta institucional e confirmar as cotas de execução e de e-mail.
  - [ ] Aprovar com a gestão as regras completadas: RN06 (um agendamento ativo por posto), RN07 (cancelar até 2 h antes), RN08 (tolerância de 15 min), RN09 (de 1 a 30 dias de antecedência), RN10 (retenção de 90 dias).
  - [ ] Escolher os 1 ou 2 postos do piloto e levantar a grade real (dias, horários, vagas por horário).
  - [ ] Medir a linha de base no posto do piloto: tempo de uma marcação por telefone e agendamentos por dia.
  - [ ] Confirmar o nome completo do aluno no formulário.

### Agiliza + (`agiliza-mais`)

- **Visual**: acento `#4338ca`, emblema `raio`, layout `lateral`, padrão `grade`, cabeçalho `institucional`.
- **Sprints concluídos**: 1 a 3; 4 a 11 em versão mínima em 03/11/2026 (`src/sprint4.js`). O fluxo completo funciona: pasta, extração, conferência com correção registrada (RN04), textos (RN08), quesitos (RN09, RN10), conferência automática (RN11), `.docx` gerado pelo modelo embutido (RN12), revisão que conclui o caso (RN14), histórico com CSV e limpeza do caso (LGPD). Cenário `s4_a_s11_laudo_completo` passa (10/10).
- **Falta**: ler a requisição em PDF com o pdf.js (já em `vendor/`, mas não embutido) e o OCR, que hoje são digitação na conferência; o caso de exemplo sem pasta não tem dados para extrair; os itens finos de cada sprint no `sprint.md`; S12 (aceite e piloto) e S13 (opcional).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Conferir com o perito o formato real dos TXT e HTML (amostra anonimizada) e anotar os rótulos exatos em `exemplos/FORMATOS.md`.
  - [ ] Copiar o modelo institucional para `modelos/modelo-laudo-celular.docx` e inserir os marcadores (`{numero_protocolo}`, `{imei_1}`, `{#sims}`...). Lista dos marcadores em `modelos/MARCADORES.md`.
  - [ ] Reunir os textos padronizados da Gerência em `exemplos/textos.json` (categoria, título, conteúdo), sem dados pessoais.
  - [ ] Criar a planilha da linha de base (protocolo, início, fim, correções) e começar a medir os laudos manuais: **2 semanas**, que correm em paralelo aos Sprints 1 e 2.

### Segunda via da CIN (`cin-segunda-via`)

- **Visual**: acento `#0e7490`, emblema `identidade`, layout `topo`, padrão `ondas`, cabeçalho `claro`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6.
- **Situação**: MVP completo até o Sprint 6. O roteiro de aceite está em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Confirmar as regras oficiais da segunda via (quando dispensa nova coleta).
  - [ ] Indicar a fonte dos números (15 dias, 21.000 por mês).
  - [ ] Fotos de teste geradas (sem pessoas reais).
  - [ ] Conversa com a TI e com a empresa da coleta biométrica sobre a integração (registrar a posição).

### Comissão de Ética (`comissao-etica-denuncias`)

- **Visual**: acento `#8a1c3a`, emblema `balanca`, layout `lateral`, padrão `pontos`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6, 7.
- **Situação**: MVP completo até o Sprint 7. O roteiro de aceite está em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Conferir com a Comissão as categorias e as palavras. **Os artigos da LC nº 112/2002-MT já estão na norma real**, com o texto em `modelos/codigo-etica-lc112-2002.md`.
  - [ ] Receber os modelos de ata de reunião, ata de oitiva e relatório de recomendações.
  - [ ] Linha de base: tempo das reuniões de triagem e da preparação das oitivas nos últimos casos.

### Controle do Processo de Aquisição (`controle-aquisicoes`)

- **Visual**: acento `#b23c17`, emblema `carrinho`, layout `lateral`, padrão `grade`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6, 7.
- **Situação**: MVP completo até o Sprint 7. Roteiro de aceite em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Receber os modelos oficiais de DFD, ETP, TR e análise de riscos (a estrutura já segue a Lei nº 14.133/2021 em `modelos/MODELOS.md`).
  - [ ] Confirmar os prazos de cada etapa. **As 9 etapas e os documentos já estão ancorados na Lei nº 14.133/2021**, com 43 dias de ciclo em `modelos/fluxo-e-prazos.md`.
  - [ ] Validar as permissões e a base de processos de 2024/2025.

### Custódia Definitiva (`custodia-definitiva`)

- **Visual**: acento `#3f4a5a`, emblema `caixa`, layout `lateral`, padrão `hexagonos`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6, 7.
- **Situação**: MVP completo até o Sprint 7. Roteiro de aceite em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Conferir categorias, condições de conservação e capacidades com a equipe da custódia.
  - [ ] Receber a medição real de volume, tempo de recebimento e tempo de localização.

### Distribuição de Casos de DNA (`distribuicao-casos-dna`) · ARQUIVADO

> Em 03/11/2026 o app foi movido para `Apps/_arquivados/distribuicao-casos-dna/` e saiu do painel, do hub, dos formulários de feedback e dos testes. O registro abaixo é histórico.

- **Visual**: acento `#86198f`, emblema `dna`, layout `topo`, padrão `hexagonos`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6, 7.
- **Situação**: MVP completo até o Sprint 7. Roteiro de aceite em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Confirmar a rotação e o número de peritos ativos com a coordenação.
  - [ ] Medir a linha de base do intervalo entre processamento e distribuição.
  - [ ] Validar o número de casos por rodada e as naturezas de exame.

### DOCUMENTAPOLITEC (`documentapolitec`)

- **Visual**: acento `#7c5a16`, emblema `pasta`, layout `lateral`, padrão `linhas`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6, 7.
- **Situação**: MVP completo até o Sprint 7. Roteiro de aceite em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Confirmar o formato do número do prontuário e o modelo das caixas.
  - [ ] Receber a planilha de teste com a relação de 850 prontuários.
  - [ ] Receber uma amostra do PDF digitalizado, sem dado pessoal.

### Mapa de Equipamentos (`equipamentos-google-earth`)

- **Visual**: acento `#2f7d32`, emblema `globo`, layout `topo`, padrão `topografico`, cabeçalho `institucional`.
- **Sprints concluídos**: 1 a 9 (S4 a S9 em 03/11/2026, commit `ca57d14`). Detalhe por sprint em `equipamentos-google-earth/sprint.md`.
- **Feito em 03/11/2026, commit `0556119`**:
  - Clicar no município no mapa abre `#/municipio/<código IBGE>`, com os distritos do município, as unidades do app ali, a busca de equipamento por distrito e o botão "Abrir no Google Maps".
  - Os distritos vêm do IBGE: `dados-base/mt-distritos.json` (258 distritos em 141 dos 142 municípios; Boa Esperança do Norte não tem registro). O arquivo é gerado por `dados-base/gerar_distritos.py`, que baixa `api/v1/localidades/distritos` uma vez e filtra MT. O app não chama a API em tempo de execução.
  - **Atenção: o IBGE publica distritos, não bairros.** Cuiabá tem 7 distritos (Cuiabá, Coxipó da Ponte, Guia...), e não os bairros da cidade. Bairro de verdade vem de lei municipal e não tem base estadual aberta. O app chama o campo de "Bairro (distrito)".
  - A ficha do equipamento ganhou o campo `bairro`, com sugestões dos distritos e entrada no CSV. O seed foi regerado com um distrito sorteado do município da unidade. A malha `mt-municipios.json` ficou igual.
  - O mapa ganhou zoom pelos botões, arrasto, filtros (sem contrato, parados, ponto único, diretoria, tipo), pinos coloridos por risco, painel lateral no pino e a tabela de municípios com a coluna de distritos.
  - `#/exportar` ganhou o GeoJSON (QGIS, ArcGIS, Google Earth Engine). A ficha do equipamento ganhou o link para o Google Maps.
  - Testes: `python testes/testar.py` passa, e o cenário `s6_mapa_e_municipio` passa em `testes/cenarios.py`.
- **Pergunta em aberto: Google Maps ou Google Earth "de verdade"**. O usuário perguntou se algum projeto de `github.com/topics/google-earth-engine` resolveria. Resposta: o Google Earth Engine analisa imagem de satélite, e não é mapa de cadastro, por isso não serve de base do app. Hoje o app chega ao mapa real por três caminhos sem chave de API: o `.kmz` (Google Earth Pro e Web), o GeoJSON (QGIS, ArcGIS, GEE, geojson.io) e o link para o Google Maps. **Para decidir amanhã**: colocar um mapa de fundo real (ruas e satélite) dentro do app. A opção indicada é Leaflet em `vendor/` com tiles do OpenStreetMap, mas isso exige internet e quebra a regra "offline first, zero requisição de rede" que o `testar.py` cobra. Por isso, se for feito, fica como camada opcional, ligada só com internet. A alternativa é a Google Maps JavaScript API, que pede chave e cobrança.
- **Feito no fim do dia (`src/sprint6.js`)**: parâmetros de custo editáveis com data da alteração, unidade dona da cópia, `.json` com ou sem fotos, gráficos de barras e de linha em SVG no painel, fórmula no hover dos KPIs, KPI que abre o mapa filtrado, aviso de CPF antes de salvar (RN09) e texto de privacidade. Cenário `s10_config_e_graficos` passa (7/7).
- **Falta**: tela de conflitos campo a campo na mesclagem (hoje a escolha é por unidade inteira), foto no balão do KML, conferência no Lighthouse, teste manual no Google Earth Pro e Web, e o Sprint 11 (aceite, LEIA-ME e piloto).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Ler o `contexto.md` com a coordenadora e marcar cada **[validar]** como aceito, alterado ou recusado.
  - [ ] Preencher de novo no formulário (importando o `projeto.json`) as seções MVP, papéis, entidades, regras, telas e KPIs, com o escopo validado.
  - [ ] **Retirar o número de 11 dígitos** do campo "dados pessoais tratados".
  - [ ] Levantar a lista de diretorias e unidades da POLITEC com município de cada uma.
  - [ ] Reunir a planilha que existe hoje ("parcialmente", segundo o formulário) e anotar as colunas.
  - [ ] Definir com a coordenadoria o `valor_referencia_atendimento` e o custo alternativo padrão (terceirização, deslocamento para outra unidade).
  - [ ] Escolher 3 unidades para o piloto e medir a linha de base: quantos equipamentos estão sem contrato, quantas paradas houve no último trimestre e quanto tempo levou para responder "quanto custa essa parada?".

### Gestão de Documentos (`gestao-documentos`)

- **Visual**: acento `#2b5a8a`, emblema `carimbo`, layout `lateral`, padrão `linhas`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6, 7.
- **Situação**: MVP completo até o Sprint 7. Roteiro de aceite em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Validar a matriz de papéis e quem pode excluir documentos.
  - [ ] Definir os anexos obrigatórios por tipo de processo (RN01).
  - [ ] Medir a linha de base (1 h/dia, 200 processos/mês, 48 h na triagem).

### Banco de Demandas (`horus-banco-demandas`)

- **Visual**: acento `#8f6b00`, emblema `olho`, layout `lateral`, padrão `pontos`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6, 7, 8.
- **Situação**: MVP completo até o Sprint 8. Roteiro de aceite em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Decidir com o aluno o papel da versão offline: (a) substituir o módulo, (b) servir às unidades sem acesso ao Hórus e entregar no formato dele, ou (c) ficar como exercício. Proposta: **(b)**.
  - [ ] Copiar do Hórus o esquema real das 3 tabelas (DDL do Supabase) para `horus/esquema.sql` e conferir com o `contexto.md`, seção 5.
  - [ ] Definir o formato `horus-import-ciclo.json` (versão do esquema, órgão, diretoria, ciclo, linhas das 3 tabelas) e o caminho de importação no Hórus (tela de importação ou SQL).
  - [ ] Decidir o relatório: `@media print` ou jsPDF embutido.
  - [ ] Juntar ao envio os anexos citados (relatório PDF e print da tela).

### Inscrições em Cursos (`inscricoes-cursos`)

- **Visual**: acento `#0369a1`, emblema `capelo`, layout `topo`, padrão `ondas`, cabeçalho `institucional`.
- **Sprints concluídos**: 1 a 8 (S4 a S8 em 03/11/2026, commit `0b67e02`). Detalhe em `inscricoes-cursos/sprint.md`.
- **Falta**:
  - S3: testar o formulário no Outlook desktop, no Outlook Web e no celular (manual).
  - S8: acessibilidade do formulário de inscrição (rótulos, teclado, contraste).
  - S9: publicar no GitHub Pages, roteiro de aceite com a gerência e uma diretoria, piloto com uma turma reduzida.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Ler o `contexto.md` com a aluna e decidir cada **[validar]**.
  - [ ] Decidir com a chefia: **o CPF sai do formulário**? (proposta: sim, a matrícula basta).
  - [ ] Confirmar com a TI se a caixa `capacitacao@politec.mt.gov.br` aceita uma regra de resposta automática por assunto `[INSCRICAO]`.
  - [ ] Listar as diretorias que recebem vagas (nome e sigla).
  - [ ] Medir a linha de base em 2 cursos recentes: tempo da divulgação à lista final, espera pelas diretorias, erros corrigidos na planilha, vagas ociosas.
  - [ ] Corrigir no formulário (importando o `projeto.json`) as métricas, a hospedagem e a defesa que vieram de outro projeto.

### Mapa de Distribuição (`mapa-distribuicao-credor`)

- **Visual**: acento `#047857`, emblema `tabela`, layout `lateral`, padrão `grade`, cabeçalho `institucional`.
- **Sprints concluídos**: 1 a 7 (S4 a S7 em 03/11/2026, commit `fb0005b`). Detalhe em `mapa-distribuicao-credor/sprint.md`.
- **Falta**:
  - S4: a regra de substituição do estimado pelo homologado (RN03) segue a premissa, porque a decisão "por item ou por desconto do grupo" é do Sprint 0. Falta o teste contra o gabarito.
  - S5: teste de que todas as divergências de `DIVERGENCIAS.md` são apontadas.
  - S6: teste contra o gabarito, com um caso de dotação insuficiente.
  - Os três testes dependem do `mapa-manual-referencia.xlsx` (Sprint 0, feito à mão pela equipe).
  - S8: teste de aceite do aluno, publicação no GitHub Pages, piloto com um processo encerrado, LEIA-ME e atualização do `PROJETO.md` e do `README.md`.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Anexar o `WorkFlow.docx` (exemplos 1 a 8) à pasta e conferir as colunas de cada exemplo com o `contexto.md`.
  - [ ] Decidir com a equipe e o orçamento os 4 pontos **[validar]** do `contexto.md`, seção 6 (homologado por grupo ou item, arredondamento, ordem da dotação, grupo misto), e escrever cada regra com um exemplo numérico.
  - [ ] Conseguir um relatório do pregoeiro de amostra (sem dado pessoal) e anotar o formato (colunas, cabeçalho, linhas de total).
  - [ ] Montar à mão, no Excel, o `mapa-manual-referencia.xlsx` (o gabarito).
  - [ ] Medir a linha de base em 3 a 6 processos encerrados: horas por etapa, divergências achadas e número de planilhas.

### Metas pelo BI (`metas-bi-ocr`)

- **Visual**: acento `#9d174d`, emblema `alvo`, layout `topo`, padrão `grade`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6.
- **Situação**: MVP completo até o Sprint 6. Roteiro de aceite em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Perguntar à TI se o Power BI 1 permite **Exportar dados** (CSV/Excel) no visual de pendências.
  - [ ] Conseguir uma amostra do PDF mensal com números fictícios (ou com os números tapados).
  - [ ] Copiar o cabeçalho da planilha do Google (colunas e uma linha de exemplo).
  - [ ] Listar as unidades e os nomes como aparecem no relatório.
  - [ ] Linha de base: cronometrar a atualização do mês atual.

### Passivo Ambiental (`passivo-ambiental`)

- **Visual**: acento `#4d7c0f`, emblema `folha`, layout `topo`, padrão `topografico`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6, 7.
- **Situação**: MVP completo até o Sprint 7. Roteiro de aceite em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Receber uma requisição real anonimizada e o modelo de laudo da unidade.
  - [ ] Confirmar o modelo de mapa (norte, escala, área) com o perito.
  - [ ] Cronometrar 5 laudos para confirmar a linha de base de 16 h.

### Renovação de Contratos · Hórus (`renovacao-contratos-horus`)

- **Visual**: acento `#3b4f7a`, emblema `contrato`, layout `lateral`, padrão `linhas`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6, 7.
- **Situação**: MVP completo até o Sprint 7. Roteiro de aceite em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Confirmar as seis faixas do semáforo e o alerta de 90 dias com a gestão.
  - [ ] Definir as permissões de escrita (autor, chefia, gestor).

### Não Conformidades (`rnc-nao-conformidade`)

- **Visual**: acento `#b42318`, emblema `alerta`, layout `lateral`, padrão `linhas`, cabeçalho `institucional`.
- **Sprints concluídos**: 1 a 8 (Sprint 7: feedback de 03/11; Sprint 8: ID da planilha e setores, 04/11/2026).
- **Situação**: MVP completo até o Sprint 8. Importa a planilha oficial com o ID dela, padroniza os setores e não guarda nome de pessoa. Roteiro de aceite em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Próximo passo**: confirmar com a Sabrina as siglas dos setores (`SETORES_POLITEC` em `src/app.js`) e conferir o documento com o modelo oficial da CQUAL.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Listar com a CQUAL as categorias de não conformidade e as gravidades.
  - [ ] Copiar o cabeçalho da planilha de respostas do Forms (sem dados) e anotar cada coluna.
  - [ ] Linha de base: tempo de cada etapa e cobranças da CQUAL nas RNCs do primeiro mês.

### TAP Digital (`tap-portfolio-projetos`)

- **Visual**: acento `#5b21b6`, emblema `portfolio`, layout `topo`, padrão `pontos`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6.
- **Situação**: MVP completo até o Sprint 6. Roteiro de aceite em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Receber o modelo vigente do TAP e a lista oficial de documentos.
  - [ ] Validar com a área responsável os campos obrigatórios e os tamanhos mínimos (RN01, RN02).
  - [ ] Linha de base: 4 semanas de registro (recebimento, documentação completa, devoluções e motivos).

### TCIN · Trilha de Custódia e Identificação (`trilha-custodia-necropsia`)

- **Visual**: acento `#1e3a5f` (navy do protótipo DMML), emblema `etiqueta`, layout `lateral`, padrão `pontos`, cabeçalho `institucional`.
- **Sprints concluídos**: 1 a 10.
- **Situação**: MVP completo. Desde o Sprint 10 (05/11/2026) o app é o **espelho do protótipo** da aluna ("Sistema de Controle de Necropsia — DMML _ POLITEC.html", em `entregas/2026-11-05/`): faixa de cabeçalho navy, painel de dez indicadores, lista de corpos com filtros e gaveta lateral, resumo por agente causal e ficha do caso com as sete etapas, assinatura no canvas e janela de justificativa. Os dados fictícios são os dez corpos do protótipo. O que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Confirmar com a aluna e o IML o nome do projeto (CNC ou TCIN).
  - [ ] Validar os quatro marcos e os livros que o app substitui.
  - [ ] Medir a linha de base de remoção, identificação e liberação.
  - [ ] Confirmar os campos do protótipo que o app assume (chegada ao local,
    câmara e gaveta, estado do corpo, os quatro materiais da necropsia e o
    alcance de cada perfil).


## Onda 2 concluída (03/11/2026)

- **Renovação de contratos**: fiscais e gestores com nome, e-mail e telefone; edição do contrato por ADM/gestor; aviso no semáforo e na ficha com fila local; objeto e busca na Instrução; importação da planilha do setor (`.xlsx`/`.csv`). Cenário `s8` 9/9.
- **Metas BI**: filtro de gerência no importador e na conferência; recorte de unidades monitoradas; cartão "Pendentes" só com monitoradas; total ajustado ao recorte; aprovação abre a planilha. Cenário `s8` 6/6.
- **TAP**: objetivos estratégicos editáveis em `#/config`; sanar pendências devolve o TAP para a análise; prazo de 5 dias úteis; fila local de avisos (demandante, equipe, autoridade); cartão de prazos na Triagem. Cenário `s8` 6/6.
- **Comissão de Ética**: texto do artigo visível e enquadramento padrão; membros em lista suspensa; fundamento padrão com datas e artigo; exclusão e encerramento de oitivas; ata com admissão/enquadramento; curso no relatório de recomendações; encerramento com o texto das recomendações; envio por `mailto:`. Cenário `s8` 9/9.
- **Testes**: `testar.py` 21/21 e `testar_sprints.py` 130/130. Sem commit.
- **Próxima onda**: Inscrições, Mapa de Distribuição, Gestão de Identificados (cruzamento) e Equipamentos (teste manual).


## Onda 3 concluída (03/11/2026)

- **Inscrições em cursos**: perfis diretoria, coordenação, gerência e chefe; instrutores e monitores no curso; termo de convocação com convocação e compensação, impressão, cópia e `mailto:`; checklist antes de divulgar e estado vazio na Triagem. Cenário `s10` 5/5.
- **Mapa de Distribuição**: leitura do relatório do pregoeiro em PDF (com aviso quando é imagem) e botão **Mapa orçamentário (SESP)** no Exportar. Cenário `s10` 3/3.
- **Gestão de Identificados**: botão **Ver corpos**, até 10 candidatos com motivo, confirmação/descarte/exame com justificativa em `correspondencias` e no `log` do corpo. Cenário `s5` 4/4.
- **Equipamentos**: nenhum ajuste de código; resta o teste manual do `.kmz` no Google Earth.
- **Testes**: `testar.py` 21/21 e `testar_sprints.py` 133/133. Sem commit.
- **Próximo passo**: teste manual do Google Earth, integração global (painel, hubs, links, diagramas) e entrega.

## 5. Resultado da verificação (30/10/2026)

%RESULTADO%


## Evento de Substituição Temporária (09/11/2026)

- **App**: `Apps/evento-substituicao-temporaria/` (Simone Alem, Gerência de Suporte à Gestão de Pessoas).
- **Fonte**: `evento-substituicao-temporaria/entregas/Evento de Substituição Temporária.docx`, com o texto em `envio-original.json`.
- **O que faz**: ofício no SIGADOC, autorização por nível da linha hierárquica, Gabinete de Direção, análise de RH com a ficha, assinatura do Diretor Geral Adjunto, envio à SESP até o dia 05, publicação no Diário Oficial e planilha de controle em Excel (`.xlsx`) e CSV. Cinco perfis, trilha de sete etapas e fila por perfil.
- **Sprints**: 0 a 8 feitos em 09/11/2026, mais a identidade (casca de trilho, "Minha fila", ficha em abas e trilho das etapas). O Sprint 8 trouxe o ajuste da unidade antes do reenvio e a planilha Excel com as abas Controle e Resumo.
- **Testes**: `python testes/testar.py` OK; `python testes/cenarios.py` 8 cenários (47 verificações) OK; `python testes/jornada.py` 8/8; `_base/testar.py` e `_base/testar_sprints.py` OK; formulário de feedback com 6 telas OK.
- **Repositório**: público em `github.com/renato0503/evento-substituicao-temporaria`.
- **Falta**: login da Simone para o convite de push; confirmar unidades, chefias e níveis; receber o desenho oficial da ficha; medir o volume mensal e o tempo por etapa no piloto; integração futura com o SIGADOC. As premissas estão em `PREMISSAS.md`.
