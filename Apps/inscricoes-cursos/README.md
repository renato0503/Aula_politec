# Gestão Dinâmica de Inscrições em Cursos

Fluxo padronizado de inscrição em capacitações da POLITEC: o servidor se
inscreve, recebe o comprovante "em análise", a diretoria faz a triagem (titular
e reserva) e a Gerência de Formação comunica a convocação.

| Campo | Valor |
|---|---|
| Aluna | Edilaura Rondon |
| Contato | capacitacao@politec.mt.gov.br |
| Unidade | Gerência de Formação Inicial e Continuada |
| Tipo | Aplicativo para cidadão, servidor ou equipe |
| Plataforma pedida | Planilha com automação (Forms + Power Automate) |
| Fonte | `Aula 8/Entregas/Edilaura - ...-2026-10-27 (2).json` (29/10/2026 08:56, horário de Cuiabá) |

## Arquivos

- `projeto.json`: resposta do formulário. Pode ser importada para continuar a edição.
- `PROJETO.md`: gerado pelo próprio formulário a partir do `.json` (a aluna
  enviou só o `.json`).
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.

## Pendências

- Parte das métricas, da linha de base, da hospedagem e da defesa fala de
  "transações financeiras", "clientes", CNPJ e Render/Supabase. Esses trechos
  não descrevem o processo de inscrição e foram desconsiderados no `contexto.md`.
- O projeto coleta **CPF** dos servidores. O `contexto.md` propõe usar a
  matrícula como chave e não coletar CPF (minimização, LGPD art. 6º, III).
- O entregável descrito é documentação + Forms. A arquitetura do curso troca
  isso por um app HTML monolítico (ver `contexto.md`, seção 3).

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos preenchidos (estavam vazios):** `stack_detalhe`, `lacunas`, `doc_faltando`.

**Campos substituídos:**

- `base_periodo`: o texto enviado falava de transações financeiras, clientes, CNPJ ou Render/Supabase, que não são deste processo; reescrito a partir do AS-IS e do MVP da aluna.
- `campos_data`: o texto enviado falava de transações financeiras, clientes, CNPJ ou Render/Supabase, que não são deste processo; reescrito a partir do AS-IS e do MVP da aluna.
- `hospedagem_escolhida`: o texto enviado falava de transações financeiras, clientes, CNPJ ou Render/Supabase, que não são deste processo; reescrito a partir do AS-IS e do MVP da aluna.
- `conta_quem`: o texto enviado falava de transações financeiras, clientes, CNPJ ou Render/Supabase, que não são deste processo; reescrito a partir do AS-IS e do MVP da aluna.
- `orcamento`: o texto enviado falava de transações financeiras, clientes, CNPJ ou Render/Supabase, que não são deste processo; reescrito a partir do AS-IS e do MVP da aluna.
- `restricoes`: o texto enviado falava de transações financeiras, clientes, CNPJ ou Render/Supabase, que não são deste processo; reescrito a partir do AS-IS e do MVP da aluna.
- `hipotese_campo`: o texto enviado falava de transações financeiras, clientes, CNPJ ou Render/Supabase, que não são deste processo; reescrito a partir do AS-IS e do MVP da aluna.
- `apoio`: o texto enviado falava de transações financeiras, clientes, CNPJ ou Render/Supabase, que não são deste processo; reescrito a partir do AS-IS e do MVP da aluna.
- `aprendizado`: o texto enviado falava de transações financeiras, clientes, CNPJ ou Render/Supabase, que não são deste processo; reescrito a partir do AS-IS e do MVP da aluna.
- `frase`: o texto enviado falava de transações financeiras, clientes, CNPJ ou Render/Supabase, que não são deste processo; reescrito a partir do AS-IS e do MVP da aluna.
- `provas`: o texto enviado falava de transações financeiras, clientes, CNPJ ou Render/Supabase, que não são deste processo; reescrito a partir do AS-IS e do MVP da aluna.
- `piloto`: o texto enviado falava de transações financeiras, clientes, CNPJ ou Render/Supabase, que não são deste processo; reescrito a partir do AS-IS e do MVP da aluna.
- `risco_defesa`: o texto enviado falava de transações financeiras, clientes, CNPJ ou Render/Supabase, que não são deste processo; reescrito a partir do AS-IS e do MVP da aluna.
- `lgpd_dados`: o CPF saiu (minimização, LGPD art. 6º, III) e a plataforma passou de planilha para o app HTML pedido para todos os projetos.
- `mvp_plataforma`: o CPF saiu (minimização, LGPD art. 6º, III) e a plataforma passou de planilha para o app HTML pedido para todos os projetos.
- `entrega`: a aluna previa Forms e Power Automate e excluía "desenvolver um sistema"; ajustado ao app HTML pedido para todos os projetos, mantendo o restante do escopo.
- `fora`: a aluna previa Forms e Power Automate e excluía "desenvolver um sistema"; ajustado ao app HTML pedido para todos os projetos, mantendo o restante do escopo.
- `mvp_mock`: a aluna previa Forms e Power Automate e excluía "desenvolver um sistema"; ajustado ao app HTML pedido para todos os projetos, mantendo o restante do escopo.
- `doc_descricao`: o texto colado foi separado e movido para a tabela de telas e artefatos.

**Tabelas:**

- AS-IS (`tAsIs`): refeita. A aluna enviou 1 etapa que resumia o processo; as 6 etapas vêm do campo "como é feito hoje", das decisões e das exceções que ela descreveu. A etapa com 36 h é a espera informada.
- TO-BE (`tToBe`): refeita. A linha única enviada foi dividida em 5 etapas, com o mesmo conteúdo.
- papéis (`tPapeis`): linhas acrescentadas. Acrescentado o papel do servidor, que aparece nas telas e no critério de aceite.
- telas e artefatos (`tArtefatos`): refeita. Os 7 artefatos estavam colados sem separação no campo de documentos; foram separados sem mudar o conteúdo (Forms e planilha trocados pelas telas do app).
- entidades (`tEntidades`): refeita. A aluna enviou 1 linha genérica; as entidades vêm dos campos do formulário de inscrição e das etapas descritas.
- regras de negócio (`tRegras`): refeita. A aluna enviou a regra "001 CPF"; o CPF saiu (minimização) e as regras vêm das decisões e exceções que ela descreveu.
- fontes de dados (`tFontes`): refeita. A linha enviada foi detalhada e acrescentadas as fontes citadas pela aluna (e-mails e SEAP).
- métricas (`tMetricas`): refeita. As métricas enviadas eram de outro projeto (cadastro de clientes, HTTP 400); substituídas pelas métricas do gargalo descrito pela aluna.
- hospedagem (`tHospedagem`): refeita. A tabela enviada estava colada numa célula e falava de localhost e SQLite; refeita com a proposta da aluna (Forms) e a arquitetura do curso.
- marcos (`tMarcos`): refeita. A tabela veio vazia; as datas seguem o `sprint.md`.
- riscos (`tRiscos`): refeita. A tabela veio vazia.
- referências (`tRefs`): refeita. A tabela veio vazia.

**Marcações:**

- `stack`: era Planilha com automação; alinhado à arquitetura do curso.
- `req`: acrescentado Funcionar offline.
