# -*- coding: utf-8 -*-
"""Gera os datasets de Orcamento e Contratos (modelo estrela) da Aula 4.

Tema: execucao orcamentaria e contratos administrativos de um orgao de
pericia oficial (POLITEC/MT). O conjunto e sintetico e serve para a
preparacao de Power BI Desktop (Parte 0 do caderno do Dia 4).

Produz, em Aula 4/datasets/orcamento/:

  Orcamento_Contratos_LIMPO.xlsx   -> gabarito do professor (star schema limpo)
  Orcamento_Contratos_SUJO.xlsx    -> para os alunos: mesmos dados com defeitos
  fato_empenhos.csv, fato_dotacao.csv, dim_*.csv  -> modelo estrela em CSV
  README.md                        -> dicionario de dados + lista de defeitos

Modelo estrela (grao = 1 empenho):

  fato_empenhos (620 linhas)
    -> dim_calendario, dim_contrato, dim_fornecedor, dim_setor,
       dim_rubrica, dim_modalidade, dim_fonte, dim_status_empenho
  fato_dotacao (192 linhas) -> orcado por setor x rubrica x ano
    -> dim_setor, dim_rubrica, dim_calendario (ano)

Uso:  python gerar_datasets_orcamento.py
"""
import csv
import datetime as dt
import pathlib
import random

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

RAIZ = pathlib.Path(__file__).resolve().parent
DESTINO = RAIZ / "datasets" / "orcamento"
SEED = 20260116

random.seed(SEED)


# =================================================================
# CATALOGOS DE DIMENSAO
# =================================================================
SETORES = [
    (1, "ADM", "Diretoria de Administracao"),
    (2, "IDT", "Diretoria de Identificacao"),
    (3, "DLF", "Diretoria de Laboratorios Forenses"),
    (4, "DNA", "Coordenadoria de Pericias de DNA"),
    (5, "TOX", "Laboratorio de Toxicologia"),
    (6, "BAL", "Laboratorio de Balistica"),
    (7, "IML", "Instituto Medico Legal"),
    (8, "INF", "Setor de Pericias de Informatica"),
]

RUBRICAS = [
    (1, "339014", "Diarias", "Custeio"),
    (2, "339030", "Material de Consumo", "Custeio"),
    (3, "339033", "Passagens e Despesas com Locomocao", "Custeio"),
    (4, "339035", "Servicos de Consultoria", "Custeio"),
    (5, "339039", "Outros Servicos de Terceiros - PJ", "Custeio"),
    (6, "339047", "Obrigacoes Tributarias e Contributivas", "Custeio"),
    (7, "449052", "Equipamentos e Material Permanente", "Investimento"),
    (8, "449051", "Obras e Instalacoes", "Investimento"),
]

MODALIDADES = [
    (1, "Dispensa de Licitacao"),
    (2, "Pregao Eletronico"),
    (3, "Concorrencia"),
    (4, "Inexigibilidade"),
    (5, "Adesao a Ata de Registro de Precos"),
]

FONTES = [
    (1, "Tesouro Estadual"),
    (2, "Convenio Federal"),
    (3, "Fundo Especial"),
    (4, "Emenda Parlamentar"),
]

STATUS = [
    (1, "Empenhado"),
    (2, "Em processo de liquidacao"),
    (3, "Liquidado"),
    (4, "Pago"),
    (5, "Cancelado"),
]

MUNICIPIOS_MT = [
    ("Cuiaba", "MT"), ("Varzea Grande", "MT"), ("Rondonopolis", "MT"),
    ("Sinop", "MT"), ("Tangara da Serra", "MT"), ("Caceres", "MT"),
    ("Sorriso", "MT"), ("Barra do Garcas", "MT"), ("Primavera do Leste", "MT"),
    ("Lucas do Rio Verde", "MT"),
]

PORTA = ["ME", "EPP", "Medio", "Grande"]

_PREFIXOS = ["ALFA", "BIOGEN", "CIENTIFICA", "DELTA", "FORENSE", "GENESYS",
             "HEXA", "INOVA", "LABOR", "ORION", "PRISMA", "QUANTA", "SOLAR",
             "TECNO", "VETOR", "XENON", "ATIVA", "CENTRAL", "DIAGNOSTICA",
             "EXATA", "FORTE", "GLOBAL", "HORIZONTE", "INTERLAB", "JUPITER",
             "LIDER", "MERIDIANO", "NEXO", "ONIX", "PONTO", "QUIMICA",
             "RADIAL", "SEGURA", "TREND", "UNIAO", "VERTICE", "WEST",
             "XL", "ZENITH", "APEX"]
