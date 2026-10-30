# Importação, relatório e unidades (fictício)

> **Premissa assumida em 30/10/2026.** A exportação do Power BI 1, a amostra do
> PDF mensal, o cabeçalho da planilha do Google e a lista de unidades não foram
> confirmados com a TI. Ver [PREMISSAS.md](../../PREMISSAS.md).

## 1. O caminho de importação

O app importa a **exportação CSV do visual de pendências** do Power BI 1. O PDF
mensal entra só como conferência visual dos números, não como fonte de dados.

| Arquivo | Papel |
|---|---|
| `exemplos/powerbi1-2026-07.csv` | fonte de dados (o que o app importa) |
| `exemplos/powerbi1-2026-07.pdf` | conferência visual do mesmo mês |

## 2. O cabeçalho da planilha do Google

```
Unidade;Indicador;Realizado;Meta;Observação
```

O app identifica a coluna de unidade, a de realizado e a de meta, e avisa quando
alguma linha está sem uma delas (RN01).

## 3. As 10 unidades

| Unidade |
|---|
| IML Cuiabá |
| IML Várzea Grande |
| Laboratório Forense |
| Criminalística Cuiabá |
| Regional Rondonópolis |
| Regional Sinop |
| Regional Cáceres |
| Regional Barra do Garças |
| Regional Tangará da Serra |
| Regional Alta Floresta |

## 4. O relatório

Cada relatório carrega o total e as linhas do mês. A conferência (Sprint 3) é
linha a linha: o conferente marca a linha como conferida, ou corrige com
motivo (RN02 a RN05). A versão aprovada gera o relatório exportável do mês
(Sprint 4).

## 5. Linha de base

A atualização do mês leva **1 dia útil** (dia 5 do mês seguinte). O exemplo traz
3 meses, de julho a setembro de 2026.

## Como confirmar

1. Perguntar à TI se o Power BI 1 permite exportar dados do visual.
2. Conseguir a amostra do PDF mensal com números fictícios.
3. Copiar o cabeçalho real da planilha do Google.
4. Confirmar a lista de unidades e os nomes como aparecem no relatório.
5. Cronometrar a atualização do mês.
