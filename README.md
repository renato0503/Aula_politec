# Capacitacao POLITEC/MT — Analise de Dados aplicada a Pericia Criminal

Material do curso ministrado pelo **Professor Renato Rosa** para a **POLITEC/MT**
(Pericia Oficial e Identificacao Tecnica de Mato Grosso). O repositorio organiza
**uma aula = uma pasta `Aula N/`**, cada uma com caderno vivo (HTML), PDF, slides e
materiais de pratica.

> O contrato do repositorio (padrao, convencoes e passo a passo) esta em
> **[`AGENTS.md`](./AGENTS.md)**. Este README e o indice de navegacao do curso.

---

## Aulas disponiveis

| Aula | Tema | Seções | Slides | Caderno HTML | PDF |
|---|---|---|---|---|---|
| [1](Aula%201/) | Fundamentos da Analise + Estatistica | 61 | 5,2 MB | [161 KB](Aula%201/caderno-dia1.html) | 53 pág · 4,9 MB |
| [2](Aula%202/) | Planilhas / Excel e Google Sheets | 69 | 4,4 MB | [207 KB](Aula%202/caderno-dia2.html) | 71 pág · 4,6 MB |
| [3](Aula%203/) | Organizacao, Visualizacao e ETL | 64 | 4,0 MB | [144 KB](Aula%203/caderno-dia3.html) | 48 pág · 4,2 MB |
| [4](Aula%204/) | Business Intelligence / Power BI | 107 | 6,3 MB | [227 KB](Aula%204/caderno-dia4.html) | PDF a regerar |
| [5](Aula%205/) | Dashboards de BI - 5 cenarios com datasets proprios | 80 | — | [140 KB](Aula%205/caderno-dia5.html) | PDF opcional |
| [6](Aula%206/) | Painel de Processo (manha) + Gestao de Projetos (tarde) | 80 | — | [417 KB](Aula%206/caderno-dia6.html) | PDF opcional |

Cada pasta `Aula N/` contem: `README.md` (indice da aula), `caderno-diaN.html`
(fonte viva), `Caderno Dia N - POLITEC.pdf`, `Dia-N-Politec.pdf` (slides) e
`gerar_caderno_aulaN.py` (gerador de conteudo). A Aula 6 acrescenta
`gerar_datasets_aula6.py` (5 datasets de processo), `gerar_excel_aula6.py`
(5 workbooks `.xlsx` com todas as tabelas em abas) e a pasta `datasets/` com
os 5 cenarios.

---

## O que e o caderno

O **caderno** e o material de **aprofundamento** do aluno — complementa, nao
substitui, os slides. Ele traz:

- **Formato em dois turnos** (a partir da Aula 6): a **manha** e de paineis, BI
  e analise de dados; a **tarde** e de hands-on em gestao de projetos e mini
  apps. O caderno se organiza em **6 a 10 partes** conforme a aula (a Aula 6
  usa 10: fundamentos do painel, 5 receitas por dataset, analise, projeto,
  BPMN/Mermaid, TO-BE, labs, cenarios e fechamento).
- **Passo a passo** de cliques/atalhos/contas (`step`) em toda secao pratica.
- **Exemplos e aplicacoes na POLITEC** (`aplicab`: QUANDO / POR QUE / EXEMPLO).
- **Labs** (6-8 por aula) e **cenarios reais** (3-4 por aula).
- **Quiz** com gabarito expansivel, glossario e referencias.
- **Recursos**: tema claro/escuro, indice lateral com busca, botao Imprimir/PDF,
  blocos de codigo com botao Copiar. Um arquivo HTML autossuficiente — abre com
  duplo clique, offline.

---

## Novidades da Aula 6 (formato novo do curso)

A partir da Aula 6, o curso opera em **dois turnos** e o caderno da aula foi
reescrito do zero em **portugues do Brasil**:

- **Manha (08h-12h)**: paineis, BI e analise de dados. O aluno abre o workbook
  do dataset, importa no Power BI, modela o relaciomanto, cria as medidas e
  monta o painel (cartoes, graficos, Pareto, linha do tempo, matriz, filtros,
  segmentacoes e tabela resumo).
- **Tarde (13h-17h)**: hands-on de gestao de projetos, BPMN/Mermaid, AS-IS,
  TO-BE, calculo do ganho e canvas do mini app. Nas aulas seguintes, a tarde
  vira ideacao e prototipacao de mini apps com IA agentica.

