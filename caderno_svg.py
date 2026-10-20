# -*- coding: utf-8 -*-
"""Biblioteca de SVG do caderno POLITEC/MT.

Reune os **icones da notacao BPMN 2.0** (desenhados com a geometria oficial),
um conjunto de **ilustracoes** (galeria de simbolos, anatomia de swimlane,
comparacao espera x execucao) e um **construtor de diagramas** que desenha
processos completos em SVG puro.

Nao ha dependencia externa: os SVGs sao <svg> inline, herdam as cores do tema
(`var(--ink)`, `var(--accent)`, `var(--verde)`, `var(--vermelho)`...) e por isso
funcionam no tema claro, no escuro e na impressao.

Uso (num gerador de caderno):

    import pathlib, sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
    from caderno_lib import Caderno, p, tbl
    from caderno_svg import icon, gallery, swimlane_anatomy, gates_anatomy,
                           wait_vs_touch, build_process_asis, build_process_tobe

    cad.section("bpmn-galeria", "Os simbolos do BPMN 2.0",
        p("Cada elemento tem um simbolo padronizado.") + gallery())
"""
import itertools

_uid = itertools.count(1)

STROKE = "var(--ink)"
INK = "var(--ink)"
SOFT = "var(--ink-soft)"
FAINT = "var(--ink-faint)"
SURF = "var(--surface)"

TONES = {
    "n": (STROKE, SURF, INK),
    "a": ("var(--accent)", "var(--accent-soft)", "var(--accent)"),
    "g": ("var(--verde)", "var(--verde-soft)", "var(--verde)"),
    "w": ("var(--ambar)", "var(--ambar-soft)", "var(--ambar)"),
    "r": ("var(--vermelho)", "var(--vermelho-soft)", "var(--vermelho)"),
    "p": ("var(--roxo)", "var(--roxo-soft)", "var(--roxo)"),
}


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def lines(text, maxlen=15):
    """Quebra um rotulo em linhas. Use '|' para quebra forcada."""
    if "|" in str(text):
        return [x.strip() for x in str(text).split("|") if x.strip()]
    out, cur = [], ""
    for w in str(text).split():
        cand = (cur + " " + w).strip()
        if len(cand) > maxlen and cur:
            out.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        out.append(cur)
    return out


# =================================================================
# ICONES BPMN (geometria oficial)
# =================================================================
def _svg(body, size=34, vb=44, cls="ic-svg", extra=""):
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 {vb} {vb}" '
            f'fill="none" xmlns="http://www.w3.org/2000/svg" '
            f'style="flex:none;vertical-align:middle" {extra}>{body}</svg>')


