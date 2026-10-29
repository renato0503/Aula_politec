"""Testa o index.html de cada app no Chromium (Playwright), como o critério de pronto do Sprint 1.

Para cada app:
  1. abre por file:// e confere que nenhuma requisição sai para a rede;
  2. roda #/testes e exige 100% de testes passando;
  3. escolhe o primeiro perfil (quando há perfis) e abre todas as rotas, sem "Erro nesta tela";
  4. carrega os dados fictícios em #/config, recarrega a página e confere que os dados ficaram;
  5. não aceita erro no console.

Uso: python Apps/_base/testar.py [pasta-do-app ...]
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

APPS = pathlib.Path(__file__).resolve().parent.parent
TODOS = sorted(p.parent.name for p in APPS.glob("*/app.json"))


def testar(navegador, pasta):
    falhas, rede, console = [], [], []
    url = (APPS / pasta / "index.html").as_uri()
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
        return [f"o app não abriu a tela de testes; erros no console: {console[:3]}"], "não abriu"
    testes = pg.evaluate("window.__testes")
    for t in testes:
        if not t["ok"]:
            falhas.append(f"teste falhou: {t['nome']} {t['msg']}")

    app = pg.evaluate("APP")
    if app.get("perfis"):
        pg.goto(url + "#/config")
        pg.wait_for_timeout(300)
        if pg.locator("[data-perfil]").count():
            pg.locator("[data-perfil]").first.click()
            pg.wait_for_timeout(300)
    for r in app["rotas"]:
        rota = r["rota"].replace(":proc", "PROC-2026-001").replace(":id", "x").replace(":curso", "x").replace(":protocolo", "x")
        pg.goto(url + rota)
        pg.wait_for_timeout(150)
        texto = pg.inner_text("#conteudo")
        if "Erro nesta tela" in texto or "Tela não encontrada" in texto:
            falhas.append(f"rota {r['rota']}: {texto[:120]}")

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
    pg.click("#btnTema")
    if pg.evaluate("document.documentElement.dataset.theme") not in ("dark", "light"):
        falhas.append("botão de tema sem efeito")
    if rede:
        falhas.append(f"requisições de rede: {rede[:3]}")
    if console:
        falhas.append(f"erros no console: {console[:3]}")
    ctx.close()
    ok = sum(t["ok"] for t in testes)
    resumo = {k: v for k, v in depois.items() if v}
    return falhas, f"{ok}/{len(testes)} testes · {len(app['rotas'])} rotas · dados {json.dumps(resumo, ensure_ascii=False)}"


def main():
    alvos = sys.argv[1:] or TODOS
    erro = False
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for pasta in alvos:
            falhas, resumo = testar(nav, pasta)
            print(("OK   " if not falhas else "FALHA"), pasta, "·", resumo)
            for f in falhas:
                print("      -", f)
            erro |= bool(falhas)
        nav.close()
    sys.exit(1 if erro else 0)


if __name__ == "__main__":
    main()
