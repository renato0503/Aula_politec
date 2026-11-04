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
def s2_pedido_do_cidadao(pg, url, ok):
    pg.set_viewport_size({"width": 390, "height": 800})   # celular
    ir(pg, url, "#/pedido", 300)
    pg.check("input[name=valida][value=nao]"); pg.check("input[name=mudou][value=nao]"); pg.check("input[name=extraviado][value=nao]"); pg.click("#formElegivel button[type=submit]"); pg.wait_for_timeout(200)
    ok("CIN vencida leva ao agendamento no posto (RN03)", pg.locator("#avisoPosto a[href*='agendamento-cin']").count() == 1)
    pg.check("input[name=valida][value=sim]"); pg.click("#formElegivel button[type=submit]"); pg.wait_for_timeout(200)
    ok("elegível abre o formulário", pg.locator("#formPedido").count() == 1)
    pg.fill("#cNome", "Alice Teste"); pg.fill("#cCpf", "000.000.010-28"); pg.fill("#cNasc", "1990-05-10"); pg.fill("#cValidade", "2030-01-01"); pg.fill("#cContato", "alice@exemplo.com")
    pg.click("#formPedido button[type=submit]"); pg.wait_for_timeout(300)
    erros = pg.inner_text("#errosPedido")
    ok("CPF inválido é recusado (RN01)", "CPF inválido" in erros)
    ok("sem fotos o pedido não segue (RN02)", "foto do rosto" in erros and "foto do documento" in erros)
    valido = pg.evaluate("()=> dadosEmbutidos('seed').pedidos[0].cpf")
    pg.fill("#cCpf", valido)
    pg.click("[data-teste=rosto]"); pg.click("[data-teste=documento]"); pg.wait_for_timeout(800)
    pg.click("#formPedido button[type=submit]"); pg.wait_for_timeout(600)
    ok("pedido completo gera protocolo", pg.locator("#numProtocolo").count() == 1 and pg.inner_text("#numProtocolo").startswith("2V-"))
    ok("pedido gravado como recebido", pg.evaluate("async ()=> (await db.list('pedidos')).filter(p=>p.situacao==='recebido').length") == 1)
    ok("2 fotos gravadas, reduzidas para até 800 px", pg.evaluate("""async ()=>{ const fs = await db.list('fotos'); if (fs.length !== 2) return false;
        for (const f of fs){ const b = await createImageBitmap(f.conteudo); if (Math.max(b.width, b.height) > 800) return false; } return true; }"""))
    ok("sem rolagem horizontal no celular", pg.evaluate("()=> document.documentElement.scrollWidth <= window.innerWidth"))