def icon(name, size=34):
    """Retorna um <svg> inline com o simbolo BPMN (ou icone de navegacao)."""
    s = STROKE
    b = {
        # --- Eventos ---
        "start": f'<circle cx="22" cy="22" r="12" fill="{SURF}" stroke="{s}" stroke-width="2.4"/>',
        "end": f'<circle cx="22" cy="22" r="12" fill="{s}"/>',
        "end-error": (f'<circle cx="22" cy="22" r="12" fill="{s}"/>'
                      f'<path d="M22 12 L30.5 27.5 H13.5 Z" fill="{SURF}"/>'
                      f'<circle cx="22" cy="23.5" r="1.7" fill="{s}"/>'
                      f'<rect x="21.2" y="25.2" width="1.6" height="4" rx="0.8" fill="{s}"/>'),
        "end-cancel": (f'<circle cx="22" cy="22" r="12" fill="{s}"/>'
                       f'<path d="M16 16 L28 28 M28 16 L16 28" stroke="{SURF}" stroke-width="2.6"/>'),
        "intermediate": (f'<circle cx="22" cy="22" r="12" fill="{SURF}" stroke="{s}" stroke-width="2.2"/>'
                         f'<circle cx="22" cy="22" r="7.4" fill="none" stroke="{s}" stroke-width="2"/>'),
        "intermediate-msg": (f'<circle cx="22" cy="22" r="12" fill="{SURF}" stroke="{s}" stroke-width="2.2"/>'
                             f'<circle cx="22" cy="22" r="7.4" fill="none" stroke="{s}" stroke-width="1.8"/>'
                             f'<rect x="16.2" y="19.4" width="11.6" height="7" rx="1" fill="none" stroke="{s}" stroke-width="1.6"/>'
                             f'<path d="M16.2 19.4 L22 23.4 L27.8 19.4" fill="none" stroke="{s}" stroke-width="1.6"/>'),
        "intermediate-timer": (f'<circle cx="22" cy="22" r="12" fill="{SURF}" stroke="{s}" stroke-width="2.2"/>'
                               f'<circle cx="22" cy="22" r="7.4" fill="none" stroke="{s}" stroke-width="1.8"/>'
                               f'<circle cx="22" cy="22" r="4.6" fill="none" stroke="{s}" stroke-width="1.6"/>'
                               f'<path d="M22 19.4 V22 L24 23.4" stroke="{s}" stroke-width="1.6"/>'),
        "intermediate-signal": (f'<circle cx="22" cy="22" r="12" fill="{SURF}" stroke="{s}" stroke-width="2.2"/>'
                                f'<circle cx="22" cy="22" r="7.4" fill="none" stroke="{s}" stroke-width="1.8"/>'
                                f'<path d="M22 15.4 L28 26 H16 Z" fill="{s}"/>'),
        "intermediate-condition": (f'<circle cx="22" cy="22" r="12" fill="{SURF}" stroke="{s}" stroke-width="2.2"/>'
                                   f'<circle cx="22" cy="22" r="7.4" fill="none" stroke="{s}" stroke-width="1.8"/>'
                                   f'<path d="M16 25 L22 19 L28 25" fill="none" stroke="{s}" stroke-width="1.8"/>'),
        "boundary": (f'<circle cx="22" cy="26" r="10" fill="{SURF}" stroke="{s}" '
                     f'stroke-width="2.2" stroke-dasharray="3.4 2.6"/>'),
        "boundary-msg": (f'<circle cx="22" cy="26" r="10" fill="{SURF}" stroke="{s}" '
                         f'stroke-width="2.2" stroke-dasharray="3.4 2.6"/>'
                         f'<rect x="17" y="23.6" width="10" height="5.4" rx="1" fill="none" stroke="{s}" stroke-width="1.4"/>'
                         f'<path d="M17 23.6 L22 27 L27 23.6" fill="none" stroke="{s}" stroke-width="1.4"/>'),
        "boundary-timer": (f'<circle cx="22" cy="26" r="10" fill="{SURF}" stroke="{s}" '
                           f'stroke-width="2.2" stroke-dasharray="3.4 2.6"/>'
                           f'<circle cx="22" cy="26" r="4.2" fill="none" stroke="{s}" stroke-width="1.5"/>'
                           f'<path d="M22 23.6 V26 L23.8 27.2" stroke="{s}" stroke-width="1.5"/>'),

        # --- Atividades ---
        "task": (f'<rect x="5" y="11" width="34" height="22" rx="4" fill="{SURF}" '
                 f'stroke="{s}" stroke-width="2.4"/>'),
        "task-user": (f'<rect x="5" y="11" width="34" height="22" rx="4" fill="{SURF}" stroke="{s}" stroke-width="2.4"/>'
                      f'<circle cx="16" cy="19" r="3.1" fill="none" stroke="{s}" stroke-width="1.6"/>'
                      f'<path d="M10.5 28 C10.5 24.4 13 23 16 23 C19 23 21.5 24.4 21.5 28" '
                      f'fill="none" stroke="{s}" stroke-width="1.6"/>'
                      f'<path d="M25 18.5 H34 M25 24.5 H34" stroke="{s}" stroke-width="1.6"/>'),
        "task-script": (f'<rect x="5" y="11" width="34" height="22" rx="4" fill="var(--verde-soft)" '
                        f'stroke="var(--verde)" stroke-width="2.4"/>'
                        f'<path d="M13 17 L11.5 22 L16 22 L14.5 27" stroke="var(--verde)" '
                        f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
                        f'<path d="M21 27 L28 17" stroke="var(--verde)" stroke-width="1.6" stroke-dasharray="2 2"/>'),
        "subprocess": (f'<rect x="5" y="11" width="34" height="22" rx="4" fill="{SURF}" stroke="{s}" stroke-width="2.4"/>'
                       f'<rect x="9.5" y="15.5" width="25" height="13" rx="2" fill="none" '
                       f'stroke="{s}" stroke-width="1.6"/>'
                       f'<path d="M22 18.6 L25.4 22 L22 25.4 L18.6 22 Z" fill="{s}"/>'),
        "call-activity": (f'<rect x="5" y="11" width="34" height="22" rx="4" fill="{SURF}" '
                          f'stroke="{s}" stroke-width="2.4"/>'
                          f'<rect x="5" y="11" width="7" height="22" rx="3" fill="{s}"/>'),
        "group": (f'<rect x="4" y="10" width="36" height="24" rx="9" fill="none" '
                  f'stroke="{s}" stroke-width="2.2"/>'),

        # --- Gateways ---
        "gateway-exclusive": (f'<path d="M22 6 L38 22 L22 38 L6 22 Z" fill="{SURF}" stroke="{s}" stroke-width="2.3"/>'
                              f'<path d="M17 17 L27 27 M27 17 L17 27" stroke="{s}" stroke-width="2.1"/>'),
        "gateway-parallel": (f'<path d="M22 6 L38 22 L22 38 L6 22 Z" fill="{SURF}" stroke="{s}" stroke-width="2.3"/>'
                             f'<path d="M16 22 H28 M22 16 V28" stroke="{s}" stroke-width="2.4"/>'),
        "gateway-inclusive": (f'<path d="M22 6 L38 22 L22 38 L6 22 Z" fill="{SURF}" stroke="{s}" stroke-width="2.3"/>'
                              f'<circle cx="22" cy="22" r="5.2" fill="none" stroke="{s}" stroke-width="2.1"/>'),
        "gateway-event": (f'<path d="M22 6 L38 22 L22 38 L6 22 Z" fill="{SURF}" stroke="{s}" stroke-width="2.3"/>'
                          f'<path d="M22 13 L29 17.5 L29 26.5 L22 31 L15 26.5 L15 17.5 Z" '
                          f'fill="none" stroke="{s}" stroke-width="1.7"/>'
                          f'<circle cx="22" cy="22" r="2.2" fill="{s}"/>'),
        "gateway-complex": (f'<path d="M22 6 L38 22 L22 38 L6 22 Z" fill="{SURF}" stroke="{s}" stroke-width="2.3"/>'
                            f'<path d="M16 22 H28 M22 16 V28" stroke="{s}" stroke-width="2"/>'
                            f'<path d="M14.5 14.5 L29.5 29.5" stroke="{s}" stroke-width="1.6"/>'),

        # --- Estrutura e objetos ---
        "pool": (f'<rect x="3" y="8" width="38" height="28" rx="2" fill="none" stroke="{s}" stroke-width="2.2"/>'
                 f'<rect x="3" y="8" width="11" height="28" fill="var(--raised)" stroke="{s}" stroke-width="2.2"/>'),
        "lane": (f'<rect x="3" y="8" width="38" height="28" rx="2" fill="none" stroke="{s}" stroke-width="2.2"/>'
                 f'<path d="M3 20 H41" stroke="{s}" stroke-width="2"/>'
                 f'<path d="M3 32 H41" stroke="{s}" stroke-width="1.4" stroke-dasharray="0"/>'),
        "message": (f'<rect x="4" y="13" width="36" height="19" rx="2" fill="{SURF}" stroke="{s}" stroke-width="2.2"/>'
                    f'<path d="M4 14 L22 26 L40 14" fill="none" stroke="{s}" stroke-width="2"/>'),
        "data-object": (f'<path d="M7 10 H27 L37 20 V34 H7 Z" fill="{SURF}" stroke="{s}" stroke-width="2.2"/>'
                        f'<path d="M27 10 V20 H37" fill="none" stroke="{s}" stroke-width="2.2"/>'),
        "data-store": (f'<ellipse cx="22" cy="12" rx="13" ry="4.6" fill="{SURF}" stroke="{s}" stroke-width="2.1"/>'
                       f'<path d="M9 12 V32 C9 34.6 15 36.6 22 36.6 C29 36.6 35 34.6 35 32 V12" '
                       f'fill="{SURF}" stroke="{s}" stroke-width="2.1"/>'),
        "annotation": (f'<rect x="6" y="12" width="32" height="20" rx="2" fill="none" '
                       f'stroke="{s}" stroke-width="2.1"/>'
                       f'<path d="M12 12 V32" stroke="{s}" stroke-width="3"/>'),

        # --- Fluxos ---
        "sequence-flow": (f'<path d="M6 22 H32" stroke="{s}" stroke-width="2.2"/>'
                          f'<path d="M30 16 L38 22 L30 28" fill="none" stroke="{s}" '
                          f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'),
        "message-flow": (f'<path d="M6 22 H32" stroke="{s}" stroke-width="2.1" stroke-dasharray="6 4"/>'
                         f'<path d="M30 16 L38 22 L30 28" fill="none" stroke="{s}" '
                         f'stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/>'),
        "association": (f'<path d="M6 22 H34" stroke="{s}" stroke-width="1.9" stroke-dasharray="2.5 3"/>'),

        # --- Icones de navegacao (Partes do caderno) ---
        "project": (f'<rect x="6" y="9" width="32" height="27" rx="3" fill="none" stroke="{s}" stroke-width="2.2"/>'
                    f'<rect x="13" y="6" width="18" height="6" rx="2" fill="{s}"/>'
                    f'<path d="M14 23 L20 29 L31 17" fill="none" stroke="{s}" stroke-width="2.6" '
                    f'stroke-linecap="round" stroke-linejoin="round"/>'),
        "book": (f'<path d="M22 12 C18 9 12 9 7 10 V34 C12 33 18 33 22 36 C26 33 32 33 37 34 V10 '
                 f'C32 9 26 9 22 12 Z" fill="none" stroke="{s}" stroke-width="2.2" stroke-linejoin="round"/>'
                 f'<path d="M22 12 V36" stroke="{s}" stroke-width="2"/>'),
        "search": (f'<circle cx="19" cy="19" r="11" fill="none" stroke="{s}" stroke-width="2.4"/>'
                   f'<path d="M27 27 L36 36" stroke="{s}" stroke-width="3" stroke-linecap="round"/>'),
        "gear": (f'<circle cx="22" cy="22" r="7" fill="none" stroke="{s}" stroke-width="2.4"/>'
                 f'<path d="M22 6 V11 M22 33 V38 M6 22 H11 M33 22 H38 M11 11 L14.8 14.8 '
                 f'M29.2 29.2 L33 33 M33 11 L29.2 14.8 M14.8 29.2 L11 33" '
                 f'stroke="{s}" stroke-width="2.6" stroke-linecap="round"/>'),
        "rocket": (f'<path d="M22 6 C28 12 31 19 30 27 L25 30 H19 L14 27 C13 19 16 12 22 6 Z" '
                   f'fill="none" stroke="{s}" stroke-width="2.2" stroke-linejoin="round"/>'
                   f'<circle cx="22" cy="17" r="4" fill="none" stroke="{s}" stroke-width="2"/>'
                   f'<path d="M15 30 L12 36 L18 33 M29 30 L32 36 L26 33" fill="none" '
                   f'stroke="{s}" stroke-width="2"/>'),
        "lab": (f'<path d="M17 7 H27 M19 7 V17 L11 33 C10 35 11 36 13 36 H31 C33 36 34 35 33 33 '
                f'L25 17 V7" fill="none" stroke="{s}" stroke-width="2.2" stroke-linejoin="round"/>'
                f'<path d="M14 27 H30" stroke="{s}" stroke-width="2"/>'),
        "map": (f'<path d="M7 11 L17 8 L27 12 L37 9 V33 L27 36 L17 32 L7 35 Z" fill="none" '
                f'stroke="{s}" stroke-width="2.2" stroke-linejoin="round"/>'
                f'<path d="M17 8 V32 M27 12 V36" stroke="{s}" stroke-width="1.8"/>'),
        "money": (f'<rect x="5" y="11" width="34" height="22" rx="3" fill="none" stroke="{s}" stroke-width="2.2"/>'
                  f'<circle cx="22" cy="22" r="6" fill="none" stroke="{s}" stroke-width="2"/>'
                  f'<path d="M11 17 H12 M32 27 H33" stroke="{s}" stroke-width="2.4"/>'),
        "chain": (f'<rect x="5" y="16" width="17" height="12" rx="6" fill="none" stroke="{s}" stroke-width="2.3"/>'
                  f'<rect x="22" y="16" width="17" height="12" rx="6" fill="none" stroke="{s}" stroke-width="2.3"/>'
                  f'<path d="M17 22 H27" stroke="{s}" stroke-width="2.3"/>'),
        "check": (f'<circle cx="22" cy="22" r="15" fill="none" stroke="{s}" stroke-width="2.4"/>'
                  f'<path d="M14 22 L20 28 L31 16" fill="none" stroke="{s}" stroke-width="2.8" '
                  f'stroke-linecap="round" stroke-linejoin="round"/>'),
        "alert": (f'<path d="M22 7 L39 35 H5 Z" fill="none" stroke="{s}" stroke-width="2.3" '
                  f'stroke-linejoin="round"/>'
                  f'<rect x="21" y="17" width="2" height="9" rx="1" fill="{s}"/>'
                  f'<circle cx="22" cy="30" r="1.5" fill="{s}"/>'),
        "chart": (f'<path d="M6 8 V36 H39" fill="none" stroke="{s}" stroke-width="2.2" stroke-linecap="round"/>'
                  f'<rect x="11" y="24" width="6" height="9" fill="{s}"/>'
                  f'<rect x="20" y="17" width="6" height="16" fill="{s}"/>'
                  f'<rect x="29" y="12" width="6" height="21" fill="var(--vermelho)"/>'),
    }.get(name)
    if b is None:
        b = f'<circle cx="22" cy="22" r="13" fill="none" stroke="{s}" stroke-width="2.4"/>'
    return _svg(b, size=size)


def icon_row(items, size=40):
    """Linha horizontal de icones com legenda."""
    cells = []
    for name, label in items:
        cells.append(
            f'<div style="text-align:center;padding:10px 6px;border:1px solid var(--border);'
            f'border-radius:10px;background:var(--raised);min-width:96px">'
            f'{icon(name, size)}<div style="font-family:Archivo,sans-serif;font-size:11.5px;'
            f'margin-top:6px;color:var(--ink-soft);line-height:1.25">{label}</div></div>')
    return ('<div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center;'
            f'margin:16px 0">{"".join(cells)}</div>')


# =================================================================
# CONSTRUTOR DE DIAGRAMAS
# =================================================================
class Dia:
    """Acumula o corpo de um diagrama SVG e emite marcadores sob demanda."""

    def __init__(self, w, h, title=""):
        self.w, self.h, self.title = w, h, title
        self.parts = []
        self._arrows = {}
        self.uid = next(_uid)

    def add(self, s):
        self.parts.append(s)

    def _arrow(self, tone, open=False, dash=False):
        key = (tone, open, dash)
        if key in self._arrows:
            return f"a{self._arrows[key]}"
        i = len(self._arrows)
        self._arrows[key] = i
        col = TONES[tone][0]
        shape = ("<path d='M0,0 L9,4 L0,8 Z' fill='none' stroke='%s' stroke-width='1.9' "
                 "stroke-linecap='round' stroke-linejoin='round'/>" % col) if open else \
                ("<path d='M0,0 L9,4 L0,8 Z' fill='%s'/>" % col)
        return f"a{i}"

    def _defs(self):
        out = []
        for (tone, open, dash), i in self._arrows.items():
            col = TONES[tone][0]
            shape = ("<path d='M0,0 L9,4 L0,8 Z' fill='none' stroke='%s' stroke-width='1.9' "
                     "stroke-linecap='round' stroke-linejoin='round'/>" % col) if open else \
                    ("<path d='M0,0 L9,4 L0,8 Z' fill='%s'/>" % col)
            dashattr = ' stroke-dasharray="7 4"' if dash else ""
            out.append(f'<marker id="ar{self.uid}_{i}" viewBox="0 0 10 8" refX="9" refY="4" '
                       f'markerWidth="7" markerHeight="6" orient="auto">{shape}</marker>')
        return "<defs>" + "".join(out) + "</defs>"

    # -- primitivas -------------------------------------------------
    def text(self, x, y, s, size=12, weight=600, anchor="middle", fill=INK, opacity=None):
        op = f' opacity="{opacity}"' if opacity is not None else ""
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
                 f'text-anchor="{anchor}" fill="{fill}"{op}>{esc(s)}</text>')

    def label(self, x, y, s, size=11, fill=SOFT, maxlen=15, weight=600):
        ls = lines(s, maxlen)
        top = y - (len(ls) - 1) * size * 0.62
        for i, t in enumerate(ls):
            self.text(x, top + i * size * 1.24, t, size=size, weight=weight, fill=fill)
        return top + (len(ls) - 1) * size * 1.24

    def lane(self, x, y, w, h, title, sub="", tone="n", head=132):
        col = TONES[tone][0]
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{SURF}" '
                 f'stroke="var(--border)" stroke-width="1.4"/>')
        self.add(f'<rect x="{x}" y="{y}" width="{head}" height="{h}" fill="var(--raised)" '
                 f'stroke="var(--border)" stroke-width="1.4"/>')
        self.add(f'<rect x="{x + 4}" y="{y + 4}" width="4" height="{h - 8}" fill="{col}"/>')
        cy = y + h / 2
        if sub:
            self.label(x + head / 2, cy - 4, title, size=12, fill=INK, maxlen=12)
            lim = int(head / 5.0)
            s = sub if len(sub) <= lim else sub[:lim - 1].rstrip() + "..."
            self.text(x + head / 2, cy + 14, s, size=9.5, weight=500, fill=FAINT)
        else:
            self.label(x + head / 2, cy + 4, title, size=12, fill=INK, maxlen=12)

    def start(self, cx, cy, tone="n", r=15):
        col = TONES[tone][0]
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SURF}" stroke="{col}" stroke-width="2.6"/>')

    def end(self, cx, cy, tone="n", r=15):
        col = TONES[tone][0]
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" stroke="{col}" stroke-width="2"/>')

    def end_error(self, cx, cy, r=15):
        col = "var(--vermelho)"
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/>')
        self.add(f'<path d="M{cx} {cy-9} L{cx+7.8} {cy+5.5} L{cx-7.8} {cy+5.5} Z" fill="{SURF}"/>')
        self.add(f'<circle cx="{cx}" cy="{cy-3.5}" r="1.6" fill="{col}"/>')
        self.add(f'<rect x="{cx-0.8}" cy="{cy-1.6}" width="1.6" height="4" rx="0.8" fill="{col}"/>')

    def task(self, cx, cy, s, w=132, h=56, tone="n", maxlen=14, sub=None, glyph=None):
        col, fill, _ = TONES[tone]
        x, y = cx - w / 2, cy - h / 2
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" '
                 f'stroke="{col}" stroke-width="2.3"/>')
        if glyph == "bot":
            gx, gy = x + 15, y + h / 2
            self.add(f'<path d="M{gx} {gy-9} V{gy-6.4}" stroke="{col}" stroke-width="1.5"/>'
                     f'<circle cx="{gx}" cy="{gy-10.4}" r="1.5" fill="{col}"/>'
                     f'<rect x="{gx-5.2}" y="{gy-6}" width="10.4" height="9.4" rx="2.6" '
                     f'fill="{fill}" stroke="{col}" stroke-width="1.6"/>'
                     f'<circle cx="{gx-2.3}" cy="{gy-1.6}" r="1.1" fill="{col}"/>'
                     f'<circle cx="{gx+2.3}" cy="{gy-1.6}" r="1.1" fill="{col}"/>')
        elif glyph == "human":
            gx, gy = x + 15, y + h / 2
            self.add(f'<circle cx="{gx}" cy="{gy-5.5}" r="3.2" fill="none" stroke="{col}" stroke-width="1.7"/>'
                     f'<path d="M{gx-5.5} {gy+6.5} C{gx-5.5} {gy+1} {gx-3} {gy-0.5} {gx} {gy-0.5} '
                     f'C{gx+3} {gy-0.5} {gx+5.5} {gy+1} {gx+5.5} {gy+6.5}" fill="none" '
                     f'stroke="{col}" stroke-width="1.7"/>')
        ls = lines(s, maxlen)
        base = y + h / 2 - (len(ls) - 1) * 7 + (4 if len(ls) == 1 else 0)
        if sub:
            base -= 7
        for i, t in enumerate(ls):
            self.text(cx, base + i * 14.4, t, size=12, weight=600, fill=INK)
        if sub:
            self.text(cx, y + h - 10, sub, size=9.5, weight=500, fill=TONES[tone][0])
        return (x, y, x + w, y + h)

    def subprocess(self, cx, cy, s, w=140, h=60, tone="n", maxlen=14):
        col, fill, _ = TONES[tone]
        x, y = cx - w / 2, cy - h / 2
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" '
                 f'stroke="{col}" stroke-width="2.5"/>')
        self.add(f'<rect x="{x+5}" y="{y+5}" width="{w-10}" height="{h-10}" rx="3" fill="none" '
                 f'stroke="{col}" stroke-width="1.5"/>')
        self.add(f'<path d="M{cx} {cy-12} L{cx+7} {cy-4} L{cx} {cy+4} L{cx-7} {cy-4} Z" fill="{col}"/>')
        self.label(cx, cy + 16, s, size=11.5, maxlen=maxlen)
        return (x, y, x + w, y + h)

    def _gw(self, cx, cy, kind, size=50, tone="n", s=None, maxlen=12):
        col, fill, _ = TONES[tone]
        h = size / 2
        self.add(f'<path d="M{cx} {cy-h} L{cx+h} {cy} L{cx} {cy+h} L{cx-h} {cy} Z" '
                 f'fill="{fill}" stroke="{col}" stroke-width="2.4"/>')
        if kind == "x":
            self.add(f'<path d="M{cx-8} {cy-8} L{cx+8} {cy+8} M{cx+8} {cy-8} L{cx-8} {cy+8}" '
                     f'stroke="{col}" stroke-width="2.2"/>')
        elif kind == "+":
            self.add(f'<path d="M{cx-9} {cy} H{cx+9} M{cx} {cy-9} V{cy+9}" stroke="{col}" stroke-width="2.5"/>')
        elif kind == "o":
            self.add(f'<circle cx="{cx}" cy="{cy}" r="6" fill="none" stroke="{col}" stroke-width="2.2"/>')
        if s:
            self.label(cx, cy + h + 18, s, size=10.5, maxlen=maxlen, fill=SOFT)
        return (cx - h, cy - h, cx + h, cy + h)

    def gw_x(self, cx, cy, s=None, tone="n", size=50, maxlen=12):
        return self._gw(cx, cy, "x", size, tone, s, maxlen)

    def gw_plus(self, cx, cy, s=None, tone="n", size=50, maxlen=12):
        return self._gw(cx, cy, "+", size, tone, s, maxlen)

    def gw_or(self, cx, cy, s=None, tone="n", size=50, maxlen=12):
        return self._gw(cx, cy, "o", size, tone, s, maxlen)

    def flow(self, pts, tone="n", dash=False, open_arrow=False, label=None,
             lx=None, ly=None, width=2.2, lsize=10.5):
        d = "M " + " L ".join(f"{x},{y}" for x, y in pts)
        mk = self._arrow(tone, open_arrow, dash)
        da = ' stroke-dasharray="7 4"' if dash else ''
        self.add(f'<path d="{d}" fill="none" stroke="{TONES[tone][0]}" stroke-width="{width}"{da} '
                 f'marker-end="url(#{mk})" stroke-linejoin="round" stroke-linecap="round"/>')
        if label:
            px = lx if lx is not None else pts[0][0]
            py = ly if ly is not None else pts[0][1] - 8
            self.text(px, py, label, size=lsize, weight=700, fill=TONES[tone][0])

    def note(self, x, y, w, s, tone="a", h=None, size=10.5):
        col, fill, _ = TONES[tone]
        ls = lines(s, int(w / 6.4))
        hh = h or (20 + 13 * len(ls))
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="7" fill="{fill}" '
                 f'stroke="{col}" stroke-width="1.5" stroke-dasharray="5 3"/>')
        for i, t in enumerate(ls):
            self.text(x + w / 2, y + 17 + i * 13, t, size=size, weight=600, fill=TONES[tone][0])
        return (x, y, x + w, y + hh)

    def message(self, cx, cy, w=54, h=32, tone="n", s=None):
        col = TONES[tone][0]
        x, y = cx - w / 2, cy - h / 2
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{SURF}" '
                 f'stroke="{col}" stroke-width="2"/>')
        self.add(f'<path d="M{x+2} {y+2} L{cx} {cy+2} L{x+w-2} {y+2}" fill="none" '
                 f'stroke="{col}" stroke-width="1.8"/>')
        if s:
            self.text(cx, y + h + 13, s, size=10, weight=600, fill=SOFT)

    def obj_data(self, cx, cy, s, w=86, h=44, tone="n"):
        col = TONES[tone][0]
        x, y = cx - w / 2, cy - h / 2
        self.add(f'<path d="M{x} {y} H{x+w-13} L{x+w} {y+13} V{y+h} H{x} Z" fill="{SURF}" '
                 f'stroke="{col}" stroke-width="1.9"/>')
        self.add(f'<path d="M{x+w-13} {y} V{y+13} H{x+w}" fill="none" stroke="{col}" stroke-width="1.9"/>')
        self.text(cx, y + h + 14, s, size=10.5, weight=600, fill=SOFT)

    def timer(self, cx, cy, r=13, tone="a"):
        col = TONES[tone][0]
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SURF}" stroke="{col}" '
                 f'stroke-width="2.3" stroke-dasharray="4 2.6"/>')
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r-5}" fill="none" stroke="{col}" stroke-width="1.5"/>')
        self.add(f'<path d="M{cx} {cy-r+6} V{cy} L{cx+3.5} {cy+2.4}" stroke="{col}" stroke-width="1.5"/>')

    def render(self, caption="", sub=""):
        head = (f'<div style="font-family:Archivo,sans-serif;font-weight:700;font-size:13.5px;'
                f'margin:0 0 2px">{esc(self.title)}</div>'
                if self.title else "")
        subs = (f'<div style="font-size:12px;color:var(--ink-faint);margin:0 0 10px">'
                f'{esc(sub)}</div>' if sub else "")
        svg = (f'<svg viewBox="0 0 {self.w} {self.h}" width="100%" '
               f'style="max-width:{self.w}px;height:auto;display:block;margin:0 auto" '
               f'xmlns="http://www.w3.org/2000/svg" font-family="Archivo,system-ui,sans-serif">'
               f'{self._defs()}{"".join(self.parts)}</svg>')
        cap = (f'<figcaption>{esc(caption)}</figcaption>' if caption else "")
        return ('<figure class="svgfig">' + head + subs +
                f'<div class="svgfig-box">{svg}</div>' + cap + '</figure>')


