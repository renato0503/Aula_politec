"""Gera as categorias iniciais e 10 casos fictícios da Comissão de Ética (Sprint 0).

As categorias são uma PROPOSTA para a Comissão conferir com o Código de Ética
(LC nº 112/2002): os artigos ficam "a conferir". Cada caso traz a categoria
esperada, usada no teste da classificação assistida (Sprint 3).

Semente fixa = 20261029.
Uso: python "Apps/comissao-etica-denuncias/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)

CATEGORIAS = [
    ("assedio_moral", "Assédio moral ou humilhação", ["humilh", "assédio", "assedio", "constrang", "grit", "xing", "ameaç", "perseguiç"]),
    ("desrespeito_publico", "Tratamento desrespeitoso ao público", ["cidadão", "atendimento", "grosseir", "mal atendid", "desrespeit", "público", "usuário"]),
    ("uso_cargo", "Uso do cargo em proveito próprio ou de terceiros", ["favor", "vantagem", "proveito", "parente", "fura fila", "furou a fila", "influência", "propina"]),
    ("sigilo", "Quebra de sigilo funcional", ["sigilo", "vazou", "vazamento", "divulgou", "compartilhou", "foto do laudo", "informação sigilosa"]),
    ("redes_sociais", "Conduta inadequada em redes sociais e aplicativos", ["whatsapp", "instagram", "rede social", "grupo", "postou", "publicação", "print"]),
    ("assiduidade", "Descumprimento de escala, plantão ou horário", ["plantão", "escala", "faltou", "atraso", "ausente", "abandon", "horário"]),
    ("conflito_interesses", "Conflito de interesses", ["empresa", "contrato", "fornecedor", "sócio", "interesse particular", "consultoria"]),
    ("uso_bens", "Uso indevido de bens e recursos públicos", ["viatura", "combustível", "equipamento", "material", "uso particular", "computador"]),
]
ROTEIRO_BASE = ["Descreva, com suas palavras, o que aconteceu.", "Quando e onde o fato ocorreu?", "Quem estava presente?",
                "Existe registro (mensagem, documento, escala) do fato?", "O fato já tinha acontecido antes?"]
CASOS = [
    ("assedio_moral", "O chefe do setor gritou com a servidora na frente da equipe e a humilhou repetidas vezes, com ameaças de remoção."),
    ("desrespeito_publico", "O cidadão relata que foi mal atendido no balcão, tratado de forma grosseira e sem resposta sobre o laudo."),
    ("uso_cargo", "Servidor teria furado a fila de exames para atender um parente, usando a influência do cargo."),
    ("sigilo", "Foto do laudo de um caso em andamento foi compartilhada fora da instituição; suspeita de vazamento de informação sigilosa."),
    ("redes_sociais", "Servidor postou no grupo de WhatsApp da unidade print de conversa com comentários ofensivos sobre colegas."),
    ("assiduidade", "Plantonista faltou ao plantão sem aviso e a escala ficou descoberta por seis horas."),
    ("conflito_interesses", "Servidor indicou empresa da qual seria sócio para o contrato de manutenção do laboratório."),
    ("uso_bens", "Viatura da unidade foi usada para uso particular no fim de semana, com gasto de combustível."),
    ("assedio_moral", "Colega relata perseguição constante e constrangimento em reuniões, com xingamentos."),
    ("assiduidade", "Atrasos repetidos no horário de entrada e abandono do posto antes do fim da escala."),
]


def main():
    base = dt.date(2026, 9, 1)
    categorias = [{"id": i, "nome": n, "artigos": "a conferir no Código de Ética (LC nº 112/2002)", "palavras": p, "roteiro_base": ROTEIRO_BASE} for i, n, p in CATEGORIAS]
    denuncias = []
    for n, (cat, relato) in enumerate(CASOS):
        rec = base + dt.timedelta(days=n * 5)
        denuncias.append({"id": f"CE-2026-{n + 1:03d}", "protocolo": f"CE-2026-{n + 1:03d}", "data_recebimento": rec.isoformat(), "canal": "e-mail",
                          "relato": relato, "denunciante": f"Denunciante Fictício {n + 1}", "denunciado": f"Servidor Fictício {chr(65 + n)}",
                          "etapa": "registro", "situacao": "aberto", "categoria_esperada": cat, "sigilo": True})
    seed = {"categorias": categorias, "denuncias": denuncias}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
