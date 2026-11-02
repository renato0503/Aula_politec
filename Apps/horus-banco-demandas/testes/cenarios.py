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
def s2_cadastro_demanda(pg, url, ok):
    perfil(pg, url, "USUARIO_SETORIAL")
    semear(pg, url); ir(pg, url, "#/config", 400)
    pg.fill("#cfgUsuario", "teste.usuario"); pg.dispatch_event("#cfgUsuario", "change")
    uni = pg.evaluate("async ()=> (await db.list('unidades'))[0].id"); pg.select_option("#selUnidade", uni); pg.wait_for_timeout(200)
    ir(pg, url, "#/demanda/nova", 400)
    pg.fill("#dValor", "33,33"); pg.fill("#dQtd", "3")
    medida = pg.evaluate("async ()=> (await db.list('unidades_medida'))[0].id"); pg.select_option("#dMedida", medida)
    pg.fill("#dEspec", "Reagente de teste para o laboratório, frasco de 500 mL, validade de 12 meses.")
    pg.fill("#dJust", "x" * 99); pg.fill("#dLinks", "https://exemplo.com/produto")
    ok("valor global calculado na hora (R4)", pg.inner_text("#dGlobal") == "R$ 99,99")
    n0 = contar(pg, "banco_demandas")
    pg.click("#formDemanda button[type=submit]"); pg.wait_for_timeout(400)
    ok("justificativa de 99 caracteres é recusada (R2)", "R2" in pg.inner_text("#errosDemanda") and contar(pg, "banco_demandas") == n0)
    pg.fill("#dJust", "x" * 100)
    pg.set_input_files("#dPdf", {"name": "orcamento.pdf", "mimeType": "application/pdf", "buffer": b"%PDF-1.4 teste"})
    pg.click("#formDemanda button[type=submit]"); pg.wait_for_timeout(500)
    ok("com 100 caracteres, a demanda é salva", contar(pg, "banco_demandas") == n0 + 1)
    d = pg.evaluate("async ()=> (await db.list('banco_demandas')).find(x=>x.criado_por==='teste.usuario')")
    ok("valor global gravado = 99,99", d and d["valor_global"] == 99.99)
    ok("PDF guardado com a demanda", pg.evaluate("async ()=> (await db.list('banco_demandas')).find(x=>x.criado_por==='teste.usuario').arquivo_pdf instanceof Blob"))
    alheia = pg.evaluate("async ()=> (await db.list('banco_demandas')).find(x=>x.criado_por!=='teste.usuario').id")
    ir(pg, url, "#/demanda/" + alheia, 400)
    ok("demanda de outro autor não abre para edição (R8)", "R8" in pg.inner_text("#conteudo") and pg.locator("#formDemanda").count() == 0)
    ir(pg, url, "#/demanda/" + d["id"], 400)
    ok("o autor edita a própria demanda", pg.locator("#formDemanda").count() == 1)

# origem: sprint3.py
@cenario
def s3_grade_e_ficha(pg, url, ok):
    perfil(pg, url, "DIRETOR")
    semear(pg, url)
    ir(pg, url, "#/banco", 500)
    ok("os 15 itens do exemplo aparecem", pg.inner_text("#qtdBanco") == "15" and pg.locator(".cartao-demanda").count() == 15)
    soma = 0
    for g in ("CUSTEIO", "INVESTIMENTO"):
        pg.select_option("#fbGrupo", g); pg.wait_for_timeout(300); soma += int(pg.inner_text("#qtdBanco"))
    ok("filtros por grupo somam o total (15)", soma == 15)
    pg.select_option("#fbGrupo", ""); pg.wait_for_timeout(200); pg.select_option("#fbSituacao", "interesse"); pg.wait_for_timeout(300)
    ok("2 demandas com interesse (exemplo)", pg.inner_text("#qtdBanco") == "2")
    pg.evaluate("""async ()=>{ const d = (await db.list('banco_demandas'))[0], c = (await db.list('ciclos'))[0];
        await db.put('banco_demanda_inclusoes', {id: 'inc-teste', banco_demanda_id: d.id, quadro_id: c.id, demanda_id: null, criado_por: 'teste', created_at: agora()}); }""")
    pg.select_option("#fbSituacao", "aprovada"); pg.wait_for_timeout(300)
    ok("selo Aprovada no ciclo 2027 no card", pg.inner_text("#qtdBanco") == "1" and "Aprovada no ciclo 2027" in pg.inner_text(".cartao-demanda"))
    pg.click(".cartao-demanda"); pg.wait_for_timeout(500)
    ok("a ficha mostra especificação, links e o ciclo", "Especificação técnica" in pg.inner_text("#conteudo") and "Aprovada no ciclo 2027" in pg.inner_text("#conteudo"))
    com = pg.evaluate("async ()=> (await db.list('banco_demanda_manifestacoes'))[0].banco_demanda_id")
    n = pg.evaluate("async id => (await db.porIndice('banco_demanda_manifestacoes','banco_demanda_id',id)).length", com)
    ir(pg, url, "#/demanda/" + com + "/ver", 400)
    ok("a ficha lista as manifestações de interesse", f"Manifestações de interesse ({n})" in pg.inner_text("#conteudo") and n >= 1)

