# PROJETO.md — Controle do processo de aquisição

**Aluno ou equipe:** Kasteline Gonçalves
**Unidade:** Aquisição
**Contato:** kastelinesilva@politec.mt.gov.br
**Projeto:** Controle do processo de aquisição
**Tipo de projeto:** Painel de Business Intelligence (dashboard)
**Data:** 2026-10-27
**Resumo:** Criar o número do processo no SIGADOC e no SIAG

## 1. Problema (a dor)

**Problema:** A falta de controle no processo de aquisição pode gerar atrasos, compras inadequadas, custos excessivos
**Impacto:** jurídicas e na correção de pendências pode prolongar as contratações e comprometer o atendimento das demandas institucionais. Além disso, inconsistências nos documentos, como DFD, ETP e TR, podem gerar devoluções e retrabalho, enquanto falhas na pesquisa de preços podem comprometer a estimativa de custos e a economicidade da contratação. Esses impactos devem ser comprovados por evidências, como os registros de tramitação no SIGADOC e no SIAG, o histórico de devoluções e correções, os pareceres técnicos e jurídicos e a comparação entre os preços estimados e os contratados
**Quem sofre:** Equipe interna
**Como é feito hoje:** Na prática, o processo de aquisição da POLITEC começa com a identificação da necessidade pela unidade requisitante, seguida da elaboração do DFD e da assinatura do diretor-geral. Depois, são elaborados o ETP, a análise de riscos, quando aplicável, e o TR. Em seguida, realiza-se a pesquisa de preços em plataformas como o Compras.gov.br, formaliza-se o processo no SIGADOC e no SIAG, verifica-se a disponibilidade orçamentária e providenciam-se as análises técnicas e jurídicas necessárias. Por fim, define-se a modalidade de contratação, por licitação ou contratação direta, conforme a legislação. O tempo costuma se perder na elaboração e revisão dos documentos, na coleta e validação de preços, nas assinaturas, nas análises dos setores envolvidos e na correção de pendências processuais.
**Evidências:** Planilha ou controle local
**Detalhe da evidência:** Planilha de conferência controle de processos.
**O que não pode ser automatizado:** A decisão final deve permanecer com os agentes públicos responsáveis.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Validar um fluxo padronizado de aquisição na POLITEC, com controle de etapas, documentos, responsáveis, prazos e pendências, reduzindo o retrabalho e melhorando a rastreabilidade do processo.
**O que o MVP não faz:** -
**Entregável do projeto:** O entregável final é um processo de aquisição padronizado e automatizado para a POLITEC, com fluxo de etapas definido, documentos organizados, responsabilidades estabelecidas, aprovações rastreáveis e acompanhamento de prazos e pendências, visando reduzir o tempo de tramitação, o retrabalho e as falhas processuais.
**Dentro do escopo:** O escopo contempla o mapeamento, a padronização e a automatização do processo de aquisição da POLITEC, desde a identificação da necessidade pela unidade requisitante até a definição da modalidade de contratação. Inclui a formalização da demanda (DFD), a elaboração do ETP, do TR e da análise de riscos, quando aplicável, a pesquisa de preços, a verificação orçamentária, a instrução processual nos sistemas SIGADOC e SIAG, as análises técnicas e jurídicas, as aprovações necessárias e o acompanhamento de prazos, responsáveis e pendências, visando reduzir o retrabalho, aumentar a transparência e melhorar o controle das aquisições.
**Fora do escopo:** Ficam fora do escopo inicial a execução completa de licitações e contratações diretas, a gestão e fiscalização de contratos, a substituição dos sistemas oficiais SIGADOC e SIAG, a integração automática com todas as plataformas governamentais e a tomada de decisões técnicas, jurídicas e administrativas pela ferramenta. Esses itens ficam de fora para manter o MVP viável, reduzir a complexidade da implementação, respeitar as competências dos servidores e validar primeiro o controle do fluxo, dos documentos, dos prazos e das pendências do processo de aquisição da POLITEC.
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** A primeira tela é um painel de controle de aquisições da POLITEC, com a lista de processos em andamento, suas etapas, responsáveis, prazos, status das aprovações e pendências, além da opção de iniciar uma nova solicitação de aquisição.
**Simulado no MVP:** No MVP, será simulado o fluxo de aquisição da POLITEC desde a identificação da necessidade até a instrução processual e definição da modalidade de contratação, incluindo o preenchimento do DFD, a elaboração do ETP e do TR, a pesquisa de preços, as etapas de aprovação, a verificação de pendências e o acompanhamento de prazos e responsáveis, sem integração real com o SIGADOC e o SIAG ou execução efetiva da contratação.
**Critério de aceite:** O MVP será considerado funcional quando permitir registrar e acompanhar um processo de aquisição da POLITEC do início ao fim do fluxo proposto, visualizar as etapas, os documentos, os responsáveis, os prazos e as pendências, registrar as aprovações e identificar etapas incompletas, garantindo a rastreabilidade das ações e a redução de falhas e retrabalho durante os testes com os usuários.
**Dados de exemplo:** -
**O que já existe pronto e pode ser reaproveitado:** Podem ser reaproveitados os modelos institucionais de DFD, ETP, TR e análise de riscos da POLITEC, os procedimentos e fluxos de aquisição já utilizados, as normas e orientações legais aplicáveis, os registros de processos anteriores, as pesquisas de preços e os sistemas existentes, como SIGADOC e SIAG. Também podem ser aproveitados os critérios de aprovação, as responsabilidades dos setores e os documentos padronizados, reduzindo o esforço de desenvolvimento do MVP e garantindo maior aderência à rotina institucional.
**Dependências:** Liberação da TI

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| Unidade requisitante | Setor que identifica a necessidade | O processo e as pendências | Justifica a demanda e faz o DFD | Decidir a modalidade ou assinar | Número do processo e DFD |
| Equipe de planejamento | Servidores da aquisição | DFD, ETP, risco e TR | Elabora e revisa os documentos | Aprovar as análises jurídica e técnica | Versões e anexos |
| Setor de compras | Equipe de aquisições | Processo, documentos e preços | Instrui o processo e formaliza no SIGADOC e no SIAG | Decidir o mérito | Tramitação e pendências |
| Análises técnica, orçamentária e jurídica | Setores competentes | Documentos da sua área | Emite parecer | Assinar pela autoridade | Pareceres e datas |
| Diretor-geral e autoridades | Autoridades competentes | Processo instruído | Aprova e assina | Delegar a decisão ao sistema | Aprovações |

