"""Coleta o painel publico de pessoas desaparecidas do CNPD/MJ.

Fonte: https://cnpd.mj.gov.br/painel-publico
Endpoint: POST /api/api/painel-publico/desaparecidos/filtrar?ordenacao=...&pagina=N

O resultado e gravado em dados/cnpd-snapshot.json. O painel (index.html) e
gerado a partir desse arquivo por gerar_painel.py.

Uso:
    python coletar_dados.py
    python coletar_dados.py --saida dados/cnpd-snapshot.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib

from api_cnpd import CnpdClient

ORDENACAO = "MAIS_RECENTE"
PASTA = pathlib.Path(__file__).resolve().parent


def coletar(ordenacao: str = ORDENACAO) -> dict:
    cli = CnpdClient()
    pessoas = cli.todas({"nome": ""}, ordenacao=ordenacao, progresso=True)
    total_informado = cli.filtrar({"nome": ""}, ordenacao, 0).total_registros
    return {
        "fonte": "CNPD/MJ - Painel Publico de Pessoas Desaparecidas",
        "site": "https://cnpd.mj.gov.br/painel-publico",
        "endpoint": "https://cnpd.mj.gov.br/api/api/painel-publico/desaparecidos/filtrar",
        "ordenacao": ordenacao,
        "coletado_em": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "total_registros_informado": total_informado,
        "total_registros_coletado": len(pessoas),
        "registros": [
            {
                "id": p.id,
                "nome": p.nome,
                "idadeAtual": p.idade_atual,
                "idadeDesaparecimento": p.idade_desaparecimento,
                "sexo": p.sexo,
                "racaCor": p.raca_cor,
                "localRegistro": p.local_registro,
                "ufRegistro": p.uf_registro,
                "dataDesaparecimento": p.data_desaparecimento,
                "dataRegistroDesaparecimento": p.data_registro_desaparecimento,
                "flLocalizacaoConfirmada": p.localizacao_confirmada,
            }
            for p in pessoas
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--saida",
        default=str(PASTA / "dados" / "cnpd-snapshot.json"),
        help="arquivo JSON de saida",
    )
    args = parser.parse_args()

    destino = pathlib.Path(args.saida)
    destino.parent.mkdir(parents=True, exist_ok=True)

    dados = coletar()
    destino.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"gravado: {destino} ({len(dados['registros'])} registros)")


if __name__ == "__main__":
    main()
