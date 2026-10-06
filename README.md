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
| [2](Aula%202/) | Planilhas / Excel e Google Sheets | 68 | 4,5 MB | [174 KB](Aula%202/caderno-dia2.html) | 60 pág · 3,8 MB |
| [3](Aula%203/) | Organizacao, Visualizacao e ETL | 63 | 4,0 MB | [138 KB](Aula%203/caderno-dia3.html) | 47 pág · 4,2 MB |
| [4](Aula%204/) | Business Intelligence / Power BI | 71 | 6,3 MB | [155 KB](Aula%204/caderno-dia4.html) | 55 pág · 4,9 MB |

Cada pasta `Aula N/` contem: `README.md` (indice da aula), `caderno-diaN.html`
(fonte viva), `Caderno Dia N - POLITEC.pdf`, `Dia-N-Politec.pdf` (slides) e
`gerar_caderno_aulaN.py` (gerador de conteudo).

---

## O que e o caderno

O **caderno** e o material de **aprofundamento** do aluno — complementa, nao
substitui, os slides. Ele traz:

- **6 partes**: Abertura, Modulo da manha, Modulo da tarde, Pratica guiada,
  Cenarios e Fechamento (quiz + folha de cola).
- **Passo a passo** de cliques/atalhos/contas (`step`) em toda secao pratica.
- **Exemplos e aplicacoes na POLITEC** (`aplicab`: QUANDO / POR QUE / EXEMPLO).
- **Labs** (6-8 por aula) e **cenarios reais** (3-4 por aula).
- **Quiz** com gabarito expansivel, glossario e referencias.
- **Recursos**: tema claro/escuro, indice lateral com busca, botao Imprimir/PDF,
  blocos de codigo com botao Copiar. Um arquivo HTML autossuficiente — abre com
  duplo clique, offline.

---

## Estrutura do repositorio

```
Aula Politec/
├── README.md              ← este indice
├── AGENTS.md              ← contrato do repositorio (padrao dos cadernos)
├── caderno_lib.py         ← motor compartilhado (CSS + helpers + classe Caderno)
├── exportar_pdf.py        ← exporta caderno-diaN.html -> "Caderno Dia N - POLITEC.pdf"
├── validar.py             ← checa secoes x TOC x h2, tema, erros de console
├── Aula 1/ … Aula 4/      ← uma pasta por aula
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

**Criar uma nova aula** — siga `AGENTS.md` > "Como criar uma nova aula".

---

## Convencoes rapidas

- Nomes: `Dia-N-Politec.pdf`, `caderno-diaN.html`, `Caderno Dia N - POLITEC.pdf`,
  `gerar_caderno_aulaN.py` (sem zero a esquerda).
- Texto em portugues **sem acentos** (padrao das aulas).
- HTML sem dependencia externa; tema claro/escuro; UTF-8.
- Numeros sempre com fonte (slide ou dataset).

---

## Pendencias / proximos passos

1. **PDF fiel ao HTML** — o `@media print` atual comprime as secoes; falta um
   layout de impressao dedicado (capa, quebras por parte). O HTML e a fonte de verdade.
2. **Aula 5** — DAX, publicacao e projeto final (quando houver slides).
3. **Datasets** — arquivos sinteticos (`datasets/`) para os labs de Excel/Power BI.

---

*Padrao herdado do curso SESP/MT. Motor do caderno: [`caderno_lib.py`](./caderno_lib.py).*
