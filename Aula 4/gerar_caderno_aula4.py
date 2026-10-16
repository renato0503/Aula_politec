# -*- coding: utf-8 -*-
"""Gerador do caderno da Aula 4 - POLITEC/MT.

Tema: Business Intelligence na Administracao Publica (Power BI - Basico).
Conteudo derivado dos slides Dia-4-Politec.pdf (55 paginas).

Rode:  python gerar_caderno_aula4.py
PDF:   python ..\\exportar_pdf.py 4
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from caderno_lib import (Caderno, p, h3, ul, checklist, ficha, callout, tbl,
                         code, step, q, aplicab, grid2, flow_h, kpi,
                         antesdepois, legenda, glossary, bar_chart)

cad = Caderno(
    out=str(pathlib.Path(__file__).resolve().parent / "caderno-dia4.html"),
    dia=4,
    kicker="Aula 4 · Business Intelligence",
    headline="Business Intelligence na Administracao Publica",
    sub="Do arquivo bruto ao dashboard institucional de gestao pericial. A interface do Power BI "
        "Desktop, a conexao de dados, os visuais essenciais, a publicacao no Service, os workspaces "
        "com governanca e a atualizacao agendada a servico da POLITEC/MT.",
    meta="Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 4 · Modulo 6",
    descricao="Caderno do Dia 4 do Curso de Capacitacao POLITEC/MT: Business Intelligence aplicado "
              "a pericia criminal com Power BI. O que e BI (Dresner/Gartner), arquitetura Desktop/Service/Mobile, "
              "conexao de mais de 100 fontes, Importacao x DirectQuery, visuais essenciais, mapas com Bing, "
              "slicers, publicacao, workspaces segregados, permissoes, Apps, atualizacao agendada, "
              "On-premises Data Gateway, KPIs (TAT, SLA, QL), alertas, LGPD e uma previa de DAX.",
)

# =================================================================
# ABERTURA
# =================================================================
cad.grp("Abertura", "O proposito do dia: transformar o dado bruto em decisao institucional.")

cad.section("boas-vindas", "Bem-vindo ao caderno do Dia 4",
    p("Depois de dominar a estatistica (Dia 1), a planilha (Dias 2 e 3) e a qualidade dos dados, "
      "chegou a hora de dar o salto: <b>Business Intelligence</b>. No Dia 4 a planilha estruturada "
      "deixa de ser um arquivo no computador do analista e vira uma <b>inteligencia institucional "
      "viva</b>, acessada pelo Diretor, pelo Chefe de Setor e pelo perito, em qualquer lugar.") +
    p("Este caderno acompanha os dois blocos do dia — manha (interface, conexao e primeiros "
      "relatorios) e tarde (publicacao, compartilhamento e workspaces) — com passo a passo de "
      "cliques no Power BI Desktop e no Power BI Service.") +
    legenda([
        ("\U0001f5a5", "Parte 1 - Interface e relatorios",
         "Power BI Desktop, conexao de dados, Power Query, visuais essenciais e o primeiro dashboard."),
        ("\u2601", "Parte 2 - Publicacao e governanca",
         "Power BI Service, workspaces, permissoes, Apps, atualizacao agendada e Data Gateway."),
        ("\U0001f9ea", "Parte 3 - Pratica guiada",
         "Sete laboratorios que constroem, do zero, o painel de backlog da POLITEC."),
        ("\U0001f3db", "Partes 4 e 5 - Aplicacoes e fechamento",
         "Dashboards, KPIs, cenarios reais, LGPD, exercicio final, quiz e glossario."),
    ]) +
    callout("note", "Ferramentas do dia",
        "O <b>Power BI Desktop</b> e gratuito e roda no PC do perito. O compartilhamento privado na "
        "nuvem exige conta corporativa <code>@politec.mt.gov.br</code> com licenca <b>Pro</b> ou "
        "<b>Premium</b>. Tenha a pasta <code>datasets/</code> (as tabelas <code>fato_*</code> e "
        "<code>dim_*</code>) a mao para praticar.")
)

cad.section("mapa-do-dia", "Mapa do Dia 4: dois blocos, um dashboard institucional",
    p("O dia comeca no cockpit do Desktop e termina com um dashboard publicado, com atualizacao "
      "automatica, governanca de acesso e conformidade com a LGPD.") +
    grid2([
        ("\U0001f305 Manha (08h-12h) - Modulo 6, Parte 1",
         ul(["O que e BI na pericia criminal (Dresner, Gartner 1989)",
             "Excel x Power BI: calculo x inteligencia corporativa",
             "Os 3 pilares: <b>Desktop, Service e Mobile</b>",
             "Interface do Desktop e os <b>3 modos</b> de trabalho",
             "Conexao de dados e <b>Importacao x DirectQuery</b>",
             "Visuais essenciais, mapas com Bing e <b>slicers</b>",
             "Construcao do primeiro dashboard de backlog"])),
        ("\U0001f306 Tarde (13h-17h) - Modulo 6, Parte 2",
         ul(["Power BI Service e o requisito de licenca Pro/Premium",
             "<b>Workspaces</b> institucionais e segregacao por area",
             "<b>Permissoes</b>: Admin, Membro e Visualizador",
             "<b>Apps</b>: o pacote <i>Painel do Perito</i>",
             "<b>Atualizacao agendada</b> e o On-premises Data Gateway",
             "Dashboards estrategico e tatico, KPIs (TAT, SLA, QL)",
             "Governanca, erros comuns, LGPD e previa de DAX"])),
    ]) +
    ficha("g", "Objetivo do dia",
        "Sair sabendo transformar registros periciais em <b>paineis interativos e seguros</b>, "
        "publicados na nuvem com o dado certo para a pessoa certa.")
)

cad.section("da-planilha-ao-bi", "Da planilha ao BI: a ponte construida nos Dias 2 e 3",
    p("Nada aqui comeca do zero. O BI e a <b>continuacao natural</b> do trabalho feito nas aulas "
      "anteriores: a base que voce estruturou (Ctrl+T), validou e padronizou e exatamente o que "
      "alimenta o dashboard de hoje.") +
    flow_h([
        ("\U0001f4c4", "Base bruta"),
        ("\U0001f4d0", "Tabela estruturada"),
        ("\U0001f50d", "Qualidade de dados"),
        ("\U0001f4ca", "Dashboard Power BI"),
        ("\u2601", "Inteligencia na nuvem"),
    ]) +
    aplicab(
        "Sempre que a gestao pericial precisar decidir com base em volume, prazo ou custo.",
        "Porque a planilha responde perguntas pontuais; o BI responde perguntas repetidas e combinadas, para muitas pessoas ao mesmo tempo.",
        "O backlog de DNA que voce controlava em <code>CONT.SE</code> no Dia 2 vira, no Dia 4, um "
        "<b>cartao de KPI atualizado de hora em hora</b> e um mapa de calor por municipio.") +
    callout("tip", "Prepare hoje, colha hoje",
        "Se a base dos Dias 2 e 3 estiver em Tabela Estruturada, com nomes sem acento, sem celulas "
        "mescladas e datas numericas, a importacao no Power BI e quase automatica.")
)

# =================================================================
# PARTE 0 - PREPARACAO: POWER BI DESKTOP DO ZERO
# =================================================================
cad.grp("Parte 0 · Preparação - Power BI Desktop do zero",
        "O manual do iniciante: instalar, entender a tela, obter e limpar dados, modelar, "
        "criar visuais e montar as 3 abas do painel de orçamento e contratos.")

cad.section("p0-antes-de-comecar", "Antes de começar: o que você vai construir",
    p("Esta parte é o <b>guia de preparação</b> do Dia 4. Ela existe para que você nunca tenha "
      "aberto o Power BI antes e, mesmo assim, saia dela capaz de montar o primeiro dashboard. "
      "Vamos construir, do zero, um painel de <b>orçamento e contratos</b> de um órgão de perícia, "
      "com <b>três abas</b> independentes e interligadas.") +
    p("O material usa um conjunto de dados sintético em <b>modelo estrela</b> (uma tabela de "
      "empenhos com mais de 600 linhas cercada por dimensões de setor, rubrica, fornecedor, "
      "contrato, modalidade e fonte). Ele vem em <b>dois arquivos</b>: um com defeitos de propósito "
      "(para você treinar a limpeza) e um gabarito já limpo.") +
    legenda([
        ("1", "Aba 1 - Visão Orçamentária",
         "Dotação x empenhado x pago, com cartões de KPI e evolução no tempo."),
        ("2", "Aba 2 - Execução por Setor e Rubrica",
         "Quem gasta, em quê e quanto ainda há para executar."),
        ("3", "Aba 3 - Contratos e Fornecedores",
         "Contratos vigentes, maiores fornecedores e distribuição por modalidade."),
    ]) +
    callout("note", "Pré-requisitos",
        "Tenha o <b>Power BI Desktop</b> instalado (Windows 10 ou superior, 64 bits) e a pasta "
        "<code>datasets/orcamento/</code> desta aula em mãos, com os arquivos "
        "<code>Orcamento_Contratos_SUJO.xlsx</code> e <code>Orcamento_Contratos_LIMPO.xlsx</code>.") +
    p("<i>Nota de leitura:</i> esta parte reapresenta, de forma guiada e do zero, a interface que a "
      "<b>Parte 1</b> discute conceitualmente e que a <b>Parte 3</b> pratica em laboratórios. "
      "Use-a como degrau de entrada.")
)

cad.section("p0-instalar", "Instalando o Power BI Desktop",
    p("O <b>Power BI Desktop</b> é o programa gratuito que roda no seu computador. É nele que você "
      "conecta os dados, limpa, modela e desenha o relatório. Tudo começa com a instalação.") +
    step([
        ("Requisitos", "Windows 10 ou 11, 64 bits, com pelo menos 4 GB de RAM "
         "(8 GB recomendado) e o Microsoft Edge WebView2 instalado (o instalador resolve)."),
        ("Duas formas de instalar", "Pelo site oficial <b>powerbi.microsoft.com</b> (botão "
         "<i>Baixar o Power BI Desktop</i>) ou pela <b>Microsoft Store</b> (atualiza sozinho)."),
        ("Abra o programa", "Ao abrir pela primeira vez, aparece uma tela de boas-vindas. "
         "Feche-a: é aqui que começamos do zero."),
        ("Idioma", "Confira em <b>Arquivo &rarr; Opções e configurações &rarr; Opções &rarr; "
         "Configurações regionais</b> que o idioma e a localidade estão em <b>Português (Brasil)</b>."),
    ]) +
    callout("err", "Não confunda Desktop com Service",
        "O <b>Desktop</b> é o programa que você instala e onde o painel é <i>construído</i>. O "
        "<b>Service</b> (powerbi.com) é o site na nuvem, onde o painel é <i>compartilhado</i>. "
        "Nesta parte trabalhamos só no <b>Desktop</b>.") +
    aplicab(
        "Sempre que a gestão precisar de um painel novo, o primeiro passo é abrir o Desktop.",
        "Porque o Desktop é gratuito e funciona offline: você monta e testa antes de publicar.",
        "Um servidor da POLITEC monta o painel de contratos no Desktop do seu próprio computador, "
        "sem depender de licença paga, e só depois decide o que publicar.")
)

cad.section("p0-tour-interface", "Tour pela tela: a interface do Power BI Desktop",
    p("Antes de clicar, reconheça o terreno. A tela se divide em cinco áreas. Se você localiza cada "
      "uma, o resto fica fácil.") +
    tbl(["Área", "Onde fica", "Para que serve"],
        [["<b>Faixa de opções</b>", "Topo da janela",
          "Menus: Página Inicial, Inserir, Modelagem, Exibir, Otimizar, Ajuda."],
         ["<b>Canvas</b> (tela)", "Centro",
          "A folha onde os visuais são desenhados — o relatório em si."],
         ["<b>Painel Visualizações</b>", "Direita, aba <i>Visualizações</i>",
          "Lista de visuais (colunas, linha, cartão, matriz, mapa...)."],
         ["<b>Painel Dados / Campos</b>", "Direita, aba <i>Dados</i>",
          "As tabelas importadas e seus campos, prontos para arrastar."],
         ["<b>Painel Filtros</b>", "Direita, aba <i>Filtros</i>",
          "Filtros de nível visual, de página e de relatório."]],
        num_cols=[]) +
    legenda([
        ("🗺", "Faixa de opções", "Tudo se inicia em Página Inicial: Obter Dados, Formatar, Publicar."),
        ("📄", "Canvas", "A folha em branco onde o painel ganha forma, visual por visual."),
        ("🧰", "Painéis laterais", "Visualizações, Dados e Filtros: seu canivete suíço."),
    ]) +
    callout("tip", "Reduza a bagunça visual",
        "Se a lista de campos estiver poluída, use o ícone de busca no painel Dados e o botão "
        "<b>Expandir/Recolher</b> para trabalhar só com a tabela que importa no momento.")
)

cad.section("p0-tres-visoes", "As três visões: Relatório, Dados e Modelo",
    p("No canto inferior esquerdo existem três ícones que trocam o modo de trabalho. Cada visão tem "
      "uma função específica e você alterna entre elas o tempo todo.") +
    tbl(["Visão", "Ícone", "O que você faz nela"],
        [["<b>Relatório</b>", "Gráfico de barras",
          "Cria e organiza os <i>visuais</i>: é a visão principal do painel."],
         ["<b>Dados</b>", "Tabela",
          "Confere as linhas importadas, ajusta formatos, tipos e cria colunas calculadas."],
         ["<b>Modelo</b>", "Diagrama de caixas",
          "Cria e inspeciona os <i>relacionamentos</i> entre fato e dimensão."]],
        num_cols=[]) +
    step([
        ("Vá para Dados", "Clique no ícone do meio, à esquerda. Veja as tabelas importadas e "
         "as primeiras linhas."),
        ("Vá para Modelo", "Clique no ícone do diagrama. As tabelas aparecem como caixas ligadas "
         "por linhas (os relacionamentos)."),
        ("Volte para Relatório", "Clique no ícone do gráfico. É aqui que passamos a maior parte do tempo."),
    ]) +
    callout("note", "Regra de ouro",
        "Dado se <b>confere</b> na visão Dados, relação se <b>cria</b> na visão Modelo e história se "
        "<b>conta</b> na visão Relatório. Cada coisa no seu lugar.")
)

cad.section("p0-obter-dados", "Obter Dados: conectando o Excel pela primeira vez",
    p("Aqui começa a mágica. Vamos abrir o arquivo <b>sujo</b> de propósito: a ideia é justamente "
      "sentir o problema para aprender a resolver. O Power BI lê o arquivo e mostra uma prévia antes "
      "de importar qualquer coisa.") +
    step([
        ("Obter Dados", "Na faixa <b>Página Inicial</b>, clique em <b>Obter Dados</b> e escolha "
         "<b>Pasta de Trabalho do Excel</b>."),
        ("Escolha o arquivo", "Navegue até <code>datasets/orcamento/</code> e abra "
         "<code>Orcamento_Contratos_SUJO.xlsx</code>."),
        ("Navegador", "Aparece a janela <b>Navegador</b> com as abas do arquivo. Clique em uma aba "
         "para ver a prévia dos dados."),
        ("Selecione as abas", "Marque <b>fato_empenhos</b>, <b>fato_dotacao</b> e todas as "
         "<b>dim_*</b>. Use a caixa da aba para marcar várias de uma vez."),
        ("Transformar, não Carregar", "Clique em <b>Transformar Dados</b>. Vamos limpar antes de "
         "trazer para o modelo."),
    ]) +
    code("""
        Página Inicial > Obter Dados > Pasta de Trabalho do Excel
        Arquivo : datasets/orcamento/Orcamento_Contratos_SUJO.xlsx
        Abas    : fato_empenhos, fato_dotacao,
                  dim_calendario, dim_setor, dim_rubrica, dim_modalidade,
                  dim_fonte, dim_status_empenho, dim_fornecedor, dim_contrato
        Botão   : Transformar Dados
        """, "powerbi") +
    callout("tip", "Por que não o arquivo LIMPO?",
        "Use o <b>SUJO</b> para praticar a limpeza de verdade (é o que acontece na vida real). "
        "O <b>LIMPO</b> fica como gabarito, para conferir se o seu resultado bateu.")
)

cad.section("p0-navegador", "O Navegador: Carregar x Transformar Dados",
    p("Depois de escolher as abas, os botões <b>Carregar</b> e <b>Transformar Dados</b> parecem "
      "iguais, mas levam a caminhos diferentes. Entenda a diferença antes de clicar.") +
    tbl(["Botão", "Quando usar", "O que acontece"],
        [["<b>Carregar</b>", "Base já limpa e no formato certo.",
          "Traz a tabela direto para o modelo, sem passar pela oficina."],
         ["<b>Transformar Dados</b>", "Base com defeito (nosso caso).",
          "Abre o <b>Power Query</b>, onde você limpa antes de carregar."]],
        num_cols=[]) +
    step([
        ("Seleção múltipla", "Marque a caixa <b>Selecionar vários itens</b> (ou clique na "
         "primeira, segure <kbd>Shift</kbd> e clique na última)."),
        ("Escolha a ação", "Como a base tem defeitos, clique em <b>Transformar Dados</b>."),
        ("Confira a chegada", "Um editor novo abre com cada aba do Excel como uma <i>consulta</i> "
         "na coluna esquerda."),
    ]) +
    callout("err", "Carregar duas versões da mesma tabela",
        "Nunca carregue o arquivo SUJO <i>e</i> o LIMPO juntos: você cria tabelas duplicadas e "
        "confunde os relacionamentos. Escolha um caminho.")
)

cad.section("p0-power-query", "Power Query: a oficina de limpeza",
    p("O <b>Power Query</b> é a oficina onde o dado bruto vira dado confiável. Cada passo que você "
      "dá fica registrado como uma <b>receita</b>: na próxima vez que o arquivo mudar, os mesmos "
      "ajustes rodam sozinhos.") +
    flow_h([
        ("📥", "Obter"),
        ("🧽", "Limpar"),
        ("🔤", "Tipar"),
        ("✅", "Fechar & Aplicar"),
    ]) +
    tbl(["Aba / ferramenta", "Para que serve"],
        [["<b>Página Inicial</b>", "Remover linhas/colunas, usar primeira linha como cabeçalho, "
          "substituir valores, mesclar consultas."],
         ["<b>Transformar</b>", "Dividir/mesclar colunas, formatar texto, extrair, agrupar."],
         ["<b>Adicionar Coluna</b>", "Coluna personalizada, condicional, de exemplo, índice."],
         ["<b>Painel Etapas Aplicadas</b>", "A lista, à direita, de tudo que você fez — dá para "
          "voltar, renomear ou apagar uma etapa."]],
        num_cols=[]) +
    callout("note", "Tudo é reversível",
        "Errou uma etapa? Clique no <b>X</b> ao lado dela no painel <b>Etapas Aplicadas</b>. "
        "A limpeza é não destrutiva: o arquivo original nunca é alterado.")
)

cad.section("p0-limpeza-estrutura", "Limpeza 1: cabeçalho, linhas inúteis e duplicatas",
    p("O primeiro grupo de defeitos é o mais comum em relatórios exportados de sistemas: a planilha "
      "não começa pelo cabeçalho, tem linhas vazias no meio, uma linha de <b>TOTAL GERAL</b> no fim "
      "e até linhas repetidas.") +
    tbl(["Defeito", "Onde está", "Ação no Power Query"],
        [["Linha de título na linha 1", "todas as abas",
          "<b>Página Inicial &rarr; Usar Primeira Linha como Cabeçalho</b>"],
         ["Linhas em branco no meio", "fato_empenhos, dim_calendario",
          "<b>Página Inicial &rarr; Remover Linhas &rarr; Remover Linhas Vazias</b>"],
         ["Linha TOTAL GERAL no fim", "fato_empenhos",
          "Filtrar <code>id_empenho</code> diferente de TOTAL GERAL (Remover Linhas Filtradas)"],
         ["Linhas duplicadas", "fato_empenhos, dim_fornecedor",
          "<b>Página Inicial &rarr; Remover Linhas &rarr; Remover Duplicatas</b>"]],
        num_cols=[]) +
    step([
        ("Promova o cabeçalho", "Com a consulta selecionada, clique em <b>Usar Primeira Linha "
         "como Cabeçalho</b>. O título sai e os nomes das colunas sobem."),
        ("Remova as linhas vazias", "<b>Remover Linhas &rarr; Remover Linhas Vazias</b>."),
        ("Tire o TOTAL GERAL", "Clique na seta da coluna <code>id_empenho</code>, desmarque "
         "<b>TOTAL GERAL</b>. Nunca deixe um total dentro da base de fatos."),
        ("Remova duplicatas", "Selecione a coluna-chave (<code>id_empenho</code>) e use "
         "<b>Remover Duplicatas</b>."),
    ]) +
    antesdepois(
        "Base com título, brancos e o TOTAL GERAL misturado às linhas: a soma dobra e o gráfico mente.",
        "Base com cabeçalho correto, sem brancos e sem total: cada linha é um empenho de verdade.") +
    callout("err", "O erro clássico do TOTAL GERAL",
        "Se você deixar a linha <b>TOTAL GERAL</b>, o Power BI vai somá-la junto com os empenhos. "
        "É a causa número um de dashboards com número errado.")
)

cad.section("p0-limpeza-datas", "Limpeza 2: datas que chegam como texto",
    p("No arquivo sujo, as datas vêm como <b>texto</b>, em cinco formatos diferentes "
      "(<code>03/01/2024</code>, <code>2024-01-05</code>, <code>05-01-2024</code>, "
      "<code>05/01/24</code>, <code>01/05/2024</code>). Enquanto forem texto, não existe cálculo de "
      "tempo, ordenação nem eixo cronológico.") +
    step([
        ("Altere o tipo", "Selecione a coluna <code>data</code> (ou <code>data_empenho_key</code>) e, "
         "em <b>Transformar &rarr; Tipo de Dados</b>, escolha <b>Data</b>."),
        ("Use a localidade certa", "Se o Power Query reclamar, vá em <b>Tipo de Dados &rarr; Usando "
         "Localidade</b> e escolha <b>Português (Brasil)</b>. Assim <code>05/01</code> é lido como "
         "5 de janeiro, e não maio."),
        ("Limpe a hora", "Em <code>dim_calendario</code> algumas datas vêm como "
         "<code>01/01/2024 00:00:00</code>. Divida a coluna por espaço ou apenas altere o tipo para "
         "<b>Data</b>, descartando a hora."),
        ("Confira", "Abra a visão <b>Dados</b>: as datas devem aparecer alinhadas à esquerda como "
         "texto ou, melhor, com o ícone de calendário."),
    ]) +
    code("""
        // Formato M aplicado por baixo dos panos:
        Table.TransformColumnTypes(Fonte,
            {{"data", type date}}, "pt-BR")
        """, "powerquery") +
    callout("err", "O dia 05/01/2024 virar maio",
        "Sem a localidade <b>pt-BR</b>, o Power BI interpreta <code>mm/dd</code> (padrão americano) "
        "e troca dia por mês. Datas erradas deslocam todo o eixo temporal do painel.")
)

cad.section("p0-limpeza-moeda", "Limpeza 3: valores em texto (R$, espaços e parênteses)",
    p("Os valores monetários também vieram como texto: <code>R$ 95.824,77</code>, "
      "<code>461.642,99</code>, <code>R$ 193417.89</code> e até <code> 571.672,34 </code> com espaços. "
      "Enquanto forem texto, o Power BI conta linhas em vez de somar dinheiro.") +
    step([
        ("Remova o R$", "Selecione a coluna e use <b>Substituir Valores</b>: substitua <code>R$</code> "
         "por vazio."),
        ("Remova os espaços", "Ainda em <b>Substituir Valores</b>, substitua o espaço por vazio. "
         "Ou use <b>Transformar &rarr; Formatar &rarr; Cortar (Trim)</b> e <b>Limpar</b>."),
        ("Trate os negativos", "Estornos vêm entre parênteses, como <code>(1.500,00)</code>. "
         "Substitua <code>(</code> por <code>-</code> e depois remova o <code>)</code>."),
        ("Converta para decimal", "<b>Tipo de Dados &rarr; Número Decimal &rarr; Usando Localidade "
         "&rarr; Português (Brasil)</b>, para que a vírgula seja o separador decimal."),
    ]) +
    antesdepois(
        "Coluna de texto: <code>R$ 95.824,77</code> — o resumo mostra Contagem, não Soma.",
        "Coluna decimal: <code>95.824,77</code> — o resumo mostra Soma e o KPI funciona.") +
    aplicab(
        "Sempre que o relatório do sistema vier com símbolos e pontos no número.",
        "Porque o visual só soma o que é número; texto com R$ é apenas enfeite.",
        "O total de empenhos do ano passa de R$ 185 milhões quando os valores são números — e é "
        "zero se você tentar somar a coluna ainda em texto.")
)

cad.section("p0-limpeza-texto", "Limpeza 4: textos, espaços e categorias padronizadas",
    p("As dimensões vêm com o mesmo rótulo escrito de várias formas — <code>LAB. TOXICOLOGIA</code>, "
      "<code>Laboratorio de Toxicologia</code>, <code> laboratorio de toxicologia </code>. Sem "
      "padronizar, o mesmo setor aparece três vezes no gráfico.") +
    step([
        ("Cortar e limpar", "<b>Transformar &rarr; Formatar &rarr; Cortar (Trim)</b> remove espaços "
         "das pontas; <b>Limpar</b> remove caracteres invisíveis."),
        ("Padronize a caixa", "<b>Formatar &rarr; Caixa da Palavra (Capitalizar Cada Palavra)</b> "
         "deixa os rótulos consistentes."),
        ("Remova as duplicatas", "Depois de padronizar, selecione a coluna-chave "
         "(<code>setor_key</code>) e use <b>Remover Duplicatas</b>. As três grafias viram uma só."),
        ("Separe código e texto", "Em <code>dim_rubrica</code>, a coluna traz "
         "<code>339014 - Diarias</code> junta. Use <b>Dividir Coluna &rarr; Por Delimitador</b> com "
         "o separador <code> - </code> (hífen entre espaços)."),
    ]) +
    grid2([
        ("Antes de padronizar",
         ul(["LAB. TOXICOLOGIA", "Laboratorio de Toxicologia", " lab toxicologia "])),
        ("Depois de padronizar",
         ul(["Laboratorio de Toxicologia", "(uma linha só, sem duplicata)"])),
    ]) +
    callout("err", "Formatar texto antes de remover duplicatas",
        "Ordem errada: se remover duplicatas <i>antes</i> de padronizar, as grafias diferentes "
        "sobrevivem. Padronize <b>primeiro</b>, deduplique <b>depois</b>.")
)

cad.section("p0-limpeza-colunas", "Limpeza 5: dividir, mesclar e colunas de exemplo",
    p("Nem sempre o dado chega no formato que precisamos. As três ferramentas abaixo resolvem quase "
      "todo caso: dividir uma coluna em duas, juntar duas colunas em uma, ou criar uma coluna nova a "
      "partir de um exemplo.") +
    tbl(["Ferramenta", "Onde", "Exemplo na base"],
        [["<b>Dividir Coluna</b>", "Transformar",
          "Separar <code>339014 - Diarias</code> em código e descrição."],
         ["<b>Mesclar Colunas</b>", "Transformar",
          "Juntar <code>municipio</code> + <code>uf</code> em <code>Municipio/UF</code>."],
         ["<b>Coluna de Exemplo</b>", "Adicionar Coluna",
          "Criar <code>Faixa de valor</code> (Baixo / Médio / Alto) digitando um exemplo."],
         ["<b>Coluna Condicional</b>", "Adicionar Coluna",
          "Marcar <code>Em atraso</code> quando o contrato já venceu."]],
        num_cols=[]) +
    step([
        ("Divida", "Em <code>dim_rubrica</code>: <b>Dividir Coluna &rarr; Por Delimitador &rarr; "
         "Personalizado &rarr; <code> - </code></b>. Renomeie para <code>codigo</code> e "
         "<code>rubrica</code>."),
        ("Mescle", "Em <code>dim_fornecedor</code>: selecione <code>municipio</code> e "
         "<code>uf</code> e use <b>Mesclar Colunas</b> com separador <code>/</code>."),
        ("Crie por exemplo", "<b>Adicionar Coluna &rarr; Coluna de Exemplo</b>: digite "
         "<code>Baixo</code> para um caso e o Power BI aprende a regra."),
    ]) +
    aplicab(
        "Quando a coluna certa para o visual simplesmente não existe na base.",
        "Porque criar colunas no Power Query é mais rápido (e mais seguro) que fazer isso na mão.",
        "Uma coluna <b>Faixa de valor</b> transforma 600 empenhos em três blocos (Baixo, Médio, "
        "Alto) e deixa o gráfico de distribuição legível.")
)

cad.section("p0-editor-avancado", "O Editor Avançado e o Fechar & Aplicar",
    p("Todo clique no Power Query escreve código na linguagem <b>M</b>. Você não precisa programar, "
      "mas espiar o <b>Editor Avançado</b> ajuda a entender e a reaproveitar a limpeza.") +
    code("""
        let
            Origem      = Excel.Workbook(File.Contents("...Orcamento_Contratos_SUJO.xlsx"), null, true),
            Aba         = Origem{[Item="fato_empenhos", Kind="Sheet"]}[Data],
            Cabecalho   = Table.PromoteHeaders(Aba, [PromoteAllScalars=true]),
            SemVazios   = Table.SelectRows(Cabecalho, each not List.IsEmpty(
                              List.RemoveMatchingItems(Record.FieldValues(_), {null, ""}))),
            Tipos       = Table.TransformColumnTypes(SemVazios,
                              {{"valor_empenhado", type number}, {"status_key", Int64.Type}}, "pt-BR")
        in
            Tipos
        """, "powerquery") +
    step([
        ("Veja o M", "<b>Página Inicial &rarr; Editor Avançado</b> mostra os passos que você criou."),
        ("Feche a oficina", "Quando terminar, clique em <b>Página Inicial &rarr; Fechar e Aplicar</b>."),
        ("Observe as etapas", "No painel <b>Etapas Aplicadas</b>, cada passo tem um nome. Clicar "
         "volta a versão da tabela naquele momento."),
    ]) +
    callout("tip", "Fechar & Aplicar é a assinatura do Power Query",
        "Ao clicar em <b>Fechar e Aplicar</b>, o Power BI executa a receita inteira e carrega o "
        "resultado no modelo. Na próxima atualização, ela roda sozinha — é a automação do Dia 4.")
)

cad.section("p0-modelo-relacionamentos", "O modelo: criando relacionamentos",
    p("Cada aba virou uma tabela no painel Dados. Mas elas estão <b>soltas</b>: por enquanto o Power "
      "BI não sabe que <code>fato_empenhos[setor_key]</code> conversa com "
      "<code>dim_setor[setor_key]</code>. O relacionamento é o que amarra tudo.") +
    step([
        ("Vá para Modelo", "Clique na visão <b>Modelo</b> (ícone do diagrama)."),
        ("Arraste a chave", "Arraste <code>dim_setor[setor_key]</code> até "
         "<code>fato_empenhos[setor_key]</code>. Aparece uma linha ligando as duas."),
        ("Confirme a direção", "A relação é <b>Muitos para Um (N:1)</b>: muitos empenhos para um "
         "setor, direção de filtro <b>Única</b>."),
        ("Ligue o resto", "Repita para todas as dimensões da lista abaixo."),
        ("Valide", "Crie uma matriz setor x valor empenhado e confira se as somas fazem sentido."),
    ]) +
    tbl(["Tabela fato", "Liga às dimensões por"],
        [["<code>fato_empenhos</code>", "dim_calendario, dim_contrato, dim_fornecedor, dim_setor, "
          "dim_rubrica, dim_modalidade, dim_fonte, dim_status_empenho"],
         ["<code>fato_dotacao</code>", "dim_setor, dim_rubrica (e o ano via dim_calendario)"]],
        num_cols=[]) +
    callout("err", "Tabela solta = número errado",
        "Sem relacionamento, o Power BI soma valores sem cruzar contexto. Você vê um total que não "
        "bate com nenhum filtro. Sempre confira a visão Modelo antes de confiar no painel.")
)

cad.section("p0-cardinalidade", "Cardinalidade e direção do filtro",
    p("Dentro de cada relacionamento há dois ajustes que decidem o comportamento do filtro. Duplo "
      "clique na linha do relacionamento para vê-los.") +
    tbl(["Ajuste", "Opções", "O que significa"],
        [["<b>Cardinalidade</b>", "Muitos para um (N:1)",
          "O caso normal: muitos fatos apontam para uma dimensão."],
         ["", "Um para um (1:1)", "Raro; evite — geralmente indica modelagem inadequada."],
         ["", "Muitos para muitos (N:N)", "Existe, mas exige cuidado; pode dar resultado ambíguo."],
         ["<b>Direção do filtro</b>", "Única",
          "O filtro corre da dimensão para a fato (o padrão correto)."],
         ["", "Cruzada (ambas)", "Permite filtro nos dois sentidos; use só quando necessário."]],
        num_cols=[]) +
    aplicab(
        "Ao revisar o modelo, antes de publicar.",
        "Porque uma direção cruzada indevida cria caminhos ambíguos e números inconsistentes.",
        "No painel de orçamento, todas as relações são N:1 com direção única: o filtro do setor "
        "desce para os empenhos, e a hierarquia de datas desce para a dotação.")
)

cad.section("p0-tabela-datas", "Criando e marcando a tabela de datas",
    p("Para usar funções de tempo (ano a ano, mês a mês, acumulado), o ideal é ter uma "
      "<b>tabela de datas</b> dedicada e contínua. Nosso <code>dim_calendario</code> já é isso: tem "
      "uma linha por dia, de 2024 a 2026, com ano, mês, trimestre e dia da semana.") +
    step([
        ("Abra a tabela", "Na visão Dados ou Modelo, clique com o botão direito em "
         "<code>dim_calendario</code>."),
        ("Marque como data", "Escolha <b>Marcar como Tabela de Data</b> e aponte a coluna "
         "<code>data</code>."),
        ("Use a hierarquia", "Nos visuais, use os campos <code>ano</code>, <code>trimestre</code>, "
         "<code>nome_mes</code> para construir eixos e matrizes temporais."),
        ("Ordene nome_mes", "Na visão Dados, selecione <code>nome_mes</code> &rarr; <b>Classificar "
         "por Coluna</b> &rarr; <code>mes</code>, para janeiro vir antes de fevereiro."),
    ]) +
    callout("tip", "Tabela de datas = tempo confiável",
        "Com a tabela marcada, o Power BI reconhece <i>tempo</i> de verdade e você evita erros de "
        "ano/mês que aparecem quando a única data é um field de fato.")
)

cad.section("p0-formatacao-campos", "Formatando campos: tipo, formato, resumo e ordenação",
    p("Antes de arrastar campos para os visuais, ajuste cada um na visão <b>Dados</b>. É aqui que o "
      "valor vira moeda, o número ganha casas decimais e o mês ordena corretamente.") +
    step([
        ("Escolha o campo", "Visão Dados, selecione uma coluna, por exemplo "
         "<code>valor_empenhado</code>."),
        ("Defina o formato", "Na faixa <b>Ferramentas de Coluna</b>, escolha <b>Moeda</b>, "
         "<b>R$ Português (Brasil)</b> e <b>2 casas decimais</b>."),
        ("Escolha o resumo", "No painel direito, em <b>Resumir por</b>, deixe <b>Soma</b> para "
         "valores e <b>Contagem</b> para chaves como <code>id_empenho</code>."),
        ("Ordene", "Para <code>nome_mes</code>, use <b>Classificar por Coluna &rarr; mes</b>."),
    ]) +
    callout("err", "Resumir a coluna errada",
        "Se <code>id_empenho</code> (que é texto) entrar como Soma, ou uma chave numérica como "
        "Soma, o visual mostra um número sem significado. Chave se <b>conta</b>; valor se <b>soma</b>.")
)

cad.section("p0-medidas-dax", "Medidas DAX essenciais",
    p("<b>Medidas</b> são cálculos que reagem ao contexto do visual (o filtro do setor, o mês "
      "selecionado). São o coração da inteligência do painel. Comece com sete medidas simples.") +
    code("""
        Total Empenhado      = SUM ( fato_empenhos[valor_empenhado] )
        Total Liquidado      = SUM ( fato_empenhos[valor_liquidado] )
        Total Pago           = SUM ( fato_empenhos[valor_pago] )
        Dotacao Atualizada   = SUM ( fato_dotacao[valor_atualizado] )
        % Execucao           = DIVIDE ( [Total Empenhado], [Dotacao Atualizada] )
        Saldo a Pagar        = [Total Liquidado] - [Total Pago]
        N. de Empenhos       = COUNTROWS ( fato_empenhos )
        """, "dax") +
    step([
        ("Nova medida", "Botão direito em <code>fato_empenhos</code> &rarr; <b>Nova medida</b>."),
        ("Escreva a fórmula", "Digite <code>Total Empenhado = SUM(fato_empenhos[valor_empenhado])</code>."),
        ("Formate", "Com a medida selecionada, aplique o formato de Moeda, R$ e 2 casas."),
        ("Repita", "Crie as demais medidas da lista."),
    ]) +
    callout("tip", "DIVIDE em vez de /",
        "Use sempre <b>DIVIDE(a, b)</b> em vez de <code>a/b</code>: ele já trata a divisão por zero "
        "sem estourar erro quando o filtro deixa o denominador vazio.")
)

cad.section("p0-colunas-calculadas", "Colunas calculadas e medidas: o que calcular",
    p("Enquanto a medida é recalculada <b>a cada visual</b>, a <b>coluna calculada</b> é materializada "
      "na tabela. Use coluna calculada quando o valor for por linha e não mudar de acordo com o filtro.") +
    code("""
        // Coluna calculada: classifica cada empenho por faixa de valor
        Faixa de Valor =
        SWITCH ( TRUE(),
            fato_empenhos[valor_empenhado] >= 300000, "Alto",
            fato_empenhos[valor_empenhado] >= 50000,  "Medio",
            "Baixo" )
        """, "dax") +
    grid2([
        ("Coluna calculada",
         "Uma linha da tabela, um resultado. Ex.: <i>Faixa de Valor</i>, <i>Ano do empenho</i>."),
        ("Medida",
         "Um agregado que responde ao filtro. Ex.: <i>Total Empenhado</i>, <i>% Execução</i>."),
    ]) +
    callout("note", "Qual usar?",
        "Precisa aparecer no eixo de um gráfico (categoria)? <b>Coluna calculada</b>. Precisa "
        "somar/contar dentro do visual? <b>Medida</b>.")
)

cad.section("p0-hierarquias", "Hierarquias e grupos (bins)",
    p("<b>Hierarquias</b> deixam você navegar do geral ao detalhe em um clique "
      "(Ano &rarr; Trimestre &rarr; Mês). <b>Grupos (bins)</b> transformam um número contínuo em "
      "faixas, como valores de R$ 0 a 50 mil, de 50 a 100 mil, etc.") +
    step([
        ("Crie a hierarquia", "Na visão Dados, arraste <code>ano</code> sobre "
         "<code>nome_mes</code> na tabela <code>dim_calendario</code> para criar "
         "<b>Calendário</b>."),
        ("Use nos visuais", "No gráfico de linha, use a hierarquia no eixo e clique na seta de "
         "expansão para <i>drill</i> de ano para mês."),
        ("Crie um grupo", "Botão direito em <code>valor_empenhado</code> &rarr; <b>Agrupar</b> &rarr; "
         "<b>Agrupar em faixas</b> &rarr; tamanho 50.000."),
    ]) +
    aplicab(
        "Quando o gestor quer 'ver por ano' e, se precisar, 'abrir por mês'.",
        "Porque a hierarquia entrega os dois níveis no mesmo visual, sem telas separadas.",
        "A evolução do empenhado no tempo abre de 2024 para os doze meses, mostrando em quais meses "
        "a execução acelerou.")
)

cad.section("p0-visuais-catalogo", "Catálogo de visuais: os 12 que resolvem quase tudo",
    p("O painel de <b>Visualizações</b> tem dezenas de opções, mas uma dúzia resolve praticamente "
      "todos os painéis de gestão. Conheça cada um com um exemplo na POLITEC.") +
    tbl(["Visual", "Pergunta que responde", "Exemplo no orçamento"],
        [["<b>Cartão</b>", "Qual o número agora?", "Total empenhado: R$ 185,6 mi."],
         ["<b>KPI</b>", "Atingiu a meta?", "% execução contra o esperado."],
         ["<b>Colunas</b>", "Compara categorias?", "Empenhado por setor."],
         ["<b>Barras</b>", "Ranking?", "Top 10 fornecedores."],
         ["<b>Linhas</b>", "Tendência?", "Empenhado mês a mês."],
         ["<b>Linhas e colunas</b>", "Duas escalas?", "Empenhado (coluna) x nº empenhos (linha)."],
         ["<b>Rosca / Pizza</b>", "Composição?", "Distribuição por modalidade."],
         ["<b>Treemap</b>", "Composição com área?", "Rubricas por volume gasto."],
         ["<b>Tabela</b>", "Detalhe em lista?", "Contratos com vigência e valor."],
         ["<b>Matriz</b>", "Cruzamento com totais?", "Setor x rubrica."],
         ["<b>Segmentação (Slicer)</b>", "Permite filtrar?", "Ano, setor, fonte."],
         ["<b>Mapa preenchido</b>", "Onde está?", "Fornecedores por município."]],
        num_cols=[]) +
    callout("tip", "Comece pelos cinco grandes",
        "Cartão, colunas, linhas, matriz e segmentação cobrem 80% de qualquer painel. Só adicione "
        "os demais quando houver uma pergunta que eles não respondem.")
)

cad.section("p0-visual-formatacao", "Formatando um visual e aplicando um tema",
    p("Um visual só comunica quando está legível. A formatação é o que separa um relatório amador de "
      "um profissional: título claro, cores com significado, rótulos de dados e eixos limpos.") +
    step([
        ("Selecione o visual", "Clique nele e vá ao painel <b>Formatar visual</b> (ícone do pincel)."),
        ("Dê um título", "Em <b>Título</b>, escreva a pergunta que o visual responde, por exemplo "
         "<b>Empenhado por setor (2024-2026)</b>."),
        ("Ligue os rótulos", "Em <b>Rótulos de dados</b>, ative para mostrar os valores sobre as barras."),
        ("Ajuste as cores", "Em <b>Barras</b>, escolha uma cor única ou defina cor por categoria."),
        ("Aplique um tema", "Em <b>Exibir &rarr; Temas</b>, escolha um tema; ou importe um tema "
         "institucional (JSON) com as cores da POLITEC."),
    ]) +
    callout("err", "Arco-íris de cores sem sentido",
        "Cor é informação, não decoração. Use uma cor única para comparação e reserve o vermelho "
        "para o que está fora do prazo ou acima do limite.")
)

cad.section("p0-interacoes", "Interações entre visuais, filtros e segmentações",
    p("No Power BI, os visuais já conversam entre si: clicar em um setor filtra os demais visuais "
      "da página. Você pode controlar <b>como</b> essa interação acontece.") +
    step([
        ("Adicione uma segmentação", "<b>Visualizações &rarr; Segmentação</b> e arraste o campo "
         "<code>ano</code>."),
        ("Teste", "Clique em 2024 e observe os outros visuais reagirem."),
        ("Edite as interações", "Selecione um visual e use <b>Formatar &rarr; Editar interações</b>. "
         "Você escolhe se o clique <i>filtra</i>, <i>destaca</i> ou <i>não faz nada</i>."),
        ("Use os filtros de nível", "No painel <b>Filtros</b>, aplique filtros no nível "
         "<b>visual</b>, <b>página</b> ou <b>relatório</b> inteiro."),
    ]) +
    callout("note", "Filtro x Segmentação",
        "A <b>segmentação</b> é um filtro <i>visível</i> para quem usa o painel. O painel de "
        "<b>Filtros</b> é um filtro fixo que você define e deixa 'escondido' no comportamento do visual.")
)

cad.section("p0-drill", "Drill down, drill through e a página de detalhes",
    p("<b>Drill</b> é descer do resumo para o detalhe. Há duas formas: expandir a hierarquia no "
      "próprio visual (<b>drill down</b>) e pular para uma página de detalhe mantendo o contexto "
      "(<b>drill through</b>).") +
    step([
        ("Drill down", "No gráfico com hierarquia Ano &rarr; Mês, clique na <b>seta para baixo</b> e "
         "depois em uma coluna para abrir aquele ano em meses."),
        ("Drill through", "Crie uma página, arraste <code>setor</code> para o campo "
         "<b>Drill through</b> no painel Filtros."),
        ("Volte", "No detalhe, o botão de <b>voltar</b> aparece no canto; ele restaura o contexto."),
    ]) +
    aplicab(
        "Quando o gestor vê um total alto e quer saber 'de que é feito esse número'.",
        "Porque o detalhe fica a um clique, sem poluir a visão geral.",
        "Do total empenhado do setor, o gestor desce para o mês, depois para o contrato e o "
        "fornecedor que puxaram o valor.")
)

cad.section("p0-formatacao-condicional", "Formatação condicional: cores, ícones e barras",
    p("A <b>formatação condicional</b> pinta a célula ou o valor conforme uma regra. É o que faz o "
      "dashboard 'gritar' quando um indicador sai do esperado — sem ninguém precisar ler os números.") +
    step([
        ("Abra o menu", "Em uma <b>Tabela</b> ou <b>Matriz</b>, vá em <b>Formatar &rarr; Células com "
         "formatação condicional</b>."),
        ("Escolha o tipo", "<b>Cor da tela de fundo</b>, <b>Cor da fonte</b>, <b>Ícones</b> ou "
         "<b>Barras de dados</b>."),
        ("Defina a regra", "Ex.: pintar de vermelho a <b>% de execução</b> abaixo de 50%."),
        ("Aplique", "Aplique ao campo de valor e veja as células reagirem."),
    ]) +
    callout("tip", "Semáforo de gestão",
        "Verde (dentro da meta), amarelo (atenção) e vermelho (crítico) transformam a matriz em um "
        "painel de alerta que o gestor entende em segundos.")
)

cad.section("p0-botoes-bookmarks", "Botões, formas, marcadores e navegação entre abas",
    p("Um dashboard com três abas precisa de <b>navegação</b>. Com botões e <b>marcadores "
      "(bookmarks)</b> você cria um menu que leva de uma aba a outra, com visual de aplicativo.") +
    step([
        ("Crie os botões", "<b>Inserir &rarr; Botões</b> e escolha <b>Navegador de página</b>."),
        ("Aponte o destino", "Selecione o botão e, em <b>Ação</b>, escolha <b>Navegação de página</b> "
         "e a aba de destino."),
        ("Formate", "Dê ao botão a cor institucional e o texto da aba: Visão Orçamentária, Setores, Contratos."),
        ("Use marcadores", "Em <b>Exibir &rarr; Marcadores</b>, salve estados (com ou sem filtro) e "
         "acione-os por botões."),
    ]) +
    code("""
        Inserir > Botões > Navegador de página
          Rótulo : Visão Orçamentária | Setores | Contratos
          Ação   : Navegação de página > <destino>
          Exibir : Marcadores (salvar estado da página)
        """, "powerbi") +
    callout("note", "Bookmark = foto da tela",
        "Um marcador guarda o estado de filtros e visibilidade de uma página. É a base de menus, "
        "de abas e de relatórios que se comportam como um aplicativo.")
)

cad.section("p0-analise-extras", "Análise extras: linhas de referência, previsão e tooltips",
    p("No painel <b>Analisar</b> (ao lado de Formatar) há recursos que enriquecem o visual sem "
      "escrever uma linha de DAX.") +
    ul([
        "<b>Linha de referência</b> — uma meta ou limite desenhado no gráfico (ex.: limite de R$ 1 mi).",
        "<b>Linha de tendência</b> — mostra se a série está subindo ou caindo.",
        "<b>Previsão</b> — projeta os próximos períodos com base no histórico.",
        "<b>Dicas de ferramenta (tooltips)</b> — o balão que aparece ao passar o mouse; pode receber "
        "um <i>página de dica</i> com um mini-relatório.",
        "<b>Obter mais visuais</b> — botão que abre o <b>AppSource</b>, a loja de visuais extras.",
    ]) +
    callout("tip", "Um mini-relatório no hover",
        "Uma <b>página de dica de ferramenta</b> transforma o passar do mouse sobre uma barra em um "
        "raio-x daquele item: contrato, fornecedor, valores. Impressiona pela profundidade.")
)

cad.section("p0-atalhos", "Atalhos e produtividade no Desktop",
    p("Quem monta painel com frequência ganha horas com alguns atalhos. Estes são os que mais usamos.") +
    tbl(["Atalho", "O que faz"],
        [["<kbd>Ctrl</kbd> + <kbd>Z</kbd>", "Desfazer a última ação no canvas."],
         ["<kbd>Ctrl</kbd> + <kbd>S</kbd>", "Salvar o arquivo <code>.pbix</code>."],
         ["<kbd>Ctrl</kbd> + <kbd>C</kbd> / <kbd>V</kbd>", "Copiar e colar um visual inteiro."],
         ["<kbd>Ctrl</kbd> + <kbd>clique</kbd>", "Selecionar vários visuais de uma vez."],
         ["<kbd>Alt</kbd> + arrastar", "Alinhar/copiar formatação entre visuais."],
         ["<kbd>Enter</kbd> (na fórmula)", "Quebra de linha para deixar o DAX legível."],
         ["<kbd>F4</kbd>", "Renomear a seleção (visual, página ou medida)."]],
        num_cols=[]) +
    callout("tip", "Nomeie as medidas em português",
        "Medidas como <b>Total Empenhado</b> (com espaço e acento) aparecem bonitas nos cartões. "
        "O nome técnico fica na fórmula; o rótulo, para o gestor.")
)

cad.section("p0-tres-abas", "Mão na massa: o plano das 3 abas",
    p("Chegou a hora de montar o painel. São três páginas, cada uma respondendo a um bloco de "
      "perguntas de gestão. Use as medidas DAX já criadas e o modelo relacionado.") +
    flow_h([
        ("📊", "Aba 1 · Orçamentária"),
        ("🏢", "Aba 2 · Setores e rubricas"),
        ("📄", "Aba 3 · Contratos"),
    ]) +
    tbl(["Aba", "Pergunta central", "Visuais principais"],
        [["<b>1 · Visão Orçamentária</b>", "Quanto foi orçado, empenhado, liquidado e pago?",
          "5 cartões de KPI, colunas por ano, linha mensal, segmentações de ano e fonte."],
         ["<b>2 · Setores e Rubricas</b>", "Quem executa mais e em quê? Onde há saldo?",
          "Barras por setor, matriz setor x rubrica, treemap de rubricas, KPI de % execução."],
         ["<b>3 · Contratos e Fornecedores</b>", "Quais contratos e fornecedores concentram gasto?",
          "Top 10 fornecedores, tabela de contratos, rosca por modalidade, mapa por município."]],
        num_cols=[]) +
    callout("note", "Uma página por bloco mental",
        "Cada aba responde perguntas de um mesmo 'dono': a Diretoria olha a aba 1, o chefe de setor "
        "olha a aba 2, a área de contratos olha a aba 3.")
)

cad.section("p0-aba1", "Aba 1 - Visão Orçamentária (Orçado x Empenhado x Pago)",
    p("A primeira aba responde, em cinco segundos, 'como está o orçamento'. Comece pelos cartões de "
      "KPI no topo e desça para as tendências.") +
    step([
        ("Cinco cartões", "<b>Cartão</b> para <i>Dotação Atualizada</i>, <i>Total Empenhado</i>, "
         "<i>Total Liquidado</i>, <i>Total Pago</i> e <i>% Execução</i>."),
        ("Colunas por ano", "<b>Colunas Clusterizadas</b> com <code>ano</code> no eixo e as medidas "
         "<i>Empenhado</i>, <i>Liquidado</i> e <i>Pago</i> nos valores."),
        ("Linha mensal", "<b>Gráfico de Linhas</b> com <code>nome_mes</code> no eixo e "
         "<i>Total Empenhado</i> nos valores, drill de ano para mês."),
        ("Segmentações", "Duas <b>Segmentações</b>: <code>ano</code> e <code>fonte</code>."),
        ("Título e tema", "Título da página <b>Visão Orçamentária - POLITEC</b> e tema institucional."),
    ]) +
    kpi([
        ("R$ 257,0 mi", "Dotação atualizada"),
        ("R$ 185,6 mi", "Empenhado"),
        ("R$ 119,8 mi", "Liquidado"),
        ("R$ 91,5 mi", "Pago"),
        ("72,2%", "% Execução"),
    ]) +
    callout("err", "Confundir empenhado com pago",
        "Empenhar é reservar; pagar é desembolsar. Um empenho de R$ 500 mil pode ter R$ 0 pago. "
        "Deixe as três colunas lado a lado para a diferença ficar óbvia.")
)

cad.section("p0-aba2", "Aba 2 - Execução por Setor e Rubrica",
    p("A segunda aba mostra <b>quem</b> gasta e <b>em quê</b>. É a página que responde 'onde está o "
      "dinheiro' e 'onde ainda há saldo para executar'.") +
    step([
        ("Barras por setor", "<b>Barras Clusterizadas</b> com <code>setor</code> no eixo e "
         "<i>Total Empenhado</i> nos valores, ordenado do maior para o menor."),
        ("Matriz de detalhe", "<b>Matriz</b> com <code>setor</code> nas linhas, <code>rubrica</code> "
         "nas colunas e <i>Total Empenhado</i> nos valores."),
        ("Treemap", "<b>Treemap</b> com <code>rubrica</code> na categoria e <i>Total Empenhado</i>."),
        ("KPI de execução", "<b>Cartão</b> com a medida <i>% Execução</i> e <b>formatação "
         "condicional</b> (vermelho abaixo de 50%)."),
        ("Segmentação", "<b>Segmentação</b> de <code>setor</code> e <code>grupo</code> "
         "(Custeio x Investimento)."),
    ]) +
    aplicab(
        "Na reunião de planejamento, para priorizar o remanejamento de recursos.",
        "Porque mostra em um só lugar o setor que executa e a rubrica com saldo sobrando.",
        "A matriz revela que um laboratório tem saldo alto em 'Equipamentos' e baixo em 'Material de "
        "Consumo' — insumo direto para remanejar verba dentro do exercício.")
)

cad.section("p0-aba3", "Aba 3 - Contratos e Fornecedores",
    p("A terceira aba dá visibilidade à <b>rede de contratos</b>: com quem a instituição gasta, por "
      "qual modalidade e por qual preço. É a página de governança e transparência.") +
    step([
        ("Top fornecedores", "<b>Barras</b> com <code>razao_social</code> no eixo e "
         "<i>Total Empenhado</i>, mostrando o <b>Top 10</b>."),
        ("Tabela de contratos", "<b>Tabela</b> com <code>numero</code>, <code>objeto</code>, "
         "<code>data_inicio</code>, <code>data_fim</code>, <code>valor_contrato</code> e o total "
         "empenhado do contrato."),
        ("Rosca por modalidade", "<b>Gráfico de Rosca</b> com <code>modalidade</code> e a contagem "
         "de empenhos ou o valor."),
        ("Mapa de fornecedores", "<b>Mapa Preenchido</b> com <code>municipio</code> e "
         "<i>Nº de Empenhos</i>."),
        ("Segmentações", "<b>Segmentação</b> de <code>porte</code> e <code>modalidade</code>."),
    ]) +
    callout("tip", "Contratos a vencer",
        "Adicione um cartão com a contagem de contratos cujo <code>data_fim</code> cai nos próximos "
        "90 dias. É um alerta de gestão que evita interrupção de serviço.")
)

cad.section("p0-erros", "Erros de iniciante e como evitá-los",
    p("Quase todo primeiro painel tropeça nos mesmos pontos. Conhecer a lista evita retrabalho.") +
    antesdepois(
        "Importar tudo, modelar depois, corrigir no visual: modelo sujo e número errado.",
        "Limpar no Power Query, relacionar no Modelo e só então desenhar o visual.") +
    tbl(["Erro", "Consequência", "Como evitar"],
        [["Somar chaves em vez de contar", "Número sem sentido", "Chave se <b>conta</b>"],
         ["Deixar linha TOTAL GERAL", "Soma dobrada", "Filtrar/remover antes de carregar"],
         ["Tabelas sem relacionamento", "Filtros não cruzam", "Criar as relações N:1 no Modelo"],
         ["Datas como texto", "Eixo temporal quebrado", "Tipo Data + localidade pt-BR"],
         ["Valor como texto", "Cartões mostram contagem", "Converta para decimal"],
         ["Cores aleatórias", "Leitura difícil", "Cor única ou com significado"]],
        num_cols=[]) +
    callout("err", "Publicar sem conferir",
        "Antes de publicar, valide os totais contra uma fonte conhecida (aqui, o gabarito "
        "<code>Orcamento_Contratos_LIMPO.xlsx</code>) e verifique se não há dado sensível na tela.")
)

cad.section("p0-salvar", "Salvando o .pbix e indo para a publicação",
    p("Seu painel existe só na sua tela até você salvar. O arquivo <b>.pbix</b> guarda o modelo, os "
      "dados importados, os visuais e as medidas — é o projeto inteiro do relatório.") +
    step([
        ("Salve", "<b>Arquivo &rarr; Salvar como</b> e grave como "
         "<code>Painel_Orcamento_Contratos.pbix</code>."),
        ("Confira", "Reabra o arquivo: os dados, as relações e as 3 abas devem continuar lá."),
        ("Prepare a publicação", "Só publique depois de revisar a aba <b>1</b>, <b>2</b> e <b>3</b> e "
         "checar se há dado pessoal ou sensível à mostra."),
        ("Publique", "<b>Página Inicial &rarr; Publicar</b> e escolha o workspace "
         "(a Parte 2 deste caderno detalha o Service)."),
    ]) +
    checklist([
        "As 10 tabelas foram limpas e as chaves são números inteiros.",
        "Todos os relacionamentos N:1 estão criados no Modelo.",
        "As medidas DAX estão formatadas como moeda e porcentagem.",
        "As 3 abas estão construídas, com títulos e segmentações.",
        "Os totais batem com o gabarito LIMPO (empenhado ~ R$ 185,6 mi).",
        "Não há coluna de dado pessoal visível no painel.",
        "O arquivo <code>.pbix</code> foi salvo.",
    ]) +
    callout("note", "Daqui em diante",
        "Com o painel salvo, siga para a <b>Parte 1</b> (conceitos e interface), a <b>Parte 2</b> "
        "(publicação e governança) e a <b>Parte 3</b> (laboratórios) para aprofundar.")
)

cad.section("p0-quiz", "Quiz do iniciante em Power BI Desktop",
    p("Responda e confira o gabarito. São os conceitos que você mais vai usar no dia a dia.") +
    q("Qual botão abre a oficina de limpeza antes de carregar os dados?",
      ["Carregar", "Transformar Dados", "Publicar", "Atualizar"], 1,
      "Transformar Dados abre o Power Query, onde o dado é limpo antes de entrar no modelo.") +
    q("Uma coluna de valores aparece como 'R$ 95.824,77'. O que fazer para poder somá-la?",
      ["Nada, o Power BI soma texto", "Formatar como moeda na visão Dados",
       "Substituir R$ e espaços, tratar parênteses e converter para Número Decimal (pt-BR)",
       "Criar um relacionamento"], 2,
      "Texto não soma. Remova os símbolos, trate negativos e converta o tipo com localidade pt-BR.") +
    q("Na visão Modelo, qual é a cardinalidade típica entre fato e dimensão?",
      ["Um para um", "Muitos para muitos", "Muitos para um (N:1)", "Nenhuma"], 2,
      "Muitos fatos apontam para uma dimensão: Muitos para Um, direção de filtro única.") +
    q("O que acontece se você publicar com uma linha 'TOTAL GERAL' na base?",
      ["Nada muda", "O total é somado junto, dobrando o valor",
       "O Power BI remove sozinho", "A publicação falha"], 1,
      "A linha de total entra como se fosse um registro e dobrando a soma. Remova-a no Power Query.") +
    q("Para criar um cálculo que responde ao filtro (por setor, por mês), o que usar?",
      ["Uma coluna calculada", "Uma medida DAX", "Um relacionamento", "Um tema"], 1,
      "A medida é recalculada no contexto do visual. A coluna calculada é fixa por linha.") +
    q("Um contrato tem data_inicio como '01/05/2024'. Sem localidade pt-BR, o que pode acontecer?",
      ["Nada", "O Power BI lê como 5 de janeiro (mm/dd)",
       "A data vira texto", "O arquivo corrompe"], 1,
      "Sem pt-BR, o padrão é mm/dd e o dia 05/01 vira maio. Sempre configure a localidade.") +
    q("Qual recurso guarda uma 'foto' do estado de filtros de uma página para menus e abas?",
      ["Segmentação", "Marcador (bookmark)", "Drill through", "Filtro de relatório"], 1,
      "Marcadores salvam o estado da página e alimentam menus e navegação entre abas.") +
    q("Qual é o formato nativo do projeto do relatório, que guarda modelo, dados e visuais?",
      [".xlsx", ".csv", ".pbix", ".json"], 2,
      "O .pbix é o arquivo do projeto do Power BI Desktop.")
)

cad.section("p0-referencias", "Referências para continuar",
    p("Se quiser aprofundar cada recurso apresentado, estas são as fontes oficiais que valem o tempo.") +
    glossary([
        ("Documentação Power BI", "learn.microsoft.com/power-bi — guias oficiais de Desktop, Power "
         "Query e DAX."),
        ("Power Query (linguagem M)", "Referência oficial das transformações usadas na limpeza."),
        ("DAX", "learn.microsoft.com/dax — funções SUM, DIVIDE, CALCULATE e boas práticas."),
        ("Comunidade Power BI", "community.powerbi.com — fóruns com respostas da comunidade e da Microsoft."),
        ("AppSource", "Loja de visuais personalizados acessível por Obter mais visuais."),
        ("Gabarito do exercício", "<code>datasets/orcamento/Orcamento_Contratos_LIMPO.xlsx</code> — "
         "conferência do resultado esperado."),
    ]) +
    callout("tip", "Pratique com o gabarito",
        "Repita o exercício partindo do arquivo <b>LIMPO</b> e compare com o que você obteve limpando "
        "o <b>SUJO</b>. A diferença entre os dois é exatamente o que você aprendeu nesta parte.")
)

# =================================================================
# PARTE 1 - MODULO 6 PARTE 1
# =================================================================
cad.grp("Parte 1 · Modulo 6 - Interface e Primeiros Relatorios",
        "Manha: o conceito de BI, a arquitetura do Power BI, a conexao de dados e o primeiro dashboard.")

cad.section("o-que-e-bi", "O que e Business Intelligence na pericia criminal",
    p("<b>Business Intelligence (BI)</b> e o conjunto de tecnologias e processos que transforma "
      "dados brutos de requisicoes, laudos e estoque em <b>informacoes estrategicas</b> para a "
      "gestao do laboratorio e do IML. A definicao classica foi cunhada por <b>Howard Dresner</b>, "
      "analista da <b>Gartner</b>, em <b>1989</b>.") +
    ficha("p", "A definicao de Dresner (Gartner, 1989)",
        "'BI e a aplicacao de conhecimento sobre dados para melhorar a performance da organizacao.'") +
    aplicab(
        "Na pericia criminal, quando o gestor precisa decidir onde alocar peritos, o que comprar e qual fila priorizar.",
        "Porque o BI nao e um relatorio estatico: ele cruza requisicoes, laudos e insumos e mostra a relacao entre producao, prazo e custo.",
        "Na POLITEC/MT, o BI permite <b>conhecer os dados de producao pericial</b> para otimizar a "
        "alocacao de peritos e a compra de insumos com precisao e embasamento tecnico.") +
    callout("err", "BI nao e 'fazer grafico bonito'",
        "Confundir BI com decoracao visual e o erro numero um. BI e responder a perguntas de gestao "
        "com dado confiavel. Um cartao com um numero certo vale mais que dez graficos vistosos.")
)

cad.section("excel-vs-powerbi", "Excel x Power BI: qual a diferenca",
    p("Excel e Power BI <b>nao competem</b>: eles cumprem papeis diferentes na rotina da pericia. "
      "Entender essa divisao evita tanto o uso errado da planilha quanto a expectativa errada do BI.") +
    tbl(["Criterio", "Excel", "Power BI"],
        [["Papel", "Ferramenta de <b>calculo e controle diario</b> do perito.", "Plataforma de <b>inteligencia corporativa</b> para a direcao."],
         ["Exemplo POLITEC", "Planilha de controle de estoque de reagentes na Toxicologia.", "Painel de <b>backlog, TAT e produtividade</b> em tempo real para o Diretor e o Secretario."],
         ["Escopo", "Trabalho <b>individual e rotineiro</b> de cada analista.", "Decisao <b>gerencial e estrategica</b>, com dados consolidados de toda a instituicao."],
         ["Atualizacao", "Manual, por arquivo e por pessoa.", "Agendada e automatica na nuvem."],
         ["Acesso", "Arquivo local ou compartilhado.", "Link/tela na nuvem, com controle de quem ve o que."]],
        num_cols=[]) +
    antesdepois(
        "Manter tudo em uma planilha unica compartilhada por e-mail, gerando versoes concorrentes.",
        "Planilha para a entrada e a conferencia do dado; Power BI para a leitura consolidada da gestao.",
        "Uso errado", "Uso certo") +
    callout("tip", "A regra da casa",
        "Planilha e a <b>bancada</b>; Power BI e a <b>sala de controle</b>. O dado nasce e e conferido "
        "na planilha; a decisao estrategica acontece no dashboard.")
)

cad.section("tres-pilares", "A arquitetura do Power BI: os 3 pilares",
    p("Todo o ecossistema Power BI se organiza em tres pecas que conversam entre si. Saber onde cada "
      "uma vive e o primeiro passo para nao se perder entre o arquivo local e a nuvem.") +
    legenda([
        ("\U0001f5a5", "Power BI Desktop - Autoria",
         "Onde voce <b>cria</b> os relatorios. Gratuito, instalado no PC do analista ou perito responsavel. E o seu local de trabalho."),
        ("\u2601", "Power BI Service - Nuvem",
         "Onde voce <b>publica, compartilha e colabora</b> com toda a equipe. Acessado em app.powerbi.com."),
        ("\U0001f4f1", "Power BI Mobile - Mobilidade",
         "App para o Diretor ou o Chefe de Setor <b>consultar o backlog no celular</b>, em qualquer lugar e horario."),
    ]) +
    ficha("a", "Gratuito ate a hora de compartilhar",
        "O <b>Power BI Desktop e 100% gratuito</b>. A instituicao so paga quando precisa "
        "compartilhar relatorios de forma <b>privada e segura</b> na nuvem (licenca Pro ou Premium).") +
    callout("note", "Analogia util",
        "Pense no Desktop como a <b>oficina</b> (onde se constroi), no Service como a <b>vitrine "
        "institucional</b> (onde se exibe com controle) e no Mobile como o <b>bolso do gestor</b>.")
)

cad.section("ben-brumfield", "Autor referencia: Ben Brumfield, o 'Pai do Power BI'",
    p("Conhecido como o <b>'Pai do Power BI'</b> na Microsoft, <b>Ben Brumfield</b> liderou o time "
      "que transformou o antigo <b>Project Crescent</b> no Power BI moderno entre <b>2013 e 2015</b>.") +
    ficha("p", "A frase que define o espirito do produto",
        "'Queriamos colocar o poder da analise de dados nas maos de qualquer pessoa, nao apenas de "
        "programadores de TI.' - Ben Brumfield.") +
    aplicab(
        "Sempre que um perito ou analista administrativo precisa construir seus proprios paineis.",
        "Porque o legado de Brumfield e a <b>democratizacao do BI</b>: o dado deixa de ser refem de uma equipe de TI.",
        "Na POLITEC, o proprio analista do laboratorio monta o painel do seu setor, sem abrir um "
        "chamado para o time de tecnologia.") +
    callout("tip", "O que isso muda na pratica",
        "Se voce sabe usar planilha, ja conhece os conceitos: tabelas, colunas, filtros e formulas. "
        "O Power BI troca a digitacao de celulas pelo <b>arrastar de campos</b>.")
)

cad.section("interface-cockpit", "A interface do Power BI Desktop: o cockpit",
    p("O Desktop lembra o pacote Office. Quem ja usou Excel reconhece a organizacao. A tela se divide "
      "em tres regioes principais: a <b>Faixa de Opcoes</b>, o <b>Painel de Dados</b> e a "
      "<b>Area Central</b>.") +
    tbl(["Regiao", "O que contem", "Para que serve"],
        [["<b>Faixa de Opcoes (Ribbon)</b>", "Abas <i>Pagina Inicial</i>, <i>Modelagem</i>, <i>Exibicao</i>.",
          "Agrupa todas as ferramentas de criacao, de 'Obter Dados' ate a formatacao."],
         ["<b>Painel de Dados (direita)</b>", "Suas <b>Tabelas e Colunas</b> (ex.: <code>Tabela_Laudos</code>), os tipos de visualizacao e os filtros.",
          "Escolher campos, definir tipos e montar os visuais."],
         ["<b>Area Central</b>", "O <b>canvas</b> do relatorio e as vistas de dados/modelo.",
          "Onde os graficos sao desenhados e onde as tabelas se relacionam."]],
        num_cols=[]) +
    callout("note", "Sem medo da tela cheia",
        "O Desktop tem muita coisa visivel, mas voce usara poucos botoes no dia a dia. Comece por "
        "<b>Obter Dados</b> e pelo <b>painel de Visualizacoes</b>.")
)

cad.section("modos-do-desktop", "Os 3 modos da area central: Relatorio, Tabela e Modelo",
    p("No topo da area central, tres icones alternam o modo de trabalho do Desktop. Cada modo mostra "
      "uma face diferente do mesmo trabalho: a apresentacao, o dado e as relacoes.") +
    grid2([
        ("\U0001f4ca Relatorio (Report)",
         "Onde se monta os graficos e o dashboard final. E o modo de apresentacao, o que o gestor ve."),
        ("\U0001f4cb Tabela (Data)",
         "Exibe os <b>dados brutos</b> das requisicoes, linha a linha. Serve para conferir o que foi importado."),
        ("\U0001f517 Modelo (Model)",
         "Conecta tabelas relacionadas. Exemplo: <b>ID do Perito</b> na tabela de laudos ligado a uma tabela de peritos."),
    ]) +
    aplicab(
        "Ao alternar entre construir o visual, conferir o dado e ajustar relacionamentos.",
        "Porque entender o dado <b>antes</b> de desenhar evita graficos errados por campo equivocado.",
        "Ao importar as tabelas de <code>datasets/</code>, vale abrir o modo <b>Tabela</b> e conferir "
        "se as datas chegaram como data e as chaves como numero inteiro.") +
    callout("err", "Grafico 'bonito' com dado errado",
        "Muita gente so usa o modo Relatorio. Resultado: descobre tarde que a coluna escolhida estava "
        "com tipo de dados errado. Confira sempre no modo <b>Tabela</b> antes de confiar no visual.")
)

cad.section("conexao-dados", "Conexao de dados: o primeiro passo de tudo",
    p("Um dashboard e tao bom quanto o dado que o alimenta. O Power BI se conecta nativamente a "
      "<b>mais de 100 fontes de dados diferentes</b> — de um simples CSV a bancos corporativos e "
      "servicos de nuvem.") +
    flow_h([
        ("\U0001f4e5", "Obter Dados"),
        ("\U0001f50c", "Escolher fonte"),
        ("\U0001f50d", "Pre-visualizar"),
        ("\U0001f4be", "Carregar"),
    ]) +
    ficha("g", "Por que isso importa tanto",
        "A conexao correta define a <b>confiabilidade</b> do painel. Conectar a fonte oficial (o "
        "sistema de gestao de laudos) e melhor que copiar numeros manualmente para uma planilha.") +
    callout("tip", "Comece pela fonte oficial",
        "Sempre que existir, prefira a fonte <b>oficial e atualizada</b>. Quanto menos copiar-colar "
        "manual entre a fonte e o Power BI, menor o risco de erro.")
)

cad.section("fontes-politec", "Fontes de dados comuns na POLITEC/MT",
    p("Das mais de 100 fontes suportadas, tres familias concentram o dia a dia da POLITEC: "
      "<b>arquivos</b>, <b>bancos de dados</b> e <b>nuvem</b>.") +
    tbl(["Familia", "Exemplos", "Observacao POLITEC"],
        [["<b>Arquivos</b>", "Excel (.xlsx), CSV exportados e PDFs digitalizados.",
          "O ponto de entrada mais comum. Ideal para bases de laboratorio e historicos."],
         ["<b>Banco de dados</b>", "SQL Server e Oracle.",
          "Muitos sistemas legados de pericia operam em bancos relacionais e podem ser conectados direto."],
         ["<b>Nuvem</b>", "SharePoint, OneDrive e Dataverse.",
          "Integracao nativa com o ecossistema Microsoft, muito usado em ambientes governamentais."]],
        num_cols=[]) +
    aplicab(
        "Ao escolher de onde o painel vai puxar o dado.",
        "Porque a fonte define a frequencia de atualizacao e o nivel de automacao possivel.",
        "Estoque de reagentes costuma nascer em <b>planilha Excel</b>; o backlog oficial, em "
        "<b>SQL Server</b>; e a colaboracao entre setores, no <b>SharePoint/OneDrive</b>.") +
    callout("err", "Conectar a copia, nao a fonte",
        "Conectar o Power BI a uma planilha intermediaria que alguem atualiza a mao cria um painel "
        "que envelhece rapido. Aponte para a <b>fonte</b> ou automatize a atualizacao.")
)

cad.section("importacao-vs-directquery", "Importacao x DirectQuery: historico x tempo real",
    p("Ha dois modos centrais de trazer o dado para o Power BI. A escolha muda <b>desempenho</b>, "
      "<b>frequencia</b> e <b>dependencia de infraestrutura</b>.") +
    tbl(["Aspecto", "Importacao", "DirectQuery"],
        [["Como funciona", "Copia os dados <b>para dentro</b> do Power BI.", "Consulta o banco <b>em tempo real</b>, sem copiar localmente."],
         ["Desempenho", "Processamento mais <b>rapido</b>.", "Depende da rede e do banco."],
         ["Uso ideal", "Analise de <b>historico</b> de laudos emitidos.", "Painel de <b>entrada de requisicoes</b> que exige dado ao vivo."],
         ["Requisito", "Nenhum alem do arquivo/fonte.", "Conexao <b>estavel</b> e banco bem estruturado."]],
        num_cols=[]) +
    grid2([
        ("Quando preferir Importacao",
         "Backlog, TAT medio, producao mensal, custo por setor — indicadores de <b>historico</b>. "
         "A resposta rapida agrada e o dado muda pouco ao longo do dia."),
        ("Quando preferir DirectQuery",
         "Fila de entrada em tempo real no IML, com dezenas de requisicoes chegando por hora. Exige "
         "banco organizado e rede confiavel."),
    ]) +
    callout("tip", "Regra de bolso",
        "Se a pergunta for 'como estamos hoje?', pense em <b>DirectQuery</b>. Se for 'como "
        "evoluimos?', use <b>Importacao</b>. Na duvida, comece por Importacao: e mais simples e rapido.")
)

cad.section("caso-integracao-brasil", "Caso real: integracao de dados forenses no Brasil",
    p("Secretarias de Seguranca de estados como <b>Sao Paulo e Ceara</b> integraram bancos de dados "
      "da <b>Policia Civil, Policia Militar e Pericia</b> usando ferramentas de BI.") +
    step([
        ("O problema", "Cada corporacao tinha seu proprio sistema, e o gestor enxergava a seguranca "
                       "publica em fragmentos."),
        ("A integracao", "Com BI, os bancos foram reunidos em um <b>unico painel</b>. O Secretario "
                         "passou a ver nao apenas o numero de prisoes, mas o <b>tempo real de espera "
                         "pelo laudo de DNA</b> que embasava cada caso."),
        ("O insight", "A pericia deixou de ser linha de custo e passou a ser <b>parte visivel da "
                      "cadeia de resultado</b> da seguranca publica."),
    ]) +
    ficha("g", "Licao para MT",
        "A POLITEC pode consumir dados do <b>SINESP</b> ou do sistema interno para criar paineis "
        "que mostrem o <b>impacto direto da pericia</b> na elucidacao de crimes.") +
    callout("note", "TAT ao lado de prisoes",
        "Quando o TAT do DNA aparece <b>ao lado</b> do numero de prisoes, a sociedade entende que "
        "demora no laudo significa demora na justica.")
)

cad.section("cole-knaflic", "Autor referencia: Cole Nussbaumer Knaflic e os 5 segundos",
    p("Autora de <b>'Storytelling com Dados' (2015)</b>, Cole Nussbaumer Knaflic ensinou toda uma "
      "geracao de analistas a comunicar dados com clareza. Seu legado no curso e o <b>Principio dos "
      "5 segundos</b>.") +
    ficha("p", "A frase que guia o dashboard",
        "'Dados sem contexto sao apenas numeros. Dados com historia sao decisoes.' - Cole "
        "Nussbaumer Knaflic.") +
    aplicab(
        "Ao desenhar qualquer pagina do dashboard pericial.",
        "Porque o gestor nao quer ver 50 graficos: ele quer a resposta a pergunta principal em 5 segundos.",
        "O Diretor abre o painel e, em 5 segundos, entende: <b>'Qual setor esta com o TAT mais "
        "critico hoje?'</b>. Simplicidade e clareza valem mais que sofisticacao visual.") +
    callout("err", "Sofisticacao que atrapalha",
        "Graficos 3D, gradientes e efeitos podem parecer modernos, mas escondem a informacao. "
        "Simplicidade vence: e o principio dos 5 segundos.")
)

cad.section("fluxo-dashboard", "Construindo o primeiro dashboard: o fluxo da POLITEC",
    p("Objetivo pratico do dia: criar um painel de <b>'Gestao de Backlog e TAT'</b> usando uma base "
      "simulada de requisicoes periciais. Sao seis etapas encadeadas.") +
    flow_h([
        ("\U0001f4e5", "Obter Dados"),
        ("\U0001f527", "Transformar"),
        ("\U0001f4be", "Carregar"),
        ("\U0001f4ca", "Criar Visuais"),
        ("\U0001f3a8", "Formatar"),
        ("\u2601", "Publicar"),
    ]) +
    step([
        ("Obter Dados", "Obter Dados \u2192 Texto/CSV (ou Pasta) \u2192 selecionar os "
         "<code>fato_*</code> e <code>dim_*</code> de <code>datasets/</code>."),
        ("Transformar", "No Power Query, ajustar tipos: datas como data, chaves como numero inteiro."),
        ("Carregar", "Fechar e Aplicar para trazer as tabelas ao modelo e criar os relacionamentos."),
        ("Criar Visuais", "Arrastar campos para os eixos e montar os graficos."),
        ("Formatar", "Cores, titulos e layout para leitura em 5 segundos."),
        ("Publicar", "Enviar o relatorio ao Power BI Service, no workspace correto."),
    ]) +
    callout("note", "Uma etapa de cada vez",
        "Nao tente fazer tudo em um clique. O fluxo e sequencial: dado limpo primeiro, visual depois. "
        "Pular a transformacao contamina todo o painel.")
)

cad.section("obter-dados", "Passo 1: Obter Dados das tabelas do modelo",
    p("A primeira acao concreta do dia. O Power BI le os arquivos de <code>datasets/</code> e mostra "
      "uma pre-visualizacao antes de importar. Agora sao varias tabelas: as quatro <code>fato_*</code> "
      "e as dez <code>dim_*</code>.") +
    step([
        ("Abra o Desktop", "Power BI Desktop \u2192 <kbd>Pagina Inicial</kbd> \u2192 "
         "<kbd>Obter Dados</kbd> \u2192 <kbd>Texto/CSV</kbd> (ou <i>Pasta</i>, para carregar todas de uma vez)."),
        ("Aponte para a pasta", "Selecione a pasta <code>datasets/</code> da aula. O Power BI lista os "
         "arquivos <code>.csv</code>."),
        ("Confira o delimitador", "Ponto e virgula como separador e codificacao UTF-8. Verifique a "
         "pre-visualizacao das colunas antes de combinar."),
        ("Fato ou dimensao", "O prefixo indica o papel: <code>fato_*</code> guarda os eventos; "
         "<code>dim_*</code> guarda os rotulos (setor, tipo de exame, perito)."),
        ("Transformar ou Carregar", "Se o dado ja esta limpo (os CSVs sao padronizados), clique em "
         "<b>Carregar</b>. Se precisar ajustar tipos, clique em <b>Transformar Dados</b>."),
    ]) +
    code("""
        Pagina Inicial > Obter Dados > Texto/CSV (ou Pasta)
        Pasta: datasets/
        Fato : fato_requisicoes.csv, fato_movimentacao.csv,
               fato_produtividade.csv, fato_orcamento.csv
        Dim  : dim_calendario.csv, dim_setor.csv, dim_tipo_exame.csv,
               dim_perito.csv, dim_delegacia.csv, dim_status.csv,
               dim_reagente.csv, dim_fornecedor.csv,
               dim_tipo_movimentacao.csv, dim_rubrica.csv
        Botoes: Transformar Dados  |  Carregar
        """, "powerbi") +
    callout("err", "Nao importe as fontes planas junto",
        "As bases <code>requisicoes_periciais.csv</code> e demais ja estao representadas no modelo. "
        "Carregar as duas versoes gera tabelas duplicadas e confunde os relacionamentos.")
)

cad.section("power-query-limpeza", "Passo 2: Transformar no Power Query",
    p("O <b>Power Query</b> e o motor de limpeza e transformacao do Power BI. Nos CSVs do modelo o "
      "dado ja vem padronizado; aqui o trabalho e <b>conferir tipos</b> e corrigir o que o sistema "
      "legado costuma exportar errado.") +
    tbl(["Problema na base", "Acao no Power Query", "Resultado"],
        [["Datas como texto", "<i>Transformar</i> \u2192 tipo <b>Data</b>.",
          "O calculo de DATEDIFF/DAX passa a funcionar."],
         ["Chaves como texto", "<i>Transformar</i> \u2192 tipo <b>Numero Inteiro</b>.",
          "O relacionamento fato x dimensao liga corretamente."],
         ["Linha 'Total Geral' no fim", "<i>Remover Linhas</i> \u2192 <i>Remover Linhas Filtradas</i>.",
          "A base deixa de somar o total como se fosse um setor."]],
        num_cols=[]) +
    code("""
        let
            Origem   = Csv.Document(File.Contents("datasets\\fato_requisicoes.csv"),
                           [Delimiter=";", Encoding=65001]),
            Cabecalho = Table.PromoteHeaders(Origem, [PromoteAllScalars=true]),
            TiposOk  = Table.TransformColumnTypes(Cabecalho,
                           {{"data_recebimento_key", Int64.Type},
                            {"data_laudo_key", Int64.Type},
                            {"dias_uteis", Int64.Type}, {"em_atraso", Int64.Type}})
        in
            TiposOk
        """, "powerquery") +
    callout("tip", "Fechar e Aplicar",
        "Ao terminar, clique em <kbd>Pagina Inicial</kbd> \u2192 <kbd>Fechar e Aplicar</kbd>. As "
        "transformacoes sao gravadas como uma <b>receita</b>: na proxima atualizacao, rodam sozinhas.")
)

cad.section("carregar-modelo", "Passo 3: Carregar e relacionar o modelo",
    p("Depois do <i>Fechar e Aplicar</i>, cada arquivo vira uma tabela no painel direito. Antes de "
      "desenhar, confira o dado e monte os <b>relacionamentos</b> no modo Modelo. Toda relacao e "
      "<b>fato \u2192 dimensao</b>, de muitos para um.") +
    tbl(["Tabela fato", "Liga a dimensao por", "Cardinalidade"],
        [["<code>fato_requisicoes</code>", "dim_calendario (data_recebimento e data_laudo), dim_setor, "
          "dim_tipo_exame, dim_perito, dim_delegacia, dim_status", "N:1"],
         ["<code>fato_movimentacao</code>", "dim_calendario, dim_reagente, dim_setor, "
          "dim_tipo_movimentacao, dim_fornecedor", "N:1"],
         ["<code>fato_produtividade</code>", "dim_calendario, dim_perito, dim_tipo_exame", "N:1"],
         ["<code>fato_orcamento</code>", "dim_setor, dim_rubrica", "N:1"]],
        num_cols=[]) +
    step([
        ("Modo Tabela", "Abra a vista <b>Tabela</b> e confira algumas linhas: as datas do "
         "<code>dim_calendario</code> estao como data? as chaves estao como numero inteiro?"),
        ("Modo Modelo", "Abra <b>Modelo</b>. As tabelas aparecem soltas; os relacionamentos serao "
         "criados agora."),
        ("Ligue fato e dimensao", "Arraste a chave da dimensao para a chave estrangeira da fato. "
         "Exemplo: <code>dim_tipo_exame[tipo_exame_key]</code> \u2192 "
         "<code>fato_requisicoes[tipo_exame_key]</code>."),
        ("Repita para as demais", "Use a tabela acima como lista. O <code>fato_requisicoes</code> liga "
         "a <code>dim_calendario</code> duas vezes (data de recebimento e data de laudo)."),
        ("Confira a cardinalidade", "Abre a relacao e confirme <b>Muitos para Um</b> com direcao de "
         "filtro <b>Unica</b>."),
        ("Valide pelo modelo", "Crie uma matriz simples (setor x tipo_exame) e confira se os numeros "
         "batem com as contagens dos CSVs (Necropsia 32, Balistica 30)."),
    ]) +
    aplicab(
        "Sempre depois de carregar, antes de criar o primeiro visual.",
        "Um modelo sem relacionamento gera graficos que somam valores errados sem avisar.",
        "No modo Tabela, uma chave aparecendo a esquerda e sinal de que continua sendo <b>texto</b>; "
        "volte ao Power Query e corrija o tipo.") +
    callout("err", "Modelo sem relacionamento",
        "Duas tabelas soltas geram resultados errados ao cruzar campos. Defina os relacionamentos no "
        "modo <b>Modelo</b> antes de usar campos de fato e dimensao juntos.")
)

cad.section("primeiro-visual", "Passo 4: criar o primeiro visual (arrastar e soltar)",
    p("Agora o gesto central do Power BI: <b>arrastar campos</b> do painel de dados para os eixos do "
      "visual. Vamos construir o grafico de backlog por setor.") +
    step([
        ("Escolha o visual", "No painel de Visualizacoes, selecione <b>Grafico de Colunas "
         "Clusterizadas</b>."),
        ("Eixo X", "Arraste o campo <code>Setor</code> para o eixo <b>X</b> (categoria)."),
        ("Eixo Y", "Arraste <code>ID_Requisicao</code> para o eixo <b>Y</b> — o Power BI faz a "
         "<b>contagem</b> automaticamente."),
        ("Ajuste o agregado", "Confirme que o campo esta como <b>Contagem</b> de ID_Requisicao "
         "(contar requisicoes) e nao como soma."),
        ("Formate", "Em Formatar visual, adicione o titulo <b>'Backlog Atual por Setor'</b> e ajuste as cores."),
    ]) +
    code("""
        Tipo de visual: Colunas Clusterizadas
        X (categoria) : Setor
        Y (valor)     : Contagem de ID_Requisicao
        Titulo        : Backlog Atual por Setor
        """, "powerbi") +
    callout("err", "Somar ID em vez de contar",
        "Se o campo <code>ID_Requisicao</code> entrar como <b>Soma</b>, o grafico mostra um numero "
        "sem sentido. Clique na seta do campo e troque para <b>Contagem</b>.")
)

cad.section("visuais-essenciais", "Os 5 visuais essenciais para a pericia",
    p("Nao e preciso dominar dezenas de visuais. Cinco deles resolvem a maior parte dos paineis "
      "de gestao pericial.") +
    tbl(["Visual", "Para que serve", "Exemplo POLITEC"],
        [["<b>Cartao (Card)</b>", "Exibe um <b>unico numero</b> em destaque (KPI).",
          "Total de Laudos Pendentes = <b>1.240</b>."],
         ["<b>Colunas Clusterizadas</b>", "Comparacao entre categorias.",
          "TAT Medio (dias) por Setor: DNA x Tox x IML."],
         ["<b>Grafico de Linhas</b>", "Tendencia temporal.",
          "Evolucao mensal de laudos emitidos nos ultimos 12 meses."],
         ["<b>Mapa Preenchido</b>", "Geolocalizacao por regiao.",
          "Mapa de calor de necropsias por municipio de origem."],
         ["<b>Matriz</b>", "Tabela dinamica com totais e subtotais.",
          "Cruzamento de 'Mes' x 'Tipo de Exame' com totais de laudos."]],
        num_cols=[]) +
    legenda([
        ("\U0001f522", "Cartao", "Um numero que resume o estado geral."),
        ("\U0001f4ca", "Colunas", "Comparacao entre setores ou tipos."),
        ("\U0001f4c8", "Linhas", "A tendencia que conta a historia do periodo."),
        ("\U0001f5fa", "Mapa", "De onde vem a demanda pericial."),
        ("\U0001f4cb", "Matriz", "O detalhe cruzado por tras dos totais."),
    ]) +
    callout("tip", "Menos e mais",
        "Cole na mesma pagina os cinco visuais que respondem as cinco perguntas do gestor. "
        "Resista a tentacao de encher o canvas.")
)

cad.section("poder-mapas", "O poder dos mapas no Power BI",
    p("O Power BI usa o <b>Bing Maps</b> nativamente para <b>geocodificar</b> enderecos sem "
      "configuracao adicional. Isso transforma uma lista de municipios em um mapa de calor.") +
    step([
        ("Tenha a coluna geografica", "Basta uma coluna de <code>Municipio</code> ou "
         "<code>CEP da Delegacia Requisitante</code>."),
        ("Insira o Mapa Preenchido", "Selecione o visual <b>Mapa Preenchido</b> (Filled Map)."),
        ("Local e cor", "Arraste <code>Municipio</code> para <b>Local</b> e a quantidade para "
         "<b>Saturacao de Cor</b>."),
        ("Confira", "O Bing reconhece automaticamente o nome do municipio e pinta a regiao."),
    ]) +
    aplicab(
        "Quando a pergunta de gestao e 'de onde vem a demanda?'.",
        "Porque revela concentracoes regionais que a tabela esconde.",
        "Revela de quais regioes de Mato Grosso vem as maiores demandas periciais — insumo direto "
        "para alocar equipes e abrir unidades regionais.") +
    callout("err", "Municipio escrito errado",
        "O Bing so geocodifica o que reconhece. Grafias erradas ou nomes abreviados podem cair no "
        "mapa errado ou ficar de fora. Padronize antes (Dia 3).")
)

cad.section("slicers", "Filtros e segmentacao de dados (Slicers)",
    p("Os <b>Slicers</b> (segmentacoes) sao botoes visuais que permitem filtrar os dados de forma "
      "interativa. Quando o Diretor clica em <b>'Toxicologia'</b>, todos os graficos do dashboard "
      "se atualizam automaticamente.") +
    tbl(["Slicer", "Opcoes", "Uso na POLITEC"],
        [["<b>Ano / Mes</b>", "Navegacao temporal.",
          "Comparar o mes atual com o anterior e ver tendencia."],
         ["<b>Setor</b>", "DNA, Toxicologia, Balistica, IML.",
          "Isolar a fila de um laboratorio especifico."],
         ["<b>Status do Laudo</b>", "Pendente, Em Analise, Emitido.",
          "Focar no backlog ou na producao do periodo."]],
        num_cols=[]) +
    step([
        ("Insira o slicer", "<kbd>Visualizacoes</kbd> \u2192 <kbd>Slicer</kbd>."),
        ("Escolha o campo", "Arraste <code>Setor</code> para o slicer."),
        ("Ajuste o estilo", "Em <i>Formatar visual</i>, escolha lista suspensa ou botoes lado a lado."),
        ("Teste a interacao", "Clique em um setor e veja todos os outros visuais reagirem."),
    ]) +
    callout("note", "Interatividade por padrao",
        "No Power BI, os visuais ja se comunicam entre si sem programacao. O clique em um setor "
        "filtra os demais visuais da pagina automaticamente.")
)

cad.section("caso-iml", "Caso real: dashboard de gestao do IML",
    p("Um <b>Instituto Medico Legal</b> implementou um dashboard em Power BI para monitorar a entrada "
      "de corpos e a emissao de laudos de necropsia em tempo real.") +
    grid2([
        ("Funcionalidades implementadas",
         ul(["<b>Mapa de calor</b> de ocorrencias por municipio",
             "Filtros por <b>tipo de morte</b>: Violenta, Natural, Indeterminada",
             "Alertas visuais em <b>vermelho</b> quando o TAT ultrapassa o prazo legal"])),
        ("Resultado concreto",
         "O <b>Ministerio Publico</b> passou a acompanhar o painel publicamente, aumentando a "
         "transparencia. A gestao conseguiu <b>justificar a contratacao de mais peritos</b> com dados "
         "objetivos e inquestionaveis."),
    ]) +
    ficha("g", "A licao para MT",
        "O argumento que transforma pedido em <b>orcamento aprovado</b> nao e 'estamos sobrecarregados' "
        "— e um mapa que mostra o gargalo, com numero e data.") +
    callout("tip", "Transparencia como aliada",
        "Quando o MP acompanha o painel, a transparencia deixa de ser risco e passa a ser "
        "<b>argumento de gestao</b> para conseguir recursos.")
)

cad.section("fechamento-manha", "Fechamento da manha: do zero ao primeiro painel",
    p("A manha percorreu cinco marcos. Antes de seguir para a tarde, o recap fixa o essencial.") +
    legenda([
        ("\U0001f3d7\ufe0f", "Arquitetura", "Desktop (criacao), Service (publicacao) e Mobile (consulta em campo)."),
        ("\U0001f5a5", "Interface", "Ribbon similar ao Office, com paineis de Dados, Visualizacoes e Filtros."),
        ("\U0001f50c", "Conexao", "Mais de 100 fontes. Importacao (historico) x DirectQuery (tempo real)."),
        ("\U0001f4ca", "Visuais", "Cartao, Colunas, Linhas, Mapa e Matriz: a base de todo dashboard pericial."),
        ("\U0001f39a\ufe0f", "Interatividade", "Slicers que permitem explorar por setor, periodo e status do laudo."),
    ]) +
    kpi([("3", "pilares do Power BI"), ("100+", "fontes de dados"),
         ("5", "visuais essenciais"), ("5s", "principio de leitura")]) +
    callout("tip", "Ponte para a tarde",
        "O painel da manha vive no seu PC. A tarde responde: como levar isso para <b>toda a "
        "instituicao</b>, com seguranca e atualizacao automatica?")
)

# =================================================================
# PARTE 2 - MODULO 6 PARTE 2
# =================================================================
cad.grp("Parte 2 · Modulo 6 - Publicacao, Compartilhamento e Workspaces",
        "Tarde: levar o dashboard do analista para a instituicao, com governanca, seguranca e automacao.")

cad.section("powerbi-service", "O Power BI Service: a nuvem da inteligencia institucional",
    p("O <b>Power BI Service</b> (<code>app.powerbi.com</code>) e a plataforma online onde voce "
      "publica, compartilha e colabora em dashboards com toda a equipe da POLITEC. E a diferenca "
      "entre um <b>arquivo no computador</b> e uma <b>inteligencia institucional viva</b>.") +
    grid2([
        ("Desktop",
         "Arquivo <code>.pbix</code> no seu PC. <b>Offline, individual e nao compartilhado</b>. "
         "Otimo para criar, ruim para distribuir."),
        ("Service",
         "Relatorio na nuvem. <b>Online, colaborativo</b> e com <b>atualizacao automatica</b> de "
         "dados. E o ambiente de consumo institucional."),
    ]) +
    aplicab(
        "Quando o painel precisa chegar a mais de uma pessoa, de forma controlada.",
        "Porque o arquivo local nao escala nem governa acesso: a nuvem centraliza a distribuicao.",
        "O Diretor abre o painel no navegador ou no celular, sem precisar do arquivo nem do Desktop "
        "instalado na maquina dele.") +
    callout("note", "O Service nao substitui o Desktop",
        "O Desktop <b>cria</b>; o Service <b>publica e consome</b>. Voce continua editando o "
        "<code>.pbix</code> no Desktop e republicando quando houver mudancas.")
)

cad.section("desktop-vs-service", "Desktop x Service: licenca e hospedagem no Brasil",
    p("A publicacao tem regras: conta corporativa e licenca. E, no caso da POLITEC, um ponto decisivo "
      "de conformidade.") +
    ficha("a", "Requisito de licenca",
        "Conta corporativa <code>@politec.mt.gov.br</code> com licenca <b>Power BI Pro</b> ou "
        "<b>Premium</b>. Publicar e compartilhar de forma privada nao e gratuito.") +
    ficha("g", "Hospedagem e LGPD",
        "O Service e hospedado na <b>Azure</b>, com <b>data centers no Brasil</b>, garantindo "
        "conformidade com a <b>LGPD</b> e mantendo os dados sob a legislacao brasileira.") +
    tbl(["Criterio", "Desktop", "Service"],
        [["Custo", "Gratuito", "Pro ou Premium (pago)"],
         ["Acesso", "Na maquina do analista", "Navegador e celular, de qualquer lugar"],
         ["Atualizacao", "Manual (republicar)", "Agendada e automatica"],
         ["Governanca", "Nao se aplica", "Workspaces, permissoes e auditoria"]],
        num_cols=[]) +
    callout("err", "Publicar com conta pessoal",
        "Publicar com conta <code>@gmail</code> ou pessoal rompe a governanca e a LGPD. O relatorio "
        "institucional deve viver sob a conta <b>corporativa</b>.")
)

cad.section("publicacao", "Publicacao: do Desktop para a nuvem",
    p("Publicar e um processo curto, mas com uma <b>checagem critica</b> antes do clique final.") +
    step([
        ("Conecte ao workspace", "No Desktop, clique em <kbd>Pagina Inicial</kbd> \u2192 <kbd>Publicar</kbd>."),
        ("Selecione o destino", "Escolha o <b>workspace</b> correto (ex.: <i>POLITEC - Laboratorios</i>)."),
        ("Aguarde o upload", "Confirme o envio e espere a mensagem de sucesso."),
        ("Abra no navegador", "Clique no link para abrir o relatorio em <code>app.powerbi.com</code>."),
    ]) +
    callout("err", "Seguranca critica antes de publicar",
        "Antes de publicar, verifique se nao ha <b>dados sensiveis</b> (nomes de vitimas do IML, "
        "CPFs, laudos sigilosos). Use a funcao <b>'Ocultar'</b> nas colunas sensiveis ou crie um "
        "nivel de acesso restrito ao workspace.") +
    ficha("r", "Publicar e rapido; despublicar, nem tanto",
        "Depois que o relatorio esta na nuvem, quem tem permissao pode abri-lo imediatamente. "
        "A ocultacao de dados sensiveis precisa acontecer <b>antes</b> do upload.")
)

cad.section("jorge-camoes", "Autor referencia: Jorge Camoes e a governanca",
    p("Autor de <b>'Data Visualization in Excel and Power BI' (2021)</b>, Jorge Camoes e a referencia "
      "de <b>governanca</b> na visualizacao de dados.") +
    ficha("p", "A frase que define a tarde",
        "'Um dashboard publicado sem governanca e um tiro no pe. Governanca e saber quem ve o que.' "
        "- Jorge Camoes.") +
    aplicab(
        "Ao definir quem acessa cada workspace e cada relatorio.",
        "Porque publicar sem controle pode expor dados sigilosos de investigacao.",
        "Na POLITEC/MT, o <b>Secretario de Seguranca</b> acessa o dashboard macro estrategico, "
        "enquanto o <b>perito do setor</b> visualiza exclusivamente o dashboard do proprio laboratorio.") +
    callout("note", "Governanca nao e burocracia",
        "E <b>protecao da investigacao e da instituicao</b>. Um acesso indevido a um laudo sigiloso "
        "compromete a cadeia de custodia e a propria apuracao.")
)

cad.section("workspaces", "Workspaces: a organizacao institucional",
    p("Workspaces sao <b>espacos colaborativos</b> no Power BI Service para agrupar dashboards de uma "
      "equipe ou projeto. A estrutura recomendada para a POLITEC/MT separa tres ambientes.") +
    tbl(["Workspace", "Conteudo", "Acesso"],
        [["<b>POLITEC - Diretoria</b>", "Dashboards estrategicos: backlog geral, TAT macro e orcamento.",
          "Exclusivo do Diretor e do Secretario de Seguranca."],
         ["<b>POLITEC - IML</b>", "Dashboards operacionais de necropsias e clinica forense; prazos legais.",
          "Gestao do IML e equipes de necropsia."],
         ["<b>POLITEC - Laboratorios</b>", "Dashboards taticos por chefe de setor (DNA, Toxicologia, Balistica).",
          "Cada chefe gerencia a propria fila interna."]],
        num_cols=[]) +
    ficha("g", "Por que isso funciona",
        "Cada perfil ve <b>exatamente o que precisa</b>. O estrategico nao se perde no operacional, e "
        "o operacional nao tem acesso ao sigiloso de outra area.") +
    callout("tip", "Um workspace por proposito",
        "Nao crie um workspace unico para tudo. Segmente por <b>nivel de decisao</b> (estrategico, "
        "operacional, tatico) e por <b>sensibilidade do dado</b>.")
)

cad.section("segregacao-workspaces", "Por que segregar workspaces",
    p("Separar ambientes nao e capricho de organizacao: e <b>obrigacao legal</b> e ganho de "
      "<b>eficiencia</b>.") +
    grid2([
        ("Seguranca da Informacao",
         "Cada workspace tem suas <b>proprias permissoes e conjuntos de dados</b>. Um perito de "
         "Toxicologia nao acessa dados sensiveis do IML, e vice-versa."),
        ("Eficiencia Operacional",
         "Cada equipe ve apenas o relevante. <b>Sem ruido</b> de informacao, a analise fica focada e "
         "as decisoes, mais rapidas."),
    ]) +
    aplicab(
        "Ao organizar o BI de uma instituicao com areas sensiveis diferentes.",
        "Porque a segmentacao concilia autonomia de setor com controle centralizado.",
        "Sob a <b>LGPD</b> e os regulamentos de sigilo de investigacao, a segregacao deixa de ser boa "
        "pratica e passa a ser <b>exigencia</b>. Administradores mantem controle sem tirar a "
        "autonomia de cada laboratorio.") +
    callout("err", "Workspace 'geral' para todos",
        "Colocar toda a instituicao no mesmo workspace e o caminho mais curto para um incidente de "
        "vazamento. Quem nao precisa ver, nao deve ver.")
)

cad.section("caso-governanca-40", "Caso real: governanca de BI na pericia",
    p("Instituicoes forenses com workspaces <b>segregados por area</b> (IML, Lab Central, Pericias "
      "Externas) reduziram em <b>40% os incidentes de seguranca</b> da informacao e vazamento de "
      "dados sensiveis.") +
    bar_chart(["Sem segregacao", "Com segregacao"], [100, 60],
              title="Indice de incidentes de seguranca (base 100)",
              subtitulo="Reducao de 40% apos a segregacao por area e a definicao formal de papeis.",
              destaque=1) +
    ficha("g", "Licao para MT",
        "A POLITEC deve criar uma <b>politica de governanca clara antes</b> de multiplicar "
        "workspaces, definindo formalmente quem e <b>Admin</b>, quem e <b>Membro</b> e quem e apenas "
        "<b>Visualizador</b> em cada ambiente.") +
    callout("tip", "Politica primeiro, tecnologia depois",
        "Defina o papel de cada pessoa <b>antes</b> de criar os ambientes. Assim voce nao precisa "
        "corrigir permissoes erradas depois.")
)

cad.section("compartilhamento", "Compartilhamento: quem ve o que",
    p("Ha tres formas principais de distribuir um dashboard, cada uma com um proposito.") +
    tbl(["Forma", "O que faz", "Quando usar"],
        [["<b>Compartilhar Relatorio</b>", "Envio direto por <b>link</b> para usuarios especificos.",
          "Uso pontual, uma pessoa ou um grupo pequeno."],
         ["<b>Compartilhar Workspace</b>", "Adiciona usuarios com <b>permissoes</b> ao espaco.",
          "Ideal para equipes que colaboram e editam."],
         ["<b>Aplicativo (App)</b>", "Empacota varios relatorios em um <b>unico app</b>.",
          "Distribuicao organizada para um publico grande."]],
        num_cols=[]) +
    aplicab(
        "Ao decidir como o painel chega as pessoas.",
        "Porque cada forma tem um nivel diferente de controle e de esforco de manutencao.",
        "Um link resolve uma consulta rapida; um <b>App 'POLITEC Intelligence'</b> distribui o "
        "pacote completo para centenas de peritos de uma so vez.") +
    callout("err", "Link publico na internet",
        "Compartilhar com 'qualquer pessoa com o link' pode expor dado sigiloso. Restrinja a "
        "<b>pessoas da instituicao</b> e revise as permissoes.")
)

cad.section("niveis-permissao", "Niveis de permissao no workspace",
    p("As permissoes definem o que cada pessoa pode fazer dentro de um workspace. Tres papeis "
      "resolvem quase tudo.") +
    tbl(["Papel", "Pode", "Exemplo POLITEC"],
        [["<b>Admin</b>", "Controle total: gerenciar membros, publicar e excluir conteudo.",
          "<code>diretor.politec@politec.mt.gov.br</code>"],
         ["<b>Membro</b>", "Publicar novos relatorios e editar dashboards existentes.",
          "<code>analista.bi@politec.mt.gov.br</code>"],
         ["<b>Visualizador</b>", "Acessar e consultar dashboards do setor. Nao edita nem publica.",
          "<code>perito.dna@politec.mt.gov.br</code>"]],
        num_cols=[]) +
    legenda([
        ("\U0001f511", "Admin", "Poucos, de confianca: controlam o ambiente inteiro."),
        ("\u270f\ufe0f", "Membro", "Constroi e mantem: o analista de BI do setor."),
        ("\U0001f441", "Visualizador", "So consome: a maioria dos usuarios."),
    ]) +
    callout("err", "Todos como Admin",
        "Dar Admin a todos anula a governanca. A regra e o <b>menor privilegio</b>: cada pessoa com "
        "o minimo de acesso necessario para a sua funcao.")
)

cad.section("apps-powerbi", "O poder dos Aplicativos (Apps) no Power BI",
    p("Um <b>App</b> e um pacote organizado de multiplos relatorios, navegados por <b>abas</b> dentro "
      "de uma interface limpa e profissional.") +
    flow_h([
        ("\U0001f4e6", "Empacotar"),
        ("\u2601", "Publicar 1x"),
        ("\U0001f465", "200 peritos"),
        ("\U0001f4f1", "Consumir por abas"),
    ]) +
    step([
        ("Reuna os relatorios", "Agrupe os relatorios que fazem sentido para um mesmo publico."),
        ("Crie o App", "No workspace, use <kbd>Criar aplicativo</kbd> e escolha os relatorios."),
        ("Organize por abas", "Monte a navegacao por abas (ex.: Minha Fila, Backlog, Estoque)."),
        ("Publique e distribua", "Publique o app e conceda acesso aos usuarios ou grupos."),
    ]) +
    callout("tip", "Publicar uma vez, distribuir para todos",
        "Voce publica o app <b>uma unica vez</b> e distribui para 200 peritos simultaneamente — sem "
        "precisar compartilhar relatorio por relatorio.")
)

cad.section("app-painel-perito", "Exemplo de App: o 'Painel do Perito'",
    p("Um app bem desenhado leva o dado certo ao perito certo, sem distracao. O <i>Painel do Perito</i> "
      "organiza o trabalho em tres abas.") +
    tbl(["Aba", "Conteudo", "Pergunta que responde"],
        [["<b>1. Minha Fila de Trabalho</b>", "As requisicoes atribuidas ao proprio perito.",
          "'O que eu preciso fazer hoje?'"],
         ["<b>2. Backlog do Setor</b>", "A fila do laboratorio como um todo.",
          "'Como esta a carga do meu setor?'"],
         ["<b>3. Estoque de Reagentes</b>", "Insumos proximos do nivel minimo.",
          "'Falta algum insumo para produzir?'"]],
        num_cols=[]) +
    ficha("g", "Cada perito ve apenas o seu contexto",
        "A interface e <b>simples e sem distracoes</b>: o perito abre o app e enxerga a propria fila, "
        "nao o painel macro da instituicao.") +
    callout("err", "App com tudo dentro",
        "Um app que mostra tudo para todos deixa de ser util. O valor do app esta em <b>selecionar</b> "
        "o que cada publico precisa ver.")
)

cad.section("atualizacao-agendada", "Atualizacao agendada: automacao na nuvem",
    p("Configurar o Service para atualizar automaticamente elimina a necessidade de reexportar "
      "planilhas manualmente — uma das <b>maiores fontes de erro</b> em ambientes operacionais.") +
    step([
        ("Abra o dataset", "No workspace, localize o <b>conjunto de dados</b> ligado ao relatorio."),
        ("Configuracoes", "Menu do dataset \u2192 <kbd>Configuracoes</kbd>."),
        ("Atualizacao agendada", "Expanda <kbd>Atualizacao agendada</kbd> e ative."),
        ("Frequencia e horario", "Defina quantas vezes por dia e em quais horarios."),
        ("Notificacao", "Ative o aviso de falha para saber se algo quebrou."),
    ]) +
    ficha("a", "Sem atualizacao, o painel envelhece",
        "Um dashboard com dados de ontem apresentado como 'situacao atual' e pior do que nenhum "
        "painel. A atualizacao agendada e o que mantem o dado vivo.") +
    callout("tip", "Ative a notificacao de falha",
        "Atualizacoes podem falhar (fonte fora do ar, credencial expirada). O aviso por e-mail "
        "permite corrigir antes que o gestor abra um painel desatualizado.")
)

cad.section("frequencia-atualizacao", "Frequencia de atualizacao recomendada",
    p("Nao existe uma frequencia unica: ela depende da <b>natureza do dado</b>. Tres padroes cobrem "
      "a POLITEC.") +
    tbl(["Tipo de fonte", "Frequencia", "Motivo"],
        [["<b>Fontes na nuvem</b> (SharePoint/OneDrive)", "Nativa, sem configuracao.",
          "O Service detecta as mudancas automaticamente."],
         ["<b>Dados operacionais</b> (entrada de requisicoes)", "A cada <b>1 hora</b>.",
          "Exige o On-premises Data Gateway para fontes locais."],
         ["<b>Dados historicos</b> (laudos emitidos)", "<b>1x por dia, as 06h00</b>.",
          "Dados frescos na abertura do expediente."]],
        num_cols=[]) +
    kpi([("Nativa", "Fontes na nuvem"), ("1h", "Dados operacionais"),
         ("06h00", "Dados historicos"), ("Diaria", "Visao do gestor")]) +
    callout("note", "Nem mais, nem menos",
        "Atualizar de minuto em minuto gera custo e ruido sem ganho de decisao. Escolha a frequencia "
        "que <b>muda a decisao</b>.")
)

cad.section("data-gateway", "O On-premises Data Gateway",
    p("O sistema de gestao de laudos da POLITEC roda em um <b>servidor local</b>. Por padrao, o "
      "Service na nuvem nao acessa esse servidor diretamente. O <b>Gateway</b> resolve isso.") +
    grid2([
        ("O desafio",
         "O banco SQL Server esta <b>on-premises</b> (na rede da instituicao). A nuvem, sozinha, nao "
         "alcanca esse servidor com seguranca."),
        ("A solucao: Gateway",
         "Um software instalado na rede local cria um <b>tunel seguro e criptografado</b> entre o "
         "servidor local e a nuvem — <b>sem expor o servidor a internet</b>."),
    ]) +
    flow_h([
        ("\U0001f5c4\ufe0f", "SQL local"),
        ("\U0001f512", "Gateway"),
        ("\u2601", "Power BI Service"),
        ("\U0001f4ca", "Dashboard"),
    ]) +
    callout("tip", "Soberania dos dados",
        "E possivel ter dashboards modernos na nuvem <b>mantendo total soberania e seguranca</b> "
        "dos dados no servidor local da instituicao.")
)

cad.section("caso-gateway", "Caso real: Gateway na seguranca publica",
    p("Policias Civis e Institutos de Pericia de diversos estados usam o <b>On-premises Data "
      "Gateway</b> para conectar o Service aos seus bancos locais em <b>SQL Server</b>, sem jamais "
      "expor os servidores a internet publica.") +
    grid2([
        ("Por que usam",
         "O dado sigiloso de investigacao permanece no servidor da corporacao, sob sua "
         "administracao, e apenas a <b>consulta agregada</b> chega a nuvem."),
        ("Seguranca garantida",
         "O gateway usa <b>criptografia de ponta</b>, <b>autenticacao multifator (MFA)</b> e "
         "<b>logs de auditoria</b> completos — requisitos da LGPD e dos padroes do setor publico."),
    ]) +
    ficha("g", "Requisitos de conformidade atendidos",
        "Criptografia, MFA e auditoria sao exatamente o que a LGPD e as normas de seguranca do setor "
        "publico exigem. O gateway nao e um 'jeitinho': e a arquitetura correta.") +
    callout("err", "Abrir o banco para a internet",
        "Liberar o SQL Server diretamente para a nuvem expoe a instituicao a ataques. O tunel do "
        "gateway existe justamente para evitar isso.")
)

cad.section("simulacao-workspace", "Simulacao: criando o workspace 'POLITEC - Laboratorios'",
    p("Este exercicio simula o <b>fluxo completo</b> de implantacao de um ambiente colaborativo de BI "
      "na POLITEC — do workspace vazio ao dashboard acessivel por toda a equipe de peritos.") +
    flow_h([
        ("\u2795", "Criar Workspace"),
        ("\U0001f465", "Adicionar Membros"),
        ("\u2b06\ufe0f", "Publicar"),
        ("\u2699\ufe0f", "Configurar Gateway"),
        ("\U0001f4e4", "Compartilhar App"),
    ]) +
    step([
        ("Criar workspace", "No Service: <kbd>Workspaces</kbd> \u2192 <kbd>Criar um workspace</kbd> \u2192 "
         "nome <i>POLITEC - Laboratorios</i>."),
        ("Adicionar membros", "Convide os responsaveis com os papeis corretos (Admin, Membro, Visualizador)."),
        ("Publicar dashboard", "No Desktop, publique o relatorio neste workspace."),
        ("Configurar gateway", "Associe o gateway e ative a atualizacao agendada."),
        ("Compartilhar app", "Empacote e distribua o app para a equipe de peritos."),
    ]) +
    callout("note", "Simulacao sem risco",
        "O exercicio usa base simulada. Faca na ordem e observe os papeis mudando o que cada usuario "
        "consegue fazer.")
)

cad.section("membros-permissoes", "Definindo membros e permissoes",
    p("Com o workspace criado, atribua os papeis com base na <b>funcao real</b> de cada pessoa na "
      "instituicao. O exemplo abaixo usa e-mails institucionais.") +
    tbl(["Usuario", "Papel", "Pode fazer"],
        [["<code>diretor.politec@politec.mt.gov.br</code>", "<b>Admin</b>",
          "Controle total: gerenciar membros, publicar e excluir conteudo."],
         ["<code>analista.bi@politec.mt.gov.br</code>", "<b>Membro</b>",
          "Publicar novos relatorios e editar dashboards existentes."],
         ["<code>perito.dna@politec.mt.gov.br</code>", "<b>Visualizador</b>",
          "Acessar e consultar dashboards do setor. Nao edita nem publica."]],
        num_cols=[]) +
    step([
        ("Abra o acesso", "No workspace, clique em <kbd>Acesso</kbd>."),
        ("Adicione a pessoa", "Digite o e-mail institucional e escolha o papel."),
        ("Revise", "Confirme antes de enviar — a permissao vale imediatamente."),
        ("Documente", "Registre quem entrou, com que papel e quando."),
    ]) +
    callout("tip", "Menor privilegio sempre",
        "Na duvida entre Membro e Visualizador, comece como <b>Visualizador</b>. E facil promover "
        "depois; e caro corrigir um vazamento.")
)

cad.section("boas-praticas-governanca", "Boas praticas de governanca na POLITEC",
    p("Governanca e um conjunto de habitos. Quatro deles sustentam todo o resto.") +
    legenda([
        ("\U0001f4dc", "Politica antes de criar",
         "Documente <b>quem</b> e responsavel por cada workspace, <b>quais dados</b> contem e <b>quem</b> tem acesso."),
        ("\U0001f512", "Oculte dados sensiveis",
         "Use a funcao 'Ocultar' em colunas com nomes de vitimas, CPFs e detalhes sigilosos. Nunca publique sem essa checagem."),
        ("\U0001f504", "Revise permissoes",
         "Quem muda de setor ou sai da instituicao deve ter o acesso <b>revogado imediatamente</b>."),
        ("\U0001f4d6", "Documente as fontes",
         "Mantenha um <b>data dictionary</b>: de onde vem cada tabela, quem a mantem e com que frequencia atualiza."),
    ]) +
    checklist([
        "Politica de governanca escrita e aprovada.",
        "Colunas sensiveis ocultas ou removidas.",
        "Permissoes revisadas mensalmente.",
        "Catalogo de dados atualizado.",
    ]) +
    callout("err", "Governanca de uma vez so",
        "Tentar documentar e arrumar tudo depois e caro. Incorpore a governanca ao <b>processo</b> de "
        "criacao de cada workspace.")
)

# =================================================================
# PARTE 3 - PRATICA GUIADA
# =================================================================
cad.grp("Parte 3 · Pratica guiada",
        "Sete laboratorios que constroem, do zero, o dashboard de backlog da POLITEC.")

cad.section("lab1-obter-dados", "Lab 1 - Obter Dados e conferir o modelo",
    p("Objetivo: importar as tabelas <code>fato_*</code> e <code>dim_*</code> de "
      "<code>datasets/</code> e conferir o que chegou antes de qualquer visual.") +
    step([
        ("Obter Dados", "<kbd>Pagina Inicial</kbd> \u2192 <kbd>Obter Dados</kbd> \u2192 "
         "<kbd>Texto/CSV</kbd> (ou <kbd>Pasta</kbd>) \u2192 selecione a pasta <code>datasets/</code>."),
        ("Escolher os arquivos", "Marque os quatro <code>fato_*</code> e as dez <code>dim_*</code>; "
         "observe a pre-visualizacao."),
        ("Transformar", "Clique em <b>Transformar Dados</b> para abrir o Power Query."),
        ("Conferir tipos", "Confirme <code>data_key</code> e as chaves <code>*_key</code> como numero "
         "inteiro e <code>data</code> como Data."),
        ("Fechar e Aplicar", "Traga as tabelas tratadas para o modelo e siga para os relacionamentos."),
    ]) +
    callout("err", "Importar a fonte plana junto",
        "Nao marque tambem as bases planas (<code>requisicoes_periciais.csv</code> etc.). Elas ja estao "
        "representadas no modelo e criariam tabelas duplicadas.")
)

cad.section("lab2-power-query", "Lab 2 - Limpar a base no Power Query",
    p("Objetivo: deixar a base pronta — sem linha de total, com tipos corretos e setores padronizados.") +
    step([
        ("Remover 'Total Geral'", "Filtre a coluna Setor e <b>desmarque</b> 'Total Geral'."),
        ("Corrigir tipos", "Selecione as colunas de data \u2192 <kbd>Transformar</kbd> \u2192 "
         "<kbd>Tipo de Dados</kbd> \u2192 <kbd>Data</kbd>."),
        ("Padronizar setores", "Substitua variacoes: 'Tox' \u2192 'Toxicologia', 'Lab. DNA' \u2192 'DNA'."),
        ("Renomear a consulta", "Deixe o nome legivel: <code>Tabela_Laudos</code>."),
        ("Fechar e Aplicar", "Grave a receita para as proximas atualizacoes."),
    ]) +
    code("""
        = Table.SelectRows(#"Etapa Anterior", each [Setor] <> "Total Geral")
        """, "m") +
    callout("err", "Limpar no Excel, nao no Power Query",
        "Nao conserte a base manualmente na planilha de origem. Corrija no <b>Power Query</b>: assim "
        "a limpeza <b>se repete sozinha</b> em cada atualizacao.")
)

cad.section("lab3-primeiro-visual", "Lab 3 - O primeiro visual: backlog por setor",
    p("Objetivo: construir o grafico de colunas que responde 'qual setor tem mais backlog?'.") +
    step([
        ("Escolha o visual", "Painel de Visualizacoes \u2192 <b>Colunas Clusterizadas</b>."),
        ("Eixo X", "Arraste <code>Setor</code> para o eixo X."),
        ("Eixo Y", "Arraste <code>ID_Requisicao</code> para o eixo Y e confirme <b>Contagem</b>."),
        ("Titulo", "Em Formatar visual, escreva <b>'Backlog Atual por Setor'</b>."),
        ("Cores", "Destaque o setor mais critico em uma cor de alerta."),
    ]) +
    aplicab(
        "Quando o gestor pergunta 'onde esta o gargalo?'.",
        "Porque a comparacao entre setores mostra, de imediato, quem concentra o backlog.",
        "O Diretor ve que o <b>DNA</b> concentra a maior fila e direciona o reforco de equipe para la.") +
    callout("tip", "Confira a contagem",
        "Clique no campo no eixo Y e verifique o agregado. <b>Soma de ID</b> nao faz sentido; "
        "<b>Contagem de ID</b> sim.")
)

cad.section("lab4-visuais-essenciais", "Lab 4 - Cartao, linha e matriz",
    p("Objetivo: completar a pagina com os tres visuais que dao contexto ao grafico de colunas.") +
    step([
        ("Cartao de pendentes", "Visual <b>Cartao</b> \u2192 arraste uma medida de laudos pendentes e "
         "formate o numero em destaque."),
        ("Linha de tendencia", "Visual <b>Grafico de Linhas</b> \u2192 eixo com o mes, valores com a "
         "contagem de laudos emitidos (12 meses)."),
        ("Matriz", "Visual <b>Matriz</b> \u2192 linhas = Mes, colunas = Tipo de Exame, valores = "
         "contagem de laudos."),
        ("Alinhe o layout", "Distribua os visuais na pagina e deixe o cartao no canto superior."),
    ]) +
    kpi([("1.240", "Laudos pendentes"), ("18 dias", "TAT medio da semana"),
         ("312", "Laudos emitidos no mes"), ("96", "Requisicoes hoje")]) +
    callout("err", "Matriz com totais errados",
        "Se os subtotais parecerem estranhos, confira se nao ha <b>linhas de total</b> vindas da "
        "planilha somadas as da matriz. Remova os 'Total Geral' no Power Query.")
)

cad.section("lab5-mapa-calor", "Lab 5 - O mapa de calor por municipio",
    p("Objetivo: revelar de quais municipios vem a maior demanda pericial.") +
    step([
        ("Insira o mapa", "Visual <b>Mapa Preenchido</b> (Filled Map)."),
        ("Local", "Arraste <code>Municipio</code> para o campo <b>Local</b>."),
        ("Saturacao", "Arraste <code>Qtd_Requisicoes</code> para <b>Saturacao de Cor</b>."),
        ("Escala de cor", "Configure verde (baixa demanda) \u2192 vermelho (alta demanda)."),
        ("Confira a geocodificacao", "Verifique se todos os municipios foram reconhecidos pelo Bing."),
    ]) +
    flow_h([
        ("\U0001f5fa", "Mapa Preenchido"),
        ("\U0001f4cd", "Municipio"),
        ("\U0001f3a8", "Saturacao de Cor"),
        ("\U0001f53a", "Alta demanda"),
    ]) +
    callout("err", "Municipio fora do mapa",
        "Alguns pontos podem ficar de fora se o nome nao for reconhecido. Padronize a grafia dos "
        "municipios (Dia 3) e evite abreviacoes.")
)

cad.section("lab6-slicers", "Lab 6 - Slicers: a interatividade do painel",
    p("Objetivo: permitir que o gestor explore o painel por periodo, setor e status do laudo.") +
    step([
        ("Slicer de periodo", "Visual <b>Slicer</b> \u2192 arraste <code>Ano/Mes</code>."),
        ("Slicer de setor", "Novo slicer \u2192 arraste <code>Setor</code> e escolha botoes."),
        ("Slicer de status", "Novo slicer \u2192 arraste <code>Status_Laudo</code> (Pendente, Em Analise, Emitido)."),
        ("Teste", "Clique em 'Toxicologia' e confirme que todos os visuais se atualizam."),
        ("Organize", "Posicione os slicers em uma faixa no topo, alinhados."),
    ]) +
    ficha("g", "O dashboard conversa",
        "Com os slicers, o mesmo conjunto de visuais responde a dezenas de perguntas sem precisar de "
        "dezenas de graficos. <b>Interatividade poupa espaco e cabeca</b>.") +
    callout("tip", "Editar interacoes",
        "<kbd>Formatar</kbd> \u2192 <kbd>Editar interacoes</kbd> permite controlar quais visuais um "
        "slicer afeta. Use com moderacao para nao confundir o usuario.")
)

cad.section("lab7-publicar-compartilhar", "Lab 7 - Publicar e compartilhar com governanca",
    p("Objetivo: realizar o fluxo completo de publicacao, da checagem de dados sensiveis ao "
      "compartilhamento.") +
    step([
        ("Ocultar dados sensiveis", "Antes de publicar, oculte/remova CPFs e nomes de vitimas."),
        ("Publicar", "Pagina Inicial \u2192 <kbd>Publicar</kbd> \u2192 workspace "
         "<i>POLITEC - Laboratorios</i>."),
        ("Abrir no Service", "Confirme o relatorio em <code>app.powerbi.com</code>."),
        ("Atualizacao agendada", "No dataset, ative a atualizacao (1x/dia as 06h00)."),
        ("Compartilhar", "Escolha link, workspace ou um <b>App</b> conforme o publico."),
    ]) +
    checklist([
        "Colunas com dados pessoais ocultas ou removidas.",
        "Workspace de destino correto.",
        "Atualizacao agendada testada.",
        "'Ultima Atualizacao' visivel no dashboard.",
        "Filtros de slicer funcionando na nuvem.",
        "Usuarios comunicados sobre o novo painel.",
        "Fontes e frequencia documentadas.",
    ]) +
    callout("err", "Publicar antes de ocultar",
        "Nunca inverta a ordem. Primeiro <b>oculte</b>, depois <b>publique</b>. Dado sensivel ja "
        "publicado pode ter sido visto antes de voce corrigir.")
)

# =================================================================
# PARTE 4 - CENARIOS E APLICACOES
# =================================================================
cad.grp("Parte 4 · Cenarios e Aplicacoes Praticas",
        "Dashboards, KPIs e cenarios reais de gestao pericial na POLITEC/MT.")

cad.section("dashboard-diretoria", "O dashboard estrategico da Diretoria",
    p("O dashboard estrategico deve responder as perguntas criticas da gestao em <b>menos de 5 "
      "segundos</b>, seguindo o principio de Cole Nussbaumer Knaflic.") +
    tbl(["Pergunta critica", "KPI (cartao de destaque)"],
        [["Qual e o backlog total de laudos hoje?", "<b>Total de Laudos Pendentes</b>"],
         ["Qual setor esta com o TAT mais critico?", "<b>TAT Medio (dias) - Semana Atual</b>"],
         ["Como esta a evolucao mensal de producao?", "<b>Laudos Emitidos - Mes Atual</b>"],
         ["Quantas requisicoes chegaram hoje?", "<b>Requisicoes Recebidas - Hoje</b>"]],
        num_cols=[]) +
    kpi([("1.240", "Laudos pendentes"), ("18 dias", "TAT medio da semana"),
         ("312", "Laudos emitidos no mes"), ("96", "Requisicoes hoje")]) +
    callout("tip", "Cinco segundos, quatro respostas",
        "Coloque os cartoes de KPI no topo e a tendencia logo abaixo. Sem rolagem, sem clique: o "
        "Diretor entende o estado geral ao abrir.")
)

cad.section("dashboard-setor", "O dashboard tatico do Chefe de Setor",
    p("Enquanto o Diretor precisa da visao macro, o Chefe de Setor (ex.: responsavel pelo laboratorio "
      "de DNA) precisa de um dashboard <b>tatico</b>, focado na fila do seu laboratorio.") +
    legenda([
        ("\U0001f464", "Fila por Analista",
         "Quantas requisicoes cada perito esta gerenciando. Mostra sobrecarga e ociosidade."),
        ("\u23f0", "Prazo de Entrega",
         "Laudos proximos do vencimento do prazo legal, ordenados por urgencia."),
        ("\U0001f9ea", "Estoque Critico",
         "Reagentes abaixo do nivel minimo de seguranca, para acionar a compra a tempo."),
    ]) +
    aplicab(
        "Na rotina diaria de gestao de um laboratorio especifico.",
        "Porque o gestor tatico precisa distribuir tarefas e antecipar gargalos, nao ver o total da instituicao.",
        "O Chefe do DNA ve que um perito esta com 40 laudos e outro com 8, e redistribui a fila "
        "<b>antes</b> que o prazo estoure.") +
    callout("note", "Macro x tatico",
        "O estrategico responde 'como vai a instituicao?'; o tatico responde 'o que minha equipe faz "
        "hoje?'. Sao perguntas diferentes e precisam de dashboards diferentes.")
)

cad.section("kpis-essenciais", "Os KPIs essenciais da gestao pericial",
    p("Tres indicadores formam o nucleo da gestao pericial. Eles se complementam: um mede tempo, "
      "outro mede conformidade e o terceiro mede volume.") +
    tbl(["KPI", "Nome", "O que mede"],
        [["<b>TAT</b>", "Tempo de Emissao",
          "Tempo medio entre a entrada da requisicao e a emissao do laudo. Principal indicador de <b>eficiencia operacional</b>."],
         ["<b>SLA</b>", "Cumprimento de Prazo",
          "Percentual de laudos emitidos <b>dentro do prazo</b> legal ou regulamentar. Mede conformidade."],
         ["<b>QL</b>", "Produtividade",
          "Quantidade de laudos <b>por perito</b> no periodo. Permite identificar sobrecargas e redistribuir demandas."]],
        num_cols=[]) +
    bar_chart(["TAT", "SLA", "QL"], [18, 85, 12],
              title="Painel ilustrativo de KPIs (dias, %, laudos/perito)",
              subtitulo="Cada KPI responde uma dimensao diferente: tempo, conformidade e volume.",
              destaque=0) +
    callout("err", "Medir um so KPI",
        "Perseguir so o TAT pode empurrar laudos incompletos para baixar a media. <b>TAT, SLA e QL "
        "juntos</b> evitam que a otimizacao de um piore o outro.")
)

cad.section("alertas-visuais", "Alertas visuais: quando o dado grita",
    p("O Power BI permite configurar <b>alertas automaticos</b> em cartoes e KPIs: quando um valor "
      "ultrapassa um limite definido, o sistema envia um <b>e-mail ou notificacao</b>.") +
    step([
        ("Selecione o cartao", "Clique no visual do KPI que sera monitorado."),
        ("Criar alerta", "Menu do visual \u2192 <kbd>Gerenciar alertas</kbd> \u2192 <kbd>Adicionar regra</kbd>."),
        ("Definir o limite", "Ex.: disparar quando o TAT medio do DNA ultrapassar <b>30 dias</b>."),
        ("Frequencia", "Escolha com que frequencia verificar (ex.: a cada hora)."),
        ("Notificacao", "Ative o e-mail institucional para o responsavel."),
    ]) +
    ficha("a", "Exemplo pratico",
        "Se o TAT medio do setor de <b>DNA</b> ultrapassar <b>30 dias</b>, o Chefe de Setor recebe "
        "uma notificacao automatica por e-mail institucional — antes que o problema vire crise.") +
    callout("tip", "Alerta acionavel, nao ruido",
        "Configure poucos alertas, ligados a decisoes reais. Muitos alertas treinam a equipe a "
        "ignora-los.")
)

cad.section("integracao-sinesp", "Integracao com o SINESP e sistemas estaduais",
    p("A POLITEC/MT pode consumir dados do <b>SINESP</b> (Sistema Nacional de Informacoes de "
      "Seguranca Publica) e dos sistemas internos para criar paineis que evidenciem o impacto da "
      "pericia na elucidacao de crimes.") +
    flow_h([
        ("\U0001f4be", "SINESP"),
        ("\U0001f50e", "Sistema interno POLITEC"),
        ("\U0001f504", "Power BI"),
        ("\U0001f3af", "Decisao de seguranca publica"),
    ]) +
    antesdepois(
        "POLITEC reativa: apenas responde requisicoes quando demandada.",
        "POLITEC parceira estrategica: entrega inteligencia que orienta a politica de seguranca do estado.",
        "Antes", "Depois do BI") +
    callout("note", "A mudanca de posicao",
        "Com os dados integrados, a POLITEC deixa de ser um <b>orgao reativo</b> e se torna "
        "<b>parceira estrategica</b> da inteligencia de seguranca publica de Mato Grosso.")
)

cad.section("mapa-calor-crimes", "O mapa de calor de crimes por municipio",
    p("O mapa de calor por municipio expoe quais regioes de Mato Grosso <b>sobrecarregam mais a "
      "POLITEC</b>, subsidiando decisoes estruturais.") +
    step([
        ("Adicionar visual", "Adicione o <b>Mapa Preenchido</b> ao relatorio."),
        ("Arrastar local", "Arraste <code>Municipio</code> para o campo <b>Local</b>."),
        ("Saturacao", "Arraste <code>Qtd_Requisicoes</code> para <b>Saturacao de Cor</b>."),
        ("Escala", "Configure verde (baixa demanda) \u2192 vermelho (alta demanda)."),
    ]) +
    grid2([
        ("O que o mapa revela",
         "As regioes que mais demandam pericia e as que estao subatendidas, orientando a logistica."),
        ("Decisoes que ele subsidia",
         ul(["Abertura de <b>novas unidades regionais</b>",
             "Alocacao temporaria de <b>peritos itinerantes</b>",
             "Priorizacao de investimentos em <b>infraestrutura</b>"])),
    ]) +
    callout("err", "Mapa bonito, decisao nenhuma",
        "Um mapa so ajuda se levar a uma decisao. Amarre o mapa a uma pergunta de alocacao: 'onde "
        "abrir a proxima unidade?'. Caso contrario, e so decoracao.")
)

cad.section("cenario-backlog", "Cenario 1 - Zerando o backlog com prioridade visivel",
    p("A POLITEC enfrenta um backlog crescente e a direcao precisa atacar os casos mais criticos "
      "primeiro, com equipe limitada.") +
    step([
        ("Construir o painel", "Cartao de pendentes + colunas por setor + linha de tendencia."),
        ("Classificar a gravidade", "Tabela de apoio com prioridade por tipo de crime."),
        ("Filtrar", "Slicer de status = 'Pendente' e de prioridade = 'Maxima'."),
        ("Acionar", "Enviar alerta quando a fila critica passar de um limite."),
    ]) +
    kpi([("A - Maxima", "Homicidio/crime sexual"), ("B - Alta", "Roubo/trafico"),
         ("C - Padrao", "Furto/demais")]) +
    ficha("g", "O ganho",
        "O setor ataca primeiro o que tem maior impacto social e prazo legal mais curto, em vez de "
        "<b>atender por ordem de chegada</b>.") +
    callout("tip", "Prioridade e politica, nao tecnica",
        "Defina as prioridades <b>com a direcao</b> e registre-as. O dashboard apenas executa a "
        "politica de priorizacao acordada.")
)

cad.section("cenario-produtividade", "Cenario 2 - Redistribuindo a carga entre peritos",
    p("Um laboratorio tem dois peritos sobrecarregados e dois com folga, mas ninguem percebe pela "
      "planilha. O BI torna a distribuicao visivel.") +
    bar_chart(["Perito A", "Perito B", "Perito C", "Perito D"], [40, 8, 35, 12],
              title="Laudos em andamento por perito",
              subtitulo="O QL revela a sobrecarga e orienta a redistribuicao da fila.",
              destaque=0) +
    aplicab(
        "Na gestao diaria da fila de um laboratorio.",
        "Porque o volume total esconde a ma distribuicao entre as pessoas.",
        "O Chefe do DNA ve 40 laudos com o Perito A e 8 com o Perito B, e redistribui a fila "
        "<b>antes</b> que o prazo legal estoure.") +
    callout("err", "Medir produtividade sem contexto",
        "Um perito com menos laudos pode estar em casos muito mais complexos. O QL e um sinal, nao "
        "um veredito. Cruze com <b>tipo de exame</b> e <b>complexidade</b>.")
)

cad.section("cenario-orcamento", "Cenario 3 - Transformando dado em orcamento aprovado",
    p("A direcao precisa justificar a contratacao de peritos e a compra de reagentes com evidencia, "
      "nao com percepcao.") +
    step([
        ("Medir o problema", "Painel mostra backlog e TAT crescendo mes a mes."),
        ("Quantificar o impacto", "Cada dia de atraso do laudo de DNA adia a elucidacao de um crime."),
        ("Apresentar a historia", "Storytelling: a pergunta, a tendencia e o ponto critico em destaque."),
        ("Defender a proposta", "O numero deixa de ser reclamacao e vira <b>argumento tecnico</b>."),
    ]) +
    ficha("p", "A frase que resume",
        "Um dashboard nao e so um relatorio de status: e o <b>argumento para a proxima reuniao de "
        "orcamento</b>, a justificativa para contratar e a evidencia de eficiencia institucional.") +
    callout("tip", "Mostre a tendencia",
        "Um backlog de 1.240 laudos nao significa nada sozinho. Mostre se esta <b>crescendo ou "
        "diminuindo</b> em relacao ao mes anterior — e ai o numero ganha forca.")
)

# =================================================================
# PARTE 5 - FECHAMENTO
# =================================================================
cad.grp("Parte 5 · Fechamento",
        "Erros comuns, LGPD, ecossistema, DAX, exercicio final, quiz e referencias.")

cad.section("storytelling", "Storytelling com dados: o dashboard que convence",
    p("'O dashboard nao e o destino — e o <b>veiculo</b> para uma conversa baseada em evidencias. "
      "Quem apresenta os dados precisa saber contar a historia por tras deles.'") +
    tbl(["Passo", "Como fazer", "No dashboard da POLITEC"],
        [["<b>1. Defina a pergunta principal</b>", "Antes de construir, pergunte: 'qual decisao esse dashboard deve apoiar?'.",
          "'Onde alocar peritos no proximo trimestre?'"],
         ["<b>2. Mostre a tendencia</b>", "Nao mostre so o numero; mostre a evolucao.",
          "O TAT esta subindo ou caindo em relacao ao mes anterior?"],
         ["<b>3. Destaque o que importa</b>", "Use cor para guiar o olho ao ponto critico.",
          "So o setor em alerta fica vermelho; o resto, neutro."]],
        num_cols=[]) +
    ficha("g", "A hierarquia visual",
        "Use cor para <b>guiar</b> o olho do gestor ao ponto critico — nao para decorar o painel. "
        "Se tudo esta colorido, nada se destaca.") +
    callout("err", "Contar a historia errada",
        "Comece pela pergunta, nao pelo grafico. Montar visuais empolgantes sem uma pergunta clara "
        "produz um painel bonito e inutil.")
)

cad.section("erros-comuns", "Erros comuns ao criar dashboards periciais",
    p("Os quatro erros que mais aparecem em paineis de gestao publica — e como evita-los.") +
    grid2([
        ("\u274c Excesso de visuais",
         "Um dashboard com 20 graficos nao informa mais: <b>confunde</b>. Limite-se a <b>5-7 visuais "
         "por pagina</b>, cada um respondendo uma pergunta."),
        ("\u274c Dados desatualizados",
         "Um painel com dados de ontem apresentado como 'situacao atual' e pior que nenhum painel. "
         "Configure a <b>atualizacao agendada</b>."),
        ("\u274c Sem contexto de periodo",
         "Sempre mostre o periodo de referencia de forma visivel: <b>'Atualizado em: DD/MM/AAAA as HH:MM'</b>."),
        ("\u274c Publicar dados sensiveis",
         "Verifique e <b>oculte</b> colunas com dados pessoais de vitimas, reus ou investigados antes "
         "de qualquer publicacao."),
    ]) +
    checklist([
        "No maximo 5-7 visuais por pagina.",
        "Atualizacao agendada configurada.",
        "'Ultima Atualizacao' visivel no dashboard.",
        "Dados sensiveis ocultos antes de publicar.",
    ]) +
    callout("err", "O erro que envergonha",
        "Publicar dado sensivel e o unico da lista que <b>nao se desfaz</b> com um clique. Trate-o "
        "como porta de saida: ninguem passa sem checar.")
)

cad.section("checklist-publicacao", "Checklist de publicacao segura (7 itens)",
    p("Antes de publicar qualquer relatorio no Service, percorra os sete itens. Todos precisam estar "
      "marcados.") +
    checklist([
        "Colunas com dados pessoais estao <b>ocultas ou removidas</b>.",
        "O <b>workspace</b> de destino tem as <b>permissoes corretas</b>.",
        "A <b>atualizacao agendada</b> foi testada apos a publicacao.",
        "'<b>Ultima Atualizacao</b>' esta visivel no dashboard.",
        "Os <b>filtros de slicer</b> funcionam corretamente na nuvem.",
        "Os usuarios foram <b>comunicados</b> sobre o novo painel e como acessar.",
        "As <b>fontes de dados</b> e a frequencia de atualizacao estao documentadas.",
    ]) +
    ficha("g", "Regra dos 7",
        "Sete itens marcados = publicacao segura. Qualquer item em branco e um <b>risco de "
        "seguranca</b> ou de decisao baseada em dado errado.") +
    callout("tip", "Ritual, nao burocracia",
        "Transforme o checklist em um <b>habito de equipe</b>: quem publica assina os sete itens. "
        "Com o tempo, vira cultura.")
)

cad.section("bi-lgpd", "BI e a LGPD na seguranca publica",
    p("A <b>Lei Geral de Protecao de Dados (LGPD - Lei 13.709/2018)</b> se aplica ao setor publico e "
      "impoe responsabilidades claras no tratamento de <b>dados pessoais</b> — inclusive os presentes "
      "em laudos, necropsias e registros de vitimas.") +
    tbl(["Obrigacao", "Na pratica da POLITEC"],
        [["<b>Anonimizacao</b>", "Dados pessoais devem ser anonimizados nos dashboards de uso amplo."],
         ["<b>Logs de acesso</b>", "Devem ser mantidos para auditoria — quem viu o que e quando."],
         ["<b>Retencao</b>", "O prazo de guarda deve seguir as politicas institucionais."],
         ["<b>Notificacao</b>", "Vazamentos devem ser comunicados a <b>ANPD em ate 72h</b>."]],
        num_cols=[]) +
    ficha("r", "72 horas",
        "A janela de notificacao a <b>ANPD</b> e de ate <b>72 horas</b>. Por isso governanca e "
        "prevencao valem mais do que remediacao as pressas.") +
    callout("err", "LGPD so para o setor privado",
        "Mito comum. A LGPD vale tambem para o <b>poder publico</b>. Laudos e necropsias contem "
        "dados pessoais sensiveis e exigem cuidado redobrado.")
)

cad.section("ecossistema-microsoft", "O ecossistema Microsoft na seguranca publica",
    p("O Power BI nao vive sozinho: ele se conecta a um ecossistema que a administracao publica ja "
      "costuma ter contratado.") +
    legenda([
        ("\U0001f4ca", "Power BI", "Visualizacao e inteligencia de negocio sobre os dados."),
        ("\U0001f4c1", "SharePoint / OneDrive", "Armazenamento e colaboracao dos arquivos de origem."),
        ("\U0001f4be", "Azure", "Nuvem com data centers no Brasil e servicos de dados."),
        ("\U0001f510", "Entra ID (Azure AD)", "Identidade corporativa e controle de acesso (SSO, MFA)."),
        ("\U0001f4dd", "Dataverse", "Plataforma de dados para aplicacoes governamentais."),
    ]) +
    aplicab(
        "Ao planejar a arquitetura de BI de uma instituicao publica.",
        "Porque usar o ecossistema ja existente reduz custo, simplifica a identidade e facilita a conformidade.",
        "A conta <code>@politec.mt.gov.br</code> do Entra ID ja autentica o usuario no Power BI, no "
        "SharePoint e no OneDrive — <b>um login, um controle de acesso</b>.") +
    callout("note", "Identidade e a base da governanca",
        "Sem uma identidade corporativa forte (Entra ID), nao ha como saber 'quem ve o que'. A "
        "governanca comeca pela <b>identidade</b>.")
)

cad.section("proximos-passos", "Proximos passos: do basico ao avancado",
    p("O Dia 4 e o nivel <b>basico</b>. A trilha de evolucao da POLITEC tem quatro degraus.") +
    step([
        ("1. Basico (hoje)", "Interface, conexao de dados, visuais essenciais, publicacao e workspaces."),
        ("2. Intermediario", "<b>DAX</b> (linguagem de formulas), relacionamentos entre tabelas, "
         "medidas calculadas e KPIs dinamicos."),
        ("3. Avancado", "<b>Power Query avancado</b>, integracao com Python/R, <b>Row-Level Security "
         "(RLS)</b> e deployment pipelines."),
        ("4. Institucional", "Governanca corporativa de dados, catalogo de dados, <b>Center of "
         "Excellence (CoE)</b> e BI para decisao estrategica."),
    ]) +
    flow_h([
        ("\U0001f331", "Basico"),
        ("\U0001f4d0", "Intermediario"),
        ("\U0001f680", "Avancado"),
        ("\U0001f3db", "Institucional"),
    ]) +
    callout("tip", "Um degrau de cada vez",
        "Nao tente RLS no primeiro dia. Consolide o basico (dado limpo, visuais claros, publicacao "
        "governada) antes de subir para DAX e seguranca avancada.")
)

cad.section("previa-dax", "Previa de DAX: o proximo nivel",
    p("<b>DAX (Data Analysis Expressions)</b> e a linguagem de formulas do Power BI, similar as "
      "formulas do Excel, mas muito mais poderosa para analises sobre grandes volumes de dados "
      "relacionais.") +
    code("""
        TAT Medio (dias) =
        AVERAGEX(
            Tabela_Laudos,
            DATEDIFF(
                [DataRequisicao],
                [DataEmissao],
                DAY
            )
        )
        """, "dax") +
    aplicab(
        "Quando um cartao precisa reagir a qualquer filtro do dashboard.",
        "Porque a medida calcula o TAT medio para o contexto selecionado, sem recriar a formula.",
        "Essa formula calcula automaticamente o TAT medio para <b>qualquer filtro</b> selecionado no "
        "slicer — por setor, periodo ou perito.") +
    callout("note", "Excel dentro do Power BI",
        "Quem domina <code>MEDIA</code> e <code>SOMASE</code> reconhece a logica do DAX. A diferenca "
        "e que a medida se adapta sozinha ao <b>contexto de filtro</b>.")
)

cad.section("recursos-aprendizado", "Recursos de aprendizado recomendados",
    p("Tres recursos gratuitos cobrem a maior parte do que voce precisa para evoluir.") +
    tbl(["Recurso", "O que oferece", "Por que usar"],
        [["<b>Microsoft Learn</b>", "Plataforma oficial gratuita com trilhas completas de Power BI, do basico ao avancado, em portugues.",
          "learn.microsoft.com — a fonte oficial e estruturada."],
         ["<b>Storytelling com Dados</b>", "Livro de Cole Nussbaumer Knaflic (2015).",
          "Leitura obrigatoria para quem precisa comunicar dados a decisores."],
         ["<b>Comunidade Power BI</b>", "Forum oficial com milhares de solucoes e exemplos.",
          "community.powerbi.com — respostas praticas da comunidade global."]],
        num_cols=[]) +
    ficha("g", "Trilha sugerida",
        "Comece pelo <b>Microsoft Learn</b> para a tecnica, leia <b>Storytelling</b> para a "
        "comunicacao e use a <b>Comunidade</b> para resolver duvidas concretas.") +
    callout("tip", "Estude com dado real (anonimizado)",
        "Nada substitui praticar com as tabelas de <code>datasets/</code>. Reconstrua o "
        "painel do zero sempre que puder.")
)

cad.section("exercicio-final", "Exercicio final do Dia 4",
    p("Usando o modelo de <code>datasets/</code>, cada participante entrega tres etapas ao "
      "final do dia.") +
    step([
        ("1. Dashboard de Backlog", "Painel com <b>Cartao</b> de total de pendencias, <b>grafico de "
         "colunas por setor</b> e <b>filtro (Slicer)</b> de status do laudo."),
        ("2. Publicacao no Service", "Publicar no workspace <i>POLITEC - Treinamento</i> criado pelo "
         "professor, com o arquivo <code>.pbix</code> nomeado corretamente: "
         "<b>NOME_BACKLOG_POLITEC.pbix</b>."),
        ("3. Compartilhamento", "Compartilhar o relatorio publicado com o e-mail do professor, "
         "demonstrando o fluxo completo: criacao \u2192 publicacao \u2192 compartilhamento."),
    ]) +
    flow_h([
        ("\U0001f4ca", "Criar dashboard"),
        ("\u2601", "Publicar no Service"),
        ("\U0001f4e4", "Compartilhar"),
    ]) +
    callout("note", "Entregavel", 
        "O arquivo <code>NOME_BACKLOG_POLITEC.pbix</code> publicado no workspace do professor e a "
        "prova de dominio do fluxo completo ensinado no dia.")
)

cad.section("takeaways", "Principais takeaways do Modulo 6",
    p("Quatro ideias resumem o modulo inteiro.") +
    grid2([
        ("\U0001f4a1 BI transforma dados em decisoes",
         "O objetivo nao e ter um painel bonito — e responder perguntas estrategicas que melhorem a "
         "gestao pericial."),
        ("\U0001f512 Governanca e inegociavel",
         "Workspaces segregados, permissoes corretas e conformidade com a LGPD sao a base de qualquer "
         "iniciativa de BI no setor publico."),
        ("\U0001f331 Comece simples, itere",
         "Um dashboard com 3 KPIs bem definidos vale mais do que 20 graficos confusos. Comece pelo "
         "que o gestor mais precisa saber."),
        ("\u2601 A nuvem e o futuro institucional",
         "O Power BI Service, com Gateway e atualizacao agendada, permite dados modernos e seguros "
         "sem abrir mao da soberania local."),
    ]) +
    ficha("p", "A frase de encerramento",
        "'A pericia criminal que mede seu desempenho e a que pode melhora-lo. Dados nao sao "
        "burocracia — sao o argumento mais poderoso que um gestor publico pode ter.' - Prof. Renato Rosa") +
    callout("tip", "Ponte para o proximo modulo",
        "Com o basico de BI dominado, o proximo passo natural e o <b>DAX</b> e os relacionamentos, "
        "que transformam o dashboard em um modelo analitico robusto.")
)

cad.section("quiz", "Quiz final do Dia 4",
    q("Quem cunhou a definicao classica de Business Intelligence, em 1989, na Gartner?",
      ["Bill Jelen", "Howard Dresner", "Cole Nussbaumer Knaflic", "Ben Brumfield"], 1,
      "Dresner definiu BI como a aplicacao de conhecimento sobre dados para melhorar a performance da organizacao.") +
    q("Qual e a diferenca central entre Excel e Power BI, segundo o modulo?",
      ["Power BI e so uma versao paga do Excel",
       "Excel e calculo e controle diario; Power BI e inteligencia corporativa e decisao estrategica",
       "Excel nao aceita mais de 100 linhas",
       "Power BI nao faz graficos"], 1,
      "O Excel e a bancada individual; o Power BI consolida a instituicao para a decisao gerencial.") +
    q("Quais sao os 3 pilares da arquitetura do Power BI?",
      ["Word, Excel e PowerPoint", "Desktop, Service e Mobile",
       "Importacao, DirectQuery e Gateway", "Cartao, Mapa e Matriz"], 1,
      "Desktop (autoria, gratuito), Service (nuvem) e Mobile (consulta).") +
    q("O Power BI Desktop e:",
      ["Pago por usuario", "Gratuito para criar relatorios",
       "Usado apenas no celular", "Hospedado somente na Azure"], 1,
      "O Desktop e 100% gratuito; a instituicao paga ao compartilhar de forma privada na nuvem.") +
    q("Quando usar DirectQuery em vez de Importacao?",
      ["Para analise de historico de laudos emitidos",
       "Quando o painel exige dados ao vivo, como a entrada de requisicoes no IML",
       "Sempre que a base for pequena",
       "Quando nao ha conexao de rede"], 1,
      "DirectQuery consulta o banco em tempo real; Importacao copia os dados e e ideal para historico.") +
    q("O Principio dos 5 segundos, de Cole Nussbaumer Knaflic, diz que o dashboard deve:",
      ["Ter no minimo 5 abas", "Atualizar a cada 5 minutos",
       "Responder a pergunta principal em ate 5 segundos", "Usar 5 cores no maximo"], 2,
      "O gestor precisa entender a resposta principal em 5 segundos, sem cliques nem rolagem.") +
    q("No Power BI, o que o Bing Maps faz nativamente?",
      ["Criptografa os dados", "Geocodifica enderecos e municipios para o mapa",
       "Cria tabelas dinamicas", "Agenda a atualizacao"], 1,
      "Basta uma coluna de Municipio ou CEP para o mapa funcionar automaticamente.") +
    q("Para que serve um Slicer no dashboard?",
      ["Aumentar a velocidade da consulta", "Filtrar os dados de forma interativa, atualizando os visuais",
       "Publicar o relatorio", "Ocultar dados sensiveis"], 1,
      "O clique em um setor no slicer filtra automaticamente todos os visuais da pagina.") +
    q("Qual licenca e necessaria para publicar e compartilhar de forma privada na nuvem?",
      ["Nenhuma; o Service e gratuito", "Power BI Pro ou Premium",
       "Somente Office 365 Basico", "Uma conta pessoal @gmail"], 1,
      "O compartilhamento privado exige conta corporativa com licenca Pro ou Premium.") +
    q("Por que segregar workspaces na POLITEC?",
      ["Para deixar o sistema mais bonito", "Por seguranca da informacao e conformidade com a LGPD",
       "Porque o Power BI so permite um relatorio por workspace", "Para reduzir o custo de licenca"], 1,
      "Cada area ve apenas o que lhe compete; a segregacao e obrigacao legal e ganho de eficiencia.") +
    q("No workspace, qual papel pode apenas consultar dashboards, sem editar nem publicar?",
      ["Admin", "Membro", "Visualizador", "Proprietario"], 2,
      "Visualizador acessa e consulta; Membro publica/edita; Admin controla o workspace.") +
    q("Para que serve o On-premises Data Gateway?",
      ["Substituir o Power BI Desktop",
       "Criar um tunel seguro entre o servidor local e a nuvem, sem expor o servidor a internet",
       "Aumentar o numero de fontes suportadas para 200",
       "Gerar graficos automaticamente"], 1,
      "O gateway conecta o SQL Server local ao Service com criptografia, MFA e logs de auditoria.") +
    q("Um alerta visual no Power BI serve para:",
      ["Deixar o painel colorido", "Notificar o responsavel quando um KPI ultrapassa um limite",
       "Bloquear o acesso de visualizadores", "Reduzir o numero de visuais"], 1,
      "Ex.: avisar o Chefe do DNA por e-mail se o TAT medio ultrapassar 30 dias.") +
    q("Segundo a LGPD, um vazamento de dados deve ser comunicado a ANPD em ate:",
      ["24 horas", "72 horas", "7 dias", "30 dias"], 1,
      "A LGPD (Lei 13.709/2018) exige notificacao a ANPD em ate 72 horas.") +
    q("O que representam os KPIs TAT, SLA e QL, respectivamente?",
      ["Custo, lucro e receita",
       "Tempo de emissao, cumprimento de prazo e produtividade por perito",
       "Total, setor e laudo", "Taxa, sistema e qualidade"], 1,
      "TAT mede tempo; SLA mede conformidade de prazo; QL mede volume por perito.")
)

cad.section("glossario", "Glossario de Business Intelligence",
    glossary([
        ("Business Intelligence (BI)", "Conjunto de tecnologias e processos que transforma dados brutos em informacoes estrategicas para a gestao. Definicao de Howard Dresner (Gartner, 1989)."),
        ("Power BI Desktop", "Aplicativo gratuito de autoria onde os relatorios sao criados. Roda no PC do analista."),
        ("Power BI Service", "Plataforma na nuvem (app.powerbi.com) onde se publica, compartilha e colabora. Exige licenca Pro ou Premium para uso privado."),
        ("Power BI Mobile", "App para consultar dashboards e KPIs no celular, em qualquer lugar."),
        ("Importacao", "Modo que copia os dados para dentro do Power BI. Rapido e ideal para analise de historico."),
        ("DirectQuery", "Modo que consulta o banco em tempo real, sem copiar os dados localmente. Exige conexao estavel."),
        ("Power Query", "Motor de limpeza e transformacao do Power BI. Registra a limpeza como uma receita repetivel."),
        ("Slicer", "Segmentacao visual que filtra os dados de forma interativa, atualizando os visuais da pagina."),
        ("Workspace", "Espaco colaborativo no Service que agrupa dashboards e define permissoes de uma equipe ou projeto."),
        ("App (Aplicativo)", "Pacote de varios relatorios organizados por abas, publicado uma vez e distribuido a muitos usuarios."),
        ("On-premises Data Gateway", "Software que cria um tunel seguro e criptografado entre o servidor local e a nuvem, sem expor o servidor a internet."),
        ("TAT", "Turnaround Time - tempo medio entre a entrada da requisicao e a emissao do laudo. Indicador de eficiencia."),
        ("SLA", "Service Level Agreement - percentual de laudos emitidos dentro do prazo legal ou regulamentar. Mede conformidade."),
        ("QL", "Produtividade - quantidade de laudos emitidos por perito no periodo. Orienta redistribuicao de carga."),
        ("DAX", "Data Analysis Expressions - linguagem de formulas do Power BI, similar ao Excel, mas adaptavel ao contexto de filtro."),
        ("LGPD", "Lei Geral de Protecao de Dados (Lei 13.709/2018). Dispoe sobre o tratamento de dados pessoais, inclusive no setor publico."),
    ]) +
    tbl(["Indicador", "Formula / Fonte", "Significado"],
        [["TAT medio", "AVERAGEX + DATEDIFF (DAX)", "Tempo medio de emissao do laudo."],
         ["SLA", "Laudos no prazo / total", "Conformidade com o prazo legal."],
         ["QL", "Laudos por perito", "Produtividade individual no periodo."],
         ["Backlog", "Contagem de ID pendentes", "Volume aguardando processamento."]],
        num_cols=[])
)

cad.section("referencias", "Referencias e encerramento do Dia 4",
    p("As referencias que sustentam o Dia 4:") +
    tbl(["Autor / Fonte", "Obra", "Por que importa"],
        [["Howard Dresner (Gartner)", "Definicao de Business Intelligence (1989)",
          "A definicao classica de BI usada no modulo."],
         ["Ben Brumfield", "Lider do time do Power BI (Project Crescent, 2013-2015)",
          "O 'Pai do Power BI' e a democratizacao da analise de dados."],
         ["Cole Nussbaumer Knaflic", "'Storytelling com Dados' (2015)",
          "O Principio dos 5 segundos e a clareza na comunicacao de dados."],
         ["Jorge Camoes", "'Data Visualization in Excel and Power BI' (2021)",
          "Referencia de governanca: saber quem ve o que."],
         ["Microsoft Learn", "Trilhas oficiais de Power BI (learn.microsoft.com)",
          "A fonte oficial para aprofundar do basico ao avancado."],
         ["Comunidade Power BI", "community.powerbi.com",
          "Solucoes e respostas praticas da comunidade global."]],
        num_cols=[]) +
    ficha("g", "Fim do Modulo 6 - Basico",
        "Hoje o caminho completo foi percorrido: do conceito de BI a publicacao de um dashboard "
        "institucional real na nuvem, com governanca e LGPD.") +
    callout("tip", "Proximo encontro",
        "Dia 5 encerra a capacitacao consolidando o ecossistema de dados da POLITEC e os proximos "
        "passos do BI institucional (DAX, relacionamentos e governanca corporativa).")
)

cad.build()
