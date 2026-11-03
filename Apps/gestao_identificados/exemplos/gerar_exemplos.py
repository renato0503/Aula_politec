"""Gera os 24 corpos fictícios do NIHDE, com semente fixa.

Cobre as seis situações, as quatro vias de identificação, família, sepultamento
pelo município e identificação depois do sepultamento.

Uso: python "Apps/gestao_identificados/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261103)

UNIDADES = ["IML Cuiabá", "IML Sinop", "IML Rondonópolis", "IML Cáceres", "IML Barra do Garças"]
VIAS = ["necropapiloscopia", "DNA", "odontologia", "antropologia"]
NOMES = ["Maria Fictícia Souza", "João Fictício Lima", "Ana Fictícia Alves", "Carlos Fictício Rocha",
         "Beatriz Fictícia Dias", "Paulo Fictício Matos", "Rita Fictícia Prado", "Sérgio Fictício Lima",
         "Helena Fictícia Alves", "Lucas Fictício Costa", "Fernanda Fictícia Melo", "Rafael Fictício Nunes"]
SITUACOES = (["não identificado"] * 8 + ["identificado"] * 6 + ["não reclamado"] * 4 +
             ["sepultado"] * 3 + ["identificado após sepultamento"] * 2 + ["entregue"])


def main():
    base = dt.date(2026, 8, 1)
    corpos, log = [], []
    for n, situacao in enumerate(SITUACOES):
        data = base + dt.timedelta(days=n * 3)
        sepultado = situacao in ("sepultado", "identificado após sepultamento")
        if sepultado:
            data = base - dt.timedelta(days=45 - n)
        identificado = situacao in ("identificado", "não reclamado", "identificado após sepultamento", "entregue")
        nome = NOMES[n % len(NOMES)] if identificado or situacao == "identificado após sepultamento" else ""
        via = VIAS[n % len(VIAS)] if identificado else ""
        exames = {v: {"status": "não solicitado", "protocolo": "", "data": ""} for v in VIAS}
        if identificado:
            exames[via] = {"status": "positivo", "protocolo": f"EX-{n + 1:03d}", "data": (data + dt.timedelta(days=8)).isoformat()}
        else:
            exames["necropapiloscopia"] = {"status": "negativo", "protocolo": f"EX-{n + 1:03d}", "data": (data + dt.timedelta(days=5)).isoformat()}
            exames["DNA"] = {"status": "em andamento" if n % 2 else "negativo", "protocolo": f"EX-{n + 1:03d}-D", "data": (data + dt.timedelta(days=6)).isoformat()}
        familia = {}
        entrega = None
        if situacao == "entregue":
            familia = {"nome": "Familiar Fictício", "parentesco": "irmão", "contato": "contato@exemplo.gov.br",
                       "busca_iniciada_em": (data + dt.timedelta(days=2)).isoformat(), "localizada": True,
                       "localizada_em": (data + dt.timedelta(days=4)).isoformat(), "entrega_em": (data + dt.timedelta(days=6)).isoformat()}
            entrega = (data + dt.timedelta(days=6)).isoformat()
        elif situacao == "identificado" and n % 2 == 0:
            familia = {"nome": "Familiar Fictício", "parentesco": "mãe", "busca_iniciada_em": (data + dt.timedelta(days=3)).isoformat(),
                       "localizada": True, "localizada_em": (data + dt.timedelta(days=5)).isoformat()}
        elif situacao == "não reclamado":
            familia = {"busca_iniciada_em": (data + dt.timedelta(days=3)).isoformat(), "busca_sem_sucesso": True,
                       "busca_encerrada_em": (data + dt.timedelta(days=20)).isoformat()}
        sep = None
        if sepultado:
            sep = {"data": (data + dt.timedelta(days=31)).isoformat(), "municipio": ["Cuiabá", "Sinop", "Rondonópolis"][n % 3],
                   "local": "Cemitério municipal fictício", "certidao": f"CO-NI-{n + 1:03d}"}
        data_ident = ""
        if identificado and situacao == "identificado após sepultamento":
            data_ident = (data + dt.timedelta(days=60)).isoformat()
        elif identificado:
            data_ident = (data + dt.timedelta(days=8)).isoformat()
        corpos.append({"id": f"C-{n + 1:04d}", "protocolo": f"2026.{n + 1:04d}", "unidade": UNIDADES[n % len(UNIDADES)],
                       "data_entrada": data.isoformat(), "municipio": ["Cuiabá", "Sinop", "Rondonópolis", "Cáceres", "Barra do Garças"][n % 5],
                       "local": f"Local fictício {n + 1}", "data_localizacao": data.isoformat(),
                       "sexo": ["Feminino", "Masculino"][n % 2], "idade": 20 + n * 3, "altura": f"1,{55 + n % 30}",
                       "peso": str(55 + n), "olhos": ["castanhos", "pretos", "azuis"][n % 3], "cabelo": ["preto", "castanho", "grisalho"][n % 3],
                       "pele": ["parda", "branca", "preta"][n % 3], "sinais": "" if n % 4 else "cicatriz no braço esquerdo",
                       "nome": nome, "documento": f"DOC-{n + 1:03d}" if identificado else "", "identificado": identificado,
                       "situacao": situacao, "via_identificacao": via, "data_identificacao": data_ident,
                       "exames": exames, "familia": familia, "sepultamento": sep, "entrega_em": entrega,
                       "observacoes": "Registro fictício para o protótipo.", "criado_em": data.isoformat() + "T08:00:00"})
        log.append({"id": f"L-{n + 1}-E", "corpo_id": f"C-{n + 1:04d}", "acao": "entrada registrada", "detalhe": f"2026.{n + 1:04d}",
                    "data_hora": data.isoformat() + "T08:00:00", "perfil": "iml"})
        if identificado:
            log.append({"id": f"L-{n + 1}-I", "corpo_id": f"C-{n + 1:04d}", "acao": "identificação registrada", "detalhe": via,
                        "data_hora": data_ident + "T10:00:00", "perfil": "nihde"})
        if sep:
            log.append({"id": f"L-{n + 1}-S", "corpo_id": f"C-{n + 1:04d}", "acao": "sepultamento registrado", "detalhe": sep["local"],
                        "data_hora": sep["data"] + "T11:00:00", "perfil": "nihde"})
    seed = {"corpos": corpos, "log": log}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
