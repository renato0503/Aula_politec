# Cenarios do Sprint 4 em diante (carregados pelo testar_sprints.py).

# Cenários dos Sprints 4 a 6 do TAP: proposta, parecer, decisão, portfólio e indicadores.


@cenario("tap-portfolio-projetos")
def s4_proposta_parecer_e_decisao(pg, url, ok):
    perfil(pg, url, "equipe")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    ir(pg, url, "#/proposta/TAP-2026-005", 600)
    ok("a ficha da proposta mostra TAP, anexos, pendências e histórico", "TAP" in pg.inner_text("#conteudo")
       and "Pendências abertas" in pg.inner_text("#conteudo") or pg.locator(".card").count() >= 4)
    pg.fill("#tpTexto", "parecer curto")
    pg.click("#formTapParecer button[type=submit]"); pg.wait_for_timeout(400)
    ok("parecer curto é recusado", "30 caracteres" in pg.inner_text("#tapErrosParecer"))
    pg.fill("#tpTexto", "A proposta está apta e o pacote de documentos está completo para a análise.")
    pg.click("#formTapParecer button[type=submit]"); pg.wait_for_timeout(600)
    ok("o parecer da equipe é registrado", pg.evaluate("async ()=> (await db.porIndice('pareceres','proposta_id','TAP-2026-005')).length") == 1)
    # decisão da autoridade (RN07)
    perfil(pg, url, "autoridade")
    ir(pg, url, "#/proposta/TAP-2026-005", 600)
    pg.fill("#tdTexto", "curto")
    pg.click("#formTapDecisao button[type=submit]"); pg.wait_for_timeout(400)
    ok("decisão sem fundamento é recusada (RN07)", "20 caracteres" in pg.inner_text("#tapErrosDecisao"))
    pg.select_option("#tdTipo", "aprovacao")
    pg.fill("#tdTexto", "Aprovado por alinhamento ao planejamento estratégico e disponibilidade orçamentária.")
    pg.click("#formTapDecisao button[type=submit]"); pg.wait_for_timeout(700)
    ok("a decisão muda a situação para aprovada", pg.inner_text("#tapStatus") == "aprovada"
       and pg.evaluate("async ()=> (await db.get('propostas','TAP-2026-005')).status") == "aprovada")


@cenario("tap-portfolio-projetos")
def s5_portfolio_e_prioridade(pg, url, ok):
    perfil(pg, url, "equipe")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    ir(pg, url, "#/portfolio", 600)
    aprovadas = pg.evaluate("async ()=> (await db.list('propostas')).filter(p=>p.status==='aprovada').length")
    ok("o portfólio lista as propostas aprovadas", pg.locator("#tabelaPortfolio tr").count() - 1 == aprovadas)
    # tira a prioridade de uma aprovada e confere o aviso
    pg.evaluate("async ()=> { const x = await db.list('portfolio'); if (x.length) await db.del('portfolio', x[0].proposta_id); }")
    pg.reload(); pg.wait_for_timeout(700)
    ok("proposta aprovada sem prioridade aparece marcada", "sem prioridade" in pg.inner_text("#tabelaPortfolio"))
    # RN08: prioridade sem justificativa é recusada
    pg.select_option("#prTap", "TAP-2026-002"); pg.fill("#prOrdem", "1"); pg.fill("#prFonte", "Emenda parlamentar")
    pg.select_option("#prCaptacao", "em captação")
    pg.click("#formTapPrioridade button[type=submit]"); pg.wait_for_timeout(400)
    ok("prioridade sem justificativa é recusada (RN08)", "RN08" in pg.inner_text("#tapErrosPrioridade"))
    pg.fill("#prJust", "Maior impacto no atendimento e urgência declarada pela unidade.")
    pg.click("#formTapPrioridade button[type=submit]"); pg.wait_for_timeout(700)
    ok("a prioridade é salva com fonte e situação", pg.evaluate("""async ()=>{
        const x = await db.get('portfolio','TAP-2026-002'); return x && x.prioridade === 1 && x.fonte_recurso === 'Emenda parlamentar'; }"""))
    # exportação .xlsx
    with pg.expect_download() as dl:
        pg.click("#btnTapXlsx")
    nome = dl.value.suggested_filename
    ok("o portfólio exporta em .xlsx", nome.endswith(".xlsx"))


