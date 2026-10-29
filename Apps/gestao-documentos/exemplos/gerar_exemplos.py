"""Gera os 12 processos fictícios da Gestão de Documentos (Sprint 0), com semente fixa.

Cobre os três sinais do prazo (verde, amarelo e vermelho), dois concluídos e as
três situações de exceção do envio: anexo faltante, redistribuição e prazo
suspenso (representado por prazo maior).

Uso: python "Apps/gestao-documentos/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)

ASSUNTOS = ["Pedido de informações da Corregedoria", "Ofício da Delegacia de Cuiabá", "Requisição de cópia de laudo",
            "Solicitação de diligência externa", "Encaminhamento do Ministério Público", "Pedido de prorrogação de prazo",
            "Reclamação de atendimento", "Requisição de perícia complementar", "Ofício da Secretaria de Segurança",
            "Pedido de vista de processo", "Convite para reunião técnica", "Solicitação de dados estatísticos"]
LOTACOES = ["Gabinete de Direção", "Corregedoria", "Diretoria de Laboratório Forense", "Diretoria de Interiorização", "Identificação Civil"]
USUARIOS = [
    ("U1", "Servidor Fictício A", "servidor"),
    ("U2", "Servidor Fictício B", "servidor"),
    ("U3", "Chefia Fictícia", "gestor"),
    ("U4", "Autoridade Fictícia", "autoridade"),
]
ANEXOS = ["Requerimento", "Documento de identificação", "Anexos obrigatórios"]


def main():
    hoje = dt.date(2026, 10, 29)
    # dias decorridos com prazo 15: 3 (20%), 12 (80%), 18 (120%), 16 (107%), 6 (40%), ...
    decorridos = [3, 5, 12, 8, 18, 16, 2, 11, 14, 4, 9, 20]
    status = ["em andamento"] * 9 + ["concluido", "concluido", "em andamento"]
    processos, documentos, log = [], [], []
    for n, dias in enumerate(decorridos):
        data = hoje - dt.timedelta(days=dias)
        pid = f"PR-{n + 1:04d}"
        numero = f"{data.year}.{n + 1:04d}-SD"
        requerente = f"Requerente Fictício {chr(65 + n)}"
        pessoal = USUARIOS[n % len(USUARIOS)]
        anexos = list(ANEXOS) if n != 4 else ANEXOS[:2]     # exceção: anexo faltante
        processos.append({"id_processo": pid, "numero_processo": numero, "assunto": ASSUNTOS[n], "requerente": requerente,
                          "lotacao": LOTACOES[n % len(LOTACOES)], "data_autuacao": data.isoformat(),
                          "dias_prazo": 15 if n != 7 else 30, "responsavel": pessoal[0], "anexos": anexos,
                          "status": status[n], "criado_em": data.isoformat() + "T09:00:00"})
        for i, a in enumerate(anexos):
            documentos.append({"id_documento": f"{pid}-D{i + 1}", "processo_id": pid, "tipo_documento": a,
                               "data_criacao": data.isoformat() + "T09:05:00", "assinado": status[n] == "concluido"})
        log.append({"id": f"L-{pid}", "processo_id": pid, "tipo_evento": "autuação", "descricao": f"{numero} · {ASSUNTOS[n]}",
                    "perfil": pessoal[2], "data_hora": data.isoformat() + "T09:00:00"})
    seed = {"processos": processos, "documentos": documentos, "usuarios": [{"id_usuario": i, "nome": nome, "perfil": perfil} for i, nome, perfil in USUARIOS], "log": log}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
