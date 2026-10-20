# Aula 6 — Gestao de Projetos: do zero ao avancado com BPMN e Mermaid

**Modulo 8** — o salto final da capacitacao. Depois de medir o dado (Dias 1-5),
agora voce **muda o processo**: descreve o AS-IS, converte em diagrama BPMN com
Mermaid, **mede onde esta o gargalo**, redesenha o TO-BE e resolve o gargalo com
**automatizacao**. Tres datasets de processo com mais de 30.000 execucoes de
etapa em modelo estrela para medir em vez de chutar.

Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 6.

**Novidade**: o caderno agora usa a biblioteca `caderno_svg.py` (icones BPMN
2.0 oficiais em SVG + construtores de diagramas). Sao **34 simbolos** com a
geometria oficial OMG (eventos, atividades, gateways, swimlanes, objetos),
mais **10 ilustrações** (galeria, anatomias, comparacao de gateways, espera x
execucao, anatomia da automacao, cadeia do metodo) e **4 diagramas completos**
(AS-IS/TO-BE do Cenario 1, Cenarios 2 e 3). Os SVGs sao inline, sem
dependencia externa, e adaptam ao tema claro, escuro e a impressao via
`var(--ink)` / `var(--accent)` etc.

---

## O metodo da aula (6 passos)

```
1. Descrever  →  2. Diagramar  →  3. Medir
                                          ↓
6. Medir o ganho  ←  5. Automatizar  ←  4. Redesenhar (TO-BE)
```

---

## Conteudo do caderno (67 secoes em 8 partes)

| Parte | Conteudo |
|---|---|
| Abertura | Boas-vindas, mapa do Dia 6, recap dos 5 dias anteriores e objetivo do dia |
| **1 — Fundamentos de Gestao de Projetos** | O que e projeto (x operacao), o triangulo de projeto, ciclo de vida (5 grupos de processos), stakeholders e matriz poder/interesse, gestao de risco (prob x impacto), indicadores de projeto (SPI/CPI/TAT) |
| **2 — BPMN e Mermaid** | Por que modelar, o que e BPMN 2.0, elementos (eventos/atividades/gateways), os 3 gateways, pools e swimlanes, eventos e evento de fronteira, **Mermaid 1-5**: flowchart, subgraph (swimlanes), sequenceDiagram, stateDiagram-v2, gantt/journey/mindmap/C4 |
| **3 — Do Texto ao Diagrama** | Por que nao desenhar a mao, **o metodo das 7 perguntas**, exemplo pratico completo, heuristicas de legibilidade, versionar o processo no Git |
| **4 — Gargalos com Dados** | A descoberta espera x execucao, diagrama de esperas por etapa (com numeros medidos), **Pareto dos gargalos**, retrabalho (o desperdicio invisivel), **Little's Law (L = λ × W)**, custo da espera |
| **5 — TO-BE e Intervencao Digital** | O que e TO-BE (e o que nao e), os **5 principios de redesenho**, exemplo de TO-BE (fila priorizada), catalogo de intervencao digital, automatizar com script, **calculo do ganho**, roadmap em 4 ondas |
| **6 — Pratica Guiada** | 7 labs: descrever em texto → diagrama AS-IS → **medir o gargalo nos dados** → validar com quem executa → desenhar TO-BE → calcular ganho → apresentar e coletar feedback |
| **7 — Cenarios POLITEC** | 3 processos reais modelados ponta a ponta: **Cenario 1** Requisicao Pericial (AS-IS, gargalo, TO-BE, ganho), **Cenario 2** Empenho e Contrato (idem), **Cenario 3** Cadeia de Custodia (idem) |
| **8 — Fechamento** | O metodo resumido, erros comuns, quiz (15), glossario (21 termos), referencias, encerramento da capacitacao |

---

## Laboratorios praticos (Parte 6)

| Lab | Titulo | Entregavel |
|---|---|---|
| 1 | Descrever o processo em texto | Paragrafo AS-IS de 10-15 linhas (7 perguntas) |
| 2 | Converter texto em diagrama (Mermaid) | `processo-asis.mmd` renderizado |
| 3 | **Medir o gargalo nos dados** | Tabela dinamica espera x execucao por etapa |
| 4 | Validar o gargalo com quem executa | Lista de causas raiz confirmadas |
| 5 | Desenhar o TO-BE com intervencao | `processo-tobe.mmd` com mudancas destacadas |
| 6 | **Calcular o ganho** | Tabela antes x depois (tempo, dinheiro, capacidade) |
| 7 | Apresentar e coletar feedback | Apresentacao de 4 blocos + pedido de decisao |

---

## Cenarios com datasets proprios (Parte 7)

Todos os dados estao em `Aula 6/datasets/cenarioN_*/`, no mesmo schema
(modelo estrela), com **tempos de espera e execucao separados** — o que permite
medir o gargalo.

| # | Cenario | Pasta | Fato | Linhas | Gargalo medido |
|---|---|---|---|---|---|
| 1 | Requisicao Pericial | `cenario1_processo_pericial/` | `fato_execucao` | **10.352** | Fila do perito (41,5% da espera) |
| 2 | Empenho e Contrato | `cenario2_processo_orcamento/` | `fato_execucao` | **9.541** | Parecer + Autorizacao (51,2%) |
| 3 | Cadeia de Custodia | `cenario3_processo_custodia/` | `fato_execucao` | **10.840** | Guarda (35,3%) + lacre em papel |

