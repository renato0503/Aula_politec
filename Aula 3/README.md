# Aula 3 — Organizacao, Visualizacao e Ferramentas de Analise na Pericia

**Modulos 4 e 5** — validacao e limpeza de dados, visualizacao honesta, mini-painel
de gestao pericial, Excel x Power BI, ETL e Power Query aplicados a POLITEC/MT.

Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 3.

---

## Conteudo do caderno (63 secoes em 6 partes)

| Parte | Conteudo |
|---|---|
| Abertura | Boas-vindas, mapa do dia, autores de referencia (Cairo, Tufte, Kimball) |
| **1 — Modulo 4: Organizacao e Visualizacao** | Cadeia de custodia digital, validacao (listas, datas, numeros), cadeia de erros, limpeza (ARRUMAR/PRI.MAIUSCULA/SUBSTITUIR), duplicatas, custo dos dados sujos, Cairo, regras do grafico honesto, triangulo da visualizacao, problema da pizza, Tufte e chartjunk, caso do grafico 3D, honesto x enganoso, guia de escolha, mini-painel (estrutura, KPIs, formatacao, resultado) |
| **2 — Modulo 5: Ferramentas e ETL** | Excel x Power BI (paradigma, forcas, limites, quando usar), Kimball, processo ETL, ETL na pratica, transparencia pericial, origem do Power BI, 4 problemas de exportacao, checklist Pre-ETL, nomenclatura, Power Query, automacao do relatorio mensal, filosofia da automacao, comparativo consolidado, cadeia completa, erros de iniciantes, inteligencia compartilhada, TAT por setor, evolucao mensal, resumo |
| **3 — Pratica guiada** | 6 laboratorios com passo a passo de cliques e atalhos |
| **4 — Cenarios e aplicacoes praticas** | 4 cenarios reais da POLITEC (grafico 3D, transparencia MP/Defensoria, automacao de 4 planilhas, integracao de seguranca publica) |
| **5 — Fechamento** | Resumo do dia, ponte para o Dia 4, tarefa de casa, quiz (15), glossario, referencias |

---

## Laboratorios praticos (Parte 3)

| Lab | Titulo | O que constroi |
|---|---|---|
| 1 | Validacao de dados na entrada | Listas suspensas, restricao de datas e limites numericos |
| 2 | Limpeza (ARRUMAR, PRI.MAIUSCULA, SUBSTITUIR) | Padronizacao de nomes, setores e tipos de exame |
| 3 | Remocao de duplicatas pela chave unica | Contagem de producao sem dupla contagem |
| 4 | Estruturar a base do mini-painel | Tabela estruturada com coluna TAT viva |
| 5 | KPIs e slicers do mini-painel | Producao, TAT medio e % atrasados com filtros Mes/Setor |
| 6 | Automatizar a limpeza com Power Query | Receita de ETL gravada: 2 dias -> 30s |

---

## Cenarios praticos (Parte 4)

| Cenario | Situacao | Entregavel |
|---|---|---|
| 1 | O grafico 3D que enganou o Secretario | Grafico em 2D com eixo Y no zero |
| 2 | Portal de transparencia para MP e Defensoria | Painel Power BI publicado e autoatendido |
| 3 | Automatizar o relatorio de 4 planilhas | Pasta Entrada_Mensal + Power Query |
| 4 | Inteligencia integrada de seguranca publica | Visao de cruzamento pericia + policia |

---

## Estatisticas

| Arquivo | Tamanho |
|---|---|
| `Dia-3-Politec.pdf` (slides do professor) | 4,0 MB |
| `caderno-dia3.html` (fonte viva, tema claro/escuro) | 138 KB |
| `gerar_caderno_aula3.py` (gerador de conteudo) | 81 KB |
| `Caderno Dia 3 - POLITEC.pdf` (caderno exportado, A4) | 4,2 MB · 47 paginas |

| Metrica | Valor |
|---|---|
| Secoes no caderno | 63 |
| Partes (grupos) | 6 |
| Laboratorios | 6 |
| Cenarios | 4 |
| Perguntas de quiz | 15 |
| Blocos QUANDO/POR QUE/EXEMPLO | 5 |
| Graficos de barras embutidos | 6 |
| Avisos de armadilha (`callout err`) | 17 |
| Passos guiados (`step`) | 16 |

---

## Como abrir

1. **Navegacao interativa** — abra `caderno-dia3.html` no navegador
   (tema claro/escuro, indice lateral com busca, botao Imprimir/PDF).
2. **Impressao/leitura offline** — abra `Caderno Dia 3 - POLITEC.pdf`
   (47 paginas, sumario com numeros de pagina) ou exporte com
   `python ..\exportar_pdf.py 3` (requer Playwright).
3. **Editar/regerar** — `python gerar_caderno_aula3.py`.

---

## Proximas aulas

- **Dia 4**: Power BI Desktop — interface, conexao de dados reais, modelagem
  dimensional (modelo estrela) e o primeiro dashboard funcional de gestao pericial.
- **Dia 5**: DAX, publicacao e projeto final.

---

*Material gerado via `gerar_caderno_aula3.py`, usando o motor `../caderno_lib.py`
(ver `../AGENTS.md`).*
