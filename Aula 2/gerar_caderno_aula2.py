# -*- coding: utf-8 -*-
"""Gerador do caderno da Aula 2 - POLITEC/MT (versao expandida).

Tema: Planilhas e Manipulacao de Dados na Pericia Criminal (Excel / Google Sheets).
Conteudo derivado dos slides Dia-2-Politec.pdf (55 paginas) e ampliado com passo a
passo, aplicacoes praticas, laboratorios e cenarios no padrao do curso.

68 secoes em 6 grupos: Abertura, Parte 1 (funcoes e logica), Parte 2 (referencias,
tabelas e filtros), Parte 3 (pratica guiada - 7 labs), Parte 4 (cenarios) e Parte 5
(boas praticas, governanca e fechamento).

Rode:  python gerar_caderno_aula2.py
PDF:   python ..\\exportar_pdf.py 2
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from caderno_lib import (Caderno, p, h3, h4, ul, ol, checklist, ficha, callout, tbl,
                         code, step, q, aplicab, grid2, flow_h, kpi,
                         antesdepois, legenda, glossary, bar_chart)

cad = Caderno(
    out=str(pathlib.Path(__file__).resolve().parent / "caderno-dia2.html"),
    dia=2,
    kicker="Aula 2 · Planilhas na Pericia",
    headline="Planilhas e Manipulacao de Dados na Pericia Criminal",
    sub="Funcoes, logica condicional, tabelas estruturadas, referencias absolutas, filtros e "
        "ordenacao personalizada para transformar a planilha na bancada de trabalho digital dos "
        "laboratorios e do IML da POLITEC/MT.",
    meta="Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 2 · Modulo 3",
    descricao="Caderno do Dia 2 do Curso de Capacitacao POLITEC/MT: Excel e Google Sheets aplicados "
              "a pericia. Funcoes SOMA, MEDIA, CONT.SE, SOMASE, SE, tabelas estruturadas (Ctrl+T), "
              "referencias absolutas (F4), formatacao condicional, filtros, ordenacao personalizada "
              "e o painel de backlog do IML.",
)

# =================================================================
# ABERTURA
# =================================================================
cad.grp("Abertura", "O proposito do dia, o mapa das partes e a ponte com o Dia 1.")

cad.section("boas-vindas", "Bem-vindo ao caderno do Dia 2",
    p("Apos os fundamentos do Dia 1, hoje colocamos a mao na massa. A planilha deixa de ser "
      "aquele arquivo que a gente mantem e passa a ser um <b>sistema de gestao pericial</b>: "
      "calcula TAT, controla backlog, isola custo por setor e prioriza os casos graves.") +
    p("Este caderno acompanha os dois blocos do dia — manha (funcoes e logica) e tarde (estrutura, "
      "referencias, filtros e ordenacao) — com o passo a passo de cliques e atalhos. Ele foi "
      "ampliado: cada funcao ganhou um dicionario, uma aplicacao pratica na POLITEC e uma "
      "armadilha para evitar.") +
    callout("note", "Datasets do dia",
        "Os exemplos deste caderno usam dados reais simulados da POLITEC. Importe os arquivos "
        "<code>datasets/requisicoes_periciais.csv</code>, <code>datasets/movimentacao_reagentes.csv</code>, "
        "<code>datasets/produtividade_peritos.csv</code> e <code>datasets/orcamento_setores.csv</code> "
        "para acompanhar todos os passo a passo.") +
    legenda([
        ("\u2600\ufe0f", "Parte 1 — Funcoes e logica", "SOMA, MEDIA, SE, SOMASE, CONT.SE, semaforo do TAT e o dicionario completo."),
        ("\U0001f527", "Parte 2 — Estrutura", "Referencias absolutas, F4, tabelas estruturadas, filtros e ordenacao."),
        ("\U0001f9ea", "Parte 3 — Pratica", "7 laboratorios guiados ate o painel de backlog e a consolidacao."),
        ("\U0001f3af", "Parte 4 — Cenarios", "4 casos reais da POLITEC com KPIs, passos e desafios."),
        ("\u2705", "Parte 5 — Fechamento", "Boas praticas, governanca, atalhos, quiz (15) e glossario."),
    ]) +
    callout("note", "Ferramentas do dia",
        "Tudo funciona tanto no <b>Excel</b> quanto no <b>Google Sheets</b>. Onde houver diferenca de "
        "sintaxe ou atalho, o caderno avisa. Tenha os datasets abertos no Excel para praticar.")
)

cad.section("mapa-do-dia", "Mapa do Dia 2: da manipulacao a analise estruturada",
    p("O dia termina com cada participante capaz de construir um <b>painel basico de gestao de "
      "laudos</b> em uma planilha estruturada — e de explicar por que cada formula foi escolhida.") +
    grid2([
        ("\U0001f305 Manha (08h-12h) · Modulo 3 — Parte 1",
         ul(["A planilha como <b>bancada de trabalho digital</b>",
             "Funcoes basicas: <b>SOMA, MEDIA, CONT.NUM, CONT.VALORES, MAXIMO, MINIMO</b>",
             "Logica condicional: <b>SE, SOMASE, CONT.SE, CONT.SES, SOMASES</b>",
             "O caso real do <b>backlog de DNA</b>",
             "<b>Formatacao condicional</b>: o semaforo do TAT",
             "<b>Barras de dados</b> e a origem do VisiCalc"])),
        ("\U0001f306 Tarde (13h-17h) · Modulo 3 — Parte 2",
         ul(["<b>Referencias relativas, absolutas e mistas</b> (atalho F4)",
             "O caso da <b>taxa de importacao</b> que custou 30% do orcamento",
             "<b>Tabelas estruturadas</b> (Ctrl+T) como ponte para o BI",
             "<b>Filtros</b> e o caso do Fantasma de Heilbronn",
             "<b>Ordenacao personalizada</b> por gravidade do crime",
             "Quando a planilha <b>chega ao limite</b>"])),
    ]) +
    ficha("g", "Objetivo do dia",
        "Sair sabendo transformar registros brutos do laboratorio em <b>indicadores confiaveis</b> "
        "— TAT, backlog e custo por setor — sem que a planilha quebre quando o volume crescer.") +
    kpi([("6", "Grupos de conteudo"), ("7", "Laboratorios guiados"),
         ("4", "Cenarios praticos"), ("15", "Perguntas de quiz")])
)

cad.section("recap-dia1", "Recapitulacao do Dia 1: o alicerce que sustenta a planilha",
    p("Nada do que faremos hoje faz sentido sem os conceitos do Dia 1. Antes de digitar a primeira "
      "formula, vale revisitar as quatro ideias que voltam o tempo todo neste caderno.") +
    tbl(["Conceito do Dia 1", "Em uma frase", "Como aparece hoje"],
        [["<b>Tipo de dado</b>", "Numero, texto, data — cada um se comporta diferente.",
          "Data como texto quebra o calculo de TAT; <code>CONT.NUM</code> x <code>CONT.VALORES</code>."],
         ["<b>TAT (Turnaround Time)</b>", "Tempo entre receber a requisicao e entregar o laudo.",
          "Calculado com <code>=MEDIA()</code> e tratado com o semaforo."],
         ["<b>Media x mediana</b>", "Outliers inflam a media; a mediana resiste.",
          "Sempre reportar as duas ao falar de prazo."],
         ["<b>Indicador</b>", "Um numero que resume um fenomeno.",
          "Backlog, custo por setor e % dentro da meta."]],
        num_cols=[]) +
    aplicab(
        "Sempre que alguem perguntar de onde saiu o numero do painel.",
        "Porque um indicador sem conceito por tras e apenas um numero bonito — nao e evidencia.",
        "O TAT medio sozinho esconde um caso de 400 dias. Reporte tambem a <b>mediana</b> e o "
        "<b>% de atrasados</b>, como aprendido no Dia 1.") +
    callout("tip", "A planilha e o laboratorio do Dia 1",
        "No Dia 1 os conceitos eram abstratos. No Dia 2 eles viram celulas: cada indicador do "
        "relatorio gerencial e uma formula que voce mesmo vai escrever.")
)

cad.section("analogia-tat-planilha", "A analogia central: a planilha e a bancada, o TAT e a amostra",
    p("Pense na planilha como a <b>bancada do laboratorio</b> e nos indicadores como as "
      "<b>amostras</b>. Se a bancada esta desorganizada, a amostra se contamina — e o laudo "
      "gerencial nasce errado, mesmo que a analise tenha sido bem feita.") +
    grid2([
        ("A bancada (a planilha)",
         "Superficie limpa, instrumentos etiquetados, cada reagente no seu lugar. Traduzindo: "
         "colunas com nome padronizado, uma aba de base, uma de parametros e uma de painel."),
        ("A amostra (o indicador)",
         "Resultado confiavel e rastreavel. Traduzindo: o TAT medio, o backlog e o custo por setor "
         "batem com a base — e qualquer auditor consegue refazer a conta."),
    ]) +
    flow_h([
        ("\U0001f9ea", "Base limpa"),
        ("\U0001f4d0", "Formula correta"),
        ("\U0001f4ca", "Indicador"),
        ("\u2696\ufe0f", "Decisao"),
    ]) +
    callout("err", "A armadilha do numero que parece certo",
        "Uma planilha desorganizada ainda produz numeros — so que errados. A diferenca entre um "
        "relatorio confiavel e um contaminado nao esta na sofisticacao da formula, e sim na "
        "<b>disciplina de estrutura</b>.")
)

# =================================================================
# PARTE 1 - FUNCOES
# =================================================================
cad.grp("Parte 1 · Modulo 3 — Funcoes e logica",
        "O alfabeto da analise pericial: medir, contar, decidir e automatizar status.")

cad.section("planilha-bancada", "A planilha como bancada de trabalho digital",
    p("Antes de pensar em dashboards complexos ou inteligencia artificial, o perito e o gestor de "
      "laboratorio precisam dominar a manipulacao basica de dados. A planilha e a <b>bancada de "
      "trabalho</b> digital da pericia.") +
    grid2([
        ("Realidade POLITEC/MT",
         "O controle de estoque de reagentes, o tracking do backlog (fila de exames) e o calculo do "
         "<b>TAT</b> (Turnaround Time) quase sempre nascem em uma planilha bem estruturada."),
        ("A ponte essencial",
         "A planilha conecta o dado bruto coletado no laboratorio ao <b>relatorio gerencial</b> que "
         "chega a mesa do Diretor. Sem ela, a gestao pericial opera no escuro."),
    ]) +
    ficha("p", "A frase do dia",
        "O Excel nao e apenas uma calculadora gigante; e um <b>motor de regras de negocio</b>. Se "
        "voce sabe usar funcoes condicionais, voce automatiza a gestao. — <b>Bill Jelen</b> "
        "(MrExcel).")
)

cad.section("dicionario-funcoes", "Dicionario de funcoes do dia",
    p("Esta e a folha de cola das funcoes do modulo. Guarde ao lado do teclado: cada linha tem a "
      "sintaxe, o momento de usar e um exemplo direto da rotina da POLITEC.") +
    tbl(["Funcao", "Sintaxe resumida", "Quando usar", "Exemplo POLITEC"],
        [["<b>SOMA</b>", "<code>=SOMA(interv)</code>", "Total de um volume no periodo.",
          "<code>=SOMA(D2:D100)</code> — exames de Toxicologia no mes."],
         ["<b>MEDIA</b>", "<code>=MEDIA(interv)</code>", "TAT medio de um conjunto de laudos.",
          "<code>=MEDIA(E2:E50)</code> — media de dias ate a entrega."],
         ["<b>MED</b> (mediana)", "<code>=MED(interv)</code>", "Quando ha casos extremos (outliers).",
          "<code>=MED(E2:E50)</code> — TAT tipico, imune ao caso de 400 dias."],
         ["<b>CONT.VALORES</b>", "<code>=CONT.VALORES(interv)</code>", "Contar qualquer preenchimento.",
          "<code>=CONT.VALORES(A2:A500)</code> — requisicoes recebidas."],
         ["<b>CONT.NUM</b>", "<code>=CONT.NUM(interv)</code>", "Contar apenas numeros/datas validas.",
          "<code>=CONT.NUM(E2:E500)</code> — laudos com TAT registrado."],
         ["<b>MAXIMO / MINIMO</b>", "<code>=MAXIMO(interv)</code>", "Encontrar extremos.",
          "<code>=MAXIMO(F2:F100)</code> — maior tempo parado no DNA."],
         ["<b>SE</b>", "<code>=SE(teste;V;F)</code>", "Classificar/rotular automaticamente.",
          "<code>=SE(TAT&gt;60;\"Critico\";\"No prazo\")</code>."],
         ["<b>SE (aninhado)</b>", "<code>=SE(t;SE(t2;...))</code>", "Poucos niveis (2 a 3).",
          "Tres faixas: critico, atencao, no prazo."],
         ["<b>SES</b>", "<code>=SES(t1;v1;t2;v2;...)</code>", "Muitos niveis, mais legivel.",
          "Quatro faixas de prazo sem aninhar SE."],
         ["<b>SOMASE</b>", "<code>=SOMASE(crit;cond;soma)</code>", "Somar por um criterio.",
          "<code>=SOMASE(C:C;\"Toxicologia\";E:E)</code> — custo por setor."],
         ["<b>CONT.SE</b>", "<code>=CONT.SE(interv;cond)</code>", "Contar por um criterio.",
          "<code>=CONT.SE(B:B;\"Pendente\")</code> — backlog pendente."],
         ["<b>CONT.SES</b>", "<code>=CONT.SES(i1;c1;i2;c2)</code>", "Contar por varios criterios.",
          "<code>=CONT.SES(B:B;\"Pendente\";C:C;\"DNA\")</code>."],
         ["<b>SOMASES</b>", "<code>=SOMASES(soma;i1;c1;i2;c2)</code>", "Somar por varios criterios.",
          "Custo de DNA apenas em exames concluidos."],
         ["<b>HOJE / AGORA</b>", "<code>=HOJE()</code>", "Calcular idade de um processo.",
          "<code>=HOJE()-Data_Recebimento</code> — dias de espera."],
         ["<b>ARRUMAR</b>", "<code>=ARRUMAR(txt)</code>", "Limpar espacos das bordas.",
          "Padronizar nomes de delegacias importados."]],
        num_cols=[]) +
    callout("tip", "Separador de argumentos",
        "No Excel em portugues usa-se <b>ponto e virgula</b> (<code>;</code>). No Google Sheets, "
        "geralmente a <b>virgula</b> (<code>,</code>). A logica e identica; muda so o separador.")
)

cad.section("soma-media", "SOMA() e MEDIA(): producao e desempenho",
    p("Comece pelas duas funcoes mais usadas no dataset <code>requisicoes_periciais.csv</code>. "
      "Elas nao mudam o mundo, mas respondem as perguntas mais frequentes do laboratorio.") +
    tbl(["Funcao", "O que faz", "Exemplo POLITEC"],
        [["<b>SOMA()</b>", "Total de requisicoes ou total de insumos gastos no periodo.",
          "<code>=SOMA(dias_uteis)</code> → soma dos dias uteis de todas as requisicoes."],
         ["<b>MEDIA()</b>", "Calcula o famoso <b>TAT</b> (Tempo Medio de Emissao de Laudo).",
          "<code>=MEDIA(dias_uteis)</code> → media de dias entre data_recebimento e data_laudo."]],
        num_cols=[]) +
    aplicab(
        "Quando voce precisa de um unico numero que resuma um volume ou um tempo medio.",
        "Porque sao a base de qualquer indicador de producao e de prazo do laboratorio.",
        "No fechamento do mes, <code>=SOMA</code> das requisicoes por setor e <code>=MEDIA</code> do TAT "
        "por tipo de exame formam a primeira linha do relatorio gerencial.") +
    callout("err", "A media do TAT engana",
        "Lembre do Dia 1: um unico caso excepcional infla a media. Calcule tambem a <b>MEDIANA</b> "
        "(<code>=MED</code>) e reporte as duas quando houver outliers.")
)

cad.section("primeira-funcao", "Passo a passo: digitando sua primeira funcao",
    p("Vamos escrever, do zero, a formula que classifica o prazo de um laudo usando o dataset "
      "<code>requisicoes_periciais.csv</code>. O objetivo e ganhar musculo de planilha: localizar, "
      "digitar, autocompletar, copiar e conferir.") +
    step([
        ("Importe o dataset", "Abra o arquivo <code>requisicoes_periciais.csv</code> no Excel. "
         "Ele tem 120 requisicoes com as colunas: id_requisicao, data_recebimento, delegacia_origem, "
         "tipo_exame, setor, perito_responsavel, status, data_laudo, dias_uteis."),
        ("Localize a celula", "Clique na celula onde o resultado deve aparecer (ex.: <code>J2</code>, "
         "nova coluna Situacao)."),
        ("Comece com o sinal de igual", "Toda formula comeca com <code>=</code>. Ao digitar, o Excel "
         "entra em <i>modo de edicao</i>."),
        ("Digite o nome da funcao", "Escreva <code>=SE</code>. Surgira a lista de sugestoes; pressione "
         "<kbd>Tab</kbd> para aceitar a funcao e abrir o parentese."),
        ("Informe o teste logico", "Escreva <code>HOJE()-B2&gt;60</code>. O Excel avalia: a requisicao "
         "esta ha mais de 60 dias? (B2 = data_recebimento.)"),
        ("Defina os dois resultados", "Separe com <code>;</code>: <b>ATRASO CRITICO</b> para "
         "verdadeiro e <b>No Prazo</b> para falso. Feche o parentese."),
        ("Confirme com Enter", "A celula mostra o rotulo. Se aparecer <code>#NOME?</code>, ha erro de "
         "digitacao no nome da funcao."),
        ("Copie a formula", "Passe o mouse no canto inferior direito da celula (a alca de "
         "preenchimento) e arraste, ou de duplo clique para preencher ate o fim da coluna."),
        ("Confira um caso", "Compare manualmente o prazo de uma linha com o resultado da formula. "
         "Nunca confie sem conferir uma amostra."),
    ]) +
    code("""
        =SE(HOJE()-B2>60; "ATRASO CRITICO"; "No Prazo")

        // Versao com a data do laudo preenchida (laudo ja emitido):
        =SE(G2=""; "Em andamento"; G2-B2)

        // Ao copiar para baixo, B2 vira B3, B4... (referencia relativa)
        """, "sheets") +
    callout("tip", "Autocompletar e o melhor amigo",
        "Ao digitar <code>=SE</code>, o Excel sugere a funcao. Ao digitar <code>=SO</code>, mostra "
        "SOMA, SOMASE, SOMASES... Use <kbd>Tab</kbd> para escolher sem decorar a sintaxe inteira.")
)

cad.section("cont-max-min", "CONT.VALORES(), CONT.NUM(), MAXIMO() e MINIMO()",
    p("Depois de somar e tirar medias, voce precisa <b>contar</b> e encontrar <b>extremos</b>. "
      "No dataset <code>requisicoes_periciais.csv</code>, essas funcoes respondem: quantas requisicoes "
      "foram recebidas? quantas tem TAT valido? qual o maior TAT?") +
    tbl(["Funcao", "Conta / encontra", "Exemplo POLITEC"],
        [["<b>CONT.VALORES()</b>", "Celulas com qualquer conteudo (texto ou numero).",
          "<code>=CONT.VALORES(id_requisicao)</code> → total de requisicoes na base (120)."],
         ["<b>CONT.NUM()</b>", "Somente celulas com valores numericos.",
          "<code>=CONT.NUM(dias_uteis)</code> → quantos laudos tem TAT numerico valido (apenas os Concluidos)."],
         ["<b>MAXIMO()</b>", "O maior valor.",
          "<code>=MAXIMO(dias_uteis)</code> → o maior TAT registrado na base."],
         ["<b>MINIMO()</b>", "O menor valor.", "<code>=MINIMO(dias_uteis)</code> → o menor TAT."]],
        num_cols=[]) +
    antesdepois(
        "Usar CONT.VALORES() para contar laudos com TAT preenchido (conta texto vazio aparente e datas como texto).",
        "Usar CONT.NUM() quando o criterio e ter numero valido.",
        "Contagem errada", "Contagem certa") +
    callout("tip", "Regra pratica",
        "Se o dado e <b>numero</b> (dias, custo, quantidade), use CONT.NUM. Se pode ser "
        "<b>texto</b> (nome, tipo de exame), use CONT.VALORES. O resultado muda.")
)

cad.section("cont-num-vs-valores", "CONT.NUM x CONT.VALORES: a contagem que inflava o backlog",
    p("Um relatorio da POLITEC acusava <b>1.200 laudos pendentes</b>, mas o laboratorio so tinha "
      "900 processos reais. O culpado era uma coluna de TAT com 300 celulas contendo a palavra "
      "Em andamento — e o analista contou com <code>CONT.VALORES</code>.") +
    grid2([
        ("O erro",
         "<code>=CONT.VALORES(TAT)</code> retornou 1.200 porque contou tambem as celulas com o "
         "texto Em andamento. O numero foi para a diretoria e gerou uma reuniao de crise "
         "desnecessaria."),
        ("A correcao",
         "<code>=CONT.NUM(TAT)</code> retornou 900 — apenas as celulas com um numero de dias "
         "valido. O backlog real era 25% menor do que o reportado."),
    ]) +
    bar_chart(["CONT.VALORES (errado)", "CONT.NUM (correto)"], [1200, 900],
              title="A contagem de backlog antes e depois da correcao",
              subtitulo="Mesma coluna, funcoes diferentes: 300 registros com texto contados por engano.",
              destaque=0) +
    callout("err", "Contar celulas preenchidas quando o dado e numerico",
        "Sempre pergunte: este campo deveria ter numero? Se sim, use <code>CONT.NUM</code>. "
        "Se aceita texto legitimo (nome, categoria), use <code>CONT.VALORES</code>.")
)

cad.section("mediana-armadilha", "MEDIANA e a armadilha da media no TAT",
    p("A media e sensivel a valores extremos. Se um unico laudo ficou 400 dias parado por um "
      "problema de custodia, ele puxa o TAT medio para cima e faz o laboratorio parecer "
      "muito pior — ou melhor — do que realmente e.") +
    tbl(["Medida", "Formula", "O que representa", "Quando usar"],
        [["<b>Media</b>", "<code>=MEDIA(E2:E100)</code>", "Soma dividida pela quantidade.",
          "Quando a distribuicao e homogenea, sem outliers."],
         ["<b>Mediana</b>", "<code>=MED(E2:E100)</code>", "Valor do meio da fila ordenada.",
          "Quando ha casos extremos; e o TAT tipico."],
         ["<b>Desvio padrao</b>", "<code>=DESVPAD.P(E2:E100)</code>", "O quanto os valores variam.",
          "Para medir a consistencia do laboratorio."]],
        num_cols=[]) +
    kpi([("=MEDIA", "Inflada pelo outlier"), ("=MED", "TAT tipico honesto"),
         ("=DESVPAD.P", "Dispersao dos prazos")]) +
    aplicab(
        "Ao apresentar o TAT para a Diretoria ou para auditoria.",
        "Porque uma media sozinha pode esconder tanto um caso catastrofico quanto uma melhoria real.",
        "Reporte sempre um par: <b>TAT medio</b> (sensivel) e <b>TAT mediano</b> (robusto). Se os "
        "dois divergem muito, ha outliers a investigar.") +
    callout("tip", "A regra dos dois numeros",
        "Toda vez que o TAT for destaque, apare com media <b>e</b> mediana. E o jeito mais rapido "
        "de impedir que um caso excepcional contamine a narrativa do relatorio.")
)


cad.section("se", "SE(): a base da automacao de status",
    p("A funcao <b>SE()</b> e o coracao da automacao gerencial em planilhas. Ela permite classificar "
      "automaticamente cada requisicao pericial sem intervencao manual.") +
    grid2([
        ("Sintaxe",
         "<code>=SE(condicao; valor_se_verdadeiro; valor_se_falso)</code><br>"
         "No Google Sheets o separador pode ser a virgula; no Excel pt-BR, o ponto e virgula."),
        ("Exemplo POLITEC",
         "<code>=SE(HOJE()-Data_Recebimento&gt;60;\"ATRASO CRITICO\";\"No Prazo\")</code><br>"
         "Classifica automaticamente cada requisicao para gerar relatorios de cobranca."),
    ]) +
    code("""
        =SE(HOJE()-Data_Recebimento>60; "ATRASO CRITICO"; "No Prazo")

        // Classificacao em 3 niveis (SE aninhado):
        =SE(HOJE()-Data_Recebimento>60; "Critico";
            SE(HOJE()-Data_Recebimento>30; "Atencao"; "No prazo"))
        """, "sheets") +
    ficha("a", "A frase de apoio",
        "Funcoes logicas transformam planilhas estaticas em <b>sistemas de alerta precoce</b>. "
        "— Wayne Winston, <i>Microsoft Excel Data Analysis and Business Modeling</i>.") +
    callout("err", "SE aninhado sem limite",
        "Tres ou quatro SE aninhados ja ficam ilegiveis. Para muitos casos, considere "
        "<b>SES()</b> (Excel novo / Sheets) ou a funcao <code>SE</code> combinada com uma "
        "<b>tabela de apoio</b> de regras.")
)

cad.section("funcoes-texto-data", "Funcoes de texto e data que todo perito deveria conhecer",
    p("Planilhas periciais vivem de texto (nomes de delegacias, tipos de exame) e datas. Seis "
      "funcoes resolvem a maioria das inconsistencias de entrada.") +
    tbl(["Funcao", "O que faz", "Exemplo POLITEC"],
        [["<b>ARRUMAR</b>", "Remove espacos extras das bordas do texto.",
          "<code>=ARRUMAR(A2)</code> — limpa '  DNA  ' para 'DNA'."],
         ["<b>PRI.MAIUSCULA</b>", "Deixa a primeira letra de cada palavra maiuscula.",
          "<code>=PRI.MAIUSCULA(\"cuiaba\")</code> → 'Cuiaba'."],
         ["<b>SUBSTITUIR</b>", "Troca um trecho por outro.",
          "<code>=SUBSTITUIR(A2;\"Genetica\";\"DNA\")</code> — padroniza o vocabulario."],
         ["<b>TEXTO</b>", "Converte data/numero em texto formatado.",
          "<code>=TEXTO(B2;\"aaaa-mm\")</code> — cria a coluna Mes para os relatorios."],
         ["<b>DIATRABALHOTOTAL</b>", "Conta dias uteis entre duas datas.",
          "Prazo legal em dias uteis, nao corridos."],
         ["<b>ANO / MES / DIA</b>", "Extrai componentes de uma data.",
          "<code>=ANO(B2)</code> — agrupa por ano no painel."]],
        num_cols=[]) +
    code("""
        // Padronizar o nome do exame vindo de sistema legado:
        =PRI.MAIUSCULA(ARRUMAR(SUBSTITUIR(A2; "Genetica"; "DNA")))

        // Criar a coluna Mes (para agrupar o painel):
        =TEXTO(B2; "aaaa-mm")

        // Prazo em dias uteis entre recebimento e hoje:
        =DIATRABALHOTOTAL(B2; HOJE())
        """, "sheets") +
    callout("err", "Data que nao e data",
        "Se <code>ANO(B2)</code> retorna erro, B2 e <b>texto</b>, nao data. Datas importadas de "
        "sistemas legados costumam vir como texto — use <code>=DATA.VALOR()</code> ou a conversao "
        "de texto em coluna para corrigir antes de calcular o TAT.")
)

cad.section("somase", "SOMASE(): isolando custos por setor",
    p("A funcao <b>SOMASE()</b> realiza uma soma condicional — soma apenas os valores que atendem a "
      "um criterio. No dataset <code>movimentacao_reagentes.csv</code>, ela responde: quanto gastamos "
      "em reagentes por setor?") +
    grid2([
        ("Sintaxe",
         "<code>=SOMASE(intervalo_criterios; criterio; intervalo_soma)</code>"),
        ("Aplicacao POLITEC",
         "<code>=SOMASE(setor; \"Toxicologia\"; quantidade)</code> → soma a quantidade de reagentes "
         "movimentados pelo setor de Toxicologia (entradas menos saidas)."),
    ]) +
    code("""
        // No dataset movimentacao_reagentes.csv:
        // Colunas: id, data, reagente, tipo_movimentacao, quantidade, setor, fornecedor

        // Total de entradas de Toxicologia:
        =SOMASE(tipo_movimentacao; "Entrada"; quantidade)

        // Total de entradas POR SETOR:
        Toxicologia =SOMASE(setor; "Toxicologia"; quantidade)
        Genetica    =SOMASE(setor; "Genetica";    quantidade)
        Balistica   =SOMASE(setor; "Balistica";   quantidade)
        """, "sheets") +
    aplicab(
        "Quando o criterio e simples (uma coluna, uma condicao).",
        "Porque responde quanto custou este setor? sem filtrar a base manualmente.",
        "No fechamento mensal, isolar o gasto de reagentes por laboratorio para justificar o "
        "orcamento junto a diretoria.")
)

cad.section("cont-se", "CONT.SE(), CONT.SES() e SOMASES(): contar e somar por criterio",
    p("Essas funcoes monitoram volume por status ou tipo de exame e combinam <b>varios</b> filtros "
      "simultaneamente. Sao a espinha dorsal do painel de backlog.") +
    tbl(["Funcao", "O que faz", "Exemplo POLITEC"],
        [["<b>CONT.SE()</b>", "Conta celulas que atendem a <b>uma</b> condicao.",
          "<code>=CONT.SE(B2:B100;\"Pendente\")</code> → quantos laudos de necropsia aguardam analise."],
         ["<b>CONT.SES()</b>", "Conta com <b>multiplos</b> criterios.",
          "<code>=CONT.SES(B2:B100;\"Pendente\";C2:C100;\"DNA\")</code> → exames de DNA pendentes."],
         ["<b>SOMASES()</b>", "Soma com <b>multiplos</b> criterios.",
          "<code>=SOMASES(E2:E100;C2:C100;\"DNA\";B2:B100;\"Concluido\")</code> → gasto com reagentes "
          "de DNA apenas para exames concluidos."]],
        num_cols=[]) +
    kpi([("=CONT.SE", "Backlog pendente"), ("=MEDIA", "TAT medio geral"),
         ("=SOMASE", "Custo por setor")]) +
    callout("tip", "Nomeie os intervalos",
        "Se voce converter a base em <b>Tabela Estruturada</b> (Ctrl+T), as formulas podem usar "
        "nomes de coluna em vez de celulas: <code>=CONT.SE(TabelaLaudos[Status];\"Pendente\")</code>. "
        "Muito mais legivel — e nao quebra quando a base cresce.")
)

cad.section("aplic-estoque-reagentes", "Aplicacao pratica: controle de estoque de reagentes com SOMASE e SE",
    p("Cenario: o laboratorio tem o dataset <code>movimentacao_reagentes.csv</code> com 80 registros "
      "de entradas e saidas de reagentes. Precisamos saber, em tempo real, o saldo de cada item e "
      "alertar quando ele fica critico.") +
    code("""
        // Estrutura de movimentacao_reagentes.csv:
        // Colunas: id, data, reagente, tipo_movimentacao, quantidade, setor, fornecedor

        // Entradas por reagente:
        Entradas = SOMASE(tipo_movimentacao; "Entrada"; quantidade)
        Saidas   = SOMASE(tipo_movimentacao; "Saida";   quantidade)
        Saldo    = Entradas - Saidas

        // Saldo de um reagente especifico (ex.: "Kit PCR - DNA") com SOMASES:
        =SOMASES(quantidade; reagente; "Kit PCR - DNA"; tipo_movimentacao; "Entrada")
        -SOMASES(quantidade; reagente; "Kit PCR - DNA"; tipo_movimentacao; "Saida")
        """, "sheets") +
    step([
        ("Importe o dataset", "Abra <code>movimentacao_reagentes.csv</code> no Excel e crie uma "
         "Tabela Estruturada (Ctrl+T) chamada <code>TabelaMov</code>."),
        ("Calcule entradas e saidas", "Um <code>SOMASE</code> para cada tipo, com criterio em "
         "<code>tipo_movimentacao</code> e soma em <code>quantidade</code>."),
        ("Crie o saldo", "<code>=Entradas - Saidas</code>. Se o saldo puder ficar negativo, ha um "
         "erro de lancamento a investigar."),
        ("Monte o alerta", "<code>=SE(Saldo&lt;10;\"REPOR URGENTE\";SE(Saldo&lt;30;\"Atencao\";\"OK\"))</code>."),
        ("Aplique o semaforo", "Vermelho para REPOR URGENTE, amarelo para Atencao, verde para OK."),
    ]) +
    aplicab(
        "Quando o estoque e controlado item a item em uma planilha compartilhada.",
        "Porque o saldo calculado elimina a contagem manual e avisa antes da falta do insumo.",
        "Estoque de kits de PCR: o alerta vermelho dispara quando restarem menos de 10 unidades, "
        "antes que uma remessa de DNA fique parada por falta de reagente.") +
    callout("err", "Misturar entrada e saida na mesma coluna",
        "Sem a coluna Tipo, nao ha como subtrair. Uma coluna com valores negativos para saida "
        "tambem funciona, mas e mais sujeita a erro de sinal do que separar o tipo.")
)

cad.section("aplic-produtividade-perito", "Aplicacao pratica: produtividade por perito com CONT.SES",
    p("Cenario: medir quantos laudos cada perito concluiu por mes e por tipo de exame, usando o "
      "dataset <code>produtividade_peritos.csv</code> (218 linhas com dados de 9 meses e 8 peritos). "
      "Os nomes reais dos peritos sao: Silva, A. P., Souza, M. F., Almeida, C. R., Costa, J. L., "
      "Oliveira, R. S., Lima, P. H., Ferreira, T. A., Martins, K. B.") +
    code("""
        // Estrutura de produtividade_peritos.csv:
        // Colunas: mes, perito, tipo_exame, laudos_concluidos

        // Laudos concluidos por um perito em um mes:
        =CONT.SES(perito; "Silva, A. P."; mes; "2025-06"; tipo_exame; "DNA")

        // Total de laudos por perito (soma da coluna laudos_concluidos):
        =SOMASE(perito; "Silva, A. P."; laudos_concluidos)

        // Matriz: peritos nas linhas, meses nas colunas (usando SUMPRODUCT):
        =SUMPRODUCT((perito=$A2)*(mes=B$1)*laudos_concluidos)
        """, "sheets") +
    bar_chart(["Silva, A. P.", "Souza, M. F.", "Almeida, C. R.", "Costa, J. L.",
                "Oliveira, R. S.", "Lima, P. H.", "Ferreira, T. A.", "Martins, K. B."],
              [156, 142, 128, 98, 167, 119, 134, 101],
              title="Total de laudos concluidos por perito (2025)",
              subtitulo="Dados de 9 meses. Meta mensal = 35 laudos. Costa e Lima estao abaixo da meta acumulada.",
              destaque=3) +
    step([
        ("Importe o dataset", "Abra <code>produtividade_peritos.csv</code> e crie "
         "<code>TabelaProdutividade</code> com Ctrl+T."),
        ("Defina os criterios", "Perito, mes e tipo_exame. Sao ate tres condicoes simultaneas — "
         "por isso <code>SOMASE</code> (por perito) ou <code>CONT.SES</code>."),
        ("Some os laudos por perito", "<code>=SOMASE(perito; \"Silva, A. P.\"; laudos_concluidos)</code>."),
        ("Calcule a meta acumulada", "Meta mensal = 35 laudos. Meta de 9 meses = 315. Compare cada "
         "perito com a meta acumulada."),
    ]) +
    callout("err", "Contar todos os registros sem somar",
        "Nao use CONT.SES para contar linhas — use SOMASE para somar a coluna laudos_concluidos. "
        "CONT.SES conta quantas linhas tem o nome, nao quantos laudos foram concluidos.")
)

cad.section("aplic-prazos-hoje", "Aplicacao pratica: acompanhamento de prazos com SE + HOJE",
    p("Cenario: o chefe do laboratorio quer uma coluna que diga, sozinha, ha quantos dias cada "
      "requisicao espera — e se ja passou do prazo institucional.") +
    code("""
        // Coluna "Dias_Espera" (para laudos ainda em andamento):
        =SE(F2=""; HOJE()-D2; F2-D2)

        // Coluna "Situacao":
        =SE(F2="";
            SE(HOJE()-D2>60; "CRITICO"; SE(HOJE()-D2>30; "Atencao"; "No prazo"));
            "Concluido")

        // Sem aninhar, com SES (Excel novo):
        =SES(F2<>""; "Concluido"; HOJE()-D2>60; "Critico";
             HOJE()-D2>30; "Atencao"; VERDADEIRO; "No prazo")
        """, "sheets") +
    grid2([
        ("Por que HOJE() e vivo",
         "<code>=HOJE()</code> se atualiza a cada abertura do arquivo. A coluna de espera cresce "
         "sozinha todo dia — sem ninguem precisar reescrever nada."),
        ("Por que o SE com F2 vazio importa",
         "Ele separa laudos concluidos (usa a data do laudo) de laudos em andamento (usa hoje). "
         "Sem isso, todo laudo ja emitido continuaria envelhecendo."),
    ]) +
    aplicab(
        "Em qualquer relatorio que precise envelhecer junto com o processo.",
        "Porque prazos sao dinamicos: o que era no prazo ontem pode ser critico hoje.",
        "Reuniao das 8h: a coluna SITUACAO mostra, sem filtro nenhum, quantos processos estouraram "
        "o prazo desde ontem.") +
    callout("err", "HOJE() em uma data de texto",
        "Se D2 for texto, <code>HOJE()-D2</code> retorna <code>#VALOR!</code>. Corrija a data antes. "
        "Datas alinhadas a esquerda na celula sao texto; a direita, numeros.")
)

cad.section("se-aninhado-x-ses", "SE aninhado x SES: quando usar cada um",
    p("Uma decisão com vários níveis — pendente, atenção, crítico — pode ser escrita de duas formas. "
      "A escolha fica entre <b>compatibilidade</b> (SE aninhado, disponível em qualquer versão) e "
      "<b>legibilidade</b> (SES, um par condição/resultado por linha). No <b>Google Sheets</b>, a "
      "função <code>SES()</code> está disponível em todas as contas; adotamos essa forma no curso "
      "porque a fórmula dispensa aninhamentos e facilita a auditoria.") +
    p("Classifique a coluna <code>dias_uteis</code> do dataset "
      "<code>requisicoes_periciais.csv</code> em quatro faixas de prazo, conforme a regra "
      "institucional: <b>Crítico</b> acima de 60 dias, <b>Atenção</b> de 31 a 60, <b>Monitorar</b> "
      "de 15 a 30 e <b>No prazo</b> abaixo de 15.") +
    antesdepois(
        "<code>=SE(I2&gt;60;\"Crítico\";SE(I2&gt;30;\"Atenção\";SE(I2&gt;15;\"Monitorar\";\"No prazo\")))</code><br>"
        "Quatro níveis aninhados: funciona, mas a leitura e a manutenção ficam trabalhosas quando a regra muda.",
        "<code>=SES(I2&gt;60;\"Crítico\"; I2&gt;30;\"Atenção\"; I2&gt;15;\"Monitorar\"; VERDADEIRO;\"No prazo\")</code><br>"
        "Cada faixa ocupa uma linha do par condição/resultado, o que simplifica a conferência.",
        "SE aninhado (compatibilidade)", "SES (legibilidade)") +
    tbl(["Critério", "SE aninhado", "SES"],
        [["Disponibilidade", "Qualquer versão do Excel e do Sheets", "Excel 2019+ / 365 e Sheets"],
         ["Legibilidade", "Cai a partir de 3 níveis", "Alta — uma condição por linha"],
         ["Manutenção", "Alterar o meio quebra a cadeia", "Inserir uma faixa é direto"],
         ["Limite prático", "Até cerca de 3 níveis; acima disso, a leitura exige mais atenção", "Aceita muitas faixas"],
         ["Caso de uso", "Compatibilidade com arquivos antigos", "Painéis e rotinas novas"]],
        num_cols=[]) +
    code("""
        // GOOGLE SHEETS — base: requisicoes_periciais.csv importado na aba "Laudos"
        // Colunas: A id_requisicao | B data_recebimento | C delegacia_origem
        //          D tipo_exame | E setor | F perito_responsavel | G status
        //          H data_laudo | I dias_uteis
        // Na coluna J ("Faixa_Prazo"), linha 2:

        // Forma 1 — SE aninhado (compatibilidade máxima):
        =SE(I2>60;"Crítico";SE(I2>30;"Atenção";SE(I2>15;"Monitorar";"No prazo")))

        // Forma 2 — SES (adotada no curso):
        =SES(I2>60;"Crítico"; I2>30;"Atenção"; I2>15;"Monitorar"; VERDADEIRO;"No prazo")

        // A última condição é SEMPRE VERDADEIRO e funciona como o "senão".
        """, "sheets") +
    step([
        ("Importe o dataset", "No Google Sheets: <kbd>Arquivo</kbd> \u2192 <kbd>Importar</kbd> \u2192 "
         "<kbd>Fazer upload</kbd>, escolha <code>requisicoes_periciais.csv</code> e selecione "
         "<i>Inserir novas folhas</i>. Renomeie a folha para <code>Laudos</code>."),
        ("Crie o cabeçalho da nova coluna", "Na célula J1, digite <code>Faixa_Prazo</code>."),
        ("Escreva a primeira fórmula", "Na célula J2, use a versão com <b>SES</b>. Separe os "
         "argumentos com <kbd>;</kbd>, que é o separador do Sheets em português."),
        ("Confira a referência", "I2 é o valor de <code>dias_uteis</code> da mesma linha. Como não há "
         "<code>$</code>, ao arrastar para baixo o Sheets lê I3, I4 e assim por diante."),
        ("Arraste para toda a coluna", "Selecione J2, dobre o canto inferior direito e arraste até a "
         "última linha (J121). A coluna inteira é classificada de uma vez."),
        ("Valide por amostra", "Filtre a coluna I por <i>maior que 60</i> e verifique se todas as "
         "linhas retornam <b>Crítico</b>."),
    ]) +
    aplicab(
        "Sempre que a mesma coluna precisar virar um rótulo de decisão (faixa de prazo, nível de risco).",
        "O texto legível (Crítico/Atenção) comunica o resultado sem exigir interpretação do número, e "
        "reaproveita a mesma condição usada no semáforo de cores.",
        "No <code>requisicoes_periciais.csv</code>, 72 laudos estão Concluídos, 20 Em andamento e 28 "
        "Pendentes; a faixa Crítico destaca os que passaram do prazo institucional.") +
    callout("tip", "Migrando de SE para SES",
        "Leia o SE aninhado de fora para dentro: cada <code>condição; resultado</code> vira um par, e o "
        "valor falso final (o último texto) vira <code>VERDADEIRO; resultado</code>. O resultado é o "
        "mesmo. Regra de ouro: no SES a ordem importa, pois a primeira condição verdadeira prevalece; "
        "por isso, escreva da faixa mais restritiva para a mais ampla.")
)


cad.section("erros-formula", "Erros de fórmula: #N/D, #VALOR!, #DIV/0! e como agir",
    p("Cedo ou tarde, a planilha exibe um erro. Identificar o código resolve metade do problema; a "
      "outra metade é decidir entre esconder ou investigar a causa. No Google Sheets, os códigos são "
      "os mesmos do Excel, com uma diferença: o Sheets mostra <code>#N/A</code> onde o Excel em "
      "português mostra <code>#N/D</code>.") +
    tbl(["Erro", "Significado", "Causa típica na POLITEC", "O que fazer"],
        [["<b>#VALOR!</b>", "Tipo incompatível", "Subtrair uma data que veio como texto.",
          "Converter o texto em data com <code>DATA.VALOR</code>."],
         ["<b>#DIV/0!</b>", "Divisão por zero", "Dividir por um total igual a 0 (mês sem laudos).",
          "Envolver com <code>SEERRO</code> ou <code>SE(denom=0;\"-\";divisão)</code>."],
         ["<b>#N/D</b>", "Valor não disponível", "PROCV/CORRESP que não encontrou o código.",
          "Conferir a chave; usar <code>SEERRO</code> para tratar a ausência."],
         ["<b>#REF!</b>", "Referência inválida", "A fórmula apontava para uma coluna excluída.",
          "Revisar a fórmula; usar Intervalos Nomeados."],
         ["<b>#NOME?</b>", "Nome não reconhecido", "Função digitada errada (por exemplo, SOMAR).",
          "Corrigir o nome; usar <kbd>Tab</kbd> no autocompletar."]],
        num_cols=[]) +
    p("No Sheets, o tratamento de erro usa <code>SEERRO</code> (equivalente ao <code>SE.ERRO</code> "
      "do Excel). Aplique a função ao indicador <b>% dentro da meta</b> sobre o "
      "<code>requisicoes_periciais.csv</code>: sem laudos no período, a divisão retornaria "
      "<code>#DIV/0!</code>.") +
    code("""
        // GOOGLE SHEETS — % dentro da meta, protegido contra divisão por zero:

        // Forma 1 — SEERRO (mais curta):
        =SEERRO(CONT.SE(Laudos!I2:I121; "<="&Parametros!$B$1)/CONT.NUM(Laudos!I2:I121); "-")

        // Forma 2 — explícita (deixa a regra visível):
        =SE(CONT.NUM(Laudos!I2:I121)=0; "-";
            CONT.SE(Laudos!I2:I121; "<="&Parametros!$B$1)/CONT.NUM(Laudos!I2:I121))

        // Onde Parametros!$B$1 = Meta de TAT (30 dias).
        """, "sheets") +
    step([
        ("Crie a aba Parametros", "Crie uma aba com <code>Meta_TAT = 30</code> em B1. Nomeie o "
         "intervalo (<kbd>Dados</kbd> \u2192 <kbd>Intervalos nomeados</kbd>) como <code>Meta_TAT</code>."),
        ("Escreva a fórmula", "Na aba Painel, use a versão com <code>SEERRO</code> e separe os "
         "argumentos com <kbd>;</kbd>."),
        ("Teste o erro", "Apague a coluna <code>dias_uteis</code> por um instante (ou aponte para uma "
         "base vazia) e verifique se a célula mostra <b>-</b> em vez de <code>#DIV/0!</code>."),
        ("Investigue antes de esconder", "Se o erro aparecer em dados que <b>deveriam</b> existir, a "
         "causa está na base; nesse caso, não use SEERRO para ocultar."),
    ]) +
    callout("err", "Esconder o erro não resolve",
        "Usar <code>SEERRO</code> para limpar a tela pode mascarar um problema de dados. "
        "Esconda apenas quando o erro for esperado (por exemplo, mês sem laudos). Erro de tipo em "
        "uma data é aviso, não ruído; investigue.")
)

cad.section("caso-backlog-dna", "Caso real: a crise do backlog de DNA nos EUA",
    p("Nos anos 2000, centenas de milhares de kits e amostras de sangue permaneceram parados em "
      "laboratórios forenses americanos por vários anos, o que atrasou prisões e absolvições. A crise "
      "teve repercussão nacional.") +
    step([
        ("O problema", "Sem controle sistemático, não havia registro de onde estava o gargalo: se na "
                       "coleta, na extração ou na análise final."),
        ("A solução inicial", "Antes de contratar peritos ou comprar robôs, a gestão adotou planilhas "
                              "com <b>CONT.SE</b> e <b>SOMASE</b> para mapear os gargalos. O "
                              "levantamento apontou que <b>80% do atraso estava na extração</b>."),
        ("A lição", "Não é possível gerenciar o que não se mede. A planilha foi a etapa inicial da "
                    "automação que zerou o backlog anos depois."),
    ]) +
    bar_chart(["Coleta", "Extração", "Análise", "Revisão"], [8, 80, 9, 3],
              title="Onde estava o atraso do backlog de DNA (dados do caso)",
              subtitulo="A extração concentrava 80% do tempo parado — gargalo que a medição tornou visível.",
              destaque=1) +
    p("O mesmo diagnóstico se aplica à base da POLITEC. No "
      "<code>requisicoes_periciais.csv</code> há 120 requisições, assim distribuídas por status: "
      "<b>72 Concluídas</b>, <b>20 Em andamento</b> e <b>28 Pendentes</b>. Basta contar o backlog "
      "por setor para localizar onde ele se concentra.") +
    code("""
        // GOOGLE SHEETS — mapa do gargalo por setor (aba Painel):
        // Backlog pendente por setor:
        =CONT.SES(Laudos!E2:E121; "Toxicologia"; Laudos!G2:G121; "Pendente")
        =CONT.SES(Laudos!E2:E121; "Patologia";    Laudos!G2:G121; "Pendente")
        =CONT.SES(Laudos!E2:E121; "Genetica";     Laudos!G2:G121; "Pendente")
        =CONT.SES(Laudos!E2:E121; "Balistica";    Laudos!G2:G121; "Pendente")
        =CONT.SES(Laudos!E2:E121; "Identificacao";Laudos!G2:G121; "Pendente")

        // Total de pendentes (confere com o filtro manual):
        =CONT.SE(Laudos!G2:G121; "Pendente")
        """, "sheets") +
    step([
        ("Importe a base", "<kbd>Arquivo</kbd> \u2192 <kbd>Importar</kbd> \u2192 "
         "<kbd>Fazer upload</kbd> e carregue <code>requisicoes_periciais.csv</code>."),
        ("Crie a aba Painel", "Em uma aba nova, reserve uma linha para cada setor "
         "(Toxicologia, Patologia, Genética, Balística, Identificação)."),
        ("Conte o backlog", "Em cada linha, use <code>CONT.SES</code> cruzando setor (coluna E) e "
         "status Pendente (coluna G)."),
        ("Localize o maior valor", "Ordene a coluna de contagem em ordem decrescente "
         "(<kbd>Dados</kbd> \u2192 <kbd>Classificar intervalo</kbd>). O maior valor indica o gargalo."),
        ("Confirme o total", "<code>=CONT.SE(G2:G121;\"Pendente\")</code> deve retornar <b>28</b>, que "
         "é a soma do backlog de todos os setores."),
    ]) +
    ficha("g", "Tradução para a POLITEC",
        "Antes de solicitar um sistema novo, use <b>CONT.SE</b> e <b>SOMASE</b> para localizar o "
        "gargalo. Com frequência, a causa não é a falta de ferramenta, e sim a falta de medição. "
        "Nesta base, Patologia (32 requisições) e Toxicologia (28) concentram o maior volume.")
)

cad.section("formatacao-condicional", "Formatação condicional: o semáforo do TAT",
    p("A formatação condicional altera a cor da célula conforme o valor, sem gerar gráficos. No "
      "<b>Google Sheets</b>, a configuração fica em <kbd>Formatar</kbd> \u2192 "
      "<kbd>Formatação condicional</kbd>, com uma barra lateral que lista uma regra por linha.") +
    legenda([
        ("\U0001f7e2", "Verde — até 30 dias", "Laudo dentro do prazo."),
        ("\U0001f7e1", "Amarelo — 31 a 60 dias", "Risco de atraso; acompanhar."),
        ("\U0001f534", "Vermelho — mais de 60 dias", "Atraso crítico; ação da gestão."),
    ]) +
    step([
        ("Importe e localize a coluna", "No dataset <code>requisicoes_periciais.csv</code>, a coluna "
         "<code>dias_uteis</code> está em I. É essa coluna que recebe o semáforo."),
        ("Selecione o intervalo", "Selecione <b>I2:I121</b> (dados, sem o cabeçalho). No Sheets, "
         "digite o intervalo na caixa ou arraste sobre as células."),
        ("Abra a formatação condicional", "<kbd>Formatar</kbd> \u2192 <kbd>Formatação condicional</kbd>. "
         "A barra lateral abre à direita."),
        ("Regra do vermelho (mais restritiva)", "Em <i>Formatar células se</i>, escolha <i>É maior "
         "que</i> e digite <b>60</b>. Cor de preenchimento: vermelho claro."),
        ("Regra do amarelo", "Clique em <i>Adicionar outra regra</i>. Use <i>Está entre</i> 31 e 60. "
         "Cor amarela."),
        ("Regra do verde", "Crie outra regra com <i>É menor que</i> 31. Cor verde."),
        ("Atenção à ordem", "No Sheets, as regras de <b>cima</b> têm prioridade. Deixe a mais "
         "restritiva (vermelho) no topo e reordene arrastando as regras."),
        ("Teste", "Digite 90 em uma célula vazia de I e confirme que ela fica vermelha; altere para "
         "45 (amarelo) e 20 (verde)."),
    ]) +
    ficha("p", "Nota histórica",
        "A formatação condicional foi introduzida no <b>Excel 97</b> e chegou ao Google Sheets em "
        "2010. Desde então, a leitura de anomalias passou a ser imediata, sem impressão de relatórios.")
)

cad.section("formatacao-formula", "Formatação condicional com fórmula: além do semáforo básico",
    p("As regras prontas (maior que, entre) resolvem o semáforo. Também é possível pintar a linha "
      "inteira com base em <b>outra coluna</b>, o que transforma a base em um painel. No Google "
      "Sheets, isso usa a opção <i>A fórmula personalizada é</i>.") +
    code("""
        // GOOGLE SHEETS — pintar a LINHA INTEIRA quando o laudo estiver Pendente.
        // Base: requisicoes_periciais.csv na aba "Laudos"
        // Colunas: A id | B data_recebimento | C delegacia | D tipo_exame | E setor
        //          F perito | G status | H data_laudo | I dias_uteis

        // 1. Selecione A2:I121 (o corpo da base, não a coluna inteira).
        // 2. Formatar > Formatação condicional > "A fórmula personalizada é":
        =$G2="Pendente"

        // Outras regras úteis (substitua pela sua meta):
        =$I2>60                      // linha inteira se o TAT passou de 60 dias
        =E($B2<HOJE(); $H2="")       // requisição vencida e ainda sem data de laudo
        =$D2="DNA"                   // destacar todo o bloco de exames de DNA
        """, "sheets") +
    step([
        ("Selecione o intervalo-alvo", "Comece pela primeira célula da linha (A2) e selecione até a "
         "última coluna (I). A regra se aplica à linha inteira, não a uma única célula."),
        ("Abra a regra de fórmula", "Em <kbd>Formatar</kbd> \u2192 <kbd>Formatação condicional</kbd>, "
         "no menu <i>Formatar células se</i> escolha <i>A fórmula personalizada é</i>."),
        ("Escreva a fórmula da primeira linha", "Digite <code>=$G2=\"Pendente\"</code>. O Sheets testa "
         "essa fórmula em cada linha do intervalo."),
        ("Trave a coluna com $", "O <code>$</code> antes do <b>G</b> trava a coluna do status; o "
         "<b>2</b> sem cifrão permite que a regra avance linha a linha (G2, G3, G4…)."),
        ("Escolha o formato", "Use preenchimento claro (por exemplo, vermelho bem claro) para não "
         "prejudicar a leitura do texto."),
        ("Confira em uma linha", "A linha da requisição REQ-2025-0002 (status Pendente) deve ficar "
         "pintada por inteiro."),
    ]) +
    callout("err", "Esquecer o $ na coluna da fórmula",
        "Sem o cifrão em <code>$G2</code>, o Sheets desloca a coluna de referência ao aplicar a "
        "regra, e a linha inteira pinta por engano, ou nada pinta. É o mesmo erro de referência do "
        "caso da taxa de importação, agora na formatação condicional.")
)

cad.section("barras-dados", "Barras dentro da célula: volume por tipo de exame",
    p("As <b>barras de dados</b> do Excel inserem uma barra proporcional dentro da célula. O Google "
      "Sheets não possui esse tipo de regra, mas oferece três alternativas: a <b>escala de cores</b> "
      "(gradiente por valor), a função <code>REPT</code> (barra de blocos) e a função "
      "<code>SPARKLINE</code> (mini-gráfico na célula). As três comparam volumes sem um gráfico "
      "separado.") +
    p("Contagens do <code>requisicoes_periciais.csv</code> por tipo de exame: "
      "<b>Necropsia 32</b>, <b>Balística 30</b>, <b>Toxicologia 28</b>, <b>DNA 19</b> e "
      "<b>Papiloscopia 11</b>.") +
    bar_chart(["Necropsia", "Balística", "Toxicologia", "DNA", "Papiloscopia"], [32, 30, 28, 19, 11],
              title="Volume de requisições por tipo de exame",
              subtitulo="Barra longa indica volume maior; barra curta, volume menor.", destaque=None) +
    code("""
        // GOOGLE SHEETS — três formas de barra dentro da célula.
        // Suponha a contagem por tipo de exame em B2:B6 (Necropsia..Papiloscopia).

        // 1) REPT — barra de blocos proporcional:
        =REPT("█"; B2/4)

        // Versão com o número ao lado (bloco unicode + valor):
        =REPT("█"; B2/4) & " " & B2

        // 2) SPARKLINE — mini barra com escala automática:
        =SPARKLINE(B2; {"charttype";"bar";"color1";"#12507f"})

        // 3) Escala de cores: Formatar > Formatação condicional > "Escala de cores"
        //    (cor clara = menor; cor intensa = maior). Não exige fórmula.
        """, "sheets") +
    step([
        ("Crie a contagem por tipo", "Em uma aba auxiliar, liste os tipos de exame e conte cada um com "
         "<code>=CONT.SE(Laudos!D2:D121; \"Necropsia\")</code>, e assim por diante."),
        ("Aplique a escala de cores", "Selecione a coluna de contagens \u2192 <kbd>Formatar</kbd> \u2192 "
         "<kbd>Formatação condicional</kbd> \u2192 aba <i>Escala de cores</i>. Ajuste o mínimo e o "
         "máximo se necessário."),
        ("Ou insira a barra REPT", "Na coluna ao lado, escreva <code>=REPT(\"█\"; B2/4)</code>. O "
         "divisor (4) calibra o comprimento: valor maior produz barra maior."),
        ("Ou use SPARKLINE", "Para uma barra mais fina e colorida, use "
         "<code>=SPARKLINE(B2; {\"charttype\";\"bar\"})</code>."),
        ("Confira a proporção", "Necropsia (32) deve exibir a barra mais longa; Papiloscopia (11), a "
         "mais curta, com cerca de um terço do comprimento."),
    ]) +
    callout("note", "Sem gráfico, a leitura continua visual",
        "As barras dentro da célula permitem comparação direta na própria planilha. Indicadas para "
        "bases lidas linha a linha e para relatórios que serão colados em e-mails.")
)

cad.section("visicalc", "Curiosidade: a origem da planilha eletrônica",
    p("Em <b>1979</b>, <b>Dan Bricklin</b> criou o <b>VisiCalc</b>, a primeira planilha eletrônica da "
      "história, que impulsionou a venda do Apple II no mundo.") +
    grid2([
        ("O momento zero",
         "Antes do VisiCalc, um único erro em uma célula de papel exigia recalcular toda a planilha "
         "manualmente, o que consumia horas de trabalho."),
        ("Impacto na gestão pericial",
         "Se, no <code>requisicoes_periciais.csv</code>, o prazo institucional mudar de 30 para 45 "
         "dias, basta editar uma célula em Parametros e a planilha reclassifica os 120 laudos no "
         "mesmo instante. O que consumia horas em 1978 passou a levar um milissegundo."),
    ]) +
    ficha("g", "A linhagem",
        "A lógica criada por Dan Bricklin está presente em cada <code>=SOMA()</code> digitada hoje no "
        "Excel, no Google Sheets e em qualquer ferramenta de planilha.")
)

cad.section("fechamento-manha", "Fechamento da manhã: da bancada ao painel",
    p("Em quatro horas, passamos dos fundamentos às ferramentas que transformam uma planilha em um "
      "sistema de monitoramento pericial. Todo o trabalho ocorre no Google Sheets, sobre os quatro "
      "datasets do dia. Antes de seguir, fixe os três blocos da manhã.") +
    flow_h([
        ("\U0001f522", "Medir"),
        ("\u2699\ufe0f", "Decidir"),
        ("\U0001f7e2", "Alertar"),
        ("\U0001f4ca", "Painel"),
    ]) +
    grid2([
        ("1. Medir (SOMA, MÉDIA, CONT.NÚM)",
         "Produção do laboratório e volume de insumos: <code>produtividade_peritos.csv</code> e "
         "<code>movimentacao_reagentes.csv</code>. Sem medição, não há gestão."),
        ("2. Decidir (SE, SOMASE, CONT.SE)",
         "Lógica condicional que classifica o prazo, isola o custo por setor e conta o backlog, com "
         "<code>requisicoes_periciais.csv</code>."),
        ("3. Alertar (Formatação condicional)",
         "O semáforo do TAT e as barras dentro da célula convertem números em um painel visual de "
         "alertas."),
        ("Próximo passo (tarde)",
         "Estruturar essas planilhas (referências travadas, tabela, filtros) para que não se rompam "
         "quando o volume de dados aumentar."),
    ]) +
    ficha("a", "O que você já sabe fazer",
        "Ao fim da manhã, você consegue medir a produção, isolar o custo de cada setor, contar o "
        "backlog por status e pintar os atrasos automaticamente, tudo no Sheets. Falta definir a "
        "estrutura, e é o que vem agora.")
)


# =================================================================
# PARTE 2 - ESTRUTURA
# =================================================================
cad.grp("Parte 2 · Módulo 3 — Referências, tabelas e filtros",
        "Estruturar a planilha para que ela permaneça funcional quando o volume de dados crescer.")

cad.section("referencias", "Referências de células",
    p("Entender como o <b>Google Sheets</b> interpreta referências de células é fundamental para "
      "criar fórmulas que funcionam ao serem copiadas e que não geram <b>erros silenciosos</b> nos "
      "relatórios. A coluna <code>dias_uteis</code> do <code>requisicoes_periciais.csv</code> serve "
      "de exemplo.") +
    tbl(["Tipo", "Como se escreve", "Comportamento", "Quando usar"],
        [["<b>Relativa</b>", "<code>I2</code>",
          "Muda quando a fórmula é copiada para outra célula.",
          "Calcular o prazo linha a linha: <code>=I2-$B$1</code> vira <code>=I3-$B$1</code>."],
         ["<b>Absoluta</b>", "<code>$B$1</code>",
          "Não muda ao copiar. Trava linha e coluna.",
          "Parâmetros que se repetem (meta de TAT, taxa, preço): <code>=I2-$B$1</code>."],
         ["<b>Mista</b>", "<code>$A1</code> ou <code>A$1</code>",
          "Trava apenas a linha ou apenas a coluna.",
          "Matrizes de cruzamento (Tipo de Exame x Mês)."]],
        num_cols=[]) +
    code("""
        // GOOGLE SHEETS — coluna J "Dias_vs_Meta" (meta em Parametros!B1 = 30).
        // I = dias_uteis.

        // Relativa (muda ao copiar para baixo):
        =I2 - Parametros!B1     -> copiada vira =I3 - Parametros!B1

        // Com a meta travada (correto para arrastar):
        =I2 - Parametros!$B$1   -> copiada continua =I3 - Parametros!$B$1

        // Sem o cifrão, ao copiar, o Sheets desloca a referência da meta junto com a linha e
        // passa a capturar valores errados ou vazios.
        """, "sheets") +
    step([
        ("Crie a aba Parametros", "<kbd>+</kbd> na base das abas para criar uma folha "
         "<code>Parametros</code>; em B1 digite <code>30</code> (meta de TAT em dias)."),
        ("Escreva na primeira linha", "Na aba Laudos, em J2, digite <code>=I2-Parametros!B1</code>."),
        ("Trave a referência", "Com o cursor sobre <code>B1</code>, pressione <kbd>F4</kbd> até virar "
         "<code>$B$1</code> (no Mac: <kbd>Fn</kbd>+<kbd>F4</kbd>)."),
        ("Arraste para baixo", "Dobre o canto inferior direito de J2 e arraste até J121. A meta "
         "permanece fixa em B1 e apenas a linha muda."),
        ("Confira uma linha do meio", "Clique em J50: a fórmula deve terminar em "
         "<code>-Parametros!$B$1</code>, e não em <code>-Parametros!B49</code>."),
    ]) +
    callout("err", "Parâmetro fixo sem travar",
        "Esquecer o <code>$</code> em um parâmetro fixo faz a referência descer ao copiar para 500 "
        "linhas e capturar valores errados. Aplique <kbd>F4</kbd> em todo parâmetro.")
)

cad.section("guia-f4", "Guia do F4: os quatro modos de referência",
    p("O <b>F4</b> alterna o tipo de referência durante a edição de uma fórmula e também funciona no "
      "Google Sheets (no Mac, use <kbd>Fn</kbd>+<kbd>F4</kbd>). O atalho percorre os quatro modos em "
      "sequência e evita o parâmetro solto que causou o prejuízo de 30% do orçamento no caso real.") +
    step([
        ("Entre na edição da célula", "Clique na célula e pressione <kbd>F2</kbd> (ou dê um duplo "
         "clique) para editar a fórmula no lugar."),
        ("Posicione o cursor", "Deixe o cursor dentro ou após a referência <code>B1</code> que você "
         "quer travar."),
        ("F4 — primeira vez", "Vira <code>$B$1</code> (absoluta: trava linha e coluna)."),
        ("F4 — segunda vez", "Vira <code>B$1</code> (mista: trava somente a linha)."),
        ("F4 — terceira vez", "Vira <code>$B1</code> (mista: trava somente a coluna)."),
        ("F4 — quarta vez", "Volta para <code>B1</code> (relativa). O ciclo se repete."),
        ("Teste a cópia", "Arraste a fórmula para células vizinhas e observe o que muda e o que "
         "permanece travado."),
    ]) +
    tbl(["Modo", "Como aparece", "Trava", "Uso típico POLITEC"],
        [["Relativa", "<code>B1</code>", "Nada", "Cálculo linha a linha (dias_uteis - meta)."],
         ["Absoluta", "<code>$B$1</code>", "Linha e coluna", "Parâmetros: meta de TAT, taxa, preço."],
         ["Mista (linha)", "<code>B$1</code>", "Somente a linha", "Matriz: fixa o mês no topo."],
         ["Mista (coluna)", "<code>$B1</code>", "Somente a coluna", "Matriz: fixa o tipo de exame."]],
        num_cols=[]) +
    callout("tip", "No Google Sheets o F4 também funciona",
        "Ao editar uma fórmula, <kbd>F4</kbd> alterna relativa/absoluta (Mac: <kbd>Fn</kbd>+<kbd>F4</kbd>; "
        "ChromeOS: <kbd>Search</kbd>+<kbd>4</kbd>). Se o atalho não responder, digite o "
        "<code>$</code> antes da letra, do número ou de ambos.")
)

cad.section("referencia-mista", "Referência mista e o atalho F4",
    p("A referência mista (<code>$A1</code> ou <code>A$1</code>) trava <b>apenas</b> a linha ou "
      "apenas a coluna. É o recurso usado nas <b>matrizes de cruzamento</b>. A seguir, cruzamos "
      "<b>Tipo de Exame</b> (linhas) com <b>Setor</b> (colunas) do "
      "<code>requisicoes_periciais.csv</code>.") +
    grid2([
        ("Quando usar",
         "Matrizes que cruzam duas dimensões. Cada célula precisa referenciar a linha do seu critério "
         "e a coluna do outro, sem que os dois se movam juntos. Exemplo: Tipo de Exame (Necropsia, "
         "DNA, Tox…) x Setor (Patologia, Genética, Toxicologia…)."),
        ("Atalho: F4",
         "Pressione <kbd>F4</kbd> enquanto edita a fórmula para percorrer os quatro modos: "
         "<code>A1</code> \u2192 <code>$A$1</code> \u2192 <code>A$1</code> \u2192 <code>$A1</code>."),
    ]) +
    code("""
        // GOOGLE SHEETS — matriz Tipo de Exame (linhas) x Setor (colunas).
        // Base: requisicoes_periciais.csv. D = tipo_exame, E = setor.
        // Monte o cabeçalho: A2:A6 = tipos, B1:F1 = setores.

        // Na célula B2 da matriz:
        =CONT.SES($D$2:$D$121; $A2; $E$2:$E$121; B$1)

        // $A2  -> a coluna do critério-linha fica travada; a linha anda ao copiar para baixo.
        // B$1  -> a linha do cabeçalho fica travada; a coluna anda ao copiar para a direita.
        // A matriz inteira se preenche sem que nenhuma referência se desloque.
        """, "sheets") +
    step([
        ("Monte os rótulos", "Liste os tipos de exame em A2:A6 (Necropsia, Balística, Toxicologia, "
         "DNA, Papiloscopia) e os setores em B1:F1."),
        ("Escreva a fórmula em B2", "Use <b>referências mistas</b> nos intervalos de critério e nos "
         "critérios de linha e coluna."),
        ("Copie para a direita", "Arraste B2 até F2: apenas o setor (B$1) muda para C$1, D$1…"),
        ("Copie para baixo", "Selecione B2:F2 e arraste até a linha 6: apenas o tipo ($A2) muda para "
         "$A3, $A4…"),
        ("Confira uma célula", "A célula Necropsia x Patologia deve reproduzir a contagem de "
         "<code>=CONT.SES(D2:D121;\"Necropsia\";E2:E121;\"Patologia\")</code>."),
    ]) +
    aplicab(
        "Ao montar uma matriz de cruzamento (tipo x setor, tipo x mês, perito x exame).",
        "A fórmula precisa avançar na vertical e permanecer travada na horizontal, e vice-versa.",
        "A matriz Tipo x Setor sobre os 120 registros: a fórmula é escrita em B2 e arrastada para a "
        "grade inteira.") +
    callout("tip", "F4 no Google Sheets",
        "Durante a edição, <kbd>F4</kbd> também percorre os cifrões no Sheets. Se preferir, digite "
        "<code>$</code> antes da letra, do número ou de ambos.")
)

cad.section("referencias-abas-nomes", "Referências entre abas, intervalos nomeados e tabelas",
    p("As fórmulas podem referenciar outras abas. Referenciar outra aba, nomear intervalos e "
      "converter a base em <b>Tabela</b> tornam a planilha legível e evitam parâmetros escondidos no "
      "meio dos dados.") +
    tbl(["Recurso", "Sintaxe (Google Sheets)", "Vantagem"],
        [["<b>Referência a outra aba</b>", "<code>=Parametros!B1</code>",
          "Separa metas e preços da base, conforme a arquitetura de abas."],
         ["<b>Aba com espaço no nome</b>", "<code>='Base de Dados'!B1</code>",
          "Funciona, mas o nome entre apóstrofos é mais frágil. Prefira <code>Parametros</code>."],
         ["<b>Intervalo nomeado</b>", "<code>=Meta_TAT</code>",
          "Em vez de <code>Parametros!$B$1</code>, usa-se um nome, o que reduz a leitura de cifrões."],
         ["<b>Nome de Tabela</b>", "<code>=TabelaLaudos[dias_uteis]</code>",
          "Aponta para a coluna inteira sem depender do tamanho da base."]],
        num_cols=[]) +
    step([
        ("Crie a aba Parametros", "<kbd>+</kbd> na barra de abas para criar uma folha com apenas as "
         "metas (Meta_TAT = 30 em B1), separada da base."),
        ("Selecione a célula", "Clique em <code>Parametros!B1</code>, que contém a meta de TAT."),
        ("Abra os intervalos nomeados", "<kbd>Dados</kbd> \u2192 <kbd>Intervalos nomeados</kbd> \u2192 "
         "<i>Adicionar um intervalo</i>."),
        ("Defina o nome", "Nome: <code>Meta_TAT</code>; intervalo: <code>Parametros!$B$1</code>. Nomes "
         "não podem ter espaços nem acentos."),
        ("Converta a base em Tabela", "Selecione a base \u2192 <kbd>Formatar</kbd> \u2192 "
         "<kbd>Converter em tabela</kbd> e nomeie como <code>TabelaLaudos</code>."),
        ("Use nas fórmulas", "<code>=CONT.SE(TabelaLaudos[dias_uteis];\"&lt;=\"&amp;Meta_TAT)</code> "
         "dispensa cifrões e não exige contar linhas."),
    ]) +
    callout("err", "Nome com espaço ou acento",
        "Nomes de intervalo com espaço exigem colchetes e quebram em outras ferramentas. Use "
        "<code>_</code> e evite acentos: <code>Meta_TAT</code>, em vez de 'Meta TAT'.")
)

cad.section("caso-taxa", "Caso real: o erro de referência que custou milhões",
    p("Um laboratório de análises clínicas calculou o orçamento anual de reagentes em uma planilha. "
      "O analista esqueceu de travar a célula da <b>Taxa de Importação</b> com referência absoluta. "
      "O mesmo cenário pode ser reproduzido no <code>orcamento_setores.csv</code>.") +
    step([
        ("O erro técnico", "A fórmula sem cifrão foi copiada para as 36 linhas de orçamento. A taxa "
                           "de importação desceu pelas linhas e passou a capturar valores aleatórios "
                           "ou zerados de outras células."),
        ("A consequência", "O orçamento foi aprovado com um <b>déficit de 30%</b>. O laboratório "
                           "ficou sem reagentes no meio do ano fiscal, o que comprometeu as análises."),
        ("A lição para a POLITEC", "Use <kbd>F4</kbd> para travar células de parâmetros fixos: preços "
                           "de reagentes, metas de TAT e taxas de conversão."),
    ]) +
    antesdepois(
        "<code>=(orcado - realizado)/orcado</code> sem travar a coluna, copiada e desalinhada em cada linha.",
        "<code>=D2/Parametros!$B$1</code> com o parâmetro travado em uma célula absoluta.",
        "Parâmetro solto", "Parâmetro travado ($)") +
    ficha("r", "A conta do prejuízo",
        "Um cifrão ausente (<code>$</code>) gerou um prejuízo de 30% do orçamento anual. No "
        "<code>orcamento_setores.csv</code>, o orçado total é R$ 2.277.060 e o realizado, "
        "R$ 1.893.191 (83% de execução). Nenhuma fórmula estava incorreta; apenas solta. Esse erro "
        "não aparece na tela e só se revela na apuração final.")
)

cad.section("aplic-orcamento-reagentes", "Aplicação prática: orçamento de reagentes com parâmetros travados",
    p("Objetivo: montar o orçamento anual do <code>orcamento_setores.csv</code> (36 linhas = 6 "
      "laboratórios x 6 rubricas) de modo que nenhum parâmetro se desloque ao ser copiado. Os "
      "parâmetros fixos ficam na aba <code>Parametros</code> e são sempre travados.") +
    code("""
        // GOOGLE SHEETS — estrutura do orcamento_setores.csv:
        // A laboratorio | B rubrica | C orcado | D realizado
        // Nova coluna E: % de execução.

        // Aba Parametros:
        //   B1 = Tolerância de alerta (%)  -> nome: Tolerancia   (ex.: 0,85 = 85%)
        //   B2 = Fator de correção         -> nome: Fator        (ex.: 1,00)

        // Aba Orcamento, coluna E (% de execução), com o parâmetro TRAVADO:
        =D2*Fator/Parametros!$B$1

        // Sem nomes, forma clássica (equivalente):
        =D2*Parametros!$B$2/Parametros!$B$1

        // Como a tolerância está travada em $B$1, arrastar para baixo não desloca a referência.
        """, "sheets") +
    step([
        ("Importe o dataset", "<kbd>Arquivo</kbd> \u2192 <kbd>Importar</kbd> \u2192 "
         "<kbd>Fazer upload</kbd> e carregue <code>orcamento_setores.csv</code>, escolhendo "
         "<i>Inserir novas folhas</i>. Renomeie para <code>Orcamento</code>."),
        ("Separe a aba Parametros", "<kbd>+</kbd> para criar a folha <code>Parametros</code> com "
         "tolerância, fator e taxa; não insira parâmetros no meio da base."),
        ("Nomeie os parâmetros", "<kbd>Dados</kbd> \u2192 <kbd>Intervalos nomeados</kbd> \u2192 "
         "<code>Tolerancia</code> apontando para <code>Parametros!$B$1</code>."),
        ("Escreva a fórmula na primeira linha", "Em E2, combine realizado, fator e tolerância, com os "
         "parâmetros travados (<kbd>F4</kbd>)."),
        ("Confira a primeira linha", "Calcule o % de execução de Toxicologia/Reagentes: "
         "R$ 60.707 / R$ 91.810 = 66%. Confira o valor antes de arrastar."),
        ("Arraste para as 36 linhas", "Com o parâmetro travado, a fórmula copia corretamente de "
         "Balística a Toxicologia."),
        ("Simule variações", "Altere a tolerância em Parametros e observe o alerta do orçamento se "
         "ajustar de forma consistente."),
    ]) +
    aplicab(
        "Em orçamentos com parâmetros que se repetem (taxa, frete, imposto, meta).",
        "Um único parâmetro solto contamina centenas de linhas sem gerar aviso.",
        "Orçamento de reagentes por laboratório: a tolerância fica travada em "
        "<code>Parametros!$B$1</code> e vale para todas as rubricas.") +
    callout("err", "Parâmetro em linha fora do intervalo",
        "Se você travar <code>$B$1</code> e cortar a linha 1 ao selecionar o intervalo, a referência "
        "quebra. Deixe sempre uma margem ao redor da célula de parâmetro.")
)

cad.section("tabelas-estruturadas", "Tabelas: o fim das planilhas desorganizadas",
    p("No Google Sheets, um intervalo comum vira uma <b>Tabela</b> por <kbd>Formatar</kbd> \u2192 "
      "<kbd>Converter em tabela</kbd>. A tabela passa a ter comportamento de banco de dados: "
      "expansão automática, filtros no cabeçalho e <b>referências por nome de coluna</b>. No dataset "
      "<code>requisicoes_periciais.csv</code>, a <code>TabelaLaudos</code> terá 9 colunas.") +
    legenda([
        ("\u2795", "Expansão automática", "Ao colar 50 novas requisições no fim da tabela, fórmulas e "
         "formatação se estendem sozinhas, sem arrastar a alça."),
        ("\U0001f4d6", "Fórmulas legíveis", "Em vez de <code>=SOMASE(E2:E121;\"Toxicologia\";I2:I121)</code>, "
         "usa-se <code>=SOMASE(TabelaLaudos[setor];\"Toxicologia\";TabelaLaudos[dias_uteis])</code>."),
        ("\U0001f53d", "Filtros no cabeçalho", "As setas de filtro aparecem no cabeçalho de cada "
         "coluna sem configuração adicional."),
    ]) +
    step([
        ("Importe e selecione", "Após importar <code>requisicoes_periciais.csv</code>, selecione "
         "qualquer célula do corpo da base (ou o intervalo A1:I121)."),
        ("Converta em tabela", "<kbd>Formatar</kbd> \u2192 <kbd>Converter em tabela</kbd>. O Sheets "
         "reconhece o cabeçalho e sugere um nome."),
        ("Nomeie a tabela", "Clique no nome sugerido e renomeie para <code>TabelaLaudos</code>. Esse "
         "nome será usado nas fórmulas."),
        ("Aplique as fórmulas", "Reescreva os indicadores com nomes de coluna: "
         "<code>=CONT.SE(TabelaLaudos[status];\"Pendente\")</code>."),
        ("Teste a expansão", "Cole uma linha nova logo abaixo da última e observe o intervalo da "
         "tabela se estender sozinho."),
    ]) +
    callout("err", "Nem tudo aceita referência de tabela no Sheets",
        "No Google Sheets, as <b>referências de tabela não funcionam</b> dentro de formatação "
        "condicional, gráficos e tabelas dinâmicas. Nesses casos, use o intervalo normal (por "
        "exemplo, <code>E2:E121</code>) ou um Intervalo Nomeado. Também não mescle células dentro de "
        "uma tabela.")
)

cad.section("tabela-estruturada-detalhe", "Tabela em detalhe: referências por nome de coluna",
    p("A Tabela dispensa a contagem de linhas: as fórmulas passam a usar o nome da coluna, como a "
      "coluna <code>setor</code> da <code>TabelaLaudos</code>.") +
    tbl(["Notação", "Significado", "Exemplo"],
        [["<code>TabelaLaudos[setor]</code>", "A <b>coluna inteira</b> setor.",
          "Vai de E2 até o fim, mesmo que a base dobre."],
         ["<code>TabelaLaudos[[#TOTALS];[dias_uteis]]</code>", "Linha de totais da tabela (se ativa).",
          "Total calculado sem fórmula separada."],
         ["<code>TabelaLaudos[#ALL]</code>", "Tabela inteira (cabeçalho + dados).",
          "Uso pouco frequente em fórmulas."],
         ["<code>TabelaLaudos[#HEADERS]</code>", "Apenas a linha de cabeçalho.",
          "Uso em validação de estrutura."]],
        num_cols=[]) +
    code("""
        // NÃO use referências de células fixas dentro da tabela:
        =SOMASE(E2:E121; "Toxicologia"; I2:I121)    // quebra se a base crescer

        // USE nomes de coluna (Sheets e Excel):
        =SOMASE(TabelaLaudos[setor]; "Toxicologia"; TabelaLaudos[dias_uteis])

        // Coluna calculada linha a linha: digite na primeira linha da coluna.
        // O Sheets preenche a coluna inteira da tabela automaticamente:
        =H2 - B2      // data_laudo - data_recebimento, na primeira linha de dados
        """, "sheets") +
    step([
        ("Escreva o nome da coluna", "Dentro da tabela, digite <code>=SOMA(TabelaLaudos[</code> e o "
         "Sheets exibe a lista de colunas. Selecione com as setas e confirme com <kbd>Tab</kbd>."),
        ("Confira o alvo", "A referência <code>TabelaLaudos[dias_uteis]</code> equivale a "
         "<code>I2:I121</code> hoje e a I150 se a base crescer."),
        ("Teste a coluna calculada", "Na primeira célula vazia à direita, digite <code>=H2-B2</code>: "
         "a fórmula desce por toda a coluna da tabela."),
        ("Evite referências fixas", "Troque qualquer <code>I2:I121</code> antigo pelo nome de coluna "
         "para manter a fórmula válida quando a base crescer."),
    ]) +
    callout("tip", "Digite o nome e o Sheets ajuda",
        "Ao digitar <code>TabelaLaudos[</code>, o Sheets lista as colunas disponíveis. Selecione e "
        "confirme com <kbd>Tab</kbd>; não é necessário decorar nomes nem contar linhas.")
)


cad.section("tabela-bi", "A tabela como ponte para o BI",
    p("A planilha de controle de laudos estruturada hoje será o <b>mesmo arquivo</b> que alimentará o "
      "Power BI no Dia 4, sem retrabalho e sem perda de dados. O nome de coluna criado agora será o "
      "nome do campo no painel.") +
    ficha("p", "A frase que orienta a transição",
        "Antes de modelar dados em um sistema de BI, eles precisam ser estruturados. Tabelas são a "
        "ponte entre a planilha amadora e o banco de dados profissional. — <b>Ralph Kimball</b>, "
        "pai do Data Warehouse dimensional.") +
    flow_h([
        ("\U0001f4c4", "Base bruta"),
        ("\U0001f4d0", "Tabela"),
        ("\U0001f4ca", "Indicadores"),
        ("\U0001f4c8", "Power BI"),
    ]) +
    callout("tip", "Prepare hoje, colha no Dia 4",
        "Se a base estiver em Tabela, com colunas nomeadas e sem células mescladas, a importação no "
        "Power BI é quase automática (o <code>requisicoes_periciais.csv</code> já vem limpo). O "
        "trabalho de hoje é o modelo de amanhã.")
)

cad.section("filtros", "Filtros: selecionando linhas por critério",
    p("O filtro reduz uma base volumosa a uma resposta objetiva, o que agiliza a leitura dos dados na "
      "gestão pericial. No <b>Google Sheets</b>, o filtro é criado em <kbd>Dados</kbd> \u2192 "
      "<kbd>Criar um filtro</kbd>.") +
    tbl(["Tipo de filtro", "Como acionar (Sheets)", "Uso na POLITEC"],
        [["<b>Por valores</b>", "Ícone de filtro no cabeçalho \u2192 desmarque o que não deve aparecer.",
          "Isolar requisições de uma delegacia específica com status Pendente."],
         ["<b>Por condição</b>", "Ícone do filtro \u2192 <i>Filtrar por condição</i> \u2192 "
          "<i>O texto contém</i> / <i>É maior que</i>.",
          "Ver apenas os laudos com TAT acima de 60 dias."],
         ["<b>Por cor</b>", "Ícone do filtro \u2192 <i>Filtrar por cor</i> \u2192 <i>Cor de preenchimento</i>.",
          "Ver apenas os laudos com <b>Atraso Crítico</b>, cor gerada pelo semáforo do TAT."]],
        num_cols=[]) +
    step([
        ("Ative o filtro", "Selecione a base \u2192 <kbd>Dados</kbd> \u2192 <kbd>Criar um filtro</kbd>. "
         "Surgem ícones de filtro em cada cabeçalho da linha 1."),
        ("Abra a coluna", "Clique no ícone de filtro da coluna que será isolada (por exemplo, G "
         "status)."),
        ("Defina o critério", "Desmarque todos e marque apenas <b>Pendente</b>, ou use <i>Filtrar por "
         "condição</i> para uma regra."),
        ("Leia o resultado", "O Sheets exibe, na parte inferior do ícone, quantos valores (linhas) "
         "permaneceram."),
        ("Remova ao terminar", "<kbd>Dados</kbd> \u2192 <kbd>Remover filtro</kbd>."),
    ]) +
    callout("err", "Filtrar e esquecer de limpar",
        "Um filtro esquecido no arquivo faz o relatório seguinte somar poucos laudos, embora a base "
        "esteja completa. Antes de salvar ou compartilhar, volte a <kbd>Dados</kbd> \u2192 "
        "<kbd>Remover filtro</kbd>.")
)

cad.section("filtros-avancados", "Filtros avançados: condição, cor e os maiores valores",
    p("O filtro por valores apenas esconde linhas. O <b>filtro por condição</b> responde perguntas de "
      "gestão: quais laudos estão entre 31 e 60 dias? quais vieram de uma delegacia específica? o que "
      "está com atraso crítico?") +
    tbl(["Filtro", "Como fazer (Sheets)", "Pergunta que responde"],
        [["<b>Intervalo / entre</b>", "<i>Filtrar por condição</i> \u2192 <i>Está entre</i> 31 e 60.",
          "Quantos laudos estão na faixa de atenção (amarelo)?"],
         ["<b>Contém / começa com</b>", "<i>Filtrar por condição</i> \u2192 <i>O texto contém</i>.",
          "Quais requisições vieram de uma delegacia específica?"],
         ["<b>Maiores valores</b>", "O filtro não tem '10 maiores': use <i>Classificar intervalo</i> "
          "Z\u2192A ou a fórmula <code>=MAIOR(intervalo; n)</code>.",
          "Quais exames tiveram o maior TAT no período?"],
         ["<b>Por cor</b>", "<i>Filtrar por cor</i> \u2192 <i>Cor de preenchimento</i> \u2192 Vermelho.",
          "Quais laudos estão em atraso crítico (do semáforo)?"],
         ["<b>Vários níveis</b>", "Filtre primeiro por Setor e depois por Status.",
          "Quantos laudos de DNA estão pendentes no setor Genética?"]],
        num_cols=[]) +
    code("""
        // GOOGLE SHEETS — filtrar a base requisicoes_periciais.csv na tela.
        // 1. Dados > Criar um filtro.
        // 2. Coluna G (status): Filtrar por valores > apenas "Pendente".
        // 3. Coluna I (dias_uteis): Filtrar por condição > "É maior que" > 60.
        // Resultado: apenas os laudos pendentes há mais de 60 dias.

        // Para os maiores valores, sem filtro:
        =MAIOR(Laudos!I2:I121; 1)     // maior TAT da base

        // Contagem do que sobrou no filtro, por fórmula (independe do filtro na tela):
        =CONT.SES(Laudos!G2:G121;"Pendente"; Laudos!I2:I121;">60")
        """, "sheets") +
    step([
        ("Ative os filtros", "<kbd>Dados</kbd> \u2192 <kbd>Criar um filtro</kbd> na base (ou na "
         "TabelaLaudos)."),
        ("Filtre o status", "No ícone da coluna G, marque apenas <b>Pendente</b>."),
        ("Aplique a condição numérica", "No ícone da coluna I, <i>Filtrar por condição</i> \u2192 "
         "<i>É maior que</i> \u2192 <b>60</b>."),
        ("Combine os filtros", "Os dois filtros atuam juntos: pendentes E com mais de 60 dias."),
        ("Confira pela fórmula", "Use <code>=CONT.SES(...)</code> para conferir a contagem "
         "independentemente do filtro na tela."),
    ]) +
    callout("tip", "Um filtro de cor por vez",
        "O Sheets filtra por <b>uma</b> cor de preenchimento por vez, sem combinar vermelho e "
        "amarelo. Para isolar os vermelhos do semáforo do TAT, use <i>Filtrar por cor</i> \u2192 "
        "<i>Cor de preenchimento</i> \u2192 Vermelho.")
)

cad.section("fantasma-heilbronn", "O Fantasma de Heilbronn: como ordenar revelou a origem",
    p("Entre 2007 e 2009, a polícia de vários países europeus encontrou o mesmo DNA feminino em cenas "
      "de crime distintas — um homicídio na Áustria, um roubo na França e outros casos na Alemanha. A "
      "imprensa adotou o termo <b>O Fantasma de Heilbronn</b>.") +
    step([
        ("A investigação", "Centenas de investigadores foram mobilizados. A suposta autora foi "
                           "incluída na lista de procurados da Europa, com recompensa de "
                           "<b>300 mil euros</b>."),
        ("A virada pelos dados", "Um analista exportou a base de todos os casos, <b>ordenou pelo "
                                 "número do lote do swab de algodão</b> e filtrou os resultados. "
                                 "Todos os casos positivos correspondiam ao mesmo lote de swabs."),
        ("A conclusão", "O DNA atribuído à autora era de uma <b>operária austríaca</b> "
                        "que fabricava os cotonetes usados pela polícia, sem luvas, anos antes."),
    ]) +
    p("O mesmo raciocínio se aplica ao dataset <code>movimentacao_reagentes.csv</code>: ao suspeitar de "
      "contaminação, ordenar por fornecedor e filtrar por um reagente mostra se as ocorrências se "
      "concentram em um único lote ou fornecedor.") +
    code("""
        // GOOGLE SHEETS — movimentacao_reagentes.csv
        // Colunas: A id | B data | C reagente | D tipo | E quantidade | F setor | G fornecedor

        // Ordene a base pelo fornecedor e depois filtre um reagente sob suspeita:
        // Dados > Classificar intervalo > Classificar por: G (fornecedor) > A a Z

        // Quantas entradas um fornecedor trouxe de um reagente específico:
        =CONT.SES(F2:F81; "Genetica"; G2:G81; "ChemLab Brasil")
        """, "sheets") +
    ficha("r", "A lição",
        "Ordenar e filtrar não é burocracia. É o procedimento que separa uma investigação bem "
        "conduzida de um erro de origem. A contaminação estava no dado de entrada, o lote de swabs e "
        "o reagente, não na análise de DNA.")
)

cad.section("ordenacao", "Ordenação: definindo a prioridade da fila",
    p("Ordenar define quem é atendido primeiro e quais casos chegam ao topo da fila. No Sheets, a "
      "ordenação fica em <kbd>Dados</kbd> \u2192 <kbd>Classificar intervalo</kbd>.") +
    grid2([
        ("Ordenação por uma coluna",
         "Crescente (A\u2192Z) ou decrescente (Z\u2192A) por uma coluna. <b>Aplicação:</b> ordenar a "
         "fila por <code>data_recebimento</code> coloca os casos mais antigos no topo, o que direciona "
         "o trabalho do mais atrasado ao mais recente."),
        ("Ordenação por prioridade",
         "Ordem que não é alfabética nem numérica. <b>Aplicação na POLITEC:</b> ordenar por gravidade "
         "do crime, independente da data de entrada. Como o Sheets não disponibiliza lista "
         "personalizada em todas as versões, usa-se uma <b>coluna auxiliar de prioridade</b> (1, 2, 3)."),
    ]) +
    tbl(["Nível", "Prioridade", "Tipos de crime"],
        [["\U0001f534 1", "Máxima", "Homicídio / Crime Sexual"],
         ["\U0001f7e0 2", "Alta", "Roubo / Tráfico de Drogas"],
         ["\U0001f7e1 3", "Padrão", "Furto / Demais crimes"]],
        num_cols=[]) +
    code("""
        // GOOGLE SHEETS — coluna auxiliar de prioridade.
        // Suponha o tipo de crime na coluna D. Crie a coluna K "Prioridade":

        =SES(D2="Homicidio";1; D2="Crime Sexual";1; D2="Roubo";2; D2="Trafico de Drogas";2;
             VERDADEIRO;3)

        // Depois: Dados > Classificar intervalo >
        //   Classificar por: K (Prioridade) > A a Z  (1 primeiro)
        //   Adicionar outra coluna: B (data_recebimento) > A a Z (mais antigos primeiro)
        """, "sheets") +
    step([
        ("Crie a coluna Prioridade", "Na primeira coluna vazia à direita, digite <code>Prioridade</code> "
         "e a fórmula <code>SES</code> que converte o tipo de crime em 1, 2 ou 3."),
        ("Copie para toda a base", "Arraste a fórmula até a última linha (ou deixe a Tabela expandir a "
         "coluna)."),
        ("Classifique", "<kbd>Dados</kbd> \u2192 <kbd>Classificar intervalo</kbd> \u2192 <i>Classificar "
         "por</i> Prioridade \u2192 <i>A a Z</i>."),
        ("Adicione o desempate", "Clique em <i>Adicionar outra coluna de classificação</i> \u2192 "
         "<code>data_recebimento</code> \u2192 <i>A a Z</i> (mais antigos primeiro)."),
        ("Confira o topo", "As primeiras linhas devem ser homicídios e crimes sexuais mais antigos, a "
         "fila que a gestão ataca primeiro."),
    ]) +
    callout("note", "Google Sheets e a ordem personalizada",
        "Algumas versões do Sheets oferecem <i>Ordem de classificação personalizada</i>; se a sua não "
        "tiver, a coluna auxiliar de prioridade funciona em qualquer versão e deixa a regra explícita "
        "na planilha.")
)

cad.section("aplic-fila-laudos-criticos", "Aplicação prática: a fila de laudos críticos para a reunião das 8h",
    p("Objetivo: montar, em menos de 10 segundos, a lista de laudos críticos que serão cobrados na "
      "reunião das 8h, usando o <code>requisicoes_periciais.csv</code> e priorizando gravidade do "
      "crime e antiguidade do processo.") +
    step([
        ("Parta da TabelaLaudos", "A base está importada e convertida em Tabela "
         "(<kbd>Formatar</kbd> \u2192 <kbd>Converter em tabela</kbd>)."),
        ("Aplique o semáforo", "A coluna <code>dias_uteis</code> (I) está pintada em verde, amarelo e "
         "vermelho."),
        ("Filtre por cor vermelha", "Ícone do filtro na coluna I \u2192 <i>Filtrar por cor</i> \u2192 "
         "<i>Cor de preenchimento</i> \u2192 Vermelho. Permanecem apenas os atrasos críticos."),
        ("Ordene pela prioridade", "Classifique primeiro pela coluna auxiliar <code>Prioridade</code> "
         "(1 = homicídio/crime sexual)."),
        ("Desempate por data", "Dentro de cada prioridade, ordene por <code>data_recebimento</code> "
         "crescente, dos mais antigos para os mais recentes."),
        ("Leve a lista", "Copie as linhas filtradas para a pauta da reunião ou imprima."),
    ]) +
    flow_h([
        ("\u2328\ufe0f", "Converter em tabela"),
        ("\U0001f534", "Filtrar vermelho"),
        ("\U0001f522", "Ordenar prioridade"),
        ("\u2705", "Lista 8h"),
    ]) +
    callout("err", "Esquecer de limpar o filtro antes de salvar",
        "Se o arquivo for salvo com o filtro vermelho ativo, quem abrir depois verá apenas parte da "
        "base. Volte a <kbd>Dados</kbd> \u2192 <kbd>Remover filtro</kbd> antes de arquivar.")
)

cad.section("combinacao", "Combinando as técnicas: o fluxo da reunião das 8h",
    p("A combinação de <b>Tabela</b>, <b>formatação condicional</b>, <b>filtro por cor</b> e "
      "<b>ordenação por prioridade</b> produz, em poucos cliques, a lista da reunião das 8h no Google "
      "Sheets.") +
    flow_h([
        ("\u2328\ufe0f", "Converter em tabela"),
        ("\U0001f534", "Filtrar vermelho"),
        ("\U0001f522", "Ordenar prioridade"),
        ("\u2705", "Lista 8h"),
    ]) +
    step([
        ("Converta em tabela", "<kbd>Formatar</kbd> \u2192 <kbd>Converter em tabela</kbd> para a base "
         "ganhar filtros e expansão automática."),
        ("Filtre o vermelho", "Mostre apenas os atrasos críticos, na cor vermelha do semáforo do TAT."),
        ("Ordene por prioridade", "Classifique pela coluna auxiliar de prioridade, com homicídios "
         "primeiro."),
        ("Obtenha a lista", "Em menos de 10 segundos, a lista pronta para a reunião das 8h."),
    ]) +
    ficha("g", "O resultado",
        "Em <b>menos de 10 segundos</b>, o Diretor da POLITEC obtém a lista de laudos críticos a "
        "cobrar na reunião das 8h, com três cliques e sem intervenção manual adicional.")
)


cad.section("aplic-consolidacao-planilhas", "Aplicação prática: consolidação de várias planilhas (prévia do Power Query)",
    p("Objetivo: reunir as planilhas de cada setor em <b>uma base consolidada</b>, sem copiar e colar "
      "linha por linha. O exercício reproduz o ETL que o Power Query fará no Dia 3, usando o "
      "<code>requisicoes_periciais.csv</code>, que contém os cinco setores (Patologia, Toxicologia, "
      "Identificação, Balística, Genética).") +
    step([
        ("Padronize os cabeçalhos", "Todas as planilhas devem ter as mesmas colunas: "
         "<code>id_requisicao, data_recebimento, delegacia_origem, tipo_exame, setor, "
         "perito_responsavel, status, data_laudo, dias_uteis</code>."),
        ("Exporte em CSV UTF-8", "Exporte cada planilha de setor no mesmo formato e codificação "
         "(UTF-8). No Sheets, <kbd>Arquivo</kbd> \u2192 <kbd>Fazer download</kbd> \u2192 "
         "<i>Valores separados por vírgula (.csv)</i>."),
        ("Empilhe as bases", "Cole as linhas de todos os setores na aba <code>Base</code>, uma abaixo "
         "da outra, mantendo a ordem das colunas."),
        ("Adicione a coluna de origem", "Crie uma coluna <code>Arquivo_Origem</code> com o nome do "
         "setor, para rastreabilidade."),
        ("Converta em tabela", "<kbd>Formatar</kbd> \u2192 <kbd>Converter em tabela</kbd> e nomeie "
         "<code>TabelaConsolidada</code>."),
        ("Valide por CONT.SE", "Compare <code>=CONT.SE(TabelaConsolidada[setor];\"Genetica\")</code> "
         "com o total original do setor. Os números devem coincidir."),
    ]) +
    code("""
        // GOOGLE SHEETS — validação da consolidação (total por setor deve bater com cada origem)
        =CONT.SE(TabelaConsolidada[setor]; "Patologia")      // esperado: 32
        =CONT.SE(TabelaConsolidada[setor]; "Toxicologia")    // esperado: 28
        =CONT.SE(TabelaConsolidada[setor]; "Identificacao")  // esperado: 21
        =CONT.SE(TabelaConsolidada[setor]; "Balistica")      // esperado: 20
        =CONT.SE(TabelaConsolidada[setor]; "Genetica")       // esperado: 19

        // Total geral (deve fechar em 120):
        =CONT.VALORES(TabelaConsolidada[id_requisicao])
        """, "sheets") +
    callout("err", "Copiar e colar de várias abas mistura colunas",
        "Se as planilhas de setor tiverem ordem de colunas diferente, o empilhamento desalinha os "
        "dados. Padronize os cabeçalhos <b>antes</b> de juntar. No Dia 3, o Power Query (e a função "
        "<code>IMPORTRANGE</code> do Sheets) faz esse ajuste automaticamente.")
)

cad.section("subtotais-dinamicas", "Tabela dinâmica e subtotais: o primeiro passo da análise",
    p("Antes do Power BI, a própria planilha responde perguntas de agrupamento. No Google Sheets, a "
      "<b>Tabela dinâmica</b> (<kbd>Inserir</kbd> \u2192 <kbd>Tabela dinâmica</kbd>) cumpre o papel do "
      "assistente de subtotais do Excel e não altera o dado bruto.") +
    tbl(["Recurso", "O que faz", "Quando usar"],
        [["<b>Subtotais por fórmula</b>", "SOMASE/CONT.SE por grupo (setor, tipo).",
          "Valor de painel que precisa atualizar sozinho."],
         ["<b>Tabela dinâmica</b>", "Agrupa e cruza dados por arrastar campos.",
          "Explorar produção por setor x tipo sem refazer fórmulas."],
         ["<b>Filtros da dinâmica</b>", "Botão de filtro ligado à tabela dinâmica.",
          "Painel interativo dentro da planilha."]],
        num_cols=[]) +
    step([
        ("Prepare a base", "A base precisa de cabeçalhos limpos. No Sheets não é necessário ordenar "
         "antes, ao contrário do assistente de subtotais do Excel."),
        ("Insira a dinâmica", "<kbd>Inserir</kbd> \u2192 <kbd>Tabela dinâmica</kbd> \u2192 escolha "
         "<i>Intervalo existente</i> e a seleção da base."),
        ("Monte linhas e valores", "Arraste <code>setor</code> para <i>Linhas</i> e "
         "<code>dias_uteis</code> para <i>Valores</i> (resumo <b>MÉDIA</b>)."),
        ("Cruze dimensões", "Arraste <code>tipo_exame</code> para <i>Colunas</i> para ver a matriz "
         "setor x exame."),
        ("Entenda a diferença", "As fórmulas de subtotal ficam na aba do painel; a dinâmica fica em "
         "outra aba e não altera o dado bruto."),
    ]) +
    callout("tip", "Dinâmica x fórmula",
        "Para um número que precisa atualizar sozinho em um painel, prefira <code>CONT.SES</code> e "
        "<code>SOMASES</code>. Para exploração ad-hoc (ver o TAT médio por setor no momento), a "
        "Tabela dinâmica atende.")
)

cad.section("colunas-medidas", "Colunas calculadas x medidas: preparando o vocabulário do BI",
    p("A estruturação da base hoje prepara o Dia 4. Duas palavras que reaparecem no Power BI podem "
      "ser entendidas na planilha: <b>coluna calculada</b> e <b>medida</b>.") +
    grid2([
        ("Coluna calculada (linha a linha)",
         "Um valor por <b>linha</b>. Exemplo no Sheets: <code>=H2-B2</code> (data_laudo menos "
         "data_recebimento). É o mesmo papel da coluna <code>dias_uteis</code> que já existe no "
         "dataset."),
        ("Medida (agregação)",
         "Um valor que resume <b>muitas linhas</b>. Exemplo: <code>=MÉDIA(Laudos!I2:I121)</code>. É o "
         "número que a direção consulta no cartão do painel."),
    ]) +
    tbl(["Pergunta", "Resposta", "Tipo"],
        [["Qual o TAT desta requisição?", "dias_uteis (já existe na base).", "Por linha"],
         ["Qual o TAT médio do laboratório?", "MÉDIA(dias_uteis).", "Agregada"],
         ["Quantas requisições por setor?", "CONT.SE(setor; \"Toxicologia\").", "Agregada"],
         ["Esta requisição está em atraso?", "SE(dias_uteis>60; \"Crítico\"; \"OK\").", "Por linha"]],
        num_cols=[]) +
    callout("note", "Por que isso importa agora",
        "No Power BI, colunas calculadas e medidas se comportam de forma diferente e a escolha afeta "
        "o desempenho. Entender a distinção ainda no Sheets reduz o esforço da transição do Dia 4.")
)

cad.section("limite-excel", "Quando a planilha chega ao seu limite",
    p("O Google Sheets suporta até <b>10 milhões de células</b> por arquivo (o Excel, até 1.048.576 "
      "linhas), o que cobre a maior parte das operações periciais. O limite que importa, porém, é "
      "prático.") +
    grid2([
        ("O limite prático na POLITEC",
         "Acima de algumas dezenas de milhares de linhas com fórmulas condicionais (SOMASES, SE "
         "aninhados, formatação condicional extensa), o Sheets fica lento e cada recálculo demora. "
         "Funções voláteis como <code>HOJE()</code> agravam esse efeito."),
        ("A hora de migrar",
         "Quando a base de requisições se aproximar de <b>50.000 linhas</b>, a análise deve migrar para "
         "ferramentas mais robustas."),
    ]) +
    tbl(["Ponto de virada", "Ferramenta", "Para que serve"],
        [["Transformação pesada", "<b>Power Query</b> (no Excel)",
          "Limpeza e transformação de dados grandes."],
         ["Análise e visualização", "<b>Power BI</b>",
          "Painéis interativos para a liderança (Dia 4)."],
         ["Grandes volumes multiusuário", "<b>Banco de dados relacional</b>",
          "Gestão com muitos usuários simultâneos."]],
        num_cols=[]) +
    callout("tip", "Regra de bolso",
        "A planilha atende até dezenas de milhares de linhas. Acima disso, ela continua servindo como "
        "<b>entrada</b>, mas a análise deve ir para o Power Query ou o Power BI. Os datasets do curso "
        "(120, 80, 218 e 36 linhas) são pequenos de propósito.")
)

cad.section("checklist-migracao-bi", "Checklist de migração da planilha para o BI",
    p("Antes de levar a base da POLITEC para o Power BI (Dia 4), passe por este checklist. Cada item "
      "marcado evita um erro de importação.") +
    checklist([
        "Base em <b>Tabela</b>, com nome definido (<code>TabelaLaudos</code>).",
        "Cabeçalhos curtos, sem espaços nem acentos (<code>dias_uteis</code>).",
        "Datas no formato <b>numérico</b> (alinhadas à direita).",
        "Nenhuma célula mesclada nem linha de total no meio da base.",
        "Sem linhas de Total Geral ou rodapés exportados pelo sistema legado.",
        "Arquivo salvo/exportado como <b>CSV UTF-8</b> ou .xlsx com uma única aba de base.",
        "Colunas calculadas criadas (dias_uteis, mes).",
        "Contagens validadas por <code>CONT.SE</code> contra a origem (120 requisições).",
    ]) +
    flow_h([
        ("\U0001f9f9", "Base limpa"),
        ("\U0001f4d0", "Tabela"),
        ("\U0001f4c4", "CSV UTF-8"),
        ("\U0001f4c8", "Power BI"),
    ]) +
    callout("err", "Linha de Total Geral no CSV",
        "Sistemas legados exportam uma linha de total no fim. Se ela chegar ao BI, vira uma categoria "
        "fantasma e distorce as somas. Delete antes de carregar.")
)

cad.section("fechamento-tarde", "Fechamento da tarde: da planilha ao banco de dados",
    p("A tarde tratou da <b>estrutura</b>: referências travadas, tabela, filtros e ordenação por "
      "prioridade, tudo no Google Sheets. Em conjunto, essas técnicas transformam a planilha em um "
      "<b>banco de dados</b>.") +
    grid2([
        ("O que aprendemos",
         ul(["Referências relativas, absolutas e mistas (F4)",
             "Tabela com nomes de coluna (Converter em tabela)",
             "Filtros por valores, condição e cor",
             "Ordenação por prioridade com coluna auxiliar",
             "Consolidação de várias planilhas e validação"])),
        ("Por que importa",
         ul(["A planilha permanece funcional ao crescer",
             "As fórmulas ficam legíveis e auditáveis",
             "Os parâmetros deixam de se deslocar",
             "A base de hoje vira a fonte do BI amanhã",
             "A fila de laudos vira decisão em 10 segundos"])),
    ]) +
    ficha("g", "O saldo do dia",
        "Pela manhã, o foco foi <b>medir e decidir</b>. À tarde, <b>estruturar</b> para que a medição "
        "não se rompa. É a ponte que o Dia 3 atravessa com validação e visualização.")
)


# =================================================================
# PARTE 3 - PRATICA
# =================================================================
cad.grp("Parte 3 · Prática guiada",
        "Sete laboratórios que constroem, do zero, o painel de gestão de laudos.")

cad.section("lab1", "Lab 1 — Estruturar a base no Google Sheets",
    p("Objetivo: a partir do dataset <code>requisicoes_periciais.csv</code>, criar a <b>Tabela</b> que "
      "servirá de base para todos os cálculos do painel de gestão, no Google Sheets.") +
    step([
        ("Importe o CSV", "No Google Sheets: <kbd>Arquivo</kbd> \u2192 <kbd>Importar</kbd> \u2192 "
         "<kbd>Fazer upload</kbd>. Selecione <code>requisicoes_periciais.csv</code>."),
        ("Escolha onde inserir", "Na janela de importação, em <i>Local de importação</i>, escolha "
         "<i>Inserir novas folhas</i> (ou <i>Substituir planilha</i> se estiver começando do zero)."),
        ("Confirme o separador", "O Sheets detecta o ponto e vírgula. Se os dados vierem em uma única "
         "coluna, refaça a importação marcando <i>Separador: ponto e vírgula</i>."),
        ("Verifique as colunas", "O dataset tem: A id_requisicao, B data_recebimento, C "
         "delegacia_origem, D tipo_exame, E setor, F perito_responsavel, G status, H data_laudo, "
         "I dias_uteis."),
        ("Renomeie a folha", "Clique no nome da aba e renomeie para <code>Laudos</code>."),
        ("Confira o formato das datas", "As colunas B e H devem estar alinhadas à direita (numérico). "
         "Se estiverem à esquerda, são texto; corrija com <code>=DATA.VALOR(B2)</code>."),
        ("Converta em tabela", "Selecione qualquer célula da base \u2192 <kbd>Formatar</kbd> \u2192 "
         "<kbd>Converter em tabela</kbd> \u2192 nomeie <code>TabelaLaudos</code>."),
        ("Teste a expansão", "Cole duas linhas novas abaixo da última e observe o intervalo da tabela "
         "se estender sozinho."),
    ]) +
    callout("err", "Antes de tudo: sem células mescladas",
        "Cabeçalhos mesclados ou linhas vazias no meio impedem a criação da tabela. Desmescle "
        "(<kbd>Formatar</kbd> \u2192 <kbd>Mesclar</kbd> \u2192 <i>Desfazer mesclagem</i>) e preencha "
        "as lacunas antes de continuar.")
)

cad.section("lab2", "Lab 2 — Verificar o TAT com SE e HOJE",
    p("Objetivo: no dataset <code>requisicoes_periciais.csv</code>, a coluna <code>dias_uteis</code> "
      "já existe para laudos concluídos. Vamos criar uma coluna que indique se o laudo pendente está "
      "em atraso, comparando <code>data_recebimento</code> com <code>HOJE()</code>.") +
    code("""
        // GOOGLE SHEETS — nova coluna J "Status_Prazo" na Laudos.
        // B = data_recebimento | H = data_laudo | J2:

        =SE($H2=""; "Em andamento";
            SE(HOJE()-$B2>60; "ATRASO CRITICO";
               SE(HOJE()-$B2>30; "Atencao"; "No prazo")))
        """, "sheets") +
    step([
        ("Crie a nova coluna", "Na célula J1, digite <code>Status_Prazo</code>."),
        ("Escreva a fórmula em J2", "Use <code>SE</code> aninhado: primeiro verifica se "
         "<code>data_laudo</code> está vazia (laudo pendente)."),
        ("Arraste para toda a base", "Dobre o canto de J2 e arraste até J121."),
        ("Leia o resultado", "Laudos sem data_laudo aparecem como <b>Em andamento</b>; os concluídos "
         "são classificados pelos dias desde o recebimento."),
        ("Confira uma linha", "Na REQ-2025-0002 (status Pendente), verifique se <code>HOJE()-B</code> "
         "ultrapassa 60 e retorna ATRASO CRITICO."),
    ]) +
    callout("tip", "HOJE() atualiza a cada abertura",
        "<code>=HOJE()</code> se atualiza sempre que a planilha é aberta, e a coluna de espera cresce "
        "sem intervenção. Como é uma função volátil, deixa planilhas grandes mais lentas.")
)

cad.section("lab3", "Lab 3 — Aplicar o semáforo do TAT",
    p("Objetivo: pintar a coluna <code>Status_Prazo</code> da <code>TabelaLaudos</code> em verde, "
      "amarelo e vermelho, com regras no Google Sheets.") +
    step([
        ("Selecione a coluna", "Selecione J2:J121 (sem o cabeçalho)."),
        ("Abra a formatação condicional", "<kbd>Formatar</kbd> \u2192 <kbd>Formatação condicional</kbd>."),
        ("Regra 1 (vermelho)", "<i>Formatar células se</i> \u2192 <i>O texto contém</i> \u2192 digite "
         "<b>CRITICO</b> \u2192 preenchimento vermelho claro."),
        ("Regra 2 (amarelo)", "<i>Adicionar outra regra</i> \u2192 texto contém <b>Atencao</b> \u2192 "
         "preenchimento amarelo claro."),
        ("Regra 3 (verde)", "<i>Adicionar outra regra</i> \u2192 texto contém <b>No prazo</b> \u2192 "
         "preenchimento verde claro."),
        ("Atenção à ordem", "Deixe a regra do vermelho no topo. No Sheets, a regra de cima prevalece "
         "quando mais de uma é atendida."),
    ]) +
    checklist([
        "Status contendo \"CRITICO\" ficam vermelhos.",
        "Status contendo \"Atencao\" ficam amarelos.",
        "Status contendo \"No prazo\" ficam verdes.",
        "O filtro por cor (Filtrar por cor) mostra apenas os vermelhos.",
    ])
)

cad.section("lab4", "Lab 4 — Criar os indicadores com referências absolutas",
    p("Objetivo: montar a aba de indicadores sobre a <code>TabelaLaudos</code> (dataset "
      "<code>requisicoes_periciais.csv</code>), com referências absolutas nos parâmetros.") +
    code("""
        // GOOGLE SHEETS — aba "Parametros":
        Meta_TAT     = 30     (célula $B$1)   // dias úteis aceitáveis
        Meta_Diaria  = 5      (célula $B$2)   // laudos/dia

        // Aba "Painel" (sobre TabelaLaudos):
        Total requisições    = CONT.VALORES(TabelaLaudos[id_requisicao])   // 120
        Backlog pendente     = CONT.SE(TabelaLaudos[status]; "Pendente")   // 28
        TAT médio geral      = MÉDIA(TabelaLaudos[dias_uteis])
        TAT mediano          = MED(TabelaLaudos[dias_uteis])
        Laudos por setor     = CONT.SE(TabelaLaudos[setor]; "Toxicologia") // 28
        % dentro da meta     = CONT.SE(TabelaLaudos[dias_uteis]; "<="&Parametros!$B$1)
                               / CONT.NÚM(TabelaLaudos[dias_uteis])
        """, "sheets") +
    step([
        ("Separe a aba Parametros", "<kbd>+</kbd> para criar a folha <code>Parametros</code> com "
         "Meta_TAT = 30 em B1 e Meta_Diaria = 5 em B2."),
        ("Trave as referências", "Em toda fórmula que usa parâmetro, deixe o cursor sobre a célula e "
         "pressione <kbd>F4</kbd> até virar <code>Parametros!$B$1</code>."),
        ("Valide por amostra", "Filtre a base manualmente por status = Pendente e confira se o "
         "<code>CONT.SE(...)</code> retorna o mesmo total (28)."),
        ("Formate", "TAT em dias (0 decimal); % dentro da meta com 1 casa decimal."),
    ]) +
    callout("err", "Parâmetro na mesma aba dos dados",
        "Não insira parâmetros junto à base. Se a base crescer e a tabela se expandir, a célula do "
        "parâmetro pode ser deslocada e a fórmula quebra. A aba separada evita esse problema.")
)

cad.section("lab5", "Lab 5 — Filtros e ordenação por prioridade (painel do diretor)",
    p("Objetivo: reproduzir, em 10 segundos, a lista de laudos críticos para a reunião das 8h, usando "
      "a <code>TabelaLaudos</code> (dataset <code>requisicoes_periciais.csv</code>).") +
    step([
        ("Crie a prioridade", "Adicione a coluna K <code>Prioridade</code> com a fórmula "
         "<code>SES</code> que converte o tipo de exame/crime em 1, 2 ou 3."),
        ("Ative o filtro", "<kbd>Dados</kbd> \u2192 <kbd>Criar um filtro</kbd>."),
        ("Filtre os críticos", "Na coluna J (Status_Prazo), use <i>Filtrar por cor</i> \u2192 "
         "<i>Cor de preenchimento</i> \u2192 Vermelho."),
        ("Ordene por prioridade", "<kbd>Dados</kbd> \u2192 <kbd>Classificar intervalo</kbd> \u2192 "
         "Prioridade (A a Z), depois data_recebimento (A a Z)."),
        ("Leve a lista", "Copie as linhas visíveis para a pauta da reunião."),
    ]) +
    ficha("g", "Resultado esperado",
        "Uma lista curta, priorizada por gravidade e antiguidade, com apenas os casos em atraso "
        "crítico. Não há macro nem código envolvido.")
)

cad.section("painel-backlog", "Lab integrador — o painel de backlog completo",
    p("Ao final do Dia 2, o participante deve construir o painel de gestão de laudos da POLITEC/MT no "
      "Google Sheets, combinando as técnicas do dia sobre o dataset "
      "<code>requisicoes_periciais.csv</code>.") +
    step([
        ("Estruturar a base", "Importe <code>requisicoes_periciais.csv</code> e converta em tabela "
         "(<kbd>Formatar</kbd> \u2192 <kbd>Converter em tabela</kbd>) com o nome "
         "<code>TabelaLaudos</code>."),
        ("Criar Status_Prazo",
         "<code>=SE($H2=\"\";\"Em andamento\";SE(HOJE()-$B2>60;\"ATRASO CRITICO\";"
         "SE(HOJE()-$B2>30;\"Atencao\";\"No prazo\")))</code>"),
        ("Aplicar o semáforo", "<kbd>Formatar</kbd> \u2192 <kbd>Formatação condicional</kbd> na coluna "
         "Status_Prazo: No prazo (verde) / Atencao (amarelo) / ATRASO CRITICO (vermelho), com a regra "
         "vermelha no topo."),
        ("Criar os indicadores", "Em aba separada: <code>CONT.SE</code> para backlog pendente, "
         "<code>MÉDIA</code> para TAT médio, <code>CONT.SE</code> por setor, com referências absolutas "
         "nos parâmetros."),
        ("Montar o painel", "KPIs no topo (backlog, TAT médio, % no prazo) e a "
         "<code>TabelaLaudos</code> filtravel logo abaixo."),
        ("Filtrar e ordenar", "Aplique o filtro por cor (vermelho = ATRASO CRITICO) para gerar a fila "
         "de prioridades da reunião das 8h."),
    ]) +
    kpi([("=CONT.SE", "Backlog"), ("=MÉDIA", "TAT médio"), ("=CONT.SE", "Req/setor"), ("Semáforo", "TAT")]) +
    callout("tip", "Entregável do dia",
        "Guarde este arquivo: no Dia 4 ele será a <b>fonte do Power BI</b>. Exporte como CSV UTF-8 "
        "(<kbd>Arquivo</kbd> \u2192 <kbd>Fazer download</kbd>) ou mantenha o Sheets como fonte; a "
        "convenção de versionamento está na governança.")
)

cad.section("lab6-auditoria-base", "Lab 6 — Auditoria de base suja (limpeza)",
    p("Objetivo: aplicar o roteiro de limpeza ao dataset <code>requisicoes_periciais.csv</code>, "
      "simulando os defeitos comuns em bases exportadas de sistemas legados, no Google Sheets.") +
    step([
        ("Duplique a folha", "Clique com o botão direito na aba <code>Laudos</code> \u2192 "
         "<kbd>Duplicar</kbd>. Renomeie a cópia para <code>Base_Limpa</code> e mantenha a original "
         "como <code>Base_Bruta</code>."),
        ("Verifique as datas", "Confirme que B e H estão alinhadas à direita (numérico). Se estiverem "
         "à esquerda, corrija com <code>=DATA.VALOR(B2)</code>."),
        ("Limpe os textos", "<code>=ARRUMAR(C2)</code> remove espaços das bordas; "
         "<code>=MAIÚSCULA(ARRUMAR(C2))</code> padroniza a capitalização das delegacias."),
        ("Verifique duplicatas", "Em uma coluna auxiliar: <code>=CONT.SE($A$2:$A$121; A2)</code>. "
         "Valores maiores que 1 indicam requisição duplicada."),
        ("Fixe o resultado como valor", "Selecione as colunas limpas, copie e use "
         "<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd> \u2192 <i>Somente valores</i>."),
        ("Remova duplicatas", "<kbd>Dados</kbd> \u2192 <kbd>Limpeza de dados</kbd> \u2192 "
         "<kbd>Remover duplicatas</kbd>, marcando a coluna <code>id_requisicao</code>."),
        ("Valide as contagens", "Compare <code>=CONT.VALORES(A2:A121)</code> antes e depois da "
         "limpeza e registre quantas linhas foram alteradas."),
        ("Converta em tabela", "<kbd>Formatar</kbd> \u2192 <kbd>Converter em tabela</kbd> e nomeie "
         "<code>TabelaLaudos</code>."),
    ]) +
    code("""
        // GOOGLE SHEETS — verificação de qualidade (colunas auxiliares na Base_Limpa):
        =ÉNÚM(B2)                       // FALSO = data em texto
        =ÉNÚM(H2)                       // FALSO = data em texto
        =ARRUMAR(C2)<>C2                // VERDADEIRO = espaço extra
        =CONT.SE($A$2:$A$121; A2)>1     // VERDADEIRO = duplicado

        // Resumo da auditoria (quantos defeitos de cada tipo):
        =CONT.SE(aux_verificacao; VERDADEIRO)
        """, "sheets") +
    callout("err", "Limpar sem antes duplicar a folha",
        "Não limpe a base original diretamente. Duplique a folha (<i>Base_Bruta</i> e "
        "<i>Base_Limpa</i>) para preservar o dado de entrada; a cadeia de custódia dos dados começa "
        "aqui.")
)

cad.section("lab7-consolidacao", "Lab 7 — Consolidando as planilhas dos setores",
    p("Objetivo: reunir as planilhas de setores em uma base consolidada, pronta para o painel, e "
      "validar que nenhum registro se perdeu. O <code>requisicoes_periciais.csv</code> contém todos os "
      "setores, o que permite conferir a soma no final.") +
    step([
        ("Reconheça os setores", "O dataset tem 5 setores: Patologia (32), Toxicologia (28), "
         "Identificação (21), Balística (20) e Genética (19), total 120."),
        ("Crie uma aba por setor", "Filtre por setor, copie as linhas e cole em abas "
         "<code>Setor_Patologia</code>, <code>Setor_Toxicologia</code> etc."),
        ("Adicione a coluna de origem", "Em cada aba, adicione a coluna <code>Setor_Origem</code> com "
         "o nome do setor."),
        ("Empilhe na aba Base", "Cole todas as linhas em uma única aba, uma abaixo da outra, sem "
         "repetir o cabeçalho."),
        ("Converta em tabela", "<kbd>Formatar</kbd> \u2192 <kbd>Converter em tabela</kbd>, nome "
         "<code>TabelaConsolidada</code>."),
        ("Valide por setor", "Conte com <code>=CONT.SE(Setor_Origem;\"Toxicologia\")</code> e compare "
         "com a contagem original da aba de Toxicologia (28)."),
    ]) +
    kpi([("5", "Setores consolidados"), ("1", "Base consolidada"),
         ("120", "Requisições somadas"), ("100%", "Validação por CONT.SE")]) +
    callout("tip", "Este é o embrião do ETL",
        "Padronizar, empilhar, adicionar origem e validar é exatamente o que o <b>Power Query</b> fará "
        "automaticamente no Dia 3/4. Hoje o passo é manual; depois, torna-se um clique em Atualizar.")
)


# =================================================================
# PARTE 4 - CENARIOS
# =================================================================
cad.grp("Parte 4 · Cenários e aplicações práticas",
        "Quatro casos completos da POLITEC: problema, indicadores, passos e desafio.")

cad.section("cenario-orcamento-reagentes", "Cenário A — O orçamento anual de reagentes",
    p("Problema: o laboratório precisa montar o orçamento do próximo ano fiscal com base no dataset "
      "<code>orcamento_setores.csv</code> (36 linhas: 6 laboratórios x 6 rubricas). O orçamento "
      "anterior estourou por um erro de referência.") +
    kpi([("36", "Linhas de orçamento"), ("6", "Rubricas por laboratório"),
         ("30%", "Estouro evitado com F4"), ("R$ 0", "Custo do erro corrigido na origem")]) +
    tbl(["Passo", "O que fazer", "Ferramenta (Sheets)"],
        [["1", "Criar a aba <code>Parametros</code> com meta de gasto e tolerância.", "Arquitetura de abas"],
         ["2", "Estruturar o CSV em Tabela.", "<kbd>Formatar</kbd> \u2192 Converter em tabela"],
         ["3", "Calcular o % de execução travando os parâmetros.", "F4 / Intervalo nomeado"],
         ["4", "Somar o realizado por laboratório com SOMASE.", "SOMASE / SOMASES"],
         ["5", "Comparar orçado e realizado em gráfico.", "Coluna calculada + gráfico"]],
        num_cols=[]) +
    step([
        ("Importe o dataset", "<kbd>Arquivo</kbd> \u2192 <kbd>Importar</kbd> e carregue "
         "<code>orcamento_setores.csv</code>: colunas laboratorio, rubrica, orcado, realizado."),
        ("Calcule o % de execução", "Nova coluna <code>Pct_Execucao</code>: <code>=D2/C2</code>. "
         "Formate como porcentagem."),
        ("Identifique estouro", "Formatação condicional: vermelho se &gt; 100%, amarelo se &gt; 85%."),
        ("Some por laboratório", "<code>=SOMASE(A:A; \"Genetica\"; D:D)</code> para o realizado."),
        ("Calcule o total geral", "<code>=SOMA(D2:D37)</code>, que deve resultar em R$ 1.893.191."),
    ]) +
    bar_chart(["Identificacao", "Quimica", "Genetica", "Patologia", "Toxicologia", "Balistica"],
              [374273, 369041, 343047, 340653, 276362, 189815],
              title="Realizado por laboratório (R$)",
              subtitulo="Dados de orcamento_setores.csv. Identificação e Química lideram o gasto realizado.",
              destaque=0) +
    ficha("p", "Desafio do cenário",
        "Crie uma coluna <code>Variacao</code> que calcule <code>=(D2-C2)/C2</code> e pinte com "
        "semáforo. Depois use <code>SOMASES</code> para somar apenas a rubrica "
        "<code>Reagentes</code> por laboratório e identificar o maior gasto nesse insumo.") +
    callout("err", "Parâmetro solto no orçamento", "Um cifrão ausente desloca o custo em centenas de "
        "itens. O orçamento estoura no fim do ano sem que o erro seja percebido durante o "
        "preenchimento.") +
    ficha("g", "O que este cenário ensina",
        "Orçamento consistente exige parâmetros centralizados, referências travadas e validação por "
        "setor. O mesmo padrão vale para qualquer planilha de custos da POLITEC.")
)

cad.section("cenario-fila-criticos", "Cenário B — A fila de laudos críticos para a reunião das 8h",
    p("Problema: o Diretor precisa, todas as manhãs às 8h, da lista dos laudos críticos priorizada por "
      "gravidade do crime e antiguidade. Hoje a equipe monta essa lista manualmente em 40 minutos.") +
    kpi([("40 min", "Tempo manual por dia"), ("10 s", "Tempo com a planilha"),
         ("3", "Faixas do semáforo"), ("3", "Cliques para a lista")]) +
    flow_h([
        ("\U0001f9f9", "Base limpa"),
        ("\U0001f534", "Filtro vermelho"),
        ("\U0001f522", "Ordenar prioridade"),
        ("\u2705", "Lista 8h"),
    ]) +
    step([
        ("Prepare a base", "<code>TabelaLaudos</code> com a coluna <code>Prioridade</code> (1 a 3) e o "
         "semáforo do TAT aplicado."),
        ("Aplique o semáforo", "TAT em verde, amarelo e vermelho pela formatação condicional."),
        ("Filtre por cor", "Ícone do filtro \u2192 <i>Filtrar por cor</i> \u2192 "
         "<i>Cor de preenchimento</i> \u2192 Vermelho."),
        ("Ordene", "<kbd>Dados</kbd> \u2192 <kbd>Classificar intervalo</kbd> por Prioridade e depois "
         "por <code>data_recebimento</code> (A a Z)."),
        ("Distribua", "Copie a lista para a pauta da reunião ou imprima."),
    ]) +
    tbl(["Prioridade", "Critério", "Ação na reunião"],
        [["\U0001f534 Crítico", "TAT &gt; 60 dias", "Cobrança imediata do setor responsável."],
         ["\U0001f7e0 Alto", "31 a 60 dias + crime grave", "Monitorar e redistribuir carga."],
         ["\U0001f7e1 Padrão", "No prazo", "Acompanhar o fluxo normal."]],
        num_cols=[]) +
    callout("err", "Ordenar só por data e ignorar a gravidade",
        "Se a fila for ordenada apenas por antiguidade, um homicídio recente pode ficar atrás de "
        "furtos antigos. A coluna auxiliar de prioridade corrige isso: a prioridade institucional "
        "prevalece sobre a data.") +
    ficha("a", "Desafio do cenário",
        "Automatize o envio: use a coluna <code>Status_Prazo</code> e um filtro para gerar, no início "
        "do dia, apenas os casos que <b>entraram</b> em atraso crítico desde ontem. Quem cruzou a "
        "linha das 8h é o foco da reunião.")
)

cad.section("cenario-produtividade-perito", "Cenário C — Painel de produtividade por perito",
    p("Problema: distribuir a carga de trabalho entre os peritos e detectar sobrecarga ou ociosidade. "
      "Hoje a avaliação é subjetiva. Usamos o dataset <code>produtividade_peritos.csv</code>, com 218 "
      "registros de 9 meses.") +
    bar_chart(["Silva, A. P.", "Souza, M. F.", "Almeida, C. R.", "Costa, J. L.",
                "Oliveira, R. S.", "Lima, P. H.", "Ferreira, T. A.", "Martins, K. B."],
              [312, 269, 282, 371, 300, 215, 325, 326],
              title="Total de laudos por perito (9 meses de 2025)",
              subtitulo="Meta acumulada = 315 laudos (35/mês x 9). Lima (215), Souza (269) e Almeida (282) estão abaixo; investigar.",
              destaque=5) +
    tbl(["Indicador", "Fórmula (Sheets)", "Leitura"],
        [["Laudos por perito", "<code>=SOMASE(B:B; \"Silva, A. P.\"; D:D)</code>", "Total acumulado do perito."],
         ["Média mensal", "<code>=SOMASE(...) / 9</code>", "Média de laudos por mês."],
         ["% da meta", "<code>=Total / 315</code>", "Atingimento do compromisso acumulado."],
         ["Ranking", "<code>=ORDEM(A2; intervalo)</code>", "Posição relativa entre os peritos."]],
        num_cols=[]) +
    step([
        ("Importe o dataset", "<kbd>Arquivo</kbd> \u2192 <kbd>Importar</kbd> e carregue "
         "<code>produtividade_peritos.csv</code> (colunas mes, perito, tipo_exame, laudos_concluidos)."),
        ("Converta em tabela", "<kbd>Formatar</kbd> \u2192 <kbd>Converter em tabela</kbd>: "
         "<code>TabelaProdutividade</code>."),
        ("Some por perito", "<code>=SOMASE(perito; \"Costa, J. L.\"; laudos_concluidos)</code> para "
         "cada um dos 8 peritos."),
        ("Calcule a meta acumulada", "Meta mensal = 35. Meta de 9 meses = 315 laudos."),
        ("Calcule o % de atingimento", "<code>=Total / 315</code>. Abaixo de 80% entra em zona de alerta."),
        ("Decida com dados", "Redistribua a carga com base nos números."),
    ]) +
    aplicab(
        "No fechamento mensal de produtividade da equipe pericial.",
        "A percepção de carga não mede o volume efetivo nem a complexidade dos casos.",
        "Lima entregou 215 laudos (68% da meta acumulada), o que pode indicar casos complexos ou "
        "afastamento. Apenas os dados indicam a causa.") +
    ficha("p", "Desafio do cenário",
        "Cruze produtividade e TAT: um perito que entrega muitos laudos, mas com TAT alto, pode estar "
        "cometendo erros por pressa. Use a média de <code>dias_uteis</code> por perito "
        "(<code>MÉDIA.SE</code> ou <code>SOMASE/CONT.SE</code>) para comparar.")
)

cad.section("cenario-auditoria-qualidade", "Cenário D — Auditoria de qualidade da base",
    p("Problema: antes de publicar o relatório gerencial, o gestor precisa garantir que a base não tem "
      "defeitos: células mescladas, datas como texto, duplicatas e valores fora de faixa.") +
    kpi([("4", "Tipos de defeito"), ("0", "Células mescladas aceitáveis"),
         ("100%", "Datas numéricas"), ("0", "Duplicatas pela chave")]) +
    tbl(["Defeito", "Como detectar (Sheets)", "Como corrigir"],
        [["<b>Células mescladas</b>", "<kbd>Formatar</kbd> \u2192 <kbd>Mesclar</kbd> mostra a mesclagem ativa.",
          "Desmesclar e preencher os rótulos."],
         ["<b>Datas como texto</b>", "Datas alinhadas à esquerda; <code>=ÉNÚM(...)</code> falso.",
          "Dividir texto em colunas ou <code>=DATA.VALOR()</code>."],
         ["<b>Duplicatas</b>", "<code>=CONT.SE(chave;chave)&gt;1</code> em coluna auxiliar.",
          "<kbd>Dados</kbd> \u2192 <kbd>Limpeza de dados</kbd> \u2192 Remover duplicatas."],
         ["<b>Valores fora de faixa</b>", "Formatação condicional em pesos e custos.",
          "Corrigir ou excluir o registro inválido."],
         ["<b>Espaços extras</b>", "<code>=ARRUMAR(célula)&lt;&gt;célula</code>.",
          "Aplicar <code>=ARRUMAR()</code> e colar como valores."]],
        num_cols=[]) +
    step([
        ("Detecte mesclagens", "Selecione a área de dados e verifique em <kbd>Formatar</kbd> \u2192 "
         "<kbd>Mesclar</kbd> se há mesclagem ativa; qualquer uma é um risco a filtros e fórmulas."),
        ("Valide as datas", "Coluna auxiliar <code>=ÉNÚM(B2)</code>: se retornar FALSO, a data é texto."),
        ("Encontre duplicatas", "Coluna auxiliar <code>=CONT.SE($A$2:$A$121; A2)&gt;1</code>."),
        ("Verifique as faixas", "Formatação condicional para custos negativos ou valores fora do "
         "intervalo esperado."),
        ("Documente", "Registre quantos defeitos foram encontrados e corrigidos para fins de auditoria."),
        ("Só então publique", "Uma base aprovada na auditoria gera um relatório confiável."),
    ]) +
    code("""
        // GOOGLE SHEETS — checklist de qualidade em colunas auxiliares:
        =ÉNÚM(B2)                       // FALSO = data em texto
        =CONT.SE($A$2:$A$121; A2)>1     // VERDADEIRO = duplicado
        =ARRUMAR(C2)<>C2                // VERDADEIRO = tem espaço extra
        =OU(E2<0; E2>10000)             // VERDADEIRO = valor suspeito

        // Resumo da auditoria:
        =CONT.SE(aux; VERDADEIRO)       // quantos defeitos de cada tipo
        """, "sheets") +
    callout("err", "Publicar sem auditoria",
        "Um relatório publicado com defeitos de estrutura compromete a credibilidade do dado. A "
        "auditoria de qualidade é tão necessária quanto o semáforo do TAT.") +
    ficha("r", "Desafio do cenário",
        "Crie uma <b>aba de auditoria</b> que some todos os defeitos por coluna e retorne um semáforo "
        "geral da base: verde (zero defeitos), amarelo (defeitos tratáveis) e vermelho (base "
        "contaminada). Ninguém publica sem o verde.")
)


# =================================================================
# PARTE 5 - BOAS PRATICAS E FECHAMENTO
# =================================================================
cad.grp("Parte 5 · Boas práticas, governança e fechamento",
        "Erros que contaminam relatórios, nomenclatura, governança, quiz, glossário e referências.")

cad.section("erros-comuns", "Erros comuns e como evitá-los",
    p("Os erros mais frequentes em planilhas periciais não são de fórmula, e sim de <b>estrutura</b>. "
      "Identificá-los antes evita que contaminem os relatórios gerenciais.") +
    grid2([
        ("\u274c Células mescladas",
         "Mesclar pode parecer organizado, mas quebra filtros, ordenações e fórmulas de contagem. Não "
         "mescle células em uma base de dados; use a mesclagem apenas em títulos."),
        ("\u274c Datas como texto",
         "Uma data importada como texto (alinhada à esquerda) faz o cálculo de TAT retornar erro. "
         "Verifique com <code>=ÉNÚM()</code> e corrija com <code>=DATA.VALOR()</code>."),
        ("\u274c Referência absoluta ausente",
         "Copiar fórmulas sem travar parâmetros (preço, prazo, taxa) causou o déficit de 30% do caso "
         "real. Use F4."),
        ("\u274c Dados misturados em uma coluna",
         "Escrever 'Toxicologia - 30 dias' em uma célula mistura tipo e prazo. Cada informação precisa "
         "de sua própria coluna."),
    ]) +
    ficha("r", "O princípio único",
        "Uma célula, um dado. Uma coluna, um tipo de informação. Um parâmetro, uma célula travada. "
        "Essas três regras evitam a maior parte dos erros de planilha.")
)

cad.section("nomenclatura", "Boas práticas de nomenclatura e arquitetura",
    p("Uma planilha organizada começa antes das fórmulas, na convenção de nomes e na arquitetura das "
      "abas. Estabeleça um padrão e documente-o.") +
    tbl(["Nomenclatura de colunas", "Arquitetura de abas"],
        [["Sem espaços: <code>data_recebimento</code>, não Data Recebimento.", "<b>Laudos</b> — dados brutos; não editar manualmente."],
         ["Minúsculas e sem acento nos cabeçalhos: <code>dias_uteis</code>.", "<b>Painel</b> — indicadores calculados e semáforos."],
         ["Descritivos e curtos: <code>dias_uteis</code>, <code>tipo_exame</code>, <code>status</code>.", "<b>Parametros</b> — metas, preços e taxas (com referências absolutas)."],
         ["Padronize a nomenclatura de categorias (por exemplo, sempre Arma de Fogo).", "<b>Historico</b> — dados de meses anteriores para comparação."]],
        num_cols=[]) +
    callout("note", "Por que padronizar categorias",
        "Conforme o Dia 1, padronizar 'Arma de Fogo' (em vez de Revólver, arma, rvl) pode aumentar em "
        "até <b>40%</b> a eficácia dos cruzamentos estatísticos.")
)

cad.section("sheets-excel", "Google Sheets x Excel na POLITEC",
    p("Neste curso, o trabalho ocorre no <b>Google Sheets</b>. As duas ferramentas suportam as funções "
      "do dia; a escolha depende do ambiente e da necessidade de colaboração da equipe.") +
    tbl(["Critério", "Google Sheets (o do curso)", "Excel"],
        [["Funções do dia", "Todas disponíveis (separador <kbd>;</kbd>)", "Todas disponíveis"],
         ["Colaboração simultânea", "Nativa — várias pessoas ao mesmo tempo", "Limitada (coautoria no 365)"],
         ["Permissões por e-mail", "Nativo, granular", "Via OneDrive/SharePoint"],
         ["Atalho F4 (cifrão)", "Funciona ao editar a fórmula (Mac: Fn+F4)", "Percorre os 4 modos"],
         ["Versionamento", "Histórico de versões automático", "Local, com nome de arquivo"],
         ["Dados sensíveis", "Compartilhamento e proteção de intervalos", "Senha de arquivo"]],
        num_cols=[]) +
    callout("tip", "Escolha pelo contexto",
        "Equipe distribuída e colaboração em tempo real: <b>Sheets</b>. Bases maiores, macros e "
        "integração com Power BI: <b>Excel</b>. Padronize uma ferramenta por base para evitar versões "
        "concorrentes.")
)

cad.section("governanca", "Governança: a planilha como documento oficial",
    p("No contexto da POLITEC/MT, a planilha de controle de laudos pode ser solicitada em auditorias, "
      "processos judiciais e prestações de contas ao <b>TCE-MT</b>. A qualidade dos dados tem o mesmo "
      "peso da qualidade técnica do laudo pericial.") +
    legenda([
        ("\U0001f5c2\ufe0f", "Versionamento", "Use o <b>Histórico de versões</b> do Sheets "
         "(<kbd>Arquivo</kbd> \u2192 <kbd>Histórico de versões</kbd>) ou exporte cópias mensais "
         "(<kbd>Arquivo</kbd> \u2192 <kbd>Fazer download</kbd>). Não sobrescreva a base histórica."),
        ("\U0001f512", "Controle de acesso", "Proteja as abas Laudos e Parametros em <kbd>Dados</kbd> "
         "\u2192 <kbd>Proteger planilhas e intervalos</kbd>. Permita edição apenas nas abas de entrada "
         "e compartilhe por e-mail com o nível adequado."),
        ("\U0001f4dd", "Auditabilidade", "O Sheets registra quem alterou, o que e quando. Mantenha "
         "também um registro na aba Historico. Dados periciais têm cadeia de custódia, inclusive os "
         "digitais."),
    ]) +
    ficha("p", "A frase do professor",
        "Uma planilha bem estruturada é a <b>cadeia de custódia dos seus dados</b>. Se a base está "
        "desorganizada, o laudo gerencial fica comprometido. — Prof. Renato Rosa.")
)

cad.section("atalhos", "Atalhos essenciais no Google Sheets",
    p("Dominar atalhos aumenta a velocidade de trabalho, o que importa no contexto pericial, em que os "
      "relatórios precisam ser gerados com rapidez. Aperte <kbd>Ctrl</kbd>+<kbd>/</kbd> no Sheets para "
      "ver a lista completa.") +
    tbl(["Atalho (Sheets)", "Ação"],
        [["<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>↓</kbd>", "Selecionar até o fim dos dados"],
         ["<kbd>F2</kbd>", "Editar a célula"],
         ["<kbd>F4</kbd>", "Alternar referência relativa/absoluta ($) ao editar"],
         ["<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd>", "Colar somente valores"],
         ["<kbd>Ctrl</kbd> + <kbd>;</kbd>", "Inserir a data de hoje (fixa)"],
         ["<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>:</kbd>", "Inserir a hora atual (fixa)"],
         ["<kbd>Ctrl</kbd> + <kbd>/</kbd>", "Mostrar todos os atalhos"],
         ["<kbd>Ctrl</kbd> + <kbd>Z</kbd>", "Desfazer"]],
        num_cols=[])
)

cad.section("checklist", "Checklist do gestor: planilha pericial",
    p("Antes de compartilhar qualquer planilha gerencial com a liderança da POLITEC/MT, verifique "
      "estes itens.") +
    checklist([
        "Dados organizados em Tabela (Converter em tabela).",
        "Parâmetros fixos travados com referência absoluta ($).",
        "Formatação condicional (semáforo do TAT) aplicada e funcionando.",
        "Fórmulas CONT.SE e SOMASE validadas com uma amostra dos dados.",
        "Coluna auxiliar de prioridade por gravidade de crime.",
        "Aba de Parametros separada da aba de dados.",
        "Nenhuma célula mesclada na área de dados.",
        "Datas verificadas como formato numérico (não texto).",
        "Contagens antes e depois conferidas na limpeza e na consolidação.",
        "Filtros removidos antes de salvar e compartilhar.",
    ]) +
    callout("tip", "Passe o checklist antes de enviar",
        "Dez itens marcados indicam que a planilha está pronta para circular. Qualquer item em branco "
        "é risco de retrabalho ou de dado contaminado no relatório.")
)

cad.section("quiz", "Quiz final do Dia 2 (15 perguntas)",
    q("Para somar o custo de reagentes <b>apenas</b> do setor de Toxicologia, a função correta é:",
      ["=SOMA(E2:E100)", "=SOMASE(C2:C100;\"Toxicologia\";E2:E100)",
       "=CONT.SE(C2:C100;\"Toxicologia\")", "=MÉDIA(E2:E100)"], 1,
      "SOMASE soma condicionalmente: o critério fica na coluna C e os valores, na coluna E.") +
    q("No Google Sheets, onde se converte um intervalo em uma Tabela?",
      ["Inserir > Gráfico", "Formatar > Converter em tabela",
       "Dados > Criar um filtro", "Ferramentas > Macros"], 1,
      "Formatar > Converter em tabela cria a Tabela, com filtros e referências por nome de coluna.") +
    q("A função CONT.NÚM() conta:",
      ["Qualquer célula preenchida", "Somente células com valores numéricos",
       "Apenas células vazias", "Somente texto"], 1,
      "Para contar datas e números válidos (por exemplo, laudos com TAT registrado), use CONT.NÚM.") +
    q("O atalho F4, durante a edição de uma fórmula, serve para:",
      ["Excluir a fórmula", "Alternar entre referência relativa e absoluta ($)",
       "Inserir uma função", "Formatar a célula"], 1,
      "No Sheets também: F4 alterna B1 -> $B$1 -> B$1 -> $B1. Trava parâmetros fixos.") +
    q("No semáforo do TAT, a cor vermelha corresponde a:",
      ["Até 30 dias", "Entre 31 e 60 dias", "Mais de 60 dias", "Laudo em andamento"], 2,
      "Mais de 60 dias indica atraso crítico e exige ação.") +
    q("Por que não se deve mesclar células em uma base de dados?",
      ["Deixa o arquivo mais pesado", "Quebra filtros, ordenações e contagens",
       "O Sheets proíbe em qualquer versão", "Impede o uso de cores"], 1,
      "A mesclagem compromete a estrutura tabular da base.") +
    q("O Fantasma de Heilbronn foi esclarecido porque o analista:",
      ["Contratou mais peritos", "Ordenou pelo lote do swab e filtrou os positivos",
       "Comprou um supercomputador", "Ignorou os outliers"], 1,
      "A contaminação estava no lote dos cotonetes, visível ao ordenar e filtrar a base.") +
    q("Uma Tabela permite escrever fórmulas:",
      ["Só com referências como D2:D121", "Com nomes de coluna, por exemplo TabelaLaudos[tipo_exame]",
       "Apenas com macros", "Sem nenhuma referência"], 1,
      "Os nomes de coluna tornam a fórmula legível e válida mesmo quando a base cresce.") +
    q("Quando a análise deve migrar para Power Query ou Power BI?",
      ["Sempre, mesmo com 100 linhas", "Quando a base se aproxima de 50.000 a 100.000 linhas",
       "Nunca; a planilha atende tudo", "Somente se não houver internet"], 1,
      "Acima desse volume, fórmulas e formatação condicional tornam a planilha lenta.") +
    q("A função MED() é mais adequada que MÉDIA() quando:",
      ["Não há números", "Existem casos extremos (outliers)",
       "A base tem só texto", "A coluna está vazia"], 1,
      "A mediana resiste a outliers; a média é influenciada por eles.") +
    q("Para contar exames de DNA que estão pendentes, usa-se:",
      ["CONT.SE(D:D;\"Pendente\")", "CONT.SES(G:G;\"Pendente\";D:D;\"DNA\")",
       "SOMASE(G:G;\"Pendente\";D:D)", "MÉDIA(D:D)"], 1,
      "São dois critérios simultâneos: status Pendente E tipo DNA, o que exige CONT.SES.") +
    q("A referência mista <code>$A1</code> trava:",
      ["A linha e a coluna", "Somente a coluna", "Somente a linha", "Nada"], 1,
      "$A1 trava a coluna A; a linha 1 permanece relativa.") +
    q("O erro <code>#VALOR!</code> normalmente indica:",
      ["Divisão por zero", "Tipo incompatível (por exemplo, subtrair data que é texto)",
       "Função digitada errada", "Referência a célula excluída"], 1,
      "Subtrair datas armazenadas como texto é a causa mais comum na POLITEC.") +
    q("No Sheets, filtrar por cor (do semáforo) funciona porque:",
      ["A tabela dinâmica pinta as células", "A formatação condicional pinta as células",
       "Um gráfico de barras cria as cores", "Uma macro aplica a cor"], 1,
      "O filtro por cor isola as cores criadas pela formatação condicional.") +
    q("Segundo a lição do módulo, dados periciais têm:",
      ["Apenas valor contábil", "Cadeia de custódia, inclusive os digitais",
       "Valor somente se numéricos", "Nenhuma exigência de auditoria"], 1,
      "A planilha de laudos é documento oficial e precisa ser auditável.")
)

cad.section("glossario", "Glossário pericial de planilhas",
    glossary([
        ("TAT — Turnaround Time", "Tempo entre o recebimento da requisição pericial e a entrega do laudo finalizado. Calculado com MÉDIA/mediana sobre a diferença entre datas."),
        ("Backlog", "Fila de exames aguardando processamento. Monitorado com CONT.SE(status;\"Pendente\")."),
        ("Mediana (MED)", "Valor central de uma fila ordenada. Resiste a outliers; reportada junto com a média."),
        ("Desvio padrão", "Medida de dispersão dos prazos. Indica a consistência operacional do laboratório."),
        ("Referência absoluta ($)", "Travamento de célula em fórmulas; impede que parâmetros fixos (preços, metas) se movam ao copiar. Atalho: F4."),
        ("Referência mista", "Trava apenas a linha ou apenas a coluna ($A1 ou A$1). Usada em matrizes de cruzamento."),
        ("Intervalo nomeado", "Intervalo batizado (por exemplo, Meta_TAT) via Dados > Intervalos nomeados; substitui referências cifradas."),
        ("Tabela", "Intervalo convertido em objeto de dados (Formatar > Converter em tabela): expansão automática, filtros nativos e referências por nome de coluna."),
        ("Referência de tabela", "Notação TabelaLaudos[dias_uteis], que aponta para a coluna inteira por nome, sem contar linhas."),
        ("Formatação condicional", "Cor automática conforme o valor ou uma fórmula. Base do semáforo do TAT."),
        ("CONT.SE / SOMASE", "Contagem e soma condicionais por um critério. CONT.SES/SOMASES combinam vários critérios."),
        ("SES", "Função que substitui o SE aninhado com pares condição/resultado. Sempre termina em VERDADEIRO; valor."),
        ("Semáforo do TAT", "Regra visual verde (<=30), amarelo (31 a 60) e vermelho (>60) aplicada à coluna de dias_uteis."),
        ("Ordenação por prioridade", "Ordem definida pelo gestor (por exemplo, gravidade do crime) via coluna auxiliar de prioridade."),
        ("Filtro por cor", "Filtro que isola as cores criadas pela formatação condicional; usado para localizar atrasos críticos."),
        ("Power Query", "Ferramenta de transformação e limpeza de dados, para volumes maiores e automação do ETL."),
        ("Coluna calculada x medida", "Coluna calculada: um valor por linha. Medida: um valor agregado que resume muitas linhas (prepara o vocabulário do Power BI)."),
        ("ETL", "Extract, Transform, Load — padrão de extração, limpeza e carga de dados que sustenta o BI."),
    ]) +
    tbl(["Indicador do dia", "Fórmula (Sheets)", "Significado"],
        [["Backlog pendente", "CONT.SE(...;\"Pendente\")", "Exames aguardando processamento."],
         ["TAT médio", "MÉDIA(dias_uteis)", "Tempo médio de emissão de laudo."],
         ["TAT mediano", "MED(dias_uteis)", "Tempo típico, sem influência de outliers."],
         ["Requisições por setor", "CONT.SE(setor; \"Toxicologia\")", "Volume isolado por laboratório."],
         ["% dentro da meta", "CONT.SE(<=meta)/CONT.NÚM", "Taxa de conformidade com o prazo."]],
        num_cols=[])
)

cad.section("referencias", "Referências e ponte para o Dia 3",
    p("As referências que sustentam o Dia 2:") +
    tbl(["Autor / Fonte", "Obra", "Por que consultar"],
        [["Ajuda do Google", "Suporte oficial do Google Sheets (pt-BR)",
          "Sintaxe e nomes das funções localizados. support.google.com/docs/table/25273."],
         ["Bill Jelen (MrExcel)", "Dezenas de livros de Excel avançado",
          "Referência em automação e gestão com planilhas. mrexcel.com."],
         ["Wayne Winston", "\"Microsoft Excel Data Analysis and Business Modeling\"",
          "Referência acadêmica sobre funções lógicas como sistemas de alerta."],
         ["Ralph Kimball", "Obras sobre modelagem dimensional e Data Warehouse",
          "Contexto da transição da planilha para o BI (Power BI, Dia 4)."]],
        num_cols=[]) +
    ficha("g", "Próximo passo — Dia 3",
        "O Dia 3 trata de <b>garantir que dados de qualidade entrem na planilha</b> e de comunicar os "
        "resultados visualmente: <b>validação de dados</b> (listas suspensas e regras de entrada), "
        "<b>mini-painéis</b> na própria planilha e <b>organização</b> da base mestra da POLITEC. A "
        "base estruturada hoje será usada nos próximos módulos.")
)

cad.build()