# =================================================================
# ILUSTRACOES PRONTAS
# =================================================================
def gallery():
    """Galeria completa dos simbolos BPMN 2.0."""
    out = ['<h3>Eventos</h3>',
           icon_row([("start", "Inicio"), ("intermediate", "Intermed."),
                     ("intermediate-msg", "Mensagem"), ("intermediate-timer", "Timer"),
                     ("intermediate-signal", "Sinal"), ("intermediate-condition", "Condicao"),
                     ("end", "Fim"), ("end-error", "Fim com erro"), ("end-cancel", "Cancelamento")]),
           '<h3>Atividades</h3>',
           icon_row([("task", "Tarefa"), ("task-user", "Tarefa de usuario"),
                     ("task-script", "Tarefa automatizada"), ("subprocess", "Subprocesso"),
                     ("call-activity", "Atividade chamada"), ("group", "Grupo")]),
           '<h3>Gateways</h3>',
           icon_row([("gateway-exclusive", "Exclusivo (X)"), ("gateway-parallel", "Paralelo (+)"),
                     ("gateway-inclusive", "Inclusivo (O)"), ("gateway-event", "Baseado em evento"),
                     ("gateway-complex", "Complexo")]),
           '<h3>Fluxos, objetos e estrutura</h3>',
           icon_row([("sequence-flow", "Fluxo de sequencia"), ("message-flow", "Fluxo de mensagem"),
                     ("association", "Associacao"), ("message", "Mensagem"),
                     ("data-object", "Objeto de dados"), ("data-store", "Armazenamento"),
                     ("annotation", "Anotacao"), ("boundary-timer", "Evento de fronteira"),
                     ("pool", "Pool"), ("lane", "Lanes")])]
    return "".join(out)


