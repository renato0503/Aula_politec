# -*- coding: utf-8 -*-
"""Empacota os 5 datasets da Aula 7 em um workbook Excel por cenario.

Cada arquivo .xlsx tem as 8 tabelas do modelo estrela em abas separadas
(`fato_execucao`, `dim_*`) + uma aba `LEIA-ME` com o guia de uso, o dicionario
de dados e a tabela-resumo medida.

Uso:  python gerar_excel_aula7.py
"""
import csv
import pathlib
from collections import defaultdict

import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parent
DATASETS = RAIZ / "datasets"

TABELAS = [
    "fato_execucao",
    "dim_etapa",
    "dim_unidade",
    "dim_sistema",
    "dim_tipo_atividade",
    "dim_status_execucao",
    "dim_projeto",
    "dim_calendario",
]

CENARIOS = [
    {
        "pasta": "cenario1_apreensao_armas",
        "xlsx": "Cenario1_Apreensao_Armas.xlsx",
        "titulo": "Apreensao e pericia de armas",
        "desc": "Da apreensao na prisao ate o encaminhamento a autoridade. O painel "
                "precisa mostrar a fila da prova de fogo e o peso do registro no SINARM.",
        "gargalo": "Prova de fogo",
        "perguntas": [
            "Qual etapa concentra a maior fila do processo de armas?",
            "Quanto da espera esta no SINARM e quanto esta na prova de fogo?",
            "O retrabalho esta concentrado na conferencia ou no registro?",
            "Qual unidade acumula mais espera: o armamento ou a pericia balistica?",
        ],
    },
    {
        "pasta": "cenario2_sinistro_transito",
        "xlsx": "Cenario2_Sinistro_Transito.xlsx",
        "titulo": "Sinistro de transito",
        "desc": "Da abertura do sinistro ate o pagamento da indenizacao. O painel "
                "precisa separar a espera da empresa de documentos da espera interna.",
        "gargalo": "Documentos",
        "perguntas": [
            "Quanto do tempo do sinistro e espera por documento do segurado?",
            "A vistoria em campo e gargalo ou so e trabalho?",
            "Em que etapa o retrabalho e maior?",
            "Qual unidade acumula mais espera?",
        ],
    },
    {
        "pasta": "cenario3_credenciamento_peritos",
        "xlsx": "Cenario3_Credenciamento_Peritos.xlsx",
        "titulo": "Credenciamento de peritos",
        "desc": "Do edital ate o repasse do pagamento. O painel precisa mostrar a fila "
                "da analise de curriculo e do parecer da comissao.",
        "gargalo": "Curriculo + Parecer",
        "perguntas": [
            "Curriculo e parecer concentram quanto da espera do credenciamento?",
            "A inscricao on-line ja reduz a espera de entrada?",
            "O retrabalho vem de documento faltando ou de parecer devolvido?",
            "Qual etapa tem mais trabalho manual e qual tem mais fila?",
        ],
    },
    {
        "pasta": "cenario4_etilometria",
        "xlsx": "Cenario4_Etilometria.xlsx",
        "titulo": "Operacao de etilometria",
        "desc": "Do acionamento da operacao ate o envio ao DETRAN. O painel precisa "
                "mostrar a fila da conferencia do aparelho e da emissao do auto.",
        "gargalo": "Conferencia + Auto",
        "perguntas": [
            "A espera esta na conferencia do aparelho ou na emissao do auto?",
            "Quantas execucoes sao automatizadas hoje?",
            "O retrabalho vem de falha de impressao ou de devolucao?",
            "Qual unidade e responsavel pelo maior volume de espera?",
        ],
    },
    {
        "pasta": "cenario5_atendimento_ouvidoria",
        "xlsx": "Cenario5_Atendimento_Ouvidoria.xlsx",
        "titulo": "Atendimento ao publico e ouvidoria",
        "desc": "Da abertura do protocolo ate o encerramento. O painel precisa mostrar "
                "a fila de instrucao e o peso do retrabalho por documento faltando.",
        "gargalo": "Instrucao + Resposta",
        "perguntas": [
            "Quanto do tempo do cidadao e espera por instrucao e resposta?",
            "Qual etapa concentra o retrabalho?",
            "A abertura digital ja corta a espera de entrada?",
            "Qual area tecnica mais demora para responder?",
        ],
    },
]


