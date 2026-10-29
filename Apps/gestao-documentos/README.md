# Gestão de Documentos · processos e prazos do Gabinete

Cadastro, atribuição e acompanhamento dos processos do Gabinete de Direção, com o
prazo calculado e o sinal verde, amarelo ou vermelho. A cobrança automática é
simulada no MVP; a decisão e a assinatura continuam com as pessoas.

| Campo | Valor |
|---|---|
| Equipe | Vitória Araújo Dias |
| Contato | vitoriadias@politec.mt.gov.br |
| Unidade | Gabinete de Direção |
| Tipo | Aplicativo para servidor |
| Stack | HTML único (CSS/JS inline), IndexedDB, GitHub Pages |
| Fonte | `Aula 8/Entregas/Vitória Araújo.json` (29/10/2026) |
| GitHub | `Vitoriadias-droide` (Vitória) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado (sem campos vazios; o TO-BE
  está descrito nos campos do formulário).
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.
- `app.json`, `src/app.js`, `exemplos/`, `index.html`.

## Pendências

- Confirmar com a chefia a matriz de papéis (requerente, servidor, analista e
  autoridade) e quem pode excluir documentos.
- O envio e o cronjob reais ficam fora do MVP: na versão de sala, a cobrança é
  registrada na trilha, sem SMTP.
- O TO-BE está descrito só em texto no envio; montar o diagrama em Mermaid no
  Sprint 3.
- A linha de base (1 h/dia, 200 processos/mês, 48 h na triagem) precisa ser
  medida no piloto de 30 dias.
