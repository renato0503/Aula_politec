"""Separa cada app em uma pasta autônoma, pronta para virar um repositório próprio no GitHub.

Depois de rodar, cada Apps/<app>/ tem:
  nucleo/casca.html     a casca do app (cabeçalho, menu, roteador, IndexedDB, perfis, backup, testes)
  nucleo/visual.css     a identidade visual do app
  nucleo/icones.js      os ícones
  nucleo/comum.js       configuração e testes comuns
  construir.py          gera o index.html (e embute vendor/ e os JSON de dados)
  testes/testar.py      teste de estrutura (zero rede, #/testes, rotas, dados, tema)
  testes/cenarios.py    os cenários de interface dos sprints deste app
  .gitignore

Nenhum app depende mais de Apps/_base/. O _base/ fica como molde para apps novos.
Uso (uma vez): python Apps/_base/separar.py [app ...]
"""
import ast
import json
import pathlib
import shutil
import sys

AQUI = pathlib.Path(__file__).resolve().parent
APPS = AQUI.parent
TODOS = sorted(p.parent.name for p in APPS.glob("*/app.json"))

CONSTRUIR = r'''"""Constrói o index.html deste app (arquivo único, offline).

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

PADROES = %(padroes)s
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
'''

TESTAR = r'''"""Teste de estrutura deste app no Chromium (Playwright).

  1. abre por file:// e confere que nenhuma requisição sai para a rede;
  2. roda #/testes e exige 100% de testes passando;
  3. abre todas as rotas com cada perfil, sem "Erro nesta tela";
  4. carrega os dados fictícios, recarrega e confere que os dados ficaram;
  5. troca o perfil pelo menu do cabeçalho; confere o tema e o celular sem rolagem horizontal;
  6. não aceita erro no console.

Uso: python testes/testar.py      (requer: pip install playwright && playwright install chromium)
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

PASTA = pathlib.Path(__file__).resolve().parent.parent


def testar(navegador):
    falhas, rede, console = [], [], []
    url = (PASTA / "index.html").as_uri()
    ctx = navegador.new_context()
    pg = ctx.new_page()
    pg.on("request", lambda r: rede.append(r.url) if not r.url.startswith(("file:", "data:", "blob:")) else None)
    pg.on("console", lambda m: console.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: console.append(str(e)))
    pg.on("dialog", lambda d: d.accept())

    pg.goto(url + "#/testes")
    try:
        pg.wait_for_selector("#resumoTestes", timeout=15000)
    except Exception:
        ctx.close()
        return [f"o app não abriu a tela de testes; erros no console: {console[:3]}"]
    for t in pg.evaluate("window.__testes"):
        if not t["ok"]:
            falhas.append(f"teste falhou: {t['nome']} {t['msg']}")

    app = pg.evaluate("APP")
    pg.goto(url); pg.wait_for_timeout(400)
    if "Escolha o perfil" in pg.inner_text("#conteudo"):
        falhas.append("a primeira abertura mostra uma tela de escolha de perfil")
    perfis = [p["id"] for p in app.get("perfis") or []] or [None]
    for p in perfis:
        if p:
            pg.evaluate("async p => { await db.meta('perfil', p); }", p)
            pg.reload(); pg.wait_for_timeout(300)
        for r in app["rotas"]:
            rota = r["rota"].replace(":proc", "PROC-2026-001").replace(":id", "x").replace(":curso", "x").replace(":protocolo", "x").replace(":mes", "2026-01")
            pg.goto(url + rota)
            pg.wait_for_timeout(120)
            texto = pg.inner_text("#conteudo")
            if "Erro nesta tela" in texto or "Tela não encontrada" in texto:
                falhas.append(f"perfil {p} · rota {r['rota']}: {texto[:120]}")

    pg.goto(url + "#/config")
    pg.wait_for_timeout(300)
    stores = list(app["db"]["stores"])
    if pg.locator("#btnSeed").count():
        pg.click("#btnSeed")
        pg.wait_for_timeout(800)
    contar = "async (s)=>{ const r = {}; for (const n of s) r[n] = (await db.list(n)).length; return r; }"
    antes = pg.evaluate(contar, stores)
    pg.reload()
    pg.wait_for_timeout(500)
    depois = pg.evaluate(contar, stores)
    if antes != depois:
        falhas.append(f"dados mudaram depois de recarregar: {antes} -> {depois}")
    if not any(depois.values()):
        falhas.append("nenhum dado carregado")
    if len(perfis) > 1 and perfis[0]:
        pg.click("#btnPerfil"); pg.wait_for_timeout(150)
        pg.click(f"#perfilLista [data-escolher-perfil='{perfis[1]}']"); pg.wait_for_timeout(400)
        if pg.evaluate("estado.perfil") != perfis[1]:
            falhas.append("o menu do cabeçalho não trocou o perfil")
    pg.click("#btnTema")
    if pg.evaluate("document.documentElement.dataset.theme") not in ("dark", "light"):
        falhas.append("botão de tema sem efeito")
    ctx.close()

    cel = navegador.new_context(viewport={"width": 390, "height": 844})
    pc = cel.new_page(); pc.on("dialog", lambda d: d.accept())
    pc.goto(url); pc.wait_for_timeout(500)
    if pc.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 2"):
        falhas.append("no celular (390 px) a página rola na horizontal")
    cel.close()

    if rede:
        falhas.append(f"requisições de rede: {rede[:3]}")
    if console:
        falhas.append(f"erros no console: {console[:3]}")
    return falhas


def main():
    with sync_playwright() as p:
        nav = p.chromium.launch()
        falhas = testar(nav)
        nav.close()
    print(("OK   " if not falhas else "FALHA"), PASTA.name)
    for f in falhas:
        print("      -", f)
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
'''

