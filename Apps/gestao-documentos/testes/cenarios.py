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
def s2_autuacao_e_prazo(pg, url, ok):
    perfil(pg, url, "servidor")
    semear(pg, url)
    venc = pg.evaluate("async ()=> (await db.list('processos')).filter(p=>gdPrazo(p).sinal === 'vermelho').length")
    ir(pg, url, "#/painel", 400)
    ok("o painel conta os processos vencidos", pg.inner_text("[data-vencidos]") == str(venc) and venc > 0)  # o número muda com a data de hoje
    ir(pg, url, "#/processo/novo", 400)
    pg.fill("#gdAssunto", "Processo de teste"); pg.fill("#gdRequerente", "Requerente Teste"); pg.fill("#gdLotacao", "Gabinete de Direção")
    pg.check("#gdAnexo0")
    pg.click("#formGdNovo button[type=submit]"); pg.wait_for_timeout(400)
    ok("sem todos os anexos, a autuação é recusada (RN01)", "Faltam anexos" in pg.inner_text("#gdErros") and contar(pg, "processos") == 12)
    pg.check("#gdAnexo1"); pg.check("#gdAnexo2")
    pg.click("#formGdNovo button[type=submit]"); pg.wait_for_timeout(600)
    ok("autua com o número gerado no formato AAAA.NNNN-SD (RN02)", "#/processo/PR-0013" in pg.url
       and pg.evaluate("async ()=> (await db.get('processos','PR-0013')).numero_processo") == "2026.0013-SD")
    ok("os três documentos entram na ficha", pg.evaluate("async ()=> (await db.porIndice('documentos','processo_id','PR-0013')).length") == 3)
    ok("o prazo de 15 dias começa em verde", pg.inner_text("#gdSinalAtual") == "No prazo")
    ir(pg, url, "#/processo/novo", 300)
    pg.fill("#gdNumero", "2026.0001-SD"); pg.fill("#gdAssunto", "X"); pg.fill("#gdRequerente", "Y"); pg.fill("#gdLotacao", "Z")
    for i in range(3): pg.check(f"#gdAnexo{i}")
    pg.click("#formGdNovo button[type=submit]"); pg.wait_for_timeout(400)
    ok("número de processo repetido é recusado", "já está cadastrado" in pg.inner_text("#gdErros"))
    ir(pg, url, "#/processos", 400); pg.select_option("#gdSinal", "vermelho"); pg.wait_for_timeout(400)
    ok("o filtro pelo sinal vermelho mostra só os vencidos", pg.evaluate("async ()=> document.querySelectorAll('table tr').length - 1") == venc)

