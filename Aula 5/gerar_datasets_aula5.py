# -*- coding: utf-8 -*-
"""Gerador dos 5 datasets da Aula 5 (Dashboards de BI pericial).

Cada cenario vira uma pasta em ``datasets/cenarioN_*/`` com o seu modelo
estrela (uma tabela fato cercada pelas suas dimensoes + dim_calendario).

Cenarios (todos com >=1000 linhas na tabela fato):

  1. cenario1_backlog        -> fato_requisicoes (~1200)        - Backlog de pericias
  2. cenario2_dna            -> fato_exames_dna (~1100)         - TAT do laboratorio de DNA
  3. cenario3_criminalidade  -> fato_ocorrencias (~1500)        - Mapa da criminalidade em MT
  4. cenario4_orcamento      -> fato_empenhos (~1300)+dotacao   - Orcamento e contratos
  5. cenario5_custodia       -> fato_mov_evidencia (~1300)      - Cadeia de custodia

Convencoes:
- CSV UTF-8 com BOM, separador ';', datas ISO (AAAA-MM-DD).
- Chaves substitutas inteiras (1..N) atribuidas por ordem alfabetica.
- dim_calendario de 2023-01-01 a 2025-12-31 (1096 dias).

Uso:  python gerar_datasets_aula5.py
"""
import csv
import datetime as dt
import pathlib
import random

RAIZ = pathlib.Path(__file__).resolve().parent
DATASETS = RAIZ / "datasets"
SEED = 20260120
random.seed(SEED)

INICIO = dt.date(2023, 1, 1)
FIM = dt.date(2025, 12, 31)
DIAS = (FIM - INICIO).days + 1   # 1096
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


def dim_alfabetica(valores, com_label=None):
    """Retorna (mapa valor->chave, linhas_fato).

    Cada linha de `linhas_fato` e [chave, valor]. `com_label` informa um rotulo
    extra para o cabecalho (opcional).
    """
    ordenados = sorted(set(valores))
    mapa = {v: i + 1 for i, v in enumerate(ordenados)}
    linhas = [[mapa[v], v] for v in ordenados]
    return mapa, linhas


def gerar_calendario(inicio=INICIO, fim=FIM):
    """Gera dim_calendario entre [inicio, fim]."""
    linhas = []
    d = inicio
    while d <= fim:
        linhas.append([
            d.year * 10000 + d.month * 100 + d.day,
            d.isoformat(),
            d.year,
            d.month,
            NOMES_MES[d.month],
            f"{d.year:04d}-{d.month:02d}",
            (d.month - 1) // 3 + 1,
            d.day,
            d.isoweekday(),
            NOMES_SEM[d.isoweekday()],
        ])
        d += dt.timedelta(days=1)
    return linhas


def gravar_calendario(pasta):
    linhas = gerar_calendario()
    csv_gravar(pasta, "dim_calendario.csv",
               ["data_key", "data", "ano", "mes", "nome_mes", "ano_mes",
                "trimestre", "dia", "dia_semana", "nome_dia_semana"], linhas)


def dias_uteis(d_ini, d_fim):
    """Conta dias uteis (seg-sex) entre [d_ini, d_fim]."""
    if not (d_ini and d_fim) or d_fim < d_ini:
        return 0
    n, d = 0, d_ini
    while d <= d_fim:
        if d.isoweekday() <= 5:
            n += 1
        d += dt.timedelta(days=1)
    return n


def data_aleatoria(inicio=INICIO, fim=FIM):
    delta = (fim - inicio).days
    return inicio + dt.timedelta(days=random.randint(0, delta))


def data_pos(data_base, dias_min, dias_max):
    return data_base + dt.timedelta(days=random.randint(dias_min, dias_max))


def chave(v):
    """Chave inteira 1..N para um valor (substituta)."""
    return v


def pct(p):
    """Bernoulli com probabilidade p (True/False)."""
    return random.random() < p


# =================================================================
# CATALOGOS COMPARTILHADOS
# =================================================================
# Para manter consistencia entre os cenarios que referenciam setor, usamos
# o mesmo catalogo de setores (8) e municipios MT (18). Os IDs sao
# atribuidos em cada cenario de acordo com a ordem alfabetica no escopo
# daquela pasta.

SETORES_TXT = [
    "ADM - Diretoria de Administracao",
    "BAL - Laboratorio de Balistica",
    "DNA - Coordenadoria de DNA",
    "IDT - Diretoria de Identificacao",
    "IML - Instituto Medico Legal",
    "INF - Pericias de Informatica",
    "TOX - Laboratorio de Toxicologia",
    "TRA - Pericias de Transito",
]

MUNICIPIOS_MT = [
    "Alta Floresta", "Barra do Garcas", "Caceres", "Campo Verde",
    "Cuiaba", "Diamantino", "Juina", "Lucas do Rio Verde",
    "Pontes Lacerda", "Primavera do Leste", "Rondonopolis",
    "Sapezal", "Sinop", "Sorriso", "Tangara da Serra",
    "Varzea Grande",
]


