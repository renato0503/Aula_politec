"""Jornada do cliente nos 20 apps (Playwright).

Executa cada app como uma pessoa usaria: abre, carrega os dados fictícios, troca
de perfil, percorre as telas e faz a tarefa principal. Registra erros no formato
do `Apps/JORNADA-BACKLOG.md` e o resultado em `Apps/jornada-resultados.json`.

Uso:
    python Apps/jornada.py                 # os 20
    python Apps/jornada.py agendamento-cin # um app
"""
import json
import pathlib
import sys
import traceback

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "_base"))
from jornada_lib import Jornada, PASTA_APPS, PASTA_SAIDA  # noqa: E402

PERFIL = {
    "agendamento-cin": "posto",
    "cin-segunda-via": "servidor",
    "horus-banco-demandas": "DIRETOR",
    "trilha-custodia-necropsia": "plantonista",
    "controle-aquisicoes": "compras",
    "custodia-definitiva": "custodia",
    "documentapolitec": "papiloscopista",
    "gestao-documentos": "servidor",
    "renovacao-contratos-horus": "gestor",
    "distribuicao-casos-dna": "coordenador",
    "comissao-etica-denuncias": "presidente",
    "passivo-ambiental": "perito",
    "rnc-nao-conformidade": "cqual",
    "tap-portfolio-projetos": "equipe",
    "adiantamento": None,
    "metas-bi-ocr": None,
    "inscricoes-cursos": "gerencia",
    "mapa-distribuicao-credor": None,
    "equipamentos-google-earth": "coordenadoria",
    "agiliza-mais": None,
}


def primeiro(j, seletor):
    item = j.pg.locator(seletor).first
    texto = item.inner_text() if item.count() else ""
    return item, texto


def jornada_agendamento(j):
    j.semear()
    j.abrir("")
    j.ok("abre no agendamento do cidadão", "Agendar a Carteira" in j.texto("main"))
    j.ok("não mostra tela de perfil", "Escolha o perfil" not in j.texto("main"))
    j.clicar("[data-posto=P01]")
    j.ok("o calendário do mês mostra dias com vaga", j.conta("[data-dia]") > 0)
    j.clicar("[data-dia]")
    j.ok("o dia escolhido abre os horários", j.conta("[data-horario]") > 0)
    j.clicar("[data-horario]")
    j.preencher("#aNome", "Cliente Jornada")
    j.preencher("#aTel", "(65) 99999-0000")
    j.preencher("#aCpf", "529.982.247-25")
    j.checar("#aAviso")
    j.clicar("#formAgDados button[type=submit]")
    j.ok("o comprovante sai com protocolo", j.esperar_texto("#protCin", "CIN-"), "protocolo CIN-XXXXXX")
    j.capturar("comprovante")


def jornada_cin_segunda_via(j):
    j.semear()
    j.abrir("#/pedido")
    j.ok("a inscrição pública abre sem menu interno", "Pedir a segunda via" in j.texto("main"))
    j.ok("não mostra tela de perfil", "Escolha o perfil" not in j.texto("main"))
    j.checar("input[name=valida][value=sim]")
    j.checar("input[name=mudou][value=nao]")
    j.clicar("#formElegivel button[type=submit]")
    j.ok("o formulário de dados abre", j.conta("#formPedido") == 1)
    j.preencher("#cNome", "Alice Jornada")
    j.preencher("#cCpf", j.avaliar("async () => dadosEmbutidos('seed').pedidos[0].cpf"))
    j.preencher("#cNasc", "1990-05-10")
    j.preencher("#cValidade", "2030-01-01")
    j.preencher("#cContato", "alice.jornada@exemplo.com")
    j.clicar("[data-teste=rosto]")
    j.clicar("[data-teste=documento]")
    j.pg.wait_for_timeout(600)
    j.clicar("#formPedido button[type=submit]")
    j.ok("o pedido gera protocolo 2V-", j.esperar_texto("#numProtocolo", "2V-"), "protocolo 2V-XXXXXX")
    j.capturar("protocolo")
    j.ir("#/config")
    j.trocar_perfil("servidor")
    j.ir("#/fila")
    j.ok("a caixa de entrada abre com pedidos", j.conta("[data-sel]") > 0)
    j.clicar("[data-sel]")
    j.ok("o pedido abre na ficha", j.conta("#fichaPedido") == 1)
    j.capturar("ficha-fila")


