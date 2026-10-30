# Aula Politec — organização do curso e padrao dos cadernos

Este repositorio guarda o material da **Capacitacao POLITEC/MT em Analise de Dados
aplicada a Pericia Criminal** (Prof. Renato Rosa). O padrao de organizacao e o
mesmo que deu certo no curso SESP/MT: **uma aula = uma pasta `Aula N/`**, com
caderno vivo (HTML), PDF, slides e datasets.

> Leia este arquivo antes de criar ou alterar qualquer aula. Ele e o contrato do
> repositorio. O passo a passo de reproducao esta em **"Como criar uma nova aula"**.

---

## 0. Estado atual do curso (o que ja existe)

Cadernos entregues e validados. Todos seguem o mesmo motor (`caderno_lib.py`) e o
mesmo formato de 6 partes (ver secao 3.5).

| Aula | Tema | Seções | HTML | PDF | Labs | Cenários | Gerador |
|---|---|---|---|---|---|---|---|
| 1 | Fundamentos da Analise + Estatistica | 61 | 161 KB | 53 pág · 4,9 MB | 7 | 4 | 102 KB |
| 2 | Planilhas / Excel e Google Sheets | 68 | 174 KB | 60 pág · 3,8 MB | 7 + integrador | 4 | 111 KB |
| 2 | Planilhas / Google Sheets (adaptado) | 69 | 207 KB | 71 pág · 4,6 MB | 7 + integrador | 4 | 150 KB |
| 3 | Organizacao, Visualizacao e ETL | 64 | 144 KB | 48 pág · 4,2 MB | 7 | 4 | 86 KB |
| 4 | Business Intelligence / Power BI | 107 | 227 KB | PDF a regerar | 7 (+ guia Parte 0) | 3 + 4 casos | 146 KB |
| 5 | Dashboards de BI - 5 cenarios com datasets proprios | 80 | 140 KB | PDF opcional | 7 + integrador | 5 (cada um com dataset proprio) | 85 KB |
| 6 | Painel de Processo (manha) + Gestao de Projetos (tarde) | 80 | 417 KB | PDF opcional | 8 (4+4) | 5 datasets (3 modelados ponta a ponta) | 167 KB |
| 7 | Gargalo medido, Automacao e Antigravity | 68 | 378 KB | 135 pag | 8 (4+4) | 5 cenarios + 5 workbooks | 58.408 execucoes |
| 8 | Fase de ideacao e prototipacao (formulario, hub, MVP) | — | formulario-ideacao.html + hub + app.html | — | — | 14 blocos / 12 tabelas | — |

Ferramentas de apoio na raiz: `caderno_lib.py` (motor), `exportar_pdf.py` (PDF em 2
passadas), `validar.py` (checagem automatica) e `ptbr.py` (acentuacao pt-BR).
Slides de origem em cada `Aula N/`.

Aulas 5, 6 e 7 nao tem slides (e o salto final — A5 e projeto integrador de
dashboards com 5 datasets; A6 e o novo formato: manha de painel/BI e tarde de
gestao de projetos/melhoria de processos, com 5 datasets de processo; A7 e a
construcao do app: gargalo medido, automacao/digitalizacao, Antigravity e
GitHub).

> **Formato a partir da Aula 6**: a manha e sempre de **paineis, BI e analise de
> dados**; a tarde e de **hands-on em gestao de projetos** e, nas aulas
> seguintes, **ideacao/prototipacao de mini apps com IA agentica**. Ver secao
> 3.5.1.
>
> **Formato a partir da Aula 7**: a tarde nao redesenha o workflow (ja feito na
> Aula 6): ela parte do **gargalo medido no painel**, **propoe a intervencao
> com numero** (catalogo de automacao/digitalizacao, TO-BE em Mermaid, ganho e
> piloto) e **constroi o app no GitHub**, com o agente do **Antigravity**.

> **Idioma a partir da Aula 6**: o caderno e escrito em **portugues do Brasil,
> com acentuacao completa**, sem **adjetivacoes** (preferir o verbo ou o
> numero), sem **travessoes** e com **conectivos** ligando as frases depois do
> ponto final. Ver secao 5.2.

---

## 1. Estrutura de uma aula (o contrato)

```
Aula N/
├── README.md                     ← indice da aula (partes, labs, estatisticas)
├── caderno-diaN.html             ← fonte viva (tema claro/escuro, indice, busca)
├── Caderno Dia N - POLITEC.pdf   ← caderno exportado (A4, sumario com paginas)
├── Dia-N-Politec.pdf             ← slides do professor (material de sala)
├── gerar_caderno_aulaN.py        ← gerador Python do caderno (conteudo)
└── datasets/                     ← (opcional) CSVs sinteticos usados nos labs
    ├── README.md
    └── *.csv
```

Regras:

- **Nada solto na raiz.** Tudo pertence a uma pasta `Aula N/`.
- **Nao renomeie os slides** (`Dia-N-Politec.pdf`) — sao a fonte de verdade do conteudo.
- A unidade "uma aula = uma pasta" e o **contrato pedagogico**: o aluno do Dia 3
  sabe que encontra tudo em `Aula 3/`.
- Convencao de zero: **sem zero a esquerda** (`Dia-1`, `caderno-dia1.html`).

### Variacoes por tipo de aula

| Tipo | Acrescentar |
|---|---|
| Fundamentos / estatistica (ex.: Dia 1) | Labs de analise (papel, planilha ou Python) |
| Excel / planilhas (ex.: Dia 2 a 3) | `datasets/*.csv` + planilha modelo `.xlsx` |
| Power BI / modelagem (ex.: Dia 4+) | `fato_*` + `dim_*` + `.pbix` |
| Python / analise | `analise_*.py`, `.png` de graficos, relatorio `.md` |

---

## 2. Nomes de arquivo (convencao)

| Arquivo | Convencao | Exemplo |
|---|---|---|
| Slides do professor | `Dia-{N}-Politec.pdf` | `Dia-1-Politec.pdf` |
| HTML do caderno | `caderno-dia{N}.html` | `caderno-dia1.html` |
| PDF do caderno | `Caderno Dia {N} - POLITEC.pdf` | `Caderno Dia 1 - POLITEC.pdf` |
| Gerador do caderno | `gerar_caderno_aula{N}.py` | `gerar_caderno_aula1.py` |
| Pasta de dados | `datasets/` | `datasets/` |
| README | `README.md` (MAIUSCULO) | `README.md` |

---

## 3. Arquitetura do material

### 3.1 Slides x caderno (papeis diferentes)

- **Slides** (`Dia-N-Politec.pdf`): o que e projetado em sala. Sintetico, visual.
- **Caderno** (`caderno-diaN.html`): material de **aprofundamento**. O aluno leva
  para casa, abre no tablet/celular, navega pelo indice, busca, muda o tema e
  imprime. Ele **ancora** o que foi dito em sala: exemplos extras, pegadinhas,
  passo a passo de cliques, quiz e folha de cola.

O caderno **nao substitui o professor** e **nao reescreve os slides** — ele expande.

### 3.2 Um arquivo so

O caderno e autossuficiente: CSS embutido no `<style>`, zero JS de build, zero
dependencia local. Tipografia via Google Fonts (falha graciosamente offline).
Abre com duplo clique em qualquer maquina.

- **Tema claro/escuro**: variaveis CSS em `:root` + `:root[data-theme="dark"]`,
  respeitando `prefers-color-scheme`, com botao manual.
- **Tipografia tripla**: `Archivo` (UI), `JetBrains Mono` (codigo), `Source Serif 4`
  (corpo de leitura).
- **Nunca** use cor hardcoded fora de `:root` — sempre `var(--accent)` etc.

### 3.3 O motor compartilhado: `caderno_lib.py`

Para nao repetir ~400 linhas de CSS em cada aula, o CSS e os helpers ficam em
**[`caderno_lib.py`](./caderno_lib.py)** (na raiz). Cada gerador importa a classe
`Caderno` e os helpers, e declara **so o conteudo**.