# =================================================================
# CENARIO 1 - BACKLOG DE PERICIAS
# =================================================================
def cenario1_backlog(pasta):
    # ---------- Dimensoes
    setores_map, setores_rows = dim_alfabetica(SETORES_TXT)
    csv_gravar(pasta, "dim_setor.csv", ["setor_key", "setor"], setores_rows)

    peritos = []
    nomes_p = ["Ana Beatriz", "Carlos Magno", "Daniel Augusto", "Eduardo Lima",
               "Fernanda Costa", "Gabriel Souza", "Helena Machado", "Igor Almeida",
               "Joana Vidal", "Karina Prado", "Lucas Miranda", "Marcos Reis"]
    for i, nome in enumerate(sorted(nomes_p), start=1):
        setor = sorted(SETORES_TXT)[i % len(SETORES_TXT)]
        esp = setor.split(" - ", 1)[1]
        peritos.append((i, nome, esp, setores_map[setor]))
    csv_gravar(pasta, "dim_perito.csv",
               ["perito_key", "perito", "especialidade", "setor_key"], peritos)

    tipos_exame = ["Acidente de Transito", "Balistica", "DNA", "Documentoscopia",
                   "Informatica Forense", "Necropsia", "Quimica Forense", "Toxicologia"]
    tipos_map, tipos_rows = dim_alfabetica(tipos_exame)
    csv_gravar(pasta, "dim_tipo_exame.csv", ["tipo_exame_key", "tipo_exame"], tipos_rows)

    delegs = [(i + 1, m, "MT") for i, m in enumerate(sorted(MUNICIPIOS_MT))]
    csv_gravar(pasta, "dim_delegacia.csv",
               ["delegacia_key", "delegacia", "uf"], delegs)

    prioridades = ["Alta", "Media", "Baixa"]
    prior_map, prior_rows = dim_alfabetica(prioridades)
    csv_gravar(pasta, "dim_prioridade.csv", ["prioridade_key", "prioridade"], prior_rows)

    status = ["Aguardando Triagem", "Em Analise", "Em Revisao", "Concluido", "Arquivado"]
    status_map, status_rows = dim_alfabetica(status)
    csv_gravar(pasta, "dim_status.csv", ["status_key", "status"], status_rows)

    gravar_calendario(pasta)

    # ---------- Fato (1200 linhas)
    fato = []
    prazos_por_exame = {
        "Acidente de Transito": 30, "Balistica": 45, "DNA": 90, "Documentoscopia": 30,
        "Informatica Forense": 60, "Necropsia": 15, "Quimica Forense": 60, "Toxicologia": 45,
    }
    for n_req in range(1, 1201):
        data_entrada = data_aleatoria()
        tipo = random.choice(tipos_exame)
        prazo = prazos_por_exame[tipo]
        # 80% concluidos
        if pct(0.80):
            data_conc = data_pos(data_entrada, int(prazo * 0.3), int(prazo * 1.6))
            if data_conc > FIM:
                data_conc = FIM
            du = dias_uteis(data_entrada, data_conc)
            status = random.choices(
                ["Concluido", "Em Revisao", "Arquivado"], weights=[78, 14, 8])[0]
        else:
            data_conc = ""
            du = ""
            status = random.choices(
                ["Aguardando Triagem", "Em Analise", "Em Revisao"],
                weights=[20, 55, 25])[0]
        em_atraso = 1 if (du != "" and du > prazo) else 0
        perito_idx = random.randint(0, len(nomes_p) - 1)
        perito = sorted(nomes_p)[perito_idx]
        setor = sorted(SETORES_TXT)[perito_idx % len(SETORES_TXT)]
        fato.append([
            f"REQ-{data_entrada.year}-{n_req:05d}",
            data_key(data_entrada),
            data_key(data_conc) if data_conc else "",
            setores_map[setor],
            tipos_map[tipo],
            peritos[perito_idx][0],
            random.randint(1, len(MUNICIPIOS_MT)),
            prior_map[random.choices(prioridades, weights=[20, 50, 30])[0]],
            status_map[status],
            du,
            prazo,
            em_atraso,
            random.randint(500, 250000) if pct(0.7) else "",
        ])
    csv_gravar(pasta, "fato_requisicoes.csv",
               ["id_requisicao", "data_entrada_key", "data_conclusao_key",
                "setor_key", "tipo_exame_key", "perito_key", "delegacia_key",
                "prioridade_key", "status_key", "dias_uteis", "prazo_legal",
                "em_atraso", "valor_causa"], fato)


# =================================================================
# CENARIO 2 - TAT DO LABORATORIO DE DNA
# =================================================================
def cenario2_dna(pasta):
    # ---------- Dimensoes
    labs = ["Lab. DNA Cuiaba Central", "Lab. DNA Rondonopolis",
            "Lab. DNA Sinop", "Lab. DNA Varzea Grande"]
    labs_map, labs_rows = dim_alfabetica(labs)
    csv_gravar(pasta, "dim_laboratorio.csv", ["laboratorio_key", "laboratorio"], labs_rows)

    metod = ["mtDNA", "NGS - Painel Expandido", "SNPs Autossomicos",
             "STR Autossomico - 15 loci", "Y-STR"]
    met_map, met_rows = dim_alfabetica(metod)
    csv_gravar(pasta, "dim_metodologia.csv", ["metodologia_key", "metodologia"], met_rows)

    analistas = []
    for i, nome in enumerate(sorted([
        "Aline Peixoto", "Bruno Tavares", "Camila Vargas", "Diego Nogueira",
        "Erika Sales", "Felipe Andrade", "Gisele Rocha", "Henrique Bessa",
        "Isabela Coutinho", "Joao Pedro Lira", "Karla Diniz", "Luiz Fernando",
        "Marina Tavares", "Nelson Goes",
    ]), start=1):
        analistas.append([i, nome, random.choice(labs)])
    csv_gravar(pasta, "dim_analista.csv",
               ["analista_key", "analista", "laboratorio"], analistas)

    status = ["Aguardando Coleta", "Em Extracao", "Em Amplificacao",
              "Em Analise", "Concluido", "Amostra Insuficiente"]
    status_map, status_rows = dim_alfabetica(status)
    csv_gravar(pasta, "dim_status_exame.csv",
               ["status_exame_key", "status_exame"], status_rows)

    kits = []
    nomes_kit = [
        ("GlobalFiler", "Thermo Fisher", "L051823"),
        ("PowerPlex 16", "Promega", "P091024"),
        ("AmpFLSTR Identifiler", "Thermo Fisher", "I112526"),
        ("Yfiler Plus", "Thermo Fisher", "Y020525"),
        ("Quantifiler Trio", "Thermo Fisher", "Q030624"),
        ("PowerQuant", "Promega", "PQ041223"),
        ("ForenSeq DNA Signature", "Verogen", "FS051024"),
        ("Plexor HY", "Promega", "PH060725"),
        ("mtDNA Control Region", "Roche", "M071024"),
        ("NextSeq Reagent Mid", "Illumina", "NS082125"),
        ("Ion AmpliSeq", "Thermo Fisher", "IA091224"),
        ("QIAamp DNA Mini", "Qiagen", "QA101224"),
    ]
    for i, (nome, marca, lote) in enumerate(nomes_kit, start=1):
        kits.append([i, nome, marca, lote])
    csv_gravar(pasta, "dim_kit_reagente.csv",
               ["kit_key", "kit", "marca", "lote"], kits)

    gravar_calendario(pasta)

    # ---------- Fato (1100 exames)
    fato = []
    tat_meta = 90
    for n in range(1, 1101):
        data_receb = data_aleatoria()
        # 88% concluidos, 12% ainda em curso ou com problema
        if pct(0.88):
            tat = random.choice([
                random.randint(15, tat_meta - 10),
                random.randint(tat_meta - 5, tat_meta + 15),
                random.randint(tat_meta + 16, tat_meta + 70),
            ])
            data_conc = data_receb + dt.timedelta(days=tat)
            if data_conc > FIM:
                data_conc = FIM
            st = "Concluido"
        else:
            data_conc = ""
            tat = ""
            st = random.choice(["Aguardando Coleta", "Em Extracao",
                                "Em Amplificacao", "Em Analise", "Amostra Insuficiente"])
        amostra = random.choices(
            ["Alta", "Media", "Baixa"], weights=[55, 30, 15])[0]
        qtd = random.choices([1, 2, 3, 4], weights=[50, 30, 15, 5])[0]
        fato.append([
            f"DNA-{data_receb.year}-{n:05d}",
            data_key(data_receb),
            data_key(data_conc) if data_conc else "",
            labs_map[random.choice(labs)],
            met_map[random.choice(metod)],
            analistas[random.randint(0, 13)][0],
            status_map[st],
            random.randint(1, 12),
            qtd,
            amostra,
            tat,
        ])
    csv_gravar(pasta, "fato_exames_dna.csv",
               ["id_exame", "data_recebimento_key", "data_conclusao_key",
                "laboratorio_key", "metodologia_key", "analista_key",
                "status_exame_key", "kit_key", "qtd_amostras",
                "qualidade_amostra", "tat_dias"], fato)


