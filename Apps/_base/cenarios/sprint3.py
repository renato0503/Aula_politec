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


@cenario("custodia-definitiva")
def s3_busca_csv_e_historico(pg, url, ok):
    perfil(pg, url, "custodia")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
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


@cenario("trilha-custodia-necropsia")
def s3_situacao_identificacao_e_busca(pg, url, ok):
    perfil(pg, url, "plantonista")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    ir(pg, url, "#/painel", 500)
    nomes = pg.evaluate("async ()=> (await db.list('corpos')).filter(c=>c.nome).map(c=>c.nome)")
    txt = pg.inner_text("#tcTabelaPainel")
    ok("o painel não mostra nome completo, só as iniciais (RN05)", nomes and not any(n in txt for n in nomes) and "M. F. S" in txt)
    ir(pg, url, "#/corpos", 400)
    ok("a lista de corpos também usa iniciais (RN05)", not any(n in pg.inner_text("#conteudo") for n in nomes))
    cid = pg.evaluate("async ()=> (await db.list('corpos')).find(c=>c.situacao==='aguardando identificação').id_corpo")
    ir(pg, url, "#/corpo/" + cid, 500)
    pg.select_option("#tcNovaSit", "não identificado"); pg.click("#btnTcSit"); pg.wait_for_timeout(400)
    ok("não identificado sem motivo é recusado", "motivo" in pg.inner_text("#tcErrosSit"))
    pg.fill("#tcMotivo", "30 dias sem identificação"); pg.click("#btnTcSit"); pg.wait_for_timeout(500)
    ok("muda para não identificado com motivo no histórico", pg.inner_text("#tcSitAtual") == "não identificado" and "30 dias" in pg.inner_text("#tcHistSit"))
    pg.select_option("#tcNovaSit", "em custódia"); pg.click("#btnTcSit"); pg.wait_for_timeout(400)
    ok("em custódia exige identificação", "identificado" in pg.inner_text("#tcErrosSit"))
    pg.check("#tcIdent"); pg.fill("#tcIdNome", "Pessoa Fictícia Identificada"); pg.fill("#tcIdDoc", "DOC-TESTE-9")
    pg.click("#btnTcSit"); pg.wait_for_timeout(400)
    ok("identificação sem método é recusada", "método" in pg.inner_text("#tcErrosSit"))
    pg.select_option("#tcIdMetodo", "papiloscopia"); pg.click("#btnTcSit"); pg.wait_for_timeout(500)
    c = pg.evaluate("async id => await db.get('corpos', id)", cid)
    ok("identifica e volta a em custódia", c["identificado"] and c["nome"] == "Pessoa Fictícia Identificada" and c["situacao"] == "em custódia" and c["metodo_identificacao"] == "papiloscopia")
    pg.select_option("#tcNovaSit", "não reclamado"); pg.fill("#tcMotivo", "Edital publicado"); pg.click("#btnTcSit"); pg.wait_for_timeout(500)
    ok("identificado sem família vira não reclamado", pg.inner_text("#tcSitAtual") == "não reclamado")
    ir(pg, url, "#/busca", 400); pg.fill("#tcBusca", "DOC-TESTE-9"); pg.press("#tcBusca", "Enter"); pg.wait_for_timeout(500)
    ok("a busca acha pelo documento (RN04)", "Pessoa Fictícia Identificada" in pg.inner_text("#tcResultado"))
    lac = pg.evaluate("async ()=> (await db.list('lacres'))[0]")
    pg.fill("#tcBusca", lac["codigo"]); pg.press("#tcBusca", "Enter"); pg.wait_for_timeout(500)
    prot = pg.evaluate("async id => (await db.get('corpos', id)).protocolo", lac["corpo_id"])
    ok("a busca acha pelo código do lacre", prot in pg.inner_text("#tcResultado"))
    pg.fill("#tcBusca", "maria souza"); pg.press("#tcBusca", "Enter"); pg.wait_for_timeout(500)
    ok("a busca por nome aceita palavras fora de ordem", "Maria Fictícia Souza" in pg.inner_text("#tcResultado"))

# Cenário do Sprint 3 do Passivo Ambiental: mapa temático (RN02) e versão impressa (RN03).


