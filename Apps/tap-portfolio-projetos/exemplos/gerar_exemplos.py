"""Gera propostas fictícias e o checklist de documentos do TAP (Sprint 0).

8 propostas: completas, sem anexo obrigatório, com justificativa curta, devolvidas
e aprovadas no portfólio. O checklist é uma proposta até o modelo oficial chegar.

Semente fixa = 20261029.
Uso: python "Apps/tap-portfolio-projetos/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)

DOCUMENTOS = [("pesquisa_precos", "Pesquisa de preços (mínimo 3 orçamentos)", True), ("estudo_tecnico", "Estudo técnico preliminar", True),
              ("anuencia_chefia", "Anuência da chefia da unidade", True), ("cronograma", "Cronograma físico-financeiro", False),
              ("fotos", "Fotos ou evidências da necessidade", False)]
OBJETIVOS = ["Reduzir o tempo de emissão de laudos", "Modernizar a infraestrutura das unidades", "Ampliar a capacidade dos laboratórios",
             "Fortalecer a identificação civil", "Qualificar os servidores"]
PROPOSTAS = [("Ampliação do laboratório de DNA", "Laboratório de Genética Forense", 2400000), ("Digitalização do arquivo de identificação", "Identificação Civil", 380000),
             ("Reforma do IML de Sinop", "Regional Sinop", 1150000), ("Capacitação em perícia digital", "Informática Forense", 95000),
             ("Frota de viaturas para local de crime", "Criminalística", 1600000), ("Sistema de gestão de vestígios", "Central de Custódia", 520000),
             ("Energia solar nas regionais", "DAS", 870000), ("Câmara fria para o IML de Cuiabá", "IML Cuiabá", 310000)]
SITUACAO = ["aprovada", "aprovada", "devolvida", "em triagem", "em análise", "rascunho", "devolvida", "aprovada"]


def main():
    base = dt.date(2026, 8, 3)
    propostas, pendencias, decisoes, portfolio = [], [], [], []
    for n, ((titulo, unidade, valor), sit) in enumerate(zip(PROPOSTAS, SITUACAO)):
        pid = f"TAP-2026-{n + 1:03d}"
        env = base + dt.timedelta(days=n * 9)
        curta = sit == "rascunho"
        propostas.append({"id": pid, "titulo": titulo, "unidade": unidade, "responsavel": f"Responsável Fictício {n + 1}", "contato": f"responsavel{n + 1}@exemplo.gov.br",
                          "objetivo": f"{titulo} para atender à demanda crescente da unidade e reduzir o tempo de resposta à sociedade.",
                          "justificativa": "Justificativa curta." if curta else ("A unidade atende volume crescente de demandas com estrutura insuficiente. "
                                            "O projeto reduz filas, melhora a qualidade do serviço e está alinhado ao planejamento estratégico da SESP e da POLITEC para o período."),
                          "objetivo_estrategico": OBJETIVOS[n % len(OBJETIVOS)], "valor_estimado": valor, "prazo_meses": random.choice([6, 12, 18, 24]),
                          "status": sit, "enviado_em": None if sit == "rascunho" else env.isoformat(),
                          "documentos": {d: (sit != "devolvida" or d != "pesquisa_precos") for d, _, _ in DOCUMENTOS}})
        if sit == "devolvida":
            pendencias.append({"id": f"{pid}-P1", "proposta_id": pid, "motivo": "Pesquisa de preços ausente", "aberta_em": (env + dt.timedelta(days=2)).isoformat(), "resolvida_em": None})
        if sit == "aprovada":
            decisoes.append({"id": f"{pid}-D1", "proposta_id": pid, "tipo": "aprovação", "texto": "Aprovado pela instância competente (fictício).", "autor": "Autoridade fictícia",
                             "data": (env + dt.timedelta(days=20)).isoformat()})
            portfolio.append({"proposta_id": pid, "prioridade": len(portfolio) + 1, "justificativa_prioridade": "Critério fictício de impacto e urgência.",
                              "fonte_recurso": random.choice(["Tesouro estadual", "Emenda parlamentar", "Convênio federal"]), "situacao_captacao": "em prospecção"})
    seed = {"propostas": propostas, "pendencias": pendencias, "decisoes": decisoes, "portfolio": portfolio,
            "documentos": [{"tipo": t, "nome": n, "obrigatorio": o} for t, n, o in DOCUMENTOS]}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
