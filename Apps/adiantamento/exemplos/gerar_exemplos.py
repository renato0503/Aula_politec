"""Gera 10 adiantamentos fictícios e os feriados nacionais (Sprint 0).

Casos: completos, sem orçamento, com devolução da contabilidade, com prazo vencido,
em cada etapa do fluxo. Feriados: só os nacionais de 2026 e 2027; os de MT e do
município entram pela tela de configuração.

Semente fixa = 20261029.
Uso: python "Apps/adiantamento/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)

ETAPAS = ["Levantar orçamentos", "Análise da DAS", "Cadastro no SICAD", "Aprovação da chefia", "Conferência SESP",
          "Dotação (NGER)", "Autorização do ordenador", "Pagamento", "Aplicação do recurso", "Prestação de contas",
          "Análise da contabilidade", "Encerrado"]
FERIADOS = [("2026-01-01", "Confraternização Universal"), ("2026-04-03", "Sexta-feira Santa"), ("2026-04-21", "Tiradentes"),
            ("2026-05-01", "Dia do Trabalho"), ("2026-09-07", "Independência"), ("2026-10-12", "Nossa Senhora Aparecida"),
            ("2026-11-02", "Finados"), ("2026-11-15", "Proclamação da República"), ("2026-11-20", "Consciência Negra"),
            ("2026-12-25", "Natal"), ("2027-01-01", "Confraternização Universal"), ("2027-03-26", "Sexta-feira Santa"),
            ("2027-04-21", "Tiradentes"), ("2027-05-01", "Dia do Trabalho"), ("2027-09-07", "Independência"),
            ("2027-10-12", "Nossa Senhora Aparecida"), ("2027-11-02", "Finados"), ("2027-11-15", "Proclamação da República"),
            ("2027-11-20", "Consciência Negra"), ("2027-12-25", "Natal")]
UNIDADES = ["IML Cuiabá", "Laboratório Forense", "Identificação Civil", "Regional Rondonópolis", "Regional Sinop"]
FINALIDADES = [("compra", "Material de limpeza emergencial"), ("serviço", "Conserto de ar-condicionado da sala de necropsia"),
               ("compra", "Reagentes para exame urgente"), ("predial", "Reparo do telhado do almoxarifado"),
               ("serviço", "Manutenção do gerador"), ("compra", "Peças para a impressora de documentos")]


def main():
    hoje = dt.date(2026, 10, 29)
    processos, orcamentos, etapas, pendencias, notas = [], [], [], [], []
    for n in range(10):
        tipo, fin = FINALIDADES[n % len(FINALIDADES)]
        valor = round(random.uniform(800, 7900), 2)
        criado = hoje - dt.timedelta(days=random.randint(10, 150))
        ate = [11, 5, 2, 7, 9, 10, 11, 1, 8, 6][n]  # etapa atual de cada caso
        pid = f"AD-2026-{n + 1:03d}"
        dia, pago = criado, None
        for i in range(ate + 1):
            fim = None if i == ate else dia + dt.timedelta(days=random.randint(1, 6) if i < 8 else random.randint(20, 60))
            etapas.append({"id": f"{pid}-E{i:02d}", "processo_id": pid, "etapa": ETAPAS[i], "entrada_em": dia.isoformat(),
                           "saida_em": fim.isoformat() if fim else None, "responsavel": ["Unidade", "DAS", "Servidor", "Chefia", "SESP Financeiro",
                           "NGER", "Ordenador", "SESP Financeiro", "Servidor", "Servidor", "SESP Contabilidade", "SESP Contabilidade"][i]})
            if i == 7 and fim:
                pago = fim
            if fim:
                dia = fim
        if n == 1:
            orcs = 2  # pedido sem o terceiro orçamento (RN01)
        else:
            orcs = 3
        for k in range(orcs):
            orcamentos.append({"id": f"{pid}-O{k + 1}", "processo_id": pid, "fornecedor": f"Fornecedor Fictício {chr(65 + k)} Ltda",
                               "cnpj": "", "valor": round(valor * random.uniform(1.0, 1.25), 2)})
        if n in (4, 6):
            aberta = hoje - dt.timedelta(days=12 if n == 4 else 3)
            pendencias.append({"id": f"{pid}-P1", "processo_id": pid, "motivo": "Nota fiscal sem identificação do órgão",
                               "aberta_em": aberta.isoformat(), "prazo": None, "resolvida_em": None})
        if ate >= 10:
            for k in range(random.randint(1, 3)):
                notas.append({"id": f"{pid}-N{k + 1}", "processo_id": pid, "numero": f"{random.randint(1000, 99999)}", "cnpj": "",
                              "valor": round(valor / 2, 2), "data": (pago or hoje).isoformat()})
        processos.append({"id": pid, "numero_sicad": f"SICAD-{2026}{n + 41:05d}" if ate >= 2 else "", "unidade": UNIDADES[n % 5],
                          "solicitante": f"Servidor Fictício {n + 1}", "matricula": str(300000 + n * 17), "finalidade": fin, "tipo": tipo,
                          "valor_solicitado": valor, "valor_concedido": valor if ate >= 7 else None, "situacao": "encerrado" if ate == 11 else "em andamento",
                          "etapa_atual": ETAPAS[ate], "pago_em": pago.isoformat() if pago else None, "criado_em": criado.isoformat()})
    seed = {"processos": processos, "orcamentos": orcamentos, "etapas": etapas, "pendencias": pendencias, "notas": notas,
            "feriados": [{"data": d, "nome": nome} for d, nome in FERIADOS]}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
