# Cenario 1 - Backlog de Pericias

Dataset sintetico de **requisicoes periciais** da POLITEC/MT para o **projeto
integrador** da Aula 5. O foco e construir um dashboard de **fila de trabalho**
com TAT (turnaround time), atraso por setor e perito, e distribuicao por
tipo de exame e prioridade. Anonimizado, gerado por
`../gerar_datasets_aula5.py` (semente fixa).

---

## Arquivos (modelo estrela)

```text
              dim_calendario  dim_status  dim_prioridade
                    \           |              |
   dim_setor -- fato_requisicoes -- dim_perito
                    |
            dim_tipo_exame  dim_delegacia
```

| Tabela              | Grao (1 linha =)    | Linhas |
|---------------------|---------------------|--------|
| `fato_requisicoes`  | 1 requisicao        | 1200   |
| `dim_setor`         | 1 setor             | 8      |
| `dim_perito`        | 1 perito            | 12     |
| `dim_tipo_exame`    | 1 tipo de exame     | 8      |
| `dim_delegacia`     | 1 delegacia (MT)    | 16     |
| `dim_prioridade`    | Alta / Media / Baixa | 3     |
| `dim_status`        | 5 estados           | 5      |
| `dim_calendario`    | 1 dia               | 1096   |

---

## Sugestoes de visuais para a aba de Backlog

- **Cartao (KPI)**: total em atraso, % de laudos concluidos no prazo.
- **Colunas agrupadas**: backlog por `setor_key` filtrando `status = Aguardando/Em Analise`.
- **Linha temporal**: TAT medio mensal (mediana) por mes/ano.
- **Matriz**: cruzamento `setor x tipo_exame` com `em_atraso`.
- **Slicer**: `data_entrada_key`, `prioridade`, `tipo_exame`, `delegacia_key`.
- **Tabela de detalhe**: top 10 requisicoes atrasadas (drill through).

---

## Numeros de referencia (referencia)

| Indicador                                   | Valor aprox. |
|---------------------------------------------|--------------|
| Total de requisicoes                        | 1.200        |
| % concluidas                                | ~80%         |
| % dentro do prazo                           | ~70%         |
| Prazo medio (dias uteis) para DNA           | 90           |
| Prazo medio (dias uteis) para Necropsia     | 15           |
| Periodo dos fatos                           | 2023-01-01 a 2025-12-31 |
