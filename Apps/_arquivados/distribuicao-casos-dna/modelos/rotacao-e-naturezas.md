# Rotação, cascos por rodada e naturezas de exame (fictício)

> **Premissa assumida em 30/10/2026.** A rotação, o número de peritos ativos, os
> casos por rodada e as naturezas de exame não foram confirmados com a
> coordenação. Ver [PREMISSAS.md](../../PREMISSAS.md).

## 1. Peritos ativos

**4 peritos ativos**, em rotação estrita:

| Perito | Especialidade |
|---|---|
| P1 | crime sexual |
| P2 | identificação humana |
| P3 | local de crime |
| P4 | crime sexual |

## 2. A rotação

O perito da rodada **não pode ser o da rodada anterior** (RN04). O Sprint 3
melhorou isso: a ordem de sugestão passa a vir do **histórico de rotação**, e
não só do último escalado.

A ordem é:
1. quem está há **mais tempo sem rodada**;
2. em empate, quem tem **menos casos** acumulados;
3. em empate, pela sigla do perito.

O perito da rodada anterior fica de fora da lista de candidatos.

## 3. Casos por rodada

**8 casos por rodada**:

| Tipo | Quantidade | Fila |
|---|---|---|
| Ordinário | 6 | rodada inteira para um perito (RN02) |
| Cobrança | 2 | fila separada, distribuída em rodízio (RN03) |

A rodada só é distribuída com **todos os ordinários processados** (RN01). Com
ordinário aguardando, o botão de distribuição fica bloqueado.

## 4. Naturezas de exame

**3 naturezas**, que já aparecem na tabela de casos:

| Natureza |
|---|
| DNA |
| sexual |
| identificação humana |

## 5. Medidas

| Medida | Valor assumido |
|---|---|
| Intervalo entre processamento e distribuição | 2,5 dias (média do exemplo) |
| Meta | 1 dia |
| Dias sem rodada para a rodada ser considerada parada | mais de 5 dias |

## 6. Fila de urgência (Sprint 3)

Um caso entra na fila de urgência com **prioridade** (crítico, alta ou média) e
**justificativa** (RN05). Sem os dois, o app recusa. A ordem da fila é por
prioridade e, em empate, pela hora do registro.

## Como confirmar

1. Confirmar a rotação e o número de peritos ativos com a coordenação.
2. Confirmar os casos por rodada e a lista de naturezas de exame.
3. Medir o intervalo entre processamento e distribuição.
