"""Coleta uma amostra pública de casos do NamUs (EUA) com Scrapling.

Fonte: https://www.namus.gov/MissingPersons/Search
API usada pelo próprio site:
  POST /api/CaseSets/NamUs/MissingPersons/Search
  GET  /api/CaseSets/NamUs/MissingPersons/Cases/{id}

O NamUs não é uma API oficial documentada; o coletor reproduz as chamadas do
site. A amostra é limitada de propósito (padrão: 400 casos mais recentes) para
não sobrecarregar o serviço e para caber no HTML offline do MVP. O total
informado pelo NamUs é gravado em `total_registros_informado`.

Uso:
    python coletar_namus.py                 # 400 casos
    python coletar_namus.py --limite 100
    python coletar_namus.py --limite 0      # tenta todos (26 mil; demorado)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import time

from scrapling.fetchers import Fetcher

PASTA = pathlib.Path(__file__).resolve().parent
BUSCA = "https://www.namus.gov/api/CaseSets/NamUs/MissingPersons/Search"
CASO = "https://www.namus.gov/api/CaseSets/NamUs/MissingPersons/Cases/{id}"
PROJECOES = [
    "idFormatted",
    "dateOfLastContact",
    "lastName",
    "firstName",
    "computedMissingMinAge",
    "computedMissingMaxAge",
    "cityOfLastContact",
    "countyDisplayNameOfLastContact",
    "stateDisplayNameOfLastContact",
    "gender",
    "raceEthnicity",
    "modifiedDateTime",
    "namus2Number",
]


def _texto(valor) -> str:
    if isinstance(valor, dict):
        return valor.get("localizedName") or valor.get("name") or ""
    return str(valor or "")


def _sexo(nome: str) -> str:
    return {"Female": "Feminino", "Male": "Masculino", "Other": "Outro", "Unsure": "Não informado"}.get(
        nome, nome or "Não informado"
    )


def _data_iso(valor: str | None) -> str | None:
    if not valor:
        return None
    return str(valor)[:10] if len(str(valor)) >= 10 else str(valor)


def buscar(skip: int, take: int = 100) -> dict:
    corpo = {
        "predicates": [],
        "take": take,
        "skip": skip,
        "projections": PROJECOES,
        "orderSpecifications": [{"field": "dateOfLastContact", "direction": "Descending"}],
        "documentFragments": ["birthDate"],
    }
    resposta = Fetcher.post(BUSCA, json=corpo, timeout=60)
    if resposta.status != 200:
        raise RuntimeError(f"busca HTTP {resposta.status}")
    return json.loads(resposta.body.decode("utf-8"))


def detalhe(caso_id: int) -> dict | None:
    resposta = Fetcher.get(CASO.format(id=caso_id), timeout=60)
    if resposta.status != 200:
        return None
    return json.loads(resposta.body.decode("utf-8"))


def normalizar(bruto: dict, completo: dict | None) -> dict:
    ident = (completo or {}).get("subjectIdentification") or {}
    desc = (completo or {}).get("subjectDescription") or {}
    local = ((completo or {}).get("sighting") or {}).get("address") or {}
    geo = (((completo or {}).get("sighting") or {}).get("publicGeolocation") or {}).get("coordinates") or {}

    primeiro = ident.get("firstName") or bruto.get("firstName") or ""
    meio = ident.get("middleName") or ""
    ultimo = ident.get("lastName") or bruto.get("lastName") or ""
    nome = " ".join(p for p in (primeiro, meio, ultimo) if p).strip() or "Sem nome"

    idade = ident.get("computedMissingMinAge", bruto.get("computedMissingMinAge"))
    idade_atual = (
        ident.get("currentMinAge")
        or bruto.get("currentAgeFrom")
        or bruto.get("computedMissingMinAge")
    )
    cidade = local.get("city") or bruto.get("cityOfLastContact") or ""
    uf = _texto(local.get("state")) or bruto.get("stateDisplayNameOfLastContact") or ""
    if not uf and local.get("state"):
        uf = _texto(local.get("state"))

    return {
        "id": bruto.get("namus2Number") or (completo or {}).get("id"),
        "idFormatado": bruto.get("idFormatted") or (completo or {}).get("idFormatted"),
        "nome": nome,
        "idadeAtual": idade_atual,
        "idadeDesaparecimento": idade,
        "sexo": _sexo(_texto(desc.get("sex")) or bruto.get("gender") or ""),
        "racaCor": _texto(desc.get("primaryEthnicity")) or bruto.get("raceEthnicity") or "",
        "localRegistro": f"{cidade}/{uf}".strip("/") if cidade or uf else "",
        "ufRegistro": uf,
        "dataDesaparecimento": _data_iso(bruto.get("dateOfLastContact")),
        "dataRegistroDesaparecimento": _data_iso((completo or {}).get("modifiedDateTime")),
        "flLocalizacaoConfirmada": "CONFIRMADO" if (completo or {}).get("caseIsResolved") else "NAO_CONFIRMADO",
        "lat": geo.get("lat"),
        "lon": geo.get("lon"),
        "url": f"https://www.namus.gov/MissingPersons/Case#/{bruto.get('namus2Number')}",
        "fonte": "NamUs",
    }


def coletar(limite: int = 400, pausa: float = 0.15) -> dict:
    total_informado = 0
    registros: list[dict] = []
    vistos: set[int] = set()
    skip = 0
    while limite <= 0 or len(registros) < limite:
        lote = buscar(skip, 100)
        total_informado = int(lote.get("count") or 0)
        resultados = lote.get("results") or []
        if not resultados:
            break
        for bruto in resultados:
            if limite > 0 and len(registros) >= limite:
                break
            numero = bruto.get("namus2Number")
            if not numero or numero in vistos:
                continue
            vistos.add(numero)
            completo = detalhe(numero)
            registros.append(normalizar(bruto, completo))
            if len(registros) % 25 == 0:
                print(f"  {len(registros)} casos...", flush=True)
            time.sleep(pausa)
        print(f"pagina skip={skip}: {len(registros)} acumulados de {total_informado}", flush=True)
        skip += len(resultados)
        if skip >= total_informado:
            break

    return {
        "fonte": "NamUs - National Missing and Unidentified Persons System (EUA)",
        "site": "https://www.namus.gov/MissingPersons/Search",
        "endpoint": BUSCA,
        "coletado_em": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "total_registros_informado": total_informado,
        "total_registros_coletado": len(registros),
        "amostra": limite if limite > 0 else "completa",
        "ordenacao": "dateOfLastContact descendente",
        "registros": registros,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limite", type=int, default=400, help="0 = todos")
    parser.add_argument("--pausa", type=float, default=0.15)
    parser.add_argument(
        "--saida",
        default=str(PASTA / "dados" / "namus-snapshot.json"),
    )
    args = parser.parse_args()

    destino = pathlib.Path(args.saida)
    destino.parent.mkdir(parents=True, exist_ok=True)
    print(f"coletando NamUs (limite={args.limite or 'todos'})...")
    dados = coletar(args.limite, args.pausa)
    destino.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"gravado: {destino} ({len(dados['registros'])} de {dados['total_registros_informado']})")


if __name__ == "__main__":
    main()
