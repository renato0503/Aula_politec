"""Gera os dados fictícios da Custódia Definitiva (Sprint 0), com semente fixa.

30 vestígios em 5 categorias, 5 contêineres e 12 meses de histórico. Traz de
propósito as três situações de exceção do MVP: um contêiner cheio, um material
sem endereço por pendência documental e uma categoria que só cabe em contêiner
refrigerado.

Uso: python "Apps/custodia-definitiva/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)

CATEGORIAS = [
    ("entorpecentes", "Entorpecentes e contraprovas", "ambiente seco, longe de umidade", "lacre e identificação"),
    ("armas-brancas", "Armas brancas", "ambiente seco", "integridade do fio e do cabo"),
    ("roupas", "Roupas e têxteis", "ambiente seco e ventilado", "proteção contra mofo"),
    ("eletronicos", "Eletrônicos e mídias", "ambiente seco, sem campo magnético", "proteção eletrostática"),
    ("biologicos", "Materiais biológicos", "refrigeração entre 2 e 8 graus", "controle de temperatura"),
]
CONTEINERES = [
    ("C-01", "entorpecentes", 200, "ambiente seco", "Sala de custódia, prateleira A"),
    ("C-02", "armas-brancas", 80, "ambiente seco", "Sala de custódia, armário B"),
    ("C-03", "roupas", 60, "ambiente seco e ventilado", "Sala de custódia, prateleira C"),
    ("C-04", "eletronicos", 40, "ambiente seco", "Sala de custódia, armário D"),
    ("C-05", "biologicos", 50, "refrigerado de 2 a 8 graus", "Contêiner refrigerado, doca 5"),
]


def main():
    base = dt.date(2025, 11, 3)
    categorias = [{"id_categoria": i, "nome": n, "tipo_conservacao": t, "restricao": r} for i, n, t, r in CATEGORIAS]
    conteineres = [{"id_conteiner": i, "categoria_permitida": c, "capacidade": cap, "tipo_conservacao": t, "localizacao_fisica": loc, "status": "ativo"}
                   for i, c, cap, t, loc in CONTEINERES]
    ocupado = {c[0]: 0 for c in CONTEINERES}
    vestigios = []
    for n in range(30):
        cat = CATEGORIAS[n % 5][0]
        cont = next(c for c in CONTEINERES if c[1] == cat)
        volume = random.randint(2, 5)
        data = base + dt.timedelta(days=n * 11)
        status = "pendencia" if n == 7 else "armazenado"
        if status == "pendencia":
            vestigios.append({"id_vestigio": f"V-{n + 1:04d}", "protocolo": f"PROC-2026-{n + 1:03d}", "lacre": f"LC-{2026}{n + 1:04d}",
                              "categoria_id": cat, "volume_ocupado": volume, "data_entrada": data.isoformat(), "status": status,
                              "descricao": "Material separado para conferência documental; sem endereço até a regularização.", "conteiner_id": None, "posicao": None})
            continue
        ocupado[cont[0]] += volume
        vestigios.append({"id_vestigio": f"V-{n + 1:04d}", "protocolo": f"PROC-2026-{n + 1:03d}", "lacre": f"LC-{2026}{n + 1:04d}",
                          "categoria_id": cat, "volume_ocupado": volume, "data_entrada": data.isoformat(), "status": status,
                          "descricao": f"{volume} alíquotas/unidades de {dict((c[0], c[1]) for c in CATEGORIAS)[cat].lower()}.",
                          "conteiner_id": cont[0], "posicao": f"P{ocupado[cont[0]]:03d}"})
    # exceção 1: contêiner de eletrônicos cheio
    alvo = next(v for v in vestigios if v["categoria_id"] == "eletronicos" and v["status"] == "armazenado")
    while ocupado["C-04"] < 40:
        falta = 40 - ocupado["C-04"]
        alvo["volume_ocupado"] += falta
        ocupado["C-04"] += falta
    historico = []
    oc = sum(v["volume_ocupado"] for v in vestigios if v["conteiner_id"])
    for m in range(12):
        mes = (dt.date(2025, 11, 1) + dt.timedelta(days=31 * m)).replace(day=1)
        entradas = 260 + (m * 7) % 90
        saidas = 180 + (m * 11) % 70
        oc = max(0, oc + entradas - saidas)
        historico.append({"id_periodo": mes.strftime("%Y-%m"), "mes": mes.isoformat(), "entradas": entradas, "saidas": saidas, "ocupacao_final": oc})
    seed = {"categorias": categorias, "conteineres": conteineres, "vestigios": vestigios,
            "movimentacoes": [{"id_movimentacao": f"M-{v['id_vestigio']}", "vestigio_id": v["id_vestigio"], "tipo": "entrada",
                               "data_hora": v["data_entrada"] + "T09:00:00", "responsavel": "custodia", "origem": "recebimento",
                               "destino": f"{v['conteiner_id']} · {v['posicao']}" if v["conteiner_id"] else "sem endereço"} for v in vestigios],
            "historico_mensal": historico}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()}, "ocupado", ocupado)


if __name__ == "__main__":
    main()