def swimlane_anatomy():
    """Anatomia de um pool com lanes: quem faz o que."""
    d = Dia(880, 388, "Anatomia de pool e swimlanes")
    d.lane(0, 40, 880, 88, "DELEGACIA", "orgao externo")
    d.lane(0, 128, 880, 94, "ATO - Gabinete", "triagem")
    d.lane(0, 222, 880, 94, "LABORATORIO", "perito e revisao")

    d.start(176, 84)
    d.task(286, 84, "Registrar|no SIGT", w=128, glyph="human")
    d.flow([(191, 84), (220, 84)])
    d.flow([(286, 112), (286, 150)])

    d.task(286, 178, "Triagem", w=118, glyph="human")
    d.gw_x(420, 178, "completo?", size=48)
    d.flow([(346, 178), (394, 178)])

    d.task(560, 178, "Fila do perito", w=148, tone="r", glyph="human", sub="gargalo medido")
    d.flow([(446, 178), (484, 178)], label="Sim", lx=466, ly=170)
    d.flow([(420, 154), (420, 138), (268, 138), (268, 150)],
           tone="r", label="Nao", lx=336, ly=133)

    d.task(748, 178, "Analise", w=118, tone="g", glyph="bot", sub="automatizada")
    d.flow([(636, 178), (687, 178)])

    d.task(748, 269, "Revisao|tecnica", w=130, tone="a", sub="segunda opiniao")
    d.flow([(748, 206), (748, 241)])
    d.end(858, 269)
    d.flow([(815, 269), (841, 269)])

    d.note(150, 330, 580, "Cada transicao entre lanes e um ponto de espera potencial - e e por ali "
                          "que nasce o gargalo. Medir a espera em cada fronteira muda o diagnostico.",
           tone="a")
    return d.render("O fluxo atravessa as faixas: cada mudanca de mao (linha) e um ponto onde o caso pode parar.")


