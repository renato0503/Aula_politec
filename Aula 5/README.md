# Aula 5 — Dashboards de BI - 5 cenarios com datasets proprios

**Modulo 7 (encerramento da capacitacao)** — DAX avancado, governanca
corporativa, RLS/OLS, Power Platform e um **projeto integrador** com cinco
cenarios tematicos, cada um com seu dataset proprio em modelo estrela
(mais de 1000 linhas cada). O aluno escolhe **pelo menos tres** e constroi o
painel final institucional da POLITEC/MT.

Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 5.

---

## Conteudo do caderno (80 secoes em 7 partes)

| Parte | Conteudo |
|---|---|
| Abertura | Boas-vindas, mapa do Dia 5, recap do curso (D1-D4) e objetivo do dia |
| **1 — DAX avancado (Modulo 7 - manha)** | Recap DAX, medida x coluna calculada, contexto de linha, contexto de filtro, **CALCULATE**, iteradores (SUMX/AVERAGEX), **DIVIDE**, COUNTROWS/DISTINCTCOUNT, **ALL/REMOVEFILTERS/KEEPFILTERS**, FILTER, time intelligence (YTD/QTD/MoM/YoY, 7 funcoes-chave), variaveis (VAR), padroes DAX uteis, performance DAX, arvore de decisao |
| **2 — Service, Seguranca e Governanca (Modulo 7 - tarde)** | Service recap, **Dataflows**, datasets compartilhados, **RLS (Row-Level Security)**, **OLS (Object-Level Security)**, RLS x OLS, Apps avancado, **Deployment Pipelines**, Data Gateway avancado, **Power Platform** (Power Apps, Automate, Virtual Agents, Pages), **Microsoft Fabric** (introducao), BI x LGPD (recap), BI institucional sustentavel |
| **3 — Pratica guiada** | 7 laboratorios: importar datasets, relacionamentos/cardinalidade, tabela de medidas (DAX basicas), time intelligence, KPI com formatacao condicional, **RLS** (Desktop + Service), publicar e distribuir via App |
| **4 — 5 Cenarios com datasets proprios** | Cenario 1 — Backlog de Pericias (1200 linhas); Cenario 2 — TAT do Laboratorio de DNA (1100); Cenario 3 — Mapa da Criminalidade em MT (1500); Cenario 4 — Orcamento e Contratos (1300 + 240 dotacao); Cenario 5 — Cadeia de Custodia de Evidencias (1300). Para cada cenario: necessidade, dataset, visuais sugeridos, medidas DAX, caso real. Como juntar diferentes cenarios no mesmo .pbix |
| **5 — Projeto Integrador** | Objetivo, requisitos minimos (3+ abas), guia para escolher as 3 abas (por publico-alvo), plano de 1 pagina do painel, **RLS recomendada**, checklist de entrega, rubrica de avaliacao |
| **6 — Fechamento** | Ecossistema Microsoft (camadas), 10 erros que todo perito cai, checklist de publicacao v2, proximos passos, 3 casos extras (Power Automate + Embedded + Fabric), quiz (15), glossario, referencias, agradecimentos |

---

## Laboratorios praticos (Parte 3)

| Lab | Titulo | O que constroi |
|---|---|---|
| 1 | Importar 2 ou 3 datasets com Obter Dados -> Pasta | Modelo de dados inicial |
| 2 | Relacionamentos e cardinalidade | Modelo estrela com N:1 |
| 3 | Tabela de medidas (DAX basicas) | Tabela central de medidas |
| 4 | Time intelligence (YTD, MoM, YoY) | Comparacoes temporais |
| 5 | KPIs com formatacao condicional | Cartoes verdes/amarelos/vermelhos |
| 6 | RLS - teste no Desktop e Service | Funcoes de seguranca por papel |
| 7 | Publicar e distribuir via App | Workspace + App |

---

## Cenarios com datasets proprios (Parte 4)

Todos os datasets estao em `Aula 5/datasets/cenarioN_<tema>/` em formato
modelo estrela (CSV UTF-8 com BOM, separador `;`).

