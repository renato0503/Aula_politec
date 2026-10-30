# Distribuição de Casos de DNA · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py distribuicao-casos-dna` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py distribuicao-casos-dna` passa (cenário em `Apps/_base/cenarios/sprint2.py`). |
| 3 | Feito em 30/10/2026. `python Apps/_base/testar_sprints.py distribuicao-casos-dna` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |

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

- [ ] Confirmar a rotação e o número de peritos ativos com a coordenação.
- [ ] Medir a linha de base do intervalo entre processamento e distribuição.
- [ ] Validar o número de casos por rodada e as naturezas de exame.

---

## Sprint 1 · Esqueleto e painel

- [x] `index.html` com 5 rotas, IndexedDB e backup.
- [x] Painel com casos sem perito, rodadas e tempo médio.
- [x] Lista de rodadas.

**Pronto quando**: `python Apps/_base/testar.py distribuicao-casos-dna` passa.

---

## Sprint 2 · Núcleo do MVP

- [x] Rodada com ordinários e cobranças, processamento registrado (RN01).
- [x] Rodada ordinária inteira para um perito, em rotação (RN02, RN04).
- [x] Cobranças em fila separada (RN03).

**Pronto quando**: `python Apps/_base/testar_sprints.py distribuicao-casos-dna` passa.

---

## Sprint 3 · Telas e regras

- [x] Sugestão automática do próximo perito com histórico de rotação.
- [x] Fila de urgência com justificativa (RN05).
- [x] Alerta de rodada parada.

**Pronto quando**: `python Apps/_base/testar_sprints.py distribuicao-casos-dna` passa (cenário do Sprint 3).

---

## Sprint 4 · Telas e regras

- [ ] Painel do coordenador com tempo entre processamento e distribuição.
- [ ] Comparação por rodada, perito e natureza de exame.
- [ ] Meta de 1 dia e acompanhamento.

---

## Sprint 5 · Telas e regras

- [ ] Importar a planilha de controle dos protocolos.
- [ ] Associação de colunas e relatório de aceitas e recusadas.
- [ ] Histórico de importações.

---

## Sprint 6 · Telas e regras

- [ ] Relatório de tempo médio, casos por perito e exportação CSV.
- [ ] Indicadores do piloto.
- [ ] Impressão em A4.

---

## Sprint 7 · Aceite e piloto

- [ ] Roteiro de aceite com a coordenação.
- [ ] Piloto de 30 dias comparando antes e depois.
- [ ] Atualizar `PROJETO.md` e `README.md`.

**Meta do piloto**: 30 dias (Da rodada à distribuição, com medida de espera.).