**Observações sobre os papéis:** Os papéis devem ter responsabilidades bem definidas, com acesso às informações e aos documentos conforme suas atribuições e permissões. A unidade requisitante é responsável por justificar a necessidade; a equipe de planejamento, por elaborar os documentos; o setor de compras, por conduzir a instrução processual; os setores técnico, orçamentário e jurídico, por realizar as análises de sua competência; e o diretor-geral e demais autoridades competentes, pelas aprovações cabíveis. A automação deve facilitar a comunicação, o acompanhamento de prazos e a rastreabilidade das ações, sem substituir a responsabilidade dos agentes públicos pelas decisões e aprovações

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| Processo | Processo de aquisição da POLITEC | id_processo; numero_sigadoc; numero_siag; objeto; unidade; responsavel; data_abertura; prazo_dias; etapa; status | id_processo | 10 no exemplo | Cadastro do app | Sim |
| Documento | DFD, ETP, análise de riscos, TR e pesquisa de preços | id_documento; processo_id; tipo_documento; nome; data | id_documento | 35 no exemplo | Anexo do app | Sim |
| Pendência | Pendência que trava o avanço da etapa | id_pendencia; processo_id; motivo; aberta_em; resolvida_em | id_pendencia | 2 no exemplo | Registro do app | Sim |
| Log | Histórico das ações | id; processo_id; acao; perfil; data_hora | id | — | App | Sim |

