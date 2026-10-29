# PROJETO.md — Hórus — Banco de Demandas (repositório de demandas de contratação reutilizáveis)

**Aluno ou equipe:** Iohan Camões de Albuquerque
**Unidade:** POLITEC/MT — Planejamento de Contratações (PCA)
**Contato:** iohan.camoes@gmail.com
**Projeto:** Hórus — Banco de Demandas (repositório de demandas de contratação reutilizáveis)
**Tipo de projeto:** Aplicativo web / portal
**Data:** 2026-10-27
**Resumo:** Repositório global de demandas de contratação em que cada unidade cadastra um item uma única vez (com especificação, valor, quantidade e orçamento), podendo ser reaproveitado por outras unidades da mesma Diretoria e aprovado para o ciclo orçamentário anual.

## 1. Problema (a dor)

**Problema:** As demandas de contratação ficam dispersas em planilhas por unidade, são recadastradas a cada ciclo e não há reaproveitamento entre unidades, gerando retrabalho e inconsistência de valores/especificações.
**Impacto:** Retrabalho de recadastro a cada ciclo; divergência de especificação e preço do mesmo item entre unidades; perda de histórico e de orçamentos de referência; dificuldade de consolidar valor global por grupo (custeio/investimento) e por unidade.
**Quem sofre:** Servidor da unidade, Equipe interna, Unidade parceira, Chefia
**Como é feito hoje:** Cada unidade mantém planilhas locais com itens que deseja contratar. No PCA, essas listas são reenviadas e redigitadas; especificação técnica, valor unitário e orçamento vêm em formatos distintos e muitas vezes sem anexo de referência. A consolidação por Diretoria é manual.
**Evidências:** Planilha ou controle local, Relatório de sistema, Documento ou norma oficial
**Detalhe da evidência:** Planilhas de demanda das unidades enviadas no ciclo anterior do PCA, com o mesmo item em formatos e valores diferentes; o módulo já em produção no Hórus registra o uso real.
**O que não pode ser automatizado:** A decisão de aprovar a demanda para o ciclo é da chefia (Diretor/Coordenador) — é ato de gestão e permanece humano. A redação da especificação técnica e da justificativa também é responsabilidade da unidade (requisito de qualidade mínima).

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Cadastrar uma demanda válida e aprová-la para o ciclo ativo, com relatório PDF consolidado.
**O que o MVP não faz:** Não substitui o Kanban/Acompanhamento do ciclo (apenas injeta a demanda nele); não faz cotação automática de preços.
**Entregável do projeto:** Módulo web "Banco de Demandas" integrado ao PCA do Hórus.
**Dentro do escopo:** Cadastro/edição/exclusão de demanda; anexo de PDF de orçamento; preview Open Graph de links; manifestação de interesse; aprovação para o ciclo ativo; reabrir item; relatórios PDF (Geral e Aprovadas); isolamento por Diretoria/órgão (RLS).
**Fora do escopo:** Workflow de aprovação com múltiplas etapas (o cadastro é livre; "aprovar" = copiar para o ciclo); dashboard dedicado; métrica de tempo de atendimento.
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** Grade de cards "Banco de Demandas · repositório global (N)".
**Simulado no MVP:** Um órgão/Diretoria com unidades fictícias, um ciclo ATIVO e demandas sintéticas (custeio e investimento).
**Critério de aceite:** Dado um ciclo ATIVO, ao aprovar uma demanda do banco ela aparece como APROVADO no Kanban e no relatório "Aprovadas", e o item fica marcado "Aprovada no ciclo".
**Dados de exemplo:** 10–15 demandas sintéticas (ex.: reagentes, EPIs, equipamentos de laboratório), com valores, quantidades e links de referência.
**O que já existe pronto e pode ser reaproveitado:** Autenticação, RBAC, unidades, unidades de medida, módulo de ciclos/quadros (PCA) e o gerador de PDF (jsPDF) do Hórus.
**Dependências:** Da existência de um ciclo orçamentário ativo (módulo PCA) e do cadastro de unidades/unidades de medida.

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| ADM | Administrador do sistema | Todos os órgãos/Diretorias (acesso total) | Tudo: cria, edita, exclui, aprova, gera relatórios | — | Todas as ações |
| DIRETOR | Diretor da unidade | Banco da sua Diretoria | Cria, edita qualquer card, aprova, gera relatórios | Ver outra Diretoria (salvo ADM) | Autor e aprovador |
| COORDENADOR | Coordenador | Banco da Diretoria | Cria; aprova demandas das unidades que gerencia; gera relatórios | Aprovar fora das unidades que gerencia | Autor e aprovador |
| GERENTE | Gerente de unidade | Banco da Diretoria | Cria/edita os próprios itens; manifesta interesse | Aprovar; editar item de terceiro | Autor |
| USUARIO_SETORIAL | Servidor do setor | Banco da Diretoria | Cria/edita os próprios itens; manifesta interesse | Aprovar; editar item de terceiro | Autor |
| INVENTARIANTE | Inventariante | Banco (somente leitura) | Visualiza | Criar, editar ou aprovar | — |