# origem: sprint4.py
@cenario
def s4_troca_de_unidade(pg, url, ok):
    perfil(pg, url, "ADM")
    semear(pg, url)
    ir(pg, url, "#/trocar", 600)
    ok("a tela de troca lista as demandas", pg.locator("#tabelaDemandasTroca tr").count() > 1)
    pg.locator("[data-trocar]").first.click(); pg.wait_for_timeout(500)
    pg.click("#formTroca button[type=submit]"); pg.wait_for_timeout(500)
    ok("a troca sem unidade é recusada", "Escolha a unidade" in pg.inner_text("#errosTroca"))
    destino = pg.evaluate("""async ()=>{ const d = (await db.list('banco_demandas')).find(x=>x.transferencias===undefined);
        const u = (await db.list('unidades')).find(x=>x.id !== d.unidade_id); return {id: d.id, unidade: u.id}; }""")
    pg.locator("[data-trocar]").first.click(); pg.wait_for_timeout(400)
    pg.select_option("#trocaUnidade", destino["unidade"])
    pg.click("#formTroca button[type=submit]"); pg.wait_for_timeout(400)
    ok("a troca sem motivo é recusada", "motivo" in pg.inner_text("#errosTroca"))
    pg.select_option("#trocaUnidade", destino["unidade"]); pg.fill("#trocaMotivo", "Redistribuição da demanda para a unidade que tem o equipamento.")
    pg.click("#formTroca button[type=submit]"); pg.wait_for_timeout(800)
    ok("a troca fica registrada com motivo e histórico",
       pg.evaluate("async ()=> (await db.list('banco_demandas')).some(d=>(d.transferencias||[]).some(t=>t.motivo))"))

# origem: sprint4.py
@cenario
def s5_manifestacao_de_interesse(pg, url, ok):
    perfil(pg, url, "ADM")
    semear(pg, url)
    did = pg.evaluate("async ()=> (await db.list('banco_demandas'))[0].id")
    ir(pg, url, "#/demanda/" + did + "/interesse", 700)
    ok("a tela de interesse lista as manifestações do exemplo", pg.locator("#tabelaManifestacoes").count() == 1)
    ok("quantidade zero e justificativa curta são recusadas pela regra",
       pg.evaluate("()=>{ const f = horFaltaInteresse({quantidade: 0, justificativa: 'curto'}); return f.length === 2 && f.join(' ').includes('quantidade'); }"))
    un = pg.evaluate("async ()=> (await db.list('unidades'))[0].id")
    pg.select_option("#intUnidade", un); pg.fill("#intQtd", "50")
    pg.fill("#intJust", "A unidade usa o mesmo insumo nas triagens diárias.")
    pg.click("#formInteresse button[type=submit]"); pg.wait_for_timeout(800)
    ok("a manifestação é registrada com unidade, quantidade e justificativa",
       pg.evaluate("async id => (await db.porIndice('banco_demanda_manifestacoes','banco_demanda_id',id)).some(m=>m.quantidade===50)", did))

# origem: sprint4.py
@cenario
def s6_ciclo_e_aprovacao(pg, url, ok):
    perfil(pg, url, "ADM")
    semear(pg, url)
    ir(pg, url, "#/ciclos", 700)
    ok("a tela de ciclos mostra o ciclo do exemplo", pg.locator("#tabelaCiclos tr").count() >= 2)
    pg.fill("#cicNome", "PCA 2028"); pg.fill("#cicAno", "2028")
    pg.click("#formCiclo button[type=submit]"); pg.wait_for_timeout(700)
    ok("o ciclo novo entra como encerrado", pg.evaluate("async ()=> (await db.list('ciclos')).some(c=>c.nome==='PCA 2028' && c.status==='ENCERRADO')"))
    ir(pg, url, "#/aprovar", 700)
    ok("a aprovação exige ao menos uma demanda", pg.locator("#tabelaAprovar tr").count() > 1)
    pg.click("#formAprovar button[type=submit]"); pg.wait_for_timeout(500)
    ok("sem seleção, a aprovação é recusada", "Selecione" in pg.inner_text("#errosAprovar"))
    pg.locator("[data-aprovar]").first.check()
    pg.click("#formAprovar button[type=submit]"); pg.wait_for_timeout(800)
    ok("a demanda aprovada entra no ciclo ativo", pg.evaluate("async ()=> (await db.list('banco_demanda_inclusoes')).length >= 1"))

# origem: sprint4.py
@cenario
def s7_relatorio_e_pacote(pg, url, ok):
    perfil(pg, url, "ADM")
    semear(pg, url)
    ir(pg, url, "#/aprovar", 700)
    pg.locator("[data-aprovar]").first.check()
    pg.click("#formAprovar button[type=submit]"); pg.wait_for_timeout(800)
    ir(pg, url, "#/relatorios", 800)
    ok("o relatório conta as demandas aprovadas e o valor", pg.locator("[data-hor-ind=aprovadas]").count() == 1
       and pg.locator("[data-hor-ind=valor]").count() == 1)
    ok("o relatório agrupa por grupo e por unidade", pg.locator("#tabelaGrupo").count() == 1 and pg.locator("#tabelaUnidadeHor").count() == 1)
    with pg.expect_download() as dl:
        pg.click("#btnHorPacote")
    import json as _json
    pacote = _json.loads(pathlib.Path(dl.value.path()).read_text(encoding="utf-8"))
    ok("o pacote do Hórus sai com versão, ciclo e demandas aprovadas",
       pacote.get("versao") == 1 and pacote.get("ciclo") and len(pacote.get("demandas", [])) >= 1)
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
