"""Cenários de interface do Evento de Substituição Temporária.

Usam a tela como uma pessoa usaria e conferem o "Pronto quando" de cada sprint
do sprint.md.

Uso: python testes/cenarios.py      (requer: pip install playwright && playwright install chromium)
"""
import io
import pathlib
import sys
import tempfile
import time
import zipfile

from playwright.sync_api import sync_playwright

PASTA = pathlib.Path(__file__).resolve().parent.parent
TMP = pathlib.Path(tempfile.mkdtemp(prefix="cenarios-est-"))
CENARIOS = []


def cenario(fn):
    CENARIOS.append(fn)
    return fn


def contar(pg, store):
    return pg.evaluate("async s => (await db.list(s)).length", store)


def esperar(pg, expr, arg=None, timeout=60):
    fim = time.time() + timeout
    while time.time() < fim:
        if pg.evaluate(expr, arg):
            return True
        pg.wait_for_timeout(150)
    raise AssertionError("tempo esgotado: " + expr[:70])


def semear(pg, url):
    ir(pg, url, "#/config")
    pg.click("#btnSeed")
    esperar(pg, "async () => (await db.list('log')).some(l => String(l.acao || '').startsWith('dados fictícios'))")
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


def evento(pg, expr):
    return pg.evaluate("async expr => { const es = await db.list('eventos'); return (es.find(e => (" + expr + ")))?.id_evento || ''; }", None)


# Sprint 2 · abertura e regras
@cenario
def s1_abertura_e_regras(pg, url, ok):
    perfil(pg, url, "unidade")
    semear(pg, url)
    antes = contar(pg, "eventos")
    ir(pg, url, "#/evento/novo", 400)
    pg.click("#formEstNovo button[type=submit]")
    pg.wait_for_timeout(400)
    erros = pg.inner_text("#estErros")
    ok("sem os dados, a abertura é recusada (RN01 e RN02)", "Informe o número" in erros and "motivo válido" in erros and contar(pg, "eventos") == antes)
    pg.fill("#estNumero", "2026.9999-SIGADOC")
    pg.select_option("#estUnidade", "U-GAB")
    pg.select_option("#estMotivo", "Férias")
    pg.fill("#estSubstituido", "Ana Fictícia")
    pg.fill("#estSubstituto", "Ana Fictícia")
    pg.click("#formEstNovo button[type=submit]")
    pg.wait_for_timeout(400)
    ok("o substituto não pode ser o substituído (RN02)", "RN02" in pg.inner_text("#estErros"))
    pg.fill("#estSubstituto", "Beto Fictício")
    pg.click("#formEstNovo button[type=submit]")
    pg.wait_for_timeout(700)
    novo = pg.evaluate("async () => (await db.list('eventos')).find(e => e.numero_sigadoc === '2026.9999-SIGADOC')")
    ok("o ofício é registrado e abre a ficha", bool(novo) and "#/evento/" + novo["id_evento"] in pg.url)
    ok("o evento entra em autorização hierárquica", bool(novo) and novo["status"] == "autorizacao")
    ok("a abertura cria um nível de autorização por chefia", bool(novo) and pg.evaluate("async id => (await db.porIndice('autorizacoes','evento_id',id)).length", novo["id_evento"]) == 2)
    ir(pg, url, "#/evento/novo", 400)
    pg.fill("#estNumero", "2026.9999-SIGADOC")
    pg.select_option("#estUnidade", "U-GAB")
    pg.select_option("#estMotivo", "Férias")
    pg.fill("#estSubstituido", "Ana Fictícia")
    pg.fill("#estSubstituto", "Beto Fictício")
    pg.click("#formEstNovo button[type=submit]")
    pg.wait_for_timeout(400)
    ok("o processo do SIGADOC repetido é recusado", "já está cadastrado" in pg.inner_text("#estErros"))
    ir(pg, url, "#/eventos", 500)
    ok("a lista mostra o evento novo e o limite do dia 05", "2026.9999-SIGADOC" in pg.inner_text("table") and "Limite" in pg.inner_text("table"))


