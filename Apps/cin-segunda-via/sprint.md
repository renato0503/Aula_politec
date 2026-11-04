# Segunda via da CIN a distância · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.
> O MVP prova o fluxo com dados fictícios; biometria real fica fora (LGPD, art. 11).

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py cin-segunda-via` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py cin-segunda-via` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py cin-segunda-via` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |
| 4 | Feito em 30/10/2026. `#/protocolo/:id` e a retenção (RN06); código em `src/sprint4.js` e `src/sprint5.js`. |
| 5 | Feito em 30/10/2026. `#/indicadores` e o teste de acessibilidade; cenário em `Apps/_base/cenarios/sprint5.py`. |
| 6 | Feito em 30/10/2026. Roteiro de aceite e posição da TI em `modelos/roteiro-aceite.md`. |
| 7 | Feito em 03/11/2026: fotos das impressões quando o documento foi extraviado, encaminhamento no protocolo/fila, texto do confronto e troca de perfil pelo menu. A integração biométrica segue externa. |

CPF de teste gerados a partir de 000.000.0xx, com dígito válido; sem fotos (o app gera as de teste no Sprint 2).

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Regras, fontes e dados | Regras da segunda via, fontes dos números, 30 pedidos fictícios |
| 1 | Esqueleto | `index.html` com perfis, rotas, IndexedDB e backup |
| 2 | Pedido do cidadão | Elegibilidade, dados, fotos e protocolo |
| 3 | Fila do servidor | Aceitar ou recusar com motivo, resumo para o sistema |
| 4 | Protocolo e retenção | Cidadão vê a situação; apagar após a decisão |
| 5 | Indicadores e acessibilidade | Painel do piloto, celular, leitor de tela |
| 6 | Aceite e piloto | Roteiro com 30 pedidos e posição da TI sobre produção |
| Identidade e usabilidade | Feito em 02/11/2026. Casca de cidadão, fonte arredondada, cantos redondos e KPI em número; caixa de entrada com fila à esquerda e pedido à direita, busca por protocolo, nome ou CPF, espera em horas, atalhos J/K/A/R e “Aceitar e próximo” / “Recusar e próximo”. `python testes/testar.py` e `python testes/cenarios.py` passam. |

**MVP 100% pronto = Sprints 0 a 6.**

---

## Sprint 0 · Regras, fontes e dados

- [ ] Confirmar as regras oficiais da segunda via (quando dispensa nova coleta). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Indicar a fonte dos números (15 dias, 21.000 por mês). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [x] Gerar 30 pedidos fictícios: elegíveis, CIN vencida, mudança de dados, foto ilegível.
- [ ] Fotos de teste geradas (sem pessoas reais). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Conversa com a TI e com a empresa da coleta biométrica sobre a integração (registrar a posição). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

## Sprint 1 · Esqueleto

- [x] `index.html` gerado pela base comum, perfis Servidor e Gestão; `#/pedido` público.
- [x] Backup, dados fictícios e `#/testes`.

**Pronto quando**: `python Apps/_base/testar.py cin-segunda-via` passa.

## Sprint 2 · Pedido do cidadão

- [x] Perguntas de elegibilidade antes do formulário (RN03): não elegível vai para o agendamento-cin.
- [x] Dados com validação de CPF (RN01) e data.
- [x] Fotos de rosto e documento pela câmera do celular, reduzidas para 800 px (RN02).
- [x] Protocolo na tela.

## Sprint 3 · Fila do servidor

- [x] `#/fila`: pedidos por situação e por data.
- [x] Ficha do pedido com as fotos e a elegibilidade.
- [x] Aceitar ou recusar com motivo (RN05), com registro no `log`.
- [x] `#/pedido/:id/resumo`: dados no formato do cadastro, para copiar ou imprimir.

## Sprint 4 · Protocolo e retenção

- [x] `#/protocolo/:id`: situação e motivo.
- [x] Apagar pedido e fotos decididos (RN06), mantendo só as contagens.

## Sprint 5 · Indicadores e acessibilidade

- [x] `#/indicadores`: pedidos, elegíveis, aceitos, recusados por motivo, tempo.
- [x] Teste no celular (tela pequena, câmera) e com leitor de tela.

## Sprint 6 · Aceite e piloto

- [x] Roteiro com os 30 pedidos fictícios, do pedido ao resumo.
- [x] Registrar a posição da TI e do encarregado de dados sobre produção.
- [x] Atualizar `PROJETO.md` e `README.md`.

## Sprint 7 · Correções do feedback (03/11/2026)

> Feedback de André (nota 3).

### Código
- [x] Pedido: quando o documento foi extraviado, pedir as fotos das impressões digitais (não a foto do documento). (4 dedos: polegares e indicadores)
- [x] Anexar e encaminhar as imagens das impressões no protocolo e na fila.
- [x] Melhorar a troca de perfil. O seletor do cabeçalho troca no mesmo lugar, sem recarregar a tela; testado no celular.
- [x] Deixar claro na tela o que é conferido no confronto papiloscópico. (qualidade, base biométrica e coerência com a CIN)

### Decisão do setor
- [x] Conjunto mínimo e qualidade. Premissa: 4 fotos (polegar e indicador de cada mão), 800 px e JPEG 0.8; confirmar com a papiloscopia.
- [ ] Integração com a base biométrica (TI e empresa da coleta) e LGPD. O MVP guarda as imagens no navegador e apaga depois da decisão; a API é externa.
- [x] Quem valida o confronto. Premissa: o papiloscopista; a fila registra o perfil na decisão e o resultado do confronto não é automático.

**Pronto quando**: o pedido sem documento aceita as fotos das impressões e o protocolo mostra o encaminhamento.

