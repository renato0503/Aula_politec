# Cenario 4 - Orcamento e Contratos

Dataset sintetico de **execucao orcamentaria e contratos** da POLITEC/MT, com
empenhos, dotacao anual, fornecedores, contratos e modalidades. Foco do
dashboard: **execucao orcamentaria (empenhado x liquidado x pago)**, ranking de
fornecedores, prazo de vigencia dos contratos e visibilidade para a **diretoria
financeira**. Anonimizado.

---

## Arquivos

| Tabela              | Grao (1 linha =)        | Linhas |
|---------------------|--------------------------|--------|
| `fato_empenhos`     | 1 nota de empenho        | 1.300  |
| `fato_dotacao`      | 1 setor x rubrica x ano  | 240    |
| `dim_setor`         | 1 setor                  | 8      |
| `dim_rubrica`       | 1 rubrica (codigo+rotulo)| 10     |
| `dim_modalidade`    | 1 modalidade             | 6      |
| `dim_fonte`         | 1 fonte de recurso       | 5      |
| `dim_status_empenho`| 1 status                 | 5      |
| `dim_fornecedor`    | 1 fornecedor             | 50     |
| `dim_contrato`      | 1 contrato               | 80     |
| `dim_calendario`    | 1 dia                    | 1096   |

---

## Sugestoes de visuais para a aba de Orcamento

- **Cartao (KPI)**: total empenhado, total pago, % execucao vs dotacao.
- **Funil (Waterfall)**: orcado x atual x empenhado x liquidado x pago.
- **Linha temporal**: empenho diario / mensal por fonte.
- **Colunas empilhadas**: setor x status de empenho.
- **Top-N (10) com detalhamento**: fornecedores com maior valor pago.
- **Tabela com sparkline**: contratos vigentes x valor x dias para vencer.
- **Slicer**: ano, setor, rubrica, fonte, modalidade, status.

---

## Numeros de referencia

| Indicador                                  | Valor aprox. |
|--------------------------------------------|--------------|
| Total empenhado (R$)                       | ~85 milhoes  |
| % Pago                                     | ~30%         |
| % Cancelado                                | ~8%          |
| Contratos ativos (nao vencidos em 2025)    | ~52          |
| Periodo dos fatos                          | 2023-01-01 a 2025-12-31 |
