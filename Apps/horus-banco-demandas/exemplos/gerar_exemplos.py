"""Gera o seed fictício do Banco de Demandas (Sprint 0).

1 órgão, 1 diretoria, 4 unidades, unidades de medida, 1 ciclo ATIVO, 15 demandas
(reagentes, EPIs, equipamentos) e 3 manifestações de interesse. As colunas seguem
as tabelas do Hórus (banco_demandas, banco_demanda_manifestacoes,
banco_demanda_inclusoes). Valores em reais com 2 casas.

Semente fixa = 20261029.
Uso: python "Apps/horus-banco-demandas/exemplos/gerar_exemplos.py"
"""
import json
import pathlib
import random
import uuid

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)
U = lambda: str(uuid.UUID(int=random.getrandbits(128), version=4))

ORGAO = {"id": U(), "nome": "POLITEC/MT (fictício)"}
DIRETORIA = {"id": U(), "nome": "Diretoria Metropolitana de Criminalística (fictícia)", "sigla": "DMC"}
UNIDADES = [{"id": U(), "nome": n, "sigla": s, "diretoria_id": DIRETORIA["id"], "orgao_id": ORGAO["id"]} for n, s in [
    ("Laboratório de Química Forense", "LQF"), ("Laboratório de Genética Forense", "LGF"),
    ("Núcleo de Perícias em Local de Crime", "NPLC"), ("Núcleo de Informática Forense", "NIF")]]
MEDIDAS = [{"id": U(), "sigla": s, "nome": n} for s, n in [("UN", "unidade"), ("CX", "caixa"), ("FR", "frasco"), ("PCT", "pacote"), ("KIT", "kit")]]
CICLO = {"id": U(), "ano": 2027, "status": "ATIVO", "nome": "PCA 2027"}
USUARIOS = ["servidor.lqf", "servidor.lgf", "gerente.nplc", "servidor.nif", "diretor.dmc"]

DEMANDAS = [
    ("CUSTEIO", 0, "Reagente luminol para revelação de manchas de sangue latente, frasco de 500 mL, validade mínima de 12 meses na entrega", "FR", 285.40, 40),
    ("CUSTEIO", 0, "Kit de reagente de Kastle-Meyer para teste presuntivo de sangue, com fenolftaleína reduzida e peróxido", "KIT", 412.00, 25),
    ("CUSTEIO", 1, "Kit de extração de DNA de amostras biológicas, 50 reações, compatível com extrator automatizado", "KIT", 3980.00, 12),
    ("CUSTEIO", 1, "Ponteira com filtro de 1000 microlitros, estéril, livre de DNase e RNase, caixa com 96 unidades", "CX", 96.50, 120),
    ("CUSTEIO", 2, "Luva nitrílica sem pó, tamanho M, caixa com 100 unidades, para manuseio de vestígios em local de crime", "CX", 38.90, 300),
    ("CUSTEIO", 2, "Envelope de segurança para vestígios com lacre numerado e campo de cadeia de custódia, tamanho A4", "PCT", 189.00, 80),
    ("CUSTEIO", 2, "Swab estéril com haste de plástico e tubo protetor, embalado individualmente, pacote com 100", "PCT", 74.30, 150),
    ("CUSTEIO", 3, "Mídia de armazenamento SSD de 2 TB para cópia forense de dispositivos apreendidos", "UN", 899.00, 30),
    ("CUSTEIO", 3, "Cabo de dados USB-C para extração de celulares, com blindagem e 1 metro de comprimento", "UN", 59.90, 60),
    ("INVESTIMENTO", 0, "Cromatógrafo a gás acoplado a espectrômetro de massas para identificação de drogas de abuso", "UN", 685000.00, 1),
    ("INVESTIMENTO", 1, "Termociclador para PCR em tempo real com 96 poços e software de análise de genotipagem", "UN", 248000.00, 1),
    ("INVESTIMENTO", 2, "Fonte de luz forense multibanda com filtros de 365 a 640 nm para busca de vestígios", "UN", 78500.00, 2),
    ("INVESTIMENTO", 2, "Câmera fotográfica digital full frame com lente macro para documentação de local de crime", "UN", 21900.00, 3),
    ("INVESTIMENTO", 3, "Bloqueador de escrita forense para discos SATA, NVMe e USB, com certificação de integridade", "UN", 9800.00, 4),
    ("INVESTIMENTO", 3, "Estação de trabalho para extração e análise de dispositivos móveis com 128 GB de memória", "UN", 46500.00, 2),
]
JUST = ("A demanda atende à rotina do setor e foi dimensionada pela média de consumo dos dois últimos anos, "
        "considerando o volume de exames recebidos e a necessidade de manter estoque mínimo para três meses.")


def main():
    medida = {m["sigla"]: m["id"] for m in MEDIDAS}
    demandas = []
    for n, (grupo, u, espec, um, valor, qtd) in enumerate(DEMANDAS):
        criado = f"2026-10-{(n % 20) + 5:02d}T13:{n:02d}:00Z"
        demandas.append({
            "id": U(), "grupo": grupo, "unidade_id": UNIDADES[u]["id"], "especificacao_tecnica": espec,
            "valor_unitario": valor, "quantidade": qtd, "unidade_medida_id": medida[um],
            "valor_global": round(valor * qtd, 2),
            "links_referencia": [f"https://www.exemplo-fornecedor.com.br/produto/{1000 + n}"],
            "preview_title": "Página de referência do fornecedor (fictícia)",
            "justificativa": JUST, "arquivo_pdf": None, "criado_por": USUARIOS[u],
            "diretoria_id": DIRETORIA["id"], "orgao_id": ORGAO["id"], "created_at": criado, "updated_at": criado})
    manifestacoes = []
    for dem_idx, uni_idx, qtd in [(4, 0, 100), (4, 1, 80), (6, 1, 40)]:
        d = demandas[dem_idx]
        manifestacoes.append({
            "id": U(), "banco_demanda_id": d["id"], "unidade_id": UNIDADES[uni_idx]["id"], "quantidade": qtd,
            "justificativa": "A unidade usa o mesmo item na rotina e prefere aderir à especificação já cadastrada.",
            "criado_por": USUARIOS[uni_idx], "orgao_id": ORGAO["id"], "diretoria_id": DIRETORIA["id"],
            "created_at": "2026-10-27T15:00:00Z"})
    seed = {"orgaos": [ORGAO], "diretorias": [DIRETORIA], "unidades": UNIDADES, "unidades_medida": MEDIDAS,
            "ciclos": [CICLO], "banco_demandas": demandas, "banco_demanda_manifestacoes": manifestacoes,
            "banco_demanda_inclusoes": []}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    (AQUI / "unidades-medida.json").write_text(json.dumps(MEDIDAS, ensure_ascii=False, indent=1), encoding="utf-8")
    print("demandas", len(demandas), "| manifestações", len(manifestacoes),
          "| valor global R$", f"{sum(d['valor_global'] for d in demandas):,.2f}")


if __name__ == "__main__":
    main()