_SUFIXOS = ["SUPRIMENTOS LTDA", "LABORATORIOS LTDA", "COMERCIO E SERVICOS EIRELI",
            "TECNOLOGIA LTDA", "DIAGNOSTICOS LTDA", "SEGURANCA LTDA",
            "ENGENHARIA LTDA", "DISTRIBUIDORA LTDA"]

OBJETOS = [
    "Fornecimento de reagentes analiticos",
    "Locacao de veiculos sem motorista",
    "Manutencao predial preventiva e corretiva",
    "Fornecimento de equipamentos de protecao individual",
    "Servicos de tecnologia da informacao e suporte",
    "Fornecimento de material de escritorio",
    "Servicos de vigilancia patrimonial",
    "Fornecimento de kits de coleta de DNA",
    "Manutencao de equipamentos laboratoriais",
    "Fornecimento de armamento e municao",
    "Servico de impressao corporativa",
    "Fornecimento de mobiliario de escritorio",
    "Contratacao de seguro patrimonial",
    "Servico de transporte de amostras biologicas",
    "Fornecimento de vidrarias e insumos de laboratorio",
]


def cnpj_sintetico(n):
    base = f"{n:08d}"
    return base


def gerar_fornecedores(qtd=40):
    combos = []
    for p in _PREFIXOS:
        for s in _SUFIXOS:
            combos.append(f"{p} {s}")
    random.shuffle(combos)
    fornecedores = []
    cnpjs = set()
    for i, nome in enumerate(combos[:qtd], start=1):
        while True:
            c = f"{random.randint(10, 99)}.{random.randint(100, 999)}.{random.randint(100, 999)}" \
                f"/0001-{random.randint(10, 99)}"
            if c not in cnpjs:
                cnpjs.add(c)
                break
        mun, uf = random.choice(MUNICIPIOS_MT) if random.random() < 0.7 else random.choice(
            [("Sao Paulo", "SP"), ("Goiania", "GO"), ("Campo Grande", "MS"), ("Brasilia", "DF")])
        fornecedores.append({
            "fornecedor_key": i,
            "razao_social": nome,
            "cnpj": c,
            "porte": random.choice(PORTA),
            "municipio": mun,
            "uf": uf,
        })
    return fornecedores


def gerar_contratos(fornecedores, qtd=60):
    contratos = []
    for i in range(1, qtd + 1):
        forn = random.choice(fornecedores)
        ano = random.choice([2024, 2025, 2026])
        inicio = dt.date(ano, random.randint(1, 10), random.randint(1, 28))
        fim = inicio + dt.timedelta(days=random.randint(180, 730))
        tipo = random.choices(["Contrato", "Ata de Registro de Precos", "Convenio"],
                              weights=[6, 3, 1])[0]
        setor = random.choice(SETORES)[0]
        valor = round(random.uniform(50_000, 2_500_000), 2)
        contratos.append({
            "contrato_key": i,
            "numero": f"{random.choice([10, 20, 30, 40, 50, 60, 70])}/{ano}-{i:03d}",
            "tipo": tipo,
            "objeto": random.choice(OBJETOS),
            "data_inicio": inicio,
            "data_fim": fim,
            "valor_contrato": valor,
            "fornecedor_key": forn["fornecedor_key"],
            "setor_key": setor,
            "licitacao_numero": f"{random.choice(['PE', 'CC', 'DI', 'IL'])}-{ano}/{random.randint(1, 90):03d}",
        })
    return contratos


def gerar_calendario(ini=dt.date(2024, 1, 1), fim=dt.date(2026, 12, 31)):
    meses = ["", "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    semanas = ["", "Segunda-feira", "Terca-feira", "Quarta-feira", "Quinta-feira",
               "Sexta-feira", "Sabado", "Domingo"]
    linhas = []
    d = ini
    while d <= fim:
        linhas.append({
            "data_key": d.year * 10000 + d.month * 100 + d.day,
            "data": d,
            "ano": d.year,
            "mes": d.month,
            "nome_mes": meses[d.month],
            "ano_mes": f"{d.year:04d}-{d.month:02d}",
            "trimestre": (d.month - 1) // 3 + 1,
            "dia": d.day,
            "dia_semana": d.isoweekday(),
            "nome_dia_semana": semanas[d.isoweekday()],
        })
        d += dt.timedelta(days=1)
    return linhas