# =================================================================
# CENARIO 3 - MAPA DA CRIMINALIDADE EM MT
# =================================================================
def cenario3_criminalidade(pasta):
    # ---------- Dimensoes
    municipios = sorted(MUNICIPIOS_MT + ["Mirassol d'Oeste", "Sao Jose do Rio Claro"])
    mun_map, mun_rows = dim_alfabetica(municipios)
    csv_gravar(pasta, "dim_municipio.csv",
               ["municipio_key", "municipio", "uf"], [[k, m, "MT"] for k, m in mun_rows])

    tipos = ["Estupro", "Homicidio Doloso", "Lesao Corporal", "Porte Ilegal de Arma",
             "Roubo", "Roubo de Veiculo", "Trafico de Drogas"]
    tipo_map, tipo_rows = dim_alfabetica(tipos)
    csv_gravar(pasta, "dim_tipo_crime.csv",
               ["tipo_crime_key", "tipo_crime"], tipo_rows)

    armas = ["Arma Branca (faca)", "Arma de Fogo", "Arma de Fogo Artesanal",
            "Nao Utilizada", "Outros", "Veiculo"]
    arma_map, arma_rows = dim_alfabetica(armas)
    csv_gravar(pasta, "dim_arma.csv", ["arma_key", "arma"], arma_rows)

    faixas = ["0-11 anos", "12-17 anos", "18-24 anos", "25-39 anos",
              "40-59 anos", "60+ anos"]
    fx_map, fx_rows = dim_alfabetica(faixas)
    csv_gravar(pasta, "dim_faixa_etaria.csv",
               ["faixa_etaria_key", "faixa_etaria"], fx_rows)

    periodos = ["Madrugada (00h-05h)", "Manha (06h-11h)",
                "Tarde (12h-17h)", "Noite (18h-23h)"]
    per_map, per_rows = dim_alfabetica(periodos)
    csv_gravar(pasta, "dim_periodo_dia.csv",
               ["periodo_dia_key", "periodo_dia"], per_rows)

    gravar_calendario(pasta)

    # ---------- Fato (1500 ocorrencias)
    fato = []
    pesos_mun = {  # municipios MT mais populosos = mais ocorrencias
        "Cuiaba": 22, "Varzea Grande": 14, "Rondonopolis": 12,
        "Sinop": 8, "Tangara da Serra": 7, "Sorriso": 6,
        "Primavera do Leste": 5, "Lucas do Rio Verde": 5,
        "Caceres": 5, "Barra do Garcas": 4, "Alta Floresta": 4,
        "Campo Verde": 3, "Diamantino": 3, "Juina": 3,
        "Pontes Lacerda": 3, "Sapezal": 2,
        "Mirassol d'Oeste": 2, "Sao Jose do Rio Claro": 2,
    }
    mun_pesos = [pesos_mun[m] for m in municipios]
    tipo_pesos = [12, 14, 22, 8, 24, 12, 8]  # Roubo lidera, Lesao/Leve vem depois
    arma_pesos = [14, 38, 4, 28, 8, 8]
    fx_pesos = [3, 8, 22, 30, 22, 15]
    per_pesos = [22, 18, 26, 34]

    for n in range(1, 1501):
        d = data_aleatoria()
        mun = random.choices(municipios, weights=mun_pesos)[0]
        fato.append([
            f"OC-{d.year}-{n:05d}",
            data_key(d),
            mun_map[mun],
            tipo_map[random.choices(tipos, weights=tipo_pesos)[0]],
            arma_map[random.choices(armas, weights=arma_pesos)[0]],
            fx_map[random.choices(faixas, weights=fx_pesos)[0]],
            per_map[random.choices(periodos, weights=per_pesos)[0]],
            random.choices([1, 2, 3, 4], weights=[85, 12, 2, 1])[0],
            random.choices([1, 2, 3], weights=[80, 16, 4])[0],
            1 if pct(0.07) else 0,
            1 if pct(0.18) else 0,
        ])
    csv_gravar(pasta, "fato_ocorrencias.csv",
               ["id_ocorrencia", "data_key", "municipio_key",
                "tipo_crime_key", "arma_key", "faixa_etaria_key",
                "periodo_dia_key", "qtd_vitimas", "qtd_autos",
                "flag_latrocinio", "flag_flagrante"], fato)