Entregas da Aula 6:

- **5 datasets de processo** (57.293 execucoes medidas), cada um em um
  **workbook `.xlsx` com 9 abas** (`LEIA-ME` + `fato_execucao` + 7 `dim_*`).
- **5 receitas de painel** no caderno, uma por dataset, com 19 passos cada.
- **8 labs** (4 de painel pela manha + 4 de processo e mini app pela tarde).
- **80 secoes em 10 partes**, com quiz, glossario e referencias.
- Novo padrao de idioma: acentuacao completa, sem adjetivacoes, sem
  travessoes e com conectivos depois do ponto final (aplicado por `ptbr.py`).

---

## Estrutura do repositorio

```
Aula Politec/
├── README.md              ← este indice
├── AGENTS.md              ← contrato do repositorio (padrao dos cadernos)
├── caderno_lib.py         ← motor compartilhado (CSS + helpers + classe Caderno)
├── caderno_svg.py         ← biblioteca SVG (icones BPMN 2.0 e diagramas de processo)
├── ptbr.py                ← acentuacao pt-BR do HTML gerado
├── ptbr_dict.json         ← dicionario de acentuacao (403 entradas)
├── exportar_pdf.py        ← exporta caderno-diaN.html -> "Caderno Dia N - POLITEC.pdf"
├── validar.py             ← checa secoes x TOC x h2, tema, erros de console
├── gerar_datasets_estrela.py ← monta o modelo estrela (fato_*/dim_*) nas Aulas 2, 3 e 4
├── Aula 1/ … Aula 6/      ← uma pasta por aula
```

---

## Como usar

**So ler** — abra o `caderno-diaN.html` da aula no navegador (ou o PDF).

**Editar/regerar um caderno**

```powershell
python "Aula N\gerar_caderno_aulaN.py"   # gera o HTML
python validar.py N                       # precisa imprimir OK
python exportar_pdf.py N                  # gera o PDF (opcional)
```

Requisitos das ferramentas: `pip install playwright pymupdf` e
`playwright install chromium` (so para o PDF).

**Regerar os datasets da Aula 6** (na ordem)

```powershell
python "Aula 6\gerar_datasets_aula6.py"   # 5 datasets (CSVs + READMEs)
python "Aula 6\gerar_excel_aula6.py"      # 5 workbooks .xlsx (uma aba por tabela)
python "Aula 6\gerar_caderno_aula6.py"    # caderno (ja aplica a acentuacao pt-BR)
python validar.py 6
```

**Criar uma nova aula** — siga `AGENTS.md` > "Como criar uma nova aula".

---

## Convencoes rapidas

- Nomes: `Dia-N-Politec.pdf`, `caderno-diaN.html`, `Caderno Dia N - POLITEC.pdf`,
  `gerar_caderno_aulaN.py` (sem zero a esquerda).
- Texto em portugues **sem acentos** (padrao das Aulas 1 a 5). **A partir da
  Aula 6**, o padrao e portugues do Brasil **com acentuacao completa**, sem
  adjetivacoes, sem travessoes e com conectivos ligando as frases depois do
  ponto final.
- HTML sem dependencia externa; tema claro/escuro; UTF-8.
- Numeros sempre com fonte (slide ou dataset).

---

## Pendencias / proximos passos

1. **PDF fiel ao HTML** — o `@media print` atual comprime as secoes; falta um
   layout de impressao dedicado (capa, quebras por parte). O HTML e a fonte de verdade.
2. **Datasets** — arquivos sinteticos (`datasets/`) para os labs de Excel/Power BI.
3. **PDFs das Aulas 5 e 6** — opcional; rodar `python exportar_pdf.py 5` e `python exportar_pdf.py 6`.
4. **Aulas 7+** — proxima fase: manha de BI e tarde de ideacao/prototipacao de mini apps com IA agentica (Antigravity). A tarde da Aula 6 ja deixa o **canvas do mini app** pronto (problema, usuario, dado, acao e medida), que e o ponto de partida do prototipo.
5. **Ampliar o dicionario pt-BR** — ao escrever palavras novas no gerador, incluir a entrada em `ptbr_dict.json` para que a acentuacao continue correta.

---

*Padrao herdado do curso SESP/MT. Motor do caderno: [`caderno_lib.py`](./caderno_lib.py).*
