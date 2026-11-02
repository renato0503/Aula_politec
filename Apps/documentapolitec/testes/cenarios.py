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
def s2_caixa_e_conferencia(pg, url, ok):
    perfil(pg, url, "papiloscopista")
    semear(pg, url)
    ir(pg, url, "#/painel", 400)
    ok("o exemplo traz 12 caixas e 1 conferida", contar(pg, "caixas") == 12 and pg.inner_text("[data-conferidas]") == "1")
    ir(pg, url, "#/caixa/nova", 400)
    pg.fill("#docCaixa", "CX-TESTE-1"); pg.fill("#docSetor", "Arquivo corrente"); pg.fill("#docResponsavel", "Papiloscopista Teste")
    pg.fill("#docRelacao", "2019.900001\n2019.900002\n2019.900001")
    pg.click("#formDocNova button[type=submit]"); pg.wait_for_timeout(400)
    ok("prontuário repetido na relação é recusado (RN01)", "repetido" in pg.inner_text("#docErros"))
    num = pg.evaluate("async ()=> (await db.list('prontuarios'))[0].numero")
    pg.fill("#docRelacao", "2019.900001\n2019.900002\n" + num)
    pg.click("#formDocNova button[type=submit]"); pg.wait_for_timeout(400)
    ok("prontuário de outra caixa é recusado (RN01)", "Já cadastrado" in pg.inner_text("#docErros"))
    pg.fill("#docRelacao", "2019.900001\n2019.900002")
    pg.click("#formDocNova button[type=submit]"); pg.wait_for_timeout(600)
    ok("cadastra a caixa com 2 prontuários", "#/caixa/CX-TESTE-1" in pg.url and contar(pg, "prontuarios") == 137)
    pg.click("#btnDocConferir"); pg.wait_for_timeout(600)
    ok("sem divergência, a caixa é conferida e lacrada (RN02)", pg.inner_text("#docStatus").startswith("Conferida") and pg.evaluate("async ()=> (await db.get('caixas','CX-TESTE-1')).lacrada_por") == "Papiloscopista Teste")
    ir(pg, url, "#/caixa/nova", 300)
    pg.fill("#docCaixa", "CX-TESTE-2"); pg.fill("#docSetor", "Sala cofre"); pg.fill("#docResponsavel", "Papiloscopista Teste")
    pg.fill("#docRelacao", " ".join(f"2019.91{i:04d}" for i in range(12)))
    pg.click("#formDocNova button[type=submit]"); pg.wait_for_timeout(500)
    pg.click("#btnDocConferir"); pg.wait_for_timeout(600)
    ok("com 1 ausente no digital, a caixa fica com divergência e sem lacre", pg.inner_text("#docStatus").startswith("Com divergência")
       and pg.evaluate("async ()=> (await db.get('caixas','CX-TESTE-2')).lacrada_por") is None)
    ir(pg, url, "#/busca", 400); pg.fill("#docBusca", "2019.900002"); pg.click("#btnDocBuscar"); pg.wait_for_timeout(500)
    ok("a busca localiza a caixa do prontuário", "CX-TESTE-1" in pg.inner_text("#resultadoBusca"))

# origem: sprint3.py
@cenario
def s3_importacao_e_conferencia(pg, url, ok):
    perfil(pg, url, "papiloscopista")
    semear(pg, url)
    ex = PASTA / "exemplos"
    ir(pg, url, "#/importar", 500)
    ok("a tela de importação começa vazia", pg.locator("#docBlocoRelacao").count() == 1 and "Nenhuma planilha carregada" in pg.inner_text("#conteudo"))
    # sem os dois arquivos, a importação é recusada
    pg.click("#formDocImport button[type=submit]"); pg.wait_for_timeout(400)
    ok("sem planilha e sem índice, a importação é recusada", "Carregue a planilha" in pg.inner_text("#docErrosImport"))
    pg.set_input_files("#arqRelacao", str(ex / "relacao-prontuarios.csv")); pg.wait_for_timeout(700)
    ok("a planilha é lida e a coluna do prontuário é sugerida", pg.input_value("#mapRel_numero") == "0")
    pg.set_input_files("#arqDigital", str(ex / "indice-arquivo-digital.csv")); pg.wait_for_timeout(700)
    ok("o índice digital também sugere a coluna", pg.input_value("#mapDig_numero") == "0")
    pg.select_option("#docCaixaDestino", "nova")
    pg.fill("#docIdCaixa", "CX-013"); pg.fill("#docSetor", "DMIT · Arquivo corrente"); pg.fill("#docResponsavel", "Papiloscopista Teste")
    pg.click("#formDocImport button[type=submit]"); pg.wait_for_timeout(2500)
    ok("a planilha entra na base", pg.evaluate("async ()=> (await db.get('caixas','CX-013')).qtd") == 850)
    ok("os prontuários aceitos estão na caixa nova", pg.evaluate("async ()=> (await db.porIndice('prontuarios','caixa_id','CX-013')).length") == 850)
    ir(pg, url, "#/relatorio-importacao", 600)
    aceitas = pg.inner_text("#docQtdAceitas"); rec = pg.inner_text("#docQtdRecusadas"); div = pg.inner_text("#docQtdDivergentes")
    ok("o relatório conta as linhas aceitas, recusadas e divergentes", aceitas == "850" and rec == "3" and div == "5")
    ok("o relatório lista as linhas aceitas", pg.locator("#tabelaAceitas tr").count() == 851)
    ok("as recusas trazem o motivo", "repetido" in pg.inner_text("#tabelaRecusadas") and "fora do formato" in pg.inner_text("#tabelaRecusadas"))
    ok("as divergências apontam o que não está no arquivo digital", "não localizado no arquivo digital" in pg.inner_text("#tabelaDivergentes")
       and "não veio na planilha" in pg.inner_text("#tabelaDivergentes"))
    # o prontuário importado aparece na busca
    ir(pg, url, "#/busca", 400); pg.fill("#docBusca", "2018.000001"); pg.click("#btnDocBuscar"); pg.wait_for_timeout(500)
    ok("o prontuário importado é localizado pela busca", "CX-013" in pg.inner_text("#resultadoBusca"))
    # o histórico da caixa registra a importação
    ir(pg, url, "#/caixa/CX-013", 500)
    ok("o histórico da caixa registra a planilha importada", "planilha importada" in pg.inner_text("#conteudo"))

