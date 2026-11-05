"""Gera o `processo.html` (AS-IS -> TO-BE + MVP) de cada app.

Lê `app.json` (identidade) e `projeto.json` (tabelas AS-IS, TO-BE, métricas,
regras e papéis) e escreve um HTML autossuficiente na pasta do app.

Uso: python Apps/_base/gerar_hubs.py
"""
import html
import json
import re
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent

ASSINATURA = {
    "agendamento-cin": "Calendário do mês com vagas por dia e horários em botões grandes",
    "cin-segunda-via": "Caixa de entrada: fila à esquerda e pedido à direita, com Aceitar e próximo",
    "horus-banco-demandas": "Vitrine com filtros em facetas, ordenação e alternância cartões/tabela",
    "trilha-custodia-necropsia": "Quadro das sete etapas para o Técnico e fila da ADM para o Gestor, com cartões de corpo",
    "controle-aquisicoes": "Kanban das 9 etapas da Lei 14.133",
    "custodia-definitiva": "Balcão de leitura do lacre e mapa das prateleiras",
    "documentapolitec": "Estante de caixas em lombadas e conferência por leitura",
    "gestao-documentos": "Caixa por perfil: a instruir, a revisar e a assinar",
    "renovacao-contratos-horus": "Régua de vencimentos de 0 a 180 dias e semáforo em barra",
    "distribuicao-casos-dna": "Placa de 96 poços com a cor do perito",
    "comissao-etica-denuncias": "Funil do processo ético e dossiê Reservado",
    "passivo-ambiental": "Fila de laudos com prazo e miniatura do mapa",
    "rnc-nao-conformidade": "Quadro por etapa do ciclo da RNC",
    "tap-portfolio-projetos": "Matriz do portfólio (valor × prioridade)",
    "adiantamento": "Régua de prazos por processo",
    "metas-bi-ocr": "Ano em 12 meses com a situação de cada mês",
    "inscricoes-cursos": "Cartões de curso com a esteira Divulgar → Turma",
    "mapa-distribuicao-credor": "Esteira de 8 etapas e grade em formato planilha",
    "equipamentos-google-earth": "Mapa de MT em SVG com os pinos das unidades",
    "agiliza-mais": "Bancada do caso: passos à esquerda e trabalho à direita",
    "gestao_identificados": "Painel da pergunta do MVP e ficha em etapas de identificação",
}

CRITICA = {
    "agendamento-cin": "O comprovante ainda não tem “salvar no celular”; a agenda do posto usa tabela com rolagem interna.",
    "cin-segunda-via": "O fluxo público exige duas fotos e a redução depende de canvas; no Lightpanda essa etapa não roda.",
    "horus-banco-demandas": "O contexto de unidade fica dentro do menu de perfil; a vitrine avisa a unidade no subtítulo.",
    "trilha-custodia-necropsia": "A ficha em abas separa as etapas, o laudo e o encerramento na aba Etapas; a mudança manual de situação fica na aba Situação.",
    "controle-aquisicoes": "O kanban de 9 colunas exige rolagem horizontal no celular.",
    "custodia-definitiva": "A prateleira leva ao acervo filtrado, não à ficha do contêiner.",
    "documentapolitec": "Cada Enter da conferência redesenha a ficha inteira; em caixas grandes isso custa tempo.",
    "gestao-documentos": "O aviso da autoridade agora aparece no topo e na aba Conclusão.",
    "renovacao-contratos-horus": "Os fiscais do seed agora existem; o nome do fiscal ainda é digitado no painel.",
    "distribuicao-casos-dna": "Os poços da placa agora mostram o caso ao clique; não há ficha própria de caso.",
    "comissao-etica-denuncias": "O funil tem 7 etapas e a barra do caso tem 6; os nomes não coincidem.",
    "passivo-ambiental": "A fila do perito agora tem busca e filtro de atrasados.",
    "rnc-nao-conformidade": "O contexto de setor foi corrigido e preenche Minhas RNCs.",
    "tap-portfolio-projetos": "A matriz não tem escala numérica nos eixos; pontos próximos se sobrepõem.",
    "adiantamento": "Sem perfis e sem “minha fila”: todo mundo vê todos os processos.",
    "metas-bi-ocr": "O exemplo de CSV está na importação; conferência e geração ainda ficam no cartão do mês, fora do menu.",
    "inscricoes-cursos": "A Diretoria tem a Triagem, o formulário abre pelo botão e os passos sem tela aparecem como em breve.",
    "mapa-distribuicao-credor": "A importação agora tem a tabela de 3 linhas, mas a associação de colunas continua nos cartões.",
    "equipamentos-google-earth": "A lista agora pagina; o mapa é estático, sem zoom e sem arrastar.",
    "agiliza-mais": "Os passos sem tela aparecem como “em breve”; o caso de exemplo está no botão da tela de casos.",
}

