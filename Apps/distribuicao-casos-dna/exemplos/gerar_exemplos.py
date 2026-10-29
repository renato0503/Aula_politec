"""Gera as 6 rodadas e 48 casos fictícios de DNA (Sprint 0), com semente fixa.

Inclui duas rodadas já distribuídas (em rotação), uma com ordinário aguardando
processamento e cobranças pendentes, para exercitar RN01 a RN04.

Uso: python "Apps/distribuicao-casos-dna/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)

PERITOS = [("P1", "Perito Fictício A", "crime sexual"), ("P2", "Perito Fictício B", "identificação humana"),
           ("P3", "Perito Fictício C", "local de crime"), ("P4", "Perito Fictício D", "crime sexual")]


def main():
    hoje = dt.date(2026, 10, 29)
    peritos = [{"id_perito": i, "nome": n, "especialidade": e, "ativo": True} for i, n, e in PERITOS]
    rodadas, casos, log = [], [], []
    n = 0
    for k in range(6):
        data = hoje - dt.timedelta(days=(6 - k) * 7)
        rid = f"RD-{k + 1:03d}"
        distribuida = k < 2
        aguardando = k == 4
        perito = PERITOS[k % len(PERITOS)][0] if distribuida else None
        rodadas.append({"id_rodada": rid, "placa": f"PL-2026-{k + 11:02d}", "data": data.isoformat(), "perito_id": perito,
                        "status": "distribuida" if distribuida else "aberta", "criado_em": data.isoformat() + "T08:00:00"})
        for j in range(8):
            n += 1
            tipo = "ordinario" if j < 6 else "cobranca"
            if distribuida:
                status, distrib = "distribuido", (data + dt.timedelta(days=random.randint(1, 3))).isoformat() + "T10:00:00"
                perito_caso = perito
            elif aguardando and tipo == "ordinario":
                status, distrib, perito_caso = "aguardando", None, None
            else:
                status, distrib, perito_caso = "processado", None, None
            casos.append({"id_caso": f"{rid}-{j + 1:02d}", "rodada_id": rid, "protocolo": f"2026.{n:06d}",
                          "tipo": tipo, "status": status, "data_processamento": None if status == "aguardando" else (data + dt.timedelta(days=1)).isoformat(),
                          "perito_id": perito_caso, "distribuido_em": distrib})
        log.append({"id": f"L-{rid}", "rodada_id": rid, "acao": "rodada criada", "perfil": "coordenador", "data_hora": data.isoformat() + "T08:00:00"})
        if distribuida:
            log.append({"id": f"L-{rid}-d", "rodada_id": rid, "acao": "rodada distribuída (6 ordinários)", "perfil": "coordenador",
                        "data_hora": (data + dt.timedelta(days=1)).isoformat() + "T10:00:00"})
    seed = {"rodadas": rodadas, "casos": casos, "peritos": peritos, "log": log}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
