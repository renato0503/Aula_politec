# DOCUMENTAPOLITEC · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py documentapolitec` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py documentapolitec` passa (cenário em `Apps/_base/cenarios/sprint2.py`). |

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

- [ ] Confirmar o formato do número do prontuário e o modelo das caixas.
- [ ] Receber a planilha de teste com a relação de 850 prontuários.
- [ ] Receber uma amostra do PDF digitalizado, sem dado pessoal.

---

## Sprint 1 · Esqueleto e painel

- [x] `index.html` com 6 rotas, IndexedDB e backup.
- [x] Painel com caixas conferidas, pendentes, prontuários e divergências.
- [x] Lista das caixas com situação da conferência.

**Pronto quando**: `python Apps/_base/testar.py documentapolitec` passa.

---

## Sprint 2 · Núcleo do MVP

- [x] Caixa com relação de prontuários e recusa de duplicidade (RN01).
- [x] Conferência com o arquivo digital (simulado).
- [x] Lacre com responsável e data, só sem divergência (RN02).

**Pronto quando**: `python Apps/_base/testar_sprints.py documentapolitec` passa.

---

## Sprint 3 · Telas e regras

- [ ] Importar a planilha de 850 prontuários com associação de colunas.
- [ ] Ler o PDF digitalizado e comparar com a relação.
- [ ] Relatório de linhas aceitas, recusadas e divergentes.

---

## Sprint 4 · Telas e regras

- [ ] Busca por nome do cidadão, com índice autorizado e controle de acesso (RN03).
- [ ] Resultado com caixa, setor e situação.
- [ ] Trilha de consultas.

---

## Sprint 5 · Telas e regras

- [ ] Etiqueta da caixa com QR Code e código de conferência.
- [ ] Leitura do QR Code na conferência.
- [ ] Impressão das etiquetas em lote.

---

## Sprint 6 · Telas e regras

- [ ] Caixas conferidas, pendentes, espaço liberado e prontuários por período.
- [ ] Relatório em CSV e impressão.
- [ ] Indicadores de tempo de conferência.

---

## Sprint 7 · Aceite e piloto

- [ ] Roteiro de aceite com a DMIT.
- [ ] Piloto de 30 dias com 2.400 prontuários fictícios.
- [ ] Atualizar `PROJETO.md` e `README.md`.

**Meta do piloto**: 2.400 prontuários (Da caixa ao lacre e à busca do prontuário.).