def ler_csv(pasta, nome):
    return pd.read_csv(pasta / f"{nome}.csv", sep=";", encoding="utf-8-sig")


def resumo_etapas(pasta):
    fato = ler_csv(pasta, "fato_execucao")
    etapa = ler_csv(pasta, "dim_etapa")
    fato["tempo_espera_min"] = pd.to_numeric(fato["tempo_espera_min"], errors="coerce").fillna(0)
    fato["tempo_execucao_min"] = pd.to_numeric(fato["tempo_execucao_min"], errors="coerce").fillna(0)
    fato["flag_retrabalho"] = pd.to_numeric(fato["flag_retrabalho"], errors="coerce").fillna(0)
    g = fato.groupby("etapa_key").agg(
        execucoes=("id_execucao", "count"),
        espera_min=("tempo_espera_min", "sum"),
        execucao_min=("tempo_execucao_min", "sum"),
        retrabalho=("flag_retrabalho", "sum"),
    ).reset_index()
    g = g.merge(etapa[["etapa_key", "etapa", "sequencia", "unidade_padrao"]], on="etapa_key", how="left")
    g["espera_h"] = g["espera_min"] / 60
    g["execucao_h"] = g["execucao_min"] / 60
    total_espera = g["espera_h"].sum()
    total_exec = g["execucao_h"].sum()
    total = total_espera + total_exec
    g["share_espera"] = g["espera_h"] / total_espera
    g["espera_media_h"] = g["espera_h"] / g["execucoes"]
    g["execucao_media_h"] = g["execucao_h"] / g["execucoes"]
    g["retrabalho_pct"] = g["retrabalho"] / g["execucoes"]
    g = g.sort_values("sequencia")
    return fato, g, total_espera, total_exec, total