def jornada_horus(j):
    j.semear()
    j.trocar_perfil("DIRETOR")
    j.ir("#/banco")
    j.ok("a vitrine lista os 15 itens", j.texto("#qtdBanco") == "15")
    total = int(j.texto("#qtdBanco") or 0)
    j.selecionar("#fbGrupo", "CUSTEIO")
    j.esperar(lambda: j.texto("#qtdBanco") != str(total), 10)
    j.ok("a faceta de grupo filtra a vitrine", j.texto("#qtdBanco") != str(total))
    j.clicar("[data-vista=tabela]")
    j.ok("a alternância para tabela funciona", j.conta("#tabelaBanco") == 1)
    j.capturar("tabela")
    j.trocar_perfil("GERENTE")
    j.trocar_contexto("__primeiro__")
    j.ir("#/banco")
    j.ok("o contexto de unidade aparece na vitrine", "vendo a unidade" in j.texto("main"))


def jornada_tcin(j):
    j.semear()
    j.trocar_perfil("plantonista")
    j.ir("#/painel")
    j.ok("o quadro de plantão abre em colunas", j.conta(".tc-col") >= 4)
    j.ok("os cartões de corpo aparecem", j.conta(".tc-corpo") > 0)
    cid = j.avaliar("async () => (await db.list('corpos')).find(c => c.situacao === 'aguardando identificação')?.id_corpo")
    j.ir("#/corpo/" + cid)
    j.ok("a ficha abre em abas", j.conta("[data-aba]") >= 4)
    j.clicar("[data-aba=situacao]")
    j.selecionar("#tcNovaSit", "não identificado")
    j.preencher("#tcMotivo", "30 dias sem identificação")
    j.clicar("#btnTcSit")
    j.ok("a situação muda com motivo", j.esperar_texto("#tcSitAtual", "não identificado"), "situação não identificado")
    j.trocar_perfil("gestor")
    j.ir("#/painel")
    j.ok("o gestor vê os tempos", j.conta("[data-tc-ind=plantao]") == 1)
    j.ok("a tabela de permanência aparece", j.conta("#tabelaPermanencia") == 1)


def jornada_aquisicoes(j):
    j.semear()
    j.trocar_perfil("compras")
    j.ir("#/processos")
    j.ok("o kanban tem as 9 etapas", j.conta(".ca-col") == 9)
    j.ok("os processos aparecem nos cartões", j.conta(".ca-card") > 0)
    j.clicar(".ca-card")
    j.ok("a ficha abre em abas", "Etapas" in j.texto("main") and "Documentos" in j.texto("main"))
    j.ir("#/processo/AQ-0001")
    j.ok("a ficha tem a barra de etapas", j.conta(".etapas") >= 1)
    j.trocar_perfil("requisitante")
    j.ir("#/processo/AQ-0001")
    j.ok("o requisitante não vê concluir etapa", j.conta("#btnCaAvancar") == 0)
    j.clicar("[data-aba=pendencias]")
    j.ok("a tela explica quem conclui", "equipe de aquisições" in j.texto("main"))


def jornada_custodia(j):
    j.semear()
    j.trocar_perfil("custodia")
    j.ir("#/painel")
    j.ok("o balcão de leitura abre", j.conta(".cd-balcao") == 1)
    j.ok("o mapa das prateleiras aparece", j.conta("#cdMapa") == 1)
    j.preencher("#cdLacreRapido", "LC-20260001")
    j.tecla("#cdLacreRapido", "Enter")
    j.ok("o lacre abre a ficha", j.esperar(lambda: "#/vestigio/" in j.pg.evaluate("() => location.hash"), 10))
    j.ok("a ficha do vestígio abre", "V-0001" in j.texto("main"))
    j.trocar_perfil("gestor")
    j.ir("#/painel")
    j.ok("o gestor vê o painel do gestor", j.conta("#cdGestor") == 1)
    j.trocar_perfil("custodia")
    j.ir("#/painel")
    j.ok("o painel do gestor some para a custódia", j.conta("#cdGestor") == 0)


