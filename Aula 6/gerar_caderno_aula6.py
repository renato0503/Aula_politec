# -*- coding: utf-8 -*-
"""Gerador do caderno da Aula 6 - POLITEC/MT.

Novo formato do curso: a manha e de paineis, BI e analise de dados; a tarde e
de hands-on em gestao de projetos (BPMN/Mermaid, AS-IS/TO-BE) e nocoes de mini
app. Conteudo: painel de processo no Power BI (modelo, medidas DAX, layout e
leitura), analise de gargalos (espera x execucao, Pareto, Little's Law),
fundamentos de projeto, BPMN 2.0, Mermaid, AS-IS/TO-BE e canvas do mini app.

Rode:  python gerar_caderno_aula6.py
PDF:   python ..\\exportar_pdf.py 6
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from caderno_lib import (Caderno, p, h3, ul, checklist, ficha, callout, tbl, code,
                         step, q, aplicab, grid2, flow_h, kpi, antesdepois,
                         legenda, glossary, bar_chart)
import ptbr
from caderno_svg import (icon, gallery, swimlane_anatomy, gates_anatomy,
                         wait_vs_touch, automation_anatomy, method_chain,
                         build_process_asis, build_process_tobe,
                         build_process_orcamento, build_process_custodia)

cad = Caderno(
    out=str(pathlib.Path(__file__).resolve().parent / "caderno-dia6.html"),
    dia=6,
    kicker="Aula 6 · Manha de BI, tarde de projeto",
    headline="Do painel de processo ao projeto de melhoria",
    sub="Novo formato: a manha e de paineis, BI e analise de dados; a tarde e de "
        "hands-on em gestao de projetos e nocoes de mini app. Monte o painel que "
        "mostra onde o caso espera, leia o gargalo com numero e transforme a "
        "leitura em AS-IS, TO-BE e um canvas de mini app. Cinco datasets de "
        "processo com 57.293 execucoes de etapa para medir, em vez de chutar.",
    meta="Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 6 · "
         "Modulo 8 (Painel de Processo + Gestao de Projetos)",
    descricao="Caderno do Dia 6 do Curso de Capacitacao POLITEC/MT no novo formato: "
              "manha de paineis, BI e analise de dados; tarde de hands-on em gestao "
              "de projetos e nocoes de mini app. Painel de processo no Power BI "
              "(modelo estrela, 8 medidas DAX, 5 visuais, leitura em 60 segundos), "
              "analise de gargalos (espera x execucao, Pareto, retrabalho, Little's Law, "
              "custo da espera), fundamentos de projeto (escopo, prazo, custo, risco, "
              "stakeholders), BPMN 2.0 (swimlanes, gateways, eventos), Mermaid, AS-IS, "
              "TO-BE, intervencao digital e canvas do mini app. 5 datasets de processo "
              "com 57.293 execucoes de etapa em modelo estrela."
)

# =================================================================
# ABERTURA
# =================================================================
cad.grp("Abertura", "O curso passa a operar em dois turnos: a manhã com painéis e análise, a tarde com gestão de projetos.")

cad.section("boas-vindas", "Bem-vindo ao caderno do Dia 6",
    p("O Dia 6 inaugura o formato de dois turnos da capacitação. A manhã é "
      "dedicada a painéis, BI e análise de dados. A tarde é dedicada a "
      "atividades práticas de gestão de projetos e, nas aulas seguintes, à "
      "ideação e à prototipação de mini apps com apoio de IA agêntica.") +
    p("Neste dia, a manhã parte dos dados de processo e chega a um painel que "
      "mostra onde o caso espera. A tarde usa esse painel como evidência para "
      "ensinar o mínimo de gestão de projetos e a notação BPMN/Mermaid. Com "
      "isso, a turma sai com o painel, o diagnóstico do gargalo e o desenho do "
      "processo que precisa mudar.") +
    ficha("a", "A regra dos dois turnos",
        "A manhã responde à pergunta <b>&quot;o que o dado mostra?&quot;</b>. "
        "A tarde responde à pergunta <b>&quot;o que faremos com essa "
        "informação?&quot;</b>. Dessa forma, um turno alimenta o outro: sem o "
        "painel, a tarde fica sem evidência; sem a tarde, o painel fica sem "
        "decisão.") +
    legenda([
        (icon("chart", 26), "Manhã: painéis e análise",
         "Modelo de dados, medidas DAX, layout e leitura do painel de processo."),
        (icon("search", 26), "Manhã: gargalo medido",
         "Espera e execução, Pareto, retrabalho e Little's Law sobre os datasets."),
        (icon("project", 26), "Tarde: fundamentos de projeto",
         "Escopo, prazo, custo, risco e partes interessadas."),
        (icon("map", 26), "Tarde: BPMN e Mermaid",
         "Do texto ao diagrama AS-IS, sem desenhar à mão."),
        (icon("rocket", 26), "Tarde: TO-BE e mini app",
         "Redesenho do processo, intervenção digital e as primeiras noções de mini app."),
    ])
)

cad.section("mapa-do-dia", "Mapa do Dia 6: manhã de painel, tarde de projeto",
    p("O dia tem dois turnos com entregáveis próprios e ligados entre si. O "
      "painel da manhã é a evidência que a tarde usa para decidir o que mudar. "
      "Por isso, a leitura do painel aparece antes de qualquer proposta de "
      "intervenção.") +
    grid2([
        ("\U0001f305 Manhã (08h-12h): painéis, BI e análise de dados",
         ul(["<b>Parte 1</b>: fundamentos do painel, com modelo, medidas e layout",
             "<b>Parte 2</b>: cinco receitas, uma para cada dataset",
             "<b>Parte 3</b>: análise do processo, com espera, Pareto, retrabalho e Little's Law",
             "<b>Labs 1 a 4</b>: montagem do painel no Power BI e escrita da hipótese de gargalo"])),
        ("\U0001f306 Tarde (13h-17h): gestão de projetos",
         ul(["<b>Parte 4</b>: fundamentos de projeto, com escopo, prazo, custo, risco e partes interessadas",
             "<b>Partes 5 e 6</b>: BPMN e Mermaid, do texto ao diagrama AS-IS",
             "<b>Parte 7</b>: TO-BE, intervenção digital e noções de mini app",
             "<b>Labs 5 a 8</b>: AS-IS, TO-BE, cálculo do ganho e pitch"]))
    ]) +
    callout("note", "Escopo desta primeira aula do novo formato",
        "A tarde fica nos fundamentos e nas noções de gestão de projetos. A "
        "prototipação do mini app com IA agêntica começa nas aulas seguintes. "
        "Neste dia, o objetivo é sair com o vocabulário, o diagrama e o "
        "critério para construir o app na etapa seguinte.")
)

cad.section("recap-do-curso", "Recap dos cinco dias anteriores",
    p("Até aqui, a turma percorreu o ciclo que vai do dado à decisão. Cada dia "
      "acrescentou uma camada ao trabalho de análise. Por isso, o Dia 6 "
      "começa com o painel e termina com a proposta de mudança.") +
    tbl(["Dia", "Foco", "Entregável"],
        [["<b>D1</b>", "Estatística, qualidade e indicadores", "Raciocínio sobre o dado"],
         ["<b>D2</b>", "Planilha, fórmulas e validação", "Planilha limpa e tipada"],
         ["<b>D3</b>", "Organização, visualização e ETL", "Base consolidada"],
         ["<b>D4</b>", "Power BI Desktop e Service", "Relatório e dashboard"],
         ["<b>D5</b>", "Dashboards de BI em cinco cenários", "Painel institucional"],
         ["<b>D6 manhã</b>", "Painel de processo e análise", "<b>Painel do gargalo</b>"],
         ["<b>D6 tarde</b>", "Gestão de projetos e BPMN", "<b>AS-IS e TO-BE</b>"]],
        num_cols=[]) +
    callout("note", "A mudança de foco",
        "Até o D5, o trabalho era descrever o que já existe. A partir do D6, o "
        "trabalho é decidir o que mudar. Nesse sentido, a decisão começa no "
        "painel e não na opinião.")
)

cad.section("objetivo-do-dia", "Objetivo do Dia 6: um painel que aponta o gargalo",
    p("Ao fim da manhã, a turma tem um painel. Ao fim da tarde, tem a leitura "
      "do processo e o desenho do que muda. Por isso, os entregáveis do dia "
      "seguem esta ordem:") +
    checklist([
        "Um <b>painel de processo</b> no Power BI, com 8 medidas e 5 visuais.",
        "A <b>leitura do gargalo</b> em uma frase, com número.",
        "O <b>AS-IS</b> do processo em BPMN/Mermaid.",
        "O <b>TO-BE</b> ligado ao gargalo medido.",
        "O <b>canvas do mini app</b> e um pitch de 3 minutos.",
    ]) +
    kpi([
        ("8", "medidas DAX"),
        ("5", "visuais no painel"),
        ("5", "datasets de processo"),
        ("8", "labs no dia"),
    ]) +
    method_chain() +
    ficha("g", "O princípio que organiza o dia",
        "Não se melhora um processo que não se mede. A manhã mede e a tarde "
        "decide. Se a tarde não conseguir apontar o número que justifica a "
        "mudança, o trabalho volta ao painel.")
)

# =================================================================
# PARTE 1 - MANHA: O PAINEL DE PROCESSO
# =================================================================
cad.grp("Parte 1 - Manhã: o painel de processo",
        "Do arquivo Excel ao painel que mostra, em 60 segundos, onde o processo perde tempo.")

cad.section("painel-de-processo", "Por que um painel de processo, e não mais um relatório",
    p("Um relatório descreve o que aconteceu. Um painel de processo responde, "
      "toda semana, à mesma pergunta: onde o caso está parando? Por isso, ele "
      "não é um catálogo de gráficos. É um instrumento de decisão.") +
    tbl(["Relatório tradicional", "Painel de processo"],
        [["Mostra o total do mês", "Mostra a <b>etapa</b> que concentra a espera"],
         ["Responde &quot;quanto foi?&quot;", "Responde &quot;onde trava?&quot;"],
         ["Atualiza quando alguém pede", "Atualiza com o mesmo modelo de dados"],
         ["Serve para prestar contas", "Serve para <b>decidir a intervenção</b>"]],
        num_cols=[]) +
    ficha("a", "A pergunta que o painel responde",
        "&quot;Se eu puder melhorar apenas uma etapa deste processo neste "
        "trimestre, qual devo escolher?&quot; O painel existe para responder a "
        "essa pergunta com número. Por isso, a primeira leitura é sempre a "
        "espera por etapa.") +
    aplicab(
        "Na reunião mensal da unidade, antes de decidir contratação ou compra.",
        "A decisão de capacidade precisa olhar a fila, e não apenas o volume total.",
        "No Cenário 1, o painel mostra a Fila perito com 41,5% da espera. "
        "Nesse caso, a reunião começa por essa etapa, e não pela etapa que mais "
        "executa.") +
    callout("err", "Painel sem pergunta",
        "Um painel com 30 gráficos que ninguém abre para decidir não é "
        "instrumento de gestão. Se o visual não muda uma decisão, ele não "
        "deveria estar no painel.")
)

cad.section("modelo-dados-processo", "O modelo de dados do painel: a estrela do processo",
    p("O painel nasce de uma tabela fato e de suas dimensões. Neste caso, o "
      "grão é uma execução de etapa. Cada linha representa um caso passando "
      "por uma etapa, com o tempo de espera e o tempo de execução separados.") +
    tbl(["Tabela", "Grão e papel", "Uso no painel"],
        [["<code>fato_execucao</code>", "1 linha = 1 execução de etapa", "Tempos, flags e custo"],
         ["<code>dim_etapa</code>", "1 linha = 1 etapa", "Nome e ordem da etapa, que vira o eixo do Pareto"],
         ["<code>dim_unidade</code>", "1 linha = 1 unidade", "Swimlane, filtro e matriz de responsabilidade"],
         ["<code>dim_sistema</code>", "1 linha = 1 sistema", "Mostra quanto do processo ainda é manual"],
         ["<code>dim_calendario</code>", "1 linha = 1 dia", "Permite TAT e evolução no tempo"]],
        num_cols=[]) +
    code(
        "fato_execucao\n"
        "  id_execucao (PK)\n"
        "  id_ciclo      -> agrupa as etapas de um caso\n"
        "  etapa_key     -> dim_etapa\n"
        "  unidade_key   -> dim_unidade\n"
        "  sistema_key   -> dim_sistema\n"
        "  data_inicio_key -> dim_calendario\n"
        "  tempo_espera_min    (fila)\n"
        "  tempo_execucao_min  (trabalho)\n"
        "  flag_retrabalho\n"
        "  custo_execucao_rs",
        "modelo"
    ) +
    step([
        ("Importe as 8 abas do workbook",
         "No Power BI, use <b>Obter dados &rarr; Pasta de trabalho do Excel</b>. "
         "Selecione o <code>.xlsx</code> do cenário e marque a "
         "<code>fato_execucao</code> e as 7 dimensões."),
        ("Confirme o cabeçalho e os tipos",
         "No Power Query, use <b>Usar Primeira Linha como Cabeçalho</b>. "
         "Tempos como <b>Número Decimal</b>, chaves como <b>Número Inteiro</b> e "
         "datas como <b>Data</b>."),
        ("Crie os relacionamentos",
         "Arraste <code>etapa_key</code> da fato para <code>dim_etapa</code>. "
         "Repita o procedimento para unidade, sistema, tipo, status e projeto. "
         "Mantenha a direção única, da dimensão para a fato."),
        ("Marque a tabela de datas",
         "Selecione <code>dim_calendario</code> &rarr; <b>Marcar como tabela de "
         "datas</b> &rarr; coluna <code>data</code>."),
    ]) +
    callout("err", "O erro de grão que altera o resultado",
        "Se a fato for unida à dimensão antes da soma, as linhas podem ser "
        "duplicadas e a espera fica maior do que é. Por isso, some sempre pela "
        "fato e filtre pela dimensão.")
)

cad.section("medidas-painel", "As 8 medidas do painel em DAX",
    p("Uma medida não é uma coluna. A coluna guarda o dado, e a medida "
      "responde à pergunta. As oito medidas abaixo cobrem o que o painel "
      "precisa informar.") +
    code(
        "Tempo Espera (h) = SUM(fato_execucao[tempo_espera_min]) / 60\n"
        "\n"
        "Tempo Execucao (h) = SUM(fato_execucao[tempo_execucao_min]) / 60\n"
        "\n"
        "Tempo Total (h) = [Tempo Espera (h)] + [Tempo Execucao (h)]\n"
        "\n"
        "% Espera = DIVIDE([Tempo Espera (h)], [Tempo Total (h)])\n"
        "\n"
        "Casos = DISTINCTCOUNT(fato_execucao[id_ciclo])\n"
        "\n"
        "TAT Medio (h) = DIVIDE([Tempo Total (h)], [Casos])\n"
        "\n"
        "Espera Media (h) = AVERAGE(fato_execucao[tempo_espera_min]) / 60\n"
        "\n"
        "Taxa Retrabalho =\n"
        "    DIVIDE(\n"
        "        CALCULATE(COUNTROWS(fato_execucao), fato_execucao[flag_retrabalho] = 1),\n"
        "        COUNTROWS(fato_execucao)\n"
        "    )",
        "dax"
    ) +
    tbl(["Medida", "Pergunta que responde", "Onde usar"],
        [["<b>Tempo Espera (h)</b>", "Quanto tempo o caso fica parado", "Cartão e barras"],
         ["<b>Tempo Execucao (h)</b>", "Quanto tempo alguém trabalha", "Barras empilhadas"],
         ["<b>Tempo Total (h)</b>", "Quanto dura o processo", "Cartão de TAT"],
         ["<b>% Espera</b>", "Quanto do processo é fila", "Cartão e meta"],
         ["<b>Casos</b>", "Quantos casos únicos existem", "Cartão e denominador"],
         ["<b>TAT Medio (h)</b>", "Tempo médio por caso", "Linha do tempo"],
         ["<b>Espera Media (h)</b>", "Espera média por execução", "Pareto por etapa"],
         ["<b>Taxa Retrabalho</b>", "Quanto se refaz", "Matriz por unidade"]],
        num_cols=[]) +
    callout("tip", "Nomeie a medida como o gestor fala",
        "&quot;TAT Medio (h)&quot; é mais claro do que &quot;avg_total&quot;. "
        "Além disso, o nome da medida é a primeira camada de documentação do "
        "painel. Quem abre o relatório precisa entender o indicador sem "
        "perguntar.") +
    aplicab(
        "Sempre que o painel for compartilhado com a direção.",
        "A medida é a parte do painel que carrega a regra de negócio.",
        "Se a direção pergunta quanto do tempo é espera, a resposta é "
        "<code>% Espera</code>, e não uma conta feita à mão no slide.")
)

cad.section("layout-painel", "O layout: 5 visuais que contam a história",
    p("O painel não precisa de 20 visuais. Precisa de cinco, e cada um "
      "responde a uma pergunta diferente. A leitura começa no topo, com os "
      "números, e desce para o detalhe, com a etapa que concentra o problema.") +
    kpi([
        ("92,4%", "do tempo é espera"),
        ("44 h", "espera média na fila"),
        ("41,5%", "da espera na Fila perito"),
        ("11,6%", "de retrabalho"),
    ]) +
    tbl(["#", "Visual", "Campos", "Pergunta que responde"],
        [["<b>1</b>", "Cartões (KPI)", "TAT Medio, % Espera, Casos, Taxa Retrabalho", "Como está o processo hoje?"],
         ["<b>2</b>", "Barras empilhadas", "Etapa no eixo; Espera e Execução nos valores", "Onde o caso espera mais?"],
         ["<b>3</b>", "Pareto (barras e linha)", "Etapa, Espera e % acumulado", "Quais poucas etapas explicam a maior parte?"],
         ["<b>4</b>", "Linha do tempo", "Mês e TAT Medio", "O processo está melhorando ou piorando?"],
         ["<b>5</b>", "Matriz", "Unidade nas linhas, etapa nas colunas e retrabalho nos valores", "Quem concentra o retrabalho?"]],
        num_cols=[]) +
    step([
        ("Comece pelos cartões",
         "Coloque quatro cartões no topo, com <b>TAT Medio</b>, <b>% Espera</b>, "
         "<b>Casos</b> e <b>Taxa Retrabalho</b>. Eles formam a manchete do painel."),
        ("Coloque o Pareto no centro",
         "Use barras de espera por etapa, em ordem decrescente, e uma linha de "
         "percentual acumulado. Esse é o visual que aponta o gargalo."),
        ("Use a linha do tempo para a tendência",
         "No eixo de meses, coloque o TAT Medio. Assim, o painel mostra se a "
         "intervenção mudou o resultado ao longo do tempo."),
        ("Deixe a matriz para o detalhe",
         "Use unidade nas linhas, etapa nas colunas e retrabalho nos valores. "
         "Com isso, o gestor identifica quem precisa de apoio, e não apenas onde "
         "está o problema."),
    ]) +
    callout("err", "O painel que responde a tudo e a nada",
        "Se cada visual tem uma pergunta própria, o painel se lê em 60 "
        "segundos. Se todos mostram a mesma coisa com filtros diferentes, o "
        "painel não ajuda a decidir. Por isso, antes de inserir um visual, "
        "escreva a pergunta que ele responde.")
)

cad.section("passo-a-passo-painel", "Passo a passo: montar o painel no Power BI",
    p("A sequência abaixo assume que o Power BI Desktop já está instalado, "
      "conforme o Dia 4. O caminho é o mesmo para os cinco datasets. O que "
      "muda é o nome do arquivo e o gargalo de cada processo.") +
    step([
        ("1. Obtenha os dados",
         "<b>Página Inicial &rarr; Obter dados &rarr; Pasta de trabalho do "
         "Excel</b>. Selecione o workbook do cenário, como "
         "<code>Cenario1_Requisicao_Pericial.xlsx</code>."),
        ("2. Ajuste no Power Query",
         "Marque as 8 abas de dados, sem a aba <code>LEIA-ME</code>. Em cada "
         "tabela, confirme o cabeçalho, ajuste os tipos e renomeie a consulta. "
         "Ao final, clique em <b>Fechar e Aplicar</b>."),
        ("3. Modele",
         "No modo <b>Modelo</b>, crie os relacionamentos de 1:N das dimensões "
         "para a fato. Confira se a direção do filtro está correta."),
        ("4. Crie as medidas",
         "Em <b>Modelagem &rarr; Nova medida</b>, insira as oito medidas da "
         "seção anterior. Organize todas em uma tabela de medidas chamada "
         "<code>_Medidas</code>."),
        ("5. Monte os visuais",
         "Arraste os campos para os cinco visuais do layout. Formate títulos, "
         "cores e casas decimais."),
        ("6. Adicione filtros",
         "Inclua segmentações de <b>etapa</b>, <b>unidade</b> e <b>ano</b>. "
         "Depois, teste o painel com um filtro aplicado."),
        ("7. Publique, se necessário",
         "No Power BI Service, publique em um workspace da unidade e configure "
         "a atualização agendada da origem."),
        ("8. Salve o .pbix",
         "Guarde o arquivo com o nome do processo. O <code>.pbix</code> é a "
         "fonte do painel, e o caderno é o guia de montagem."),
    ]) +
    callout("err", "Não marque abas de outro cenário",
        "Cada workbook tem a sua própria contagem de linhas. Se o Power Query "
        "mostrar mais do que o esperado, você marcou uma aba de outro arquivo "
        "ou combinou workbooks. Confira os totais: <b>10.352</b> (C1), "
        "<b>9.541</b> (C2), <b>10.840</b> (C3), <b>12.664</b> (C4) e "
        "<b>13.896</b> (C5).")
)

cad.section("ler-painel", "Como ler o painel em 60 segundos",
    p("Abrir o painel e decorar números não é ler. Ler é seguir uma ordem fixa "
      "de perguntas, sempre a mesma. Dessa forma, a reunião começa no problema, "
      "e não no gráfico que chama mais atenção.") +
    step([
        ("Olhe o TAT e o % Espera",
         "Se a espera passa de 80% do tempo, o problema está na fila, e não no "
         "trabalho. Essa leitura muda o rumo da conversa."),
        ("Ordene a espera por etapa",
         "A primeira barra do Pareto é o gargalo. Se ela concentra mais de 30% "
         "da espera, você já sabe onde intervir."),
        ("Compare com o volume de casos",
         "Espera alta em uma etapa com poucos casos pode ser um caso isolado. "
         "Espera alta com volume alto indica problema sistêmico."),
        ("Cheque o retrabalho",
         "Retrabalho alto na mesma unidade do gargalo sugere causa comum, como "
         "checklist, formulário ou critério de aceitação."),
        ("Escreva a hipótese em uma frase",
         "&quot;O caso espera X horas na etapa Y, que concentra Z% da espera; a "
         "causa provável é W.&quot; Se a frase não sai, o painel ainda não foi "
         "lido."),
    ]) +
    tbl(["O que você vê", "O que significa", "O que fazer"],
        [["Espera alta e execução baixa", "Fila: falta capacidade ou prioridade", "Redesenhar a fila no TO-BE"],
         ["Execução alta e espera baixa", "Trabalho manual intenso", "Automatizar ou simplificar a tarefa"],
         ["Retrabalho alto", "Erro ou critério ausente", "Checklist e validação na entrada"],
         ["TAT estável e alto", "Processo crônico", "Meta e intervenção estrutural"],
         ["TAT caindo no tempo", "A intervenção funcionou", "Documentar e replicar"]],
        num_cols=[]) +
    callout("tip", "O painel é o começo da conversa",
        "O painel não entrega a causa raiz. Ele entrega o onde. A causa raiz "
        "vem da conversa com quem executa, nos Labs 4 e 5. Por isso, use o "
        "painel para fazer a pergunta certa, e não para encerrar o assunto.")
)

# =================================================================
# PARTE 2 - MANHA: AS 5 RECEITAS DE PAINEL
# =================================================================
cad.grp("Parte 2 - Manhã: as 5 receitas de painel",
        "Cinco workbooks, um mesmo esquema e cinco painéis: do Excel ao dashboard, com o passo a passo completo.")

cad.section("receitas-intro", "As 5 receitas: escolha o seu dataset",
    p("Cada receita abaixo é autossuficiente. Ela abre o workbook, importa as "
      "abas, modela os dados, cria as medidas e monta o painel. As cinco usam "
      "o mesmo esquema, com a fato e as 7 dimensões. Por isso, o que você "
      "aprende em uma receita serve para as outras; mudam o nome das etapas e "
      "o gargalo.") +
    tbl(["#", "Dataset", "Workbook", "Execuções", "Gargalo medido"],
        [["<b>1</b>", "Requisição pericial", "<a href='datasets/cenario1_processo_pericial/Cenario1_Requisicao_Pericial.xlsx'><code>Cenario1_Requisicao_Pericial.xlsx</code></a>", "10.352", "Fila perito (41,5%)"],
         ["<b>2</b>", "Empenho e contrato", "<a href='datasets/cenario2_processo_orcamento/Cenario2_Empenho_Contrato.xlsx'><code>Cenario2_Empenho_Contrato.xlsx</code></a>", "9.541", "Parecer + Autorização (51,2%)"],
         ["<b>3</b>", "Cadeia de custódia", "<a href='datasets/cenario3_processo_custodia/Cenario3_Cadeia_Custodia.xlsx'><code>Cenario3_Cadeia_Custodia.xlsx</code></a>", "10.840", "Guarda (35,3%)"],
         ["<b>4</b>", "Local de crime", "<a href='datasets/cenario4_local_crime/Cenario4_Local_Crime.xlsx'><code>Cenario4_Local_Crime.xlsx</code></a>", "12.664", "Deslocamento (35,2%)"],
         ["<b>5</b>", "Análise laboratorial", "<a href='datasets/cenario5_analise_laboratorial/Cenario5_Analise_Laboratorial.xlsx'><code>Cenario5_Analise_Laboratorial.xlsx</code></a>", "13.896", "Equipamento (47,1%)"]],
        num_cols=[]) +
    callout("tip", "Como usar em sala",
        "O professor conduz a <b>Receita 1</b> na tela, e as equipes repetem "
        "as <b>Receitas 2 a 5</b> no próprio ritmo. Quem termina antes ajuda o "
        "vizinho. Dessa forma, o objetivo é que todos saiam com um painel em "
        "funcionamento, e não com uma captura de tela.") +
    checklist([
        "Um workbook por equipe, ou um cenário por pessoa.",
        "Power BI Desktop instalado, conforme o Dia 4.",
        "A Parte 1 deste caderno aberta como referência das 8 medidas base.",
        "A tabela de resultado esperado de cada receita para conferir o painel.",
    ]) +
    aplicab(
        "Em qualquer unidade que receba o dataset e queira reproduzir o painel sozinha.",
        "A receita é um roteiro repetível, com o mesmo modelo, as mesmas medidas e os mesmos visuais.",
        "A equipe do IML usa a Receita 1; a equipe de compras usa a Receita 2; "
        "a custódia usa a 3; a equipe de campo usa a 4; os laboratórios usam a 5.")
)


DAX_PARETO = (
    "Rank da Etapa (espera) =\n"
    "RANKX(\n"
    "    ALL(dim_etapa[etapa]),\n"
    "    CALCULATE([Tempo Espera (h)]),\n"
    "    ,\n"
    "    DESC\n"
    ")\n"
    "\n"
    "% Acumulado da Espera =\n"
    "VAR RankAtual =\n"
    "    RANKX(\n"
    "        ALL(dim_etapa[etapa]),\n"
    "        CALCULATE([Tempo Espera (h)]),\n"
    "        ,\n"
    "        DESC\n"
    "    )\n"
    "VAR EsperaAcumulada =\n"
    "    CALCULATE(\n"
    "        [Tempo Espera (h)],\n"
    "        FILTER(\n"
    "            ALL(dim_etapa),\n"
    "            RANKX(\n"
    "                ALL(dim_etapa[etapa]),\n"
    "                CALCULATE([Tempo Espera (h)]),\n"
    "                ,\n"
    "                DESC\n"
    "            ) <= RankAtual\n"
    "        )\n"
    "    )\n"
    "RETURN\n"
    "    DIVIDE(\n"
    "        EsperaAcumulada,\n"
    "        CALCULATE([Tempo Espera (h)], ALL(dim_etapa))\n"
    "    )\n"
    "\n"
    "Espera por Etapa (h) =\n"
    "CALCULATE([Tempo Espera (h)], ALL(dim_etapa))"
)


def receita(anchor, titulo, contexto, prova, abas, medidas, resultado, armadilha,
            foco, workbook, linhas, entrega):
    cad.section(anchor, titulo,
        p(contexto) +
        ficha("a", "O que o painel precisa provar", prova) +
        tbl(["Aba", "Grão", "Uso no painel"], abas, num_cols=[]) +
        callout("note", "Como usar esta receita",
            "Os 8 blocos abaixo formam o roteiro completo, do arquivo do Excel "
            "ao painel publicado. Cada bloco traz o caminho do menu e o que "
            "esperar na tela. Sugestão de tempo: 3 horas no total, em uma "
            "turma de 4 horas. Se um bloco travar, pule para o próximo e volte "
            "depois: o painel só fecha no fim.") +

        h3("Bloco 1 - Prepare o arquivo no Excel (10 min)") +
        step([
            ("1.1. Abra o workbook e localize a pasta",
             "Abra <code>" + workbook + "</code>. Ele fica em "
             "<code>Aula 6/datasets/</code>, dentro da pasta do cenário. Se "
             "preferir, use o link do arquivo na tabela da Parte 2."),
            ("1.2. Leia a aba LEIA-ME",
             "A aba <code>LEIA-ME</code> tem o dicionário das tabelas, a "
             "contagem de linhas de cada uma e a tabela-resumo com os tempos "
             "medidos por etapa. Essa tabela é o gabarito do seu painel: use "
             "ela para conferir o resultado no final."),
            ("1.3. Confira as 9 abas",
             "Você verá <code>LEIA-ME</code>, <code>fato_execucao</code> e as 7 "
             "dimensões. Expanda a <code>fato_execucao</code> e confirme que a "
             "linha de cabeçalho tem 16 colunas e que a contagem bate com a "
             "aba <code>LEIA-ME</code>: " + linhas + " linhas."),
            ("1.4. Confira a coluna etapa_key",
             "Abra a aba <code>dim_etapa</code> e veja que a coluna "
             "<code>etapa_key</code> vai de 1 a 8 e que a coluna "
             "<code>sequencia</code> dá a ordem do processo. É pela "
             "<code>sequencia</code> que o Pareto será ordenado."),
            ("1.5. Feche o Excel",
             "Não é preciso alterar nada no arquivo. Ele é a fonte, e o "
             "Power BI vai ler direto dele. Se você fechar o Excel com o "
             "arquivo aberto, o Power BI continua lendo; apenas o desempenho "
             "cai um pouco."),
        ]) +

        h3("Bloco 2 - Importe os dados no Power BI (20 min)") +
        step([
            ("2.1. Crie o arquivo e salve antes de importar",
             "<b>Arquivo &rarr; Novo</b> e, logo depois, <b>Arquivo &rarr; Salvar "
             "como</b>. Nomeie <code>Painel_" + foco.replace(" ", "_") +
             ".pbix</code> e escolha uma pasta do seu computador. Salvar no "
             "início evita perder trabalho se o Power BI travar."),
            ("2.2. Abra o conector de pasta de trabalho do Excel",
             "<b>Pagina Inicial &rarr; Obter dados &rarr; Mais</b> e procure por "
             "<b>Pasta de trabalho do Excel</b>. Essa opção abre o navegador de "
             "arquivos e mostra as abas de todos os workbooks da pasta."),
            ("2.3. Aponte para o arquivo",
             "Navegue até a pasta do cenário, selecione <code>" + workbook +
             "</code> e clique em <b>Abrir</b>. Não selecione a pasta inteira: "
             "se o conector apontar para a pasta, ele trará o LEIA-ME e "
             "misturará cenários."),
            ("2.4. Escolha as abas no navegador",
             "Aparecerá uma lista com as 9 abas. Marque <b>fato_execucao</b> e as "
             "7 <code>dim_*</code>. Use <b>Ctrl</b> (ou <b>Shift</b>) para marcar "
             "várias de uma vez. <b>Desmarque <code>LEIA-ME></code></b>: essa aba "
             "é documentação e, se entrar, cria uma tabela vazia no modelo."),
            ("2.5. Confira a pré-visualização",
             "Cada aba marcada mostra a primeira linha de dados. Confirme que a "
             "fato tem 16 colunas e que as dimensões têm 2 a 10 colunas. Se "
             "alguma aba vier vazia, o problema é o arquivo, não a importação."),
            ("2.6. Carregue e espere",
             "Clique em <b>Carregar</b>. O Power BI abre o Power Query com 8 "
             "consultas, uma por aba. Aguarde o carregamento terminar antes de "
             "qualquer edição."),
            ("2.7. Renomeie as consultas",
             "No painel de <b>Consultas</b> (à esquerda), clique com o botão "
             "direito em cada consulta e escolha <b>Renomear</b>. Use "
             "<code>fato</code> para a fato e o nome curto da dimensão nas "
             "demais: <code>etapa</code>, <code>unidade</code>, <code>sistema</code>, "
             "<code>tipo</code>, <code>status</code>, <code>projeto</code> e "
             "<code>calendario</code>. O nome aparece no modelo e nos gráficos."),
            ("2.8. Confira a contagem de cada consulta",
             "No rodapé do Power Query, a consulta <code>fato</code> deve "
             "mostrar " + linhas + " linhas. Se mostrar mais, alguma aba foi "
             "marcada duas vezes ou a tabela veio de outro cenário."),
        ]) +

        h3("Bloco 3 - Trate os dados no Power Query (20 min)") +
        step([
            ("3.1. Use a primeira linha como cabeçalho",
             "Com a consulta <code>fato</code> selecionada, vá em <b>Início &rarr; "
             "Usar Primeira Linha como Cabeçalho</b>. O mesmo para as 7 "
             "dimensões. Sem isso, os nomes das colunas viram V1, V2, V3."),
            ("3.2. Confira os tipos de dado",
             "Selecione uma coluna e olhe o tipo no topo da faixa de opções. "
             "Tempos e custo devem ser <b>Número Decimal</b>; chaves, "
             "<b>Número Inteiro</b>; <code>data</code> em <code>dim_calendario</code>, "
             "<b>Data</b>; flags, <b>Número Inteiro</b>."),
            ("3.3. Corrija o tipo da coluna data",
             "Em <code>dim_calendario</code>, clique com o botão direito no "
             "cabeçalho de <code>data</code> e escolha <b>Alterar tipo &rarr; Data</b>. "
             "O formato do Brasil é <b>dd/mm/aaaa</b>. Depois, em <b>Colunas "
             "Especiais &rarr; Ano e Mês</b>, extraia também <b>Ano</b> e "
             "<b>Nome do Mês</b>."),
            ("3.4. Remova colunas que não serão usadas",
             "Em cada dimensão, clique com o botão direito no cabeçalho e "
             "desmarque as colunas que o painel não usa. Menos colunas significam "
             "modelo mais leve e leitura mais rápida."),
            ("3.5. Remova linhas em branco",
             "Em <b>Início &rarr; Remover Linhas &rarr; Remover Linhas em Branco</b>. "
             "O arquivo vem limpo, mas essa verificação evita erro de contagem."),
            ("3.6. Marque a tabela de datas",
             "Isso é feito no Power BI, e não no Power Query: selecione a "
             "consulta <code>calendario</code> e use <b>Ferramenta de Tabela "
             "de Datas</b> na guia <b>Modelagem</b>. Escolha a coluna "
             "<code>data</code> e confirme. O aviso some e a segmentação de ano "
             "passa a funcionar."),
            ("3.7. Feche e aplique",
             "<b>Início &rarr; Fechar e Aplicar</b>. O modelo aparece com 8 "
             "tabelas. Se o Power BI mostrar aviso de tipo misto, volte ao "
             "Power Query e corrija a coluna indicada."),
            ("3.8. Use o botão de Editar consultas quando precisar",
             "Se algo mudar no arquivo do Excel, você não precisa reimportar. "
             "Clique com o botão direito na consulta e escolha <b>Editar "
             "consultas</b>. O histórico de etapas fica registrado no botão "
             "<b>Etapas aplicadas</b>."),
        ]) +

        h3("Bloco 4 - Monte o modelo (15 min)") +
        step([
            ("4.1. Vá para o modo Modelo",
             "No canto inferior esquerdo, use <b>Modelo</b>. As tabelas aparecem "
             "como caixas."),
            ("4.2. Crie a relação da etapa",
             "Arraste o campo <code>etapa_key</code> da tabela <code>fato</code> "
             "até o campo <code>etapa_key</code> da tabela <code>etapa</code>. "
             "Surgem três caixas de configuração: <b>1:1</b>, <b>1:* (muitos para "
             "um)</b> e <b>*:1</b>. Escolha <b>1:*</b>, que é o padrão correto "
             "para dimensão e fato."),
            ("4.3. Crie as outras seis relações do mesmo jeito",
             "Repita o arraste para <code>unidade_key</code>, "
             "<code>sistema_key</code>, <code>tipo_atividade_key</code>, "
             "<code>status_execucao_key</code> e <code>projeto_key</code>. "
             "Ao final, a fato tem 6 relações de 1 para muitos."),
            ("4.4. Crie a relação com o calendário",
             "Arraste <code>data_inicio_key</code> da fato até <code>data_key</code> "
             "do <code>calendario</code>. Deixe a cardinalidade em 1:* e a "
             "direção de filtro única, com a tabela dimensional filtrando a "
             "fato."),
            ("4.5. Confira o sentido do filtro",
             "Com a relação selecionada, veja a seta na linha. Ela deve apontar "
             "da dimensão para a fato. Se inverter, a segmentação de ano "
             "deixará de filtrar o gráfico."),
            ("4.6. Marque o calendário como tabela de datas",
             "Selecione a tabela <code>calendario</code> e use <b>Modelagem "
             "&rarr; Marcar como tabela de datas</b>. Escolha a coluna "
             "<code>data</code>."),
            ("4.7. Esconda as chaves",
             "No painel de campos, clique na seta de contexto ao lado de "
             "<code>etapa_key</code>, <code>unidade_key</code> e das outras "
             "chaves, e escolha <b>Ocultar no relatório</b>. As chaves "
             "permanecem no modelo, mas saem dos campos visíveis."),
            ("4.8. Renomeie a tabela de medidas",
             "Ainda não existe tabela de medidas. Crie uma agora, como no Bloco "
             "5, e dê o nome <code>_Medidas</code>. O nome com underscore "
             "sinaliza que é tabela auxiliar."),
            ("4.9. Verifique a integridade do modelo",
             "Use <b>Modelagem &rarr; Verificar o modelo</b> ou passe o mouse "
             "pelo relationships. O aviso de cardinalidade many-to-many não deve "
             "aparecer. Se aparecer, é porque a direção do filtro ficou "
             "duplicada."),
            ("4.10. Salve",
             "<b>Arquivo &rarr; Salvar</b> (Ctrl+S). A partir daqui, qualquer "
             "erro de modelo aparece como número errado no painel, e o lugar "
             "mais provável é a relação."),
        ]) +

        h3("Bloco 5 - Crie as medidas (25 min)") +
        step([
            ("5.1. Crie a tabela de medidas",
             "<b>Modelagem &rarr; Inserir tabela de cálculo</b> e nomeie "
             "<code>_Medidas</code>. Todas as medidas criadas a seguir vão "
             "para essa tabela."),
            ("5.2. Crie as três medidas de tempo",
             "Com <b>Nova medida</b>, cole uma medida por vez. <b>Tempo Espera "
             "(h)</b> e <b>Tempo Execução (h)</b> convertem minutos em horas, e "
             "<b>Tempo Total (h)</b> soma as duas. O código está na Parte 1."),
            ("5.3. Crie as cinco medidas de leitura",
             "<b>% Espera</b>, <b>Casos</b>, <b>TAT Médio (h)</b>, <b>Espera "
             "Média (h)</b> e <b>Taxa Retrabalho</b>. Use o <code>DIVIDE</code> "
             "em todas as razões, para não aparecer erro de divisão por zero."),
            ("5.4. Formate as medidas",
             "Selecione a medida e use <b>Ferramenta de Medida &rarr; Formatar</b>. "
             "Horas e percentuais com uma casa decimal, e a contagem de casos "
             "com separador de milhar. Sem formatação, o cartão mostra 44,1768."),
            ("5.5. Organize as medidas em pastas",
             "Na barra de fórmulas, use <b>Criar pasta</b> para separar por "
             "tema: <code>Tempo</code>, <code>Leitura</code> e <code>Pareto</code>. "
             "Com 10+ medidas, a pasta economiza muito tempo de quem vai "
             "montar o painel depois."),
            ("5.6. Teste cada medida em uma tabela",
             "Insira um visual de tabela vazio, arraste <code>etapa</code> e a "
             "medida, e confira o valor contra a tabela-resumo da aba "
             "<code>LEIA-ME</code>. É o teste mais rápido para achar erro de "
             "medida ou de filtro."),
            ("5.7. Crie as medidas do Pareto",
             "Cole as três medidas do gráfico de Pareto que estão na próxima "
             "seção: <b>Rank da Etapa</b>, <b>% Acumulado da Espera</b> e "
             "<b>Espera por Etapa</b>."),
            ("5.8. Crie as medidas específicas do cenário",
             "Cole as medidas específicas deste dataset, que estão na seção "
             "seguinte. Elas respondem à pergunta que só este processo faz."),
            ("5.9. Escreva um comentário em cada medida",
             "No botão de comentário ao lado do nome da medida, escreva uma "
             "frase com o que ela responde. Quem abrir o painel depois entende "
             "a regra sem ler o código."),
        ]) +

        h3("Bloco 6 - Monte o painel (60 min)") +
        step([
            ("6.1. Configure a página antes de inserir visuais",
             "<b>Modelagem &rarr; Tamanho da página</b> ou, no modo Exibir, "
             "<b>Página &rarr; Tamanho da página</b>. Use <b>16:9</b> ou o "
             "<b>Toolbox do telefone</b> se o painel for para celular."),
            ("6.2. Insira os quatro cartões",
             "<b>Exibir &rarr; Cartão</b>. Em cada um, arraste uma medida para "
             "<b>Valores</b>. Deixe o nome do cartão com a medida para não "
             "duplicar o rótulo. Formate o número em <b>Ferramenta de cartão "
             "&rarr; Formatar</b>."),
            ("6.3. Posicione os cartões em linha",
             "Arraste os cartões para o topo da página, alinhados. Use "
             "<b>Exibir &rarr; Alinhar</b> e <b>Distribuir horizontalmente</b> "
             "para dar espaçamento igual."),
            ("6.4. Monte as barras empilhadas",
             "<b>Exibir &rarr; Gráfico de barras empilhadas</b>. Arraste "
             "<code>etapa</code> para <b>Eixo Y</b> e as duas medidas de tempo "
             "para <b>Valores</b>. O Power BI empilha espera sobre execução, e "
             "a etapa mais alta é a que mais espera."),
            ("6.5. Ordene as etapas pela sequência do processo",
             "Clique com o botão direito em <code>etapa</code> no painel de "
             "campos e escolha <b>Classificar por coluna &rarr; sequencia</b>. "
             "Assim, as etapas aparecem na ordem do fluxo, e não em ordem "
             "alfabética."),
            ("6.6. Destaque a etapa do gargalo",
             "No visual de barras, selecione a barra da etapa " + foco + " e "
             "use <b>Formatar &rarr; Barra &rarr; Cores</b>. Escolha uma cor de "
             "destaque e deixe as demais na cor padrão."),
            ("6.7. Monte o Pareto",
             "<b>Exibir &rarr; Gráfico de barras e colunas</b>. No visual, use "
             "<b>Adicionar valor ao eixo secundário</b> no botão de Analyze do "
             "canto superior direito. Arraste <b>Espera por Etapa (h)</b> para "
             "o eixo Y primário e <b>% Acumulado da Espera</b> para o eixo Y "
             "secundário."),
            ("6.8. Ajuste a escala do eixo secundário",
             "Com o eixo secundário selecionado, use <b>Formatar &rarr; Eixo "
             "Y &rarr; Escala</b> e fixe o mínimo em 0% e o máximo em 100%. "
             "Com isso, a linha de acumulado sai de 0 a 100 e passa pelo topo "
             "do gráfico."),
            ("6.9. Ordene o Pareto pelo volume, não pelo eixo",
             "Clique com o botão direito em <b>Espera por Etapa (h)</b> e "
             "escolha <b>Classificar por valor &rarr; Descendente</b>. A ordem "
             "passa a ser pela espera, que é a ordem do Pareto."),
            ("6.10. Monte a linha do tempo",
             "<b>Exibir &rarr; Gráfico de linhas</b>. Arraste "
             "<code>ano_mes</code> do <code>calendario</code> para o eixo X e "
             "<b>TAT Médio (h)</b> para os valores."),
            ("6.11. Adicione a linha de meta",
             "Com o visual selecionado, use <b>Analisar &rarr; Linha de análise "
             "&rarr; Linha de referência constante</b> e informe o valor da meta. "
             "Ou, se preferir uma meta por mês, crie a medida "
             "<b>Meta de TAT (h)</b> e arraste-a para o eixo Y."),
            ("6.12. Monte a matriz de retrabalho",
             "<b>Exibir &rarr; Matriz</b>. Arraste <code>unidade</code> para "
             "<b>Linhas</b>, <code>etapa</code> para <b>Colunas</b> e "
             "<b>Taxa Retrabalho</b> para <b>Valores</b>."),
            ("6.13. Aplique a escala de cor na matriz",
             "No visual, use <b>Ferramenta de matriz &rarr; Formatar &rarr; "
             "Células &rarr; Escala de cores</b>. Escolha uma escala de duas "
             "cores, em que o claro é o mínimo e o escuro é o máximo. A célula "
             "mais escara aponta a unidade com mais retrabalho."),
            ("6.14. Escreva o título e o subtítulo da página",
             "Use <b>Exibir &rarr; Cartões de texto</b> acima dos cartões. O "
             "título diz o que o painel mede, e o subtítulo diz o recorte: "
             "período, unidade e o que a página responde."),
        ]) +

        h3("Bloco 7 - Filtros, segmentações e tabela resumo (20 min)") +
        step([
            ("7.1. Insira as segmentações",
             "<b>Exibir &rarr; Segmentação de dados</b>, uma para cada campo: "
             "<code>etapa</code>, <code>unidade</code> e <code>ano</code>. "
             "Arraste o campo para o visual e o visual para a área da "
             "segmentação."),
            ("7.2. Formate as segmentações",
             "Em <b>Ferramenta de segmentação &rarr; Formatar &rarr; "
             "Segmentação</b>, escolha o estilo <b>Antes e depois</b> ou "
             "<b>Lista suspensa</b>, com borda e texto na cor da marca."),
            ("7.3. Sincronize as segmentações entre as páginas",
             "No painel de segmentações, use o botão <b>Sincronizar segmentações "
             "de dados</b> (ícone de elos) na parte superior. As páginas de "
             "detalhe passam a respeitar o filtro das páginas de resumo."),
            ("7.4. Defina os filtros de relatório e de página",
             "Abra <b>Painel de filtros</b> (Exibir &rarr; Filtros). No nível "
             "<b>Todos os relatórios</b>, mantenha só o que vale para o painel "
             "inteiro. No nível da página, defina o recorte padrão."),
            ("7.5. Configure as interações entre visuais",
             "Clique com o botão direito em um visual e escolha <b>Editar "
             "interações</b>. A janela lista os visuais da página, e cada "
             "checkbox liga ou desliga o filtro. Por padrão, clicar no cartão "
             "de TAT filtra todos os gráficos, o que é o comportamento "
             "desejado neste painel."),
            ("7.6. Monte a tabela resumo",
             "<b>Exibir &rarr; Tabela</b>. Arraste <code>etapa</code> para as "
             "colunas e, para cada medida, <b>Valores &rarr; Mais valores</b>. "
             "A ordem final é: etapa, espera, execução, "
             "% espera e taxa de retrabalho."),
            ("7.7. Ordene a tabela pela espera",
             "Clique com o botão direito no cabeçalho da coluna de espera e "
             "escolha <b>Classificar por valor &rarr; Descendente</b>. A "
             "primeira linha passa a ser o gargalo, e a tabela vira o resumo "
             "executivo do painel."),
            ("7.8. Formate a tabela",
             "Em <b>Ferramenta de tabela &rarr; Formatar</b>, ative "
             "<b>Linhas de cabeçalho</b>, desative as bordas e use "
             "<b>Formatação condicional &rarr; Barras de dados</b> na coluna "
             "de espera. O resultado é uma tabela que mostra o ranking sem "
             "precisar de gráfico."),
            ("7.9. Teste a tabela contra a aba LEIA-ME",
             "Compare a tabela resumo com a tabela da aba <code>LEIA-ME</code> "
             "do workbook. Os números da espera, da execução e do retrabalho "
             "têm de ser iguais. Se não forem, o problema está no modelo, e "
             "não no visual."),
        ]) +

        h3("Bloco 8 - Formate, salve e publique (20 min)") +
        step([
            ("8.1. Crie uma segunda página para o detalhe",
             "Duplique a página com <b>Exibir &rarr; Página &rarr; Duplicar "
             "página</b> e mantenha apenas a matriz e a tabela resumo. A "
             "primeira página fica com o resumo, e a segunda com o detalhe."),
            ("8.2. Esconda a página de detalhe do menu",
             "Com a página de detalhe selecionada, desmarque <b>Permitir "
             "alterações de layout</b> e, em <b>Configurações da página "
             "&rarr; Ocultar página</b>, marque a opção de ocultar. O menu de "
             "páginas mostra só a visão de resumo."),
            ("8.3. Aplique um tema ao painel",
             "Em <b>Exibir &rarr; Temas</b>, escolha um tema ou crie um com a "
             "cor da instituição. O tema formata cores, fontes e o plano de "
             "fundo de uma vez."),
            ("8.4. Revise a acessibilidade",
             "Em <b>Exibir &rarr; Painel de acessibilidade</b>, confira os "
             "itens marcados. O mais comum é a ordem dos objetos, que se ajusta "
             "com <b>Painel de seleção</b>."),
            ("8.5. Salve o arquivo do Power BI",
             "<b>Arquivo &rarr; Salvar</b>. O <code>.pbix</code> guarda o "
             "modelo, as medidas e o layout, e é o arquivo que se entrega."),
            ("8.6. Publique no Power BI Service, se necessário",
             "<b>Arquivo &rarr; Publicar</b> e escolha o workspace da unidade. "
             "Na primeira publicação, o Power BI pergunta se o gateway é "
             "local ou em nuvem, e se os dados serão atualizados "
             "automaticamente."),
            ("8.7. Agende a atualização, se a origem mudar",
             "No workspace, abra a configuração do conjunto de dados e agende a "
             "atualização. Para arquivos em rede, é preciso instalar o Gateway "
             "na máquina que tem a pasta."),
            ("8.8. Verifique no celular",
             "No Service, use <b>Painel &rarr; Exibir &rarr; Dispositivo "
             "móvel</b> para conferir o layout em tela pequena. Se a página "
             "não couber, reduza a quantidade de visuais ou use a página de "
             "detalhe."),
            ("8.9. Registre o resultado",
             "Anote no caderno, na coluna de resultado esperado, o número que "
             "você mediu. Esse número é a linha de base do TO-BE, e é com ele "
             "que o ganho da tarde será calculado."),
        ]) +

        h3("As medidas do gráfico de Pareto") +
        code(DAX_PARETO, "dax") +
        h3("As medidas específicas deste cenário") +
        code(medidas, "dax") +
        h3("Os 5 visuais e a tabela resumo") +
        tbl(["Visual", "Campos", "Pergunta"],
            [["Cartões", "TAT Médio, % Espera, Casos, Taxa Retrabalho", "Como está o processo?"],
             ["Barras empilhadas", "Etapa, Espera e Execução", "Onde o caso espera?"],
             ["Pareto", "Etapa, Espera por Etapa e % Acumulado", "Quais poucas etapas importam?"],
             ["Linha do tempo", "Ano e mês, TAT Médio", "Melhorou ou piorou?"],
             ["Matriz", "Unidade, Etapa e Taxa Retrabalho", "Quem concentra o retrabalho?"],
             ["Tabela resumo", "Etapa, Espera, Execução, % Espera e Retrabalho", "Qual é o retrato final?"]],
            num_cols=[]) +
        h3("Resultado esperado (confira o seu painel)") +
        tbl(["Indicador", "Valor medido", "Leitura"], resultado, num_cols=[1]) +
        callout("err", "A armadilha deste dataset", armadilha) +
        checklist(entrega)
    )


receita(
    "receita-1-pericial",
    "Receita 1: Requisição pericial (10.352 execuções)",
    "Este é o fluxo mais conhecido da POLITEC, que vai da delegacia até a "
    "assinatura do laudo. O painel precisa mostrar que o problema está na "
    "fila, e não no trabalho do perito.",
    "A Fila perito concentra 41,5% de toda a espera, enquanto a Análise tem o "
    "maior tempo de execução. Por isso, o painel precisa deixar essa diferença "
    "visível em uma única leitura.",
    [["<code>fato_execucao</code>", "1 execução de etapa", "Tempos, retrabalho e custo"],
     ["<code>dim_etapa</code>", "1 etapa (8)", "Nome, sequência e unidade padrão"],
     ["<code>dim_unidade</code>", "1 unidade (7)", "Laboratórios, ATO, IML e campo"],
     ["<code>dim_sistema</code>", "1 sistema (6)", "Quanto ainda passa por papel e Excel"],
     ["<code>dim_calendario</code>", "1 dia (1.096)", "TAT por mês e sazonalidade"]],
    "Espera Fila Perito (h) =\n"
    "    CALCULATE([Tempo Espera (h)], dim_etapa[etapa] = \"Fila perito\")\n"
    "\n"
    "Peso Fila Perito =\n"
    "    DIVIDE([Espera Fila Perito (h)], [Tempo Espera (h)])\n"
    "\n"
    "Fila vs Analise =\n"
    "    DIVIDE(\n"
    "        [Espera Fila Perito (h)],\n"
    "        CALCULATE([Tempo Execucao (h)], dim_etapa[etapa] = \"Analise\")\n"
    "    )",
    [["Execuções", "10.352", "Contagem da fato, que você confere no Power Query"],
     ["% espera", "92,4%", "Quase todo o tempo é fila"],
     ["Fila perito", "44,2 h e 41,5%", "Maior espera média e maior participação"],
     ["Revisão", "13,1 h e 12,3%", "Segundo maior bloco de espera"],
     ["Análise", "4,8 h de execução", "Maior trabalho manual, mas não é o gargalo"],
     ["TAT médio por caso", "497,2 h", "Espera mais execução, dividido por 300 casos"],
     ["Retrabalho", "11,6%", "Sistêmico, com taxa parecida em todas as etapas"]],
    "Não confunda a etapa que mais executa, a Análise, com a etapa que mais "
    "espera, a Fila perito. Se o seu Pareto mostrar a Análise em primeiro "
    "lugar, você provavelmente somou execução em vez de espera.",
    "Fila perito",
    "Cenario1_Requisicao_Pericial.xlsx",
    "10.352",
    ["Workbook importado com 8 abas e 10.352 linhas na fato.",
     "Relacionamentos criados e dim_calendario marcada como tabela de datas.",
     "8 medidas base e 3 medidas do cenário.",
     "4 cartões, barras empilhadas, Pareto, linha do tempo e matriz.",
     "Tabela resumo e 3 segmentações: etapa, unidade e ano.",
     "Números conferem com a tabela de resultado esperado."]
)

receita(
    "receita-2-orcamento",
    "Receita 2: Empenho e contrato (9.541 execuções)",
    "Este é o caminho do dinheiro público, que passa por pedido, cotação, "
    "mapa, parecer, autorização, empenho e publicação. O painel precisa "
    "mostrar que o problema está nas aprovações encadeadas, e não no mapa "
    "comparativo.",
    "Parecer e autorização, juntos, concentram 51,2% da espera. Por isso, o "
    "painel precisa somar as duas etapas em uma medida própria, porque no "
    "Pareto elas aparecem separadas.",
    [["<code>fato_execucao</code>", "1 execução de etapa", "Tempos, retrabalho e custo"],
     ["<code>dim_etapa</code>", "1 etapa (7)", "Pedido, cotação, mapa, parecer, autorização e outras"],
     ["<code>dim_unidade</code>", "1 unidade (5)", "Compras, Diretoria, Jurídico e Controle"],
     ["<code>dim_sistema</code>", "1 sistema (6)", "Excel e e-mail concentram a espera"],
     ["<code>dim_calendario</code>", "1 dia (1.096)", "Evolução do TAT no tempo"]],
    "Espera Aprovacoes (h) =\n"
    "    CALCULATE(\n"
    "        [Tempo Espera (h)],\n"
    "        dim_etapa[etapa] IN {\"Parecer\", \"Autorizacao\"}\n"
    "    )\n"
    "\n"
    "Peso Aprovacoes =\n"
    "    DIVIDE([Espera Aprovacoes (h)], [Tempo Espera (h)])\n"
    "\n"
    "Mapa vs Parecer =\n"
    "    DIVIDE(\n"
    "        CALCULATE([Tempo Execucao (h)], dim_etapa[etapa] = \"Mapa\"),\n"
    "        CALCULATE([Tempo Execucao (h)], dim_etapa[etapa] = \"Parecer\")\n"
    "    )",
    [["Execuções", "9.541", "Contagem da fato"],
     ["% espera", "88,1%", "O processo é dominado por fila"],
     ["Parecer", "35,9 h e 29,3%", "Maior espera isolada"],
     ["Autorização", "26,8 h e 21,9%", "Segunda maior espera"],
     ["Parecer e autorização", "51,2%", "A medida de aprovações revela o conjunto"],
     ["Mapa", "6,1 h de execução", "Maior trabalho manual do processo"],
     ["TAT médio por caso", "757,4 h", "Espera mais execução, dividido por 250 casos"],
     ["Retrabalho", "16,6%", "A maior taxa entre os cinco datasets"]],
    "O Pareto mostra Parecer e Autorização como duas barras. Se você olhar "
    "apenas a primeira, perde metade do problema. Por isso, crie a medida "
    "<code>Espera Aprovacoes</code> para ver as duas etapas juntas.",
    "Parecer + Autorização",
    "Cenario2_Empenho_Contrato.xlsx",
    "9.541",
    ["Workbook importado com 8 abas e 9.541 linhas na fato.",
     "Relacionamentos criados e dim_calendario marcada como tabela de datas.",
     "8 medidas base e 3 medidas do cenário.",
     "4 cartões, barras empilhadas, Pareto, linha do tempo e matriz.",
     "Tabela resumo e 3 segmentações: etapa, unidade e ano.",
     "Números conferem com a tabela de resultado esperado."]
)

receita(
    "receita-3-custodia",
    "Receita 3: Cadeia de custódia (10.840 execuções)",
    "Este processo vai da coleta no local até a baixa da evidência. O painel "
    "mede tempo e rastreabilidade. A guarda é a etapa que mais retém a "
    "evidência, e a divergência de lacre é um status que precisa de medida "
    "própria.",
    "A Guarda concentra 35,3% da espera. A divergência de lacre aparece em "
    "poucas execuções, mas tem impacto sobre a prova. Por isso, o painel "
    "precisa mostrar as duas informações.",
    [["<code>fato_execucao</code>", "1 execução de etapa", "Tempos, retrabalho e custo"],
     ["<code>dim_etapa</code>", "1 etapa (8)", "Coleta, lacre, transporte, guarda, perícia e outras"],
     ["<code>dim_unidade</code>", "1 unidade (6)", "Campo, transporte, laboratórios e custódia"],
     ["<code>dim_status_execucao</code>", "1 status (4)", "Inclui <b>Divergência de lacre</b>"],
     ["<code>dim_calendario</code>", "1 dia (1.096)", "Tempo parado por mês"]],
    "Espera Guarda (h) =\n"
    "    CALCULATE([Tempo Espera (h)], dim_etapa[etapa] = \"Guarda\")\n"
    "\n"
    "Peso Guarda =\n"
    "    DIVIDE([Espera Guarda (h)], [Tempo Espera (h)])\n"
    "\n"
    "Divergencia de Lacre =\n"
    "    DIVIDE(\n"
    "        CALCULATE(\n"
    "            COUNTROWS(fato_execucao),\n"
    "            dim_status_execucao[status_execucao] = \"Divergencia de lacre\"\n"
    "        ),\n"
    "        COUNTROWS(fato_execucao)\n"
    "    )",
    [["Execuções", "10.840", "Contagem da fato"],
     ["% espera", "92,5%", "Quase todo o tempo é fila"],
     ["Guarda", "54,5 h e 35,3%", "Maior espera média e maior participação"],
     ["Baixa", "25,3 h e 16,4%", "Segundo maior bloco de espera"],
     ["Perícia", "5,9 h de execução", "Maior trabalho manual"],
     ["TAT médio por caso", "1.027,5 h", "O maior TAT entre os cinco datasets"],
     ["Retrabalho", "4,7%", "A menor taxa entre os cinco; o problema é tempo, não erro"]],
    "A divergência de lacre é um status, e não uma etapa. Se você filtrar o "
    "painel por etapa, ela desaparece. Por isso, crie a medida própria e "
    "coloque um cartão separado, fora do filtro de etapa.",
    "Guarda",
    "Cenario3_Cadeia_Custodia.xlsx",
    "10.840",
    ["Workbook importado com 8 abas e 10.840 linhas na fato.",
     "Relacionamentos criados e dim_calendario marcada como tabela de datas.",
     "8 medidas base e 3 medidas do cenário, incluindo a divergência de lacre.",
     "4 cartões, barras empilhadas, Pareto, linha do tempo e matriz.",
     "Tabela resumo e 3 segmentações: etapa, unidade e ano.",
     "Números conferem com a tabela de resultado esperado."]
)

receita(
    "receita-4-local-crime",
    "Receita 4: Atendimento de local de crime (12.664 execuções)",
    "Este processo vai do acionamento da equipe ao relatório de atendimento. O "
    "painel precisa separar deslocamento, coleta e liberação, porque o tempo "
    "perdido não está onde o trabalho aparece.",
    "O Deslocamento concentra 35,2% da espera, embora a Coleta tenha o maior "
    "tempo de execução. Por isso, o painel precisa mostrar espera e execução "
    "lado a lado.",
    [["<code>fato_execucao</code>", "1 execução de etapa", "Tempos, retrabalho e custo"],
     ["<code>dim_etapa</code>", "1 etapa (8)", "Acionamento, deslocamento, coleta, lacre e outras"],
     ["<code>dim_unidade</code>", "1 unidade (5)", "ATO, ATV, IML, LAB e plantão"],
     ["<code>dim_sistema</code>", "1 sistema (6)", "Excel e e-mail na operação de campo"],
     ["<code>dim_calendario</code>", "1 dia (1.096)", "Atendimentos por mês"]],
    "Espera Deslocamento (h) =\n"
    "    CALCULATE([Tempo Espera (h)], dim_etapa[etapa] = \"Deslocamento\")\n"
    "\n"
    "Peso Deslocamento =\n"
    "    DIVIDE([Espera Deslocamento (h)], [Tempo Espera (h)])\n"
    "\n"
    "Coleta vs Deslocamento =\n"
    "    DIVIDE(\n"
    "        CALCULATE([Tempo Execucao (h)], dim_etapa[etapa] = \"Coleta\"),\n"
    "        CALCULATE([Tempo Execucao (h)], dim_etapa[etapa] = \"Deslocamento\")\n"
    "    )",
    [["Execuções", "12.664", "Contagem da fato"],
     ["% espera", "86,5%", "O menor percentual entre os cinco, mas ainda é fila"],
     ["Deslocamento", "22,9 h e 35,2%", "Maior espera média e maior participação"],
     ["Liberação", "10,8 h e 16,6%", "Gargalo que aparece depois da coleta"],
     ["Coleta", "3,7 h de execução", "Maior trabalho manual"],
     ["TAT médio por caso", "497,0 h", "Espera mais execução, dividido por 240 casos"],
     ["Retrabalho", "8,4%", "Uniforme entre as etapas, o que indica problema de checklist"]],
    "O Deslocamento tem execução e espera. Quem olha apenas o tempo de "
    "execução conclui que o problema está na coleta. Por isso, o painel "
    "precisa empilhar espera e execução na mesma barra.",
    "Deslocamento",
    "Cenario4_Local_Crime.xlsx",
    "12.664",
    ["Workbook importado com 8 abas e 12.664 linhas na fato.",
     "Relacionamentos criados e dim_calendario marcada como tabela de datas.",
     "8 medidas base e 3 medidas do cenário.",
     "4 cartões, barras empilhadas, Pareto, linha do tempo e matriz.",
     "Tabela resumo e 3 segmentações: etapa, unidade e ano.",
     "Números conferem com a tabela de resultado esperado."]
)

receita(
    "receita-5-laboratorio",
    "Receita 5: Análise laboratorial (13.896 execuções)",
    "Este processo vai do recebimento da amostra ao laudo assinado. O painel "
    "precisa mostrar que a fila está no equipamento, na amplificação e na "
    "eletroforese, e não na interpretação do perfil.",
    "Eletroforese e Amplificação somam 47,1% da espera. A Interpretação tem o "
    "maior trabalho manual. Por isso, o painel precisa separar capacidade de "
    "equipamento de esforço humano.",
    [["<code>fato_execucao</code>", "1 execução de etapa", "Tempos, retrabalho e custo"],
     ["<code>dim_etapa</code>", "1 etapa (8)", "Recebimento, extração, PCR, eletroforese e outras"],
     ["<code>dim_unidade</code>", "1 unidade (5)", "Biologia, Toxicologia, Física, IML e Qualidade"],
     ["<code>dim_tipo_atividade</code>", "1 tipo (6)", "Manual, automatizada, aprovação e outras"],
     ["<code>dim_calendario</code>", "1 dia (1.096)", "Prazo de laudo por mês"]],
    "Espera Equipamento (h) =\n"
    "    CALCULATE(\n"
    "        [Tempo Espera (h)],\n"
    "        dim_etapa[etapa] IN {\"Amplificacao\", \"Eletroforese\"}\n"
    "    )\n"
    "\n"
    "Peso Equipamento =\n"
    "    DIVIDE([Espera Equipamento (h)], [Tempo Espera (h)])\n"
    "\n"
    "Interpretacao vs Equipamento =\n"
    "    DIVIDE(\n"
    "        CALCULATE([Tempo Execucao (h)], dim_etapa[etapa] = \"Interpretacao\"),\n"
    "        CALCULATE([Tempo Execucao (h)], dim_etapa[etapa] IN {\"Amplificacao\", \"Eletroforese\"})\n"
    "    )",
    [["Execuções", "13.896", "Contagem da fato"],
     ["% espera", "88,6%", "Processo dominado por fila"],
     ["Eletroforese", "27,5 h e 24,9%", "Maior espera isolada"],
     ["Amplificação", "24,6 h e 22,2%", "Segunda maior espera"],
     ["Equipamento", "47,1%", "As duas etapas juntas concentram quase metade da espera"],
     ["Interpretação", "3,2 h de execução", "Maior trabalho manual"],
     ["TAT médio por caso", "834,2 h", "Espera mais execução, dividido por 260 casos"],
     ["Retrabalho", "6,8%", "Baixo e uniforme; o problema é capacidade"]],
    "A Interpretação tem o maior tempo de execução, mas a fila está no "
    "equipamento. Se o seu painel destacar a interpretação como gargalo, você "
    "olhou o trabalho em vez do tempo parado.",
    "Amplificação + Eletroforese",
    "Cenario5_Analise_Laboratorial.xlsx",
    "13.896",
    ["Workbook importado com 8 abas e 13.896 linhas na fato.",
     "Relacionamentos criados e dim_calendario marcada como tabela de datas.",
     "8 medidas base e 3 medidas do cenário.",
     "4 cartões, barras empilhadas, Pareto, linha do tempo e matriz.",
     "Tabela resumo e 3 segmentações: etapa, unidade e ano.",
     "Números conferem com a tabela de resultado esperado."]
)

# =================================================================
# PARTE 3 - MANHA: ANALISE DO PROCESSO COM DADOS
# =================================================================
cad.grp("Parte 3 - Manhã: análise do processo com dados",
        "Onde o processo perde tempo e dinheiro, com medição e não com suposição.")

cad.section("espera-vs-execucao", "A diferença que muda a leitura: espera e execução",
    p("Todo processo tem dois tipos de tempo. O primeiro é o tempo em que "
      "alguém trabalha. O segundo é o tempo em que o caso fica parado, "
      "esperando. Na maior parte dos processos, a espera ocupa mais tempo do "
      "que o trabalho.") +
    tbl(["Tipo de tempo", "O que é", "Exemplo"],
        [["<b>Tempo de execução</b> (touch time)", "Minutos em que alguém trabalha", "O perito analisa a amostra"],
         ["<b>Tempo de espera</b> (wait time)", "Tempo em que o caso fica parado na fila", "O exame espera o perito"]],
        num_cols=[]) +
    callout("g", "O achado dos 5 datasets da aula",
        "Nos cinco processos da POLITEC, a espera representa de 86% a 93% do "
        "tempo total. Por isso, o problema não está na velocidade com que as "
        "pessoas trabalham. Está no tempo em que os casos ficam parados na "
        "fila.") +
    wait_vs_touch(92)
)

cad.section("diagrama-espera", "O funil de espera por etapa",
    p("O diagrama que mais revela um processo é o de esperas por etapa. Cada "
      "etapa aparece com o tempo em que o caso ficou parado nela. Dessa forma, "
      "a etapa com a maior barra é o gargalo.") +
    bar_chart(
        ["Fila perito", "Revisão", "Distribuição", "Triagem", "Assinatura", "Análise", "Arquivamento"],
        [57175, 16888, 16360, 13480, 13380, 12860, 7000],
        "Cenário 1: tempo de espera por etapa (horas, soma de todo o período)",
        "A etapa Fila perito concentra 41,5% de toda a espera do processo. "
        "Esse é o gargalo medido no dataset cenario1_processo_pericial.",
        destaque=0
    ) +
    tbl(["Etapa", "Espera (h)", "% da espera", "Leitura"],
        [["<b>Fila perito</b>", "57.175", "<b>41,5%</b>", "<b>GARGALO</b>: o caso fica parado até ser atendido"],
         ["Revisão", "16.888", "12,3%", "Fila do revisor"],
         ["Distribuição", "16.360", "11,9%", "Passagem entre setores"],
         ["Triagem", "13.480", "9,8%", "Fila do ATO"],
         ["Assinatura", "13.380", "9,7%", "Assinatura e liberação"],
         ["Análise", "12.860", "9,3%", "Fila do perito antes de começar"],
         ["Arquivamento", "7.000", "5,1%", "Envio e arquivo"]],
        num_cols=[1, 2]) +
    callout("purple", "Leia o gargalo correto",
        "A etapa Análise tem o maior tempo de execução, que é o trabalho do "
        "perito. A etapa Fila perito tem o maior tempo de espera. Por isso, o "
        "gargalo a atacar é a fila. Mesmo que o perito trabalhe mais rápido, o "
        "caso continua parado enquanto espera.")
)

cad.section("pareto-gargalos", "Pareto dos gargalos: a regra 20/80 do processo",
    p("A análise de Pareto ordena as etapas por tempo e mostra que poucas "
      "etapas concentram a maior parte do desperdício. Esse é o princípio de "
      "Pareto aplicado a processos.") +
    bar_chart(
        ["Fila perito", "Revisão", "Distribuição", "Triagem", "Assinatura"],
        [41.5, 12.3, 11.9, 9.8, 9.7],
        "Pareto da espera: percentual do tempo de espera por etapa",
        "As duas primeiras etapas, Fila perito e Revisão, somam 53,8% de toda "
        "a espera. Atacar essas duas etapas resolve mais da metade do problema.",
        fmt="{:.1f}%",
        destaque=0
    ) +
    tbl(["Conceito", "Aplicação no processo"],
        [["Princípio de Pareto (80/20)", "20% das etapas concentram 80% do tempo"],
         ["Pareto de espera", "Onde o processo mais para"],
         ["Pareto de retrabalho", "Onde mais se erra"],
         ["Pareto de custo", "Onde o dinheiro mais se perde"]],
        num_cols=[]) +
    callout("tip", "Comece pelo topo",
        "Se você puder atacar apenas uma etapa, ataque a primeira do Pareto. "
        "Se puder atacar duas, ataque as duas primeiras. Com isso, o ganho por "
        "unidade de esforço fica maior.")
)

cad.section("retrabalho", "Retrabalho: o desperdício que não aparece",
    p("Retrabalho é refazer uma etapa já feita, por erro ou por devolução. Ele "
      "não aparece no tempo de espera e, por isso, passa despercebido. Neste "
      "caso, um exame que volta da revisão para nova análise refaz todo o "
      "trabalho do perito.") +
    bar_chart(
        ["Pericial", "Orçamento", "Custódia", "Local de crime", "Laboratório"],
        [11.6, 16.6, 4.7, 8.4, 6.8],
        "Taxa média de retrabalho por dataset",
        "O processo orçamentário tem a maior taxa, com 16,6%. Nele, o mapa e o "
        "parecer são refeitos com frequência. Os dados vêm dos cinco datasets "
        "da Aula 6.",
        fmt="{:.1f}%",
        destaque=1
    ) +
    step([
        ("Mapeie o caminho de retorno no diagrama",
         "Toda seta de volta, por correção ou devolução, precisa aparecer no AS-IS."),
        ("Meça o retrabalho nos dados",
         "Use a coluna <code>flag_retrabalho</code> da <code>fato_execucao</code> "
         "e calcule o percentual por etapa."),
        ("Ordene por taxa, e não por volume",
         "Um processo com 5% de retrabalho em 15.000 casos custa mais do que "
         "15% de retrabalho em 200 casos."),
        ("Ataca a causa, e não o sintoma",
         "Retrabalho alto na etapa 3, que é o mapa, indica problema no "
         "checklist ou na planilha, e não no mapeamento em si."),
    ]) +
    tbl(["Retrabalho típico", "Causa raiz", "Intervenção"],
        [["Exame volta da revisão", "Falta de checklist do perito", "Checklist padronizado no TO-BE"],
         ["Mapa comparativo refeito", "Falta de critério de aceitação", "Alerta de dotação e regra clara"],
         ["Pedido devolvido", "Formulário incompleto", "Formulário digital com validação"],
         ["Evidência com divergência", "Lacre em papel", "QR Code digital"]],
        num_cols=[]) +
    callout("err", "Retrabalho invisível no diagrama",
        "Se o AS-IS não mostra o caminho de volta, o tempo real fica "
        "subestimado. Por isso, inclua o fluxo de retorno no diagrama e meça o "
        "retrabalho nos dados.")
)

cad.section("littles-law", "Little's Law: quanto de fila o processo suporta",
    p("Little's Law é a relação entre o número de itens no sistema, a taxa de "
      "chegada e o tempo de permanência. A fórmula é <b><code>L = λ × W</code></b>, "
      "em que L é o número de itens no sistema, λ é a taxa de chegada e W é o "
      "tempo de permanência. Com ela, é possível calcular o tamanho da fila a "
      "partir da demanda e do tempo.") +
    code(
        "L = λ × W\n"
        "\n"
        "λ (chegadas/periodo) = 1.200 requisicoes / ano\n"
        "W (tempo no processo) = 92 dias (o TAT medio)\n"
        "L = (1200/365) × 92 ≈ 302 requisicoes em transito\n"
        "\n"
        "Se W cair para 30 dias:\n"
        "L = (1200/365) × 30 ≈ 99 requisicoes em transito",
        "formula"
    ) +
    tbl(["Se você quer...", "Você precisa..."],
        [["Reduzir a fila (L)", "Reduzir W, que é o tempo, ou λ, que é a chegada"],
         ["Absorver mais demanda", "Aumentar a capacidade, o que eleva W"],
         ["Reduzir o backlog", "Reduzir W ou aumentar a capacidade"]],
        num_cols=[]) +
    callout("purple", "Little's Law no seu TO-BE",
        "Use Little's Law para prever o efeito da automação. Se o TO-BE reduz "
        "a espera da fila de 44 h para 8 h, W cai e L cai na mesma proporção. "
        "Com isso, o investimento fica justificado por número, e não por "
        "opinião.")
)

cad.section("custo-espera", "Custo da espera: quando tempo vira dinheiro",
    p("O custo do processo é a soma do custo de execução, que é o tempo de "
      "trabalho multiplicado pelo custo por hora, com o custo da espera, que "
      "inclui atraso, multa, retrabalho e insatisfação. Nos datasets, a coluna "
      "<code>custo_execucao_rs</code> permite calcular o custo direto da "
      "execução de cada etapa.") +
    tbl(["Componente de custo", "Como aparece no processo da POLITEC"],
        [["Mão de obra", "Horas do perito ou do técnico na execução"],
         ["Atraso (TAT)", "Caso urgente que vence o prazo"],
         ["Retrabalho", "Refazer etapa por erro"],
         ["Perda de validade", "Amostra que se degrada na fila"],
         ["Insatisfação", "Cidadão que demora para receber o laudo"]],
        num_cols=[]) +
    callout("tip", "Transforme espera em reais",
        "Ao apresentar o TO-BE, converta a espera economizada em dinheiro. "
        "Use a conta <b>(espera_antes menos espera_depois) × volume anual × "
        "custo unitário</b>. Esse é o número que sustenta a decisão de "
        "orçamento.")
)

# =================================================================
# PARTE 4 - TARDE: FUNDAMENTOS DE GESTAO DE PROJETOS
# =================================================================
cad.grp("Parte 4 - Tarde: fundamentos de gestão de projetos",
        "O mínimo que um projeto precisa ter: escopo, prazo, custo, qualidade e risco.")

cad.section("o-que-e-projeto", "O que é um projeto e o que não é",
    p("Um projeto é um esforço temporário para criar um produto, serviço ou "
      "resultado único. O triângulo de escopo, prazo, custo e qualidade define "
      "o projeto. Você pode cortar um dos quatro, mas precisa saber qual está "
      "cortando.") +
    tbl(["Projeto tem...", "Operação não tem..."],
        [["Início e fim definidos", "Fim definido, porque é o dia a dia"],
         ["Objetivo único", "Objetivo recorrente"],
         ["Recursos próprios", "Recursos rotineiros"],
         ["Riscos de incerteza", "Riscos de rotina"],
         ["Equipe temporária", "Equipe permanente"]],
        num_cols=[]) +
    aplicab(
        "Quando a POLITEC decide acelerar o fluxo de requisição pericial.",
        "Esse trabalho é um projeto, porque tem início, fim e objetivo de reduzir o TAT. Não é operação, porque a operação seria atender requisições todos os dias.",
        "Implantar uma fila priorizada por prazo legal no SIGT em 90 dias é um projeto. Atender requisições todos os dias é a operação.") +
    callout("err", "A confusão mais comum",
        "Chamar toda mudança de projeto. Se não há início, fim e resultado "
        "único, a atividade é da operação e não deve ser gerenciada com as "
        "ferramentas de projeto.")
)

cad.section("triangulo-projeto", "O triângulo de projeto: o que você pode cortar",
    p("Escopo, prazo, custo e qualidade estão ligados. Quando um deles muda, "
      "os outros reagem. Por isso, o sponsor precisa saber qual restrição será "
      "alterada.") +
    tbl(["Você quer...", "Então aceite que..."],
        [["Reduzir o prazo", "O custo aumenta, o escopo diminui ou o risco cresce"],
         ["Reduzir o custo", "O prazo aumenta ou o escopo diminui"],
         ["Aumentar o escopo", "O prazo aumenta ou o custo cresce"],
         ["Aumentar a qualidade", "O custo aumenta ou o prazo cresce"],
         ["Cortar escopo", "Essa é a primeira alavanca em um projeto com restrição de recurso"]],
        num_cols=[]) +
    antesdepois(
        "O sponsor pede prazo curto, sem aumento de custo e com mais funcionalidades. O projeto aceita a promessa e descobre, no meio do caminho, que vai cortar qualidade.",
        "O projeto responde que consegue prazo e custo se o escopo for priorizado em fases, ou que consegue prazo e escopo se houver aumento de orçamento.",
        errado="Promessa sem análise",
        certo="Trade-off explícito"
    ) +
    callout("tip", "A pergunta para o sponsor",
        "Quando o escopo cresce, pergunte qual restrição será alterada: prazo, "
        "custo ou escopo. Com isso, a conversa deixa de ser emocional e passa a "
        "ser uma decisão de projeto.")
)

cad.section("ciclo-de-vida", "O ciclo de vida de um projeto: os 5 grupos de processos",
    p("Todo projeto passa por cinco grupos de processos, conforme o modelo do "
      "PMBOK. Cada grupo tem perguntas e entregáveis próprios. Por isso, o "
      "ciclo ajuda a evitar dois erros: executar sem medir e nunca encerrar.") +
    tbl(["Grupo", "Quando", "Pergunta-chave", "Entregável típico"],
        [["<b>Iniciar</b>", "Início", "Vale a pena? Quem apoia?", "Termo de abertura e sponsor"],
         ["<b>Planejar</b>", "Início", "Como, quando e com quem?", "Plano, cronograma e escopo"],
         ["<b>Executar</b>", "Meio", "Estamos fazendo o plano?", "Produtos parciais"],
         ["<b>Monitorar</b>", "Contínuo", "Estamos dentro do plano?", "Relatórios e mudanças"],
         ["<b>Encerrar</b>", "Fim", "O que aprendemos?", "Termo de aceite e lições"]],
        num_cols=[]) +
    flow_h([
        ("INI", "Iniciar"),
        ("PLA", "Planejar"),
        ("EXE", "Executar"),
        ("MON", "Monitorar"),
        ("ENC", "Encerrar"),
    ]) +
    step([
        ("Fase 1: iniciar (semanas 1 e 2)",
         "Reúna o problema, identifique o sponsor, defina o objetivo e os "
         "critérios de sucesso. Ao final, escreva um parágrafo com o que vai "
         "mudar e como será medido."),
        ("Fase 2: planejar (semanas 2 a 6)",
         "Mapeie o AS-IS, meça o gargalo, desenhe o TO-BE e estime esforço e "
         "prazo. Ao final, você tem o AS-IS, o TO-BE e o plano de ondas."),
        ("Fase 3: executar (semanas 6 a 26)",
         "Implante uma onda por vez e meça o ganho de cada uma. Ao final, o "
         "processo opera com a primeira onda."),
        ("Fase 4: monitorar (contínuo)",
         "Compare o TAT planejado com o realizado a cada ciclo. Ao final, você "
         "tem o painel de acompanhamento e as decisões de repriorização."),
        ("Fase 5: encerrar (ao fim)",
         "Meça o ganho final, documente o que funcionou e arquive o histórico "
         "do processo para o próximo projeto."),
    ]) +
    aplicab(
        "Quando a direção decide automatizar a cadeia de custódia.",
        "O ciclo de vida evita começar a executar sem medir e evita também nunca encerrar o projeto sem registrar as lições aprendidas.",
        "Na POLITEC, o projeto do QR Code na custódia levou 26 semanas: 6 de mapeamento e medição, 8 de piloto em duas unidades, 12 de implantação e 3 de medição do ganho.") +
    callout("purple", "Monitorar não é só no fim",
        "A maior parte das falhas de projeto vem de descobrir tarde que o "
        "escopo cresceu ou que o prazo atrasou. Por isso, compare o planejado "
        "com o realizado de forma contínua e corrija cedo.")
)

cad.section("stakeholders", "Partes interessadas e a matriz poder e interesse",
    p("Parte interessada é qualquer pessoa ou grupo afetado pelo projeto ou "
      "que possa afetá-lo. Você mapeia quem tem poder, que é a capacidade de "
      "decidir, e interesse, que é o grau de envolvimento. Com isso, define "
      "como comunicar com cada grupo.") +
    tbl(["Quadrante", "Perfil", "Como gerenciar"],
        [["Alto poder e alto interesse", "Parceiro próximo", "Gerencie de perto e mantenha o envolvimento"],
         ["<b>Alto poder e baixo interesse</b>", "Sponsor ou chefe", "<b>Mantenha satisfeito</b>, com relato curto"],
         ["<b>Baixo poder e alto interesse</b>", "Quem executa ou usa", "<b>Mantenha informado</b>, com formação e demonstrações"],
         ["Baixo poder e baixo interesse", "Grupo marginal", "Monitore com atenção mínima"]],
        num_cols=[]) +
    aplicab(
        "Quando você propõe automatizar a etapa de triagem.",
        "O chefe do intermediário, com alto poder e interesse eventual, precisa de um relato curto de impacto. Os triadores, com baixo poder e alto interesse, precisam de treinamento e de participação no desenho.",
        "Na POLITEC, o sponsor é o Diretor Técnico, que acompanha o TAT. A equipe é formada pelos triadores do ATO, que precisam de formação no novo sistema.") +
    callout("err", "Parte interessada esquecida",
        "A parte interessada esquecida com mais frequência é o usuário final, "
        "que vai usar o processo todos os dias. Um processo redesenhado sem a "
        "participação do usuário é rejeitado na operação.")
)

cad.section("gestao-de-risco", "Risco de projeto: identificar, medir e tratar",
    p("Risco é um evento incerto que, se ocorrer, afeta o projeto. O gestor "
      "identifica o risco, avalia a probabilidade e o impacto e define o "
      "tratamento: evitar, reduzir, transferir ou aceitar.") +
    tbl(["Probabilidade e impacto", "Zona", "Ação"],
        [["Alta e alto", "<b>Vermelha (crítica)</b>", "Mitigar agora e preparar plano de contingência"],
         ["Alta e baixo", "Amarela", "Reduzir e monitorar"],
         ["Baixa e alto", "Amarela", "Preparar plano de resposta"],
         ["Baixa e baixo", "Verde", "Aceitar e monitorar"]],
        num_cols=[]) +
    aplicab(
        "Quando o projeto de automação da triagem começa.",
        "Dois riscos dominam a etapa. O primeiro é a ausência de API no SIGT, com alta probabilidade e alto impacto. O segundo é a resistência dos triadores, com probabilidade média e alto impacto.",
        "Na POLITEC, a mitigação do primeiro risco é começar com exportação CSV e integrar depois. A mitigação do segundo é envolver os triadores no desenho e oferecer treinamento.") +
    callout("purple", "Risco não é problema",
        "Risco é algo que pode acontecer. Problema é algo que já aconteceu. Um "
        "risco alto se transforma em problema quando não é tratado.")
)

cad.section("indicadores-projeto", "Como saber se o projeto está saudável",
    p("Um projeto sem indicador é um projeto sem direção. Na gestão pública, "
      "os indicadores de prazo e custo vêm do Earned Value Management. Na "
      "POLITEC, o TAT do processo também funciona como indicador de resultado.") +
    tbl(["Indicador", "Fórmula", "O que informa"],
        [["SPI (Índice de Performance de Prazo)", "Valor ganho dividido pelo valor planejado", "Se o projeto está atrasado"],
         ["CPI (Índice de Performance de Custo)", "Custo real dividido pelo valor ganho", "Se o projeto está gastando mais"],
         ["Atraso médio", "Prazo real menos prazo planejado", "Quanto tempo foi perdido"],
         ["TAT do processo", "Soma de espera e execução", "Quanto tempo o fluxo leva"]],
        num_cols=[]) +
    callout("note", "SPI e CPI juntos",
        "Quando o SPI é menor que 1, o projeto está atrasado. Quando o CPI é "
        "maior que 1, o custo está acima do previsto. Na prática da POLITEC, um "
        "TAT com tendência de alta é o sinal de que o projeto precisa de "
        "atuação.")
)

# =================================================================
# PARTE 5 - TARDE: BPMN E MERMAID
# =================================================================
cad.grp("Parte 5 - Tarde: BPMN e Mermaid",
        "A notação padrão para modelar processos e a ferramenta para desenhar diagramas como código.")

cad.section("por-que-modelar", "Por que modelar um processo antes de mudar",
    p("Modelar um processo não é burocracia. É a forma de ver o processo "
      "inteiro, encontrar o gargalo e comunicar a mudança sem ambiguidade. "
      "Além disso, o desenho funciona como contrato entre as pessoas que vão "
      "mudar o processo.") +
    ul([
        "<b>Evidencia o desperdício</b>: ao desenhar, você vê as etapas que não agregam valor.",
        "<b>Revela gargalos</b>: o ponto de espera fica visível no desenho.",
        "<b>Facilita a conversa</b>: um desenho substitui páginas de texto.",
        "<b>Permite comparar</b>: AS-IS e TO-BE podem ser vistos lado a lado.",
    ]) +
    antesdepois(
        "&quot;O processo do laboratório demora demais, alguém tem que acelerar.&quot; Essa é uma opinião, sem dado e sem solução.",
        "Um desenho com o ponto de espera destacado e o tempo ao lado: &quot;a espera na fila do perito é de 44 h; se ela cair para 8 h, o TAT cai 30%&quot;.",
        errado="Opinião",
        certo="Evidência"
    ) +
    callout("tip", "Regra de ouro",
        "Se o processo não está desenhado, ele não está gerenciado. O AS-IS é "
        "a linha de base contra a qual o TO-BE será medido.")
)

cad.section("o-que-e-bpmn", "O que é BPMN (Business Process Modeling Notation)",
    p("BPMN 2.0 é a notação padrão internacional para modelar processos de "
      "negócio. Ela nasceu na OMG, é lida por ferramentas de automação, como "
      "Camunda, Bizagi e Power Automate, e é usada em todo o mundo. O "
      "diferencial do BPMN é descrever o que acontece e quem faz, com notação "
      "gráfica padronizada.") +
    tbl(["Característica", "BPMN 2.0"],
        [["Padrão", "OMG (Object Management Group), ISO 19510"],
         ["Foco", "Processos de negócio"],
         ["Granularidade", "Fluxo, e não apenas o organograma"],
         ["Elementos", "Eventos, atividades, gateways e swimlanes"],
         ["Uso", "Modelagem e alimentação de ferramentas de automação"]],
        num_cols=[]) +
    callout("purple", "BPMN não é a linguagem do Mermaid",
        "BPMN é a notação, com o conjunto de símbolos e regras. Mermaid é uma "
        "ferramenta, em que você escreve código e ela desenha. Os dois são "
        "complementares: o Mermaid desenha o fluxo, mas não substitui o rigor "
        "do BPMN. Nesta aula, o Mermaid é a forma rápida de materializar o "
        "desenho BPMN.")
)

cad.section("elementos-bpmn", "Os elementos do BPMN: eventos, atividades e gateways",
    p("Todo diagrama BPMN combina três famílias de elementos. Com eles, você "
      "descreve qualquer processo. A galeria abaixo mostra os símbolos na "
      "geometria oficial da OMG. Use-a como referência no seu processo.") +
    gallery() +
    tbl(["Elemento", "Símbolo", "Quando usar"],
        [["Início", "Círculo vazio", "O primeiro passo do processo"],
         ["Fim", "Círculo cheio", "O último passo do processo"],
         ["Tarefa", "Retângulo", "Ação manual ou automática"],
         ["Gateway exclusivo", "Losango com X", "Se A, então X; senão, Y"],
         ["Gateway paralelo", "Losango com +", "Faz X e Y ao mesmo tempo"],
         ["Gateway inclusivo", "Losango com O", "Pode fazer um, outro ou os dois"],
         ["Mensagem", "Seta tracejada", "Um ator passa algo para outro"],
         ["Timer", "Relógio", "Acontece em data programada"],
         ["Fila (pool)", "Retângulo", "Um sistema ou unidade separada"],
         ["Objeto de dados", "Retângulo com canto", "Documento que entra ou sai"]],
        num_cols=[]) +
    callout("purple", "Leia o código do desenho",
        "Os símbolos seguem a geometria padronizada. A notação importa: quando "
        "duas pessoas leem o mesmo diagrama, elas veem as mesmas coisas. É "
        "isso que permite automatizar o processo depois.")
)

cad.section("gateways-detalhe", "Gateways: as três portas de decisão",
    p("O gateway, representado pelo losango, é o ponto em que o processo "
      "decide. Escolher o gateway correto evita que o diagrama minta sobre o "
      "processo.") +
    gates_anatomy() +
    grid2([
        ("\u2715 Gateway exclusivo (X)",
         "<b>Exatamente uma</b> das rotas é escolhida. É o mais comum. "
         "Exemplo: <i>&quot;O material biológico está íntegro? Se sim, segue "
         "para a análise; se não, segue para a guarda.&quot;</i>"),
        ("\u2715 Gateway paralelo (+)",
         "<b>Todas</b> as rotas saem juntas. Use para dividir trabalho em "
         "paralelo. Exemplo: <i>&quot;envia ao laboratório e notifica o "
         "delegado ao mesmo tempo&quot;.</i>"),
        ("\u25ef Gateway inclusivo (O)",
         "<b>Uma, várias ou nenhuma</b> rota pode ser escolhida, conforme uma "
         "condição mais complexa. É o mais flexível e o mais difícil de ler."),
    ]) +
    callout("err", "Gateway mal usado",
        "Usar um gateway paralelo quando apenas um caminho ocorre cria um "
        "paralelismo que não existe no processo real. Com isso, o TO-BE parece "
        "melhor do que é. Se apenas uma rota ocorre, use o exclusivo.")
)

cad.section("swimlanes", "Pools e swimlanes: quem faz o quê",
    p("As swimlanes separam o processo por ator, que pode ser uma unidade, um "
      "cargo ou um sistema. O fluxo cruza as faixas e deixa visível onde o "
      "processo muda de mãos. Esse ponto costuma ser onde está o gargalo.") +
    tbl(["Elemento", "O que representa", "Exemplo na POLITEC"],
        [["<b>Pool</b>", "Um sistema ou organização separada", "SIGT e papel"],
         ["<b>Lane</b>", "Um papel dentro do pool", "Triador, perito, chefe e sistema"]],
        num_cols=[]) +
    swimlane_anatomy() +
    step([
        ("Liste os atores do processo",
         "Quem executa alguma coisa? No fluxo pericial: <b>Delegacia</b>, "
         "<b>ATO</b>, <b>Laboratório</b> e <b>Sistema</b>."),
        ("Crie uma swimlane por ator",
         "Uma faixa horizontal por ator, na ordem em que o caso passa."),
        ("Coloque cada atividade na faixa de quem a executa",
         "A triagem vai na faixa do ATO, e a análise vai na faixa do laboratório."),
        ("Marque as fronteiras",
         "Onde o fluxo atravessa duas faixas, existe uma espera potencial. "
         "Sinalize esse ponto com um comentário ou uma cor."),
    ]) +
    aplicab(
        "Quando você quer prever onde o processo vai travar.",
        "Cada transição entre swimlanes é um ponto de espera potencial, porque uma mão passa o objeto para outra.",
        "No fluxo da requisição pericial, o caso cruza quatro swimlanes: Delegacia, ATO, Laboratório e Sistema. Medindo a espera em cada fronteira, a Fila perito aparece com 41,5% do tempo.") +
    callout("purple", "Onde nasce o gargalo",
        "Cada transição entre swimlanes é um ponto de espera potencial. O "
        "gargalo quase sempre está nessas fronteiras. Por isso, medir a espera "
        "por etapa, e não apenas a execução, muda o diagnóstico.")
)

cad.section("eventos-bpmn", "Eventos: o que dispara, espera ou detecta",
    p("Eventos BPMN são os gatilhos e as respostas do processo. Eles dão "
      "profundidade ao desenho e são necessários para a automação.") +
    ul([
        "<b>Evento de início</b>: o que dispara o processo, como mensagem, timer, erro ou sinal.",
        "<b>Evento intermediário</b>: o que acontece no meio e exige reação, como o vencimento do prazo legal.",
        "<b>Evento de fim</b>: como o processo termina, de forma normal, com erro ou com cancelamento.",
        "<b>Evento de fronteira</b>: fica anexo a uma atividade e reage a um erro ou a um prazo.",
    ]) +
    callout("tip", "O evento de fronteira e a automação",
        "&quot;Se o prazo vencer, dispara alerta&quot; é um evento de fronteira "
        "com timer. É assim que se constrói um alarme automático no TO-BE.")
)

cad.section("mermaid-intro", "Mermaid: diagramas como código",
    p("Mermaid é uma linguagem de texto para diagramas. Você escreve o "
      "diagrama em texto, dentro de um bloco de Markdown, deste caderno, de "
      "uma IDE ou de uma wiki, e o Mermaid renderiza o desenho. Como o "
      "diagrama é texto, ele entra no Git, é versionado, revisado e "
      "reaparece sozinho.") +
    tbl(["Vantagem", "Explicação"],
        [["Versionável", "O diagrama fica no Git e pode ser comparado ou revertido"],
         ["Colaborativo", "Duas pessoas editam o mesmo texto do diagrama"],
         ["Barato de mudar", "Mover uma etapa exige editar uma linha de texto"],
         ["Renderiza em qualquer lugar", "GitHub, GitLab, VS Code, Notion e este caderno"]],
        num_cols=[]) +
    step([
        ("Escreva o diagrama como texto",
         "Comece com <code>flowchart TD</code> e uma seta: <code>A[Req.] --&gt; B[Triagem]</code>."),
        ("Renderize no navegador",
         "Cole em <b>mermaid.live</b>, que é gratuito e não exige instalação, e "
         "veja o desenho aparecer."),
        ("Itere e limpe",
         "Adicione etapas, gateways e swimlanes. O texto cresce e o desenho "
         "acompanha."),
        ("Versione no repositório",
         "Salve como <code>processo.mmd</code> no Git. Com isso, o diagrama "
         "passa a ter histórico."),
    ]) +
    callout("note", "BPMN formal e Mermaid rápido",
        "Mermaid é adequado para rascunho, documentação e diagramas que vivem "
        "junto do código. Para um projeto formal com ferramenta de BPMN, use "
        "uma ferramenta dedicada. Nesta aula, o Mermaid é o apoio para "
        "desenhar o BPMN com velocidade.")
)

cad.section("mermaid-flowchart", "Mermaid 1: flowchart, o diagrama de fluxo",
    p("O <code>flowchart</code> é o tipo mais usado e o mais próximo do BPMN. "
      "Com ele, você desenha o fluxo completo de um processo.") +
    code(
        "flowchart TD\n"
        "    A([Inicio: requisicao recebida]) --> B[Triagem]\n"
        "    B --> C{Exame urgente?}\n"
        "    C -->|Sim| D[Fila prioritaria]\n"
        "    C -->|Nao| E[Fila normal]\n"
        "    D --> F[Analise do exame]\n"
        "    E --> F\n"
        "    F --> G([Fim: laudo emitido])",
        "mermaid"
    ) +
    tbl(["Elemento", "Sintaxe", "Significado no BPMN"],
        [["Nós", "`A[Retangulo]`", "Atividade (tarefa)"],
         ["Nós com borda dupla", "`A[[Subprocesso]]`", "Subprocesso"],
         ["Retângulo arredondado", "`A([Inicio])`", "Evento de início ou fim"],
         ["Losango", "`C{Decisao?}`", "Gateway"],
         ["Seta simples", "`A --> B`", "Fluxo"],
         ["Seta rotulada", "`A -->|Sim| B`", "Fluxo com condição"],
         ["Caixa dupla", "`A[[Sub]]`", "Subprocesso"]],
        num_cols=[]) +
    callout("tip", "Direção do fluxo",
        "<code>TD</code> significa top-down, na vertical, que é o padrão do "
        "BPMN. <code>LR</code> significa left-right, na horizontal, e é melhor "
        "para processos longos. Comece com <code>TD</code> e mude para "
        "<code>LR</code> se o diagrama ficar comprido demais.")
)

cad.section("mermaid-subgraphs", "Mermaid 2: subgraph, as swimlanes",
    p("O <code>subgraph</code> do Mermaid reproduz as swimlanes do BPMN. Cada "
      "bloco é um ator, que pode ser uma unidade, um papel ou um sistema, e o "
      "fluxo cruza os blocos.") +
    code(
        "flowchart LR\n"
        "    subgraph DELEG[\"Delegacia\"]\n"
        "        A([Req. recebida]) --> B[Registrar no SIGT]\n"
        "    end\n"
        "    subgraph ATO[\"ATO - Gabinete\"]\n"
        "        C[Triagem] --> D{Dados completos?}\n"
        "    end\n"
        "    subgraph LAB[\"Laboratorio\"]\n"
        "        E[Fila do perito] --> F[Analise]\n"
        "        F --> G[Revisao]\n"
        "    end\n"
        "    B --> C\n"
        "    D -->|Sim| E\n"
        "    D -->|Nao| C\n"
        "    G --> H([Laudo])",
        "mermaid"
    ) +
    callout("purple", "A regra do subgraph",
        "Um processo só está bem modelado quando cada atividade está dentro de "
        "uma swimlane. Se uma tarefa está na swimlane errada, o diagrama está "
        "errado. Essa é a mesma disciplina do BPMN formal.")
)

cad.section("mermaid-sequence", "Mermaid 3: sequenceDiagram, quem fala com quem",
    p("O <code>sequenceDiagram</code> mostra o fluxo no tempo, com os atores "
      "trocando mensagens. Ele é adequado para processos com integração entre "
      "sistemas ou com comunicação com terceiros.") +
    code(
        "sequenceDiagram\n"
        "    participant D as Delegacia\n"
        "    participant S as SIGT\n"
        "    participant P as Perito\n"
        "    participant L as Laboratorio\n"
        "    D->>S: Registra requisicao\n"
        "    S-->>D: Protocolo + fila\n"
        "    S->>P: Notifica novo exame\n"
        "    P->>L: Recolhe amostra\n"
        "    L-->>P: Resultado\n"
        "    P->>S: Anexa laudo\n"
        "    S-->>D: Laudo disponivel",
        "mermaid"
    ) +
    tbl(["Seta", "Significado"],
        [["`->>`", "Mensagem síncrona (chamada)"],
         ["`-->>`", "Retorno (resposta)"],
         ["`-) `", "Mensagem assíncrona (sem espera)"],
         ["`->>`", "Fluxo de dados ou evento"]],
        num_cols=[]) +
    callout("tip", "flowchart e sequenceDiagram",
        "O <b>flowchart</b> mostra os passos, ou seja, o que acontece. O "
        "<b>sequenceDiagram</b> mostra as mensagens, ou seja, quem fala com "
        "quem e quando. Para automação e integração entre sistemas, o "
        "sequenceDiagram é mais útil.")
)

cad.section("mermaid-state", "Mermaid 4: stateDiagram, o ciclo de vida",
    p("O <code>stateDiagram-v2</code> mostra os estados que um objeto, como "
      "uma requisição, uma evidência ou um projeto, assume ao longo do tempo. "
      "É a visão natural para quem já estudou o ciclo de vida no Dia 1.") +
    code(
        "stateDiagram-v2\n"
        "    [*] --> AguardandoTriagem\n"
        "    AguardandoTriagem --> EmAnalise: triagem aprovada\n"
        "    AguardandoTriagem --> Cancelado: dados incompletos\n"
        "    EmAnalise --> AguardandoRevisao: exame concluido\n"
        "    AguardandoRevisao --> EmAnalise: revisao reprovou\n"
        "    AguardandoRevisao --> LaudoEmitido: aprovado\n"
        "    LaudoEmitido --> [*]",
        "mermaid"
    ) +
    callout("note", "Estado e etapa",
        "Um estado é uma condição duradoura, como a requisição que está em "
        "análise. Uma etapa é um passo, como o perito que recolheu a amostra. "
        "O stateDiagram foca no estado, e o flowchart foca na etapa. Nos dois, "
        "o gargalo é o estado em que o objeto fica parado por mais tempo.")
)

cad.section("mermaid-outros", "Mermaid 5: gantt, journey, mindmap e C4",
    p("O Mermaid tem outros tipos úteis para a gestão de projeto. Cada um "
      "responde a uma pergunta diferente, e todos podem ser versionados como "
      "texto.") +
    code(
        "gantt\n"
        "    title Projeto - automacao da triagem\n"
        "    dateFormat YYYY-MM-DD\n"
        "    section Planejamento\n"
        "    Mapeamento AS-IS   :a1, 2026-01-10, 20d\n"
        "    Desenho do TO-BE    :a2, after a1, 10d\n"
        "    section Execucao\n"
        "    Prototipo (MVP)     :b1, 2026-02-10, 25d\n"
        "    Validacao com uso   :b2, after b1, 15d",
        "mermaid"
    ) +
    tbl(["Tipo", "Para que serve", "Exemplo na POLITEC"],
        [["<code>gantt</code>", "Cronograma do projeto", "Prazo das fases de uma automação"],
         ["<code>journey</code>", "Experiência do usuário", "Como a delegacia vivencia o processo"],
         ["<code>mindmap</code>", "Decomposição do escopo", "Árvore do escopo (WBS)"],
         ["<code>C4</code>", "Arquitetura de software", "Como o app conversa com o SIGT"],
         ["<code>erDiagram</code>", "Modelo de dados", "Entidades do processo, como requisição e exame"]],
        num_cols=[]) +
    callout("purple", "O diagrama de viagem (journey)",
        "O <code>journey</code> mapeia a experiência do cidadão ou do servidor "
        "ao longo do processo. Ele revela o momento de espera na perspectiva de "
        "quem passa pelo processo. Esse é o argumento para a automação.")
)

# =================================================================
# PARTE 6 - TARDE: DO TEXTO AO DIAGRAMA
# =================================================================
cad.grp("Parte 6 - Tarde: do texto ao diagrama",
        "O método que converte uma descrição em linguagem natural em um diagrama BPMN.")

cad.section("por-que-automatizar-o-desenho", "Por que não desenhar à mão",
    p("Desenhar um diagrama de processo à mão é lento, difícil de manter e "
      "difícil de versionar. O desenho como texto, com Mermaid, muda essa "
      "situação. Você escreve o processo em minutos, versiona no Git e "
      "qualquer pessoa com o texto consegue gerar o diagrama.") +
    grid2([
        ("\u2717 Desenho manual (Visio ou Lucidchart)",
         ul(["Lento para montar e para mudar",
             "Várias pessoas não editam o mesmo arquivo",
             "Sem histórico de mudanças",
             "O arquivo se perde em PDF ou PNG"])),
        ("\u2713 Diagrama como texto (Mermaid)",
         ul(["Minutos para escrever e segundos para gerar",
             "Editável por qualquer pessoa com o texto",
             "Versionado no Git, com diff legível",
             "Renderiza no GitHub, na wiki, na IDE e neste caderno"]))
    ]) +
    callout("tip", "O desenho deixa de ser documento e passa a ser código",
        "Um diagrama Mermaid é um arquivo de texto. Ele entra no mesmo controle "
        "de versão do código. Assim, quem mudou o processo mudou o diagrama, e "
        "o histórico mostra a mudança.")
)

cad.section("metodo-7-perguntas", "O método das 7 perguntas: de texto para diagrama",
    p("Para transformar uma descrição em diagrama, faça sete perguntas, sempre "
      "na mesma ordem. A ordem importa, porque cada pergunta depende da "
      "anterior.") +
    tbl(["#", "Pergunta", "Vira no diagrama..."],
        [["<b>1</b>", "<b>Quem ou o que dispara?</b> O que inicia o processo?", "Evento de início"],
         ["<b>2</b>", "<b>Onde começa?</b> Qual é a primeira atividade?", "Primeira tarefa"],
         ["<b>3</b>", "<b>O que acontece em seguida?</b> Repita a pergunta.", "Cadeia de tarefas"],
         ["<b>4</b>", "<b>Há decisão?</b> Existe condição do tipo se e senão?", "Gateway"],
         ["<b>5</b>", "<b>Quem faz cada etapa?</b> Qual é a unidade ou o papel?", "Swimlanes"],
         ["<b>6</b>", "<b>O que entra e sai?</b> Quais documentos circulam?", "Objetos de dados e mensagens"],
         ["<b>7</b>", "<b>Como termina?</b> Com sucesso, erro ou cancelamento?", "Eventos de fim"]],
        num_cols=[]) +
    callout("g", "Por que a ordem importa",
        "A pergunta 5, que trata de quem faz, só faz sentido depois de saber "
        "quais atividades existem, o que é respondido nas perguntas 2 a 4. A "
        "pergunta 7, que trata do fim, só faz sentido depois de mapear o "
        "caminho. Pular direto para o desenho leva a diagramas com tarefa na "
        "swimlane errada ou sem fim.")
)

cad.section("exemplo-pratico", "Exemplo prático: do texto ao diagrama",
    p("Um perito descreve o fluxo, e a descrição vira o diagrama abaixo. O "
      "roteiro são as sete perguntas, aplicadas na ordem.") +
    code(
        "flowchart TD\n"
        "    subgraph DELEG[\"Delegacia\"]\n"
        "        A([1. Requisicao recebida]) --> B[2. Registrar no SIGT]\n"
        "    end\n"
        "    subgraph ATO[\"ATO - Gabinete\"]\n"
        "        C[3. Triagem] --> D{4. Dados completos?}\n"
        "    end\n"
        "    subgraph LAB[\"Laboratorio\"]\n"
        "        E[5. Fila do perito] --> F[6. Analise do exame]\n"
        "        F --> G{7. Passe a revisao?}\n"
        "        G -->|Sim| H[8. Revisao tecnica]\n"
        "        G -->|Nao| I[Corrigir e refazer]\n"
        "        I --> F\n"
        "        H --> J([9. Laudo emitido])\n"
        "    end",
        "mermaid"
    ) +
    tbl(["Pergunta", "Resposta", "Onde está no diagrama"],
        [["1. Quem dispara?", "A delegacia recebe a requisição", "Evento de início A"],
         ["2. Onde começa?", "Registrar no SIGT", "Tarefa B"],
         ["3. O que acontece depois?", "Triagem, fila e análise", "C, E e F"],
         ["4. Há decisão?", "Dados completos e passa à revisão", "Gateways D e G"],
         ["5. Quem faz?", "Delegacia, ATO e Laboratório", "Três swimlanes"],
         ["6. O que entra e sai?", "Protocolo e laudo", "Nós de borda"],
         ["7. Como termina?", "Laudo emitido", "Evento de fim J"]],
        num_cols=[])
)

cad.section("heuristicas-diagrama", "Heurísticas: como fazer um diagrama legível",
    p("Um diagrama bom se lê em segundos. As heurísticas abaixo seguem a boa "
      "prática de BPMN e melhoram a leitura do processo.") +
    ul([
        "<b>Fluxo de cima para baixo</b>, exceto em processos longos, que podem usar a horizontal.",
        "<b>Uma swimlane por ator</b>, sem atividades fora de uma faixa.",
        "<b>Poucos elementos por página</b>. Se não couber, quebre em subprocessos.",
        "<b>Rotule as setas com a condição</b>, como Sim e Não.",
        "<b>Evite linhas cruzadas</b>. Se elas se cruzam, reveja o layout ou quebre o diagrama.",
        "<b>Nomeie as atividades com verbo</b>, como Registrar, e não Registro.",
        "<b>Destaque o gargalo</b> com cor ou nota, conforme a Parte 3.",
    ]) +
    callout("err", "O diagrama emaranhado",
        "Um diagrama com 40 caixas e 60 setas cruzadas não comunica. Se o "
        "processo não cabe, ele tem subprocessos. Quebre em caixas duplas e "
        "detalhe cada uma.")
)

cad.section("versionar-processo", "Versionar o processo: o diagrama como histórico",
    p("Como o diagrama é texto, ele entra no Git como qualquer código. Isso "
      "cria um histórico do processo. Assim, é possível ver quando e como o "
      "fluxo mudou e voltar atrás se a mudança não funcionou.") +
    ul([
        "<code>processos/requisicao-pericial.mmd</code>: o diagrama AS-IS versionado.",
        "<code>processos/requisicao-pericial-tobe.mmd</code>: a versão proposta.",
        "Os commits descrevem as mudanças, como &quot;prioriza fila por prazo legal&quot;.",
        "A revisão do código aprova a mudança do processo, como ocorre com o código.",
    ]) +
    callout("purple", "É possível medir o processo no tempo",
        "Se o AS-IS está versionado, você tem a linha de base. A cada "
        "trimestre, redesenhe o processo real e compare com o TO-BE planejado. "
        "Assim, o processo real e o planejado ficam documentados com prova.")
)

# =================================================================
# PARTE 7 - TARDE: TO-BE E INTERVENCAO DIGITAL
# =================================================================
cad.grp("Parte 7 - Tarde: TO-BE e intervenção digital",
        "Redesenhe o processo sobre o gargalo medido e trate o gargalo com automação.")

cad.section("o-que-e-tobe", "TO-BE: o processo futuro sem utopia",
    p("O TO-BE é o desenho do processo depois da intervenção. O erro comum é "
      "criar um TO-BE utópico, com fila zero, espera zero e tudo automático. "
      "Esse desenho não convence e não se implanta.") +
    antesdepois(
        "TO-BE utópico: &quot;um app resolve tudo, fila zero e laudo em 2 horas&quot;, sem dado, sem viabilidade e sem plano.",
        "TO-BE viável: &quot;reduzir a espera da fila de 44 h para 8 h com fila priorizada por prazo e painel de carga; meta de 82% de redução, validada nos dados&quot;.",
        errado="Utopia",
        certo="Viável"
    ) +
    callout("g", "A regra do TO-BE",
        "Cada mudança no TO-BE precisa estar ligada a um gargalo medido. Se "
        "você redesenha algo que não era gargalo, gasta esforço sem retorno. "
        "Além disso, se não consegue medir o ganho, provavelmente escolheu a "
        "mudança errada.")
)

cad.section("principios-tobe", "Os 5 princípios de redesenho do processo",
    p("Reorganizar um processo não é apenas automatizar. Os cinco princípios "
      "abaixo orientam o redesenho, nesta ordem de impacto.") +
    tbl(["#", "Princípio", "O que faz", "Exemplo no processo pericial"],
        [["1", "<b>Eliminar</b>", "Remover etapa que não agrega valor", "Eliminar a dupla conferência manual"],
         ["2", "<b>Simplificar</b>", "Reduzir passos, formulários e passagens", "Um formulário em vez de três"],
         ["3", "<b>Integrar</b>", "Unir etapas separadas por sistemas", "SIGT integrado ao laboratório"],
         ["4", "<b>Automatizar</b>", "Máquina faz o que o humano faz", "Fila priorizada por prazo"],
         ["5", "<b>Padronizar</b>", "Uniformizar para facilitar", "Checklist igual em todas as delegacias"]],
        num_cols=[]) +
    callout("err", "Automatizar primeiro",
        "Automatizar um processo ruim cria um processo ruim e mais rápido. Você "
        "gasta para acelerar algo que deveria ter sido eliminado ou "
        "simplificado antes.")
)

cad.section("tobe-fila-priorizada", "Exemplo de TO-BE: a fila priorizada",
    p("O gargalo medido do Cenário 1 é a fila do perito, com 44 h de espera "
      "média e 41,5% de toda a espera. A intervenção atua nesse ponto, com uma "
      "fila priorizada por prazo legal.") +
    code(
        "flowchart TD\n"
        "    subgraph DELEG[\"Delegacia\"]\n"
        "        A([Req. recebida]) --> B[Registrar no SIGT com prazo legal]\n"
        "    end\n"
        "    subgraph ATO[\"ATO - Gabinete\"]\n"
        "        C[Triagem automatica por tipo] --> D{Dados completos?}\n"
        "    end\n"
        "    subgraph LAB[\"Laboratorio\"]\n"
        "        E[Fila priorizada por prazo] --> F[Analise do exame]\n"
        "        F --> G{Revisao?}\n"
        "        G -->|Sim| H[Revisao]\n"
        "        G -->|Nao| I[Corrigir]\n"
        "        I --> F\n"
        "        H --> J([Laudo])\n"
        "        subgraph PANEL[\"Painel de carga\"]\n"
        "            P[WIP por perito em tempo real]\n"
        "        end\n"
        "        P -.-> E\n"
        "    end\n"
        "    B --> C\n"
        "    D -->|Sim| E\n"
        "    D -->|Nao| C",
        "mermaid"
    ) +
    tbl(["Mudança no TO-BE", "Foco", "Efeito esperado"],
        [["Fila por ordem de chegada", "AS-IS", "Urgente espera junto com a rotina"],
         ["<b>Fila por prazo legal</b>", "<b>TO-BE</b>", "<b>Urgente atendido primeiro</b>"],
         ["Triagem automática por tipo", "TO-BE", "Menos espera na triagem"],
         ["Painel de carga em tempo real", "TO-BE", "Redistribui antes de acumular"],
         ["Sem dupla digitação", "TO-BE", "Menos retrabalho"]],
        num_cols=[])
)

cad.section("intervencao-digital", "Intervenção digital: o catálogo de ferramentas",
    p("A intervenção no processo pode usar diferentes recursos digitais. As "
      "ferramentas da Microsoft, apresentadas desde o Dia 4, resolvem a maior "
      "parte dos casos.") +
    grid2([
        ("\U0001f504 Automatizar a regra",
         "<b>Power Automate</b>: se o prazo vencer, dispara alerta; se o "
         "processo estiver completo, avança a etapa; se for urgente, sobe na fila."),
        ("\U0001f4f1 Digitalizar o registro",
         "<b>Power Apps ou formulário</b>: substitui o papel por registro "
         "digital, com validação e carimbo de tempo."),
        ("\U0001f517 Integrar sistemas",
         "<b>Conector ou API</b>: liga o SIGT ao laboratório sem redigitação e "
         "reduz o retrabalho."),
        ("\U0001f4ca Visualizar para decidir",
         "<b>Power BI</b>: painel de carga e WIP para decidir a redistribuição."),
        ("\U0001f9ea Automatizar o cálculo",
         "<b>Script ou fórmula</b>: cálculo automático de SLA e de prioridade "
         "por prazo."),
        ("\U0001f4e1 Notificar",
         "<b>E-mail ou Teams</b>: alerta enviado ao responsável, em vez de "
         "esperar que alguém perceba.")
    ]) +
    step([
        ("1. Liste as intervenções possíveis",
         "Para cada etapa do TO-BE, verifique se é possível eliminar, "
         "automatizar, integrar ou visualizar."),
        ("2. Priorize pelo impacto no gargalo",
         "A intervenção que mais altera o gargalo vem primeiro. Automatizar "
         "uma etapa que não é gargalo é desperdício."),
        ("3. Escolha a ferramenta",
         "Regra de uma condição vai para o Power Automate. Formulário vai para "
         "o Power Apps. Indicador vai para o Power BI. Regra complexa vai para "
         "script."),
        ("4. Defina o medidor de sucesso",
         "Qual número do AS-IS vai mudar? Por exemplo, a espera da fila de 44 h "
         "para 8 h. Sem medidor, não há como provar o ganho."),
    ]) +
    tbl(["Intervenção", "Custo", "Prazo", "Risco"],
        [["Alerta automático", "Baixo", "1 a 2 semanas", "Baixo"],
         ["Painel de carga em BI", "Baixo", "2 a 4 semanas", "Baixo"],
         ["Formulário digital", "Médio", "4 a 8 semanas", "Médio, por causa da adoção"],
         ["Fila priorizada por regra", "Médio", "4 a 6 semanas", "Médio"],
         ["Integração entre sistemas", "Alto", "3 a 6 meses", "Alto, por causa da dependência"],
         ["Aplicativo com QR Code", "Alto", "3 a 6 meses", "Alto, por causa do campo"]],
        num_cols=[]) +
    callout("tip", "Comece pelo alerta",
        "A primeira automação de um processo quase sempre é um alerta, como "
        "notificar quando o prazo vencer. Ela custa pouco, produz efeito "
        "imediato e prepara o terreno para automações maiores.") +
    automation_anatomy()
)

cad.section("script-automacao", "Automatizar com script: um exemplo real",
    p("Nem toda automação exige Power Automate. Para uma regra de uma "
      "condição, um script em Python, Excel ou planilha resolve. O exemplo "
      "abaixo prioriza a fila por prazo legal.") +
    code(
        "# Prioriza a fila de exames por prazo legal restante\n"
        "import csv, datetime as dt\n"
        "\n"
        "hoje = dt.date(2026, 6, 10)\n"
        "fila = []\n"
        "\n"
        "with open('requisicoes.csv', encoding='utf-8-sig') as f:\n"
        "    for linha in csv.DictReader(f, delimiter=';'):\n"
        "        prazo = dt.date.fromisoformat(linha['prazo_legal'])\n"
        "        dias = (prazo - hoje).days\n"
        "        fila.append((dias, linha['id'], linha['exame']))\n"
        "\n"
        "# menor prazo primeiro = maior urgencia\n"
        "fila.sort()\n"
        "\n"
        "print('Fila priorizada (prazo, id, exame):')\n"
        "for dias, id_, exame in fila[:10]:\n"
        "    print(f'  {dias:>4}d  {id_:12s} {exame}')",
        "python"
    ) +
    callout("note", "Regra antes do código",
        "Antes de automatizar, escreva a regra em linguagem clara. No exemplo, "
        "a regra é que o exame com menor prazo legal vai primeiro. Se você não "
        "consegue escrever a regra, não consegue automatizar. O código é apenas "
        "a tradução da regra.")
)

cad.section("calcular-o-ganho", "O cálculo do ganho: como provar que valeu",
    p("Todo TO-BE precisa de uma conta que mostre o retorno. O ganho é medido "
      "pela comparação entre o AS-IS e o TO-BE projetado, usando os mesmos "
      "dados.") +
    tbl(["Ganho", "Fórmula", "Exemplo no Cenário 1"],
        [["Espera reduzida", "espera_ASIS menos espera_TOBE", "44 h &rarr; 8 h"],
         ["TAT reduzido", "TAT_ASIS menos TAT_TOBE", "92 d &rarr; 70 d, com redução de 24%"],
         ["Custo poupado", "minutos_poupados vezes custo por minuto", "R$ X por ano"],
         ["Capacidade liberada", "casos atendidos a mais no mesmo tempo", "+N exames por ano"]],
        num_cols=[]) +
    callout("g", "A conta do ganho no Cenário 1",
        "A fila do perito cai de 44 h para 8 h, o que representa 36 h por caso. "
        "Com 1.200 casos por ano, são cerca de 43.200 h por ano de espera "
        "poupadas. A R$ 78,40 por hora de produção útil, isso equivale a um "
        "perito-equivalente liberado para trabalho técnico, sem contratar "
        "ninguém.")
)

cad.section("roadmap-tobe", "Como levar o TO-BE à prática: roadmap de implantação",
    p("Um TO-BE não é implantado de uma vez. Use um roadmap em ondas e meça o "
      "ganho de cada uma. Assim, o risco fica distribuído e o aprendizado de "
      "uma onda serve para a seguinte.") +
    tbl(["Onda", "Intervenção", "Ganho esperado", "Esforço"],
        [["<b>Onda 1 (0 a 3 meses)</b>", "Alertas de prazo e painel de carga em BI", "Visibilidade e 10% de redução na espera", "Baixo"],
         ["<b>Onda 2 (3 a 6 meses)</b>", "Fila priorizada por prazo legal", "30% de redução na espera da fila", "Médio"],
         ["<b>Onda 3 (6 a 12 meses)</b>", "Triagem automática e integração com o SIGT", "20% de redução na espera e menos retrabalho", "Alto"],
         ["<b>Onda 4 (12 meses ou mais)</b>", "Integração ponta a ponta", "Redesenho completo", "Alto"]],
        num_cols=[]) +
    callout("purple", "A Onda 1 custa menos e produz efeito rápido",
        "Comece pelo alerta e pelo painel de carga. Essas intervenções custam "
        "pouco, são implantadas em pouco tempo e mostram o problema em tempo "
        "real. Com isso, preparam o argumento para as ondas seguintes.")
)

# =================================================================
# PARTE 8 - PRATICA GUIADA (8 LABS: 4 MANHA + 4 TARDE)
# =================================================================
cad.grp("Parte 8 - Prática guiada",
        "Oito labs: quatro de painel pela manhã e quatro de processo e mini app pela tarde.")

cad.section("labs-intro", "Os 8 labs desta aula",
    p("Cada lab entrega uma parte do resultado final. Os quatro primeiros "
      "acontecem na manhã, em torno do painel. Os quatro últimos acontecem na "
      "tarde, em torno do processo e da ideia do mini app.") +
    tbl(["Turno", "Lab", "O que você faz", "Ferramenta", "Tempo"],
        [["Manhã", "<b>1</b>", "Conectar o workbook e montar o modelo estrela", "Power BI e Power Query", "30 min"],
         ["Manhã", "<b>2</b>", "Criar as 8 medidas DAX", "Power BI", "30 min"],
         ["Manhã", "<b>3</b>", "Montar os 5 visuais do painel", "Power BI", "40 min"],
         ["Manhã", "<b>4</b>", "Ler o painel e escrever a hipótese de gargalo", "Painel e caderno", "20 min"],
         ["Tarde", "<b>5</b>", "Descrever o processo em texto, com as 7 perguntas", "Papel e caneta", "30 min"],
         ["Tarde", "<b>6</b>", "Converter o texto em diagrama AS-IS", "Mermaid", "40 min"],
         ["Tarde", "<b>7</b>", "Desenhar o TO-BE e calcular o ganho", "Mermaid e planilha", "50 min"],
         ["Tarde", "<b>8</b>", "Fazer o pitch de 3 minutos e o canvas do mini app", "Apresentação", "30 min"]],
        num_cols=[]) +
    callout("tip", "Qual processo usar",
        "Escolha um processo em que você trabalha ou conhece. Os cinco datasets "
        "servem como treino, mas o projeto final fica melhor se for de uma área "
        "real, porque você tem acesso às pessoas e aos dados.")
)

cad.section("lab1-modelo", "Lab 1: conectar o workbook e montar o modelo",
    p("O primeiro lab trata da preparação dos dados. A tarefa é trazer o "
      "workbook do cenário e deixar o modelo pronto para as medidas. Um modelo "
      "errado contamina todo o painel.") +
    step([
        ("Crie um arquivo novo",
         "No Power BI Desktop, use <b>Arquivo &rarr; Novo</b>. Salve como "
         "<code>Painel_CenarioN.pbix</code> antes de importar."),
        ("Escolha o workbook",
         "Use um dos cinco: <code>Cenario1_Requisicao_Pericial.xlsx</code>, "
         "<code>Cenario2_Empenho_Contrato.xlsx</code>, "
         "<code>Cenario3_Cadeia_Custodia.xlsx</code>, "
         "<code>Cenario4_Local_Crime.xlsx</code> ou "
         "<code>Cenario5_Analise_Laboratorial.xlsx</code>."),
        ("Obtenha os dados",
         "Use <b>Obter dados &rarr; Pasta de trabalho do Excel</b> e selecione "
         "o arquivo. O Power BI mostra a lista de abas do workbook."),
        ("Marque as 8 abas de dados",
         "Selecione <code>fato_execucao</code> e as 7 <code>dim_*</code>. "
         "Desmarque <code>LEIA-ME</code>, porque ela é documentação e não tabela."),
        ("Ajuste os tipos",
         "No Power Query, use Número Decimal para tempos e custo, Número "
         "Inteiro para chaves e flags, e Data para a coluna <code>data</code>."),
        ("Relacione",
         "No modo Modelo, ligue cada <code>*_key</code> da fato à sua dimensão. "
         "Confirme a cardinalidade muitos para um."),
        ("Valide a contagem",
         "A fato precisa ter 10.352 linhas no C1, 9.541 no C2, 10.840 no C3, "
         "12.664 no C4 ou 13.896 no C5. Se tiver mais, você marcou abas de outro "
         "cenário."),
    ]) +
    code(
        "// Power Query: ler a aba fato do workbook\n"
        "let\n"
        "    Origem = Excel.Workbook(\n"
        "        File.Contents(\"Cenario1_Requisicao_Pericial.xlsx\"),\n"
        "        null, true\n"
        "    ),\n"
        "    Fato = Origem{[Item = \"fato_execucao\", Kind = \"Sheet\"]}[Data],\n"
        "    Cabecalho = Table.PromoteHeaders(Fato, [PromoteAllScalars = true]),\n"
        "    Tipos = Table.TransformColumnTypes(Cabecalho, {\n"
        "        {\"tempo_espera_min\", type number},\n"
        "        {\"tempo_execucao_min\", type number},\n"
        "        {\"etapa_key\", Int64.Type}\n"
        "    })\n"
        "in\n"
        "    Tipos",
        "m"
    ) +
    callout("err", "Não marque LEIA-ME nem abas de outro cenário",
        "A aba <code>LEIA-ME</code> não é tabela. Se você a importar, o modelo "
        "ganha uma tabela vazia. Além disso, não combine workbooks de cenários "
        "diferentes, porque cada um tem a sua própria contagem de linhas.")
)

cad.section("lab2-medidas", "Lab 2: criar as 8 medidas DAX",
    p("Com o modelo pronto, as medidas transformam colunas em respostas. Crie "
      "todas na mesma tabela de medidas para manter o painel organizado.") +
    step([
        ("Crie a tabela de medidas",
         "Em Modelagem, use <b>Inserir tabela de cálculo</b> e nomeie a tabela "
         "como <code>_Medidas</code>. Todas as medidas vão para ela."),
        ("Crie as medidas de tempo",
         "Crie Tempo Espera (h), Tempo Execução (h) e Tempo Total (h). Formate "
         "com uma casa decimal."),
        ("Crie as medidas de leitura",
         "Crie % Espera, Casos, TAT Médio (h), Espera Média (h) e Taxa "
         "Retrabalho."),
        ("Teste cada medida",
         "Coloque um cartão na tela e arraste a medida. Confira o número contra "
         "o caderno. No Cenário 1, a espera é de 92,4% e a fila tem 44 h."),
        ("Formate",
         "Use uma casa decimal para percentuais e horas, e separador de milhar "
         "para a contagem de casos."),
    ]) +
    code(
        "% Espera =\n"
        "DIVIDE(\n"
        "    SUM(fato_execucao[tempo_espera_min]),\n"
        "    SUM(fato_execucao[tempo_espera_min])\n"
        "        + SUM(fato_execucao[tempo_execucao_min])\n"
        ")",
        "dax"
    ) +
    callout("tip", "Teste a medida com um filtro",
        "Se <code>% Espera</code> muda quando você filtra por unidade, o "
        "relacionamento está funcionando. Se o valor fica igual, a medida está "
        "ignorando o filtro. Nesse caso, volte ao modelo.")
)

cad.section("lab3-visuais", "Lab 3: montar os 5 visuais do painel",
    p("Neste lab, o painel ganha forma. A regra é um visual para cada pergunta. "
      "Se você não sabe qual pergunta o visual responde, ele não entra.") +
    step([
        ("Coloque os cartões no topo",
         "Use quatro cartões: TAT Médio (h), % Espera, Casos e Taxa Retrabalho."),
        ("Monte as barras empilhadas",
         "No eixo, use <code>etapa</code>. Nos valores, use Tempo Espera (h) e "
         "Tempo Execução (h). Ordene pela espera."),
        ("Monte o Pareto",
         "Use barras de espera por etapa e uma linha de percentual acumulado. "
         "O visual pode ser o de barras e colunas ou um gráfico combinado."),
        ("Monte a linha do tempo",
         "No eixo, use <code>ano_mes</code> da <code>dim_calendario</code>. No "
         "valor, use TAT Médio (h). Adicione uma linha de meta."),
        ("Monte a matriz de retrabalho",
         "Use <code>unidade</code> nas linhas, <code>etapa</code> nas colunas e "
         "Taxa Retrabalho nos valores. Formate com escala de cor."),
        ("Adicione filtros e título",
         "Inclua segmentações de etapa, unidade e ano. Use o título "
         "&quot;Processo de Requisição Pericial: onde o caso espera&quot;."),
    ]) +
    tbl(["Visual", "Pergunta", "Sinal de alerta"],
        [["Cartões", "Como está o processo?", "TAT alto e espera acima de 85%"],
         ["Barras empilhadas", "Onde se espera mais?", "Uma etapa domina as barras"],
         ["Pareto", "Quais poucas etapas importam?", "Primeira barra acima de 30%"],
         ["Linha do tempo", "Melhorou ou piorou?", "Tendência de alta por três meses"],
         ["Matriz", "Quem concentra o retrabalho?", "Célula muito acima da média"]],
        num_cols=[]) +
    callout("err", "Cinco visuais e cinco filtros diferentes",
        "Se cada visual tem um filtro próprio, o leitor compara coisas "
        "diferentes sem perceber. Use as mesmas segmentações no painel inteiro e "
        "deixe o filtro explícito no título.")
)

cad.section("lab4-hipotese", "Lab 4: ler o painel e escrever a hipótese",
    p("A manhã termina com a interpretação. O painel não decide por você. Ele "
      "reduz a dúvida a uma frase testável.") +
    step([
        ("Selecione o Cenário 1",
         "Filtre o painel para <code>cenario1_processo_pericial</code> e "
         "confirme os números: 92,4% de espera e 44 h na fila."),
        ("Ordene a espera",
         "No Pareto, a Fila perito aparece em primeiro. Anote o percentual de "
         "41,5%."),
        ("Verifique o retrabalho",
         "O retrabalho é parecido entre as etapas, com cerca de 11,6%. Isso "
         "sugere um problema sistêmico, e não de uma pessoa."),
        ("Escreva a hipótese",
         "&quot;O caso espera 44 h na Fila perito, que concentra 41,5% da "
         "espera. A causa provável é a fila por ordem de chegada.&quot;"),
        ("Marque o que falta saber",
         "O painel não diz por que a fila se forma. Anote as perguntas para o "
         "Lab 5: falta perito, falta prioridade ou falta dado na entrada?"),
    ]) +
    kpi([
        ("44 h", "espera na Fila perito"),
        ("41,5%", "da espera total"),
        ("92,4%", "do tempo é espera"),
        ("11,6%", "de retrabalho sistêmico"),
    ]) +
    callout("g", "A ligação entre a manhã e a tarde",
        "A hipótese é o entregável da manhã. A tarde não começa do zero, porque "
        "parte dessa frase. Quem chega à tarde sem a hipótese volta ao painel "
        "antes de desenhar qualquer processo.")
)

cad.section("lab5-descrever", "Lab 5: descrever o processo em texto, com as 7 perguntas",
    p("A tarde começa com texto, e não com desenho. O parágrafo do AS-IS é a "
      "fonte do diagrama e o ponto em que as pessoas reconhecem o próprio "
      "trabalho.") +
    step([
        ("Defina o escopo",
         "Determine onde o processo começa e onde termina. Por exemplo: do "
         "recebimento da requisição na delegacia até a assinatura do laudo."),
        ("Aplique as 7 perguntas",
         "Pergunte quem dispara, onde começa, o que vem depois, se há decisão, "
         "quem faz, o que entra e sai e como termina."),
        ("Anote os tempos",
         "Registre quanto tempo cada etapa leva e quanto tempo o caso fica "
         "parado. Pergunte em dias ou semanas, e não em minutos."),
        ("Registre as dificuldades",
         "Anote onde as pessoas reclamam, o que se repete e com quais palavras "
         "elas descrevem o problema."),
        ("Escreva de 10 a 15 linhas",
         "Produza um parágrafo corrido, sem diagrama. Esse texto é o AS-IS na "
         "linguagem de quem executa."),
    ]) +
    ficha("g", "Dica",
        "Grave a entrevista. Quem passa pelo processo conhece detalhes que "
        "ninguém mais conhece. Esses detalhes explicam a fila que o painel "
        "mostrou.") +
    aplicab(
        "Ao entrevistar quem executa, antes de abrir o Power BI.",
        "O dado mostra onde o problema está; a entrevista mostra por que ele acontece.",
        "No Cenário 1, o painel mostra a fila. A entrevista revela que a fila é por ordem de chegada, e não por prazo legal.")
)

cad.section("lab6-asis", "Lab 6: converter o texto em diagrama AS-IS",
    p("Agora o parágrafo vira diagrama. O objetivo não é a estética. É a "
      "completude e a honestidade, inclusive com o caminho de retorno.") +
    step([
        ("Defina as swimlanes",
         "Quantos atores existem? No fluxo pericial: Delegacia, ATO, "
         "Laboratório e Sistema."),
        ("Coloque cada atividade na faixa certa",
         "Se uma atividade não cabe em nenhuma faixa, crie a faixa que falta. "
         "Isso indica que o processo está mal definido."),
        ("Insira os gateways",
         "Cada condição do tipo se e senão vira um losango. Rotule as setas com "
         "a condição, como Sim e Não."),
        ("Inclua o retorno",
         "Toda devolução ou correção precisa de uma seta de volta. Sem isso, o "
         "diagrama não representa o tempo real."),
        ("Renderize e revise",
         "Cole o texto em <b>mermaid.live</b> ou no GitHub. Leia de cima para "
         "baixo e verifique se a história faz sentido para quem executa."),
    ]) +
    code(
        "flowchart TD\n"
        "    subgraph DELEG[\"Delegacia\"]\n"
        "        A([Requisicao recebida]) --> B[Registrar no SIGT]\n"
        "    end\n"
        "    subgraph ATO[\"ATO - Gabinete\"]\n"
        "        C[Triagem e classificacao] --> D[Dados completos?]\n"
        "        D -->|Nao| C\n"
        "    end\n"
        "    subgraph LAB[\"Laboratorio\"]\n"
        "        E[Fila do perito] --> F[Analise do exame]\n"
        "        F --> G[Revisao tecnica]\n"
        "        G -->|Devolvido| F\n"
        "        G --> H[Assinatura e release]\n"
        "    end\n"
        "    B --> C\n"
        "    D -->|Sim| E\n"
        "    H --> I([Laudo e arquivamento])",
        "mermaid"
    ) +
    callout("err", "O diagrama que ninguém lê",
        "Um diagrama com 40 caixas não comunica. Quebre o processo em "
        "subprocessos e detalhe cada um. Um diagrama legível cabe em uma tela.")
)

cad.section("lab7-tobe-ganho", "Lab 7: desenhar o TO-BE e calcular o ganho",
    p("Com o AS-IS validado e o gargalo medido, o TO-BE nasce do AS-IS. Cada "
      "mudança precisa estar ligada a uma etapa do Pareto.") +
    step([
        ("Copie o AS-IS",
         "Salve <code>processo-asis.mmd</code> como <code>processo-tobe.mmd</code>. "
         "Não desenhe do zero, porque o TO-BE é uma edição do AS-IS."),
        ("Aplique os 5 princípios",
         "Siga a ordem: eliminar, simplificar, integrar, automatizar e padronizar."),
        ("Marque a intervenção",
         "Use <code>style</code> no Mermaid para destacar o que mudou. Assim, "
         "quem lê vê onde a automação atua."),
        ("Defina a meta por etapa",
         "Por exemplo: fila de 44 h para 8 h e triagem de 10 h para 2 h. Meta "
         "sem número não é meta."),
        ("Calcule o ganho",
         "Compare AS-IS e TO-BE nos mesmos dados: espera poupada, TAT, custo e "
         "capacidade liberada."),
        ("Escreva a frase de impacto",
         "&quot;Com a fila priorizada, a espera cai de 44 h para 8 h e libera "
         "43.200 h por ano.&quot; Use número, e não adjetivo."),
    ]) +
    code(
        "flowchart TD\n"
        "    A([Req. recebida]) --> B[SIGT registra com prazo legal]\n"
        "    B --> C[Triagem automatica por tipo]\n"
        "    C --> D{Dados completos?}\n"
        "    D -->|Nao| E[Notificar dados faltantes]\n"
        "    E --> B\n"
        "    D -->|Sim| F[Fila priorizada por prazo]\n"
        "    F --> G[Analise]\n"
        "    G --> H[Revisao]\n"
        "    H --> I([Laudo])\n"
        "    style F fill:#d4edda,stroke:#28a745\n"
        "    style C fill:#d4edda,stroke:#28a745",
        "mermaid"
    ) +
    kpi([
        ("44 h &rarr; 8 h", "espera na fila"),
        ("-82%", "redução na etapa"),
        ("-24%", "redução no TAT"),
        ("43.200 h", "poupadas por ano"),
    ]) +
    callout("g", "O ganho precisa ser plausível",
        "Um ganho de 20% a 40% em processo real já é relevante. Se a conta der "
        "90%, reveja a premissa, porque provavelmente você assumiu que a fila "
        "zera. Fila não zera.")
)

cad.section("lab8-pitch-canvas", "Lab 8: pitch de 3 minutos e canvas do mini app",
    p("O dia termina com comunicação e com a primeira ideia de mini app. Nesta "
      "aula, a ideia fica no canvas. A construção com IA agêntica vem nas "
      "próximas aulas.") +
    step([
        ("Monte o pitch em quatro blocos",
         "Apresente o processo hoje e o gargalo medido, a proposta, o ganho em "
         "número e o que você precisa: decisão, pessoa ou recurso."),
        ("Mostre os dois diagramas lado a lado",
         "Coloque AS-IS e TO-BE na mesma tela. A diferença visual é o argumento."),
        ("Peça feedback ao time",
         "Pergunte o que falta, o que não vai funcionar e onde o processo "
         "trava. Anote e ajuste antes de pedir a decisão."),
        ("Preencha o canvas do mini app",
         "Use cinco blocos: problema, usuário, dado, ação e medida. Escreva uma "
         "frase por bloco, sem definir a tecnologia."),
        ("Escolha o candidato da equipe",
         "Qual etapa do TO-BE pede um app, como formulário, fila, checklist ou "
         "rastreio? Esse é o candidato para a próxima aula."),
    ]) +
    tbl(["Bloco do canvas", "Pergunta", "Exemplo no Cenário 1"],
        [["<b>Problema</b>", "Que dor o app resolve?", "Fila do perito por ordem de chegada"],
         ["<b>Usuário</b>", "Quem usa, onde e quando?", "Triagem do ATO, no desktop"],
         ["<b>Dado</b>", "Que dado entra e sai?", "Requisição, prazo legal e tipo de exame"],
         ["<b>Ação</b>", "O que o app faz?", "Ordena a fila por prazo e alerta o perito"],
         ["<b>Medida</b>", "Como saber se funcionou?", "Espera média na fila, de 44 h para 8 h"]],
        num_cols=[]) +
    checklist([
        "AS-IS validado com quem executa.",
        "Gargalo medido com número no painel.",
        "TO-BE ligado ao gargalo, com cada mudança justificada.",
        "Ganho calculado em tempo e recurso.",
        "Canvas do mini app preenchido com os cinco blocos.",
        "Pedido de decisão explícito.",
    ]) +
    callout("note", "O que vem depois",
        "Na próxima aula, o canvas vira protótipo com IA agêntica. Você "
        "descreve o app em linguagem natural, e a ferramenta constrói a tela. "
        "Nesta primeira aula, o objetivo é sair com o problema bem definido, "
        "porque a IA acelera a construção, mas não decide o que construir.")
)

# =================================================================
# PARTE 9 - CENARIOS POLITEC
# =================================================================
cad.grp("Parte 9 - Cenários POLITEC",
        "Três dos cinco processos, modelados ponta a ponta: AS-IS medido, gargalo e TO-BE.")

cad.section("cenarios-intro", "Os 3 cenários modelados entre os 5 datasets",
    p("Cada cenário abaixo vem com um dataset medido, com 30.733 execuções de "
      "etapa nos três, e um caso completo de AS-IS, gargalo e TO-BE. Os "
      "Cenários 4 e 5 têm a receita de painel na Parte 2. O método AS-IS e "
      "TO-BE desta parte se aplica a eles da mesma forma.") +
    grid2([
        ("\U0001f5fa Cenário 1: requisição pericial",
         "Do registro na delegacia ao laudo assinado. O gargalo é a <b>fila do "
         "perito</b>, com 41,5% da espera e 10.352 execuções."),
        ("\U0001f4b0 Cenário 2: empenho e contrato",
         "Do pedido do setor à publicação do ato. O gargalo é o <b>parecer "
         "jurídico e a autorização</b>, com 51,2% da espera, 9.541 execuções e "
         "a maior taxa de retrabalho."),
        ("\U0001f52c Cenário 3: cadeia de custódia",
         "Da coleta no local à baixa da evidência. O gargalo é a <b>guarda</b>, "
         "com 35,3% da espera, além do risco de lacre, em 10.840 execuções."),
    ])
)

# --- Cenario 1 completo ---
cad.section("cen1-asis", "Cenário 1: o AS-IS da requisição pericial",
    p("Este é o processo mais conhecido da POLITEC. São 8 etapas, 4 atores e "
      "um processo em que <b>92,4% do tempo é espera</b>.") +
    build_process_asis() +
    code(
        "flowchart TD\n"
        "    subgraph DELEG[\"Delegacia\"]\n"
        "        A([Req. recebida]) --> B[Registrar no SIGT - papel + sistema]\n"
        "    end\n"
        "    subgraph ATO[\"ATO - Gabinete\"]\n"
        "        C[Triagem manual] --> D{Dados completos?}\n"
        "    end\n"
        "    subgraph LAB[\"Laboratorio\"]\n"
        "        E[Fila do perito - ESPERA] --> F[Analise do exame]\n"
        "        F --> G[Revisao tecnica]\n"
        "        G --> H[Assinatura e release]\n"
        "    end\n"
        "    subgraph SIS[\"Sistema\"]\n"
        "        S1[Livro de protocolo] --> S2[Envio e arquivamento]\n"
        "    end\n"
        "    B --> C\n"
        "    D -->|Nao| E1[Devolve a delegacia]\n"
        "    E1 --> A\n"
        "    D -->|Sim| E\n"
        "    H --> S1\n"
        "    S2 --> I([Laudo entregue])",
        "mermaid"
    ) +
    tbl(["Etapa", "Espera", "Execução", "Retrabalho"],
        [["1. Entrada", "0 h", "0 h", "11,2%"],
         ["2. Triagem", "10 h", "1 h", "12,7%"],
         ["3. Distribuição", "13 h", "1 h", "11,4%"],
         ["<b>4. Fila perito</b>", "<b>44 h</b>", "0 h", "12,1%"],
         ["5. Análise", "9 h", "5 h", "11,5%"],
         ["6. Revisão", "13 h", "2 h", "10,4%"],
         ["7. Assinatura", "10 h", "0 h", "11,7%"],
         ["8. Arquivamento", "7 h", "0 h", "11,7%"]],
        num_cols=[1, 2, 3]) +
    callout("err", "O que o diagrama revela",
        "O caso atravessa quatro sistemas, que são papel, SIGT, e-mail e "
        "planilha, e muda de mãos quatro vezes. Cada fronteira de swimlane é um "
        "ponto de espera, e é nesse ponto que está o gargalo.")
)

cad.section("cen1-gargalo", "Cenário 1: o gargalo medido na fila do perito",
    p("Ao rodar a tabela dinâmica do Lab 3 nos dados do Cenário 1, a etapa "
      "Fila perito concentra <b>41,5% de toda a espera</b> do processo.") +
    bar_chart(
        ["Fila perito", "Revisão", "Distribuição", "Triagem", "Assinatura", "Análise"],
        [41.5, 12.3, 11.9, 9.8, 9.7, 9.3],
        "Cenário 1: participação da espera por etapa",
        "41,5% da espera do processo está em uma única etapa. Essa fila não "
        "exige mais peritos para encurtar. Exige a ordem correta de atendimento.",
        fmt="{:.1f}%",
        destaque=0
    ) +
    tbl(["Achado", "Número", "Implicação"],
        [["Processo é espera", "92,4%", "O trabalho é mínimo; a parada é o problema"],
         ["Gargalo", "Fila perito, 41,5%", "Atacar a fila, e não a análise"],
         ["Maior execução", "Análise, 5 h", "Há mais trabalho, mas apenas 9,3% da espera"],
         ["Menor espera da análise", "9 h, contra 44 h", "O perito trabalha; o caso espera"]],
        num_cols=[]) +
    ficha("r", "A leitura contraintuitiva",
        "A intuição diz que o gargalo é a análise, que demora 5 h. O dado diz o "
        "contrário: a análise é rápida, e o problema é o caso esperar 44 h na "
        "fila antes de começar. Sem medir, a equipe contrataria mais peritos "
        "para resolver um problema de fila.")
)

cad.section("cen1-tobe", "Cenário 1: o TO-BE com fila priorizada por prazo legal",
    p("A intervenção atua no gargalo. Em vez de atender por ordem de chegada, o "
      "processo prioriza por prazo legal e monitora a carga em tempo real.") +
    build_process_tobe() +
    code(
        "flowchart TD\n"
        "    subgraph DELEG[\"Delegacia\"]\n"
        "        A([Req. recebida]) --> B[SIGT registra com prazo legal]\n"
        "    end\n"
        "    subgraph ATO[\"ATO - Gabinete\"]\n"
        "        C[Triagem assistida por tipo] --> D{Dados completos?}\n"
        "    end\n"
        "    subgraph LAB[\"Laboratorio\"]\n"
        "        F[Fila PRIORIZADA por prazo] --> G[Analise do exame]\n"
        "        G --> H{Revisao?}\n"
        "        H -->|Nao| I[Corrigir]\n"
        "        I --> G\n"
        "        H -->|Sim| J[Revisao tecnica]\n"
        "        J --> K([Laudo])\n"
        "    end\n"
        "    subgraph BI[\"Painel de carga (Power BI)\"]\n"
        "        P[WIP por perito em tempo real]\n"
        "        Q[Alerta se fila > 24h]\n"
        "    end\n"
        "    B --> C\n"
        "    D -->|Nao| R[Notificar dados faltantes]\n"
        "    R --> B\n"
        "    D -->|Sim| F\n"
        "    P -.rebalanceia.-> F\n"
        "    Q -.dispara alerta.-> F\n"
        "    style F fill:#d4edda,stroke:#28a745\n"
        "    style C fill:#d4edda,stroke:#28a745\n"
        "    style P fill:#cce5ff,stroke:#004085\n"
        "    style Q fill:#cce5ff,stroke:#004085\n"
        "    %% verde = automatizado | azul = observabilidade",
        "mermaid"
    ) +
    tbl(["Mudança", "Tipo", "Foco no gargalo"],
        [["Fila por prazo legal", "Integrar e automatizar", "<b>Sim</b>, porque reordena a fila"],
         ["Triagem assistida por tipo", "Automatizar", "Indireto, porque reduz a entrada na fila"],
         ["Notificação de dados faltantes", "Automatizar", "Indireto, porque evita o ciclo de devolução"],
         ["Painel de WIP por perito", "Visualizar em BI", "<b>Sim</b>, porque rebalanceia antes de acumular"],
         ["Alerta de fila acima de 24 h", "Notificar", "<b>Sim</b>, porque aciona antes de virar gargalo"]],
        num_cols=[])
)

cad.section("cen1-ganho", "Cenário 1: o ganho calculado",
    p("A comparação entre o AS-IS medido e o TO-BE proposto mostra o ganho. A "
      "conta usa os mesmos dados e o volume anual do processo.") +
    tbl(["Métrica", "AS-IS", "TO-BE", "Ganho"],
        [["<b>Espera na fila</b>", "44 h", "8 h", "<b>-82%</b>"],
         ["TAT total aproximado", "92 dias", "70 dias", "<b>-24%</b>"],
         ["Fila de casos, por Little's Law", "cerca de 302 casos", "cerca de 230 casos", "menos 72 casos"],
         ["<b>Horas por ano poupadas</b>", "-", "-", "<b>43.200 h</b>"],
         ["Equivalente em pessoa", "-", "-", "<b>cerca de 1 perito-equivalente</b>"]],
        num_cols=[1, 2, 3]) +
    code(
        "Horas poupadas/ano = (44h - 8h) × 1.200 casos/ano\n"
        "                   = 36 h × 1.200\n"
        "                   = 43.200 horas/ano\n"
        "\n"
        "Em peritos-equivalentes:\n"
        "43.200 h ÷ (220 dias × 8 h) ≈ 1 perito",
        "formula"
    ) +
    callout("g", "A frase para a direção",
        "Hoje, 36% do TAT do laudo corresponde ao tempo em que o caso fica "
        "parado na fila. Se a fila for priorizada por prazo legal, o processo "
        "elimina 43 mil horas de espera por ano, sem contratar ninguém e apenas "
        "ajustando a ordem de atendimento.")
)

# --- Cenario 2 completo ---
cad.section("cen2-asis", "Cenário 2: o AS-IS do empenho e contrato",
    p("Este é o caminho do dinheiro público, com 7 etapas, 5 unidades e a maior "
      "taxa de retrabalho entre os cinco datasets, de cerca de 16,6%.") +
    build_process_orcamento() +
    code(
        "flowchart TD\n"
        "    subgraph SETOR[\"Setor solicitante\"]\n"
        "        A([Pedido do setor - PAPEIS]) --> B[Cotacao no sistema]\n"
        "    end\n"
        "    subgraph COMPRAS[\"Divisao de Compras\"]\n"
        "        C[Mapa comparativo] --> D{Valor / modalidade?}\n"
        "    end\n"
        "    subgraph JUR[\"Assessoria Juridica\"]\n"
        "        E[Parecer juridico - ESPERA] --> F{Conforme a lei?}\n"
        "    end\n"
        "    subgraph CTRL[\"Ordenador / Controle\"]\n"
        "        G[Autorizacao do ordenador] --> H[Empenho e contratacao]\n"
        "    end\n"
        "    subgraph SIS[\"Sistema\"]\n"
        "        I[Publicacao do ato]\n"
        "    end\n"
        "    B --> C\n"
        "    D -->|Cotacao direta| E\n"
        "    D -->|Licitacao| E\n"
        "    F -->|Nao| C\n"
        "    F -->|Sim| G\n"
        "    H --> I\n"
        "    I --> J([Contrato assinado])",
        "mermaid"
    ) +
    tbl(["Etapa", "Espera", "Execução", "Retrabalho"],
        [["1. Pedido", "0 h", "4 h", "15,9%"],
         ["2. Cotação", "10 h", "0 h", "16,4%"],
         ["3. Mapa comparativo", "21 h", "6 h", "17,0%"],
         ["<b>4. Parecer jurídico</b>", "<b>36 h</b>", "5 h", "17,0%"],
         ["<b>5. Autorização</b>", "<b>27 h</b>", "1 h", "16,3%"],
         ["6. Empenho", "11 h", "0 h", "16,6%"],
         ["7. Publicação", "18 h", "0 h", "16,9%"]],
        num_cols=[1, 2, 3]) +
    callout("err", "Onde o processo perde tempo",
        "As duas aprovações, parecer e autorização, somam 51,2% da espera. Além "
        "disso, o retrabalho de cerca de 16,6% indica que um em cada seis "
        "documentos volta para refação, quase sempre no mapa e no parecer.")
)

cad.section("cen2-gargalo", "Cenário 2: o gargalo das aprovações encadeadas",
    p("Diferente do Cenário 1, o gargalo aqui é um conjunto de etapas. São duas "
      "aprovações em sequência, e nenhuma delas é medida com frequência.") +
    bar_chart(
        ["Parecer jurídico", "Autorização", "Mapa comparativo", "Publicação", "Empenho", "Cotação"],
        [29.3, 21.9, 17.0, 14.7, 10.9, 6.2],
        "Cenário 2: participação da espera por etapa",
        "Parecer e autorização somam 51,2% da espera. São as duas únicas "
        "aprovações do processo.",
        fmt="{:.1f}%",
        destaque=0
    ) +
    tbl(["Causa raiz", "Como confirmar", "Evidência no processo"],
        [["Fila única no jurídico", "Contar quantos processos ficam na fila", "36 h de espera média"],
         ["Autorizador com muitas pendências", "Pedir a pauta do ordenador", "27 h de espera"],
         ["Parecer devolvido com frequência", "Contar devoluções", "16,6% de retrabalho"],
         ["Expediente que chega tarde", "Registrar a hora de chegada", "A fila cresce no fim do dia"]],
        num_cols=[])
)

cad.section("cen2-tobe", "Cenário 2: o TO-BE com pauta automática e alerta de dotação",
    p("A intervenção não é aprovar mais rápido. É ordenar e avisar, com uma "
      "pauta automática que monta o que vence e alerta quando algo trava.") +
    code(
        "flowchart TD\n"
        "    subgraph SETOR[\"Setor\"]\n"
        "        A([Pedido - formulario digital]) --> B[Cotacao automatica]\n"
        "    end\n"
        "    subgraph COMPRAS[\"Compras\"]\n"
        "        C[Mapa comparativo assistido] --> D{Dotacao suficiente?}\n"
        "    end\n"
        "    subgraph JUR[\"Juridico\"]\n"
        "        E[Pauta automatica por prazo] --> F[Parecer]\n"
        "    end\n"
        "    subgraph CTRL[\"Ordenador\"]\n"
        "        G[Autorizacao com alerta de fila] --> H[Empenho]\n"
        "    end\n"
        "    D -->|Nao| D1[Alerta de dotacao ao setor]\n"
        "    D -->|Sim| E\n"
        "    E --> F\n"
        "    F --> G\n"
        "    H --> I[Publicacao automatica]\n"
        "    subgraph BI[\"Painel de compras\"]\n"
        "        P[Expedientes parados > 48h]\n"
        "    end\n"
        "    P -.notifica.-> E\n"
        "    P -.notifica.-> G\n"
        "    style E fill:#d4edda,stroke:#28a745\n"
        "    style D1 fill:#fff3cd,stroke:#ffc107\n"
        "    style P fill:#cce5ff,stroke:#004085",
        "mermaid"
    ) +
    tbl(["Intervenção", "Tipo", "Resolve"],
        [["Pauta automática por prazo", "Automatizar", "Fila do jurídico, com 29,3% da espera"],
         ["Alerta de dotação insuficiente", "Automatizar e notificar", "Retrabalho do mapa"],
         ["Checklist de parecer", "Padronizar", "16,6% de retrabalho"],
         ["Painel de expedientes parados", "Visualizar em BI", "Fila do ordenador, com 21,9% da espera"],
         ["Formulário digital de pedido", "Digitalizar", "Papel e redigitação"]],
        num_cols=[])
)

cad.section("cen2-ganho", "Cenário 2: o ganho",
    p("O ganho aparece nas duas aprovações e no retrabalho. Além disso, a "
      "redução de uma etapa afeta as etapas seguintes, porque o processo é "
      "encadeado.") +
    tbl(["Métrica", "AS-IS", "TO-BE", "Ganho"],
        [["<b>Parecer jurídico, espera</b>", "36 h", "14 h", "<b>-61%</b>"],
         ["<b>Autorização, espera</b>", "27 h", "10 h", "<b>-63%</b>"],
         ["<b>Retrabalho</b>", "16,6%", "6,0%", "<b>-64%</b>"],
         ["TAT do empenho, aproximado", "38 dias", "26 dias", "<b>-32%</b>"],
         ["Horas por ano poupadas", "-", "-", "<b>52.800 h</b>"]],
        num_cols=[1, 2, 3]) +
    callout("g", "O efeito em cadeia",
        "Quando o mapa comparativo volta corrigido, ele volta antes e o parecer "
        "espera menos. O ganho não está apenas na etapa otimizada, mas também "
        "nas etapas seguintes. Por isso, o processo é medido inteiro, e não "
        "etapa por etapa.")
)

# --- Cenario 3 completo ---
cad.section("cen3-asis", "Cenário 3: o AS-IS da cadeia de custódia",
    p("Este é o processo mais crítico quanto à rastreabilidade. Além do tempo, "
      "o problema é o risco de prova, porque um lacre aberto pode inviabilizar "
      "o laudo.") +
    build_process_custodia() +
    code(
        "flowchart TD\n"
        "    subgraph CAMPO[\"Operacao de campo\"]\n"
        "        A([Coleta no local]) --> B[Acondicionamento e lacre]\n"
        "    end\n"
        "    subgraph CTRL[\"Controle de custodia\"]\n"
        "        C[Registro da ocorrencia] --> D[Transporte ao destino]\n"
        "    end\n"
        "    subgraph LAB[\"Laboratorio\"]\n"
        "        E[Recebimento e conferencia] --> F{Lacre confere?}\n"
        "        F -->|Nao| F1[Divergencia - acionar responsavel]\n"
        "        F1 --> G[Guarda / refrigeracao]\n"
        "        F -->|Sim| G\n"
        "        G --> H[Pericia propriamente dita]\n"
        "        H --> I[Baixa e destino final]\n"
        "    end\n"
        "    B --> C\n"
        "    D --> E\n"
        "    I --> J([Destino final registrado])",
        "mermaid"
    ) +
    tbl(["Etapa", "Espera", "Execução", "Divergência de lacre"],
        [["1. Coleta", "0 h", "2 h", "4,9%"],
         ["2. Lacre", "11 h", "1 h", "5,5%"],
         ["3. Registro", "12 h", "0 h", "3,9%"],
         ["4. Transporte", "16 h", "3 h", "4,2%"],
         ["5. Recebimento", "14 h", "1 h", "5,5%"],
         ["<b>6. Guarda</b>", "<b>55 h</b>", "0 h", "4,0%"],
         ["7. Perícia", "21 h", "6 h", "5,2%"],
         ["8. Baixa", "25 h", "0 h", "4,6%"]],
        num_cols=[1, 2, 3]) +
    callout("err", "O gargalo duplo",
        "A etapa 6, a guarda, concentra 35,3% da espera. O gargalo real, porém, "
        "é duplo: o tempo de guarda e a fragilidade do lacre em papel, com 4,8% "
        "de divergência. O TO-BE precisa atacar os dois.")
)

cad.section("cen3-gargalo", "Cenário 3: o gargalo da guarda e da rastreabilidade",
    p("Neste cenário, a leitura muda. O gargalo não é apenas de tempo, mas de "
      "confiabilidade do processo. Uma evidência parada 55 h na guarda e um "
      "lacre em papel são riscos diferentes.") +
    bar_chart(
        ["Guarda", "Baixa", "Perícia", "Transporte", "Recebimento", "Registro", "Lacre"],
        [35.3, 16.4, 13.8, 10.6, 6.7, 5.7, 5.3],
        "Cenário 3: participação da espera por etapa",
        "A guarda responde por 35,3% da espera. O custo maior deste processo, "
        "porém, não está em nenhum desses números.",
        fmt="{:.1f}%",
        destaque=0
    ) +
    tbl(["Risco", "Probabilidade", "Impacto", "Zona"],
        [["Lacre aberto no transporte", "4,2%", "Alto, porque inviabiliza a prova", "<b>Vermelha</b>"],
         ["Divergência no recebimento", "5,5%", "Alto", "<b>Vermelha</b>"],
         ["Amostra que se degrada na guarda", "Média", "Alto", "<b>Vermelha</b>"],
         ["Perda de rastreio do responsável", "Média", "Médio", "Amarela"]],
        num_cols=[]) +
    ficha("r", "A diferença deste cenário",
        "Nos Cenários 1 e 2, o gargalo é econômico, porque tempo é dinheiro. "
        "Aqui, o gargalo é jurídico, porque rastreabilidade é validade da prova. "
        "Um TO-BE que apenas reduz tempo é insuficiente. Ele precisa garantir o "
        "rastreio.")
)

cad.section("cen3-tobe", "Cenário 3: o TO-BE com custódia e QR Code",
    p("A intervenção troca o lacre em papel por rastreio digital. Cada "
      "transferência vira um evento com responsável, hora e QR Code. Além "
      "disso, um alerta dispara se a evidência ficar parada além do prazo.") +
    code(
        "flowchart TD\n"
        "    subgraph CAMPO[\"App de custodia (campo)\"]\n"
        "        A([Coleta]) --> B[QR Code gerado no local]\n"
        "        B --> C[Foto do lacre + geolocalizacao]\n"
        "    end\n"
        "    subgraph CTRL[\"Sistema de custodia\"]\n"
        "        D[Registro automatico] --> E{Responsavel confere?}\n"
        "    end\n"
        "    subgraph LAB[\"Laboratorio\"]\n"
        "        F[Leitor QR no recebimento] --> G{Lacre confere?}\n"
        "        G -->|Nao| H[BLOQUEIO + alerta ao responsavel]\n"
        "        G -->|Sim| I[Guarda com alerta de prazo]\n"
        "        I --> J[Pericia]\n"
        "        J --> K[Baixa com assinatura digital]\n"
        "    end\n"
        "    C --> D\n"
        "    E -->|Nao| H\n"
        "    E -->|Sim| F\n"
        "    H --> G\n"
        "    subgraph ALERTA[\"Alertas automaticos\"]\n"
        "        L1[Para > 24h na guarda]\n"
        "        L2[Divergencia de lacre]\n"
        "        L3[Transporte > 48h]\n"
        "    end\n"
        "    L1 -.-> I\n"
        "    L2 -.-> H\n"
        "    L3 -.-> F\n"
        "    style B fill:#d4edda,stroke:#28a745\n"
        "    style F fill:#d4edda,stroke:#28a745\n"
        "    style H fill:#f8d7da,stroke:#dc3545\n"
        "    style L1 fill:#cce5ff,stroke:#004085\n"
        "    style L2 fill:#cce5ff,stroke:#004085",
        "mermaid"
    ) +
    tbl(["Intervenção", "Tipo", "Resolve"],
        [["QR Code por evidência", "Digitalizar e rastrear", "Lacre em papel e 5,5% de divergência"],
         ["Leitor de QR no recebimento", "Automatizar", "Conferência manual da etapa 5"],
         ["Bloqueio e alerta em divergência", "Automatizar e notificar", "4,8% de divergência total"],
         ["Alerta de guarda acima de 24 h", "Automatizar", "35,3% da espera"],
         ["Assinatura digital na baixa", "Digitalizar", "Rastreabilidade do destino"]],
        num_cols=[])
)

cad.section("cen3-ganho", "Cenário 3: o ganho",
    p("O ganho aparece no tempo de guarda, na divergência de lacre e na "
      "rastreabilidade. Neste cenário, a redução de tempo é importante, mas a "
      "garantia de rastreio tem peso maior.") +
    tbl(["Métrica", "AS-IS", "TO-BE", "Ganho"],
        [["<b>Espera na guarda</b>", "55 h", "18 h", "<b>-67%</b>"],
         ["<b>Divergência de lacre</b>", "4,8%", "menos de 0,5%", "<b>-90%</b>"],
         ["Rastreio do responsável", "Manual e pouco confiável", "Digital e automático", "<b>Total</b>"],
         ["TAT da custódia, aproximado", "210 dias", "180 dias", "<b>-14%</b>"],
         ["Horas por ano poupadas", "-", "-", "<b>46.000 h</b>"]],
        num_cols=[1, 2, 3]) +
    callout("g", "O ganho que não cabe em número",
        "Neste cenário, o ganho maior não é tempo, e sim validade da prova. Um "
        "lacre com rastreio digital evita 4,8% de divergência e sustenta a "
        "cadeia de custódia perante o Ministério Público. Esse argumento vale "
        "mais do que a hora poupada.")
)

# =================================================================
# PARTE 10 - FECHAMENTO
# =================================================================
cad.grp("Parte 10 - Fechamento",
        "O método resumido, os erros comuns, o quiz, o glossário e as referências.")

cad.section("metodo-resumido", "O método resumido para levar ao seu processo",
    p("O dia tem dois métodos que se encaixam. A manhã sai do dado para a "
      "hipótese, e a tarde sai da hipótese para o processo redesenhado. Por "
      "isso, o método da manhã e o da tarde aparecem juntos.") +
    flow_h([("\U0001f4c4", "Workbook"), ("\U0001f517", "Modelo"),
            ("\U0001f4d0", "Medidas"), ("\U0001f4ca", "Painel"),
            ("\U0001f4a1", "Hipótese")]) +
    p("Na tarde, siga os seis passos abaixo como checklist:") +
    step([
        ("1. Delimite", "Onde começa e onde termina o processo? Escolha um processo real."),
        ("2. Descreva", "Aplique as 7 perguntas e escreva o parágrafo do AS-IS."),
        ("3. Diagrame", "Converta o texto em Mermaid ou BPMN, com swimlanes por ator."),
        ("4. Meça", "Compare espera e execução por etapa e encontre o gargalo no Pareto."),
        ("5. Redesenhe o TO-BE", "Elimine, simplifique, integre e automatize a etapa que é o gargalo."),
        ("6. Automatize e prove", "Faça a intervenção digital, calcule o ganho e apresente o resultado."),
    ]) +
    ficha("g", "A frase final",
        "Desenhe, meça, mude e prove. Quatro verbos que resumem a aula e o "
        "método de melhoria de processo com dado.")
)

cad.section("erros-comuns", "Erros comuns: o que não fazer",
    ul([
        "<b>Painel sem pergunta</b>: 30 visuais que não mudam uma decisão são custo, não instrumento.",
        "<b>Somar a fato depois de juntar com a dimensão</b>: duplica linhas e aumenta a espera.",
        "<b>Usar medida implícita no lugar de explícita</b>: o número aparece, mas ninguém sabe de onde veio.",
        "<b>Automatizar antes de medir</b>: gasta recurso em um processo que talvez não seja o gargalo.",
        "<b>Criar um TO-BE utópico</b>: fila zero e laudo em 2 h não convencem ninguém.",
        "<b>Medir execução sem medir espera</b>: o gargalo quase sempre está na fila, e não no trabalho.",
        "<b>Desenhar sem quem executa</b>: processo desenhado longe da realidade não é adotado.",
        "<b>Confundir projeto com operação</b>: atendimento diário é operação, e não projeto.",
        "<b>Esquecer o caminho de retorno</b>: sem o fluxo de correção, o diagrama não representa o tempo.",
        "<b>Prometer 90% de ganho</b>: um ganho de 20% a 40% em processo real já é relevante.",
        "<b>Ignorar a fronteira do sistema</b>: automatizar o que depende de outro órgão sem acordo.",
    ]) +
    callout("err", "O erro que custa mais",
        "Automatizar o processo errado. Você entrega no prazo, e o gargalo "
        "continua no mesmo lugar, agora com um sistema caro rodando por cima. "
        "Por isso, meça primeiro.")
)

cad.section("quiz", "Quiz final: 15 perguntas",
    p("As 15 perguntas cobrem painel, DAX, BPMN, Mermaid, gargalos e TO-BE.") +
    q("Em BPMN, o losango (gateway) representa...",
      ["a) Uma atividade", "b) Uma decisão ou divisão de fluxo",
       "c) Um evento de início", "d) Uma swimlane"], 1) +
    q("O que é Little's Law (L = λ × W)?",
      ["a) Relação entre fila, chegada e tempo",
       "b) Fórmula de custo de projeto",
       "c) Método de priorização de risco",
       "d) Tipo de gráfico de Pareto"], 0,
      "Número de itens no sistema = taxa de chegada × tempo de permanência.") +
    q("No Mermaid, o subgraph serve para...",
      ["a) Sublinhar texto", "b) Representar swimlanes, agrupando por ator",
       "c) Importar dados", "d) Gerar relatório"], 1) +
    q("Na sequência das 7 perguntas, a pergunta 'quem faz cada etapa'...",
      ["a) Vem primeiro", "b) Vem depois de mapear as atividades",
       "c) É opcional", "d) Vem só no final"], 1,
      "Só faz sentido saber o que existe antes de saber quem faz.") +
    q("O que diferencia o tempo de espera do tempo de execução?",
      ["a) São a mesma coisa", "b) Espera é o tempo parado; execução é o trabalho",
       "c) Espera é o trabalho; execução é a parada",
       "d) Depende do projeto"], 1) +
    q("Onde o gargalo de um processo geralmente está?",
      ["a) Na etapa com mais tempo de execução",
       "b) Na etapa com mais tempo de espera, na fila",
       "c) Sempre na primeira etapa", "d) Na etapa mais barata"], 1,
      "Em média, de 86% a 93% do tempo de processo é espera.") +
    q("O princípio de Pareto aplicado a processos diz que...",
      ["a) Metade do processo é prazo",
       "b) Poucas etapas concentram a maior parte do desperdício",
       "c) Todo processo deve ter 20 etapas",
       "d) O processo ideal tem 80 etapas"], 1) +
    q("Na ordem dos 5 princípios de redesenho, o que vem antes de automatizar?",
      ["a) Padronizar", "b) Eliminar, simplificar e integrar",
       "c) Visualizar", "d) Medir"], 1,
      "Automatizar um processo ruim cria um processo ruim e mais rápido.") +
    q("Um gateway paralelo (+), diferente do exclusivo (X)...",
      ["a) Escolhe só um caminho", "b) Faz todos os caminhos em paralelo",
       "c) Não existe em BPMN", "d) É só para mensagens"], 1) +
    q("O que o sequenceDiagram do Mermaid mostra que o flowchart não mostra bem?",
      ["a) O fluxo de mensagens entre atores no tempo",
       "b) O custo do processo", "c) O gráfico de espera", "d) O organograma"], 0) +
    q("No Power BI, o grão da tabela fato_execucao é...",
      ["a) 1 caso completo", "b) 1 execução de etapa",
       "c) 1 unidade", "d) 1 dia"], 1,
      "Cada linha é uma etapa de um caso. Por isso, a soma de espera por etapa é válida.") +
    q("Para provar o ganho de um TO-BE, você compara...",
      ["a) O TO-BE com o AS-IS medido, nos mesmos dados",
       "b) O TO-BE com a opinião do sponsor",
       "c) O AS-IS com o orçamento",
       "d) O TO-BE com outro projeto"], 0) +
    q("Qual é a primeira automação, na Onda 1, com menor custo e efeito rápido?",
      ["a) Trocar todo o sistema", "b) Alertas de prazo e painel de carga em BI",
       "c) Contratar mais gente", "d) Refazer o banco de dados"], 1) +
    q("No Cenário 1, da requisição pericial, o gargalo medido é...",
      ["a) A análise do exame", "b) A fila do perito",
       "c) A assinatura", "d) O arquivamento"], 1,
      "41,5% de toda a espera do processo está na fila do perito.") +
    q("Por que versionar o diagrama do processo AS-IS no Git?",
      ["a) Para ficar mais apresentável",
       "b) Para ter linha de base e histórico do processo",
       "c) Porque o GitHub exige",
       "d) Para impressionar a direção"], 1)
)

cad.section("glossario", "Glossário rápido da Aula 6",
    glossary([
        ("Painel de processo", "Relatório visual que responde onde o caso espera e qual etapa atacar."),
        ("Workbook (Excel)", "Arquivo .xlsx com as tabelas do dataset, uma por aba, e a aba LEIA-ME."),
        ("Grão da fato", "O que uma linha representa. Aqui, uma execução de etapa."),
        ("Power Query", "Editor de transformação do Power BI, com cabeçalho, tipos e colunas calculadas."),
        ("DAX", "Linguagem de medidas do Power BI, com SUM, CALCULATE, DIVIDE e outras funções."),
        ("Medida e coluna", "A medida é um cálculo avaliado no contexto do filtro; a coluna guarda o dado bruto."),
        ("Segmentação (slicer)", "Filtro visual que não altera o modelo, apenas o que aparece no painel."),
        ("AS-IS", "Diagrama do processo como ele é hoje."),
        ("TO-BE", "Diagrama do processo como ele será depois da intervenção."),
        ("BPMN 2.0", "Notação padrão internacional para modelar processos, da OMG e da ISO 19510."),
        ("Mermaid", "Linguagem de texto que gera diagramas, como flowchart, sequence, state e gantt."),
        ("Evento (BPMN)", "Ponto que dispara, espera ou detecta: início, intermediário ou fim."),
        ("Atividade (BPMN)", "O que é feito: tarefa ou subprocesso."),
        ("Gateway (BPMN)", "Losango que decide ou divide o fluxo: exclusivo, paralelo ou inclusivo."),
        ("Swimlane ou lane", "Faixa que indica quem executa a atividade."),
        ("Subgraph (Mermaid)", "Bloco que agrupa atividades e equivale a uma swimlane."),
        ("Gargalo", "Etapa que mais restringe o fluxo, medida por espera ou por ação."),
        ("Espera (wait time)", "Tempo em que o caso fica parado na fila."),
        ("Execução (touch time)", "Tempo em que alguém efetivamente trabalha no caso."),
        ("TAT", "Tempo de ciclo total do processo, com a soma de esperas e execuções."),
        ("Little's Law", "L = λ × W, em que a fila é o produto da chegada pelo tempo."),
        ("Pareto", "Ordenação por impacto para identificar os 20% críticos."),
        ("WIP", "Work in Progress, ou itens em processamento simultâneo."),
        ("Retrabalho", "Refazer uma etapa já feita, por erro ou devolução."),
        ("Intervenção digital", "Mudar o processo com tecnologia, como app, automação, BI ou script."),
        ("Roadmap do TO-BE", "Implantar o TO-BE em ondas, medindo o ganho de cada uma."),
        ("Stakeholder", "Parte interessada no projeto, como sponsor, equipe, usuário ou cliente."),
        ("Sponsor", "Quem aprova e libera recursos e decisões do projeto."),
    ])
)

cad.section("referencias", "Referências e para ir além",
    ul([
        "<b>BPMN 2.0 (OMG)</b> - <code>omg.org/spec/BPMN/2.0/</code>: a especificação oficial da notação.",
        "<b>Mermaid</b> - <code>mermaid.js.org</code> e o <b>Mermaid Live Editor</b> (mermaid.live), para renderizar online.",
        "<b>ISO 19510</b>: padrão internacional de modelagem de processos.",
        "<b>Lean Enterprise e Value Stream Mapping</b>: a disciplina de mapear o fluxo e localizar o desperdício.",
        "<b>Womack e Jones</b> - <i>Lean Thinking</i>: os princípios de eliminação de desperdício.",
        "<b>John Little</b>: a fórmula L = λ × W, que dimensiona filas.",
        "<b>PMBOK Guide</b>: os 5 grupos de processos da gestão de projetos.",
        "<b>Power Automate e Power BI</b>: as ferramentas de intervenção digital apresentadas nos Dias 4 e 5.",
        "<b>Power BI e DAX</b> - <code>learn.microsoft.com/power-bi</code>: documentação do modelo, das medidas e dos visuais.",
        "<b>Google Antigravity</b> - <code>antigravity.google</code>: plataforma agent-first que será usada nas próximas aulas para prototipar mini apps.",
    ]) +
    callout("tip", "Para começar hoje",
        "Escolha um processo pequeno da sua área, pegue o workbook do cenário "
        "mais parecido e execute a receita da Parte 2. Em seguida, faça o Lab 5, "
        "que descreve o processo em texto, e o Lab 6, que desenha o AS-IS em "
        "Mermaid. Em uma tarde, você tem o painel e o AS-IS do seu processo.")
)

cad.section("encerramento", "O começo da fase de mini apps",
    p("São seis dias de fundamentação, dados, planilha, ETL, dashboards e, "
      "hoje, painel de processo e gestão de projetos. O ciclo do dado até a "
      "decisão está fechado. Agora começa a fase de construir: a tarde das "
      "próximas aulas vira ideação e prototipação de mini apps com IA agêntica.") +
    legenda([
        ("\U0001f4a1", "D1 a D3: dados e planilha",
         "Aprendeu a medir, organizar e validar, que é a base de tudo."),
        ("\U0001f4ca", "D4 e D5: dashboards de BI",
         "Transformou dado em visual para ver o processo e o gargalo."),
        ("\U0001f5fa", "D6: painel e projeto",
         "Montou o painel, leu o gargalo, desenhou AS-IS e TO-BE e preencheu o canvas do mini app."),
        ("\U0001f680", "Próximas aulas: mini apps com IA agêntica",
         "O canvas vira protótipo: você descreve o app e a ferramenta constrói a tela.")
    ]) +
    callout("purple", "A mensagem que fica",
        "&quot;O dado só tem valor quando vira decisão. A decisão só tem valor "
        "quando vira mudança no processo. E a mudança só se sustenta quando é "
        "medida.&quot; Na próxima fase, acrescente a construção: o app só tem "
        "valor quando resolve o gargalo que o painel mostrou.")
)

# =================================================================
# CONSTRUCAO
# =================================================================
cad.build()
ptbr.acentuar_arquivo(pathlib.Path(__file__).resolve().parent / "caderno-dia6.html")