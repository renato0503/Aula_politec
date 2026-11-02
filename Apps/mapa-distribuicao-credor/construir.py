"""Constrói o index.html deste app (arquivo único, offline).

Fontes:
  app.json            título, banco (stores), perfis, rotas, bibliotecas, dados e o bloco "visual"
  src/app.js          telas, regras e testes; depois src/sprint*.js em ordem e, por último, src/identidade.js
  src/app.css         CSS próprio (opcional)
  nucleo/casca.html   casca do app (cabeçalho, menu, roteador, IndexedDB, perfis, backup, #/testes)
  nucleo/visual.css   identidade visual
  nucleo/icones.js    ícones
  nucleo/comum.js     configuração e testes comuns
  vendor/*.js         bibliotecas embutidas no index.html
  exemplos/seed.json  dados fictícios embutidos

O index.html é gerado: não edite ele direto.
Uso: python construir.py
"""
import json
import pathlib
import re
import urllib.parse

PASTA = pathlib.Path(__file__).resolve().parent
NUCLEO = PASTA / "nucleo"

CSP = ('<meta http-equiv="Content-Security-Policy" content="default-src \'self\' \'unsafe-inline\' data: blob:; '
       'connect-src \'none\'; img-src \'self\' data: blob:; media-src \'self\' blob: mediastream:; worker-src blob:">')

PADROES = {
    "linhas": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"22\" height=\"22\"><path d=\"M-2 24 24-2M9 24l15-15M-2 13 13-2\" stroke=\"#fff\" stroke-opacity=\".07\" stroke-width=\"1.2\"/></svg>",
    "pontos": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"18\" height=\"18\"><circle cx=\"2\" cy=\"2\" r=\"1.3\" fill=\"#fff\" fill-opacity=\".10\"/></svg>",
    "grade": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"28\" height=\"28\"><path d=\"M28 0H0v28\" fill=\"none\" stroke=\"#fff\" stroke-opacity=\".07\"/></svg>",
    "hexagonos": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"28\" height=\"48\"><path d=\"M14 0l14 8v16l-14 8L0 24V8zM14 32v16\" fill=\"none\" stroke=\"#fff\" stroke-opacity=\".08\"/></svg>",
    "ondas": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"80\" height=\"20\"><path d=\"M0 10c10-8 30-8 40 0s30 8 40 0\" fill=\"none\" stroke=\"#fff\" stroke-opacity=\".08\" stroke-width=\"1.4\"/></svg>",
    "topografico": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"120\" height=\"120\"><g fill=\"none\" stroke=\"#fff\" stroke-opacity=\".07\"><circle cx=\"30\" cy=\"40\" r=\"14\"/><circle cx=\"30\" cy=\"40\" r=\"26\"/><circle cx=\"30\" cy=\"40\" r=\"38\"/><circle cx=\"96\" cy=\"96\" r=\"12\"/><circle cx=\"96\" cy=\"96\" r=\"24\"/></g></svg>"
}
VISUAL_PADRAO = {"acento": "#12487f", "icone": "escudo", "layout": "topo", "padrao": "linhas", "estilo": "institucional", "setor": ""}
IDENTIDADE = {"cabecalho": "degrade", "fonte": "sistema", "densidade": "normal", "cantos": "suaves", "superficie": "cartoes", "kpi": "barra"}

RE_LIB = re.compile(r"<!-- LIB:([\w.\-]+) -->.*?<!-- /LIB:\1 -->", re.S)
RE_DADOS = re.compile(r"<!-- DADOS:([\w\-]+):([^ ]+) -->.*?<!-- /DADOS:\1 -->", re.S)


def _rgb(h):
    h = h.lstrip("#"); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def _hex(c):
    return "#" + "".join(f"{max(0, min(255, round(x))):02x}" for x in c)


def _mistura(h, alvo, k):
    return _hex([a + (b - a) * k for a, b in zip(_rgb(h), alvo)])


def css_visual(v):
    a = v["acento"]
    uri = "data:image/svg+xml," + urllib.parse.quote(PADROES.get(v["padrao"], PADROES["linhas"]), safe="/:=\" ")
    return (f':root{{--app-acento:{a};--app-acento-claro:{v.get("acento_claro") or _mistura(a, [255] * 3, .22)};'
            f'--app-acento-forte:{_mistura(a, [0] * 3, .28)};--app-acento-escuro:{v.get("acento_escuro") or _mistura(a, [255] * 3, .52)};'
            f"--padrao:url('{uri}')}}")


