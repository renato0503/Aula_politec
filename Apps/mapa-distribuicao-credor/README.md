# Mapa de Distribuição por Credor e Distribuição Orçamentária

Rotina que lê a planilha de distribuição por órgão (anexo do TR) e o relatório
do pregoeiro e gera o mapa por grupo, órgão e empresa, a tabela de conferência
e a distribuição orçamentária por credor e órgão, sem redigitação.

| Campo | Valor |
|---|---|
| Aluno | Igor Henrique de Menezes Costa |
| Contato | izgdreyar@gmail.com |
| Unidade | Setor de Licitações, POLITEC/MT |
| Tipo | Automação de script ou rotina |
| Stack pedida | HTML único (CSS/JS inline), JSON embutido, GitHub Pages (já é a arquitetura do curso) |
| Fonte | `Aula 8/Entregas/Automao-do-Mapa-...-2026-10-29 (2).json` (29/10/2026 09:04, horário de Cuiabá) |

## Arquivos

- `projeto.json`: resposta do formulário (importável).
- `PROJETO.md`: gerado pelo próprio formulário a partir do `.json`.
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.

## Pendências

- O `WorkFlow.docx` (fluxo atual com os exemplos 1 a 8 das planilhas) é a base
  do AS-IS e não veio com o envio.
- Faltam planilhas de exemplo e um relatório do pregoeiro de amostra, sem dado
  pessoal. Sem eles, o leitor de arquivos é escrito sobre um formato suposto.
- Na tabela de telas, as colunas ficaram deslocadas (o objetivo está em "rota",
  o usuário em "objetivo"). O `contexto.md` usa a leitura corrigida.
- A distribuição orçamentária está marcada como "MVP: Não" na tabela de telas,
  mas aparece no escopo e no critério de aceite. O `contexto.md` a mantém no MVP.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos substituídos:**

- `doc_faltando`: acrescentado o mapa manual de referência, que o critério de aceite exige.

**Tabelas:**

- telas e artefatos (`tArtefatos`): refeita. As colunas vieram deslocadas uma posição (o objetivo estava em rota, o usuário em objetivo); realinhadas, com as rotas do `contexto.md`. A distribuição orçamentária passou a MVP "Sim", como no escopo e no critério de aceite. Acrescentadas a tabela por empresa e a exportação.
- papéis (`tPapeis`): refeita. O terceiro papel (quem fornece o relatório com vencedores e valores) estava como "Analista de licitações"; corrigido para Pregoeiro.
- regras de negócio (`tRegras`): linhas acrescentadas. Acrescentadas as 4 regras que o formulário deixava abertas (homologado por item, arredondamento, ordem da dotação e grupo misto), com a proposta mais próxima das planilhas da equipe.
- fontes de dados (`tFontes`): linhas acrescentadas. Acrescentada a fonte da dotação, citada nas entradas do AS-IS.
- riscos (`tRiscos`): linhas acrescentadas. Acrescentados os riscos do cálculo.
- referências (`tRefs`): refeita. A Lei nº 4.320/1964 estava com o uso "justificar dados sintéticos"; ajustado para a classificação 3 e 4, que é o que o projeto usa. Acrescentada a homologação (Lei nº 14.133/2021).
