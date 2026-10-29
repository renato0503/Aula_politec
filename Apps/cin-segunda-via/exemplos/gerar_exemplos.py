"""Gera 30 pedidos fictícios de segunda via da CIN (Sprint 0).

Casos: elegíveis, CIN vencida, mudança de dados, foto ilegível. Nomes inventados;
CPF de teste com dígito verificador válido, gerado a partir de 000.000.0xx (não
use estes números fora do teste). Sem fotos: o app gera as fotos de teste.

Semente fixa = 20261029.
Uso: python "Apps/cin-segunda-via/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)
NOMES = ["Alice Teste", "Bento Exemplo", "Cora Fictícia", "Dario Modelo", "Eva Amostra", "Fausto Simulado", "Gaia Protótipo", "Ivo Ensaio"]


def cpf_teste(n):
    base = [int(c) for c in f"{n:09d}"]
    for pesos in (range(10, 1, -1), range(11, 1, -1)):
        s = sum(d * p for d, p in zip(base, pesos)) % 11
        base.append(0 if s < 2 else 11 - s)
    return "".join(map(str, base))


def main():
    hoje = dt.date(2026, 10, 29)
    pedidos = []
    for n in range(30):
        caso = ["elegível"] * 18 + ["CIN vencida"] * 5 + ["mudança de dados"] * 4 + ["foto ilegível"] * 3
        tipo = caso[n]
        validade = hoje + dt.timedelta(days=random.randint(200, 3000)) if tipo != "CIN vencida" else hoje - dt.timedelta(days=random.randint(10, 400))
        criado = dt.datetime(2026, 10, 20, 8) + dt.timedelta(hours=n * 7)
        situacao = "recebido" if n % 4 else random.choice(["aceito", "recusado"])
        pedidos.append({"protocolo": f"2V-{criado:%Y%m%d}-{n + 1:03d}", "nome": random.choice(NOMES), "cpf": cpf_teste(10 + n),
                        "nascimento": f"{random.randint(1960, 2006)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                        "numero_cin": cpf_teste(10 + n), "validade_cin": validade.isoformat(), "mudou_dados": tipo == "mudança de dados",
                        "contato": f"teste{n + 1}@exemplo.com", "criado_em": criado.isoformat(), "situacao": situacao,
                        "motivo": "Foto ilegível" if (situacao == "recusado" or tipo == "foto ilegível") else "", "caso_teste": tipo})
    seed = {"pedidos": pedidos}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print("pedidos", len(pedidos), {t: sum(p["caso_teste"] == t for p in pedidos) for t in set(p["caso_teste"] for p in pedidos)})


if __name__ == "__main__":
    main()
