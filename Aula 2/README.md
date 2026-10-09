# Aula 2 — Planilhas e Manipulacao de Dados na Pericia

**Modulo 3** — Excel e Google Sheets aplicados a gestao de laboratorios e IML:
funcoes, logica condicional, formatacao condicional, referencias absolutas,
tabelas estruturadas, filtros e ordenacao personalizada.

Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 2.

---

## Conteudo do caderno (68 secoes em 6 grupos)

| Grupo | Conteudo |
|---|---|
| **Abertura** | Boas-vindas, mapa do Dia 2, recapitulacao do Dia 1 e a analogia TAT/planilha (bancada x amostra) |
| **1 — Modulo 3 Parte 1: Funcoes e logica** | Dicionario de funcoes do dia, primeira funcao passo a passo, SOMA/MEDIA, CONT.NUM/CONT.VALORES/MAX/MIN, MEDIANA, SE, funcoes de texto/data, SOMASE, CONT.SE/CONT.SES/SOMASES, aplicacoes (estoque de reagentes, produtividade por perito, prazos com HOJE), SE aninhado x SES, erros de formula, caso do backlog de DNA, semaforo do TAT, formatacao com formula, barras de dados, VisiCalc e fechamento da manha |
| **2 — Modulo 3 Parte 2: Referencias, tabelas e filtros** | Referencias relativa/absoluta/mista, guia do F4, referencias entre abas e nomes, caso da taxa de importacao, orcamento imune a erro, tabelas estruturadas (Ctrl+T) e detalhe do `[@]`, ponte para o BI (Kimball), filtros e filtros avancados, Fantasma de Heilbronn, ordenacao personalizada, fila de criticos, consolidacao de planilhas, subtotais/dinamicas, colunas x medidas, limite do Excel, checklist de migracao ao BI e fechamento da tarde |
| **3 — Pratica guiada** | 7 laboratorios + painel de backlog integrador |
| **4 — Cenarios e aplicacoes praticas** | 4 cenarios completos (orcamento de reagentes, fila de criticos 8h, produtividade por perito, auditoria de qualidade) |
| **5 — Boas praticas e fechamento** | Erros comuns, nomenclatura, Sheets x Excel, governanca, atalhos, checklist do gestor, quiz (15), glossario ampliado e referencias |

---

## Datasets (datasets/)

Todos os exemplos, labs e cenarios do caderno usam dados reais simulados da POLITEC/MT.
Importe os CSVs para acompanhar os passo a passo no Excel.

| Arquivo | Descricao | Linhas | Colunas |
|---|---|---|---|
| `requisicoes_periciais.csv` | Base principal de requisicoes periciais | 120 | id_requisicao, data_recebimento, delegacia_origem, tipo_exame, setor, perito_responsavel, status, data_laudo, dias_uteis |
| `movimentacao_reagentes.csv` | Entradas e saidas de reagentes por setor | 80 | id, data, reagente, tipo_movimentacao, quantidade, setor, fornecedor |
| `produtividade_peritos.csv` | Laudos concluidos por perito, mes e tipo | 218 | mes, perito, tipo_exame, laudos_concluidos |
| `orcamento_setores.csv` | Custo orcado x realizado por laboratorio | 36 | laboratorio, rubrica, orcado, realizado |

---

## Laboratorios praticos (Parte 3)

| Lab | Titulo | O que constroi |
|---|---|---|
| 1 | Estruturar a base (Ctrl+T) | Tabela estruturada pronta para crescer |
| 2 | Calcular o TAT automaticamente | Coluna TAT com tratamento de "Em andamento" |
| 3 | Aplicar o semaforo do TAT | Regras condicionais verde/amarelo/vermelho |
| 4 | Criar os indicadores | CONT.SE, MEDIA, SOMASE com referencias absolutas |
| 5 | Filtros + ordenacao personalizada | A lista do diretor para a reuniao das 8h |
| 6 | Auditoria de base suja (limpeza) | Mesclagens, datas texto, espacos e duplicatas corrigidos |
| 7 | Consolidando 4 planilhas de setores | Base unificada validada por CONT.SE |
| — | Painel de backlog (integrador) | Tudo junto: base + TAT + semaforo + indicadores |

---

## Cenarios e aplicacoes (Parte 4)

| Cenario | Problema real | Entregavel |
|---|---|---|
| A | Orcamento anual de reagentes estourou por erro de referencia | Orcamento imune a erro com parametros travados (F4) |
| B | Fila de laudos criticos montada a mao em 40 min | Lista das 8h em 10 segundos (cor + ordenacao) |
| C | Carga entre peritos decidida por percepcao | Painel de produtividade com CONT.SES e meta |
| D | Relatorio publicado com base contaminada | Auditoria de qualidade (mesclagens, datas, duplicatas) |

---

## Estatisticas

| Arquivo | Tamanho |
|---|---|
| `Dia-2-Politec.pdf` (slides do professor) | 4,5 MB |
| `caderno-dia2.html` (fonte viva, tema claro/escuro) | 177 KB |
| `Caderno Dia 2 - POLITEC.pdf` (caderno exportado, A4) | 3,8 MB · 60 paginas |
| `gerar_caderno_aula2.py` (gerador de conteudo) | 111 KB |

| Metrica | Valor |
|---|---|
| Secoes no caderno | 68 |
| Grupos (partes) | 6 |
| Laboratorios | 7 + 1 integrador |
| Cenarios praticos | 4 |
| Perguntas de quiz | 15 |
| Atalhos catalogados | 8 |
| Itens do checklist do gestor | 10 |

---

## Como abrir

1. **Navegacao interativa** — abra `caderno-dia2.html` no navegador.
2. **Impressao/leitura offline** — abra `Caderno Dia 2 - POLITEC.pdf`.
3. **Praticar com os datasets** — importe os CSVs de `datasets/` no Excel e siga os labs.
4. **Editar/regerar** — `python gerar_caderno_aula2.py` e
   `python ..\exportar_pdf.py 2`.

---

## Proximas aulas

- **Dia 3**: validacao de dados (listas suspensas e regras de entrada),
  mini-dashboards na propria planilha e organizacao avancada da base.
- **Dia 4**: Power BI — a planilha estruturada vira dashboard interativo.

---

*Material gerado via `gerar_caderno_aula2.py`, usando o motor `../caderno_lib.py`
(ver `../AGENTS.md`).*
