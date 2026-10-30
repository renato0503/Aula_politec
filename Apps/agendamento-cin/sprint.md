# Agendamento CIN · sprints até o MVP

> Arquitetura: HTML monolítico servido pelo Apps Script, com o painel do posto
> offline first (ver `contexto.md`).
> Cada sprint dura **1 semana** e termina com o app publicado numa conta de
> teste, com dados fictícios.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Parte técnica feita em 29/10/2026 (dados fictícios, bibliotecas, modelos). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026, falta só publicar no Apps Script (precisa da conta institucional). |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py agendamento-cin` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py agendamento-cin` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). `Code.gs` ganhou `listarVagas`, `reservar` e `comprovante`; `node testes/testar_code_gs.js` passa (17/17). A trava contra reserva simultânea fica para o Sprint 4. |
| 4 | Feito em 30/10/2026 a parte do app (RN06, releitura da capacidade e fila de e-mail). A trava (`LockService`), o envio (`MailApp`) e o teste de concorrência ficam para o Apps Script, com o passo a passo no botão escondido do app. |
| 5 | Feito em 30/10/2026. Consulta por protocolo + telefone ou CPF, cancelamento até 2 h (RN07), devolução da vaga e fila do e-mail de cancelamento. |
| 6 | Feito em 30/10/2026. Agenda do dia e da semana, busca, comparecimento e ausência (RN08), agenda no IndexedDB e fila local de envio. |
| 7 | Feito em 30/10/2026. Indicadores por posto, usuários com desativação e retenção de 90 dias pelo botão. O gatilho diário fica para o Apps Script. |
| 8 | Feito em 30/10/2026. Roteiro de aceite em `modelos/roteiro-aceite.md`. O piloto depende da TI e dos postos. |

`Code.gs` com `doGet`, `listarPostos`, `listarHorarios` e `quemSou`, testado contra a planilha modelo. `DEPLOY.md` explica os dois projetos (público e interno). Modo de teste local no `index.html`, sem Apps Script.

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Autorização, regras e dados | TI consultada, regras RN06 a RN10 aprovadas, planilha modelo pronta |
| 1 | Esqueleto | `index.html` servido pelo Apps Script, com as 7 rotas e a planilha ligada |
| 2 | Postos e horários | Gestão cadastra postos; posto cria a grade de horários |
| 3 | Agendamento do cidadão | Calendário com vagas, formulário, protocolo |
| 4 | Trava de vagas e confirmação | Sem reserva duplicada; e-mail de confirmação |
| 5 | Consulta e cancelamento | Cidadão consulta e cancela; vaga volta ao calendário |
| 6 | Painel do posto offline first | Agenda do dia, comparecimento e fila de envio |
| 7 | Painel da gestão, LGPD e acessibilidade | Indicadores, retenção, aviso de privacidade |
| 8 | Aceite e piloto de 4 semanas | Roteiro cumprido e piloto em 1 ou 2 postos |

**MVP 100% pronto = Sprints 0 a 8.**

---

## Sprint 0 · Autorização, regras e dados

- [ ] Pedir à TI a autorização para publicar um app da web do Apps Script com a
      conta institucional e confirmar as cotas de execução e de e-mail. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Aprovar com a gestão as regras completadas: RN06 (um agendamento ativo por
      posto), RN07 (cancelar até 2 h antes), RN08 (tolerância de 15 min), RN09
      (de 1 a 30 dias de antecedência), RN10 (retenção de 90 dias). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Escolher os 1 ou 2 postos do piloto e levantar a grade real (dias, horários, vagas por horário). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [x] Criar a planilha modelo com as 5 abas e dados fictícios: 2 postos, 2
      semanas de horários e 30 agendamentos (confirmados, cancelados, ausentes).
- [ ] Medir a linha de base no posto do piloto: tempo de uma marcação por
      telefone e agendamentos por dia. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Confirmar o nome completo do aluno no formulário. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

**Pronto quando**: a TI respondeu, as regras estão aprovadas e a planilha modelo existe.

## Sprint 1 · Esqueleto

- [ ] Projeto do Apps Script ligado à planilha; `appsscript.json` com fuso `America/Cuiaba`.
- [x] `doGet()` devolve o `index.html` (`HtmlService`), com CSS e JS embutidos.
- [x] Roteador por hash com as 7 rotas do `contexto.md`.
- [x] Funções de leitura no `Code.gs` (`listarPostos`, `listarHorarios`) chamadas por `google.script.run`.
- [x] Identificação do servidor (`Session.getActiveUser()`) comparada à aba `usuarios`.
- [ ] Repositório com `clasp` configurado.

**Pronto quando**: o link publicado abre a tela do cidadão com os postos fictícios,
e um usuário de posto vê o próprio painel.

## Sprint 2 · Postos e horários

