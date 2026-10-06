# -*- coding: utf-8 -*-
"""Gerador do caderno da Aula 3 - POLITEC/MT.

Tema: Organizacao, Visualizacao e Ferramentas de Analise na Pericia.
Modulos 4 (Organizacao e Visualizacao) e 5 (Ferramentas e Linguagens).
Conteudo derivado dos slides Dia-3-Politec.pdf (55 paginas).

Rode:  python gerar_caderno_aula3.py
PDF:   python ..\\exportar_pdf.py 3
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from caderno_lib import (Caderno, p, h3, ul, checklist, ficha, callout, tbl,
                         code, step, q, aplicab, grid2, flow_h, kpi,
                         antesdepois, legenda, glossary, bar_chart)

cad = Caderno(
    out=str(pathlib.Path(__file__).resolve().parent / "caderno-dia3.html"),
    dia=3,
    kicker="Aula 3 · Organizacao e BI",
    headline="Organizacao, Visualizacao e Ferramentas de Analise na Pericia",
    sub="Da validacao de dados a preparacao para o Business Intelligence: como garantir que o "
        "dado entra limpo, comunicar resultados com graficos honestos e automatizar a limpeza com "
        "ETL e Power Query na rotina da POLITEC/MT.",
    meta="Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 3 · Modulos 4 e 5",
    descricao="Caderno do Dia 3 do Curso de Capacitacao POLITEC/MT: validacao de dados na entrada, "
              "limpeza (ARRUMAR, PRI.MAIUSCULA, SUBSTITUIR), remocao de duplicatas, visualizacao "
              "honesta com Cairo e Tufte, escolha de graficos, mini-painel de gestao pericial, "
              "Excel x Power BI, ETL de Kimball, Power Query e preparacao de bases para BI.",
)

# =================================================================
# ABERTURA
# =================================================================
cad.grp("Abertura", "O proposito do dia, o mapa das partes e os autores de referencia.")

cad.section("boas-vindas", "Bem-vindo ao caderno do Dia 3",
    p("O Dia 3 marca a virada do curso: saimos da logica da planilha isolada e entramos na "
      "<b>gestao de dados como inteligencia institucional</b>. Pela manha (Modulo 4) tratamos de "
      "<b>organizacao e visualizacao</b> — validar na entrada, limpar, escolher o grafico certo. "
      "A tarde (Modulo 5) comparamos <b>Excel x Power BI</b> e aprendemos o <b>ETL</b> e o "
      "<b>Power Query</b>.") +
    p("A ideia central do dia cabe em uma frase: <b>dado sujo e prova contaminada</b>. Na pericia, "
      "um grafico distorcido ou uma base duplicada tem o mesmo peso de uma amostra mal "
      "documentada — compromete a conclusao e a credibilidade do laudo.") +
    legenda([
        ("\U0001f4cb", "Parte 1 — Modulo 4", "Validacao, limpeza, duplicatas, graficos honestos e o mini-painel pericial."),
        ("\U0001f517", "Parte 2 — Modulo 5", "Excel x Power BI, ETL de Kimball, Power Query e preparacao de bases."),
        ("\U0001f9ea", "Parte 3 — Pratica", "6 laboratorios guiados, passo a passo de cliques e atalhos."),
        ("\U0001f3af", "Parte 4 — Cenarios", "4 casos reais da POLITEC com KPIs, visuais e passos."),
        ("\u2705", "Parte 5 — Fechamento", "Resumo, ponte para o Dia 4, tarefa de casa, quiz, glossario e referencias."),
    ]) +
    callout("note", "Como usar este caderno",
        "Cada secao traz um conceito, um exemplo na <b>POLITEC</b> e, quando faz sentido, um passo "
        "a passo de cliques. As respostas do quiz ficam escondidas em <i>Ver resposta</i> e abrem "
        "automaticamente na impressao em PDF.")
)

cad.section("mapa-do-dia", "Mapa do Dia 3: dos dados limpos ao dashboard",
    p("A agenda do dia foi desenhada em dois blocos que se completam: primeiro <b>organizar e "
      "visualizar</b>, depois <b>escolher a ferramenta e automatizar</b>.") +
    grid2([
        ("\U0001f305 Manha (08h-12h) · Modulo 4 — Organizacao e Visualizacao",
         ul(["<b>Validacao de dados</b> na entrada (listas suspensas, datas, limites)",
             "A <b>cadeia de erros</b> ate o risco processual",
             "<b>Limpeza</b>: ARRUMAR, PRI.MAIUSCULA, SUBSTITUIR",
             "<b>Remocao de duplicatas</b> e o custo oculto dos dados sujos",
             "<b>Alberto Cairo</b> e a visualizacao honesta",
             "<b>Edward Tufte</b> e o combate ao chartjunk",
             "O <b>caso do grafico 3D</b> que enganou a todos",
             "<b>Mini-painel</b> de gestao pericial"])),
        ("\U0001f306 Tarde (13h-17h) · Modulo 5 — Ferramentas e Linguagens",
         ul(["<b>Excel x Power BI</b>: paradigma, forcas e limites",
             "Quando usar cada ferramenta",
             "<b>Ralph Kimball</b> e o Data Warehousing",
             "O processo <b>ETL</b> (Extract, Transform, Load)",
             "A migracao da <b>transparencia pericial</b> para portais",
             "Preparacao de bases (<b>4 problemas</b> classicos)",
             "<b>Power Query</b>: limpe uma vez, atualize sempre",
             "Erros comuns de iniciantes no BI"])),
    ]) +
    ficha("g", "Objetivo do dia",
        "Sair capaz de <b>blindar a entrada de dados</b>, <b>limpar bases herdadas</b>, "
        "<b>escolher o grafico certo</b> e <b>automatizar a limpeza</b> com Power Query — "
        "montando, ao final, um mini-painel de gestao pericial que responde as tres perguntas "
        "criticas da direcao.")
)

cad.section("autores-do-dia", "Os autores que sustentam o Dia 3",
    p("Tres nomes aparecem de forma recorrente nos slides e no dia a dia da analise pericial. "
      "Conhecer a ideia central de cada um ajuda a lembrar <i>por que</i> fazemos o que fazemos.") +
    legenda([
        ("\U0001f4d8", "Alberto Cairo", "\"The Truthful Art\": a visualizacao comunica a verdade "
         "operacional. Escala Y no zero, titulo, fonte e cores com significado."),
        ("\U0001f4d0", "Edward Tufte", "\"The Visual Display of Quantitative Information\": "
         "data-ink ratio e a guerra ao <b>chartjunk</b> — sem 3D, sombras ou gradientes."),
        ("\U0001f5c4\ufe0f", "Ralph Kimball", "\"The Data Warehouse Toolkit\": modelagem "
         "dimensional e o processo <b>ETL</b> que sustenta todo sistema de BI moderno."),
    ]) +
    callout("purple", "Por que estes autores importam na POLITEC",
        "Cairo nos protege do grafico enganoso que distorce a gestao; Tufte nos protege do ruido "
        "visual que atrasa a leitura; Kimball nos da a arquitetura para que o dado saia do sistema "
        "legado e chegue confiavel ao dashboard do Diretor.")
)

# =================================================================
# PARTE 1 - MODULO 4
# =================================================================
cad.grp("Parte 1 · Modulo 4 — Organizacao e Visualizacao",
        "Validacao, limpeza, duplicatas e a comunicacao visual honesta dos dados periciais.")

cad.section("cadeia-custodia-digital", "Validacao de dados: a cadeia de custodia digital comeca na entrada",
    p("Na pericia, um dado de entrada incorreto pode gerar um laudo com informacao trocada e causar "
      "<b>nulidade processual</b>. Validar e impedir que dados invalidos ou inconsistentes entrem "
      "na base — e o <b>primeiro elo da cadeia de custodia digital</b>.") +
    grid2([
        ("\U0001f4cb Listas Suspensas (Dropdowns)",
         "Padronizam o <b>Tipo de Exame</b>. Evita que um perito escreva <i>DNA</i>, outro "
         "<i>Genetica</i> e outro <i>Perfil Genetico</i> — o que fragmenta a contagem estatistica."),
        ("\U0001f4c5 Restricao de Datas",
         "As datas de recebimento da requisicao sao limitadas ao passado, impedindo registros "
         "futuros inconsistentes com a realidade processual."),
    ]) +
    grid2([
        ("\U0001f522 Limites Numericos",
         "Campos como <i>Peso da Amostra</i> nao aceitam valores negativos — regras simples que "
         "eliminam erros absurdos antes que contaminem a base."),
        ("\u26a1 Impacto direto",
         "A validacao bem configurada reduz em ate <b>80% o tempo</b> gasto posteriormente com "
         "limpeza de dados. E o melhor investimento de tempo do processo inteiro."),
    ]) +
    callout("err", "Base aceita qualquer coisa",
        "Uma coluna sem validacao aceita <i>qualquer</i> texto. Depois, no fechamento do mes, "
        "ninguem consegue somar a producao porque existem cinco grafias para o mesmo setor.")
)

cad.section("validacao-listas", "Listas suspensas: padronizando o vocabulario pericial",
    p("A lista suspensa (dropdown) e a forma mais simples e mais eficaz de validacao. Ela troca a "
      "digitacao livre por uma <b>escolha controlada</b>, garantindo que o vocabulario da base seja "
      "sempre o mesmo.") +
    aplicab(
        "Quando uma coluna tem um conjunto finito de respostas possiveis (tipo de exame, setor, status).",
        "Porque a maior fonte de fragmentacao de dados e a variacao de escrita humana para a mesma coisa.",
        "A coluna <b>Tipo_Exame</b> so aceita: DNA, Toxicologia, Balistica, Documentoscopia, "
        "Necropsia. Some os exames de DNA sem medo de achar <i>Genetica</i> escondido em outra linha.") +
    step([
        ("Crie a lista em uma area reservada", "Em uma aba de apoio, digite os valores permitidos, "
         "um por linha: DNA, Toxicologia, Balistica, Documentoscopia, Necropsia."),
        ("Selecione a coluna que sera validada", "Clique na coluna <b>Tipo_Exame</b> (ou no "
         "intervalo da coluna, dentro da tabela)."),
        ("Abra a validacao de dados", "No Excel: <kbd>Dados</kbd> \u2192 <kbd>Validacao de Dados</kbd>. "
         "No Sheets: <kbd>Dados</kbd> \u2192 <kbd>Validacao de dados</kbd>."),
        ("Escolha Lista", "Em <i>Permitir</i>, selecione <b>Lista</b> e aponte para o intervalo dos "
         "valores permitidos. Marque <i>Ignorar em branco</i> se fizer sentido."),
        ("Teste a entrada", "Tente digitar uma palavra fora da lista: a ferramenta deve recusar ou "
         "avisar. A base fica protegida."),
    ]) +
    callout("tip", "Aviso x bloqueio",
        "O <b>Aviso de Erro</b> apenas alerta; o <b>Bloqueio</b> impede a digitacao invalida. Para "
        "dados periciais criticos, use o bloqueio. Ele evita o problema em vez de apenas sinaliza-lo.")
)

cad.section("validacao-datas-numeros", "Restricao de datas e limites numericos",
    p("Datas e numeros tambem se validam. Um registro de recebimento no futuro ou um peso negativo "
      "sao <b>impossibilidades fisicas</b> que podem ser impedidas na propria entrada.") +
    tbl(["Tipo de validacao", "Configuracao", "Efeito na POLITEC"],
        [["<b>Data no passado</b>", "Permitir <i>Data</i> \u2192 menor ou igual a <code>=HOJE()</code>",
          "Impede requisicao recebida no futuro, impossivel na realidade processual."],
         ["<b>Intervalo de datas</b>", "Permitir <i>Data</i> \u2192 entre <code>01/01/2020</code> e <code>=HOJE()</code>",
          "Mantem a base dentro da janela historica valida do laboratorio."],
         ["<b>Numero minimo</b>", "Permitir <i>Numero inteiro</i> \u2192 maior ou igual a 0",
          "Bloqueia peso negativo de amostra ou quantidade negativa de itens."],
         ["<b>Teto numerico</b>", "Permitir <i>Decimal</i> \u2192 entre 0 e 1000",
          "Evita digitar um peso de 10.000 g por engano e distorcer os indicadores."]],
        num_cols=[]) +
    code("""
        // Lista de apoio em uma aba Parametros:
        // A2:A6 -> DNA, Toxicologia, Balistica, Documentoscopia, Necropsia

        // Validacao aplicada na coluna Tipo_Exame:
        // Dados > Validacao de Dados > Lista > =Parametros!$A$2:$A$6

        // Regra de data (recebimento no passado):
        // Dados > Validacao de Dados > Data > menor ou igual a > =HOJE()
        """, "excel") +
    callout("err", "Erro de digitacao vira erro de indicador",
        "Sem limite numerico, um peso de <code>10000</code> em vez de <code>100.00</code> desloca "
        "a media do setor. A validacao numerica e a barreira contra o erro mais humano de todos: o dedo.")
)

cad.section("por-que-validar", "Por que validar na entrada? A cadeia de erros",
    p("O custo de corrigir um erro <b>cresce exponencialmente</b> conforme ele avanca no fluxo de "
      "trabalho. Um campo digitado errado na entrada gera analises erradas, laudos incorretos e "
      "relatorios que distorcem a realidade operacional da POLITEC.") +
    flow_h([
        ("\u270f\ufe0f", "Entrada invalida"),
        ("\U0001f9e9", "Base fragmentada"),
        ("\U0001f4c9", "Estatistica distorcida"),
        ("\u2696\ufe0f", "Risco processual"),
    ]) +
    step([
        ("Entrada invalida", "Campo sem validacao aceita qualquer texto."),
        ("Base fragmentada", "Termos distintos para o mesmo exame quebram as contagens."),
        ("Estatistica distorcida", "Relatorios oficiais saem com dados incorretos."),
        ("Risco processual", "Laudo com informacao trocada — <b>nulidade juridica</b>."),
    ]) +
    ficha("r", "A licao",
        "Cada etapa <i>descendente</i> da cadeia e mais cara que a anterior. Validar no primeiro "
        "elo custa segundos; corrigir no ultimo custa um processo. Previna na entrada.")
)

cad.section("limpeza-funcoes", "Limpeza de dados: o kit de higiene do analista",
    p("Mesmo com validacao, bases herdadas de sistemas legados chegam sujas. As funcoes de limpeza "
      "sao o <b>kit basico de higiene de dados</b> para qualquer analista da POLITEC.") +
    tbl(["Funcao", "O que faz", "Antes \u2192 Depois"],
        [["<b>ARRUMAR()</b> / <b>TRIM()</b>", "Remove espacos extras no inicio e no fim do texto.",
          "<code>'  Delegacia de Homicidios  '</code> \u2192 <code>'Delegacia de Homicidios'</code>"],
         ["<b>PRI.MAIUSCULA()</b>", "Padroniza a capitalizacao de nomes de peritos e delegacias.",
          "<code>cuiaba</code> \u2192 <code>Cuiaba</code>"],
         ["<b>SUBSTITUIR()</b>", "Troca termos antigos por novos padroes institucionais.",
          "<code>Ex. Necropsia</code> \u2192 <code>Necropsia</code>"]],
        num_cols=[]) +
    code("""
        =ARRUMAR(A2)                         // limpa espacos das bordas
        =PRI.MAIUSCULA(A2)                   // primeira letra maiuscula
        =SUBSTITUIR(A2; "Ex. Necropsia"; "Necropsia")   // troca padrao

        // Combinando (limpeza completa em uma celula):
        =PRI.MAIUSCULA(ARRUMAR(SUBSTITUIR(A2; "Ex. "; "")))
        """, "excel") +
    aplicab(
        "Sempre que a base vier de um sistema legado (LIS, SISP) com texto baguncado.",
        "Porque espacos, capitalizacao irregular e termos antigos quebram contagens e cruzam errado.",
        "Padronizar <i>cuiaba</i>, <i>Cuiaba</i> e <i>CUIABA</i> para <b>Cuiaba</b> faz a contagem "
        "por comarca refletir a realidade.") +
    callout("err", "Limpar sem padronizar o alvo",
        "SUBSTITUIR so remove o que voce manda. Antes de limpar, <b>liste os valores unicos</b> da "
        "coluna para descobrir todas as variacoes: <i>cuiaba, Cba, CUIABA, CUIABA-MT</i>.")
)

cad.section("remocao-duplicatas", "Remocao de duplicatas: um risco real na pericia",
    p("Em sistemas periciais, o mesmo exame pode ser registrado <b>duas vezes</b>: uma na "
      "requisicao e outra na entrega do laudo. Isso gera <b>contagem dupla de producao</b> — um "
      "erro que distorce os indicadores e pode inflar artificialmente os numeros reportados.") +
    ficha("a", "Curiosidade do setor",
        "Analistas de dados em laboratorios forenses gastam, em media, <b>60% do tempo</b> de um "
        "projeto apenas limpando e organizando dados — e apenas <b>40%</b> analisando de fato a "
        "producao.") +
    step([
        ("Identifique a chave unica", "Antes de eliminar qualquer linha, defina o que torna um "
         "registro unico. Na pericia, o par <b>numero do laudo + data</b> costuma ser a chave."),
        ("Marque os duplicados", "No Excel: <kbd>Dados</kbd> \u2192 <kbd>Remover Duplicatas</kbd> e "
         "selecione apenas as colunas da chave (ex.: Num_Laudo e Data)."),
        ("Confirme a contagem", "Compare a contagem antes e depois. Se sumiram 40 de 1.000 linhas, "
         "voce tinha 4% de registros duplicados."),
        ("Documente", "Anote quantos registros foram removidos e por qual criterio — a decisao "
         "precisa ser auditavel."),
    ]) +
    callout("err", "Remover duplicata pela linha inteira",
        "Se voce marcar <i>todas</i> as colunas, o sistema pode considerar dois laudos iguais como "
        "unicos apenas porque os textos batem. Use a <b>chave</b>, e nao a linha toda.")
)

cad.section("custo-dados-sujos", "O custo oculto dos dados sujos",
    p("O dado sujo nao aparece no orcamento, mas consome a maior parte do tempo da equipe. Os "
      "numeros do modulo resumem bem o problema.") +
    kpi([
        ("60%", "Tempo gasto so limpando bases de requisicoes"),
        ("80%", "Queda nos erros de digitacao com validacao na entrada"),
        ("40%", "Tempo efetivamente dedicado a analise tecnica"),
    ]) +
    bar_chart(
        ["Limpeza de dados", "Analise real", "Reducao de erros"],
        [60, 40, 80],
        title="Onde vai o tempo do analista forense",
        subtitulo="Fracao do tempo de projeto (limpeza x analise) e queda de erros com validacao.",
        destaque=0) +
    ficha("p", "A conta que ninguem faz",
        "Se a equipe perde 60% do tempo limpando, investir em <b>validacao na entrada</b> nao e "
        "capricho — e liberar mais da metade da capacidade analitica do laboratorio.")
)

cad.section("autor-cairo", "Alberto Cairo e a arte verdadeira dos dados",
    p("A obra <i>The Truthful Art</i> estabelece que visualizacao de dados na gestao publica "
      "<b>nao e sobre fazer graficos bonitos</b> para assessoria de imprensa — e sobre comunicar "
      "a verdade operacional de forma clara e honesta.") +
    ficha("p", "A frase que resume Cairo",
        "\"Um grafico mentiroso ou confuso esconde gargalos e custa vidas ou recursos.\"") +
    aplicab(
        "Sempre que um grafico for apresentado a gestores, autoridades ou ao Poder Judiciario.",
        "Porque a visualizacao e um argumento: um eixo manipulado convence o gestor de uma eficiencia que nao existe.",
        "Nunca usar uma escala que nao comeca no zero para mostrar <i>queda do backlog</i> — isso "
        "exagera pequenas reducoes e passa uma falsa sensacao de eficiencia.")
)

cad.section("regras-grafico-honesto", "As quatro regras do grafico honesto",
    p("Cairo deixa quatro regras praticas que valem para qualquer painel pericial. Sao simples de "
      "verificar e evitam a maior parte dos graficos enganosos.") +
    checklist([
        "Escala Y <b>sempre inicia em zero</b>.",
        "Titulo do grafico <b>descreve o que esta sendo medido</b>.",
        "Fonte dos dados <b>sempre visivel</b>.",
        "Cores com <b>significado consistente</b> (a mesma cor sempre quer dizer a mesma coisa).",
    ]) +
    grid2([
        ("Por que o zero importa",
         "Truncar o eixo Y amplia visualmente a diferenca entre dois valores. Uma queda de 5% pode "
         "parecer de 80%, e o gestor decide com base numa percepcao falsa."),
        ("Por que a fonte importa",
         "Um numero sem fonte nao e auditavel. No contexto pericial, fonte e parte da prova — o "
         "grafico precisa dizer de onde vieram os dados."),
    ]) +
    callout("tip", "Teste dos 3 segundos",
        "Se o Diretor do Laboratorio nao entender o grafico em <b>3 segundos</b>, o grafico esta "
        "ruim — nao o diretor. Clareza e responsabilidade de quem comunica.")
)

cad.section("triangulo-visualizacao", "A escolha certa do grafico: o triangulo da visualizacao",
    p("Cada tipo de grafico responde a uma <b>pergunta diferente</b>. Escolher o grafico errado e "
      "como usar o instrumento de pericia errado: o resultado parece valido, mas a conclusao e "
      "equivocada.") +
    tbl(["Tipo de grafico", "Pergunta que responde", "Exemplo POLITEC"],
        [["<b>Linhas</b>", "Como a variavel <b>mudou ao longo do tempo</b>?",
          "Evolucao mensal de laudos de Toxicologia emitidos nos ultimos 24 meses."],
         ["<b>Barras</b>", "Quais categorias <b>se destacam na comparacao</b>?",
          "TAT medio entre os 5 setores: DNA, Toxicologia, Balistica, Documentoscopia, IML."],
         ["<b>Pizza / Rosca</b>", "Qual a <b>proporcao de cada parte no todo</b>?",
          "Tipos de morte no IML: 60% violentas, 30% naturais, 10% indeterminadas."]],
        num_cols=[]) +
    flow_h([
        ("\U0001f4c8", "Linha = tempo"),
        ("\U0001f4ca", "Barra = comparacao"),
        ("\U0001f369", "Rosca = proporcao"),
    ]) +
    callout("note", "A pergunta vem antes do grafico",
        "Antes de abrir a ferramenta, escreva a pergunta. Se a pergunta e <i>como evoluiu</i>, "
        "linha; se e <i>quem e maior</i>, barra; se e <i>quanto do todo</i>, rosca. O grafico e a "
        "resposta, nao o ponto de partida.")
)

cad.section("problema-pizza", "Alerta vermelho: o problema com o grafico de pizza",
    p("O cerebro humano tem grande dificuldade em <b>comparar angulos</b>. Quando duas fatias tem "
      "valores proximos (ex.: 32% e 34%), e praticamente impossivel identificar qual e maior sem "
      "olhar os rotulos.") +
    ul([
        "Use no maximo <b>3 a 4 categorias</b> em graficos de pizza.",
        "Prefira a versao <b>Rosca (Donut)</b> — mais legivel e moderna.",
        "Se tiver <b>mais de 4 categorias</b>, migre para um grafico de barras.",
        "Evite fatias com valores abaixo de <b>5%</b> — ficam invisiveis.",
    ]) +
    grid2([
        ("Exemplo POLITEC — IML",
         "Ate 3 categorias (Violentas 60%, Naturais 30%, Indeterminadas 10%), o grafico de rosca "
         "funciona bem e comunica rapido."),
        ("Contraexemplo",
         "Cinco tipos de exame com fatias de 9% e 11% proximas: ninguem distingue qual e maior. "
         "Nesse caso, <b>barras</b> resolvem."),
    ]) +
    callout("err", "Pizza com dez fatias",
        "Uma pizza com 10 categorias e um grafico decorativo, nao analitico. O leitor nao consegue "
        "comparar angulos pequenos — use barras ordenadas.")
)

cad.section("autor-tufte", "Edward Tufte e o chartjunk",
    p("Tufte cunhou o termo <b>chartjunk</b> (lixo de grafico): qualquer elemento visual que nao "
      "agrega informacao — sombras 3D, cores neon, bordas grossas, grades excessivas. Para ele, "
      "quanto mais <b>tinta para dados</b>, melhor; quanto mais tinta ornamental, pior.") +
    ficha("p", "A ideia do data-ink ratio",
        "A proporcao de tinta que efetivamente representa dados deve ser maxima. Tudo o que nao e "
        "dado (rotulos redundantes, grades, sombras, fundos) deve ser minimizado ou removido.") +
    legenda([
        ("\u274c", "Chartjunk", "Sombras 3D, gradientes, cores neon, bordas grossas, grades excessivas."),
        ("\u2705", "Data-ink", "Eixo limpo, cor sobria, dado em destaque, rotulo direto."),
    ]) +
    callout("tip", "Tufte na pratica pericial",
        "Dashboards de gestao pericial devem ser legiveis em 3 segundos. Remova o que nao ajuda a "
        "responder a pergunta — inclusive o efeito bonito que so serve para impressionar.")
)

cad.section("chartjunk-pratica", "Chartjunk: o inimigo da clareza na gestao pericial",
    p("O problema mais classico do chartjunk e o <b>grafico 3D</b>. Uma pizza 3D inclinada "
      "distorce a percepcao: a fatia da frente parece maior que a de tras, mesmo que representem "
      "exatamente o mesmo valor.") +
    antesdepois(
        "Grafico de pizza 3D inclinado — a fatia frontal parece maior sem ser; sombras e gradientes "
        "confundem a leitura das proporcoes.",
        "Grafico 2D de rosca, com cores sobrias e rotulos diretos — a proporcao fica honesta.",
        "\u2717 Chartjunk", "\u2713 Grafico limpo") +
    tbl(["Regra de ouro POLITEC", "Por que"],
        [["<b>Sempre em 2D</b>", "O 3D distorce angulos e areas; nao ha ganho de informacao."],
         ["<b>Cores sobrias e de alto contraste</b>", "Facilita leitura impressa e para daltonicos."],
         ["<b>Sem sombras, gradientes ou efeitos 3D</b>", "Tufte: tinta ornamental reduz o data-ink ratio."],
         ["<b>Ler o grafico em 3 segundos</b>", "O gestor decide rapido; se nao entende, o painel falhou."]],
        num_cols=[]) +
    callout("err", "Decisao de alocacao baseada em distorcao",
        "Em apresentacoes para o Secretario de Seguranca, um 3D pode influenciar a alocacao de "
        "recursos. A distorcao e involuntaria, mas o efeito na decisao e real.")
)

cad.section("caso-grafico-3d", "Caso real: o grafico 3D que 'resolveu' o backlog",
    p("Um laboratorio forense estadual apresentou um grafico de colunas 3D ao Secretario de "
      "Seguranca, mostrando uma aparente <b>drastica reducao</b> no backlog de exames de DNA.") +
    step([
        ("O truque", "O eixo Y nao comecava em zero — iniciava em 800 laudos. Uma queda de 900 para "
         "850 parecia visualmente uma reducao enorme."),
        ("A realidade", "A reducao real foi de apenas <b>5%</b>, mas o grafico sugeria algo proximo "
         "de <b>80%</b>."),
        ("A consequencia", "O gestor tomou decisoes estrategicas baseadas numa percepcao falsa de "
         "eficiencia, comprometendo o planejamento real da secretaria."),
        ("A licao", "Transparencia e precisao visual sao questoes de <b>credibilidade tecnica</b>. "
         "Um dado apresentado de forma distorcida tem o mesmo impacto de uma prova mal documentada."),
    ]) +
    ficha("r", "A frase que fica",
        "Na pericia, a integridade do grafico e tao importante quanto a integridade da amostra.")
)

cad.section("grafico-honesto-enganoso", "Grafico honesto x grafico enganoso",
    p("O mesmo dado pode contar duas historias opostas dependendo de onde o eixo Y comeca. Veja a "
      "diferenca entre um grafico honesto e um truncado.") +
    bar_chart(
        ["Jan", "Fev", "Mar", "Abr"],
        [900, 880, 860, 850],
        title="Grafico HONESTO — eixo Y a partir de zero",
        subtitulo="Laudos em backlog. A queda de ~5% e pequena e proporcional (900 \u2192 850).",
        destaque=None) +
    bar_chart(
        ["Jan", "Fev", "Mar", "Abr"],
        [100, 60, 30, 0],
        title="Grafico ENGANOSO — eixo Y truncado em 800",
        subtitulo="Os MESMOS dados (900, 880, 860, 850) desenhados com base 800 parecem despencar.",
        destaque=3) +
    antesdepois(
        "Eixo Y truncado: a mesma queda de 5% parece uma reducao dramatica — percepcao falsa.",
        "Eixo Y a partir do zero: a queda real e proporcional e visivelmente pequena.",
        "Eixo truncado", "Eixo no zero") +
    callout("err", "O eixo truncado e a mentira mais comum",
        "O gestor que so ve a versao truncada toma decisao errada. Nos paineis da POLITEC, a escala "
        "Y comeca no zero por regra — sem excecao para 'melhorar' o visual.")
)

cad.section("guia-escolha-grafico", "Guia pratico: qual grafico usar?",
    p("O guia de escolha dos slides vira uma tabela de bolso para o analista pericial consultar "
      "antes de montar qualquer visualizacao.") +
    tbl(["Se a pergunta e...", "Use", "Cuidado"],
        [["Como mudou <b>ao longo do tempo</b>?", "Grafico de <b>linhas</b>",
          "Comece o eixo Y no zero e marque o periodo."],
         ["Quais categorias <b>se destacam</b>?", "Grafico de <b>barras</b> (horizontais se nomes longos)",
          "Ordene por valor para facilitar a leitura."],
         ["Qual a <b>proporcao</b> no todo?", "<b>Pizza/Rosca</b> (ate 3-4 categorias)",
          "Acima de 4 categorias, migre para barras."],
         ["Quero comparar <b>um numero com uma meta</b>?", "Barras + <b>linha de meta</b>",
          "Deixe a meta visualmente marcada."]],
        num_cols=[]) +
    ficha("g", "Regra de ouro",
        "Escolha o grafico pela <b>pergunta</b>, nunca pela estetica. A estetica serve a clareza; a "
        "clareza serve a verdade.")
)

cad.section("mini-painel-intro", "Hands-on: o mini-painel de gestao pericial",
    p("Objetivo: criar uma <b>visao tatica de 1 pagina</b> para o Chefe do Laboratorio ou Diretor "
      "do IML — um painel que responda, em menos de 10 segundos, as tres perguntas criticas da "
      "gestao pericial.") +
    kpi([
        ("1", "Quantos laudos emitimos?"),
        ("2", "Qual e o nosso TAT medio?"),
        ("3", "Quantos estao atrasados?"),
    ]) +
    grid2([
        ("\U0001f4e6 Producao total",
         "KPI de contagem de laudos concluidos no periodo. Responde a produtividade bruta do "
         "laboratorio."),
        ("\u23f1\ufe0f TAT medio",
         "Tempo medio de emissao por setor. O principal indicador de eficiencia operacional."),
        ("\u26a0\ufe0f Atrasados",
         "Percentual de laudos alem do prazo legal. Sinaliza gargalos por setor ou tipo de exame."),
    ]) +
    callout("note", "Uma pagina, tres perguntas",
        "Um painel bem construido substitui <b>50 paginas de relatorio</b> em texto corrido. O "
        "gestor navega pelos dados e responde com um clique — em vez de 'vou verificar e te retorno'.")
)

cad.section("estrutura-base-painel", "A estrutura da base de dados para o painel",
    p("A base deve ter <b>uma linha por laudo</b>, com colunas estruturadas e sem formatacoes "
      "especiais. Nenhuma celula mesclada, nenhuma cor como informacao, nenhum subtotal embutido.") +
    tbl(["Data_Recebimento", "Data_Emissao", "Tipo_Exame", "Setor", "Status"],
        [["01/06/2025", "10/06/2025", "Toxicologia", "Lab. Quimico", "Concluido"],
         ["05/06/2025", "\u2014", "DNA", "Genetica", "Em andamento"],
         ["02/06/2025", "20/06/2025", "Balistica", "Armamento", "Concluido"]],
        num_cols=[]) +
    code("""
        // Com a base estruturada, o Excel calcula o TAT automaticamente:
        TAT_Dias = Data_Emissao - Data_Recebimento

        // Colunas minimas do painel:
        Data_Recebimento | Data_Emissao | Tipo_Exame | Setor | Status
        """, "excel") +
    callout("err", "Subtotal embutido na base",
        "Linhas de 'Total geral' ou celulas com cor representando status quebram o painel. O dado "
        "bruto fica puro; o calculo acontece no lado do painel.")
)

cad.section("kpis-painel", "KPIs do painel: os tres termometros da gestao",
    p("Os tres KPIs do mini-painel respondem, cada um, a uma dimensao distinta da gestao: "
      "produtividade, eficiencia e conformidade.") +
    tbl(["KPI", "Como calcular", "O que revela"],
        [["<b>Total de Laudos Emitidos</b>",
          "Contagem de laudos com <code>Status = 'Concluido'</code> no periodo.",
          "Produtividade bruta do setor."],
         ["<b>TAT Medio</b>",
          "Media de <code>(Data_Emissao - Data_Recebimento)</code> em dias.",
          "Eficiencia operacional — o indicador central da pericia."],
         ["<b>% de Laudos Atrasados</b>",
          "Proporcao com TAT superior ao prazo legal ou regulamentar.",
          "Gargalos por setor ou tipo de exame; risco processual."]],
        num_cols=[]) +
    code("""
        Total_Emitidos = CONT.SE(TabelaLaudos[Status]; "Concluido")

        TAT_Medio = MEDIA(TabelaLaudos[TAT_Dias])

        Pct_Atrasados = CONT.SE(TabelaLaudos[TAT_Dias]; ">"&$Meta_Prazo)
                        / CONT.NUM(TabelaLaudos[TAT_Dias])
        """, "excel") +
    callout("tip", "TAT medio nao basta",
        "Reporte tambem a <b>mediana</b> do TAT e o <b>percentual atrasado</b>. A media sozinha "
        "esconde casos extremos que puxam o indicador para cima.")
)

cad.section("regras-formatacao-painel", "Regras de formatacao do painel pericial",
    p("Um painel bem formatado transmite <b>credibilidade institucional</b> antes mesmo de ser "
      "lido. A estetica serve a autoridade tecnica do documento.") +
    antesdepois(
        "Efeitos 3D em qualquer grafico; mais de 4 cores; texto menor que 10pt; graficos "
        "sobrepostos; informacoes decorativas sem dados; cores neon ou gradientes.",
        "Remover linhas de grade do fundo; cores da identidade visual da POLITEC; alinhar "
        "elementos; titulo claro em cada grafico; fonte dos dados visivel; slicer de Mes e Setor.",
        "O que EVITAR", "O que FAZER") +
    grid2([
        ("\u2705 O que FAZER",
         ul(["Remover linhas de grade do fundo",
             "Usar cores da identidade visual da POLITEC",
             "Alinhar todos os elementos",
             "Titulo claro em cada grafico",
             "Fonte dos dados visivel",
             "Slicer (filtro) para Mes e Setor"])),
        ("\u274c O que EVITAR",
         ul(["Efeitos 3D em qualquer grafico",
             "Mais de 4 cores diferentes",
             "Texto menor que 10pt",
             "Graficos sobrepostos ou apertados",
             "Informacoes decorativas sem dados",
             "Cores neon ou gradientes"])),
    ]) +
    callout("tip", "Estetica a servico da autoridade tecnica",
        "O painel e a face publica da gestao pericial. Um visual sobrio e limpo reforca a "
        "confianca na instituicao; o excesso de efeitos a enfraquece.")
)

cad.section("resultado-painel", "O resultado: um painel que fala por si",
    p("Um mini-painel bem construido <b>substitui 50 paginas de relatorio</b> em texto corrido. "
      "Em uma reuniao com o Secretario de Seguranca Publica, o gestor deve navegar pelos dados em "
      "tempo real e responder perguntas com um clique.") +
    flow_h([
        ("\U0001f4c4", "Base estruturada"),
        ("\U0001f4d0", "KPIs calculados"),
        ("\U0001f39b\ufe0f", "Slicers Mes/Setor"),
        ("\U0001f4ca", "Visuais honestos"),
        ("\U0001f5e3\ufe0f", "Resposta em 1 clique"),
    ]) +
    ficha("g", "O entregavel da manha",
        "Ao final do Modulo 4, o participante tem um painel tatico de uma pagina com producao, "
        "TAT e atraso — filtravel por mes e setor. Ele sera a base do dashboard do Dia 4.")
)

# =================================================================
# PARTE 2 - MODULO 5
# =================================================================
cad.grp("Parte 2 · Modulo 5 — Ferramentas e ETL",
        "Excel x Power BI, o processo ETL de Kimball, o Power Query e a preparacao de bases.")

cad.section("paradigma-excel-pbi", "O paradigma: Excel x Power BI na pericia criminal",
    p("A escolha entre Excel e Power BI <b>nao e ideologica — e estrategica</b>. Cada ferramenta "
      "tem um dominio natural. Usar a errada para a tarefa certa e como usar luminol para analisar "
      "balistica.") +
    grid2([
        ("\U0001f4d2 Excel — a planilha do perito",
         "Flexibilidade total, calculos ad-hoc, manipulacao celula a celula. Ideal para o controle "
         "diario, analises pontuais e bases com <b>menos de 100 mil linhas</b>."),
        ("\U0001f4ca Power BI — a inteligencia institucional",
         "Processa milhoes de linhas, atualizacao automatica, modelagem relacional e publicacao em "
         "nuvem. Ideal para dashboards institucionais e relatorios para a Secretaria."),
    ]) +
    callout("note", "Nao e um duel: e um fluxo",
        "O Excel continua sendo a porta de entrada e a bancada do perito. O Power BI e a camada "
        "institucional que escala a analise. Um alimenta o outro.")
)

cad.section("excel-forcas-limitacoes", "Excel: forcas e limitacoes para a pericia",
    p("Conhecer os <b>limites</b> da ferramenta e tao importante quanto conhecer suas forcas. O "
      "planejamento da POLITEC deve assumir esses limites na origem.") +
    grid2([
        ("\u2705 Pontos fortes",
         ul(["Flexibilidade total de manipulacao",
             "Calculos ad-hoc rapidos",
             "Controle diario do perito",
             "Gestao de estoque de reagentes",
             "Ideal para bases pequenas (menos de 100 mil linhas)",
             "Curva de aprendizado baixa"])),
        ("\u26a0\ufe0f Limitacoes criticas",
         ul(["Limite de <b>1.048.576 linhas</b>",
             "Atualizacao sempre manual",
             "Propenso a erros de referencia circular",
             "Dificil colaboracao em tempo real",
             "Lento com muitas formulas complexas",
             "Sem modelagem de dados relacional"])),
    ]) +
    callout("err", "1 milhao de linhas nao e o problema",
        "O limite de linhas raramente e atingido. O problema pratico e a <b>lentidao</b> com "
        "centenas de milhares de linhas e muitas formulas condicionais. Ai a planilha trava.")
)

cad.section("pbi-forcas-limitacoes", "Power BI: forcas e limitacoes para a pericia",
    p("O Power BI foi feito para escala e governanca. Ele resolve o que a planilha nao resolve, "
      "mas cobra um preco em curva de aprendizado e infraestrutura.") +
    grid2([
        ("\u2705 Pontos fortes",
         ul(["Processa todo o historico do <b>SINESP/LIS</b>",
             "Atualizacao automatica agendada",
             "Modelagem de dados relacional",
             "Interatividade avancada com <b>slicers</b>",
             "Publicacao na nuvem para a Secretaria",
             "Padrao de mercado em governos estaduais"])),
        ("\u26a0\ufe0f Limitacoes",
         ul(["Curva de aprendizado inicial mais ingreme",
             "Menos flexivel para 'rabiscos' rapidos",
             "Requer licenciamento corporativo completo",
             "Dependente de infraestrutura de dados"])),
    ]) +
    callout("tip", "Desktop e gratuito",
        "O <b>Power BI Desktop e gratuito</b> para uso individual. So a publicacao em nuvem "
        "(compartilhamento) exige licenca Pro ou Premium. Voce pode praticar hoje, de graca.")
)

cad.section("quando-usar-cada", "Quando usar cada ferramenta?",
    p("A decisao se resume a tres dimensoes: <b>volume</b>, <b>frequencia de atualizacao</b> e "
      "<b>publico</b> do resultado.") +
    tbl(["Cenario", "Ferramenta", "Motivo"],
        [["Controle diario do perito e analises pontuais", "<b>Excel</b>",
          "Flexibilidade e velocidade para pequenos ajustes."],
         ["Base com menos de 100 mil linhas", "<b>Excel</b>",
          "A planilha da conta sem perder desempenho."],
         ["Historico completo de laudos (milhoes de linhas)", "<b>Power BI</b>",
          "Processa volume que a planilha nao suporta."],
         ["Dashboard que a Secretaria acessa sozinha", "<b>Power BI</b>",
          "Publicacao na nuvem, acesso simultaneo, atualizacao agendada."],
         ["Relatorio mensal recorrente", "<b>Power BI + Power Query</b>",
          "Limpe uma vez, atualize sempre, sem retrabalho manual."]],
        num_cols=[]) +
    aplicab(
        "Sempre que a POLITEC precisar decidir entre agilidade local e alcance institucional.",
        "Porque usar a ferramenta errada gera retrabalho e limita a escala da analise.",
        "O controle semanal do laboratorio fica no Excel; o painel de transparencia mensal vai para "
        "o Power BI publicado na nuvem.")
)

cad.section("autor-kimball", "Ralph Kimball: o pai do Data Warehousing",
    p("Ralph Kimball e responsavel pelos fundamentos da <b>Modelagem Dimensional</b> — a "
      "arquitetura que organiza dados para analise gerencial. Seu conceito mais importante para a "
      "pericia e o processo <b>ETL</b>: Extract, Transform, Load.") +
    ficha("p", "A frase de apoio",
        "\"O Data Warehouse nao e apenas um banco grande; e um ambiente de decisao onde os dados "
        "sao organizados para serem compreendidos.\" — parafraseando Kimball.") +
    legenda([
        ("\U0001f4e4", "Extract", "Extrair o dado bruto da fonte (CSV, LIS, SISP)."),
        ("\U0001f527", "Transform", "Limpar, padronizar e criar colunas calculadas."),
        ("\U0001f4e5", "Load", "Carregar no modelo de dados do BI, pronto para a analise."),
    ]) +
    callout("note", "Modelagem estrela",
        "Kimball organiza a analise em <b>tabelas fato</b> (as medidas, ex.: um laudo) e "
        "<b>tabelas dimensao</b> (o contexto, ex.: setor, tipo de exame, data). O modelo estrela "
        "volta no Dia 4.")
)

cad.section("processo-etl", "O processo ETL aplicado a POLITEC",
    p("O ETL e o <b>coracao da automacao analitica</b>. Feito corretamente uma vez, ele pode ser "
      "replicado automaticamente mes a mes, sem intervencao manual.") +
    flow_h([
        ("\U0001f4e4", "Extract"),
        ("\U0001f527", "Transform"),
        ("\U0001f4e5", "Load"),
        ("\U0001f4ca", "Dashboard"),
    ]) +
    grid2([
        ("Extract — Extracao",
         "Puxar o CSV bruto exportado do sistema de gestao de laudos (LIS/SISP). O dado chega "
         "<b>do jeito que o sistema entrega</b> — geralmente sujo e nao padronizado."),
        ("Transform — Transformacao",
         "Limpar e padronizar: nomes de delegacias, remover acentos problematicos, criar colunas "
         "calculadas como <b>Mes de Emissao</b> e <b>TAT em dias</b>. A etapa mais trabalhosa — e a "
         "mais importante."),
    ]) +
    ficha("g", "Load — Carregamento",
        "Carregar o dado limpo e estruturado no modelo do Power BI. A partir dai, os dashboards se "
        "constroem sobre uma base <b>confiavel e auditavel</b>.")
)

cad.section("etl-pratica", "ETL na pratica pericial: cada etapa importa",
    p("Vamos ver o ETL com exemplo concreto da POLITEC, etapa por etapa.") +
    step([
        ("Extract", "Puxar o CSV bruto exportado do LIS/SISP. Ele chega com acentos quebrados, "
         "linhas de 'Total Geral' e cabecalhos longos."),
        ("Transform", "Aplicar ARRUMAR, PRI.MAIUSCULA e SUBSTITUIR; remover duplicatas pela chave "
         "numero do laudo + data; criar as colunas <b>Mes_Emissao</b> e <b>TAT_Dias</b>."),
        ("Load", "Carregar o resultado no modelo de dados do Power BI (<b>tabela fato</b> de laudos "
         "+ dimensoes de setor, tipo de exame e calendario)."),
        ("Atualizar", "No mes seguinte, bastam dois cliques em <b>Atualizar</b>: o ETL repete tudo."),
    ]) +
    callout("err", "Pular o Transform",
        "Carregar o CSV bruto direto no Power BI e o erro mais comum. O resultado sao colunas com "
        "tipo errado e valores ininteligiveis — o painel nasce quebrado.")
)

cad.section("caso-migracao-transparencia", "Caso real: a migracao da transparencia pericial",
    p("Secretarias de Seguranca Publica em todo o Brasil comecaram a migrar seus relatorios "
      "mensais estaticos — PDFs com tabelas de Excel — para <b>portais de dados abertos em Power "
      "BI</b>, acessiveis ao Ministerio Publico, Defensoria Publica e a sociedade civil.") +
    grid2([
        ("De PDFs a portais interativos",
         "O relatorio que antes virava um PDF imutavel agora e um painel filtravel por tipo de "
         "crime, comarca e periodo. O MP e a Defensoria acessam <b>sem oficios formais</b>."),
        ("Para o Mato Grosso",
         "O Power BI deixa de ser ferramenta interna e vira <b>transparencia institucional</b> e "
         "<b>accountability</b> perante o sistema de Justica."),
    ]) +
    kpi([
        ("Autoatendimento", "MP e Defensoria filtram sozinhos"),
        ("Menos oficios", "Servidores liberados para a tecnica"),
        ("Prestacao de contas", "Accountability ao Judiciario"),
    ]) +
    callout("tip", "Transparencia que reduz trabalho",
        "O portal nao so melhora a imagem institucional — ele <b>reduz a carga burocratica</b> de "
        "responder oficio por oficio. Todos ganham.")
)

cad.section("curiosidade-origem-pbi", "Curiosidade historica: a origem do Power BI",
    p("Hoje o Power BI supera Tableau e Qlik em adocao governamental. A historia comeca como um "
      "projeto interno da Microsoft.") +
    step([
        ("2010 — Project Crescent", "Nasce como projeto de uso interno da Microsoft para "
         "visualizacao de dados."),
        ("2013 — Plugins do Excel", "<b>Power Query</b> e <b>Power Pivot</b> sao lancados como "
         "plugins do Excel — a base do motor atual."),
        ("2015 — Power BI", "Rebatizado oficialmente como <b>Power BI</b> e lancado ao publico."),
        ("Hoje", "Lider absoluto de mercado, adotado por governos estaduais de todo o Brasil."),
    ]) +
    ficha("p", "A ponte com a seguranca publica",
        "Para Mato Grosso, a integracao representa a possibilidade de cruzar <b>dados periciais "
        "com dados policiais</b> em uma unica plataforma — a visao de inteligencia de seguranca "
        "publica do futuro.")
)

cad.section("preparacao-bases-exportacao", "Preparacao de bases para exportacao: os 4 problemas",
    p("O maior inimigo do Power BI nao e a complexidade dos dados — e a <b>ma qualidade do "
      "arquivo de entrada</b>. Sistemas legados da POLITEC e do SINESP frequentemente exportam "
      "CSVs com problemas que impedem a importacao correta.") +
    tbl(["Problema", "Sintoma", "Como corrigir"],
        [["<b>Codificacao errada</b>", "Acentos viram caracteres estranhos: <i>Cuiaba</i> vira "
          "<i>CuiabA</i>.", "Salvar o CSV como <b>UTF-8</b>."],
         ["<b>Delimitadores confusos</b>", "Ponto e virgula vs. virgula — o BI nao sabe separar as "
          "colunas.", "Padronizar o separador e conferir na importacao."],
         ["<b>Linhas de rodape</b>", "'Total Geral' exportado automaticamente quebra a importacao.",
          "Deletar as linhas de total antes de carregar."],
         ["<b>Cabecalhos inadequados</b>", "<i>Data de Emissao do Laudo (dd/mm/aaaa)</i> e ilegivel "
          "para o BI.", "Renomear para <code>Data_Emissao</code>."]],
        num_cols=[]) +
    callout("err", "Os 4 problemas juntos",
        "Uma base com acento quebrado, delimitador errado, linha de total e cabecalho longo e "
        "praticamente impossivel de importar sem limpeza. E por isso que existe o <b>Pre-ETL</b>.")
)

cad.section("checklist-pre-etl", "Checklist de preparacao: o 'Pre-ETL' no Excel",
    p("Antes de levar qualquer base ao Power BI, execute este checklist de <b>4 pontos</b>. Eles "
      "evitam 90% dos erros de importacao.") +
    checklist([
        "<b>Codificacao UTF-8</b> — salvar como CSV UTF-8 (delimitado por virgulas); preserva "
        "acentos: Cuiaba, Obito, Toxicologico.",
        "<b>Cabecalho limpo</b> — primeira linha com nomes claros, sem espacos ou caracteres "
        "especiais: <code>Data_Emissao</code>, nao 'Data de Emissao do Laudo (dd/mm/aaaa)'.",
        "<b>Tipagem correta</b> — colunas de data como <b>Data</b>, nao como Texto; o BI nao "
        "calcula TAT com texto.",
        "<b>Limpeza de lixo</b> — deletar linhas em branco ao final e textos de 'Total Geral' "
        "gerados automaticamente.",
    ]) +
    kpi([
        ("90%", "Dos erros de importacao evitados"),
        ("4", "Itens do checklist Pre-ETL"),
        ("UTF-8", "Codificacao obrigatoria"),
    ]) +
    callout("tip", "Faca uma vez, no Excel",
        "O Pre-ETL e rapido e evita horas de depuracao no BI. Trate o arquivo de saida como "
        "<b>produto</b>: limpo, tipado e com cabecalho descritivo.")
)

cad.section("nomenclatura-colunas", "Nomenclatura de colunas: um padrao que salva horas",
    p("O nome da coluna e a interface entre o dado e a analise. Nomes limpos economizam horas "
      "de depuracao e evitam erros de formula.") +
    tbl(["Nome inadequado", "Nome correto"],
        [["<code>Data de Emissao do Laudo (dd/mm/aaaa)</code>", "<code>Data_Emissao</code>"],
         ["<code>Tipo/Categoria do Exame Realizado</code>", "<code>Tipo_Exame</code>"],
         ["<code>Setor Responsavel pelo Laudo</code>", "<code>Setor</code>"],
         ["<code>Situacao atual do processo</code>", "<code>Status</code>"],
         ["<code>N do Laudo Pericial</code>", "<code>Num_Laudo</code>"]],
        num_cols=[]) +
    antesdepois(
        "Nomes longos, com espacos, acentos, parenteses e barras — quebram formulas e codigo.",
        "Nomes curtos, sem espacos nem caracteres especiais, no padrao <b>Pythonico</b>: "
        "<code>Data_Emissao</code>, <code>Num_Laudo</code>.",
        "Nome baguncado", "Nome limpo") +
    callout("err", "Espaco no nome da coluna",
        "Nome com espaco obriga a usar <code>[coluna com espaco]</code> entre colchetes e quebra "
        "codigo em Python/SQL. Use <code>_</code> desde o inicio.")
)

cad.section("power-query-motor", "Power Query: o motor da limpeza automatizada",
    p("O <b>Power Query</b> e uma ferramenta de ETL embutida no Excel e no Power BI que <b>grava "
      "os passos da limpeza como uma receita</b>. Cada acao que voce realiza fica registrada na "
      "sequencia — e pode ser repetida automaticamente.") +
    grid2([
        ("O que e o Power Query?",
         "Um motor de ETL embutido no Excel e no Power BI. Ele registra cada etapa da limpeza e a "
         "reproduz sempre que o dado e atualizado."),
        ("Por que isso importa na pericia?",
         "O relatorio de producao mensal deixa de ser manual: o processo torna-se <b>deterministico "
         "e auditavel</b>, aplicando sempre os mesmos passos e eliminando erros de digitacao."),
    ]) +
    ficha("g", "Vantagem decisiva",
        "Se voce receber a base do mes seguinte com o mesmo formato sujo, basta clicar em "
        "<b>Atualizar</b> e o Power Query repete todos os passos. <b>Limpeza configurada uma vez "
        "\u2192 replicada automaticamente para sempre.</b>")
)

cad.section("power-query-pratica", "Power Query na pratica: exemplo POLITEC",
    p("Quatro operacoes resolvem a maior parte da sujeira de uma base exportada de sistema "
      "legado. Elas ficam gravadas como uma sequencia permanente.") +
    step([
        ("Promover Cabecalhos", "A primeira linha de dados vira o cabecalho da tabela, eliminando "
         "titulos longos do sistema."),
        ("Substituir Nulos", "Onde faltam valores economicos ou categoricos, aplicamos a regra "
         "padrao (ex.: 'Nao informado' ou 0), em vez de deixar celulas vazias."),
        ("Dividir DataHora", "Uma coluna de data-hora vira <b>Data</b> e <b>Hora</b> separadas, "
         "permitindo calcular o TAT em dias."),
        ("Fechar e Carregar", "O resultado vai para a planilha ou o modelo de dados do Power BI, "
         "pronto para alimentar os visuais."),
    ]) +
    code("""
        // Sequencia de passos gravados no Power Query (M):
        let
            Origem = Csv.Document(File.Contents("LIS_export.csv"), [Delimiter=","]),
            Cabecalho = Table.PromoteHeaders(Origem),
            SemNulos = Table.ReplaceValue(Cabecalho, null, "Nao informado", Replacer.ReplaceValue),
            DataHora = Table.SplitColumn(SemNulos, "DataHora", Splitter.SplitTextByDelimiter(" ")),
            TAT = Table.AddColumn(DataHora, "TAT_Dias", each [Data_Emissao] - [Data_Recebimento])
        in
            TAT
        """, "powerquery") +
    callout("tip", "Na proxima exportacao",
        "O analista apenas clica em <b>Atualizar</b> e o Power Query executa tudo automaticamente. "
        "O trabalho de limpeza deixa de ser manual e passa a ser <b>codigo auditavel</b>.")
)

cad.section("caso-automacao-relatorio", "Caso real: a automacao do relatorio de producao mensal",
    p("Um setor administrativo de laboratorio forense gastava <b>2 dias inteiros</b> no inicio de "
      "cada mes copiando e colando dados de 4 planilhas diferentes — uma por setor — para montar o "
      "relatorio de producao do Diretor.") +
    grid2([
        ("O problema",
         "4 planilhas x copiadas manualmente x 12 meses = risco de erro em cada iteracao. Sem "
         "falar no desgaste do profissional e no tempo perdido em tarefa puramente mecanica."),
        ("A solucao implementada",
         "Criar uma pasta <b>Entrada_Mensal</b>. O Power Query foi configurado para ler todos os "
         "arquivos dessa pasta e empilha-los automaticamente em uma unica tabela consolidada."),
    ]) +
    kpi([
        ("2 dias", "Tempo anterior (manual)"),
        ("30s", "Tempo atual (salvar + Atualizar)"),
        ("99%", "Reducao de tempo"),
    ]) +
    bar_chart(
        ["Antes", "Depois"],
        [100, 1],
        title="Tempo de consolidacao mensal (escala relativa)",
        subtitulo="2 dias de trabalho manual viram 30 segundos com Power Query.",
        destaque=1)
)

cad.section("filosofia-automacao", "A filosofia por tras da automacao",
    p("A automacao nao e sobre substituir pessoas — e sobre <b>liberar o perito</b> da tarefa "
      "mecanica para o que realmente importa: a analise tecnica.") +
    ficha("g", "A frase que orienta",
        "\"A tecnologia deve trabalhar para o perito, liberando tempo para o que realmente "
        "importa: a analise tecnica.\"") +
    antesdepois(
        "Perito como <b>operador de planilha</b> — copiar, colar, formatar. Tarefa mecanica e de "
        "baixo valor agregado.",
        "Perito como <b>analista</b> — interpretar padroes, concluir e decidir tecnicamente.",
        "Antes da automacao", "Depois da automacao") +
    callout("tip", "Cada hora poupada vira analise",
        "Cada hora economizada em copiar e colar e uma hora a mais para aprofundar a analise "
        "forense, identificar padroes de criminalidade ou melhorar a qualidade do laudo.")
)

cad.section("comparativo-consolidado", "Comparativo consolidado: Excel x Power BI",
    p("A visao consolidada dos slides serve como criterio de decisao institucional.") +
    tbl(["Criterio", "Excel", "Power BI"],
        [["Volume de dados", "Ate ~1 milhao de linhas", "Dezenas de milhoes de linhas"],
         ["Atualizacao", "Manual", "Automatica (agendada)"],
         ["Colaboracao", "Limitada", "Nuvem — acesso simultaneo"],
         ["Curva de aprendizado", "Baixa", "Media-alta"],
         ["Publicacao institucional", "PDF / e-mail", "Portal web interativo"],
         ["Melhor uso na POLITEC", "Controle diario do perito", "Dashboard do Diretor/Secretario"]],
        num_cols=[]) +
    callout("note", "Escolha por criterio, nao por gosto",
        "A pergunta certa nao e 'qual e melhor?', e '<b>qual resolve este problema?</b>'. O volume, "
        "a frequencia de atualizacao e o publico definem a ferramenta.")
)

cad.section("cadeia-completa", "A cadeia completa: do dado bruto ao dashboard",
    p("O caminho do dado pericial ate o painel do Diretor passa por todas as etapas do dia. Cada "
      "elo depende do anterior — e um elo fraco contamina todo o resultado.") +
    flow_h([
        ("\U0001f5c2\ufe0f", "Sistema legado"),
        ("\U0001f4e4", "Extract"),
        ("\U0001f527", "Transform"),
        ("\U0001f4e5", "Load"),
        ("\U0001f4ca", "Dashboard"),
    ]) +
    grid2([
        ("A montante",
         "Validacao na entrada e Pre-ETL no Excel garantem que o dado chegue limpo ao pipeline."),
        ("A jusante",
         "Visualizacoes honestas (Cairo/Tufte) garantem que o dado limpo seja comunicado sem "
         "distorcao — a cadeia so fecha quando a decisao e correta."),
    ]) +
    ficha("p", "O principio do dia",
        "Dado sujo e prova contaminada. Da entrada ao grafico, a <b>cadeia de custodia digital</b> "
        "precisa ser integra em todos os elos.")
)

cad.section("erros-iniciantes-pbi", "Erros comuns de iniciantes no Power BI",
    p("Quatro erros aparecem com frequencia em quem esta comecando no BI. Todos tem a mesma raiz: "
      "tratar o dado sem a disciplina do ETL.") +
    tbl(["Erro", "O que acontece", "O correto"],
        [["<b>Importar sem limpar</b>",
          "Levar o CSV bruto ao Power BI sem passar pelo Pre-ETL: colunas com tipo errado e valores "
          "ininteligiveis.", "Fazer o Pre-ETL (UTF-8, cabecalho, tipagem) antes de importar."],
         ["<b>Medidas na planilha, nao no modelo</b>",
          "Calcular TAT no Excel e importar o resultado. O BI nao recalcula dinamicamente.",
          "Deixar o Power BI calcular via <b>DAX</b>, permitindo filtros interativos."],
         ["<b>Usar formatacao como dado</b>",
          "Pintar celulas de amarelo para indicar 'atrasado'. O BI nao le cores.",
          "Criar uma coluna <code>Status_Atraso</code> com texto: 'Atrasado' ou 'No Prazo'."],
         ["<b>Ignorar relacionamentos</b>",
          "Colocar tudo em uma tabela gigante em vez de criar um <b>modelo estrela</b>.",
          "Criar tabelas fato + dimensoes relacionadas, com melhor performance e flexibilidade."]],
        num_cols=[]) +
    callout("err", "O BI nao le cor",
        "Formatacao e para humanos; o motor de BI le <b>valores</b>. Toda informacao precisa virar "
        "uma coluna com texto ou numero — nunca apenas uma cor.")
)

cad.section("inteligencia-compartilhada", "Inteligencia compartilhada: o poder do BI em rede",
    p("Quando o Power BI e publicado na nuvem, cada gestor — do Chefe do Setor ao Secretario de "
      "Estado — ve os <b>mesmos dados atualizados em tempo real</b>. Elimina-se a versao "
      "desatualizada circulando por e-mail.") +
    grid2([
        ("O problema do arquivo por e-mail",
         "Cada pessoa tem uma copia diferente da planilha. Quando alguem decide, ja nao se sabe "
         "qual e a versao correta — cada um produziu seu proprio numero."),
        ("A fonte unica da verdade",
         "Com o BI em rede, todos consultam o mesmo painel, atualizado automaticamente. A decisao "
         "institucional passa a se basear em um numero so."),
    ]) +
    ficha("g", "A frase do modulo",
        "Estabelece-se uma <b>unica fonte da verdade</b> para toda a SESP/MT. Nada de cinco "
        "versoes do mesmo indicador: um portal, um numero, uma decisao.")
)

cad.section("visualizacoes-tat", "Visualizacoes para gestao do TAT na pericia",
    p("Barras <b>horizontais</b> sao ideais quando os nomes das categorias sao longos — como os "
      "setores periciais. A <b>linha de meta</b> torna imediatamente visivel quais setores estao "
      "acima ou abaixo do padrao.") +
    bar_chart(
        ["DNA", "Toxicologia", "Balistica", "Documentoscopia", "IML"],
        [28, 18, 12, 9, 5],
        title="TAT medio por setor (dias) — meta: 15 dias",
        subtitulo="DNA e Toxicologia estao acima da meta (destaque em vermelho); os demais abaixo.",
        destaque=0) +
    kpi([
        ("Meta", "15 dias"),
        ("DNA", "28 dias (acima)"),
        ("Toxicologia", "18 dias (acima)"),
        ("IML", "5 dias (melhor)"),
    ]) +
    ficha("a", "A leitura do gestor",
        "Neste exemplo ilustrativo, <b>DNA e Toxicologia</b> estao acima da meta — sinalizacao "
        "clara para priorizar recursos ou investigar gargalos operacionais.")
)

cad.section("evolucao-mensal", "Evolucao mensal de producao: grafico de linhas",
    p("O grafico de <b>linhas</b> revela tendencias que nenhuma tabela estatica consegue mostrar: "
      "quedas sazonais, picos de demanda e a progressao ao longo do tempo.") +
    bar_chart(
        ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
        [45, 48, 52, 55, 50, 58],
        title="Producao mensal por setor (exemplo ilustrativo)",
        subtitulo="Linhas permitem comparar a tendencia entre Toxicologia, Balistica e DNA.",
        destaque=None) +
    aplicab(
        "Quando o objetivo e acompanhar tendencia e sazonalidade da producao.",
        "Porque a pergunta e 'como mudou ao longo do tempo', e nao 'quem e maior'.",
        "Uma queda em janeiro pode indicar ferias ou recesso; um pico em junho, mutirao de "
        "conclusao de casos antigos.")
)

cad.section("resumo-conceitos", "Resumo do Dia: os conceitos que ficam",
    p("Quatro ideias resumem o dia inteiro. Sao elas que voce deve levar para a pratica.") +
    legenda([
        ("\U0001f9f9", "Validacao e limpeza", "Pre-requisitos, nao opcionais. Dado sujo e prova "
         "contaminada; a cadeia de custodia digital comeca na entrada."),
        ("\U0001f4ca", "Visualizacao honesta", "Escolha o grafico pela pergunta, nao pela estetica. "
         "Eixo Y no zero. Sem 3D em paineis de gestao."),
        ("\U0001f517", "Excel x Power BI", "Excel para controle diario e analise flexivel; Power BI "
         "para inteligencia institucional escalavel e transparencia."),
        ("\U0001f527", "ETL e Power Query", "Limpe uma vez, atualize para sempre. O ETL e o coracao "
         "da automacao analitica na gestao pericial moderna."),
    ]) +
    ficha("g", "A ponte para o Dia 4",
        "Tudo o que fizemos hoje prepara o <b>laboratorio de Power BI</b> do proximo dia: base "
        "limpa, colunas bem nomeadas, modelo pensado. Sem isso, o dashboard nao decola.")
)

# =================================================================
# PARTE 3 - PRATICA GUIADA
# =================================================================
cad.grp("Parte 3 · Pratica guiada",
        "Seis laboratorios que constroem, do zero, uma base limpa e um mini-painel pericial.")

cad.section("lab1-validacao", "Lab 1 — Validacao de dados na entrada",
    p("Objetivo: impedir que dados invalidos entrem na base, configurando listas suspensas, "
      "restricao de datas e limites numericos.") +
    step([
        ("Crie uma aba de parametros", "No Excel/Sheets, crie uma aba <b>Parametros</b> com as "
         "listas de <code>Tipo_Exame</code>, <code>Setor</code> e <code>Status</code>."),
        ("Aplique a lista suspensa", "Selecione a coluna <code>Tipo_Exame</code> \u2192 "
         "<kbd>Dados</kbd> \u2192 <kbd>Validacao de Dados</kbd> \u2192 <i>Lista</i> \u2192 aponte "
         "para o intervalo da aba Parametros."),
        ("Restrinja as datas", "Na coluna <code>Data_Recebimento</code>, valide como <i>Data</i> "
         "menor ou igual a <code>=HOJE()</code>."),
        ("Limite os numeros", "Na coluna de peso/quantidade, valide <i>Numero inteiro</i> maior ou "
         "igual a 0."),
        ("Teste o bloqueio", "Tente digitar um tipo de exame inexistente e uma data futura: ambos "
         "devem ser recusados."),
    ]) +
    callout("err", "Validacao aplicada na coluna errada",
        "Valide o <b>intervalo exato</b> da coluna. Se a base ganhar linhas novas fora do intervalo "
        "validado, a protecao some. Em Tabela Estruturada, a validacao se estende sozinha.")
)

cad.section("lab2-limpeza", "Lab 2 — Limpeza com ARRUMAR, PRI.MAIUSCULA e SUBSTITUIR",
    p("Objetivo: receber uma base baguncada de sistema legado e entregar nomes de delegacias e "
      "tipos de exame padronizados.") +
    code("""
        // Em colunas auxiliares, limpe cada campo:

        Setor_limpo     = PRI.MAIUSCULA(ARRUMAR(A2))
        Delegacia_limpa = ARRUMAR(SUBSTITUIR(B2; "Ex. "; ""))

        // Depois, cole os resultados como valor e remova as colunas originais.
        // NUNCA sobrescreva o dado bruto sem antes conferir uma amostra.
        """, "excel") +
    step([
        ("Liste os valores unicos", "Antes de limpar, use <i>Dados \u2192 Remover Duplicatas</i> em "
         "uma copia da coluna para ver todas as variacoes existentes."),
        ("Aplique a limpeza combinada", "Use <code>=PRI.MAIUSCULA(ARRUMAR(SUBSTITUIR(...)))</code> "
         "em uma coluna auxiliar."),
        ("Cole como valor", "Copie a coluna limpa e cole como <b>valores</b> sobre a original "
         "(Ctrl+Shift+V)."),
        ("Confira a contagem", "Compare o numero de categorias antes e depois: deve diminuir e "
         "estabilizar."),
    ]) +
    callout("tip", "SUBSTITUIR em cascata",
        "Para varias variacoes do mesmo termo, encadeie: "
        "<code>=SUBSTITUIR(SUBSTITUIR(A2;'Genetica';'DNA');'Perfil Genetico';'DNA')</code>.")
)

cad.section("lab3-duplicatas", "Lab 3 — Remocao de duplicatas pela chave unica",
    p("Objetivo: eliminar a contagem dupla de producao, removendo registros repetidos com base na "
      "chave <b>numero do laudo + data</b>.") +
    step([
        ("Faca uma copia da base", "Nunca remova duplicatas na base original sem backup."),
        ("Selecione a base inteira", "Clique em qualquer celula dentro dos dados."),
        ("Abra a ferramenta", "<kbd>Dados</kbd> \u2192 <kbd>Remover Duplicatas</kbd>. No Sheets: "
         "<i>Dados \u2192 Remover duplicatas \u2192 Comparar por colunas</i>."),
        ("Marque apenas a chave", "Deixe marcadas somente <code>Num_Laudo</code> e <code>Data</code>. "
         "Desmarque as demais colunas."),
        ("Registre o numero removido", "Anote quantos registros sairam — a decisao precisa ser "
         "<b>auditavel</b>."),
    ]) +
    kpi([
        ("Antes", "1.000 registros"),
        ("Duplicados", "40 linhas (4%)"),
        ("Depois", "960 laudos unicos"),
    ]) +
    callout("err", "Chave errada",
        "Se a chave for fraca (ex.: apenas a data), dois laudos legitimos do mesmo dia podem ser "
        "removidos. Use <b>numero do laudo + data</b> como par de identificacao.")
)

cad.section("lab4-estrutura-painel", "Lab 4 — Estruturar a base do mini-painel",
    p("Objetivo: transformar a base limpa em uma <b>Tabela Estruturada</b> com as colunas do "
      "painel, sem celulas mescladas nem formatacao como dado.") +
    code("""
        // Colunas da base (uma linha por laudo):
        Data_Recebimento | Data_Emissao | Tipo_Exame | Setor | Status

        // Coluna calculada (dentro da tabela):
        TAT_Dias = SE([@[Data_Emissao]]=""; "Em andamento";
                      [@[Data_Emissao]] - [@[Data_Recebimento]])
        """, "excel") +
    step([
        ("Converta em Tabela", "<kbd>Ctrl</kbd> + <kbd>T</kbd> e marque <i>Minha tabela tem "
         "cabecalho</i>."),
        ("Renomeie a tabela", "Em <i>Design da Tabela</i>, chame de <code>TabelaLaudos</code>."),
        ("Crie a coluna TAT", "Adicione <code>TAT_Dias</code> com a formula acima, tratando o "
         "'Em andamento'."),
        ("Confira a tipagem", "Data_Recebimento e Data_Emissao devem ser <b>datas numericas</b>; "
         "TAT_Dias, um numero de dias."),
    ]) +
    callout("err", "TAT na base em vez do modelo",
        "Calcular o TAT como texto estatico impede a atualizacao automatica. Deixe a coluna como "
        "<b>calculo vivo</b> — no Excel agora, no modelo DAX depois.")
)

cad.section("lab5-kpis-slicers", "Lab 5 — KPIs e slicers do mini-painel",
    p("Objetivo: montar a visao tatica de uma pagina com os tres KPIs e os filtros de Mes e Setor.") +
    code("""
        Total_Emitidos = CONT.SE(TabelaLaudos[Status]; "Concluido")
        TAT_Medio      = MEDIA(TabelaLaudos[TAT_Dias])
        Pct_Atrasados  = CONT.SE(TabelaLaudos[TAT_Dias]; ">"&$Meta_Prazo)
                         / CONT.NUM(TabelaLaudos[TAT_Dias])
        """, "excel") +
    step([
        ("Monte a area de KPIs", "Em uma aba Painel, crie tres cartoes: Producao, TAT medio e "
         "% Atrasados."),
        ("Crie os slicers", "Selecione a TabelaLaudos e insira segmentacoes de dados (slicers) por "
         "<b>Mes</b> e <b>Setor</b>."),
        ("Adicione as visualizacoes", "Barras horizontais para TAT por setor, com <b>linha de "
         "meta</b>; linhas para a evolucao mensal."),
        ("Formate", "Remova linhas de grade, use no maximo 4 cores, texto maior que 10pt, fonte "
         "dos dados visivel."),
    ]) +
    callout("tip", "Teste dos 10 segundos",
        "Filtre por um setor e um mes: os tres KPIs e os graficos devem se atualizar e responder "
        "as tres perguntas <b>em menos de 10 segundos</b>.")
)

cad.section("lab6-powerquery", "Lab 6 — Automatizar a limpeza com Power Query",
    p("Objetivo: gravar a receita de limpeza no Power Query para que o relatorio mensal vire "
      "questao de clicar em <b>Atualizar</b>.") +
    step([
        ("Importe o CSV", "No Excel: <kbd>Dados</kbd> \u2192 <kbd>Obter Dados</kbd> \u2192 "
         "<i>De Texto/CSV</i>. Selecione o arquivo exportado do LIS/SISP."),
        ("Promova os cabecalhos", "No editor do Power Query, use <i>Usar Primeira Linha como "
         "Cabecalho</i> para eliminar os titulos do sistema."),
        ("Substitua nulos", "Em cada coluna critica, substitua <i>null</i> por 'Nao informado' ou 0."),
        ("Divida DataHora", "Divida a coluna de data-hora em <b>Data</b> e <b>Hora</b>; depois crie "
         "a coluna <code>TAT_Dias</code>."),
        ("Fechar e Carregar", "Carregue no modelo de dados. Na proxima exportacao, basta "
         "<kbd>Dados</kbd> \u2192 <kbd>Atualizar Tudo</kbd>."),
    ]) +
    ficha("g", "O resultado",
        "A limpeza que hoje consome <b>2 dias</b> passa a levar <b>30 segundos</b> por mes. O "
        "processo fica deterministico, auditavel e repetivel.")
)

# =================================================================
# PARTE 4 - CENARIOS
# =================================================================
cad.grp("Parte 4 · Cenarios e aplicacoes praticas",
        "Quatro situacoes reais da POLITEC para treinar decisao, visual e automacao.")

cad.section("cenario-grafico-3d", "Cenario 1 — O grafico 3D que enganou o Secretario",
    p("Um relatorio apresenta uma suposta <i>queda drastica</i> no backlog de DNA. Voce percebe "
      "que o eixo Y comeca em 800. Preciso reconstruir o grafico e explicar o erro.") +
    kpi([
        ("900 \u2192 850", "Valores reais (Jan \u2192 Abr)"),
        ("5%", "Queda real"),
        ("80%", "Queda percebida no 3D"),
    ]) +
    grid2([
        ("Passos para corrigir",
         ul(["Refazer o grafico em <b>2D</b>.",
             "Fixar o eixo Y em <b>zero</b>.",
             "Adicionar titulo, mes e fonte dos dados.",
             "Reapresentar ao Secretario com a escala honesta."])),
        ("Visuais indicados",
         ul(["<b>Colunas</b> para a evolucao mensal do backlog.",
             "Destaque na <b>meta</b> de backlog.",
             "Nota de rodape com a variacao real (%)"])),
    ]) +
    callout("err", "Nao basta 'tirar o 3D'",
        "O problema nao era o efeito 3D — era o <b>eixo truncado</b>. Sem corrigir a escala, o "
        "grafico continua enganoso mesmo em 2D.")
)

cad.section("cenario-transparencia", "Cenario 2 — Portal de transparencia para o MP e a Defensoria",
    p("A POLITEC recebe muitos oficios pedindo os mesmos dados de TAT. A proposta e publicar um "
      "painel em Power BI que o MP e a Defensoria acessem sozinhos.") +
    step([
        ("Preparar a base", "Aplicar o <b>Pre-ETL</b>: UTF-8, cabecalho limpo, tipagem correta, "
         "sem linhas de total."),
        ("Modelar", "Criar tabela fato de laudos e dimensoes de setor, tipo de exame e calendario "
         "(modelo estrela)."),
        ("Publicar", "Subir o painel para a nuvem com permissoes de leitura para os orgaos externos."),
        ("Comunicar", "Divulgar o link e reduzir o fluxo de oficios; treinar a equipe para apontar "
         "ao portal."),
    ]) +
    kpi([
        ("TAT por comarca", "Autoatendimento"),
        ("Menos oficios", "Menos burocracia"),
        ("Accountability", "Prestacao de contas"),
    ]) +
    ficha("g", "Resultado esperado",
        "Do <b>PDF estatico</b> ao <b>portal interativo</b>: MP e Defensoria filtram dados de TAT "
        "por tipo de crime e comarca em tempo real, e a POLITEC libera servidores para a tecnica.")
)

cad.section("cenario-automacao-mensal", "Cenario 3 — Automatizar o relatorio de 4 planilhas",
    p("O relatorio de producao consome 2 dias por mes, consolidando manualmente 4 planilhas de "
      "setores. A meta e automatizar com uma pasta de entrada e Power Query.") +
    flow_h([
        ("\U0001f4c1", "Pasta Entrada_Mensal"),
        ("\U0001f50d", "Power Query le tudo"),
        ("\U0001f9f9", "Limpeza automatica"),
        ("\U0001f4ca", "Relatorio consolidado"),
    ]) +
    step([
        ("Criar a pasta", "Uma pasta <b>Entrada_Mensal</b> onde cada setor salva seu arquivo "
         "mensal no padrao definido."),
        ("Conectar a pasta", "No Power Query, <i>Obter Dados \u2192 De Pasta</i>; ele empilha os "
         "arquivos automaticamente."),
        ("Aplicar a receita", "Promover cabecalhos, substituir nulos, criar TAT e Mes_Emissao."),
        ("Atualizar mensalmente", "Salvar os arquivos na pasta e clicar em <b>Atualizar Tudo</b>."),
    ]) +
    kpi([
        ("2 dias", "Tempo antes"),
        ("30s", "Tempo depois"),
        ("99%", "Reducao de tempo"),
    ])
)

cad.section("cenario-integracao-seguranca", "Cenario 4 — Inteligencia integrada de seguranca publica",
    p("O horizonte do BI na POLITEC/MT e integrar dados periciais a outros dados de seguranca "
      "publica (PM, PC, Bombeiros) em uma plataforma unica.") +
    grid2([
        ("O que a integracao permite",
         ul(["Cruzar dados periciais com boletins de ocorrencia.",
             "Identificar padroes regionais de criminalidade.",
             "Apoiar a alocacao de recursos periciais por comarca.",
             "Subsidiar politicas publicas baseadas em evidencia."])),
        ("Pre-requisitos",
         ul(["Nomenclatura padronizada entre orgaos.",
             "<b>ETL</b> robusto e auditavel para cada fonte.",
             "Modelo relacional (estrela) bem definido.",
             "Governanca e LGPD no tratamento dos dados."])),
    ]) +
    callout("note", "Visao de futuro",
        "Para Mato Grosso, isso representa a possibilidade de <b>cruzar dados periciais com dados "
        "policiais</b> em uma unica plataforma — a visao de inteligencia de seguranca publica que "
        "o curso prepara para os proximos modulos.")
)

# =================================================================
# PARTE 5 - FECHAMENTO
# =================================================================
cad.grp("Parte 5 · Fechamento",
        "Resumo, ponte para o Dia 4, tarefa de casa, quiz, glossario e referencias.")

cad.section("resumo-dia3", "Fechamento do Dia 3: a ponte para a analise avancada",
    p("Reunimos, em dois blocos, os conceitos que sustentam a reta final do curso.") +
    grid2([
        ("\U0001f305 Manha — Organizacao e Visualizacao",
         ul(["Validacao e limpeza: pre-requisitos, nunca opcionais.",
             "Dado sujo na pericia = prova contaminada.",
             "Escolha o grafico pela pergunta, nao pela estetica.",
             "Um mini-painel bem feito vale mais que 50 paginas de texto.",
             "Tufte: sem chartjunk; Cairo: sem escalas enganosas."])),
        ("\U0001f306 Tarde — Ferramentas e ETL",
         ul(["Excel: analise flexivel e controle diario do perito.",
             "Power BI: inteligencia institucional escalavel.",
             "ETL (Power Query): limpe uma vez, atualize para sempre.",
             "UTF-8 + cabecalhos limpos = 90% dos erros de BI evitados.",
             "Relatorio de 2 dias \u2192 30 segundos com automacao."])),
    ]) +
    ficha("p", "A frase do dia",
        "Excelencia tecnica do laudo pericial deve ser espelhada pela <b>excelencia analitica</b> "
        "dos dados que o gerenciam. — Prof. Renato Rosa")
)

cad.section("ponte-dia4", "O que vem a seguir: Dia 4",
    p("No Dia 4, colocamos a mao na massa diretamente no <b>Power BI Desktop</b>: interface, "
      "conexao de dados reais, modelagem relacional e a construcao do primeiro dashboard funcional "
      "de gestao pericial — do zero ao painel publicado.") +
    step([
        ("Interface do Power BI Desktop", "Navegacao, paineis e a logica da ferramenta."),
        ("Conexao e importacao de dados", "Conectar ao CSV preparado da POLITEC."),
        ("Modelagem dimensional", "Tabelas fato, dimensao e relacionamentos."),
        ("Primeiro dashboard funcional", "KPIs, graficos e slicers — ao vivo."),
    ]) +
    callout("tip", "Chegue preparado",
        "A base que voce limpou e estruturou no Dia 3 e exatamente o que vamos importar no Dia 4. "
        "Sem o Pre-ETL, o dashboard nao decola.")
)

cad.section("tarefa-casa", "Tarefa de casa: preparando para o Dia 4",
    p("Antes do Dia 4, complete estas tres tarefas praticas para chegar pronto ao laboratorio de "
      "Power BI.") +
    checklist([
        "Baixe o <b>Power BI Desktop</b> em powerbi.microsoft.com e instale no notebook que "
        "trouxer para a aula.",
        "Prepare sua <b>base CSV</b>: exporte uma amostra do seu setor ou use a base simulada do "
        "professor; salve como CSV UTF-8 com cabecalhos limpos.",
        "Identifique <b>3 perguntas</b> de gestao que voce mais precisa responder com dados — elas "
        "guiarao o design do seu primeiro dashboard.",
    ]) +
    ficha("a", "Por que isso importa",
        "Chegar com a base pronta e as perguntas definidas transforma o Dia 4 de 'aula expositiva' "
        "em <b>laboratorio real</b>. O design do dashboard comeca pela pergunta.")
)

cad.section("quiz-final", "Quiz final do Dia 3",
    q("A validacao de dados bem configurada reduz em ate quanto o tempo gasto posteriormente com limpeza?",
      ["20%", "50%", "80%", "100%"], 2,
      "Os slides destacam reducao de ate 80% no tempo de limpeza.") +
    q("Qual funcao remove espacos extras no inicio e no fim de um texto?",
      ["PRI.MAIUSCULA()", "ARRUMAR() / TRIM()", "SUBSTITUIR()", "CONCATENAR()"], 1,
      "ARRUMAR (TRIM) faz o corte de espacos das bordas.") +
    q("Na remocao de duplicatas de laudos, a chave unica recomendada e:",
      ["A linha inteira", "Apenas o setor", "Numero do laudo + data", "O nome do perito"], 2,
      "O par numero do laudo + data identifica o registro sem remover laudos legitimos.") +
    q("Segundo a curiosidade do setor, qual fracao do tempo de projeto os analistas gastam limpando dados?",
      ["20%", "40%", "60%", "80%"], 2,
      "Cerca de 60% limpando e apenas 40% analisando de fato.") +
    q("Segundo Alberto Cairo, uma escala honesta de grafico deve:",
      ["Comecar no valor minimo", "Comecar no zero", "Ser sempre logaritmica", "Ocultar a fonte"], 1,
      "Escala Y sempre inicia em zero; truncar exagera pequenas variacoes.") +
    q("Qual grafico e mais adequado para mostrar a evolucao mensal de laudos ao longo do tempo?",
      ["Pizza", "Rosca", "Linhas", "Colunas 3D"], 2,
      "Linhas respondem a 'como mudou ao longo do tempo'.") +
    q("O termo cunhado por Edward Tufte para o lixo visual em graficos e:",
      ["Data-ink", "Chartjunk", "Pareto", "Outlier"], 1,
      "Chartjunk e qualquer elemento visual que nao agrega informacao.") +
    q("No caso do grafico 3D, uma queda real de 5% parecia uma reducao de aproximadamente:",
      ["8%", "20%", "50%", "80%"], 3,
      "O eixo truncado em 800 fez a queda de 5% parecer proxima de 80%.") +
    q("Para TAT medio por setor (nomes longos), o grafico recomendado e:",
      ["Pizza 3D", "Barras horizontais", "Linhas", "Rosca"], 1,
      "Barras horizontais acomodam nomes longos e a linha de meta.") +
    q("O processo ETL de Kimball significa:",
      ["Excel, Tabela, Linha", "Extract, Transform, Load", "Entrada, Tipo, Limpeza",
       "Extrair, Testar, Linkar"], 1,
      "Extract (extrair), Transform (transformar), Load (carregar).") +
    q("Antes de importar um CSV no Power BI, o Pre-ETL recomenda salvar como:",
      ["CSV ANSI com ponto e virgula", "CSV UTF-8 com cabecalhos limpos",
       "XLSX com macros", "PDF tabulado"], 1,
      "UTF-8 preserva acentos; cabecalhos limpos evitam erros de importacao.") +
    q("A grande vantagem do Power Query na pericia e:",
      ["Deixar o grafico mais bonito", "Gravar a receita de limpeza e repeti-la ao atualizar",
       "Aumentar o limite de linhas do Excel", "Eliminar a necessidade de validacao"], 1,
      "Limpeza configurada uma vez e replicada automaticamente a cada atualizacao.") +
    q("Por que pintar celulas de amarelo para indicar 'atrasado' e um erro no BI?",
      ["Deixa o arquivo pesado", "O BI nao le cores; e preciso uma coluna com o status",
       "A cor amarela nao existe no BI", "Impede a publicacao na nuvem"], 1,
      "O motor le valores: crie uma coluna Status_Atraso com texto.") +
    q("Qual e o volume de dados tipico que justifica migrar do Excel para o Power BI?",
      ["Acima de 1.000 linhas", "Acima de 5.000 linhas", "Dezenas de milhoes de linhas",
       "Somente textos"], 2,
      "O Power BI processa dezenas de milhoes de linhas; o Excel fica lento muito antes.") +
    q("Segundo a filosofia da automacao, o objetivo e:",
      ["Substituir o perito por software", "Fazer a tecnologia trabalhar para o perito",
       "Eliminar o uso de planilhas", "Reduzir a equipe do laboratorio"], 1,
      "A automacao libera o perito da tarefa mecanica para a analise tecnica.")
)

cad.section("glossario", "Glossario do Dia 3",
    glossary([
        ("Validacao de dados", "Conjunto de regras (listas, datas, limites) que impede a entrada de dados invalidos. Reduz ate 80% do tempo de limpeza posterior."),
        ("DROP / Lista suspensa", "Lista de valores permitidos em uma coluna. Padroniza o vocabulario pericial e evita variacoes de escrita."),
        ("ARRUMAR / TRIM", "Remove espacos extras no inicio e no fim de um texto."),
        ("PRI.MAIUSCULA", "Padroniza a capitalizacao (ex.: cuiaba -> Cuiaba)."),
        ("SUBSTITUIR", "Troca termos antigos por padroes institucionais (ex.: Ex. Necropsia -> Necropsia)."),
        ("Duplicata", "Registro repetido que infla a producao. Removida pela chave unica (numero do laudo + data)."),
        ("Chartjunk", "Termo de Tufte para elementos visuais sem informacao: sombras 3D, gradientes, cores neon."),
        ("Data-ink ratio", "Proporcao de tinta que representa dados. Deve ser maximizada."),
        ("Escala Y no zero", "Regra de Cairo: o eixo vertical comeca em zero para nao exagerar variacoes."),
        ("ETL", "Extract, Transform, Load — extrair, transformar e carregar dados num modelo de BI (Kimball)."),
        ("Modelo estrela", "Organizacao em tabela fato (medidas) + tabelas dimensao (contexto), relacionadas."),
        ("Power Query", "Motor de ETL embutido no Excel e no Power BI que grava a receita de limpeza e a repete ao atualizar."),
        ("Pre-ETL", "Checklist no Excel antes de importar: UTF-8, cabecalho limpo, tipagem correta, limpeza de lixo."),
        ("TAT", "Turnaround Time — tempo entre recebimento da requisicao e emissao do laudo."),
        ("Slicer", "Filtro visual (ex.: Mes, Setor) que atualiza KPIs e graficos de um painel."),
    ])
)

cad.section("referencias", "Autores e referencias do Dia 3",
    p("As referencias que sustentam o dia inteiro:") +
    tbl(["Autor", "Obra", "Por que importa"],
        [["<b>Alberto Cairo</b>", "\"The Truthful Art\"",
          "Visualizacao como comunicacao da verdade operacional. Responsabilidade etica do grafico."],
         ["<b>Edward Tufte</b>", "\"The Visual Display of Quantitative Information\"",
          "Principios de clareza, data-ink ratio e a guerra ao chartjunk."],
         ["<b>Ralph Kimball</b>", "\"The Data Warehouse Toolkit\"",
          "Fundamentos do ETL, modelagem dimensional e a arquitetura de todo BI moderno."]],
        num_cols=[]) +
    ficha("g", "Proximo passo — Dia 4",
        "Entramos de cabeca no <b>Power BI Desktop</b>: interface, conexao de dados reais, "
        "modelagem relacional e a construcao do primeiro dashboard funcional de gestao pericial. "
        "A base limpa hoje vira o painel de amanha.")
)

cad.build()