```python
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from caderno_lib import (Caderno, p, h3, ul, checklist, ficha, callout, tbl,
                         code, step, q, aplicab, grid2, flow_h, kpi,
                         antesdepois, legenda, glossary, bar_chart)
```

Componentes disponiveis (ver secao 5):

| Helper | Para que serve |
|---|---|
| `p(txt)` | paragrafo |
| `h3/h4(txt)` | subtitulo |
| `ul(items)` / `checklist(items)` | lista / lista com checkbox |
| `ficha(kind, label, body)` | destaque lateral (`""`,`g`,`a`,`r`,`p`) |
| `callout(kind, label, body)` | nota (`note`,`tip`,`err`,`purple`) |
| `tbl(headers, rows, num_cols=None)` | tabela |
| `code(text, lang)` | bloco de codigo com rotulo e botao Copiar |
| `step(items)` | passo a passo numerado |
| `q(stem, options, ans_idx, hint="")` | quiz com gabarito expansivel |
| `aplicab(quando, porque, exemplo)` | bloco QUANDO / POR QUE / EXEMPLO |
| `grid2(cards)` | grade de 2 cards |
| `flow_h(nodes)` | fluxo horizontal com setas |
| `kpi(items)` | painel de indicadores |
| `antesdepois(ruim, bom, ...)` | comparacao certo x errado |
| `legenda(items)` | cards com icone + titulo + descricao |
| `glossary(items)` | lista de definicoes |
| `bar_chart(labels, values, ...)` | grafico de barras (histograma / comparacao) |

### 3.7 Biblioteca de SVG (`caderno_svg.py`)

Para quando o caderno precisa de **diagrama**, nao so de texto. Sem dependencia
externa, sem CDN: sao `<svg>` inline que herdam as variaveis de cor do tema
(`var(--ink)`, `var(--accent)`, `var(--verde)`, `var(--vermelho)`,
`var(--ambar)`, `var(--roxo)`) e por isso funcionam no tema claro, no escuro e
na impressao.

```python
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from caderno_svg import (icon, icon_row, gallery, swimlane_anatomy,
                         gates_anatomy, wait_vs_touch, automation_anatomy,
                         method_chain, Dia,
                         build_process_asis, build_process_tobe)
```

**O que a biblioteca oferece**

| Chamada | Devolve |
|---|---|
| `icon("gateway-exclusive")` | um simbolo BPMN 2.0 isolado (inline svg) |
| `icon_row([("start", "Inicio"), ...])` | linha de icones com legenda |
| `gallery()` | galeria com **todos** os simbolos BPMN (eventos, atividades, gateways, fluxos, objetos) |
| `swimlane_anatomy()` | anatomia de pool + lanes |
| `gates_anatomy()` | comparacao dos 3 gateways (X, +, O) |
| `wait_vs_touch(92)` | barra espera x execucao |
| `automation_anatomy()` | AS-IS x TO-BE com o ponto de intervencao |
| `method_chain()` | cadeia de passos do metodo |
| `build_process_asis()` / `build_process_tobe()` / `build_process_orcamento()` / `build_process_custodia()` | diagramas de processo completos |

**Construtor de diagramas (classe `Dia`)** — para desenhar processos novos:

```python
d = Dia(980, 540, "Titulo do diagrama")
d.lane(0, 44, 980, 110, "DELEGACIA", "orgao requisitante")   # swimlane
d.start(178, 102); d.end(925, 480)                            # eventos
d.task(300, 102, "Registrar|no SIGT", w=148, sub="manual", glyph="human")
d.gw_x(438, 202, "Dados completos?", size=46)                 # gateway X
d.flow([(376, 202), (411, 202)], label="Sim", lx=500, ly=250) # fluxo rotulado
d.timer(560, 150)                                            # evento de fronteira
d.note(150, 300, 330, "texto da anotacao", tone="r")
return d.render("legenda", "subtitulo")
```

Paletas: `tone="n" | "a" (accent) | "g" (verde) | "w" (ambar) | "r" (vermelho) | "p" (roxo)`.
Glifos de atividade: `glyph="human"` (pessoa) ou `glyph="bot"` (robo = automatizada).

> **Regra**: ao acrescentar uma figura SVG, confira que nada sai do `viewBox`
> (texto cortado) e que nenhum rotulo colide. Renderize com Playwright e olhe.

### 3.8 Apps dos grupos (`Apps/`)

A partir da Aula 8, cada projeto entregue no formulario ganha uma pasta em
`Apps/<slug-do-projeto>/`. O material do curso continua em `Aula N/`; o codigo
dos mini apps fica em `Apps/`.

Regras:

- uma pasta por grupo, com `README.md`, `PROJETO.md`, `contexto.md`, `sprint.md`,
  `projeto.json`, `envio-original.json`, `app.json`, `src/` e `exemplos/`;
- `envio-original.json` nunca e editado; `projeto.json` e a versao completada
  pelo professor e `PROJETO.md` e gerado a partir dele;
- app = **um unico `index.html`** (CSS, JS, libs e dados embutidos), offline
  first, IndexedDB e backup `.json`. A excecao e `agendamento-cin`, servido pelo
  Google Apps Script porque a agenda publica precisa de fonte unica de vagas;
- **edite as fontes, nunca o `index.html`**: ele e gerado por
  `Apps/_base/construir.py` a partir de `_base/base.html` + `_base/js_comum.js`
  + `<app>/app.json` + `<app>/src/*.js` (o `app.js` primeiro, depois
  `sprint1.js`, `sprint2.js`...);
- os dados ficticios tem semente fixa e vivem em `<app>/exemplos/seed.json`,
  gerados por `<app>/exemplos/gerar_exemplos.py`;
- **premissas**: quando um item do Sprint 0 depende de decisao institucional,
  documento oficial ou medicao do processo real, assume-se um valor plausivel e
  registra-se em `Apps/PREMISSAS.md` (valor, onde aparece no app, nivel de
  confianca A/B/C e o que confirmar). As referencias que faltam vao para
  `<app>/modelos/` (ou `<app>/horus/`, quando for esquema de banco);
- bibliotecas de terceiros ficam em `<app>/vendor/`, com versao e SHA-256 em
  `VERSOES.md`;
- **visual**: cada app tem um bloco `visual` no `app.json` (acento, emblema,
  layout `lateral`/`topo`, padrao do cabecalho, estilo `institucional`/`claro`,
  setor). O tema claro e o padrao; o escuro so entra pelo botao. A fonte vai de
  80% a 150% pelos botoes A-/A+. Nao ha faixa de aviso de prototipo. Detalhes em
  `Apps/IDENTIDADE-VISUAL.md`;
- **passagem para outro agente**: `Apps/CONTINUAR.md` traz o que foi feito e o
  proximo passo de cada app;
- **o que depende de fora fica como "a implementar"**: quando uma etapa precisa de
  servico externo (Apps Script, `LockService`, `MailApp`, gatilho, banco, e-mail),
  o app faz a parte local (fila, releitura, botao) e o passo a passo de como
  ligar fica no array `AJUDA_TECNICA` do app. O painel abre com **tres cliques no
  nome do app, no rodape** (e nao aparece no menu).

Ferramentas (em `Apps/_base/`):

