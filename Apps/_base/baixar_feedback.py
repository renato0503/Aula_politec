"""Baixa o feedback dos alunos (coleção `feedback_apps` do Firestore) e escreve
o Apps/<app>/FEEDBACK.md de cada app que recebeu resposta.

O FEEDBACK.md é a entrada do próximo ciclo de desenvolvimento: prioridades,
telas com erro ou ajuste, o que falta e as regras que não batem com o processo.
Cada item vira uma linha de checklist para marcar no sprint.md.

A leitura usa a API REST pública do Firestore (as regras liberam leitura), sem
credencial. Respostas com o nome começando por "TESTE AUTOMATIZADO" são
ignoradas.

Uso: python Apps/_base/baixar_feedback.py            (todos os apps)
     python Apps/_base/baixar_feedback.py <app>      (um app)
"""
import collections
import datetime as dt
import json
import pathlib
import sys
import urllib.request

APPS = pathlib.Path(__file__).resolve().parent.parent
PROJETO = "aulapolitec"
CHAVE = "AIzaSyBmMTIdsrY7sfzgmzzz_5wcaDa0p8kIgVg"  # chave web pública do app (a mesma de Aula 8/firebase-config.js)
URL = f"https://firestore.googleapis.com/v1/projects/{PROJETO}/databases/(default)/documents/feedback_apps"
SIT = {"ok": "funciona como esperado", "ajuste": "precisa de ajuste", "erro": "não funciona ou deu erro"}
PAPEL = {"equipe": "equipe do app", "usuario": "servidor do setor", "outro": "outro"}
USARIA = {"sim": "sim, como está", "ajustes": "sim, com ajustes", "nao": "não"}


def valor(v):
    """Converte o formato tipado da API REST do Firestore para Python."""
    if "stringValue" in v: return v["stringValue"]
    if "integerValue" in v: return int(v["integerValue"])
    if "doubleValue" in v: return v["doubleValue"]
    if "booleanValue" in v: return v["booleanValue"]
    if "timestampValue" in v: return v["timestampValue"]
    if "nullValue" in v: return None
    if "arrayValue" in v: return [valor(x) for x in v["arrayValue"].get("values", [])]
    if "mapValue" in v: return {k: valor(x) for k, x in v["mapValue"].get("fields", {}).items()}
    return None


def baixar():
    docs, token = [], ""
    while True:
        url = f"{URL}?key={CHAVE}&pageSize=300" + (f"&pageToken={token}" if token else "")
        with urllib.request.urlopen(url, timeout=60) as r:
            d = json.loads(r.read().decode("utf-8"))
        for doc in d.get("documents", []):
            item = {k: valor(v) for k, v in doc.get("fields", {}).items()}
            item["id"] = doc["name"].rsplit("/", 1)[-1]
            docs.append(item)
        token = d.get("nextPageToken")
        if not token:
            return docs


def markdown(app, respostas):
    titulo = respostas[0].get("projeto") or app
    notas = [r["nota"] for r in respostas if r.get("nota")]
    L = [f"# Feedback dos alunos · {titulo}", "",
         f"Gerado por `python Apps/_base/baixar_feedback.py` em {dt.date.today():%d/%m/%Y}, a partir da coleção `feedback_apps` do Firestore.",
         f"{len(respostas)} resposta(s) · nota média {sum(notas) / len(notas):.1f} de 5".replace(".", ",") if notas else f"{len(respostas)} resposta(s)", "",
         "Use este arquivo para abrir o próximo sprint: cada item vira uma linha do `sprint.md`. Os números com fonte são da própria resposta.", ""]
    usaria = collections.Counter(USARIA.get(r.get("usaria"), r.get("usaria") or "—") for r in respostas)
    piloto = collections.Counter(r.get("piloto") or "sem resposta" for r in respostas)
    L += ["## Resumo", "", f"- Usaria no trabalho: " + "; ".join(f"{k} ({v})" for k, v in usaria.most_common()),
          f"- Piloto: " + "; ".join(f"{k} ({v})" for k, v in piloto.most_common()), ""]
    prios = [(r["aluno"], i + 1, p) for r in respostas for i, p in enumerate(r.get("prioridades") or [])]
    if prios:
        L += ["## Prioridades (na ordem de cada pessoa)", ""] + [f"- [ ] {p} _({a}, {n}ª)_" for a, n, p in sorted(prios, key=lambda x: x[1])] + [""]
    telas = collections.defaultdict(list)
    for r in respostas:
        for t in r.get("telas") or []:
            telas[(t.get("rota"), t.get("titulo"))].append((r["aluno"], t.get("situacao"), t.get("comentario")))
    if telas:
        L += ["## Tela por tela", ""]
        for (rota, nome), itens in sorted(telas.items(), key=lambda kv: -sum(1 for x in kv[1] if x[1] in ("erro", "ajuste"))):
            cont = collections.Counter(SIT.get(s, "não testou") for _, s, _ in itens)
            L += [f"### {nome} (`{rota}`)", "", "Situação: " + "; ".join(f"{k} ({v})" for k, v in cont.items()), ""]
            L += [f"- [ ] {c} _({a})_" for a, s, c in itens if c] + [""]
    for chave, rotulo in [("erros", "Erros encontrados"), ("falta", "O que falta"), ("regras", "Regras, nomes e números que não batem"), ("observacoes", "Observações")]:
        itens = [(r["aluno"], r.get(chave)) for r in respostas if r.get(chave)]
        if itens:
            L += [f"## {rotulo}", ""] + [f"- [ ] {t} _({a})_" for a, t in itens] + [""]
    L += ["## Quem respondeu", ""] + [f"- {r['aluno']} · {PAPEL.get(r.get('papel'), r.get('papel'))}{' · ' + r['setor'] if r.get('setor') else ''} · nota {r.get('nota')} · {str(r.get('criadoEm', ''))[:10]}" for r in respostas] + [""]
    return "\n".join(L)


def main():
    filtro = sys.argv[1] if len(sys.argv) > 1 else None
    docs = [d for d in baixar() if not str(d.get("aluno", "")).startswith("TESTE AUTOMATIZADO")]
    por_app = collections.defaultdict(list)
    for d in docs:
        por_app[d.get("app")].append(d)
    print(f"{len(docs)} resposta(s) em {len(por_app)} app(s)")
    for app, respostas in sorted(por_app.items()):
        if filtro and app != filtro:
            continue
        if not app or not (APPS / app / "app.json").exists():
            print("  app desconhecido:", app); continue
        respostas.sort(key=lambda r: str(r.get("criadoEm", "")))
        (APPS / app / "FEEDBACK.md").write_text(markdown(app, respostas), encoding="utf-8")
        print(f"  {app}: {len(respostas)} resposta(s) -> Apps/{app}/FEEDBACK.md")


if __name__ == "__main__":
    main()