FONTES = {"sistema": "system-ui, 'Segoe UI', sans-serif", "serifa": "Georgia, Cambria, serif",
          "condensada": "'Bahnschrift', 'Arial Narrow', sans-serif", "mono": "Consolas, 'Courier New', monospace",
          "arredondada": "'Trebuchet MS', 'Segoe UI', sans-serif"}

CSS = """
:root{--acento:#12487f;--tinta:#17212b;--tinta2:#5b6672;--papel:#fff;--fundo:#f2f4f7;--linha:#dce1e8;--suave:#eef3fa;--verde:#127a45;--ambar:#a35f00;--vermelho:#b42318}
*{box-sizing:border-box}
body{margin:0;background:var(--fundo);color:var(--tinta);font-family:system-ui,'Segoe UI',sans-serif;line-height:1.55}
a{color:var(--acento)}
.capa{background:linear-gradient(135deg,var(--acento),color-mix(in srgb,var(--acento) 62%,#0a1b2b));color:#fff;padding:42px 24px 30px}
.capa .in{max-width:1120px;margin:auto}
.capa .selo{display:inline-block;border:1px solid rgba(255,255,255,.5);border-radius:999px;padding:4px 12px;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.capa h1{font-size:clamp(26px,4vw,42px);margin:14px 0 8px;line-height:1.15}
.capa p{margin:0;max-width:820px;color:rgba(255,255,255,.86)}
.capa .meta{margin-top:14px;font-size:13px;color:rgba(255,255,255,.72)}
.capa nav{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.capa nav a{border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:8px 14px;color:#fff;text-decoration:none;font-size:13px}
.capa nav a.prim{background:#fff;color:var(--acento);border-color:#fff;font-weight:700}
main{max-width:1120px;margin:0 auto;padding:28px 24px 60px}
section{background:var(--papel);border:1px solid var(--linha);border-radius:14px;padding:24px;margin:20px 0;box-shadow:0 1px 0 var(--linha)}
section h2{margin:0 0 6px;font-size:23px}
section h3{margin:20px 0 8px;font-size:16px}
.sub{color:var(--tinta2);font-size:13.5px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:16px 0}
.kpi{background:var(--suave);border:1px solid var(--linha);border-radius:10px;padding:12px}
.kpi b{display:block;font-size:26px;line-height:1.1;color:var(--acento)}
.kpi span{font-size:12.5px;color:var(--tinta2)}
.figura{margin:14px 0 4px;text-align:center}
.figura img{display:block;width:100%;max-width:360px;height:auto;margin:0 auto;border:1px solid var(--linha);border-radius:10px;background:#fff}
.figura .sub{max-width:760px;margin:6px auto 0}
.fluxo{display:flex;gap:8px;overflow-x:auto;padding:6px 2px 12px}
.fluxo .passo{flex:0 0 190px;background:var(--papel);border:1px solid var(--linha);border-top:4px solid var(--acento);border-radius:10px;padding:12px}
.fluxo .passo .n{font-size:11px;color:var(--tinta2);letter-spacing:.08em;text-transform:uppercase}
.fluxo .passo b{display:block;margin:3px 0 5px;font-size:14px}
.fluxo .passo small{color:var(--tinta2);font-size:12px}
.fluxo .seta{align-self:center;color:var(--tinta2);font-size:18px}
.tabela{width:100%;max-width:100%;min-width:0;overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{border-bottom:1px solid var(--linha);padding:8px 9px;text-align:left;vertical-align:top}
th{background:var(--suave);font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--tinta2);white-space:nowrap}
tr:last-child td{border-bottom:0}
.duas{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.mvp-tabelas{display:grid;gap:16px}
.mvp-tabelas > *{min-width:0}
.duas > *{min-width:0}
@media(max-width:800px){.duas{grid-template-columns:1fr}}
.caixa{border-left:4px solid var(--acento);background:var(--suave);border-radius:0 10px 10px 0;padding:12px 14px;margin:12px 0}
.caixa.alerta{border-left-color:var(--ambar);background:#fdf6e8}
.caixa.verde{border-left-color:var(--verde);background:#eef8f2}
.tag{display:inline-block;border:1px solid var(--linha);border-radius:999px;padding:2px 9px;font-size:11.5px;color:var(--tinta2);margin:2px 4px 2px 0}
.tag.ok{border-color:var(--verde);color:var(--verde)}
.tag.auto{border-color:var(--acento);color:var(--acento)}
.lista{display:grid;gap:8px;margin:10px 0;padding:0;list-style:none}
.lista li{padding:10px 12px;border:1px solid var(--linha);border-radius:9px;background:#fff}
.lista b{color:var(--acento)}
.metricas{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
.metrica{border:1px solid var(--linha);border-radius:10px;padding:12px}
.metrica b{display:block;font-size:14px;margin-bottom:2px}
.metrica .base{color:var(--tinta2);font-size:12px}
.metrica .esperado{color:var(--verde);font-size:12px;font-weight:700}
.rodape{max-width:1120px;margin:0 auto;padding:0 24px 40px;color:var(--tinta2);font-size:12px}
code{font-family:Consolas,monospace;background:var(--suave);padding:1px 5px;border-radius:4px}
pre{background:#111a24;color:#e8eef6;border-radius:10px;padding:14px;overflow:auto;font-size:12.5px}
@media print{body{background:#fff}.capa{background:#fff;color:#000;border-bottom:2px solid #000}.capa a{color:#000}.capa .selo{border-color:#000}section{box-shadow:none;break-inside:avoid}nav{display:none}}
"""