# Sprint 3 · autorização hierárquica e devolução
@cenario
def s2_autorizacao_e_devolucao(pg, url, ok):
    perfil(pg, url, "hierarquia")
    semear(pg, url)
    eid = evento(pg, "e.status === 'autorizacao'")
    ok("há evento aguardando autorização", bool(eid))
    ir(pg, url, "#/evento/" + eid, 700)
    pg.locator("[data-est-autorizar]").first.click()
    pg.wait_for_timeout(700)
    ok("a primeira chefia autoriza", pg.evaluate("async id => (await db.porIndice('autorizacoes','evento_id',id)).some(a => a.situacao === 'autorizado')", eid))
    if pg.locator("[data-est-autorizar]").count():
        pg.locator("[data-est-autorizar]").first.click()
        pg.wait_for_timeout(700)
    ok("com todas as autorizações, o evento segue ao Gabinete (RN03)", pg.evaluate("async id => (await db.get('eventos',id)).status === 'gabinete'", eid))
    ok("o histórico registra o envio ao Gabinete", pg.evaluate("async id => (await db.porIndice('log','evento_id',id)).some(l => l.tipo_evento === 'enviado ao Gabinete')", eid))

    eid2 = evento(pg, "e.status === 'autorizacao'")
    ok("há outro evento para devolver", bool(eid2))
    ir(pg, url, "#/evento/" + eid2, 700)
    pg.locator("[data-est-devolver]").first.click()
    pg.wait_for_timeout(700)
    ok("a chefia devolve o evento à unidade", pg.evaluate("async id => (await db.get('eventos',id)).status === 'devolvido'", eid2))
    perfil(pg, url, "unidade")
    ir(pg, url, "#/evento/" + eid2, 700)
    pg.click("#btnEstReenviar")
    pg.wait_for_timeout(700)
    ok("a unidade reenvia e as autorizações voltam a pendente", pg.evaluate("async id => (await db.get('eventos',id)).status === 'autorizacao' && (await db.porIndice('autorizacoes','evento_id',id)).every(a => a.situacao === 'pendente')", eid2))


# Sprint 4 · Gabinete, análise de RH e ficha
@cenario
def s3_gabinete_rh_e_ficha(pg, url, ok):
    perfil(pg, url, "gabinete")
    semear(pg, url)
    eid = evento(pg, "e.status === 'gabinete'")
    ok("há evento no Gabinete", bool(eid))
    ir(pg, url, "#/evento/" + eid, 700)
    pg.click("#btnEstEnviarRh")
    pg.wait_for_timeout(700)
    ok("o Gabinete encaminha ao RH (RN04)", pg.evaluate("async id => (await db.get('eventos',id)).status === 'analise_rh'", eid))
    perfil(pg, url, "rh")
    ir(pg, url, "#/evento/" + eid, 700)
    pg.fill("#estFichaAnalista", "Analista de Teste")
    pg.click("#formEstFicha button[type=submit]")
    pg.wait_for_timeout(800)
    ok("a ficha de solicitação é incluída", pg.evaluate("async id => (await db.porIndice('fichas','evento_id',id)).length === 1", eid))
    ok("com a ficha, o evento segue para assinatura", pg.evaluate("async id => (await db.get('eventos',id)).status === 'aguardando_assinatura'", eid))
    ok("o histórico registra a ficha", pg.evaluate("async id => (await db.porIndice('log','evento_id',id)).some(l => l.tipo_evento === 'ficha de solicitação incluída')", eid))