**O que precisa ser coletado:** Marcar por 2 semanas
**Quem libera o acesso:** Chefia imediata

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| SIGADOC | Sistema oficial | POLITEC | Sim | Um processo formalizado | 10 por semana | numero, data, tramitação | Contínua | Sim |
| SIAG | Sistema oficial | POLITEC | Sim | Um processo orçamentário | 10 por semana | numero, dotação | Contínua | Sim |
| Planilha de conferência | Planilha | Aquisição | Sim | Um processo por linha | 10 | numero, etapa, prazo | Semanal | Não |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | Números do SIGADOC e do SIAG são obrigatórios e únicos | No registro | Nenhuma | Sistema | Validação |
| RN02 | A etapa só é concluída com os documentos que ela exige | Ao concluir a etapa | Nenhuma | Sistema | Negócio |
| RN03 | Pendência aberta impede o avanço da etapa | Ao concluir a etapa | Resolvida a pendência | Sistema | Negócio |
| RN04 | O processo fica atrasado quando passa o prazo em dias corridos | No painel | Processo concluído | Sistema | Cálculo |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/painel | Painel | Ver a fila por etapa, os atrasados e as pendências | Chefia | Processos, prazos e pendências | Filtrar e abrir o processo | RN04 | Tela | Contagens conferem com a base | Sim |
| #/processo/novo | Nova aquisição | Registrar o processo com SIGADOC e SIAG | Requisitante e compras | Números, objeto, unidade, responsável e prazo | Salvar | RN01 | Tela | Processo criado no DFD | Sim |
| #/processo/:id | Processo | Anexar documentos e concluir etapas | Compras | Etapa, documentos e pendências | Anexar e avançar | RN02, RN03 | Tela | Avança só com documento e sem pendência | Sim |
| #/processos | Lista de processos | Consultar e filtrar | Todos | Etapa, situação e busca | Filtrar | — | Tela | Resultado confere com o filtro | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo de tramitação | Quanto tempo o processo leva do DFD à modalidade? | Soma dos dias por processo / processos concluídos | Registro do app | 8 h por processo (informado) | 30 dias | Medir 10 processos por 2 semanas |
| Retrabalho por pendência | Quantas pendências cada processo acumula? | Pendências / processos | Registro do app | não informada | menos de 1 por processo | Contar as pendências abertas |

**Período da linha de base:** Todos os registros dede 2024
**Campos de data e tempo que existem:** Entrada e data de envio

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** Planilha com automação
**Detalhe da stack:** Um único index.html (HTML, CSS e JS embutidos), com dados no IndexedDB do navegador e backup .json, publicado no GitHub Pages. O painel simula o fluxo do DFD à definição da modalidade; a integração com SIGADOC e SIAG fica fora do MVP.
**Hospedagem:** fluxo padronizado, acompanhamento de etapas, documentos, responsáveis, prazos e pendências, por ser uma solução viável para testar rapidamente, reduzir o retrabalho e melhorar a rastreabilidade sem exigir, inicialmente
**Custo e licenças:** Sem custos
**Contas e domínio:** o próprio servidor

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| Arquivo HTML local | Arquivo local | Computador da unidade | Zero | Equipe do projeto | Quem recebe o arquivo | IndexedDB | Uma cópia por setor | Backup manual em .json |
| GitHub Pages | Estática e gratuita | github.io | Zero | Equipe do projeto | Link do protótipo | Não tem | Baixa | Só o app, nunca os dados |


## 9. Restrições e LGPD

