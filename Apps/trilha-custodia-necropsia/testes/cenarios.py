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
def s2_acionamento_marcos_e_lacres(pg, url, ok):
    perfil(pg, url, "tecnico")
    semear(pg, url)
    ir(pg, url, "#/painel", 400)
    ok("o painel conta os corpos em custódia", pg.inner_text("[data-em-custodia]") == "5" and contar(pg, "corpos") == 12)
    ir(pg, url, "#/corpo/novo", 400)
    ok("o protocolo é gerado no acionamento (RN01)", pg.input_value("#tcProt") == "NEC-2026-013")
    pg.fill("#tcOrigem", "Delegacia de Teste"); pg.fill("#tcNat", "local de crime"); pg.fill("#tcMun", "Cuiabá")
    pg.fill("#tcTec", "Técnico Teste"); pg.fill("#tcLocal", "Rua Fictícia, 10")
    pg.uncheck("#tcDesc"); pg.fill("#tcNome", "Vítima Fictícia Teste")
    pg.click("#formTcNovo button[type=submit]"); pg.wait_for_timeout(600)
    ok("registra o corpo identificado em custódia", "#/corpo/C-0013" in pg.url and pg.inner_text("#tcSitAtual") == "em custódia")
    ir(pg, url, "#/corpo/novo", 300)
    pg.fill("#tcOrigem", "X"); pg.fill("#tcNat", "Y"); pg.fill("#tcMun", "Z"); pg.fill("#tcTec", "W"); pg.fill("#tcLocal", "L"); pg.fill("#tcNome", "N")
    pg.fill("#tcProt", "NEC-2026-001"); pg.click("#formTcNovo button[type=submit]"); pg.wait_for_timeout(400)
    ok("protocolo repetido é recusado (RN01)", "já está registrado" in pg.inner_text("#tcErros") and contar(pg, "corpos") == 13)
    ir(pg, url, "#/corpo/C-0013", 500)
    pg.select_option("#tcMarco", "Saída da base"); pg.click("#btnTcMarco"); pg.wait_for_timeout(500)
    ok("o marco entra na linha do tempo (RN03)", "1/4" in pg.inner_text("#conteudo") and pg.evaluate("async ()=> (await db.porIndice('marcos','corpo_id','C-0013')).length") == 1)
    pg.fill("#tcLacre", "LC-TESTE-1"); pg.fill("#tcDestino", "Laboratório de DNA"); pg.click("#btnTcLacre"); pg.wait_for_timeout(500)
    ok("o lacre fica registrado com perfil e data", pg.evaluate("async ()=> (await db.porIndice('lacres','corpo_id','C-0013'))[0].perfil") == "tecnico")
    pg.select_option("#tcNovaSit", "liberado"); pg.uncheck("#tcIdent"); pg.click("#btnTcSit"); pg.wait_for_timeout(400)
    ok("sem identificação e auto, a liberação é recusada (RN02)", "RN02" in pg.inner_text("#tcErrosSit"))
    pg.check("#tcIdent"); pg.fill("#tcResp", "Responsável Teste"); pg.fill("#tcDocEntrega", "AUTO-TESTE")
    pg.click("#btnTcSit"); pg.wait_for_timeout(500)
    ok("com identificação e auto, o corpo é liberado", pg.inner_text("#tcSitAtual") == "liberado")
    ir(pg, url, "#/busca", 400); pg.fill("#tcBusca", "NEC-2026-013"); pg.click("#btnTcBuscar"); pg.wait_for_timeout(500)
    ok("a busca acha o corpo pelo protocolo (RN04)", "NEC-2026-013" in pg.inner_text("#tcResultado"))

