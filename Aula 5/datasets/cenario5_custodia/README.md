# Cenario 5 - Cadeia de Custodia de Evidencias

Dataset sintetico de **movimentacao de evidencias** na cadeia de custodia
POLITEC/MT, da coleta ate o destino (lab/arquivo/destruicao). Foco do
dashboard: **rastreabilidade**, integridade da cadeia, tempo medio de
transporte, gargalo por local de armazenamento e **conformidade processual**
(quem coletou, quem recebeu, em quanto tempo).

---

## Arquivos

| Tabela                    | Grao (1 linha =)    | Linhas |
|---------------------------|---------------------|--------|
| `fato_mov_evidencia`      | 1 evidencia (ciclo) | 1.300  |
| `dim_tipo_evidencia`      | 1 tipo              | 10     |
| `dim_origem`              | 1 origem            | 8      |
| `dim_destino`             | 1 destino           | 8      |
| `dim_status_custodia`     | 1 status (5)        | 5      |
| `dim_responsavel`         | 1 pessoa            | 15     |
| `dim_local_armazenamento` | 1 local             | 8      |
| `dim_calendario`          | 1 dia               | 1096   |

---

## Sugestoes de visuais para a aba de Custodia

- **Sankey** ou **Fluxo**: origem -> destino (por tipo de evidencia).
- **Cartao (KPI)**: total de evidencias, tempo medio de transporte, lacradas.
- **Heatmap**: hora de coleta x dia da semana (gargalo operacional).
- **Linha do tempo (Drill Through)** por evidencia: cadeia completa.
- **Pareto**: tipos de evidencia por quantidade e por valor estimado.
- **Tabela de auditoria**: evidencias com `status = Em Transporte` (> 14 dias = alerta).
- **Slicer**: tipo, origem, destino, status, periodo.

---

## Numeros de referencia

| Indicador                                | Valor aprox. |
|------------------------------------------|--------------|
| Total de evidencias (ciclos)             | 1.300        |
| % lacradas ou concluidas                 | ~50%         |
| % ainda em transporte                    | ~15%         |
| Tempo medio de transporte (horas)        | ~80h         |
| % Materiais biologicos (DNA)             | ~22%         |
| Periodo dos fatos                        | 2023-01-01 a 2025-12-31 |

---

## Como integrar tudo no projeto integrador

1. Copie **pelo menos 3** pastas de cenario para `Documents/Projeto_Integrador/datasets/`.
2. No Power BI Desktop, **Obter Dados -> Pasta** apontando para essa pasta:
   o Power BI junta as tabelas (cada cenario tem suas proprias tabelas).
3. **Cuidado com dimensoes de mesmo nome**: tabelas `dim_calendario` vao se
   fundir se tiverem os mesmos campos; use sufixo (`dim_calendario_backlog`,
   `dim_calendario_dna`) ou remova de um dos cenarios.
4. Monte cada aba tematica: cada aba consome apenas as tabelas do seu cenario.
5. O **projeto integrador** exige **>=3 abas**, **>=1 slicer por aba**, e
   pelo menos um KPI com formato condicional.
