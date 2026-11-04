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
def s2_importar_planilha(pg, url, ok):
    ex = PASTA / "exemplos"
    perfil(pg, url, "cqual")
    pg.evaluate("async ()=>{ for (const s of dadosEmbutidos('seed').setores) await db.put('setores', s); }")
    def importar(arq):
        ir(pg, url, "#/importar", 300); pg.set_input_files("#arqRnc", str(arq)); pg.wait_for_timeout(400)
        pg.click("#btnImportarRnc"); pg.wait_for_timeout(1200)
    importar(ex / "respostas-forms-ficticio.csv")
    ok("as 20 RNCs do Forms viram 20 novas", pg.inner_text("#qtdNovas") == "20 novas" and contar(pg, "rncs") == 20)
    ok("cada RNC abre a etapa de validação com prazo de 5 dias", pg.evaluate("async ()=>{ const e = (await db.list('etapas'))[0]; return (new Date(e.prazo) - new Date(e.inicio)) / 86400000 === 5; }"))
    ok("setores casados pela sigla", pg.evaluate("async ()=> (await db.list('rncs')).every(r=>r.setor_relator.length <= 4)"))
    importar(ex / "respostas-forms-ficticio.csv")
    ok("importar de novo não duplica", pg.inner_text("#qtdExistentes") == "20 já existentes" and contar(pg, "rncs") == 20)
    # planilha com nome do servidor e sem a coluna Número
    linhas = (ex / "respostas-forms-ficticio.csv").read_text(encoding="utf-8-sig").splitlines()
    cab = linhas[0].split(",")
    nova = [",".join(cab[:-1] + ["Nome do servidor"])] + [",".join(l.split(",")[:-1] + ["Fulano de Tal"]).replace("2026,", "2026,").replace("/09/2026", "/10/2026", 1) for l in linhas[1:3]]
    arq = TMP / "forms-com-nome.csv"; arq.write_text("\n".join(nova), encoding="utf-8")
    importar(arq)
    ok("coluna Nome do servidor é descartada (RN07)", "Nome do servidor" in pg.inner_text("#mapaRnc") and "descartadas" in pg.inner_text("#mapaRnc"))
    ok("nenhum nome de servidor gravado", "Fulano" not in pg.evaluate("async ()=> JSON.stringify(await db.list('rncs'))"))
    ok("sem coluna Número, o app numera DLF/2026-021 em diante", pg.evaluate("async ()=> !!(await db.get('rncs', 'DLF/2026-021'))"))

# origem: sprint3.py
@cenario
def s3_etapas_e_prazos(pg, url, ok):
    import datetime as dt
    from urllib.parse import quote
    perfil(pg, url, "cqual")
    semear(pg, url)
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

# origem: sprint4.py
@cenario
def s4_arquivo_do_setor(pg, url, ok):
    perfil(pg, url, "cqual")
    semear(pg, url)
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

# origem: sprint4.py
@cenario
def s5_plano_avaliacao_e_painel(pg, url, ok):
    perfil(pg, url, "setor")
    semear(pg, url)
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

# origem: sprint4.py
@cenario
def s6_aceite_e_piloto(pg, url, ok):
    perfil(pg, url, "cqual")
    semear(pg, url)
    # o fluxo completo: importar a planilha do Forms, ver a RNC, exportar para o setor
    ex = PASTA / "exemplos"
    ir(pg, url, "#/importar", 500)
    pg.set_input_files("#arqRnc", str(ex / "respostas-forms-ficticio.csv")); pg.wait_for_timeout(900)
    ok("a planilha do Forms é lida e as colunas são associadas", pg.locator("#mapaRnc").count() == 1
       and pg.locator("#btnImportarRnc").count() == 1)
    ir(pg, url, "#/exportar", 500)
    ok("a tela de arquivo do setor abre", pg.locator("#btnExportarSetor").count() == 1)
    ok("o roteiro de aceite está em modelos/", (PASTA / "modelos" / "roteiro-aceite.md").exists())

