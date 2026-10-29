"""Registra o login do GitHub de um aluno no app dele e atualiza a tabela do Apps/README.md.

Fonte: Apps/equipes.json (um repositório por app, compartilhado com a equipe).

Uso:
  python Apps/_base/equipes.py                          só refaz a tabela do README
  python Apps/_base/equipes.py <app> "<nome>" <login>   grava o login (o nome casa pelo início, sem acento)
"""
import json
import pathlib
import re
import sys
import unicodedata

APPS = pathlib.Path(__file__).resolve().parent.parent
ARQ = APPS / "equipes.json"


def sem_acento(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower().strip()


def gravar_login(e, app, nome, login):
    alunos = e["apps"][app]["alunos"]
    achou = [a for a in alunos if sem_acento(a["nome"]).startswith(sem_acento(nome)) or sem_acento(nome).startswith(sem_acento(a["nome"]))]
    if achou:
        achou[0]["github"] = login
    else:
        alunos.append({"nome": nome, "email": None, "github": login})
    e["sem_projeto"] = [s for s in e.get("sem_projeto", []) if s["github"] != login]


def tabela(e):
    linhas = ["## Equipes e GitHub", "", "Fonte: `equipes.json` (usado para criar um repositório por app e dar acesso à equipe).",
              "Para acrescentar um login: `python Apps/_base/equipes.py <app> \"<nome>\" <login>`.", "",
              "| App | Integrantes | GitHub |", "|---|---|---|"]
    for app, d in sorted(e["apps"].items()):
        gh = ", ".join(f"`{a['github']}` ({a['nome'].split()[0]})" for a in d["alunos"] if a["github"]) or "a informar"
        linhas.append(f"| {app} | {', '.join(a['nome'] for a in d['alunos'])} | {gh} |")
    for s in e.get("sem_projeto", []):
        linhas.append(f"| (sem projeto) | {s['nome']} | `{s['github']}` |")
    return "\n".join(linhas) + "\n"


def main():
    e = json.loads(ARQ.read_text(encoding="utf-8"))
    if len(sys.argv) == 4:
        gravar_login(e, *sys.argv[1:])
        ARQ.write_text(json.dumps(e, ensure_ascii=False, indent=2), encoding="utf-8")
    readme = APPS / "README.md"
    t = readme.read_text(encoding="utf-8")
    bloco = tabela(e)
    t = re.sub(r"## Equipes e GitHub\n.*?(?=\n## |\Z)", bloco, t, flags=re.S) if "## Equipes e GitHub" in t else t.rstrip() + "\n\n" + bloco
    readme.write_text(t, encoding="utf-8")
    com = sum(1 for d in e["apps"].values() for a in d["alunos"] if a["github"])
    total = sum(len(d["alunos"]) for d in e["apps"].values())
    print(f"{com} de {total} alunos com GitHub")


if __name__ == "__main__":
    main()