**Observações sobre os papéis:** Edição de um card específico é do criador (ou ADM/Diretor). Visibilidade é isolada por Diretoria dentro do órgão via RLS; ADM é global.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| banco_demandas | Item do catálogo | id:uuid; grupo:text(CUSTEIO/INVESTIMENTO); unidade_id:uuid; especificacao_tecnica:text(≥50); valor_unitario:numeric(12,2)>0; quantidade:numeric(10,3)>0; unidade_medida_id:uuid; valor_global:numeric(15,2) GENERATED; links_referencia:text[]; justificativa:text(≥100); arquivo_pdf_url:text; preview_image/title:text; criado_por:uuid; diretoria_id:uuid; orgao_id:uuid; created_at/updated_at:timestamptz | id (PK) | Dezenas a centenas | Cadastro da unidade | Sim |
| banco_demanda_inclusoes | Em quais ciclos o item entrou | id:uuid; banco_demanda_id:uuid; quadro_id:uuid; demanda_id:uuid (ON DELETE SET NULL); criado_por:uuid; orgao_id:uuid; created_at:timestamptz | id (PK); unique(banco_demanda_id, quadro_id) | 1 por ciclo | Aprovação | Sim |
| banco_demanda_manifestacoes | Interesse de outra unidade | id:uuid; banco_demanda_id:uuid; unidade_id:uuid; quantidade:numeric(10,3)>0; justificativa:text(≥50); criado_por:uuid; orgao_id:uuid; diretoria_id:uuid; created_at:timestamptz | id (PK); unique(banco_demanda_id, unidade_id) | Poucas por item | Outra unidade | Sim |

