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

# origem: sprint2.py
@cenario
def s2_requisicao_e_cabecalho(pg, url, ok):
    perfil(pg, url, "perito")
    semear(pg, url)
    atras = pg.evaluate("async ()=> (await db.list('requisicoes')).filter(r=>r.status!=='concluida' && r.prazo_dias < Math.round((Date.now()-new Date(r.data_requisicao))/86400000)).length")
    ir(pg, url, "#/painel", 400)
    ok("o painel conta as requisições fora do prazo", pg.inner_text("[data-atrasadas]") == str(atras) and atras > 0)
    ir(pg, url, "#/requisicao/nova", 400)
    pg.fill("#paNumero", "2026.999999-9"); pg.fill("#paOrgao", "Delegacia de Teste"); pg.fill("#paTipo", "desmatamento"); pg.fill("#paLocal", "Fazenda Teste")
    pg.click("#formPaNova button[type=submit]"); pg.wait_for_timeout(600)
    ok("a requisição abre o laudo com o cabeçalho preenchido (RN01)", "#/laudo/REQ-0013" in pg.url and "2026.999999-9" in pg.inner_text("#tabelaCabecalho")
       and "Delegacia de Teste" in pg.inner_text("#tabelaCabecalho") and "Fazenda Teste" in pg.inner_text("#tabelaCabecalho"))
    ok("a requisição entra na base com a situação laudo", pg.evaluate("async ()=> (await db.get('requisicoes','REQ-0013')).status") == "laudo")
    pg.click("#btnPaConcluir"); pg.wait_for_timeout(400)
    ok("concluir sem mapa é recusado (RN03)", "mapa" in pg.inner_text("#paErrosLaudo") and pg.evaluate("async ()=> (await db.get('laudos','L-REQ-0013')).status") == "rascunho")
    pg.fill("#paHoras", "6"); pg.click("#formPaLaudo button[type=submit]"); pg.wait_for_timeout(500)
    ok("o rascunho guarda as horas trabalhadas", pg.evaluate("async ()=> (await db.get('laudos','L-REQ-0013')).horas_trabalhadas") == 6)
    ir(pg, url, "#/requisicao/nova", 300)
    pg.fill("#paNumero", "2026.999999-9"); pg.fill("#paOrgao", "X"); pg.fill("#paTipo", "Y"); pg.fill("#paLocal", "Z")
    pg.click("#formPaNova button[type=submit]"); pg.wait_for_timeout(400)
    ok("requisição repetida é recusada", "já está cadastrada" in pg.inner_text("#paErros"))

# origem: sprint3.py
@cenario
def s3_mapa_e_pdf(pg, url, ok):
    perfil(pg, url, "perito")
    semear(pg, url)
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
    ok("mapa sem elementos obrigatórios é recusado (RN02)", "RN02" in pg.inner_text("#paErrosMapa") and contar(pg, "mapas") == 6)
    for tipo in ("localizacao", "antes", "depois"):
        ir(pg, url, "#/mapa/REQ-0013", 300)
        pg.select_option("#paTipoMapa", tipo)
        pg.select_option("#paModelo", "localizacao")
        pg.fill("#paExtra", "12,5")
        for campo_id in ("paEl_norte", "paEl_escala", "paEl_legenda", "paEl_data", "paEl_fonte"):
            pg.fill("#" + campo_id, "valor de teste")
        pg.click("#formPaMapa button[type=submit]"); pg.wait_for_timeout(500)
    ok("os três mapas completos são anexados ao laudo", "#/laudo/REQ-0013" in pg.url and contar(pg, "mapas") == 9)
    m = pg.evaluate("async ()=> (await db.porIndice('mapas','laudo_id','L-REQ-0013')).find(x=>x.tipo_mapa==='localizacao')")
    ok("o mapa guarda tipo, modelo, elementos e medida (RN02)", m["tipo_mapa"] == "localizacao" and m["modelo_id"] == "localizacao" and m["elementos"]["norte"] == "valor de teste" and m["valor_extra"] == "12,5")
    ok("a lista de mapas mostra os três elementos conferidos", pg.locator("#paListaMapas li.feito").count() == 3)
    # com mapa e cabeçalho, a versão impressa abre
    ir(pg, url, "#/pdf/REQ-0013", 500)
    ok("com mapa e cabeçalho, a versão impressa abre (RN03)", pg.locator("#paDocumento").count() == 1)
    doc = pg.inner_text("#paDocumento")
    ok("o documento traz o cabeçalho e os mapas anexados", "LAUDO" in doc and "2026.888888-8" in doc and "Mapas anexados (3)" in doc)
    # conclusão salva aparece no documento
    ir(pg, url, "#/laudo/REQ-0013", 400)
    pg.fill("#paConclusao", "Área de 12,5 ha com vegetação queimada."); pg.click("#formPaConclusao button[type=submit]"); pg.wait_for_timeout(500)
    ir(pg, url, "#/pdf/REQ-0013", 500)
    ok("a conclusão vai para a versão impressa", "vegetação queimada" in pg.inner_text("#paDocumento"))
    # a conclusão do laudo concluído exige mapa, e o exemplo já tem
    ok("todos os mapas do exemplo e o novo vêm com os elementos completos",
       pg.evaluate("async ()=> (await db.list('mapas')).filter(m=>paMapaCompleto(m)).length") == 9)

