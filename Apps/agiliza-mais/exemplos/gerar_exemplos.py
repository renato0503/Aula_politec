"""Gera os casos fictícios, o modelo Word e a biblioteca de textos do Agiliza + (Sprint 0).

Saídas:
  exemplos/caso-ficticio-001/   caso completo: requisição (PDF com texto e digitalizada),
                                DEVICE INFO.txt, HASHDOHASH.txt, OBJ 01-A e OBJ 01-B com o HTML do SIM
  exemplos/caso-ficticio-002/   aparelho sem cartão SIM (RN06)
  exemplos/caso-ficticio-003/   falta o HASHDOHASH.txt (RN02)
  exemplos/textos.json          textos padronizados e respostas-modelo (fictícios)
  exemplos/FORMATOS.md          formato SUPOSTO dos arquivos; trocar pelas amostras reais
  modelos/modelo-laudo-celular.docx   modelo com marcadores do docxtemplater
  modelos/MARCADORES.md         lista dos marcadores
  exemplos/seed.json            biblioteca de textos no formato do app

IMEI e ICCID com dígito de Luhn válido; SHA-256 aleatório. Tudo fictício.
Semente fixa = 20261029.
Uso: python "Apps/agiliza-mais/exemplos/gerar_exemplos.py"
"""
import hashlib
import json
import pathlib
import random

import fitz  # PyMuPDF
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

AQUI = pathlib.Path(__file__).resolve().parent
MODELOS = AQUI.parent / "modelos"
random.seed(20261029)


def luhn(base):
    soma = 0
    for i, c in enumerate(reversed(base)):
        d = int(c)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        soma += d
    return base + str((10 - soma % 10) % 10)


def imei():
    return luhn("35" + "".join(random.choice("0123456789") for _ in range(12)))


def iccid():
    return luhn("8955" + random.choice(["10", "11", "02", "05"]) + "".join(random.choice("0123456789") for _ in range(12)))


def requisicao_pdf(caminho, caso):
    c = canvas.Canvas(str(caminho), pagesize=A4)
    _, alt = A4
    y = alt - 60
    linhas = [
        ("Helvetica-Bold", 13, "DELEGACIA DE POLÍCIA FICTÍCIA DE CUIABÁ"),
        ("Helvetica-Bold", 12, "REQUISIÇÃO DE EXAME PERICIAL"),
        ("Helvetica", 11, ""),
        ("Helvetica", 11, f"Protocolo: {caso['protocolo']}"),
        ("Helvetica", 11, f"Ofício nº {caso['oficio']}"),
        ("Helvetica", 11, f"Processo nº {caso['processo']}"),
        ("Helvetica", 11, f"Autoridade requisitante: {caso['autoridade']}"),
        ("Helvetica", 11, f"Data da solicitação: {caso['data']}"),
        ("Helvetica", 11, ""),
        ("Helvetica", 11, "Requisito a realização de exame pericial no aparelho celular apreendido,"),
        ("Helvetica", 11, "acondicionado em envelope de segurança, para extração e análise de dados."),
        ("Helvetica", 11, ""),
        ("Helvetica-Bold", 11, "QUESITOS"),
    ] + [("Helvetica", 11, f"{i}) {q}") for i, q in enumerate(caso["quesitos"], 1)] + [
        ("Helvetica", 11, ""), ("Helvetica", 11, "Documento fictício gerado para testes. Sem dados reais.")]
    for fonte, tam, txt in linhas:
        c.setFont(fonte, tam)
        c.drawString(60, y, txt)
        y -= 18
    c.save()


def digitalizar(origem, destino):
    """PDF só com imagem (sem camada de texto), como um documento escaneado."""
    src = fitz.open(origem)
    out = fitz.open()
    for pg in src:
        pix = pg.get_pixmap(dpi=110, colorspace=fitz.csGRAY)
        nova = out.new_page(width=pg.rect.width, height=pg.rect.height)
        nova.insert_image(nova.rect, pixmap=pix)
    out.save(destino)


