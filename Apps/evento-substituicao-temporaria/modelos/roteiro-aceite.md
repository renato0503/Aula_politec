# Roteiro de aceite · Evento de Substituição Temporária

> Use os dados fictícios (`#/config` → Carregar dados fictícios). Cada item tem o
> perfil, o caminho e o resultado esperado. Marque no `sprint.md` quando o setor
> confirmar.

## 1. Abertura (perfil Unidade solicitante)

- [ ] `#/evento/novo` sem preencher: o app recusa e lista os campos.
- [ ] Motivo em branco: o app recusa com a RN01.
- [ ] Substituto igual ao substituído: o app recusa com a RN02.
- [ ] Período com o fim antes do início: o app recusa.
- [ ] Número do SIGADOC repetido: o app recusa.
- [ ] Preenchido corretamente: o evento é registrado, abre a ficha e entra em
      autorização hierárquica.
- [ ] A ficha mostra a trilha das sete etapas e o limite do dia 05.

## 2. Autorização hierárquica (perfil Gestor hierárquico)

- [ ] `#/fila` lista os eventos em autorização.
- [ ] Autorizar o nível 1 mantém o evento em autorização.
- [ ] Autorizar o nível 2 leva o evento ao Gabinete (RN03).
- [ ] Devolver um evento muda a situação para "Devolvido à unidade".
- [ ] O histórico registra cada autorização e a devolução.

## 3. Reenvio (perfil Unidade solicitante)

- [ ] `#/fila` lista o evento devolvido.
- [ ] O formulário de ajuste abre com os dados do evento.
- [ ] Substituto igual ao substituído é recusado (RN02).
- [ ] "Salvar ajuste e reenviar" atualiza os dados e zera as autorizações.
- [ ] "Reenviar sem alterar" volta o evento e zera as autorizações.

## 4. Gabinete (perfil Gabinete de Direção)

- [ ] `#/fila` lista os eventos no Gabinete.
- [ ] "Encaminhar ao RH" muda a situação para "Em análise de RH".
- [ ] O histórico registra o encaminhamento.

## 5. Ficha de RH (perfil Gerência de Suporte à Gestão de Pessoas)

- [ ] `#/fila` lista os eventos em análise.
- [ ] A ficha é incluída com número, data e analista.
- [ ] Com a ficha, o evento segue para "Aguardando assinatura" (RN04).
- [ ] Sem a ficha, o evento não avança.

## 6. Assinatura (perfil Diretor Geral Adjunto)

- [ ] `#/fila` lista os eventos aguardando assinatura.
- [ ] Assinar grava nome, cargo e data (RN05).
- [ ] O evento volta ao RH como "Assinado · aguardando envio à SESP".

## 7. Envio à SESP (perfil Gerência de Suporte à Gestão de Pessoas)

- [ ] Evento assinado com o limite do dia 05 no futuro: o envio é permitido.
- [ ] Evento assinado com o limite do dia 05 vencido: o envio é bloqueado e o
      app pede o indeferimento (RN06).
- [ ] O indeferimento grava o motivo.
- [ ] O envio grava a data em `envio_sesp_em`.

## 8. Publicação e encerramento (perfil Gerência de Suporte à Gestão de Pessoas)

- [ ] `#/fila` lista os eventos encaminhados à SESP.
- [ ] A publicação grava o número e a data do Diário Oficial.
- [ ] O evento só fica "Publicado" com a publicação (RN07).
- [ ] O histórico registra "evento encerrado".

## 9. Planilha de controle

- [ ] `#/planilha` mostra substituído, substituto, motivo, período e publicação no DO.
- [ ] O CSV sai com BOM, ponto e vírgula e as cinco colunas.
- [ ] O `.xlsx` abre no Excel com as abas **Controle** e **Resumo**.
- [ ] A impressão mantém a tabela legível.

## 10. Painel e filas

- [ ] `#/painel` mostra os indicadores e a "Minha fila" do perfil.
- [ ] A fila do diretor tem um cartão por evento aguardando assinatura.
- [ ] A fila do RH reúne análise, envio e publicação.
- [ ] A fila da unidade mostra os devolvidos.
- [ ] No celular (390 px), a página não rola na horizontal e o menu "Telas" abre.

## 11. Sinais de que o aceite terminou

- [ ] Todos os itens acima marcados com o setor.
- [ ] `python testes/testar.py`, `python testes/cenarios.py` e
      `python testes/jornada.py` passando.
- [ ] Linha de base do piloto registrada (volume mensal e tempo por etapa).
