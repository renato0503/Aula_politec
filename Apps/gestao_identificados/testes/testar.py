"""Teste de estrutura deste app no Chromium (Playwright).

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
import time

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
    contar = "async (s)=>{ const r = {}; for (const n of s) r[n] = (await db.list(n)).length; return r; }"
    if pg.locator("#btnSeed").count():
        pg.click("#btnSeed")
        # espera a importação terminar: a contagem para de mudar (o tempo fixo dava corrida)
        fim = time.time() + 30; anterior = None
        while time.time() < fim:
            atual = pg.evaluate(contar, stores)
            if atual == anterior:
                break
            anterior = atual; pg.wait_for_timeout(250)
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
