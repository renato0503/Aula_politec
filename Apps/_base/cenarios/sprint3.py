# Cenários do Sprint 3 (carregados pelo testar_sprints.py; usam cenario, ir, perfil, contar, TMP, APPS)


@cenario("inscricoes-cursos")
def s3_formulario_de_inscricao(pg, url, ok):
    perfil(pg, url, "gerencia")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(600)
    link = pg.evaluate("async ()=> linkInscricao(await db.get('cursos','CURSO-2026-11'))")
    fechado = pg.evaluate("async ()=>{ const c = await db.get('cursos','CURSO-2026-11'); return linkInscricao({...c, id:'X', inscricao_inicio:'2026-01-01', inscricao_fim:'2026-01-31'}); }")
    p2 = pg.context.browser.new_context().new_page()   # o servidor abre o link no próprio navegador
    p2.goto(link); p2.wait_for_timeout(500)
    p2.fill("#iMatricula", "123456"); p2.fill("#iNome", "Servidor Teste"); p2.fill("#iLotacao", "IML Cuiabá"); p2.select_option("#iDiretoria", "DML")
    p2.fill("#iEmail", "servidor@gmail.com"); p2.check("input[name=pre0][value=sim]"); p2.check("input[name=pre1][value=nao]")
    p2.click("#formInscricao button[type=submit]"); p2.wait_for_timeout(300)
    ok("e-mail fora do domínio é recusado ao lado do campo (RN02)", "RN02" in p2.inner_text("#erro-iEmail"))
    p2.fill("#iEmail", "servidor.teste@politec.mt.gov.br"); p2.click("#formInscricao button[type=submit]"); p2.wait_for_timeout(400)
    prot = p2.inner_text("#protInscricao") if p2.locator("#protInscricao").count() else ""
    ok("comprovante com protocolo e situação em análise", len(prot) == 8 and "em análise" in p2.inner_text("#cardComprovante"))
    href = p2.get_attribute("#lnkEmail", "href")
    ok("o e-mail vai para capacitacao@ com o assunto [INSCRICAO] e o protocolo", href.startswith("mailto:capacitacao%40politec.mt.gov.br") and "%5BINSCRICAO%5D" in href and prot in href)
    from urllib.parse import unquote
    corpo = unquote(href.split("body=")[1])
    lido = p2.evaluate("t => blocoInscricao.ler(t)", corpo)
    ok("o bloco do e-mail volta inteiro na leitura da gerência", len(lido) == 1 and lido[0].get("dados", {}).get("m") == "123456" and lido[0]["dados"]["p"] == prot)
    ok("pré-requisito marcado como não atendo fica de fora da declaração", lido[0]["dados"]["r"] == ["Ser servidor efetivo"])
    p2.goto(fechado); p2.wait_for_timeout(400)
    ok("fora do período a inscrição fica fechada (RN04)", p2.locator("#foraPeriodo").count() == 1 and p2.locator("#formInscricao").count() == 0)
    p2.context.close()


@cenario("horus-banco-demandas")
def s3_grade_e_ficha(pg, url, ok):
    perfil(pg, url, "DIRETOR")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
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


@cenario("agiliza-mais")
def s3_extratores(pg, url, ok):
    import json
    ex = APPS / "agiliza-mais" / "exemplos"
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


