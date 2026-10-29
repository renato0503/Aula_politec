# Registro de Não Conformidade (RNC)

Acompanhamento das RNCs com os setores no centro: cada setor relator e
notificado vê e cumpre a sua parte, e a CQUAL passa de executora a apoio e
monitoramento, com indicadores de recorrência.

| Campo | Valor |
|---|---|
| Aluna | Sabrina Ellen (GitHub: `Sabrinaelllen1209`) |
| Contato | sabrinasilva@politec.mt.gov.br |
| Unidade | CQUAL (Coordenadoria da Qualidade) |
| Tipo | Formulário ou modelo de coleta, com painel |
| Stack pedida | Ainda não definida (o fluxo atual usa Forms, Sheets, Trello e Autocrat) |
| Fonte | `Aula 8/Entregas/Fluxo-elaborao-de-Registro-de-no-conformidade-2026-10-27 (1).json` (29/10/2026 09:46, horário de Cuiabá) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado (ver abaixo).
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.

## Pendências

- A própria aluna listou o que faltava (TO-BE, MVP, entidades, regras,
  métricas, hospedagem e hipótese). Foi completado com propostas.
- A tabela de telas veio com as colunas deslocadas.
- O formulário atual coleta o nome de quem causou a não conformidade. A aluna
  informa que isso já está sendo trocado pelo setor. O app registra só o setor.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos preenchidos (estavam vazios):** `fora`, `tobe_restricao`, `tobe_piloto`, `mvp_mock`, `base_periodo`, `stack_detalhe`, `hospedagem_escolhida`, `conta_quem`, `orcamento`, `restricoes`, `hipotese_campo`, `lacunas`, `apoio`, `lgpd_base`.

**Campos substituídos:**

- `aluno`: o envio trazia só o primeiro nome; o sobrenome vem do e-mail e precisa ser confirmado.
- `tobe_mudanca`: a aluna listou estes campos como faltando ou os preencheu com o fluxo atual; completados a partir do impacto e da visão TO-BE que ela escreveu.
- `entrega`: a aluna listou estes campos como faltando ou os preencheu com o fluxo atual; completados a partir do impacto e da visão TO-BE que ela escreveu.
- `dentro`: a aluna listou estes campos como faltando ou os preencheu com o fluxo atual; completados a partir do impacto e da visão TO-BE que ela escreveu.
- `mvp_objetivo`: a aluna listou estes campos como faltando ou os preencheu com o fluxo atual; completados a partir do impacto e da visão TO-BE que ela escreveu.
- `mvp_plataforma`: a aluna listou estes campos como faltando ou os preencheu com o fluxo atual; completados a partir do impacto e da visão TO-BE que ela escreveu.
- `mvp_criterio`: a aluna listou estes campos como faltando ou os preencheu com o fluxo atual; completados a partir do impacto e da visão TO-BE que ela escreveu.
- `mvp_naofaz`: a aluna listou estes campos como faltando ou os preencheu com o fluxo atual; completados a partir do impacto e da visão TO-BE que ela escreveu.
- `dependencias`: a aluna listou estes campos como faltando ou os preencheu com o fluxo atual; completados a partir do impacto e da visão TO-BE que ela escreveu.
- `lgpd_dados`: a aluna listou estes campos como faltando ou os preencheu com o fluxo atual; completados a partir do impacto e da visão TO-BE que ela escreveu.
- `lgpd_retencao`: a aluna listou estes campos como faltando ou os preencheu com o fluxo atual; completados a partir do impacto e da visão TO-BE que ela escreveu.
- `lgpd_acesso`: a aluna listou estes campos como faltando ou os preencheu com o fluxo atual; completados a partir do impacto e da visão TO-BE que ela escreveu.

**Tabelas:**

- TO-BE (`tToBe`): refeita. A tabela veio vazia; montada a partir da visão TO-BE da aluna ("cada um fará seu papel").
- telas e artefatos (`tArtefatos`): refeita. As colunas vieram deslocadas; realinhadas e com rotas.
- entidades (`tEntidades`): refeita. A tabela veio vazia; a numeração DIRETORIA/ANO-SEQUENCIAL é a informada pela aluna.
- regras de negócio (`tRegras`): refeita. A tabela veio vazia; os prazos (5 e 30 dias) e a corregedoria vêm das exceções descritas pela aluna.
- métricas (`tMetricas`): refeita. A métrica enviada só tinha o nome; completadas com a dor descrita ("todas as demandas voltam para o setor").
- hospedagem (`tHospedagem`): refeita. A tabela veio vazia.
- marcos (`tMarcos`): refeita. A tabela veio vazia.
- riscos (`tRiscos`): refeita. A mitigação estava vazia; acrescentados dois riscos.
- referências (`tRefs`): refeita. A tabela veio vazia.

**Marcações:**

- `stack`: estava como Ainda não definido.
- `req`: a aluna marcou Nenhum, mas descreve dados sensíveis; ajustado.