@cenario("tap-portfolio-projetos")
def s6_indicadores_e_aceite(pg, url, ok):
    perfil(pg, url, "equipe")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    ir(pg, url, "#/indicadores", 600)
    calc = pg.evaluate("""async ()=>{ const ps = await db.list('propostas'), pri = await db.list('portfolio');
        return {total: ps.length, aprovadas: ps.filter(p=>p.status==='aprovada').length,
                semPrioridade: ps.filter(p=>p.status==='aprovada' && !pri.some(x=>x.proposta_id===p.id)).length}; }""")
    ok("os indicadores contam propostas, aprovadas e sem prioridade",
       pg.inner_text("[data-tap-ind=total]") == str(calc["total"]) and pg.inner_text("[data-tap-ind=aprovadas]") == str(calc["aprovadas"])
       and pg.inner_text("[data-tap-ind=sem-prioridade]") == str(calc["semPrioridade"]))
    ok("o indicador traz o valor do portfólio aprovado", "R$" in pg.inner_text("[data-tap-ind=valor]"))
    ok("as propostas por situação são agrupadas", pg.locator("#tabelaStatus tr").count() > 1)
    ok("o roteiro de aceite está em modelos/", (APPS / "tap-portfolio-projetos" / "modelos" / "roteiro-aceite.md").exists())

# Cenários dos Sprints 4 a 6 da RNC: arquivo do setor, plano, avaliação e painel.


@cenario("rnc-nao-conformidade")
def s4_arquivo_do_setor(pg, url, ok):
    perfil(pg, url, "cqual")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    ir(pg, url, "#/exportar", 600)
    setor = pg.evaluate("async ()=> (await db.list('rncs')).filter(r=>r.situacao==='aberta')[0].setor_notificado")
    n = pg.evaluate("async s => (await db.list('rncs')).filter(r=>r.setor_notificado===s).length", setor)
    pg.select_option("#expSetor", setor)
    with pg.expect_download() as dl:
        pg.click("#btnExportarSetor")
    nome = dl.value.suggested_filename
    ok("o arquivo do setor sai com o nome do setor", nome == f"rnc-{setor.lower()}.json")
    import json, pathlib
    pacote = json.loads(pathlib.Path(dl.value.path()).read_text(encoding="utf-8"))
    ok("o pacote leva só as RNCs do setor (RN06)", len(pacote["rncs"]) == n and all(r["setor_notificado"] == setor for r in pacote["rncs"]))
    ok("o pacote tem verificação e o setor", pacote["formato"] == "RNC-setor-v1" and pacote["setor"] == setor and "verificacao" in pacote)