@cenario
def s7_planilha_oficial_xlsx(pg, url, ok):
    perfil(pg, url, "cqual")
    arq = PASTA / "Registro de Não Conformidade Oficial 1.xlsx"
    ok("a planilha oficial está na pasta do app", arq.exists())
    ir(pg, url, "#/importar", 700)
    pg.set_input_files("#arqRnc", str(arq)); pg.wait_for_timeout(2200)
    ok("o .xlsx é lido e as colunas oficiais aparecem", "Carimbo de data/hora" in pg.inner_text("#mapaRnc")
       and pg.locator("#btnImportarRnc").count() == 1)
    ok("a descrição é traduzida para a coluna certa e e-mail/nome ficam de fora",
       pg.evaluate("() => document.querySelector('#rmap-descricao').value") == "13"
       and "Nome Completo" in pg.inner_text("#mapaRnc") and "descartadas (RN07)" in pg.inner_text("#mapaRnc"))
    pg.click("#btnImportarRnc"); pg.wait_for_timeout(2500)
    ok("as 19 linhas com conteúdo viram RNCs", pg.inner_text("#qtdNovas") == "19 novas")
    ok("os metadados da planilha são guardados", pg.evaluate("""async ()=>{
        const r = (await db.list('rncs')).find(x=>x.numero==='DLF/2026-008');
        return r && r.data_ocorrido === '2026-05-31' && r.processo.includes('ATENA') && r.status_trello === 'CONCLUÍDO'; }"""))
    ok("a categoria vira a sigla oficial (ADM)", pg.evaluate("async () => (await db.get('rncs','DLF/2026-008')).categoria_sigla") == "ADM")
    ir(pg, url, "#/rnc/DLF%2F2026-008", 900)
    ok("a ficha da RNC mostra os dados da planilha oficial", pg.locator("#rncPlanilha").count() == 1
       and "Dados da planilha oficial" in pg.inner_text("#conteudo"))

@cenario
def s8_google_planilhas(pg, url, ok):
    perfil(pg, url, "cqual")
    csv = (PASTA / "exemplos" / "respostas-forms-ficticio.csv").read_text(encoding="utf-8")
    pedidos = []
    def rota(route):
        pedidos.append(route.request.url)
        route.fulfill(status=200, headers={"access-control-allow-origin": "*", "content-type": "text/csv; charset=utf-8"}, body=csv)
    pg.route("https://docs.google.com/**", rota)
    ir(pg, url, "#/importar", 700)
    pg.fill("#rncPlanilha", "https://docs.google.com/spreadsheets/d/10-Oqfv6x9GY4VDz3ZfVKxmipz0ev0fyyNzThi_A4DSI/edit")
    pg.click("#btnRncGoogle"); pg.wait_for_timeout(1500)
    ok("a sincronização busca o CSV público da planilha", pedidos and "/gviz/tq?tqx=out:csv" in pedidos[0])
    ok("as linhas lidas do Google entram no mapa", "20 linha(s) lidas" in pg.inner_text("#rncGoogleStatus") and pg.locator("#btnImportarRnc").count() == 1)
    pg.click("#btnImportarRnc"); pg.wait_for_timeout(2000)
    ok("a importação do Google cria as RNCs", pg.inner_text("#qtdNovas") == "20 novas" and contar(pg, "rncs") == 20)
    ok("o link da planilha fica guardado", "docs.google.com/spreadsheets" in (pg.evaluate("async () => await db.meta('rnc_planilha_url')") or ""))

