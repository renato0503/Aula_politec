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
def s2_pasta_do_caso(pg, url, ok):
    ex = PASTA / "exemplos"
    def inventario(caso):
        ir(pg, url, "#/inicio", 300); pg.click("#btnNovoCaso"); pg.wait_for_timeout(400)
        pg.set_input_files("#inpPasta", str(ex / caso)); pg.wait_for_timeout(800)
        return pg.evaluate("async ()=> (await db.get('casos', await db.meta('caso_atual'))).inventario")
    inv = inventario("caso-ficticio-001")
    st = {i["chave"]: i["status"] for i in inv["itens"]}
    ok("caso 001: requisição, device e hash presentes", st.get("requisicao") == st.get("device") == st.get("hash") == "presente")
    ok("caso 001: 2 cartões SIM (01-A e 01-B)", inv["qtdSims"] == 2 and "sim:01-A" in st and "sim:01-B" in st)
    ok("caso 001: cronômetro iniciado", pg.evaluate("async ()=> !!(await db.get('casos', await db.meta('caso_atual'))).inicio_em"))
    inv = inventario("caso-ficticio-002")
    ok("caso 002: sem SIM e sem erro (RN06)", inv["qtdSims"] == 0 and not inv["faltando"])
    inv = inventario("caso-ficticio-003")
    ok("caso 003: acusa o HASHDOHASH.txt ausente", inv["faltando"] == ["hash"])
    pg.click("#btnAvancar"); pg.wait_for_timeout(300)
    ok("caso 003: avançar é bloqueado (RN02)", "HASHDOHASH" in pg.inner_text("#avisoAvancar") and "#/arquivos" in pg.url)
    pg.check("[data-manual=hash]"); pg.wait_for_timeout(200); pg.click("#btnAvancar"); pg.wait_for_timeout(300)
    ok("informar manualmente libera o avanço", "#/dados" in pg.url)
    ok("3 casos criados", contar(pg, "casos") == 3)
    ok("os originais não mudaram de tamanho", (ex / "caso-ficticio-001" / "DEVICE INFO.txt").stat().st_size > 0)

# origem: sprint3.py
@cenario
def s3_extratores(pg, url, ok):
    import json
    ex = PASTA / "exemplos"
    for caso in ("caso-ficticio-001", "caso-ficticio-002", "caso-ficticio-003"):
        g = json.loads((ex / caso / "GABARITO.json").read_text(encoding="utf-8"))
        ir(pg, url, "#/inicio", 300); pg.click("#btnNovoCaso"); pg.wait_for_timeout(400)
        pg.set_input_files("#inpPasta", str(ex / caso)); pg.wait_for_timeout(700)
        if pg.locator("[data-manual]").count():
            pg.check("[data-manual]"); pg.wait_for_timeout(200)
        pg.click("#btnAvancar"); pg.wait_for_timeout(1000)
        r = pg.evaluate("""async ()=>{ const id = await db.meta('caso_atual');
            return {ap: (await db.porIndice('aparelhos','id_caso',id))[0], hs: (await db.porIndice('hashes','id_caso',id))[0], sims: await db.porIndice('sims','id_caso',id)}; }""")
        ap = r["ap"]; a = g["aparelho"]
        ok(f"{caso}: marca, modelo e IMEIs iguais ao gabarito", ap and ap["marca"]["valor"] == a["marca"] and ap["modelo"]["valor"] == a["modelo"] and ap["imei_1"]["valor"] == a["imei_1"]
           and ((ap["imei_2"] or {}).get("valor", "") == a["imei_2"]))
        ok(f"{caso}: IMEIs com Luhn válido", ap["imei_1"]["valido"] and (not a["imei_2"] or ap["imei_2"]["valido"]))
        ok(f"{caso}: hash igual ao gabarito (ou ausente quando falta o arquivo)", (r["hs"] or {}).get("valor_hash", {}).get("valor") == g["hash"] if g["hash"] else r["hs"] is None)
        sims = {s["identificador_objeto"]: (s["iccid"]["valor"], s["operadora"]["valor"]) for s in r["sims"]}
        ok(f"{caso}: SIMs iguais ao gabarito ({len(g['sims'])})", sims == {s["identificador_objeto"]: (s["iccid"], s["operadora"]) for s in g["sims"]})
    ir(pg, url, "#/testes", 800)
    ok("testes dos extratores todos verdes", pg.evaluate("window.__testes.every(t=>t.ok)"))

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
