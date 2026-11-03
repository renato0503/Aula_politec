# Roteiro de aceite e piloto da Distribuição de Casos de DNA (fictício)

> **Premissa assumida em 30/10/2026.** O piloto de 30 dias não foi executado.
> Ver [PREMISSAS.md](../../PREMISSAS.md) e
> [rotacao-e-naturezas.md](rotacao-e-naturezas.md).

## Roteiro do aceite (com a coordenação)

1. Abrir `#/config` e carregar os dados fictícios (4 peritos, 6 rodadas, 48 casos).
2. Em `#/rodada/nova`, montar uma rodada com 6 ordinários e 2 cobranças. Tentar
   distribuir com ordinário aguardando processamento: tem que bloquear (RN01).
3. Registrar o processamento e distribuir: a rodada inteira vai para um perito,
   que não é o da rodada anterior (RN02 e RN04).
4. Distribuir as cobranças em fila separada (RN03).
5. Em `#/rodada/<id>`, conferir a **sugestão do próximo perito** pelo histórico
   de rotação e marcar um caso como urgente com prioridade e justificativa
   (RN05).
6. Abrir `#/painel`: tempo médio entre processamento e distribuição, meta de
   1 dia, casos acima da meta e comparação por perito, natureza e rodada.
7. Em `#/importar`, importar a planilha de protocolos, associar as colunas e
   conferir o relatório de aceitas e recusadas. Repetir um protocolo na planilha:
   tem que recusar.
8. Exportar o CSV e imprimir em A4.

**Critério de aceite**: a rodada não distribui com ordinário pendente; a sugestão
respeita a rotação; a planilha não duplica protocolo.

## Piloto de 30 dias

| Medida | Linha de base | Meta |
|---|---|---|
| Intervalo processamento → distribuição | 2,5 dias (premissa) | 1 dia |
| Rodadas paradas | não medido | zero |
| Casos urgentes com justificativa | não medido | 100% |
| Protocolos importados sem duplicidade | não medido | 100% |

## Como confirmar

1. Rodar o roteiro com a coordenação da Biologia Molecular.
2. Confirmar a rotação e o número de peritos ativos.
3. Medir o intervalo real em 30 dias e comparar com a meta de 1 dia.
