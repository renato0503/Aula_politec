# WorkFlow · exemplos 1 a 8 (fictício)

> **Premissa assumida em 30/10/2026.** O `WorkFlow.docx` do aluno não pôde ser
> anexado ao repositório. Os 8 exemplos abaixo reproduzem a estrutura que o app
> espera: cada processo tem um item por etapa, com o total que deve sair do
> rateio. Servem de gabarito para conferir a importação contra o arquivo real.
> Ver [PREMISSAS.md](../../PREMISSAS.md).

| # | Situação | Item | Dotação | Total esperado | Observação |
|---|---|---|---|---|---|
| 1 | Distribuição simples | Item 01 | Órgão A | 1.250,00 | Rateio proporcional, sem resto |
| 2 | Item com limite | Item 02 | Órgão A | 900,00 | Limite de 3 itens por credor |
| 3 | Dotação insuficiente | Item 03 | Órgão B | 0,00 | Dotação menor que o estimado: fica de fora |
| 4 | Resto de rateio | Item 04 | Órgãos C e D | 1.333,33 e 1.333,33 | Divisão por rateio, resto vai ao maior |
| 5 | Item homologado | Item 05 | Órgão A | 2.000,00 | Resultado do pregoeiro muda o valor |
| 6 | Item fracassado | Item 06 | Órgão B | 0,00 | Deserto: não distribui |
| 7 | Valor com diferença pequena | Item 07 | Órgão C | 749,98 | Tolerância de R$ 50,00 na checagem |
| 8 | Processo com várias áreas | Itens 08 a 12 | Órgãos A, B, C, D e E | rateio de 5 | Cada órgão recebe a parte da sua dotação |

## Colunas do arquivo do pregoeiro

| Coluna | Conteúdo | Observação |
|---|---|---|
| Item | Código do item | `01`, `02`… com 2 dígitos |
| Descrição | Texto do item | obrigatório |
| Situação | homologado, fracassado ou deserto | só homologado distribui |
| Empresa | Razão social | obrigatório quando homologado |
| CNPJ | 14 dígitos | validado pelo app |
| Valor unitário homologado | em R$ | obrigatório quando homologado |

## Colunas da planilha de distribuição

| Coluna | Conteúdo |
|---|---|
| Órgão | sigla do órgão destinatário |
| Item | código do item |
| Tipo de despesa | 3 (custeio) ou 4 (investimento) |
| Valor unitário estimado | em R$ |
| Quantidade total | número |

## Como confirmar

1. Conferir as colunas reais do `WorkFlow.docx` contra esta tabela.
2. Recalcular à mão 3 processos e bater com o gabarito
   `exemplos/mapa-manual-referencia.xlsx`.
3. Confirmar os 4 pontos de decisão: distribuição por dotação, rateio
   proporcional, limite de 3 itens por credor e tolerância de R$ 50,00.
