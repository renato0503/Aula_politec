"""Cenário de uso do Mapa de Distribuição: importar a planilha, salvar e percorrer as 8 etapas.

A versão atual (planilha única) não tem mais os cenários dos Sprints 1 a 7; eles
ficaram em legado/testes/. Este cenário usa a tela como uma pessoa usaria.
Uso: python testes/cenarios.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from testar import EXEMPLO, testar  # noqa: E402

if __name__ == "__main__":
    falhas = testar(EXEMPLO)
    for x in falhas:
        print("FALHA", x)
    print(f"mapa-distribuicao-credor: {'1/1' if not falhas else '0/1'} cenário (importar, salvar e abrir as 8 etapas)")
    sys.exit(1 if falhas else 0)
