"""Gera o README.md desta pasta: indice dos trabalhos de BI da Aula 7/8.

Le cada .pbix (zip) e cada projeto .pbip, extrai as paginas do relatorio e
conta os visuais. Nao abre o Power BI. Uso:
  python "Aula 8/Entregas BI/gerar_indice.py"
"""
import json
import pathlib
import zipfile

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
EQUIPES = json.loads((RAIZ / "Apps/equipes.json").read_text(encoding="utf-8"))

# nome do arquivo -> (aluno, app)
MAPA = {
    "andreia": ("Andreia Cristina", "agiliza-mais"),
    "edilaura": ("Edilaura Rondon", "inscricoes-cursos"),
    "dashboard-andr": ("André", "cin-segunda-via"),
    "edjane": ("Edjane Ávila", "custodia-definitiva"),
    "elthon": ("Elthon Teixeira", "agendamento-cin"),
    "luciana": ("Luciana", "distribuicao-casos-dna"),
    "flavia": ("Flávia", "cin-segunda-via"),
    "francineide": ("Francineide da Silva", "agiliza-mais"),
    "jaque": ("Jaqueline", "adiantamento"),
    "joao lucas": ("João Lucas Nogueira Ponce", "equipamentos-google-earth"),
    "karine": ("Karine Assunção", "metas-bi-ocr"),
    "linicker": ("Linicker", "adiantamento"),
    "nelson": ("Nelson", "distribuicao-casos-dna"),
    "letícia": ("Letícia", "comissao-etica-denuncias"),
    "leticia": ("Letícia", "comissao-etica-denuncias"),
    "rodrigo": ("Rodrigo Neves Ribeiro", "renovacao-contratos-horus"),
    "sabrina": ("Sabrina Ellen", "rnc-nao-conformidade"),
    "silmara": ("Silmara", None),
    "thiago": ("Thiago", "comissao-etica-denuncias"),
    "francis": ("Francis Souza", None),
    "iohan": ("Iohan Camões de Albuquerque", "horus-banco-demandas"),
}


def quem(nome):
    baixo = nome.lower()
    for chave, (aluno, app) in MAPA.items():
        if chave in baixo:
            return aluno, app
    return "a identificar", None


def paginas_pbix(arq):
    with zipfile.ZipFile(arq) as z:
        texto = z.read("Report/Layout").decode("utf-16-le").lstrip("\ufeff")
    j = json.loads(texto)
    return [(s.get("displayName") or "(sem nome)", len(s.get("visualContainers", []))) for s in j.get("sections", [])]


def paginas_pbip(arq):
    pasta = arq.with_suffix("")
    pasta = arq.parent / (arq.stem + ".Report")
    paginas = []
    for f in sorted((pasta / "definition/pages").glob("*/page.json")):
        j = json.loads(f.read_text(encoding="utf-8"))
        paginas.append((j.get("displayName") or f.parent.name, None))
    return paginas


def main():
    linhas = []
    for arq in sorted(AQUI.iterdir()):
        if arq.suffix.lower() not in (".pbix", ".pbip"):
            continue
        aluno, app = quem(arq.name)
        try:
            paginas = paginas_pbix(arq) if arq.suffix.lower() == ".pbix" else paginas_pbip(arq)
            erro = ""
        except Exception as e:  # noqa: BLE001
            paginas, erro = [], f"não consegui ler: {type(e).__name__}"
        vis = sum(n for _, n in paginas if n is not None)
        nomes = "; ".join(n for n, _ in paginas[:6]) + ("…" if len(paginas) > 6 else "")
        linhas.append((arq.name, aluno, app, f"{arq.stat().st_size / 1024 / 1024:.2f} MB", len(paginas), vis, nomes, erro))

    total = len(linhas)
    n_pbix = sum(1 for x in linhas if x[0].lower().endswith(".pbix"))
    n_pbip = total - n_pbix
    txt = ["# Entregas de BI · Aula 7/8", "",
           "Trabalhos de Power BI entregues pela turma. O índice é gerado por",
           "`gerar_indice.py`, que lê as páginas e os visuais de cada `.pbix` (zip) e de",
           "cada projeto `.pbip`, sem abrir o Power BI.", "",
           f"**{total} trabalhos** ({n_pbix} `.pbix`, {n_pbip} `.pbip`).", "",
           "| Arquivo | Aluno | App relacionado | Tamanho | Páginas | Visuais | Páginas do relatório |",
           "|---|---|---|---:|---:|---:|---|"]
    for nome, aluno, app, tam, npag, vis, nomes, erro in linhas:
        txt.append(f"| `{nome}` | {aluno} | {('`' + app + '`') if app else '—'} | {tam} | {npag} | {vis or '—'} | {nomes or (erro or '—')} |")
    txt += ["", "## O que falta nesta pasta", "",
            "- **Silmara** entregou BI e não aparece em nenhuma equipe do formulário (`Apps/equipes.json`); confirmar o projeto.",
            "- **Francis Souza** entregou o projeto `.pbip` (Painel Gargalo Ouvidoria) e ainda não tem app vinculado.",
            "- Os arquivos são binários e grandes; nenhum está publicado no site. Se forem publicados, precisam de uma página de índice e de autorização dos alunos.",
            "- A avaliação de conteúdo (medidas, modelagem, narrativa) não é feita por este índice; ele só descreve o que existe.",
            "- Alunos sem entrega de BI nesta pasta: Diego Costa, Glauce, Danielle, Aline, Kasteline, Fábio, Vitória e Luciana não aparecem (ou aparecem por outro nome).",
            "", "Gerar de novo: `python \"Aula 8/Entregas BI/gerar_indice.py\"`.", ""]
    (AQUI / "README.md").write_text("\n".join(txt), encoding="utf-8")
    print(f"README.md: {total} trabalhos")


if __name__ == "__main__":
    main()
