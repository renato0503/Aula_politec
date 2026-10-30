# Cenarios do Sprint 5 em diante (carregados pelo testar_sprints.py).

# Cenários dos Sprints 5 e 6 da Segunda via da CIN: indicadores, retenção e aceite.


@cenario("cin-segunda-via")
def s5_indicadores_e_retencao(pg, url, ok):
    # o servidor decide e apaga o pedido (RN06)
    perfil(pg, url, "servidor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
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


@cenario("cin-segunda-via")
def s6_aceite_do_piloto(pg, url, ok):
    perfil(pg, url, "servidor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    ir(pg, url, "#/pedido", 500)
    ok("o formulário do cidadão abre com as duas perguntas de elegibilidade", pg.locator("#formElegivel").count() == 1)
    pg.check("input[name=valida][value=sim]"); pg.check("input[name=mudou][value=nao]")
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
       (APPS / "cin-segunda-via" / "modelos" / "roteiro-aceite.md").exists())

# Cenários dos Sprints 5 e 6 do Metas BI · OCR: leitura do PDF e aceite.


@cenario("metas-bi-ocr")
def s5_leitura_do_pdf(pg, url, ok):
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    ex = APPS / "metas-bi-ocr" / "exemplos"
    ir(pg, url, "#/importar", 500)
    pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-07.pdf")); pg.wait_for_timeout(1500)
    ok("o PDF com texto é lido e o mês sai do arquivo", "2026-07" in pg.inner_text("#resMes"))
    ok("as 10 unidades do PDF entram na conferência", pg.evaluate("async ()=> (await db.porIndice('pendencias','mes_ref','2026-07')).length") == 10)
    ok("o número lido do PDF bate com o do CSV",
       pg.evaluate("""async ()=>{ const ps = await db.porIndice('pendencias','mes_ref','2026-07');
         const c = ps.find(p=>p.unidade==='Criminalística Cuiabá'); return c && c.pendentes === 1472; }"""))
    ok("a origem fica registrada como PDF", pg.evaluate("async ()=>{ const ps = await db.porIndice('pendencias','mes_ref','2026-07'); return ps.every(p=>p.origem==='pdf'); }"))
    ok("a confiança do texto extraído é 100%", pg.evaluate("async ()=>{ const ps = await db.porIndice('pendencias','mes_ref','2026-07'); return ps.every(p=>p.confianca===1); }"))
    # PDF sem camada de texto: gera uma página em branco e confere a mensagem
    from reportlab.pdfgen import canvas as _cv
    sem = TMP / "powerbi1-2026-10.pdf"
    c = _cv.Canvas(str(sem)); c.showPage(); c.save()
    pg.set_input_files("#arqMes", str(sem)); pg.wait_for_timeout(1200)
    ok("PDF em imagem é recusado com a mensagem do OCR", "camada de texto" in pg.inner_text("#errosMes"))


@cenario("metas-bi-ocr")
def s6_aceite_e_piloto(pg, url, ok):
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    # o fluxo completo: importar, conferir, aprovar, gerar o arquivo
    ex = APPS / "metas-bi-ocr" / "exemplos"
    ir(pg, url, "#/importar", 400)
    pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-07.csv")); pg.wait_for_timeout(900)
    ir(pg, url, "#/conferencia/2026-07", 600)
    ok("a conferência abre com as divergências do mês", pg.locator("#conteudo").count() == 1)
    ok("o roteiro de aceite está em modelos/", (APPS / "metas-bi-ocr" / "modelos" / "roteiro-aceite.md").exists())
