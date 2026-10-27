# -*- coding: utf-8 -*-
"""Gerador do caderno da Aula 7 - POLITEC/MT.

Formato: manha de paineis (BI) com 5 cenarios novos, detalhados passo a passo;
tarde de gargalo medido, proposta de automacao e digitalizacao, e aulao de
Antigravity (Google) com conexao do GitHub.

Rode:  python gerar_caderno_aula7.py
PDF:   python ..\\exportar_pdf.py 7
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from caderno_lib import (Caderno, p, h3, h4, ul, ol, checklist, ficha, callout, tbl,
                         code, step, q, aplicab, grid2, flow_h, kpi, antesdepois,
                         legenda, glossary, bar_chart)
import ptbr

cad = Caderno(
    out=str(pathlib.Path(__file__).resolve().parent / "caderno-dia7.html"),
    dia=7,
    kicker="Aula 7 · Gargalo medido, automação e Antigravity",
    headline="Do gargalo no painel à solução no GitHub",
    sub="Cinco processos novos da POLITEC/MT, cada um com o dashboard montado "
        "passo a passo, do Excel ao Power BI. A tarde parte do gargalo medido, "
        "passa pela proposta de automação e digitalização, e termina no aulão de "
        "Antigravity com a conexão do GitHub feita pelo navegador.",
    meta="Curso de Capacitacao POLITEC/MT · Professor Renato Rosa · Dia 7 · "
         "Modulo 9 (Gargalo medido + Automacao + Antigravity)",
    descricao="Caderno do Dia 7 do Curso de Capacitacao POLITEC/MT: cinco "
              "receitas de painel de processo (apreensao de armas, sinistro de "
              "transito, credenciamento de peritos, etilometria, atendimento e "
              "ouvidoria) com passo a passo detalhado do Excel ao Power BI, "
              "analise de gargalo, catalogo de automacao e digitalizacao, "
              "proposta de solucao por cenario, aulao de Google Antigravity e "
              "conexao da conta do GitHub pelo navegador."
)

# =================================================================
# DADOS MEDIDOS DOS 5 CENARIOS (fonte: Aula 7/datasets)
# =================================================================
CENARIOS = [
    {
        "n": 1,
        "pasta": "cenario1_apreensao_armas",
        "xlsx": "Cenario1_Apreensao_Armas.xlsx",
        "titulo": "Apreensão e perícia de armas",
        "sub": "Da apreensão na prisão até o encaminhamento à autoridade",
        "processo": "A arma apreendida passa pela conferência no IML, pelo registro no "
                    "SINARM, pela conferência documental, pela prova de fogo, pelo "
                    "laudo pericial e só então chega à autoridade.",
        "exec": 11312,
        "espera_pct": 92.1,
        "tat_h": 821.4,
        "gargalo": "Prova de fogo",
        "gargalo_share": 40.3,
        "gargalo_esp_h": 69.0,
        "segundo": "SINARM",
        "segundo_share": 21.3,
        "segundo_esp_h": 36.5,
        "top2": 61.6,
        "retrabalho": 14.6,
        "auto_pct": 12.5,
        "espera_total_h": 241981,
        "custo_exec": 1721349,
        "etapas": [
            ("Apreensão e lacre na prisão", 0.0, 1.2, 13.7),
            ("Transporte ao IML", 4.5, 7.7, 13.0),
            ("Recebimento e conferência", 6.4, 11.0, 11.9),
            ("Registro no SINARM", 21.3, 36.5, 14.6),
            ("Conferência documental", 13.5, 23.1, 12.5),
            ("Prova de fogo", 40.3, 69.0, 14.6),
            ("Laudo pericial e assinatura", 8.8, 15.1, 11.7),
            ("Encaminhamento e baixa", 5.2, 8.9, 12.4),
        ],
        "medida_extra": ("Armas no Mês",
                         "CALCULATE(\n"
                         "    DISTINCTCOUNT(fato[id_ciclo]),\n"
                         "    ALL(dim_calendario)\n"
                         ")"),
        "medida_extra_uso": "Cartão que mostra quantas armas entraram no mês, ao lado do "
                            "cartão de tempo. Serve para responder se a fila cresceu por "
                            "falta de perito ou por aumento da demanda.",
        "filtro_extra": ("tipo de atividade", "Mostra quanto de cada tipo de trabalho existe no gargalo"),
    },
    {
        "n": 2,
        "pasta": "cenario2_sinistro_transito",
        "xlsx": "Cenario2_Sinistro_Transito.xlsx",
        "titulo": "Sinistro de trânsito",
        "sub": "Da abertura do sinistro até o pagamento da indenização",
        "processo": "O sinistro é aberto pelo segurado, passa por triagem, vistoria "
                    "pericial, conferência de documentos, laudo, parecer com a "
                    "seguradora, liquidação e pagamento.",
        "exec": 11336,
        "espera_pct": 93.9,
        "tat_h": 696.7,
        "gargalo": "Documentos",
        "gargalo_share": 35.7,
        "gargalo_esp_h": 54.4,
        "segundo": "Parecer",
        "segundo_share": 19.3,
        "segundo_esp_h": 29.4,
        "top2": 55.0,
        "retrabalho": 17.6,
        "auto_pct": 37.5,
        "espera_total_h": 215980,
        "custo_exec": 1033127,
        "etapas": [
            ("Abertura do sinistro", 0.0, 0.0, 15.9),
            ("Triagem do processo", 6.6, 10.0, 15.5),
            ("Vistoria pericial", 12.3, 18.7, 17.6),
            ("Conferência de documentos", 35.7, 54.4, 17.0),
            ("Emissão do laudo", 9.3, 14.1, 14.4),
            ("Parecer com a seguradora", 19.3, 29.4, 17.3),
            ("Liquidação e pagamento", 12.4, 18.9, 15.7),
            ("Encerramento e arquivo", 4.5, 6.9, 15.5),
        ],
        "medida_extra": ("Documentos Pendentes",
                         "CALCULATE(\n"
                         "    COUNTROWS(\n"
                         "        FILTER(\n"
                         "            fato,\n"
                         "            fato[etapa_key] = 4\n"
                         "        )\n"
                         "    )\n"
                         ")"),
        "medida_extra_uso": "Cartão que conta quantos processos estão parados na conferência "
                            "de documentos. É o número que o atendimento precisa reduzir.",
        "filtro_extra": ("sistema", "Mostra o quanto do processo ainda roda em papel ou e-mail"),
    },
    {
        "n": 3,
        "pasta": "cenario3_credenciamento_peritos",
        "xlsx": "Cenario3_Credenciamento_Peritos.xlsx",
        "titulo": "Credenciamento de peritos",
        "sub": "Do edital até o repasse do pagamento do apoio pericial",
        "processo": "A chamada de apoio é publicada, o perito se inscreve, a área "
                    "técnica analisa o currículo, há entrevista, a comissão emite "
                    "parecer, a contratação é registrada e o repasse é feito.",
        "exec": 10152,
        "espera_pct": 94.6,
        "tat_h": 976.7,
        "gargalo": "Currículo",
        "gargalo_share": 31.3,
        "gargalo_esp_h": 68.5,
        "segundo": "Parecer",
        "segundo_share": 18.2,
        "segundo_esp_h": 39.7,
        "top2": 49.5,
        "retrabalho": 18.7,
        "auto_pct": 25.0,
        "espera_total_h": 277321,
        "custo_exec": 1517702,
        "etapas": [
            ("Publicação da chamada", 0.0, 0.0, 17.0),
            ("Inscrição e upload", 7.3, 16.1, 19.1),
            ("Conferência de requisitos", 10.6, 23.1, 18.2),
            ("Análise de currículo", 31.3, 68.5, 18.7),
            ("Entrevista e teste técnico", 15.1, 33.0, 18.0),
            ("Parecer da comissão", 18.2, 39.7, 18.9),
            ("Contratação e cadastro", 9.4, 20.6, 17.2),
            ("Repasse do pagamento", 8.0, 17.6, 17.0),
        ],
        "medida_extra": ("Pareceres no Mês",
                         "CALCULATE(\n"
                         "    COUNTROWS(\n"
                         "        FILTER(\n"
                         "            fato,\n"
                         "            fato[etapa_key] = 6\n"
                         "        )\n"
                         "    )\n"
                         ")"),
        "medida_extra_uso": "Cartão que mostra a produção da comissão. Serve para provar que a "
                            "fila do parecer cresce com a entrada de peritos.",
        "filtro_extra": ("projeto", "Mostra qual intervenção planejada já existe no processo"),
    },
    {
        "n": 4,
        "pasta": "cenario4_etilometria",
        "xlsx": "Cenario4_Etilometria.xlsx",
        "titulo": "Operação de etilometria",
        "sub": "Do acionamento da operação até o envio do processo ao DETRAN",
        "processo": "A operação é acionada, o aparelho é conferido, o teste é feito, a "
                    "prova é coletada, o auto de infração é emitido, o condutor é "
                    "notificado, a instrução corre e o processo vai ao DETRAN.",
        "exec": 12176,
        "espera_pct": 96.5,
        "tat_h": 856.0,
        "gargalo": "Auto de infração",
        "gargalo_share": 28.9,
        "gargalo_esp_h": 53.4,
        "segundo": "Conferência do aparelho",
        "segundo_share": 28.1,
        "segundo_esp_h": 51.8,
        "top2": 57.0,
        "retrabalho": 15.3,
        "auto_pct": 37.5,
        "espera_total_h": 280908,
        "custo_exec": 707836,
        "etapas": [
            ("Acionamento da operação", 0.0, 0.0, 14.5),
            ("Conferência do aparelho", 28.1, 51.8, 15.0),
            ("Teste do etilômetro", 5.4, 10.0, 15.3),
            ("Coleta de prova e contraprova", 11.7, 21.7, 14.3),
            ("Emissão do auto de infração", 28.9, 53.4, 13.9),
            ("Notificação ao condutor", 7.1, 13.1, 13.9),
            ("Instrução e decisão", 14.5, 26.8, 14.5),
            ("Envio ao DETRAN e arquivo", 4.2, 7.8, 14.3),
        ],
        "medida_extra": ("Testes no Mês",
                         "CALCULATE(\n"
                         "    DISTINCTCOUNT(fato[id_ciclo]),\n"
                         "    ALL(dim_calendario)\n"
                         ")"),
        "medida_extra_uso": "Cartão com o número de fiscalizações do mês. A comparação entre "
                            "esse cartão e o de espera mostra se a fila é de demanda ou de capacidade.",
        "filtro_extra": ("status da execução", "Revela quanto do processo foi devolvido ou cancelado"),
    },
    {
        "n": 5,
        "pasta": "cenario5_atendimento_ouvidoria",
        "xlsx": "Cenario5_Atendimento_Ouvidoria.xlsx",
        "titulo": "Atendimento ao público e ouvidoria",
        "sub": "Da abertura do protocolo até o encerramento e a pesquisa de satisfação",
        "processo": "O cidadão abre um protocolo, o assunto é classificado e "
                    "encaminhado, a área técnica instrui o caso e pede documentos, "
                    "emite parecer, responde, acompanha o prazo e encerra.",
        "exec": 13432,
        "espera_pct": 97.2,
        "tat_h": 822.6,
        "gargalo": "Instrução",
        "gargalo_share": 35.5,
        "gargalo_esp_h": 60.9,
        "segundo": "Resposta",
        "segundo_share": 18.7,
        "segundo_esp_h": 32.1,
        "top2": 54.2,
        "retrabalho": 20.5,
        "auto_pct": 37.5,
        "espera_total_h": 287825,
        "custo_exec": 485102,
        "etapas": [
            ("Abertura do protocolo", 0.0, 0.0, 17.8),
            ("Triagem e classificação", 8.0, 13.7, 17.5),
            ("Encaminhamento à área", 11.0, 18.8, 18.8),
            ("Instrução e pedido de documentos", 35.5, 60.9, 20.5),
            ("Parecer e decisão", 14.8, 25.3, 20.7),
            ("Resposta formal ao cidadão", 18.7, 32.1, 19.2),
            ("Comunicação de prazo", 7.7, 13.3, 18.9),
            ("Encerramento e pesquisa", 4.3, 7.3, 18.4),
        ],
        "medida_extra": ("Protocolos no Mês",
                         "CALCULATE(\n"
                         "    DISTINCTCOUNT(fato[id_ciclo]),\n"
                         "    ALL(dim_calendario)\n"
                         ")"),
        "medida_extra_uso": "Cartão com o volume de protocolos abertos. Serve para mostrar que a "
                            "fila de instrução cresce junto com a demanda do cidadão.",
        "filtro_extra": ("unidade responsável", "Mostra qual área técnica mais segura o prazo"),
    },
]

TOTAL_EXECUCOES = sum(c["exec"] for c in CENARIOS)

# =================================================================
# ABERTURA
# =================================================================
cad.grp("Abertura", "Cinco processos novos, medidos do primeiro clique ao painel publicado.")

cad.section("boas-vindas", "Bem-vindo ao caderno do Dia 7",
    p("Hoje não há introdução de conceito novo. A turma chega aqui com o "
      "mapeamento dos workflows já desenhado em Mermaid, na Aula 6, e com o "
      "modelo de dados, as medidas e a leitura de painel prontos. Por isso, o "
      "caderno entra direto nos cinco cenários, cada um com o dashboard "
      "montado do zero.") +
    p("A manhã entrega cinco painéis. A tarde parte do gargalo medido em cada "
      "painel, passa pela proposta de automação e digitalização, e termina no "
      "aulão de Antigravity, que é a ferramenta que vai transformar a proposta "
      "em código versionado no GitHub.") +
    ficha("a", "A regra do dia",
        "Nenhuma proposta de solução começa sem o número do painel. E nenhum "
        "código começa sem o número do painel. A ordem é: <b>medir</b>, "
        "<b>propor</b>, <b>construir</b>.") +
    kpi([
        ("5", "painéis construídos do zero"),
        ("58.408", "execuções de etapa medidas"),
        ("96", "passos em cada receita de painel"),
        ("3", "entregáveis por cenário"),
    ])
)

cad.section("mapa-do-dia", "Mapa do Dia 7: cinco cenários, três entregas",
    p("O dia tem três entregas, uma para cada turno da tarde e uma para a "
      "manhã. Cada cenário aparece três vezes: no painel, na proposta de "
      "solução e no código do mini app.") +
    tbl(["#", "Cenário", "Execuções", "Gargalo medido", "Share da espera"],
        [["<b>1</b>", "Apreensão e perícia de armas", "11.312", "Prova de fogo", "40,3%"],
         ["<b>2</b>", "Sinistro de trânsito", "11.336", "Conferência de documentos", "35,7%"],
         ["<b>3</b>", "Credenciamento de peritos", "10.152", "Análise de currículo", "31,3%"],
         ["<b>4</b>", "Operação de etilometria", "12.176", "Emissão do auto de infração", "28,9%"],
         ["<b>5</b>", "Atendimento e ouvidoria", "13.432", "Instrução", "35,5%"]],
        num_cols=[2, 4]) +
    grid2([
        ("Manhã (08h-12h): os cinco painéis",
         ul(["Receita 1: apreensão de armas, com o registro no SINARM e a prova de fogo",
             "Receita 2: sinistro de trânsito, com a fila de documentos do segurado",
             "Receita 3: credenciamento de peritos, com a fila de currículo e parecer",
             "Receita 4: etilometria, com a conferência do aparelho e o auto de infração",
             "Receita 5: ouvidoria, com a fila de instrução e resposta"])),
        ("Tarde (13h-17h): do número ao código",
         ul(["Parte 6: leitura comparada dos cinco gargalos medidos",
             "Parte 7: catálogo de automação e digitalização, com cálculo de ganho",
             "Parte 8: proposta de solução para cada um dos cinco cenários",
             "Partes 9 e 10: aulão de Antigravity e conexão do GitHub pelo navegador",
             "Parte 11: oito labs, do primeiro arquivo ao primeiro push"])),
    ]) +
    callout("note", "Como usar em sala",
        "Cada equipe fica com um cenário. Quem terminar o painel primeiro ajuda "
        "a equipe vizinha na etapa de revisão do modelo, que é a única parte do "
        "Power BI em que o erro aparece como número errado.")
)

cad.section("o-que-voce-ja-sabe", "O que você já traz da Aula 6",
    p("Nada do que segue repete a Aula 6. O que já foi feito aparece aqui "
      "como pré-requisito, para ninguém perder tempo.") +
    tbl(["Você já sabe fazer", "Onde vai usar hoje"],
        [["Modelar o processo em Mermaid", "Reconhecer a etapa do gargalo no diagrama AS-IS"],
         ["Montar o modelo estrela no Power BI", "Os cinco painéis, agora com outros processos"],
         ["Criar medidas DAX de espera e execução", "As medidas de Pareto de cada cenário"],
         ["Desenhar o TO-BE", "O TO-BE de cada solução proposta na Parte 8"],
         ["Escrever a hipótese em uma frase", "A hipótese de cada painel, conferida contra o dado"]],
        num_cols=[]) +
    callout("tip", "O que a Aula 6 não cobriu",
        "A Aula 6 parou no diagnóstico. Hoje o diagnóstico já está pronto, com "
        "número, e a tarde começa pela solução: o que automatizar, o que "
        "digitalizar, quanto custa e quanto render.")
)

# =================================================================
# DAX BASE (as mesmas 8 medidas da Aula 6, mais as 3 do Pareto)
# =================================================================
DAX_BASE = """Tempo Espera (h) =
SUM ( fato[tempo_espera_min] ) / 60


Tempo Execução (h) =
SUM ( fato[tempo_execucao_min] ) / 60


Tempo Total (h) =
[ Tempo Espera (h)] + [Tempo Execução (h)]


% Espera =
DIVIDE ( [Tempo Espera (h)], [Tempo Total (h)] )


Casos =
DISTINCTCOUNT ( fato[id_ciclo] )


TAT Médio (h) =
DIVIDE ( [Tempo Total (h)], [Casos] )


Espera Média (h) =
DIVIDE ( [Tempo Espera (h)], [Casos] )


Taxa Retrabalho =
DIVIDE (
    CALCULATE ( COUNTROWS ( fato ), fato[flag_retrabalho] = 1 ),
    COUNTROWS ( fato )
)"""


DAX_PARETO = """Rank da Etapa (espera) =
RANKX (
    ALL ( dim_etapa[etapa] ),
    CALCULATE ( [Tempo Espera (h)] ),
    ,
    DESC
)


% Acumulado da Espera =
VAR RankAtual =
    RANKX (
        ALL ( dim_etapa[etapa] ),
        CALCULATE ( [Tempo Espera (h)] ),
        ,
        DESC
    )
VAR EsperaAcumulada =
    CALCULATE (
        [Tempo Espera (h)],
        FILTER (
            ALL ( dim_etapa ),
            RANKX (
                ALL ( dim_etapa[etapa] ),
                CALCULATE ( [Tempo Espera (h)] ),
                ,
                DESC
            ) <= RankAtual
        )
    )
RETURN
    DIVIDE (
        EsperaAcumulada,
        CALCULATE ( [Tempo Espera (h)], ALL ( dim_etapa) )
    )


