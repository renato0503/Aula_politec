"""Gera a planilha modelo do Agendamento CIN (Sprint 0), com dados fictícios.

Saídas (nesta pasta), uma por aba da planilha Google:
  postos.csv  horarios.csv  agendamentos.csv  usuarios.csv  log.csv
  seed.json   as mesmas abas, usadas pelo modo local do index.html (sem Apps Script)

2 postos, horários de 3 semanas úteis (08h às 16h, de 30 em 30 min, 2 vagas),
com a semana passada, a corrente e a seguinte,
30 agendamentos (confirmados, cancelados, compareceu, ausente), 3 usuários.
As datas são relativas a hoje: a grade cobre a semana passada, a corrente e a
seguinte, para
o painel do posto nunca envelhecer.
Para importar no Google Planilhas: Arquivo > Importar > Enviar, uma aba por CSV.

Semente fixa = 20261029.
Uso: python "Apps/agendamento-cin/planilha-modelo/gerar_planilha.py"
"""
import csv
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)
HOJE = dt.date.today()
INICIO = HOJE - dt.timedelta(days=HOJE.weekday() + 7)  # segunda-feira da semana passada

POSTOS = [
    {"posto_id": "P01", "nome": "Posto de Identificação Centro (fictício)", "municipio": "Cuiabá", "endereco": "Rua Fictícia, 100",
     "email": "posto.centro@exemplo.gov.br", "ativo": True,
     "documentos_orientacao": "Certidão de nascimento ou casamento original; CPF; comprovante de residência."},
    {"posto_id": "P02", "nome": "Posto de Identificação Várzea Grande (fictício)", "municipio": "Várzea Grande", "endereco": "Avenida Fictícia, 200",
     "email": "posto.vg@exemplo.gov.br", "ativo": True,
     "documentos_orientacao": "Certidão de nascimento ou casamento original; CPF; comprovante de residência."},
]
USUARIOS = [
    {"usuario_id": "U01", "email": "servidor.centro@politec.mt.gov.br", "perfil": "posto", "posto_id": "P01", "ativo": True},
    {"usuario_id": "U02", "email": "servidor.vg@politec.mt.gov.br", "perfil": "posto", "posto_id": "P02", "ativo": True},
    {"usuario_id": "U03", "email": "gestao.identificacao@politec.mt.gov.br", "perfil": "gestao", "posto_id": "", "ativo": True},
]
NOMES = ["Ana Souza", "Bruno Lima", "Carla Dias", "Davi Rocha", "Elaine Paz", "Felipe Reis", "Gisele Mota", "Hugo Pires",
         "Iara Costa", "Jonas Melo", "Katia Ramos", "Leo Vieira", "Mara Nunes", "Nilo Prado", "Otávio Luz"]


def main():
    horarios = []
    for p in POSTOS:
        for d in range(21):
            dia = INICIO + dt.timedelta(days=d)
            if dia.weekday() >= 5:
                continue
            for k in range(16):
                hora = f"{8 + k // 2:02d}:{30 * (k % 2):02d}"
                horarios.append({"horario_id": f"{p['posto_id']}-{dia.isoformat()}-{hora.replace(':', '')}", "posto_id": p["posto_id"],
                                 "data": dia.isoformat(), "hora": hora, "capacidade": 2, "ocupadas": 0, "situacao": "aberto"})
    agendamentos = []
    # garante o fluxo visível na agenda de cada posto: hoje tem agendamentos confirmados
    forcados = []
    for p in POSTOS:
        doDia = [x for x in horarios if x["posto_id"] == p["posto_id"] and x["data"] == HOJE.isoformat() and x["ocupadas"] < x["capacidade"]]
        random.shuffle(doDia)
        forcados.extend(doDia[:2])
    for n, h in enumerate(forcados):
        h["ocupadas"] += 1
        nome = random.choice(NOMES)
        agendamentos.append({
            "protocolo": f"CIN-{100000 + n * 7919 % 900000:06d}", "posto_id": h["posto_id"], "horario_id": h["horario_id"], "nome": nome,
            "telefone": f"(65) 9{random.randint(8000, 9999)}-{random.randint(1000, 9999)}",
            "email": (nome.split()[0].lower().replace("á", "a") + "@exemplo.com") if n % 3 else "",
            "cpf_final4": f"{random.randint(0, 9999):04d}" if n % 2 else "", "status": "confirmado",
            "criado_em": (dt.datetime.combine(HOJE - dt.timedelta(days=6), dt.time(9)) + dt.timedelta(hours=n * 3)).isoformat() + "-04:00",
            "cancelado_em": "", "compareceu_em": ""})
    for n in range(len(forcados), 30):
        h = random.choice([x for x in horarios if x["ocupadas"] < x["capacidade"]])
        h["ocupadas"] += 1
        atras = h["data"] < HOJE.isoformat()
        possiveis = ["compareceu", "ausente", "cancelado"] if atras else ["confirmado", "cancelado"]
        status = random.choice(possiveis)
        if status == "cancelado":
            h["ocupadas"] -= 1
        criado = dt.datetime.combine(HOJE - dt.timedelta(days=6), dt.time(9)) + dt.timedelta(hours=n * 3)
        nome = random.choice(NOMES)
        agendamentos.append({
            "protocolo": f"CIN-{100000 + n * 7919 % 900000:06d}", "posto_id": h["posto_id"], "horario_id": h["horario_id"], "nome": nome,
            "telefone": f"(65) 9{random.randint(8000, 9999)}-{random.randint(1000, 9999)}",
            "email": (nome.split()[0].lower().replace("á", "a") + "@exemplo.com") if n % 3 else "",
            "cpf_final4": f"{random.randint(0, 9999):04d}" if n % 2 else "", "status": status,
            "criado_em": criado.isoformat() + "-04:00",
            "cancelado_em": (criado + dt.timedelta(days=1)).isoformat() + "-04:00" if status == "cancelado" else "",
            "compareceu_em": f"{h['data']}T{h['hora']}:00-04:00" if status == "compareceu" else ""})
    abas = {"postos": POSTOS, "horarios": horarios, "agendamentos": agendamentos, "usuarios": USUARIOS, "log": []}
    cab_log = ["id", "data_hora", "usuario", "acao", "protocolo", "detalhe"]
    for nome, linhas in abas.items():
        cab = list(linhas[0].keys()) if linhas else cab_log
        with open(AQUI / f"{nome}.csv", "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=cab)
            w.writeheader()
            w.writerows(linhas)
    (AQUI / "seed.json").write_text(json.dumps(abas, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in abas.items()})


if __name__ == "__main__":
    main()
