"""Gera os 12 corpos fictícios da TCIN (Sprint 0), com semente fixa.

Cobre as cinco situações, os quatro marcos, lacres e um caso sem identificação.

Uso: python "Apps/trilha-custodia-necropsia/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)

MARCOS = ["Saída da base", "Chegada ao local", "Saída do local", "Retorno ao IML"]
SITUACOES = ["em custódia", "em custódia", "aguardando identificação", "não identificado", "não reclamado",
             "em custódia", "liberado", "em custódia", "aguardando identificação", "não reclamado", "liberado", "em custódia"]
NOMES = ["Maria Fictícia Souza", "", "João Fictício Lima", "", "", "Ana Fictícia Alves", "Carlos Fictício Rocha",
         "Beatriz Fictícia Dias", "", "", "Paulo Fictício Matos", "Rita Fictícia Prado"]
ORIGENS = ["Delegacia de Polícia de Cuiabá", "Delegacia de Várzea Grande", "Delegacia de Rondonópolis", "CIOP"]
NATUREZAS = ["local de crime", "morte natural", "acidente de trânsito", "morte a esclarecer"]


def main():
    base = dt.date(2026, 10, 18)
    corpos, marcos, lacres, log = [], [], [], []
    for n in range(12):
        data = base + dt.timedelta(days=n)
        cid = f"C-{n + 1:04d}"
        situacao = SITUACOES[n]
        nome = NOMES[n]
        desconhecido = not nome
        identificado = bool(nome) and situacao != "aguardando identificação"
        entrega = {"responsavel": "Servidor Fictício", "documento": f"AUTO-{n + 1:03d}", "data": (data + dt.timedelta(days=2)).isoformat() + "T15:00:00"} if situacao == "liberado" else None
        corpos.append({"id_corpo": cid, "protocolo": f"NEC-2026-{n + 1:03d}", "origem": ORIGENS[n % len(ORIGENS)],
                       "natureza": NATUREZAS[n % len(NATUREZAS)], "municipio": ["Cuiabá", "Várzea Grande", "Rondonópolis"][n % 3],
                       "local": f"Endereço fictício {n + 1}", "nome": nome, "documento": f"DOC-{n + 1:03d}" if nome else "",
                       "desconhecido": desconhecido, "identificado": identificado, "sexo": ["Feminino", "Masculino"][n % 2],
                       "idade": 20 + n * 3, "tecnico": f"Técnico Fictício {chr(65 + n % 4)}", "situacao": situacao,
                       "criado_em": data.isoformat() + "T08:00:00", "entrega": entrega})
        # marcos: os dois primeiros para todos; os quatro para quem já voltou ao IML
        qtd = 4 if situacao in ("em custódia", "liberado") else 2 if situacao == "aguardando identificação" else 3
        for k in range(qtd):
            marcos.append({"id_marco": f"{cid}-M{k + 1}", "corpo_id": cid, "tipo": MARCOS[k],
                           "data_hora": (data.isoformat() + f"T{8 + k * 2:02d}:00:00"), "perfil": "tecnico", "observacao": ""})
        # lacres: dois em metade dos casos
        if n % 2 == 0:
            for k in range(2):
                lacres.append({"id_lacre": f"{cid}-L{k + 1}", "corpo_id": cid, "codigo": f"LC-{n + 1:03d}{k + 1}",
                               "destino": ["Laboratório de DNA", "Toxicologia"][k], "data_hora": data.isoformat() + "T12:00:00", "perfil": "tecnico"})
        log.append({"id": f"L-{cid}", "corpo_id": cid, "acao": "corpo registrado", "perfil": "operador", "data_hora": data.isoformat() + "T08:00:00"})
        if situacao == "liberado":
            log.append({"id": f"L-{cid}-lib", "corpo_id": cid, "acao": "situação: liberado", "perfil": "plantonista", "data_hora": entrega["data"]})
    seed = {"corpos": corpos, "marcos": marcos, "lacres": lacres, "log": log}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
