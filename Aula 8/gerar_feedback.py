"""Gera o formulário de feedback de cada app e a página de respostas.

Para cada app de Apps/equipes.json, lê o Apps/<app>/app.json (título, telas e
descrição) e grava Aula 8/feedback/<app>.html: um HTML pequeno com a
configuração do app, que carrega feedback.css e feedback.js. As respostas vão
para a coleção `feedback_apps` do Firestore (regras em Aula 8/firestore.rules).

Saídas:
  Aula 8/feedback/<app>.html   um formulário por app
  Aula 8/feedback/index.html   respostas por app (para o professor)

Uso: python "Aula 8/gerar_feedback.py"
Depois de mudar telas de um app (app.json), rode de novo.
"""
import html
import json
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
APPS = RAIZ / "Apps"
SAIDA = RAIZ / "Aula 8" / "feedback"
SITE = "https://renato0503.github.io/Aula_politec/"
# telas que não entram no feedback: configuração e testes internos
FORA = {"#/config", "#/testes"}

MODELO = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} | POLITEC/MT</title>
<meta name="description" content="{descricao}">
<link rel="stylesheet" href="feedback.css">
</head>
<body>
<header class="top" id="topo"><div class="wrap"><h1>{titulo}</h1><p>Carregando o formulário…</p></div></header>
<main class="wrap" id="conteudo"><noscript>Ative o JavaScript para responder.</noscript></main>
<footer class="foot"><div class="wrap">Curso de Capacitação POLITEC/MT · Professor Renato Rosa · As respostas vão para o Firestore do curso, sem dado pessoal de caso.</div></footer>
<script>window.FEEDBACK = {config};</script>
<script type="module" src="feedback.js"></script>
</body>
</html>
"""


def equipes():
    dados = json.loads((APPS / "equipes.json").read_text(encoding="utf-8"))["apps"]
    return {slug: ", ".join(a["nome"] for a in v["alunos"]) for slug, v in dados.items()}


def config_do_app(slug, equipe):
    a = json.loads((APPS / slug / "app.json").read_text(encoding="utf-8"))
    telas = [{"rota": r["rota"], "titulo": r["titulo"], "descricao": r.get("descricao", "")}
             for r in a["rotas"] if r["rota"] not in FORA]
    return {"app": slug, "titulo": a["titulo"], "subtitulo": a.get("subtitulo", ""), "equipe": equipe,
            "link_app": f"{SITE}Apps/{slug}/index.html", "link_hub": f"{SITE}Apps/{slug}/processo.html", "telas": telas}


def gravar(nome, titulo, descricao, config):
    texto = MODELO.format(titulo=html.escape(titulo), descricao=html.escape(descricao),
                          config=json.dumps(config, ensure_ascii=False).replace("</", "<\\/"))
    (SAIDA / nome).write_text(texto, encoding="utf-8")


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    resumo = []
    for slug, equipe in sorted(equipes().items()):
        c = config_do_app(slug, equipe)
        gravar(f"{slug}.html", f"Feedback · {c['titulo']}", f"Feedback dos alunos sobre o app {c['titulo']}.", c)
        resumo.append({"app": slug, "titulo": c["titulo"], "equipe": equipe})
        print(f"{slug:28s} {len(c['telas']):2d} telas")
    gravar("index.html", "Feedback dos apps · respostas", "Respostas do feedback dos alunos, por app.",
           {"modo": "respostas", "apps": resumo})
    print(len(resumo), "formulários e a página de respostas em", SAIDA.relative_to(RAIZ))


if __name__ == "__main__":
    main()