# =================================================================
# CENARIO 4 - ORCAMENTO E CONTRATOS
# =================================================================
def cenario4_orcamento(pasta):
    # ---------- Dimensoes
    setores_map, setores_rows = dim_alfabetica(SETORES_TXT)
    csv_gravar(pasta, "dim_setor.csv", ["setor_key", "setor"], setores_rows)

    rubricas = [
        ("339014", "Diarias"), ("339030", "Material de Consumo"),
        ("339033", "Passagens e Locomocao"), ("339035", "Servicos de Consultoria"),
        ("339036", "Outros Servicos de Terceiros - PF"),
        ("339039", "Outros Servicos de Terceiros - PJ"),
        ("339047", "Obrigacoes Tributarias"),
        ("449051", "Obras e Instalacoes"),
        ("449052", "Equipamentos e Material Permanente"),
        ("449061", "Aquisicao de Imoveis"),
    ]
    rubricas.sort(key=lambda x: x[0])
    rub_rows = [[i + 1, c, n, "Custeio" if c.startswith("339") else "Investimento"]
                for i, (c, n) in enumerate(rubricas)]
    rub_map = {r[1]: r[0] for r in rub_rows}
    csv_gravar(pasta, "dim_rubrica.csv",
               ["rubrica_key", "codigo", "rubrica", "grupo"], rub_rows)

    mods = ["Adesao a Ata de RP", "Concorrencia", "Dispensa de Licitacao",
            "Inexigibilidade", "Pregao Eletronico", "Pregao Presencial"]
    mod_map, mod_rows = dim_alfabetica(mods)
    csv_gravar(pasta, "dim_modalidade.csv",
               ["modalidade_key", "modalidade"], mod_rows)

    fontes = ["Convenio Federal", "Emenda Parlamentar",
              "Fundo Especial", "Recurso Proprio", "Tesouro Estadual"]
    fonte_map, fonte_rows = dim_alfabetica(fontes)
    csv_gravar(pasta, "dim_fonte.csv",
               ["fonte_key", "fonte"], fonte_rows)

    statuses = ["Cancelado", "Em Liquidacao", "Empenhado", "Liquidado", "Pago"]
    st_map, st_rows = dim_alfabetica(statuses)
    csv_gravar(pasta, "dim_status_empenho.csv",
               ["status_empenho_key", "status_empenho"], st_rows)

    # 50 fornecedores
    pref = ["ALFA", "BIOGEN", "CIENTIFICA", "DELTA", "EXATA", "FORENSE",
            "GENESYS", "HEXA", "INOVA", "JUPITER", "LABOR", "MEDLAB",
            "NORDIC", "ORION", "PRISMA", "QUANTA", "RADIAL", "SOLAR",
            "TECNO", "UNIAO", "VECTOR", "WEST", "XENON", "ZENITH"]
    sufx = ["SUPRIMENTOS LTDA", "LABORATORIOS LTDA", "COMERCIO E SERVICOS EIRELI",
            "TECNOLOGIA LTDA", "DIAGNOSTICOS LTDA", "ENGENHARIA LTDA",
            "DISTRIBUIDORA LTDA", "MANUTENCAO LTDA", "COMERCIO EIRELI",
            "LOCACOES LTDA"]
    portes = ["ME", "EPP", "Medio", "Grande"]
    forn = []
    idx = 1
    while idx <= 50:
        r = random.choice(pref) + " " + random.choice(sufx)
        if any(f[1] == r for f in forn):
            continue
        forn.append([idx, r, f"{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}/0001-{random.randint(10,99):02d}",
                     random.choice(portes), random.choice(sorted(MUNICIPIOS_MT)), "MT"])
        idx += 1
    csv_gravar(pasta, "dim_fornecedor.csv",
               ["fornecedor_key", "razao_social", "cnpj", "porte", "municipio", "uf"],
               forn)

    # 80 contratos
    tipos_contrato = ["Aquisicao", "Fornecimento", "Locacao", "Prestacao de Servicos"]
    objetos = [
        "Reagentes analiticos", "Kits de coleta de DNA", "Equipamentos de protecao",
        "Veiculos sem motorista", "Manutencao predial", "Servicos de TI",
        "Material de escritorio", "Vigilancia patrimonial",
        "Equipamentos laboratoriais", "Armamento e municao", "Impressao corporativa",
        "Limpeza e conservacao", "Cafe e generos alimenticios",
    ]
    contratos = []
    for i in range(1, 81):
        forn_k = random.randint(1, 50)
        setor_k = random.randint(1, len(SETORES_TXT))
        di = data_aleatoria()
        dur = random.randint(120, 720)
        df = di + dt.timedelta(days=dur)
        contratos.append([
            i, f"CTR-{di.year}-{i:04d}", random.choice(tipos_contrato),
            random.choice(objetos), di.isoformat(), df.isoformat(),
            random.randint(8000, 2500000), forn_k, setor_k,
            f"PE {di.year}/{random.randint(1, 99):02d}",
        ])
    csv_gravar(pasta, "dim_contrato.csv",
               ["contrato_key", "numero", "tipo", "objeto",
                "data_inicio", "data_fim", "valor_contrato",
                "fornecedor_key", "setor_key", "licitacao_numero"],
               contratos)

    gravar_calendario(pasta)

    # ---------- Fato (1300 empenhos)
    fato = []
    for n in range(1, 1301):
        d = data_aleatoria()
        valor_emp = round(random.uniform(800, 250000), 2)
        # 8% cancelado, 12% em liquidacao, 30% empenhado, 30% liquidado, 20% pago
        s = random.choices(statuses, weights=[8, 12, 30, 30, 20])[0]
        if s == "Cancelado":
            valor_liq = valor_pag = 0.0
        elif s == "Empenhado":
            valor_liq = 0.0
            valor_pag = 0.0
        elif s == "Em Liquidacao":
            valor_liq = round(valor_emp * random.uniform(0.2, 0.7), 2)
            valor_pag = 0.0
        elif s == "Liquidado":
            valor_liq = valor_emp
            valor_pag = 0.0
        else:  # Pago
            valor_liq = valor_emp
            valor_pag = valor_emp
        cod_rub = random.choice([r[0] for r in rubricas])
        fato.append([
            f"EMP-{d.year}-{n:05d}",
            data_key(d),
            random.randint(1, 80),
            random.randint(1, 50),
            random.randint(1, len(SETORES_TXT)),
            rub_map[cod_rub],
            random.randint(1, len(mods)),
            random.randint(1, len(fontes)),
            st_map[s],
            valor_emp, valor_liq, valor_pag,
            random.randint(1, 200),
        ])
    csv_gravar(pasta, "fato_empenhos.csv",
               ["id_empenho", "data_empenho_key", "contrato_key", "fornecedor_key",
                "setor_key", "rubrica_key", "modalidade_key", "fonte_key",
                "status_empenho_key", "valor_empenhado", "valor_liquidado",
                "valor_pago", "qtd_itens"], fato)

    # dotacao anual por (setor, rubrica) nos 3 anos
    fato_dot = []
    for ano in (2023, 2024, 2025):
        for setor_k in range(1, len(SETORES_TXT) + 1):
            for cod_rub in [r[0] for r in rubricas]:
                v_ini = round(random.uniform(50000, 2000000), 2)
                v_atu = round(v_ini * random.uniform(0.85, 1.45), 2)
                fato_dot.append([
                    setor_k, rub_map[cod_rub], ano, v_ini, v_atu,
                ])
    csv_gravar(pasta, "fato_dotacao.csv",
               ["setor_key", "rubrica_key", "ano",
                "valor_inicial", "valor_atualizado"], fato_dot)


