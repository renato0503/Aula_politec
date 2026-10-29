"""Embute bibliotecas e dados dentro do index.html de um app (mantém o app em um arquivo só).

O index.html marca onde cada conteúdo entra:

  <!-- LIB:xlsx.full.min.js --><!-- /LIB:xlsx.full.min.js -->
      recebe <script> com o conteúdo de vendor/xlsx.full.min.js

  <!-- DADOS:seed:exemplos/seed.json --><!-- /DADOS:seed -->
      recebe <script type="application/json" id="seed"> com o JSON (minificado)

O que estiver entre os marcadores é substituído a cada execução. Por isso, rodar de
novo depois de atualizar uma biblioteca ou um seed atualiza o app.

Uso: python Apps/_base/embutir.py "Apps/<pasta-do-app>"
"""
import json
import pathlib
import re
import sys

RE_LIB = re.compile(r"<!-- LIB:([\w.\-]+) -->.*?<!-- /LIB:\1 -->", re.S)
RE_DADOS = re.compile(r"<!-- DADOS:([\w\-]+):([^ ]+) -->.*?<!-- /DADOS:\1 -->", re.S)


def embutir(pasta):
    pasta = pathlib.Path(pasta)
    html_path = pasta / "index.html"
    html = html_path.read_text(encoding="utf-8")
    relatorio = []

    def lib(m):
        nome = m.group(1)
        codigo = (pasta / "vendor" / nome).read_text(encoding="utf-8").replace("</script", "<\\/script")
        relatorio.append(f"LIB   {nome:28s} {len(codigo) / 1024:8.0f} KB")
        return f"<!-- LIB:{nome} -->\n<script>{codigo}</script>\n<!-- /LIB:{nome} -->"

    def dados(m):
        ident, caminho = m.group(1), m.group(2)
        obj = json.loads((pasta / caminho).read_text(encoding="utf-8"))
        texto = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        relatorio.append(f"DADOS {ident:28s} {len(texto.encode('utf-8')) / 1024:8.0f} KB  ({caminho})")
        return f'<!-- DADOS:{ident}:{caminho} -->\n<script type="application/json" id="{ident}">{texto}</script>\n<!-- /DADOS:{ident} -->'

    html = RE_LIB.sub(lib, html)
    html = RE_DADOS.sub(dados, html)
    html_path.write_text(html, encoding="utf-8")
    relatorio.append(f"index.html total {html_path.stat().st_size / 1024:.0f} KB")
    return relatorio


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for linha in embutir(sys.argv[1]):
        print(linha)