| Arquivo | O que faz |
|---|---|
| `base.html` | Base comum: faixa do governo, cabecalho com emblema, botoes de fonte e tema, roteador por hash, IndexedDB, perfis, backup, carga dos dados ficticios e a tela `#/testes`. |
| `visual.css` | Identidade visual SESP/MT e POLITEC/MT comum a todos os apps (paleta, tema claro padrao e escuro, componentes). Ver `Apps/IDENTIDADE-VISUAL.md`. |
| `icones.js` | 48 icones das telas e do emblema, com escolha automatica pelo titulo da rota. |
| `construir.py` | Gera o `index.html` de cada app. Uso: `python Apps/_base/construir.py` (todos) ou `python Apps/_base/construir.py <app>`. |
| `js_comum.js` | Tela de configuracao e testes comuns a todos os apps. |
| `embutir.py` | Copia `vendor/*.js` e os JSON de dados para dentro do `index.html`, entre os marcadores `<!-- LIB:... -->` e `<!-- DADOS:... -->`. |
| `testar.py` | Abre cada app no Chromium e confere zero requisicao de rede, `#/testes` 100%, todas as rotas, dados ficticios, persistencia e tema. |
| `testar_sprints.py` | Um cenario de interface por sprint: usa a tela como uma pessoa usaria e confere o "Pronto quando" do `sprint.md`. Os cenarios do Sprint 3 em diante ficam em `Apps/_base/cenarios/sprintN.py`. |
| `equipes.py` | Grava o login do GitHub de um aluno em `equipes.json` e refaz a tabela "Equipes e GitHub" do `Apps/README.md`. Uso: `python Apps/_base/equipes.py <app> "<nome>" <login>`. |
| `painel.py` | Gera `Apps/painel.html`, o painel de desenvolvimento: telas prontas x pendentes por sprint, itens abertos, GitHub e trabalhos de BI. Uso: `python Apps/_base/painel.py` (e `python Apps/_base/hub_apps.py` para o hub). |
| `equipes.json` | Fonte dos logins (um repositorio por app). |
| `Aula 8/Entregas/` | Respostas originais dos alunos (JSON/MD) e os `.pbix` da turma. |

Sequencia ao mexer num app:

```powershell
python Apps/_base/construir.py <app>                  # gera o index.html
python Apps/_base/testar.py <app>                     # estrutura
python Apps/_base/testar_sprints.py <app>             # cenario de cada sprint
node Apps/agendamento-cin/testes/testar_code_gs.js    # apenas o agendamento
```

Estado (30/10/2026): **20 apps**, todos com a identidade visual SESP/MT e
POLITEC/MT. Os 12 primeiros estao com os Sprints 1, 2 e 3 feitos (dois deles,
`cin-segunda-via` e `metas-bi-ocr`, com o Sprint 4 parcial). Os 8 novos
(`custodia-definitiva`, `trilha-custodia-necropsia`, `passivo-ambiental`,
`renovacao-contratos-horus`, `documentapolitec`, `gestao-documentos`,
`controle-aquisicoes` e `distribuicao-casos-dna`) estao com os Sprints 1, 2 e 3.
Todos tem a parte tecnica do Sprint 0 (dados ficticios, bibliotecas, modelos).
Os itens do Sprint 0 que dependiam de pessoas foram **elucubrados** em
30/10/2026: cada um tem um valor plausivel assumido, documentado em
`Apps/PREMISSAS.md` com o nivel de confianca e o que precisa ser confirmado.
As referencias que faltavam (modelos de DFD, ETP, TR, TAP, ata, laudo, caixa,
marcos, plano de trabalho, esquema do Hórus) foram criadas nas pastas
`modelos/` e `horus/` dos apps. Os cenarios do Sprint 2 dos apps novos ficam em
`Apps/_base/cenarios/sprint2.py`; os do Sprint 3, em `cenarios/sprint3.py`; os do
Sprint 4 em diante, em `cenarios/sprintN.py`. O proximo passo de cada app esta em
`Apps/CONTINUAR.md`. Detalhes em `Apps/README.md`.

### 3.4 Estado do documento

```python
cad = Caderno(
    out="caderno-dia1.html",
    dia=1,
    kicker="Aula 1 · Fundamentos da Analise",
    headline="Fundamentos da Analise de Dados e Estatistica aplicada a Pericia",
    sub="...",
    meta="Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 1",
    descricao="<meta name=description>",
)

cad.grp("Parte 1 · Fundamentos da Analise", "descricao da parte")
cad.section("anchor", "Titulo da secao", p("...") + callout("tip", "...", "..."))

cad.build()   # escreve o HTML em `out`
```

- `grp()` abre um grupo (parte). Toda `section()` entra no grupo aberto.
- `section()` recebe `(anchor, titulo, body_html)`; `body_html` e uma string
  concatenada com `+`.
- `build()` monta header, sumario, indice lateral (TOC com busca), secoes, JS e
  escreve o arquivo. Se receber um JSON de mapa de paginas (2a passada do PDF),
  imprime os numeros de pagina no sumario.

### 3.5 Formato expandido do caderno (6 partes)

Cada caderno grande segue **6 grupos** (partes), nesta ordem:

```
Abertura                          → boas-vindas, como usar, mapa do dia, roadmap do curso
Parte 1 · <Modulo da manha>       → conceitos + como fazer (step) + aplicacoes
Parte 2 · <Modulo da tarde>       → conceitos + como fazer (step) + aplicacoes
Parte 3 · Pratica guiada          → 6-8 laboratorios com passo a passo de cliques
Parte 4 · Cenarios e aplicacoes   → 3-4 cenarios reais da POLITEC (problema > KPIs > passos)
Parte 5 · Fechamento              → quiz (12-15), folha de cola/glossario, referencias
```

Dentro de cada secao de conteudo, o ritmo e: paragrafo de abertura + pelo menos
2 componentes variados (ficha, callout, `aplicab`, `tbl`, `step`, `grid2`,
`legenda`, `antesdepois`, `flow_h`, `kpi`, `code`, `bar_chart`). Use `step` para
todo "como fazer" (cliques, atalhos, contas) e `aplicab` para conectar com a
POLITEC.

### 3.5.1 Formato em dois turnos (a partir da Aula 6)

A partir da **Aula 6**, o curso passa a operar em dois turnos com papeis
distintos. O caderno deve refletir essa divisao explicitamente (no mapa do dia,
nos grupos e nos labs):

```
Manha (08h-12h)  → paineis, BI e analise de dados
                   modelo, medidas, layout, leitura do painel, datasets

Tarde (13h-17h)  → hands-on: gestao de projetos, BPMN/Mermaid, AS-IS/TO-BE
                   e, a partir das proximas aulas, ideacao/prototipacao de
                   mini apps com IA agentica
```

Regras do formato:

- **A manha comeca pelo dado** e termina com uma leitura/hipotese em uma frase.
  Nao ha tarde sem a evidencia da manha.
- **A tarde comeca pela leitura da manha** (nao do zero) e termina com um
  artefato: diagrama AS-IS, TO-BE, canvas do mini app ou pitch.
- **Cada dataset da manha vira uma receita** (`receita()` no gerador): **72
  passos em 8 blocos**, do workbook Excel ao `.pbix` publicado. Os blocos sao:
  (1) preparar o arquivo no Excel, (2) importar os dados no Power BI, (3) tratar
  no Power Query, (4) montar o modelo, (5) criar as medidas, (6) montar o painel,
  (7) filtros, segmentacoes e tabela resumo, (8) formatar, salvar e publicar.
  Cada passo traz o caminho do menu e o que esperar na tela.
- **Cada dataset e um workbook `.xlsx`** com todas as tabelas em abas
  (`LEIA-ME`, `fato_*`, `dim_*`). O CSV fica como fonte; o `.xlsx` e o material
  de sala.
- A tarde da Aula 6 fica em **fundamentos e nocoes** de gestao de projetos. A
  prototipacao de mini apps com IA agentica comeca nas aulas seguintes.

Estrutura de referencia da Aula 6 (10 partes, 80 secoes): Abertura; Parte 1
(fundamentos do painel); Parte 2 (5 receitas, uma por dataset); Parte 3
(analise: espera x execucao, Pareto, Little's Law); Parte 4 (fundamentos de
projeto); Parte 5 (BPMN/Mermaid); Parte 6 (texto -> diagrama); Parte 7 (TO-BE e
intervencao digital); Parte 8 (8 labs); Parte 9 (3 cenarios modelados); Parte
10 (fechamento).

### 3.6 Ferramentas do repositorio (na raiz)