def gerar_empenhos(fornecedores, contratos, qtd=620):
    linhas = []
    seq = {}
    for _ in range(qtd):
        contrato = random.choice(contratos)
        forn = next(f for f in fornecedores if f["fornecedor_key"] == contrato["fornecedor_key"])
        ano = random.choices([2024, 2025, 2026], weights=[4, 6, 3])[0]
        dia = dt.date(ano, random.randint(1, 12), random.randint(1, 28))
        seq[ano] = seq.get(ano, 0) + 1
        status = random.choices([1, 2, 3, 4, 5], weights=[15, 12, 15, 50, 8])[0]
        valor_emp = round(random.uniform(2_000, 600_000), 2)
        if status == 5:
            liq = pago = 0.0
        elif status == 1:
            liq = pago = 0.0
        elif status == 2:
            liq = round(valor_emp * random.uniform(0, 0.6), 2)
            pago = 0.0
        elif status == 3:
            liq = round(valor_emp * random.uniform(0.6, 1.0), 2)
            pago = 0.0
        else:  # Pago
            liq = valor_emp
            pago = valor_emp
        linhas.append({
            "id_empenho": f"{ano}NE{seq[ano]:06d}",
            "data_empenho": dia,
            "data_empenho_key": dia.year * 10000 + dia.month * 100 + dia.day,
            "contrato_key": contrato["contrato_key"],
            "fornecedor_key": forn["fornecedor_key"],
            "setor_key": contrato["setor_key"] if random.random() < 0.75 else random.choice(SETORES)[0],
            "rubrica_key": random.randint(1, 8),
            "modalidade_key": random.choices([1, 2, 3, 4, 5], weights=[3, 5, 1, 2, 2])[0],
            "fonte_key": random.choices([1, 2, 3, 4], weights=[5, 2, 2, 1])[0],
            "status_key": status,
            "valor_empenhado": valor_emp,
            "valor_liquidado": liq,
            "valor_pago": pago,
            "quantidade_itens": random.randint(1, 200),
        })
    linhas.sort(key=lambda r: (r["data_empenho"], r["id_empenho"]))
    return linhas


def gerar_dotacao(empenhos):
    """Dotacao por setor x rubrica x ano, sempre >= ao empenhado do periodo."""
    chave = {}
    for e in empenhos:
        k = (e["data_empenho"].year, e["setor_key"], e["rubrica_key"])
        chave[k] = chave.get(k, 0.0) + e["valor_empenhado"]
    linhas = []
    for ano in (2024, 2025, 2026):
        for s in SETORES:
            for r in RUBRICAS:
                emp = chave.get((ano, s[0], r[0]), 0.0)
                base = emp if emp > 0 else random.uniform(20_000, 250_000)
                atualizado = round(base * random.uniform(1.15, 1.6), 2)
                inicial = round(atualizado * random.uniform(0.8, 0.98), 2)
                linhas.append({
                    "ano": ano,
                    "setor_key": s[0],
                    "rubrica_key": r[0],
                    "valor_inicial": inicial,
                    "valor_atualizado": atualizado,
                })
    return linhas


# =================================================================
# ESCRITA DE CSV (modelo estrela limpo)
# =================================================================
def brl(v):
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gravar_csv(nome, cabecalho, linhas):
    DESTINO.mkdir(parents=True, exist_ok=True)
    with open(DESTINO / nome, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";", lineterminator="\r\n")
        w.writerow(cabecalho)
        w.writerows(linhas)


# =================================================================
# ESCRITA DE XLSX
# =================================================================
def estilo_cabecalho(ws, ncols):
    fill = PatternFill("solid", fgColor="12507F")
    for c in range(1, ncols + 1):
        cel = ws.cell(row=1, column=c)
        cel.font = Font(bold=True, color="FFFFFF")
        cel.fill = fill
        cel.alignment = Alignment(horizontal="center")


def escrever_aba(wb, nome, cabecalho, linhas):
    ws = wb.create_sheet(nome)
    ws.append(cabecalho)
    for ln in linhas:
        ws.append(ln)
    estilo_cabecalho(ws, len(cabecalho))
    for i, h in enumerate(cabecalho, start=1):
        ws.column_dimensions[get_column_letter(i)].width = max(12, min(28, len(h) + 4))
    ws.freeze_panes = "A2"
    return ws


def cel_data(d):
    return d  # openpyxl trata datetime nativamente


