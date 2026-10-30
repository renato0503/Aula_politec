# Controle do Processo de Aquisição · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py controle-aquisicoes` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py controle-aquisicoes` passa (cenário em `Apps/_base/cenarios/sprint2.py`). |
| 3 | Feito em 30/10/2026. `python Apps/_base/testar_sprints.py controle-aquisicoes` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |
| 4 | Feito em 30/10/2026. Trilha de aprovação com as três análises (setor, perfil, data e parecer) e modalidade com critério de julgamento; código em `src/sprint4.js`. |
| 5 | Feito em 30/10/2026. Painel do gestor com tempo por etapa, retrabalho, pendências por unidade e por responsável e alerta de processo parado. |
| 6 | Feito em 30/10/2026. Processos por etapa, prazo médio, exportação CSV e impressão em A4. |
| 7 | Feito em 30/10/2026. Roteiro de aceite em `modelos/roteiro-aceite.md`. |

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

- [ ] Receber os modelos oficiais de DFD, ETP, TR e análise de riscos. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Confirmar o fluxo real de tramitação e os prazos de cada etapa. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Validar as permissões e a base de processos de 2024/2025. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

---

## Sprint 1 · Esqueleto e painel

- [x] `index.html` com 5 rotas, IndexedDB e backup.
- [x] Painel por etapa, atrasados e pendências.
- [x] Lista de processos com filtros.

**Pronto quando**: `python Apps/_base/testar.py controle-aquisicoes` passa.

---

## Sprint 2 · Núcleo do MVP

- [x] Registro com SIGADOC e SIAG únicos (RN01).
- [x] Avanço de etapa só com os documentos exigidos (RN02).
- [x] Pendência aberta impede o avanço (RN03).

**Pronto quando**: `python Apps/_base/testar_sprints.py controle-aquisicoes` passa.

---

## Sprint 3 · Telas e regras

- [x] Pesquisa de preços com três cotações e memória de cálculo (RN04).
- [x] Alerta de inconsistência entre estimado e cotado.
- [x] Histórico de preços por objeto.

**Pronto quando**: `python Apps/_base/testar_sprints.py controle-aquisicoes` passa (cenário do Sprint 3).

---

## Sprint 4 · Telas e regras

- [x] Trilha de aprovação por setor, com perfil e data.
- [x] Análise técnica, orçamentária e jurídica.
- [x] Definição da modalidade registrada.

---

## Sprint 5 · Telas e regras

- [x] Painel do gestor com tempo por etapa e retrabalho.
- [x] Pendências por unidade e por responsável.
- [x] Alerta de processo parado.

---

## Sprint 6 · Telas e regras

- [x] Processos por etapa, prazo médio e exportação CSV.
- [x] Relatório de retrabalho e devoluções.
- [x] Impressão em A4.

---

## Sprint 7 · Aceite e piloto

- [x] Roteiro de aceite com a aquisição.
- [x] Piloto com processos simulados, comparando o fluxo atual e o novo.
- [x] Atualizar `PROJETO.md` e `README.md`.

**Meta do piloto**: processos simulados (Do DFD à definição da modalidade.).