| Arquivo | O que faz |
|---|---|
| `caderno_lib.py` | Motor compartilhado: CSS, helpers e a classe `Caderno`. |
| `caderno_svg.py` | Biblioteca de **SVG**: icones da **notacao BPMN 2.0** (geometria oficial OMG) + construtores de diagramas. SVG inline puro, herda `var(--ink)`, `var(--accent)`, `var(--verde)`... e por isso acompanha o tema claro/escuro e a impressao sem CSS extra. Ver secao 3.7. |
| `exportar_pdf.py` | Exporta `caderno-diaN.html` -> `Caderno Dia N - POLITEC.pdf` (2 passadas, numero de pagina no sumario). Uso: `python exportar_pdf.py N`. |
| `validar.py` | Checa secoes x links do TOC x `h2`, links orfaos, tema escuro e erros de console. Uso: `python validar.py N` (deve imprimir `OK`). |
| `gerar_datasets_estrela.py` | Le as fontes planas de `Aula 2/datasets/` e monta o modelo estrela (`fato_*` + `dim_*` + `dim_calendario`) nas pastas `datasets/` das Aulas 2, 3 e 4. Uso: `python gerar_datasets_estrela.py`. |
| `Aula 4/gerar_datasets_orcamento.py` | Gera o conjunto de **orcamento e contratos** da Parte 0 do Dia 4 (star schema, `fato_empenhos` 620 linhas): `Orcamento_Contratos_SUJO.xlsx` (14 defeitos plantados), `Orcamento_Contratos_LIMPO.xlsx` (gabarito) e os CSV em `Aula 4/datasets/orcamento/`. Uso: `python "Aula 4/gerar_datasets_orcamento.py"`. |
| `Aula 5/gerar_datasets_aula5.py` | Gera os **5 datasets sinteticos** da Aula 5 (um por cenario), cada um com `fato_*` >= 1000 linhas, dimensoes proprias + `dim_calendario` 1096 dias (2023-01-01 a 2025-12-31). Semente fixa = 20260120. Grava em `Aula 5/datasets/cenarioN_*/` + um `README.md` por cenario com esquema e visuais sugeridos. Uso: `python "Aula 5/gerar_datasets_aula5.py"`. |
| `Aula 6/gerar_datasets_aula6.py` | Gera os **5 datasets de processo** da Aula 6 (requisicao pericial, empenho e contrato, cadeia de custodia, local de crime, analise laboratorial). Mesmo schema nos 5: `fato_execucao` (1 linha por execucao de etapa, com `tempo_espera_min` e `tempo_execucao_min` separados) + `dim_etapa`, `dim_unidade`, `dim_sistema`, `dim_tipo_atividade`, `dim_status_execucao`, `dim_projeto`, `dim_calendario` 1096 dias. Semente fixa = 20260610. Tempos de espera lognormal (cauda longa realista), calibrados para que 86-93% do processo seja espera — assim o gargalo emerge do dado, nao e plantado. Grava em `Aula 6/datasets/cenarioN_*/` + README por cenario com a tabela de tempos medidos. Uso: `python "Aula 6/gerar_datasets_aula6.py"`. |
| `Aula 6/gerar_excel_aula6.py` | Empacota cada um dos **5 datasets** em um **workbook `.xlsx`** com 9 abas (`LEIA-ME` + `fato_execucao` + 7 `dim_*`), cabecalho formatado, filtro, painel congelado e a tabela-resumo medida na aba `LEIA-ME`. E o material de sala da manha. Uso: `python "Aula 6/gerar_excel_aula6.py"` (depois do gerador de datasets). |
| `Aula 7/gerar_datasets_aula7.py` | Gera os **5 datasets novos** da Aula 7 (apreensao de armas, sinistro de transito, credenciamento de peritos, etilometria, atendimento/ouvidoria). Mesmo schema da Aula 6: `fato_execucao` (1 linha por execucao de etapa) + as 7 dimensoes. **58.408 execucoes**. Semente fixa = 20261027. Uso: `python "Aula 7/gerar_datasets_aula7.py"`. |
| `Aula 7/gerar_excel_aula7.py` | Empacota os **5 datasets novos** em um workbook `.xlsx` por cenario, com 9 abas e a tabela-resumo medida. Uso: `python "Aula 7/gerar_excel_aula7.py"`. |
| `ptbr.py` | **Acentuacao pt-BR do caderno**: percorre os nos de texto do HTML gerado e aplica a ortografia de `ptbr_dict.json`, sem tocar em codigo, tags, atributos, SVG ou blocos Mermaid/DAX/SQL. Remove travessoes. Chamado no fim do gerador da Aula 6 (`ptbr.acentuar_arquivo(...)`). Uso: `python -c "import ptbr; ptbr.acentuar_arquivo('Aula 6/caderno-dia6.html')"`. |
| `ptbr_dict.json` | **Dicionario de acentuacao** usado pelo `ptbr.py` (403 entradas: `nao` → `não`, `execucao` → `execução`, `analise` → `análise`, `manha` → `manhã` e afins). Ao acrescentar palavra nova no texto, inclua a entrada aqui. |
| `firebase.json` | Configuracao do Firebase Hosting (projeto `aulapolitec`, serve da raiz). |
| `.firebaserc` | Aponta para o projeto `aulapolitec`. |

Sequencia padrao ao mexer numa aula:

```powershell
python "Aula N\gerar_caderno_aulaN.py"   # gera o HTML
python validar.py N                       # precisa dar OK
python exportar_pdf.py N                  # gera o PDF (opcional)
firebase deploy                           # publica no Firebase Hosting
```

> **Firebase Hosting**: o site esta em `https://aulapolitec.web.app`. Para fazer deploy,
> basta rodar `firebase deploy` na raiz (requer `firebase-tools` instalado e login feito).
> Arquivos Python, CSVs, MD e `analises/` estao excluidos do `firebase.json`.

> Nota: o PDF usa o mesmo HTML, mas o layout de impressao A4 ainda nao e fiel ao
> visual de tela. O HTML e a fonte de verdade; o PDF e um extra.

---

## 4. Pipeline de producao

```
slides Dia-N-Politec.pdf
  └── extrair o conteudo (pdfplumber / leitura)
       └── outline em partes + secoes
            └── gerar_caderno_aulaN.py  (conteudo + helpers)
                 └── caderno-diaN.html  (fonte viva)
                      └── exportar_pdf.py → "Caderno Dia N - POLITEC.pdf"
                           └── validacao (Playwright / console)
```

### Como criar uma nova aula

1. **Slides**: coloque `Dia-N-Politec.pdf` em `Aula N/`.
2. **Extrair o conteudo** dos slides (ex.: `python -c "import pdfplumber..."`) e
   salvar o texto num `.txt` de trabalho.
3. **Esbocar** o outline no formato da aula: **6 partes** para as aulas 1-5 ou
   **dois turnos / 10 partes** para as aulas 6+ (manha de BI, tarde de projeto) —
   ver secoes 3.5 e 3.5.1. A partir da Aula 6, cada dataset da manha vira uma
   **receita** de 72 passos em 8 blocos e um workbook `.xlsx` com todas as tabelas em abas.
4. **Copie** `Aula 1/gerar_caderno_aula1.py` (ou a Aula 2, mais completa) como
   `Aula N/gerar_caderno_aulaN.py` e ajuste `Caderno(...)` + as secoes.
5. **Rode**: `python "Aula N/gerar_caderno_aulaN.py"` → confere o HTML no navegador.
6. **Valide**: `python validar.py N` (precisa imprimir `OK`).
7. **Exporte o PDF**: `python exportar_pdf.py N` (2 passadas; ver secao 6).
8. **README.md** da aula (indice + labs + cenarios + estatisticas).

> Meta de tamanho: cada caderno tem **55-71 secoes**, com 6-8 labs e 3-4 cenarios.
> E o que diferencia o caderno (aprofundamento) dos slides (sala de aula).

---

## 5. Diretrizes de conteudo

Uma boa secao do caderno segue este ritmo:

