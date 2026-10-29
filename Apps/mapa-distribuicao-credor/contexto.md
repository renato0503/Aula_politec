# Mapa de Distribuição por Credor · contexto e arquitetura

> Aluno: Igor Henrique de Menezes Costa (Setor de Licitações)
> Fonte: `PROJETO.md` (versão de 29/10/2026 09:04) e a decisão de arquitetura do
> professor: **HTML monolítico, offline first**. O aluno já tinha escolhido
> HTML único no GitHub Pages, então a arquitetura confirma a proposta dele.
> Os itens marcados com **[proposta]** dependem das regras da equipe de
> licitações e do orçamento (Sprint 0).

---

## 1. O problema

A equipe de licitações monta o mapa de distribuição em **8 etapas**, todas em
Excel, copiando os mesmos dados de uma planilha para outra:

| # | Etapa do AS-IS | Regra |
|---|---|---|
| 1 | Receber a distribuição de itens por órgão | cada item com sua unidade de medida |
| 2 | Compor o mapa por grupo e item (código, descrição, unidade, quantidade, valor unitário, total, estimado por órgão) | valores da pesquisa de preço |
| 3 | Preencher empresa vencedora e valor homologado | homologado substitui o estimado |
| 4 | Separar grupos homologados, fracassados e desertos | a situação define a observação |
| 5 | Criar resultado geral e por órgão | soma por órgão e total geral |
| 6 | Montar tabela por empresa e órgão | grupos ganhos por empresa |
| 7 | Montar tabela de conferência | totais batem com a planilha base |
| 8 | Montar a distribuição orçamentária por credor e órgão | custeio (3) ou investimento (4); excedente vai para o ano seguinte |

**Dor**: o mesmo dado é redigitado em cerca de **6 planilhas** (estimativa do
aluno). Por isso, a divergência entre estimado, homologado e distribuído só
aparece na etapa 7, no fim do trabalho, e atrasa a dotação. O tempo total e o
número de erros ainda estão **A MEDIR** (3 a 6 processos encerrados).

## 2. O que o MVP faz e o que não faz

| Faz | Não faz |
|---|---|
| Importa a planilha de distribuição por órgão e o relatório do pregoeiro | Busca dados no sistema oficial de licitação |
| Calcula totais por item, grupo, órgão e empresa | Valida a dotação (é decisão de pessoa) |
| Classifica cada grupo: homologado, fracassado, deserto | Gera documento oficial ou assinatura |
| Substitui o estimado pelo homologado | Grava no sistema de orçamento |
| Aponta divergências antes da distribuição | |
| Gera a distribuição orçamentária por credor e órgão, com o ano seguinte quando a dotação não basta | |
| Exporta tudo em `.xlsx`, com a origem de cada número | |

**Critério de aceite** (do aluno): os totais gerados batem com a planilha
manual de referência, **com diferença zero**, e as divergências inseridas de
propósito nos dados de teste são apontadas.

## 3. Arquitetura: HTML monolítico, offline first

**Um único `index.html`**, publicado no GitHub Pages e que também abre por
duplo clique. Os arquivos importados são lidos no navegador, e nada é enviado
a servidor.

```mermaid
flowchart LR
  A[Planilha de distribuição<br/>por órgão .xlsx] --> IMP
  B[Relatório do pregoeiro<br/>.xlsx / .csv] --> IMP
  C[Dotação por órgão<br/>e tipo .xlsx] --> IMP
  subgraph index.html - navegador, offline
    IMP[Importação<br/>SheetJS + mapeamento de colunas] --> VAL[Validação<br/>colunas, CNPJ, tipos]
    VAL --> MOT[Motor de cálculo<br/>centavos inteiros]
    MOT --> CONF[Conferência<br/>RN04 e divergências]
    CONF --> ORC[Distribuição<br/>orçamentária RN05/RN06]
    DB[(IndexedDB<br/>mapa_distribuicao_v1)]
    MOT <--> DB
  end
  ORC --> X[Mapa_Distribuicao_PROCESSO.xlsx<br/>8 abas, uma por etapa]
  CONF --> P[Relatório de divergências<br/>impressão / PDF]
```

### 3.1 Princípios

1. **Um arquivo só**: HTML, CSS, JS e a biblioteca SheetJS embutidos.
2. **Offline first**: o processo em andamento fica no IndexedDB, e o backup é
   um `.json`. Os dados de exemplo vêm embutidos no arquivo.
