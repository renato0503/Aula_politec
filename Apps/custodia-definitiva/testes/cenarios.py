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
def s2_cadastro_e_endereco(pg, url, ok):
    perfil(pg, url, "custodia")
    semear(pg, url)
    ir(pg, url, "#/painel", 400)
    ok("o exemplo tem 30 vestígios e o contêiner de eletrônicos cheio", contar(pg, "vestigios") == 30 and "100%" in pg.inner_text("#tabelaOcupacao"))
    ir(pg, url, "#/vestigio/novo", 400)
    pg.fill("#cdProtocolo", "PROC-TESTE-1"); pg.fill("#cdLacre", "LC-TESTE-1"); pg.select_option("#cdCategoria", "roupas")
    pg.fill("#cdVolume", "3"); pg.click("#formCdNovo button[type=submit]"); pg.wait_for_timeout(600)
    ok("cadastra e endereça no contêiner compatível", "#/vestigio/V-0031" in pg.url and pg.evaluate("async ()=> (await db.get('vestigios','V-0031')).conteiner_id") == "C-03")
    ok("a movimentação de entrada registra o perfil (RN04)", pg.evaluate("async ()=> (await db.porIndice('movimentacoes','vestigio_id','V-0031'))[0].responsavel") == "custodia")
    ir(pg, url, "#/vestigio/novo", 300)
    pg.fill("#cdProtocolo", "PROC-TESTE-2"); pg.fill("#cdLacre", "LC-TESTE-1"); pg.select_option("#cdCategoria", "roupas"); pg.fill("#cdVolume", "2")
    pg.click("#formCdNovo button[type=submit]"); pg.wait_for_timeout(400)
    ok("lacre repetido é recusado (RN01)", "já está em uso" in pg.inner_text("#cdErros") and contar(pg, "vestigios") == 31)
    pg.fill("#cdLacre", "LC-TESTE-2"); pg.select_option("#cdCategoria", "eletronicos"); pg.fill("#cdVolume", "2")
    pg.click("#formCdNovo button[type=submit]"); pg.wait_for_timeout(400)
    ok("categoria sem folga é recusada (RN02/RN03)", "compatível" in pg.inner_text("#cdErros") and contar(pg, "vestigios") == 31)
    ir(pg, url, "#/vestigios", 400); pg.select_option("#cdCat", "roupas"); pg.wait_for_timeout(400)
    ok("o filtro por categoria mostra só as roupas", pg.evaluate("async ()=>{ const t = document.querySelectorAll('table tr').length - 1; const n = (await db.list('vestigios')).filter(v=>v.categoria_id==='roupas').length; return t === n; }"))

# origem: sprint3.py
@cenario
def s3_busca_csv_e_historico(pg, url, ok):
    perfil(pg, url, "custodia")
    semear(pg, url)
    ir(pg, url, "#/vestigios", 400)
    pg.fill("#cdBusca", "LC-20260001"); pg.wait_for_timeout(700)
    ok("a busca pelo lacre acha o vestígio", pg.inner_text("#cdQtd") == "1" and "V-0001" in pg.inner_text("#cdTabelaAcervo"))
    pg.fill("#cdBusca", "C-03"); pg.wait_for_timeout(700)
    n03 = pg.evaluate("async ()=> (await db.list('vestigios')).filter(v=>v.conteiner_id==='C-03').length")
    ok("a busca pelo contêiner lista só o C-03", pg.inner_text("#cdQtd") == str(n03) and n03 > 0)
    pg.fill("#cdBusca", ""); pg.wait_for_timeout(700)
    pg.select_option("#cdCat", "entorpecentes"); pg.wait_for_timeout(300); pg.fill("#cdDe", "2026-01-01"); pg.dispatch_event("#cdDe", "change"); pg.wait_for_timeout(400)
    esperado = pg.evaluate("async ()=> (await db.list('vestigios')).filter(v=>v.categoria_id==='entorpecentes' && v.data_entrada>='2026-01-01').length")
    ok("filtros combinados (categoria + período)", pg.inner_text("#cdQtd") == str(esperado))
    with pg.expect_download() as d:
        pg.click("#btnCdCsv")
    linhas = open(d.value.path(), encoding="utf-8-sig").read().strip().splitlines()
    ok("o CSV traz o cabeçalho e as linhas filtradas", linhas[0].startswith("id_vestigio;protocolo;lacre") and len(linhas) - 1 == esperado)
    ir(pg, url, "#/vestigio/V-0011", 400)
    cat = pg.evaluate("async ()=> (await db.get('vestigios','V-0011')).categoria_id")
    pg.select_option("#cdMovTipo", "transferencia"); pg.wait_for_timeout(100)
    pg.click("#formCdMov button[type=submit]"); pg.wait_for_timeout(300)
    ok("movimentação sem motivo é recusada (RN04)", "motivo" in pg.inner_text("#cdMovErros"))
    pg.select_option("#cdMovTipo", "saida"); pg.wait_for_timeout(100)
    pg.fill("#cdMovPara", "Laboratório de Química Forense"); pg.fill("#cdMovMotivo", "Requisição 123/2026"); pg.click("#formCdMov button[type=submit]"); pg.wait_for_timeout(500)
    ok("saída para perícia marca o vestígio fora do acervo", pg.evaluate("async ()=> (await db.get('vestigios','V-0011')).fora") is True and "Fora" in pg.inner_text("#cdEndereco"))
    pg.fill("#cdMovMotivo", "Devolvido pelo laboratório"); pg.click("#formCdMov button[type=submit]"); pg.wait_for_timeout(500)
    movs = pg.evaluate("async ()=> (await db.porIndice('movimentacoes','vestigio_id','V-0011')).map(m=>m.tipo).sort().join()")
    ok("o histórico guarda entrada, saída e retorno", movs == "entrada,retorno,saida" and pg.locator("#cdMovs li").count() == 3)
    destino_errado = pg.evaluate("async c => (await db.list('conteineres')).find(x=>x.categoria_permitida!==c && x.categoria_permitida!=='todas').id_conteiner", cat)
    erro = pg.evaluate("async d => { try { await cdMovimentar('V-0011','transferencia',{destino:d, motivo:'teste'}); return ''; } catch(e){ return e.message; } }", destino_errado)
    ok("transferência para contêiner de outra categoria é recusada (RN02)", "RN02" in erro)

