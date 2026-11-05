"""Apoio da jornada do cliente (Playwright).

Cada app tem uma função de jornada em `Apps/jornada.py`. Esta biblioteca cuida
do contexto do navegador, das esperas, das capturas, do console/rede e do
registro dos erros no formato do `JORNADA-BACKLOG.md`.

Uso: importado por `Apps/jornada.py`.
"""
import json
import pathlib
import re
import time

PASTA_APPS = pathlib.Path(__file__).resolve().parent.parent
PASTA_SAIDA = PASTA_APPS / "_testes" / "jornada"


def slug(texto):
    texto = re.sub(r"[^a-zA-Z0-9]+", "-", texto).strip("-").lower()
    return texto[:60] or "passo"


def aceitar_dialogo(dialogo):
    """Aceita o confirm() sem derrubar a conexão quando o navegador (Lightpanda)
    já fechou o diálogo."""
    try:
        dialogo.accept()
    except Exception:
        pass


class Jornada:
    def __init__(self, app, pg, url, viewport, perfil, resultados, erros, outdir):
        self.app = app
        self.pg = pg
        self.url = url
        self.viewport = viewport
        self.perfil = perfil
        self.resultados = resultados
        self.erros = erros
        self.outdir = outdir
        self.console = []
        self.rede = []
        self.origem = url.rsplit("/", 1)[0] if "/" in url else url
        self._passo_atual = ""
        pg.on("pageerror", lambda e: self.console.append(f"pageerror: {e}"))
        pg.on("console", lambda m: self.console.append(m.text) if m.type == "error" else None)
        pg.on("request", lambda r: self.rede.append(r.url) if not r.url.startswith(("file:", "data:", "blob:")) and not r.url.startswith(self.origem) else None)

    # ---------- navegação e espera ----------
    def abrir(self, rota="", espera=500):
        self.pg.goto(self.url + rota)
        self.pg.wait_for_timeout(espera)
        try:
            self.pg.wait_for_function("() => typeof db === 'undefined' || !!db.con", timeout=15000)
        except Exception:
            pass
        self.pg.wait_for_timeout(200)

    def ir(self, rota, espera=400):
        self.abrir(rota, espera)

    def esperar(self, cond, timeout=20, intervalo=200):
        fim = time.time() + timeout
        while time.time() < fim:
            try:
                if cond():
                    return True
            except Exception:
                pass
            self.pg.wait_for_timeout(intervalo)
        return False

    def esperar_texto(self, seletor, texto, timeout=20):
        return self.esperar(lambda: texto in self.texto(seletor), timeout)

    def esperar_seletor(self, seletor, timeout=20):
        try:
            self.pg.wait_for_selector(seletor, timeout=timeout * 1000)
            return True
        except Exception:
            return False

    # ---------- leitura e ação ----------
    def texto(self, seletor="main"):
        try:
            return self.pg.inner_text(seletor)
        except Exception:
            return ""

    def valor(self, seletor):
        try:
            return self.pg.input_value(seletor)
        except Exception:
            return ""

    def conta(self, seletor):
        return self.pg.locator(seletor).count()

    def visivel(self, seletor):
        try:
            return self.pg.locator(seletor).first.is_visible()
        except Exception:
            return False

    def clicar(self, seletor, espera=300):
        self.pg.locator(seletor).first.click()
        self.pg.wait_for_timeout(espera)

    def preencher(self, seletor, valor):
        self.pg.fill(seletor, str(valor))

    def selecionar(self, seletor, valor):
        self.pg.select_option(seletor, str(valor))

    def checar(self, seletor):
        self.pg.check(seletor)

    def deschecar(self, seletor):
        self.pg.uncheck(seletor)

    def tecla(self, seletor, tecla):
        self.pg.locator(seletor).first.press(tecla)

    def arquivos(self, seletor, caminho):
        self.pg.set_input_files(seletor, str(caminho))

    def avaliar(self, expressao, arg=None):
        return self.pg.evaluate(expressao, arg)

    # ---------- perfil ----------
    def trocar_perfil(self, perfil):
        if not self.pg.locator("#btnPerfil").count():
            return False
        self.pg.click("#btnPerfil")
        self.pg.wait_for_timeout(150)
        item = self.pg.locator(f"#perfilLista [data-escolher-perfil='{perfil}']")
        if not item.count():
            self.pg.keyboard.press("Escape")
            return False
        item.first.click()
        self.pg.wait_for_timeout(500)
        self.perfil = perfil
        return True

    def trocar_contexto(self, valor):
        if not self.pg.locator("#btnPerfil").count():
            return False
        self.pg.click("#btnPerfil")
        self.pg.wait_for_timeout(150)
        if not self.pg.locator("#perfilContexto").count():
            self.pg.keyboard.press("Escape")
            return False
        if valor == "__primeiro__":
            self.pg.select_option("#perfilContexto", index=1)
        else:
            self.pg.select_option("#perfilContexto", valor)
        self.pg.wait_for_timeout(500)
        return True

    # ---------- dados fictícios ----------
    def semear(self):
        self.ir("#/config", 300)
        if not self.pg.locator("#btnSeed").count():
            return False
        self.pg.click("#btnSeed")
        if self.pg.evaluate("() => !!(APP.db.stores && APP.db.stores.log)"):
            self.esperar(lambda: self.pg.evaluate("async () => (await db.list('log')).some(l => String(l.acao || '').startsWith('dados fictícios'))"), 30)
        else:
            self.esperar(lambda: "Dados fictícios carregados" in self.texto("body"), 30)
        self.pg.wait_for_timeout(300)
        self.pg.reload()
        self.pg.wait_for_timeout(600)
        try:
            self.pg.wait_for_function("() => typeof db !== 'undefined' && !!db.con", timeout=15000)
        except Exception:
            pass
        return True

    # ---------- registro ----------
    def ok(self, passo, cond, esperado="", observado="", severidade="P1"):
        cond = bool(cond)
        self.resultados.append({"passo": passo, "ok": cond, "esperado": esperado, "observado": observado or ("" if cond else self.texto("main")[:180])})
        if not cond:
            self.erro(passo, severidade, esperado, observado)
        return cond

    def erro(self, passo, severidade, esperado, observado="", captura=True):
        nome = slug(passo)
        if captura:
            try:
                self.capturar(nome)
            except Exception:
                pass
        self.erros.append({
            "id": f"{self.app}-{len(self.erros) + 1:02d}",
            "app": self.app,
            "severidade": severidade,
            "perfil": self.perfil,
            "viewport": self.viewport,
            "rota": self.pg.evaluate("() => location.hash || '(sem hash)'"),
            "passo": passo,
            "esperado": esperado,
            "observado": observado or self.texto("main")[:240],
            "console": list(self.console[-4:]),
            "rede": list(self.rede[-4:]),
            "screenshot": str(self.capturar_nome(nome)),
        })

    def capturar_nome(self, nome):
        return self.outdir / f"{self.viewport}-{slug(nome)}.png"

    def capturar(self, nome):
        destino = self.capturar_nome(nome)
        self.pg.screenshot(path=str(destino), full_page=True)
        return destino

    def fechar(self):
        if self.console:
            self.erro("erros no console", "P2", "nenhum erro de console", "; ".join(self.console[:3]), captura=False)
        if self.rede:
            self.erro("requisições de rede", "P2", "nenhuma requisição de rede", "; ".join(self.rede[:3]), captura=False)
