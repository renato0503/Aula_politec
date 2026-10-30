"""Gera os 15 contratos fictícios da Renovação de Contratos (Sprint 0), com semente fixa.

Cobre as seis faixas do semáforo (R3), contratos fora da contagem e dois com
termo aditivo já publicado. CNPJs são sintéticos, com dígitos verificadores
válidos.

Uso: python "Apps/renovacao-contratos-horus/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)

FORNECEDORES = ["Papelaria Central Ltda", "Tecnologia Mato Grosso S.A.", "Transportes Cerrado Ltda", "Laboratório Vida Diagnósticos",
                "Segurança Norte Serviços", "Limpeza Cuiabá Ltda", "Locadora Pantanal Veículos", "Comercial Araguaia Eireli",
                "Sistemas Integrados MT", "Manutenção Predial Centro-Oeste", "Gráfica Rondon", "Energia Solar Sinop",
                "Refrigeração Tropical", "Editora Verde Amazônia", "Rede Fibras MT"]
OBJETOS = ["Fornecimento de material de expediente", "Locação de equipamentos de informática", "Serviço de transporte de vestígios",
           "Insumos para exames laboratoriais", "Vigilância patrimonial", "Serviço de limpeza e conservação",
           "Locação de veículos", "Gêneros alimentícios", "Suporte e manutenção de sistemas", "Manutenção predial",
           "Serviços gráficos", "Instalação de painéis solares", "Manutenção de câmaras frias", "Assinatura de periódicos",
           "Link de internet dedicado"]
DIAS = [210, 135, 110, 95, 80, 70, 55, 45, 35, 20, 5, -12, -45, 400, 62]
STATUS = ["Vigente"] * 13 + ["Encerrado", "Vigente"]


def cnpj(n):
    base = [int(x) for x in f"{n:08d}0001"]
    def dv(nums):
        pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2][-len(nums):]
        s = sum(a * b for a, b in zip(nums, pesos))
        r = s % 11
        return 0 if r < 2 else 11 - r
    d1 = dv(base)
    d2 = dv(base + [d1])
    return "".join(map(str, base + [d1, d2]))


def menos_meses(data, meses):
    d = data.replace(day=1)
    ano, mes = d.year, d.month - meses
    while mes <= 0:
        mes += 12
        ano -= 1
    return data.replace(year=ano, month=mes)


def main():
    hoje = dt.date(2026, 10, 29)
    contratos, aditivos, auditoria = [], [], []
    for n, dias in enumerate(DIAS):
        fim = hoje + dt.timedelta(days=dias)
        inicio = menos_meses(fim, 12)
        cid = f"CT-{n + 1:03d}"
        c = {"id_contrato": cid, "numero": f"{n + 1:03d}/2025", "fornecedor": FORNECEDORES[n], "cnpj": cnpj(n + 1),
             "valor_c": (60000 + n * 18500) * 100 + 37, "data_inicio": inicio.isoformat(), "vigencia_meses": 12, "data_fim": fim.isoformat(),
             "objeto": OBJETOS[n], "permite_prorrogacao": n != 4, "alerta_dias": 90, "status": STATUS[n],
             "criado_em": inicio.isoformat() + "T09:00:00"}
        contratos.append(c)
        auditoria.append({"id_evento": f"A-{n + 1}-0", "contrato_id": cid, "acao": "contrato cadastrado", "detalhe": f"{c['numero']} · término {c['data_fim']}",
                          "perfil": "admin", "data_hora": inicio.isoformat() + "T09:00:00"})
        if n in (2, 7):
            aditivos.append({"id_aditivo": f"AD-{n + 1}", "contrato_id": cid, "numero_aditivo": "1º TA", "data_assinatura": (fim - dt.timedelta(days=120)).isoformat(),
                             "nova_vigencia": (fim + dt.timedelta(days=365)).isoformat(), "fundamento": "Lei nº 14.133/2021, art. 107",
                             "status": "Publicado", "criado_em": (fim - dt.timedelta(days=120)).isoformat() + "T10:00:00"})
    seed = {"contratos": contratos, "aditivos": aditivos, "auditoria": auditoria}
    # Sprint 3: itens de instrução já marcados (o resto fica para o gestor marcar)
    ITENS = ["solicitacao", "justificativa", "regularidade", "trabalhista", "parecer", "minuta", "publicacao"]
    instrucao = []
    for n in (0, 1, 2):
        cid = f"CT-{n + 1:03d}"
        for k, item in enumerate(ITENS[:4 + n]):   # contratos diferentes com quantidades diferentes de itens
            instrucao.append({"id_item": f"I-{cid}-{item}", "contrato_id": cid, "item": item, "ordem": ITENS.index(item),
                              "feito": True, "data_hora": contratos[n]["criado_em"], "responsavel": "admin"})
    seed["instrucao"] = instrucao
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()}, cnpj(1))


if __name__ == "__main__":
    main()
