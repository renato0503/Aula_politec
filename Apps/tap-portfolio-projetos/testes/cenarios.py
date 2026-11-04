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
def s2_tap_guiado(pg, url, ok):
    perfil(pg, url, "demandante")
    pg.evaluate("async ()=>{ for (const d of dadosEmbutidos('seed').documentos) await db.put('documentos', d); }")
    ir(pg, url, "#/tap/novo", 500)
    ok("TAP vazio mostra as pendências", int(pg.inner_text("#qtdPend")) >= 9)
    pg.fill("#tap-titulo", "Projeto de teste"); pg.fill("#tap-unidade", "Laboratório Forense"); pg.fill("#tap-responsavel", "Responsável Teste")
    pg.fill("#tap-contato", "teste@politec.mt.gov.br"); pg.wait_for_timeout(400)
    pg.reload(); pg.wait_for_timeout(600)
    ok("rascunho salvo: o título volta depois de recarregar", pg.input_value("#tap-titulo") == "Projeto de teste")
    pg.click("[data-etapa=objetivo]"); pg.wait_for_timeout(300)
    pg.fill("#tap-objetivo", "o" * 120); pg.fill("#tap-justificativa", "j" * 150); pg.wait_for_timeout(300)
    ok("justificativa curta segue pendente (RN02)", "Justificativa: 150 de 200" in pg.inner_text("#painelPendencias"))
    pg.fill("#tap-justificativa", "j" * 210); pg.wait_for_timeout(300)
    pg.click("[data-etapa=alinhamento]"); pg.wait_for_timeout(300); pg.select_option("#tap-objetivo_estrategico", index=1); pg.wait_for_timeout(200)
    pg.click("[data-etapa=custo]"); pg.wait_for_timeout(300); pg.fill("#tap-valor_estimado", "150.000,00"); pg.fill("#tap-prazo_meses", "12"); pg.wait_for_timeout(300)
    pg.click("[data-etapa=anexos]"); pg.wait_for_timeout(300)
    ok("faltam os 3 anexos obrigatórios", pg.inner_text("#qtdPend") == "3")
    pg.set_input_files("[data-anexo=estudo_tecnico]", {"name": "grande.pdf", "mimeType": "application/pdf", "buffer": b"0" * (11 * 1024 * 1024)}); pg.wait_for_timeout(400)
    ok("anexo de 11 MB é recusado (RN04)", contar(pg, "anexos") == 0)
    for t in ("pesquisa_precos", "estudo_tecnico"):
        pg.set_input_files(f"[data-anexo={t}]", {"name": f"{t}.pdf", "mimeType": "application/pdf", "buffer": b"%PDF-1.4"}); pg.wait_for_timeout(500)
    ok("2 anexos guardados", contar(pg, "anexos") == 2)
    pg.fill("#aus-anuencia_chefia", "A chefia assina no SEI depois da triagem."); pg.wait_for_timeout(400)
    ok("ausência justificada fecha a última pendência (RN03)", pg.inner_text("#qtdPend") == "0")
    pg.click("#btnConcluir"); pg.wait_for_timeout(500)
    ok("TAP concluído fica pronto para envio", pg.evaluate("async ()=> (await db.list('propostas')).filter(p=>p.status==='pronto para envio').length") == 1)
    ok("valor estimado gravado em reais sem erro", pg.evaluate("async ()=> (await db.list('propostas')).find(p=>p.status==='pronto para envio').valor_estimado") == 150000)

# origem: sprint3.py
@cenario
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

# origem: sprint4.py
@cenario
def s4_proposta_parecer_e_decisao(pg, url, ok):
    perfil(pg, url, "equipe")
    semear(pg, url)
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

# origem: sprint4.py
@cenario
def s5_portfolio_e_prioridade(pg, url, ok):
    perfil(pg, url, "equipe")
    semear(pg, url)
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

# origem: sprint4.py
@cenario
def s6_indicadores_e_aceite(pg, url, ok):
    perfil(pg, url, "equipe")
    semear(pg, url)
    ir(pg, url, "#/indicadores", 600)
    calc = pg.evaluate("""async ()=>{ const ps = await db.list('propostas'), pri = await db.list('portfolio');
        return {total: ps.length, aprovadas: ps.filter(p=>p.status==='aprovada').length,
                semPrioridade: ps.filter(p=>p.status==='aprovada' && !pri.some(x=>x.proposta_id===p.id)).length}; }""")
    ok("os indicadores contam propostas, aprovadas e sem prioridade",
       pg.inner_text("[data-tap-ind=total]") == str(calc["total"]) and pg.inner_text("[data-tap-ind=aprovadas]") == str(calc["aprovadas"])
       and pg.inner_text("[data-tap-ind=sem-prioridade]") == str(calc["semPrioridade"]))
    ok("o indicador traz o valor do portfólio aprovado", "R$" in pg.inner_text("[data-tap-ind=valor]"))
    ok("as propostas por situação são agrupadas", pg.locator("#tabelaStatus tr").count() > 1)
    ok("o roteiro de aceite está em modelos/", (PASTA / "modelos" / "roteiro-aceite.md").exists())

