# Datasets da Capacitacao POLITEC/MT (Aulas 2, 3 e 4)

Dados **sinteticos** de um laboratorio pericial da POLITEC/MT. O conjunto e
**autocontido** e replicado nas pastas `datasets/` das Aulas 2, 3 e 4, para que
cada aula funcione isolada. Ha dois niveis de dados:

1. **Fontes planas** — as bases como saem do sistema de origem (uma tabela por
   assunto). Usadas na Aula 2 (planilhas) e como entrada do ETL na Aula 3.
2. **Modelo estrela** — as mesmas bases organizadas em tabelas `fato_*` e `dim_*`
   com chaves substitutas. Usadas para modelagem e BI na Aula 3 (ETL) e na Aula 4
   (Power BI).

Gerado por `../../gerar_datasets_estrela.py` a partir das fontes planas.

---

## 1. Fontes planas

| Arquivo | Linhas | Colunas |
|---|---|---|
| `requisicoes_periciais.csv` | 120 | id_requisicao, data_recebimento, delegacia_origem, tipo_exame, setor, perito_responsavel, status, data_laudo, dias_uteis |
| `movimentacao_reagentes.csv` | 80 | id, data, reagente, tipo_movimentacao, quantidade, setor, fornecedor |
| `produtividade_peritos.csv` | 218 | mes, perito, tipo_exame, laudos_concluidos |
| `orcamento_setores.csv` | 36 | laboratorio, rubrica, orcado, realizado |

---

## 2. Modelo estrela

### Tabelas fato

| Arquivo | Grao (1 linha =) | Linhas | Chaves estrangeiras | Medidas |
|---|---|---|---|---|
| `fato_requisicoes.csv` | 1 requisicao pericial | 120 | data_recebimento_key, data_laudo_key, setor_key, tipo_exame_key, perito_key, delegacia_key, status_key | dias_uteis, em_atraso |
| `fato_movimentacao.csv` | 1 movimento de reagente | 80 | data_key, reagente_key, setor_key, tipo_movimentacao_key, fornecedor_key | quantidade |
| `fato_produtividade.csv` | 1 perito x mes x tipo de exame | 218 | perito_key, data_key, tipo_exame_key | laudos_concluidos |
| `fato_orcamento.csv` | 1 laboratorio x rubrica | 36 | setor_key, rubrica_key | orcado, realizado |

### Dimensoes

| Arquivo | Linhas | Chave | Atributo |
|---|---|---|---|
| `dim_calendario.csv` | 396 | data_key (AAAAMMDD) | data, ano, mes, nome_mes, ano_mes, trimestre, dia, dia_semana, nome_dia_semana |
| `dim_setor.csv` | 6 | setor_key | setor |
| `dim_tipo_exame.csv` | 5 | tipo_exame_key | tipo_exame |
| `dim_perito.csv` | 8 | perito_key | perito |
| `dim_delegacia.csv` | 13 | delegacia_key | delegacia |
| `dim_status.csv` | 3 | status_key | status |
| `dim_reagente.csv` | 10 | reagente_key | reagente |
| `dim_fornecedor.csv` | 6 | fornecedor_key | fornecedor |
| `dim_tipo_movimentacao.csv` | 2 | tipo_movimentacao_key | tipo_movimentacao |
| `dim_rubrica.csv` | 6 | rubrica_key | rubrica |

`dim_setor` e uma **dimensao conformada**: atende requisicoes, movimentacao e
orcamento (o campo `laboratorio` do orcamento aponta para a mesma dimensao).

### Relacionamentos (1 fato -> N dimensoes)

```
fato_requisicoes -> dim_calendario (data_recebimento_key, data_laudo_key)
                 -> dim_setor, dim_tipo_exame, dim_perito, dim_delegacia, dim_status
fato_movimentacao -> dim_calendario (data_key), dim_reagente, dim_setor,
                     dim_tipo_movimentacao, dim_fornecedor
fato_produtividade -> dim_calendario (data_key = 1o dia do mes), dim_perito, dim_tipo_exame
fato_orcamento     -> dim_setor, dim_rubrica
```

---

## 3. Como usar em cada aula

- **Aula 2 (Google Sheets):** as fontes planas para formulas e filtros; o modelo
  estrela para praticar `PROCV`/`XPROCV` (traduzir a chave pelo atributo da
  dimensao) e para entender fato x dimensao antes do BI.
- **Aula 3 (ETL / Power Query):** transformar as fontes planas no modelo estrela
  (mesclar com as dimensoes, gerar chaves) e validar as contagens.
- **Aula 4 (Power BI):** carregar as tabelas `fato_*` e `dim_*`, criar os
  relacionamentos e as medidas do painel.

---

## 4. Convencoes

- **CSV UTF-8 com BOM**, separador `;`, quebra de linha CRLF.
- **Datas** em ISO `AAAA-MM-DD`; `data_key` no formato inteiro `AAAAMMDD`.
- **Chaves substitutas** inteiras, atribuidas em ordem alfabetica do atributo.
- **Valores categoricos** sem acento, como no sistema de origem
  (`Concluido`, `Identificacao`, `Genetica`). Os rotulos do calendario
  (`nome_mes`, `nome_dia_semana`) seguem o portugues com acento.
- **Chave vazia** significa "sem valor" (ex.: `data_laudo_key` de laudo pendente
  e `fornecedor_key` de uma saida de estoque).

*Dados sinteticos/anonimizados para fins educacionais. Qualquer semelhanca com
dados reais e coincidencia.*
