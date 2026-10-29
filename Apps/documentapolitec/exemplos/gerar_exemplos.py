"""Gera as 12 caixas fictícias do DOCUMENTAPOLITEC (Sprint 0), com semente fixa.

Cada caixa traz a relação de prontuários, uma já conferida e lacrada, uma com
divergência no arquivo digital e as demais pendentes.

Uso: python "Apps/documentapolitec/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)

SETORES = ["DMIT · Arquivo corrente", "DMIT · Sala cofre", "Instituto de Identificação", "Posto de Cuiabá",
           "Posto de Várzea Grande", "Posto de Rondonópolis", "Posto de Sinop", "Arquivo central"]


def main():
    base = dt.date(2026, 9, 1)
    caixas, prontuarios, log = [], [], []
    n = 0
    for k in range(12):
        cid = f"CX-{k + 1:03d}"
        qtd = random.randint(8, 14)
        conferida = k == 0
        divergente = k == 1
        caixas.append({"id_caixa": cid, "setor_origem": SETORES[k % len(SETORES)], "responsavel": "Papiloscopista Fictício",
                       "data": (base + dt.timedelta(days=k * 2)).isoformat(), "qtd": qtd,
                       "status": "conferida" if conferida else "divergencia" if divergente else "pendente",
                       "criado_em": (base + dt.timedelta(days=k * 2)).isoformat() + "T09:00:00",
                       "lacrada_por": "Papiloscopista Fictício" if conferida else None,
                       "lacrada_em": (base + dt.timedelta(days=k * 2)).isoformat() + "T16:00:00" if conferida else None})
        for i in range(qtd):
            n += 1
            numero = f"2019.{n:06d}"
            prontuarios.append({"numero": numero, "caixa_id": cid, "conferido": conferida or divergente,
                                "digital": not (divergente and i == qtd - 1)})
        log.append({"id": f"L-{k + 1}", "caixa_id": cid, "acao": "caixa cadastrada", "perfil": "papiloscopista",
                    "data_hora": (base + dt.timedelta(days=k * 2)).isoformat() + "T09:00:00", "detalhe": f"{qtd} prontuários"})
        if conferida or divergente:
            log.append({"id": f"L-{k + 1}-c", "caixa_id": cid, "acao": "caixa conferida e lacrada" if conferida else "conferência com divergência",
                        "perfil": "papiloscopista", "data_hora": (base + dt.timedelta(days=k * 2)).isoformat() + "T16:00:00",
                        "detalhe": "Papiloscopista Fictício" if conferida else "1 prontuário sem correspondência"})
    seed = {"caixas": caixas, "prontuarios": prontuarios, "log": log}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
