# Datasets da Aula 2 — Planilhas e Manipulacao de Dados

## Arquivos disponiveis

| Arquivo | Descricao | Linhas |
|---|---|---|
| `requisicoes_periciais.csv` | Base principal de requisicoes periciais (laudos) | 120 |
| `movimentacao_reagentes.csv` | Entradas e saidas de reagentes por setor | 80 |
| `produtividade_peritos.csv` | Laudos concluidos por perito, mes e tipo | 96 |
| `orcamento_setores.csv` | Custo orcado x realizado por laboratorio | 24 |

## Estrutura

### 1. `requisicoes_periciais.csv`
Base de 120 requisicoes periciais com dados reais simulados de um laboratorio pericial.

| Coluna | Descricao | Exemplo |
|---|---|---|
| `id_requisicao` | Codigo unico da requisicao | `REQ-2025-0001` |
| `data_recebimento` | Data de entrada no laboratorio (AAAA-MM-DD) | `2025-03-15` |
| `delegacia_origem` | Nome da delegacia que requisitou | `1a DP - Cuiaba` |
| `tipo_exame` | Tipo de exame pericial | `Toxicologia` |
| `setor` | Laboratorio/setor responsavel | `Toxicologia` |
| `perito_responsavel` | Nome do perito | `Silva, A. P.` |
| `status` | Situacao atual | `Concluido`, `Em andamento`, `Pendente` |
| `data_laudo` | Data de emissao do laudo (vazio se pendente) | `2025-04-10` |
| `dias_uteis` | Dias uteis entre recebimento e laudo | `18` |

### 2. `movimentacao_reagentes.csv`
Controle de estoque de reagentes com entradas e saidas.

| Coluna | Descricao | Exemplo |
|---|---|---|
| `id` | Identificador unico | `1` |
| `data` | Data da movimentacao | `2025-01-10` |
| `reagente` | Nome do reagente | `Kit PCR - DNA` |
| `tipo_movimentacao` | `Entrada` ou `Saida` | `Entrada` |
| `quantidade` | Qtd em unidades | `50` |
| `setor` | Setor que entrou/saiu | `Genetica` |
| `fornecedor` | Origem da entrada (vazio em saida) | `Lab Diagnosticos Ltda` |

### 3. `produtividade_peritos.csv`
Laudos concluidos por perito, mes e tipo de exame.

| Coluna | Descricao | Exemplo |
|---|---|---|
| `mes` | Ano-Mes (AAAA-MM) | `2025-01` |
| `perito` | Nome do perito | `Silva, A. P.` |
| `tipo_exame` | Tipo de exame | `DNA` |
| `laudos_concluidos` | Quantidade de laudos | `12` |

### 4. `orcamento_setores.csv`
Execucao orcamentaria por laboratorio/setor.

| Coluna | Descricao | Exemplo |
|---|---|---|
| `laboratorio` | Nome do laboratorio | `Toxicologia` |
| `rubrica` | Categoria de gasto | `Reagentes` |
| `orcado` | Valor orcado (R$) | `45000` |
| `realizado` | Valor realizado (R$) | `38200` |

---

*Dados sinteticos/anonimizados gerados para fins educacionais. Qualquer semelhanca com dados reais e coincidencia.*