```
§ N. Titulo
    [paragrafo curto de abertura]
    [ficha: o conceito central]        ou [callout note/tip]
    [bloco QUANDO / POR QUE / EXEMPLO na POLITEC]   (aplicab)
    [tabela ou lista comparativa]
    [passo a passo com cliques/atalhos]              (step)
    [quiz com <details>]                             (q)
```

- **Exemplo sempre na POLITEC.** Todo conceito ganha um caso de laboratorio/IML/TAT.
- **Pelo menos um `callout("err", ...)`** por armadilha classica.
- **Fechamento**: quiz (12-15), folha de cola/glossario e referencias.
- **Labs** (Parte 3) e **cenarios** (Parte 4) em secoes proprias — ver secao 3.5.
- **Caderno grande e detalhado**: toda secao pratica traz um `step` de "como fazer"
  (cliques/atalhos/contas) e um `aplicab` (QUANDO / POR QUE / EXEMPLO). A meta e
  55-71 secoes por aula.
- Texto em **portugues sem acentos** (ex.: `analise`, `nao`, `referencia`) — padrao
  das Aulas 1 a 5. **A partir da Aula 6, o padrao muda**: ver secao 5.2.
  Numeros devem ter fonte (do slide ou do dataset).
- **Encoding**: Python e HTML em UTF-8; evite aspas duplas dentro de string
  delimitada por aspas duplas (use aspas simples ou `&quot;`).

### 5.2 Idioma e estilo do texto (Aula 6 em diante)

A partir da **Aula 6**, o caderno e escrito em **portugues do Brasil, com
acentuacao completa**. As regras valem para todo o texto visivel: paragrafos,
titulos, tabelas, callouts, passos, quiz e glossario.

| Regra | Como aplicar | Exemplo |
|---|---|---|
| **Acentuacao completa** | Toda palavra recebe a grafia oficial: `análise`, `execução`, `gestão`, `não`, `número`, `mês`, `manhã`, `custódia` | nao escrever "analise" nem "nao" |
| **Sem adjetivacoes** | Prefira o verbo, o numero ou o fato. Nada de "muito bom", "enorme", "simples", "robusto", "claro", "forte" | "o painel e o gargalo" em vez de "o painel e claro" |
| **Sem travessoes** | Nunca use `—` ou `–`. Troque por virgula, ponto ou dois-pontos | "o processo mede 44 h de espera, e nao 5 h" |
| **Conectivos apos o ponto final** | Ligue as frases com "Além disso", "Por isso", "Dessa forma", "Nesse sentido", "Com isso", "Em seguida", "Por fim" | "A espera ocupa 92% do tempo. Além disso, a etapa 4 concentra 41,5% dela." |
| **Verbo no lugar de substantivo abstrato** | "O painel mostra" em vez de "Ha uma evidencia no painel" | "a fila cresce no fim do dia" |
| **Numeros com fonte** | Todo numero vem do slide ou do dataset medido | "41,5% da espera (dataset cenario1)" |

Exemplo de paragrafo no padrao da Aula 6:

> Todo processo tem dois tipos de tempo. O primeiro e o tempo em que alguem
> trabalha, e o segundo e o tempo em que o caso fica parado, esperando.
> Alem disso, nos cinco processos da POLITEC, a espera representa de 86% a
> 93% do tempo total. Por isso, o problema nao esta na velocidade com que as
> pessoas trabalham, e sim no tempo em que os casos ficam parados na fila.

**Ferramenta de apoio**: `ptbr.py` aplica a acentuacao no HTML gerado, usando o
`ptbr_dict.json`. Ele nao altera codigo, tags, atributos, SVG nem blocos
Mermaid/DAX/SQL. Ao escrever uma palavra nova no texto, inclua a entrada no
dicionario para que a acentuacao continue correta.

### Armadilhas de autoria (ja vistas no SESP)

| Armadilha | Como evitar |
|---|---|
| Variavel de loop sobrescreve o parametro `titulo` | Use nomes distintos nos loops (`k_nome`, `v_titulo`) |
| `visual=`/`bonus=` antes da lista de passos | Ordem: posicionais → keywords |
| Aspas duplas dentro de string delimitada por aspas duplas | Use aspas simples |
| `<div class="shell"><div class="wrap">` | O motor ja faz certo: nao mexa no grid |

---

## 6. Exportacao de PDF

`exportar_pdf.py` (na raiz) faz **duas passadas**: gera o HTML + PDF, descobre em
que pagina cada secao comecou, regera o HTML com os numeros no sumario e exporta
de novo. Usa Playwright (Chromium) com `prefer_css_page_size` e fonte de rodape
com numero de pagina.

```powershell
python exportar_pdf.py 1     # exporta Aula 1 -> "Caderno Dia 1 - POLITEC.pdf"
python exportar_pdf.py 2     # exporta Aula 2
python exportar_pdf.py 3     # exporta Aula 3
python exportar_pdf.py 4     # exporta Aula 4
```

Requisitos: `pip install playwright pymupdf` e `playwright install chromium`.

> **Estado do PDF**: todos os cadernos ja tem PDF A4 com sumario paginado, mas o
> layout de impressao **ainda nao e fiel ao visual de tela** (o `@media print` atual
> comprime as secoes). O HTML e a fonte de verdade. Melhoria pendente: um
> `@media print` dedicado, com capa e quebras de pagina por parte.

Alternativa sem Playwright (sem numero de pagina no sumario):

```powershell
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
& $edge --headless=new --disable-gpu --no-sandbox --hide-scrollbars `
        --print-to-pdf="Aula 1\Caderno Dia 1 - POLITEC.pdf" `
        --virtual-time-budget=15000 "file:///D:/Dev/Aula%20Politec/Aula%201/caderno-dia1.html"
```

---

## 7. Convencoes de repositorio

- **Encoding**: UTF-8 em todo codigo e HTML.
- **Indent**: 4 espacos (Python), 2 espacos (CSS/JS/HTML).
- **Datas em CSV**: `AAAA-MM-DD` (ISO). CSV de trabalho: UTF-8 com BOM, `;`.
- **Sem PII real**: datasets sempre sinteticos/anonimizados.
- **Sem dependencia externa** no HTML do caderno (nada de CDN de JS).

---

## 8. Publicacao do site

O site do curso e publicado em **dois lugares**, a partir do mesmo repositorio
`renato0503/Aula_politec` (branch `main`):

| Canal | Endereco | Como e publicado |
|---|---|---|
| GitHub Pages | `https://renato0503.github.io/Aula_politec/` | Push na branch `main`: o Pages serve a raiz do repositorio |
| Firebase Hosting | `https://aulapolitec.web.app` | `firebase deploy` na raiz (projeto `aulapolitec`) |

Fluxo de publicacao:

```powershell
python "Aula N\gerar_caderno_aulaN.py"     # gera o HTML
python validar.py N                        # precisa imprimir OK
git add <arquivos da aula> <docs>
git commit -m "Aula N: <resumo>"
git push origin main
```

Regras de publicacao:

- **Push apenas do que pertence a entrega.** Arquivos modificados por outros
  trabalhos (por exemplo, os workbooks de dados da Aula 4) ficam fora do commit.
- **O cache do CDN do GitHub Pages leva de 1 a 10 minutos.** Apos o push, a
  pagina pode continuar servindo a versao anterior por alguns minutos. Para
  conferir se o commit chegou, use
  `https://raw.githubusercontent.com/renato0503/Aula_politec/main/<caminho>`.
- **Os workbooks `.xlsx` sao publicados junto**, e podem ser baixados direto do
  site, em `Aula 6/datasets/cenarioN/`.
- O `index.html` da raiz e o hub do curso: ele resume as aulas e deve ser
  atualizado sempre que uma aula mudar de tema, de estrutura ou de numero de
  secoes.

---

## 9. Checklist de "pronto"