@cenario
def s9_documento_oficial(pg, url, ok):
    perfil(pg, url, "cqual")
    pg.evaluate("""async ()=>{ await db.put('rncs', {numero: 'DLF/2026-901', aberta_em: '2026-10-01', setor_relator: 'CQUAL',
        setor_notificado: 'Laboratório Forense', categoria: 'Administração', gravidade: 'Média', descricao: 'Descrição fictícia da ocorrência.',
        etapa: 'validação', situacao: 'aberta'});
        await db.put('etapas', {id: 'DLF/2026-901#0', rnc: 'DLF/2026-901', etapa: 'validação', inicio: '2026-10-01', fim: null, prazo: '2026-10-06'}); }""")
    ir(pg, url, "#/rnc/DLF%2F2026-901/documento", 900)
    ok("o documento oficial da RNC abre", pg.locator("#docRnc").count() == 1 and "REGISTRO DE NÃO CONFORMIDADE" in pg.inner_text("#docRnc"))
    ok("a categoria aparece pela sigla e pelo nome", "ADM" in pg.inner_text("#docRnc") and "Administração" in pg.inner_text("#docRnc"))
    ok("o documento tem o botão de imprimir e a assinatura", pg.locator("#btnImprimirDoc").count() == 1 and "Relator / CQUAL" in pg.inner_text("#docRnc"))
    ok("RN03: o complemento conta em dias úteis", pg.evaluate("() => somarDiasUteisRnc('2026-10-02', 5)") == "2026-10-09")

@cenario
def s10_relacao_e_responsavel(pg, url, ok):
    perfil(pg, url, "cqual")
    semear(pg, url)
    ir(pg, url, "#/exportar", 600)
    setor = pg.evaluate("async ()=> (await db.list('rncs'))[0].setor_notificado")
    n = pg.evaluate("async s => (await db.list('rncs')).filter(r=>r.setor_notificado===s).length", setor)
    pg.select_option("#expSetor", setor)
    pg.click("#btnRelacaoSetor"); pg.wait_for_timeout(600)
    ok("a relação do setor é gerada para impressão", pg.locator("#relacaoSetor:not([hidden])").count() == 1
       and "Relação de RNCs" in pg.inner_text("#relacaoSetor") and setor in pg.inner_text("#relacaoSetor"))
    ok("a relação lista as RNCs do setor e mantém o botão de imprimir", pg.locator("#relacaoSetor tbody tr").count() == n
       and pg.locator("#btnImprimirRelacao:not([hidden])").count() == 1)

    perfil(pg, url, "setor")
    ir(pg, url, "#/minhas", 600)
    pg.select_option("#rncMeuSetor", setor); pg.click("#btnSalvarSetor"); pg.wait_for_timeout(600)
    pg.locator("[data-plano]").first.click(); pg.wait_for_timeout(400)
    pg.fill("#plResp", "Fulano de Tal (setor)"); pg.fill("#plAcoes", "Treinamento da equipe e revisão do procedimento interno.")
    pg.click("#formPlano button[type=submit]"); pg.wait_for_timeout(600)
    ok("o plano registra quem respondeu", pg.evaluate("async ()=> (await db.list('planos'))[0].responsavel") == "Fulano de Tal (setor)")
    ok("a tabela do setor mostra o responsável", "Fulano de Tal (setor)" in pg.inner_text("#tabelaMinhasRnc"))
    pg.locator("[data-aval]").first.click(); pg.wait_for_timeout(400)
    pg.fill("#avResp", "Beltrano (setor)"); pg.select_option("#avEficaz", "sim"); pg.fill("#avObs", "A ação resolveu a causa.")
    pg.click("#formAval button[type=submit]"); pg.wait_for_timeout(600)
    ok("a avaliação registra quem respondeu", pg.evaluate("async ()=> (await db.list('avaliacoes'))[0].responsavel") == "Beltrano (setor)")


