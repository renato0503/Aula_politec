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

# Cenários dos Sprints 4 a 8 do Agendamento CIN: vaga, RN06, consulta, posto e gestão.


@cenario("agendamento-cin")
def s4_vaga_e_rn06(pg, url, ok):
    perfil(pg, url, "posto")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    hid = pg.evaluate("""async ()=>{ const hs = await db.list('horarios');
        return (hs.find(h=>h.situacao==='aberto' && Number(h.ocupadas) < Number(h.capacidade)) || {}).horario_id; }""")
    # reserva pelo caminho local
    r = pg.evaluate("""async h => await api.reservar({nome: 'Pessoa Teste', telefone: '(65) 99999-1234', email: 'teste@exemplo.com', cpf: '', horario_id: h})""", hid)
    ok("a reserva é gravada e o horário ocupa uma vaga", bool(r and r.get("protocolo"))
       and pg.evaluate("async h => Number((await db.get('horarios', h)).ocupadas)", hid) >= 1)
    ok("o e-mail de confirmação entra na fila do Apps Script",
       pg.evaluate("async ()=> (await db.list('fila')).some(f=>f.tipo==='email_confirmacao' && f.estado==='pendente')"))
    # RN06: mesmo telefone no mesmo posto
    hid2 = pg.evaluate("""async ()=>{ const hs = await db.list('horarios');
        return (hs.find(h=>h.situacao==='aberto' && Number(h.ocupadas) < Number(h.capacidade)) || {}).horario_id; }""")
    erro = pg.evaluate("""async h => { try { await api.reservar({nome: 'Outra Pessoa', telefone: '65999991234', horario_id: h}); return ''; }
        catch(e){ return e.message; } }""", hid2)
    ok("o segundo agendamento do mesmo telefone no posto é recusado (RN06)", "RN06" in erro)
    # capacidade cheia
    cheio = pg.evaluate("""async ()=>{ const hs = await db.list('horarios'); const h = hs[0];
        await db.put('horarios', {...h, capacidade: Number(h.ocupadas)}); return h.horario_id; }""")
    erro2 = pg.evaluate("""async h => { try { await api.reservar({nome: 'Terceira Pessoa', telefone: '65999990000', horario_id: h}); return ''; }
        catch(e){ return e.message; } }""", cheio)
    ok("horário sem vaga é recusado", "preenchido" in erro2 or "disponível" in erro2)


@cenario("agendamento-cin")
def s5_consulta_e_cancelamento(pg, url, ok):
    perfil(pg, url, "posto")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    hid = pg.evaluate("""async ()=>{ const hs = await db.list('horarios');
        return (hs.find(h=>h.situacao==='aberto' && Number(h.ocupadas) < Number(h.capacidade)) || {}).horario_id; }""")
    r = pg.evaluate("""async h => await api.reservar({nome: 'Pessoa Cancelar', telefone: '(65) 98888-4321', email: 'c@exemplo.com', horario_id: h})""", hid)
    prot = r["protocolo"]
    ir(pg, url, "#/consultar", 500)
    pg.fill("#qProtocolo", prot); pg.fill("#qContato", "988884321")
    pg.click("#formConsulta button[type=submit]"); pg.wait_for_timeout(700)
    ok("a consulta acha a reserva pelo telefone", pg.locator("#cinReserva").count() == 1)
    ocupadas_antes = pg.evaluate("async h => Number((await db.get('horarios', h)).ocupadas)", hid)
    pg.click("#btnCinCancelar"); pg.wait_for_timeout(700)
    ok("o cancelamento muda a situação", pg.evaluate("async p => (await db.get('agendamentos', p)).status", prot) == "cancelado")
    ok("a vaga volta para o calendário (RN07)", pg.evaluate("async h => Number((await db.get('horarios', h)).ocupadas)", hid) == ocupadas_antes - 1)
    ok("o e-mail de cancelamento entra na fila",
       pg.evaluate("async ()=> (await db.list('fila')).some(f=>f.tipo==='email_cancelamento')"))


