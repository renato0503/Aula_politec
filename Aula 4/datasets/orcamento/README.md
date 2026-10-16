# Datasets de Orcamento e Contratos (Aula 4)

Conjunto **sintetico** de execucao orcamentaria e contratos administrativos de um
orgao de pericia oficial (POLITEC/MT), preparado para a **Parte 0 do caderno do
Dia 4** (preparacao de Power BI Desktop). Modelo **estrela**: uma tabela fato de
empenhos cercada por dimensoes.

> Dados anonimizados, gerados por `../../gerar_datasets_orcamento.py` (semente
> fixa). Qualquer semelhanca com dados reais e coincidencia.

---

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `Orcamento_Contratos_LIMPO.xlsx` | **Gabarito do professor**: as 10 tabelas do modelo estrela, limpas e tipadas (1 aba por tabela). |
| `Orcamento_Contratos_SUJO.xlsx` | **Arquivo do aluno**: os mesmos dados com **defeitos plantados** de proposito, para treinar a limpeza no Power Query. |
| `fato_*.csv`, `dim_*.csv` | O modelo estrela limpo em CSV (UTF-8 com BOM, separador `;`), para conferencia rapida. |

---

## Modelo estrela

Grao da fato principal: **1 linha = 1 empenho**.

```
                    dim_calendario
                          |
   dim_contrato --- fato_empenhos --- dim_fornecedor
                          |  |
        dim_setor --- dim_rubrica --- dim_modalidade
                          |
                     dim_fonte --- dim_status_empenho
```

### Tabelas fato

| Tabela | Grao (1 linha =) | Linhas | Chaves estrangeiras | Medidas |
|---|---|---|---|---|
| `fato_empenhos` | 1 empenho (nota de empenho) | 620 | data_empenho_key, contrato_key, fornecedor_key, setor_key, rubrica_key, modalidade_key, fonte_key, status_key | valor_empenhado, valor_liquidado, valor_pago, quantidade_itens |
| `fato_dotacao` | 1 setor x rubrica x ano | 192 | setor_key, rubrica_key, ano | valor_inicial, valor_atualizado |

### Dimensoes

| Tabela | Linhas | Chave | Atributos |
|---|---|---|---|
| `dim_calendario` | 1096 | data_key (AAAAMMDD) | data, ano, mes, nome_mes, ano_mes, trimestre, dia, dia_semana, nome_dia_semana |
| `dim_setor` | 8 | setor_key | sigla, setor |
| `dim_rubrica` | 8 | rubrica_key | codigo, rubrica, grupo |
| `dim_modalidade` | 5 | modalidade_key | modalidade |
| `dim_fonte` | 4 | fonte_key | fonte |
| `dim_status_empenho` | 5 | status_key | status |
| `dim_fornecedor` | 40 | fornecedor_key | razao_social, cnpj, porte, municipio, uf |
| `dim_contrato` | 60 | contrato_key | numero, tipo, objeto, data_inicio, data_fim, valor_contrato, fornecedor_key, setor_key, licitacao_numero |

`dim_setor` e uma **dimensao conformada** (atende `fato_empenhos` e `fato_dotacao`);
`dim_calendario` liga a data do empenho (`data_empenho_key`) e o ano da dotacao.

### Relacionamentos (N:1, direcao unica)

```
fato_empenhos -> dim_calendario (data_empenho_key)
              -> dim_contrato, dim_fornecedor, dim_setor, dim_rubrica,
                 dim_modalidade, dim_fonte, dim_status_empenho
fato_dotacao  -> dim_setor, dim_rubrica
              -> dim_calendario (ano <-> ano)
```

---

## Numeros de referencia

| Indicador | Valor |
|---|---|
| Empenhado total | R$ 185,647,376.30 |
| Liquidado total | R$ 119,816,424.10 |
| Pago total | R$ 91,516,819.49 |
| Dotacao atualizada | R$ 256,998,996.59 |
| Execucao (empenhado / dotacao) | 72.2% |

---

## Defeitos plantados no arquivo SUJO

Todos aparecem no `Orcamento_Contratos_SUJO.xlsx`; o `_LIMPO` e o gabarito.

| # | Defeito | Onde aparece | Como corrigir |
|---|---|---|---|
| 1 | Linha de titulo antes do cabecalho | todas as abas (linha 1) | Power Query: *Usar Primeira Linha como Cabecalho* |
| 2 | Datas como texto, em 5 formatos | fato_empenhos, dim_contrato, dim_calendario | tipo **Data**, com **Localidade: Portugues (Brasil)** |
| 3 | Datas com hora `00:00:00` no fim | dim_calendario | *Dividir coluna* por espaco ou alterar tipo para Data |
| 4 | Valores como texto (`R$ 1.234,56`, `1.234,56`, `R$ 1234.56`) | fato_empenhos, dim_contrato, fato_dotacao | *Substituir Valores* (remover `R$` e espacos) + tipo **Decimal** com virgula |
| 5 | Negativos entre parenteses `(1.500,00)` | fato_empenhos | *Substituir* `(` por `-` e remover `)` |
| 6 | Categorias com variacao de caixa e espacos | dim_setor (5 fica com 4 rotulos), dim_modalidade, dim_fonte, dim_status_empenho | *Formatar > Colunas de Texto*: **Cortar (Trim)** + **Caixa da Palavra (Capitalizar)**; depois *Remover Duplicatas* |
| 7 | Coluna `codigo` + `rubrica` juntos | dim_rubrica (`339014 - Diarias`) | *Dividir Coluna* por delimitador ` - ` |
| 8 | CNPJ com e sem pontuacao | dim_fornecedor | padronizar com *Substituir* ou manter so digitos |
| 9 | Espacos antes/depois do texto | dim_setor, dim_fornecedor, dim_rubrica | *Cortar (Trim)* |
| 10 | Linhas em branco no meio | fato_empenhos, dim_calendario | *Remover Linhas Vazias* |
| 11 | Linha `TOTAL GERAL` no fim | fato_empenhos | *Remover Linhas Filtradas* (filtrar `id_empenho` diferente de TOTAL GERAL) |
| 12 | Linhas duplicadas | fato_empenhos, dim_fornecedor | *Remover Duplicatas* |
| 13 | Chaves como texto | todas | alterar tipo para **Numero Inteiro** |
| 14 | Membro de dimensao orfao (key 999) | dim_fornecedor | filtrar/remover apos conferir |

---

## Como usar (Power Query)

1. Abra o Power BI Desktop -> **Obter Dados** -> **Pasta de Trabalho do Excel**.
2. Aponte para `Orcamento_Contratos_SUJO.xlsx` e marque as abas desejadas.
3. **Transformar Dados** e aplicar os ajustes da tabela de defeitos acima.
4. **Fechar e Aplicar**, criar os relacionamentos (N:1) e montar as 3 abas do painel.

O passo a passo detalhado esta na **Parte 0 do caderno do Dia 4**
(`../caderno-dia4.html`).

---

## Convencoes

- CSV UTF-8 com BOM, separador `;`, datas ISO `AAAA-MM-DD`.
- `data_key` inteiro no formato `AAAAMMDD`.
- Valores monetarios com virgula decimal no padrao pt-BR.
