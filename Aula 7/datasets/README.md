# Aula 7 - Datasets de Processo (Gargalo medido + Automação + Antigravity)

Cinco **processos novos da POLITEC/MT**, medidos etapa a etapa. São a base dos
cinco painéis da manhã e das cinco propostas de solução da tarde:
**gargalo medido** -> catálogo de intervenção -> **TO-BE** -> app no **GitHub**.

Cada cenário tem o mesmo esquema em **modelo estrela**, com as mesmas dimensões.
O fato tem uma linha por **execução de etapa**, com **tempo de espera** (fila) e
**tempo de execução** (trabalho) separados. É essa separação que revela o
gargalo.

| # | Cenário | Pasta | Workbook Excel | Fato | Linhas | Gargalo medido |
|---|---------|-------|----------------|------|--------|----------------|
| 1 | Apreensão e perícia de armas | `cenario1_apreensao_armas/` | `Cenario1_Apreensao_Armas.xlsx` | `fato_execucao` | **11.312** | Prova de fogo (40,3%) |
| 2 | Sinistro de trânsito | `cenario2_sinistro_transito/` | `Cenario2_Sinistro_Transito.xlsx` | `fato_execucao` | **11.336** | Conferência de documentos (35,7%) |
| 3 | Credenciamento de peritos | `cenario3_credenciamento_peritos/` | `Cenario3_Credenciamento_Peritos.xlsx` | `fato_execucao` | **10.152** | Análise de currículo (31,3%) |
| 4 | Operação de etilometria | `cenario4_etilometria/` | `Cenario4_Etilometria.xlsx` | `fato_execucao` | **12.176** | Emissão do auto de infração (28,9%) |
| 5 | Atendimento e ouvidoria | `cenario5_atendimento_ouvidoria/` | `Cenario5_Atendimento_Ouvidoria.xlsx` | `fato_execucao` | **13.432** | Instrução (35,5%) |

Total: **58.408 execuções de etapa**. Todos com `dim_calendario` de 1.096 dias
(2023-01-01 a 2025-12-31).

> **Para a sala de aula**, use o workbook `.xlsx` de cada pasta: ele traz todas
> as tabelas em abas separadas (`fato_execucao`, `dim_*`) mais uma aba
> `LEIA-ME` com o dicionário, os números medidos e o resumo por etapa. Os CSVs
> ficam como fonte e para quem preferir importar por pasta.

---

## O schema (idêntico nos 5 cenários)

```text
      dim_calendario   dim_projeto        dim_tipo_atividade
             |              |                       |
   dim_sistema --- fato_execucao --- dim_status_execucao
             |              |
      dim_unidade ---  dim_etapa
```

### Fato: `fato_execucao` (grão = 1 execução de etapa)

| Coluna | O que é | Como usar |
|---|---|---|
| `id_execucao` | Identificador único da execução | chave da linha |
| `id_ciclo` | Identificador do **processo** (todos os casos começam com `CIC-`) | agrupa as etapas de um caso |
| `etapa_key` | Etapa do processo | **dimensão que identifica o gargalo** |
| `unidade_key` | Quem executa | swimlane do diagrama e matriz do painel |
| `sistema_key` | Em que sistema ou suporte | identifica o trabalho manual |
| `tipo_atividade_key` | Manual / automatizada / aprovação / decisão | base do mapeamento BPMN |
| `status_execucao_key` | Concluído / em andamento / devolvido / cancelado | qualidade do dado |
| `projeto_key` | Projeto de intervenção | planejar o TO-BE |
| `data_inicio_key` / `data_fim_key` | Datas | linha do tempo, lead time |
| **`tempo_espera_min`** | **Minutos na fila ANTES de começar** | **onde o gargalo costuma estar** |
| `tempo_execucao_min` | Minutos de trabalho efetivo | onde há trabalho real |
| `tempo_total_h` | Soma dos dois, em **horas** | tempo de ciclo daquela etapa |
| `flag_retrabalho` | 1 se a etapa voltou | desperdício |
| `flag_automatizada` | 1 se já automatizada | baseline de automação |
| `custo_execucao_rs` | Custo da mão de obra daquela execução, em **R$** | custo do processo |