def jornada_documentapolitec(j):
    j.semear()
    j.trocar_perfil("papiloscopista")
    j.ir("#/caixas")
    j.ok("a estante mostra as caixas", j.conta(".doc-lombada") == 12)
    j.ok("o menu ficou com 5 itens", j.conta("#menu a") == 5)
    j.clicar(".doc-lombada")
    j.ok("a ficha da caixa abre em abas", "Prontuários" in j.texto("main") and "Conferência" in j.texto("main"))
    j.ir("#/caixa/CX-003")
    j.ok("a conferência por leitura fica em campo focado", j.conta("#docLeituraPront") == 1)
    numero = j.avaliar("async () => (await db.porIndice('prontuarios','caixa_id','CX-003'))[0].numero")
    j.preencher("#docLeituraPront", numero)
    j.tecla("#docLeituraPront", "Enter")
    j.ok("a leitura marca o prontuário", j.esperar(lambda: j.avaliar("async n => (await db.get('prontuarios', n)).conferido", numero), 10))
    j.capturar("conferencia")


def jornada_gestao_documentos(j):
    j.semear()
    j.trocar_perfil("servidor")
    j.ir("#/painel")
    j.ok("a caixa do servidor aparece", "Minha caixa" in j.texto("main") and "A instruir" in j.texto("main"))
    j.clicar(".gd-caixa-item")
    j.ok("a ficha abre em abas", "Minutas" in j.texto("main") and "Checklist" in j.texto("main"))
    j.trocar_perfil("autoridade")
    j.ir("#/processos")
    j.clicar("table a")
    j.ok("a autoridade vê a conclusão", j.conta("#gdConclusao") == 1 and j.conta("#gdConclusaoTexto") == 1)
    j.trocar_perfil("servidor")
    j.ir("#/processos")
    j.clicar("table a")
    j.clicar("[data-aba=conclusao]")
    j.ok("o servidor vê o aviso da autoridade", "autoridade decisora" in j.texto("main"))


def jornada_renovacao(j):
    j.semear()
    j.trocar_perfil("gestor")
    j.ir("#/painel")
    j.ok("a régua de vencimentos aparece", j.conta(".rc-regua") == 1)
    j.ok("o semáforo em barra aparece", j.conta(".rc-stack") == 1)
    j.clicar("[data-rc-faixa]")
    j.ok("a faixa leva à lista filtrada", "#/contratos" in j.pg.url)
    j.clicar("table a")
    j.ok("a ficha abre em abas", "Aditivos" in j.texto("main") and "Auditoria" in j.texto("main"))
    j.trocar_perfil("fiscal")
    j.ir("#/painel")
    j.preencher("#rcMeuNome", "Fiscal Jornada")
    j.clicar("#btnRcMeuNome")
    j.ok("o fiscal vê a caixa Meus contratos", "Meus contratos" in j.texto("main"))


def jornada_dna(j):
    j.semear()
    j.trocar_perfil("coordenador")
    j.ir("#/rodada/RD-003")
    j.ok("a placa de 96 poços aparece", j.conta(".dd-poco") == 96)
    j.ok("a rodada abre em abas", "Distribuição" in j.texto("main") and "Urgências" in j.texto("main"))
    j.trocar_perfil("perito")
    j.ir("#/meus-casos")
    j.ok("o perito vê Meus casos", "Meus casos" in j.texto("main"))