def escrever_leia_me(wb, ws, meta, fato, g, total_espera, total_exec, total, contagens):
    fmt_titulo = wb.add_format({"bold": True, "font_size": 18, "font_color": "#1F3864"})
    fmt_sub = wb.add_format({"bold": True, "font_size": 12, "font_color": "#1F3864"})
    fmt_txt = wb.add_format({"text_wrap": True, "valign": "top"})
    fmt_cab = wb.add_format({"bold": True, "font_color": "#FFFFFF", "bg_color": "#1F3864",
                             "border": 1, "valign": "vcenter"})
    fmt_cel = wb.add_format({"border": 1, "valign": "top", "text_wrap": True})
    fmt_num = wb.add_format({"border": 1, "num_format": "#,##0.0", "valign": "top"})
    fmt_pct = wb.add_format({"border": 1, "num_format": "0.0%", "valign": "top"})
    fmt_int = wb.add_format({"border": 1, "num_format": "#,##0", "valign": "top"})

    ws.set_column("A:A", 4)
    ws.set_column("B:B", 30)
    ws.set_column("C:C", 16)
    ws.set_column("D:D", 16)
    ws.set_column("E:E", 16)
    ws.set_column("F:F", 22)

    r = 0
    ws.write(r, 0, f"Cenario {meta['n']} - {meta['titulo']}", fmt_titulo); r += 1
    ws.write(r, 0, meta["desc"], fmt_txt); r += 2

    ws.write(r, 0, "O QUE TEM NESTE ARQUIVO", fmt_sub); r += 1
    ws.write(r, 0, "Cada aba e uma tabela do modelo estrela. A tabela fato tem "
                   "uma linha por execucao de etapa; as dimensoes dao nome, "
                   "unidade, sistema, tipo, status, projeto e data.", fmt_txt); r += 2

    ws.write(r, 0, "N", fmt_cab)
    ws.write(r, 1, "Aba", fmt_cab)
    ws.write(r, 2, "Linhas", fmt_cab)
    ws.write(r, 3, "Grao", fmt_cab)
    ws.write(r, 4, "Papel no painel", fmt_cab)
    ws.write(r, 5, "Tipo", fmt_cab); r += 1
    abas = [
        ("LEIA-ME", "guia", "-", "Este guia", "Nao importar no Power BI"),
        ("fato_execucao", "fato", len(fato), "1 linha = 1 execucao de etapa", "Tempos, flags e custo"),
        ("dim_etapa", "dimensao", contagens.get("dim_etapa", "-"), "1 linha = 1 etapa", "Nome e ordem da etapa (eixo do Pareto)"),
        ("dim_unidade", "dimensao", contagens.get("dim_unidade", "-"), "1 linha = 1 unidade", "Swimlane, filtro e matriz"),
        ("dim_sistema", "dimensao", contagens.get("dim_sistema", "-"), "1 linha = 1 sistema", "Quanto do processo ainda e manual"),
        ("dim_tipo_atividade", "dimensao", contagens.get("dim_tipo_atividade", "-"), "1 linha = 1 tipo", "Tarefa manual, aprovacao, espera..."),
        ("dim_status_execucao", "dimensao", contagens.get("dim_status_execucao", "-"), "1 linha = 1 status", "Qualidade, devolucao e cancelamento"),
        ("dim_projeto", "dimensao", contagens.get("dim_projeto", "-"), "1 linha = 1 projeto", "Intervencoes planejadas"),
        ("dim_calendario", "dimensao", contagens.get("dim_calendario", "-"), "1 linha = 1 dia", "TAT, sazonalidade e linha do tempo"),
    ]
    for idx, (nome, tipo, linhas, grao, papel) in enumerate(abas, start=1):
        ws.write(r, 0, idx, fmt_int)
        ws.write(r, 1, nome, fmt_cel)
        ws.write(r, 2, linhas, fmt_cel if isinstance(linhas, str) else fmt_int)
        ws.write(r, 3, grao, fmt_cel)
        ws.write(r, 4, papel, fmt_cel)
        ws.write(r, 5, tipo, fmt_cel)
        r += 1
    r += 1

    ws.write(r, 0, "NUMEROS MEDIDOS NESTE DATASET", fmt_sub); r += 1
    ws.write(r, 0, "Execucoes", fmt_cab)
    ws.write(r, 1, "Espera total (h)", fmt_cab)
    ws.write(r, 2, "Execucao total (h)", fmt_cab)
    ws.write(r, 3, "% espera", fmt_cab)
    ws.write(r, 4, "TAT medio por caso (h)", fmt_cab)
    ws.write(r, 5, "Retrabalho", fmt_cab); r += 1
    ciclos = fato["id_ciclo"].nunique()
    retr = (pd.to_numeric(fato["flag_retrabalho"], errors="coerce").fillna(0) == 1).mean()
    ws.write(r, 0, len(fato), fmt_int)
    ws.write(r, 1, total_espera, fmt_num)
    ws.write(r, 2, total_exec, fmt_num)
    ws.write(r, 3, total_espera / total, fmt_pct)
    ws.write(r, 4, total / ciclos, fmt_num)
    ws.write(r, 5, retr, fmt_pct)
    r += 2

    ws.write(r, 0, "RESUMO POR ETAPA (referencia - confira contra o seu painel)", fmt_sub); r += 1
    cabec = ["Seq", "Etapa", "Execucoes", "Espera media (h)", "Execucao media (h)",
             "Share da espera", "Retrabalho"]
    for i, c in enumerate(cabec):
        ws.write(r, i, c, fmt_cab)
    r += 1
    for _, row in g.iterrows():
        ws.write(r, 0, int(row["sequencia"]), fmt_int)
        ws.write(r, 1, row["etapa"], fmt_cel)
        ws.write(r, 2, int(row["execucoes"]), fmt_int)
        ws.write(r, 3, row["espera_media_h"], fmt_num)
        ws.write(r, 4, row["execucao_media_h"], fmt_num)
        ws.write(r, 5, row["share_espera"], fmt_pct)
        ws.write(r, 6, row["retrabalho_pct"], fmt_pct)
        r += 1
    r += 1

    ws.write(r, 0, "COMO USAR NO POWER BI", fmt_sub); r += 1
    passos = [
        "1. Power BI Desktop > Obter dados > Pasta de trabalho do Excel.",
        "2. Selecione este arquivo e marque as 8 abas de dados (nao marque LEIA-ME).",
        "3. Em Transformar dados, confirme a primeira linha como cabecalho e os tipos.",
        "4. Feche e aplique. No Modelo, ligue cada *_key da fato a sua dimensao.",
        "5. Marque dim_calendario como tabela de datas (coluna data).",
        "6. Crie as medidas de tempo, % espera, casos, TAT e retrabalho.",
        "7. Monte os visuais: cartoes, barras empilhadas, Pareto, linha do tempo e matriz.",
        "8. Adicione segmentacoes de etapa, unidade e ano. Salve o .pbix.",
    ]
    for passo in passos:
        ws.write(r, 0, passo, fmt_txt); r += 1
    r += 1

    ws.write(r, 0, "PERGUNTAS QUE O PAINEL DEVE RESPONDER", fmt_sub); r += 1
    for pergunta in meta["perguntas"]:
        ws.write(r, 0, "- " + pergunta, fmt_txt); r += 1
    r += 1

    ws.write(r, 0, "CONVENCOES", fmt_sub); r += 1
    convencoes = [
        "Separador original: ponto e virgula. Os CSVs usam UTF-8 com BOM.",
        "tempo_espera_min e tempo_execucao_min em minutos; tempo_total_h em horas.",
        "custo_execucao_rs em R$. data_key no formato AAAAMMDD.",
        "Dados sinteticos: qualquer semelhanca com processos reais e coincidencia.",
    ]
    for conv in convencoes:
        ws.write(r, 0, "- " + conv, fmt_txt); r += 1


