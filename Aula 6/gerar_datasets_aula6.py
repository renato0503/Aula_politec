# -*- coding: utf-8 -*-
"""Gerador dos 5 datasets de processo da Aula 6 (Painel de Processo + AS-IS/TO-BE).

Cada cenario e um **processo real da POLITEC/MT** medido etapa a etapa. O fato
(`fato_execucao`) tem uma linha por **execucao de etapa**, com tempos de
**espera** (fila) e de **execucao** (trabalho), retrabalho e custo. E o que
permite ao aluno **medir o gargalo** em vez de chutar.

Cenarios (todos com >=1000 linhas no fato):

  1. cenario1_processo_pericial      -> Requisicao pericial
  2. cenario2_processo_orcamento     -> Empenho e contrato
  3. cenario3_processo_custodia      -> Cadeia de custodia
  4. cenario4_local_crime            -> Atendimento de local de crime
  5. cenario5_analise_laboratorial   -> Analise laboratorial (DNA/toxicologia)

Convencoes:
- CSV UTF-8 com BOM, separador ';', datas ISO (AAAA-MM-DD).
- data_key inteiro AAAAMMDD. Chaves substitutas 1..N em ordem alfabetica.
- dim_calendario de 2023-01-01 a 2025-12-31 (1096 dias).

Uso:  python gerar_datasets_aula6.py
"""
import csv
import datetime as dt
import pathlib
import random

RAIZ = pathlib.Path(__file__).resolve().parent
DATASETS = RAIZ / "datasets"
SEED = 20260610
random.seed(SEED)

