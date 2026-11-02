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


def esperar(pg, expr, arg=None, timeout=30):
    """Espera uma condição assíncrona. wait_for_function não serve para função
    async: ela devolve Promise (truthy) e a espera terminaria na hora."""
    fim = time.time() + timeout
    while time.time() < fim:
        if pg.evaluate(expr, arg):
            return True
        pg.wait_for_timeout(150)
    raise AssertionError("tempo esgotado: " + expr[:70])


def semear(pg, url):
    """Carrega os dados fictícios e espera a importação terminar e a página parar."""
    ir(pg, url, "#/config")
    pg.click("#btnSeed")
    esperar(pg, "async () => (await db.list('log')).some(l => l.acao === 'dados fictícios carregados')")
    pg.wait_for_timeout(300)
    pg.reload()
    pg.wait_for_function("() => typeof db !== 'undefined' && !!db.con", timeout=15000)
    esperar(pg, "async () => (await db.list('processos')).length > 0")
    pg.wait_for_timeout(200)


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
def s2_novo_pedido(pg, url, ok):
    ir(pg, url, "#/pedido/novo", 400)
    pg.fill("#pUnidade", "IML Cuiabá"); pg.fill("#pSolicitante", "Servidor Teste"); pg.fill("#pMatricula", "123456")
    pg.fill("#pValor", "2.500,00"); pg.fill("#pFinalidade", "Conserto emergencial do gerador")
    pg.fill("#pJust", "O gerador parou e o IML ficou sem energia para as câmaras frias; o conserto é urgente.")
    pg.fill("#oForn1", "Fornecedor A"); pg.fill("#oCnpj1", "11.222.333/0001-81"); pg.fill("#oValor1", "2.400,00")
    pg.fill("#oForn2", "Fornecedor B"); pg.fill("#oCnpj2", "11222333000182"); pg.fill("#oValor2", "2.600,00")   # CNPJ inválido
    pg.click("#formPedido button[type=submit]"); pg.wait_for_timeout(400)
    erros = pg.inner_text("#errosPedido")
    ok("2 orçamentos são recusados (RN01)", "RN01" in erros)
    ok("CNPJ inválido é apontado", "Orçamento 2: CNPJ inválido" in erros)
    ok("nada foi gravado", contar(pg, "processos") == 0)
    pg.fill("#oCnpj2", "44.555.666/0001-81"); pg.fill("#oForn3", "Fornecedor C"); pg.fill("#oCnpj3", "77.888.999/0001-81"); pg.fill("#oValor3", "2.550,00")
    pg.click("#formPedido button[type=submit]"); pg.wait_for_timeout(600)
    ok("com 3 orçamentos válidos, o pedido é registrado", contar(pg, "processos") == 1 and contar(pg, "orcamentos") == 3)
    ok("o pedido entra na etapa Análise da DAS (RN02)", pg.evaluate("async ()=> (await db.list('processos'))[0].etapa_atual") == "Análise da DAS")
    ok("valor gravado sem erro de centavo", pg.evaluate("async ()=> (await db.list('processos'))[0].valor_solicitado") == 2500)
    ok("etapa da DAS aberta, sem saída", pg.evaluate("async ()=> (await db.list('etapas')).filter(e=>e.saida_em===null).length") == 1)

