"""Prepara os dados do mapa: municipios, centroides de UF e malha das UFs.

Fontes (guardadas em dados/fontes/):
- Municipios-Brasileiros (kelvins/Municipios-Brasileiros, MIT): nome, latitude,
  longitude de cada municipio.
- Malhas Territoriais do IBGE (qualidade minima, por UF).

Saidas:
- dados/municipios-br.json  -> {uf: {chave_do_municipio: [lat, lon]}}
- dados/brasil-ufs.geojson  -> FeatureCollection com propriedades uf e nome
- dados/ufs-centroides.json -> {uf: {nome, lat, lon}}

Uso:
    python preparar_mapa.py
    python preparar_mapa.py --snapshot dados/cnpd-snapshot.json   # confere cobertura
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
import unicodedata

PASTA = pathlib.Path(__file__).resolve().parent
FONTES = PASTA / "dados" / "fontes"

UFS = {
    "11": ("RO", "Rondônia"),
    "12": ("AC", "Acre"),
    "13": ("AM", "Amazonas"),
    "14": ("RR", "Roraima"),
    "15": ("PA", "Pará"),
    "16": ("AP", "Amapá"),
    "17": ("TO", "Tocantins"),
    "21": ("MA", "Maranhão"),
    "22": ("PI", "Piauí"),
    "23": ("CE", "Ceará"),
    "24": ("RN", "Rio Grande do Norte"),
    "25": ("PB", "Paraíba"),
    "26": ("PE", "Pernambuco"),
    "27": ("AL", "Alagoas"),
    "28": ("SE", "Sergipe"),
    "29": ("BA", "Bahia"),
    "31": ("MG", "Minas Gerais"),
    "32": ("ES", "Espírito Santo"),
    "33": ("RJ", "Rio de Janeiro"),
    "35": ("SP", "São Paulo"),
    "41": ("PR", "Paraná"),
    "42": ("SC", "Santa Catarina"),
    "43": ("RS", "Rio Grande do Sul"),
    "50": ("MS", "Mato Grosso do Sul"),
    "51": ("MT", "Mato Grosso"),
    "52": ("GO", "Goiás"),
    "53": ("DF", "Distrito Federal"),
}
CODIGO_POR_UF = {sigla: codigo for codigo, (sigla, _) in UFS.items()}


def chave(texto: str) -> str:
    """Mesma normalizacao usada no JavaScript do painel."""
    decomposto = unicodedata.normalize("NFKD", str(texto or ""))
    sem_acento = "".join(c for c in decomposto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", sem_acento.lower())).strip()


def ler_municipios() -> tuple[dict, dict]:
    caminho = FONTES / "municipios.csv"
    municipios: dict[str, dict[str, list[float]]] = {}
    somas: dict[str, list[float]] = {}
    with caminho.open(encoding="utf-8", newline="") as fh:
        for linha in csv.DictReader(fh):
            codigo = str(linha.get("codigo_uf") or "").zfill(2)
            if codigo not in UFS:
                continue
            sigla = UFS[codigo][0]
            nome = linha.get("nome") or ""
            try:
                lat = float(linha["latitude"])
                lon = float(linha["longitude"])
            except (KeyError, TypeError, ValueError):
                continue
            municipios.setdefault(sigla, {})[chave(nome)] = [
                round(lat, 5),
                round(lon, 5),
            ]
            soma = somas.setdefault(sigla, [0.0, 0.0, 0])
            soma[0] += lat
            soma[1] += lon
            soma[2] += 1

    centroides = {}
    for sigla, (soma_lat, soma_lon, total) in somas.items():
        centroides[sigla] = {
            "nome": UFS[CODIGO_POR_UF[sigla]][1],
            "lat": round(soma_lat / total, 5),
            "lon": round(soma_lon / total, 5),
            "municipios": total,
        }
    return municipios, centroides


def arredondar_coordenadas(objeto):
    if isinstance(objeto, (int, float)):
        return round(float(objeto), 4)
    if isinstance(objeto, list):
        return [arredondar_coordenadas(item) for item in objeto]
    if isinstance(objeto, dict):
        return {k: arredondar_coordenadas(v) for k, v in objeto.items()}
    return objeto


def ler_malha() -> dict:
    bruto = json.loads((FONTES / "brasil-ufs-ibge.geojson").read_text(encoding="utf-8"))
    feicoes = []
    for feicao in bruto.get("features", []):
        codigo = str((feicao.get("properties") or {}).get("codarea") or "").zfill(2)
        if codigo not in UFS:
            continue
        sigla, nome = UFS[codigo]
        feicoes.append(
            {
                "type": "Feature",
                "properties": {"uf": sigla, "nome": nome},
                "geometry": arredondar_coordenadas(feicao["geometry"]),
            }
        )
    return {"type": "FeatureCollection", "features": feicoes}


US_FIPS = {
    "01": ("AL", "Alabama"), "02": ("AK", "Alaska"), "04": ("AZ", "Arizona"),
    "05": ("AR", "Arkansas"), "06": ("CA", "Califórnia"), "08": ("CO", "Colorado"),
    "09": ("CT", "Connecticut"), "10": ("DE", "Delaware"), "11": ("DC", "Distrito de Colúmbia"),
    "12": ("FL", "Flórida"), "13": ("GA", "Geórgia"), "15": ("HI", "Havaí"),
    "16": ("ID", "Idaho"), "17": ("IL", "Illinois"), "18": ("IN", "Indiana"),
    "19": ("IA", "Iowa"), "20": ("KS", "Kansas"), "21": ("KY", "Kentucky"),
    "22": ("LA", "Luisiana"), "23": ("ME", "Maine"), "24": ("MD", "Maryland"),
    "25": ("MA", "Massachusetts"), "26": ("MI", "Michigan"), "27": ("MN", "Minnesota"),
    "28": ("MS", "Mississippi"), "29": ("MO", "Missouri"), "30": ("MT", "Montana"),
    "31": ("NE", "Nebraska"), "32": ("NV", "Nevada"), "33": ("NH", "Nova Hampshire"),
    "34": ("NJ", "Nova Jersey"), "35": ("NM", "Novo México"), "36": ("NY", "Nova York"),
    "37": ("NC", "Carolina do Norte"), "38": ("ND", "Dakota do Norte"), "39": ("OH", "Ohio"),
    "40": ("OK", "Oklahoma"), "41": ("OR", "Oregon"), "42": ("PA", "Pensilvânia"),
    "44": ("RI", "Rhode Island"), "45": ("SC", "Carolina do Sul"), "46": ("SD", "Dakota do Sul"),
    "47": ("TN", "Tennessee"), "48": ("TX", "Texas"), "49": ("UT", "Utah"),
    "50": ("VT", "Vermont"), "51": ("VA", "Virgínia"), "53": ("WA", "Washington"),
    "54": ("WV", "Virgínia Ocidental"), "55": ("WI", "Wisconsin"), "56": ("WY", "Wyoming"),
}


def ler_malha_eua() -> dict:
    bruto = json.loads((FONTES / "us-states.geojson").read_text(encoding="utf-8"))
    feicoes = []
    for feicao in bruto.get("features", []):
        codigo = str(feicao.get("id") or "").zfill(2)
        if codigo not in US_FIPS:
            continue
        sigla, nome = US_FIPS[codigo]
        feicoes.append(
            {
                "type": "Feature",
                "properties": {"uf": sigla, "nome": nome},
                "geometry": arredondar_coordenadas(feicao["geometry"]),
            }
        )
    return {"type": "FeatureCollection", "features": feicoes}


def municipios_do_snapshot(snapshot: pathlib.Path, municipios: dict) -> dict:
    """Só os municípios que aparecem no snapshot, para o app ficar leve."""
    if not snapshot.exists():
        return {}
    dados = json.loads(snapshot.read_text(encoding="utf-8"))
    reduzido: dict[str, dict[str, list[float]]] = {}
    for pessoa in dados.get("registros") or []:
        local = pessoa.get("localRegistro") or ""
        uf = (pessoa.get("ufRegistro") or "").strip().upper()
        if "/" in local:
            cidade, uf_local = local.rsplit("/", 1)
            uf = uf_local.strip().upper() or uf
        else:
            cidade = local
        k = chave(cidade)
        coord = municipios.get(uf, {}).get(k)
        if coord:
            reduzido.setdefault(uf, {})[k] = coord
    return reduzido


def cobertura(snapshot: pathlib.Path, municipios: dict) -> None:
    if not snapshot.exists():
        return
    dados = json.loads(snapshot.read_text(encoding="utf-8"))
    registros = dados.get("registros") or []
    achados = 0
    faltando: dict[str, int] = {}
    for pessoa in registros:
        local = pessoa.get("localRegistro") or ""
        uf = (pessoa.get("ufRegistro") or "").strip().upper()
        if "/" in local:
            cidade, uf_local = local.rsplit("/", 1)
            uf = uf_local.strip().upper() or uf
        else:
            cidade = local
        if chave(cidade) in municipios.get(uf, {}):
            achados += 1
        else:
            faltando[local or "?"] = faltando.get(local or "?", 0) + 1
    print(f"cobertura: {achados}/{len(registros)} registros com coordenada")
    if faltando:
        print("sem coordenada:")
        for local, total in sorted(faltando.items(), key=lambda x: -x[1]):
            print(f"  {local}: {total}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--snapshot",
        default=str(PASTA / "dados" / "cnpd-snapshot.json"),
        help="snapshot para conferir a cobertura",
    )
    args = parser.parse_args()

    municipios, centroides = ler_municipios()
    malha = ler_malha()
    malha_eua = ler_malha_eua()
    snapshot = pathlib.Path(args.snapshot)
    reduzido = municipios_do_snapshot(snapshot, municipios)

    destino_municipios = PASTA / "dados" / "municipios-br.json"
    destino_municipios.write_text(
        json.dumps(municipios, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    destino_centroides = PASTA / "dados" / "ufs-centroides.json"
    destino_centroides.write_text(
        json.dumps(centroides, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    destino_malha = PASTA / "dados" / "brasil-ufs.geojson"
    destino_malha.write_text(
        json.dumps(malha, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    destino_reduzido = PASTA / "dados" / "municipios-cnpd.json"
    destino_reduzido.write_text(
        json.dumps(reduzido, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    destino_eua = PASTA / "dados" / "eua-ufs.geojson"
    destino_eua.write_text(
        json.dumps(malha_eua, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    total = sum(len(v) for v in municipios.values())
    print(f"municipios: {total} em {len(municipios)} UFs")
    print(f"malha BR: {len(malha['features'])} UFs")
    print(f"malha EUA: {len(malha_eua['features'])} estados")
    print(f"municípios do snapshot: {sum(len(v) for v in reduzido.values())}")
    print(f"gravado: {destino_municipios}")
    print(f"gravado: {destino_centroides}")
    print(f"gravado: {destino_malha}")
    print(f"gravado: {destino_reduzido}")
    print(f"gravado: {destino_eua}")
    cobertura(snapshot, municipios)


if __name__ == "__main__":
    main()