- [ ] `README.md` da aula escrito (partes + labs + cenarios + estatisticas).
- [ ] `caderno-diaN.html` abre com duplo clique; TOC e main sem sobreposicao.
- [ ] Tema escuro funciona; `meta name="description"` preenchido.
- [ ] `python validar.py N` imprime `OK` (secoes == links TOC == `h2`, sem orfaos,
      sem erro de console).
- [ ] Quiz com `<details>` (gabarito) no fim; respostas abrem no PDF.
- [ ] `Caderno Dia N - POLITEC.pdf` gerado (quando desejado).
- [ ] Tudo dentro de `Aula N/`; nada solto na raiz.
- [ ] `AGENTS.md`, `README.md` e `Aula N/README.md` atualizados com o que foi
      feito, e o `index.html` da raiz conferido.
- [ ] Commit feito e `git push origin main` executado.

---

## 10. Historico de producao

| Etapa | O que foi feito |
|---|---|
| Fundacao | Criados `AGENTS.md`, `caderno_lib.py` (motor), `exportar_pdf.py`, `validar.py`. |
| Aulas 1 e 2 (v1) | Primeiros cadernos (32 e 37 secoes), extraidos dos slides. |
| Aulas 3 e 4 | Cadernos novos (63 e 71 secoes) seguindo o mesmo motor e formato de 6 partes. |
| Aulas 1 e 2 (v2) | Expandidos para 61 e 68 secoes: mais `step`, `aplicab`, labs e cenarios. |
| Firebase Hosting | Configurado `firebase.json` e `.firebaserc` para hospedagem em `aulapolitec.web.app`. |
| Aula 2 — Datasets | Criados 4 CSVs sinteticos em `Aula 2/datasets/`: `requisicoes_periciais.csv` (120 linhas), `movimentacao_reagentes.csv` (80), `produtividade_peritos.csv` (218), `orcamento_setores.csv` (36). Caderno atualizado com referencias aos datasets reais em todos os exemplos, labs e cenarios. |
| Aula 2 — Google Sheets | Caderno reescrito a partir de "SE aninhado x SES": passo a passo no Google Sheets (pt-BR, com acentos), tom sem adjetivacoes e exemplos ancorados nos datasets. 69 secoes. |
| Modelo estrela | Criado `gerar_datasets_estrela.py`, que monta 4 tabelas fato + 10 dimensoes (+ `dim_calendario`) nas pastas `datasets/` das Aulas 2, 3 e 4. Cadernos atualizados: Aula 2 (secao fato x dimensao), Aula 3 (Lab 7 de ETL) e Aula 4 (Obter Dados, relacionamentos e Power Query sobre o modelo). |
| Hub + GitHub | `index.html` publicado no Firebase Hosting e no GitHub Pages (`aulapolitec.web.app`). Link do Google Drive adicionado ao hub. |
| Aula 4 — Parte 0 (guia do iniciante) | Adicionada a **Parte 0** ao caderno do Dia 4 (30 secoes, 77 -> 107): passo a passo completo do Power BI Desktop para iniciantes, da instalacao as 3 abas do painel. Novo dataset de **orcamento e contratos** (star schema, `fato_empenhos` com 620 linhas) em `Aula 4/datasets/orcamento/`: `Orcamento_Contratos_SUJO.xlsx` (14 defeitos plantados) + `Orcamento_Contratos_LIMPO.xlsx` (gabarito) + CSVs, gerado por `Aula 4/gerar_datasets_orcamento.py`. |

Melhorias pendentes:

1. **PDF fiel ao HTML** — reescrever o `@media print` em `caderno_lib.py` (capa,
   quebras por parte, tipografia de impressao) para o PDF seguir o padrao da tela.
2. **Aula 5** — quando houver slides, seguir a secao "Como criar uma nova aula".
3. **Datasets para a Aula 1** — gerar CSVs sinteticos analogos aos da Aula 2.

---

## Historico de producao — continuacao

