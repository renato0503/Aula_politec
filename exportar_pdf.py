# -*- coding: utf-8 -*-
"""Exporta o caderno de uma aula para PDF A4 (duas passadas).

Uso:
    python exportar_pdf.py 1     # Aula 1/caderno-dia1.html -> "Caderno Dia 1 - POLITEC.pdf"
    python exportar_pdf.py 2     # Aula 2

Passada 1: gera o HTML e o PDF, descobre em que pagina cada secao comecou.
Passada 2: regera o HTML com os numeros no sumario e exporta de novo.
Forca tema claro, abre as respostas do quiz e cria marcadores (outline) no PDF.

Requisitos: pip install playwright pymupdf && playwright install chromium
"""
import json
import pathlib
import subprocess
import sys

import pymupdf
from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent
N = sys.argv[1] if len(sys.argv) > 1 else "1"
PASTA = RAIZ / f"Aula {N}"
HTML = PASTA / f"caderno-dia{N}.html"
PDF = PASTA / f"Caderno Dia {N} - POLITEC.pdf"
GERADOR = PASTA / f"gerar_caderno_aula{N}.py"
MAPA = PASTA / "_paginas.json"

RODAPE = ('<div style="width:100%;font-family:Arial,sans-serif;font-size:8px;color:#7a8084;padding:0 13mm;'
          'display:flex;justify-content:space-between">'
          f'<span>Caderno do Dia {N} · Curso de Capacitacao POLITEC/MT</span>'
          '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')


def gerar_html(com_paginas=False):
    args = [sys.executable, str(GERADOR)]
    if com_paginas:
        args.append(str(MAPA))
    subprocess.run(args, check=True)


def exportar():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(color_scheme="light")
        pg.goto(HTML.as_uri(), wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        pg.wait_for_timeout(800)
        pg.emulate_media(media="print")
        pg.pdf(path=str(PDF), prefer_css_page_size=True, print_background=True,
               display_header_footer=True, header_template="<span></span>", footer_template=RODAPE,
               outline=True, tagged=True)
        ids = pg.eval_on_selector_all("main section", "els => els.map(e => e.id)")
        b.close()
    return ids


def mapear_paginas(ids):
    doc = pymupdf.open(str(PDF))
    paginas = {}
    for n, anchor in enumerate(ids, start=1):
        alvo = f"§ {n}"
        for i, page in enumerate(doc):
            linhas = [l.strip() for l in page.get_text().splitlines()]
            if alvo in linhas:
                paginas[anchor] = i + 1
                break
    return paginas, len(doc)


if not HTML.exists() or not GERADOR.exists():
    print("Nao encontrei caderno/gerador da Aula", N, "-", PASTA)
    sys.exit(1)

gerar_html()
ids = exportar()
mapa, _ = mapear_paginas(ids)
MAPA.write_text(json.dumps(mapa), encoding="utf-8")

gerar_html(com_paginas=True)
ids = exportar()
mapa2, total = mapear_paginas(ids)
MAPA.unlink()

faltando = [a for a in ids if a not in mapa2]
if mapa != mapa2 or faltando:
    print("ATENCAO: sumario pode estar desalinhado", faltando,
          {k: (mapa.get(k), v) for k, v in mapa2.items() if mapa.get(k) != v})
print(f"PDF: {PDF.name} — {total} paginas, {len(ids)} secoes no sumario")