def embutir(html):
    relatorio = []

    def lib(m):
        nome = m.group(1)
        codigo = (PASTA / "vendor" / nome).read_text(encoding="utf-8").replace("</script", "<\\/script")
        relatorio.append(f"LIB   {nome:28s} {len(codigo) / 1024:8.0f} KB")
        return f"<!-- LIB:{nome} -->\n<script>{codigo}</script>\n<!-- /LIB:{nome} -->"

    def dados(m):
        ident, caminho = m.group(1), m.group(2)
        obj = json.loads((PASTA / caminho).read_text(encoding="utf-8"))
        texto = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        relatorio.append(f"DADOS {ident:28s} {len(texto.encode('utf-8')) / 1024:8.0f} KB  ({caminho})")
        return f'<!-- DADOS:{ident}:{caminho} -->\n<script type="application/json" id="{ident}">{texto}</script>\n<!-- /DADOS:{ident} -->'

    return RE_DADOS.sub(dados, RE_LIB.sub(lib, html)), relatorio


def construir():
    cfg = json.loads((PASTA / "app.json").read_text(encoding="utf-8"))
    src = PASTA / "src"
    extras = sorted((p for p in src.glob("*.js") if p.name != "app.js"), key=lambda p: (p.name == "identidade.js", p.name))
    js_app = "\n".join(p.read_text(encoding="utf-8") for p in [src / "app.js", *extras])
    css = src / "app.css"
    visual = {**VISUAL_PADRAO, **cfg.get("visual", {})}
    if visual.get("casca"):
        visual["layout"] = visual["casca"]
    app = {"id": PASTA.name, "titulo": cfg["titulo"], "db": cfg["db"], "rotas": cfg["rotas"], "visual": visual}
    for k in ("perfis", "rotaSemPerfil", "perfilPadrao", "rotaInicial", "permissoes", "buscaGlobal"):
        if k in cfg:
            app[k] = cfg[k]
    libs = [f"<!-- LIB:{n} --><!-- /LIB:{n} -->" for n in cfg.get("libs", [])]
    libs += [f"<!-- DADOS:{i}:{c} --><!-- /DADOS:{i} -->" for i, c in cfg.get("dados", [])]
    data_visual = " ".join(f'data-{k}="{visual.get(k) or p}"' for k, p in IDENTIDADE.items())
    trocas = {
        "%%CSP%%": CSP if cfg.get("csp", True) else "<!-- Sem CSP: a página é servida pelo Apps Script (HtmlService). -->",
        "%%TITULO%%": cfg["titulo"], "%%SUBTITULO%%": cfg["subtitulo"], "%%DESCRICAO%%": cfg["descricao"],
        "%%AVISO%%": f'<div class="aviso-topo">{cfg["aviso"]}</div>' if cfg.get("aviso") else "",
        "%%CSS_BASE%%": (NUCLEO / "visual.css").read_text(encoding="utf-8"),
        "%%CSS_VISUAL%%": css_visual(visual),
        "%%LAYOUT%%": visual["layout"], "%%DATA_VISUAL%%": data_visual, "%%ESTILO%%": visual["estilo"],
        "%%SETOR%%": visual["setor"] or cfg["subtitulo"],
        "%%APP_ID%%": PASTA.name, "%%ICONES%%": (NUCLEO / "icones.js").read_text(encoding="utf-8"),
        "%%CSS_APP%%": css.read_text(encoding="utf-8") if css.exists() else "",
        "%%LIBS%%": "\n".join(libs) or "<!-- nenhuma -->",
        "%%APP_JSON%%": json.dumps(app, ensure_ascii=False, indent=2),
        "%%JS_APP%%": (NUCLEO / "comum.js").read_text(encoding="utf-8") + "\n" + js_app,
    }
    html = (NUCLEO / "casca.html").read_text(encoding="utf-8")
    for k, v in trocas.items():
        html = html.replace(k, v)
    html, relatorio = embutir(html)
    (PASTA / "index.html").write_text(html, encoding="utf-8")
    relatorio.append(f"index.html total {(PASTA / 'index.html').stat().st_size / 1024:.0f} KB")
    return relatorio


if __name__ == "__main__":
    for linha in construir():
        print(linha)
