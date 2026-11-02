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
def s2_registro_e_etapas(pg, url, ok):
    perfil(pg, url, "compras")
    semear(pg, url)
    atras = pg.evaluate("async ()=> (await db.list('processos')).filter(p=>caAtrasado(p)).length")
    ir(pg, url, "#/painel", 400)
    ok("o painel conta os processos fora do prazo", pg.inner_text("[data-atrasados]") == str(atras) and atras > 0)  # o número muda com a data de hoje
    ir(pg, url, "#/processo/novo", 400)
    pg.fill("#caSigadoc", "2026.1000-SD"); pg.fill("#caSiag", "SIAG-TESTE"); pg.fill("#caUnidade", "Aquisições"); pg.fill("#caResponsavel", "Servidor Teste"); pg.fill("#caObjeto", "Objeto de teste")
    pg.select_option("#caDFD", "nao")
    pg.click("#formCaNovo button[type=submit]"); pg.wait_for_timeout(400)
    ok("SIGADOC repetido é recusado (RN01)", "já está cadastrado" in pg.inner_text("#caErros") and contar(pg, "processos") == 10)
    pg.fill("#caSigadoc", "2026.9999-SD")
    pg.click("#formCaNovo button[type=submit]"); pg.wait_for_timeout(600)
    ok("registra a aquisição na etapa DFD", "#/processo/AQ-0011" in pg.url and pg.evaluate("async ()=> (await db.get('processos','AQ-0011')).etapa") == "DFD")
    pg.click("#btnCaAvancar"); pg.wait_for_timeout(400)
    ok("sem o DFD não avança da etapa (RN02)", "Anexe antes de avançar" in pg.inner_text("#caErrosPend") and pg.evaluate("async ()=> (await db.get('processos','AQ-0011')).etapa") == "DFD")
    pg.select_option("#caTipo", "DFD"); pg.fill("#caNome", "DFD-teste.pdf"); pg.click("#formCaDoc button[type=submit]"); pg.wait_for_timeout(500)
    ok("o documento anexado entra na ficha", "DFD-teste.pdf" in pg.inner_text("#conteudo"))
    pg.click("#btnCaAvancar"); pg.wait_for_timeout(500)
    ok("com o documento, avança para o ETP", pg.evaluate("async ()=> (await db.get('processos','AQ-0011')).etapa") == "ETP")
    pg.select_option("#caMotivo", "Documento incompleto"); pg.click("#btnCaPend"); pg.wait_for_timeout(500)
    pg.select_option("#caTipo", "ETP"); pg.fill("#caNome", "ETP-teste.pdf"); pg.click("#formCaDoc button[type=submit]"); pg.wait_for_timeout(500)
    pg.click("#btnCaAvancar"); pg.wait_for_timeout(400)
    ok("pendência aberta impede avançar (RN03)", "pendência" in pg.inner_text("#caErrosPend") and pg.evaluate("async ()=> (await db.get('processos','AQ-0011')).etapa") == "ETP")

# origem: sprint3.py
@cenario
def s3_pesquisa_de_precos(pg, url, ok):
    perfil(pg, url, "compras")
    semear(pg, url)
    ir(pg, url, "#/processo/AQ-0001", 500)
    ok("o exemplo já traz duas pesquisas do mesmo objeto", pg.evaluate("async ()=> (await db.porIndice('pesquisas','processo_id','AQ-0001')).length") == 2)
    ok("a ficha mostra as duas pesquisas", pg.locator("#caHistoricoPrecos > .card").count() == 2)
    ok("a pesquisa com o cotado 40% acima entra em alerta", "Alerta:" in pg.inner_text("#caHistoricoPrecos"))
    # RN04: sem três cotações, a pesquisa é recusada
    pg.fill("#caPesqEstimado", "10000")
    pg.fill("#caCotFornecedor1", "Fornecedor A"); pg.fill("#caCotValor1", "10000")
    pg.click("#formCaPesquisa button[type=submit]"); pg.wait_for_timeout(400)
    ok("sem três cotações, a pesquisa é recusada (RN04)", "RN04" in pg.inner_text("#caErrosPesquisa")
       and pg.evaluate("async ()=> (await db.list('pesquisas')).length") == 2)
    # com três cotações dentro da tolerância, a pesquisa entra sem alerta
    pg.fill("#caPesqEstimado", "10000")
    for k, v in ((1, "10000"), (2, "10200"), (3, "9800")):
        pg.fill(f"#caCotFornecedor{k}", f"Fornecedor {k}"); pg.fill(f"#caCotValor{k}", v); pg.fill(f"#caCotData{k}", "2026-10-20")
    pg.click("#formCaPesquisa button[type=submit]"); pg.wait_for_timeout(600)
    ok("com três cotações, a pesquisa é registrada", pg.evaluate("async ()=> (await db.list('pesquisas')).length") == 3)
    ok("a nova pesquisa não entra em alerta", pg.evaluate("async ()=> { const q = (await db.list('pesquisas')).sort((a,b)=>a.data_hora.localeCompare(b.data_hora)).at(-1); return !caAlertaEstimado(q); }"))
    # com cotado 40% acima, entra em alerta
    pg.fill("#caPesqEstimado", "10000")
    for k, v in ((1, "14000"), (2, "14000"), (3, "14000")):
        pg.fill(f"#caCotFornecedor{k}", f"Fornecedor {k}"); pg.fill(f"#caCotValor{k}", v)
    pg.click("#formCaPesquisa button[type=submit]"); pg.wait_for_timeout(600)
    ok("o cotado 40% acima do estimado entra em alerta", pg.evaluate("async ()=> { const q = (await db.list('pesquisas')).sort((a,b)=>a.data_hora.localeCompare(b.data_hora)).at(-1); return caAlertaEstimado(q); }")
       and "Alerta:" in pg.inner_text("#caHistoricoPrecos"))
    # histórico por objeto
    ir(pg, url, "#/precos", 600)
    ok("o histórico mostra o objeto com as quatro pesquisas", pg.locator("#tabelaHistoricoPrecos tr").count() == 2)
    linha = pg.inner_text("#tabelaHistoricoPrecos")
    ok("o histórico compara a primeira e a última média", "notebooks" in linha.lower() and "%" in linha)
    ok("o histórico leva ao processo", "AQ-0001" in pg.inner_text("#tabelaHistoricoPrecos"))

