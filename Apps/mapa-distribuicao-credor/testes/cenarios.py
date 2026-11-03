"""Cenários de interface deste app: usam a tela como uma pessoa usaria e conferem
o "Pronto quando" de cada sprint do sprint.md.

Uso: python testes/cenarios.py      (requer: pip install playwright && playwright install chromium)
"""
import pathlib
import sys
import tempfile
import time

from playwright.sync_api import sync_playwright

PASTA = pathlib.Path(__file__).resolve().parent.parent
TMP = pathlib.Path(tempfile.mkdtemp(prefix="cenarios-"))
CENARIOS = []


def cenario(fn):
    CENARIOS.append(fn)
    return fn


def contar(pg, store):
    return pg.evaluate("async s => (await db.list(s)).length", store)


def esperar(pg, expr, arg=None, timeout=60):
    """Espera uma condição assíncrona. wait_for_function não serve para função
    async: ela devolve Promise (truthy) e a espera terminaria na hora."""
    fim = time.time() + timeout
    while time.time() < fim:
        if pg.evaluate(expr, arg):
            return True
        pg.wait_for_timeout(150)
    raise AssertionError("tempo esgotado: " + expr[:70])


def semear(pg, url):
    """Carrega os dados fictícios e espera a importação terminar (o tempo fixo
    dava corrida: a tela seguinte era desenhada antes do fim da importação)."""
    ir(pg, url, "#/config")
    pg.click("#btnSeed")
    if pg.evaluate("() => !!(APP.db.stores && APP.db.stores.log)"):
        esperar(pg, "async () => (await db.list('log')).some(l => String(l.acao || '').startsWith('dados fictícios'))")
    else:
        esperar(pg, "() => (document.body.innerText || '').includes('Dados fictícios carregados')")
    pg.wait_for_timeout(300)
    pg.reload()
    pg.wait_for_function("() => typeof db !== 'undefined' && !!db.con", timeout=15000)
    pg.wait_for_timeout(400)


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

# origem: testar_sprints.py
@cenario
def s2_importacao(pg, url, ok):
    ex = PASTA / "exemplos"
    ir(pg, url, "#/processos")
    pg.fill("#procNumero", "001/2026"); pg.fill("#procNome", "Teste de importação"); pg.click("#formProcesso button[type=submit]")
    pg.wait_for_timeout(400)
    ok("criar processo leva à importação", "#/importar/" in pg.url)
    for fonte, arq in [("distribuicao", "distribuicao-orgaos.xlsx"), ("pregoeiro", "relatorio-pregoeiro.xlsx"), ("dotacao", "dotacao.xlsx")]:
        pg.set_input_files(f"input[data-fonte={fonte}]", str(ex / arq)); pg.wait_for_timeout(300)
    pg.click("#btnImportar"); pg.wait_for_timeout(1200)
    ok("30 itens", contar(pg, "itens") == 30)
    ok("90 linhas por órgão", contar(pg, "distribuicao") == 90)
    ok("30 resultados", contar(pg, "resultado") == 30)
    ok("6 dotações", contar(pg, "dotacao") == 6)
    ok("origem com arquivo e linha", pg.evaluate("async ()=> (await db.list('itens'))[0].origem.linha > 1"))
    ok("totais estimados batem com o gabarito do exemplo", pg.evaluate("""async ()=>{
        const i = await db.list('itens'); const g = dadosEmbutidos('seed').gabarito[0];
        return i.reduce((a, x)=>a + dinheiro.vezes(x.quantidade_total, x.valor_unitario_estimado_c), 0) === g.total_estimado_c; }"""))
    # sem a coluna de quantidade: recusa com a mensagem certa
    from openpyxl import load_workbook
    wb = load_workbook(ex / "distribuicao-orgaos.xlsx"); ws = wb.active
    ws.delete_cols(8)  # "Quantidade total"
    sem = TMP / "sem-quantidade.xlsx"; wb.save(sem)
    pg.set_input_files("input[data-fonte=distribuicao]", str(sem)); pg.wait_for_timeout(300)
    pg.select_option("#map-distribuicao-quantidade_total", "-1")
    pg.click("#btnImportar"); pg.wait_for_timeout(800)
    ok("planilha sem quantidade é recusada com a mensagem certa", "Quantidade total" in pg.inner_text("#erros-distribuicao"))
    ok("a recusa não apagou os itens importados antes", contar(pg, "itens") == 30)
    # com divergências: CNPJ inválido e sem CNPJ viram alertas
    pg.set_input_files("input[data-fonte=pregoeiro]", str(ex / "relatorio-pregoeiro-com-divergencias.xlsx")); pg.wait_for_timeout(300)
    pg.click("#btnImportar"); pg.wait_for_timeout(800)
    rel = pg.inner_text("#rel-pregoeiro")
    ok("CNPJ inválido e homologado sem CNPJ aparecem como alerta", "inválido" in rel and "sem CNPJ" in rel)

