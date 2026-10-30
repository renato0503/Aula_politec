# Renovação de Contratos · Hórus · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py renovacao-contratos-horus` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py renovacao-contratos-horus` passa (cenário em `Apps/_base/cenarios/sprint2.py`). |
| 3 | Feito em 30/10/2026. `python Apps/_base/testar_sprints.py renovacao-contratos-horus` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |

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

- [ ] Confirmar as seis faixas do semáforo e o alerta de 90 dias com a gestão.
- [ ] Definir as permissões de escrita (autor, chefia, gestor).
- [x] Receber uma base de contratos anonimizada ou validar os 15 fictícios.

---

## Sprint 1 · Esqueleto e painel

- [x] `index.html` com 5 rotas, IndexedDB e backup.
- [x] Painel com vencendo em 90 dias, urgentes, vencidos e as seis faixas.
- [x] Lista de contratos com filtros.

**Pronto quando**: `python Apps/_base/testar.py renovacao-contratos-horus` passa.

---

## Sprint 2 · Núcleo do MVP

- [x] Cadastro com término calculado e ajuste manual (R2).
- [x] Semáforo de seis faixas e exclusão dos encerrados (R3).
- [x] Termo aditivo atualiza a vigência e mantém Vigente (R4).

**Pronto quando**: `python Apps/_base/testar_sprints.py renovacao-contratos-horus` passa.

---

## Sprint 3 · Telas e regras

- [x] Checklist de instrução e anexos do processo (R7).
- [x] Documentos em repositório local com controle de acesso (R8).
- [x] Aviso de contrato sem instrução a 60 dias do fim.

**Pronto quando**: `python Apps/_base/testar_sprints.py renovacao-contratos-horus` passa (cenário do Sprint 3).

---

## Sprint 4 · Telas e regras

- [ ] Reajuste, repactuação e reequilíbrio com memória de cálculo.
- [ ] Fluxo Solicitado → Em análise → Aprovado → Aplicado.
- [ ] Limites legais de acréscimo e supressão.

---

## Sprint 5 · Telas e regras

- [ ] Trilha append-only completa (R6) e escrita por autor e chefia (R5).
- [ ] Histórico de substituição de fiscais.
- [ ] Perfis administrativos e de gestão.

---

## Sprint 6 · Telas e regras

- [ ] Contratos por faixa, valor em risco e tempo até a renovação.
- [ ] Relatório em CSV e impressão em A4.
- [ ] Comparação com a janela de 90 dias.

---

## Sprint 7 · Aceite e piloto

- [ ] Roteiro de aceite com a gestão de contratos.
- [ ] Piloto de 30 dias com contratos fictícios.
- [ ] Atualizar `PROJETO.md` e `README.md`.

**Meta do piloto**: 30 dias (Do monitoramento ao termo aditivo.).