def gates_anatomy():
    """Comparacao visual dos tres gateways principais."""
    d = Dia(880, 336, "Os tres gateways que resolvem 90% dos fluxos")
    d.note(40, 12, 800,
           "Gateway errado = diagrama que mente. Paralelo onde so uma rota ocorre inventa uma "
           "simultaneidade que nao existe.", tone="r", h=42)
    cols = [
        ("x", "Exclusivo (X)", "Exatamente UMA rota sai.",
         "Se / senao, validacao, filtro.", "1 de 2 rotas sai",
         [("SIM", "g", True), ("NAO", None, False)]),
        ("+", "Paralelo (+)", "TODAS as rotas saem juntas.",
         "Dividir trabalho em paralelo.", "as 2 rotas saem",
         [("TAREFA A", "g", True), ("TAREFA B", "g", True)]),
        ("o", "Inclusivo (O)", "Uma, varias ou nenhuma.",
         "Condicao mais complexa.", "1, 2 ou nenhuma",
         [("ROTA A", "g", True), ("ROTA B", "g", True), ("...", "w", False)]),
    ]
    for i, (kind, nome, d1, d2, sub, chips) in enumerate(cols):
        x = 160 + i * 280
        d.add(f'<rect x="{x-132}" y="68" width="264" height="252" rx="14" fill="var(--raised)" '
              f'stroke="var(--border)" stroke-width="1.4"/>')
        {"x": d.gw_x, "+": d.gw_plus, "o": d.gw_or}[kind](x, 126, None, size=72)
        d.text(x, 188, nome, size=13, weight=800, fill=INK)
        d.text(x, 210, d1, size=11.5, weight=600, fill=SOFT)
        d.text(x, 228, d2, size=10.5, weight=500, fill=FAINT)
        d.text(x, 258, sub, size=11, weight=700, fill=FAINT)
        cw, cg = 74, 8
        total = len(chips) * cw + (len(chips) - 1) * cg
        bx = x - total / 2
        for lb, tone, on in chips:
            if on:
                col, fill, tc = TONES[tone][0], TONES[tone][1], TONES[tone][0]
                da = ""
            else:
                col, fill, tc = "var(--border)", "var(--surface)", FAINT
                da = ' stroke-dasharray="4 3"'
            d.add(f'<rect x="{bx}" y="272" width="{cw}" height="28" rx="14" fill="{fill}" '
                  f'stroke="{col}" stroke-width="1.5"{da}/>')
            d.text(bx + cw / 2, 290, lb, size=10, weight=700, fill=tc)
            bx += cw + cg
    return d.render(
        "Se so uma rota acontece, use o exclusivo. Paralelo apenas quando as tarefas realmente correm juntas.")