def esc(v):
    return html.escape(str(v if v is not None else ""))


def texto(row, *chaves):
    for chave in chaves:
        if row.get(chave):
            return str(row[chave])
    return ""


def soma_tempos(linhas):
    total = 0.0
    for linha in linhas:
        nums = re.findall(r"\d+(?:[.,]\d+)?", str(linha.get("tempo", "")))
        valores = [float(n.replace(",", ".")) for n in nums]
        if len(valores) == 1:
            total += valores[0]
        elif len(valores) > 1:
            total += sum(valores) / len(valores)
    return total


def tabela_asis(linhas):
    if not linhas:
        return '<p class="sub">A tabela AS-IS não veio no projeto.</p>'
    corpo = "".join(f"<tr><td>{esc(texto(l, 'etapa'))}</td><td>{esc(texto(l, 'papel'))}</td><td>{esc(texto(l, 'entra'))}</td>"
                    f"<td>{esc(texto(l, 'acao'))}</td><td>{esc(texto(l, 'sai'))}</td><td>{esc(texto(l, 'sistema'))}</td>"
                    f"<td>{esc(texto(l, 'regra'))}</td><td>{esc(texto(l, 'espera'))}</td><td>{esc(texto(l, 'tempo'))}</td>"
                    f"<td>{esc(texto(l, 'auto'))}</td></tr>" for l in linhas)
    return ('<div class="tabela"><table><thead><tr><th>Etapa</th><th>Quem faz</th><th>Entra</th><th>Ação</th><th>Sai</th>'
            '<th>Sistema</th><th>Regra</th><th>Onde espera</th><th>Tempo</th><th>Automatizável</th></tr></thead>'
            f"<tbody>{corpo}</tbody></table></div>")