# =================================================================
# LIMPO
# =================================================================
def montar_limpo(setores, rubricas, modalidades, fontes, status,
                 fornecedores, contratos, calendario, empenhos, dotacao):
    wb = Workbook()
    wb.remove(wb.active)

    escrever_aba(wb, "dim_calendario",
                 ["data_key", "data", "ano", "mes", "nome_mes", "ano_mes",
                  "trimestre", "dia", "dia_semana", "nome_dia_semana"],
                 [[c["data_key"], c["data"], c["ano"], c["mes"], c["nome_mes"],
                   c["ano_mes"], c["trimestre"], c["dia"], c["dia_semana"],
                   c["nome_dia_semana"]] for c in calendario])

    escrever_aba(wb, "dim_setor", ["setor_key", "sigla", "setor"],
                 [[s[0], s[1], s[2]] for s in setores])

    escrever_aba(wb, "dim_rubrica", ["rubrica_key", "codigo", "rubrica", "grupo"],
                 [[r[0], r[1], r[2], r[3]] for r in rubricas])

    escrever_aba(wb, "dim_modalidade", ["modalidade_key", "modalidade"],
                 [[m[0], m[1]] for m in modalidades])

    escrever_aba(wb, "dim_fonte", ["fonte_key", "fonte"],
                 [[f[0], f[1]] for f in fontes])

    escrever_aba(wb, "dim_status_empenho", ["status_key", "status"],
                 [[s[0], s[1]] for s in status])

    escrever_aba(wb, "dim_fornecedor",
                 ["fornecedor_key", "razao_social", "cnpj", "porte", "municipio", "uf"],
                 [[f["fornecedor_key"], f["razao_social"], f["cnpj"], f["porte"],
                   f["municipio"], f["uf"]] for f in fornecedores])

    escrever_aba(wb, "dim_contrato",
                 ["contrato_key", "numero", "tipo", "objeto", "data_inicio", "data_fim",
                  "valor_contrato", "fornecedor_key", "setor_key", "licitacao_numero"],
                 [[c["contrato_key"], c["numero"], c["tipo"], c["objeto"], c["data_inicio"],
                   c["data_fim"], c["valor_contrato"], c["fornecedor_key"], c["setor_key"],
                   c["licitacao_numero"]] for c in contratos])

    escrever_aba(wb, "fato_empenhos",
                 ["id_empenho", "data_empenho_key", "contrato_key", "fornecedor_key",
                  "setor_key", "rubrica_key", "modalidade_key", "fonte_key", "status_key",
                  "valor_empenhado", "valor_liquidado", "valor_pago", "quantidade_itens"],
                 [[e["id_empenho"], e["data_empenho_key"], e["contrato_key"],
                   e["fornecedor_key"], e["setor_key"], e["rubrica_key"],
                   e["modalidade_key"], e["fonte_key"], e["status_key"],
                   e["valor_empenhado"], e["valor_liquidado"], e["valor_pago"],
                   e["quantidade_itens"]] for e in empenhos])

    escrever_aba(wb, "fato_dotacao",
                 ["ano", "setor_key", "rubrica_key", "valor_inicial", "valor_atualizado"],
                 [[d["ano"], d["setor_key"], d["rubrica_key"], d["valor_inicial"],
                   d["valor_atualizado"]] for d in dotacao])

    wb.save(DESTINO / "Orcamento_Contratos_LIMPO.xlsx")


# =================================================================
# SUJO (defeitos plantados de proposito)
# =================================================================
def _variantes_data(d, i):
    mod = i % 5
    if mod == 0:
        return d.strftime("%d/%m/%Y")
    if mod == 1:
        return d.isoformat()
    if mod == 2:
        return d.strftime("%d-%m-%Y")
    if mod == 3:
        return d.strftime("%d/%m/%y")
    return d.strftime("%m/%d/%Y")


def _variantes_moeda(v, i):
    """Valor como texto em formatos variados (ou numero puro)."""
    mod = i % 5
    if v < 0:
        return f"({brl(abs(v))})"
    if mod == 0:
        return f"R$ {brl(v)}"
    if mod == 1:
        return brl(v)
    if mod == 2:
        return f"R$ {v:.2f}"
    if mod == 3:
        return round(v, 2)
    return f" {brl(v)} "


def titulo(wb, nome, texto):
    wa = wb.create_sheet(nome)
    wa.append([texto])
    wa["A1"].font = Font(bold=True, size=12, color="12507F")
    return wa


def sujo_fornecedor(f):
    nome = f["razao_social"]
    i = f["fornecedor_key"]
    if i % 4 == 0:
        nome = f"  {nome} "          # espacos nas pontas (TRIM)
    if i % 5 == 0:
        nome = nome.lower()          # caixa inconsistente
    cnpj = f["cnpj"] if i % 3 else f["cnpj"].replace(".", "").replace("/", "").replace("-", "")
    return [f["fornecedor_key"], nome, cnpj, f["porte"], f["municipio"], f["uf"]]


