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

# origem: sprint2.py
@cenario
def s2_fila_e_extracao(pg, url, ok):
    perfil(pg, url, "triador")
    semear(pg, url)
    ir(pg, url, "#/painel", 500)
    ok("a bancada lista os 10 e-mails", contar(pg, "emails") == 10 and pg.locator("[data-te-email]").count() == 10)
    ok("o detalhe abre com os 9 campos", pg.locator("#teDetalhe").count() == 1 and pg.locator(".te-form .campo").count() == 9)
    pg.click("[data-te-email=EM-003]"); pg.wait_for_timeout(500)
    ok("o e-mail com campo faltando não valida", pg.locator("#btnTeValidar").is_disabled())
    pg.fill("#te_protocolo", "000999/2026"); pg.click("#btnTeSalvar"); pg.wait_for_timeout(600)
    pg.click("#btnTeValidar"); pg.wait_for_timeout(600)
    ok("com os 9 campos, a requisição é validada", pg.evaluate("async () => (await db.get('emails','EM-003')).status") == "validado")
    ok("a validação entra na trilha", pg.evaluate("async () => (await db.list('log')).some(l=>l.acao==='requisição validada' && String(l.detalhe).startsWith('EM-003'))"))

# origem: sprint3.py
@cenario
def s3_divergencia_e_ocr(pg, url, ok):
    perfil(pg, url, "triador")
    semear(pg, url)
    ir(pg, url, "#/painel", 500)
    pg.click("[data-te-email=EM-004]"); pg.wait_for_timeout(500)
    ok("a divergência bloqueia a validação", pg.locator("#btnTeValidar").is_disabled() and pg.locator("#btnTeAlerta").count() == 1)
    pg.click("#btnTeAlerta"); pg.wait_for_timeout(500)
    pg.click("#btnTeValidar"); pg.wait_for_timeout(500)
    ok("tratar o alerta libera a validação", pg.evaluate("async () => (await db.get('emails','EM-004')).status") == "validado")
    pg.click("[data-te-email=EM-005]"); pg.wait_for_timeout(500)
    ok("o PDF imagem entra como leitura manual", "PDF sem texto" in pg.inner_text("#teDetalhe") and pg.locator("#btnTeAlerta").count() == 1)
    pg.fill("#te_objetivo_claro", "Confronto de amostra biológica para o inquérito."); pg.click("#btnTeSalvar"); pg.wait_for_timeout(500)
    pg.click("#btnTeAlerta"); pg.wait_for_timeout(500)
    pg.click("#btnTeValidar"); pg.wait_for_timeout(500)
    ok("depois da leitura manual, o e-mail é validado", pg.evaluate("async () => (await db.get('emails','EM-005')).status") == "validado")

# origem: sprint4.py
@cenario
def s4_lote_e_planilha(pg, url, ok):
    perfil(pg, url, "triador")
    semear(pg, url)
    ir(pg, url, "#/lote", 500)
    pg.click("[data-te-lote=LT-001]"); pg.wait_for_timeout(1000)
    ok("o lote grava a extração dos e-mails", contar(pg, "extracao") >= 5)
    ir(pg, url, "#/planilha", 500)
    ok("a planilha traz os 10 e-mails e os 9 campos", pg.locator("#tabelaTeia tr").count() == 11 and pg.locator("#tabelaTeia th").count() == 12)
    with pg.expect_download() as dl:
        pg.click("#btnTeCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV sai com BOM e os campos", csv.startswith(b"\xef\xbb\xbf") and b"data_cobranca" in csv and b"protocolo" in csv)


@cenario
def s5_feedback_campos_e_reiteracao(pg, url, ok):
    perfil(pg, url, "triador")
    semear(pg, url)
    ir(pg, url, "#/painel", 600)
    pg.click("[data-te-email=EM-001]"); pg.wait_for_timeout(600)
    ok("a ficha tem vítima, investigado e réu preso",
       pg.locator("#te_nome_vitima").count() == 1 and pg.locator("#te_nome_investigado").count() == 1 and pg.locator("#te_reu_preso").count() == 1)
    ok("Nível e Nº da cobrança saíram", pg.locator("#te_nivel").count() == 0 and pg.locator("#te_numero_cobranca").count() == 0)
    ok("o protocolo está no formato nnnnnn/aaaa",
       bool(pg.evaluate("/^\\d{6}\\/\\d{4}$/.test(document.getElementById('te_protocolo').value)")))
    ok("a data da cobrança é a data do e-mail",
       pg.evaluate("async () => document.getElementById('te_data_cobranca').value === (await db.get('emails','EM-001')).recebido_em.slice(0,10)"))
    ok("a lista de regionais é a do feedback", pg.locator("#te_regional option").count() >= 30)
    pg.click("#btnTeExtrair"); pg.wait_for_timeout(700)
    ok("a cobrança reiterada gera alerta",
       pg.evaluate("async () => (await db.get('emails','EM-001')).alerta") == "reiteracao")
    ok("o alerta aparece na ficha", "reiterada" in pg.inner_text("#teDetalhe"))
    pg.click("#btnTeAlerta"); pg.wait_for_timeout(500)
    pg.click("#btnTeValidar"); pg.wait_for_timeout(600)
    ok("depois de tratar, a requisição é validada",
       pg.evaluate("async () => (await db.get('emails','EM-001')).status") == "validado")


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