# origem: sprint4.py
@cenario
def s4_projecao_e_saturacao(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    ir(pg, url, "#/painel", 800)
    ok("o painel do gestor abre com a projeção e a saturação", pg.locator("#cdGestor").count() == 1)
    calc = pg.evaluate("""async ()=>{ const h = await db.list('historico_mensal'), vs = await db.list('vestigios'), cs = await db.list('conteineres');
        const p = cdProjecao(h, 6), sat = cs.map(c=>({c, ...cdSaturacao(c, vs)}));
        return {ocupacao: p.ocupacao, projecao: p.mensal[p.mensal.length-1].ocupacao, saturados: sat.filter(x=>x.alerta).length}; }""")
    ok("a ocupação e a projeção batem com o cálculo", pg.inner_text("[data-cd-ind=ocupacao]") == str(calc["ocupacao"])
       and pg.inner_text("[data-cd-ind=projecao]") == str(calc["projecao"]))
    ok("os contêineres em alerta são contados", pg.inner_text("[data-cd-ind=saturados]") == str(calc["saturados"]))
    ok("o painel tem os três gráficos em SVG", pg.locator("svg[role=img]").count() == 3)
    ok("a tabela de saturação mostra ocupação e capacidade", pg.locator("#tabelaSat tr").count() == 6)

# origem: sprint4.py
@cenario
def s5_descarte_com_autorizacao(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    # cria um vestígio antigo de roupa (apto ao descarte)
    vid = pg.evaluate("""async ()=>{ const cat = (await db.list('categorias')).find(c=>c.id_categoria==='roupas'); const cs = await db.list('conteineres');
        const c = cs.find(x=>x.categoria_permitida === 'roupas' || x.categoria_permitida === 'todas') || cs[0];
        await db.put('vestigios', {id_vestigio: 'V-ANTIGO', protocolo: 'PROC-ANTIGO', lacre: 'LC-ANTIGO', categoria_id: cat.id_categoria,
          volume_ocupado: 1, data_entrada: '2019-01-10', status: 'armazenado', descricao: 'Item antigo fictício', conteiner_id: c.id_conteiner, posicao: 'P999'});
        return 'V-ANTIGO'; }""")
    ir(pg, url, "#/vestigio/" + vid, 700)
    ok("o bloco de descarte mostra a idade e a regra da categoria", pg.locator("#cdDescarte").count() == 1
       and "ano(s)" in pg.inner_text("#cdDescarte"))
    ok("sem autorização, o botão de descartar não existe", pg.locator("#btnCdDescartar").count() == 0)
    pg.fill("#cdAuthMotivo", "curto")
    pg.click("#formCdAutorizar button[type=submit]"); pg.wait_for_timeout(400)
    ok("motivo curto é recusado", "15 caracteres" in pg.inner_text("#cdErrosDescarte"))
    pg.fill("#cdAuthMotivo", "Prazo da categoria vencido e sem interesse pericial.")
    pg.click("#formCdAutorizar button[type=submit]"); pg.wait_for_timeout(700)
    ok("a autorização é registrada com responsável e data", pg.evaluate("async id => { const d = (await db.porIndice('descartes','vestigio_id',id))[0]; return d && d.autorizado_por && d.autorizado_em; }", vid))
    ok("com autorização, o descarte fica disponível", pg.locator("#btnCdDescartar").count() == 1)
    pg.click("#btnCdDescartar"); pg.wait_for_timeout(800)
    ok("o vestígio é descartado e a movimentação registrada", pg.evaluate("async id => (await db.get('vestigios', id)).status === 'descartado'", vid)
       and pg.evaluate("async id => (await db.porIndice('movimentacoes','vestigio_id',id)).some(m=>m.tipo==='descarte')", vid))

# origem: sprint4.py
@cenario
def s6_relatorio_e_aceite(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    ir(pg, url, "#/painel", 800)
    ok("o painel mostra o tempo médio até a primeira movimentação", pg.locator("[data-cd-ind=localizacao]").count() == 1)
    with pg.expect_download() as dl:
        pg.click("#btnCdCsvGestor")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV de ocupação e movimentações sai com BOM e ponto e vírgula", csv.startswith(b"\xef\xbb\xbf") and b"id;protocolo;lacre" in csv)
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