def montar_sujo(setores, rubricas, modalidades, fontes, status,
                fornecedores, contratos, calendario, empenhos, dotacao):
    wb = Workbook()
    wb.remove(wb.active)
    stamp = "Relatorio extraido do sistema SIAFISICO em 12/01/2026 - uso interno"

    # ---- dim_calendario
    ws = titulo(wb, "dim_calendario", stamp)
    ws.append(["data_key", "data", "ano", "mes", "nome_mes", "ano_mes",
               "trimestre", "dia", "dia_semana", "nome_dia_semana"])
    for i, c in enumerate(calendario):
        d = c["data"]
        val = _variantes_data(d, i)
        if i % 7 == 0:
            val = f"{d.strftime('%d/%m/%Y')} 00:00:00"
        ws.append([c["data_key"], val, c["ano"], c["mes"], c["nome_mes"],
                   c["ano_mes"], c["trimestre"], c["dia"], c["dia_semana"],
                   c["nome_dia_semana"]])
        if i % 400 == 199:
            ws.append([])  # linha em branco

    # ---- dim_setor (variações de rotulo + duplicatas)
    ws = titulo(wb, "dim_setor", stamp)
    ws.append(["setor_key", "sigla", "setor"])
    variantes = {
        5: ["LAB. TOXICOLOGIA", "Laboratorio de Toxicologia",
            "LAB TOXICOLOGIA", " laboratorio de toxicologia "],
        8: ["Pericias de Informatica", "PERICIAS DE INFORMATICA"],
        3: ["Diretoria de Laboratorios Forenses", "DIR. DE LABORATORIOS FORENSES"],
    }
    for s in setores:
        if s[0] in variantes:
            for v in variantes[s[0]]:
                ws.append([s[0], s[1], v])
        else:
            nome = s[2]
            if s[0] % 2 == 0:
                nome = f"  {nome} "
            ws.append([s[0], s[1], nome])

    # ---- dim_rubrica (codigo + descricao juntos)
    ws = titulo(wb, "dim_rubrica", stamp)
    ws.append(["rubrica_key", "rubrica", "grupo"])
    for i, r in enumerate(rubricas):
        texto = f"{r[1]} - {r[2]}"
        if i % 3 == 0:
            texto = f" {texto} "
        ws.append([r[0], texto, r[3]])

    # ---- dim_modalidade
    ws = titulo(wb, "dim_modalidade", stamp)
    ws.append(["modalidade_key", "modalidade"])
    for i, m in enumerate(modalidades):
        txt = m[1]
        if i % 2 == 0:
            txt = txt.upper()
        ws.append([m[0], txt])
    ws.append([2, "PREGAO ELETRONICO"])  # duplicata

    # ---- dim_fonte
    ws = titulo(wb, "dim_fonte", stamp)
    ws.append(["fonte_key", "fonte"])
    for i, f in enumerate(fontes):
        txt = f[1] if i % 2 else f[1].upper()
        ws.append([f[0], txt])

    # ---- dim_status_empenho
    ws = titulo(wb, "dim_status_empenho", stamp)
    ws.append(["status_key", "status"])
    for i, s in enumerate(status):
        txt = s[1]
        if i % 2 == 0:
            txt = txt.upper()
        if i == 4:
            txt = "CANCELADO "
        ws.append([s[0], txt])

    # ---- dim_fornecedor
    ws = titulo(wb, "dim_fornecedor", stamp)
    ws.append(["fornecedor_key", "razao_social", "cnpj", "porte", "municipio", "uf"])
    for f in fornecedores:
        ws.append(sujo_fornecedor(f))
    ws.append([999, "Fornecedor a cadastrar", "0", "ME", "Cuiaba", "MT"])  # orfao
    ws.append(sujo_fornecedor(fornecedores[3]))  # duplicata

    # ---- dim_contrato
    ws = titulo(wb, "dim_contrato", stamp)
    ws.append(["contrato_key", "numero", "tipo", "objeto", "data_inicio", "data_fim",
               "valor_contrato", "fornecedor_key", "setor_key", "licitacao_numero"])
    for c in contratos:
        ws.append([c["contrato_key"], c["numero"], c["tipo"], c["objeto"],
                   _variantes_data(c["data_inicio"], c["contrato_key"]),
                   _variantes_data(c["data_fim"], c["contrato_key"] + 2),
                   _variantes_moeda(c["valor_contrato"], c["contrato_key"]),
                   c["fornecedor_key"], c["setor_key"], c["licitacao_numero"]])

    # ---- fato_empenhos
    ws = titulo(wb, "fato_empenhos", stamp)
    ws.append(["id_empenho", "data_empenho_key", "contrato_key", "fornecedor_key",
               "setor_key", "rubrica_key", "modalidade_key", "fonte_key", "status_key",
               "valor_empenhado", "valor_liquidado", "valor_pago", "quantidade_itens"])
    for i, e in enumerate(empenhos):
        ws.append([e["id_empenho"], _variantes_data(e["data_empenho"], i),
                   e["contrato_key"], e["fornecedor_key"], e["setor_key"],
                   e["rubrica_key"], e["modalidade_key"], e["fonte_key"], e["status_key"],
                   _variantes_moeda(e["valor_empenhado"], i),
                   _variantes_moeda(e["valor_liquidado"], i + 1),
                   _variantes_moeda(e["valor_pago"], i + 2),
                   e["quantidade_itens"]])
        if i in (100, 300, 500):
            ws.append([])  # linhas em branco
        if i in (150, 250, 350):
            ws.append([e["id_empenho"], e["data_empenho_key"].__str__(), e["contrato_key"],
                       e["fornecedor_key"], e["setor_key"], e["rubrica_key"],
                       e["modalidade_key"], e["fonte_key"], e["status_key"],
                       e["valor_empenhado"], e["valor_liquidado"], e["valor_pago"],
                       e["quantidade_itens"]])  # duplicata
    ws.append(["TOTAL GERAL", "", "", "", "", "", "", "", "",
               round(sum(e["valor_empenhado"] for e in empenhos), 2),
               round(sum(e["valor_liquidado"] for e in empenhos), 2),
               round(sum(e["valor_pago"] for e in empenhos), 2), ""])

    # ---- fato_dotacao
    ws = titulo(wb, "fato_dotacao", stamp)
    ws.append(["ano", "setor_key", "rubrica_key", "valor_inicial", "valor_atualizado"])
    for i, d in enumerate(dotacao):
        ws.append([str(d["ano"]),
                   d["setor_key"], d["rubrica_key"],
                   f"R$ {brl(d['valor_inicial'])}",
                   f"R$ {brl(d['valor_atualizado'])}"])

    wb.save(DESTINO / "Orcamento_Contratos_SUJO.xlsx")