INICIO = dt.date(2023, 1, 1)
FIM = dt.date(2025, 12, 31)
NOMES_MES = ["", "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
NOMES_SEM = ["", "Segunda-feira", "Terca-feira", "Quarta-feira", "Quinta-feira",
             "Sexta-feira", "Sabado", "Domingo"]


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


# =================================================================
# CATALOGOS COMPARTILHADOS
# =================================================================
SISTEMAS = [
    "Papel + livro de protocolo",
    "Sistema SIGT (requisicoes)",
    "Excel (controle local)",
    "Sistema patrimonial",
    "E-mail institucional",
    "Plataforma de atendimento digital",
]

TIPOS_ATIVIDADE = [
    "Tarefa manual", "Tarefa automatizada", "Aprovacao", "Decisao",
    "Espera", "Transferencia",
]


# =================================================================
# CENARIO 1 - PROCESSO DE REQUISICAO PERICIAL (AS-IS)
# =================================================================
def cenario1_pericial(pasta):
    etapas = [
        # (rotulo, chave, espera_mediana_h, exec_mediana_min, exec_sigma, autom)
        ("Entrada da requisicao (delegacia)", "Entrada", 4, 90, 0.6, 1),
        ("Triagem e classificacao", "Triagem", 8, 60, 0.5, 0),
        ("Distribuicao ao setor", "Distribuicao", 10, 40, 0.6, 0),
        ("Fila de espera do perito", "Fila perito", 34, 10, 0.8, 0),
        ("Analise do exame", "Analise", 6, 240, 0.7, 0),
        ("Revisao tecnica", "Revisao", 9, 90, 0.6, 0),
        ("Assinatura e release do laudo", "Assinatura", 7, 30, 0.5, 1),
        ("Envio e arquivamento", "Arquivamento", 4, 25, 0.4, 1),
    ]
    etapa_map, _ = dim([e[1] for e in etapas])
    ordem = {e[1]: i for i, e in enumerate(etapas)}
    unidade_padrao = {
        "Entrada": "ATO - Gabinete", "Triagem": "ATO - Gabinete",
        "Distribuicao": "ATO - Gabinete", "Fila perito": "LAB - Biologia",
        "Analise": "LAB - Biologia", "Revisao": "LAB - Biologia",
        "Assinatura": "ATO - Gabinete", "Arquivamento": "ATO - Gabinete",
    }
    csv_gravar(pasta, "dim_etapa.csv",
               ["etapa_key", "etapa", "sequencia", "unidade_padrao", "ativada_no_tobe"],
               [[etapa_map[e[1]], e[1], i + 1, unidade_padrao[e[1]], 0] for i, e in enumerate(etapas)])

    unidades = ["ATO - Gabinete", "LAB - Biologia", "LAB - Fisica", "LAB - Toxicologia",
                "LAB - Informatica", "IML - Medicina Legal", "ATV - Campo"]
    un_map, un_rows = dim(unidades)
    csv_gravar(pasta, "dim_unidade.csv", ["unidade_key", "unidade", "tipo"],
               [[k, u, "Laboratorio" if u.startswith("LAB") or u.startswith("IML") else "Apoio"]
                for k, u in un_rows])

    sis_map, sis_rows = dim(SISTEMAS)
    csv_gravar(pasta, "dim_sistema.csv",
               ["sistema_key", "sistema", "digitizado", "integrado"],
               [[k, s, 1 if i >= 1 else 0, 1 if i in (1, 3, 5) else 0]
                for i, (k, s) in enumerate(sis_rows)])

    ta_map, ta_rows = dim(TIPOS_ATIVIDADE)
    csv_gravar(pasta, "dim_tipo_atividade.csv",
               ["tipo_atividade_key", "tipo_atividade"], ta_rows)

    st = ["Concluido", "Em andamento", "Devolvido", "Cancelado"]
    st_map, st_rows = dim(st)
    csv_gravar(pasta, "dim_status_execucao.csv", ["status_execucao_key", "status_execucao"], st_rows)

    prj = [(1, "PRJ-001 - Digitalizacao do fluxo pericial"),
           (2, "PRJ-002 - Integracao SIGT x laboratorio"),
           (3, "PRJ-003 - Portal de solicitacao"),
           (4, "PRJ-004 - App de checklist do perito")]
    csv_gravar(pasta, "dim_projeto.csv", ["projeto_key", "projeto", "escopo"],
               [[k, p, (p.split(" - ")[1][:40])] for k, p in prj])

    gravar_calendario(pasta)

    fato = []
    n = 0
    for ciclo in range(300):
        d0 = data_aleatoria()
        unidade = random.choices(unidades, weights=[8, 24, 18, 20, 12, 13, 5])[0]
        retrabalho_etapa = random.randint(1, 8)
        for rep in range(retrabalho_etapa):
            d_ini = d0
            status = "Cancelado" if pct(0.03) else (
                "Em andamento" if pct(0.12) else ("Devolvido" if pct(0.06) else "Concluido"))
            for idx, (rot, key, esp_med, exe_med, sig, autom) in enumerate(etapas):
                n += 1
                if idx == 0:
                    espera = 0
                else:
                    # o gargalo: a fila do perito cresce com a demanda do trimestre
                    fator = 1.25 if esp_med >= 60 else 1.0
                    sigma = 0.5 if esp_med >= 60 else 0.65
                    espera = lognormal(esp_med * fator, sigma)
                if status == "Cancelado" and idx > 3:
                    espera, exe_med = "", 0
                else:
                    exe = 0 if autom and idx in (0, 6, 7) else lognormal(exe_med, sig)
                    espera_min = round(espera * 60, 1) if espera != "" else ""
                    exe_min = exe
                if status == "Cancelado" and idx > 3:
                    d_fim = ""
                else:
                    dias = max(0, int((espera if espera != "" else 0) / 24) + int(
                        (exe_min if exe_min != "" else 0) / 480) + random.randint(0, 1))
                    d_fim = d_ini + dt.timedelta(days=min(dias, 120))
                    if d_fim > FIM:
                        d_fim = FIM
                fato.append([
                    f"EXE-{n:06d}",
                    f"CIC-{ciclo + 1:05d}",
                    etapa_map[key],
                    un_map[unidade],
                    sis_map[random.choice(SISTEMAS[:4])],
                    ta_map[random.choice(TIPOS_ATIVIDADE[:4])],
                    st_map[status],
                    random.randint(1, 4),
                    data_key(d_ini),
                    data_key(d_fim),
                    espera_min,
                    exe_min,
                    round(float(espera_min or 0) / 60 + float(exe_min or 0) / 60, 2),
                    1 if pct(0.11) else 0,
                    1 if autom else 0,
                    round(float(exe_min or 0) / 60 * 78.40, 2),
                ])
                if d_fim:
                    d_ini = d_fim + dt.timedelta(days=random.randint(0, 1))
    csv_gravar(pasta, "fato_execucao.csv",
               ["id_execucao", "id_ciclo", "etapa_key", "unidade_key", "sistema_key",
                "tipo_atividade_key", "status_execucao_key", "projeto_key",
                "data_inicio_key", "data_fim_key", "tempo_espera_min", "tempo_execucao_min",
                "tempo_total_h", "flag_retrabalho", "flag_automatizada",
                "custo_execucao_rs"], fato)


# =================================================================
# CENARIO 2 - PROCESSO DE EMPENHO E CONTRATO
# =================================================================
def cenario2_orcamento(pasta):
    etapas = [
        ("Pedido do setor (papeis)", "Pedido", 14, 180, 0.8, 0),
        ("Cotacao no sistema", "Cotacao", 8, 240, 0.7, 1),
        ("Mapa comparativo", "Mapa", 18, 300, 0.6, 0),
        ("Parecer juridico", "Parecer", 32, 240, 0.8, 0),
        ("Autorizacao do ordenador", "Autorizacao", 24, 60, 0.5, 0),
        ("Empenho e contratacao", "Empenho", 10, 90, 0.5, 1),
        ("Publicacao do ato", "Publicacao", 16, 45, 0.5, 1),
    ]
    etapa_map, _ = dim([e[1] for e in etapas])
    unidade_padrao = {
        "Pedido": "ADM - Divisao de Compras", "Cotacao": "ADM - Divisao de Compras",
        "Mapa": "ADM - Divisao de Compras", "Parecer": "JUR - Assessoria Juridica",
        "Autorizacao": "ADM - Diretoria", "Empenho": "ADM - Divisao de Compras",
        "Publicacao": "ADM - Divisao de Compras",
    }
    csv_gravar(pasta, "dim_etapa.csv",
               ["etapa_key", "etapa", "sequencia", "unidade_padrao", "ativada_no_tobe"],
               [[etapa_map[e[1]], e[1], i + 1, unidade_padrao[e[1]], 0] for i, e in enumerate(etapas)])

    unidades = ["ADM - Diretoria", "ADM - Divisao de Compras", "PLEN - Planejamento",
                "CONT - Controle Interno", "JUR - Assessoria Juridica"]
    un_map, un_rows = dim(unidades)
    csv_gravar(pasta, "dim_unidade.csv", ["unidade_key", "unidade", "tipo"],
               [[k, u, "Apoio" if u.startswith(("ADM", "PLEN")) else "Controle"] for k, u in un_rows])

    sis_map, sis_rows = dim(SISTEMAS)
    csv_gravar(pasta, "dim_sistema.csv",
               ["sistema_key", "sistema", "digitizado", "integrado"],
               [[k, s, 1 if i >= 1 else 0, 1 if i in (1, 3, 5) else 0]
                for i, (k, s) in enumerate(sis_rows)])

    ta_map, ta_rows = dim(TIPOS_ATIVIDADE)
    csv_gravar(pasta, "dim_tipo_atividade.csv", ["tipo_atividade_key", "tipo_atividade"], ta_rows)

    st = ["Concluido", "Em andamento", "Devolvido para ajuste", "Cancelado"]
    st_map, st_rows = dim(st)
    csv_gravar(pasta, "dim_status_execucao.csv", ["status_execucao_key", "status_execucao"], st_rows)

    prj = [(1, "PRJ-010 - Compras eletronicas end-to-end"),
           (2, "PRJ-011 - Catalogo de contratos"),
           (3, "PRJ-012 - Alertas de dotacao"),
           (4, "PRJ-013 - Pauta automatica de autorizacao")]
    csv_gravar(pasta, "dim_projeto.csv", ["projeto_key", "projeto", "escopo"],
               [[k, p, p.split(" - ")[1][:40]] for k, p in prj])

    gravar_calendario(pasta)

    fato, n = [], 0
    for ciclo in range(250):
        d0 = data_aleatoria()
        unidade = random.choices(unidades, weights=[22, 34, 16, 16, 12])[0]
        qtd = random.randint(3, 8)
        for rep in range(qtd):
            n += 1
            d_ini = d0
            status = "Cancelado" if pct(0.06) else (
                "Devolvido para ajuste" if pct(0.14) else (
                    "Em andamento" if pct(0.18) else "Concluido"))
            for idx, (rot, key, esp_med, exe_med, sig, autom) in enumerate(etapas):
                espera = 0 if idx == 0 else lognormal(esp_med, 0.55)
                if status == "Cancelado" and idx > 2:
                    espera = ""
                    exe_min = 0
                else:
                    exe_min = 0 if autom else lognormal(exe_med, sig)
                espera_min = round(espera * 60, 1) if espera != "" else ""
                if status == "Cancelado" and idx > 2:
                    d_fim = ""
                else:
                    dias = int((espera if espera != "" else 0) / 24) + int(
                        (exe_min or 0) / 480) + random.randint(0, 2)
                    d_fim = d_ini + dt.timedelta(days=min(dias, 180))
                    if d_fim > FIM:
                        d_fim = FIM
                fato.append([
                    f"EXO-{n:06d}", f"CIC-{ciclo + 1:05d}", etapa_map[key], un_map[unidade],
                    sis_map[random.choice([SISTEMAS[1], SISTEMAS[2], SISTEMAS[4]])],
                    ta_map[random.choice(TIPOS_ATIVIDADE[:4])], st_map[status],
                    random.randint(1, 4), data_key(d_ini), data_key(d_fim),
                    espera_min, exe_min,
                    round(float(espera_min or 0) / 60 + float(exe_min or 0) / 60, 2),
                    1 if pct(0.16) else 0, 1 if autom else 0,
                    round(float(exe_min or 0) / 60 * 62.80, 2),
                ])
                if d_fim:
                    d_ini = d_fim + dt.timedelta(days=random.randint(0, 3))
    csv_gravar(pasta, "fato_execucao.csv",
               ["id_execucao", "id_ciclo", "etapa_key", "unidade_key", "sistema_key",
                "tipo_atividade_key", "status_execucao_key", "projeto_key",
                "data_inicio_key", "data_fim_key", "tempo_espera_min", "tempo_execucao_min",
                "tempo_total_h", "flag_retrabalho", "flag_automatizada",
                "custo_execucao_rs"], fato)


# =================================================================
# CENARIO 3 - PROCESSO DE CADEIA DE CUSTODIA
# =================================================================
def cenario3_custodia(pasta):
    etapas = [
        ("Coleta no local", "Coleta", 6, 90, 0.7, 0),
        ("Acondicionamento e lacre", "Lacre", 9, 45, 0.5, 0),
        ("Registro da ocorrencia", "Registro", 10, 60, 0.6, 1),
        ("Transporte ao destino", "Transporte", 14, 120, 0.8, 0),
        ("Recebimento e conferencia", "Recebimento", 12, 50, 0.5, 0),
        ("Guarda / refrigeracao", "Guarda", 38, 10, 1.0, 0),
        ("Pericia propriamente dita", "Pericia", 18, 240, 0.9, 0),
        ("Baixa e destino final", "Baixa", 22, 35, 0.7, 1),
    ]
    etapa_map, _ = dim([e[1] for e in etapas])
    unidade_padrao = {
        "Coleta": "CAMPO - Operacao", "Lacre": "CAMPO - Operacao",
        "Registro": "CAMPO - Operacao", "Transporte": "CAMPO - Transporte",
        "Recebimento": "LAB - Recebimento", "Guarda": "LAB - Arquivo",
        "Pericia": "LAB - Pericia", "Baixa": "CTRL - Custodia",
    }
    csv_gravar(pasta, "dim_etapa.csv",
               ["etapa_key", "etapa", "sequencia", "unidade_padrao", "ativada_no_tobe"],
               [[etapa_map[e[1]], e[1], i + 1, unidade_padrao[e[1]], 0] for i, e in enumerate(etapas)])

    unidades = ["CAMPO - Operacao", "CAMPO - Transporte", "LAB - Recebimento",
                "LAB - Pericia", "LAB - Arquivo", "CTRL - Custodia"]
    un_map, un_rows = dim(unidades)
    csv_gravar(pasta, "dim_unidade.csv", ["unidade_key", "unidade", "tipo"],
               [[k, u, "Laboratorio" if u.startswith("LAB") else "Campo"] for k, u in un_rows])

    sis_map, sis_rows = dim(SISTEMAS)
    csv_gravar(pasta, "dim_sistema.csv",
               ["sistema_key", "sistema", "digitizado", "integrado"],
               [[k, s, 1 if i >= 1 else 0, 1 if i in (1, 3, 5) else 0]
                for i, (k, s) in enumerate(sis_rows)])

    ta_map, ta_rows = dim(TIPOS_ATIVIDADE)
    csv_gravar(pasta, "dim_tipo_atividade.csv", ["tipo_atividade_key", "tipo_atividade"], ta_rows)

    st = ["Concluido", "Em andamento", "Divergencia de lacre", "Cancelado"]
    st_map, st_rows = dim(st)
    csv_gravar(pasta, "dim_status_execucao.csv", ["status_execucao_key", "status_execucao"], st_rows)

    prj = [(1, "PRJ-020 - App de custodia com QR Code"),
           (2, "PRJ-021 - Rastreio GPS de transporte"),
           (3, "PRJ-022 - Integracao com a instituicao receptora"),
           (4, "PRJ-023 - Alerta de guarda vencida")]
    csv_gravar(pasta, "dim_projeto.csv", ["projeto_key", "projeto", "escopo"],
               [[k, p, p.split(" - ")[1][:40]] for k, p in prj])

    gravar_calendario(pasta)

    fato, n = [], 0
    for ciclo in range(220):
        d0 = data_aleatoria()
        unidade = random.choices(unidades, weights=[20, 16, 20, 26, 10, 8])[0]
        qtd = random.randint(4, 8)
        for rep in range(qtd):
            n += 1
            d_ini = d0
            status = "Cancelado" if pct(0.02) else (
                "Divergencia de lacre" if pct(0.05) else (
                    "Em andamento" if pct(0.16) else "Concluido"))
            for idx, (rot, key, esp_med, exe_med, sig, autom) in enumerate(etapas):
                fator = 1.25 if esp_med >= 30 else 1.0
                espera = 0 if idx == 0 else lognormal(esp_med * fator, 0.55)
                if status == "Cancelado" and idx > 3:
                    espera = ""
                    exe_min = 0
                else:
                    exe_min = 0 if autom else lognormal(exe_med, sig)
                espera_min = round(espera * 60, 1) if espera != "" else ""
                if status == "Cancelado" and idx > 3:
                    d_fim = ""
                else:
                    dias = int((espera if espera != "" else 0) / 24) + int(
                        (exe_min or 0) / 480) + random.randint(0, 1)
                    d_fim = d_ini + dt.timedelta(days=min(dias, 200))
                    if d_fim > FIM:
                        d_fim = FIM
                fato.append([
                    f"EXC-{n:06d}", f"CIC-{ciclo + 1:05d}", etapa_map[key], un_map[unidade],
                    sis_map[random.choice([SISTEMAS[0], SISTEMAS[1], SISTEMAS[4]])],
                    ta_map[random.choice(TIPOS_ATIVIDADE[:5])], st_map[status],
                    random.randint(1, 4), data_key(d_ini), data_key(d_fim),
                    espera_min, exe_min,
                    round(float(espera_min or 0) / 60 + float(exe_min or 0) / 60, 2),
                    1 if pct(0.05) else 0, 1 if autom else 0,
                    round(float(exe_min or 0) / 60 * 71.20, 2),
                ])
                if d_fim:
                    d_ini = d_fim + dt.timedelta(days=random.randint(0, 1))
    csv_gravar(pasta, "fato_execucao.csv",
               ["id_execucao", "id_ciclo", "etapa_key", "unidade_key", "sistema_key",
                "tipo_atividade_key", "status_execucao_key", "projeto_key",
                "data_inicio_key", "data_fim_key", "tempo_espera_min", "tempo_execucao_min",
                "tempo_total_h", "flag_retrabalho", "flag_automatizada",
                "custo_execucao_rs"], fato)


# =================================================================
# CENARIO 4 - ATENDIMENTO DE LOCAL DE CRIME
# =================================================================
def cenario4_local_crime(pasta):
    etapas = [
        ("Acionamento da equipe", "Acionamento", 4, 30, 0.5, 1),
        ("Deslocamento ao local", "Deslocamento", 14, 120, 0.8, 0),
        ("Isolamento e preservacao", "Isolamento", 3, 45, 0.5, 0),
        ("Coleta de vestigios", "Coleta", 6, 180, 0.7, 0),
        ("Registro fotografico", "Fotografia", 4, 60, 0.6, 1),
        ("Acondicionamento e lacre", "Lacre", 5, 40, 0.6, 0),
        ("Liberacao do local", "Liberacao", 9, 30, 0.7, 0),
        ("Relatorio de atendimento", "Relatorio", 7, 90, 0.6, 0),
    ]
    etapa_map, _ = dim([e[1] for e in etapas])
    unidade_padrao = {
        "Acionamento": "ATO - Gabinete", "Deslocamento": "ATV - Campo",
        "Isolamento": "ATV - Campo", "Coleta": "ATV - Campo",
        "Fotografia": "ATV - Campo", "Lacre": "IML - Medicina Legal",
        "Liberacao": "ATO - Gabinete", "Relatorio": "ATO - Gabinete",
    }
    csv_gravar(pasta, "dim_etapa.csv",
               ["etapa_key", "etapa", "sequencia", "unidade_padrao", "ativada_no_tobe"],
               [[etapa_map[e[1]], e[1], i + 1, unidade_padrao[e[1]], 0] for i, e in enumerate(etapas)])

    unidades = ["ATO - Gabinete", "ATV - Campo", "IML - Medicina Legal",
                "LAB - Fisica", "CTRL - Plantao"]
    un_map, un_rows = dim(unidades)
    csv_gravar(pasta, "dim_unidade.csv", ["unidade_key", "unidade", "tipo"],
               [[k, u, "Campo" if u.startswith("ATV") else (
                   "Laboratorio" if u.startswith(("LAB", "IML")) else "Apoio")]
                for k, u in un_rows])

    sis_map, sis_rows = dim(SISTEMAS)
    csv_gravar(pasta, "dim_sistema.csv",
               ["sistema_key", "sistema", "digitizado", "integrado"],
               [[k, s, 1 if i >= 1 else 0, 1 if i in (1, 3, 5) else 0]
                for i, (k, s) in enumerate(sis_rows)])

    ta_map, ta_rows = dim(TIPOS_ATIVIDADE)
    csv_gravar(pasta, "dim_tipo_atividade.csv", ["tipo_atividade_key", "tipo_atividade"], ta_rows)

    st = ["Concluido", "Em andamento", "Devolvido", "Cancelado"]
    st_map, st_rows = dim(st)
    csv_gravar(pasta, "dim_status_execucao.csv", ["status_execucao_key", "status_execucao"], st_rows)

    prj = [(1, "PRJ-030 - App de atendimento de local"),
           (2, "PRJ-031 - Checklist digital de vestigios"),
           (3, "PRJ-032 - Roteirizacao de equipes"),
           (4, "PRJ-033 - Integracao com a custodia")]
    csv_gravar(pasta, "dim_projeto.csv", ["projeto_key", "projeto", "escopo"],
               [[k, p, p.split(" - ")[1][:40]] for k, p in prj])

    gravar_calendario(pasta)

    fato, n = [], 0
    for ciclo in range(240):
        d0 = data_aleatoria()
        unidade = random.choices(unidades, weights=[24, 42, 12, 12, 10])[0]
        qtd = random.randint(4, 9)
        for rep in range(qtd):
            n += 1
            d_ini = d0
            status = "Cancelado" if pct(0.03) else (
                "Devolvido" if pct(0.08) else (
                    "Em andamento" if pct(0.15) else "Concluido"))
            for idx, (rot, key, esp_med, exe_med, sig, autom) in enumerate(etapas):
                fator = 1.35 if esp_med >= 10 else 1.0
                espera = 0 if idx == 0 else lognormal(esp_med * fator, 0.6)
                if status == "Cancelado" and idx > 1:
                    espera = ""
                    exe_min = 0
                else:
                    exe_min = 0 if autom else lognormal(exe_med, sig)
                espera_min = round(espera * 60, 1) if espera != "" else ""
                if status == "Cancelado" and idx > 1:
                    d_fim = ""
                else:
                    dias = int((espera if espera != "" else 0) / 24) + int(
                        (exe_min or 0) / 480) + random.randint(0, 2)
                    d_fim = d_ini + dt.timedelta(days=min(dias, 180))
                    if d_fim > FIM:
                        d_fim = FIM
                fato.append([
                    f"EXL-{n:06d}", f"CIC-{ciclo + 1:05d}", etapa_map[key], un_map[unidade],
                    sis_map[random.choice([SISTEMAS[0], SISTEMAS[2], SISTEMAS[4]])],
                    ta_map[random.choice(TIPOS_ATIVIDADE[:5])], st_map[status],
                    random.randint(1, 4), data_key(d_ini), data_key(d_fim),
                    espera_min, exe_min,
                    round(float(espera_min or 0) / 60 + float(exe_min or 0) / 60, 2),
                    1 if pct(0.09) else 0, 1 if autom else 0,
                    round(float(exe_min or 0) / 60 * 68.50, 2),
                ])
                if d_fim:
                    d_ini = d_fim + dt.timedelta(days=random.randint(0, 2))
    csv_gravar(pasta, "fato_execucao.csv",
               ["id_execucao", "id_ciclo", "etapa_key", "unidade_key", "sistema_key",
                "tipo_atividade_key", "status_execucao_key", "projeto_key",
                "data_inicio_key", "data_fim_key", "tempo_espera_min", "tempo_execucao_min",
                "tempo_total_h", "flag_retrabalho", "flag_automatizada",
                "custo_execucao_rs"], fato)


# =================================================================
# CENARIO 5 - ANALISE LABORATORIAL (DNA / TOXICOLOGIA)
# =================================================================
def cenario5_laboratorio(pasta):
    etapas = [
        ("Recebimento e protocolo", "Recebimento", 4, 30, 0.5, 1),
        ("Triagem da amostra", "Triagem", 8, 45, 0.6, 0),
        ("Preparo e extracao", "Extracao", 12, 180, 0.8, 0),
        ("Quantificacao", "Quantificacao", 10, 60, 0.7, 0),
        ("Amplificacao (PCR)", "Amplificacao", 16, 120, 0.8, 0),
        ("Eletroforese", "Eletroforese", 18, 90, 0.8, 0),
        ("Interpretacao do perfil", "Interpretacao", 9, 150, 0.7, 0),
        ("Revisao e laudo", "Laudo", 8, 60, 0.6, 1),
    ]
    etapa_map, _ = dim([e[1] for e in etapas])
    unidade_padrao = {
        "Recebimento": "LAB - Biologia", "Triagem": "LAB - Biologia",
        "Extracao": "LAB - Biologia", "Quantificacao": "LAB - Toxicologia",
        "Amplificacao": "LAB - Biologia", "Eletroforese": "LAB - Fisica",
        "Interpretacao": "LAB - Biologia", "Laudo": "CTRL - Qualidade",
    }
    csv_gravar(pasta, "dim_etapa.csv",
               ["etapa_key", "etapa", "sequencia", "unidade_padrao", "ativada_no_tobe"],
               [[etapa_map[e[1]], e[1], i + 1, unidade_padrao[e[1]], 0] for i, e in enumerate(etapas)])

    unidades = ["LAB - Biologia", "LAB - Toxicologia", "LAB - Fisica",
                "IML - Medicina Legal", "CTRL - Qualidade"]
    un_map, un_rows = dim(unidades)
    csv_gravar(pasta, "dim_unidade.csv", ["unidade_key", "unidade", "tipo"],
               [[k, u, "Laboratorio" if u.startswith(("LAB", "IML")) else "Controle"]
                for k, u in un_rows])

    sis_map, sis_rows = dim(SISTEMAS)
    csv_gravar(pasta, "dim_sistema.csv",
               ["sistema_key", "sistema", "digitizado", "integrado"],
               [[k, s, 1 if i >= 1 else 0, 1 if i in (1, 3, 5) else 0]
                for i, (k, s) in enumerate(sis_rows)])

    ta_map, ta_rows = dim(TIPOS_ATIVIDADE)
    csv_gravar(pasta, "dim_tipo_atividade.csv", ["tipo_atividade_key", "tipo_atividade"], ta_rows)

    st = ["Concluido", "Em andamento", "Devolvido", "Cancelado"]
    st_map, st_rows = dim(st)
    csv_gravar(pasta, "dim_status_execucao.csv", ["status_execucao_key", "status_execucao"], st_rows)

    prj = [(1, "PRJ-040 - Integracao LIMS x SIGT"),
           (2, "PRJ-041 - Fila unica de amostras"),
           (3, "PRJ-042 - Alerta de prazo de analise"),
           (4, "PRJ-043 - Painel de capacidade do laboratorio")]
    csv_gravar(pasta, "dim_projeto.csv", ["projeto_key", "projeto", "escopo"],
               [[k, p, p.split(" - ")[1][:40]] for k, p in prj])

    gravar_calendario(pasta)

    fato, n = [], 0
    for ciclo in range(260):
        d0 = data_aleatoria()
        unidade = random.choices(unidades, weights=[30, 26, 18, 12, 14])[0]
        qtd = random.randint(4, 9)
        for rep in range(qtd):
            n += 1
            d_ini = d0
            status = "Cancelado" if pct(0.02) else (
                "Devolvido" if pct(0.06) else (
                    "Em andamento" if pct(0.12) else "Concluido"))
            for idx, (rot, key, esp_med, exe_med, sig, autom) in enumerate(etapas):
                fator = 1.30 if key in ("Amplificacao", "Eletroforese") else 1.0
                espera = 0 if idx == 0 else lognormal(esp_med * fator, 0.6)
                if status == "Cancelado" and idx > 2:
                    espera = ""
                    exe_min = 0
                else:
                    exe_min = 0 if autom else lognormal(exe_med, sig)
                espera_min = round(espera * 60, 1) if espera != "" else ""
                if status == "Cancelado" and idx > 2:
                    d_fim = ""
                else:
                    dias = int((espera if espera != "" else 0) / 24) + int(
                        (exe_min or 0) / 480) + random.randint(0, 2)
                    d_fim = d_ini + dt.timedelta(days=min(dias, 200))
                    if d_fim > FIM:
                        d_fim = FIM
                fato.append([
                    f"EXA-{n:06d}", f"CIC-{ciclo + 1:05d}", etapa_map[key], un_map[unidade],
                    sis_map[random.choice([SISTEMAS[1], SISTEMAS[2], SISTEMAS[4]])],
                    ta_map[random.choice(TIPOS_ATIVIDADE[:4])], st_map[status],
                    random.randint(1, 4), data_key(d_ini), data_key(d_fim),
                    espera_min, exe_min,
                    round(float(espera_min or 0) / 60 + float(exe_min or 0) / 60, 2),
                    1 if pct(0.07) else 0, 1 if autom else 0,
                    round(float(exe_min or 0) / 60 * 82.40, 2),
                ])
                if d_fim:
                    d_ini = d_fim + dt.timedelta(days=random.randint(0, 2))
    csv_gravar(pasta, "fato_execucao.csv",
               ["id_execucao", "id_ciclo", "etapa_key", "unidade_key", "sistema_key",
                "tipo_atividade_key", "status_execucao_key", "projeto_key",
                "data_inicio_key", "data_fim_key", "tempo_espera_min", "tempo_execucao_min",
                "tempo_total_h", "flag_retrabalho", "flag_automatizada",
                "custo_execucao_rs"], fato)


# =================================================================
# READMES
# =================================================================
README_GERAL = r"""# Aula 6 - Datasets de Processo (Painel de Processo + Gestao de Projetos)

Cinco **processos reais da POLITEC/MT**, medidos etapa a etapa. Sao a base do
painel da manha (BI) e do metodo da tarde: AS-IS -> BPMN/Mermaid -> **gargalo
medido** -> TO-BE -> **automacao**.

Cada cenario tem o mesmo esquema em **modelo estrela**, com as mesmas dimensoes.
O fato tem uma linha por **execucao de etapa**, com **tempo de espera** (fila) e
**tempo de execucao** (trabalho) separados. E essa separacao que revela o
gargalo.

| # | Cenario | Pasta | Workbook Excel | Fato | Linhas |
|---|---------|-------|----------------|------|--------|
| 1 | Requisicao pericial | `cenario1_processo_pericial/` | `Cenario1_Requisicao_Pericial.xlsx` | `fato_execucao` | **10.352** |
| 2 | Empenho e contrato | `cenario2_processo_orcamento/` | `Cenario2_Empenho_Contrato.xlsx` | `fato_execucao` | **9.541** |
| 3 | Cadeia de custodia | `cenario3_processo_custodia/` | `Cenario3_Cadeia_Custodia.xlsx` | `fato_execucao` | **10.840** |
| 4 | Local de crime | `cenario4_local_crime/` | `Cenario4_Local_Crime.xlsx` | `fato_execucao` | **12.664** |
| 5 | Analise laboratorial | `cenario5_analise_laboratorial/` | `Cenario5_Analise_Laboratorial.xlsx` | `fato_execucao` | **13.896** |

Todos com `dim_calendario` de 1.096 dias (2023-01-01 a 2025-12-31).

> **Para a sala de aula**, use o workbook `.xlsx` de cada pasta: ele traz todas
> as tabelas em abas separadas (`fato_execucao`, `dim_*`) mais uma aba
> `LEIA-ME`. Os CSVs ficam como fonte e para quem preferir importar por pasta.

---

## O schema (identico nos 5 cenarios)

```text
      dim_calendario   dim_projeto        dim_tipo_atividade
             |              |                       |
   dim_sistema --- fato_execucao --- dim_status_execucao
             |              |
      dim_unidade ---  dim_etapa
```

### Fato: `fato_execucao` (grao = 1 execucao de etapa)

| Coluna | O que e | Como usar |
|---|---|---|
| `id_execucao` | Identificador unico da execucao | chave da linha |
| `id_ciclo` | Identificador do **processo** (todos os casos comecam com `CIC-`) | agrupa as etapas de um caso |
| `etapa_key` | Etapa do processo | **dimensao que identifica o gargalo** |
| `unidade_key` | Quem executa | swimlane do diagrama |
| `sistema_key` | Em que sistema/support | identifica o trabalho manual |
| `tipo_atividade_key` | Manual / automatizada / aprovacao / decisao | base do mapeamento BPMN |
| `status_execucao_key` | Concluido / em andamento / devolvido / cancelado | qualidade do dado |
| `projeto_key` | Projeto de intervencao | planejar o TO-BE |
| `data_inicio_key` / `data_fim_key` | Datas | linha do tempo, lead time |
| **`tempo_espera_min`** | **Minutos na fila ANTES de comecar** | **onde o gargalo costuma estar** |
| `tempo_execucao_min` | Minutos de trabalho efetivo | onde ha trabalho real |
| `tempo_total_h` | Soma dos dois, em **horas** | tempo de ciclo daquela etapa |
| `flag_retrabalho` | 1 se a etapa voltou | desperdicio |
| `flag_automatizada` | 1 se ja automatizada | baseline de automacao |
| `custo_execucao_rs` | Custo da mao de obra daquela execucao, em **R$** | custo do processo |

### Dimensoes

| Dimensao | Linhas | Chave | Atributos |
|---|---|---|---|
| `dim_etapa` | 7-8 | `etapa_key` | etapa, sequencia, unidade_padrao, ativada_no_tobe |
| `dim_unidade` | 5-7 | `unidade_key` | unidade, tipo (Laboratorio / Apoio / Campo / Controle) |
| `dim_sistema` | 6 | `sistema_key` | sistema, digitizado, integrado |
| `dim_tipo_atividade` | 6 | `tipo_atividade_key` | tipo_atividade |
| `dim_status_execucao` | 4 | `status_execucao_key` | status_execucao |
| `dim_projeto` | 4 | `projeto_key` | projeto, escopo |
| `dim_calendario` | 1.096 | `data_key` | data, ano, mes, ano_mes, trimestre, dia, dia_semana |

> **Atencao**: a `fato_execucao` e a `dim_etapa` usam a **mesma chave**
> (`etapa_key`), entao o join funciona. Para ordenar as etapas do processo,
> use `dim_etapa.sequencia`, e nao o texto da etapa.

---

## O metodo que estes dados sustentam

1. **AS-IS**: leia `dim_etapa` em ordem (`sequencia`) e desenhe o diagrama.
2. **Faca as perguntas do metodo** (Quem inicia? Onde espera? Quem decide?).
3. **Meça o gargalo**: some `tempo_espera_min` por `etapa_key`. A etapa com
   maior soma de espera e o gargalo (ver **Pareto das esperas** no caderno).
4. **TO-BE**: redesenhe o diagrama **eliminando ou automatizando** a etapa
   gargalo. Marque em `dim_etapa.ativada_no_tobe`.
5. **Automacao**: proponha um artefato digital (App, formulario, script) e
   calcule o **ganho** (minutos/ano e R$/ano poupados).

---

## Como usar (Excel / Google Sheets / Power BI)

1. **CSV UTF-8 com BOM, separador `;`**. Importe direto.
2. Comece pela tabela dinamica: `etapa` nas linhas, `SOMA(tempo_espera_min)`
   nas colunas. A maior barra e o gargalo.
3. Em Power BI, faca o mesmo com uma **matriz** e um **grafico de barras
   empilhadas** (espera x execucao por etapa).

---

## Convencoes

- CSV UTF-8 com BOM, separador `;`, datas ISO `AAAA-MM-DD`.
- `data_key` inteiro no formato `AAAAMMDD`.
- Chaves substitutas inteiras 1..N em ordem alfabetica.
- `tempo_espera_min` e `tempo_execucao_min` em **minutos** (fracionarios com 1 casa);
  `tempo_total_h` em **horas** (2 casas); `custo_execucao_rs` em **R$**.
- Gerado por `../gerar_datasets_aula6.py` (semente fixa `20260610`).
- Dados sinteticos: qualquer semelhanca com processos reais e coincidencia.
"""

README_CEN = {}

README_CEN["cenario1_processo_pericial"] = r"""# Cenario 1 - Processo de Requisicao Pericial (AS-IS)

O fluxo mais iconico da POLITEC: da delegacia ate a assinatura do
laudo. O gargalo classico e a **fila do perito** (etapa 4).

Numeros **medidos** no dataset gerado (media por execucao de etapa):

| Etapa | Espera media | Execucao media | Retrabalho |
|---|---|---|---|
| 1. Entrada da requisicao | 0 h | 0 h | 11,2% |
| 2. Triagem e classificacao | 10 h | 1 h | 12,7% |
| 3. Distribuicao ao setor | 13 h | 1 h | 11,4% |
| **4. Fila de espera do perito** | **44 h** | 0 h | 12,1% |
| 5. Analise do exame | 9 h | 5 h | 11,5% |
| 6. Revisao tecnica | 13 h | 2 h | 10,4% |
| 7. Assinatura e release | 10 h | 0 h | 11,7% |
| 8. Envio e arquivamento | 7 h | 0 h | 11,7% |

**Achado principal**: a etapa 4 concentra **41,5% de toda a espera** do
processo, e o processo inteiro e **92,4% espera** contra 7,6% de trabalho
efetivo. A analise (etapa 5) tem mais execucao (5 h) que qualquer outra, mas
apenas 9 h de espera - a **fila**, nao o trabalho, e o gargalo.

**Para onde aponta a intervencao**: a etapa 4. A TO-BE combina uma fila
priorizada por prazo legal (nao por ordem de chegada) com um painel de carga
por perito, reduzindo a espera sem aumentar a capacidade.

**Sugestao de Mermaid**: desenhe as 8 etapas como retangulos, com os sistemas
como swimlanes (SIGT, papel, e-mail).
"""

README_CEN["cenario2_processo_orcamento"] = r"""# Cenario 2 - Processo de Empenho e Contrato

O caminho do dinheiro publico: pedido, cotacao, parecer juridico, autorizacao,
empenho e publicacao. Aqui o gargalo e um **conjunto** (parecer + autorizacao
= 51,2% da espera), tipico de processo com varias aprovacoes encadeadas.

Numeros **medidos** no dataset gerado (media por execucao de etapa):

| Etapa | Espera media | Execucao media | Retrabalho |
|---|---|---|---|
| 1. Pedido do setor (papeis) | 0 h | 4 h | 15,9% |
| 2. Cotacao no sistema | 10 h | 0 h | 16,4% |
| 3. Mapa comparativo | 21 h | 6 h | 17,0% |
| **4. Parecer juridico** | **36 h** | 5 h | 17,0% |
| **5. Autorizacao do ordenador** | **27 h** | 1 h | 16,3% |
| 6. Empenho e contratacao | 11 h | 0 h | 16,6% |
| 6. Publicacao do ato | 18 h | 0 h | 16,9% |

**Achado principal**: **51,2% da espera** esta em duas etapas de aprovacao
(parecer + autorizacao), e o retrabalho e o mais alto dos cinco datasets
(**~16,5%**). O mapa comparativo (etapa 3) tem **6 h de execucao** — o maior
trabalho manual do processo, e ele e atrasado por causa das aprovacoes.

**Para onde aponta a intervencao**: as duas aprovacoes. A TO-BE move a **pauta
automatica**: o sistema monta a pauta (todo expediente dentro do prazo) e
dispara a aprovacao, com fila priorizada por dotacao critica.

**Sugestao de Mermaid**: use subgraphs por unidade (Divisao de Compras,
Juridico, Controle Interno). Destaque o gateway de decisao "dotacao
suficiente?".

---

## Observacao sobre nomes duplicados

As etapas 6 e 7 desta tabela aparecem com prefixos iguais porque a coluna
`etapa` foi truncada na geracao. A distincao esta em `dim_etapa.sequencia`
(6 = Empenho, 7 = Publicacao). Sempre ordene por `sequencia`, nunca pelo texto.
"""

README_CEN["cenario3_processo_custodia"] = r"""# Cenario 3 - Cadeia de Custodia de Evidencias

O processo mais critico quanto a rastreabilidade: da coleta no local ate a baixa.
O gargalo nao e so tempo - e **risco de rastreabilidade** (perda de lacre,
divergencia). O TO-BE aqui prioriza **rastreio** acima de velocidade.

Numeros **medidos** no dataset gerado (media por execucao de etapa):

| Etapa | Espera media | Execucao media | Divergencia de lacre |
|---|---|---|---|
| 1. Coleta no local | 0 h | 2 h | 4,9% |
| 2. Acondicionamento e lacre | 11 h | 1 h | 5,5% |
| 3. Registro da ocorrencia | 12 h | 0 h | 3,9% |
| 4. Transporte ao destino | 16 h | 3 h | 4,2% |
| 5. Recebimento e conferencia | 14 h | 1 h | 5,5% |
| **6. Guarda / refrigeracao** | **55 h** | 0 h | 4,0% |
| 7. Pericia propriamente dita | 21 h | 6 h | 5,2% |
| 8. Baixa e destino final | 25 h | 0 h | 4,6% |

**Achado principal**: a etapa 6 concentra **35,3% da espera**, e o processo e
**92,5% espera**. A pericia (etapa 7) tem o maior trabalho (6 h) mas apenas 21 h
de espera. A divergencia de lacre aparece em **~4,8%** das execucoes — pouco em
termos absolutos, mas grave em termos de processo (um lacre aberto pode
inviabilizar a prova).

**Para onde aponta a intervencao**: a etapa 6 (guarda) e a rastreabilidade. A
TO-BE usa **QR Code por evidencia** e **app de custodia**: cada recebimento
digitaliza o lacre, cada transferencia registra responsavel e hora, e um alerta
dispara se a evidencia ficar parada alem do prazo.

**Sugestao de Mermaid**: BPMN com **mensagens** (o QR substitui o papel) e um
gateway de "lacre confere?". Este e o melhor cenario para ensinar **rastreio**
em vez de apenas velocidade.
"""

README_CEN["cenario4_local_crime"] = r"""# Cenario 4 - Atendimento de Local de Crime

O processo que comeca no acionamento da equipe e termina no relatorio de
atendimento. O gargalo classico nao esta na coleta (o trabalho visivel), mas no
**deslocamento** e na **liberacao do local** - as duas filas que dependem de
equipe, veiculo e autoridade.

Numeros **medidos** no dataset gerado (media por execucao de etapa):

| Etapa | Espera media | Execucao media | Retrabalho |
|---|---|---|---|
| 1. Acionamento da equipe | 0 h | 0 h | 8,5% |
| **2. Deslocamento ao local** | **22,9 h** | 2,6 h | 7,5% |
| 3. Isolamento e preservacao | 3,9 h | 0,8 h | 8,0% |
| 4. Coleta de vestigios | 7,5 h | 3,7 h | 8,3% |
| 5. Registro fotografico | 5,1 h | 0 h | 8,1% |
| 6. Acondicionamento e lacre | 6,2 h | 0,8 h | 8,6% |
| 7. Liberacao do local | 10,8 h | 0,6 h | 8,8% |
| 8. Relatorio de atendimento | 8,6 h | 1,7 h | 9,0% |

**Achado principal**: o deslocamento concentra **35,2% da espera**, e o processo
e **86,5% espera**. A coleta tem o maior trabalho manual (3,7 h), mas nao e o
gargalo. O retrabalho e sistemico (8,4%, parecido em todas as etapas), sinal de
problema de checklist/padrao, nao de uma equipe especifica.

**Para onde aponta a intervencao**: roteirizacao de equipes + checklist digital
de vestigios. A TO-BE reduz o deslocamento com fila por proximidade e elimina a
redigitacao do relatorio.

**Sugestao de Mermaid**: swimlanes por unidade (ATO, ATV - Campo, IML, CTRL) e
um gateway "local preservado?" antes da coleta.
"""

README_CEN["cenario5_analise_laboratorial"] = r"""# Cenario 5 - Analise Laboratorial (DNA / Toxicologia)

O processo de bancada: do recebimento da amostra ao laudo assinado. O gargalo
tipico e a **fila do equipamento** (amplificacao e eletroforese), nao a
interpretacao - que e o trabalho mais visivel do perito.

Numeros **medidos** no dataset gerado (media por execucao de etapa):

| Etapa | Espera media | Execucao media | Retrabalho |
|---|---|---|---|
| 1. Recebimento e protocolo | 0 h | 0 h | 6,6% |
| 2. Triagem da amostra | 10,2 h | 0,9 h | 7,1% |
| 3. Preparo e extracao | 15,5 h | 4,2 h | 6,9% |
| 4. Quantificacao | 12,2 h | 1,3 h | 6,5% |
| **5. Amplificacao (PCR)** | **24,6 h** | 2,6 h | 7,0% |
| **6. Eletroforese** | **27,5 h** | 2,1 h | 6,2% |
| 7. Interpretacao do perfil | 11,0 h | 3,2 h | 6,8% |
| 8. Revisao e laudo | 9,7 h | 0 h | 7,7% |

**Achado principal**: as duas etapas de equipamento concentram **47,1% da
espera** (24,9% + 22,2%), e o processo e **88,6% espera**. A interpretacao tem o
maior trabalho manual (3,2 h), mas nao e o gargalo. O retrabalho e baixo e
uniforme (6,8%) - o problema e **capacidade de equipamento**, nao erro de
execucao.

**Para onde aponta a intervencao**: fila unica de amostras + painel de
capacidade do laboratorio. A TO-BE agenda a placa por prazo e prioridade, em vez
de ordem de chegada.

**Sugestao de Mermaid**: swimlanes por laboratorio (Biologia, Toxicologia,
Fisica) e um gateway "amostra conforme?" na triagem.
"""


def escrever_readmes():
    for nome, txt in README_CEN.items():
        (DATASETS / nome).mkdir(parents=True, exist_ok=True)
        (DATASETS / nome / "README.md").write_text(txt, encoding="utf-8")
    (DATASETS / "README.md").write_text(README_GERAL, encoding="utf-8")


def main():
    cenario1_pericial(DATASETS / "cenario1_processo_pericial")
    cenario2_orcamento(DATASETS / "cenario2_processo_orcamento")
    cenario3_custodia(DATASETS / "cenario3_processo_custodia")
    cenario4_local_crime(DATASETS / "cenario4_local_crime")
    cenario5_laboratorio(DATASETS / "cenario5_analise_laboratorial")
    escrever_readmes()
    print("5 datasets de processo + READMEs gerados em:", DATASETS.relative_to(RAIZ))
    for p in sorted(DATASETS.iterdir()):
        if p.is_dir():
            print(f"  {p.name:34s}  {len(list(p.glob('*.csv')))} CSVs")
    print("Semente:", SEED)


if __name__ == "__main__":
    main()