# -*- coding: utf-8 -*-
"""Gerador dos 5 datasets de processo da Aula 7 (Painel + Gargalo + Automacao).

Cada cenario e um **processo real da POLITEC/MT** medido etapa a etapa. O fato
(`fato_execucao`) tem uma linha por **execucao de etapa**, com tempos de
**espera** (fila) e de **execucao** (trabalho), retrabalho e custo. E o que
permite ao aluno **medir o gargalo** em vez de chutar.

Cenarios (todos com >=1000 linhas no fato):

  1. cenario1_apreensao_armas        -> Apreensao, conferencia e pericia de armas
  2. cenario2_sinistro_transito      -> Sinistro de transito (abertura a indenizacao)
  3. cenario3_credenciamento_peritos -> Credenciamento e chamada de apoio pericial
  4. cenario4_etilometria             -> Operacao de etilometria e auto de infracao
  5. cenario5_atendimento_ouvidoria  -> Atendimento ao publico e ouvidoria

Convencoes:
- CSV UTF-8 com BOM, separador ';', datas ISO (AAAA-MM-DD).
- data_key inteiro AAAAMMDD. Chaves substitutas 1..N em ordem alfabetica.
- dim_calendario de 2023-01-01 a 2025-12-31 (1096 dias).

Uso:  python gerar_datasets_aula7.py
"""
import csv
import datetime as dt
import pathlib
import random

RAIZ = pathlib.Path(__file__).resolve().parent
DATASETS = RAIZ / "datasets"
SEED = 20261027
random.seed(SEED)

