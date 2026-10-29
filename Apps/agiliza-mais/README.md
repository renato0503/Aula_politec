# Agiliza +

Gerador em Python que automatiza a criação de laudos periciais em Word, a partir
de dados e textos padronizados, com revisão final pelo perito.

| Campo | Valor |
|---|---|
| Grupo | Diego Costa, Francineide da Silva e Andreia Cristina (enviado no formulário como "Alunos POLITEC") |
| Contato | diego.n.costa@aluno.senai.br |
| Unidade | POLITEC no geral |
| Tipo | Automação de script ou rotina |
| Plataforma | Aplicativo local no Windows |
| Fonte | Firestore, coleção `ideacao`, documento `hpZAU51V3OyVYHfkB7d1` (27/10/2026 16:41, horário de Cuiabá) |

## Arquivos

- `PROJETO.md`: gerado a partir do documento do Firestore. Os títulos das seções
  repetem os nomes dos campos gravados.
- `projeto-firestore.json`: o documento do Firestore em JSON simples. Não está
  no formato de importação do formulário.

## Pendências

- Nenhum arquivo anexado.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json` (ou `projeto-firestore.json`).
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos preenchidos (estavam vazios):** `evid_detalhe`, `papeis_obs`, `dependencias`, `stack_detalhe`, `doc_faltando`.

**Campos substituídos:**

- `doc_descricao`: alinhado à arquitetura do curso (HTML monolítico, offline first) ou movido para a tabela correta; o texto anterior está em `projeto-firestore.json`.
- `apoio`: alinhado à arquitetura do curso (HTML monolítico, offline first) ou movido para a tabela correta; o texto anterior está em `projeto-firestore.json`.
- `hospedagem_escolhida`: alinhado à arquitetura do curso (HTML monolítico, offline first) ou movido para a tabela correta; o texto anterior está em `projeto-firestore.json`.
- `mvp_plataforma`: alinhado à arquitetura do curso (HTML monolítico, offline first) ou movido para a tabela correta; o texto anterior está em `projeto-firestore.json`.

**Tabelas:**

- AS-IS (`tAsIs`): refeita. As 14 etapas estavam coladas no campo de documentos; foram movidas para a tabela sem mudar o texto.
- TO-BE (`tToBe`): refeita. As 11 etapas estavam no campo de documentos.
- telas e artefatos (`tArtefatos`): refeita. As 10 telas estavam no campo de documentos; a coluna de rota foi preenchida com as rotas do `contexto.md`.
- entidades (`tEntidades`): refeita. As 9 entidades estavam no campo de documentos.
- regras de negócio (`tRegras`): refeita. As 16 regras (RN01 a RN16) estavam no campo de documentos.
- fontes de dados (`tFontes`): refeita. As 8 fontes estavam no campo de documentos; o tipo foi ajustado às opções do formulário e o formato original foi para a observação.
- métricas (`tMetricas`): refeita. As 2 métricas estavam no campo de documentos.
- hospedagem (`tHospedagem`): refeita. As 3 opções estavam no campo de documentos; acrescentada a opção HTML único, que é a arquitetura do curso.
- marcos (`tMarcos`): refeita. Os 8 marcos estavam no campo de documentos.
- riscos (`tRiscos`): refeita. Os 8 riscos estavam colados no campo de apoio.
- referências (`tRefs`): refeita. As 2 referências estavam no campo de documentos; acrescentada a cadeia de custódia (CPP, art. 158-A), que trata do hash.
- papéis (`tPapeis`): linhas acrescentadas. Acrescentados os papéis que aparecem nas regras (quem aprova os textos e quem mede o piloto).

**Marcações:**

- `stack`: era Python; alinhado à arquitetura do curso.
- `req`: acrescentados Funcionar offline e Trilha de auditoria (o grupo pede registro das conferências).