# origem: sprint3.py
@cenario
def s3_situacao_identificacao_e_busca(pg, url, ok):
    perfil(pg, url, "plantonista")
    semear(pg, url)
    ir(pg, url, "#/painel", 500)
    nomes = pg.evaluate("async ()=> (await db.list('corpos')).filter(c=>c.nome).map(c=>c.nome)")
    txt = pg.inner_text("#tcTabelaPainel")
    ok("o painel não mostra nome completo, só as iniciais (RN05)", nomes and not any(n in txt for n in nomes) and "M. F. S" in txt)
    ir(pg, url, "#/corpos", 400)
    ok("a lista de corpos também usa iniciais (RN05)", not any(n in pg.inner_text("#conteudo") for n in nomes))
    cid = pg.evaluate("async ()=> (await db.list('corpos')).find(c=>c.situacao==='aguardando identificação').id_corpo")
    ir(pg, url, "#/corpo/" + cid, 500)
    pg.select_option("#tcNovaSit", "não identificado"); pg.click("#btnTcSit"); pg.wait_for_timeout(400)
    ok("não identificado sem motivo é recusado", "motivo" in pg.inner_text("#tcErrosSit"))
    pg.fill("#tcMotivo", "30 dias sem identificação"); pg.click("#btnTcSit"); pg.wait_for_timeout(500)
    ok("muda para não identificado com motivo no histórico", pg.inner_text("#tcSitAtual") == "não identificado" and "30 dias" in pg.inner_text("#tcHistSit"))
    pg.select_option("#tcNovaSit", "em custódia"); pg.click("#btnTcSit"); pg.wait_for_timeout(400)
    ok("em custódia exige identificação", "identificado" in pg.inner_text("#tcErrosSit"))
    pg.check("#tcIdent"); pg.fill("#tcIdNome", "Pessoa Fictícia Identificada"); pg.fill("#tcIdDoc", "DOC-TESTE-9")
    pg.click("#btnTcSit"); pg.wait_for_timeout(400)
    ok("identificação sem método é recusada", "método" in pg.inner_text("#tcErrosSit"))
    pg.select_option("#tcIdMetodo", "papiloscopia"); pg.click("#btnTcSit"); pg.wait_for_timeout(500)
    c = pg.evaluate("async id => await db.get('corpos', id)", cid)
    ok("identifica e volta a em custódia", c["identificado"] and c["nome"] == "Pessoa Fictícia Identificada" and c["situacao"] == "em custódia" and c["metodo_identificacao"] == "papiloscopia")
    pg.select_option("#tcNovaSit", "não reclamado"); pg.fill("#tcMotivo", "Edital publicado"); pg.click("#btnTcSit"); pg.wait_for_timeout(500)
    ok("identificado sem família vira não reclamado", pg.inner_text("#tcSitAtual") == "não reclamado")
    ir(pg, url, "#/busca", 400); pg.fill("#tcBusca", "DOC-TESTE-9"); pg.press("#tcBusca", "Enter"); pg.wait_for_timeout(500)
    ok("a busca acha pelo documento (RN04)", "Pessoa Fictícia Identificada" in pg.inner_text("#tcResultado"))
    lac = pg.evaluate("async ()=> (await db.list('lacres'))[0]")
    pg.fill("#tcBusca", lac["codigo"]); pg.press("#tcBusca", "Enter"); pg.wait_for_timeout(500)
    prot = pg.evaluate("async id => (await db.get('corpos', id)).protocolo", lac["corpo_id"])
    ok("a busca acha pelo código do lacre", prot in pg.inner_text("#tcResultado"))
    pg.fill("#tcBusca", "maria souza"); pg.press("#tcBusca", "Enter"); pg.wait_for_timeout(500)
    ok("a busca por nome aceita palavras fora de ordem", "Maria Fictícia Souza" in pg.inner_text("#tcResultado"))

