# -*- coding: utf-8 -*-
"""Motor compartilhado dos cadernos POLITEC/MT.

Reune o CSS e os helpers de conteudo usados por todos os cadernos do curso.
Cada aula escreve apenas o conteudo (secoes) e chama ``Caderno.build()``.

Uso tipico (arquivo ``Aula N/gerar_caderno_aulaN.py``):

    import pathlib, sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
    from caderno_lib import Caderno, p, h3, ul, ficha, callout, tbl, code, q

    cad = Caderno(out="caderno-diaN.html", dia=N, kicker="...", headline="...",
                  sub="...", meta="...", descricao="...")
    cad.grp("Parte 1 · ...", "descricao")
    cad.section("anchor", "Titulo", p("...") + callout("tip", "...", "..."))
    cad.build()

O ``build()`` aceita, opcionalmente, um caminho de JSON (via ``sys.argv[1]``)
com o mapa ``{anchor: pagina}`` para imprimir os numeros no sumario (2a
passada da exportacao de PDF).
"""
import html
import json
import pathlib
import re
import sys

# =================================================================
# CSS
# =================================================================
CSS_BASE = r"""
:root{
  --paper:#faf9f6; --surface:#ffffff; --raised:#f3f1ec;
  --ink:#1a1d1e; --ink-soft:#4a4f52; --ink-faint:#82888c;
  --accent:#12507f; --accent-soft:#e6eff7;
  --verde:#1c8a5b; --verde-soft:#e4f5ec;
  --ambar:#b4790a; --ambar-soft:#fbeed9;
  --vermelho:#c33b3b; --vermelho-soft:#fbe7e7;
  --roxo:#6b3fa0; --roxo-soft:#efe6f8;
  --border:#e3e0d8; --code-bg:#1e2124; --code-ink:#e6e6e6;
  --shadow: 0 1px 2px rgba(0,0,0,.04), 0 4px 14px rgba(0,0,0,.05);
}
:root[data-theme="dark"]{
  --paper:#15171a; --surface:#1b1e22; --raised:#20242a;
  --ink:#eceeef; --ink-soft:#b6bcc2; --ink-faint:#7d858c;
  --accent:#5fa8dd; --accent-soft:#16283a;
  --verde:#5cc797; --verde-soft:#123528;
  --ambar:#e0ac4c; --ambar-soft:#3a2c11;
  --vermelho:#e77f7f; --vermelho-soft:#3a1c1c;
  --roxo:#b18ce0; --roxo-soft:#2a1f3a;
  --border:#2c3036; --code-bg:#0f1113; --code-ink:#d8dadb;
  --shadow: 0 1px 2px rgba(0,0,0,.3), 0 4px 18px rgba(0,0,0,.35);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#15171a; --surface:#1b1e22; --raised:#20242a;
    --ink:#eceeef; --ink-soft:#b6bcc2; --ink-faint:#7d858c;
    --accent:#5fa8dd; --accent-soft:#16283a;
    --verde:#5cc797; --verde-soft:#123528;
    --ambar:#e0ac4c; --ambar-soft:#3a2c11;
    --vermelho:#e77f7f; --vermelho-soft:#3a1c1c;
    --roxo:#b18ce0; --roxo-soft:#2a1f3a;
    --border:#2c3036; --code-bg:#0f1113; --code-ink:#d8dadb;
  }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:'Source Serif 4', Georgia, serif; font-size:17px; line-height:1.65;
}
h1,h2,h3,h4,.ui{font-family:'Archivo',sans-serif}
code,pre,.mono{font-family:'JetBrains Mono',monospace}
a{color:var(--accent)}
header.top{
  padding:40px 24px 28px; border-bottom:1px solid var(--border);
  background:linear-gradient(180deg,var(--surface),var(--paper));
}
header.top .inner{max-width:1160px;margin:0 auto}
.kicker{font-family:'Archivo',sans-serif;font-size:12.5px;letter-spacing:.09em;text-transform:uppercase;
  color:var(--accent); background:var(--accent-soft); display:inline-block; padding:4px 10px; border-radius:20px; font-weight:600;}
header.top h1{font-size:clamp(28px,4vw,42px); margin:14px 0 6px; letter-spacing:-.01em}
header.top p.sub{color:var(--ink-soft); font-size:17px; margin:0; max-width:760px}
header.top .meta{margin-top:14px; font-size:13.5px; color:var(--ink-faint); font-family:'Archivo',sans-serif}
.wrap.shell{
  max-width:1160px; margin:0 auto; padding:28px 24px 100px;
  display:grid; grid-template-columns:1fr; gap:28px;
}
@media(min-width:1000px){ .wrap.shell{grid-template-columns:250px 1fr;} }
nav.toc{
  align-self:start; position:sticky; top:16px; max-height:calc(100vh - 32px); overflow:auto;
  background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:16px;
  font-family:'Archivo',sans-serif; font-size:13.3px;
}
nav.toc input{
  width:100%; padding:8px 10px; margin-bottom:10px; border-radius:8px; border:1px solid var(--border);
  background:var(--paper); color:var(--ink); font-family:inherit; font-size:12.8px;
}
nav.toc .grp{color:var(--ink-faint); text-transform:uppercase; letter-spacing:.06em; font-size:10.8px;
  font-weight:700; margin:14px 0 5px;}
nav.toc .grp:first-child{margin-top:0}
nav.toc a{display:block; color:var(--ink-soft); text-decoration:none; padding:4.5px 8px; border-radius:7px; line-height:1.35}
nav.toc a:hover{background:var(--raised); color:var(--ink)}
nav.toc a.active{background:var(--accent-soft); color:var(--accent); font-weight:600}
main section{
  background:var(--surface); border:1px solid var(--border); border-radius:16px;
  padding:30px 32px; margin-bottom:22px; box-shadow:var(--shadow); scroll-margin-top:16px;
}
main section .secnum{font-family:'Archivo',sans-serif; font-size:12px; color:var(--ink-faint); letter-spacing:.08em; text-transform:uppercase}
main section h2{font-size:24px; margin:6px 0 16px; letter-spacing:-.01em}
main section h3{font-size:17.5px; margin:22px 0 8px}
main section h4{font-size:15.5px; margin:16px 0 6px}
main section p{margin:0 0 13px}
main section ul, main section ol{margin:0 0 13px; padding-left:22px}
main section li{margin-bottom:5px}
.ficha{border-radius:12px; padding:16px 18px; margin:16px 0; border-left:4px solid var(--accent); background:var(--accent-soft); font-family:'Archivo',sans-serif; font-size:15px}
.ficha.g{border-color:var(--verde); background:var(--verde-soft)}
.ficha.a{border-color:var(--ambar); background:var(--ambar-soft)}
.ficha.r{border-color:var(--vermelho); background:var(--vermelho-soft)}
.ficha.p{border-color:var(--roxo); background:var(--roxo-soft)}
.ficha b.lbl{display:block; text-transform:uppercase; font-size:11px; letter-spacing:.08em; margin-bottom:5px; opacity:.85}
.callout{border-radius:12px; padding:14px 18px; margin:16px 0; font-size:15.3px; border:1px solid var(--border); background:var(--raised)}
.callout.note{border-color:var(--accent); background:var(--accent-soft)}
.callout.tip{border-color:var(--verde); background:var(--verde-soft)}
.callout.err{border-color:var(--vermelho); background:var(--vermelho-soft)}
.callout.purple{border-color:var(--roxo); background:var(--roxo-soft)}
.callout b.lbl{font-family:'Archivo',sans-serif; text-transform:uppercase; font-size:11px; letter-spacing:.08em; display:block; margin-bottom:5px}
ul.f{list-style:none; margin:16px 0; padding:14px 16px; border-radius:12px; background:var(--code-bg); color:var(--code-ink);
  font-family:'JetBrains Mono',monospace; font-size:13.6px; overflow-x:auto; position:relative;}
ul.f li{white-space:pre; margin:0; padding:1px 0}
ul.f::before{content:attr(data-lang); position:absolute; top:8px; right:14px; font-family:'Archivo',sans-serif;
  font-size:10px; letter-spacing:.08em; text-transform:uppercase; color:#8b9199;}
ul.f code, table code{background:none; border:none; padding:0}
.tbl{overflow-x:auto; margin:16px 0}
table{width:100%; border-collapse:collapse; font-family:'Archivo',sans-serif; font-size:14.3px}
table th{text-align:left; background:var(--raised); padding:9px 12px; border-bottom:2px solid var(--border); font-weight:700}
table td{padding:9px 12px; border-bottom:1px solid var(--border); vertical-align:top}
table td.num, table th.num{text-align:right}
ol.step{list-style:none; margin:16px 0; padding:0; counter-reset:stp}
ol.step li{counter-increment:stp; position:relative; padding:4px 0 14px 40px; border-left:2px solid var(--border); margin-left:14px}
ol.step li:last-child{border-color:transparent; padding-bottom:0}
ol.step li::before{content:counter(stp); position:absolute; left:-14px; top:0; width:28px; height:28px; border-radius:50%;
  background:var(--accent); color:#fff; font-family:'Archivo',sans-serif; font-weight:700; font-size:13px; display:flex; align-items:center; justify-content:center}
ol.step .stitle{font-family:'Archivo',sans-serif; font-weight:700; font-size:15.5px; margin-bottom:2px}
ol.step .snote{color:var(--ink-faint); font-size:13.6px; margin-top:4px}
.btnref{display:inline-block; font-family:'JetBrains Mono',monospace; font-size:12.8px; background:var(--raised);
  border:1px solid var(--border); border-radius:6px; padding:1.5px 7px; color:var(--ink)}
.q{border:1px solid var(--border); border-radius:12px; padding:14px 18px; margin:12px 0; background:var(--raised)}
.q .stem{font-family:'Archivo',sans-serif; font-weight:700; margin-bottom:8px}
.q details summary{cursor:pointer; color:var(--accent); font-family:'Archivo',sans-serif; font-size:13.8px; font-weight:600}
.q details[open] summary{margin-bottom:6px}
.q .resp-lbl{font-family:'Archivo',sans-serif; font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--verde); margin-right:6px}
.aplicab{display:grid; grid-template-columns:1fr; gap:12px; margin:16px 0}
@media(min-width:760px){.aplicab{grid-template-columns:1fr 1fr 1fr}}
.aplicab > div{border:1px solid var(--border); border-radius:12px; padding:14px 16px; background:var(--raised)}
.aplicab .lbl{font-family:'Archivo',sans-serif; font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:.06em; margin-bottom:6px; color:var(--accent)}
.grid2{display:grid; grid-template-columns:1fr; gap:14px; margin:16px 0}
@media(min-width:760px){.grid2{grid-template-columns:1fr 1fr}}
.card{border:1px solid var(--border); border-radius:12px; padding:16px 18px; background:var(--raised)}
.card h4{margin:0 0 8px; font-size:15.5px}
.flow{display:flex; flex-wrap:wrap; align-items:stretch; gap:0; margin:18px 0}
.flow .fnode{flex:1 1 140px; text-align:center; padding:16px 10px; position:relative}
.flow .fnode .circ{width:64px;height:64px;border-radius:50%;border:2.5px solid var(--accent); margin:0 auto 10px;
  display:flex; align-items:center; justify-content:center; background:var(--surface); font-size:22px}
.flow .fnode .lbl{font-family:'Archivo',sans-serif; font-weight:600; font-size:13.4px}
.flow .fnode:not(:last-child)::after{content:"\2192"; position:absolute; right:-6px; top:26px; color:var(--accent); font-size:20px; font-weight:700}
.kpi{display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:14px; margin:16px 0}
.kpi .k{border:1px solid var(--border); border-radius:12px; padding:16px; text-align:center; background:var(--raised)}
.kpi .k .val{font-family:'Archivo',sans-serif; font-weight:800; font-size:28px; color:var(--accent)}
.kpi .k .lbl{font-size:12.6px; color:var(--ink-faint); font-family:'Archivo',sans-serif; margin-top:4px}
.glossary dt{font-family:'Archivo',sans-serif; font-weight:700; margin-top:10px}
.glossary dd{margin:2px 0 0; color:var(--ink-soft)}
.barchart{margin:18px 0; border:1px solid var(--border); border-radius:12px; padding:16px 18px; background:var(--surface)}
.barchart .bct{font-family:'Archivo',sans-serif; font-weight:700; font-size:13.8px; margin-bottom:2px}
.barchart .bcs{font-size:12.6px; color:var(--ink-faint); margin-bottom:12px; font-family:'Archivo',sans-serif}
.barchart .bcplot{display:flex; align-items:flex-end; gap:12px; height:200px; border-left:1px solid var(--border); border-bottom:1px solid var(--border); padding:0 8px}
.barchart .bcbar{flex:1; display:flex; flex-direction:column; justify-content:flex-end; align-items:center; height:100%}
.barchart .bcbar .bcv{font-family:'Archivo',sans-serif; font-weight:700; font-size:12.5px; color:var(--accent); margin-bottom:4px}
.barchart .bcbar .bcfill{width:100%; max-width:64px; background:var(--accent); border-radius:5px 5px 0 0; min-height:2px}
.barchart .bcbar.dest .bcfill{background:var(--vermelho)}
.barchart .bcbar.dest .bcv{color:var(--vermelho)}
.barchart .bcx{display:flex; gap:12px; padding:7px 8px 0}
.barchart .bcx div{flex:1; text-align:center; font-family:'Archivo',sans-serif; font-size:11.6px; color:var(--ink-soft)}
.themebtn,.pdfbtn{position:fixed; right:20px; z-index:50; font-family:'Archivo',sans-serif; font-size:12.8px; font-weight:600;
  border:1px solid var(--border); background:var(--surface); color:var(--ink); border-radius:24px; padding:9px 16px; cursor:pointer; box-shadow:var(--shadow)}
.themebtn{bottom:20px}
.pdfbtn{bottom:66px}
footer.pagefoot{max-width:1160px;margin:0 auto;padding:0 24px 60px;color:var(--ink-faint);font-family:'Archivo',sans-serif;font-size:12.5px;text-align:center}
"""

