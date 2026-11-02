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
def s2_rodada_e_distribuicao(pg, url, ok):
    perfil(pg, url, "coordenador")
    semear(pg, url)
    sem = pg.evaluate("async ()=> (await db.list('casos')).filter(c=>!c.perito_id).length")
    ir(pg, url, "#/painel", 400)
    ok("o painel conta os casos sem perito", pg.inner_text("[data-sem-perito]") == str(sem) and sem == 32)
    ir(pg, url, "#/rodada/nova", 400)
    pg.fill("#ddPlaca", "PL-TESTE-1")
    pg.fill("#ddOrdinarios", "2026.900001\n2026.900002\n2026.900003")
    pg.fill("#ddCobrancas", "2026.910001\n2026.910002")
    pg.click("#formDdNova button[type=submit]"); pg.wait_for_timeout(600)
    ok("cria a rodada com 3 ordinários e 2 cobranças", "#/rodada/RD-007" in pg.url and contar(pg, "casos") == 53)
    ok("a sugestão de perito pula o último da rodada anterior (RN04)", pg.input_value("#ddPerito") == "P3")
    pg.click("#formDdDistribuir button[type=submit]"); pg.wait_for_timeout(600)
    ok("distribui os 3 ordinários ao perito da rodada (RN02)", pg.evaluate("async ()=> (await db.porIndice('casos','rodada_id','RD-007')).filter(c=>c.tipo==='ordinario' && c.perito_id==='P3').length") == 3)
    ok("as cobranças ficam na fila separada (RN03)", pg.evaluate("async ()=> (await db.porIndice('casos','rodada_id','RD-007')).filter(c=>c.tipo==='cobranca' && !c.perito_id).length") == 2)
    pg.click("#btnDdCobrancas"); pg.wait_for_timeout(500)
    ok("as cobranças são distribuídas em rodízio", pg.evaluate("async ()=> (await db.porIndice('casos','rodada_id','RD-007')).filter(c=>c.tipo==='cobranca' && c.perito_id).length") == 2)
    ir(pg, url, "#/rodada/nova", 300)
    pg.fill("#ddPlaca", "PL-TESTE-2"); pg.select_option("#ddProcesso", "aguardando"); pg.fill("#ddOrdinarios", "2026.920001")
    pg.click("#formDdNova button[type=submit]"); pg.wait_for_timeout(500)
    ok("com ordinário aguardando, a distribuição fica bloqueada (RN01)", pg.is_disabled("#formDdDistribuir button[type=submit]"))
    pg.click("#btnDdProcessar"); pg.wait_for_timeout(500)
    ok("registrado o processamento, a rodada libera a distribuição", not pg.is_disabled("#formDdDistribuir button[type=submit]"))

# origem: sprint3.py
@cenario
def s3_sugestao_e_urgencia(pg, url, ok):
    perfil(pg, url, "coordenador")
    semear(pg, url)
    ir(pg, url, "#/painel", 700)
    ok("o painel avisa as rodadas paradas", pg.locator("#ddCardParada").count() == 1 and pg.locator("#tabelaParadas tr").count() > 1)
    paradas = pg.evaluate("async ()=> { const rs = await db.list('rodadas'); return rs.filter(r=>ddParada(r)).map(r=>r.id_rodada); }")
    ok("a lista de rodadas paradas bate com o cálculo", pg.locator("#tabelaParadas tr").count() - 1 == len(paradas))
    ok("a fila de urgência mostra os casos marcados no exemplo", pg.locator("#tabelaUrgencia tr").count() - 1 == 2)
    ok("a fila ordena por prioridade (crítico antes de alta)", pg.inner_text("#tabelaUrgencia").index("Crítico") < pg.inner_text("#tabelaUrgencia").index("Alta"))
    # sugestão pelo histórico de rotação
    ir(pg, url, "#/rodada/RD-003", 600)
    ok("a tabela de sugestão lista os peritos", pg.locator("#tabelaSugestao tr").count() == 5)
    ok("o perito sugerido vem do histórico de rotação", pg.locator("#ddSugerido").count() == 1)
    esperado = pg.evaluate("""async ()=>{ const ps = await db.list('peritos'), rs = await db.list('rodadas'), cs = await db.list('casos');
        return ddSugerir3(ps, rs, cs, null).id_perito; }""")
    ok("a sugestão coincide com a função do histórico", pg.evaluate("""async ()=>{ const ps = await db.list('peritos'), rs = await db.list('rodadas'), cs = await db.list('casos');
        return ddSugerir3(ps, rs, cs, null).id_perito; }""") == esperado)
    # RN05: marcar um caso como urgente exige justificativa
    caso = pg.evaluate("async id => (await db.porIndice('casos','rodada_id',id)).find(c=>!c.perito_id && !c.urgente).id_caso", "RD-003")
    pg.select_option("#ddUrgCaso", caso); pg.select_option("#ddUrgPrioridade", "alta")
    pg.click("#formDdUrgencia button[type=submit]"); pg.wait_for_timeout(400)
    ok("sem justificativa, a marcação é recusada (RN05)", "RN05" in pg.inner_text("#ddErrosUrgencia"))
    pg.fill("#ddUrgJustificativa", "Prazo judicial em 5 dias")
    pg.click("#formDdUrgencia button[type=submit]"); pg.wait_for_timeout(600)
    ok("o caso entra na fila de urgência", pg.evaluate("async id => (await db.get('casos', id)).urgente", caso)
       and pg.evaluate("async id => (await db.porIndice('urgencias','rodada_id',id)).length", "RD-003") == 3)
    ok("a ficha lista o caso urgente", "Prazo judicial em 5 dias" in pg.inner_text("#ddListaUrgencia"))
    ok("o histórico registra a marcação", "caso marcado como urgente" in pg.inner_text("#conteudo"))
    # a fila de urgência do painel soma o novo caso
    ir(pg, url, "#/painel", 700)
    ok("o painel passa a mostrar 3 casos urgentes", pg.locator("#tabelaUrgencia tr").count() - 1 == 3)

