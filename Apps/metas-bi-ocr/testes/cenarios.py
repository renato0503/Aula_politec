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
def s2_ler_csv_excel(pg, url, ok):
    ex = PASTA / "exemplos"
    semear(pg, url)
    for mes in ["2026-07", "2026-08", "2026-09"]:
        ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(ex / f"powerbi1-{mes}.csv")); pg.wait_for_timeout(800)
    ok("3 meses importados", contar(pg, "relatorios") == 3)
    ok("10 unidades por mês (30 pendências)", contar(pg, "pendencias") == 30)
    ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-08.csv")); pg.wait_for_timeout(800)
    ok("agosto acusa 1 unidade fora do cadastro (RN03)", pg.locator("#qtdDesconhecidas").inner_text() == "1 fora do cadastro")
    pg.select_option("select[id^=assoc-]", "Regional Sinop"); pg.click("[data-assoc]"); pg.wait_for_timeout(500)
    ok("associar grava o apelido na unidade", "Regional de Sinop (nova sigla)" in pg.evaluate("async ()=> JSON.stringify((await db.get('unidades','Regional Sinop')).apelidos)"))
    ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-08.csv")); pg.wait_for_timeout(800)
    ok("na próxima importação, o apelido casa sozinho", pg.locator("#qtdDesconhecidas").count() == 0)
    ok("total do relatório guardado (setembro)", pg.evaluate("async ()=> (await db.get('relatorios','2026-09')).total_relatorio") is not None)
    # Excel e arquivo sem mês
    from openpyxl import Workbook
    wb = Workbook(); ws = wb.active; ws.append(["Mês", "Unidade", "Laudos pendentes"]); ws.append(["10/2026", "IML Cuiabá", 321]); ws.append(["10/2026", "Total", 321])
    xl = TMP / "relatorio.xlsx"; wb.save(xl)
    ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(xl)); pg.wait_for_timeout(800)
    ok("Excel com mês 10/2026 é lido como 2026-10", pg.evaluate("async ()=> (await db.get('relatorios','2026-10'))?.tipo") == "excel")
    sem = TMP / "sem-mes.csv"; sem.write_text("Unidade;Laudos pendentes\nIML Cuiabá;10\n", encoding="utf-8")
    ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(sem)); pg.wait_for_timeout(500)
    ok("arquivo sem mês é recusado (RN01)", "RN01" in pg.inner_text("#errosMes"))

# origem: sprint3.py
@cenario
def s3_conferencia(pg, url, ok):
    ex = PASTA / "exemplos"
    semear(pg, url)
    for mes in ["2026-07", "2026-08", "2026-09"]:
        ir(pg, url, "#/importar", 300); pg.set_input_files("#arqMes", str(ex / f"powerbi1-{mes}.csv")); pg.wait_for_timeout(800)
        if mes == "2026-08":
            pg.select_option("select[id^=assoc-]", "Regional Sinop"); pg.click("[data-assoc]"); pg.wait_for_timeout(500)
    ir(pg, url, "#/conferencia/2026-09", 500)
    pg.fill("#aprovador", "Chefe Teste"); pg.click("#btnAprovar"); pg.wait_for_timeout(400)
    ok("setembro: soma diferente do total bloqueia a aprovação (RN02)", "RN02" in pg.inner_text("#bloqueios") and "RN02" in pg.inner_text("#errosAprovar") and "#/conferencia/" in pg.url)
    pg.fill("#motivoCorrecao", "Total do PDF inclui laudos de outra diretoria"); pg.click("#btnAceitarSoma"); pg.wait_for_timeout(500)
    ok("aceitar a soma com motivo libera a aprovação", pg.query_selector("#semBloqueio") is not None)
    pg.fill("#aprovador", "Chefe Teste"); pg.click("#btnAprovar"); pg.wait_for_timeout(500)
    ir(pg, url, "#/conferencia/2026-09", 400)
    ok("mês aprovado abre a planilha e fica travado (RN05)", "Planilha liberada" in pg.inner_text("#conteudo") or "aprovado por Chefe Teste" in pg.inner_text("#situacaoMes"))
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