CSS_EXTRA = r"""
.wrap.shell{grid-template-columns:minmax(0,1fr)}
@media(min-width:1000px){ .wrap.shell{grid-template-columns:250px minmax(0,1fr)} }
main{min-width:0}
@media(max-width:999px){ nav.toc{position:static; max-height:none} }
@media screen and (max-width:600px){ .flow{flex-direction:column; align-items:center}
  .flow .fnode{flex:none; width:100%; padding:8px 10px 18px}
  .flow .fnode:not(:last-child)::after{content:"\2193"; right:auto; left:50%; transform:translateX(-50%); top:auto; bottom:-6px} }
.grid2 > *, .legenda > *, .antesdepois > *, .aplicab > *, .kpi > *{min-width:0}
code{overflow-wrap:anywhere; font-size:.9em; background:var(--raised); border:1px solid var(--border); border-radius:5px; padding:0 4px}
ul.f{padding-top:30px}
ul.f .cpy{position:absolute; top:6px; left:14px; font-family:'Archivo',sans-serif; font-size:10.5px; font-weight:700;
  letter-spacing:.06em; text-transform:uppercase; background:rgba(255,255,255,.08); color:#c9cdd2; border:1px solid rgba(255,255,255,.14);
  border-radius:6px; padding:2px 9px; cursor:pointer}
ul.f .cpy:hover{background:rgba(255,255,255,.16)}
.parte{border-radius:14px; padding:18px 22px; margin:-6px 0 22px; background:var(--accent); color:#fff}
.parte .pk{font-family:'Archivo',sans-serif; font-size:11.5px; font-weight:700; letter-spacing:.12em; text-transform:uppercase; opacity:.85}
.parte .pt{font-family:'Archivo',sans-serif; font-size:23px; font-weight:800; margin:2px 0 6px; line-height:1.2}
.parte .pd{font-size:15px; opacity:.95; margin:0}
.parte ol{margin:10px 0 0; padding-left:20px; font-family:'Archivo',sans-serif; font-size:13.4px; opacity:.95}
.parte ol li{margin:1px 0}
.antesdepois{display:grid; grid-template-columns:1fr; gap:12px; margin:14px 0}
@media(min-width:760px){.antesdepois{grid-template-columns:1fr 1fr}}
.antesdepois > div{border-radius:12px; padding:12px 14px; border:1px solid var(--border)}
.antesdepois .ruim{background:var(--vermelho-soft); border-color:var(--vermelho)}
.antesdepois .bom{background:var(--verde-soft); border-color:var(--verde)}
.antesdepois .lbl{font-family:'Archivo',sans-serif; font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; margin-bottom:6px}
.antesdepois .ruim .lbl{color:var(--vermelho)} .antesdepois .bom .lbl{color:var(--verde)}
.antesdepois p{margin:0; font-size:14.6px}
.check{list-style:none; padding-left:0 !important}
.check li{padding-left:28px; position:relative}
.check li::before{content:"\2610"; position:absolute; left:4px; top:-1px; color:var(--accent); font-size:17px}
.legenda{display:grid; grid-template-columns:1fr; gap:10px; margin:14px 0}
@media(min-width:760px){.legenda{grid-template-columns:1fr 1fr}}
.legenda > div{display:flex; gap:12px; align-items:flex-start; border:1px solid var(--border); border-radius:12px; padding:12px 14px; background:var(--raised)}
.legenda .ic{font-size:22px; line-height:1}
.legenda > div > div > b{font-family:'Archivo',sans-serif; display:block; font-size:14.5px}
.legenda span.d{font-size:14px; color:var(--ink-soft)}
.sumario{display:none}

@media print{
  @page { size: A4; margin: 14mm 13mm 16mm 13mm; }
  :root, :root[data-theme="dark"], :root:not([data-theme="light"]){
    --paper:#ffffff !important; --surface:#ffffff !important; --raised:#f4f2ed !important;
    --ink:#1a1d1e !important; --ink-soft:#4a4f52 !important; --ink-faint:#7a8084 !important;
    --accent:#12507f !important; --accent-soft:#e6eff7 !important;
    --verde:#1c8a5b !important; --verde-soft:#e4f5ec !important;
    --ambar:#b4790a !important; --ambar-soft:#fbeed9 !important;
    --vermelho:#c33b3b !important; --vermelho-soft:#fbe7e7 !important;
    --roxo:#6b3fa0 !important; --roxo-soft:#efe6f8 !important;
    --border:#e3e0d8 !important; --code-bg:#1e2124 !important; --code-ink:#e6e6e6 !important;
    --shadow:none !important; color-scheme:light;
  }
  html{ -webkit-print-color-adjust:exact; print-color-adjust:exact }
  html, body{ margin:0; padding:0; background:#fff; font-size:13.5px; line-height:1.5 }
  .themebtn,.pdfbtn,nav.toc,button,.cpy{ display:none !important }

  header.top{ padding:70mm 0 12mm !important; background:none !important; border-bottom:3px solid var(--accent) !important }
  header.top .inner{ max-width:100% !important; padding:0 !important }
  header.top h1{ font-size:34px !important; margin:14px 0 10px !important }
  header.top p.sub{ font-size:16px !important; max-width:none !important }

  .sumario{ display:block; break-before:page; page-break-before:always; break-after:page; page-break-after:always; font-family:'Archivo',sans-serif }
  .sumario h2{ font-size:19px; margin:0 0 2mm; padding-bottom:2mm; border-bottom:2px solid var(--accent) }
  .sumario .sg{ font-weight:800; font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--accent); margin:3mm 0 .5mm }
  .sumario .si{ display:flex; align-items:baseline; gap:6px; font-size:11.8px; line-height:1.35; padding:.35mm 0; color:var(--ink) }
  .sumario .si .n{ min-width:20px; color:var(--ink-faint) }
  .sumario .si .dots{ flex:1; border-bottom:1px dotted #b9b6ae; transform:translateY(-3px) }
  .sumario .si .pg{ min-width:18px; text-align:right; font-weight:700 }

  .wrap.shell{ display:block !important; max-width:100% !important; margin:0 !important; padding:0 !important }
  main{ overflow:visible !important }

  main section{
    background:#fff !important; box-shadow:none !important; border:none !important; border-radius:0 !important;
    padding:0 !important; margin:0 0 8mm !important; break-before:auto; page-break-before:auto;
  }
  main section:not(.inicio-parte){ border-top:1px solid var(--border) !important; padding-top:5mm !important }
  main section.inicio-parte{ break-before:page; page-break-before:always }
  .parte{ margin:0 0 6mm !important; padding:6mm 7mm !important; break-inside:avoid }
  .parte .pt{ font-size:22px !important }
  main section h2{ font-size:18.5px !important; margin:1mm 0 4mm !important }
  main section h3{ font-size:14.8px !important; margin:10px 0 5px !important }
  main section p{ margin:0 0 9px }

  h1, h2, h3, h4, .secnum, ol.step .stitle{ break-after:avoid; page-break-after:avoid; break-inside:avoid }
  h2 + *, h3 + *, h4 + *{ break-before:avoid; page-break-before:avoid }
  .parte{ break-after:avoid; page-break-after:avoid }
  .ficha, .callout, .q, ul.f, .card, .aplicab > div, .kpi, .kpi .k, .flow, ol.step li,
  tr, dt, dd, .antesdepois > div, .legenda > div, .barchart, img, svg{ break-inside:avoid; page-break-inside:avoid }
  dt{ break-after:avoid }
  thead{ display:table-header-group }
  p, li{ orphans:3; widows:3 }
  .tbl{ overflow:visible !important }

  ul.f{ overflow:visible !important; font-size:10.4px !important; padding:22px 10px 8px !important; margin:10px 0 !important; line-height:1.45 }
  ul.f li{ white-space:pre-wrap !important; overflow-wrap:anywhere }
  ul.f::before{ top:6px !important }
  table{ font-size:11.3px !important } table th, table td{ padding:5px 8px !important }
  .ficha, .callout{ padding:8px 11px !important; margin:8px 0 !important; font-size:12.8px !important }
  .card{ padding:10px 12px !important; font-size:12.8px }
  .aplicab, .grid2, .legenda{ gap:8px !important; margin:10px 0 !important }
  .aplicab{ grid-template-columns:1fr 1fr 1fr !important }
  .grid2, .legenda, .antesdepois{ grid-template-columns:1fr 1fr !important }
  .aplicab > div{ padding:8px 10px !important; font-size:12.4px }
  .kpi{ grid-template-columns:repeat(4,1fr) !important; gap:8px !important }
  .kpi .k{ padding:8px !important } .kpi .k .val{ font-size:22px !important }

  .flow{ flex-wrap:nowrap !important; margin:10px 0 !important }
  .flow .fnode{ flex:1 1 0 !important; padding:6px 3px !important; min-width:0 }
  .flow .fnode .circ{ width:44px !important; height:44px !important; font-size:18px !important; margin-bottom:6px !important }
  .flow .fnode .lbl{ font-size:10.6px !important; line-height:1.25 }
  .flow .fnode:not(:last-child)::after{ right:-7px !important; top:15px !important; font-size:15px !important }

  ol.step li{ padding-bottom:9px !important }
  .q details summary{ display:none }
  footer.pagefoot{ padding:4mm 0 0 !important; break-before:avoid }
}
"""

