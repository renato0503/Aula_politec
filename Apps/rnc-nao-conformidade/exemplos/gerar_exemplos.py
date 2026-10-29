"""Gera 20 RNCs fictícias e a planilha do Forms em CSV (Sprint 0).

Saídas:
  respostas-forms-ficticio.csv   formato SUPOSTO da planilha de respostas (trocar pelo cabeçalho real)
  seed.json                      setores, RNCs e etapas no formato do app

Casos: anulada (sem complemento em 5 dias), prorrogada, recorrente (mesmo setor e
categoria em 90 dias), grave (corregedoria), em cada etapa. Só setores, sem nomes.
Semente fixa = 20261029.
Uso: python "Apps/rnc-nao-conformidade/exemplos/gerar_exemplos.py"
"""
import csv
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)
SETORES = [("LQF", "Laboratório de Química Forense"), ("LGF", "Laboratório de Genética Forense"), ("LTX", "Laboratório de Toxicologia"),
           ("REC", "Recepção de vestígios"), ("ALM", "Almoxarifado"), ("CUS", "Central de Custódia")]
CATEGORIAS = ["Cadeia de custódia", "Registro incompleto", "Equipamento sem calibração", "Prazo de laudo", "Armazenamento de amostra", "Biossegurança"]
ETAPAS = ["validação", "plano", "avaliação", "encerramento"]


def main():
    base = dt.date(2026, 9, 1)
    rncs, etapas, linhas = [], [], []
    for n in range(20):
        aberta = base + dt.timedelta(days=n * 2 + random.randint(0, 1))
        rel, notif = random.sample(SETORES, 2)
        if n in (3, 9, 15):
            notif = SETORES[0]
            cat = "Registro incompleto"  # recorrência (RN05)
        else:
            cat = random.choice(CATEGORIAS)
        numero = f"DLF/2026-{n + 1:03d}"
        ate = [3, 3, 2, 3, 1, 1, 2, 0, 3, 2, 1, 1, 0, 2, 1, 1, 0, 1, 0, 1][n]
        situacao = "encerrada" if ate == 3 else "aberta"
        if n == 7:
            situacao = "anulada"
        grave = n == 12
        dia = aberta
        for i in range(ate + 1):
            dur = {0: random.randint(1, 3), 1: random.randint(10, 38), 2: random.randint(2, 6), 3: 1}[i]
            fim = dia + dt.timedelta(days=dur) if (i < ate or situacao == "encerrada") else None
            prazo = dia + dt.timedelta(days=5 if i == 0 else 30 if i == 1 else 10)
            etapas.append({"id": f"{numero}#{i}", "rnc": numero, "etapa": ETAPAS[i], "inicio": dia.isoformat(),
                           "fim": fim.isoformat() if fim else None, "prazo": prazo.isoformat()})
            if fim:
                dia = fim
        rncs.append({"numero": numero, "aberta_em": aberta.isoformat(), "setor_relator": rel[0], "setor_notificado": notif[0], "categoria": cat,
                     "gravidade": "grave" if grave else random.choice(["leve", "moderada"]), "descricao": f"Ocorrência fictícia {n + 1} ({cat.lower()}).",
                     "etapa": ETAPAS[ate], "situacao": "encaminhada à corregedoria" if grave else situacao})
        linhas.append({"Carimbo de data/hora": f"{aberta.strftime('%d/%m/%Y')} 09:{n:02d}:00", "Setor relator": rel[1], "Setor notificado": notif[1],
                       "Categoria": cat, "Descrição da ocorrência": rncs[-1]["descricao"], "Gravidade": rncs[-1]["gravidade"], "Número": numero})
    with open(AQUI / "respostas-forms-ficticio.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    seed = {"setores": [{"sigla": s, "nome": n, "diretoria": "DLF"} for s, n in SETORES], "rncs": rncs, "etapas": etapas}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
