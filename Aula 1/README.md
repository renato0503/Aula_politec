# Aula 1 — Fundamentos da Analise de Dados e Estatistica aplicada a Pericia

**Modulos 1 e 2** — o ciclo de dados na Pericia Criminal, a piramide DIKW, o principio
de Locard, tipos e qualidade da informacao, e toda a estatistica descritiva que
sustenta a gestao dos laboratorios e do IML da POLITEC/MT.

Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 1.

---

## Conteudo do caderno (61 secoes em 6 partes)

| Parte | Secoes | Conteudo |
|---|---|---|
| Abertura | 4 | Boas-vindas, como usar o caderno, mapa do Dia 1 e **roadmap do curso (Dia 1 a Dia 5)** |
| **1 — Modulo 1: Fundamentos da Analise** | 20 | Ciclo de dados, piramide DIKW, Locard, tipos de dados, os 4 pilares da qualidade, dashboards sob pressao (Stephen Few), custo do dado sujo, **dado x metrica x indicador**, **estudo de caso do swab ao mandado**, **mapear o ciclo de dados do setor**, **fluxo de investigacao**, **fontes de dados**, **integracao de sistemas**, **padronizacao de campos**, **LGPD**, **campo a bancada** e **KPIs** |
| **2 — Modulo 2: Fundamentos Estatisticos** | 21 | Estatistica descritiva, media/mediana/moda, TAT do DNA, Deming, desvio padrao, boxplot (Tukey), histogramas, correlacao x causalidade, Cobra Effect, outliers, Cisnes Negros (Taleb), **como calcular media/mediana/moda**, **como calcular desvio padrao**, **amplitude/variancia/CV**, **quartis e percentis**, **como montar um boxplot**, **curva normal 68-95-99,7**, **erro x vies**, **escolher a medida certa** e **metricas de gestao (TAT/backlog/produtividade/qualidade)** |
| **3 — Pratica guiada** | 7 | 7 laboratorios de raciocinio, calculo e leitura de dados |
| **4 — Cenarios e aplicacoes praticas** | 4 | TAT do DNA, auditoria do IML, relatorio para a diretoria e deteccao de um Cisne Negro |
| **5 — Fechamento** | 5 | Resumo, tarefa de casa, quiz (15 perguntas), folha de cola/glossario e referencias |

---

## Laboratorios praticos (Parte 3)

| Lab | Titulo | O que treina |
|---|---|---|
| 1 | Media x mediana com dados de TAT | Como um outlier distorce a media |
| 2 | Classifique os dados da POLITEC | Estruturado / semiestruturado / nao estruturado |
| 3 | Auditoria de qualidade nos 4 pilares | Acuracia, completude, consistencia, atualidade |
| 4 | Lendo um boxplot e um histograma | Interpretacao visual da producao |
| 5 | Caca a causalidade | Correlacao espuria x causalidade inversa |
| 6 | Calculo manual de variancia e desvio padrao | Desvios, quadrados, variancia e raiz — no papel |
| 7 | Interpretando uma tabela de producao real | Media, mediana, outlier e resumo executivo |

---

## Cenarios e aplicacoes praticas (Parte 4)

| Cenario | Foco |
|---|---|
| A — Diagnostico de TAT do laboratorio de DNA | Media x mediana x P90 com outlier explicado |
| B — Auditoria de qualidade da base de necropsias do IML | Os 4 pilares aplicados a uma base real |
| C — Relatorio gerencial para a diretoria | Escolha de 3 a 5 KPIs com meta e contexto |
| D — Deteccao precoce de um Cisne Negro | Limites estatisticos, investigacao e contingencia |

---

## Estatisticas

| Arquivo | Tamanho |
|---|---|
| `Dia-1-Politec.pdf` (slides do professor) | 5,2 MB |
| `caderno-dia1.html` (fonte viva, tema claro/escuro) | 161 KB |
| `Caderno Dia 1 - POLITEC.pdf` (caderno exportado, A4) | 4,9 MB · 53 paginas |
| `gerar_caderno_aula1.py` (gerador de conteudo) | 102 KB |

| Metrica | Valor |
|---|---|
| Secoes no caderno | 61 |
| Partes (grupos) | 6 |
| Laboratorios | 7 |
| Cenarios reais | 4 |
| Perguntas de quiz | 15 |
| Graficos de barras | 5 (TAT do DNA, histograma semanal, curva normal, metricas de gestao e lab de histograma) |
| Blocos QUANDO / POR QUE / EXEMPLO (`aplicab`) | 11 |
| Passos numerados (`step`) | 22 |
| Itens do glossario/folha de cola | 20 |

---

## Como abrir

1. **Navegacao interativa** — abra `caderno-dia1.html` no navegador.
   - Botao **Tema** alterna claro/escuro; **Imprimir / PDF** abre a impressao.
   - Indice sticky a esquerda com busca.
2. **Impressao/leitura offline** — abra `Caderno Dia 1 - POLITEC.pdf`.
3. **Editar/regerar** — `python gerar_caderno_aula1.py` e
   `python ..\exportar_pdf.py 1`.

---

## Proximas aulas

- **Dia 2**: planilhas e manipulacao de dados no Excel/Google Sheets.
- **Dia 3**: validacao de dados, mini-dashboards e organizacao avancada.
- **Dia 4**: Power BI — da planilha estruturada ao dashboard interativo.
- **Dia 5**: encerramento da capacitacao — consolidacao do ecossistema de dados.

---

*Material gerado via `gerar_caderno_aula1.py`, usando o motor `../caderno_lib.py`
(ver `../AGENTS.md`).*
