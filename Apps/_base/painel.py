"""Gera o painel de desenvolvimento dos apps (Apps/painel.html).

Le app.json, src/*.js, sprint.md, equipes.json e os dados fictícios. Não abre
navegador: as telas são conferidas pelas chaves `TELAS[...]` do código e o
`#/config` (que vem da base comum). Uso:
  python Apps/_base/painel.py
"""
import datetime as dt
import html
import json
import pathlib
import re

APPS = pathlib.Path(__file__).resolve().parent.parent
RAIZ = APPS.parent
EQUIPES = json.loads((APPS / "equipes.json").read_text(encoding="utf-8"))
RE_TELAS = re.compile(r"""TELAS\[["']([^"']+)["']\]""")
RE_TELAS_DOT = re.compile(r"""TELAS\.([A-Za-z0-9_]+)\s*=""")
TELAS_BASE = {"#/config"}


def ler_telas(pasta):
    achadas = set(TELAS_BASE)
    for f in (pasta / "src").glob("*.js"):
        t = f.read_text(encoding="utf-8")
        achadas |= set(RE_TELAS.findall(t))
        achadas |= set(RE_TELAS_DOT.findall(t))
    return achadas


def ler_sprints(pasta):
    t = (pasta / "sprint.md").read_text(encoding="utf-8")
    feitos = sorted({int(x) for x in re.findall(r"(?m)^\| (\d+) \| Feito", t)})
    parciais = sorted({int(x) for x in re.findall(r"(?m)^\| (\d+) \| Parcial", t)})
    abertos = len(re.findall(r"(?m)^- \[ \]", t))
    s0 = t.split("## Sprint 1")[0] if "## Sprint 1" in t else t
    s0_abertos = len(re.findall(r"(?m)^- \[ \]", s0))
    return feitos, parciais, abertos, s0_abertos


def ler_seed(pasta):
    arq = pasta / "exemplos/seed.json"
    if not arq.exists():
        return 0
    try:
        d = json.loads(arq.read_text(encoding="utf-8"))
        return sum(len(v) for v in d.values() if isinstance(v, list))
    except Exception:  # noqa: BLE001
        return 0


def docs_faltando(pasta):
    exigidos = ["README.md", "PROJETO.md", "contexto.md", "sprint.md", "projeto.json",
                "app.json", "src/app.js", "exemplos/seed.json", "index.html"]
    return [f for f in exigidos if not (pasta / f).exists()]


def grupo(feitos, parciais):
    if 4 in parciais:
        return "s4p"
    if feitos and max(feitos) >= 3:
        return "s3"
    return "s2"


def rotulo(g, feitos):
    if g == "s4p":
        return "Sprint 4 parcial"
    return f"Sprints 1–{max(feitos)}" if feitos else "Sprint 1"


apps, pendentes_sprint = [], {}
for pasta in sorted(p for p in APPS.iterdir() if (p / "app.json").exists()):
    cfg = json.loads((pasta / "app.json").read_text(encoding="utf-8"))
    src = "\n".join(f.read_text(encoding="utf-8") for f in (pasta / "src").glob("*.js"))
    telas = ler_telas(pasta)
    rotas = [r["rota"] for r in cfg.get("rotas", [])]
    sem_tela = [r for r in cfg.get("rotas", []) if r["rota"] not in telas]
    for r in sem_tela:
        pendentes_sprint.setdefault(int(r.get("sprint", 1)), []).append((pasta.name, r["rota"]))
    feitos, parciais, abertos, s0 = ler_sprints(pasta)
    equipe = EQUIPES["apps"].get(pasta.name, {}).get("alunos", [])
    quem = ", ".join(a["nome"] for a in equipe) or "a confirmar"
    github = [a["github"] for a in equipe if a["github"]]
    g = grupo(feitos, parciais)
    apps.append({
        "nome": pasta.name, "titulo": cfg["titulo"], "equipe": quem, "github": github,
        "rotas": len(rotas), "telas": len([r for r in rotas if r in telas]), "sem_tela": sem_tela,
        "feitos": feitos, "parciais": parciais, "abertos": abertos, "s0": s0,
        "seed": ler_seed(pasta), "testes": len(re.findall(r"\bteste\(", src)),
        "regras": len(set(re.findall(r"\b(RN\d+|R\d+)\b", src))), "linhas": len(src.splitlines()),
        "grupo": g, "rotulo": rotulo(g, feitos), "faltando": docs_faltando(pasta),
    })

