# Agendamento CIN

Agendamento centralizado da Carteira de Identidade Nacional (CIN) nos postos
próprios de identificação: o cidadão escolhe o posto, a data e o horário por um
link, e o posto gerencia as reservas e registra o comparecimento.

| Campo | Valor |
|---|---|
| Aluno | Elthon (o e-mail indica Teixeira; confirmar o nome completo) |
| Contato | elthonteixeira@politec.mt.gov.br |
| Unidade | Identificação Civil |
| Tipo | Aplicativo web / portal |
| Stack pedida | Google Apps Script + Google Planilhas |
| Fonte | `Aula 8/Entregas/Elthon - Agendamento-CIN-2026-10-27 (1).json` (29/10/2026 09:08, horário de Cuiabá) |

## Arquivos

- `envio-original.json`: o envio do aluno, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado (ver a seção abaixo). O
  `PROJETO.md` é gerado pelo próprio formulário.
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.

## Pendências

- Na tabela de telas, as colunas ficaram deslocadas (o objetivo está em "rota",
  o usuário em "objetivo"). Corrigido no `projeto.json` completado.
- O agendamento público precisa de uma agenda **compartilhada**, que um app só
  offline não oferece. O `contexto.md` usa o HTML monolítico servido pelo
  próprio Apps Script, com o painel do posto offline first.
- O formulário coleta CPF (opcional). O `contexto.md` mantém o CPF opcional e
  propõe guardar só os 4 últimos dígitos para a consulta da reserva.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos preenchidos (estavam vazios):** `papeis_obs`, `doc_descricao`, `doc_faltando`.

**Campos substituídos:**

- `aluno`: o nome veio sem sobrenome (completado pelo e-mail, confirmar), a duração estava ambígua, a stack ganhou o HTML monolítico e o critério de aceite estava cortado.
- `asis_duracao`: o nome veio sem sobrenome (completado pelo e-mail, confirmar), a duração estava ambígua, a stack ganhou o HTML monolítico e o critério de aceite estava cortado.
- `stack_detalhe`: o nome veio sem sobrenome (completado pelo e-mail, confirmar), a duração estava ambígua, a stack ganhou o HTML monolítico e o critério de aceite estava cortado.
- `mvp_criterio`: o nome veio sem sobrenome (completado pelo e-mail, confirmar), a duração estava ambígua, a stack ganhou o HTML monolítico e o critério de aceite estava cortado.

**Tabelas:**

- telas e artefatos (`tArtefatos`): refeita. As colunas vieram deslocadas uma posição; realinhadas, com as rotas do `contexto.md`, e acrescentadas as telas de comprovante, consulta e grade de horários.
- TO-BE (`tToBe`): linhas acrescentadas. Acrescentadas as etapas de confirmação, cancelamento e comparecimento, que estão no escopo do aluno.
- regras de negócio (`tRegras`): linhas acrescentadas. Acrescentadas regras de duplicidade, cancelamento, ausência, antecedência e retenção, que o aluno descreve nas exceções e na LGPD sem fixar valores. Os valores são propostas.
- fontes de dados (`tFontes`): refeita. O tipo vinha como "planilha digital" e similares, que não são opções do formulário; trocado por "não existe ainda" (as planilhas serão criadas) e o texto original foi para a observação.
- hospedagem (`tHospedagem`): refeita. Tipos ajustados: GitHub Pages é estática e gratuita; a hospedagem tradicional é servidor interno.
- métricas (`tMetricas`): linhas acrescentadas. Acrescentadas as métricas de cancelamento (citada no impacto) e de tempo para agendar ("o processo demora vários minutos").

**Marcações:**

- `req`: acrescentados Funcionar offline (painel do posto) e Trilha de auditoria (o aluno pede o registro das ações).