| # | Cenario | Pasta | Tema | Fato | Linhas |
|---|---|---|---|---|---|
| 1 | Backlog de Pericias | `cenario1_backlog/` | Operacional (fila, TAT) | `fato_requisicoes` | **1.200** |
| 2 | TAT do Laboratorio de DNA | `cenario2_dna/` | Laboratorio (qualidade, TAT) | `fato_exames_dna` | **1.100** |
| 3 | Mapa da Criminalidade em MT | `cenario3_criminalidade/` | Inteligencia geografica | `fato_ocorrencias` | **1.500** |
| 4 | Orcamento e Contratos | `cenario4_orcamento/` | Financeiro | `fato_empenhos` + `fato_dotacao` | **1.300 + 240** |
| 5 | Cadeia de Custodia de Evidencias | `cenario5_custodia/` | Rastreabilidade processual | `fato_mov_evidencia` | **1.300** |

Cada pasta traz o proprio `README.md` com o esquema estrela, numeros de
referencia e **sugestoes de visuais** para a aba tematica correspondente.

---

## Como abrir

1. **Caderno vivo** — abra `caderno-dia5.html` no navegador.
2. **Datasets** — va direto em `datasets/cenarioN_*/`. O `README.md` da
   pasta explica o esquema estrela e os visuais sugeridos.
3. **Regerar o caderno** — `python gerar_caderno_aula5.py`.
4. **Regerar os datasets** (semente fixa = `20260120`) —
   `python gerar_datasets_aula5.py`.
5. **PDF** (opcional) — `python ..\exportar_pdf.py 5`.

---

## Projeto Integrador (Parte 5)

O entregavel do dia e o **Painel Final da POLITEC**: um arquivo
`Projeto_Integrador.pbix` com **>= 3 abas tematicas**, cada uma vinda de um
cenario.

**Requisitos minimos** (rubrica):

- 3+ abas tematicas (cada uma de um cenario diferente);
- 1 slicer por aba (periodo + atributo do cenario);
- 1 KPI com formatacao condicional por aba;
- 1 visual **temporal OU geografico** por aba;
- **RLS ativa** em ao menos 1 aba;
- Publicacao em **workspace segregado** + App com link.

**Guia de escolha das 3 abas por publico-alvo** (ver Parte 5 do caderno):

| Publico-alvo | Aba 1 | Aba 2 | Aba 3 |
|---|---|---|---|
| Diretor Tecnico | Backlog | DNA | Custodia |
| Diretor Financeiro | Orcamento | DNA | Backlog |
| Diretor de Inteligencia | Mapa Criminal | Backlog | Custodia |
| Chefe de Laboratorio DNA | DNA | Custodia | Orcamento |
| Chefe do IML | Criminalidade | Custodia | Backlog |

---

## Estatisticas

| Arquivo | Tamanho |
|---|---|
| `caderno-dia5.html` (fonte viva, tema claro/escuro) | 139 KB |
| `gerar_caderno_aula5.py` (gerador de conteudo) | ~85 KB |
| `gerar_datasets_aula5.py` (gerador dos 5 datasets) | ~33 KB |

| Metrica | Valor |
|---|---|
| Secoes no caderno | 80 |
| Partes (grupos) | 7 |
| Cenarios com datasets proprios | 5 (+1 intro) |
| Total de linhas nos fatos | 5.400 (1200 + 1100 + 1500 + 1300 + 1300) |
| Laboratorios praticos | 7 |
| Tabelas CSV no total | 51 (10 fatos e 41 dimensoes) |
| Perguntas de quiz | 15 |
| Itens do glossario | 20 |
| Blocos QUANDO / POR QUE / EXEMPLO (`aplicab`) | 10+ |
| Medidas DAX exemplo | 30+ |

---

## Convencoes dos datasets

- CSV UTF-8 com BOM, separador `;`, datas ISO `AAAA-MM-DD`.
- `data_key` inteiro no formato `AAAAMMDD` (ex.: 20250304).
- Chaves substitutas inteiras 1..N atribuidas por ordem alfabetica.
- `dim_calendario` cobre 2023-01-01 a 2025-12-31 (1096 dias, 3 anos).
- Os mesmos 8 setores e 16-18 municipios MT aparecem em varios cenarios
  (catalogo compartilhado).

---

*Material gerado via `gerar_caderno_aula5.py`, usando o motor `../caderno_lib.py`
(ver `../AGENTS.md`).*
