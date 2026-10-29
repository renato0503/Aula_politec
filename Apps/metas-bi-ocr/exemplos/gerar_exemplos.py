"""Gera 3 meses fictícios do relatório do Power BI 1 (laudos pendentes por unidade) (Sprint 0).

Saídas:
  powerbi1-AAAA-MM.csv    "Exportar dados" SUPOSTO do visual (trocar pelo formato real no Sprint 0)
  powerbi1-AAAA-MM.pdf    o mesmo relatório em PDF com texto (o PDF em imagem entra no Sprint 5)
  seed.json               unidades e os 3 meses no formato do app
  DIVERGENCIAS.md         uma divergência plantada por mês

Semente fixa = 20261029.
Uso: python "Apps/metas-bi-ocr/exemplos/gerar_exemplos.py"
"""
import json
import pathlib
import random

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)
UNIDADES = ["IML Cuiabá", "IML Várzea Grande", "Laboratório Forense", "Criminalística Cuiabá", "Regional Rondonópolis",
            "Regional Sinop", "Regional Cáceres", "Regional Barra do Garças", "Regional Tangará da Serra", "Regional Alta Floresta"]
MESES = ["2026-07", "2026-08", "2026-09"]


def main():
    pend = {u: random.randint(40, 900) for u in UNIDADES}
    meses, divergencias = [], []
    for m_idx, mes in enumerate(MESES):
        linhas = []
        for u in UNIDADES:
            pend[u] = max(0, int(pend[u] * random.uniform(0.85, 1.12)))
            linhas.append((u, pend[u]))
        total = sum(v for _, v in linhas)
        total_impresso = total
        if m_idx == 0:
            linhas[3] = (linhas[3][0], linhas[3][1] * 2)
            divergencias.append(f"| {mes} | Criminalística Cuiabá dobrou (variação acima de 30%, RN04) |")
        elif m_idx == 1:
            linhas[5] = ("Regional de Sinop (nova sigla)", linhas[5][1])
            divergencias.append(f"| {mes} | Unidade com nome diferente do cadastro (RN03) |")
        else:
            total_impresso = total + 17
            divergencias.append(f"| {mes} | Total do relatório 17 a mais que a soma das unidades (RN02) |")
        (AQUI / f"powerbi1-{mes}.csv").write_text("﻿Mês;Unidade;Laudos pendentes\n" + "".join(f"{mes};{u};{v}\n" for u, v in linhas) +
                                                  f"{mes};Total;{total_impresso}\n", encoding="utf-8")
        c = canvas.Canvas(str(AQUI / f"powerbi1-{mes}.pdf"), pagesize=A4)
        y = 790
        c.setFont("Helvetica-Bold", 13); c.drawString(50, y, f"Power BI 1 · Laudos pendentes (fictício) · {mes}"); y -= 30
        c.setFont("Helvetica-Bold", 11); c.drawString(50, y, "Unidade"); c.drawRightString(500, y, "Pendentes"); y -= 18
        c.setFont("Helvetica", 11)
        for u, v in linhas:
            c.drawString(50, y, u); c.drawRightString(500, y, str(v)); y -= 18
        c.setFont("Helvetica-Bold", 11); c.drawString(50, y, "Total"); c.drawRightString(500, y, str(total_impresso))
        c.save()
        meses.append({"id": mes, "total_relatorio": total_impresso, "linhas": [{"unidade": u, "pendentes": v} for u, v in linhas]})
    (AQUI / "DIVERGENCIAS.md").write_text("# Divergências plantadas\n\n| Mês | Divergência |\n|---|---|\n" + "\n".join(divergencias) + "\n", encoding="utf-8")
    seed = {"unidades": [{"nome": u, "apelidos": []} for u in UNIDADES],
            "exemplos": meses}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print("meses", MESES, "| unidades", len(UNIDADES))


if __name__ == "__main__":
    main()