@cenario
def s11_numero_da_planilha(pg, url, ok):
    """Feedback da Sabrina (04/11): o app criava um código em vez de usar o ID ocorrência da planilha."""
    perfil(pg, url, "cqual")
    semear(pg, url)
    arq = PASTA / "Registro de Não Conformidade Oficial 1.xlsx"
    ir(pg, url, "#/importar", 700)
    pg.set_input_files("#arqRnc", str(arq)); pg.wait_for_timeout(2200)
    pg.click("#btnImportarRnc"); pg.wait_for_timeout(3000)
    ok("com os fictícios carregados, as 19 linhas da planilha entram como novas", pg.inner_text("#qtdNovas") == "19 novas")
    ok("DLF/2026-008 traz a descrição real, e não a fictícia", pg.evaluate("""async ()=>{
        const r = await db.get('rncs', 'DLF/2026-008'); return !!r.chave_importacao && !/fictícia/.test(r.descricao) && r.data_ocorrido === '2026-05-31'; }"""))
    ok("as etapas do fictício substituído saem junto", pg.evaluate("async ()=> (await db.list('etapas')).filter(e=>e.rnc==='DLF/2026-008').length") == 1)
    # linha importada antes com código gerado pelo app; a planilha corrigida traz o ID certo
    pg.evaluate("async ()=>{ for (const n of ['rncs','etapas','planos','avaliacoes']) await db.limpar(n); }")
    cab = "Carimbo de data/hora,Setor relator,Setor notificado,Categoria,Descrição da ocorrência,Gravidade,ID ocorrência"
    errado = TMP / "rnc-id-errado.csv"; certo = TMP / "rnc-id-certo.csv"
    errado.write_text(cab + "\n05/10/2026 09:00:00,CQUAL,LGF,Administração,Teste de número,leve,\n", encoding="utf-8")
    certo.write_text(cab + "\n05/10/2026 09:00:00,CQUAL,LGF,Administração,Teste de número,leve, dlf / 2026-050 \n", encoding="utf-8")
    for a in (errado, certo):
        ir(pg, url, "#/importar", 400); pg.set_input_files("#arqRnc", str(a)); pg.wait_for_timeout(500)
        pg.click("#btnImportarRnc"); pg.wait_for_timeout(1200)
    ok("a RNC com código gerado passa a usar o ID da planilha", pg.evaluate("""async ()=>{
        const l = await db.list('rncs'); return l.length === 1 && l[0].numero === 'DLF/2026-050'
          && (await db.list('etapas')).every(e=>e.rnc === 'DLF/2026-050'); }"""))


@cenario
def s12_setores_da_planilha(pg, url, ok):
    """Feedback da Sabrina (04/11): setores por extenso, grafias diferentes e nome de pessoa no setor notificado."""
    perfil(pg, url, "cqual")
    arq = PASTA / "Registro de Não Conformidade Oficial 1.xlsx"
    ir(pg, url, "#/importar", 700)
    pg.set_input_files("#arqRnc", str(arq)); pg.wait_for_timeout(2200)
    pg.click("#btnImportarRnc"); pg.wait_for_timeout(3000)
    conta = pg.evaluate("""async ()=>{ const c = {}; (await db.list('rncs')).forEach(r=>c[r.setor_notificado]=(c[r.setor_notificado]||0)+1); return c; }""")
    ok("as 3 grafias da GML de Rondonópolis viram GMLROO (4 RNCs)", conta.get("GMLROO") == 4)
    ok("as 3 grafias da necropsia de Cuiabá viram GNEC", conta.get("GNEC") == 3)
    ok("o relator por extenso vira CPBM", pg.evaluate("async ()=> (await db.get('rncs','DLF/2026-008')).setor_relator") == "CPBM")
    ok("texto sem unidade (aaaa, Fulana e ciclano) fica como setor a definir", conta.get("ADEF", 0) >= 6)
    tudo = pg.evaluate("async ()=> JSON.stringify({r: await db.list('rncs'), s: await db.list('setores')})")
    ok("nenhum nome de pessoa da coluna de envolvidos entra no app (RN07)", not any(x in tudo for x in ("RENATA", "Neimar", "Fulana")))
    ok("os setores da planilha entram no cadastro com o nome", pg.evaluate("async ()=> (await db.get('setores','GMLROO'))?.nome") == "Gerência de Medicina Legal de Rondonópolis")
    ir(pg, url, "#/rnc/DLF%2F2026-008", 900)
    ok("a ficha mostra a sigla e o nome do setor", "CPBM (Coordenadoria de Perícias em Biologia Molecular)" in pg.inner_text("#conteudo"))
    ir(pg, url, "#/importar", 700)
    pg.set_input_files("#arqRnc", str(arq)); pg.wait_for_timeout(2200)
    pg.click("#btnImportarRnc"); pg.wait_for_timeout(3000)
    ok("reimportar não duplica nem cria setor de novo", pg.inner_text("#qtdNovas") == "0 novas"
       and "setores cadastrados" not in pg.inner_text("#relRnc"))


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
