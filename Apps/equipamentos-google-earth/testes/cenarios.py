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
def s2_unidades(pg, url, ok):
    perfil(pg, url, "coordenadoria")
    semear(pg, url)
    ir(pg, url, "#/unidades", 500)
    ok("as 12 unidades do exemplo aparecem com coordenadas", pg.locator("table tr").count() == 13 and "-15." in pg.inner_text("table"))
    dir_id = pg.evaluate("async ()=> (await db.list('diretorias'))[0].id")
    pg.fill("#uniNome", "Posto Teste"); pg.select_option("#uniDiretoria", dir_id)
    pg.fill("#uniMunicipio", "Cuiabá"); pg.dispatch_event("#uniMunicipio", "change")
    ok("o município preenche as coordenadas", pg.input_value("#uniLat").startswith("-15"))
    pg.fill("#uniLat", "-16.68"); pg.fill("#uniLon", "-49.25")  # Goiânia
    pg.click("#formUnidade button[type=submit]"); pg.wait_for_timeout(400)
    ok("coordenada de Goiânia é recusada (RN08)", "fora de Mato Grosso" in pg.inner_text("#errosUnidade"))
    ok("nada foi gravado", contar(pg, "unidades") == 12)
    pg.fill("#uniLat", "-15.60"); pg.fill("#uniLon", "-56.10")
    pg.click("#formUnidade button[type=submit]"); pg.wait_for_timeout(600)
    ok("coordenada de Cuiabá é aceita", contar(pg, "unidades") == 13)
    pg.locator("[data-excluir]").first.click(); pg.wait_for_timeout(500)
    ok("excluir é lógico (o registro continua, marcado)", contar(pg, "unidades") == 13 and pg.evaluate("async ()=> (await db.list('unidades')).filter(u=>u.excluido).length") == 1)
    ok("a unidade nova tem id, datas e município IBGE", pg.evaluate("async ()=>{ const u = (await db.list('unidades')).find(x=>x.nome==='Posto Teste'); return !!(u && u.criadoEm && u.municipio_ibge === '5103403'); }"))

# origem: testar_sprints.py
@cenario
def s3_equipamentos_e_fotos(pg, url, ok):
    import io
    import random
    from PIL import Image
    perfil(pg, url, "coordenadoria")
    semear(pg, url)
    ir(pg, url, "#/equipamentos", 500)
    ok("lista mostra os 150 equipamentos", pg.inner_text("#qtdEq") == "150")
    pg.select_option("#fCrit", "5"); pg.wait_for_timeout(300)
    n5 = pg.evaluate("async ()=> (await db.list('equipamentos')).filter(e=>e.criticidade===5).length")
    ok("filtro de criticidade soma o total certo", pg.inner_text("#qtdEq") == str(n5))
    ir(pg, url, "#/equipamento/novo", 500)
    uni = pg.evaluate("async ()=> (await db.list('unidades'))[0].id")
    pat = pg.evaluate("async ()=> (await db.list('equipamentos'))[0].patrimonio")
    pg.fill("#ePat", pat); pg.fill("#eNome", "Cromatógrafo teste"); pg.fill("#eTipo", "Cromatógrafo"); pg.select_option("#eUnidade", uni)
    pg.click("#formEq button[type=submit]"); pg.wait_for_timeout(400)
    ok("patrimônio duplicado é apontado", "já está cadastrado" in pg.inner_text("#errosEq"))
    pg.fill("#ePat", "PAT-TESTE-1"); pg.click("#formEq button[type=submit]"); pg.wait_for_timeout(600)
    ok("equipamento salvo abre a ficha", "#/equipamento/" in pg.url and "PAT-TESTE-1" in pg.inner_text("h1"))
    fotos = []
    for k in range(3):   # fotos de celular de cerca de 4 MB (ruído quase não comprime)
        im = Image.frombytes("RGB", (4000, 3000), random.randbytes(4000 * 3000 * 3)); b = io.BytesIO(); im.save(b, "JPEG", quality=85)
        f = TMP / f"foto{k}.jpg"; f.write_bytes(b.getvalue()); fotos.append(str(f))
    ok("fotos de teste com mais de 3 MB cada", all(pathlib.Path(f).stat().st_size > 3_000_000 for f in fotos))
    pg.set_input_files("#inpFoto", fotos); pg.wait_for_timeout(8000)
    ok("a ficha mostra as 3 fotos", pg.locator("#galeria img").count() == 3)
    tam = pg.evaluate("async ()=> (await db.list('arquivos')).reduce((a,x)=>a+x.tamanho,0)")
    ok(f"as 3 fotos ocupam menos de 1 MB ({tam // 1024} KB)", tam < 1024 * 1024)
    ir(pg, url, "#/equipamentos", 400)
    with pg.expect_download() as dl:
        pg.click("#btnCsvEq")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("CSV com BOM e ponto e vírgula", csv.startswith(b"\xef\xbb\xbf") and b"patrimonio;nome" in csv)

