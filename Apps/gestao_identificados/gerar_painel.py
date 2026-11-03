"""Gera o desaparecidos.html do painel a partir do template e do snapshot do CNPD.

Fonte dos dados: dados/cnpd-snapshot.json (gerado por coletar_dados.py).
Fonte da tela:   painel/template.html.

O snapshot e embutido no HTML para o painel abrir com duplo clique, sem
servidor e sem depender de rede (as fotos, quando disponiveis, sao carregadas
do CNPD sob demanda).

Uso:
    python gerar_painel.py
    python gerar_painel.py --snapshot dados/cnpd-snapshot.json --saida index.html
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re

PASTA = pathlib.Path(__file__).resolve().parent
PLACEHOLDER = "/*__DADOS__*/null"
PLACEHOLDER_MAPA = "/*__MAPA__*/null"


def json_seguro(dados: dict) -> str:
    texto = json.dumps(dados, ensure_ascii=False, separators=(",", ":"))
    # impede que um nome com "</script>" feche o bloco antes da hora
    return texto.replace("<", "\\u003c").replace(">", "\\u003e")


def carregar_mapa() -> dict | None:
    dados = PASTA / "dados"
    try:
        municipios = json.loads((dados / "municipios-br.json").read_text(encoding="utf-8"))
        ufs = json.loads((dados / "ufs-centroides.json").read_text(encoding="utf-8"))
        geojson = json.loads((dados / "brasil-ufs.geojson").read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("aviso: dados do mapa ausentes; rode preparar_mapa.py")
        return None
    return {"municipios": municipios, "ufs": ufs, "geojson": geojson}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--snapshot",
        default=str(PASTA / "dados" / "cnpd-snapshot.json"),
        help="snapshot coletado do CNPD",
    )
    parser.add_argument(
        "--template",
        default=str(PASTA / "painel" / "template.html"),
        help="template HTML com o marcador",
    )
    parser.add_argument(
        "--saida",
        default=str(PASTA / "desaparecidos.html"),
        help="arquivo HTML de saida",
    )
    args = parser.parse_args()

    snapshot = json.loads(pathlib.Path(args.snapshot).read_text(encoding="utf-8"))
    template = pathlib.Path(args.template).read_text(encoding="utf-8")

    if PLACEHOLDER not in template:
        raise SystemExit(f"marcador {PLACEHOLDER!r} nao encontrado no template")

    html = template.replace(PLACEHOLDER, json_seguro(snapshot))
    if PLACEHOLDER_MAPA in template:
        mapa = carregar_mapa()
        html = html.replace(PLACEHOLDER_MAPA, json_seguro(mapa) if mapa else "null")
    destino = pathlib.Path(args.saida)
    destino.write_text(html, encoding="utf-8")

    tamanho = destino.stat().st_size / 1024
    print(
        f"gerado: {destino} ({tamanho:.0f} KB, "
        f"{len(snapshot.get('registros', []))} registros)"
    )


if __name__ == "__main__":
    main()
