"""Baixa a divisão por distritos (bairros) dos municípios de MT e grava o arquivo
que o app usa, embutido no index.html.

Fonte: API de localidades do IBGE (dados abertos, sem chave).
  https://servicodados.ibge.gov.br/api/v1/localidades/distritos

Saída: mt-distritos.json, no formato {codigo_ibge: ["Nome do distrito", ...]}
O app funciona offline: o arquivo é embutido no index.html e a API nunca é
chamada em tempo de execução.

Uso: python "Apps/equipamentos-google-earth/dados-base/gerar_distritos.py"
"""
import gzip
import json
import pathlib
import time
import urllib.error
import urllib.request

AQUI = pathlib.Path(__file__).resolve().parent
ENTRADA = AQUI / "mt-municipios.json"
SAIDA = AQUI / "mt-distritos.json"
URL = "https://servicodados.ibge.gov.br/api/v1/localidades/distritos"


def baixar(tentativas=3):
    """Baixa a lista de distritos do Brasil (a API não tem filtro por município
    que traga todos os distritos de MT)."""
    for tentativa in range(tentativas):
        try:
            req = urllib.request.Request(URL, headers={"User-Agent": "aula-politec/1.0", "Accept-Encoding": "identity"})
            with urllib.request.urlopen(req, timeout=120) as r:
                bruto = r.read()
                if r.headers.get("Content-Encoding") == "gzip" or bruto[:2] == b"\x1f\x8b":
                    bruto = gzip.decompress(bruto)
                return json.loads(bruto.decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            if tentativa == tentativas - 1:
                raise
            time.sleep(2 * (tentativa + 1))
    return []


def uf_do_distrito(d):
    m = d.get("municipio") or {}
    meso = (m.get("microrregiao") or {}).get("mesorregiao") or {}
    uf = meso.get("UF") or (m.get("regiao-intermediaria") or {}).get("UF")
    return (uf or {}).get("sigla")


def main():
    municipios = json.loads(ENTRADA.read_text(encoding="utf-8"))
    codigos = {m["c"]: m["n"] for m in municipios}
    print("municípios do app:", len(codigos))
    print("baixando a lista de distritos do IBGE...")
    distritos = baixar()
    por_municipio = {}
    for d in distritos:
        if uf_do_distrito(d) != "MT":
            continue
        m = d.get("municipio") or {}
        cod = str(m.get("id") or "")
        if cod not in codigos:
            continue
        por_municipio.setdefault(cod, set()).add(d["nome"].strip())
    saida = {cod: sorted(nomes) for cod, nomes in sorted(por_municipio.items())}
    SAIDA.write_text(json.dumps(saida, ensure_ascii=False, indent=0, sort_keys=True), encoding="utf-8")
    total = sum(len(v) for v in saida.values())
    sem = [codigos[c] for c in codigos if c not in saida]
    print(f"distritos: {total} em {len(saida)} municípios | arquivo: {SAIDA.stat().st_size // 1024} KB")
    if sem:
        print("municípios sem distrito registrado no IBGE:", ", ".join(sorted(sem)))


if __name__ == "__main__":
    main()
