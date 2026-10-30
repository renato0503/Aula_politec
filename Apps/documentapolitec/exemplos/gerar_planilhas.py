"""Gera os arquivos de exemplo do Sprint 3 do DOCUMENTAPOLITEC.

Dois arquivos de texto (CSV):
  relacao-prontuarios.csv  a planilha de 850 prontuários que o setor entrega, com algumas linhas repetidas e um número fora do formato
  indice-arquivo-digital.csv o índice dos prontuários localizados no PDF digitalizado, com um prontuário a mais

Uso: python "Apps/documentapolitec/exemplos/gerar_planilhas.py"
"""
import csv
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261030)

TOTAL = 850
PRIMEIRO = 2018000001   # 10 dígitos: AAAA.NNNNNN, igual ao formato do acervo


def main():
    numeros = [f"{PRIMEIRO + i:09d}" for i in range(TOTAL)]
    relacao, digital = [], []
    for k, num in enumerate(numeros):
        ano = num[:4]
        relacao.append({"Número do prontuário": f"{ano}.{num[4:]}", "Caixa": f"CX-{(k % 12) + 1:03d}", "Ano": ano})
        # o arquivo digital não tem 4 prontuários e tem um que não veio na planilha
        if k not in (17, 128, 401, 655):
            digital.append({"Número do prontuário": num})
    # duas linhas repetidas e um número fora do formato, para exercitar a recusa
    relacao.append(dict(relacao[3]))
    relacao.append(dict(relacao[500]))
    relacao.append({"Número do prontuário": "19.1", "Caixa": "CX-001", "Ano": "2019"})
    digital.append({"Número do prontuário": f"{PRIMEIRO + TOTAL:09d}"})

    with (AQUI / "relacao-prontuarios.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["Número do prontuário", "Caixa", "Ano"], delimiter=";")
        w.writeheader(); w.writerows(relacao)
    with (AQUI / "indice-arquivo-digital.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["Número do prontuário"], delimiter=";")
        w.writeheader(); w.writerows(digital)
    print(f"relacao-prontuarios.csv: {len(relacao)} linhas · indice-arquivo-digital.csv: {len(digital)} linhas")


if __name__ == "__main__":
    main()