def formatar_aba(wb, ws, df, nome):
    fmt_cab = wb.add_format({"bold": True, "font_color": "#FFFFFF", "bg_color": "#1F3864",
                             "border": 1, "align": "center", "valign": "vcenter"})
    fmt_data = wb.add_format({"num_format": "0.0"})
    fmt_hora = wb.add_format({"num_format": "0.00"})
    fmt_moeda = wb.add_format({"num_format": "#,##0.00"})
    fmt_int = wb.add_format({"num_format": "#,##0"})

    for col, nome_col in enumerate(df.columns):
        largura = max(10, min(42, max(len(str(nome_col)) + 2,
                                      df[nome_col].astype(str).head(120).str.len().max() or 10)))
        ws.set_column(col, col, largura)
    ws.set_row(0, 26, fmt_cab)
    ws.freeze_panes(1, 0)
    ws.autofilter(0, 0, len(df), len(df.columns) - 1)

    for col, nome_col in enumerate(df.columns):
        if nome_col in ("tempo_espera_min", "tempo_execucao_min"):
            ws.set_column(col, col, 16, fmt_data)
        elif nome_col == "tempo_total_h":
            ws.set_column(col, col, 14, fmt_hora)
        elif nome_col == "custo_execucao_rs":
            ws.set_column(col, col, 16, fmt_moeda)
        elif nome_col.endswith("_key") or nome_col in ("dia", "mes", "trimestre", "dia_semana"):
            ws.set_column(col, col, 12, fmt_int)


def main():
    for i, meta in enumerate(CENARIOS, start=1):
        pasta = DATASETS / meta["pasta"]
        fato, g, total_espera, total_exec, total = resumo_etapas(pasta)
        meta = dict(meta, n=i)
        destino = pasta / meta["xlsx"]
        with pd.ExcelWriter(destino, engine="xlsxwriter") as writer:
            wb = writer.book
            ws_leia = wb.add_worksheet("LEIA-ME")
            contagens = {t: len(ler_csv(pasta, t)) for t in TABELAS}
            escrever_leia_me(wb, ws_leia, meta, fato, g, total_espera, total_exec, total, contagens)
            for tabela in TABELAS:
                df = ler_csv(pasta, tabela)
                df.to_excel(writer, sheet_name=tabela, index=False)
                formatar_aba(wb, writer.sheets[tabela], df, tabela)
            wb.set_properties({
                "title": f"Cenario {i} - {meta['titulo']}",
                "subject": "Dataset de processo da Aula 7 - POLITEC/MT",
                "author": "Curso de Capacitacao POLITEC/MT",
                "comments": "Dados sinteticos para aula de BI, gargalo e automacao.",
            })
        print(f"  {destino.name}  ({destino.stat().st_size/1024:.0f} KB)")
    print("5 workbooks gerados.")


if __name__ == "__main__":
    main()