total_rotas = sum(a["rotas"] for a in apps)
total_telas = sum(a["telas"] for a in apps)
total_pend = total_rotas - total_telas
total_abertos = sum(a["abertos"] for a in apps)
total_s0 = sum(a["s0"] for a in apps)
total_alunos = sum(len(d["alunos"]) for d in EQUIPES["apps"].values())
total_github = sum(1 for d in EQUIPES["apps"].values() for a in d["alunos"] if a["github"])
sem_github = [a["nome"] for d in EQUIPES["apps"].values() for a in d["alunos"] if not a["github"]]
bi = RAIZ / "Aula 8/Entregas BI"
n_bi = len(list(bi.glob("*.pbix"))) + len(list(bi.glob("*.pbip")))
atualizado = dt.date.today().strftime("%d/%m/%Y")

cards = [
    (str(len(apps)), "apps"),
    (f"{total_telas}/{total_rotas}", "telas prontas"),
    (str(total_pend), "telas no placeholder"),
    (str(total_s0), "itens do Sprint 0 abertos"),
    (f"{total_github}/{total_alunos}", "alunos com GitHub"),
    (str(n_bi), "trabalhos de BI"),
]

linhas = []
for a in apps:
    busca = (a["nome"] + " " + a["titulo"] + " " + a["equipe"]).lower()
    pct = round(a["telas"] / a["rotas"] * 100) if a["rotas"] else 0
    pend = "".join(f"<li><code>{html.escape(r['rota'])}</code> <span class='silencioso'>Sprint {r.get('sprint', 1)}</span></li>" for r in a["sem_tela"])
    gh = ", ".join(f"<code>{html.escape(x)}</code>" for x in a["github"]) or "<span class='alerta'>sem GitHub</span>"
    falta = ("<p class='alerta'>Falta: " + ", ".join(html.escape(x) for x in a["faltando"]) + "</p>") if a["faltando"] else ""
    linhas.append(f"""<details class="app" data-grupo="{a['grupo']}" data-busca="{html.escape(busca)}">
  <summary>
    <span class="nome"><b>{html.escape(a['titulo'])}</b><small>{html.escape(a['nome'])} · {html.escape(a['equipe'])}</small></span>
    <span class="selo g-{a['grupo']}">{html.escape(a['rotulo'])}</span>
    <span class="barra"><span style="width:{pct}%"></span></span>
    <span class="num">{a['telas']}/{a['rotas']}</span>
    <span class="num pend">{len(a['sem_tela'])}</span>
  </summary>
  <div class="corpo">
    <div class="colunas">
      <div><h4>O que falta</h4>{'<ul>' + pend + '</ul>' if pend else '<p class="ok">Todas as rotas declaradas têm tela.</p>'}{falta}</div>
      <div><h4>Números</h4><p>{a['linhas']} linhas de código · {a['testes']} testes embutidos · {a['regras']} regras citadas<br>
        {a['seed']} registros fictícios · {a['abertos']} itens abertos no sprint.md (Sprint 0: {a['s0']})</p>
        <p><b>GitHub:</b> {gh}</p></div>
    </div>
    <p class="links"><a href="{a['nome']}/index.html">Abrir o app</a> ·
      <a href="{a['nome']}/README.md">README</a> ·
      <a href="{a['nome']}/PROJETO.md">PROJETO</a> ·
      <a href="{a['nome']}/sprint.md">sprint.md</a></p>
  </div>
</details>""")

