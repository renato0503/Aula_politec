# Custódia Definitiva · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py custodia-definitiva` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py custodia-definitiva` passa (cenário em `Apps/_base/cenarios/sprint2.py`). |
| 3 | Feito em 30/10/2026. `python Apps/_base/testar_sprints.py custodia-definitiva` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |

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

- [ ] Conferir categorias, condições de conservação e capacidades com a equipe da custódia. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Receber a medição real de volume, tempo de recebimento e tempo de localização. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [x] Gerar 30 vestígios fictícios, 5 contêineres e 12 meses de histórico.

---

## Sprint 1 · Esqueleto e painel

- [x] `index.html` com perfis, 6 rotas, IndexedDB e backup.
- [x] Painel com total de vestígios, ocupação, contêineres cheios e pendências.
- [x] Tela de contêineres com capacidade e folga.

**Pronto quando**: `python Apps/_base/testar.py custodia-definitiva` passa.

---

## Sprint 2 · Núcleo do MVP

- [x] Cadastro com lacre único, categoria e volume (RN01).
- [x] Sugestão de contêiner compatível e recusa de volume sem folga (RN02, RN03).
- [x] Movimentação de entrada com perfil, data e hora (RN04).

**Pronto quando**: `python Apps/_base/testar_sprints.py custodia-definitiva` passa.

---

## Sprint 3 · Telas e regras

- [x] Busca por lacre, protocolo, categoria e contêiner.
- [x] Filtros combinados e exportação CSV do acervo.
- [x] Histórico de movimentações por vestígio.

**Pronto quando**: `python Apps/_base/testar_sprints.py custodia-definitiva` passa (cenário do Sprint 3).

---

## Sprint 4 · Telas e regras

- [ ] Projeção de ocupação a partir da série de 12 meses.
- [ ] Tendência e alerta de saturação por contêiner.
- [ ] Cenário de crescimento com entradas e saídas.

---

## Sprint 5 · Telas e regras

- [ ] Regra de elegibilidade para descarte por categoria e idade.
- [ ] Sinalização de materiais aptos, com autorização humana registrada.
- [ ] Bloqueio de descarte sem autorização (fora do MVP).

---

## Sprint 6 · Telas e regras

- [ ] Painel do gestor por categoria, contêiner e período.
- [ ] Relatório de ocupação e movimentações em CSV.
- [ ] Indicadores de tempo de localização antes e depois.

---

## Sprint 7 · Aceite e piloto

- [ ] Roteiro de aceite com a equipe da custódia.
- [ ] Piloto de 90 dias com dados fictícios e medição do tempo de localização.
- [ ] Atualizar `PROJETO.md` e `README.md`.

**Meta do piloto**: 90 dias (Do cadastro à consulta e à projeção de ocupação.).
