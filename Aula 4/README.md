# Aula 4 — Business Intelligence na Administracao Publica

**Modulo 6** — Power BI aplicado a gestao pericial: interface, conexao de dados,
visuais essenciais, publicacao no Service, workspaces com governanca,
permissoes, atualizacao agendada e LGPD.

Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 4.

---

## Conteudo do caderno (107 secoes em 7 partes)

| Parte | Conteudo |
|---|---|
| Abertura | Boas-vindas, mapa do Dia 4, da planilha ao BI |
| **0 — Preparacao: Power BI Desktop do zero** | Guia do iniciante: instalacao, tour da interface, as 3 visoes, Obter Dados no Excel, Power Query (limpeza de cabecalho/brancos/TOTAL GERAL/duplicatas/datas em texto/moeda em texto/categorias), Editor Avancado (M) e Fechar & Aplicar, relacionamentos, cardinalidade, tabela de datas, formatacao de campos, medidas DAX, colunas calculadas, hierarquias, catalogo de 12 visuais, formatacao e temas, interacoes/slicers, drill down/through, formatacao condicional, botoes e bookmarks, recursos de analise, atalhos, o plano das **3 abas** do painel de orcamento e contratos (aba 1 Orcamentaria, aba 2 Setores/Rubricas, aba 3 Contratos/Fornecedores), salvamento do .pbix, checklist inicial, quiz do iniciante e referencias |
| **1 — Modulo 6 Parte 1: Interface e Primeiros Relatorios** | O que e BI (Dresner/Gartner 1989), Excel x Power BI, os 3 pilares, Ben Brumfield, interface/cockpit, os 3 modos, conexao de dados, fontes da POLITEC, Importacao x DirectQuery, caso de integracao forense (SP/CE), Cole Nussbaumer Knaflic e os 5 segundos, fluxo do dashboard, Obter Dados (modelo estrela de `datasets/`), Power Query, relacionamentos fato x dimensao, primeiro visual, visuais essenciais, mapas com Bing, slicers, caso do IML, fechamento da manha |
| **2 — Modulo 6 Parte 2: Publicacao e Governanca** | Power BI Service, Desktop x Service (licenca/Azure/LGPD), publicacao, Jorge Camoes, workspaces, segregacao, caso de reducao de 40% de incidentes, formas de compartilhamento, niveis de permissao, Apps, App "Painel do Perito", atualizacao agendada, frequencia recomendada, On-premises Data Gateway, caso em policias civis, simulacao de workspace, membros/permissoes, boas praticas de governanca |
| **3 — Pratica guiada** | 7 laboratorios: Obter Dados, Power Query, primeiro visual, cartao/linha/matriz, mapa de calor, slicers, publicar e compartilhar |
| **4 — Cenarios e Aplicacoes** | Dashboard estrategico da Diretoria, dashboard tatico do Chefe de Setor, KPIs (TAT/SLA/QL), alertas visuais, integracao com o SINESP, mapa de calor de crimes, 3 cenarios (backlog, produtividade, orcamento) |
| **5 — Fechamento** | Storytelling, erros comuns, checklist de publicacao (7 itens), BI e LGPD, ecossistema Microsoft, proximos passos, previa de DAX, recursos, exercicio final, takeaways, quiz (14), glossario, referencias |

---

## Laboratorios praticos (Parte 3)

| Lab | Titulo | O que constroi |
|---|---|---|
| 1 | Obter Dados e conferir o modelo | Importacao das tabelas `fato_*` e `dim_*` de `datasets/` e conferencia de tipos |
| 2 | Limpar a base no Power Query | Remocao de "Total Geral", correcao de tipos e padronizacao de setores |
| 3 | O primeiro visual | Grafico de colunas "Backlog Atual por Setor" |
| 4 | Cartao, linha e matriz | KPIs de contexto + tendencia + detalhe cruzado |
| 5 | O mapa de calor por municipio | Mapa Preenchido com saturacao de cor |
| 6 | Slicers | Interatividade por periodo, setor e status do laudo |
| 7 | Publicar e compartilhar | Fluxo completo com checagem de dados sensiveis e atualizacao agendada |

---

## Cenarios reais e aplicacoes (Parte 4)