**O que precisa ser coletado:** Nada novo para o MVP — tudo é sintético, gerado no exercício.
**Quem libera o acesso:** Administrador do Hórus (perfis/RBAC) e habilitação do módulo PCA para o órgão.

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| banco_demandas | Banco de dados | Supabase (Postgres) | Sim | Uma demanda de contratação | Dezenas a centenas | created_at / updated_at | A cada cadastro | Duvidaso |
| banco_demanda_inclusoes | Banco de dados | Supabase (Postgres) | Sim | Vínculo entre item e ciclo | 1 por ciclo | created_at | A cada aprovação | Não |
| banco_demanda_manifestacoes | Banco de dados | Supabase (Postgres) | Sim | Interesse de uma unidade em um item | Poucas por item | created_at | A cada adesão | Duvidaso |
| demandas (ciclo) | Banco de dados | Supabase (Postgres) | Sim | Demanda no Kanban do ciclo | — | created_at | A cada aprovação | Não |
| Storage demandas-docs | Banco de dados | Supabase Storage (bucket) | Sim | PDF de orçamento | 1 por demanda | — | A cada upload | Não |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| R1 | Especificação técnica ≥ 50 caracteres | No cadastro/edição | — | Formulário + check no banco | Validação |
| R2 | Justificativa ≥ 100 caracteres | No cadastro/edição | — | Formulário + check no banco | Validação |
| R3 | valor_unitario > 0 e quantidade > 0 | No cadastro | — | Formulário + check no banco | Validação |
| R4 | valor_global = valor_unitario × quantidade | Sempre | — | Coluna GENERATED (banco) | Cálculo |
| R5 | Pelo menos 1 link de referência iniciando com http | No cadastro | — | Formulário | Validação |
| R6 | PDF de orçamento ≤ 10 MB | No upload | Anexo é opcional | Formulário/Storage | Validação |
| R7 | Aprovar exige ciclo orçamentário ATIVO | Na aprovação | — | Serviço (buscarCicloAtivo) | Negócio |
| R8 | Editar card: só o criador (ou ADM/Diretor) | Na edição | ADM/Diretor | RLS + interface | Acesso |
| R9 | Manifestação: só de outra unidade, 1 por unidade | Na manifestação | — | RLS + restrição unique | Negócio |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/banco | Grade de cards | Ver o repositório | Todos (conforme RLS) | Itens da Diretoria | Navegar/filtrar | Isolamento por Diretoria | Tela | Card aparece na grade | Sim |
| #/demanda/nova | Formulário "Nova Demanda" | Cadastrar item | Servidor/Gerente | Especificação, valor, quantidade, links, PDF | Salvar | Validações mínimas (R1–R6) | Tela | Item criado e visível no card | Sim |
| #/demanda/:id/interesse | Manifestar interesse | Aderir a item de outra unidade | Outra unidade | Quantidade + justificativa | Salvar | 1 manifestação por unidade | Tela | Interesse listado no card | Sim |
| #/aprovar | Aprovar demanda | Injetar a demanda no ciclo | Diretor/Coordenador | Item + ciclo ativo | Aprovar | Exige ciclo ATIVO | Ação | Demanda APROVADO aparece no Kanban | Sim |
| #/relatorios | Relatório PDF | Consolidar demandas | Coordenador/Diretor/ADM | KPIs + ficha por demanda | Gerar PDF | — | Relatório | PDF baixado | Sim |
| #/trocar | Troca de arquivos | Levar as demandas entre unidade, diretoria e Hórus | Todos | Demandas, catálogo, manifestações, aprovações | Exportar e importar | Recusar arquivo de outra diretoria | Integração | Arquivo importado no Hórus mostra a demanda no Kanban | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Total de demandas | Quantas demandas há? | count(banco_demandas) | banco_demandas | 0 | Crescente | Contar os cards |
| Valor global total | Quanto somam as demandas? | Σ valor_global | banco_demandas | R$ 0 | — | Somatório no relatório |
| Valor por grupo | Custeio vs. Investimento? | Σ valor_global por grupo | banco_demandas | — | — | KPI do PDF |
| Demandas aprovadas | Quantas entraram no ciclo? | count(inclusões ativas) | banco_demanda_inclusoes | 0 | ≥ 1 no teste | Relatório "Aprovadas" |
| Unidades distintas | Quantas unidades participam? | count(distinct unidade) | banco_demandas | — | — | KPI do PDF |
| Reuso (manifestações) | Houve reaproveitamento? | count(manifestações) | banco_demanda_manifestacoes | 0 | ≥ 1 no teste | Contar no card |

**Período da linha de base:** Um ciclo (exercício), com 10–15 demandas sintéticas.
**Campos de data e tempo que existem:** created_at e updated_at nas três tabelas; created_at nas inclusões e manifestações.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** Versão HTML monolítica: um único index.html com IndexedDB, troca por arquivo .json entre unidade e diretoria e exportação no formato das tabelas do Hórus (banco_demandas, banco_demanda_inclusoes, banco_demanda_manifestacoes). O módulo em produção continua em TanStack Start/React + Supabase/Postgres.
**Hospedagem:** Arquivo HTML único, aberto por duplo clique ou na pasta de rede da diretoria, sem servidor. O Hórus (Vercel + Supabase) continua como registro oficial e recebe o arquivo exportado.
**Custo e licenças:** Planos atuais de Vercel e Supabase do projeto; sem licenças adicionais para o MVP.
**Contas e domínio:** Equipe do Hórus (administração do projeto).

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| Vercel + Supabase | Plataforma como serviço | Nuvem | Plano atual do projeto | Equipe Hórus | Web autenticado | Supabase/Postgres | Boa | Dependência de nuvem |
| Servidor próprio | Servidor interno | Datacenter do órgão | Custo de infraestrutura | TI do órgão | Rede interna | Postgres local | Média | Mais operação |
| Arquivo HTML único | Arquivo local | Computador ou pasta de rede da diretoria | Zero | Equipe Hórus | Quem abre o arquivo | IndexedDB do navegador | Uma base por diretoria | Isolamento por diretoria depende de não repassar os arquivos |