# Sprint 5 · assinatura, envio à SESP e prazo do dia 05
@cenario
def s4_assinatura_e_prazo(pg, url, ok):
    perfil(pg, url, "diretor")
    semear(pg, url)
    eid = evento(pg, "e.status === 'aguardando_assinatura'")
    ok("há evento aguardando assinatura", bool(eid))
    ir(pg, url, "#/evento/" + eid, 700)
    pg.fill("#estAssNome", "Diretor Signatário de Teste")
    pg.click("#formEstAssinar button[type=submit]")
    pg.wait_for_timeout(800)
    ok("a assinatura fica registrada (RN05)", pg.evaluate("async id => { const e = await db.get('eventos',id); return e.status === 'assinado' && e.assinado_por && e.assinado_em; }", eid))
    perfil(pg, url, "rh")
    eid2 = evento(pg, "e.status === 'assinado' && estEnvioNoPrazo(e)")
    ok("há evento assinado dentro do prazo", bool(eid2))
    ir(pg, url, "#/evento/" + eid2, 700)
    pg.click("#btnEstEnviarSesp")
    pg.wait_for_timeout(800)
    ok("o evento é encaminhado à SESP dentro do prazo", pg.evaluate("async id => { const e = await db.get('eventos',id); return e.status === 'encaminhado_sesp' && !!e.envio_sesp_em; }", eid2))

    eid3 = evento(pg, "e.status === 'assinado' && !estEnvioNoPrazo(e)")
    ok("há evento assinado fora do prazo do dia 05", bool(eid3))
    ir(pg, url, "#/evento/" + eid3, 700)
    ok("fora do prazo, o envio é bloqueado (RN06)", "Fora do prazo" in pg.inner_text("#conteudo") and pg.locator("#btnEstEnviarSesp").count() == 0)
    pg.select_option("#estIndMotivo", "Enviado depois do dia 05 (RN06)")
    pg.click("#formEstIndeferir button[type=submit]")
    pg.wait_for_timeout(700)
    ok("o evento fora do prazo é indeferido", pg.evaluate("async id => (await db.get('eventos',id)).status === 'indeferido'", eid3))


# Sprint 6 · publicação no DO e planilha de controle
@cenario
def s5_publicacao_e_planilha(pg, url, ok):
    perfil(pg, url, "rh")
    semear(pg, url)
    eid = evento(pg, "e.status === 'encaminhado_sesp'")
    ok("há evento encaminhado à SESP", bool(eid))
    ir(pg, url, "#/evento/" + eid, 700)
    pg.fill("#estPubNumero", "DO-2026-9999")
    pg.click("#formEstPublicar button[type=submit]")
    pg.wait_for_timeout(800)
    ok("a publicação no DO encerra o evento (RN07)", pg.evaluate("async id => (await db.get('eventos',id)).status === 'publicado'", eid))
    ok("a publicação fica registrada", pg.evaluate("async id => (await db.porIndice('publicacoes','evento_id',id)).length === 1", eid))
    ok("o histórico registra o encerramento", pg.evaluate("async id => (await db.porIndice('log','evento_id',id)).some(l => l.tipo_evento === 'evento encerrado')", eid))
    ir(pg, url, "#/planilha", 600)
    texto = pg.inner_text("#tabelaEstPlanilha")
    ok("a planilha traz os cinco campos obrigatórios", all(x in texto for x in ["Substituído", "Substituto", "Motivo", "Período", "Publicação no DO"]))
    ok("a publicação aparece na planilha", "DO-2026-9999" in texto)
    with pg.expect_download() as dl:
        pg.click("#btnEstCsv")
    csv = pathlib.Path(dl.value.path()).read_bytes()
    ok("o CSV sai com BOM e as colunas do controle", csv.startswith(b"\xef\xbb\xbf") and "Publicação no DO".encode() in csv and "Substituído".encode() in csv)


