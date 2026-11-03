"""Testa os formularios de feedback dos 21 apps no Chromium (Playwright).

Para cada app de Apps/equipes.json:
  1. abre Aula 8/feedback/<app>.html por HTTP local (os modulos ES nao rodam por file://);
  2. confere titulo, equipe e a lista de telas contra o app.json;
  3. tenta enviar vazio e exige as mensagens de campo obrigatorio;
  4. preenche, recarrega e confere que o rascunho voltou do localStorage;
  5. poe um CPF no texto e exige o bloqueio;
  6. baixa o .json e confere o conteudo;
  7. com --enviar, envia ao Firestore com o nome "TESTE AUTOMATIZADO ..." e le o
     documento de volta pela API REST (o baixar_feedback.py ignora esse nome).

Uso: python "Aula 8/feedback/testar_formularios.py" [--enviar] [app ...]
     Sem --enviar, a etapa 7 nao roda: as 1 a 6 valem para todos os apps.
"""
import functools
import http.server
import json
import pathlib
import socketserver
import sys
import threading
import urllib.parse
import urllib.request

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parents[2]
FEED = RAIZ / "Aula 8" / "feedback"
APPS = RAIZ / "Apps"
CHAVE = "AIzaSyBmMTIdsrY7sfzgmzzz_5wcaDa0p8kIgVg"  # chave web publica, a mesma de firebase-config.js
REST = "https://firestore.googleapis.com/v1/projects/aulapolitec/databases/(default)/documents/feedback_apps"
FORA = {"#/config", "#/testes"}
PREFIXO = "TESTE AUTOMATIZADO"


class Servidor(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(RAIZ), **k)

    def log_message(self, *a, **k):
        pass


