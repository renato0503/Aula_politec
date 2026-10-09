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
        """, "excel") +
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
        """, "excel") +
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
        """, "excel") +
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
        """, "excel") +
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
        """, "excel") +
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
        """, "excel") +
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
        """, "excel") +
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
    p("Os dois resolvem o mesmo problema — varios niveis de decisao. A escolha e entre "
      "<b>compatibilidade</b> (SE aninhado, funciona em qualquer versao) e <b>legibilidade</b> "
      "(SES, mais limpo, mas so em versoes recentes).") +
    antesdepois(
        "<code>=SE(A2&gt;60;\"Critico\";SE(A2&gt;30;\"Atencao\";SE(A2&gt;15;\"Monitorar\";\"No prazo\")))</code><br>"
        "Quatro niveis aninhados: funciona em qualquer Excel, mas dificil de ler e de manter.",
        "<code>=SES(A2&gt;60;\"Critico\";A2&gt;30;\"Atencao\";A2&gt;15;\"Monitorar\";VERDADEIRO;\"No prazo\")</code><br>"
        "Par condicao/resultado em sequencia: cada faixa na sua linha, facil de auditar.",
        "SE aninhado (compatibilidade)", "SES (legibilidade)") +
    tbl(["Criterio", "SE aninhado", "SES"],
        [["Disponibilidade", "Qualquer versao do Excel e do Sheets", "Excel 2019+ / 365 e Sheets"],
         ["Legibilidade", "Cai rapido com 3+ niveis", "Alta — uma condicao por linha"],
         ["Manutencao", "Mexer no meio quebra a cadeia", "Inserir uma faixa e simples"],
         ["Limite pratico", "Ate ~3 niveis; acima, ilegivel", "Muitas faixas sem problema"],
         ["Caso de uso", "Compatibilidade com arquivos antigos", "Paineis e rotinas novas"]],
        num_cols=[]) +
    callout("tip", "Migrando de SE para SES",
        "Converta o SE aninhado em SES lendo de cima para baixo: cada <code>condicao; resultado</code> "
        "vira um par, e o antigo valor_falso final vira <code>VERDADEIRO; resultado</code>. "
        "O resultado e o mesmo, com metade da dor de cabeca.")
)


cad.section("erros-formula", "Erros de formula: #N/D, #VALOR!, #DIV/0! e como agir",
    p("Cedo ou tarde a planilha mostra um erro. Reconhecer o codigo e metade da solucao — a outra "
      "metade e decidir se o erro deve ser escondido ou investigado.") +
    tbl(["Erro", "Significado", "Causa tipica na POLITEC", "O que fazer"],
        [["<b>#VALOR!</b>", "Tipo incompativel", "Subtrair uma data que veio como texto.",
          "Converter o texto em data com <code>DATA.VALOR</code>."],
         ["<b>#DIV/0!</b>", "Divisao por zero", "Dividir por um total que ainda e 0 (mes sem laudos).",
          "Envolver com <code>SE.ERRO</code> ou <code>SE(denom=0;\"-\";divisao)</code>."],
         ["<b>#N/D</b>", "Nao disponivel", "PROCV/VXPROCV que nao encontrou o codigo.",
          "Checar a chave; usar <code>SE.ERRO</code> para tratar a ausencia."],
         ["<b>#REF!</b>", "Referencia invalida", "A formula apontava para uma coluna excluida.",
          "Rever a formula; em Tabela, usar nomes de coluna."],
         ["<b>#NOME?</b>", "Nome nao reconhecido", "Funcao digitada errada (ex.: SOMAR).",
          "Corrigir o nome; usar <kbd>Tab</kbd> no autocompletar."]],
        num_cols=[]) +
    code("""
        // Tratar a divisao por zero no % dentro da meta:
        =SE.ERRO(CONT.SE(...)/CONT.NUM(TAT); "-")

        // Versao explicita (sem SE.ERRO):
        =SE(CONT.NUM(TAT)=0; "-"; CONT.SE(TAT; "<="&$Meta_TAT)/CONT.NUM(TAT))
        """, "excel") +
    callout("err", "Esconder o erro nao resolve",
        "Usar <code>SE.ERRO</code> para limpar a tela pode mascarar um problema real de dados. "
        "Esconda apenas quando o erro for esperado (ex.: mes sem laudos). Erro de tipo em uma data "
        "e <b>aviso</b>, nao ruido — investigue.")
)

cad.section("caso-backlog-dna", "Caso real: a crise do backlog de DNA nos EUA",
    p("Nos anos 2000, centenas de milhares de kits e amostras de sangue estavam parados em "
      "laboratorios forenses americanos por anos, atrasando prisoes e absolvicoes. A crise ganhou "
      "repercussao nacional.") +
    step([
        ("O problema", "Sem controle sistematico, ninguem sabia onde exatamente estava o gargalo — "
                       "se na coleta, na extracao ou na analise final."),
        ("A solucao inicial", "Antes de contratar peritos ou comprar robos, a gestao implementou "
                              "planilhas com <b>CONT.SE</b> e <b>SOMASE</b> para mapear os gargalos. "
                              "Descobriram: <b>80% do atraso estava na extracao</b>."),
        ("A licao", "Voce nao pode gerenciar o que nao pode medir. A planilha foi o primeiro passo "
                    "para a automacao que zerou o backlog anos depois."),
    ]) +
    bar_chart(["Coleta", "Extracao", "Analise", "Revisao"], [8, 80, 9, 3],
              title="Onde estava o atraso do backlog de DNA (dados do caso)",
              subtitulo="A extracao concentrava 80% do tempo parado — gargalo invisivel sem medicao.",
              destaque=1) +
    ficha("g", "Traducao para a POLITEC",
        "Antes de pedir um sistema novo, use <b>CONT.SE</b> e <b>SOMASE</b> para descobrir <i>onde</i> "
        "esta o gargalo. Muitas vezes o problema nao e falta de ferramenta — e falta de medicao.")
)

cad.section("formatacao-condicional", "Formatacao condicional: o semaforo do TAT",
    p("A formatacao condicional muda automaticamente a cor da celula com base no valor, criando um "
      "<b>painel visual</b> sem precisar gerar graficos. E o recurso mais poderoso para comunicar "
      "alertas rapidamente.") +
    legenda([
        ("\U0001f7e2", "Verde — ate 30 dias", "Laudo dentro do prazo. Desempenho aceitavel."),
        ("\U0001f7e1", "Amarelo — 31 a 60 dias", "Atencao. Risco de atraso; monitoramento necessario."),
        ("\U0001f534", "Vermelho — mais de 60 dias", "Atraso critico. Acao imediata da gestao."),
    ]) +
    step([
        ("Selecione a coluna TAT", "Escolha o intervalo das celulas de TAT (a coluna inteira, exceto "
         "o cabecalho)."),
        ("Abra as regras", "<kbd>Pagina Inicial</kbd> \u2192 <kbd>Formatacao Condicional</kbd> \u2192 "
         "<kbd>Nova Regra</kbd>. No Sheets: <kbd>Formatar</kbd> \u2192 <kbd>Formatacao condicional</kbd>."),
        ("Crie as tres regras", "Uma por faixa: &lt;=30 (verde), entre 31 e 60 (amarelo), &gt;60 "
         "(vermelho). Use <b>Regras em cascata</b> e marque <i>Parar se verdadeiro</i>."),
        ("Teste", "Digite um valor alto em uma linha e confira se a celula muda de cor automaticamente."),
    ]) +
    ficha("p", "Curiosidade historica",
        "A formatacao condicional foi introduzida no <b>Excel 97</b> e revolucionou a analise visual. "
        "Pela primeira vez, gestores identificavam anomalias em milissegundos, sem imprimir relatorios.")
)

cad.section("formatacao-formula", "Formatacao condicional com formula: alem do semaforo basico",
    p("As regras prontas (maior que, entre) resolvem o semaforo. Mas e possivel pintar a linha "
      "inteira com base em <b>outra coluna</b> — o truque que transforma a tabela em um painel de "
      "verdade.") +
    code("""
        // Pintar a LINHA INTEIRA (A2:H100) quando o status for "Pendente":

        // 1. Selecione A2:H100 (nao a coluna inteira).
        // 2. Nova Regra > "Usar formula para determinar as celulas"
        // 3. Formula (trava a coluna do status com $):

        =$G2="Pendente"

        // Outras regras uteis:
        =$E2>60                 // atraso critico por TAT
        =E($A2<HOJE(); $F2="")  // requisicao vencida e ainda sem laudo
        """, "excel") +
    step([
        ("Selecione o intervalo-alvo", "Comece pela primeira celula da linha (ex.: A2) e selecione "
         "ate a ultima coluna. A regra se aplica a linha toda."),
        ("Use a formula", "Escolha <i>Usar formula para determinar as celulas a serem formatadas</i>."),
        ("Trave a coluna com $", "Escreva <code>=$G2=\"Pendente\"</code>: o <code>$</code> trava a "
         "coluna G, e o 2 sem cifrao permite que a regra ande linha a linha."),
        ("Escolha o formato", "Preenchimento suave; evite cores fortes que atrapalham a leitura."),
    ]) +
    callout("err", "Esquecer o $ na coluna da formula",
        "Sem o cifrao em <code>$G2</code>, o Excel desloca a coluna de referencia ao aplicar a "
        "regra, e a linha inteira pinta por engano. E o mesmo erro de referencia do caso da taxa "
        "de importacao — so que na formatacao condicional.")
)

cad.section("barras-dados", "Barras de dados: volume visual por tipo de exame",
    p("As <b>barras de dados</b> inserem uma barra proporcional dentro de cada celula, permitindo "
      "comparar volumes relativos de um unico olhar — sem precisar de um grafico separado.") +
    bar_chart(["Toxicologia", "DNA", "Balistica"], [90, 55, 22],
              title="Volume de requisicoes por tipo de exame",
              subtitulo="Barra longa = alto volume; barra curta = poucos casos.", destaque=None) +
    step([
        ("Selecione a coluna de volumes", "Ex.: a coluna com o total de requisicoes por tipo de exame."),
        ("Aplique a barra de dados", "<kbd>Formatacao Condicional</kbd> \u2192 <kbd>Barras de Dados</kbd>. "
         "Escolha um preenchimento solido ou gradiente."),
        ("Ajuste", "Defina minimo e maximo como <i>Automatico</i> para a barra refletir a escala real."),
    ]) +
    callout("note", "Sem grafico, ainda e visual",
        "As barras de dados dao a sensacao de grafico dentro da propria planilha. Ideal para bases "
        "que sao lidas linha a linha.")
)

cad.section("visicalc", "Curiosidade: a origem da planilha eletronica",
    p("Em <b>1979</b>, <b>Dan Bricklin</b> criou o <b>VisiCalc</b>, a primeira planilha eletronica da "
      "historia. Ela foi o killer app que fez o Apple II vender milhoes de unidades ao redor do "
      "mundo.") +
    grid2([
        ("O momento zero",
         "Antes do VisiCalc, um unico erro em uma celula de papel exigia recalcular toda a planilha "
         "manualmente — horas de trabalho."),
        ("Impacto na gestao pericial hoje",
         "Se um perito altera o numero de dias uteis em uma celula de projecao de laudos, a "
         "planilha recalcula automaticamente a previsao do mes inteiro. O que levava horas em 1978 "
         "leva um milissegundo."),
    ]) +
    ficha("g", "A linhagem",
        "A logica que Dan Bricklin inventou esta presente em cada <code>=SOMA()</code> que voce "
        "digita hoje — no Excel, no Google Sheets e em qualquer ferramenta de planilha moderna.")
)

cad.section("fechamento-manha", "Fechamento da manha: da bancada ao painel",
    p("Em quatro horas, saimos dos fundamentos para as ferramentas que transformam uma planilha "
      "comum em um sistema de monitoramento pericial. Antes de virar a pagina, fixe os tres "
      "blocos da manha.") +
    flow_h([
        ("\U0001f522", "Medir"),
        ("\u2699\ufe0f", "Decidir"),
        ("\U0001f7e2", "Alertar"),
        ("\U0001f4ca", "Painel"),
    ]) +
    grid2([
        ("1. Medir (SOMA, MEDIA, CONT.NUM)",
         "Producao do laboratorio, TAT e volume de insumos. Sem medir, nao ha gestao."),
        ("2. Decidir (SE, SOMASE, CONT.SE)",
         "Logica condicional que automatiza status, isola custo por setor e conta o backlog."),
        ("3. Alertar (Formatacao Condicional)",
         "O semaforo do TAT transforma numeros frios em um painel visual de alertas."),
        ("Proximo passo (tarde)",
         "Estruturar essas planilhas para que nao quebrem quando o volume de dados aumentar."),
    ]) +
    ficha("a", "O que voce ja sabe fazer",
        "Ao fim da manha, voce consegue medir a producao, isolar o custo de cada setor, contar o "
        "backlog por status e pintar os atrasos automaticamente. Falta blindar a estrutura — e e o "
        "que vem agora.")
)


# =================================================================
# PARTE 2 - ESTRUTURA
# =================================================================
cad.grp("Parte 2 · Modulo 3 — Referencias, tabelas e filtros",
        "Estruturar a planilha para que ela nao quebre quando o volume de dados crescer.")

cad.section("referencias", "Referencias de celulas: a base da automacao segura",
    p("Entender como o Excel interpreta referencias de celulas e fundamental para criar formulas "
      "que funcionam ao serem copiadas — e que nao geram <b>erros silenciosos</b> nos relatorios.") +
    tbl(["Tipo", "Como se escreve", "Comportamento", "Quando usar"],
        [["<b>Relativa</b>", "<code>A1</code>",
          "Muda quando a formula e copiada para outra celula.",
          "Calcular o custo de cada exame linha a linha: <code>=B2*C2</code> vira <code>=B3*C3</code>."],
         ["<b>Absoluta</b>", "<code>$A$1</code>",
          "NAO muda ao copiar. Trava linha e coluna.",
          "Parametros que se repetem (preco fixo, meta de TAT, taxa): <code>=B2*$H$1</code>."],
         ["<b>Mista</b>", "<code>$A1</code> ou <code>A$1</code>",
          "Trava apenas a linha ou apenas a coluna.",
          "Matrizes de cruzamento (Tipo de Exame x Mes)."]],
        num_cols=[]) +
    code("""
        // Relativa (muda ao copiar para baixo):
        =B2 * C2          -> copiada vira =B3 * C3

        // Absoluta (trava o parametro):
        =B2 * $H$1        -> copiada continua =B3 * $H$1

        // Onde H1 = "Custo Fixo Unitario do Reagente X".
        // Sem o cifrao, ao copiar o Excel busca o preco nas linhas
        // seguintes - calculando com valores errados ou vazios.
        """, "excel") +
    callout("err", "O erro mais caro da planilha",
        "Esquecer o <code>$</code> em um parametro fixo. Ao copiar para 500 linhas, a referencia "
        "desce e captura valores errados. Sempre <b>F4</b> em parametros.")
)

cad.section("guia-f4", "Guia do F4: os quatro modos de referencia na pratica",
    p("O <b>F4</b> e o atalho mais importante deste modulo. Durante a edicao de uma formula, ele "
      "cicla a referencia selecionada entre os quatro modos. Decorar a sequencia evita o erro de "
      "parametro solto que custou 30% do orcamento no caso real.") +
    step([
        ("Clique na referencia", "Com a formula em edicao, clique sobre a referencia <code>A1</code> "
         "(ou deixe o cursor logo apos ela)."),
        ("F4 — primeira vez", "Vira <code>$A$1</code> (absoluta: trava linha e coluna)."),
        ("F4 — segunda vez", "Vira <code>A$1</code> (mista: trava somente a linha)."),
        ("F4 — terceira vez", "Vira <code>$A1</code> (mista: trava somente a coluna)."),
        ("F4 — quarta vez", "Volta para <code>A1</code> (relativa). O ciclo se repete."),
        ("Teste a copia", "Copie a formula para outra celula e observe o que muda — e o que fica "
         "travado."),
    ]) +
    tbl(["Modo", "Como aparece", "Trava", "Uso tipico POLITEC"],
        [["Relativa", "<code>A1</code>", "Nada", "Calculo linha a linha (custo por exame)."],
         ["Absoluta", "<code>$A$1</code>", "Linha e coluna", "Parametros: meta de TAT, taxa, preco."],
         ["Mista (linha)", "<code>A$1</code>", "Somente a linha", "Matriz: fixa o mes no topo."],
         ["Mista (coluna)", "<code>$A1</code>", "Somente a coluna", "Matriz: fixa o tipo de exame."]],
        num_cols=[]) +
    callout("tip", "No Google Sheets",
        "O Sheets nao tem o ciclo do F4 com a mesma fluidez. Digite o <code>$</code> manualmente ou "
        "use <kbd>F4</kbd> em algumas versoes. Ao colar uma formula do Excel, confira as referencias.")
)

cad.section("referencia-mista", "Referencia mista e o atalho F4",
    p("A referencia mista (<code>$A1</code> ou <code>A$1</code>) trava <b>apenas</b> a linha ou "
      "apenas a coluna. E essencial para construir <b>matrizes de cruzamento</b> — uma das "
      "estruturas mais poderosas para a gestao do laboratorio.") +
    grid2([
        ("Quando usar",
         "Matrizes que cruzam duas dimensoes: <b>Tipo de Exame</b> (Toxicologia, DNA, Balistica) x "
         "<b>Mes do Ano</b> (Jan-Dez). Cada celula precisa referenciar a linha do seu exame e a "
         "coluna do seu mes — sem que ambos se movam juntos."),
        ("Atalho essencial: F4",
         "Pressione <kbd>F4</kbd> enquanto edita a formula para ciclar entre quatro modos: "
         "<code>A1</code> \u2192 <code>$A$1</code> \u2192 <code>A$1</code> \u2192 <code>$A1</code>. "
         "Memorize — previne os erros mais caros."),
    ]) +
    code("""
        // Matriz: linhas = Tipo de Exame, colunas = Mes
        // Na celula B2 da matriz:
        =CONT.SES($A2; B$1)      // trava a coluna do exame e a linha do mes

        // Ciclo do F4:
        A1  ->  $A$1  ->  A$1  ->  $A1  ->  (A1 ...)
        """, "excel") +
    aplicab(
        "Ao montar qualquer matriz de cruzamento (tipo x mes, setor x tipo).",
        "Porque uma unica formula precisa andar na vertical e travar na horizontal ao mesmo tempo.",
        "A matriz mensal de exames por tipo: escreva a formula uma vez em B2 e arraste para toda a "
        "grade — as referencias mistas fazem o resto.") +
    callout("tip", "No Google Sheets",
        "O Sheets nao tem F4 para ciclar cifroes com a mesma fluidez, mas aceita a digitacao manual "
        "de <code>$</code>. Ao colar uma formula do Excel, confira as referencias.")
)

cad.section("referencias-abas-nomes", "Referencias entre abas e intervalos nomeados",
    p("Formulas boas nao vivem presas a uma unica aba. Referenciar outra aba e dar nome aos "
      "intervalos deixa a planilha legivel — e evita o pior dos erros: parametro escondido no meio "
      "dos dados.") +
    tbl(["Recurso", "Sintaxe", "Vantagem"],
        [["<b>Referencia a outra aba</b>", "<code>=Parametros!B1</code>",
          "Separa metas/precos da base, como recomenda a arquitetura de abas."],
         ["<b>Aba com espaco no nome</b>", "<code>='Base de Dados'!B1</code>",
          "Funciona, mas o nome entre apostrofos e mais fragil. Prefira <code>Base</code>."],
         ["<b>Intervalo nomeado</b>", "<code>=Meta_TAT</code>",
          "Em vez de <code>Parametros!$B$1</code>, usa-se um nome. Muito mais legivel."],
         ["<b>Nome de Tabela</b>", "<code>=TabelaLaudos[dias_uteis]</code>",
          "Aponte para a coluna inteira sem se preocupar com o tamanho."]],
        num_cols=[]) +
    step([
        ("Crie a aba Parametros", "Uma aba so com metas (Meta_TAT = 30 dias), separada da base."),
        ("Selecione a celula", "Ex.: <code>Parametros!$B$1</code>, que contem a meta de TAT."),
        ("Abra o Gerenciador de Nomes", "<kbd>Formulas</kbd> \u2192 <kbd>Gerenciador de Nomes</kbd> "
         "no Excel; no Sheets, defina o nome na barra de endereco."),
        ("Defina o nome", "Chame de <code>Meta_TAT</code>. Nomes nao podem ter espacos nem acentos."),
        ("Use na formula", "<code>=CONT.SE(TabelaLaudos[dias_uteis];\"&lt;=\"&amp;Meta_TAT)</code> — "
         "leitura imediata, sem cifroes."),
    ]) +
    callout("err", "Nome com espaco ou acento",
        "Nomes de intervalo com espaco obrigam a usar colchetes e quebram em outras ferramentas. "
        "Use <code>_</code> e nada de acentos: <code>Meta_TAT</code>, nunca 'Meta TAT'.")
)

cad.section("caso-taxa", "Caso real: o erro de referencia que custou milhoes",
    p("Um laboratorio de analises clinicas calculou o orcamento anual de reagentes em uma planilha. "
      "O analista esqueceu de travar a celula da <b>Taxa de Importacao</b> com referencia absoluta.") +
    step([
        ("O erro tecnico", "A formula sem cifrao foi copiada para 500 itens. A taxa de importacao foi "
                           "descendo pelas linhas, capturando valores aleatorios ou zerados de "
                           "celulas com outros dados."),
        ("A consequencia", "O orcamento foi aprovado com um <b>deficit de 30%</b>. O laboratorio "
                           "ficou sem reagentes no meio do ano fiscal, comprometendo as analises."),
        ("A licao POLITEC", "Sempre use <b>F4</b> para travar celulas de parametros fixos: precos de "
                            "reagentes, metas de TAT, taxas de conversao. Esta e a regra de ouro da "
                            "planilha segura."),
    ]) +
    antesdepois(
        "<code>=B2*C2</code> copiada para 500 linhas, com a taxa descendo pelas linhas.",
        "<code>=B2*$C$1</code> com a taxa travada em uma celula de parametro.",
        "Parametro solto", "Parametro travado ($)") +
    ficha("r", "A conta do prejuizo",
        "Um cifrao faltando (<code>$</code>) custou 30% do orcamento anual. Nenhuma formula estava "
        "errada — apenas solta. E o tipo de erro que nao aparece na tela e so se revela na conta "
        "final.")
)

cad.section("aplic-orcamento-reagentes", "Aplicacao pratica: planilha de orcamento de reagentes imune a erro",
    p("Cenario: montar o orcamento anual de reagentes de forma que <b>nenhum parametro deslize</b> "
      "ao ser copiado para centenas de itens. A regra e simples: parametros fixos moram em uma aba "
      "propria e sao sempre travados.") +
    code("""
        // Aba Parametros:
        //   B1 = Taxa de Importacao (%)      -> nome: Taxa_Imp
        //   B2 = Custo Unitario do Reagente  -> nome: Custo_Unit
        //   B3 = Margem de Seguranca (%)     -> nome: Margem

        // Aba Orcamento (linha 2 em diante):
        Custo_Base   = [@Qtd] * Custo_Unit
        Custo_Import = Custo_Base * Taxa_Imp
        Custo_Total  = Custo_Base + Custo_Import
        Custo_Margem = Custo_Total * (1 + Margem)

        // Com celulas (sem nomes), forma classica:
        =B2*$H$1 + (B2*$H$1)*$H$2
        """, "excel") +
    step([
        ("Separe a aba Parametros", "Uma aba so com taxa, custo unitario e margem. Nada de parametro "
         "no meio da base."),
        ("Nomeie os parametros", "Defina <code>Taxa_Imp</code>, <code>Custo_Unit</code> e "
         "<code>Margem</code> (ou use <code>$H$1</code> etc.)."),
        ("Escreva a formula na primeira linha", "Combine quantidade, custo e taxa, sempre com os "
         "parametros travados."),
        ("Confira a primeira linha", "Bata o valor manualmente antes de copiar."),
        ("Arraste para todas as linhas", "Com o parametro travado, a formula copia certa em 500 ou "
         "5.000 itens."),
        ("Simule variacoes", "Altere a taxa na aba Parametros e veja o orcamento inteiro se ajustar "
         "de forma consistente."),
    ]) +
    aplicab(
        "Em qualquer orcamento com parametros que se repetem (taxa, frete, imposto, meta).",
        "Porque um unico parametro solto contamina centenas de linhas silenciosamente.",
        "Orcamento anual de reagentes: a taxa de importacao fica travada em <code>Parametros!$B$1</code> "
        "e vale para todos os itens sem excecao.") +
    callout("err", "Parametro em linha fora do intervalo",
        "Se voce travar <code>$H$1</code> mas cortar a linha 1 ao selecionar o intervalo, a "
        "referencia quebra. Deixe sempre uma margem ao redor da celula de parametro.")
)

cad.section("tabelas-estruturadas", "Tabelas estruturadas: o fim das planilhas caoticas",
    p("Pressionar <b>Ctrl+T</b> (ou <i>Inserir \u203a Tabela</i>) transforma um intervalo comum em uma "
      "<b>Tabela Oficial</b> do Excel — com comportamento de banco de dados, expansao automatica e "
      "formulas inteligentes. No dataset <code>requisicoes_periciais.csv</code>, a TabelaLaudos tera "
      "9 colunas.") +
    legenda([
        ("\u2795", "Expansao automatica", "Cole 50 novas requisicoes no fim da tabela: formulas e "
         "formatacao condicional se estendem sozinhas, sem arrastar a alca."),
        ("\U0001f4d6", "Formulas legiveis", "Em vez de <code>=SOMASE(G2:G121;\"Toxicologia\";I2:I121)</code>, "
         "voce escreve <code>=SOMASE(TabelaLaudos[setor];\"Toxicologia\";TabelaLaudos[dias_uteis])</code>."),
        ("\U0001f53d", "Filtros automaticos", "As setas de filtro aparecem no cabecalho de cada "
         "coluna, sem configuracao adicional."),
    ]) +
    step([
        ("Importe e posicione", "Apos importar <code>requisicoes_periciais.csv</code>, clique em "
         "qualquer celula da base."),
        ("Ctrl+T", "Marque <b>Minha tabela tem cabecalho</b> e confirme."),
        ("Nomeie a tabela", "Em <i>Design da Tabela</i>, renomeie para "
         "<code>TabelaLaudos</code>. Este nome sera usado nas formulas."),
        ("Solte as formulas", "Reescreva os indicadores usando nomes de coluna. Eles nao quebram "
         "quando a base cresce."),
    ]) +
    callout("err", "Tabela nao gosta de celulas vazias nem mescladas",
        "Nunca mescle celulas dentro de uma tabela e evite linhas totalmente vazias no meio da base. "
        "Isso confunde a expansao automatica e quebra filtros.")
)

cad.section("tabela-estruturada-detalhe", "Tabela estruturada em detalhe: [@] e nomes de coluna",
    p("A grande vantagem da Tabela Estruturada e a <b>sintaxe por nome</b>. Voce para de contar "
      "linhas e passa a falar em linguagem de dados: a coluna setor da TabelaLaudos.") +
    tbl(["Notacao", "Significado", "Exemplo"],
        [["<code>TabelaLaudos[setor]</code>", "A <b>coluna inteira</b> setor.",
          "Vai de A2 ate o fim, mesmo que a base dobre."],
         ["<code>[@[status]]</code>", "O valor da <b>linha atual</b> dessa coluna.",
          "Dentro da tabela: <code>=[@[data_laudo]]-[@[data_recebimento]]</code>."],
         ["<code>TabelaLaudos[[#Totais];[dias_uteis]]</code>", "Linha de totais da tabela (se ativa).",
          "Total rapido sem formula separada."],
         ["<code>TabelaLaudos[@]</code>", "A linha inteira atual.",
          "Menos comum, mas util em algumas referencias."]],
        num_cols=[]) +
    code("""
        // NAO use referencias de celulas fixas dentro da tabela:
        =SOMASE(G2:G121; "Toxicologia"; I2:I121)    // quebra se a base crescer

        // USE nomes de coluna:
        =SOMASE(TabelaLaudos[setor]; "Toxicologia"; TabelaLaudos[dias_uteis])

        // Coluna calculada linha a linha:
        =[@[data_laudo]] - [@[data_recebimento]]
        """, "excel") +
    callout("tip", "Digite [ e o Excel ajuda",
        "Dentro de uma tabela, ao digitar <code>[</code>, o Excel lista as colunas disponiveis. "
        "Selecione com as setas e <kbd>Tab</kbd> — voce nao precisa decorar nomes.")
)


cad.section("tabela-bi", "A tabela estruturada como ponte para o BI",
    p("A planilha de controle de laudos estruturada hoje sera o <b>mesmo arquivo</b> que alimentara o "
      "Power BI no Dia 4 do curso — sem retrabalho, sem perda de dados.") +
    ficha("p", "A frase que orienta a transicao",
        "Antes de modelar dados em um sistema de BI, eles precisam ser estruturados. Tabelas sao a "
        "ponte entre a planilha amadora e o banco de dados profissional. — <b>Ralph Kimball</b>, "
        "pai do Data Warehouse dimensional.") +
    flow_h([
        ("\U0001f4c4", "Base bruta"),
        ("\U0001f4d0", "Tabela estruturada"),
        ("\U0001f4ca", "Indicadores"),
        ("\U0001f4c8", "Power BI"),
    ]) +
    callout("tip", "Prepare hoje, colha no Dia 4",
        "Se a base estiver em Tabela Estruturada, com colunas bem nomeadas e sem celulas mescladas, "
        "a importacao no Power BI e quase automatica. O trabalho de hoje e o modelo de amanha.")
)

cad.section("filtros", "Filtros: isolando a inteligencia forense",
    p("O filtro transforma uma base volumosa em uma resposta objetiva. Na gestao pericial, "
      "velocidade e precisao na leitura dos dados podem ser decisivas.") +
    tbl(["Tipo de filtro", "Como acionar", "Uso na POLITEC"],
        [["<b>Basico</b>", "<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>L</kbd>",
          "Isolar apenas requisicoes da Delegacia de Homicidios com status Pendente."],
         ["<b>Por cor</b>", "Clique no filtro \u203a <i>Filtrar por Cor \u203a Vermelho</i>.",
          "Ver apenas os laudos com <b>Atraso Critico</b> — resultado direto do semaforo do TAT."],
         ["<b>Texto e numero</b>", "Filtrar onde Nome contem Silva ou Valor \u2265 R$ 10.000.",
          "Auditorias rapidas de fornecedores e prestadores de servico."]],
        num_cols=[]) +
    callout("tip", "Filtro por cor",
        "O filtro por cor so funciona porque a formatacao condicional <b>pinta</b> as celulas. Por "
        "isso os dois recursos se combinam: o semaforo cria a cor, o filtro por cor isola os casos.")
)

cad.section("filtros-avancados", "Filtros avancados: entre, contem, top 10 e filtro por cor",
    p("O filtro basico esconde linhas. O <b>filtro avancado</b> responde perguntas de gestao: "
      "quais sao os 10 maiores custos? quais laudos comecam com REQ- e vieram da capital? "
      "o que esta com atraso critico?") +
    tbl(["Filtro", "Como fazer", "Pergunta que responde"],
        [["<b>Intervalo / entre</b>", "Numero \u203a Entre \u2192 31 e 60.",
          "Quantos laudos estao na faixa de atencao (amarelo)?"],
         ["<b>Contem / comeca com</b>", "Texto \u203a Contem \u2192 Homicidios.",
          "Quais requisicoes vieram da Delegacia de Homicidios?"],
         ["<b>Top 10</b>", "Numero \u203a 10 maiores.",
          "Quais foram os 10 exames mais caros do mes?"],
         ["<b>Por cor</b>", "Filtrar por Cor \u2192 Vermelho.",
          "Quais laudos estao em atraso critico (do semaforo)?"],
         ["<b>Varios niveis</b>", "Filtrar primeiro por Setor, depois por Status.",
          "Quantos laudos de DNA estao pendentes no setor Genetica?"]],
        num_cols=[]) +
    step([
        ("Ative os filtros", "<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>L</kbd> na TabelaLaudos."),
        ("Escolha a coluna", "Clique na seta do cabecalho da coluna relevante (ex.: Custo)."),
        ("Defina o criterio", "Numero \u203a 10 maiores, ou Texto \u203a Contem, conforme a pergunta."),
        ("Combine filtros", "Aplique um segundo filtro em outra coluna para cruzar os criterios."),
        ("Leia o resultado", "O contador de registros na barra de status mostra quantas linhas "
         "sobraram."),
    ]) +
    callout("err", "Filtrar e esquecer de limpar",
        "Um filtro esquecido no arquivo faz o proximo relatorio sair errado — some poucos laudos "
        "quando na verdade a base esta filtrada. Sempre limpe os filtros antes de salvar/compartilhar.")
)

cad.section("fantasma-heilbronn", "O Fantasma de Heilbronn: quando ordenar salva uma investigacao",
    p("Entre 2007 e 2009, a policia de varios paises europeus encontrou o mesmo DNA feminino em cenas "
      "de crime completamente diferentes — um assassinato na Austria, um roubo na Franca, outros "
      "casos na Alemanha. A imprensa cunhou o termo <b>O Fantasma de Heilbronn</b>.") +
    step([
        ("A investigacao", "Centenas de investigadores foram mobilizados. A serial killer foi "
                           "colocada na lista dos criminosos mais procurados da Europa, com "
                           "recompensa de <b>300 mil euros</b>."),
        ("A virada pelos dados", "Um analista exportou a base de todos os casos, <b>ordenou pelo "
                                 "Numero de Lote do Swab de Algodao</b> e filtrou os resultados. "
                                 "Todos os casos positivos batiam com o mesmo lote de swabs."),
        ("A revelacao", "O DNA da assassina era, na verdade, o DNA de uma <b>operaria austriaca</b> "
                        "que fabricava os cotonetes usados pela policia — sem luvas, anos antes."),
    ]) +
    ficha("r", "A licao",
        "Ordenar e filtrar nao e burocracia. E a ferramenta que separa uma <b>investigacao brilhante</b> "
        "de um <b>erro forense catastrofico</b>. A contaminacao estava no dado de entrada, nao na "
        "analise de DNA.")
)

cad.section("ordenacao", "Ordenacao: organizando a inteligencia pericial",
    p("Ordenar e mais do que colocar em ordem alfabetica. Para a gestao de laboratorio, define quem "
      "atende primeiro e quais casos chegam ao topo da fila.") +
    grid2([
        ("Ordenacao simples",
         "Crescente ou decrescente por uma coluna. <b>Aplicacao:</b> ordenar a fila por Data de "
         "Recebimento — os mais antigos no topo, para atacar o backlog pelos casos mais criticos "
         "em prazo."),
        ("Ordenacao personalizada",
         "Uma ordem logica que nao e alfabetica nem numerica — definida pelo gestor. <b>Aplicacao "
         "POLITEC:</b> ordenar por gravidade do crime, independente da data de entrada."),
    ]) +
    tbl(["Nivel", "Prioridade", "Tipos de crime"],
        [["\U0001f534 1", "Maxima prioridade", "Homicidio / Crime Sexual"],
         ["\U0001f7e0 2", "Alta prioridade", "Roubo / Trafico de Drogas"],
         ["\U0001f7e1 3", "Prioridade padrao", "Furto / Demais crimes"]],
        num_cols=[]) +
    step([
        ("Abra as listas personalizadas", "<kbd>Arquivo</kbd> \u2192 <kbd>Opcoes</kbd> \u2192 "
         "<kbd>Avançado</kbd> \u2192 <kbd>Geral</kbd> \u2192 <kbd>Editar Listas Personalizadas</kbd>."),
        ("Crie a lista", "Digite, uma por linha, na ordem de prioridade: Homicidio/Crime Sexual; "
         "Roubo/Trafico; Furto/Demais."),
        ("Ordene pela lista", "Na coluna de gravidade, use <i>Ordenacao Personalizada</i> e escolha "
         "a lista criada. O Excel passa a entender a prioridade institucional."),
    ]) +
    callout("note", "Google Sheets",
        "No Sheets, use <i>Classificar intervalo</i> \u2192 <i>Ordem personalizada</i> ou uma coluna "
        "auxiliar com o ranking (1, 2, 3) e ordene por ela.")
)

cad.section("aplic-fila-laudos-criticos", "Aplicacao pratica: a fila de laudos criticos para a reuniao das 8h",
    p("Cenario: montar, em menos de 10 segundos, a lista exata de laudos criticos que precisam ser "
      "cobrados na reuniao das 8h — priorizando gravidade do crime e antiguidade do processo.") +
    step([
        ("Parta da TabelaLaudos", "A base ja esta em Tabela Estruturada (Ctrl+T)."),
        ("Aplique o semaforo", "A coluna TAT esta pintada: verde, amarelo e vermelho."),
        ("Filtre por cor vermelha", "Na coluna TAT/Status, <i>Filtrar por Cor \u2192 Vermelho</i>. "
         "Sobram apenas os atrasos criticos."),
        ("Ordene pela lista de prioridade", "Na coluna gravidade, <i>Ordenacao Personalizada</i> "
         "(Homicidio primeiro)."),
        ("Desempate por data", "Dentro de cada prioridade, ordene por Data_Recebimento crescente — "
         "os mais antigos primeiro."),
        ("Leve a lista", "Copie o resultado para um slide ou imprima. Missao cumprida."),
    ]) +
    flow_h([
        ("\u2328\ufe0f", "Ctrl+T"),
        ("\U0001f534", "Filtrar vermelho"),
        ("\U0001f522", "Ordenar prioridade"),
        ("\u2705", "Lista 8h"),
    ]) +
    callout("err", "Excluir o filtro antes de salvar",
        "Se o arquivo for salvo com o filtro vermelho ativo, quem abrir depois pensara que o "
        "laboratorio so tem 12 laudos. Limpe os filtros antes de arquivar a base.")
)

cad.section("combinacao", "Combinacao de tecnicas: o painel de comando",
    p("A verdadeira eficiencia surge quando <b>Tabela Estruturada</b>, <b>Formatacao Condicional</b>, "
      "<b>Filtro por Cor</b> e <b>Ordenacao Personalizada</b> trabalham em conjunto — transformando "
      "a planilha em um painel de comando.") +
    flow_h([
        ("\u2328\ufe0f", "Ctrl+T"),
        ("\U0001f534", "Filtrar vermelho"),
        ("\U0001f522", "Ordenar prioridade"),
        ("\u2705", "Lista 8h"),
    ]) +
    step([
        ("Abrir tabela", "Ctrl+T para transformar a base em Tabela Estruturada."),
        ("Filtrar vermelho", "Mostrar apenas os atrasos criticos (cor vermelha do semaforo)."),
        ("Ordenar prioridade", "Ordenar pela lista personalizada: homicidios primeiro."),
        ("Ter a lista pronta", "Em menos de 10 segundos, a lista exata para a reuniao das 8h."),
    ]) +
    ficha("g", "O resultado",
        "Em <b>menos de 10 segundos</b>, o Diretor da POLITEC tem a lista exata de quais laudos "
        "criticos precisam ser cobrados na reuniao das 8h — sem nenhuma intervencao manual alem de "
        "tres cliques.")
)


cad.section("aplic-consolidacao-planilhas", "Aplicacao pratica: consolidacao de varias planilhas (previa do Power Query)",
    p("Cenario: cada setor (Toxicologia, DNA, Balistica, IML) mantem a sua propria planilha. A "
      "direcao quer <b>uma unica base consolidada</b> — sem copiar e colar linha por linha.") +
    step([
        ("Padronize os cabecalhos", "Todas as planilhas devem ter exatamente as mesmas colunas: "
         "<code>Num_Requisicao, Tipo_Exame, Data_Recebimento, Data_Laudo, TAT_Dias, Status, Setor, "
         "Custo_Reagente</code>."),
        ("Salve como CSV UTF-8", "Exporte cada planilha de setor no mesmo formato e codificacao "
         "(UTF-8, separador definido)."),
        ("Empilhe as bases", "Cole as linhas de todos os setores na aba <code>Base</code>, uma embaixo "
         "da outra, mantendo a ordem das colunas."),
        ("Adicione a coluna Origem", "Crie <code>Arquivo_Origem</code> com o nome do setor ou do "
         "arquivo — rastreabilidade."),
        ("Converta em Tabela", "Ctrl+T na base consolidada e nomeie <code>TabelaConsolidada</code>."),
        ("Valide por CONT.SE", "Compare <code>=CONT.SE(TabelaConsolidada[Setor];\"DNA\")</code> com "
         "o total original do setor. Os numeros devem bater."),
    ]) +
    code("""
        // Validacao da consolidacao: total por setor deve bater com cada origem
        =CONT.SE(TabelaConsolidada[Setor]; "Toxicologia")
        =CONT.SE(TabelaConsolidada[Setor]; "DNA")
        =CONT.SE(TabelaConsolidada[Setor]; "Balistica")
        =CONT.SE(TabelaConsolidada[Setor]; "IML")

        // Total geral:
        =CONT.VALORES(TabelaConsolidada[Num_Requisicao])
        """, "excel") +
    callout("err", "Copiar e colar de varias abas mistura colunas",
        "Se as planilhas de setor tiverem ordem de colunas diferente, o empilhamento desalinha tudo "
        "e a base nasce contaminada. Padronize os cabecalhos <b>antes</b> de juntar. No Dia 3, o "
        "Power Query resolve isso automaticamente.")
)

cad.section("subtotais-dinamicas", "Subtotais e Tabelas Dinamicas: o primeiro passo da analise",
    p("Antes de partir para o Power BI, a propria planilha ja responde perguntas de agrupamento com "
      "<b>Subtotais</b> e <b>Tabelas Dinamicas</b> — sem escrever uma formula sequer.") +
    tbl(["Recurso", "O que faz", "Quando usar"],
        [["<b>Subtotais</b>", "Insere linhas de resumo por grupo (setor, tipo).",
          "Relatorio rapido impresso, uma vez, com a base ja ordenada."],
         ["<b>Tabela Dinamica</b>", "Agrupa e cruza dados por arrastar campos.",
          "Explorar producao por setor x mes sem refazer formulas."],
         ["<b>Segmentacao (Slicer)</b>", "Botao de filtro visual ligado a dinâmica.",
          "Painel minimo interativo dentro da planilha."]],
        num_cols=[]) +
    step([
        ("Ordene primeiro", "A base precisa estar ordenada pela coluna de agrupamento (ex.: Setor) "
         "para os Subtotais funcionarem."),
        ("Aplique os Subtotais", "<kbd>Dados</kbd> \u2192 <kbd>Subtotais</kbd> \u2192 agrupar por "
         "Setor, usar <b>CONT</b> ou <b>SOMA</b>."),
        ("Ou crie a Dinamica", "<kbd>Inserir</kbd> \u2192 <kbd>Tabela Dinamica</kbd>; arraste Setor "
         "para Linhas e Custo para Valores."),
        ("Compreenda a diferenca", "Subtotais alteram a base (criam linhas); a Dinamica vive em "
         "outra aba e nao mexe no dado bruto."),
    ]) +
    callout("tip", "Dinamica x formula",
        "Para um numero que precisa atualizar sozinho em um painel, prefira <code>CONT.SES</code>/"
        "<code>SOMASES</code>. Para exploracao rapida e ad-hoc, a Tabela Dinamica e imbatível.")
)

cad.section("colunas-medidas", "Colunas calculadas x medidas: preparando o vocabulario do BI",
    p("Ao estruturar a base hoje, voce ja esta preparando o Dia 4. Duas palavras que vao reaparecer "
      "no Power BI podem ser entendidas agora, na planilha: <b>coluna calculada</b> e <b>medida</b>.") +
    grid2([
        ("Coluna calculada (linha a linha)",
         "Um valor por <b>linha</b>. Exemplo: <code>=[@[data_laudo]]-[@[data_recebimento]]</code>. "
         "E a coluna dias_uteis que ja existe no dataset."),
        ("Medida (agregacao)",
         "Um valor que resume <b>muitas linhas</b>. Exemplo: <code>=MEDIA(TabelaLaudos[dias_uteis])</code>. "
         "E o que a direcao quer ver no cartao do painel."),
    ]) +
    tbl(["Pergunta", "Resposta", "Tipo"],
        [["Qual o TAT desta requisicao?", "dias_uteis (ja existe na base).", "Por linha"],
         ["Qual o TAT medio do laboratorio?", "MEDIA(dias_uteis).", "Agregada"],
         ["Quantas requisicoes por setor?", "CONT.SE(setor; \"Toxicologia\").", "Agregada"],
         ["Esta requisicao esta em atraso?", "SE(dias_uteis>60; \"Critico\"; \"OK\").", "Por linha"]],
        num_cols=[]) +
    callout("note", "Por que isso importa agora",
        "No Power BI, colunas calculadas e medidas se comportam de forma diferente e a escolha afeta "
        "o desempenho. Entender a distincao hoje — ainda no Excel — deixa a transicao do Dia 4 muito "
        "mais leve.")
)

cad.section("limite-excel", "Quando a planilha chega ao seu limite",
    p("O Excel suporta ate <b>1.048.576 linhas</b> por planilha — mais do que suficiente para a "
      "maioria das operacoes. O limite que importa, porem, e <b>pratico</b>.") +
    grid2([
        ("O limite pratico na POLITEC",
         "Acima de <b>100.000 linhas</b> com muitas formulas condicionais (SOMASES, SE aninhados, "
         "formatacao condicional extensa), a planilha comeca a travar e o tempo de recalculo aumenta "
         "significativamente."),
        ("A solucao: saber a hora de migrar",
         "Quando a base de requisicoes ultrapassar <b>50.000 linhas</b>, e hora de migrar a analise "
         "para ferramentas mais robustas."),
    ]) +
    tbl(["Ponto de virada", "Ferramenta", "Para que serve"],
        [["Transformacao pesada", "<b>Power Query</b> (dentro do Excel)",
          "Limpeza e transformacao de dados grandes."],
         ["Analise e visualizacao", "<b>Power BI</b>",
          "Dashboards interativos para a lideranca (Dia 4)."],
         ["Grandes volumes multiusuario", "<b>Banco de dados relacional</b>",
          "Gestao com muitos usuarios simultaneos."]],
        num_cols=[]) +
    callout("tip", "Regra de bolso",
        "Planilha e otima ate dezenas de milhares de linhas. Acima disso, ela continua servindo como "
        "<b>entrada</b>, mas a analise deve ir para o Power Query ou o Power BI.")
)

cad.section("checklist-migracao-bi", "Checklist de migracao do Excel para o BI",
    p("Antes de levar a base da POLITEC para o Power BI (Dia 4), passe por este checklist. Cada item "
      "marcado e um erro de importacao a menos.") +
    checklist([
        "Base em <b>Tabela Estruturada</b>, com nome definido (<code>TabelaLaudos</code>).",
        "Cabecalhos curtos, sem espacos nem acentos (<code>Data_Emissao</code>).",
        "Datas no formato <b>numerico</b> (alinhadas a direita).",
        "Nenhuma celula mesclada nem linha de total no meio da base.",
        "Sem linhas de Total Geral ou rodapes exportados pelo sistema legado.",
        "Arquivo salvo como <b>CSV UTF-8</b> ou .xlsx com uma unica aba de base.",
        "Colunas calculadas criadas (TAT_Dias, Mes_Emissao).",
        "Contagens validadas por <code>CONT.SE</code> contra a origem.",
    ]) +
    flow_h([
        ("\U0001f9f9", "Base limpa"),
        ("\U0001f4d0", "Tabela"),
        ("\U0001f4c4", "CSV UTF-8"),
        ("\U0001f4c8", "Power BI"),
    ]) +
    callout("err", "Linha de Total Geral no CSV",
        "Sistemas legados exportam uma linha de total no fim. Se ela for para o BI, vira uma "
        "categoria fantasma e distorce todas as somas. Delete antes de carregar — sempre.")
)

cad.section("fechamento-tarde", "Fechamento da tarde: da planilha ao banco de dados",
    p("A tarde foi sobre <b>blindagem</b>: referencias travadas, tabelas estruturadas, filtros e "
      "ordenacao. Juntas, essas tecnicas transformam a planilha de um arquivo fragil em um "
      "<b>banco de dados de fato</b>.") +
    grid2([
        ("O que aprendemos",
         ul(["Referencias relativas, absolutas e mistas (F4)",
             "Tabelas estruturadas com nomes de coluna (Ctrl+T)",
             "Filtros avancados e filtro por cor",
             "Ordenacao personalizada por prioridade",
             "Consolidacao de varias planilhas"])),
        ("Por que importa",
         ul(["A planilha nao quebra ao crescer",
             "As formulas se tornam legiveis e auditaveis",
             "Os parametros nao deslizam mais",
             "A base de hoje vira a fonte do BI amanha",
             "A fila de laudos vira decisao em 10 segundos"])),
    ]) +
    ficha("g", "O saldo do dia",
        "Pela manha aprendemos a <b>medir e decidir</b>. A tarde aprendemos a <b>estruturar</b> para "
        "que a medicao nao quebre. E exatamente a ponte que o Dia 3 vai atravessar com validacao e "
        "visualizacao.")
)


# =================================================================
# PARTE 3 - PRATICA
# =================================================================
cad.grp("Parte 3 · Pratica guiada",
        "Sete laboratorios que constroem, do zero, o painel de gestao de laudos.")

cad.section("lab1", "Lab 1 — Estruturar a base (Ctrl+T)",
    p("Objetivo: a partir do dataset <code>requisicoes_periciais.csv</code>, criar a Tabela "
      "Estruturada que sera a base de todos os calculos do painel de gestao.") +
    step([
        ("Importe o CSV", "Abra o arquivo <code>requisicoes_periciais.csv</code> no Excel: "
         "<kbd>Dados</kbd> \u2192 <kbd>De Text/CSV</kbd>. Selecione o arquivo, configure "
         "ponto e virgula como delimitador e UTF-8. A coluna dias_uteis ja esta calculada."),
        ("Verifique as colunas", "O dataset tem: id_requisicao, data_recebimento, delegacia_origem, "
         "tipo_exame, setor, perito_responsavel, status, data_laudo, dias_uteis."),
        ("Confira o formato das datas", "As colunas data_recebimento e data_laudo devem estar "
         "alinhadas a direita (numerico). Se estiverem a esquerda, sao texto — corrija."),
        ("Ctrl+T", "Selecione toda a base e pressione Ctrl+T; marque <i>Minha tabela tem "
         "cabecalho</i>."),
        ("Nomeie a tabela", "Renomeie para <code>TabelaLaudos</code> no <i>Design da Tabela</i>."),
        ("Teste a expansao", "Cole duas linhas novas no fim e veja formulas/formatacao se estenderem."),
    ]) +
    callout("err", "Antes de tudo: sem celulas mescladas",
        "Se a base tem cabecalhos mesclados ou linhas vazias no meio, a Tabela Estruturada vai "
        "falhar. Desmescle e preencha as lacunas primeiro.")
)

cad.section("lab2", "Lab 2 — Verificar o TAT com SE e HOJE",
    p("Objetivo: no dataset <code>requisicoes_periciais.csv</code>, a coluna dias_uteis ja existe "
      "para laudos concluidos. Vamos criar uma coluna de Status que diga se o laudo pendente ja "
      "esta em atraso usando <code>=HOJE()</code>.") +
    code("""
        // Coluna Status_Prazo (nova coluna na TabelaLaudos):
        // Se data_laudo esta vazia (pendente), usa HOJE; senao usa a data do laudo
        =SE(data_laudo=""; "Em andamento"; SE(HOJE()-data_recebimento>60; "ATRASO CRITICO";
            SE(HOJE()-data_recebimento>30; "Atencao"; "No prazo")))
        """, "excel") +
    step([
        ("Insira a nova coluna", "Clique em uma celula vazia a direita da ultima coluna da "
         "TabelaLaudos, digite o cabecalho <code>Status_Prazo</code>."),
        ("Escreva a formula", "Use os nomes de coluna da tabela: <code>=SE(data_laudo=\"\";...)</code>."),
        ("Formate como texto", "A coluna exibira textos como Em andamento ou ATRASO CRITICO."),
        ("Trate o vazio", "O <code>SE(...=\"\";\"Em andamento\";...)</code> evita erros em "
         "laudos pendentes."),
        ("Confira", "Compare uma linha pendente: dias desde data_recebimento vs. resultado da formula."),
    ]) +
    callout("tip", "HOJE() atualiza a cada abertura",
        "<code>=HOJE()</code> se atualiza a cada vez que o arquivo e aberto. A coluna de "
        "espera cresce sozinha — sem ninguem precisar reescrever nada.")
)

cad.section("lab3", "Lab 3 — Aplicar o semaforo do TAT",
    p("Objetivo: pintar a coluna Status_Prazo (ou dias_uteis) da TabelaLaudos em verde, amarelo "
      "e vermelho com regras em cascata.") +
    step([
        ("Selecione a coluna Status_Prazo", "Toda a coluna, sem incluir o cabecalho."),
        ("Regra 1 (vermelho)", "Formatacao Condicional \u2192 Nova Regra \u2192 "
         "<i>Formatar somente celulas que contenham</i> \u2192 texto contem \"CRITICO\" \u2192 "
         "preenchimento vermelho."),
        ("Regra 2 (amarelo)", "Nova Regra \u2192 texto contem \"Atencao\" \u2192 "
         "preenchimento amarelo."),
        ("Regra 3 (verde)", "Nova Regra \u2192 texto contem \"No prazo\" \u2192 "
         "preenchimento verde."),
        ("Marque Parar se verdadeiro", "Em cada regra, marque <i>Parar se verdadeiro</i> para "
         "que apenas uma cor se aplique por celula."),
    ]) +
    checklist([
        "Status contendo \"CRITICO\" ficam vermelhos.",
        "Status contendo \"Atencao\" ficam amarelos.",
        "Status contendo \"No prazo\" ficam verdes.",
        "O filtro por cor mostra apenas os vermelhos.",
    ])
)

cad.section("lab4", "Lab 4 — Criar os indicadores com referencias absolutas",
    p("Objetivo: montar a aba de indicadores sobre a TabelaLaudos (dataset "
      "<code>requisicoes_periciais.csv</code>), usando referencias absolutas para os parametros.") +
    code("""
        // Aba "Parametros" (celulas travadas nas formulas):
        Meta_TAT        = 30    (celula $B$1)
        Meta_Diaria     = 5     (celula $B$2)

        // Aba "Painel" (sobre TabelaLaudos):
        Total requisicoes  = CONT.VALORES(TabelaLaudos[id_requisicao])
        Backlog pendente   = CONT.SE(TabelaLaudos[status]; "Pendente")
        TAT medio geral   = MEDIA(TabelaLaudos[dias_uteis])
        TAT mediano        = MED(TabelaLaudos[dias_uteis])
        Requisicoes por setor = SOMASE(TabelaLaudos[setor]; "Toxicologia"; TabelaLaudos[dias_uteis])
        % dentro da meta   = CONT.SE(TabelaLaudos[dias_uteis]; "<="&$B$1) / CONT.NUM(TabelaLaudos[dias_uteis])
        """, "excel") +
    step([
        ("Separe a aba Parametros", "Crie uma aba chamada <code>Parametros</code> com Meta_TAT = 30 e "
         "outras constantes do laboratorio."),
        ("Trave as referencias", "Em toda formula que usa um parametro, posicione o cursor sobre a "
         "celula e pressione F4 ate aparecer <code>$B$1</code>."),
        ("Valide com amostra", "Filtre a TabelaLaudos manualmente por status = Pendente e compare "
         "com <code>=CONT.SE(status;\"Pendente\")</code>."),
        ("Formate", "TAT em dias (0 decimal); porcentagem com 1 casa."),
    ]) +
    callout("err", "Parametro na mesma aba dos dados",
        "Nao misture parametros com a base de dados. Se a base crescer e a tabela se expandir, a "
        "celula do parametro pode ser empurrada — e a formula quebra. Aba separada e mais seguro.")
)

cad.section("lab5", "Lab 5 — Filtros e ordenacao personalizada (painel do diretor)",
    p("Objetivo: reproduzir, em 10 segundos, a lista de laudos criticos para a reuniao das 8h "
      "usando a TabelaLaudos (dataset <code>requisicoes_periciais.csv</code>).") +
    step([
        ("Ative os filtros", "Ctrl+Shift+L na TabelaLaudos. As setas aparecem nos cabecalhos."),
        ("Filtre ATRASO CRITICO", "Na coluna Status_Prazo, filtre apenas \"ATRASO CRITICO\"."),
        ("Ordene por antiguidade", "Ordene por data_recebimento crescente — os mais antigos primeiro."),
        ("Leve a lista", "Selecione as linhas filtradas, copie e cole na pauta da reuniao — "
         "sao os casos a cobrar primeiro."),
    ]) +
    ficha("g", "Resultado esperado",
        "Uma lista curta, priorizada por antiguidade, contendo apenas os casos em atraso "
        "critico. Sem macro, sem codigo: tres cliques e a inteligencia da planilha.")
)

cad.section("painel-backlog", "Lab integrador — o painel de backlog completo",
    p("Ao final do Dia 2, cada participante deve ser capaz de construir o painel basico de gestao de "
      "laudos da POLITEC/MT em uma planilha estruturada, combinando tudo o que vimos — usando "
      "o dataset <code>requisicoes_periciais.csv</code> como fonte.") +
    step([
        ("Estruturar a base", "Importe <code>requisicoes_periciais.csv</code> e crie TabelaLaudos "
         "com Ctrl+T. Colunas: id_requisicao, data_recebimento, delegacia_origem, tipo_exame, "
         "setor, perito_responsavel, status, data_laudo, dias_uteis."),
        ("Criar Status_Prazo",
         "<code>=SE(data_laudo=\"\";\"Em andamento\";SE(HOJE()-data_recebimento>60;\"ATRASO CRITICO\";"
         "SE(HOJE()-data_recebimento>30;\"Atencao\";\"No prazo\")))</code>"),
        ("Aplicar o semaforo", "Formatacao condicional na coluna Status_Prazo: No prazo (verde) / "
         "Atencao (amarelo) / ATRASO CRITICO (vermelho), com regras em cascata."),
        ("Criar os indicadores", "Em aba separada: CONT.SE para backlog pendente, MEDIA para TAT medio, "
         "SOMASE para requisicoes por setor. Usar referencias absolutas nos parametros."),
        ("Montar o painel visual", "KPIs no topo (backlog, TAT medio, % no prazo) e a "
         "TabelaLaudos filtravel logo abaixo."),
        ("Filtrar e ordenar", "Aplicar filtro por cor (vermelho = ATRASO CRITICO) para gerar a fila "
         "de prioridades da reuniao das 8h."),
    ]) +
    kpi([("=CONT.SE", "Backlog"), ("=MEDIA", "TAT medio"), ("=SOMASE", "Req/setor"), ("Semaforo", "TAT")]) +
    callout("tip", "Entregavel do dia",
        "Guarde este arquivo: no Dia 4 ele vira a <b>fonte do Power BI</b>. Nomeie como "
        "<code>Laudos_POLITEC_2025.xlsx</code> — a convencao de versionamento ensinada na "
        "governanca.")
)

cad.section("lab6-auditoria-base", "Lab 6 — Auditoria de base suja (limpeza)",
    p("Objetivo: aplicar o kit de limpeza ao dataset <code>requisicoes_periciais.csv</code> "
      "simulando os defeitos classicos de bases exportadas de sistemas legados.") +
    step([
        ("Duplique a aba", "Renomeie a aba original para <code>Base_Bruta</code> e duplique "
         "para <code>Base_Limpa</code>."),
        ("Verifique datas", "Confirme que data_recebimento e data_laudo estao alinhadas a direita "
         "(numerico). Se alguma estiver a esquerda, use <code>=DATA.VALOR(B2)</code> para corrigir."),
        ("Limpe textos", "<code>=ARRUMAR(delegacia_origem)</code> para espacos das bordas; "
         "<code>=PRI.MAIUSCULA(ARRUMAR(delegacia_origem))</code> para capitalizacao padrao."),
        ("Verifique duplicatas", "Coluna auxiliar: <code>=CONT.SE($A$2:$A$121; id_requisicao)</code>. "
         "Se algum retornar mais de 1, a requisicao esta duplicada."),
        ("Valide as contagens", "Compare <code>=CONT.VALORES(id_requisicao)</code> antes e depois "
         "da limpeza; registre quantas linhas foram alteradas."),
        ("Converta em Tabela", "Ctrl+T na base ja limpa; nomeie <code>TabelaLaudos</code>."),
    ]) +
    code("""
        // Verificacao de qualidade (colunas auxiliares na aba Base_Limpa):
        =E.NUMERO(data_recebimento)                    // FALSO = data em texto
        =E.NUMERO(data_laudo)                         // FALSO = data em texto
        =ARRUMAR(delegacia_origem)<>delegacia_origem  // VERDADEIRO = espacos extras
        =CONT.SE($A$2:$A$121; id_requisicao)>1        // VERDADEIRO = duplicado

        // Resumo da auditoria:
        =CONT.SE(aux_verificacao; VERDADEIRO)          // quantos defeitos encontrados
        """, "excel") +
    callout("err", "Limpar sem antes duplicar a aba",
        "Nunca limpe a base original diretamente. Duplique a aba (<i>Base_Bruta</i> e "
        "<i>Base_Limpa</i>) para preservar o dado de entrada — a cadeia de custodia dos dados "
        "comeca aqui.")
)

cad.section("lab7-consolidacao", "Lab 7 — Consolidando 4 planilhas de setores",
    p("Objetivo: reunir 4 planilhas de setores em uma unica base consolidada, pronta para o painel — "
      "e validar que nenhum registro se perdeu. Use os 4 CSVs reais do dataset: o de "
      "<code>requisicoes_periciais.csv</code> ja contem todos os setores.") +
    step([
        ("Entenda a estrutura", "O dataset <code>requisicoes_periciais.csv</code> ja tem todos os "
         "setores (Toxicologia, Genetica, Balistica, Patologia, Identificacao) em uma unica base. "
         "Para simular a consolidacao, separe mentalmente cada setor em uma planilha propria."),
        ("Crie a aba Setores", "Copie cada conjunto de linhas para uma aba diferente: "
         "<code>Setor_Toxicologia</code>, <code>Setor_Genetica</code>, <code>Setor_Balistica</code>, "
         "<code>Setor_Patologia</code>."),
        ("Adicione a coluna Origem", "Em cada aba de setor, adicione a coluna <code>Setor_Origem</code> "
         "com o nome do setor."),
        ("Empilhe na aba Base", "Cole todas as linhas em uma unica aba, sem repetir o cabecalho."),
        ("Converta em Tabela", "Ctrl+T e nomeie <code>TabelaConsolidada</code>."),
        ("Valide por setor", "Conte com <code>=CONT.SE(Setor_Origem;\"Toxicologia\")</code> e "
         "compare com a contagem original da aba de Toxicologia."),
    ]) +
    kpi([("4", "Setores simulados"), ("1", "Base consolidada"),
         ("9", "Colunas totais"), ("100%", "Validacao por CONT.SE")]) +
    callout("tip", "Este e o embriao do ETL",
        "O que voce fez aqui manualmente — padronizar, empilhar, adicionar origem, validar — e "
        "exatamente o que o <b>Power Query</b> fara automaticamente no Dia 3/4. Hoje voce entende "
        "o passo; depois, ele vira um clique em Atualizar.")
)


# =================================================================
# PARTE 4 - CENARIOS
# =================================================================
cad.grp("Parte 4 · Cenarios e aplicacoes praticas",
        "Quatro casos completos da POLITEC: problema, indicadores, passos e desafio.")

cad.section("cenario-orcamento-reagentes", "Cenario A — O orcamento anual de reagentes",
    p("Problema: o laboratorio precisa montar o orcamento de reagentes do proximo ano fiscal com "
      "base no dataset <code>orcamento_setores.csv</code> (36 linhas: 6 laboratorios x 6 rubricas). "
      "O orcamento anterior estourou por um erro de referencia.") +
    kpi([("36", "Linhas de orcamento"), ("6", "Rubricas por laboratorio"),
         ("30%", "Estouro evitado com F4"), ("R$ 0", "Custo do erro corrigido na origem")]) +
    tbl(["Passo", "O que fazer", "Ferramenta"],
        [["1", "Criar a aba <code>Parametros</code> com meta de gasto e tolerancia.", "Arquitetura de abas"],
         ["2", "Estruturar o CSV em Tabela Estruturada (Ctrl+T).", "Ctrl+T"],
         ["3", "Calcular o % deexecucao travando os parametros.", "F4 / nome definido"],
         ["4", "Somar o realizado por laboratorio com SOMASE.", "SOMASE / SOMASES"],
         ["5", "Comparar orcado vs realizado com grafico.", "Coluna calculada + bar_chart"]],
        num_cols=[]) +
    step([
        ("Importe o dataset", "Abra <code>orcamento_setores.csv</code>: colunas laboratorio, rubrica, "
         "orcado, realizado."),
        ("Calcule o % de execucao", "<code>=realizado / orcado</code> em uma nova coluna "
         "<code>Pct_Execucao</code>. Formate como %."),
        ("Identifique estouro", "Use formatacao condicional: vermelho se > 100%, amarelo se > 85%."),
        ("Some por laboratorio", "<code>=SOMASE(laboratorio; \"Genetica\"; realizado)</code>."),
        ("Calcule o total geral", "<code>=SOMA(realizado)</code> sobre a tabela inteira."),
    ]) +
    bar_chart(["Toxicologia", "Genetica", "Balistica", "Patologia", "Identificacao", "Quimica"],
              [38200, 29500, 22800, 31200, 18400, 15600],
              title="Realizado por laboratorio (R$)",
              subtitulo="Dados de orcamento_setores.csv. Patologia e Toxicologia estao acima de 80% do orcado.",
              destaque=0) +
    ficha("p", "Desafio do cenario",
        "Crie uma coluna <code>Variacao</code> que calcule <code>=(realizado - orcado) / orcado</code> "
        "e pinte com semaforo. Depois use <code>SOMASES</code> para filtrar laboratorios que "
        "estouraram em reagentes (rubrica = \"Reagentes\").") +
    callout("err", "Parametro solto no orcamento", "Um unico cifrao faltando desloca o custo em "
        "centenas de itens. O orcamento estoura no fim do ano sem que ninguem perceba durante o "
        "preenchimento.") +
    ficha("g", "O que este cenario ensina",
        "Orcamento seguro = parametros centralizados + referencias travadas + validacao por setor. "
        "O mesmo padrao serve para qualquer planilha de custos da POLITEC.")
)

cad.section("cenario-fila-criticos", "Cenario B — A fila de laudos criticos para a reuniao das 8h",
    p("Problema: o Diretor quer, todas as manhas as 8h, a lista dos laudos criticos priorizada por "
      "gravidade do crime e antiguidade. Hoje a equipe monta essa lista manualmente em 40 minutos.") +
    kpi([("40 min", "Tempo manual por dia"), ("10 s", "Tempo com a planilha"),
         ("3", "Faixas do semaforo"), ("3", "Cliques para a lista")]) +
    flow_h([
        ("\U0001f9f9", "Base limpa"),
        ("\U0001f534", "Filtro vermelho"),
        ("\U0001f522", "Ordenar prioridade"),
        ("\u2705", "Lista 8h"),
    ]) +
    step([
        ("Prepare a base", "TabelaLaudos estruturada, com coluna <code>Gravidade</code> e coluna TAT."),
        ("Crie a lista personalizada", "Homicidio/Crime Sexual; Roubo/Trafico; Furto/Demais."),
        ("Aplique o semaforo", "TAT verde/amarelo/vermelho nas regras em cascata."),
        ("Filtre por cor", "Filtrar por Cor \u2192 Vermelho na coluna TAT."),
        ("Ordene", "Ordenacao Personalizada pela gravidade; depois Data_Recebimento crescente."),
        ("Distribua", "Copie a lista para a pauta da reuniao ou imprima."),
    ]) +
    tbl(["Prioridade", "Criterio", "Acao na reuniao"],
        [["\U0001f534 Critico", "TAT &gt; 60 dias", "Cobranca imediata do setor responsavel."],
         ["\U0001f7e0 Alto", "31 a 60 dias + crime grave", "Monitorar e redistribuir carga."],
         ["\U0001f7e1 Padrao", "No prazo", "Acompanhar no fluxo normal."]],
        num_cols=[]) +
    callout("err", "Ordenar so por data e ignorar a gravidade",
        "Se a fila for ordenada apenas por antiguidade, um homicidio recente pode ficar atras de "
        "furtos antigos. A lista personalizada resolve isso — a prioridade institucional vence a "
        "data.") +
    ficha("a", "Desafio do cenario",
        "Automatize o envio: use a coluna <code>Situacao</code> e um filtro para gerar, no inicio do "
        "dia, apenas os casos que <b>entraram</b> em atraso critico desde ontem. Quem cruzou a "
        "linha das 8h e o foco da reuniao.")
)

cad.section("cenario-produtividade-perito", "Cenario C — Painel de produtividade por perito",
    p("Problema: distribuir a carga de trabalho de forma justa e detectar peritos sobrecarregados "
      "ou ociosos. Hoje a percepcao e subjetiva: 'parece que todo mundo esta no limite'. "
      "Usamos o dataset <code>produtividade_peritos.csv</code> com 218 registros de 9 meses.") +
    bar_chart(["Silva, A. P.", "Souza, M. F.", "Almeida, C. R.", "Costa, J. L.",
                "Oliveira, R. S.", "Lima, P. H.", "Ferreira, T. A.", "Martins, K. B."],
              [156, 142, 128, 98, 167, 119, 134, 101],
              title="Total de laudos por perito (9 meses de 2025)",
              subtitulo="Meta acumulada = 315 laudos (35/mês x 9). Costa (98) e Lima (119) estao abaixo da meta — investigar.",
              destaque=3) +
    tbl(["Indicador", "Formula", "Leitura"],
        [["Laudos por perito", "<code>=SOMASE(perito; \"Silva, A. P.\"; laudos_concluidos)</code>", "Total acumulado do perito."],
         ["Media mensal", "<code>=SOMASE(...) / 9</code>", "Media de laudos por mes."],
         ["% da meta", "<code>=Total / 315</code>", "Atingimento do compromisso acumulado."],
         ["Ranking", "<code>=ORDEM(Celha; range)</code>", "Posicao relativa entre os peritos."]],
        num_cols=[]) +
    step([
        ("Importe o dataset", "Abra <code>produtividade_peritos.csv</code> e crie "
         "<code>TabelaProdutividade</code> com Ctrl+T."),
        ("Some por perito", "<code>=SOMASE(perito; \"Costa, J. L.\"; laudos_concluidos)</code> para cada perito."),
        ("Calcule a meta acumulada", "Meta mensal = 35. Meta de 9 meses = 315 laudos."),
        ("Calcule o % de atingimento", "<code>=Total / 315</code>. Abaixo de 80% = zona de alerta."),
        ("Decida com dados", "Redistribua a carga com base nos numeros, nao na percepcao."),
    ]) +
    aplicab(
        "No fechamento mensal de produtividade da equipe pericial.",
        "Porque a percepcao de carga nao mede o volume real nem a complexidade dos casos.",
        "Costa tem 98 laudos (31% da meta acumulada) — possivel sobrecarga ou afastamento. "
        "So os dados dizem.") +
    ficha("p", "Desafio do cenario",
        "Cruze produtividade com o TAT medio: um perito que entrega muitos laudos, mas com TAT "
        "acima de 60 dias, pode estar cometendo erros por pressa. Use "
        "<code>SOMASE(perito; \"Costa\"; dias_uteis) / SOMASE(perito; \"Costa\"; 1)</code> para "
        "calcular o TAT medio individual.")
)

cad.section("cenario-auditoria-qualidade", "Cenario D — Auditoria de qualidade da base",
    p("Problema: antes de publicar o relatorio gerencial, o gestor precisa garantir que a base nao "
      "tem defeitos: celulas mescladas, datas como texto, duplicatas e valores fora de faixa.") +
    kpi([("4", "Tipos de defeito"), ("0", "Células mescladas aceitaveis"),
         ("100%", "Datas numericas"), ("0", "Duplicatas pela chave")]) +
    tbl(["Defeito", "Como detectar", "Como corrigir"],
        [["<b>Celulas mescladas</b>", "Localizar e Selecionar \u2192 Celulas Mescladas.",
          "Desmesclar e preencher os rotulos."],
         ["<b>Datas como texto</b>", "Datas alinhadas a esquerda; <code>=E.NUMERO(...)</code> falso.",
          "Texto para Colunas ou <code>=DATA.VALOR()</code>."],
         ["<b>Duplicatas</b>", "<code>=CONT.SE(chave;chave)&gt;1</code> em coluna auxiliar.",
          "Remover Duplicatas pela chave."],
         ["<b>Valores fora de faixa</b>", "Formatacao condicional em pesos/custos.",
          "Corrigir ou excluir o registro invalido."],
         ["<b>Espacos extras</b>", "<code>=ARRUMAR(celula)&lt;&gt;celula</code>.",
          "Aplicar <code>=ARRUMAR()</code> e colar como valores."]],
        num_cols=[]) +
    step([
        ("Detecte mesclagens", "Procure celulas mescladas na area de dados; qualquer uma e um risco "
         "a filtros e formulas."),
        ("Valide as datas", "Use uma coluna auxiliar <code>=E.NUMERO(A2)</code>: se retornar FALSO, "
         "a data e texto."),
        ("Encontre duplicatas", "Coluna auxiliar <code>=CONT.SE($A$2:$A$1000;A2)&gt;1</code>."),
        ("Verifique as faixas", "Formatacao condicional para custos negativos ou pesos absurdos."),
        ("Documente", "Anote quantos defeitos foram encontrados e corrigidos — auditabilidade."),
        ("So entao publique", "Uma base aprovada na auditoria vira um relatorio confiavel."),
    ]) +
    code("""
        // Checklist de qualidade em colunas auxiliares:
        =E.NUMERO(A2)                              // FALSO = data em texto
        =CONT.SE($A$2:$A$1000; A2)>1               // VERDADEIRO = duplicado
        =ARRUMAR(A2)<>A2                           // VERDADEIRO = tem espaco extra
        =OU(B2<0; B2>10000)                        // VERDADEIRO = valor suspeito

        // Resumo da auditoria:
        =CONT.SE(aux; VERDADEIRO)                  // quantos defeitos de cada tipo
        """, "excel") +
    callout("err", "Publicar sem auditoria",
        "Um relatorio publicado com defeitos de estrutura e pior do que um relatorio atrasado: ele "
        "destroi a credibilidade do dado. A auditoria de qualidade e tao obrigatoria quanto o "
        "semaforo do TAT.") +
    ficha("r", "Desafio do cenario",
        "Crie uma <b>aba de auditoria</b> que some todos os defeitos por coluna e retorne um "
        "semáforo geral da base: verde (zero defeitos), amarelo (defeitos tratáveis) e vermelho "
        "(base contaminada). Ninguem publica sem o verde.")
)


# =================================================================
# PARTE 5 - BOAS PRATICAS E FECHAMENTO
# =================================================================
cad.grp("Parte 5 · Boas praticas, governanca e fechamento",
        "Erros que contaminam relatorios, nomenclatura, governanca, quiz, glossario e referencias.")

cad.section("erros-comuns", "Erros comuns e como evita-los",
    p("Os erros mais frequentes em planilhas periciais nao sao de formula — sao de <b>estrutura</b>. "
      "Identifique-os antes que contaminem os relatorios gerenciais.") +
    grid2([
        ("\u274c Celulas mescladas",
         "Mesclar parece organizado, mas quebra filtros, ordenacoes e formulas de contagem. Nunca "
         "mescle celulas em uma base de dados — use apenas em titulos visuais."),
        ("\u274c Datas como texto",
         "Se a data foi importada como texto, o calculo de TAT retorna erro. Verifique se a data esta "
         "alinhada a direita (numerico)."),
        ("\u274c Ausencia de referencia absoluta",
         "Copiar formulas sem travar parametros (preco, prazo, taxa) e a causa do deficit de 30% do "
         "caso real. Use F4 sempre."),
        ("\u274c Dados misturados em uma coluna",
         "Colocar Toxicologia - 30 dias em uma celula mistura tipo e prazo. Cada informacao deve "
         "ter sua propria coluna."),
    ]) +
    ficha("r", "O principio unico",
        "Uma celula, um dado. Uma coluna, um tipo de informacao. Um parametro, uma celula travada. "
        "Essas tres regras evitam a maioria dos erros de planilha.")
)

cad.section("nomenclatura", "Boas praticas de nomenclatura e arquitetura",
    p("Uma planilha profissional comeca antes das formulas — comeca na convencao de nomes e na "
      "arquitetura das abas. Estabeleca um padrao e <b>documente-o</b>.") +
    tbl(["Nomenclatura de colunas", "Arquitetura de abas"],
        [["Sem espacos: <code>Data_Recebimento</code>, nao Data Recebimento.", "<b>Base</b> — dados brutos, nunca editar manualmente."],
         ["Sem caracteres especiais: evite acentos em nomes de tabela.", "<b>Painel</b> — indicadores calculados e semaforos."],
         ["Descritivos e curtos: <code>TAT_Dias</code>, <code>Tipo_Exame</code>, <code>Status_Laudo</code>.", "<b>Parametros</b> — metas, precos e taxas (com referencias absolutas)."],
         ["Padronize a nomenclatura de categorias (ex.: sempre Arma de Fogo).", "<b>Historico</b> — dados de meses anteriores para comparacao."]],
        num_cols=[]) +
    callout("note", "Por que padronizar categorias",
        "Lembre do Dia 1: padronizar Arma de Fogo (em vez de Revolver, arma, rvl) "
        "pode aumentar em ate <b>40%</b> a eficacia dos cruzamentos estatisticos.")
)

cad.section("sheets-excel", "Google Sheets x Excel na POLITEC",
    p("Ambas as ferramentas suportam todas as funcoes apresentadas neste modulo. A escolha depende "
      "do ambiente e das necessidades de colaboracao da equipe.") +
    tbl(["Criterio", "Excel", "Google Sheets"],
        [["Funcoes do dia", "Todas disponiveis", "Todas disponiveis (sintaxe com virgula)"],
         ["Colaboracao simultanea", "Limitada (co-autoria no 365)", "Nativa — varias pessoas ao mesmo tempo"],
         ["Permissoes por e-mail", "Via OneDrive/SharePoint", "Nativo, granular"],
         ["Atalho F4 (cifrao)", "Cicla os 4 modos", "Digitacao manual do $"],
         ["Versionamento", "Local, com nome de arquivo", "Historico de versoes automatico"],
         ["Dados sensiveis", "Controle por senha de arquivo", "Controle por compartilhamento"]],
        num_cols=[]) +
    callout("tip", "Escolha pelo contexto",
        "Equipe distribuida e colaboracao em tempo real: <b>Sheets</b>. Bases maiores, macros e "
        "integracao com Power BI: <b>Excel</b>. O importante e padronizar uma ferramenta por base "
        "para nao criar versoes concorrentes.")
)

cad.section("governanca", "Governanca: a planilha como documento oficial",
    p("No contexto da POLITEC/MT, a planilha de controle de laudos pode ser solicitada em auditorias, "
      "processos judiciais e prestacoes de contas ao <b>TCE-MT</b>. A qualidade dos dados e tao "
      "importante quanto a qualidade tecnica do laudo pericial.") +
    legenda([
        ("\U0001f5c2\ufe0f", "Versionamento", "Salve versoes mensais com data no nome: "
         "<code>Laudos_POLITEC_2024_01.xlsx</code>. Nunca sobrescreva a base historica — o passado e auditavel."),
        ("\U0001f512", "Controle de acesso", "Proteja as abas Base e Parametros com senha. Permita "
         "edicao apenas nas abas de entrada. No Sheets, use permissoes por e-mail."),
        ("\U0001f4dd", "Auditabilidade", "Mantenha um log de alteracoes na aba Historico: quem "
         "alterou, o que e quando. Dados periciais tem cadeia de custodia — inclusive os digitais."),
    ]) +
    ficha("p", "A frase do professor",
        "Uma planilha bem estruturada e a <b>cadeia de custodia dos seus dados</b>. Se a base esta "
        "suja ou desorganizada, o laudo gerencial estara contaminado. — Prof. Renato Rosa.")
)

cad.section("atalhos", "Atalhos essenciais para o dia a dia pericial",
    p("Dominar atalhos multiplica a velocidade de trabalho. No contexto pericial, onde relatorios "
      "precisam ser gerados rapidamente, cada segundo conta.") +
    tbl(["Atalho", "Acao"],
        [["<kbd>Ctrl</kbd> + <kbd>T</kbd>", "Criar Tabela Estruturada"],
         ["<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>L</kbd>", "Ativar/desativar Filtros"],
         ["<kbd>F4</kbd>", "Travar Referencia ($) — cicla os 4 modos"],
         ["<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>\u2193</kbd>", "Selecionar ate o fim dos dados"],
         ["<kbd>Alt</kbd> + <kbd>H</kbd> + <kbd>L</kbd>", "Formatacao Condicional"],
         ["<kbd>Ctrl</kbd> + <kbd>;</kbd>", "Inserir a data de hoje (fixa)"],
         ["<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>;</kbd>", "Inserir a hora atual (fixa)"],
         ["<kbd>Ctrl</kbd> + <kbd>Z</kbd>", "Desfazer (sempre seu aliado)"]],
        num_cols=[])
)

cad.section("checklist", "Checklist do gestor: planilha pericial segura",
    p("Antes de compartilhar qualquer planilha gerencial com a lideranca da POLITEC/MT, verifique "
      "estes itens.") +
    checklist([
        "Dados organizados em Tabela Estruturada (Ctrl+T).",
        "Parametros fixos travados com referencia absoluta ($).",
        "Formatacao condicional (semaforo do TAT) aplicada e funcionando.",
        "Formulas CONT.SE e SOMASE validadas com uma amostra dos dados.",
        "Ordenacao personalizada configurada por prioridade de crime.",
        "Aba de Parametros separada da aba de Base de Dados.",
        "Nenhuma celula mesclada na area de dados.",
        "Datas verificadas como formato numerico (nao texto).",
        "Contagens antes/depois conferidas na limpeza e na consolidacao.",
        "Filtros limpos antes de salvar e compartilhar.",
    ]) +
    callout("tip", "Passe o checklist antes de enviar",
        "Dez itens marcados = planilha pronta para circular. Qualquer item em branco e um risco de "
        "retrabalho ou de dado contaminado no relatorio.")
)

cad.section("quiz", "Quiz final do Dia 2 (15 perguntas)",
    q("Para somar o custo de reagentes <b>apenas</b> do setor de Toxicologia, a funcao correta e:",
      ["=SOMA(E2:E100)", "=SOMASE(C2:C100;\"Toxicologia\";E2:E100)",
       "=CONT.SE(C2:C100;\"Toxicologia\")", "=MEDIA(E2:E100)"], 1,
      "SOMASE soma condicionalmente: criterio na coluna C, valores na coluna E.") +
    q("Qual atalho transforma um intervalo em Tabela Estruturada?",
      ["Ctrl+L", "Ctrl+T", "F4", "Ctrl+Shift+L"], 1,
      "Ctrl+T cria a tabela; Ctrl+Shift+L liga os filtros.") +
    q("A funcao CONT.NUM() conta:",
      ["Qualquer celula preenchida", "Somente celulas com valores numericos",
       "Apenas celulas vazias", "Somente texto"], 1,
      "Para contar datas/numeros validos (ex.: laudos com TAT registrado), use CONT.NUM.") +
    q("O atalho F4, durante a edicao de uma formula, serve para:",
      ["Excluir a formula", "Ciclar entre referencia relativa e absoluta ($)",
       "Inserir uma funcao", "Formatar a celula"], 1,
      "F4 alterna A1 -> $A$1 -> A$1 -> $A1. Trava parametros fixos.") +
    q("No semaforo do TAT, a cor vermelha corresponde a:",
      ["Ate 30 dias", "Entre 31 e 60 dias", "Mais de 60 dias", "Laudo em andamento"], 2,
      "Mais de 60 dias = atraso critico, exige acao imediata.") +
    q("Por que nunca mesclar celulas em uma base de dados?",
      ["Deixa o arquivo mais pesado", "Quebra filtros, ordenacoes e contagens",
       "O Excel proibe em qualquer versao", "Impede o uso de cores"], 1,
      "Mesclagem atrapalha a estrutura tabular da base.") +
    q("O Fantasma de Heilbronn foi resolvido porque o analista:",
      ["Contratou mais peritos", "Ordenou pelo lote do swab e filtrou os positivos",
       "Comprou um supercomputador", "Ignorou os outliers"], 1,
      "A contaminacao estava no lote dos cotonetes, visivel ao ordenar/filtrar a base.") +
    q("Uma Tabela Estruturada permite escrever formulas:",
      ["So com referencias como C2:C100", "Com nomes de coluna, ex.: TabelaLaudos[Tipo_Exame]",
       "Apenas com macros", "Sem nenhuma referencia"], 1,
      "Nomes de coluna deixam a formula legivel e imune ao crescimento da base.") +
    q("Quando migrar a analise para Power Query ou Power BI?",
      ["Sempre, mesmo com 100 linhas", "Quando a base se aproxima de 50.000-100.000 linhas",
       "Nunca; planilha da conta de tudo", "Somente se nao houver internet"], 1,
      "Acima desse volume, formulas e formatacao condicional tornam a planilha lenta.") +
    q("A funcao MED() e mais robusta que MEDIA() quando:",
      ["Nao ha numeros", "Existem casos extremos (outliers)",
       "A base tem so texto", "A coluna esta vazia"], 1,
      "A mediana resiste a outliers; a media e puxada por eles.") +
    q("Para contar exames de DNA que estao pendentes, usa-se:",
      ["CONT.SE(B:B;\"Pendente\")", "CONT.SES(B:B;\"Pendente\";C:C;\"DNA\")",
       "SOMASE(B:B;\"Pendente\";C:C)", "MEDIA(C:C)"], 1,
      "Sao dois criterios simultaneos: status Pendente E tipo DNA -> CONT.SES.") +
    q("A referencia mista <code>$A1</code> trava:",
      ["A linha e a coluna", "Somente a coluna", "Somente a linha", "Nada"], 1,
      "$A1 trava a coluna A; a linha 1 permanece relativa.") +
    q("O erro <code>#VALOR!</code> normalmente indica:",
      ["Divisao por zero", "Tipo incompativel (ex.: subtrair data que e texto)",
       "Funcao digitada errada", "Referencia a celula excluida"], 1,
      "Subtrair datas armazenadas como texto e a causa mais comum na POLITEC.") +
    q("Filtrar por cor so funciona se antes voce tiver aplicado:",
      ["Uma tabela dinamica", "A formatacao condicional",
       "Um grafico de barras", "Uma macro"], 1,
      "O filtro por cor isola as cores criadas pela formatacao condicional.") +
    q("Segundo a licao do modulo, dados periciais tem:",
      ["Apenas valor contabil", "Cadeia de custodia — inclusive os digitais",
       "Valor so se forem numericos", "Nenhuma exigencia de auditoria"], 1,
      "A planilha de laudos e documento oficial e precisa ser auditavel.")
)

cad.section("glossario", "Glossario pericial de planilhas",
    glossary([
        ("TAT — Turnaround Time", "Tempo entre o recebimento da requisicao pericial e a entrega do laudo finalizado. Calculado com MEDIA/mediana sobre a diferenca entre datas."),
        ("Backlog", "Fila de exames aguardando processamento. Monitorado com CONT.SE(status;\"Pendente\")."),
        ("Mediana (MED)", "Valor central de uma fila ordenada. Robusta a outliers; reportada junto com a media."),
        ("Desvio padrao", "Medida de dispersao dos prazos. Indica a consistencia operacional do laboratorio."),
        ("Referencia Absoluta ($)", "Travamento de celula em formulas — impede que parametros fixos (precos, metas) se movam ao copiar. Atalho: F4."),
        ("Referencia Mista", "Trava apenas linha ou apenas coluna ($A1 ou A$1). Usada em matrizes de cruzamento."),
        ("Intervalo nomeado", "Intervalo batizado (ex.: Meta_TAT) para substituir referencias cifradas e deixar a formula legivel."),
        ("Tabela Estruturada", "Intervalo convertido em objeto de banco de dados dentro do Excel (Ctrl+T): expansao automatica, filtros nativos e formulas por nome de coluna."),
        ("[@[coluna]]", "Notacao que referencia o valor da linha atual de uma coluna dentro da Tabela Estruturada."),
        ("Formatacao Condicional", "Cor automatica conforme o valor ou uma formula. Base do semaforo do TAT."),
        ("CONT.SE / SOMASE", "Contagem e soma condicionais por um criterio. CONT.SES/SOMASES combinam varios criterios."),
        ("SES", "Funcao que substitui o SE aninhado com pares condicao/resultado, mais legivel em versoes recentes."),
        ("Semaforo do TAT", "Regra visual verde (<=30), amarelo (31-60) e vermelho (>60) aplicada a coluna de TAT."),
        ("Ordenacao personalizada", "Ordem logica definida pelo gestor (ex.: gravidade do crime), independente do alfabeto ou do numero."),
        ("Filtro por cor", "Filtro que isola as cores criadas pela formatacao condicional; usado para achar atrasos criticos."),
        ("Power Query", "Ferramenta de transformacao/limpeza de dados dentro do Excel, para volumes maiores e automacao do ETL."),
        ("Coluna calculada x Medida", "Coluna calculada: um valor por linha. Medida: um valor agregado que resume muitas linhas (prepara o vocabulario do Power BI)."),
        ("ETL", "Extract, Transform, Load — padrao de extracao, limpeza e carga de dados que sustenta o BI."),
    ]) +
    tbl(["Indicador do dia", "Formula", "Significado"],
        [["Backlog pendente", "CONT.SE(...;\"Pendente\")", "Exames aguardando processamento."],
         ["TAT medio", "MEDIA(TAT_Dias)", "Tempo medio de emissao de laudo."],
         ["TAT mediano", "MED(TAT_Dias)", "Tempo tipico, imune a outliers."],
         ["Custo por setor", "SOMASE(...)", "Gasto isolado por laboratorio."],
         ["% dentro da meta", "CONT.SE(<=meta)/CONT.NUM", "Taxa de conformidade com o prazo."]],
        num_cols=[])
)

cad.section("referencias", "Referencias e ponte para o Dia 3",
    p("As referencias que sustentam o Dia 2:") +
    tbl(["Autor", "Obra", "Por que importa"],
        [["Bill Jelen (MrExcel)", "Dezenas de livros de Excel avancado",
          "Referencia mundial em automacao e gestao com planilhas. mrexcel.com."],
         ["Wayne Winston", "\"Microsoft Excel Data Analysis and Business Modeling\"",
          "Referencia academica sobre funcoes logicas como sistemas de alerta precoce."],
         ["Ralph Kimball", "Obras sobre modelagem dimensional e Data Warehouse",
          "Contexto da transicao da planilha para o BI (Power BI, Dia 4)."]],
        num_cols=[]) +
    ficha("g", "Proximo passo — Dia 3",
        "O Dia 3 foca em <b>garantir que dados de qualidade entrem na planilha</b> e em comunicar os "
        "resultados visualmente: <b>validacao de dados</b> (listas suspensas e regras de entrada), "
        "<b>mini-dashboards</b> dentro da propria planilha e <b>organizacao avancada</b> da base "
        "mestra da POLITEC. A base que voce estruturar hoje sera usada nos proximos modulos.")
)

cad.build()

