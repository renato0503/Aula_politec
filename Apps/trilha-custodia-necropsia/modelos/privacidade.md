# Privacidade e retenção (TCIN)

> **Premissa assumida em 30/10/2026.** O prazo de retenção e o texto abaixo não
> foram validados com o IML nem com o encarregado de dados. Ver
> [PREMISSAS.md](../../PREMISSAS.md).

## O que o app guarda

| Dado | Para quê | Onde |
|---|---|---|
| Protocolo, origem, natureza, município e local | identificar o acionamento | `corpos` |
| Nome e documento do corpo identificado | identificação civil | `corpos` |
| Marcos de deslocamento, com data, hora e perfil | trilha de custódia (RN03) | `marcos` |
| Lacres e destino das amostras | rastrear a amostra | `lacres` |
| Auto de entrega: responsável, documento e data | liberação (RN02) | `corpos.entrega` |
| Histórico de ações | auditoria | `log` |

## O que o app não guarda

- Nenhum dado de pessoa viva além do necessário à identificação do corpo.
- Nenhuma foto, nenhum laudo e nenhum dado de saúde.
- Nada sai do navegador: o app é offline e os dados ficam no IndexedDB.

## Retenção

| Situação | Prazo | O que acontece |
|---|---|---|
| Caso em andamento | enquanto durar | dados completos |
| Caso liberado | até a conferência da chefia | botão **Apagar os dados deste caso**: remove corpo, marcos, lacres e histórico do caso e mantém a contagem |
| Contagem | permanente | só o número de casos apagados (`contagens.tcin_apagados`) |

O botão de apagar só funciona em caso **liberado**. Caso em andamento não pode
ser apagado, para não perder a trilha de custódia.

## Acesso

O perfil escolhido na cópia define as telas, não é controle de segurança. A
recomendação é:

- **técnico** e **plantonista**: registram marcos, lacres e a situação;
- **gestor**: vê o painel, o relatório e pode apagar um caso liberado.

Fora da ficha, o nome aparece só pelas iniciais (RN05). O relatório e o CSV não
levam nome.

## O que confirmar

1. O prazo de retenção que o IML e o arquivo exigem (hoje: apagar depois da
   liberação, por decisão da chefia).
2. Se o auto de entrega precisa ser digitalizado e anexado (o app guarda só os
   dados do auto).
3. A base legal do tratamento (atribuição legal da perícia) e o encarregado de
   dados da POLITEC.