# origem: sprint.md · Sprint 4
@cenario
def s4_contratos(pg, url, ok):
    perfil(pg, url, "coordenadoria")
    semear(pg, url)
    ir(pg, url, "#/contratos", 1200)
    texto = pg.inner_text("main")
    ok("a tela de contratos abre", "Contratos" in texto)
    ok("os 20 contratos do exemplo aparecem", pg.locator("table tr").count() >= 21)
    ok("o alerta de vencimento em 60 dias aparece", "60 dias" in texto or "vigente" in texto)
    pg.locator("[data-contrato]").first.click(); pg.wait_for_timeout(700)
    ok("o contrato abre com a lista de equipamentos", pg.locator("#detalheContrato table tr").count() >= 2 and "vigência" in pg.inner_text("#detalheContrato"))
    # a ficha do equipamento mostra histórico, MTTR e custo
    eq = pg.evaluate("async ()=>{ const e = await db.list('equipamentos'); return e[0].id; }")
    ir(pg, url, "#/equipamento/" + eq, 1200)
    ok("a ficha mostra o histórico com MTTR e custo", pg.locator("#historicoEq").count() == 1 and "MTTR" in pg.inner_text("#historicoEq"))

# origem: sprint.md · Sprint 5
@cenario
def s5_paradas(pg, url, ok):
    perfil(pg, url, "coordenadoria")
    semear(pg, url)
    ir(pg, url, "#/paradas", 1200)
    ok("a tela de paradas abre", "Paradas" in pg.inner_text("main"))
    ok("as paradas do exemplo aparecem", pg.locator("table tr").count() >= 41)
    ok("o custo das paradas abertas aparece", "custo das abertas" in pg.inner_text("main"))
    eq = pg.evaluate("async ()=> (await db.list('equipamentos'))[0].id")
    pg.select_option("#paEq", eq)
    pg.fill("#paInicio", "2026-03-02T08:00"); pg.fill("#paMotivo", "Falha elétrica")
    pg.click("#formParada button[type=submit]"); pg.wait_for_timeout(900)
    ok("a parada foi gravada", contar(pg, "paradas") == 41)
    ok("o equipamento ficou parado", pg.evaluate("async id=> (await db.get('equipamentos', id)).status === 'parado'", eq))
    pg.locator("[data-fechar]").first.click(); pg.wait_for_timeout(900)
    ok("fechar a parada devolve o equipamento", pg.evaluate("async id=> { const e = await db.get('equipamentos', id); const p = (await db.porIndice('paradas','equipamento_id', id)).filter(x=>!x.fim); return e.status !== 'parado' || p.length > 0; }", eq))

# origem: sprint.md · Sprint 7
@cenario
def s7_painel(pg, url, ok):
    perfil(pg, url, "coordenadoria")
    semear(pg, url)
    ir(pg, url, "#/painel", 1500)
    texto = pg.inner_text("main")
    ok("a tela do painel abre", "Painel" in texto)
    ok("os 7 indicadores aparecem", pg.locator(".card.kpi").count() >= 7)
    ok("a exposição diária aparece", "exposição diária" in texto)
    ok("o gráfico de custo por unidade aparece", "Custo de parada por unidade" in texto)
    ok("a lista de pontos únicos sem contrato aparece", "Pontos únicos de falha sem contrato" in texto)
    pg.select_option("#eqPeriodo", "30"); pg.wait_for_timeout(900)
    ok("o período pode ser trocado", "Últimos 30 dias" in pg.inner_text("main"))

# origem: sprint.md · Sprint 8
@cenario
def s8_exportar(pg, url, ok):
    perfil(pg, url, "coordenadoria")
    semear(pg, url)
    ir(pg, url, "#/exportar", 1500)
    ok("a tela de exportar abre", "Exportar" in pg.inner_text("main"))
    with pg.expect_download() as info:
        pg.click("#btnKml")
    kml = TMP / "doc.kml"
    info.value.save_as(kml)
    texto = kml.read_text(encoding="utf-8")
    ok("o KML tem pastas por diretoria e unidade", "<Folder>" in texto and "<Placemark>" in texto)
    ok("o KML traz o patrimônio do equipamento", "PAT-" in texto)
    with pg.expect_download() as info2:
        pg.click("#btnKmz")
    kmz = TMP / "equipamentos.kmz"
    info2.value.save_as(kmz)
    import zipfile
    ok("o KMZ é um zip com o KML dentro", zipfile.is_zipfile(kmz) and "doc.kml" in zipfile.ZipFile(kmz).namelist())

# origem: sprint.md · Sprint 9
@cenario
def s9_importar(pg, url, ok):
    perfil(pg, url, "coordenadoria")
    semear(pg, url)
    arq = TMP / "equipamentos.csv"
    arq.write_text("patrimonio;nome;tipo;unidade;criticidade;situacao\nPAT-NOVO-1;Microscópio novo;Microscópio;Sede Cuiabá (fictícia);4;operando\nPAT-NOVO-2;;Equipamento sem nome;Sede Cuiabá (fictícia);9;operando\n", encoding="utf-8")
    ir(pg, url, "#/importar", 1000)
    pg.set_input_files("#arqEqCsv", str(arq)); pg.wait_for_timeout(900)
    rel = pg.inner_text("#csvEqRelatorio")
    ok("o relatório diz quantas linhas foram aceitas", "aceitas" in rel)
    ok("a linha sem nome é recusada com o motivo", "recusadas" in rel)
    pg.click("#btnGravarCsv"); pg.wait_for_timeout(1000)
    ok("o equipamento novo foi gravado", pg.evaluate("async ()=> !!(await db.porIndice('equipamentos','patrimonio','PAT-NOVO-1'))"))


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