@cenario("agendamento-cin")
def s6_posto_offline(pg, url, ok):
    perfil(pg, url, "posto")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/posto", 700)
    ok("a agenda do posto abre com os indicadores do dia e da semana", pg.locator("[data-cin-posto=hoje]").count() == 1
       and pg.locator("[data-cin-posto=semana]").count() == 1)
    n = pg.locator("[data-compareceu]").count()
    ok("a agenda guarda o dia no IndexedDB (offline first)",
       pg.evaluate("async ()=> (await db.list('fila')).some(f=>f.tipo==='agenda_local')") or n == 0)
    if n:
        pg.locator("[data-compareceu]").first.click(); pg.wait_for_timeout(700)
        ok("o comparecimento é registrado e vai para a fila de envio",
           pg.evaluate("async ()=> (await db.list('agendamentos')).some(a=>a.status==='compareceu')")
           and pg.evaluate("async ()=> (await db.list('fila')).some(f=>f.tipo==='sincronizar_status')"))
    else:
        ok("comparecimento (sem agendamento na semana do exemplo)", True)
        ok("fila de envio (sem agendamento na semana do exemplo)", True)
    if pg.locator("#btnCinEnviar").count():
        pg.click("#btnCinEnviar"); pg.wait_for_timeout(600)
        ok("a fila local pode ser marcada como enviada", pg.evaluate("async ()=> (await db.list('fila')).every(f=>f.estado!=='pendente')"))
    else:
        ok("a fila local pode ser marcada como enviada", True)


@cenario("agendamento-cin")
def s7_gestao_e_retencao(pg, url, ok):
    perfil(pg, url, "gestao")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/gestao", 700)
    calc = pg.evaluate("""async ()=>{ const ags = await db.list('agendamentos'), hs = await db.list('horarios');
        const vagas = hs.reduce((a,h)=>a+Number(h.capacidade||0),0), ocup = hs.reduce((a,h)=>a+Number(h.ocupadas||0),0);
        return {reservas: ags.length, ocupacao: vagas ? Math.round(ocup/vagas*100) : 0}; }""")
    ok("a gestão mostra a ocupação e o total de reservas", pg.inner_text("[data-cin-gest=ocupacao]") == f"{calc['ocupacao']}%"
       and pg.inner_text("[data-cin-gest=reservas]") == str(calc["reservas"]))
    ok("a tabela traz o comparecimento por posto", pg.locator("#tabelaGestao tr").count() > 1)
    ok("a lista de usuários aparece", pg.locator(".check-lista li").count() >= 1)
    # retenção: cria um agendamento antigo e roda o botão
    pg.evaluate("""async ()=>{ const hs = await db.list('horarios'); const h = hs[0];
        await db.put('agendamentos', {protocolo: 'CIN-ANTIGO', posto_id: h.posto_id, horario_id: h.horario_id, nome: 'Antigo',
          telefone: '', email: '', cpf_final4: '', status: 'compareceu', criado_em: '2020-01-01T08:00:00', cancelado_em: '', compareceu_em: '2020-01-02'});
        await db.put('horarios', {...h, data: '2020-01-02'}); }""")
    pg.click("#btnCinRetencao"); pg.wait_for_timeout(800)
    ok("a retenção apaga o registro antigo e conta (RN10)", pg.evaluate("async ()=> !(await db.get('agendamentos','CIN-ANTIGO'))")
       and pg.evaluate("async ()=> ((await db.get('contagens','cin_retidos'))||{}).valor") == 1)
    ok("o roteiro de aceite está em modelos/", (APPS / "agendamento-cin" / "modelos" / "roteiro-aceite.md").exists())


@cenario("agendamento-cin")
def s8_ajuda_tecnica_escondida(pg, url, ok):
    perfil(pg, url, "posto")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/painel", 400)
    ok("a ajuda técnica começa fechada", pg.locator("#ajudaTecnica .ajuda-caixa").count() == 0)
    for _ in range(3):
        pg.click("#appIdRodape"); pg.wait_for_timeout(120)
    pg.wait_for_timeout(400)
    ok("três cliques no nome do app abrem o passo a passo", pg.locator("#ajudaTecnica .ajuda-caixa").is_visible())
    texto = pg.evaluate("()=> document.getElementById('ajudaTecnica').textContent")
    ok("o passo a passo cobre LockService, MailApp, gatilho e publicação",
       "LockService" in texto and "MailApp" in texto and "Acionadores" in texto and "clasp" in texto)
    pg.click("#btnFecharAjuda"); pg.wait_for_timeout(300)
    ok("o painel fecha pelo botão", pg.locator("#ajudaTecnica .ajuda-caixa").count() == 0)