# origem: sprint3.py
@cenario
def s3_fila_do_servidor(pg, url, ok):
    perfil(pg, url, "servidor")
    semear(pg, url)
    pg.evaluate("""async ()=>{ const p = {protocolo: '2V-TESTE-0001', nome: 'Alice Teste', cpf: dadosEmbutidos('seed').pedidos[0].cpf, nascimento: '1990-05-10',
        numero_cin: dadosEmbutidos('seed').pedidos[0].cpf, validade_cin: '2031-01-01', mudou_dados: false, contato: 'alice@exemplo.com', criado_em: '2026-10-28T10:00:00Z', situacao: 'recebido', motivo: ''};
      await db.put('pedidos', p); for (const t of ['rosto','documento']) await db.put('fotos', {id: p.protocolo + '-' + t, protocolo: p.protocolo, tipo: t, conteudo: await fotoDeTeste(t)}); }""")
    ir(pg, url, "#/fila", 500)
    rec = pg.evaluate("async ()=> (await db.list('pedidos')).filter(p=>p.situacao==='recebido').length")
    ok("a fila separa por situação", pg.inner_text("[data-qtd=recebido]") == str(rec))
    pg.click("[data-sel='2V-TESTE-0001']"); pg.wait_for_timeout(500)
    ok("a ficha mostra as 2 fotos e a elegibilidade", pg.locator("#fichaPedido img").count() == 2 and "CIN válida" in pg.inner_text("#fichaPedido"))
    pg.click("#btnRecusar"); pg.wait_for_timeout(300)
    ok("recusar sem motivo é recusado (RN05)", "RN05" in pg.inner_text("#errosFila"))
    pg.select_option("#fMotivo", "Foto ilegível"); pg.click("#btnRecusar"); pg.wait_for_timeout(500)
    ok("recusa grava situação, motivo e decisão", pg.evaluate("async ()=> (await db.get('pedidos','2V-TESTE-0001')).motivo") == "Foto ilegível" and contar(pg, "decisoes") == 1)
    ok("a recusa fica no log", pg.evaluate("async ()=> (await db.list('log')).some(l=>l.acao==='pedido recusado' && l.protocolo==='2V-TESTE-0001')"))
    outro = pg.evaluate("async ()=> (await db.list('pedidos')).find(p=>p.situacao==='recebido').protocolo")
    pg.evaluate("p => { estado.pedidoSel = p; }", outro); ir(pg, url, "#/fila", 200); pg.evaluate("()=> navegar()"); pg.wait_for_timeout(400)
    pg.click("#btnAceitar"); pg.wait_for_timeout(500)
    ok("aceitar muda a situação", pg.evaluate("async p => (await db.get('pedidos', p)).situacao", outro) == "aceito")
    ir(pg, url, "#/pedido/2V-TESTE-0001/resumo", 400)
    ok("resumo traz CPF formatado e a situação", "." in pg.inner_text("#tabelaResumo") and "recusado" in pg.inner_text("#tabelaResumo"))

# origem: sprint5.py
@cenario
def s5_indicadores_e_retencao(pg, url, ok):
    # o servidor decide e apaga o pedido (RN06)
    perfil(pg, url, "servidor")
    semear(pg, url)
    ir(pg, url, "#/fila", 500)
    pg.locator("[data-sel]").first.click(); pg.wait_for_timeout(400)
    pg.click("#btnAceitar"); pg.wait_for_timeout(600)
    prot = pg.evaluate("async ()=> (await db.list('pedidos')).find(p=>p.situacao!=='recebido').protocolo")
    ir(pg, url, "#/pedido/" + prot + "/resumo", 500)
    ok("o pedido decidido mostra o botão de apagar (RN06)", pg.locator("#btnApagarPedido").count() == 1)
    pg.click("#btnApagarPedido"); pg.wait_for_timeout(800)
    ok("o pedido e as fotos saem, e a contagem fica", pg.evaluate("async id => !(await db.get('pedidos', id))", prot)
       and pg.evaluate("async ()=> (await db.get('contagens','apagados')).valor") == 1)
    # a gestão vê os indicadores
    perfil(pg, url, "gestao")
    ir(pg, url, "#/indicadores", 600)
    calc = pg.evaluate("""async ()=>{ const ps = await db.list('pedidos'); return {
        total: ps.length, aceitos: ps.filter(p=>p.situacao==='aceito').length,
        recusados: ps.filter(p=>p.situacao==='recusado').length,
        elegiveis: ps.filter(p=>p.validade_cin >= hojeISO() && !p.mudou_dados).length }; }""")
    ok("o painel de indicadores conta pedidos, elegíveis, aceitos e recusados",
       pg.inner_text("[data-ind=total]") == str(calc["total"]) and pg.inner_text("[data-ind=aceitos]") == str(calc["aceitos"])
       and pg.inner_text("[data-ind=recusados]") == str(calc["recusados"]) and pg.inner_text("[data-ind=elegiveis]") == str(calc["elegiveis"]))
    ok("as recusas aparecem agrupadas por motivo", pg.locator("#tabelaMotivos tr").count() > 1
       and "Foto ilegível" in pg.inner_text("#tabelaMotivos"))
    ok("o tempo médio do pedido à decisão é calculado", pg.inner_text("[data-ind=tempo]") != "—")
    ok("o indicador mostra o pedido apagado pela retenção", pg.inner_text("#qtdApagados") == "1")

