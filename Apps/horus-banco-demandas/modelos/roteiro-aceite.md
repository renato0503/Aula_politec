# Roteiro de aceite e piloto do Banco de Demandas (fictício)

> **Premissa assumida em 30/10/2026.** O piloto não foi executado. Decisão de
> projeto (premissa): a versão offline **serve às unidades sem acesso ao Hórus** e
> devolve o registro para digitação no sistema oficial.
> Ver [PREMISSAS.md](../../PREMISSAS.md) e [../horus/esquema.sql](../horus/esquema.sql).

## Roteiro do aceite (com o Hórus)

1. Abrir `#/config` e carregar os dados fictícios (1 órgão, 4 unidades, ciclo
   PCA 2027, 15 demandas, 3 manifestações).
2. Em `#/banco`, filtrar por grupo e situação e abrir uma demanda.
3. Em `#/trocar`, transferir uma demanda para outra unidade, com motivo. O
   histórico registra de onde veio, para onde foi, quem e quando.
4. Em `#/demanda/<id>/interesse`, registrar manifestação com unidade, quantidade
   e justificativa (20 caracteres).
5. Em `#/ciclos`, conferir o ciclo ativo. Criar um ciclo novo (entra encerrado) e
   ativar.
6. Em `#/aprovar`, selecionar demandas e aprovar no ciclo ativo.
7. Em `#/relatorios`, conferir demandas aprovadas, valor estimado, manifestações,
   por grupo e por unidade.
8. Exportar o **pacote do Hórus** (`.json`), conferir o campo `versao`, o ciclo e
   as demandas aprovadas, e importar na cópia do Hórus (ou entregar para
   digitação).
9. Exportar o CSV e imprimir em A4.

**Critério de aceite**: a troca exige motivo; a manifestação exige quantidade e
justificativa; o pacote leva **só** as demandas aprovadas no ciclo ativo.

## Piloto

| Medida | Linha de base | Meta |
|---|---|---|
| Demandas registradas fora do Hórus | planilha local | pelo app |
| Retrabalho de digitação | não medido | zero no pacote |
| Unidades sem acesso ao Hórus atendidas | não medido | todas |
| Manifestações com justificativa | não medido | 100% |

## Como confirmar

1. Rodar o roteiro com a gestão do Hórus.
2. Confirmar o esquema das 3 tabelas em `../horus/esquema.sql`.
3. Confirmar o formato de intercâmbio `horus-import-ciclo.json`.