# origem: sprint3.py
@cenario
def s3_etapas_e_linha_do_tempo(pg, url, ok):
    semear(pg, url)
    pid = pg.evaluate("async ()=> (await db.list('processos')).find(p=>p.etapa_atual==='Análise da DAS').id")
    ir(pg, url, "#/processo/" + pid, 500)
    ok("a linha do tempo mostra as 12 etapas com a atual em destaque", pg.locator(".linha-tempo li").count() == 12 and pg.locator(".etapa-atual").inner_text().startswith("2. Análise da DAS"))
    pg.click("#btnAvancar"); pg.wait_for_timeout(500)
    ok("avança para Cadastro no SICAD", pg.inner_text("#etapaAtual") == "Cadastro no SICAD")
    pg.click("#btnAvancar"); pg.wait_for_timeout(400)
    ok("sem o número SICAD não segue", "SICAD" in pg.inner_text("#errosEtapa") and pg.inner_text("#etapaAtual") == "Cadastro no SICAD")
    pg.fill("#pSicad", "SICAD-2026-777"); pg.click("#btnSicad"); pg.wait_for_timeout(400)
    pg.click("#btnAvancar"); pg.wait_for_timeout(500)
    ok("com o número SICAD, avança para a chefia", pg.inner_text("#etapaAtual") == "Aprovação da chefia")
    pg.click("#btnDevolver"); pg.wait_for_timeout(300)
    ok("devolver sem motivo é recusado", "motivo" in pg.inner_text("#errosEtapa"))
    pg.fill("#mObs", "Falta assinatura na justificativa"); pg.click("#btnDevolver"); pg.wait_for_timeout(500)
    ok("devolução volta uma etapa e marca 'devolvido'", pg.inner_text("#etapaAtual") == "Cadastro no SICAD" and "devolvido" in pg.inner_text(".linha-tempo"))
    ok("o histórico registra avanços, número SICAD e devolução", all(x in pg.inner_text("#historicoAd") for x in ("etapa avançada", "número SICAD", "processo devolvido")))
    ok("uma etapa aberta por vez", pg.evaluate("async id => (await db.porIndice('etapas','processo_id',id)).filter(e=>!e.saida_em).length", pid) == 1)

# origem: sprint4.py
@cenario
def s4_motor_de_prazos(pg, url, ok):
    semear(pg, url)
    pid = pg.evaluate("async ()=> (await db.list('processos')).find(p=>p.situacao!=='encerrado').id")
    ir(pg, url, "#/processo/" + pid, 600)
    ok("a ficha mostra o prazo com a base de contagem (RN03)", pg.locator("#adPrazo").count() == 1
       and "Base de contagem" in pg.inner_text("#adPrazo"))
    calc = pg.evaluate("""async id => { const p = await db.get('processos', id), f = await db.list('feriados');
        const r = prazosDoProcesso(p, f); return {limite: r.limite, restam: r.restam, selo: r.selo}; }""", pid)
    ok("o limite e os dias restantes batem com o motor", pg.inner_text("[data-ad-restam]") == str(calc["restam"]))
    ok("o motor considera o tipo do processo", pg.evaluate("""async id => { const p = await db.get('processos', id), f = [];
        const r = prazosDoProcesso(p, f); return r.regra.uteis === (p.tipo !== 'predial'); }""", pid))
    # feriados na configuração
    ir(pg, url, "#/config", 500)
    antes = contar(pg, "feriados")
    pg.fill("#feData", "2026-12-08"); pg.fill("#feNome", "Feriado de teste"); pg.select_option("#feEscopo", "estadual")
    pg.click("#btnAddFeriado"); pg.wait_for_timeout(600)
    ok("o feriado é acrescentado pela configuração", contar(pg, "feriados") == antes + 1
       and pg.evaluate("async ()=> (await db.get('feriados','2026-12-08')).escopo") == "estadual")
    pg.fill("#feData", "2026-12-08"); pg.fill("#feNome", "Repetido")
    pg.click("#btnAddFeriado"); pg.wait_for_timeout(400)
    ok("feriado repetido não entra duas vezes", contar(pg, "feriados") == antes + 1)