# Sprint 1 e 3 · painel e fila por perfil
@cenario
def s6_painel_e_fila(pg, url, ok):
    perfil(pg, url, "diretor")
    semear(pg, url)
    aguardando = pg.evaluate("async () => (await db.list('eventos')).filter(e => e.status === 'aguardando_assinatura').length")
    ir(pg, url, "#/painel", 800)
    ok("o painel conta os eventos aguardando assinatura", pg.inner_text("[data-est-kpi=assinatura]") == str(aguardando))
    ok("o painel mostra a minha fila do perfil", "Minha fila" in pg.inner_text("#conteudo") and "Aguardando assinatura" in pg.inner_text("#conteudo"))
    ir(pg, url, "#/fila", 700)
    ok("a fila do diretor tem um cartão por evento", pg.locator(".est-fila-card").count() == aguardando)
    perfil(pg, url, "rh")
    esperados = pg.evaluate("async () => (await db.list('eventos')).filter(e => ['analise_rh','assinado','encaminhado_sesp'].includes(e.status)).length")
    ir(pg, url, "#/fila", 700)
    ok("a fila do RH reúne análise, envio e publicação", pg.locator(".est-fila-card").count() == esperados)
    perfil(pg, url, "unidade")
    devolvidos = pg.evaluate("async () => (await db.list('eventos')).filter(e => e.status === 'devolvido').length")
    ir(pg, url, "#/fila", 700)
    ok("a fila da unidade mostra os devolvidos", pg.locator(".est-fila-card").count() == devolvidos)


# Sprint 8 · ajuste da unidade antes do reenvio
@cenario
def s7_ajuste_e_reenvio(pg, url, ok):
    perfil(pg, url, "unidade")
    semear(pg, url)
    eid = evento(pg, "e.status === 'devolvido'")
    ok("há evento devolvido para ajustar", bool(eid))
    ir(pg, url, "#/evento/" + eid, 700)
    ok("a unidade vê o formulário de ajuste", pg.locator("#formEstAjuste").count() == 1)
    substituido = pg.input_value("#estAjusteSubstituido")
    pg.fill("#estAjusteSubstituto", substituido)
    pg.click("#formEstAjuste button[type=submit]")
    pg.wait_for_timeout(400)
    ok("o ajuste recusa o substituto igual ao substituído (RN02)", "RN02" in pg.inner_text("#estErrosAjuste"))
    pg.fill("#estAjusteSubstituto", "Substituto Ajustado")
    pg.fill("#estAjusteObservacao", "Ajustado depois da devolução da chefia.")
    pg.click("#formEstAjuste button[type=submit]")
    pg.wait_for_timeout(800)
    ok("o ajuste atualiza o substituto e reenvia", pg.evaluate("async id => { const e = await db.get('eventos',id); return e.status === 'autorizacao' && e.substituto === 'Substituto Ajustado'; }", eid))
    ok("o reenvio zera as autorizações", pg.evaluate("async id => (await db.porIndice('autorizacoes','evento_id',id)).every(a => a.situacao === 'pendente')", eid))
    ok("o histórico registra o ajuste", pg.evaluate("async id => (await db.porIndice('log','evento_id',id)).some(l => l.tipo_evento === 'evento ajustado pela unidade')", eid))


# Sprint 8 · planilha Excel
@cenario
def s8_planilha_excel(pg, url, ok):
    perfil(pg, url, "rh")
    semear(pg, url)
    ir(pg, url, "#/planilha", 600)
    ok("o botão da planilha Excel existe", pg.locator("#btnEstXlsx").count() == 1)
    with pg.expect_download() as dl:
        pg.click("#btnEstXlsx")
    dados = pathlib.Path(dl.value.path()).read_bytes()
    ok("o .xlsx é um arquivo ZIP", dados.startswith(b"PK") and len(dados) > 1000)
    with zipfile.ZipFile(io.BytesIO(dados)) as z:
        wb = z.read("xl/workbook.xml").decode("utf-8", "ignore")
    ok("o .xlsx tem as abas Controle e Resumo", "Controle" in wb and "Resumo" in wb)


def main():
    erro = False
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for fn in CENARIOS:
            ctx = nav.new_context(accept_downloads=True)
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
