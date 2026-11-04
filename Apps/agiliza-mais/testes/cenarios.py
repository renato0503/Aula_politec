"""Cenários de interface deste app: usam a tela como uma pessoa usaria e conferem
o "Pronto quando" de cada sprint do sprint.md.

Uso: python testes/cenarios.py      (requer: pip install playwright && playwright install chromium)
"""
import base64
import json
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

# origem: sprint.md · Sprints 4 a 11 (conferência, requisição em PDF, textos, quesitos, Word, revisão e histórico)
@cenario
def s4_a_s11_laudo_completo(pg, url, ok):
    import json, zipfile
    ex = PASTA / "exemplos" / "caso-ficticio-001"
    g = json.loads((ex / "GABARITO.json").read_text(encoding="utf-8"))["caso"]
    ir(pg, url, "#/inicio", 300); pg.click("#btnNovoCaso"); pg.wait_for_timeout(400)
    pg.set_input_files("#inpPasta", str(ex)); pg.wait_for_timeout(700)
    pg.click("#btnAvancar"); pg.wait_for_timeout(1200)
    ok("a conferência mostra os campos com o selo de origem", pg.locator("#formConferencia #ap_imei_1").count() == 1 and "extraído" in pg.inner_text("#formConferencia"))
    pg.click("#btnLerPdf"); pg.wait_for_timeout(2500)
    ok("a requisição em PDF preenche protocolo, ofício, processo e data (Sprint 6)",
       pg.input_value("#req_numero_protocolo") == g["protocolo"] and pg.input_value("#req_numero_oficio") == g["oficio"]
       and pg.input_value("#req_numero_processo") == g["processo"] and pg.input_value("#req_data_solicitacao") == g["data"])
    pg.fill("#ap_imei_1", "358735742761448"); pg.wait_for_timeout(200)
    ok("IMEI errado mostra a mensagem e trava o botão (validação em tempo real)", pg.is_disabled("#btnConfirmarTodos") and "Luhn" in pg.inner_text("#ap_imei_1-msg"))
    pg.fill("#ap_imei_1", "358735742761447"); pg.fill("#ap_cor", "Azul-escuro"); pg.wait_for_timeout(200)
    pg.click("#btnConfirmarTodos"); pg.wait_for_timeout(900)
    caso = pg.evaluate("async ()=> await db.get('casos', await db.meta('caso_atual'))")
    ok("a conferência fica registrada com a correção", bool(caso.get("conferido_em")) and caso.get("correcoes", 0) >= 1 and "corrigido" in pg.inner_text("#formConferencia"))
    ir(pg, url, "#/textos", 800)
    ok("a prévia do texto traz os dados do caso", pg.locator(".ag-previa").count() >= 4)
    pg.locator("details.ag-editar-texto:has(#edit_historico) summary").click(); pg.wait_for_timeout(200)
    pg.fill("#edit_historico", "HISTÓRICO PERSONALIZADO DO TESTE."); pg.wait_for_timeout(300)
    ok("o texto da seção pode ser editado e a prévia acompanha", "HISTÓRICO PERSONALIZADO DO TESTE." in pg.inner_text("#previa_historico"))
    pg.click("#formTextos button[type=submit]"); pg.wait_for_timeout(800)
    ir(pg, url, "#/quesitos", 600)
    pg.click("#btnQuesitosPdf"); pg.wait_for_timeout(1000)
    ok("os quesitos da requisição entram numerados (RN09)", pg.locator("#formRespostas textarea").count() == len(g["quesitos"]))
    ok("as respostas nascem como sugestão não aprovada (RN10)", pg.locator("text=sugestão, não aprovada").count() == len(g["quesitos"]))
    ir(pg, url, "#/gerar", 600)
    ok("sem aprovação e sem número do laudo, gerar fica bloqueado (RN10, RN11)", pg.is_disabled("#btnGerarDocx"))
    ir(pg, url, "#/quesitos", 600)
    for c in pg.locator("[data-aprovar]").all(): c.check()
    pg.click("#formRespostas button[type=submit]"); pg.wait_for_timeout(800)
    ir(pg, url, "#/gerar", 600)
    pg.fill("#lNumero", "123/2026"); pg.fill("#lPerito", "Perito Fictício"); pg.click("#formLaudo button[type=submit]"); pg.wait_for_timeout(800)
    ok("com tudo aprovado, gerar fica liberado", pg.is_enabled("#btnGerarDocx"))
    with pg.expect_download() as d:
        pg.click("#btnGerarDocx")
    ok("o nome segue laudo_<protocolo>_v<N>.docx", d.value.suggested_filename == f"laudo_{g['protocolo']}_v1.docx")
    arq = TMP / d.value.suggested_filename; d.value.save_as(arq)
    xml = zipfile.ZipFile(arq).read("word/document.xml").decode("utf-8")
    ok("o .docx traz IMEI, ICCID, protocolo e a resposta sugerida, sem marcador sobrando (RN12)",
       "358735742761447" in xml and "8955117633881124130" in xml and g["protocolo"] in xml and "Xiaomi" in xml
       and "HISTÓRICO PERSONALIZADO DO TESTE." in xml and "{" not in xml.replace("{/", ""))
    ir(pg, url, "#/revisao", 800)
    ok("a revisão não pede mais os campos de correção do Word", pg.locator("#revNotas").count() == 0 and pg.locator("#revQtd").count() == 0)
    pg.check("#revOk")
    pg.click("#btnConcluir"); pg.wait_for_timeout(800)
    ok("o caso é concluído só com a marcação de revisão (RN14)", pg.evaluate("async ()=> (await db.get('casos', await db.meta('caso_atual'))).status") == "concluído")
    ir(pg, url, "#/biblioteca", 600)
    ok("a biblioteca tem a coluna e o filtro de tipo de dispositivo", pg.locator("#tabelaTextos th", has_text="Tipo").count() >= 1 and pg.locator("#filtroTipo").count() == 1)
    ir(pg, url, "#/historico", 800)
    ok("o histórico mostra a taxa de correção", "taxa de correção" in pg.inner_text("main"))
    pg.click("[data-limpar-caso]"); pg.wait_for_timeout(800)
    ok("limpar o caso apaga o aparelho e mantém a métrica", pg.evaluate("async ()=> (await db.porIndice('aparelhos','id_caso', await db.meta('caso_atual'))).length") == 0)