## 9. Restrições e LGPD

**Restrições:** Isolamento obrigatório por Diretoria/órgão (RLS); aprovação exige ciclo ativo; PDF ≤ 10 MB; edição restrita ao criador.
**Dados pessoais tratados:** Apenas identificação do servidor autor (vínculo criado_por → perfil). Sem dado pessoal sensível. No exercício, usar dados sintéticos.
**Base legal:** Execução de política pública de planejamento de contratações (PCA). Finalidade: registrar e consolidar demandas de contratação do órgão.
**Retenção:** Vinculado ao ciclo de planejamento/execução orçamentária (anual, conforme norma do órgão).
**Acesso e registro:** Acesso por perfil (RBAC) e isolamento por Diretoria/órgão (RLS). Registra-se autor (criado_por) e aprovador (aprovado_por na demanda do ciclo).
**Requisitos marcados:** Funcionar offline, Integração com sistema oficial, LGPD e dado pessoal, Segurança e controle de acesso, Trilha de auditoria

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Unidade identifica a necessidade de um item/serviço para o ano.
**Fim:** Item consolidado (ou não) no PCA da Diretoria.
**Entradas:** Necessidade da unidade, especificação, estimativa de preço, orçamentos.
**Saídas:** Lista de demandas por unidade, consolidada manualmente por Diretoria.
**Volume:** Dezenas a centenas de itens por ciclo, por Diretoria.
**Duração:** Dias a semanas (coleta + consolidação manual).
**Frequência:** Por demanda
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Levantar necessidade | Servidor da unidade | Necessidade | Lista itens em planilha | Planilha local | Planilha | — | — | 4 | Sim, com regra clara |
| Cotar preço | Servidor | Item | Pesquisa preço/orçamento | Valor + PDF | E-mail/planilha | Mínimo de 1 orçamento | Fornecedores | 8 | Sim, com apoio humano |
| Enviar à chefia | Servidor | Planilha | Envia por e-mail | E-mail | E-mail | — | Caixa da chefia | 1 | Sim, com regra clara |
| Consolidar | Coordenador/Diretor | Planilhas de várias unidades | Junta e padroniza | Lista da Diretoria | Planilha | Agrupar por grupo (custeio/investimento) | — | 6 | Sim, com regra clara |
| Aprovar para o ciclo | Diretor/Coordenador | Lista consolidada | Decide o que entra | Demandas aprovadas | Planilha | Ciclo ativo | — | 2 | Não |

**Decisões e aprovações:** Aprovação da chefia (Diretor/Coordenador) sobre o que entra no ciclo.
**Exceções:** Itens duplicados entre unidades; itens sem orçamento; itens que mudam de valor entre ciclos.
**Já digitalizado:** Planilhas e e-mails (sem base de dados única nem reaproveitamento).

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Toda demanda é cadastrada uma vez num banco único, reaproveitável e rastreável, e aprovada para o ciclo com um clique.
**Mudança principal:** Sai a planilha dispersa; entra um repositório com validação, anexo de orçamento, preview de links, manifestação de interesse entre unidades e aprovação que injeta a demanda direto no ciclo (Kanban/PTA).
**O que fica igual:** A decisão de aprovação continua humana (chefia); a especificação/justificativa continua sendo escrita pela unidade.
**O que não pode mudar:** Isolamento por Diretoria/órgão (LGPD/segregação); exigência de ciclo ativo para aprovar; rastreabilidade de autor e aprovador.
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Cadastrar demanda | Formulário validado + PDF + preview de link | A pessoa assistida pela máquina | Padronização, sem recadastro | Baixo |
| Disponibilizar no banco | Card no repositório da Diretoria | A máquina (automação) | Reuso e transparência | Baixo |
| Manifestar interesse | Outra unidade adere (quantidade + justificativa) | A pessoa assistida pela máquina | Elimina item duplicado | Baixo |
| Aprovar para o ciclo | 1 clique cria a demanda APROVADO no ciclo | A pessoa assistida pela máquina | Entrada direta no PTA | Baixo |
| Acompanhar | Demanda vai ao Kanban do ciclo | A pessoa assistida pela máquina | Rastreio ponta a ponta | Médio |

