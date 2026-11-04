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

# (situação, nome): a nome só existe em corpo identificado.
# "em custódia", "não reclamado" e "liberado" são corpos identificados (RN03 do Sprint 3);
# "aguardando identificação" e "não identificado" são corpos sem identificação, sem nome.
CASOS = [
    ("em custódia", "Maria Fictícia Souza"),
    ("em custódia", "João Fictício Lima"),
    ("aguardando identificação", ""),
    ("não identificado", ""),
    ("não reclamado", "Beatriz Fictícia Dias"),
    ("em custódia", "Ana Fictícia Alves"),
    ("liberado", "Carlos Fictício Rocha"),
    ("em custódia", "Paulo Fictício Matos"),
    ("aguardando identificação", ""),
    ("não reclamado", "Rita Fictícia Prado"),
    ("liberado", "Sérgio Fictício Lima"),
    ("em custódia", "Helena Fictícia Alves"),
]
ORIGENS = ["Delegacia de Polícia de Cuiabá", "Delegacia de Várzea Grande", "Delegacia de Rondonópolis", "CIOP"]
NATUREZAS = ["local de crime", "morte natural", "acidente de trânsito", "morte a esclarecer"]
AGENTES = ["Causa natural", "Acidente", "Homicídio", "Suicídio", "Indeterminada", "Óbito administrativo"]
ETAPA_DA_SITUACAO = {"em custódia": 6, "aguardando identificação": 5, "não identificado": 6,
                     "não reclamado": 6, "liberado": 7}


def main():
    base = dt.date(2026, 10, 18)
    corpos, marcos, lacres, log = [], [], [], []
    for n in range(len(CASOS)):
        data = base + dt.timedelta(days=n)
        cid = f"C-{n + 1:04d}"
        situacao, nome = CASOS[n]
        desconhecido = not nome
        identificado = bool(nome)
        entrega = {"responsavel": "Servidor Fictício", "documento": f"AUTO-{n + 1:03d}", "data": (data + dt.timedelta(days=2)).isoformat() + "T15:00:00"} if situacao == "liberado" else None
        familia = None
        laudo = None
        sepultamento = None
        destino = ""
        finalizada = False
        if situacao == "liberado":
            familia = {"encontrada": True, "nome": "Familiar Fictício", "parentesco": "irmão",
                       "documento": f"DOC-FAM-{n + 1:03d}", "busca_iniciada_em": data.isoformat() + "T10:00:00",
                       "busca_encerrada_em": data.isoformat() + "T11:00:00", "liberado_em": entrega["data"]}
            laudo = {"entregue_por": "Técnico Fictício A", "recebido_por": "Gestor ADM Fictício",
                     "entregue_em": entrega["data"], "recebido_em": entrega["data"]}
            destino, finalizada = "família", True
        elif situacao == "não reclamado":
            familia = {"encontrada": False, "busca_sem_sucesso": True, "busca_iniciada_em": data.isoformat() + "T09:00:00",
                       "busca_encerrada_em": (data + dt.timedelta(days=5)).isoformat() + "T09:00:00"}
        elif situacao == "não identificado":
            familia = {"encontrada": False, "busca_sem_sucesso": True, "busca_iniciada_em": data.isoformat() + "T09:00:00",
                       "busca_encerrada_em": (data + dt.timedelta(days=5)).isoformat() + "T09:00:00"}
            sepultamento = {"justificativa": "Busca de familiares encerrada sem êxito após o prazo legal.",
                            "autorizado_em": (data + dt.timedelta(days=6)).isoformat() + "T09:00:00", "perfil": "gestor"}
            destino = "sepultamento"
        corpos.append({"id_corpo": cid, "protocolo": f"NEC-2026-{n + 1:03d}", "origem": ORIGENS[n % len(ORIGENS)],
                       "natureza": NATUREZAS[n % len(NATUREZAS)], "municipio": ["Cuiabá", "Várzea Grande", "Rondonópolis"][n % 3],
                       "local": f"Endereço fictício {n + 1}", "nome": nome, "documento": f"DOC-{n + 1:03d}" if nome else "",
                       "desconhecido": desconhecido, "identificado": identificado, "sexo": ["Feminino", "Masculino"][n % 2],
                       "idade": 20 + n * 3, "tecnico": f"Técnico Fictício {chr(65 + n % 4)}", "situacao": situacao,
                       "criado_em": data.isoformat() + "T08:00:00", "entrega": entrega,
                       "etapa": ETAPA_DA_SITUACAO[situacao], "etapa_em": data.isoformat() + "T08:00:00",
                       "agente_causal": AGENTES[n % len(AGENTES)],
                       "ocorrencia": "Acionamento fictício registrado para o exemplo.",
                       "identificacao": ({"resultado": "nao_identificado", "em": data.isoformat() + "T12:00:00"} if desconhecido and situacao in ("não identificado",) else None),
                       "familia": familia, "laudo": laudo, "sepultamento": sepultamento,
                       "destino_final": destino, "custodia_finalizada": finalizada})
        # marcos: os dois primeiros para todos; os quatro para quem já voltou ao IML
        qtd = 4 if situacao in ("em custódia", "liberado") else 2 if situacao == "aguardando identificação" else 3
        for k in range(qtd):
            marcos.append({"id_marco": f"{cid}-M{k + 1}", "corpo_id": cid, "tipo": MARCOS[k],
                           "data_hora": (data.isoformat() + f"T{8 + k * 2:02d}:00:00"), "perfil": "tecnico", "observacao": ""})
        # lacres: dois em metade dos casos
        if n % 2 == 0:
            for k in range(2):
                recebido = (n % 4 == 0)
                lacres.append({"id_lacre": f"{cid}-L{k + 1}", "corpo_id": cid, "codigo": f"LC-{n + 1:03d}{k + 1}",
                               "destino": ["Laboratório de DNA", "Toxicologia"][k], "data_hora": data.isoformat() + "T12:00:00", "perfil": "tecnico",
                               **({"recebido_em": data.isoformat() + "T14:00:00", "recebido_por": "gestor", "recebido_perfil": "gestor"} if recebido else {})})
        log.append({"id": f"L-{cid}", "corpo_id": cid, "acao": "corpo registrado", "perfil": "operador", "data_hora": data.isoformat() + "T08:00:00"})
        if situacao == "liberado":
            log.append({"id": f"L-{cid}-lib", "corpo_id": cid, "acao": "situação: liberado", "perfil": "plantonista", "data_hora": entrega["data"]})
    seed = {"corpos": corpos, "marcos": marcos, "lacres": lacres, "log": log}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
