# Hórus · Banco de Demandas

Repositório de demandas de contratação reutilizáveis: cada unidade cadastra o
item uma vez (especificação, valor, quantidade, orçamento), outras unidades da
mesma diretoria manifestam interesse e a chefia aprova o item para o ciclo do
PCA.

| Campo | Valor |
|---|---|
| Aluno | Iohan Camões de Albuquerque |
| Contato | iohan.camoes@gmail.com |
| Unidade | POLITEC/MT, Planejamento de Contratações (PCA) |
| Tipo | Aplicativo web / portal |
| Stack informada | TanStack Start/React + Supabase/Postgres, na Vercel (já em produção no Hórus) |
| Fonte | `Aula 8/Entregas/Hrus-Banco-de-Demandas-...-2026-10-27.json` e `.md` (29/10/2026 08:47, horário de Cuiabá) |

## Arquivos

- `projeto.json` e `PROJETO.md`: o envio do aluno (o `.md` confere com o `.json`).
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.

## Pendências

- O módulo **já existe** no Hórus: os 5 marcos estão como "Feito". O
  `contexto.md` descreve a versão HTML monolítica e offline first pedida para
  todos os apps, com exportação compatível com as tabelas do Supabase.
  Confirmar com o aluno se essa versão é o objetivo ou se ele segue no Hórus.
- Os anexos citados (`relatorio-demandas-geral.pdf` e `tela-banco-demandas.png`)
  não vieram com o envio.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos preenchidos (estavam vazios):** `evid_detalhe`, `provas`, `piloto`, `risco_defesa`.

**Campos substituídos:**

- `frase`: o aluno marcou "não se aplica" na defesa e a stack era a do Hórus em produção; alinhado à arquitetura do curso, sem descartar o Hórus.
- `stack_detalhe`: o aluno marcou "não se aplica" na defesa e a stack era a do Hórus em produção; alinhado à arquitetura do curso, sem descartar o Hórus.
- `hospedagem_escolhida`: o aluno marcou "não se aplica" na defesa e a stack era a do Hórus em produção; alinhado à arquitetura do curso, sem descartar o Hórus.

**Tabelas:**

- telas e artefatos (`tArtefatos`): refeita. Preenchida a coluna de rota, que estava vazia, e acrescentada a tela de troca de arquivos da versão offline.
- fontes de dados (`tFontes`): refeita. O anexo de orçamento estava como "documento em papel"; é um PDF digital.
- hospedagem (`tHospedagem`): linhas acrescentadas. Acrescentada a opção da arquitetura do curso.
- marcos (`tMarcos`): linhas acrescentadas. Os 5 marcos do Hórus estão feitos; acrescentados os da versão HTML.
- referências (`tRefs`): linhas acrescentadas. Acrescentado o artigo específico do PCA.

**Marcações:**

- `stack`: era React + Supabase (produção do Hórus); alinhado à arquitetura do curso para a versão offline.
- `req`: acrescentados Funcionar offline e Integração (exportação para o Hórus).