3. **O dado é lido uma vez**: toda tabela é calculada a partir das três fontes
   importadas. Nenhum número é digitado no meio do caminho.
4. **Rastreabilidade**: cada valor guarda o arquivo, a aba e a linha de origem.
   A edição manual fica registrada com o valor anterior (papel do analista:
   "não altera valor homologado sem registro").
5. **Dinheiro em centavos inteiros**, para o total bater com a planilha manual
   sem erro de arredondamento.

### 3.2 Estrutura de pastas

```
Apps/mapa-distribuicao-credor/
├── index.html
├── contexto.md
├── sprint.md
├── PROJETO.md
├── projeto.json
├── vendor/                 ← SheetJS (xlsx.full.min.js) + VERSOES.md
├── exemplos/
│   ├── distribuicao-orgaos.xlsx     ← 3 órgãos, 6 grupos, 30 itens (sintético)
│   ├── relatorio-pregoeiro.xlsx     ← 4 empresas fictícias, 1 fracassado, 1 deserto
│   ├── dotacao.xlsx                 ← custeio e investimento por órgão
│   ├── mapa-manual-referencia.xlsx  ← gabarito feito à mão (critério de aceite)
│   └── DIVERGENCIAS.md              ← lista das divergências plantadas
└── testes/testes.html
```

| Biblioteca | Uso | Tamanho aproximado |
|---|---|---|
| SheetJS Community (`xlsx.full.min.js`) | ler e gravar `.xlsx` e `.csv` | 900 KB |

O relatório em PDF usa `@media print`, sem biblioteca.

## 4. Telas (rotas)

| Rota | Quem | O que faz | Etapa do AS-IS |
|---|---|---|---|
| `#/processos` | Analista | Lista de processos, novo processo, backup | |
| `#/importar/:proc` | Analista | Carrega as 3 fontes, mapeia colunas, mostra o resumo lido | 1 |
| `#/mapa/:proc` | Analista | Mapa por grupo e item, com quantidade por órgão e estimado | 2 |
| `#/resultado/:proc` | Analista | Situação dos grupos e homologado no lugar do estimado | 3, 4, 5 |
| `#/empresas/:proc` | Analista | Tabela por empresa e órgão participante | 6 |
| `#/conferencia/:proc` | Analista, chefia | Totais, estimado x homologado, lista de divergências | 7 |
| `#/orcamento/:proc` | Analista, orçamento | Distribuição por credor e órgão, ano corrente e ano seguinte | 8 |
| `#/exportar/:proc` | Analista | `.xlsx` com 8 abas, relatório de divergências, `.json` | |
| `#/auditoria/:proc` | Analista, chefia | Importações, edições e aprovações com data e origem | |

## 5. Modelo de dados (IndexedDB `mapa_distribuicao_v1`)

| Store | Chave | Campos | Fonte |
|---|---|---|---|
| `processos` | `id_processo` | nome, numero, ano, status, criado_em | analista |
| `itens` | `grupo + item` | id_processo, codigo, descricao, unidade, quantidade_total, valor_unitario_estimado_c, tipo_despesa (3 ou 4), origem | planilha de distribuição |
| `distribuicao` | `orgao + item` | id_processo, orgao, grupo, item, quantidade, origem | planilha de distribuição |
| `resultado` | `grupo` (ou `grupo + item`) | situacao (homologado, fracassado, deserto), empresa, cnpj, valor_homologado_c, origem | relatório do pregoeiro |
| `dotacao` | `orgao + tipo + ano` | valor_c, validada_por, validada_em | orçamento |
| `distribuicao_orcamentaria` | `credor + orgao + tipo + ano` | valor_c, ano_seguinte_c | calculado |
| `auditoria` | `id` | data_hora, usuario, acao, arquivo, aba, linha, valor_anterior, valor_novo | app |

O sufixo `_c` indica valor em centavos (inteiro).

## 6. Regras de cálculo

| ID | Regra | Observação |
|---|---|---|
| RN01 | Total do item = quantidade × valor unitário | em centavos |
| RN02 | Grupo sem empresa é fracassado ou deserto, conforme o relatório | a situação vem do relatório, não é deduzida |
| RN03 | Valor homologado substitui o estimado | exceto grupo fracassado ou deserto, que mantém as colunas com a observação |
| RN04 | Soma por órgão = total do grupo | diferença vira alerta |
| RN05 | Se a dotação não comporta o valor no ano corrente, o excedente vai para o ano seguinte | coluna "ano seguinte" |
| RN06 | Cada grupo é custeio (3) ou investimento (4) | define a dotação usada |
| RN07 | CNPJ com 14 dígitos | o app também confere os dígitos verificadores |

