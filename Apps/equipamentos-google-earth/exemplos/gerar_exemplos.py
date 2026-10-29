"""Gera a base de MT e o seed fictício do Mapa de Equipamentos (Sprint 0).

Entrada (baixada do IBGE para uma pasta de trabalho, fora do repositório):
  malha.json        api/v3/malhas/estados/51?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=municipio
  municipios.json   api/v1/localidades/estados/51/municipios

Saídas:
  ../dados-base/mt-municipios.json   [{c: código IBGE, n: nome, lat, lon, p: [[lon, lat], ...]}]
                                     polígono simplificado (Douglas-Peucker, 0,01 grau) e 3 casas decimais;
                                     lat/lon = centroide do polígono (não é a sede do município)
  ../dados-base/mt-municipios.csv    código; nome; latitude; longitude
  seed.json                          3 diretorias, 12 unidades, 150 equipamentos, 20 contratos,
                                     200 manutenções, 40 paradas e os parâmetros de custo (fictícios)

Semente fixa = 20261029.
Uso: python "Apps/equipamentos-google-earth/exemplos/gerar_exemplos.py" <pasta com malha.json e municipios.json>
"""
import datetime as dt
import json
import pathlib
import random
import sys
import uuid

AQUI = pathlib.Path(__file__).resolve().parent
BASE = AQUI.parent / "dados-base"
random.seed(20261029)
U = lambda: str(uuid.UUID(int=random.getrandbits(128), version=4))


def rdp(pts, tol):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    norma = (dx * dx + dy * dy) ** 0.5 or 1e-12
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / norma
        if d > dmax:
            dmax, idx = d, i
    if dmax > tol:
        return rdp(pts[:idx + 1], tol)[:-1] + rdp(pts[idx:], tol)
    return [pts[0], pts[-1]]


def centroide(anel):
    a = cx = cy = 0
    for (x0, y0), (x1, y1) in zip(anel, anel[1:] + anel[:1]):
        f = x0 * y1 - x1 * y0
        a += f; cx += (x0 + x1) * f; cy += (y0 + y1) * f
    a *= 0.5
    return (cx / (6 * a), cy / (6 * a)) if a else anel[0]


