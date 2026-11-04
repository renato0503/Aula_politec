"""Atualiza o seed do TEIA para o Sprint 4 do feedback (03/11/2026).

Mudanças:
- remove `numero_cobranca` e `nivel`;
- acrescenta `nome_vitima`, `nome_investigado` e `reu_preso`;
- `data_cobranca` passa a ser a data do e-mail (`recebido_em`);
- protocolo no formato `nnnnnn/aaaa`;
- tipo de crime nas quatro categorias do feedback;
- AR para confronto em Sim/Não/Não informado;
- regional com a lista enviada pelo Nelson;
- cria uma cobrança reiterada (EM-001 e EM-006 com o mesmo protocolo).

O script é idempotente: pode ser rodado de novo sobre o seed já atualizado.
Uso: python exemplos/atualizar_seed_feedback.py
"""
from __future__ import annotations

import json
import pathlib
import re

PASTA = pathlib.Path(__file__).resolve().parent
SEED = PASTA / "seed.json"

REGIONAIS = {
    "Cuiabá": "Coordenadoria de Perícias em Vivos",
    "Várzea Grande": "Coordenadoria de Perícias em Vivos",
    "Sinop": "Coordenadoria Regional de Sinop",
    "Rondonópolis": "Coordenadoria Regional de Rondonópolis",
    "Cáceres": "Coordenadoria Regional de Cáceres",
    "Barra do Garças": "Coordenadoria Regional de Barra do Garças",
    "Tangará da Serra": "Coordenadoria Regional de Tangará da Serra",
    "Alta Floresta": "Gerência Regional de Alta Floresta",
}
CRIMES = {
    "Homicídio": "Local de Crime",
    "Tráfico de drogas": "Biologia",
    "Latrocínio": "Local de Crime",
    "Violência doméstica": "Crime Sexual",
    "Roubo": "Local de Crime",
    "Abuso sexual": "Crime Sexual",
    "Local de crime": "Local de Crime",
}
CRIME_POR_ID = {
    "EM-004": "Identificação Humana",
    "EM-008": "Identificação Humana",
    "EM-010": "Biologia",
}
NOMES = {
    "EM-001": ("Maria Clara Souza", "João Pedro Alves", "Não"),
    "EM-002": ("Ana Beatriz Lima", "Carlos Eduardo Ferreira", "Não informado"),
    "EM-003": ("Bruna Almeida", "Rafael Souza", "Não"),
    "EM-004": ("José Carlos Pereira", "Marcos Vinícius", "Sim"),
    "EM-005": ("Luana Santos", "Pedro Henrique", "Não"),
    "EM-006": ("Patrícia Gomes", "André Luiz", "Não informado"),
    "EM-007": ("Fernanda Alves", "Marcos Paulo", "Sim"),
    "EM-008": ("Pedro Henrique Lima", "Não informado", "Não"),
    "EM-009": ("Não informado", "Não informado", "Não informado"),
    "EM-010": ("Juliana Ribeiro", "Não informado", "Não"),
}
PROTOCOLO_DUPLICADO = "001001/2026"


def protocolo(novo: str | None, antigo: str) -> str:
    if antigo == "2026.1006-DNA":
        return PROTOCOLO_DUPLICADO
    m = re.fullmatch(r"2026\.(\d{4})-DNA", antigo or "")
    if m:
        return f"{int(m.group(1)):06d}/2026"
    if re.fullmatch(r"\d{6}/\d{4}", antigo or ""):
        return antigo
    return antigo or ""


def main() -> None:
    dados = json.loads(SEED.read_text(encoding="utf-8"))
    for email in dados["emails"]:
        ident = email["id"]
        c = email.get("campos") or {}
        antigo_protocolo = c.get("protocolo") or ""
        novo_protocolo = protocolo(None, antigo_protocolo)
        nome_vitima, nome_investigado, reu_preso = NOMES.get(
            ident, ("Não informado", "Não informado", "Não informado")
        )
        c.pop("numero_cobranca", None)
        c.pop("nivel", None)
        c["data_cobranca"] = (email.get("recebido_em") or "")[:10]
        c["protocolo"] = novo_protocolo
        c["tipo_crime"] = CRIME_POR_ID.get(ident, CRIMES.get(c.get("tipo_crime"), c.get("tipo_crime") or ""))
        c["nome_vitima"] = nome_vitima
        c["nome_investigado"] = nome_investigado
        c["reu_preso"] = reu_preso
        c["ar_para_confronto"] = {
            "Pendente de recebimento físico": "Não informado",
            "": "",
        }.get(c.get("ar_para_confronto"), c.get("ar_para_confronto") or "")
        c["regional"] = REGIONAIS.get(c.get("regional"), c.get("regional") or "")
        email["campos"] = c
        if antigo_protocolo and antigo_protocolo != novo_protocolo:
            email["corpo"] = str(email.get("corpo") or "").replace(antigo_protocolo, novo_protocolo)
        if re.search(r"2026\.\d{4}-DNA", email.get("corpo") or "") and novo_protocolo:
            email["corpo"] = re.sub(r"2026\.\d{4}-DNA", novo_protocolo, email["corpo"])
    SEED.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"seed atualizado: {len(dados['emails'])} e-mails")


if __name__ == "__main__":
    main()