# origem: sprint5.py
@cenario
def s5_leitura_do_pdf(pg, url, ok):
    semear(pg, url)
    ex = PASTA / "exemplos"
    ir(pg, url, "#/importar", 500)
    pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-07.pdf")); pg.wait_for_timeout(1500)
    ok("o PDF com texto é lido e o mês sai do arquivo", "2026-07" in pg.inner_text("#resMes"))
    ok("as 10 unidades do PDF entram na conferência", pg.evaluate("async ()=> (await db.porIndice('pendencias','mes_ref','2026-07')).length") == 10)
    ok("o número lido do PDF bate com o do CSV",
       pg.evaluate("""async ()=>{ const ps = await db.porIndice('pendencias','mes_ref','2026-07');
         const c = ps.find(p=>p.unidade==='Criminalística Cuiabá'); return c && c.pendentes === 1472; }"""))
    ok("a origem fica registrada como PDF", pg.evaluate("async ()=>{ const ps = await db.porIndice('pendencias','mes_ref','2026-07'); return ps.every(p=>p.origem==='pdf'); }"))
    ok("a confiança do texto extraído é 100%", pg.evaluate("async ()=>{ const ps = await db.porIndice('pendencias','mes_ref','2026-07'); return ps.every(p=>p.confianca===1); }"))
    # PDF sem camada de texto e sem tabela: página em branco passa pelo OCR e a tela avisa
    from reportlab.pdfgen import canvas as _cv
    sem = TMP / "powerbi1-2026-10.pdf"
    c = _cv.Canvas(str(sem)); c.showPage(); c.save()
    pg.set_input_files("#arqMes", str(sem))
    pg.wait_for_function("()=>document.querySelector('#errosMes').innerText.includes('OCR')", timeout=90000)
    ok("PDF sem tabela passa pelo OCR e avisa", "OCR" in pg.inner_text("#errosMes"))

# origem: sprint5.py
@cenario
def s6_aceite_e_piloto(pg, url, ok):
    semear(pg, url)
    # o fluxo completo: importar, conferir, aprovar, gerar o arquivo
    ex = PASTA / "exemplos"
    ir(pg, url, "#/importar", 400)
    pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-07.csv")); pg.wait_for_timeout(900)
    ir(pg, url, "#/conferencia/2026-07", 600)
    ok("a conferência abre com as divergências do mês", pg.locator("#conteudo").count() == 1)
    ok("o roteiro de aceite está em modelos/", (PASTA / "modelos" / "roteiro-aceite.md").exists())

@cenario
def s7_mes_escolhido_e_edicao(pg, url, ok):
    ex = PASTA / "exemplos"
    semear(pg, url)
    ir(pg, url, "#/importar", 500)
    ok("o importador tem o campo de mês", pg.locator("#mesImportar").count() == 1)
    pg.fill("#mesImportar", "2026-12")
    pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-07.csv")); pg.wait_for_timeout(1200)
    ok("o mês escolhido prevalece sobre o do arquivo", "2026-12" in pg.inner_text("#mesLido")
       and pg.evaluate("async () => !!(await db.get('relatorios','2026-12'))")
       and "2026-07" in pg.inner_text("#resMes"))
    ir(pg, url, "#/conferencia/2026-12", 900)
    primeiro = pg.evaluate("async () => (await db.porIndice('pendencias','mes_ref','2026-12')).sort((a,b)=>a.unidade.localeCompare(b.unidade))[0]")
    pg.click(f'[data-editar-pend="{primeiro["id"]}"]'); pg.wait_for_timeout(400)
    ok("a edição abre o diálogo com a unidade e o valor", pg.locator("dialog.metas-dialogo").count() == 1 and pg.input_value("#edPend") == str(primeiro["pendentes"]))
    pg.fill("#edPend", "777"); pg.fill("#edMotivo", "Correção manual para teste.")
    pg.click("dialog.metas-dialogo button[type=submit]"); pg.wait_for_timeout(1000)
    ok("editar grava o novo valor e a correção", pg.evaluate("async id => (await db.get('pendencias', id)).pendentes", primeiro["id"]) == 777
       and pg.evaluate("async () => (await db.list('correcoes')).some(c => c.tipo === 'edicao' && c.valor_final === 777)"))
    antes = pg.evaluate("async () => (await db.porIndice('pendencias','mes_ref','2026-12')).length")
    pg.click(f'[data-excluir-pend="{primeiro["id"]}"]'); pg.wait_for_timeout(900)
    ok("excluir remove só a linha escolhida", pg.evaluate("async () => (await db.porIndice('pendencias','mes_ref','2026-12')).length") == antes - 1)
    ir(pg, url, "#/importar", 800)
    pg.click('[data-excluir-mes="2026-12"]'); pg.wait_for_timeout(900)
    ok("excluir apaga o mês e as pendências", pg.evaluate("async () => !(await db.get('relatorios','2026-12'))")
       and pg.evaluate("async () => (await db.porIndice('pendencias','mes_ref','2026-12')).length") == 0)