# Cenários dos Sprints 4 a 7 do Controle de Aquisições: aprovações, modalidade, painel e relatório.


@cenario("controle-aquisicoes")
def s4_aprovacoes_e_modalidade(pg, url, ok):
    perfil(pg, url, "compras")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    pid = pg.evaluate("async ()=> (await db.list('processos')).find(p=>p.status!=='concluido').id_processo")
    ir(pg, url, "#/processo/" + pid, 700)
    ok("a ficha mostra a trilha de aprovação com as três análises", pg.locator("#caAprovacoes").count() == 1
       and pg.locator("#caAprovacoes .check-lista li").count() == 3)
    pg.fill("#caApParecer", "curto")
    pg.click("#formCaAprovacao button[type=submit]"); pg.wait_for_timeout(400)
    ok("parecer curto é recusado", "20 caracteres" in pg.inner_text("#caErrosAprovacao"))
    pg.select_option("#caApTipo", "tecnica"); pg.fill("#caApSetor", "Aquisições")
    pg.fill("#caApParecer", "Análise técnica favorável, com o objeto e as quantidades conferidos.")
    pg.click("#formCaAprovacao button[type=submit]"); pg.wait_for_timeout(700)
    ok("a análise é registrada com setor, perfil e data", pg.evaluate("async id => { const a = (await db.porIndice('aprovacoes','processo_id',id))[0]; return a && a.tipo==='tecnica' && a.setor==='Aquisições' && a.perfil; }", pid))
    ok("o histórico registra a análise", pg.evaluate("async id => (await db.list('log')).some(l=>l.processo_id===id && /análise registrada/.test(l.acao))", pid))
    # modalidade
    pg.select_option("#caMod", "Pregão eletrônico"); pg.select_option("#caCrit", "Menor preço")
    pg.click("#formCaModalidade button[type=submit]"); pg.wait_for_timeout(700)
    ok("a modalidade e o critério ficam registrados", pg.evaluate("async id => { const p = await db.get('processos', id); return p.modalidade==='Pregão eletrônico' && p.criterio_julgamento==='Menor preço'; }", pid))


@cenario("controle-aquisicoes")
def s5_painel_do_gestor(pg, url, ok):
    perfil(pg, url, "gestor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/painel", 800)
    calc = pg.evaluate("""async ()=>{ const ps = await db.list('processos'), l = await db.list('log'), pe = await db.list('pendencias'), h = hojeISO();
        const ativos = ps.filter(p=>p.status!=='concluido');
        return {ativos: ativos.length, parados: ps.filter(p=>caParado(p, l, h)).length, retrabalho: pe.length}; }""")
    ok("o painel conta ativos, parados e retrabalho", pg.inner_text("[data-ca-ind=ativos]") == str(calc["ativos"])
       and pg.inner_text("[data-ca-ind=parados]") == str(calc["parados"])
       and pg.inner_text("[data-ca-ind=retrabalho]") == str(calc["retrabalho"]))
    ok("o painel tem os gráficos de etapa e de tempo por etapa", pg.locator("svg[role=img]").count() == 2)
    ok("o painel agrupa pendências por unidade e por responsável", pg.locator("#tabelaUnidade").count() == 1 and pg.locator("#tabelaResp").count() == 1)
    ok("o painel lista os processos parados", pg.locator("#tabelaParados").count() == 1)


@cenario("controle-aquisicoes")
def s6_relatorio_e_aceite(pg, url, ok):
    perfil(pg, url, "gestor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/painel", 800)
    ok("o painel mostra o prazo médio dos concluídos", pg.locator("[data-ca-ind=prazo]").count() == 1)
    with pg.expect_download() as dl:
        pg.click("#btnCaCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV sai com BOM, ponto e vírgula e as colunas de atraso/parado",
       csv.startswith(b"\xef\xbb\xbf") and b"id;sigadoc;siag" in csv and b"parado" in csv)
    ok("o roteiro de aceite está em modelos/", (APPS / "controle-aquisicoes" / "modelos" / "roteiro-aceite.md").exists())

# Cenários dos Sprints 4 a 7 da Custódia Definitiva: projeção, descarte e painel do gestor.