INICIO = dt.date(2023, 1, 1)
FIM = dt.date(2025, 12, 31)
NOMES_MES = ["", "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
NOMES_SEM = ["", "Segunda-feira", "Terca-feira", "Quarta-feira", "Quinta-feira",
             "Sexta-feira", "Sabado", "Domingo"]

STATUS = ["Concluido", "Em andamento", "Devolvido", "Cancelado"]


# =================================================================
# UTILITARIOS
# =================================================================
def csv_gravar(pasta, arquivo, cabecalho, linhas):
    pasta.mkdir(parents=True, exist_ok=True)
    with open(pasta / arquivo, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";", lineterminator="\r\n")
        w.writerow(cabecalho)
        w.writerows(linhas)


def data_key(d):
    if isinstance(d, str):
        d = dt.date.fromisoformat(d) if d else None
    if not d:
        return ""
    return d.year * 10000 + d.month * 100 + d.day


def dim(valores):
    ordenados = sorted(set(valores))
    return {v: i + 1 for i, v in enumerate(ordenados)}, [[i + 1, v] for i, v in enumerate(ordenados)]


def gravar_calendario(pasta):
    linhas, d = [], INICIO
    while d <= FIM:
        linhas.append([d.year * 10000 + d.month * 100 + d.day, d.isoformat(), d.year, d.month,
                       NOMES_MES[d.month], f"{d.year:04d}-{d.month:02d}", (d.month - 1) // 3 + 1,
                       d.day, d.isoweekday(), NOMES_SEM[d.isoweekday()]])
        d += dt.timedelta(days=1)
    csv_gravar(pasta, "dim_calendario.csv",
               ["data_key", "data", "ano", "mes", "nome_mes", "ano_mes",
                "trimestre", "dia", "dia_semana", "nome_dia_semana"], linhas)


def data_aleatoria():
    return INICIO + dt.timedelta(days=random.randint(0, (FIM - INICIO).days))


def pct(p):
    return random.random() < p


def lognormal(mediana, sigma):
    """Amostra lognormal: reproduz cauda longa de tempos (grosso modo real)."""
    return int(random.lognormvariate(0, sigma) * mediana) + 1


TIPOS_ATIVIDADE = [
    "Tarefa manual", "Tarefa automatizada", "Aprovacao", "Decisao",
    "Espera", "Transferencia",
]


# =================================================================
# GERADOR GENERICO DE CENARIO
# =================================================================
def gerar_cenario(cfg):
    """Monta um cenario de processo a partir de um dicionario de configuracao.

    Chaves esperadas em cfg:
      pasta, etapas, unidades, pesos_unidade, sistemas, projetos,
      ciclos, sistema_por_etapa (opcional), gargalo
    """
    pasta = DATASETS / cfg["pasta"]
    etapas = cfg["etapas"]

    etapa_map, _ = dim([e[1] for e in etapas])
    csv_gravar(pasta, "dim_etapa.csv",
               ["etapa_key", "etapa", "sequencia", "unidade_padrao", "ativada_no_tobe"],
               [[etapa_map[e[1]], e[1], i + 1, e[6], 0] for i, e in enumerate(etapas)])

    un_map, un_rows = dim(cfg["unidades"])
    csv_gravar(pasta, "dim_unidade.csv", ["unidade_key", "unidade", "tipo"],
               [[k, u, cfg["tipo_unidade"].get(u, "Apoio")] for k, u in un_rows])

    sis_map, sis_rows = dim(cfg["sistemas"])
    csv_gravar(pasta, "dim_sistema.csv",
               ["sistema_key", "sistema", "digitizado", "integrado"],
               [[k, s, 1 if i >= 1 else 0, 1 if i in cfg["integrados"] else 0]
                for i, (k, s) in enumerate(sis_rows)])

    ta_map, ta_rows = dim(TIPOS_ATIVIDADE)
    csv_gravar(pasta, "dim_tipo_atividade.csv", ["tipo_atividade_key", "tipo_atividade"], ta_rows)

    st_map, st_rows = dim(STATUS)
    csv_gravar(pasta, "dim_status_execucao.csv", ["status_execucao_key", "status_execucao"], st_rows)

    prj = cfg["projetos"]
    csv_gravar(pasta, "dim_projeto.csv", ["projeto_key", "projeto", "escopo"],
               [[k, p, p.split(" - ")[1][:40]] for k, p in prj])

    gravar_calendario(pasta)

    sistema_por_etapa = cfg.get("sistema_por_etapa", {})
    fato = []
    n = 0
    for ciclo in range(cfg["ciclos"]):
        d0 = data_aleatoria()
        unidade = random.choices(cfg["unidades"], weights=cfg["pesos_unidade"])[0]
        repeticoes = random.randint(1, 8)
        status = "Cancelado" if pct(cfg.get("p_cancel", 0.03)) else (
            "Em andamento" if pct(cfg.get("p_andamento", 0.12)) else (
                "Devolvido" if pct(cfg.get("p_devolvido", 0.07)) else "Concluido"))
        for _rep in range(repeticoes):
            d_ini = d0
            for idx, (rot, key, esp_med, exe_med, sig, autom, unid_pad) in enumerate(etapas):
                n += 1
                if idx == 0:
                    espera = 0
                else:
                    espera = lognormal(esp_med, sig)
                if status == "Cancelado" and idx >= cfg.get("corte_cancelado", 4):
                    espera, exe = "", 0
                else:
                    exe = 0 if autom else lognormal(exe_med, sig)
                    espera_min = round(espera * 60, 1) if espera != "" else ""
                    exe_min = exe
                if status == "Cancelado" and idx >= cfg.get("corte_cancelado", 4):
                    d_fim = ""
                else:
                    dias = max(0, int((espera if espera != "" else 0) / 24) + int(
                        (exe_min if exe_min is not None else 0) / 480) + random.randint(0, 1))
                    d_fim = d_ini + dt.timedelta(days=min(dias, 120))
                    if d_fim > FIM:
                        d_fim = FIM
                sis = sistema_por_etapa.get(key) or random.choice(cfg["sistemas"])
                fato.append([
                    f"EXE-{n:06d}",
                    f"CIC-{ciclo + 1:05d}",
                    etapa_map[key],
                    un_map[unidade],
                    sis_map[sis],
                    ta_map[random.choice(TIPOS_ATIVIDADE[:4])],
                    st_map[status],
                    random.randint(1, len(prj)),
                    data_key(d_ini),
                    data_key(d_fim),
                    espera_min,
                    exe_min,
                    round(float(espera_min or 0) / 60 + float(exe_min or 0) / 60, 2),
                    1 if pct(cfg.get("p_retrabalho", 0.11)) else 0,
                    1 if autom else 0,
                    round(float(exe_min or 0) / 60 * cfg.get("custo_hora", 78.40), 2),
                ])
                if d_fim:
                    d_ini = d_fim + dt.timedelta(days=random.randint(0, 1))
    csv_gravar(pasta, "fato_execucao.csv",
               ["id_execucao", "id_ciclo", "etapa_key", "unidade_key", "sistema_key",
                "tipo_atividade_key", "status_execucao_key", "projeto_key",
                "data_inicio_key", "data_fim_key", "tempo_espera_min", "tempo_execucao_min",
                "tempo_total_h", "flag_retrabalho", "flag_automatizada",
                "custo_execucao_rs"], fato)
    return len(fato)


# =================================================================
# CENARIO 1 - APREENSAO E PERICIA DE ARMAS (ANEXO I / SINARM)
# =================================================================
def cenario1_armas():
    etapas = [
        # (rotulo, chave, espera_med_h, exe_med_min, sigma, autom, unidade_padrao)
        ("Apreensao e lacre na prisao", "Apreensao", 3, 60, 0.5, 0, "PR - Guarda de Prisao"),
        ("Transporte ao IML", "Transporte", 6, 45, 0.6, 0, "PR - Viatura"),
        ("Recebimento e conference da arma", "Recebimento", 9, 90, 0.6, 0, "IML - Armamento"),
        ("Registro no SINARM (numero e characteristics)", "SINARM", 26, 120, 0.8, 0, "IML - Armamento"),
        ("Conferencia documental (procura e registration)", "Documental", 18, 150, 0.7, 0, "IML - Armamento"),
        ("Prova de fogo e teste balistico", "Prova de fogo", 46, 120, 0.9, 0, "IML - Pericia Balistica"),
        ("Laudo pericial e assinatura", "Laudo", 12, 90, 0.6, 0, "IML - Pericia Balistica"),
        ("Encaminhamento a autoridade e baixa", "Encaminhamento", 7, 45, 0.5, 1, "IML - Gabinete"),
    ]
    cfg = {
        "pasta": "cenario1_apreensao_armas",
        "etapas": etapas,
        "ciclos": 320,
        "unidades": ["PR - Guarda de Prisao", "PR - Viatura", "IML - Armamento",
                     "IML - Pericia Balistica", "IML - Gabinete", "PR - Delegacia"],
        "pesos_unidade": [14, 6, 30, 28, 14, 8],
        "tipo_unidade": {"PR - Guarda de Prisao": "Operacao", "PR - Viatura": "Operacao",
                         "PR - Delegacia": "Operacao", "IML - Armamento": "Laboratorio",
                         "IML - Pericia Balistica": "Laboratorio", "IML - Gabinete": "Apoio"},
        "sistemas": ["Papel + livro de protocolo", "Sistema SINARM", "Sistema de armas (IML)",
                     "Planilha Excel (controle local)", "E-mail institucional",
                     "Plataforma de atendimento digital"],
        "integrados": [1],
        "sistema_por_etapa": {"SINARM": "Sistema SINARM", "Prova de fogo": "Sistema de armas (IML)",
                              "Laudo": "Sistema de armas (IML)", "Recebimento": "Sistema de armas (IML)"},
        "projetos": [(1, "PRJ-101 - App de conferencia de arma"),
                     (2, "PRJ-102 - Integracao SINARM com o IML"),
                     (3, "PRJ-103 - Prova de fogo com fila priorizada"),
                     (4, "PRJ-104 - QR Code no lacre e na cadeia de custodia")],
        "p_retrabalho": 0.13,
        "custo_hora": 82.50,
        "gargalo": "Prova de fogo",
    }
    return gerar_cenario(cfg)


# =================================================================
# CENARIO 2 - SINISTRO DE TRANSITO (ABERTURA A INDENIZACAO)
# =================================================================
def cenario2_sinistro():
    etapas = [
        ("Abertura do sinistro (comunicacao do segurado)", "Abertura", 4, 45, 0.5, 1, "PR - Atendimento"),
        ("Triagem do processo e definicao de cobertura", "Triagem", 8, 60, 0.6, 0, "PR - Atendimento"),
        ("Vistoria pericial do veiculo", "Vistoria", 14, 120, 0.7, 0, "PR - Vistoria"),
        ("Conferencia de documentos do veiculo", "Documentos", 38, 60, 0.9, 0, "PR - Atendimento"),
        ("Emissao do laudo pericial", "Laudo", 11, 90, 0.6, 0, "PR - Vistoria"),
        ("Parecer e negociacao com a seguradora", "Parecer", 21, 120, 0.8, 0, "PR - Pericia"),
        ("Liquidacao e pagamento da indenizacao", "Pagamento", 15, 45, 0.6, 1, "PR - Financeiro"),
        ("Encerramento, aviso e arquivo", "Arquivo", 5, 30, 0.5, 1, "PR - Atendimento"),
    ]
    cfg = {
        "pasta": "cenario2_sinistro_transito",
        "etapas": etapas,
        "ciclos": 330,
        "unidades": ["PR - Atendimento", "PR - Vistoria", "PR - Pericia", "PR - Financeiro",
                     "PR - Central de Vistoria"],
        "pesos_unidade": [26, 22, 20, 16, 16],
        "tipo_unidade": {"PR - Atendimento": "Apoio", "PR - Vistoria": "Operacao",
                         "PR - Pericia": "Laboratorio", "PR - Financeiro": "Apoio",
                         "PR - Central de Vistoria": "Operacao"},
        "sistemas": ["Formulario em papel", "Sistema de sinistros (SIGS)",
                     "Planilha Excel (controle local)", "E-mail institucional",
                     "Portal do segurado", "Aplicativo de vistoria em campo"],
        "integrados": [1, 4, 5],
        "sistema_por_etapa": {"Abertura": "Portal do segurado", "Documentos": "Sistema de sinistros (SIGS)",
                              "Vistoria": "Aplicativo de vistoria em campo",
                              "Parecer": "Sistema de sinistros (SIGS)", "Pagamento": "Sistema de sinistros (SIGS)"},
        "projetos": [(1, "PRJ-111 - Upload de fotos pelo segurado"),
                     (2, "PRJ-112 - Checklist digital de vistoria"),
                     (3, "PRJ-113 - Alerta automatico de documentos pendentes"),
                     (4, "PRJ-114 - Integracao com a seguradora")],
        "p_retrabalho": 0.16,
        "custo_hora": 74.20,
        "gargalo": "Documentos",
    }
    return gerar_cenario(cfg)


# =================================================================
# CENARIO 3 - CREDENCIAMENTO E CHAMADA DE APOIO PERICIAL
# =================================================================
def cenario3_credenciamento():
    etapas = [
        ("Publicacao da chamada de apoio pericial", "Edital", 5, 120, 0.5, 1, "PR - Gabinete"),
        ("Inscricao e upload de documentos", "Inscricao", 12, 45, 0.7, 0, "PR - Gabinete"),
        ("Conferencia de requisitos e documentos", "Requisitos", 17, 60, 0.7, 0, "PR - Gabinete"),
        ("Analise de curriculo pela area tecnica", "Curriculo", 44, 90, 0.9, 0, "IML - Coordenacao"),
        ("Entrevista e teste tecnico", "Entrevista", 24, 120, 0.8, 0, "IML - Coordenacao"),
        ("Parecer da comissao de credenciamento", "Parecer", 29, 150, 0.8, 0, "PR - Comissao"),
        ("Contratacao, cadastro e liberacao", "Contratacao", 16, 90, 0.6, 0, "PR - Gabinete"),
        ("Repasse do pagamento do apoio", "Repasse", 13, 45, 0.6, 1, "PR - Financeiro"),
    ]
    cfg = {
        "pasta": "cenario3_credenciamento_peritos",
        "etapas": etapas,
        "ciclos": 300,
        "unidades": ["PR - Gabinete", "IML - Coordenacao", "PR - Comissao", "PR - Financeiro",
                     "IML - Area Tecnica"],
        "pesos_unidade": [18, 30, 22, 14, 16],
        "tipo_unidade": {"PR - Gabinete": "Apoio", "IML - Coordenacao": "Laboratorio",
                         "PR - Comissao": "Apoio", "PR - Financeiro": "Apoio",
                         "IML - Area Tecnica": "Laboratorio"},
        "sistemas": ["Edital em PDF", "Sistema de credenciamento", "Planilha Excel (controle local)",
                     "E-mail institucional", "Plataforma de inscricao on-line"],
        "integrados": [1, 4],
        "sistema_por_etapa": {"Inscricao": "Plataforma de inscricao on-line",
                              "Curriculo": "Sistema de credenciamento",
                              "Parecer": "Sistema de credenciamento",
                              "Edital": "Edital em PDF"},
        "projetos": [(1, "PRJ-121 - Formulario on-line de inscricao"),
                     (2, "PRJ-122 - Parecer com modelo preenchido pelo sistema"),
                     (3, "PRJ-123 - Agenda de entrevistas automatica"),
                     (4, "PRJ-124 - Portal do perito credenciado")],
        "p_retrabalho": 0.18,
        "custo_hora": 96.80,
        "gargalo": "Curriculo + Parecer",
    }
    return gerar_cenario(cfg)


# =================================================================
# CENARIO 4 - OPERACAO DE ETILOMETRIA E AUTO DE INFRACAO
# =================================================================
def cenario4_etilometria():
    etapas = [
        ("Acionamento e distribuicao da operacao", "Acionamento", 4, 30, 0.5, 1, "PR - Operacao"),
        ("Conferencia do aparelho e teste do condutor", "Conferencia", 33, 40, 0.9, 0, "PR - Operacao"),
        ("Teste do etilometro (medicao)", "Teste", 8, 15, 0.6, 0, "PR - Operacao"),
        ("Coleta de prova e contraprova", "Prova", 16, 45, 0.7, 0, "PR - Operacao"),
        ("Emissao do auto de infracao", "Auto", 37, 60, 0.9, 0, "PR - Delegacia"),
        ("Notificacao ao condutor", "Notificacao", 10, 25, 0.6, 1, "PR - Delegacia"),
        ("Instrucao, defesa e decisao", "Instrucao", 19, 120, 0.8, 0, "PR - Julgamento"),
        ("Envio ao DETRAN e arquivo", "Arquivo", 6, 30, 0.5, 1, "PR - Gabinete"),
    ]
    cfg = {
        "pasta": "cenario4_etilometria",
        "etapas": etapas,
        "ciclos": 340,
        "unidades": ["PR - Operacao", "PR - Delegacia", "PR - Julgamento", "PR - Gabinete",
                     "PR - Fiscalizacao de Transito"],
        "pesos_unidade": [40, 24, 18, 10, 8],
        "tipo_unidade": {"PR - Operacao": "Operacao", "PR - Delegacia": "Operacao",
                         "PR - Julgamento": "Apoio", "PR - Gabinete": "Apoio",
                         "PR - Fiscalizacao de Transito": "Operacao"},
        "sistemas": ["Papel + livro de protocolo", "Sistema de multas (DETRAN)",
                     "Planilha Excel (controle local)", "E-mail institucional",
                     "Sistema de etilometro (app)", "Formulario digital de infracao"],
        "integrados": [1, 4, 5],
        "sistema_por_etapa": {"Teste": "Sistema de etilometro (app)",
                              "Conferencia": "Sistema de etilometro (app)",
                              "Auto": "Formulario digital de infracao",
                              "Notificacao": "Sistema de multas (DETRAN)"},
        "projetos": [(1, "PRJ-131 - App do etilometro com impressao automatica"),
                     (2, "PRJ-132 - Auto de infracao digital"),
                     (3, "PRJ-133 - Escala de aparelho por data"),
                     (4, "PRJ-134 - Integracao com o DETRAN")],
        "p_retrabalho": 0.15,
        "custo_hora": 69.90,
        "gargalo": "Conferencia + Auto",
    }
    return gerar_cenario(cfg)


# =================================================================
# CENARIO 5 - ATENDIMENTO AO PUBLICO E OUVIDORIA
# =================================================================
def cenario5_ouvidoria():
    etapas = [
        ("Abertura do protocolo (balcao, telefone ou web)", "Abertura", 5, 20, 0.5, 1, "PR - Atendimento"),
        ("Triagem e classificacao do assunto", "Triagem", 11, 30, 0.6, 0, "PR - Atendimento"),
        ("Encaminhamento a area responsavel", "Encaminhamento", 14, 25, 0.7, 0, "PR - Atendimento"),
        ("Instrucao e pedido de documentos", "Instrucao", 41, 45, 0.9, 0, "PR - Area Tecnica"),
        ("Parecer e decisao", "Parecer", 18, 75, 0.7, 0, "PR - Area Tecnica"),
        ("Resposta formal ao cidadao", "Resposta", 22, 40, 0.8, 0, "PR - Atendimento"),
        ("Comunicacao do prazo e acompanhamento", "Acompanhamento", 9, 20, 0.6, 1, "PR - Atendimento"),
        ("Encerramento, pesquisa e arquivo", "Encerramento", 4, 15, 0.5, 1, "PR - Atendimento"),
    ]
    cfg = {
        "pasta": "cenario5_atendimento_ouvidoria",
        "etapas": etapas,
        "ciclos": 360,
        "unidades": ["PR - Atendimento", "PR - Area Tecnica", "PR - Gabinete",
                     "PR - Ouvidoria", "PR - Arquivo"],
        "pesos_unidade": [34, 30, 16, 12, 8],
        "tipo_unidade": {"PR - Atendimento": "Apoio", "PR - Area Tecnica": "Laboratorio",
                         "PR - Gabinete": "Apoio", "PR - Ouvidoria": "Apoio",
                         "PR - Arquivo": "Apoio"},
        "sistemas": ["Papel + livro de protocolo", "Sistema de protocolos (SEI-like)",
                     "Planilha Excel (controle local)", "E-mail institucional",
                     "Portal de atendimento digital", "Chat e abertura on-line"],
        "integrados": [1, 4, 5],
        "sistema_por_etapa": {"Abertura": "Chat e abertura on-line",
                              "Triagem": "Sistema de protocolos (SEI-like)",
                              "Resposta": "Sistema de protocolos (SEI-like)",
                              "Instrucao": "E-mail institucional"},
        "projetos": [(1, "PRJ-141 - Abertura de protocolo pelo celular"),
                     (2, "PRJ-142 - Alerta automatico de prazo"),
                     (3, "PRJ-143 - Minuta de resposta padronizada"),
                     (4, "PRJ-144 - Painel de tempo de resposta ao cidadao")],
        "p_retrabalho": 0.19,
        "custo_hora": 58.40,
        "gargalo": "Instrucao + Resposta",
    }
    return gerar_cenario(cfg)


# =================================================================
# MAIN
# =================================================================
def main():
    geradores = [
        ("Cenario 1 - Apreensao de armas", cenario1_armas),
        ("Cenario 2 - Sinistro de transito", cenario2_sinistro),
        ("Cenario 3 - Credenciamento de peritos", cenario3_credenciamento),
        ("Cenario 4 - Etilometria", cenario4_etilometria),
        ("Cenario 5 - Atendimento e ouvidoria", cenario5_ouvidoria),
    ]
    total = 0
    for nome, ger in geradores:
        n = ger()
        total += n
        print(f"  {nome:42s} {n:>7,} execucoes".replace(",", "."))
    print(f"Total: {total:,} execucoes de etapa.".replace(",", "."))


if __name__ == "__main__":
    main()
