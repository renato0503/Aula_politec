"""Gera os dados fictícios das inscrições em cursos (Sprint 0).

Saídas (nesta pasta):
  curso-ficticio.json     um curso com vagas por diretoria
  seap-ficticio.csv       relatório de servidores ativos (UTF-8 com BOM, ;)
  emails-ficticios.txt    60 e-mails de inscrição com o bloco INSCRICAO-v1
                          (50 válidos, 5 reenvios da mesma matrícula, 5 inválidos)
  seed.json               curso + SEAP no formato do app

Formato do bloco (o app lê exatamente isto):
  INSCRICAO-v1:<base64url do JSON>.<fnv1a-32 em hex do base64url>
  JSON: {p: protocolo, c: curso_id, m: matrícula, n: nome, l: lotação,
         d: diretoria, e: e-mail, t: telefone, r: [pré-requisitos declarados], s: enviado_em}

Tudo fictício. Semente fixa = 20261029.
Uso: python "Apps/inscricoes-cursos/exemplos/gerar_exemplos.py"
"""
import base64
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)

DIRETORIAS = [("DMC", "Diretoria Metropolitana de Criminalística"), ("DML", "Diretoria Metropolitana de Medicina Legal"),
              ("DII", "Diretoria de Identificação"), ("DIN", "Diretoria de Interiorização")]
CURSO = {"id": "CURSO-2026-11", "nome": "Fotografia Forense em Local de Crime", "carga_horaria": 24,
         "inicio": "2026-11-23", "fim": "2026-11-25", "local": "Auditório da sede (fictício)",
         "prerequisitos": ["Ser servidor efetivo", "Atuar em local de crime ou em laboratório"],
         "vagas_por_diretoria": {"DMC": 8, "DML": 4, "DII": 2, "DIN": 6}, "link_grupo": "https://chat.whatsapp.com/EXEMPLO-FICTICIO",
         "inscricao_inicio": "2026-10-29", "inscricao_fim": "2026-11-12", "prazo_triagem": "2026-11-16", "status": "inscrições abertas"}
NOMES = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Fábio", "Gabriela", "Heitor", "Isabela", "João", "Karen", "Lucas",
         "Marina", "Nelson", "Olívia", "Paulo", "Queila", "Rafael", "Sílvia", "Tiago", "Úrsula", "Vítor", "Wanda", "Xavier", "Yasmin", "Zeca"]
SOBRENOMES = ["Almeida", "Barros", "Campos", "Duarte", "Esteves", "Freitas", "Gomes", "Holanda", "Igarashi", "Jardim", "Lima", "Moraes", "Nunes", "Prado"]
LOTACOES = {"DMC": ["Núcleo de Local de Crime", "Laboratório de Química"], "DML": ["IML Cuiabá", "IML Várzea Grande"],
            "DII": ["Posto de Identificação Centro"], "DIN": ["Regional de Rondonópolis", "Regional de Sinop", "Regional de Cáceres"]}


def fnv1a(txt):
    h = 0x811C9DC5
    for b in txt.encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"


def bloco(dados):
    b64 = base64.urlsafe_b64encode(json.dumps(dados, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).decode().rstrip("=")
    return f"INSCRICAO-v1:{b64}.{fnv1a(b64)}"


def protocolo(curso, matricula, quando):
    return fnv1a(curso + "|" + matricula + "|" + quando)[:8].upper()


def main():
    servidores = []
    for i in range(70):
        sig = random.choice(DIRETORIAS)[0]
        nome = f"{random.choice(NOMES)} {random.choice(SOBRENOMES)} {random.choice(SOBRENOMES)}"
        servidores.append({"matricula": str(200000 + i * 37), "nome": nome, "cargo": random.choice(["Perito Oficial Criminal", "Técnico em Necropsia", "Papiloscopista", "Médico Legista"]),
                           "lotacao": random.choice(LOTACOES[sig]), "diretoria": sig, "vinculo_ativo": i % 23 != 0})
    linhas = ["﻿matricula;nome;cargo;lotacao;diretoria;vinculo_ativo"] + [
        f"{s['matricula']};{s['nome']};{s['cargo']};{s['lotacao']};{s['diretoria']};{'S' if s['vinculo_ativo'] else 'N'}" for s in servidores]
    (AQUI / "seap-ficticio.csv").write_text("\n".join(linhas) + "\n", encoding="utf-8")

    emails = []
    for n, s in enumerate(servidores[:50]):
        quando = f"2026-10-{29 + n // 30:02d}T{8 + n % 10:02d}:{(n * 7) % 60:02d}:00-04:00".replace("-10-30", "-10-30")
        primeiro = s["nome"].split()[0].lower().replace("á", "a").replace("í", "i").replace("ú", "u").replace("ó", "o").replace("é", "e")
        d = {"p": protocolo(CURSO["id"], s["matricula"], quando), "c": CURSO["id"], "m": s["matricula"], "n": s["nome"],
             "l": s["lotacao"], "d": s["diretoria"], "e": f"{primeiro}.{s['matricula']}@politec.mt.gov.br",
             "t": f"(65) 9{random.randint(8000, 9999)}-{random.randint(1000, 9999)}" if n % 3 else "",
             "r": CURSO["prerequisitos"] if n % 9 else CURSO["prerequisitos"][:1], "s": quando}
        emails.append((d, bloco(d)))
    for n in range(5):  # reenvio da mesma matrícula, mais recente (RN03)
        d = dict(emails[n][0]); d["s"] = "2026-10-31T10:0%d:00-04:00" % n; d["t"] = "(65) 99999-000%d" % n
        d["p"] = protocolo(CURSO["id"], d["m"], d["s"])
        emails.append((d, bloco(d)))
    invalidos = []
    b = emails[10][1]; invalidos.append(b[:-1] + ("0" if b[-1] != "0" else "1"))                     # código alterado
    d = dict(emails[11][0]); d["e"] = "pessoal@gmail.com"; invalidos.append(bloco(d))                # e-mail fora do domínio (RN02)
    d = dict(emails[12][0]); d["m"] = ""; invalidos.append(bloco(d))                                  # sem matrícula (RN01)
    d = dict(emails[13][0]); d["c"] = "CURSO-OUTRO"; invalidos.append(bloco(d))                        # outro curso
    invalidos.append(emails[14][1][:40])                                                               # bloco cortado pelo e-mail
    corpo = []
    for d, blc in emails:
        corpo.append(f"De: {d['e']}\nAssunto: [INSCRICAO] {CURSO['nome']} {d['p']}\n\nSegue minha inscrição.\n\n{blc}\n\n---\n")
    for blc in invalidos:
        corpo.append(f"De: desconhecido\nAssunto: [INSCRICAO] {CURSO['nome']}\n\n{blc}\n\n---\n")
    (AQUI / "emails-ficticios.txt").write_text("\n".join(corpo), encoding="utf-8")
    (AQUI / "curso-ficticio.json").write_text(json.dumps(CURSO, ensure_ascii=False, indent=1), encoding="utf-8")
    seed = {"cursos": [CURSO], "seap": servidores, "diretorias": [{"sigla": s, "nome": n} for s, n in DIRETORIAS]}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print("servidores", len(servidores), "| e-mails", len(emails) + len(invalidos), "(50 válidos, 5 reenvios, 5 inválidos)")


if __name__ == "__main__":
    main()