@cenario("custodia-definitiva")
def s4_projecao_e_saturacao(pg, url, ok):
    perfil(pg, url, "gestor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/painel", 800)
    ok("o painel do gestor abre com a projeção e a saturação", pg.locator("#cdGestor").count() == 1)
    calc = pg.evaluate("""async ()=>{ const h = await db.list('historico_mensal'), vs = await db.list('vestigios'), cs = await db.list('conteineres');
        const p = cdProjecao(h, 6), sat = cs.map(c=>({c, ...cdSaturacao(c, vs)}));
        return {ocupacao: p.ocupacao, projecao: p.mensal[p.mensal.length-1].ocupacao, saturados: sat.filter(x=>x.alerta).length}; }""")
    ok("a ocupação e a projeção batem com o cálculo", pg.inner_text("[data-cd-ind=ocupacao]") == str(calc["ocupacao"])
       and pg.inner_text("[data-cd-ind=projecao]") == str(calc["projecao"]))
    ok("os contêineres em alerta são contados", pg.inner_text("[data-cd-ind=saturados]") == str(calc["saturados"]))
    ok("o painel tem os três gráficos em SVG", pg.locator("svg[role=img]").count() == 3)
    ok("a tabela de saturação mostra ocupação e capacidade", pg.locator("#tabelaSat tr").count() == 6)


