# -*- coding: utf-8 -*-
"""Gerador do caderno da Aula 5 - POLITEC/MT.

Tema: Dashboards de BI - o salto final. Cenarios com datasets proprios
(>=1000 linhas cada) para o aluno treinar construcao de dashboards em Power BI
e montar um projeto integrador com >=3 abas tematicas.

Rode:  python gerar_caderno_aula5.py
PDF:   python ..\\exportar_pdf.py 5
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from caderno_lib import (Caderno, p, h3, ul, checklist, ficha, callout, tbl, code,
                         step, q, aplicab, grid2, flow_h, kpi, antesdepois,
                         legenda, glossary, bar_chart)

cad = Caderno(
    out=str(pathlib.Path(__file__).resolve().parent / "caderno-dia5.html"),
    dia=5,
    kicker="Aula 5 · Dashboards de BI",
    headline="Dashboards de BI - 5 cenarios com datasets proprios",
    sub="O salto final do curso. DAX avancado, governanca corporativa, RLS, "
        "Otimizacao e um projeto integrador com 5 cenarios tematicos "
        "(Backlog, DNA, Criminalidade, Orcamento, Custodia). "
        "Cada cenario tem seu dataset proprio com mais de 1000 linhas no "
        "modelo estrela. Voce monta o painel final com pelo menos 3 abas.",
    meta="Curso de Capacitacao POLITEC/MT - Professor Renato Rosa - Dia 5 - Modulo 7 "
         "(Encerramento da Capacitacao)",
    descricao="Caderno do Dia 5 do Curso de Capacitacao POLITEC/MT: Dashboards de BI aplicados "
              "a pericia criminal. DAX avancado (CALCULATE, iteradores, time intelligence, "
              "variaveis, performance), Power BI Service avancado (dataflows, datasets "
              "compartilhados, Apps), seguranca (RLS, OLS), Power Platform, Microsoft Fabric. "
              "Projeto integrador com 5 cenarios tematicos (Backlog de Pericias, TAT do DNA, "
              "Mapa da Criminalidade em MT, Orcamento, Cadeia de Custodia), cada um com "
              "dataset sintetico de 1100-1500 linhas em modelo estrela."
)

# =================================================================
# ABERTURA
# =================================================================
cad.grp("Abertura", "O salto final do curso: do Desktop a instituicao data-driven.")

cad.section("boas-vindas", "Bem-vindo ao caderno do Dia 5",
    p("Chegou a hora de fechar o ciclo. Depois de estatistica, planilha, "
      "organizacao e Power BI, hoje a <b>pericia criminal</b> se transforma em "
      "<b>inteligencia institucional</b> data-driven.") +
    p("O Dia 5 entrega o <b>projeto integrador</b>: cinco cenarios tematicos, "
      "cada um com dataset proprio, todos com mais de 1000 linhas no modelo "
      "estrela. Voce escolhe pelo menos <b>tres</b> e monta um painel "
      "institucional completo no Power BI.") +
    legenda([
        ("\U0001f4a1", "Parte 1 - DAX avancado",
         "CALCULATE, iteradores (SUMX/AVERAGEX), time intelligence, variaveis, performance."),
        ("\U0001f6e1", "Parte 2 - Service e governanca",
         "Dataflows, RLS, OLS, Apps avancado, Power Platform e Microsoft Fabric."),
        ("\U0001f9ea", "Parte 3 - 7 laboratorios",
         "Sete labs praticos que culminam no painel final."),
        ("\U0001f5fa", "Parte 4 - 5 cenarios com datasets",
         "Backlog, DNA, Criminalidade em MT, Orcamento e Cadeia de Custodia."),
        ("\U0001f3af", "Parte 5 - Projeto integrador",
         "Monte o seu painel final com 3+ abas tematicas."),
        ("\U0001f4dc", "Parte 6 - Fechamento",
         "Erros, checklist final, ecossistema, quiz e referencias do curso."),
    ])
)

cad.section("mapa-do-dia", "Mapa do Dia 5: dois blocos, cinco cenarios, um projeto",
    p("O dia comeca no DAX (linguagem do Power BI) e termina com o seu "
      "dashboard publicado, com seguranca por linha (RLS) e governanca "
      "apropriada para um orgao publico.") +
    grid2([
        ("\U0001f305 Manha (08h-12h) - DAX avancado",
         ul(["Revisao da teoria de medidas x colunas calculadas",
             "Contexto de linha x contexto de filtro",
             "CALCULATE, iteradores (SUMX, AVERAGEX, COUNTX)",
             "Time intelligence (YTD, QTD, MoM, YoY)",
             "Variaveis (VAR), performance e estrela do esquema",
             "Voce saira escrevendo medidas densas com seguranca"])),
        ("\U0001f306 Tarde (13h-17h) - Service, seguranca e projeto",
         ul(["Power BI Service avancado: dataflows e datasets compartilhados",
             "RLS (Row-Level Security) e OLS (Object-Level Security)",
             "Apps, deployment pipelines, gateways",
             "Microsoft Fabric e Power Platform (introducao)",
             "<b>Projeto integrador</b>: 5 cenarios, escolha 3, monte 3+ abas"]))
    ])
)

cad.section("recap-do-curso", "Recap dos quatro dias anteriores",
    p("Antes de avancarmos, vale lembrar onde estamos. Em quatro dias a turma "
      "percorrer o caminho completo:") +
    flow_h([
        ("1", "D1 - Dados"),
        ("2", "D2 - Planilha"),
        ("3", "D3 - Organizacao"),
        ("4", "D4 - Power BI"),
        ("5", "D5 - Dashboards"),
    ]) +
    tbl(["Dia", "Foco", "Entregavel principal"],
        [["<b>D1</b>", "Estatistica, qualidade, KPIs", "Raciocínio sobre dado"],
         ["<b>D2</b>", "Planilha (Excel/Sheets), formulas", "Planilha limpa e tipada"],
         ["<b>D3</b>", "Validacao, organizacao, mini-dashboard", "Base consolidada"],
         ["<b>D4</b>", "Power BI Desktop + Service", ".pbix publicavel"],
         ["<b>D5</b>", "DAX avancado, RLS, projeto integrador", "Painel institucional"]],
        num_cols=[]) +
    callout("note", "O contrato pedagogico",
        "Cada dia construiu o palco do proximo. Hoje nao comecamos do zero: "
        "voce ja sabe o ciclo do dado, formula, validacao, visual. O que falta "
        "e a <b>camada de inteligencia</b>: medidas com logica de negocio, "
        "seguranca por papel, governanca multi-equipe.")
)

cad.section("objetivo-do-dia", "Objetivo do Dia 5: o painel institucional da POLITEC",
    p("Ao fim do dia, voce entrega um <b>.pbix publicavel</b> com:") +
    checklist([
        "Ao menos <b>3 abas</b> tematicas (cada uma vinda de um cenario).",
        "<b>Relacionamentos</b> corretos e tabelas fato bem tipadas.",
        "<b>Medidas DAX</b> com logica de negocio (TAT, % no prazo, execucao).",
        "<b>RLS</b> (Row-Level Security) habilitada em ao menos uma aba.",
        "<b>Formatacao condicional</b> em ao menos 3 KPIs.",
        "<b>Publicacao</b> em workspace segregado e link via App.",
    ]) +
    ficha("g", "Criterio de conclusao",
        "Ao terminar o dia, o chefe do seu setor e o diretor conseguer abrir "
        "o seu painel no celular, fazer drill down em um municipio e ler o "
        "TAT sem perguntar nada. Se isso for possivel, a Aula 5 foi "
        "cumprida.") +
    callout("tip", "O segredo esta nao nas ferramentas, e nos dados",
        "Power BI nao resolve dado sujo - ele <b>amplifica</b> o que esta bom "
        "ou ruim. Por isso, cada dataset da Aula 5 e <b>sintetico e limpo</b>: "
        "voce aprende o pipeline em ambiente controlado. Quando jogar o dado "
        "real da POLITEC, aplicara a mesma logica.")
)

# =================================================================
# PARTE 1 - MODULO 7 PARTE 1: DAX AVANCADO
# =================================================================
cad.grp("Parte 1 - DAX Avancado",
        "A linguagem do Power BI para criar logica de negocio: medidas, contexto, tempo, performance.")

cad.section("dax-recap", "Recap de DAX: o que ja vimos no Dia 4",
    p("No Dia 4 voce usou DAX em <b>medidas simples</b> e <b>colunas "
      "calculadas</b>. Hoje vamos alem:Medidas com <b>contexto de filtro</b> "
      "alterado por CALCULATE, <b>iteradores</b> que percorrem linhas, "
      "<b>time intelligence</b> e <b>variaveis</b> para performance.") +
    callout("note", "Lembrete rapido",
        "<b>Medida</b>: calculada sob demanda no visual (recalcula a cada "
        "filtro). <b>Coluna calculada</b>: materializada na tabela (consome "
        "RAM). Em 95% dos casos da Aula 5, voce quer <b>medidas</b>.")
)

cad.section("medidas-vs-colunas", "Medida x Coluna calculada - decisao consciente",
    p("A decisao mais importante do DAX: calcular no visual ou materializar "
      "na tabela?") +
    tbl(["Aspecto", "Medida (medida)", "Coluna calculada (coluna calculada)"],
        [["<b>Onde calcula</b>", "No visual, a cada slicer", "Na tabela, uma unica vez"],
         ["<b>Espaco em disco</b>", "Quase zero", "Consome RAM/VertiPaq"],
         ["<b>Filtros?</b>", "Reage (recalcula)", "Estatico (fica na linha)"],
         ["<b>Contexto</b>", "Filtro + linha", "Linha da tabela"],
         ["<b>Uso ideal</b>", "Agregacoes, KPIs, %", "Categorias derivadas, ordem custom"]],
        num_cols=[]) +
    antesdepois(
        "<b>Coluna</b> para calcular <code>Categoria = IF(Valor>1000,&quot;Alto&quot;,&quot;Baixo&quot;)</code>"
        " em 100k linhas (consome RAM).",
        "<b>Medida</b> para <code>% Atraso = COUNTROWS(FILTER(...)) / COUNTROWS(...)</code>"
        ": recalcula so quando muda o filtro.",
        errado="Anti-pattern",
        certo="Boa pratica")
)

cad.section("contexto-de-linha", "Contexto de linha: por linha, por vez",
    p("O <b>contexto de linha</b> e o &quot;ambiente&quot; que existe para cada "
      "linha individual de uma tabela, durante a avaliacao de uma coluna "
      "calculada ou de uma funcao iteradora. Ele e automatico: para cada "
      "linha, os valores daquela linha estao disponiveis.") +
    code(
        "Categoria Valor = [Valor]\n"
        "Acima de 1000 = IF([Valor] > 1000, \"Alto\", \"Baixo\")\n"
        "Categoria Valor 2 = SWITCH(\n"
        "    TRUE(),\n"
        "    [Valor] >= 10000, \"Premium\",\n"
        "    [Valor] >= 1000, \"Alto\",\n"
        "    [Valor] >= 100, \"Medio\",\n"
        "    \"Baixo\"\n"
        ")",
        "DAX"
    ) +
    callout("tip", "Quando o contexto de linha importa",
        "Em qualquer <b>coluna calculada</b> e dentro de funcoes "
        "<b>iteradoras</b> (SUMX, AVERAGEX, FILTER). Em medidas simples como "
        "<code>SUM(Valor)</code>, voce ja esta no contexto de filtro.")
)

cad.section("contexto-de-filtro", "Contexto de filtro: o palco do Power BI",
    p("O <b>contexto de filtro</b> e o conjunto de filtros ativos no visual no "
      "momento da avaliacao. Ele vem dos <b>slicers</b>, dos <b>eixos do "
      "grafico</b>, das <b>legendas</b> e dos <b>filtros do painel</b>. Toda "
      "medida e avaliada dentro de um contexto de filtro - e por isso "
      "&quot;responde&quot; aos slicers sem codigo extra.") +
    callout("purple", "Exemplos",
        "Em um grafico de barras com eixo = Setor, cada barra e calculada "
        "com o filtro <code>Setor = X</code>. A medida <code>SUM(Valor)</code> "
        "retorna o valor daquele setor - e nao do total. Isso e o contexto "
        "de filtro em acao.")
)

cad.section("calculate", "CALCULATE: a funcao mais importante do DAX",
    p("<code>CALCULATE</code> troca o contexto de filtro. &quot;Calcule esta "
      "medida, mas antes ajuste o filtro para X&quot;. E a funcao que destrava "
      "90% das medidas avancadas.") +
    code(
        "Receita SP = CALCULATE(SUM(Vendas[Valor]), Regiao[UF] = \"SP\")\n"
        "Receita exceto SP = CALCULATE(SUM(Vendas[Valor]),\n"
        "    FILTER(ALL(Regiao), Regiao[UF] <> \"SP\"))\n"
        "% SP = DIVIDE([Receita SP], [Receita Total])",
        "DAX"
    ) +
    aplicab(
        "<b>Quando o chefe pergunta</b> &quot;quanto da receita veio de SP?&quot;",
        "<code>CALCULATE</code> permite <b>filtros extras</b> ou <b>remover "
        "filtros</b> (com <code>ALL</code> ou <code>REMOVEFILTERS</code>).",
        "Na POLITEC: <i>&quot;quantos laudos foram feitos <b>por peritos "
        "que nao estao no meu setor</b>?</i> - <code>CALCULATE(COUNTROWS(Req), "
        "PERITO[setor_key] &lt;&gt; SELECTEDVALUE(dim_setor[setor_key]))</code>"
    )
)

cad.section("sumx-averagex", "SUMX e AVERAGEX: iteradores",
    p("Funcoes <b>iteradoras</b> percorrem linha a linha, calculam a expressao e "
      "depois agregam. Sao como um <code>for</code> em programacao.") +
    code(
        "Receita Total = SUMX(Vendas, Vendas[Qtd] * Vendas[Preco])\n"
        "Receita Media = AVERAGEX(Vendas, Vendas[Qtd] * Vendas[Preco])\n"
        "Receita Ponderada = SUMX(Vendas, Vendas[Preco] * Vendas[Peso]) / SUM(Vendas[Peso])",
        "DAX"
    ) +
    tbl(["Funcao", "Itera?", "Agrega"],
        [["SUM, AVERAGE, COUNT", "Nao", "Soma, media, conta a coluna"],
         ["SUMX, AVERAGEX, COUNTX, MINX, MAXX", "<b>Sim</b>", "Soma, media, conta a expressao"],
         ["FILTER", "<b>Sim</b>", "Retorna tabela filtrada (nao agrega)"]],
        num_cols=[]) +
    callout("err", "Usar SUMX com soma simples",
        "<code>SUMX(Vendas, Vendas[Valor])</code> e <b>mais lento</b> do que "
        "<code>SUM(Vendas[Valor])</code> sem nenhum beneficio. Use o X <b>so "
        "quando a expressao da linha e complexa</b> (multiplicacao, condicao, "
        "calculo).")
)

cad.section("divide-seguro", "DIVIDE: dividir sem erro de #DIV/0!",
    p("Em DAX, <code>1/0</code> retorna <code>Infinity</code>, nao erro - e "
      "algumas vezes isso bagunca visualizacoes. <code>DIVIDE</code> trata "
      "o denominador zero automaticamente.") +
    code(
        "% no Prazo = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(Requisicoes), Requisicoes[em_atraso] = 0),\n"
        "    COUNTROWS(Requisicoes)\n"
        ")",
        "DAX"
    ) +
    antesdepois(
        "<code>% = A / B</code>. Se B = 0 (nenhuma requisicao concluida), "
        "<b>Infinity</b> aparece no grafico.",
        "<code>% = DIVIDE(A, B, 0)</code>. Se B = 0, retorna 0 e o grafico "
        "fica limpo. Opcionalmente passe um alternativo: <code>DIVIDE(A, B, BLANK())</code>.",
        errado="Frgil",
        certo="Robusto"
    )
)

cad.section("countrows-e-count", "COUNTROWS x COUNT x DISTINCTCOUNT",
    p("Tres formas de contar: cada uma serve a um contexto diferente.") +
    tbl(["Funcao", "O que conta", "Quando usar"],
        [["COUNTROWS(tabela)", "Linhas de uma tabela (ou tabela filtrada)", "Para contar eventos (requisicoes, exames)"],
         ["COUNT(coluna)", "Linhas nao-vazias da coluna", "Para contar valores preenchidos"],
         ["DISTINCTCOUNT(coluna)", "Valores unicos nao-vazios", "Para contar clientes, municipios, peritos distintos"]],
        num_cols=[]) +
    code(
        "Requisicoes = COUNTROWS(Requisicoes)\n"
        "Municipios Atendidos = DISTINCTCOUNT(Ocorrencias[municipio_key])\n"
        "Peritos Ativos = DISTINCTCOUNT(Produtividade[perito_key])",
        "DAX"
    )
)

cad.section("filtros-all-remove", "ALL, REMOVEFILTERS, KEEPFILTERS: mexendo no filtro",
    p("Essas tres funcoes sao a chave para medidas de <b>% do total</b>, "
      "<b>classificacao</b> e <b>comparacao com o todo</b>.") +
    code(
        "% do Total = DIVIDE([Receita Atual], CALCULATE([Receita Atual], ALL(Regiao)))\n"
        "Receita Sem Filtro Setor = CALCULATE(SUM(Vendas[Valor]), REMOVEFILTERS(Setor))\n"
        "Receita Mantendo Filtro UF = CALCULATE(SUM(Vendas[Valor]), KEEPFILTERS(Regiao))",
        "DAX"
    ) +
    aplicab(
        "<b>Quando</b> o usuario quer saber quanto aquele setor representa "
        "do total.",
        "<code>ALL(Setor)</code> remove o filtro de Setor, mostrando o "
        "denominador total. <code>KEEPFILTERS</code> faz o oposto: preserva "
        "filtros externos.",
        "Na POLITEC: <i>Quero o backlog do DNA mas a porcentagem em relacao "
        "ao backlog total.</i> Use <code>CALCULATE([Backlog], ALL(dim_setor))</code> "
        "para o denominador."
    )
)

cad.section("filter-table", "FILTER: tabela filtrada como parametro",
    p("<code>FILTER</code> retorna uma tabela, nao um valor. E o &quot;WHERE&quot; "
      "do DAX e combina com qualquer iterador.") +
    code(
        "Requisicoes Atrasadas = COUNTROWS(FILTER(Requisicoes, Requisicoes[em_atraso] = 1))\n"
        "Top 10 Faturas = TOPN(10, FILTER(Vendas, Vendas[Status] = \"Pago\"), Vendas[Valor], DESC)",
        "DAX"
    ) +
    callout("tip", "Truque de performance",
        "<code>FILTER</code> itera a tabela inteira - pode ser caro. "
        "Quando puder, use <b>filtros diretos</b> na propria medida "
        "(<code>CALCULATE(COUNTROWS(T), T[campo] = X)</code>) que o motor "
        "otimiza melhor.")
)

cad.section("time-intel-intro", "Time intelligence: comparando com o tempo",
    p("Toda medida temporal no Power BI exige uma <b>tabela de datas marcada</b> "
      "(ja feita no Dia 4). A partir disso, DAX oferece funcoes de "
      "<b>inteligencia temporal</b>.") +
    code(
        "Mes Atual = TOTALMTD(SUM(Vendas[Valor]), dim_calendario[data])\n"
        "Mes Anterior = CALCULATE([Mes Atual], DATEADD(dim_calendario[data], -1, MONTH))\n"
        "YTD = TOTALYTD(SUM(Vendas[Valor]), dim_calendario[data])",
        "DAX"
    ) +
    callout("err", "Time intel falhando?",
        "O motivo #1 e a tabela de datas nao estar <b>marcada como tabela "
        "de datas</b> (clique direito na tabela -> Marcar como tabela de "
        "datas). Sem isso, <code>TOTALYTD</code> e <code>SAMEPERIODLASTYEAR</code> "
        "retornam vazio.")
)

cad.section("time-intel-essenciais", "As 7 funcoes de time intelligence que vao salvar voce",
    tbl(["Funcao", "O que faz", "Exemplo na POLITEC"],
        [["<code>SAMEPERIODLASTYEAR</code>", "Mesmo periodo do ano passado", "TAT-2024 para comparar com 2025"],
         ["<code>DATEADD(c, n, MES)</code>", "Deslocamento em n meses", "Ultimos 30 dias / 60 dias"],
         ["<code>PARALLELPERIOD</code>", "Periodo paralelo (mes inteiro)", "Mes anterior completo"],
         ["<code>TOTALYTD</code>", "Acumulado no ano", "Laudos concluidos em 2025 ate hoje"],
         ["<code>TOTALQTD</code>", "Acumulado no trimestre", "TAT do trimestre atual"],
         ["<code>PREVIOUSMONTH</code>", "Mes anterior (atalho)", "Comparar com mes passado"],
         ["<code>DATESINPERIOD</code>", "Janela customizada (rolling)", "Ultimos 90 dias uteis"]],
        num_cols=[])
)

cad.section("ytd-vs-ytm", "YTD x YTM x MoM x YoY - os 4 basicos de gestao",
    code(
        "YTD Receita = TOTALYTD(SUM(Vendas[Valor]), dim_calendario[data])\n"
        "MoM % = DIVIDE([Receita Atual] - [Receita Mes Anterior], [Receita Mes Anterior])\n"
        "YoY % = DIVIDE([Receita Atual] - [Receita Mesmo Mes Ano Passado], [Receita Mesmo Mes Ano Passado])\n"
        "YTM Receita = TOTALYTD(SUM(Vendas[Valor]), dim_calendario[data])",
        "DAX"
    ) +
    callout("tip", "Padrao MoM/YoY",
        "Toda medida comparativa segue esse padrao: <b>atual</b> vs "
        "<b>periodo anterior recalculado</b> dentro de "
        "<code>CALCULATE</code>, e a diferenca dividida pelo anterior. "
        "Esse e o arroz-com-feijao da inteligencia temporal.")
)

cad.section("variaveis-var", "VAR: variaveis em DAX para legibilidade e performance",
    p("Variaveis em DAX sao declaradas com <code>VAR</code>, usadas com "
      "<code>RETURN</code>, e valem dentro do escopo da medida. Sao "
      "essenciais para medidas densas e para performance.") +
    code(
        "% Atraso por Setor = \n"
        "VAR totalReq = COUNTROWS(Requisicoes)\n"
        "VAR reqAtrasadas = CALCULATE([Requisicoes], Requisicoes[em_atraso] = 1)\n"
        "RETURN DIVIDE(reqAtrasadas, totalReq, 0)",
        "DAX"
    ) +
    tbl(["Sem VAR", "Com VAR"],
        [["<code>DIVIDE(CALCULATE(COUNTROWS(T), T[flag]=1), COUNTROWS(T))</code>", "<code>VAR a=...; VAR t=...; RETURN DIVIDE(a,t)</code>"]],
        num_cols=[]) +
    aplicab(
        "<b>Quando</b> a expressao repete calculos ou testa condicoes.",
        "<code>VAR</code> calcula uma vez, guarda o valor, evita recalcular. "
        "Em medidas com varios <code>FILTER</code> ou <code>CALCULATE</code> "
        "aninhados, a economia e grande.",
        "Na POLITEC: ao calcular <i>TAT mediano e P90 de exames de DNA</i>, "
        "usamos <code>VAR base = FILTER(...)</code> para nao recalcular a base."
    )
)

cad.section("dax-padroes-uteis", "8 medidas que vao para todo dashboard",
    p("Estes sao os <b>padroes DAX</b> que voce vai copiar e colar para "
      "<b>todo</b> dashboard institucional da POLITEC:") +
    code(
        "Total Eventos = COUNTROWS(fato)\n"
        "Total Valor = SUMX(fato, fato[col1] * fato[col2])\n"
        "% Filtro = DIVIDE(CALCULATE([Total], dim[cat]=\"X\"), [Total], 0)\n"
        "Top N = CALCULATE([Total], TOPN(10, ALL(tab), [Total], DESC))\n"
        "Vs Mes Anterior = [Total] - CALCULATE([Total], DATEADD(cal[data], -1, MONTH))\n"
        "YTD = TOTALYTD([Total], cal[data])\n"
        "Mes Anterior = CALCULATE([Total], DATEADD(cal[data], -1, MONTH))\n"
        "Rank = RANKX(ALL(dim[cat]), [Total],, DESC)",
        "DAX"
    )
)

cad.section("dax-performatico", "Performance DAX: 6 regras para nao derrubar o .pbix",
    p("Dashboard institucional tem audiencia grande e filtro pesado. "
      "Cuide da performance agora, antes do .pbix virar um sapo.") +
    ul([
        "<b>1. Esquema estrela</b>: fatos cercadas por dimensoes planas. "
        "Evite snowflake ou tabelas grandes conectadas a fato.",
        "<b>2. Sem colunas calculadas desnecessarias</b>: cada coluna custa "
        "RAM do VertiPaq. Use medida quando puder.",
        "<b>3. Colunas que <i>precisam</i> existir na tabela</b>: chaves "
        "substitutas (ja criadas nos datasets da Aula 5), ano, mes, dia.",
        "<b>4. Filtros diretos</b> em vez de <code>FILTER</code> "
        "(<code>CALCULATE(T, T[col]=X)</code> otimiza melhor).",
        "<b>5. Evite <code>ALL()</code> sem proposito</b>: ele remove tudo e "
        "invalida segmentacoes uteis.",
        "<b>6. Agregations</b> (Power BI Premium) para tabelas com milhoes de linhas."
    ]) +
    callout("err", "Performance Analysis",
        "No Power BI Desktop: <b>Performance Analyzer</b> "
        "(menu Exibicao). Mostra <b>qual visual</b> demora, <b>qual "
        "medida DAX</b> esta lenta e <b>onde voce ganha performance</b> com "
        "uma coluna calculada ou uma aggregation.")
)

cad.section("dax-vs-calculated-column-resumo", "Resumo: a arvore de decisao DAX",
    tbl(["Pergunta", "Resposta"],
        [["E um calculo por linha da tabela?", "<b>Coluna calculada</b>"],
         ["E um calculo de agregacao?", "<b>Medida</b>"],
         ["Depende de slicer/filtro?", "<b>Medida</b>"],
         ["Sao poucos valores que nao mudam?", "<b>Coluna calculada</b>"],
         ["E comparacao com periodo anterior?", "<b>Medida</b> (com time intel)"],
         ["E total % sobre uma categoria?", "<b>Medida</b> + <code>CALCULATE</code> + <code>ALL</code>"]],
        num_cols=[]) +
    callout("tip", "Regra de ouro",
        "Quando voce estiver em duvida: comece tentando como <b>medida</b>. "
        "So materialize em coluna quando a performance pedir ou quando o valor "
        "for estatico por linha.")
)

# =================================================================
# PARTE 2 - MODULO 7 PARTE 2: SERVICE, SEGURANCA E GOVERNANCA
# =================================================================
cad.grp("Parte 2 - Service, Seguranca e Governanca",
        "Da planilha para a instituicao: dataflows, RLS, OLS, Apps avancado e Microsoft Fabric.")

cad.section("service-recap", "Power BI Service - o que voce ja conhece (Dia 4)",
    p("No Dia 4 voce viu que o <b>Power BI Service</b> e a nuvem da Microsoft "
      "onde os .pbix vivem. Ele guarda workspaces, datasets compartilhados, "
      "apps e dashboards mobile.") +
    flow_h([
        ("DESKTOP", "Cria o relatorio"),
        ("SERVICE", "Hospeda, governa, compartilha"),
        ("MOBILE", "Consome em qualquer lugar"),
        ("APPS", "Empacota para o usuario final"),
    ]) +
    p("Hoje o foco e o que vem <b>depois</b> do basico: seguranca por linha, "
      "dados compartilhados (dataflows) e a ponte para o ecossistema maior "
      "(Fabric, Power Platform).")
)

cad.section("dataflows", "Dataflows: um &quot;mini-Data Lake&quot; dentro do Power BI",
    p("Um <b>Dataflow</b> e uma tabela ou um conjunto de tabelas tratadas no "
      "Power BI Service (similar ao Power Query, mas na nuvem). Ele serve "
      "como fonte <b>compartilhada</b> entre varios .pbix, evitando que cada "
      "equipe faca sua propria copia do mesmo ETL.") +
    tbl(["Aspecto", "Power Query (no Desktop)", "Dataflow (no Service)"],
        [["Onde roda", "No seu .pbix", "No Service (nuvem Microsoft)"],
         ["Reaproveitamento", "So dentro do mesmo .pbix", "Entre varios .pbix"],
         ["Atualizacao", "Manual / agendada", "Agendada (mesmo gateway)"],
         ["Destino", "VertiPaq (in-memory)", "CDSA/ADLS (Lake)"],
         ["Quem mexe", "O autor do .pbix", "Admin do workspace"]],
        num_cols=[]) +
    aplicab(
        "<b>Quando</b> tres setores consomem o mesmo cadastro de peritos.",
        "<code>Dataflow</code> permite que o <b>setor de RH</b> mantenha o "
        "cadastro, e os <b>tres .pbix</b> (DNA, Toxicologia, Informatica) "
        "consomem da mesma fonte.",
        "Na POLITEC: o <b>cadastro de setores</b>, o <b>calendario oficial</b> "
        "e o <b>tabela de municipios MT</b> sao candidatos naturais a "
        "dataflow compartilhado."
    )
)

cad.section("datasets-compartilhados", "Datasets compartilhados (shared datasets)",
    p("Um <b>dataset compartilhado</b> e um modelo semantico publicado uma vez "
      "e consumido por varios relatorios (.pbix). O .pbix se conecta como "
      "<b>Live Connection</b> - <b>nao importa copia</b> dos dados.") +
    callout("note", "Vantagem",
        "Atualize os dados <b>uma vez</b> e todos os relatorios que dependem "
        "dele sao atualizados. Ideal para o painel da Diretoria: varios "
        "relatorios consomem o mesmo modelo estrela.") +
    callout("err", "Cuidado com a performance",
        "Um dataset compartilhado com schema confuso impacta todos os "
        "relatorios. <b>Governe antes de compartilhar</b>: documente o "
        "esquema, faca revisao de medidas, monitore queries.")
)

cad.section("rls", "RLS - Row-Level Security: cada usuario ve o que pode ver",
    p("<b>RLS (Row-Level Security)</b> filtra as linhas da tabela fato por "
      "usuario. E a forma mais natural de impedir que um perito de Cuiaba "
      "veja ocorrencias de Sinop, ou que o chefe do DNA veja requisicoes de "
      "Toxicologia.") +
    step([
        ("No Desktop: clique na tabela fato -> Gerenciamento de Funcoes",
         "Crie uma funcao DAX que receba o usuario (<code>USERPRINCIPALNAME()</code>) "
         "e devolva as linhas permitidas: <code>[perito_setor] = LOOKUPVALUE(...)</code>."),
        ("Teste no Desktop: Exibicao -> Exibir como -> Funcoes",
         "Simule o filtro de cada papel (Diretor x Chefe de Setor x Perito) "
         "<b>sem sair do Desktop</b>."),
        ("No Service: workspace -> Dataset -> Seguranca",
         "Adicione usuarios ou grupos de seguranca do AAD (Microsoft Entra) a "
         "cada papel criado."),
        ("Teste no Service",
         "Use &quot;Testar como papel&quot; para validar que o filtro esta "
         "realmente restringindo."),
    ]) +
    code(
        "// Funcao RLS para a tabela fato Requisicoes\n"
        "RequisicoesSeguranca = \n"
        "FILTER(\n"
        "    Requisicoes,\n"
        "    IF(\n"
        "        USERPRINCIPALNAME() = \"diretor@politec.mt.gov.br\",\n"
        "        TRUE(),\n"
        "        Requisicoes[setor_key] IN\n"
        "            FILTER(\n"
        "                VALUES(dim_perito),\n"
        "                dim_perito[perito] = USERPRINCIPALNAME()\n"
        "            )\n"
        "    )\n"
        ")",
        "DAX (RLS)"
    ) +
    callout("purple", "Regra de ouro do RLS",
        "Cada filtro de RLS e um <b>grupo de seguranca do Microsoft Entra</b> "
        "(AD). Nao use logins individuais: quando o perito sair do setor, "
        "voce so precisa remove-lo do grupo.")
)

cad.section("ols", "OLS - Object-Level Security: esconde a coluna inteira",
    p("<b>OLS</b> esconde a <b>coluna</b> ou a <b>tabela</b> inteira para "
      "determinados usuarios. E o complemento do RLS: RLS esconde linhas, "
      "OLS esconde atributos.") +
    tbl(["Aspecto", "RLS", "OLS"],
        [["O que esconde", "<b>Linhas</b> da tabela (mantem a coluna)", "<b>Colunas/tabelas</b> inteiras"],
         ["Quando usar", "Usuario A ve dados do setor X, B ve setor Y", "Coluna de CPF so para RH"],
         ["Configuracao", "Gerenciar funcoes na tabela", "No Service: Modelo -> Seguranca -> OLS"],
         ["Sinal visual", "O <i>campo</i> continua visivel", "O <i>campo</i> desaparece do .pbix"]],
        num_cols=[]) +
    aplicab(
        "<b>Quando</b> o diretor financeiro <b>nao pode</b> ver o CPF do "
        "perito.",
        "<b>OLS</b> retira a coluna do painel. <b>RLS</b> nao da - ele "
        "esconde apenas as linhas.",
        "Na POLITEC: <i>o chefe da Diretoria de Identificacao nao ve <b>o "
        "endereco da vitima</b> nas ocorrencias</i>. Use OLS na coluna "
        "<code>vitima_endereco</code>."
    )
)

cad.section("rls-vs-ols", "RLS x OLS: usar em conjunto",
    p("RLS e OLS nao competem. RLS esconde <b>linhas</b>, OLS esconde "
      "<b>colunas</b>. Em um dashboard institucional, os dois convivem:") +
    flow_h([
        ("Diretor", "RLS: tudo / OLS: tudo"),
        ("Chefe Setor", "RLS: seu setor / OLS: sem dados pessoais"),
        ("Perito", "RLS: seus exames / OLS: sem CPF / sem vitima"),
        ("Auditor", "RLS: tudo / OLS: tudo (read-only)"),
    ])
)

cad.section("apps-avancado", "Apps: o pacote final para o usuario",
    p("Um <b>App</b> e um pacote de dashboards, relatorios e datasets "
      "compartilhados para um <b>publico-alvo</b>. O usuario final so ve os "
      "dashboards que o App libera - sem ver o workspace nem os .pbix "
      "intermediarios.") +
    step([
        ("No Service: workspace -> Criar App",
         "De um nome ao App (ex: <i>Painel do Perito</i>), adicione uma descricao."),
        ("Adicione os dashboards que vao compor o App",
         "Pode-se escolher quais abas ou dashboards publicar."),
        ("Defina o publico",
         "<b>Toda a organizacao</b>, <b>grupos especificos de "
        "seguranca</b> ou usuarios individuais."),
        ("Publique",
         "Atualizacao do App e manual (ou via pipeline). Quando o .pbix "
         "atualiza no workspace, clique &quot;Atualizar App&quot; para publicar "
         "a nova versao."),
    ])
)

cad.section("deployment-pipelines", "Deployment Pipelines: dev -> test -> prod",
    p("<b>Deployment Pipelines</b> automatizam o caminho entre "
      "<b>desenvolvimento</b>, <b>teste</b> e <b>producao</b>. Sao o "
      "&quot;git do Power BI&quot;: cada estagio tem seu workspace, e os "
      "artefatos vao sendo promovidos.") +
    flow_h([
        ("DEV", "desenvolvedor mexe"),
        ("TEST", "homologacao com usuarios"),
        ("PROD", "publicado, governado"),
    ]) +
    aplicab(
        "<b>Quando</b> o analista cria/atualiza um dashboard.",
        "<code>DEV -> TEST -> PROD</code>: cada estagio tem seu workspace. "
        "Diff mostra o que mudou. Promotion pede confirmacao.",
        "Na POLITEC: <i>o estagiario de TI cria no DEV; o chefe da TI revisa "
        "no TEST; o diretor homologa no PROD.</i>"
    )
)

cad.section("data-gateway-avancado", "Data Gateway: a ponte local-nuvem",
    p("O <b>On-premises Data Gateway</b> e um servico que roda em uma "
      "maquina dentro da rede da POLITEC e traduz os pedidos do Service "
      "para os bancos de dados locais (SQL Server, Oracle, MySQL, pastas de "
      "rede).") +
    tbl(["Modo", "Quando usar", "Limite"],
        [["<b>Personal</b>", "Um usuario, uma maquina, fontes locais", "Sem escalabilidade (nuvem pessoal)"],
         ["<b>Standard</b>", "Varios .pbix, varios usuarios", "Indicado para orgaos publicos medios"],
         ["<b>Dataflow</b>", "Para dataflows do Service", "Especifico para o Power BI Service"],
         ["<b>Virtual network (VNet)</b>", "Azure-only", "Mais seguro (rede virtual)"]],
        num_cols=[]) +
    callout("tip", "Onde instalar o gateway",
        "Instale em uma <b>maquina dedicada</b>, com fonte de energia "
        "redundante e monitoracao. Quando o gateway cai, todo o servico cai - "
        "e os dashboards ficam mostrando &quot;dados nao disponiveis&quot;.")
)

cad.section("power-platform", "Power Platform: o ecossistema alem do BI",
    p("O Power BI e parte de um ecossistema maior: a <b>Power Platform</b> "
      "da Microsoft. Conheca as pecas adjacentes:") +
    tbl(["Ferramenta", "Serve para", "Conexao com Power BI"],
        [["<b>Power Apps</b>", "Apps low-code (formularios, coleta)", "Painel Power BI com botao para abrir app"],
         ["<b>Power Automate</b>", "Fluxos automatizados (aprovacao, alerta)", "Dispara fluxo quando KPI violado"],
         ["<b>Power Virtual Agents</b>", "Chatbots para autoatendimento", "Embed no App"],
         ["<b>Power Pages</b>", "Sites externos com dados do Power BI", "Publica dashboards no portal do cidadao"]],
        num_cols=[]) +
    aplicab(
        "<b>Quando</b> o diretor quer um botao no painel para abrir uma "
        "<b>solicitacao de orcamento</b>.",
        "<code>Power Automate</code> cria o fluxo. <code>Power Apps</code> "
        "cria o formulario. <code>Power BI</code> mostra o botao na tela. Os "
        "tres convivem.",
        "Na POLITEC: <i>quando o chefe de seto ve um KPI em vermelho, "
        "clica em &quot;Acionar Investigacao&quot; e abre um Power Apps "
        "pre-preenchido com o contexto.</i>"
    )
)

cad.section("fabric-intro", "Microsoft Fabric: o guarda-chuva de dados",
    p("<b>Microsoft Fabric</b> e a plataforma <b>unificada</b> de dados da "
      "Microsoft. Reune OneLake (lake comum), Data Factory (ETL), Synapse "
      "(DW), Power BI e Data Activator em um unico tenant. O Power BI "
      "passa a ser &quot;uma das pecas&quot; do Fabric.") +
    callout("note", "Por que importa",
        "Mesmo que a POLITEC nao adote Fabric amanha, vale saber que o "
        "<b>esquema estrela</b>, o <b>DAX</b> e o <b>RLS</b> que voce esta "
        "aprendendo <b>continuam valendo</b> dentro do Fabric - eles sao "
        "transferiveis.")
)

cad.section("bi-lgpd-recap", "BI e LGPD (recap rapido)",
    p("A LGPD continua valendo. Em qualquer publicacao, garanta:") +
    checklist([
        "Colunas com dados pessoais <b>ocultas</b> (via OLS) ou <b>anonimizadas</b>.",
        "<b>Logs de acesso</b> ativos no Service (auditoria).",
        "<b>Retencao</b> dos dados conforme politica institucional.",
        "<b>RLS</b> ativa para limitar quem ve o que.",
        "Em caso de vazamento, <b>ANPD notificada em ate 72h</b>.",
    ])
)

cad.section("bi-sustentavel", "BI institucional sustentavel: as 5 praticas",
    p("Para garantir que o BI nao morra com a rotatividade, adote cinco "
      "praticas:") +
    tbl(["Pratica", "Por que"],
        [["<b>Documentacao dos modelos</b>", "Quem chega depois entende o que ha por tras"],
         ["<b>Definicao de papel oficial</b>", "Cada um sabe quem mantem o que"],
         ["<b>Agenda de atualizacao</b>", "Nunca confundimos 'atual' com 'de hoje'"],
         ["<b>Revisao de acessos trimestral</b>", "Ex-peritos nao continuam com RLS ampla"],
         ["<b>Reuniao mensal de feedback</b>", "Usuarios apontam o que precisa melhorar"]],
        num_cols=[]) +
    callout("purple", "A pergunta-chave para manter o BI vivo",
        "Se o analista que construiu o painel sair, alguem assume? Se a "
        "resposta for 'nao sei', o BI esta em risco. <b>Documente e "
        "compartilhe</b> - o ecosistema sustenta a pessoa, nao o contrario.")
)

# =================================================================
# PARTE 3 - PRATICA GUIADA (7 LABS)
# =================================================================
cad.grp("Parte 3 - Pratica Guiada",
        "Sete labs que separam Desktop, Service, DAX e publicacao.")

cad.section("labs-intro", "Os 7 labs desta aula",
    p("Os labs desta aula vao do <b>plano em branco</b> ate a <b>publicacao "
      "com governanca</b>. Cada laboratorio corresponde a uma secao do "
      "capitulo: comece pelo Lab 1 e va avancando. Ao final do Lab 5 voce "
      "tera o esqueleto do projeto integrador.") +
    tbl(["Lab", "Foco", "Aba / area", "Tempo sugerido"],
        [["<b>1</b>", "Importar 2-3 datasets com Obter Dados/Pasta", "Modelo de dados", "30 min"],
         ["<b>2</b>", "Relacionamentos e cardinalidade", "Modelo", "20 min"],
         ["<b>3</b>", "Tabela de medidas (DAX basicas)", "Reutilizavel", "30 min"],
         ["<b>4</b>", "Time intelligence (YTD, MoM, YoY)", "Aba do projeto", "30 min"],
         ["<b>5</b>", "Formatacao condicional e KPIs", "Aba do projeto", "30 min"],
         ["<b>6</b>", "RLS - teste no Desktop e Service", "Aba restrita", "30 min"],
         ["<b>7</b>", "Publicar e distribuir via App", "Service + Mobile", "30 min"]],
        num_cols=[]) +
    callout("tip", "Como escolher quais cenarios usar",
        "Nos labs, use <b>os 2-3 datasets que voce decidiu abraçar</b> no "
        "projeto integrador (ver Parte 5). Manter um unico .pbix por lab.")
)

cad.section("lab1-importar", "Lab 1 - Importar 2 ou 3 datasets com Obter Dados -> Pasta",
    p("Vamos abrir o Power BI Desktop do zero e importar os datasets da "
      "Aula 5.") +
    step([
        ("Crie um novo arquivo <code>.pbix</code>",
         "Power BI Desktop -> Novo. Salve como <code>Projeto_Integrador.pbix</code>."),
        ("Obter Dados -> Pasta",
         "No friso inicial, clique em <b>Obter Dados</b> -> <b>Pasta</b> "
         "(do Excel)."),
        ("Selecione a pasta da Aula 5/datasets/ completa",
         "O Power BI vai listar todos os CSVs. <b>Selecione apenas</b> os que "
         "correspondem aos cenarios que voce escolheu (ex.: cenario1_backlog + "
         "cenario3_criminalidade + cenario4_orcamento)."),
        ("Combine e transforme",
         "Marque <b>Combinar e Transformar</b>. O Power BI abre o Power Query "
         "com todas as tabelas. Revise os tipos e clique <b>Fechar e Aplicar</b>."),
        ("Verifique tipos",
         "Na aba Dados, garanta: <code>data_key</code> como numero inteiro, "
         "<code>nome_mes</code> como texto, <code>valor_*</code> como decimal."),
    ]) +
    callout("err", "Erro comum",
        "<b>Dim_calendario duplicada</b>: se voce importou <i>tres pastas de "
        "cenario</i>, ganhara <i>tres</i> tabelas <code>dim_calendario</code>. "
        "Mantenha so uma (ou use sufixos). Veja o passo a passo em "
        "<code>cenario5_custodia/README.md</code>.")
)

cad.section("lab2-relacionamentos", "Lab 2 - Relacionamentos e cardinalidade",
    p("Com os dados importados, vamos montar o modelo. Esta e a secao mais "
      "importante de qualquer .pbix: se o modelo estiver errado, nenhuma "
      "medida vai funcionar direito.") +
    step([
        ("Abra a aba <b>Modelo</b> (icone de relacionamento)",
         "Voce vera as tabelas. Arraste cada <code>setor_key</code>, "
         "<code>perito_key</code>, etc., para sua dimensao correspondente."),
        ("Peca a cardinalidade certa",
         "<code>fato (N) -> dim (1)</code>. Power BI detecta automaticamente, "
         "mas confira: <b>direcao do filtro</b> sempre <i>unica</i> "
         "(de fato para dim)."),
        ("Tabela de datas",
         "Em cada <code>dim_calendario</code>: clique direito -> <b>Marcar "
         "como tabela de datas</b>. Confirme se a coluna chave e <code>data</code>."),
        ("Esconda as colunas tecnicas",
         "Na visualizacao Tabela (modo Dados), oculte todas as colunas "
         "<code>*_key</code> para que aparecam somente os rotulos nas tabelas.")
    ]) +
    callout("tip", "Por que ocultar chaves?",
        "Quando o usuario final cria um visual de tabela, as chaves (1, 2, "
        "3...) aparecem junto com os rotulos. Ocultar as chaves faz o visual "
        "mostrar <i>so os rotulos</i>, diminuindo confusao visual e vazamento "
        "de modelo.")
)

cad.section("lab3-medidas-basicas", "Lab 3 - Tabela de medidas (DAX basicas)",
    p("Crie uma <b>Tabela de Medidas</b> para centralizar o DAX. E a melhor "
      "pratica do mercado:") +
    step([
        ("Nova tabela de medidas",
         "Em <b>Dados</b> (ou <b>Modelagem</b>): <b>Nova Tabela</b> com "
         "formula <code>Medidas = ROW(\"Medidas\", BLANK())</code>."),
        ("Crie as medidas base",
         "Cada medida fica dentro dessa tabela. Exemplos: <code>Total "
         "Eventos = COUNTROWS(Requisicoes)</code>, <code>Total Valor = "
         "SUM(Requisicoes[valor_causa])</code>."),
        ("Formate as medidas",
         "Cada medida tem um formato (%, moeda, numero inteiro) e uma pasta "
         "de Exibicao: clique na medida -> <b>Exibicao do Modelo</b> -> pasta "
         "(ex.: <i>KPIs</i>)."),
        ("Documente",
         "Use a descricao da medida (<b>Exibicao do Modelo -> Descricao</b>) "
         "para contar a historia: <i>&quot;Total de requisicoes em qualquer "
         "status, recalculado por slicer.&quot;</i>")
    ]) +
    code(
        "Total Requisicoes = COUNTROWS(Requisicoes)\n"
        "Total Valor Causa = SUMX(\n"
        "    FILTER(Requisicoes, NOT(ISBLANK(Requisicoes[valor_causa]))),\n"
        "    Requisicoes[valor_causa]\n"
        ")\n"
        "Requisicoes Atrasadas = CALCULATE([Total Requisicoes], Requisicoes[em_atraso] = 1)",
        "DAX"
    )
)

cad.section("lab4-time-intelligence", "Lab 4 - Time intelligence (YTD, MoM, YoY)",
    p("Agora que temos as medidas base, vamos <b>comparar com o tempo</b>.") +
    step([
        ("Confirme a tabela de datas",
         "Lab 2: <code>dim_calendario</code> marcada como tabela de datas."),
        ("Crie as medidas",
         "<code>YTD = TOTALYTD([Total Requisicoes], dim_calendario[data])</code>, "
         "<code>MoM % = DIVIDE([Total Requisicoes] - [Mes Anterior], [Mes Anterior])</code>."),
        ("Insira em um visual de linha",
         "Eixo: <code>dim_calendario[data]</code> (mes/ano). Valores: "
         "<code>YTD</code> + <code>Total Requisicoes</code>. Observe o "
         "&quot;cume&quot; anual."),
        ("Slicer por periodo",
         "Adicione slicer de Ano-Mes. Teste o efeito das medidas comparativas."),
    ]) +
    callout("purple", "Por que time intel retorna vazio",
        "<b>Causa #1</b>: a tabela de datas nao foi marcada (Lab 2). "
        "<b>Causa #2</b>: a coluna usada como eixo nao e a coluna chave "
        "(<code>data</code>) da dim_calendario."
    )
)

cad.section("lab5-kpi-condicional", "Lab 5 - KPIs com formatacao condicional",
    p("KPIs sao a alma do dashboard institucional. Vamos deixa-los gritar "
      "quando o numero esta ruim.") +
    step([
        ("Insira um visual de Cartao (KPI)",
         "Categoria: <code>dim_setor[setor]</code>. Valor: <code>% Atraso</code>. "
         "Indicador: <code>Requisicoes Atrasadas</code>."),
        ("Formate como porcentagem",
         "<b>Formato -> Porcentagem</b>, com 1 casa decimal."),
        ("Adicione formatacao condicional",
         "Em Formatacao -> Cor de Fundo: regras ->"
         "<code>&lt; 10% verde / 10%-20% amarelo / &gt; 20% vermelho</code>."),
        ("Adicione icones (opcional)",
         "Formatacao -> Rotulos (ou Icones): setas de tendencia para indicar "
         "se o indicador subiu ou caiu em relacao ao mes anterior."),
    ]) +
    antesdepois(
        "Cartoes que mostram so o numero - sem cor, sem icones, sem "
        "contexto.",
        "Cartoes que <b>destacam o risco</b>: verde (saudavel), amarelo "
        "(atencao), vermelho (alerta), com icone de seta e comparacao com "
        "mes anterior.",
        errado="Escondido",
        certo="Evidente"
    )
)

cad.section("lab6-rls", "Lab 6 - RLS - teste no Desktop e Service",
    p("RLS e o laboratorio de <b>seguranca</b>. Mesmo no dataset sintetico da "
      "Aula 5, exercite o fluxo.") +
    step([
        ("Desktop: gerencie a funcao RLS",
         "Clique na tabela <code>fato</code>. Em <b>Modelagem -> Gerenciar "
         "Seguranca</b>, crie <code>SetorCuiaba</code> que filtre por um setor "
         "ficticio."),
        ("Teste em Desktop",
         "<b>Exibicao -> Mostrar como Funcoes</b> -> selecione "
         "<code>SetorCuiaba</code>. Veja o painel mudar."),
        ("Publique o .pbix no Service",
         "<b>Publicar</b> -> selecione um workspace."),
        ("Service: configure a seguranca",
         "No workspace -> Dataset -> <b>Seguranca</b> -> Adicione um usuario "
         "ou grupo a <code>SetorCuiaba</code>. Confirme."),
        ("Teste no Service",
         "Abra o relatorio com 'Testar como papel' - ve apenas os registros "
         "do setor."),
    ]) +
    callout("err", "RLS nao funciona - por que?",
        "<b>1.</b> Esqueca de marcar a tabela fato como a que tem a funcao. "
        "<b>2.</b> Esconderam a dimensao, mas RLS depende dela estar visivel. "
        "<b>3.</b> A funcao usa <code>FILTER</code> com ALL() no lugar "
        "errado. <b>4.</b> Multiplos papeis nao estao em ordem.")
)

cad.section("lab7-publicar-app", "Lab 7 - Publicar e distribuir via App",
    p("Ultimo laboratorio: tirar o painel do Desktop e levar para o "
      "Service, com governanca.") +
    step([
        ("Antes de publicar",
         "Confira o checklist da Aula 4: dimensoes ok, RLS ok, paginas nomeadas, "
         "Ultima Atualizacao visivel."),
        ("Publicar",
         "<b>Publicar</b> -> selecione workspace -> <b>OK</b>."),
        ("Workspace -> Criar App",
         "<b>Novo App</b> -> de um nome. Adicione os dashboards/abas para o "
         "App. Publique."),
        ("Teste o App",
         "Abra o link do App como usuario comum (<code>..@politec.mt.gov.br</code>). "
         "Verifique: slicers funcionam? RLS se aplica?"),
        ("Monitore atualizacoes",
         "Workspace -> Dataset -> <b>Atualizar Agora</b> para validar. Em "
         "producao, use atualizacao agendada (a cada 6h ou diaria)."),
    ]) +
    callout("tip", "Atalhos para o Service",
        "<b>Shift + clique</b> numa pinea do App para abrir no modo "
        "<i>Tela Cheia</i> (modo quiosque). Use em reunioes ou projetores."
    )
)

# =================================================================
# PARTE 4 - 5 CENARIOS COM DATASETS PROPRIOS
# =================================================================
cad.grp("Parte 4 - Cenarios com datasets proprios",
        "Cinco cenarios tematicos, cada um com seu star schema limpo e >=1000 linhas. O aluno escolhe tres.")

cad.section("p4-intro", "Cinco cenarios - cinco temas para o seu painel",
    p("Para cada cenario voce tera:") +
    ul([
        "<b>Dataset sintetico</b> (modelo estrela, em <code>datasets/cenarioN_*/</code>).",
        "<b>Problema de gestao</b> realista da POLITEC/MT.",
        "<b>Sugestoes de visuais</b> que funcionam bem para aquela aba.",
        "<b>Numeros de referencia</b> que aparecem no dataset.",
    ]) +
    p("O projeto integrador (Parte 5) solicita que voce construa "
      "<b>pelo menos 3 abas</b>. Escolha os 3 cenarios que mais combinam "
      "com a sua realidade.") +
    grid2([
        ("\U0001f4c9 Cenario 1 - Backlog de Pericias",
         "Operacional: filas, TAT, peritos sobrecarregados. Requisicao por "
         "requisicao (1200 linhas)."),
        ("\U0001f9ec Cenario 2 - TAT do Laboratorio de DNA",
         "Laboratorio: tempo de turnaround por metodologia, kit e laboratorio."),
        ("\U0001f5fa Cenario 3 - Mapa da Criminalidade em MT",
         "Inteligencia geografica: municipios, tipos de crime, faixa etaria."),
        ("\U0001f4b0 Cenario 4 - Orcamento e Contratos",
         "Financeiro: empenho x dotacao, fornecedores, contratos vigentes."),
        ("\U0001f50d Cenario 5 - Cadeia de Custodia",
         "Logistica processual: coleta, transporte, armazenamento, baixa.")
    ])
)

# ---------- CENARIO 1 ----------
cad.section("p4-cenario1-necessidade", "Cenario 1 - A necessidade: zerando o backlog",
    p("O diretor pergunta: <i>&quot;Onde estao os gargalos? Quem esta "
      "atrasado? Qual perito precisa de reforco?&quot;</i>") +
    aplicab(
        "<b>Quando</b> o chefe da Diretoria Tecnica precisa de um relatorio "
        "semanal de backlog.",
        "<b>Por que</b> um dashboard institucionaliza a visibilidade: nao "
        "depende do Excel do analista.",
        "<b>Exemplo</b> na POLITEC: <i>relatorio semanal com os 10 laudos "
        "mais atrasados; TAT por setor; peritos com maior backlog.</i>"
    ) +
    callout("tip", "Onde encontrar",
        "<code>datasets/cenario1_backlog/</code> - fato_requisicoes.csv com "
        "1200 registros, 12 peritos e 16 delegacias.")
)

cad.section("p4-cenario1-dados", "Cenario 1 - O dataset (1200 requisicoes)",
    tbl(["Tabela", "Linhas", "Foco"],
        [["<code>fato_requisicoes</code>", "1.200", "Cada requisicao pericial (1 linha = 1 caso)"],
         ["<code>dim_setor</code>", "8", "DNA, Toxicologia, Balistica, IML, ..."],
         ["<code>dim_perito</code>", "12", "Nome, especialidade, setor"],
         ["<code>dim_tipo_exame</code>", "8", "DNA, Necropsia, Balistica, ..."],
         ["<code>dim_delegacia</code>", "16", "Delegacias de MT"],
         ["<code>dim_prioridade</code>", "3", "Alta / Media / Baixa"],
         ["<code>dim_status</code>", "5", "Triagem / Em Analise / Em Revisao / Concluido / Arquivado"],
         ["<code>dim_calendario</code>", "1.096", "2023-01-01 a 2025-12-31"]],
        num_cols=[]) +
    callout("note", "Campo a observar",
        "<code>em_atraso</code> ja vem calculada: 1 se "
        "<code>dias_uteis &gt; prazo_legal</code>, 0 caso contrario. "
        "E a coluna-chave para o KPI de <b>atraso</b> da aba."
    )
)

cad.section("p4-cenario1-visuais", "Cenario 1 - Sugestoes de visuais para a aba de Backlog",
    ul([
        "<b>Cartao (KPI)</b>: total de requisicoes em atraso (com formatacao "
        "condicional verde / amarelo / vermelho).",
        "<b>Colunas agrupadas</b>: backlog por Setor, filtrando "
        "<code>status &lt;&gt; &quot;Concluido&quot;</code>.",
        "<b>Linha temporal</b>: TAT medio mensal por Setor (mediana, via medida DAX).",
        "<b>Matriz</b>: cruzamento <code>setor x tipo_exame</code> com "
        "<code>% atrasadas</code> (DRE).",
        "<b>Tabela de detalhe</b>: Top 10 requisicoes atrasadas (drill through).",
        "<b>Slicer</b>: <code>prioridade</code>, <code>data_entrada</code>, "
        "<code>delegacia</code>, <code>tipo_exame</code>."
    ]) +
    code(
        "% Atraso = DIVIDE(\n"
        "    CALCULATE([Total Requisicoes], Requisicoes[em_atraso] = 1),\n"
        "    [Total Requisicoes]\n"
        ")\n"
        "TAT Mediano = MEDIANX(Requisicoes, Requisicoes[dias_uteis])",
        "DAX"
    )
)

cad.section("p4-cenario1-medidas", "Cenario 1 - Medidas DAX uteis",
    code(
        "Requisicoes Abertas = CALCULATE(\n"
        "    COUNTROWS(Requisicoes),\n"
        "    Requisicoes[status] IN {\"Aguardando Triagem\", \"Em Analise\", \"Em Revisao\"}\n"
        ")\n"
        "TAT Medio = AVERAGEX(Requisicoes, Requisicoes[dias_uteis])\n"
        "% no Prazo = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(Requisicoes), Requisicoes[em_atraso] = 0),\n"
        "    COUNTROWS(Requisicoes)\n"
        ")\n"
        "Top 10 Atrasadas = TOPN(10, Requisicoes, Requisicoes[dias_uteis], DESC)",
        "DAX"
    )
)

# ---------- CENARIO 2 ----------
cad.section("p4-cenario2-necessidade", "Cenario 2 - A necessidade: diagnostico do DNA",
    p("A coordenadoria de DNA recebe a meta de <b>90 dias</b> por exame. "
      "Onde esta o gargalo? E por <b>metodologia</b> ou por "
      "<b>laboratorio</b>? E a <b>qualidade da amostra</b> esta piorando?") +
    aplicab(
        "<b>Quando</b> a coordenadoria do DNA precisa monitorar a meta de 90 dias.",
        "<b>Por que</b> o tempo de cada exame exige comparacao com o mesmo "
        "periodo do ano anterior (sazonalidade).",
        "<b>Exemplo</b> na POLITEC: <i>exames STR com mtDNA sao mais lentos. "
        "Na amostra Baixa, 30% tem Amostra Insuficiente. Monitorar "
        "calibra o SL.</i>"
    ) +
    callout("tip", "Onde encontrar",
        "<code>datasets/cenario2_dna/</code> - fato_exames_dna.csv com "
        "1100 registros, 4 laboratorios e 14 analistas.")
)

cad.section("p4-cenario2-dados", "Cenario 2 - O dataset (1100 exames)",
    tbl(["Tabela", "Linhas", "Foco"],
        [["<code>fato_exames_dna</code>", "1.100", "Cada exame de DNA"],
         ["<code>dim_laboratorio</code>", "4", "Cuiaba Central, Rondonopolis, Sinop, Varzea Grande"],
         ["<code>dim_metodologia</code>", "5", "STR, Y-STR, mtDNA, SNPs, NGS"],
         ["<code>dim_analista</code>", "14", "Peritos analistas"],
         ["<code>dim_status_exame</code>", "6", "Coleta, Extracao, Amplificacao, Analise, Concluido, Insuficiente"],
         ["<code>dim_kit_reagente</code>", "12", "Kit, marca, lote"],
         ["<code>dim_calendario</code>", "1.096", "Datas de recebimento e conclusao"]],
        num_cols=[]) +
    callout("note", "Campo a observar",
        "<code>tat_dias</code> ja vem calculado. Vacile com preenchimentos "
        "vazios em exames nao concluidos."
    )
)

cad.section("p4-cenario2-visuais", "Cenario 2 - Sugestoes de visuais para a aba de TAT do DNA",
    ul([
        "<b>Cartao (KPI)</b>: TAT medio (geral), TAT mediano, % exames "
        "concluidos em ate 90 dias.",
        "<b>Histograma ou Boxplot nativo</b>: distribuicao do "
        "<code>tat_dias</code>.",
        "<b>Linha temporal</b>: TAT mensal por laboratorio (4 series).",
        "<b>Pareto</b>: concentracao de metodologias (qual responde por 80%).",
        "<b>Heatmap ou Tabela cruzada</b>: laboratorio x status.",
        "<b>Slicer</b>: periodo, laboratorio, metodologia, status."
    ]) +
    code(
        "TAT Medio = AVERAGE(Exames[tat_dias])\n"
        "TAT Mediano = MEDIAN(Exames[tat_dias])\n"
        "% na Meta = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(Exames), Exames[tat_dias] <= 90),\n"
        "    COUNTROWS(Exames)\n"
        ")\n"
        "TAT MoM = DIVIDE([TAT Medio] - [TAT Mes Anterior], [TAT Mes Anterior])",
        "DAX"
    )
)

cad.section("p4-cenario2-medidas", "Cenario 2 - Medidas DAX uteis",
    code(
        "% Amostra Baixa = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(Exames), Exames[qualidade] = \"Baixa\"),\n"
        "    COUNTROWS(Exames)\n"
        ")\n"
        "Exames por Laboratorio = CALCULATE(COUNTROWS(Exames), ALLEXCEPT(Exames, dim_laboratorio))\n"
        "Kit Mais Usado = TOPN(1, VALUES(dim_kit[kit]), COUNTROWS(Exames), DESC)",
        "DAX"
    )
)

# ---------- CENARIO 3 ----------
cad.section("p4-cenario3-necessidade", "Cenario 3 - A necessidade: mapa da criminalidade",
    p("O IML e a Diretoria de Inteligencia precisam de um olhar "
      "<b>geografico</b>: onde a criminalidade se concentra? Em que "
      "<b>horario</b>? Com qual arma?") +
    aplicab(
        "<b>Quando</b> a Diretoria de Inteligencia prepara o boletim mensal.",
        "<b>Por que</b> a concentracao geografica muda a alocacao de peritos "
        "e o planejamento operacional.",
        "<b>Exemplo</b> na POLITEC: <i>Cuiaba e Varzea Grande concentram 36% "
        "dos robos de veiculo; 60% dos homicidios a partir das 18h.</i>"
    ) +
    callout("tip", "Onde encontrar",
        "<code>datasets/cenario3_criminalidade/</code> - "
        "fato_ocorrencias.csv com 1500 registros em 18 municipios MT.")
)

cad.section("p4-cenario3-dados", "Cenario 3 - O dataset (1500 ocorrencias)",
    tbl(["Tabela", "Linhas", "Foco"],
        [["<code>fato_ocorrencias</code>", "1.500", "Cada BO / ocorrencia"],
         ["<code>dim_municipio</code>", "18", "Municipios-polo de MT"],
         ["<code>dim_tipo_crime</code>", "7", "Homicidio, Roubo, Furto, Estupro, ..."],
         ["<code>dim_arma</code>", "6", "Fogo, Branca, Artesanal, Veiculo, ..."],
         ["<code>dim_faixa_etaria</code>", "6", "0-11, 12-17, 18-24, 25-39, 40-59, 60+"],
         ["<code>dim_periodo_dia</code>", "4", "Madrugada, Manha, Tarde, Noite"],
         ["<code>dim_calendario</code>", "1.096", "Datas das ocorrencias"]],
        num_cols=[]) +
    callout("note", "Flags uteis",
        "<code>flag_latrocinio</code>: 1 se o crime foi em resistencia "
        "seguida de morte. <code>flag_flagrante</code>: 1 se houve prisao em "
        "flagrante. Ambas vao para KPIs.")
)

cad.section("p4-cenario3-visuais", "Cenario 3 - Sugestoes de visuais para a aba de Mapa Criminal",
    ul([
        "<b>Mapa Preenchido (Shape Map)</b>: ocorrencias por municipio, "
        "densidade por cor.",
        "<b>Linha temporal</b>: serie diaria ou mensal com pico de sazonalidade.",
        "<b>Colunas empilhadas 100%</b>: tipo de crime x arma.",
        "<b>Piramide etaria</b>: vitimas por faixa etaria e genero (se tiver).",
        "<b>Heatmap de calendario</b>: dia da semana x periodo do dia.",
        "<b>Cartoes KPI</b>: total de vitimas, latrocinios, % flagrante.",
        "<b>Slicer</b>: ano, municipio, tipo, arma."
    ]) +
    code(
        "Ocorrencias = COUNTROWS(Ocorrencias)\n"
        "Vitimas = SUM(Ocorrencias[qtd_vitimas])\n"
        "% Flagrante = DIVIDE(\n"
        "    CALCULATE([Ocorrencias], Ocorrencias[flag_flagrante] = 1),\n"
        "    [Ocorrencias]\n"
        ")\n"
        "Ocorrencias YoY = CALCULATE([Ocorrencias], SAMEPERIODLASTYEAR(dim_calendario[data]))",
        "DAX"
    )
)

cad.section("p4-cenario3-medidas", "Cenario 3 - Medidas DAX uteis",
    code(
        "% Arma de Fogo = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(Ocorrencias), Ocorrencias[arma] = \"Arma de Fogo\"),\n"
        "    [Ocorrencias]\n"
        ")\n"
        "% Roubo Veiculo = DIVIDE(\n"
        "    CALCULATE([Ocorrencias], Ocorrencias[tipo] = \"Roubo de Veiculo\"),\n"
        "    [Ocorrencias]\n"
        ")\n"
        "Taxa por 100k = DIVIDE([Ocorrencias], SUM(dim_municipio[populacao_aprox])) * 100000",
        "DAX"
    )
)

# ---------- CENARIO 4 ----------
cad.section("p4-cenario4-necessidade", "Cenario 4 - A necessidade: orcamento sob pressao",
    p("Cada ano, a diretoria precisa justificar a contratacao de peritos e "
      "a compra de reagentes com evidencia:") +
    aplicab(
        "<b>Quando</b> o chefe da Administracao prepara a defesa do orcamento.",
        "<b>Por que</b> a instituicao que mostra <b>execucao</b> recebe mais "
        "que a que mostra <b>so orcado</b>.",
        "<b>Exemplo</b> na POLITEC: <i>custeio: 8% cancelado e 30% nao "
        "pago indica cadeira burocratica - e a <b>lead time</b> esta alta.</i>"
    ) +
    callout("tip", "Onde encontrar",
        "<code>datasets/cenario4_orcamento/</code> - "
        "fato_empenhos.csv com 1300 empenhos + fato_dotacao.csv com 240 dotacoes."
    )
)

cad.section("p4-cenario4-dados", "Cenario 4 - O dataset (1300 empenhos)",
    tbl(["Tabela", "Linhas", "Foco"],
        [["<code>fato_empenhos</code>", "1.300", "Cada nota de empenho"],
         ["<code>fato_dotacao</code>", "240", "Dotacao anual por setor x rubrica"],
         ["<code>dim_contrato</code>", "80", "Tipo, objeto, vigencia, valor, fornecedor"],
         ["<code>dim_fornecedor</code>", "50", "CNPJ, porte, municipio/UF"],
         ["<code>dim_rubrica</code>", "10", "Codigo + rotulo + grupo (custeio/investimento)"],
         ["<code>dim_modalidade</code>", "6", "Pregao, Concorrencia, Dispensa, ..."],
         ["<code>dim_fonte</code>", "5", "Tesouro, Convenio, Fundo, ..."],
         ["<code>dim_status_empenho</code>", "5", "Empenhado, Liquidando, Liquidado, Pago, Cancelado"],
         ["<code>dim_setor</code>", "8", "Mesmo catalogo dos demais cenarios"],
         ["<code>dim_calendario</code>", "1.096", "Datas de empenho"]],
        num_cols=[])
)

cad.section("p4-cenario4-visuais", "Cenario 4 - Sugestoes de visuais para a aba de Orcamento",
    ul([
        "<b>Cartao (KPI)</b>: total empenhado, total pago, % execucao vs dotacao.",
        "<b>Waterfall</b>: orcado -> atual -> empenhado -> liquidado -> pago.",
        "<b>Linha temporal</b>: empenho mensal por fonte de recurso.",
        "<b>Colunas empilhadas</b>: setor x status.",
        "<b>Top 10</b>: fornecedores com maior valor pago.",
        "<b>Slicer</b>: ano, setor, rubrica, fonte, modalidade, status."
    ]) +
    code(
        "Total Empenhado = SUM(Empenhos[valor_empenhado])\n"
        "Total Liquidado = SUM(Empenhos[valor_liquidado])\n"
        "Total Pago = SUM(Empenhos[valor_pago])\n"
        "% Execucao = DIVIDE(\n"
        "    [Total Pago],\n"
        "    CALCULATE(SUM(Dotacao[valor_atualizado]))\n"
        ")\n"
        "Cancelados = CALCULATE([Total Empenhado], Empenhos[status] = \"Cancelado\")",
        "DAX"
    )
)

cad.section("p4-cenario4-medidas", "Cenario 4 - Medidas DAX uteis",
    code(
        "Saldo a Pagar = [Total Empenhado] - [Total Pago]\n"
        "Ticket Medio = DIVIDE([Total Pago], DISTINCTCOUNT(Empenhos[fornecedor_key]))\n"
        "Contratos a Vencer 60d = CALCULATE(\n"
        "    COUNTROWS(dim_contrato),\n"
        "    dim_contrato[data_fim] <= TODAY() + 60,\n"
        "    dim_contrato[data_fim] >= TODAY()\n"
        ")",
        "DAX"
    )
)

# ---------- CENARIO 5 ----------
cad.section("p4-cenario5-necessidade", "Cenario 5 - A necessidade: custodia sem falha",
    p("Cada evidencia percorre um caminho: <b>coleta</b> -> "
      "<b>transporte</b> -> <b>lacrado</b> -> <b>destino (lab ou arquivo)</b>. "
      "Onde ela demora? Onde o lacre se perde?") +
    aplicab(
        "<b>Quando</b> o Ministerio Publico pede um <b>mapa de custodia</b>.",
        "<b>Por que</b> cada evidencia precisa de <b>tempo, responsavel e "
        "local</b> registrados - e o dashboard comprova.",
        "<b>Exemplo</b> na POLITEC: <i>uma evidencia coletada em Cuiaba nao "
        "pode chegar a Lab. DNA em Sinop com <code>tempo_transporte &gt; "
        "48h</code> - alerta visual.</i>"
    ) +
    callout("tip", "Onde encontrar",
        "<code>datasets/cenario5_custodia/</code> - fato_mov_evidencia.csv "
        "com 1300 movimentacoes em 8 origens e 8 destinos.")
)

cad.section("p4-cenario5-dados", "Cenario 5 - O dataset (1300 evidencias)",
    tbl(["Tabela", "Linhas", "Foco"],
        [["<code>fato_mov_evidencia</code>", "1.300", "Cada ciclo de custodia"],
         ["<code>dim_tipo_evidencia</code>", "10", "Arma, Municao, Droga, Documento, Biologico, Smartphone, ..."],
         ["<code>dim_origem</code>", "8", "Delegacia, Flagrante, Busca Domiciliar, IML, ...,"],
         ["<code>dim_destino</code>", "8", "Lab. DNA, Lab. Toxico, Balistica, Informatica, ..."],
         ["<code>dim_status_custodia</code>", "5", "Coletada, Lacrada, Em Transporte, Recebida, Concluida"],
         ["<code>dim_responsavel</code>", "15", "Peritos, delegados, agentes, escreventes"],
         ["<code>dim_local_armazenamento</code>", "8", "Cofres, camaras frias, depositos"],
         ["<code>dim_calendario</code>", "1.096", "Datas de coleta, recebimento, baixa"]],
        num_cols=[]) +
    callout("note", "Coluna chave",
        "<code>tempo_transporte_horas</code> = "
        "<code>(data_recebimento - data_coleta) * 24 + hora</code>. "
        "Vazio se o recebimento ainda nao aconteceu."
    )
)

cad.section("p4-cenario5-visuais", "Cenario 5 - Sugestoes de visuais para a aba de Custodia",
    ul([
        "<b>Sankey ou Fluxo</b>: origem -> destino (por tipo de evidencia).",
        "<b>Cartao (KPI)</b>: total em custodia, tempo medio de transporte, % lacradas.",
        "<b>Heatmap</b>: hora de coleta x dia da semana (gargalo).",
        "<b>Drill Through</b>: clique em uma evidencia e veja o ciclo completo.",
        "<b>Pareto</b>: tipos de evidencia por quantidade e por valor estimado.",
        "<b>Tabela de auditoria</b>: evidencias com <code>status = Em Transporte "
        "&gt; 14 dias</code> = alerta.",
        "<b>Slicer</b>: tipo, origem, destino, status, periodo."
    ]) +
    code(
        "Evidencias = COUNTROWS(Evidencias)\n"
        "% Lacradas = DIVIDE(\n"
        "    CALCULATE([Evidencias], Evidencias[status] = \"Lacrada\"),\n"
        "    [Evidencias]\n"
        ")\n"
        "Tempo Medio Transporte = AVERAGE(Evidencias[tempo_transporte_horas])\n"
        "Em Transporte > 14d = CALCULATE(\n"
        "    [Evidencias],\n"
        "    Evidencias[status] = \"Em Transporte\",\n"
        "    Evidencias[tempo_transporte_horas] > 14 * 24\n"
        ")",
        "DAX"
    )
)

cad.section("p4-cenario5-medidas", "Cenario 5 - Medidas DAX uteis",
    code(
        "Peso Total (kg) = DIVIDE(SUM(Evidencias[peso_gramas]), 1000)\n"
        "Valor em Custodia = SUMX(Evidencias, Evidencias[valor_estimado])\n"
        "SLA Medio Coletada->Recebida = AVERAGEX(\n"
        "    FILTER(Evidencias, NOT(ISBLANK(Evidencias[tempo_transporte_horas]))),\n"
        "    Evidencias[tempo_transporte_horas]\n"
        ")",
        "DAX"
    )
)

cad.section("p4-juntar-cenarios", "Como juntar cenarios diferentes no mesmo .pbix",
    p("Se voce quiser usar <b>3 ou 4 cenarios no mesmo .pbix</b>, alguns "
      "cuidados:") +
    ul([
        "<b>Dim_calendario</b>: as cinco dimensoes tem o mesmo esquema. "
        "<b>Mantenha apenas uma</b> (ou use sufixos: <code>dim_calendario_backlog</code>, "
        "<code>dim_calendario_dna</code>) e una por relacionamento ou <i>Append Queries</i>.",
        "<b>Dim_setor</b>: as cinco tabelas tem o <i>mesmo conteudo</i> (8 "
        "setores). Mesma logica: una por <i>Append Queries</i> no Power Query.",
        "<b>Dim_universal</b> no projeto integrador: considere criar uma "
        "unica <code>dim_setor</code> e uma unica <code>dim_calendario</code> "
        "para alimentar todas as abas."
    ]) +
    code(
        "// Power Query: juntar dois dim_calendario (Mesma schema)\n"
        "let\n"
        "    cal1 = dim_calendario_backlog,\n"
        "    cal2 = dim_calendario_dna,\n"
        "    union = Table.Combine({cal1, cal2}),\n"
        "    distinct = Table.Distinct(union)\n"
        "in\n"
        "    distinct",
        "Power Query M"
    )
)

# =================================================================
# PARTE 5 - PROJETO INTEGRADOR
# =================================================================
cad.grp("Parte 5 - Projeto Integrador",
        "Seu painel final: 3+ abas tematicas, RLS, publicacao.")

cad.section("p5-objetivo", "O projeto integrador da Aula 5",
    p("Esse e o entregavel do dia. Ao terminar, voce tera um "
      "<b>.pbix publicavel</b> com pelo menos 3 abas, governanca por RLS "
      "e publicacao em workspace segregado.") +
    kpi([
        ("3", "Abas tematicas"),
        ("6+", "Medidas DAX"),
        ("1", "RLS ativa"),
        ("1", "App publicado"),
    ])
)

cad.section("p5-requisitos", "Requisitos minimos do projeto",
    p("O painel tem que cumprir, no minimo:") +
    tbl(["Requisito", "Como comprovar"],
        [["<b>3 abas</b>, cada uma de um cenario", "A primeira aba apos publica&ccedil;ão tem 3 telas"],
         ["<b>1 slicer por aba</b> (periodo + atributo do cenario)", "Visual documentado: periodo + setor/mun/tipo"],
         ["<b>1 KPI com formatacao condicional</b>", "Cartao com regras de cor (verde/amarelo/vermelho)"],
         ["<b>1 visual temporal OU geografico</b> por aba", "Linha temporal ou mapa preenchido"],
         ["<b>RLS ativa</b> em pelo menos 1 aba", "Gerenciamento de funcoes + Service configurado"],
         ["<b>Workspace segregado</b> e App publicada", "Service -> Workspace -> App -> link"]],
        num_cols=[]) +
    callout("purple", "Bonus (subindo a nota)",
        "(a) Aplicar OLS em uma coluna sensivel. (b) Incluir <b>Deployment "
        "Pipeline</b> com estagio DEV/TEST/PROD. (c) Adicionar um <b>botao "
        "Power Automate</b> que dispara email quando o KPI fura a meta."
    )
)

cad.section("p5-3-abas-guia", "Guia para escolher as 3 abas",
    p("Combinacoes recomendadas de 3 dos 5 cenarios, dependendo do publico "
      "do seu painel:") +
    tbl(["Publico-alvo", "Aba 1", "Aba 2", "Aba 3"],
        [["<b>Diretor Tecnico</b>", "Backlog (operacional)", "DNA (laboratorio)", "Custodia (processual)"],
         ["<b>Diretor Financeiro</b>", "Orcamento", "DNA (custo de kit)", "Backlog (custo do atraso)"],
         ["<b>Diretor de Inteligencia</b>", "Mapa Criminal", "Backlog (tempo-resposta)", "Custodia (tempo-transporte)"],
         ["<b>Chefe de Laboratorio DNA</b>", "DNA (principal)", "Custodia (entrada DNA)", "Orcamento (custo de kit)"],
         ["<b>Chefe do IML</b>", "Criminalidade", "Custodia", "Backlog (necropsia)"]],
        num_cols=[])
)

cad.section("p5-plano-painel", "Plano de 1 pagina do painel integrador",
    p("Voce vai usar este plano como <b>mapa</b>:") +
    tbl(["Pagina", "Titulo", "Cenario", "Filtro Slicer", "KPIs", "Visual Principal"],
        [["Aba 1", "Backlog / Fila", "cenario1_backlog", "data_entrada (ano-mes), setor",
          "% no prazo, Requisicoes em atraso", "Colunas agrupadas setor"],
         ["Aba 2", "TAT do DNA", "cenario2_dna", "data_recebimento (mes), laboratorio",
          "TAT Medio, % na Meta", "Linha temporal por laboratorio"],
         ["Aba 3", "Mapa Criminal MT", "cenario3_criminalidade", "data (mes), municipio",
          "Ocorrencias, Vitimas", "Mapa Preenchido + Heatmap dia/hora"],
         ["Aba Bonus 4", "Orcamento", "cenario4_orcamento", "data_empenho (mes), setor",
          "Total Empenhado, % Execucao", "Waterfall + Top fornecedores"],
         ["Aba Bonus 5", "Cadeia de Custodia", "cenario5_custodia", "data_coleta (mes), status",
          "Evidencias em Transporte, Tempo Medio", "Sankey ou Matriz origem/destino"]],
        num_cols=[])
)

cad.section("p5-rls-recomendada", "RLS recomendada para o projeto",
    p("O painel integrador tem RLS baseada no <b>setor do usuario</b>. "
      "Aqui esta o esqueleto da funcao:") +
    code(
        "// RLS: cada perito ve apenas exames ou ocorrencias do seu setor.\n"
        "// Configurada na tabela fato principal do projeto.\n"
        "Seguranca = \n"
        "FILTER(\n"
        "    ALL(UsuarioSetor),\n"
        "    UsuarioSetor[email] = USERPRINCIPALNAME()\n"
        ")\n"
        "// Faca uma tabela dim_setor com EMAIL do perito (atributo\n"
        "// adicional). A funcao acima retorna o setor do usuario logado.",
        "DAX (RLS)"
    ) +
    aplicab(
        "<b>Quando</b> um perito do DNA abre o painel.",
        "A funcao retorna o <code>setor_key</code> dele. Todas as paginas "
        "filtram <code>fato_requisicoes[setor_key] = variavel</code>.",
        "Na POLITEC: <i>perito do DNA so ve requisicoes de DNA; perito da "
        "Toxicologia so ve Toxicologia; diretor ve tudo.</i>"
    )
)

cad.section("p5-checklist-entrega", "Checklist de entrega do projeto",
    p("Antes de submeter, valide cada item:") +
    checklist([
        "<b>3+ abas</b> com tema distinto e titulo claro.",
        "Cada aba tem <b>1 slicer</b> (data + atributo do cenario).",
        "Cada aba tem <b>1 KPI com formatacao condicional</b>.",
        "Pelo menos <b>1 visual temporal ou geografico</b> por aba.",
        "<b>RLS</b> ativa em ao menos 1 aba (testada como papel).",
        "<b>Publicacao</b> em workspace segregado + App.",
        "Documentacao (<code>README.md</code> do projeto): cenario escolhido, "
        "medidas criadas, KPI principais.",
        "<b>LGPD</b>: nenhuma coluna sensivel (CPF, endereco) ficou visivel.",
        "<b>Testar como papel</b>: Diretor (tudo) + Chefe (setor) + Perito (so seu setor).",
    ])
)

cad.section("p5-rubrica", "Rubrica de avaliacao (nota final)",
    p("Como o projeto sera avaliado:") +
    tbl(["Dimensao", "Peso", "Excelente (4)", "Suficiente (2-3)", "Insuficiente (0-1)"],
        [["Cubrimento", "3", "3+ abas completas", "2 abas completas", "1 aba ou menos"],
         ["DAX", "3", "6+ medidas; usa CALCULATE, time intel, contexto", "4 medidas; mistura basica", "Poucas medidas"],
         ["Visual & UX", "2", "Hierarquia visual, slicers funcionais, formato condicional", "Slicers funcionando", "Confuso"],
         ["Governanca", "2", "RLS ativa + OLS + App publicada", "RLS documentada", "Sem RLS"],
         ["Pitch", "2", "Storytelling com dado (cenario -> decisao)", "Merecido: justifica uso", "Pura descricao"],
         ["<b>Total</b>", "12", "12 pontos", "6-11", "Abaixo de 6"]],
        num_cols=[])
)

# =================================================================
# PARTE 6 - FECHAMENTO
# =================================================================
cad.grp("Parte 6 - Fechamento",
        "Ecossistema, LGPD, erros, quiz, glossario e referencias do curso.")

cad.section("p6-stack-microsoft", "Ecossistema Microsoft: o mapa completo",
    p("O Power BI nao esta sozinho. Ele vive dentro de uma plataforma "
      "que se retroalimenta:") +
    tbl(["Camada", "Ferramenta", "Funcao"],
        [["<b>Dados</b>", "Azure SQL, Synapse, ADLS, Databricks", "Armazena e processa"],
         ["<b>ETL</b>", "Data Factory, Power Query, Dataflows", "Prepara dados"],
         ["<b>Modelo</b>", "VertiPaq (no Desktop)", "Compacta e indexa"],
         ["<b>Visual</b>", "Power BI Desktop", "Cria o .pbix"],
         ["<b>Distribuicao</b>", "Service, Apps, Embed", "Publica"],
         ["<b>Consumo</b>", "Mobile, Teams, Excel, Portal", "Alcana usuario"],
         ["<b>Automacao</b>", "Power Automate, Power Apps", "Age sobre o dado"],
         ["<b>IA</b>", "Copilot, AI Visuals, Azure OpenAI", "Conversa com o dado"]],
        num_cols=[])
)

cad.section("p6-erros-finais", "10 erros que todo perito cai",
    p("Lista dos erros mais comuns em projetos reiais de BI pericial - "
      "evite-os:") +
    tbl(["#", "Erro", "Por que e problematico"],
        [["1", "Publicar dado pessoal (CPF, endereco)", "Vazamento LGPD; notificacao ANPD"],
         ["2", "Atualizacao nao agendada", "Decisao com dado de ontem"],
         ["3", "RLS mal configurada", "Diretor acha que todo mundo ve tudo"],
         ["4", "Painel com 20 visuais", "Ninguem sabe qual olhar"],
         ["5", "Sem data e hora visivel", "Fica em duvida qual versao esta olhando"],
         ["6", "Medidas calculadas no Desktop, nao no modelo", "Cada report recalcula do zero"],
         ["7", "Drill through sem contexto", "Vai para uma pagina vazia"],
         ["8", "Tipos errados (texto em numero)", "Soma nao funciona, ordem alfabetica prevalece"],
         ["9", "Coluna calculada onde media servia", "RAM extra sem necessidade"],
         ["10", "Nome obscuro de aba", "Usuario fecha o app e diz 'nao entendi'"]],
        num_cols=[])
)

cad.section("p6-checklist-publicacao-v2", "Checklist de publicacao - versao final (10 itens)",
    p("Antes de publicar o projeto integrador - e qualquer outro - em "
      "producao, percorra os 10:") +
    checklist([
        "Modelo tem esquema estrela (fato cercada por dimensoes).",
        "<b>Tipos</b> das colunas conferidos (numeros em numero, datas em data).",
        "<b>dim_calendario</b> marcada como tabela de datas.",
        "<b>Medida de DAX</b> chave (ex.: total eventos) ja existe.",
        "<b>RLS</b> documentada e testada em Desktop e Service.",
        "<b>OLS</b> aplicada a colunas sensiveis (CPF, endereco).",
        "Filtros sensiveis <b>ocultos</b> (ex.: Nome da Vitima).",
        "Atualizacao agendada configurada (6h ou diaria).",
        "'Ultima Atualizacao' visivel na primeira aba.",
        "Workspace segregado, App publicada e linkado para os destinatarios."
    ])
)

cad.section("p6-proximos-passos", "Proximos passos do seu ecossistema de BI",
    p("A capacitacao termina; a jornada do BI nao. Sugestoes para a "
      "POLITEC seguir:") +
    ul([
        "Curto prazo (30 dias): colocar o painel integrador em "
        "homologacao com 3 setores-piloto.",
        "Medio prazo (90 dias): institucionalizar <b>Deployment Pipelines</b> "
        "(dev / test / prod), treinando 2-3 pessoas em DAX/RLS.",
        "Longo prazo (12 meses): avaliar <b>Microsoft Fabric</b> para "
        "consolidar OneLake; criar <b>Dataflows compartilhados</b>."
    ])
)

cad.section("p6-casos-extras", "3 casos extras para a pratica avancada",
    p("Para quem terminou cedo: tres missoes extras.") +
    aplicab(
        "<b>Caso A - Power BI + Power Automate</b>",
        "Crie um <b>fluxo no Power Automate</b> que dispara quando "
        "<code>% Atraso</code> ultrapassa 20% no Lab 1, enviando email ao "
        "chefe do setor.",
        "<b>Exemplo</b>: gatilho 'Power BI - valor ultrapassa limite', "
        "destinatario do chefe do setor, mensagem automatica."
    ) +
    aplicab(
        "<b>Caso B - Embedded no SharePoint</b>",
        "Publique o painel como <b>Embedded</b> no SharePoint institucional "
        "(separadamente ou via App).",
        "<b>Exemplo</b>: portal <i>POLITEC Dados</i>, com 4 iframes "
        "apontando para os 4 principais dashboards."
    ) +
    aplicab(
        "<b>Caso C - Parque de Dados com Fabric</b>",
        "Crie um <b>Dataflow Gen2</b> dentro do Microsoft Fabric que le "
        "<code>datasets/cenario4_orcamento/</code> e armazena no OneLake.",
        "<b>Exemplo</b>: substituir o caminho CSV direto por um Lake que "
        "alimentara o painel."
    )
)

cad.section("p6-quiz", "Quiz final - 15 perguntas",
    p("Fecha a capacitacao com 15 perguntas sobre DAX, RLS, governanca e "
      "o projeto integrador. As respostas abrem no clique.") +
    q("Qual funcao em DAX altera o contexto de filtro antes do calculo?",
      ["a) SUMX", "b) CALCULATE", "c) DIVIDE", "d) VALUES"],
      1, hint="E a funcao mais importante do DAX.") +
    q("O que significa RLS no Power BI?",
      ["a) Row-Level Security", "b) Real-Time Load", "c) Report Label Standard", "d) Resource Limit Service"],
      0, hint="Filtragem de linhas por papel do usuario.") +
    q("Qual e a diferenca entre RLS e OLS?",
      ["a) RLS esconde colunas; OLS esconde linhas",
       "b) RLS esconde linhas; OLS esconde colunas",
       "c) Sao sinonimos",
       "d) Nenhuma das anteriores"],
      1) +
    q("Para usar time intelligence (TOTALYTD, SAMEPERIODLASTYEAR), o que "
      "precisamos ter no modelo?",
      ["a) Uma medida de soma", "b) Uma tabela de datas marcada",
       "c) Um visual de calendario", "d) Uma coluna calculada"],
      1) +
    q("Qual funcao retorna a soma de uma expressao iterada por linha?",
      ["a) SUM", "b) COUNT", "c) SUMX", "d) TOTALYTD"],
      2) +
    q("Em DIVIDE(A, B), o que acontece se B for 0 e voce chamar DIVIDE(A, B, 0)?",
      ["a) Retorna erro", "b) Retorna BLANK()", "c) Retorna 0", "d) Retorna A"],
      2) +
    q("Quantas linhas tem o <code>fato_requisicoes</code> do cenario 1?",
      ["a) 800", "b) 1000", "c) 1200", "d) 1500"],
      2) +
    q("O <code>fato_ocorrencias</code> do cenario 3 cobre quantos municipios?",
      ["a) 10", "b) 14", "c) 16", "d) 18"],
      3) +
    q("Quantos kits de DNA distintos o cenario 2 oferece?",
      ["a) 8", "b) 10", "c) 12", "d) 14"],
      2) +
    q("O Dataflow roda onde?",
      ["a) No Power BI Desktop (local)", "b) No Power BI Service (nuvem)",
       "c) No banco de origem", "d) No OneDrive"],
      1) +
    q("O que faz a funcao ALL(dimensao) em DAX?",
      ["a) Remove todos os visuais", "b) Remove o filtro daquela dimensao",
       "c) Adiciona uma nova coluna", "d) Marca a tabela como oculta"],
      1) +
    q("Quantos cenarios a Aula 5 oferece com datasets proprios?",
      ["a) 3", "b) 4", "c) 5", "d) 7"],
      2) +
    q("O projeto integrador exige no minimo quantas abas tematicas?",
      ["a) 1", "b) 2", "c) 3", "d) 5"],
      2) +
    q("Qual a diferenca entre Deployment Pipeline e Publicacao Direta?",
      ["a) Sao sinonimos",
       "b) Pipeline automatiza DEV -> TEST -> PROD",
       "c) Publicacao Direta usa Copilot",
       "d) Pipeline so funciona no Premium"],
      1) +
    q("Por que e importante marcar a tabela de datas como tabela de datas?",
      ["a) Para colorir graficos",
       "b) Para que funcoes de time intelligence (TOTALYTD) funcionem",
       "c) Para obrigar a versao premium",
       "d) E opcional"],
      1)
)

cad.section("p6-glossario", "Glossario rapido da Aula 5",
    glossary([
        ("DAX", "Linguagem de formula do Power BI. Calcula medidas, colunas, "
         "e tabelas calculadas."),
        ("CALCULATE", "Funcao que troca o contexto de filtro antes de calcular."),
        ("Iterador (X)", "Funcao que percorre linha a linha: SUMX, AVERAGEX, COUNTX."),
        ("Time Intelligence", "Conjunto de funcoes (TOTALYTD, SAMEPERIODLASTYEAR) "
         "que dependem de dim_calendario."),
        ("RLS (Row-Level Security)", "Filtra linhas por papel do usuario."),
        ("OLS (Object-Level Security)", "Esconde coluna/tabela por papel."),
        ("Dataflow", "ETL na nuvem. Tabela transformada que varios .pbix consomem."),
        ("Dataset compartilhado", "Modelo semantico publicado e consumido por "
         "varios relatorios via Live Connection."),
        ("Deployment Pipeline", "Fluxo DEV -> TEST -> PROD com diff e promotion."),
        ("App", "Pacote do Power BI Service com dashboards para um publico alvo."),
        ("Microsoft Fabric", "Plataforma unificada de dados (OneLake + Data Factory "
         "+ Synapse + Power BI)."),
        ("Star Schema", "Modelo dimensional: uma fato cercada por dimensoes."),
        ("Surrogate Key", "Chave inteira (1..N) atribuida a cada linha de dimensao."),
        ("Schema Measurement", "Tabela central de medidas, separadas em pastas para "
         "organizacao."),
        ("Performance Analyzer", "Ferramenta no Desktop que mostra visual e medida lentos."),
        ("Card Visual", "Cartao KPI - exibe um numero grande, com icone ou tendencia."),
        ("Drill Through", "Clique em um valor e vai para uma pagina de detalhe."),
        ("KPI Formatado", "Cartao com formatacao condicional (verde/amarelo/vermelho)."),
        ("LGPD", "Lei Geral de Protecao de Dados (Lei 13.709/2018)."),
        ("ANPD", "Autoridade Nacional de Protecao de Dados."),
        ("PDF - Politec Pericial", "Painel Final - o entregavel do projeto integrador."),
    ])
)

cad.section("p6-referencias", "Referencias e materiais de apoio",
    p("Para ir alem da Aula 5:") +
    ul([
        "<b>Documentacao oficial do Power BI DAX</b> - "
        "<code>learn.microsoft.com/dax/</code>",
        "<b>DAX Patterns</b> - colecao de medidas prontas (SQLBI, Marco Russo).",
        "<b>SQLBI (Marco Russo e Alberto Ferrari)</b> - livros <i>The Definitive "
        "Guide to DAX</i> e <i>Analyzing Data with Power BI and Power Pivot</i>.",
        "<b>Cole Nussbaumer Knaflic</b> - <i>Storytelling with Data</i>: boas "
        "praticas de visualizacao que se aplicam ao Power BI.",
        "<b>Microsoft Learn</b> - trilhas gratuitas de Power BI, Fabric e Power Platform.",
        "<b>POLITEC/MT</b> - relatorios institucionais e bases anonimizadas para "
        "pratica supervisionada.",
        "<b>Proximo curso</b> - DAX 2 (formula avancada, otimizacao) e "
        "Microsoft Fabric 1 (OneLake, Synapse)."
    ])
)

cad.section("p6-agradecimentos", "Obrigado pela jornada",
    p("Voce chegou ao fim da Capacitacao POLITEC/MT em Analise de Dados "
      "aplicada a Pericia Criminal. Foram 5 dias, 4 cadernos de "
      "aprofundamento, dezenas de laboratorios e cenarios e 5 datasets "
      "que transformam teoria em pratica.") +
    legenda([
        ("\U0001f4a1", "Voce aprendeu a fazer perguntas",
         "Estatistica, qualidade, ciclo dos dados: a <b>pergunta certa</b> vem antes do grafico."),
        ("\U0001f4f0", "Voce aprendeu a organizar",
         "Planilha limpa, validada, tipada. O Power BI nao resolve dado sujo."),
        ("\U0001f4ca", "Voce aprendeu a visualizar",
         "Do Excel ate o Power BI, do Power BI ate o painel final."),
        ("\U0001f6e1", "Voce aprendeu a governar",
         "RLS, OLS, LGPD, publicacao, Apps. O BI institucional exige responsabilidade."),
    ]) +
    callout("purple", "Continue",
        "<b>A capacitacao acabou, mas o BI da POLITEC e so comeco</b>. "
        "Continue treinando, publique seu painel, compartilhe com seu chefe. "
        "O futuro da pericia criminal em MT passa pela inteligencia dos "
        "dados - e por profissionais que sabem transforma-los em decisao. "
        "<b>Ate a proxima!</b>")
)

# =================================================================
# CONSTRUCAO
# =================================================================
cad.build()
