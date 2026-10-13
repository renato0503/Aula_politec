# -*- coding: utf-8 -*-
"""Gerador do modelo estrela (fato/dim) da POLITEC/MT.

Le os 4 CSVs planos de origem em `Aula 2/datasets/` e monta um modelo
dimensional completo (4 tabelas fato + 10 dimensoes + dim_calendario),
gravando o resultado em `datasets/` das Aulas 2, 3 e 4 (autocontido).

Convencoes:
- CSV UTF-8 com BOM, separador ';', datas ISO (AAAA-MM-DD).
- Chaves substitutas (surrogate keys) inteiras, atribuidas por ordem alfabetica.
- dim_setor e uma dimensao conformada (atende requisicoes, movimentacao e orcamento).

Uso:  python gerar_datasets_estrela.py
"""
import pathlib
import csv
import datetime as dt

RAIZ = pathlib.Path(__file__).resolve().parent
ORIGEM = RAIZ / "Aula 2" / "datasets"
DESTINOS = [RAIZ / "Aula 2" / "datasets", RAIZ / "Aula 3" / "datasets", RAIZ / "Aula 4" / "datasets"]

FONTES = ["requisicoes_periciais.csv", "movimentacao_reagentes.csv",
          "produtividade_peritos.csv", "orcamento_setores.csv"]