@cenario("agendamento-cin")
def s3_agendamento_do_cidadao(pg, url, ok):
    pg.set_viewport_size({"width": 390, "height": 800})
    ir(pg, url, "#/agendar", 600)
    pg.click("[data-posto=P01]"); pg.wait_for_timeout(400)
    ok("mostra os dias com vaga no posto", pg.locator("[data-dia]").count() > 0)
    pg.locator("[data-dia]").first.click(); pg.wait_for_timeout(300)
    hid = pg.locator("[data-horario]").first.get_attribute("data-horario")
    antes = pg.evaluate("async id => (await db.get('horarios', id)).ocupadas", hid)
    pg.locator("[data-horario]").first.click(); pg.wait_for_timeout(400)
    pg.fill("#aNome", "Ana Teste"); pg.fill("#aTel", "(65) 99999-0000"); pg.fill("#aCpf", "111.111.111-11"); pg.check("#aAviso")
    pg.click("#formAgDados button[type=submit]"); pg.wait_for_timeout(300)
    ok("CPF inválido é recusado", "CPF inválido" in pg.inner_text("#errosAg"))
    pg.fill("#aCpf", "529.982.247-25"); pg.click("#formAgDados button[type=submit]"); pg.wait_for_timeout(600)
    prot = pg.inner_text("#protCin") if pg.locator("#protCin").count() else ""
    ok("gera protocolo e mostra o comprovante com documentos", prot.startswith("CIN-") and "Documentos para levar" in pg.inner_text("#cardComprovanteCin"))
    ag = pg.evaluate("async p => await db.get('agendamentos', p)", prot)
    ok("o agendamento entra na base com só os 4 últimos dígitos do CPF", ag and ag["cpf_final4"] == "4725" and "52998224725" not in str(ag))
    ok("a vaga é ocupada no horário", pg.evaluate("async id => (await db.get('horarios', id)).ocupadas", hid) == antes + 1)
    ok("sem rolagem horizontal no celular", pg.evaluate("()=> document.documentElement.scrollWidth <= window.innerWidth"))


@cenario("adiantamento")
def s3_etapas_e_linha_do_tempo(pg, url, ok):
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    pid = pg.evaluate("async ()=> (await db.list('processos')).find(p=>p.etapa_atual==='Análise da DAS').id")
    ir(pg, url, "#/processo/" + pid, 500)
    ok("a linha do tempo mostra as 12 etapas com a atual em destaque", pg.locator(".linha-tempo li").count() == 12 and pg.locator(".etapa-atual").inner_text().startswith("2. Análise da DAS"))
    pg.click("#btnAvancar"); pg.wait_for_timeout(500)
    ok("avança para Cadastro no SICAD", pg.inner_text("#etapaAtual") == "Cadastro no SICAD")
    pg.click("#btnAvancar"); pg.wait_for_timeout(400)
    ok("sem o número SICAD não segue", "SICAD" in pg.inner_text("#errosEtapa") and pg.inner_text("#etapaAtual") == "Cadastro no SICAD")
    pg.fill("#pSicad", "SICAD-2026-777"); pg.click("#btnSicad"); pg.wait_for_timeout(400)
    pg.click("#btnAvancar"); pg.wait_for_timeout(500)
    ok("com o número SICAD, avança para a chefia", pg.inner_text("#etapaAtual") == "Aprovação da chefia")
    pg.click("#btnDevolver"); pg.wait_for_timeout(300)
    ok("devolver sem motivo é recusado", "motivo" in pg.inner_text("#errosEtapa"))
    pg.fill("#mObs", "Falta assinatura na justificativa"); pg.click("#btnDevolver"); pg.wait_for_timeout(500)
    ok("devolução volta uma etapa e marca 'devolvido'", pg.inner_text("#etapaAtual") == "Cadastro no SICAD" and "devolvido" in pg.inner_text(".linha-tempo"))
    ok("o histórico registra avanços, número SICAD e devolução", all(x in pg.inner_text("#historicoAd") for x in ("etapa avançada", "número SICAD", "processo devolvido")))
    ok("uma etapa aberta por vez", pg.evaluate("async id => (await db.porIndice('etapas','processo_id',id)).filter(e=>!e.saida_em).length", pid) == 1)