def wait_vs_touch(pct_espera=92, caption="", titulo="Onde o processo realmente gasta o tempo"):
    """Barra mostrando a fatia de espera x execucao."""
    w, h = 880, 218
    d = Dia(w, h, titulo)
    x0, x1, y, bh = 40, 840, 72, 48
    total = 100
    wp = x1 - x0
    wpx = wp * pct_espera / total
    seg = x0 + wpx + (wp - wpx) / 2
    d.text(x0, y - 14, "tempo total do processo", size=10.5, weight=600, fill=FAINT, anchor="start")
    d.add(f'<rect x="{x0}" y="{y}" width="{wp}" height="{bh}" rx="7" fill="var(--raised)" '
          f'stroke="var(--border)" stroke-width="1.4"/>')
    d.add(f'<rect x="{x0}" y="{y}" width="{wpx:.0f}" height="{bh}" fill="var(--accent-soft)" '
          f'stroke="var(--accent)" stroke-width="1.8"/>')
    d.add(f'<rect x="{x0 + wpx:.0f}" y="{y}" width="{wp - wpx:.0f}" height="{bh}" rx="7" '
          f'fill="var(--verde-soft)" stroke="var(--verde)" stroke-width="1.8"/>')
    d.text(x0 + wpx / 2, y + 29, f"ESPERA na fila - {pct_espera}%", size=14, weight=800,
           fill="var(--accent)")
    d.text(seg, y + 29, f"{100 - pct_espera}%", size=12, weight=800, fill="var(--verde)")
    d.text(seg, y - 14, f"TRABALHO - {100 - pct_espera}%", size=10.5, weight=700,
           fill="var(--verde)")
    d.add(f'<path d="M{seg} {y - 8} V{y}" stroke="var(--verde)" stroke-width="1.4" '
          f'stroke-dasharray="2 2"/>')
    for i, (nm, lb) in enumerate([("intermediate-timer", "Caso parado na fila"),
                                  ("task-user", "Alguem trabalhando")]):
        bx = 44 + i * 300
        d.add(f'<g transform="translate({bx},156) scale(1.15)">{icon(nm, 36)}</g>')
        d.text(bx + 52, 180, lb, size=12.5, weight=700, anchor="start", fill=INK)
    d.note(596, 140, 268, "O gargalo quase sempre esta na fatia azul: na fila, nao no trabalho.",
           tone="a")
    return d.render(caption or "Medir execucao sem medir espera e olhar a coisa errada.")


def _inline(name, size, color):
    """Desenha um simbolo BPMN numa posicao, com cor forcada."""
    base = icon(name, size)
    return base


def automation_anatomy():
    """Antes x depois em uma etapa automatizada."""
    d = Dia(880, 312, "Onde entra a intervencao digital no processo")
    d.text(28, 44, "AS-IS - trabalho manual", size=13.5, weight=800, anchor="start",
           fill="var(--vermelho)")
    d.task(110, 100, "Perito confere|a fila", w=140, h=52, glyph="human")
    d.task(285, 100, "Espera na|fila", w=132, h=52, tone="r")
    d.task(460, 100, "Executa a|analise", w=140, h=52, glyph="human")
    d.flow([(182, 100), (218, 100)])
    d.flow([(352, 100), (388, 100)])
    d.timer(250, 126, r=12)
    d.text(300, 160, "44 h parado na fila", size=11.5, weight=700, fill="var(--vermelho)")

    d.text(28, 196, "TO-BE - com intervencao digital", size=13.5, weight=800, anchor="start",
           fill="var(--verde)")
    d.task(110, 240, "Sistema|prioriza", w=140, h=52, tone="g", glyph="bot")
    d.task(285, 240, "Fila por|prazo", w=132, h=52, tone="g", glyph="bot")
    d.task(460, 240, "Executa a|analise", w=140, h=52, tone="g", glyph="bot")
    d.flow([(182, 240), (218, 240)], tone="g")
    d.flow([(352, 240), (388, 240)], tone="g")
    d.timer(250, 266, r=12, tone="g")
    d.text(300, 300, "8 h parado (-82%)", size=11.5, weight=700, fill="var(--verde)")

    d.add(f'<path d="M580 100 V240" stroke="var(--border)" stroke-width="1.6" '
          f'marker-end="url(#{d._arrow("n")})"/>')
    d.text(600, 148, "44 h", size=24, weight=800, anchor="start", fill="var(--vermelho)")
    d.text(600, 178, "8 h", size=24, weight=800, anchor="start", fill="var(--verde)")
    d.text(600, 206, "-82% na espera, com o mesmo perito", size=11.5, weight=600,
           anchor="start", fill=SOFT)
    d.note(560, 226, 296,
           "A regra automatica nao elimina a etapa: muda a ordem e dispara o alerta antes do estrago.",
           tone="g")
    return d.render("A intervencao digital entra exatamente na etapa que o dado apontou como gargalo.")


