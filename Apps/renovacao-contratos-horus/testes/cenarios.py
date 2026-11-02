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
    """Espera uma condição assíncrona (wait_for_function não aguarda Promise)."""
    fim = time.time() + timeout
    while time.time() < fim:
        if pg.evaluate(expr, arg):
            return True
        pg.wait_for_timeout(150)
    raise AssertionError("tempo esgotado: " + expr[:70])


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

# origem: sprint2.py
@cenario
def s2_cadastro_e_semaforo(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    venc = pg.evaluate("""async ()=>{ const h = hojeISO(); return (await db.list('contratos')).filter(c=>!['Encerrado','Rescindido','Expirado'].includes(c.status)
        && Math.round((new Date(c.data_fim+'T12:00:00')-new Date(h+'T12:00:00'))/86400000) <= 90
        && Math.round((new Date(c.data_fim+'T12:00:00')-new Date(h+'T12:00:00'))/86400000) >= 0).length; }""")
    ir(pg, url, "#/painel", 400)
    ok("o painel conta os contratos vencendo em 90 dias", pg.inner_text("[data-vencendo90]") == str(venc) and venc == 8)
    ok("as seis faixas aparecem no semáforo", len(pg.query_selector_all("#tabelaFaixas tr")) == 7)
    ir(pg, url, "#/contrato/novo", 400)
    pg.fill("#rcNumero", "999/2026"); pg.fill("#rcFornecedor", "Fornecedor Teste"); pg.fill("#rcCnpj", "11.111.111/1111-11")
    pg.fill("#rcValor", "1200"); pg.fill("#rcInicio", "2026-11-01"); pg.fill("#rcMeses", "12"); pg.fill("#rcObjeto", "Objeto de teste")
    pg.click("#formRcNovo button[type=submit]"); pg.wait_for_timeout(400)
    ok("CNPJ inválido é recusado", "CNPJ inválido" in pg.inner_text("#rcErros") and contar(pg, "contratos") == 15)
    pg.fill("#rcCnpj", "11.222.333/0001-81")
    pg.dispatch_event("#rcMeses", "change"); pg.wait_for_timeout(200)
    ok("a data de término é calculada pelos meses (R2)", pg.input_value("#rcFim") == "2027-11-01")
    pg.click("#formRcNovo button[type=submit]"); pg.wait_for_timeout(600)
    ok("cadastra o contrato e abre a ficha", "#/contrato/CT-016" in pg.url and "Fornecedor Teste" in pg.inner_text("#conteudo"))
    ok("a auditoria registra o cadastro (R6)", "contrato cadastrado" in pg.inner_text("#tabelaAuditoria"))
    pg.fill("#rcAditivo", "1º TA"); pg.dispatch_event("#rcNovaVigencia", "input"); pg.fill("#rcNovaVigencia", "2028-11-01")
    pg.click("#formRcAditivo button[type=submit]"); pg.wait_for_timeout(600)
    ok("o aditivo atualiza a vigência (R4)", pg.evaluate("async ()=> (await db.get('contratos','CT-016')).data_fim") == "2028-11-01")
    ok("o aditivo fica na auditoria", "aditivo publicado" in pg.inner_text("#tabelaAuditoria"))

# origem: sprint3.py
@cenario
def s3_instrucao_e_documentos(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    ir(pg, url, "#/painel", 600)
    aviso = pg.evaluate("""async ()=>{ const h = hojeISO(), cs = await db.list('contratos');
        const n = [];
        for (const c of cs){ const itens = await db.porIndice('instrucao','contrato_id',c.id_contrato);
            if (rcSemInstrucao(c, itens, h)) n.push(c.id_contrato); }
        return n; }""")
    ok("o painel avisa os contratos que vencem em 60 dias sem instrução completa (Sprint 3)", bool(aviso) and pg.locator("#rcAvisoInstrucao").count() == 1
       and pg.locator("#tabelaAviso tr").count() - 1 == len(aviso))
    # abrir um contrato do aviso e completar a instrução
    cid = aviso[0]
    ir(pg, url, "#/contrato/" + cid, 500)
    falta_antes = pg.locator("#rcListaInstrucao li.falta").count()
    ok("o checklist mostra os itens obrigatórios faltando", falta_antes >= 6 and "Falta concluir a instrução" in pg.inner_text("#conteudo"))
    for _ in range(8):
        b = pg.locator("#rcListaInstrucao .rcItem[data-obrigatorio='1'][data-feito='0']").first
        if not b.count():
            break
        b.click(); pg.wait_for_timeout(450)
    ok("marcar os itens obrigatórios deixa a instrução completa", pg.locator("#rcListaInstrucao li.falta").count() == 1
       and "Instrução completa" in pg.inner_text("#conteudo"))
    ok("o item facultativo não impede a conclusão", "Falta concluir a instrução" not in pg.inner_text("#conteudo"))
    ok("a auditoria registra a marcação do item", pg.evaluate("async id => (await db.porIndice('auditoria','contrato_id',id)).some(a=>a.acao.includes('item de instrução marcado'))", cid))
    ir(pg, url, "#/instrucao", 500)
    ok("a tela de instrução mostra o progresso de cada contrato", pg.locator("#tabelaInstrucao tr").count() == 15)
    # repositório de documentos: o fiscal não vê o restrito (R8)
    ir(pg, url, "#/contrato/" + cid, 500)
    pg.fill("#rcAnexoNome", "oficio-solicitacao.pdf"); pg.select_option("#rcAnexoVis", "gestao"); pg.fill("#rcAnexoTexto", "Documento fictício restrito.")
    pg.click("#formRcAnexo button[type=submit]"); pg.wait_for_timeout(600)
    ok("o documento fica guardado no contrato", pg.evaluate("async ()=> (await db.list('anexos')).length") == 1)
    ok("o gestor vê o documento restrito", "oficio-solicitacao.pdf" in pg.inner_text("#rcListaAnexos"))
    perfil(pg, url, "fiscal")
    ir(pg, url, "#/contrato/" + cid, 600)
    ok("o fiscal não vê o documento restrito à gestão (R8)", "oficio-solicitacao.pdf" not in pg.inner_text("#rcListaAnexos"))
    ok("o checklist continua visível para o fiscal", pg.locator("#rcListaInstrucao").count() == 1)

# origem: sprint4.py
@cenario
def s4_reajuste_e_fluxo(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    cid = pg.evaluate("async ()=> (await db.list('contratos')).find(c=>c.status==='Vigente').id_contrato")
    ir(pg, url, "#/contrato/" + cid, 700)
    ok("a ficha mostra o bloco de ajustes", pg.locator("#rcAjustes").count() == 1)
    pg.select_option("#rcAjTipo", "reajuste"); pg.fill("#rcAjPercentual", "30")
    pg.fill("#rcAjMemoria", "Índice aplicado sobre o valor original do contrato, conforme a série do IPCA.")
    pg.click("#formRcAjuste button[type=submit]"); pg.wait_for_timeout(500)
    ok("acima de 25% excede o limite legal (art. 125)", "limite legal" in pg.inner_text("#rcErrosAjuste"))
    pg.fill("#rcAjPercentual", "5")
    pg.click("#formRcAjuste button[type=submit]"); pg.wait_for_timeout(800)
    ok("o pedido entra como solicitado e com a memória", pg.evaluate("async id => { const a = (await db.porIndice('reajustes','contrato_id',id))[0]; return a && a.status==='solicitado' && a.valor_novo_c > a.valor_anterior_c; }", cid))
    # fluxo: em análise -> aprovado -> aplicado
    for _ in range(3):
        b = pg.locator("[data-rc-avancar]").first
        if not b.count():
            break
        b.click(); pg.wait_for_timeout(600)
    ok("o ajuste chega a aplicado", pg.evaluate("async id => (await db.porIndice('reajustes','contrato_id',id))[0].status === 'aplicado'", cid))
    ok("aplicado, o valor do contrato é atualizado", pg.evaluate("async id => { const c = await db.get('contratos', id); const a = (await db.porIndice('reajustes','contrato_id',id))[0]; return c.valor_c === a.valor_novo_c; }", cid))

# origem: sprint4.py
@cenario
def s5_fiscais_e_trilha(pg, url, ok):
    perfil(pg, url, "admin")
    semear(pg, url)
    cid = pg.evaluate("async ()=> (await db.list('contratos'))[0].id_contrato")
    ir(pg, url, "#/contrato/" + cid, 700)
    pg.fill("#rcFisNome", "Fiscal Fictício Novo")
    pg.click("#btnRcFiscal")
    esperar(pg, "async id => (await db.porIndice('fiscais','contrato_id',id)).some(x=>!x.ate && x.nome === 'Fiscal Fictício Novo')", arg=cid)
    ok("o fiscal novo entra como atual", pg.evaluate("async id => { const f = await db.porIndice('fiscais','contrato_id',id); const atual = f.find(x=>!x.ate); return atual && atual.nome === 'Fiscal Fictício Novo'; }", cid))
    pg.fill("#rcFisNome", "Fiscal Fictício Substituto")
    pg.click("#btnRcFiscal")
    esperar(pg, "async id => (await db.porIndice('fiscais','contrato_id',id)).filter(x=>x.ate).length === 1 && (await db.porIndice('fiscais','contrato_id',id)).length === 2", arg=cid)
    ok("a substituição fecha o anterior com data", pg.evaluate("async id => { const f = await db.porIndice('fiscais','contrato_id',id); return f.filter(x=>x.ate).length === 1 && f.length === 2; }", cid))
    ok("a substituição entra na auditoria (R6)", pg.evaluate("async id => (await db.porIndice('auditoria','contrato_id',id)).some(a=>a.acao==='fiscal substituído')", cid))

# origem: sprint4.py
@cenario
def s6_valor_em_risco_e_aceite(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    ir(pg, url, "#/painel", 900)
    calc = pg.evaluate("""async ()=>{ const cs = (await db.list('contratos')).filter(c=>!['Encerrado','Rescindido','Expirado'].includes(c.status));
        const h = hojeISO(), jan = cs.filter(c=>{ const d = Math.round((new Date(c.data_fim+'T12:00:00')-new Date(h+'T12:00:00'))/86400000); return d>=0 && d<=90; });
        return {n: jan.length, valor: jan.reduce((a,c)=>a+Number(c.valor_c||0),0)}; }""")
    ok("o painel conta os contratos na janela de 90 dias", pg.inner_text("[data-rc-ind=contratos]") == str(calc["n"]))
    ok("o painel mostra o valor em risco", pg.inner_text("[data-rc-ind=risco]").replace(".", "").replace(",", ".").replace("R$ ", "") != "")
    ok("o painel mostra o tempo médio até a renovação", pg.locator("[data-rc-ind=tempo]").count() == 1)
    with pg.expect_download() as dl:
        pg.click("#btnRcCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV sai com BOM e as colunas do contrato e da faixa", csv.startswith(b"\xef\xbb\xbf") and b"contrato;numero;fornecedor" in csv and b"faixa" in csv)
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
