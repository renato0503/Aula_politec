# Gestão de Documentos · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py gestao-documentos` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py gestao-documentos` passa (cenário em `Apps/_base/cenarios/sprint2.py`). |
| 3 | Feito em 30/10/2026. `python Apps/_base/testar_sprints.py gestao-documentos` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Processo e dados | Regras validadas com as pessoas, dados fictícios e linha de base |
| 1 | Esqueleto e painel | `index.html` com rotas, IndexedDB e painel |
| 2 | Núcleo do MVP | O fluxo principal da entrega, com as regras do Sprint 2 |
| 3 a 6 | Telas e regras | As telas e regras dos sprints seguintes, uma por semana |
| 7 | Aceite e piloto | Roteiro de aceite e piloto com dados fictícios |

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

- [ ] Cobrança automática registrada no vencimento (RN08).
- [ ] Opção de desligar a cobrança por lotação.
- [ ] Histórico de cobranças.

---

## Sprint 5 · Telas e regras

- [ ] Conclusão somente com assinatura da autoridade (RN09).
- [ ] Notificação ao requerente e arquivamento (RN10).
- [ ] Trilha de aprovação.

---

## Sprint 6 · Telas e regras

- [ ] Tempo médio de atribuição, alertas amarelos e cobranças.
- [ ] Relatório em CSV e impressão.
- [ ] Indicadores por lotação.

---

## Sprint 7 · Aceite e piloto

- [ ] Roteiro de aceite com o Gabinete.
- [ ] Piloto de 30 dias comparando o antes e o depois.
- [ ] Atualizar `PROJETO.md` e `README.md`.

**Meta do piloto**: 30 dias (Da autuação à conclusão assinada.).