**Total: 30.733 execucoes de etapa medidas.** Cada pasta tem um `README.md` com
a tabela de tempos medidos e o desenho sugerido.

### Schema (identico nos 3 cenarios)

| Tabela | Linhas | Grao |
|---|---|---|
| `fato_execucao` | 9.541-10.840 | **1 execucao de etapa** |
| `dim_etapa` | 7-8 | 1 etapa do processo (com `sequencia` e `ativada_no_tobe`) |
| `dim_unidade` | 5-7 | 1 unidade (vira swimlane) |
| `dim_sistema` | 6 | 1 sistema (papel, SIGT, planilha, e-mail, portal) |
| `dim_tipo_atividade` | 6 | Manual / automatizada / aprovacao / decisao / espera |
| `dim_status_execucao` | 4 | Concluido / em andamento / devolvido / cancelado |
| `dim_projeto` | 4 | 1 projeto de intervencao |
| `dim_calendario` | 1.096 | 1 dia (2023-01-01 a 2025-12-31) |

Colunas-chave do fato: `id_ciclo` (agrupa as etapas de um caso),
`tempo_espera_min`, `tempo_execucao_min`, `flag_retrabalho`,
`flag_automatizada`, `custo_minuto`.

---

## Numeros medidos que sustentam os cenarios

| Cenario | Processo e espera | Gargalo | Retrabalho |
|---|---|---|---|
| **1 - Pericial** | 92,4% | Fila do perito: 44 h de espera, 0 h de execucao | 11,6% |
| **2 - Orcamento** | 88,1% | Parecer (36 h) + Autorizacao (27 h) | 16,6% |
| **3 - Custodia** | 92,5% | Guarda: 55 h de espera + 4,8% de divergencia de lacre | 4,7% |

O achado que permeia os tres cenarios: **quase todo o tempo do processo e
espera, nao trabalho** — e por isso que o gargalo quase sempre esta na fila,
e nao na etapa que mais demora.

---

## Ganhos calculados nos cenarios

| Cenario | Intervencao (TO-BE) | Ganho |
|---|---|---|
| 1 | Fila priorizada por prazo legal + painel WIP | Espera 44 h &rarr; 8 h (**-82%**), 43.200 h/ano |
| 2 | Pauta automatica + alerta de dotacao | Parecer 36 h &rarr; 14 h (**-61%**), retrabalho -64% |
| 3 | QR Code por evidencia + alertas | Guarda 55 h &rarr; 18 h (**-67%**), divergencia -90% |

---

## Como abrir

1. **Caderno vivo** — abra `caderno-dia6.html` no navegador.
2. **Datasets** — va em `datasets/cenarioN_*/`. O `README.md` de cada pasta tem
   a tabela de tempos medidos.
3. **Renderizar diagramas** — cole qualquer bloco Mermaid em
   **mermaid.live** (gratis, no navegador) ou no GitHub.
4. **Regerar o caderno** — `python gerar_caderno_aula6.py`.
5. **Regerar os datasets** (semente fixa = `20260610`) —
   `python gerar_datasets_aula6.py`.
6. **PDF** (opcional) — `python ..\exportar_pdf.py 6`.

---

## Estatisticas

| Arquivo | Tamanho |
|---|---|
| `caderno-dia6.html` (fonte viva, tema claro/escuro) | 159 KB |
| `gerar_caderno_aula6.py` (gerador de conteudo) | ~76 KB |
| `gerar_datasets_aula6.py` (gerador dos 3 datasets) | ~30 KB |

| Metrica | Valor |
|---|---|
| Secoes no caderno | 67 |
| Partes (grupos) | 8 |
| Laboratorios praticos | 7 |
| Cenarios modelados ponta a ponta | 3 (AS-IS + gargalo + TO-BE + ganho) |
| Blocos de codigo | 36 |
| Blocos Mermaid prontos para copiar | 14 |
| Tabelas | 39 |
| **Diagramas SVG com notacao BPMN 2.0** | **4 completos** (Cenario 1 AS-IS, Cenario 1 TO-BE, Cenario 2, Cenario 3) |
| **Figuras ilustradas em SVG** | **6** (cadeia do metodo, comparacao dos 3 gateways, anatomia de swimlane, espera x execucao, anatomia da automacao, ...) + **galeria com 34 icones BPMN** |
| Graficos de barras (Pareto de gargalo, retrabalho) | 6 |
| Blocos QUANDO / POR QUE / EXEMPLO (`aplicab`) | 6 |
| Passos numerados (`step`) | 12 |
| Perguntas de quiz | 15 |
| Itens do glossario | 21 |
| Execucoes de etapa nos 3 datasets | 30.733 |

---

## Convencoes dos datasets

- CSV UTF-8 com BOM, separador `;`, datas ISO `AAAA-MM-DD`.
- `data_key` inteiro no formato `AAAAMMDD`.
- Chaves substitutas inteiras 1..N em ordem alfabetica.
- Tempos em **minutos** (fracionarios com 1 casa) — o que permite separar
  espera de execucao e calcular o gargalo corretamente.
- Distribuicao lognormal (cauda longa), realista para tempos de processo.
- Gerado por `../gerar_datasets_aula6.py` (semente fixa `20260610`).
- Dados sinteticos: qualquer semelhanca com processos reais e coincidencia.

---

*Material gerado via `gerar_caderno_aula6.py`, usando o motor `../caderno_lib.py`
(ver `../AGENTS.md`).*