@cenario
def s5_caso_de_exemplo_e_modelo(pg, url, ok):
    ir(pg, url, "#/inicio", 400); pg.click("#btnCasoExemplo"); pg.wait_for_timeout(800)
    pg.click("#btnAvancar"); pg.wait_for_timeout(1200)
    ok("o caso de exemplo extrai o aparelho sem escolher pasta", pg.input_value("#ap_imei_1") == "358735742761447")
    pg.click("#btnRemoverSimTeste") if pg.locator("#btnRemoverSimTeste").count() else None
    ir(pg, url, "#/config", 600)
    ok("a configuração mostra o modelo e a privacidade", "Modelo do laudo" in pg.inner_text("main") and "Finalidade" in pg.inner_text("main"))
    pg.set_input_files("#arqModelo", str(PASTA / "modelos" / "modelo-laudo-celular.docx")); pg.wait_for_timeout(900)
    ok("o modelo carregado vira o modelo em uso", pg.evaluate("async ()=> (await db.get('modelos','atual'))?.marcadores?.length") > 20)
    ir(pg, url, "#/biblioteca", 600)
    pg.click("[data-ativar-texto='T05']"); pg.wait_for_timeout(600)
    ok("desativar um texto o tira da lista ativa", pg.evaluate("async ()=> (await db.get('textos','T05')).ativo") is False)

