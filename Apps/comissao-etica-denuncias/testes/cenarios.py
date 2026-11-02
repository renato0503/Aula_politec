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
def s2_registro_da_denuncia(pg, url, ok):
    perfil(pg, url, "secretario")
    ir(pg, url, "#/denuncia/nova", 400)
    pg.fill("#dDenunciante", "Denunciante Teste"); pg.fill("#dDenunciado", "Servidor Teste"); pg.fill("#dRelato", "curto")
    pg.click("#formDenuncia button[type=submit]"); pg.wait_for_timeout(300)
    ok("relato curto é recusado", "50 caracteres" in pg.inner_text("#errosDenuncia") and contar(pg, "denuncias") == 0)
    pg.fill("#dRelato", "O chefe gritou com a servidora na frente da equipe e a humilhou, com ameaças de remoção do setor.")
    pg.set_input_files("#dAnexos", {"name": "print.png", "mimeType": "image/png", "buffer": b"PNG teste"})
    pg.click("#formDenuncia button[type=submit]"); pg.wait_for_timeout(600)
    ok("denúncia registrada com protocolo CE-AAAA-001", pg.evaluate("async ()=> (await db.list('denuncias'))[0]?.protocolo || ''").endswith("-001"))
    ok("anexo guardado", contar(pg, "anexos") == 1)
    ok("histórico registra a ação com o perfil (RN05)", "denúncia registrada" in pg.inner_text("#historico") and "secretario" in pg.inner_text("#historico"))
    ir(pg, url, "#/painel", 300)
    ok("o caso aparece no painel, na etapa registro", pg.inner_text("[data-etapa-qtd=registro]") == "1")

# origem: sprint3.py
@cenario
def s3_classificacao_assistida(pg, url, ok):
    perfil(pg, url, "membro")
    semear(pg, url)
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

# origem: sprint4.py
@cenario
def s4_admissibilidade_e_prova_pendente(pg, url, ok):
    perfil(pg, url, "presidente")
    semear(pg, url)
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

# origem: sprint4.py
@cenario
def s5_oitivas_com_roteiro(pg, url, ok):
    perfil(pg, url, "membro")
    semear(pg, url)
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

# origem: sprint4.py
@cenario
def s6_documentos_cominacao_e_relatorio(pg, url, ok):
    perfil(pg, url, "presidente")
    semear(pg, url)
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
    ok("o roteiro de aceite está em modelos/", (PASTA / "modelos" / "roteiro-aceite.md").exists())

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