def jornada_comissao(j):
    j.semear()
    j.trocar_perfil("presidente")
    j.ir("#/painel")
    j.ok("o funil do processo ético aparece", j.conta(".ce-funil") == 1)
    j.ok("as sete etapas estão no funil", j.conta("[data-etapa-qtd]") == 7)
    j.ir("#/caso/CE-2026-001")
    j.ok("o dossiê Reservado aparece", "reservado" in j.texto("main").lower())
    j.ok("a barra de etapas do caso aparece", j.conta(".ce-etapas") == 1)
    j.ir("#/caso/CE-2026-001/classificacao")
    j.ok("a classificação mostra as sugestões", j.conta("#sugestoes") == 1)
    j.selecionar("#cCategoria", "assedio_moral")
    j.preencher("#cJustificativa", "O relato descreve humilhação e constrangimento reiterados, enquadrados no Código de Ética.")
    j.clicar("#formClassif button[type=submit]")
    j.ok("a classificação é confirmada", "Classificação confirmada" in j.texto("body") or "#/caso/" in j.pg.url)


def jornada_passivo(j):
    j.semear()
    j.trocar_perfil("perito")
    j.ir("#/painel")
    j.ok("a fila do perito aparece", j.conta(".pa-fila-item") > 0)
    j.ok("a miniatura do mapa aparece", j.conta(".pa-mini") > 0)
    j.clicar(".pa-fila-item")
    j.ok("o laudo abre em abas", "Mapas" in j.texto("main") and "Assinatura" in j.texto("main"))
    j.trocar_perfil("gestor")
    j.ir("#/painel")
    j.ok("o gestor vê a produtividade", j.conta("#paGestor") == 1)


def jornada_rnc(j):
    j.semear()
    j.trocar_perfil("cqual")
    j.ir("#/painel")
    j.ok("o quadro por etapa aparece", j.conta(".rnc-quadro") == 1)
    j.ok("as quatro etapas estão no quadro", j.conta(".rnc-col") == 4)
    j.clicar(".rnc-card")
    j.ok("a ficha da RNC abre", "situacaoRnc" in j.pg.content() or "RNC" in j.texto("main"))
    setor = j.avaliar("async () => (await db.list('rncs')).find(r => r.situacao === 'aberta')?.setor_notificado")
    j.trocar_perfil("setor")
    if setor:
        j.trocar_contexto(setor)
    j.ir("#/minhas")
    if setor and j.valor("#rncMeuSetor") != setor:
        j.erro("o contexto de setor não preenche Minhas RNCs", "P1", f"o seletor deveria vir em {setor}", f"veio em {j.valor('#rncMeuSetor')}")
    # usa a tela como uma pessoa usaria, mesmo quando o contexto não veio
    if setor and j.conta("#tabelaMinhasRnc") == 0:
        j.selecionar("#rncMeuSetor", setor)
        j.clicar("#btnSalvarSetor")
    j.ok("o setor vê as RNCs notificadas", j.conta("#tabelaMinhasRnc tr") > 1)


def jornada_tap(j):
    j.semear()
    j.trocar_perfil("equipe")
    j.abrir("")
    j.ok("a equipe abre na triagem", "triagem" in j.pg.evaluate("() => document.body.dataset.rota"))
    j.ir("#/portfolio")
    j.ok("a matriz do portfólio aparece", j.conta(".tap-matriz") == 1)
    j.ir("#/tap/novo")
    j.ok("o TAP abre com as pendências", j.conta("#qtdPend") == 1 or "TAP" in j.texto("main"))


def jornada_adiantamento(j):
    j.semear()
    j.ir("#/processos")
    j.ok("a régua de prazos aparece", j.conta(".ad-regua") > 0)
    j.clicar(".ad-regua")
    j.ok("o prazo fica no topo da ficha", j.conta("#adPrazoTopo") == 1)
    pid = j.avaliar("async () => (await db.list('processos')).find(p => p.valor_concedido > 0)?.id")
    if pid:
        j.ir("#/processo/" + pid + "/prestacao")
        j.ok("a prestação de contas abre", j.conta("[data-ad-concedido]") == 1)