# =================================================================
# CENARIO 5 - CADEIA DE CUSTODIA DE EVIDENCIAS
# =================================================================
def cenario5_custodia(pasta):
    # ---------- Dimensoes
    tipos = ["Arma de Fogo", "Documento", "Digitais (papiloscopia)",
             "Material Biologico - DNA", "Municao", "Smartphone/Eletronico",
             "Substancia - Droga", "Veiculo Apreendido", "Vestigio (papel/tecido)",
             "Outros"]
    tipo_map, tipo_rows = dim_alfabetica(tipos)
    csv_gravar(pasta, "dim_tipo_evidencia.csv",
               ["tipo_evidencia_key", "tipo_evidencia"], tipo_rows)

    origens = ["Busca Domiciliar", "Delegacia", "Flagrante",
               "IML", "Operacao de Campo", "Outro Orgao",
               "Pericia Anterior (encaminhamento)", "Voluntaria"]
    orig_map, orig_rows = dim_alfabetica(origens)
    csv_gravar(pasta, "dim_origem.csv",
               ["origem_key", "origem"], orig_rows)

    destinos = ["Arquivo Morto", "Cofre de Evidencias Informatica",
                "Cofre IML", "Destruicao", "Lab. Balistica",
                "Lab. DNA", "Lab. Toxicologia", "Sala de Evidencias"]
    dest_map, dest_rows = dim_alfabetica(destinos)
    csv_gravar(pasta, "dim_destino.csv",
               ["destino_key", "destino"], dest_rows)

    status = ["Coletada", "Concluida (custodia encerrada)", "Em Transporte",
              "Lacrada", "Recebida pelo destino"]
    st_map, st_rows = dim_alfabetica(status)
    csv_gravar(pasta, "dim_status_custodia.csv",
               ["status_custodia_key", "status_custodia"], st_rows)

    responsaveis = []
    nomes_r = sorted([
        "Agente 1o Ten. Pereira", "Agente Cabo Souza", "Agente Cabo Martins",
        "Delegado Dr. Almeida", "Delegado Dr. Belo", "Perita Dra. Holanda",
        "Perita Dra. Lemos", "Perito Dr. Khouri", "Perito Dr. Meirelles",
        "Perito Dr. Nogueira", "Perito Dr. Tanaka", "Perito Dr. Werneck",
        "Escrevente Hilda", "Escrevente Ronaldo", "Escrevente Silvia",
    ])
    for i, n in enumerate(nomes_r, start=1):
        responsaveis.append([i, n])
    csv_gravar(pasta, "dim_responsavel.csv",
               ["responsavel_key", "responsavel"], responsaveis)

    locais = sorted([
        "Camara Fria Substancias", "Cofre Balistica", "Cofre DNA",
        "Cofre IML", "Deposito Central (Cuiaba)",
        "Deposito Informatica", "Reserva Tecnica 1", "Sala Evidencias Gerais",
    ])
    local_map, local_rows = dim_alfabetica(locais)
    csv_gravar(pasta, "dim_local_armazenamento.csv",
               ["local_armaz_key", "local_armazenamento"], local_rows)

    gravar_calendario(pasta)

    # ---------- Fato (1300 movimentacoes)
    fato = []
    pesos_tipo = [10, 14, 8, 22, 9, 18, 8, 6, 12, 5]
    pesos_dest = [10, 8, 10, 4, 12, 22, 18, 16]
    pesos_status = [10, 25, 15, 30, 20]
    pesos_local = [14, 14, 18, 12, 8, 12, 6, 16]

    for n in range(1, 1301):
        d_coleta = data_aleatoria()
        # 70% ja foi recebida pelo destino, 30% ainda em custodia
        if pct(0.70):
            d_receb = d_coleta + dt.timedelta(days=random.randint(1, 14))
            d_baixa = (d_receb + dt.timedelta(days=random.randint(30, 360))
                       if pct(0.50) else "")
        else:
            d_receb = ""
            d_baixa = ""
        # timestamps via tempo em horas
        hr_coleta = random.randint(0, 23)
        hr_receb = (random.randint(0, 23) if d_receb else "")
        tempo_h = ""
        if d_coleta and d_receb:
            tempo_h = (d_receb - d_coleta).days * 24 + (hr_receb - hr_coleta) % 24
        tipo = random.choices(tipos, weights=pesos_tipo)[0]
        qtd = (random.randint(1, 50) if tipo not in ("Veiculo Apreendido", "Smartphone/Eletronico")
               else 1)
        if tipo == "Material Biologico - DNA":
            peso = round(random.uniform(0.5, 50.0), 2)
        elif tipo == "Substancia - Droga":
            peso = round(random.uniform(1.0, 5000.0), 2)
        elif tipo == "Veiculo Apreendido":
            peso = round(random.uniform(800, 2500), 0)
        else:
            peso = round(random.uniform(0.05, 8.0), 2)
        valor = (round(random.uniform(5000, 180000), 2) if tipo in
                 ("Veiculo Apreendido", "Smartphone/Eletronico", "Arma de Fogo") else "")
        st_escolhido = random.choices(status, weights=pesos_status)[0]
        fato.append([
            f"EVC-{d_coleta.year}-{n:05d}",
            data_key(d_coleta),
            data_key(d_receb) if d_receb else "",
            data_key(d_baixa) if d_baixa else "",
            tipo_map[tipo],
            orig_map[random.choice(origens)],
            dest_map[random.choices(destinos, weights=pesos_dest)[0]],
            st_map[st_escolhido],
            responsaveis[random.randint(0, len(responsaveis) - 1)][0],
            local_map[random.choices(locais, weights=pesos_local)[0]],
            qtd,
            peso,
            valor,
            tempo_h,
        ])
    csv_gravar(pasta, "fato_mov_evidencia.csv",
               ["id_evidencia", "data_coleta_key", "data_recebimento_key",
                "data_baixa_key", "tipo_evidencia_key", "origem_key",
                "destino_key", "status_custodia_key", "responsavel_key",
                "local_armaz_key", "qtd_itens", "peso_gramas",
                "valor_estimado", "tempo_transporte_horas"], fato)