### Dimensões

| Dimensão | Linhas | Chave | Atributos |
|---|---|---|---|
| `dim_etapa` | 8 | `etapa_key` | etapa, sequencia, unidade_padrao, ativada_no_tobe |
| `dim_unidade` | 5-6 | `unidade_key` | unidade, tipo (Laboratório / Apoio / Operação) |
| `dim_sistema` | 6 | `sistema_key` | sistema, digitizado, integrado |
| `dim_tipo_atividade` | 6 | `tipo_atividade_key` | tipo_atividade |
| `dim_status_execucao` | 4 | `status_execucao_key` | status_execucao |
| `dim_projeto` | 4 | `projeto_key` | projeto, escopo |
| `dim_calendario` | 1.096 | `data_key` | data, ano, mes, ano_mes, trimestre, dia, dia_semana |

> **Atenção**: a `fato_execucao` e a `dim_etapa` usam a **mesma chave**
> (`etapa_key`), então o join funciona. Para ordenar as etapas do processo,
> use `dim_etapa.sequencia`, e não o texto da etapa.

---

## Os números medidos, por cenário

| Cenário | % espera do processo | TAT médio por caso | Espera acumulada em 3 anos | Top 2 do Pareto |
|---|---|---|---|---|
| 1. Armas | 92,1% | 821,4 h | 241.981 h | 61,6% |
| 2. Sinistro | 93,9% | 696,7 h | 215.980 h | 55,0% |
| 3. Credenciamento | 94,6% | 976,7 h | 277.321 h | 49,5% |
| 4. Etilometria | 96,5% | 856,0 h | 280.908 h | 57,0% |
| 5. Ouvidoria | 97,2% | 822,6 h | 287.825 h | 54,2% |

O padrão dos cinco: a espera domina o tempo do processo, e duas etapas
concentram de 49,5% a 61,6% dela.

---

## O método que estes dados sustentam

1. **Painel**: importe o workbook, relacione as chaves e crie as 11 medidas
   (8 base, 3 do Pareto e 1 do cenário).
2. **Pareto**: ordene as etapas por `tempo_espera_min` somado. A etapa com
   maior soma é o gargalo.
3. **Tipo de fila**: leia `dim_sistema` e `dim_tipo_atividade` da etapa do
   gargalo. Fila de sistema, de documento, de pessoa, de aprovação ou de
   equipamento.
4. **Intervenção**: escolha no catálogo de 10 intervenções da Parte 7 do caderno.
5. **Ganho**: espera medida x taxa de redução (hipótese) x um terço do período.
6. **TO-BE**: redesenhe o diagrama em Mermaid com a etapa nova de decisão.
7. **Piloto**: rode em uma unidade, por 30 a 90 dias, e meça o antes e o depois.

---

## Como usar (Excel / Google Sheets / Power BI)

1. **CSV UTF-8 com BOM, separador `;`**. Importe direto.
2. Comece pela tabela dinâmica: `etapa` nas linhas, `SOMA(tempo_espera_min)`
   nas colunas. A maior barra é o gargalo.
3. Em Power BI, faça o mesmo com uma **matriz** e um **gráfico de barras
   empilhadas** (espera x execução por etapa).

---

## Convenções

- CSV UTF-8 com BOM, separador `;`, datas ISO `AAAA-MM-DD`.
- `data_key` inteiro no formato `AAAAMMDD`.
- Chaves substitutas inteiras 1..N em ordem alfabética.
- `tempo_espera_min` e `tempo_execucao_min` em **minutos** (fracionários com 1 casa);
  `tempo_total_h` em **horas** (2 casas); `custo_execucao_rs` em **R$**.
- Gerado por `../gerar_datasets_aula7.py` (semente fixa `20261027`).
- Dados sintéticos: qualquer semelhança com processos reais é coincidência.