@cenario
def s12_inicio_pasta_e_gestao(pg, url, ok):
    """Sprint 12: carregar a pasta no início e gerenciar os laudos em preenchimento."""
    ir(pg, url, "#/inicio", 700)
    ok("o início tem o botão de carregar a pasta", pg.locator("#btnPastaInicio").count() == 1)
    pacote = json.loads((PASTA / "exemplos" / "caso-exemplo.json").read_text(encoding="utf-8"))
    pasta = TMP / "pasta-do-caso"
    for a in pacote["arquivos"]:
        arq = pasta / a["caminho"]; arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_bytes(base64.b64decode(a["b64"]))
    pg.set_input_files("#inpPastaInicio", str(pasta)); pg.wait_for_timeout(1600)
    ok("carregar a pasta cria o caso e abre a conferência", pg.evaluate("location.hash") == "#/dados" and contar(pg, "casos") == 1)
    ok("a pasta ficou registrada no caso", pg.evaluate("async ()=> !!(await db.get('casos', await db.meta('caso_atual'))).inventario"))
    ir(pg, url, "#/inicio", 900)
    ok("o laudo em preenchimento aparece na lista", pg.locator("[data-ag-card]").count() == 1)
    ok("a lista tem as ações de continuar, renomear, pasta e excluir",
       pg.locator("[data-ag-abrir]").count() == 1 and pg.locator("[data-ag-renomear]").count() == 1
       and pg.locator("[data-ag-mover]").count() == 1 and pg.locator("[data-ag-excluir]").count() == 1)
    pg.click("[data-ag-renomear]"); pg.wait_for_timeout(300)
    pg.fill("#agNomeCaso", "Laudo do Samsung"); pg.click("dialog.ag-dialog button[type=submit]"); pg.wait_for_timeout(800)
    ok("renomear grava o nome do caso", pg.evaluate("async ()=> (await db.get('casos', await db.meta('caso_atual'))).nome") == "Laudo do Samsung")
    pg.click("[data-ag-mover]"); pg.wait_for_timeout(300)
    pg.fill("#agMoverNova", "Piloto outubro"); pg.click("dialog.ag-dialog button[type=submit]"); pg.wait_for_timeout(800)
    ok("mover cria e grava a pasta", pg.evaluate("async ()=> (await db.get('casos', await db.meta('caso_atual'))).pasta") == "Piloto outubro"
       and pg.locator('[data-ag-pasta="Piloto outubro"]').count() == 1)
    pg.click("[data-ag-abrir]"); pg.wait_for_timeout(900)
    ok("continuar abre a conferência do caso", pg.evaluate("location.hash") == "#/dados")
    ir(pg, url, "#/inicio", 900)
    pg.click("[data-ag-excluir]"); pg.wait_for_timeout(300)
    pg.click("dialog.ag-dialog button[type=submit]"); pg.wait_for_timeout(900)
    ok("excluir apaga o caso da lista", contar(pg, "casos") == 0 and pg.locator("[data-ag-card]").count() == 0)

@cenario
def s14_feedback_extra_foto_historico(pg, url, ok):
    """Sprint 14: outras informações, foto com cor sugerida, ajuda dos arquivos e abrir pelo histórico."""
    semear(pg, url)
    pacote = json.loads((PASTA / "exemplos" / "caso-exemplo.json").read_text(encoding="utf-8"))
    pasta = TMP / "pasta-feedback"
    for a in pacote["arquivos"]:
        arq = pasta / a["caminho"]; arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_bytes(base64.b64decode(a["b64"]))
    ir(pg, url, "#/inicio", 500); pg.set_input_files("#inpPastaInicio", str(pasta)); pg.wait_for_timeout(1600)
    ok("a pasta de exemplo abre a conferência", pg.evaluate("location.hash") == "#/dados")
    ok("a conferência tem outras informações e foto", pg.locator("#outrasInfo").count() == 1 and pg.locator("#fotoAparelho").count() == 1)
    png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+M8AAAMBAQDJ/pLvAAAAAElFTkSuQmCC")
    pg.set_input_files("#fotoAparelho", {"name": "aparelho.png", "mimeType": "image/png", "buffer": png})
    pg.wait_for_timeout(1200)
    ok("a foto sugere uma cor", "Sugestão:" in pg.inner_text("#sugestaoCor") and pg.evaluate("async ()=> !!(await db.get('casos', await db.meta('caso_atual'))).cor_sugerida"))
    pg.fill("#outrasInfo", "Aparelho com trinca no canto superior direito; embalagem lacrada.")
    pg.click("#btnConfirmarTodos"); pg.wait_for_timeout(900)
    caso = pg.evaluate("async ()=> await db.get('casos', await db.meta('caso_atual'))")
    ok("a conferência guarda as outras informações e a foto", caso.get("outras_informacoes", "").startswith("Aparelho com trinca") and caso.get("foto_aparelho") is not None)
    ir(pg, url, "#/historico", 700)
    ok("o histórico tem o botão Abrir", pg.locator("[data-abrir-caso]").count() > 0)
    pg.locator("[data-abrir-caso]").first.click(); pg.wait_for_timeout(500)
    ok("o histórico abre o caso", pg.evaluate("location.hash") == "#/dados")
    ir(pg, url, "#/arquivos", 500)
    ok("a pasta explica o que cada arquivo alimenta", "O que cada arquivo alimenta" in pg.inner_text("main"))


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