# origem: sprint4.py
@cenario
def s4_conclusao_com_assinatura(pg, url, ok):
    perfil(pg, url, "perito")
    semear(pg, url)
    rid = pg.evaluate("""async ()=>{ const rs = await db.list('requisicoes'); const r = rs.find(x=>x.status!=='concluida');
        const l = (await db.porIndice('laudos','requisicao_id',r.id_requisicao))[0];
        for (const [i, tipo] of ['localizacao','antes','depois'].entries()) await db.put('mapas', {id_mapa: 'M-TESTE-' + i, laudo_id: l.id_laudo,
          tipo_mapa: tipo, modelo_id: 'delimitacao', modelo: 'Delimitação da área de dano',
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

# origem: sprint4.py
@cenario
def s5_fila_e_prioridade(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
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

# origem: sprint4.py
@cenario
def s6_produtividade_e_aceite(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    ir(pg, url, "#/painel", 900)
    ok("o painel mostra tempo médio do laudo e horas médias com a meta de 12 h",
       pg.locator("[data-pa-ind=dias]").count() == 1 and pg.locator("[data-pa-ind=horas]").count() == 1
       and "meta 12 h" in pg.inner_text("#paGestor"))
    ok("as horas por tipo de infração aparecem em gráfico", pg.locator("#paGestor svg[role=img]").count() == 1)
    with pg.expect_download() as dl:
        pg.click("#btnPaCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV de produtividade sai com BOM e as colunas do laudo", csv.startswith(b"\xef\xbb\xbf") and b"requisicao;numero;orgao" in csv)
    ok("o roteiro de aceite está em modelos/", (PASTA / "modelos" / "roteiro-aceite.md").exists())

@cenario
def s8_feedback_secoes_e_docx(pg, url, ok):
    perfil(pg, url, "perito")
    semear(pg, url)
    rid = pg.evaluate("async ()=> (await db.list('requisicoes')).find(r=>r.status!=='concluida').id_requisicao")
    ir(pg, url, "#/laudo/" + rid, 700)
    ok("o cabeçalho tem autoridade, natureza, datas, horários e setor",
       all(x in pg.inner_text("#tabelaCabecalho") for x in ("Autoridade requisitante", "Natureza do exame", "Data de elaboração", "Horário de início", "Setor")))
    ok("as abas novas existem", all(pg.locator("#aba-" + a).count() == 1 for a in ("metodologia", "consideracoes", "valoracao", "quesitos")))
    pg.click("#aba-metodologia"); pg.fill("#paMetodologia", "Metodologia de teste com sensoriamento remoto.")
    pg.click("#aba-consideracoes"); pg.fill("#paConsideracoes", "Considerações de teste sobre a imagem.")
    pg.click("#aba-valoracao"); pg.fill("#paAreaHa", "2"); pg.fill("#paValorHa", "100")
    ok("a valoração calcula o total", pg.input_value("#paValorTotal") == "200.00")
    pg.click("#aba-quesitos"); pg.fill("#paQuesitos", "1) Houve dano? Sim.")
    pg.click("#aba-conclusao"); pg.click("[data-pa-salvar]"); pg.wait_for_timeout(700)
    l = pg.evaluate("async id => (await db.porIndice('laudos','requisicao_id',id))[0]", rid)
    ok("as seções ficam gravadas no laudo", l.get("metodologia", "").startswith("Metodologia de teste") and l.get("valor_total") == 200 and l.get("quesitos_texto", "").startswith("1)"))
    with pg.expect_download() as dl:
        pg.click("#btnPaDocx")
    dados = pathlib.Path(dl.value.path()).read_bytes()
    import io, zipfile
    with zipfile.ZipFile(io.BytesIO(dados)) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    ok("o .docx leva cabeçalho, metodologia, valoração e quesitos",
       dados[:2] == b"PK" and all(x in xml for x in ("LAUDO PERICIAL AMBIENTAL", "Metodologia", "Valoração", "Quesitos", "Autoridade requisitante")))


@cenario
def s10_timbre_no_laudo(pg, url, ok):
    import io, zipfile
    perfil(pg, url, "perito")
    semear(pg, url)
    rid = pg.evaluate("async ()=> (await db.list('requisicoes')).find(r=>r.status!=='concluida').id_requisicao")
    ir(pg, url, "#/laudo/" + rid, 700)
    with pg.expect_download() as dl:
        pg.click("#btnPaDocx")
    dados = pathlib.Path(dl.value.path()).read_bytes()
    with zipfile.ZipFile(io.BytesIO(dados)) as z:
        nomes = z.namelist(); cab = z.read("word/header1.xml").decode("utf-8"); rod = z.read("word/footer1.xml").decode("utf-8"); doc = z.read("word/document.xml").decode("utf-8")
    ok("o .docx traz cabeçalho e rodapé timbrados", "PERÍCIA OFICIAL E IDENTIFICAÇÃO TÉCNICA" in cab and "Diretoria de Interiorização" in cab and "NUMPAGES" in rod and "headerReference" in doc and "footerReference" in doc)
    ok("o brasão e a faixa da missão entram no .docx", "word/media/brasao.png" in nomes and "word/media/faixa.jpg" in nomes)
    # laudo completo, para a versão impressa liberar
    pg.evaluate("""async id=>{ const l = (await db.porIndice('laudos','requisicao_id',id))[0]; const m = {elementos:{escala:'1:1000',fonte:'INPE',norte:true,legenda:true,coordenadas:true,titulo:'t',responsavel:'r',data:'d'},valor_extra:'1',laudo_id:l.id_laudo,requisicao_id:id};
      const base = (await db.list('mapas'))[0] || {}; for (const [t, mod] of [['localizacao','localizacao'],['antes','delimitacao'],['depois','app']]) await db.put('mapas', {...base, ...(base.id_mapa?{}:m), id_mapa:'M-'+t, laudo_id:l.id_laudo, tipo_mapa:t, modelo_id:mod}); }""", rid)
    ir(pg, url, "#/pdf/" + rid, 700)
    corpo = pg.content()
    if pg.locator("#paDocumento").count():
        ok("a versão impressa tem o timbre e a faixa", "PERÍCIA OFICIAL E IDENTIFICAÇÃO TÉCNICA" in pg.inner_text("#paDocumento") and pg.locator("#paDocumento .pa-timbre img").count() == 1 and "@bottom-center" in corpo and "print-color-adjust:exact" in corpo)
    else:
        ok("a versão impressa tem o timbre e a faixa", False)


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
