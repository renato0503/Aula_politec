"""Cliente Python para o painel publico de desaparecidos do CNPD/MJ.

Nao e uma API oficial: o cliente reproduz as chamadas que o site
https://cnpd.mj.gov.br/painel-publico faz. O endpoint aceita requisicoes sem
autenticacao e devolve CORS aberto (Access-Control-Allow-Origin: *).

Exemplos:
    python api_cnpd.py --nome maria --uf BA --pagina 0
    python api_cnpd.py --id 229101
    python api_cnpd.py --todas --saida desaparecidos.json

Como biblioteca:
    from api_cnpd import CnpdClient
    cli = CnpdClient()
    pagina = cli.filtrar({"sexo": "Feminino", "estado": "MT"})
    for pessoa in pagina.registros:
        print(pessoa.id, pessoa.nome)
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Iterable

BASE_PADRAO = "https://cnpd.mj.gov.br/api/api/painel-publico/desaparecidos"
IMG_PADRAO = "https://cnpd.mj.gov.br/api/desaparecimentos"
ORDENACOES = ("MAIS_RECENTE", "MAIS_ANTIGO", "NOME_ASC", "NOME_DESC")

# Campos aceitos pelo corpo do POST /filtrar (o mesmo formulario do site).
FILTROS = (
    "nome",
    "sexo",
    "racaCor",
    "estado",
    "municipio",
    "idadeAtual",
    "idadeDesaparecimento",
    "faixaEtariaAtualDe",
    "faixaEtariaAtualAte",
    "faixaEtariaDesaparecimentoDe",
    "faixaEtariaDesaparecimentoAte",
    "anoRegistro",
    "mesRegistro",
)


@dataclasses.dataclass(slots=True)
class Pessoa:
    id: int
    nome: str
    idade_atual: int | None = None
    idade_desaparecimento: int | None = None
    sexo: str | None = None
    raca_cor: str | None = None
    local_registro: str | None = None
    uf_registro: str | None = None
    data_desaparecimento: str | None = None
    data_registro_desaparecimento: str | None = None
    localizacao_confirmada: str | None = None

    @classmethod
    def de_json(cls, bruto: dict[str, Any]) -> "Pessoa":
        return cls(
            id=bruto.get("id"),
            nome=bruto.get("nome") or "",
            idade_atual=bruto.get("idadeAtual"),
            idade_desaparecimento=bruto.get("idadeDesaparecimento"),
            sexo=bruto.get("sexo"),
            raca_cor=bruto.get("racaCor"),
            local_registro=bruto.get("localRegistro"),
            uf_registro=bruto.get("ufRegistro"),
            data_desaparecimento=bruto.get("dataDesaparecimento"),
            data_registro_desaparecimento=bruto.get("dataRegistroDesaparecimento"),
            localizacao_confirmada=bruto.get("flLocalizacaoConfirmada"),
        )

    @property
    def localizado(self) -> bool:
        return bool(self.localizacao_confirmada) and self.localizacao_confirmada != "NAO_CONFIRMADO"

    @property
    def data_desaparecimento_iso(self) -> str | None:
        return _iso(self.data_desaparecimento)

    @property
    def data_registro_iso(self) -> str | None:
        return _iso(self.data_registro_desaparecimento)


@dataclasses.dataclass(slots=True)
class Pagina:
    registros: list[Pessoa]
    total_registros: int
    total_paginas: int
    pagina_atual: int
    tamanho_pagina: int


def _iso(data: str | None) -> str | None:
    if not data:
        return None
    try:
        return dt.datetime.strptime(data, "%d/%m/%Y").date().isoformat()
    except ValueError:
        return None


class CnpdClient:
    def __init__(
        self,
        base_url: str = BASE_PADRAO,
        img_url: str = IMG_PADRAO,
        timeout: int = 40,
        user_agent: str = "NIHDE-painel-desaparecidos/1.0 (uso institucional)",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.img_url = img_url.rstrip("/")
        self.timeout = timeout
        self.user_agent = user_agent

    def _abrir(self, req: urllib.request.Request) -> bytes:
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return resp.read()

    def _post(self, url: str, corpo: dict[str, Any]) -> dict[str, Any]:
        req = urllib.request.Request(
            url,
            data=json.dumps(corpo, ensure_ascii=False).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": self.user_agent,
            },
            method="POST",
        )
        return json.loads(self._abrir(req).decode("utf-8"))

    def _get(self, url: str) -> dict[str, Any]:
        req = urllib.request.Request(
            url,
            headers={"Accept": "application/json", "User-Agent": self.user_agent},
            method="GET",
        )
        return json.loads(self._abrir(req).decode("utf-8"))

    def filtrar(
        self,
        filtros: dict[str, Any] | None = None,
        ordenacao: str = "MAIS_RECENTE",
        pagina: int = 0,
    ) -> Pagina:
        if ordenacao not in ORDENACOES:
            raise ValueError(f"ordenacao deve ser uma de {ORDENACOES}")
        corpo = {k: v for k, v in (filtros or {}).items() if k in FILTROS and v not in (None, "")}
        url = f"{self.base_url}/filtrar?ordenacao={ordenacao}&pagina={int(pagina)}"
        bruto = self._post(url, corpo)
        return Pagina(
            registros=[Pessoa.de_json(p) for p in bruto.get("desaparecidos") or []],
            total_registros=int(bruto.get("totalRegistros") or 0),
            total_paginas=int(bruto.get("totalPaginas") or 0),
            pagina_atual=int(bruto.get("paginaAtual") or 0),
            tamanho_pagina=int(bruto.get("tamanhoPagina") or 0),
        )

    def obter(self, pessoa_id: int) -> Pessoa:
        return Pessoa.de_json(self._get(f"{self.base_url}/{int(pessoa_id)}"))

    def imagem(self, pessoa_id: int) -> tuple[str, bytes]:
        """Devolve (extensao, bytes) da foto principal. Somente /main e publico."""
        bruto = self._get(f"{self.img_url}/{int(pessoa_id)}/arquivos-imagem/main")
        dto = (bruto.get("arquivoCnpd") or {}).get("arquivoDTO") or {}
        conteudo = dto.get("conteudo")
        if not conteudo:
            raise LookupError(f"pessoa {pessoa_id} sem imagem principal")
        import base64

        return str(dto.get("extensao") or "jpg"), base64.b64decode(conteudo)

    def todas(
        self,
        filtros: dict[str, Any] | None = None,
        ordenacao: str = "MAIS_RECENTE",
        pausa: float = 0.4,
        progresso: bool = True,
    ) -> list[Pessoa]:
        pagina = 0
        total_paginas = 1
        vistos: set[int] = set()
        acumulado: list[Pessoa] = []
        while pagina < total_paginas:
            lote = self.filtrar(filtros, ordenacao, pagina)
            total_paginas = lote.total_paginas or 1
            for pessoa in lote.registros:
                if pessoa.id in vistos:
                    continue
                vistos.add(pessoa.id)
                acumulado.append(pessoa)
            if progresso:
                print(
                    f"pagina {pagina + 1}/{total_paginas}: {len(lote.registros)} itens "
                    f"(acumulado {len(acumulado)}/{lote.total_registros})",
                    file=sys.stderr,
                )
            pagina += 1
            if pagina < total_paginas:
                time.sleep(pausa)
        return acumulado


def _json_padrao(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    raise TypeError(f"tipo nao serializavel: {type(obj)!r}")


def main(argv: Iterable[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Consulta o painel publico do CNPD/MJ")
    p.add_argument("--nome", help="trecho do nome")
    p.add_argument("--uf", help="UF do registro, ex.: MT")
    p.add_argument("--municipio", help="municipio do registro")
    p.add_argument("--sexo", choices=["Masculino", "Feminino", "Intersexo"])
    p.add_argument("--idade-de", type=int, dest="idade_de", help="idade atual minima")
    p.add_argument("--idade-ate", type=int, dest="idade_ate", help="idade atual maxima")
    p.add_argument("--ordenacao", default="MAIS_RECENTE", choices=ORDENACOES)
    p.add_argument("--pagina", type=int, default=0)
    p.add_argument("--id", type=int, help="busca uma pessoa pelo id")
    p.add_argument("--todas", action="store_true", help="percorre todas as paginas")
    p.add_argument("--saida", help="grava o resultado em JSON")
    args = p.parse_args(list(argv) if argv is not None else None)

    cli = CnpdClient()
    try:
        if args.id:
            obj: Any = cli.obter(args.id)
        else:
            filtros = {
                "nome": args.nome or "",
                "estado": args.uf or "",
                "municipio": args.municipio or "",
                "sexo": args.sexo or "",
                "faixaEtariaAtualDe": args.idade_de,
                "faixaEtariaAtualAte": args.idade_ate,
            }
            if args.todas:
                obj = cli.todas(filtros, args.ordenacao)
            else:
                obj = cli.filtrar(filtros, args.ordenacao, args.pagina)
    except urllib.error.HTTPError as e:
        print(f"erro HTTP {e.code}: {e.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"falha de rede: {e.reason}", file=sys.stderr)
        return 1

    texto = json.dumps(obj, ensure_ascii=False, indent=2, default=_json_padrao)
    if args.saida:
        with open(args.saida, "w", encoding="utf-8") as fh:
            fh.write(texto)
        print(f"gravado: {args.saida}", file=sys.stderr)
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
