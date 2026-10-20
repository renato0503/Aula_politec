# Aula 6 - Datasets de Processo (Gestao de Projetos)

Tres **processos reais da POLITEC/MT**, medidos etapa a etapa. Sao a base do
metodo AS-IS -> BPMN/Mermaid -> **gargalo medido** -> TO-BE -> **automacao**.

Cada cenario tem o mesmo esquema em **modelo estrela**, com a mesma dimensao
de tabelas. O fato tem uma linha por **execucao de etapa**, com **tempo de
espera** (fila) e **tempo de execucao** (trabalho) separados. E essa separacao
que revela o gargalo.

| # | Cenario | Pasta | Fato | Linhas |
|---|---------|-------|------|--------|
| 1 | Requisicao pericial | `cenario1_processo_pericial/` | `fato_execucao` | ~1.800 |
| 2 | Empenho e contrato | `cenario2_processo_orcamento/` | `fato_execucao` | ~1.500 |
| 3 | Cadeia de custodia | `cenario3_processo_custodia/` | `fato_execucao` | ~1.600 |

Todos com `dim_calendario` de 1.096 dias (2023-01-01 a 2025-12-31).

---

## O schema (identico nos 3 cenarios)

```text
      dim_calendario   dim_projeto        dim_tipo_atividade
             |              |                       |
   dim_sistema --- fato_execucao --- dim_status_execucao
             |              |
      dim_unidade ---  dim_etapa
```

### Fato: `fato_execucao` (grao = 1 execucao de etapa)

| Coluna | O que e | Como usar |
|---|---|---|
| `id_execucao` | Identificador unico da execucao | chave da linha |
| `id_ciclo` | Identificador do **processo** (todos os casos comecam com `CIC-`) | agrupa as etapas de um caso |
| `etapa_key` | Etapa do processo | **dimensao que identifica o gargalo** |
| `unidade_key` | Quem executa | swimlane do diagrama |
| `sistema_key` | Em que sistema/support | identifica o trabalho manual |
| `tipo_atividade_key` | Manual / automatizada / aprovacao / decisao | base do mapeamento BPMN |
| `status_execucao_key` | Concluido / em andamento / devolvido / cancelado | qualidade do dado |
| `projeto_key` | Projeto de intervencao | planejar o TO-BE |
| `data_inicio_key` / `data_fim_key` | Datas | linha do tempo, lead time |
| **`tempo_espera_min`** | **Minutos na fila ANTES de comecar** | **onde o gargalo costuma estar** |
| `tempo_execucao_min` | Minutos de trabalho efetivo | onde ha trabalho real |
| `tempo_total_min` | Soma dos dois | tempo de ciclo |
| `flag_retrabalho` | 1 se a etapa voltou | desperdicio |
| `flag_automatizada` | 1 se ja automatizada |baseline de automacao |
| `custo_minuto` | Custo da Mao de obra | custo do processo |

### Dimensoes

| Dimensao | Linhas | Chave | Atributos |
|---|---|---|---|
| `dim_etapa` | 7-8 | `etapa_key` | etapa, sequencia, unidade_padrao, ativada_no_tobe |
| `dim_unidade` | 5-7 | `unidade_key` | unidade, tipo (Laboratorio / Apoio / Campo) |
| `dim_sistema` | 6 | `sistema_key` | sistema, digitizado, integrado |
| `dim_tipo_atividade` | 6 | `tipo_atividade_key` | tipo_atividade |
| `dim_status_execucao` | 4 | `status_execucao_key` | status_execucao |
| `dim_projeto` | 4 | `projeto_key` | projeto, escopo |
| `dim_calendario` | 1.096 | `data_key` | data, ano, mes, ano_mes, trimestre, dia, dia_semana |

---

## O metodo que estes dados sustentam

1. **AS-IS**: leia `dim_etapa` em ordem (`sequencia`) e desenhe o diagrama.
2. **Faca as perguntas do metodo** (Quem inicia? Onde espera? Quem decide?).
3. **Meça o gargalo**: some `tempo_espera_min` por `etapa_key`. A etapa com
   maior soma de espera e o gargalo (ver **Pareto das esperas** no caderno).
4. **TO-BE**: redesenhe o diagrama **eliminando ou automatizando** a etapa
   gargalo. Marque em `dim_etapa.ativada_no_tobe`.
5. **Automacao**: proponha um artefato digital (App, formulario, script) e
   calcule o **ganho** (minutos/ano e R$/ano poupados).

---

## Como usar (Excel / Google Sheets / Power BI)

1. **CSV UTF-8 com BOM, separador `;`**. Importe direto.
2. Comece pela tabela dinamica: `etapa` nas linhas, `SOMA(tempo_espera_min)`
   nas colunas. A maior barra e o gargalo.
3. Em Power BI, faca o mesmo com uma **matriz** e um **grafico de barras
   empilhadas** (espera x execucao por etapa).

---

## Convencoes

- CSV UTF-8 com BOM, separador `;`, datas ISO `AAAA-MM-DD`.
- `data_key` inteiro no formato `AAAAMMDD`.
- Chaves substitutas inteiras 1..N em ordem alfabetica.
- Tempos em **minutos** (fracionarios com 1 casa).
- Gerado por `../gerar_datasets_aula6.py` (semente fixa `20260610`).
- Dados sinteticos: qualquer semelhanca com processos reais e coincidencia.
