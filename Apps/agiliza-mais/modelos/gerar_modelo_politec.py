"""Gera o modelo institucional do laudo com os marcadores do docxtemplater.

Parte do layout enviado pela equipe (CASO TESTE 2/MODELO DE LAUDO - Projeto.dotx),
mantém cabeçalho, rodapé, brasão, faixa da missão e estilos, e troca cada dado do
caso real por um marcador. O resultado não traz nome, IMEI, ICCID, lacre nem número
de procedimento do caso de origem: ele é embutido no index.html, que é publicado.

Saída: modelos/modelo-laudo-politec.docx e modelos/modelo-laudo-politec.json
Uso:   python modelos/gerar_modelo_politec.py
"""
import base64
import json
import pathlib
import re
import zipfile

AQUI = pathlib.Path(__file__).resolve().parent
ORIGEM = AQUI.parent / "CASO TESTE 2" / "MODELO DE LAUDO - Projeto.dotx"
SAIDA = AQUI / "modelo-laudo-politec.docx"
JSON_SAIDA = AQUI / "modelo-laudo-politec.json"

RE_P = re.compile(r"<w:p[ >].*?</w:p>", re.S)
RE_T = re.compile(r"<w:t(?: [^>]*)?>([^<]*)</w:t>")
# dados do caso de origem: nada disto pode sobrar no modelo gerado.
# a lista fica na pasta do caso (fora do repositório), para o script não publicar dado real
PROIBIDOS = [x.strip() for x in (ORIGEM.parent / "dados-de-origem.txt").read_text(encoding="utf-8").splitlines() if x.strip()]


def define_runs(p, novos):
    """Troca o texto dos <w:t> das posições indicadas; os demais ficam como estão."""
    i = -1

    def troca(m):
        nonlocal i
        i += 1
        if i not in novos:
            return m.group(0)
        return f'<w:t xml:space="preserve">{novos[i]}</w:t>'

    return RE_T.sub(troca, p)


def um_texto(p, texto):
    """Deixa o parágrafo com um texto só, na formatação do primeiro trecho."""
    n = len(RE_T.findall(p))
    return define_runs(p, {i: (texto if i == 0 else "") for i in range(n)})


def marcador(tag):
    return f'<w:p><w:r><w:t>{tag}</w:t></w:r></w:p>'


def quebra_antes(p):
    return p.replace("<w:pPr>", "<w:pPr><w:pageBreakBefore/>", 1)


def corpo(xml):
    ini = xml.index("<w:body>") + len("<w:body>")
    ps = list(RE_P.finditer(xml, ini))
    trocas = {}
    P = lambda n: ps[n].group(0)

    trocas[11] = define_runs(P(11), {0: "LAUDO PERICIAL Nº {numero_laudo}", 1: "", 2: ""})
    trocas[15] = um_texto(P(15), "Contém o presente Laudo Pericial o total de {total_folhas_texto} folhas, onde fica arquivada digitalmente "
                                 "no sistema de laudos uma cópia, sendo todas as folhas devidamente numeradas da forma como segue: ")
    # o .dotx veio de uma conversão e colava dois itens no mesmo parágrafo: aqui cada um fica no seu
    trocas[18] = um_texto(P(18), "As páginas de 02 a {ultima_folha} compõem o texto;").replace("<w:tab/>", "")         + um_texto(P(18), "Em anexo envelope(s) de segurança de número:").replace("<w:tab/>", "")
    trocas[20] = define_runs(P(20), {1: " {lacre_saida} contendo os objetos encaminhados para esta gerência com seu lacre de entrada;", 2: "", 3: ""})
    for n in (5, 6, 7, 12, 13):  # linhas em branco a menos: a folha de rosto cabe em uma página com todas as referências
        assert not "".join(RE_T.findall(P(n))).strip() and "w:drawing" not in P(n), n
        trocas[n] = ""
    trocas[22] = define_runs(P(22), {0: "Requisição de Perícia {numero_requisicao}"})
    trocas[24] = define_runs(P(24), {0: "{data_solicitacao}"})
    trocas[26] = define_runs(P(26), {0: "{natureza_exame}"})
    trocas[30] = define_runs(P(30), {0: "{destinacao_laudo}"})
    trocas[32] = um_texto(P(32), "{#procedimento}IP {procedimento}{/procedimento}")
    trocas[34] = um_texto(P(34), "{#boletim_ocorrencia}BO {boletim_ocorrencia}{/boletim_ocorrencia}")
    # o espaço em branco que empurrava o HISTÓRICO vira quebra de página: a folha de rosto fica estável
    for n in range(36, 44):
        assert not RE_T.sub("", P(n)).count("w:sectPr") and not "".join(RE_T.findall(P(n))).strip(), n
        trocas[n] = ""
    trocas[44] = quebra_antes(P(44))
    trocas[45] = um_texto(P(45), "{texto_historico}")
    trocas[47] = um_texto(P(47), "Foram encaminhados para esta gerência acondicionado(s) em envelope de segurança lacrado {lacre_entrada}, os seguintes objetos: ")
    trocas[48] = define_runs(P(48), {2: " 01 (um) celular na(s) cor(es) {cor}, marca {marca}, modelo {modelo}{texto_capa}. O objeto apresentava "
                                        "o(s) seguinte(s) número(s) de IMEI: {imei_1}{#imei_2} e {imei_2}{/imei_2}{frase_itens}",
                                     3: "", 4: "", 5: "", 6: ""})
    trocas[49] = marcador("{#sims}") + define_runs(P(49), {2: "Objeto {identificador_objeto}", 3: ": um cartão SIM da operadora {operadora}, com número de série ICCID {iccid}{fim}"}) + marcador("{/sims}")
    trocas[52] = um_texto(P(52), "{titulo_objetos}")
    trocas[53] = um_texto(P(53), "{texto_exames}")
    trocas[58] = um_texto(P(58), "{hash_algoritmo}")
    trocas[59] = um_texto(P(59), "{hash_arquivo}")
    trocas[60] = um_texto(P(60), "{valor_hash}")
    trocas[61] = define_runs(P(61), {2: " {hash_algoritmo}, quando aplicada sobre o arquivo “{hash_arquivo}”"})
    trocas[62] = marcador("{#tem_quesitos}") + P(62) + marcador("{#quesitos}")
    # a figura com o quesito do caso de origem sai; o parágrafo do quesito usa a formatação da resposta
    n64 = len(RE_T.findall(P(64)))
    trocas[63] = um_texto(P(64), "{numero_quesito}) {enunciado}")
    trocas[64] = define_runs(P(64), {i: ("Resposta" if i == 0 else ": {resposta}" if i == 1 else "") for i in range(n64)}) + marcador("{/quesitos}") + marcador("{/tem_quesitos}")
    trocas[66] = um_texto(P(66), "{texto_consideracoes}")
    trocas[67] = ""
    trocas[68] = um_texto(P(68), "Cuiabá, {data_extenso}.")
    trocas[72] = um_texto(P(72), "{nome_perito}")
    for n in range(74, 80):  # linhas em branco finais e a nota digitada (que passa para o texto padrão da resposta)
        trocas[n] = ""

    saida, pos = [], 0
    for n, m in enumerate(ps):
        if n in trocas:
            saida += [xml[pos:m.start()], trocas[n]]
            pos = m.end()
    return com_linha_autoridade("".join(saida) + xml[pos:])