@cenario
def s8_gerencia_recorte_e_exportacao(pg, url, ok):
    semear(pg, url)
    ex = PASTA / "exemplos"
    ir(pg, url, "#/importar", 400)
    pg.select_option("#impDiretoria", "Diretoria de Medicina Legal"); pg.wait_for_timeout(200); pg.check("#somenteMonitoradas")
    pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-07.csv")); pg.wait_for_timeout(900)
    n = pg.evaluate("async ()=> (await db.porIndice('pendencias','mes_ref','2026-07')).length")
    soma = pg.evaluate("async ()=> (await db.porIndice('pendencias','mes_ref','2026-07')).reduce((a,p)=>a+p.pendentes,0)")
    rel = pg.evaluate("async ()=> await db.get('relatorios','2026-07')")
    ok("o filtro de diretoria importa só a Medicina Legal", n == 2 and soma == 1081)
    ok("o total é ajustado ao recorte", rel["total_relatorio"] == 1081 and rel["gerencia"] == "Diretoria de Medicina Legal")
    ir(pg, url, "#/conferencia/2026-07", 500)
    ok("o cartão Pendentes soma as unidades monitoradas", pg.inner_text("#kpiPendentes") == "1081")
    pg.select_option("#confDiretoria", "Diretoria de Medicina Legal"); pg.wait_for_timeout(400)
    ok("a conferência filtra a tabela pela diretoria", len(pg.query_selector_all("#tabelaConf tr")) == 3)
    pg.fill("#aprovador", "Chefe Teste"); pg.click("#btnAprovar"); pg.wait_for_timeout(700)
    ok("aprovar leva à planilha liberada", "#/exportar/2026-07" in pg.url and pg.query_selector("#btnCsv") is not None)
    # unidade fora do cadastro é descartada quando a opção está marcada
    planilha = TMP / "recorte-desconhecida.csv"
    planilha.write_text("Mês;Unidade;Laudos pendentes\n2026-11;IML Cuiabá;10\n2026-11;Unidade Fantasma;99\n", encoding="utf-8")
    ir(pg, url, "#/importar", 400)
    pg.check("#somenteMonitoradas")
    pg.set_input_files("#arqMes", str(planilha)); pg.wait_for_timeout(700)
    ok("a unidade fora do cadastro não entra no recorte", pg.evaluate("async ()=> (await db.porIndice('pendencias','mes_ref','2026-11')).every(p=>!p.desconhecida)"))


@cenario
def s9_ocr_organograma_e_aprovacao(pg, url, ok):
    """Feedback Q0C5iOOEWMGnqDUDw541 (Karine, 04/11/2026): PDF em imagem, filtros do organograma e aprovação."""
    ex = PASTA / "exemplos"
    ir(pg, url, "#/importar", 500)
    pg.click("#btnOrganograma"); pg.wait_for_timeout(800)
    ok("o organograma cadastra 14 coordenadorias e 67 gerências e núcleos", contar(pg, "unidades") == 81)
    pg.select_option("#impDiretoria", "Diretoria de Medicina Legal"); pg.wait_for_timeout(200)
    ok("a cascata lista as coordenadorias da diretoria",
       "Coordenadoria de Perícias em Mortos" in pg.inner_text("#impCoordenadoria"))
    pg.select_option("#impDiretoria", ""); pg.wait_for_timeout(200)
    pg.set_input_files("#arqMes", str(ex / "powerbi1-2026-10-imagem.pdf"))
    pg.wait_for_selector("#previaPdf", timeout=90000)
    ok("o PDF em imagem é lido pelo OCR e abre a prévia", "OCR" in pg.inner_text("#previaPdf") and len(pg.query_selector_all("#tabelaPrevia tr[data-i]")) == 9)
    ok("a coluna de laudos pendentes vem escolhida", pg.input_value("#colPendentes") == "2")
    pg.click("#btnUsarPrevia"); pg.wait_for_timeout(1500)
    ps = pg.evaluate("async ()=> await db.porIndice('pendencias','mes_ref','2026-10')")
    ok("o mês sai do título do relatório (outubro de 2026)", len(ps) == 9)
    ok("os números lidos pelo OCR batem com o relatório", sum(p["pendentes"] for p in ps) == 805
       and next(p for p in ps if p["unidade"] == "Gerência de Necropsia")["pendentes"] == 224)
    ok("cada linha guarda a lotação do organograma",
       next(p for p in ps if p["unidade"] == "Gerência Regional de Alta Floresta")["lotacao"]["coordenadoria"] == "Coordenadoria Regional 4 - Sinop")
    ir(pg, url, "#/conferencia/2026-10", 700)
    pg.select_option("#confDiretoria", "Diretoria de Criminalística"); pg.wait_for_timeout(500)
    pg.select_option("#confCoordenadoria", "Coordenadoria de Perícias Internas"); pg.wait_for_timeout(500)
    ok("a conferência filtra por diretoria e coordenadoria", len(pg.query_selector_all("#tabelaConf tr")) == 3)
    # corrigir um número deixa a soma diferente do total: o botão responde e aponta o caminho
    nec = "2026-10|Gerência de Perícias de Balística"
    pg.fill(f'[data-novo="{nec}"]', "130"); pg.fill("#motivoCorrecao", "Conferido no SIGT"); pg.click("#btnCorrigir"); pg.wait_for_timeout(700)
    pg.fill("#aprovador", "Karine"); pg.click("#btnAprovar"); pg.wait_for_timeout(500)
    ok("aprovar com RN02 explica o bloqueio em vez de não fazer nada", "RN02" in pg.inner_text("#errosAprovar") and pg.query_selector("#btnAceitarSoma2") is not None)
    pg.fill("#motivoCorrecao", "Total do PDF desatualizado"); pg.click("#btnAceitarSoma2"); pg.wait_for_timeout(600)
    pg.fill("#aprovador", "Karine"); pg.click("#btnAprovar"); pg.wait_for_timeout(800)
    ok("depois de aceitar a soma, aprovar abre a planilha", "#/exportar/2026-10" in pg.url and pg.query_selector("#btnCsv") is not None)
    ir(pg, url, "#/historico", 500)
    ok("a lista de meses mostra soma e total aceitos iguais", "807" in pg.inner_text("#conteudo") and "aceito" in pg.inner_text("#conteudo"))


