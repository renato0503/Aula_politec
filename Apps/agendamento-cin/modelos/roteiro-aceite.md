# Roteiro de aceite e piloto de 4 semanas (fictício)

> **Premissa assumida em 30/10/2026.** O piloto não foi executado e a TI não
> respondeu. O que depende do Google (trava de vaga, e-mail e retenção diária)
> está como **a implementar**, com o passo a passo no botão escondido do app
> (três cliques no nome do app, no rodapé).
> Ver [PREMISSAS.md](../../PREMISSAS.md) e [DEPLOY.md](../DEPLOY.md).

## 1. Roteiro de aceite

| # | Passo | O que tem que acontecer |
|---|---|---|
| 1 | O cidadão agenda pelo celular | posto, dia e horário escolhidos, dados, aviso de privacidade, comprovante com protocolo |
| 2 | O cidadão consulta e cancela | com protocolo + telefone, o cancelamento até 2 h antes devolve a vaga (RN07) |
| 3 | O posto vê a reserva | em `#/posto`, agenda do dia e da semana, com busca por nome ou protocolo |
| 4 | O posto marca comparecimento e ausência | a situação muda e vai para a fila de envio (RN08) |
| 5 | Duas pessoas na última vaga | só uma reserva é gravada (RN04, trava no Apps Script) |
| 6 | A gestão vê os indicadores | ocupação, comparecimento, cancelamento e retenção em `#/gestao` |
| 7 | O cidadão tenta o segundo agendamento no mesmo posto | recusado por telefone ou CPF (RN06) |

**Critério de aceite**: nenhuma etapa gera erro no console; a vaga volta ao
calendário no cancelamento; o segundo agendamento do mesmo telefone é recusado.

## 2. O que falta implementar (depende do Google)

| Item | Onde | Como |
|---|---|---|
| Trava de vaga (`LockService`) | `Code.gs`, função `reservar` | `getScriptLock()` + `waitLock(10000)` + `releaseLock()` no `finally` |
| E-mail de confirmação e cancelamento (`MailApp`) | `Code.gs`, função `enviarPendentes` | lê a aba `fila` com estado `pendente` e envia |
| Retenção diária de 90 dias (RN10) | `Code.gs`, função `retencao` + acionador | acionador diário entre 2 h e 3 h |
| Publicação | `clasp` + implantação como app da Web | ver `DEPLOY.md` |

O app local já faz a parte de tela: enfileira os e-mails em `fila`, relê a
capacidade antes de gravar e apaga os registros antigos pelo botão de retenção.

## 3. Piloto de 4 semanas

| Medida | Meta |
|---|---|
| Ocupação das vagas | 70% |
| Comparecimento | 85% |
| Tempo de uma marcação | 4 minutos (premissa) |
| Agendamentos por dia | 1.200 no posto (premissa) |

## 4. Antes do piloto

1. Autorização da TI para a conta institucional e as cotas de execução e e-mail.
2. Confirmar as regras RN06 a RN10 com a gestão.
3. Decidir se o piloto usa só dados fictícios (recomendado) ou dados reais.
