"""Cenários de interface do NIHDE: usa a tela como uma pessoa usaria.

Uso: python testes/cenarios.py
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
    fim = time.time() + timeout
    while time.time() < fim:
        if pg.evaluate(expr, arg):
            return True
        pg.wait_for_timeout(150)
    raise AssertionError("tempo esgotado: " + expr[:70])


def semear(pg, url):
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


@cenario
def s1_painel_e_identificacao(pg, url, ok):
    semear(pg, url)
    ir(pg, url, "#/painel", 800)
    ok("o painel responde quantos não identificados", pg.inner_text("[data-ni=nao-identificados]") == "11" and pg.inner_text("[data-ni=total]") == "24")
    ok("o painel conta não reclamados e sepultados", pg.inner_text("[data-ni=nao-reclamados]") == "4" and pg.inner_text("[data-ni=sepultados]") == "5")
    cid = pg.evaluate("async () => (await db.list('corpos')).find(c => c.situacao === 'não identificado').id")
    ir(pg, url, "#/corpo/" + cid, 800)
    ok("a ficha mostra as quatro vias de exame", pg.locator("[id^=niEx_]").count() == 4)
    pg.select_option("#niEx_DNA", "positivo"); pg.fill("#niProto_DNA", "EX-TESTE"); pg.fill("#niData_DNA", "2026-10-01")
    pg.click("#btnNiExames"); pg.wait_for_timeout(700)
    ok("os exames ficam gravados", pg.evaluate("async id => (await db.get('corpos', id)).exames.DNA.status", cid) == "positivo")
    pg.select_option("#niViaIdent", "DNA"); pg.fill("#niDataIdent", "2026-10-02"); pg.click("#btnNiIdent"); pg.wait_for_timeout(700)
    ok("a identificação pela DNA muda a situação", pg.inner_text("#niSitAtual") == "identificado")
    pg.click("#btnNiBusca"); pg.wait_for_timeout(500)
    pg.fill("#niFamNome", "Familiar Fictício"); pg.fill("#niFamParentesco", "irmã"); pg.fill("#niFamContato", "contato@exemplo.gov.br")
    pg.click("#btnNiFam"); pg.wait_for_timeout(600)
    pg.click("#btnNiEntregar"); pg.wait_for_timeout(700)
    ok("a entrega exige e registra a família", pg.inner_text("#niSitAtual") == "entregue")
    ok("a auditoria registra as ações", "identificação registrada" in pg.inner_text("#conteudo") and "corpo entregue à família" in pg.inner_text("#conteudo"))


@cenario
def s2_entrada_duplicada_e_sepultamento(pg, url, ok):
    semear(pg, url)
    ir(pg, url, "#/corpo/novo", 600)
    pg.fill("#niProt", "2026.0001"); pg.fill("#niMun", "Cuiabá"); pg.fill("#niLocal", "Local de teste")
    pg.click("#formNiNovo button[type=submit]"); pg.wait_for_timeout(600)
    ok("protocolo repetido é recusado", "já está registrado" in pg.inner_text("#niErrosNovo"))
    pg.fill("#niProt", "2026.9999"); pg.fill("#niMun", "Cuiabá"); pg.fill("#niLocal", "Local de teste"); pg.select_option("#niSexo", "Feminino")
    pg.click("#formNiNovo button[type=submit]"); pg.wait_for_timeout(800)
    ok("uma entrada nova abre a ficha", contar(pg, "corpos") == 25 and "#/corpo/C-0025" in pg.url)
    cid = pg.evaluate("async () => (await db.list('corpos')).find(c => !c.identificado && !c.sepultamento).id")
    ir(pg, url, "#/corpo/" + cid, 800)
    ok("o sepultamento fica disponível depois de 30 dias", pg.is_enabled("#btnNiSepultar"))
    pg.fill("#niSepLocal", "Cemitério de teste"); pg.fill("#niSepCert", "CO-TESTE"); pg.click("#btnNiSepultar"); pg.wait_for_timeout(800)
    ok("o sepultamento muda a situação", pg.inner_text("#niSitAtual") == "sepultado")
    pg.select_option("#niViaIdent", "odontologia"); pg.fill("#niDataIdent", "2026-10-20"); pg.click("#btnNiIdent"); pg.wait_for_timeout(800)
    ok("a identificação depois do sepultamento é registrada", pg.inner_text("#niSitAtual") == "identificado após sepultamento")


@cenario
def s3_relatorio_e_csv(pg, url, ok):
    semear(pg, url)
    ir(pg, url, "#/relatorio", 800)
    ok("o relatório tem a tabela por unidade", pg.locator("#tabelaRel tr").count() == 6)
    with pg.expect_download() as d:
        pg.click("#btnNiCsv")
    arq = pathlib.Path(d.value.path())
    csv = arq.read_bytes()
    ok("o CSV sai com BOM e as colunas do corpo", csv.startswith(b"\xef\xbb\xbf") and b"protocolo;unidade" in csv and b"sepultado" in csv)


@cenario
def s4_desaparecidos_e_fontes(pg, url, ok):
    ir(pg, url, "#/desaparecidos", 1200)
    ok("o módulo CNPD mostra 381 registros", pg.locator("#conteudo .kpi .v").first.inner_text() == "381")
    ok("o mapa do CNPD desenha as localidades", pg.locator("#desMapa path.leaflet-interactive").count() > 0)
    pg.select_option("#desUf", "AL"); pg.wait_for_timeout(700)
    ok("o filtro de UF reduz o recorte", pg.locator("#conteudo .kpi .v").first.inner_text() == "151")
    pg.click('[data-des-fonte="namus"]'); pg.wait_for_timeout(1000)
    ok("o NamUs carrega a amostra e o mapa", pg.locator("#conteudo .kpi .v").first.inner_text() == "300" and pg.locator("#desMapa path.leaflet-interactive").count() > 0)
    pg.click('[data-des-fonte="fontes"]'); pg.wait_for_timeout(400)
    ok("o catálogo lista as fontes", pg.locator("#conteudo table tbody tr").count() >= 15)
    with pg.expect_download() as d:
        pg.click('[data-des-fonte="cnpd"]'); pg.wait_for_timeout(700)
        pg.click("#desCsv")
    csv = pathlib.Path(d.value.path()).read_bytes()
    ok("o CSV do módulo sai com BOM, fonte, data e as colunas", csv.startswith(b"\xef\xbb\xbf") and b"fonte;id;nome" in csv and b"CNPD/MJ" in csv and b"coletado_em" in csv)


@cenario
def s5_cruzamento_cnpd_corpos(pg, url, ok):
    semear(pg, url)
    par = pg.evaluate("""async ()=>{
      const d = dadosEmbutidos('cnpd').registros.find(x=>x.sexo && x.idadeAtual != null && x.localRegistro?.includes('/'));
      if (!d) return null;
      const [cidade] = d.localRegistro.split('/');
      const m = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(d.dataDesaparecimento || '');
      const iso = m ? `${m[3]}-${m[2]}-${m[1]}` : '2026-01-01';
      const dt = new Date(iso + 'T12:00:00'); dt.setDate(dt.getDate() + 30);
      const corpoId = 'C-TESTE-CRUZAMENTO';
      await db.put('corpos', {id: corpoId, protocolo: '2026.9999', unidade: 'IML Cuiabá', sexo: d.sexo,
        idade: d.idadeAtual, altura: '1,65', municipio: cidade, data_localizacao: dt.toISOString().slice(0,10),
        olhos: 'castanhos', cabelo: 'preto', pele: 'parda', sinais: 'cicatriz', identificado: false, situacao: 'não identificado'});
      return {id: d.id, nome: d.nome};
    }""")
    ok("há um par fictício para o cruzamento", bool(par))
    pg.reload(); pg.wait_for_function("()=>typeof db!=='undefined'&&!!db.con"); pg.wait_for_timeout(500)
    ir(pg, url, "#/desaparecidos", 700)
    pg.fill("#desQ", par["nome"]); pg.wait_for_timeout(500)
    botao = pg.query_selector(f'[data-des-match="{par["id"]}"]')
    ok("o registro tem o botão de ver corpos", botao is not None)
    if botao: pg.click(f'[data-des-match="{par["id"]}"]'); pg.wait_for_timeout(500)
    ok("o cruzamento lista o corpo compatível", "C-TESTE-CRUZAMENTO" in pg.inner_text("#conteudo") or "2026.9999" in pg.inner_text("#conteudo"))
    pg.fill("#desMatchJust", "Mesmo sexo, idade, altura e município; indício para revisão humana e exames complementares.")
    pg.click('[data-des-confirmar="C-TESTE-CRUZAMENTO"]'); pg.wait_for_timeout(700)
    ok("a confirmação fica na auditoria", pg.evaluate("async ()=> (await db.porIndice('correspondencias','corpo_id','C-TESTE-CRUZAMENTO')).some(x=>x.status==='confirmado')"))


def main():
    erro = False
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for fn in CENARIOS:
            ctx = nav.new_context(accept_downloads=True)
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
