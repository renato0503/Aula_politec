"""Testa o index.html do Mapa de Distribuição no Chromium (Playwright).

Também confere a situação do processo, o tipo custeio/investimento e o mapa orçamentário (SESP).

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


def conferir_pedidos_do_igor(pg, url, base):
    import io
    import openpyxl
    f = []
    pg.select_option("[data-situacao]", "cancelado"); pg.wait_for_timeout(300)
    pg.reload(); pg.wait_for_timeout(500)
    if pg.input_value("[data-situacao]") != "cancelado":
        f.append("a situação do processo não ficou gravada")
    pid = pg.evaluate("() => banco.listar().then(l => l[0].id)")
    # os resultados e uma dotação entram pelos dados, para o exemplo ter vencedor e valor
    grupo = pg.evaluate("""async id => { const p = await banco.ler(id); const g = p.grupos[0];
        g.situacao = 'vencedor'; g.empresa = g.empresa || 'EMPRESA FICTICIA LTDA'; g.cnpj = g.cnpj || '00000000000191';
        p.orgaos.forEach(o => { p.dot.grupos[chaveG(g.grupo, o)] = '3.3.90.30.' + o; }); await banco.gravar(p); return g.grupo; }""", pid)
    pg.goto(f"{url}#{base}/empresas"); pg.wait_for_timeout(400)
    if not pg.locator("#tabGrupos").count() or "Empresa ganhadora" not in pg.inner_text("#tabGrupos"):
        f.append("a tabela Grupos e empresas não apareceu")
        return f
    pg.select_option(f'[data-tipo-grupo="{grupo}"]', "investimento"); pg.wait_for_timeout(300)
    pg.reload(); pg.wait_for_timeout(500)
    if pg.input_value(f'[data-tipo-grupo="{grupo}"]') != "investimento":
        f.append("o tipo do grupo não ficou gravado")
    pg.goto(f"{url}#{base}/exportar"); pg.wait_for_timeout(400)
    with pg.expect_download() as d:
        pg.click("#xSesp")
    wb = openpyxl.load_workbook(io.BytesIO(pathlib.Path(d.value.path()).read_bytes()), data_only=False)
    if wb.sheetnames != ["MAPA ORÇAMENTÁRIO", "DOTAÇÃO ORÇAMENTÁRIA"]:
        f.append(f"abas do mapa SESP: {wb.sheetnames}")
    linhas = [r for r in wb["MAPA ORÇAMENTÁRIO"].iter_rows(values_only=True)]
    dados = [r for r in linhas[5:] if r[0] and r[0] != "TOTAL" and not str(r[0]).startswith("SALDO")]
    if not dados or any(r[1] != "4" or not str(r[2]).startswith("3.3.90.30.") or not r[4] for r in dados):
        f.append("o mapa SESP não trouxe tipo, dotação e credor")
    esperado = pg.evaluate("() => { const g = dotacaoGerada(ATUAL); return Math.round(g.linhas.reduce((a, l) => a + l.total, 0) * 100); }")
    if round(sum(r[7] for r in dados) * 100) != esperado or esperado <= 0:
        f.append(f"o total do mapa SESP difere do quadro de dotação: {esperado}")
    with pg.expect_download() as d:
        pg.click("#xCompleto")
    nomes = openpyxl.load_workbook(io.BytesIO(pathlib.Path(d.value.path()).read_bytes()), read_only=True).sheetnames
    if nomes != ["PROCESSO", "MAPA", "DOTAÇÃO ORÇAMENTÁRIA", "DOTAÇÃO POR ITEM", "LANÇAMENTOS POR EXERCÍCIO", "APURAÇÃO POR EMPRESA", "CONFERÊNCIA"]:
        f.append(f"o Mapa completo mudou: {nomes}")
    # importar de novo mantém o que foi marcado na tela
    pg.goto(url + "#/processos"); pg.wait_for_timeout(500)
    pg.set_input_files("#arquivo", str(EXEMPLO)); pg.wait_for_selector("#pSalvar", timeout=15000)
    if not pg.input_value("#pProcesso"):
        pg.fill("#pProcesso", pg.evaluate("() => banco.listar().then(l => l[0].processo)"))
    pg.click("#pSalvar"); pg.wait_for_timeout(900)
    p = pg.evaluate("() => banco.listar().then(l => ({n: l.length, s: l[0].situacao, t: l[0].tiposGrupo}))")
    if p["n"] != 1 or p["s"] != "cancelado" or p["t"].get(str(grupo)) != "investimento":
        f.append(f"a nova importação perdeu a situação ou o tipo: {p}")
    return f


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
            falhas += conferir_pedidos_do_igor(pg, url, base)

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