def servidor():
    srv = Servidor(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def ler_doc(doc_id):
    url = f"{REST}/{urllib.parse.quote(doc_id)}?key={CHAVE}"
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def texto(campo):
    """Campo tipado da API REST do Firestore -> valor Python (so string aqui)."""
    return campo.get("stringValue") if isinstance(campo, dict) else None


def testar_app(pg, base, slug, enviar):
    cfg = json.loads((APPS / slug / "app.json").read_text(encoding="utf-8"))
    esperadas = [r for r in cfg["rotas"] if r["rota"] not in FORA]
    falhas, protocolo = [], ""

    pg.goto(f"{base}/Aula%208/feedback/{slug}.html")
    pg.wait_for_selector("#formFeedback", timeout=45000)

    h1 = pg.inner_text("#topo h1").strip()
    if h1 != cfg["titulo"]:
        falhas.append(f"titulo da tela: {h1!r} != {cfg['titulo']!r}")
    if "Equipe:" not in pg.inner_text("#topo"):
        falhas.append("cabecalho sem a equipe")

    telas = pg.locator("#formFeedback .tela")
    if telas.count() != len(esperadas):
        falhas.append(f"{telas.count()} telas no formulario, {len(esperadas)} no app.json")
    rotas = [r.strip() for r in pg.locator("#formFeedback .tela .rota").all_inner_texts()]
    if rotas != [t["rota"] for t in esperadas]:
        falhas.append(f"rotas fora de ordem ou diferentes: {rotas[:4]}...")

    for nome, qtd in (("papel", 3), ("nota", 5), ("usaria", 3)):
        n = pg.locator(f'input[name="{nome}"]').count()
        if n != qtd:
            falhas.append(f"{n} opcoes de {nome}, esperado {qtd}")
        if not pg.locator(f'input[name="{nome}"][required]').count():
            falhas.append(f"{nome} sem required")

    # 3. envio vazio
    pg.click("#btnEnviar")
    pg.wait_for_timeout(200)
    erro = pg.inner_text("#errosForm")
    for msg in ("Informe o seu nome", "Diga se você é da equipe", "Dê a nota", "Diga se usaria"):
        if msg not in erro:
            falhas.append(f"validacao sem a mensagem: {msg!r}")

    # 4. preenche e recarrega (rascunho)
    pg.fill("#nome", f"{PREFIXO} · {slug}")
    pg.fill("#setor", "Teste automatizado")
    pg.check('input[name="papel"][value="equipe"]')
    pg.check('input[name="nota"][value="5"]')
    pg.check('input[name="usaria"][value="ajustes"]')
    if esperadas:
        pg.select_option("#tela_sit_0", "ok")
        pg.fill("#tela_com_0", "Preenchido pelo teste automatizado.")
    pg.fill("#falta", "Itens de teste do formulario.")
    pg.fill("#prio1", "Primeira prioridade de teste")
    pg.fill("#prio2", "Segunda prioridade de teste")
    pg.fill("#prio3", "Terceira prioridade de teste")
    pg.fill("#obs", "Resposta criada por Aula 8/feedback/testar_formularios.py.")

    pg.reload()
    pg.wait_for_selector("#formFeedback", timeout=45000)
    if pg.input_value("#nome") != f"{PREFIXO} · {slug}":
        falhas.append("rascunho nao recuperou o nome")
    if not pg.is_checked('input[name="nota"][value="5"]'):
        falhas.append("rascunho nao recuperou a nota")
    if esperadas and pg.input_value("#tela_com_0") != "Preenchido pelo teste automatizado.":
        falhas.append("rascunho nao recuperou o comentario da tela")

    # 5. CPF no texto
    pg.fill("#falta", "Paciente com CPF 123.456.789-00 no texto.")
    pg.click("#btnEnviar")
    pg.wait_for_timeout(200)
    if "formato de CPF" not in pg.inner_text("#errosForm"):
        falhas.append("CPF no texto nao foi bloqueado")
    pg.fill("#falta", "Itens de teste do formulario.")

    # 6. baixar .json
    with pg.expect_download(timeout=15000) as d:
        pg.click("#btnBaixar")
    arq = d.value
    if arq.suggested_filename != f"feedback-{slug}.json":
        falhas.append(f"nome do .json: {arq.suggested_filename!r}")
    dados = json.loads(pathlib.Path(arq.path()).read_text(encoding="utf-8"))
    if dados.get("app") != slug or not dados.get("aluno", "").startswith(PREFIXO):
        falhas.append(".json sem app ou nome do teste")
    if len(dados.get("telas") or []) != (1 if esperadas else 0):
        falhas.append(f".json com {len(dados.get('telas') or [])} tela(s)")
    if len(dados.get("prioridades") or []) != 3:
        falhas.append(".json sem as 3 prioridades")

    # 7. envio real ao Firestore
    if enviar:
        pg.click("#btnEnviar")
        pg.wait_for_selector("#avisoEnvio .aviso.ok", timeout=60000)
        msg = pg.inner_text("#avisoEnvio")
        resto = msg.split("Protocolo", 1)[-1].strip() if "Protocolo" in msg else ""
        protocolo = "".join(c for c in resto.split()[0] if c.isalnum()) if resto else ""
        if not protocolo:
            falhas.append("envio sem protocolo")
        else:
            try:
                doc = ler_doc(protocolo)
                campos = doc.get("fields", {})
                if texto(campos.get("app")) != slug:
                    falhas.append(f"documento com app {texto(campos.get('app'))!r}")
                if not (texto(campos.get("aluno")) or "").startswith(PREFIXO):
                    falhas.append("documento sem o nome do teste")
                if campos.get("nota", {}).get("integerValue") != "5":
                    falhas.append("documento sem a nota 5")
            except Exception as e:
                falhas.append(f"nao li o documento {protocolo}: {e}")
        if pg.evaluate("localStorage.getItem('feedback:rascunho:' + %r)" % slug):
            falhas.append("rascunho nao foi limpo depois do envio")
        if pg.input_value("#nome"):
            falhas.append("formulario nao foi limpo depois do envio")

    return falhas, len(esperadas), protocolo


def testar_respostas(pg, base):
    pg.goto(f"{base}/Aula%208/feedback/index.html")
    pg.wait_for_selector("#conteudo table", timeout=45000)
    linhas = pg.locator("#conteudo table tr").count()
    if linhas < 22:
        return [f"pagina de respostas com {linhas} linhas, esperado 21 apps + cabecalho"]
    if "Não consegui ler o Firestore" in pg.inner_text("#conteudo"):
        return ["pagina de respostas nao leu o Firestore"]
    return []


def main():
    enviar = "--enviar" in sys.argv
    alvos = [a for a in sys.argv[1:] if not a.startswith("--")]
    equipes = json.loads((APPS / "equipes.json").read_text(encoding="utf-8"))["apps"]
    slugs = sorted(equipes)
    if alvos:
        slugs = [s for s in slugs if s in alvos]

    srv = servidor()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    total_falhas, total_telas, enviados = 0, 0, []
    with sync_playwright() as p:
        nav = p.chromium.launch()
        ctx = nav.new_context(accept_downloads=True)
        pg = ctx.new_page()
        erros_pagina = []
        pg.on("pageerror", lambda e: erros_pagina.append(str(e)))
        for slug in slugs:
            erros_pagina.clear()
            falhas, telas, protocolo = testar_app(pg, base, slug, enviar)
            falhas = erros_pagina[:2] + falhas
            total_falhas += len(falhas)
            total_telas += telas
            if protocolo:
                enviados.append((slug, protocolo))
            estado = "OK" if not falhas else "FALHA"
            extra = f" · protocolo {protocolo}" if protocolo else ""
            print(f"{estado:5s} {slug:28s} {telas:2d} telas{extra}")
            for f in falhas:
                print(f"      - {f}")
        falhas = testar_respostas(pg, base)
        total_falhas += len(falhas)
        print(f"{'OK' if not falhas else 'FALHA':5s} {'(pagina de respostas)':28s}")
        for f in falhas:
            print(f"      - {f}")
        ctx.close()
        nav.close()

    print()
    print(f"{len(slugs)} formulario(s) · {total_telas} telas conferidas · {len(enviados)} envio(s) ao Firestore · {total_falhas} falha(s)")
    if enviados:
        print("Testes gravados (o baixar_feedback.py ignora o prefixo):")
        for slug, protocolo in enviados:
            print(f"  {slug}: {protocolo}")
    srv.shutdown()
    return 1 if total_falhas else 0


if __name__ == "__main__":
    sys.exit(main())
