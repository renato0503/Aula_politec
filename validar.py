# -*- coding: utf-8 -*-
"""Valida um caderno: secoes, links do TOC, tema e erros de console.

Uso:  python validar.py 1     # valida Aula 1/caderno-dia1.html
"""
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent
N = sys.argv[1] if len(sys.argv) > 1 else "1"
HTML = RAIZ / f"Aula {N}" / f"caderno-dia{N}.html"

if not HTML.exists():
    print("HTML nao encontrado:", HTML)
    sys.exit(1)

texto = HTML.read_text(encoding="utf-8")
ids = set(re.findall(r'<section id="([^"]+)"', texto))
anchors = set(re.findall(r'nav\.toc|<a href="#([^"]+)"', texto))
hrefs = set(re.findall(r'<a href="#([^"]+)"', texto))
orfaos = sorted(hrefs - ids)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(HTML.as_uri(), wait_until="load")
    pg.wait_for_timeout(600)
    secs = pg.query_selector_all("main section")
    links = pg.query_selector_all("nav.toc a")
    h2s = pg.eval_on_selector_all("main section h2", "els => els.map(e => e.textContent.trim())")
    pg.click("#themebtn")
    tema = pg.get_attribute("html", "data-theme")
    b.close()

print(f"Arquivo: {HTML.name} ({len(texto)//1024} KB)")
print(f"Secoes: {len(secs)} | Links no TOC: {len(links)} | h2: {len(h2s)}")
print(f"Tema apos toggle: {tema}")
print(f"Links orfaos (TOC -> section inexistente): {orfaos or 'nenhum'}")
print(f"Erros de console: {errs or 'nenhum'}")
print("OK" if (len(secs) == len(links) == len(h2s) and not orfaos and not errs) else "ATENCAO")