**Pontos que o formulário deixava abertos (propostas registradas como RN08 a RN11 no `PROJETO.md`)**

1. **Homologado por grupo ou por item?** O relatório tem uma linha por grupo.
   Para distribuir o valor por órgão, o app precisa do valor unitário
   homologado de cada item. Se o relatório só traz o total do grupo, a proposta
   (RN08) é aplicar o mesmo desconto (homologado ÷ estimado) a todos os itens
   do grupo. A equipe confirma no Sprint 0.
2. **Arredondamento**: proposta (RN09): valor unitário com 2 casas e total do
   item arredondado a 2 casas, com as somas em centavos. A planilha manual
   define o gabarito, e o motor tem que repetir a mesma regra.
3. **Ordem de uso da dotação (RN05)**: quando vários credores dividem a mesma
   dotação de um órgão e ela não basta, qual entra primeiro no ano corrente?
   Proposta (RN10): ordem dos grupos no processo, salvo outra ordem definida pelo orçamento.
4. **Grupos "mistos"** (citados nos dados de exemplo): proposta (RN11): grupo
   com itens adjudicados a empresas diferentes, tratado item a item.

## 7. Divergências que a conferência aponta

| Código | Divergência | Nível |
|---|---|---|
| D01 | Soma das quantidades por órgão ≠ quantidade total do item | bloqueia |
| D02 | Item da distribuição sem grupo no relatório do pregoeiro | bloqueia |
| D03 | Homologado maior que o estimado | alerta |
| D04 | Grupo homologado sem empresa ou sem CNPJ | bloqueia |
| D05 | CNPJ inválido (RN07) | bloqueia |
| D06 | Soma por órgão ≠ total do grupo (RN04) | bloqueia |
| D07 | Órgão sem dotação do tipo do grupo | alerta |
| D08 | Valor enviado ao ano seguinte (RN05) | informa |
| D09 | Total do mapa gerado ≠ total da planilha manual de referência | bloqueia (no teste de aceite) |

## 8. Exportação

O `Mapa_Distribuicao_<processo>.xlsx` repete o formato que a equipe já usa
(exemplos 1 a 8 do `WorkFlow.docx`), uma aba por etapa: mapa por item, por
órgão, resultado, situação dos grupos, por empresa e órgão, conferência,
distribuição orçamentária e auditoria. Os valores saem como número, e não como
texto, para a equipe continuar usando as fórmulas dela no Excel.

## 9. LGPD e segurança

- Sem dado pessoal: órgãos, itens, valores e empresas (razão social e CNPJ são
  dados de pessoa jurídica). No MVP, tudo sintético.
- Os arquivos são lidos no navegador. A meta CSP bloqueia `connect-src`. Por
  isso, mesmo publicado no GitHub Pages, nenhum dado sai do computador.
- O GitHub Pages hospeda **só o app e os dados sintéticos**. Planilha real
  nunca vai para o repositório.
- Trilha de auditoria (requisito marcado): importações, edições e validações
  com data, usuário informado e arquivo de origem.

## 10. KPIs

| KPI | Fórmula | Linha de base |
|---|---|---|
| Tempo de montagem do mapa | hora final − hora inicial, por processo | A MEDIR (3 a 6 processos) |
| Divergências por processo | nº de divergências achadas na conferência | A MEDIR |
| Retrabalho de digitação | nº de planilhas que repetem o mesmo dado | cerca de 6 → meta 1 |

## 11. Riscos

| Risco | Mitigação |
|---|---|
| Relatório do pregoeiro muda de formato | Mapeamento de colunas salvo por modelo, e validação das colunas obrigatórias na importação |
| Falta de liberação dos dados reais | Dados sintéticos no MVP. O piloto usa um processo encerrado |
| Regra de arredondamento diferente da planilha manual | Teste de aceite com diferença zero contra o gabarito (D09) |
| Regra da dotação (ordem, ano seguinte) não está escrita | Sprint 0 escreve a regra com o orçamento antes do Sprint 6 |