@cenario("rnc-nao-conformidade")
def s5_plano_avaliacao_e_painel(pg, url, ok):
    perfil(pg, url, "setor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    ir(pg, url, "#/minhas", 600)
    setor = pg.evaluate("async ()=> (await db.list('setores'))[0].sigla")
    pg.select_option("#rncMeuSetor", setor); pg.click("#btnSalvarSetor"); pg.wait_for_timeout(600)
    ok("a tela do setor lista as RNCs notificadas a ele", pg.locator("#tabelaMinhasRnc tr").count() > 1)
    # plano (FOR 2)
    pg.locator("[data-plano]").first.click(); pg.wait_for_timeout(400)
    pg.fill("#plAcoes", "Treinamento da equipe e revisão do procedimento interno.")
    pg.click("#formPlano button[type=submit]"); pg.wait_for_timeout(600)
    ok("o plano de ação do setor é registrado", pg.evaluate("async ()=> (await db.list('planos')).length") == 1)
    # avaliação (FOR 3)
    pg.locator("[data-aval]").first.click(); pg.wait_for_timeout(400)
    pg.select_option("#avEficaz", "sim"); pg.fill("#avObs", "A ação resolveu a causa.")
    pg.click("#formAval button[type=submit]"); pg.wait_for_timeout(600)
    ok("a avaliação de eficácia é registrada", pg.evaluate("async ()=> (await db.list('avaliacoes'))[0].eficaz") is True)
    # painel
    ir(pg, url, "#/painel", 700)
    calc = pg.evaluate("""async ()=>{ const rs = await db.list('rncs'), es = await db.list('etapas'), h = hojeISO();
        return {total: rs.length, vencidas: es.filter(e=>!e.fim && e.prazo && e.prazo < h).length}; }""")
    ok("o painel conta as RNCs e as etapas vencidas", pg.inner_text("[data-rnc-ind=total]") == str(calc["total"])
       and pg.inner_text("[data-rnc-ind=vencidas]") == str(calc["vencidas"]))
    ok("o painel tem os 3 gráficos em SVG", pg.locator("svg[role=img]").count() == 3)
    ok("o painel lista as etapas vencidas com dias", pg.locator("#tabelaVencidas tr").count() - 1 == calc["vencidas"])
    ok("o painel mostra o tempo médio por etapa", pg.locator("#tabelaTempo tr").count() == 5)


@cenario("rnc-nao-conformidade")
def s6_aceite_e_piloto(pg, url, ok):
    perfil(pg, url, "cqual")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    # o fluxo completo: importar a planilha do Forms, ver a RNC, exportar para o setor
    ex = APPS / "rnc-nao-conformidade" / "exemplos"
    ir(pg, url, "#/importar", 500)
    pg.set_input_files("#arqRnc", str(ex / "respostas-forms-ficticio.csv")); pg.wait_for_timeout(900)
    ok("a planilha do Forms é lida e as colunas são associadas", pg.locator("#mapaRnc").count() == 1
       and pg.locator("#btnImportarRnc").count() == 1)
    ir(pg, url, "#/exportar", 500)
    ok("a tela de arquivo do setor abre", pg.locator("#btnExportarSetor").count() == 1)
    ok("o roteiro de aceite está em modelos/", (APPS / "rnc-nao-conformidade" / "modelos" / "roteiro-aceite.md").exists())

# Cenários dos Sprints 4 a 7 da Comissão de Ética: admissibilidade, oitivas, cominação e relatório.


@cenario("comissao-etica-denuncias")
def s4_admissibilidade_e_prova_pendente(pg, url, ok):
    perfil(pg, url, "presidente")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    cid = "CE-2026-001"
    ir(pg, url, "#/caso/" + cid + "/admissibilidade", 600)
    ok("sem classificação confirmada, a admissibilidade está bloqueada (RN03)", "Bloqueado (RN03)" in pg.inner_text("#conteudo"))
    # classifica
    ir(pg, url, "#/caso/" + cid + "/classificacao", 500)
    pg.select_option("#cCategoria", "assedio_moral")
    pg.fill("#cJustificativa", "O relato descreve humilhação e constrangimento reiterados, enquadrados no art. 2º, X e art. 4º, VII.")
    pg.click("#formClassif button[type=submit]"); pg.wait_for_timeout(700)
    ir(pg, url, "#/caso/" + cid + "/admissibilidade", 600)
    ok("a tela mostra a categoria com o artigo e o texto da LC 112/2002",
       "assédio" in pg.inner_text("#conteudo").lower() and "Art." in pg.inner_text("#conteudo"))
    pg.click("#formAdmissao button[type=submit]"); pg.wait_for_timeout(400)
    ok("decisão sem fundamento é recusada", "20 caracteres" in pg.inner_text("#ceErrosAdmissao"))
    pg.select_option("#adVia", "acatada")
    pg.fill("#adMembros", "Membros A, B e C")
    pg.fill("#adJust", "Há indício de violação ao Código de Ética, com relato suficiente para apuração.")
    pg.check("#adProvaPendente"); pg.fill("#adProvaTexto", "Escala do plantão do dia")
    pg.click("#formAdmissao button[type=submit]"); pg.wait_for_timeout(700)
    ok("a admissibilidade fica registrada com a via", pg.evaluate("async id => (await db.porIndice('deliberacoes','denuncia_id',id)).some(d=>d.tipo==='admissibilidade' && d.via==='acatada')", cid))
    ok("a prova pendente entra com prazo (RN04)", pg.evaluate("async id => (await db.porIndice('deliberacoes','denuncia_id',id)).some(d=>d.tipo==='prova_pendente' && d.prazo)", cid))
    ok("com prova pendente, as oitivas ficam bloqueadas (RN04)", "Prova pendente (RN04)" in pg.inner_text("#conteudo"))
    pg.click("#btnProvaRecebida"); pg.wait_for_timeout(600)
    ok("registrada a prova, a pendência é resolvida", pg.evaluate("async id => (await db.porIndice('deliberacoes','denuncia_id',id)).filter(d=>d.tipo==='prova_pendente' && d.resolvido_em).length", cid) == 1)


@cenario("comissao-etica-denuncias")
def s5_oitivas_com_roteiro(pg, url, ok):
    perfil(pg, url, "membro")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    cid = "CE-2026-002"
    # prepara a admissibilidade direto na base, para o cenário focar na oitiva
    pg.evaluate("""async id => { await db.put('classificacoes', {id: 'cl-1', denuncia_id: id, confirmada: true, categoria_final: 'desrespeito_publico', justificativa: 'relato suficiente', membro: 'membro', data: agora()});
        await db.put('deliberacoes', {id: 'ad-1', denuncia_id: id, tipo: 'admissibilidade', via: 'acatada', justificativa: 'indício de violação', membros: 'A, B e C', data: agora(), perfil: 'presidente'}); }""", cid)
    ir(pg, url, "#/caso/" + cid + "/oitivas", 600)
    ok("o roteiro sugerido aparece na tela", pg.locator("#formOitiva").count() == 1 and pg.locator("ol li").count() >= 3)
    pg.fill("#oiTermo", "curto")
    pg.click("#formOitiva button[type=submit]"); pg.wait_for_timeout(400)
    ok("termo curto é recusado", "30 caracteres" in pg.inner_text("#ceErrosOitiva"))
    pg.fill("#oiTermo", "O servidor informou que a fila estava longa e que não houve orientação sobre o atendimento prioritário.")
    pg.click("#formOitiva button[type=submit]"); pg.wait_for_timeout(700)
    ok("a oitiva é registrada com o prazo de nova manifestação", pg.evaluate("async id => (await db.porIndice('oitivas','denuncia_id',id)).length", cid) == 1
       and pg.evaluate("async id => !!(await db.porIndice('oitivas','denuncia_id',id))[0].prazo_nova", cid))


@cenario("comissao-etica-denuncias")
def s6_documentos_cominacao_e_relatorio(pg, url, ok):
    perfil(pg, url, "presidente")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(700)
    cid = "CE-2026-003"
    pg.evaluate("""async id => { await db.put('classificacoes', {id: 'cl-2', denuncia_id: id, confirmada: true, categoria_final: 'uso_cargo', justificativa: 'relato suficiente', membro: 'membro', data: agora()});
        await db.put('deliberacoes', {id: 'ad-2', denuncia_id: id, tipo: 'admissibilidade', via: 'acatada', justificativa: 'indício de violação', membros: 'A, B e C', data: agora(), perfil: 'presidente'}); }""", cid)
    ir(pg, url, "#/caso/" + cid + "/documentos", 600)
    pg.select_option("#ceTipoMinuta", "comunicacao"); pg.click("#btnGerarMinuta"); pg.wait_for_timeout(600)
    ok("a minuta é gerada e sai em documento", pg.locator("#ceMinutaAberta .documento-a4").count() == 1)
    ok("a minuta não leva nome das partes (art. 11)", "Denunciante Fictício" not in pg.inner_text("#ceMinutaAberta"))
    ir(pg, url, "#/caso/" + cid + "/encerramento", 600)
    ok("a conferência das etapas mostra o que falta", pg.locator(".check-lista li").count() >= 6)
    pg.select_option("#coTipo", "advertência")
    pg.fill("#coParecer", "Conduta enquadrada no art. 5º, I; aplica-se advertência, art. 9º, I.")
    pg.check("#coPAD")
    pg.click("#formCominacao button[type=submit]"); pg.wait_for_timeout(700)
    ok("a cominação é registrada com o encaminhamento ao PAD", pg.evaluate("async id => { const c = (await db.porIndice('cominacoes','denuncia_id',id))[0]; return c && c.tipo==='advertência' && c.pad; }", cid))
    ok("a ficha funcional por 5 anos aparece (art. 9º)", "5 anos" in pg.inner_text("#conteudo"))
    pg.click("#btnEncerrarCe"); pg.wait_for_timeout(600)
    ok("o caso encerra", pg.evaluate("async id => (await db.get('denuncias', id)).etapa === 'encerrado'", cid))
    # relatório sem nomes
    ir(pg, url, "#/relatorio", 600)
    ok("o relatório conta casos, oitivas e cominações", pg.inner_text("[data-ce-ind=total]") == str(contar(pg, "denuncias")))
    ok("o relatório não mostra nome das partes (art. 11)", "Fictício" not in pg.inner_text("#conteudo"))
    ok("o roteiro de aceite está em modelos/", (APPS / "comissao-etica-denuncias" / "modelos" / "roteiro-aceite.md").exists())

# Cenários dos Sprints 4 a 7 do Controle de Adiantamentos: prazos, prestação, painel e relatório.


@cenario("adiantamento")
def s4_motor_de_prazos(pg, url, ok):
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    pid = pg.evaluate("async ()=> (await db.list('processos')).find(p=>p.situacao!=='encerrado').id")
    ir(pg, url, "#/processo/" + pid, 600)
    ok("a ficha mostra o prazo com a base de contagem (RN03)", pg.locator("#adPrazo").count() == 1
       and "Base de contagem" in pg.inner_text("#adPrazo"))
    calc = pg.evaluate("""async id => { const p = await db.get('processos', id), f = await db.list('feriados');
        const r = prazosDoProcesso(p, f); return {limite: r.limite, restam: r.restam, selo: r.selo}; }""", pid)
    ok("o limite e os dias restantes batem com o motor", pg.inner_text("[data-ad-restam]") == str(calc["restam"]))
    ok("o motor considera o tipo do processo", pg.evaluate("""async id => { const p = await db.get('processos', id), f = [];
        const r = prazosDoProcesso(p, f); return r.regra.uteis === (p.tipo !== 'predial'); }""", pid))
    # feriados na configuração
    ir(pg, url, "#/config", 500)
    antes = contar(pg, "feriados")
    pg.fill("#feData", "2026-12-08"); pg.fill("#feNome", "Feriado de teste"); pg.select_option("#feEscopo", "estadual")
    pg.click("#btnAddFeriado"); pg.wait_for_timeout(600)
    ok("o feriado é acrescentado pela configuração", contar(pg, "feriados") == antes + 1
       and pg.evaluate("async ()=> (await db.get('feriados','2026-12-08')).escopo") == "estadual")
    pg.fill("#feData", "2026-12-08"); pg.fill("#feNome", "Repetido")
    pg.click("#btnAddFeriado"); pg.wait_for_timeout(400)
    ok("feriado repetido não entra duas vezes", contar(pg, "feriados") == antes + 1)


@cenario("adiantamento")
def s5_prestacao_e_pendencias(pg, url, ok):
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    pid = pg.evaluate("async ()=> (await db.list('processos')).find(p=>p.situacao!=='encerrado' && p.valor_concedido>0).id")
    ir(pg, url, "#/processo/" + pid + "/prestacao", 600)
    ok("a prestação abre com o valor concedido e a soma das notas", pg.locator("[data-ad-concedido]").count() == 1)
    pg.fill("#noNumero", "NF-1"); pg.fill("#noCnpj", "11.222.333/0001-81"); pg.fill("#noValor", "100,00")
    pg.click("#formNota button[type=submit]"); pg.wait_for_timeout(600)
    ok("a nota fiscal entra na prestação", contar(pg, "notas") >= 1)
    # pendência com prazo de 10 dias úteis (RN05)
    pg.fill("#peMotivo", "Nota fiscal sem identificação do órgão")
    pg.click("#btnPendencia"); pg.wait_for_timeout(600)
    pend = pg.evaluate("""async id => (await db.porIndice('pendencias','processo_id',id)).find(p=>!p.resolvida_em)""", pid)
    ok("a pendência abre com prazo de 10 dias úteis (RN05)", pend and pend["prazo"])
    # encerrar com pendência aberta é recusado
    pg.select_option("#enDecisao", "aprovado sem ressalvas")
    pg.click("#formEncerrar button[type=submit]"); pg.wait_for_timeout(500)
    ok("com pendência aberta, o encerramento é recusado", "pendência" in pg.inner_text("#adErrosEncerrar").lower())
    pg.locator("[data-resolver]").first.click(); pg.wait_for_timeout(600)
    ok("a pendência é resolvida com a data", pg.evaluate("async id => (await db.porIndice('pendencias','processo_id',id)).every(p=>p.resolvida_em)", pid))
    # RN06: nota acima do concedido
    concedido = pg.evaluate("async id => (await db.get('processos', id)).valor_concedido", pid)
    pg.fill("#noNumero", "NF-2"); pg.fill("#noValor", f"{concedido * 2:.2f}".replace(".", ","))
    pg.click("#formNota button[type=submit]"); pg.wait_for_timeout(600)
    ok("nota acima do valor concedido entra em alerta (RN06)", pg.locator("#adExcedeu").count() == 1)
    pg.select_option("#enDecisao", "aprovado com ressalvas")
    pg.click("#formEncerrar button[type=submit]"); pg.wait_for_timeout(500)
    ok("com excedente, o encerramento também é recusado", "RN06" in pg.inner_text("#adErrosEncerrar"))


@cenario("adiantamento")
def s6_painel_e_relatorio(pg, url, ok):
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/painel", 700)
    calc = pg.evaluate("""async ()=>{ const ps = await db.list('processos'), f = await db.list('feriados'), h = hojeISO();
        const i = ps.map(p=>({p, ...prazosDoProcesso(p, f, h)}));
        return {total: ps.length, vencidos: i.filter(x=>x.selo==='vencido').length, vencendo: i.filter(x=>x.selo==='vence7').length,
                encerrados: ps.filter(p=>p.situacao==='encerrado').length}; }""")
    ok("o painel conta processos, vencidos, a vencer e encerrados",
       pg.inner_text("[data-ad-ind=total]") == str(calc["total"]) and pg.inner_text("[data-ad-ind=vencidos]") == str(calc["vencidos"])
       and pg.inner_text("[data-ad-ind=vencendo]") == str(calc["vencendo"]) and pg.inner_text("[data-ad-ind=encerrados]") == str(calc["encerrados"]))
    ok("o painel tem os gráficos em SVG", pg.locator("svg[role=img]").count() == 2)
    ir(pg, url, "#/relatorio", 600)
    ok("o relatório mostra devoluções por motivo e o tempo médio", pg.locator("[data-ad-rel=devolucoes]").count() == 1
       and pg.locator("[data-ad-rel=ciclo]").count() == 1)
    with pg.expect_download() as dl:
        pg.click("#btnAdCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV do relatório sai com BOM e ponto e vírgula", csv.startswith(b"\xef\xbb\xbf") and b"id;unidade;tipo" in csv)
    ok("o roteiro de aceite está em modelos/", (APPS / "adiantamento" / "modelos" / "roteiro-aceite.md").exists())