@cenario("passivo-ambiental")
def s3_mapa_e_pdf(pg, url, ok):
    perfil(pg, url, "perito")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    # requisição nova, sem mapa: a exportação fica bloqueada (RN03)
    ir(pg, url, "#/requisicao/nova", 400)
    pg.fill("#paNumero", "2026.888888-8"); pg.fill("#paOrgao", "Delegacia de Teste"); pg.fill("#paTipo", "queimada")
    pg.fill("#paLocal", "Área de teste"); pg.fill("#paCoord", "-12.9000, -55.8000")
    pg.click("#formPaNova button[type=submit]"); pg.wait_for_timeout(600)
    ok("a requisição abre o laudo", "#/laudo/REQ-0013" in pg.url)
    ir(pg, url, "#/pdf/REQ-0013", 400)
    ok("sem mapa, a versão impressa fica bloqueada (RN03)", "RN03" in pg.inner_text("#conteudo") and pg.locator("#paDocumento").count() == 0)
    # mapa sem os elementos obrigatórios é recusado (RN02)
    ir(pg, url, "#/mapa/REQ-0013", 400)
    pg.select_option("#paModelo", "delimitacao")
    pg.click("#formPaMapa button[type=submit]"); pg.wait_for_timeout(400)
    ok("mapa sem elementos obrigatórios é recusado (RN02)", "RN02" in pg.inner_text("#paErrosMapa") and contar(pg, "mapas") == 4)
    pg.select_option("#paModelo", "localizacao")
    pg.fill("#paExtra", "12,5")
    for campo_id in ("paEl_norte", "paEl_escala", "paEl_legenda", "paEl_data", "paEl_fonte"):
        pg.fill("#" + campo_id, "valor de teste")
    pg.click("#formPaMapa button[type=submit]"); pg.wait_for_timeout(600)
    ok("o mapa completo é anexado ao laudo", "#/laudo/REQ-0013" in pg.url and contar(pg, "mapas") == 5)
    m = pg.evaluate("async ()=> (await db.porIndice('mapas','laudo_id','L-REQ-0013'))[0]")
    ok("o mapa guarda modelo, elementos e medida (RN02)", m["modelo_id"] == "localizacao" and m["elementos"]["norte"] == "valor de teste" and m["valor_extra"] == "12,5")
    ok("a lista de mapas mostra os elementos conferidos", pg.locator("#paListaMapas li.feito").count() == 1)
    # com mapa e cabeçalho, a versão impressa abre
    ir(pg, url, "#/pdf/REQ-0013", 500)
    ok("com mapa e cabeçalho, a versão impressa abre (RN03)", pg.locator("#paDocumento").count() == 1)
    doc = pg.inner_text("#paDocumento")
    ok("o documento traz o cabeçalho e os mapas anexados", "LAUDO" in doc and "2026.888888-8" in doc and "Mapas anexados (1)" in doc)
    # conclusão salva aparece no documento
    ir(pg, url, "#/laudo/REQ-0013", 400)
    pg.fill("#paConclusao", "Área de 12,5 ha com vegetação queimada."); pg.click("#formPaConclusao button[type=submit]"); pg.wait_for_timeout(500)
    ir(pg, url, "#/pdf/REQ-0013", 500)
    ok("a conclusão vai para a versão impressa", "vegetação queimada" in pg.inner_text("#paDocumento"))
    # a conclusão do laudo concluído exige mapa, e o exemplo já tem
    ok("todos os mapas do exemplo e o novo vêm com os elementos completos",
       pg.evaluate("async ()=> (await db.list('mapas')).filter(m=>paMapaCompleto(m)).length") == 5)

# Cenário do Sprint 3 da Renovação de Contratos: checklist de instrução, repositório de documentos e aviso de 60 dias.