# origem: sprint4.py
@cenario
def s4_busca_por_nome(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    indice = TMP / "indice-nomes.csv"
    indice.write_text("numero;nome;caixa\n2019.000001;Maria Fictícia Souza;CX-001\n2019.000002;João Fictício Lima;CX-001\n", encoding="utf-8-sig")
    ir(pg, url, "#/busca-nome", 600)
    ok("a busca por nome pede o índice autorizado", pg.locator("#arqIndice").count() == 1)
    pg.set_input_files("#arqIndice", str(indice)); pg.wait_for_timeout(900)
    ok("o índice é carregado sem guardar o nome em claro",
       pg.evaluate("async ()=> { const i = await db.list('indice_nomes'); return i.length === 2 && i.every(x=>!('nome' in x) && x.nome_hash); }"))
    pg.fill("#docNome", "maria ficticia souza")
    pg.click("#formBuscaNome button[type=submit]"); pg.wait_for_timeout(800)
    ok("a busca acha o prontuário e mostra caixa, setor e situação", "2019.000001" in pg.inner_text("#docResNome")
       and "CX-001" in pg.inner_text("#docResNome") and "DMIT" in pg.inner_text("#docResNome"))
    ok("a consulta entra na trilha (RN03)", pg.evaluate("async ()=> (await db.list('consultas')).length") == 1
       and pg.locator("#tabelaConsultas tr").count() == 2)
    # acesso restrito
    perfil(pg, url, "papiloscopista")
    ir(pg, url, "#/busca-nome", 600)
    ok("o perfil papiloscopista não acessa a busca por nome (RN03)", "não usa esta tela" in pg.inner_text("#conteudo")
       or "Acesso restrito" in pg.inner_text("#conteudo"))

# origem: sprint4.py
@cenario
def s5_etiqueta_e_leitura(pg, url, ok):
    perfil(pg, url, "papiloscopista")
    semear(pg, url)
    ir(pg, url, "#/caixa/CX-001", 700)
    ok("a etiqueta mostra o código de conferência e o código de barras",
       pg.locator("#docCodConf").count() == 1 and pg.locator("#docEtiqueta svg[role=img]").count() == 1)
    cod = pg.inner_text("#docCodConf")
    ok("o código de conferência tem o formato da caixa", "-" in cod and len(cod) >= 8)
    pg.fill("#docLeituraCod", "XX0-0000")
    pg.click("#btnDocLeitura"); pg.wait_for_timeout(600)
    ok("código errado é recusado", "não confere" in pg.inner_text("#docErrosLeitura"))
    pg.fill("#docLeituraCod", cod)
    pg.click("#btnDocLeitura"); pg.wait_for_timeout(600)
    ok("código certo é aceito e fica no histórico", pg.evaluate("async ()=> (await db.list('log')).some(l=>l.acao==='código de conferência lido')"))

# origem: sprint4.py
@cenario
def s6_painel_e_relatorio(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    ir(pg, url, "#/painel", 800)
    calc = pg.evaluate("""async ()=>{ const cs = await db.list('caixas'), ps = await db.list('prontuarios');
        return {conferidas: cs.filter(c=>c.status==='conferida').length, pendentes: cs.filter(c=>c.status!=='conferida').length,
                conferidos: ps.filter(p=>p.conferido).length}; }""")
    ok("o painel conta conferidas e pendentes", pg.inner_text("[data-doc-ind=conferidas]") == str(calc["conferidas"])
       and pg.inner_text("[data-doc-ind=pendentes]") == str(calc["pendentes"]))
    ok("o espaço liberado é calculado pelos prontuários conferidos", f"{round(calc['conferidos']*0.03, 2)}" in pg.inner_text("[data-doc-ind=espaco]"))
    ok("o painel mostra os prontuários por período", pg.locator("#tabelaPeriodo tr").count() > 1)
    with pg.expect_download() as dl:
        pg.click("#btnDocCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV sai com BOM e as colunas da caixa", csv.startswith(b"\xef\xbb\xbf") and b"caixa;setor;data" in csv)
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