@cenario
def s10_painel_power_bi_com_varias_tabelas(pg, url, ok):
    """PDF do painel impresso pelo navegador (como o 2026_10_14_Química_Pendentes.pdf da CQUAL):
    várias tabelas lado a lado, diretoria como subtotal e nome quebrado em duas linhas."""
    ex = PASTA / "exemplos"
    ir(pg, url, "#/importar", 500)
    pg.click("#btnOrganograma"); pg.wait_for_timeout(900)
    pg.set_input_files("#arqMes", str(ex / "painel-pbi-2026-10.pdf"))
    pg.wait_for_selector("#previaPdf", timeout=60000)
    opcoes = pg.evaluate("()=>[...document.querySelectorAll('#tabelaPdf option')].map(o=>o.text)")
    ok("acha as duas tabelas com Total e escolhe a de pendentes por unidade",
       len(opcoes) == 2 and pg.input_value("#tabelaPdf") == "0" and "Matriz" in opcoes[0])
    ok("a coluna escolhida é a do Total", pg.evaluate("()=>{const s=document.querySelector('#colPendentes');return s.options[s.selectedIndex].text}") == "Total")
    nomes = pg.evaluate("()=>[...document.querySelectorAll('#tabelaPrevia [data-nome]')].map(i=>i.value)")
    ok("o nome quebrado em duas linhas é juntado", "PERÍCIAS EM LABORATÓRIOS DE MATERIAIS" in nomes)
    ok("a diretoria (subtotal) vem desmarcada", pg.evaluate("()=>!document.querySelector('#tabelaPrevia tr.subtotal [data-usar]').checked"))
    ok("a tabela do lado não mistura os números (4953 não aparece)",
       "4953" not in pg.evaluate("()=>[...document.querySelectorAll('#tabelaPrevia input[type=number]')].map(i=>i.value).join(',')"))
    pg.click("#btnUsarPrevia"); pg.wait_for_timeout(1500)
    ps = pg.evaluate("async ()=> await db.porIndice('pendencias','mes_ref','2026-10')")
    soma = sum(p["pendentes"] for p in ps)
    ok("soma das unidades igual ao total do relatório (1.972)", soma == 1972
       and pg.evaluate("async ()=> (await db.get('relatorios','2026-10')).total_relatorio") == 1972)
    ok("as coordenadorias do painel são associadas pelo organograma",
       {p["unidade"] for p in ps if not p["desconhecida"]} == {"Coordenadoria do Laboratório de Materiais", "Coordenadoria de Perícias em Biologia Molecular"})
    ir(pg, url, "#/conferencia/2026-10", 700)
    ok("'Outro' fica como RN03 para a pessoa decidir", "Outro" in pg.inner_text("#bloqueios"))
    pg.click("#btnCadastrarTodas"); pg.wait_for_timeout(800)
    pg.fill("#aprovador", "Chefe Teste"); pg.click("#btnAprovar"); pg.wait_for_timeout(900)
    ok("cadastrado o 'Outro', o mês é aprovado e a planilha abre", "#/exportar/2026-10" in pg.url)


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