@cenario("renovacao-contratos-horus")
def s3_instrucao_e_documentos(pg, url, ok):
    perfil(pg, url, "gestor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    ir(pg, url, "#/painel", 600)
    aviso = pg.evaluate("""async ()=>{ const h = hojeISO(), cs = await db.list('contratos');
        const n = [];
        for (const c of cs){ const itens = await db.porIndice('instrucao','contrato_id',c.id_contrato);
            if (rcSemInstrucao(c, itens, h)) n.push(c.id_contrato); }
        return n; }""")
    ok("o painel avisa os contratos que vencem em 60 dias sem instrução completa (Sprint 3)", bool(aviso) and pg.locator("#rcAvisoInstrucao").count() == 1
       and pg.locator("#tabelaAviso tr").count() - 1 == len(aviso))
    # abrir um contrato do aviso e completar a instrução
    cid = aviso[0]
    ir(pg, url, "#/contrato/" + cid, 500)
    falta_antes = pg.locator("#rcListaInstrucao li.falta").count()
    ok("o checklist mostra os itens obrigatórios faltando", falta_antes >= 6 and "Falta concluir a instrução" in pg.inner_text("#conteudo"))
    for _ in range(8):
        b = pg.locator("#rcListaInstrucao .rcItem[data-obrigatorio='1'][data-feito='0']").first
        if not b.count():
            break
        b.click(); pg.wait_for_timeout(450)
    ok("marcar os itens obrigatórios deixa a instrução completa", pg.locator("#rcListaInstrucao li.falta").count() == 1
       and "Instrução completa" in pg.inner_text("#conteudo"))
    ok("o item facultativo não impede a conclusão", "Falta concluir a instrução" not in pg.inner_text("#conteudo"))
    ok("a auditoria registra a marcação do item", pg.evaluate("async id => (await db.porIndice('auditoria','contrato_id',id)).some(a=>a.acao.includes('item de instrução marcado'))", cid))
    ir(pg, url, "#/instrucao", 500)
    ok("a tela de instrução mostra o progresso de cada contrato", pg.locator("#tabelaInstrucao tr").count() == 15)
    # repositório de documentos: o fiscal não vê o restrito (R8)
    ir(pg, url, "#/contrato/" + cid, 500)
    pg.fill("#rcAnexoNome", "oficio-solicitacao.pdf"); pg.select_option("#rcAnexoVis", "gestao"); pg.fill("#rcAnexoTexto", "Documento fictício restrito.")
    pg.click("#formRcAnexo button[type=submit]"); pg.wait_for_timeout(600)
    ok("o documento fica guardado no contrato", pg.evaluate("async ()=> (await db.list('anexos')).length") == 1)
    ok("o gestor vê o documento restrito", "oficio-solicitacao.pdf" in pg.inner_text("#rcListaAnexos"))
    perfil(pg, url, "fiscal")
    ir(pg, url, "#/contrato/" + cid, 600)
    ok("o fiscal não vê o documento restrito à gestão (R8)", "oficio-solicitacao.pdf" not in pg.inner_text("#rcListaAnexos"))
    ok("o checklist continua visível para o fiscal", pg.locator("#rcListaInstrucao").count() == 1)

# Cenário do Sprint 3 do DOCUMENTAPOLITEC: importação da planilha com associação de colunas e comparação com o arquivo digital.


@cenario("documentapolitec")
def s3_importacao_e_conferencia(pg, url, ok):
    perfil(pg, url, "papiloscopista")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    ex = APPS / "documentapolitec" / "exemplos"
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

# Cenário do Sprint 3 da Gestão de Documentos: minutas padronizadas, emissão de ofício e despacho e checklist de instrução.


@cenario("gestao-documentos")
def s3_minutas_e_checklist(pg, url, ok):
    perfil(pg, url, "servidor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    ir(pg, url, "#/processo/novo", 400)
    pg.fill("#gdAssunto", "Pedido de cópia de laudo"); pg.fill("#gdRequerente", "Requerente Teste"); pg.fill("#gdLotacao", "Gabinete de Direção")
    pg.select_option("#gdResponsavel", "U1")
    for i in range(3): pg.check(f"#gdAnexo{i}")
    pg.click("#formGdNovo button[type=submit]"); pg.wait_for_timeout(600)
    pid = pg.evaluate("async ()=> (await db.list('processos')).sort((a,b)=>b.criado_em.localeCompare(a.criado_em))[0].id_processo")
    ok("o processo novo está na ficha", "#/processo/" + pid in pg.url)
    # RN04: minuta sai preenchida com os dados do processo
    pg.select_option("#gdTipoMinuta", "oficio_encaminhamento")
    pg.click("#formGdMinuta button[type=submit]"); pg.wait_for_timeout(600)
    ok("a minuta é emitida e entra na lista", pg.evaluate("async id => (await db.porIndice('minutas','processo_id',id)).length", pid) == 1)
    ok("a emissão cria o documento correspondente", pg.evaluate("async id => (await db.porIndice('documentos','processo_id',id)).some(d=>d.tipo_documento==='Ofício de encaminhamento')", pid))
    ok("o histórico registra a minuta emitida", pg.evaluate("async id => (await db.porIndice('log','processo_id',id)).some(l=>l.tipo_evento==='minuta emitida')", pid))
    pg.click(".gdMinutaAbrir"); pg.wait_for_timeout(500)
    txt = pg.inner_text("#gdMinutaTexto")
    ok("a minuta aberta traz o número, o assunto, o requerente e a lotação (RN04)", "Pedido de cópia de laudo" in txt
       and "Requerente Teste" in txt and "Gabinete de Direção" in txt and "2026." in txt)
    # despacho
    pg.select_option("#gdTipoMinuta", "despacho")
    pg.click("#formGdMinuta button[type=submit]"); pg.wait_for_timeout(600)
    ok("o despacho também é emitido", pg.evaluate("async id => (await db.porIndice('minutas','processo_id',id)).length", pid) == 2)
    # checklist por etapa
    ok("o checklist traz as duas etapas", pg.locator("#gdCheck_Instrução li").count() == 4 and pg.locator("#gdCheck_Decisão li").count() == 3)
    for _ in range(8):
        b = pg.locator(".gdCheckItem[data-feito='0']").first
        if not b.count():
            break
        b.click(); pg.wait_for_timeout(400)
    ok("todos os itens do checklist ficam marcados", pg.locator(".gdCheckItem[data-feito='0']").count() == 0)
    ok("o histórico registra o checklist", pg.evaluate("async id => (await db.porIndice('log','processo_id',id)).some(l=>l.tipo_evento==='checklist: item marcado')", pid))
    # RN04: processo sem os dados exigidos não emite minuta
    pg.evaluate("async id => { const p = await db.get('processos', id); await db.put('processos', {...p, requerente: ''}); }", pid)
    pg.reload(); pg.wait_for_timeout(700)
    ok("sem requerente, a minuta fica bloqueada (RN04)", pg.locator("#gdErrosMinuta").count() == 1 and "requerente" in pg.inner_text("#gdErrosMinuta"))
    pg.click("#formGdMinuta button[type=submit]"); pg.wait_for_timeout(400)
    ok("a emissão é recusada com o motivo", "RN04" in pg.inner_text("#gdErrosEmissao"))

# Cenário do Sprint 3 do Controle de Aquisições: pesquisa de preços com três cotações, alerta estimado x cotado e histórico por objeto.


@cenario("controle-aquisicoes")
def s3_pesquisa_de_precos(pg, url, ok):
    perfil(pg, url, "compras")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    ir(pg, url, "#/processo/AQ-0001", 500)
    ok("o exemplo já traz duas pesquisas do mesmo objeto", pg.evaluate("async ()=> (await db.porIndice('pesquisas','processo_id','AQ-0001')).length") == 2)
    ok("a ficha mostra as duas pesquisas", pg.locator("#caHistoricoPrecos > .card").count() == 2)
    ok("a pesquisa com o cotado 40% acima entra em alerta", "Alerta:" in pg.inner_text("#caHistoricoPrecos"))
    # RN04: sem três cotações, a pesquisa é recusada
    pg.fill("#caPesqEstimado", "10000")
    pg.fill("#caCotFornecedor1", "Fornecedor A"); pg.fill("#caCotValor1", "10000")
    pg.click("#formCaPesquisa button[type=submit]"); pg.wait_for_timeout(400)
    ok("sem três cotações, a pesquisa é recusada (RN04)", "RN04" in pg.inner_text("#caErrosPesquisa")
       and pg.evaluate("async ()=> (await db.list('pesquisas')).length") == 2)
    # com três cotações dentro da tolerância, a pesquisa entra sem alerta
    pg.fill("#caPesqEstimado", "10000")
    for k, v in ((1, "10000"), (2, "10200"), (3, "9800")):
        pg.fill(f"#caCotFornecedor{k}", f"Fornecedor {k}"); pg.fill(f"#caCotValor{k}", v); pg.fill(f"#caCotData{k}", "2026-10-20")
    pg.click("#formCaPesquisa button[type=submit]"); pg.wait_for_timeout(600)
    ok("com três cotações, a pesquisa é registrada", pg.evaluate("async ()=> (await db.list('pesquisas')).length") == 3)
    ok("a nova pesquisa não entra em alerta", pg.evaluate("async ()=> { const q = (await db.list('pesquisas')).sort((a,b)=>a.data_hora.localeCompare(b.data_hora)).at(-1); return !caAlertaEstimado(q); }"))
    # com cotado 40% acima, entra em alerta
    pg.fill("#caPesqEstimado", "10000")
    for k, v in ((1, "14000"), (2, "14000"), (3, "14000")):
        pg.fill(f"#caCotFornecedor{k}", f"Fornecedor {k}"); pg.fill(f"#caCotValor{k}", v)
    pg.click("#formCaPesquisa button[type=submit]"); pg.wait_for_timeout(600)
    ok("o cotado 40% acima do estimado entra em alerta", pg.evaluate("async ()=> { const q = (await db.list('pesquisas')).sort((a,b)=>a.data_hora.localeCompare(b.data_hora)).at(-1); return caAlertaEstimado(q); }")
       and "Alerta:" in pg.inner_text("#caHistoricoPrecos"))
    # histórico por objeto
    ir(pg, url, "#/precos", 600)
    ok("o histórico mostra o objeto com as quatro pesquisas", pg.locator("#tabelaHistoricoPrecos tr").count() == 2)
    linha = pg.inner_text("#tabelaHistoricoPrecos")
    ok("o histórico compara a primeira e a última média", "notebooks" in linha.lower() and "%" in linha)
    ok("o histórico leva ao processo", "AQ-0001" in pg.inner_text("#tabelaHistoricoPrecos"))

# Cenário do Sprint 3 da Distribuição de Casos de DNA: sugestão por histórico de rotação, fila de urgência e alerta de rodada parada.


@cenario("distribuicao-casos-dna")
def s3_sugestao_e_urgencia(pg, url, ok):
    perfil(pg, url, "coordenador")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    ir(pg, url, "#/painel", 700)
    ok("o painel avisa as rodadas paradas", pg.locator("#ddCardParada").count() == 1 and pg.locator("#tabelaParadas tr").count() > 1)
    paradas = pg.evaluate("async ()=> { const rs = await db.list('rodadas'); return rs.filter(r=>ddParada(r)).map(r=>r.id_rodada); }")
    ok("a lista de rodadas paradas bate com o cálculo", pg.locator("#tabelaParadas tr").count() - 1 == len(paradas))
    ok("a fila de urgência mostra os casos marcados no exemplo", pg.locator("#tabelaUrgencia tr").count() - 1 == 2)
    ok("a fila ordena por prioridade (crítico antes de alta)", pg.inner_text("#tabelaUrgencia").index("Crítico") < pg.inner_text("#tabelaUrgencia").index("Alta"))
    # sugestão pelo histórico de rotação
    ir(pg, url, "#/rodada/RD-003", 600)
    ok("a tabela de sugestão lista os peritos", pg.locator("#tabelaSugestao tr").count() == 5)
    ok("o perito sugerido vem do histórico de rotação", pg.locator("#ddSugerido").count() == 1)
    esperado = pg.evaluate("""async ()=>{ const ps = await db.list('peritos'), rs = await db.list('rodadas'), cs = await db.list('casos');
        return ddSugerir3(ps, rs, cs, null).id_perito; }""")
    ok("a sugestão coincide com a função do histórico", pg.evaluate("""async ()=>{ const ps = await db.list('peritos'), rs = await db.list('rodadas'), cs = await db.list('casos');
        return ddSugerir3(ps, rs, cs, null).id_perito; }""") == esperado)
    # RN05: marcar um caso como urgente exige justificativa
    caso = pg.evaluate("async id => (await db.porIndice('casos','rodada_id',id)).find(c=>!c.perito_id && !c.urgente).id_caso", "RD-003")
    pg.select_option("#ddUrgCaso", caso); pg.select_option("#ddUrgPrioridade", "alta")
    pg.click("#formDdUrgencia button[type=submit]"); pg.wait_for_timeout(400)
    ok("sem justificativa, a marcação é recusada (RN05)", "RN05" in pg.inner_text("#ddErrosUrgencia"))
    pg.fill("#ddUrgJustificativa", "Prazo judicial em 5 dias")
    pg.click("#formDdUrgencia button[type=submit]"); pg.wait_for_timeout(600)
    ok("o caso entra na fila de urgência", pg.evaluate("async id => (await db.get('casos', id)).urgente", caso)
       and pg.evaluate("async id => (await db.porIndice('urgencias','rodada_id',id)).length", "RD-003") == 3)
    ok("a ficha lista o caso urgente", "Prazo judicial em 5 dias" in pg.inner_text("#ddListaUrgencia"))
    ok("o histórico registra a marcação", "caso marcado como urgente" in pg.inner_text("#conteudo"))
    # a fila de urgência do painel soma o novo caso
    ir(pg, url, "#/painel", 700)
    ok("o painel passa a mostrar 3 casos urgentes", pg.locator("#tabelaUrgencia tr").count() - 1 == 3)