@cenario("rnc-nao-conformidade")
def s3_etapas_e_prazos(pg, url, ok):
    import datetime as dt
    from urllib.parse import quote
    perfil(pg, url, "cqual")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    abertas = pg.evaluate("async ()=> (await db.list('rncs')).filter(r=>r.etapa==='validação' && r.situacao==='aberta').map(r=>r.numero)")
    ok("o exemplo tem RNCs na validação", len(abertas) >= 2)
    a, b = abertas[0], abertas[1]
    ir(pg, url, "#/rnc/" + quote(a, safe=""), 400); pg.click("[data-acao=complemento]"); pg.wait_for_timeout(400)
    ok("pedido de complemento põe a RNC aguardando", pg.inner_text("#situacaoRnc") == "aguardando complemento")
    # 6 dias depois, sem resposta (simula a passagem do tempo)
    pg.evaluate("async n => { const r = await db.get('rncs', n); r.complemento_prazo = '2020-01-01'; await db.put('rncs', r); }", a)
    ir(pg, url, "#/painel", 200); ir(pg, url, "#/rnc/" + quote(a, safe=""), 400)
    ok("sem resposta em 5 dias, a RNC é anulada (RN02)", pg.inner_text("#situacaoRnc") == "anulada" and "RN02" in pg.inner_text("#conteudo"))
    ir(pg, url, "#/rnc/" + quote(b, safe=""), 400)
    data_b = pg.evaluate("async n => (await db.porIndice('etapas','rnc',n))[0].inicio", b)
    pg.fill("#rData", data_b); pg.click("[data-acao=aprovar]"); pg.wait_for_timeout(400)
    prazo = pg.evaluate("async n => (await db.porIndice('etapas','rnc',n)).find(e=>e.etapa==='plano').prazo", b)
    ok("aprovar abre o plano com prazo de 30 dias (RN03)", prazo == (dt.date.fromisoformat(data_b) + dt.timedelta(days=30)).isoformat())
    pg.click("[data-acao=prorrogar]"); pg.wait_for_timeout(300)
    ok("prorrogar sem justificativa é recusado", "justificativa" in pg.inner_text("#errosAcaoRnc"))
    pg.fill("#rTexto", "Setor aguarda a calibração do equipamento"); pg.click("[data-acao=prorrogar]"); pg.wait_for_timeout(400)
    ok("prorrogação registrada (+15 dias)", "prorrogado" in pg.inner_text("#tabelaEtapas") and pg.evaluate("async n => (await db.get('planos', n + '-plano')).prorrogado_ate", b) == (dt.date.fromisoformat(prazo) + dt.timedelta(days=15)).isoformat())
    pg.fill("#rTexto", "Recorrência com exposição de vestígio"); pg.click("[data-acao=grave]"); pg.wait_for_timeout(400)
    ok("grave encaminha à corregedoria (RN04)", pg.inner_text("#situacaoRnc") == "encaminhada à corregedoria" and pg.locator("#formAcaoRnc").count() == 0)


