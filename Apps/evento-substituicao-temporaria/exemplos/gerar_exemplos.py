"""Gera os 15 eventos fictícios do Evento de Substituição Temporária.

As datas são relativas a hoje, para que o prazo do dia 05 (RN06) e a fila de
cada perfil fiquem sempre com casos no prazo e casos atrasados. A semente é
fixa; os nomes, unidades e processos são fictícios.

Uso: python "Apps/evento-substituicao-temporaria/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261109)
HOJE = dt.date.today()


def add_mes(d, n):
    m = d.month - 1 + n
    return dt.date(d.year + m // 12, m % 12 + 1, 1)


MES = HOJE.replace(day=1)
MES1 = add_mes(MES, 1)

UNIDADES = [
    {"id_unidade": "U-GAB", "nome": "Gabinete de Direção", "sigla": "GAB",
     "chefia": "Chefe de Gabinete Fictício", "diretor": "Diretor de Gabinete Fictício"},
    {"id_unidade": "U-DLF", "nome": "Diretoria de Laboratório Forense", "sigla": "DLF",
     "chefia": "Chefia do Laboratório Fictícia", "diretor": "Diretor do Laboratório Fictício"},
    {"id_unidade": "U-DI", "nome": "Diretoria de Interiorização", "sigla": "DI",
     "chefia": "Chefia de Interiorização Fictícia", "diretor": "Diretor de Interiorização Fictício"},
    {"id_unidade": "U-IC", "nome": "Identificação Civil", "sigla": "IC",
     "chefia": "Chefia de Identificação Fictícia", "diretor": "Diretor de Identificação Fictício"},
    {"id_unidade": "U-CORR", "nome": "Corregedoria", "sigla": "CORR",
     "chefia": "Corregedor Fictício", "diretor": "Corregedor Adjunto Fictício"},
    {"id_unidade": "U-CQUAL", "nome": "Coordenadoria de Qualidade", "sigla": "CQUAL",
     "chefia": "Coordenador de Qualidade Fictício", "diretor": "Diretor de Qualidade Fictício"},
]
for u in UNIDADES:
    u["niveis"] = [
        {"nivel": 1, "gestor": u["chefia"], "cargo": "Chefia imediata"},
        {"nivel": 2, "gestor": u["diretor"], "cargo": "Direção da unidade"},
    ]

MOTIVOS = ["Férias", "Licença Prêmio", "Licença para tratamento da própria saúde",
           "Licença para acompanhar pessoa da família"]
CARGOS = ["Diretor", "Coordenador", "Chefe de Divisão", "Gerente", "Chefe de Núcleo"]

# status, mês do período (0 = atual, 1 = seguinte), dia inicial, dias de duração, unidade
PLANILHA = [
    ("autorizacao", 1, 10, 14, 0),
    ("autorizacao", 1, 3, 14, 1),
    ("devolvido", 1, 1, 9, 3),
    ("gabinete", 1, 8, 14, 0),
    ("gabinete", 1, 12, 12, 5),
    ("analise_rh", 1, 12, 14, 4),
    ("analise_rh", 1, 15, 14, 1),
    ("aguardando_assinatura", 1, 9, 14, 2),
    ("aguardando_assinatura", 1, 5, 14, 3),
    ("assinado", 1, 7, 14, 0),
    ("assinado", -1, 15, 14, 5),
    ("encaminhado_sesp", 1, 3, 14, 4),
    ("encaminhado_sesp", 0, 20, 10, 1),
    ("publicado", 0, 1, 14, 0),
    ("indeferido", 0, 10, 14, 2),
]

AVANCO = ["autorizacao", "gabinete", "analise_rh", "aguardando_assinatura",
          "assinado", "encaminhado_sesp", "publicado"]
ORDEM = {s: i for i, s in enumerate(AVANCO)}
ORDEM["devolvido"] = 0
ORDEM["indeferido"] = 9


def dias_antes(data, n):
    return data - dt.timedelta(days=n)


def main():
    eventos, autorizacoes, fichas, publicacoes, log = [], [], [], [], []
    for i, (status, mes, dia, duracao, iu) in enumerate(PLANILHA, start=1):
        eid = f"EST-{i:04d}"
        base = {0: MES, 1: MES1, -1: add_mes(MES, -1)}[mes]
        inicio = base.replace(day=dia)
        fim = inicio + dt.timedelta(days=duracao - 1)
        oficio = min(dias_antes(inicio, 10), dias_antes(HOJE, 2))
        u = UNIDADES[iu]
        substituido = f"Gestor Fictício {chr(64 + i)}"
        substituto = f"Substituto Fictício {chr(64 + i)}"
        evento = {
            "id_evento": eid,
            "numero_sigadoc": f"2026.{i:04d}-SIGADOC",
            "data_oficio": oficio.isoformat(),
            "unidade": u["id_unidade"],
            "unidade_nome": u["nome"],
            "motivo": MOTIVOS[(i - 1) % len(MOTIVOS)],
            "substituido": substituido,
            "cargo_substituido": CARGOS[(i - 1) % len(CARGOS)],
            "substituto": substituto,
            "cargo_substituto": CARGOS[i % len(CARGOS)],
            "periodo_inicio": inicio.isoformat(),
            "periodo_fim": fim.isoformat(),
            "observacao": "",
            "status": status,
            "criado_em": oficio.isoformat() + "T09:00:00",
        }
        ordem = ORDEM[status]
        if ordem >= ORDEM["assinado"]:
            evento.update({"assinado_por": "Diretor Geral Adjunto Fictício",
                           "assinado_cargo": "Diretor Geral Adjunto",
                           "assinado_em": (oficio + dt.timedelta(days=5)).isoformat()})
        if status == "encaminhado_sesp":
            if mes == 1:
                evento["envio_sesp_em"] = (HOJE - dt.timedelta(days=2)).isoformat()
            else:
                evento["envio_sesp_em"] = min(MES.replace(day=4), HOJE).isoformat()
        if status == "publicado":
            evento["envio_sesp_em"] = (MES - dt.timedelta(days=3)).isoformat()
            evento["publicacao_numero"] = "DO-2026-0001"
            evento["publicacao_do"] = (HOJE - dt.timedelta(days=1)).isoformat()
            evento["encerrado_em"] = evento["publicacao_do"]
            publicacoes.append({"id": f"PUB-{i:04d}", "evento_id": eid, "numero_do": "DO-2026-0001",
                                "data_publicacao": evento["publicacao_do"],
                                "criado_em": evento["publicacao_do"] + "T10:00:00"})
        if status == "indeferido":
            evento["indeferido_motivo"] = "Enviado depois do dia 05 (RN06)"
            evento["indeferido_em"] = (HOJE - dt.timedelta(days=1)).isoformat()
        eventos.append(evento)

        for nv in u["niveis"]:
            situacao, data = "pendente", None
            if ordem >= ORDEM["gabinete"]:
                situacao = "autorizado"
                data = (oficio + dt.timedelta(days=nv["nivel"])).isoformat()
            elif status == "devolvido" and nv["nivel"] == 1:
                situacao, data = "devolvido", (oficio + dt.timedelta(days=1)).isoformat()
            elif status == "autorizacao" and nv["nivel"] == 1 and i % 2 == 1:
                situacao, data = "autorizado", (oficio + dt.timedelta(days=1)).isoformat()
            autorizacoes.append({"id": f"AUT-{eid}-{nv['nivel']}", "evento_id": eid, "nivel": nv["nivel"],
                                 "gestor": nv["gestor"], "cargo": nv["cargo"],
                                 "situacao": situacao, "data": data, "perfil": "hierarquia"})

        if ordem >= ORDEM["aguardando_assinatura"]:
            fichas.append({"id": f"FIC-{i:04d}", "evento_id": eid, "numero_ficha": f"FS-{i:04d}",
                           "data": (oficio + dt.timedelta(days=3)).isoformat(),
                           "analista": "Analista de RH Fictício",
                           "observacao": "Ficha de solicitação de substituição temporária anexada ao processo.",
                           "criado_em": (oficio + dt.timedelta(days=3)).isoformat() + "T11:00:00"})

        def reg(tipo, descricao, data):
            log.append({"id": f"LOG-{eid}-{len(log):03d}", "evento_id": eid, "tipo_evento": tipo,
                        "descricao": descricao, "perfil": "sistema",
                        "data_hora": data.isoformat() + "T09:00:00"})

        reg("ofício registrado", f"{evento['numero_sigadoc']} · {substituido} → {substituto} · {evento['motivo']}", oficio)
        reg("enviado para autorização", "2 níveis na linha hierárquica", oficio)
        if status == "devolvido":
            reg("devolvido à unidade", "Chefia imediata devolveu o evento para ajuste", oficio + dt.timedelta(days=1))
        if ordem >= ORDEM["gabinete"]:
            reg("enviado ao Gabinete", "todas as autorizações da linha hierárquica foram concedidas", oficio + dt.timedelta(days=2))
        if ordem >= ORDEM["analise_rh"]:
            reg("encaminhado ao RH", "Gabinete de Direção → Gerência de Suporte à Gestão de Pessoas", oficio + dt.timedelta(days=3))
        if ordem >= ORDEM["aguardando_assinatura"]:
            reg("ficha de solicitação incluída", f"FS-{i:04d} · Analista de RH Fictício", oficio + dt.timedelta(days=3))
            reg("enviado para assinatura", "Diretor Geral Adjunto", oficio + dt.timedelta(days=4))
        if ordem >= ORDEM["assinado"]:
            reg("assinatura registrada", "Diretor Geral Adjunto Fictício · Diretor Geral Adjunto", oficio + dt.timedelta(days=5))
        if status in ("encaminhado_sesp", "publicado"):
            reg("encaminhado à SESP", "enviado dentro do prazo do dia 05", dt.date.fromisoformat(evento["envio_sesp_em"]))
        if status == "publicado":
            reg("publicação no Diário Oficial", f"DO-2026-0001 · {evento['publicacao_do']}", dt.date.fromisoformat(evento["publicacao_do"]))
            reg("evento encerrado", "encerrado com a publicação no Diário Oficial (RN07)", dt.date.fromisoformat(evento["publicacao_do"]))
        if status == "indeferido":
            reg("evento indeferido", evento["indeferido_motivo"], dt.date.fromisoformat(evento["indeferido_em"]))

    seed = {"eventos": eventos, "autorizacoes": autorizacoes, "fichas": fichas,
            "publicacoes": publicacoes, "unidades": UNIDADES, "log": log}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