# =================================================================
# READMES POR CENARIO
# =================================================================
READMES = {}

READMES["cenario1_backlog"] = r"""# Cenario 1 - Backlog de Pericias

Dataset sintetico de **requisicoes periciais** da POLITEC/MT para o **projeto
integrador** da Aula 5. O foco e construir um dashboard de **fila de trabalho**
com TAT (turnaround time), atraso por setor e perito, e distribuicao por
tipo de exame e prioridade. Anonimizado, gerado por
`../gerar_datasets_aula5.py` (semente fixa).

---

## Arquivos (modelo estrela)

```text
              dim_calendario  dim_status  dim_prioridade
                    \           |              |
   dim_setor -- fato_requisicoes -- dim_perito
                    |
            dim_tipo_exame  dim_delegacia
```

| Tabela              | Grao (1 linha =)    | Linhas |
|---------------------|---------------------|--------|
| `fato_requisicoes`  | 1 requisicao        | 1200   |
| `dim_setor`         | 1 setor             | 8      |
| `dim_perito`        | 1 perito            | 12     |
| `dim_tipo_exame`    | 1 tipo de exame     | 8      |
| `dim_delegacia`     | 1 delegacia (MT)    | 16     |
| `dim_prioridade`    | Alta / Media / Baixa | 3     |
| `dim_status`        | 5 estados           | 5      |
| `dim_calendario`    | 1 dia               | 1096   |

---

## Sugestoes de visuais para a aba de Backlog

- **Cartao (KPI)**: total em atraso, % de laudos concluidos no prazo.
- **Colunas agrupadas**: backlog por `setor_key` filtrando `status = Aguardando/Em Analise`.
- **Linha temporal**: TAT medio mensal (mediana) por mes/ano.
- **Matriz**: cruzamento `setor x tipo_exame` com `em_atraso`.
- **Slicer**: `data_entrada_key`, `prioridade`, `tipo_exame`, `delegacia_key`.
- **Tabela de detalhe**: top 10 requisicoes atrasadas (drill through).

---

## Numeros de referencia (referencia)

| Indicador                                   | Valor aprox. |
|---------------------------------------------|--------------|
| Total de requisicoes                        | 1.200        |
| % concluidas                                | ~80%         |
| % dentro do prazo                           | ~70%         |
| Prazo medio (dias uteis) para DNA           | 90           |
| Prazo medio (dias uteis) para Necropsia     | 15           |
| Periodo dos fatos                           | 2023-01-01 a 2025-12-31 |
"""

READMES["cenario2_dna"] = r"""# Cenario 2 - TAT do Laboratorio de DNA

Dataset sintetico de **exames de DNA** da POLITEC/MT (4 laboratorios, 5
metodologias). Foco do dashboard: **TAT (turnaround time)**, gargalo por
laboratorio, qualidade da amostra, custo-eficiencia de kits. Anonimizado.

---

## Arquivos

| Tabela               | Grao (1 linha =)    | Linhas |
|----------------------|---------------------|--------|
| `fato_exames_dna`    | 1 exame de DNA      | 1100   |
| `dim_laboratorio`    | 1 laboratorio DNA   | 4      |
| `dim_metodologia`    | 1 metodologia       | 5      |
| `dim_analista`       | 1 analista          | 14     |
| `dim_status_exame`   | 1 status            | 6      |
| `dim_kit_reagente`   | 1 kit (kit, marca, lote) | 12 |
| `dim_calendario`     | 1 dia               | 1096   |

---

## Sugestoes de visuais para a aba de TAT do DNA

- **Cartao (KPI)**: TAT medio (geral), TAT mediano, % exames dentro da meta (90 dias).
- **Boxplot** nativo ou histograma: distribuicao de `tat_dias`.
- **Linha temporal**: TAT mensal por laboratorio.
- **Pareto**: exames por metodologia (concentracao de demanda).
- **Heatmap**: laboratorio (linha) x status (coluna), contagem.
- **Tabela cruzada**: kits mais usados por metodologia.
- **Slicer**: periodo (ano/mes), laboratorio, metodologia, status.

---

## Numeros de referencia (referencia)

| Indicador                                  | Valor aprox. |
|--------------------------------------------|--------------|
| Total de exames                            | 1.100        |
| % concluidos                               | ~88%         |
| TAT medio (dias)                           | ~70          |
| TAT P90 (estimado)                         | ~150 dias    |
| Periodo dos fatos                          | 2023-01-01 a 2025-12-31 |
"""

