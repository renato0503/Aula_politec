"""Gera exemplos/painel-pbi-2026-10.pdf: um painel do Power BI impresso (fictício),
com duas tabelas lado a lado, como o PDF que a CQUAL baixa do navegador.

- à esquerda, a "Matriz de Duração de Pendentes por Unidade": a diretoria (DMLF)
  como subtotal e as coordenadorias recuadas abaixo, com o nome quebrado em duas linhas;
- à direita, uma "Relação de Pendentes" com protocolo e tempo, sem linha Total;
- embaixo, a "Distribuição de Protocolos por Unidade e Servidor", com Total.

Os nomes de servidores são fictícios. Uso: python exemplos/gerar_painel_ficticio.py
"""
import pathlib
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

SAIDA = pathlib.Path(__file__).resolve().parent / "painel-pbi-2026-10.pdf"
c = canvas.Canvas(str(SAIDA), pagesize=A4)
W, H = A4
y0 = H - 60
c.setFont("Helvetica-Bold", 9); c.drawString(40, y0, "PAINEL DE PRODUTIVIDADE PERICIAL")
c.setFont("Helvetica", 6); c.drawString(40, y0 - 10, "Impresso em 14/10/2026, 08:59")
# KPIs (números soltos, sem Total)
for i, (r, v) in enumerate([("Protocolos Registrados", "85.529"), ("Finalizados", "83.415"), ("Pendentes", "1.972")]):
    c.setFont("Helvetica", 5); c.drawString(40 + i * 90, y0 - 30, r); c.setFont("Helvetica-Bold", 8); c.drawString(40 + i * 90, y0 - 40, v)

# matriz (esquerda)
y = y0 - 80
c.setFont("Helvetica-Bold", 7); c.drawString(40, y, "Matriz de Duração de Pendentes por Unidade")
cols = [150, 185, 220, 255, 290, 330, 360]
rot = ["1. Até 10 Dias", "2. Até 30 Dias", "3. Até 60 Dias", "4. Até 180 Dias", "5. Até 365 Dias", "6. Mais de 1 ano", "Total"]
y -= 14; c.setFont("Helvetica", 4.5); c.drawString(40, y, "DIRETORIA")
for x, t in zip(cols, rot): c.drawRightString(x, y, t)
linhas = [(42, ["DMLF"], ["45", "84", "76", "368", "393", "1.006", "1.972"]),
          (50, ["PERÍCIAS EM LABORATÓRIOS", "DE MATERIAIS"], ["45", "84", "75", "364", "393", "931", "1.892"]),
          (50, ["Outro"], ["", "", "1", "4", "", "72", "77"]),
          (50, ["PERÍCIAS EM BIOLOGIA", "MOLECULAR"], ["", "", "", "", "", "3", "3"])]
for x, nome, vals in linhas:
    y -= 10
    for k, parte in enumerate(nome): c.drawString(x, y - k * 6, parte)
    for xc, v in zip(cols, vals):
        if v: c.drawRightString(xc, y, v)
    y -= 6 * (len(nome) - 1)
y -= 10; c.setFont("Helvetica-Bold", 4.5); c.drawString(40, y, "Total")
for xc, v in zip(cols, ["45", "84", "76", "368", "393", "1.006", "1.972"]): c.drawRightString(xc, y, v)

# relação de pendentes (direita, mesma altura da matriz)
y = y0 - 80; c.setFont("Helvetica-Bold", 7); c.drawString(400, y, "Relação de Pendentes")
c.setFont("Helvetica", 4.5); y -= 14
c.drawString(400, y, "Servidor"); c.drawString(480, y, "Protocolo"); c.drawRightString(550, y, "Tempo")
for nome, prot, t in [("SERVIDOR FICTÍCIO A", "448/2013", "4953"), ("SERVIDOR FICTÍCIO B", "2878/2013", "4847"),
                      ("SERVIDOR FICTÍCIO C", "3337/2013", "4830"), ("SERVIDOR FICTÍCIO D", "3341/2013", "4830")]:
    y -= 10; c.drawString(400, y, nome); c.drawString(480, y, prot); c.drawRightString(550, y, t)

# distribuição (embaixo)
y = y0 - 230; c.setFont("Helvetica-Bold", 7); c.drawString(40, y, "Distribuição de Protocolos por Unidade e Servidor")
c.setFont("Helvetica", 4.5); y -= 14
c.drawString(40, y, "Unidade"); c.drawString(170, y, "Servidor")
for x, t in [(300, "Registrados"), (340, "Pendentes"), (380, "Finalizados")]: c.drawRightString(x, y, t)
for srv, a, b, d in [("SERVIDORA FICTÍCIA E", "105", "2", "103"), ("SERVIDOR FICTÍCIO F", "2", "2", ""),
                     ("SERVIDORA FICTÍCIA G", "1", "1", ""), ("SERVIDOR FICTÍCIO H", "8", "", "8")]:
    y -= 9; c.drawString(40, y, "COORDENADORIA DE LABORATÓRIO DE MATERIAIS"); c.drawString(170, y, srv)
    for x, v in [(300, a), (340, b), (380, d)]:
        if v: c.drawRightString(x, y, v)
y -= 9; c.setFont("Helvetica-Bold", 4.5); c.drawString(40, y, "Total")
for x, v in [(300, "116"), (340, "5"), (380, "111")]: c.drawRightString(x, y, v)
c.showPage(); c.save()
print(SAIDA)
