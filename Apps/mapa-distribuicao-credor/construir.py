"""Constrói o index.html do Mapa de Distribuição (arquivo único, offline).

Fonte:   src/mapa.html          telas, regras, leitura da planilha e do PDF do pregoeiro
Libs:    vendor/xlsx.full.min.js (SheetJS 0.18.5), embutida no lugar de <!-- LIB:xlsx.full.min.js -->

O index.html é gerado: não edite ele direto.
A versão anterior (Sprints 1 a 7, com núcleo comum e #/testes) está em legado/.
Uso: python construir.py
"""
import pathlib
import re

PASTA = pathlib.Path(__file__).resolve().parent


def lib(m):
    codigo = (PASTA / "vendor" / m.group(1)).read_text(encoding="utf-8").replace("</script", r"<\/script")
    return f"<script>{codigo}</script>"


def main():
    fonte = (PASTA / "src" / "mapa.html").read_text(encoding="utf-8")
    html, n = re.subn(r"<!-- LIB:([\w.\-]+) -->", lib, fonte)
    (PASTA / "index.html").write_text(html, encoding="utf-8", newline="\n")
    print(f"index.html: {len(html.encode('utf-8')) / 1024:.0f} KB, {n} biblioteca(s) embutida(s)")


if __name__ == "__main__":
    main()