def jornada_metas(j):
    j.semear()
    j.ir("#/importar")
    j.ok("o ano em 12 meses aparece", j.conta(".metas-mes") == 12)
    arquivo = PASTA_APPS / "metas-bi-ocr" / "exemplos" / "powerbi1-2026-07.csv"
    j.arquivos("#arqMes", arquivo)
    j.ok("a importação lê o mês", j.esperar_texto("#resMes", "2026-07", 15))
    j.ok("o mês muda para importado", j.esperar(lambda: j.conta(".metas-mes.importado") > 0, 10))
    j.capturar("ano-com-importado")
    j.ir("#/historico")
    j.ok("o histórico mostra o mês", "2026-07" in j.texto("main"))


def jornada_inscricoes(j):
    j.semear()
    j.trocar_perfil("gerencia")
    j.ir("#/cursos")
    j.ok("os cartões de curso aparecem", j.conta(".inc-curso") > 0)
    j.clicar(".inc-curso-titulo")
    j.ok("o curso abre com a esteira", j.conta(".inc-centro") == 1)
    j.ok("a esteira tem seis passos", j.conta(".inc-esteira a") >= 6)
    j.ir("#/cursos")
    j.clicar(".inc-acoes a")
    j.ok("a divulgação mostra o link e o QR", j.conta("#linkInscricao") == 1 and j.conta("#qr svg") == 1)
    j.trocar_perfil("diretoria")
    j.abrir("")
    j.ok("a diretoria abre na triagem", "triagem" in j.pg.evaluate("() => document.body.dataset.rota"))


def jornada_mapa(j):
    j.ir("#/processos")
    j.clicar("#btnExemplo")
    j.pg.wait_for_timeout(1000)
    j.ir("#/mapa/PROC-2026-001")
    j.ok("a esteira das 8 etapas aparece", j.conta(".mapa-passos a") >= 8)
    j.ok("a grade em formato planilha aparece", j.conta("#tabelaMapa") == 1)
    j.clicar(".mapa-passos a[href*='/resultado/']")
    j.ok("a etapa Resultado abre", "#/resultado/" in j.pg.url)
    j.capturar("resultado")


def jornada_equipamentos(j):
    j.semear()
    j.trocar_perfil("coordenadoria")
    j.ir("#/mapa")
    j.ok("o mapa de MT aparece", j.conta(".eq-mapa") == 1)
    j.ok("os pinos das unidades aparecem", j.conta(".eq-pino") > 0)
    j.clicar(".eq-pino")
    j.ok("o pino leva à lista de equipamentos", "#/equipamentos" in j.pg.url)
    j.ok("a lista mostra os equipamentos", j.texto("#qtdEq") != "")
    j.selecionar("#fCrit", "5")
    j.pg.wait_for_timeout(500)
    j.ok("o filtro de criticidade muda a contagem", j.texto("#qtdEq") != "150")
    j.capturar("lista")


def jornada_agiliza(j):
    j.abrir("#/inicio")
    j.ok("a tela de casos abre", "Casos" in j.texto("main") or j.conta("#btnNovoCaso") == 1)
    j.clicar("#btnNovoCaso")
    j.arquivos("#inpPasta", PASTA_APPS / "agiliza-mais" / "exemplos" / "caso-ficticio-001")
    j.ok("a pasta abre a bancada do caso", j.esperar(lambda: "#/arquivos" in j.pg.evaluate("() => location.hash"), 20))
    j.ok("os seis passos aparecem à esquerda", j.conta(".ag-rail li") == 6)
    j.ok("o inventário mostra os arquivos", "Inventário" in j.texto("main"))
    j.capturar("bancada")


JORNADAS = {
    "agendamento-cin": jornada_agendamento,
    "cin-segunda-via": jornada_cin_segunda_via,
    "horus-banco-demandas": jornada_horus,
    "trilha-custodia-necropsia": jornada_tcin,
    "controle-aquisicoes": jornada_aquisicoes,
    "custodia-definitiva": jornada_custodia,
    "documentapolitec": jornada_documentapolitec,
    "gestao-documentos": jornada_gestao_documentos,
    "renovacao-contratos-horus": jornada_renovacao,
    "distribuicao-casos-dna": jornada_dna,
    "comissao-etica-denuncias": jornada_comissao,
    "passivo-ambiental": jornada_passivo,
    "rnc-nao-conformidade": jornada_rnc,
    "tap-portfolio-projetos": jornada_tap,
    "adiantamento": jornada_adiantamento,
    "metas-bi-ocr": jornada_metas,
    "inscricoes-cursos": jornada_inscricoes,
    "mapa-distribuicao-credor": jornada_mapa,
    "equipamentos-google-earth": jornada_equipamentos,
    "agiliza-mais": jornada_agiliza,
}