def base_mt(pasta):
    malha = json.loads((pasta / "malha.json").read_text(encoding="utf-8"))
    nomes = {str(m["id"]): m["nome"] for m in json.loads((pasta / "municipios.json").read_text(encoding="utf-8"))}
    saida = []
    for f in malha["features"]:
        cod = f["properties"]["codarea"]
        geo = f["geometry"]
        anel = geo["coordinates"][0] if geo["type"] == "Polygon" else max((p[0] for p in geo["coordinates"]), key=len)
        simpl = rdp(anel[:-1] if anel[0] == anel[-1] else anel, 0.01)
        lon, lat = centroide(anel)
        saida.append({"c": cod, "n": nomes.get(cod, cod), "lat": round(lat, 4), "lon": round(lon, 4),
                      "p": [[round(x, 3), round(y, 3)] for x, y in simpl]})
    sem_malha = sorted(set(nomes) - {s["c"] for s in saida})
    for cod in sem_malha:  # município criado depois da malha publicada
        saida.append({"c": cod, "n": nomes[cod], "lat": None, "lon": None, "p": [], "obs": "sem polígono na malha do IBGE"})
    saida.sort(key=lambda s: s["n"])
    BASE.mkdir(exist_ok=True)
    (BASE / "mt-municipios.json").write_text(json.dumps(saida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (BASE / "mt-municipios.csv").write_text("﻿codigo_ibge;nome;latitude;longitude\n" + "".join(
        f"{s['c']};{s['n']};{s['lat'] if s['lat'] is not None else ''};{s['lon'] if s['lon'] is not None else ''}\n" for s in saida), encoding="utf-8")
    return {s["n"]: s for s in saida}, sem_malha


DIRETORIAS = [("Diretoria Metropolitana (fictícia)", "DMET"), ("Diretoria do Interior Norte (fictícia)", "DINN"), ("Diretoria do Interior Sul (fictícia)", "DINS")]
UNIDADES = [("Sede Cuiabá", "Cuiabá", 0, "sede", 120), ("Posto Várzea Grande", "Várzea Grande", 0, "posto", 60),
            ("Regional Rondonópolis", "Rondonópolis", 2, "regional", 55), ("Regional Sinop", "Sinop", 1, "regional", 50),
            ("Regional Cáceres", "Cáceres", 2, "regional", 30), ("Regional Barra do Garças", "Barra do Garças", 2, "regional", 28),
            ("Núcleo Tangará da Serra", "Tangará da Serra", 1, "núcleo", 22), ("Núcleo Alta Floresta", "Alta Floresta", 1, "núcleo", 18),
            ("Núcleo Primavera do Leste", "Primavera do Leste", 2, "núcleo", 20), ("Núcleo Sorriso", "Sorriso", 1, "núcleo", 24),
            ("Núcleo Juína", "Juína", 1, "núcleo", 12), ("Núcleo Pontes e Lacerda", "Pontes e Lacerda", 2, "núcleo", 14)]
TIPOS = [("Cromatógrafo", 5, 380000), ("Microscópio comparador", 4, 220000), ("Câmara de cianoacrilato", 3, 45000),
         ("Scanner de impressões digitais", 4, 18000), ("Impressora de documentos de identidade", 5, 65000),
         ("Geladeira de necrotério", 5, 140000), ("Autoclave", 3, 38000), ("Computador de extração forense", 4, 52000),
         ("Câmera fotográfica forense", 2, 21000), ("Etilômetro", 3, 9000), ("Centrífuga", 2, 16000), ("Gerador de energia", 4, 70000)]
FORNECEDORES = ["Manutec Serviços Técnicos (fictícia)", "Labcare Assistência (fictícia)", "Clima Frio Refrigeração (fictícia)", "TecForense Suporte (fictícia)"]
HOJE = dt.date(2026, 10, 29)


def seed(municipios):
    diretorias = [{"id": U(), "nome": n, "sigla": s} for n, s in DIRETORIAS]
    unidades = []
    for nome, mun, d, tipo, atend in UNIDADES:
        m = municipios[mun]
        unidades.append({"id": U(), "nome": nome + " (fictícia)", "tipo": tipo, "diretoria_id": diretorias[d]["id"],
                         "municipio_ibge": m["c"], "municipio": mun, "latitude": m["lat"], "longitude": m["lon"],
                         "horas_uteis_dia": 8, "atendimentos_dia": atend})
    contratos = []
    for i in range(20):
        inicio = HOJE - dt.timedelta(days=random.randint(30, 700))
        fim = inicio + dt.timedelta(days=365 * random.choice([1, 2]))
        contratos.append({"id": U(), "numero": f"{i + 1:03d}/{inicio.year}", "fornecedor": random.choice(FORNECEDORES),
                          "objeto": "Manutenção preventiva e corretiva", "inicio": inicio.isoformat(), "fim": fim.isoformat(),
                          "valor_mensal": round(random.uniform(900, 9500), 2), "sla_horas": random.choice([24, 48, 72]), "equipamento_ids": []})
    equipamentos = []
    for i in range(150):
        u = unidades[min(int(random.expovariate(0.28)), 11)]
        nome, crit, valor = random.choice(TIPOS)
        aquis = HOJE - dt.timedelta(days=random.randint(200, 4000))
        eq = {"id": U(), "patrimonio": f"PAT-{100000 + i * 13}", "nome": nome, "tipo": nome, "fabricante": "Fabricante fictício",
              "modelo": f"M-{random.randint(100, 999)}", "numero_serie": f"SN{random.randint(10**7, 10**8 - 1)}", "unidade_id": u["id"],
              "setor": random.choice(["Laboratório", "Identificação", "Necropsia", "Local de crime", "Administrativo"]),
              "criticidade": max(1, min(5, crit + random.choice([-1, 0, 0, 1]))), "tem_redundancia": random.random() < 0.35,
              "data_aquisicao": aquis.isoformat(), "valor_aquisicao": round(valor * random.uniform(0.8, 1.2), 2),
              "status": "operando", "latitude": u["latitude"], "longitude": u["longitude"], "contrato_id": None, "foto_ids": []}
        if random.random() < 0.55:
            c = random.choice(contratos); eq["contrato_id"] = c["id"]; c["equipamento_ids"].append(eq["id"])
        equipamentos.append(eq)
    manutencoes = []
    for _ in range(200):
        eq = random.choice(equipamentos)
        ab = HOJE - dt.timedelta(days=random.randint(5, 700))
        manutencoes.append({"id": U(), "equipamento_id": eq["id"], "tipo": random.choice(["preventiva", "corretiva", "corretiva"]),
                            "abertura": ab.isoformat(), "conclusao": (ab + dt.timedelta(days=random.randint(1, 25))).isoformat(),
                            "custo_rs": round(random.uniform(250, 18000), 2), "fornecedor": random.choice(FORNECEDORES),
                            "descricao": "Serviço fictício", "comprovante_id": None})
    paradas = []
    for i in range(40):
        eq = random.choice(equipamentos)
        ini = dt.datetime(2026, 1, 1, 8) + dt.timedelta(days=random.randint(0, 295), hours=random.randint(0, 8))
        aberta = i < 4
        fim = None if aberta else ini + dt.timedelta(days=random.randint(1, 30))
        if aberta:
            eq["status"] = "parado"
        paradas.append({"id": U(), "equipamento_id": eq["id"], "inicio": ini.isoformat(), "fim": fim.isoformat() if fim else None,
                        "motivo": random.choice(["Falha elétrica", "Peça quebrada", "Falha de software", "Desgaste"]),
                        "atendimentos_perdidos_dia": None, "custo_alternativo_dia": round(random.choice([0, 0, 350, 800]), 2)})
    parametros = [{"chave": "valor_referencia_atendimento", "valor": 180.0, "obs": "Valor de teste. A coordenadoria define o valor real."},
                  {"chave": "custo_alternativo_padrao_dia", "valor": 0.0, "obs": "Terceirização ou deslocamento, por dia."},
                  {"chave": "alerta_contrato_dias", "valor": 60, "obs": "RN05"}]
    return {"diretorias": diretorias, "unidades": unidades, "equipamentos": equipamentos, "contratos": contratos,
            "manutencoes": manutencoes, "paradas": paradas, "parametros": parametros}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    municipios, sem_malha = base_mt(pathlib.Path(sys.argv[1]))
    s = seed(municipios)
    (AQUI / "seed.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    tam = (BASE / "mt-municipios.json").stat().st_size
    print(f"municípios {len(municipios)} (sem polígono: {sem_malha}) | base {tam / 1024:.0f} KB")
    print({k: len(v) for k, v in s.items()})


if __name__ == "__main__":
    main()
