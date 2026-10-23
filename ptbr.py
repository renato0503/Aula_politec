# -*- coding: utf-8 -*-
"""Acentuação e ajustes de texto em pt-BR para os cadernos da Aula 6.

O conteudo do gerador e escrito sem acentos. Esta etapa aplica a ortografia
pt-BR nos nós de texto do HTML, sem alterar código, tags, atributos ou blocos
de Mermaid/DAX/SQL.

Uso:
    import ptbr
    ptbr.acentuar_arquivo("Aula 6/caderno-dia6.html")
"""
import json
import pathlib
import re

from bs4 import BeautifulSoup

RAIZ = pathlib.Path(__file__).resolve().parent
_DICT_PATH = RAIZ / "ptbr_dict.json"
_DICT = {}


def _carregar():
    global _DICT
    if not _DICT:
        _DICT = {k.lower(): v for k, v in json.loads(
            _DICT_PATH.read_text(encoding="utf-8")).items()}
    return _DICT


def _match_case(orig, novo):
    if orig.isupper():
        return novo.upper()
    if orig[:1].isupper():
        return novo[:1].upper() + novo[1:]
    return novo


def acentuar_texto(texto):
    d = _carregar()

    def repl(m):
        w = m.group(0)
        low = w.lower()
        if low in d:
            return _match_case(w, d[low])
        return w

    texto = re.sub(r"[A-Za-zÀ-ÿ]+", repl, texto)
    texto = texto.replace(" — ", ", ").replace(" – ", ", ")
    texto = texto.replace("—", ", ").replace("–", ", ")
    return texto


def _ignorar(el):
    proibidos = {"code", "pre", "script", "style", "kbd", "samp", "svg", "textarea"}
    if el.parent is None:
        return True
    if el.parent.name in proibidos:
        return True
    for pai in el.parents:
        if pai.name in proibidos:
            return True
        classes = pai.get("class") or []
        if "f" in classes or pai.get("data-lang"):
            return True
    return False


def acentuar_html(html):
    soup = BeautifulSoup(html, "lxml")
    for el in soup.find_all(string=True):
        if _ignorar(el):
            continue
        t = str(el)
        if not re.search(r"[A-Za-zÀ-ÿ]", t):
            continue
        novo = acentuar_texto(t)
        if novo != t:
            el.replace_with(novo)
    return str(soup)


def acentuar_arquivo(caminho):
    p = pathlib.Path(caminho)
    html = p.read_text(encoding="utf-8")
    p.write_text(acentuar_html(html), encoding="utf-8")
