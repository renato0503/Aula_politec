# Cenario 2 - TAT do Laboratorio de DNA

Dataset sintetico de **exames de DNA** da POLITEC/MT (4 laboratorios, 5
metodologias). Foco do dashboard: **TAT (turnaround time)**, gargalo por
laboratorio, qualidade da amostra, custo-eficiencia de kits. Anonimizado.

---

## Arquivos

| Tabela               | Grao (1 linha =)    | Linhas |
|----------------------|---------------------|--------|
| `fato_exames_dna`    | 1 exame de DNA      | 1100   |
| `dim_laboratorio`    | 1 laboratorio DNA   | 4      |
| `dim_metodologia`    | 1 metodologia       | 5      |
| `dim_analista`       | 1 analista          | 14     |
| `dim_status_exame`   | 1 status            | 6      |
| `dim_kit_reagente`   | 1 kit (kit, marca, lote) | 12 |
| `dim_calendario`     | 1 dia               | 1096   |

---

## Sugestoes de visuais para a aba de TAT do DNA

- **Cartao (KPI)**: TAT medio (geral), TAT mediano, % exames dentro da meta (90 dias).
- **Boxplot** nativo ou histograma: distribuicao de `tat_dias`.
- **Linha temporal**: TAT mensal por laboratorio.
- **Pareto**: exames por metodologia (concentracao de demanda).
- **Heatmap**: laboratorio (linha) x status (coluna), contagem.
- **Tabela cruzada**: kits mais usados por metodologia.
- **Slicer**: periodo (ano/mes), laboratorio, metodologia, status.

---

## Numeros de referencia (referencia)

| Indicador                                  | Valor aprox. |
|--------------------------------------------|--------------|
| Total de exames                            | 1.100        |
| % concluidos                               | ~88%         |
| TAT medio (dias)                           | ~70          |
| TAT P90 (estimado)                         | ~150 dias    |
| Periodo dos fatos                          | 2023-01-01 a 2025-12-31 |
