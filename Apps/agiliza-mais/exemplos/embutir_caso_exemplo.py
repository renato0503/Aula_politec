"""Empacota o caso fictício 001 (sem o PDF digitalizado, de 1,1 MB) num JSON que
o construir.py embute no index.html. O botão "Carregar caso de exemplo" usa
esses arquivos como se a pasta tivesse sido escolhida.

Uso: python exemplos/embutir_caso_exemplo.py
"""
import base64
import json
import pathlib

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI / "caso-ficticio-001"
SAIDA = AQUI / "caso-exemplo.json"

arquivos = []
for f in sorted(PASTA.rglob("*")):
    if f.is_dir() or f.name in ("GABARITO.json", "Requisicao-digitalizada.pdf"):
        continue
    arquivos.append({"caminho": f.relative_to(PASTA).as_posix(), "b64": base64.b64encode(f.read_bytes()).decode()})
SAIDA.write_text(json.dumps({"pasta": PASTA.name, "arquivos": arquivos}, ensure_ascii=False), encoding="utf-8")
print(len(arquivos), "arquivos |", SAIDA.stat().st_size // 1024, "KB")
