# Controle de Adiantamentos

Acompanhamento do adiantamento (suprimento de fundos) da POLITEC, do pedido com
os 3 orçamentos à prestação de contas aprovada, com prazos e pendências. Não
substitui o SICAD, que continua sendo o sistema oficial.

| Campo | Valor |
|---|---|
| Alunos | Jaqueline e Linicker (sobrenomes a confirmar) |
| Contato | jaquelineaguiar@politec.mt.gov.br |
| Unidade | POLITEC (DAS) e SESP (Gabinete) |
| Tipo | Mapeamento de processo, com protótipo |
| Stack pedida | HTML único (CSS/JS inline), JSON embutido, GitHub Pages (já é a arquitetura do curso) |
| Fonte | `Aula 8/Entregas/FLUXO-DE-ADIANTAMENTO-2026-10-27 (1).json` (29/10/2026 10:18, horário de Cuiabá) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado (ver abaixo). O `PROJETO.md` é gerado pelo formulário.
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.

## Pendências

- Sete tabelas vieram com as **linhas de exemplo do próprio formulário** (a
  conferência de arma, "180 por mês", a regra da matrícula). Foram trocadas
  pelo fluxo de adiantamento descrito no resumo.
- O campo de base legal cita a Orientação Técnica nº 02/2026 da CGE/MT, e a
  tabela de referências cita a nº 06/2025. Confirmar qual vale.
- Os documentos citados (AS-IS e TO-BE em .docx, planilha de controle,
  legislação em PDF) não vieram com o envio.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos preenchidos (estavam vazios):** `papeis_obs`, `stack_detalhe`.

**Campos substituídos:**

- `tipo_projeto`: o resumo trazia o fluxo inteiro (que foi para a tabela AS-IS), a plataforma era só diagrama e o CPF saiu; os demais textos foram detalhados a partir do que os alunos escreveram.
- `mvp_plataforma`: o resumo trazia o fluxo inteiro (que foi para a tabela AS-IS), a plataforma era só diagrama e o CPF saiu; os demais textos foram detalhados a partir do que os alunos escreveram.
- `resumo`: o resumo trazia o fluxo inteiro (que foi para a tabela AS-IS), a plataforma era só diagrama e o CPF saiu; os demais textos foram detalhados a partir do que os alunos escreveram.
- `lgpd_dados`: o resumo trazia o fluxo inteiro (que foi para a tabela AS-IS), a plataforma era só diagrama e o CPF saiu; os demais textos foram detalhados a partir do que os alunos escreveram.
- `limite`: o resumo trazia o fluxo inteiro (que foi para a tabela AS-IS), a plataforma era só diagrama e o CPF saiu; os demais textos foram detalhados a partir do que os alunos escreveram.
- `mvp_objetivo`: o resumo trazia o fluxo inteiro (que foi para a tabela AS-IS), a plataforma era só diagrama e o CPF saiu; os demais textos foram detalhados a partir do que os alunos escreveram.
- `mvp_criterio`: o resumo trazia o fluxo inteiro (que foi para a tabela AS-IS), a plataforma era só diagrama e o CPF saiu; os demais textos foram detalhados a partir do que os alunos escreveram.
- `tobe_mudanca`: o resumo trazia o fluxo inteiro (que foi para a tabela AS-IS), a plataforma era só diagrama e o CPF saiu; os demais textos foram detalhados a partir do que os alunos escreveram.
- `tobe_visao`: o resumo trazia o fluxo inteiro (que foi para a tabela AS-IS), a plataforma era só diagrama e o CPF saiu; os demais textos foram detalhados a partir do que os alunos escreveram.

**Tabelas:**

- AS-IS (`tAsIs`): refeita. As 16 etapas do resumo viraram 12 linhas (pedido e prestação de contas); os prazos vêm do Decreto nº 1.487/2022 citado pelos alunos. a tabela trazia a linha de exemplo do formulário (conferência de arma); refeita com o fluxo de adiantamento descrito no resumo.
- TO-BE (`tToBe`): refeita. a tabela trazia a linha de exemplo do formulário (conferência de arma); refeita com o fluxo de adiantamento descrito no resumo.
- papéis (`tPapeis`): refeita. A tabela trazia um papel genérico; refeita com os papéis do fluxo.
- telas e artefatos (`tArtefatos`): refeita. A tabela veio com as colunas deslocadas e uma linha só; refeita com as telas do escopo descrito.
- entidades (`tEntidades`): refeita. a tabela trazia a linha de exemplo do formulário (conferência de arma); refeita com o fluxo de adiantamento descrito no resumo.
- regras de negócio (`tRegras`): refeita. Prazos do Decreto Estadual nº 1.487/2022 (arts. 10 e 14), citados pelos alunos. a tabela trazia a linha de exemplo do formulário (conferência de arma); refeita com o fluxo de adiantamento descrito no resumo.
- fontes de dados (`tFontes`): refeita. a tabela trazia a linha de exemplo do formulário (conferência de arma); refeita com o fluxo de adiantamento descrito no resumo.
- métricas (`tMetricas`): refeita. a tabela trazia a linha de exemplo do formulário (conferência de arma); refeita com o fluxo de adiantamento descrito no resumo.
- hospedagem (`tHospedagem`): refeita. A linha enviada era a de exemplo do formulário; mantida a opção HTML e acrescentado o GitHub Pages, que os alunos escolheram.
- referências (`tRefs`): linhas acrescentadas. Acrescentado o artigo que dá os prazos usados no app.

**Marcações:**

- `req`: tirados Integração (fora do MVP) e Nenhum (contradizia os demais); acrescentado Funcionar offline.
