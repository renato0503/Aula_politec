"""Jornada do cliente do TEIA (Playwright).

Uso:
    python testes/jornada.py
    python testes/jornada.py --cdp http://127.0.0.1:9222 --base http://127.0.0.1:8000
"""
import argparse, json, pathlib, sys, tempfile, traceback
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from jornada_lib import Jornada, aceitar_dialogo, PASTA_APPS  # noqa: E402

APP = "teia-triagem-emails"
PERFIL = "triador"


def jornada_teia(j):
    j.semear()
    j.abrir("#/painel")
    j.ok("a bancada abre com a fila", j.conta("[data-te-email]") == 10)
    j.ok("o detalhe mostra os 8 campos", j.conta(".te-form .campo") == 8)
    j.clicar("[data-te-email=EM-006]")
    j.ok("o e-mail urgente abre com os campos", j.conta("#btnTeValidar") == 1)
    j.clicar("#btnTeValidar")
    j.ok("a requisição completa é validada", j.avaliar("async () => (await db.get('emails','EM-006')).status") == "validado")
    j.clicar("[data-te-email=EM-003]")
    j.ok("o e-mail com campo faltando não valida", j.pg.locator("#btnTeValidar").is_disabled())
    j.preencher("#te_protocolo", "2026.9999-DNA")
    j.clicar("#btnTeSalvar")
    j.clicar("#btnTeValidar")
    j.ok("com o campo preenchido, a requisição é validada", j.avaliar("async () => (await db.get('emails','EM-003')).status") == "validado")
    j.ir("#/planilha")
    j.ok("a planilha lista os e-mails e os campos", j.conta("#tabelaTeia tr") == 11 and j.conta("#tabelaTeia th") == 11)
    j.capturar("planilha")


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


def executar(navegador, url):
    outdir = pathlib.Path(tempfile.mkdtemp(prefix="jornada-teia-"))
    res, erros = [], []
    ctx = navegador.new_context(viewport={"width": 1366, "height": 900}, accept_downloads=True)
    ctx.add_init_script("try { window.confirm = () => true; } catch (e) {}")
    pg = ctx.new_page(); pg.on("dialog", aceitar_dialogo)
    j = Jornada(APP, pg, url, "desktop", PERFIL, res, erros, outdir)
    try:
        j.abrir("#/config"); j.trocar_perfil(PERFIL); jornada_teia(j)
    except Exception as e:
        j.erro("exceção durante a jornada", "P1", "a jornada termina sem exceção", f"{type(e).__name__}: {e}"); traceback.print_exc()
    j.fechar(); ctx.close()
    ctx2 = navegador.new_context(viewport={"width": 390, "height": 844})
    ctx2.add_init_script("try { window.confirm = () => true; } catch (e) {}")
    pg2 = ctx2.new_page(); pg2.on("dialog", aceitar_dialogo)
    jm = Jornada(APP, pg2, url, "mobile", PERFIL, res, erros, outdir)
    try:
        jm.abrir("#/config"); jm.trocar_perfil(PERFIL); jornada_mobile(jm)
    except Exception as e:
        jm.erro("exceção no celular", "P1", "a jornada mobile termina sem exceção", f"{type(e).__name__}: {e}"); traceback.print_exc()
    jm.fechar(); ctx2.close()
    return res, erros, outdir


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cdp", default="")
    ap.add_argument("--base", default="")
    args = ap.parse_args()
    url = (args.base.rstrip("/") + "/" + APP + "/index.html") if args.base else (PASTA_APPS / "index.html").as_uri()
    with sync_playwright() as p:
        navegador = p.chromium.connect_over_cdp(args.cdp) if args.cdp else p.chromium.launch()
        res, erros, outdir = executar(navegador, url)
        if not args.cdp: navegador.close()
    falhas = [x for x in res if not x["ok"]]
    destino = pathlib.Path(tempfile.gettempdir()) / ("jornada-" + APP + ".json")
    destino.write_text(json.dumps({"app": APP, "url": url, "cdp": args.cdp, "resultados": res, "erros": erros, "capturas": str(outdir)}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(("OK   " if not erros else "FALHA"), APP, f"{len(res)-len(falhas)}/{len(res)} passos", f"{len(erros)} erro(s)")
    for e in erros: print("      -", e["severidade"], e["passo"], "·", e["observado"][:120])
    print("saída:", destino)
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
