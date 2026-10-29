# Cenários do Sprint 4 (carregados pelo testar_sprints.py).


@cenario("cin-segunda-via")
def s4_protocolo_do_cidadao(pg, url, ok):
    perfil(pg, url, "servidor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    prot = pg.evaluate("async ()=> (await db.list('pedidos')).find(p=>p.situacao==='recebido').protocolo")
    ir(pg, url, "#/protocolo/" + prot, 500)
    ok("o protocolo mostra a situação e os dados do pedido", pg.inner_text("#sitProtocolo").startswith("Recebido") and "Validade da CIN" in pg.inner_text("#conteudo"))
    pg.evaluate("""async p => { const x = await db.get('pedidos', p); await db.put('pedidos', {...x, situacao: 'recusado', motivo: 'Foto ilegível'});
        await db.put('decisoes', {id: 'd-teste', protocolo: p, resultado: 'recusado', motivo: 'Foto ilegível', servidor: 'servidor', data: agora()}); }""", prot)
    ir(pg, url, "#/pedido", 200); ir(pg, url, "#/protocolo/" + prot, 400)
    ok("a recusa mostra o motivo e a decisão", pg.inner_text("#sitProtocolo") == "Recusado" and pg.inner_text("#motivoProtocolo") == "Foto ilegível" and "Foto ilegível" in pg.inner_text("#conteudo"))
    ir(pg, url, "#/protocolo/2V-00000000-XXXX", 400)
    ok("protocolo inexistente mostra o aviso", "não encontrado" in pg.inner_text("#conteudo"))


@cenario("metas-bi-ocr")
def s4_exportar_mes(pg, url, ok):
    ex = APPS / "metas-bi-ocr" / "exemplos"
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(600)
    ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-09.csv")); pg.wait_for_timeout(800)
    ir(pg, url, "#/exportar/2026-09", 500)
    ok("mês não aprovado não libera a exportação (RN05)", pg.locator("#btnCsv").count() == 0 and "precisa ser aprovado" in pg.inner_text("#avisoNaoAprovado"))
    pg.evaluate("""async ()=>{ const r = await db.get('relatorios','2026-09');
        await db.put('relatorios', {...r, aprovado_por: 'Chefe Teste', aprovado_em: agora()}); }""")
    ir(pg, url, "#/historico", 200); ir(pg, url, "#/exportar/2026-09", 500)
    ok("mês aprovado mostra as três formas de baixar", pg.locator("#btnCsv").count() == 1 and pg.locator("#btnXlsx").count() == 1 and pg.locator("#btnCopiar").count() == 1)
    ok("a tabela de exportação tem as unidades do mês", len(pg.query_selector_all("#tabelaExport tr")) > 2)
    with pg.expect_download() as dl:
        pg.click("#btnCsv")
    arq = TMP / "metas-2026-09.csv"; dl.value.save_as(arq)
    dados = arq.read_bytes()
    ok("CSV com BOM, ponto e vírgula e a coluna da planilha", dados.startswith(b"\xef\xbb\xbf") and "Unidade;Laudos pendentes".encode() in dados)
    with pg.expect_download() as dl2:
        pg.click("#btnXlsx")
    ok("Excel gerado com o nome do mês", dl2.value.suggested_filename == "metas-2026-09.xlsx")
