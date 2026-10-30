# Modelo de caixa e formato do prontuário (fictício)

> **Premissa assumida em 30/10/2026.** O número oficial do prontuário e o modelo
> da caixa não chegaram ao grupo. Ver [PREMISSAS.md](../../PREMISSAS.md).

## 1. Formato do número do prontuário

**AAAA.NNNNNN**, com 10 dígitos:

| Parte | Significado | Exemplo |
|---|---|---|
| AAAA | ano de abertura do prontuário | 2019 |
| . | separador fixo | . |
| NNNNNN | sequencial dentro do ano | 000001 |

O app remove pontos e barras para comparar (2019.000001 = 2019000001) e recusa
número fora do formato de 4 a 12 dígitos.

## 2. Modelo da caixa

| Campo | Regra |
|---|---|
| Identificação | `CX-NNN`, sequencial |
| Setor de origem | unidade que entregou |
| Responsável pela conferência | quem assina o lacre (RN02) |
| Data | da conferência, não pode ser futura |
| Capacidade | de 8 a 14 prontuários por caixa |
| Relação | a lista de prontuários, um por linha |

O mesmo prontuário não pode estar em duas caixas (RN01). A relação aceita linha,
vírgula ou ponto e vírgula como separador.

## 3. Conferência e lacre (RN02)

1. O app confere a relação da caixa com o índice do arquivo digital.
2. Prontuário sem correspondência impede o lacre: a caixa fica com **divergência**.
3. Sem divergência, a caixa é lacrada com responsável e data.

## 4. Planilha de 850 prontuários

A planilha de exemplo (`exemplos/relacao-prontuarios.csv`) tem 850 linhas, com 3
linhas que a app deve recusar: 2 repetidas e 1 com número fora do formato. Serve
para medir a conferência.

## 5. Índice do arquivo digital

A leitura do PDF digitalizado chega como **relação de números** (o texto
extraído), no arquivo `exemplos/indice-arquivo-digital.csv`. O app compara as
duas listas e aponta, nas duas direções, o que não bate.

## Como confirmar

1. Confirmar o formato do número e a capacidade da caixa.
2. Receber a planilha real de 850 prontuários e a amostra do PDF.
3. Conferir se o índice do PDF digitalizado chega como texto extraído ou se o
   app precisa ler o PDF direto.