Espera por Etapa (h) =
CALCULATE ( [Tempo Espera (h)], ALL ( dim_etapa) )"""


# =================================================================
# RECEITA DETALHADA DE MONTAGEM DO PAINEL
# =================================================================
def receita(c):
    """Monta a receita completa de painel de um cenario.

    Devolve 4 blocos de HTML: a receita de 8 blocos, as medidas, a montagem
    visual a visual e a leitura do painel.
    """
    n = c["n"]
    wb = c["xlsx"]
    foco = c["gargalo"]
    etapas = c["etapas"]
    linha_espera = c["espera_pct"]
    lat = c["espera_total_h"]

    # ------------------------------------------------------------------
    # SECAO 1 - A RECEITA (8 BLOCOS)
    # ------------------------------------------------------------------
    s1 = (
        p(f"O roteiro abaixo monta o painel do cenário <b>{c['titulo']}</b> do "
          f"zero. Ele tem oito blocos, na ordem exata em que você vai clicar. "
          f"Não pule bloco. Se um bloco travar, anote o número do passo, pule "
          f"para o próximo e volte depois, porque o painel só fecha no fim.") +
        ficha("a", "O que este painel precisa provar",
            f"Que a maior parte do tempo do processo é espera, e que essa espera "
            f"se concentra em <b>{foco}</b>, com {c['gargalo_share']}% de toda a "
            f"espera do processo. Sem esse número, a proposta de solução da "
            f"Parte 8 vira opinião.") +
        callout("err", "O erro que mais aparece nesta receita",
            "Apontar o conector do Power BI para a <b>pasta</b> do cenário, em "
            "vez do <b>arquivo</b>. Aí o Power BI lê o LEIA-ME, o workbook do "
            "outro cenário e cria tabelas que não têm relação com nada. Se o "
            "nome da consulta aparecer como <code>Tabela1</code>, <code>Tabela2</code> "
            "e assim por diante, refaça a importação.") +
        tbl(["Aba do arquivo", "Grão", "Para que serve no painel"],
            [["<code>fato_execucao</code>", "1 linha = 1 execução de etapa",
              "Tempos de espera e execução, retrabalho, automação e custo"],
             ["<code>dim_etapa</code>", "1 linha = 1 etapa", "Nome, ordem e unidade padrão da etapa"],
             ["<code>dim_unidade</code>", "1 linha = 1 unidade", "Filtro por área, swimlane do processo"],
             ["<code>dim_sistema</code>", "1 linha = 1 sistema", "Mede quanto do processo ainda é papel"],
             ["<code>dim_tipo_atividade</code>", "1 linha = 1 tipo", "Separa trabalho, aprovação e decisão"],
             ["<code>dim_status_execucao</code>", "1 linha = 1 status", "Revela devoluções e cancelamentos"],
             ["<code>dim_projeto</code>", "1 linha = 1 projeto", "Mostra qual intervenção já existe"],
             ["<code>dim_calendario</code>", "1 linha = 1 dia", "Ano, mês, trimestre e linha do tempo"]],
            num_cols=[]) +
        callout("note", "Tempo de cada bloco",
            f"Bloco 1: 10 min. Bloco 2: 20 min. Bloco 3: 20 min. Bloco 4: 15 min. "
            f"Bloco 5: 25 min. Bloco 6: 25 min. Bloco 7: 40 min. Bloco 8: 25 min. "
            f"São 3 horas de montagem, com 1 hora de revisão e ajuste. O material "
            f"do arquivo <code>{wb}</code> já vem pronto, com {c['exec']} linhas "
            f"na fato.")
    )

    # ------------------------------------------------------------------
    # BLOCO 1
    # ------------------------------------------------------------------
    b1 = h3("Bloco 1 - Prepare o arquivo no Excel (10 min)") + step([
        ("1.1. Abra o workbook do seu cenário",
         f"Abra <code>{wb}</code>, que está na pasta "
         f"<code>Aula 7/datasets/{c['pasta']}/</code>. Se preferir, baixe pelo "
         f"link do arquivo na tabela da abertura deste caderno."),
        ("1.2. Leia a aba LEIA-ME até o fim",
         "A aba <code>LEIA-ME</code> tem quatro partes: o que tem no arquivo, os "
         "números medidos do dataset, o resumo por etapa e o passo a passo no "
         "Power BI. O resumo por etapa é o seu gabarito: no fim do dia, você "
         "compara o painel contra ele."),
        ("1.3. Anote os três números do bloco NUMEROS MEDIDOS",
         f"Anote: execuções = {c['exec']}; espera total = {lat:,} h; e a "
         f"percentual de espera = {linha_espera}%. Esses três números precisam "
         f"aparecer no painel. Se não aparecerem, o erro está na importação ou "
         f"na medida, não no dado.".replace(",", ".")),
        ("1.4. Confira as nove abas",
         "Você verá <code>LEIA-ME</code>, <code>fato_execucao</code> e as sete "
         "dimensões <code>dim_*</code>. Clique na seta ao lado de "
         "<code>fato_execucao</code> e veja se a linha de cabeçalho tem 16 "
         "colunas."),
        ("1.5. Confira a coluna etapa_key na dim_etapa",
         "Abra <code>dim_etapa</code>. A coluna <code>etapa_key</code> vai de 1 a "
         "8 e a coluna <code>sequencia</code> dá a ordem real do processo. É pela "
         "<code>sequencia</code> que o eixo do Pareto vai ser ordenado. "
         "Confira também a coluna <code>unidade_padrao</code>: ela diz quem "
         "cuida de cada etapa."),
        ("1.6. Confira se não há linha em branco no fim da fato",
         "Vá até o final da aba <code>fato_execucao</code> com Ctrl+End. Se a "
         "última linha estiver vazia, selecione a última linha preenchida e "
         "apague as de baixo. Arquivo com linha vazia no fim gera erro de "
         "contagem no painel."),
        ("1.7. Feche o Excel, mas mantenha o arquivo no mesmo lugar",
         "O Power BI lê o arquivo do disco. Se você mover o workbook para outra "
         "pasta depois de importar, a atualização falha. Deixe o arquivo onde "
         "está e não renomeie."),
        ("1.8. Abra o Power BI Desktop e crie um arquivo novo",
         "<b>Arquivo &rarr; Novo</b>. Logo depois, <b>Arquivo &rarr; Salvar "
         f"como</b>, e nomeie <code>Painel_Cenario{n}.pbix</code>. Salvar antes "
         "de importar evita perder 40 minutos de trabalho se o Power BI travar."),
    ])

    # ------------------------------------------------------------------
    # BLOCO 2
    # ------------------------------------------------------------------
    b2 = h3("Bloco 2 - Importe os dados no Power BI (20 min)") + step([
        ("2.1. Abra o conector de pasta de trabalho do Excel",
         "<b>Pagina Inicial &rarr; Obter dados &rarr; Mais</b>. Na janela que "
         "abrir, procure por <b>Pasta de trabalho do Excel</b> e clique em "
         "<b>Conectar</b>. Se o Power BI pedir versão de credenciais, escolha "
         "a versão atual."),
        ("2.2. Aponte para o arquivo, não para a pasta",
         "Navegue até <code>Aula 7/datasets/" + c["pasta"] + "/</code>, clique "
         f"uma vez no arquivo <code>{wb}</code> e clique em <b>Abrir</b>. "
         "Nunca selecione a pasta: isso mistura os arquivos dos outros cenários."),
        ("2.3. Escolha as oito abas de dados",
         "Aparece uma lista com as nove abas. Marque <b>fato_execucao</b> e as "
         "sete <code>dim_*</code>. Use <b>Ctrl</b> para marcar várias de uma "
         "vez, ou <b>Shift</b> para marcar um bloco inteiro de linhas."),
        ("2.4. Desmarque a aba LEIA-ME",
         "A aba <code>LEIA-ME</code> é documentação. Se ela for marcada, entra no "
         "modelo como uma tabela sem chave, e o Power BI reclama de tipo de "
         "dado misto quando você tenta relacionar."),
        ("2.5. Confira a pré-visualização de cada aba",
         "Cada aba marcada mostra um quadradinho com o nome e a primeira linha "
         "de dados. Clique em cada uma e olhe: a fato tem 16 colunas e as "
         "dimensões têm de 2 a 10. Uma aba que veio vazia ou com uma linha só "
         "significa que o arquivo está corrompido ou que você marked a aba "
         "errada."),
        ("2.6. Clique em Carregar",
         "O botão fica no canto inferior direito. O Power BI abre o Power Query "
         "com oito consultas, uma por aba. Espere a barra de carregamento "
         "terminar antes de tocar em qualquer coisa."),
        ("2.7. Renomeie as consultas uma por uma",
         "No painel <b>Consultas</b>, à esquerda, clique com o botão direito em "
         "cada consulta e escolha <b>Renomear</b>. Use estes nomes: <code>fato</code>, "
         "<code>etapa</code>, <code>unidade</code>, <code>sistema</code>, "
         "<code>tipo</code>, <code>status</code>, <code>projeto</code> e "
         "<code>calendario</code>. Os nomes aparecem no painel de campos e nos "
         "gráficos, então vale renomear agora."),
        ("2.8. Confira a contagem de linhas de cada consulta",
         "O número de linhas fica no rodapé do Power Query, à direita. A consulta "
         f"<code>fato</code> tem que mostrar {c['exec']} linhas. Se mostrar "
         "mais, alguma aba foi marcada duas vezes. Se mostrar menos, o filtro de "
         "cabeçalho foi aplicado antes de carregar."),
        ("2.9. Não edite nada ainda",
         "Parece LOSSO de esperar, mas editar na pressa é o caminho mais curto "
         "para um modelo quebrado. Feche e aplique primeiro, olhe o resultado, e "
         "só então volte para tratar."),
    ])

    # ------------------------------------------------------------------
    # BLOCO 3
    # ------------------------------------------------------------------
    b3 = h3("Bloco 3 - Trate os dados no Power Query (20 min)") + step([
        ("3.1. Use a primeira linha como cabeçalho, nas oito consultas",
         "Selecione a consulta <code>fato</code>. Na guia <b>Início</b>, clique "
         "em <b>Usar Primeira Linha como Cabeçalho</b>. Repita nas outras sete. "
         "Sem isso, os campos aparecem com nome V1, V2, V3, e nenhum nome de "
         "campo serve para a medida."),
        ("3.2. Confira os tipos de dado da fato",
         "Clique na coluna <code>tempo_espera_min</code>. O tipo aparece na "
         "faixa de opções, no alto. Tempos devem ser <b>Número Decimal</b>. "
         "Chaves como <code>etapa_key</code> devem ser <b>Número Inteiro</b>. "
         "Se aparecer <b>Texto</b>, clique com o botão direito no cabeçalho e "
         "escolha <b>Alterar tipo &rarr; Número Decimal</b>."),
        ("3.3. Confira os tipos das dimensões",
         "As chaves <code>*_key</code> são <b>Número Inteiro</b>. As colunas de "
         "nome, como <code>etapa</code> e <code>unidade</code>, são <b>Texto</b>. "
         "A coluna <code>sequencia</code> é <b>Número Inteiro</b>."),
        ("3.4. Corrija o tipo da coluna data do calendário",
         "Na consulta <code>calendario</code>, clique com o botão direito no "
         "cabeçalho de <code>data</code> e escolha <b>Alterar tipo &rarr; Data</b>. "
         "Depois vá em <b>Colunas Especiais &rarr; Ano e Mês</b> e marque "
         "<b>Ano</b> e <b>Nome do Mês</b>. Assim a linha do tempo já sai pronta."),
        ("3.5. Remova as colunas que o painel não vai usar",
         "Em cada dimensão, clique com o botão direito no cabeçalho e desmarque "
         "as colunas inúteis. Menos colunas significam modelo mais leve, "
         "carregamento mais rápido e um painel com menos ruído na lista de "
         "campos."),
        ("3.6. Remova linhas em branco",
         "<b>Início &rarr; Remover Linhas &rarr; Remover Linhas em Branco</b>. "
         "Rode nas oito consultas. É uma verificação, não uma correção: o "
         "arquivo já vem limpo, e o objetivo é você saber que está limpo."),
        ("3.7. Crie a coluna de ano no calendário, se ainda não existir",
         "Com a consulta <code>calendario</code> selecionada, use <b>Colunas "
         "Especiais &rarr; Ano e Mês &rarr; Ano</b>. O nome sai como "
         "<code>ano</code>. Essa coluna é a que liga a linha do tempo."),
        ("3.8. Feche e aplique",
         "<b>Início &rarr; Fechar e Aplicar</b>. O modelo aparece com oito "
         "tabelas. Se aparecer aviso de tipo misto, volte ao Power Query, "
         "clique na coluna indicada no aviso e corrija o tipo."),
        ("3.9. Marque a tabela de datas (isso é no Power BI, não no Power Query)",
         "Vá para o modo <b>Modelo</b>. Selecione a tabela <code>calendario</code> "
         "e use <b>Ferramenta de Tabela de Datas</b> na guia <b>Modelagem</b>. "
         "Escolha a coluna <code>data</code> e confirme. O aviso some e a "
         "segmentação de ano passa a funcionar."),
        ("3.10. Renomeie a consulta do calendário para data",
         "Clique com o botão direito na consulta <code>calendario</code> e "
         "escolha <b>Renomear</b>. Escreva <code>data</code>. É o nome da tabela "
         "de datas no modelo, e o nome que aparece no eixo de tempo dos gráficos."),
    ])

    # ------------------------------------------------------------------
    # BLOCO 4
    # ------------------------------------------------------------------
    b4 = h3("Bloco 4 - Monte o modelo (15 min)") + step([
        ("4.1. Vá para o modo Modelo",
         "No canto inferior esquerdo da janela do Power BI, clique em <b>Modelo</b>. "
         "As oito tabelas aparecem como caixas, e o painel de campos fica à "
         "esquerda."),
        ("4.2. Crie a relação da etapa",
         "Arraste o campo <code>etapa_key</code> da tabela <code>fato</code> até o "
         "campo <code>etapa_key</code> da tabela <code>etapa</code>. Solte o "
         "mouse. Surgem três caixas de configuração: <b>1:1</b>, <b>1:*</b> e "
         "<b>*:1</b>. Marque <b>1:*</b> e <b>Ativo</b>, que já vem marcado."),
        ("4.3. Crie a relação da unidade",
         "Arraste <code>unidade_key</code> da fato até <code>unidade_key</code> "
         "da unidade. De novo, <b>1:*</b> e filtro de uma direção, com a dimensão "
         "filtrando a fato."),
        ("4.4. Crie a relação do sistema",
         "Arraste <code>sistema_key</code> da fato até <code>sistema_key</code> da "
         "dimensão sistema. Este é o filtro que vai mostrar quanto do processo "
         "ainda roda em papel."),
        ("4.5. Crie a relação do tipo de atividade",
         "Arraste <code>tipo_atividade_key</code> da fato até a dimensão tipo. "
         "É a relação que separa tarefa manual de aprovação."),
        ("4.6. Crie a relação do status",
         "Arraste <code>status_execucao_key</code> da fato até a dimensão status. "
         "É a relação que revela devolução e cancelamento."),
        ("4.7. Crie a relação do projeto",
         "Arraste <code>projeto_key</code> da fato até a dimensão projeto. "
         "Serve para marcar sobre qual intervenção o dado já passa."),
        ("4.8. Crie a relação com o calendário, do jeito certo",
         "Arraste <code>data_inicio_key</code> da fato até <code>data_key</code> da "
         "tabela de datas. Deixe em <b>1:*</b>, filtro de uma direção, com a "
         "tabela de datas filtrando a fato. A seta da linha precisa apontar da "
         "dimensão para a fato."),
        ("4.9. Confira o sentido do filtro",
         "Passe o mouse por cima da linha da relação. A seta aparece no meio. "
         "Se ela apontar da fato para a dimensão, a segmentação de ano vai "
         "filtrar o eixo errado e o painel fica sem filtro nenhum. Nesse caso, "
         "clique com o botão direito na relação, escolha <b>Editar relações</b> e "
         "marque a seta dupla."),
        ("4.10. Esconda as chaves",
         "No painel de campos, clique na seta de contexto ao lado de cada "
         "<code>*_key</code> e escolha <b>Ocultar no relatório</b>. As chaves "
         "continuam no modelo, mas somem da lista de campos, e o painel fica "
         "limpo para quem vai usar."),
        ("4.11. Verifique a integridade do modelo",
         "<b>Modelagem &rarr; Verificar o modelo</b>. Não deve aparecer aviso de "
         "cardinalidade de muitos para muitos. Se aparecer, é porque a direção "
         "do filtro ficou duplicada em alguma relação."),
        ("4.12. Salve o arquivo",
         "<b>Arquivo &rarr; Salvar</b> (Ctrl+S). A partir de agora, qualquer erro "
         "de modelo aparece como número errado no painel, e o lugar mais provável "
         "é a relação."),
    ])

    # ------------------------------------------------------------------
    # BLOCO 5
    # ------------------------------------------------------------------
    b5 = h3("Bloco 5 - Crie as medidas (25 min)") + step([
        ("5.1. Crie a tabela de medidas",
         "<b>Modelagem &rarr; Inserir tabela de cálculo</b>. Nomeie "
         "<code>_Medidas</code>. Todas as medidas criadas a seguir vão para "
         "dentro dessa tabela."),
        ("5.2. Crie as três medidas de tempo, uma de cada vez",
         "Clique em <b>Nova medida</b> e cole o código de <b>Tempo Espera (h)</b>. "
         "Depois <b>Tempo Execução (h)</b>. Depois <b>Tempo Total (h)</b>. "
         "Cole exatamente como está, com a quebra de linha depois do nome da "
         "medida."),
        ("5.3. Crie as cinco medidas de leitura",
         "Agora <b>% Espera</b>, <b>Casos</b>, <b>TAT Médio (h)</b>, <b>Espera "
         "Média (h)</b> e <b>Taxa Retrabalho</b>. Todas usam <code>DIVIDE</code> "
         "nas divisões, para não aparecer erro de divisão por zero."),
        ("5.4. Formate cada medida assim que ela for criada",
         "Clique na medida e use <b>Ferramenta de Medida &rarr; Formatar</b>. "
         "Horas com uma casa decimal, percentual com uma casa decimal, contagem "
         "com separador de milhar. Sem formatação, o cartão mostra 44,1768 e "
         "ninguém lê."),
        ("5.5. Crie as três medidas do Pareto",
         "Cole <b>Rank da Etapa</b>, <b>% Acumulado da Espera</b> e <b>Espera por "
         "Etapa (h)</b>. O código está na seção seguinte deste caderno."),
        ("5.6. Crie a medida específica do cenário",
         f"Crie <b>{c['medida_extra'][0]}</b>, com o código que está na seção "
         "seguinte. Essa medida responde a uma pergunta que só este processo faz."),
        ("5.7. Coloque um comentário em cada medida",
         "Clique no ícone de comentário ao lado do nome da medida e escreva uma "
         "frase com o que ela responde. Quem abrir o painel depois entende a "
         "regra sem ler o código."),
        ("5.8. Organize as medidas em pastas",
         "Na barra de fórmulas, use <b>Criar pasta</b> para separar por tema: "
         "<code>Tempo</code>, <code>Leitura</code>, <code>Pareto</code> e "
         "<code>Cenario</code>. Com mais de dez medidas, a pasta economiza "
         "muito tempo de quem for montar o painel depois."),
        ("5.9. Teste cada medida em uma tabela antes de seguir",
         "No modo <b>Exibir</b>, insira um visual de tabela vazio. Arraste "
         "<code>etapa</code> e a medida <b>Tempo Espera (h)</b> para dentro dele. "
         "Compare os valores com o resumo por etapa da aba LEIA-ME. Esse é o "
         "teste mais rápido para achar erro de medida ou de filtro."),
        ("5.10. Apague a tabela de teste",
         "Depois do teste, apague o visual de tabela que você criou. Ele não faz "
         "parte do painel final e só ocupa espaço na página."),
        ("5.11. Confira se o total de espera bate com o arquivo",
         f"O valor de <b>Tempo Espera (h)</b> sem nenhum filtro tem que ser "
         f"{lat:,} horas. Divida por 60 para conferir em dias: são "
         f"{lat / 60:,.0f} dias.".replace(",", ".")),
        ("5.12. Salve de novo",
         "Ctrl+S. Agora o arquivo tem os dados e as medidas, mas ainda não tem "
         "nenhum visual."),
    ])

    # ------------------------------------------------------------------
    # BLOCO 6
    # ------------------------------------------------------------------
    b6 = h3("Bloco 6 - Monte o painel, parte 1: cartões e segmentações (25 min)") + step([
        ("6.1. Configure o tamanho da página antes de inserir qualquer coisa",
         "<b>Exibir &rarr; Tamanho da página</b>. Escolha <b>16:9</b> (1280 por "
         "720 pixels). Se o painel for para celular, escolha <b>Toolbox do "
         "telefone</b>. Configurar depois faz os visuais mudarem de tamanho e "
         "cruzarem com os outros."),
        ("6.2. Insira o primeiro cartão",
         "<b>Exibir &rarr; Cartão</b>. Ele aparece como um quadrado vazio. "
         "Arraste a medida <b>Casos</b> do painel de campos até o espaço "
         "<b>Valores</b> do cartão. O número aparece dentro dele."),
        ("6.3. Renomeie o cartão",
         "Dê dois cliques no nome do cartão, que vem como <b>Cartão</b>, e "
         "escreva <b>Casos no período</b>. Se o nome do cartão for igual ao "
         "nome da medida, o texto aparece duplicado embaixo do número."),
        ("6.4. Insira o segundo cartão: a espera média",
         "<b>Exibir &rarr; Cartão</b>. Arraste <b>Espera Média (h)</b> para "
         "<b>Valores</b>. Renomeie para <b>Espera média por caso</b>. Este é o "
         "cartão que responde à pergunta principal do painel."),
        ("6.5. Insira o terceiro cartão: a percentual de espera",
         "Arraste <b>% Espera</b> para <b>Valores</b>. Renomeie para "
         "<b>% do tempo é espera</b>. Formate o número em "
         "<b>Ferramenta de cartão &rarr; Formatar</b> e marque <b>Porcentagem</b> "
         "com uma casa decimal."),
        ("6.6. Insira o quarto cartão: a taxa de retrabalho",
         "Arraste <b>Taxa Retrabalho</b> para <b>Valores</b>. Renomeie para "
         "<b>Taxa de retrabalho</b>. Este cartão mostra quanto do trabalho "
         "precisa ser refeito."),
        ("6.7. Insira o quinto cartão, o do cenário",
         f"Arraste <b>{c['medida_extra'][0]}</b> para <b>Valores</b>. Renomeie "
         f"para <b>{c['medida_extra'][0]}</b>. A descrição do que ele responde "
         f"está na seção de medidas deste caderno."),
        ("6.8. Posicione os cinco cartões em uma linha no alto da página",
         "Arraste cada cartão até o topo. Deixe os cinco com a mesma altura e "
         "com o mesmo espaçamento entre eles. Use <b>Exibir &rarr; Alinhar "
         "&rarr; Alinhar ao topo</b> e depois <b>Distribuir horizontalmente</b>. "
         "Se os cartões ficarem tortos, selecione todos e use "
         "<b>Alinhar &rarr; Distribuir horizontalmente</b>."),
        ("6.9. Insira a primeira segmentação: o ano",
         "<b>Exibir &rarr; Segmentação de dados</b>. Arraste o campo "
         "<code>ano</code>, que está dentro da tabela de datas, para o espaço "
         "<b>Valores</b>. Em <b>Ferramentas de segmentação de dados</b>, "
         "escolha <b>Entre valores</b> e desmarque <b>Mostrar todos</b>."),
        ("6.10. Insira a segunda segmentação: a unidade",
         "Arraste <code>unidade</code> da dimensão unidade para <b>Valores</b>. "
         "Em <b>Ferramentas de segmentação de dados</b>, marque <b>Seleção "
         "múltipla</b> e <b>Ocultar itens sem dados</b>. Essa segmentação é a "
         "que responde por que área segura a fila."),
        ("6.11. Insira a terceira segmentação: a etapa",
         "Arraste <code>etapa</code> da dimensão etapa para <b>Valores</b>. "
         "Deixe a seleção múltipla ligada. Esta segmentação serve para você "
         "olhar uma etapa de cada vez enquanto monta os gráficos."),
        ("6.12. Insira a quarta segmentação, específica do cenário",
         f"Arraste <code>{c['filtro_extra'][0]}</code> para <b>Valores</b>. "
         f"Ela responde: {c['filtro_extra'][1]}."),
        ("6.13. Posicione as segmentações em uma coluna à esquerda",
         "Arraste as quatro segmentações para a coluna da esquerda, uma abaixo "
         "da outra, com a mesma largura. Deixe o resto da página livre para os "
         "gráficos."),
        ("6.14. Escreva um título para a página",
         "<b>Exibir &rarr; Cartão de texto</b>, ou clique na área vazia do "
         f"cabeçalho e digite <b>{c['titulo']} - leitura do gargalo</b>. "
         "Depois, com o texto selecionado, use <b>Formatar &rarr; Título do "
         "painel</b>."),
        ("6.15. Salve",
         "Ctrl+S. Os cinco cartões já contam a história principal: o volume, a "
         "espera média, o quanto do tempo é fila, o retrabalho e o número do "
         "cenário."),
    ])

    # ------------------------------------------------------------------
    # BLOCO 7
    # ------------------------------------------------------------------
    b7 = h3("Bloco 7 - Monte o painel, parte 2: os gráficos (40 min)") + step([
        ("7.1. Insira o gráfico de barras empilhadas",
         "<b>Exibir &rarr; Gráfico de barras empilhadas</b>. Arraste "
         "<code>etapa</code> da dimensão etapa para <b>Eixo Y</b> e as medidas "
         "<b>Tempo Espera (h)</b> e <b>Tempo Execução (h)</b> para <b>Valores</b>. "
         "O Power BI empilha a espera sobre a execução."),
        ("7.2. Ordene as etapas pela sequência do processo",
         "Clique com o botão direito em <code>etapa</code> no painel de campos "
         "e escolha <b>Classificar por coluna &rarr; sequencia</b>. Assim as "
         "etapas aparecem na ordem do fluxo, e não em ordem alfabética."),
        ("7.3. Renomeie o visual",
         "Dê dois cliques no nome do visual, que vem como <b>Nome do visual</b>, "
         "e escreva <b>Onde o tempo passa</b>. O nome do visual aparece no "
         "modelo e nas referências de outros visuais."),
        ("7.4. Destaque a etapa do gargalo na cor",
         f"Selecione a barra de <b>{foco}</b>. Use <b>Formatar &rarr; Barra "
         "&rarr; Cores</b> e escolha uma cor de destaque. Depois, no mesmo "
         "menu, em <b>Negativo</b>, deixe as demais barras na cor padrão. "
         "Duas cores são suficientes: destaque e neutro."),
        ("7.5. Renomeie as séries do gráfico",
         "No painel de campos, o nome que aparece ao lado de cada medida é o "
         "nome da série. Clique no nome da série e edite para <b>Espera</b> e "
         "<b>Execução</b>. Sem isso, o gráfico mostra o nome técnico da medida."),
        ("7.6. Insira o Pareto",
         "<b>Exibir &rarr; Gráfico de barras e colunas</b>. Arraste "
         "<code>etapa</code> para <b>Eixo X</b> e <b>Espera por Etapa (h)</b> "
         "para <b>Eixo Y</b>. Depois clique no botão <b>Analyze</b> (o símbolo "
         "de três pontos) no canto superior direito do visual e marque "
         "<b>Adicionar valor ao eixo secundário</b>."),
        ("7.7. Arraste a linha de acumulado para o eixo secundário",
         "Arraste <b>% Acumulado da Espera</b> para <b>Eixo Y secundário</b>. "
         "O gráfico passa a ter duas escalas: barras para as horas e linha para "
         "o percentual acumulado."),
        ("7.8. Fixe a escala do eixo secundário de 0% a 100%",
         "Com o eixo secundário selecionado, use <b>Formatar &rarr; Eixo Y "
         "&rarr; Escala</b>. Em <b>Mínimo</b>, escreva <b>0%</b>. Em "
         "<b>Máximo</b>, escreva <b>100%</b>. Em <b>Unidade de exibição</b>, "
         "deixe como porcentagem. Sem isso, a linha sai com escala própria e "
         "não se lê como Pareto."),
        ("7.9. Ordene o Pareto pela espera, não pela sequência",
         "No gráfico, clique com o botão direito em <code>etapa</code> e "
         "escolha <b>Classificar por coluna &rarr; Rank da Etapa</b>. As "
         "barras passam a ficar em ordem decrescente de espera, que é a ordem "
         "do Pareto."),
        ("7.10. Insira a linha do tempo",
         "<b>Exibir &rarr; Gráfico de linhas</b>. Arraste <code>data</code> da "
         "tabela de datas para <b>Eixo X</b> e <b>Tempo Espera (h)</b> para "
         "<b>Valores</b>. Em <b>Ferramenta de eixo X</b>, amplie o tipo para "
         "<b>Mês</b> e depois <b>Ano</b>, para o gráfico mostrar doze meses e "
         "depois os três anos."),
        ("7.11. Insira a matriz de etapa por unidade",
         "<b>Exibir &rarr; Matriz</b>. Arraste <code>etapa</code> para "
         "<b>Linhas</b>, <code>unidade</code> para <b>Colunas</b> e "
         "<b>Tempo Espera (h)</b> para <b>Valores</b>. Essa matriz é o "
         "retrato da fila: ela mostra qual área segura a etapa que mais espera."),
        ("7.12. Aplique formatação condicional na matriz",
         "Com a matriz selecionada, use <b>Formatar &rarr; Células &rarr; "
         "Cores de fundo</b> e escolha <b>Escala de cores</b>. Escolha uma "
         "escala de vermelho para o menor e verde para o maior, ou o inverso. "
         "O padrão é vermelho para o valor mais alto, porque o valor mais alto "
         "é onde a fila está."),
        ("7.13. Insira o gráfico de barras da espera por etapa",
         "<b>Exibir &rarr; Gráfico de barras</b>. Arraste <code>etapa</code> "
         "para <b>Eixo Y</b> e <b>Espera Média (h)</b> para <b>Valores</b>. "
         "Este é o gráfico que você vai fotografar para o relatório: ele mostra "
         "as horas de fila que cada etapa entrega para cada caso."),
        ("7.14. Insira o gráfico de sistema, para medir a digitalização",
         "<b>Exibir &rarr; Gráfico de barras empilhadas</b>. Arraste "
         "<code>sistema</code> para <b>Eixo Y</b> e <b>Tempo Espera (h)</b> "
         "para <b>Valores</b>. Este gráfico responde: quanto do processo ainda "
         "está em papel, e-mail ou planilha?"),
        ("7.15. Organize os visuais na tela",
         "Linha de cima: os cinco cartões. Faixa do meio, à esquerda: as barras "
         "empilhadas, com cerca de 420 pixels de largura. Ao lado: o Pareto. "
         "Faixa de baixo, à esquerda: a linha do tempo. Ao lado: a matriz. "
         "Na direita, empilhados: o gráfico de barras por etapa e o de sistema."),
        ("7.16. Tire o título de todos os visuais, menos o do meio",
         "Para cada visual que não for o gráfico principal, abra <b>Formatar "
         "&rarr; Título</b> e marque <b>Desligar</b>. O painel fica mais limpo "
         "e o gráfico principal ganha destaque."),
        ("7.17. Configure as interações entre visuais",
         "Em cada visual, use <b>Formatar &rarr; Editar interações</b>. Deixe "
         "marcado <b>Sem seleção</b> para o gráfico de barras por etapa, para "
         "que clicar em uma etapa dele não filtre os outros gráficos. Para o "
         "Pareto, deixe o filtro funcionando."),
        ("7.18. Salve",
         "Ctrl+S. O painel está pronto. Falta conferir os números."),
    ])

    # ------------------------------------------------------------------
    # BLOCO 8
    # ------------------------------------------------------------------
    b8 = h3("Bloco 8 - Formate, salve e publique (25 min)") + step([
        ("8.1. Confira os cinco cartões contra a aba LEIA-ME",
         f"O cartão de casos tem que mostrar perto de {c['exec'] // 8:,} "
         f"execuções no total do período. O cartão de espera média tem que "
         f"mostrar o valor da coluna <i>Espera media (h)</i> do resumo por "
         f"etapa, multiplicado pelo número de etapas.".replace(",", ".")),
        ("8.2. Confira o Pareto contra o número do gargalo",
         f"A primeira barra do Pareto tem que ser <b>{foco}</b>, e a segunda "
         f"tem que ser <b>{c['segundo']}</b>. As duas juntas somam "
         f"{c['top2']}% de toda a espera. Se a ordem estiver diferente, o "
         f"problema é a medida <b>Rank da Etapa</b>, não o gráfico."),
        ("8.3. Confira a matriz",
         "A linha de <b>" + foco + "</b> tem que mostrar mais espera do que "
         "as outras linhas. É nessa matriz que você descobre qual área segura "
         "a fila: clique na célula de maior valor e veja o nome da unidade no "
         "canto do visual."),
        ("8.4. Teste os filtros",
         "Clique em 2024 na segmentação de ano. Veja se o Pareto muda de "
         "tamanho. Clique em uma unidade. Veja se a matriz muda. Se nada "
         "mudar, o filtro não está chegando aos visuais: volte ao modelo e "
         "confira a direção do filtro das relações."),
        ("8.5. Teste a seleção de etapa",
         "Na segmentação de etapa, marque só <b>" + foco + "</b>. Os gráficos "
         "devem mostrar só aquela etapa. Desmarque depois."),
        ("8.6. Aumente o tamanho da fonte dos rótulos",
         "Com um visual selecionado, use <b>Formatar &rarr; Eixo Y &rarr; Texto "
         "&rarr; Tamanho</b> e leve para 11 ou 12. Nomes de etapa são longos e "
         "ficam cortados no tamanho padrão."),
        ("8.7. Coloque o logo da unidade no canto do painel",
         "<b>Exibir &rarr; Imagens</b> e arraste o arquivo de logo. Deixe no "
         "canto superior direito, pequeno. Se não houver logo, pule este passo."),
        ("8.8. Use um tema de cores consistente",
         "<b>Exibir &rarr; Temas</b>. Escolha um tema e depois vá em <b>Configurações "
         "&rarr; Temas &rarr; Personalizar tema</b> e troque a cor de destaque "
         "pela cor da sua unidade. O painel inteiro herda a mudança, inclusive "
         "os cartões e o Pareto."),
        ("8.9. Salve o arquivo .pbix",
         "<b>Arquivo &rarr; Salvar</b>. O nome do arquivo é o mesmo do começo: "
         "<code>Painel_Cenario" + str(n) + ".pbix</code>."),
        ("8.10. Publique no Power BI Service",
         "<b>Publicar</b> no topo. Escolha o espaço de trabalho e o nome "
         "<b>Painel do processo - cenário " + str(n) + "</b>. Se você não tem "
         "conta no Service, pule este passo e guarde o .pbix."),
        ("8.11. Escreva a hipótese em uma frase, e só depois",
         "Abra o caderno e responda: <i>onde o processo deste cenário perde "
         "tempo, e quanto</i>. A frase tem que ter o número. Exemplo: "
         f"<i>Em {c['titulo']}, {foco} concentra {c['gargalo_share']}% da "
         f"espera do processo, com {c['gargalo_esp_h']} horas de fila por "
         f"caso</i>."),
        ("8.12. Guarde uma captura de tela do painel",
         "Print da página inteira, com a segmentação de ano em <b>Todos</b> e o "
         "Pareto visível. Esse é o insumo da proposta de solução da Parte 8."),
    ])

    return s1 + b1 + b2 + b3 + b4 + b5 + b6 + b7 + b8


# =================================================================
# SECAO DE MEDIDAS DO CENARIO
# =================================================================
def secao_medidas(c):
    medidas_cenario = (
        h3(f"A medida que só o cenário {c['n']} tem") +
        p(f"Além das 11 medidas iguais para todos os cenários, este processo "
          f"precisa de uma medida que responde a uma pergunta específica. É a "
          f"medida <b>{c['medida_extra'][0]}</b>.") +
        code(c["medida_extra"][1], "dax") +
        p(f"Para que ela serve: {c['medida_extra_uso']}") +
        callout("note", "Como criar uma medida nova em 30 segundos",
                "<b>Modelagem &rarr; Nova medida</b>. Digite o nome, aperte "
                "Enter, cole o código abaixo do nome e aperte Enter de novo. "
                "Se a medida ficar vermelha, é erro de sintaxe: confira as "
                "parênteses. Se ficar preta mas mostrar valor errado, é erro de "
                "lógica: confira o nome da etapa dentro do código."))

    return (
        p(f"Todo painel deste dia usa as mesmas 11 medidas. Elas estão aqui "
          f"completas, na ordem em que você deve criar, para você não ter que "
          f"adivinhar nada.") +
        h3("As 8 medidas base, na ordem de criação") +
        code(DAX_BASE, "dax") +
        h3("As 3 medidas do Pareto") +
        p("O Pareto ordena as etapas pela espera e mostra quanto de espera está "
          "acumulado nas primeiras. Sem essas três medidas, o gráfico de "
          "barras e colunas não tem como mostrar a linha de acumulado.") +
        code(DAX_PARETO, "dax") +
        medidas_cenario +
        h3("As medidas de formatação, campo a campo") +
        tbl(["Medida", "Tipo", "Formato", "Onde aparece"],
            [["Tempo Espera (h)", "Soma de minutos dividida por 60", "1 casa decimal",
              "Barras empilhadas, Pareto e matriz"],
             ["Tempo Execução (h)", "Soma de minutos dividida por 60", "1 casa decimal",
              "Barras empilhadas e cartão de tempo"],
             ["Tempo Total (h)", "Soma das duas medidas de tempo", "1 casa decimal", "Cartão de tempo"],
             ["% Espera", "DIVIDE entre espera e total", "Porcentagem, 1 casa",
              "Cartão de percentual"],
             ["Casos", "DISTINCTCOUNT de id_ciclo", "Separador de milhar", "Cartão de volume"],
             ["TAT Médio (h)", "Total dividido pelos casos", "1 casa decimal", "Cartão de tempo de ciclo"],
             ["Espera Média (h)", "Espera dividida pelos casos", "1 casa decimal", "Cartão de fila"],
             ["Taxa Retrabalho", "DIVIDE entre linhas com flag e total", "Porcentagem, 1 casa",
              "Cartão de retrabalho"],
             ["Rank da Etapa", "RANKX sobre a espera", "Inteiro", "Ordenação do Pareto"],
             ["% Acumulado da Espera", "Filtro por rank e DIVIDE", "Porcentagem, 1 casa",
              "Linha do Pareto"],
             ["Espera por Etapa (h)", "CALCULATE com ALL na etapa", "1 casa decimal", "Barras do Pareto"]],
            num_cols=[]) +
        callout("err", "Três erros que quebram o painel",
                "<b>1.</b> Usar <code>SUM</code> no lugar de "
                "<code>DISTINCTCOUNT</code> na medida <b>Casos</b>: o cartão passa "
                "a mostrar o número de execuções de etapa, que é cerca de oito "
                "vezes maior que o número de casos. <b>2.</b> Esquecer o "
                "<code>ALL ( dim_etapa )</code> dentro de <b>Espera por Etapa "
                "(h)</b>: todas as barras do Pareto ficam com o mesmo valor. "
                "<b>3.</b> Não usar <code>DIVIDE</code>: quando o filtro deixa a "
                "medida sem linha, aparece o erro de divisão por zero no cartão "
                "e o painel inteiro fica marcado em vermelho no relatório.") +
        callout("tip", "Como conferir uma medida sem gastar tempo",
                "Insira um visual de tabela vazio, arraste a etapa e a medida, e "
                "compare com a aba LEIA-ME do workbook. Se o número bater, a "
                "medida está certa e o erro está no visual. Se não bater, o "
                "erro está na medida ou na relação.")
    )


# =================================================================
# SECAO DE LEITURA DO PAINEL
# =================================================================
def secao_leitura(c):
    etapas = c["etapas"]
    rotulos = [e[0] for e in etapas]
    valores = [e[1] for e in etapas]
    maior = max(range(len(valores)), key=lambda i: valores[i])

    return (
        p(f"O painel do cenário <b>{c['titulo']}</b> está pronto. Agora vem a "
          f"parte que separa um painel de uma decoração: ler o painel em 60 "
          f"segundos e escrever a hipótese em uma frase, com número.") +
        h3("Os quatro gráficos na ordem em que você olha") +
        ol([
            "<b>Cartão de espera média.</b> Quantas horas, em média, cada caso "
            f"passa parado na fila. Aqui: {c['tat_h']:.1f} horas de tempo total "
            f"por caso, das quais {c['espera_pct']}% são espera.",
            "<b>Pareto.</b> Qual etapa concentra a fila. Aqui: "
            f"<b>{c['gargalo']}</b>, com {c['gargalo_share']}% de toda a espera, "
            f"seguida de <b>{c['segundo']}</b>, com {c['segundo_share']}%. As duas "
            f"juntas somam {c['top2']}%.",
            "<b>Matriz etapa por unidade.</b> Quem segura a fila. A célula mais "
            "escura da linha do gargalo diz a área responsável.",
            "<b>Linha do tempo.</b> A fila cresceu por demanda ou por "
            "capacidade? Se o número de casos e a espera sobem juntos, é "
            "demanda. Se os casos ficam e a espera sobe, é falta de gente ou de "
            "equipamento na etapa.",
        ]) +
        bar_chart(rotulos, valores,
                  f"Onde a espera se esconde - {c['titulo']}",
                  f"Participação de cada etapa na espera total (%). Gargalo: {c['gargalo']}",
                  destaque=maior, fmt="{:.1f}%") +
        h3("A hipótese, escrita na forma que a turma vai usar") +
        ficha("g", "Hipótese do cenário",
            f"<b>Em {c['titulo']}, {c['gargalo']} concentra "
            f"{c['gargalo_share']}% de toda a espera do processo, o que dá "
            f"{c['gargalo_esp_h']} horas de fila por caso; com {c['segundo']}, "
            f"são {c['top2']}% da espera em duas etapas. Como a espera total é "
            f"{c['espera_pct']}% do tempo do processo, mexer em outra etapa "
            f"não muda o resultado do caso.</b>") +
        tbl(["Pergunta que o painel responde", "Resposta com número"],
            [["Quanto do tempo do processo é espera?", f"{c['espera_pct']}%"],
             ["Qual etapa é o gargalo?", f"{c['gargalo']}, com {c['gargalo_share']}% da espera"],
             ["Quanto o caso espera na etapa do gargalo?", f"{c['gargalo_esp_h']} horas por caso"],
             ["Qual é a segunda etapa do gargalo?", f"{c['segundo']}, com {c['segundo_share']}%"],
             ["Quanto do trabalho precisa ser refeito?", f"{c['retrabalho']}% das execuções"],
             ["Quanto do processo já é automatizado?", f"{c['auto_pct']}% das execuções"],
             ["Qual é o tempo de ciclo médio do caso?", f"{c['tat_h']:.1f} horas"],
             ["Quanto tempo de fila o processo acumulou no período?",
              f"{c['espera_total_h']:,} horas".replace(",", ".")]],
            num_cols=[1]) +
        callout("err", "O que o painel não prova",
                "O painel mostra <b>onde</b> a fila está, não <b>por que</b>. A "
                "causa vem da conversa com quem trabalha na etapa: escala "
                "insuficiente, sistema que não integra, documento que chega "
                "incompleto, retrabalho por devolução. Escrever a causa antes "
                "de ouvir a área é chute, e o chute se disfarça de painel.") +
        aplicab(
            f"Na reunião de apresentação do cenário {c['n']}, quando alguém "
            f"perguntar por que o processo demora.",
            f"Porque a pergunta tem resposta no dado: {c['gargalo_share']}% da "
            f"espera em uma etapa muda a prioridade de qualquer projeto.",
            f"A equipe do IML apresenta: <i>a arma passa "
            f"{c['gargalo_esp_h']:.0f} horas na fila da prova de fogo, e são "
            f"{c['gargalo_share']}% de toda a espera do processo de armas</i>. "
            f"Com esse número, o pedido de fila priorizada deixa de ser "
            f"preferência e vira requisito.")
    )


# =================================================================
# OS 5 CENARIOS
# =================================================================
for c in CENARIOS:
    n = c["n"]
    cad.grp(f"Parte {n} - Cenário {n}: {c['titulo']}",
            f"{c['sub']}. Gargalo medido: {c['gargalo']}, com "
            f"{c['gargalo_share']}% de toda a espera do processo.")

    cad.section(f"cenario{n}-contexto", f"Cenário {n}: o processo e o que o painel precisa provar",
        p(c["processo"]) +
        ficha("a", "A pergunta que este painel responde",
            f"Onde o caso espera neste processo, quanto tempo ele espera e quem "
            f"segura a fila. A resposta medida é <b>{c['gargalo']}</b>, com "
            f"<b>{c['gargalo_share']}%</b> da espera total.") +
        tbl(["#", "Etapa", "Share da espera", "Espera média por caso (h)", "Retrabalho"],
            [[i + 1, e[0], f"{e[1]:.1f}%", f"{e[2]:.1f}", f"{e[3]:.1f}%"]
             for i, e in enumerate(c["etapas"])],
            num_cols=[2, 3, 4]) +
        ul([
            f"<b>Volume:</b> {c['exec']:,} execuções de etapa medidas no "
            f"período.".replace(",", "."),
            f"<b>Tempo de ciclo médio por caso:</b> {c['tat_h']:.1f} horas.",
            f"<b>Espera acumulada no período:</b> {c['espera_total_h']:,} horas.".replace(",", "."),
            f"<b>Automatização atual:</b> {c['auto_pct']}% das execuções.",
            f"<b>Custo de execução registrado:</b> R$ {c['custo_exec']:,}.".replace(",", "."),
        ]) +
        callout("note", "De onde vêm esses números",
                "Todos os números desta tabela saíram do arquivo "
                f"<code>{c['xlsx']}</code>, aba <code>LEIA-ME</code>, bloco "
                "<i>RESUMO POR ETAPA</i>. Quando você montar o seu painel, os "
                "números precisam bater com esses. Se não baterem, o erro está "
                "na importação, no modelo ou na medida.") +
        aplicab(
            f"Quando a equipe do cenário {n} for apresentar o painel para a "
            f"diretoria.",
            "Porque a apresentação começa pelo gargalo, e o gargalo é um número "
            "com fonte, não uma impressão.",
            f"A frase de abertura: <i>Em {c['titulo']}, {c['gargalo_share']}% da "
            f"espera do processo está em uma única etapa, e são "
            f"{c['gargalo_esp_h']:.0f} horas por caso</i>.")
    )

    cad.section(f"cenario{n}-receita",
                f"Cenário {n}: a receita completa do painel, do Excel ao gráfico",
                receita(c))

    cad.section(f"cenario{n}-medidas",
                f"Cenário {n}: as 11 medidas DAX, prontas para copiar",
                secao_medidas(c))

    cad.section(f"cenario{n}-leitura",
                f"Cenário {n}: ler o painel em 60 segundos e escrever a hipótese",
                secao_leitura(c))


# =================================================================
# PARTE 6 - DO PAINEL AO GARGALO
# =================================================================
REDUCAO = {1: 0.60, 2: 0.60, 3: 0.60, 4: 0.50, 5: 0.60}
VALOR_HORA_FILA = 42.00


def ganho(c):
    """Retorna (horas por ano liberadas, valor por ano, share dos 5)."""
    espera_gargalo = c["espera_total_h"] * c["gargalo_share"] / 100
    h_3anos = espera_gargalo * REDUCAO[c["n"]]
    h_ano = h_3anos / 3
    return h_ano, h_ano * VALOR_HORA_FILA


cad.grp("Parte 6 - Manhã: do painel ao gargalo",
        "Os cinco painéis na mesma régua: onde a fila está, quanto custa e por onde começar.")

cad.section("cinco-gargalos", "Os cinco gargalos na mesma régua",
    p("Cada painel foi lido sozinho. Agora os cinco entram na mesma régua, e "
      "a comparação mostra um padrão que nenhum dashboard mostra sozinho: em "
      "todos os processos, a espera é o processo.") +
    tbl(["Cenário", "Gargalo medido", "Share da espera", "2ª etapa", "Top 2", "Espera do processo"],
        [[f"<b>{c['n']}</b>. {c['titulo']}", f"<b>{c['gargalo']}</b>",
          f"{c['gargalo_share']}%", f"{c['segundo']} ({c['segundo_share']}%)",
          f"{c['top2']}%", f"{c['espera_pct']}%"] for c in CENARIOS],
        num_cols=[2, 4, 5]) +
    bar_chart([f"C{c['n']}" for c in CENARIOS],
              [c["gargalo_share"] for c in CENARIOS],
              "Share da espera no gargalo de cada cenário",
              "Quanto da espera do processo está na etapa mais crítica, em %",
              destaque=0, fmt="{:.1f}%") +
    callout("note", "O padrão que aparece nos cinco",
        f"O share do gargalo fica entre {min(c['gargalo_share'] for c in CENARIOS)}% "
        f"e {max(c['gargalo_share'] for c in CENARIOS)}%. Nenhum processo tem "
        f"gargalo espalhado. Por isso, a estratégia não é redesenhar tudo: é "
        f"atacar uma etapa por processo.") +
    tbl(["Cenário", "Horas de fila liberadas por ano", "Valor por ano (R$ 42,00/h)"],
        [[f"<b>{c['n']}</b>. {c['titulo']}", f"{ganho(c)[0]:,.0f}".replace(",", "."),
          f"{ganho(c)[1]:,.0f}".replace(",", ".")] for c in CENARIOS],
        num_cols=[1, 2]) +
    callout("err", "Como ler esse valor sem se enganar",
            "O valor por ano é <b>capacidade liberada</b>, e não dinheiro no "
            "caixa. A hora que deixa de ser gasta em fila não vira economia "
            "automática: ela vira fila menor, e fila menor vira prazo menor, e "
            "prazo menor vira mais casos atendidos, e aí sim vira economia. Quem "
            "apresenta a capacidade liberada como economia está vendendo o "
            "mesmo dinheiro duas vezes.")
)

cad.section("espera-vs-execucao", "Espera x execução: o padrão dos cinco processos",
    p("Todo processo tem dois tempos: o tempo em que alguém trabalha e o tempo "
      "em que o caso fica parado. Nos cinco processos da POLITEC, o segundo "
      "tempo domina.") +
    tbl(["Cenário", "Espera do processo", "Execução do processo", "Relação"],
        [[f"<b>{c['n']}</b>. {c['titulo']}", f"{c['espera_pct']}%",
          f"{round(100 - c['espera_pct'], 1)}%",
          f"1 hora de trabalho para {c['espera_pct'] / (100 - c['espera_pct']):.0f} horas de fila"]
         for c in CENARIOS],
        num_cols=[1, 2]) +
    callout("err", "A conclusão errada que todo mundo tira",
            "<i>Tem gente demais, precisa contratar mais gente.</i> Não. Se a "
            "fila é de espera por documento, por conferência, por assinatura de "
            "quem estava em reunião, contratar não resolve: o contratado vira "
            "mais gente esperando o mesmo documento. O dado aponta o tipo de "
            "espera: fila de pessoas, fila de sistema, fila de documento ou "
            "fila de aprovação.") +
    tbl(["Tipo de espera", "Como aparece no painel", "Intervenção típica"],
        [["Fila de pessoas", "Etapa com muita espera e pouco trabalho",
          "Priorização, escala, polymorphism de capacidade"],
         ["Fila de sistema", "Etapa ligada a sistema não integrado",
          "Integração, automação de digitação, leitura automática de documento"],
         ["Fila de documento", "Etapa que espera documento de fora",
          "Upload pelo cidadão, alerta automático,minuta pronta"],
         ["Fila de aprovação", "Etapa de parecer ou autorização com retrabalho",
          "Regra de decisão, alçada, parecer com modelo preenchido"],
         ["Fila de equipamento", "Etapa com espera e alta concentração de trabalho",
          "Escala de equipamentos, leitura por imagem, teste automatizado"]],
        num_cols=[]) +
    callout("tip", "Como separar fila de pessoa de fila de documento",
            "Olhe o gráfico de <b>sistema</b> do painel. Se a etapa do gargalo "
            "estiver ligada a sistema não integrado ou a papel, a fila é de "
            "sistema e de documento. Se estiver ligada ao sistema principal e "
            "mesmo assim esperar, a fila é de pessoa ou de aprovação.")
)

cad.section("pareto-dos-gargalos", "Pareto: duas etapas resolvem a maior parte",
    p("Em cada cenário, duas etapas concentram a maior parte da espera. É o "
      "princípio de Pareto aplicado a processo: a mão de massa está em poucos "
      "lugares.") +
    tbl(["Cenário", "1ª etapa do Pareto", "2ª etapa do Pareto", "Soma das duas", "Restante"],
        [[f"<b>{c['n']}</b>. {c['titulo']}", f"{c['gargalo']} ({c['gargalo_share']}%)",
          f"{c['segundo']} ({c['segundo_share']}%)", f"<b>{c['top2']}%</b>",
          f"{round(100 - c['top2'], 1)}%"] for c in CENARIOS],
        num_cols=[3, 4]) +
    callout("note", "O que isso significa para o projeto",
        "Se a equipe do cenário 1 atacar a prova de fogo e o registro no "
        "SINARM, ela mexe em 61,6% da espera do processo. Se ela atacar as "
        "outras seis etapas, mexe em 38,4%. O projeto é o mesmo, o resultado "
        "não é.") +
    callout("err", "O erro de leitura do Pareto",
            "O Pareto do processo ordena etapas por <b>espera</b>, não por "
            "<b>espera por caso</b>. Uma etapa com muita espera e poucos casos "
            "pode aparecer em primeiro no ranking bruto e ser irrelevante no "
            "tempo de ciclo. Por isso, o painel usa a medida <b>Espera por "
            "Etapa (h)</b>, que já é a soma das horas, e a média por caso vem "
            "da coluna de espera média da aba LEIA-ME.")
)

FORMULA_LITTLE = (
    "L = λ × W\n\n"
    "L  = número médio de casos na fila\n"
    "λ  = taxa de chegada de casos (casos por hora)\n"
    "W  = tempo médio de permanência na fila (horas)\n\n"
    "Exemplo do cenário 1 (Prova de fogo):\n"
    "λ = 1.414 casos / 26.280 h do período = 0,0538 casos por hora\n"
    "W = 69,0 horas de espera média na etapa\n"
    "L = 0,0538 × 69,0 = 3,7 casos na fila, ao mesmo tempo, na prova de fogo"
)

cad.section("fila-e-littles-law", "A fila que não aparece: Little's Law aplicada ao processo",
    p("Little's Law diz que o número de itens em uma fila é o tempo de "
      "permanência na fila multiplicado pela taxa de chegada. Aplicado ao "
      "processo, ela mostra quantos casos estão parados ao mesmo tempo.") +
    code(FORMULA_LITTLE, "texto") +
    tbl(["Cenário", "Etapa", "Casos na fila ao mesmo tempo"],
        [[f"<b>{c['n']}</b>", c["gargalo"], f"{c['exec'] / 8 / 26280 * c['gargalo_esp_h']:.1f}"]
         for c in CENARIOS],
        num_cols=[2]) +
    callout("note", "Para que serve esse número",
            "Ele dimensiona a fila, e a fila dimensiona a solução. Se são 3,7 "
            "casos na fila da prova de fogo ao mesmo tempo, com 2 peritos a fila "
            "cai pela metade. Se a solução proposta for digital, a fila vira 0 "
            "e o dimensionamento é outro.") +
    callout("err", "Erro comum de unidade",
            "λ precisa estar na mesma unidade de W. Se W está em horas, λ "
            "precisa estar em casos por hora. Misturar casos por dia com "
            "horas de espera entrega um número que parece bonito e não quer "
            "dizer nada.")
)

cad.section("prioridade", "Prioridade: qual gargalo atacar primeiro",
    p("Cinco gargalos medidos, mas uma equipe só. A prioridade vem de duas "
      "coisas: o tamanho do ganho e o custo de construir a solução.") +
    tbl(["Cenário", "Ganho anual (horas)", "Esforço de implementação", "Prioridade"],
        [["<b>1</b>. Armas", f"{ganho(CENARIOS[0])[0]:,.0f}".replace(",", "."),
          "Alto (app de conferência com leitura automática)", "<b>1</b> - maior fila isolada"],
         ["<b>2</b>. Sinistro", f"{ganho(CENARIOS[1])[0]:,.0f}".replace(",", "."),
          "Baixo (upload de foto e alerta de documento)", "<b>2</b> - ganho rápido"],
         ["<b>3</b>. Credenciamento", f"{ganho(CENARIOS[2])[0]:,.0f}".replace(",", "."),
          "Médio (formulário on-line e parecer assistido)", "<b>3</b>"],
         ["<b>4</b>. Etilometria", f"{ganho(CENARIOS[3])[0]:,.0f}".replace(",", "."),
          "Médio (app do aparelho e auto digital)", "<b>3</b>"],
         ["<b>5</b>. Ouvidoria", f"{ganho(CENARIOS[4])[0]:,.0f}".replace(",", "."),
          "Baixo (abertura no celular e minuta de resposta)", "<b>2</b> - ganho rápido"]],
        num_cols=[1]) +
    grid2([
        ("Atacar primeiro: o ganho rápido",
         p("Os cenários 2 e 5 têm a mesma característica: a fila é de documento "
           "ou de pessoa, e a intervenção é uma tela. App de upload, alerta "
           "automático, minuta de resposta. São semanas, não meses, e o "
           "resultado aparece no painel no mês seguinte.")),
        ("Atacar depois: o ganho estrutural",
         p("Os cenários 1 e 3 exigem integração com sistema oficial e "
           "reconhecimento automático. São projetos maiores, com mais risco, "
           "e que dependem de decisão da diretoria. O número justifica, mas a "
           "execução leva mais tempo.")),
    ]) +
    aplicab(
        "Na reunião que decide o portfólio de projetos do ano.",
        "Porque portfólio se decide por ganho sobre esforço, e o ganho aqui "
        "está medido, não estimado.",
        f"A proposta para a diretoria: <i>começamos pelo sinistro de trânsito e "
        f"pela ouvidoria, porque liberam "
        f"{ganho(CENARIOS[1])[0] + ganho(CENARIOS[4])[0]:,.0f} horas de fila por "
        f"ano com intervenções de tela; armas e credenciamento entram na fase "
        f"2</i>.".replace(",", "."))
)


# =================================================================
# PARTE 7 - GARGALO, AUTOMACAO E DIGITALIZACAO
# =================================================================
cad.grp("Parte 7 - Tarde: gargalo, automação e digitalização",
        "O catálogo de intervenções, o cálculo do ganho e o business case de cada proposta.")

cad.section("automatizar-ou-digitalizar", "Automatizar ou digitalizar: a diferença que decide o projeto",
    p("Duas palavras que aparecem em toda proposta e que significam coisas "
      "diferentes. Confundi-las gera projeto que não resolve o gargalo medido.") +
    antesdepois(
        "<b>Digitalizar</b> é trocar o papel por tela: o formulário vira "
        "aplicativo, o livro de protocolo vira sistema, o e-mail vira "
        "notificação. A pessoa continua fazendo a mesma decisão, mas com o "
        "dado já organizado e sem retrabalho de digitação.",
        "<b>Automatizar</b> é fazer a máquina executar a etapa: o sistema lê o "
        "documento e preenche o auto de infração, o app prioriza a fila por "
        "prazo, o alerta dispara sozinho. A etapa muda de mão.") +
    tbl(["Palavra", "O que muda", "Exemplo neste dia", "Risco"],
        [["Digitalizar", "A forma de entrada e de saída de dados",
          "Segurado fotografa o documento no celular", "Baixo"],
         ["Automatizar", "A execução da etapa pela máquina",
          "App do etilômetro imprime o auto de infração", "Médio"],
         ["Integrar", "A comunicação entre dois sistemas",
          "Consulta do SINARM direto no sistema de perícia", "Médio"],
         ["Regra de negócio", "O critério da decisão",
          "Fila priorizada por prazo legal e por reincidência", "Alto"]],
        num_cols=[]) +
    callout("err", "A confusão que custa o projeto",
            "Digitalizar o formulário de auto de infração não resolve a fila da "
            "emissão do auto: o problema do cenário 4 é a espera na delegacia, "
            "não o meio de escrever. A intervenção certa para a fila é a "
            "regra de prioridade e a emissão assistida. Sempre volte do "
            "gargalo medido para a intervenção, e nunca do costume para a "
            "ferramenta.")
)

cad.section("catalogo-intervencoes", "O catálogo de 10 intervenções",
    p("Estas dez intervenções cobrem os cinco cenários do dia. Cada uma tem o "
      "tipo de fila que ela resolve, o esforço aproximado e o que ela devolve "
      "ao processo.") +
    tbl(["#", "Intervenção", "Fila que resolve", "Esforço", "Cenários"],
        [["1", "Formulário de abertura no celular do cidadão",
          "Fila de papel e de digitação", "Baixo", "2 e 5"],
         ["2", "Upload de foto e documento com conferência automática",
          "Fila de documento", "Baixo", "2 e 5"],
         ["3", "Alerta automático de pendência com prazo",
          "Fila de espera sem cobrança", "Baixo", "2, 3 e 5"],
         ["4", "Fila priorizada por prazo legal e reincidência",
          "Fila de prioridade", "Baixo", "1 e 4"],
         ["5", "Emissão assistida: o sistema preenche e a pessoa confere",
          "Fila de digitação", "Médio", "1 e 4"],
         ["6", "Leitura automática de documento por imagem",
          "Fila de conferência documental", "Médio", "1 e 3"],
         ["7", "Parecer com modelo preenchido pelo sistema",
          "Fila de aprovação", "Médio", "3 e 5"],
         ["8", "Agenda e horário de entrevista com invitation automática",
          "Fila de agendamento", "Baixo", "3"],
         ["9", "Rastreio de código de barras e custódia por QR Code",
          "Fila de rastreabilidade", "Médio", "1"],
         ["10", "Integração entre sistemas oficiais",
          "Fila de sistema", "Alto", "1, 3 e 4"]],
        num_cols=[]) +
    callout("note", "Como escolher uma linha da tabela",
            "Comece pelo tipo de fila que o painel mostrou. Depois procure a "
            "intervenção que resolve aquele tipo. E não escolha por-modismo: "
            "integração entre sistemas oficiais é a intervenção de maior "
            "esforço de todas, e ela só se paga quando a fila for de sistema, "
            "não de pessoa.")
)

cad.section("matriz-gargalo-intervencao", "A matriz gargalo, intervenção e ganho",
    p("A matriz junta as duas coisas que o dia produz: o gargalo medido no "
      "painel e a intervenção que o tackle.") +
    tbl(["Cenário", "Gargalo medido", "Tipo de fila", "Intervenções do catálogo", "Ganho"],
        [["<b>1</b>. Armas", "Prova de fogo (40,3%)", "Fila de pessoa e de conferência",
          "4, 5, 6, 9, 10", f"{ganho(CENARIOS[0])[0]:,.0f} h/ano".replace(",", ".")],
         ["<b>2</b>. Sinistro", "Documentos (35,7%)", "Fila de documento",
          "1, 2, 3, 5", f"{ganho(CENARIOS[1])[0]:,.0f} h/ano".replace(",", ".")],
         ["<b>3</b>. Credenciamento", "Currículo (31,3%)", "Fila de pessoa e de aprovação",
          "3, 6, 7, 8, 10", f"{ganho(CENARIOS[2])[0]:,.0f} h/ano".replace(",", ".")],
         ["<b>4</b>. Etilometria", "Auto de infração (28,9%)", "Fila de aprovação e de digitação",
          "4, 5, 10", f"{ganho(CENARIOS[3])[0]:,.0f} h/ano".replace(",", ".")],
         ["<b>5</b>. Ouvidoria", "Instrução (35,5%)", "Fila de documento e de aprovação",
          "1, 2, 3, 7", f"{ganho(CENARIOS[4])[0]:,.0f} h/ano".replace(",", ".")]],
        num_cols=[4]) +
    callout("tip", "Como escrever a proposta em uma frase",
            "<i>Porque {gargalo} concentra {share}% da espera do processo, "
            "{intervencao} reduz a fila de {tipo de fila} e libera {ganho} "
            "horas por ano.</i>")
)

FORMULA_GANHO = (
    "Ganho (horas por ano) =\n"
    "    Espera da etapa do gargalo (horas em 3 anos)\n"
    "  x taxa de redução da fila\n"
    "  / 3 anos\n\n"
    "Cenário 1, prova de fogo:\n"
    "  Espera da etapa no período .... 97.558 h\n"
    "  Taxa de redução da fila ......... 60%\n"
    "  Ganho em 3 anos ................. 58.535 h\n"
    "  Ganho por ano .................... 19.512 h\n"
    "  Valor por ano (R$ 42,00/h) ...... R$ 819.497\n\n"
    "Atenção: a taxa de redução de 60% é uma hipótese de projeto,\n"
    "não uma medição. Ela precisa ser testada em um piloto de 30 dias,\n"
    "e o painel do cenário mostra o resultado do piloto."
)

cad.section("dimensionar-ganho", "Como dimensionar o ganho, sem inventar número",
    p("O ganho de uma intervenção de fila tem quatro parcelas, e só três delas "
      "dependem do projeto. A quarta depende de decisão da área.") +
    code(FORMULA_GANHO, "texto") +
    callout("err", "O erro de apresentar o ganho como certeza",
            "O número 60% é hipótese. Quem apresenta hipótese como resultado "
            "perde a credibilidade no primeiro piloto. O jeito certo é "
            "apresentar o número em três linhas: o que foi medido, qual é a "
            "hipótese e como ela será testada.") +
    tbl(["Cenário", "Fila medida (h em 3 anos)", "Redução hipotética", "Ganho por ano (h)"],
        [[f"<b>{c['n']}</b>. {c['titulo']}",
          f"{c['espera_total_h'] * c['gargalo_share'] / 100:,.0f}".replace(",", "."),
          f"{int(REDUCAO[c['n']] * 100)}%",
          f"{ganho(c)[0]:,.0f}".replace(",", ".")] for c in CENARIOS],
        num_cols=[1, 3]) +
    callout("note", "O piloto de 30 dias",
            "Todo projeto de fila começa com piloto: uma equipe, uma unidade, "
            "um mês. No fim do piloto, o painel mostra o antes e o depois na "
            "mesma etapa. Se a redução for menor que a hipótese, corrige-se a "
            "hipótese, e não o painel.")
)

cad.section("business-case", "O business case: custo, benefício e prazo",
    p("O business case de um projeto de fila tem quatro linhas. Cabe em uma "
      "página e é o que a diretoria aprova.") +
    tbl(["Linha", "Conteúdo", "Fonte"],
        [["<b>Diagnóstico</b>", "Etapa, share da espera e horas por caso",
          "Painel do cenário"],
         ["<b>Intervenção</b>", "Lista de intervenções do catálogo, com esforço",
          "Matriz gargalo, intervenção e ganho"],
         ["<b>Ganho esperado</b>", "Horas liberadas por ano e capacidade liberada",
          "Cálculo com taxa de redução hipotética"],
         ["<b>Investimento</b>", "Desenvolvimento, integração, treinamento e sustentação",
          "Estimativa da equipe de TI"]],
        num_cols=[]) +
    tbl(["Cenário", "Ganho anual (h)", "Investimento estimado", "Retorno em 2 anos", "Payback"],
        [["<b>1</b>. Armas", f"{ganho(CENARIOS[0])[0]:,.0f}".replace(",", "."),
          "R$ 480.000", f"R$ {ganho(CENARIOS[0])[1] * 2:,.0f}".replace(",", "."), "14 meses"],
         ["<b>2</b>. Sinistro", f"{ganho(CENARIOS[1])[0]:,.0f}".replace(",", "."),
          "R$ 120.000", f"R$ {ganho(CENARIOS[1])[1] * 2:,.0f}".replace(",", "."), "5 meses"],
         ["<b>3</b>. Credenciamento", f"{ganho(CENARIOS[2])[0]:,.0f}".replace(",", "."),
          "R$ 260.000", f"R$ {ganho(CENARIOS[2])[1] * 2:,.0f}".replace(",", "."), "9 meses"],
         ["<b>4</b>. Etilometria", f"{ganho(CENARIOS[3])[0]:,.0f}".replace(",", "."),
          "R$ 310.000", f"R$ {ganho(CENARIOS[3])[1] * 2:,.0f}".replace(",", "."), "7 meses"],
         ["<b>5</b>. Ouvidoria", f"{ganho(CENARIOS[4])[0]:,.0f}".replace(",", "."),
          "R$ 95.000", f"R$ {ganho(CENARIOS[4])[1] * 2:,.0f}".replace(",", "."), "3 meses"]],
        num_cols=[1, 3]) +
    callout("note", "Como ler a coluna do retorno",
            "O retorno é o valor da capacidade liberada multiplicado por dois "
            "anos. Ele não é caixa. O business case honesto mostra os dois "
            "números: o ganho em horas, que é certo, e o valor em dinheiro, "
            "que depende de a área converter a capacidade liberada em "
            "atendimento a mais.") +
    callout("tip", "O argumento que convence a diretoria",
            "O cenário 5 tem o menor investimento do portfólio e o menor "
            "payback. Começar por ele entrega prova de valor em três meses, "
            "e esse resultado é o que destrava o investimento maior do "
            "cenário 1.")
)

cad.section("o-que-nao-automatizar", "O que não automatizar",
    p("Automatizar é fácil demais e perigoso demais. As regras abaixo vêm de "
      "processo de perícia e de atendimento público.") +
    ul([
        "<b>A decisão sobre o direito não é da máquina.</b> Julgamento, "
        "instrução de defesa, parecer conclusivo e laudo com valor de prova "
        "continuam com a pessoa que responde pela assinatura.",
        "<b>Dado pessoal não entra em fluxo automático sem base legal.</b> "
        "CPF, endereço e foto do cidadão têm purpose restrito, com registro de "
        "acesso e prazo de retenção.",
        "<b>Nada de decisão automática de classificação de risco.</b> O modelo "
        "pode sugerir a prioridade; a prioridade é confirmada pela pessoa.",
        "<b>Todo fluxo automático deixa rastro.</b> Quem rodou, com qual versão "
        "do modelo, o que mudou e o que foi aceito.",
        "<b>Retrabalho automático é diferente de retrabalho humano.</b> "
        "Devolução feita por sistema volta ao início com o motivo escrito; "
        "devolução feita por pessoa tem contexto.",
    ]) +
    callout("err", "O erro de automatizar a fila sem arrumar a causa",
            "Automatizar o envio de documento que chega incompleto só faz o "
            "incompleto chegar mais rápido. A ordem certa é: medir a causa da "
            "fila, corrigir a etapa que gera o retrabalho, e só então "
            "automatizar o transporte.")
)

cad.section("roadmap", "Roadmap: da medição ao sistema em 4 fases",
    p("O projeto de melhoria de processo tem quatro fases, e cada fase tem "
      "entregável próprio. Sem a fase 1, as outras três não têm parâmetro.") +
    flow_h([("1", "Medir"), ("2", "Diagnosticar"), ("3", "Pilotar"), ("4", "Escalar")]) +
    tbl(["Fase", "Duração", "O que se faz", "Entregável", "Critério de saída"],
        [["<b>1. Medir</b>", "2 semanas",
          "Montar o painel do cenário", "Painel publicado e validado",
          "Número do gargalo confirmado por duas fontes"],
         ["<b>2. Diagnosticar</b>", "2 semanas",
          "Ouvir a área, ler o fluxo, classificar a fila",
          "Relatório de causa raiz", "Causa escrita e aceita pela área"],
         ["<b>3. Pilotar</b>", "4 a 8 semanas",
          "Intervenção em uma unidade, com medição do antes e do depois",
          "Piloto com resultado", "Redução medida maior que 30% da fila"],
         ["<b>4. Escalar</b>", "3 a 12 meses",
          "Implantação na área, nova versão do painel",
          "Painel pós-intervenção", "Ganho sustentado por 3 meses"]],
        num_cols=[]) +
    callout("note", "O painel muda de papel na fase 4",
            "Depois do piloto, o painel deixa de ser diagnóstico e vira "
            "controle: os cartões mostram o número novo, ao lado do número "
            "antigo. É assim que se prova que a mudança ficou, e não que o "
            "processo voltou ao normal."))


# =================================================================
# PARTE 8 - A PROPOSTA DE SOLUCAO DE CADA CENARIO
# =================================================================
PROPOSTAS = {
    1: {
        "intervencoes": ["Fila priorizada por prazo legal e reincidência (catálogo 4)",
                         "Emissão assistida do laudo a partir do teste de prova de fogo (catálogo 5)",
                         "Leitura automática da ficha de registro do SINARM (catálogo 6)",
                         "QR Code no lacre e na transferência de custódia (catálogo 9)"],
        "tobe": (
            "flowchart TD\n"
            "    A[Arma apreendida e lacrada] --> B[Aplicativo de conferencia no celular]\n"
            "    B --> C[Leitura automatica da ficha do SINARM]\n"
            "    C --> D{Dados conferem com o registro?}\n"
            "    " + "D -- Sim --> E[Prova de fogo com fila priorizada por prazo legal]\n"
            "    " + "D -- Nao --> F[Fila de excecao com perito escalado]\n"
            "    E --> G[Emissao assistida do laudo]\n"
            "    F --> G\n"
            "    G --> H[Envio por QR Code para a autoridade]"
        ),
        "piloto": "Uma sala de armas e um perito balístico, durante 60 dias, com a fila "
                  "priorizada e a emissão assistida. O painel do cenário 1 mede o antes e "
                  "o depois na mesma etapa.",
        "artefato": "Aplicativo de conferência de arma em celular, com leitura da ficha do "
                    "SINARM, fila priorizada por prazo legal e geração do laudo a partir do "
                    "teste de prova de fogo.",
        "risco": "O teste de prova de fogo é prova material e não pode ser automatizado: a "
                 "automação do laudo é assistive, e a assinatura continua humana e "
                 "datada.",
    },
    2: {
        "intervencoes": ["Abertura do sinistro pelo celular do segurado (catálogo 1)",
                         "Upload de foto e documento com conferência automática (catálogo 2)",
                         "Alerta automático de pendência com prazo (catálogo 3)",
                         "Emissão assistida do laudo pericial (catálogo 5)"],
        "tobe": (
            "flowchart TD\n"
            "    A[Segurado fotografa o veiculo e o documento] --> B[Conferencia automatica do documento]\n"
            "    B --> C{O documento esta completo?}\n"
            "    C -- Nao --> D[Alerta automatico com prazo de 48h]\n"
            "    D --> A\n"
            "    C -- Sim --> E[Fila priorizada por prazo de regulacao]\n"
            "    E --> F[Vistoria pericial com checklist no celular]\n"
            "    F --> G[Emissao assistida do laudo]\n"
            "    G --> H[Parecer e liquidacao]"
        ),
        "piloto": "Uma central de vistoria, por 90 dias, com a abertura digital e o alerta de "
                  "pendência. O painel do cenário 2 mede a queda da etapa de documentos.",
        "artefato": "Aplicativo do segurado para abertura de sinistro e envio de foto e "
                    "documento, com painel de retorno do estado do processo.",
        "risco": "O segurado pode não ter smartphone ou sinal. O fluxo em papel precisa "
                 "continuar existindo, com a digitação feita pela central, e não "
                 "descartada.",
    },
    3: {
        "intervencoes": ["Leitura automática do currículo e dos diplomas (catálogo 6)",
                         "Parecer com modelo preenchido pelo sistema (catálogo 7)",
                         "Convite e agendamento automático de entrevista (catálogo 8)",
                         "Integração com o sistema de credenciamento (catálogo 10)"],
        "tobe": (
            "flowchart TD\n"
            "    A[Edital publicado com link de inscricao] --> B[Perito se inscreve on-line]\n"
            "    B --> C[Leitura automatica de diploma e curriculo]\n"
            "    C --> D{Requisitos atendidos?}\n"
            "    D -- Nao --> E[Convite automatico parasupplementary document]\n"
            "    D -- Sim --> F[Parecer com modelo preenchido pelo sistema]\n"
            "    E --> C\n"
            "    F --> G[Convite e agendamento automatico de entrevista]\n"
            "    G --> H[Contratacao e liberacao]"
        ),
        "piloto": "Uma chamada de apoio pericial, do edital ao repasse, com a inscrição on-line "
                  "e o parecer assistido. O painel do cenário 3 mede a fila de currículo e a "
                  "fila de parecer.",
        "artefato": "Portal de credenciamento do perito: inscrição, status do processo, "
                    "agendamento e parecer em modelo.",
        "risco": "A avaliação de currículo do perito não pode ser reduzida a pontuação "
                 "automática. O modelo preenche o modelo do parecer, e a comissão "
                 "decide.",
    },
    4: {
        "intervencoes": ["Fila priorizada por gravidade e reincidência (catálogo 4)",
                         "Emissão assistida do auto de infração a partir do teste (catálogo 5)",
                         "Integração do app do aparelho com o sistema de multas (catálogo 10)"],
        "tobe": (
            "flowchart TD\n"
            "    A[Fiscalizacao em operacao] --> B[App do etilometro registra o teste]\n"
            "    B --> C[Auto de infracao gerado automaticamente]\n"
            "    C --> D{Fila priorizada por gravidade}\n"
            "    D --> E[Delegacia revisa e assina]\n"
            "    E --> F[Notificacao ao condutor pelo app]\n"
            "    F --> G[Instrucao e recurso]\n"
            "    G --> H[Envio ao DETRAN]"
        ),
        "piloto": "Uma operação de fiscalização por 60 dias, com o app do aparelho e a "
                  "emissão assistida. O painel do cenário 4 mede a fila de emissão do auto e "
                  "a de conferência do aparelho.",
        "artefato": "App do etilômetro com teste, conferência automática do aparelho, geração do "
                    "auto de infração e envio à delegacia.",
        "risco": "O valor do teste de alcoolemia é prova comEquipamento homologado. A "
                 "automação não pode alterar a medição, e a conferência do aparelho "
                 "continua registrada por pessoa responsável.",
    },
    5: {
        "intervencoes": ["Abertura do protocolo pelo celular ou chat (catálogo 1)",
                         "Upload de documento com conferência automática (catálogo 2)",
                         "Alerta automático de prazo de resposta (catálogo 3)",
                         "Minuta de resposta padronizada por assunto (catálogo 7)"],
        "tobe": (
            "flowchart TD\n"
            "    A[Cidadao abre protocolo no celular] --> B[Classificacao automatica do assunto]\n"
            "    B --> C[Minuta de resposta montada pelo sistema]\n"
            "    C --> D{A area tecnica precisa de documento?}\n"
            "    D -- Sim --> E[Alerta automatico com prazo ao cidadao]\n"
            "    D -- Nao --> F[Resposta com revisao e assinatura]\n"
            "    E --> F\n"
            "    F --> G[Comunicacao do prazo e encerramento]"
        ),
        "piloto": "Um assunto de maior volume, por 60 dias, com abertura no celular e minuta de "
                  "resposta. O painel do cenário 5 mede a fila de instrução e de resposta.",
        "artefato": "Aplicativo de atendimento ao cidadão: abertura de protocolo, envio de "
                    "documento, acompanhamento e resposta.",
        "risco": "A minuta de resposta é sempre revisada por pessoa antes de sair. Nenhuma "
                 "resposta a cidadão sai sem assinatura e registro de quem revisou.",
    },
}

cad.grp("Parte 8 - Tarde: a solução proposta para cada cenário",
        "Do gargalo medido ao desenho do TO-BE e ao app que vai ser construído no GitHub.")

for c in CENARIOS:
    n = c["n"]
    prop = PROPOSTAS[n]
    h_ano, v_ano = ganho(c)

    cad.section(f"prop{n}-solucao", f"Cenário {n}: a solução proposta para {c['gargalo']}",
        p(f"O diagnóstico do cenário {n} está fechado: "
          f"<b>{c['gargalo']}</b> concentra {c['gargalo_share']}% da espera do "
          f"processo, com {c['gargalo_esp_h']} horas de fila por caso, e "
          f"{c['espera_pct']}% de todo o tempo do processo é espera. A proposta "
          f"abaixo responde a esse número, etapa por etapa.") +
        h3("As quatro intervenções, na ordem de implantação") +
        ol(prop["intervencoes"]) +
        h3("O desenho do TO-BE em Mermaid") +
        p("Cole o código abaixo em <code>mermaid.live</code> para ver o desenho. É "
          "o mesmo formato que você usou na Aula 6, agora com o TO-BE, que é o "
          "processo depois da mudança. Guarde o código no GitHub, no mesmo "
          "repositório do app.") +
        code(prop["tobe"], "mermaid") +
        ficha("g", "O que muda no desenho",
            f"Antes, o caso entrava em uma fila única de "
            f"{c['gargalo_esp_h']:.0f} horas. Depois, o caso entra em uma fila "
            f"com critério de prioridade, a conferência vira automática e a "
            f"digitação desaparece. A etapa de decisão continua com a pessoa, "
            f"com data e hora.") +
        h3("O ganho esperado, com a conta aberta") +
        tbl(["Item", "Valor", "Origem"],
            [["Espera medida na etapa do gargalo (3 anos)",
              f"{c['espera_total_h'] * c['gargalo_share'] / 100:,.0f} h".replace(",", "."),
              "Painel do cenário"],
             ["Redução hipotética da fila", f"{int(REDUCAO[n] * 100)}%", "Hipótese de projeto"],
             ["Ganho por ano", f"{h_ano:,.0f} h".replace(",", "."), "Cálculo da aula"],
             ["Capacidade liberada por ano", f"R$ {v_ano:,.0f}".replace(",", "."),
              "A R$ 42,00 por hora de fila"],
             ["Investimento estimado", f"R$ {['480.000', '120.000', '260.000', '310.000', '95.000'][n - 1]}",
              "Estimativa de desenvolvimento"],
             ["Payback estimado",
              f"{['14', '5', '9', '7', '3'][n - 1]} meses", "Business case"]],
            num_cols=[1]) +
        callout("tip", "Como descrever a proposta em uma frase",
                f"<i>{c['gargalo']} concentra {c['gargalo_share']}% da espera de "
                f"{c['titulo']}; com fila priorizada, conferência automática e "
                f"emissão assistida, liberamos {h_ano:,.0f} horas de fila por "
                f"ano e o tempo de ciclo do caso cai de {c['tat_h']:.0f} para "
                f"cerca de {c['tat_h'] * (1 - REDUCAO[n] * c['gargalo_share'] / 100):.0f} "
                f"horas.</i>".replace(",", ".")) +
        h3("O piloto e o artefato que vai para o GitHub") +
        ul([
            f"<b>Piloto:</b> {prop['piloto']}",
            f"<b>Artefato final:</b> {prop['artefato']}",
            f"<b>Limite da automação:</b> {prop['risco']}",
        ]) +
        aplicab(
            f"Na fase 3 do roadmap, quando o piloto do cenário {n} for "
            f"definir com a área.",
            "Porque o piloto precisa de uma unidade, um prazo e uma métrica de "
            "saída, e o painel já dá a métrica.",
            f"Para a área do cenário {n}: <i>vamos rodar em uma unidade por 60 "
            f"dias e medir a etapa {c['gargalo']} no painel. O critério de saída "
            f"é a redução de 30% das horas de fila nessa etapa</i>.")
    )


# =================================================================
# PARTE 9 - AULAO DE ANTIGRAVITY
# =================================================================
cad.grp("Parte 9 - Tarde: aulão de Antigravity",
        "Cada botão, cada janela e cada comando da ferramenta que vai escrever o app do seu cenário.")

cad.section("antigravity-o-que-e", "O que é o Antigravity",
    p("Antigravity é a plataforma de desenvolvimento com agentes da Google. "
      "A ideia central é simples: em vez de você escrever cada linha de código, "
      "você descreve o que quer, e o agente escreve, roda, mostra a diferença "
      "e espera a sua aprovação.") +
    p("A plataforma tem cinco superfícies. Em sala, a turma vai usar duas: a "
      "<b>IDE do Antigravity</b> e a <b>CLI</b>. As outras três aparecem no "
      "curso quando o tema pedir.") +
    tbl(["Superfície", "Para que serve", "Onde se usa no curso"],
        [["<b>Antigravity App</b>", "Central de comando: gerencia vários agentes em paralelo, "
          "com projetos, conversas e tarefas agendadas", "Visão geral de projeto e acompanhamento"],
         ["<b>Antigravity IDE</b>", "Editor completo, com painel do agente, terminal "
          "embutido, revisão de mudanças e controle de versão", "<b>Usado no dia de hoje</b>"],
         ["<b>Antigravity CLI</b>", "Cliente de terminal, com o comando <code>agy</code>",
          "Automação e ambientes sem interface gráfica"],
         ["<b>Extensões de IDE</b>", "Antigravity dentro do VS Code, JetBrains, Visual Studio, "
          "Zed e Xcode", "Quem já tem ambiente pronto em outra IDE"],
         ["<b>Antigravity SDK</b>", "Biblioteca Python para criar agentes próprios",
          "Fase seguinte, com automação de rotinas"]],
        num_cols=[]) +
    callout("note", "O que o agente faz e o que ele não faz",
            "O agente lê e escreve arquivos, roda comandos no terminal, abre "
            "navegador para pesquisa e mostra as mudanças antes de você aceitar. "
            "Ele não decide o que é correto no seu processo: essa decisão já "
            "está no painel, e é a regra que você vai escrever no pedido.")
)

cad.section("antigravity-instalacao", "Instalação, passo a passo",
    p("Três caminhos possíveis. Escolha um e siga até o fim, sem misturar.") +
    h3("Caminho A: a IDE do Antigravity, para o painel") +
    step([
        ("1. Baixe o instalador",
         "Acesse a página de download do Antigravity e pegue o instalador do seu "
         "sistema: Windows de 64 bits, macOS 12 ou mais recente, ou Linux com "
         "glibc 2.28 ou mais novo."),
        ("2. Execute o instalador e siga o assistente",
         "No Windows, rode o arquivo <code>.exe</code> baixado e aceite os "
         "termos. A instalação cria o atalho do Antigravity."),
        ("3. Abra o aplicativo pela primeira vez",
         "O aplicativo abre pedindo que você entre com a sua conta Google "
         "pessoal ou com as credenciais do Gemini Enterprise. Use a mesma conta "
         "em todos os lugares do curso."),
        ("4. Crie a sua primeira pasta de trabalho",
         "No canto superior esquerdo, use o botão de pasta com sinal de mais "
         "(<b>New Project</b>) na barra lateral. Clique em <b>Add Folder</b> e "
         "escolha a pasta onde vai morar o projeto, por exemplo "
         "<code>Documentos\\politec-mini-app</code>. Clique em <b>Create</b>."),
        ("5. Escolha o modo do agente",
         "Ao abrir uma nova conversa, aparece uma janela de configuração com "
         "duas opções: <b>Local mode</b>, em que o agente trabalha direto nas "
         "suas pastas, e <b>New worktree mode</b>, em que o agente cria uma "
         "cópia isolada do repositório Git. Para o trabalho de hoje, comece "
         "pelo modo local."),
        ("6. Escreva o primeiro pedido",
         "No campo de texto do painel do agente, digite a instrução e aperte "
         "Enter. Exemplo: <i>crie um README.md explicando o que este projeto "
         "resolve, com base no arquivo TO-BE.md desta pasta</i>."),
    ]) +
    h3("Caminho B: a CLI, para o terminal") +
    step([
        ("1. Instale a CLI",
         "No Windows, com o PowerShell: "
         "<code>irm https://antigravity.google/cli/install.ps1 | iex</code>. "
         "No macOS ou Linux: "
         "<code>curl -fsSL https://antigravity.google/cli/install.sh | bash</code>."),
        ("2. Verifique a instalação",
         "Rode <code>agy --version</code>. No Windows, a CLI fica em "
         "<code>C:\\Users\\&lt;seu_usuario&gt;\\AppData\\Local\\agy\\bin</code>; "
         "no macOS e Linux, em <code>~/.local/bin/agy</code>. Se o sistema não "
         "achar o comando, abra um terminal novo."),
        ("3. Complete a configuração da primeira execução",
         "A CLI pergunta três coisas: o esquema de cores (Dark, Solarized "
         "Dark, Solarized Light ou o do terminal), o modo de renderização "
         "(Alt-Screen, que ocupa a tela inteira, ou Inline, que rola no "
         "histórico) e a confiança no repositório. Confirme a confiança só "
         "em pastas que você reconhece."),
        ("4. Inicie uma sessão na pasta do projeto",
         "Dentro da pasta do projeto, rode <code>agy</code>. Para já entrar com "
         "uma tarefa: <code>agy \"crie o esqueleto do aplicativo\"</code>."),
        ("5. Revise o que foi gerado",
         "Quando o agente terminar, ele avisa. Aperte <b>Ctrl + R</b> para "
         "abrir a tela de revisão de artefatos, navegue com as setas, use "
         "<b>Tab</b> para ver o diff dentro do arquivo e <b>Y</b> para aprovar."),
    ]) +
    h3("Caminho C: a extensão no VS Code") +
    p("Abra o VS Code, acione <b>Ctrl + Shift + X</b> para abrir as "
      "extensões, procure por <b>Google Antigravity</b> e instale. O VS Code "
      "precisa ser a versão 1.90 ou mais nova. Depois, clique no ícone do "
      "Antigravity na barra de atividade, entre com a conta e o painel do "
      "agente abre dentro do editor. Para quem já trabalha no VS Code, este "
      "é o caminho mais curto.")
)

cad.section("antigravity-janela", "A janela do Antigravity, botão por botão",
    p("A interface do Antigravity é a do VS Code, com acréscimos. Esta seção "
      "é o mapa de todos os botões, para ninguém ficar procurando.") +
    tbl(["Onde", "Botão ou elemento", "O que faz", "Quando usar"],
        [["Barra de atividade (esquerda)", "ícone do Explorer",
          "Mostra as pastas e os arquivos do projeto", "Para achar o que o agente criou"],
         ["Barra de atividade", "ícone de pesquisa (Ctrl+Shift+F)",
          "Busca texto em todos os arquivos", "Para achar um função específica"],
         ["Barra de atividade", "ícone de Git",
          "Mostra as alterações, o histórico e as branches", "Antes de todo commit"],
         ["Barra de atividade", "ícone de terminal",
          "Abre o terminal embutido", "Para rodar <code>git</code>, <code>npm</code> e testes"],
         ["Barra de atividade", "ícone do Antigravity",
          "Abre o painel do agente", "Para pedir tarefa e revisar o resultado"],
         ["Barra de atividade", "ícone de extensões (Ctrl+Shift+X)",
          "Instala e gerencia extensões", "Para instalar a integração do GitHub"],
         ["Topo da janela", "botão de pasta com sinal de mais (New Project)",
          "Cria um projeto a partir de uma ou mais pastas", "No primeiro uso do dia"],
         ["Topo da janela", "botão do Agent Manager (Ctrl+E)",
          "Abre o gerenciador de agentes, com os projetos e as conversas",
          "Para ver o que os agentes estão fazendo"],
         ["Topo da janela", "seletor de modelo",
          "Escolhe o modelo e o nível de raciocínio", "Antes de cada pedido grande"],
         ["Topo da janela", "botão de terminal (Ctrl+Shift+`)",
          "Abre ou fecha o terminal embutido", "Para instalar a CLI do GitHub"],
         ["Canto inferior direito", "botão de conta",
          "Abre o menu de contas, com a entrada na conta Google e nas contas do editor",
          "Para entrar e para conectar o GitHub"],
         ["Canto inferior esquerdo", "ícone de engrenagem",
          "Abre as configurações", "Para tema, modelo e permissões"],
         ["Painel direito", "painel do Agente",
          "Conversa com o agente, histórico, anexos e revisão de mudanças",
          "É a janela principal do trabalho"]],
        num_cols=[]) +
    callout("note", "Atalhos que economizam tempo",
            "<b>Ctrl + P</b> abre a busca de arquivos. <b>Ctrl + K</b> abre o "
            "seletor de conversas. <b>Ctrl + L</b> joga o cursor no campo de "
            "pergunta do agente. <b>Ctrl + N</b> começa uma conversa nova. "
            "<b>Ctrl + R</b> abre a revisão de artefatos. <b>Tab</b> abre o "
            "diff do arquivo. <b>Ctrl + C</b> interrompe a geração. "
            "<b>Ctrl + D</b> encerra a sessão.")
)

cad.section("antigravity-painel-agente", "O painel do agente, botão por botão",
    p("O painel do agente fica à direita do editor. É ali que mora o pedido, "
      "o histórico e a revisão do que foi feito.") +
    tbl(["Elemento", "O que é", "O que fazer com ele"],
        [["Campo de pergunta (parte de baixo)", "Caixa onde você escreve o pedido",
          "Escreva o pedido completo, em uma frase, com o resultado esperado"],
         ["<b>@</b> no campo", "Menciona um arquivo ou pasta como contexto",
          "Digite <code>@</code> e escolha <code>TO-BE.md</code>, para o agente ler o seu desenho"],
         ["<b>/</b> no campo", "Abre os comandos de barra", "Digite <code>/</code> e veja a lista"],
         ["Ícone de clipe de papel", "Anexa imagem ao pedido",
          "Anexe a captura do painel, para o agente ler o número do gargalo"],
         ["Seletor de modo do agente", "Escolhe entre os modos de trabalho do agente",
          "Use o modo de planejamento quando o pedido for grande"],
         ["Seletor de modelo", "Escolhe o modelo e o nível de raciocínio",
          "Para refatoração, escolha o modelo com raciocínio alto"],
         ["Histórico de conversas", "Lista das conversas do projeto",
          "Volte a uma conversa anterior sem perder o histórico"],
         ["Barra inferior do painel", "Artefatos, processos de terminal e <b>Review Changes</b>",
          "Acompanhe o que foi gerado e o que ainda está rodando"],
         ["Lista de arquivos editados", "Arquivos que o agente mexeu nesta conversa",
          "Abra o diff de cada arquivo antes de aceitar"]],
        num_cols=[]) +
    callout("tip", "Como escrever um pedido que funciona",
            "Três partes: <b>o que</b> (a tarefa), <b>onde</b> (o arquivo ou a "
            "pasta) e <b>como verificar</b> (o teste ou a tela). Exemplo: "
            "<i>crie em <code>src/app.js</code> o formulário de abertura de "
            "protocolo, com validação de CPF e de telefone, e escreva um teste "
            "para o campo obrigatório</i>. Pedido sem verificação devolve "
            "código que parece certo e não funciona.")
)

cad.section("antigravity-agent-manager", "O Agent Manager e os projetos",
    p("O Agent Manager é a central do aplicativo do Antigravity. Ele "
      "organiza os projetos, as conversas e os agentes que trabalham em "
      "paralelo.") +
    ul([
        "<b>Projetos.</b> Um projeto é a configuração de pastas que define o "
        "escopo e as permissões do agente. O projeto pode ter uma pasta ou "
        "várias, e cada projeto tem as próprias configurações isoladas.",
        "<b>Pastas.</b> O projeto pode apontar para uma pasta comum, que não "
        "tem Git, ou para uma cópia de um repositório Git.",
        "<b>Local mode e New worktree mode.</b> No modo local, o agente "
        "trabalha direto na sua pasta. No modo de novo worktree, o Antigravity "
        "cria uma cópia isolada do repositório para a conversa, o que deixa a "
        "sua pasta ativa intacta e evita conflito entre agentes paralelos.",
        "<b>Configurações por projeto.</b> Um projeto novo herda as permissões "
        "globais da máquina, com leitura e escrita nas pastas do projeto, e "
        "pode acrescentar as suas próprias.",
        "<b>Permissões dentro do terminal.</b> No predefinido, os comandos "
        "rodam sem pedir confirmação dentro do sandbox do terminal e pedem "
        "aprovação fora dele.",
    ]) +
    callout("note", "Como abrir o editor a partir do Agent Manager",
            "No menu do workspace, use <b>Focus Editor</b>, ou os botões "
            "<b>Open Editor</b>, ou o atalho <b>Ctrl + E</b>. E na outra "
            "direção: dentro do editor, o botão do Agent Manager no topo, ou "
            "<b>Ctrl + E</b>, abre o gerenciador.")
)

cad.section("antigravity-modelos", "Modelos e nível de raciocínio",
    p("O seletor de modelo fica no topo do painel do agente. O modelo e o "
      "nível de raciocínio podem ser ajustados a cada turno de conversa.") +
    tbl(["Família de modelo", "Quando usar", "Nível de raciocínio"],
        [["Gemini 4 Argon", "Tarefa difícil, código novo, decisão de arquitetura",
          "Alto, quando o erro sai caro"],
         ["Gemini 3.8 Flash", "Tarefa de rotina: ajuste de texto, campo de formulário",
          "Médio ou baixo, para responder rápido"],
         ["Gemini 3.7 e 3.6 Flash", "Correção pontual e script de automação",
          "Baixo, para volume"],
         ["Gemini 3.1 Pro", "Análise de código existente e refatoração",
          "Alto"],
         ["Claude Sonnet e Opus", "Segunda opinião em código legado ou em regra complexa",
          "Thinking, quando o raciocínio profundo compensa"],
         ["GPT-OSS 120B", "Teste local, sem depender de serviço externo",
          "Médio"]],
        num_cols=[]) +
    callout("note", "Como o limite de uso funciona",
            "Há dois limites: um semanal e um de cinco horas. Eles aparecem "
            "na área de modelos. Para o trabalho de sala, use o modelo "
            "padrão com raciocínio médio, e reserve o raciocínio alto para os "
            "dois momentos em que o resultado precisa estar certo: a regra de "
            "negócio e a revisão do código."),
)

cad.section("antigravity-terminal", "O terminal embutido e o painel de versão",
    p("Desde a atualização de agosto de 2026, o Antigravity tem controle de "
      "versão no painel da direita e um terminal embutido. É o que fecha o "
      "ciclo: pedir, revisar, rodar, versionar e publicar.") +
    tbl(["Aba no painel", "O que mostra", "Para que serve"],
        [["<b>Agent Edits</b>", "Arquivos alterados pelo agente nesta conversa",
          "Revisar o que a IA mexeu"],
         ["<b>Uncommitted</b>", "Alterações no working tree, including as de script",
          "Ver o que o repositório tem de diferente da branch"],
         ["<b>Branch</b>", "Tudo que mudou em relação à <code>origin/main</code>",
          "Ver o conjunto da sua entrega"]],
        num_cols=[]) +
    ul([
        "<b>Inspecione o diff:</b> clique no arquivo modificado, alterne entre "
        "<b>Split</b> e <b>Unified Diff</b> no menu de três pontos, e use a "
        "ferramenta de busca do painel para achar um trecho específico.",
        "<b>Prepare o commit:</b> marque os arquivos com a caixa de seleção, ou "
        "use o botão <b>Commit</b> para pegar tudo. A janela de commit mostra "
        "a mensagem sugerida, e você edita antes de confirmar.",
        "<b>Publique:</b> o botão <b>Push</b> envia o commit para o remoto.",
        "<b>Rode comandos:</b> o ícone de terminal na barra de atividade abre o "
        "terminal embutido, com o atalho <b>Ctrl + Shift + `</b>.",
    ]) +
    callout("tip", "A regra de ouro do versionamento",
            "Antes de pedir qualquer coisa ao agente, confirme que o "
            "repositório está limpo: <code>git status</code> no terminal "
            "embutido. Depois do pedido, olhe o diff antes de aceitar. Se o "
            "diff não faz sentido, não aceite e peça de novo com o pedido "
            "mais preciso.")
)

cad.section("antigravity-artefatos", "Artefatos, plano e revisão de mudanças",
    p("O agente não escreve direto no seu arquivo. Ele produz artefatos: um "
      "plano de implementação, os arquivos propostos e um relatório de "
      "verificação. Cada artefato passa por você.") +
    ul([
        "<b>Plano de implementação.</b> Abre antes da primeira linha de "
        "código, e diz o que será criado, o que será alterado e como será "
        "verificado. Leia o plano: é o lugar mais barato de corrigir o agente.",
        "<b>Diff unificado.</b> Mostra, arquivo a arquivo, o que entra e o que "
        "sai. Use <b>Split</b> quando a mudança for grande em arquivo pequeno.",
        "<b>Relatório de verificação.</b> Traz o resultado dos testes, das "
        "checagens e das capturas de tela do navegador.",
        "<b>Capturas de tela da verificação.</b> Quando o agente abre o "
        "navegador para testar a tela, o registro fica anexado ao artefato. É "
        "a prova de que a tela funciona, e não só de que o código compila.",
        "<b>Aceitar ou recusar.</b> Navegue entre os arquivos com as setas, "
        "aproveve com <b>Y</b> e feche a revisão com <b>Esc</b>. O que você não "
        "aprovar não entra no projeto.",
    ]) +
    callout("err", "O erro de aceitar tudo",
            "Aprovar com <b>Y</b> em cada arquivo sem ler o diff é a forma mais "
            "rápida de colocar código errado no repositório oficial. A regra do "
            "curso: nenhum arquivo entra sem diff lido. Se são dez arquivos, "
            "são dez diffs lidos.")
)

cad.section("antigravity-permissoes", "Permissões, sandbox e segurança",
    p("O agente executa comandos na sua máquina. A forma de controlar isso é "
      "por política, e ela é ajustável por projeto.") +
    tbl(["Predefinição", "Comportamento", "Quando usar"],
        [["<b>Inherit Global</b>", "Usa as permissões globais da máquina",
          "Padrão de projeto novo"],
         ["<b>Default</b>", "Comandos rodam sem pedir dentro do sandbox do terminal "
          "e pedem aprovação fora dele", "Equipes que confiam no agente"],
         ["<b>Permissão anterior</b>", "O agente pergunta antes de rodar cada comando",
          "Ambiente com dados sensíveis"]],
        num_cols=[]) +
    p("No nível de código, as políticas se escrevem por ferramenta, com três "
      "verbos: <code>allow</code>, <code>deny</code> e <code>ask_user</code>. "
      "Um exemplo de política que permite ler arquivo e proíbe executar "
      "comando:") +
    code(
        "from google.antigravity import Agent, LocalAgentConfig\n"
        "from google.antigravity.hooks.policy import allow, deny\n\n"
        "config = LocalAgentConfig(\n"
        "    policies=[allow(\"view_file\"), deny(\"run_command\")],\n"
        "    system_instructions=\"Voce e um tecnico da POLITEC.\",\n"
        ")\n\n"
        "async with Agent(config) as agent:\n"
        "    response = await agent.chat(\"Audite o repositorio.\")\n"
        "    print(await response.text())",
        "python") +
    callout("err", "Nunca rode o agente com a pasta da rede inteira",
            "Abra o agente em uma pasta de projeto, não em "
            "<code>C:\\Users</code> nem em uma pasta com dados pessoais. O "
            "agente indexa a pasta e pode ler o que for pedido dentro dela.")
)

cad.section("antigravity-comandos", "Comandos de barra, skills e MCP",
    p("Os comandos de barra são atalhos escritos dentro do campo de pergunta. "
      "Eles mudam o comportamento do agente naquela conversa.") +
    tbl(["Comando", "O que faz", "Quando usar"],
        [["/goal", "Roda a tarefa até o fim, sem parar para perguntar",
          "Tarefa fechada, com critério de pronto claro"],
         ["/plan", "Faz o plano antes de executar", "Pedido grande, com mais de um arquivo"],
         ["/grill-me", "O agente te entrevista sobre requisitos antes de começar",
          "Quando você mesmo não sabe ainda o que quer"],
         ["/diff", "Mostra as mudanças feitas", "Antes de aceitar"],
         ["/context", "Mostra o contexto que o agente está usando", "Suspeita de que ele leu o arquivo errado"],
         ["/codesearch", "Busca no código por símbolo ou texto", "Encontrar a função certa"],
         ["/permissions", "Mostra e ajusta as permissões", "Antes de rodar comando fora do sandbox"],
         ["/browser", "Abre o navegador para pesquisa e depuração", "Testar a tela do app"],
         ["/schedule", "Agenda a tarefa, uma vez ou de forma recorrente", "Relatório semanal automático"],
         ["/agents", "Troca entre subagentes em segundo plano", "Vários trabalhos ao mesmo tempo"],
         ["/usage", "Mostra o consumo de cota do modelo", "Antes do fim de semana"],
         ["/exit", "Fecha a sessão e devolve o terminal", "Fim do trabalho"]],
        num_cols=[]) +
    callout("note", "Skills, regras e MCP",
            "<b>Skills</b> são procedimentos reutilizáveis, escritos em um "
            "arquivo <code>SKILL.md</code>. <b>Regras</b> são instruções "
            "permanentes do projeto, como o padrão de código da unidade. "
            "<b>MCP</b> são servidores que conectam o agente a outros "
            "sistemas, como o GitHub, o Google Cloud ou o Chrome. Para o "
            "trabalho de hoje, a regra do projeto vai ser: <i>todo código novo "
            "precisa de teste e de explicação em português</i>.")
)

cad.section("antigravity-remote-control", "Antigravity no navegador: o Remote Control",
    p("O Remote Control permite abrir a sessão do Antigravity no navegador de "
      "qualquer dispositivo. É o recurso que resolve a dúvida de quem não "
      "consegue instalar nada no computador da sala.") +
    step([
        ("1. Ative o Remote Control no aplicativo",
         "Abra as configurações com <b>Ctrl + ,</b> (ou <b>Cmd + ,</b>) e vá na "
         "seção <b>Application</b>. Ligue a chave <b>Enable Remote Control</b>."),
        ("2. Dê um nome para a máquina",
         "No mesmo campo, digite um nome de fácil identificação, como "
         "<code>workstation-sala3</code>. Esse nome é o que aparece na lista de "
         "máquinas do painel web."),
        ("3. Abra o painel no navegador",
         "No celular ou em outro computador, abra o painel do Remote Control do "
         "Antigravity e entre com a mesma conta Google que você usou no "
         "aplicativo."),
        ("4. Escolha a máquina na lista",
         "No seletor de instância, escolha a máquina que você acabou de "
         "habilitar. A partir daí, você vê as conversas ativas, pode iniciar "
         "novas tarefas, ler planos e inspecionar artefatos."),
        ("5. Alternativa pela CLI",
         "Dentro de uma sessão da CLI, digite <code>/remote-control</code>. O "
         "terminal imprime o nome do host e um endereço para abrir em outro "
         "dispositivo. Para um daemon sempre ligado, use "
         "<code>agy remote-control start --name \"meu-notebook\"</code>, "
         "<code>agy remote-control status</code> e "
         "<code>agy remote-control stop</code>."),
    ]) +
    callout("tip", "Para a sala de aula",
            "Com o Remote Control ligado, o professor conduz o agente no "
            "notebook e a turma acompanha pelo celular, no navegador. Cada "
            "aluno pode depois repetir o fluxo no próprio ritmo, com o mesmo "
            "código do professor no GitHub.")
)


# =================================================================
# PARTE 10 - GITHUB CONECTADO AO ANTIGRAVITY
# =================================================================
cad.grp("Parte 10 - Tarde: o GitHub conectado ao Antigravity",
        "Os comandos para entrar com a conta do GitHub pelo navegador, versionar e publicar o app.")

cad.section("github-por-que", "Por que o GitHub entra antes do código",
    p("O GitHub é onde o app do seu cenário vai nascer. Ele serve para três "
      "coisas concretas na aula: guardar o histórico, revisar o código antes "
      "de publicar, e permitir que o agente do Antigravity trabalhe dentro de "
      "um repositório com regra de versionamento.") +
    grid2([
        ("O que o GitHub guarda",
         ul(["Cada versão do app, com autor, data e mensagem",
             "Os arquivos do diagrama Mermaid do TO-BE, ao lado do código",
             "As issues com a tarefa de cada aluno",
             "As revisões de pull request, que são a revisão do código"])),
        ("O que isso resolve na aula",
         ul(["Perda de trabalho: nada se perde, porque está no histórico",
             "Erro do agente: o diff mostra o que ele mexeu, antes de aceitar",
             "Trabalho em equipe: cada aluno em uma branch, com pull request",
             "Continuidade: quem termina primeiro deixa o caminho pronto"])),
    ]) +
    callout("note", "A regra do curso",
            "Nenhum código de aluno entra em um repositório oficial sem passar "
            "por pull request. E nenhum pull request é aceito sem o diff lido. "
            "O Antigravity faz a parte difícil; a revisão continua sendo sua.")
)

cad.section("github-conectar", "Conectar a conta do GitHub no Antigravity, pelo navegador",
    p("Existem três caminhos. Faça o <b>primeiro</b>, que é o mais curto, e "
      "use o segundo se o primeiro não estiver disponível na sua instalação.") +
    h3("Caminho 1: pelo botão de conta do Antigravity (o mais direto)") +
    step([
        ("1. Abra o menu de contas",
         "No canto inferior direito da janela do Antigravity, clique no botão de "
         "conta, o ícone de pessoa. Abre a lista de contas do editor."),
        ("2. Escolha a opção de entrar com conta",
         "Procure a entrada de adicionar conta, ou a opção de entrar. Se houver "
         "duas, escolha a de conta do editor, e não a conta Google do "
         "Antigravity, que já está conectada."),
        ("3. Escolha o provedor GitHub",
         "Na lista de provedores, escolha <b>GitHub</b>. Se o GitHub não "
         "aparecer na lista, instale a extensão oficial <b>GitHub Pull Requests "
         "and Issues</b>, do publicador GitHub, pela barra de extensões "
         "(<b>Ctrl + Shift + X</b>), e volte ao botão de conta."),
        ("4. Confirme que o navegador vai abrir",
         "O Antigravity abre o navegador automaticamente na página de "
         "autorização do GitHub. Se o navegador não abrir sozinho, copie o "
         "endereço que apareceu na notificação e cole na barra de endereço."),
        ("5. Entre na sua conta do GitHub e autorize",
         "No navegador, entre com o usuário e a senha do seu GitHub, revise as "
         "permissões solicitadas e clique em <b>Authorize</b>. Uma tela verde de "
         "confirmação aparece."),
        ("6. Volte ao Antigravity",
         "A janela do editor reaparece e o nome da sua conta aparece no botão "
         "de conta, no canto inferior direito. Feche a aba do navegador: a "
         "sessão já está valendo no editor."),
        ("7. Confirme a conexão",
         "Abra o terminal embutido (ícone de terminal na barra de atividade, ou "
         "<b>Ctrl + Shift + `</b>) e rode <code>git config --global user.name</code> "
         "e <code>git config --global user.email</code>. Se aparecer o seu nome e "
         "o seu e-mail do GitHub, a identidade está configurada."),
    ]) +
    h3("Caminho 2: pelo terminal, com a ferramenta oficial do GitHub") +
    p("Este é o caminho que funciona em qualquer instalação e em qualquer "
      "terminal, inclusive o terminal embutido do Antigravity. A autenticação "
      "acontece no navegador, com um código de uso único.") +
    step([
        ("1. Instale a ferramenta do GitHub, se ela não estiver na máquina",
         "No Windows, com o PowerShell: <code>winget install --id GitHub.cli</code>. "
         "No macOS: <code>brew install gh</code>. No Linux com Debian ou Ubuntu: "
         "<code>sudo apt install gh</code>. Se a máquina da sala já tiver "
         "instalado, pule este passo."),
        ("2. Verifique a instalação",
         "Rode <code>gh --version</code>. Se o Windows responder que não "
         "reconhece o comando, feche e abra o terminal de novo, porque o "
         "caminho da instalação só entra no PATH depois disso."),
        ("3. Entre com a conta, com autenticação pelo navegador",
         "Rode exatamente este comando no terminal embutido do Antigravity: "
         "<code>gh auth login --hostname github.com --git-protocol https --web</code>"),
        ("4. Copie o código de uso único",
         "O terminal imprime um código no formato <b>XXXX-XXXX</b>. Copie esse "
         "código. O mesmo comando abre o navegador na página de autorização do "
         "GitHub."),
        ("5. Autorize no navegador",
         "Na página que abriu, cole o código no campo indicado, entre na sua "
         "conta, clique em <b>Continue</b> e depois em <b>Authorize github</b>. "
         "Se o navegador não abriu, abra <code>https://github.com/login/device</code> "
         "e cole o código lá."),
        ("6. Volte ao terminal e confira",
         "Rode <code>gh auth status</code>. Deve aparecer a conta, com o "
         "comando de login usado. Se aparecer <i>Logged in to github.com as "
         "SEU_USUARIO</i>, está conectado."),
        ("7. Configure o Git para usar essa conta",
         "Rode <code>gh auth setup-git</code>. Esse comando diz ao Git que, "
         "quando pedir senha, ele deve usar a conta que acabou de autenticar. "
         "Sem esse passo, o <code>git push</code> pede senha e falha."),
        ("8. Teste a conexão sem escrever nada",
         "Rode <code>gh repo list</code>. Se a lista de repositórios aparecer, a "
         "conexão está completa, com leitura e escrita."),
    ]) +
    callout("tip", "Atalho útil",
            "O comando <code>gh auth login</code> tem a forma curta "
            "<code>gh auth login</code>, que faz as mesmas perguntas de forma "
            "interativa. E existe <code>gh auth logout</code>, para sair da "
            "conta, e <code>gh auth switch</code>, para trocar de conta quando "
            "você usa mais de uma. Não compartilhe a saída de "
            "<code>gh auth token</code>: esse comando imprime o seu token de "
            "acesso pessoal, e token vazou para o grupo vira chave pública.") +
    h3("Caminho 3: pelo servidor MCP do GitHub") +
    p("Com o MCP, o próprio agente do Antigravity passa a ler e escrever no "
      "repositório, e não só o terminal. O arquivo de configuração do MCP fica "
      "na pasta do projeto, com o nome <code>.antigravity/mcp.json</code>, e "
      "tem esta forma:") +
    code(
        "{\n"
        "  \"mcpServers\": {\n"
        "    \"github\": {\n"
        "      \"command\": \"npx\",\n"
        "      \"args\": [\"-y\", \"@modelcontextprotocol/server-github\"],\n"
        "      \"env\": {\n"
        "        \"GITHUB_PERSONAL_ACCESS_TOKEN\": \"COLE_AQUI_O_TOKEN\"\n"
        "      }\n"
        "    }\n"
        "  }\n"
        "}",
        "json") +
    ul([
        "Crie o token no GitHub: <b>Settings &rarr; Developer settings "
        "&rarr; Personal access tokens &rarr; Fine-grained tokens</b>.",
        "Dê um nome ao token, escolha apenas o repositório do seu projeto e "
        "marque as permissões de leitura e escrita de conteúdo e de pull requests.",
        "Copie o token gerado e cole no arquivo, no lugar do texto de exemplo.",
        "Reinicie o Antigravity e peça ao agente: <i>liste as issues abertas do "
        "repositório politec-mini-app</i>.",
    ]) +
    callout("err", "Três erros que acontecem na primeira tentativa",
            "<b>1.</b> <i>O navegador não abre.</i> Não trava: o terminal "
            "imprime o endereço e o código. Abra o endereço no navegador e "
            "cole o código. <b>2.</b> <i>O push falha com 403 ou "
            "Authentication failed.</i> Quase sempre é o passo 7 do Caminho 2: "
            "falta o <code>gh auth setup-git</code>. <b>3.</b> <i>O comando gh "
            "não é reconhecido.</i> Feche e abra o terminal, e confira se você "
            "instalou a CLI, e não a IDE.")
)

cad.section("github-publicar", "Publicar o projeto: do arquivo ao GitHub",
    p("Com a conta conectada, publicar o projeto do seu cenário leva cinco "
      "minutos. Estes são os comandos, na ordem.") +
    h3("Preparar o repositório local") +
    code(
        "# 1. transformar a pasta em repositório Git\n"
        "cd Documents\\politec-mini-app\n"
        "git init\n\n"
        "# 2. branch principal com o nome padrao\n"
        "git branch -M main\n\n"
        "# 3. configurar a identidade (so se nunca configurou)\n"
        "git config --global user.name \"Seu Nome\"\n"
        "git config --global user.email \"seu-email@exemplo.gov.br\"\n\n"
        "# 4. ignorar o que nao deve versionar\n"
        "notepad .gitignore\n"
        "#   node_modules/\n"
        "#   .env\n"
        "#   dist/\n\n"
        "# 5. ver o que vai entrar\n"
        "git status\n\n"
        "# 6. gravar a primeira versao\n"
        "git add .\n"
        "git commit -m \"Aula 7: esqueleto do app do cenario 1\"\n\n"
        "# 7. conferir o remoto antes de publicar\n"
        "git remote -v",
        "bash") +
    h3("Criar o repositório no GitHub e publicar") +
    code(
        "# 8. criar o repositorio ja privado e publicar de uma vez\n"
        "gh repo create politec-mini-app --private --source=. --remote=origin --push\n\n"
        "# alternativa: repositorio ja existe no GitHub\n"
        "git remote add origin https://github.com/SEU_USUARIO/politec-mini-app.git\n"
        "git push -u origin main\n\n"
        "# conferir tudo\n"
        "gh repo view\n"
        "gh repo list\n"
        "git status",
        "bash") +
    callout("note", "Por que deixar o repositório privado",
            "O repositório da turma é trabalho em curso, com dados de exemplo e "
            "código em construção. Deixar privado até a entrega final evita "
            "exposição e permite corrigir sem constrangimento. Quando o "
            "trabalho estiver pronto, a publicação pode ser feita para o "
            "repositório oficial, por pull request.") +
    h3("O fluxo diário, depois da primeira publicação") +
    code(
        "git status                 # o que mudou\n"
        "git diff                    # o que mudou, linha a linha\n"
        "git add arquivo.py         # prepara um arquivo\n"
        "git commit -m \"mensagem\"   # grava a versao\n"
        "git push                    # envia para o GitHub\n"
        "git pull                    # traz o que o colega enviou",
        "bash") +
    ul([
        "<b>Antes de aceitar o que o agente fez</b>, rode <code>git status</code> "
        "e <code>git diff</code>. O painel de revisão do Antigravity mostra o "
        "mesmo, com mais conforto.",
        "<b>Uma branch por tarefa</b>: <code>git switch -c feat/formulario-protocolo</code>. "
        "Assim o trabalho de dois alunos não se mistura.",
        "<b>Pull request para integrar</b>: no GitHub, abra a pull request da "
        "sua branch para a <code>main</code>. É ali que a revisão acontece.",
        "<b>Mensagem de commit escrita para o futuro</b>: <i>Adiciona validação "
        "de CPF no formulário de protocolo</i> é útil. <i>ajustes</i> não é.",
    ]) +
    callout("tip", "Quando o push pedir senha",
            "Se o <code>git push</code> pedir usuário e senha, o GitHub não "
            "aceita mais senha de conta: ele exige <b>token</b> ou navegador. "
            "Rode <code>gh auth setup-git</code> de novo, ou troque a URL do "
            "remoto para o protocolo do GitHub CLI. Nunca digite a senha da sua "
            "conta no prompt do Git: ela não funciona e ainda fica registrada "
            "no histórico do Windows.")
)


# =================================================================
# PARTE 11 - LABS
# =================================================================
cad.grp("Parte 11 - Prática guiada",
        "Oito labs, do primeiro arquivo ao primeiro push no GitHub.")

cad.section("labs-intro", "Os oito labs do dia",
    p("Os labs da manhã são de painel, e os da tarde são de projeto e código. "
      "Cada lab tem entregável próprio, e o entregável do lab anterior é "
      "entrada do próximo.") +
    tbl(["Lab", "Turno", "Entregável", "Tempo"],
        [["1. Montar o painel do seu cenário", "Manhã", "Arquivo .pbix com cartões, barras e Pareto", "90 min"],
         ["2. Revisar modelo e medidas", "Manhã", "Números do painel batendo com a aba LEIA-ME", "45 min"],
         ["3. Escrever a hipótese do gargalo", "Manhã", "Uma frase com número e fonte", "20 min"],
         ["4. Escrever a proposta de solução", "Tarde", "TO-BE em Mermaid e cálculo do ganho", "45 min"],
         ["5. Instalar o Antigravity e abrir o projeto", "Tarde", "Projeto criado, agente respondendo", "40 min"],
         ["6. Conectar o GitHub pelo navegador", "Tarde", "Conta conectada e repositório criado", "30 min"],
         ["7. Pedir o app ao agente e revisar o diff", "Tarde", "App gerado, diff lido, primeira versão", "60 min"],
         ["8. Publicar a primeira versão", "Tarde", "Push no GitHub e pull request aberto", "40 min"]],
        num_cols=[3]) +
    callout("note", "Ordem obrigatória",
            "Os labs 5 a 8 só fazem sentido depois do 4. Sem a proposta escrita, "
            "o agente vira um gerador de código sem objetivo, e o código gerado "
            "sem objetivo é desperdício de tempo com aparência de trabalho.")
)

cad.section("lab1-painel", "Lab 1: montar o painel do seu cenário",
    checklist([
        "Abri o workbook do meu cenário e li a aba LEIA-ME até o fim.",
        "Criei o arquivo <code>Painel_CenarioN.pbx</code> antes de importar.",
        "Importei as oito abas de dados, sem a LEIA-ME, do arquivo e não da pasta.",
        "Usei a primeira linha como cabeçalho nas oito consultas.",
        "Corrigi os tipos de dado e marquei a tabela de datas.",
        "Criei as sete relações da fato, todas em 1:* e com filtro de uma direção.",
        "Criei a tabela <code>_Medidas</code> e as 11 medidas.",
        "Montei os cinco cartões, o Pareto, a matriz e a linha do tempo.",
        "Instalei as quatro segmentações e o título do painel.",
        "Salvei o arquivo .pbix.",
    ]) +
    p("Quando terminar, confira o seu painel contra a tabela de etapas do "
      "seu caderno. O número que não bater indica onde está o erro.") +
    callout("err", "Três sinais de que o modelo está errado",
            "O cartão de casos mostra um número oito vezes maior do que o "
            "esperado: você somou execuções em vez de contar casos. O Pareto "
            "tem todas as barras do mesmo tamanho: falta o <code>ALL</code> "
            "na medida <b>Espera por Etapa (h)</b>. A segmentação de ano não "
            "filtra nada: o sentido do filtro de alguma relação está invertido.")
)

cad.section("lab2-revisao", "Lab 2: revisar modelo e medidas",
    ol([
        "Abra o painel do colega e confira a tabela de etapas do caderno com o "
        "seu painel. Divergência no total de espera significa erro de importação.",
        "Abra <b>Modelagem &rarr; Verificar o modelo</b> e confirme que não há "
        "aviso de cardinalidade.",
        "Clique na etapa do gargalo na matriz e leia o nome da unidade que "
        "aparece. Anote: a fila está concentrada em uma área só ou em várias.",
        "Clique no cartão de percentual de espera. O número tem que ser "
        f"próximo de {CENARIOS[0]['espera_pct']}%, e não 100%: se der 100%, a "
        "medida de execução está com problema.",
        "Teste os três filtros: ano, unidade e etapa. Registre o que muda e o "
        "que não muda.",
        "Escreva no rodapé do painel, em um cartão de texto: a data, o autor e "
        "o número da versão. Sem isso, ninguém sabe de quando é o painel.",
    ]) +
    callout("tip", "Revisão em dupla",
            "Troque de painel com o colega e refaça os seis passos. É a revisão "
            "mais barata que existe, e encontra o erro antes da apresentação.")
)

cad.section("lab3-hipotese", "Lab 3: escrever a hipótese do gargalo",
    p("O entregável deste lab são quatro linhas, no modelo abaixo, com número e "
      "fonte.") +
    code(
        "CENÁRIO: N\n"
        "GARGALO: etapa X, com S% da espera do processo\n"
        "TEMPO: T horas de fila por caso na etapa X\n"
        "FONTE: painel do cenário N, arquivo CenarioN_*.xlsx, aba LEIA-ME\n"
        "COMPLEMENTO: a segunda etapa é Y, com S2% da espera",
        "texto") +
    callout("err", "Três hipóteses que a turma escreve e que devem ser recusadas",
            "<i>O processo está lento porque o quadro de pessoal está "
            "incompleto.</i> Sem número e sem fonte, é opinião. <i>A etapa X é "
            "o gargalo porque ela demora mais.</i> Errado: o gargalo é a etapa "
            "que mais <b>espera</b>, não a que mais trabalha. <i>O gargalo é o "
            "setor que mais executa.</i> Também errado: quem mais executa "
            "pode ser quem menos espera.")
)

cad.section("lab4-proposta", "Lab 4: escrever a proposta de solução",
    checklist([
        "Escolhi duas a quatro intervenções do catálogo da Parte 7.",
        "Escrevi o TO-BE em Mermaid, com a etapa nova de decisão marcada.",
        "Calculei o ganho: espera medida x taxa de redução x um terço do período.",
        "Defini o piloto: uma unidade, um prazo e a métrica de saída.",
        "Escrevi o limite da automação, ou seja, o que continua com a pessoa.",
        "Escrevi a frase de proposta de uma linha.",
    ]) +
    p("O código do Mermaid vai para o GitHub, dentro do repositório do "
      "projeto, no arquivo <code>TO-BE.md</code>. É esse arquivo que você vai "
      "mencionar com <b>@</b> no pedido para o agente do Antigravity.") +
    callout("tip", "Nomeie o arquivo de forma óbvia",
            "<code>TO-BE.md</code>, <code>AS-IS.md</code>, <code>PAREto.md</code> e "
            "<code>GARGAHO.md</code>. O agente do Antigravity entende a "
            "intenção do arquivo pelo nome, e a equipe entende pelo repositório. "
            "Nome críptico, como <code>doc1.md</code>, não ajuda ninguém.")
)

cad.section("lab5-antigravity", "Lab 5: instalar o Antigravity e abrir o projeto",
    step([
        ("1. Instale o aplicativo ou a extensão",
         "Siga o Caminho A ou o Caminho C da seção de instalação. Se a máquina "
         "da sala já estiver com o Antigravity, pule para o passo 2."),
        ("2. Entre com a sua conta Google",
         "Use a conta pessoal. A conta define os limites de uso do modelo e o "
         "acesso ao Remote Control."),
        ("3. Crie a pasta do projeto",
         "Crie a pasta <code>politec-mini-app</code> no seu computador, com uma "
         "subpasta por cenário."),
        ("4. Copie para a pasta os arquivos do lab 4",
         "Os arquivos <code>TO-BE.md</code>, <code>AS-IS.md</code> e "
         "<code>GARGAHO.md</code> precisam estar na pasta antes de você abrir o "
         "agente."),
        ("5. Crie o projeto no Antigravity",
         "Use o botão de pasta com sinal de mais na barra lateral, clique em "
         "<b>Add Folder</b>, escolha a pasta do projeto e clique em <b>Create</b>."),
        ("6. Escolha o modo local",
         "Na janela de configuração da primeira conversa, escolha <b>Local "
         "mode</b>. O modo de worktree isolado fica para quando você quiser "
         "trabalhar em paralelo sem arriscar a pasta."),
        ("7. Faça o primeiro pedido",
         "Escreva: <i>leia o arquivo GARGAHO.md e o arquivo TO-BE.md desta pasta "
         "e me diga, em cinco linhas, qual é o gargalo e o que o TO-BE muda</i>. "
         "É um pedido de leitura, sem risco, e ele mostra se o agente está "
         "entendendo o contexto."),
        ("8. Confira a resposta contra o seu caderno",
         "Se o agente acertar o gargalo e as etapas, o contexto está carregado. "
         "Se errar, o problema é o arquivo, ou o <b>@</b> não foi usado."),
    ]) +
    callout("note", "Se o agente responder errado",
            "Três causas: o arquivo não está na pasta, o pedido não apontou o "
            "arquivo, ou o agente precisa de mais contexto. Na dúvida, peça: "
            "<i>liste os arquivos desta pasta com as primeiras linhas de cada "
            "um</i>. É o equivalente computacional de olhar a mesa antes de "
            "sentar.")
)

cad.section("lab6-github", "Lab 6: conectar o GitHub pelo navegador",
    checklist([
        "Abri o botão de conta do Antigravity e escolhi entrar com conta do editor.",
        "Autorizei no navegador e o nome da conta apareceu no canto inferior direito.",
        "Se usei o Caminho 2, instalei a ferramenta do GitHub e rodei "
        "<code>gh auth login --hostname github.com --git-protocol https --web</code>.",
        "Colei o código de uso único no navegador e autorizei.",
        "Rodei <code>gh auth status</code> e a conta apareceu.",
        "Rodei <code>gh auth setup-git</code>.",
        "Rodei <code>gh repo list</code> e a lista de repositórios apareceu.",
        "Criei o repositório privado com "
        "<code>gh repo create politec-mini-app --private --source=. --remote=origin --push</code>.",
        "Abri <code>https://github.com</code> no navegador e vi o repositório novo.",
    ]) +
    callout("err", "Se o passo final falhar",
            "<b>Remote already exists.</b> O repositório já tem um remoto com "
            "esse nome. Use <code>git remote set-url origin "
            "https://github.com/SEU_USUARIO/politec-mini-app.git</code> e rode o "
            "push de novo. <b>Push rejected.</b> Alguém já enviou commits para a "
            "<code>main</code>. Rode <code>git pull --rebase origin main</code> e "
            "depois o push. <b>Permission denied (publickey).</b> O token não foi "
            "instalado: refaça o <code>gh auth setup-git</code>.")
)

cad.section("lab7-app", "Lab 7: pedir o app ao agente e revisar o diff",
    p("Agora a parte que liga o painel ao código. O pedido ao agente tem três "
      "partes: o que, onde e como verificar.") +
    code(
        "Crie em src/app.js o formulario de abertura de protocolo do cenario 1,\n"
        "com os campos: nome do cidadao, CPF, telefone, assunto e descricao.\n"
        "O CPF precisa ser validado por digito verificador antes de salvar.\n"
        "Escreva um teste para o campo de CPF, com um CPF valido e um invalido.\n"
        "Ao final, rode o teste e me mostre o resultado.",
        "texto") +
    ol([
        "Abra o terminal embutido e rode <code>git status</code>. O "
        "repositório precisa estar limpo antes do pedido.",
        "Cole o pedido no painel do agente e aperte Enter.",
        "Leia o plano de implementação antes de qualquer código. Corrija o "
        "plano se ele estiver errado: é muito mais barato corrigir o plano.",
        "Acompanhe o progresso pelo painel. O <b>Tab</b> abre o diff de cada "
        "arquivo enquanto o agente trabalha.",
        "Quando terminar, abra a revisão com <b>Ctrl + R</b>.",
        "Leia o diff de cada arquivo. Um por um. Olhe o nome das variáveis, o "
        "tratamento de erro e o que o código faz quando o campo está vazio.",
        "Rode os testes no terminal embutido. O relatório de verificação do "
        "agente ajuda, mas você confirma rodando.",
        "Se estiver tudo certo, aproveve com <b>Y</b>. Se algo estiver errado, "
        "recuse e peça de novo, mais específico.",
        "Rode <code>git status</code> de novo e confira que os arquivos "
        "criados são só os esperados.",
    ]) +
    callout("err", "O pedido que devolve código inútil",
            "<i>Crie um site para mim</i> devolve um site genérico, bonito e "
            "sem relação com o processo. <i>Crie o formulário de abertura de "
            "protocolo do cenário 1, com validação de CPF por dígito "
            "verificador, teste e leitura do TO-BE</i> devolve algo que a "
            "equipa pode usar amanhã. A diferença está no detalhe do pedido.")
)

cad.section("lab8-publicar", "Lab 8: publicar a primeira versão",
    code(
        "git status\n"
        "git add .\n"
        "git commit -m \"Aula 7: formulario de abertura de protocolo do cenario 1\"\n"
        "git push -u origin main\n"
        "gh repo view\n",
        "bash") +
    ol([
        "Rode <code>git status</code> e confira a lista de arquivos que vai "
        "entrar. Nada de <code>.env</code>, nada de chave, nada de dado pessoal.",
        "Grave a primeira versão com uma mensagem que explica o que o código faz.",
        "Envie para o GitHub com <code>git push</code>.",
        "Abra o repositório no navegador e confirme que os arquivos estão lá.",
        "Abra uma branch para a sua tarefa seguinte e um pull request para "
        "revisão da equipe.",
    ]) +
    callout("note", "O que a equipe entrega no fim do dia",
            "Um repositório privado por equipe, com o TO-BE em Mermaid, o "
            "painel em PDF, o app gerado e revisado, e o histórico de commits "
            "contando a evolução. O professor abre os pull requests no "
            "GitHub e comenta o que precisa mudar.")
)


# =================================================================
# PARTE 12 - FECHAMENTO
# =================================================================
cad.grp("Parte 12 - Fechamento",
        "O método resumido, os erros que mais custam tempo e o teste final.")

cad.section("metodo-resumido", "O método do Dia 7 em oito passos",
    ol([
        "Abrir o workbook do cenário e ler a aba LEIA-ME.",
        "Importar as oito abas de dados no Power BI, do arquivo, não da pasta.",
        "Tratar no Power Query e fechar e aplicar.",
        "Relacionar as sete chaves da fato, todas em 1:*.",
        "Criar as onze medidas, na ordem, e testá-las na tabela.",
        "Montar os cinco cartões, o Pareto, a matriz e a linha do tempo.",
        "Ler o painel em 60 segundos e escrever a hipótese com número.",
        "Escrever a proposta: intervenção, TO-BE em Mermaid, ganho e piloto.",
        "Abrir o projeto no Antigravity, pedir o app, revisar o diff e publicar.",
    ]) +
    callout("g", "O princípio do dia",
            "Nenhuma proposta sem número, e nenhum código sem proposta. Quem "
            "pula a leitura do painel entrega opinião; quem pula a proposta "
            "entrega código sem destino.")
)

cad.section("erros-comuns", "Os erros que mais custaram tempo na turma",
    tbl(["Erro", "Onde aparece", "Como corrigir"],
        [["Importar a pasta em vez do arquivo", "Consultas com nome Tabela1, Tabela2",
          "Refaça a importação e renomeie as consultas"],
         ["Esquecer a primeira linha como cabeçalho", "Campos com nome V1, V2",
          "<b>Início &rarr; Usar Primeira Linha como Cabeçalho</b> nas oito consultas"],
         ["Relação invertida", "Segmentação de ano não filtra",
          "<b>Editar relações</b> e corrigir o sentido do filtro"],
         ["SOM no lugar de DISTINCTCOUNT", "Cartão de casos oito vezes maior",
          "Reescreva a medida <b>Casos</b>"],
         ["Falta do ALL na medida do Pareto", "Todas as barras com o mesmo valor",
          "Inclua <code>ALL ( dim_etapa )</code> dentro do CALCULATE"],
         ["Aprovar o diff sem ler", "Código errado no repositório oficial",
          "Diff lido, arquivo por arquivo"],
         ["Aguardar o navegador do GitHub", "Sessão travada na autorização",
          "Abra <code>https://github.com/login/device</code> e cole o código"],
         ["Colocar o token no commit", "Credencial exposta",
          "<code>.gitignore</code> com <code>.env</code> e arquivo de token"]],
        num_cols=[]) +
    callout("err", "O erro mais caro de todos",
            "Commitar uma chave, um token ou dado pessoal. Isso não se desfaz "
            "com um novo commit: o histórico guarda a versão antiga, e a "
            "credencial precisa ser trocada no servidor. Antes de todo commit, "
            "rode <code>git status</code> e leia a lista de arquivos.")
)

cad.section("quiz", "Quiz final: 15 perguntas",
    q("No processo de apreensão de armas, qual etapa concentra a maior parte da espera?",
      ["Prova de fogo", "Transporte ao IML", "Apreensão e lacre", "Encaminhamento à autoridade"],
      0, "O gargalo medido do cenário 1, com 40,3% da espera total.") +
    q("Em um painel de processo, a etapa que mais trabalha é o gargalo?",
      ["Sim, sempre", "Não, o gargalo é a etapa que mais espera",
       "Sim, se o retrabalho for alto", "Depende do tipo de atividade"],
      1, "Gargalo é fila, e fila é espera, não trabalho.") +
    q("A medida Casos deve ser escrita com:",
      ["SUM(fato[id_ciclo])", "DISTINCTCOUNT(fato[id_ciclo])", "COUNT(fato[id_ciclo])",
       "AVERAGE(fato[id_ciclo])"],
      1, "Cada caso tem várias execuções de etapa, então é preciso contar os valores distintos.") +
    q("No Pareto do processo, as duas primeiras barras somam:",
      ["Cerca de 50% da espera", "Mais de 70% da espera",
       "Entre 55% e 62% da espera, conforme o cenário", "A totalidade da espera"],
      2, "Nos cinco cenários do dia, o top 2 fica entre 49,5% e 61,6%.") +
    q("Little's Law relaciona fila, taxa de chegada e:",
      ["Custo", "Tempo de permanência na fila", "Número de employees",
       "Retrabalho"],
      1, "L = lambda vezes W, com W sendo o tempo médio de permanência na fila.") +
    q("No cenário do sinistro de trânsito, a maior fila é de:",
      ["Vistoria pericial", "Conferência de documentos", "Laudo pericial", "Pagamento"],
      1, "35,7% da espera do processo, com 54,4 horas por caso.") +
    q("Digitalizar e automatizar são a mesma coisa?",
      ["Sim", "Não: digitalizar troca papel por tela, automatizar faz a máquina executar a etapa",
       "Digitalizar é para cliente e automatizar é para servidor",
       "São sinônimos no contexto de processo"],
      1, "A diferença decide o tipo de projeto e o risco.") +
    q("Quando uma proposta apresenta ganho, o número correto é:",
      ["O dinheiro economizado no caixa", "A capacidade liberada, com o horário e a taxa assumidos",
       "O percentual de espera do processo", "O número de casos no gargalo"],
      1, "Capacidade liberada não é economia automática: é o que a área vai fazer com ela.") +
    q("No Antigravity, o que abre a tela de revisão de artefatos?",
      ["Ctrl + R", "Ctrl + P", "Ctrl + Shift + `", "Ctrl + E"],
      0, "Ctrl + R abre a revisão; Ctrl + P é busca de arquivos e Ctrl + E abre o Agent Manager.") +
    q("Para aceitar um arquivo gerado pelo agente, você deve:",
      ["Aceitar tudo de uma vez", "Ler o diff e aprovar arquivo por arquivo",
       "Confiar no relatório de verificação", "Rodar o teste e aceitar sem ler"],
      1, "Aprovar sem ler é o caminho mais curto para o código errado no repositório.") +
    q("O comando que entra no GitHub pelo navegador, pela ferramenta oficial, é:",
      ["gh login", "gh auth login --hostname github.com --git-protocol https --web",
       "git login --browser", "gh connect"],
      1, "Ele imprime um código de uso único, que você cola na página do GitHub.") +
    q("Depois de gh auth login, o comando que faz o Git usar essa conta é:",
      ["gh auth git", "git config --global credential.helper gh", "gh auth setup-git", "gh auth save"],
      2, "Sem esse passo, o push continua pedindo senha e falha.") +
    q("No Power BI, a relação entre a fato e a dimensão deve ser:",
      ["1:1", "1:* (muitos para um)", "*:1", "Muitos para muitos"],
      1, "Com filtro de uma direção, da dimensão para a fato.") +
    q("Um número de espera que não bate com a aba LEIA-ME costuma indicar:",
      ["Erro na medida", "Erro na importação ou no modelo", "Tema do painel errado",
       "Segmentação não aplicada"],
      1, "Antes de mexer na medida, confirme a importação e o modelo.") +
    q("Antes de fazer o commit, o comando que mostra o que vai entrar é:",
      ["git status", "git log", "git show", "git branch"],
      0, "É o git status, e ele é a checagem que evita credencial no histórico.")
)

cad.section("glossario", "Glossário do Dia 7",
    glossary([
        ("Gargalo", "Etapa do processo que concentra a maior parte do tempo de espera."),
        ("Fila", "Volume de casos que espera a mesma etapa ao mesmo tempo."),
        ("Pareto", "Ordenação por espera com o percentual acumulado, que mostra onde está a massa."),
        ("Top 2", "Soma do share das duas primeiras etapas do Pareto."),
        ("Espera x execução", "Separação entre o tempo em que o caso está parado e o tempo em que alguém trabalha."),
        ("Little's Law", "Relação entre taxa de chegada, tempo de fila e número de itens na fila."),
        ("TAT", "Tempo de ciclo total, do início do processo até o fim, medido por caso."),
        ("Retrabalho", "Execução refeita por devolução, correção ou incompletude de documento."),
        ("Fila priorizada", "Fila com critério de ordem, como prazo legal ou reincidência."),
        ("Emissão assistida", "Sistema que preenche o documento e a pessoa confere e assina."),
        ("Digitalizar", "Trocar papel e formulário por tela, sem mudar quem executa a etapa."),
        ("Automatizar", "Fazer a máquina executar a etapa, com a pessoa no controle e na aprovação."),
        ("Intervenção digital", "Mudança no processo apoiada em tecnologia, com efeito medido no painel."),
        ("Antigravity", "Plataforma de desenvolvimento com agentes da Google, com IDE, CLI, extensões e SDK."),
        ("Agent Manager", "Central do aplicativo do Antigravity, com projetos, conversas e agentes em paralelo."),
        ("Worktree", "Cópia isolada do repositório Git, usada pelo agente para não mexer na pasta ativa."),
        ("Artefato", "Entregável produzido pelo agente, como plano, diff e relatório de verificação."),
        ("Remote Control", "Recurso que abre a sessão do Antigravity no navegador de outro dispositivo."),
        ("gh", "Ferramenta oficial do GitHub para terminal, usada na linha de comando."),
        ("MCP", "Protocolo que conecta o agente a sistemas externos, como o GitHub."),
    ])
)

cad.section("referencias", "Referências e para ir além",
    ul([
        "<b>Documentação do Antigravity</b> - <code>antigravity.google/docs</code>, "
        "com as páginas de instalação, modelos, permissões, revisão de mudanças, "
        "projetos e Remote Control.",
        "<b>GitHub CLI</b> - <code>cli.github.com</code>, com o manual de todos os "
        "comandos da ferramenta <code>gh</code>.",
        "<b>GitHub Docs</b> - <code>docs.github.com</code>, em especial a parte de "
        "tokens de acesso pessoal e de pull requests.",
        "<b>Mermaid</b> - <code>mermaid.js.org</code> e o editor <code>mermaid.live</code>, "
        "para renderizar os diagramas do TO-BE.",
        "<b>Power BI</b> - <code>learn.microsoft.com/power-bi</code>, com a referência de "
        "DAX, de relações e de formatação de visual.",
        "<b>Power Query</b> - <code>learn.microsoft.com/power-query</code>, para as "
        "funções de tratamento de dados.",
        "<b>LGPD</b> - Lei nº 13.709 de 2018, para o tratamento de dado pessoal nos "
        "fluxos digitais.",
    ]) +
    callout("note", "O próximo dia",
            "O próximo encontro pega o app que hoje está no GitHub e transforma "
            "ele em um artefato pronto para apresentar: teste automatizado, "
            "imagem de tela, documentação e deploy. O painel que você montou "
            "hoje é o critério de aceitação do app de amanhã.")
)

# =================================================================
# BUILD
# =================================================================
if __name__ == "__main__":
    cad.build()
    destino = pathlib.Path(__file__).resolve().parent / "caderno-dia7.html"
    ptbr.acentuar_arquivo(destino)
    print(f"HTML gerado: {destino}")