def tabela_tobe(linhas):
    if not linhas:
        return '<p class="sub">A tabela TO-BE não veio no projeto.</p>'
    corpo = "".join(f"<tr><td>{esc(texto(l, 'etapa'))}</td><td>{esc(texto(l, 'muda'))}</td><td>{esc(texto(l, 'quem'))}</td>"
                    f"<td>{esc(texto(l, 'beneficio'))}</td><td>{esc(texto(l, 'esforco'))}</td></tr>" for l in linhas)
    return ('<div class="tabela"><table><thead><tr><th>Etapa</th><th>O que muda</th><th>Quem faz</th><th>Benefício</th><th>Esforço</th></tr></thead>'
            f"<tbody>{corpo}</tbody></table></div>")


def cartoes_tobe(linhas):
    return "".join(f'<li><b>{esc(texto(l, "etapa"))}</b><br>{esc(texto(l, "muda"))}'
                   f'<br><span class="tag ok">{esc(texto(l, "quem"))}</span>'
                   f'<span class="tag">{esc(texto(l, "beneficio"))}</span></li>' for l in linhas)


def tabela_metricas(linhas):
    if not linhas:
        return '<p class="sub">As métricas não vieram no projeto.</p>'
    return '<div class="metricas">' + "".join(
        f'<div class="metrica"><b>{esc(texto(l, "nome"))}</b><span class="base">{esc(texto(l, "pergunta"))}</span>'
        f'<div class="base">Base: {esc(texto(l, "base"))}</div><div class="esperado">Esperado: {esc(texto(l, "esperado"))}</div>'
        f'<div class="base">Fonte: {esc(texto(l, "fonte"))}</div></div>' for l in linhas) + "</div>"


def tabela_regras(linhas):
    if not linhas:
        return '<p class="sub">As regras não vieram no projeto.</p>'
    corpo = "".join(f"<tr><td><code>{esc(texto(l, 'id'))}</code></td><td>{esc(texto(l, 'regra'))}</td>"
                    f"<td>{esc(texto(l, 'quando'))}</td><td>{esc(texto(l, 'tipo'))}</td><td>{esc(texto(l, 'excecao'))}</td></tr>" for l in linhas)
    return ('<div class="tabela"><table><thead><tr><th>ID</th><th>Regra</th><th>Quando</th><th>Tipo</th><th>Exceção</th></tr></thead>'
            f"<tbody>{corpo}</tbody></table></div>")


def tabela_papeis(linhas):
    if not linhas:
        return '<p class="sub">Os papéis não vieram no projeto.</p>'
    corpo = "".join(f"<tr><td><b>{esc(texto(l, 'papel'))}</b></td><td>{esc(texto(l, 'quem'))}</td><td>{esc(texto(l, 've'))}</td>"
                    f"<td>{esc(texto(l, 'faz'))}</td><td>{esc(texto(l, 'naofaz'))}</td><td>{esc(texto(l, 'registro'))}</td></tr>" for l in linhas)
    return ('<div class="tabela"><table><thead><tr><th>Papel</th><th>Quem é</th><th>O que vê</th><th>O que faz</th><th>O que não faz</th><th>Registro</th></tr></thead>'
            f"<tbody>{corpo}</tbody></table></div>")