# origem: sprint3.py
@cenario
def s3_minutas_e_checklist(pg, url, ok):
    perfil(pg, url, "servidor")
    semear(pg, url)
    ir(pg, url, "#/processo/novo", 400)
    pg.fill("#gdAssunto", "Pedido de cópia de laudo"); pg.fill("#gdRequerente", "Requerente Teste"); pg.fill("#gdLotacao", "Gabinete de Direção")
    pg.select_option("#gdResponsavel", "U1")
    for i in range(3): pg.check(f"#gdAnexo{i}")
    pg.click("#formGdNovo button[type=submit]"); pg.wait_for_timeout(600)
    pid = pg.evaluate("async ()=> (await db.list('processos')).sort((a,b)=>b.criado_em.localeCompare(a.criado_em))[0].id_processo")
    ok("o processo novo está na ficha", "#/processo/" + pid in pg.url)
    # RN04: minuta sai preenchida com os dados do processo
    pg.select_option("#gdTipoMinuta", "oficio_encaminhamento")
    pg.click("#formGdMinuta button[type=submit]"); pg.wait_for_timeout(600)
    ok("a minuta é emitida e entra na lista", pg.evaluate("async id => (await db.porIndice('minutas','processo_id',id)).length", pid) == 1)
    ok("a emissão cria o documento correspondente", pg.evaluate("async id => (await db.porIndice('documentos','processo_id',id)).some(d=>d.tipo_documento==='Ofício de encaminhamento')", pid))
    ok("o histórico registra a minuta emitida", pg.evaluate("async id => (await db.porIndice('log','processo_id',id)).some(l=>l.tipo_evento==='minuta emitida')", pid))
    pg.click(".gdMinutaAbrir"); pg.wait_for_timeout(500)
    txt = pg.inner_text("#gdMinutaTexto")
    ok("a minuta aberta traz o número, o assunto, o requerente e a lotação (RN04)", "Pedido de cópia de laudo" in txt
       and "Requerente Teste" in txt and "Gabinete de Direção" in txt and "2026." in txt)
    # despacho
    pg.select_option("#gdTipoMinuta", "despacho")
    pg.click("#formGdMinuta button[type=submit]"); pg.wait_for_timeout(600)
    ok("o despacho também é emitido", pg.evaluate("async id => (await db.porIndice('minutas','processo_id',id)).length", pid) == 2)
    # checklist por etapa
    ok("o checklist traz as duas etapas", pg.locator("#gdCheck_Instrução li").count() == 4 and pg.locator("#gdCheck_Decisão li").count() == 3)
    for _ in range(8):
        b = pg.locator(".gdCheckItem[data-feito='0']").first
        if not b.count():
            break
        b.click(); pg.wait_for_timeout(400)
    ok("todos os itens do checklist ficam marcados", pg.locator(".gdCheckItem[data-feito='0']").count() == 0)
    ok("o histórico registra o checklist", pg.evaluate("async id => (await db.porIndice('log','processo_id',id)).some(l=>l.tipo_evento==='checklist: item marcado')", pid))
    # RN04: processo sem os dados exigidos não emite minuta
    pg.evaluate("async id => { const p = await db.get('processos', id); await db.put('processos', {...p, requerente: ''}); }", pid)
    pg.reload(); pg.wait_for_timeout(700)
    ok("sem requerente, a minuta fica bloqueada (RN04)", pg.locator("#gdErrosMinuta").count() == 1 and "requerente" in pg.inner_text("#gdErrosMinuta"))
    pg.click("#formGdMinuta button[type=submit]"); pg.wait_for_timeout(400)
    ok("a emissão é recusada com o motivo", "RN04" in pg.inner_text("#gdErrosEmissao"))

