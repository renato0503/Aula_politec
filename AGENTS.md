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
| 3 | Organizacao, Visualizacao e ETL | 63 | 138 KB | 47 pág · 4,2 MB | 6 | 4 | 81 KB |
| 4 | Business Intelligence / Power BI | 71 | 155 KB | 55 pág · 4,9 MB | 7 | 3 + 4 casos | 93 KB |

Ferramentas de apoio na raiz: `caderno_lib.py` (motor), `exportar_pdf.py` (PDF em 2
passadas) e `validar.py` (checagem automatica). Slides de origem em cada `Aula N/`.

Aulas 5+ ainda nao possuem slides nem caderno neste repositorio.

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

### 3.6 Ferramentas do repositorio (na raiz)

| Arquivo | O que faz |
|---|---|
| `caderno_lib.py` | Motor compartilhado: CSS, helpers e a classe `Caderno`. |
| `exportar_pdf.py` | Exporta `caderno-diaN.html` -> `Caderno Dia N - POLITEC.pdf` (2 passadas, numero de pagina no sumario). Uso: `python exportar_pdf.py N`. |
| `validar.py` | Checa secoes x links do TOC x `h2`, links orfaos, tema escuro e erros de console. Uso: `python validar.py N` (deve imprimir `OK`). |
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
3. **Esbocar** o outline no formato expandido de **6 partes** (Abertura, Modulos,
   Pratica, Cenarios, Fechamento) — ver secao 3.5.
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
  adotado em todas as aulas. Numeros devem ter fonte (do slide ou do dataset).
- **Encoding**: Python e HTML em UTF-8; evite aspas duplas dentro de string
  delimitada por aspas duplas (use aspas simples ou `&quot;`).

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

## 8. Checklist de "pronto"

- [ ] `README.md` da aula escrito (partes + labs + cenarios + estatisticas).
- [ ] `caderno-diaN.html` abre com duplo clique; TOC e main sem sobreposicao.
- [ ] Tema escuro funciona; `meta name="description"` preenchido.
- [ ] `python validar.py N` imprime `OK` (secoes == links TOC == `h2`, sem orfaos,
      sem erro de console).
- [ ] Quiz com `<details>` (gabarito) no fim; respostas abrem no PDF.
- [ ] `Caderno Dia N - POLITEC.pdf` gerado (quando desejado).
- [ ] Tudo dentro de `Aula N/`; nada solto na raiz.

---

## 9. Historico de producao

| Etapa | O que foi feito |
|---|---|
| Fundacao | Criados `AGENTS.md`, `caderno_lib.py` (motor), `exportar_pdf.py`, `validar.py`. |
| Aulas 1 e 2 (v1) | Primeiros cadernos (32 e 37 secoes), extraidos dos slides. |
| Aulas 3 e 4 | Cadernos novos (63 e 71 secoes) seguindo o mesmo motor e formato de 6 partes. |
| Aulas 1 e 2 (v2) | Expandidos para 61 e 68 secoes: mais `step`, `aplicab`, labs e cenarios. |
| Firebase Hosting | Configurado `firebase.json` e `.firebaserc` para hospedagem em `aulapolitec.web.app`. |
| Aula 2 — Datasets | Criados 4 CSVs sinteticos em `Aula 2/datasets/`: `requisicoes_periciais.csv` (120 linhas), `movimentacao_reagentes.csv` (80), `produtividade_peritos.csv` (218), `orcamento_setores.csv` (36). Caderno atualizado com referencias aos datasets reais em todos os exemplos, labs e cenarios. |
| Hub + GitHub | `index.html` publicado no Firebase Hosting e no GitHub Pages (`aulapolitec.web.app`). Link do Google Drive adicionado ao hub. |

Melhorias pendentes:

1. **PDF fiel ao HTML** — reescrever o `@media print` em `caderno_lib.py` (capa,
   quebras por parte, tipografia de impressao) para o PDF seguir o padrao da tela.
2. **Aula 5** — quando houver slides, seguir a secao "Como criar uma nova aula".
3. **Datasets para Aulas 1, 3 e 4** — gerar CSVs sinteticos analogos aos da Aula 2.

---

*Padrao herdado do curso SESP/MT (ver `D:\Dev\Aula Sesp\skills\`). Motor do caderno:
`caderno_lib.py`.*