def gerar(app):
    pasta = RAIZ / app
    cfg = json.loads((pasta / "app.json").read_text(encoding="utf-8"))
    proj = json.loads((pasta / "projeto.json").read_text(encoding="utf-8"))
    campos = proj.get("campos", {})
    tab = proj.get("tabelas", {})
    asis = [l for l in tab.get("tAsIs", []) if any(str(v or "").strip() for v in l.values())]
    tobe = [l for l in tab.get("tToBe", []) if any(str(v or "").strip() for v in l.values())]
    tempos = soma_tempos(asis)
    auto = sum(1 for l in asis if str(l.get("auto", "")).lower().startswith("sim"))
    esperas = sum(1 for l in asis if texto(l, "espera") and "não identificado" not in texto(l, "espera").lower())
    vis = cfg.get("visual", {})
    acento = vis.get("acento", "#12487f")
    fonte = FONTES.get(vis.get("fonte", "sistema"), FONTES["sistema"])
    nome = campos.get("nome_projeto") or cfg.get("titulo") or app
    setor = vis.get("setor") or cfg.get("subtitulo") or ""
    aluno = campos.get("aluno") or ""
    unidade = campos.get("unidade") or ""
    data = campos.get("data") or ""
    problema = campos.get("problema") or ""
    hoje = campos.get("hoje") or ""
    impacto = campos.get("impacto") or ""
    resumo = campos.get("resumo") or ""
    mudanca = campos.get("tobe_mudanca") or ""
    visao = campos.get("tobe_visao") or ""
    passos = "".join(f'<div class="passo"><span class="n">{i + 1}</span><b>{esc(texto(l, "etapa"))}</b>'
                     f'<small>{esc(texto(l, "papel") or texto(l, "quem"))}</small></div>'
                     + ('<span class="seta">→</span>' if i < len(asis) - 1 else "")
                     for i, l in enumerate(asis))
    menus = [r for r in cfg.get("rotas", []) if r.get("menu") is not False and ":" not in r.get("rota", "") and not r.get("publica")]
    menu_html = "".join(f'<span class="tag">{esc(r.get("titulo"))}</span>' for r in menus)
    modulo_html = ""
    if app == "gestao_identificados":
        modulo_html = """<section id="modulo"><h2>Módulo de desaparecidos</h2>
  <p class="sub">Painel público do CNPD/MJ com os registros de pessoas desaparecidas, em uma página separada para não misturar a base pública com o cadastro dos corpos. O módulo é construído pela outra IA; o contrato está em <a href="docs/CONTRATO-DESAPARECIDOS.md">docs/CONTRATO-DESAPARECIDOS.md</a>.</p>
  <p><a class="prim" style="display:inline-block;background:#fff;color:var(--acento);padding:10px 16px;border-radius:999px;text-decoration:none;font-weight:700" href="desaparecidos.html">Abrir o painel de desaparecidos →</a></p></section>

"""
    html_doc = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AS-IS e TO-BE · {esc(nome)}</title>
<style>{CSS}
body{{font-family:{fonte}}}
:root{{--acento:{acento}}}
</style></head><body>
<header class="capa"><div class="in">
  <span class="selo">MVP · {esc(app)}</span>
  <h1>{esc(nome)}</h1>
  <p>{esc(resumo[:420])}{'…' if len(resumo) > 420 else ''}</p>
  <div class="meta">{esc(aluno)} · {esc(unidade)} · {esc(data)} · {esc(setor)}</div>
  <nav><a href="#asis">Antes · AS-IS</a><a href="#tobe">Depois · TO-BE</a><a href="#mvp">O MVP</a><a class="prim" href="index.html">Abrir o MVP →</a></nav>
</div></header>
<main>
<section id="problema"><h2>O problema</h2><p>{esc(problema)}</p>
  <div class="duas"><div class="caixa alerta"><b>Como é hoje</b><br>{esc(hoje)}</div>
  <div class="caixa"><b>Impacto</b><br>{esc(impacto)}</div></div></section>

