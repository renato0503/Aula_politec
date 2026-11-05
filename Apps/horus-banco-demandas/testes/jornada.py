"""Jornada do cliente deste app (Playwright).

Roda no Chromium ou em um navegador via CDP, por exemplo o Lightpanda:
    python testes/jornada.py
    python testes/jornada.py --cdp http://127.0.0.1:9222 --base http://127.0.0.1:8000

Sem `--base`, abre o `index.html` por `file://`. Com `--base`, usa
`<base>/horus-banco-demandas/index.html` (necessário no Lightpanda, que roda no WSL).
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

APP = "horus-banco-demandas"
PERFIL = "DIRETOR"

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



def jornada_catalogo(j):
    """Catálogo de unidades (setores) e de unidades de medida, e uma demanda usando as duas."""
    j.trocar_perfil("DIRETOR")
    j.ir("#/config")
    j.preencher("#uNome", "Setor de Catálogo")
    j.preencher("#uSigla", "CAT")
    j.clicar("#btnUnidade")
    j.esperar_texto("#blocoUnidades", "Setor de Catálogo")
    j.ok("cadastra uma unidade (setor) no catálogo", "Setor de Catálogo" in j.texto("#blocoUnidades"))
    j.preencher("#mSigla", "M3")
    j.preencher("#mNome", "metro cúbico")
    j.clicar("#btnMedida")
    j.esperar_texto("#blocoMedidas", "M3")
    j.ok("cadastra uma unidade de medida no catálogo", "M3" in j.texto("#blocoMedidas"))

    j.ir("#/demanda/nova")
    uid = j.avaliar("() => db.list('unidades').then(x => x.find(u => u.sigla === 'CAT').id)")
    mid = j.avaliar("() => db.list('unidades_medida').then(x => x.find(m => m.sigla === 'M3').id)")
    j.selecionar("#dUnidade", uid)
    j.selecionar("#dMedida", mid)
    j.preencher("#dValor", "12,50")
    j.preencher("#dQtd", "4")
    j.preencher("#dEspec", "Material de consumo do setor de catálogo, com especificação técnica acima do mínimo exigido de cinquenta caracteres.")
    j.preencher("#dJust", "Justificativa acima de cem caracteres para atender à regra R2, descrevendo a necessidade do setor de catálogo e a finalidade do item no ciclo do PCA.")
    j.preencher("#dLinks", "https://www.gov.br/compras")
    j.clicar("#formDemanda button[type=submit]")
    j.esperar(lambda: j.avaliar("() => location.hash") == "#/banco", 15)
    j.ok("salva a demanda com a unidade e a medida cadastradas", j.avaliar("() => location.hash") == "#/banco")
    j.ir("#/config")
    j.clicar("[data-excluir-unidade='%s']" % uid)
    j.esperar_texto("#blocoUnidades", "Setor de Catálogo")
    j.ok("bloqueia excluir uma unidade que já está em uso", "Setor de Catálogo" in j.texto("#blocoUnidades"))


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
    outdir = pathlib.Path(tempfile.mkdtemp(prefix="jornada-horus-banco-demandas-"))
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
        jornada_horus(j)
        jornada_catalogo(j)
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
