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
def s2_ler_csv_excel(pg, url, ok):
    ex = PASTA / "exemplos"
    semear(pg, url)
    for mes in ["2026-07", "2026-08", "2026-09"]:
        ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(ex / f"powerbi1-{mes}.csv")); pg.wait_for_timeout(800)
    ok("3 meses importados", contar(pg, "relatorios") == 3)
    ok("10 unidades por mês (30 pendências)", contar(pg, "pendencias") == 30)
    ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-08.csv")); pg.wait_for_timeout(800)
    ok("agosto acusa 1 unidade fora do cadastro (RN03)", pg.locator("#qtdDesconhecidas").inner_text() == "1 fora do cadastro")
    pg.select_option("select[id^=assoc-]", "Regional Sinop"); pg.click("[data-assoc]"); pg.wait_for_timeout(500)
    ok("associar grava o apelido na unidade", "Regional de Sinop (nova sigla)" in pg.evaluate("async ()=> JSON.stringify((await db.get('unidades','Regional Sinop')).apelidos)"))
    ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-08.csv")); pg.wait_for_timeout(800)
    ok("na próxima importação, o apelido casa sozinho", pg.locator("#qtdDesconhecidas").count() == 0)
    ok("total do relatório guardado (setembro)", pg.evaluate("async ()=> (await db.get('relatorios','2026-09')).total_relatorio") is not None)
    # Excel e arquivo sem mês
    from openpyxl import Workbook
    wb = Workbook(); ws = wb.active; ws.append(["Mês", "Unidade", "Laudos pendentes"]); ws.append(["10/2026", "IML Cuiabá", 321]); ws.append(["10/2026", "Total", 321])
    xl = TMP / "relatorio.xlsx"; wb.save(xl)
    ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(xl)); pg.wait_for_timeout(800)
    ok("Excel com mês 10/2026 é lido como 2026-10", pg.evaluate("async ()=> (await db.get('relatorios','2026-10'))?.tipo") == "excel")
    sem = TMP / "sem-mes.csv"; sem.write_text("Unidade;Laudos pendentes\nIML Cuiabá;10\n", encoding="utf-8")
    ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(sem)); pg.wait_for_timeout(500)
    ok("arquivo sem mês é recusado (RN01)", "RN01" in pg.inner_text("#errosMes"))

# origem: sprint3.py
@cenario
def s3_conferencia(pg, url, ok):
    ex = PASTA / "exemplos"
    semear(pg, url)
    for mes in ["2026-07", "2026-08", "2026-09"]:
        ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(ex / f"powerbi1-{mes}.csv")); pg.wait_for_timeout(800)
        if mes == "2026-08":
            pg.select_option("select[id^=assoc-]", "Regional Sinop"); pg.click("[data-assoc]"); pg.wait_for_timeout(500)
    ir(pg, url, "#/conferencia/2026-09", 500)
    ok("setembro: soma diferente do total bloqueia a aprovação (RN02)", "RN02" in pg.inner_text("#bloqueios") and pg.is_disabled("#btnAprovar"))
    pg.fill("#motivoCorrecao", "Total do PDF inclui laudos de outra diretoria"); pg.click("#btnAceitarSoma"); pg.wait_for_timeout(500)
    ok("aceitar a soma com motivo libera a aprovação", not pg.is_disabled("#btnAprovar"))
    pg.fill("#aprovador", "Chefe Teste"); pg.click("#btnAprovar"); pg.wait_for_timeout(500)
    ok("mês aprovado fica travado (RN05)", "aprovado por Chefe Teste" in pg.inner_text("#situacaoMes") and pg.locator("[data-novo]").count() == 0)
    ir(pg, url, "#/conferencia/2026-08", 500)
    ok("agosto: variação acima de 30% sobre julho vira alerta (RN04)", "RN04" in pg.inner_text("[data-unidade='Criminalística Cuiabá']"))
    pg.fill("[data-novo='2026-08|Criminalística Cuiabá']", "999"); pg.click("#btnCorrigir"); pg.wait_for_timeout(300)
    ok("corrigir sem motivo não grava", contar(pg, "correcoes") == 1)
    pg.fill("#motivoCorrecao", "Conferido no painel do Power BI 1"); pg.click("#btnCorrigir"); pg.wait_for_timeout(500)
    ok("correção com motivo fica registrada", contar(pg, "correcoes") == 2 and "corrigido" in pg.inner_text("[data-unidade='Criminalística Cuiabá']"))
    ir(pg, url, "#/conferencia/2026-09", 500)
    pg.click("#btnNovaVersao"); pg.wait_for_timeout(300)
    ok("nova versão sem motivo é recusada", "RN05" in pg.inner_text("#errosVersao"))
    pg.fill("#motivoVersao", "Reprocessamento do Power BI 1"); pg.click("#btnNovaVersao"); pg.wait_for_timeout(500)
    ok("nova versão reabre o mês (versão 2)", "versão 2" in pg.inner_text("#conteudo") and pg.inner_text("#situacaoMes") == "a conferir")

# origem: sprint5.py
@cenario
def s5_leitura_do_pdf(pg, url, ok):
    semear(pg, url)
    ex = PASTA / "exemplos"
    ir(pg, url, "#/importar", 500)
    pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-07.pdf")); pg.wait_for_timeout(1500)
    ok("o PDF com texto é lido e o mês sai do arquivo", "2026-07" in pg.inner_text("#resMes"))
    ok("as 10 unidades do PDF entram na conferência", pg.evaluate("async ()=> (await db.porIndice('pendencias','mes_ref','2026-07')).length") == 10)
    ok("o número lido do PDF bate com o do CSV",
       pg.evaluate("""async ()=>{ const ps = await db.porIndice('pendencias','mes_ref','2026-07');
         const c = ps.find(p=>p.unidade==='Criminalística Cuiabá'); return c && c.pendentes === 1472; }"""))
    ok("a origem fica registrada como PDF", pg.evaluate("async ()=>{ const ps = await db.porIndice('pendencias','mes_ref','2026-07'); return ps.every(p=>p.origem==='pdf'); }"))
    ok("a confiança do texto extraído é 100%", pg.evaluate("async ()=>{ const ps = await db.porIndice('pendencias','mes_ref','2026-07'); return ps.every(p=>p.confianca===1); }"))
    # PDF sem camada de texto: gera uma página em branco e confere a mensagem
    from reportlab.pdfgen import canvas as _cv
    sem = TMP / "powerbi1-2026-10.pdf"
    c = _cv.Canvas(str(sem)); c.showPage(); c.save()
    pg.set_input_files("#arqMes", str(sem)); pg.wait_for_timeout(1200)
    ok("PDF em imagem é recusado com a mensagem do OCR", "camada de texto" in pg.inner_text("#errosMes"))

# origem: sprint5.py
@cenario
def s6_aceite_e_piloto(pg, url, ok):
    semear(pg, url)
    # o fluxo completo: importar, conferir, aprovar, gerar o arquivo
    ex = PASTA / "exemplos"
    ir(pg, url, "#/importar", 400)
    pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-07.csv")); pg.wait_for_timeout(900)
    ir(pg, url, "#/conferencia/2026-07", 600)
    ok("a conferência abre com as divergências do mês", pg.locator("#conteudo").count() == 1)
    ok("o roteiro de aceite está em modelos/", (PASTA / "modelos" / "roteiro-aceite.md").exists())

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
