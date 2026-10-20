# Cenario 2 - Processo de Empenho e Contrato

O caminho do dinheiro publico: pedido, cotacao, parecer juridico, autorizacao,
empenho e publicacao. Aqui o gargalo e um **conjunto** (parecer + autorizacao
= 51,2% da espera), tipico de processo com varias aprovacoes encadeadas.

Numeros **medidos** no dataset gerado (media por execucao de etapa):

| Etapa | Espera media | Execucao media | Retrabalho |
|---|---|---|---|
| 1. Pedido do setor (papeis) | 0 h | 4 h | 15,9% |
| 2. Cotacao no sistema | 10 h | 0 h | 16,4% |
| 3. Mapa comparativo | 21 h | 6 h | 17,0% |
| **4. Parecer juridico** | **36 h** | 5 h | 17,0% |
| **5. Autorizacao do ordenador** | **27 h** | 1 h | 16,3% |
| 6. Empenho e contratacao | 11 h | 0 h | 16,6% |
| 6. Publicacao do ato | 18 h | 0 h | 16,9% |

**Achado principal**: **51,2% da espera** esta em duas etapas de aprovacao
(parecer + autorizacao), e o retrabalho e o mais alto dos tres cenarios
(**~16,5%**). O mapa comparativo (etapa 3) tem **6 h de execucao** — o maior
trabalho manual do processo, e ele e atrasado por causa das aprovacoes.

**Para onde aponta a intervencao**: as duas aprovacoes. A TO-BE move a **pauta
automatica**: o sistema monta a pauta (todo expediente dentro do prazo) e
dispara a aprovacao, com fila priorizada por dotacao critica.

**Sugestao de Mermaid**: use subgraphs por unidade (Divisao de Compras,
Juridico, Controle Interno). Destaque o gateway de decisao "dotacao
suficiente?".

---

## Observacao sobre nomes duplicados

As etapas 6 e 7 desta tabela aparecem com prefixos iguais porque a coluna
`etapa` foi truncada na geracao. A distincao esta em `dim_etapa.sequencia`
(6 = Empenho, 7 = Publicacao). Sempre ordene por `sequencia`, nunca pelo texto.