def method_chain():
    """A cadeia de 6 passos do metodo da aula."""
    d = Dia(880, 200, "O metodo do dia, em seis passos")
    passos = [("1. Descrever", "AS-IS em texto", "annotation"),
              ("2. Diagramar", "BPMN / Mermaid", "task"),
              ("3. Medir", "espera x execucao", "chart"),
              ("4. Redesenhar", "TO-BE", "subprocess"),
              ("5. Automatizar", "intervencao digital", "task-script"),
              ("6. Medir o ganho", "antes x depois", "check")]
    w = 128
    gap = 12
    x = 40
    for i, (t, s, ic) in enumerate(passos):
        col = ["var(--accent)", "var(--accent)", "var(--ambar)",
               "var(--roxo)", "var(--verde)", "var(--verde)"][i]
        fill = ["var(--accent-soft)", "var(--accent-soft)", "var(--ambar-soft)",
                "var(--roxo-soft)", "var(--verde-soft)", "var(--verde-soft)"][i]
        d.add(f'<rect x="{x}" y="46" width="{w}" height="112" rx="10" fill="{fill}" '
              f'stroke="{col}" stroke-width="1.8"/>')
        svg_ic = icon(ic, 36).replace(f'stroke="{STROKE}"', f'stroke="{col}"')
        d.add(f'<g transform="translate({x + w/2 - 18},58)">{svg_ic}</g>')
        d.text(x + w / 2, 124, t, size=12.5, weight=700, fill=INK)
        d.text(x + w / 2, 144, s, size=10, weight=500, fill=col)
        if i < 5:
            d.flow([(x + w + 1, 102), (x + w + gap - 1, 102)], tone="n", width=1.8)
        x += w + gap
    return d.render("Cada passo so funciona bem se o anterior foi feito: sem medir, nao se redesenha.")


# =================================================================
# DIAGRAMAS DE PROCESSO (AS-IS e TO-BE)
# =================================================================
def _pericial_layout(d, tobe=False):
    """Desenha o processo de requisicao pericial (AS-IS ou TO-BE)."""
    W = 980
    L1, L2, L3, L4 = 44, 154, 264, 434
    d.lane(0, L1, W, 110, "DELEGACIA", "orgao requisitante")
    d.lane(0, L2, W, 110, "ATO - Gabinete", "triagem e distribuicao")
    d.lane(0, L3, W, 170, "LABORATORIO", "perito e revisao")
    d.lane(0, L4, W, 88, "SISTEMA", "SIGT e arquivo")

    # --- sw 1: entrada
    d.start(178, L1 + 58)
    d.text(178, L1 + 28, "Req. recebida", size=10, weight=600, fill=SOFT)
    d.task(300, L1 + 58, "Registrar|no SIGT", w=148, sub="manual + sistema", glyph="human")
    d.flow([(193, L1 + 58), (224, L1 + 58)])

    # --- sw 2: triagem + gateway
    d.task(300, L2 + 48, "Triagem e|classificacao", w=148,
           tone=("g" if tobe else "n"), sub=("assistida por tipo" if tobe else "manual"),
           glyph="human")
    d.flow([(300, L1 + 110), (300, L2 + 20)])
    d.gw_x(438, L2 + 48, "Dados completos?", size=46)
    d.flow([(376, L2 + 48), (413, L2 + 48)])
    # laco "nao" dentro da propria faixa
    d.flow([(415, L2 + 60), (398, L2 + 60), (398, L2 + 96), (370, L2 + 96), (370, L2 + 78)],
           tone="r", label="Nao", lx=348, ly=L2 + 92)
    # retorno a delegacia (mensagem)
    d.message(190, L2 + 48, 52, 30)
    d.flow([(218, L2 + 48), (224, L2 + 48)], tone="a", open_arrow=True, width=1.8)
    d.flow([(190, L2 + 32), (190, L2 - 4)], tone="a", open_arrow=True, dash=True, width=1.8)
    d.text(200, L2 - 6, "exige complemento", size=9.5, weight=700, anchor="start",
           fill="var(--accent)")

    # --- sw 3: gargalo, analise, revisao
    if tobe:
        d.task(560, L3 + 40, "Fila priorizada|por prazo", w=150, tone="g",
               sub="regra automatica", glyph="bot")
    else:
        d.task(560, L3 + 40, "Fila do perito", w=150, tone="r",
               sub="ESPERA - gargalo", glyph="human")
    d.flow([(461, L2 + 48), (472, L2 + 48), (472, L3 + 40), (483, L3 + 40)],
           label="Sim", lx=496, ly=L2 + 96)
    d.task(738, L3 + 40, "Analise do|exame", w=132,
           tone=("g" if tobe else "n"), sub=("com checklist" if tobe else "manual"),
           glyph="human")
    d.flow([(637, L3 + 40), (670, L3 + 40)])
    d.gw_x(848, L3 + 40, "Aprovado?", size=44)
    d.flow([(806, L3 + 40), (824, L3 + 40)])

    d.task(848, L3 + 122, "Revisao|tecnica", w=134, tone="a", sub="segunda opiniao")
    d.flow([(848, L3 + 64), (848, L3 + 94)], label="Sim", lx=902, ly=L3 + 86)
    d.flow([(826, L3 + 52), (798, L3 + 78), (738, L3 + 78), (738, L3 + 68)],
           tone="r", label="Nao", lx=884, ly=L3 + 40)

    # --- sw 4: assinatura e arquivo
    d.task(800, L4 + 44, "Assinatura e|arquivamento", w=184, tone="g",
           sub="automatizado", glyph="bot")
    d.flow([(848, L3 + 150), (848, L4 + 16)])
    d.end(925, L4 + 44)
    d.flow([(894, L4 + 44), (908, L4 + 44)])

    if tobe:
        d.timer(560, L3 + 100)
        d.text(576, L3 + 104, "alerta se a fila passar de 24 h", size=10, weight=700,
               anchor="start", fill="var(--ambar)")
        d.note(150, L3 + 112, 330,
               "O gargalo nao desaparece: e reordenado e vigiado. Mesma capacidade, "
               "mesmo perito - espera de 44 h para 8 h.", tone="g")
    else:
        d.note(150, L3 + 112, 330,
               "41,5% de toda a espera do processo esta nesta etapa. Nao e opiniao: "
               "e a soma da coluna tempo_espera_min nos dados.", tone="r")