def com_linha_autoridade(xml):
    """A autoridade vira a primeira linha da tabela da folha de rosto, no formato das demais."""
    m = re.search(r"<w:tr[ >].*?</w:tr>", xml[xml.index("<w:tbl>"):], re.S)
    ini = xml.index("<w:tbl>") + m.start()
    linha = m.group(0).replace("Solicitação inicial:", "Autoridade Solicitante:").replace("Requisição de Perícia {numero_requisicao}", "{autoridade_solicitante}")
    assert "{autoridade_solicitante}" in linha
    return xml[:ini] + linha + xml[ini:]


def cabecalho(xml):
    """No cabeçalho, o número do laudo vem de um marcador só."""
    textos = RE_T.findall(xml)
    i = next(n for n, t in enumerate(textos) if t.startswith("nº 214"))
    p = next(m for m in RE_P.finditer(xml) if "nº 214" in m.group(0))
    base = sum(len(RE_T.findall(q.group(0))) for q in RE_P.finditer(xml) if q.end() <= p.start())
    novo = define_runs(p.group(0), {i - base: "nº {numero_laudo}", i - base + 1: "", i - base + 2: ""})
    return xml[:p.start()] + novo + xml[p.end():]


def main():
    z = zipfile.ZipFile(ORIGEM)
    saida = {}
    for info in z.infolist():
        nome, dado = info.filename, z.read(info.filename)
        if nome == "word/media/image2.jpg":  # recorte com o quesito do caso de origem
            continue
        if nome == "word/document.xml":
            dado = corpo(dado.decode("utf-8")).encode("utf-8")
        elif nome in ("word/header1.xml", "word/header2.xml"):
            dado = cabecalho(dado.decode("utf-8")).encode("utf-8")
        elif nome == "word/_rels/document.xml.rels":
            dado = re.sub(r'<Relationship [^>]*Target="media/image2\.jpg"[^>]*/>', "", dado.decode("utf-8")).encode("utf-8")
        elif nome == "[Content_Types].xml":
            dado = dado.replace(b"wordprocessingml.template.main+xml", b"wordprocessingml.document.main+xml")
        elif nome == "docProps/core.xml":
            t = dado.decode("utf-8")
            t = re.sub(r"<dc:creator>[^<]*</dc:creator>", "<dc:creator>POLITEC/MT</dc:creator>", t)
            t = re.sub(r"<cp:lastModifiedBy>[^<]*</cp:lastModifiedBy>", "<cp:lastModifiedBy>POLITEC/MT</cp:lastModifiedBy>", t)
            dado = t.encode("utf-8")
        saida[nome] = dado
    with zipfile.ZipFile(SAIDA, "w", zipfile.ZIP_DEFLATED) as w:
        for nome, dado in saida.items():
            w.writestr(nome, dado)
    # conferência: nenhum dado do caso de origem sobrou em nenhuma parte de texto
    achados = []
    for nome, dado in saida.items():
        if nome.endswith((".xml", ".rels")):
            texto = "".join(RE_T.findall(dado.decode("utf-8"))) if nome.startswith("word/") and nome.endswith(".xml") else dado.decode("utf-8")
            achados += [f"{nome}: {p}" for p in PROIBIDOS if p in texto]
    if achados:
        raise SystemExit("Sobrou dado do caso de origem: " + "; ".join(achados))
    JSON_SAIDA.write_text(json.dumps({"nome": SAIDA.name, "b64": base64.b64encode(SAIDA.read_bytes()).decode("ascii")}), encoding="utf-8")
    print(SAIDA.name, SAIDA.stat().st_size, "bytes; nenhum dado do caso de origem")


if __name__ == "__main__":
    main()