CENARIOS_CAB = r'''"""Cenários de interface deste app: usam a tela como uma pessoa usaria e conferem
o "Pronto quando" de cada sprint do sprint.md.

Uso: python testes/cenarios.py      (requer: pip install playwright && playwright install chromium)
"""
import pathlib
import sys
import tempfile

from playwright.sync_api import sync_playwright

PASTA = pathlib.Path(__file__).resolve().parent.parent
TMP = pathlib.Path(tempfile.mkdtemp(prefix="cenarios-"))
CENARIOS = []


def cenario(fn):
    CENARIOS.append(fn)
    return fn


def contar(pg, store):
    return pg.evaluate("async s => (await db.list(s)).length", store)


def ir(pg, url, rota, espera=250):
    pg.goto(url + rota)
    pg.wait_for_timeout(espera)
    try:
        pg.wait_for_function("() => typeof db === 'undefined' || !!db.con", timeout=10000)
    except Exception:
        pass


def perfil(pg, url, nome):
    ir(pg, url, "#/config")
    pg.evaluate("async p => { await db.meta('perfil', p); }", nome)
    pg.reload()
    pg.wait_for_function("() => typeof db !== 'undefined' && !!db.con", timeout=15000)
    pg.wait_for_timeout(300)

'''

CENARIOS_PE = r'''

def main():
    erro = False
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for fn in CENARIOS:
            ctx = nav.new_context(accept_downloads=True)
            # nos cenários, todas as abas das fichas ficam abertas (os campos precisam estar visíveis)
            ctx.add_init_script("try { localStorage.setItem('abas:todas', '1'); } catch (e) {}")
            pg = ctx.new_page()
            console = []
            pg.on("pageerror", lambda e: console.append(str(e)))
            pg.on("console", lambda m: console.append(m.text) if m.type == "error" else None)
            pg.on("dialog", lambda d: d.accept())
            resultados = []

            def ok(nome, cond):
                resultados.append((nome, bool(cond)))
            try:
                fn(pg, (PASTA / "index.html").as_uri(), ok)
            except Exception as e:
                resultados.append((f"exceção: {str(e).splitlines()[0][:160]}", False))
            if console:
                resultados.append((f"erros no console: {console[:2]}", False))
            falhas = [n for n, c in resultados if not c]
            print(("OK   " if not falhas else "FALHA"), PASTA.name, "·", fn.__name__, f"· {len(resultados) - len(falhas)}/{len(resultados)}")
            for n in falhas:
                print("      -", n)
            erro |= bool(falhas)
            ctx.close()
        nav.close()
    sys.exit(1 if erro else 0)


if __name__ == "__main__":
    main()
'''


def cenarios_do_app(app):
    """Extrai, dos arquivos de cenários atuais, as funções marcadas com @cenario("<app>")."""
    blocos = []
    fontes = [AQUI / "testar_sprints.py", *sorted((AQUI / "cenarios").glob("*.py"))]
    for arq in fontes:
        texto = arq.read_text(encoding="utf-8")
        linhas = texto.splitlines()
        for no in ast.parse(texto).body:
            if not isinstance(no, ast.FunctionDef):
                continue
            dec = [d for d in no.decorator_list if isinstance(d, ast.Call) and getattr(d.func, "id", "") == "cenario"]
            if not dec or dec[0].args[0].value != app:
                continue
            ini = dec[0].lineno - 1
            corpo = "\n".join(linhas[ini:no.end_lineno])
            corpo = corpo.replace(f'@cenario("{app}")', "@cenario", 1)
            corpo = corpo.replace(f'APPS / "{app}"', "PASTA")
            blocos.append(f"# origem: {arq.name}\n{corpo}")
    return blocos


def padroes():
    sys.path.insert(0, str(AQUI))
    import construir as molde  # noqa: E402
    return molde.PADROES


def separar(app):
    pasta = APPS / app
    nucleo = pasta / "nucleo"
    # depois da separação o núcleo é do app e diverge do molde: não sobrescrever sem pedir
    if nucleo.exists() and "--forcar" not in sys.argv:
        return "já separado (use --forcar para sobrescrever o núcleo, os testes e o construir.py)"
    nucleo.mkdir(exist_ok=True)
    shutil.copyfile(AQUI / "base.html", nucleo / "casca.html")
    css = (AQUI / "visual.css").read_text(encoding="utf-8") + "\n" + (AQUI / "visual-identidade.css").read_text(encoding="utf-8")
    (nucleo / "visual.css").write_text(css, encoding="utf-8")
    shutil.copyfile(AQUI / "icones.js", nucleo / "icones.js")
    shutil.copyfile(AQUI / "js_comum.js", nucleo / "comum.js")
    (pasta / "construir.py").write_text(CONSTRUIR.replace("%(padroes)s", json.dumps(padroes(), ensure_ascii=False, indent=4)), encoding="utf-8")
    testes = pasta / "testes"
    testes.mkdir(exist_ok=True)
    (testes / "testar.py").write_text(TESTAR, encoding="utf-8")
    blocos = cenarios_do_app(app)
    (testes / "cenarios.py").write_text(CENARIOS_CAB + "\n\n".join(blocos) + CENARIOS_PE, encoding="utf-8")
    gi = pasta / ".gitignore"
    if not gi.exists():
        gi.write_text("__pycache__/\n*.pyc\n.venv/\n", encoding="utf-8")
    return len(blocos)


if __name__ == "__main__":
    for a in [x for x in sys.argv[1:] if not x.startswith("--")] or TODOS:
        print(f"{a:28s} {separar(a)} cenário(s)")