READMES["cenario3_criminalidade"] = r"""# Cenario 3 - Mapa da Criminalidade em MT

Dataset sintetico de **ocorrencias criminais** nos 18 municipios-polo da
POLITEC/MT, com tipo de crime, arma, faixa etaria da vitima e periodo do dia.
Foco do dashboard: **inteligencia geografica** (mapa), perfil da vitima,
sazonalidade, arma predominante, alerta de latrocinio. Anonimizado.

---

## Arquivos

| Tabela                | Grao (1 linha =)    | Linhas |
|-----------------------|---------------------|--------|
| `fato_ocorrencias`    | 1 ocorrencia/BO     | 1500   |
| `dim_municipio`       | 1 municipio (MT)    | 18     |
| `dim_tipo_crime`      | 1 tipo              | 7      |
| `dim_arma`            | 1 tipo de arma      | 6      |
| `dim_faixa_etaria`    | 1 faixa             | 6      |
| `dim_periodo_dia`     | 1 faixa de horario  | 4      |
| `dim_calendario`      | 1 dia               | 1096   |

---

## Sugestoes de visuais para a aba de Criminalidade

- **Mapa Preenchido (Shape Map / Bing)**: ocorrencias por municipio, com densidade.
- **Linha temporal**: serie diaria ou mensal com pico de sazonalidade.
- **Colunas empilhadas**: tipo de crime x arma (%).
- **Piramide etaria (barras divergentes)**: vitimas por faixa etaria e sexo.
- **Heatmap de calendario (matrix)**: dia da semana x hora do dia.
- **Cartoes KPI**: total de vitimas, latrocinios, % flagrante.
- **Slicer**: ano, municipio (com hierarquia microrregiao se quiser), tipo, arma.

---

## Numeros de referencia

| Indicador                          | Valor aprox. |
|------------------------------------|--------------|
| Total de ocorrencias               | 1.500        |
| Vitimas envolvidas (soma)          | ~1.700       |
| % Roubo (tipo mais frequente)      | ~24%         |
| % Arma de Fogo                     | ~38%         |
| % flagrante                        | ~18%         |
| Periodo dos fatos                  | 2023-01-01 a 2025-12-31 |
"""

READMES["cenario4_orcamento"] = r"""# Cenario 4 - Orcamento e Contratos

Dataset sintetico de **execucao orcamentaria e contratos** da POLITEC/MT, com
empenhos, dotacao anual, fornecedores, contratos e modalidades. Foco do
dashboard: **execucao orcamentaria (empenhado x liquidado x pago)**, ranking de
fornecedores, prazo de vigencia dos contratos e visibilidade para a **diretoria
financeira**. Anonimizado.

---

## Arquivos

| Tabela              | Grao (1 linha =)        | Linhas |
|---------------------|--------------------------|--------|
| `fato_empenhos`     | 1 nota de empenho        | 1.300  |
| `fato_dotacao`      | 1 setor x rubrica x ano  | 240    |
| `dim_setor`         | 1 setor                  | 8      |
| `dim_rubrica`       | 1 rubrica (codigo+rotulo)| 10     |
| `dim_modalidade`    | 1 modalidade             | 6      |
| `dim_fonte`         | 1 fonte de recurso       | 5      |
| `dim_status_empenho`| 1 status                 | 5      |
| `dim_fornecedor`    | 1 fornecedor             | 50     |
| `dim_contrato`      | 1 contrato               | 80     |
| `dim_calendario`    | 1 dia                    | 1096   |

---

## Sugestoes de visuais para a aba de Orcamento

- **Cartao (KPI)**: total empenhado, total pago, % execucao vs dotacao.
- **Funil (Waterfall)**: orcado x atual x empenhado x liquidado x pago.
- **Linha temporal**: empenho diario / mensal por fonte.
- **Colunas empilhadas**: setor x status de empenho.
- **Top-N (10) com detalhamento**: fornecedores com maior valor pago.
- **Tabela com sparkline**: contratos vigentes x valor x dias para vencer.
- **Slicer**: ano, setor, rubrica, fonte, modalidade, status.

---

## Numeros de referencia

| Indicador                                  | Valor aprox. |
|--------------------------------------------|--------------|
| Total empenhado (R$)                       | ~85 milhoes  |
| % Pago                                     | ~30%         |
| % Cancelado                                | ~8%          |
| Contratos ativos (nao vencidos em 2025)    | ~52          |
| Periodo dos fatos                          | 2023-01-01 a 2025-12-31 |
"""