# origem: sprint4.py
@cenario
def s4_aprovacoes_e_modalidade(pg, url, ok):
    perfil(pg, url, "compras")
    semear(pg, url)
    pid = pg.evaluate("async ()=> (await db.list('processos')).find(p=>p.status!=='concluido').id_processo")
    ir(pg, url, "#/processo/" + pid, 700)
    ok("a ficha mostra a trilha de aprovação com as três análises", pg.locator("#caAprovacoes").count() == 1
       and pg.locator("#caAprovacoes .check-lista li").count() == 3)
    pg.fill("#caApParecer", "curto")
    pg.click("#formCaAprovacao button[type=submit]"); pg.wait_for_timeout(400)
    ok("parecer curto é recusado", "20 caracteres" in pg.inner_text("#caErrosAprovacao"))
    pg.select_option("#caApTipo", "tecnica"); pg.fill("#caApSetor", "Aquisições")
    pg.fill("#caApParecer", "Análise técnica favorável, com o objeto e as quantidades conferidos.")
    pg.click("#formCaAprovacao button[type=submit]"); pg.wait_for_timeout(700)
    ok("a análise é registrada com setor, perfil e data", pg.evaluate("async id => { const a = (await db.porIndice('aprovacoes','processo_id',id))[0]; return a && a.tipo==='tecnica' && a.setor==='Aquisições' && a.perfil; }", pid))
    ok("o histórico registra a análise", pg.evaluate("async id => (await db.list('log')).some(l=>l.processo_id===id && /análise registrada/.test(l.acao))", pid))
    # modalidade
    pg.select_option("#caMod", "Pregão eletrônico"); pg.select_option("#caCrit", "Menor preço")
    pg.click("#formCaModalidade button[type=submit]"); pg.wait_for_timeout(700)
    ok("a modalidade e o critério ficam registrados", pg.evaluate("async id => { const p = await db.get('processos', id); return p.modalidade==='Pregão eletrônico' && p.criterio_julgamento==='Menor preço'; }", pid))

# origem: sprint4.py
@cenario
def s5_painel_do_gestor(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    ir(pg, url, "#/painel", 800)
    calc = pg.evaluate("""async ()=>{ const ps = await db.list('processos'), l = await db.list('log'), pe = await db.list('pendencias'), h = hojeISO();
        const ativos = ps.filter(p=>p.status!=='concluido');
        return {ativos: ativos.length, parados: ps.filter(p=>caParado(p, l, h)).length, retrabalho: pe.length}; }""")
    ok("o painel conta ativos, parados e retrabalho", pg.inner_text("[data-ca-ind=ativos]") == str(calc["ativos"])
       and pg.inner_text("[data-ca-ind=parados]") == str(calc["parados"])
       and pg.inner_text("[data-ca-ind=retrabalho]") == str(calc["retrabalho"]))
    ok("o painel tem os gráficos de etapa e de tempo por etapa", pg.locator("svg[role=img]").count() == 2)
    ok("o painel agrupa pendências por unidade e por responsável", pg.locator("#tabelaUnidade").count() == 1 and pg.locator("#tabelaResp").count() == 1)
    ok("o painel lista os processos parados", pg.locator("#tabelaParados").count() == 1)

# origem: sprint4.py
@cenario
def s6_relatorio_e_aceite(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    ir(pg, url, "#/painel", 800)
    ok("o painel mostra o prazo médio dos concluídos", pg.locator("[data-ca-ind=prazo]").count() == 1)
    with pg.expect_download() as dl:
        pg.click("#btnCaCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV sai com BOM, ponto e vírgula e as colunas de atraso/parado",
       csv.startswith(b"\xef\xbb\xbf") and b"id;sigadoc;siag" in csv and b"parado" in csv)
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
