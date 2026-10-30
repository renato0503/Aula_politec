# Roteiro de aceite e piloto da Custódia Definitiva (fictício)

> **Premissa assumida em 30/10/2026.** O piloto de 90 dias não foi executado.
> Ver [PREMISSAS.md](../../PREMISSAS.md) e
> [categorias-e-conservacao.md](categorias-e-conservacao.md).

## Roteiro do aceite (com a equipe da custódia)

1. Abrir `#/config` e carregar os dados fictícios. Conferir as 5 categorias e a
   capacidade dos 5 contêineres.
2. Em `#/vestigio/novo`, cadastrar um vestígio e conferir a **sugestão de
   contêiner** (RN01 a RN03). Tentar um contêiner de outra categoria: tem que
   recusar.
3. Em `#/vestigios`, buscar por lacre, protocolo, categoria e contêiner, combinar
   filtros e exportar o CSV.
4. Em `#/vestigio/<id>`, registrar uma **transferência**, uma **saída para
   perícia** e o **retorno**, e conferir o histórico (RN04).
5. Abrir o bloco de **descarte**: conferir a idade do vestígio e o prazo da
   categoria. Autorizar o descarte com motivo (mínimo de 15 caracteres) e só
   então descartar.
6. Abrir `#/painel`: projeção de ocupação em 6 meses, saturação por contêiner,
   itens por categoria e por contêiner, entradas por mês e tempo médio até a
   primeira movimentação.
7. Exportar o CSV e imprimir em A4.

**Critério de aceite**: o vestígio não vai para contêiner de outra categoria nem
sem folga; o descarte só acontece com autorização registrada; a projeção usa os
12 meses da série.

## Piloto de 90 dias

| Medida | Linha de base | Meta |
|---|---|---|
| Tempo de recebimento | 40 min (premissa) | 40 min |
| Tempo de localização | 15 min (premissa) | 5 min |
| Contêineres em saturação | não medido | nenhum acima de 85% |
| Descarte com autorização registrada | não medido | 100% |

## Como confirmar

1. Rodar o roteiro com a equipe da custódia.
2. Conferir as categorias, a conservação e a capacidade real dos contêineres.
3. Medir o tempo de localização antes e depois, durante 90 dias.
