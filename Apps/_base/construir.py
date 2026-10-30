"""Constrói o index.html de cada app (arquivo único, entregue ao usuário).

Fontes de cada app:
  Apps/<app>/app.json      título, aviso, banco (stores), perfis, rotas, bibliotecas e dados embutidos
  Apps/<app>/src/app.js    o código do app (telas, regras, testes)
  Apps/<app>/src/*.js      código acrescentado por sprint (sprint3.js, sprint4.js...), juntado depois do app.js
  Apps/<app>/src/app.css   CSS do app (opcional)
  bloco "visual" do app.json  acento, icone, layout (topo|lateral), padrao do cabeçalho, estilo (institucional|claro), setor

Fontes comuns (Apps/_base/):
  base.html                tema, roteador, IndexedDB, perfis, backup, #/testes
  js_comum.js              tela de configuração e testes comuns
  visual.css               identidade visual SESP/MT e POLITEC/MT (comum a todos)
  icones.js                ícones das telas e do emblema

O index.html é gerado: não edite ele direto. Depois de construir, as bibliotecas
de vendor/ e os JSON de dados entram pelo embutir.py.

Uso:
  python Apps/_base/construir.py            constrói todos os apps
  python Apps/_base/construir.py <app> ...  constrói só os indicados
"""
import json
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
APPS = AQUI.parent
sys.path.insert(0, str(AQUI))
from embutir import embutir  # noqa: E402

CSP = ('<meta http-equiv="Content-Security-Policy" content="default-src \'self\' \'unsafe-inline\' data: blob:; '
       'connect-src \'none\'; img-src \'self\' data: blob:; media-src \'self\' blob: mediastream:; worker-src blob:">')


# padrões do cabeçalho (SVG em data URI, traço branco translúcido)
PADROES = {
    "linhas": '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22"><path d="M-2 24 24-2M9 24l15-15M-2 13 13-2" stroke="#fff" stroke-opacity=".07" stroke-width="1.2"/></svg>',
    "pontos": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18"><circle cx="2" cy="2" r="1.3" fill="#fff" fill-opacity=".10"/></svg>',
    "grade": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28"><path d="M28 0H0v28" fill="none" stroke="#fff" stroke-opacity=".07"/></svg>',
    "hexagonos": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="48"><path d="M14 0l14 8v16l-14 8L0 24V8zM14 32v16" fill="none" stroke="#fff" stroke-opacity=".08"/></svg>',
    "ondas": '<svg xmlns="http://www.w3.org/2000/svg" width="80" height="20"><path d="M0 10c10-8 30-8 40 0s30 8 40 0" fill="none" stroke="#fff" stroke-opacity=".08" stroke-width="1.4"/></svg>',
    "topografico": '<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120"><g fill="none" stroke="#fff" stroke-opacity=".07"><circle cx="30" cy="40" r="14"/><circle cx="30" cy="40" r="26"/><circle cx="30" cy="40" r="38"/><circle cx="96" cy="96" r="12"/><circle cx="96" cy="96" r="24"/></g></svg>',
}
VISUAL_PADRAO = {"acento": "#12487f", "icone": "escudo", "layout": "topo", "padrao": "linhas", "estilo": "institucional", "setor": ""}


def _rgb(h):
    h = h.lstrip("#"); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def _hex(c):
    return "#" + "".join(f"{max(0, min(255, round(x))):02x}" for x in c)


def _mistura(h, alvo, k):
    return _hex([a + (b - a) * k for a, b in zip(_rgb(h), alvo)])


def css_visual(v):
    """Variáveis do acento do app: claro (emblema), forte (hover) e escuro (tema escuro)."""
    import urllib.parse
    a = v["acento"]
    svg = PADROES.get(v["padrao"], PADROES["linhas"])
    uri = "data:image/svg+xml," + urllib.parse.quote(svg, safe="/:=\" ")
    return (f':root{{--app-acento:{a};--app-acento-claro:{v.get("acento_claro") or _mistura(a, [255] * 3, .22)};'
            f'--app-acento-forte:{_mistura(a, [0] * 3, .28)};--app-acento-escuro:{v.get("acento_escuro") or _mistura(a, [255] * 3, .52)};'
            f"--padrao:url('{uri}')}}")


def todos():
    return sorted(p.parent.name for p in APPS.glob("*/app.json"))


def construir(pasta):
    raiz = APPS / pasta
    cfg = json.loads((raiz / "app.json").read_text(encoding="utf-8"))
    # src/app.js primeiro; depois os demais src/*.js em ordem (sprint3.js, sprint4.js, ...)
    extras = sorted(p for p in (raiz / "src").glob("*.js") if p.name != "app.js")
    js_app = "\n".join(p.read_text(encoding="utf-8") for p in [raiz / "src" / "app.js", *extras])
    css = raiz / "src" / "app.css"
    visual = {**VISUAL_PADRAO, **cfg.get("visual", {})}
    app = {"id": pasta, "titulo": cfg["titulo"], "db": cfg["db"], "rotas": cfg["rotas"], "visual": visual}
    for k in ("perfis", "rotaSemPerfil"):
        if k in cfg:
            app[k] = cfg[k]
    libs = [f"<!-- LIB:{n} --><!-- /LIB:{n} -->" for n in cfg.get("libs", [])]
    libs += [f"<!-- DADOS:{i}:{c} --><!-- /DADOS:{i} -->" for i, c in cfg.get("dados", [])]
    trocas = {
        "%%CSP%%": CSP if cfg.get("csp", True) else "<!-- Sem CSP: a página é servida pelo Apps Script (HtmlService). -->",
        "%%TITULO%%": cfg["titulo"], "%%SUBTITULO%%": cfg["subtitulo"], "%%DESCRICAO%%": cfg["descricao"],
        "%%AVISO%%": f'<div class="aviso-topo">{cfg["aviso"]}</div>' if cfg.get("aviso") else "",
        "%%CSS_BASE%%": (AQUI / "visual.css").read_text(encoding="utf-8"),
        "%%CSS_VISUAL%%": css_visual(visual),
        "%%LAYOUT%%": visual["layout"], "%%ESTILO%%": visual["estilo"], "%%SETOR%%": visual["setor"] or cfg["subtitulo"],
        "%%APP_ID%%": pasta, "%%ICONES%%": (AQUI / "icones.js").read_text(encoding="utf-8"),
        "%%CSS_APP%%": css.read_text(encoding="utf-8") if css.exists() else "",
        "%%LIBS%%": "\n".join(libs) or "<!-- nenhuma -->",
        "%%APP_JSON%%": json.dumps(app, ensure_ascii=False, indent=2),
        "%%JS_APP%%": (AQUI / "js_comum.js").read_text(encoding="utf-8") + "\n" + js_app,
    }
    html = (AQUI / "base.html").read_text(encoding="utf-8")
    for k, v in trocas.items():
        html = html.replace(k, v)
    (raiz / "index.html").write_text(html, encoding="utf-8")
    return embutir(raiz)


def main():
    alvos = sys.argv[1:] or todos()
    for pasta in alvos:
        rel = construir(pasta)
        print(f"{pasta:28s} {rel[-1]}")


if __name__ == "__main__":
    main()