READMES["cenario5_custodia"] = r"""# Cenario 5 - Cadeia de Custodia de Evidencias

Dataset sintetico de **movimentacao de evidencias** na cadeia de custodia
POLITEC/MT, da coleta ate o destino (lab/arquivo/destruicao). Foco do
dashboard: **rastreabilidade**, integridade da cadeia, tempo medio de
transporte, gargalo por local de armazenamento e **conformidade processual**
(quem coletou, quem recebeu, em quanto tempo).

---

## Arquivos

| Tabela                    | Grao (1 linha =)    | Linhas |
|---------------------------|---------------------|--------|
| `fato_mov_evidencia`      | 1 evidencia (ciclo) | 1.300  |
| `dim_tipo_evidencia`      | 1 tipo              | 10     |
| `dim_origem`              | 1 origem            | 8      |
| `dim_destino`             | 1 destino           | 8      |
| `dim_status_custodia`     | 1 status (5)        | 5      |
| `dim_responsavel`         | 1 pessoa            | 15     |
| `dim_local_armazenamento` | 1 local             | 8      |
| `dim_calendario`          | 1 dia               | 1096   |

---

## Sugestoes de visuais para a aba de Custodia

- **Sankey** ou **Fluxo**: origem -> destino (por tipo de evidencia).
- **Cartao (KPI)**: total de evidencias, tempo medio de transporte, lacradas.
- **Heatmap**: hora de coleta x dia da semana (gargalo operacional).
- **Linha do tempo (Drill Through)** por evidencia: cadeia completa.
- **Pareto**: tipos de evidencia por quantidade e por valor estimado.
- **Tabela de auditoria**: evidencias com `status = Em Transporte` (> 14 dias = alerta).
- **Slicer**: tipo, origem, destino, status, periodo.

---

## Numeros de referencia

| Indicador                                | Valor aprox. |
|------------------------------------------|--------------|
| Total de evidencias (ciclos)             | 1.300        |
| % lacradas ou concluidas                 | ~50%         |
| % ainda em transporte                    | ~15%         |
| Tempo medio de transporte (horas)        | ~80h         |
| % Materiais biologicos (DNA)             | ~22%         |
| Periodo dos fatos                        | 2023-01-01 a 2025-12-31 |

---

## Como integrar tudo no projeto integrador

1. Copie **pelo menos 3** pastas de cenario para `Documents/Projeto_Integrador/datasets/`.
2. No Power BI Desktop, **Obter Dados -> Pasta** apontando para essa pasta:
   o Power BI junta as tabelas (cada cenario tem suas proprias tabelas).
3. **Cuidado com dimensoes de mesmo nome**: tabelas `dim_calendario` vao se
   fundir se tiverem os mesmos campos; use sufixo (`dim_calendario_backlog`,
   `dim_calendario_dna`) ou remova de um dos cenarios.
4. Monte cada aba tematica: cada aba consome apenas as tabelas do seu cenario.
5. O **projeto integrador** exige **>=3 abas**, **>=1 slicer por aba**, e
   pelo menos um KPI com formato condicional.
"""

README_GERAL = r"""# Aula 5 - Datasets para o Projeto Integrador

Cinco datasets sinteticos da POLITEC/MT em **modelo estrela** (cada cenario =
1 pasta, 1 tabela fato + dimensoes proprias + dim_calendario compartilhada).
Todos os fatos tem **>= 1000 linhas** para permitir pratica realista de
agregacoes, slicers, drill e DAX. Cada cenario foi desenhado para virar **uma
aba tematica** do dashboard final do projeto integrador.

| # | Cenario | Pasta | Tema | Fato (linhas) |
|---|---------|-------|------|---------------|
| 1 | Backlog de Pericias      | `cenario1_backlog/`       | Operacional - filas e TAT     | 1.200 |
| 2 | TAT do Laboratorio de DNA | `cenario2_dna/`           | Laboratorio - qualidade/TAT   | 1.100 |
| 3 | Mapa da Criminalidade em MT | `cenario3_criminalidade/` | Inteligencia geografica      | 1.500 |
| 4 | Orcamento e Contratos    | `cenario4_orcamento/`     | Gestao financeira             | 1.300 + 240 |
| 5 | Cadeia de Custodia       | `cenario5_custodia/`      | Rastreabilidade de evidencias | 1.300 |

> Cada cenario traz `README.md` proprio com o esquema estrela, numeros de
> referencia e **sugestoes de visuais** (quais visuais funcionam bem para aquela
> aba tematica).

---

## O projeto integrador exige, no minimo

- **3 abas tematicas** (pegar 3 dos 5 cenarios; cada aba = 1 cenario);
- **1 slicer por aba** (periodo + 1 atributo do cenario);
- **1 KPI com formatacao condicional** (verde / amarelo / vermelho);
- **1 visual geografico OU temporal** para cada aba;
- **RLS (Row-Level Security)** recomendada em pelo menos uma aba;
- Publicacao em **workspace segregado** + link para a App.

Detalhes no caderno: `Parte 5 - Projeto Integrador`.

---

## Como carregar no Power BI

1. Abra o Power BI Desktop e crie um arquivo novo (`Projeto_Integrador.pbix`).
2. **Obter Dados -> Pasta** e selecione **a pasta inteira** da Aula 5/datasets/.
3. O Power BI importa cada CSVs como uma tabela individual. Conecte-as com a
   `dim_calendario` propria de cada cenario por relacionamentos 1:N.
4. Para limpar e "tipar", use o Power Query (o caderno da Aula 4 tem o
   passo a passo).
5. Crie a tabela de medidas (clicar com botao direito em qualquer medida ->
   nova medida) e aplique DAX.

---

## Convencoes

- CSV UTF-8 com BOM, separador `;`, datas ISO `AAAA-MM-DD`.
- `data_key` inteiro no formato `AAAAMMDD`.
- Chaves substitutas (surrogate keys) inteiras, atribuidas por ordem alfabetica.
- `dim_calendario` compartilhada em cada pasta, comecando em
  `2023-01-01` ate `2025-12-31` (1096 dias).
- Sem dependencia externa: todos os arquivos abrem com duplo clique.
"""


def escrever_readmes():
    pasta_datasets = DATASETS
    for nome in READMES:
        (pasta_datasets / nome).mkdir(parents=True, exist_ok=True)
        (pasta_datasets / nome / "README.md").write_text(READMES[nome], encoding="utf-8")
    (pasta_datasets / "README.md").write_text(README_GERAL, encoding="utf-8")


# =================================================================
# MAIN
# =================================================================
def main():
    cenario1_backlog(DATASETS / "cenario1_backlog")
    cenario2_dna(DATASETS / "cenario2_dna")
    cenario3_criminalidade(DATASETS / "cenario3_criminalidade")
    cenario4_orcamento(DATASETS / "cenario4_orcamento")
    cenario5_custodia(DATASETS / "cenario5_custodia")
    escrever_readmes()

    print("5 datasets + READMEs gerados em:", DATASETS.relative_to(RAIZ))
    for p in sorted(DATASETS.iterdir()):
        if p.is_dir():
            csvs = list(p.glob("*.csv"))
            print(f"  {p.name:30s}  {len(csvs)} CSVs")
    print("Semente:", SEED)


if __name__ == "__main__":
    main()
