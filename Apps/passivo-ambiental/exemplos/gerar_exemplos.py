"""Gera as 12 requisições fictícias do Passivo Ambiental (Sprint 0), com semente fixa.

Inclui o passivo antigo (requisições desde 2020), laudos em elaboração e dois
laudos concluídos com mapa, para o teste da RN03.

Uso: python "Apps/passivo-ambiental/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)

ORGAOS = ["Delegacia de Polícia de Cuiabá", "Delegacia de Polícia de Sinop", "Delegacia de Polícia de Rondonópolis",
          "Delegacia Especializada do Meio Ambiente", "Ministério Público Estadual", "Delegacia de Polícia de Cáceres"]
TIPOS = ["desmatamento", "queimada", "extração irregular de madeira", "ocupação irregular de área de preservação",
         "poluição de curso d'água", "mineração irregular"]
LOCAIS = ["Fazenda Santa Rita, município de Sinop", "Área de preservação do Rio Cuiabá", "Assentamento Nova Esperança",
          "Reserva legal da Fazenda Boa Vista", "Margem do Rio Araguaia", "Área rural de Cáceres"]


def main():
    hoje = dt.date(2026, 10, 29)
    requisicoes, laudos, mapas = [], [], []
    for n in range(12):
        if n < 7:
            data = hoje - dt.timedelta(days=400 + n * 120)   # passivo antigo
            status = "laudo"
        elif n < 10:
            data = hoje - dt.timedelta(days=20 + n)
            status = "laudo"
        else:
            data = hoje - dt.timedelta(days=45 + n)
            status = "concluida"
        rid = f"REQ-{n + 1:04d}"
        requisicoes.append({"id_requisicao": rid, "numero_processo": f"2026.000{n + 1:03d}-{n % 9 + 1}", "orgao": ORGAOS[n % len(ORGAOS)],
                            "data_requisicao": data.isoformat(), "tipo_infracao": TIPOS[n % len(TIPOS)], "prazo_dias": 10,
                            "local": LOCAIS[n % len(LOCAIS)], "coordenadas": f"-12.{random.randint(1000, 9999)}, -55.{random.randint(1000, 9999)}",
                            "status": status, "criado_em": data.isoformat() + "T08:00:00"})
        lid = f"L-{rid}"
        concluido = status == "concluida"
        laudos.append({"id_laudo": lid, "requisicao_id": rid, "status": "concluido" if concluido else "rascunho",
                       "local": requisicoes[-1]["local"], "coordenadas": requisicoes[-1]["coordenadas"], "tipo_infracao": requisicoes[-1]["tipo_infracao"],
                       "horas_trabalhadas": 16 if concluido else random.choice([0, 4, 8]), "criado_em": data.isoformat() + "T09:00:00"})
        if concluido:
            for k in range(2):
                mapas.append({"id_mapa": f"{lid}-M{k + 1}", "laudo_id": lid, "modelo_id": "delimitacao",
                              "modelo": "Delimitação da área de dano",
                              "elementos": {"norte": "N", "escala": "1:25.000", "legenda": "azul = área danificada; verde = vegetação preservada",
                                            "data": data.isoformat(), "fonte": "Imagem de satélite (fictícia)"},
                              "valor_extra": f"{12 + k * 3},5", "criado_em": data.isoformat() + "T11:00:00"})
    seed = {"requisicoes": requisicoes, "laudos": laudos, "mapas": mapas}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