@cenario("metas-bi-ocr")
def s3_conferencia(pg, url, ok):
    ex = APPS / "metas-bi-ocr" / "exemplos"
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(600)
    for mes in ["2026-07", "2026-08", "2026-09"]:
        ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(ex / f"powerbi1-{mes}.csv")); pg.wait_for_timeout(800)
        if mes == "2026-08":
            pg.select_option("select[id^=assoc-]", "Regional Sinop"); pg.click("[data-assoc]"); pg.wait_for_timeout(500)
    ir(pg, url, "#/conferencia/2026-09", 500)
    ok("setembro: soma diferente do total bloqueia a aprovação (RN02)", "RN02" in pg.inner_text("#bloqueios") and pg.is_disabled("#btnAprovar"))
    pg.fill("#motivoCorrecao", "Total do PDF inclui laudos de outra diretoria"); pg.click("#btnAceitarSoma"); pg.wait_for_timeout(500)
    ok("aceitar a soma com motivo libera a aprovação", not pg.is_disabled("#btnAprovar"))
    pg.fill("#aprovador", "Chefe Teste"); pg.click("#btnAprovar"); pg.wait_for_timeout(500)
    ok("mês aprovado fica travado (RN05)", "aprovado por Chefe Teste" in pg.inner_text("#situacaoMes") and pg.locator("[data-novo]").count() == 0)
    ir(pg, url, "#/conferencia/2026-08", 500)
    ok("agosto: variação acima de 30% sobre julho vira alerta (RN04)", "RN04" in pg.inner_text("[data-unidade='Criminalística Cuiabá']"))
    pg.fill("[data-novo='2026-08|Criminalística Cuiabá']", "999"); pg.click("#btnCorrigir"); pg.wait_for_timeout(300)
    ok("corrigir sem motivo não grava", contar(pg, "correcoes") == 1)
    pg.fill("#motivoCorrecao", "Conferido no painel do Power BI 1"); pg.click("#btnCorrigir"); pg.wait_for_timeout(500)
    ok("correção com motivo fica registrada", contar(pg, "correcoes") == 2 and "corrigido" in pg.inner_text("[data-unidade='Criminalística Cuiabá']"))
    ir(pg, url, "#/conferencia/2026-09", 500)
    pg.click("#btnNovaVersao"); pg.wait_for_timeout(300)
    ok("nova versão sem motivo é recusada", "RN05" in pg.inner_text("#errosVersao"))
    pg.fill("#motivoVersao", "Reprocessamento do Power BI 1"); pg.click("#btnNovaVersao"); pg.wait_for_timeout(500)
    ok("nova versão reabre o mês (versão 2)", "versão 2" in pg.inner_text("#conteudo") and pg.inner_text("#situacaoMes") == "a conferir")