| Etapa | O que foi feito |
|---|---|
| Aula 5 — Dashboards de BI | Criados **5 datasets sinteticos** (um por cenario, cada um com `fato_*` >= 1000 linhas e modelo estrela) em `Aula 5/datasets/cenarioN_*/`: (1) Backlog de Pericias (1200), (2) TAT do Laboratorio de DNA (1100), (3) Mapa da Criminalidade em MT (1500), (4) Orcamento e Contratos (1300 + 240 dotacao), (5) Cadeia de Custodia (1300). Gerador: `Aula 5/gerar_datasets_aula5.py` (semente fixa 20260120). Caderno `Aula 5/gerar_caderno_aula5.py` com **80 secoes** em 7 partes: Abertura, DAX avancado, Service/Seguranca/Governanca, 7 labs, 5 cenarios com datasets proprios, projeto integrador (>=3 abas) e fechamento. |
| Aula 6 — Gestao de Projetos (BPMN/Mermaid) | Criados **3 datasets de processo** em `Aula 6/datasets/cenarioN_*/`, todos com o mesmo schema (`fato_execucao` = 1 execucao de etapa, com `tempo_espera_min` e `tempo_execucao_min` separados) e **30.733 execucoes no total**: (1) Requisicao Pericial (10.352, gargalo = fila do perito, 41,5% da espera), (2) Empenho e Contrato (9.541, gargalo = parecer + autorizacao, 51,2%), (3) Cadeia de Custodia (10.840, gargalo = guarda, 35,3%). Gerador: `Aula 6/gerar_datasets_aula6.py` (semente fixa 20260610). Caderno `Aula 6/gerar_caderno_aula6.py` com **67 secoes** em 8 partes: Abertura, fundamentos de projeto, BPMN + Mermaid (14 blocos mermaid prontos), metodo das 7 perguntas (texto → diagrama), gargalos com dados (Pareto, Little's Law, retrabalho), TO-BE + intervencao digital, 7 labs, 3 cenarios modelados ponta a ponta (AS-IS → gargalo → TO-BE → ganho) e fechamento. |
| Aula 6 — novo formato (dois turnos) | Reestruturada para o formato **manha de BI / tarde de gestao de projetos**: **5 datasets** (requisicao pericial, empenho e contrato, cadeia de custodia, local de crime, analise laboratorial), **57.293 execucoes**, cada um empacotado em um **workbook `.xlsx`** com 9 abas (`LEIA-ME` + fato + 7 dims) e formatacao de sala. Caderno com **80 secoes em 10 partes**: fundamentos do painel (8 medidas DAX, 5 visuais), **5 receitas de painel** (72 passos cada, em 8 blocos: Excel -> importacao -> Power Query -> modelo -> medidas -> cartoes/graficos/Pareto/linha/matriz/filtros/tabela resumo -> formatacao e publicacao), analise (espera x execucao, Pareto, Little's Law), fundamentos de projeto, BPMN/Mermaid, TO-BE, 8 labs (4+4), 3 cenarios modelados e fechamento. Gerador de Excel: `Aula 6/gerar_excel_aula6.py`. |

| Refinaria visual (Aula 6) | Criada `caderno_svg.py` (na raiz): biblioteca SVG com **34 icones** da notacao BPMN 2.0 (geometria oficial OMG — eventos inicio/intermediario/fim, atividades, 3 gateways, swimlanes, objetos, mensagens), ilustrações pre-prontas (galeria de simbolos, anatomia de swimlane, comparacao dos 3 gateways, espera x execucao, anatomia da automacao, cadeia do metodo) e **diagramas de processo completos** (build_process_asis/_tobe/_orcamento/_custodia). CSS em `caderno_lib.py` adicionado para `.svgfig`. Os diagramas usam `var(--ink)`, `var(--accent)`, `var(--verde)` etc., entao adaptam ao tema claro, escuro e a impressao sem CSS extra.

| Aula 6 — reescrita em pt-BR | Todo o caderno do Dia 6 (abertura, 10 partes, 80 secoes) foi **reescrito em portugues do Brasil com acentuacao completa**, sem adjetivacoes e sem travessoes, com **conectivos** ligando as frases depois do ponto final (" alem disso", " por isso", " dessa forma", " nesse sentido", " com isso", " em seguida", " por fim"). Criada a ferramenta `ptbr.py` (raiz), que aplica a acentuacao nos nos de texto do HTML sem tocar em codigo, tags, SVG ou blocos Mermaid/DAX/SQL, com o dicionario `ptbr_dict.json` (403 entradas). O gerador chama `ptbr.acentuar_arquivo(...)` no final do build. Corrigido o quiz do fechamento, em que a pergunta sobre o grao da fato estava com as alternativas do stateDiagram. |

| Aula 6 — receitas detalhadas | A funcao `receita()` do gerador passou a produzir **72 passos em 8 blocos** por dataset (antes eram 19): (1) preparar o arquivo no Excel, (2) importar os dados no Power BI, (3) tratar no Power Query, (4) montar o modelo, (5) criar as medidas, (6) montar o painel, (7) filtros, segmentacoes e tabela resumo, (8) formatar, salvar e publicar. Cada passo indica o caminho do menu, o campo ou a opcao e o que esperar na tela. Acrescentadas as medidas do Pareto (`Rank da Etapa`, `% Acumulado da Espera` e `Espera por Etapa`) e as instrucoes de eixo secundario, escala, interacoes entre visuais, formatação condicional da matriz, marcacao da tabela de datas e publicacao no Service. |

| Aula 6 — integridade dos datasets | Corrigidos tres defeitos que quebravam a analise e os labs: (1) **chaves de etapa desalinhadas** — `dim_etapa.etapa_key` usava `i+1` enquanto a fato usava a chave alfabetica de `dim()`, o que fazia o join errado (a etapa 41,5% aparecia com o nome errado); (2) **cabecalhos incompletos** em `dim_unidade` (faltava `tipo`) e `dim_projeto` (faltava `escopo`); (3) **colunas renomeadas** para o que realmente significam — `tempo_total_min` passou a `tempo_total_h` (o valor esta em horas) e `custo_minuto` passou a `custo_execucao_rs` (e o custo da execucao em R$). O campo `unidade_padrao` da `dim_etapa`, que antes repetia a espera mediana da etapa, passou a trazer o nome da unidade. Semente fixa `20260610` mantida, entao os valores nao mudaram. |

| Aula 6 — publicacao no GitHub Pages | Commit `3516501` na branch `main` do repositorio `renato0503/Aula_politec`, com o caderno reescrito em pt-BR, as 5 receitas com 72 passos, os 5 workbooks `.xlsx` e a documentacao atualizada. O site `https://renato0503.github.io/Aula_politec/` passou a servir o card novo da Aula 6, o caderno com 80 secoes e os workbooks para download (verificado com HTTP 200). O `index.html` da raiz foi atualizado com o tema, os numeros e o rodape do curso. |

| Aula 6 — PDF do caderno | Gerado `Aula 6/Caderno Dia 6 - POLITEC.pdf` com **121 paginas** e 80 secoes no sumario paginado, em 2 passadas (`python exportar_pdf.py 6`). O PDF acompanha o HTML no site, junto dos workbooks. |

| Aula 7 — gargalo medido, automacao e Antigravity | Criados **5 datasets novos** em `Aula 7/datasets/cenarioN_*/`, com o mesmo schema da Aula 6 (`fato_execucao` = 1 execucao de etapa) e **58.408 execucoes** no total: (1) Apreensao e pericia de armas (11.312, gargalo = prova de fogo, 40,3%), (2) Sinistro de transito (11.336, gargalo = documentos, 35,7%), (3) Credenciamento de peritos (10.152, gargalo = curriculo, 31,3%), (4) Etilometria (12.176, gargalo = auto de infracao, 28,9%), (5) Atendimento e ouvidoria (13.432, gargalo = instrucao, 35,5%). A espera ocupa 92,1% a 97,2% do tempo dos cinco processos. Geradores: `Aula 7/gerar_datasets_aula7.py` (semente fixa 20261027) e `Aula 7/gerar_excel_aula7.py`. Caderno `Aula 7/gerar_caderno_aula7.py` com **68 secoes em 12 partes**: Abertura, 5 cenarios (cada um com 4 secoes: contexto medido, receita de 8 blocos e 96 passos, as 11 medidas DAX e a leitura do painel), analise comparada dos 5 gargalos, gargalo x automacao e digitalizacao (catalogo de 10 intervencoes, matriz, ganho, business case, roadmap), proposta de solucao com TO-BE em Mermaid para cada cenario, **aulão de Antigravity** (11 secoes, botao por botao), **GitHub conectado pelo navegador** (comandos `gh`), 8 labs e fechamento. PDF com **135 paginas** (`python exportar_pdf.py 7`). |

| Aula 8 — fase de ideacao e prototipacao (Firestore, plano Spark) | Criada a pasta `Aula 8/` com o material da fase: `formulario-ideacao.html` (formulario em **14 blocos**: identificacao, problema, **AS-IS** com tabela de etapas — quem faz, o que entra, acao, o que sai, sistema, regra, onde espera, tempo, automatizavel —, **papeis** com o que cada um ve e faz, **TO-BE** com a tabela de etapas futuras (maquina, pessoa assistida ou pessoa), **escopo e MVP minimo** (o que faz e o que nao faz, telas com rota `#/painel`, criterio de aceite, dados de exemplo), **entidades e colunas**, **regras de negocio RN01**, **LGPD**, **stack**, **fontes de dados**, **KPIs** com linha de base e valor esperado, **hospedagem** (opcoes, custo, quem mantem, limitacao), pesquisa de apoio com fontes, marcos e riscos, defesa e **upload de documentos**), `index.html` (o **hub**: um cartao por projeto, busca, filtros, indicadores de completude e CSV), `app.html` (pagina do projeto com 15 secoes, download dos arquivos e **prompts de Mermaid** preenchidos), `prompt-bpmn-mermaid.md` (o papel (role) de Mermaid/BPMN com as convencoes e os tres comandos: AS-IS, TO-BE e TO-BE com automacao), `firestore.rules`, `firebase-config.js` (fallback de versao do SDK), `formulario-ideacao.md` e `template-metricas.md`. O formulario **exporta o `PROJETO.md`** nas 9 secoes (problema, objetivo do MVP, papeis, dados, regras, telas, KPIs, stack, restricoes e LGPD) com os anexos A a E, **importa o `.md` e o `.json`** para continuar de onde parou, e em todas as **12 tabelas** oferece **copiar modelo, copiar tabela e colar tudo de uma vez** (TAB do Excel, ponto e virgula, dois espacos ou tabela Markdown), com distribuicao por nome de coluna. O envio valida: nao envia formulario vazio, avisa as pendencias antes de enviar e oferece **envio por e-mail** quando o Firebase esta bloqueado. Projeto no **plano Spark**: so Firestore, sem Storage; cada arquivo vira um documento na colecao `ideacao_arquivos`, em base64, com limite de 600 KB. Publicado no GitHub Pages (`https://renato0503.github.io/Aula_politec/Aula%208/formulario-ideacao.html` para o aluno e `/Aula%208/` para o professor) e no Firebase Hosting (`https://aulapolitec.web.app/Aula%208/`). O `index.html` da raiz ganhou o card da fase. |

| Aula 8 — apps dos grupos (20 projetos) | Processadas as entregas do formulario da Aula 8 em `Apps/<slug>/`: **20 apps**, cada um com `README.md`, `PROJETO.md`, `contexto.md`, `sprint.md`, `projeto.json`, `envio-original.json`, `app.json`, `src/` e `exemplos/`. Os 12 primeiros chegaram aos Sprints 1, 2 e 3; os 8 novos (`custodia-definitiva`, `passivo-ambiental`, `renovacao-contratos-horus`, `documentapolitec`, `gestao-documentos`, `controle-aquisicoes`, `distribuicao-casos-dna`, `trilha-custodia-necropsia`) chegaram aos Sprints 1 e 2. Criada a base comum `Apps/_base/` (`base.html`, `construir.py`, `embutir.py`, `js_comum.js`, `testar.py`, `testar_sprints.py`, `equipes.py`, `equipes.json`) e os cenarios `_base/cenarios/sprint2.py` e `sprint3.py`. Cada app e um `index.html` gerado, offline first, com IndexedDB, backup `.json`, perfis, dados ficticios com semente fixa e a tela `#/testes`; a excecao e `agendamento-cin` (Google Apps Script). Registrados os logins do GitHub em `Apps/equipes.json`, com a tabela "Equipes e GitHub" gerada por `_base/equipes.py`. |


| Apps — identidade visual e Sprint 3 (30/10/2026) | Criada a identidade visual comum SESP/MT e POLITEC/MT (`Apps/_base/visual.css` e `icones.js`): faixa do governo, cabecalho institucional com emblema, filete acento/dourado/verde, menu com icones, cartoes, KPIs, tabelas, selos e rodape. Cada app ganhou o bloco `visual` no `app.json` (acento, emblema, layout, padrao, estilo e setor). Tema claro como padrao em todos os apps, botoes de tamanho da fonte (80% a 150%) e faixa de aviso de prototipo removida. Registro para continuar em outro agente: `Apps/CONTINUAR.md`; mídia kit: `Apps/IDENTIDADE-VISUAL.md`. |
| Apps — Sprint 3 dos 6 apps novos (30/10/2026) | Feito o Sprint 3 de `passivo-ambiental` (editor de mapa com modelos e elementos obrigatorios, anexo ao laudo e versao para impressao em `#/pdf/:id`, RN02 e RN03), `renovacao-contratos-horus` (checklist de instrucao R7, repositorio local de documentos com visibilidade restrita a gestao R8 e aviso de contrato sem instrucao a 60 dias, com a tela `#/instrucao`), `documentapolitec` (importacao da planilha de 850 prontuarios com associacao de colunas em `#/importar`, comparacao com o indice do arquivo digital e relatorio de aceitas, recusadas e divergentes em `#/relatorio-importacao`; exemplos em `exemplos/gerar_planilhas.py`), `gestao-documentos` (minutas padronizadas com os dados do processo RN04, emissao de oficio e despacho e checklist de instrucao por etapa), `controle-aquisicoes` (pesquisa de precos com tres cotacoes e memoria de calculo RN04, alerta de inconsistencia entre estimado e cotado com tolerancia de 30% e historico de precos por objeto em `#/precos`) e `distribuicao-casos-dna` (sugestao do proximo perito pelo historico de rotacao, fila de urgencia com justificativa RN05 e alerta de rodada parada). Codigo em `src/sprint3.js` de cada app, cenarios em `Apps/_base/cenarios/sprint3.py`. Os 20 apps passam em `testar.py` e os 42 cenarios passam em `testar_sprints.py`. |

| Apps — elucubração dos 77 itens do Sprint 0 (30/10/2026) | Os itens do Sprint 0 que dependiam de decisao institucional, documento oficial ou medicao do processo real foram fechados com **premissas**: cada um tem um valor plausivel assumido, o lugar onde ele aparece no app, o **nivel de confianca (A, B ou C)** e o que precisa ser confirmado. Tudo em `Apps/PREMISSAS.md`. As referencias que faltavam foram criadas: modelos de DFD/ETP/TR/risco (`controle-aquisicoes/modelos/`), atas da comissao de etica (`comissao-etica-denuncias/modelos/`), modelo do TAP (`tap-portfolio-projetos/modelos/`), modelo do laudo ambiental (`passivo-ambiental/modelos/`), modelo da caixa (`documentapolitec/modelos/`), marcos e livros da TCIN (`trilha-custodia-necropsia/modelos/`), categorias e conservacao da custodia (`custodia-definitiva/modelos/`), tabela AS-IS (`adiantamento/modelos/`), WorkFlow (`mapa-distribuicao-credor/modelos/`), regras de CIN (`cin-segunda-via/modelos/`), regras do RNC (`rnc-nao-conformidade/modelos/`), importacao do BI (`metas-bi-ocr/modelos/`), formulario e linha de base (`inscricoes-cursos/modelos/`), papel e anexos (`gestao-documentos/modelos/`), semaforo e permissoes (`renovacao-contratos-horus/modelos/`), rotacao e naturezas (`distribuicao-casos-dna/modelos/`), relatorio e print (`horus-banco-demandas/modelos/`) e o **esquema SQL do Hórus** (`horus-banco-demandas/horus/esquema.sql`) com o formato `horus-import-ciclo.json`. O codigo mudou em 3 apps: `adiantamento` (feriados de MT e do municipio, com `escopo`, e 2 testes novos), `distribuicao-casos-dna` (natureza de exame no caso e na tabela) e `documentapolitec` (planilha de 850 prontuarios e indice do arquivo digital, com o relatorio de aceitas, recusadas e divergentes). Os itens do Sprint 0 nos 20 `sprint.md` continuam **pendentes de confirmacao**, mas com a premissa anotada. |

| Apps — base legal real na Comissão de Ética e nas Aquisições (30/10/2026) | Duas premissas deixaram de ser elucubração porque a norma foi consultada no acervo `ctresb/leis` (fonte oficial indicada no cabeçalho de cada norma). **Comissão de Ética**: as 8 categorias passaram a citar o artigo e o trecho real do **Código de Ética Funcional do Servidor Público Civil do Estado de Mato Grosso (LC nº 112/2002-MT)** — art. 2º (X, XI, XII, XIV, VI, VII), art. 4º (V, VI, VII, IX, XI) e art. 5º (I, VI, VII, XI, XII) —, com o texto guardado em `comissao-etica-denuncias/modelos/codigo-etica-lc112-2002.md` e editavel em `#/config`; a tela de classificação mostra o texto do artigo e a fonte, e o prompt da IA cita a lei. **Aquisições**: o fluxo de 9 etapas foi ancorado na **Lei nº 14.133/2021** (art. 18, I, II, X e § 1º com os 13 elementos do ETP; art. 23, § 1º, IV para as 3 cotações; art. 53 para o parecer jurídico; art. 55 para os prazos de divulgação), com prazo por etapa (`CA_PRAZO_ETAPA`, 43 dias de ciclo) e a base legal visível na ficha do processo. O detalhamento está em `controle-aquisicoes/modelos/fluxo-e-prazos.md`. O que continua sendo elucubração são os prazos em dias e a divisão em etapas, porque a lei não fixa esses números para o fluxo interno da POLITEC. |

| Apps — sprints finais dos 20 apps (30/10/2026) | Continuidade do desenvolvimento, app por app, na ordem das sprints. Ficaram com o **MVP completo (17 de 20)**: adiantamento (S1-7), segunda via da CIN (S1-6), comissao de etica (S1-7), metas BI (S1-6, exceto OCR de PDF em imagem), RNC (S1-6), TAP (S1-6), agendamento CIN (S1-8, com LockService/MailApp/gatilho como a implementar), controle de aquisicoes (S1-7), custodia definitiva (S1-7), distribuicao de casos de DNA (S1-7), documentapolitec (S1-7, com QR Code a implementar), gestao de documentos (S1-7), passivo ambiental (S1-7), renovacao de contratos (S1-7), trilha de custodia (S1-7) e Horus banco de demandas (S1-8). Cada app ganhou `modelos/roteiro-aceite.md`, o cenario em `Apps/_base/cenarios/sprint4.py` e o `sprint.md` marcado. Criado o **botao escondido de ajuda tecnica** (tres cliques no nome do app, no rodape) que abre o passo a passo do que depende de servico externo. Faltam 22 rotas em 4 apps: mapa de distribuicao a credores (S4-S8), inscricoes em cursos (S4-S9), equipamentos no Google Earth (S4-S11) e agiliza mais (S4-S13). Estado detalhado em `Apps/CONTINUAR.md`. |

---

*Padrao herdado do curso SESP/MT (ver `D:\Dev\Aula Sesp\skills\`). Motor do caderno:
`caderno_lib.py`.*
