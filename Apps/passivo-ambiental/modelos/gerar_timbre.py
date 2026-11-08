"""Copia o brasão e a faixa da missão do modelo timbrado do Agiliza+ para este app.

Provisório, até a Diretoria de Interiorização enviar o layout oficial do laudo
ambiental. O modelo do Agiliza+ não traz dado de caso e cada app continua
autônomo: o resultado fica em modelos/timbre-politec.json e entra no index.html.

Uso: python modelos/gerar_timbre.py
"""
import base64
import json
import pathlib
import zipfile

AQUI = pathlib.Path(__file__).resolve().parent
ORIGEM = AQUI.parent.parent / "agiliza-mais" / "modelos" / "modelo-laudo-politec.docx"

with zipfile.ZipFile(ORIGEM) as z:
    dados = {"brasao": base64.b64encode(z.read("word/media/image1.png")).decode("ascii"),
             "faixa": base64.b64encode(z.read("word/media/image3.jpg")).decode("ascii")}
(AQUI / "timbre-politec.json").write_text(json.dumps(dados), encoding="utf-8")
print("timbre-politec.json", sum(len(v) for v in dados.values()) // 1024, "KB")
