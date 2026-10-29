# Monitoramento de Metas pelo BI

Lê o relatório mensal do Power BI 1 (laudos pendentes), confere os números e
gera a planilha que alimenta o Power BI de monitoramento, no lugar da digitação
manual.

| Campo | Valor |
|---|---|
| Aluna | Karine Assunção |
| Contato | karineassuncao@politec.mt.gov.br |
| Unidade | CQUAL (Núcleo de Informações, NIINS) |
| Tipo | Automação de script ou rotina |
| Stack pedida | Power BI + Google Planilhas, com OCR do PDF |
| Fonte | `Aula 8/Entregas/Automao-do-monitoramento-de-metas-pelo-BI-2026-10-27.json` (29/10/2026 10:14, horário de Cuiabá) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado (ver abaixo).
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.

## Pendências

- O formato do PDF do Power BI 1 não veio com o envio. Sem uma amostra (com
  números fictícios), o leitor é escrito sobre um formato suposto.
- Confirmar se o Power BI 1 permite **Exportar dados** (CSV ou Excel) nos
  visuais. Se permitir, o OCR deixa de ser necessário e o risco principal da
  defesa (erro de reconhecimento) some.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos preenchidos (estavam vazios):** `mvp_plataforma`, `doc_descricao`.

**Campos substituídos:**

- `aluno`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `contato`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `dentro`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `entrega`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `mvp_tela_inicial`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `mvp_criterio`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `mvp_dados`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `mvp_mock`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `hospedagem_escolhida`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `lgpd_dados`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `stack_detalhe`: a stack marcada era Power BI; o Power BI continua como fonte e destino, e o app faz a ponte entre os dois.

**Tabelas:**

- AS-IS (`tAsIs`): refeita. A aluna informou 8 h no total; dividido pelas etapas descritas (consulta, digitação, conferência). Os tempos por etapa são estimativa.
- TO-BE (`tToBe`): refeita. A linha única foi dividida nas etapas da visão TO-BE.
- papéis (`tPapeis`): refeita. A tabela trazia um papel genérico.
- telas e artefatos (`tArtefatos`): refeita. A tabela veio com uma linha deslocada.
- entidades (`tEntidades`): refeita. A entidade enviada só tinha a coluna data.
- regras de negócio (`tRegras`): linhas acrescentadas. Acrescentadas as conferências citadas no AS-IS.
- fontes de dados (`tFontes`): refeita. Detalhada a fonte e acrescentada a planilha de destino.
- métricas (`tMetricas`): refeita. A métrica enviada só tinha a pergunta.
- hospedagem (`tHospedagem`): refeita. A linha enviada só tinha o tipo; acrescentada a opção que a aluna citou nas lacunas.
- marcos (`tMarcos`): refeita. O marco enviado era um risco; movido para a tabela de riscos.
- riscos (`tRiscos`): refeita. A tabela veio vazia.
- referências (`tRefs`): linhas acrescentadas. Acrescentada a alternativa ao OCR.

**Marcações:**

- `stack`: era Power BI; o Power BI continua como fonte e destino.
- `req`: acrescentados Trilha de auditoria (correções) e Funcionar offline.
