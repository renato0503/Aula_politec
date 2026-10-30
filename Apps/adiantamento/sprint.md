# Controle de Adiantamentos · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py adiantamento` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py adiantamento` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py adiantamento` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |
| 4 | Feito em 30/10/2026. Motor de prazos (dias corridos e úteis com feriados), regra por tipo, selos e tela de feriados em `#/config`; código em `src/sprint4.js`. |
| 5 | Feito em 30/10/2026. Pendência com prazo de 10 dias úteis (RN05), prestação de contas com notas e conferência do concedido (RN06) e encerramento com ressalvas. |
| 6 | Feito em 30/10/2026. Painel com gráficos SVG, vencidos e a vencer; relatório com CSV e impressão em A4. |
| 7 | Feito em 30/10/2026. Roteiro de aceite e piloto em `modelos/roteiro-aceite.md`. |

Feriados: só os nacionais de 2026 e 2027; os de MT e do município entram pela tela de configuração (Sprint 4).

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Fluxo validado e dados | Fluxo validado com a DAS e a contabilidade, 10 pedidos fictícios, linha de base |
| 1 | Esqueleto | `index.html` com rotas, IndexedDB e backup |
| 2 | Novo pedido | Pedido com 3 orçamentos e justificativa (RN01) |
| 3 | Etapas e linha do tempo | Avançar etapa com data e responsável |
| 4 | Motor de prazos | Prazos do decreto em dias corridos e úteis, com feriados |
| 5 | Pendências e prestação de contas | Devoluções com prazo e notas fiscais (RN05, RN06) |
| 6 | Painel e relatório | Vencidos, a vencer, tempo por etapa, CSV |
| 7 | Aceite e piloto | Roteiro cumprido e 4 semanas de registro |

**MVP 100% pronto = Sprints 0 a 7.**

---

## Sprint 0 · Fluxo validado e dados

- [ ] Validar as 12 etapas da tabela AS-IS com a DAS e com a contabilidade da SESP. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Confirmar qual Orientação Técnica da CGE/MT vale (02/2026 ou 06/2025). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Anexar os documentos citados (AS-IS e TO-BE em .docx, planilha de controle). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [x] Gerar 10 pedidos fictícios: completos, sem orçamento, com devolução e com prazo vencido.
- [x] Montar a lista de feriados nacionais de 2026 e 2027.
- [ ] Acrescentar os feriados de MT e do município (Cuiabá) à lista. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Linha de base: anotar as datas dos pedidos de 4 semanas (proposta dos alunos). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

## Sprint 1 · Esqueleto

- [x] `index.html` gerado pela base comum, com as 6 rotas e os 7 stores.
- [x] Faixa do topo: "Protótipo, sem validade administrativa. O SICAD é o sistema oficial."
- [x] Backup `.json`, dados fictícios e `#/testes`.

**Pronto quando**: `python Apps/_base/testar.py adiantamento` passa.

## Sprint 2 · Novo pedido

- [x] Formulário com unidade, solicitante (nome e matrícula), finalidade, tipo, valor.
- [x] Três orçamentos (fornecedor, CNPJ com dígito verificador, valor) e justificativa.
- [x] Recusar o pedido sem os 3 orçamentos ou sem justificativa (RN01).
- [x] Ao salvar, abrir a etapa "Análise da DAS" (RN02).

## Sprint 3 · Etapas e linha do tempo

- [x] `#/processo/:id`: linha do tempo com as 12 etapas, a atual em destaque.
- [x] Avançar etapa: data (padrão hoje), responsável e observação, com registro no `log`.
- [x] Voltar etapa (devolução) com motivo.
- [x] Campo do número SICAD, preenchido quando o servidor cadastra no sistema.

## Sprint 4 · Motor de prazos

- [x] Funções testadas: `somarDiasCorridos`, `somarDiasUteis` (com feriados), `prazosDoProcesso`.
- [x] RN03 e RN04 a partir da data do pagamento e do tipo do processo.
- [x] Selos: no prazo, vence em até 7 dias, vencido.
- [x] Tela de feriados em `#/config`.

**Pronto quando**: os testes de prazo passam, incluindo 10 dias úteis com um feriado no meio.

## Sprint 5 · Pendências e prestação de contas

- [x] Registrar devolução da contabilidade: motivo e prazo de 10 dias úteis (RN05).
- [x] Resolver a pendência com a data.
- [x] `#/processo/:id/prestacao`: notas fiscais e soma comparada ao valor concedido (RN06).
- [x] Encerramento: "aprovado sem ressalvas" ou "com ressalvas" (decisão do ordenador, só registrada).

## Sprint 6 · Painel e relatório

- [x] `#/painel`: contagem por situação, vencidos, a vencer, tempo médio por etapa (gráfico em SVG).
- [x] `#/relatorio`: devoluções por motivo, tempo do pedido ao pagamento, CSV.
- [x] Relatório impresso em A4.

## Sprint 7 · Aceite e piloto

- [x] Roteiro de aceite com a DAS: registrar um pedido, avançar etapas, registrar uma devolução, ver o painel.
- [x] Piloto de 4 semanas com os pedidos reais (sem CPF, só o necessário).
- [x] Comparar com a linha de base e atualizar `PROJETO.md` e `README.md`.
