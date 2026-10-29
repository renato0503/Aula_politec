# Visão geral dos equipamentos no estado (Google Earth)

Cadastro de equipamentos com fotos, custos e histórico de manutenção, com
cálculo do impacto e do custo de parada por defeito, e com a localização de
cada equipamento no mapa do estado, no Google Earth.

| Campo | Valor |
|---|---|
| Aluno | João Lucas Nogueira Ponce |
| Contato | joaoponce@politec.mt.gov.br |
| Unidade | Coordenadoria de qualidade |
| Tipo | Outro |
| Plataforma | Site web (abre no navegador) |
| Fonte | `Aula 8/Entregas/...-2026-10-28 (1).json` (28/10/2026 08:44, horário de Cuiabá) |

## Arquivos

- `projeto.json`: a versão mais recente da resposta (62 campos e 12 tabelas).
  Pode ser importada no formulário para continuar a edição.
- `PROJETO.md`: o export do formulário, atualizado com os 2 campos da versão
  das 08:44 (plataforma alvo e detalhe da evidência).

## Histórico

No Firestore há 3 envios do mesmo projeto (08:24, 08:27 e 08:33). Os dois
primeiros não têm MVP, papéis nem TO-BE. Esta pasta usa a versão local das
08:44, que é posterior a todos eles.

## Pendências

- O nome do projeto foi enviado como "google heart". O resumo diz Google Earth.
- Nenhum arquivo anexado.
- O campo "dados pessoais tratados" traz um número de 11 dígitos que parece
  um CPF. Retirar no próximo envio.
- MVP, papéis, entidades, regras, telas e KPIs vieram em branco ou com "1".
  O `contexto.md` propõe o escopo, e o Sprint 0 valida com o aluno.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos preenchidos (estavam vazios):** `evid_detalhe`, `asis_inicio`, `asis_fim`, `asis_decisoes`, `asis_excecoes`, `asis_digital`, `papeis_obs`, `tobe_visao`, `tobe_mudanca`, `tobe_inalterado`, `tobe_restricao`, `tobe_piloto`, `entrega`, `dentro`, `fora`, `dependencias`, `mvp_objetivo`, `mvp_tela_inicial`, `mvp_mock`, `mvp_criterio`, `mvp_dados`, `mvp_reuso`, `mvp_naofaz`, `coletar`, `acesso`, `base_periodo`, `campos_data`, `conta_quem`, `orcamento`, `lgpd_base`, `lgpd_retencao`, `lgpd_acesso`, `restricoes`, `hipotese_campo`, `lacunas`, `frase`, `provas`, `risco_defesa`, `doc_descricao`, `doc_faltando`.

**Campos substituídos:**

- `nome_projeto`: o texto anterior estava vazio, com erro de digitação ("google heart"), com um CPF no lugar da descrição dos dados, ou com a stack Python; alinhado ao resumo do aluno e à arquitetura do curso.
- `tipo_projeto`: o texto anterior estava vazio, com erro de digitação ("google heart"), com um CPF no lugar da descrição dos dados, ou com a stack Python; alinhado ao resumo do aluno e à arquitetura do curso.
- `stack_detalhe`: o texto anterior estava vazio, com erro de digitação ("google heart"), com um CPF no lugar da descrição dos dados, ou com a stack Python; alinhado ao resumo do aluno e à arquitetura do curso.
- `hospedagem_escolhida`: o texto anterior estava vazio, com erro de digitação ("google heart"), com um CPF no lugar da descrição dos dados, ou com a stack Python; alinhado ao resumo do aluno e à arquitetura do curso.
- `lgpd_dados`: o texto anterior estava vazio, com erro de digitação ("google heart"), com um CPF no lugar da descrição dos dados, ou com a stack Python; alinhado ao resumo do aluno e à arquitetura do curso.
- `mvp_plataforma`: o texto anterior estava vazio, com erro de digitação ("google heart"), com um CPF no lugar da descrição dos dados, ou com a stack Python; alinhado ao resumo do aluno e à arquitetura do curso.

**Tabelas:**

- AS-IS (`tAsIs`): refeita. Montado a partir do problema ("não é feito acompanhamento via ferramenta"), das entradas (comprovantes de manutenção) e do impacto informados pelo aluno.
- TO-BE (`tToBe`): refeita. Montado a partir do resumo do aluno (fotos, custos, histórico, impacto e Google Earth).
- papéis (`tPapeis`): refeita. A tabela veio com "1" em todas as células.
- telas e artefatos (`tArtefatos`): refeita. A tabela veio com "1"; as telas seguem o `contexto.md`.
- entidades (`tEntidades`): refeita. A tabela veio com "1"; as entidades seguem o `contexto.md`, seção 5.
- regras de negócio (`tRegras`): refeita. A tabela veio com "1"; as regras seguem o `contexto.md`, seção 6.
- fontes de dados (`tFontes`): refeita. A tabela veio com "1".
- métricas (`tMetricas`): refeita. A tabela veio com "1".
- hospedagem (`tHospedagem`): refeita. A tabela veio com "1".
- marcos (`tMarcos`): refeita. A tabela veio com "1"; as datas seguem os sprints de 1 semana do `sprint.md`.
- riscos (`tRiscos`): refeita. A tabela veio com "1".
- referências (`tRefs`): refeita. A tabela veio com "1".

**Marcações:**

- `stack`: era Python/Flask; alinhado à arquitetura do curso.
- `req`: mantida Acessibilidade; acrescentados Funcionar offline e Impressão (relatório A4).
- `evid`: acrescentada a planilha parcial citada pelo aluno.