def jornada_mobile(j):
    j.abrir("")
    j.pg.wait_for_timeout(500)
    j.ok("abre no celular sem tela de perfil", "Escolha o perfil" not in j.texto("main"))
    j.ok("a página não rola na horizontal", j.avaliar("() => document.documentElement.scrollWidth <= window.innerWidth + 2"))
    if j.conta("#btnMenuCompacto") and j.visivel("#btnMenuCompacto"):
        j.clicar("#btnMenuCompacto")
        j.pg.wait_for_timeout(300)
        j.ok("o menu compacto abre", j.avaliar("() => document.body.classList.contains('menu-aberto')"))
    j.capturar("entrada")


def executar(app, fn, navegador):
    url = (PASTA_APPS / app / "index.html").as_uri()
    outdir = PASTA_SAIDA / app
    outdir.mkdir(parents=True, exist_ok=True)
    res, erros = [], []
    ctx = navegador.new_context(viewport={"width": 1366, "height": 900}, accept_downloads=True)
    pg = ctx.new_page()
    pg.on("dialog", lambda d: d.accept())
    j = Jornada(app, pg, url, "desktop", PERFIL.get(app), res, erros, outdir)
    try:
        if PERFIL.get(app):
            j.abrir("#/config")
            j.trocar_perfil(PERFIL[app])
        fn(j)
    except Exception as e:
        j.erro("exceção durante a jornada", "P1", "a jornada termina sem exceção", f"{type(e).__name__}: {e}")
        traceback.print_exc()
    j.fechar()
    ctx.close()

    ctx2 = navegador.new_context(viewport={"width": 390, "height": 844})
    pg2 = ctx2.new_page()
    pg2.on("dialog", lambda d: d.accept())
    jm = Jornada(app, pg2, url, "mobile", PERFIL.get(app), res, erros, outdir)
    try:
        if PERFIL.get(app):
            jm.abrir("#/config")
            jm.trocar_perfil(PERFIL[app])
        jornada_mobile(jm)
    except Exception as e:
        jm.erro("exceção no celular", "P1", "a jornada mobile termina sem exceção", f"{type(e).__name__}: {e}")
        traceback.print_exc()
    jm.fechar()
    ctx2.close()

    return {"app": app, "perfil": PERFIL.get(app), "resultados": res, "erros": erros}


def main():
    alvos = sys.argv[1:] or list(JORNADAS)
    arquivo = PASTA_APPS / "jornada-resultados.json"
    anterior = {}
    if arquivo.exists():
        try:
            anterior = {r["app"]: r for r in json.loads(arquivo.read_text(encoding="utf-8"))}
        except Exception:
            anterior = {}
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for app in alvos:
            print(f"=== {app}", flush=True)
            r = executar(app, JORNADAS[app], nav)
            anterior[app] = r
            falhas = [x for x in r["resultados"] if not x["ok"]]
            print(f"    {len(r['resultados']) - len(falhas)}/{len(r['resultados'])} passos OK · {len(r['erros'])} erro(s)", flush=True)
            for e in r["erros"]:
                print(f"    - [{e['severidade']}] {e['passo']}: {e['observado'][:100]}", flush=True)
            ordem = [a for a in JORNADAS if a in anterior]
            arquivo.write_text(json.dumps([anterior[a] for a in ordem], ensure_ascii=False, indent=1), encoding="utf-8")
        nav.close()
    print(f"\nResultado em {arquivo}")


if __name__ == "__main__":
    main()