@cenario
def s7_dashboard_orcamentario(pg, url, ok):
    perfil(pg, url, "equipe")
    semear(pg, url)
    ir(pg, url, "#/dashboard", 900)
    ok("o dashboard abre com os KPIs", pg.locator("[data-dash=empenhado]").count() == 1 and pg.locator("[data-dash=liquidado]").count() == 1
       and pg.locator("[data-dash=saldo]").count() == 1 and pg.locator("[data-dash=percentual]").count() == 1)
    ok("a base de exemplo tem 15 lançamentos", contar(pg, "orcamentos") == 15)
    ok("o resumo por ano e eixo lista os grupos", pg.locator("#tabelaOrcResumo tr").count() == 16)
    pg.select_option("#dashAno", "2026"); pg.wait_for_timeout(700)
    esperado = pg.evaluate("async ()=> tapReal(tapResumoOrc(await db.list('orcamentos'), {ano: '2026'}).empenhado)")
    ok("o filtro de ano recalcula o empenhado", pg.inner_text("[data-dash=empenhado]") == esperado)
    pg.fill("#orcAno", "2027"); pg.select_option("#orcEixo", "Infraestrutura"); pg.fill("#orcProjeto", "Projeto de teste")
    pg.fill("#orcEmpenhado", "1.000,00"); pg.fill("#orcLiquidado", "400,00")
    pg.click("#formOrc button[type=submit]"); pg.wait_for_timeout(900)
    ok("adicionar um lançamento grava no banco", contar(pg, "orcamentos") == 16)
    pg.select_option("#dashAno", ""); pg.wait_for_timeout(700)
    alvo = pg.evaluate("async ()=> (await db.list('orcamentos')).find(r=>r.projeto==='Projeto de teste').id")
    pg.click(f'[data-orc-editar="{alvo}"]'); pg.wait_for_timeout(700)
    pg.fill("#orcLiquidado", "900,00"); pg.click("#formOrc button[type=submit]"); pg.wait_for_timeout(900)
    ok("editar atualiza o liquidado", pg.evaluate("async id => (await db.get('orcamentos', id)).liquidado", alvo) == 900)
    pg.click(f'[data-orc-excluir="{alvo}"]'); pg.wait_for_timeout(900)
    ok("excluir remove o lançamento", contar(pg, "orcamentos") == 15)
    csv = TMP / "orcamento.csv"
    csv.write_text("ano;eixo;projeto;empenhado;liquidado\n2028;Infraestrutura;Importado;2.000,00;1.500,00\n", encoding="utf-8")
    pg.set_input_files("#arqOrc", str(csv)); pg.wait_for_timeout(1600)
    ok("importar o .csv atualiza a base", contar(pg, "orcamentos") == 16
       and pg.evaluate("async ()=> !!(await db.list('orcamentos')).find(r=>r.projeto==='Importado')"))

@cenario
def s8_fluxo_pendencia_e_avisos(pg, url, ok):
    perfil(pg, url, "equipe")
    semear(pg, url)
    ir(pg, url, "#/proposta/TAP-2026-003", 500)
    ok("a proposta devolvida mostra o botão de sanar", pg.query_selector("#btnTapSanar") is not None)
    pg.click("#btnTapSanar"); pg.wait_for_timeout(700)
    ok("sanar volta o TAP para análise", pg.evaluate("async ()=> (await db.get('propostas','TAP-2026-003')).status") == "em análise")
    avisos = pg.evaluate("async ()=> (await db.porIndice('avisos','proposta_id','TAP-2026-003')).map(a=>a.para)")
    ok("a equipe e a autoridade entram na fila de avisos", "equipe de projetos" in avisos and "autoridade" in avisos)
    # pendência em atraso aparece no painel e gera cobrança
    pg.evaluate("""async ()=>{ const x = (await db.porIndice('pendencias','proposta_id','TAP-2026-007')).find(p=>!p.resolvida_em);
      await db.put('pendencias', {...x, prazo_limite: '2026-10-01'}); }""")
    ir(pg, url, "#/triagem", 1000)
    pg.wait_for_selector("#tapPainelAvisos", timeout=10000)
    ok("a triagem lista a pendência fora do prazo", "em atraso" in pg.inner_text("#tapPainelAvisos"))
    pg.click("[data-tap-cobrar]"); pg.wait_for_timeout(600)
    ok("a cobrança entra na fila local", pg.evaluate("async ()=> (await db.list('avisos')).some(a=>a.texto.includes('venceu'))"))
    # objetivos configuráveis
    ir(pg, url, "#/config", 500)
    pg.fill("#tapObjetivos", "Objetivo oficial A\nObjetivo oficial B")
    pg.click("#btnTapObjetivos"); pg.wait_for_timeout(500)
    ir(pg, url, "#/tap/novo", 700)
    pg.click("[data-etapa='alinhamento']"); pg.wait_for_timeout(400)
    opcoes = pg.evaluate("()=>[...document.querySelectorAll('#tap-objetivo_estrategico option')].map(o=>o.value)")
    ok("os objetivos configurados aparecem no novo TAP", "Objetivo oficial A" in opcoes and "Objetivo oficial B" in opcoes)


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