# =================================================================
# README
# =================================================================
def escrever_readme(empenhos, dotacao, calendario, fornecedores, contratos):
    tot_emp = sum(e["valor_empenhado"] for e in empenhos)
    tot_liq = sum(e["valor_liquidado"] for e in empenhos)
    tot_pag = sum(e["valor_pago"] for e in empenhos)
    tot_atual = sum(d["valor_atualizado"] for d in dotacao)
    pct = tot_emp / tot_atual * 100 if tot_atual else 0

    texto = f"""# Datasets de Orcamento e Contratos (Aula 4)

Conjunto **sintetico** de execucao orcamentaria e contratos administrativos de um
orgao de pericia oficial (POLITEC/MT), preparado para a **Parte 0 do caderno do
Dia 4** (preparacao de Power BI Desktop). Modelo **estrela**: uma tabela fato de
empenhos cercada por dimensoes.

> Dados anonimizados, gerados por `../../gerar_datasets_orcamento.py` (semente
> fixa). Qualquer semelhanca com dados reais e coincidencia.

---

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `Orcamento_Contratos_LIMPO.xlsx` | **Gabarito do professor**: as 10 tabelas do modelo estrela, limpas e tipadas (1 aba por tabela). |
| `Orcamento_Contratos_SUJO.xlsx` | **Arquivo do aluno**: os mesmos dados com **defeitos plantados** de proposito, para treinar a limpeza no Power Query. |
| `fato_*.csv`, `dim_*.csv` | O modelo estrela limpo em CSV (UTF-8 com BOM, separador `;`), para conferencia rapida. |

---

## Modelo estrela

Grao da fato principal: **1 linha = 1 empenho**.

```
                    dim_calendario
                          |
   dim_contrato --- fato_empenhos --- dim_fornecedor
                          |  |
        dim_setor --- dim_rubrica --- dim_modalidade
                          |
                     dim_fonte --- dim_status_empenho
```

### Tabelas fato

| Tabela | Grao (1 linha =) | Linhas | Chaves estrangeiras | Medidas |
|---|---|---|---|---|
| `fato_empenhos` | 1 empenho (nota de empenho) | {len(empenhos)} | data_empenho_key, contrato_key, fornecedor_key, setor_key, rubrica_key, modalidade_key, fonte_key, status_key | valor_empenhado, valor_liquidado, valor_pago, quantidade_itens |
| `fato_dotacao` | 1 setor x rubrica x ano | {len(dotacao)} | setor_key, rubrica_key, ano | valor_inicial, valor_atualizado |

### Dimensoes

| Tabela | Linhas | Chave | Atributos |
|---|---|---|---|
| `dim_calendario` | {len(calendario)} | data_key (AAAAMMDD) | data, ano, mes, nome_mes, ano_mes, trimestre, dia, dia_semana, nome_dia_semana |
| `dim_setor` | {len(SETORES)} | setor_key | sigla, setor |
| `dim_rubrica` | {len(RUBRICAS)} | rubrica_key | codigo, rubrica, grupo |
| `dim_modalidade` | {len(MODALIDADES)} | modalidade_key | modalidade |
| `dim_fonte` | {len(FONTES)} | fonte_key | fonte |
| `dim_status_empenho` | {len(STATUS)} | status_key | status |
| `dim_fornecedor` | {len(fornecedores)} | fornecedor_key | razao_social, cnpj, porte, municipio, uf |
| `dim_contrato` | {len(contratos)} | contrato_key | numero, tipo, objeto, data_inicio, data_fim, valor_contrato, fornecedor_key, setor_key, licitacao_numero |

`dim_setor` e uma **dimensao conformada** (atende `fato_empenhos` e `fato_dotacao`);
`dim_calendario` liga a data do empenho (`data_empenho_key`) e o ano da dotacao.

### Relacionamentos (N:1, direcao unica)

```
fato_empenhos -> dim_calendario (data_empenho_key)
              -> dim_contrato, dim_fornecedor, dim_setor, dim_rubrica,
                 dim_modalidade, dim_fonte, dim_status_empenho
fato_dotacao  -> dim_setor, dim_rubrica
              -> dim_calendario (ano <-> ano)
```

---

## Numeros de referencia

| Indicador | Valor |
|---|---|
| Empenhado total | R$ {tot_emp:,.2f} |
| Liquidado total | R$ {tot_liq:,.2f} |
| Pago total | R$ {tot_pag:,.2f} |
| Dotacao atualizada | R$ {tot_atual:,.2f} |
| Execucao (empenhado / dotacao) | {pct:.1f}% |

---

## Defeitos plantados no arquivo SUJO

Todos aparecem no `Orcamento_Contratos_SUJO.xlsx`; o `_LIMPO` e o gabarito.

| # | Defeito | Onde aparece | Como corrigir |
|---|---|---|---|
| 1 | Linha de titulo antes do cabecalho | todas as abas (linha 1) | Power Query: *Usar Primeira Linha como Cabecalho* |
| 2 | Datas como texto, em 5 formatos | fato_empenhos, dim_contrato, dim_calendario | tipo **Data**, com **Localidade: Portugues (Brasil)** |
| 3 | Datas com hora `00:00:00` no fim | dim_calendario | *Dividir coluna* por espaco ou alterar tipo para Data |
| 4 | Valores como texto (`R$ 1.234,56`, `1.234,56`, `R$ 1234.56`) | fato_empenhos, dim_contrato, fato_dotacao | *Substituir Valores* (remover `R$` e espacos) + tipo **Decimal** com virgula |
| 5 | Negativos entre parenteses `(1.500,00)` | fato_empenhos | *Substituir* `(` por `-` e remover `)` |
| 6 | Categorias com variacao de caixa e espacos | dim_setor (5 fica com 4 rotulos), dim_modalidade, dim_fonte, dim_status_empenho | *Formatar > Colunas de Texto*: **Cortar (Trim)** + **Caixa da Palavra (Capitalizar)**; depois *Remover Duplicatas* |
| 7 | Coluna `codigo` + `rubrica` juntos | dim_rubrica (`339014 - Diarias`) | *Dividir Coluna* por delimitador ` - ` |
| 8 | CNPJ com e sem pontuacao | dim_fornecedor | padronizar com *Substituir* ou manter so digitos |
| 9 | Espacos antes/depois do texto | dim_setor, dim_fornecedor, dim_rubrica | *Cortar (Trim)* |
| 10 | Linhas em branco no meio | fato_empenhos, dim_calendario | *Remover Linhas Vazias* |
| 11 | Linha `TOTAL GERAL` no fim | fato_empenhos | *Remover Linhas Filtradas* (filtrar `id_empenho` diferente de TOTAL GERAL) |
| 12 | Linhas duplicadas | fato_empenhos, dim_fornecedor | *Remover Duplicatas* |
| 13 | Chaves como texto | todas | alterar tipo para **Numero Inteiro** |
| 14 | Membro de dimensao orfao (key 999) | dim_fornecedor | filtrar/remover apos conferir |

---

## Como usar (Power Query)

1. Abra o Power BI Desktop -> **Obter Dados** -> **Pasta de Trabalho do Excel**.
2. Aponte para `Orcamento_Contratos_SUJO.xlsx` e marque as abas desejadas.
3. **Transformar Dados** e aplicar os ajustes da tabela de defeitos acima.
4. **Fechar e Aplicar**, criar os relacionamentos (N:1) e montar as 3 abas do painel.

O passo a passo detalhado esta na **Parte 0 do caderno do Dia 4**
(`../caderno-dia4.html`).

---

## Convencoes

- CSV UTF-8 com BOM, separador `;`, datas ISO `AAAA-MM-DD`.
- `data_key` inteiro no formato `AAAAMMDD`.
- Valores monetarios com virgula decimal no padrao pt-BR.
"""
    (DESTINO / "README.md").write_text(texto, encoding="utf-8")


