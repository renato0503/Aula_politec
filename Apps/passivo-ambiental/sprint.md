# Passivo Ambiental · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py passivo-ambiental` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py passivo-ambiental` passa (cenário em `Apps/_base/cenarios/sprint2.py`). |
| 3 | Feito em 30/10/2026. `python Apps/_base/testar_sprints.py passivo-ambiental` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |

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

- [ ] Receber uma requisição real anonimizada e o modelo de laudo da unidade. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Confirmar o modelo de mapa (norte, escala, área) com o perito. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Cronometrar 5 laudos para confirmar a linha de base de 16 h. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

---

## Sprint 1 · Esqueleto e painel

- [x] `index.html` com 5 rotas, IndexedDB e backup.
- [x] Painel do passivo: abertas, fora do prazo, concluídas e horas.
- [x] Lista de requisições com prazo restante.

**Pronto quando**: `python Apps/_base/testar.py passivo-ambiental` passa.

---

## Sprint 2 · Núcleo do MVP

- [x] Registro da requisição e abertura do laudo com cabeçalho (RN01).
- [x] Rascunho e horas trabalhadas por laudo.
- [x] Recusa de requisição repetida e de data futura.

**Pronto quando**: `python Apps/_base/testar_sprints.py passivo-ambiental` passa.

---

## Sprint 3 · Telas e regras

- [x] Editor de mapa com modelos pré-definidos e elementos obrigatórios (RN02).
- [x] Anexo de mapas ao laudo.
- [x] Exportação em PDF com cabeçalho e mapas (RN03).

**Pronto quando**: `python Apps/_base/testar_sprints.py passivo-ambiental` passa (cenário do Sprint 3).

---

## Sprint 4 · Telas e regras

- [ ] Conclusão do laudo com assinatura registrada.
- [ ] Bloqueio de conclusão sem cabeçalho completo e sem mapa.
- [ ] Atualização da situação da requisição.

---

## Sprint 5 · Telas e regras

- [ ] Fila do passivo por prazo e complexidade.
- [ ] Priorização das 300 requisições atrasadas.
- [ ] Alerta de prazo no painel.

---

## Sprint 6 · Telas e regras

- [ ] Tempo por laudo e horas por tipo de infração.
- [ ] Relatório de produtividade em CSV.
- [ ] Comparação com a meta de 12 h.

---

## Sprint 7 · Aceite e piloto

- [ ] Roteiro de aceite com o perito.
- [ ] Piloto com 5 laudos reais autorizados.
- [ ] Atualizar `PROJETO.md` e `README.md`.

**Meta do piloto**: 5 laudos (Da requisição ao laudo em PDF, com mapas.).