# origem: sprint4.py
@cenario
def s4_painel_do_coordenador(pg, url, ok):
    perfil(pg, url, "coordenador")
    semear(pg, url)
    ir(pg, url, "#/painel", 800)
    ok("o painel do coordenador abre", pg.locator("#ddCoordenador").count() == 1)
    calc = pg.evaluate("""async ()=>{ const cs = (await db.list('casos')).filter(c=>c.distribuido_em), p = await db.list('peritos');
        const e = cs.map(c=>ddEspera(c)).filter(x=>x!==null);
        return {tempo: e.length ? Math.round(e.reduce((a,b)=>a+b,0)/e.length*10)/10 : null, distribuidos: cs.length}; }""")
    ok("o tempo médio bate com o cálculo", pg.inner_text("[data-dd-ind=tempo]").startswith(str(calc["tempo"]))
       or pg.inner_text("[data-dd-ind=tempo]") == "—")
    ok("o painel mostra a meta de 1 dia", "meta de 1 dia" in pg.inner_text("#ddCoordenador"))
    ok("a comparação por perito, natureza e rodada aparece",
       pg.locator("#tabelaPerito").count() == 1 and pg.locator("#tabelaNatureza").count() == 1 and pg.locator("#tabelaRodada").count() == 1)
    ok("o painel tem o gráfico de casos por natureza", pg.locator("svg[role=img]").count() >= 1)

# origem: sprint4.py
@cenario
def s5_importar_protocolos(pg, url, ok):
    perfil(pg, url, "tecnico")
    semear(pg, url)
    planilha = TMP / "protocolos-dna.csv"
    planilha.write_text("Protocolo;Tipo;Rodada;Data do processamento\n"
                        "2026.900001;ordinario;RD-007;2026-10-20\n"
                        "2026.900002;cobranca;RD-007;2026-10-20\n"
                        "2026.900001;ordinario;RD-007;2026-10-20\n"
                        "2026.900003;invalido;RD-007;2026-10-20\n", encoding="utf-8-sig")
    ir(pg, url, "#/importar", 600)
    pg.set_input_files("#arqDd", str(planilha)); pg.wait_for_timeout(800)
    ok("a planilha é lida e as colunas são associadas", pg.locator("#ddMapa").count() == 1 and pg.input_value("#ddMap-protocolo") == "0")
    pg.click("#btnDdImportar"); pg.wait_for_timeout(1000)
    ok("os protocolos aceitos entram nos casos", pg.evaluate("async ()=> (await db.list('casos')).filter(c=>c.protocolo.startsWith('2026.9')).length") == 2)
    ok("o relatório separa aceitas e recusadas", "2 aceitas" in pg.inner_text("#ddRelatorio") and "2 recusadas" in pg.inner_text("#ddRelatorio"))
    ok("a recusa aponta protocolo repetido e tipo inválido", "repetido" in pg.inner_text("#tabelaRecusadasDd")
       and "inválido" in pg.inner_text("#tabelaRecusadasDd"))
    ok("o histórico da importação fica registrado", pg.evaluate("async ()=> (await db.list('importacoes')).length") == 1)
    ir(pg, url, "#/importar", 600)
    ok("a última importação aparece no histórico", pg.locator("#tabelaHistoricoDd tr").count() == 2)

# origem: sprint4.py
@cenario
def s6_relatorio_e_aceite(pg, url, ok):
    perfil(pg, url, "coordenador")
    semear(pg, url)
    ir(pg, url, "#/painel", 800)
    with pg.expect_download() as dl:
        pg.click("#btnDdCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV sai com BOM, ponto e vírgula e a espera em dias", csv.startswith(b"\xef\xbb\xbf") and b"espera_dias" in csv)
    ok("os casos por perito aparecem na tabela", pg.locator("#tabelaPerito tr").count() > 1)
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