# =================================================================
# MAIN
# =================================================================
def main():
    fornecedores = gerar_fornecedores(40)
    contratos = gerar_contratos(fornecedores, 60)
    calendario = gerar_calendario()
    empenhos = gerar_empenhos(fornecedores, contratos, 620)
    dotacao = gerar_dotacao(empenhos)

    # ---- CSVs do modelo estrela limpo
    gravar_csv("dim_calendario.csv",
               ["data_key", "data", "ano", "mes", "nome_mes", "ano_mes", "trimestre",
                "dia", "dia_semana", "nome_dia_semana"],
               [[c["data_key"], c["data"].isoformat(), c["ano"], c["mes"], c["nome_mes"],
                 c["ano_mes"], c["trimestre"], c["dia"], c["dia_semana"],
                 c["nome_dia_semana"]] for c in calendario])
    gravar_csv("dim_setor.csv", ["setor_key", "sigla", "setor"],
               [[s[0], s[1], s[2]] for s in SETORES])
    gravar_csv("dim_rubrica.csv", ["rubrica_key", "codigo", "rubrica", "grupo"],
               [[r[0], r[1], r[2], r[3]] for r in RUBRICAS])
    gravar_csv("dim_modalidade.csv", ["modalidade_key", "modalidade"],
               [[m[0], m[1]] for m in MODALIDADES])
    gravar_csv("dim_fonte.csv", ["fonte_key", "fonte"],
               [[f[0], f[1]] for f in FONTES])
    gravar_csv("dim_status_empenho.csv", ["status_key", "status"],
               [[s[0], s[1]] for s in STATUS])
    gravar_csv("dim_fornecedor.csv",
               ["fornecedor_key", "razao_social", "cnpj", "porte", "municipio", "uf"],
               [[f["fornecedor_key"], f["razao_social"], f["cnpj"], f["porte"],
                 f["municipio"], f["uf"]] for f in fornecedores])
    gravar_csv("dim_contrato.csv",
               ["contrato_key", "numero", "tipo", "objeto", "data_inicio", "data_fim",
                "valor_contrato", "fornecedor_key", "setor_key", "licitacao_numero"],
               [[c["contrato_key"], c["numero"], c["tipo"], c["objeto"],
                 c["data_inicio"].isoformat(), c["data_fim"].isoformat(),
                 f"{c['valor_contrato']:.2f}", c["fornecedor_key"], c["setor_key"],
                 c["licitacao_numero"]] for c in contratos])
    gravar_csv("fato_empenhos.csv",
               ["id_empenho", "data_empenho_key", "contrato_key", "fornecedor_key",
                "setor_key", "rubrica_key", "modalidade_key", "fonte_key", "status_key",
                "valor_empenhado", "valor_liquidado", "valor_pago", "quantidade_itens"],
               [[e["id_empenho"], e["data_empenho_key"], e["contrato_key"],
                 e["fornecedor_key"], e["setor_key"], e["rubrica_key"],
                 e["modalidade_key"], e["fonte_key"], e["status_key"],
                 f"{e['valor_empenhado']:.2f}", f"{e['valor_liquidado']:.2f}",
                 f"{e['valor_pago']:.2f}", e["quantidade_itens"]] for e in empenhos])
    gravar_csv("fato_dotacao.csv",
               ["ano", "setor_key", "rubrica_key", "valor_inicial", "valor_atualizado"],
               [[d["ano"], d["setor_key"], d["rubrica_key"],
                 f"{d['valor_inicial']:.2f}", f"{d['valor_atualizado']:.2f}"] for d in dotacao])

    # ---- XLSX
    montar_limpo(SETORES, RUBRICAS, MODALIDADES, FONTES, STATUS,
                 fornecedores, contratos, calendario, empenhos, dotacao)
    montar_sujo(SETORES, RUBRICAS, MODALIDADES, FONTES, STATUS,
                fornecedores, contratos, calendario, empenhos, dotacao)

    # ---- README
    escrever_readme(empenhos, dotacao, calendario, fornecedores, contratos)

    # ---- Estatisticas para referencia
    tot_emp = sum(e["valor_empenhado"] for e in empenhos)
    tot_liq = sum(e["valor_liquidado"] for e in empenhos)
    tot_pag = sum(e["valor_pago"] for e in empenhos)
    tot_atual = sum(d["valor_atualizado"] for d in dotacao)
    pct_exec = tot_emp / tot_atual * 100 if tot_atual else 0
    print("Datasets de Orcamento e Contratos gerados em:", DESTINO.relative_to(RAIZ))
    print(f"  fato_empenhos: {len(empenhos)} linhas")
    print(f"  fato_dotacao:  {len(dotacao)} linhas")
    print(f"  dim_calendario:{len(calendario)} linhas; dim_fornecedor {len(fornecedores)}; "
          f"dim_contrato {len(contratos)}")
    print(f"  Empenhado: R$ {tot_emp:,.2f}  ({pct_exec:.1f}% da dotacao atualizada)")
    print(f"  Liquidado: R$ {tot_liq:,.2f} | Pago: R$ {tot_pag:,.2f}")
    print(f"  Dotacao atualizada: R$ {tot_atual:,.2f}")


if __name__ == "__main__":
    main()