<section id="asis"><h2>AS-IS · o processo antes do MVP</h2>
  <p class="sub">O caminho real, com quem faz, o que entra, onde espera e o que é automatizável. Fonte: tabela AS-IS do projeto.</p>
  <div class="figura"><img src="docs/diagramas/as-is.svg" alt="Fluxograma AS-IS"><p class="sub">Fluxograma AS-IS · amarelo: etapa manual; tracejado: ponto de espera. Os números correspondem à tabela. <a href="docs/diagramas/processo.md">Fonte Mermaid</a>.</p></div>
  <div class="kpis"><div class="kpi"><b>{len(asis)}</b><span>etapas</span></div>
    <div class="kpi"><b>{tempos:g}</b><span>tempo declarado (h)</span></div>
    <div class="kpi"><b>{esperas}</b><span>pontos de espera</span></div>
    <div class="kpi"><b>{auto}</b><span>etapas automatizáveis</span></div></div>
  <div class="fluxo">{passos}</div>
  {tabela_asis(asis)}
</section>

<section id="tobe"><h2>TO-BE · o processo com o MVP</h2>
  <p class="sub">O que muda em cada etapa, quem passa a fazer e o ganho esperado. Fonte: tabela TO-BE do projeto.</p>
  <div class="figura"><img src="docs/diagramas/to-be.svg" alt="Fluxograma TO-BE"><p class="sub">Fluxograma TO-BE · verde: máquina (automação local); azul: pessoa (fé pública). <a href="docs/diagramas/processo.md">Fonte Mermaid</a>.</p></div>
  <div class="kpis"><div class="kpi"><b>{len(tobe)}</b><span>etapas no novo fluxo</span></div>
    <div class="kpi"><b>{max(0, len(asis) - len(tobe))}</b><span>etapas a menos</span></div>
    <div class="kpi"><b>{auto}</b><span>etapas que saem do trabalho manual</span></div></div>
  {('<div class="caixa verde"><b>Mudança central:</b> ' + esc(mudanca) + '</div>') if mudanca else ''}
  {('<p>' + esc(visao) + '</p>') if visao else ''}
  <ul class="lista">{cartoes_tobe(tobe)}</ul>
  {tabela_tobe(tobe)}
  <div class="caixa alerta"><b>Leitura crítica:</b> {esc(CRITICA.get(app, "O MVP cobre o fluxo principal; o que ainda é manual está na coluna quem."))}</div>
</section>

<section id="mvp"><h2>O que o MVP entrega</h2>
  <p><b>Tela-assinatura:</b> {esc(ASSINATURA.get(app, "A tela inicial do app."))}.</p>
  <p class="sub">Menu do MVP: {menu_html}</p>
  <div class="mvp-tabelas"><div><h3>Regras de negócio</h3>{tabela_regras(tab.get("tRegras", []))}</div>
    <div><h3>Papéis</h3>{tabela_papeis(tab.get("tPapeis", []))}</div></div>
  <h3>Métricas do piloto</h3>{tabela_metricas(tab.get("tMetricas", []))}
</section>

{modulo_html}<section id="teste"><h2>Como testar</h2>
  <p class="sub">O MVP é um `index.html` offline, com dados fictícios. Abra <a href="index.html">index.html</a>.</p>
  <pre>cd Apps/{app}
python construir.py
python testes/testar.py
python testes/cenarios.py
python testes/jornada.py

# Lightpanda (via WSL, CDP em 9222 e HTTP em 8000)
python testes/jornada.py --cdp http://127.0.0.1:9222 --base http://127.0.0.1:8000</pre>
  <p class="sub">Documentos: <a href="PROJETO.md">PROJETO.md</a> · <a href="sprint.md">sprint.md</a> · <a href="README.md">README.md</a></p>
</section>
</main>
<footer class="rodape">Gerado a partir de <code>projeto.json</code> e <code>app.json</code> · POLITEC/MT · {esc(nome)}</footer>
</body></html>"""
    (pasta / "processo.html").write_text(html_doc, encoding="utf-8")
    return len(html_doc)


def main():
    for pasta in sorted(RAIZ.iterdir()):
        if not pasta.is_dir() or pasta.name.startswith("_"):
            continue
        if not (pasta / "projeto.json").exists():
            print("sem projeto.json:", pasta.name)
            continue
        n = gerar(pasta.name)
        print(f"ok {pasta.name:32s} {n / 1024:6.1f} KB")


if __name__ == "__main__":
    main()