**Restrições:** As principais restrições conhecidas são o cumprimento obrigatório da legislação de compras públicas, a necessidade de manter as decisões e aprovações sob responsabilidade dos agentes públicos competentes, a dependência dos sistemas institucionais SIGADOC e SIAG, a necessidade de respeitar as permissões de acesso e a segurança das informações. No MVP, também há a limitação de não realizar integrações completas com os sistemas oficiais nem executar contratações reais, concentrando-se na simulação do fluxo, no controle de documentos, prazos, responsáveis e pendências.
**Dados pessoais tratados:** Matrícula funcional
**Base legal:** Lei nº. 14.133
**Retenção:** -
**Acesso e registro:** Login
**Requisitos marcados:** Acessibilidade

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** E-mail enviado pelo Diretor de Administração Sistêmica
**Fim:** O processo se encerra com a definição e formalização da contratação, após a conclusão das etapas administrativas, técnicas, orçamentárias e jurídicas necessárias, estando o processo devidamente instruído e apto à execução da aquisição ou contratação.
**Entradas:** O Documento de Formalização da Demanda (DFD), as informações do planejamento anual de contratações, o Estudo Técnico Preliminar (ETP), a análise de riscos, quando aplicável, o Termo de Referência (TR), as pesquisas e estimativas de preços, a comprovação de disponibilidade orçamentária e os demais documentos, registros e pareceres necessários à instrução e definição da modalidade de contratação.
**Saídas:** Contratação de serviço ou aquisição de bem e serviço.
**Volume:** 10
**Duração:** 8 horas
**Frequência:** Semanal
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| 1. Identificação da necessidade | Unidade requisitante | Demanda do setor | Registra a necessidade | Demanda formalizada | E-mail e planilha | Previsão no plano anual | Fila da unidade | — | Pouco |
| 2. DFD | Unidade requisitante e diretor-geral | Demanda formalizada | Elabora e assina o DFD | DFD assinado | Word e SIGADOC | Assinatura do diretor-geral | Aguardando assinatura | — | Não |
| 3. ETP, riscos e TR | Equipe de planejamento | DFD assinado | Elabora e revisa os documentos | ETP, risco e TR | Word e SIGADOC | Modelos institucionais | Revisão | — | Pouco |
| 4. Pesquisa de preços | Equipe de compras | TR aprovado | Pesquisa no Compras.gov.br e valida | Estimativa de preços | Compras.gov.br | Três cotações | Coleta | — | Pouco |
| 5. Formalização | Equipe de compras | Processo instruído | Cria o número no SIGADOC e no SIAG e verifica a dotação | Processo formalizado | SIGADOC e SIAG | Disponibilidade orçamentária | Fila dos sistemas | — | Sim, com apoio humano |
| 6. Análises e modalidade | Setores técnico, orçamentário e jurídico | Processo formalizado | Emite pareceres e define a modalidade | Processo apto à contratação | SIGADOC | Lei nº 14.133/2021 | Fila de análise | — | Não |

**Decisões e aprovações:** DFD pelo diretor-geral da POLITEC, a avaliação e aprovação, ETP e TR pelo coordenador de aquisições e contratos.
**Exceções:** -
**Já digitalizado:** Todo o sistema no SIAG

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** A POLITEC passará a contar com um processo de aquisição integrado, padronizado e rastreável, reduzindo prazos, retrabalho e falhas, com maior transparência e segurança nas contratações públicas.
**Mudança principal:** A centralização e automatização do fluxo de aquisições da POLITEC, permitindo acompanhar todas as etapas, documentos, responsáveis, aprovações e prazos em um único processo integrado, reduzindo atrasos, falhas e retrabalho.
**O que fica igual:** Permanecem inalterados o cumprimento da legislação vigente, as etapas obrigatórias da contratação pública, as competências dos setores envolvidos, a responsabilidade dos servidores e das autoridades pelas decisões e aprovações, bem como os princípios da legalidade, transparência, economicidade e controle dos atos administrativos.
**O que não pode mudar:** Devem ser mantidos o cumprimento da legislação vigente, a transparência, a rastreabilidade dos atos administrativos, a segregação de funções, a segurança das informações e a responsabilidade dos servidores e das autoridades competentes pelas análises, decisões e aprovações do processo de aquisição da POLITEC.
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| DFD a TR | Checklist e modelos padronizados com os campos do processo | A pessoa assistida pela máquina | Menos retrabalho e devolução | Médio |
| Pesquisa de preços | Conferência automática de três cotações e da estimativa | A pessoa assistida pela máquina | Menos erro de preço | Médio |
| Acompanhamento | Painel com etapa, prazo e pendência por processo | A máquina (automação) | Atraso visível e cobrança antes do vencimento | Baixo |
| SIGADOC e SIAG | Registro do número e da data no processo | A pessoa assistida pela máquina | Rastreabilidade | Baixo |