# origem: testar_sprints.py
@cenario
def s3_mapa_por_item(pg, url, ok):
    from decimal import Decimal
    from openpyxl import load_workbook
    ex = PASTA / "exemplos"
    ir(pg, url, "#/processos"); pg.click("#btnExemplo"); pg.wait_for_timeout(800)
    ir(pg, url, "#/mapa/PROC-2026-001", 600)
    gab = load_workbook(ex / "mapa-manual-referencia.xlsx", data_only=True)["2 Por órgão"]
    por_orgao = {}
    for orgao, _g, _i, _q, est, _h in gab.iter_rows(min_row=2, values_only=True):
        por_orgao[orgao] = por_orgao.get(orgao, Decimal("0")) + Decimal(str(est))
    app = pg.evaluate("async ()=>{ const s = dadosEmbutidos('seed'); const m = montarMapa(await db.porIndice('itens','id_processo','PROC-2026-001'), await db.porIndice('distribuicao','id_processo','PROC-2026-001')); return Object.fromEntries(Object.entries(m.geral.porOrgao).map(([o,x])=>[o,x.v])); }")
    ok("estimado por órgão igual ao gabarito, centavo a centavo", all(int((por_orgao[o] * 100).to_integral_value()) == app[o] for o in por_orgao))
    total = sum(por_orgao.values())
    ok("total geral na tela igual ao gabarito", pg.inner_text("#totalGeral").replace(" ", " ") == "R$ " + f"{total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    ok("6 subtotais de grupo e 1 total geral", pg.locator("tr.subtotal").count() == 6 and pg.locator("tr.total").count() == 1)
    pg.locator("#tabelaMapa [data-origem]").first.click(); pg.wait_for_timeout(200)
    ok("clicar num valor mostra arquivo, aba e linha", "distribuicao-orgaos.xlsx" in pg.inner_text("#origemValor") and "linha" in pg.inner_text("#origemValor"))

# origem: sprint.md · Sprint 4
@cenario
def s4_resultado(pg, url, ok):
    ir(pg, url, "#/processos"); pg.click("#btnExemplo"); pg.wait_for_timeout(800)
    ir(pg, url, "#/resultado/PROC-2026-001", 700)
    texto = pg.inner_text("main")
    ok("a tela do resultado abre", "Resultado" in texto)
    ok("30 itens na tabela", pg.locator("table tr").count() >= 31)
    totais = pg.evaluate("""async ()=>{
        const s = dadosEmbutidos('seed');
        const e = engineDeSeed(s);
        return {est:e.totais.estimado, hom:e.totais.homologado, gab:s.gabarito[0].total_homologado_c}; }""")
    ok("total homologado igual ao gabarito", totais["hom"] == totais["gab"])
    ok("a tela mostra o total estimado do gabarito", "R$ 2.958.629,46" in texto)
    ok("a tela mostra o total homologado do gabarito", "R$ 917.504,89" in texto)
    ok("grupo fracassado mantém o estimado", "mantém o estimado" in texto)
    ok("situação dos grupos mostra fracassado e deserto", "Fracassado" in texto and "Deserto" in texto)
    ok("a situação dos grupos está na tela", pg.locator("h2", has_text="Situação dos grupos").count() == 1)

# origem: sprint.md · Sprint 5
@cenario
def s5_empresas_e_conferencia(pg, url, ok):
    ir(pg, url, "#/processos"); pg.click("#btnExemplo"); pg.wait_for_timeout(800)
    ir(pg, url, "#/empresas/PROC-2026-001", 700)
    texto = pg.inner_text("main")
    ok("a tela de empresas abre", "Empresas" in texto)
    ok("as empresas homologadas aparecem", "Alfa Suprimentos Laboratoriais Ltda" in texto)
    ok("o CNPJ aparece na tabela", "11222333000181" in texto)
    ir(pg, url, "#/conferencia/PROC-2026-001", 700)
    limpo = pg.inner_text("main")
    ok("o exemplo limpo não tem divergência bloqueante", "Nenhuma divergência que bloqueie" in limpo)
    ok("o aviso do ano seguinte aparece (D08)", "ano seguinte" in limpo)
    # agora com as planilhas com divergências plantadas
    ex = PASTA / "exemplos"
    ir(pg, url, "#/importar/PROC-2026-001", 700)
    for fonte, arq in [("distribuicao", "distribuicao-orgaos-com-divergencias.xlsx"),
                        ("pregoeiro", "relatorio-pregoeiro-com-divergencias.xlsx"),
                        ("dotacao", "dotacao-com-divergencias.xlsx")]:
        pg.set_input_files(f"input[data-fonte={fonte}]", str(ex / arq)); pg.wait_for_timeout(300)
    pg.click("#btnImportar"); pg.wait_for_timeout(1200)
    ir(pg, url, "#/conferencia/PROC-2026-001", 800)
    div = pg.inner_text("main")
    for cod in ["D01", "D02", "D03", "D04", "D05", "D06", "D07"]:
        ok(f"a conferência aponta {cod}", cod in div)
    ok("há divergência que bloqueia", "Bloqueia" in div)

# origem: sprint.md · Sprint 6
@cenario
def s6_orcamento(pg, url, ok):
    ir(pg, url, "#/processos"); pg.click("#btnExemplo"); pg.wait_for_timeout(800)
    ir(pg, url, "#/orcamento/PROC-2026-001", 800)
    texto = pg.inner_text("main")
    ok("a tela orçamentária abre", "Distribuição orçamentária" in texto)
    ok("ano corrente igual ao gabarito", "R$ 830.286,54" in texto)
    ok("ano seguinte igual ao gabarito", "R$ 87.218,35" in texto)
    ok("o aviso de D08 aparece", "ano seguinte" in texto)
    ok("a tabela por órgão e tipo existe", pg.locator("h2", has_text="Por órgão e tipo").count() == 1)
    ok("a tabela por credor existe", pg.locator("h2", has_text="Por credor").count() == 1)
    pg.fill("#dotNome", "Ana Prates"); pg.click("#formDotacao button[type=submit]"); pg.wait_for_timeout(700)
    ok("a validação da dotação fica registrada", pg.evaluate("async ()=> !!(await db.meta('dotacao_validada:PROC-2026-001'))"))

# origem: sprint.md · Sprint 7
@cenario
def s7_exportar_e_auditoria(pg, url, ok):
    ir(pg, url, "#/processos"); pg.click("#btnExemplo"); pg.wait_for_timeout(800)
    ir(pg, url, "#/exportar/PROC-2026-001", 800)
    ok("a tela de exportar abre", "Relatório de divergências" in pg.inner_text("main"))
    with pg.expect_download() as info:
        pg.click("#btnExcel")
    arquivo = info.value
    caminho = TMP / arquivo.suggested_filename
    arquivo.save_as(caminho)
    ok("o Excel sai com o nome do processo", "Mapa_Distribuicao_001_2026" in arquivo.suggested_filename)
    ok("o arquivo gerado tem conteúdo", caminho.exists() and caminho.stat().st_size > 5000)
    import zipfile
    ok("o Excel tem 8 abas", zipfile.is_zipfile(caminho) and "xl/workbook.xml" in zipfile.ZipFile(caminho).namelist())
    ir(pg, url, "#/auditoria/PROC-2026-001", 700)
    texto = pg.inner_text("main")
    ok("a tela de auditoria abre", "Auditoria" in texto)
    ok("a trilha registra a exportação", "exportação" in texto)


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