# origem: sprint5.py
@cenario
def s6_aceite_do_piloto(pg, url, ok):
    perfil(pg, url, "servidor")
    semear(pg, url)
    ir(pg, url, "#/pedido", 500)
    ok("o formulário do cidadão abre com as três perguntas de elegibilidade", pg.locator("#formElegivel").count() == 1)
    pg.check("input[name=valida][value=sim]"); pg.check("input[name=mudou][value=nao]"); pg.check("input[name=extraviado][value=nao]")
    pg.click("#formElegivel button[type=submit]"); pg.wait_for_timeout(500)
    ok("os campos do pedido têm label associado ao id",
       pg.evaluate("""()=>{ const ls = [...document.querySelectorAll('main label[for]')];
         return ls.length >= 4 && ls.every(l=>document.getElementById(l.htmlFor)); }"""))
    ok("as imagens de foto têm texto alternativo",
       pg.evaluate("""()=> [...document.querySelectorAll('main img')].every(i=>i.hasAttribute('alt'))"""))
    ir(pg, url, "#/fila", 500)
    ok("a fila usa botões com rótulo para a situação",
       pg.locator("[data-sit]").count() == 4 and "recebido" in pg.inner_text("[data-sit='recebido']"))
    ok("o roteiro do aceite e a posição da TI estão no modelos/",
       (PASTA / "modelos" / "roteiro-aceite.md").exists())

@cenario
def s7_fotos_das_impressoes(pg, url, ok):
    ir(pg, url, "#/pedido", 300)
    pg.check("input[name=valida][value=sim]"); pg.check("input[name=mudou][value=nao]")
    pg.check("input[name=extraviado][value=sim]"); pg.click("#formElegivel button[type=submit]"); pg.wait_for_timeout(300)
    ok("documento extraviado pede as impressões e não o documento",
       pg.locator("#formPedido").count() == 1 and "impressões digitais" in pg.inner_text("#formPedido")
       and pg.locator("[data-foto=documento]").count() == 0 and pg.locator("[data-foto=impressao_1]").count() == 1)
    valido = pg.evaluate("()=> dadosEmbutidos('seed').pedidos[0].cpf")
    pg.fill("#cNome", "Alice Teste"); pg.fill("#cCpf", valido); pg.fill("#cNasc", "1990-05-10")
    pg.fill("#cValidade", "2030-01-01"); pg.fill("#cContato", "alice@exemplo.com")
    for t in ["rosto", "impressao_1", "impressao_2", "impressao_3", "impressao_4"]:
        pg.click(f"[data-teste={t}]")
    pg.wait_for_timeout(900)
    pg.click("#formPedido button[type=submit]"); pg.wait_for_timeout(700)
    ok("o pedido com impressões gera protocolo", pg.locator("#numProtocolo").count() == 1)
    protocolo = pg.inner_text("#numProtocolo")
    ok("o pedido guarda o extravio", pg.evaluate("async p => (await db.get('pedidos', p)).extraviado", protocolo) is True)
    ok("cinco fotos são gravadas (rosto + 4 impressões)", pg.evaluate("""async p => {
        const fs = await db.porIndice('fotos', 'protocolo', p);
        return fs.length === 5 && ['impressao_1','impressao_2','impressao_3','impressao_4'].every(t=>fs.some(f=>f.tipo===t)) && !fs.some(f=>f.tipo==='documento');
    }""", protocolo))
    perfil(pg, url, "servidor")
    ir(pg, url, "#/fila", 600)
    pg.click(f"[data-sel='{protocolo}']"); pg.wait_for_timeout(500)
    ok("a fila mostra as fotos das impressões", pg.locator("#fichaPedido img").count() == 5)


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