def device_info(marca, modelo, i1, i2, cor):
    return ("Relatório de extração (formato suposto)\r\n"
            "========================================\r\n"
            f"Manufacturer: {marca}\r\nModel: {modelo}\r\nColor: {cor}\r\n"
            f"IMEI 1: {i1}\r\n" + (f"IMEI 2: {i2}\r\n" if i2 else "") +
            "Operating System: Android 13\r\nExtraction date: 2026-10-21 14:32:10\r\n")


def sim_html(obj, numero, operadora):
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>SIM {obj}</title></head><body>
<h1>Relatório do cartão SIM (formato suposto)</h1>
<table border="1"><tr><th>Campo</th><th>Valor</th></tr>
<tr><td>Objeto</td><td>{obj}</td></tr><tr><td>ICCID</td><td>{numero}</td></tr>
<tr><td>Operadora</td><td>{operadora}</td></tr><tr><td>IMSI</td><td>72410{random.randint(10**9, 10**10 - 1)}</td></tr>
</table></body></html>"""


QUESITOS = ["Qual a marca, o modelo e os IMEIs do aparelho examinado?",
            "O aparelho continha cartão SIM? Em caso positivo, qual a operadora e o ICCID?",
            "Foi possível extrair os dados armazenados no aparelho?",
            "Os dados extraídos foram preservados com garantia de integridade?"]


def caso(n, sims, com_hash=True):
    pasta = AQUI / f"caso-ficticio-{n:03d}"
    pasta.mkdir(exist_ok=True)
    dados = {"protocolo": f"2026.{1000 + n:07d}", "oficio": f"{100 + n}/2026/DPF-CBA", "processo": f"000{1230 + n}-56.2026.8.11.0041",
             "autoridade": "Delegado de Polícia Fictício da Silva", "data": f"{18 + n}/10/2026", "quesitos": QUESITOS}
    requisicao_pdf(pasta / "Requisicao.pdf", dados)
    digitalizar(pasta / "Requisicao.pdf", pasta / "Requisicao-digitalizada.pdf")
    i1, i2 = imei(), (imei() if n != 2 else "")
    marca, modelo = random.choice([("Samsung", "SM-A325M"), ("Motorola", "XT2237-1"), ("Xiaomi", "2201117TL")])
    (pasta / "DEVICE INFO.txt").write_text(device_info(marca, modelo, i1, i2, random.choice(["Preto", "Azul", "Branco"])), encoding="utf-8")
    sha = hashlib.sha256(f"extracao-ficticia-{n}".encode()).hexdigest()
    if com_hash:
        (pasta / "HASHDOHASH.txt").write_text(f"Arquivo: OBJ01_extracao_{n:03d}.zip\r\nAlgoritmo: SHA-256\r\nHash: {sha}\r\n", encoding="utf-8")
    gabarito = {"caso": dados, "aparelho": {"marca": marca, "modelo": modelo, "imei_1": i1, "imei_2": i2},
                "hash": sha if com_hash else None, "sims": []}
    for letra in sims:
        obj = f"01-{letra}"
        num, op = iccid(), random.choice(["VIVO", "CLARO", "TIM"])
        (pasta / f"OBJ {obj}").mkdir(exist_ok=True)
        (pasta / f"OBJ {obj}" / "SIM.html").write_text(sim_html(obj, num, op), encoding="utf-8")
        gabarito["sims"].append({"identificador_objeto": obj, "iccid": num, "operadora": op})
    (pasta / "GABARITO.json").write_text(json.dumps(gabarito, ensure_ascii=False, indent=1), encoding="utf-8")
    return gabarito


SECOES = [
    ("PREÂMBULO", ["Protocolo: {numero_protocolo}        Ofício: {numero_oficio}",
                   "Processo: {numero_processo}",
                   "Autoridade requisitante: {autoridade_solicitante}        Data da solicitação: {data_solicitacao}"]),
    ("1. HISTÓRICO", ["{texto_historico}"]),
    ("2. DESCRIÇÃO DOS OBJETOS", ["Aparelho celular {marca} {modelo}, cor {cor}, IMEI 1 {imei_1}{#imei_2}, IMEI 2 {imei_2}{/imei_2}.",
                                 "{#sims}Objeto {identificador_objeto}: cartão SIM da operadora {operadora}, ICCID {iccid}.{/sims}",
                                 "{^sims}{texto_sem_sim}{/sims}",
                                 "{texto_descricao_objetos}"]),
    ("3. EXAMES", ["{texto_exames}"]),
    ("4. ANEXOS E MÍDIAS", ["Arquivo {hash_arquivo}, algoritmo {hash_algoritmo}, valor {valor_hash}.", "{texto_anexos}"]),
    ("5. QUESITOS E RESPOSTAS", ["{#quesitos}{numero_quesito}) {enunciado}", "Resposta: {resposta}{/quesitos}"]),
    ("6. CONSIDERAÇÕES FINAIS", ["{texto_consideracoes}", "", "Cuiabá, {data_laudo}.", "{nome_perito}", "Perito Oficial Criminal"]),
]


def modelo_docx():
    MODELOS.mkdir(exist_ok=True)
    doc = Document()
    estilo = doc.styles["Normal"]
    estilo.font.name, estilo.font.size = "Arial", Pt(11)
    for txt in ("POLÍCIA JUDICIÁRIA CIVIL · PERÍCIA OFICIAL (MODELO FICTÍCIO)", "LAUDO PERICIAL Nº {numero_laudo}", "Exame em aparelho de telefonia celular"):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(txt)
        r.bold = True
    for titulo, paragrafos in SECOES:
        h = doc.add_paragraph()
        h.add_run(titulo).bold = True
        for t in paragrafos:
            doc.add_paragraph().add_run(t)  # cada marcador fica num único run
    doc.save(MODELOS / "modelo-laudo-celular.docx")
    marcadores = sorted({m for _, ps in SECOES for t in ps for m in __import__("re").findall(r"\{[#^/]?([a-z0-9_]+)\}", t)} | {"numero_laudo"})
    (MODELOS / "MARCADORES.md").write_text(
        "# Marcadores do modelo\n\nSintaxe do docxtemplater: `{campo}` troca pelo valor; `{#lista}...{/lista}` repete para cada item; "
        "`{^lista}...{/lista}` aparece quando a lista está vazia.\n\n"
        "O `modelo-laudo-celular.docx` é **fictício**. No Sprint 0, os mesmos marcadores entram no modelo institucional, "
        "escritos de uma vez (sem formatação no meio do marcador, para o Word não dividir o texto em vários trechos).\n\n"
        "| Marcador | Origem |\n|---|---|\n" + "".join(f"| `{m}` | {origem(m)} |\n" for m in marcadores), encoding="utf-8")


def origem(m):
    if m in ("numero_protocolo", "numero_oficio", "numero_processo", "autoridade_solicitante", "data_solicitacao"):
        return "requisição em PDF"
    if m in ("marca", "modelo", "cor", "imei_1", "imei_2"):
        return "DEVICE INFO.txt"
    if m in ("sims", "identificador_objeto", "operadora", "iccid"):
        return "HTML das pastas OBJ"
    if m in ("hash_arquivo", "hash_algoritmo", "valor_hash"):
        return "HASHDOHASH.txt"
    if m in ("quesitos", "numero_quesito", "enunciado", "resposta"):
        return "requisição + resposta conferida pelo perito"
    if m.startswith("texto_"):
        return "biblioteca de textos padronizados"
    return "perito"


TEXTOS = [
    ("historico", "Histórico padrão", "Em atendimento à requisição em epígrafe, foi encaminhado a este Instituto o material descrito a seguir, acondicionado em envelope de segurança lacrado, para exame pericial."),
    ("descricao_objetos", "Envelope lacrado", "O material foi recebido em envelope de segurança com lacre íntegro, que foi rompido pelo perito no início dos exames."),
    ("sem_sim", "Aparelho sem cartão SIM", "O aparelho não continha cartão SIM no momento do exame."),
    ("exames", "Extração lógica", "Foi realizada extração lógica dos dados do aparelho com ferramenta forense, com geração de relatório e cálculo do hash do material extraído."),
    ("exames", "Extração física", "Foi realizada extração física da memória do aparelho com ferramenta forense, preservando a integridade do conteúdo original."),
    ("anexos", "Mídia de anexos", "Os dados extraídos foram gravados em mídia óptica que acompanha este laudo, identificada pelo valor de hash indicado."),
    ("consideracoes", "Considerações padrão", "Nada mais havendo a relatar, encerra-se o presente laudo, que segue assinado digitalmente pelo perito."),
    ("resposta", "Resposta: identificação do aparelho", "Sim. O aparelho foi identificado conforme a descrição dos objetos (seção 2)."),
    ("resposta", "Resposta: cartão SIM", "Sim. Os dados do cartão SIM constam da descrição dos objetos (seção 2)."),
    ("resposta", "Resposta: extração", "Sim. A extração foi realizada conforme a seção 3."),
    ("resposta", "Resposta: integridade", "Sim. A integridade foi garantida pelo cálculo do hash, informado na seção 4."),
]


def main():
    g = [caso(1, ["A", "B"]), caso(2, []), caso(3, ["A"], com_hash=False)]
    modelo_docx()
    textos = [{"id_texto": f"T{i + 1:02d}", "categoria": c, "titulo": t, "conteudo": x, "versao": "1", "ativo": True} for i, (c, t, x) in enumerate(TEXTOS)]
    (AQUI / "textos.json").write_text(json.dumps(textos, ensure_ascii=False, indent=1), encoding="utf-8")
    (AQUI / "seed.json").write_text(json.dumps({"textos": textos}, ensure_ascii=False, indent=1), encoding="utf-8")
    (AQUI / "FORMATOS.md").write_text(
        "# Formatos dos arquivos do caso (SUPOSTOS)\n\nOs formatos abaixo foram **inventados** para os testes. "
        "No Sprint 0, o grupo traz amostras anonimizadas dos arquivos reais, e as regras de leitura do app são ajustadas a elas.\n\n"
        "| Arquivo | Formato suposto | O app procura |\n|---|---|---|\n"
        "| `DEVICE INFO.txt` | linhas `Rótulo: valor`, CRLF, UTF-8 | `Manufacturer`, `Model`, `Color`, `IMEI 1`, `IMEI 2` |\n"
        "| `HASHDOHASH.txt` | linhas `Rótulo: valor` | `Arquivo`, `Algoritmo`, `Hash` (64 hexadecimais) |\n"
        "| `OBJ 01-A/SIM.html` | tabela com linhas campo / valor | `Objeto`, `ICCID`, `Operadora` |\n"
        "| `Requisicao.pdf` | PDF com texto, rótulos fixos | `Protocolo:`, `Ofício nº`, `Processo nº`, `Autoridade requisitante:`, `Data da solicitação:`, bloco `QUESITOS` |\n"
        "| `Requisicao-digitalizada.pdf` | o mesmo conteúdo, só imagem (sem camada de texto) | exige OCR ou digitação (Sprint 10) |\n\n"
        "Cada pasta traz um `GABARITO.json` com os valores certos, para os testes dos extratores.\n\n"
        "| Caso | Situação |\n|---|---|\n| 001 | completo, 2 cartões SIM (01-A e 01-B) |\n| 002 | sem cartão SIM e sem IMEI 2 (RN06) |\n| 003 | sem `HASHDOHASH.txt` (RN02) |\n",
        encoding="utf-8")
    print("casos", [x["caso"]["protocolo"] for x in g], "| textos", len(textos))


if __name__ == "__main__":
    main()