| Cenario | Foco |
|---|---|
| 1 — Zerando o backlog | Prioridade visivel por gravidade e prazo legal |
| 2 — Redistribuindo a carga | QL por perito e redistribuicao da fila |
| 3 — Orcamento aprovado | Transformar dado em argumento tecnico de gestao |
| Casos no corpo do caderno | Integracao forense no Brasil (SP/CE), dashboard do IML, governanca de BI (-40% de incidentes), Gateway na seguranca publica |

---

## Datasets (`datasets/`)

Modelo estrela gerado a partir das quatro fontes planas da Aula 2
(`../gerar_datasets_estrela.py`). As tabelas `fato_*` guardam os eventos com as
chaves; as `dim_*`, os rotulos. Colunas detalhadas em `datasets/README.md`.

| Fato | Grao | Linhas |
|---|---|---|
| `fato_requisicoes.csv` | 1 requisicao | 120 |
| `fato_movimentacao.csv` | 1 movimento de reagente | 80 |
| `fato_produtividade.csv` | 1 perito x mes x exame | 218 |
| `fato_orcamento.csv` | 1 laboratorio x rubrica | 36 |

| Dimensao | Linhas |
|---|---|
| `dim_calendario.csv` | 396 |
| `dim_setor.csv` | 6 |
| `dim_tipo_exame.csv` | 5 |
| `dim_perito.csv` | 8 |
| `dim_delegacia.csv` | 13 |
| `dim_status.csv` | 3 |
| `dim_reagente.csv` | 10 |
| `dim_fornecedor.csv` | 6 |
| `dim_tipo_movimentacao.csv` | 2 |
| `dim_rubrica.csv` | 6 |

As quatro fontes planas (`requisicoes_periciais.csv` etc.) tambem ficam na pasta,
para conferencia e para o ETL do Dia 3.

### Datasets de orcamento e contratos (Parte 0)

Alem do modelo de pericia, a pasta `datasets/orcamento/` guarda o conjunto
dedicado ao guia do iniciante (Parte 0), no tema **orcamento e contratos**:

| Arquivo | O que e |
|---|---|
| `Orcamento_Contratos_SUJO.xlsx` | Arquivo do aluno: modelo estrela com **14 defeitos plantados** (datas/moeda em texto, TOTAL GERAL, duplicatas, brancos, categorias inconsistentes). |
| `Orcamento_Contratos_LIMPO.xlsx` | Gabarito do professor: as 10 tabelas limpas e tipadas. |
| `fato_*.csv`, `dim_*.csv` | Modelo estrela limpo em CSV, para conferencia. |

Modelo: `fato_empenhos` (**620 linhas**) + `fato_dotacao` (192) + 8 dimensoes
(`dim_calendario` 1.096 dias, `dim_fornecedor` 40, `dim_contrato` 60, entre
outras). Gerado por `gerar_datasets_orcamento.py`. Defeitos e dicionario de
dados detalhados em `datasets/orcamento/README.md`.

---

## Estatisticas

| Arquivo | Tamanho |
|---|---|
| `Dia-4-Politec.pdf` (slides do professor) | 6,14 MB |
| `caderno-dia4.html` (fonte viva, tema claro/escuro) | 227 KB |
| `Caderno Dia 4 - POLITEC.pdf` (caderno exportado, A4) | PDF a regerar (Parte 0 adicionada) |
| `gerar_caderno_aula4.py` (gerador de conteudo) | 146 KB |

| Metrica | Valor |
|---|---|
| Secoes no caderno | 107 |
| Partes (grupos) | 7 |
| Laboratorios | 7 |
| Cenarios reais | 3 (+ 4 casos aplicados) |
| Perguntas de quiz | 14 |
| Itens do glossario | 16 |
| Itens do checklist de publicacao | 7 |

---

## Como abrir

1. **Navegacao interativa** — abra `caderno-dia4.html` no navegador.
2. **Impressao/leitura offline** — abra `Caderno Dia 4 - POLITEC.pdf`
   (55 paginas) ou regenere com `python ..\exportar_pdf.py 4` (A4, sumario com paginas).
3. **Editar/regerar** — `python gerar_caderno_aula4.py` e depois
   `python ..\exportar_pdf.py 4`.

---

## Proximas aulas

- **Dia 5**: encerramento da capacitacao — consolidacao do ecossistema de dados
  da POLITEC e proximos passos do BI institucional (DAX, relacionamentos,
  Row-Level Security e governanca corporativa).

---

*Material gerado via `gerar_caderno_aula4.py`, usando o motor `../caderno_lib.py`
(ver `../AGENTS.md`).*
