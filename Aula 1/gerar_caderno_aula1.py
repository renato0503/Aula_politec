# -*- coding: utf-8 -*-
"""Gerador do caderno da Aula 1 - POLITEC/MT.

Tema: Fundamentos da Analise de Dados e Estatistica aplicada a Pericia Criminal.
Conteudo derivado dos slides Dia-1-Politec.pdf (37 paginas).

Rode:  python gerar_caderno_aula1.py
PDF:   python ..\\exportar_pdf.py 1
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from caderno_lib import (Caderno, p, h3, ul, checklist, ficha, callout, tbl,
                         code, step, q, aplicab, grid2, flow_h, kpi,
                         antesdepois, legenda, glossary, bar_chart)

cad = Caderno(
    out=str(pathlib.Path(__file__).resolve().parent / "caderno-dia1.html"),
    dia=1,
    kicker="Aula 1 · Fundamentos da Analise",
    headline="Fundamentos da Analise de Dados e Estatistica aplicada a Pericia",
    sub="Do vestigio bruto a decisaao: o ciclo de dados na Pericia Criminal, a piramide DIKW, "
        "qualidade da informacao e a estatistica descritiva que sustenta a gestao dos laboratorios "
        "e do IML da POLITEC/MT.",
    meta="Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 1 · Modulos 1 e 2",
    descricao="Caderno do Dia 1 do Curso de Capacitacao POLITEC/MT: fundamentos da analise de dados "
              "e estatistica aplicada a pericia criminal. Ciclo de dados, piramide DIKW, principio de "
              "Locard, tipos e qualidade da informacao, estatistica descritiva, dispersao, boxplot, "
              "histogramas, correlacao x causalidade e outliers.",
)

# =================================================================
# ABERTURA
# =================================================================
cad.grp("Abertura", "O que este caderno cobre, como usa-lo, o mapa do Dia 1 e o roadmap do curso.")

cad.section("boas-vindas", "Bem-vindo ao caderno do Dia 1",
    p("Este caderno nao substitui a aula — ele <b>ancora</b> o que foi discutido em sala e "
      "vai alem. Aqui voce encontra os conceitos explicados com calma, exemplos de bancada da "
      "POLITEC, pegadinhas classicas, laboratorios passo a passo e um quiz para fechar.") +
    p("O fio condutor do dia e simples: <b>todo vestigio vira dado, todo dado vira decisao</b>. "
      "Entre o vestigio recolhido em campo e a decisao do gestor ou do juizo existe uma cadeia "
      "de tratamento. Se qualquer elo falha, a decisao — tecnica ou judicial — fica comprometida.") +
    legenda([
        ("\U0001f4d6", "Leitura guiada", "Percorra as <b>Partes 1 e 2</b> na ordem. Cada secao tem um caso da POLITEC."),
        ("\U0001f9ea", "Pratica", "Na <b>Parte 3</b> estao 7 laboratorios curtos, de papel e raciocinio, para fixar conceitos."),
        ("\U0001f3af", "Cenarios", "Na <b>Parte 4</b>, 4 situacoes reais da POLITEC para treinar decisao com dados."),
        ("\u2705", "Fechamento", "Na <b>Parte 5</b>: quiz com 15 perguntas, folha de cola e referencias."),
    ]) +
    callout("note", "Como navegar",
        "Use o indice a esquerda (tem busca), o botao <b>Tema</b> para alternar claro/escuro e "
        "<b>Imprimir / PDF</b> para levar o caderno em papel. Os blocos com botao <b>Copiar</b> "
        "reproduzem formulas e listas sem erro de digitacao.")
)

cad.section("como-usar", "Como usar este caderno (roteiro de estudo)",
    p("O caderno foi desenhado para ser lido em <b>tres velocidades</b>. Escolha a sua conforme o "
      "tempo disponivel. O importante e que cada secao termina com algo que voce consegue aplicar "
      "na rotina do laboratorio ou do IML.") +
    grid2([
        ("\u26a1 Leitura rapida (20 min)",
         ul(["Leia os titulos e os <b>blocos coloridos</b> (fichas e callouts).",
             "Veja os graficos de barras e as tabelas.",
             "Faca o quiz final para se situar."])),
        ("\U0001f4d6 Leitura completa (2-3 h)",
         ul(["Siga as Partes 1 e 2 na ordem.",
             "Resolva os 7 laboratorios da Parte 3 no papel.",
             "Leia os 4 cenarios da Parte 4 e escreva suas respostas."])),
        ("\U0001f9e0 Estudo ativo (recomendado)",
         ul(["Leia a secao e <b>feche o caderno</b>.",
             "Explique o conceito em voz alta, com um exemplo seu.",
             "Volte e confira; refaca os labs com dados do seu setor."])),
    ]) +
    checklist([
        "Tenho em mente <b>uma pergunta real</b> do meu setor para testar os conceitos.",
        "Sei onde esta a folha de cola (Parte 5) para consulta rapida.",
        "Reservei um caderno ou arquivo para anotar os dados dos labs.",
        "Terminei o dia sabendo a diferenca entre <b>dado, metrica e indicador</b>.",
    ]) +
    callout("tip", "A regra do caderno",
        "Nenhum conceito fica no abstrato: cada um vira um caso da POLITEC. Se voce terminar uma "
        "secao sem um exemplo proprio, releia — o objetivo nao e decorar, e saber usar.")
)

cad.section("mapa-do-dia", "Mapa do Dia 1: o que vamos aprender",
    p("O dia tem dois modulos. A manha constroi a base conceitual (o dado e sua qualidade); a "
      "tarde entrega as ferramentas estatisticas para descrever o que os dados mostram.") +
    grid2([
        ("\u2600\ufe0f Manha (08h-12h) · Modulo 1 — Fundamentos da Analise",
         ul(["O <b>ciclo de dados</b> na Pericia Criminal",
             "A <b>piramide DIKW</b> aplicada a ciencia forense",
             "O <b>principio de Locard</b> e a era digital",
             "<b>Tipos de dados</b> nos laboratorios da POLITEC",
             "Os <b>4 pilares</b> da qualidade da informacao",
             "Dashboards que funcionam sob pressao (Stephen Few)",
             "Dado, metrica e indicador; o ciclo de dados do setor"])),
        ("\U0001f306 Tarde (13h-17h) · Modulo 2 — Fundamentos Estatisticos",
         ul(["<b>Estatistica descritiva</b>: a linguagem da gestao pericial",
             "Tendencia central: <b>media, mediana e moda</b> passo a passo",
             "Dispersao: <b>variancia e desvio padrao</b> na mao",
             "O <b>boxplot</b> de Tukey e os histogramas",
             "<b>Correlacao x causalidade</b>",
             "<b>Outliers</b> e Cisnes Negros",
             "Metricas de gestao: TAT, backlog, produtividade e qualidade"])),
    ]) +
    ficha("g", "Objetivo do dia",
        "Ao final, voce tera ferramentas concretas para transformar <b>dados periciais em decisoes "
        "tecnicas e gerenciais mais precisas e defensaveis juridicamente</b>. Nao e sobre decorar "
        "formulas: e sobre saber qual pergunta o dado responde — e qual ele <i>nao</i> responde.")
)

cad.section("roadmap-curso", "Roadmap do curso: do vestigio ao dashboard (Dia 1 a Dia 5)",
    p("O Dia 1 e a fundacao de uma capacitacao de cinco dias. Cada encontro entrega uma camada nova "
      "sobre a anterior — e todas voltam, no final, ao mesmo objetivo: <b>decidir melhor com "
      "evidencia</b>. Conhecer o mapa inteiro ajuda voce a enxergar onde o dia de hoje se encaixa.") +
    tbl(["Dia", "Tema", "O que voce leva", "Ferramenta"],
        [["<b>Dia 1</b>", "Fundamentos da analise e estatistica descritiva",
          "Ciclo do dado, DIKW, qualidade da informacao, media/mediana/dispersao, outliers.",
          "Papel, raciocinio e planilha"],
         ["<b>Dia 2</b>", "Planilhas e manipulacao de dados periciais",
          "Limpeza, padronizacao, tabelas estruturadas, referencias, filtros e o painel de backlog.",
          "Excel / Google Sheets"],
         ["<b>Dia 3</b>", "Organizacao, visualizacao e ETL",
          "Validacao na entrada, graficos honestos, Excel x Power BI, Power Query e preparacao de bases.",
          "Excel + Power Query"],
         ["<b>Dia 4</b>", "Business Intelligence com Power BI",
          "Interface, conexao de dados, visuais, publicacao, workspaces, governanca, LGPD e DAX.",
          "Power BI Desktop / Service"],
         ["<b>Dia 5</b>", "Encerramento e consolidacao do ecossistema de dados",
          "Projeto aplicado, integracao dos sistemas, governanca corporativa e proximos passos do BI.",
          "Ecossistema completo"]],
        num_cols=[]) +
    flow_h([
        ("\U0001f4d0", "Dia 1 · Fundamentos"),
        ("\U0001f4d2", "Dia 2 · Planilha"),
        ("\U0001f9f9", "Dia 3 · ETL"),
        ("\U0001f4ca", "Dia 4 · BI"),
        ("\U0001f3c1", "Dia 5 · Consolidacao"),
    ]) +
    ficha("p", "A logica da escada",
        "Nao se constroi um dashboard (Dia 4) sem uma base limpa (Dias 2 e 3); nao se limpa uma "
        "base sem saber o que e <b>qualidade de dado</b> (Dia 1). O curso e uma escada — pular "
        "degraus faz o painel nascer quebrado.")
)

# =================================================================
# PARTE 1 - MODULO 1
# =================================================================
cad.grp("Parte 1 · Modulo 1 — Fundamentos da Analise",
        "O caminho do vestigio ate a inteligencia: DIKW, Locard, tipos de dados, qualidade da informacao e a pratica do setor.")

cad.section("ciclo-dados", "O ciclo de dados na Pericia Criminal",
    p("Cada vestigio coletado em campo percorre um caminho estruturado ate se tornar inteligencia "
      "para a investigacao e a decisao judicial. Esse caminho e o <b>ciclo de vida do dado pericial</b>.") +
    flow_h([
        ("\U0001f50d", "Coleta em campo"),
        ("\U0001f4dd", "Registro"),
        ("\U0001f4c2", "Armazenamento"),
        ("\U0001f50e", "Analise"),
        ("\U0001f4ca", "Relatorio"),
        ("\u2696\ufe0f", "Decisao"),
    ]) +
    p("O ciclo repete o mesmo cuidado da <b>cadeia de custodia</b> das evidencias fisicas, agora "
      "aplicado ao dado. Cada etapa deixa rastro e pode ser auditada.") +
    aplicab(
        "Sempre que um vestigio entra na instituicao — do swab de DNA ao laudo narrativo.",
        "Porque a decisao final (mandado, denuncia, condenacao) depende de o dado ter percorrido "
        "todo o ciclo sem quebra nem contaminacao.",
        "Um exame de toxicologia entra as 14h30 e e registrado; 3 dias depois o resultado vira "
        "laudo; o laudo alimenta o relatorio gerencial do IML e, por fim, a decisao do delegado.") +
    callout("tip", "A pergunta que guia tudo",
        "Em cada etapa do ciclo, pergunte: <b>&ldquo;o dado que sai daqui e confiavel para quem vem "
        "depois?&rdquo;</b>. Se a resposta for nao, o problema nao esta na proxima etapa — esta aqui.")
)

cad.section("dikw", "A piramide DIKW na ciencia forense",
    p("A piramide <b>DIKW</b> foi proposta por <b>Russell Ackoff</b> (1989) para descrever a evolucao "
      "do dado bruto ate a acao estrategica: <b>D</b>ata (dado) \u2192 <b>I</b>nformation (informacao) "
      "\u2192 <b>K</b>nowledge (conhecimento) \u2192 <b>W</b>isdom (sabedoria).") +
    flow_h([
        ("\U0001f4be", "Dado"),
        ("\U0001f4cb", "Informacao"),
        ("\U0001f9e0", "Conhecimento"),
        ("\U0001f3af", "Sabedoria"),
    ]) +
    tbl(["Nivel", "Pergunta que responde", "Quem usa na rotina pericial"],
        [["<b>Dado</b>", "O que foi registrado?", "O sistema / a ficha de campo"],
         ["<b>Informacao</b>", "O que isso significa quando cruzado com outras fontes?", "O analista"],
         ["<b>Conhecimento</b>", "Que padrao se repete? O que isso implica?", "O perito / o gestor"],
         ["<b>Sabedoria</b>", "O que devemos <i>fazer</i> agora?", "O delegado / o diretor"]],
        num_cols=[]) +
    callout("err", "Pegadinha: parar no dado",
        "Muitas instituicoes acumulam <b>dados</b> e chamam isso de gestao. Sem os degraus de "
        "informacao e conhecimento, o acervo e apenas um cemiterio de registros — ninguem decide "
        "nada com ele.")
)

cad.section("dikw-dna", "DIKW na pratica: o caso do DNA na POLITEC",
    p("Veja como cada nivel da piramide se manifesta em um caso real de analise de DNA. O mesmo "
      "vestigio, visto em quatro alturas diferentes, muda completamente o que se pode fazer com ele.") +
    step([
        ("Dado", "&ldquo;Mancha biologica de 5 ml, coletada as 14h30, Local X.&rdquo; — o <b>registro bruto</b> "
                 "da ocorrencia, sem qualquer interpretacao."),
        ("Informacao", "&ldquo;O perfil genetico da mancha coincide com o banco de dados de condenados.&rdquo; "
                       "— o dado <b>processado e cruzado</b> com outras fontes."),
        ("Conhecimento", "&ldquo;Este perfil esta ligado a 3 outros locais de crime nao resolvidos no mesmo "
                         "bairro nos ultimos 6 meses.&rdquo; — um <b>padrao</b> identificado."),
        ("Sabedoria", "&ldquo;Emitir oficio urgente a Delegacia solicitando mandado de busca e apreensao no "
                      "endereco vinculado ao perfil.&rdquo; — <b>acao estrategica</b> baseada em evidencia."),
    ]) +
    ficha("p", "Leitura gerencial",
        "O salto de dado para sabedoria nao e automatico. Ele exige metodo (analise), contexto "
        "(outros casos) e responsabilidade (a decisao). O analista de dados periciais e o "
        "profissional que constroi essa ponte.")
)

cad.section("locard", "O principio de Locard e a era digital",
    p("<b>Edmond Locard</b> (1877-1966) foi pioneiro da ciencia forense e criador do primeiro "
      "laboratorio policial do mundo, em Lyon, em 1910. Ele demonstrou que evidencias fisicas, "
      "analisadas cientificamente, valem mais do que testemunhos.") +
    ficha("a", "A frase que fundou a criminalistica",
        "&ldquo;Todo contato deixa um vestigio.&rdquo; — Principio de Locard, adaptado a era digital: todo "
        "contato, fisico ou digital, <b>deixa um dado</b>.") +
    p("Na era digital, o principio se expande. Cada transacao, cada acesso, cada equipamento de "
      "laboratorio gera registros. A missao da POLITEC moderna e coletar, preservar e analisar esses "
      "dados com a mesma rigidez da cadeia de custodia tradicional.") +
    callout("note", "A equivalencia que sustenta tudo",
        "Um dado digital corrompido ou mal registrado tem o <b>mesmo peso juridico</b> de uma "
        "evidencia fisica contaminada. A cadeia de custodia dos dados e tao critica quanto a cadeia "
        "de custodia das evidencias fisicas.")
)

cad.section("tipos-dados", "Tipos de dados na POLITEC: a realidade dos laboratorios",
    p("Os dados produzidos e consumidos pela POLITEC se dividem em <b>tres grandes categorias</b>. "
      "Compreende-las e o primeiro passo para escolher a estrategia correta de analise, "
      "armazenamento e integracao.") +
    tbl(["Categoria", "Como se parece", "Exemplos na POLITEC"],
        [["<b>Estruturados</b>",
          "Altamente organizados, em linhas e colunas. Facil de filtrar, somar e cruzar.",
          "Estoque de reagentes; banco de perfis geneticos (CODIS); planilhas de entrada/saida de "
          "exames no IML; resultados numericos de toxicologia (ex.: 0,8 mg/L)."],
         ["<b>Semiestruturados</b>",
          "Tem marcadores (tags), mas nao obedecem a um esquema rigido de tabela.",
          "Arquivos XML/JSON de integracao entre o sistema de gestao da POLITEC e o banco nacional "
          "de impressoes digitais ou de DNA."],
         ["<b>Nao estruturados</b>",
          "Sem formato predefinido, ricos em contexto. Cerca de <b>80%</b> do acervo pericial.",
          "Fotografias de local de crime; laudos em texto livre; audios de entrevistas; varreduras "
          "3D balisticas; videos de necropsias."]],
        num_cols=[]) +
    aplicab(
        "Antes de escolher a ferramenta (planilha, BI, banco de dados ou IA), classifique o dado.",
        "Porque cada tipo pede um tratamento diferente: dado estruturado quer tabela; texto livre "
        "quer analise semantica; imagem quer visao computacional.",
        "O estoque de reagentes (estruturado) cabe numa planilha; o laudo narrativo (nao estruturado) "
        "precisa de analise de texto ou IA para virar indicador.") +
    callout("err", "Nao trate tudo como tabela",
        "Forcar dado nao estruturado dentro de colunas e a causa numero um de perda de contexto. "
        "A descricao da dinamica de um homicidio nao cabe em um menu suspenso.")
)

cad.section("nao-estruturado", "Por que 80% do acervo e a maior mina de ouro da POLITEC",
    p("Fotografias, laudos narrativos e varreduras 3D contem contexto que nenhum campo de banco de "
      "dados consegue capturar completamente. A descricao da dinamica de um homicidio, por exemplo, "
      "exige linguagem tecnica livre que transcende checkboxes.") +
    p("O desafio crescente e desenvolver metodologias — inclusive com <b>inteligencia artificial</b> — "
      "para extrair padroes estruturados do nao estruturado: reconhecimento de padroes em fotos, "
      "analise semantica de laudos, transcricao e indexacao de audios.") +
    grid2([
        ("O que se perde hoje",
         ul(["Contexto rico preso em PDFs e fotos",
             "Padroes que ninguem consegue cruzar manualmente",
             "Tempo do perito gasto lendo, nao analisando"])),
        ("O que a IA pode destravar",
         ul(["Classificacao automatica de fotos de local",
             "Extracao de entidades de laudos (arma, vitima, local)",
             "Indice buscavel de audios e videos"])),
    ]) +
    ficha("g", "A tese da secao",
        "A maior reserva de inteligencia da POLITEC <b>nao esta</b> nos campos organizados — esta nos "
        "80% que hoje ninguem consegue consultar. Quem aprender a estruturar essa massa primeiro sai "
        "na frente.")
)

cad.section("cadeia-custodia", "Caso real: a quebra da cadeia de custodia por dado sujo",
    p("Diversos processos criminais foram anulados no Brasil nao porque a pericia estava errada, mas "
      "porque o <b>registro do dado falhou</b>.") +
    step([
        ("O contexto", "A qualidade do dado nao e responsabilidade da &ldquo;TI&rdquo; — e <b>validade "
                        "juridica</b>. Um dado inconsistente invalida a prova, independentemente da "
                        "excelencia tecnica da analise."),
        ("O erro", "Um perito anotou a hora da coleta como <b>14:00</b>, mas o sistema registrou o "
                   "recebimento no laboratorio como <b>13:30</b> — erro de digitacao ou de fuso horario."),
        ("A consequencia", "A defesa alegou quebra da cadeia de custodia. O laudo, tecnicamente "
                           "perfeito, foi declarado <b>nulo</b> pelo juizo."),
    ]) +
    antesdepois(
        "Focar na excelencia tecnica da analise e deixar o registro para depois.",
        "Tratar o registro como parte da prova: hora, local, responsavel e metodo conferidos na origem.",
        "Foco so na tecnica", "Registro e tecnica juntos") +
    ficha("r", "Licao",
        "Um dado sujo derruba um laudo perfeito. Na pericia, <b>qualidade do registro e qualidade "
        "da prova</b>.")
)

cad.section("qualidade-4pilares", "Qualidade da informacao: os 4 pilares na pericia",
    p("Para que um dado pericial tenha valor probatorio e operacional, ele precisa atender a quatro "
      "dimensoes. A falha em qualquer pilar compromete o laudo inteiro.") +
    grid2([
        ("\U0001f3af Acuracia", "O dado reflete a realidade fisica?<br><span class='d'>Ex.: uma "
         "coordenada GPS apontando para o meio de um lago indica erro do aparelho ou do operador.</span>"),
        ("\U0001f4d0 Completude", "Faltam partes vitais?<br><span class='d'>Ex.: laudo sem assinatura "
         "do perito responsavel ou sem especificacao do metodo analitico utilizado.</span>"),
        ("\U0001f517 Consistencia", "O mesmo dado e igual em todos os sistemas?<br><span class='d'>"
         "Ex.: exame &ldquo;Positivo&rdquo; no laboratorio, mas &ldquo;Pendente&rdquo; no portal da Delegacia.</span>"),
        ("\u23f1\ufe0f Atualidade", "O dado chega em tempo de ser util?<br><span class='d'>Ex.: um "
         "laudo de embriaguez que demora 6 meses perde valor probatorio e operacional.</span>"),
    ]) +
    aplicab(
        "Ao criar ou revisar qualquer formulario, planilha ou sistema de registro pericial.",
        "Porque a qualidade se constroi na entrada — depois so resta corrigir o estrago.",
        "Ao desenhar o formulario de recebimento de exames no IML, defina campos obrigatorios "
        "(completude), validacao de faixa (acuracia), sincronizacao entre sistemas (consistencia) e "
        "prazo de registro (atualidade).") +
    callout("tip", "Teste rapido dos 4 pilares",
        "Pegue um laudo qualquer e pergunte: <b>e verdadeiro? esta completo? e igual em todo lugar? "
        "chegou a tempo?</b> Quatro &ldquo;sim&rdquo; = dado confiavel.")
)

cad.section("stephen-few", "Stephen Few e a regra dos 3 segundos",
    p("<b>Stephen Few</b>, especialista em visualizacao de dados e Business Intelligence, dedicou "
      "decadas a entender como gestores tomam decisoes sob pressao com base em informacao visual.") +
    ficha("p", "A frase que define o bom dashboard",
        "&ldquo;Dashboards devem ser legiveis em 3 segundos por um gestor sob pressao.&rdquo; — Stephen Few "
        "(<i>Information Dashboard Design</i>, 2006).") +
    p("O Diretor do IML ou o Chefe do Laboratorio nao precisa de 50 graficos. Ele precisa responder "
      "em 3 segundos:") +
    ul(["Qual e o <b>backlog critico</b> de exames pendentes?",
        "Qual <b>equipamento</b> esta parado ou em manutencao?",
        "Qual a <b>taxa de emissao de laudos</b> neste momento?"]) +
    antesdepois(
        "Uma parede de graficos, cores sem significado e numeros sem comparacao.",
        "Poucos indicadores, com meta clara, cor que aponta o que exige acao.",
        "Painel ruidoso", "Painel que responde em 3s") +
    callout("note", "A ponte com o resto do curso",
        "Essa regra conecta o Dia 1 (fundamentos) ao Dia 4 (Power BI). Um dashboard nao e um "
        "enfeite: e a resposta visual a uma pergunta de gestao, calculada a partir de dados "
        "confiaveis.")
)

cad.section("custo-dado-sujo", "Curiosidade: o custo real do dado sujo na justica",
    p("Erros em registros periciais e atrasos na digitalizacao de laudos custam <b>milhoes</b> aos "
      "cofres publicos — em horas extras, reagentes vencidos e, principalmente, em revisoes de "
      "processos judiciais que poderiam ter sido evitadas.") +
    grid2([
        ("\U0001f4b8 Impacto financeiro direto",
         ul(["Horas extras para reprocessar e corrigir registros",
             "Reagentes vencidos por planejamento baseado em dado errado",
             "Revisoes de processo e possiveis indenizacoes"])),
        ("\U0001f4c8 O poder da nomenclatura padronizada",
         "Padronizar o termo <b>&ldquo;Arma de Fogo&rdquo;</b> no sistema — eliminando variacoes como "
         "&ldquo;Revolver&rdquo;, &ldquo;arma&rdquo;, &ldquo;rvl&rdquo; ou &ldquo;pistola&rdquo; — pode aumentar em ate <b>40%</b> a eficacia "
         "dos cruzamentos estatisticos para identificar modus operandi de quadrilhas."),
    ]) +
    ficha("g", "A mensagem",
        "Padronizacao de dados nao e burocracia — e <b>inteligencia operacional</b>. Cada campo bem "
        "preenchido e uma consulta futura que vai funcionar.")
)

# ---- NOVAS SECOES DO MODULO 1 ----

cad.section("dado-metrica-indicador", "Dado, metrica e indicador: qual a diferenca",
    p("Tres palavras que muita gente usa como sinonimos — e que nao sao. Confundi-las e a origem de "
      "paineis que mostram numeros bonitos e nao respondem a nenhuma pergunta de gestao.") +
    tbl(["Conceito", "Definicao", "Exemplo POLITEC", "Pergunta que responde"],
        [["<b>Dado</b>", "O registro bruto, sem tratamento.",
          "&ldquo;Laudo 4471 emitido em 12/03.&rdquo;", "O que aconteceu?"],
         ["<b>Metrica</b>", "Uma medida calculada a partir de um ou mais dados.",
          "Tempo de emissao = 7 dias (diferenca entre duas datas).", "Quanto / quanto tempo?"],
         ["<b>Indicador (KPI)</b>", "Uma metrica com <b>meta</b> e <b>direcao de sucesso</b>.",
          "&ldquo;82% dos laudos emitidos dentro do prazo de 15 dias.&rdquo;", "Estamos bem ou mal?"]],
        num_cols=[]) +
    aplicab(
        "Ao montar qualquer painel ou pedir um numero para a direcao.",
        "Porque um dado sozinho nao orienta acao; a metrica quantifica; so o indicador diz se o "
        "resultado e bom ou ruim — porque traz meta e contexto.",
        "O backlog (numero de exames pendentes) e uma <b>metrica</b>; ele so vira <b>indicador</b> "
        "quando comparado com a capacidade diaria ou com uma meta de reducao.") +
    grid2([
        ("Erro classico",
         "Entregar dado bruto (&ldquo;temos 1.200 exames pendentes&rdquo;) e chamar de indicador. "
         "Sem meta, ninguem sabe se 1.200 e muito ou pouco."),
        ("Pratica correta",
         "Transformar em: &ldquo;1.200 pendentes, <b>18% acima da meta</b> de 1.000; cresceu 12% no mes&rdquo;. "
         "Agora a frase orienta decisao."),
    ]) +
    callout("err", "KPI sem meta e so numero",
        "Se o indicador nao tem meta, direcao (quanto maior melhor, ou menor melhor) e frequencia de "
        "leitura, nao e um KPI — e decoracao. Todo painel pericial comeca pela pergunta e pela meta.")
)

cad.section("caso-integrado-swab", "Estudo de caso integrado: do swab de DNA ao mandado de busca",
    p("Vamos seguir um unico vestigio — um <b>swab de DNA</b> coletado em um local de crime — por "
      "todo o ciclo, ate virar uma acao policial concreta. Cada etapa mostra onde o dado pode ganhar "
      "ou perder valor.") +
    flow_h([
        ("\U0001f9ea", "Swab em campo"),
        ("\U0001f4dd", "Registro e custodia"),
        ("\U0001f52c", "Analise no lab"),
        ("\U0001f4be", "Perfil no CODIS"),
        ("\U0001f50e", "Cruzamento (match)"),
        ("\u2696\ufe0f", "Mandado de busca"),
    ]) +
    step([
        ("Coleta", "A equipe recolhe o swab com tecnica asseptica, fotografa o local e anota hora, "
         "temperatura e responsavel. <b>Os 4 pilares da qualidade</b> comecam aqui."),
        ("Registro e custodia", "O swab recebe um numero de cadeia de custodia. O sistema registra "
         "entrada; a hora do registro <b>tem que bater</b> com a hora da coleta (o &ldquo;dado sujo&rdquo; aqui "
         "pode anular o laudo)."),
        ("Analise no laboratorio", "A extracao do DNA gera um <b>perfil genetico</b> — dado "
         "estruturado, composto por pares de alelos. A partir daqui, e dado confiavel para cruzar."),
        ("Perfil no CODIS", "O perfil entra no banco. A qualidade do perfil (numero de marcadores) "
         "define se ele e pesquisavel ou se precisa de reanalise."),
        ("Cruzamento (match)", "O sistema aponta coincidencia com um perfil de condenado. Esse e o "
         "degrau de <b>informacao</b> da piramide DIKW — o dado virou algo acionavel."),
        ("Inteligencia", "O analista cruza o match com outros 3 locais de crime nao resolvidos no "
         "mesmo bairro: um <b>padrao</b> emerge. E o degrau de <b>conhecimento</b>."),
        ("Mandado de busca", "A policia usa o endereco vinculado ao perfil para pedir o mandado. "
         "Aqui o vestigio virou <b>sabedoria</b> — decisao estrategica baseada em cadeia integra."),
    ]) +
    ficha("g", "A moral do caso",
        "O mesmo swab pode gerar um mandado de busca ou um processo anulado. A diferenca nao esta no "
        "laboratorio — esta na <b>integridade de cada elo do ciclo</b> e na qualidade dos registros.")
)

cad.section("mapear-ciclo-dados", "Como mapear o ciclo de dados do seu setor",
    p("Voce nao consegue melhorar o que nao enxerga. Este roteiro, feito uma vez por setor, revela "
      "onde o dado nasce, onde se perde e onde esta o maior ganho de qualidade. Vale para o "
      "laboratorio de DNA, para o IML e para qualquer setor administrativo.") +
    step([
        ("Liste as entradas", "Escreva <b>tudo</b> que entra no setor: requisicoes, material "
         "biologico, amostras, oficios, laudos de outros setores, planilhas externas."),
        ("Liste as saidas", "Escreva o que sai: laudos, pareceres, relatorios gerenciais, respostas "
         "a oficios, dados enviados a outros sistemas."),
        ("Identifique os sistemas", "Marque onde cada dado e registrado (LIS, SISP, CODIS, planilha "
         "local, papel). Onde o dado vive em <b>mais de um lugar</b>, ha risco de inconsistencia."),
        ("Desenhe o fluxo", "Ligue entradas e saidas em sequencia — o mesmo desenho do ciclo de "
         "dados da primeira secao. Use post-its ou um quadro branco."),
        ("Aponte os pontos de quebra", "Em cada seta, pergunte: <b>quem confere? o que pode falhar? "
         "qual a consequencia?</b> Circule os pontos de risco."),
        ("Priorize uma melhoria", "Escolha o ponto de quebra mais critico e defina uma acao "
         "concreta: campo obrigatorio, validacao, integracao ou padronizacao."),
    ]) +
    tbl(["Etapa do ciclo", "Pergunta de auditoria", "Risco tipico"],
        [["Coleta", "O formulario exige hora, local e responsavel?", "Campo em branco ou preenchido a posteriori."],
         ["Registro", "A hora do sistema bate com a hora real?", "Dado sujo que quebra a cadeia de custodia."],
         ["Armazenamento", "O dado esta em um so lugar confiavel?", "Duas versoes da verdade."],
         ["Analise", "O metodo esta documentado e e repetivel?", "Resultado nao auditavel."],
         ["Relatorio", "A informacao chega em tempo de ser util?", "Laudo tardio perde valor."],
         ["Decisao", "Quem decide tem o dado certo na mao?", "Decisao baseada em numero distorcido."]],
        num_cols=[]) +
    callout("tip", "Mapeie em uma tarde",
        "Nao precisa de software. Uma folha A3, post-its e 90 minutos com a equipe ja revelam 80% "
        "dos pontos de quebra. O mapa vira o <b>plano de qualidade de dados</b> do setor.")
)

cad.section("fluxo-investigacao", "Fluxo de investigacao e aplicacoes praticas",
    p("O ciclo de dados nao existe isolado: ele alimenta a <b>investigacao</b>. Ver como a pericia se "
      "conecta ao trabalho policial e ao Judiciario ajuda o analista a priorizar o que medir.") +
    flow_h([
        ("\U0001f692", "Ocorrencia"),
        ("\U0001f50d", "Pericia de campo"),
        ("\U0001f52c", "Exame laboratorial"),
        ("\U0001f4c4", "Laudo"),
        ("\U0001f46e", "Inquerito"),
        ("\u2696\ufe0f", "Processo"),
    ]) +
    grid2([
        ("Cenario A — Homicidio sem suspeito",
         "A pericia de campo coleta vestigios; a balistica e o DNA apontam vinculos. O cruzamento "
         "de perfis no CODIS gera um match que direciona a investigacao — <b>de vestigio a suspeito</b>."),
        ("Cenario B — Acidente de transito",
         "A toxicologia identifica alcool ou droga; a pericia mecanica aponta falha. Os dados "
         "sustentam a tipificacao do crime e a responsabilizacao — <b>de amostra a prova</b>."),
    ]) +
    step([
        ("Identifique a pergunta policial", "O que a investigacao precisa saber? Pai genetica? "
         "Substancia? Cronologia? A pergunta define o exame e o dado a coletar."),
        ("Selecione o vestigio", "Nem tudo precisa ser analisado — o vestigio com maior poder de "
         "resposta e priorizado. Isso economiza reagente e tempo (TAT)."),
        ("Registre com rigor", "Cada amostra recebe identificacao, custodia e metodo. Sem isso, a "
         "prova perde validade juridica."),
        ("Analise e interprete", "O resultado e interpretado no contexto do caso — nunca isolado. "
         "Um numero sem contexto pode enganar."),
        ("Entregue no prazo", "O laudo chega em tempo de ser util. Um resultado perfeito, tarde, "
         "nao muda a investigacao."),
    ]) +
    aplicab(
        "Sempre que o laboratorio precisar decidir a ordem de processamento dos exames.",
        "Porque a investigacao tem prazos e gravidade diferentes; nem todo exame tem a mesma "
        "urgencia policial.",
        "Um homicidio em flagrante e um caso de menor potencial ofensivo chegam juntos; a triagem "
        "tecnica define qual recebe <b>prioridade</b> — e a gestao precisa documentar o criterio.")
)

cad.section("fontes-dados-politec", "Onde nascem os dados da POLITEC: as quatro fontes",
    p("Antes de falar em dashboards e IA, vale saber <b>de onde vem</b> o dado pericial. Sao quatro "
      "origens principais, cada uma com um nivel de estrutura e um desafio proprio.") +
    tbl(["Fonte", "Tipo predominante", "Exemplos", "Desafio"],
        [["<b>Campo / local de crime</b>", "Nao estruturado",
          "Fotos, croquis, videos, relatos.", "Contexto rico, dificil de cruzar."],
         ["<b>Bancada / laboratorio</b>", "Estruturado",
          "Resultados numericos, perfis geneticos, cromatogramas.", "Padronizar unidades e metodos."],
         ["<b>Sistemas de gestao</b>", "Estruturado / semiestruturado",
          "LIS, SISP, planilhas de entrada e saida, XML/JSON.", "Integrar formatos e evitar duplicidade."],
         ["<b>Documentos / laudos</b>", "Nao estruturado",
          "Laudos narrativos, pareceres, oficios.", "Extrair entidades para virar indicador."]],
        num_cols=[]) +
    kpi([
        ("2", "Fontes majoritariamente nao estruturadas"),
        ("80%", "Do acervo e nao estruturado"),
        ("1", "Meta: uma fonte unica da verdade"),
    ]) +
    callout("err", "Ignorar a fonte nao estruturada",
        "Quem so conta com o que esta em tabela perde <b>80% da informacao</b> da instituicao. A "
        "pericia criminal nasce, em boa parte, do que nao cabe em colunas.")
)

cad.section("integracao-sistemas", "Integracao de sistemas: o dado que nao conversa",
    p("A POLITEC nao vive isolada: seus dados precisam circular entre laboratorios, delegacias, IML, "
      "Ministerio Publico e sistemas nacionais. Quando cada sistema fala uma lingua, o dado perde "
      "valor no caminho.") +
    flow_h([
        ("\U0001f5c4\ufe0f", "Laboratorio (LIS)"),
        ("\U0001f310", "Barramento / API"),
        ("\U0001f3e2", "Delegacia (SISP)"),
        ("\U0001f3db\ufe0f", "Sistema nacional"),
        ("\u2696\ufe0f", "Justica"),
    ]) +
    grid2([
        ("Problemas tipicos de integracao",
         ul(["Nomes de campo diferentes para a mesma coisa",
             "Formatos de data divergentes (ISO x dd/mm/aaaa)",
             "Codificacao com acentos quebrados",
             "Status que nao batem entre sistemas"])),
        ("Como mitigar",
         ul(["Definir um <b>vocabulario controlado</b> comum",
             "Usar <b>padroes de integracao</b> (XML/JSON bem documentados)",
             "Validar na origem, reconciliar periodicamente",
             "Uma chave unica por laudo, reconhecida por todos"])),
    ]) +
    callout("err", "Integrar sem reconciliar",
        "Conectar dois sistemas e deixar os numeros divergirem e pior do que nao integrar: cria-se "
        "a falsa sensacao de que o dado &ldquo;esta la&rdquo;, quando na verdade ha duas versoes da verdade. "
        "<b>Reconcile sempre.</b>")
)

cad.section("padronizacao-campos", "Padronizacao dos campos: o que medir em cada exame",
    p("Padronizar e decidir, antes de coletar, <b>como cada campo sera preenchido</b>. Sem isso, a "
      "estatistica nasce impossivel: cinco grafias para o mesmo tipo de exame quebram qualquer "
      "contagem.") +
    antesdepois(
        "Campo livre: o perito escreve <i>DNA</i>, <i>Genetica</i>, <i>Perfil Genetico</i>, "
        "<i>GEN-E</i> ou <i>exame genetico</i>. A contagem de exames de DNA fica fragmentada e "
        "subestimada.",
        "Lista controlada: a coluna <code>Tipo_Exame</code> so aceita <b>DNA</b>. O filtro soma "
        "exames de DNA sem medo de achar uma variacao escondida.",
        "Campo livre", "Lista controlada") +
    tbl(["Campo", "Formato padrao", "Por que"],
        [["<i>Tipo de exame</i>", "Lista controlada (DNA, Toxicologia, Balistica...)", "Evita variacoes de escrita."],
         ["<i>Data</i>", "ISO <code>AAAA-MM-DD</code> ou tipo Data numerico", "Calculo de TAT e ordenacao corretos."],
         ["<i>Numero do laudo</i>", "Sem espacos nem caracteres especiais", "Serve de chave unica."],
         ["<i>Setor</i>", "Nome oficial curto", "Agrupamento e comparacao entre setores."],
         ["<i>Status</i>", "Conjunto fechado (Em andamento, Concluido, Atrasado)", "Indicadores de prazo confiaveis."]],
        num_cols=[]) +
    callout("err", "Padronizar depois e mais caro",
        "Corrigir depois exige limpeza manual, arrisca apagar variacoes legitimas e nao e auditavel. "
        "A padronizacao se faz <b>na entrada</b>, com validacao — nao no fechamento do mes.")
)

cad.section("dado-sensivel-lgpd", "Dados sensiveis e LGPD na pericia",
    p("Dados periciais sao, por natureza, <b>sensiveis</b>: envolvem pessoas, saude, biometria e "
      "questoes criminais. A LGPD (Lei 13.709/2018) nao e um obstaculo a analise — e o <b>limite "
      "etico e juridico</b> que orienta o que pode ser tratado, por quem e com qual finalidade.") +
    grid2([
        ("Categorias sensiveis na pericia",
         ul(["Dados geneticos (DNA)",
             "Dados biometricos (impressoes digitais, face)",
             "Dados de saude (necropsia, toxicologia)",
             "Dados de investigacao criminal"])),
        ("Principios que valem na analise",
         ul(["<b>Finalidade</b>: tratar so para o fim legitimo",
             "<b>Minimizacao</b>: coletar so o necessario",
             "<b>Seguranca</b>: proteger contra vazamento",
             "<b>Prestacao de contas</b>: comprovar o cuidado"])),
    ]) +
    checklist([
        "O dado tem <b>base legal</b> e finalidade definida?",
        "O acesso e <b>restrito a quem precisa</b> (perfil minimo)?",
        "Os resultados publicados estao <b>anonimizados/agregados</b>?",
        "Ha <b>registro de auditoria</b> de quem acessou e por que?",
    ]) +
    callout("err", "Expor mais do que o necessario",
        "Publicar um painel com nomes, CPF ou caso individual viola a LGPD e o sigilo processual. "
        "Painel gerencial mostra <b>agregados</b>: totais, percentuais e medias — nunca o caso "
        "identificavel.")
)

cad.section("ciclo-campo-bancada", "O caminho do vestigio: do campo a bancada (passo a passo)",
    p("Esta secao traduz o ciclo de dados em um <b>checklist operacional</b> que o perito e o "
      "auxiliar executam na pratica. E a qualidade do registro que garante que a bancada tenha o que "
      "analisar e que o laudo tenha valor.") +
    flow_h([
        ("\U0001f5fa\ufe0f", "Preservar o local"),
        ("\U0001f4f8", "Fotografar e medir"),
        ("\U0001f9ea", "Coletar e acondicionar"),
        ("\U0001f4dd", "Rotular e registrar"),
        ("\U0001f69a", "Transportar"),
        ("\U0001f52c", "Receber na bancada"),
    ]) +
    step([
        ("1. Preservacao", "Isole a area, proteja os vestigios e evite contaminacao cruzada. Use "
         "EPI adequado e registre quem entrou."),
        ("2. Documentacao visual", "Fotografe <b>antes</b> de tocar em qualquer coisa; use escala e "
         "referencia. Anote iluminacao, clima e hora — contexto tambem e dado."),
        ("3. Coleta", "Recolha cada vestigio com material esteril e individual. Um swab por vestigio "
         "evita contaminacao e preserva a interpretacao."),
        ("4. Rotulagem", "Rotule com numero de cadeia de custodia, data, hora e responsavel. "
         "<b>Nunca</b> escreva direto sobre a embalagem que contem a amostra."),
        ("5. Transporte", "Garanta temperatura e lacre adequados. Registre a saida e a chegada — "
         "quebras de continuidade sao fatais para a prova."),
        ("6. Recebimento", "Na bancada, confira o lacre, registre no sistema e confira <b>se a hora "
         "bate</b> com o campo. Divergencia aqui e sinal de dado sujo."),
    ]) +
    ficha("r", "O elo mais fragil",
        "A maioria dos problemas nasce <b>antes</b> da analise: no registro e no transporte. Invista "
        "tempo na cadeia de custodia — e o seguro juridico do laudo.")
)

cad.section("kpis-intro", "Do dado ao KPI: os indicadores que a direcao sempre pede",
    p("Fechando o Modulo 1, vale conectar tudo o que vimos aos numeros que a direcao cobra. Estes "
      "sao os indicadores que voltam em todos os dias do curso — e todos dependem de dado limpo e "
      "qualidade na entrada.") +
    tbl(["Indicador", "Definicao", "Depende de", "Dia do curso"],
        [["<b>TAT</b>", "Tempo entre recebimento e emissao do laudo.", "Datas numericas e completas.", "Dias 2-4"],
         ["<b>Backlog</b>", "Exames aguardando processamento ou emissao.", "Status confiavel e unico.", "Dias 2-4"],
         ["<b>Produtividade</b>", "Laudos emitidos por perito/setor no periodo.", "Numero do laudo unico.", "Dias 3-4"],
         ["<b>Qualidade</b>", "Aderencia a metodo, completude e ausencia de erro.", "Registro padronizado.", "Dias 1-3"],
         ["<b>% Atrasados</b>", "Proporcao de laudos alem do prazo legal.", "TAT e prazo definidos.", "Dias 3-4"]],
        num_cols=[]) +
    kpi([
        ("TAT", "O indicador central da eficiencia"),
        ("Backlog", "O termometro da demanda"),
        ("Qualidade", "O que impede o retrabalho"),
    ]) +
    aplicab(
        "Sempre que a direcao pedir &ldquo;como esta a producao?&rdquo;.",
        "Porque volume sozinho nao responde: e preciso prazo (TAT), fila (backlog) e qualidade no "
        "mesmo painel para uma leitura honesta.",
        "Reportar so &ldquo;emitimos 300 laudos&rdquo; esconde se eles sairam no prazo, se a fila cresceu ou "
        "se houve retrabalho. O conjunto TAT + backlog + qualidade conta a historia real.") +
    callout("note", "Ponte para a Parte 2",
        "Tudo isso depende de <b>estatistica descritiva</b>. Antes de calcular qualquer KPI, "
        "precisamos dominar media, mediana, dispersao e outliers — que e exatamente o Modulo 2, a "
        "seguir.")
)

# =================================================================
# PARTE 2 - MODULO 2
# =================================================================
cad.grp("Parte 2 · Modulo 2 — Fundamentos Estatisticos",
        "As ferramentas matematicas simples que revelam verdades profundas sobre a operacao dos laboratorios.")

cad.section("estatistica-descritiva", "Estatistica descritiva: a linguagem da gestao pericial",
    p("A estatistica descritiva resume um conjunto de dados em poucos numeros e graficos. Ela nao "
      "adivinha o futuro nem prova causas — ela <b>descreve o que aconteceu</b>, com precisao.") +
    p("No contexto pericial, ela responde perguntas de gestao: quanto o laboratorio produziu, em "
      "quanto tempo, com que variacao, e onde estao os gargalos.") +
    grid2([
        ("Duas familias de medidas",
         ul(["<b>Tendencia central</b>: onde o dado se concentra (media, mediana, moda).",
             "<b>Dispersao</b>: o quanto o dado se espalha (desvio padrao, amplitude)."])),
        ("Duas familias de graficos",
         ul(["<b>Histograma</b>: como a frequencia se distribui por faixas.",
             "<b>Boxplot</b>: a distribuicao resumida e onde estao os outliers."])),
    ]) +
    callout("note", "Por que comecar por aqui",
        "Antes de dashboards e IA, o gestor precisa dominar a leitura descritiva. Sem ela, qualquer "
        "indicador avancado e apenas um numero bonito — e provavelmente enganoso.")
)

cad.section("tendencia-central", "Medidas de tendencia central: a tirania da media",
    p("Media, mediana e moda descrevem o &ldquo;centro&rdquo; dos dados, mas cada uma conta uma historia "
      "diferente. Escolher a errada pode distorcer completamente o diagnostico da gestao pericial.") +
    tbl(["Medida", "O que e", "Comportamento", "Quando usar"],
        [["\U0001f4ca <b>Media</b>",
          "Soma dos valores dividida pela quantidade.",
          "Altamente sensivel a valores extremos (outliers).",
          "Quando os dados sao homogeneos, sem casos atipicos."],
         ["\U0001f4cd <b>Mediana</b>",
          "O valor central que divide o conjunto ao meio.",
          "Robusta — ignora extremos e representa melhor a rotina.",
          "Quando ha outliers ou distribuicao assimetrica (o caso pericial tipico)."],
         ["\U0001f501 <b>Moda</b>",
          "O valor que mais se repete.",
          "Util para dados categoricos e padroes recorrentes.",
          "Para identificar o comportamento tipico do processo."]],
        num_cols=[]) +
    aplicab(
        "Sempre que for apresentar um indicador de tempo, custo ou produtividade em relatorio.",
        "Porque a media esconde casos atipicos e pode gerar diagnosticos falsos — desmoralizando "
        "equipes excelentes ou escondendo gargalos reais.",
        "Um laboratorio com TAT (Tempo Medio de Emissao de Laudo) quase sempre informe um caso "
        "excepcional deve apresentar <b>mediana + contexto</b>, nunca so a media.")
)

cad.section("tat-dna", "Exemplo real: media x mediana no TAT do DNA",
    p("Tempos de emissao de laudo de DNA (em dias) em um periodo: <b>4, 5, 5, 6 e 120</b>. O caso de "
      "120 dias foi excepcional — exigiu reanalise completa e aguardou reagente importado de dificil "
      "obtencao.") +
    kpi([("28 dias", "Media"), ("5 dias", "Mediana"), ("5 dias", "Moda")]) +
    bar_chart(["Caso 1", "Caso 2", "Caso 3", "Caso 4", "Caso 5 (outlier)"],
              [4, 5, 5, 6, 120],
              title="Dias para emissao do laudo",
              subtitulo="Um unico caso excepcional eleva a media de 5 para 28 dias.",
              destaque=4) +
    p("O gestor e cobrado, e a imprensa publica: <i>&ldquo;Laboratorio da Politec leva quase um mes para "
      "emitir laudos de DNA.&rdquo;</i> Mas a verdade operacional e outra: <b>a rotina do laboratorio e "
      "agil (mediana de 5 dias)</b>. Houve apenas um evento atipico que distorceu a media.") +
    antesdepois(
        "&ldquo;Nosso tempo medio de emissao e 28 dias.&rdquo; (diagnostico falso, equipe desmoralizada)",
        "&ldquo;Nossa mediana e 5 dias. O caso de 120 dias foi excepcional, por conta de [motivo tecnico].&rdquo;",
        "So a media", "Mediana + contexto") +
    callout("err", "A armadilha do relatorio",
        "Apresentar apenas a media em relatorios de gestao publica <b>e gerar um diagnostico falso</b>. "
        "A pratica correta e sempre <b>mediana + contexto dos outliers</b>.")
)

cad.section("deming", "Deming: a variacao como inimiga da qualidade",
    p("<b>W. Edwards Deming</b>, pai do controle estatistico de qualidade moderno, ensinou que a "
      "media diz <i>onde</i> o bolo esta; a dispersao diz se ele e <i>uniforme</i>. Dois processos "
      "com a mesma media podem exigir estrategias de gestao radicalmente diferentes.") +
    ficha("a", "A frase central",
        "&ldquo;A variacao e o maior inimigo da qualidade.&rdquo; — W. Edwards Deming.") +
    p("Na POLITEC, essa licao se traduz diretamente na analise da producao dos laboratorios e no "
      "planejamento de estoques de insumos criticos. Um laboratorio imprevisivel e mais caro e mais "
      "arriscado do que um laboratorio estavel, mesmo que ambos produzam a mesma media.") +
    callout("tip", "Pergunta de gestor",
        "Nunca pare em &ldquo;qual a media?&rdquo; Pergunte tambem: <b>&ldquo;a producao e estavel ou oscila?&rdquo;</b>. "
        "A resposta muda a escala de plantao, o estoque e o plano de manutencao.")
)

cad.section("dispersao", "Medidas de dispersao: o perigo oculto na producao",
    p("O <b>desvio padrao</b> indica a volatilidade dos dados — o quanto os valores individuais se "
      "afastam da media. Dois laboratorios com a mesma media podem ter realidades operacionais "
      "completamente distintas.") +
    grid2([
        ("Laboratorio A — desvio padrao baixo",
         "<b>Produz entre 95 e 105 exames/mes.</b> Rotina estavel e previsivel. Facil de gerir "
         "estoques de reagentes, escala de pessoal e manutencao de equipamentos. "
         "<b>Risco baixo de desperdicio.</b>"),
        ("Laboratorio B — desvio padrao alto",
         "<b>Produz 20 exames em um mes e 180 no outro.</b> Rotina caotica. Exige gestao de crise "
         "constante, horas extras imprevisiveis e alto risco de vencimento de insumos estocados em "
         "excesso."),
    ]) +
    kpi([("100 exames/mes", "Media - Lab A"), ("~3", "Desvio - Lab A"),
         ("100 exames/mes", "Media - Lab B"), ("~57", "Desvio - Lab B")]) +
    ficha("r", "Mesma media, estrategias opostas",
        "O desvio padrao e a informacao que faz a diferenca no planejamento. Dois laboratorios com "
        "media de 100 exames/mes pedem <b>gestoes completamente diferentes</b>.")
)

cad.section("tukey-boxplot", "John Tukey e o boxplot: o raio-X da producao pericial",
    p("<b>John Tukey</b> (1977) criou a Analise Exploratoria de Dados (EDA) e o <b>boxplot</b> "
      "(diagrama de caixa) para que cientistas pudessem compreender a distribuicao completa de um "
      "conjunto de dados sem precisar de supercomputadores — usando apenas papel e lapis.") +
    ficha("p", "A frase que resume a EDA",
        "&ldquo;E melhor ter uma resposta aproximada a pergunta certa do que uma resposta exata a pergunta "
        "errada.&rdquo; — John Tukey.") +
    tbl(["Elemento do boxplot", "O que revela"],
        [["<b>A caixa</b>", "Contem 50% dos dados normais — a rotina padrao do laboratorio."],
         ["<b>A linha central</b>", "A <b>mediana</b> — o valor que representa a realidade operacional tipica."],
         ["<b>As antenas (whiskers)</b>", "O limite do comportamento esperado — a fronteira entre o normal e o atipico."],
         ["<b>Os pontos isolados</b>", "Os <b>outliers</b> — valores fora da curva que merecem atencao imediata."]],
        num_cols=[]) +
    aplicab(
        "Quando voce precisa comparar a producao de varios laboratorios ou meses de uma so vez.",
        "Porque o boxplot mostra media, mediana, dispersao e outliers no mesmo desenho — uma "
        "radiografia da distribuicao.",
        "Ao comparar 12 meses de TAT do IML, o boxplot revela num relance meses instaveis e pontos "
        "fora da curva que uma tabela de medias esconderia.") +
    callout("tip", "O boxplot substitui a media?",
        "Nao substitui — <b>completa</b>. Ele mostra a caixa (50% central) e os extremos. "
        "A media e uma linha; o boxplot e a distribuicao inteira.")
)

cad.section("histogramas", "Histogramas na pratica pericial",
    p("Histogramas sao graficos de barras que mostram a <b>distribuicao de frequencia</b>. Na "
      "POLITEC, revelam padroes operacionais que relatorios numericos escondem.") +
    bar_chart(["Segunda", "Terca", "Quarta", "Quinta", "Sexta"],
              [78, 42, 44, 40, 48],
              title="Exames recebidos por dia da semana",
              subtitulo="Gargalo no recebimento as segundas-feiras: quase o dobro dos demais dias.",
              destaque=0) +
    p("O histograma evidencia um <b>gargalo no recebimento de material as segundas-feiras</b> — "
      "quase o dobro dos demais dias. Essa informacao e <b>invisivel</b> em uma tabela com totais "
      "semanais.") +
    p("Com esse diagnostico visual, o gestor pode ajustar a escala de plantao, reforcar a equipe de "
      "triagem as segundas, ou renegociar os prazos de envio de material pelas delegacias parceiras.") +
    ficha("g", "A licao",
        "Visualizar a <b>distribuicao</b>, nao apenas o total, revela onde esta o gargalo real.")
)

cad.section("correlacao", "Correlacao x causalidade: a armadilha logica",
    p("<b>Correlacao</b> e quando duas variaveis se movem juntas no grafico — quando uma sobe, a "
      "outra tambem sobe (ou desce). <b>Causalidade</b> e quando uma variavel <i>provoca</i> a "
      "mudanca na outra, com um mecanismo real de causa e efeito, verificavel e replicavel.") +
    ficha("r", "A frase que evita erros graves",
        "&ldquo;Correlacao <b>nao</b> implica causalidade.&rdquo; — principio central da estatistica, "
        "popularizado por Tyler Vigen em <i>Spurious Correlations</i>.") +
    p("Vigen catalogou centenas de correlacoes absurdas com dados reais, como a correlacao perfeita "
      "entre o consumo per capita de <b>queijo</b> nos EUA e o numero de mortes por <b>emaranhamento "
      "em lencois</b>. A licao e direta: sem teoria, a estatistica pode &ldquo;provar&rdquo; qualquer coisa.") +
    antesdepois(
        "&ldquo;Os dois graficos sobem juntos, logo um causou o outro.&rdquo;",
        "&ldquo;Os dois sobem juntos. Vamos investigar se ha um mecanismo real — ou uma terceira causa.&rdquo;",
        "Salto logico", "Hipotese + mecanismo")
)

cad.section("peritos-mortes", "Exemplo critico: correlacao real, causalidade invertida",
    p("A observacao nos dados: &ldquo;Aumentou o numero de peritos lotados no IML e aumentou o numero de "
      "mortes violentas no estado.&rdquo; Os dois graficos sobem juntos. A correlacao e "
      "<b>estatisticamente real</b>.") +
    antesdepois(
        "&ldquo;Os peritos estao causando mortes? O crescimento do IML e o responsavel pelo aumento da "
        "violencia?&rdquo;",
        "O aumento da criminalidade (ou uma mudanca legislativa exigindo pericia em todos os casos) "
        "e que demandou mais peritos.",
        "Causalidade mal lida", "Causalidade inversa") +
    ficha("a", "A leitura correta",
        "A correlacao e real, mas a causalidade e <b>inversa</b>. E o crime que gera a demanda por "
        "peritos, nao o contrario. Sem entender o mecanismo, a estatistica conta a historia de "
        "cabeca para baixo.")
)

cad.section("cobra-effect", "O Cobra Effect na pericia: quando a metrica destroi a qualidade",
    p("Um gestor decide bonificar os peritos que emitem <b>mais laudos</b> por mes. A intencao e "
      "aumentar a produtividade e reduzir o backlog. O efeito foi o oposto do esperado.") +
    flow_h([
        ("\U0001f4b0", "Bonus por volume"),
        ("\u2702\ufe0f", "Fragmentacao"),
        ("\U0001f4c9", "Qualidade cai"),
    ]) +
    step([
        ("Gestao cria bonificacao por numero de laudos", "O indicador escolhido foi o volume bruto, "
         "facil de medir — e facil de manipular."),
        ("Peritos dividem exames complexos em varios laudos", "Um exame que geraria um laudo passa a "
         "gerar tres ou quatro. O numero sobe; o trabalho nao muda."),
        ("Laudos +300%; qualidade tecnica cai", "O incentivo premiou a fragmentacao, nao a resolucao "
         "do caso."),
    ]) +
    ficha("r", "A licao",
        "Metricas mal desenhadas geram comportamentos indesejados. A estatistica deve medir "
        "<b>qualidade e impacto</b>, nao apenas volume bruto. O que e medido e gerenciado — para o "
        "bem ou para o mal.")
)

cad.section("outliers", "Outliers: erro de medicao ou pista de inteligencia?",
    p("No mundo corporativo, outliers sao frequentemente tratados como erros de medicao e "
      "descartados para nao distorcer a analise. <b>Na pericia criminal, sao o contrario</b>: "
      "pistas de inteligencia ou alertas de gestao. Nunca devem ser ignorados ou apagados sem "
      "investigacao.") +
    tbl(["Exemplo na POLITEC", "O que investigar"],
        [["<b>Outlier de producao</b>: 0 exames processados em uma semana inteira.",
          "Falta de reagente? Quebra do equipamento principal? Paralisacao?"],
         ["<b>Outlier de caso</b>: um exame de toxicologia que levou 200 horas (media: 5h).",
          "Envenenamento por substancia rara que exigiu protocolo especial de analise?"]],
        num_cols=[]) +
    ficha("g", "O lema da secao",
        "Na POLITEC, o outlier <b>nao e apagado — ele e investigado</b>. Ele aponta para um gargalo "
        "operacional critico ou para um caso de alta complexidade que merece atencao.")
)

cad.section("taleb", "Cisnes Negros na pericia criminal",
    p("<b>Nassim Nicholas Taleb</b> (2007) definiu o <b>Cisne Negro</b> como um evento raro, de alto "
      "impacto e imprevisivel pela media historica. Ele demonstrou que os maiores eventos da historia "
      "— crises financeiras, pandemias, descobertas cientificas — eram invisiveis para os modelos "
      "baseados em medias historicas. A estatistica convencional e cega para aquilo que nunca "
      "aconteceu antes.") +
    grid2([
        ("\U0001f9ea Nova droga sintetica",
         "Substancia que os reagentes e protocolos atuais nao conseguem detectar, exigindo "
         "desenvolvimento emergencial de novos metodos analiticos."),
        ("\U0001f30a Desastre de massa",
         "Evento que sobrecarrega o IML em <b>1000%</b> (acidente aereo, desastre natural, conflito). "
         "Modelos baseados na media do passado falham completamente."),
    ]) +
    ficha("p", "Consequencia pratica",
        "Planos de contingencia sao obrigatorios. Modelos estatisticos baseados apenas no passado "
        "<b>nao preveem Cisnes Negros</b> — por isso a gestao pericial precisa de reserva de "
        "capacidade e protocolos de crise.")
)

# ---- NOVAS SECOES DO MODULO 2 ----

cad.section("como-calcular-central", "Como calcular media, mediana e moda passo a passo",
    p("A teoria fica clara quando a gente calcula na mao. Vamos usar os tempos de emissao de 7 "
      "laudos (em dias): <b>3, 4, 4, 5, 6, 7, 90</b>. Esse e o mesmo conjunto do Lab 1, com um caso "
      "atipico de 90 dias.") +
    step([
        ("Ordene os dados", "Coloque em ordem crescente: 3, 4, 4, 5, 6, 7, 90. Ordenar e o primeiro "
         "passo para achar a mediana e enxergar a distribuicao."),
        ("Calcule a media", "Some todos e divida pela quantidade: "
         "<b>(3+4+4+5+6+7+90) / 7 = 119 / 7 = 17 dias</b>. A media foi puxada para cima pelo 90."),
        ("Ache a mediana (n impar)", "Com 7 valores (impar), a mediana e o <b>4o valor</b> — o "
         "central. Ordem: 3, 4, 4, [5], 6, 7, 90. Mediana = <b>5 dias</b>."),
        ("Ache a moda", "O valor que mais se repete e o <b>4</b> (aparece duas vezes). Moda = "
         "<b>4 dias</b>."),
        ("Compare as tres", "Media 17, mediana 5, moda 4. Repare como a media esta muito longe da "
         "mediana e da moda — sinal classico de <b>distribuicao assimetrica com outlier</b>."),
    ]) +
    code("""
        // No Excel / Google Sheets:
        =MEDIA(A2:A8)      // media   -> 17
        =MED(A2:A8)        // mediana -> 5
        =MODO(A2:A8)       // moda    -> 4

        // A distancia entre media e mediana mede a influencia de outliers:
        // media (17) - mediana (5) = 12 dias de distorcao.
        """, "excel") +
    callout("err", "Mediana de conjunto par",
        "Com numero <b>par</b> de valores, a mediana e a media dos <b>dois centrais</b>. Ex.: 3, 4, 4, "
        "5, 6, 7 -> mediana = (4+5)/2 = 4,5. Nao e &ldquo;o valor do meio&rdquo; porque nao existe um so.")
)

cad.section("como-calcular-desvio", "Como calcular o desvio padrao passo a passo",
    p("O desvio padrao parece assustador por causa da formula, mas o raciocinio e simples: "
      "<b>quanto, em media, cada valor se afasta da media?</b> Vamos calcular para a producao "
      "mensal (em exames) de 5 meses: <b>90, 95, 100, 105, 110</b>.") +
    step([
        ("Calcule a media", "(90+95+100+105+110) / 5 = 500 / 5 = <b>100 exames</b>."),
        ("Subtraia a media de cada valor", "90-100 = -10; 95-100 = -5; 100-100 = 0; 105-100 = +5; "
         "110-100 = +10. Esses sao os <b>desvios</b>."),
        ("Eleve cada desvio ao quadrado", "100; 25; 0; 25; 100. Elevar ao quadrado elimina o sinal e "
         "penaliza desvios grandes — dai a sensibilidade a outliers."),
        ("Some os quadrados", "100+25+0+25+100 = <b>250</b>. Essa e a soma dos quadrados dos desvios."),
        ("Divida e extraia a raiz", "Variancia = 250 / 5 = <b>50</b>. Desvio padrao = raiz de 50 = "
         "<b>~7,1 exames</b>. Ou seja, os meses variam cerca de 7 exames em torno da media de 100."),
    ]) +
    code("""
        // Passo a passo no Excel (dados em A2:A6):

        Media      = MEDIA(A2:A6)                  -> 100
        Desvio     = A2 - $Media                   -> -10, -5, 0, 5, 10
        Quadrado   = Desvio^2                      -> 100, 25, 0, 25, 100
        Variancia  = SOMA(Quadrados) / 5           -> 50
        DesvPadrao = RAIZ(Variancia)               -> 7,1

        // Funcao direta (populacao):
        =DESVPAD.P(A2:A6)     -> 7,1
        =VAR.P(A2:A6)         -> 50
        """, "excel") +
    tbl(["Medida", "Valor do exemplo", "O que significa"],
        [["Media", "100 exames", "O centro da producao."],
         ["Variancia", "50", "Unidade ao quadrado — pouco intuitiva."],
         ["Desvio padrao", "~7,1 exames", "Dispersao na mesma unidade dos dados: ~7 exames."]],
        num_cols=[]) +
    callout("err", "DesvPad amostral x populacional",
        "Se seus dados sao a <b>populacao inteira</b> (todos os meses do periodo), use "
        "<code>DESVPAD.P</code>. Se sao uma <b>amostra</b>, use <code>DESVPAD.A</code>. Para gestao "
        "pericial, na pratica a diferenca e pequena — mas os slides usam a populacao.")
)

cad.section("amplitude-variancia-cv", "Amplitude, variancia e coeficiente de variacao",
    p("O desvio padrao nao e a unica medida de dispersao. Tres ferramentas se complementam — e a "
      "terceira permite comparar setores de tamanhos diferentes, algo essencial na gestao.") +
    tbl(["Medida", "Como se calcula", "Unidade", "Ponto fraco"],
        [["<b>Amplitude</b>", "Maior valor - menor valor", "Igual a dos dados",
          "So olha os extremos; sensivel a um unico outlier."],
         ["<b>Variancia</b>", "Media dos desvios ao quadrado", "Dados <b>ao quadrado</b>",
          "Dificil de interpretar por causa da unidade quadrada."],
         ["<b>Desvio padrao</b>", "Raiz da variancia", "Igual a dos dados",
          "Nao permite comparar grandezas de escalas diferentes."],
         ["<b>Coef. de variacao (CV)</b>", "Desvio padrao / media (em %)", "Percentual",
          "Perde sentido quando a media e proxima de zero."]],
        num_cols=[]) +
    code("""
        // Exemplo: Lab A media 100, desvio 7  -> CV = 7%
        // Exemplo: Lab B media 100, desvio 57 -> CV = 57%

        CV = DESVPAD.P(A2:A12) / MEDIA(A2:A12)     // formato percentual
        Amplitude = MAX(A2:A12) - MIN(A2:A12)
        """, "excel") +
    aplicab(
        "Quando voce compara a estabilidade de setores com volumes muito diferentes.",
        "Porque o CV coloca a dispersao em escala percentual, permitindo comparar um setor pequeno "
        "(IML) com um setor grande (Toque).",
        "Um setor que produz media 20 e desvio 6 tem CV de 30%; outro com media 200 e desvio 20 tem "
        "CV de 10%. Em <b>estabilidade</b>, o segundo e melhor — apesar de produzir muito mais.") +
    kpi([
        ("CV < 10%", "Muito estavel"),
        ("CV 10-20%", "Estavel"),
        ("CV 20-35%", "Instavel"),
        ("CV > 35%", "Critico"),
    ]) +
    callout("tip", "Regra de bolso do CV",
        "Use o CV para comparar setores. Use o desvio padrao absoluto para dimensionar estoque e "
        "escala dentro de um mesmo setor. Sao leituras complementares.")
)

cad.section("quartis-percentis", "Quartis, percentis e a leitura fina da distribuicao",
    p("Enquanto a mediana divide os dados em dois, os <b>quartis</b> dividem em quatro e os "
      "<b>percentis</b> em cem. Eles permitem responder perguntas de prazo que a media nao responde — "
      "como &ldquo;em quanto tempo 90% dos laudos ficam prontos?&rdquo;.") +
    step([
        ("Ordene os dados", "Sempre o primeiro passo: da menor para a maior observacao."),
        ("Ache a mediana (Q2)", "Divide o conjunto em 50% abaixo e 50% acima. E o segundo quartil."),
        ("Ache Q1 (25%)", "A mediana da <b>metade inferior</b>. Um quarto dos dados fica abaixo dele."),
        ("Ache Q3 (75%)", "A mediana da <b>metade superior</b>. Tres quartos ficam abaixo dele."),
        ("Interprete o IQR", "IQR = Q3 - Q1. E a &ldquo;caixa&rdquo; do boxplot: onde vive a rotina central."),
    ]) +
    code("""
        // Excel / Google Sheets:
        =QUARTIL(A2:A100; 1)   // Q1 (25%)
        =MED(A2:A100)          // Q2 (mediana, 50%)
        =QUARTIL(A2:A100; 3)   // Q3 (75%)
        =PERCENTIL(A2:A100; 0,9)   // P90: prazo em que 90% dos laudos sairam

        // IQR (intervalo interquartil):
        IQR = Q3 - Q1
        """, "excel") +
    aplicab(
        "Quando a pergunta de gestao e sobre prazo extremo, e nao sobre a media.",
        "Porque a direcao costuma querer saber &ldquo;qual o pior caso que devo explicar&rdquo;, e isso e um "
        "percentil alto (P90, P95), nao uma media.",
        "Se o P90 do TAT de DNA e 30 dias, significa que <b>90% dos laudos</b> saem em ate 30 dias — "
        "uma meta mais defensavel do que prometer &ldquo;media de 5 dias&rdquo;.") +
    callout("err", "Confundir percentil com porcentagem de erro",
        "P90 <b>nao</b> quer dizer 90% de erro nem nota 90. Quer dizer: 90% da massa de dados esta "
        "<b>abaixo</b> daquele valor. E uma medida de posicao, nao de qualidade.")
)

cad.section("como-montar-boxplot", "Como montar um boxplot do zero",
    p("Com Q1, Q2, Q3 e o IQR em maos, montar um boxplot no papel e imediato. Ele e o <b>raio-X</b> "
      "da producao: mostra a rotina (caixa), o centro (mediana), a fronteira do esperado (antenas) e "
      "os pontos fora da curva (outliers).") +
    step([
        ("Calcule os cinco numeros", "Minimo, Q1, mediana (Q2), Q3 e maximo. Ex.: minima 3, Q1 4, "
         "mediana 5, Q3 7, maxima 90."),
        ("Desenhe a caixa", "Um retangulo de Q1 a Q3. A linha interna e a mediana. A caixa contem os "
         "<b>50% centrais</b> — a rotina do setor."),
        ("Calcule o IQR", "IQR = Q3 - Q1 = 7 - 4 = <b>3</b>."),
        ("Defina as antenas", "Limite inferior = Q1 - 1,5 x IQR; limite superior = Q3 + 1,5 x IQR. "
         "Ex.: 4 - 4,5 = -0,5 (na pratica, a minima) e 7 + 4,5 = 11,5."),
        ("Marque os outliers", "Todo valor acima do limite superior (aqui, o <b>90</b>) vira um ponto "
         "isolado, fora da antena. Ele <b>nao</b> e descartado — e sinalizado para investigacao."),
    ]) +
    code("""
        // Os cinco numeros do exemplo (TAT de DNA):
        Minimo = 3
        Q1     = 4
        Mediana= 5
        Q3     = 7
        Maximo = 90

        IQR = Q3 - Q1            -> 3
        Cerca inferior = Q1 - 1,5*IQR = -0,5
        Cerca superior = Q3 + 1,5*IQR = 11,5

        // Tudo acima de 11,5 e outlier -> o caso de 90 dias.
        """, "excel") +
    ficha("p", "Os cinco numeros",
        "Boxplot desenhado e, no fundo, um retrato de <b>cinco numeros</b>: minimo, Q1, mediana, Q3 e "
        "maximo. Domine-os e voce le qualquer conjunto de dados de unidade sem planilha.")
)

cad.section("distribuicao-normal", "A curva normal e a regra 68-95-99,7",
    p("Quando um processo e estavel e simetrico, a distribuicao dos dados assume a forma de "
      "<b>sino</b> — a curva normal (gaussiana). Ela aparece tanto em medidas fisicas (altura, erro "
      "de medicao) quanto em tempo de processamento. Conhecer sua forma ajuda a detectar quando algo "
      "esta fora do padrao.") +
    bar_chart(["-3 dp", "-2 dp", "-1 dp", "Media", "+1 dp", "+2 dp", "+3 dp"],
              [3, 13, 34, 34, 34, 13, 3],
              title="Forma da curva normal (frequencia relativa)",
              subtitulo="68% dos dados ficam a 1 desvio padrao da media; 95% a 2; 99,7% a 3.",
              destaque=3) +
    tbl(["Faixa em torno da media", "Percentual dos dados", "Leitura na POLITEC"],
        [["Media +/- 1 desvio padrao", "<b>68%</b>", "A rotina esperada do laboratorio."],
         ["Media +/- 2 desvios padrao", "<b>95%</b>", "Quase tudo o que se observa no periodo."],
         ["Media +/- 3 desvios padrao", "<b>99,7%</b>", "Fora daqui, e evento raro e investigavel."]],
        num_cols=[]) +
    aplicab(
        "Ao definir limites de alerta em um painel de gestao.",
        "Porque limites estatisticos (2 ou 3 desvios) indicam automaticamente quando um mes e "
        "atipico, sem depender da intuicao de quem olha.",
        "Se o TAT medio do setor e 10 dias com desvio 2, um mes com 18 dias (4 desvios acima) e "
        "<b>alerta vermelho</b>: algo mudou no processo e merece investigacao.") +
    callout("err", "Achar que todo dado e normal",
        "Volume de crimes, concentracao de casos e tempos com outliers extremos <b>nao</b> seguem "
        "curva normal. Aplicar a regra dos desvios sem verificar a forma da distribuicao leva a "
        "conclusoes erradas. Sempre olhe o histograma antes.")
)

cad.section("erro-medicao-vies", "Erro de medicao, vies e precisao na pericia",
    p("Nem toda variacao nos dados e real. Parte dela vem do <b>erro de medicao</b> (do instrumento "
      "ou do operador) e parte vem do <b>vies</b> (um desvio sistematico). Distinguir os dois e "
      "essencial: o erro aleatorio se dilui na media; o vies <b>nao</b> — ele desloca o resultado.") +
    grid2([
        ("Erro aleatorio",
         "Oscila para cima e para baixo, sem direcao fixa. Ex.: pequenas variacoes na leitura de "
         "uma balanca. <b>Dilui-se</b> com mais medicoes e nao invalida a media."),
        ("Vies (erro sistematico)",
         "Erro com <b>direcao constante</b>. Ex.: uma balanca descalibrada que sempre marca 5 g a "
         "mais. <b>Nao</b> se dilui com mais medidas — <b>contamina todas</b> elas do mesmo jeito."),
    ]) +
    tbl(["Situacao na POLITEC", "Tipo", "Consequencia"],
        [["Balanca descalibrada que pesa sempre acima", "Vies", "Todos os laudos daquele periodo saem errados."],
         ["Variacao natural entre tecnicos ao pipetar", "Erro aleatorio", "Some com a media de varias medidas."],
         ["Sistema com fuso horario errado no registro", "Vies sistematico", "Todas as horas ficam deslocadas."],
         ["Leitura de absorbancia com ruido do aparelho", "Erro aleatorio", "Reduz-se com calibracao e replica."]],
        num_cols=[]) +
    callout("err", "Mais dados nao corrigem vies",
        "Se o vies existe, medir mais so produz mais dados errados. Antes de aumentar o volume, "
        "<b>calibre o instrumento e revise o processo</b>. Erro aleatorio a estatistica resolve; "
        "vies so a metrologia resolve.")
)

cad.section("aplicacao-medida-certa", "Aplicacao pratica: escolhendo a medida certa para cada pergunta",
    p("Nao existe &ldquo;melhor medida&rdquo;. Existe a medida que responde a pergunta que foi feita. Este guia "
      "de bolso ajuda a escolher — e a nao cair na armadilha de responder tudo com a media.") +
    tbl(["A pergunta do gestor", "Medida certa", "Por que nao a media"],
        [["&ldquo;Como esta o desempenho tipico?&rdquo;", "<b>Mediana</b>",
          "A media e distorcida por poucos casos extremos."],
         ["&ldquo;Total produzido no mes?&rdquo;", "<b>Soma</b>",
          "Aqui nao e estatistica, e acumulado — a soma responde direto."],
         ["&ldquo;O processo e estavel?&rdquo;", "<b>Desvio padrao / CV</b>",
          "A media nao diz nada sobre variacao entre meses."],
         ["&ldquo;Qual o pior caso que devo explicar?&rdquo;", "<b>P90 / P95 / maximo</b>",
          "A media esconde a cauda longa dos casos lentos."],
         ["&ldquo;Qual exame e mais frequente?&rdquo;", "<b>Moda</b>",
          "A media nao faz sentido para categoria."],
         ["&ldquo;O setor Y e mais lento que o X?&rdquo;", "<b>Comparacao de medianas</b>",
          "Medias podem parecer iguais com distribuicoes muito diferentes."]],
        num_cols=[]) +
    grid2([
        ("Pergunta de eficiencia",
         "Use <b>mediana + P90</b>. A mediana mostra a rotina; o P90 mostra o que a direcao precisa "
         "explicar nas reunioes. As duas juntas contam a historia completa."),
        ("Pergunta de planejamento",
         "Use <b>desvio padrao</b> e <b>CV</b>. Eles dizem quanta capacidade extra o setor precisa "
         "para absorver a variacao sem estourar prazos."),
    ]) +
    callout("tip", "A pergunta vem primeiro",
        "Antes de escolher a medida, escreva a pergunta em uma frase. Se a frase tem &ldquo;tipico&rdquo;, "
        "pense em mediana; se tem &ldquo;total&rdquo;, em soma; se tem &ldquo;estavel&rdquo;, em dispersao; se tem &ldquo;pior "
        "caso&rdquo;, em percentil.")
)

cad.section("metricas-gestao-pericial", "Metricas de gestao pericial: TAT, backlog, produtividade e qualidade",
    p("Chegamos a ponte entre os fundamentos e o resto do curso. Quatro familias de metricas "
      "sustentam a gestao de qualquer laboratorio — e cada uma tem uma pitada de estatistica "
      "descritiva por dentro.") +
    tbl(["Familia", "Metricas tipicas", "Medida estatistica util", "Pergunta que responde"],
        [["<b>Prazo (TAT)</b>", "Tempo de emissao, % dentro do prazo",
          "Mediana, P90, media", "Entregamos no tempo prometido?"],
         ["<b>Fila (backlog)</b>", "Exames pendentes, idade da fila",
          "Soma, tendencia", "A fila cresce ou encolhe?"],
         ["<b>Produtividade</b>", "Laudos/perito, exames/setor",
          "Media, mediana, ranking", "Quem produz o que, e a que custo?"],
         ["<b>Qualidade</b>", "Retrabalho, completude, erros",
          "% / taxa de inconsistencia", "O trabalho foi feito bem da primeira vez?"]],
        num_cols=[]) +
    bar_chart(["TAT", "Backlog", "Produtividade", "Qualidade"],
              [28, 62, 45, 80],
              title="Exemplo ilustrativo: onde a gestao mais precisa agir",
              subtitulo="Barra em destaque = pior desempenho relativo a meta. Aqui, o backlog.",
              destaque=1) +
    kpi([
        ("TAT", "Prazo"),
        ("Backlog", "Fila"),
        ("Produtividade", "Volume"),
        ("Qualidade", "Retrabalho"),
    ]) +
    callout("err", "Medir produtividade sem qualidade",
        "O <b>Cobra Effect</b> mostrou o risco. Produtividade sem uma metrica de qualidade ao lado "
        "vira convite a fragmentacao de laudos. As quatro familias andam <b>juntas</b> — nunca "
        "isole o volume.")
)

# =================================================================
# PARTE 3 - PRATICA
# =================================================================
cad.grp("Parte 3 · Pratica guiada",
        "Sete laboratorios curtos de papel e raciocinio para fixar os conceitos do dia.")

cad.section("lab1", "Lab 1 — Media x mediana com dados de TAT",
    p("Objetivo: sentir, na pratica, como um unico outlier distorce a media e como a mediana "
      "protege o diagnostico.") +
    ficha("g", "Contexto",
        "Voce e o gestor do laboratorio de DNA e recebeu os tempos de emissao (em dias) de 7 laudos: "
        "<b>3, 4, 4, 5, 6, 7 e 90</b>. O caso de 90 dias aguardou reagente importado.") +
    step([
        ("Ordene os dados", "3, 4, 4, 5, 6, 7, 90. Confirme que a mediana e o 4o valor: <b>5</b>."),
        ("Calcule a media", "(3+4+4+5+6+7+90) / 7 = 119 / 7 = <b>17 dias</b>."),
        ("Compare com a mediana", "Media 17 x mediana 5. Qual descreve a rotina do laboratorio?"),
        ("Escreva a frase para a imprensa", "Use o padrao <b>mediana + contexto do outlier</b>."),
        ("Repita sem o outlier", "3,4,4,5,6,7: media 4,83 e mediana 5. Note como a media &ldquo;salta&rdquo; "
         "para perto da mediana quando o caso atipico sai."),
    ]) +
    callout("tip", "Resposta esperada",
        "<i>&ldquo;Nossa mediana e 5 dias. O caso de 90 dias foi excepcional, por falta de reagente "
        "importado; ja foi resolvido e nao representa a rotina.&rdquo;</i>")
)

cad.section("lab2", "Lab 2 — Classifique os dados da POLITEC",
    p("Objetivo: treinar a classificacao estruturado / semiestruturado / nao estruturado antes de "
      "escolher qualquer ferramenta.") +
    step([
        ("Liste os itens do seu setor", "Estoque de reagentes, perfil genetico no CODIS, laudo em "
         "PDF, foto de local, audio de entrevista, resultado de toxicologia (0,8 mg/L), planilha de "
         "entrada/saida no IML."),
        ("Classifique cada um", "Escreva E, S ou N ao lado."),
        ("Justifique", "Por que o laudo em PDF e nao estruturado, mesmo sendo um arquivo?"),
        ("Escolha a ferramenta", "Para cada tipo, que ferramenta faz sentido: planilha, banco "
         "relacional ou IA/visao computacional?"),
    ]) +
    tbl(["Item", "Tipo", "Ferramenta provavel"],
        [["Estoque de reagentes", "Estruturado", "Planilha / banco"],
         ["Perfil genetico no CODIS", "Estruturado", "Banco de dados"],
         ["Laudo em texto livre", "Nao estruturado", "IA / NLP"],
         ["Foto de local de crime", "Nao estruturado", "Visao computacional"],
         ["XML/JSON de integracao", "Semiestruturado", "Parser / middleware"],
         ["Resultado de toxicologia (0,8 mg/L)", "Estruturado", "Planilha"],
         ["Audio de entrevista", "Nao estruturado", "Transcricao + indice"]],
        num_cols=[])
)

cad.section("lab3", "Lab 3 — Auditoria de qualidade nos 4 pilares",
    p("Objetivo: aplicar os quatro pilares a um laudo real (ou ficticio) e decidir se ele e "
      "confiavel.") +
    step([
        ("Escolha um laudo", "Pode ser um modelo em branco do seu setor."),
        ("Acuracia", "A hora, o local e as medidas conferem com a realidade fisica?"),
        ("Completude", "Ha assinatura do responsavel e especificacao do metodo analitico?"),
        ("Consistencia", "O status no laboratorio e igual ao status no portal da Delegacia?"),
        ("Atualidade", "O laudo chegou em tempo de ser util a investigacao?"),
    ]) +
    checklist([
        "Identifiquei pelo menos uma falha em algum pilar.",
        "Propus uma correcao concreta (campo obrigatorio, validacao, integracao, prazo).",
        "Sei dizer qual pilar, se falhar, derruba o laudo inteiro.",
    ])
)

cad.section("lab4", "Lab 4 — Lendo um boxplot e um histograma",
    p("Objetivo: interpretar os graficos que resumem a producao sem olhar os numeros brutos.") +
    bar_chart(["Seg", "Ter", "Qua", "Qui", "Sex"], [78, 42, 44, 40, 48],
              title="Exames recebidos por dia", subtitulo="Histograma de exemplo.", destaque=0) +
    step([
        ("Leia o histograma", "Em qual dia esta o maior volume? O que isso sugere para a escala?"),
        ("Leia o boxplot (do slide do Tukey)", "Onde esta a mediana? Onde comecam as antenas? Ha "
         "pontos isolados?"),
        ("Ligue os dois", "Um pico no histograma e um outlier no boxplot sao a mesma coisa? Por que?"),
        ("Decida uma acao", "Escreva uma medida de gestao a partir do que voce viu."),
    ]) +
    callout("err", "Confusao comum",
        "Histograma mostra <b>distribuicao de frequencia</b>; boxplot mostra <b>resumo de uma "
        "variavel</b> (mediana, quartis, outliers). Sao instrumentos diferentes — muitas vezes "
        "usados juntos.")
)

cad.section("lab5", "Lab 5 — Caca a causalidade",
    p("Objetivo: treinar o reflexo de desconfiar de correlacoes antes de afirmar causas.") +
    step([
        ("Leia as tres manchetes", "1) &ldquo;Uso de protetor solar cai quando aumenta o consumo de "
         "sorvete.&rdquo; 2) &ldquo;Mais peritos lotados no IML coincide com mais mortes violentas.&rdquo; "
         "3) &ldquo;Laboratorios com mais computadores emitem mais laudos.&rdquo;"),
        ("Para cada uma, pergunte", "Existe correlacao? Existe mecanismo real? Ha uma terceira "
         "variavel escondida?"),
        ("Classifique", "Correlacao espuria / causalidade real / causalidade inversa."),
        ("Escreva a versao correta", "Reescreva a manchete sem afirmar causa sem prova."),
    ]) +
    tbl(["Manchete", "Veredito", "Terceira variavel"],
        [["Protetor solar x sorvete", "Correlacao espuria", "Temperatura / epoca do ano"],
         ["Peritos x mortes violentas", "Causalidade inversa", "O crime gera a demanda por pericia"],
         ["Computadores x laudos", "Confusao", "Tamanho e estrutura do laboratorio"]],
        num_cols=[])
)

cad.section("lab6-variancia-desvio", "Lab 6 — Calculo manual de variancia e desvio padrao",
    p("Objetivo: calcular variancia e desvio padrao com lapis e papel, entendendo cada passo — sem "
      "usar a funcao pronta da planilha. A producao (em exames) de 5 meses foi: <b>90, 95, 100, 105, "
      "110</b>.") +
    step([
        ("Calcule a media", "(90+95+100+105+110) / 5 = 500 / 5 = <b>100</b>."),
        ("Monte a tabela dos desvios", "Para cada valor, calcule valor - media: -10, -5, 0, +5, +10."),
        ("Eleve ao quadrado", "100, 25, 0, 25, 100. A soma dos quadrados e <b>250</b>."),
        ("Calcule a variancia", "250 / 5 = <b>50</b> (media dos quadrados dos desvios)."),
        ("Extraia a raiz", "Raiz de 50 = <b>~7,1 exames</b>. Esse e o desvio padrao: a variacao "
         "tipica em torno da media."),
        ("Interprete", "O setor varia cerca de 7 exames para mais ou para menos. E estavel? Calcule "
         "o CV: 7,1 / 100 = <b>7%</b> — muito estavel."),
    ]) +
    code("""
        Valor   | Desvio | Desvio^2
        --------+--------+---------
         90     |  -10   |   100
         95     |   -5   |    25
        100     |    0   |     0
        105     |   +5   |    25
        110     |  +10   |   100
        --------+--------+---------
        Soma            =    250
        Variancia = 250/5 =   50
        Desvio    = raiz(50) = 7,1
        CV        = 7,1/100  = 7%
        """, "texto") +
    callout("err", "Esquecer de elevar ao quadrado",
        "Se voce simplesmente somar os desvios (-10-5+0+5+10), o resultado e <b>zero</b> — e nao "
        "diz nada. Elevar ao quadrado e o que impede os desvios positivos e negativos de se "
        "cancelarem.")
)

cad.section("lab7-tabela-producao", "Lab 7 — Interpretando uma tabela de producao real",
    p("Objetivo: partir de uma tabela de producao mensal (dados ilustrativos) e extrair dela as "
      "metricas de gestao: media, mediana, desvio, CV, P90 e outliers. Este e o tipo de leitura "
      "que a direcao espera de voce.") +
    tbl(["Mes", "Laudos emitidos", "TAT medio (dias)"],
        [["Janeiro", "120", "6"],
         ["Fevereiro", "95", "5"],
         ["Marco", "110", "7"],
         ["Abril", "100", "6"],
         ["Maio", "105", "45"],
         ["Junho", "115", "6"]],
        num_cols=[1, 2]) +
    step([
        ("Media dos laudos", "(120+95+110+100+105+115) / 6 = 645 / 6 = <b>107,5 laudos/mes</b>."),
        ("Mediana dos laudos", "Ordene: 95, 100, 105, [110, 115], 120. Mediana = (110+115)/2 = "
         "<b>112,5</b>."),
        ("TAT: media x mediana", "TATs: 6, 5, 7, 6, 45, 6. Media = 75/6 = <b>12,5 dias</b>; "
         "mediana = <b>6 dias</b>. A media foi distorcida por maio."),
        ("Investigue o outlier", "Maio tem TAT 45 dias — 7x a mediana. Pergunte: <b>o que aconteceu "
         "em maio?</b> Ferias? Falta de insumo? Mutirao em outro setor?"),
        ("Decida a acao", "Sem explicacao, o caso de maio contamina todo o relatorio. Com contexto, "
         "a narrativa fica: &ldquo;mediana de 6 dias; maio foi atipico por [motivo]&rdquo;."),
        ("Monte o resumo executivo", "Produza a frase que voce levaria a direcao, com mediana + "
         "contexto e sem esconder o outlier."),
    ]) +
    kpi([
        ("107,5", "Media de laudos/mes"),
        ("112,5", "Mediana de laudos"),
        ("6 dias", "Mediana do TAT"),
        ("12,5 dias", "Media do TAT (distorcida)"),
    ]) +
    callout("tip", "Resumo executivo do Lab 7",
        "<i>&ldquo;A producao tipica e de ~112 laudos/mes, com TAT mediano de 6 dias. Em maio houve "
        "um caso atipico de 45 dias, puxando a media do TAT para 12,5; o motivo foi investigado e "
        "ja corrigido.&rdquo;</i>")
)

# =================================================================
# PARTE 4 - CENARIOS
# =================================================================
cad.grp("Parte 4 · Cenarios e aplicacoes praticas",
        "Quatro situacoes reais da POLITEC para treinar decisao com dados, no estilo do curso SESP/MT.")

cad.section("cenario-tat-dna", "Cenario A — Diagnostico de TAT do laboratorio de DNA",
    p("<b>O problema:</b> a direcao recebe uma denuncia de que o laboratorio de DNA e lento. O "
      "relatorio atual mostra apenas a <b>media de 28 dias</b> e a imprensa ja publicou a manchete. "
      "Voce precisa reconstruir o diagnostico com honestidade estatistica.") +
    kpi([
        ("28 dias", "Media (distorcida)"),
        ("5 dias", "Mediana (rotina real)"),
        ("120 dias", "Outlier a explicar"),
    ]) +
    grid2([
        ("Passos para diagnosticar",
         ul(["Listar os <b>TATs individuais</b> do periodo.",
             "Calcular <b>media, mediana e P90</b>.",
             "Isolar o <b>outlier</b> e investigar a causa.",
             "Comparar a rotina (mediana) com a meta pactuada.",
             "Montar um boxplot e um histograma dos TATs."])),
        ("KPIs a reportar",
         ul(["<b>Mediana do TAT</b> — eficiencia tipica.",
             "<b>P90 do TAT</b> — o pior caso que a direcao explica.",
             "<b>% dentro do prazo</b> — conformidade.",
             "<b>Numero de outliers</b> — casos especiais.",
             "<b>CV</b> — estabilidade do processo."])),
    ]) +
    step([
        ("Recolha os dados", "Exporte os TATs de todos os laudos do periodo, um por linha, com data "
         "de recebimento e de emissao."),
        ("Calcule o conjunto", "Media, mediana, P90 e desvio padrao. Anote a distancia entre media e "
         "mediana — ela mede o efeito dos extremos."),
        ("Investigue os outliers", "Para cada TAT muito acima da mediana, registre a causa: "
         "reagente, reanalise, pendencia de informacao da delegacia."),
        ("Monte a narrativa", "Reporte <b>mediana + contexto</b>. Nunca so a media."),
        ("Proponha acao", "Um plano concreto para reduzir os casos extremos (estoque de seguranca, "
         "fluxo de reanalise, comunicacao com a delegacia)."),
    ]) +
    callout("err", "Prometer a media como meta",
        "Definir a meta de TAT pela <b>media</b> garante que metade dos casos fique acima dela. A "
        "meta deve olhar a mediana (rotina) e o P90 (pior caso), nao a media.")
)

cad.section("cenario-auditoria-iml", "Cenario B — Auditoria de qualidade da base de necropsias do IML",
    p("<b>O problema:</b> antes de publicar qualquer indicador de mortalidade, a direcao do IML "
      "precisa confiar na base. Voce foi chamado para auditar os registros de necropsias aplicando "
      "os <b>4 pilares da qualidade</b> e apontar onde o dado falha.") +
    grid2([
        ("\U0001f3af Acuracia",
         "As causas de morte e as coordenadas batem com os laudos fisicos? Ha idade ou peso "
         "impossiveis? <b>Teste:</b> compare uma amostra com o documento original."),
        ("\U0001f4d0 Completude",
         "Faltam campos obrigatorios (causa, data, responsavel)? <b>Teste:</b> conte celulas vazias "
         "nos campos criticos e calcule o percentual."),
        ("\U0001f517 Consistencia",
         "O status no IML bate com o portal da Delegacia? Ha duas necropsias para o mesmo caso? "
         "<b>Teste:</b> procure duplicatas por chave (numero + data)."),
        ("\u23f1\ufe0f Atualidade",
         "Os registros estao sincronizados com a rotina atual? Ha casos antigos sem baixa? "
         "<b>Teste:</b> compare a data do ultimo registro com a data de hoje."),
    ]) +
    step([
        ("Defina a chave unica", "Numero de necropsia + data identifica o caso sem ambiguidade."),
        ("Amostre", "Selecione aleatoriamente 30-50 registros para conferencia manual contra os "
         "laudos. E o suficiente para estimar o padrao de erro."),
        ("Meca cada pilar", "Acuracia (erros/amostra), completude (% vazios), consistencia "
         "(divergencias), atualidade (defasagem em dias)."),
        ("Priorize", "Ordene as falhas por impacto. Uma taxa alta de campos vazios na causa da morte "
         "inviabiliza qualquer estatistica de mortalidade."),
        ("Documente", "Registre a metodologia da auditoria. A auditoria tambem precisa ser auditavel."),
    ]) +
    ficha("r", "O risco de publicar base suja",
        "Indicadores de mortalidade construidos sobre base incompleta levam a politicas publicas "
        "erradas. Antes de medir, <b>auditar</b>. Qualidade de dado nao e preciosismo — e a base da "
        "decisao publica.")
)

cad.section("cenario-relatorio-diretoria", "Cenario C — Relatorio gerencial para a diretoria",
    p("<b>O problema:</b> a diretoria pede <b>um painel de uma pagina</b> com o desempenho da "
      "instituicao. Voce tem muitas metricas disponiveis e precisa escolher <b>poucas</b> — as que "
      "respondem as perguntas certas e resistem a questionamento.") +
    step([
        ("Comece pela pergunta, nao pelo dado", "Escreva as <b>3 perguntas</b> que a diretoria "
         "realmente precisa responder. Ex.: &ldquo;estamos no prazo?&rdquo;, &ldquo;a fila cresce?&rdquo;, &ldquo;a qualidade "
         "se mantem?&rdquo;."),
        ("Escolha 3 a 5 KPIs", "Para cada pergunta, um indicador com <b>meta e direcao</b>. Ex.: TAT "
         "mediano, % dentro do prazo, backlog total, taxa de retrabalho."),
        ("Defina o contexto", "Cada KPI vem com comparacao: mes anterior, mesma epoca do ano, meta. "
         "Numero solto nao orienta decisao."),
        ("Use visualizacao honesta", "Barras e linhas, eixo Y no zero, titulo claro, fonte dos "
         "dados. Nada de 3D nem de pizza com 10 fatias."),
        ("Feche com uma recomendacao", "O painel termina com a <b>acao proposta</b>, nao so com o "
         "diagnostico. Gestor decide; relatorio so descreve."),
    ]) +
    tbl(["Pergunta da diretoria", "KPI escolhido", "Meta", "Visual"],
        [["Estamos no prazo?", "% laudos dentro do prazo", ">= 90%", "Cartao + linha de tendencia"],
         ["A fila cresce?", "Backlog total e variacao mensal", "Estavel ou em queda", "Colunas + linha"],
         ["A qualidade se mantem?", "Taxa de retrabalho", "<= 5%", "Cartao + barras por setor"],
         ["Onde esta o gargalo?", "TAT mediano por setor", "<= 15 dias", "Barras horizontais"]],
        num_cols=[]) +
    callout("err", "Painel com 30 indicadores",
        "Um painel que mostra tudo nao responde nada. A diretoria decide sob pressao: <b>3 a 5 KPIs</b> "
        "com meta valem mais do que 30 numeros sem hierarquia. A regra dos 3 segundos de Few "
        "continua valendo.")
)

cad.section("cenario-cisne-negro", "Cenario D — Deteccao precoce de um Cisne Negro",
    p("<b>O problema:</b> em uma semana, o volume de exames de uma nova substancia cresce 40%, "
      "fora do padrao historico. Ninguem sabe ainda do que se trata. Voce tem a chance de detectar "
      "<b>precocemente</b> um evento raro de alto impacto — ou de deixa-lo passar como mais um "
      "outlier.") +
    flow_h([
        ("\U0001f4c8", "Sinal fora da curva"),
        ("\U0001f50e", "Investigacao"),
        ("\U0001f9ea", "Protocolo novo"),
        ("\U0001f6e1\ufe0f", "Plano de contingencia"),
    ]) +
    kpi([
        ("+40%", "Volume fora do padrao"),
        ("7 dias", "Janela de deteccao"),
        ("1000%", "Sobrecarga possivel em crise"),
    ]) +
    step([
        ("Detecte o desvio", "Monitore o volume por tipo de exame com <b>limites estatisticos</b> "
         "(2-3 desvios padrao). O sinal precisa aparecer sozinho, nao depender de alguem notar."),
        ("Nao descarte como erro", "Um pico nao e &ldquo;dado sujo&rdquo; por definicao. Na pericia, outlier e "
         "pista — investigue antes de descartar."),
        ("Investigue a causa", "Nova droga? Novo metodo de adulteracao? Mudanca regulatoria? "
         "Envolva a equipe tecnica e a inteligencia."),
        ("Acione protocolo", "Se for substancia desconhecida, mobilize desenvolvimento de metodo "
         "analitico e reagentes alternativos."),
        ("Prepare contingencia", "Ative reserva de capacidade, escala extra e estoque emergencial. "
         "Modelos baseados na media do passado nao preveem Cisnes Negros."),
        ("Registre e aprenda", "Documente o evento e o plano. O proximo Cisne Negro pode ser "
         "diferente, mas a <b>capacidade de reagir</b> se transfere."),
    ]) +
    ficha("p", "A licao de Taleb aplicada",
        "Voce nao preve o Cisne Negro com a media historica — mas pode construir <b>antifragilidade</b>: "
        "monitoramento de desvios, reserva de capacidade e protocolos de crise. Detectar em 7 dias "
        "vale mais do que acertar a previsao impossivel.")
)

# =================================================================
# PARTE 5 - FECHAMENTO
# =================================================================
cad.grp("Parte 5 · Fechamento — resumo, tarefa, quiz, folha de cola e referencias",
        "Consolide o dia: recapitule, teste-se, guarde a cola e siga as referencias.")

cad.section("resumo-dia1", "Resumo do Dia 1: os conceitos que ficam",
    p("Reunimos, em dois blocos, tudo o que sustenta o restante do curso. Se voce levar so esta "
      "pagina para casa, que ela sirva de mapa mental do dia.") +
    grid2([
        ("\U0001f305 Manha — Fundamentos da Analise",
         ul(["<b>DIKW</b>: dado -> informacao -> conhecimento -> sabedoria.",
             "<b>Locard digital</b>: todo contato deixa um dado.",
             "<b>3 tipos</b> de dados; 80% do acervo e nao estruturado.",
             "<b>4 pilares</b>: acuracia, completude, consistencia, atualidade.",
             "Dado sujo = prova contaminada (nulidade processual).",
             "Dado, metrica e indicador sao coisas diferentes."])),
        ("\U0001f306 Tarde — Fundamentos Estatisticos",
         ul(["<b>Media mente; mediana conta a verdade.</b>",
             "<b>Dispersao</b> define a estrategia (desvio, variancia, CV).",
             "<b>Boxplot e histograma</b> revelam o que a media esconde.",
             "<b>Correlacao nao implica causalidade</b>.",
             "<b>Outliers</b> sao pistas, nao lixo.",
             "<b>Cisnes Negros</b> pedem contingencia, nao previsao."])),
    ]) +
    legenda([
        ("\U0001f4d0", "Dado confiavel", "Construido na entrada, com os 4 pilares; auditavel em toda a cadeia de custodia."),
        ("\U0001f3af", "Decisao com contexto", "Mediana + outlier explicado, quatro familias de metricas, pergunta antes da medida."),
        ("\U0001f517", "Ponte para o Dia 2", "A base limpa e padronizada que voce vai manipular no Excel comeca nas ideias de hoje."),
    ]) +
    ficha("g", "A frase do dia",
        "<b>Transformar vestigios em inteligencia tecnico-cientifica</b> exige tanto rigor na bancada "
        "quanto rigor no dado. — Prof. Renato Rosa")
)

cad.section("tarefa-casa", "Tarefa de casa: preparando o Dia 2",
    p("Antes do proximo encontro, complete estas tarefas praticas. Elas transformam os conceitos de "
      "hoje em base concreta para o laboratorio de planilhas.") +
    checklist([
        "Escolha <b>um indicador</b> do seu setor e defina: formula, meta, direcao e frequencia de leitura.",
        "Mapeie o <b>ciclo de dados</b> do seu setor em uma folha (entradas, saidas, sistemas, pontos de quebra).",
        "Separe <b>uma base real anonimizada</b> do seu setor para trabalharmos no Dia 2.",
        "Teste os <b>4 pilares</b> em um formulario ou laudo do seu setor e anote as falhas.",
        "Traga o <b>notebook com Excel</b> (ou conta Google) instalado e atualizado.",
    ]) +
    ficha("a", "Por que isso importa",
        "Chegar ao Dia 2 com uma base e um indicador definidos transforma a aula de planilha em "
        "<b>trabalho aplicado sobre o seu problema</b> — nao em exercicio generico.")
)

cad.section("quiz", "Quiz final do Dia 1 (15 perguntas)",
    q("A sequencia correta da piramide DIKW e:",
      ["Sabedoria \u2192 Conhecimento \u2192 Informacao \u2192 Dado",
       "Dado \u2192 Informacao \u2192 Conhecimento \u2192 Sabedoria",
       "Dado \u2192 Conhecimento \u2192 Informacao \u2192 Sabedoria",
       "Informacao \u2192 Dado \u2192 Sabedoria \u2192 Conhecimento"], 1,
      "A base e o dado bruto; o topo e a acao estrategica.") +
    q("Um exame tem tempo de emissao de 4, 5, 5, 6 e 120 dias. Qual par de medidas descreve melhor "
      "a rotina e o caso atipico?",
      ["Media (28) e moda (5)", "Mediana (5) e o contexto do outlier de 120",
       "Somente a media (28)", "Amplitude (116) apenas"], 1,
      "A mediana representa a rotina; o outlier precisa ser explicado, nao escondido.") +
    q("O desvio padrao alto em um laboratorio indica que:",
      ["A media esta errada", "A producao e imprevisivel e exige gestao de crise",
       "O laboratorio produz mais", "Nao ha outliers"], 1,
      "Dispersao alta = variacao alta = maior dificuldade de planejamento.") +
    q("O boxplot de Tukey mostra, na caixa, aproximadamente:",
      ["Todos os dados", "50% centrais dos dados (a rotina)",
       "Apenas os outliers", "A soma total"], 1,
      "A caixa vai do 1o ao 3o quartil (50% central); as antenas marcam o esperado.") +
    q("Qual afirmacao esta correta?",
      ["Correlacao sempre implica causalidade",
       "Causalidade sempre implica correlacao, mas nao o contrario",
       "Causalidade nunca gera correlacao",
       "Nenhuma das anteriores"], 1,
      "Se A causa B, eles tendem a andar juntos; mas andar junto nao prova causa.") +
    q("Segundo Locard, adaptado a era digital:",
      ["So contatos fisicos deixam vestigios",
       "Todo contato, fisico ou digital, deixa um dado",
       "Dados digitais nao valem como prova",
       "O vestigio so importa se for biologico"], 1,
      "A cadeia de custodia dos dados e tao critica quanto a das evidencias fisicas.") +
    q("Qual dos 4 pilares da qualidade fala de &ldquo;o mesmo dado ser igual em todos os sistemas&rdquo;?",
      ["Acuracia", "Completude", "Consistencia", "Atualidade"], 2,
      "Positivo no laboratorio e Pendente no portal e um caso de inconsistencia.") +
    q("Um outlier de &ldquo;0 exames em uma semana&rdquo; deve ser:",
      ["Apagado da base", "Investigado (falta de reagente? quebra? paralisacao?)",
       "Substituido pela media", "Ignorado, pois distorce"], 1,
      "Na POLITEC, o outlier nao e apagado: e investigado como alerta de gestao.") +
    q("O Cisne Negro de Taleb, na pericia, e melhor tratado com:",
      ["Modelos baseados na media historica", "Planos de contingencia e reserva de capacidade",
       "Mais graficos de pizza", "Descarte de casos raros"], 1,
      "Eventos extremos e improvaveis nao aparecem na media do passado.") +
    q("A regra dos 3 segundos de Stephen Few serve para:",
      ["Medir tempo de processamento", "Garantir que um gestor entenda o dashboard rapidamente",
       "Definir o numero de graficos permitidos", "Calcular o TAT"], 1,
      "Poucos indicadores, com meta e cor que apontam a acao.") +
    q("Na producao mensal 90, 95, 100, 105, 110 (exames), o desvio padrao e aproximadamente:",
      ["0", "7,1", "50", "100"], 1,
      "Variancia = 50; desvio padrao = raiz de 50 = ~7,1 exames.") +
    q("Um laudo com &ldquo;Positivo&rdquo; no laboratorio e &ldquo;Pendente&rdquo; no portal viola qual pilar?",
      ["Acuracia", "Completude", "Consistencia", "Atualidade"], 2,
      "Consistencia e o pilar que exige o mesmo dado igual em todos os sistemas.") +
    q("Qual medida usar para responder &ldquo;em quanto tempo 90% dos laudos ficam prontos?&rdquo;",
      ["A media", "A moda", "O percentil 90 (P90)", "A amplitude"], 2,
      "O P90 da o prazo que cobre 90% dos casos — melhor que a media para prazos.") +
    q("No exemplo dos dois laboratorios com media 100 exames/mes, o que os diferencia e:",
      ["O total produzido", "O desvio padrao (dispersao)", "A moda", "O numero de meses"], 1,
      "Mesma media, dispersoes distintas: um estavel, outro caotico.") +
    q("A melhor definicao de indicador (KPI) e:",
      ["Um dado bruto registrado", "Uma metrica com meta e direcao de sucesso",
       "Qualquer grafico colorido", "O total acumulado do ano"], 1,
      "Metrica vira indicador quando tem meta e direcao que orientam a decisao.")
)

cad.section("cheatsheet", "Folha de cola do Dia 1",
    glossary([
        ("DIKW", "Data \u2192 Information \u2192 Knowledge \u2192 Wisdom. A escada do vestigio ate a decisao (Ackoff, 1989)."),
        ("Principio de Locard", "&ldquo;Todo contato deixa um vestigio.&rdquo; Base da criminalistica (Lyon, 1910)."),
        ("Cadeia de custodia do dado", "Garantia de que o dado e integro, rastreavel e valido do registro a decisao."),
        ("Dado x metrica x indicador", "Dado = registro; metrica = medida; indicador = metrica com meta e direcao."),
        ("4 pilares da qualidade", "Acuracia, Completude, Consistencia, Atualidade."),
        ("Media", "Soma \u00f7 quantidade. Sensivel a outliers."),
        ("Mediana", "Valor central. Robusta a outliers — representa a rotina."),
        ("Moda", "Valor que mais se repete. Util para categorias."),
        ("Amplitude", "Maior valor menos o menor. Olha so os extremos."),
        ("Variancia", "Media dos desvios ao quadrado. Unidade ao quadrado."),
        ("Desvio padrao", "Raiz da variancia. Baixo = estavel; alto = imprevisivel."),
        ("Coef. de variacao (CV)", "Desvio / media, em %. Permite comparar setores de tamanhos diferentes."),
        ("Quartis e percentis", "Q1/Q2/Q3 dividem em 4; P90 e o prazo que cobre 90% dos casos."),
        ("Boxplot", "Caixa (50% central) + mediana + antenas + outliers (Tukey, 1977)."),
        ("Histograma", "Distribuicao de frequencia por faixas. Revela gargalos."),
        ("Curva normal", "68% a 1 desvio, 95% a 2, 99,7% a 3. Base dos limites de alerta."),
        ("Erro x vies", "Erro aleatorio dilui-se na media; vies e sistematico e contamina tudo."),
        ("Correlacao", "Duas variaveis andam juntas. Nao prova causa."),
        ("Outlier", "Valor fora da curva. Na pericia, e pista a investigar, nao lixo a apagar."),
        ("Cisne Negro", "Evento raro e de alto impacto, invisivel a media historica (Taleb, 2007)."),
    ]) +
    tbl(["Numero do dia", "Significado"],
        [["4, 5, 5, 6, 120", "TAT de DNA: media 28, mediana 5."],
         ["80%", "Parcela do acervo pericial que e dado nao estruturado."],
         ["+40%", "Ganho potencial de cruzamento com nomenclatura padronizada."],
         ["3 segundos", "Tempo maximo para um gestor ler um dashboard (Few)."],
         ["1000%", "Sobrecarga do IML em um desastre de massa (Cisne Negro)."],
         ["68 / 95 / 99,7%", "Faixas da curva normal (1, 2 e 3 desvios padrao)."],
         ["P90", "Prazo em que 90% dos laudos ficam prontos — meta de prazo defensavel."]],
        num_cols=[0])
)

cad.section("referencias", "Referencias e ponte para o Dia 2",
    p("As referencias que sustentam o Dia 1:") +
    tbl(["Autor", "Obra", "Por que importa"],
        [["Russell Ackoff", "&ldquo;From Data to Wisdom&rdquo; (1989)",
          "Origem da piramide DIKW e da evolucao do conhecimento organizacional."],
         ["Edmond Locard", "Principio de Locard (Lyon, 1910)",
          "Fundamento da criminalistica moderna: &ldquo;todo contato deixa um vestigio&rdquo;."],
         ["Stephen Few", "&ldquo;Information Dashboard Design&rdquo; (2006)",
          "Design de dashboards para decisao sob pressao (regra dos 3 segundos)."],
         ["John Tukey", "&ldquo;Exploratory Data Analysis&rdquo; (1977)",
          "Criacao do boxplot e da Analise Exploratoria de Dados (EDA)."],
         ["Nassim N. Taleb", "&ldquo;A Logica do Cisne Negro&rdquo; (2007)",
          "Eventos de alto impacto e os limites dos modelos estatisticos convencionais."],
         ["W. Edwards Deming", "Controle estatistico da qualidade (seculo XX)",
          "A variacao como inimigo da qualidade; base do pensamento de processo."]],
        num_cols=[]) +
    ficha("g", "Proximo passo — Dia 2",
        "No Dia 2 colocamos a mao na massa: <b>limpeza, padronizacao e estrutura das bases de "
        "exames e ocorrencias periciais no Excel/Google Sheets</b>, com tabelas estruturadas, "
        "referencias absolutas, filtros, ordenacao personalizada, formatacao condicional e o painel "
        "de backlog. Traga seu notebook com Excel instalado.")
)

cad.build()