def build_process_asis():
    d = Dia(980, 540, "Cenario 1 - AS-IS: requisicao pericial")
    _pericial_layout(d, tobe=False)
    return d.render(
        "AS-IS medido nos dados. A etapa em vermelho concentra 41,5% de toda a espera do processo.",
        "4 swimlanes (quem faz) x 8 etapas (o que faz). Destaque em vermelho = gargalo medido.")


def build_process_tobe():
    d = Dia(980, 540, "Cenario 1 - TO-BE: fila priorizada e monitorada")
    _pericial_layout(d, tobe=True)
    return d.render(
        "TO-BE: a etapa que era gargalo vira verde, com fila por prazo e alerta automatico. "
        "O resto do processo nao muda - e o ganho vem inteiro do gargalo.",
        "Intervencao digital aplicada exatamente onde o dado mostrou que o tempo se perde.")


def build_process_orcamento():
    d = Dia(940, 552, "Cenario 2 - AS-IS: empenho e contrato")
    W = 940
    L1, L2, L3, L4 = 44, 144, 248, 368
    d.lane(0, L1, W, 100, "SETOR SOLICITANTE", "pedido em papel")
    d.lane(0, L2, W, 104, "DIVISAO DE COMPRAS", "cotacao e mapa")
    d.lane(0, L3, W, 120, "ASSESSORIA JURIDICA", "parecer")
    d.lane(0, L4, W, 120, "ORDENADOR / SISTEMA", "autorizacao e publicacao")

    # sw 1
    d.start(166, 94)
    d.task(290, 94, "Pedido do setor", w=150, sub="em papel", glyph="human")
    d.flow([(181, 94), (213, 94)])
    d.task(500, 94, "Cotacao no|sistema", w=155, tone="g", sub="automatizado", glyph="bot")
    d.flow([(367, 94), (420, 94)])

    # sw 2
    d.task(500, 196, "Mapa|comparativo", w=150, sub="6 h de trabalho", glyph="human")
    d.flow([(500, 144), (500, 166)])
    d.gw_x(690, 196, "Dotacao suficiente?", size=48)
    d.flow([(577, 196), (664, 196)])
    d.flow([(666, 206), (650, 206), (650, 232), (578, 232), (578, 226)],
           tone="r", label="Nao", lx=628, ly=228)

    # sw 3
    d.task(690, 308, "Parecer|juridico", w=155, tone="r", sub="36 h de espera", glyph="human")
    d.flow([(714, 196), (730, 196), (730, 308), (766, 308)], label="Sim", lx=752, ly=250)
    d.gw_x(830, 308, "Conforme?", size=44)
    d.flow([(770, 308), (806, 308)])

    # sw 4
    d.task(700, 404, "Autorizacao do|ordenador", w=170, tone="r",
           sub="27 h de espera", glyph="human")
    d.flow([(852, 308), (880, 308), (880, 404), (787, 404)], label="Sim", lx=900, ly=356)
    d.task(700, 462, "Empenho e|publicacao", w=175, tone="g", sub="automatizado", glyph="bot")
    d.flow([(700, 438), (700, 434)])
    d.end(845, 462, r=14)
    d.flow([(789, 462), (829, 462)])

    d.note(140, 500, 520,
           "Parecer + Autorizacao = 51,2% de toda a espera do processo. E o retrabalho de 16,6% "
           "vem praticamente inteiro daqui.", tone="r")
    return d.render(
        "Cenario 2: o gargalo e um conjunto - duas aprovacoes encadeadas, e o maior retrabalho dos tres processos.")


def build_process_custodia():
    d = Dia(960, 548, "Cenario 3 - cadeia de custodia")
    W = 960
    L1, L2, L3 = 44, 164, 284
    d.lane(0, L1, W, 120, "CAMPO", "coleta e lacre")
    d.lane(0, L2, W, 120, "TRANSPORTE E CUSTODIA", "registro e deslocamento")
    d.lane(0, L3, W, 190, "LABORATORIO", "recebimento, guarda e pericia")

    # sw 1
    d.start(168, 104)
    d.text(168, 76, "Coleta", size=10, weight=600, fill=SOFT)
    d.task(290, 104, "Coleta no local", w=140, glyph="human")
    d.flow([(183, 104), (218, 104)])
    d.task(490, 104, "Lacre e|acondicionamento", w=160, sub="em papel", glyph="human")
    d.flow([(362, 104), (408, 104)])
    d.task(700, 104, "QR Code + foto|do lacre", w=165, tone="g", sub="TO-BE", glyph="bot")
    d.flow([(572, 104), (616, 104)])

    # sw 2
    d.flow([(700, 164), (700, 196)])
    d.task(330, 224, "Registro da ocorrencia", w=170, tone="g", sub="automatico", glyph="bot")
    d.task(640, 224, "Transporte ao destino", w=170, sub="com rastreio", glyph="human")
    d.flow([(417, 224), (553, 224)])

    # sw 3 - linha 1
    d.flow([(640, 284), (640, 296), (250, 296), (250, 300)])
    d.task(250, 330, "Recebimento e|conferencia", w=150, sub="manual", glyph="human")
    d.gw_x(390, 330, "Lacre confere?", size=46)
    d.flow([(327, 330), (365, 330)])
    d.task(560, 330, "Guarda /|refrigeracao", w=150, tone="r", sub="55 h de espera")
    d.flow([(415, 330), (483, 330)])
    d.task(700, 330, "Pericia", w=110, sub="6 h de trabalho", glyph="human")
    d.flow([(637, 330), (643, 330)])
    d.task(830, 330, "Baixa", w=110, tone="g", sub="assinatura digital", glyph="bot")
    d.flow([(757, 330), (773, 330)])
    d.end(920, 330, r=14)
    d.flow([(887, 330), (904, 330)])

    # sw 3 - linha 2 (intervencoes)
    d.task(250, 428, "BLOQUEIO + alerta|ao responsavel", w=195, tone="r",
           sub="divergencia de lacre", glyph="bot")
    d.flow([(390, 353), (390, 428), (349, 428)], tone="r", label="Nao", lx=436, ly=394)
    d.flow([(560, 358), (560, 428), (592, 428)], tone="a", dash=True)
    d.timer(560, 396)
    d.task(700, 428, "Alerta de guarda vencida", w=210, tone="a", sub="automatico", glyph="bot")

    d.note(140, 486, 660,
           "O gargalo aqui e duplo: tempo de guarda (35,3% da espera) e fragilidade do lacre em papel "
           "(4,8% de divergencia). Por isso o TO-BE ataca os dois.", tone="a")
    return d.render(
        "Cenario 3: um TO-BE so de tempo nao basta. Aqui a intervencao digital protege a validade da prova.")