**Piloto do TO-BE:** O TO-BE será testado inicialmente em ambiente controlado na POLITEC, com um projeto-piloto utilizando processos de aquisição de menor complexidade, por meio da simulação das etapas, dos documentos, das aprovações e do acompanhamento de prazos. Participarão servidores das unidades requisitantes, da equipe de compras e dos setores técnico, orçamentário e jurídico. Serão avaliados o tempo de tramitação, a redução de retrabalho, a identificação de pendências e a rastreabilidade das informações, para validar o novo fluxo antes de sua implantação definitiva.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** A principal hipótese é que a padronização e o acompanhamento centralizado das etapas, dos documentos, dos responsáveis e dos prazos reduzirão o retrabalho e o tempo de tramitação dos processos de aquisição da POLITEC.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Lei nº 14.133/2021 | Norma ou lei | Planalto | 2021 | Licitações e contratos administrativos | Fundamenta as etapas, as análises e a decisão da modalidade | Sim |
| Processos de 2025 | Documento interno | DSI | 2024 | Base de processos para a linha de base | Sustenta o volume e o prazo | Sim |

**Lacunas:** -
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| INÍCIO DA AQUISIÇÃO | 05/12/2026 | Kasteline Goncalves | CADA SETOR | Em andamento |
| Início da aquisição | 05/12/2026 | Kasteline Gonçalves | Cada setor | Planejado |
| Modelos de DFD, ETP e TR recebidos | 20/11/2026 | Aquisições | Documentos oficiais | Planejado |
| Protótipo com etapas e documentos | 11/12/2026 | Kasteline | Regras definidas | Planejado |
| Piloto com 10 processos simulados | 29/01/2027 | Chefia | Aceite | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Não aceite pelos outros servidores | Média | Médio | Piloto com dados fictícios e capacitação dos servidores |
| Modelos documentais desatualizados | Média | Alto | Confirmar os modelos oficiais com a aquisição antes do Sprint 3 |
| Processo registrado em duplicidade | Média | Médio | Validar o SIGADOC único no cadastro (RN01) |

**Apoio necessário:** É necessário o apoio da direção-geral da POLITEC para autorizar o projeto piloto, dos setores de compras e planejamento para validar o fluxo e os documentos, das áreas técnica, orçamentária e jurídica para verificar os requisitos, e da equipe de tecnologia da informação para avaliar a viabilidade técnica, a segurança dos dados e as possíveis integrações com o SIGADOC e o SIAG.
**Aprendizado necessário:** É necessário aprofundar o conhecimento sobre o fluxo real de aquisições da POLITEC, a legislação vigente de compras públicas, os procedimentos e modelos de DFD, ETP e TR, as funcionalidades do SIGADOC e do SIAG, as possibilidades de automação de processos, a segurança da informação e os critérios para medir prazos, retrabalho e eficiência, além de aprender a desenvolver e testar o MVP com os servidores envolvidos.

# Anexo D — A defesa

**Frase de defesa:** A automatização e a padronização do processo de aquisição da POLITEC reduzirão o retrabalho, aumentarão a transparência e melhorarão o controle e a eficiência das contratações públicas.
**Provas:** 1. Demora na tramitação: necessidade de analisar os prazos de cada etapa nos registros do SIGADOC e do SIAG para identificar gargalos.
**Piloto:** A proposta será testada por meio de um projeto-piloto com processos de aquisição simulados da POLITEC, comparando o fluxo atual com o fluxo automatizado do MVP. Serão avaliados o tempo de execução das etapas, a quantidade de erros e correções documentais, o número de pendências identificadas e a facilidade de acompanhamento dos processos pelos servidores, verificando se a solução reduz o retrabalho e melhora a rastreabilidade das informações.
**Maior risco:** O maior risco é a resistência dos servidores à mudança e a dificuldade de integrar o novo fluxo aos sistemas SIGADOC e SIAG; para mitigá-lo, será realizado um projeto-piloto com dados fictícios, capacitação dos usuários e validação gradual do processo, mantendo as aprovações sob responsabilidade dos agentes públicos competentes.

# Anexo E — Documentos enviados

**Descrição dos documentos:** Fluxo de trabalho na aquisição:
**O que ainda falta:** Para desenvolver o MVP, ainda são necessários os modelos oficiais de DFD, ETP e TR utilizados pela POLITEC, o fluxo real de tramitação das aquisições, a definição dos responsáveis e das permissões de acesso, os critérios de aprovação e os prazos de cada etapa. Também é necessário validar com os setores envolvidos quais funcionalidades são prioritárias, obter exemplos de processos concluídos sem dados sensíveis e definir os recursos tecnológicos disponíveis para construir e testar o protótipo.