**Piloto do TO-BE:** Em ambiente do Hórus com um ciclo orçamentário ATIVO: cadastrar uma demanda, manifestar interesse por outra unidade e aprovar; conferir que surge no Kanban como APROVADO e no relatório "Aprovadas".

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** Centralizar e reaproveitar demandas reduz recadastro e divergência de preço/especificação entre unidades.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Lei nº 14.133/2021 (Nova Lei de Licitações) | Norma ou lei | planalto.gov.br | 2021 | Exigência de planejamento e do PCA | Fundamenta o PCA | Sim |
| Norma interna de PCA do órgão | Documento interno | POLITEC/MT | — | Fluxo de consolidação | Base do AS-IS | Não |
| Lei nº 14.133/2021, art. 12, VII (plano de contratações anual) | Norma ou lei | planalto.gov.br | 2021 | Os órgãos podem elaborar o plano de contratações anual | Fundamentar o ciclo do PCA | Não |

**Lacunas:** Exercício com dados sintéticos; não mede tempo de atendimento; não cobre integração com sistemas externos de compras.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Modelo de dados (3 tabelas + RLS) |  | Equipe | Supabase | Feito |
| Tela + formulário de cadastro |  | Equipe | Modelo de dados | Feito |
| Manifestação de interesse |  | Equipe | Tela | Feito |
| Aprovação → ciclo |  | Equipe | Módulo PCA | Feito |
| Relatório PDF |  | Equipe | Dados | Feito |
| Versão HTML: cadastro, grade e ficha | Semana 3 | Iohan | Esquema das tabelas do Hórus | Planejado |
| Versão HTML: troca de arquivos e manifestação | Semana 5 | Iohan | Cadastro | Planejado |
| Versão HTML: aprovação e exportação para o Hórus | Semana 7 | Iohan | Ciclo ativo | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Aprovar sem ciclo ativo | Média | Alto | Bloqueio por buscarCicloAtivo |
| Vazamento entre Diretorias | Baixa | Alto | RLS (órgão + Diretoria) |
| Item sem orçamento/qualidade baixa | Média | Médio | Validações mínimas (especificação, justificativa, links) |
| PDF grande demais | Baixa | Baixo | Limite de 10 MB + envio alternativo |

**Apoio necessário:** Administração do Hórus para habilitar o módulo PCA e criar um ciclo de teste.
**Aprendizado necessário:** RLS do Postgres e integração do banco de demandas com o Kanban do ciclo.

# Anexo D — A defesa

**Frase de defesa:** Se cada demanda for cadastrada uma vez e reaproveitada pelas unidades da diretoria, o PCA deixa de ser redigitado a cada ciclo e o mesmo item passa a ter uma só especificação e um só preço de referência.
**Provas:** 1) O mesmo item chega com especificação e preço diferentes de unidades distintas (planilhas do ciclo anterior). 2) O PCA é obrigatório pela Lei nº 14.133/2021, art. 12, VII. 3) O teste com 15 demandas sintéticas mostra o cadastro único, a manifestação de interesse e a aprovação para o ciclo.
**Piloto:** Um ciclo de teste com uma diretoria e 4 unidades: cada unidade cadastra suas demandas, uma unidade manifesta interesse no item de outra e o diretor aprova; o arquivo exportado é importado no Hórus e a demanda aparece como APROVADO no Kanban.
**Maior risco:** Duas bases (Hórus e versão offline) divergirem. Mitigação: a versão offline exporta no formato das tabelas do Hórus, e o Hórus continua sendo o registro oficial do ciclo.

# Anexo E — Documentos enviados

**Descrição dos documentos:** relatorio-demandas-geral.pdf: exemplo de relatório gerado pelo módulo · tela-banco-demandas.png: print da grade de cards
**O que ainda falta:** Dados sintéticos empacotados e prints da tela.