def ler(nome):
    with open(ORIGEM / nome, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def gravar(nome, cabecalho, linhas):
    for destino in DESTINOS:
        destino.mkdir(parents=True, exist_ok=True)
        with open(destino / nome, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, delimiter=";", lineterminator="\r\n")
            w.writerow(cabecalho)
            w.writerows(linhas)


def dim(valores):
    """Retorna (mapa valor->chave, linhas) com chave inteira em ordem alfabetica."""
    ordenados = sorted(set(valores))
    mapa = {v: i + 1 for i, v in enumerate(ordenados)}
    linhas = [[mapa[v], v] for v in ordenados]
    return mapa, linhas


def data_key(iso):
    """'2025-03-04' -> 20250304 (int). Vazio -> ''."""
    if not iso:
        return ""
    d = dt.date.fromisoformat(iso)
    return d.year * 10000 + d.month * 100 + d.day


def primeiro_dia_mes(ano_mes):
    """'2025-06' -> '2025-06-01'."""
    ano, mes = ano_mes.split("-")
    return f"{ano}-{mes}-01"


def main():
    req = ler("requisicoes_periciais.csv")
    mov = ler("movimentacao_reagentes.csv")
    pro = ler("produtividade_peritos.csv")
    orc = ler("orcamento_setores.csv")

    # ---- Dimensoes ----------------------------------------------------
    setor_map, setor_rows = dim(
        [r["setor"] for r in req] + [m["setor"] for m in mov] + [o["laboratorio"] for o in orc])
    tipo_map, tipo_rows = dim([r["tipo_exame"] for r in req] + [p["tipo_exame"] for p in pro])
    perito_map, perito_rows = dim([r["perito_responsavel"] for r in req] + [p["perito"] for p in pro])
    deleg_map, deleg_rows = dim([r["delegacia_origem"] for r in req])
    status_map, status_rows = dim([r["status"] for r in req])
    reag_map, reag_rows = dim([m["reagente"] for m in mov])
    forn_map, forn_rows = dim([m["fornecedor"] for m in mov if m["fornecedor"]])
    tmov_map, tmov_rows = dim([m["tipo_movimentacao"] for m in mov])
    rubrica_map, rubrica_rows = dim([o["rubrica"] for o in orc])

    gravar("dim_setor.csv", ["setor_key", "setor"], setor_rows)
    gravar("dim_tipo_exame.csv", ["tipo_exame_key", "tipo_exame"], tipo_rows)
    gravar("dim_perito.csv", ["perito_key", "perito"], perito_rows)
    gravar("dim_delegacia.csv", ["delegacia_key", "delegacia"], deleg_rows)
    gravar("dim_status.csv", ["status_key", "status"], status_rows)
    gravar("dim_reagente.csv", ["reagente_key", "reagente"], reag_rows)
    gravar("dim_fornecedor.csv", ["fornecedor_key", "fornecedor"], forn_rows)
    gravar("dim_tipo_movimentacao.csv", ["tipo_movimentacao_key", "tipo_movimentacao"], tmov_rows)
    gravar("dim_rubrica.csv", ["rubrica_key", "rubrica"], rubrica_rows)

    # ---- Calendario ---------------------------------------------------
    datas = []
    for r in req:
        datas.append(r["data_recebimento"])
        if r["data_laudo"]:
            datas.append(r["data_laudo"])
    datas += [m["data"] for m in mov]
    dtos = sorted(dt.date.fromisoformat(d) for d in datas if d)
    inicio = dtos[0].replace(day=1)
    fim_bruto = dtos[-1]
    fim = (fim_bruto.replace(day=1) + dt.timedelta(days=31)).replace(day=1) - dt.timedelta(days=1)

    meses = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    dias_sem = ["", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira",
                "Sexta-feira", "Sábado", "Domingo"]

    cal_rows = []
    d = inicio
    while d <= fim:
        cal_rows.append([
            d.year * 10000 + d.month * 100 + d.day,
            d.isoformat(),
            d.year,
            d.month,
            meses[d.month],
            f"{d.year:04d}-{d.month:02d}",
            (d.month - 1) // 3 + 1,
            d.day,
            d.isoweekday(),
            dias_sem[d.isoweekday()],
        ])
        d += dt.timedelta(days=1)
    gravar("dim_calendario.csv",
           ["data_key", "data", "ano", "mes", "nome_mes", "ano_mes", "trimestre",
            "dia", "dia_semana", "nome_dia_semana"], cal_rows)

    # ---- Fatos --------------------------------------------------------
    fato_req = []
    for r in req:
        dias = int(r["dias_uteis"]) if r["dias_uteis"] else ""
        em_atraso = 1 if (dias != "" and dias > 60) else 0
        fato_req.append([
            r["id_requisicao"],
            data_key(r["data_recebimento"]),
            data_key(r["data_laudo"]),
            setor_map[r["setor"]],
            tipo_map[r["tipo_exame"]],
            perito_map[r["perito_responsavel"]],
            deleg_map[r["delegacia_origem"]],
            status_map[r["status"]],
            dias,
            em_atraso,
        ])
    gravar("fato_requisicoes.csv",
           ["id_requisicao", "data_recebimento_key", "data_laudo_key", "setor_key",
            "tipo_exame_key", "perito_key", "delegacia_key", "status_key",
            "dias_uteis", "em_atraso"], fato_req)

    fato_mov = []
    for m in mov:
        fato_mov.append([
            int(m["id"]),
            data_key(m["data"]),
            reag_map[m["reagente"]],
            setor_map[m["setor"]],
            tmov_map[m["tipo_movimentacao"]],
            int(m["quantidade"]),
            forn_map[m["fornecedor"]] if m["fornecedor"] else "",
        ])
    gravar("fato_movimentacao.csv",
           ["id", "data_key", "reagente_key", "setor_key", "tipo_movimentacao_key",
            "quantidade", "fornecedor_key"], fato_mov)

    fato_prod = []
    for p in pro:
        fato_prod.append([
            perito_map[p["perito"]],
            data_key(primeiro_dia_mes(p["mes"])),
            tipo_map[p["tipo_exame"]],
            int(p["laudos_concluidos"]),
        ])
    gravar("fato_produtividade.csv",
           ["perito_key", "data_key", "tipo_exame_key", "laudos_concluidos"], fato_prod)

    fato_orc = []
    for o in orc:
        fato_orc.append([
            setor_map[o["laboratorio"]],
            rubrica_map[o["rubrica"]],
            int(o["orcado"]),
            int(o["realizado"]),
        ])
    gravar("fato_orcamento.csv",
           ["setor_key", "rubrica_key", "orcado", "realizado"], fato_orc)

    # ---- Copiar as fontes planas para Aulas 3 e 4 (autocontido) --------
    for destino in DESTINOS:
        destino.mkdir(parents=True, exist_ok=True)
        for nome in FONTES:
            (destino / nome).write_bytes((ORIGEM / nome).read_bytes())

    print("Modelo estrela gerado.")
    print(f"  dims: 10 (dim_calendario com {len(cal_rows)} dias)")
    print(f"  fato_requisicoes:  {len(fato_req)}")
    print(f"  fato_movimentacao: {len(fato_mov)}")
    print(f"  fato_produtividade:{len(fato_prod)}")
    print(f"  fato_orcamento:    {len(fato_orc)}")
    print("  destinos: " + ", ".join(str(d.relative_to(RAIZ)) for d in DESTINOS))


if __name__ == "__main__":
    main()
