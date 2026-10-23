# Aula 6 — Painel de Processo (manhã) + Gestão de Projetos (tarde)

**Módulo 8** — a aula que inaugura o **novo formato do curso**: a manhã é sempre
de **painéis, BI e análise de dados**; a tarde é de **hands-on em gestão de
projetos**, com noções de mini app e IA agêntica.

A manhã pega cinco processos reais da POLITEC/MT e transforma cada um em um
**workbook Excel** com todas as tabelas em abas. O aluno abre o arquivo, importa
no Power BI, modela, cria as medidas e monta o painel — com o passo a passo nos
mínimos detalhes. A tarde usa o painel para ensinar o mínimo de gestão de
projetos, BPMN/Mermaid, AS-IS/TO-BE e um canvas de mini app.

Curso de Capacitação POLITEC/MT · Professor Renato Rosa · Dia 6.

---

## Rewritten in pt-BR (this delivery)

The whole notebook was **rewritten in Brazilian Portuguese with full
accentuation**, without subjective adjectives and without em dashes, and with
**connectives linking the sentences after the full stop** (Além disso, Por isso,
Dessa forma, Nesse sentido, Com isso, Em seguida, Por fim).

| Item | What was done |
|---|---|
| **Text** | Abertura and all 10 parts (80 sections) rewritten: no "e" in place of "é", no "esta" in place of "está", no travessões, no subjective adjectives, connectives after each full stop |
| **Tooling** | `ptbr.py` (root) applies the accentuation to the text nodes of the generated HTML, without touching code, tags, attributes, SVG or Mermaid/DAX/SQL blocks. The dictionary is `ptbr_dict.json` (403 entries) |
| **Call** | `gerar_caderno_aula6.py` calls `ptbr.acentuar_arquivo(...)` at the end of the build, so every regeneration keeps the orthography |
| **Quiz fix** | The question about the grain of `fato_execucao` had the options of the old stateDiagram question; corrected to "1 execução de etapa" |
| **Datasets** | Fixed 3 defects that broke the analysis: (1) `dim_etapa.etapa_key` did not match the key used by the fact, so the join showed the wrong stage name on the 41,5% bar; (2) missing headers in `dim_unidade` (`tipo`) and `dim_projeto` (`escopo`); (3) `tempo_total_min` renamed to `tempo_total_h` (the value is in hours) and `custo_minuto` renamed to `custo_execucao_rs` (the value is the execution cost in R$). The `unidade_padrao` field now carries the unit name instead of repeating the stage wait |
| **Recipes** | The 5 panel recipes went from 19 to **72 steps in 8 blocks** (Excel, import, Power Query, model, measures, panel, filters and summary table, format and publish), with the DAX of the Pareto (`Rank da Etapa`, `% Acumulado da Espera`, `Espera por Etapa`) and the instructions for the secondary axis, the scale, the interactions between visuals, the conditional formatting of the matrix, the date table and the publication in the Service |
| **Numbers** | The same seed (20260610) was kept, so the measured values did not change; only the schema and the labels were corrected |

> When you write a new word in the generator, add the entry to `ptbr_dict.json`
> so the accentuation stays correct.

---

## O dia em dois turnos

| Turno | Foco | Entregável |
|---|---|---|
| **Manhã (08h–12h)** | Painéis, BI e análise de dados | Um **painel de processo** no Power BI, com 8 medidas, 5 visuais, filtros e tabela resumo |
| **Tarde (13h–17h)** | Hands-on de gestão de projetos | **AS-IS + TO-BE**, ganho calculado e **canvas do mini app** |

> **Nesta primeira aula do novo formato**, a tarde fica nos fundamentos e
> noções de gestão de projetos. A prototipação do mini app com IA agêntica
> (Antigravity) começa nas próximas.

---

## Conteúdo do caderno (80 seções em 10 partes)