# origem: sprint4.py
@cenario
def s4_auto_de_entrega(pg, url, ok):
    perfil(pg, url, "plantonista")
    semear(pg, url)
    # corpo identificado e em custódia
    cid = pg.evaluate("async ()=> (await db.list('corpos')).find(c=>c.identificado && c.situacao!=='liberado').id_corpo")
    ir(pg, url, "#/corpo/" + cid, 700)
    ok("a ficha mostra o bloco do auto de entrega", pg.locator("#tcLiberacao").count() == 1)
    pg.fill("#tcAutoResp", ""); pg.fill("#tcAutoDoc", "")
    pg.click("#formTcAuto button[type=submit]"); pg.wait_for_timeout(600)
    ok("sem responsável e documento, a liberação é recusada (RN02)", "responsável" in pg.inner_text("#tcErrosAuto"))
    pg.fill("#tcAutoResp", "Familiar Fictício"); pg.fill("#tcAutoDoc", "AUTO-TESTE-1")
    pg.click("#formTcAuto button[type=submit]"); pg.wait_for_timeout(900)
    ok("com o auto completo, o corpo é liberado", pg.evaluate("async id => (await db.get('corpos', id)).situacao === 'liberado'", cid))
    ok("a liberação entra na trilha do caso", pg.evaluate("async id => (await db.list('log')).some(l=>l.corpo_id===id && l.acao==='liberação registrada')", cid))
    # corpo não identificado: bloqueado
    cid2 = pg.evaluate("async ()=> (await db.list('corpos')).find(c=>!c.identificado).id_corpo")
    ir(pg, url, "#/corpo/" + cid2, 700)
    ok("corpo sem identificação tem o botão de liberar bloqueado", pg.is_disabled("#formTcAuto button[type=submit]"))

# origem: sprint4.py
@cenario
def s5_painel_do_gestor(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    ir(pg, url, "#/painel", 900)
    ok("o painel do gestor mostra os três tempos", pg.locator("[data-tc-ind=remocao]").count() == 1
       and pg.locator("[data-tc-ind=identificacao]").count() == 1 and pg.locator("[data-tc-ind=liberacao]").count() == 1)
    calc = pg.evaluate("""async ()=>{ const cs = await db.list('corpos'), ms = await db.list('marcos'); return tcTempos(cs, ms); }""")
    ok("o tempo de remoção bate com os marcos", pg.inner_text("[data-tc-ind=remocao]").startswith(str(calc["remocao"])) or calc["remocao"] is None)
    ok("a tabela de permanência lista os corpos no IML", pg.locator("#tabelaPermanencia tr").count() > 1)
    ok("o painel conta os corpos sem movimentação (plantão)", pg.locator("[data-tc-ind=plantao]").count() == 1)
    ok("o alerta de passagem de plantão aparece quando há corpo parado",
       pg.locator("#tcAlertaPlantao").count() == (1 if calc["remocao"] is not None and int(pg.inner_text("[data-tc-ind=plantao]")) > 0 else 0))

# origem: sprint4.py
@cenario
def s6_relatorio_e_retencao(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    ir(pg, url, "#/painel", 900)
    with pg.expect_download() as dl:
        pg.click("#btnTcCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV sai com BOM e as colunas do caso", csv.startswith(b"\xef\xbb\xbf") and b"protocolo;situacao;identificado" in csv)
    # retenção: libera um corpo e apaga
    cid = pg.evaluate("async ()=> (await db.list('corpos')).find(c=>c.identificado && c.situacao!=='liberado').id_corpo")
    pg.evaluate("""async id => { const c = await db.get('corpos', id);
        await db.put('corpos', {...c, situacao: 'liberado', entrega: {responsavel: 'Familiar', documento: 'AUTO-X', data: agora()}}); }""", cid)
    ir(pg, url, "#/corpo/" + cid, 800)
    ok("o caso liberado mostra o bloco de privacidade e retenção", "Privacidade e retenção" in pg.inner_text("#conteudo"))
    pg.click("#btnTcApagar"); pg.wait_for_timeout(900)
    ok("os dados do caso são apagados e a contagem fica", pg.evaluate("async id => !(await db.get('corpos', id))", cid)
       and pg.evaluate("async ()=> ((await db.get('contagens','tcin_apagados'))||{}).valor") == 1)
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
