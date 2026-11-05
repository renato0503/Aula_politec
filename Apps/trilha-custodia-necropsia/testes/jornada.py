"""Jornada do cliente deste app (Playwright).

Roda no Chromium ou em um navegador via CDP, por exemplo o Lightpanda:
    python testes/jornada.py
    python testes/jornada.py --cdp http://127.0.0.1:9222 --base http://127.0.0.1:8000

Sem `--base`, abre o `index.html` por `file://`. Com `--base`, usa
`<base>/trilha-custodia-necropsia/index.html` (necessário no Lightpanda, que roda no WSL).
"""
import argparse
import json
import pathlib
import sys
import tempfile
import traceback

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from jornada_lib import Jornada, aceitar_dialogo, PASTA_APPS  # noqa: E402

APP = "trilha-custodia-necropsia"
PERFIL = "tecnico"

def jornada_tcin(j):
    j.semear()
    j.trocar_perfil("tecnico")
    j.ir("#/painel")
    j.ok("o painel mostra os dez indicadores", j.conta("#espKpiGrid .esp-kpi") == 10)
    j.ok("o quadro das sete etapas abre em colunas", j.conta(".esp-coluna") == 7)
    j.ok("os cartões de corpo aparecem", j.conta(".esp-cartao") > 0)
    cid = j.avaliar("async () => (await db.list('corpos')).find(c => c.etapa === 5)?.id_corpo")
    j.ir("#/corpo/" + cid)
    j.ok("a ficha mostra o stepper das sete etapas", j.conta(".esp-passo") == 7)
    j.ok("a etapa da identificação aparece", j.conta("#espEtapa5") == 1)
    j.ok("o histórico do caso aparece", j.conta("#espHistorico .esp-timeline li") > 0)
    j.ir("#/corpos")
    j.ok("a lista traz os corpos", j.conta(".esp-tabela tbody tr") == 10)
    j.clicar("[data-esp-acao=esp-ver-detalhes]")
    j.pg.wait_for_timeout(500)
    j.ok("a gaveta lateral abre com a ficha", j.conta(".esp-gaveta") == 1)
    j.pg.keyboard.press("Escape")
    j.pg.wait_for_timeout(400)
    j.ok("a tecla Escape fecha a gaveta", j.conta(".esp-gaveta") == 0)
    j.trocar_perfil("gestor")
    j.ir("#/painel")
    j.ok("o gestor vê a fila da ADM", j.conta("[data-esp-adm=lacres]") == 1)
    j.ok("a fila da ADM lista as pendências", j.conta("#espFilaAdm, .esp-tabela tbody tr") > 0)



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


def executar(navegador, url, cdp):
    outdir = pathlib.Path(tempfile.mkdtemp(prefix="jornada-trilha-custodia-necropsia-"))
    res, erros = [], []
    ctx = navegador.new_context(viewport={"width": 1366, "height": 900}, accept_downloads=True)
    ctx.add_init_script("try { window.confirm = () => true; } catch (e) {}")
    pg = ctx.new_page()
    pg.on("dialog", aceitar_dialogo)
    j = Jornada(APP, pg, url, "desktop", PERFIL, res, erros, outdir)
    try:
        if PERFIL:
            j.abrir("#/config")
            j.trocar_perfil(PERFIL)
        jornada_tcin(j)
    except Exception as e:
        j.erro("exceção durante a jornada", "P1", "a jornada termina sem exceção", f"{type(e).__name__}: {e}")
        traceback.print_exc()
    j.fechar()
    ctx.close()

    ctx2 = navegador.new_context(viewport={"width": 390, "height": 844})
    ctx2.add_init_script("try { window.confirm = () => true; } catch (e) {}")
    pg2 = ctx2.new_page()
    pg2.on("dialog", aceitar_dialogo)
    jm = Jornada(APP, pg2, url, "mobile", PERFIL, res, erros, outdir)
    try:
        if PERFIL:
            jm.abrir("#/config")
            jm.trocar_perfil(PERFIL)
        jornada_mobile(jm)
    except Exception as e:
        jm.erro("exceção no celular", "P1", "a jornada mobile termina sem exceção", f"{type(e).__name__}: {e}")
        traceback.print_exc()
    jm.fechar()
    ctx2.close()
    return res, erros, outdir


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cdp", default="", help="URL do servidor CDP (ex.: http://127.0.0.1:9222)")
    ap.add_argument("--base", default="", help="URL base HTTP (ex.: http://127.0.0.1:8000)")
    args = ap.parse_args()
    url = (args.base.rstrip("/") + "/" + APP + "/index.html") if args.base else (PASTA_APPS / "index.html").as_uri()
    with sync_playwright() as p:
        if args.cdp:
            navegador = p.chromium.connect_over_cdp(args.cdp)
        else:
            navegador = p.chromium.launch()
        res, erros, outdir = executar(navegador, url, args.cdp)
        if not args.cdp:
            navegador.close()
    falhas = [x for x in res if not x["ok"]]
    saida = {"app": APP, "url": url, "cdp": args.cdp, "resultados": res, "erros": erros, "capturas": str(outdir)}
    destino = pathlib.Path(tempfile.gettempdir()) / ("jornada-" + APP + ".json")
    destino.write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(("OK   " if not erros else "FALHA"), APP, f"{len(res) - len(falhas)}/{len(res)} passos", f"{len(erros)} erro(s)")
    for e in erros:
        print("      -", e["severidade"], e["passo"], "·", e["observado"][:120])
    print("saída:", destino)
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