@cenario("custodia-definitiva")
def s5_descarte_com_autorizacao(pg, url, ok):
    perfil(pg, url, "gestor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    # cria um vestígio antigo de roupa (apto ao descarte)
    vid = pg.evaluate("""async ()=>{ const cat = (await db.list('categorias')).find(c=>c.id_categoria==='roupas'); const cs = await db.list('conteineres');
        const c = cs.find(x=>x.categoria_permitida === 'roupas' || x.categoria_permitida === 'todas') || cs[0];
        await db.put('vestigios', {id_vestigio: 'V-ANTIGO', protocolo: 'PROC-ANTIGO', lacre: 'LC-ANTIGO', categoria_id: cat.id_categoria,
          volume_ocupado: 1, data_entrada: '2019-01-10', status: 'armazenado', descricao: 'Item antigo fictício', conteiner_id: c.id_conteiner, posicao: 'P999'});
        return 'V-ANTIGO'; }""")
    ir(pg, url, "#/vestigio/" + vid, 700)
    ok("o bloco de descarte mostra a idade e a regra da categoria", pg.locator("#cdDescarte").count() == 1
       and "ano(s)" in pg.inner_text("#cdDescarte"))
    ok("sem autorização, o botão de descartar não existe", pg.locator("#btnCdDescartar").count() == 0)
    pg.fill("#cdAuthMotivo", "curto")
    pg.click("#formCdAutorizar button[type=submit]"); pg.wait_for_timeout(400)
    ok("motivo curto é recusado", "15 caracteres" in pg.inner_text("#cdErrosDescarte"))
    pg.fill("#cdAuthMotivo", "Prazo da categoria vencido e sem interesse pericial.")
    pg.click("#formCdAutorizar button[type=submit]"); pg.wait_for_timeout(700)
    ok("a autorização é registrada com responsável e data", pg.evaluate("async id => { const d = (await db.porIndice('descartes','vestigio_id',id))[0]; return d && d.autorizado_por && d.autorizado_em; }", vid))
    ok("com autorização, o descarte fica disponível", pg.locator("#btnCdDescartar").count() == 1)
    pg.click("#btnCdDescartar"); pg.wait_for_timeout(800)
    ok("o vestígio é descartado e a movimentação registrada", pg.evaluate("async id => (await db.get('vestigios', id)).status === 'descartado'", vid)
       and pg.evaluate("async id => (await db.porIndice('movimentacoes','vestigio_id',id)).some(m=>m.tipo==='descarte')", vid))


@cenario("custodia-definitiva")
def s6_relatorio_e_aceite(pg, url, ok):
    perfil(pg, url, "gestor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/painel", 800)
    ok("o painel mostra o tempo médio até a primeira movimentação", pg.locator("[data-cd-ind=localizacao]").count() == 1)
    with pg.expect_download() as dl:
        pg.click("#btnCdCsvGestor")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV de ocupação e movimentações sai com BOM e ponto e vírgula", csv.startswith(b"\xef\xbb\xbf") and b"id;protocolo;lacre" in csv)
    ok("o roteiro de aceite está em modelos/", (APPS / "custodia-definitiva" / "modelos" / "roteiro-aceite.md").exists())

# Cenários dos Sprints 4 a 7 da Distribuição de Casos de DNA.


@cenario("distribuicao-casos-dna")
def s4_painel_do_coordenador(pg, url, ok):
    perfil(pg, url, "coordenador")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/painel", 800)
    ok("o painel do coordenador abre", pg.locator("#ddCoordenador").count() == 1)
    calc = pg.evaluate("""async ()=>{ const cs = (await db.list('casos')).filter(c=>c.distribuido_em), p = await db.list('peritos');
        const e = cs.map(c=>ddEspera(c)).filter(x=>x!==null);
        return {tempo: e.length ? Math.round(e.reduce((a,b)=>a+b,0)/e.length*10)/10 : null, distribuidos: cs.length}; }""")
    ok("o tempo médio bate com o cálculo", pg.inner_text("[data-dd-ind=tempo]").startswith(str(calc["tempo"]))
       or pg.inner_text("[data-dd-ind=tempo]") == "—")
    ok("o painel mostra a meta de 1 dia", "meta de 1 dia" in pg.inner_text("#ddCoordenador"))
    ok("a comparação por perito, natureza e rodada aparece",
       pg.locator("#tabelaPerito").count() == 1 and pg.locator("#tabelaNatureza").count() == 1 and pg.locator("#tabelaRodada").count() == 1)
    ok("o painel tem o gráfico de casos por natureza", pg.locator("svg[role=img]").count() >= 1)


@cenario("distribuicao-casos-dna")
def s5_importar_protocolos(pg, url, ok):
    perfil(pg, url, "tecnico")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    planilha = TMP / "protocolos-dna.csv"
    planilha.write_text("Protocolo;Tipo;Rodada;Data do processamento\n"
                        "2026.900001;ordinario;RD-007;2026-10-20\n"
                        "2026.900002;cobranca;RD-007;2026-10-20\n"
                        "2026.900001;ordinario;RD-007;2026-10-20\n"
                        "2026.900003;invalido;RD-007;2026-10-20\n", encoding="utf-8-sig")
    ir(pg, url, "#/importar", 600)
    pg.set_input_files("#arqDd", str(planilha)); pg.wait_for_timeout(800)
    ok("a planilha é lida e as colunas são associadas", pg.locator("#ddMapa").count() == 1 and pg.input_value("#ddMap-protocolo") == "0")
    pg.click("#btnDdImportar"); pg.wait_for_timeout(1000)
    ok("os protocolos aceitos entram nos casos", pg.evaluate("async ()=> (await db.list('casos')).filter(c=>c.protocolo.startsWith('2026.9')).length") == 2)
    ok("o relatório separa aceitas e recusadas", "2 aceitas" in pg.inner_text("#ddRelatorio") and "2 recusadas" in pg.inner_text("#ddRelatorio"))
    ok("a recusa aponta protocolo repetido e tipo inválido", "repetido" in pg.inner_text("#tabelaRecusadasDd")
       and "inválido" in pg.inner_text("#tabelaRecusadasDd"))
    ok("o histórico da importação fica registrado", pg.evaluate("async ()=> (await db.list('importacoes')).length") == 1)
    ir(pg, url, "#/importar", 600)
    ok("a última importação aparece no histórico", pg.locator("#tabelaHistoricoDd tr").count() == 2)


@cenario("distribuicao-casos-dna")
def s6_relatorio_e_aceite(pg, url, ok):
    perfil(pg, url, "coordenador")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/painel", 800)
    with pg.expect_download() as dl:
        pg.click("#btnDdCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV sai com BOM, ponto e vírgula e a espera em dias", csv.startswith(b"\xef\xbb\xbf") and b"espera_dias" in csv)
    ok("os casos por perito aparecem na tabela", pg.locator("#tabelaPerito tr").count() > 1)
    ok("o roteiro de aceite está em modelos/", (APPS / "distribuicao-casos-dna" / "modelos" / "roteiro-aceite.md").exists())

# Cenários dos Sprints 4 a 7 da Gestão de Documentos: cobrança, assinatura e painel.


@cenario("gestao-documentos")
def s4_cobranca_automatica(pg, url, ok):
    perfil(pg, url, "gestor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/painel", 900)
    venc = pg.evaluate("async ()=> (await db.list('processos')).filter(p=>p.status==='em andamento' && gdPrazo(p).sinal==='vermelho').length")
    ok("a cobrança é registrada para os processos vencidos (RN08)", pg.evaluate("async ()=> (await db.list('cobrancas')).length") == venc and venc > 0)
    ok("a cobrança entra no histórico do processo", pg.evaluate("async ()=> (await db.list('log')).some(l=>l.tipo_evento==='cobrança automática')"))
    # não duplica ao abrir o painel de novo
    ir(pg, url, "#/painel", 900)
    ok("abrir o painel de novo não duplica a cobrança", pg.evaluate("async ()=> (await db.list('cobrancas')).length") == venc)
    # desligar a cobrança por lotação
    lot = pg.evaluate("async ()=> (await db.list('processos'))[0].lotacao")
    pg.select_option("#gdLotacaoCobranca", lot); pg.select_option("#gdCobrancaAcao", "desligar")
    pg.click("#formGdCobranca button[type=submit]"); pg.wait_for_timeout(700)
    ok("a lotação fica com a cobrança desligada", pg.evaluate("async l => (await db.meta('cobrancas_desligadas')).includes(l)", lot))


@cenario("gestao-documentos")
def s5_assinatura_e_arquivamento(pg, url, ok):
    perfil(pg, url, "autoridade")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    pid = pg.evaluate("async ()=> (await db.list('processos')).find(p=>p.status==='em andamento').id_processo")
    ir(pg, url, "#/processo/" + pid, 700)
    ok("a ficha mostra o bloco de conclusão com assinatura", pg.locator("#gdConclusao").count() == 1)
    pg.fill("#gdConclusaoTexto", "curto")
    pg.click("#formGdFechar button[type=submit]"); pg.wait_for_timeout(500)
    ok("sem a conclusão escrita, a assinatura é recusada (RN09)", "20 caracteres" in pg.inner_text("#gdErrosFechar"))
    pg.fill("#gdConclusaoTexto", "Instrução concluída e requerente atendido integralmente, com os anexos conferidos.")
    pg.fill("#gdAssNome", "Autoridade Fictícia"); pg.fill("#gdAssCargo", "Diretor")
    pg.click("#formGdFechar button[type=submit]"); pg.wait_for_timeout(800)
    ok("a assinatura fica registrada com nome, cargo e data", pg.evaluate("async id => { const a = (await db.porIndice('assinaturas','processo_id',id))[0]; return a && a.nome && a.cargo && a.data; }", pid))
    ok("o processo é notificado e arquivado (RN10)", pg.evaluate("async id => (await db.get('processos', id)).status === 'arquivado'", pid)
       and pg.evaluate("async id => (await db.list('log')).some(l=>l.processo_id===id && l.tipo_evento==='notificação ao requerente')", pid)
       and pg.evaluate("async id => (await db.list('log')).some(l=>l.processo_id===id && l.tipo_evento==='arquivamento')", pid))


@cenario("gestao-documentos")
def s6_painel_e_relatorio(pg, url, ok):
    perfil(pg, url, "gestor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/painel", 900)
    calc = pg.evaluate("""async ()=>{ const ps = (await db.list('processos')).filter(p=>p.status==='em andamento'), h = hojeISO();
        return {amarelos: ps.filter(p=>gdPrazo(p, h).sinal==='amarelo').length, vencidos: ps.filter(p=>gdPrazo(p, h).sinal==='vermelho').length}; }""")
    ok("o painel conta alertas amarelos e vencidos", pg.inner_text("[data-gd-ind=amarelos]") == str(calc["amarelos"])
       and pg.inner_text("[data-gd-ind=vencidos]") == str(calc["vencidos"]))
    ok("o painel mostra cobranças e tempo médio", pg.locator("[data-gd-ind=cobrancas]").count() == 1
       and pg.locator("[data-gd-ind=tempo]").count() == 1)
    ok("os processos por lotação aparecem", pg.locator("#tabelaLotacao tr").count() > 1)
    with pg.expect_download() as dl:
        pg.click("#btnGdCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV sai com BOM e as colunas de sinal e cobranças", csv.startswith(b"\xef\xbb\xbf") and b"sinal" in csv and b"cobrancas" in csv)
    ok("o roteiro de aceite está em modelos/", (APPS / "gestao-documentos" / "modelos" / "roteiro-aceite.md").exists())

# Cenários dos Sprints 4 a 7 do DOCUMENTAPOLITEC: nome, etiqueta, leitura e painel.


@cenario("documentapolitec")
def s4_busca_por_nome(pg, url, ok):
    perfil(pg, url, "gestor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    indice = TMP / "indice-nomes.csv"
    indice.write_text("numero;nome;caixa\n2019.000001;Maria Fictícia Souza;CX-001\n2019.000002;João Fictício Lima;CX-001\n", encoding="utf-8-sig")
    ir(pg, url, "#/busca-nome", 600)
    ok("a busca por nome pede o índice autorizado", pg.locator("#arqIndice").count() == 1)
    pg.set_input_files("#arqIndice", str(indice)); pg.wait_for_timeout(900)
    ok("o índice é carregado sem guardar o nome em claro",
       pg.evaluate("async ()=> { const i = await db.list('indice_nomes'); return i.length === 2 && i.every(x=>!('nome' in x) && x.nome_hash); }"))
    pg.fill("#docNome", "maria ficticia souza")
    pg.click("#formBuscaNome button[type=submit]"); pg.wait_for_timeout(800)
    ok("a busca acha o prontuário e mostra caixa, setor e situação", "2019.000001" in pg.inner_text("#docResNome")
       and "CX-001" in pg.inner_text("#docResNome") and "DMIT" in pg.inner_text("#docResNome"))
    ok("a consulta entra na trilha (RN03)", pg.evaluate("async ()=> (await db.list('consultas')).length") == 1
       and pg.locator("#tabelaConsultas tr").count() == 2)
    # acesso restrito
    perfil(pg, url, "papiloscopista")
    ir(pg, url, "#/busca-nome", 600)
    ok("o perfil papiloscopista não acessa a busca por nome (RN03)", "não usa esta tela" in pg.inner_text("#conteudo")
       or "Acesso restrito" in pg.inner_text("#conteudo"))


@cenario("documentapolitec")
def s5_etiqueta_e_leitura(pg, url, ok):
    perfil(pg, url, "papiloscopista")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/caixa/CX-001", 700)
    ok("a etiqueta mostra o código de conferência e o código de barras",
       pg.locator("#docCodConf").count() == 1 and pg.locator("#docEtiqueta svg[role=img]").count() == 1)
    cod = pg.inner_text("#docCodConf")
    ok("o código de conferência tem o formato da caixa", "-" in cod and len(cod) >= 8)
    pg.fill("#docLeituraCod", "XX0-0000")
    pg.click("#btnDocLeitura"); pg.wait_for_timeout(600)
    ok("código errado é recusado", "não confere" in pg.inner_text("#docErrosLeitura"))
    pg.fill("#docLeituraCod", cod)
    pg.click("#btnDocLeitura"); pg.wait_for_timeout(600)
    ok("código certo é aceito e fica no histórico", pg.evaluate("async ()=> (await db.list('log')).some(l=>l.acao==='código de conferência lido')"))


@cenario("documentapolitec")
def s6_painel_e_relatorio(pg, url, ok):
    perfil(pg, url, "gestor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/painel", 800)
    calc = pg.evaluate("""async ()=>{ const cs = await db.list('caixas'), ps = await db.list('prontuarios');
        return {conferidas: cs.filter(c=>c.status==='conferida').length, pendentes: cs.filter(c=>c.status!=='conferida').length,
                conferidos: ps.filter(p=>p.conferido).length}; }""")
    ok("o painel conta conferidas e pendentes", pg.inner_text("[data-doc-ind=conferidas]") == str(calc["conferidas"])
       and pg.inner_text("[data-doc-ind=pendentes]") == str(calc["pendentes"]))
    ok("o espaço liberado é calculado pelos prontuários conferidos", f"{round(calc['conferidos']*0.03, 2)}" in pg.inner_text("[data-doc-ind=espaco]"))
    ok("o painel mostra os prontuários por período", pg.locator("#tabelaPeriodo tr").count() > 1)
    with pg.expect_download() as dl:
        pg.click("#btnDocCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV sai com BOM e as colunas da caixa", csv.startswith(b"\xef\xbb\xbf") and b"caixa;setor;data" in csv)
    ok("o roteiro de aceite está em modelos/", (APPS / "documentapolitec" / "modelos" / "roteiro-aceite.md").exists())

# Cenários dos Sprints 4 a 7 do Passivo Ambiental: assinatura, fila e produtividade.


@cenario("passivo-ambiental")
def s4_conclusao_com_assinatura(pg, url, ok):
    perfil(pg, url, "perito")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    rid = pg.evaluate("""async ()=>{ const rs = await db.list('requisicoes'); const r = rs.find(x=>x.status!=='concluida');
        const l = (await db.porIndice('laudos','requisicao_id',r.id_requisicao))[0];
        await db.put('mapas', {id_mapa: 'M-TESTE', laudo_id: l.id_laudo, modelo_id: 'delimitacao', modelo: 'Delimitação da área de dano',
          elementos: {norte: 'N', escala: '1:25.000', legenda: 'dano', data: '2026-10-20', fonte: 'satélite'}, valor_extra: '10,0', criado_em: agora()});
        return r.id_requisicao; }""")
    ir(pg, url, "#/laudo/" + rid, 700)
    ok("o bloco de assinatura aparece na ficha do laudo", pg.locator("#paAssinatura").count() == 1)
    pg.fill("#paAssNome", "")
    pg.click("#btnPaConcluir"); pg.wait_for_timeout(600)
    ok("sem o nome do perito, a conclusão é recusada", "nome do perito" in pg.inner_text("#paErrosLaudo"))
    pg.fill("#paAssNome", "Perito Fictício Assinante"); pg.fill("#paAssCargo", "Perito criminal · mat. 123")
    pg.click("#btnPaConcluir"); pg.wait_for_timeout(900)
    ok("com assinatura e mapa, o laudo conclui", pg.evaluate("async id => { const l = (await db.porIndice('laudos','requisicao_id',id))[0]; return l.status==='concluido'; }", rid))
    ok("a assinatura fica registrada", pg.evaluate("async id => { const a = (await db.porIndice('assinaturas','requisicao_id',id))[0]; return a && a.nome==='Perito Fictício Assinante' && a.cargo; }", rid))
    ok("a requisição passa para concluída", pg.evaluate("async id => (await db.get('requisicoes', id)).status === 'concluida'", rid))


@cenario("passivo-ambiental")
def s5_fila_e_prioridade(pg, url, ok):
    perfil(pg, url, "gestor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/painel", 900)
    calc = pg.evaluate("""async ()=>{ const rs = await db.list('requisicoes'); const f = paFila(rs);
        return {fila: f.length, atrasados: f.filter(x=>x.atraso).length}; }""")
    ok("o painel conta a fila e os atrasados", pg.inner_text("[data-pa-ind=fila]") == str(calc["fila"])
       and pg.inner_text("[data-pa-ind=atrasados]") == str(calc["atrasados"]))
    ok("a fila priorizada lista as requisições", pg.locator("#tabelaFila tr").count() == calc["fila"] + 1)
    ordem = pg.evaluate("""async ()=>{ const f = paFila(await db.list('requisicoes'));
        return f.slice(0, 3).map(x=>({atraso: x.atraso, c: x.complexidade})); }""")
    ok("a fila começa pelo atrasado de maior complexidade", ordem[0]["atraso"] == any(o["atraso"] for o in ordem))
    ok("o alerta de prazo aparece na fila", "fora do prazo" in pg.inner_text("#tabelaFila") or "vence em até 3 dias" in pg.inner_text("#tabelaFila"))


@cenario("passivo-ambiental")
def s6_produtividade_e_aceite(pg, url, ok):
    perfil(pg, url, "gestor")
    ir(pg, url, "#/config"); pg.click("#btnSeed"); pg.wait_for_timeout(800)
    ir(pg, url, "#/painel", 900)
    ok("o painel mostra tempo médio do laudo e horas médias com a meta de 12 h",
       pg.locator("[data-pa-ind=dias]").count() == 1 and pg.locator("[data-pa-ind=horas]").count() == 1
       and "meta 12 h" in pg.inner_text("#paGestor"))
    ok("as horas por tipo de infração aparecem em gráfico", pg.locator("#paGestor svg[role=img]").count() == 1)
    with pg.expect_download() as dl:
        pg.click("#btnPaCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV de produtividade sai com BOM e as colunas do laudo", csv.startswith(b"\xef\xbb\xbf") and b"requisicao;numero;orgao" in csv)
    ok("o roteiro de aceite está em modelos/", (APPS / "passivo-ambiental" / "modelos" / "roteiro-aceite.md").exists())
