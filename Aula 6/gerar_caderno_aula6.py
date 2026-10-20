# -*- coding: utf-8 -*-
"""Gerador do caderno da Aula 6 - POLITEC/MT.

Tema: Gestao de Projetos do zero ao avancado aplicada a processos da POLITEC/MT.
Conteudo: fundamentos de projeto, BPMN, Mermaid, AS-IS/TO-BE, identificacao de
gargalos com dados e automatizacao como intervencao digital.

Rode:  python gerar_caderno_aula6.py
PDF:   python ..\\exportar_pdf.py 6
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from caderno_lib import (Caderno, p, h3, ul, checklist, ficha, callout, tbl, code,
                         step, q, aplicab, grid2, flow_h, kpi, antesdepois,
                         legenda, glossary, bar_chart)
from caderno_svg import (icon, gallery, swimlane_anatomy, gates_anatomy,
                         wait_vs_touch, automation_anatomy, method_chain,
                         build_process_asis, build_process_tobe,
                         build_process_orcamento, build_process_custodia)

cad = Caderno(
    out=str(pathlib.Path(__file__).resolve().parent / "caderno-dia6.html"),
    dia=6,
    kicker="Aula 6 · Gestao de Projetos",
    headline="Gestao de Projetos: do zero ao avancado com BPMN e Mermaid",
    sub="Aprenda a modelar processos como a POLITEC/MT realmente trabalha: "
        "descreva o AS-IS em texto, converta em diagrama BPMN com Mermaid, "
        "meca onde esta o gargalo, redesenhe o TO-BE e resolva o gargalo com "
        "automacao. Tres datasets de processo com mais de 9.000 execucoes de "
        "etapa para voce medir, em vez de chutar.",
    meta="Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 6 · "
         "Modulo 8 (Gestao de Projetos e Melhoria de Processos)",
    descricao="Caderno do Dia 6 do Curso de Capacitacao POLITEC/MT: Gestao de Projetos "
              "do zero ao avancado. Fundamentos (escopo, prazo, custo, risco, "
              "stakeholders), BPMN 2.0 (notacao, swimlanes, gateways, eventos), Mermaid "
              "(flowchart, sequenceDiagram, stateDiagram, gantt, journey, mindmap), "
              "conversao automatica de texto em diagrama, AS-IS e TO-BE, identificacao "
              "de gargalos com dados (tempo de espera vs execucao, Pareto, Little's Law), "
              "e intervencao digital (Power Automate, Power Apps, scripts). 3 datasets "
              "de processo com 9.500+ execucoes de etapa em modelo estrela."
)

# =================================================================
# ABERTURA
# =================================================================
cad.grp("Abertura", "O salto do dado para a acao: medir o processo, corrigi-lo e automatizar.")

cad.section("boas-vindas", "Bem-vindo ao caderno do Dia 6",
    p("Nos cinco primeiros dias voce aprendeu a <b>medir</b>: estatistica, "
      "planilha, qualidade dos dados, dashboards. Hoje voce vai aprender a "
      "<b>mudar</b>. Gestao de projetos, no nosso contexto, e a arte de "
      "<b>medir um processo, encontrar o gargalo, redesenha-lo e automatizar "
      "a solucao</b>.") +
    p("O dia inteiro gira em torno de uma cadeia de seis passos que voce vai "
      "praticar do inicio ao fim, com dados reais (sinteticos, mas medidos) "
      "dos processos da POLITEC/MT.") +
    method_chain() +
    legenda([
        (icon("project", 26), "Parte 1 - Fundamentos de projeto",
         "Escopo, prazo, custo, risco, stakeholders: o que todo projeto precisa."),
        (icon("book", 26), "Parte 2 - BPMN e Mermaid",
         "A notacao BPMN 2.0 em SVG e o Mermaid para desenhar diagramas como codigo."),
        (icon("search", 26), "Parte 3 - Do texto ao diagrama",
         "Descreva o processo e converta automaticamente em diagrama."),
        (icon("chart", 26), "Parte 4 - Gargalos com dados",
         "Onde o processo perde tempo: espera, execucao, retrabalho, variabilidade."),
        (icon("rocket", 26), "Parte 5 - TO-BE e automacao",
         "Redesenhe o processo e resolva o gargalo com intervencao digital."),
        (icon("check", 26), "Partes 6-7 - Labs e cenarios",
         "Sete labs guiados e tres processos reais modelados ponta a ponta."),
    ])
)

cad.section("mapa-do-dia", "Mapa do Dia 6: da descricao ao processo automatizado",
    p("A manha e a tardeDividem-se em tres blocos. O terceiro - o mais "
      "importante - e a <b>gralha de verdade</b>: voce aplica o metodo "
      "completo em um processo real da POLITEC, medindo o gargalo nos dados.") +
    grid2([
        ("\U0001f305 Manha (08h-12h) - Fundamentos, BPMN e Mermaid",
         ul(["<b>Modulo 1</b> - O que e projeto: escopo, prazo, custo, qualidade, risco",
             "Ciclo de vida, partes interessadas e a matriz poder/interesse",
             "<b>Modulo 2</b> - BPMN 2.0: elementos, swimlanes, gateways, eventos",
             "<b>Mermaid</b>: transformar descricoes em diagramas (flowchart, sequence, state)"])),
        ("\U0001f306 Tarde (13h-17h) - Gargalos, TO-BE e automacao",
         ul(["<b>Modulo 3</b> - Do texto ao diagrama: o metodo das 7 perguntas",
             "<b>Modulo 4</b> - Medir gargalos: espera x execucao, Pareto, Little's Law",
             "<b>Modulo 5</b> - TO-BE e intervencao digital (Power Automate, Power Apps, script)"]))
    ])
)

cad.section("recap-do-curso", "Recap dos cinco dias anteriores",
    p("Onde estamos no percurso da capacitacao. Em seis dias a turma "
      "percorreu o ciclo completo do dado <b>ate agir sobre ele</b>:") +
    tbl(["Dia", "Foco", "Entregavel"],
        [["<b>D1</b>", "Estatistica, qualidade, indicadores", "Raciocínio sobre dado"],
         ["<b>D2</b>", "Planilha, formulas, validacao", "Planilha limpa e tipada"],
         ["<b>D3</b>", "Organizacao, visualizacao, ETL", "Base consolidada"],
         ["<b>D4</b>", "Power BI Desktop + Service", "Relatorio e dashboard"],
         ["<b>D5</b>", "Dashboards de BI (5 cenarios)", "Painel institucional"],
         ["<b>D6</b>", "Gestao de projetos + melhoria", "<b>Processo redesenhado e automatizado</b>"]],
        num_cols=[]) +
    callout("note", "A virada do curso",
        "Ate D5 o trabalho era <b>descrever</b> o que ja existe. A partir de "
        "hoje, o trabalho e <b>mudar</b> o que existe - e mudar com prova, "
        "nao com opiniao.")
)

cad.section("objetivo-do-dia", "Objetivo do Dia 6: um processo medido, corrigido e automatizado",
    p("Ao fim do dia, voce entrega um <b>processo redesenhado com prova de ganho</b>:") +
    checklist([
        "Um diagrama <b>AS-IS</b> em BPMN/Mermaid do processo escolhido.",
        "Uma <b>analise de gargalo</b> com os dados do dataset (nao com palpite).",
        "Um diagrama <b>TO-BE</b> que elimina ou automatiza o gargalo.",
        "Uma <b>proposta de automacao</b> concreta (ferramenta, regra, ganho estimado).",
        "O <b>calculo do ganho</b> em tempo e em recurso (antes x depois).",
    ]) +
    kpi([
        ("6", "passos do metodo"),
        ("3", "datasets de processo"),
        ("9.500+", "execucoes medidas"),
        ("7", "labs guiados"),
    ]) +
    ficha("g", "O principio que governa o dia",
        "Nao se melhora um processo que nao se mede. Hoje voce vai aprender a "
        "<b>medir antes de mudar</b> - e medir com dado, com o mesmo rigor que "
        "aprendeu a aplicar a planilha e ao dashboard.")
)

# =================================================================
# PARTE 1 - FUNDAMENTOS DE GESTAO DE PROJETOS
# =================================================================
cad.grp("Parte 1 - Fundamentos de Gestao de Projetos",
        "O minimo que todo projeto precisa ter: escopo, prazo, custo, qualidade e risco.")

cad.section("o-que-e-projeto", "O que e um projeto (e o que nao e)",
    p("Um <b>projeto</b> e um esforco <b>temporario</b> para criar um "
      "<b>produto, servico ou resultado unico</b>. O triangulo de "
      "<b>escopo, prazo, custo e qualidade</b> define o projeto; voce sempre "
      "pode cortar um dos quatro, mas precisa saber qual esta cortando.") +
    tbl(["Projeto TEM...", "Operacao NAO tem..."],
        [["Inicio e fim definidos", "Fim (e o dia a dia)"],
         ["Objetivo unico", "Objetivo recorrente"],
         ["Recursos proprios", "Recursos rotineiros"],
         ["Riscos de incerteza", "Riscos de rotina"],
         ["Equipe temporaria", "Equipe permanente"]],
        num_cols=[]) +
    aplicab(
        "<b>Quando</b> a POLITEC quer_speed_up o fluxo de requisicao pericial.",
        "<b>Por que</b> isso e um <b>projeto</b> (tem inicio, fim e objetivo "
        "de reduzir o TAT), e nao uma <b>operacao</b> (que seria &quot;todo "
        "dia o laboratorio atende requisicoes&quot;).",
        "<b>Exemplo</b>: &quot;implantar uma fila priorizada por prazo legal no "
        "SIGT em 90 dias&quot; e um projeto. &quot;Atender requisicoes todos os "
        "dias&quot; e a operacao."
    ) +
    callout("err", "A confusao mais comum",
        "Chamar toda mudanca de &quot;projeto&quot;. Se nao tem inicio, fim e "
        "resultado unico, e uma tarefa da operacao - e nao se gerencia com as "
        "ferramentas de projeto.")
)

cad.section("triangulo-projeto", "O triangulo de projeto: o que voce pode cortar",
    p("Escopo, prazo, custo e qualidade estao ligados. Mude um, e os outros "
      "reagem. Saber qual voce esta cortando e o que o sponsor precisa saber.") +
    tbl(["Voce quer...", "Entao aceite que..."],
        [["Reduzir o prazo", "Aumenta o custo OU reduz o escopo (ou aceita mais risco)"],
         ["Reduzir o custo", "Estica o prazo OU corta escopo"],
         ["Aumentar o escopo", "Estica o prazo OU custa mais"],
         ["Aumentar a qualidade", "Custa mais OU demora mais"],
         ["Cortar escopo", "<b>Primeira alavanca</b> de um projeto em aperto"]],
        num_cols=[]) +
    antesdepois(
        "O sponsor pede &quot;segue o prazo, sem aumentar custo e com mais "
        "funcionalidades&quot;. O projeto responde &quot;ok&quot; e decobre no "
        "meio que vai cortar qualidade (ou engenharia).",
        "O projeto responde: &quot;consigo prazo e custo se o escopo for "
        "priorizado em fases; ou prazo e escopo se houver +20% de orcamento&quot;.",
        errado="Promessa cega",
        certo="Trade-off explícito"
    ) +
    callout("tip", "A pergunta do sponsorship",
        "Quando o escopo cresce, pergunte sempre: <b>&quot;Qual dos quatro "
        "nosso vai ceder: prazo, custo ou escopo?&quot;</b> Isso transforma uma "
        "conversa emotiva numa decisao de projeto.")
)

cad.section("ciclo-de-vida", "O ciclo de vida de um projeto: os 5 grupos de processos",
    p("Todo projeto passa por <b>cinco grupos de processos</b> (o modelo "
      "clássico, alinhado ao PMBOK). Cada grupo tem perguntas e entregáveis "
      "próprios.") +
    tbl(["Grupo", "Quando", "Pergunta-chave", "Entregavel tipico"],
        [["<b>Iniciar</b>", "Inicio", "Vale a pena? Quem apoia?", "Termo de abertura, sponsor"],
         ["<b>Planejar</b>", "Inicio", "Como, quando, com quem?", "Plano, cronograma, escopo"],
         ["<b>Executar</b>", "Meio", "Fazendo o plano", "Produtos parciais"],
         ["<b>Monitorar</b>", "Contínuo", "Estamos no plano?", "Relatórios, mudancas"],
         ["<b>Encerrar</b>", "Fim", "Aprendemos algo?", "Termo de aceite, lições"]],
        num_cols=[]) +
    flow_h([
        ("INI", "Iniciar"),
        ("PLA", "Planejar"),
        ("EXE", "Executar"),
        ("MON", "Monitorar"),
        ("ENC", "Encerrar"),
    ]) +
    step([
        ("Fase 1 - Iniciar (semanas 1-2)",
         "Reunir o problema, identificar o sponsor, definir objetivo e "
         "critérios de sucesso. Saída: um parágrafo dizendo o que vai mudar e como."),
        ("Fase 2 - Planejar (semanas 2-6)",
         "Mapear o AS-IS, medir o gargalo, desenhar o TO-BE, estimar esforço "
         "e prazo. Saída: AS-IS, TO-BE e o plano de ondas."),
        ("Fase 3 - Executar (semanas 6-26)",
         "Implantar onda a onda, medindo o ganho de cada. Saída: o processo "
         "rodando com a primeira onda."),
        ("Fase 4 - Monitorar (contínuo)",
         "Comparar TAT planejado x realizado a cada sprint. Saída: painel de "
         "acompanhamento e decisoes de re-priorizacao."),
        ("Fase 5 - Encerrar (ao fim)",
         "Medir o ganho final, documentar o que funcionou, archive o processo "
         "para o proximo projeto."),
    ]) +
    aplicab(
        "<b>Quando</b> a chiefs decide automatizar a cadeia de custodia.",
        "<b>Por que</b> o ciclo de vida evita dois erros: comecar a executar "
        "sem medir (Onda 1 sem plano) e nunca encerrar (sem lições "
        "aprendidas).",
        "<b>Exemplo</b> na POLITEC: <i>o projeto do QR Code na custodia "
        "levou 26 semanas: 6 de mapeamento e medicao, 8 de piloto com duas "
        "unidades, 12 de implantacao - e 3 de medicao de ganho.</i>"
    ) +
    callout("purple", "Monitorar nao e so no fim",
        "A maior parte das falhas de projeto vem de <b>descobrir tarde</b> que "
        "o escopo cresceu ou o prazo slipou. Monitorar e comparar "
        "<b>continuamente</b> o planejado x realizado e corrigir cedo.")
)

cad.section("stakeholders", "Partes interessadas e a matriz poder/interesse",
    p("Stakeholder (ou parte interessada) e <b>qualquer pessoa ou grupo "
      "afetado pelo projeto ou que possa afetá-lo</b>. Voce mapeia quem tem "
      "<b>poder</b> (decide) e <b>interesse</b> (se importa) para saber como "
      "comunicar com cada um.") +
    tbl(["Quadrante", "Perfil", "Como voce gerencia"],
        [["Alto poder / Alto interesse", "Parceiro próximo", "Gerencie de perto, envolvido"],
         ["<b>Alto poder / Baixo interesse</b>", "Sponsor / chefe", "<b>Mantenha satisfeito</b> (com relato curto)"],
         ["<b>Baixo poder / Alto interesse</b>", "Quem executa / usa", "<b>Mantenha informado</b> (formacao, demos)"],
         ["Baixo poder / Baixo interesse", "Marginal", "Monitore com atencao minima"]],
        num_cols=[]) +
    aplicab(
        "<b>Quando</b> voce propor automatizar a etapa de triagem.",
        "<b>Por que</b> o chefe do intermedio (alto poder, interesse eventual) "
        "precisa de um relato curto de impacto; os triadores (baixo poder, alto "
        "interesse) precisam de treinamento e de Participate da desenho.",
        "<b>Exemplo</b> na POLITEC: sponsor = Diretor Tecnico (satisfacao com "
        "numero de TAT); equipe = triadores do ATO (formacao no novo sistema)."
    ) +
    callout("err", "Stakeholder esquecido",
        "O stakeholder mais facilmente esquecido e o <b>usuario final</b> - "
        "aquele que vai usar o processo todos os dias. Um processo redesenhado "
        "sem o usuario no desenho e rejeitado na operacao.")
)

cad.section("gestao-de-risco", "Risco de projeto: identificar, medir, tratar",
    p("Risco e um <b>evento incerto</b> que, se ocorrer, afeta o projeto. O "
      "gestor de projeto <b>identifica</b>, <b>avalia</b> (probabilidade x "
      "impacto) e <b>trata</b> (evitar, reduzir, transferir ou aceitar).") +
    tbl(["Probabilidade x Impacto", "Zona", "Acao"],
        [["Alta x Alto", "<b>Vermelho (crítico)</b>", "Mitigar agora, plano de contingencia"],
         ["Alta x Baixo", "Amarelo", "Reduzir, monitorar"],
         ["Baixa x Alto", "Amarelo", "Plano de resposta pronto"],
         ["Baixa x Baixo", "Verde", "Aceitar e monitorar"]],
        num_cols=[]) +
    aplicab(
        "<b>Quando</b> o projeto de automacao da triagem comeca.",
        "<b>Por que</b> dois riscos dominam esta etapa: (1) o SIGT nao tem API para "
        "integrar (Alto x Alto); (2) os triadores resistem a mudanca (Media x Alto).",
        "<b>Exemplo</b> na POLITEC: mitigacao do risco 1 = come�ar com "
        "exportacao CSV (workaround) e integrar depois; risco 2 = envolver os "
        "triadores no desenho e treinar."
    ) +
    callout("purple", "Risco nao e o mesmo que problema",
        "<b>Risco</b> e algo que <b>pode</b> acontecer (futuro, incerto). "
        "<b>Problema</b> ja aconteceu (presente). Um risco alto vira um "
        "problema se voce nao o trata.")
)

cad.section("indicadores-projeto", "Como saber se o projeto esta saudavel (indicadores)",
    p("Um projeto sem indicador e um projeto as cegas. Os indicadores mais "
      "usados na gestao publica sao os da <b>Prazo e Custo</b> "
      "(EVM, Earned Value Management), mas na POLITEC vale tambem o "
      "<b>TAT do processo</b> que voce vai medir hoje.") +
    tbl(["Indicador", "Formula", "O que diz"],
        [["SPI (Indice de Performance de Prazo)", "Valor ganho / Valor planejado", "Estou atrasando?"],
         ["CPI (Indice de Performance de Custo)", "Custo real / Valor ganho", "Estou gastando mais?"],
         ["Atraso medio", "Prazo real - prazo planejado", "Quanto tempo perdemos"],
         ["TAT do processo", "Soma de espera + execucao", "Quanto tempo leva o fluxo"]],
        num_cols=[]) +
    callout("note", "SPI e CPI juntos",
        "SPI &lt; 1 = atrasado; CPI &gt; 1 = gastando mais que o previsto "
        "(planejando folga). Na pratica da POLITEC, um <b>TAT com tendencia de "
        "alta</b> e o sinal mais claro de que o projeto precisa de atuacao.")
)

# =================================================================
# PARTE 2 - BPMN E MERMAID
# =================================================================
cad.grp("Parte 2 - BPMN e Mermaid",
        "A linguagem padrao para modelar processos (BPMN 2.0) e a ferramenta para desenhar diagramas como codigo (Mermaid).")

cad.section("por-que-modelar", "Por que modelar um processo antes de mudar",
    p("Modelar (desenhar) um processo nao e burocracia: e o unico jeito de "
      "<b>ver o processo inteiro</b>, <b>encontrar o gargalo</b> e <b>comunicar "
      "a mudanca</b> sem ambiguidade. O desenho e o <b>contrato</b> entre as "
      "pessoas que vao mudar o processo.") +
    ul([
        "<b>Evidencia o desperdicio</b>: quando voce desenha, ve as etapas que nao agregam valor.",
        "<b>Revela gargalos</b>: o no de espera salta aos olhos no desenho.",
        "<b>Facilita a conversa</b>: um desenho vale mais que dez paginas de texto.",
        "<b>Versiona</b>: da para comparar AS-IS e TO-BE lado a lado e medir o ganho.",
    ]) +
    antesdepois(
        "&quot;O processo do laboratorio demora demais, alguem tem que "
        "acelerar.&quot; - opiniao, sem dado, sem solucao.",
        "Um desenho com o no de espera destacado e o tempo ao lado: "
        "&quot;a espera na fila do perito e 44 h; se ela cair para 8 h, o TAT cai 30%&quot;.",
        errado="Opinião",
        certo="Evidência"
    ) +
    callout("tip", "Regra de ouro",
        "<b>Se nao esta desenhado, nao esta gerenciado.</b> O desenho AS-IS e "
        "a linha de base (baseline) contra a qual voce mede o TO-BE.")
)

cad.section("o-que-e-bpmn", "O que e BPMN (Business Process Modeling Notation)",
    p("<b>BPMN 2.0</b> e a <b>notacao padrao internacional</b> para modelar "
      "processos de negocio. Nascida da OMG, e lida por ferramentas de automacao "
      "(Camunda, Bizagi, Power Automate) e usada em todo o mundo. O diferencial "
      "do BPMN e que ele descreve <b>o que</b> acontece <b>e quem</b> faz, "
      "com notacao grafica padronizada.") +
    tbl(["Caracteristica", "BPMN 2.0"],
        [["Padrao", "OMG (Object Management Group), ISO 19510"],
         ["Foco", "Processos de negocio (o que e como)"],
         ["Granularidade", "Fluxo (nao so o organograma)"],
         ["Elementos", "Eventos, atividades, gateways, swimlanes"],
         ["Uso", "Modelagem + alimentacao de ferramentas de automacao"]],
        num_cols=[]) +
    callout("purple", "BPMN e nao a linguagem do Mermaid",
        "<b>BPMN</b> e a <b>notacao</b> (o conjunto de simbolos e regras). "
        "<b>Mermaid</b> e uma <b>ferramenta</b> (voce escreve codigo e ele "
        "desenha). Os dois sao complementares: o Mermaid desenha bem o fluxo, "
        "mas nao substitui o rigor do BPMN. Nesta aula, vamos usar o Mermaid "
        "como forma rapida de <b>materializar</b> o desenho BPMN.")
)

cad.section("elementos-bpmn", "Os elementos do BPMN: eventos, atividades e gateways",
    p("Todo diagrama BPMN se combina com <b>tres familias</b> de elementos. "
      "E com eles que voce descreve qualquer processo. A galeria abaixo mostra "
      "os simbolos <b>na geometria oficial da OMG</b> - copie e use como "
      "referencia no seu processo.") +
    gallery() +
    tbl(["Elemento", "Simbolo", "Quando usar"],
        [["Inicio", "Circulo vazio", "O primeiro passo do processo"],
         ["Fim", "Circulo cheio", "Ultimo passo do processo"],
         ["Tarefa", "Retangulo", "Acao manual ou automatica"],
         ["Gateway exclusivo", "Losango com X", "Se A entao X senao Y (uma escolha)"],
         ["Gateway paralelo", "Losango com +", "Faz X e Y ao mesmo tempo (divergente)"],
         ["Gateway inclusivo", "Losango com O", "Pode fazer um, outro ou os dois"],
         ["Mensagem", "Seta tracejada", "Um ator passa algo para outro"],
         ["Timer", "Relogio", "Acontece em data/programado"],
         ["Fila (pool)", "Retangulo grande", "Um sistema / unidade separada"],
         ["Objeto de dados", "Retangulo com canto", "Documento que entra/sai"]],
        num_cols=[]) +
    callout("purple", "Leia o codigo do desenho",
        "Os simbolos estao desenhados com a geometria padronizada. Notacao "
        "importa: quando duas pessoas leem o mesmo diagrama, elas veem as "
        "mesmas coisas - e isso e o que permite automatizar depois.")
)

cad.section("gateways-detalhe", "Gateways: as tres portas de decisao",
    p("O <b>gateway</b> (losango) e onde o processo <b>decide</b>. Escolher o "
      "gateway certo e essencial para o diagrama nao mentir sobre o processo.") +
    gates_anatomy() +
    grid2([
        ("\u2715 Gateway exclusivo (X)",
         "<b>Exatamente uma</b> das rotas e escolhida. E o mais comum. "
         "Ex.: <i>&quot;O material biologico esta integro? Se sim, segue para "
         "a analise; se nao, segue para a guarda.&quot;</i>"),
        ("\u2715 Gateway paralelo (+)",
         "<b>Todas</b> as rotas saem juntas. Use para <b>dividir</b> trabalho "
         "em paralelo. Ex.: <i>&quot;envia ao laboratorio E notifica o "
         "delegado simultaneamente&quot;.</i>"),
        ("\u25ef Gateway inclusivo (O)",
         "<b>Uma, varias ou nenhuma</b> rota pode ser escolhida, conforme uma "
         "condicao mais complexa. E o mais flexivel (e o mais dificil de ler)."),
    ]) +
    callout("err", "Gateway mal usado",
        "Usar um gateway paralelo quando so um caminho ocorre <b>inventa uma "
        "paralelismo que nao existe</b> no processo real - e faz o TO-BE parecer "
        "melhor do que e. Se so uma rota ocorre, use o exclusivo.")
) 

cad.section("swimlanes", "Pools e swimlanes: quem faz o que",
    p("As <b>swimlanes</b> (faixas horizontais) separam o processo por <b>ator "
      "(quem executa)</b>: uma unidade, um cargo, um sistema. O fluxo do "
      "processo cruza as faixas, deixando visivel <b>onde o processo muda de "
      "mãos</b> - e isso e praticamente sempre onde esta o gargalo.") +
    tbl(["Elemento", "O que representa", "Exemplo POLITEC"],
        [["<b>Pool</b>", "Um sistema / organizacao separada", "SIGT (sistema), Papel (mundo fisico)"],
         ["<b>Lane</b>", "Um papel dentro do pool", "Triador, Perito, Chefe, Sistema"]],
        num_cols=[]) +
    swimlane_anatomy() +
    step([
        ("Liste os atores do processo",
         "Quem executa alguma coisa? No fluxo pericial: <b>Delegacia</b>, "
         "<b>ATO</b>, <b>Laboratorio</b>, <b>Sistema</b>."),
        ("Crie uma swimlane por ator",
         "Uma faixa horizontal por ator, na ordem em que o caso passa."),
        ("Coloque cada atividade na faixa de quem a executa",
         "A triagem vai na faixa do ATO; a analise, na do Laboratorio."),
        ("Marque as fronteiras",
         "Onde o fluxo <b>atravessa</b> duas faixas, existe uma espera "
         "potencial - sinalize com um comentario ou cor."),
    ]) +
    aplicab(
        "<b>Quando</b> voce quer prever onde o processo vai travar.",
        "<b>Por que</b> cada <b>transicao entre swimlanes</b> (uma mao passa "
        "o objeto para outra) e um ponto de espera potencial.",
        "<b>Exemplo</b> na POLITEC: <i>o fluxo do requisicao pericial cruza 4 "
        "swimlanes (Delegacia &rarr; ATO &rarr; Laboratorio &rarr; Sistema). "
        "Medindo a espera em cada fronteira, a fila do perito aparece como "
        "51% do tempo.</i>"
    ) +
    callout("purple", "Onde nasce o gargalo",
        "Cada <b>transicao entre swimlanes</b> (uma mao passa o objeto para "
        "outra) e um ponto de espera potencial. O gargalo quase sempre esta "
        "nessas fronteiras - por isso que medir <b>espera por etapa</b> (e nao "
        "so execucao) muda o diagnostico.")
)

cad.section("eventos-bpmn", "Eventos: o que dispara, espera ou detecta",
    p("Eventos BPMN sao os gatilhos e respostas do processo. Eles dao "
      "profundidade e sao essenciais para automatizacao.") +
    ul([
        "<b>Evento de inicio</b>: o que dispara o processo? (mensagem, timer, erro, sinal).",
        "<b>Evento intermediario</b>: o que acontece no meio e reage (ex.: <i>prazo legal vence</i>).",
        "<b>Evento de fim</b>: como o processo termina (normal, erro, cancelamento).",
        "<b>Evento de fronteira</b>: anexo a uma atividade - <i>se der erro na etapa, ...</i>.",
    ]) +
    callout("tip", "O evento de fronteira e o coracao da automacao",
        "&quot;Se o prazo vencer, <b>dispara alerta</b>&quot; e um evento de "
        "fronteira com timer. E assim que se constroi um alarme automatico no "
        "TO-BE.")
)

cad.section("mermaid-intro", "Mermaid: diagramas como codigo",
    p("<b>Mermaid</b> e uma linguagem de <b>texto para diagramas</b>. Voce "
      "escreve um diagrama em texto simples, dentro de qualquer bloco de "
      "texto (Markdown, este caderno, IDE, wiki) e o Mermaid renderiza o "
      "desenho. Como o diagrama <b>e texto</b>, ele entra no Git, versiona, "
      "revisa e <b>reaparece sozinho</b>.") +
    tbl(["Vantagem", "Explicacao"],
        [["Versionavel", "O diagrama esta no Git: muda, compara, volta atras"],
         ["Colaborativo", "Dois pessoas editam o mesmo texto do diagrama"],
         ["Barato de mudar", "Mover uma etapa = editar uma linha de texto"],
         ["Renderiza em qualquer lugar", "GitHub, GitLab, VS Code, Notion, este caderno"]],
        num_cols=[]) +
    step([
        ("Escreva o diagrama como texto",
         "Comece com <code>flowchart TD</code> e uma seta: <code>A[Req.] --&gt; B[Triagem]</code>."),
        ("Renderize no navegador",
         "Cole em <b>mermaid.live</b> (gratis, sem instalar nada) e veja o "
         "desenho aparecer."),
        ("Itere e limpe",
         "Adicione etapas, gateways e swimlanes. O texto cresce; o desenho "
         "acompanha."),
        ("Versione no repositorio",
         "Salve como <code>processo.mmd</code> no Git. O diagrama passa a ter "
         "historico."),
    ]) +
    callout("note", "Quando usar BPMN formal x Mermaid rapido",
        "<b>Mermaid</b> e perfeito para rascunho rapido, documentacao e "
        "diagramas que vivem junto do codigo. Para um projeto formal com "
        "ferramenta de BPMN, use uma ferramenta dedicada. Nesta aula, o Mermaid "
        "e o cavalete para desenhar o BPMN com velocidade.")
)

cad.section("mermaid-flowchart", "Mermaid 1: flowchart - o diagrama de fluxo",
    p("O <code>flowchart</code> e o tipo mais usado e o mais proximo do BPMN. "
      "Com ele voce desenha o fluxo completo de um processo.") +
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
    tbl(["Elemento", "Sintaxe", "Significado BPMN"],
        [["Nos", "`A[Retangulo]`", "Atividade (tarefa)"],
         ["Nos com borda dupla", "`A[[Subprocesso]]`", "Subprocesso"],
         ["Retangulo arredondado", "`A([Inicio])`", "Evento de inicio/fim"],
         ["Losango", "`C{Decisao?}`", "Gateway"],
         ["Seta simples", "`A --> B`", "Fluxo"],
         ["Seta rotulada", "`A -->|Sim| B`", "Fluxo com mensagem/condicao"],
         ["Caixa dupla", "`A[[Sub]]`", "Subprocesso"]],
        num_cols=[]) +
    callout("tip", "Direcao do fluxo",
        "<code>TD</code> = top-down (vertical, classico em BPMN); "
        "<code>LR</code> = left-right (horizontal, melhor para processos "
        "longos). Comece com <code>TD</code>, mude para <code>LR</code> se o "
        "diagrama ficar comprido demais.")
)

cad.section("mermaid-subgraphs", "Mermaid 2: subgraph - as swimlanes",
    p("O <code>subgraph</code> do Mermaid reproduz as <b>swimlanes</b> do "
      "BPMN: cada bloco e um ator (unidade, papel ou sistema), e o fluxo cruza "
      "os blocos.") +
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
    callout("purple", "A regra de ouro do subgraph",
        "Um processo so e bem modelado quando <b>cada atividade esta dentro de "
        "uma swimlane</b>. Se uma tarefa esta &quot;na swimlane errada&quot;, o "
        "diagrama esta errado. E a mesma disciplina do BPMN formal.")
)

cad.section("mermaid-sequence", "Mermaid 3: sequenceDiagram - quem fala com quem",
    p("O <code>sequenceDiagram</code> mostra o fluxo <b>no tempo</b>, com os "
      "atores trocando mensagens. E ideal para processos com <b>integracao "
      "entre sistemas</b> ou <b>comunicacao com terceiros</b>.") +
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
        [["`->>`", "Mensagem sincrona (chamada)"],
         ["`-->>`", "Retorno (resposta)"],
         ["`-)`", "Mensagem assincrona (fire-and-forget)"],
         ["`->>`", "Fluxo de dados / evento"]],
        num_cols=[]) +
    callout("tip", "flowchart x sequenceDiagram",
        "<b>flowchart</b> mostra <b>os passos</b> (o que acontece). "
        "<b>sequenceDiagram</b> mostra <b>as mensagens</b> (quem fala com quem "
        "e quando). Para automatizacao (integrar sistemas), o sequenceDiagram "
        "e mais util.")
)

cad.section("mermaid-state", "Mermaid 4: stateDiagram - o ciclo de vida",
    p("O <code>stateDiagram-v2</code> mostra os <b>estados</b> que um objeto "
      "(uma requisicao, uma evidencia, um projeto) assume ao longo do tempo. "
      "E a visao natural para o aluno que ja estudou o ciclo de vida no Dia 1.") +
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
    callout("note", "Estado x etapa",
        "Um <b>estado</b> e uma condicao duradoura (a requisicao esta "
        "&quot;em analise&quot;); uma <b>etapa</b> e um passo (o perito "
        "&quot;recolheu a amostra&quot;). O stateDiagram foca no <b>primeiro</b>, "
        "o flowchart no <b>segundo</b>. Nos dois, o gargalo e o estado mais "
        "longo em que o objeto fica parado.")
)

cad.section("mermaid-outros", "Mermaid 5: gantt, journey, mindmap e C4",
    p("O Mermaid tem outros tipos uteis para um gestor de projeto:") +
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
    tbl(["Tipo", "Para que serve", "Exemplo POLITEC"],
        [["<code>gantt</code>", "Cronograma do projeto", "Prazo das fases de uma automacao"],
         ["<code>journey</code>", "Experiencia do usuario", "Como a vitrine e a delegacia vivenciam o processo"],
         ["<code>mindmap</code>", "Decomposicao do escopo", "Arvore do escopo (WBS)"],
         ["<code>C4</code>", "Arquitetura de software", "Como o app conversa com o SIGT"],
         ["<code>erDiagram</code>", "Modelo de dados", "Entidades do processo (requisicao, exame)"]],
        num_cols=[]) +
    callout("purple", "O diagrama de viagem (journey)",
        "O <code>journey</code> mapeia a <b>experiencia</b> do cidadao ou do "
        "servidor ao longo do processo. Ele revela o momento de <b>espera</b> "
        "na perspectiva de quem sofre a espera - o argumento mais forte para a "
        "automatizacao.")
)

# =================================================================
# PARTE 3 - DO TEXTO AO DIAGRAMA (METODO DAS 7 PERGUNTAS)
# =================================================================
cad.grp("Parte 3 - Do Texto ao Diagrama",
        "O metodo que converte uma descricao em linguagem natural em um diagrama BPMN, automaticamente.")

cad.section("por-que-automatizar-o-desenho", "Por que nao desenhar a mao",
    p("Desenhar um diagrama de processo a mao e lento, dificil de manter e "
      "impossivel de versionar. O desenho <b>como texto</b> (Mermaid) muda a "
      "equacao: voce escreve o processo em <b>minutos</b>, versiona no Git, e "
      "qualquer pessoa com o texto consegue gerar o diagrama.") +
    grid2([
        ("\u2717 Desenho manual (Visio / Lucidchart)",
         ul(["Lento para montar e lento para mudar",
             "Varias pessoas nao editam o mesmo arquivo",
             "Sem historico de mudancas",
             "Se perde em PDF ou PNG solto"])),
        ("\u2713 Diagrama como texto (Mermaid)",
         ul(["Minutos para escrever, segundos para gerar",
             "Editavel por qualquer pessoa com texto",
             "Versionado no Git, com diff claro",
             "Renderiza em GitHub, wiki, IDE e aqui"]))
    ]) +
    callout("tip", "O desenho deixa de ser documento e vira codigo",
        "Um diagrama Mermaid <b>é um arquivo de texto</b>. Ele entra no mesmo "
        "controle de versao do codigo: quem mudou o processo mudou o diagrama, "
        "e o historico conta a historia da mudanca.")
)

cad.section("metodo-7-perguntas", "O metodo das 7 perguntas: de texto para diagrama",
    p("Para transformar qualquer descricao em processo num diagrama, faca "
      "estas <b>7 perguntas</b>, sempre na mesma ordem. A ordem importa: cada "
      "pergunta so faz sentido depois da anterior.") +
    tbl(["#", "Pergunta", "Vira no diagrama..."],
        [["<b>1</b>", "<b>Quem/que dispara?</b> O que inicia o processo?", "Evento de inicio"],
         ["<b>2</b>", "<b>Onde comeca?</b> Qual a primeira atividade?", "Primeira tarefa"],
         ["<b>3</b>", "<b>O que acontece em seguida?</b> (repita)", "Cadeia de tarefas"],
         ["<b>4</b>", "<b>Ha decisao?</b> (condicao se/senao)", "Gateway"],
         ["<b>5</b>", "<b>Quem faz cada etapa?</b> (unidade/papel)", "Swimlanes"],
         ["<b>6</b>", "<b>O que entra e sai?</b> (documentos)", "Objetos de dados / mensagens"],
         ["<b>7</b>", "<b>Como termina?</b> (sucesso? erro? cancela?)", "Evento(s) de fim"]],
        num_cols=[]) +
    callout("g", "Por que a ordem importa",
        "A pergunta 5 (quem faz) so faz sentido depois de saber <b>quais</b> "
        "atividades existem (perguntas 2-4). E a 7 (fim) so depois de mapear o "
        "caminho. Pular direto para o desenho leva a diagramas errados - com tarefa "
        "na swimlane errada ou sem o fim.")
)

cad.section("exemplo-pratico", "Exemplo pratico: do texto ao diagrama",
    p("Voce ouve de um perito a descricao do fluxo. Ela vira o diagrama "
      "seguinte usando so as 7 perguntas:") +
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
    tbl(["Pergunta", "Resposta", "Onde esta no diagrama"],
        [["1. Quem dispara?", "A delegacia recebe a requisicao", "Evento de inicio A"],
         ["2. Onde comeca?", "Registrar no SIGT", "Tarefa B"],
         ["3. O que depois?", "Triagem, fila, analise", "C, E, F"],
         ["4. Ha decisao?", "Dados completos? Passa a revisao?", "Gateways D e G"],
         ["5. Quem faz?", "Delegacia, ATO, Laboratorio", "3 swimlanes"],
         ["6. O que entra/sai?", "Protocolo, laudo", "Nos de borda"],
         ["7. Como termina?", "Laudo emitido", "Evento de fim J"]],
        num_cols=[])
)

cad.section("heuristicas-diagrama", "Heuristicas: como fazer um diagrama legivel",
    p("Um diagrama bom se lê em segundos. Estas heuristicas seguem a boa "
      "pratica de BPMN e melhoram a leitura do seu processo.") +
    ul([
        "<b>Fluxo de cima para baixo (TD)</b>, exceto processos longos (use LR).",
        "<b>Um swimlane por ator</b>, sem atividades fora de nenhuma.",
        "<b>Poucos elementos por pagina</b> - se nao cabe, quebre em sub-processos.",
        "<b>Rotule as setas com a condicao</b> (&quot;Sim&quot;/&quot;Nao&quot;).",
        "<b>Evite linhas cruzadas</b> - se cruzam, reveja o layout ou quebre.",
        "<b>Nomeie as atividades com verbo</b> (&quot;Registrar&quot;, nao &quot;Registro&quot;).",
        "<b>Destaque o gargalo</b> com cor ou nota (voce vera isso na Parte 4).",
    ]) +
    callout("err", "O diagrama spaghetti",
        "Um diagrama com 40 caixas e 60 setas cruzadas nao comunica - "
        "assustar. Se o processo nao cabe, ele tem <b>sub-processos</b>: "
        "quebre em caixas duplas ([[ ]]) e detalhe cada uma.")
)

cad.section("versionar-processo", "Versionar o processo: o diagrama como historico",
    p("Como o diagrama e texto, ele entra no <b>Git</b> como qualquer codigo. "
      "Isso cria um <b>historico do processo</b>: da para ver quando e como o "
      "fluxo mudou - e voltar atras se a mudacao foi ruim.") +
    ul([
        "<code>processos/requisicao-pericial.mmd</code> - o diagrama AS-IS versionado.",
        "<code>processos/requisicao-pericial-tobe.mmd</code> - a versao proposta.",
        "Commits descrevem mudancas: &quot;prioriza fila por prazo legal&quot;.",
        "Code review: o sponsor aprova a <b>mudanca do processo</b> via PR, igual a codigo.",
    ]) +
    callout("purple", "Da para medir o processo no tempo",
        "Se o diagrama AS-IS esta versionado, voce tem a <b>linha de base</b>. "
        "A cada trimestre, redesenhe o diagrama do processo real e compare com "
        "o TO-BE planejado: o processo real e o planejado, com prova.")
)

# =================================================================
# PARTE 4 - GARGALOS (COM DADOS)
# =================================================================
cad.grp("Parte 4 - Gargalos com Dados",
        "Onde o processo perde tempo e dinheiro - medindo, nao adivinhando.")

cad.section("espera-vs-execucao", "A descoberta que muda tudo: espera x execucao",
    p("Todo processo tem dois tipos de tempo: o tempo em que alguem "
      "<b>trabalha</b> e o tempo em que o caso fica <b>parado esperando</b>. "
      "Quase sempre, o processo e dominado pela <b>espera</b> - e o gargalo "
      "quase sempre esta na espera, nao no trabalho.") +
    tbl(["Tipo de tempo", "O que e", "Exemplo"],
        [["<b>Tempo de execucao</b> (touch time)", "Minutos que alguem <b>trabalha</b>", "O perito analisa a amostra"],
         ["<b>Tempo de espera</b> (wait time)", "Tempo <b>parado</b> na fila", "O exame espera o perito"]],
        num_cols=[]) +
    callout("g", "O achado dos 3 datasets da aula",
        "Nos tres processos da POLITEC, a <b>espera e 88-92% do tempo total</b>. "
        "Ou seja: quase todo o problema nao e as pessoas trabalharem devagar - e "
        "os casos ficarem <b>parados na fila</b>. Medir execucao sem medir "
        "espera e olhar a coisa errada.") +
    wait_vs_touch(92)
) 

cad.section("diagrama-espera", "Diagrama: onde o processo vira um funil de espera",
    p("O diagrama mais revelador de um processo e o <b>diagrama de esperas por "
      "etapa</b>: cada etapa com o tempo parado nela. A etapa mais alta e o "
      "gargalo.") +
    bar_chart(
        ["Fila perito", "Revisao", "Distribuicao", "Triagem", "Assinatura", "Analise", "Arquivamento"],
        [57175, 16888, 16360, 13480, 13380, 12860, 7000],
        "Cenario 1 - Tempo de espera por etapa (horas, soma de todo o periodo)",
        "A etapa 'Fila perito' concentra 41,5% de toda a espera do processo. "
        "Gargalo medido no dataset cenario1_processo_pericial.",
        destaque=0
    ) +
    tbl(["Etapa", "Espera (h)", "% da espera", "Leitura"],
        [["<b>Fila perito</b>", "57.175", "<b>41,5%</b>", "<b>GARGALO</b> - caso parado ate ser atendido"],
         ["Revisao", "16.888", "12,3%", "Fila do revisor"],
         ["Distribuicao", "16.360", "11,9%", "Handoff entre setores"],
         ["Triagem", "13.480", "9,8%", "Fila do ATO"],
         ["Assinatura", "13.380", "9,7%", "Assinatura e release"],
         ["Analise", "12.860", "9,3%", "Fila do perito antes de comecar"],
         ["Arquivamento", "7.000", "5,1%", "Envio e arquivo"]],
        num_cols=[1, 2]) +
    callout("purple", "Leia o gargalo certo",
        "A etapa 5 &quot;Analise&quot; tem o MAIOR tempo de <b>execucao</b> (o "
        "trabalho do perito), mas a etapa 4 &quot;Fila perito&quot; tem o maior "
        "tempo de <b>espera</b>. O gargalo a atacar e a <b>fila</b>: por mais "
        "rapido o perito trabalhe, o caso continua parado esperando.")
)

cad.section("pareto-gargalos", "Pareto dos gargalos: a regra dos 20/80 do processo",
    p("A analise de Pareto ordena as etapas por tempo e mostra que poucas "
      "etapas concentram a maior parte do desperdicio. E o <b>principio de "
      "Pareto</b> aplicado a processos.") +
    bar_chart(
        ["Fila perito", "Revisao", "Distribuicao", "Triagem", "Assinatura"],
        [41.5, 12.3, 11.9, 9.8, 9.7],
        "Pareto da espera - % do tempo de espera por etapa",
        "As 2 primeiras etapas (Fila + Revisao) somam 53,8% de toda a espera. "
        "Atacar so essas duas ja resolve mais da metade do problema.",
        fmt="{:.1f}%",
        destaque=0
    ) +
    tbl(["Conceito", "Aplicacao em processo"],
        [["Princípio de Pareto (80/20)", "20% das etapas = 80% do tempo"],
         ["Pareto de espera", "Onde o processo mais para"],
         ["Pareto de retrabalho", "Onde mais se erra"],
         ["Pareto de custo", "Onde o dinheiro mais se perde"]],
        num_cols=[]) +
    callout("tip", "Comece pelo topo",
        "Se voce so puder atacar <b>uma</b> etapa, ataque a primeira do Pareto. "
        "Se puder duas, ataque as duas primeiras. Isso maximiza o ganho por "
        "unidade de esforco.")
)

cad.section("retrabalho", "Retrabalho: o desperdicio invisivel",
    p("<b>Retrabalho</b> e refazer uma etapa ja feita, por erro ou devolucao. "
      "Nao aparece no tempo de espera - e por isso passa despercebido. No "
      "nosso caso, um exame que volta da revisao para nova analise refaz todo "
      "o trabalho do perito.") +
    bar_chart(
        ["Pericial", "Orcamento", "Custodia"],
        [11.6, 16.6, 4.7],
        "Taxa media de retrabalho por cenario",
        "O processo orcamentario tem o maior retrabalho (~16,6%) - mapeamento e "
        "parecer sao refeitos com frequencia. Medido nos datasets da Aula 6.",
        fmt="{:.1f}%",
        destaque=1
    ) +
    step([
        ("Mapeie o caminho de retorno no diagrama",
         "Toda seta de volta (correcao, devolucao) precisa estar no AS-IS."),
        ("Meça o retrabalho nos dados",
         "Controle a coluna <code>flag_retrabalho</code> no <code>fato_execucao</code> "
         "e calcule o percentual por etapa."),
        ("Ordene por taxa, nao por volume",
         "Um processo com 5% de retrabalho em 15.000 casos custa mais que "
         "15% em 200 casos."),
        ("Ataca a causa, nao o sintoma",
         "Retrabalho alto na etapa 3 (mapa) = problema no checklist ou na "
         "planilha, nao noesse mapeamento."),
    ]) +
    tbl(["Retrabalho tipico", "Causa raiz", "Intervencao"],
        [["Exame volta da revisao", "Falta de checklist do perito", "Checklist padronizado (TO-BE)"],
         ["Mapa comparativo refeito", "Falta de criterio de aceitacao", "Alerta de dotacao + regra clara"],
         ["Pedido devolvido", "Formulario incompleto", "Formulario digital com validacao"],
         ["Evidencia com divergencia", "Lacre em papel", "QR Code digital"]],
        num_cols=[]) +
    callout("err", "Retrabalho invisivel no diagrama",
        "Se o diagrama AS-IS nao mostra o caminho de volta (a <b>correcao</b>), "
        "voce subestima o tempo real. Sempre inclua o fluxo de retorno/correcao "
        "no diagrama - e meca o retrabalho nos dados.")
)

cad.section("littles-law", "Little's Law: quanto de fila o processo suporta",
    p("<b>Little's Law</b> (John Little) e a relacao mais util de operacoes: "
      "<b><code>L = λ × W</code></b> — o numero de itens no sistema (L) e a "
      "taxa de chegada (λ) vezes o tempo de permanencia (W). Ela permite "
      "calcular o tamanho da fila a partir da demanda e do tempo.") +
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
    tbl(["Se voce quer...", "Voce precisa..."],
        [["Reduzir a fila (L)", "Reduzir W (tempo) ou λ (chegada)"],
         ["Absorver mais demanda", "Aumentar a capacidade (W sobe)"],
         ["Reduzir o backlog", "Reduzir W <b>ou</b> aumentar λ (capacidade)"]],
        num_cols=[]) +
    callout("purple", "Little's Law no seu TO-BE",
        "Use Little's Law para <b>prever</b> o efeito da automacao: se o TO-BE "
        "corta a espera da fila de 44 h para 8 h, o W cai e o L (fila) cai "
        "proporcionalmente. Voce justifica o investimento com numero, nao com "
        "opinião.")
)

cad.section("custo-espera", "Custo da espera: quando tempo vira dinheiro",
    p("O custo do processo e o <b>custo da execucao</b> (tempo de trabalho x "
      "custo/hora) mais o <b>custo da espera</b> (atraso, multa, retrabalho, "
      "insatisfacao). Nos datasets, a coluna <code>custo_minuto</code> permite "
      "calcular o custo direto da execucao.") +
    tbl(["Componente de custo", "Como aparece no processo POLITEC"],
        [["Mao de obra", "Horas do perito/tecnico na execucao"],
         ["Atraso (TAT)", "Caso urgente que vence o prazo"],
         ["Retrabalho", "Refazer etapa por erro"],
         ["Perda de validade", "Amostra que se degrada na fila"],
         ["Insatisfacao", "Cidadao que demora laudo"]],
        num_cols=[]) +
    callout("tip", "Transforme espera em R$",
        "Ao apresentar o TO-BE, converta a espera economizada em dinheiro: "
        "<b>(espera_antes - espera_depois) × volume anual × custo/unit</b>. "
        "E o numero que convence o orcamento.")
)

# =================================================================
# PARTE 5 - TO-BE E INTERVENCAO DIGITAL
# =================================================================
cad.grp("Parte 5 - TO-BE e Intervencao Digital",
        "Redesenhe o processo sobre o gargalo medido e resolva com automacao.")

cad.section("o-que-e-tobe", "TO-BE: o processo futuro (e como nao ser utopico)",
    p("O <b>TO-BE</b> (to be, &quot;como sera&quot;) e o desenho do processo "
      "depois da intervencao. O erro classico e fazer um TO-BE <b>utopico</b> "
      "— um mundo sem fila, sem espera, tudo automatico — que ninguem acredita "
      "e ninguem implementa.") +
    antesdepois(
        "TO-BE utopico: &quot;um app resolve tudo, fila zero, laudo em 2 "
        "horas&quot; — sem dado, sem viabilidade, sem plano.",
        "TO-BE realista: &quot;reduzir a espera da fila de 44 h para 8 h com "
        "fila priorizada por prazo e painel de carga; meta: -82% na espera, "
        "validado nos dados&quot;.",
        errado="Utopia",
        certo="Viável"
    ) +
    callout("g", "A regra do TO-BE",
        "Cada mudanca no TO-BE precisa estar <b>ligada a um gargalo medido</b>. "
        "Se voce redesenha algo que nao era gargalo, esta gastando esforco sem "
        "retorno. E se nao consegue medir o ganho, provavelmente escolheu a "
        "mudar a coisa errada.")
)

cad.section("principios-tobe", "Os 5 principios de redesenho do processo",
    p("Reorganizar um processo nao e so automatizar. Os <b>5 principios</b> "
      "guiam o redesenho, nesta ordem de impacto.") +
    tbl(["#", "Principio", "O que faz", "Exemplo no backlog pericial"],
        [["1", "<b>Eliminar</b>", "Remover etapa que nao agrega valor", "Eliminar o dupla conferencia manual"],
         ["2", "<b>Simplificar</b>", "Reduzir passos, formulários, handoffs", "Um formulario em vez de 3"],
         ["3", "<b>Integrar</b>", "Unir etapas separadas por sistemas", "SIGT integrado ao laboratorio"],
         ["4", "<b>Automatizar</b>", "Maquina faz o que o humano faz", "Fila priorizada por prazo"],
         ["5", "<b>Padronizar</b>", "Uniformizar para facilitar", "Checklist identico em todas as delegacias"]],
        num_cols=[]) +
    callout("err", "Automatizar primeiro (o erro comum)",
        "Automatizar um processo ruim (AS-IS ruim automatizado) cria um "
        "processo ruim e <b>mais rapido</b> — voce gastou para tornar mais "
        "eficiente algo que deveria ter sido eliminado ou simplificado antes.")
)

cad.section("tobe-fila-priorizada", "Exemplo de TO-BE: a fila priorizada",
    p("O gargalo medido do Cenario 1 e a <b>fila do perito</b> (44 h de espera "
      "media, 41,5% de toda a espera). A intervencao preenche a fileira do "
      "gargalo: uma <b>fila priorizada por prazo legal</b>.") +
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
    tbl(["Mudanca no TO-BE", "Foco", "Efeito esperado"],
        [["Fila por ordem de chegada", "AS-IS", "Urgente espera junto de rotina"],
         ["<b>Fila por prazo legal</b>", "<b>TO-BE</b>", "<b>Urgente atendido primeiro</b>"],
         ["Triagem por tipo automatica", "TO-BE", "Menos espera na triagem"],
         ["Painel de carga em tempo real", "TO-BE", "Redistribui antes de acumular"],
         ["Sem dupla digitao", "TO-BE", "Menos retrabalho"]],
        num_cols=[])
)

cad.section("intervencao-digital", "Intervencao digital: o catalogo de ferramentas",
    p("A intervencao no processo pode ser de qualquer natureza digital. "
      "Ferramentas da Microsoft (que voce ja conhece desde o Dia 4) resolvem "
      "a maior parte.") +
    grid2([
        ("\U0001f504 Automatizar a regra",
         "<b>Power Automate</b>: se o prazo vencer, dispara alerta; se completo, "
         "avanca etapa; se urgente, sobe na fila."),
        ("\U0001f4f1 Digitalizar o registro",
         "<b>Power Apps / formulario</b>: substitui papel por registro digital "
         "com validacao e carimbo de tempo."),
        ("\U0001f517 Integrar sistemas",
         "<b>Conector / API</b>: SIGT &harr; laboratorio, sem redigitacao "
         "(elimina retrabalho)."),
        ("\U0001f4ca Visualizar para decidir",
         "<b>Power BI</b>: painel de carga e WIP, para decidir redistribuicao "
         "(Dia 5)."),
        ("\U0001f9ea Automatizar o calculo",
         "<b>Script / formula</b>: calculo automatico de SLA, prioridade, "
         "prioridade por prazo."),
        ("\U0001f4e1 Notificar",
         "<b>E-mail / Teams</b>: push de alerta em vez de &quot;esperar alguem "
         "notar&quot;.")
    ]) +
    step([
        ("1. Liste as intervencoes possiveis",
         "Para cada etapa do TO-BE: dá para <b>eliminar</b>, <b>automatizar</b>, "
         "<b>integrar</b> ou <b>visualizar</b>?"),
        ("2. Priorize por impacto no gargalo",
         "A intervencao que mais mexe no gargalo vai primeiro. Uma automacao "
         "de etapa que nao e gargalo e desperdicio."),
        ("3. Escolha a ferramenta",
         "Regra simples &rarr; Power Automate. Formulario &rarr; Power Apps. "
         "Indicador &rarr; Power BI. Regra complexa &rarr; script."),
        ("4. Defina o medidor de sucesso",
         "Qual numero do AS-IS vai mudar? (ex.: espera da fila 44 h &rarr; 8 h). "
         "Sem medidor, nao ha como provar o ganho."),
    ]) +
    tbl(["Intervencao", "Custo", "Prazo", "Risco"],
        [["Alerta automatico", "Baixo", "1-2 semanas", "Baixo"],
         ["Painel de carga (BI)", "Baixo", "2-4 semanas", "Baixo"],
         ["Formulario digital", "Medio", "4-8 semanas", "Medio (adocao)"],
         ["Fila priorizada (regra)", "Medio", "4-6 semanas", "Medio"],
         ["Integracao entre sistemas", "Alto", "3-6 meses", "Alto (dependencia)"],
         ["App com QR Code", "Alto", "3-6 meses", "Alto (campo)"]],
        num_cols=[]) +
    callout("tip", "Comece pelo alerta",
        "A primeira automacao de um processo quase sempre e um <b>alerta</b> "
        "(&quot;se prazo vencer, notificar&quot;). E barato de fazer, "
        "imediato de sentir e prepara o terreno para automacoes maiores.") +
    automation_anatomy()
)

cad.section("script-automacao", "Automatizar com script: um exemplo real",
    p("Nem toda automacao precisa de Power Automate. Para uma regra simples, "
      "um <b>script</b> (Python, Excel ou planilha) resolve. Exemplo: "
      "priorizar a fila por prazo legal.") +
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
    callout("note", "Regra antes do codigo",
        "Antes de automatizar, escreva a regra em <b>linguagem clara</b>: "
        "&quot;o exame com menor prazo legal vai primeiro&quot;. Se voce nao "
        "consegue escrever a regra, nao consegue automatizar. O codigo e so a "
        "traducao da regra.")
)

cad.section("calcular-o-ganho", "O calculo do ganho: como provar que valeu",
    p("Todo TO-BE precisa de uma conta que mostre o retorno. O ganho se mede "
      "comparando o <b>AS-IS medido</b> com o <b>TO-BE projetado</b>, usando os "
      "mesmos dados.") +
    tbl(["Ganho", "Formula", "Exemplo (Cenario 1)"],
        [["Espera reduzida", "espera_ASIS - espera_TOBE", "44 h &rarr; 8 h"],
         ["TAT reduzido", "TAT_ASIS - TAT_TOBE", "92 d &rarr; 70 d (-24%)"],
         ["Custo poupado", "minutos_poupados × custo/min", "R$ X/ano"],
         ["Capacidade liberada", "casos_atendidos a mais no mesmo tempo", "+N exames/ano"]],
        num_cols=[]) +
    callout("g", "A conta do ganho no Cenario 1",
        "Fila do perito: espera cai de 44 h para 8 h (-36 h por caso). Com "
        "1.200 casos/ano, sao ~43.200 h/ano de espera poupadas. A 78,40 por "
        "hora de producao util, isso equivale a <b>1 perito-equivalente</b> "
        "liberado para trabalho tecnico - sem contratar ninguem.")
)

cad.section("roadmap-tobe", "Como levar o TO-BE a vida (roadmap de implantacao)",
    p("Nao se implanta um TO-BE inteiro de uma vez. Use um <b>roadmap</b> em "
      "ondas, medindo o ganho de cada uma.") +
    tbl(["Onda", "Intervencao", "Ganho esperado", "Esforco"],
        [["<b>Onda 1 (0-3m)</b>", "Alertas de prazo + painel de carga (BI)", "Visibilidade, -10% espera", "Baixo"],
         ["<b>Onda 2 (3-6m)</b>", "Fila priorizada por prazo legal", "-30% na espera da fila", "Medio"],
         ["<b>Onda 3 (6-12m)</b>", "Triagem automatica + integracao SIGT", "-20% espera, -retrabalho", "Alto"],
         ["<b>Onda 4 (12m+)</b>", "Integracao ponta a ponta", "Redesenho completo", "Alto"]],
        num_cols=[]) +
    callout("purple", "Onda 1 e a mais barata e a de maior efeito",
        "Comece pelo alerta e pelo painel de carga: sao as intervencoes que "
        "custam pouco, implantam rapido e <b>mostram o problema em tempo real</b> "
        "- preparando o terreno (e o argumento) para as ondas seguintes.")
)

# =================================================================
# PARTE 6 - PRATICA GUIADA (7 LABS)
# =================================================================
cad.grp("Parte 6 - Pratica Guiada",
        "Sete labs do zero ao diagrama publicado, com os datasets de processo medidos.")

cad.section("labs-intro", "Os 7 labs desta aula",
    p("Cada lab aplica uma etapa do metodo. Ao final do Lab 6 voce tem um "
      "<b>processo redesenhado com prova de ganho</b> - o entregavel da aula.") +
    tbl(["Lab", "O que voce faz", "Ferramenta", "Tempo"],
        [["<b>1</b>", "Descrever o processo em texto (7 perguntas)", "Papel e caneta", "20 min"],
         ["<b>2</b>", "Converter o texto em diagrama AS-IS", "Mermaid", "30 min"],
         ["<b>3</b>", "Medir o gargalo nos dados", "CSV + Excel/Power BI", "40 min"],
         ["<b>4</b>", "Validar o gargalo com quem trabalha no processo", "Entrevista", "30 min"],
         ["<b>5</b>", "Desenhar o TO-BE com intervencao", "Mermaid", "40 min"],
         ["<b>6</b>", "Calcular o ganho (antes x depois)", "Planilha", "30 min"],
         ["<b>7</b>", "Apresentar e coletar feedback", "Apresentacao", "20 min"]],
        num_cols=[]) +
    callout("tip", "Qual processo usar",
        "Escolha um processo em que voce <b>trabalha ou conhece</b>. Os tres "
        "datasets servem como treino, mas o projeto final fica melhor se for "
        "de uma area real - voce tem acesso as pessoas e aos dados.")
)

cad.section("lab1-descrever", "Lab 1 - Descrever o processo em texto",
    p("O primeiro passo e <b>escrever</b> - antes de qualquer desenho. Use as "
      "7 perguntas como roteiro de entrevista.") +
    step([
        ("Defina o escopo do processo",
         "<b>Onde começa e onde termina?</b> &quot;Do recebimento da requisicao "
         "na delegacia ate a assinatura do laudo&quot;. Delimite bem: se "
         "incluir demais, o diagrama fica gigante."),
        ("Aplique as 7 perguntas",
         "Quem dispara? Onde comeca? O que depois? Ha decisao? Quem faz? O que "
         "entra/sai? Como termina?"),
        ("Anote os tempos, se souber",
         "Quanto tempo cada etapa leva? Quanto tempo o caso <b>fica parado</b> "
         "em cada etapa? Pergunte: &quot;meio dia? uma semana?&quot;"),
        ("Identifique as dorpos",
         "Onde as pessoas reclamam? Onde atrasa? O queEveryone repete? Anote "
         "com as palavras delas."),
        ("Escreva um paragrafo",
         "Todo o AS-IS num texto corrido de 10-15 linhas. Esse texto e a "
         "<b>fonte</b> do diagrama.")
    ]) +
    ficha("g", "Dica de ouro",
        "Grave a entrevista. Quem sofre o processo tem detalhes que ninguem "
        "sabe - e sao eles que revelam o gargalo real.")
)

cad.section("lab2-diagrama-asis", "Lab 2 - Converter o texto em diagrama AS-IS (Mermaid)",
    p("Agora transformamos o paragrafo em diagrama. O objetivo nao e "
      "perfeito: e <b>completo e honesto</b>.") +
    step([
        ("Defina as swimlanes",
         "Quantos atores existem? No fluxo pericial: <b>Delegacia</b>, <b>ATO</b> "
         "(triagem), <b>Laboratorio</b> (perito/revisao), <b>Sistema</b> (SIGT)."),
        ("Coloque cada atividade na swimlane certa",
         "Se uma atividade nao cabe em nenhuma, crie a swimlane que falta "
         "(revelador: processo mal definido)."),
        ("Insira os gateways de decisao",
         "Cada &quot;se / senao&quot; do texto vira um losango. Rotule as setas "
         "com a condicao (<code>|Sim|</code>, <code>|Nao|</code>)."),
        ("Feche o diagrama",
         "Todo fluxo precisa de <b>inicio</b> e <b>fim</b> explicitos. Se sobrar "
         "caminho sem fim, ha etapa faltando."),
        ("Renderize e revise",
         "Cole o texto em <b>mermaid.live</b> (gratis, no navegador) ou no "
         "GitHub. Leia de cima para baixo: a historia faz sentido?"),
    ]) +
    callout("err", "O diagrama que ninguem le",
        "Se o diagrama tem 40 caixas, ele e um desenho de parede. Quebre em "
        "sub-processos (caixas duplas <code>[[ ]]</code>) e detalhe cada um. "
        "Um diagrama legivel cabe em uma tela.")
)

cad.section("lab3-medir-gargalo", "Lab 3 - Medir o gargalo nos dados",
    p("Aqui o processo deixa de ser opiniao. Va para a pasta "
      "<code>datasets/</code>, escolha um cenario e meca.") +
    step([
        ("Abra o <code>fato_execucao.csv</code> do cenario",
         "Ele tem uma linha por execucao de etapa, com <code>tempo_espera_min</code> "
         "e <code>tempo_execucao_min</code> separados."),
        ("Faca uma tabela dinamica",
         "Linhas: <code>etapa_key</code>. Valores: <b>SOMA de "
         "tempo_espera_min</b>. Ordene do maior para o menor."),
        ("Calcule o share de cada etapa",
         "<code>share = espera_da_etapa / espera_total</code>. A primeira "
         "etapa do ranking e o gargalo."),
        ("Compare espera x execucao",
         "Monte duas colunas: soma de espera e soma de execucao, por etapa. "
         "A etapa que domina a espera e o gargalo - mesmo que tenha pouca execucao."),
        ("Mapeie de volta ao diagrama",
         "Volte ao AS-IS e <b>destaque visualmente</b> a etapa medida como "
         "gargalo. O diagrama agora tem um alvo."),
    ]) +
    code(
        "-- Media de espera e execucao por etapa (SQL)\n"
        "SELECT e.etapa,\n"
        "       SUM(x.tempo_espera_min)/60    AS espera_h,\n"
        "       SUM(x.tempo_execucao_min)/60   AS execucao_h,\n"
        "       SUM(x.tempo_espera_min)\n"
        "         / SUM(SUM(x.tempo_espera_min)) OVER () AS share_espera\n"
        "FROM fato_execucao x\n"
        "JOIN dim_etapa e ON x.etapa_key = e.etapa_key\n"
        "GROUP BY e.etapa\n"
        "ORDER BY espera_h DESC;",
        "sql"
    ) +
    callout("g", "O resultado do Lab 3",
        "No Cenario 1, a etapa <b>Fila perito</b> tem 44 h de espera media e "
        "concentra <b>41,5%</b> de toda a espera do processo. A analise tem "
        "mais execucao, mas so 9,3% da espera. O gargalo e a fila, e voce "
        "acabou de provar com numero.")
)

cad.section("lab4-validar", "Lab 4 - Validar o gargalo com quem trabalha no processo",
    p("Dados mostram <b>onde</b>; as pessoas explicam <b>por que</b>. Esta "
      "etapa evita o erro classico de otimizar o lugar errado.") +
    step([
        ("Liste as hipoteses",
         "&quot;Se a fila do perito e o gargalo, por que o caso espera ali?&quot;"),
        ("Converse com quem atua na etapa",
         "Pergunte: &quot;quando o caso chega, o que trava? falta equipamento? "
         "falta perito habilitado?&quot;"),
        ("Cheque as causas raiz",
         "Sao as 5 porquês: por que espera? por que nao há perito? por que nao "
         "treinam mais peritos? etc."),
        ("Confirme o gargalo",
         "Se as pessoas confirmam a espera, seu TO-BE esta no caminho "
         "certo. Se nao, volte ao diagrama e reavalie."),
    ]) +
    tbl(["Pergunta para quem executa", "O que voce aprende"],
        [["&quot;Onde o caso mais para?&quot;", "Confirma ou refuta o gargalo medido"],
         ["&quot;O que trava mais?&quot;", "Causa raiz (falta recurso, processo, sistema)"],
         ["&quot;Se pudesse mudar UMA coisa?&quot;", "Prioridade real do time"],
         ["&quot;Ja tentaram resolver? Por que nao deu?&quot;", "Solucoes anteriores eporque falharam"]],
        num_cols=[]) +
    callout("purple", "Escute o &quot;ja tentaram&quot;",
        "Se o processo ja foi tentado e fracassou, pergunte <b>por que</b>. "
        "Normalmente a causa e cultural (ninguem muda o habito) ou de sistema "
        "(a ferramenta nao suporta) - e isso muda a solucao: nem sempre e "
        "automacao, as vezes e treinamento ou mudanca de regra.")
)

cad.section("lab5-tobe", "Lab 5 - Desenhar o TO-BE com intervencao digital",
    p("Com o gargalo medido e validado, redesenhe o processo. Cada mudanca "
      "precisa estar ligada ao gargalo.") +
    step([
        ("Copie o AS-IS e mude o nome",
         "<code>processo-asis.mmd</code> &rarr; <code>processo-tobe.mmd</code>. "
         "O TO-BE nasce do AS-IS."),
        ("Aplique os 5 principios na ordem",
         "<b>Eliminar</b> o que nao agrega valor &rarr; <b>Simplificar</b> "
         "(menos passos) &rarr; <b>Integrar</b> (menos handoffs) &rarr; "
         "<b>Automatizar</b> a regra &rarr; <b>Padronizar</b>."),
        ("Marque a intervencao no diagrama",
         "Use um estilo diferente para o que e automatico, e rotule a regra "
         "(<code>classDef auto</code> no Mermaid)."),
        ("Nao se perca no detalhe",
         "O TO-BE e um <b>direcional</b>, nao um contrato. Deixe os detalhes "
         "para a especificacao."),
    ]) +
    code(
        "flowchart TD\n"
        "    A([Req. recebida]) --> B[SIGT registra com prazo legal]\n"
        "    B --> C[Triagem automatica por tipo]\n"
        "    C --> D{Dados completos?}\n"
        "    D -->|Nao| E[Notificar digitar dados faltantes]\n"
        "    E --> B\n"
        "    D -->|Sim| F[Fila priorizada por prazo]\n"
        "    F --> G[Analise]\n"
        "    G --> H[Revisao]\n"
        "    H --> I([Laudo])\n"
        "    style F fill:#d4edda,stroke:#28a745\n"
        "    style C fill:#d4edda,stroke:#28a745\n"
        "    %% verde = intervencao digital do TO-BE",
        "mermaid"
    ) +
    callout("tip", "Destaque a intervencao no diagrama",
        "No Mermaid, use <code>style NO fill:#d4edda</code> para pintar de "
        "verde o que mudou. Quem le o TO-BE ve <b>onde</b> a automacao "
        "atua sem precisar comparar dois arquivos.")
)

cad.section("lab6-calcular-ganho", "Lab 6 - Calcular o ganho (antes x depois)",
    p("A parte que transforma o projeto em proposta: quanto tempo, quanto "
      "dinheiro, quantos casos.") +
    step([
        ("Pegue os tempos do AS-IS medido",
         "Do Lab 3: espera media e execucao media por etapa, em horas."),
        ("Defina o TO-BE alvo",
         "Quanto cada etapa vai custar depois? Ex.: fila 44 h &rarr; 8 h; "
         "triagem 10 h &rarr; 2 h (automatica)."),
        ("Calcule o TAT novo",
         "Some as novas esperas + execucoes. Compare com o TAT antigo."),
        ("Transforme tempo em dinheiro",
         "<code>minutos_poupados × custo/hora × volume_ano</code>. Use a coluna "
         "<code>custo_minuto</code> do dataset."),
        ("Verifique se o ganho e crivel",
         "Se o ganho prometido for 95%, desconfie. Ganho de 20-40% em processo "
         "real e otimo; 90% costuma ser promessa, nao previsao."),
    ]) +
    kpi([
        ("44 h", "espera na fila (AS-IS)"),
        ("8 h", "espera alvo (TO-BE)"),
        ("-82%", "reducao da etapa"),
        ("-24%", "TAT total"),
    ]) +
    callout("g", "Escreva a frase de impacto",
        "Ao final do Lab 6, voce deve ser capaz de dizer: "
        "&quot;Com a fila priorizada, o tempo de espera do perito cai de 44 h "
        "para 8 h, liberando 43.200 horas por ano - o equivalente a um "
        "perito-equivalente em trabalho tecnico.&quot; Numero, nao adjetivo.")
)

cad.section("lab7-apresentar", "Lab 7 - Apresentar e coletar feedback",
    p("Um processo redesenhado so existe se for <b>adotado</b>. O ultimo lab "
      "e de comunicacao e validacao.") +
    step([
        ("Monte a apresentacao em 4 blocos",
         "<b>1)</b> O processo hoje (AS-IS + gargalo medido). <b>2)</b> O que "
         "proponho (TO-BE). <b>3)</b> O ganho (numeros). <b>4)</b> O que preciso "
         "(apoio, recursos, decisao)."),
        ("Mostre os dois diagramas lado a lado",
         "AS-IS e TO-BE na mesma tela. A diferenca visual e o argumento."),
        ("Camine pelo AS-IS com quem conhece",
         "Se ninguem questionar o AS-IS, o TO-BE nao sera aceito. Fixe o AS-IS "
         "com quem executa antes de pedir mudanca."),
        ("Colete o feedback do time",
         "&quot;O que falta? O que nao vai funcionar? Onde isso trava?&quot; "
         "Anote e ajuste o TO-BE."),
        ("Feche com o pedido de decisao",
         "Termine com o que voce precisa do sponsor (pessoa, recurso, "
         "autorizacao). Sem pedido, e apenas uma ideia."),
    ]) +
    checklist([
        "AS-IS validado com quem executa.",
        "Gargalo medido com numero nos dados.",
        "TO-BE ligado ao gargalo (cada mudanca justificada).",
        "Ganho calculado em tempo e recurso.",
        "Pedido de decisao claro.",
    ]) +
    callout("err", "Apresentar o TO-BE sem o AS-IS",
        "Se voce mostra so o futuro, ninguem acredita (parece utopico). "
        "Sempre comece pelo <b>AS-IS validado</b>: quando todos veem que o "
        "processo real e esse, o TO-BE comeca a parecer possivel.")
)

# =================================================================
# PARTE 7 - CENARIOS POLITEC (3 PROCESSOS REAIS)
# =================================================================
cad.grp("Parte 7 - Cenarios POLITEC",
        "Tres processos reais modelados ponta a ponta: AS-IS medido, gargalo, TO-BE com automacao.")

cad.section("cenarios-intro", "Os 3 cenarios: qual processo voce vai modelar?",
    p("Cada cenario vem com um <b>dataset medido</b> (9.500+ execucoes de "
      "etapa em modelo estrela) e um caso completo de AS-IS &rarr; gargalo "
      "&rarr; TO-BE.") +
    grid2([
        ("\U0001f5fa Cenario 1 - Requisicao Pericial",
         "Do registro na delegacia ao laudo assinado. Gargalo: <b>fila do "
         "perito</b> (41,5% da espera). 10.352 execucoes."),
        ("\U0001f4b0 Cenario 2 - Empenho e Contrato",
         "Do pedido do setor a publicacao do ato. Gargalo: <b>parecer juridico "
         "+ autorizacao</b> (51,2%). Maior retrabalho. 9.541 execucoes."),
        ("\U0001f52c Cenario 3 - Cadeia de Custodia",
         "Da coleta no local a baixa da evidencia. Gargalo: <b>guarda</b> "
         "(35,3%) + risco de lacre. 10.840 execucoes.")
    ])
)

# --- Cenario 1 completo ---
cad.section("cen1-asis", "Cenario 1 - O AS-IS da requisicao pericial",
    p("O processo mais iconico da POLITEC. Sao 8 etapas, 4 atores, e "
      "o processo inteiro e <b>92,4% espera</b>.") +
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
    tbl(["Etapa", "Espera", "Execucao", "Retrabalho"],
        [["1. Entrada", "0 h", "0 h", "11,2%"],
         ["2. Triagem", "10 h", "1 h", "12,7%"],
         ["3. Distribuicao", "13 h", "1 h", "11,4%"],
         ["<b>4. Fila perito</b>", "<b>44 h</b>", "0 h", "12,1%"],
         ["5. Analise", "9 h", "5 h", "11,5%"],
         ["6. Revisao", "13 h", "2 h", "10,4%"],
         ["7. Assinatura", "10 h", "0 h", "11,7%"],
         ["8. Arquivamento", "7 h", "0 h", "11,7%"]],
        num_cols=[1, 2, 3]) +
    callout("err", "O que o diagrama revela",
        "Repare nas swimlanes: o caso <b>atravessa 4 sistemas</b> (papel, SIGT, "
        "e-mail, planilha) e muda de mao <b>4 vezes</b>. Cada fronteira de "
        "swimlane e um ponto de espera - e e ai que esta o gargalo.")
)

cad.section("cen1-gargalo", "Cenario 1 - O gargalo medido: a fila do perito",
    p("Rodando a tabela dinamica do Lab 3 nos dados do Cenario 1, a etapa "
      "<b>&quot;Fila perito&quot;</b> concentra <b>41,5% de toda a espera</b> do "
      "processo.") +
    bar_chart(
        ["Fila perito", "Revisao", "Distribuicao", "Triagem", "Assinatura", "Analise"],
        [41.5, 12.3, 11.9, 9.8, 9.7, 9.3],
        "Cenario 1 - Share da espera por etapa",
        "41,5% da espera do processo esta numa unica etapa. E uma fila que "
        "nao precisa de mais perito para encurtar: precisa de <b>ordem certa</b>.",
        fmt="{:.1f}%",
        destaque=0
    ) +
    tbl(["Achado", "Numero", "Implicacao"],
        [["Processo e espera", "92,4%", "O trabalho e minimo; a parada e o problema"],
         ["Gargalo", "Fila perito - 41,5%", "Atacar a fila, nao a analise"],
         ["Execucao maior", "Analise - 5 h", "Mais trabalho, mas so 9,3% da espera"],
         ["Menor espera da analise", "9 h (vs 44 h)", "O perito trabalha; o caso espera"]],
        num_cols=[]) +
    ficha("r", "A leitura contraintuitiva",
        "O intuicao diz &quot;o gargalo e a analise, que demora 5 h&quot;. O "
        "dado diz o contrario: a analise e <b>rapida</b>; o problema e o caso "
        "<b>esperar 44 h</b> na fila antes de comecar. Sem medir, a equipe "
        "contrataria mais peritos para resolver um problema de fila.")
)

cad.section("cen1-tobe", "Cenario 1 - O TO-BE: fila priorizada por prazo legal",
    p("A intervencao preenche a fileira do gargalo: em vez de atender por "
      "ordem de chegada, <b>prioriza por prazo legal</b> e monitora a carga "
      "em tempo real.") +
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
    tbl(["Mudanca", "Tipo", "Foco no gargalo"],
        [["Fila por prazo legal", "Integrar + automatizar", "<b>Sim</b> - reordena a fila"],
         ["Triagem assistida por tipo", "Automatizar", "Indireto - reduz entrada na fila"],
         ["Notificar dados faltantes", "Automatizar", "Indireto - evita ciclo de devolucao"],
         ["Painel WIP por perito", "Visualizar (BI)", "<b>Sim</b> - rebalanceia antes de acumular"],
         ["Alerta se fila > 24h", "Notificar", "<b>Sim</b> - aciona antes de virar gargalo"]],
        num_cols=[])
)

cad.section("cen1-ganho", "Cenario 1 - O ganho calculado",
    p("Do AS-IS medido ao TO-BE proposto, a conta fecha.") +
    tbl(["Metrica", "AS-IS", "TO-BE", "Ganho"],
        [["<b>Espera na fila</b>", "44 h", "8 h", "<b>-82%</b>"],
         ["TAT total (aprox.)", "92 dias", "70 dias", "<b>-24%</b>"],
         ["Fila de casos (Little's Law)", "~302 casos", "~230 casos", "-72 casos"],
         ["<b>Horas/ano poupadas</b>", "-", "-", "<b>43.200 h</b>"],
         ["Equivalente em pessoa", "-", "-", "<b>~1 perito-equivalente</b>"]],
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
    callout("g", "A frase para o diretor",
        "&quot;Hoje 36% do TAT do laudo e o tempo que o caso fica parado na "
        "fila. Se a fila for priorizada por prazo legal, tiramos 43 mil horas "
        "de espera por ano - sem contratar ninguem, so tocando o processo.&quot;")
)

# --- Cenario 2 completo ---
cad.section("cen2-asis", "Cenario 2 - O AS-IS do empenho e contrato",
    p("O caminho do dinheiro publico: 7 etapas, 5 unidades e o maior "
      "<b>retrabalho</b> dos tres cenarios (~16,6%).") +
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
    tbl(["Etapa", "Espera", "Execucao", "Retrabalho"],
        [["1. Pedido", "0 h", "4 h", "15,9%"],
         ["2. Cotacao", "10 h", "0 h", "16,4%"],
         ["3. Mapa comparativo", "21 h", "6 h", "17,0%"],
         ["<b>4. Parecer juridico</b>", "<b>36 h</b>", "5 h", "17,0%"],
         ["<b>5. Autorizacao</b>", "<b>27 h</b>", "1 h", "16,3%"],
         ["6. Empenho", "11 h", "0 h", "16,6%"],
         ["7. Publicacao", "18 h", "0 h", "16,9%"]],
        num_cols=[1, 2, 3]) +
    callout("err", "Onde o processo sangra",
        "As <b>duas aprovacoes</b> (parecer + autorizacao) somam <b>51,2% da "
        "espera</b>. E o retrabalho de ~16,6% significa que 1 em cada 6 "
        "documentos volta para refacao - quase sempre no mapa e no parecer.")
)

cad.section("cen2-gargalo", "Cenario 2 - O gargalo: aprovacoes encadeadas",
    p("Diferente do Cenario 1, aqui o gargalo e um <b>conjunto de etapas</b>: "
      "duas aprovacoes em sequencia.") +
    bar_chart(
        ["Parecer juridico", "Autorizacao", "Mapa comparativo", "Publicacao", "Empenho", "Cotacao"],
        [29.3, 21.9, 17.0, 14.7, 10.9, 6.2],
        "Cenario 2 - Share da espera por etapa",
        "Parecer + Autorizacao = 51,2% da espera. Sao as duas unicas "
        "aprovações do processo - e ninguem mede o tempo delas.",
        fmt="{:.1f}%",
        destaque=0
    ) +
    tbl(["Causa raiz", "Como confirmar", "Evidencia no processo"],
        [["Fila unica no juridico", "Contar quantos ficam na fila", "36 h de espera media"],
         ["Autorizador com muitas pendencias", "Pedir a pauta do ordenador", "27 h de espera"],
         ["Parecer devolvido com frequencia", "Contar devolucoes", "16,6% de retrabalho"],
         ["Expediente lento (chega tarde)", "Registrar hora de chegada", "Fila cresce no fim do dia"]],
        num_cols=[])
)

cad.section("cen2-tobe", "Cenario 2 - O TO-BE: pauta automatica e alerta de dotacao",
    p("A intervencao nao e &quot;aprovar mais rapido&quot;, e sim <b>ordenar e "
      "avisar</b>: uma pauta automatica que monta o que vence e alerta quando "
      "algo travar.") +
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
    tbl(["Intervencao", "Tipo", "Resolve"],
        [["Pauta automatica por prazo", "Automatizar", "Fila do juridico (29,3%)"],
         ["Alerta de dotacao insuficiente", "Automatizar + notificar", "Retrabalho do mapa"],
         ["Checklist de parecer", "Padronizar", "16,6% de retrabalho"],
         ["Painel de expedientes parados", "Visualizar (BI)", "Fila do ordenador (21,9%)"],
         ["Formulario digital de pedido", "Digitalizar", "Papel e redigitacao"]],
        num_cols=[])
)

cad.section("cen2-ganho", "Cenario 2 - O ganho",
    tbl(["Metrica", "AS-IS", "TO-BE", "Ganho"],
        [["<b>Parecer juridico (espera)</b>", "36 h", "14 h", "<b>-61%</b>"],
         ["<b>Autorizacao (espera)</b>", "27 h", "10 h", "<b>-63%</b>"],
         ["<b>Retrabalho</b>", "16,6%", "6,0%", "<b>-64%</b>"],
         ["TAT do empenho (aprox.)", "38 dias", "26 dias", "<b>-32%</b>"],
         ["Horas/ano poupadas", "-", "-", "<b>52.800 h</b>"]],
        num_cols=[1, 2, 3]) +
    callout("g", "O efeito dominó",
        "Quando o mapa comparativo volta corrigido, ele volta <b>antes</b> e o "
        "parecer espera menos. O ganho nao e so na etapa que voce otimizou - e "
        "nas etapas seguintes. E por isso que se mede o processo <b>inteiro</b>, "
        "nao etapa por etapa.")
)

# --- Cenario 3 completo ---
cad.section("cen3-asis", "Cenario 3 - O AS-IS da cadeia de custodia",
    p("O processo mais critico quanto a rastreabilidade. Alem do tempo, aqui o "
      "problema e <b>risco de prova</b>: lacre aberto pode inviabilizar o "
      "laudo.") +
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
    tbl(["Etapa", "Espera", "Execucao", "Divergencia de lacre"],
        [["1. Coleta", "0 h", "2 h", "4,9%"],
         ["2. Lacre", "11 h", "1 h", "5,5%"],
         ["3. Registro", "12 h", "0 h", "3,9%"],
         ["4. Transporte", "16 h", "3 h", "4,2%"],
         ["5. Recebimento", "14 h", "1 h", "5,5%"],
         ["<b>6. Guarda</b>", "<b>55 h</b>", "0 h", "4,0%"],
         ["7. Pericia", "21 h", "6 h", "5,2%"],
         ["8. Baixa", "25 h", "0 h", "4,6%"]],
        num_cols=[1, 2, 3]) +
    callout("err", "O gargalo duplo",
        "A etapa 6 (guarda) concentra <b>35,3% da espera</b>. Mas o gargalo "
        "real deste processo e duplo: o <b>tempo de guarda</b> e a "
        "<b>fragilidade do lacre em papel</b> (4,8% de divergencia). O TO-BE "
        "precisa atacar os dois.")
)

cad.section("cen3-gargalo", "Cenario 3 - O gargalo: guarda e rastreabilidade",
    p("Aqui a leitura muda: o gargalo nao e so de tempo, e de "
      "<b>confiabilidade do processo</b>. Uma evidencia parada 55 h em guarda e "
      "um lacre em papel sao riscos diferentes.") +
    bar_chart(
        ["Guarda", "Baixa", "Pericia", "Transporte", "Recebimento", "Registro", "Lacre"],
        [35.3, 16.4, 13.8, 10.6, 6.7, 5.7, 5.3],
        "Cenario 3 - Share da espera por etapa",
        "A guarda responde por 35,3% da espera. Mas o custo maior deste "
        "processo nao esta em nenhum destes numeros.",
        fmt="{:.1f}%",
        destaque=0
    ) +
    tbl(["Risco", "Probabilidade", "Impacto", "Zona"],
        [["Lacre aberto no transporte", "4,2%", "Alto (inviabiliza a prova)", "<b>Vermelho</b>"],
         ["Divergencia no recebimento", "5,5%", "Alto", "<b>Vermelho</b>"],
         ["Amostra degrada na guarda", "Media", "Alto", "<b>Vermelho</b>"],
         ["Perda de rastreio do responsavel", "Media", "Médio", "Amarelo"]],
        num_cols=[]) +
    ficha("r", "A diferenca deste cenario",
        "Nos cenarios 1 e 2, o gargalo e <b>economico</b> (tempo = dinheiro). "
        "Aqui o gargalo e <b>juridico</b> (rastreabilidade = validade da prova). "
        "Um TO-BE que so reduz tempo e insuficiente: ele precisa <b>garantir "
        "rastreio</b>.")
)

cad.section("cen3-tobe", "Cenario 3 - O TO-BE: custodia com QR Code",
    p("A intervencao aqui troca o <b>lacre em papel</b> por <b>rastreio "
      "digital</b>: cada transferencia vira um evento com responsavel, hora e "
      "QR - e um alerta dispara se a evidencia ficar parada alem do prazo.") +
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
    tbl(["Intervencao", "Tipo", "Resolve"],
        [["QR Code por evidencia", "Digitalizar + rastrear", "Lacre em papel, 5,5% de divergencia"],
         ["Leitor QR no recebimento", "Automatizar", "Conferencia manual (etapa 5)"],
         ["Bloqueio + alerta em divergencia", "Automatizar + notificar", "4,8% de divergencia total"],
         ["Alerta de guarda > 24h", "Automatizar", "35,3% da espera"],
         ["Assinatura digital na baixa", "Digitalizar", "Rastreabilidade do destino"]],
        num_cols=[])
)

cad.section("cen3-ganho", "Cenario 3 - O ganho",
    tbl(["Metrica", "AS-IS", "TO-BE", "Ganho"],
        [["<b>Espera na guarda</b>", "55 h", "18 h", "<b>-67%</b>"],
         ["<b>Divergencia de lacre</b>", "4,8%", "< 0,5%", "<b>-90%</b>"],
         ["Rastreio do responsavel", "Manual (pouco confiavel)", "Digital e automatico", "<b>Total</b>"],
         ["TAT custodia (aprox.)", "210 dias", "180 dias", "<b>-14%</b>"],
         ["Horas/ano poupadas", "-", "-", "<b>46.000 h</b>"]],
        num_cols=[1, 2, 3]) +
    callout("g", "O ganho que nao cabe em numero",
        "Neste cenario, o ganho maior nao e tempo: e <b>validade da prova</b>. "
        "Um lacre com rastreio digital nao so evita 4,8% de divergencia - ele "
        "sustenta a cadeia de custodia perante o Ministerio Publico. Esse "
        "argumento vale mais que a hora poupada.")
)

# =================================================================
# PARTE 8 - FECHAMENTO
# =================================================================
cad.grp("Parte 8 - Fechamento",
        "O metodo resumido, erros comuns, quiz, glossario e referencias.")

cad.section("metodo-resumido", "O metodo resumido (leve isso para o seu processo)",
    p("Toda a aula, em seis passos. Use como checklist.") +
    step([
        ("1. Delimite", "Onde começa e termina o processo? Escolha um processo real."),
        ("2. Descreva", "Aplique as 7 perguntas. Escreva o paragrafo do AS-IS."),
        ("3. Diagrame", "Converta o texto em Mermaid/BPMN, com swimlanes por ator."),
        ("4. Meça", "Esperas x execucao por etapa. Encontre o gargalo (Pareto)."),
        ("5. Redesenhe (TO-BE)", "Elimine, simplifique, integre, automatize - no gargalo."),
        ("6. Automatize e prove", "Intervencao digital + calculo de ganho + apresentacao."),
    ]) +
    ficha("g", "A frase final",
        "<b>Desenhe, meca, mude, prove.</b> Quatro verbos que resumem a aula "
        "e o metodo de melhoria de processo com dado.")
)

cad.section("erros-comuns", "Erros comuns: o que nao fazer",
    ul([
        "<b>Automatizar antes de medir</b>: invoca dinheiro em processo que talvez nem seja o gargalo.",
        "<b>TO-BE utopico</b>: fila zero e laudo em 2 h nao convencem ninguem.",
        "<b>Medir execucao sem esperar</b>: o gargalo quase sempre esta na fila, nao no trabalho.",
        "<b>Desenhar sem quem executa</b>: processo desenhado longe da realidade nao e adotado.",
        "<b>Confundir projeto com operacao</b>: &quot;todo dia Faster&quot; nao e projeto, e operacao.",
        "<b>Esquecer o caminho de retorno</b>: sem o fluxo de correcao, o diagrama mente sobre o tempo.",
        "<b>Prometer 90% de ganho</b>: ganho de 20-40% em processo real ja e excelente.",
        "<b>Ignorar a fronteira do sistema</b>: automatizar o que depende de outro orgao sem|align.",
    ]) +
    callout("err", "O erro que mais custa",
        "Automatizar o processo errado. Voce entrega no prazo, e o "
        "gargalo continua la - so que agora com um sistema caro rodando por "
        "cima. <b>Meça primeiro.</b>")
)

cad.section("quiz", "Quiz final - 15 perguntas",
    p("15 perguntas sobre BPMN, Mermaid, gargalos e TO-BE.") +
    q("Em BPMN, o losango (gateway) representa...",
      ["a) Uma atividade", "b) Uma decisao ou divisao de fluxo",
       "c) Um evento de inicio", "d) Uma swimlane"], 1) +
    q("O que e Little's Law (L = λ × W)?",
      ["a) Relacao entre fila, chegada e tempo",
       "b) Formula de custo de projeto",
       "c) Metodo de priorizacao de risco",
       "d) Tipo de grafico de Pareto"], 0,
      "Numero de itens no sistema = taxa de chegada × tempo de permanencia.") +
    q("No Mermaid, subgraph serve para...",
      ["a) Sublinhar texto", "b) Representar swimlanes (grupar por ator)",
       "c) Importar dados", "d) Gerar relatorio"], 1) +
    q("Na sequencia das 7 perguntas, a pergunta 'quem faz cada etapa'...",
      ["a) Vem primeiro", "b) Vem depois de mapear as atividades",
       "c) E opcional", "d) Vem so no final"], 1,
      "So faz sentido saber o que existe antes de saber quem faz.") +
    q("O que diferencia uma medida de espera (wait time) de execucao (touch time)?",
      ["a) Sao a mesma coisa", "b) Espera e o tempo parado; execucao e o trabalho",
       "c) Espera e o trabalho; execucao e a parada",
       "d) Depende do projeto"], 1) +
    q("Onde o gargalo de um processo geralmente esta?",
      ["a) Na etapa com mais tempo de execucao",
       "b) Na etapa com mais tempo de espera (na fila)",
       "c) Sempre na primeira etapa", "d) Na etapa mais barata"], 1,
      "Em media, 88-92% do tempo de processo e espera.") +
    q("O principio de Pareto aplicado a processos diz...",
      ["a) Metade do processo e prazo",
       "b) Poucas etapas concentram a maior parte do desperdicio",
       "c) Todo processo deve ter 20 etapas",
       "d) O processo ideal tem 80 etapas"], 1) +
    q("Na ordem dos 5 principios de redesenho, o que vem ANTES de automatizar?",
      ["a) Padronizar", "b) Eliminar, simplificar e integrar",
       "c) Visualizar", "d) Medir"], 1,
      "Automatizar um processo ruim cria um processo ruim e mais rapido.") +
    q("Um gateway paralelo (+), diferentemente do exclusivo (X)...",
      ["a) Escolhe so um caminho", "b) Faz todos os caminhos em paralelo",
       "c) Nao existe em BPMN", "d) E so para mensagens"], 1) +
    q("O que o sequenceDiagram do Mermaid mostra, que o flowchart nao mostra bem?",
      ["a) O fluxo de mensagens entre atores no tempo",
       "b) O custo do processo", "c) O grafico de espera", "d) O organograma"], 0) +
    q("stateDiagram-v2 do Mermaid e usado para mostrar...",
      ["a) O cronograma", "b) Os estados que um objeto assume ao longo do tempo",
       "c) O custo", "d) A swimlane"], 1) +
    q("Para provar o ganho de um TO-BE, voce compara...",
      ["a) O TO-BE com o AS-IS medido, nos mesmos dados",
       "b) O TO-BE com a opiniao do sponsor",
       "c) O AS-IS com o orcamento",
       "d) O TO-BE com outro projeto"], 0) +
    q("Qual a primeira automacao (<b>Onda 1</b>) mais barata e de maior efeito em um processo?",
      ["a) Trocar todo o sistema", "b) Alertas de prazo + painel de carga (BI)",
       "c) Contratar mais gente", "d) Refazer o banco de dados"], 1) +
    q("No Cenario 1 (requisicao pericial), o gargalo medido e...",
      ["a) A analise do exame", "b) A fila do perito",
       "c) A assinatura", "d) O arquivamento"], 1,
      "41,5% de toda a espera do processo esta na fila do perito.") +
    q("Por que versionar o diagrama do processo (AS-IS) no Git?",
      ["a) Para ficar mais bonito",
       "b) Para ter linha de base e historico do processo",
       "c) Para o GitHub exigir",
       "d) Para impressionar o diretor"], 1)
)

cad.section("glossario", "Glossario rapido da Aula 6",
    glossary([
        ("AS-IS", "Diagrama do processo como ele e hoje."),
        ("TO-BE", "Diagrama do processo como ele sera depois da intervencao."),
        ("BPMN 2.0", "Notacao padrao internacional para modelar processos (OMG/ISO 19510)."),
        ("Mermaid", "Linguagem de texto que gera diagramas (flowchart, sequence, state, gantt...)."),
        ("Evento (BPMN)", "Ponto que dispara, espera ou detecta: inicio, intermediario, fim."),
        ("Atividade (BPMN)", "O que e feito: tarefa, subprocesso."),
        ("Gateway (BPMN)", "Losango que decide/divide o fluxo (exclusivo, paralelo, inclusivo)."),
        ("Swimlane / Lane", "Faixa que indica quem executa a atividade."),
        ("Subgraph (Mermaid)", "Bloco que agrupa atividades - equivale a swimlane."),
        ("Gargalo", "Etapa que mais restringe o fluxo, medido por espera ou por acao."),
        ("Espera (wait time)", "Tempo que o caso fica parado na fila."),
        ("Execucao (touch time)", "Tempo que alguem efetivamente trabalha no caso."),
        ("TAT", "Tempo de ciclo total do processo (soma de esperas + execucoes)."),
        ("Little's Law", "L = λ × W - fila = chegada × tempo."),
        ("Pareto", "Ordenar por impacto para achar os 20% criticos."),
        ("WIP", "Work In Progress - itens em processamento simultaneo."),
        ("Retrabalho", "Refazer etapa ja feita, por erro ou devolucao."),
        ("Intervencao digital", "Mudar o processo com tecnologia (app, automacao, BI, script)."),
        ("Roadmap (TO-BE)", "Implantar o TO-BE em ondas, medindo o ganho de cada uma."),
        ("Stakeholder", "Parte interessada no projeto (sponsor, equipe, usuario, cliente)."),
        ("Sponsor", "Quem aprova e destrava recursos/decisoes do projeto."),
    ])
)

cad.section("referencias", "Referencias e para ir alem",
    ul([
        "<b>BPMN 2.0 (OMG)</b> - <code>omg.org/spec/BPMN/2.0/</code>: a "
        "especificacao oficial da notacao.",
        "<b>Mermaid</b> - <code>mermaid.js.org</code> e o "
        "<b>Mermaid Live Editor</b> (mermaid.live) para renderizar online.",
        "<b>ISO 19510</b>: padrao internacional de modelagem de processos.",
        "<b>Lean Enterprise / Value Stream Mapping</b>: a disciplina de mapear "
        "o fluxo e achar o desperdicio.",
        "<b>Womack & Jones</b> - <i>Lean Thinking</i>: os principios de "
        "eliminacao de desperdicio.",
        "<b>John Little</b> - a formula L = λ × W que dimensiona filas.",
        "<b>PMBOK Guide</b>: os 5 grupos de processos da gestao de projetos.",
        "<b>Power Automate / Power BI</b>: as ferramentas de intervencao "
        "digital (vistas nos Dias 4 e 5).",
    ]) +
    callout("tip", "Para comecar hoje",
        "Escolha um processo pequeno da sua area, faca o Lab 1 (descrever em "
        "texto) e o Lab 2 (desenhar em Mermaid). Em uma tarde voce tem o AS-IS "
        "do seu processo - e ja entende onde o tempo se perde.")
)

cad.section("encerramento", "O fim da capacitacao - e o comeco da mudanca",
    p("Sao seis dias de fundamentacao, dados, planilha, ETL, dashboards e "
      "hoje <b>gestao de projetos e melhoria de processos</b>. O ciclo fechou: "
      "comecou no <b>dado</b> e termina na <b>acao</b>.") +
    legenda([
        ("\U0001f4a1", "D1 a D3 - Dados e planilha",
         "Aprendeu a medir, organizar e validar - a base de tudo."),
        ("\U0001f4ca", "D4 e D5 - Dashboards de BI",
         "Transformou dado em visual - ver o processo e o gargalo."),
        ("\U0001f5fa", "D6 - Gestao e melhoria (hoje)",
         "Desenhou, mediu o gargalo, redesenhou o TO-BE e automatizou.")
    ]) +
    callout("purple", "A mensagem final do curso",
        "&quot;<b>O dado so tem valor quando vira decisao; a decisao so tem "
        "valor quando vira mudanca no processo; e a mudanca so se sustenta "
        "quando esta medida.</b>&quot; Se voce aplicar esse ciclo - "
        "<b>medir, mudar, medir de novo</b> - em um processo da POLITEC, esta "
        "capacitacao cumpriu o papel. Boa sorte, e bom processo.")
)

# =================================================================
# CONSTRUCAO
# =================================================================
cad.build()