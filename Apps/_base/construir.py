"""Constrói o index.html de cada app (arquivo único, entregue ao usuário).

Fontes de cada app:
  Apps/<app>/app.json      título, aviso, banco (stores), perfis, rotas, bibliotecas e dados embutidos
  Apps/<app>/src/app.js    o código do app (telas, regras, testes)
  Apps/<app>/src/*.js      código acrescentado por sprint (sprint3.js, sprint4.js...), juntado depois do app.js
  Apps/<app>/src/app.css   CSS do app (opcional)

Fontes comuns (Apps/_base/):
  base.html                tema, roteador, IndexedDB, perfis, backup, #/testes
  js_comum.js              tela de configuração e testes comuns

O index.html é gerado: não edite ele direto. Depois de construir, as bibliotecas
de vendor/ e os JSON de dados entram pelo embutir.py.

Uso:
  python Apps/_base/construir.py            constrói os 10 apps
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


def todos():
    return sorted(p.parent.name for p in APPS.glob("*/app.json"))


def construir(pasta):
    raiz = APPS / pasta
    cfg = json.loads((raiz / "app.json").read_text(encoding="utf-8"))
    # src/app.js primeiro; depois os demais src/*.js em ordem (sprint3.js, sprint4.js, ...)
    extras = sorted(p for p in (raiz / "src").glob("*.js") if p.name != "app.js")
    js_app = "\n".join(p.read_text(encoding="utf-8") for p in [raiz / "src" / "app.js", *extras])
    css = raiz / "src" / "app.css"
    app = {"id": pasta, "titulo": cfg["titulo"], "db": cfg["db"], "rotas": cfg["rotas"]}
    for k in ("perfis", "rotaSemPerfil"):
        if k in cfg:
            app[k] = cfg[k]
    libs = [f"<!-- LIB:{n} --><!-- /LIB:{n} -->" for n in cfg.get("libs", [])]
    libs += [f"<!-- DADOS:{i}:{c} --><!-- /DADOS:{i} -->" for i, c in cfg.get("dados", [])]
    trocas = {
        "%%CSP%%": CSP if cfg.get("csp", True) else "<!-- Sem CSP: a página é servida pelo Apps Script (HtmlService). -->",
        "%%TITULO%%": cfg["titulo"], "%%SUBTITULO%%": cfg["subtitulo"], "%%DESCRICAO%%": cfg["descricao"],
        "%%AVISO%%": f'<div class="aviso-topo">{cfg["aviso"]}</div>' if cfg.get("aviso") else "",
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
