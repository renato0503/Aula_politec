"""Gera os fluxogramas AS-IS e TO-BE de cada app em Mermaid + SVG.

Lê `projeto.json` (tabelas `tAsIs` e `tToBe`), escreve:
  Apps/<app>/docs/diagramas/as-is.mmd
  Apps/<app>/docs/diagramas/to-be.mmd
  Apps/<app>/docs/diagramas/processo.md  (os dois blocos Mermaid)
  Apps/<app>/docs/diagramas/as-is.svg
  Apps/<app>/docs/diagramas/to-be.svg

O SVG é renderizado com o Mermaid local (npm) e Playwright, para o hub
`processo.html` continuar offline. O Mermaid não entra no app.

Quando existe `docs/diagramas/to-be.manual.mmd` (ou `as-is.manual.mmd`), ele vale
no lugar do fluxograma gerado pela tabela: é o caso de um fluxo com decisões que a
tabela linear não representa (ex.: `trilha-custodia-necropsia`, Sprint 9).

Uso: python Apps/_base/gerar_diagramas.py [app ...]
Requer: npm install mermaid@11 em MERMAID_DIR e Playwright/Chromium.
"""
import html
import json
import pathlib
import re

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MERMAID_DIR = pathlib.Path(r"C:\Users\Renato\AppData\Local\Temp\mermaid-render")
LIB = MERMAID_DIR / "node_modules" / "mermaid" / "dist" / "mermaid.min.js"


def limpar(texto, limite=62):
    texto = re.sub(r"\s+", " ", str(texto or "")).strip()
    texto = html.escape(texto, quote=True)
    return texto if len(texto) <= limite else texto[:limite - 1] + "…"


def nos(linhas, tipo):
    linhas = [l for l in linhas if str(l.get("etapa") or "").strip()]
    direcao = "TD"
    out = [f"%% Fluxograma {tipo.upper()} · {len(linhas)} etapas", f"flowchart {direcao}"]
    out.append('  IN(["Início"])')
    ids = []
    for i, l in enumerate(linhas):
        nid = f"N{i + 1}"
        ids.append(nid)
        etapa = limpar(l.get("etapa"), 58)
        if tipo == "asis":
            rotulo = f"{i + 1}. {etapa}"
            espera = str(l.get("espera") or "").lower()
            classe = "wait" if espera and "não identificado" not in espera and "nao identificado" not in espera else "manual"
        else:
            quem = limpar(l.get("quem"), 30)
            rotulo = f"{i + 1}. {etapa}<br/><small>{quem}</small>"
            classe = "auto" if "máquina" in str(l.get("quem") or "").lower() or "maquina" in str(l.get("quem") or "").lower() else "humano"
        out.append(f'  {nid}["{rotulo}"]::: {classe}'.replace("::: ", ":::"))
    out.append('  FIM(["Fim"])')
    if ids:
        out.append(f"  IN --> {ids[0]}")
        for a, b in zip(ids, ids[1:]):
            out.append(f"  {a} --> {b}")
        out.append(f"  {ids[-1]} --> FIM")
    else:
        out.append("  IN --> FIM")
    out.append("  classDef manual fill:#fff4e5,stroke:#a35f00,color:#3b2a00;")
    out.append("  classDef wait fill:#fff4e5,stroke:#a35f00,stroke-dasharray:5 3,color:#3b2a00;")
    out.append("  classDef auto fill:#eef8f2,stroke:#127a45,color:#0b3b23;")
    out.append("  classDef humano fill:#eef3fa,stroke:#12487f,color:#0a2f5c;")
    return "\n".join(out)


def gerar(app, pasta, tab):
    asis = tab.get("tAsIs", [])
    tobe = tab.get("tToBe", [])
    destino = pasta / "docs" / "diagramas"
    destino.mkdir(parents=True, exist_ok=True)
    m_asis = nos(asis, "asis")
    m_tobe = nos(tobe, "tobe")
    manual = {n: destino / f"{n}.manual.mmd" for n in ("as-is", "to-be")}
    if manual["as-is"].exists():
        m_asis = manual["as-is"].read_text(encoding="utf-8").strip()
    if manual["to-be"].exists():
        m_tobe = manual["to-be"].read_text(encoding="utf-8").strip()
    (destino / "as-is.mmd").write_text(m_asis + "\n", encoding="utf-8")
    (destino / "to-be.mmd").write_text(m_tobe + "\n", encoding="utf-8")
    md = f"""# Fluxogramas do processo · {app}

Gerados a partir de `projeto.json` (as setas seguem a ordem da tabela) ou de `*.manual.mmd`, quando existe.

## AS-IS

```mermaid
{m_asis}
```

## TO-BE

```mermaid
{m_tobe}
```
"""
    (destino / "processo.md").write_text(md, encoding="utf-8")
    return m_asis, m_tobe


def main():
    if not LIB.exists():
        raise SystemExit(f"Mermaid não encontrado em {LIB}. Rode: cd {MERMAID_DIR} && npm install mermaid@11")
    import sys
    filtro = set(sys.argv[1:])
    dados = []
    for pasta in sorted(RAIZ.iterdir()):
        if not pasta.is_dir() or pasta.name.startswith("_"):
            continue
        if filtro and pasta.name not in filtro:
            continue
        if not (pasta / "projeto.json").exists():
            continue
        proj = json.loads((pasta / "projeto.json").read_text(encoding="utf-8"))
        m_asis, m_tobe = gerar(pasta.name, pasta, proj.get("tabelas", {}))
        dados.append((pasta.name, m_asis, m_tobe))

    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page()
        pg.set_content("<!doctype html><html><body></body></html>")
        pg.add_script_tag(path=str(LIB))
        pg.evaluate("""() => mermaid.initialize({startOnLoad:false, theme:'base', securityLevel:'loose',
            flowchart:{htmlLabels:true, curve:'basis'}})""")
        for app, m_asis, m_tobe in dados:
            destino = RAIZ / app / "docs" / "diagramas"
            for nome, codigo in (("as-is", m_asis), ("to-be", m_tobe)):
                svg = pg.evaluate("""async ({codigo, id}) => {
                    const r = await mermaid.render(id, codigo);
                    return r.svg;
                }""", {"codigo": codigo, "id": f"{app}-{nome}".replace("-", "_")})
                (destino / f"{nome}.svg").write_text(svg, encoding="utf-8")
                print(f"ok {app:32s} {nome:6s} {len(svg) / 1024:5.1f} KB")
        nav.close()


if __name__ == "__main__":
    main()