| Parte | Conteúdo |
|---|---|
| Abertura | Novo formato, mapa do dia, recap dos 5 dias e objetivo |
| **1 — Manhã: O painel de processo** | Por que painel (x relatório), modelo estrela, 8 medidas DAX, layout de 5 visuais, passo a passo base, leitura em 60 segundos |
| **2 — Manhã: As 5 receitas** | Um passo a passo completo por dataset: abrir o workbook, importar, modelar, medir, montar cartões, gráficos, Pareto, linha do tempo, matriz, filtros e tabela resumo |
| **3 — Manhã: Análise do processo** | Espera x execução, funil de espera, Pareto, retrabalho, Little's Law e custo da espera |
| **4 — Tarde: Fundamentos de projeto** | Projeto x operação, triângulo, ciclo de vida, stakeholders, riscos e indicadores |
| **5 — Tarde: BPMN e Mermaid** | Notação BPMN 2.0 (eventos, atividades, gateways, swimlanes), Mermaid 1–5 |
| **6 — Tarde: Do texto ao diagrama** | Método das 7 perguntas, exemplo prático, heurísticas e versionamento |
| **7 — Tarde: TO-BE e intervenção digital** | TO-BE realista, 5 princípios, catálogo de ferramentas, cálculo do ganho e roadmap |
| **8 — Tarde: Prática guiada** | 8 labs: 4 de painel (manhã) + 4 de processo e mini app (tarde) |
| **9 — Cenários POLITEC** | 3 processos modelados ponta a ponta (dos 5 datasets): AS-IS, gargalo, TO-BE e ganho |
| **10 — Fechamento** | Método resumido, erros comuns, quiz (15), glossário, referências e encerramento |

---

## Os 5 datasets da manhã

Cada dataset tem **um workbook Excel** com 9 abas: `LEIA-ME`, `fato_execucao` e
as 7 dimensões (`dim_etapa`, `dim_unidade`, `dim_sistema`,
`dim_tipo_atividade`, `dim_status_execucao`, `dim_projeto`, `dim_calendario`).
O grão da fato é **1 execução de etapa**, com espera e execução separadas.

| # | Dataset | Workbook | Execuções | Gargalo medido |
|---|---|---|---|---|
| 1 | Requisição pericial | `Cenario1_Requisicao_Pericial.xlsx` | **10.352** | Fila perito (41,5%) |
| 2 | Empenho e contrato | `Cenario2_Empenho_Contrato.xlsx` | **9.541** | Parecer + Autorização (51,2%) |
| 3 | Cadeia de custódia | `Cenario3_Cadeia_Custodia.xlsx` | **10.840** | Guarda (35,3%) |
| 4 | Local de crime | `Cenario4_Local_Crime.xlsx` | **12.664** | Deslocamento (35,2%) |
| 5 | Análise laboratorial | `Cenario5_Analise_Laboratorial.xlsx` | **13.896** | Equipamento (47,1%) |

**Total: 57.293 execuções de etapa medidas.** Os CSVs continuam em cada pasta,
como fonte e para quem preferir importar por pasta.

### Onde estão

```
Aula 6/datasets/
├── README.md
├── cenario1_processo_pericial/
│   ├── Cenario1_Requisicao_Pericial.xlsx   ← use este na aula
│   ├── fato_execucao.csv
│   ├── dim_etapa.csv … dim_calendario.csv
│   └── README.md
├── cenario2_processo_orcamento/
├── cenario3_processo_custodia/
├── cenario4_local_crime/
└── cenario5_analise_laboratorial/
```

### Como abrir no Power BI (resumo)

1. **Obter dados → Pasta de trabalho do Excel** → escolha o `.xlsx`.
2. Marque as **8 abas de dados** (não marque `LEIA-ME`).
3. No Power Query, confirme cabeçalho e tipos.
4. No Modelo, ligue cada `*_key` da fato à dimensão correspondente.
5. Marque `dim_calendario` como tabela de datas.
6. Crie as 8 medidas e monte os 5 visuais + tabela resumo.

O detalhe completo está na **Parte 2** do caderno, uma receita por dataset.

---

## As 5 receitas de painel (Parte 2)

Cada receita é autossuficiente e tem **72 passos em 8 blocos**, do arquivo do
Excel ao painel publicado:

| Bloco | O que você faz | Tempo |
|---|---|---|
| **1** | Preparar o arquivo no Excel: conferir as 9 abas, a contagem de linhas e o `LEIA-ME` | 10 min |
| **2** | Importar no Power BI: conector de pasta de trabalho, seleção das 8 abas, renomear consultas e conferir a contagem | 20 min |
| **3** | Tratar no Power Query: cabeçalho, tipos de dado, extração de ano e mês, remoção de colunas e de linhas em branco | 20 min |
| **4** | Montar o modelo: as 7 relações com cardinalidade 1:*, a direção do filtro, a tabela de datas e as chaves ocultas | 15 min |
| **5** | Criar as medidas: 8 medidas base, 3 do Pareto, 3 do cenário, formatação, pastas e teste em tabela | 25 min |
| **6** | Montar o painel: 4 cartões, barras empilhadas ordenadas por `sequencia`, Pareto com eixo secundário, linha do tempo com meta e matriz com escala de cor | 60 min |
| **7** | Filtros, segmentações e tabela resumo: 3 segmentações sincronizadas, painel de filtros, editar interações, tabela com barras de dados | 20 min |
| **8** | Formatar, salvar e publicar: página de detalhe, tema, acessibilidade, `.pbix`, Service, atualização e layout de celular | 20 min |

| Receita | Dataset | O que o painel prova |
|---|---|---|
| **1** | Requisição pericial | A fila do perito (44,2 h) é o gargalo; a análise tem mais execução |
| **2** | Empenho e contrato | Parecer + autorização somam 51,2% da espera |
| **3** | Cadeia de custódia | A guarda concentra 35,3% da espera; o lacre é um risco à parte |
| **4** | Local de crime | O deslocamento (35,2%) pesa mais que a coleta |
| **5** | Análise laboratorial | A fila está no equipamento (47,1%), não na interpretação |

Cada receita entrega: **4 cartões**, **barras empilhadas**, **Pareto**, **linha
do tempo**, **matriz de retrabalho**, **tabela resumo** e **3 segmentações**
(etapa, unidade, ano). Cada receita traz ainda as medidas DAX do Pareto
(`Rank da Etapa`, `% Acumulado da Espera` e `Espera por Etapa`), as medidas
específicas do cenário, a tabela de resultado esperado e a armadilha do dataset.

---

## Laboratórios (Parte 8)

| Turno | Lab | Título | Entregável |
|---|---|---|---|
| Manhã | 1 | Conectar o workbook e montar o modelo | Modelo estrela com 8 tabelas |
| Manhã | 2 | Criar as 8 medidas DAX | Medidas de tempo, % espera, TAT e retrabalho |
| Manhã | 3 | Montar os 5 visuais do painel | Painel com cartões, barras, Pareto, linha e matriz |
| Manhã | 4 | Ler o painel e escrever a hipótese | Hipótese de gargalo em uma frase |
| Tarde | 5 | Descrever o processo em texto | Parágrafo AS-IS (7 perguntas) |
| Tarde | 6 | Converter o texto em diagrama AS-IS | `processo-asis.mmd` |
| Tarde | 7 | Desenhar o TO-BE e calcular o ganho | `processo-tobe.mmd` + tabela antes x depois |
| Tarde | 8 | Pitch de 3 minutos + canvas do mini app | Canvas com problema, usuário, dado, ação e medida |

---

## Cenários modelados ponta a ponta (Parte 9)

Dos cinco datasets, **três** são modelados do AS-IS ao ganho:

| # | Cenário | AS-IS | Gargalo | TO-BE | Ganho |
|---|---|---|---|---|---|
| 1 | Requisição pericial | 8 etapas, 92,4% espera | Fila perito (41,5%) | Fila priorizada por prazo legal | Espera 44 h → 8 h (−82%) |
| 2 | Empenho e contrato | 7 etapas, 88,1% espera | Parecer + autorização (51,2%) | Pauta automática + alerta de dotação | Parecer 36 h → 14 h (−61%) |
| 3 | Cadeia de custódia | 8 etapas, 92,5% espera | Guarda (35,3%) | QR Code + alertas | Guarda 55 h → 18 h (−67%) |

---

## Números medidos nos 5 datasets