CSS = CSS_BASE + CSS_EXTRA

# =================================================================
# HELPERS DE BLOCO
# =================================================================
def p(txt):
    return f"<p>{txt}</p>"

def h3(txt):
    return f"<h3>{txt}</h3>"

def h4(txt):
    return f"<h4>{txt}</h4>"

def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def ol(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"

def checklist(items):
    return "<ul class='check'>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def ficha(kind, label, body):
    return f'<div class="ficha {kind}"><b class="lbl">{label}</b>{body}</div>'

def callout(kind, label, body):
    return f'<div class="callout {kind}"><b class="lbl">{label}</b>{body}</div>'

def tbl(headers, rows, num_cols=None):
    num_cols = num_cols or []
    th = "".join(f'<th class="num">{h}</th>' if i in num_cols else f"<th>{h}</th>"
                 for i, h in enumerate(headers))
    trs = ""
    for r in rows:
        tds = "".join(f'<td class="num">{c}</td>' if i in num_cols else f"<td>{c}</td>"
                      for i, c in enumerate(r))
        trs += f"<tr>{tds}</tr>"
    return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'

def _lines(text):
    lns = text.strip("\n").split("\n")
    ind = min((len(l) - len(l.lstrip(" ")) for l in lns if l.strip()), default=0)
    return [l[ind:].rstrip() for l in lns]

def code(text, lang="texto"):
    linhas = _lines(text)
    lis = "".join(f"<li>{html.escape(l) if l else ' '}</li>" for l in linhas)
    return f'<ul class="f" data-lang="{lang}">{lis}</ul>'

def step(items):
    out = "<ol class='step'>"
    for it in items:
        out += f"<li><div class='stitle'>{it[0]}</div><div>{it[1]}</div>"
        if len(it) > 2 and it[2]:
            out += f"<div class='snote'>{it[2]}</div>"
        out += "</li>"
    return out + "</ol>"

def q(stem, options, ans_idx, hint=""):
    opts = "".join(f"<li>{o}</li>" for o in options)
    letra = "abcd"[ans_idx]
    hint_html = f" {hint}" if hint else ""
    return (f'<div class="q"><div class="stem">{stem}</div><ol type="a">{opts}</ol>'
            f'<details><summary>Ver resposta</summary><p><span class="resp-lbl">Resposta</span>'
            f'<b>({letra}) {options[ans_idx]}.</b>{hint_html}</p></details></div>')

def aplicab(quando, porque, exemplo, rotulo_exemplo="Exemplo na POLITEC"):
    return (f'<div class="aplicab"><div><div class="lbl">Quando</div>{quando}</div>'
            f'<div><div class="lbl">Por que</div>{porque}</div>'
            f'<div><div class="lbl">{rotulo_exemplo}</div>{exemplo}</div></div>')

def grid2(cards):
    return '<div class="grid2">' + "".join(f'<div class="card"><h4>{t}</h4>{b}</div>' for t, b in cards) + '</div>'

def flow_h(nodes):
    return '<div class="flow">' + "".join(
        f'<div class="fnode"><div class="circ">{e}</div><div class="lbl">{l}</div></div>' for e, l in nodes) + '</div>'

def kpi(items):
    return '<div class="kpi">' + "".join(
        f'<div class="k"><div class="val">{v}</div><div class="lbl">{l}</div></div>' for v, l in items) + '</div>'

def antesdepois(ruim, bom, errado="Errado", certo="Certo"):
    return (f'<div class="antesdepois"><div class="ruim"><div class="lbl">\u2717 {errado}</div><p>{ruim}</p></div>'
            f'<div class="bom"><div class="lbl">\u2713 {certo}</div><p>{bom}</p></div></div>')

def legenda(items):
    return '<div class="legenda">' + "".join(
        f'<div><span class="ic">{i}</span><div><b>{t}</b><span class="d">{d}</span></div></div>'
        for i, t, d in items) + '</div>'

def glossary(items):
    return "<dl class='glossary'>" + "".join(f"<dt>{t}</dt><dd>{d}</dd>" for t, d in items) + "</dl>"

def bar_chart(labels, values, title="", subtitulo="", destaque=None, fmt="{:.0f}"):
    mx = max(values) if values else 1
    cols = ""
    for i, (l, v) in enumerate(zip(labels, values)):
        pct = (v / mx * 82) if mx else 0
        cls = " dest" if destaque is not None and i == destaque else ""
        cols += (f'<div class="bcbar{cls}"><div class="bcv">{fmt.format(v)}</div>'
                 f'<div class="bcfill" style="height:{pct:.1f}%"></div></div>')
    xs = "".join(f"<div>{l}</div>" for l in labels)
    t = f'<div class="bct">{title}</div>' if title else ""
    s = f'<div class="bcs">{subtitulo}</div>' if subtitulo else ""
    return f'<div class="barchart">{t}{s}<div class="bcplot">{cols}</div><div class="bcx">{xs}</div></div>'


# =================================================================
# TEMPLATE
# =================================================================
TEMPLATE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>__CSS__</style>
</head>
<body>
<header class="top">
  <div class="inner">
    <span class="kicker">__KICKER__</span>
    <h1>__HEADLINE__</h1>
    <p class="sub">__SUB__</p>
    <div class="meta">__META__</div>
  </div>
</header>
__SUMARIO__
<div class="wrap shell">
  <nav class="toc">
    <input type="text" id="tocsearch" placeholder="Buscar no indice...">
    <div id="tocgroups">__TOC__</div>
  </nav>
  <main>
    __SECTIONS__
  </main>
</div>
<footer class="pagefoot">__FOOT__</footer>
<button class="themebtn" id="themebtn">\U0001f317 Tema</button>
<button class="pdfbtn" id="pdfbtn">\U0001f5a8\ufe0f Imprimir / PDF</button>
<script>
(function(){
  var btnT = document.getElementById('themebtn');
  var root = document.documentElement;
  var saved = null;
  try { saved = localStorage.getItem('caderno-theme'); } catch(e) {}
  if (saved) root.setAttribute('data-theme', saved);
  btnT.addEventListener('click', function(){
    var cur = root.getAttribute('data-theme');
    var next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('caderno-theme', next); } catch(e) {}
  });
  document.getElementById('pdfbtn').addEventListener('click', function(){ window.print(); });

  var abertos = [];
  window.addEventListener('beforeprint', function(){
    document.querySelectorAll('details:not([open])').forEach(function(d){ d.open = true; abertos.push(d); });
  });
  window.addEventListener('afterprint', function(){ abertos.forEach(function(d){ d.open = false; }); abertos = []; });

  document.querySelectorAll('ul.f').forEach(function(block){
    var b = document.createElement('button');
    b.className = 'cpy'; b.type = 'button'; b.textContent = 'Copiar';
    b.addEventListener('click', function(){
      var txt = Array.prototype.map.call(block.querySelectorAll('li'), function(li){ return li.textContent; }).join('\\n');
      var done = function(){ b.textContent = 'Copiado'; setTimeout(function(){ b.textContent = 'Copiar'; }, 1500); };
      if (navigator.clipboard) { navigator.clipboard.writeText(txt).then(done, function(){}); }
      else { var t = document.createElement('textarea'); t.value = txt; document.body.appendChild(t); t.select();
             try { document.execCommand('copy'); done(); } catch(e) {} document.body.removeChild(t); }
    });
    block.appendChild(b);
  });

  var links = Array.prototype.slice.call(document.querySelectorAll('nav.toc a'));
  var secs = Array.prototype.slice.call(document.querySelectorAll('main section'));
  function onScroll(){
    var pos = window.scrollY + 120;
    var current = secs[0];
    secs.forEach(function(s){ if (s.offsetTop <= pos) current = s; });
    links.forEach(function(a){ a.classList.toggle('active', a.getAttribute('data-anchor') === current.id); });
  }
  window.addEventListener('scroll', onScroll);
  onScroll();

  var search = document.getElementById('tocsearch');
  search.addEventListener('input', function(){
    var term = search.value.toLowerCase();
    links.forEach(function(a){
      var show = a.textContent.toLowerCase().indexOf(term) !== -1;
      a.style.display = show ? '' : 'none';
    });
    document.querySelectorAll('#tocgroups .grp').forEach(function(g){
      var next = g.nextElementSibling, any = false;
      while (next && !next.classList.contains('grp')) {
        if (next.style.display !== 'none') any = true;
        next = next.nextElementSibling;
      }
      g.style.display = any ? '' : 'none';
    });
  });
})();
</script>
</body>
</html>
"""


# =================================================================
# DOCUMENTO
# =================================================================
class Caderno:
    """Monta um caderno HTML a partir de grupos (partes) e secoes."""

    def __init__(self, out, dia, kicker, headline, sub, meta, descricao,
                 titulo=None, rodape=None, curso="POLITEC/MT"):
        self.out = pathlib.Path(out)
        self.dia = dia
        self.kicker = kicker
        self.headline = headline
        self.sub = sub
        self.meta = meta
        self.descricao = descricao
        self.titulo = titulo or f"Caderno do Dia {dia} · {curso}"
        self.rodape = rodape or f"Caderno do Dia {dia} · Curso de Capacitacao {curso} · Professor Renato Rosa"
        self.sections = []   # (anchor, titulo, body, grupo_idx)
        self.grupos = []     # (titulo, descricao)

    def grp(self, titulo, descricao=""):
        self.grupos.append((titulo, descricao))

    def section(self, anchor, titulo, body_html):
        assert self.grupos, "chame grp() antes de section()"
        self.sections.append((anchor, titulo, body_html, len(self.grupos) - 1))

    # -- render --------------------------------------------------
    def _toc(self):
        out = ""
        for gi, (gtitle, _) in enumerate(self.grupos):
            out += f'<div class="grp">{gtitle}</div>'
            for anchor, titulo, _, g in self.sections:
                if g == gi:
                    out += f'<a href="#{anchor}" data-anchor="{anchor}">{titulo}</a>'
        return out

    def _sumario(self, paginas):
        out = '<div class="sumario"><h2>Sumario</h2>'
        for gi, (gtitle, _) in enumerate(self.grupos):
            out += f'<div class="sg">{gtitle}</div>'
            for i, (anchor, titulo, _, g) in enumerate(self.sections, start=1):
                if g == gi:
                    pg = paginas.get(anchor, "")
                    out += (f'<div class="si"><span class="n">{i}</span><span>{titulo}</span>'
                            f'<span class="dots"></span><span class="pg">{pg}</span></div>')
        return out + "</div>"

    def _sections(self):
        out = ""
        visto = set()
        for i, (anchor, titulo, body, g) in enumerate(self.sections, start=1):
            banner, cls = "", ""
            if g not in visto:
                visto.add(g)
                cls = ' class="inicio-parte"'
                gtitle, gdesc = self.grupos[g]
                nomes = "".join(f"<li>{t}</li>" for _, t, _, gg in self.sections if gg == g)
                kicker, _, resto = gtitle.partition(" · ")
                banner = (f'<div class="parte"><div class="pk">{kicker}</div>'
                          f'<div class="pt">{resto or kicker}</div><p class="pd">{gdesc}</p><ol>{nomes}</ol></div>')
            out += (f'<section id="{anchor}"{cls}>{banner}<div class="shead"><span class="secnum">§ {i}</span>'
                    f'<h2>{titulo}</h2></div>{body}</section>')
        return out

    def build(self):
        paginas = {}
        if len(sys.argv) > 1 and pathlib.Path(sys.argv[1]).exists():
            paginas = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
        doc = (TEMPLATE
               .replace("__CSS__", CSS)
               .replace("__TITLE__", self.titulo)
               .replace("__DESC__", self.descricao)
               .replace("__KICKER__", self.kicker)
               .replace("__HEADLINE__", self.headline)
               .replace("__SUB__", self.sub)
               .replace("__META__", self.meta)
               .replace("__FOOT__", self.rodape)
               .replace("__SUMARIO__", self._sumario(paginas))
               .replace("__TOC__", self._toc())
               .replace("__SECTIONS__", self._sections()))
        self.out.write_text(doc, encoding="utf-8")
        print(f"Gerado: {self.out.name} - {len(self.sections)} secoes - {len(doc)//1024} KB")
        return doc