blocos_sprint = []
for s in sorted(pendentes_sprint):
    itens = pendentes_sprint[s]
    nomes = "".join(f"<li><b>{html.escape(app)}</b> · <code>{html.escape(rota)}</code></li>" for app, rota in itens)
    blocos_sprint.append(f"<details><summary>Sprint {s} <span class='num'>{len(itens)}</span></summary><ul>{nomes}</ul></details>")

html_doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Painel de desenvolvimento · Apps POLITEC</title>
<style>
:root{{--bg:#f6f4ef;--surface:#fff;--ink:#1c1a17;--soft:#5c574f;--line:#e2ddd2;--accent:#0f766e;--ok:#15803d;--alerta:#b45309;--erro:#b91c1c}}
@media (prefers-color-scheme:dark){{:root{{--bg:#141412;--surface:#1d1c19;--ink:#f2efe8;--soft:#b5afa3;--line:#33302a;--accent:#2dd4bf;--ok:#4ade80;--alerta:#fbbf24;--erro:#f87171}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,Segoe UI,Roboto,sans-serif}}
.wrap{{max-width:1180px;margin:0 auto;padding:36px 18px 60px}}
.kicker{{color:var(--accent);font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:12px}}
h1{{font-size:clamp(26px,4vw,40px);margin:6px 0 8px;letter-spacing:-.02em}}
h2{{margin:34px 0 10px;font-size:20px}}h4{{margin:12px 0 6px;font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--soft)}}
.sub{{color:var(--soft);margin:0 0 18px}}.silencioso{{color:var(--soft);font-size:12px}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:18px 0 8px}}
.kpi{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px}}
.kpi b{{display:block;font-size:24px;line-height:1.1}}.kpi span{{color:var(--soft);font-size:12.5px}}
.controles{{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:22px 0 12px}}
.controles input{{flex:1;min-width:220px;padding:9px 12px;border:1px solid var(--line);border-radius:9px;background:var(--surface);color:var(--ink)}}
.controles button{{padding:8px 12px;border:1px solid var(--line);border-radius:9px;background:var(--surface);color:var(--ink);cursor:pointer}}
.controles button.ativo{{border-color:var(--accent);color:var(--accent);font-weight:700}}
details.app{{background:var(--surface);border:1px solid var(--line);border-radius:12px;margin:8px 0}}
details.app>summary{{display:grid;grid-template-columns:minmax(220px,2.4fr) 130px minmax(80px,1fr) 46px 46px;gap:12px;align-items:center;padding:12px 14px;cursor:pointer;list-style:none}}
details.app>summary::-webkit-details-marker{{display:none}}
details.app .nome b{{display:block}}details.app .nome small{{color:var(--soft);font-size:12px}}
.selo{{font-size:11px;font-weight:700;padding:3px 8px;border-radius:999px;text-align:center;white-space:nowrap}}
.g-s3{{background:rgba(21,128,61,.15);color:var(--ok)}}.g-s2{{background:rgba(15,118,110,.15);color:var(--accent)}}.g-s4p{{background:rgba(180,83,9,.15);color:var(--alerta)}}
.barra{{height:7px;background:var(--line);border-radius:999px;overflow:hidden}}.barra span{{display:block;height:100%;background:var(--accent)}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}.pend{{color:var(--erro);font-weight:700}}
.corpo{{padding:0 14px 14px;border-top:1px solid var(--line)}}
.colunas{{display:grid;grid-template-columns:1.5fr 1fr;gap:22px}}
.corpo ul{{margin:4px 0 0 18px;padding:0}}.corpo li{{margin:3px 0}}
.ok{{color:var(--ok)}}.alerta{{color:var(--erro)}}
.links a{{color:var(--accent);font-weight:600}}a{{color:var(--accent)}}
.bloco{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:8px 14px}}
.bloco details{{border-top:1px solid var(--line);padding:8px 0}}.bloco details:first-child{{border-top:0}}
.bloco summary{{cursor:pointer;font-weight:600}}
footer{{margin-top:34px;border-top:1px solid var(--line);padding-top:16px;color:var(--soft);font-size:13px}}
@media (max-width:760px){{details.app>summary{{grid-template-columns:1fr 110px}}.barra,.num.pend{{display:none}}.colunas{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<main class="wrap">
  <div class="kicker">Capacitação POLITEC/MT · fase 2</div>
  <h1>Painel de desenvolvimento dos apps</h1>
  <p class="sub">Visão global dos {len(apps)} projetos construídos a partir das entregas da Aula 8.
    A tela pronta é conferida pelas rotas implementadas no código; o restante aparece como placeholder do sprint.
    Atualizado em {atualizado}.</p>
  <div class="kpis">{''.join(f'<div class="kpi"><b>{v}</b><span>{r}</span></div>' for v, r in cards)}</div>

  <div class="controles">
    <input id="busca" type="search" placeholder="Buscar por app, projeto ou aluno...">
    <button data-f="todos" class="ativo">Todos</button>
    <button data-f="s3">Sprints 1–3</button>
    <button data-f="s2">Sprints 1–2</button>
    <button data-f="s4p">Sprint 4 parcial</button>
  </div>
  <p class="sub" id="contador"></p>

  {''.join(linhas)}

  <h2>O que falta, por sprint</h2>
  <div class="bloco">{''.join(blocos_sprint) if blocos_sprint else '<p class="ok">Nenhuma rota pendente.</p>'}</div>

  <h2>Cadastro, BI e publicação</h2>
  <div class="bloco">
    <p><b>Alunos sem GitHub:</b> {html.escape(', '.join(sem_github)) if sem_github else 'nenhum'}.</p>
    <p><b>Trabalhos de BI:</b> {n_bi} arquivos em <code>Aula 8/Entregas BI/</code>.
      <a href="../Aula%208/Entregas%20BI/README.md">Índice do BI</a> (o Firebase não serve <code>.md</code>; no GitHub Pages, sim).</p>
    <p><b>Publicação:</b> o repositório publica no GitHub Pages a cada push; o Firebase precisa de <code>firebase deploy</code>.</p>
    <p><b>Testes:</b> <code>python Apps/_base/testar.py</code> e <code>python Apps/_base/testar_sprints.py</code>.
      O painel não executa navegador; ele lê o código e os documentos.</p>
  </div>

  <footer>Gerar de novo: <code>python Apps/_base/painel.py</code>. Fontes: <code>app.json</code>,
    <code>src/*.js</code>, <code>sprint.md</code>, <code>equipes.json</code> e <code>exemplos/seed.json</code>.</footer>
</main>
<script>
const busca = document.getElementById('busca'), apps = [...document.querySelectorAll('details.app')], contador = document.getElementById('contador');
let filtro = 'todos';
function aplicar(){{
  const q = busca.value.trim().toLowerCase();
  let n = 0;
  apps.forEach(a=>{{ const ok = (filtro === 'todos' || a.dataset.grupo === filtro) && (!q || a.dataset.busca.includes(q)); a.hidden = !ok; if (ok) n++; }});
  contador.textContent = n + ' de ' + apps.length + ' apps';
}}
busca.addEventListener('input', aplicar);
document.querySelectorAll('[data-f]').forEach(b=>b.addEventListener('click', ()=>{{
  filtro = b.dataset.f; document.querySelectorAll('[data-f]').forEach(x=>x.classList.toggle('ativo', x === b)); aplicar();
}}));
aplicar();
</script>
</body>
</html>
"""
(APPS / "painel.html").write_text(html_doc, encoding="utf-8")
print(f"Apps/painel.html: {len(apps)} apps, {total_telas}/{total_rotas} telas, {total_pend} pendentes")
