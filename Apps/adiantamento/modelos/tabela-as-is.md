# Tabela AS-IS do processo de adiantamento (fictícia)

> **Premissa assumida em 30/10/2026.** A tabela AS-IS oficial das 12 etapas não
> pôde ser anexada ao repositório. A relação abaixo é a mesma que o app usa nos
> dados fictícios e serve de referência para conferir a ordem real.
> Ver [PREMISSAS.md](../../PREMISSAS.md).

| # | Etapa | Quem entra | O que entra | O que sai | Onde o tempo passa |
|---|---|---|---|---|---|
| 1 | Levantar orçamentos | Unidade requisitante | Pedido com 3 orçamentos e CNPJ conferido | 3 propostas válidas | searching de preço |
| 2 | Dotação (NGER) | Unidade | Recurso disponível no exercício | Dotação confirmada | consulted do saldo |
| 3 | Análise da DAS | DAS | Processo com dotação e objeto | Parecer da DAS | conferindo a documentação |
| 4 | Análise da contabilidade | Contabilidade | Parecer da DAS | Parecer da contabilidade | esperando a fila da contabilidade |
| 5 | Aprovação da chefia | Chefia | Pareceres das duas análises | Autorização da chefia | aguardando a chefia |
| 6 | Autorização do ordenador | Ordenador de despesa | Autorização da chefia | Ordem autorizada | fila do ordenador |
| 7 | Cadastro no SICAD | Unidade | Ordem autorizada | Processo no SICAD | digitação no SICAD |
| 8 | Aplicação do recurso | Unidade | Processo no SICAD | Recurso aplicado | waiting do empenho |
| 9 | Pagamento | Financeiro | Empenho e nota fiscal | Comprovante de pagamento | tramitação do pagamento |
| 10 | Prestação de contas | Unidade | Comprovante de pagamento | Prestação de contas apresentada | montagem da prestação |
| 11 | Conferência SESP | SESP | Prestação de contas | Parecer da conferência | fila da conferência |
| 12 | Encerrado | — | Parecer conclusivo | Processo encerrado | — |

## Onde o tempo se perde (hipótese da linha de base)

| Etapa | Tempo médio | Fila |
|---|---|---|
| Análise da contabilidade | 4,5 dias | fila da contabilidade |
| Autorização do ordenador | 3,8 dias | fila do ordenador |
| Conferência SESP | 3,2 dias | fila da conferência |
| Pagamento | 3,0 dias | tramitação no financeiro |

**Tempo total do ciclo**: 21 dias corridos, com 15 dias úteis de espera.

## Premissas de regra

- **Orientação Técnica da CGE/MT**: vale a OT nº 06/2025, a mais recente já
  vigente no momento do desenho. A OT nº 02/2026 fica como revisão.
- **Feriados**: o prazo usa o calendário **nacional e estadual de MT**. O
  feriado municipal de Cuiabá não é aplicado, porque o recurso é federal. Os
  feriados do app estão no store `feriados`.
- **Linha de base**: 10 processos de exemplo, com entrada entre agosto e
  outubro de 2026.

## Como confirmar

1. Ler a tabela AS-IS oficial e conferir a ordem e os nomes das 12 etapas.
2. Se a ordem mudar, ajustar a lista `ETAPAS` em `exemplos/gerar_exemplos.py`.
3. Cronometrar 4 semanas de pedidos reais e substituir a coluna "tempo médio".