# origem: sprint4.py
@cenario
def s4_cobranca_automatica(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    ir(pg, url, "#/painel", 900)
    venc = pg.evaluate("async ()=> (await db.list('processos')).filter(p=>p.status==='em andamento' && ['amarelo','vermelho'].includes(gdPrazo(p).sinal)).length")
    ok("a cobrança é registrada para os prazos próximos e vencidos (RN08)", pg.evaluate("async ()=> (await db.list('cobrancas')).length") == venc and venc > 0)
    ok("a cobrança entra no histórico do processo", pg.evaluate("async ()=> (await db.list('log')).some(l=>l.tipo_evento==='cobrança automática')"))
    # não duplica ao abrir o painel de novo
    ir(pg, url, "#/painel", 900)
    ok("abrir o painel de novo não duplica a cobrança", pg.evaluate("async ()=> (await db.list('cobrancas')).length") == venc)
    # desligar a cobrança por lotação
    lot = pg.evaluate("async ()=> (await db.list('processos'))[0].lotacao")
    pg.select_option("#gdLotacaoCobranca", lot); pg.select_option("#gdCobrancaAcao", "desligar")
    pg.click("#formGdCobranca button[type=submit]"); pg.wait_for_timeout(700)
    ok("a lotação fica com a cobrança desligada", pg.evaluate("async l => (await db.meta('cobrancas_desligadas')).includes(l)", lot))

# origem: sprint4.py
@cenario
def s5_assinatura_e_arquivamento(pg, url, ok):
    perfil(pg, url, "autoridade")
    semear(pg, url)
    pid = pg.evaluate("async ()=> (await db.list('processos')).find(p=>p.status==='em andamento').id_processo")
    ir(pg, url, "#/processo/" + pid, 700)
    ok("a ficha mostra o bloco de conclusão com assinatura", pg.locator("#gdConclusao").count() == 1)
    pg.fill("#gdConclusaoTexto", "curto")
    pg.click("#formGdFechar button[type=submit]"); pg.wait_for_timeout(500)
    ok("sem a conclusão escrita, a assinatura é recusada (RN09)", "20 caracteres" in pg.inner_text("#gdErrosFechar"))
    pg.fill("#gdConclusaoTexto", "Instrução concluída e requerente atendido integralmente, com os anexos conferidos.")
    pg.fill("#gdAssNome", "Autoridade Fictícia"); pg.fill("#gdAssCargo", "Diretor")
    pg.click("#formGdFechar button[type=submit]"); pg.wait_for_timeout(800)
    ok("a assinatura fica registrada com nome, cargo e data", pg.evaluate("async id => { const a = (await db.porIndice('assinaturas','processo_id',id))[0]; return a && a.nome && a.cargo && a.data; }", pid))
    ok("o processo é notificado e arquivado (RN10)", pg.evaluate("async id => (await db.get('processos', id)).status === 'arquivado'", pid)
       and pg.evaluate("async id => (await db.list('log')).some(l=>l.processo_id===id && l.tipo_evento==='notificação ao requerente')", pid)
       and pg.evaluate("async id => (await db.list('log')).some(l=>l.processo_id===id && l.tipo_evento==='arquivamento')", pid))

# origem: sprint4.py
@cenario
def s6_painel_e_relatorio(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    ir(pg, url, "#/painel", 900)
    calc = pg.evaluate("""async ()=>{ const ps = (await db.list('processos')).filter(p=>p.status==='em andamento'), h = hojeISO();
        return {amarelos: ps.filter(p=>gdPrazo(p, h).sinal==='amarelo').length, vencidos: ps.filter(p=>gdPrazo(p, h).sinal==='vermelho').length}; }""")
    ok("o painel conta alertas amarelos e vencidos", pg.inner_text("[data-gd-ind=amarelos]") == str(calc["amarelos"])
       and pg.inner_text("[data-gd-ind=vencidos]") == str(calc["vencidos"]))
    ok("o painel mostra cobranças e tempo médio", pg.locator("[data-gd-ind=cobrancas]").count() == 1
       and pg.locator("[data-gd-ind=tempo]").count() == 1)
    ok("os processos por lotação aparecem", pg.locator("#tabelaLotacao tr").count() > 1)
    with pg.expect_download() as dl:
        pg.click("#btnGdCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV sai com BOM e as colunas de sinal e cobranças", csv.startswith(b"\xef\xbb\xbf") and b"sinal" in csv and b"cobrancas" in csv)
    ok("o roteiro de aceite está em modelos/", (PASTA / "modelos" / "roteiro-aceite.md").exists())

@cenario
def s8_feedback_anexo_entrada_cobranca(pg, url, ok):
    semear(pg, url)
    antes = contar(pg, "processos")
    ir(pg, url, "#/processo/novo", 400)
    pg.fill("#gdAssunto", "Acompanhamento de ofício"); pg.fill("#gdRequerente", "Requerente Teste")
    pg.fill("#gdLotacao", "Gabinete de Direção"); pg.select_option("#gdTipo", "acompanhamento")
    pg.click("#formGdNovo button[type=submit]"); pg.wait_for_timeout(700)
    ok("acompanhamento é cadastrado sem anexo", contar(pg, "processos") == antes + 1)
    novo = pg.evaluate("async () => (await db.list('processos')).find(p=>p.tipo_processo==='acompanhamento')")
    ok("o tipo de acompanhamento é gravado", bool(novo) and novo.get("tipo_processo") == "acompanhamento")
    ok("o acompanhamento não cria documento", bool(novo) and pg.evaluate("async id => (await db.porIndice('documentos','processo_id',id)).length", novo["id_processo"]) == 0)

    ir(pg, url, "#/processos", 500)
    ok("a lista mostra a data de entrada", "Entrada" in pg.inner_text("table"))
    alvo = pg.evaluate("""async () => {
      const ps = await db.list('processos');
      const p = ps.find(p=>p.status==='em andamento' && ['amarelo','vermelho'].includes(gdPrazo(p).sinal));
      return p ? p.id_processo : '';
    }""")
    ok("há processo com prazo próximo ou vencido para cobrar", bool(alvo))
    if alvo:
        pg.click(f'[data-gd-cobrar="{alvo}"]'); pg.wait_for_timeout(700)
        ok("a cobrança manual é registrada", pg.evaluate("async id => (await db.porIndice('cobrancas','processo_id',id)).some(c=>c.tipo==='manual')", alvo))


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
