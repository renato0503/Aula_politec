"""Gera exemplos/mapa-exemplo.xlsx: planilha fictícia no formato do modelo do app (abas PROCESSO e ITENS).

Empresas, CNPJs e valores são fictícios. Os CNPJs têm dígito verificador válido.
Uso: python exemplos/gerar_planilha_mapa.py
"""
import pathlib
import random

from openpyxl import Workbook

PASTA = pathlib.Path(__file__).resolve().parent
random.seed(20261105)


def cnpj(base12):
    d = [int(x) for x in base12]
    for pesos in ([5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]):
        r = sum(a * b for a, b in zip(d, pesos)) % 11
        d.append(0 if r < 2 else 11 - r)
    s = "".join(map(str, d))
    return f"{s[:2]}.{s[2:5]}.{s[5:8]}/{s[8:12]}-{s[12:]}"


ORGAOS = ["POLITEC", "PM", "PJC"]
GRUPOS = [
    ("1", "Alfa Suprimentos Ltda", cnpj("112223330001"), "", [("Luva nitrílica tamanho M", "CX", 38.9), ("Máscara PFF2", "UN", 2.45)]),
    ("2", "Beta Laboratório Comércio Ltda", cnpj("445556660001"), "", [("Swab estéril com tubo", "UN", 1.8), ("Envelope de segurança", "UN", 0.95), ("Lacre numerado", "PCT", 54.0)]),
    ("3", "", "", "Fracassado", [("Reagente luminol 500 ml", "FR", 312.0)]),
    ("4", "", "", "Deserto", [("Cabine de fluxo laminar", "UN", 48900.0)]),
]

wb = Workbook()
p = wb.active
p.title = "PROCESSO"
for linha in [("Processo", "PROC-2026-EXEMPLO"), ("Pregão", "012/2026"), ("Objeto", "Materiais de consumo para perícia (fictício)"), ("Exercício atual", "2026")]:
    p.append(linha)
it = wb.create_sheet("ITENS")
it.append(["Grupo", "Item", "Código SIAG", "Descrição", "Unidade", "Empresa", "CNPJ", "Situação", "Valor unitário", *[f"QTD {o}" for o in ORGAOS]])
n = 0
for g, emp, cn, sit, itens in GRUPOS:
    for desc, un, vu in itens:
        n += 1
        it.append([int(g), n, f"{random.randint(100000, 999999)}", desc, un, emp, cn, sit, vu, *[random.choice([0, 10, 20, 50, 100]) or 5 for _ in ORGAOS]])
destino = PASTA / "mapa-exemplo.xlsx"
wb.save(destino)
print("gerado:", destino)
