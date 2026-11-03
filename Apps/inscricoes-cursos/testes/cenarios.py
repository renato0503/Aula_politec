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
def s2_curso_e_link(pg, url, ok):
    perfil(pg, url, "gerencia")
    semear(pg, url)
    ir(pg, url, "#/cursos")
    pg.click("#btnNovoCurso")
    pg.fill("#cNome", "Perícia em Local de Crime"); pg.fill("#cCarga", "16"); pg.fill("#cLocal", "Auditório")
    pg.fill("#cInicio", "2026-12-07"); pg.fill("#cFim", "2026-12-08"); pg.fill("#cInscIni", "2026-11-01"); pg.fill("#cInscFim", "2026-11-20")
    pg.fill("#cTriagem", "2026-11-25"); pg.fill("#cGrupo", "https://chat.exemplo/turma")
    pg.click("#formCurso button[type=submit]"); pg.wait_for_timeout(400)
    ok("curso sem vagas é recusado", "ao menos uma vaga" in pg.inner_text("#errosCurso"))
    pg.fill("#vaga-DMC", "5"); pg.fill("#vaga-DIN", "3"); pg.dispatch_event("#vaga-DIN", "input")
    ok("total de vagas soma as diretorias", pg.inner_text("#totalVagas") == "8")
    pg.click("#formCurso button[type=submit]"); pg.wait_for_timeout(600)
    ok("salvar leva à divulgação", "#/divulgar/" in pg.url)
    link = pg.inner_text("#linkInscricao")
    ok("QR Code gerado", pg.locator("#qr svg").count() == 1)
    ok("texto de divulgação com as vagas", "5 vagas" in pg.input_value("#textoDivulgacao"))
    novo = pg.context.browser.new_context(); p2 = novo.new_page()   # outro navegador, sem dados
    p2.goto(link); p2.wait_for_timeout(500)
    ok("o link abre a inscrição com o curso, sem dado prévio", "Perícia em Local de Crime" in p2.inner_text("#conteudo"))
    ok("a inscrição não mostra o menu da gerência", p2.locator("#menu").is_hidden())
    p2.goto(link[:-1] + ("1" if link.endswith("0") else "0")); p2.wait_for_timeout(300)
    ok("link alterado mostra aviso", "alterado" in p2.inner_text("#conteudo"))
    novo.close()

# origem: sprint3.py
@cenario
def s3_formulario_de_inscricao(pg, url, ok):
    perfil(pg, url, "gerencia")
    semear(pg, url)
    link = pg.evaluate("async ()=> linkInscricao(await db.get('cursos','CURSO-2026-11'))")
    fechado = pg.evaluate("async ()=>{ const c = await db.get('cursos','CURSO-2026-11'); return linkInscricao({...c, id:'X', inscricao_inicio:'2026-01-01', inscricao_fim:'2026-01-31'}); }")
    p2 = pg.context.browser.new_context().new_page()   # o servidor abre o link no próprio navegador
    p2.goto(link); p2.wait_for_timeout(500)
    p2.fill("#iMatricula", "123456"); p2.fill("#iNome", "Servidor Teste"); p2.fill("#iLotacao", "IML Cuiabá"); p2.select_option("#iDiretoria", "DML")
    p2.fill("#iEmail", "servidor@gmail.com"); p2.check("input[name=pre0][value=sim]"); p2.check("input[name=pre1][value=nao]")
    p2.click("#formInscricao button[type=submit]"); p2.wait_for_timeout(300)
    ok("e-mail fora do domínio é recusado ao lado do campo (RN02)", "RN02" in p2.inner_text("#erro-iEmail"))
    p2.fill("#iEmail", "servidor.teste@politec.mt.gov.br"); p2.click("#formInscricao button[type=submit]"); p2.wait_for_timeout(400)
    prot = p2.inner_text("#protInscricao") if p2.locator("#protInscricao").count() else ""
    ok("comprovante com protocolo e situação em análise", len(prot) == 8 and "em análise" in p2.inner_text("#cardComprovante"))
    href = p2.get_attribute("#lnkEmail", "href")
    ok("o e-mail vai para capacitacao@ com o assunto [INSCRICAO] e o protocolo", href.startswith("mailto:capacitacao%40politec.mt.gov.br") and "%5BINSCRICAO%5D" in href and prot in href)
    from urllib.parse import unquote
    corpo = unquote(href.split("body=")[1])
    lido = p2.evaluate("t => blocoInscricao.ler(t)", corpo)
    ok("o bloco do e-mail volta inteiro na leitura da gerência", len(lido) == 1 and lido[0].get("dados", {}).get("m") == "123456" and lido[0]["dados"]["p"] == prot)
    ok("pré-requisito marcado como não atendo fica de fora da declaração", lido[0]["dados"]["r"] == ["Ser servidor efetivo"])
    p2.goto(fechado); p2.wait_for_timeout(400)
    ok("fora do período a inscrição fica fechada (RN04)", p2.locator("#foraPeriodo").count() == 1 and p2.locator("#formInscricao").count() == 0)
    p2.context.close()

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