@cenario("cin-segunda-via")
def s3_fila_do_servidor(pg, url, ok):
    perfil(pg, url, "servidor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    pg.evaluate("""async ()=>{ const p = {protocolo: '2V-TESTE-0001', nome: 'Alice Teste', cpf: dadosEmbutidos('seed').pedidos[0].cpf, nascimento: '1990-05-10',
        numero_cin: dadosEmbutidos('seed').pedidos[0].cpf, validade_cin: '2031-01-01', mudou_dados: false, contato: 'alice@exemplo.com', criado_em: '2026-10-28T10:00:00Z', situacao: 'recebido', motivo: ''};
      await db.put('pedidos', p); for (const t of ['rosto','documento']) await db.put('fotos', {id: p.protocolo + '-' + t, protocolo: p.protocolo, tipo: t, conteudo: await fotoDeTeste(t)}); }""")
    ir(pg, url, "#/fila", 500)
    rec = pg.evaluate("async ()=> (await db.list('pedidos')).filter(p=>p.situacao==='recebido').length")
    ok("a fila separa por situação", pg.inner_text("[data-qtd=recebido]") == str(rec))
    pg.click("[data-sel='2V-TESTE-0001']"); pg.wait_for_timeout(500)
    ok("a ficha mostra as 2 fotos e a elegibilidade", pg.locator("#fichaPedido img").count() == 2 and "CIN válida" in pg.inner_text("#fichaPedido"))
    pg.click("#btnRecusar"); pg.wait_for_timeout(300)
    ok("recusar sem motivo é recusado (RN05)", "RN05" in pg.inner_text("#errosFila"))
    pg.select_option("#fMotivo", "Foto ilegível"); pg.click("#btnRecusar"); pg.wait_for_timeout(500)
    ok("recusa grava situação, motivo e decisão", pg.evaluate("async ()=> (await db.get('pedidos','2V-TESTE-0001')).motivo") == "Foto ilegível" and contar(pg, "decisoes") == 1)
    ok("a recusa fica no log", pg.evaluate("async ()=> (await db.list('log')).some(l=>l.acao==='pedido recusado' && l.protocolo==='2V-TESTE-0001')"))
    outro = pg.evaluate("async ()=> (await db.list('pedidos')).find(p=>p.situacao==='recebido').protocolo")
    pg.evaluate("p => { estado.pedidoSel = p; }", outro); ir(pg, url, "#/fila", 200); pg.evaluate("()=> navegar()"); pg.wait_for_timeout(400)
    pg.click("#btnAceitar"); pg.wait_for_timeout(500)
    ok("aceitar muda a situação", pg.evaluate("async p => (await db.get('pedidos', p)).situacao", outro) == "aceito")
    ir(pg, url, "#/pedido/2V-TESTE-0001/resumo", 400)
    ok("resumo traz CPF formatado e a situação", "." in pg.inner_text("#tabelaResumo") and "recusado" in pg.inner_text("#tabelaResumo"))


@cenario("tap-portfolio-projetos")
def s3_pacote_e_triagem(pg, url, ok):
    import json
    perfil(pg, url, "demandante")
    pg.evaluate("""async ()=>{ for (const d of dadosEmbutidos('seed').documentos) await db.put('documentos', d);
      const p = {id: 'TAP-2026-101', titulo: 'Projeto pacote', unidade: 'Laboratório', responsavel: 'Resp', contato: 'r@politec.mt.gov.br', objetivo: 'o'.repeat(120),
        justificativa: 'j'.repeat(220), objetivo_estrategico: 'Ampliar a capacidade dos laboratórios', valor_estimado: 1000, prazo_meses: 6, status: 'pronto para envio',
        criado_em: agora(), ausencias: {anuencia_chefia: 'Assina no SEI.'}};
      await db.put('propostas', p);
      for (const t of ['pesquisa_precos','estudo_tecnico']) await db.put('anexos', {id: p.id + '-' + t, proposta_id: p.id, tipo: t, nome: t + '.pdf', mime: 'application/pdf', tamanho: 8, conteudo: new Blob(['%PDF-1.4'], {type: 'application/pdf'})}); }""")
    ir(pg, url, "#/minhas", 400)
    with pg.expect_download() as dl:
        pg.click("[data-pacote='TAP-2026-101']")
    pacote = TMP / "proposta-TAP-2026-101.json"; dl.value.save_as(pacote)
    d = json.loads(pacote.read_text(encoding="utf-8"))
    ok("pacote com a proposta, 2 anexos e o código de verificação", d["formato"] == "TAP-v1" and len(d["conteudo"]["anexos"]) == 2 and len(d["verificacao"]) == 8)
    alterado = TMP / "alterado.json"; alterado.write_text(pacote.read_text(encoding="utf-8").replace("Projeto pacote", "Projeto mexido"), encoding="utf-8")
    eq = pg.context.browser.new_context(accept_downloads=True).new_page(); eq.on("dialog", lambda x: x.accept())   # a equipe, em outro computador
    eq.goto(url + "#/config"); eq.wait_for_timeout(300); eq.evaluate("db.meta('perfil','equipe')"); eq.reload(); eq.wait_for_timeout(300)
    eq.evaluate("async ()=>{ for (const d of dadosEmbutidos('seed').documentos) await db.put('documentos', d); }")
    eq.goto(url + "#/triagem"); eq.wait_for_timeout(400)
    eq.set_input_files("#arqPacote", str(alterado)); eq.wait_for_timeout(400)
    ok("pacote alterado é recusado", "verificação" in eq.inner_text("#errosPacote"))
    eq.set_input_files("#arqPacote", str(pacote)); eq.wait_for_timeout(600)
    ok("a equipe recebe a proposta com o checklist", "em triagem" in eq.inner_text("#sitTap") and "ausência justificada" in eq.inner_text("#fichaTriagem"))
    ok("os anexos chegam íntegros", eq.evaluate("async ()=> (await (await db.get('anexos','TAP-2026-101-pesquisa_precos')).conteudo.text())") == "%PDF-1.4")
    eq.click("#btnPendencia"); eq.wait_for_timeout(300)
    ok("pendência sem motivo é recusada (RN05)", "RN05" in eq.inner_text("#errosTriagem"))
    eq.fill("#tMotivo", "A pesquisa de preços tem só 2 orçamentos.")
    with eq.expect_download() as dl2:
        eq.click("#btnPendencia")
    devol = TMP / "devolucao.json"; dl2.value.save_as(devol)
    ok("devolução gera o arquivo para o demandante", json.loads(devol.read_text(encoding="utf-8"))["formato"] == "TAP-DEV-v1")
    ir(pg, url, "#/minhas", 300); pg.set_input_files("#arqDevolucao", str(devol)); pg.wait_for_timeout(500)
    ok("o demandante vê a pendência devolvida", "devolvida" in pg.inner_text("#tabelaMinhas") and "2 orçamentos" in pg.inner_text("#tabelaMinhas"))
    eq.set_input_files("#arqPacote", str(pacote)); eq.wait_for_timeout(500); eq.click("#btnAceitarTap"); eq.wait_for_timeout(500)
    ok("checklist completo é aceito para análise (RN06)", eq.evaluate("async ()=> (await db.get('propostas','TAP-2026-101')).status") == "em análise")
    eq.context.close()


@cenario("comissao-etica-denuncias")
def s3_classificacao_assistida(pg, url, ok):
    perfil(pg, url, "membro")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    acertos = pg.evaluate("""async ()=>{ const cats = await categoriasAtivas(); return (await db.list('denuncias')).filter(d=>pontuar(d.relato, cats).slice(0,3).some(x=>x.id===d.categoria_esperada)).length; }""")
    ok("os 10 casos fictícios têm a categoria esperada entre as 3 sugestões", acertos == 10)
    ir(pg, url, "#/caso/CE-2026-001/classificacao", 500)
    ok("a sugestão mostra as palavras que dispararam", "Palavras:" in pg.inner_text("#sugestoes") and pg.locator("mark").count() > 0)
    pg.evaluate("async ()=>{ const d = await db.get('denuncias','CE-2026-001'); d.relato = 'Servidor Fictício A gritou com Denunciante Fictício 1 e a humilhou.'; await db.put('denuncias', d); }")
    ir(pg, url, "#/caso/CE-2026-002/classificacao", 200); ir(pg, url, "#/caso/CE-2026-001/classificacao", 500)
    pr = pg.input_value("#promptIA")
    ok("o prompt sai sem os nomes das partes", "Fictício" not in pr and "[DENUNCIADO]" in pr and "[DENUNCIANTE]" in pr)
    ok("caso aberto entra na etapa classificação", pg.evaluate("async ()=> (await db.get('denuncias','CE-2026-001')).etapa") == "classificação")
    pg.click("#formClassif button[type=submit]"); pg.wait_for_timeout(300)
    ok("sem justificativa não confirma (RN02)", "RN02" in pg.inner_text("#errosClassif") and pg.evaluate("async ()=> (await db.get('denuncias','CE-2026-001')).etapa") == "classificação")
    pg.fill("#cJustificativa", "O relato descreve humilhação e ameaças repetidas diante da equipe.")
    pg.click("#formClassif button[type=submit]"); pg.wait_for_timeout(500)
    ok("confirmada, o caso segue para a admissibilidade", pg.evaluate("async ()=> (await db.get('denuncias','CE-2026-001')).etapa") == "admissibilidade")
    ok("classificação registrada com membro, sugestões e justificativa", pg.evaluate("async ()=>{ const c = (await db.porIndice('classificacoes','denuncia_id','CE-2026-001'))[0]; return c.confirmada && c.membro==='membro' && c.sugeridas.length>0 && c.justificativa.length>20; }"))
    ok("o histórico do caso traz a confirmação com a justificativa", "classificação confirmada" in pg.inner_text("#historico") and "humilhação" in pg.inner_text("#historico"))