# origem: sprint4.py
@cenario
def s5_prestacao_e_pendencias(pg, url, ok):
    semear(pg, url)
    pid = pg.evaluate("async ()=> (await db.list('processos')).find(p=>p.situacao!=='encerrado' && p.valor_concedido>0).id")
    ir(pg, url, "#/processo/" + pid + "/prestacao", 600)
    ok("a prestação abre com o valor concedido e a soma das notas", pg.locator("[data-ad-concedido]").count() == 1)
    pg.fill("#noNumero", "NF-1"); pg.fill("#noCnpj", "11.222.333/0001-81"); pg.fill("#noValor", "100,00")
    pg.click("#formNota button[type=submit]")
    esperar(pg, "async () => (await db.list('notas')).length >= 1")
    ok("a nota fiscal entra na prestação", contar(pg, "notas") >= 1)
    # pendência com prazo de 10 dias úteis (RN05)
    pg.fill("#peMotivo", "Nota fiscal sem identificação do órgão")
    pg.click("#btnPendencia")
    esperar(pg, "async id => (await db.porIndice('pendencias','processo_id',id)).some(p=>!p.resolvida_em)", arg=pid)
    pend = pg.evaluate("""async id => (await db.porIndice('pendencias','processo_id',id)).find(p=>!p.resolvida_em)""", pid)
    ok("a pendência abre com prazo de 10 dias úteis (RN05)", pend and pend["prazo"])
    # encerrar com pendência aberta é recusado
    pg.select_option("#enDecisao", "aprovado sem ressalvas")
    pg.click("#formEncerrar button[type=submit]")
    esperar(pg, "() => (document.querySelector('#adErrosEncerrar')?.innerText || '').length > 0")
    ok("com pendência aberta, o encerramento é recusado", "pendência" in pg.inner_text("#adErrosEncerrar").lower())
    pg.locator("[data-resolver]").first.click()
    esperar(pg, "async id => (await db.porIndice('pendencias','processo_id',id)).every(p=>p.resolvida_em)", arg=pid)
    ok("a pendência é resolvida com a data", pg.evaluate("async id => (await db.porIndice('pendencias','processo_id',id)).every(p=>p.resolvida_em)", pid))
    # RN06: nota acima do concedido
    concedido = pg.evaluate("async id => (await db.get('processos', id)).valor_concedido", pid)
    pg.fill("#noNumero", "NF-2"); pg.fill("#noValor", f"{concedido * 2:.2f}".replace(".", ","))
    pg.click("#formNota button[type=submit]")
    esperar(pg, "() => !!document.querySelector('#adExcedeu')")
    ok("nota acima do valor concedido entra em alerta (RN06)", pg.locator("#adExcedeu").count() == 1)
    pg.select_option("#enDecisao", "aprovado com ressalvas")
    pg.click("#formEncerrar button[type=submit]")
    esperar(pg, "() => (document.querySelector('#adErrosEncerrar')?.innerText || '').includes('RN06')")
    ok("com excedente, o encerramento também é recusado", "RN06" in pg.inner_text("#adErrosEncerrar"))

# origem: sprint4.py
@cenario
def s6_painel_e_relatorio(pg, url, ok):
    semear(pg, url)
    ir(pg, url, "#/painel", 700)
    calc = pg.evaluate("""async ()=>{ const ps = await db.list('processos'), f = await db.list('feriados'), h = hojeISO();
        const i = ps.map(p=>({p, ...prazosDoProcesso(p, f, h)}));
        return {total: ps.length, vencidos: i.filter(x=>x.selo==='vencido').length, vencendo: i.filter(x=>x.selo==='vence7').length,
                encerrados: ps.filter(p=>p.situacao==='encerrado').length}; }""")
    ok("o painel conta processos, vencidos, a vencer e encerrados",
       pg.inner_text("[data-ad-ind=total]") == str(calc["total"]) and pg.inner_text("[data-ad-ind=vencidos]") == str(calc["vencidos"])
       and pg.inner_text("[data-ad-ind=vencendo]") == str(calc["vencendo"]) and pg.inner_text("[data-ad-ind=encerrados]") == str(calc["encerrados"]))
    ok("o painel tem os gráficos em SVG", pg.locator("svg[role=img]").count() == 2)
    ir(pg, url, "#/relatorio", 600)
    ok("o relatório mostra devoluções por motivo e o tempo médio", pg.locator("[data-ad-rel=devolucoes]").count() == 1
       and pg.locator("[data-ad-rel=ciclo]").count() == 1)
    with pg.expect_download() as dl:
        pg.click("#btnAdCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV do relatório sai com BOM e ponto e vírgula", csv.startswith(b"\xef\xbb\xbf") and b"id;unidade;tipo" in csv)
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
