# Gestão de Documentos · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py gestao-documentos` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py gestao-documentos` passa (cenário em `Apps/_base/cenarios/sprint2.py`). |
| 3 | Feito em 30/10/2026. `python Apps/_base/testar_sprints.py gestao-documentos` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |
| 4 | Feito em 30/10/2026. Cobrança automática no vencimento (RN08), desligamento por lotação, histórico de cobranças; código em `src/sprint4.js`. |
| 5 | Feito em 30/10/2026. Conclusão com assinatura da autoridade (RN09), notificação ao requerente e arquivamento (RN10) e trilha de aprovação. |
| 6 | Feito em 30/10/2026. Painel com alertas amarelos, vencidos, cobranças e tempo médio até a conclusão; processos por lotação, CSV e impressão em A4. |
| 7 | Feito em 30/10/2026. Roteiro de aceite em `modelos/roteiro-aceite.md`. |
| 8 | Feito em 03/11/2026: anexo opcional no acompanhamento, data de entrada na lista, cobrança em 70% e no vencimento (painel/ficha) e botão Cobrar na lista. |

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Processo e dados | Regras validadas com as pessoas, dados fictícios e linha de base |
| 1 | Esqueleto e painel | `index.html` com rotas, IndexedDB e painel |
| 2 | Núcleo do MVP | O fluxo principal da entrega, com as regras do Sprint 2 |
| 3 a 6 | Telas e regras | As telas e regras dos sprints seguintes, uma por semana |
| 7 | Aceite e piloto | Roteiro de aceite e piloto com dados fictícios |
| Identidade e usabilidade | Feito em 02/11/2026. Casca lateral, cabeçalho sólido, fonte serifada, cantos suaves, superfície de papel e KPI em barra; caixa por perfil (a instruir, a revisar, a assinar) com prazo em barra, ficha em abas, checklist com caixa de seleção e quem marcou, e assinatura só para a autoridade decisora. `python testes/testar.py` e `python testes/cenarios.py` passam. |

**MVP 100% pronto = Sprints 0 a 7.**

---

## Sprint 0 · Processo e dados

- [ ] Validar a matriz de papéis e quem pode excluir documentos. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Definir os anexos obrigatórios por tipo de processo (RN01). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Medir a linha de base (1 h/dia, 200 processos/mês, 48 h na triagem). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

---

## Sprint 1 · Esqueleto e painel

- [x] `index.html` com 5 rotas, IndexedDB e backup.
- [x] Painel com vencidos, em atenção, no prazo e concluídos.
- [x] Mesa virtual com o sinal de cada processo.

**Pronto quando**: `python Apps/_base/testar.py gestao-documentos` passa.

---

## Sprint 2 · Núcleo do MVP

- [x] Autuação com anexos obrigatórios (RN01) e número AAAA.NNNN-SD (RN02).
- [x] Sinal amarelo a 70% e vermelho a 100% do prazo (RN06, RN07).
- [x] Segregação entre requerente e responsável (RN05).

**Pronto quando**: `python Apps/_base/testar_sprints.py gestao-documentos` passa.

---

## Sprint 3 · Telas e regras

- [x] Minutas padronizadas com os dados do processo (RN04).
- [x] Emissão de ofício e despacho.
- [x] Checklist de instrução por etapa.

**Pronto quando**: `python Apps/_base/testar_sprints.py gestao-documentos` passa (cenário do Sprint 3).

---

## Sprint 4 · Telas e regras

- [x] Cobrança automática registrada no vencimento (RN08).
- [x] Opção de desligar a cobrança por lotação.
- [x] Histórico de cobranças.

---

## Sprint 5 · Telas e regras

- [x] Conclusão somente com assinatura da autoridade (RN09).
- [x] Notificação ao requerente e arquivamento (RN10).
- [x] Trilha de aprovação.

---

## Sprint 6 · Telas e regras

- [x] Tempo médio de atribuição, alertas amarelos e cobranças.
- [x] Relatório em CSV e impressão.
- [x] Indicadores por lotação.

---

## Sprint 7 · Aceite e piloto

- [x] Roteiro de aceite com o Gabinete.
- [x] Piloto de 30 dias comparando o antes e o depois.
- [x] Atualizar `PROJETO.md` e `README.md`.

**Meta do piloto**: 30 dias (Da autuação à conclusão assinada.).

## Sprint 8 · Correções do feedback (03/11/2026)

> Feedback de Vitória (nota 3).

### Código
- [x] Tornar o anexo opcional no cadastro de processo de acompanhamento. (tipo "acompanhamento")
- [x] Mostrar a data de entrada na lista de processos.
- [x] Gerar notificação/cobrança quando o prazo final estiver próximo, inclusive para processo em outra lotação. (amarelo em 70% e vermelho no vencimento)

### Decisão do setor
- [x] Canal da notificação. Premissa: painel/ficha, com 70% do prazo (amarelo) e vencimento (vermelho); e-mail fica para a versão institucional.
- [x] Quais processos são só de acompanhamento: os marcados como "acompanhamento" no cadastro; o anexo é opcional.

**Pronto quando**: um processo de acompanhamento é cadastrado sem anexo e aparece na cobrança antes do vencimento.

