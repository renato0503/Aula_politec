"""Cenários de interface do Sistema de Controle de Necropsia (espelho DMML / POLITEC).

Usam a tela como uma pessoa usaria e conferem o "Pronto quando" do sprint.md.

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
    """Carrega os dados fictícios e espera a importação terminar."""
    ir(pg, url, "#/config")
    pg.click("#btnSeed")
    esperar(pg, "async () => (await db.list('log')).some(l => String(l.acao || '').startsWith('dados fictícios'))")
    pg.wait_for_timeout(300)
    pg.reload()
    pg.wait_for_function("() => typeof db !== 'undefined' && !!db.con", timeout=15000)
    pg.wait_for_timeout(400)


def ir(pg, url, rota, espera=300):
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


def assinar(pg):
    """Desenha no canvas da janela de assinatura."""
    caixa = pg.locator("#espCanvas").bounding_box()
    pg.mouse.move(caixa["x"] + 20, caixa["y"] + 80)
    pg.mouse.down()
    for i in range(6):
        pg.mouse.move(caixa["x"] + 45 + i * 28, caixa["y"] + 60 + (i % 2) * 22)
    pg.mouse.up()
    pg.wait_for_timeout(250)


# ================= painel =================
@cenario
def s10_painel_indicadores(pg, url, ok):
    perfil(pg, url, "tecnico")
    semear(pg, url)
    ir(pg, url, "#/painel", 700)
    ok("o painel tem os dez indicadores do protótipo", pg.locator("#espKpiGrid .esp-kpi").count() == 10)
    esperado = {"todos": "10", "Ocorrência em andamento": "2", "Aguardando necropsia": "2",
                "Necropsia em andamento": "1", "Aguardando identificação": "1", "Aguardando família": "1",
                "Aguardando funerária": "0", "Sepultado pelo Estado": "1", "Custódia finalizada": "1",
                "lacres": "2"}
    for chave, valor in esperado.items():
        cartao = pg.locator(f'[data-esp-kpi="{chave}"]')
        ok(f"o indicador {chave} mostra {valor}", cartao.count() == 1 and cartao.inner_text().split("\n")[0] == valor)
    ok("o quadro das sete etapas aparece para o Técnico", pg.locator("#espQuadro .esp-coluna").count() == 7)
    pg.click('[data-esp-kpi="Custódia finalizada"]')
    pg.wait_for_timeout(700)
    ok("clicar no indicador leva à lista filtrada", pg.locator("#espChip .esp-chip").count() == 1
       and "Custódia finalizada" in pg.inner_text("#espChip"))
    ok("a lista filtrada mostra só o caso concluído", pg.locator(".esp-tabela tbody tr").count() == 1)


# ================= lista e gaveta =================
@cenario
def s10_lista_filtros_e_gaveta(pg, url, ok):
    perfil(pg, url, "tecnico")
    semear(pg, url)
    ir(pg, url, "#/corpos", 700)
    ok("a lista mostra os dez corpos", pg.locator(".esp-tabela tbody tr").count() == 10)
    ok("a contagem vem dos registros", "10 de 10" in pg.inner_text("#espContagem"))
    nomes = pg.evaluate("async ()=> (await db.list('corpos')).filter(c=>c.identificado).map(c=>c.nome)")
    ok("a lista mostra só as iniciais do nome (RN05)", not any(n in pg.inner_text("#espContagem") + pg.inner_text(".esp-tabela") for n in nomes))
    pg.select_option("#espStatus", "Sepultado pelo Estado")
    pg.wait_for_timeout(700)
    ok("o filtro de situação funciona", pg.locator(".esp-tabela tbody tr").count() == 1)
    pg.click("[data-esp-acao=esp-limpar-filtros]")
    pg.wait_for_timeout(700)
    pg.fill("#espBusca", "000125")
    pg.dispatch_event("#espBusca", "change")
    pg.wait_for_timeout(700)
    ok("a busca pelo protocolo acha o corpo", pg.locator(".esp-tabela tbody tr").count() == 1)
    pg.click("[data-esp-acao=esp-limpar-filtros]")
    pg.wait_for_timeout(700)
    pg.click("[data-esp-acao=esp-ver-detalhes]")
    pg.wait_for_timeout(900)
    ok("a gaveta abre com a ficha do caso", pg.locator(".esp-gaveta").count() == 1 and pg.locator(".esp-gaveta .esp-bloco").count() >= 7)
    ok("a gaveta mostra o protocolo e a situação", "Status:" in pg.inner_text(".esp-gaveta-topo"))
    pg.click(".esp-gaveta [data-esp-acao=esp-fechar-gaveta]")
    pg.wait_for_timeout(700)
    ok("a gaveta fecha", pg.locator(".esp-gaveta").count() == 0)


# ================= resumo =================
@cenario
def s10_resumo_por_agente_causal(pg, url, ok):
    perfil(pg, url, "tecnico")
    semear(pg, url)
    ir(pg, url, "#/resumo", 700)
    linhas = pg.locator(".esp-tabela tbody tr")
    ok("o resumo traz os seis agentes e o total", linhas.count() == 7)
    esperado = {"Homicídio": [3, 0, 1, 2, 0, 0], "Suicídio": [2, 1, 0, 0, 1, 1],
                "Acidente de trânsito": [2, 1, 0, 1, 0, 0], "Afogamento": [1, 0, 0, 1, 0, 0],
                "Queda de altura": [0, 0, 0, 0, 0, 0], "Indeterminada": [2, 0, 0, 2, 0, 0]}
    for agente, numeros in esperado.items():
        linha = pg.locator(".esp-tabela tbody tr", has_text=agente).first
        celulas = [c.inner_text().strip() for c in linha.locator("td").all()]
        ok(f"a linha {agente} soma as colunas do protótipo", celulas[1:] == [str(n) for n in numeros])
    total = pg.locator(".esp-tabela tbody tr.esp-total")
    ok("o total geral fecha a tabela", [c.inner_text().strip() for c in total.locator("td").all()][1:] == ["10", "2", "1", "6", "1", "1"])


# ================= a ficha do caso =================
@cenario
def s10_ficha_com_as_sete_etapas(pg, url, ok):
    perfil(pg, url, "tecnico")
    semear(pg, url)
    ir(pg, url, "#/corpo/C-0005", 900)
    ok("a ficha mostra o stepper das sete etapas", pg.locator(".esp-stepper .esp-passo").count() == 7)
    for n in range(1, 6):
        ok(f"a etapa {n} está na ficha", pg.locator(f"#espEtapa{n}").count() == 1)
    ok("as etapas 6 e 7 só aparecem quando o caso chega nelas",
       pg.locator("#espEtapa6").count() == 0 and pg.locator("#espEtapa7").count() == 0)
    ir(pg, url, "#/corpo/C-0009", 900)
    ok("no caso que chegou à etapa 7, as etapas 6 e 7 estão na ficha",
       pg.locator("#espEtapa6").count() == 1 and pg.locator("#espEtapa7").count() == 1)
    ok("a etapa 7 registra a entrega do laudo à ADM", "Entrega de laudo para ADM" in pg.inner_text("#espEtapa7"))
    ok("a etapa 4 lista os quatro materiais", pg.locator("#espEtapa4 .esp-material").count() == 4)
    ok("a necropsia mostra a equipe", "Médico legista" in pg.inner_text("#espEtapa4"))
    ok("o histórico traz os registros do caso", pg.locator("#espHistorico .esp-timeline li").count() >= 3)
    ok("a consulta ao caso fica auditada", pg.evaluate("async id => (await db.list('log')).some(l=>l.corpo_id===id && l.acao==='consulta ao caso')", "C-0005"))
    ok("a alocação na base aparece na etapa 3", pg.locator("#espEtapa3").count() == 1 and "Câmara" in pg.inner_text("#espEtapa3"))


# ================= o fluxo completo =================
@cenario
def s10_fluxo_do_caso(pg, url, ok):
    perfil(pg, url, "tecnico")
    semear(pg, url)
    ir(pg, url, "#/corpo/C-0001", 900)
    pg.click("[data-esp-acao=esp-confirmar-entrada]")
    pg.wait_for_timeout(800)
    ok("a entrada na base leva à fila da necropsia", pg.evaluate("async id => (await db.get('corpos', id)).etapa", "C-0001") == 3)
    ir(pg, url, "#/corpo/C-0003", 900)
    pg.click("[data-esp-acao=esp-concluir-necropsia]")
    pg.wait_for_timeout(800)
    ok("a necropsia concluída leva à etapa 5", pg.evaluate("async id => (await db.get('corpos', id)).etapa", "C-0003") == 5)
    pg.select_option("#espResultado", "identificado")
    pg.wait_for_timeout(800)
    pg.select_option("#espMetodo", "Necropapiloscopia")
    pg.wait_for_timeout(800)
    pg.fill("#espNomeConfirmado", "Ricardo Almeida")
    pg.fill("#espResponsavel", "Técnico Marcos Oliveira")
    pg.fill("#espDataConfirmacao", "2026-03-13")
    pg.click("[data-esp-acao=esp-confirmar-identificacao]")
    pg.wait_for_timeout(900)
    ok("a identificação leva à etapa 6", pg.evaluate("async id => { const c = await db.get('corpos', id); return c.etapa === 6 && c.identificado; }", "C-0003"))
    pg.fill("#espFamNome", "Maria Almeida")
    pg.fill("#espParentesco", "Mãe")
    pg.fill("#espFamDocumento", "RG 1.234.567-8")
    pg.fill("#espFamData", "2026-03-17")
    pg.click("[data-esp-acao=esp-assinar]")
    pg.wait_for_timeout(800)
    assinar(pg)
    pg.click("[data-esp-janela=confirmar]")
    pg.wait_for_timeout(900)
    ok("a assinatura do familiar fica registrada", pg.evaluate("async id => !!(await db.get('corpos', id)).familia?.assinatura", "C-0003"))
    pg.click("[data-esp-acao=esp-confirmar-familia]")
    pg.wait_for_timeout(900)
    ok("a liberação à família fica registrada", pg.evaluate("async id => !!(await db.get('corpos', id)).familia?.liberado_em", "C-0003"))
    pg.fill("#espFunNome", "Funerária São Judas Tadeu")
    pg.fill("#espFunAuto", "AE-20901")
    pg.fill("#espFunData", "2026-03-18")
    pg.fill("#espFunHora", "10:30")
    pg.click("[data-esp-acao=esp-confirmar-funeraria]")
    pg.wait_for_timeout(900)
    ok("a entrega à funerária leva à etapa 7", pg.evaluate("async id => (await db.get('corpos', id)).etapa", "C-0003") == 7)
    pg.fill("#espLaudoEntreguePor", "Ana Paula Ribeiro")
    pg.fill("#espLaudoRecebeuPor", "Carlos Eduardo Nunes")
    pg.fill("#espLaudoData", "2026-03-24")
    pg.click("[data-esp-acao=esp-confirmar-laudo]")
    pg.wait_for_timeout(900)
    ok("a entrega do laudo fica registrada", pg.evaluate("async id => !!(await db.get('corpos', id)).laudo?.entregue_em", "C-0003"))
    perfil(pg, url, "gestor")
    ir(pg, url, "#/corpo/C-0003", 900)
    pg.check("#espLaudoAdm")
    pg.wait_for_timeout(1000)
    ok("o recebimento do laudo pela ADM encerra a custódia (RN10)",
       pg.evaluate("async id => { const c = await db.get('corpos', id); return !!c.laudo?.recebido_em && c.custodia_finalizada === true; }", "C-0003"))
    ok("o caso encerrado avisa que não se edita", "encerrado" in pg.inner_text("#conteudo").lower())


# ================= sepultamento pelo Estado e retificação =================
@cenario
def s10_sepultamento_pelo_estado(pg, url, ok):
    perfil(pg, url, "gestor")
    semear(pg, url)
    ir(pg, url, "#/corpo/C-0006", 900)
    pg.click("[data-esp-acao=esp-decisao-sepultamento]")
    pg.wait_for_timeout(800)
    ok("a janela de justificativa abre", pg.locator(".esp-janela").count() == 1)
    pg.fill("#espJustText", "curta")
    pg.click("[data-esp-janela=confirmar]")
    pg.wait_for_timeout(600)
    ok("a justificativa curta é recusada", "20 caracteres" in pg.inner_text(".esp-janela"))
    pg.fill("#espJustText", "Busca por familiares e métodos de identificação esgotados após 30 dias.")
    pg.click("[data-esp-janela=confirmar]")
    pg.wait_for_timeout(1000)
    ok("o encaminhamento para sepultamento pelo Estado fica registrado",
       pg.evaluate("async id => (await db.get('corpos', id)).identificacao?.resultado === 'nao_identificado'", "C-0006"))
    ok("a decisão administrativa aparece no histórico",
       "decisão administrativa" in pg.inner_text("#espHistorico").lower())
    # a funerária do sepultamento pelo Estado
    ir(pg, url, "#/corpo/C-0006", 900)
    pg.fill("#espFunNome", "Funerária do Estado")
    pg.fill("#espFunAuto", "AE-SEP-1")
    pg.fill("#espFunData", "2026-03-20")
    pg.fill("#espFunHora", "15:20")
    pg.fill("#espFunAutorizacao", "SE-5531")
    pg.fill("#espFunAutData", "2026-03-19")
    pg.fill("#espFunLocal", "Cemitério Municipal")
    pg.click("[data-esp-acao=esp-confirmar-sepultamento-estado]")
    pg.wait_for_timeout(1000)
    ok("o sepultamento pelo Estado fica registrado",
       pg.evaluate("async id => !!(await db.get('corpos', id)).sepultamento?.autorizacao", "C-0006"))
    ok("o caso mostra o selo de sepultado pelo Estado", "SEPULTADO PELO ESTADO" in pg.inner_text("#conteudo"))
    # retificação (RN12)
    ir(pg, url, "#/corpo/C-0006", 900)
    pg.select_option("#espRetTipo", "Familiar localizado após o sepultamento")
    pg.fill("#espRetTexto", "Familiar procurou o IML com documento da vítima.")
    pg.fill("#espRetMotivo", "curto")
    pg.click("[data-esp-acao=esp-retificar]")
    pg.wait_for_timeout(700)
    ok("a retificação com motivo curto é recusada", "motivo" in pg.inner_text("#espErroRet"))
    pg.fill("#espRetMotivo", "Familiar localizado depois do sepultamento pelo Estado.")
    pg.click("[data-esp-acao=esp-retificar]")
    pg.wait_for_timeout(900)
    ok("a retificação entra na lista sem apagar o registro",
       pg.locator("#espListaRetificacoes").count() == 1
       and pg.evaluate("async id => (await db.list('log')).some(l=>l.corpo_id===id && l.acao.startsWith('retificação'))", "C-0006"))


# ================= exame complementar (RN11) =================
@cenario
def s10_exame_complementar(pg, url, ok):
    perfil(pg, url, "tecnico")
    semear(pg, url)
    ir(pg, url, "#/corpo/C-0006", 900)
    pg.click("[data-esp-acao=esp-exame-complementar]")
    pg.wait_for_timeout(900)
    ok("o exame complementar fica em andamento", pg.locator("#espExamePendente").count() == 1)
    pg.select_option("#espResultadoExame", "sem_resultado")
    pg.click("[data-esp-acao=esp-resultado-exame]")
    pg.wait_for_timeout(900)
    ok("o resultado do exame entra nas tentativas", "sem resultado" in pg.inner_text("#espEtapa5"))
    ok("sem exame complementar os métodos não se esgotam",
       pg.evaluate("() => !tcPodeEsgotar([{metodo: 'Necropapiloscopia', resultado: 'sem resultado'}])"))
    pg.click("[data-esp-acao=esp-esgotar]")
    pg.wait_for_timeout(900)
    ok("depois do exame, os métodos se esgotam",
       pg.evaluate("async id => (await db.get('corpos', id)).identificacao?.resultado === 'nao_identificado'", "C-0006"))


# ================= perfis =================
@cenario
def s10_permissoes_dos_perfis(pg, url, ok):
    semear(pg, url)
    perfil(pg, url, "medico")
    ir(pg, url, "#/corpo/C-0003", 900)
    ok("o Médico Legista vê o aviso de leitura", "Médico Legista" in pg.inner_text("#conteudo"))
    ok("o Médico Legista não vê a etapa 6", pg.locator("#espEtapa6").count() == 0)
    ok("o Médico Legista não vê a etapa 7", pg.locator("#espEtapa7").count() == 0)
    ok("o Médico Legista não edita a ocorrência", pg.locator("#espDelegacia").count() == 0)
    perfil(pg, url, "tecnico")
    ir(pg, url, "#/corpo/C-0003", 900)
    ok("o Técnico edita a ocorrência", pg.locator("#espDelegacia").count() == 1)
    ok("o Técnico não confirma o recebimento pela ADM", pg.locator("#espLaudoAdm").count() == 0 or pg.is_disabled("#espLaudoAdm"))
    perfil(pg, url, "gestor")
    ir(pg, url, "#/corpo/C-0005", 900)
    ok("o Gestor ADM vê a fila de lacres", pg.locator("#espEtapa4 .esp-material").count() == 4)
    ok("o Gestor ADM pode marcar todos os lacres", pg.locator("[data-esp-acao=esp-marcar-todos]").count() == 1)
    pg.click("[data-esp-acao=esp-marcar-todos]")
    pg.wait_for_timeout(900)
    ok("os lacres pendentes são recebidos pela ADM",
       pg.evaluate("async () => (await db.list('lacres')).filter(l=>l.codigo).every(l=>l.recebido_em)"))


# ================= busca e novo acionamento =================
@cenario
def s10_busca_e_novo_acionamento(pg, url, ok):
    perfil(pg, url, "tecnico")
    semear(pg, url)
    ir(pg, url, "#/busca", 600)
    pg.fill("#tcBusca", "000125")
    pg.click("#btnTcBuscar")
    pg.wait_for_timeout(700)
    ok("a busca acha pelo protocolo (RN04)", "000125/2026" in pg.inner_text("#tcResultado"))
    pg.fill("#tcBusca", "Marcelo")
    pg.click("#btnTcBuscar")
    pg.wait_for_timeout(700)
    ok("a busca acha pelo nome", "000131/2026" in pg.inner_text("#tcResultado"))
    pg.fill("#tcBusca", "LA-44101")
    pg.click("#btnTcBuscar")
    pg.wait_for_timeout(700)
    ok("a busca acha pelo código do lacre", "000127/2026" in pg.inner_text("#tcResultado"))
    ir(pg, url, "#/corpo/novo", 600)
    ok("o novo acionamento abre as etapas 1 e 2", pg.locator("#tcNec").count() == 1 and pg.locator("#tcChegada").count() == 1)
    ok("o roteiro de aceite está em modelos/", (PASTA / "modelos" / "roteiro-aceite.md").exists())
    nec = pg.input_value("#tcNec")
    pg.fill("#tcDelegacia", "Delegacia de Teste")
    pg.fill("#tcEndereco", "Rua Fictícia, 10")
    pg.fill("#tcMunicipio", "Cuiabá")
    pg.fill("#tcTecnico", "Técnico Teste")
    pg.click("#btnTcNovo")
    pg.wait_for_timeout(900)
    ok("o acionamento é registrado", "#/corpo/" in pg.url and pg.evaluate("async()=> (await db.list('corpos')).length") == 11)
    ir(pg, url, "#/corpo/novo", 600)
    pg.fill("#tcNec", nec)
    pg.fill("#tcDelegacia", "X"); pg.fill("#tcEndereco", "Y"); pg.fill("#tcMunicipio", "Z"); pg.fill("#tcTecnico", "W")
    pg.click("#btnTcNovo")
    pg.wait_for_timeout(700)
    ok("o número de necropsia repetido é recusado (RN01)", "já está registrado" in pg.inner_text("#tcErros"))


def main():
    erro = False
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for fn in CENARIOS:
            ctx = nav.new_context(accept_downloads=True, viewport={"width": 1440, "height": 1000})
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
                resultados.append((f"exceção: {str(e)[:600]}", False))
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
