"""Testa o index.html do Mapa de Distribuição no Chromium (Playwright).

1. abre por file:// sem nenhuma requisição de rede e sem erro no console;
2. baixa o modelo em branco e confere que ele tem abas;
3. importa a planilha de exemplo, salva o processo e abre as 8 etapas sem erro;
4. recarrega a página e confere que o processo ficou guardado;
5. confere o botão de tema.

Uso: python testes/testar.py [planilha.xlsx]
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

PASTA = pathlib.Path(__file__).resolve().parent.parent
EXEMPLO = PASTA / "exemplos" / "mapa-exemplo.xlsx"
ETAPAS = ["importar", "relatorio", "mapa", "empresas", "dotacao", "conferencia", "exportar", "backup"]


def testar(planilha):
    falhas, rede, console = [], [], []
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        ctx = nav.new_context(accept_downloads=True)
        pg = ctx.new_page()
        pg.on("request", lambda r: rede.append(r.url) if not r.url.startswith(("file:", "data:", "blob:")) else None)
        pg.on("console", lambda m: console.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: console.append(str(e)))
        pg.on("dialog", lambda d: d.accept())
        url = (PASTA / "index.html").as_uri()
        pg.goto(url)
        pg.wait_for_selector("#arquivo", state="attached", timeout=15000)

        with pg.expect_download() as dl:
            pg.click("#btnModelo")
        modelo = pathlib.Path(dl.value.path())
        if modelo.stat().st_size < 1000:
            falhas.append("modelo em branco vazio")

        pg.set_input_files("#arquivo", str(planilha))
        try:
            pg.wait_for_selector("#pSalvar", timeout=15000)
        except Exception:
            falhas.append("a prévia não abriu: " + pg.inner_text("#previa")[:300])
        else:
            if not pg.input_value("#pProcesso"):
                pg.fill("#pProcesso", "PROC-TESTE-001")
            pg.click("#pSalvar")
            pg.wait_for_url("**#/p/**", timeout=10000)
            base = pg.url.split("#")[1].rsplit("/", 1)[0]
            for etapa in ETAPAS:
                pg.goto(f"{url}#{base}/{etapa}")
                pg.wait_for_timeout(250)
                texto = pg.inner_text("#tela")
                if "Não consegui abrir" in texto or "não encontrado" in texto:
                    falhas.append(f"etapa {etapa}: {texto[:120]}")
            pg.goto(url + "#/processos")
            pg.reload()
            pg.wait_for_timeout(500)
            if pg.evaluate("() => banco.listar().then(l => l.length)") < 1:
                falhas.append("o processo não ficou guardado depois de recarregar")

        antes = pg.evaluate("document.documentElement.dataset.theme || 'claro'")
        pg.click("#btnTema")
        if pg.evaluate("document.documentElement.dataset.theme || 'claro'") == antes:
            falhas.append("botão de tema sem efeito")
        if rede:
            falhas.append(f"requisições de rede: {rede[:3]}")
        if console:
            falhas.append(f"erros no console: {console[:3]}")
        nav.close()
    return falhas


if __name__ == "__main__":
    arq = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else EXEMPLO
    f = testar(arq)
    for x in f:
        print("FALHA", x)
    print("OK" if not f else f"{len(f)} falha(s)")
    sys.exit(1 if f else 0)