| Dataset | Execuções | % espera | Gargalo | TAT médio/caso | Retrabalho |
|---|---|---|---|---|---|
| Requisição pericial | 10.352 | 92,4% | Fila perito (44,2 h / 41,5%) | 497,2 h | 11,6% |
| Empenho e contrato | 9.541 | 88,1% | Parecer (35,9 h / 29,3%) + Autorização (26,8 h / 21,9%) | 757,4 h | 16,6% |
| Cadeia de custódia | 10.840 | 92,5% | Guarda (54,5 h / 35,3%) | 1.027,5 h | 4,7% |
| Local de crime | 12.664 | 86,5% | Deslocamento (22,9 h / 35,2%) | 497,0 h | 8,4% |
| Análise laboratorial | 13.896 | 88,6% | Eletroforese (27,5 h / 24,9%) + Amplificação (24,6 h / 22,2%) | 834,2 h | 6,8% |

O achado que permeia os cinco: **quase todo o tempo do processo é espera, não
trabalho** — e o gargalo quase sempre está na fila, não na etapa que mais
executa.

---

## Como regenerar

```powershell
# 1. Datasets (CSVs + READMEs por cenário)
python "Aula 6\gerar_datasets_aula6.py"

# 2. Workbooks Excel (uma aba por tabela + LEIA-ME)
python "Aula 6\gerar_excel_aula6.py"

# 3. Caderno (o gerador já aplica a acentuação pt-BR com ptbr.py)
python "Aula 6\gerar_caderno_aula6.py"

# 4. Validar
python validar.py 6

# 5. PDF (opcional)
python exportar_pdf.py 6
```

Semente fixa dos datasets: `20260610`. Os workbooks são gerados a partir dos
CSVs; se você editar um CSV, rode o gerador de Excel de novo.

Para acentuar um HTML já gerado, sem regerar o caderno:

```powershell
python -c "import ptbr; ptbr.acentuar_arquivo('Aula 6/caderno-dia6.html')"
```

---

## Estatísticas

| Arquivo | Tamanho |
|---|---|
| `caderno-dia6.html` (fonte viva, tema claro/escuro) | 417 KB |
| `gerar_caderno_aula6.py` (gerador de conteúdo) | 167 KB |
| `gerar_datasets_aula6.py` (gerador dos 5 datasets) | 43 KB |
| `gerar_excel_aula6.py` (workbooks Excel) | 13 KB |

| Métrica | Valor |
|---|---|
| Seções no caderno | 80 |
| Partes (grupos) | 10 |
| Datasets | 5 |
| Workbooks Excel (um por dataset) | 5 |
| Abas por workbook | 9 (`LEIA-ME` + fato + 7 dimensões) |
| Receitas de painel | 5 (72 passos cada, em 8 blocos) |
| Laboratórios práticos | 8 (4 manhã + 4 tarde) |
| Cenários modelados ponta a ponta | 3 |
| Execuções de etapa nos datasets | 57.293 |
| Perguntas de quiz | 15 |
| Itens do glossário | 28 |
| Entradas do dicionário de acentuação | 403 |

---

## Convenções dos datasets

- Workbook Excel com uma aba por tabela + `LEIA-ME`.
- CSV UTF-8 com BOM, separador `;`, datas ISO `AAAA-MM-DD`.
- `data_key` inteiro no formato `AAAAMMDD`.
- Chaves substitutas inteiras 1..N em ordem alfabética. A `fato_execucao` e a
  `dim_etapa` usam **a mesma chave** (`etapa_key`), então o join funciona; use
  a coluna `sequencia` da `dim_etapa` para ordenar as etapas do processo.
- `tempo_espera_min` e `tempo_execucao_min` em **minutos**;
  `tempo_total_h` em **horas**; `custo_execucao_rs` em **R$**.
- `dim_unidade` tem as colunas `unidade_key`, `unidade` e `tipo`;
  `dim_projeto` tem `projeto_key`, `projeto` e `escopo`.
- Distribuição lognormal (cauda longa), realista para tempos de processo.
- Dados sintéticos: qualquer semelhança com processos reais é coincidência.

---

*Material gerado via `gerar_caderno_aula6.py`, usando o motor `../caderno_lib.py`
(ver `../AGENTS.md`).*