- [x] `#/gestao`: cadastrar, ativar e desativar postos (RN01).
- [x] `#/posto/horarios`: criar a grade por dia da semana (horário inicial,
      final, intervalo e vagas), gerar os horários das próximas semanas.
- [x] Bloquear horário ou dia (feriado, falta de servidor).
- [x] O posto só vê e altera os horários dele, conferido no servidor (RN05).

**Pronto quando**: o posto gera 2 semanas de horários, e outro posto não consegue alterá-los.

## Sprint 3 · Agendamento do cidadão

- [x] `#/agendar`: escolher posto, ver os dias com vaga e os horários abertos (RN02, RN09).
- [x] `#/agendar/dados`: nome, telefone ou e-mail, CPF opcional, aviso de privacidade.
- [x] Validação na tela (telefone, e-mail, dígitos do CPF quando informado).
- [x] Gerar protocolo único (RN03) e mostrar o comprovante com os documentos a levar.
- [x] Layout que funciona no celular, que é onde o cidadão vai abrir o link.

**Pronto quando**: um agendamento fictício gera protocolo e aparece na aba `agendamentos`.

## Sprint 4 · Trava de vagas e confirmação

- [ ] `reservar()` com `LockService`: reler a capacidade, gravar e liberar a trava (RN04). **A implementar no Apps Script** — o app local já relê a capacidade antes de gravar; a trava é o passo 1 do botão escondido (3 cliques no nome do app, no rodapé).
- [x] Recusar o segundo agendamento ativo do mesmo telefone ou CPF no posto (RN06).
- [ ] E-mail de confirmação (`MailApp`) com protocolo, posto, data, horário e link de consulta. **A implementar no Apps Script** — o app já enfileira em `fila` com estado `pendente`; o envio é o passo 2 do botão escondido.
- [ ] Teste de concorrência: 5 abas do navegador reservando a última vaga ao mesmo tempo. **Só depois da trava**, no ambiente do Apps Script.

**Pronto quando**: no teste de concorrência, só uma reserva é gravada e as outras
recebem a mensagem de vaga ocupada.

## Sprint 5 · Consulta e cancelamento

- [x] `#/consultar`: protocolo + telefone ou 4 últimos dígitos do CPF.
- [x] Cancelar até 2 h antes (RN07); a vaga volta a aparecer no calendário.
- [ ] E-mail de cancelamento. **A implementar no Apps Script** — já enfileirado em `fila`.
- [x] Remarcar = cancelar e agendar de novo, no mesmo fluxo.

**Pronto quando**: o cancelamento devolve a vaga, e o cancelamento a 1 h do horário é recusado.

## Sprint 6 · Painel do posto offline first

- [x] `#/posto`: agenda do dia e da semana, com busca por nome ou protocolo.
- [x] Marcar comparecimento e ausência (RN08); cancelar pelo posto com motivo.
- [x] Guardar a agenda do dia no IndexedDB ao abrir o painel.
- [x] Sem internet: marcar comparecimento na fila local e enviar quando voltar,
      com aviso de "pendente de envio".
- [x] Toda ação do posto vai para a aba `log`.

**Pronto quando**: com o Wi-Fi desligado, o posto marca 3 comparecimentos, e
eles aparecem na planilha quando a conexão volta.

## Sprint 7 · Painel da gestão, LGPD e acessibilidade

- [x] `#/gestao`: ocupação, comparecimento, cancelamento e antecedência por
      posto e por semana (KPIs do `contexto.md`).
- [x] Cadastro de usuários (posto ou gestão) e desativação.
- [ ] Rotina diária (`trigger`) que apaga os dados do cidadão após 90 dias (RN10) e mantém as contagens. **A implementar no Apps Script** — o botão em `#/gestao` já faz a retenção; o gatilho é o passo 3 do botão escondido.
- [ ] Acessibilidade (requisito marcado): rótulos, navegação por teclado,
      contraste, mensagens de erro lidas por leitor de tela.

**Pronto quando**: os indicadores batem com a contagem manual na planilha
fictícia, e a rotina de retenção apaga os registros antigos.

## Sprint 8 · Aceite e piloto de 4 semanas

- [x] **Roteiro de aceite** com a gestão e um posto:
  1. Cidadão agenda pelo celular e recebe o e-mail.
  2. Cidadão consulta e cancela pelo protocolo.
  3. Posto vê a reserva, marca comparecimento e ausência.
  4. Duas pessoas na última vaga: só uma reserva.
  5. Gestão vê os indicadores da semana.
- [ ] Autorização da TI para dados reais (ou piloto só com fictícios). **Depende da TI** (premissa em `Apps/PREMISSAS.md`).
- [ ] **Piloto de 4 semanas** em 1 ou 2 postos (proposta do aluno). **Depende dos postos.**
- [x] Ao fim, comparar ocupação e comparecimento com as metas (70% e 85%) e
      atualizar `PROJETO.md` e `README.md`.

**Pronto quando**: o roteiro passa e o piloto está aberto.
