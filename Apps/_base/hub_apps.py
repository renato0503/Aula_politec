"""Gera o hub dos apps (Apps/index.html) a partir de app.json, equipes.json e sprint.md.

Uso: python Apps/_base/hub_apps.py
"""
import html
import json
import pathlib
import re

APPS = pathlib.Path(__file__).resolve().parent.parent
e = json.loads((APPS / "equipes.json").read_text(encoding="utf-8"))


def sprints(pasta):
    t = (pasta / "sprint.md").read_text(encoding="utf-8")
    feitos = sorted({int(x) for x in re.findall(r"(?m)^\| (\d) \| Feito", t)})
    return f"Sprints {min(feitos)}-{max(feitos)}" if feitos else "Sprint 1"


linhas = []
for pasta in sorted(p for p in APPS.iterdir() if (p / "app.json").exists()):
    cfg = json.loads((pasta / "app.json").read_text(encoding="utf-8"))
    time_ = e["apps"].get(pasta.name, {}).get("alunos", [])
    quem = ", ".join(a["nome"] for a in time_) or "equipe a confirmar"
    rotas = len(cfg.get("rotas", []))
    linhas.append(f"""    <a class="card" href="{pasta.name}/index.html">
      <span class="dia">{html.escape(sprints(pasta))} · {rotas} rotas</span>
      <h3>{html.escape(cfg["titulo"])}</h3>
      <p>{html.escape(cfg.get("descricao", ""))}</p>
      <small>{html.escape(quem)}</small>
      <span class="abrir">Abrir o app &rarr;</span>
    </a>""")

pagina = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Apps dos grupos · POLITEC/MT</title>
<meta name="description" content="Mini apps construídos pelos grupos da Capacitação POLITEC/MT: 19 projetos, offline first, com dados fictícios.">
<style>
:root{{--bg:#f6f4ef;--surface:#fff;--ink:#1c1a17;--soft:#5c574f;--line:#e2ddd2;--accent:#0f766e}}
@media (prefers-color-scheme:dark){{:root{{--bg:#141412;--surface:#1d1c19;--ink:#f2efe8;--soft:#b5afa3;--line:#33302a;--accent:#2dd4bf}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,Segoe UI,Roboto,sans-serif}}
.wrap{{max-width:1120px;margin:0 auto;padding:40px 20px 60px}}
.kicker{{color:var(--accent);font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:12px}}
h1{{font-size:clamp(28px,4vw,44px);line-height:1.1;margin:8px 0 12px;letter-spacing:-.02em}}
.sub{{color:var(--soft);max-width:760px;margin:0 0 8px}}
.meta{{color:var(--soft);font-size:14px;margin:18px 0 28px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
.card{{display:flex;flex-direction:column;gap:8px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px;text-decoration:none;color:inherit;border-top:4px solid var(--accent)}}
.card:hover{{border-color:var(--accent)}}
.card .dia{{font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--accent)}}
.card h3{{margin:0;font-size:19px;letter-spacing:-.01em}}
.card p{{margin:0;color:var(--soft);font-size:14.5px}}
.card small{{color:var(--soft);font-size:12.5px}}
.abrir{{margin-top:auto;font-weight:700;font-size:14px;color:var(--accent)}}
footer{{margin-top:36px;color:var(--soft);font-size:13.5px;border-top:1px solid var(--line);padding-top:18px}}
a{{color:var(--accent)}}
</style>
</head>
<body>
<main class="wrap">
  <div class="kicker">Capacitação POLITEC/MT · fase 2</div>
  <h1>Apps dos grupos</h1>
  <p class="sub">Cada projeto saiu do formulário da Aula 8 e virou um app de um único arquivo:
    abre no navegador, funciona sem internet, guarda os dados no próprio computador e usa
    apenas dados fictícios. As decisões continuam com as pessoas.</p>
  <p class="meta"><a href="../index.html">&larr; Voltar ao hub do curso</a> · 19 projetos ·
    fonte dos contatos e logins: <code>Apps/equipes.json</code></p>
  <div class="grid">
{chr(10).join(linhas)}
  </div>
  <footer>Para editar um app, mexa nas fontes (<code>app.json</code>, <code>src/</code>)
    e rode <code>python Apps/_base/construir.py &lt;app&gt;</code>. O <code>index.html</code> é gerado.
    Guia completo em <a href="README.md">Apps/README.md</a>.</footer>
</main>
</body>
</html>
"""
(APPS / "index.html").write_text(pagina, encoding="utf-8")
print(f"Apps/index.html: {len(linhas)} apps")
