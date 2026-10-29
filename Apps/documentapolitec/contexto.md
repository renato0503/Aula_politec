# DOCUMENTAPOLITEC · contexto e arquitetura

> Equipe: Aline Xavier dos Passos (Coordenadoria de Patrimônio e Serviços)
> Fonte: `PROJETO.md` e a arquitetura do curso: **HTML monolítico, offline first**.

---

## 1. O problema

Os prontuários são digitalizados e guardados em sala cofre, mas falta espaço
físico. Cerca de 1.000 caixas box precisam ir para outra estrutura sem perder a
correspondência entre o físico e o digital. O risco é o extravio e a informação
equivocada.

| Dado informado | Valor |
|---|---|
| Caixas a transferir | 1.000 |
| Prontuários no acervo | 2,5 milhões |
| Prontuários físicos | anos anteriores a 2019 |
| Piloto | 30 dias, 2.400 prontuários |
| Planilha de teste | relação de 850 prontuários |

## 2. O que o MVP faz e o que não faz

| Faz | Não faz |
|---|---|
| Cadastra a caixa e a relação de prontuários | Lê o PDF digitalizado (Sprint 3) |
| Confere a relação com o arquivo digital (simulado) | Integra com o SIC |
| Aponta o prontuário sem correspondência | Guarda dados sensíveis na IA |
| Lacra a caixa com o responsável e a data (RN02) | Move as caixas fisicamente |
| Busca em qual caixa o prontuário está | Importa a planilha do Excel (Sprint 3) |

## 3. Regras

- **RN01**: o mesmo prontuário não pode estar em duas caixas nem repetido na relação.
- **RN02**: a caixa só é conferida e lacrada quando todos os prontuários conferem
  com o arquivo digital; o lacre exige o responsável.
- **RN03**: a busca localiza a caixa pelo número do prontuário (nome do cidadão no
  Sprint 4, quando houver índice autorizado).

## 4. Telas

| Rota | Perfil | O que faz |
|---|---|---|
| `#/painel` | todos | Caixas conferidas, pendentes, prontuários e divergências |
| `#/caixas` | todos | Lista das caixas e situação da conferência |
| `#/caixa/nova` | papiloscopista | Caixa com a relação de prontuários |
| `#/caixa/:id` | todos | Relação, conferência, lacre e histórico |
| `#/busca` | todos | Localiza a caixa do prontuário |
| `#/config` | todos | Perfil da cópia, backup e dados fictícios |

## 5. Modelo de dados (IndexedDB `documentapolitec_v1`)

| Store | Campos |
|---|---|
| `caixas` | id_caixa, setor_origem, responsavel, data, qtd, status, criado_em, lacrada_por, lacrada_em |
| `prontuarios` | numero, caixa_id, conferido, digital |
| `log` | id, caixa_id, acao, perfil, data_hora, detalhe |

## 6. LGPD

O protótipo usa números de prontuário fictícios, sem nome de cidadão. Na versão
institucional, o acesso exige login e senha para os servidores indicados pela
DMIT, e a busca por nome só pode existir com base legal e controle de acesso.
