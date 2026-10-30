"""Gera os 10 processos de aquisição fictícios (Sprint 0), com semente fixa.

Cobre as etapas do fluxo, processos atrasados, documentos faltantes e
pendências abertas.

Uso: python "Apps/controle-aquisicoes/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)

ETAPAS = ["DFD", "ETP", "Análise de riscos", "TR", "Pesquisa de preços", "SIGADOC e SIAG", "Análise técnica", "Análise jurídica", "Modalidade definida"]
DOCS = {"DFD": ["DFD"], "ETP": ["ETP"], "Análise de riscos": ["Análise de riscos"], "TR": ["TR"], "Pesquisa de preços": ["Pesquisa de preços"]}
OBJETOS = ["Aquisição de 40 notebooks", "Contratação de link de internet", "Compra de reagentes laboratoriais", "Locação de veículos",
           "Serviço de manutenção predial", "Aquisição de câmaras frias", "Contratação de serviço gráfico", "Compra de mobiliário",
           "Assinatura de software de gestão", "Aquisição de equipamentos de proteção"]
UNIDADES = ["Gabinete de Direção", "Laboratório Forense", "Identificação Civil", "Custódia Definitiva", "Aquisições e Contratos"]


def main():
    hoje = dt.date(2026, 10, 29)
    dias = [5, 18, 35, 40, 12, 25, 50, 8, 30, 22]
    processos, documentos, pendencias, log = [], [], [], []
    for n, dias_atras in enumerate(dias):
        etapa = ETAPAS[n % len(ETAPAS)]
        data = hoje - dt.timedelta(days=dias_atras)
        pid = f"AQ-{n + 1:04d}"
        processos.append({"id_processo": pid, "numero_sigadoc": f"2026.{1000 + n}-SD", "numero_siag": f"SIAG-2026-{n + 1:04d}",
                          "objeto": OBJETOS[n], "unidade": UNIDADES[n % len(UNIDADES)], "responsavel": f"Servidor Fictício {chr(65 + n)}",
                          "data_abertura": data.isoformat(), "prazo_dias": 30, "etapa": etapa, "status": "em andamento", "criado_em": data.isoformat() + "T09:00:00"})
        # documentos de todas as etapas anteriores e da atual (uma exceção fica sem o documento da etapa)
        ate = ETAPAS.index(etapa)
        for k in range(ate + 1):
            e = ETAPAS[k]
            if n == 3 and k == ate:
                continue
            for d in DOCS.get(e, []):
                documentos.append({"id_documento": f"{pid}-{d}", "processo_id": pid, "tipo_documento": d, "nome": f"{d}-{pid}.pdf",
                                   "data": (data + dt.timedelta(days=k + 1)).isoformat() + "T10:00:00"})
        if n in (2, 6):
            pendencias.append({"id_pendencia": f"{pid}-P1", "processo_id": pid, "motivo": random.choice(["Documento incompleto", "Pesquisa de preços insuficiente", "Aguardando assinatura"]),
                               "aberta_em": (data + dt.timedelta(days=5)).isoformat(), "resolvida_em": None})
        log.append({"id": f"L-{pid}", "processo_id": pid, "acao": "processo registrado", "perfil": "compras", "data_hora": data.isoformat() + "T09:00:00"})
    seed = {"processos": processos, "documentos": documentos, "pendencias": pendencias, "log": log}
    # Sprint 3: duas pesquisas de preços (uma com o cotado 40% acima do estimado, para o alerta)
    pesquisas = [
        {"id_pesquisa": "PE-AQ-0001-1", "processo_id": "AQ-0001", "objeto": OBJETOS[0], "valor_estimado_c": 4800000,
         "cotacoes": [{"fornecedor": "Fornecedor Fictício A", "valor_c": 4800000, "data": (data + dt.timedelta(days=6)).isoformat()},
                      {"fornecedor": "Fornecedor Fictício B", "valor_c": 4950000, "data": (data + dt.timedelta(days=7)).isoformat()},
                      {"fornecedor": "Fornecedor Fictício C", "valor_c": 5100000, "data": (data + dt.timedelta(days=8)).isoformat()}],
         "data_hora": (data + dt.timedelta(days=9)).isoformat() + "T11:00:00", "perfil": "compras"},
        {"id_pesquisa": "PE-AQ-0001-2", "processo_id": "AQ-0001", "objeto": OBJETOS[0], "valor_estimado_c": 4800000,
         "cotacoes": [{"fornecedor": "Fornecedor Fictício A", "valor_c": 6600000, "data": (data + dt.timedelta(days=20)).isoformat()},
                      {"fornecedor": "Fornecedor Fictício B", "valor_c": 6800000, "data": (data + dt.timedelta(days=21)).isoformat()},
                      {"fornecedor": "Fornecedor Fictício C", "valor_c": 6700000, "data": (data + dt.timedelta(days=22)).isoformat()}],
         "data_hora": (data + dt.timedelta(days=23)).isoformat() + "T11:00:00", "perfil": "compras"},
    ]
    seed["pesquisas"] = pesquisas
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
